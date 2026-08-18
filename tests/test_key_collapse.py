"""Tests for the key-collapse survey (tools/analysis/v3_6/measure_key_collapse.py).

Geometry algebra only (orthogonal vs collinear extremes) + a tiny-model
measure_window smoke. No trained behavior, CPU.
"""

from __future__ import annotations

import torch

import tools.analysis.v3_6.measure_key_collapse as kc
from tests.test_v37_oracle_probe import _tiny_c_config
from flued.v36 import FLUEDV36


def test_row_geometry_orthogonal_rows():
    n, d = 16, 64
    X = torch.zeros(n, d)
    X[torch.arange(n), torch.arange(n)] = 1.0  # one-hot: exactly orthogonal
    g = kc.row_geometry(X)
    assert g["mu"] == 0.0 and g["p90"] == 0.0 and g["max"] == 0.0
    assert abs(g["gram_pr"] - n) < 1e-3  # Gram = I -> PR = n
    assert abs(g["gram_pr_frac"] - 1.0) < 1e-3


def test_row_geometry_collinear_rows():
    n, d = 16, 64
    base = torch.randn(1, d)
    X = base.repeat(n, 1) * (0.5 + torch.rand(n, 1))  # same direction, random norms
    g = kc.row_geometry(X)
    assert g["mu"] > 0.999 and g["p50"] > 0.999
    assert abs(g["gram_pr"] - 1.0) < 1e-2  # rank-1 Gram
    assert g["gram_pr_frac"] < 0.07


def test_row_geometry_random_rows_sanity():
    torch.manual_seed(0)
    g = kc.row_geometry(torch.randn(100, 128))
    # random rows in 128-d: |cos| concentrated near ~0.07-0.1, PR a large fraction of n
    assert g["mu"] < 0.15
    assert g["gram_pr_frac"] > 0.5


def test_measure_window_tiny_c_grid():
    torch.manual_seed(0)
    model = FLUEDV36(_tiny_c_config()).eval()  # c grid: k=index, v=state
    ids = torch.randint(1, 258, (1, 256))
    meas = kc.measure_window(model, ids)
    assert "v_keys" in meas and "k_keys" not in meas  # c grid: only the V channel has a WriteHead
    assert len(meas["v_keys"]) == 2  # kda_heads=2 in the tiny config
    assert meas["v_input_rows"] is meas["memory_rows"]
    for g in meas["v_keys"] + meas["index_rows"] + meas["memory_rows"]:
        assert 0.0 <= g["mu"] <= 1.0 and g["n"] == meas["n_real"]
    agg = kc._agg(meas["v_keys"])
    assert 0.0 <= agg["mu_mean"] <= 1.0 and agg["n_samples"] == 2


# --- layerwise decomposition (measure_key_collapse_layerwise.py) -------------

import torch.nn.functional as F  # noqa: E402

import tools.analysis.v3_6.measure_key_collapse_layerwise as lw  # noqa: E402


def _tiny_write_head(d_mem=96, write_hidden=128, heads=2, hk=16):
    from flued.v36.model import WriteHead
    from flued.v36 import V36Config

    c = V36Config(d_mem=d_mem, write_hidden=write_hidden, kda_heads=heads, kda_head_k=hk,
                  kda_head_v=32, backbone_mode="slm", summarizer_type="dit")
    return WriteHead(c)


def test_layerwise_extraction_matches_forward_and_norm_invariance():
    torch.manual_seed(0)
    wh = _tiny_write_head()
    rows = torch.randn(20, 96)
    out = lw.layerwise_write_head(wh, rows)  # internal assert: L5 keys == wh.forward keys
    mu = out["mu"]
    # layer keys present and ordered in the dict
    assert list(mu) == ["L0_input", "L1_layernorm", "L2_linear_preact", "L3_silu_trunk_out", "L4_to_k_pre_norm", "L5_normalized"]
    assert abs(mu["L4_to_k_pre_norm"] - mu["L5_normalized"]) < 1e-6  # asserted per window; recheck here
    assert 0.0 <= out["silu_sat_rate"] <= 1.0
    assert len(out["bias_dominance_per_head"]) == 2
    assert out["n"] == 20


def test_bias_collapse_detector_fires():
    """to_k.weight ≈ 0 + big bias => every key ≈ normalized bias => μ ≈ 1."""
    torch.manual_seed(0)
    wh = _tiny_write_head()
    with torch.no_grad():
        wh.to_k.weight.mul_(0.0)
        wh.to_k.bias.copy_(torch.randn_like(wh.to_k.bias) * 10.0)
    rows = torch.randn(30, 96)
    out = lw.layerwise_write_head(wh, rows)
    assert out["mu"]["L4_to_k_pre_norm"] > 0.999  # detector must fire
    assert min(out["bias_dominance_per_head"]) > 1e3  # bias totally dominates
    # while the trunk output geometry stays whatever it was (not collapsed by construction)
    assert out["mu"]["L3_silu_trunk_out"] < 0.9


def test_norm_invariance_of_pairwise_cos():
    torch.manual_seed(0)
    X = torch.randn(40, 32) * torch.rand(40, 1) * 10  # random scales per row
    g_raw = lw.row_geometry(X)
    g_norm = lw.row_geometry(F.normalize(X, dim=-1))
    assert abs(g_raw["mu"] - g_norm["mu"]) < 1e-6
    assert abs(g_raw["p90"] - g_norm["p90"]) < 1e-6
