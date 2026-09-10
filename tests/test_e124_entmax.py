"""E124 仓内 α-entmax bisect 自包含单测（不依赖官方 entmax 包）。

数值对拍（与官方包输出/梯度逐项核对）是一次性验证产物，落
outputs/e124_entmax_parity/；本文件只含自持性质与解析参照：

(1) 单plex 约束：输出非负、沿 dim 和恰为 1；
(2) 精确零存在：α>1 且打分散开时低分项恰为 0.0（不是近似小）；
(3) α=2 退化为 sparsemax 闭式解（sort+cumsum 闭式，测试内独立实现）；
(4) α→1 趋近 softmax（α=1.001 松容差）；
(5) α 收到梯度（可学 α 是 E124 副仪表 A 的前提）；
(6) z 与 α 的解析梯度 vs 有限差分（fp64 中央差分）；
(7) -inf 遮蔽语义：遮蔽项精确零、余下行仍成单plex；
(8) α≤1 响亮报错（bisect 数值域外，不静默兜底）。
"""

from __future__ import annotations

import pytest
import torch

from flued.v36.sparsemap import entmax_bisect


def _sparsemax_closed(z: torch.Tensor, dim: int = -1) -> torch.Tensor:
    """sparsemax 闭式解（Martins & Astudillo 2016）：排序 + 累积和找支撑。"""
    zs, _ = z.sort(dim=dim, descending=True)
    ar = torch.arange(1, z.size(dim) + 1, device=z.device, dtype=z.dtype)
    ar = ar.view(*([1] * (z.dim() - 1)), -1)
    cum = zs.cumsum(dim=dim)
    cond = 1 + ar * zs > cum
    k = cond.to(torch.long).sum(dim=dim, keepdim=True)  # 支撑大小（≥1 恒成立）
    tau = (cum.gather(dim, k - 1) - 1) / k.to(z.dtype)
    return (z - tau).clamp(min=0)


def _rand(*shape, seed: int = 0, scale: float = 3.0, dtype=torch.float64):
    g = torch.Generator().manual_seed(seed)
    return (torch.randn(*shape, generator=g, dtype=dtype) * scale)


# --- (1) 单plex 约束 ----------------------------------------------------------


@pytest.mark.parametrize("alpha", [1.2, 1.5, 2.0, 3.0])
def test_simplex_constraints(alpha):
    z = _rand(4, 3, 17, seed=1)
    p = entmax_bisect(z, alpha)
    assert (p >= 0).all(), "负概率"
    assert torch.allclose(p.sum(dim=-1), torch.ones_like(p.sum(dim=-1)),
                          atol=1e-12), "和不为 1"
    assert p.dtype == z.dtype


def test_alpha_tensor_rowwise():
    """α 以逐行 tensor 形态广播（(B,1)），与逐行标量调用逐位一致。"""
    z = _rand(5, 11, seed=2)
    a = torch.linspace(1.3, 2.5, 5, dtype=torch.float64).unsqueeze(1)
    p = entmax_bisect(z, a)
    for i in range(5):
        pi = entmax_bisect(z[i], float(a[i, 0]))
        assert torch.equal(p[i], pi)


# --- (2) 精确零存在 ------------------------------------------------------------


def test_exact_zeros_present():
    z = _rand(8, 23, seed=3, scale=6.0)  # 大分散 → 必有低分项出支撑
    for alpha in (1.2, 1.5, 2.0):
        p = entmax_bisect(z, alpha)
        assert bool((p == 0.0).any()), f"α={alpha} 无精确零（稀疏性缺席）"
        # 支撑内严格为正
        assert bool((p[p > 0] > 0).all())


# --- (3) α=2 ↔ sparsemax 闭式解 ------------------------------------------------


def test_alpha2_matches_sparsemax_closed_form():
    z = _rand(6, 5, 19, seed=4)
    p = entmax_bisect(z, 2.0)
    ref = _sparsemax_closed(z)
    assert torch.allclose(p, ref, atol=1e-10), \
        f"max|Δ|={float((p - ref).abs().max())}"


# --- (4) α→1 趋近 softmax ------------------------------------------------------


def test_alpha_near1_approaches_softmax():
    z = _rand(4, 13, seed=5)
    p = entmax_bisect(z, 1.001)
    sm = torch.softmax(z, dim=-1)
    assert float((p - sm).abs().max()) < 5e-3


# --- (5) α 收到梯度 -------------------------------------------------------------


def test_alpha_receives_gradient():
    z = _rand(7, 9, seed=6)
    alpha = torch.tensor(1.5, dtype=torch.float64, requires_grad=True)
    p = entmax_bisect(z, alpha)
    target = torch.softmax(_rand(7, 9, seed=7), dim=-1)  # 任意稠密目标
    loss = (p * target).sum()
    loss.backward()
    assert alpha.grad is not None
    g = float(alpha.grad)
    assert g == g and g != 0.0, f"α 梯度缺失或为零: {g}"


# --- (6) 解析梯度 vs 有限差分（fp64 中央差分） -----------------------------------


def test_z_grad_matches_finite_differences():
    z = _rand(3, 15, seed=8, scale=2.0)
    alpha = 1.5
    w = _rand(3, 15, seed=9, scale=1.0)

    def f(zz):
        return float((entmax_bisect(zz, alpha) * w).sum())

    z = z.clone().requires_grad_(True)
    (entmax_bisect(z, alpha) * w).sum().backward()
    eps = 1e-6
    for i in range(3):
        for j in range(15):
            zp = z.detach().clone(); zp[i, j] += eps
            zm = z.detach().clone(); zm[i, j] -= eps
            fd = (f(zp) - f(zm)) / (2 * eps)
            assert abs(fd - float(z.grad[i, j])) < 1e-5, \
                f"z[{i},{j}] 解析 {float(z.grad[i, j])} vs FD {fd}"


def test_alpha_grad_matches_finite_differences():
    z = _rand(5, 12, seed=10, scale=2.0)
    w = _rand(5, 12, seed=11, scale=1.0)

    def f(aa):
        return float((entmax_bisect(z, aa) * w).sum())

    alpha = torch.tensor(1.5, dtype=torch.float64, requires_grad=True)
    (entmax_bisect(z, alpha) * w).sum().backward()
    eps = 1e-6
    fd = (f(1.5 + eps) - f(1.5 - eps)) / (2 * eps)
    assert abs(fd - float(alpha.grad)) < 1e-4, \
        f"α 解析 {float(alpha.grad)} vs FD {fd}"


# --- (7) -inf 遮蔽语义 ----------------------------------------------------------


def test_minus_inf_masked_entries_exact_zero():
    z = _rand(3, 10, seed=12)
    z[:, :4] = float("-inf")
    p = entmax_bisect(z, 1.5)
    assert bool((p[:, :4] == 0.0).all()), "遮蔽项非精确零"
    assert torch.allclose(p.sum(dim=-1), torch.ones(3, dtype=torch.float64),
                          atol=1e-12)


# --- (8) α≤1 响亮报错 ------------------------------------------------------------


def test_alpha_le1_loud_reject():
    z = _rand(2, 5, seed=13)
    with pytest.raises(ValueError, match="alpha > 1"):
        entmax_bisect(z, 1.0)
    with pytest.raises(ValueError, match="alpha > 1"):
        entmax_bisect(z, 0.9)
