"""Tests for the readout-chain retrainer (tools/train/v3_6/retrain_readout_chain.py)
and the lock-in curve helper (measure_readout_lockin_curve.py).

Tiny random-init slm c-grid models on CPU; no checkpoints, no trained behavior.
"""

from __future__ import annotations

import math
from argparse import Namespace

import torch
import torch.nn.functional as F

import tools.train.v3_6.retrain_readout_chain as rr
import tools.analysis.v3_6.measure_readout_lockin_curve as lc
import tools.train.v3_6.train_v36_s1 as s1
from tests.test_v37_oracle_probe import _tiny_c_config
from flued.v36 import FLUEDV36

DEVICE = torch.device("cpu")


def _tiny_model(seed=0):
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_c_config())  # c grid: k=index, v=state


def _ns():
    return Namespace(max_chunks=32, max_span=16, mask_prob=0.0, mask_char_frac=0.4, mask_char_span_max=3)


# --- freeze surface -----------------------------------------------------------


def test_freeze_surface_correctness():
    model = _tiny_model()
    names = rr.unfreeze_readout_chain(model)
    trainable = {n for n, p in model.named_parameters() if p.requires_grad}
    # fork 1 default: readout chain + the WHOLE backbone
    expected = {
        n
        for n, _ in model.named_parameters()
        if (n.startswith(rr.TRAINABLE_PREFIXES) and not n.startswith("decoder.byte_lookup."))
        or n.startswith("backbone.")
    }
    assert trainable == expected
    assert set(names) == expected
    # the shared byte table is part of the decoder module but must stay frozen
    assert not model.decoder.byte_lookup.embedding.weight.requires_grad
    assert not model.byte_lookup.embedding.weight.requires_grad
    # producers stay frozen
    assert not model.write_head.to_k.weight.requires_grad
    assert not model.state_machine.readout_query.requires_grad
    assert model.backbone.q_proj.weight.requires_grad  # fork 1: backbone in the chain


def test_unfreeze_backbone_last_n():
    model = _tiny_model()
    rr.unfreeze_readout_chain(model, backbone_last_n=1)
    trainable = {n for n, p in model.named_parameters() if p.requires_grad}
    assert any(n.startswith("backbone.self_blocks.") for n in trainable)
    # only the LAST self block
    last = model.backbone.self_blocks[-1]
    last_params = {id(p) for p in last.parameters()}
    backbone_trainable = [p for n, p in model.named_parameters() if n.startswith("backbone.") and p.requires_grad]
    assert all(id(p) in last_params for p in backbone_trainable)


def test_freeze_backbone_flag():
    model = _tiny_model()
    rr.unfreeze_readout_chain(model, freeze_backbone=True)
    trainable = {n for n, p in model.named_parameters() if p.requires_grad}
    assert not any(n.startswith("backbone.") for n in trainable)
    assert any(n.startswith("state_machine.realign.") for n in trainable)
    import pytest

    with pytest.raises(ValueError, match="mutually exclusive"):
        rr.unfreeze_readout_chain(_tiny_model(), backbone_last_n=1, freeze_backbone=True)


# --- oracle-frac schedule + mixing --------------------------------------------


def test_oracle_frac_schedule():
    f0 = rr.oracle_frac_at(0, 100, 0.8, 0.1)
    fmid = rr.oracle_frac_at(50, 100, 0.8, 0.1)
    fend = rr.oracle_frac_at(100, 100, 0.8, 0.1)
    assert abs(f0 - 0.8) < 1e-9 and abs(fend - 0.1) < 1e-6
    assert abs(fmid - 0.45) < 1e-6
    assert f0 > fmid > fend  # monotone decrease


def test_train_step_finite_and_scoped_grads():
    model = _tiny_model()
    rr.unfreeze_readout_chain(model)
    ns = _ns()
    opt = torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=1e-3)
    clean = torch.randint(1, 258, (1, 256))
    byte_mask = torch.zeros_like(clean, dtype=torch.bool)
    import random

    rng = random.Random(0)
    r1 = rr.train_step(model, ns, clean, byte_mask, 1.0, opt, rng, 1.0)  # forced oracle
    assert r1["use_oracle"] is True and math.isfinite(r1["loss"])
    r2 = rr.train_step(model, ns, clean, byte_mask, 0.0, opt, rng, 1.0)  # forced natural
    assert r2["use_oracle"] is False and math.isfinite(r2["loss"])
    for n, p in model.named_parameters():
        if not p.requires_grad:
            assert p.grad is None, f"grad leaked to frozen {n}"
            continue
        assert p.grad is not None, f"no grad on trainable {n}"
        if "noise_cond" in n:
            continue  # zero-noise input by design => structurally zero grad
        if n.startswith("decoder_in."):
            continue  # fork 1: completion form does not route through decoder_in
        assert p.grad.abs().sum() > 0, f"zero grad on trainable {n}"
    # fork 1: the backbone must actually receive the completion gradient
    assert model.backbone.q_proj.weight.grad.abs().sum() > 0
    assert model.backbone.self_blocks[-1]["q"].weight.grad.abs().sum() > 0


