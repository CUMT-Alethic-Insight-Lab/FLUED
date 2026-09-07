"""v3.7 Q19 闭式三段臂探针 (任务书 2026-08-27 冻结;
spec: docs/versions/v3_7/FLUED_V3_7_Q19_CLOSED_FORM_READOUT_20260827_CN.md).

合成判例（零 checkpoint 依赖）:
(1) ridge 两段合成: 可解混玩具态（oracle cumsum, 键已知）上 段1 cos≈1 ->
    段2 ridge v̂→m̂ held-out cos≈1 -> 玩具段3（固定线性 decoder 面）端到端
    acc≈1 —— 管线在"数学上可读"的输入上必须满分（容量墙若纯为表示容量,
    闭式解就该这样过）;
(2) 置乱列地板: 状态行置乱后段1 cos≈0 且端到端贴玩具先验;
(3) 明文列直通 sanity + grid_metrics 接线: 真 memory 行进段3 = 玩具 decoder
    自身 direct 水位（满分）, 且 as-encoded/clean/masked 拆分与逐槽计数正确;
(4) prior_acc / ridge_fit_predict 折纪律手算。
"""

from __future__ import annotations

import pytest
import torch
import torch.nn.functional as F

from tools.analysis.v3_6 import probe_closed_form_readout as q19
from tools.analysis.v3_6.probe_oracle_write_verdict import ridge_unmix

N_CLS = 258  # PAD-offset byte vocab + MASK/sentinel 档（与网格同宽）


def _toy_world(n=48, hk=96, hv=16, dm=20, seed=0):
    """可解混玩具态: k 单位范数（hk≥n 保证解混精确）, S = oracle cumsum;
    memory 行 m = A v（段2 精确可解）; 玩具段3 = 固定线性面 D, y=argmax(Dm)
    （构造上真 m 满分解码 = 玩具 decoder 自身 direct 水位 1.0）。"""
    g = torch.Generator().manual_seed(seed)
    k = F.normalize(torch.randn(1, n, 1, hk, generator=g), dim=-1)
    v = torch.randn(1, n, 1, hv, generator=g)
    S = torch.einsum("bchk,bchv->bchkv", k, v).cumsum(dim=1)  # oracle_states 同款
    A = torch.randn(dm, hv, generator=g)
    D = torch.randn(N_CLS, dm, generator=g)
    m = v[0, :, 0] @ A.T  # (n, dm)
    y = (m @ D.T).argmax(dim=-1)  # (n,) 构造性可解码标签
    return {"k": k, "v": v, "S": S, "A": A, "D": D, "m": m, "y": y}


def _stage2_split(t: torch.Tensor, n_folds=4):
    """把 (n, d) 行切成若干伪窗（ridge_fit_predict 的分窗输入形态）。"""
    return list(torch.chunk(t, n_folds, dim=0))


# --- 1. ridge 两段合成判例: 端到端应 ≈1 --------------------------------------------


def test_two_stage_closed_form_end_to_end_near_perfect():
    w = _toy_world()
    v_hat, cos = ridge_unmix({"k": w["k"], "v": w["v"]}, w["S"], 1e-4)
    assert cos > 0.99  # 段1: oracle 玩具态 ridge 解混近完美（E73 cos≈1 同族）
    preds, _ws = q19.ridge_fit_predict(_stage2_split(v_hat[0]), _stage2_split(w["m"]), lam=1e-4)
    m_hat = torch.cat(preds)
    assert q19.row_cos(m_hat, w["m"]) > 0.98  # 段2: held-out 窗上 m̂≈m
    acc = float((m_hat @ w["D"].T).argmax(dim=-1).eq(w["y"]).float().mean())
    assert acc > 0.9  # 段3: 玩具 decoder 面端到端 ≈1


# --- 2. 置乱列地板行为 --------------------------------------------------------------


def test_shuffled_states_floor():
    w = _toy_world()
    n = w["S"].size(1)
    perm = torch.randperm(n, generator=torch.Generator().manual_seed(q19.SHUF_SEED))
    S_shuf = w["S"][:, perm]
    _vh, cos_shuf = ridge_unmix({"k": w["k"], "v": w["v"]}, S_shuf, 1e-4)
    # 结构性注记（实测校准）: cumsum 态行置乱后, perm(i)≥i 的位置仍含 v_i
    # （对角包容幸存一半）, 良条件键下段1 cos 残留 ~0.4-0.5 是几何必然, 不是
    # 泄漏——地板纪律的硬判据在端到端 acc 贴先验（下两行）, 段1 cos 列只作
    # 台账对照（真机键塌缩+衰减下该残留预期更低, 以实跑读数为准）。
    _vh_o, cos_or = ridge_unmix({"k": w["k"], "v": w["v"]}, w["S"], 1e-4)
    assert cos_or > 0.99
    assert cos_shuf < 0.6 and cos_shuf < cos_or - 0.4
    preds, _ = q19.ridge_fit_predict(_stage2_split(_vh[0]), _stage2_split(w["m"]), lam=1e-4)
    m_hat = torch.cat(preds)
    acc = float((m_hat @ w["D"].T).argmax(dim=-1).eq(w["y"]).float().mean())
    prior = float(torch.bincount(w["y"], minlength=N_CLS).max()) / n  # 常数众数先验
    assert acc <= prior + 0.05  # 端到端贴先验 = 地板行为（无泄漏方向）


