"""v3.7 slm mode: SLMBackbone + interpreter channel routing + task grids.

Consensus doc (the architecture authority):
docs/versions/v3.7/FLUED_V3_7_ARCHITECTURE_CONSENSUS_20260817_CN.md
(user-ruled 2026-08-17). The summarizer owns the K/V interface (§1.1: the
memory row IS the standard V; a second head produces the per-chunk index =
the K side); the interpreter is an OPTIONAL per-channel KDA processor
(§1.2); the backbone is a standard small LM whose block 1 cross-reads the
precomputed store causally with self-produced Q and V-seeded positions
(§1.3); the decoder shares the backbone's V (§1.4). Grid (§3):
a=(index,memory) b=(state,memory) c=(index,state) d=(state,state);
a+pos=(index+pos,memory).
"""

from __future__ import annotations

import pytest
import torch
import torch.nn.functional as F

from flued.data import BYTE_OFFSET, MASK_ID
from flued.v36 import FLUEDV36, V36Config
from flued.v36.model import SLMBackbone, _pos_features, chunk_byte_offsets
from tools.train.v3_3.train_v33 import make_targets
from tools.train.v3_6 import train_v36_s1 as s1

GRIDS = {
    "a": ("index", "memory"),
    "b": ("state", "memory"),
    "c": ("index", "state"),
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
        backbone_layers=3,
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
        backbone_mode="slm",
        k_row_source="index",  # slm a-grid anchor (the dataclass-wide default
        v_row_source="memory",  # is the v36 "memory"; slm tests default to a)
    )
    base.update(overrides)
    return V36Config(**base)


def _s1_args(**overrides):
    from tools.train.v3_6.train_v36 import build_parser

    parser = build_parser()
    s1._add_s1_args(parser)
    args = parser.parse_args([])
    for k, v in {
        "mask_mode": "byte_span",
        "mask_prob": 0.3,
        "amp": False,
        "max_chunks": 4,
        "max_span": 8,
        **overrides,
    }.items():
        setattr(args, k, v)
    return args


def _store_rows(cfg, grid, bsz=2, n=5):
    """Fabricated store source rows with the grid's per-side widths."""
    k_src, v_src = GRIDS[grid]
    k_rows = torch.randn(bsz, n, cfg.d_pack if k_src == "state" else cfg.d_mem)
    v_rows = torch.randn(bsz, n, cfg.d_pack if v_src == "state" else cfg.d_mem)
    return k_rows, v_rows


def _spy_sdpa_all(monkeypatch):
    """Capture every (q, k, v, attn_mask) handed to SDPA."""
    calls = []
    real = F.scaled_dot_product_attention

    def spy(q, k, v, attn_mask=None, **kw):
        calls.append((q, k, v, attn_mask))
        return real(q, k, v, attn_mask=attn_mask, **kw)

    monkeypatch.setattr(F, "scaled_dot_product_attention", spy)
    return calls


# --- 1. four-grid store identity -------------------------------------------


