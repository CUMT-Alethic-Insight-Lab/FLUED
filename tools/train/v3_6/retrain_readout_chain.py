"""读出链复训协议 —— fork 1（补全形态，2026-08-19 用户拍板；前身为 2026-08-18
的 direct 形态复训器，μ 课程首跑 plateau 0.19 远低于 62% 地板后裁定换形）。

背景（E73 oracle 判决 + 锁死定量图）：c 格 V 通道写值内容在（线性探针
0.62 档），trained 读出链只读出 10% 档，且对全 μ 轴无响应——锁在
realign/decoder 接口。fork 1 把复训损失从 direct 形态换成**补全形态**：
cond = backbone_out + pos（s1 completion 形态），累积保持 CLEAN 目标网格
（make_cumulative_retention_targets(clean, ...)）——梯度真正流进主干。
默认冻结面 = {realign, decoder_in, decoder（除共享 byte_lookup）, **主干
全放**}；--freeze-backbone 恢复旧冻结面（与 --unfreeze-backbone-last-n
互斥，freeze 优先）。K 侧限定 k=index 格（护栏一的消融对象即直通 K 行）。

护栏（用户裁定）：
1. 通道消融评测：eval 双报——(a) full：主干正常消费全部 store 行（工程
   上限）；(b) state-only：置零注意力 K 行（c 格 = 直通 index 行；复用模型
   自带 k_block_eval eval 开关，影响最小、不碰 direct 路径口径），只留状态
   读出行承载内容（架构结论）。注：K-seed 格的种子通道按构造保留 index
   内容，消融只作用于注意力键。两版都报 completion byte_acc。
2. backbone 入链默认（fork 1 的目的）+ 旋钮可退回。
3. 验收线：completion_acc_natural_full 对照写死的线性探针地板 0.6185
   （日志注记：地板是 direct 口径 slot0 探针，网格不同，仅作参照）；eval
   日志加 plateau_acc（末 3 次 eval 自然态 full 臂均值）。
4. checkpoint 只读；复训产物（realign/decoder_in/decoder[/backbone] 的
   state_dict）单独落 --out-dir，绝不回写原 ckpt；独立脚本，不动生产路径。

继承自前身的防翻车设计：oracle/自然态逐样本二选一（--oracle-frac 余弦退火
0.8→0.3）；oracle 态的 μ 课程（--mu-lambda-grid 覆盖锁死曲线全轴，每步
均匀抽档）；eval = 训练终评同口径 16 窗（eval seed 1042）。fp32、无
autocast。

Usage:
  CPU 冒烟: python tools/train/v3_6/retrain_readout_chain.py --steps 20 --seq-len 512 \
      --eval-windows 2 --eval-every 10 --log-every 5 --device cpu \
      --out-dir checkpoints/_smoke_retrain_readout
  正式（GPU，20K 步）: 见任务返回命令行（completion_ubb 后缀，c 格两版本）
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
from flued.data import StreamingReconstructionDataset  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    load_model,
    oracle_states,
    trained_states,
)
from tools.analysis.v3_6.measure_readout_lockin_curve import mix_keys  # noqa: E402

LINEAR_PROBE_FLOOR = 0.6185  # E73-A6: write-value linear byte probe, slot0 acc
TRAINABLE_PREFIXES = ("state_machine.realign.", "decoder_in.", "decoder.")


def unfreeze_readout_chain(model, backbone_last_n: int = 0, freeze_backbone: bool = False) -> list[str]:
    """Freeze everything, then unfreeze {realign, decoder_in, decoder} (minus
    decoder.byte_lookup — a shared reference to the frozen byte front end).
    fork 1 (2026-08-19, user-ruled): the loss is the COMPLETION form
    (cond = backbone_out + pos), so the backbone is IN the chain by default —
    unfrozen in full. backbone_last_n>0 restricts to the last n self-attention
    blocks; freeze_backbone=True restores the pre-fork-1 surface (backbone
    frozen; the two flags are mutually exclusive, freeze wins loudly)."""
    if freeze_backbone and backbone_last_n > 0:
        raise ValueError("--freeze-backbone and --unfreeze-backbone-last-n are mutually exclusive")
    for p in model.parameters():
        p.requires_grad_(False)
    names = []
    for name, p in model.named_parameters():
        if name.startswith("decoder.byte_lookup."):
            continue  # shared frozen front end
        if name.startswith(TRAINABLE_PREFIXES):
            p.requires_grad_(True)
            names.append(name)
    if not freeze_backbone:
        if backbone_last_n > 0:
            blocks = getattr(model.backbone, "self_blocks", None)
            if blocks is None:
                raise ValueError("--unfreeze-backbone-last-n requires the slm backbone")
            targets = blocks[-backbone_last_n:]
            for name, p in model.named_parameters():
                if any(p is q for blk in targets for q in blk.parameters()):
                    p.requires_grad_(True)
                    names.append(name)
        else:
            for name, p in model.backbone.named_parameters():
                p.requires_grad_(True)
                names.append(f"backbone.{name}")
    return names


def oracle_frac_at(step: int, total: int, start: float, end: float, anneal_steps: int = 0) -> float:
    """Cosine anneal start→end over anneal_steps (default = total)."""
    T = anneal_steps or total
    t = min(step / max(T, 1), 1.0)
    return end + 0.5 * (start - end) * (1.0 + math.cos(math.pi * t))


@torch.no_grad()
def _states_for(model, source: torch.Tensor, use_oracle: bool, lam: float | None = None, z: torch.Tensor | None = None):
    """Frozen producers: front end -> memory -> write gates -> per-chunk states
    (natural delta recurrence, or oracle cumsum) + the K store source rows
    (index rows for the c grids; a constant from the frozen summarizer).
    μ 课程（修正一）：oracle 态的键先按 λ 与随机方向 z 做相干混合（锁死曲线
    全轴覆盖）再累计；lam=None 保持原始纯累计形态（默认/测试兼容）。"""
    chunks, memory, index = _front_end(model, source)
    n_real = int(chunks.chunk_mask[0].sum())
    gates = model.write_head(memory)
    sm = model.state_machine
    k_rows = index[:, :n_real]  # c grids: k=index (direct passthrough K source)
    if not use_oracle:
        return chunks, n_real, trained_states(sm, gates, n_real), k_rows
    if lam is not None:
        if z is None:
            z = torch.nn.functional.normalize(torch.randn(gates["k"].shape, device=gates["k"].device), dim=-1)
        gates = {**gates, "k": mix_keys(gates["k"].float(), z, lam)}
    return chunks, n_real, oracle_states(gates, n_real), k_rows


def _chain_logits(model, chunks, n_real: int, S: torch.Tensor, k_rows: torch.Tensor) -> torch.Tensor:
    """fork 1 COMPLETION form (gradients live): fixed readout query -> realign
    -> v_rows; SLM backbone cross-reads the store (K = k_rows, V = v_rows) ->
    backbone_out + page-local chunk_pos -> decoder. S and k_rows are constant
    inputs; the gradient starts at realign and flows through the backbone."""
    sm = model.state_machine
    q = sm.readout_query.float()  # frozen parameter used as a constant
    reads = torch.einsum("qhk,bnhkv->bnqhv", q, S.float())
    read = reads.reshape(S.size(0), n_real, q.size(0), -1).to(S.dtype)
    v_rows = sm.realign(read).mean(dim=2)  # (B, n, d_pack) — grad starts here
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_real]
    backbone_out = model.backbone(k_rows, v_rows, chunks.chunk_mask[:, :n_real], pos)
    cond = backbone_out + pos
    return model.decoder(cond, chunks.token_mask[:, :n_real])


def _direct_loss(model, ns, chunks, n_real: int, clean, byte_mask, logits) -> torch.Tensor:
    """fork 1: completion-task form — s1's coarse-V completion grid: cumulative
    CLEAN targets (make_cumulative_retention_targets(clean, byte_mask, ...))."""
    targets, slot_mask, _masked, _t = s1.make_cumulative_retention_targets(
        clean, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    return s1._ce(logits, targets[:, :n_real], slot_mask[:, :n_real])


def train_step(model, ns, clean: torch.Tensor, byte_mask: torch.Tensor, frac: float, opt, rng: random.Random, grad_clip: float, mu_lambda_grid: list | None = None) -> dict:
    model.train()
    source = clean.masked_fill(byte_mask, MASK_ID)
    use_oracle = rng.random() < frac
    lam = rng.choice(mu_lambda_grid) if (use_oracle and mu_lambda_grid) else None  # μ 课程：每步均匀抽相干档
    chunks, n_real, S, k_rows = _states_for(model, source, use_oracle, lam=lam)
    logits = _chain_logits(model, chunks, n_real, S, k_rows)
    loss = _direct_loss(model, ns, chunks, n_real, clean, byte_mask, logits)
    opt.zero_grad(set_to_none=True)
    if not torch.isfinite(loss):
        # NaN/Inf guard (2026-08-19, run-1 divergence lesson): skip the step —
        # metrics must not advance as if an optimizer step succeeded (AGENTS.md
        # pitfall 3). Extreme oracle-state norms (collapsed-key cumsum, |S|~1e3)
        # can push the now-trainable backbone into fp32 divergence.
        return {"loss": None, "skipped": True, "use_oracle": use_oracle, "frac": frac, "n_real": n_real, "mu_lambda": lam}
    loss.backward()
    torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], grad_clip)
    opt.step()
    return {"loss": float(loss.detach()), "skipped": False, "use_oracle": use_oracle, "frac": frac, "n_real": n_real, "mu_lambda": lam}


@torch.no_grad()
def _eval_acc(model, ns, windows, masks, device, use_oracle: bool, state_only: bool) -> float:
    """One eval cell: natural/oracle states x full-store/state-only ablation.
    state_only = 护栏一 (b) 臂：zero the attention K rows (the direct-source
    index rows on the c grids) via the model's k_block_eval switch, so only
    the state-readout V rows carry content (uniform attention). NOTE: the
    k-seed variant's seed channel keeps index-row content by construction —
    the ablation is attention-only."""
    bb = model.backbone
    prev = getattr(bb, "k_block_eval", False)
    if state_only:
        bb.k_block_eval = True
    hits = slots = 0
    try:
        for clean, bm in zip(windows, masks):
            clean, bm = clean.to(device), bm.to(device)
            source = clean.masked_fill(bm, MASK_ID)
            chunks, n_real, S, k_rows = _states_for(model, source, use_oracle)
            logits = _chain_logits(model, chunks, n_real, S, k_rows)
            targets, slot_mask, _m, _t = s1.make_cumulative_retention_targets(
                clean, bm, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
            )
            pred = logits.argmax(dim=-1)
            sel = slot_mask[:, :n_real]
            hits += int((pred.eq(targets[:, :n_real]) & sel).sum())
            slots += int(sel.sum())
    finally:
        bb.k_block_eval = prev
    return round(hits / max(slots, 1), 4)


@torch.no_grad()
def evaluate_chain(model, ns, windows, masks, device) -> dict:
    """Eval-seed-1042 protocol, fork 1: completion-form byte acc on
    {natural, oracle} x {full store (工程上限), state-only (架构结论)}."""
    model.eval()
    out = {}
    for tag, use_oracle in (("natural", False), ("oracle", True)):
        for arm, state_only in (("full", False), ("stateonly", True)):
            out[f"completion_acc_{tag}_{arm}"] = _eval_acc(model, ns, windows, masks, device, use_oracle, state_only)
    return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default="checkpoints/v37_c_is_v371_20k_ctx4096_20260817")
    p.add_argument("--out-dir", default="checkpoints/retrain_readout_c_v371_20260818")
    p.add_argument("--data-path", default="", help="empty = the checkpoint's data_path")
    p.add_argument("--steps", type=int, default=20000)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--oracle-frac-start", type=float, default=0.8)
    p.add_argument("--oracle-frac-end", type=float, default=0.3, help="修正一 (2026-08-19): anneal endpoint raised 0.1 -> 0.3")
    p.add_argument("--oracle-anneal-steps", type=int, default=0, help="0 = --steps")
    p.add_argument("--mu-lambda-grid", default="0.2,0.45,0.65,0.85,1.0",
                   help="μ 课程：oracle 态键相干混合 λ 档位（实测 μ≈0.9→0.07，锁死曲线全轴）；"
                   "每步均匀抽档。空串 = 退回纯累计态（修正一之前的形态）")
    p.add_argument("--eval-every", type=int, default=200)
    p.add_argument("--eval-windows", type=int, default=16)
    p.add_argument("--log-every", type=int, default=50)
    p.add_argument("--seq-len", type=int, default=0, help="0 = the checkpoint's (4096); smaller for CPU smoke")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--grad-clip", type=float, default=1.0)
    p.add_argument("--unfreeze-backbone-last-n", type=int, default=0,
                   help="0 = fork 1 default: backbone FULLY in the chain; >0 = only the last n self-attention blocks")
    p.add_argument("--freeze-backbone", action="store_true",
                   help="reverse knob: restore the pre-fork-1 surface (backbone frozen)")
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    return p


def main() -> None:
    args = build_parser().parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, ckpt_step = load_model(Path(args.run_dir), device)
    if getattr(ns, "v_row_source", "") != "state":
        raise ValueError(f"readout-chain retrain targets v=state cells; {Path(args.run_dir).name} has v_row_source={ns.v_row_source!r}")
    if getattr(ns, "k_row_source", "") != "index":
        raise ValueError(
            f"fork 1 guardrail-1 (state-only ablation) is defined for k=index cells "
            f"(direct K rows are what the ablation removes); got k_row_source={ns.k_row_source!r}"
        )
    if args.seq_len:
        ns.seq_len = args.seq_len
    if args.data_path:
        ns.data_path = args.data_path
    names = unfreeze_readout_chain(model, args.unfreeze_backbone_last_n, freeze_backbone=args.freeze_backbone)
    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[retrain] {Path(args.run_dir).name} step={ckpt_step}: trainable {n_trainable} params in {len(names)} tensors "
          f"(freeze_backbone={args.freeze_backbone}, backbone_last_n={args.unfreeze_backbone_last_n})", flush=True)

    opt = torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=args.lr)
    mix_rng = random.Random(args.seed + 7)
    s1._MASK_GENERATOR.manual_seed(args.seed)

    train_ds = StreamingReconstructionDataset(
        file_path=ns.data_path, seq_len=ns.seq_len,
        samples_per_worker=max(args.steps * 2, 2000), seed=args.seed,
    )
    train_iter = iter(torch.utils.data.DataLoader(train_ds, batch_size=1, shuffle=False, num_workers=0))
    eval_windows = build_eval_windows(ns, args.eval_windows)
    eval_masks = build_masks(eval_windows, ns)

    log_path = out_dir / "train_log.jsonl"
    mu_grid = [float(x) for x in args.mu_lambda_grid.split(",") if x.strip()]
    eval_natural_history: list[float] = []
    nan_skips = 0
    with log_path.open("a", encoding="utf-8") as log_fh:
        losses = []
        for step in range(1, args.steps + 1):
            clean = next(train_iter)[0].to(device)
            byte_mask = s1.make_mixed_mask(
                clean.cpu(), ns.mask_prob,
                char_frac=getattr(ns, "mask_char_frac", 0.4),
                char_span_max=getattr(ns, "mask_char_span_max", 3),
                tokenizer=s1._BPE_TOKENIZER, generator=s1._MASK_GENERATOR,
            ).to(device)
            frac = oracle_frac_at(step, args.steps, args.oracle_frac_start, args.oracle_frac_end, args.oracle_anneal_steps)
            r = train_step(model, ns, clean, byte_mask, frac, opt, mix_rng, args.grad_clip, mu_lambda_grid=mu_grid)
            if r["skipped"]:
                nan_skips += 1  # NaN/Inf step skipped: metrics do not advance
            else:
                losses.append(r["loss"])
            if step % args.log_every == 0 or step == 1:
                row = {"step": step, "loss": round(sum(losses) / len(losses), 4) if losses else None,
                       "oracle_frac": round(frac, 4), "use_oracle_last": r["use_oracle"],
                       "mu_lambda_last": r["mu_lambda"], "nan_skips": nan_skips}
                print(f"[retrain] {row}", flush=True)
                log_fh.write(json.dumps({"losses_window": len(losses), **row}) + "\n")
                log_fh.flush()
                losses = []
            if step % args.eval_every == 0 or step == args.steps:
                ev = evaluate_chain(model, ns, eval_windows, eval_masks, device)
                primary = ev["completion_acc_natural_full"]
                eval_natural_history.append(primary)
                plateau = sum(eval_natural_history[-3:]) / min(len(eval_natural_history), 3)
                row = {"step": step, "eval": ev, "floor": LINEAR_PROBE_FLOOR,
                       "floor_note": "floor = E73-A6 write-value linear probe (slot0, 0.6185); "
                       "completion-form acc is a different grid (clean cumulative) — reference only",
                       "plateau_acc": round(plateau, 4),
                       "verdict": "PASS" if primary > LINEAR_PROBE_FLOOR else "below_floor"}
                print(f"[retrain][eval] {row}", flush=True)
                log_fh.write(json.dumps({"eval": row}) + "\n")
                log_fh.flush()

    # save ONLY the retrained modules (byte_lookup rows stripped) — the source
    # checkpoint is never written back. fork 1: the backbone is in the chain by
    # default, so it is persisted too (skipped when --freeze-backbone).
    sd = {
        "realign": model.state_machine.realign.state_dict(),
        "decoder_in": model.decoder_in.state_dict(),
        "decoder": {k: v for k, v in model.decoder.state_dict().items() if not k.startswith("byte_lookup.")},
    }
    if not args.freeze_backbone:
        sd["backbone"] = model.backbone.state_dict()
    torch.save(
        {"step": args.steps, "modules": sd, "source_run": Path(args.run_dir).name, "args": vars(args)},
        out_dir / "retrained_readout.pt",
    )
    print(f"[retrain] done -> {out_dir / 'retrained_readout.pt'} ({time.time() - t0:.0f}s, nan_skips={nan_skips})", flush=True)


if __name__ == "__main__":
    main()
