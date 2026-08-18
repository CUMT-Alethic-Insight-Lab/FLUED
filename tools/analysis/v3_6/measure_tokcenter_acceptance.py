"""to_k_center 手术验收测量（零训练，2026-08-18；E75 手术的验收线）。

对象由 --run-dir/--control-run-dir 参数化；测量通道按 config 自动判定：
v_row_source=state → V 通道 write_head（吃 memory 行）；k_row_source=state →
K 通道 write_head_k（吃 index 行）。首批对象：c 格
（v37ks_c_is_v372_cloze_tokcenter，V 通道）与 b 格
（v37ks_b_sm_v372_cloze_tokcenter，K 通道）。对照基线见 E74 表
（outputs/key_collapse_survey_20260818/key_collapse_survey.json）。

口径（E75 操作注记）：k_center buffer persistent=False，新进程 eval 加载时
是冷的（减零=不去均值的假几何）。本脚本先对该格的 WriteHead 做**暖批**：
wh.train() 下过 N_WARM_PASSES×16 个评估窗的输入行让 EMA 升温，再
wh.eval() 冻结测量——即"若 buffer 持久化，部署时应有的几何"。每个窗口同
时报 raw（手动 to_k(trunk) 不减中心）与 centered（冻结暖 buffer 前向）
两种 μ + Gram 有效秩，差值即手术的在线效果。同窗同口径重测未手术对照
格（--control-run-dir 非空时）。

Usage:
  python tools/analysis/v3_6/measure_tokcenter_acceptance.py --device cuda \
      --run-dir checkpoints/v37ks_c_is_v372_cloze_tokcenter_20k_ctx4096_20260818 \
      --control-run-dir checkpoints/v37ks_c_is_v372_cloze_20k_ctx4096_20260818
  # b 格（K 通道）:
  python tools/analysis/v3_6/measure_tokcenter_acceptance.py --device cuda \
      --run-dir checkpoints/v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818 \
      --control-run-dir checkpoints/v37ks_b_sm_v372_cloze_20k_ctx4096_20260818
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
from tools.analysis.v3_6.measure_key_collapse import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    load_model,
    row_geometry,
)

SURGERY_RUN = "checkpoints/v37ks_c_is_v372_cloze_tokcenter_20k_ctx4096_20260818"
CONTROL_RUN = "checkpoints/v37ks_c_is_v372_cloze_20k_ctx4096_20260818"
N_WARM_PASSES = 3  # 48 次 EMA 更新（momentum 0.99），16 窗分布平稳，足够收敛


@torch.no_grad()
def _key_geometry(wh, rows: torch.Tensor, center: bool) -> list[dict]:
    """Per-head geometry of the WriteHead keys over rows (n, d_mem).
    center=False: manual to_k(trunk) WITHOUT subtracting the buffer (raw);
    center=True: the module's forward (eval mode, frozen warm buffer)."""
    n = rows.size(0)
    if center:
        k = wh(rows.unsqueeze(0))["k"][0]
    else:
        k = F.normalize(wh.to_k(wh.trunk(rows)).view(n, wh.heads, wh.hk), dim=-1)
    return [row_geometry(k[:, h]) for h in range(wh.heads)]


def _pool(per_window: list[list[dict]]) -> dict:
    samples = [g for geoms in per_window for g in geoms]
    mus = [g["mu"] for g in samples]

    def m(key):
        return round(sum(g[key] for g in samples) / len(samples), 4)

    return {
        "mu_mean": m("mu"),
        "mu_std": round((sum((x - m("mu")) ** 2 for x in mus) / max(len(mus) - 1, 1)) ** 0.5, 4),
        "p90_mean": m("p90"),
        "gram_pr_frac_mean": m("gram_pr_frac"),
        "n_samples": len(samples),
    }


def _resolve_channel(model):
    """v=state -> V 通道 write_head(memory); k=state -> K 通道 write_head_k(index)."""
    cfg = model.config
    if getattr(cfg, "v_row_source", "") == "state":
        return "v", model.write_head, "memory"
    if getattr(cfg, "k_row_source", "") == "state":
        return "k", model.write_head_k, "index"
    raise ValueError("no state channel (a grid has no WriteHead)")


