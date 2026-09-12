"""固定查询读出 cos 逐头分解探针（tools/analysis/v3_6/probe_fixed_query_cos_perhead.py）
的最小单测。

覆盖：逐头账本与全局展平 cos 的分块拼装恒等式（随机张量 + 单头承重构造 +
逐头正交结构）、head-major 展平切片约定（防两头布局混用）、逐头 cos 对拍
直接逐头计算、微型 b 格模型链路冒烟（write_head_k → trained_states →
ridge_unmix → 固定查询读出 → 逐头账本）。
"""

from __future__ import annotations

import math

import pytest
import torch
import torch.nn.functional as F

from flued.v36 import FLUEDV36
from tests.test_v37_slm import tiny_config
from tools.analysis.v3_6.probe_fixed_query_cos_perhead import (
    assemble_global_cos,
    perhead_cos_terms,
)
from tools.analysis.v3_6.probe_oracle_write_verdict import ridge_unmix, trained_states


LAM = 1e-2


# --- 1. 分块拼装恒等式 ---------------------------------------------------------------


def _rand_pair(n=17, heads=4, hv=8, seed=0):
    torch.manual_seed(seed)
    return torch.randn(n, heads, hv), torch.randn(n, heads, hv)


def test_global_assembly_identity_on_random_pair():
    a, b = _rand_pair()
    terms = perhead_cos_terms(a, b)
    # 拼装形 == 直接展平形（同 fp64, 数值地板）
    assert terms["assembly_gap"] < 1e-9
    # 与原仪器口径（fp32 F.cosine_similarity 全展平）对拍
    ref = float(F.cosine_similarity(a.reshape(-1), b.reshape(-1), dim=0))
    assert terms["global_from_terms"] == pytest.approx(ref, abs=1e-6)


def test_per_head_cos_matches_direct_per_head():
    a, b = _rand_pair(seed=1)
    terms = perhead_cos_terms(a, b)
    for h in range(a.shape[1]):
        ref = float(F.cosine_similarity(a[:, h].reshape(-1), b[:, h].reshape(-1), dim=0))
        assert terms["per_head"]["cos"][h] == pytest.approx(ref, abs=1e-6)  # fp32 参照地板


def test_head_major_layout_convention():
    # 头 h 的列块 [h*hv:(h+1)*hv] —— collect 里 read_fixed/v̂ 共用这一布局,
    # 混用（如 hv-major）会静默错分解, 这里钉死
    n, heads, hv = 5, 3, 7
    flat = torch.cat([torch.full((n, hv), float(h)) for h in range(heads)], dim=1)
    view = flat.reshape(n, heads, hv)
    for h in range(heads):
        assert torch.equal(view[:, h], torch.full((n, hv), float(h)))


def test_single_head_load_bearer_assembly():
    # 只 h3 承重: a_h3 与 b_h3 共线, 其余头随机低相干 —— 全局 = 承重头按范数
    # 份额缩放的贡献（恒等式的判别结构: 聚合 cos 由哪头扛, 逐头账本拆得开）
    n, heads, hv = 9, 4, 6
    torch.manual_seed(2)
    b = torch.randn(n, heads, hv)
    a = torch.randn(n, heads, hv)
    a[:, 3] = b[:, 3] * 0.3  # 共线（fp32 数值内 cos≈1）
    terms = perhead_cos_terms(a, b)
    assert terms["per_head"]["cos"][3] == pytest.approx(1.0, abs=1e-6)
    # 核心分解关系: 全局 cos = Σ_h cos_h · share_h, share_h = √(an2_h·bn2_h)/(√(Σan2·Σbn2))
    # ——非负权重和为 1 → 全局是逐头 cos 的范数份额加权凸组合
    an2, bn2 = terms["per_head"]["an2"], terms["per_head"]["bn2"]
    tot = math.sqrt(sum(an2) * sum(bn2))
    recon = sum(c * math.sqrt(x * y) / tot for c, x, y in zip(terms["per_head"]["cos"], an2, bn2))
    assert terms["global_from_terms"] == pytest.approx(recon, abs=1e-9)
    cos_h_all = terms["per_head"]["cos"]
    assert min(cos_h_all) - 1e-9 <= terms["global_from_terms"] <= max(cos_h_all) + 1e-9


def test_assemble_global_cos_across_windows_matches_concat():
    # 跨窗池化拼装 == 把全部窗的展平向量连起来直接算
    parts = []
    flat_a, flat_b = [], []
    for seed in (3, 4, 5):
        a, b = _rand_pair(n=11, seed=seed)
        parts.append(perhead_cos_terms(a, b))
        flat_a.append(a.reshape(-1))
        flat_b.append(b.reshape(-1))
    pooled = assemble_global_cos(parts)
    ref = float(F.cosine_similarity(torch.cat(flat_a), torch.cat(flat_b), dim=0))
    assert pooled == pytest.approx(ref, abs=1e-7)  # fp32 参照地板


def test_perhead_terms_rejects_shape_mismatch():
    a, _ = _rand_pair(n=4)
    b, _ = _rand_pair(n=5)
    with pytest.raises(ValueError):
        perhead_cos_terms(a, b)


# --- 2. 微型 b 格模型链路冒烟 ----------------------------------------------------------


def _tiny_b_cell():
    cfg = tiny_config(k_row_source="state", v_row_source="memory")
    torch.manual_seed(0)
    return FLUEDV36(cfg).eval()


def test_tiny_b_cell_chain_perhead_shapes():
    model = _tiny_b_cell()
    c = model.config
    heads, hk, hv = c.kda_heads, c.kda_head_k, c.kda_head_v
    n, d_mem, lam = 6, c.d_mem, LAM
    gates = model.write_head_k(torch.randn(1, n, d_mem))
    states = trained_states(model.state_machine_k, gates, n)
    assert states.shape == (1, n, heads, hk, hv)
    vhat, _ = ridge_unmix(gates, states, lam)
    assert vhat.shape == (1, n, heads * hv)
    q = torch.randn(heads, hk)
    read_fixed = torch.einsum("hk,bnhkv->bnhv", q, states.float())
    terms = perhead_cos_terms(
        read_fixed[0].reshape(n, heads, hv), vhat[0].reshape(n, heads, hv)
    )
    assert len(terms["per_head"]["cos"]) == heads
    for cos_h in terms["per_head"]["cos"]:
        assert -1.0 <= cos_h <= 1.0
    assert terms["assembly_gap"] < 1e-8