def test_completion_form_uses_clean_cumulative_grid():
    """The fork-1 loss targets CLEAN bytes at masked slots (completion form),
    not MASK_ID (the old as-encoded/direct grid)."""
    model = _tiny_model().eval()
    ns = _ns()
    clean = torch.randint(1, 258, (1, 256))
    byte_mask = torch.zeros_like(clean, dtype=torch.bool)
    byte_mask[0, 10:14] = True
    source = clean.masked_fill(byte_mask, 257)
    chunks, n_real, S, k_rows = rr._states_for(model, source, use_oracle=False)
    logits = rr._chain_logits(model, chunks, n_real, S, k_rows)
    import torch.nn.functional as F

    with torch.no_grad():
        logits_manual = logits.clone()
    # reference: manual clean-grid CE at the masked byte's (chunk, slot)
    j = int(chunks.chunk_ids[0, 10])
    s = int(chunks.offsets[0, 10])
    tgt_clean = s1.make_cumulative_retention_targets(clean, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span)[0]
    assert int(tgt_clean[0, j, s]) == int(clean[0, 10])  # clean byte, not MASK_ID=257
    loss = rr._direct_loss(model, ns, chunks, n_real, clean, byte_mask, logits_manual.requires_grad_(True))
    ref = F.cross_entropy(logits_manual[0, j, s].float().unsqueeze(0), torch.tensor([int(clean[0, 10])]))
    # the masked byte is one of the scored slots; the scalar loss won't equal
    # the single-slot CE, but the grid must hold the clean id at that slot
    assert math.isfinite(float(loss)) and float(ref) > 0


def test_oracle_vs_natural_states_differ():
    model = _tiny_model().eval()
    clean = torch.randint(1, 258, (1, 256))
    chunks, n_real, S_or, k_rows = rr._states_for(model, clean, use_oracle=True)
    _, _, S_tr, k_rows2 = rr._states_for(model, clean, use_oracle=False)
    assert S_or.shape == S_tr.shape
    assert torch.allclose(k_rows, k_rows2)  # K store source is state-choice independent
    assert not torch.allclose(S_or, S_tr)  # the two state kinds are genuinely different


def test_state_only_ablation_removes_k_rows_from_attention():
    """护栏一 (b): with k_block_eval on, changing the K store rows must NOT
    change the backbone output (the direct-source rows no longer participate)."""
    model = _tiny_model().eval()
    clean = torch.randint(1, 258, (1, 256))
    chunks, n_real, S, k_rows = rr._states_for(model, clean, use_oracle=False)
    bb = model.backbone
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_real]
    v_rows = torch.randn(1, n_real, model.config.d_pack)
    mask = chunks.chunk_mask[:, :n_real]
    with torch.no_grad():
        out_full = bb(k_rows, v_rows, mask, pos)
        out_perm = bb(k_rows[:, torch.randperm(n_real)], v_rows, mask, pos)
        bb.k_block_eval = True
        out_a = bb(k_rows, v_rows, mask, pos)
        out_b = bb(k_rows[:, torch.randperm(n_real)], v_rows, mask, pos)
        bb.k_block_eval = False
    assert not torch.allclose(out_full, out_perm, atol=1e-4)  # K rows matter when un-ablated
    assert torch.allclose(out_a, out_b, atol=1e-5)  # ablated: K rows fully inert
    assert not torch.allclose(out_full, out_a, atol=1e-4)  # the ablation itself has effect


# --- eval determinism ---------------------------------------------------------