@pytest.mark.parametrize("grid", sorted(GRIDS))
def test_slm_store_identity_per_grid(grid, monkeypatch):
    """Block-1 cross-attention K/V fed to SDPA must be exactly align_K/align_V
    of the grid's source rows; position i sees rows 0..i only (causal mask)."""
    k_src, v_src = GRIDS[grid]
    torch.manual_seed(0)
    cfg = tiny_config(k_row_source=k_src, v_row_source=v_src)
    m = SLMBackbone(cfg).eval()
    bsz, n = 2, 5
    k_rows, v_rows = _store_rows(cfg, grid, bsz, n)
    mask = torch.ones(bsz, n, dtype=torch.bool)
    mask[1, 4:] = False
    pos = torch.randn(1, n, cfg.d_backbone)
    calls = _spy_sdpa_all(monkeypatch)
    with torch.no_grad():
        out = m(k_rows, v_rows, mask, pos)
    assert torch.isfinite(out).all()
    nh, hd = m.nhead, cfg.d_backbone // m.nhead
    q, k, v, attn_mask = calls[0]  # block-1 cross-attention
    exp_k = m.align_k(k_rows).view(bsz, n, nh, hd).transpose(1, 2)
    exp_v = m.align_v(v_rows).view(bsz, n, nh, hd).transpose(1, 2)
    assert torch.allclose(k, exp_k, atol=1e-6)
    assert torch.allclose(v, exp_v, atol=1e-6)
    # causality: sample 0 (fully valid) sees exactly the lower triangle
    tri = torch.tril(torch.ones(n, n, dtype=torch.bool))
    assert torch.equal(attn_mask[0, 0], tri)
    # non-vacuous: different source rows would NOT match these projections
    wrong_k = m.align_k(torch.randn_like(k_rows)).view(bsz, n, nh, hd).transpose(1, 2)
    wrong_v = m.align_v(torch.randn_like(v_rows)).view(bsz, n, nh, hd).transpose(1, 2)
    assert not torch.allclose(k, wrong_k, atol=1e-3)
    assert not torch.allclose(v, wrong_v, atol=1e-3)


@pytest.mark.parametrize("grid", sorted(GRIDS))
def test_slm_store_identity_full_model(grid, monkeypatch):
    """Full-model wiring: block-1 store rows equal the aligned output of the
    grid's actual source (summarizer index/memory rows, or the channel state
    machine's per-chunk readouts K~/V~)."""
    k_src, v_src = GRIDS[grid]
    torch.manual_seed(0)
    cfg = tiny_config(k_row_source=k_src, v_row_source=v_src)
    model = FLUEDV36(cfg).eval()
    ids = torch.randint(1, 258, (2, 32))
    calls = _spy_sdpa_all(monkeypatch)
    with torch.no_grad():
        out = model(ids)
    n = out.chunks.chunk_mask.size(1)
    nh, hd = model.backbone.nhead, cfg.d_backbone // model.backbone.nhead
    # the first SDPA call on the chunk grid (q/k length == n_chunks) is the
    # slm block-1 cross-attention (front-end runs on the byte/span grids)
    q, k, v, _ = next(c for c in calls if c[0].size(-2) == n and c[1].size(-2) == n)
    with torch.no_grad():
        memory, index = model.summarizer.forward_with_index(
            out.chunks.span_embeddings, out.chunks.token_mask
        )
        if k_src == "state":
            package_k, _ = model.state_machine_k(model.write_head_k(index), out.chunks.chunk_mask)
            k_rows = package_k.mean(dim=2)
        else:
            k_rows = index
        if v_src == "state":
            package_v, _ = model.state_machine(model.write_head(memory), out.chunks.chunk_mask)
            v_rows = package_v.mean(dim=2)
        else:
            v_rows = memory
    exp_k = model.backbone.align_k(k_rows).view(2, n, nh, hd).transpose(1, 2)
    exp_v = model.backbone.align_v(v_rows).view(2, n, nh, hd).transpose(1, 2)
    assert torch.allclose(k, exp_k, atol=1e-5)
    assert torch.allclose(v, exp_v, atol=1e-5)
    # non-vacuous: the OTHER granularity (raw memory through align_K shape
    # permitting / raw index through align_V) must not match
    if k_src == "state":
        wrong = model.backbone.align_k(torch.randn_like(k_rows)).view(2, n, nh, hd).transpose(1, 2)
        assert not torch.allclose(k, wrong, atol=1e-3)


# --- 2. seed identity -------------------------------------------------------


