"""Recruitment-arm 档 a store_block mask threading tests (SLMBackbone).

Spec pinned 2026-08-21 (user-ruled 必修一 档 a): an optional (B, n_q, n_kv)
bool mask excises store rows per query position (the only bypass needing
removal — direct path is per-chunk leak-free). None = bit-identical legacy;
the diagonal is never blocked (no fully-masked query row, no NaN).
"""

from __future__ import annotations

import torch

from flued.v36 import FLUEDV36
from tests.test_v37_oracle_probe import _tiny_c_config


def _model(seed: int = 0, **kw) -> FLUEDV36:
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_c_config(**kw)).eval()


def _ids(seed: int = 1, t: int = 96):
    g = torch.Generator().manual_seed(seed)
    return torch.randint(1, 257, (1, t), generator=g)


# 1. None = bit-identical to the legacy call ------------------------------------


def test_none_bit_identical():
    m = _model()
    ids = _ids()
    a = m(ids)
    b = m(ids, store_block=None)
    assert a.logits_backbone.eq(b.logits_backbone).all()


# 2. blocking a visible store row changes the output ----------------------------


def test_block_changes_output():
    m = _model()
    ids = _ids()
    out0 = m(ids)
    n = out0.chunks.chunk_mask.size(1)
    block = torch.zeros(1, n, n, dtype=torch.bool)
    # block store row 0 from every later query (causally visible => must matter)
    block[0, 1:, 0] = True
    out1 = m(ids, store_block=block)
    assert not out1.logits_backbone.eq(out0.logits_backbone).all()


# 3. blocking a causally-invisible row is a no-op -------------------------------


def test_block_invisible_row_is_noop():
    m = _model()
    ids = _ids()
    out0 = m(ids)
    n = out0.chunks.chunk_mask.size(1)
    block = torch.zeros(1, n, n, dtype=torch.bool)
    # block store row n-1 from query 0 (future row — never visible anyway)
    if n >= 2:
        block[0, 0, n - 1] = True
        out1 = m(ids, store_block=block)
        assert out1.logits_backbone.eq(out0.logits_backbone).all()


# 4. the diagonal is never blocked: no NaN even when everything else is ---------


def test_diagonal_never_blocked_no_nan():
    m = _model()
    ids = _ids()
    out0 = m(ids)
    n = out0.chunks.chunk_mask.size(1)
    block = torch.ones(1, n, n, dtype=torch.bool)  # block EVERYTHING
    out1 = m(ids, store_block=block)
    assert torch.isfinite(out1.logits_backbone).all()
    assert torch.isfinite(out1.logits_direct).all()
