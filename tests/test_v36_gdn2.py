"""S39 stage-2 GDN2 recurrence option (erase/write gate decoupling).

recurrence="gdn2" (S39_STAGED_MATRIX_PLAN_20260817_CN appendix A): Gated
DeltaNet 2 replaces KDA's shared scalar beta with a per-K-channel erase gate b
and a per-V-channel write gate w; the decay gate (log alpha) and the delta
erase form are unchanged -- the single-variable mechanism delta. The default
recurrence="kda" must stay bit-identical to every historical arm.

CPU tests pin: gate shapes/ranges, conditional parameter creation (old
checkpoints keep loading strict-clean), the b == w == beta collapse recovering
KDA exactly (the CPU-side numerical anchor, checked against the parity-verified
KDA torch loop), streaming/final/supplementary readouts, both v3.7 interpreter
channels, and invalid-value rejection. The fla chunk_gdn2 kernel parity test
skips without CUDA+fla (same convention as test_v36_kda_lm.py).
"""

import pytest
import torch

from flued.v36 import FLUEDV36, V36Config
from flued.v36.model import KDAStateMachine, WriteHead
from tests.test_v36_smoke import tiny_config as _smoke_config

PAD_ID = 0
MASK_ID = 257


def tiny_config(**overrides):
    base = dict(per_chunk_readout=True, kda_impl="torch")
    base.update(overrides)
    return _smoke_config(**base)


def _gdn2_config(**overrides):
    base = dict(recurrence="gdn2")
    base.update(overrides)
    return tiny_config(**base)


def test_gdn2_gate_shapes_and_range():
    """WriteHead in gdn2 mode emits {k, v, b, w, alpha}: b is per K channel,
    w per V channel, both sigmoid-bounded; beta is gone."""
    torch.manual_seed(0)
    cfg = _gdn2_config()
    wh = WriteHead(cfg)
    gates = wh(torch.randn(2, 3, cfg.d_mem))
    assert set(gates) == {"k", "v", "b", "w", "alpha"}
    assert gates["b"].shape == (2, 3, cfg.kda_heads, cfg.kda_head_k)
    assert gates["w"].shape == (2, 3, cfg.kda_heads, cfg.kda_head_v)
    assert gates["k"].shape == (2, 3, cfg.kda_heads, cfg.kda_head_k)
    assert gates["v"].shape == (2, 3, cfg.kda_heads, cfg.kda_head_v)
    assert gates["alpha"].shape == (1, 1, cfg.kda_heads, cfg.kda_head_k)
    assert (gates["b"] > 0).all() and (gates["b"] < 1).all()
    assert (gates["w"] > 0).all() and (gates["w"] < 1).all()
    # -2.0 bias init, the to_beta precedent (sigmoid(-2) ~= 0.12)
    assert torch.equal(wh.to_b.bias, torch.full((cfg.kda_heads * cfg.kda_head_k,), -2.0))
    assert torch.equal(wh.to_w.bias, torch.full((cfg.kda_heads * cfg.kda_head_v,), -2.0))


def test_kda_default_path_untouched():
    """Default recurrence must be bit-identical: same state-dict keys, same
    gates keys, same forward outputs as an explicit recurrence='kda'."""
    torch.manual_seed(0)
    m_default = FLUEDV36(tiny_config())
    torch.manual_seed(0)
    m_kda = FLUEDV36(tiny_config(recurrence="kda"))
    sd1, sd2 = m_default.state_dict(), m_kda.state_dict()
    assert list(sd1) == list(sd2)
    assert all(torch.equal(sd1[k], sd2[k]) for k in sd1)
    assert "write_head.to_b.weight" not in sd1 and "write_head.to_w.weight" not in sd1
    torch.manual_seed(1)
    ids = torch.randint(1, 258, (2, 32))
    with torch.no_grad():
        o1, o2 = m_default(ids), m_kda(ids)
    assert torch.equal(o1.package, o2.package)
    assert torch.equal(o1.logits_backbone, o2.logits_backbone)
    gates = m_default.write_head(torch.randn(1, 2, m_default.config.d_mem))
    assert set(gates) == {"k", "v", "beta", "alpha"}


def test_gdn2_conditional_params_keep_old_checkpoints_strict_clean():
    """to_b/to_w exist only in gdn2 mode (the xcache_supp precedent), so a
    kda-mode state dict has exactly the historical WriteHead keys."""
    cfg_k, cfg_g = tiny_config(), _gdn2_config()
    wh_k, wh_g = WriteHead(cfg_k), WriteHead(cfg_g)
    keys_k = {n for n, _ in wh_k.named_parameters()}
    assert "to_b.weight" not in keys_k and "to_w.weight" not in keys_k
    # gdn2 is a strict superset: a kda-arm checkpoint prefix-loads cleanly
    wh_g.load_state_dict(wh_k.state_dict(), strict=False)
    delta = sum(p.numel() for p in wh_g.parameters()) - sum(p.numel() for p in wh_k.parameters())
    h, hk, hv, wh = cfg_k.kda_heads, cfg_k.kda_head_k, cfg_k.kda_head_v, cfg_k.write_hidden
    assert delta == wh * (h * hk) + h * hk + wh * (h * hv) + h * hv


