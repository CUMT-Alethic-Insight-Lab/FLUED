"""Tests for the v3.7 slm adaptation of the S39 archive-addressing probe
(tools/analysis/v3_6/probe_archive_addressing_v37.py).

Tiny random-init slm models on CPU — mechanism/shape/carry tests only; no
checkpoint and no trained behavior is exercised. boundary_mode="uniform" keeps
chunking deterministic (boundary learning is not what is under test).
"""

from __future__ import annotations

import math
import random
from argparse import Namespace

import pytest
import torch

from flued.v36 import FLUEDV36, V36Config
import tools.analysis.v3_6.probe_archive_addressing as base
import tools.analysis.v3_6.probe_archive_addressing_v37 as probe

DEVICE = torch.device("cpu")
WINDOW = 128
PAGES = 4
GRIDS = {"a": ("index", "memory"), "b": ("state", "memory"), "c": ("index", "state"), "d": ("state", "state")}


def _tiny_config(**overrides):
    cfg = dict(
        d_byte=64, encoder_layers=2, segmentor_layers=2, nhead=4, ffn_dim=128,
        d_mem=96, summarizer_slots=2, summarizer_hidden=128,
        kda_heads=2, kda_head_k=16, kda_head_v=32, write_hidden=128,
        readout_queries=1, d_pack=64, d_backbone=64,
        backbone_layers=3, backbone_nhead=4, backbone_ffn=128,
        decoder_hidden=128, decoder_layers=2,
        max_chunks=32, max_span=16, bytes_per_chunk=8, max_positions=64,
        per_chunk_readout=True, summarizer_type="dit", backbone_mode="slm",
        boundary_mode="uniform", kda_impl="torch",
        k_row_source="index", v_row_source="memory",
    )
    cfg.update(overrides)
    return V36Config(**cfg)


def _base_bytes(n: int, seed: int = 0) -> bytes:
    rng = random.Random(seed)
    words = [b"the", b"archive", b"record", b"of", b"notes", b"plain", b"text", b"fills", b"space"]
    out = b""
    while len(out) < n:
        out += rng.choice(words) + b" "
    return out[:n]


def _encode_grid(grid: str, seed: int = 0):
    k_src, v_src = GRIDS[grid]
    torch.manual_seed(seed)
    model = FLUEDV36(_tiny_config(k_row_source=k_src, v_row_source=v_src)).eval()
    for p in model.parameters():
        p.requires_grad_(False)
    rng = random.Random(3)
    built = probe.build_document(_base_bytes(WINDOW * PAGES), 2, rng)
    assert built is not None
    doc, entries = built
    ns = Namespace(mask_prob=0.0, mask_char_frac=0.4, mask_char_span_max=3)
    enc = probe.encode_document(model, ns, doc, entries, WINDOW, DEVICE, mask_seed=11)
    return model, enc


# --- document construction ---------------------------------------------------


def test_build_document_offsets():
    rng = random.Random(7)
    built = probe.build_document(_base_bytes(2048), 4, rng)
    assert built is not None
    doc, entries = built
    assert len(entries) == 5
    assert sum(e["needle"] for e in entries) == 1
    for e in entries:
        pre, code_b, suf = probe._entry_bytes(e["eid"], e["code"])
        assert len(e["code"]) == probe.CODE_DIGITS
        assert doc[e["lo"] : e["hi"]] == pre + code_b + suf
        assert doc[e["code_lo"] : e["code_hi"]] == code_b
    spans = sorted((e["lo"], e["hi"]) for e in entries)
    assert all(spans[i][1] <= spans[i + 1][0] for i in range(len(spans) - 1))
    assert len({e["eid"] for e in entries}) == len(entries)
    assert len({e["code"] for e in entries}) == len(entries)


def test_build_document_rejects_cramped_base():
    rng = random.Random(7)
    assert probe.build_document(_base_bytes(200), 16, rng) is None


# --- encode path -------------------------------------------------------------


