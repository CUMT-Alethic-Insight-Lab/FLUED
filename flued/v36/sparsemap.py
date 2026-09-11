"""α-entmax（bisect 求根形态），E124 硬预算检索门的门内命中分布件。

任务书冻结 v1.0 §6 施工可行性定论①（2026-09-09）：仓内实现、零新依赖、
与官方 `entmax` 包数值对拍（对拍产物 outputs/e124_entmax_parity/；仓内测试
tests/test_e124_entmax.py 自包含，不依赖官方包）。

算法：Peters et al. 2019 "Sparse Sequence-to-Sequence Models"（α-entmax）；
α 的梯度：Correia et al. 2019（adaptively-sparse 同族）。每行求解
    p = [(α-1)(z - τ)]_+^{1/(α-1)},   Σp = 1
τ 由二分求根（括号 [max(α-1)z - 1, max(α-1)z - d^{1-α}]，单调减函数）。
α 是可学 tensor（接收梯度）；α=2 时退化为 sparsemax。α≤1 响亮报错
（α=1 的极限是 softmax，bisect 在 α→1 数值不工作，用 torch.softmax）。

行内允许 -inf 打分（遮蔽语义）：该行对应项取精确零。整行全 -inf 是调用侧
违约（未定义，返回 NaN——与官方包同行为，不静默兜底）。
"""

from __future__ import annotations

import torch
from torch.autograd import Function


class _EntmaxBisect(Function):
    @staticmethod
    def forward(ctx, z: torch.Tensor, alpha, dim: int, n_iter: int):
        if not isinstance(alpha, torch.Tensor):
            alpha = torch.tensor(float(alpha), dtype=z.dtype, device=z.device)
        else:
            alpha = alpha.to(dtype=z.dtype, device=z.device)
        if bool((alpha <= 1.0).any()):
            raise ValueError(
                f"entmax_bisect 要求 alpha > 1（α=1 的极限是 softmax，"
                f"bisect 数值不工作），实得 min(alpha)={float(alpha.min())}"
            )
        alpha_shape = list(z.shape)
        alpha_shape[dim] = 1
        a = alpha.expand(*alpha_shape)
        ctx.input_alpha_shape = tuple(alpha.shape)

        d = z.size(dim)
        x = z * (a - 1)
        xmax = x.amax(dim=dim, keepdim=True)
        tau_lo = xmax - 1.0
        tau_hi = xmax - (1.0 / d) ** (a - 1)
        dm = tau_hi - tau_lo
        p = None
        for _ in range(n_iter):
            dm = dm / 2
            tau_m = tau_lo + dm
            p = torch.clamp(x - tau_m, min=0) ** (1 / (a - 1))
            f_m = p.sum(dim=dim, keepdim=True) - 1
            tau_lo = torch.where(f_m >= 0, tau_m, tau_lo)
        p = p / p.sum(dim=dim, keepdim=True)  # ensure_sum_one
        ctx.save_for_backward(p)
        ctx.alpha = a
        ctx.dim = dim
        return p

    @staticmethod
    def backward(ctx, dY: torch.Tensor):
        (p,) = ctx.saved_tensors
        a = ctx.alpha
        dim = ctx.dim
        # dL/dz：支撑集 w = p^{2-α} 的加权去均值（Correia et al. 2019 闭式）。
        gppr = torch.where(p > 0, p ** (2 - a), torch.zeros_like(p))
        dX = dY * gppr
        q = dX.sum(dim=dim, keepdim=True) / gppr.sum(dim=dim, keepdim=True)
        dX = dX - q * gppr
        d_alpha = None
        if ctx.needs_input_grad[1]:
            S = torch.where(p > 0, p * torch.log(p), torch.zeros_like(p))
            ent = S.sum(dim=dim, keepdim=True)
            y_skew = gppr / gppr.sum(dim=dim, keepdim=True)
            da = dY * (p - y_skew) / (a - 1) ** 2 - dY * (S - y_skew * ent) / (a - 1)
            d_alpha = da.sum(dim=dim, keepdim=True)
            # α 以广播形态进 forward，梯度收拢回输入形状
            if d_alpha.shape != ctx.input_alpha_shape:
                d_alpha = d_alpha.sum_to_size(ctx.input_alpha_shape)
        return dX, d_alpha, None, None


def entmax_bisect(z: torch.Tensor, alpha=1.5, dim: int = -1, n_iter: int = 50) -> torch.Tensor:
    """α-entmax 归一化稀疏映射（softmax 的稀疏化推广），bisect 求根实现。

    z: 打分张量；alpha: 标量 float 或可广播 tensor（>1，可学、接收梯度）；
    dim: 归一化轴；n_iter: 二分迭代数（50 = 官方默认，fp32 下 24 已饱和）。
    返回与 z 同形的概率张量：非负、沿 dim 和恰为 1、低分项精确为零（α>1）。
    """
    return _EntmaxBisect.apply(z, alpha, dim, n_iter)
