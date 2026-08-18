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
