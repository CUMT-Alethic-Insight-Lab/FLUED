"""v3.7 Q18 v2 读出墙裁定臂 (任务书 2026-08-27 冻结:
docs/versions/v3.7/FLUED_V3_7_Q18_V2_READOUT_WALL_20260827_CN.md).
实现: tools/train/v3_6/train_q18_readout_wall.py.

Covers: (1) A 臂课程断言 (p≡1.0 恒定, 退火关闭) + A′ 双列 p 固定;
(2) 段1 定点查询闭式拟合 (合成 S/v̂ 恢复真查询, 形状+残差); (3) realign
挂载形状/残差断言 (段2 桥挂 L1 前 d_bridge 行 + L2 收尾, 挂载后前向 ==
闭式手算复合); (4) 零变化律响亮退出 (低于阈值/空激活 RuntimeError, 高于
阈值通过); (5) 种子流隔离 (seed 42/1/2 链重初始化两两不同 + 同种子可复现
+ 抽签流逐比特); (6) _ridge_solve 相对 λ 预条件 (α 缩比特征下仍恢复 —
Q19 D5 动机)."""

from __future__ import annotations

import pytest
import torch
import torch.nn.functional as F

from flued.v36 import FLUEDV36
from tests.test_q17_oracle_readout import _tiny_d_run_dir
from tests.test_v37_slm import tiny_config
from tools.train.v3_6 import train_q17_oracle_readout as q17
from tools.train.v3_6 import train_q18_readout_wall as q18


# --- 1. 课程断言 (任务书 §1: A 臂退火关闭 p 恒 1.0; A′ 按列固定) -----------------------


def test_course_p_arm_a_constant():
    """A 臂: 任意 step p≡1.0 (退火课程关闭, oracle 全程)。"""
    for step in (0, 1, 199, 2000, 19_999, 20_000, 39_999, 10**6):
        assert q18._q18_course_p("A", None, step) == 1.0


def test_course_p_aprime_columns():
    """A′ 臂: oracle 列 p≡1.0 / natural 列 p≡0.0, 任意 step 恒定。"""
    for step in (0, 1, 10_000, 19_999, 10**6):
        assert q18._q18_course_p("Aprime", "oracle", step) == 1.0
        assert q18._q18_course_p("Aprime", "natural", step) == 0.0
    with pytest.raises(ValueError):
        q18._q18_course_p("B", None, 0)


# --- 2. 段1 定点查询闭式拟合 (Q18-D1) ---------------------------------------------------


def test_stage1_fit_recovers_true_query():
    """合成 S (n,H,hk,hv) 与真查询 q*: v̂ = q*ᵀS → 闭式拟合逐头恢复 q*
    (cos≈1); 形状断言 (H,hk); 加噪时残差可控。"""
    torch.manual_seed(0)
    n, H, hk, hv = 64, 2, 8, 4
    S = torch.randn(n, H, hk, hv)
    q_true = torch.randn(H, hk)
    v_hat = torch.einsum("hk,nhkv->nhv", q_true, S).reshape(n, H * hv)
    q_fit = q18._q18_fit_stage1_queries(S, v_hat, lam=1e-6)
    assert q_fit.shape == (H, hk)
    for h in range(H):
        cos = float(F.cosine_similarity(q_fit[h], q_true[h], dim=0))
        assert cos > 0.999, f"head {h} cos={cos}"
    # 挂载后链输出 ≈ v̂ (段1 残差 ≈ 0)
    u = torch.einsum("hk,nhkv->nhv", q_fit, S).reshape(n, H * hv)
    assert float(F.cosine_similarity(u, v_hat, dim=-1).mean()) > 0.999
    # 形状不符响亮退出
    with pytest.raises(AssertionError):
        q18._q18_fit_stage1_queries(S, v_hat[:, :3], lam=1e-6)