def test_slm_seed_identity():
    """The initial hidden state at position i is align_V(V source row_i) + pos
    ("each chunk asks with its own V", consensus §1.3); Q is W_q of it."""
    torch.manual_seed(0)
    cfg = tiny_config(k_row_source="state", v_row_source="memory")  # b grid
    m = SLMBackbone(cfg).eval()
    bsz, n = 2, 5
    k_rows, v_rows = _store_rows(cfg, "b", bsz, n)
    mask = torch.ones(bsz, n, dtype=torch.bool)
    pos = torch.randn(1, n, cfg.d_backbone)
    captured = {}
    handle = m.q_proj.register_forward_pre_hook(lambda module, inputs: captured.update(h=inputs[0]))
    with torch.no_grad():
        m(k_rows, v_rows, mask, pos)
    handle.remove()
    exp = m.align_v(v_rows) + pos
    assert torch.allclose(captured["h"], exp, atol=1e-6)


# --- 3. direct conditioning identity ----------------------------------------


@pytest.mark.parametrize("v_src", ["memory", "state"])
def test_direct_condition_matches_decoder_aligned_v_rows(v_src):
    """direct decodes from the decoder-aligned V source rows + pos (consensus
    §1.4): fine grid == decoder_in_mem(memory)+pos, coarse == decoder_in(V~)+pos."""
    torch.manual_seed(0)
    cfg = tiny_config(k_row_source="index", v_row_source=v_src)
    model = FLUEDV36(cfg).eval()
    ids = torch.randint(1, 258, (2, 32))
    captured = []
    handle = model.decoder.register_forward_pre_hook(lambda module, inputs: captured.append(inputs[0]))
    with torch.no_grad():
        out = model(ids)
    handle.remove()
    cond_direct = captured[0]  # the decoder's first call is the direct path
    n = out.chunks.chunk_mask.size(1)
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n]
    if v_src == "memory":
        exp = model.decoder_in_mem(out.memory) + pos
    else:
        with torch.no_grad():
            package_v, _ = model.state_machine(model.write_head(out.memory), out.chunks.chunk_mask)
        exp = model.decoder_in(package_v.mean(dim=2)) + pos
    assert torch.allclose(cond_direct, exp, atol=1e-5)


# --- 4. target-grid fracture by V granularity -------------------------------


def test_coarse_direct_grid_is_cumulative_as_encoded():
    """Coarse-V direct uses the cumulative grid over the AS-ENCODED sequence:
    row i additionally restores chunks 0..i-1's masked bytes as MASK_ID."""
    values = [10, 11, 12, 20, 21, 30, 31, 32, 33]
    clean = torch.tensor([[BYTE_OFFSET + v for v in values]], dtype=torch.long)
    chunk_ids = torch.tensor([[0, 0, 0, 1, 1, 2, 2, 2, 2]])
    offsets = torch.tensor([[0, 1, 2, 0, 1, 0, 1, 2, 3]])
    byte_mask = torch.zeros_like(clean, dtype=torch.bool)
    byte_mask[0, [1, 4, 7]] = True
    source = clean.masked_fill(byte_mask, MASK_ID)
    t_dir, s_dir, m_dir, n_trunc = s1.make_cumulative_retention_targets(
        source, byte_mask, chunk_ids, offsets, 4, 8
    )
    assert int(n_trunc) == 0
    # row 1: own as-encoded bytes (t=3 -> 20, t=4 -> MASK_ID) + recalled
    # masked byte of chunk 0 (t=1, as-encoded == MASK_ID) appended at slot 2
    assert t_dir[0, 1, 0].item() == BYTE_OFFSET + 20
    assert t_dir[0, 1, 1].item() == MASK_ID
    assert t_dir[0, 1, 2].item() == MASK_ID
    assert s_dir[0, 1].sum().item() == 3
    assert m_dir[0, 1].tolist() == [False, True, True, False, False, False, False, False]


