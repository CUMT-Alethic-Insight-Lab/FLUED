"""读出链复训协议（队列唯一闸门，2026-08-18；口令：验收线 = 超过 62% 线性
探针地板——E73-A6 实测写值 v 的线性读字节 acc slot0 = 0.6185）。

背景（E73 oracle 判决 + E75 手术验收）：c 格 V 通道的写值本身携带字节内
容（线性探针 0.62），但 trained 读出链（固定 query → realign → decoder_in
→ decoder）只读出 10% 档；oracle 完美状态/岭回归解混都救不了——锁在
读出链。本脚本只复训 {realign, decoder_in, decoder}（decoder.byte_lookup
除外，它是共享冻结前端），其余全冻结；backbone 默认不放
（--unfreeze-backbone-last-n 为防翻车设计 2 的备用旋钮，默认 0）。

防翻车设计（用户裁定）：
1. 对称 OOD 防护 + μ 课程（修正一，2026-08-19）：每个样本按
   --oracle-frac（余弦退火 0.8→--oracle-frac-end，默认回调到 0.3）在
   **oracle 态**与**自然态**（真实 delta 递推）之间二选一喂链；且 oracle
   态不再是单一无侵蚀累计态——生成时对键做受控相干混合
   （k(λ)=normalize(√(1-λ²)·k_real+λ·z)，混合器复用
   measure_readout_lockin_curve.py），λ 档位表 --mu-lambda-grid 覆盖实测
   μ≈0.9→0.07（锁死曲线全轴），每步均匀抽档，让链一次学成几何鲁棒。
2. backbone 冻结优先（--unfreeze-backbone-last-n 旋钮备用，默认 0）。
3. 验收线：eval direct_acc（state 链，自然态口径）必须超过写死的线性探针
   地板 0.62（logs 注释常量）；eval 日志加 plateau_acc（末 3 次 eval 自然
   态均值）供"above_floor 后看平台"判读。
4. checkpoint 只读；复训产物（三模块 state_dict）单独落 --out-dir，绝不
   回写原 ckpt；独立脚本，不动任何生产训练路径。

损失/口径：与 s1 的 direct 任务对齐——v=state 粗粒度格的累积 as-encoded
目标网格（make_cumulative_retention_targets(source, byte_mask, ...)），
cond = decoder_in(realign(q·S)) + 页内 chunk_pos；eval = 训练终评同口径
16 窗（StreamingReconstructionDataset seed+9999 前 N 窗，_MASK_GENERATOR
重播种 eval_mask_seed=1042）。fp32、无 autocast。

Usage:
  CPU 冒烟: python tools/train/v3_6/retrain_readout_chain.py --steps 20 --seq-len 512 \
      --eval-windows 2 --eval-every 10 --log-every 5 --device cpu \
      --out-dir checkpoints/_smoke_retrain_readout
  正式（GPU 空档，~5K 步）: 见返回命令行（c 格未手术版 / 手术版两对象）
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


def unfreeze_readout_chain(model, backbone_last_n: int = 0) -> list[str]:
    """Freeze everything, then unfreeze {realign, decoder_in, decoder} (minus
    decoder.byte_lookup — a shared reference to the frozen byte front end).
    backbone_last_n>0 additionally unfreezes the last n SLM self-attention
    blocks (防翻车设计 2 的备用旋钮; default 0 = backbone stays frozen)."""
    for p in model.parameters():
        p.requires_grad_(False)
    names = []
    for name, p in model.named_parameters():
        if name.startswith("decoder.byte_lookup."):
            continue  # shared frozen front end
        if name.startswith(TRAINABLE_PREFIXES):
            p.requires_grad_(True)
            names.append(name)
    if backbone_last_n > 0:
        blocks = getattr(model.backbone, "self_blocks", None)
        if blocks is None:
            raise ValueError("--unfreeze-backbone-last-n requires the slm backbone")
        for blk in blocks[-backbone_last_n:]:
            for name, p in blk.named_parameters():
                p.requires_grad_(True)
                names.append(f"backbone.self_blocks.{name}")
    return names


def oracle_frac_at(step: int, total: int, start: float, end: float, anneal_steps: int = 0) -> float:
    """Cosine anneal start→end over anneal_steps (default = total)."""
    T = anneal_steps or total
    t = min(step / max(T, 1), 1.0)
    return end + 0.5 * (start - end) * (1.0 + math.cos(math.pi * t))


@torch.no_grad()
def _states_for(model, source: torch.Tensor, use_oracle: bool, lam: float | None = None, z: torch.Tensor | None = None):
    """Frozen producers: front end -> memory -> write gates -> per-chunk states
    (natural delta recurrence, or oracle cumsum). μ 课程（修正一）：oracle 态
    的键先按 λ 与随机方向 z 做相干混合（锁死曲线全轴覆盖）再累计；
    lam=None 保持原始纯累计形态（默认/测试兼容）。"""
    chunks, memory, _index = _front_end(model, source)
    n_real = int(chunks.chunk_mask[0].sum())
    gates = model.write_head(memory)
    sm = model.state_machine
    if not use_oracle:
        return chunks, n_real, trained_states(sm, gates, n_real)
    if lam is not None:
        if z is None:
            z = torch.nn.functional.normalize(torch.randn(gates["k"].shape, device=gates["k"].device), dim=-1)
        gates = {**gates, "k": mix_keys(gates["k"].float(), z, lam)}
    return chunks, n_real, oracle_states(gates, n_real)


def _chain_logits(model, chunks, n_real: int, S: torch.Tensor) -> torch.Tensor:
    """The retrained chain WITH gradient: fixed readout query -> realign ->
    decoder_in -> +page-local chunk_pos -> decoder. S is a constant input."""
    sm = model.state_machine
    q = sm.readout_query.float()  # frozen parameter used as a constant
    reads = torch.einsum("qhk,bnhkv->bnqhv", q, S.float())
    read = reads.reshape(S.size(0), n_real, q.size(0), -1).to(S.dtype)
    v_rows = sm.realign(read).mean(dim=2)  # (B, n, d_pack) — grad starts here
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_real]
    cond = model.decoder_in(v_rows) + pos
    return model.decoder(cond, chunks.token_mask[:, :n_real])


def _direct_loss(model, ns, chunks, n_real: int, source, byte_mask, logits) -> torch.Tensor:
    """s1 direct-task form for the coarse-V (v=state) grid: cumulative
    as-encoded targets."""
    targets, slot_mask, _masked, _t = s1.make_cumulative_retention_targets(
        source, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    return s1._ce(logits, targets[:, :n_real], slot_mask[:, :n_real])


def train_step(model, ns, clean: torch.Tensor, byte_mask: torch.Tensor, frac: float, opt, rng: random.Random, grad_clip: float, mu_lambda_grid: list | None = None) -> dict:
    model.train()
    source = clean.masked_fill(byte_mask, MASK_ID)
    use_oracle = rng.random() < frac
    lam = rng.choice(mu_lambda_grid) if (use_oracle and mu_lambda_grid) else None  # μ 课程：每步均匀抽相干档
    chunks, n_real, S = _states_for(model, source, use_oracle, lam=lam)
    logits = _chain_logits(model, chunks, n_real, S)
    loss = _direct_loss(model, ns, chunks, n_real, source, byte_mask, logits)
    opt.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], grad_clip)
    opt.step()
    return {"loss": float(loss.detach()), "use_oracle": use_oracle, "frac": frac, "n_real": n_real, "mu_lambda": lam}


@torch.no_grad()
def evaluate_chain(model, ns, windows, masks, device) -> dict:
    """Eval-seed-1042 protocol: the chain on NATURAL states (deployment form)
    and on ORACLE states (rescue ceiling), direct cumulative-grid acc."""
    model.eval()
    out = {}
    for tag, use_oracle in (("natural", False), ("oracle", True)):
        hits = slots = 0
        for clean, bm in zip(windows, masks):
            clean, bm = clean.to(device), bm.to(device)
            source = clean.masked_fill(bm, MASK_ID)
            chunks, n_real, S = _states_for(model, source, use_oracle)
            logits = _chain_logits(model, chunks, n_real, S)
            targets, slot_mask, _m, _t = s1.make_cumulative_retention_targets(
                source, bm, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
            )
            pred = logits.argmax(dim=-1)
            sel = slot_mask[:, :n_real]
            hits += int((pred.eq(targets[:, :n_real]) & sel).sum())
            slots += int(sel.sum())
        out[f"direct_acc_{tag}"] = round(hits / max(slots, 1), 4)
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
    p.add_argument("--unfreeze-backbone-last-n", type=int, default=0)
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
    if args.seq_len:
        ns.seq_len = args.seq_len
    if args.data_path:
        ns.data_path = args.data_path
    names = unfreeze_readout_chain(model, args.unfreeze_backbone_last_n)
    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[retrain] {Path(args.run_dir).name} step={ckpt_step}: trainable {n_trainable} params in {len(names)} tensors "
          f"(backbone_last_n={args.unfreeze_backbone_last_n})", flush=True)

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
            losses.append(r["loss"])
            if step % args.log_every == 0 or step == 1:
                row = {"step": step, "loss": round(sum(losses) / len(losses), 4), "oracle_frac": round(frac, 4),
                       "use_oracle_last": r["use_oracle"], "mu_lambda_last": r["mu_lambda"]}
                print(f"[retrain] {row}", flush=True)
                log_fh.write(json.dumps({"losses_window": len(losses), **row}) + "\n")
                log_fh.flush()
                losses = []
            if step % args.eval_every == 0 or step == args.steps:
                ev = evaluate_chain(model, ns, eval_windows, eval_masks, device)
                eval_natural_history.append(ev["direct_acc_natural"])
                plateau = sum(eval_natural_history[-3:]) / min(len(eval_natural_history), 3)
                row = {"step": step, "eval": ev, "floor": LINEAR_PROBE_FLOOR,
                       "plateau_acc": round(plateau, 4),
                       "verdict": "PASS" if ev["direct_acc_natural"] > LINEAR_PROBE_FLOOR else "below_floor"}
                print(f"[retrain][eval] {row}", flush=True)
                log_fh.write(json.dumps({"eval": row}) + "\n")
                log_fh.flush()

    # save ONLY the retrained modules (byte_lookup rows stripped) — the source
    # checkpoint is never written back
    sd = {
        "realign": model.state_machine.realign.state_dict(),
        "decoder_in": model.decoder_in.state_dict(),
        "decoder": {k: v for k, v in model.decoder.state_dict().items() if not k.startswith("byte_lookup.")},
    }
    torch.save(
        {"step": args.steps, "modules": sd, "source_run": Path(args.run_dir).name, "args": vars(args)},
        out_dir / "retrained_readout.pt",
    )
    print(f"[retrain] done -> {out_dir / 'retrained_readout.pt'} ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
