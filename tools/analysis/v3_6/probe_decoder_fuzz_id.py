"""decoder 去噪臂前置测量（模糊分布身份证）探针（任务书 2026-08-29 冻结 v1.1:
docs/versions/v3.7/FLUED_V3_7_DECODER_DENOISE_20260829_CN.md §1/§3.4 —— 扰动族
一切参数由本探针实测决定, 不许拍脑袋）。

管线（b 格基座上 b 格内自产自销, Q19 段1/段2 同口径, 全闭式无梯度）:
  段1: K 通道状态 S_i（write_head_k(index) gates 的 KDA 自然递推, fp32 参考
       实现）--ridge 解混(λ_unmix=1e-2, E73/Q19 同档)--> v̂_k（K 通道写值估计）
  段2: v̂_k --ridge 闭式回归(分窗 2-fold, 逐列 RMS 预条件, Q19 ridge_fit_predict
       同函数)--> m̂（memory 行估计, 目标 = 同基座同窗真实 memory 行）
       正则三档 {λ_opt=1.0, λ×10=10.0 欠拟合, λ×0.1=0.1 过拟合} 产出三档模糊度。

与 Q19 的口径差（显式申报, 不静默）:
  F1. 窗口 = 训练流窗口（StreamingReconstructionDataset seed=ns.seed, 前 N 窗,
      掩码 = 训练态 _MASK_GENERATOR 同种子逐窗顺序抽取）——任务书 §1 裁定
      「训练流窗口（与冒烟同源数据）」, 非 Q19 的 eval 窗（seed+9999）口径。
  F2. 状态通道 = b 格自身的 K 通道（k_row_source=state, write_head_k 吃 index
      行）; Q19 段1/段2 跑在 d 格 V 通道上。本探针无跨格借口——基座即生产格。
  F3. 段2 目标 = 同基座真实 memory 行（v_row_source=memory, direct 口的生产
      输入正是它）, 无 Q19-D6 的跨格域移。
  F4. 统计主体 = 分窗 2-fold 的 held-out 预测（拟合窗与测量窗不重叠, Q19 段2
      纪律）; 另拟合一份全窗「部署桥」落盘供训练器装载（训练器用的桥不能在
      held-out 折间摇摆, 全窗拟合是部署件标准做法, 台账两列分清）。
  F5. 残差协方差落盘两份口径: 任务书 §1 测件②的 ε=m−m̂（逐维方差谱 + 有效
      秩）全量入册; 训练器噪声采样用的是「范数匹配后残差」ε_a = m̂ − ρ·m
      (ρ = 实测范数收缩率) 的收缩估计 Cholesky 因子——训练侧合成式为
      ṽ = ρ·m + ε_a, ε_a ~ N(0, Σ̂_a), 使合成行的二阶结构与 m̂ 实测对齐
      （若用 ε=m−m̂ 的协方差再加性混入, 收缩项 (1−ρ)²Cov(m) 会被计两次）。

三档定序: 按 held-out cos(m̂,m) 均值排名——轻档 = cos 最高（模糊最轻）,
重档 = cos 最低。映射入 fuzz_stats.json 的 grade_map, 训练器按它读档。

输出（outputs/decoder_denoise_fuzz_id_20260829/）:
  bridge_{light,mid,heavy}.npz     部署桥 W（含截距行）/scale/λ + 两折 W 备查
  resid_chol_{light,mid,heavy}.npz 训练器噪声采样件: Cholesky L(Σ̂_a) + ρ
  fuzz_stats.json                  三档全量统计（范数收缩/残差谱/有效秩/cos 分布）
  SUMMARY.txt                      人读摘要

Usage:
  python tools/analysis/v3_6/probe_decoder_fuzz_id.py --device cuda
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_decoder_fuzz_id.py --device cpu --max-windows 2
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.train.v3_3.train_v33 import StreamingReconstructionDataset  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    load_model,
    ridge_unmix,
    trained_states,
)
from tools.analysis.v3_6.probe_closed_form_readout import (  # noqa: E402
    _rms,
    decode_rows_donor,
    grid_metrics,
    ridge_fit_predict,
)

BASE_RUN = "checkpoints/v37ks_b_sm_v371_20k_ctx4096_20260817"  # E68 b 格 (任务书 §3.1 已裁定)
OUT_DIR = "outputs/decoder_denoise_fuzz_id_20260829"
LAM_UNMIX = 1e-2  # 段1 ridge 解混 λ (Q19 §1 同口径)
LAM_STAGE2_OPT = 1.0  # 段2 口径最优 λ (Q19 §1 同口径); 三档 = {opt, ×10, ×0.1}
LAM_LADDER = ("opt", "under", "over")  # λ_opt / λ×10 欠拟合 / λ×0.1 过拟合
GRADES = ("light", "mid", "heavy")  # 轻/中/重档 (按 held-out cos 定序, 见模块 docstring)

DECLARED_DEVIATIONS = [
    "F1: 窗口 = 训练流 (seed=42 前 N 窗 + 训练态掩码流), 与冒烟/正式训练同源; 非 Q19 的 eval 窗 (seed+9999) 口径。",
    "F2: 状态通道 = b 格自身 K 通道 (write_head_k(index) gates 自然递推); Q19 段1/2 跑在 d 格 V 通道, 本探针零跨格。",
    "F3: 段2 目标 = 同基座真实 memory 行 (v_row_source=memory), 无 Q19-D6 域移。",
    "F4: 统计主体 = 分窗 2-fold held-out; 另拟合全窗「部署桥」落盘供训练器装载 (两列分清, 不混)。",
    "F5: 测件② ε=m−m̂ 全量入册; 训练器噪声采样件 = 范数匹配后残差 ε_a=m̂−ρ·m 的收缩 Cholesky"
    " (合成式 ṽ=ρ·m+ε_a, 防收缩项被计两次)。",
]


# ---------------------------------------------------------------------------
# 训练流窗口 + 训练态掩码（与冒烟/正式训练同源, F1）
# ---------------------------------------------------------------------------


def build_train_windows(ns, count: int) -> list[torch.Tensor]:
    """训练流前 count 窗: StreamingReconstructionDataset(seed=ns.seed), 与
    make_dataloaders 的训练侧同构造 (batch=1 时窗 i = 训练第 i+1 批)。"""
    ds = StreamingReconstructionDataset(
        file_path=ns.data_path,
        seq_len=ns.seq_len,
        samples_per_worker=getattr(ns, "stream_samples_per_worker", 50000),
        seed=ns.seed,  # 训练流种子 (eval 窗是 +9999, 这里刻意不加)
    )
    loader = torch.utils.data.DataLoader(ds, batch_size=ns.batch_size, shuffle=False, num_workers=0)
    out = []
    for i, batch in enumerate(loader):
        if i >= count:
            break
        out.append(batch[0])
    return out


def build_train_masks(cleans: list[torch.Tensor], ns) -> list[torch.Tensor]:
    """训练态掩码流复演: main() 的 _MASK_GENERATOR.manual_seed(seed) 后逐批
    顺序抽取 (本基座 run 无 cloze/retrieval/burst 消费, 流序一一对应)。"""
    s1._MASK_GENERATOR.manual_seed(ns.seed)
    return [
        s1.make_mixed_mask(
            c,
            ns.mask_prob,
            char_frac=getattr(ns, "mask_char_frac", 0.4),
            char_span_max=getattr(ns, "mask_char_span_max", 3),
            tokenizer=s1._BPE_TOKENIZER,
            generator=s1._MASK_GENERATOR,
        )
        for c in cleans
    ]


# ---------------------------------------------------------------------------
# 逐窗采集: 前端 → K gates → K 自然态 → 段1 解混 v̂_k + 真 memory 行 + 端口锚
# ---------------------------------------------------------------------------


@torch.no_grad()
def collect_window(model, ns, clean, byte_mask, device, wi):
    source = clean.masked_fill(byte_mask, MASK_ID)
    chunks, memory, index = _front_end(model, source)
    n_real = int(chunks.chunk_mask[0].sum())
    gates_k = model.write_head_k(index)  # K 通道写门 (b 格, F2)
    S_nat = trained_states(model.state_machine_k, gates_k, n_real)  # fp32 参考递推
    vh_k, cos_unmix = ridge_unmix(gates_k, S_nat, LAM_UNMIX)  # 段1: (1, n, H*hv)
    m = memory[0, :n_real].float().cpu()  # 真 memory 行 (n, d_mem)

    # 端口在岗锚: 真 memory 行直喂 decoder_in_mem+pos→decoder (E68 水位复现口径,
    # fine 本段 as-encoded 格, Q19 D4 同款)
    zeros = torch.zeros_like(byte_mask)
    targets_enc, slot_mask, _m = s1.make_targets(
        source, zeros, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    logits = decode_rows_donor(model, memory[:, :n_real].float(), chunks.token_mask)
    anchor = grid_metrics(
        logits, targets_enc.to(device), slot_mask.to(device), targets_enc.to(device), torch.zeros_like(slot_mask).to(device)
    )

    return {
        "window": wi,
        "n_real": n_real,
        "cos_unmix": round(cos_unmix, 4),
        "anchor_direct_acc": round(anchor["acc"], 4),
        "vh": vh_k[0].float().cpu(),  # (n, H*hv) 段1 写值估计
        "m": m,  # (n, d_mem) 段2 目标真值
    }


# ---------------------------------------------------------------------------
# 段2: 全窗部署桥（ridge_fit_predict 同口径: RMS 预条件 + 截距, 单折全量）
# ---------------------------------------------------------------------------


def ridge_fit_all(xs_by_win: list[torch.Tensor], ys_by_win: list[torch.Tensor], lam: float):
    """全窗拟合部署桥 (F4): 与 ridge_fit_predict 同一闭式形态 (特征除全列
    pooled RMS 标量 + 截距行), 只是不分折。全部 CPU fp32。Returns (W, scale),
    W 末行为截距。"""
    X = torch.cat([x.float().cpu() for x in xs_by_win])
    Y = torch.cat([y.float().cpu() for y in ys_by_win])
    scale = _rms(X)
    X = torch.cat([X / scale, torch.ones(X.size(0), 1)], dim=1)
    W = torch.linalg.solve(X.T @ X + lam * torch.eye(X.size(1)), X.T @ Y)
    return W, float(scale)


def apply_bridge(vh: torch.Tensor, W: torch.Tensor, scale: float) -> torch.Tensor:
    """部署桥应用 (训练器同款): v̂ (..., F) -> m̂ (..., d_mem)。末维拼接 1 走截距。"""
    x = torch.cat([vh.float() / scale, torch.ones(*vh.shape[:-1], 1, device=vh.device)], dim=-1)
    return x @ W


@torch.no_grad()
def mhat_from_window(model, index: torch.Tensor, chunk_mask: torch.Tensor, W: torch.Tensor, scale: float):
    """训练器 m̂ 列的逐窗生产件 (batch-1, no_grad, fp32): index 行 → K gates →
    K 自然态 → 段1 解混 v̂_k → 部署桥 → m̂ (1, n_real, d_mem)。与采集侧逐行
    同口径 (trained_states/ridge_unmix/apply_bridge 同函数)。"""
    n_real = int(chunk_mask[0].sum())
    gates_k = model.write_head_k(index.float())
    S_nat = trained_states(model.state_machine_k, gates_k, n_real)
    vh_k, _cos = ridge_unmix(gates_k, S_nat, LAM_UNMIX)
    return apply_bridge(vh_k, W.to(vh_k.device), scale)


# ---------------------------------------------------------------------------
# 模糊三件套测量: 范数收缩率 / 残差协方差结构 / cos 分布
# ---------------------------------------------------------------------------


def _quantiles(x: torch.Tensor) -> dict:
    qs = torch.quantile(x.float(), torch.tensor([0.05, 0.25, 0.5, 0.75, 0.95]))
    return {f"q{q}": round(float(v), 6) for q, v in zip((5, 25, 50, 75, 95), qs)}


def ledoit_wolf_shrink(X: torch.Tensor):
    """Ledoit-Wolf 恒等靶收缩估计 (fp64): Σ̂ = (1−δ)S + δμI, μ=tr(S)/d。
    Returns (Σ̂ fp32, δ)。X (N, d) 已中心化与否皆可 (内部中心化)。"""
    X = X.double()
    X = X - X.mean(dim=0, keepdim=True)
    N, d = X.shape
    S = (X.T @ X) / N
    mu = torch.diag(S).mean()
    d2 = (S - mu * torch.eye(d, dtype=torch.float64)).pow(2).sum() / d
    # b̄² = mean_k ||x_k x_kᵀ − S||²_F / (N d); ||xxᵀ−S||²_F = (xᵀx)² − 2xᵀSx + ||S||²_F
    xTx = X.pow(2).sum(dim=1)
    xSx = ((X @ S) * X).sum(dim=1)
    b2 = (xTx.square() - 2 * xSx + S.pow(2).sum()).mean() / (N * d)
    delta = float((b2 / d2).clamp(0.0, 1.0))
    shrunk = (1 - delta) * S + delta * mu * torch.eye(d, dtype=torch.float64)
    return shrunk.float(), delta


def measure_grade(mhat_by_win: list[torch.Tensor], m_by_win: list[torch.Tensor], tag: str, lam: float) -> dict:
    """三件套 (held-out 池化, 任务书 §1 测件①②③) + 训练器采样件 (F5)。"""
    mhat = torch.cat(mhat_by_win).float()  # (N, d)
    m = torch.cat(m_by_win).float()
    cos = F.cosine_similarity(mhat, m, dim=-1)
    norm_ratio = mhat.norm(dim=-1) / m.norm(dim=-1).clamp(min=1e-12)
    rho = float(norm_ratio.mean())

    # 测件②: ε = m − m̂ 协方差结构 (逐维方差谱 + SVD 有效秩)
    eps = m - mhat
    eps_c = eps - eps.mean(dim=0, keepdim=True)
    var_spectrum = eps_c.pow(2).mean(dim=0)  # 逐维方差谱 (d,)
    sv = torch.linalg.svdvals(eps_c.double())
    lam2 = sv.square()
    eff_rank = float(lam2.sum().square() / lam2.square().sum().clamp(min=1e-24))

    # 训练器采样件 (F5): 范数匹配后残差 ε_a = m̂ − ρ·m 的收缩 Cholesky
    eps_a = mhat - rho * m
    cov_a, delta = ledoit_wolf_shrink(eps_a)
    jitter = 1e-8 * float(torch.diag(cov_a.double()).mean())
    L = torch.linalg.cholesky(cov_a.double() + jitter * torch.eye(cov_a.size(0), dtype=torch.float64)).float()

    return {
        "tag": tag,
        "lam": lam,
        "n_rows": int(m.size(0)),
        "cos": {"mean": round(float(cos.mean()), 6), "std": round(float(cos.std()), 6), **_quantiles(cos)},
        "norm_ratio": {"mean": round(rho, 6), "std": round(float(norm_ratio.std()), 6), **_quantiles(norm_ratio)},
        "resid": {
            "var_spectrum": [round(float(v), 8) for v in var_spectrum],  # ε=m−m̂ 逐维方差谱
            "eff_rank": round(eff_rank, 2),  # SVD 参与比有效秩
            "total_var": round(float(var_spectrum.sum()), 6),
        },
        "sampler": {"rho": rho, "shrink_delta": round(delta, 6), "jitter": jitter},
        "_chol": L,  # 内部传递, 落 npz 不进 JSON
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--base-run-dir", default=BASE_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=32, help="训练流窗数 (默认 32; Q19 是 16 窗 eval 口径)")
    p.add_argument("--out-dir", default=OUT_DIR)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, base_step = load_model(Path(args.base_run_dir), device)
    # 接口断言 (loud): b 格必须有 decoder_in_mem 端口且 k=state/v=memory
    if getattr(ns, "backbone_mode", "") != "slm" or getattr(ns, "v_row_source", "") != "memory":
        raise ValueError(f"{args.base_run_dir}: 预期 slm b 格 v_row_source='memory', got {ns.v_row_source!r}")
    if getattr(ns, "k_row_source", "") != "state" or not hasattr(model, "write_head_k"):
        raise ValueError(f"{args.base_run_dir}: 预期 k_row_source='state' + write_head_k 在岗")
    if not hasattr(model, "decoder_in_mem"):
        raise ValueError(f"{args.base_run_dir}: 缺 decoder_in_mem 端口")
    print(f"[fuzz-id] base={Path(args.base_run_dir).name} step={base_step} device={device.type}", flush=True)

    windows = build_train_windows(ns, args.max_windows)
    masks = build_train_masks(windows, ns)
    print(f"[fuzz-id] {len(windows)} 训练流窗 + 训练态掩码就位（{time.time() - t0:.0f}s）", flush=True)

    recs = []
    for wi, (clean, byte_mask) in enumerate(zip(windows, masks)):
        recs.append(collect_window(model, ns, clean.to(device), byte_mask.to(device), device, wi))
        print(
            f"[fuzz-id] window {wi} n_real={recs[-1]['n_real']} cos_unmix={recs[-1]['cos_unmix']:.3f} "
            f"锚 direct_acc={recs[-1]['anchor_direct_acc']:.3f}（{time.time() - t0:.0f}s）",
            flush=True,
        )
    n_win = len(recs)
    m_by_win = [r["m"] for r in recs]
    vh_by_win = [r["vh"] for r in recs]
    anchor_acc = round(sum(r["anchor_direct_acc"] for r in recs) / n_win, 4)

    # 段2 三档: held-out 2-fold (测量) + 全窗部署桥 (落盘)
    lam_map = {"opt": LAM_STAGE2_OPT, "under": LAM_STAGE2_OPT * 10.0, "over": LAM_STAGE2_OPT * 0.1}
    per_tag: dict[str, dict] = {}
    for tag in LAM_LADDER:
        lam = lam_map[tag]
        preds, folds = ridge_fit_predict(vh_by_win, m_by_win, lam)
        st = measure_grade(preds, m_by_win, tag, lam)
        W_all, scale_all = ridge_fit_all(vh_by_win, m_by_win, lam)
        st["_folds"] = folds
        st["_deploy"] = (W_all, scale_all)
        per_tag[tag] = st
        print(
            f"[fuzz-id] λ={lam:<5} held-out cos={st['cos']['mean']:.4f}±{st['cos']['std']:.4f} "
            f"ρ={st['norm_ratio']['mean']:.4f} eff_rank={st['resid']['eff_rank']:.0f}（{time.time() - t0:.0f}s）",
            flush=True,
        )

    # 三档定序: held-out cos 均值降序 → 轻/中/重
    order = sorted(LAM_LADDER, key=lambda t: per_tag[t]["cos"]["mean"], reverse=True)
    grade_map = {grade: tag for grade, tag in zip(GRADES, order)}  # light=cos 最高

    # 落盘: 桥 + Cholesky + 统计
    for grade, tag in grade_map.items():
        st = per_tag[tag]
        W_all, scale_all = st["_deploy"]
        np.savez(
            out_dir / f"bridge_{grade}.npz",
            W=W_all.numpy(),
            scale=np.float64(scale_all),
            lam=np.float64(st["lam"]),
            W_fold0=st["_folds"][0]["W"].numpy(),
            scale_fold0=np.float64(st["_folds"][0]["scale"]),
            W_fold1=st["_folds"][1]["W"].numpy() if len(st["_folds"]) > 1 else st["_folds"][0]["W"].numpy(),
            scale_fold1=np.float64(st["_folds"][1]["scale"] if len(st["_folds"]) > 1 else st["_folds"][0]["scale"]),
        )
        np.savez(
            out_dir / f"resid_chol_{grade}.npz",
            L=st["_chol"].numpy(),
            rho=np.float64(st["sampler"]["rho"]),
            lam=np.float64(st["lam"]),
        )

    stats = {
        "probe": "decoder 去噪臂前置测量 (模糊分布身份证)",
        "spec": "docs/versions/v3.7/FLUED_V3_7_DECODER_DENOISE_20260829_CN.md",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "base": {"run": Path(args.base_run_dir).name, "step": base_step},
        "declared_deviations": DECLARED_DEVIATIONS,
        "params": {
            "windows": n_win,
            "lam_unmix": LAM_UNMIX,
            "lam_ladder": {t: lam_map[t] for t in LAM_LADDER},
            "stream": "train (seed=42 训练流窗 + 训练态掩码流, F1)",
        },
        "anchor": {"cleartext_direct_acc": anchor_acc, "note": "真 memory 行直喂 direct 口 (E68 收官 0.7917 同格参照)"},
        "grade_map": grade_map,  # light/mid/heavy -> opt/under/over (按 held-out cos 降序)
        "per_tag": {
            tag: {k: v for k, v in per_tag[tag].items() if not k.startswith("_")} for tag in LAM_LADDER
        },
        "per_grade": {
            grade: {k: v for k, v in per_tag[tag].items() if not k.startswith("_")}
            for grade, tag in grade_map.items()
        },
        "per_window": [
            {"window": r["window"], "n_real": r["n_real"], "cos_unmix": r["cos_unmix"], "anchor_direct_acc": r["anchor_direct_acc"]}
            for r in recs
        ],
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "fuzz_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "decoder 去噪臂前置测量 —— 模糊分布身份证（任务书 2026-08-29 冻结 v1.1 §1）",
        f"日期 {stats['created']}  设备 {device.type}  训练流窗 {n_win}（F1: seed=42 训练流 + 训练态掩码, 与冒烟同源）",
        f"基座 {Path(args.base_run_dir).name} (step {base_step}, E68 b 格) | 段1 λ_unmix={LAM_UNMIX} | 段2 λ 梯 {lam_map}",
        f"端口在岗锚: 真 memory 行直喂 direct 口 acc={anchor_acc}（E68 收官 0.7917 同格参照; 窗口径 F1 有差）",
        "",
        "已申报口径偏差（不静默）:",
        *[f"  {d}" for d in DECLARED_DEVIATIONS],
        "",
        f"三档定序（held-out cos 降序 → 轻/中/重）: {grade_map}",
        "",
        "三档模糊度实测（held-out 池化, 拟合窗与测量窗不重叠）:",
    ]
    for grade in GRADES:
        tag = grade_map[grade]
        st = per_tag[tag]
        lines.append(f"== {grade} 档 (λ_stage2={st['lam']}, {tag}) ==")
        lines.append(
            f"  范数收缩率 ρ: mean={st['norm_ratio']['mean']:.4f} std={st['norm_ratio']['std']:.4f} "
            f"[q05 {st['norm_ratio']['q5']:.4f} / q50 {st['norm_ratio']['q50']:.4f} / q95 {st['norm_ratio']['q95']:.4f}]"
        )
        lines.append(
            f"  cos(m̂,m): mean={st['cos']['mean']:.4f} std={st['cos']['std']:.4f} "
            f"[q05 {st['cos']['q5']:.4f} / q50 {st['cos']['q50']:.4f} / q95 {st['cos']['q95']:.4f}]"
        )
        lines.append(
            f"  残差 ε=m−m̂: 有效秩 {st['resid']['eff_rank']:.1f} / 总方差 {st['resid']['total_var']:.4f} "
            f"(逐维方差谱入 fuzz_stats.json) | 采样件收缩 δ={st['sampler']['shrink_delta']:.4f}"
        )
    lines += [
        "",
        "段1 解混在岗: cos_unmix 逐窗均值 "
        f"{sum(r['cos_unmix'] for r in recs) / n_win:.4f}（K 通道写值估计质量, 段2 输入上限）",
        "",
        "落盘件: bridge_{light,mid,heavy}.npz（部署桥 W/scale + 两折备查）, "
        "resid_chol_{light,mid,heavy}.npz（训练器采样件: Cholesky L + ρ）, fuzz_stats.json（全量统计）",
        f"完整数据: {out_dir / 'fuzz_stats.json'}",
    ]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
