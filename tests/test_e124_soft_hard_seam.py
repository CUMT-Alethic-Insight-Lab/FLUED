"""E124 软训硬评缝（soft-train / hard-eval gate seam）单测 2026-09-11。

配套仪器：tools/analysis/v3_6/probe_e124_soft_hard_gate.py（零训练对拍：同一
ckpt 同一窗软门 rt_hard=False/τ 与硬门 rt_hard=True 前向差分）。红队总审裁定：
缝的大小必须量化进判读注记（top-k 解码必须 top-k 训练的文献判例对口）。

Covers（合成 tiny 模型，backbone 级口径同 test_e124_gate）:
  (1) 缝差分有限、形状对、种子决定论：软/硬两臂（同预算 rt_budget=2, 门激活）
      输出差分经 seam_metrics 全有限、键齐全，同输入重跑逐位同值；
  (2) 退火起点（全量预算 bypass）两臂逐位一致 → 缝指标恰全零（缝=0 的解析锚，
      「门关逐位一致」冒烟条款①在差分仪上的读数形态）；
  (3) seam_metrics / masked_byte_acc 纯函数代数：L∞/KL 手工复算对齐、空 masked
      集返回 None（不算假分数）。

方向性（硬差 ≥ 软差）不强制（任务书口径）；本测只钉「有限/形状/决定论/零点」。
"""

from __future__ import annotations

import math

import pytest
import torch

from flued.v36 import FLUEDV36
from tools.analysis.v3_6.probe_e124_soft_hard_gate import masked_byte_acc, seam_metrics
from tests.test_v37_slm import tiny_config

METRIC_KEYS = {
    "logit_linf", "logit_kl", "gate_tv", "gate_tv_max", "gate_kl",
    "soft_support", "hard_hit", "support_symdiff",
}


def _backbone_io(cfg, bsz: int = 2, n: int = 5):
    torch.manual_seed(0)
    model = FLUEDV36(cfg)
    bb = model.backbone
    torch.manual_seed(1)  # 输入流与构造 RNG 解耦（两臂逐位可比）
    k = torch.randn(bsz, n, cfg.d_mem)
    v = torch.randn(bsz, n, cfg.d_mem)
    cm = torch.ones(bsz, n, dtype=torch.bool)
    pos = torch.randn(1, n, cfg.d_backbone)
    return bb, k, v, cm, pos


def _run_arm(bb, k, v, cm, pos, hard: bool, budget: int | None):
    bb.e124_rt_budget = budget
    bb.e124_rt_progress = 0.0
    bb.e124_rt_hard = hard
    bb.e124_rt_temp = 0.05
    with torch.no_grad():
        out = bb(k, v, cm, pos, need_attn=True)
    return out, bb.last_block1_attn, bb.last_e124_hit


# --- 1. 缝差分：有限 / 形状 / 种子决定论 -------------------------------------------


def test_seam_diff_finite_shaped_deterministic():
    bb, k, v, cm, pos = _backbone_io(tiny_config(e124_budget_gate=True))
    out_h, attn_h, hit_h = _run_arm(bb, k, v, cm, pos, hard=True, budget=2)
    out_s, attn_s, hit_s = _run_arm(bb, k, v, cm, pos, hard=False, budget=2)
    # 审计口契约：硬门有离散命中集，软门 None（门激活前置非空）
    assert hit_h is not None and hit_s is None
    assert out_h.shape == out_s.shape and attn_h.shape == attn_s.shape
    assert float(bb.last_e124_k) == 2.0  # 门确实激活（预算 < 窗内块数）
    m = seam_metrics(out_h, out_s, cm, attn_s, attn_h, hit_h)
    assert set(m) == METRIC_KEYS
    for key, val in m.items():
        assert math.isfinite(val), f"{key} 非有限: {val}"
        assert val >= 0.0, f"{key} 负值: {val}"  # L∞/TV/支撑差均非负量
    # 种子决定论：同输入重跑两臂，差分逐位同值
    out_h2, attn_h2, hit_h2 = _run_arm(bb, k, v, cm, pos, hard=True, budget=2)
    out_s2, attn_s2, hit_s2 = _run_arm(bb, k, v, cm, pos, hard=False, budget=2)
    assert torch.equal(out_h, out_h2) and torch.equal(out_s, out_s2)
    assert torch.equal(attn_h, attn_h2) and torch.equal(attn_s, attn_s2)
    m2 = seam_metrics(out_h2, out_s2, cm, attn_s2, attn_h2, hit_h2)
    assert m2 == m


def test_seam_bypass_is_exactly_zero():
    """全量预算（退火起点）两臂整体 bypass legacy 路径 → 输出逐位一致、缝恰零。"""
    bb, k, v, cm, pos = _backbone_io(tiny_config(e124_budget_gate=True))
    out_h, attn_h, _ = _run_arm(bb, k, v, cm, pos, hard=True, budget=None)
    out_s, attn_s, hit_s = _run_arm(bb, k, v, cm, pos, hard=False, budget=None)
    assert torch.equal(out_h, out_s) and torch.equal(attn_h, attn_s)
    assert hit_s is None  # bypass 不进门内（命中集寄存槽保持关态）
    m = seam_metrics(out_h, out_s, cm, attn_s, attn_h, None)
    assert all(m[key] == 0.0 for key in ("logit_linf", "logit_kl", "gate_tv", "support_symdiff"))


# --- 2. 纯函数代数 ------------------------------------------------------------------


def test_seam_metrics_algebra():
    torch.manual_seed(3)
    logits_s = torch.randn(1, 4, 6)
    logits_h = logits_s.clone()
    logits_h[0, 1, 2] += 0.5  # 单位差 → L∞ = 0.5 可手算
    valid = torch.ones(1, 4, dtype=torch.bool)
    p = torch.softmax(torch.randn(1, 2, 4, 4), dim=-1)
    m = seam_metrics(logits_s, logits_h, valid, p, p.clone(), None)
    assert m["logit_linf"] == pytest.approx(0.5, abs=1e-6)
    assert m["gate_tv"] == 0.0 and m["support_symdiff"] == 0.0
    assert m["soft_support"] == pytest.approx(4.0)  # softmax 全正支持 = 每查询 n=4 行
    # KL 手工复算（valid 位均值；单点扰动下非零）
    ls = torch.log_softmax(logits_s.float(), dim=-1)
    lh = torch.log_softmax(logits_h.float(), dim=-1)
    ref = float((lh.exp() * (lh - ls)).sum(-1).mean())
    assert m["logit_kl"] == pytest.approx(ref, abs=1e-6)
    assert m["logit_kl"] > 0.0
    # 同 logits → KL 恰 0（零点锚）
    m0 = seam_metrics(logits_s, logits_s.clone(), valid, p, p.clone(), None)
    assert m0["logit_kl"] == 0.0 and m0["logit_linf"] == 0.0


def test_masked_byte_acc_algebra_and_empty_guard():
    logits = torch.zeros(1, 3, 5)
    logits[0, :, 1] = 1.0  # argmax = 1
    targets = torch.tensor([[1, 2, 1]])
    slot = torch.tensor([[True, True, False]])
    assert masked_byte_acc(logits, targets, slot) == pytest.approx(0.5)
    empty = torch.zeros(1, 3, dtype=torch.bool)
    assert masked_byte_acc(logits, targets, empty) is None  # 空集返回 None，不算假分数
