"""S39 stage-1 K/V source switches on the xattn backbone (CrossReadBackbone).

Plan doc: docs/research/S39_STAGED_MATRIX_PLAN_20260817_CN.md §4 -- the
taxonomy 2x2 lands as two config switches on the store rows' K/V sources:
"memory" (default) = project the pre-state memory rows (existing behavior);
"state" = project the per-chunk state readouts (content) through dedicated
d_pack -> d_backbone projections. Grid mapping:
a=(memory,memory) b=(state,memory) c=(memory,state) d=(state,state).
"""

import pytest
import torch
import torch.nn.functional as F

from flued.v36 import FLUEDV36, V36Config
from flued.v36.model import CrossReadBackbone

GRIDS = {
    "a": ("memory", "memory"),
    "b": ("state", "memory"),
    "c": ("memory", "state"),
    "d": ("state", "state"),
}


def tiny_config(**overrides):
    base = dict(
        d_byte=64,
        encoder_layers=2,
        segmentor_layers=2,
        nhead=4,
        ffn_dim=128,
        d_mem=96,
        summarizer_slots=2,
        summarizer_hidden=128,
        kda_heads=2,
        kda_head_k=16,
        kda_head_v=32,
        write_hidden=128,
        readout_queries=1,
        d_pack=64,
        d_backbone=64,
        backbone_layers=2,
        backbone_nhead=4,
        backbone_ffn=128,
        decoder_hidden=128,
        decoder_layers=2,
        max_chunks=4,
        max_span=8,
        bytes_per_chunk=8,
        max_positions=8,
        per_chunk_readout=True,
        summarizer_type="dit",
    )
    base.update(overrides)
    return V36Config(**base)


def _spy_sdpa(monkeypatch):
    """Capture the exact q/k/v handed to SDPA inside the backbone."""
    captured = {}
    real = F.scaled_dot_product_attention

    def spy(q, k, v, attn_mask=None, **kw):
        captured["q"], captured["k"], captured["v"] = q, k, v
        return real(q, k, v, attn_mask=attn_mask, **kw)

    monkeypatch.setattr(F, "scaled_dot_product_attention", spy)
    return captured


def _heads(m, cfg):
    return m.nhead, cfg.d_backbone // m.nhead


@pytest.mark.parametrize("grid", sorted(GRIDS))
def test_kv_source_switch_legacy_path(grid, monkeypatch):
    """Legacy s31 path (no cache_idx/gist): the K/V fed to SDPA must be the
    selected side's projection of the selected source rows -- content for
    "state", memory for "memory"."""
    k_src, v_src = GRIDS[grid]
    torch.manual_seed(0)
    cfg = tiny_config(k_row_source=k_src, v_row_source=v_src)
    m = CrossReadBackbone(cfg).eval()
    bsz, n = 2, 5
    content = torch.randn(bsz, n, cfg.d_pack)
    memory = torch.randn(bsz, n, cfg.d_mem)
    mask = torch.ones(bsz, n, dtype=torch.bool)
    mask[1, 4:] = False
    pos = torch.randn(1, n, cfg.d_backbone)
    captured = _spy_sdpa(monkeypatch)
    with torch.no_grad():
        out = m(content, memory, mask, pos)
    assert torch.isfinite(out).all()
    nh, hd = _heads(m, cfg)
    k_proj = m.k_proj_state if k_src == "state" else m.k_proj
    v_proj = m.v_proj_state if v_src == "state" else m.v_proj
    exp_k = k_proj(content if k_src == "state" else memory).view(bsz, n, nh, hd).transpose(1, 2)
    exp_v = v_proj(content if v_src == "state" else memory).view(bsz, n, nh, hd).transpose(1, 2)
    assert torch.allclose(captured["k"], exp_k, atol=1e-6)
    assert torch.allclose(captured["v"], exp_v, atol=1e-6)
    # non-vacuous: the wrong source would NOT match (projections differ)
    if k_src == "state":
        wrong = m.k_proj(memory).view(bsz, n, nh, hd).transpose(1, 2)
        assert not torch.allclose(captured["k"], wrong, atol=1e-3)
    if v_src == "state":
        wrong = m.v_proj(memory).view(bsz, n, nh, hd).transpose(1, 2)
        assert not torch.allclose(captured["v"], wrong, atol=1e-3)