def test_stage1_fit_noisy_residual():
    torch.manual_seed(1)
    n, H, hk, hv = 128, 2, 8, 4
    S = torch.randn(n, H, hk, hv)
    q_true = torch.randn(H, hk)
    v_hat = torch.einsum("hk,nhkv->nhv", q_true, S).reshape(n, H * hv)
    v_noisy = v_hat + 0.05 * torch.randn_like(v_hat)
    q_fit = q18._q18_fit_stage1_queries(S, v_noisy, lam=1e-2)
    u = torch.einsum("hk,nhkv->nhv", q_fit, S).reshape(n, H * hv)
    cos = float(F.cosine_similarity(u, v_hat, dim=-1).mean())
    assert 0.9 < cos < 1.0  # 有噪: 恢复良好但残差非零 (落盘对象)


# --- 3. realign 挂载形状/残差断言 (Q18-D2/D3) --------------------------------------------


def test_mount_stage1_requires_single_query():
    cfg = tiny_config(k_row_source="state", v_row_source="state", seed_source="k")
    model = FLUEDV36(cfg)
    sm = model.state_machine
    H, hk = cfg.kda_heads, cfg.kda_head_k
    q = torch.randn(H, hk)
    q18._q18_mount_stage1(sm, q)
    assert torch.allclose(sm.readout_query.data[0], q.to(sm.readout_query.dtype))
    # nq>1 超规格响亮退出
    if cfg.readout_queries == 1:
        sm.readout_query = torch.nn.Parameter(torch.randn(2, H, hk))
        with pytest.raises(ValueError):
            q18._q18_mount_stage1(sm, q)


def test_mount_realign_forward_matches_closed_form():
    """挂载后 realign 前向 == 闭式手算复合: LN(基座值) → L1 前 d_bridge 行 =
    W_bridge (其余置零) → SiLU → L2 = W_out。形状断言 + 残差逐位对应。"""
    torch.manual_seed(2)
    cfg = tiny_config(k_row_source="state", v_row_source="state", seed_source="k")
    model = FLUEDV36(cfg)
    sm = model.state_machine
    ln, l1, _silu, l2 = sm.realign
    d_in, d_total = l1.in_features, l1.out_features
    d_bridge = cfg.d_mem if cfg.d_mem <= d_total else d_total // 2
    n = 32
    z = torch.randn(n, d_in)
    W_bridge = torch.randn(d_in + 1, d_bridge)
    W_out = torch.randn(d_total + 1, d_total)
    q18._q18_mount_realign(sm, W_bridge, W_out)
    # L1: 前 d_bridge 行 = W_bridge.T, 其余全零
    assert torch.allclose(l1.weight.data[:d_bridge], W_bridge[:d_in].T.to(l1.weight.dtype))
    assert torch.allclose(l1.bias.data[:d_bridge], W_bridge[d_in].to(l1.bias.dtype))
    assert float(l1.weight.data[d_bridge:].abs().sum()) == 0.0
    assert float(l1.bias.data[d_bridge:].abs().sum()) == 0.0
    # L2 = W_out
    assert torch.allclose(l2.weight.data, W_out[:d_total].T.to(l2.weight.dtype))
    assert torch.allclose(l2.bias.data, W_out[d_total].to(l2.bias.dtype))
    # 挂载后前向 == _q18_chain_features 闭式复合 (逐位对应, 残差为零);
    # 注意链特征定义在 LN 后 (施工侧 z = LN(u)), 对照手算先过 LN
    out = sm.realign(z.to(next(sm.realign.parameters()).dtype))
    zn = ln(z)
    phi = q18._q18_chain_features(zn, W_bridge, d_total)
    expect = q18._q18_apply_linear(phi, W_out)
    assert torch.allclose(out.float(), expect, atol=1e-5)
    # 形状不符响亮退出
    with pytest.raises(AssertionError):
        q18._q18_mount_realign(sm, torch.randn(d_in, d_bridge), W_out)


# --- 4. 零变化律响亮退出 (任务书 §1 预注册) -----------------------------------------------