def test_grid_fracture_driven_by_v_row_source(monkeypatch):
    """step_model: in slm mode the cumulative completion/direct grids are
    driven by v_row_source (state -> cumulative, memory -> per-chunk base);
    --cumulative-mask-retention governs only the legacy xattn path."""
    recorded = []
    real_grids = s1._completion_target_grids

    def spy_grids(*a):
        recorded.append(a[-1])
        return real_grids(*a)

    cum_calls = []
    real_cum = s1.make_cumulative_retention_targets

    def spy_cum(*a):
        cum_calls.append(1)
        return real_cum(*a)

    monkeypatch.setattr(s1, "_completion_target_grids", spy_grids)
    monkeypatch.setattr(s1, "make_cumulative_retention_targets", spy_cum)
    args = _s1_args()
    batch = (torch.randint(1, 258, (2, 48)),)
    device = torch.device("cpu")
    # fine V (a grid): per-chunk base grids, no cumulative calls at all
    torch.manual_seed(0)
    fine = FLUEDV36(tiny_config())
    loss, _ = s1.step_model(fine, batch, args, device, train=False)
    assert torch.isfinite(loss)
    assert recorded == [False]
    assert len(cum_calls) == 0
    # coarse V (c grid): cumulative grids for completion AND direct
    torch.manual_seed(0)
    coarse = FLUEDV36(tiny_config(v_row_source="state"))
    loss, _ = s1.step_model(coarse, batch, args, device, train=False)
    assert torch.isfinite(loss)
    assert recorded == [False, True]
    assert len(cum_calls) == 2
    # legacy xattn: the flag still governs (regression guard)
    args_off = _s1_args(cumulative_mask_retention=False)
    torch.manual_seed(0)
    xa = FLUEDV36(tiny_config(backbone_mode="xattn", k_row_source="memory", v_row_source="memory"))
    loss, _ = s1.step_model(xa, batch, args_off, device, train=False)
    assert torch.isfinite(loss)
    assert recorded == [False, True, False]


# --- 5. a+pos arm -----------------------------------------------------------


def test_pos_inject_gate_zero_matches_a_grid_bitwise():
    """Zero-init gate: the a+pos model at step 0 is EXACTLY the a grid."""
    torch.manual_seed(0)
    ref = FLUEDV36(tiny_config())
    torch.manual_seed(1)
    pos_m = FLUEDV36(tiny_config(k_pos_inject=True))
    missing, unexpected = pos_m.load_state_dict(ref.state_dict(), strict=False)
    assert set(missing) == {"backbone.pos_proj.weight", "backbone.pos_gate"}
    assert not unexpected
    assert float(pos_m.backbone.pos_gate.detach()) == 0.0
    torch.manual_seed(2)
    ids = torch.randint(1, 258, (2, 32))
    with torch.no_grad():
        a = ref(ids)
        b = pos_m(ids)
    assert torch.equal(a.logits_backbone, b.logits_backbone)
    assert torch.equal(a.logits_direct, b.logits_direct)


def test_pos_inject_gate_moves_index_keys():
    """Gate nonzero -> the index K rows fed to SDPA shift by exactly
    gate * pos_proj(feat); gate 0 matches the plain a-grid K."""
    torch.manual_seed(0)
    cfg = tiny_config(k_pos_inject=True)
    m = SLMBackbone(cfg).eval()
    bsz, n = 2, 5
    k_rows, v_rows = _store_rows(cfg, "a", bsz, n)
    mask = torch.ones(bsz, n, dtype=torch.bool)
    pos = torch.randn(1, n, cfg.d_backbone)
    byte_off = chunk_byte_offsets(torch.ones(bsz, n, 8, dtype=torch.bool))  # 8 bytes/chunk
    ks = {}
    real = F.scaled_dot_product_attention

    def spy(q, k, v, attn_mask=None, **kw):
        ks.setdefault("first", k)  # block-1 call only
        return real(q, k, v, attn_mask=attn_mask, **kw)

    nh, hd = m.nhead, cfg.d_backbone // m.nhead
    feat = _pos_features(torch.arange(n).unsqueeze(0).expand(bsz, n), byte_off)
    with torch.no_grad():
        assert float(m.pos_gate) == 0.0
        F.scaled_dot_product_attention = spy
        try:
            m(k_rows, v_rows, mask, pos, chunk_byte_off=byte_off)
        finally:
            F.scaled_dot_product_attention = real
        base = ks["first"].clone()
        ks.clear()  # the next forward re-captures its own block-1 call
        m.pos_gate.data.fill_(0.7)
        F.scaled_dot_product_attention = spy
        try:
            m(k_rows, v_rows, mask, pos, chunk_byte_off=byte_off)
        finally:
            F.scaled_dot_product_attention = real
    exp_base = m.align_k(k_rows).view(bsz, n, nh, hd).transpose(1, 2)
    assert torch.allclose(base, exp_base, atol=1e-6)  # gate 0 == plain a-grid K
    delta = (ks["first"] - base).transpose(1, 2).reshape(bsz, n, nh * hd)
    assert torch.allclose(delta, 0.7 * m.pos_proj(feat), atol=1e-5)