def test_gdn2_param_delta_canonical_dims():
    """Appendix A estimate: +1.6M per WriteHead instance at canonical dims
    (write_hidden=1024, 4 heads, hk=128, hv=256)."""
    delta = 1024 * (4 * 128) + 4 * 128 + 1024 * (4 * 256) + 4 * 256
    assert delta == 1_574_400
    cfg_k = V36Config(kda_impl="torch")
    cfg_g = V36Config(kda_impl="torch", recurrence="gdn2")
    measured = sum(p.numel() for p in WriteHead(cfg_g).parameters()) - sum(
        p.numel() for p in WriteHead(cfg_k).parameters()
    )
    assert measured == delta


def test_invalid_recurrence_raises():
    cfg = tiny_config(recurrence="mamba2")
    with pytest.raises(ValueError, match="recurrence"):
        WriteHead(cfg)
    with pytest.raises(ValueError, match="recurrence"):
        FLUEDV36(cfg)  # model-level guard covers the no-WriteHead grids too


def test_gdn2_forward_backward_reaches_new_gates():
    torch.manual_seed(0)
    model = FLUEDV36(_gdn2_config())
    model.train()
    ids = torch.randint(1, 258, (2, 32))
    out = model(ids)
    assert out.package.shape == (2, 4, 1, 64)
    assert torch.isfinite(out.package).all()
    assert torch.isfinite(out.logits_backbone).all()
    assert torch.isfinite(out.state_norm)
    loss = out.logits_direct.square().mean() + out.logits_backbone.square().mean()
    loss.backward()
    for name in ("to_b.weight", "to_w.weight", "to_b.bias", "to_w.bias"):
        p = dict(model.write_head.named_parameters())[name]
        assert p.grad is not None and p.grad.abs().sum() > 0, name


def test_gdn2_collapse_recovers_kda():
    """Single-variable self-check: with b = w = beta broadcast over channels,
    the gdn2 torch recurrence must reproduce the (fla-parity-verified) kda
    torch recurrence exactly, padded chunks included."""
    torch.manual_seed(0)
    cfg_k, cfg_g = tiny_config(), _gdn2_config()
    sm_k, sm_g = KDAStateMachine(cfg_k), KDAStateMachine(cfg_g)
    sm_g.load_state_dict(sm_k.state_dict())  # same keys: readout_query + realign
    wh = WriteHead(cfg_k)
    memory = torch.randn(2, 4, cfg_k.d_mem)
    gates = wh(memory)
    beta = gates["beta"]  # (B, C, H)
    gates_g = {
        "k": gates["k"],
        "v": gates["v"],
        "alpha": gates["alpha"],
        "b": beta.unsqueeze(-1).expand(-1, -1, -1, cfg_k.kda_head_k).contiguous(),
        "w": beta.unsqueeze(-1).expand(-1, -1, -1, cfg_k.kda_head_v).contiguous(),
    }
    chunk_mask = torch.tensor([[True, True, True, True], [True, True, False, False]])
    with torch.no_grad():
        pkg_k, sn_k = sm_k(gates, chunk_mask)
        pkg_g, sn_g = sm_g(gates_g, chunk_mask)
    assert torch.allclose(pkg_k, pkg_g, atol=1e-5)
    assert torch.allclose(sn_k, sn_g, atol=1e-6)


def test_gdn2_stream_step_matches_batched():
    """The O(C) streaming primitive must reproduce the batched per-chunk
    package column-for-column in gdn2 mode too (torch impl)."""
    torch.manual_seed(0)
    cfg = _gdn2_config()
    model = FLUEDV36(cfg)
    memory = torch.randn(2, 3, cfg.d_mem)
    gates = model.write_head(memory)
    chunk_mask = torch.ones(2, 3, dtype=torch.bool)
    sm = model.state_machine
    with torch.no_grad():
        package, _ = sm(gates, chunk_mask)
        state = sm.init_stream_state(2, memory.device)
        cols = []
        for i in range(3):
            gi = {k: (v[:, i : i + 1] if k != "alpha" else v) for k, v in gates.items()}
            pkg_i, state = sm.stream_step(gi, state)
            cols.append(pkg_i)
        streamed = torch.cat(cols, dim=1)
    assert torch.allclose(package, streamed, atol=1e-5)


