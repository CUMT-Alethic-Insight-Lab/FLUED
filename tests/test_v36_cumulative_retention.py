"""Cumulative mask-retention completion targets (v36.8 / S39 stage-0c 配方修复).

Pre-v36.8 the S1.0 completion task scored row i on chunk i only, so the
three tasks carried an exactly-zero retention training signal. The fix
expands row i's decoder target to the masked bytes of chunks 0..i while
keeping the (B, C, max_span) grid layout. These tests pin the construction
invariants the trainer relies on:

- row i's target covers exactly the masked positions of chunks 0..i (the own
  chunk's full target is kept as before, appended slots are masked-only);
- no leakage: unmasked bytes of chunks 0..i-1 never enter row i, and nothing
  from chunks i+1.. does;
- rows that are not real chunks stay empty;
- span overflow is counted and never corrupts occupied slots;
- the trainer switch defaults ON and --no-cumulative-mask-retention restores
  the pre-v36.8 per-chunk grids.
"""

from __future__ import annotations

import torch

from flued.data import BYTE_OFFSET, PAD_ID
from tools.train.v3_3.train_v33 import make_targets
from tools.train.v3_6.train_v36_s1 import (
    _add_s1_args,
    _completion_target_grids,
    make_cumulative_retention_targets,
)

MAX_CHUNKS = 4
MAX_SPAN = 8


def _toy(max_span: int = MAX_SPAN):
    """One sample, three chunks of lengths 3/2/4, masks at t=1 (chunk 0),
    t=4 (chunk 1), t=7 (chunk 2). Byte values are distinct per position."""
    values = [10, 11, 12, 20, 21, 30, 31, 32, 33]
    clean = torch.tensor([[BYTE_OFFSET + v for v in values]], dtype=torch.long)
    chunk_ids = torch.tensor([[0, 0, 0, 1, 1, 2, 2, 2, 2]])
    offsets = torch.tensor([[0, 1, 2, 0, 1, 0, 1, 2, 3]])
    byte_mask = torch.zeros_like(clean, dtype=torch.bool)
    byte_mask[0, [1, 4, 7]] = True
    return clean, byte_mask, chunk_ids, offsets, max_span


def _ids_in_row(targets: torch.Tensor, slot_mask: torch.Tensor, row: int) -> set:
    return set(targets[0, row][slot_mask[0, row]].tolist())


def test_row_i_covers_exactly_masked_chunks_0_to_i():
    clean, byte_mask, chunk_ids, offsets, max_span = _toy()
    targets, slot_mask, masked_slot, n_trunc = make_cumulative_retention_targets(
        clean, byte_mask, chunk_ids, offsets, MAX_CHUNKS, max_span
    )
    assert int(n_trunc) == 0
    base_t, base_s, base_m = make_targets(clean, byte_mask, chunk_ids, offsets, MAX_CHUNKS, max_span)

    # Row 0 has no predecessor chunks: identical to the base grid.
    assert torch.equal(targets[0, 0], base_t[0, 0])
    assert torch.equal(slot_mask[0, 0], base_s[0, 0])
    assert torch.equal(masked_slot[0, 0], base_m[0, 0])

    # Row 1: own chunk 1 (t=3,4 at slots 0,1) + masked byte t=1 appended at
    # slot 2 (first free slot after the own bytes).
    assert _ids_in_row(targets, slot_mask, 1) == {21, 22, BYTE_OFFSET + 11}
    assert targets[0, 1, 2].item() == BYTE_OFFSET + 11
    assert slot_mask[0, 1].sum().item() == 3
    # masked slots of row 1 = own masked (t=4 -> slot 1) + recalled t=1 (slot 2)
    assert masked_slot[0, 1].tolist() == [False, True, True, False, False, False, False, False]

    # Row 2: own chunk 2 (t=5..8 at slots 0..3) + masked t=1 (rank 0) at slot
    # 4 and masked t=4 (rank 1) at slot 5, in byte order.
    assert _ids_in_row(targets, slot_mask, 2) == {31, 32, 33, 34, BYTE_OFFSET + 11, BYTE_OFFSET + 21}
    assert targets[0, 2, 4].item() == BYTE_OFFSET + 11
    assert targets[0, 2, 5].item() == BYTE_OFFSET + 21
    assert masked_slot[0, 2].tolist() == [False, False, True, False, True, True, False, False]