# --- 3. 明文列直通 sanity + grid_metrics 接线 ----------------------------------------


def _grid_from_rows(rows_logits: torch.Tensor, targets: torch.Tensor, masked_slot: torch.Tensor | None = None):
    """(C,) 目标 -> (1, C, S=1) 单槽网格 + (1, C, 1, N_CLS) logits。"""
    C = targets.numel()
    tgt = targets.view(1, C, 1)
    slot_mask = torch.ones(1, C, 1, dtype=torch.bool)
    ms = masked_slot.view(1, C, 1) if masked_slot is not None else torch.zeros(1, C, 1, dtype=torch.bool)
    logits = rows_logits.view(1, C, 1, N_CLS)
    return logits, tgt, slot_mask, ms


def test_cleartext_passthrough_matches_direct_watermark():
    w = _toy_world()
    logits_rows = w["m"] @ w["D"].T  # 真 memory 行进玩具段3
    masked = torch.zeros(w["m"].size(0), dtype=torch.bool)
    masked[3] = masked[7] = True  # 两个 masked 槽（as-encoded 视图 target=MASK_ID=256）
    tgt_clean = w["y"]
    tgt_enc = tgt_clean.clone()
    tgt_enc[masked] = 256
    logits, te, sm_, ms = _grid_from_rows(logits_rows, tgt_enc, masked)
    m1 = q19.grid_metrics(logits, te, sm_, tgt_clean.view(1, -1, 1), ms)
    # 明文列 = decoder 自身 direct 水位: clean 视图满分（masked 槽也满分,
    # 玩具 decoder 内容完备）; as-encoded 主口径在 masked 槽失分（target 是
    # MASK_ID=256 而预测是内容字节）—— 拆分接线正确
    assert m1["acc"] == pytest.approx(1.0 - 2 / w["y"].numel())
    assert m1["acc_clean"] == pytest.approx(1.0)
    assert m1["acc_clean_unmasked"] == pytest.approx(1.0)
    assert m1["acc_clean_masked"] == pytest.approx(1.0)
    assert m1["n_slots"] == w["y"].numel()
    # 逐槽 breakdown: 全量落 slot0 桶（单槽网格）, 计数守恒
    assert m1["per_slot_cnt"][0] == m1["n_slots"]
    assert sum(m1["per_slot_cnt"]) == m1["n_slots"]
    # 同一输入再过一次 = 同一读数（明文列 ≡ decoder 自身 direct 的 sanity 形态）
    m2 = q19.grid_metrics(logits, te, sm_, tgt_clean.view(1, -1, 1), ms)
    assert m1["acc"] == m2["acc"] and m1["acc_clean"] == m2["acc_clean"]
    # 聚合器: 逐槽池化 + 标量均值
    agg = q19.merge_grid_metrics([m1, m2])
    assert agg["acc"] == pytest.approx(1.0 - 2 / w["y"].numel(), abs=2e-4)  # 聚合行 round 4 位
    assert agg["per_slot_clean"][0] == pytest.approx(1.0)


# --- 4. prior_acc / ridge_fit_predict 折纪律 ----------------------------------------


def test_prior_acc_constant_and_majority():
    tgt = torch.tensor([[[5, 5, 9]]])
    sm_ = torch.tensor([[[True, True, True]]])
    acc, maj = q19.prior_acc(tgt, sm_)
    assert maj == 5 and acc == pytest.approx(2 / 3)
    tgt2 = torch.tensor([[[7, 7, 7]]])
    acc2, maj2 = q19.prior_acc(tgt2, sm_)
    assert maj2 == 7 and acc2 == pytest.approx(1.0)


def test_ridge_fit_predict_fold_discipline():
    # 精确线性世界: held-out 预测满分; 折划分 = 偶/奇窗
    g = torch.Generator().manual_seed(1)
    feats = [torch.randn(8, 8, generator=g) for _ in range(4)]
    Wf = torch.randn(9, 6, generator=g)
    targs = [torch.cat([f, torch.ones(8, 1)], dim=1) @ Wf for f in feats]
    preds, ws = q19.ridge_fit_predict(feats, targs, lam=1e-6)
    assert len(preds) == 4 and len(ws) == 2
    for p, t in zip(preds, targs):
        assert torch.allclose(p, t, atol=1e-3)  # held-out 也精确（线性可解）
    # RMS 预条件（D5）: 特征缩比 1e-3 后固定 λ 不再变相过正则, 仍精确拟合
    feats_small = [f * 1e-3 for f in feats]
    preds_s, ws_s = q19.ridge_fit_predict(feats_small, targs, lam=1e-6)
    for p, t in zip(preds_s, targs):
        assert torch.allclose(p, t, atol=1e-3)
    assert all(w_["scale"] < 1e-2 for w_ in ws_s)  # 预条件标量确实被估计并使用
    # 单窗退化路径（冒烟）: 不炸, 形状保持
    preds1, _ = q19.ridge_fit_predict(feats[:1], targs[:1], lam=1e-6)
    assert preds1[0].shape == targs[0].shape
