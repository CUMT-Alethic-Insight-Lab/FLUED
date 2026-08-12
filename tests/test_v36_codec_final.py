"""Strict codec-retention arm (--codec-final-state, user-ruled 2026-08-11;
prereg FLUED_TODO_20260805 §0.3 item 0).

The arm: the whole 512B window is encoded into the KDA state machine, only
the final state S_final is kept, and every chunk row is restored from ONE
read of S_final (no fresh per-chunk S_i reads, no backbone channel, predict
task off). These tests pin the correctness invariant (last-chunk
equivalence), the gradient topology (retention signal reaches early writes;
nothing leaks through per-chunk states), the default-off switch, and the
eval n-scan geometry.
"""

import types

import pytest
import torch

from flued.v36 import FLUEDV36
from tests.test_v36_smoke import tiny_config
from tools.train.v3_6.train_v36_s1 import s1_forward, step_model

PAD_ID = 0
MASK_ID = 257


def _codec_args(**over):
    args = types.SimpleNamespace(
        mask_prob=0.0,
        mask_span_min=1,
        mask_span_max=8,
        mask_mode="byte_span",
        max_chunks=4,
        max_span=8,
        task1_loss_weight=1.0,
        task2_loss_weight=1.0,
        predict_weight=0.0,
        predict_mode="latent",
        predict_latent_weight=0.0,
        amp=False,
        codec_final_state=True,
    )
    for k, v in over.items():
        setattr(args, k, v)
    return args


def test_read_all_final_matches_last_chunk_readout():
    """Built-in correctness invariant: the last valid chunk's S_i IS S_final
    (padded chunks are identity steps), so the final-state readout must equal
    the normal per-chunk package at each sample's last valid row."""
    torch.manual_seed(0)
    cfg = tiny_config(per_chunk_readout=True, kda_impl="torch", readout_queries=3)
    model = FLUEDV36(cfg)
    memory = torch.randn(2, 4, cfg.d_mem)
    gates = model.write_head(memory)
    chunk_mask = torch.tensor([[True, True, True, True], [True, True, False, False]])
    with torch.no_grad():
        package, state_norm = model.state_machine(gates, chunk_mask)  # (B, C, q, d_pack)
        final_pkg, final_norm = model.state_machine.read_all_final(gates, chunk_mask)
    assert final_pkg.shape == (2, 3, cfg.d_pack)  # (B, nq, d_pack) — no chunk dim
    last = chunk_mask.long().sum(dim=1) - 1  # [3, 1]
    ref = package[torch.arange(2), last]
    assert torch.allclose(final_pkg, ref, atol=1e-5)
    assert torch.allclose(final_norm, state_norm, atol=1e-5)
    assert torch.isfinite(final_pkg).all()


def test_read_all_final_gradient_reaches_early_writes():
    """The arm's whole point: a loss on the FINAL readout must backprop into
    the EARLIEST chunk's write gates (retention gradient through S_final)."""
    torch.manual_seed(0)
    cfg = tiny_config(per_chunk_readout=True, kda_impl="torch")
    model = FLUEDV36(cfg)
    memory = torch.randn(2, 3, cfg.d_mem, requires_grad=True)
    gates = model.write_head(memory)
    chunk_mask = torch.ones(2, 3, dtype=torch.bool)
    final_pkg, state_norm = model.state_machine.read_all_final(gates, chunk_mask)
    final_pkg.sum().backward()
    assert memory.grad is not None
    assert memory.grad[:, 0].abs().sum() > 0, "chunk 0 write must see the final-readout gradient"
    assert memory.grad[:, -1].abs().sum() > 0
    # the readout query itself is trained too
    assert model.state_machine.readout_query.grad is not None
    assert model.state_machine.readout_query.grad.abs().sum() > 0


def test_read_all_final_requires_state_channel():
    cfg = tiny_config(per_chunk_readout=True, kda_impl="torch", state_channel=False)
    model = FLUEDV36(cfg)
    gates = model.write_head(torch.randn(1, 2, cfg.d_mem))
    with pytest.raises(ValueError, match="state_channel"):
        model.state_machine.read_all_final(gates, torch.ones(1, 2, dtype=torch.bool))