def test_no_leakage_unmasked_or_future_chunks():
    clean, byte_mask, chunk_ids, offsets, max_span = _toy()
    targets, slot_mask, masked_slot, _ = make_cumulative_retention_targets(
        clean, byte_mask, chunk_ids, offsets, MAX_CHUNKS, max_span
    )
    # Unmasked bytes of earlier chunks (t=0 -> 11th id BYTE_OFFSET+10, t=2 ->
    # BYTE_OFFSET+12, t=3 -> BYTE_OFFSET+20, t=5/6/8 unmasked of chunk 2) must
    # never appear outside their own row.
    assert BYTE_OFFSET + 10 not in _ids_in_row(targets, slot_mask, 1)
    assert BYTE_OFFSET + 12 not in _ids_in_row(targets, slot_mask, 1)
    assert BYTE_OFFSET + 20 not in _ids_in_row(targets, slot_mask, 2)
    # Nothing from chunk 2 leaks into row 1 (future chunk).
    for future_id in (31, 32, 33, 34):
        assert future_id not in _ids_in_row(targets, slot_mask, 1)
    # Appended slots are all marked masked; unmasked slots stay own-chunk only.
    unmasked = slot_mask & ~masked_slot
    assert unmasked[0, 1].sum().item() == 1  # only t=3
    assert unmasked[0, 2].sum().item() == 3  # only t=5,6,8
    # Row 3 is not a real chunk: stays completely empty despite chunks < 3
    # containing masked bytes.
    assert not slot_mask[0, 3].any()
    # Unscored slots keep PAD targets.
    assert targets[0, 3].eq(PAD_ID).all()
    assert targets[0, 1, 3:].eq(PAD_ID).all()


def test_switch_off_restores_base_grids():
    clean, byte_mask, chunk_ids, offsets, max_span = _toy()
    comp = _completion_target_grids(
        clean, byte_mask, chunk_ids, offsets, MAX_CHUNKS, max_span, cumulative=False
    )
    base = make_targets(clean, byte_mask, chunk_ids, offsets, MAX_CHUNKS, max_span)
    assert torch.equal(comp[0], base[0])
    assert torch.equal(comp[1], base[1])
    assert torch.equal(comp[2], base[2])
    assert int(comp[3]) == 0
    # Sanity: the ON path differs from base exactly by the appended slots.
    on = _completion_target_grids(
        clean, byte_mask, chunk_ids, offsets, MAX_CHUNKS, max_span, cumulative=True
    )
    assert on[1].sum().item() == base[1].sum().item() + 3  # 3 recalled masked slots


def test_overflow_counted_and_occupied_slots_untouched():
    # max_span=3: row 1 fits exactly one recalled byte; row 2 is full of its
    # own (truncated) bytes, so both recalls overflow and must be counted.
    clean, byte_mask, chunk_ids, offsets, max_span = _toy(max_span=3)
    targets, slot_mask, masked_slot, n_trunc = make_cumulative_retention_targets(
        clean, byte_mask, chunk_ids, offsets, MAX_CHUNKS, max_span
    )
    assert int(n_trunc) == 2
    # Row 1 keeps its own bytes and gains the oldest recall at slot 2.
    assert _ids_in_row(targets, slot_mask, 1) == {21, 22, BYTE_OFFSET + 11}
    # Row 2 is full (offsets 3 dropped by the base grid): no recalls land.
    assert slot_mask[0, 2].sum().item() == 3
    assert BYTE_OFFSET + 11 not in _ids_in_row(targets, slot_mask, 2)
    # Occupied own slots are never overwritten.
    assert targets[0, 2, :3].tolist() == [31, 32, 33]


def test_switch_cli_default_on_and_flag_off():
    from tools.train.v3_6.train_v36 import build_parser

    parser = build_parser()
    _add_s1_args(parser)
    assert parser.parse_args([]).cumulative_mask_retention is True
    assert parser.parse_args(["--no-cumulative-mask-retention"]).cumulative_mask_retention is False
