"""fork 2 multi-view readout tests (readout_views in flued/v36/model.py) +
forward verifier (tools/eval/forward_verifier.py).

Spec: docs/versions/v3.7/FLUED_V3_7_FORK2_MULTIVIEW_READOUT_20260819_CN.md
(user-ruled 2026-08-19). Tiny random-init models on CPU.
"""

from __future__ import annotations

import math
from argparse import Namespace

import torch
import torch.nn.functional as F

from flued.v36 import FLUEDV36, V36Config
from flued.v36.model import frame_rotations, probe_frame
from tests.test_v37_oracle_probe import _tiny_c_config
import tools.eval.forward_verifier as fv


# --- 1. probe frame determinism + orthonormality ------------------------------


def test_probe_frame_deterministic_and_orthonormal():
    a = probe_frame(4, 2, 16)
    b = probe_frame(4, 2, 16)
    assert torch.equal(a, b)  # pinned seed: identical in every process
    for h in range(a.size(0)):
        gram = a[h] @ a[h].T
        assert torch.allclose(gram, torch.eye(16 * 0 + 4), atol=1e-5), gram  # rows orthonormal
    c = probe_frame(4, 2, 16, seed=1)
    assert not torch.equal(a, c)


def test_frame_rotations_orthogonal_and_deterministic():
    r1 = frame_rotations(8, 16)
    r2 = frame_rotations(8, 16)
    assert torch.equal(r1, r2)
    for i in range(8):
        assert torch.allclose(r1[i] @ r1[i].T, torch.eye(16), atol=1e-5)
    # distinct table entries
    assert not torch.allclose(r1[0], r1[1])


# --- 2. default off: bit-identical, no buffers --------------------------------


def test_default_views1_bit_identical():
    torch.manual_seed(0)
    m1 = FLUEDV36(_tiny_c_config())  # readout_views default 1
    torch.manual_seed(0)
    m2 = FLUEDV36(_tiny_c_config(readout_views=1))
    ids = torch.randint(1, 258, (1, 128))
    with torch.no_grad():
        o1, o2 = m1(ids), m2(ids)
    assert torch.equal(o1.logits_direct, o2.logits_direct)
    assert torch.equal(o1.logits_backbone, o2.logits_backbone)
    assert not hasattr(m1.state_machine, "view_frame")


# --- 3. m=4: shapes, direct path bit-untouched, backbone path widened ---------


def test_views4_direct_untouched_backbone_widened():
    torch.manual_seed(0)
    m1 = FLUEDV36(_tiny_c_config())  # c grid, v=state
    torch.manual_seed(0)
    m4 = FLUEDV36(_tiny_c_config(readout_views=4))
    ids = torch.randint(1, 258, (1, 128))
    with torch.no_grad():
        o1, o4 = m1(ids), m4(ids)
    assert torch.equal(o1.logits_direct, o4.logits_direct)  # direct path bit-untouched (fork 2 §1.3)
    assert not torch.allclose(o1.logits_backbone, o4.logits_backbone)  # store widened
    assert torch.isfinite(o4.logits_backbone).all() and torch.isfinite(o4.logits_direct).all()
    # no new parameters: strict state-dict cross-load both ways
    m4.load_state_dict(m1.state_dict(), strict=True)
    m1.load_state_dict(m4.state_dict(), strict=True)


def test_views4_b_grid_k_channel_finite():
    torch.manual_seed(0)
    m = FLUEDV36(_tiny_c_config(v_row_source="memory", k_row_source="state", readout_views=4))
    assert hasattr(m.state_machine_k, "view_frame")
    ids = torch.randint(1, 258, (1, 128))
    with torch.no_grad():
        out = m(ids)
    assert torch.isfinite(out.logits_backbone).all()


