"""μ 训练轨迹（复塌核查，零训练，2026-08-19；E78 后续审计 M1）。

对 to_k_center 手术格的每个里程碑 checkpoint（step_003000..018000 +
latest=20000）测 WriteHead 键的 μ：回答"去均值硬约束下，键几何是训练全程
稳定去相关，还是训着训着复塌"。两条线：
  - b 格（K 通道 write_head_k，吃 index 行）——主线格；
  - c 格（V 通道 write_head，吃 memory 行）。
每格每里程碑同时报 raw（不减中心）与 centered（暖 buffer 部署形态）——
raw 轨迹看"训练把 raw 输出推向哪里"，centered 轨迹看部署几何。

口径：所有里程碑一律冷启动（persistent=False buffer 不入档），统一暖批
N_WARM_PASSES×16 窗（与 E75 验收同协议、同窗同 mask、eval seed 1042）。

Usage:
  python tools/analysis/v3_6/measure_mu_trajectory.py --device cuda
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
from tools.analysis.v3_6.measure_key_collapse import build_eval_windows, build_masks, _front_end, load_model  # noqa: E402
from tools.analysis.v3_6.measure_tokcenter_acceptance import (  # noqa: E402
    N_WARM_PASSES,
    _key_geometry,
    _pool,
    _resolve_channel,
)

GRIDS = [
    ("b-tokcenter", "checkpoints/v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818"),
    ("c-tokcenter", "checkpoints/v37ks_c_is_v372_cloze_tokcenter_20k_ctx4096_20260818"),
]
MILESTONE_STEPS = [3000, 6000, 9000, 12000, 15000, 18000]  # + latest.pt


@torch.no_grad()
def measure_milestone(model, wh, rows_name, windows, masks, device) -> dict:
    """One milestone: encode 16 windows with THIS milestone's weights, warm the
    cold buffer (3 passes), then measure raw + centered geometry."""
    rows_per_window = []
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        _chunks, memory, index = _front_end(model, source)
        rows = (memory if rows_name == "memory" else index)[0, : int(_chunks.chunk_mask[0].sum())]
        rows_per_window.append(rows)
    wh.k_center.zero_()  # 里程碑间统计不同步：统一从零冷启动再暖批
    wh.train()
    for _ in range(N_WARM_PASSES):
        for rows in rows_per_window:
            wh(rows.unsqueeze(0))
    wh.eval()
    raw = _pool([_key_geometry(wh, r, center=False) for r in rows_per_window])
    cen = _pool([_key_geometry(wh, r, center=True) for r in rows_per_window])
    return {"raw": raw, "centered": cen, "k_center_norm": round(float(wh.k_center.norm()), 3)}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16)
    p.add_argument("--out-dir", default="outputs/key_collapse_survey_20260818")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    t0 = time.time()

    trajectories = []
    for label, run in GRIDS:
        run_dir = Path(run)
        model, ns, _step = load_model(run_dir, device)  # latest.pt just for build+windows
        channel, wh, rows_name = _resolve_channel(model)
        assert getattr(model.config, "to_k_center", False), f"{label}: expected to_k_center=True"
        windows = build_eval_windows(ns, args.max_windows)
        masks = build_masks(windows, ns)
        points = []
        files = [run_dir / f"step_{s:06d}.pt" for s in MILESTONE_STEPS] + [run_dir / "latest.pt"]
        for f in files:
            payload = torch.load(f, map_location=device, weights_only=False)
            model.load_state_dict(payload["model"], strict=True)
            step_i = int(payload.get("step", 0))
            m = measure_milestone(model, wh, rows_name, windows, masks, device)
            points.append({
                "step": step_i,
                "mu_raw": m["raw"]["mu_mean"],
                "mu_centered": m["centered"]["mu_mean"],
                "mu_centered_std": m["centered"]["mu_std"],
                "pr_frac_raw": m["raw"]["gram_pr_frac_mean"],
                "pr_frac_centered": m["centered"]["gram_pr_frac_mean"],
                "k_center_norm": m["k_center_norm"],
            })
            print(f"[mu-traj] {label} step={step_i}: raw {m['raw']['mu_mean']:.4f} -> centered {m['centered']['mu_mean']:.4f} ({time.time() - t0:.0f}s)", flush=True)
        trajectories.append({"label": label, "run": run_dir.name, "channel": channel, "input_rows": rows_name, "points": points})
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    report = {
        "probe": "mu trajectory under the to_k_center hard constraint (M1 re-collapse check)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "windows": args.max_windows,
        "warm_passes": N_WARM_PASSES,
        "trajectories": trajectories,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "mu_trajectory_tokcenter.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "",
        "=" * 78,
        "M1 μ 训练轨迹 — to_k_center 手术格复塌核查（暖 buffer 口径，16 窗，两格）",
        f"日期 {report['created']}  设备 {device.type}",
        "",
        "  step   | " + " | ".join(f"{t['label']} raw→centered" for t in trajectories),
    ]
    for i in range(len(trajectories[0]["points"])):
        cells = []
        for t in trajectories:
            pt = t["points"][i]
            cells.append(f"{pt['mu_raw']:.3f}→{pt['mu_centered']:.3f} (PR/n {pt['pr_frac_centered']:.3f})")
        lines.append(f"  {trajectories[0]['points'][i]['step']:6d} | " + " | ".join(cells))
    lines += [
        "",
        "  判读：centered μ 全程平 = 硬约束稳定；上行复塌 = 软约束化（需更硬几何）；",
        "  raw → 1.0 是设计内行为（残余即全部内容，中心被减）。",
        f"完整数据: {out_path}",
    ]
    summary_path = out_dir / "SUMMARY.txt"
    existing = summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
    marker = "M1 μ 训练轨迹"
    if marker in existing:
        existing = existing[: existing.index(marker)].rstrip("=\n ")
        summary_path.write_text(existing + "\n", encoding="utf-8")
    with summary_path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
