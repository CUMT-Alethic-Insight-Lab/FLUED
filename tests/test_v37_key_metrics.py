"""E80 补充 2: resident key-geometry dashboard metrics in train_v36_s1.py
(key_mu/key_mu_max/key_pr for the V channel, *_k for the K channel).

slm mode: default-on, zero placeholders for absent channels. Legacy xattn
paths never gain the keys.
"""

from __future__ import annotations

import torch

import tools.train.v3_6.train_v36_s1 as s1
from flued.v36 import FLUEDV36
from tests.test_v37_slm import _s1_args, tiny_config

DEVICE = torch.device("cpu")
KEYS_V = ("key_mu", "key_mu_max", "key_pr")
KEYS_K = ("key_mu_k", "key_mu_max_k", "key_pr_k")


def _run(grid_k, grid_v, mode="slm"):
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(backbone_mode=mode, k_row_source=grid_k, v_row_source=grid_v))
    args = _s1_args()
    batch = (torch.randint(1, 257, (1, 64)),)
    loss, metrics = s1.step_model(model, batch, args, DEVICE, train=False)
    assert torch.isfinite(loss)
    return metrics


def test_c_grid_v_channel_only():
    m = _run("index", "state")
    for k in KEYS_V:
        assert k in m and 0.0 <= float(m[k]) <= 1.0
    assert float(m["key_mu"]) > 0.0  # real measurement, not a placeholder
    for k in KEYS_K:
        assert float(m[k]) == 0.0  # c grid: no K WriteHead -> zero placeholders


def test_d_grid_both_channels():
    m = _run("state", "state")
    assert float(m["key_mu"]) > 0.0 and float(m["key_mu_k"]) > 0.0
    assert float(m["key_mu_max"]) >= float(m["key_mu"])  # max >= mean
    assert float(m["key_mu_max_k"]) >= float(m["key_mu_k"])


def test_a_grid_all_zero_placeholders():
    m = _run("index", "memory")
    for k in KEYS_V + KEYS_K:
        assert k in m and float(m[k]) == 0.0  # no WriteHead anywhere


def test_xattn_legacy_path_untouched():
    m = _run("memory", "memory", mode="xattn")
    for k in KEYS_V + KEYS_K:
        assert k not in m  # legacy metrics schema unchanged


# --- amp-regression: key metrics must not run bf16 rows through fp32
#     WriteHead weights outside the autocast region (crashed the first
#     split-trunk smoke at step 1) -------------------------------------------


def test_key_metrics_survive_autocast_rows():
    """Simulate the amp regime on CPU: produce the forward under autocast
    (rows come out bf16), then build metrics OUTSIDE it."""
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(k_row_source="state", v_row_source="state"))
    args = _s1_args()
    batch = (torch.randint(1, 257, (1, 64)),)
    with torch.autocast("cpu", dtype=torch.bfloat16, enabled=True):
        out = s1._slm_forward(model, batch[0], args)
    assert out["memory"].dtype == torch.bfloat16  # the amp-regime rows
    m = s1._key_geometry_metrics(model, out, DEVICE)  # outside autocast, as in step_model
    assert all(torch.isfinite(v) for v in m.values())
    assert float(m["key_mu"]) > 0 and float(m["key_mu_k"]) > 0
