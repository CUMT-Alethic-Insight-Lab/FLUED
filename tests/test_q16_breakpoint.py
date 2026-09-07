"""v3.7 Q16 相一断点定位探针链 (任务书 2026-08-25 §1 冻结;
spec: docs/versions/v3_7/FLUED_V3_7_Q16_BREAKPOINT_LOCALIZATION_20260825_CN.md).

Covers: (1) 捕获槽 last_block1_ov/last_block1_h -- 关态 None + legacy 逐位
不动; 开态形状 (B,C,d) + ov=attn@v 数值一致 + h 逐模块复算一致; (2) 分层
机械规则边界 (slot 7/8/17/18); (3) _verdict_gap 判例 (含双零禁比值、上游
<0.05 禁比值、落差/噪声带双条件); (4) _ridge_2fold_hits 合成数据 sanity
(可分时 real>>garbage); (5) _mean_ci 手算.
"""

from __future__ import annotations

import pytest
import torch

from flued.v36 import FLUEDV36
from tests.test_v37_slm import tiny_config
from tools.analysis.v3_6 import probe_breakpoint_stations as q16


def _backbone_io(cfg):
    torch.manual_seed(0)
    model = FLUEDV36(cfg)
    bb = model.backbone
    bsz, n = 2, 5
    k = torch.randn(bsz, n, cfg.d_mem)
    v = torch.randn(bsz, n, cfg.d_mem)
    cm = torch.ones(bsz, n, dtype=torch.bool)
    pos = torch.randn(1, n, cfg.d_backbone)
    return bb, k, v, cm, pos


# --- 1. 捕获槽 (任务书 §1 施工事实) ---------------------------------------------------


def test_capture_slots_off_none_and_bitwise():
    cfg = tiny_config()
    bb, k, v, cm, pos = _backbone_io(cfg)
    out1 = bb(k, v, cm, pos)
    out2 = bb(k, v, cm, pos)
    assert torch.equal(out1, out2)  # 关态逐位不动
    assert bb.last_block1_attn is None
    assert bb.last_block1_ov is None and bb.last_block1_h is None


def test_capture_slots_on_shapes_and_values():
    cfg = tiny_config()
    bb, k, v, cm, pos = _backbone_io(cfg)
    out = bb(k, v, cm, pos, need_attn=True)
    attn = bb.last_block1_attn
    ov = bb.last_block1_ov
    h = bb.last_block1_h
    bsz, n = 2, 5
    d = cfg.d_backbone
    nh = cfg.backbone_nhead
    hd = d // nh
    assert attn.shape == (bsz, nh, n, n)
    assert ov.shape == (bsz, n, d) and h.shape == (bsz, n, d)
    # ov 数值一致: ov = (attn @ v) 的 transpose/reshape (逐 op 复算)
    v_heads = bb.align_v(v).view(bsz, n, nh, hd).transpose(1, 2)
    expect_ov = torch.matmul(attn.to(v_heads.dtype), v_heads).transpose(1, 2).reshape(bsz, n, d)
    assert torch.allclose(ov, expect_ov, atol=1e-6)
    # h 数值一致: h0 = seed + pos; h = h0 + o_proj(ov); h = h + ffn1(ln(h))
    seed = bb.align_k(k) if bb.seed_source == "k" else bb.align_v(v)
    h0 = seed + pos.to(seed.dtype)
    expect_h = h0 + bb.o_proj(ov)
    expect_h = expect_h + bb.ffn1(bb.ln_ffn1(expect_h))
    assert torch.allclose(h, expect_h, atol=1e-6)
    # 开态输出与关态 allclose (Q15 need_attn 验收不被捕获槽破坏)
    out_off = bb(k, v, cm, pos)
    assert torch.allclose(out, out_off, atol=1e-5)
    assert bb.last_block1_ov is None and bb.last_block1_h is None  # 关态后清空


# --- 2. 分层机械规则边界 ---------------------------------------------------------------


def test_band_of_slot_boundaries():
    assert q16._band_of_slot(0) == "head" and q16._band_of_slot(7) == "head"
    assert q16._band_of_slot(8) == "mid" and q16._band_of_slot(17) == "mid"
    assert q16._band_of_slot(18) == "tail" and q16._band_of_slot(63) == "tail"


# --- 3. 判死口径纯函数 (含双零禁比值) ---------------------------------------------------


def test_verdict_gap_cases():
    # 落差 >50% 且后站 <0.02 -> 断点定位
    s = q16._verdict_gap(0.10, 0.01)
    assert "断点定位于该两站之间" in s
    # 上游 <0.05 -> 禁算比值 (防双零假落差)
    s = q16._verdict_gap(0.03, 0.01)
    assert "禁算比值" in s and "断在该站或上游" in s
    # 双零 -> 禁算比值 (不比值)
    s = q16._verdict_gap(0.0, 0.0)
    assert "禁算比值" in s
    # 后站 >= 0.02 -> 不满足 (即使落差够)
    s = q16._verdict_gap(0.10, 0.04)
    assert "不满足判死口径" in s
    # 落差 <= 50% -> 不满足
    s = q16._verdict_gap(0.10, 0.06)
    assert "不满足判死口径" in s
    # 边界: 落差恰好 50% 不触发 (> 严格)
    s = q16._verdict_gap(0.10, 0.05)
    assert "不满足判死口径" in s


# --- 4. 岭回归 2-fold sanity -------------------------------------------------------------


def test_ridge_2fold_separable_beats_garbage():
    torch.manual_seed(0)
    n, d, k = 300, 8, 3
    centers = torch.randn(k, d) * 5.0  #  clearly separable blobs
    y = torch.arange(n) % k
    X = centers[y] + torch.randn(n, d) * 0.1
    got = q16._ridge_2fold_hits(X, y)
    assert got is not None
    hit_r, hit_g, hit_m = got
    assert hit_r.shape == (n,) and hit_r.dtype == torch.bool
    assert float(hit_r.float().mean()) > 0.95  # real 近满分
    assert float(hit_g.float().mean()) < 0.6  # garbage 贴类别先验 (1/3 量级)
    # 逐样本 garbage 命中与 real 命中是配对同折的 (同一 fold 划分)
    # majority 基线在均衡类下 = 1/3
    assert float(hit_m.float().mean()) == pytest.approx(1 / 3, abs=0.05)


def test_ridge_2fold_too_few_samples():
    assert q16._ridge_2fold_hits(torch.randn(3, 4), torch.tensor([0, 1, 2])) is None


def test_mean_ci_manual():
    mean, ci = q16._mean_ci([0.5, 0.0, -0.5])
    assert mean == 0.0
    assert ci == pytest.approx(1.96 * 0.5 / 3**0.5, abs=1e-6)
    assert q16._mean_ci([]) == (0.0, 0.0)
    mean1, ci1 = q16._mean_ci([0.3])
    assert mean1 == 0.3 and ci1 == 0.0
