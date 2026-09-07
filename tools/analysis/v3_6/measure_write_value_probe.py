"""M3 写值信息复测（手术误伤排除，零训练，2026-08-19；E73-A6 协议复用）。

问题：手术 b 格的档案馆探针出现 V 回读裂口（backbone 臂 0.40-0.48 vs
direct 臂 0.61-0.69；b-v371 两臂持平 0.63）。两个候选机制：
  (a) 手术牵连值向量——to_k_center 的训练动力学顺带把 WriteHead 的 v 输出
      内容打掉了（手术误伤）；
  (b) 读出统计漂移（主嫌疑）——v 内容没动，是 backbone/状态读出链的统计
      变了。
判别测量：对手术 b 格 vs 未手术 b 格（同窗同口径 16 窗，eval seed 1042）
复跑 A6 闭式字节探针——one-vs-all 岭回归从 K 通道 write_head_k 的**写值
v**（to_v(trunk(index))，与 k_center buffer 无关）线性预测该段 slot 0-3
的字节 id；输入 index 行作上限对照。v-probe 显著掉档 ⇒ (a)；不掉 ⇒ (b)。

参考口径注记：E73-A6 的 0.62/0.37/0.32/0.61 是 c 格 **V 通道**写值（不同
通道），此处是 b 格 **K 通道**写值——跨格只作档级参考，配对判决看
b 格手术 vs 未手术。

Usage:
  python tools/analysis/v3_6/measure_write_value_probe.py --device cuda
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
from tools.analysis.v3_6.probe_oracle_write_verdict import byte_probe, load_model  # noqa: E402
from tools.analysis.v3_6.measure_key_collapse import build_eval_windows, build_masks, _front_end  # noqa: E402
from tools.analysis.v3_6.measure_tokcenter_acceptance import _resolve_channel  # noqa: E402

RUNS = [
    ("b-tokcenter", "checkpoints/v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818"),
    ("b-cloze-nosurgery", "checkpoints/v37ks_b_sm_v372_cloze_20k_ctx4096_20260818"),
]
E73_A6_CGRID = {"v": {"0": 0.6185, "1": 0.3727, "2": 0.3223, "3": 0.6092},
                "m": {"0": 0.7096, "1": 0.4628, "2": 0.3809, "3": 0.6273}}


@torch.no_grad()
def collect(model, windows, masks, device):
    """Per window: K/V-channel write values + input rows + slot0-3 clean byte
    targets. The value path (to_v(trunk(...))) never touches k_center — the
    measurement is buffer-state independent by construction."""
    channel, wh, rows_name = _resolve_channel(model)
    xs_v, xs_in, ys, yvalid = [], [], [], []
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        chunks, memory, index = _front_end(model, source)
        n = int(chunks.chunk_mask[0].sum())
        rows = (index if rows_name == "index" else memory)[0, :n]
        gates = wh(rows.unsqueeze(0))
        xs_v.append(gates["v"][0, :n].float().reshape(n, -1).cpu())
        xs_in.append(rows.float().cpu())
        bt, bs, _ = s1.make_targets(
            clean.to(device), torch.zeros_like(bm).to(device),
            chunks.chunk_ids, chunks.offsets, model.config.max_chunks, model.config.max_span,
        )
        ys.append(bt[0, :n, :4].cpu())
        yvalid.append(bs[0, :n, :4].cpu())
    return channel, rows_name, torch.cat(xs_v), torch.cat(xs_in), torch.cat(ys), torch.cat(yvalid)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16)
    p.add_argument("--out-dir", default="outputs/oracle_write_verdict_20260818")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    t0 = time.time()

    results = []
    windows = masks = None
    for label, run in RUNS:
        model, ns, step = load_model(Path(run), device)
        if windows is None:
            windows = build_eval_windows(ns, args.max_windows)
            masks = build_masks(windows, ns)
            print(f"[M3] {len(windows)} windows ready ({time.time() - t0:.0f}s)", flush=True)
        channel, rows_name, xs_v, xs_in, ys, yvalid = collect(model, windows, masks, device)
        row = {
            "label": label, "run": Path(run).name, "step": step,
            "channel": channel, "input_rows": rows_name,
            "to_k_center": bool(getattr(model.config, "to_k_center", False)),
            "probe_from_write_value": byte_probe(xs_v, ys, yvalid),
            "probe_from_input_rows": byte_probe(xs_in, ys, yvalid),
        }
        results.append(row)
        v0 = row["probe_from_write_value"].get("0", {})
        i0 = row["probe_from_input_rows"].get("0", {})
        print(f"[M3] {label}: v-probe slot0 acc={v0.get('acc')} (maj {v0.get('majority')}) | input-probe slot0 {i0.get('acc')} ({time.time() - t0:.0f}s)", flush=True)
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    report = {
        "probe": "M3 write-value byte probe re-measurement (surgery collateral check)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "windows": args.max_windows,
        "note": "b-grid K-channel write values (to_v(trunk(index))); buffer-independent by construction. "
        "E73-A6 reference was the c-grid V channel — cross-cell level reference only.",
        "e73_a6_cgrid_reference": E73_A6_CGRID,
        "results": results,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "write_value_probe_bgrid.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "",
        "=" * 78,
        "M3 写值信息复测 — 手术误伤排除（b 格 K 通道写值, 16 窗, 2-fold 岭回归）",
        f"日期 {report['created']}  设备 {device.type}",
        "",
        "  slot 级 acc（写值 v 探针 vs 输入行上限对照）:",
    ]
    for r in results:
        pv, pi = r["probe_from_write_value"], r["probe_from_input_rows"]
        lines.append(
            f"  {r['label']:20s} v: "
            + "/".join(f"{pv[s]['acc']:.3f}" for s in sorted(pv))
            + "   | in: "
            + "/".join(f"{pi[s]['acc']:.3f}" for s in sorted(pi))
            + f"   (majority: {'/'.join(f'{pv[s]['majority']:.3f}' for s in sorted(pv))})"
        )
    lines += [
        f"  E73-A6 参考（c 格 V 通道, 不同通道仅档级参考）: v 0.62/0.37/0.32/0.61, m 0.71/0.46/0.38/0.63",
        "",
        "  判读：手术格 v-probe 显著低于未手术格 ⇒ 手术牵连值向量（误伤）；",
        "  持平 ⇒ V 回读裂口机制指向读出统计漂移（主嫌疑）。",
        f"完整数据: {out_path}",
    ]
    summary_path = out_dir / "SUMMARY.txt"
    existing = summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
    marker = "M3 写值信息复测"
    if marker in existing:
        existing = existing[: existing.index(marker)].rstrip("=\n ")
        summary_path.write_text(existing + "\n", encoding="utf-8")
    with summary_path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
