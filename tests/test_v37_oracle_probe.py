"""Tests for the oracle-write verdict probe
(tools/analysis/v3_6/probe_oracle_write_verdict.py).

Tiny random-init slm c-grid models (k=index, v=state) on CPU — algebra and
wiring correctness only; no trained behavior. boundary_mode="uniform" keeps
chunking deterministic.
"""

from __future__ import annotations

import math
from argparse import Namespace

import torch
import torch.nn.functional as F

from flued.v36 import FLUEDV36, V36Config
import tools.analysis.v3_6.probe_oracle_write_verdict as orc
import tools.train.v3_6.train_v36_s1 as s1

DEVICE = torch.device("cpu")


def _tiny_c_config(**overrides):
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
        k_row_source="index", v_row_source="state",  # the c grid under test
    )
    cfg.update(overrides)
    return V36Config(**cfg)


def _model_and_front_end(seed=0, window=256):
    torch.manual_seed(seed)
    model = FLUEDV36(_tiny_c_config()).eval()
    ids = torch.randint(1, 258, (1, window))
    chunks, memory, index = orc._front_end(model, ids)
    return model, ids, chunks, memory, index


# --- 1. oracle-state algebra: S = Σkvᵀ and ridge unmixing restores V ---------


def test_ridge_recovers_writes_from_oracle_state():
    torch.manual_seed(0)
    # n <= hk is REQUIRED: the per-head state (hk x hv) can hold at most hk
    # independent keys; exact recovery is information-theoretically impossible
    # for n > hk (the real model's hk=128 vs ~170-280 chunks capacity gap is
    # itself one of the probe's mechanism measurements).
    n, H, hk, hv = 12, 2, 16, 8
    k = F.normalize(torch.randn(1, n, H, hk), dim=-1)
    v = torch.randn(1, n, H, hv)
    gates = {"k": k, "v": v, "beta": torch.rand(1, n, H), "alpha": torch.ones(1, 1, H, hk)}
    S = orc.oracle_states(gates, n)
    ref = torch.einsum("bchk,bchv->bchkv", k, v).cumsum(dim=1)
    assert torch.allclose(S, ref)  # S_i = Σ_{j≤i} k_j v_jᵀ exactly
    v_hat, cos = orc.ridge_unmix(gates, S, 1e-6)
    assert cos > 0.999
    assert torch.allclose(v_hat.reshape(1, n, H, hv), v, atol=1e-3)
    # mid-sequence states recover their own chunk's write too
    v_hat_mid, cos_mid = orc.ridge_unmix(gates, S[:, : n // 2], 1e-4)
    assert cos_mid > 0.99


# --- 2. trained-state construction + trained read == the model's own path ----


def test_trained_states_and_read_match_model():
    model, _ids, chunks, memory, _ = _model_and_front_end()
    sm = model.state_machine
    gates = model.write_head(memory)
    n_real = int(chunks.chunk_mask[0].sum())
    S = orc.trained_states(sm, gates, n_real)
    v_rows = orc.read_trained(sm, S)
    package, _sn = sm(gates, chunks.chunk_mask)  # the model's own torch path
    assert torch.allclose(v_rows, package.mean(dim=2)[:, :n_real], atol=1e-4)
    # and identical to the _slm_store_rows v_rows (the production wiring)
    _k, v_native, _s, _m, _i = model._slm_store_rows(chunks)
    assert torch.allclose(v_rows, v_native[:, :n_real], atol=1e-4)


# --- 3. decode wiring == _slm_forward's logits_direct -------------------------


def test_decode_direct_matches_slm_forward():
    model, ids, chunks, _memory, _ = _model_and_front_end()
    _k, v_rows, _s, _m, _i = model._slm_store_rows(chunks)
    n_real = int(chunks.chunk_mask[0].sum())
    logits_mine = orc.decode_direct(model, v_rows[:, :n_real], chunks)
    out = s1._slm_forward(model, ids, None)
    assert torch.allclose(logits_mine, out["logits_direct"][:, :n_real], atol=1e-5)


# --- 4. oracle readout path: realign(q·S) matches stream_step semantics -------


def test_oracle_read_matches_stream_step_form():
    """read_trained on manually built states must equal the state machine's
    streaming readout of the SAME states (the probe's readout wiring guard)."""
    model, _ids, chunks, memory, _ = _model_and_front_end()
    sm = model.state_machine
    gates = model.write_head(memory)
    n_real = int(chunks.chunk_mask[0].sum())
    S = orc.trained_states(sm, gates, n_real)
    # stream through the gates with the model's own stream_step; the per-chunk
    # package must equal read_trained's row
    state = sm.init_stream_state(1, DEVICE)
    import tools.eval.paging_harness as ph

    rows = []
    for i in range(n_real):
        package_i, state = sm.stream_step(ph._slice_gates(gates, i, gates["k"].size(1)), state)
        rows.append(package_i[:, 0].mean(dim=1))
    v_stream = torch.stack(rows, dim=1)
    assert torch.allclose(orc.read_trained(sm, S), v_stream, atol=1e-4)


# --- 5. tiny end-to-end: the arm matrix runs and stays finite -----------------


def test_run_window_c_tiny_end_to_end():
    model, _ids, _chunks, _memory, _ = _model_and_front_end(seed=3)
    ns = Namespace(max_chunks=32, max_span=16)
    clean = torch.randint(1, 258, (1, 256))
    byte_mask = torch.zeros_like(clean, dtype=torch.bool)
    byte_mask[0, 10:14] = True  # a few masked bytes so the recalled slot set is non-empty
    arms, mech, prows = orc.run_window_c(model, ns, clean, byte_mask, [0.01], first_window=True)
    assert prows["xs_v"].size(0) == mech["n_real"]
    assert set(arms) == {
        "A1_trained", "A2_oracle_state", "A5_passthrough",
        "A3_ridge_trained_l0.01", "A4_ridge_oracle_l0.01",
    }
    for tag, m in arms.items():
        assert math.isfinite(m["ce"]), tag
        assert 0.0 <= m["acc"] <= 1.0, tag
        assert len(m["row_acc_own"]) == mech["n_real"], tag
    assert 0 < mech["n_real"] <= 32  # uniform 8B cuts, minus utf8-continuation refusals
    assert 0.0 <= mech["ridge_cos"]["0.01"]["cos_oracle"] <= 1.0


# --- 6. A6 byte-probe algebra: linearly-decodable content is found, noise is
#        not -----------------------------------------------------------------


def test_byte_probe_algebra():
    torch.manual_seed(0)
    n, d = 400, 32
    X = torch.randn(n, d)
    # 3-class linearly separable labels (one-vs-all ridge's actual habitat)
    W_true = torch.randn(d + 1, 3)
    Xb = torch.cat([X, torch.ones(n, 1)], dim=1)
    Y = (Xb @ W_true).argmax(dim=-1).unsqueeze(1).expand(n, 2).clone() + 65
    valid = torch.ones(n, 2, dtype=torch.bool)
    out = orc.byte_probe(X, Y, valid)
    assert out["0"]["acc"] > 0.75  # linearly present content is clearly recovered (>> majority)
    Yr = torch.randint(0, 258, (n, 2))
    out_r = orc.byte_probe(X, Yr, valid)
    assert out_r["0"]["acc"] < 0.2  # absent content stays near the floor