@pytest.mark.parametrize("grid", sorted(GRIDS))
def test_kv_source_switch_store_path(grid, monkeypatch):
    """S36 store path: gist entries always go through gist_k/gist_v; the
    cache_idx-selected store rows honor the per-side source switches (gather
    source check against the module's own projections)."""
    k_src, v_src = GRIDS[grid]
    torch.manual_seed(0)
    cfg = tiny_config(xcache_gist=True, k_row_source=k_src, v_row_source=v_src)
    m = CrossReadBackbone(cfg).eval()
    bsz, n = 2, 5
    content = torch.randn(bsz, n, cfg.d_pack)
    memory = torch.randn(bsz, n, cfg.d_mem)
    mask = torch.ones(bsz, n, dtype=torch.bool)
    pos = torch.randn(1, n, cfg.d_backbone)
    gist = torch.randn(bsz, cfg.d_pack)
    cache_idx = torch.tensor([[0, 2, 3, -1, -1], [0, 2, 3, -1, -1]])
    captured = _spy_sdpa(monkeypatch)
    with torch.no_grad():
        out = m(content, memory, mask, pos, cache_idx, gist)
    assert torch.isfinite(out).all()
    nh, hd = _heads(m, cfg)
    kk = cache_idx.size(1)
    gidx = cache_idx.clamp(min=0).unsqueeze(-1)
    sel_mem = memory.gather(1, gidx.expand(-1, -1, cfg.d_mem))
    sel_state = content.gather(1, gidx.expand(-1, -1, cfg.d_pack))
    k_rows = m.k_proj_state(sel_state) if k_src == "state" else m.k_proj(sel_mem)
    v_rows = m.v_proj_state(sel_state) if v_src == "state" else m.v_proj(sel_mem)
    exp_k = torch.cat([m.gist_k(gist.unsqueeze(1)), k_rows], dim=1).view(bsz, 1 + kk, nh, hd).transpose(1, 2)
    exp_v = torch.cat([m.gist_v(gist.unsqueeze(1)), v_rows], dim=1).view(bsz, 1 + kk, nh, hd).transpose(1, 2)
    assert torch.allclose(captured["k"], exp_k, atol=1e-6)
    assert torch.allclose(captured["v"], exp_v, atol=1e-6)
    if k_src == "state":
        wrong = torch.cat([m.gist_k(gist.unsqueeze(1)), m.k_proj(sel_mem)], dim=1).view(bsz, 1 + kk, nh, hd).transpose(1, 2)
        assert not torch.allclose(captured["k"], wrong, atol=1e-3)
    if v_src == "state":
        wrong = torch.cat([m.gist_v(gist.unsqueeze(1)), m.v_proj(sel_mem)], dim=1).view(bsz, 1 + kk, nh, hd).transpose(1, 2)
        assert not torch.allclose(captured["v"], wrong, atol=1e-3)


def test_default_grid_matches_explicit_memory_memory():
    """Anti-regression red line: the default config must be point-wise
    identical to explicit (memory,memory) -- same module set (no extra
    projections), same output on the same input."""
    torch.manual_seed(0)
    ref = FLUEDV36(tiny_config(backbone_mode="xattn", xcache_gist=True))
    torch.manual_seed(0)
    twin = FLUEDV36(
        tiny_config(backbone_mode="xattn", xcache_gist=True, k_row_source="memory", v_row_source="memory")
    )
    assert set(ref.state_dict()) == set(twin.state_dict())
    assert not any("proj_state" in k for k in ref.state_dict())
    torch.manual_seed(1)
    ids = torch.randint(1, 258, (2, 32))
    with torch.no_grad():
        a = ref(ids)
        b = twin(ids)
    assert torch.equal(a.logits_backbone, b.logits_backbone)
    assert torch.equal(a.logits_direct, b.logits_direct)


def test_old_checkpoint_strict_loads_into_default():
    """A pre-switch checkpoint (no *_proj_state keys) must strict-load into
    the default (memory,memory) model; the state-grid model must surface
    exactly the new projection keys as missing."""
    torch.manual_seed(0)
    old = FLUEDV36(tiny_config(backbone_mode="xattn", xcache_gist=True))
    old_sd = old.state_dict()
    assert not any("proj_state" in k for k in old_sd)
    torch.manual_seed(1)
    new = FLUEDV36(tiny_config(backbone_mode="xattn", xcache_gist=True))
    new.load_state_dict(old_sd, strict=True)
    torch.manual_seed(2)
    st = FLUEDV36(
        tiny_config(backbone_mode="xattn", xcache_gist=True, k_row_source="state", v_row_source="state")
    )
    missing, unexpected = st.load_state_dict(old_sd, strict=False)
    assert set(missing) == {"backbone.k_proj_state.weight", "backbone.v_proj_state.weight"}
    assert not unexpected
    # K-only grid creates exactly one new projection
    torch.manual_seed(3)
    k_only = FLUEDV36(
        tiny_config(backbone_mode="xattn", xcache_gist=True, k_row_source="state")
    )
    missing, _ = k_only.load_state_dict(old_sd, strict=False)
    assert set(missing) == {"backbone.k_proj_state.weight"}


@pytest.mark.parametrize("grid", sorted(GRIDS))
def test_full_model_forward_finite_per_grid(grid):
    """Full FLUEDV36 wiring per grid (store path via xcache_gist): finite
    logits, expected shapes."""
    k_src, v_src = GRIDS[grid]
    torch.manual_seed(0)
    model = FLUEDV36(
        tiny_config(backbone_mode="xattn", xcache_gist=True, k_row_source=k_src, v_row_source=v_src)
    )
    ids = torch.randint(1, 258, (2, 32))
    with torch.no_grad():
        out = model(ids)
    assert out.logits_backbone.shape == (2, 4, 8, 258)
    assert torch.isfinite(out.logits_direct).all()
    assert torch.isfinite(out.logits_backbone).all()


def test_state_projections_receive_gradients():
    """The new projections are in the gradient path when selected."""
    torch.manual_seed(0)
    model = FLUEDV36(
        tiny_config(backbone_mode="xattn", xcache_gist=True, k_row_source="state", v_row_source="state")
    )
    model.train()
    ids = torch.randint(1, 258, (2, 32))
    out = model(ids)
    out.logits_backbone.square().mean().backward()
    params = dict(model.named_parameters())
    for name in ("backbone.k_proj_state.weight", "backbone.v_proj_state.weight"):
        p = params[name]
        assert p.grad is not None and p.grad.abs().sum() > 0, name


def test_invalid_source_raises():
    with pytest.raises(ValueError, match="k/v_row_source"):
        CrossReadBackbone(tiny_config(k_row_source="bogus"))


def test_state_source_rejected_for_paged_xattn():
    """paged_xattn content rows are page-level, not chunk-level: the state
    source is undefined there and must fail loudly, not silently misalign."""
    with pytest.raises(ValueError, match="paged_xattn"):
        CrossReadBackbone(tiny_config(backbone_mode="paged_xattn", k_row_source="state"))