def test_pos_inject_missing_offsets_raises():
    m = SLMBackbone(tiny_config(k_pos_inject=True)).eval()
    k_rows, v_rows = _store_rows(tiny_config(k_pos_inject=True), "a")
    mask = torch.ones(2, 5, dtype=torch.bool)
    pos = torch.randn(1, 5, 64)
    with pytest.raises(ValueError, match="chunk_byte_off"):
        m(k_rows, v_rows, mask, pos)


# --- 6. strict-load discipline ----------------------------------------------

SLM_NEW_PREFIXES = (
    "summarizer.index_ffn",
    "backbone.align_k",
    "backbone.align_v",
    "backbone.ln_ffn1",
    "backbone.ffn1",
    "backbone.self_blocks",
    "decoder_in_mem",
)
SLM_RETIRED_PREFIXES = ("backbone.k_proj", "backbone.v_proj", "backbone.blocks", "write_head", "state_machine")


def test_slm_loads_old_xattn_checkpoint_exact_key_accounting():
    """An old xattn (memory,memory) checkpoint loaded strict=False into the
    slm a-grid model: missing keys are exactly the new slm modules, and the
    unexpected keys are exactly the retired legacy modules.

    NOTE (spec deviation flagged for review): the S39 switch added
    projections to the SAME module, so "unexpected empty" held there; v3.7
    REPLACES the backbone (and retires the always-on content channel), so the
    retired keys surface as unexpected by construction. The discipline --
    exact, enumerable key accounting with no silent drift -- is preserved.
    """
    torch.manual_seed(0)
    old = FLUEDV36(tiny_config(backbone_mode="xattn", k_row_source="memory", v_row_source="memory"))
    old_sd = old.state_dict()
    torch.manual_seed(1)
    new = FLUEDV36(tiny_config())  # slm a grid
    missing, unexpected = new.load_state_dict(old_sd, strict=False)
    assert set(missing) == {k for k in new.state_dict() if k.startswith(SLM_NEW_PREFIXES)}
    assert "backbone.align_k.weight" in missing
    assert "summarizer.index_ffn.1.weight" in missing
    assert "decoder_in_mem.weight" in missing
    assert set(unexpected) == {k for k in old_sd if k.startswith(SLM_RETIRED_PREFIXES)}
    assert unexpected  # the swap is real, not vacuous
    assert "write_head.to_k.weight" in unexpected
    assert "state_machine.readout_query" in unexpected
    # shared-name same-shape keys load silently (front end, decoder, q/o/norm)
    assert not any(k.startswith(("byte_lookup", "encoder_blocks", "segmentor", "decoder")) for k in unexpected)
    assert "backbone.q_proj.weight" not in missing and "backbone.q_proj.weight" not in unexpected


def test_default_model_has_no_slm_keys():
    """A non-slm model's state_dict carries no slm-specific keys at all."""
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(backbone_mode="attn"))
    markers = ("align_k", "align_v", "index_ffn", "decoder_in_mem", "self_blocks", "write_head_k", "state_machine_k")
    assert not any(marker in k for k in model.state_dict() for marker in markers)


# --- 7. conditional module creation -----------------------------------------


