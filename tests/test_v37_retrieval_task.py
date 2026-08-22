"""v3.7 slm 自然检索任务 (5th task, recruitment arm prereg 2026-08-21).

Spec note: docs/versions/v3.7/FLUED_V3_7_RECRUITMENT_ARM_NATURAL_RETRIEVAL_20260821_CN.md.
Source = 32-64B in-window fragment; one ASCII word W ([A-Za-z]{3,10}) is
blanked in the tail question; 答案是：W is the echo. r = --retrieval-block-prob
is the 档 a store_block excision rate.

Covers: (1) off = bitwise-identical legacy path; (2) splice determinism +
structural invariants; (3) inactive rows (short window / no ASCII word);
(4) force-mask/unmask overrides (echo masked, source W visible); (5) echo
byte -> (chunk, slot) grid reuse; (6) store_block construction (source chunk
rows excised only for queries >= the question's first chunk); (7) finite loss
+ retrieval metrics end to end + r actually changes the forward; (8) loud
rejections (non-slm, cloze mutex, r range); (9) parser defaults.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
import torch

from flued.data import BYTE_OFFSET, MASK_ID, PAD_ID
from flued.v36 import FLUEDV36
from tests.test_v37_slm import _s1_args, tiny_config
from tools.train.v3_6 import train_v36_s1 as s1

TEXT1 = (
    b"The quick brown fox jumps over the lazy dog and runs through the forest "
    b"while the silver river winds between the hills under a cloudy sky "
    b"and every traveler remembers the winding road behind the old harbor "
) * 3
TEXT2 = (
    b"Another window with different words: the patient teacher explains the "
    b"second theorem while students copy every symbol into their notebooks "
    b"and the northern station clock keeps counting the quiet minutes "
) * 3


def _clean(rows: list[bytes], width: int) -> torch.Tensor:
    """PAD-offset encode fixed-width windows from raw bytes (prefix-valid)."""
    out = torch.full((len(rows), width), PAD_ID, dtype=torch.long)
    for b, raw in enumerate(rows):
        raw = raw[:width]
        out[b, : len(raw)] = torch.tensor([x + BYTE_OFFSET for x in raw], dtype=torch.long)
    return out


def _row_bytes(row: torch.Tensor) -> bytes:
    return bytes(int(i) - BYTE_OFFSET for i in row.tolist() if int(i) != PAD_ID)


# --- 1. off = bitwise-identical legacy path ---------------------------------


def test_retrieval_off_is_bitwise_identical():
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    batch = (torch.randint(1, 257, (2, 48)),)
    device = torch.device("cpu")
    gen_state_before = s1._RETRIEVAL_GENERATOR.get_state()
    torch.manual_seed(123)  # byte_span masks draw from the global RNG
    loss1, m1 = s1.step_model(model, batch, _s1_args(retrieval_prob=0.0, retrieval_weight=1.0), device, train=False)
    torch.manual_seed(123)
    loss2, m2 = s1.step_model(model, batch, _s1_args(retrieval_prob=0.0, retrieval_weight=99.0), device, train=False)
    assert torch.equal(loss1, loss2)  # the retrieval weight never touches an off task
    assert torch.equal(s1._RETRIEVAL_GENERATOR.get_state(), gen_state_before)  # zero RNG consumption
    for key in (
        "retrieval_loss",
        "retrieval_byte_acc",
        "retrieval_exact",
        "retrieval_count",
        "retrieval_block_rate",
    ):
        assert key in m1 and m1[key].item() == 0.0
    # the off-path loss is exactly the three-task sum
    expect = m1["direct_loss"] * 1.0 + m1["completion_loss"] * 1.0 + m1["predict_loss"] * 1.0
    assert torch.equal(loss1, expect)
    for key in m1:
        if key.startswith("retrieval_"):
            continue
        assert torch.equal(m1[key], m2[key])


# --- 2. splice determinism + structural invariants ---------------------------


def test_splice_deterministic_same_seed():
    clean = _clean([TEXT1, TEXT2], 384)
    out1, metas1 = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(7))
    out2, metas2 = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(7))
    assert torch.equal(out1, out2)
    assert metas1 == metas2
    # non-vacuous: a different seed produces a different splice
    out3, _ = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(8))
    assert not torch.equal(out1, out3)
    for b, m in enumerate(metas1):
        assert m is not None  # prob 1.0 selects every eligible row
        row = _row_bytes(out1[b])
        slo, shi = m["source_span"]
        alo, ahi = m["source_answer_span"]
        elo, ehi = m["echo_span"]
        answer = m["answer_b"]
        # source fragment: 32-64B inside the original window, W inside it
        assert 8 <= shi - slo <= 64  # UTF-8 snap may trim a few bytes off 32
        assert 0 <= slo < shi <= 384
        assert slo <= alo < ahi <= shi
        assert row[alo:ahi] == answer
        assert answer.isalpha() and answer.isascii() and 3 <= len(answer) <= 10
        # tail layout: \n前文'<F with W -> ___>'空格处是什么？\n答案是：<W>
        tail = row[m["query_start"] :]
        assert tail.startswith("\n前文'".encode("utf-8"))
        assert "'空格处是什么？".encode("utf-8") in tail
        assert tail.count(b"___") == 1
        assert elo < ehi == len(row)
        assert row[elo:ehi] == answer  # the echo answer sits at the very tail
        prompt = "\n答案是：".encode("utf-8")
        assert row[elo - len(prompt) : elo] == prompt
        # the blanked question fragment matches the source fragment
        frag = row[slo:shi]
        qfrag = frag[: alo - slo] + b"___" + frag[ahi - slo :]
        assert qfrag in tail


def test_splice_prob_zero_and_partial():
    clean = _clean([TEXT1, TEXT2, TEXT1, TEXT2], 200)
    out, metas = s1._splice_retrieval(clean, 0.0, torch.Generator().manual_seed(11))
    assert out is clean or torch.equal(out, clean)
    assert metas == [None] * 4
    assert out.shape == clean.shape  # no widening when nothing is spliced
    # prob 0.5: unselected rows stay byte-identical
    out2, metas2 = s1._splice_retrieval(clean, 0.5, torch.Generator().manual_seed(11))
    for b, m in enumerate(metas2):
        if m is None:
            assert torch.equal(out2[b, : clean.size(1)], clean[b])


# --- 3. inactive rows: short window / no ASCII word --------------------------


def test_splice_inactive_without_ascii_word():
    raw = "中文窗口没有任何可抽取的英文单词，整段都是汉字标点。".encode("utf-8") * 6
    clean = _clean([raw], 300)
    out, metas = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(5))
    assert metas == [None]  # no [A-Za-z]{3,10} run anywhere -> inactive
    assert torch.equal(out, clean)


def test_splice_inactive_short_window():
    clean = _clean([b"hi fox"], 16)  # n < 32: no qualifying fragment
    out, metas = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(5))
    assert metas == [None]
    assert torch.equal(out, clean)


# --- 4. force-mask / force-unmask overrides ---------------------------------


def test_mask_overrides_echo_masked_source_word_visible():
    clean = _clean([TEXT1], 300)
    out, metas = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(3))
    m = metas[0]
    alo, ahi = m["source_answer_span"]
    elo, ehi = m["echo_span"]
    byte_mask = torch.zeros_like(out, dtype=torch.bool)
    byte_mask[0, alo:ahi] = True  # the regular mask WOULD have hidden the source word
    noise = torch.zeros_like(out, dtype=torch.bool)
    noise[0, : elo : 2] = True  # noise elsewhere, incl. the question region
    byte_mask |= noise
    after = s1._retrieval_mask_overrides(byte_mask.clone(), metas)
    assert after[0, elo:ehi].all()  # echo fully force-MASKED
    assert not after[0, alo:ahi].any()  # source answer word fully force-UNMASKED
    keep = torch.ones_like(after)
    keep[0, elo:ehi] = False
    keep[0, alo:ahi] = False
    assert torch.equal(after & keep, byte_mask & keep)  # nothing else touched
    # and the encoded source really shows MASK_ID at the echo only
    source = out.masked_fill(after, MASK_ID)
    assert (source[0, elo:ehi] == MASK_ID).all()
    assert (source[0, alo:ahi] != MASK_ID).all()


# --- 5. echo byte -> (chunk, slot) grid (cloze slot grid reused) -------------


def test_retrieval_echo_uses_cloze_slot_grid():
    chunk_ids = torch.tensor([[0, 0, 1, 1, 2, 2, 2, 3, 3, 3]])
    offsets = torch.tensor([[0, 1, 0, 1, 0, 1, 2, 0, 1, 2]])
    metas = [{"echo_span": (4, 8), "source_span": (0, 2), "source_answer_span": (0, 2), "query_start": 6}]
    slot, active = s1._cloze_slot_grid(metas, chunk_ids, offsets, max_chunks=4, max_span=4)
    assert bool(active[0])
    got = {(int(c), int(s)) for c, s in slot[0].nonzero().tolist()}
    assert got == {(2, 0), (2, 1), (2, 2), (3, 0)}  # t=4..7 mapped through the packing


# --- 6. store_block construction (档 a excision grid) ------------------------


def _fake_chunks(chunk_ids: torch.Tensor, n_chunks: int):
    chunk_mask = torch.zeros(chunk_ids.size(0), n_chunks, dtype=torch.bool)
    chunk_mask[:, : int(chunk_ids.max()) + 1] = True
    return SimpleNamespace(chunk_ids=chunk_ids, chunk_mask=chunk_mask)


def test_store_block_construction():
    chunk_ids = torch.tensor([[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]])
    chunks = _fake_chunks(chunk_ids, 4)
    metas = [{"source_span": (3, 6), "query_start": 9, "echo_span": (10, 12)}]
    block, rate = s1._retrieval_store_block(metas, chunks, 1.0, torch.Generator().manual_seed(1))
    assert rate == 1.0
    assert block.shape == (1, 4, 4)
    # source fragment t=3..5 -> chunk 1; question head t=9 -> chunk 3
    expect = torch.zeros(1, 4, 4, dtype=torch.bool)
    expect[0, 3:, 1] = True
    assert torch.equal(block, expect)


def test_store_block_r_zero_is_none_and_stream_stable():
    chunk_ids = torch.tensor([[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]])
    chunks = _fake_chunks(chunk_ids, 4)
    metas = [{"source_span": (3, 6), "query_start": 9, "echo_span": (10, 12)}, None]
    block, rate = s1._retrieval_store_block(metas, chunks, 0.0, torch.Generator().manual_seed(1))
    assert block is None and rate == 0.0
    # the r draw is consumed for every spliced row regardless of r: the stream
    # advances identically for r=0 and r=1
    g0 = torch.Generator().manual_seed(1)
    g1 = torch.Generator().manual_seed(1)
    s1._retrieval_store_block(metas, chunks, 0.0, g0)
    s1._retrieval_store_block(metas, chunks, 1.0, g1)
    assert torch.equal(g0.get_state(), g1.get_state())


def test_store_block_deterministic_same_seed():
    chunk_ids = torch.randint(0, 4, (2, 64))
    chunk_ids[:, :4] = 0  # keep the source region packed
    chunks = _fake_chunks(chunk_ids, 6)
    metas = [
        {"source_span": (1, 3), "query_start": 40, "echo_span": (50, 55)},
        {"source_span": (0, 2), "query_start": 30, "echo_span": (40, 44)},
    ]
    b1, r1 = s1._retrieval_store_block(metas, chunks, 0.5, torch.Generator().manual_seed(9))
    b2, r2 = s1._retrieval_store_block(metas, chunks, 0.5, torch.Generator().manual_seed(9))
    assert r1 == r2
    assert (b1 is None) == (b2 is None)
    if b1 is not None:
        assert torch.equal(b1, b2)


# --- 7. end-to-end: finite loss, retrieval metrics, r changes the forward ----


def _e2e_setup(retrieval_block_prob: float):
    torch.manual_seed(0)
    cfg = tiny_config(max_chunks=64, max_span=32, bytes_per_chunk=16, max_positions=64)
    model = FLUEDV36(cfg)
    args = _s1_args(
        retrieval_prob=1.0,
        retrieval_weight=1.0,
        retrieval_block_prob=retrieval_block_prob,
        mask_prob=0.1,
        max_chunks=64,
        max_span=32,
    )
    batch = (_clean([TEXT1, TEXT2], 384),)
    return model, args, batch


def test_step_model_retrieval_finite_and_metrics():
    model, args, batch = _e2e_setup(retrieval_block_prob=1.0)
    s1._RETRIEVAL_GENERATOR.manual_seed(42 + s1._RETRIEVAL_SEED_OFFSET)
    loss, metrics = s1.step_model(model, batch, args, torch.device("cpu"), train=True)
    assert torch.isfinite(loss)
    for key in (
        "retrieval_loss",
        "retrieval_byte_acc",
        "retrieval_exact",
        "retrieval_count",
        "retrieval_block_rate",
    ):
        assert key in metrics, key
        assert torch.isfinite(metrics[key]), key
    assert metrics["retrieval_count"].item() == 1.0  # prob 1.0 + enough capacity: every sample active
    assert metrics["retrieval_block_rate"].item() == 1.0  # r=1.0 excises every spliced sample
    assert 0.0 <= metrics["retrieval_byte_acc"].item() <= 1.0
    assert metrics["retrieval_loss"].item() > 0.0
    loss.backward()
    # the retrieval gradient flows into the retrieval path (backbone store alignment)
    assert model.backbone.align_k.weight.grad is not None
    assert model.backbone.align_k.weight.grad.abs().sum() > 0


def test_store_block_actually_changes_forward():
    """r=1.0 vs r=0.0 with identical seeds: the only difference is the 档 a
    excision, so the loss must move (store_block really reaches the backbone)."""
    losses = []
    for r in (0.0, 1.0):
        model, args, batch = _e2e_setup(retrieval_block_prob=r)
        torch.manual_seed(123)
        s1._MASK_GENERATOR.manual_seed(1042)
        s1._RETRIEVAL_GENERATOR.manual_seed(1042 + s1._RETRIEVAL_SEED_OFFSET)
        loss, metrics = s1.step_model(model, batch, args, torch.device("cpu"), train=False)
        assert metrics["retrieval_count"].item() == 1.0
        assert metrics["retrieval_block_rate"].item() == r
        losses.append(loss)
    assert not torch.equal(losses[0], losses[1])


def test_step_model_retrieval_deterministic_eval_seed():
    """eval 同源固定种子: two evaluate-style passes with the same eval seed
    splice and block identically (same metrics bit-for-bit)."""
    model, args, batch = _e2e_setup(retrieval_block_prob=0.5)
    rows = []
    for _ in range(2):
        torch.manual_seed(args.eval_mask_seed)
        s1._MASK_GENERATOR.manual_seed(args.eval_mask_seed)
        s1._RETRIEVAL_GENERATOR.manual_seed(args.eval_mask_seed + s1._RETRIEVAL_SEED_OFFSET)
        loss, metrics = s1.step_model(model, batch, args, torch.device("cpu"), train=False)
        rows.append((loss, {k: v for k, v in metrics.items()}))
    assert torch.equal(rows[0][0], rows[1][0])
    for key in rows[0][1]:
        assert torch.equal(rows[0][1][key], rows[1][1][key]), key


# --- 8. loud rejections --------------------------------------------------------


def test_retrieval_rejects_xattn_path():
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(backbone_mode="xattn", k_row_source="memory", v_row_source="memory"))
    args = _s1_args(retrieval_prob=0.3)
    batch = (torch.randint(1, 257, (2, 48)),)
    with pytest.raises(ValueError, match="retrieval"):
        s1.step_model(model, batch, args, torch.device("cpu"), train=False)


def test_retrieval_rejects_cloze_mutex(tmp_path):
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    bank = tmp_path / "bank.jsonl"
    passage = "a" * 40 + "ANSWER_TOKEN_PLACEHOLDER_1234567" + "b" * 40
    bank.write_text(
        '{"id": 0, "passage": "%s", "answer": "ANSWER_TOKEN_PLACEHOLDER_1234567", '
        '"query": "%s", "answer_bytes": 32}\n'
        % (passage, passage.replace("ANSWER_TOKEN_PLACEHOLDER_1234567", "___")),
        encoding="utf-8",
    )
    s1._load_cloze_bank(str(bank))
    try:
        args = _s1_args(retrieval_prob=0.3, cloze_prob=0.3)
        batch = (torch.randint(1, 257, (2, 48)),)
        with pytest.raises(ValueError, match="mutually exclusive"):
            s1.step_model(model, batch, args, torch.device("cpu"), train=False)
    finally:
        s1._CLOZE_BANK = None  # restore module state


def test_check_retrieval_args_loud():
    base = _s1_args()
    base.retrieval_block_prob = 1.5
    with pytest.raises(SystemExit, match="retrieval-block-prob"):
        s1._check_retrieval_args(base)
    base = _s1_args()
    base.retrieval_block_prob = -0.1
    with pytest.raises(SystemExit, match="retrieval-block-prob"):
        s1._check_retrieval_args(base)
    base = _s1_args(retrieval_prob=0.5)
    base.backbone_mode = "xattn"
    with pytest.raises(SystemExit, match="slm"):
        s1._check_retrieval_args(base)
    base = _s1_args(retrieval_prob=0.5, cloze_prob=0.5)
    base.backbone_mode = "slm"
    with pytest.raises(SystemExit, match="mutually exclusive"):
        s1._check_retrieval_args(base)
    # the canonical off path passes silently
    s1._check_retrieval_args(_s1_args())
    ok = _s1_args(retrieval_prob=0.5, retrieval_block_prob=1.0)
    ok.backbone_mode = "slm"
    s1._check_retrieval_args(ok)


# --- 9. parser defaults ---------------------------------------------------------


def test_parser_defaults_retrieval_off():
    from tools.train.v3_6.train_v36 import build_parser

    s1_parser = build_parser()
    s1._add_s1_args(s1_parser)
    args = s1_parser.parse_args([])
    assert args.retrieval_prob == 0.0  # default off = zero intrusion
    assert args.retrieval_weight == 1.0
    assert args.retrieval_block_prob == 0.0