@pytest.mark.parametrize("grid", sorted(GRIDS))
def test_encode_document_shapes_per_grid(grid):
    model, enc = _encode_grid(grid)
    assert enc is not None
    G = enc["g_total"]
    d_k = model.config.d_pack if grid in ("b", "d") else model.config.d_mem
    d_v = model.config.d_pack if grid in ("c", "d") else model.config.d_mem
    assert enc["k_rows"].shape == (G, d_k)
    assert enc["v_rows"].shape == (G, d_v)
    assert enc["backbone"].shape == (G, model.config.d_backbone)
    assert enc["query"].shape == (d_k,)
    assert enc["memory"] is enc["k_rows"]  # mechanical alias for the frozen train/eval loops
    assert len(enc["code_units"]) == probe.CODE_DIGITS
    assert enc["n_pages"] == PAGES
    base.prep_k_index(enc, [1], DEVICE)
    assert enc["pos_code"][1].numel() > 0
    assert enc["pos_entry"][1].numel() >= enc["pos_code"][1].numel()


def test_stream_channel_matches_batched_single_page():
    """The carried-state streaming path must reproduce the batched
    _slm_store_rows readouts within one page (fresh state, same gates)."""
    torch.manual_seed(0)
    model = FLUEDV36(_tiny_config(k_row_source="state", v_row_source="state")).eval()
    ids = torch.randint(1, 258, (1, WINDOW))
    with torch.no_grad():
        chunks, memory, index = probe._encode_window(model, ids)
        n_real = int(chunks.chunk_mask[0].sum())
        package_k, _ = model.state_machine_k(model.write_head_k(index), chunks.chunk_mask)
        ref = package_k.mean(dim=2)[:, :n_real]
        state = model.state_machine_k.init_stream_state(1, DEVICE)
        got, _ = probe._stream_channel(
            model.state_machine_k, model.write_head_k(index), memory.size(1), n_real, state
        )
    assert torch.allclose(ref, got, atol=1e-5)


def test_state_channel_actually_carries_across_pages():
    """Page-2 state rows from the carried archive encode must differ from a
    fresh-state encode of the same page (the carry is real, not decorative)."""
    torch.manual_seed(0)
    model = FLUEDV36(_tiny_config(k_row_source="state", v_row_source="state")).eval()
    ids = torch.randint(1, 258, (1, 2 * WINDOW))
    with torch.no_grad():
        state = model.state_machine_k.init_stream_state(1, DEVICE)
        carried = None
        for w in range(2):
            chunks, memory, index = probe._encode_window(model, ids[:, w * WINDOW : (w + 1) * WINDOW])
            n_real = int(chunks.chunk_mask[0].sum())
            carried, state = probe._stream_channel(
                model.state_machine_k, model.write_head_k(index), memory.size(1), n_real, state
            )
        chunks2, memory2, index2 = probe._encode_window(model, ids[:, WINDOW:])
        n2 = int(chunks2.chunk_mask[0].sum())
        fresh, _ = probe._stream_channel(
            model.state_machine_k,
            model.write_head_k(index2),
            memory2.size(1),
            n2,
            model.state_machine_k.init_stream_state(1, DEVICE),
        )
    assert carried.shape == fresh.shape
    assert not torch.allclose(carried, fresh, atol=1e-4)


# --- K side (frozen loops reused) + V side decode ----------------------------


def test_k_side_train_eval_and_v_side_decode():
    model, enc = _encode_grid("d")  # d grid exercises both state channels
    base.prep_k_index(enc, [1], DEVICE)
    args = Namespace(lr=1e-3, steps=3, batch_docs=2, log_every=1)
    cfg = {
        "key_type": "full", "rank": None, "gran": 1, "key_src": "memrow",
        "d_query": model.config.d_pack, "d_key": model.config.d_pack, "seed": 0,
    }
    retr, log = base.train_retriever(cfg, [enc], args, DEVICE, 0)
    assert len(log) >= 1
    assert all(math.isfinite(r["loss"]) for r in log)
    metrics = base.eval_retriever(retr, [enc], cfg)
    for k in (1, 3, 5):
        assert 0.0 <= metrics[f"hit{k}"] <= 1.0
        assert 0.0 <= metrics[f"rand{k}"] <= 1.0
    out = probe.v_side_doc(model, enc, DEVICE)
    for arm in ("direct", "backbone"):
        assert out[arm]["n_bytes"] == probe.CODE_DIGITS
        assert 0.0 <= out[arm]["byte_acc"] <= 1.0


