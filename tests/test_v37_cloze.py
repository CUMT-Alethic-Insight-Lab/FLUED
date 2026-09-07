"""v3.7 slm cloze 检索回执 (4th task, user-ruled 2026-08-17).

Spec note: docs/versions/v3.7/FLUED_V3_7_CLOZE_TASK_20260817_CN.md.
Bank fixture: tests/fixtures/cloze_bank_tiny.jsonl (20 entries, the
tools/data/mine_cloze_bank.py contract: {"id","passage","answer","query",
"answer_bytes": int UTF-8 byte count}; passage 96-192B, answer 28-36B,
query == passage with the answer replaced by exactly one "___").

Covers: (1) off = bitwise-identical legacy path; (2) splice determinism
(same seed + same window -> same splice); (3) force-mask/unmask overrides
(echo fully masked, passage answer fully visible); (4) echo byte ->
(chunk, slot) grid mapping; (5) finite loss + cloze metrics end to end;
(6) loud rejection of the legacy xattn path.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import torch

from flued.data import BYTE_OFFSET, MASK_ID, PAD_ID
from flued.v36 import FLUEDV36
from tests.test_v37_slm import _s1_args, tiny_config
from tools.train.v3_6 import train_v36_s1 as s1

BANK_PATH = Path(__file__).parent / "fixtures" / "cloze_bank_tiny.jsonl"


@pytest.fixture
def bank():
    n = s1._load_cloze_bank(str(BANK_PATH))
    assert n == 20
    try:
        yield s1._CLOZE_BANK
    finally:
        s1._CLOZE_BANK = None  # restore module state: off-path tests must see None


def _row_bytes(row: torch.Tensor) -> bytes:
    return bytes(int(i) - BYTE_OFFSET for i in row.tolist() if int(i) != PAD_ID)


# --- 0. fixture bank contract self-check (reads the file, not the loader) ----


def test_fixture_bank_contract():
    rows = [
        json.loads(line)
        for line in BANK_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(rows) == 20
    for row in rows:
        assert set(row) == {"id", "passage", "answer", "query", "answer_bytes"}
        pb, ab, qb = (row[k].encode("utf-8") for k in ("passage", "answer", "query"))
        assert 96 <= len(pb) <= 192
        assert 28 <= len(ab) <= 36
        assert row["answer_bytes"] == len(ab)
        assert qb.count(b"___") == 1
        assert qb.replace(b"___", ab, 1) == pb
        lo = pb.find(ab)
        assert 0.25 * len(pb) <= lo <= 0.60 * len(pb)  # mining contract: answer start in [25%, 60%]


# --- 1. off = bitwise-identical legacy path ---------------------------------


def test_cloze_off_is_bitwise_identical():
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    batch = (torch.randint(1, 257, (2, 48)),)
    device = torch.device("cpu")
    gen_state_before = s1._CLOZE_GENERATOR.get_state()
    torch.manual_seed(123)  # byte_span masks draw from the global RNG
    loss1, m1 = s1.step_model(model, batch, _s1_args(cloze_prob=0.0, cloze_weight=0.3), device, train=False)
    torch.manual_seed(123)
    loss2, m2 = s1.step_model(model, batch, _s1_args(cloze_prob=0.0, cloze_weight=99.0), device, train=False)
    assert torch.equal(loss1, loss2)  # the cloze weight never touches an off task
    assert torch.equal(s1._CLOZE_GENERATOR.get_state(), gen_state_before)  # zero RNG consumption
    for key in ("cloze_loss", "cloze_byte_acc", "cloze_exact", "cloze_count"):
        assert key in m1 and m1[key].item() == 0.0
    # the off-path loss is exactly the three-task sum
    expect = (
        m1["direct_loss"] * 1.0 + m1["completion_loss"] * 1.0 + m1["predict_loss"] * 1.0
    )
    assert torch.equal(loss1, expect)
    for key in m1:
        if key.startswith("cloze_"):
            continue
        assert torch.equal(m1[key], m2[key])


# --- 2. splice determinism + structural invariants ---------------------------


def test_splice_deterministic_same_seed(bank):
    clean = torch.randint(1, 257, (2, 200))  # full prefix-valid rows, no PAD
    out1, metas1 = s1._splice_cloze(clean, bank, 1.0, torch.Generator().manual_seed(7))
    out2, metas2 = s1._splice_cloze(clean, bank, 1.0, torch.Generator().manual_seed(7))
    assert torch.equal(out1, out2)
    assert metas1 == metas2
    # non-vacuous: a different seed produces a different splice
    out3, _ = s1._splice_cloze(clean, bank, 1.0, torch.Generator().manual_seed(8))
    assert not torch.equal(out1, out3)
    for b, m in enumerate(metas1):
        assert m is not None  # prob 1.0 selects every eligible row
        entry = bank[m["bank_id"]]
        row = _row_bytes(out1[b])
        lo, hi = m["echo_span"]
        assert row[lo:hi] == entry["answer_b"]  # the echo answer sits at the very tail
        assert hi == len(row)
        alo, ahi = m["passage_answer_span"]
        assert row[alo:ahi] == entry["answer_b"]  # passage answer force-unmask span
        # the tail layout is \n + query + \n答案是： + answer
        assert row[lo - len(entry["query_b"]) - 14 : lo] == b"\n" + entry["query_b"] + "\n答案是：".encode("utf-8")
        # the passage was inserted whole at a UTF-8 boundary inside the first 60%
        p = alo - entry["ans_lo"]
        assert 0 <= p <= int(0.6 * 200) + 3  # +3: forward UTF-8 snap slack
        assert row[p : p + len(entry["passage_b"])] == entry["passage_b"]


def test_splice_prob_zero_and_partial(bank):
    clean = torch.randint(1, 257, (4, 120))
    out, metas = s1._splice_cloze(clean, bank, 0.0, torch.Generator().manual_seed(11))
    assert out is clean or torch.equal(out, clean)
    assert metas == [None] * 4
    assert out.shape == clean.shape  # no widening when nothing is spliced
    # prob 0.5: unselected rows stay byte-identical
    out2, metas2 = s1._splice_cloze(clean, bank, 0.5, torch.Generator().manual_seed(11))
    for b, m in enumerate(metas2):
        if m is None:
            assert torch.equal(out2[b, : clean.size(1)], clean[b])


# --- 3. force-mask / force-unmask overrides ---------------------------------


def test_mask_overrides_echo_masked_answer_visible(bank):
    clean = torch.randint(1, 257, (1, 200))
    out, metas = s1._splice_cloze(clean, bank, 1.0, torch.Generator().manual_seed(3))
    m = metas[0]
    alo, ahi = m["passage_answer_span"]
    elo, ehi = m["echo_span"]
    byte_mask = torch.zeros_like(out, dtype=torch.bool)
    byte_mask[0, alo:ahi] = True  # the regular mask WOULD have hidden the passage answer
    noise = torch.zeros_like(out, dtype=torch.bool)
    noise[0, : elo : 2] = True  # noise elsewhere, incl. the query region
    byte_mask |= noise
    after = s1._cloze_mask_overrides(byte_mask.clone(), metas)
    assert after[0, elo:ehi].all()  # echo fully force-MASKED
    assert not after[0, alo:ahi].any()  # passage answer fully force-UNMASKED
    keep = torch.ones_like(after)
    keep[0, elo:ehi] = False
    keep[0, alo:ahi] = False
    assert torch.equal(after & keep, byte_mask & keep)  # nothing else touched
    # and the encoded source really shows MASK_ID at the echo only
    source = out.masked_fill(after, MASK_ID)
    assert (source[0, elo:ehi] == MASK_ID).all()
    assert (source[0, alo:ahi] != MASK_ID).all()


# --- 4. echo byte -> (chunk, slot) grid mapping ------------------------------


def test_cloze_slot_grid_mapping():
    chunk_ids = torch.tensor([[0, 0, 1, 1, 2, 2, 2, 3, 3, 3]])
    offsets = torch.tensor([[0, 1, 0, 1, 0, 1, 2, 0, 1, 2]])
    metas = [{"echo_span": (4, 8), "passage_answer_span": (0, 2)}]
    slot, active = s1._cloze_slot_grid(metas, chunk_ids, offsets, max_chunks=4, max_span=4)
    assert bool(active[0])
    got = {(int(c), int(s)) for c, s in slot[0].nonzero().tolist()}
    assert got == {(2, 0), (2, 1), (2, 2), (3, 0)}  # t=4..7 mapped through the packing
    # one echo byte truncated out of the grid -> the sample skips the task
    broken = chunk_ids.clone()
    broken[0, 5] = -1
    slot2, active2 = s1._cloze_slot_grid(metas, broken, offsets, 4, 4)
    assert not bool(active2[0])
    assert not slot2.any()


# --- 5. end-to-end: finite loss, cloze metrics, gradient reaches the backbone


def test_step_model_cloze_finite_and_metrics(bank):
    torch.manual_seed(0)
    # capacity must hold window + splice whole so the echo survives packing
    cfg = tiny_config(max_chunks=64, max_span=32, bytes_per_chunk=16, max_positions=64)
    model = FLUEDV36(cfg)
    args = _s1_args(cloze_prob=1.0, cloze_weight=0.3, mask_prob=0.1, max_chunks=64, max_span=32)
    batch = (torch.randint(1, 257, (2, 384)),)
    loss, metrics = s1.step_model(model, batch, args, torch.device("cpu"), train=True)
    assert torch.isfinite(loss)
    for key in ("cloze_loss", "cloze_byte_acc", "cloze_exact", "cloze_count"):
        assert key in metrics, key
        assert torch.isfinite(metrics[key]), key
    assert metrics["cloze_count"].item() == 1.0  # prob 1.0 + enough capacity: every sample active
    assert 0.0 <= metrics["cloze_byte_acc"].item() <= 1.0
    assert metrics["cloze_loss"].item() > 0.0
    loss.backward()
    # the cloze gradient flows into the retrieval path (backbone store alignment)
    assert model.backbone.align_k.weight.grad is not None
    assert model.backbone.align_k.weight.grad.abs().sum() > 0


def test_step_model_cloze_deterministic_eval_seed(bank):
    """eval 同源固定种子: two evaluate-style passes with the same eval seed
    splice identically (same metrics bit-for-bit)."""
    torch.manual_seed(0)
    cfg = tiny_config(max_chunks=64, max_span=32, bytes_per_chunk=16, max_positions=64)
    model = FLUEDV36(cfg)
    args = _s1_args(cloze_prob=1.0, mask_prob=0.1, max_chunks=64, max_span=32)
    batch = (torch.randint(1, 257, (2, 384)),)
    device = torch.device("cpu")
    rows = []
    for _ in range(2):
        torch.manual_seed(args.eval_mask_seed)
        s1._MASK_GENERATOR.manual_seed(args.eval_mask_seed)
        s1._CLOZE_GENERATOR.manual_seed(args.eval_mask_seed + s1._CLOZE_SEED_OFFSET)
        loss, metrics = s1.step_model(model, batch, args, device, train=False)
        rows.append((loss, {k: v for k, v in metrics.items()}))
    assert torch.equal(rows[0][0], rows[1][0])
    for key in rows[0][1]:
        assert torch.equal(rows[0][1][key], rows[1][1][key]), key


# --- 6. loud rejections --------------------------------------------------------


def test_cloze_rejects_xattn_path(bank):
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(backbone_mode="xattn", k_row_source="memory", v_row_source="memory"))
    args = _s1_args(cloze_prob=0.3)
    batch = (torch.randint(1, 257, (2, 48)),)
    with pytest.raises(ValueError, match="cloze"):
        s1.step_model(model, batch, args, torch.device("cpu"), train=False)


def test_cloze_requires_loaded_bank():
    assert s1._CLOZE_BANK is None  # the bank fixture restores module state
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    args = _s1_args(cloze_prob=0.3)
    batch = (torch.randint(1, 257, (2, 48)),)
    with pytest.raises(ValueError, match="bank"):
        s1.step_model(model, batch, args, torch.device("cpu"), train=False)


def test_cloze_bank_loader_rejects_contract_violation(tmp_path):
    bad = BANK_PATH.read_text(encoding="utf-8").splitlines()
    row = json.loads(bad[0])
    row["answer_bytes"] = row["answer_bytes"] + 1  # break the byte-count contract
    path = tmp_path / "bad.jsonl"
    path.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="answer_bytes"):
        s1._load_cloze_bank(str(path))


def test_parser_defaults_cloze_off():
    from tools.train.v3_6.train_v36 import build_parser

    s1_parser = build_parser()
    s1._add_s1_args(s1_parser)
    args = s1_parser.parse_args([])
    assert args.cloze_prob == 0.0  # default off = zero intrusion
    assert args.cloze_weight == 0.3
    assert args.cloze_bank == ""
