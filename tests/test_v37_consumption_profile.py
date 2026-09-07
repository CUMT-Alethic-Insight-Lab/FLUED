"""Tests for the consumption-profile probe
(tools/analysis/v3_6/measure_consumption_profile.py).

Tiny random-init slm models on CPU (b grid k=state/v=memory/seed=k and c grid
k=index/v=state/seed=v); wiring/algebra correctness only — no trained behavior.
"""

from __future__ import annotations

from argparse import Namespace

import torch

from flued.data import MASK_ID
from flued.v36 import FLUEDV36
import tools.analysis.v3_6.measure_consumption_profile as cp
import tools.train.v3_6.train_v36_s1 as s1
from tests.test_v37_oracle_probe import _tiny_c_config

DEVICE = torch.device("cpu")


def _tiny_b_model(seed=0):
    """b grid (k=state, v=memory, seed=k) — the default checkpoint's grid."""
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_c_config(k_row_source="state", v_row_source="memory", seed_source="k")).eval()


def _tiny_c_model(seed=0):
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_c_config()).eval()  # c grid: k=index, v=state, seed=v


def _inputs(model, window=256):
    ids = torch.randint(1, 258, (1, window))
    bm = torch.zeros_like(ids, dtype=torch.bool)
    ns = Namespace(max_chunks=32, max_span=16)
    return cp.chain_inputs(model, ns, ids, bm)


# --- mirror parity ------------------------------------------------------------


def test_backbone_mirror_parity_matches_production():
    """site=None must be bit-identical to SLMBackbone.forward on both grids."""
    for model in (_tiny_b_model(), _tiny_c_model()):
        chunks, k_rows, v_rows, pos, n_real, _t, _sm = _inputs(model)
        ref = model.backbone(k_rows, v_rows, chunks.chunk_mask, pos)
        mine = cp.backbone_forward_mirror(model.backbone, k_rows, v_rows, chunks.chunk_mask, pos)
        assert torch.allclose(ref, mine, atol=1e-6)


def test_chain_logits_match_slm_forward_completion():
    """The full mirrored chain (backbone mirror + decoder) must reproduce
    _slm_forward's logits_backbone exactly."""
    model = _tiny_b_model()
    ids = torch.randint(1, 258, (1, 256))
    bm = torch.zeros_like(ids, dtype=torch.bool)
    ns = Namespace(max_chunks=32, max_span=16)
    chunks, k_rows, v_rows, pos, n_real, _t, _sm = cp.chain_inputs(model, ns, ids, bm)
    mine = cp.chain_logits(model, chunks, k_rows, v_rows, pos, n_real)
    out = s1._slm_forward(model, ids.masked_fill(bm, MASK_ID), None)
    assert mine.shape == out["logits_backbone"].shape
    assert torch.allclose(mine, out["logits_backbone"], atol=1e-5)


# --- shuffle targeting ---------------------------------------------------------


def test_shuffle_targets_only_the_chosen_backbone_site():
    """Intervening at bb_self0: that site consumes exactly the chunk-permuted
    baseline tensor (padding rows untouched), upstream sites are bit-identical,
    and the logits actually move."""
    model = _tiny_b_model()
    chunks, k_rows, v_rows, pos, n_real, _t, _sm = _inputs(model)
    perm = torch.randperm(n_real, generator=torch.Generator().manual_seed(0))
    base_rec, abl_rec = {}, {}
    base_logits = cp.chain_logits(model, chunks, k_rows, v_rows, pos, n_real, record=base_rec)
    abl_logits = cp.chain_logits(model, chunks, k_rows, v_rows, pos, n_real, site="bb_self0", perm=perm, record=abl_rec)
    assert torch.equal(abl_rec["bb_self0"][:, :n_real], base_rec["bb_self0"][:, perm])
    assert torch.equal(abl_rec["bb_self0"][:, n_real:], base_rec["bb_self0"][:, n_real:])  # padding untouched
    for key in ("k_rows", "v_rows", "bb_cross1"):
        assert torch.equal(abl_rec[key], base_rec[key])  # upstream unchanged
    assert not torch.allclose(base_logits, abl_logits)  # the intervention is real


def test_shuffle_k_rows_site_reaches_seed_and_store_downstream():
    """b grid seed_source='k': permuting k_rows changes the consumed k_rows and
    everything downstream (seed = aligned k rows), while v_rows stays put."""
    model = _tiny_b_model()
    chunks, k_rows, v_rows, pos, n_real, _t, _sm = _inputs(model)
    perm = torch.randperm(n_real, generator=torch.Generator().manual_seed(0))
    base_rec, abl_rec = {}, {}
    cp.chain_logits(model, chunks, k_rows, v_rows, pos, n_real, record=base_rec)
    cp.chain_logits(model, chunks, k_rows, v_rows, pos, n_real, site="k_rows", perm=perm, record=abl_rec)
    assert torch.equal(abl_rec["k_rows"][:, :n_real], base_rec["k_rows"][:, perm])
    assert torch.equal(abl_rec["v_rows"], base_rec["v_rows"])  # the other channel untouched
    assert not torch.equal(abl_rec["bb_cross1"], base_rec["bb_cross1"])  # seed=k: downstream moves


