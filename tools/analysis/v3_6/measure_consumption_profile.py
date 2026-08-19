"""附录 A 剖面测量（fork 2 实施前置，裁定 6，2026-08-19）——对冻结 checkpoint
测两张剖面，默认对象 v37ks_b_sm_v372_cloze_tokcenter（b 格：k=state,
v=memory, seed=k）。

1. 层级消费剖面：对 backbone 每个 block 与 decoder 每层的**输入**做 chunk 轴
   置乱（--mode shuffle，默认；边际分布不变、chunk-内容配对打碎，与接口探针
   的垃圾态同一纪律）或置零（--mode zero）干预，测补全 logits 的
   KL(base‖干预) 偏移与字节 acc 掉幅——回答"哪几层真的在消费读出/条件信号"。
   干预点（每窗同一固定置换，全站点共用，站点间差异不含置换采样噪声）：
     k_rows / v_rows  store 两通道入口行（b 格：k=状态读出行，v=memory 直连行）
     bb_cross1        block-1 cross-read 入口隐态（seed+pos，seed 源由
                      seed_source 决定——b 格 seed=k，读出信号从此入链）
     bb_self{i}       self-attention block i 入口隐态
     dec{j}           decoder 第 j 层入口隐态（decoder 把 chunk 轴折叠进
                      batch 维，hook 内还原 (B,C,...) 再沿 chunk 轴干预）
   backbone 前向是逐算子镜像（SLMBackbone.forward 的 block 是内联代码，
   ModuleDict 无 forward 可挂钩），site=None 与生产前向逐位一致（单测钉死
   parity）；decoder 各层是标准 nn.Module，用 forward_pre_hook 干预。
2. 逐 slot 信息剖面：接口线性探针（E73-A6 岭回归 2-fold 口径，real−garbage）
   从 slot0-3 扩到段内全部 slot（字节位置 0..max_span-1），报告前
   --report-slots（默认 32）个 slot 的信息量曲线。接口向量 = 状态通道的读出
   行（k=state → k_rows；v=state → v_rows；realign 之后、align_k/align_v
   之前）。garbage = 同一批读出行沿 chunk 轴打乱（readout 逐 chunk 独立，
   打乱读出行 ≡ 打乱状态再读出，与接口探针的垃圾态严格同构）。

口径：16 窗 eval seed 1042（build_eval_windows/build_masks，与接口探针/
oracle 判决/复训器 eval 同源）；补全 acc 用 clean 累积保留网格
（make_cumulative_retention_targets(clean, byte_mask, ...)，fork 1 补全
形态同口径）；fp32、无 autocast、checkpoint 只读硬冻结。

Usage:
  python tools/analysis/v3_6/measure_consumption_profile.py --device cuda
  CPU 冒烟: python tools/analysis/v3_6/measure_consumption_profile.py --device cpu --max-windows 2
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    byte_probe,
    load_model,
)

RUN = "checkpoints/v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818"
PERM_SEED = 20260819  # one fixed permutation per window, shared by all sites


# ---------------------------------------------------------------------------
# interventions
# ---------------------------------------------------------------------------


def _perturb_rows(x: torch.Tensor, perm: torch.Tensor, n_real: int, mode: str) -> torch.Tensor:
    """x (B, C, ...): break the chunk-content pairing of the first n_real rows
    (shuffle: marginals kept, pairing broken) or zero them outright."""
    out = x.clone()
    if mode == "shuffle":
        out[:, :n_real] = x[:, perm]
    elif mode == "zero":
        out[:, :n_real] = 0.0
    else:
        raise ValueError(f"unknown intervention mode {mode!r}")
    return out


def backbone_forward_mirror(bb, k_rows, v_rows, chunk_mask, pos, site=None, perm=None, n_real=0, mode="shuffle", record=None):
    """SLMBackbone.forward mirrored op-for-op (classic single-view 3-dim store
    path) with chunk-axis intervention points; site=None is bit-identical to
    bb(...) (parity pinned by tests). Sites: "k_rows"/"v_rows" (store-row
    inputs), "bb_cross1" (block-1 entry hidden), "bb_self{i}" (self-block i
    entry hidden). record, if given, collects the CONSUMED (post-perturbation)
    tensor at every intervention point."""
    if bb.k_pos_inject:
        raise ValueError("the mirror does not implement k_pos_inject (a+pos arm)")
    if k_rows.dim() != 3 or v_rows.dim() != 3:
        raise ValueError("the mirror covers the classic single-view store only (fork-2 multi-view rows are 4-dim)")
    bsz, n = chunk_mask.shape
    nh = bb.nhead
    hd = pos.size(-1) // nh
    if site == "k_rows":
        k_rows = _perturb_rows(k_rows, perm, n_real, mode)
    if record is not None:
        record["k_rows"] = k_rows
    if site == "v_rows":
        v_rows = _perturb_rows(v_rows, perm, n_real, mode)
    if record is not None:
        record["v_rows"] = v_rows
    store_v = bb.align_v(v_rows)  # (B, C, d) — shared: store V side AND seeds
    k_flat = bb.align_k(k_rows)
    seed = k_flat if bb.seed_source == "k" else store_v
    h = seed + pos.to(seed.dtype)
    if bb.k_block_eval:
        k_flat = torch.zeros_like(k_flat)
    if site == "bb_cross1":
        h = _perturb_rows(h, perm, n_real, mode)
    if record is not None:
        record["bb_cross1"] = h
    k = k_flat.view(bsz, n, nh, hd).transpose(1, 2)
    v = store_v.view(bsz, n, nh, hd).transpose(1, 2)
    # causal over the store; keep the diagonal even on padded rows (a
    # fully-masked SDPA row yields NaN, and 0*NaN poisons downstream)
    future = torch.triu(torch.ones(n, n, dtype=torch.bool, device=k_rows.device), diagonal=1)
    allowed = (~future).view(1, 1, n, n) & chunk_mask.view(bsz, 1, 1, n)
    allowed = allowed | torch.eye(n, dtype=torch.bool, device=k_rows.device).view(1, 1, n, n)
    # block 1: cross-read; Q self-produced from the hidden state
    q = bb.q_proj(h).view(bsz, n, nh, hd).transpose(1, 2)
    o = F.scaled_dot_product_attention(q, k, v, attn_mask=allowed)
    h = h + bb.o_proj(o.transpose(1, 2).reshape(bsz, n, nh * hd))
    h = h + bb.ffn1(bb.ln_ffn1(h))
    # blocks 2..L: standard causal self-attention + FFN (pre-norm)
    for i, blk in enumerate(bb.self_blocks):
        if site == f"bb_self{i}":
            h = _perturb_rows(h, perm, n_real, mode)
        if record is not None:
            record[f"bb_self{i}"] = h
        hn = blk["ln_s"](h)
        q = blk["q"](hn).view(bsz, n, nh, hd).transpose(1, 2)
        kk = blk["k"](hn).view(bsz, n, nh, hd).transpose(1, 2)
        vv = blk["v"](hn).view(bsz, n, nh, hd).transpose(1, 2)
        o = F.scaled_dot_product_attention(q, kk, vv, attn_mask=allowed)
        h = h + blk["o"](o.transpose(1, 2).reshape(bsz, n, nh * hd))
        h = h + blk["ffn"](blk["ln_f"](h))
    return bb.norm(h)


def _decoder_pre_hook(perm: torch.Tensor, n_real: int, mode: str, bsz: int, chunks: int):
    """forward_pre_hook factory for decoder.blocks[j]: the decoder folds the
    chunk axis into the batch dim ((B*C, span, d)) — unfold, perturb along the
    chunk axis, refold. valid/noise pass through untouched."""

    def hook(module, args):
        h, valid, noise = args
        hv = h.view(bsz, chunks, *h.shape[1:])
        hv = _perturb_rows(hv, perm, n_real, mode)
        return (hv.view(h.shape), valid, noise)

    return hook


# ---------------------------------------------------------------------------
# completion chain (production wiring: _slm_store_rows -> backbone -> decoder)
# ---------------------------------------------------------------------------


@torch.no_grad()
def chain_inputs(model, ns, clean: torch.Tensor, byte_mask: torch.Tensor):
    """Front end + store rows + completion target grid, computed ONCE per
    window (the per-site reruns only redo backbone+decoder)."""
    source = clean.masked_fill(byte_mask.to(clean.device), MASK_ID)
    chunks, _memory, _index = _front_end(model, source)
    k_rows, v_rows, _sn, _m, _i = model._slm_store_rows(chunks)
    n_real = int(chunks.chunk_mask[0].sum())
    pos = model.chunk_pos.weight.unsqueeze(0)[:, : k_rows.size(1)]
    targets, slot_mask, _masked, _t = s1.make_cumulative_retention_targets(
        clean, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    return chunks, k_rows, v_rows, pos, n_real, targets, slot_mask


@torch.no_grad()
def chain_logits(model, chunks, k_rows, v_rows, pos, n_real: int, site=None, perm=None, mode="shuffle", record=None):
    """cond = backbone_out + pos -> decoder, with an optional single-site
    intervention (backbone sites via the mirror; dec{j} via a pre-hook)."""
    backbone_out = backbone_forward_mirror(
        model.backbone, k_rows, v_rows, chunks.chunk_mask, pos,
        site=site, perm=perm, n_real=n_real, mode=mode, record=record,
    )
    cond = backbone_out + pos
    handles = []
    if site is not None and site.startswith("dec"):
        j = int(site[len("dec"):])
        bsz, nch = chunks.chunk_mask.shape
        handles.append(model.decoder.blocks[j].register_forward_pre_hook(_decoder_pre_hook(perm, n_real, mode, bsz, nch)))
    try:
        return model.decoder(cond, chunks.token_mask)
    finally:
        for h in handles:
            h.remove()


def kl_and_acc(base_logits, abl_logits, targets, slot_mask, n_real: int) -> tuple[float, float]:
    """Mean KL(base || ablated) over the scored slots + the ablated completion
    byte acc (clean cumulative grid, fork-1 completion 口径)."""
    sel = slot_mask[:, :n_real]
    p = F.softmax(base_logits[:, :n_real].float(), dim=-1)
    log_q = F.log_softmax(abl_logits[:, :n_real].float(), dim=-1)
    kl = F.kl_div(log_q, p, reduction="none").sum(dim=-1)  # (B, n, S), KL(base‖abl)
    kl_mean = float((kl * sel.float()).sum() / sel.float().sum().clamp(min=1.0))
    acc = float(s1._acc_tensor(abl_logits[:, :n_real].argmax(dim=-1), targets[:, :n_real], sel))
    return kl_mean, acc


# ---------------------------------------------------------------------------
# per-slot interface probe (all slots, real vs chunk-permuted garbage rows)
# ---------------------------------------------------------------------------


@torch.no_grad()
def collect_state_channel_rows(model, windows, masks, device, garbage: bool, seed: int = PERM_SEED):
    """Interface rows of the STATE-engaged store channel (k=state -> k_rows;
    v=state -> v_rows) per real chunk + per-slot clean byte targets for ALL
    slots (0..max_span-1). garbage=True: the rows are permuted along the chunk
    axis (same rows, wrong chunks — readout is per-chunk, so permuting the rows
    is exactly the interface probe's permute-states-then-read)."""
    cfg = model.config
    if getattr(cfg, "k_row_source", "") == "state":
        channel = "k"
    elif getattr(cfg, "v_row_source", "") == "state":
        channel = "v"
    else:
        raise ValueError("no state-engaged store channel (k_row_source/v_row_source both direct)")
    xs, ys, yvalid = [], [], []
    gen = torch.Generator().manual_seed(seed)
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        chunks, _memory, _index = _front_end(model, source)
        k_rows, v_rows, _sn, _m, _i = model._slm_store_rows(chunks)
        n = int(chunks.chunk_mask[0].sum())
        rows = (k_rows if channel == "k" else v_rows)[:, :n]
        if garbage:
            rows = rows[:, torch.randperm(n, generator=gen).to(device)]
        xs.append(rows[0].float().cpu())
        bt, bs, _ = s1.make_targets(
            clean.to(device), torch.zeros_like(bm).to(device),
            chunks.chunk_ids, chunks.offsets, cfg.max_chunks, cfg.max_span,
        )
        ys.append(bt[0, :n].cpu())
        yvalid.append(bs[0, :n].cpu())
    return torch.cat(xs), torch.cat(ys), torch.cat(yvalid), channel


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # GBK consoles cannot encode U+2212 (real−garbage)
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16, help="eval windows (16 = the training final-eval protocol)")
    p.add_argument("--mode", default="shuffle", choices=["shuffle", "zero"], help="intervention form")
    p.add_argument("--report-slots", type=int, default=32, help="slot curve length in the summary (json keeps all probed slots)")
    p.add_argument("--out-dir", default="outputs/consumption_profile_20260819")
    p.add_argument("--skip-layer-profile", action="store_true")
    p.add_argument("--skip-slot-profile", action="store_true")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, step = load_model(Path(args.run_dir), device)
    windows = build_eval_windows(ns, args.max_windows)
    masks = build_masks(windows, ns)
    sites = (
        ["k_rows", "v_rows", "bb_cross1"]
        + [f"bb_self{i}" for i in range(len(model.backbone.self_blocks))]
        + [f"dec{j}" for j in range(len(model.decoder.blocks))]
    )
    print(f"[prof] model={Path(args.run_dir).name} step={step} device={device.type} windows={len(windows)} "
          f"sites={sites} mode={args.mode} ({time.time() - t0:.0f}s)", flush=True)

    gen = torch.Generator().manual_seed(PERM_SEED)
    layer_rows = []
    if not args.skip_layer_profile:
        for wi, (clean, bm) in enumerate(zip(windows, masks)):
            clean_d, bm_d = clean.to(device), bm.to(device)
            chunks, k_rows, v_rows, pos, n_real, targets, slot_mask = chain_inputs(model, ns, clean_d, bm_d)
            base_logits = chain_logits(model, chunks, k_rows, v_rows, pos, n_real)
            _, base_acc = kl_and_acc(base_logits, base_logits, targets, slot_mask, n_real)
            perm = torch.randperm(n_real, generator=gen).to(device)  # one perm per window, shared by all sites
            row = {"window": wi, "n_real": n_real, "base_acc": round(base_acc, 4), "sites": {}}
            for site in sites:
                abl_logits = chain_logits(model, chunks, k_rows, v_rows, pos, n_real, site=site, perm=perm, mode=args.mode)
                kl, acc = kl_and_acc(base_logits, abl_logits, targets, slot_mask, n_real)
                row["sites"][site] = {"kl": round(kl, 4), "acc": round(acc, 4), "acc_drop": round(base_acc - acc, 4)}
            layer_rows.append(row)
            brief = " ".join(f"{s}:{row['sites'][s]['acc_drop']:+.3f}" for s in sites)
            print(f"[prof] window {wi} n_real={n_real} base_acc={base_acc:.4f} drops[{brief}] ({time.time() - t0:.0f}s)", flush=True)

    layer_agg = {}
    if layer_rows:
        base_acc_mean = sum(r["base_acc"] for r in layer_rows) / len(layer_rows)
        for site in sites:
            layer_agg[site] = {
                "kl": round(sum(r["sites"][site]["kl"] for r in layer_rows) / len(layer_rows), 4),
                "acc": round(sum(r["sites"][site]["acc"] for r in layer_rows) / len(layer_rows), 4),
                "acc_drop": round(sum(r["sites"][site]["acc_drop"] for r in layer_rows) / len(layer_rows), 4),
            }
        layer_agg["_base_acc"] = round(base_acc_mean, 4)

    slot_profile = None
    if not args.skip_slot_profile:
        xr, ys, yv, channel = collect_state_channel_rows(model, windows, masks, device, garbage=False)
        xg, _, _, _ = collect_state_channel_rows(model, windows, masks, device, garbage=True)
        probe_real = byte_probe(xr, ys, yv)
        probe_garb = byte_probe(xg, ys, yv)
        diff = {s: round(probe_real[s]["acc"] - probe_garb[s]["acc"], 4) for s in probe_real}
        slot_profile = {"channel": channel, "probe_real": probe_real, "probe_garbage": probe_garb, "real_minus_garbage": diff}
        print(f"[prof] slot probe channel={channel} slots={sorted(probe_real, key=int)} ({time.time() - t0:.0f}s)", flush=True)

    report = {
        "probe": "附录A consumption profile (fork-2 前置, 裁定6): layerwise consumption + per-slot interface information",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": Path(args.run_dir).name, "step": step},
        "params": {
            "windows": len(windows), "mode": args.mode, "perm_seed": PERM_SEED,
            "eval_mask_seed": ns.eval_mask_seed, "report_slots": args.report_slots,
        },
        "intervention": "chunk-axis permutation (shuffle: marginals kept, pairing broken) or zeroing of the layer input; "
        "one fixed permutation per window shared by all sites",
        "sites": sites,
        "layer_profile_agg": layer_agg,
        "layer_profile_per_window": layer_rows,
        "slot_profile": slot_profile,
        "protocol": "16 窗 eval seed 1042; completion acc = clean 累积保留网格 (fork-1 completion 口径); "
        "slot probe = E73-A6 2-fold ridge, all slots 0..max_span-1",
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "consumption_profile.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"CONSUMPTION PROFILE — 附录A 剖面（{Path(args.run_dir).name}, step {step}）",
        f"日期 {report['created']}  设备 {device.type}  窗口 {len(windows)}  干预 {args.mode}  口径 eval seed 1042",
        "",
    ]
    if layer_agg:
        lines += [
            f"层级消费剖面（补全链 cond=backbone_out+pos→decoder；baseline acc = {layer_agg['_base_acc']:.4f}）：",
            "  site      | acc    | Δacc    | KL(base‖干预)",
        ]
        for site in sites:
            a = layer_agg[site]
            lines.append(f"  {site:9s} | {a['acc']:.4f} | {a['acc_drop']:+.4f} | {a['kl']:.4f}")
        lines += [
            "",
            "  判读：Δacc/KL 大 = 该层输入的 chunk-内容配对是承重墙（该层真在消费读出/条件信号）；",
            "  ≈0 = 该层对配对惰（信号已被下游写回位置或从未到达）。store 两行对照回答哪条通道承重。",
        ]
    if slot_profile:
        pr, pg, df = slot_profile["probe_real"], slot_profile["probe_garbage"], slot_profile["real_minus_garbage"]
        shown = [s for s in sorted(pr, key=int) if int(s) < args.report_slots]
        lines += [
            "",
            f"逐 slot 信息剖面（接口 = {slot_profile['channel']}_rows 状态读出行，岭回归 2-fold，real−garbage；前 {args.report_slots} slot）：",
            "  slot | real   | garbage | real−garbage | n",
        ]
        for s in shown:
            lines.append(f"  {s:>4s} | {pr[s]['acc']:.4f} | {pg[s]['acc']:.4f} | {df[s]:+.4f}     | {pr[s]['n']}")
        lines += [
            "",
            "  判读：real−garbage 沿 slot 的衰减形态 = 接口单向量对段内深位的信息保持曲线（fork 2 多读出向量",
            f"  设计的输入依据）。majority 基线 slot0 = {pr[shown[0]]['majority']:.4f}。" if shown else "",
        ]
    lines.append(f"完整数据: {out_path}")
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