def test_zero_change_verdict_loud_exit():
    # 温启动接通: 通过并返回均值
    mean = q18._q18_zero_change_verdict([0.3, 0.2, 0.1])
    assert mean == pytest.approx(0.2)
    # 从零链同点读数 (~0.00-0.04): 响亮退出, 不许判负
    with pytest.raises(RuntimeError, match="零变化律自检失败"):
        q18._q18_zero_change_verdict([0.02, 0.04, 0.0])
    # 边界: 恰好等于阈值不过 (必须 >)
    with pytest.raises(RuntimeError):
        q18._q18_zero_change_verdict([0.15, 0.15])
    # 空激活: 无法验证 ≠ 通过
    with pytest.raises(RuntimeError, match="0 窗可读"):
        q18._q18_zero_change_verdict([])


# --- 5. 种子流隔离 (seed 42/1/2) ----------------------------------------------------------


def test_seed_stream_isolation(tmp_path):
    """seed 42/1/2: 链重初始化权重两两不同; 同种子可复现; 掩码抽签流逐比特
    同种子相同、异种子不同 (数据流隔离)。"""
    run_dir, _args = _tiny_d_run_dir(tmp_path)
    ws = []
    for sd in (42, 1, 2):
        model, _s, ns, _ = q17._q17_load_models(run_dir, torch.device("cpu"))
        q17._q17_reinit_readout_chain(model, ns, seed=sd)
        ws.append(model.state_machine.readout_query.data.clone())
    assert not torch.equal(ws[0], ws[1])
    assert not torch.equal(ws[0], ws[2])
    assert not torch.equal(ws[1], ws[2])
    # 同种子可复现
    model2, _s2, ns2, _ = q17._q17_load_models(run_dir, torch.device("cpu"))
    q17._q17_reinit_readout_chain(model2, ns2, seed=42)
    assert torch.equal(model2.state_machine.readout_query.data, ws[0])

    def draws(sd):
        g = torch.Generator().manual_seed(sd)
        return [float(torch.rand((), generator=g)) for _ in range(8)]

    assert draws(42) == draws(42)
    assert len({tuple(draws(sd)) for sd in (42, 1, 2)}) == 3


# --- 6. _ridge_solve 相对 λ 预条件 (Q19 D5 动机) ------------------------------------------


def test_ridge_solve_relative_lambda_scaling():
    """α 缩比特征 (oracle 态 ~0.003 量级): 相对预条件 ridge 的拟合质量对特征
    缩放不变 (D5 性质); 截距行在末行; 确定性 (同输入逐比特同输出)。"""
    torch.manual_seed(3)
    n, d, e = 200, 8, 3
    X0 = torch.randn(n, d)
    W_true = torch.randn(d + 1, e)
    W_true[-1] = 0  # 信号全在特征块 (否则截距恢复掩盖特征块的过正则效应)

    def rel_at(scale):
        X = X0 * scale
        Y = torch.cat([X, torch.ones(n, 1)], dim=1) @ W_true
        W = q18._ridge_solve(X, Y, lam=1e-3)
        assert W.shape == (d + 1, e)
        return float((q18._q18_apply_linear(X, W) - Y).norm() / Y.norm())

    rel1, rel2 = rel_at(1.0), rel_at(1e-3)
    assert rel1 < 5e-3 and rel2 < 5e-3, f"rel {rel1}/{rel2} — 相对预条件失效"
    # D5 动机对照: 同 λ 固定值对 α 缩比特征变相过正则 (λ 有效放大 ~1/s²)
    X = X0 * 1e-3
    Y = torch.cat([X, torch.ones(n, 1)], dim=1) @ W_true
    X1 = torch.cat([X.double(), torch.ones(n, 1, dtype=torch.float64)], dim=1)
    W_fixed = torch.linalg.solve(X1.T @ X1 + 1e-3 * torch.eye(d + 1, dtype=torch.float64), X1.T @ Y.double())
    rel_fixed = float((X1 @ W_fixed - Y.double()).norm() / Y.double().norm())
    assert rel_fixed > 0.7 and rel2 < 5e-3, f"固定 λ rel={rel_fixed} (应贴地) vs 相对 λ rel={rel2}"
    assert torch.equal(q18._ridge_solve(X, Y, lam=1e-3), q18._ridge_solve(X, Y, lam=1e-3))  # 闭式确定性