def _measure_one(run_dir: Path, warm: bool, windows, masks, device, t0) -> dict:
    """Load one checkpoint and measure its WriteHead key geometry.
    warm=True: the to_k_center warm-buffer protocol (train-mode EMA warmup,
    then frozen-eval measurement); raw (uncentered) geometry always reported."""
    model, ns, step = load_model(run_dir, device)
    channel, wh, rows_name = _resolve_channel(model)
    is_surgery = getattr(model.config, "to_k_center", False)
    rows_per_window = []
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        _chunks, memory, index = _front_end(model, source)
        rows = (memory if rows_name == "memory" else index)[0, : int(_chunks.chunk_mask[0].sum())]
        rows_per_window.append(rows)
    if warm:
        assert is_surgery, "warm protocol applies only to to_k_center checkpoints"
        wh.train()
        for _ in range(N_WARM_PASSES):
            for rows in rows_per_window:
                wh(rows.unsqueeze(0))
        wh.eval()
    raw_w = [_key_geometry(wh, rows, center=False) for rows in rows_per_window]
    out = {
        "step": step,
        "channel": channel,
        "input_rows": rows_name,
        "to_k_center": bool(is_surgery),
        "raw": _pool(raw_w),
    }
    if warm:
        cen_w = [_key_geometry(wh, rows, center=True) for rows in rows_per_window]
        out["centered_warm"] = _pool(cen_w)
        out["k_center_norm"] = round(float(wh.k_center.norm()), 4)
    print(
        f"[accept] {run_dir.name} ({channel}@{rows_name}): raw mu={out['raw']['mu_mean']:.4f}"
        + (f" -> centered mu={out['centered_warm']['mu_mean']:.4f} (PR/n {out['raw']['gram_pr_frac_mean']:.4f} -> {out['centered_warm']['gram_pr_frac_mean']:.4f})" if warm else f" PR/n={out['raw']['gram_pr_frac_mean']:.4f}")
        + f" ({time.time() - t0:.0f}s)",
        flush=True,
    )
    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16)
    p.add_argument("--run-dir", default=SURGERY_RUN, help="the surgered checkpoint (must carry to_k_center=True)")
    p.add_argument("--control-run-dir", default=CONTROL_RUN, help="un-surgered paired control; empty = skip")
    p.add_argument("--out-dir", default="outputs/key_collapse_survey_20260818")
    p.add_argument("--report-name", default="", help="JSON filename under out-dir (default tokcenter_acceptance_<run>.json)")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    t0 = time.time()

    run_dir = Path(args.run_dir)
    # windows/masks from the target run's config (16 窗, seed 1042 同口径)
    _m0, ns0, _s0 = load_model(run_dir, device)
    windows = build_eval_windows(ns0, args.max_windows)
    masks = build_masks(windows, ns0)
    del _m0
    if device.type == "cuda":
        torch.cuda.empty_cache()
    print(f"[accept] {len(windows)} windows ready ({time.time() - t0:.0f}s)", flush=True)

    surgery = _measure_one(run_dir, True, windows, masks, device, t0)
    control = None
    if args.control_run_dir:
        control = _measure_one(Path(args.control_run_dir), False, windows, masks, device, t0)

    report = {
        "probe": "to_k_center acceptance (warm-buffer protocol)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "windows": len(windows),
        "warm_passes": N_WARM_PASSES,
        "surgery_run": {"run": run_dir.name, **surgery},
        "control_run": ({"run": Path(args.control_run_dir).name, **control} if control else None),
        "e74_reference": {"v372_cloze_c_mu": 0.9568, "v371_c_mu": 0.9354, "v372_cloze_b_k_mu": 0.9037},
        "timing_sec": round(time.time() - t0, 1),
    }
    fname = args.report_name or f"tokcenter_acceptance_{run_dir.name}.json"
    out_path = out_dir / fname
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    s = surgery.get("centered_warm")
    lines = [
        "",
        "=" * 78,
        f"TO_K_CENTER 手术验收 — {run_dir.name}（{surgery['channel']}@{surgery['input_rows']}，暖 buffer 口径，16 窗同 E74）",
        f"日期 {report['created']}  设备 {device.type}",
        "",
    ]
    if control:
        lines.append(f"  未手术对照（{control['channel']} 通道）键 μ = {control['raw']['mu_mean']:.4f}±{control['raw']['mu_std']:.3f}  Gram PR/n = {control['raw']['gram_pr_frac_mean']:.4f}")
    lines.append(f"  手术格 raw（不减中心） μ = {surgery['raw']['mu_mean']:.4f}±{surgery['raw']['mu_std']:.3f}  PR/n = {surgery['raw']['gram_pr_frac_mean']:.4f}")
    if s:
        lines.append(f"  手术格 centered（暖 buffer 部署形态） μ = {s['mu_mean']:.4f}±{s['mu_std']:.3f}  PR/n = {s['gram_pr_frac_mean']:.4f}")
    lines += [
        "",
        "  判读标尺：μ≈0.93 → 塌缩（Tropp N<1.04）；μ 降到 ~0.3 档 = E75 去均值在线生效。",
        f"完整数据: {out_path}",
    ]
    summary_path = out_dir / "SUMMARY.txt"
    existing = summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
    marker = f"TO_K_CENTER 手术验收 — {run_dir.name}"
    if marker in existing:
        existing = existing[: existing.index(marker)].rstrip("=\n ")
        summary_path.write_text(existing + "\n", encoding="utf-8")
    with summary_path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
