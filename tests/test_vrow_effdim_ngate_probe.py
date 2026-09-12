"""容量界终审两直测探针（tools/analysis/v3_6/probe_vrow_effdim_ngate.py）的最小单测。

覆盖：通道选路（d→v / b→k / 双 state 默认 v / 覆写与 N/A 响亮报错）、
能量口径 n_eff 闭式（手算 γ² 几何级数 + γ²→1 极限）、参与比谱统计
（手算 PR/top1/能量秩）、二阶矩累积器（分批==全量、中心化协方差对拍）、
γ 静态读出（微型 WriteHead）、微型 d 格模型端到端形状冒烟。
"""

from __future__ import annotations

import math

import pytest
import torch

from flued.v36 import FLUEDV36
from tests.test_v37_slm import tiny_config
from tools.analysis.v3_6.probe_vrow_effdim_ngate import (
    SecondMomentAccumulator,
    channel_module,
    gamma_init_reference,
    neff_energy,
    select_channel,
    spectrum_stats,
    writehead_gamma,
)


# --- 1. 通道选路 -------------------------------------------------------------------


class _Cfg:
    def __init__(self, k="index", v="state"):
        self.k_row_source = k
        self.v_row_source = v


def test_select_channel_d_cell_defaults_to_v():
    # d 格双 state：默认 v（对照 0.076 钉 V 通道）
    assert select_channel(_Cfg("state", "state"), None) == "v"
    assert select_channel(_Cfg("state", "state"), "k") == "k"


def test_select_channel_b_cell_is_k():
    assert select_channel(_Cfg("state", "memory"), None) == "k"


def test_select_channel_na_and_mismatch_raise():
    with pytest.raises(ValueError):
        select_channel(_Cfg("index", "memory"), None)  # a 格: 无状态机
    with pytest.raises(ValueError):
        select_channel(_Cfg("index", "memory"), "v")  # 覆写 v 但 V 通道无状态机
    with pytest.raises(ValueError):
        select_channel(_Cfg("index", "state"), "k")  # 覆写 k 但 K 通道无状态机


# --- 2. 能量口径 n_eff 闭式 ----------------------------------------------------------


def test_neff_energy_hand_computed_geometric_series():
    # n_eff = Σ_{j=0}^{n-1} γ^{2j}: γ=0.5, n=4 -> 1+0.25+0.0625+0.015625
    assert float(neff_energy(torch.tensor([0.25]), torch.tensor([4.0]))[0]) == pytest.approx(1.328125)
    # γ=0: 只有最新写入存活
    assert float(neff_energy(torch.tensor([0.0]), torch.tensor([7.0]))[0]) == pytest.approx(1.0)
    # γ²→1 极限 = n（无衰减：每条写入等权）
    assert float(neff_energy(torch.tensor([1.0 - 1e-13]), torch.tensor([9.0]))[0]) == pytest.approx(9.0)


def test_neff_energy_batch_windows_shape():
    out = neff_energy(torch.tensor([0.25, 0.5]), torch.tensor([2.0, 4.0, 8.0]))
    assert out.shape == (3, 2)
    assert float(out[0, 0]) == pytest.approx(1.25)  # 1 + 0.25
    # 单调性: n 越大 n_eff 越大; γ² 越大 n_eff 越大
    assert bool((out[2] >= out[1]).all()) and bool((out[:, 1] >= out[:, 0]).all())


def test_neff_energy_matches_direct_summation():
    g = torch.tensor([0.3, 0.9, 0.99], dtype=torch.float64)
    n = 6
    direct = torch.stack([g ** (2 * j) for j in range(n)]).sum(dim=0)
    closed = neff_energy(g**2, torch.tensor([float(n)]))[0]
    assert torch.allclose(closed, direct, atol=1e-12)


# --- 3. 参与比谱统计 -----------------------------------------------------------------


def test_spectrum_stats_hand_computed():
    ev = torch.tensor([0.0, 0.0, 1.0, 9.0])  # 升序输入
    st = spectrum_stats(ev)
    assert st["dim"] == 4
    assert st["sum"] == pytest.approx(10.0)
    assert st["participation_ratio"] == pytest.approx(100.0 / 82.0)
    assert st["top1_share"] == pytest.approx(0.9)
    assert st["rank90_energy"] == 1  # 9/10 = 0.90 ≥ 0.9
    assert st["rank95_energy"] == 2  # 10/10 = 1.00 ≥ 0.95
    assert st["eigenvalues_desc"][0] == pytest.approx(9.0)


