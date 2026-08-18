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
    expected = {
        n
        for n, _ in model.named_parameters()
        if n.startswith(rr.TRAINABLE_PREFIXES) and not n.startswith("decoder.byte_lookup.")
    }
    assert trainable == expected
    assert set(names) == expected
    # the shared byte table is part of the decoder module but must stay frozen
    assert not model.decoder.byte_lookup.embedding.weight.requires_grad
    assert not model.byte_lookup.embedding.weight.requires_grad
    # producers stay frozen
    assert not model.write_head.to_k.weight.requires_grad
    assert not model.state_machine.readout_query.requires_grad
    assert not model.backbone.q_proj.weight.requires_grad


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
        if p.requires_grad:
            # noise_cond sees an identically-zero input by design (DiT noise=0)
            # => its grad is structurally zero; existence is what matters there
            assert p.grad is not None, f"no grad on trainable {n}"
            if "noise_cond" not in n:
                assert p.grad.abs().sum() > 0, f"zero grad on trainable {n}"
        else:
            assert p.grad is None, f"grad leaked to frozen {n}"


def test_oracle_vs_natural_states_differ():
    model = _tiny_model().eval()
    clean = torch.randint(1, 258, (1, 256))
    chunks, n_real, S_or = rr._states_for(model, clean, use_oracle=True)
    _, _, S_tr = rr._states_for(model, clean, use_oracle=False)
    assert S_or.shape == S_tr.shape
    assert not torch.allclose(S_or, S_tr)  # the two state kinds are genuinely different


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
