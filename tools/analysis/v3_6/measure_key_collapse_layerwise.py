"""WriteHead 键塌缩的逐层定位分解（零训练纯测量，2026-08-18；E74 后续）。

背景：E74 盘点（measure_key_collapse.py）测出 WriteHead 写入键 μ≈0.93
塌缩；主会话 W_to_k SVD 显示权重矩阵健康（有效秩 361-374/512、首奇异值
能量 18%）——塌缩不在权重，在激活。本脚本把 WriteHead 的前向逐层拆开，
定位 μ 从哪一层开始跳变：

  L0 输入行（memory 行 for V 通道 / index 行 for K 通道）
  L1 trunk[0] = LayerNorm(d_mem)（含仿射）
  L2 trunk[1] = Linear(d_mem → write_hidden)（pre-SiLU）
  L3 trunk[2] = SiLU（trunk 输出）
  L4 to_k(l3)（含 bias，pre-normalize，按头拆开）
  L5 L2 归一化后（= gates["k"]，与管线实际入状态的键逐元素一致）

每层报两两 |cos| 非对角统计（μ/p50/p90）；L3 加报每维方差谱（死维计数）
与 SiLU 饱和率（pre-activation < -4 的比例）；L4 加报 bias 支配度
‖b‖/median‖Wx‖（≫1 ⇒ 输出≈常数 bias 向量，μ 必然 ≈1）。

第 4 点注记（查源码确认 + 数学）：L2 归一化在 WriteHead.forward 内
（flued/v36/model.py:351，KDAStateMachine 内无归一化）；逐行归一化不改
两两余弦（cos 对每行尺度不变）——L4/L5 的 μ 恒等是恒等式，实测断言
（wiring 守卫：L5 键 == write_head(rows)["k"]）。

判读表：μ 逐层跳变点 = 塌缩起始层；bias 支配度 + 饱和率 + 死维佐证机制。

纪律：checkpoint 只读硬冻结、零训练、fp32；eval seed 1042 同口径 16 窗
（复用 measure_key_collapse 的管线）。

Usage:
  python tools/analysis/v3_6/measure_key_collapse_layerwise.py --device cuda
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
    GRIDS,
    build_eval_windows,
    build_masks,
    load_model,
    row_geometry,
    _front_end,
)

# (label, run_dir, channel) — channel: "v" = write_head(memory), "k" = write_head_k(index)
TARGETS = [
    ("c-v371", "checkpoints/v37_c_is_v371_20k_ctx4096_20260817", "v"),
    ("c-cloze", "checkpoints/v37ks_c_is_v372_cloze_20k_ctx4096_20260818", "v"),
    ("b-v371", "checkpoints/v37_b_sm_v371_20k_ctx4096_20260817", "k"),
]

SILU_SAT_THRESHOLD = -4.0  # SiLU(x) ≈ -0.018 below this: effectively dead zone


@torch.no_grad()
def layerwise_write_head(wh, rows: torch.Tensor) -> dict:
    """One window: rows (n, d_mem) -> per-layer geometry + mechanism stats.
    Uses the module's own submodules (no hooks); verified against wh.forward.
    E79 split-trunk aware: the key path reads trunk_k when split."""
    trunk = wh.trunk_k if getattr(wh, "split_trunk", False) else wh.trunk
    x0 = rows.float()
    l1 = trunk[0](x0)  # LayerNorm (affine)
    l2 = trunk[1](l1)  # Linear, pre-SiLU
    l3 = trunk[2](l2)  # SiLU = trunk output
    k_raw = wh.to_k(l3)  # (n, H*hk), bias included
    H, hk = wh.heads, wh.hk
    k_heads = k_raw.view(-1, H, hk)
    k_norm = F.normalize(k_heads, dim=-1)
    # wiring guard: L5 must equal the module's actual forward keys
    ref = wh(rows.unsqueeze(0))["k"][0]
    assert torch.allclose(k_norm, ref, atol=1e-6), "layerwise extraction != WriteHead.forward"

    n = x0.size(0)
    var = l3.var(dim=0)  # per-dim variance across chunks
    dead = int((var < 1e-8).sum())
    wx = F.linear(l3, wh.to_k.weight).view(-1, H, hk)  # no bias
    b = wh.to_k.bias.view(H, hk)
    bias_ratio = [
        float(b[h].norm() / wx[:, h].norm(dim=-1).median().clamp(min=1e-12)) for h in range(H)
    ]
    mu_k_pre = [row_geometry(k_heads[:, h])["mu"] for h in range(H)]
    mu_k_post = [row_geometry(k_norm[:, h])["mu"] for h in range(H)]
    # L2-normalization is a per-row rescale: pairwise cosines are invariant
    assert all(abs(a - b) < 1e-5 for a, b in zip(mu_k_pre, mu_k_post)), "norm changed pairwise cos?!"
    # de-meaned control: remove the shared component from Wx, then measure —
    # if μ collapses to ~healthy, the collapse is a single common direction and
    # a de-meaning hard constraint is sufficient surgery
    wx_dm = wx - wx.mean(dim=0, keepdim=True)
    mu_wx_demeaned = sum(row_geometry(wx_dm[:, h])["mu"] for h in range(H)) / H
    x0_dm = x0 - x0.mean(dim=0, keepdim=True)
    mu_L0_demeaned = row_geometry(x0_dm)["mu"]
    l3_dm = l3 - l3.mean(dim=0, keepdim=True)
    mu_L3_demeaned = row_geometry(l3_dm)["mu"]

    return {
        "n": n,
        "mu": {
            "L0_input": row_geometry(x0)["mu"],
            "L1_layernorm": row_geometry(l1)["mu"],
            "L2_linear_preact": row_geometry(l2)["mu"],
            "L3_silu_trunk_out": row_geometry(l3)["mu"],
            "L4_to_k_pre_norm": sum(mu_k_pre) / H,
            "L5_normalized": sum(mu_k_post) / H,
        },
        "p90": {
            "L0_input": row_geometry(x0)["p90"],
            "L3_silu_trunk_out": row_geometry(l3)["p90"],
            "L4_to_k_pre_norm": sum(row_geometry(k_heads[:, h])["p90"] for h in range(H)) / H,
        },
        "l3_dead_dims": dead,
        "l3_var_quantiles": [
            round(float(var.quantile(q)), 8) for q in (0.1, 0.5, 0.9)
        ],
        "silu_sat_rate": float((l2 < SILU_SAT_THRESHOLD).float().mean()),
        "bias_dominance_per_head": [round(r, 4) for r in bias_ratio],
        "bias_norm_per_head": [round(float(b[h].norm()), 4) for h in range(H)],
        "wx_norm_median_per_head": [round(float(wx[:, h].norm(dim=-1).median()), 4) for h in range(H)],
        "mu_wx_demeaned": mu_wx_demeaned,  # to_k 输出去共享分量后的 μ（硬约束手术可行性）
        "mu_L0_demeaned": mu_L0_demeaned,
        "mu_L3_demeaned": mu_L3_demeaned,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16)
    p.add_argument("--out-dir", default="outputs/key_collapse_survey_20260818")
    p.add_argument("--runs", default="",
                   help="override TARGETS: comma-separated label:run_dir:channel triples "
                   "(channel v=write_head@memory, k=write_head_k@index)")
    p.add_argument("--report-name", default="layerwise_decomposition.json",
                   help="JSON filename under out-dir (override for side runs so the main artifact is never clobbered)")
    p.add_argument("--section-tag", default="",
                   help="summary section title suffix (unique per side run; section-scoped replace)")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    targets = TARGETS
    if args.runs:
        targets = []
        for item in args.runs.split(","):
            label, run, channel = item.split(":")
            targets.append((label, run, channel))

    windows = masks = None
    results = []
    for label, run, channel in targets:
        model, ns, step = load_model(Path(run), device)
        if windows is None:
            windows = build_eval_windows(ns, args.max_windows)
            masks = build_masks(windows, ns)
            print(f"[layerwise] {len(windows)} eval windows + masks ready ({time.time() - t0:.0f}s)", flush=True)
        wh = model.write_head if channel == "v" else model.write_head_k
        rows_name = "memory" if channel == "v" else "index"
        per_window = []
        for clean, byte_mask in zip(windows, masks):
            source = clean.masked_fill(byte_mask.to(clean.device), MASK_ID).to(device)
            chunks, memory, index = _front_end(model, source)
            n_real = int(chunks.chunk_mask[0].sum())
            rows = (memory if channel == "v" else index)[0, :n_real]
            per_window.append(layerwise_write_head(wh, rows))
        # aggregate over windows
        mu_agg = {k: round(sum(w["mu"][k] for w in per_window) / len(per_window), 4) for k in per_window[0]["mu"]}
        p90_agg = {k: round(sum(w["p90"][k] for w in per_window) / len(per_window), 4) for k in per_window[0]["p90"]}
        row = {
            "label": label,
            "run": Path(run).name,
            "channel": channel,
            "input_rows": rows_name,
            "step": step,
            "mu_per_layer": mu_agg,
            "p90_per_layer": p90_agg,
            "mu_std_L4": round(
                (sum((w["mu"]["L4_to_k_pre_norm"] - mu_agg["L4_to_k_pre_norm"]) ** 2 for w in per_window) / max(len(per_window) - 1, 1)) ** 0.5, 4
            ),
            "l3_dead_dims_mean": round(sum(w["l3_dead_dims"] for w in per_window) / len(per_window), 1),
            "l3_width": int(wh.to_k.in_features),
            "l3_var_quantiles_mean": [
                round(sum(w["l3_var_quantiles"][i] for w in per_window) / len(per_window), 8) for i in range(3)
            ],
            "silu_sat_rate_mean": round(sum(w["silu_sat_rate"] for w in per_window) / len(per_window), 4),
            "bias_dominance_per_head": [
                round(sum(w["bias_dominance_per_head"][h] for w in per_window) / len(per_window), 4)
                for h in range(len(per_window[0]["bias_dominance_per_head"]))
            ],
            "bias_norm_per_head": [
                round(sum(w["bias_norm_per_head"][h] for w in per_window) / len(per_window), 4)
                for h in range(len(per_window[0]["bias_norm_per_head"]))
            ],
            "wx_norm_median_per_head": [
                round(sum(w["wx_norm_median_per_head"][h] for w in per_window) / len(per_window), 4)
                for h in range(len(per_window[0]["wx_norm_median_per_head"]))
            ],
            "n_real_mean": round(sum(w["n"] for w in per_window) / len(per_window), 1),
            "mu_wx_demeaned_mean": round(sum(w["mu_wx_demeaned"] for w in per_window) / len(per_window), 4),
            "mu_L0_demeaned_mean": round(sum(w["mu_L0_demeaned"] for w in per_window) / len(per_window), 4),
            "mu_L3_demeaned_mean": round(sum(w["mu_L3_demeaned"] for w in per_window) / len(per_window), 4),
        }
        results.append(row)
        print(
            f"[layerwise] {label} ({channel}@{rows_name}): "
            + " ".join(f"{k.split('_')[0]}={v:.3f}" for k, v in mu_agg.items())
            + f" | dead={row['l3_dead_dims_mean']} sat={row['silu_sat_rate_mean']:.3f} bias_ratio={row['bias_dominance_per_head']}"
            f" ({time.time() - t0:.0f}s)",
            flush=True,
        )
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    report = {
        "probe": "WriteHead key-collapse layerwise decomposition (E74 follow-up)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "windows": len(windows),
        "layers": ["L0 input rows", "L1 LayerNorm", "L2 Linear(pre-SiLU)", "L3 SiLU(trunk out)", "L4 to_k(pre-norm)", "L5 L2-normalized"],
        "note_norm": "L2 normalization is a per-row rescale: pairwise cosines are invariant (L4==L5 by construction, asserted per window)",
        "results": results,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / args.report_name
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # append the one-page section to the survey SUMMARY.txt
    lines = [
        "",
        "=" * 78,
        f"LAYERWISE DECOMPOSITION{(' — ' + args.section_tag) if args.section_tag else ''} — WriteHead 键塌缩逐层定位（16 窗同口径）",
        f"日期 {report['created']}  设备 {device.type}",
        "",
        "逐层 μ（L0 输入行 → L1 LayerNorm → L2 Linear(pre-SiLU) → L3 SiLU → L4 to_k → L5 归一化）:",
    ]
    for r in results:
        mu = r["mu_per_layer"]
        lines.append(
            f"  {r['label']:8s} {r['channel']}@{r['input_rows']:6s}: "
            f"{mu['L0_input']:.3f} → {mu['L1_layernorm']:.3f} → {mu['L2_linear_preact']:.3f} → {mu['L3_silu_trunk_out']:.3f} → {mu['L4_to_k_pre_norm']:.3f} → {mu['L5_normalized']:.3f}"
        )
    lines.append("")
    lines.append("机制证据（均值 over 16 窗）:")
    for r in results:
        lines.append(
            f"  {r['label']:8s}: L3 死维 {r['l3_dead_dims_mean']}/{r['l3_width']}  SiLU 饱和率 {r['silu_sat_rate_mean']:.3f}  "
            f"bias 支配度/头 {r['bias_dominance_per_head']}  (‖b‖ {r['bias_norm_per_head']} vs median‖Wx‖ {r['wx_norm_median_per_head']})"
        )
    lines += [
        "",
        "去均值对照（去掉共享分量后的 μ——硬约束手术可行性）:",
    ]
    for r in results:
        lines.append(
            f"  {r['label']:8s}: L0 去均值 {r['mu_L0_demeaned_mean']:.3f}  L3 去均值 {r['mu_L3_demeaned_mean']:.3f}  to_k 输出去均值 {r['mu_wx_demeaned_mean']:.3f}"
        )
    lines += [
        "",
        "判读: μ 跳变点 = 塌缩起始层；L4==L5 恒等（逐行归一化不改余弦，逐窗断言）；",
        "bias 支配度 ≫1 ⇒ to_k 输出≈常数向量 ⇒ 键必塌（bias collapse）；",
        "SiLU 饱和率高/死维多 ⇒ trunk 表示贫乏（表示塌缩）；",
        "to_k 去均值 μ ≪ 原 μ ⇒ 塌缩主体是单一共享方向（去均值/白化硬约束候选）；",
        "去均值后仍高 ⇒ 多方向相干，去均值不够，需更强几何约束（K 通道输入行即为此形态）。",
        f"完整数据: {out_path}",
    ]
    summary_path = out_dir / "SUMMARY.txt"
    existing = summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
    marker = f"LAYERWISE DECOMPOSITION{(' — ' + args.section_tag) if args.section_tag else ''}"
    if marker in existing:
        # section-scoped replace: cut ONLY this section (to the next section
        # separator or EOF) — never truncate later sections (2026-08-19 lesson:
        # the previous marker-to-EOF truncation ate four later sections)
        start = existing.index(marker)
        head = existing[:start].rstrip("=\n ")
        rest = existing[start:]
        next_sep = rest.find("\n" + "=" * 21)  # next section's separator line
        tail = rest[next_sep:] if next_sep != -1 else ""
        summary_path.write_text(head + "\n" + tail.lstrip("\n"), encoding="utf-8")
        existing = summary_path.read_text(encoding="utf-8")
    with summary_path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