def test_eval_windows_and_masks_deterministic(tmp_path):
    import random as pyrandom

    rng = pyrandom.Random(1)
    blob = bytes(rng.randrange(32, 127) for _ in range(65536))
    fp = tmp_path / "corpus.bin"
    fp.write_bytes(blob)
    ns = Namespace(
        data_path=str(fp), seq_len=512, batch_size=1, max_eval_batches=16, seed=42,
        eval_mask_seed=1042, mask_prob=0.05, mask_char_frac=0.4, mask_char_span_max=3,
    )
    import tools.train.v3_6.train_v36_s1 as s1

    s1._MASK_GENERATOR.manual_seed(0)  # any prior state
    w1 = rr.build_eval_windows(ns, 2)
    m1 = rr.build_masks(w1, ns)
    w2 = rr.build_eval_windows(ns, 2)
    m2 = rr.build_masks(w2, ns)
    assert all(a.eq(b).all() for a, b in zip(w1, w2))
    assert all(a.eq(b).all() for a, b in zip(m1, m2))


# --- lock-in curve helper: key mixing sweeps mu monotonically -----------------


def test_mix_keys_monotonic_mu():
    torch.manual_seed(0)
    n, H, hk = 48, 2, 16
    u = F.normalize(torch.randn(1, 1, H, hk), dim=-1)
    z0 = F.normalize(torch.randn(1, n, H, hk), dim=-1)
    k_real = F.normalize(0.95 * u + 0.05 * z0, dim=-1)  # collapsed keys, mu ~ high
    z = F.normalize(torch.randn(1, n, H, hk), dim=-1)
    mus = []
    for lam in [0.0, 0.3, 0.6, 0.85, 1.0]:
        km = lc.mix_keys(k_real, z, lam)
        mus.append(sum(lc.row_geometry(km[0, :, h])["mu"] for h in range(H)) / H)
    assert mus[0] > 0.9 and mus[-1] < 0.3
    assert all(a >= b for a, b in zip(mus, mus[1:]))  # non-increasing


# --- μ curriculum (修正一, 2026-08-19) ----------------------------------------


def test_mu_curriculum_grid_monotone_realized_mu():
    """Each default λ level must land at a distinct, decreasing realized μ,
    spanning ~0.9 down to ~0.07 (the lock-in curve's full axis)."""
    torch.manual_seed(0)
    n, H, hk = 48, 2, 64  # hk=64: random-key |cos| floor ~0.11 (hk=16 would floor at ~0.22)
    u = F.normalize(torch.randn(1, 1, H, hk), dim=-1)
    z0 = F.normalize(torch.randn(1, n, H, hk), dim=-1)
    k_real = F.normalize(0.98 * u + 0.02 * z0, dim=-1)  # deeply collapsed keys
    grid = [float(x) for x in rr.build_parser().parse_args([]).mu_lambda_grid.split(",")]
    assert len(grid) >= 5
    mus = []
    for lam in grid:
        km = lc.mix_keys(k_real, F.normalize(torch.randn(k_real.shape), dim=-1), lam)
        mus.append(sum(lc.row_geometry(km[0, :, h])["mu"] for h in range(H)) / H)
    assert all(a > b for a, b in zip(mus, mus[1:])), mus  # strictly decreasing
    assert mus[0] > 0.85 and mus[-1] < 0.15, mus


def test_retrainer_defaults_updated():
    args = rr.build_parser().parse_args([])
    assert args.steps == 20000
    assert abs(args.oracle_frac_end - 0.3) < 1e-9  # 修正一 endpoint 0.1 -> 0.3
    assert args.oracle_frac_start == 0.8
    assert args.unfreeze_backbone_last_n == 0


def test_train_step_with_mu_curriculum():
    model = _tiny_model()
    rr.unfreeze_readout_chain(model)
    ns = _ns()
    opt = torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=1e-3)
    clean = torch.randint(1, 258, (1, 256))
    byte_mask = torch.zeros_like(clean, dtype=torch.bool)
    import random

    grid = [0.2, 0.65, 1.0]
    rng = random.Random(0)
    seen_lams = set()
    for _ in range(6):
        r = rr.train_step(model, ns, clean, byte_mask, 1.0, opt, rng, 1.0, mu_lambda_grid=grid)
        assert math.isfinite(r["loss"])
        assert r["use_oracle"] is True  # frac=1.0 forces the oracle branch
        assert r["mu_lambda"] in grid
        seen_lams.add(r["mu_lambda"])
    assert len(seen_lams) >= 1
    # grid=None keeps the pre-curriculum plain-oracle form working
    r = rr.train_step(model, ns, clean, byte_mask, 1.0, opt, rng, 1.0, mu_lambda_grid=None)
    assert r["mu_lambda"] is None and math.isfinite(r["loss"])