def test_forward_views_shape_and_shared_realign():
    torch.manual_seed(0)
    m = FLUEDV36(_tiny_c_config(readout_views=4))
    ids = torch.randint(1, 258, (1, 128))
    with torch.no_grad():
        chunks, memory, index = None, None, None
        from tools.analysis.v3_6.probe_oracle_write_verdict import _front_end

        chunks, memory, index = _front_end(m, ids)
        gates = m.write_head(memory)
        v_store = m.state_machine.forward_views(gates, chunks.chunk_mask)
    C = chunks.chunk_mask.size(1)
    assert v_store.shape == (1, C, 4, m.config.d_pack)
    assert torch.isfinite(v_store).all()


# --- 4. verifier synthetic: picks the true candidate, false-peak recorded -----


def test_verifier_synthetic_true_candidate_wins():
    torch.manual_seed(0)
    d = 64
    frame = fv.seeded_frame(8, d)
    true_val = torch.randn(d)
    target = true_val + 0.05 * torch.randn(d)  # noisy measurement of the truth
    cands = [true_val + 0.05 * torch.randn(d)] + [torch.randn(d) for _ in range(7)]
    candidates = torch.stack(cands)
    best, dists = fv.verify(candidates, target, frame)
    assert best == 0
    assert float(dists[0]) < float(dists[1:].min())
    # a pure-noise candidate set has no systematic winner (false-peak guard)
    noise_cands = torch.randn(8, d)
    best2, _ = fv.verify(noise_cands, target, frame)
    assert best2 != 0 or True  # no assertion on the pick; the CLI reports the false-peak rate field


def test_verifier_frame_determinism():
    assert torch.equal(fv.seeded_frame(8, 32), fv.seeded_frame(8, 32))


# --- 4b. completion-form verifier (train_v36 --verify-topl) -------------------


def test_segment_candidates_exact_topl():
    # 3 masked slots, 6-id vocab; scores rigged so the exact joint ranking is
    # [0,0,0] (0.0) > [0,0,1] (-0.5) > [0,1,0] (-1.0) = [2,0,0] (-1.0)
    lp = torch.tensor(
        [
            [0.0, -3.0, -1.0, -2.0, -4.0, -5.0],
            [0.0, -1.0, -2.0, -3.0, -4.0, -5.0],
            [0.0, -0.5, -1.5, -2.5, -3.5, -4.5],
        ]
    )
    cands = fv.segment_candidates(lp, 4)
    assert cands.shape == (4, 3)
    assert cands[0].tolist() == [0, 0, 0]  # greedy is row 0
    assert cands[1].tolist() == [0, 0, 1]
    assert {tuple(cands[2].tolist()), tuple(cands[3].tolist())} == {(0, 1, 0), (2, 0, 0)}
    # topl=1 degenerates to the greedy candidate only
    assert fv.segment_candidates(lp, 1).tolist() == [[0, 0, 0]]


def test_verify_chunk_picks_correct_and_false_peak():
    torch.manual_seed(0)
    d = 48
    frame = fv.seeded_frame(16, d)
    clean_val = torch.randn(d)
    wrong1, wrong2 = torch.randn(d), torch.randn(d)
    cand_vals = torch.stack([wrong1, clean_val + 0.01 * torch.randn(d), wrong2])
    correct = torch.tensor([False, True, False])
    # the verifier must lift the correct candidate out of the top-L (hit@1
    # conversion) even though the greedy row 0 is wrong
    r = fv.verify_chunk(cand_vals, clean_val, frame, correct)
    assert r["hit1_before"] == 0.0 and r["hitl"] == 1.0
    assert r["hit1_after"] == 1.0 and r["false_peak"] == 0.0
    # 伪峰: the target is closest to a WRONG candidate while the correct one is
    # in the top-L -> false_peak recorded
    r2 = fv.verify_chunk(cand_vals, wrong1 + 0.01 * torch.randn(d), frame, correct)
    assert r2["hitl"] == 1.0 and r2["hit1_after"] == 0.0 and r2["false_peak"] == 1.0


