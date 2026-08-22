"""fork 3 F3 summarizer_pool tests (DiTChunkSummarizer pooling forms).

Spec pinned 2026-08-22 (user-ruled, E92 position-sink evidence): mean =
bit-preserved legacy; qpool = 4 position-anchored attention queries (fixed
Gaussian bias, anti-slot-collapse); poswmean = zero-param position-weighted
mean (F3z SGPT-family control).
"""

from __future__ import annotations

import torch

from flued.v36 import FLUEDV36, V36Config
from flued.v36.model import DiTChunkSummarizer
from tests.test_v37_oracle_probe import _tiny_c_config


def _summ(pool: str, seed: int = 0) -> DiTChunkSummarizer:
    torch.manual_seed(seed)
    c = V36Config(
        d_byte=64, nhead=4, ffn_dim=128, d_mem=96, summarizer_hidden=128,
        summarizer_dit_layers=2, backbone_mode="slm", summarizer_pool=pool,
    )
    return DiTChunkSummarizer(c)


def _spans(bsz=2, chunks=3, span=12, dim=64, seed=1):
    g = torch.Generator().manual_seed(seed)
    spans = torch.randn(bsz, chunks, span, dim, generator=g)
    mask = torch.ones(bsz, chunks, span, dtype=torch.bool)
    mask[0, 1, 8:] = False  # one padded chunk
    return spans, mask


# 1. default mean: bit-preserved, no extra params --------------------------------


def test_default_mean_bit_preserved():
    a = _summ("mean", seed=7)
    b = _summ("mean", seed=7)
    spans, mask = _spans()
    assert a(spans, mask).eq(b(spans, mask)).all()
    assert not hasattr(a, "pool_queries")
    assert V36Config().summarizer_pool == "mean"


# 2. qpool: shapes, queries exist, gradient flows ---------------------------------


def test_qpool_shapes_and_gradient():
    m = _summ("qpool")
    spans, mask = _spans()
    out = m(spans, mask)
    assert out.shape == (2, 3, 96)
    assert m.pool_queries is not None and m.pool_queries.shape == (4, 64)
    out.sum().backward()
    assert m.pool_queries.grad is not None and m.pool_queries.grad.abs().sum() > 0


# 3. qpool: position anchoring differentiates the queries --------------------------


def test_qpool_anchor_bias_differentiates_queries():
    m = _summ("qpool", seed=3).eval()
    spans, mask = _spans()
    with torch.no_grad():
        pooled = m._pool(spans, mask)  # (B*C, 4*d)
    q1, q4 = pooled[:, :64], pooled[:, 3 * 64 :]
    # anchored queries must NOT collapse to the same output
    assert not torch.allclose(q1, q4, atol=1e-4)


# 4. poswmean: zero new params, later positions weigh more -------------------------


def test_poswmean_zero_params_and_direction():
    m = _summ("poswmean")
    n_posw = sum(p.numel() for n, p in m.named_parameters())
    m2 = _summ("mean")
    n_mean = sum(p.numel() for n, p in m2.named_parameters())
    assert n_posw == n_mean  # zero new parameters
    # later-position emphasis: a span with signal only at the tail beats head-only
    g = torch.Generator().manual_seed(5)
    spans = torch.zeros(1, 1, 8, 64)
    spans[0, 0, -1] = torch.randn(64, generator=g) * 3  # tail signal
    mask = torch.ones(1, 1, 8, dtype=torch.bool)
    pooled = m._pool(spans, mask)
    mean_pooled = m2._pool(spans, mask)
    assert pooled.norm() > mean_pooled.norm()


# 5. full-model: qpool changes ffn width, config plumbing --------------------------


def test_full_model_and_cli():
    from tools.train.v3_6.train_v36 import build_model, build_parser

    args = build_parser().parse_args(
        ["--summarizer-pool", "qpool", "--backbone-mode", "slm", "--k-row-source", "index"]
    )
    model = build_model(args)
    assert model.config.summarizer_pool == "qpool"
    ids = torch.randint(1, 257, (1, 64))
    out = model(ids)
    assert out.memory is not None
    args_off = build_parser().parse_args(["--backbone-mode", "slm", "--k-row-source", "index"])
    assert build_model(args_off).config.summarizer_pool == "mean"
