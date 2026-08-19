"""护栏二探针：读出链接口向量的信息含量（零训练纯测量，2026-08-19）。

对象：冻结 c 格 checkpoints/v37_c_is_v371_20k_ctx4096_20260817（v=state，
读出链锁死格）。接口向量 = realign(q·S) 的状态读出行（realign 之后、
decoder_in 之前，d_pack 宽）。问题：这条链的接口上到底还剩多少字节内容？
——E73 已知链的下游解码只出 10% 档、写值线性探针 0.62 档，但"接口向量
本身线性含多少"没量过。

协议（E73-A6 同口径，16 窗 eval seed 1042，2-fold 岭回归，slot0-3）：
  - 真实态：S = 训练递推的自然态 → v_rows → 探针 acc_real；
  - 垃圾态基线：同一批状态**沿 chunk 轴打乱**（边际分布不变、chunk-内容
    配对被打碎）→ 同一 realign → 探针 acc_garbage；
  - 接口真实信息含量 = acc_real − acc_garbage（逐 slot）。
对照档：写值 v 探针 0.62（E73-A6 slot0）、memory 行 0.71。

判读标尺（用户裁定）：真实−垃圾差 >0.4 → fork 2（读出链结构性重做）暂缓；
≈0.2 → fork 2 设计文档立即开工。

Usage:
  python tools/analysis/v3_6/measure_interface_probe.py --device cuda
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

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
    read_trained,
    trained_states,
)

RUN = "checkpoints/v37_c_is_v371_20k_ctx4096_20260817"


@torch.no_grad()
def collect_interface_rows(model, windows, masks, device, garbage: bool, seed: int = 20260819):
    """Interface rows (post-realign v_rows) per real chunk + slot0-3 clean byte
    targets. garbage=True: the per-chunk states are permuted along the chunk
    axis before the readout (marginals kept, chunk-content pairing broken)."""
    xs, ys, yvalid = [], [], []
    gen = torch.Generator().manual_seed(seed)
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        chunks, memory, _index = _front_end(model, source)
        n = int(chunks.chunk_mask[0].sum())
        gates = model.write_head(memory)
        S = trained_states(model.state_machine, gates, n)
        if garbage:
            perm = torch.randperm(n, generator=gen).to(device)
            S = S[:, perm]  # same states, wrong chunks
        v_rows = read_trained(model.state_machine, S)  # (1, n, d_pack) post-realign
        xs.append(v_rows[0].float().cpu())
        bt, bs, _ = s1.make_targets(
            clean.to(device), torch.zeros_like(bm).to(device),
            chunks.chunk_ids, chunks.offsets, model.config.max_chunks, model.config.max_span,
        )
        ys.append(bt[0, :n, :4].cpu())
        yvalid.append(bs[0, :n, :4].cpu())
    return torch.cat(xs), torch.cat(ys), torch.cat(yvalid)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16)
    p.add_argument("--out-dir", default="outputs/interface_probe_20260818")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, step = load_model(Path(args.run_dir), device)
    windows = build_eval_windows(ns, args.max_windows)
    masks = build_masks(windows, ns)
    print(f"[iface] model={Path(args.run_dir).name} step={step} windows={len(windows)} ({time.time() - t0:.0f}s)", flush=True)

    xr, ys, yv = collect_interface_rows(model, windows, masks, device, garbage=False)
    xg, _, _ = collect_interface_rows(model, windows, masks, device, garbage=True)
    probe_real = byte_probe(xr, ys, yv)
    probe_garb = byte_probe(xg, ys, yv)
    diff = {s: round(probe_real[s]["acc"] - probe_garb[s]["acc"], 4) for s in probe_real}
    print(f"[iface] real   : {json.dumps(probe_real)}", flush=True)
    print(f"[iface] garbage: {json.dumps(probe_garb)}", flush=True)
    print(f"[iface] real - garbage = {json.dumps(diff)}", flush=True)

    report = {
        "probe": "readout-interface information content (real vs garbage states)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": Path(args.run_dir).name, "step": step},
        "windows": len(windows),
        "interface": "v_rows = realign(q·S_natural) — post-realign, pre-decoder_in",
        "garbage_form": "per-window chunk-axis permutation of the state sequence (marginals kept, pairing broken)",
        "protocol": "E73-A6: 2-fold one-vs-all ridge, slots 0-3, clean byte ids",
        "probe_real": probe_real,
        "probe_garbage": probe_garb,
        "real_minus_garbage": diff,
        "reference_floors": {"write_value_linear_probe_slot0": 0.6185, "memory_row_slot0": 0.7096},
        "verdict_ruler": "diff>0.4 -> fork 2 deferred; ~0.2 -> fork 2 design doc starts",
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "interface_probe.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "INTERFACE PROBE — 读出链接口信息含量（c 格 v37_c_is，16 窗，岭回归 slot0-3）",
        f"日期 {report['created']}  设备 {device.type}",
        "",
        "  slot | real | garbage | real−garbage",
    ]
    for s in sorted(probe_real, key=int):
        lines.append(f"  {s:>4s} | {probe_real[s]['acc']:.4f} | {probe_garb[s]['acc']:.4f} | {diff[s]:+.4f}")
    lines += [
        "",
        f"  对照：写值线性探针 slot0 = 0.6185（E73-A6）；majority 基线 = {probe_real['0']['majority']:.4f}（slot0）",
        "  判读标尺：real−garbage >0.4 → fork 2 暂缓；≈0.2 → fork 2 设计文档开工。",
        f"完整数据: {out_path}",
    ]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
