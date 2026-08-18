"""to_k_center 手术验收测量（零训练，2026-08-18；E75 手术的验收线）。

对象：checkpoints/v37ks_c_is_v372_cloze_tokcenter_20k_ctx4096_20260818
（v37.2 + cloze + --to-k-center，20K 训完）。对照：
outputs/key_collapse_survey_20260818/ 里 E74 的未手术 cloze c 格 μ=0.9568
与 v371 c 格 μ=0.9354。

口径（E75 操作注记）：k_center buffer persistent=False，新进程 eval 加载时
是冷的（减零=不去均值的假几何）。本脚本先对该格的 WriteHead 做**暖批**：
wh.train() 下过 N_WARM_PASSES×16 个评估窗的 memory 行让 EMA 升温，再
wh.eval() 冻结测量——即"若 buffer 持久化，部署时应有的几何"。每个窗口同
时报 raw（手动 to_k(trunk) 不减中心）与 centered（冻结暖 buffer 前向）
两种 μ + Gram 有效秩，差值即手术的在线效果。同窗同口径重测未手术
cloze c 格作配对对照。

Usage:
  python tools/analysis/v3_6/measure_tokcenter_acceptance.py --device cuda
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


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16)
    p.add_argument("--out-dir", default="outputs/key_collapse_survey_20260818")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    t0 = time.time()

    model, ns, step = load_model(Path(SURGERY_RUN), device)
    assert getattr(model.config, "to_k_center", False), "surgery checkpoint must carry to_k_center=True"
    windows = build_eval_windows(ns, args.max_windows)
    masks = build_masks(windows, ns)
    print(f"[accept] {len(windows)} windows ready ({time.time() - t0:.0f}s)", flush=True)

    rows_per_window = []
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        _chunks, memory, _index = _front_end(model, source)
        rows_per_window.append(memory[0, : int(_chunks.chunk_mask[0].sum())])

    # warm the non-persistent EMA buffer (deployment-equivalent geometry)
    wh = model.write_head
    wh.train()
    for _ in range(N_WARM_PASSES):
        for rows in rows_per_window:
            wh(rows.unsqueeze(0))
    wh.eval()
    warm_norm = float(wh.k_center.norm())
    print(f"[accept] buffer warm |k_center|={warm_norm:.3f} ({time.time() - t0:.0f}s)", flush=True)

    raw_w, cen_w = [], []
    for rows in rows_per_window:
        raw_w.append(_key_geometry(wh, rows, center=False))
        cen_w.append(_key_geometry(wh, rows, center=True))
    surgery = {"raw": _pool(raw_w), "centered_warm": _pool(cen_w), "k_center_norm": round(warm_norm, 4)}
    print(
        f"[accept] surgery ckpt: raw mu={surgery['raw']['mu_mean']:.4f} -> centered mu={surgery['centered_warm']['mu_mean']:.4f} "
        f"(PR/n {surgery['raw']['gram_pr_frac_mean']:.4f} -> {surgery['centered_warm']['gram_pr_frac_mean']:.4f})",
        flush=True,
    )
    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()

    # paired control: un-surgered cloze c grid, same windows, same protocol
    ctrl, cns, cstep = load_model(Path(CONTROL_RUN), device)
    assert not getattr(ctrl.config, "to_k_center", False)
    ctrl_w = []
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        _chunks, memory, _index = _front_end(ctrl, source)
        rows = memory[0, : int(_chunks.chunk_mask[0].sum())]
        ctrl_w.append(_key_geometry(ctrl.write_head, rows, center=False))
    control = {"raw": _pool(ctrl_w)}
    print(f"[accept] control (cloze c, 未手术): mu={control['raw']['mu_mean']:.4f} PR/n={control['raw']['gram_pr_frac_mean']:.4f}", flush=True)

    report = {
        "probe": "to_k_center acceptance (warm-buffer protocol)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "windows": len(windows),
        "warm_passes": N_WARM_PASSES,
        "surgery_run": {"run": Path(SURGERY_RUN).name, "step": step, **surgery},
        "control_run": {"run": Path(CONTROL_RUN).name, "step": cstep, **control},
        "e74_reference": {"v372_cloze_c_mu": 0.9568, "v371_c_mu": 0.9354},
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "tokcenter_acceptance.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    s, c = surgery["centered_warm"], control["raw"]
    lines = [
        "",
        "=" * 78,
        "TO_K_CENTER 手术验收 — c 格 cloze 世代（暖 buffer 口径，16 窗同 E74）",
        f"日期 {report['created']}  设备 {device.type}",
        "",
        f"  未手术 cloze c 格键 μ = {c['mu_mean']:.4f}±{c['mu_std']:.3f}  Gram PR/n = {c['gram_pr_frac_mean']:.4f}",
        f"  手术格 raw（不减中心） μ = {surgery['raw']['mu_mean']:.4f}±{surgery['raw']['mu_std']:.3f}  PR/n = {surgery['raw']['gram_pr_frac_mean']:.4f}",
        f"  手术格 centered（暖 buffer 部署形态） μ = {s['mu_mean']:.4f}±{s['mu_std']:.3f}  PR/n = {s['gram_pr_frac_mean']:.4f}",
        "",
        "  判读标尺：μ≈0.93 → 塌缩（Tropp N<1.04）；μ 降到 ~0.3 档 = E75 去均值在线生效。",
        f"完整数据: {out_path}",
    ]
    summary_path = out_dir / "SUMMARY.txt"
    existing = summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
    marker = "TO_K_CENTER 手术验收"
    if marker in existing:
        existing = existing[: existing.index(marker)].rstrip("=\n ")
        summary_path.write_text(existing + "\n", encoding="utf-8")
    with summary_path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