def test_mode_switch_default_off():
    """The switch must default off so canonical runs and the canonical-sync
    guard are untouched."""
    from tools.train.v3_6 import train_v36_s1
    from tools.train.v3_6.train_v36 import build_parser

    parser = build_parser()
    train_v36_s1._add_s1_args(parser)
    args = parser.parse_args([])
    assert args.codec_final_state is False
    assert args.predict_weight == 1.0  # canonical default unmoved
    args_on = parser.parse_args(["--codec-final-state"])
    assert args_on.codec_final_state is True


def test_s1_forward_codec_final_single_shared_readout():
    """content rows are one expanded final readout (identical across chunks by
    construction -> no per-chunk S_i can leak in); completion shares the
    direct conditioning (backbone excluded)."""
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(per_chunk_readout=True, kda_impl="torch"))
    model.train()
    ids = torch.randint(1, 258, (2, 32))
    out = s1_forward(model, ids, _codec_args())
    assert out["content"].shape == (2, 4, 64)
    assert torch.equal(out["content"][:, 0], out["content"][:, 3])
    assert out["logits_backbone"] is out["logits_direct"]
    assert out["logits_direct"].shape == (2, 4, 8, 258)
    assert torch.isfinite(out["logits_direct"]).all()
    assert torch.isfinite(out["state_norm"]).all()
    # default path untouched: per-chunk reads differ across chunks
    out_ref = s1_forward(model, ids, types.SimpleNamespace())
    assert not torch.equal(out_ref["content"][:, 0], out_ref["content"][:, 3])


def test_step_model_codec_final_predict_off_and_gradients():
    """Predict metrics are exact zeros (not computed); the codec losses train
    encoder/summarizer/write_head/state_machine/decoder; the backbone gets
    nothing."""
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(per_chunk_readout=True, kda_impl="torch"))
    model.train()
    ids = torch.randint(1, 257, (2, 32))
    loss, metrics = step_model(model, (ids,), _codec_args(), torch.device("cpu"), train=True)
    assert torch.isfinite(loss)
    for key in ("predict_loss", "predict_ce", "predict_byte_acc", "predict_cos"):
        assert float(metrics[key]) == 0.0, key
    loss.backward()
    for prefix in ("summarizer", "write_head", "state_machine", "decoder"):
        grads = [p.grad for n, p in model.named_parameters() if n.startswith(prefix)]
        assert any(g is not None and g.abs().sum() > 0 for g in grads), prefix
    b_grads = [p.grad for n, p in model.named_parameters() if n.startswith("backbone")]
    assert all(g is None or g.abs().sum() == 0 for g in b_grads), "backbone must stay out of the loss path"


def test_eval_scan_rows_and_full_density_sanity():
    """Eval n-scan reports {n1,n4,n8,nlast} full-window acc in [0,1]; n=last
    (full query density) reproduces the training-form result exactly."""
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(per_chunk_readout=True, kda_impl="torch"))
    model.eval()
    ids = torch.randint(1, 257, (2, 32))
    loss, metrics = step_model(model, (ids,), _codec_args(), torch.device("cpu"), train=False)
    for tag in ("n1", "n4", "n8", "nlast"):
        key = f"final_scan_acc_{tag}"
        assert key in metrics, key
        assert 0.0 <= float(metrics[key]) <= 1.0, key
    assert abs(float(metrics["final_scan_acc_nlast"]) - float(metrics["backbone_acc"])) < 1e-6


def test_scan_absent_when_switch_off():
    """Default mode adds no scan metrics and keeps the predict task alive."""
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(per_chunk_readout=True, kda_impl="torch"))
    model.eval()
    args = _codec_args(codec_final_state=False, predict_weight=1.0)
    ids = torch.randint(1, 257, (2, 32))
    loss, metrics = step_model(model, (ids,), args, torch.device("cpu"), train=False)
    assert not any(k.startswith("final_scan") for k in metrics)
    assert float(metrics["predict_loss"]) != 0.0 or float(metrics["predict_cos"]) != 0.0
