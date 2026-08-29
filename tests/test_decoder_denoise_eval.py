"""decoder 去噪臂四列收官探针单测（探针:
tools/analysis/v3_6/probe_decoder_denoise_eval.py; 任务书 §2 判读表评测仪器,
修订 v2 s 档语义）。

Covers: (1) 噪声列合成式 ṽ=ρ·m+s·(z@Lᵀ) 的标量倍率语义与 seed 确定性;
(2) 置乱列 = 合法置换 + seed 确定性 + 行多重集保持; (3) column_rows 列构造
正确性（clean 原样 / 三档共享 z 的精确倍率关系 / m̂ == mhat_from_window 直算 /
键集与形状）; (4) 自检门逻辑（clean 贴 E68 水位 ±2pp, scrambled 地板 ≤0.10）。
Tiny 随机初始化 b 格 (k=state, v=memory) CPU 模型; 只测代数与接线, 不碰语料。
"""

from __future__ import annotations

import torch

from flued.v36 import FLUEDV36
from tools.analysis.v3_6 import probe_decoder_denoise_eval as probe
from tools.analysis.v3_6.probe_decoder_fuzz_id import mhat_from_window
from tools.analysis.v3_6.probe_oracle_write_verdict import _front_end
from tests.test_v37_oracle_probe import _tiny_c_config

D_MEM, FEAT = 96, 2 * 32 + 1  # tiny b 格 d_mem; H*hv + 截距行


def _model(seed: int = 0) -> FLUEDV36:
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_c_config(k_row_source="state", v_row_source="memory")).eval()


def _ids(seed: int = 1, t: int = 96):
    g = torch.Generator().manual_seed(seed)
    return torch.randint(1, 257, (1, t), generator=g)


def _toy_fuzz():
    g = torch.Generator().manual_seed(5)
    return {
        "W": torch.randn(FEAT, D_MEM, generator=g) * 0.02,
        "scale": 1.0,
        "chol": torch.eye(D_MEM) * 0.1,
        "rho": 0.8,
        "lam": 1.0,
        "tag": "opt",
    }


def _m(seed: int = 7, n: int = 8, d: int = 16):
    return torch.randn(n, d, generator=torch.Generator().manual_seed(seed))


# --- 1. 噪声列标量倍率语义 ----------------------------------------------------


def test_noise_rows_scalar_semantics():
    m = _m()
    chol = torch.eye(16) * 0.1
    g1 = torch.Generator().manual_seed(99)
    v05 = probe.noise_rows(m, chol, 0.8, 0.5, g1)
    g2 = torch.Generator().manual_seed(99)
    v20 = probe.noise_rows(m, chol, 0.8, 2.0, g2)
    # 同 seed → 同 z: (ṽ−ρ·m) 恰 4 倍; ρ 收缩项不乘 s (修订 v2 语义)
    assert torch.allclose(v20 - 0.8 * m, 4.0 * (v05 - 0.8 * m), atol=1e-6)
    # 同 seed 重抽逐位确定
    g3 = torch.Generator().manual_seed(99)
    assert torch.equal(probe.noise_rows(m, chol, 0.8, 0.5, g3), v05)
    assert not torch.allclose(v05, m)  # 确实扰动


# --- 2. 置乱列: 合法置换 + 确定性 ----------------------------------------------


def test_scramble_rows_permutation_deterministic():
    m = _m()
    g1 = torch.Generator().manual_seed(3)
    s1_rows, perm1 = probe.scramble_rows(m, g1)
    g2 = torch.Generator().manual_seed(3)
    s2_rows, perm2 = probe.scramble_rows(m, g2)
    assert torch.equal(perm1, perm2) and torch.equal(s1_rows, s2_rows)  # 同 seed 确定
    assert torch.equal(perm1.sort().values, torch.arange(8))  # 合法置换
    assert torch.equal(s1_rows.sort(dim=0).values, m.sort(dim=0).values)  # 行多重集保持
    assert not torch.equal(perm1, torch.arange(8))  # 该 seed 下非恒等
    g3 = torch.Generator().manual_seed(4)
    _, perm3 = probe.scramble_rows(m, g3)
    assert not torch.equal(perm1, perm3)  # 异 seed 异序


# --- 3. column_rows 列构造正确性 (tiny b 格整机) -------------------------------


def test_column_rows_construction():
    model, ids = _model(), _ids()
    chunks, memory, index = _front_end(model, ids)
    real = chunks.chunk_mask
    n_real = int(real[0].sum())
    m = memory[0, :n_real].float()
    fuzz = _toy_fuzz()
    cols = probe.column_rows(
        model, m, index, real, fuzz,
        torch.Generator().manual_seed(11), torch.Generator().manual_seed(13),
    )
    assert set(cols) == {"clean", "noise_s0.5", "noise_s1", "noise_s2", "mhat", "scrambled"}
    for name, rows in cols.items():
        assert rows.shape == (n_real, D_MEM), (name, rows.shape)
    assert cols["clean"] is m  # 干净行原样 (不复制不扰动)
    # 三档共享同一 z (M2): 残差恰为标量倍率关系
    eps = {s: cols[f"noise_s{s:g}"] - fuzz["rho"] * m for s in (0.5, 1.0, 2.0)}
    assert torch.allclose(eps[1.0], 2.0 * eps[0.5], atol=1e-6)
    assert torch.allclose(eps[2.0], 4.0 * eps[0.5], atol=1e-6)
    # m̂ 列 == 部署桥直算 (与训练器列②同函数零域移)
    mhat_ref = mhat_from_window(model, index.float(), real, fuzz["W"], fuzz["scale"])[0]
    assert torch.allclose(cols["mhat"], mhat_ref, atol=1e-6)
    # 置乱列行多重集保持但绑定摧毁 (该 seed 下非恒等)
    assert torch.allclose(cols["scrambled"].sort(dim=0).values, m.sort(dim=0).values)
    assert not torch.equal(cols["scrambled"], m)


# --- 4. 自检门 -----------------------------------------------------------------


def test_self_check_failures():
    assert probe.self_check_failures(0.7917, 0.05) == []  # 基座预期形态: 双门过
    assert probe.self_check_failures(0.7717, 0.10) == []  # 边界值贴线过
    assert probe.self_check_failures(0.75, 0.05)  # clean 跌出水位 ±2pp → 败
    assert probe.self_check_failures(0.7917, 0.11)  # scrambled 漏地板 → 败
    assert len(probe.self_check_failures(0.60, 0.30)) == 2  # 双败报两条
