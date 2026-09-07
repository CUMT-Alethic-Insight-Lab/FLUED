"""E123 前置门仪器单测（2026-09-07，冻结任务书 §3/§7）。

Covers: (1) ParallelAttention block_mask 语义（被遮键对一切查询不可见——其它
位输出对遮位值不变）+ None 位不变； (2) DiTStyleBlock mask 线程同语义；
(3) row_swap_perm donor 规则（上游优先、c==0 走 c+2 避下游污染、小窗兜底）。
"""

from __future__ import annotations

import pytest
import torch

from flued.v34.model import DiTStyleBlock, ParallelAttention

import tools.analysis.v3_6.gate_e123_necessity_v2 as gate


@pytest.fixture(autouse=True)
def _seed():
    torch.manual_seed(0)
    yield


def _make_attn():
    return ParallelAttention(dim=16, nhead=2, use_rope=False, use_alibi=False)


def test_attn_block_mask_semantics_and_none_bitwise():
    attn = _make_attn()
    x = torch.randn(1, 5, 16)
    valid = torch.ones(1, 5, dtype=torch.bool)
    # None = 旧路径逐位不变
    with torch.no_grad():
        a = attn(x, valid)
        b = attn(x, valid, None)
    assert torch.equal(a, b)
    # 遮位 3：其它位输出对 x[3] 的值不变（键侧视野抹除的语义钉死）
    bm = torch.zeros(1, 1, 1, 5, dtype=torch.bool)
    bm[0, 0, 0, 3] = True
    x2 = x.clone()
    x2[0, 3] = torch.randn(16)
    with torch.no_grad():
        m1 = attn(x, valid, bm)
        m2 = attn(x2, valid, bm)
    assert not torch.equal(x[0, 3], x2[0, 3])  # 前提：遮位值确实不同
    for t in (0, 1, 2, 4):
        assert torch.allclose(m1[0, t], m2[0, t], atol=1e-6)
    # 遮位自身状态含残差（x[3] 本体保留——正是「内容自此只存在于状态通道」的
    # 要求：自己的表示活下去给 summarizer），注意输出对遮位值可变


def test_dit_block_mask_threading():
    blk = DiTStyleBlock(dim=16, nhead=2, ffn_dim=32, use_rope=False)
    x = torch.randn(1, 5, 16)
    valid = torch.ones(1, 5, dtype=torch.bool)
    noise = torch.zeros(1)
    with torch.no_grad():
        a = blk(x, valid, noise)
        b = blk(x, valid, noise, None)
    assert torch.equal(a, b)
    bm = torch.zeros(1, 1, 1, 5, dtype=torch.bool)
    bm[0, 0, 0, 3] = True
    x2 = x.clone()
    x2[0, 3] = torch.randn(16)
    with torch.no_grad():
        m1 = blk(x, valid, noise, bm)
        m2 = blk(x2, valid, noise, bm)
    for t in (0, 1, 2, 4):
        assert torch.allclose(m1[0, t], m2[0, t], atol=1e-6)


def test_row_swap_perm_donor_rules():
    # 上游优先
    p = gate.row_swap_perm(5, 10)
    assert p[5] == 4 and p[4] == 5
    assert all(p[i] == i for i in range(10) if i not in (4, 5))
    # c==0 → c+2（避下游 c+1 污染）
    p = gate.row_swap_perm(0, 10)
    assert p[0] == 2 and p[2] == 0
    # c==0 且窗太小 → 兜底 c+1
    p = gate.row_swap_perm(0, 2)
    assert p[0] == 1 and p[1] == 0
    # 单行窗：恒等
    assert gate.row_swap_perm(0, 1) == [0]