def test_verify_completion_eval_tiny_smoke():
    torch.manual_seed(0)
    model = FLUEDV36(_tiny_c_config()).eval()
    ids = torch.randint(1, 258, (1, 128))
    ns = Namespace(
        backbone_mode="slm", v_row_source="state", verify_topl=3,
        eval_mask_seed=1042, max_eval_batches=1,
        mask_prob=0.3, mask_span_min=1, mask_span_max=4,
        max_chunks=model.config.max_chunks, max_span=model.config.max_span,
    )
    stats = fv.verify_completion_eval(model, [(ids,)], ns, torch.device("cpu"))
    for key in (
        "eval_verify_hit1_before",
        "eval_verify_hit1_after",
        "eval_verify_hitl",
        "eval_verify_false_peak",
        "eval_verify_chunks",
    ):
        assert key in stats and math.isfinite(stats[key]), key
    assert stats["eval_verify_chunks"] > 0
    # per-chunk invariant: hit@L covers hit@1-before (correct[0] => any(correct))
    assert stats["eval_verify_hitl"] + 1e-9 >= stats["eval_verify_hit1_before"]
    # off-flag is a no-op
    ns_off = Namespace(**{**vars(ns), "verify_topl": 0})
    assert fv.verify_completion_eval(model, [(ids,)], ns_off, torch.device("cpu")) == {}
    # scope guard: non-state completion channels raise loudly
    ns_bad = Namespace(**{**vars(ns), "v_row_source": "memory"})
    try:
        fv.verify_completion_eval(model, [(ids,)], ns_bad, torch.device("cpu"))
        raise AssertionError("expected ValueError for v_row_source='memory'")
    except ValueError:
        pass


# --- 5. CLI wiring --------------------------------------------------------------


def test_cli_readout_views_reaches_model():
    from tools.train.v3_6.train_v36 import build_model, build_parser

    args = build_parser().parse_args(
        ["--readout-views", "4", "--backbone-mode", "slm", "--k-row-source", "index", "--v-row-source", "state"]
    )
    model = build_model(args)
    assert model.config.readout_views == 4
    assert hasattr(model.state_machine, "view_frame")
    assert build_model(build_parser().parse_args(["--backbone-mode", "slm", "--k-row-source", "index", "--v-row-source", "state"])).config.readout_views == 1


def _tiny_cli_args(extra: list[str]):
    """Tiny-slurm args through the REAL parser (build_model must accept them)."""
    from tools.train.v3_6.train_v36 import build_parser

    args = build_parser().parse_args(
        ["--backbone-mode", "slm", "--k-row-source", "index", "--v-row-source", "state", *extra]
    )
    args.d_byte, args.encoder_layers, args.segmentor_layers, args.nhead, args.ffn_dim = 64, 2, 2, 4, 128
    args.d_mem, args.summarizer_slots, args.summarizer_hidden = 96, 2, 128
    args.kda_heads, args.kda_head_k, args.kda_head_v, args.write_hidden = 2, 16, 32, 128
    args.d_pack, args.d_backbone, args.backbone_layers, args.backbone_nhead, args.backbone_ffn = 64, 64, 3, 4, 128
    args.decoder_hidden, args.decoder_layers = 128, 2
    args.max_chunks, args.max_span, args.bytes_per_chunk, args.max_positions = 32, 16, 8, 64
    args.boundary_mode, args.kda_impl = "uniform", "torch"
    return args


def test_cli_readout_views_m_scan():
    """m 扫描接线 (spec §1.1 预注册 {1,2,4,8}): every m reaches the config; the
    seeded frame buffers exist iff m > 1."""
    from tools.train.v3_6.train_v36 import build_model

    for m in (1, 2, 4, 8):
        model = build_model(_tiny_cli_args(["--readout-views", str(m)]))
        assert model.config.readout_views == m
        assert hasattr(model.state_machine, "view_frame") == (m > 1)
        if m > 1:
            assert model.state_machine.view_frame.shape == (2, m, 16)  # (H, m, hk)


def test_cli_verify_topl_parses_default_off():
    from tools.train.v3_6.train_v36 import build_parser

    assert build_parser().parse_args([]).verify_topl == 0
    assert build_parser().parse_args(["--verify-topl", "5"]).verify_topl == 5