def test_gdn2_read_all_final_matches_last_chunk_readout():
    """The codec-retention invariant holds in gdn2 mode: the last valid
    chunk's readout IS the final-state readout (padded steps are identity)."""
    torch.manual_seed(0)
    cfg = _gdn2_config(readout_queries=3)
    model = FLUEDV36(cfg)
    memory = torch.randn(2, 4, cfg.d_mem)
    gates = model.write_head(memory)
    chunk_mask = torch.tensor([[True, True, True, True], [True, True, False, False]])
    with torch.no_grad():
        package, state_norm = model.state_machine(gates, chunk_mask)
        final_pkg, final_norm = model.state_machine.read_all_final(gates, chunk_mask)
    assert final_pkg.shape == (2, 3, cfg.d_pack)
    last = chunk_mask.long().sum(dim=1) - 1
    assert torch.allclose(final_pkg, package[torch.arange(2), last], atol=1e-5)
    assert torch.allclose(final_norm, state_norm, atol=1e-5)


def test_gdn2_supplementary_and_residual_readouts():
    """S38/S38B extra readouts run the gdn2 recurrence too (fla call sites 1-2);
    gradients must reach both new gates through both paths."""
    torch.manual_seed(0)
    cfg = _gdn2_config(xcache_supp=2)
    model = FLUEDV36(cfg)
    sm = model.state_machine
    memory = torch.randn(2, 3, cfg.d_mem)
    gates = model.write_head(memory)
    chunk_mask = torch.tensor([[True, True, True], [True, False, False]])
    content = torch.randn(2, 3, cfg.d_pack)
    write_w = torch.rand(2, 3)
    supp = sm.read_supplementary(content, gates, chunk_mask)
    res = sm.read_residual(content, gates, chunk_mask, write_w)
    assert supp.shape == (2, 3, cfg.d_pack) and res.shape == (2, 3, cfg.d_pack)
    assert torch.isfinite(supp).all() and torch.isfinite(res).all()
    (supp.sum() + res.sum()).backward()
    for name in ("to_b.weight", "to_w.weight"):
        p = dict(model.write_head.named_parameters())[name]
        assert p.grad is not None and p.grad.abs().sum() > 0, name


def test_gdn2_slm_both_channels():
    """v3.7 interpreter: the gdn2 option applies to BOTH channel instances
    (d grid: write_head_k over the index rows, write_head over memory rows);
    the a grid creates no WriteHead at all."""
    torch.manual_seed(0)
    cfg = _gdn2_config(
        backbone_mode="slm",
        summarizer_type="dit",
        backbone_layers=3,
        k_row_source="state",
        v_row_source="state",
    )
    model = FLUEDV36(cfg)
    assert hasattr(model, "write_head_k") and hasattr(model, "write_head")
    assert model.write_head_k.recurrence == "gdn2" and model.write_head.recurrence == "gdn2"
    assert hasattr(model.write_head_k, "to_b") and hasattr(model.write_head, "to_w")
    ids = torch.randint(1, 258, (2, 32))
    out = model(ids)
    assert torch.isfinite(out.logits_backbone).all()
    assert torch.isfinite(out.state_norm)
    torch.manual_seed(0)
    cfg_a = _gdn2_config(
        backbone_mode="slm",
        summarizer_type="dit",
        backbone_layers=3,
        k_row_source="index",
        v_row_source="memory",
    )
    model_a = FLUEDV36(cfg_a)
    assert not hasattr(model_a, "write_head") and not hasattr(model_a, "write_head_k")
    with torch.no_grad():
        out_a = model_a(ids)
    assert torch.isfinite(out_a.logits_backbone).all()


def test_gdn2_fla_parity():
    """fla chunk_gdn2 vs the torch reference loop (tolerances mirror
    test_kda_fla_parity in tests/test_v36_smoke.py)."""
    if not torch.cuda.is_available():
        pytest.skip("cuda required")
    try:
        import fla.ops.gdn2  # noqa: F401
    except Exception:
        pytest.skip("fla gdn2 not installed")
    torch.manual_seed(0)
    base = FLUEDV36(_gdn2_config(kda_impl="torch")).cuda()
    twin = FLUEDV36(_gdn2_config(kda_impl="fla")).cuda()
    twin.load_state_dict(base.state_dict())
    ids = torch.randint(1, 258, (2, 32), device="cuda")
    with torch.no_grad():
        out_ref = base(ids)
        out_fla = twin(ids)
    assert torch.allclose(out_ref.package, out_fla.package, atol=5e-2, rtol=5e-2)
    assert abs(out_ref.state_norm.item() - out_fla.state_norm.item()) < 0.1