def test_decoder_hook_targets_only_the_chosen_layer():
    """dec{j} intervention: layers before j record bit-identical inputs, the
    intervention hook itself permutes the chunk axis as constructed, logits move."""
    model = _tiny_b_model()
    chunks, k_rows, v_rows, pos, n_real, _t, _sm = _inputs(model)
    perm = torch.randperm(n_real, generator=torch.Generator().manual_seed(0))
    seen_base, seen_abl = {}, {}

    def rec_hook(tag, store):
        def hook(module, args):
            store[tag] = args[0].detach().clone()

        return hook

    handles = [b.register_forward_pre_hook(rec_hook(f"dec{j}", seen_base)) for j, b in enumerate(model.decoder.blocks)]
    base_logits = cp.chain_logits(model, chunks, k_rows, v_rows, pos, n_real)
    for h in handles:
        h.remove()
    handles = [b.register_forward_pre_hook(rec_hook(f"dec{j}", seen_abl)) for j, b in enumerate(model.decoder.blocks)]
    abl_logits = cp.chain_logits(model, chunks, k_rows, v_rows, pos, n_real, site="dec1", perm=perm)
    for h in handles:
        h.remove()
    assert torch.equal(seen_abl["dec0"], seen_base["dec0"])  # upstream layer unchanged
    assert not torch.allclose(base_logits, abl_logits)

    # the pre-hook itself: chunk-axis permutation of the unfolded (B, C, S, d)
    h = torch.randn(5, 3, 4)  # (B*C, S, d) with bsz=1, chunks=5
    p3 = torch.tensor([2, 0, 1])
    hook = cp._decoder_pre_hook(p3, 3, "shuffle", 1, 5)
    h2, _valid, _noise = hook(None, (h, None, None))
    assert torch.equal(h2[:3], h[p3])
    assert torch.equal(h2[3:], h[3:])  # rows beyond n_real untouched


def test_zero_mode_zeroes_only_real_rows():
    x = torch.randn(1, 6, 4)
    out = cp._perturb_rows(x, None, 4, "zero")
    assert out[:, :4].abs().sum() == 0
    assert torch.equal(out[:, 4:], x[:, 4:])
    import pytest

    with pytest.raises(ValueError, match="unknown intervention mode"):
        cp._perturb_rows(x, None, 4, "bogus")


# --- metrics + slot profile ----------------------------------------------------


def test_kl_and_acc_baseline_is_zero_kl():
    model = _tiny_b_model()
    chunks, k_rows, v_rows, pos, n_real, targets, slot_mask = _inputs(model)
    logits = cp.chain_logits(model, chunks, k_rows, v_rows, pos, n_real)
    kl, acc = cp.kl_and_acc(logits, logits, targets, slot_mask, n_real)
    assert abs(kl) < 1e-6 and 0.0 <= acc <= 1.0


def test_slot_profile_shape_and_diff():
    """All slots are collected (0..max_span-1); the probe returns a contiguous
    prefix of slot ids with legal values; garbage rows keep the marginals."""
    model = _tiny_b_model()
    windows = [torch.randint(1, 258, (1, 256)) for _ in range(3)]
    masks = [torch.zeros_like(w, dtype=torch.bool) for w in windows]
    xr, ys, yv, channel = cp.collect_state_channel_rows(model, windows, masks, DEVICE, garbage=False)
    xg, _, _, ch2 = cp.collect_state_channel_rows(model, windows, masks, DEVICE, garbage=True)
    assert channel == ch2 == "k"  # b grid: the k channel is state-engaged
    assert ys.size(1) == model.config.max_span  # ALL slots collected, not just 0-3
    assert xr.shape == xg.shape and xr.size(1) == model.config.d_pack
    pr = cp.byte_probe(xr, ys, yv)
    pg = cp.byte_probe(xg, ys, yv)
    assert pr and set(pr) == set(pg)
    keys = sorted(int(s) for s in pr)
    assert keys == list(range(len(keys)))  # contiguous slot prefix
    for s in pr:
        assert set(pr[s]) == {"acc", "majority", "n"}
        assert 0.0 <= pr[s]["acc"] <= 1.0 and 0.0 <= pg[s]["acc"] <= 1.0
        assert pr[s]["n"] == pg[s]["n"] >= 40
        assert -1.0 <= round(pr[s]["acc"] - pg[s]["acc"], 4) <= 1.0
    # garbage discipline: same row multiset, different chunk pairing
    assert torch.allclose(xr.sort(dim=0).values, xg.sort(dim=0).values, atol=1e-5)


def test_state_channel_selection_c_grid():
    model = _tiny_c_model()
    windows = [torch.randint(1, 258, (1, 256))]
    masks = [torch.zeros_like(windows[0], dtype=torch.bool)]
    _x, _y, _yv, channel = cp.collect_state_channel_rows(model, windows, masks, DEVICE, garbage=False)
    assert channel == "v"  # c grid: the v channel is state-engaged
