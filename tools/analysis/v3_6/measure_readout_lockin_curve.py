"""读出链锁死形态定量图（零训练测量，2026-08-18；E73 oracle 判决的后续，
论文图素材）。

对象：c 格 checkpoints/v37_c_is_v371_20k_ctx4096_20260817（v=state，读出链
锁死格）。病灶链 = 状态读出（固定 query）→ realign → decoder_in → decoder。

测 **μ 响应曲线**：写值 v_j 保持真实（WriteHead 产出，E73-A6 实测线性可
读字节 0.62 档），只把键的相干性从自然塌缩（μ≈0.94）连续扫到近正交
（μ≈0.1）——k(λ) = normalize(√(1-λ²)·k_real + λ·z)，z 为每窗每头固定的
随机方向（同一 z 贯穿 λ 网格，路径单调）。状态用 oracle 累计形式
S_i = Σ_{j≤i} k_j(λ) v_jᵀ（无侵蚀、无递推），逐档喂进 trained 读出链测
direct 解码字节 acc（累积 as-encoded 网格，与 E73 臂口径一致）。两条线：
  - trained-q：模型自己的固定 query 读出（链原样）；
  - ridge-read：岭回归解混（λ_ridge=0.01）后过 realign——读出接口天花板
    对照线。
参考行：A1 自然态（真实递推 + trained-q，E73 复现 0.2965）与 λ=0 档
（= E73 A2 的 oracle-塌缩键形态，0.0482）。

判读：acc 随 μ 下降而上升 ⇒ 锁在键几何（手术路线有戏）；任何 μ 档都不动
（尤其 ridge 线贴着低位）⇒ 锁在 realign/decoder 接口形态本身 ⇒ 只有
读出链复训（retrain_readout_chain.py）能拆。

Usage:
  python tools/analysis/v3_6/measure_readout_lockin_curve.py --device cuda
"""

from __future__ import annotations

import argparse
import json
import math
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
    _arm_metrics,
    _front_end,
    build_eval_windows,
    build_masks,
    decode_direct,
    load_model,
    oracle_states,
    read_trained,
    read_via_realign,
    ridge_unmix,
    trained_states,
)
from tools.analysis.v3_6.measure_key_collapse import row_geometry  # noqa: E402

C_RUN = "checkpoints/v37_c_is_v371_20k_ctx4096_20260817"
LAMBDAS = [0.0, 0.2, 0.35, 0.5, 0.65, 0.75, 0.85, 0.93, 1.0]  # 混合向随机键的比例
RIDGE_LAM = 0.01


def mix_keys(k_real: torch.Tensor, z: torch.Tensor, lam: float) -> torch.Tensor:
    """k(λ) = normalize(√(1-λ²)·k_real + λ·z)，逐行（chunk×head）。"""
    mixed = math.sqrt(1.0 - lam * lam) * k_real + lam * z
    return F.normalize(mixed, dim=-1)


