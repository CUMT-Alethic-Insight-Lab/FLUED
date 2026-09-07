"""E123 前置门③ 余弦-距离曲线（2026-09-07，冻结任务书 §3.3；零训练）。

固定查询方向余弦沿写入-读取距离 k（chunk 单位）的衰减测量。病因分型：
  - 距离平滑衰减 = 干涉挤压（后续写入旋转/挤压内容方向；修法：结构化写入）；
  - 全程平坦近盲 = 查询压根没学/通道不携带（修法：梯度压力 = E123 合体臂）。
兼作论文机制章供数。基座 = a-w1 10K（冻结记录施工核实例②钉死）。

口径（格无关、部署形态）：
  读出面 = 生产读出行 v_rows（native _slm_store_rows，chunk 行的部署读表面）；
  固定查询 q = 全池 byte-probe ridge 权重矩阵（截距剥离）的 SVD 主方向；
  距离-k 内容方向 d_k = 池化 ridge：全窗对 (c, t=c+k) 上 v_rows[t] → chunk c 的
  字节 onehot（逐槽 0-3），λ=1.0；n_pairs<40 的槽跳过。
  曲线 A: cos(q, d_k) vs k（分型主读）；曲线 B: cos(d_0, d_k) vs k（自衰减，
  干涉旋转的查询无关读数）；零基线：同范数随机方向 cos 均值±sd。
判读只在 CUDA 线（kda_impl=fla）；任务注入零；mask 纪律照 build_masks。
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

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from flued.data import MASK_ID, PAD_ID  # noqa: E402
from tools.analysis.v3_6.probe_e122_necessity_book import assert_cell_keys  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    load_model,
)
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402

BASE_RUN = "checkpoints/v37ks_a_d1_w1_10k_ctx4096_20260904"
OUT_DIR = "outputs/e123_gate_cosine_distance_20260907"
PROBE_SLOTS = 4  # 逐槽字节目标 0-3（E73 A6 / Q19 同款）
LAM = 1.0
N_MIN = 40


def ridge_slot(X: torch.Tensor, y: torch.Tensor, valid: torch.Tensor, lam: float):
    """池化 ridge 权重矩阵（截距含）→ (F+1, 258)；样本不足返回 None。"""
    out = {}
    for s in range(y.size(1)):
        m = valid[:, s]
        if int(m.sum()) < N_MIN:
            continue
        x, yv = X[m].float(), y[m][:, s].long()
        x1 = torch.cat([x, torch.ones(x.size(0), 1, device=x.device)], dim=1)
        y1 = F.one_hot(yv.clamp(min=0, max=257), 258).float()
        W = torch.linalg.solve(x1.T @ x1 + lam * torch.eye(x1.size(1), device=x.device), x1.T @ y1)
        out[s] = W
    return out


def top_direction(W: dict[int, torch.Tensor]) -> torch.Tensor | None:
    """槽权重（截距剥离）拼接矩阵的 SVD 主方向（固定查询/内容方向）。"""
    mats = [W[s][:-1] for s in sorted(W) if W[s] is not None]
    if not mats:
        return None
    M = torch.cat(mats, dim=1)  # (F, 258*n_slots)
    u, _s, _v = torch.linalg.svd(M.float(), full_matrices=False)
    return u[:, 0]


def cos(a: torch.Tensor, b: torch.Tensor) -> float:
    return float((a @ b) / (a.norm() * b.norm() + 1e-12))


def null_baseline(dim: int, seed: int = 0) -> tuple[float, float]:
    """同范数随机方向 cos 基线（均值±sd，n=200）。"""
    g = torch.Generator().manual_seed(seed)
    cs = []
    for _ in range(200):
        a = torch.randn(dim, generator=g)
        b = torch.randn(dim, generator=g)
        cs.append(cos(a, b))
    mean = sum(cs) / len(cs)
    sd = math.sqrt(sum((c - mean) ** 2 for c in cs) / (len(cs) - 1))
    return mean, sd


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", default=BASE_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=32)
    p.add_argument("--max-k", type=int, default=16, help="曲线最远距离（chunk 数）")
    p.add_argument("--data-path", default=None, help="语料路径覆写（远端跑必须）")
    p.add_argument("--out-dir", default=OUT_DIR)
    p.add_argument("--cell-relaxed", action="store_true",
                   help="a 格档：坑 8 五键存在性+通用键不放宽、行源世代差允许")
    args = p.parse_args()
    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, step = load_model(Path(args.ckpt), device)
    assert_cell_keys(ns, model.config, strict=not args.cell_relaxed)  # 坑 8
    ns.burst_prob = 0
    ns.cloze_prob = 0
    ns.retrieval_prob = 0
    if args.data_path:
        ns.data_path = args.data_path
    batch_size = max(int(ns.batch_size), 1)
    n_batches = math.ceil(args.max_windows / batch_size)
    windows = build_eval_windows(ns, n_batches)
    masks = build_masks(windows, ns)
    print(f"[e123-cos] ckpt={Path(args.ckpt).name} step={step} device={device.type} "
          f"windows={args.max_windows} max_k={args.max_k}", flush=True)

    # 采集：逐窗 v_rows + 逐 chunk 字节目标/有效掩码
    X_rows, Ys, Yv, n_real_total = [], [], [], 0
    wi = 0
    for batch, mbatch in zip(windows, masks):
        for j in range(batch.size(0)):
            if wi >= args.max_windows:
                break
            ids = batch[j]
            cut = int(ids.ne(PAD_ID).sum())
            clean = ids[:cut].unsqueeze(0).to(device)
            byte_mask = mbatch[j][:cut].unsqueeze(0).to(device)
            source = clean.masked_fill(byte_mask, MASK_ID)
            chunks, _memory, _index = _front_end(model, source)
            n_real = int(chunks.chunk_mask[0].sum())
            v_rows = model._slm_store_rows(chunks)[1][:, :n_real].float()  # 生产读出行
            zeros = torch.zeros_like(byte_mask)
            base_targets, base_slot, _bm = s1.make_targets(
                clean, zeros, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
            )
            X_rows.append(v_rows[0])                                   # (n, F)
            Ys.append(base_targets[0, :n_real, :PROBE_SLOTS].long())   # (n, S)
            Yv.append(base_slot[0, :n_real, :PROBE_SLOTS].bool())      # (n, S)
            n_real_total += n_real
            if wi == 0:
                print(f"[e123-cos] win0: n_real={n_real} F={v_rows.size(-1)}", flush=True)
            wi += 1
        if wi >= args.max_windows:
            break
    X = torch.cat(X_rows)          # (N, F)
    Y = torch.cat(Ys)              # (N, S)
    V = torch.cat(Yv)              # (N, S)
    F_dim = X.size(1)
    print(f"[e123-cos] pooled N={X.size(0)} rows, F={F_dim} ({time.time()-t0:.0f}s)", flush=True)

    # 固定查询 q = k=0 全池权重主方向
    W0 = ridge_slot(X, Y, V, LAM)
    q = top_direction(W0)
    if q is None:
        raise SystemExit("k=0 无可用槽（样本不足）——查窗流/语料路径")
    d0 = q.clone()

    # 距离-k 池化 ridge：需要 chunk 内偏移 c → 行索引。X_rows 逐窗分段保存了，
    # 这里逐窗重拼对 (c, t=c+k)。
    curve = []
    Wk_stack: dict[int, dict[int, torch.Tensor]] = {0: W0}
    for k in range(1, args.max_k + 1):
        Xk, Yk, Vk = [], [], []
        offset = 0
        for rows, ys, yv in zip(X_rows, Ys, Yv):
            n = rows.size(0)
            if n > k:
                Xk.append(rows[k:])          # t = c+k 的行
                Yk.append(ys[:n - k])        # chunk c 的字节
                Vk.append(yv[:n - k])
            offset += n
        if not Xk:
            curve.append({"k": k, "n_pairs": 0})
            continue
        Wk = ridge_slot(torch.cat(Xk), torch.cat(Yk), torch.cat(Vk), LAM)
        Wk_stack[k] = Wk
        dk = top_direction(Wk)
        n_pairs = int(torch.cat(Xk).size(0))
        if dk is None:
            curve.append({"k": k, "n_pairs": n_pairs})
            continue
        curve.append({
            "k": k,
            "n_pairs": n_pairs,
            "cos_q_dk": round(cos(q, dk), 4),
            "cos_d0_dk": round(cos(d0, dk), 4),
        })
        print(f"[e123-cos] k={k:2d} n={n_pairs:6d} cos(q,d_k)={cos(q,dk):+.4f} "
              f"cos(d0,d_k)={cos(d0,dk):+.4f} ({time.time()-t0:.0f}s)", flush=True)

    null_mean, null_sd = null_baseline(F_dim)
    # 病因分型（冻结任务书 §3.3）：近盲 = 全部 k≥1 的 cos 落在零基线 ±2sd 内
    blind = all(
        abs(r.get("cos_q_dk", 0.0) - null_mean) <= 2 * null_sd
        for r in curve if r.get("cos_q_dk") is not None
    )
    monotone_decay = all(
        r.get("cos_q_dk") is not None
        for r in curve
    ) and all(
        curve[i]["cos_q_dk"] >= curve[i + 1]["cos_q_dk"] - 0.02
        for i in range(len(curve) - 1)
    )
    verdict = (
        "全程平坦近盲——查询压根没学/通道不携带（修法：梯度压力=E123 合体臂）"
        if blind else
        "距离平滑衰减——干涉挤压（修法：结构化写入）" if monotone_decay else
        "非单调/部分盲——分层读数待人工判（曲线入册）"
    )
    summary = {
        "gate": "E123 前置门③ 余弦-距离曲线",
        "ckpt": {"run": Path(args.ckpt).name, "step": step},
        "device": device.type,
        "params": {"max_windows": args.max_windows, "max_k": args.max_k,
                   "lam": LAM, "probe_slots": PROBE_SLOTS, "n_rows": int(X.size(0)),
                   "n_real_total": n_real_total, "F": F_dim},
        "surface": "生产读出行 v_rows（native _slm_store_rows）",
        "fixed_query": "k=0 全池 byte-probe ridge 权重（截距剥离）SVD 主方向",
        "null_baseline": {"mean": round(null_mean, 4), "sd": round(null_sd, 4)},
        "curve": curve,
        "verdict": verdict,
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                          encoding="utf-8")
    torch.save({"q_fixed": q.cpu(), "d0": d0.cpu(),
                "Wk": {k: {s: w.cpu() for s, w in Wk_stack[k].items() if w is not None}
                       for k in Wk_stack}},
               out_dir / "directions.pt")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
