"""fork 3 F2 summarizer_aux_recon tests (flued/v36/model.py + trainer wiring).

Spec pinned 2026-08-21 (user-ruled): default off = bit-identical, no aux
modules; on = train-time-only auxiliary per-slot byte-reconstruction head on
the memory rows (2-layer MLP + slot table, ~1.9M params — scout capacity
cap); conditional creation (old checkpoints strict-clean; an aux-trained
checkpoint does NOT strict-load into a flag-off model, by design loud).
"""

from __future__ import annotations

import torch

from flued.v36 import FLUEDV36, V36Config
from tests.test_v37_oracle_probe import _tiny_c_config


def _model(on: bool, seed: int = 0) -> FLUEDV36:
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_c_config(summarizer_aux_recon=on))


# 1. default off: no aux modules, config default False --------------------------


def test_default_off_no_modules():
    m = _model(False)
    assert not hasattr(m, "aux_recon") and not hasattr(m, "aux_out") and not hasattr(m, "aux_slot")
    assert V36Config().summarizer_aux_recon is False
    assert not any("aux_" in k for k in m.state_dict())


# 2. on: modules exist, shapes, params within scout cap -------------------------


def test_aux_head_shapes_and_capacity_cap():
    m = _model(True)
    cfg = m.config
    memory = torch.randn(2, 5, cfg.d_mem)
    logits = m.aux_recon_logits(memory)
    assert logits.shape == (2, 5, cfg.max_span, 258)
    n_aux = sum(p.numel() for n, p in m.named_parameters() if "aux_" in n)
    assert n_aux < 10_000_000, f"scout capacity cap violated: {n_aux}"


# 3. gradient flows through the aux head into the summarizer --------------------


def test_gradient_reaches_summarizer():
    m = _model(True)
    m.train()
    memory = torch.randn(1, 4, m.config.d_mem, requires_grad=True)
    logits = m.aux_recon_logits(memory)
    targets = torch.randint(0, 257, (1, 4, m.config.max_span))
    loss = torch.nn.functional.cross_entropy(logits.reshape(-1, 258).float(), targets.reshape(-1))
    loss.backward()
    assert memory.grad is not None and memory.grad.abs().sum() > 0
    aux_grads = [p.grad for n, p in m.named_parameters() if "aux_" in n]
    assert all(g is not None for g in aux_grads) and sum(g.abs().sum() for g in aux_grads) > 0


# 4. checkpoint compatibility both directions -----------------------------------


def test_state_dict_cross_compatibility():
    off = _model(False, seed=13)
    on = _model(True, seed=13)
    assert not any("aux_" in k for k in off.state_dict())
    # the F2 init path: legacy ckpt -> flag-on model with strict=False (aux
    # head stays at fresh init — the trainer's init loader filters + loads
    # non-strict, so the aux head starts from scratch by design)
    on.load_state_dict(off.state_dict(), strict=False)
    # strict=True fails BOTH ways by design (loud): missing aux keys one way,
    # unexpected aux keys the other — module-structure difference, like
    # split_trunk (NOT the non-persistent-buffer discipline of to_k_center)
    for src, dst in ((off, on), (on, off)):
        try:
            dst.load_state_dict(src.state_dict(), strict=True)
            raise AssertionError("expected strict load to fail across module-structure difference")
        except RuntimeError:
            pass
    # resume path: flag-on checkpoint -> flag-on model strict-clean
    on2 = _model(True, seed=99)
    on2.load_state_dict(on.state_dict(), strict=True)


# 5. plumbing: --summarizer-aux-recon reaches the built model -------------------


def test_cli_flag_reaches_model():
    from tools.train.v3_6.train_v36 import build_model, build_parser

    args = build_parser().parse_args(
        ["--summarizer-aux-recon", "--backbone-mode", "slm", "--k-row-source", "index"]
    )
    model = build_model(args)
    assert model.config.summarizer_aux_recon is True
    assert hasattr(model, "aux_recon")
    args_off = build_parser().parse_args(["--backbone-mode", "slm", "--k-row-source", "index"])
    assert build_model(args_off).config.summarizer_aux_recon is False


# 6. eval path untouched: aux head never fires in eval step ---------------------


def test_eval_step_has_no_aux_in_total_loss():
    import argparse  # noqa: F401
    from tests.test_v37_oracle_probe import _tiny_c_config  # noqa: F401

    m = _model(True)
    m.eval()
    # the aux head is only invoked from the trainer's train branch; the model
    # forward itself never calls it (V36Output carries no aux logits)
    ids = torch.randint(1, 257, (1, 64))
    out = m(ids)
    assert not hasattr(out, "aux_logits")