def test_a_grid_creates_no_state_machine_d_grid_creates_two():
    """a grid: the interpreter is entirely off the chain (no WriteHead /
    KDAStateMachine instances at all); d grid: two independent pairs."""
    torch.manual_seed(0)
    a = FLUEDV36(tiny_config())
    for name in ("write_head", "state_machine", "write_head_k", "state_machine_k"):
        assert not hasattr(a, name), name
    torch.manual_seed(1)
    d = FLUEDV36(tiny_config(k_row_source="state", v_row_source="state"))
    for name in ("write_head", "state_machine", "write_head_k", "state_machine_k"):
        assert hasattr(d, name), name
    assert d.write_head is not d.write_head_k and d.state_machine is not d.state_machine_k
    # b grid: K channel only; c grid: V channel only
    torch.manual_seed(2)
    b = FLUEDV36(tiny_config(k_row_source="state"))
    assert hasattr(b, "write_head_k") and hasattr(b, "state_machine_k")
    assert not hasattr(b, "write_head") and not hasattr(b, "state_machine")
    torch.manual_seed(3)
    c = FLUEDV36(tiny_config(v_row_source="state"))
    assert hasattr(c, "write_head") and hasattr(c, "state_machine")
    assert not hasattr(c, "write_head_k") and not hasattr(c, "state_machine_k")


def test_a_grid_state_norm_placeholder_zero():
    """No state machine engaged -> the state_norm metric is a 0 placeholder."""
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    ids = torch.randint(1, 258, (2, 32))
    with torch.no_grad():
        out = model(ids)
    assert float(out.state_norm) == 0.0


# --- 8. loud rejections ------------------------------------------------------


def test_slm_rejects_memory_k_source():
    with pytest.raises(ValueError, match="k_row_source"):
        FLUEDV36(tiny_config(k_row_source="memory"))


def test_slm_rejects_index_v_source():
    with pytest.raises(ValueError, match="v_row_source"):
        FLUEDV36(tiny_config(v_row_source="index"))


def test_slm_rejects_pos_inject_on_state_k():
    with pytest.raises(ValueError, match="k_pos_inject"):
        FLUEDV36(tiny_config(k_row_source="state", k_pos_inject=True))


def test_slm_rejects_pos_inject_on_state_v():
    """a+pos is the a-grid K-side SINGLE-VARIABLE arm: (index+pos, state)
    confounds attribution and must fail loudly (main-session ruling 2026-08-17)."""
    with pytest.raises(ValueError, match="k_pos_inject"):
        FLUEDV36(tiny_config(v_row_source="state", k_pos_inject=True))


def test_slm_rejects_prefix_task():
    with pytest.raises(ValueError, match="prefix_task"):
        FLUEDV36(tiny_config(prefix_task=True))


@pytest.mark.parametrize("readout", ["final", "paged"])
def test_slm_rejects_non_per_chunk_backbone_readout(readout):
    # the paged/final readout interfaces are N/A in slm mode (the paged_xattn
    # and draft MODES are mutually exclusive backbone_mode values by
    # construction -- argparse enforces a single choice)
    with pytest.raises(ValueError, match="backbone_readout"):
        FLUEDV36(tiny_config(backbone_readout=readout))


def test_slm_rejects_slot_summarizer():
    with pytest.raises(ValueError, match="summarizer"):
        FLUEDV36(tiny_config(summarizer_type="slot"))


def test_slm_rejects_non_per_chunk_readout():
    with pytest.raises(ValueError, match="per_chunk_readout"):
        FLUEDV36(tiny_config(per_chunk_readout=False))


def test_slm_rejects_codec_final_state():
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    args = _s1_args(codec_final_state=True)
    with pytest.raises(ValueError, match="codec_final_state"):
        s1.s1_forward(model, torch.randint(1, 258, (2, 32)), args)


