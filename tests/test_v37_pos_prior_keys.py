"""Recruitment-arm B pos_prior_keys tests (WriteHead positional-prior keys).

Spec pinned 2026-08-22 (user-ruled, prereg §2): on = write keys are FIXED
random vectors per absolute chunk position (content-independent strong
prior); values stay content-driven; default off = bit-preserved.
"""

from __future__ import annotations

import torch

from flued.v36 import V36Config
from flued.v36.model import WriteHead


def _head(on: bool, seed: int = 0, max_chunks: int = 32) -> WriteHead:
    torch.manual_seed(seed)
    c = V36Config(
        d_mem=96, write_hidden=128, kda_heads=2, kda_head_k=16, kda_head_v=32,
        backbone_mode="slm", summarizer_type="dit", pos_prior_keys=on, max_chunks=max_chunks,
    )
    return WriteHead(c)


# 1. default off: no table, bit-preserved ----------------------------------------


def test_default_off_no_table():
    wh = _head(False, seed=7)
    assert not hasattr(wh, "pos_key_table")
    assert V36Config().pos_prior_keys is False


# 2. on: keys depend ONLY on position (content-independent) ----------------------


def test_keys_are_content_independent():
    wh = _head(True, seed=3).eval()
    g = torch.Generator().manual_seed(9)
    m1 = torch.randn(2, 10, 96, generator=g)
    m2 = torch.randn(2, 10, 96, generator=g)  # different content, same shape
    k1 = wh(m1)["k"]
    k2 = wh(m2)["k"]
    assert k1.eq(k2).all()  # identical keys regardless of content
    # batch-independence: same positions -> same keys across batch elements
    assert k1[0].eq(k1[1]).all()


# 3. on: different positions get different keys -----------------------------------


def test_keys_vary_by_position():
    wh = _head(True, seed=3).eval()
    k = wh(torch.randn(1, 10, 96))["k"][0]  # (C, H, hk)
    # adjacent positions should not share a key direction (position carries identity)
    sims = (k[:-1] * k[1:]).sum(dim=-1).abs().mean()
    assert float(sims) < 0.9
    # unit norm rows
    norms = k.norm(dim=-1)
    assert torch.allclose(norms, torch.ones_like(norms), atol=1e-5)


# 4. values stay content-driven ---------------------------------------------------


def test_values_stay_content_driven():
    wh = _head(True, seed=3).eval()
    g = torch.Generator().manual_seed(9)
    m1 = torch.randn(1, 10, 96, generator=g)
    m2 = torch.randn(1, 10, 96, generator=g)
    v1 = wh(m1)["v"]
    v2 = wh(m2)["v"]
    assert not v1.eq(v2).all()


# 5. CLI plumbing -------------------------------------------------------------------


def test_cli_flag_reaches_model():
    from tools.train.v3_6.train_v36 import build_model, build_parser

    args = build_parser().parse_args(
        ["--pos-prior-keys", "--backbone-mode", "slm", "--k-row-source", "state"]
    )
    model = build_model(args)
    assert model.config.pos_prior_keys is True
    assert hasattr(model.write_head_k, "pos_key_table")
    args_off = build_parser().parse_args(["--backbone-mode", "slm", "--k-row-source", "state"])
    assert build_model(args_off).config.pos_prior_keys is False