def test_spectrum_stats_flat_spectrum_pr_equals_dim():
    st = spectrum_stats(torch.ones(8))
    assert st["participation_ratio"] == pytest.approx(8.0)
    assert st["top1_share"] == pytest.approx(0.125)
    assert st["rank90_energy"] == 8


# --- 4. 二阶矩累积器 -----------------------------------------------------------------


def test_second_moment_accumulator_batched_equals_full():
    torch.manual_seed(0)
    x = torch.randn(64, 5)
    acc = SecondMomentAccumulator(5)
    acc.update(x)
    # 分批 == 全量（三批不重叠切分）
    acc2 = SecondMomentAccumulator(5)
    for chunk in x[:10], x[10:33], x[33:]:
        acc2.update(chunk)
    assert acc2.count == acc.count
    assert torch.allclose(acc2.m, acc.m, atol=1e-9)
    assert torch.allclose(acc2.mm, acc.mm, atol=1e-6)


def test_second_moment_accumulator_covariance_matches_torch_cov():
    torch.manual_seed(1)
    x = torch.randn(200, 6) * 3.0 + 1.5
    acc = SecondMomentAccumulator(6)
    acc.update(x)
    cov = acc.covariance()
    x64 = x.to(torch.float64)
    ref_cov = (x64 - x64.mean(0)).T @ (x64 - x64.mean(0)) / (x64.size(0) - 1)
    # 累积器用 1/n 归一（谱形状不受 1/n vs 1/(n-1) 影响，这里按定义对拍）
    ref_cov_n = (x64 - x64.mean(0)).T @ (x64 - x64.mean(0)) / x64.size(0)
    assert torch.allclose(cov, ref_cov_n, atol=1e-9)
    assert not torch.allclose(cov, ref_cov, atol=1e-9)  # 归一差一份 n/(n-1)，非巧合相等


# --- 5. γ 静态读出 + 微型 d 格模型冒烟 -------------------------------------------------


def _tiny_d_model():
    cfg = tiny_config(k_row_source="state", v_row_source="state")
    torch.manual_seed(0)
    return FLUEDV36(cfg).eval()


def test_writehead_gamma_is_static_sigmoid():
    model = _tiny_d_model()
    wh = channel_module(model, "v")
    g1 = writehead_gamma(wh)
    g2 = writehead_gamma(wh)
    assert torch.equal(g1, g2)  # 静态: 两次读出逐位相同
    expect = torch.sigmoid(wh.alpha_logit.detach().to(torch.float64)).reshape(-1)
    assert torch.equal(g1, expect)
    assert bool((g1 > 0).all() and (g1 < 1).all())


def test_gamma_init_reference_matches_writehead_init_formula():
    # 未训练的微型 WriteHead 的 alpha_logit 就是 init 公式产物：参照谱必须对上
    model = _tiny_d_model()
    wh = channel_module(model, "v")
    ref = gamma_init_reference(model.config.kda_heads, model.config.kda_head_k, model.config.kda_tau_max)
    assert torch.allclose(writehead_gamma(wh), ref, atol=1e-9)
    # 单调性: init 沿通道排布单调升（tau_max 天花板封顶）
    assert bool((ref[1:] >= ref[:-1] - 1e-12).all())
    # 公式端点: 最大通道 = sigmoid(log(tau_max-1)) ≈ 1 - 1/tau_max
    top = float(ref[-1])
    assert top == pytest.approx((float(model.config.kda_tau_max) - 1) / float(model.config.kda_tau_max), abs=1e-3)


def test_channel_module_and_capture_shapes_on_tiny_d_cell():
    model = _tiny_d_model()
    assert select_channel(model.config, None) == "v"
    wh = channel_module(model, "v")
    assert wh is model.write_head and wh is not model.write_head_k
    mem = torch.randn(2, 3, model.config.d_mem)
    gates = wh(mem)
    assert gates["v"].shape == (2, 3, model.config.kda_heads, model.config.kda_head_v)
    assert gates["beta"].shape == (2, 3, model.config.kda_heads)
    assert gates["alpha"].shape == (1, 1, model.config.kda_heads, model.config.kda_head_k)