def test_slm_rejects_predict_decode_mode():
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    args = _s1_args(predict_mode="decode")
    batch = (torch.randint(1, 258, (2, 48)),)
    with pytest.raises(ValueError, match="predict_mode"):
        s1.step_model(model, batch, args, torch.device("cpu"), train=False)


# --- end-to-end CPU smoke ----------------------------------------------------


@pytest.mark.parametrize("grid", ["a", "d"])
def test_step_model_slm_finite_and_backprop(grid):
    """step_model end to end (fine a / coarse d): finite loss, and the new
    modules sit in the gradient path."""
    k_src, v_src = GRIDS[grid]
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(k_row_source=k_src, v_row_source=v_src))
    model.train()
    args = _s1_args()
    batch = (torch.randint(1, 258, (2, 48)),)
    loss, metrics = s1.step_model(model, batch, args, torch.device("cpu"), train=True)
    assert torch.isfinite(loss)
    for key in ("direct_acc", "backbone_acc", "backbone_masked_acc", "predict_cos"):
        assert torch.isfinite(metrics[key])
    loss.backward()
    params = dict(model.named_parameters())
    assert params["backbone.align_k.weight"].grad is not None
    assert params["backbone.align_k.weight"].grad.abs().sum() > 0
    if grid == "a":
        # fine V: direct/predict run through decoder_in_mem
        assert params["decoder_in_mem.weight"].grad is not None
        assert params["decoder_in_mem.weight"].grad.abs().sum() > 0
    else:
        # coarse V (d): decoder_in_mem is not even created (conditional-
        # creation discipline); both interpreter pairs sit in the gradient
        # path (tiny config: d_pack == d_backbone -> decoder_in is Identity)
        assert not hasattr(model, "decoder_in_mem")
        assert params["write_head_k.to_beta.bias"].grad is not None
        assert params["write_head.to_beta.bias"].grad is not None


@pytest.mark.parametrize("grid", sorted(GRIDS))
def test_full_model_forward_finite_per_grid(grid):
    """Full FLUEDV36 forward per grid: finite logits, expected shapes."""
    k_src, v_src = GRIDS[grid]
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(k_row_source=k_src, v_row_source=v_src))
    ids = torch.randint(1, 258, (2, 32))
    with torch.no_grad():
        out = model(ids)
    assert out.logits_backbone.shape == (2, 4, 8, 258)
    assert torch.isfinite(out.logits_direct).all()
    assert torch.isfinite(out.logits_backbone).all()
    assert out.package is None  # the content channel is retired in slm mode


# --- 8. K-block eval probe (user-ruled 2026-08-17) ---------------------------


def test_k_block_eval_zeroes_block1_keys(monkeypatch):
    """k_block_eval=True: block-1 SDPA keys are exactly zero (uniform
    attention) and the output equals running with zeroed k_rows -- under the
    probe the index channel carries zero information."""
    torch.manual_seed(0)
    m = SLMBackbone(tiny_config(k_block_eval=True)).eval()
    bsz, n = 2, 5
    k_rows, v_rows = _store_rows(cfg=tiny_config(), grid="a", bsz=bsz, n=n)
    mask = torch.ones(bsz, n, dtype=torch.bool)
    mask[1, 4:] = False
    pos = torch.randn(1, n, 64)
    calls = _spy_sdpa_all(monkeypatch)
    with torch.no_grad():
        out = m(k_rows, v_rows, mask, pos)
        out_zero = m(torch.zeros_like(k_rows), v_rows, mask, pos)
    assert torch.isfinite(out).all()
    _q, k, _v, _attn = calls[0]
    assert torch.count_nonzero(k) == 0
    assert torch.allclose(out, out_zero, atol=1e-6)
    # non-vacuous: probe OFF (same weights) gives a different output
    m2 = SLMBackbone(tiny_config()).eval()
    m2.load_state_dict(m.state_dict())
    with torch.no_grad():
        out_on = m2(k_rows, v_rows, mask, pos)
    assert not torch.allclose(out, out_on, atol=1e-4)
