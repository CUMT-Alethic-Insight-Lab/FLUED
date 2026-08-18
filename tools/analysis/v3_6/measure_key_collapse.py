"""键几何塌缩盘点（零训练纯测量，2026-08-18；oracle 判决实验的后续）：
μ = 写入键（或 index/memory 行）两两 |cos| 的非对角均值，在全部现存
v37 checkpoint 上盘点，回答"cloze 检索压力有没有动键几何"。

背景：oracle 写入判决（probe_oracle_write_verdict.py，同目录）在 c 格
V 通道 WriteHead 测出 μ=0.9354 的键塌缩；本脚本把同一测量推广到
b/c/d 三格的 K/V 双通道（分开报）、a 格的 index 行（a 格无状态机，
K 通道就是 summarizer 直产 index 行本身），以及 v37.2 cloze 世代的
同形格对照。

方法（与训练终评同口径）：冻结 checkpoint、eval 模式、fp32；
StreamingReconstructionDataset（seed=args.seed+9999）前 16 窗；
_MASK_GENERATOR 重播种 eval_mask_seed=1042 顺序抽签得 mask；逐窗编码
（前端→segmentor→summarizer 双头），取每个 engaged 状态通道的
WriteHead k_i（K 通道 eat index 行，V 通道 eat memory 行），real chunk
内、去对角线算 |cos| 统计（μ/p50/p90/max）与 Gram（K Kᵀ，带符号）
特征值有效秩（participation ratio）。继承对照：K 通道的输入 index 行、
V 通道的输入 memory 行同测——塌缩是 WriteHead 造的还是从输入继承的。

判读标尺（用户给定，写进摘要）：
- μ≈0.93 → 塌缩（Tropp 阈值 N<1.04，从 N=2 起可寻址性不存在）；
- cloze 格 vs 无 cloze 同形格的 μ 差：降了 → 压力能动几何（纯训练臂
  有戏）；没动 → 塌缩是损失面结构性最优，需几何硬约束（这条 fork 是
  全队列的下一个分叉点）。

Usage:
  python tools/analysis/v3_6/measure_key_collapse.py --device cuda
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
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    load_model,
)

# (label, run_dir, 备注) — 测量通道由 checkpoint config 自动决定
# 因子设计：seed(v371) → K-seed(ks-v371) → K-seed+cloze(ks-v372-cloze)，
# 三个台阶分离 seed_source 与 cloze 两个混杂（cloze 格全是 K-seed，
# 没有 ks-v371 对照就分不清是检索压力还是种子形态动的几何）。
GRIDS = [
    ("c-v371", "checkpoints/v37_c_is_v371_20k_ctx4096_20260817", "c 格 V-seed 基线（oracle 已测 μ=0.9354）"),
    ("d-v371", "checkpoints/v37_d_ss_v371_20k_ctx4096_20260817", "d 格 V-seed（K/V 双通道分开报）"),
    ("b-v371", "checkpoints/v37_b_sm_v371_20k_ctx4096_20260817", "b 格 V-seed（K 通道）"),
    ("a-v371", "checkpoints/v37_a_im_v371_20k_ctx4096_20260817", "a 格 V-seed：index 行互相干"),
    ("aks-v371", "checkpoints/v37ks_a_im_v371_20k_ctx4096_20260817", "a 格 K-seed 无 cloze（seed 对照）"),
    ("bks-v371", "checkpoints/v37ks_b_sm_v371_20k_ctx4096_20260817", "b 格 K-seed 无 cloze"),
    ("cks-v371", "checkpoints/v37ks_c_is_v371_20k_ctx4096_20260817", "c 格 K-seed 无 cloze"),
    ("dks-v371", "checkpoints/v37ks_d_ss_v371_20k_ctx4096_20260817", "d 格 K-seed 无 cloze"),
    ("a-cloze", "checkpoints/v37ks_a_im_v372_cloze_20k_ctx4096_20260817", "cloze a 格：index 行互相干"),
    ("b-cloze", "checkpoints/v37ks_b_sm_v372_cloze_20k_ctx4096_20260818", "cloze b 格"),
    ("c-cloze", "checkpoints/v37ks_c_is_v372_cloze_20k_ctx4096_20260818", "cloze c 格（K-seed+cloze）"),
    ("d-cloze", "checkpoints/v37ks_d_ss_v372_cloze_20k_ctx4096_20260818", "cloze d 格"),
]


# ---------------------------------------------------------------------------
# geometry of a row set
# ---------------------------------------------------------------------------


@torch.no_grad()
def row_geometry(X: torch.Tensor) -> dict:
    """X: (n, d) rows. μ = mean off-diagonal |cos|; Gram = X Xᵀ (signed cos)
    eigenvalue participation ratio. Rows are L2-normalized here (WriteHead
    keys already are; index/memory rows are not)."""
    X = F.normalize(X.float(), dim=-1)
    n = X.size(0)
    if n < 2:
        return {"mu": float("nan"), "p50": float("nan"), "p90": float("nan"), "max": float("nan"),
                "gram_pr": float("nan"), "gram_pr_frac": float("nan"), "n": n}
    G = X @ X.T
    off = G.abs()[~torch.eye(n, dtype=torch.bool, device=X.device)]
    eig = torch.linalg.eigvalsh(G).clamp(min=0.0)
    pr = float(eig.sum() ** 2 / eig.square().sum().clamp(min=1e-12))
    return {
        "mu": float(off.mean()),
        "p50": float(off.quantile(0.5)),
        "p90": float(off.quantile(0.9)),
        "max": float(off.max()),
        "gram_pr": pr,
        "gram_pr_frac": pr / n,
        "n": n,
    }


@torch.no_grad()
def key_geometry_per_head(k: torch.Tensor) -> list[dict]:
    """WriteHead keys (1, C, H, hk) -> one geometry dict per head."""
    return [row_geometry(k[0, :, h]) for h in range(k.size(2))]


def _agg(samples: list[dict]) -> dict:
    """Pool per-(window, head) geometry dicts: mu mean±std, means of the rest."""

    def m(key):
        vals = [s[key] for s in samples if s[key] == s[key]]  # nan-safe
        return round(sum(vals) / max(len(vals), 1), 4)

    mus = [s["mu"] for s in samples if s["mu"] == s["mu"]]
    var = sum((x - sum(mus) / len(mus)) ** 2 for x in mus) / max(len(mus) - 1, 1) if mus else 0.0
    return {
        "mu_mean": m("mu"),
        "mu_std": round(var ** 0.5, 4),
        "p50_mean": m("p50"),
        "p90_mean": m("p90"),
        "max_mean": m("max"),
        "gram_pr_mean": m("gram_pr"),
        "gram_pr_frac_mean": m("gram_pr_frac"),
        "n_rows_mean": m("n"),
        "n_samples": len(samples),
    }


# ---------------------------------------------------------------------------
# per-window measurement
# ---------------------------------------------------------------------------


@torch.no_grad()
def measure_window(model, source: torch.Tensor) -> dict:
    """One window -> per-channel geometry samples. Channels auto-detected from
    the config: K 通道 (write_head_k over index rows) / V 通道 (write_head over
    memory rows), each with its input-row inheritance control; index/memory
    rows themselves are always measured."""
    chunks, memory, index = _front_end(model, source)
    n_real = int(chunks.chunk_mask[0].sum())
    cfg = model.config
    out = {"n_real": n_real, "index_rows": [row_geometry(index[0, :n_real])], "memory_rows": [row_geometry(memory[0, :n_real])]}
    if cfg.k_row_source == "state":
        gates_k = model.write_head_k(index)
        out["k_keys"] = key_geometry_per_head(gates_k["k"][:, :n_real])
        out["k_input_rows"] = out["index_rows"]  # K 通道吃 index 行
    if cfg.v_row_source == "state":
        gates_v = model.write_head(memory)
        out["v_keys"] = key_geometry_per_head(gates_v["k"][:, :n_real])
        out["v_input_rows"] = out["memory_rows"]  # V 通道吃 memory 行
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16)
    p.add_argument("--out-dir", default="outputs/key_collapse_survey_20260818")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    # windows/masks built once from the first grid's config (all grids share
    # data_path/seq_len/seed/eval_mask_seed by construction)
    first_ns = None
    windows = masks = None

    results = []
    for label, run, note in GRIDS:
        model, ns, step = load_model(Path(run), device)
        if first_ns is None:
            first_ns = ns
            windows = build_eval_windows(ns, args.max_windows)
            masks = build_masks(windows, ns)
            print(f"[keys] {len(windows)} eval windows + masks ready ({time.time() - t0:.0f}s)", flush=True)
        grid = f"k={ns.k_row_source},v={ns.v_row_source},seed={getattr(ns, 'seed_source', 'v')}"
        samples: dict[str, list] = {}
        for clean, byte_mask in zip(windows, masks):
            source = clean.masked_fill(byte_mask.to(clean.device), MASK_ID).to(device)
            meas = measure_window(model, source)
            for channel, geoms in meas.items():
                if channel == "n_real":
                    continue
                samples.setdefault(channel, []).extend(geoms)
        row = {
            "label": label,
            "run": Path(run).name,
            "grid": grid,
            "step": step,
            "note": note,
            "channels": {channel: _agg(geoms) for channel, geoms in samples.items()},
        }
        results.append(row)
        brief = "  ".join(
            f"{ch}: μ={g['mu_mean']:.4f}±{g['mu_std']:.3f} PR/n={g['gram_pr_frac_mean']:.3f}"
            for ch, g in sorted(row["channels"].items()) if ch.endswith("keys") or ch == "index_rows"
        )
        print(f"[keys] {label:8s} ({grid}) {brief} ({time.time() - t0:.0f}s)", flush=True)
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    report = {
        "probe": "key-collapse survey (μ = mean off-diagonal |cos| of write keys / store rows)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "windows": len(windows),
        "protocol": "16 eval windows, eval_mask_seed 1042, fp32, frozen checkpoints, cloze off at eval",
        "results": results,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "key_collapse_survey.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # one-page summary: factorial table (seed x cloze) + 判读标尺
    by_label = {r["label"]: r for r in results}

    def cell(label, ch):
        g = by_label.get(label, {}).get("channels", {}).get(ch)
        return f"{g['mu_mean']:.4f}±{g['mu_std']:.3f}" if g else "—"

    def delta(base_label, arm_label, ch):
        b = by_label.get(base_label, {}).get("channels", {}).get(ch)
        a = by_label.get(arm_label, {}).get("channels", {}).get(ch)
        return f"{a['mu_mean'] - b['mu_mean']:+.4f}" if a and b else "—"

    def fac_row(name, ch, l_base, l_ks, l_cloze):
        return (
            f"  {name:16s} | {cell(l_base, ch):24s} | {cell(l_ks, ch):24s} | {cell(l_cloze, ch):24s}"
            f" | seedΔ {delta(l_base, l_ks, ch):>7s} | clozeΔ {delta(l_ks, l_cloze, ch):>7s}"
        )

    lines = [
        "KEY-COLLAPSE SURVEY — 键几何 μ 全盘点（零训练，16 窗，seed 1042 同口径）",
        f"日期 {report['created']}  设备 {device.type}",
        "",
        "因子表（写入键 μ = mean off-diag |cos|; seedΔ = K-seed 效应; clozeΔ = cloze 压力效应）:",
        "  通道             | V-seed 无 cloze          | K-seed 无 cloze          | K-seed + cloze           | 分解",
        fac_row("b 格 K 键", "k_keys", "b-v371", "bks-v371", "b-cloze"),
        fac_row("c 格 V 键", "v_keys", "c-v371", "cks-v371", "c-cloze"),
        fac_row("d 格 K 键", "k_keys", "d-v371", "dks-v371", "d-cloze"),
        fac_row("d 格 V 键", "v_keys", "d-v371", "dks-v371", "d-cloze"),
        fac_row("a 格 index 行", "index_rows", "a-v371", "aks-v371", "a-cloze"),
        "",
        "继承对照（输入行 μ：K 通道吃 index 行 / V 通道吃 memory 行——塌缩是 WriteHead 造的还是继承的）:",
        fac_row("b 格 index 行", "index_rows", "b-v371", "bks-v371", "b-cloze"),
        fac_row("c 格 memory 行", "memory_rows", "c-v371", "cks-v371", "c-cloze"),
        fac_row("d 格 index 行", "index_rows", "d-v371", "dks-v371", "d-cloze"),
        fac_row("d 格 memory 行", "memory_rows", "d-v371", "dks-v371", "d-cloze"),
        "",
        "判读标尺（用户给定）:",
        "  - μ≈0.93 → 塌缩（Tropp 阈值 N<1.04，从 N=2 起可寻址性不存在）；",
        "  - cloze 格 vs 无 cloze 同形格的 μ 差：降了 → 压力能动几何（纯训练臂有戏）；",
        "    没动 → 塌缩是损失面结构性最优，需几何硬约束（全队列下一个分叉点）。",
        "  - 分解注记：cloze 格全系 K-seed，单比 v371↔cloze 会被 seed_source 混杂；",
        "    本表以 seedΔ（v371→ks-v371）与 clozeΔ（ks-v371→cloze）拆开归因。",
        "",
        f"完整数据（含 p50/p90/max 与 Gram 有效秩）: {out_path}",
    ]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