# --- V-side cond wiring guards (2026-08-17 identity-scare regression) --------
# Forensics on the a-grid 20k checkpoint (cond_sensitivity_a_grid.json):
# zero-cond and cross-doc-swapped cond both crash needle byte_acc to 0.00 —
# the parallel span decode is 100% cond-driven (no byte context exists), and
# the direct/backbone arms read DISTINCT cond rows (cosine ~0.96 near-parallel
# from shared-target training, not a wiring alias). These tests pin the wiring.


def test_v_side_arms_are_not_aliased():
    """direct and backbone arms must read DIFFERENT cond rows."""
    model, enc = _encode_grid("a")
    w, j, _slot, _tgt = enc["code_units"][0]
    g = enc["metas"][w]["offset"] + j
    pos = model.chunk_pos.weight[j : j + 1].unsqueeze(0)
    direct = model.decoder_in_mem(enc["v_rows"][g : g + 1].float().unsqueeze(0)) + pos
    backbone = enc["backbone"][g : g + 1].float().unsqueeze(0) + pos
    assert direct.abs().sum() > 0 and backbone.abs().sum() > 0
    assert not torch.allclose(direct, backbone, atol=1e-3)


def test_decode_logits_depend_on_cond():
    """Mechanism guard: zeroing the cond row, or swapping in another chunk's
    row (same position embedding, wrong content), must change the logits."""
    model, enc = _encode_grid("a")
    w, j, _slot, _tgt = enc["code_units"][0]
    m = enc["metas"][w]
    tm = m["tm"][j : j + 1].unsqueeze(0)

    def row(glob):
        return model.decoder_in_mem(enc["v_rows"][glob : glob + 1].float().unsqueeze(0))

    pos = model.chunk_pos.weight[j : j + 1].unsqueeze(0)
    cond = row(m["offset"] + j) + pos
    j2 = (j + 1) % m["n_real"]
    cond_swap = row(m["offset"] + j2) + pos
    with torch.no_grad():
        logits_base = model.decoder(cond, tm)
        logits_zero = model.decoder(torch.zeros_like(cond), tm)
        logits_swap = model.decoder(cond_swap, tm)
    assert not torch.allclose(logits_base, logits_zero, atol=1e-4)
    assert not torch.allclose(logits_base, logits_swap, atol=1e-4)


# --- M2 per-item predicate helpers (probe --per-item-log) ---------------------


def test_m2_per_item_predicate_helpers():
    d = 8
    retr = base.Retriever(d, d, "full", 0)
    with torch.no_grad():
        retr.wq.weight.copy_(torch.eye(d))
    e = torch.eye(d)
    keys_a = torch.stack([e[0], e[1], e[2], e[3]])  # needle row isolated
    keys_b = torch.stack([e[0], e[0].clone(), e[1], e[2]])  # needle row has a collinear twin

    def fake_doc(keys, qi):
        return {"memory": keys, "query": keys[qi], "pos_code": {1: torch.tensor([qi])}, "eid": "QX-0000", "n_distr": 3}

    cfg = {"key_src": "memrow", "gran": 1, "key_type": "full", "rank": None}
    rows = probe.per_item_records(retr, [fake_doc(keys_a, 0), fake_doc(keys_b, 0)], cfg)
    assert rows[0]["mu_i"] < 0.01  # isolated row: no interferer
    assert rows[1]["mu_i"] > 0.999  # collinear twin: worst interferer ~= itself
    assert rows[0]["hit1"] == 1.0  # orthogonal needle wins top-1
    assert rows[0]["n_keys"] == 4 and rows[0]["n_pos"] == 1
    # summary aggregation on hand-built rows (quartile math)
    synth = [
        {"mu_i": 0.1, "hit1": 1.0}, {"mu_i": 0.2, "hit1": 0.0},
        {"mu_i": 0.9, "hit1": 0.0}, {"mu_i": 0.8, "hit1": 0.0},
    ]
    s = probe.summarize_per_item(synth)
    assert s["quartile_size"] == 1
    assert s["hit_share_in_low_mu_quartile"] == 1.0  # the only hit is in the low-mu quartile
    assert s["mean_mu_hits"] == 0.1 and s["mean_mu_misses"] > 0.5
    assert probe.summarize_per_item([]) == {"n": 0}