@torch.no_grad()
def run_window(model, ns, clean, byte_mask, lambdas, ridge_lam):
    source = clean.masked_fill(byte_mask, MASK_ID)
    chunks, memory, _index = _front_end(model, source)
    n_real = int(chunks.chunk_mask[0].sum())
    gates = model.write_head(memory)
    sm = model.state_machine
    k_real = gates["k"][:, :n_real].float()  # (1, n, H, hk)，已归一化
    v = gates["v"][:, :n_real].float()

    # target grids（与 E73 同口径：累积 as-encoded + own-slot 分解）
    enc_targets, enc_slot, _m, _t = s1.make_cumulative_retention_targets(
        source, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    _bt, own_slot, _bm = s1.make_targets(
        source, torch.zeros_like(byte_mask), chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )

    def chain_acc(v_rows):
        logits = decode_direct(model, v_rows, chunks)
        m, _p, _t2 = _arm_metrics(logits, enc_targets, enc_slot, own_slot)
        return {"acc": m["acc"], "acc_own": m["acc_own"], "acc_recalled": m["acc_recalled"]}

    # 参考行：A1 自然态
    S_tr = trained_states(sm, gates, n_real)
    ref_a1 = chain_acc(read_trained(sm, S_tr))

    # μ 扫描
    gen = torch.Generator(device=k_real.device).manual_seed(20260818)
    z = F.normalize(torch.randn(k_real.shape, generator=gen, device=k_real.device), dim=-1)
    levels = []
    for lam in lambdas:
        gates_l = {**gates, "k": mix_keys(k_real, z, lam)}
        realized_mu = sum(
            row_geometry(gates_l["k"][0, :, h])["mu"] for h in range(k_real.size(2))
        ) / k_real.size(2)
        S_l = oracle_states(gates_l, n_real)
        q_line = chain_acc(read_trained(sm, S_l))
        vh, cos_r = ridge_unmix(gates_l, S_l, ridge_lam)
        r_line = chain_acc(read_via_realign(sm, vh))
        levels.append({
            "lambda": lam,
            "mu_realized": round(realized_mu, 4),
            "ridge_cos": round(cos_r, 4),
            **{f"trainedq_{k}": v for k, v in q_line.items()},
            **{f"ridge_{k}": v for k, v in r_line.items()},
        })
    return {"n_real": n_real, "ref_A1_natural": ref_a1, "levels": levels}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=C_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16)
    p.add_argument("--lambdas", default=",".join(str(x) for x in LAMBDAS))
    p.add_argument("--ridge-lam", type=float, default=RIDGE_LAM)
    p.add_argument("--out-dir", default="outputs/readout_lockin_20260818")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    lambdas = [float(x) for x in args.lambdas.split(",")]
    t0 = time.time()

    model, ns, step = load_model(Path(args.run_dir), device)
    print(f"[lockin] model={Path(args.run_dir).name} step={step} device={device.type}", flush=True)
    windows = build_eval_windows(ns, args.max_windows)
    masks = build_masks(windows, ns)
    rows = []
    for wi, (clean, bm) in enumerate(zip(windows, masks)):
        rows.append(run_window(model, ns, clean.to(device), bm.to(device), lambdas, args.ridge_lam))
        print(f"[lockin] window {wi} done ({time.time() - t0:.0f}s)", flush=True)

    # aggregate per level
    agg_levels = []
    for li, lam in enumerate(lambdas):
        lv = [r["levels"][li] for r in rows]
        agg = {"lambda": lam}
        for key in lv[0]:
            if key == "lambda":
                continue
            vals = [x[key] for x in lv]
            agg[key] = round(sum(vals) / len(vals), 4)
            agg[key + "_se"] = round((sum((x - agg[key]) ** 2 for x in vals) / max(len(vals) - 1, 1)) ** 0.5 / math.sqrt(len(vals)), 4)
        agg_levels.append(agg)
    ref = [r["ref_A1_natural"] for r in rows]
    ref_a1 = {k: round(sum(x[k] for x in ref) / len(ref), 4) for k in ref[0]}

    report = {
        "probe": "readout-chain lock-in μ-response curve (c grid, v=state)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": Path(args.run_dir).name, "step": step},
        "params": {"windows": len(windows), "lambdas": lambdas, "ridge_lam": args.ridge_lam},
        "construction": "keys mixed toward fixed random directions (values kept real); oracle-cumsum states; "
        "direct decode on the cumulative as-encoded grid (E73 arm protocol)",
        "ref_A1_natural": ref_a1,
        "levels": agg_levels,
        "per_window": rows,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "lockin_curve.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "READOUT LOCK-IN CURVE — c 格读出链 μ 响应（16 窗, direct acc, E73 口径）",
        f"日期 {report['created']}  设备 {device.type}  checkpoint {Path(args.run_dir).name}",
        "",
        f"参考行 A1 自然态 trained-q: acc={ref_a1['acc']} own={ref_a1['acc_own']} recalled={ref_a1['acc_recalled']}",
        "",
        "μ 档（realized）× acc：trained-q 线 / ridge 线（ridge_cos = 解混质量）",
        "  λ      μ       | trained-q acc (own)        | ridge acc (own)          | ridge_cos",
    ]
    for a in agg_levels:
        lines.append(
            f"  {a['lambda']:<5.2f}  {a['mu_realized']:.3f}  | {a['trainedq_acc']:.4f} ({a['trainedq_acc_own']:.4f})     "
            f"| {a['ridge_acc']:.4f} ({a['ridge_acc_own']:.4f})     | {a['ridge_cos']:.3f}"
        )
    lines += [
        "",
        "判读：acc 随 μ 下降而升 ⇒ 锁在键几何；各档皆不动（含 ridge 线）⇒ 锁在 realign/decoder 接口 ⇒ 复训路线。",
        f"完整数据: {out_path}",
    ]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
