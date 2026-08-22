"""FLUED v3.6 S1.0: three-task trainer with fully separated decoder/backbone roles.

Tasks (spec section 20, user-designed):
1. direct (codec fidelity): decoder restores the AS-ENCODED byte sequence from
   the raw readout -- masked input means the target contains MASK_ID at masked
   positions. Pure translation, no inference.
2. backbone completion: readout -> backbone -> new matrix -> decoder restores
   the CLEAN text. Masked completion is ONLY scored on this path, so the
   backbone has an irreplaceable role (no more idling).
   v36.8 (S39 stage-0c recipe fix, user-ruled 2026-08-17): completion is
   CUMULATIVE -- row i restores the masked bytes of chunks 0..i (was: chunk i
   only), the first non-zero retention training signal for the state machine.
   ``--no-cumulative-mask-retention`` restores the old per-chunk targets.
3. backbone prediction: ``--predict-mode decode`` (v36.4+ default) decodes
   backbone_out[i] into chunk i+1's bytes through the FROZEN decoder
   (functional_call with detached params — gradients reach the backbone only,
   the decoder and shared byte table stay a fixed public ruler), plus a weak
   latent style anchor (MSE to decoder_in(content[i+1]).detach(), weight
   ``--predict-latent-weight``). Since v2.1 the predict branch consumes
   ``content.detach()``: predict CE trains the backbone only and can no longer
   deform the encoder/KDA compressed representation (E31: full-gradient v2.0
   collapsed the KDA state and destroyed the codec tasks).
   ``--predict-mode latent`` keeps the old pure-MSE behaviour for historical runs.
4. cloze retrieval receipt (v3.7 slm only, user-ruled 2026-08-17; spec note
   docs/versions/v3.7/FLUED_V3_7_CLOZE_TASK_20260817_CN.md): with probability
   ``--cloze-prob`` one bank passage (``--cloze-bank`` JSONL, the
   tools/data/mine_cloze_bank.py contract) is spliced into the window's first
   60% at a uniform UTF-8-snapped byte offset, and ``\n`` + query +
   ``\n答案是：`` + answer is appended at the window tail. The passage's
   answer span is force-UNMASKED (E23 discipline: the readback tests the
   retention of already-encoded content); the tail echo answer is force-MASKED
   (no copying from the window tail). Byte CE over the echo slots rides the
   SAME completion conditioning (decoder(backbone_out+pos)), weighted by
   ``--cloze-weight`` ON TOP of the three main tasks. Metrics: cloze_byte_acc
   / cloze_exact / cloze_count. Default off (``--cloze-prob 0.0`` = zero
   intrusion: the legacy path stays bitwise-identical). Motivation: E64/E66
   showed the three tasks put zero retrieval load on the K channel inside a
   4096B window; cloze makes "retrieve or lose points" part of the gradient.
5. natural retrieval (v3.7 slm only, recruitment arm prereg
   docs/versions/v3.7/FLUED_V3_7_RECRUITMENT_ARM_NATURAL_RETRIEVAL_20260821_CN.md):
   with probability ``--retrieval-prob`` one 32-64B in-window fragment is
   picked as the source span, one ASCII word W ([A-Za-z]{3,10}) inside it is
   blanked in a tail question (前文'...___...'空格处是什么？), and 答案是：W
   is appended as the echo. The source W is force-UNMASKED (it must enter
   the state -- that is the retrieval pressure), the echo is force-MASKED,
   byte CE on the echo slots rides the SAME completion conditioning, weighted
   by ``--retrieval-weight``. ``--retrieval-block-prob`` is the preregistered
   r (档 a 掩码级剔除): per spliced sample, the source fragment's store rows
   are excised (store_block) from every query position at/after the
   question's first chunk, so the answer reaches the question only through
   K->state->readout. Mutually exclusive with --cloze-prob>0 (同窗只允许一种
   检索任务). Default off (``--retrieval-prob 0.0`` = zero intrusion).

Metric redefinition (S1.0+): direct fidelity excludes nothing but MASK_ID
positions are reported separately (trivially correct); masked acc is backbone
only; prediction reported as predict_cos + sampled byte-level decode accuracy.

Mask modes (--mask-mode):
- ``byte_span``: legacy random 1-8B spans (kept for historical comparability).
- ``mixed`` (v36.3 default): 40% of the byte budget masks whole UTF-8 chars
  (1-3 chars per span), 60% masks whole BPE words against the 128k reference
  tokenizer. Whole-char masking trains single-char understanding; whole-word
  masking tests semantic inference without letting the architecture collapse
  into a fancy BPE (word share is kept below half).

Protocol: from-scratch ablation (only S0 four prefixes loaded), same
data/seed/eval as canonical.

Strict codec-retention arm (``--codec-final-state``, user-ruled 2026-08-11,
prereg FLUED_TODO_20260805 §0.3 item 0): the three standard tasks never
required the KDA state machine to RETAIN past chunks (direct reads the fresh
S_i, completion restores chunk i from row i, predict is one-step detached), so
the retention training signal is exactly zero. This arm welds every bypass
shut: direct and completion both decode from ONE read of the final state
S_final (``KDAStateMachine.read_all_final``), the backbone is excluded from
the loss path, and the predict task is disabled (weight 0, not computed).
Eval adds an n-scan {1,4,8,last}: n uniformly subsampled query rows serve the
whole window (/n paging geometry), reporting full-window byte-restore acc.
Note: the "retention signal is exactly zero" diagnosis above describes the
pre-v36.8 recipe; v36.8 completion is cumulative (task 2), so the standard
recipe now carries a retention signal and this arm remains the strict
welded-shut reference.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
from argparse import Namespace
from pathlib import Path

import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import BYTE_OFFSET, MASK_ID, PAD_ID  # noqa: E402
from flued.v36.model import _xcache_select, chunk_byte_offsets, paged_boundaries  # noqa: E402
from tools.train.v3_3.train_v33 import (  # noqa: E402
    _append_jsonl,
    _cosine_with_warmup,
    _safe_acc,
    build_optimizer,
    make_byte_mask,
    make_dataloaders,
    make_targets,
)
from tools.train.v3_6.train_v36 import _ce, build_model  # noqa: E402

# ---------------------------------------------------------------------------
# Mixed char/BPE-word masking (v36.3, T3)
# ---------------------------------------------------------------------------

# Module-level so the non-serializable tokenizer never lands in vars(args)
# (resolved_config.json / summary.json dump the full args namespace).
_BPE_TOKENIZER = None
# Dedicated CPU generator: evaluate() re-seeds it so the eval mask is
# deterministic regardless of dataset-RNG consumption order.
_MASK_GENERATOR = torch.Generator()

# ---------------------------------------------------------------------------
# cloze 检索回执 (v3.7 slm-only 4th task, user-ruled 2026-08-17)
# ---------------------------------------------------------------------------

# Module-level so the bank never lands in vars(args) dumps (same discipline as
# _BPE_TOKENIZER); only the path string lives in args.
_CLOZE_BANK = None
# Dedicated CPU generator (same discipline as _MASK_GENERATOR): main() seeds
# it from args.seed, evaluate() re-seeds it from args.eval_mask_seed, so eval
# splices are deterministic regardless of dataset/mask RNG consumption order.
# The offset decorrelates the cloze draw stream from the mask stream (same
# seed family, different stream).
_CLOZE_GENERATOR = torch.Generator()
_CLOZE_SEED_OFFSET = 101_003
_CLOZE_ECHO_PROMPT = "\n答案是：".encode("utf-8")


def _cloze_enabled(args) -> bool:
    return float(getattr(args, "cloze_prob", 0.0)) > 0.0


def _load_cloze_bank(path: str) -> int:
    """Load and contract-validate the cloze bank JSONL; returns entry count.

    Contract (tools/data/mine_cloze_bank.py, 勿改字段名): each line
    {"id", "passage", "answer", "query", "answer_bytes"} with answer_bytes =
    int, the answer's UTF-8 byte count; passage 96-192B; answer 28-36B;
    query == passage with the answer replaced by exactly one ``___``. The
    answer's byte span inside the passage is recovered from the query's blank
    position and cross-checked against the raw strings. Any violation raises
    ValueError with the line number (loud, never silent).
    """
    global _CLOZE_BANK
    resolved = Path(path)
    if not resolved.is_absolute():
        resolved = REPO_ROOT / resolved
    bank = []
    with resolved.open("r", encoding="utf-8") as fh:
        for ln, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            missing = {"id", "passage", "answer", "query", "answer_bytes"} - set(row)
            if missing:
                raise ValueError(f"cloze bank line {ln}: missing fields {sorted(missing)}")
            pb = row["passage"].encode("utf-8")
            ab = row["answer"].encode("utf-8")
            qb = row["query"].encode("utf-8")
            if row["answer_bytes"] != len(ab):
                raise ValueError(
                    f"cloze bank line {ln}: answer_bytes={row['answer_bytes']} != actual {len(ab)}"
                )
            if not (28 <= len(ab) <= 36):
                raise ValueError(f"cloze bank line {ln}: answer {len(ab)}B outside 28-36B")
            if not (96 <= len(pb) <= 192):
                raise ValueError(f"cloze bank line {ln}: passage {len(pb)}B outside 96-192B")
            if qb.count(b"___") != 1:
                raise ValueError(f"cloze bank line {ln}: query must contain exactly one '___' blank")
            lo = qb.find(b"___")
            if qb != pb[:lo] + b"___" + pb[lo + len(ab) :] or pb[lo : lo + len(ab)] != ab:
                raise ValueError(f"cloze bank line {ln}: query.replace('___', answer) != passage")
            bank.append({"id": row["id"], "passage_b": pb, "query_b": qb, "answer_b": ab, "ans_lo": lo})
    if not bank:
        raise ValueError(f"cloze bank empty: {resolved}")
    _CLOZE_BANK = bank
    return len(bank)


def _splice_cloze(clean: torch.Tensor, bank: list, prob: float, generator: torch.Generator):
    """Splice one cloze instance into each selected window (CPU, pre-encode).

    Per row, in a fixed draw order on ``generator`` (selection uniform, then
    bank index, then insertion offset): with probability ``prob`` insert the
    bank passage at a uniform byte offset inside the window's first 60%
    (snapped FORWARD to a UTF-8 char boundary) and append ``\\n`` + query +
    ``\\n答案是：`` + answer at the window tail. The batch tensor WIDENS past
    seq_len to hold the splice (the v3.7 front end carries no byte-level
    positional embedding, so a slightly wider window is legal; the chunk
    packer's capacity accounting is unchanged) -- the task counts only when
    the echo survives packing whole; ``_cloze_slot_grid`` enforces that skip
    rule (echo 必须在窗内才算数).

    Unselected rows stay byte-identical. Returns (new_clean, metas); metas[b]
    is None or {"echo_span": (lo, hi), "passage_answer_span": (lo, hi),
    "bank_id": int}.
    """
    bsz, width = clean.shape
    metas: list[dict | None] = [None] * bsz
    spliced: dict[int, bytes] = {}
    for b in range(bsz):
        ids = clean[b]
        valid = ids.ne(PAD_ID)
        n = int(valid.sum())
        u = float(torch.rand((), generator=generator))
        # defense: only prefix-valid rows are eligible (corpus windows always
        # are); ineligible rows keep their content byte-identical.
        if u >= prob or n == 0 or not bool(valid[:n].all()) or bool(valid[n:].any()):
            continue
        raw = bytes(int(i) - BYTE_OFFSET for i in ids[:n].tolist())
        entry = bank[int(torch.randint(len(bank), (1,), generator=generator))]
        max_off = int(0.6 * n)
        p = int(torch.randint(0, max_off + 1, (1,), generator=generator)) if max_off > 0 else 0
        while p < n and (raw[p] & 0xC0) == 0x80:
            p += 1
        new = raw[:p] + entry["passage_b"] + raw[p:] + b"\n" + entry["query_b"] + _CLOZE_ECHO_PROMPT + entry["answer_b"]
        echo_lo = len(new) - len(entry["answer_b"])
        ans_lo = p + entry["ans_lo"]
        metas[b] = {
            "echo_span": (echo_lo, len(new)),
            "passage_answer_span": (ans_lo, ans_lo + len(entry["answer_b"])),
            "bank_id": entry["id"],
        }
        spliced[b] = new
    out = clean
    if spliced:
        new_width = max([width] + [len(r) for r in spliced.values()])
        out = clean.new_full((bsz, new_width), PAD_ID)
        out[:, :width] = clean
        for b, r in spliced.items():
            out[b] = PAD_ID
            out[b, : len(r)] = torch.tensor([x + BYTE_OFFSET for x in r], dtype=clean.dtype)
    return out, metas


def _cloze_mask_overrides(byte_mask: torch.Tensor, metas: list) -> torch.Tensor:
    """E23 discipline, applied AFTER the regular mask: the passage's answer
    span is force-UNMASKED (the readback tests the retention of
    already-encoded content); the tail echo answer is force-MASKED (no copying
    the answer from the window tail)."""
    for b, m in enumerate(metas):
        if m is None:
            continue
        lo, hi = m["passage_answer_span"]
        byte_mask[b, lo:hi] = False
        lo, hi = m["echo_span"]
        byte_mask[b, lo:hi] = True
    return byte_mask


def _cloze_slot_grid(metas: list, chunk_ids: torch.Tensor, offsets: torch.Tensor, max_chunks: int, max_span: int):
    """Map each sample's echo bytes through the chunk packing into the (B, C,
    S) completion grid. A sample counts (active) only when EVERY echo byte
    lands on a valid (chunk, slot) cell -- echo 必须在窗内/网格内才算数;
    capacity-truncated samples skip the task (cloze_count=0) but keep their
    spliced content for the three main tasks."""
    bsz = chunk_ids.size(0)
    device = chunk_ids.device
    slot = torch.zeros((bsz, max_chunks, max_span), dtype=torch.bool, device=device)
    active = torch.zeros(bsz, dtype=torch.bool, device=device)
    for b, m in enumerate(metas):
        if m is None:
            continue
        lo, hi = m["echo_span"]
        if hi > chunk_ids.size(1):
            continue
        t = torch.arange(lo, hi, device=device)
        j = chunk_ids[b, t]
        s = offsets[b, t]
        ok = j.ge(0) & j.lt(max_chunks) & s.ge(0) & s.lt(max_span)
        if not bool(ok.all()):
            continue
        slot[b, j, s] = True
        active[b] = True
    return slot, active


def _cloze_loss_and_metrics(logits_backbone: torch.Tensor, comp_targets: torch.Tensor, cloze_slot: torch.Tensor, active: torch.Tensor):
    """Byte CE over the echo slots on the SAME completion conditioning as the
    masked completion task (decoder(backbone_out+pos) logits), plus the
    train_log metrics: byte accuracy over echo slots; exact = whole answer
    right (mean over active samples); count = batch hit rate."""
    cloze_loss = _ce(logits_backbone, comp_targets, cloze_slot)
    pred = logits_backbone.argmax(dim=-1)
    hit = pred.eq(comp_targets) & cloze_slot
    byte_acc = hit.float().sum() / cloze_slot.float().sum().clamp(min=1.0)
    exact_per = (hit | ~cloze_slot).flatten(1).all(dim=1) & active
    exact = exact_per.float().sum() / active.float().sum().clamp(min=1.0)
    return cloze_loss, {
        "cloze_byte_acc": byte_acc.detach(),
        "cloze_exact": exact.detach(),
        "cloze_count": active.float().mean().detach(),
    }


# ---------------------------------------------------------------------------
# 自然检索任务 (v3.7 slm-only 5th task, recruitment arm prereg 2026-08-21:
# docs/versions/v3.7/FLUED_V3_7_RECRUITMENT_ARM_NATURAL_RETRIEVAL_20260821_CN.md)
# ---------------------------------------------------------------------------

# Dedicated CPU generator (same discipline as _CLOZE_GENERATOR): main() seeds
# it from args.seed, evaluate() re-seeds it from args.eval_mask_seed, so eval
# splices/block draws are deterministic regardless of dataset/mask RNG
# consumption order. The offset decorrelates the retrieval draw stream from
# the mask and cloze streams (same seed family, different stream).
_RETRIEVAL_GENERATOR = torch.Generator()
_RETRIEVAL_SEED_OFFSET = 101_009
_RETRIEVAL_QUERY_PRE = "\n前文'".encode("utf-8")
_RETRIEVAL_QUERY_POST = "'空格处是什么？".encode("utf-8")
_RETRIEVAL_ECHO_PROMPT = "\n答案是：".encode("utf-8")
_ASCII_WORD_RE = re.compile(rb"[A-Za-z]+")
# Q11 v2 (user-ruled 2026-08-21): CJK small-segment main arm. Frozen values
# from the prereg amendment: retry cap N=8 and the punctuation boundary set
# (appendix A of FLUED_V3_7_RECRUITMENT_ARM_NATURAL_RETRIEVAL_20260821_CN.md).
_RETRIEVAL_MAX_RETRY = 8
_BOUNDARY_CHARS = frozenset(
    "。，、；：？！“”‘’（）《》〈〉【】〔〕「」『』…—～・｜＂＇"
    ".,;:?!\"'()[]{}<>/\\|@#$%^&*_+=~`-"
    " \t\n\r\u3000\u00a0"
)


def _cjk_candidates(frag: bytes) -> list[tuple[int, int]]:
    """Byte-offset (start, end) pairs of qualifying CJK small segments: every
    2–4 char substring of a maximal non-boundary-char run (v2 §1: edges never
    punctuation/whitespace, never crossing a boundary char; digits/letters
    allowed inside). Decode-for-selection only; splicing stays byte-level."""
    try:
        s = frag.decode("utf-8")
    except UnicodeDecodeError:
        return []
    offs = [0]
    for ch in s:
        offs.append(offs[-1] + len(ch.encode("utf-8")))
    runs: list[tuple[int, int]] = []
    start = None
    for i, ch in enumerate(s):
        if ch in _BOUNDARY_CHARS:
            if start is not None:
                runs.append((start, i))
                start = None
        elif start is None:
            start = i
    if start is not None:
        runs.append((start, len(s)))
    cands = []
    for lo, hi in runs:
        for L in (2, 3, 4):
            for j in range(lo, hi - L + 1):
                cands.append((offs[j], offs[j + L]))
    return cands


def _retrieval_enabled(args) -> bool:
    return float(getattr(args, "retrieval_prob", 0.0)) > 0.0


def _check_retrieval_args(args) -> None:
    """Loud CLI validation for the natural retrieval task (recruitment arm):
    r out of [0, 1] is always an error; a live task is slm-only and mutually
    exclusive with cloze (同窗只允许一种检索任务)."""
    r = float(getattr(args, "retrieval_block_prob", 0.0))
    if not 0.0 <= r <= 1.0:
        raise SystemExit(
            f"--retrieval-block-prob must lie in [0, 1] (档 a 掩码剔除比例 r, got {r})"
        )
    if not _retrieval_enabled(args):
        return
    if getattr(args, "backbone_mode", "") != "slm":
        raise SystemExit(
            "--retrieval-prob>0 requires --backbone-mode slm (v3.7 自然检索任务, 招募臂 "
            "prereg 2026-08-21); xattn/paged/draft/attn paths and "
            "codec_final/paged/draft/prefix_task combinations are N/A"
        )
    if float(getattr(args, "cloze_prob", 0.0)) > 0:
        raise SystemExit(
            "--retrieval-prob>0 and --cloze-prob>0 are mutually exclusive "
            "(同窗只允许一种检索任务)"
        )


def _splice_retrieval(clean: torch.Tensor, prob: float, generator: torch.Generator, answer_mode: str = "cjk"):
    """Splice one natural-retrieval instance into each selected window (CPU,
    pre-encode). Same splicing discipline as ``_splice_cloze``.

    Per row, in a fixed draw order on ``generator`` (selection uniform, then
    per-attempt: fragment length, fragment start, candidate index): with
    probability ``prob`` try up to ``_RETRIEVAL_MAX_RETRY`` (N=8, v2 frozen)
    fragment draws -- pick a 32-64B contiguous in-window fragment F (start
    uniform, snapped FORWARD to a UTF-8 char boundary, end snapped BACKWARD),
    then pick the answer segment inside F uniformly among the mode's
    candidates: ``cjk`` (v2 main arm) = 2–4 char substrings of maximal
    non-boundary runs (_cjk_candidates); ``ascii`` (v2 control arm) = maximal
    [A-Za-z]{3,10} runs. Append at the window tail ``\\n前文'`` + F with the
    answer replaced by ``___`` + ``'空格处是什么？`` + ``\\n答案是：`` +
    answer. The batch tensor WIDENS past seq_len (same legality as cloze).

    Rows still without a candidate after N retries stay byte-identical and
    inactive (draws consumed, splice skipped; counted in the activation
    rate). Returns (new_clean, metas); metas[b] is None or
    {"source_span": (lo, hi), "source_answer_span": (lo, hi),
    "query_start": int, "echo_span": (lo, hi), "answer_b": bytes}.
    """
    bsz, width = clean.shape
    metas: list[dict | None] = [None] * bsz
    spliced: dict[int, bytes] = {}
    for b in range(bsz):
        ids = clean[b]
        valid = ids.ne(PAD_ID)
        n = int(valid.sum())
        u = float(torch.rand((), generator=generator))
        # defense: only prefix-valid rows are eligible (same as cloze);
        # ineligible rows keep their content byte-identical.
        if u >= prob or n < 32 or not bool(valid[:n].all()) or bool(valid[n:].any()):
            continue
        raw = bytes(int(i) - BYTE_OFFSET for i in ids[:n].tolist())
        picked = None
        for _attempt in range(_RETRIEVAL_MAX_RETRY):
            frag_len = int(torch.randint(32, min(64, n) + 1, (1,), generator=generator))
            start = int(torch.randint(0, n - frag_len + 1, (1,), generator=generator))
            # UTF-8 snap: start forward to a char boundary, end backward
            while start < n and (raw[start] & 0xC0) == 0x80:
                start += 1
            end = min(start + frag_len, n)
            while end > start and end < n and (raw[end] & 0xC0) == 0x80:
                end -= 1
            frag = raw[start:end]
            if answer_mode == "cjk":
                cands = _cjk_candidates(frag)
            else:
                cands = [(m.start(), m.end()) for m in _ASCII_WORD_RE.finditer(frag) if 3 <= m.end() - m.start() <= 10]
            if not cands:
                continue
            ci = int(torch.randint(len(cands), (1,), generator=generator))
            picked = (start, end, frag, cands[ci])
            break
        if picked is None:
            continue  # N retries exhausted: inactive (counted in activation rate)
        start, end, frag, (a_lo, a_hi) = picked
        answer = frag[a_lo:a_hi]
        tail = (
            _RETRIEVAL_QUERY_PRE
            + frag[:a_lo]
            + b"___"
            + frag[a_hi:]
            + _RETRIEVAL_QUERY_POST
            + _RETRIEVAL_ECHO_PROMPT
            + answer
        )
        new = raw + tail
        echo_lo = len(new) - len(answer)
        metas[b] = {
            "source_span": (start, end),
            "source_answer_span": (start + a_lo, start + a_hi),
            "query_start": n,  # the tail starts at the original window end
            "echo_span": (echo_lo, len(new)),
            "answer_b": answer,
        }
        spliced[b] = new
    out = clean
    if spliced:
        new_width = max([width] + [len(r) for r in spliced.values()])
        out = clean.new_full((bsz, new_width), PAD_ID)
        out[:, :width] = clean
        for b, r in spliced.items():
            out[b] = PAD_ID
            out[b, : len(r)] = torch.tensor([x + BYTE_OFFSET for x in r], dtype=clean.dtype)
    return out, metas


def _retrieval_mask_overrides(byte_mask: torch.Tensor, metas: list) -> torch.Tensor:
    """E23 discipline, applied AFTER the regular mask (same form as cloze):
    the tail echo answer is force-MASKED (no copying the answer from the
    window tail); the source fragment's answer word W is force-UNMASKED --
    W must be encoded into the state, it is the retrieval pressure's whole
    point. Everything else (the rest of the source fragment included) keeps
    the regular mask."""
    for b, m in enumerate(metas):
        if m is None:
            continue
        lo, hi = m["source_answer_span"]
        byte_mask[b, lo:hi] = False
        lo, hi = m["echo_span"]
        byte_mask[b, lo:hi] = True
    return byte_mask


def _retrieval_store_block(metas: list, chunks, block_prob: float, generator: torch.Generator):
    """档 a 掩码级剔除 (prereg §1/§4): per spliced sample drawn by
    ``block_prob`` (the preregistered r), excise the store rows covering the
    source fragment from every query position at/after the question's first
    chunk -- the answer then reaches the question only through
    K->state->readout (the direct path is per-chunk leak-free by
    construction, so the SLM block1 store rows are the only bypass).

    Byte->chunk mapping reuses the packing grid (chunk_ids, make_targets
    style). Returns (store_block_or_None, block_rate); None when no sample is
    both spliced and drawn (zero-cost legacy path). The r draw is consumed
    for EVERY spliced row in fixed order, so the draw stream is independent
    of the r value itself.
    """
    chunk_ids = chunks.chunk_ids
    n_chunks = chunks.chunk_mask.size(1)
    block = None
    n_spliced = 0
    n_blocked = 0
    for b, m in enumerate(metas):
        if m is None:
            continue
        n_spliced += 1
        u = float(torch.rand((), generator=generator))
        if u >= block_prob:
            continue
        lo, hi = m["source_span"]
        src_chunks = torch.unique(chunk_ids[b, lo:hi])
        src_chunks = src_chunks[src_chunks.ge(0)]
        if src_chunks.numel() == 0:
            continue  # fragment never packed (capacity) -- nothing to excise
        tail = chunk_ids[b, m["query_start"] :]
        q_chunks = tail[tail.ge(0)]
        if q_chunks.numel() == 0:
            continue  # question truncated out of the grid -- no query to block
        qc = int(q_chunks[0])  # chunks are byte-ordered: first valid = question head
        if block is None:
            block = torch.zeros(
                chunk_ids.size(0), n_chunks, n_chunks, dtype=torch.bool, device=chunk_ids.device
            )
        block[b, qc:, src_chunks] = True
        n_blocked += 1
    block_rate = n_blocked / n_spliced if n_spliced else 0.0
    return block, block_rate


def _ascii_casefold(ids: torch.Tensor) -> torch.Tensor:
    """ASCII case-fold on PAD-offset byte ids (A-Z -> a-z; everything else,
    PAD/MASK/multibyte included, untouched)."""
    b = ids - BYTE_OFFSET
    return torch.where((b >= 65) & (b <= 90), b + 32, b)


def _retrieval_loss_and_metrics(logits_backbone: torch.Tensor, comp_targets: torch.Tensor, retrieval_slot: torch.Tensor, active: torch.Tensor):
    """Byte CE over the echo slots on the SAME completion conditioning as the
    masked completion task (same form as ``_cloze_loss_and_metrics``; the
    slot grid itself is ``_cloze_slot_grid``, the meta contract is
    compatible). exact = normalized exact match (prereg §3 答案计分口径:
    大小写/空白归一、全词命中) -- the echo span holds exactly the answer
    word's bytes ([A-Za-z]{3,10}, no whitespace by construction), so ASCII
    case-folding is the whole normalization. count = batch hit rate."""
    retrieval_loss = _ce(logits_backbone, comp_targets, retrieval_slot)
    pred = logits_backbone.argmax(dim=-1)
    hit = pred.eq(comp_targets) & retrieval_slot
    byte_acc = hit.float().sum() / retrieval_slot.float().sum().clamp(min=1.0)
    hit_norm = _ascii_casefold(pred).eq(_ascii_casefold(comp_targets)) & retrieval_slot
    exact_per = (hit_norm | ~retrieval_slot).flatten(1).all(dim=1) & active
    exact = exact_per.float().sum() / active.float().sum().clamp(min=1.0)
    return retrieval_loss, {
        "retrieval_byte_acc": byte_acc.detach(),
        "retrieval_exact": exact.detach(),
        "retrieval_count": active.float().mean().detach(),
    }


def _load_bpe_tokenizer(path: str) -> None:
    global _BPE_TOKENIZER
    from tokenizers import Tokenizer

    resolved = Path(path)
    if not resolved.is_absolute():
        resolved = REPO_ROOT / resolved
    _BPE_TOKENIZER = Tokenizer.from_file(str(resolved))


def _utf8_char_spans(bs: bytes) -> list:
    """Whole-UTF-8-char byte spans: continuation bytes (0b10xxxxxx) never start a char."""
    starts = [i for i, b in enumerate(bs) if (b & 0xC0) != 0x80]
    starts.append(len(bs))
    return [(starts[i], starts[i + 1]) for i in range(len(starts) - 1)]


def _bpe_word_spans(bs: bytes, tokenizer) -> list:
    """Whole-BPE-word byte spans against the reference tokenizer.

    Returns [] when the window is not valid UTF-8 (streaming windows can cut
    mid-char at the edges); the caller then folds the word budget into chars.
    """
    try:
        text = bs.decode("utf-8")
    except UnicodeDecodeError:
        return []
    byte_offsets = [0]
    for ch in text:
        byte_offsets.append(byte_offsets[-1] + len(ch.encode("utf-8")))
    spans = []
    max_char = len(byte_offsets) - 1
    for c0, c1 in tokenizer.encode(text, add_special_tokens=False).offsets:
        # guard: offsets must stay inside the char->byte map (a normalizer
        # changing text length would break this mapping; ours has none)
        if c1 > c0 and 0 <= c0 and c1 <= max_char:
            spans.append((byte_offsets[c0], byte_offsets[c1]))
    return spans


def make_mixed_mask(
    clean: torch.Tensor,
    mask_prob: float,
    char_frac: float = 0.4,
    char_span_max: int = 3,
    tokenizer=None,
    generator: torch.Generator | None = None,
) -> torch.Tensor:
    """40/60 mixed mask on CPU token ids (PAD-offset encoding).

    ``char_frac`` of the masked-byte budget goes to whole UTF-8 chars
    (1-``char_span_max`` chars per span), the rest to whole BPE words.
    Spans never overlap; positions beyond the valid length stay unmasked.
    """
    bsz, _seq_len = clean.shape
    mask = torch.zeros_like(clean, dtype=torch.bool)
    if mask_prob <= 0:
        return mask
    for b in range(bsz):
        ids = clean[b][clean[b].ne(PAD_ID)].tolist()
        if not ids:
            continue
        bs = bytes(i - BYTE_OFFSET for i in ids)
        n = len(bs)
        budget = float(mask_prob) * n
        word_budget = (1.0 - float(char_frac)) * budget
        char_budget = float(char_frac) * budget
        m = torch.zeros(n, dtype=torch.bool)
        word_spans = _bpe_word_spans(bs, tokenizer) if tokenizer is not None else []
        if word_spans:
            acc = 0.0
            for i in torch.randperm(len(word_spans), generator=generator).tolist():
                if acc >= word_budget:
                    break
                s, e = word_spans[i]
                if m[s:e].any():
                    continue
                m[s:e] = True
                acc += e - s
        else:
            char_budget += word_budget
        char_spans = _utf8_char_spans(bs)
        acc = 0.0
        trials = 0
        max_trials = max(8 * len(char_spans), 64)
        while acc < char_budget and trials < max_trials:
            trials += 1
            ci = int(torch.randint(len(char_spans), (1,), generator=generator))
            ln = int(torch.randint(1, int(char_span_max) + 1, (1,), generator=generator))
            s = char_spans[ci][0]
            e = char_spans[min(ci + ln, len(char_spans)) - 1][1]
            if m[s:e].any():
                continue
            m[s:e] = True
            acc += e - s
        mask[b, :n] = m
    return mask


def _prev_ids(tgts: torch.Tensor) -> torch.Tensor:
    """Teacher-forced previous-byte ids over the flattened (B, C*span) grid;
    258 = window-start sentinel (DSpark Markov head, decoder_markov>0)."""
    bsz = tgts.size(0)
    flat = tgts.reshape(bsz, -1)
    prev = torch.cat(
        [torch.full((bsz, 1), 258, dtype=tgts.dtype, device=tgts.device), flat[:, :-1]], dim=1
    )
    return prev.reshape(tgts.shape).clamp(min=0, max=258)


def make_cumulative_retention_targets(
    clean: torch.Tensor,
    byte_mask: torch.Tensor,
    chunk_ids: torch.Tensor,
    offsets: torch.Tensor,
    max_chunks: int,
    max_span: int,
):
    """Cumulative-retention completion targets (S39 stage-0c recipe fix,
    user-ruled 2026-08-17, prereg S39_STAGED_MATRIX_PLAN §4 阶段0c).

    Row i restores the masked bytes of chunks 0..i instead of chunk i only,
    so the state machine / backbone receive a non-zero RETENTION gradient
    (the pre-v36.8 per-chunk layout required nothing to survive past a
    chunk's own read -- the three tasks' retention signal was exactly zero).

    Layout (minimal-invasion): the base per-chunk grid from ``make_targets``
    is kept verbatim -- chunk i's own bytes stay at their natural slots, and
    the masked bytes of chunks 0..i-1 are appended in byte order right after
    row i's last occupied slot. The decoder is a parallel slot decoder (slot
    embedding + chunk conditioning, no autoregression), so extra target slots
    need no architectural change and the (B, C, max_span) layout is
    unchanged. Trade-off: a row's target count grows with i and can exceed
    ``max_span``; overflow drops the appended tail (oldest masked bytes keep
    their slots) and is counted in the returned truncation counter. Unmasked
    bytes of earlier chunks never enter row i's target -- only bytes that
    never entered the state (masked) must be recalled from it.

    Returns (targets, slot_mask, masked_slot, n_truncated) with base-grid
    semantics: slot_mask marks every scored slot, masked_slot the subset that
    was masked in the source (own masked + recalled masked).
    """
    targets, slot_mask, masked_slot = make_targets(
        clean, byte_mask, chunk_ids, offsets, max_chunks, max_span
    )
    valid_byte = (
        chunk_ids.ge(0)
        & chunk_ids.lt(max_chunks)
        & offsets.ge(0)
        & offsets.lt(max_span)
        & clean.ne(PAD_ID)
    )
    m = byte_mask & valid_byte
    if not bool(m.any()):
        return targets, slot_mask, masked_slot, torch.zeros((), device=clean.device)
    slot_idx = torch.arange(max_span, device=clean.device).view(1, 1, max_span)
    row_valid = slot_mask.any(dim=-1)  # (B, C) real chunk rows only
    # First slot after the row's own bytes (own offsets are 0-based contiguous
    # from chunk packing, so this equals the row's byte count).
    start = torch.where(slot_mask, slot_idx, torch.full_like(slot_idx, -1)).amax(dim=-1) + 1  # (B, C)
    # rank of each masked byte among the sample's masked bytes, in byte order
    rank = m.long().cumsum(dim=1) - m.long()  # (B, T), strictly-before count
    b_idx, t_idx = m.nonzero(as_tuple=True)  # (M,) masked byte positions
    c_t = chunk_ids[b_idx, t_idx]
    r_t = rank[b_idx, t_idx]
    rows = torch.arange(max_chunks, device=clean.device).view(1, -1)  # (1, C)
    # A masked byte of chunk c enters every REAL row i > c (row i already
    # carries chunk i's own masked bytes in the base grid). Row i's appended
    # set is exactly {masked bytes of chunks 0..i-1} in byte order because
    # chunks are contiguous: rank over all masked bytes equals rank within
    # chunks < i for any byte of a chunk < i.
    dest_ok = rows.gt(c_t.view(-1, 1)) & row_valid[b_idx]  # (M, C)
    dest_slot = start[b_idx] + r_t.view(-1, 1)  # (M, C)
    fits = dest_ok & dest_slot.lt(max_span)
    flat = (b_idx.view(-1, 1) * max_chunks + rows) * max_span + dest_slot  # (M, C)
    sel = fits.reshape(-1)
    flat_sel = flat.reshape(-1)[sel]
    vals = clean[b_idx, t_idx].view(-1, 1).expand(-1, max_chunks).reshape(-1)[sel]
    # (row, rank) pairs are unique, so scatter cannot collide.
    targets.view(-1).scatter_(0, flat_sel, vals)
    ones = torch.ones_like(flat_sel, dtype=torch.bool)
    slot_mask.view(-1).scatter_(0, flat_sel, ones)
    masked_slot.view(-1).scatter_(0, flat_sel, ones)
    n_truncated = (dest_ok & dest_slot.ge(max_span)).sum()
    return targets, slot_mask, masked_slot, n_truncated


def _completion_target_grids(
    clean: torch.Tensor,
    byte_mask: torch.Tensor,
    chunk_ids: torch.Tensor,
    offsets: torch.Tensor,
    max_chunks: int,
    max_span: int,
    cumulative: bool,
):
    """Completion-task target grids: cumulative mask retention (v36.8
    default) or the pre-v36.8 per-chunk layout (``--no-cumulative-mask-retention``
    ablation). Direct/predict keep the per-chunk base grids either way."""
    if cumulative:
        return make_cumulative_retention_targets(
            clean, byte_mask, chunk_ids, offsets, max_chunks, max_span
        )
    targets, slot_mask, masked_slot = make_targets(
        clean, byte_mask, chunk_ids, offsets, max_chunks, max_span
    )
    return targets, slot_mask, masked_slot, torch.zeros((), device=clean.device)


def s1_forward(model, source: torch.Tensor, args, clean=None, byte_mask=None, retrieval_metas=None) -> dict:
    codec_final = getattr(args, "codec_final_state", False)
    if getattr(model.config, "backbone_mode", "") == "slm":
        # v3.7 (consensus §1-2): dedicated branch. codec_final / paged / draft
        # / prefix combinations are N/A in the new mode and rejected loudly
        # (no silent mismatches); paged/draft are mutually exclusive
        # backbone_mode values by construction.
        if codec_final:
            raise ValueError(
                "codec_final_state is N/A for backbone_mode='slm' (v3.7: the state "
                "machine is an optional per-channel interpreter, not the pipeline "
                "keystone this arm welds shut)"
            )
        return _slm_forward(
            model, source, args, clean=clean, byte_mask=byte_mask, retrieval_metas=retrieval_metas
        )
    if retrieval_metas is not None:
        raise ValueError(
            "retrieval (--retrieval-prob>0) requires backbone_mode='slm' (v3.7 自然检索任务); "
            "legacy xattn/paged/draft/attn paths are N/A"
        )
    byte_states, confidence, valid, _ = model._encode(source)
    hard_cut, utf8_cont, cut_overflow = model._cuts(source, confidence, valid)
    chunks = model.chunk_builder(byte_states, valid, hard_cut, confidence)
    chunks = model.bridge(chunks, byte_states, confidence, valid, utf8_cont)
    memory = model.summarizer(chunks.span_embeddings, chunks.token_mask)
    gates = model.write_head(memory)
    if codec_final:
        # Strict codec-retention arm (user-ruled 2026-08-11): ONE read of the
        # final state S_final serves every chunk row of the window -- the
        # fresh per-chunk reads of S_i are welded shut, so the codec losses
        # train retention directly. Per-chunk rows differ only through the
        # position embedding added below (the "/n query row" identity).
        package_final, state_norm = model.state_machine.read_all_final(gates, chunks.chunk_mask)
        n_chunks = chunks.chunk_mask.size(1)
        content = package_final.mean(dim=1).unsqueeze(1).expand(-1, n_chunks, -1)  # (B, C, d_pack)
    else:
        package, state_norm = model.state_machine(gates, chunks.chunk_mask)
        if not model.config.per_chunk_readout:
            raise ValueError("S1.0 requires per_chunk_readout=True")
        content = package.mean(dim=2)  # (B, C, d_pack) — readout of S_i per chunk
    n_chunks = chunks.chunk_mask.size(1)
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_chunks]
    cond_direct = model.decoder_in(content) + pos
    logits_direct = None
    if codec_final:
        # Backbone excluded from the loss path: the xattn backbone reads
        # pre-state memory (a state-machine bypass), and this arm exists to
        # examine the state machine itself. Completion decodes from the SAME
        # final-state conditioning as direct -- two target views (as-encoded
        # vs clean) of one codec head. Predict is disabled in step_model.
        cond_backbone = cond_direct
        backbone_out = content  # metrics plumbing only
    elif getattr(model.config, "backbone_mode", "attn") == "paged_xattn":
        # S37 (spec SS24, user-proposed): page gists + per-page residual cache
        # rows; entry-level causal attention; each chunk is conditioned on its
        # page's output row (one-shot entry backbone, no iterative loop).
        boundary, serve = paged_boundaries(chunks.chunk_mask, model.config.paged_reads)
        reads = content.gather(1, boundary.unsqueeze(-1).expand(-1, -1, content.size(-1)))
        n_pages = boundary.size(1)
        page_pos = model.chunk_pos.weight[boundary]  # (B, n, d_bb) page-index embedding
        if clean is None or byte_mask is None:
            raise ValueError("paged_xattn requires clean+byte_mask (S1 trainer passes them)")
        logits_direct = model.decoder(cond_direct, chunks.token_mask)
        targets_r, slot_mask_r, _ = make_targets(
            clean, byte_mask, chunks.chunk_ids, chunks.offsets, args.max_chunks, args.max_span
        )
        ce = F.cross_entropy(
            logits_direct.float().reshape(-1, logits_direct.size(-1)),
            targets_r.reshape(-1).clamp(min=0, max=257),
            reduction="none",
            ignore_index=PAD_ID,
        ).reshape(targets_r.shape)
        resid = (ce * slot_mask_r.float()).sum(dim=-1) / slot_mask_r.float().sum(dim=-1).clamp(min=1.0)
        # per-page residual top-k (S37: the page's hardest chunks get exact rows)
        k_per = model.config.paged_cache_rows
        cgrid = torch.arange(chunks.chunk_mask.size(1), device=content.device).unsqueeze(0)
        cache_rows = []
        for p in range(n_pages):
            lo = boundary[:, p - 1] + 1 if p > 0 else torch.zeros_like(boundary[:, 0])
            hi = boundary[:, p]
            in_page = (cgrid >= lo.unsqueeze(1)) & (cgrid <= hi.unsqueeze(1)) & chunks.chunk_mask
            scores_p = resid.masked_fill(~in_page, float("-inf"))
            top = scores_p.topk(min(k_per, in_page.size(1)), dim=1).indices
            valid_p = scores_p.gather(1, top) > float("-inf") / 2
            cache_rows.append(torch.where(valid_p, top, torch.full_like(top, -1)))
        cache_idx = torch.cat(cache_rows, dim=1)  # (B, n*k_per)
        backbone_out = model.backbone(
            reads, memory, chunks.chunk_mask, page_pos,
            cache_idx=cache_idx, gist=reads, query_pos=boundary, gist_pos=boundary,
        )
        cond_backbone = backbone_out.gather(
            1, serve.unsqueeze(-1).expand(-1, -1, backbone_out.size(-1))
        ) + pos
    elif getattr(model.config, "backbone_mode", "attn") == "xattn":
        # causal cross-read backbone (s31): queries = per-chunk content,
        # K/V = pre-state memory, position i sees memory[0..i] only.
        # S36 (user-ruled 2026-08-08): optional k=1 gist token + residual-gated
        # cache (HOLA/HAM): keep only the top-frac memory rows ranked by
        # per-chunk direct-decode CE.
        cache_idx, gist = None, None
        if getattr(model.config, "xcache_gist", False) or getattr(model.config, "xcache_frac", 1.0) < 1.0:
            last = chunks.chunk_mask.long().sum(dim=1).clamp(min=1) - 1
            ar = torch.arange(content.size(0), device=content.device)
            gist = content[ar, last] if getattr(model.config, "xcache_gist", False) else None
            resid = None
            if getattr(model.config, "xcache_frac", 1.0) < 1.0:
                if clean is None or byte_mask is None:
                    raise ValueError("xcache_frac<1 requires clean+byte_mask (S1 trainer passes them)")
                logits_direct = model.decoder(cond_direct, chunks.token_mask)
                targets_r, slot_mask_r, _ = make_targets(
                    clean, byte_mask, chunks.chunk_ids, chunks.offsets, args.max_chunks, args.max_span
                )
                ce = F.cross_entropy(
                    logits_direct.float().reshape(-1, logits_direct.size(-1)),
                    targets_r.reshape(-1).clamp(min=0, max=257),
                    reduction="none",
                    ignore_index=PAD_ID,
                ).reshape(targets_r.shape)
                resid = (ce * slot_mask_r.float()).sum(dim=-1) / slot_mask_r.float().sum(dim=-1).clamp(min=1.0)
            cache_idx = _xcache_select(
                resid if resid is not None else chunks.chunk_mask.float(),
                chunks.chunk_mask,
                getattr(model.config, "xcache_frac", 1.0),
            )
        supp, supp_idx = None, None
        if getattr(model.config, "xcache_supp", 0) > 0:
            # S38: supplementary content-conditioned readouts for the top-N
            # hardest chunks NOT in the cache (decode-CE gated, CUIB pattern)
            if not getattr(model.config, "xcache_gist", False):
                raise ValueError("xcache_supp requires --xcache-gist (supp entries reuse the gist projections)")
            if resid is None:
                if clean is None or byte_mask is None:
                    raise ValueError("xcache_supp requires clean+byte_mask (S1 trainer passes them)")
                logits_direct = model.decoder(cond_direct, chunks.token_mask)
                targets_r, slot_mask_r, _ = make_targets(
                    clean, byte_mask, chunks.chunk_ids, chunks.offsets, args.max_chunks, args.max_span
                )
                ce = F.cross_entropy(
                    logits_direct.float().reshape(-1, logits_direct.size(-1)),
                    targets_r.reshape(-1).clamp(min=0, max=257),
                    reduction="none",
                    ignore_index=PAD_ID,
                ).reshape(targets_r.shape)
                resid = (ce * slot_mask_r.float()).sum(dim=-1) / slot_mask_r.float().sum(dim=-1).clamp(min=1.0)
            if getattr(model.config, "supp_source", "state") == "residual":
                # S38B: S' write weights from detached downstream decode CE
                # (CUIB gating: above-median failure writes harder)
                resid_nan = resid.masked_fill(~chunks.chunk_mask, float("nan"))
                med = resid_nan.nanmedian(dim=1, keepdim=True).values.nan_to_num(0.0)
                write_w = torch.sigmoid(
                    (resid - med) / getattr(model.config, "residual_gate_temp", 1.0)
                ).detach()
                supp = model.state_machine.read_residual(content, gates, chunks.chunk_mask, write_w)
            else:
                supp = model.state_machine.read_supplementary(content, gates, chunks.chunk_mask)
            cached = torch.zeros_like(chunks.chunk_mask)
            if cache_idx is not None:
                cached.scatter_(1, cache_idx.clamp(min=0), cache_idx >= 0)
            supp_scores = resid.masked_fill(~chunks.chunk_mask | cached, float("-inf"))
            n_supp = min(model.config.xcache_supp, supp_scores.size(1))
            top = supp_scores.topk(n_supp, dim=1).indices
            valid_s = supp_scores.gather(1, top) > float("-inf") / 2
            supp_idx = torch.where(valid_s, top, torch.full_like(top, -1)).sort(dim=1).values
        # S39 a+pos: window-relative per-chunk start byte offsets for the
        # position-injected keys (None = feature off)
        chunk_byte_off = (
            chunk_byte_offsets(chunks.token_mask)
            if getattr(model.config, "k_pos_inject", False)
            else None
        )
        backbone_out = model.backbone(content, memory, chunks.chunk_mask, pos, cache_idx, gist, supp=supp, supp_idx=supp_idx, chunk_byte_off=chunk_byte_off)
        cond_backbone = backbone_out + pos
    elif getattr(model.config, "backbone_mode", "attn") == "draft":
        # three-state drafting (spec SS23, user-ruled 2026-08-08): input = the
        # k=1 final readout; the DiT refines a fresh thinking matrix over T
        # rounds (unsupervised); the output matrix conditions each chunk row.
        last = chunks.chunk_mask.long().sum(dim=1).clamp(min=1) - 1
        ar = torch.arange(content.size(0), device=content.device)
        backbone_out, think_steps = model.backbone.think(
            content[ar, last], memory, chunks.chunk_mask, pos, content=content
        )
        cond_backbone = backbone_out + pos
    elif getattr(model.config, "backbone_readout", "per_chunk") == "final":
        # k=1 backbone interface (user-ruled 2026-08-06): the backbone consumes
        # ONLY the final state's readout (carries 0..C history through the
        # recurrence). Per-chunk readouts stay decoder-side, which is what
        # per-chunk conditioning was always for (task density, E23).
        last = chunks.chunk_mask.long().sum(dim=1).clamp(min=1) - 1
        ar = torch.arange(content.size(0), device=content.device)
        backbone_out = model.backbone(content[ar, last].unsqueeze(1))
        cond_backbone = backbone_out + pos
    elif getattr(model.config, "backbone_readout", "per_chunk") == "paged":
        # /n paging (user-ruled 2026-08-07): one state read per sub-page
        # boundary; chunk i is conditioned on the first read covering it.
        boundary, serve = paged_boundaries(chunks.chunk_mask, model.config.paged_reads)
        reads = content.gather(1, boundary.unsqueeze(-1).expand(-1, -1, content.size(-1)))
        paged_out = model.backbone(reads)
        backbone_out = paged_out
        cond_backbone = paged_out.gather(
            1, serve.unsqueeze(-1).expand(-1, -1, paged_out.size(-1))
        ) + pos
    else:
        backbone_out = model.backbone(content)
        cond_backbone = backbone_out + pos
    if logits_direct is None:
        logits_direct = model.decoder(cond_direct, chunks.token_mask)
    if codec_final:
        # one conditioning, one decode: direct and completion share the logits
        # tensor and differ only in targets (encoded vs clean) downstream
        logits_backbone = logits_direct
    else:
        logits_backbone = model.decoder(cond_backbone, chunks.token_mask)
    logits_backbone_mid = None
    if (
        getattr(model.config, "backbone_mode", "") == "draft"
        and getattr(model.config, "draft_intermediate_weight", 0.0) > 0
        and getattr(model.backbone, "last_intermediate", None) is not None
    ):
        # s35 supervised arm (LoopFormer-style short-trajectory CE): the
        # uniformly sampled intermediate thinking matrix also eats the
        # completion loss, so intermediate states are anchored without
        # per-step trajectory labels
        cond_mid = model.backbone.last_intermediate + pos
        logits_backbone_mid = model.decoder(cond_mid, chunks.token_mask)
    return {
        "logits_direct": logits_direct,
        "logits_backbone": logits_backbone,
        "logits_backbone_mid": logits_backbone_mid,
        "content": content,
        "backbone_out": backbone_out,
        "memory": memory,
        "think_steps": float(getattr(model.backbone, "last_steps", 0)),
        "chunks": chunks,
        "cut_overflow": cut_overflow,
        "state_norm": state_norm,
        "boundary_confidence_mean": confidence[valid].mean() if valid.any() else confidence.mean(),
        "hard_cut_fraction": hard_cut.float()[valid].mean() if valid.any() else hard_cut.float().mean(),
    }


def _slm_forward(model, source: torch.Tensor, args, clean=None, byte_mask=None, retrieval_metas=None) -> dict:
    """v3.7 slm branch (docs/versions/v3.7/FLUED_V3_7_ARCHITECTURE_CONSENSUS_20260817_CN.md).

    Codec full-coverage law (consensus §2): any content task's loss covers the
    full prefix 1..i -- the fine grids achieve it by per-chunk joint coverage
    (row j restores chunk j, no chunk exempt), the coarse grids by the
    cumulative retention layout (row i restores 0..i). The grid fracture is
    driven by v_row_source in step_model. Conditioning (§1.4): direct eats the
    decoder-aligned V source rows (fine: decoder_in_mem(memory); coarse:
    decoder_in(V~)), completion eats the backbone's output matrix (V^), and
    predict anchors the NEXT chunk's V source row (step_model).

    ``retrieval_metas`` (自然检索任务, recruitment arm): when given, the
    档 a store_block mask is built from the metas + chunk grid
    (``_retrieval_store_block``) and threaded into the backbone; the block
    rate rides out to step_model's metrics. None = bit-identical legacy.
    """
    byte_states, confidence, valid, _ = model._encode(source)
    hard_cut, utf8_cont, cut_overflow = model._cuts(source, confidence, valid)
    chunks = model.chunk_builder(byte_states, valid, hard_cut, confidence)
    chunks = model.bridge(chunks, byte_states, confidence, valid, utf8_cont)
    k_rows, v_rows, state_norm, memory, index, k_store, v_store = model._slm_store_rows(chunks, with_views=True)
    n_chunks = chunks.chunk_mask.size(1)
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_chunks]
    # a+pos arm: window-relative per-chunk start byte offsets (None = off)
    chunk_byte_off = (
        chunk_byte_offsets(chunks.token_mask) if getattr(model.config, "k_pos_inject", False) else None
    )
    store_block = None
    retrieval_block_rate = 0.0
    if retrieval_metas is not None:
        store_block, retrieval_block_rate = _retrieval_store_block(
            retrieval_metas, chunks, float(getattr(args, "retrieval_block_prob", 0.0)), _RETRIEVAL_GENERATOR
        )
    # fork 2: multi-view store rows when readout_views > 1 (classic rows otherwise)
    backbone_out = model.backbone(
        k_store if k_store is not None else k_rows,
        v_store if v_store is not None else v_rows,
        chunks.chunk_mask, pos, chunk_byte_off=chunk_byte_off,
        store_block=store_block,
    )
    cond_backbone = backbone_out + pos
    dec_in = model.decoder_in if model.config.v_row_source == "state" else model.decoder_in_mem
    cond_direct = dec_in(v_rows) + pos
    logits_direct = model.decoder(cond_direct, chunks.token_mask)
    logits_backbone = model.decoder(cond_backbone, chunks.token_mask)
    return {
        "logits_direct": logits_direct,
        "logits_backbone": logits_backbone,
        "logits_backbone_mid": None,
        "content": None,  # content channel retired in slm mode (consensus §4)
        "backbone_out": backbone_out,
        "v_rows": v_rows,  # decoder-side V source rows (the predict anchor, §1.4)
        "memory": memory,
        "index": index,  # summarizer K rows (resident key-geometry metrics, E80 补充 2)
        "retrieval_block_rate": retrieval_block_rate,  # 档 a excision hit rate (0.0 when off)
        "think_steps": 0.0,
        "chunks": chunks,
        "cut_overflow": cut_overflow,
        "state_norm": state_norm,
        "boundary_confidence_mean": confidence[valid].mean() if valid.any() else confidence.mean(),
        "hard_cut_fraction": hard_cut.float()[valid].mean() if valid.any() else hard_cut.float().mean(),
    }


@torch.no_grad()
def _key_geometry_metrics(model, out: dict, device) -> dict:
    """E80 补充 2 (user-ruled 2026-08-18): resident WriteHead key-geometry
    dashboard on the current training batch (slm mode only; legacy paths
    untouched). Per engaged state channel — V: write_head over the memory rows
    (bare names), K: write_head_k over the index rows (_k suffix) — report
    mu (mean off-diagonal |cos|), mu_max (worst pair), PR/n (Gram eigenvalue
    participation ratio over n_real, per-head pooled). Zero placeholders for
    absent channels (the a grid has no WriteHead). One scalar sync per step
    (n_real); metrics-only path, everything detached."""
    zero = torch.zeros((), device=device)
    res = {
        "key_mu": zero, "key_mu_max": zero.clone(), "key_pr": zero.clone(),
        "key_mu_k": zero.clone(), "key_mu_max_k": zero.clone(), "key_pr_k": zero.clone(),
    }
    chunks = out["chunks"]
    n_real = int(chunks.chunk_mask[0].sum())
    if n_real < 2:
        return res

    def stats(k: torch.Tensor):  # (B, C, H, hk) write keys (unit-norm rows)
        kr = k[0, :n_real].float()
        mus, mx, prs = [], [], []
        for h in range(kr.size(1)):
            kh = kr[:, h]
            G = kh @ kh.T
            off = G.abs()[~torch.eye(kh.size(0), dtype=torch.bool, device=kh.device)]
            eig = torch.linalg.eigvalsh(G).clamp(min=0.0)
            mus.append(off.mean())
            mx.append(off.max())
            prs.append(eig.sum() ** 2 / eig.square().sum().clamp(min=1e-12) / kh.size(0))
        return torch.stack(mus).mean().detach(), torch.stack(mx).max().detach(), torch.stack(prs).mean().detach()

    cfg = model.config
    # metrics run OUTSIDE the autocast region: the forward's rows are bf16
    # under amp; cast to fp32 before the (fp32-weight) WriteHead modules.
    if getattr(cfg, "v_row_source", "") == "state":
        gates = model.write_head(out["memory"].float())
        res["key_mu"], res["key_mu_max"], res["key_pr"] = stats(gates["k"])
    if getattr(cfg, "k_row_source", "") == "state":
        gates_k = model.write_head_k(out["index"].float())
        res["key_mu_k"], res["key_mu_max_k"], res["key_pr_k"] = stats(gates_k["k"])
    return res


def _acc_tensor(pred: torch.Tensor, target: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    """Sync-free accuracy as a GPU scalar tensor (0.0 on empty mask).

    Training-loop metrics stay on device and are only synced at log time;
    calling ``.item()``/``float()`` per step (~19 metrics) serializes the
    CPU/GPU pipeline and costs real throughput at small batch sizes.
    """
    m = mask.float()
    return (pred.eq(target).float() * m).sum() / m.sum().clamp(min=1.0)


def _frozen_decoder_logits(model, cond: torch.Tensor, token_mask: torch.Tensor) -> torch.Tensor:
    """Decoder forward with every parameter detached.

    Gradients flow into ``cond`` (the backbone path) but never into the
    decoder or the shared byte table: in predict-mode=decode the decoder is
    a fixed public ruler that the backbone must learn to write for.
    """
    from torch.func import functional_call

    params = {k: v.detach() for k, v in model.decoder.named_parameters()}
    buffers = {k: v for k, v in model.decoder.named_buffers()}
    # Checkpointing is incompatible with functional_call's param substitution
    # (backward recompute would see the live params) -- disable it for this call.
    model.decoder._ckpt_enabled = False
    try:
        return functional_call(model.decoder, (params, buffers), (cond, token_mask))
    finally:
        model.decoder._ckpt_enabled = True


def step_model(model, batch, args, device, train: bool):
    clean = batch[0]
    cloze_metas = None
    if _cloze_enabled(args):
        # v3.7 cloze 检索回执 (user-ruled 2026-08-17): slm-only; the legacy
        # xattn/paged/draft/attn paths and the codec_final/paged/draft/
        # prefix_task combinations are N/A and must fail loudly, not silently.
        if getattr(model.config, "backbone_mode", "") != "slm":
            raise ValueError(
                "cloze (--cloze-prob>0) requires backbone_mode='slm' (v3.7 检索回执); "
                "legacy xattn/paged/draft/attn paths are N/A"
            )
        if _CLOZE_BANK is None:
            raise ValueError(
                "cloze bank not loaded: main() loads --cloze-bank via "
                "_load_cloze_bank before training/eval"
            )
        clean, cloze_metas = _splice_cloze(clean, _CLOZE_BANK, float(args.cloze_prob), _CLOZE_GENERATOR)
    retrieval_metas = None
    if _retrieval_enabled(args):
        # v3.7 自然检索任务 (recruitment arm prereg 2026-08-21): slm-only; the
        # legacy xattn/paged/draft/attn paths and a simultaneously live cloze
        # task are N/A and must fail loudly, not silently.
        if getattr(model.config, "backbone_mode", "") != "slm":
            raise ValueError(
                "retrieval (--retrieval-prob>0) requires backbone_mode='slm' (v3.7 自然检索任务); "
                "legacy xattn/paged/draft/attn paths are N/A"
            )
        if cloze_metas is not None:
            raise ValueError(
                "retrieval (--retrieval-prob>0) and cloze (--cloze-prob>0) are mutually "
                "exclusive (同窗只允许一种检索任务)"
            )
        clean, retrieval_metas = _splice_retrieval(
            clean, float(args.retrieval_prob), _RETRIEVAL_GENERATOR,
            getattr(args, "retrieval_answer_mode", "cjk"),
        )
    clean = clean.to(device)
    valid = clean.ne(PAD_ID)
    if getattr(args, "mask_mode", "byte_span") == "mixed":
        byte_mask = make_mixed_mask(
            clean.cpu(),
            args.mask_prob,
            char_frac=args.mask_char_frac,
            char_span_max=args.mask_char_span_max,
            tokenizer=_BPE_TOKENIZER,
            generator=_MASK_GENERATOR,
        ).to(device)
    else:
        byte_mask = make_byte_mask(valid, args.mask_prob, args.mask_span_min, args.mask_span_max)
    if cloze_metas is not None:
        # E23 overrides AFTER the regular mask: passage answer force-unmasked,
        # tail echo force-masked (see _cloze_mask_overrides).
        byte_mask = _cloze_mask_overrides(byte_mask, cloze_metas)
    if retrieval_metas is not None:
        # same E23 form (see _retrieval_mask_overrides): source answer word
        # force-unmasked, tail echo force-masked.
        byte_mask = _retrieval_mask_overrides(byte_mask, retrieval_metas)
    source = clean.masked_fill(byte_mask, MASK_ID)
    with torch.autocast("cuda", dtype=torch.bfloat16, enabled=args.amp and device.type == "cuda"):
        out = s1_forward(model, source, args, clean=clean, byte_mask=byte_mask, retrieval_metas=retrieval_metas)
    chunks = out["chunks"]
    # Per-chunk base grids: direct (encoded) and predict views keep these.
    targets, slot_mask, masked_slot = make_targets(
        clean, byte_mask, chunks.chunk_ids, chunks.offsets, args.max_chunks, args.max_span
    )
    # v3.7 slm (consensus §2 codec full-coverage law): the target grids
    # fracture by V granularity -- fine V (memory rows) keeps the per-chunk
    # base grids (row j restores chunk j; the 1..i rows are jointly
    # supervised, no chunk exempt), coarse V (state readouts) uses the
    # cumulative retention grid (row i restores 0..i) for BOTH completion and
    # direct. The --cumulative-mask-retention flag governs the legacy xattn
    # path only; in slm mode the fracture is driven by v_row_source.
    slm_mode = getattr(model.config, "backbone_mode", "") == "slm"
    slm_coarse_v = slm_mode and getattr(model.config, "v_row_source", "memory") == "state"
    comp_cumulative = slm_coarse_v if slm_mode else getattr(args, "cumulative_mask_retention", True)
    comp_targets, comp_slot_mask, comp_masked_slot, retention_trunc = _completion_target_grids(
        clean,
        byte_mask,
        chunks.chunk_ids,
        chunks.offsets,
        args.max_chunks,
        args.max_span,
        comp_cumulative,
    )
    # as-encoded targets: the masked source itself (MASK_ID at masked slots)
    if slm_coarse_v:
        # coarse-V direct: cumulative as-encoded grid (row i restores the
        # as-encoded bytes of chunks 0..i; truncation counted together with
        # the completion side)
        encoded_targets, encoded_slot_mask, _m, direct_trunc = make_cumulative_retention_targets(
            source, byte_mask, chunks.chunk_ids, chunks.offsets, args.max_chunks, args.max_span
        )
        retention_trunc = retention_trunc + direct_trunc
    else:
        encoded_targets, encoded_slot_mask, _ = make_targets(
            source, torch.zeros_like(byte_mask), chunks.chunk_ids, chunks.offsets, args.max_chunks, args.max_span
        )
    unmasked_slot = comp_slot_mask & ~comp_masked_slot

    direct_loss = _ce(out["logits_direct"], encoded_targets, encoded_slot_mask)
    completion_loss = _ce(out["logits_backbone"], comp_targets, comp_slot_mask)
    if getattr(args, "decoder_markov", 0) > 0 and hasattr(model.decoder, "markov_out"):
        # DSpark Markov head (post-hoc on logits, teacher-forced prev byte):
        # NOTE this makes the metrics a teacher-forced protocol -- arms using
        # it are only comparable among themselves.
        b_d = model.decoder.markov_out(model.decoder.markov_embed(_prev_ids(encoded_targets)))
        b_b = model.decoder.markov_out(model.decoder.markov_embed(_prev_ids(comp_targets)))
        direct_loss = _ce(out["logits_direct"] + b_d, encoded_targets, encoded_slot_mask)
        completion_loss = _ce(out["logits_backbone"] + b_b, comp_targets, comp_slot_mask)
        out["logits_direct"] = out["logits_direct"] + b_d
        out["logits_backbone"] = out["logits_backbone"] + b_b
    if out.get("logits_backbone_mid") is not None:
        # s35 supervised arm: intermediate thinking matrix eats completion CE
        # (weight default 0.1, LoopFormer short-trajectory recipe)
        completion_loss = completion_loss + getattr(args, "draft_intermediate_weight", 0.1) * _ce(
            out["logits_backbone_mid"], comp_targets, comp_slot_mask
        )

    codec_final = getattr(args, "codec_final_state", False)
    if codec_final:
        # Predict task OFF in this arm (user-ruled 2026-08-11): it carries no
        # retention signal and would only muddy the variable set. Not computed
        # at all; zero metrics keep the log schema aligned with other arms.
        se = torch.zeros((), device=device)
        predict_cos = torch.zeros((), device=device)
        pair_mask = chunks.chunk_mask.new_ones((1,))  # placeholder, unused
    elif getattr(args, "backbone_mode", "") == "paged_xattn":
        # S37 page-level latent predict: the penultimate page's output row
        # predicts the last chunk's latent (chunk-level autoregression at
        # page granularity; the page row causally covers chunks < last)
        last = chunks.chunk_mask.long().sum(dim=1).clamp(min=2) - 1
        ar = torch.arange(out["content"].size(0), device=device)
        pred = out["backbone_out"][:, -2].float()
        with torch.no_grad():
            tgt = model.decoder_in(out["content"].float())[ar, last].detach()
        se = (pred - tgt).square().mean(dim=-1).mean()
        with torch.no_grad():
            predict_cos = F.cosine_similarity(pred, tgt, dim=-1).mean()
        pair_mask = chunks.chunk_mask.new_ones((1,))  # placeholder, unused
    elif getattr(args, "backbone_mode", "") == "draft":
        # predict rollout (spec SS23): a second thinking pass whose INPUT is
        # the penultimate readout S_{last-1} (causal to the target chunk);
        # arm B's memory view is truncated at last-1. The predict vector is
        # the mask-mean of the thinking rows (only the clean output is read).
        last = chunks.chunk_mask.long().sum(dim=1).clamp(min=2) - 1
        ar = torch.arange(out["content"].size(0), device=device)
        cidx = torch.arange(chunks.chunk_mask.size(1), device=device).unsqueeze(0)
        pmask = chunks.chunk_mask & (cidx <= (last - 1).unsqueeze(1))
        ppos = model.chunk_pos.weight.unsqueeze(0)[:, : chunks.chunk_mask.size(1)]
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=args.amp and device.type == "cuda"):
            pthink, _ = model.backbone.think(
                out["content"][ar, last - 1], out["memory"], pmask, ppos, content=out["content"]
            )
        pred = (pthink.float() * pmask.unsqueeze(-1)).sum(dim=1) / pmask.sum(dim=1, keepdim=True).clamp(min=1)
        with torch.no_grad():
            tgt = model.decoder_in(out["content"].float())[ar, last].detach()
        se = (pred - tgt).square().mean(dim=-1).mean()
        with torch.no_grad():
            predict_cos = F.cosine_similarity(pred, tgt, dim=-1).mean()
        pair_mask = chunks.chunk_mask.new_ones((1,))  # placeholder, unused in draft mode
    elif getattr(args, "backbone_readout", "per_chunk") in ("final", "paged"):
        # k=1 / paged: predict the LAST real chunk from the penultimate readout -- the
        # only in-window pair whose input still carries the full preceding
        # context through the state (chunk-level autoregression form).
        last = chunks.chunk_mask.long().sum(dim=1).clamp(min=2) - 1
        ar = torch.arange(out["content"].size(0), device=device)
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=args.amp and device.type == "cuda"):
            pred = model.backbone(out["content"][ar, last - 1].unsqueeze(1)).float().squeeze(1)
        with torch.no_grad():
            tgt = model.decoder_in(out["content"].float())[ar, last].detach()
        se = (pred - tgt).square().mean(dim=-1).mean()
        with torch.no_grad():
            predict_cos = F.cosine_similarity(pred, tgt, dim=-1).mean()
        pair_mask = chunks.chunk_mask.new_ones((1,))  # placeholder, unused in final mode
    elif getattr(model.config, "backbone_mode", "") == "slm":
        # v3.7 predict next chunk (consensus §1.4): backbone row i predicts
        # the NEXT chunk's V source row (decoder-side aligned, detached);
        # the old content-channel anchor is retired. predict_weight /
        # predict_mode semantics unchanged (latent MSE + predict_cos).
        # NB: model.config-driven, consistent with the s1_forward slm branch.
        if getattr(args, "predict_mode", "latent") == "decode":
            raise ValueError(
                "predict_mode='decode' is N/A for backbone_mode='slm' (the "
                "frozen-decoder CE form belongs to the xattn line; slm predict "
                "is latent next-chunk V anchoring)"
            )
        backbone_out = out["backbone_out"].float()
        pair_mask = (chunks.chunk_mask[:, :-1] & chunks.chunk_mask[:, 1:]).float()
        pred = backbone_out[:, :-1]
        with torch.no_grad():
            dec_in = (
                model.decoder_in
                if getattr(model.config, "v_row_source", "memory") == "state"
                else model.decoder_in_mem
            )
            tgt = dec_in(out["v_rows"].float())[:, 1:].detach()
        se = ((pred - tgt).square().mean(dim=-1) * pair_mask).sum() / pair_mask.sum().clamp(min=1.0)
        with torch.no_grad():
            cos = F.cosine_similarity(pred, tgt.float(), dim=-1)
            predict_cos = (cos * pair_mask).sum() / pair_mask.sum().clamp(min=1.0)
    else:
        backbone_out = out["backbone_out"].float()
        pair_mask = (chunks.chunk_mask[:, :-1] & chunks.chunk_mask[:, 1:]).float()
        pred = backbone_out[:, :-1]
        with torch.no_grad():
            tgt = model.decoder_in(out["content"].float())[:, 1:].detach()
        se = ((pred - tgt).square().mean(dim=-1) * pair_mask).sum() / pair_mask.sum().clamp(min=1.0)
        with torch.no_grad():
            cos = F.cosine_similarity(pred, tgt.float(), dim=-1)
            predict_cos = (cos * pair_mask).sum() / pair_mask.sum().clamp(min=1.0)

    predict_mode = getattr(args, "predict_mode", "latent")
    predict_ce = torch.zeros((), device=device)
    predict_byte_acc = torch.zeros((), device=device)
    if codec_final:
        predict_loss = torch.zeros((), device=device)
    elif predict_mode == "decode":
        # frozen-decoder supervision, v2.1: the predict branch consumes
        # content.detach() -- predict CE trains the BACKBONE ONLY. s13 (E31)
        # showed that letting this gradient reach the encoder/KDA side collapses
        # the state (norm 1.7->0.3) and destroys the codec tasks: the compressed
        # representation is owned by direct/completion, not by the predictor.
        pos = model.chunk_pos.weight.unsqueeze(0)[:, : chunks.chunk_mask.size(1)].float()
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=args.amp and device.type == "cuda"):
            backbone_pred = model.backbone(out["content"].detach())
        cond_pred = backbone_pred.float()[:, :-1] + pos[:, 1:]
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=args.amp and device.type == "cuda"):
            logits_pred = _frozen_decoder_logits(model, cond_pred, chunks.token_mask[:, 1:])
        pred_w = slot_mask[:, 1:] & pair_mask.unsqueeze(-1).bool()
        predict_ce = _ce(logits_pred, targets[:, 1:], pred_w)
        predict_byte_acc = _acc_tensor(logits_pred.argmax(dim=-1), targets[:, 1:], pred_w)
        predict_loss = predict_ce + args.predict_latent_weight * se
    else:
        predict_loss = se

    # cloze 检索回执 (v3.7 slm, user-ruled 2026-08-17): byte CE over the echo
    # slots on the SAME final completion logits as the masked completion task
    # (post-Markov-head, same form); the weight sits ON TOP of the three main
    # tasks (their weights are untouched). Zero placeholders keep the log
    # schema aligned when the task is off or no sample is active.
    cloze_loss = torch.zeros((), device=device)
    cloze_metrics = {
        "cloze_byte_acc": torch.zeros((), device=device),
        "cloze_exact": torch.zeros((), device=device),
        "cloze_count": torch.zeros((), device=device),
    }
    if cloze_metas is not None:
        cloze_slot, cloze_active = _cloze_slot_grid(
            cloze_metas, chunks.chunk_ids, chunks.offsets, args.max_chunks, args.max_span
        )
        cloze_loss, cloze_metrics = _cloze_loss_and_metrics(
            out["logits_backbone"], comp_targets, cloze_slot, cloze_active
        )

    # 自然检索任务 (v3.7 slm, recruitment arm prereg 2026-08-21): byte CE over
    # the echo slots on the SAME final completion logits as the masked
    # completion task (post-Markov-head, same form as cloze); the weight sits
    # ON TOP of the three main tasks (their weights are untouched). Zero
    # placeholders keep the log schema aligned when the task is off or no
    # sample is active.
    retrieval_loss = torch.zeros((), device=device)
    retrieval_metrics = {
        "retrieval_byte_acc": torch.zeros((), device=device),
        "retrieval_exact": torch.zeros((), device=device),
        "retrieval_count": torch.zeros((), device=device),
        "retrieval_block_rate": torch.zeros((), device=device),
    }
    if retrieval_metas is not None:
        retrieval_slot, retrieval_active = _cloze_slot_grid(
            retrieval_metas, chunks.chunk_ids, chunks.offsets, args.max_chunks, args.max_span
        )
        retrieval_loss, retrieval_metrics = _retrieval_loss_and_metrics(
            out["logits_backbone"], comp_targets, retrieval_slot, retrieval_active
        )
        retrieval_metrics["retrieval_block_rate"] = torch.tensor(
            out.get("retrieval_block_rate", 0.0), device=device
        )

    loss = (
        args.task1_loss_weight * direct_loss
        + args.task2_loss_weight * completion_loss
        + args.predict_weight * predict_loss
        + getattr(args, "cloze_weight", 0.3) * cloze_loss
        + getattr(args, "retrieval_weight", 1.0) * retrieval_loss
    )
    # fork 3 F2 (user-ruled 2026-08-21): auxiliary per-slot byte-reconstruction
    # loss on the summarizer's memory rows — the pressure path that tells the
    # summarizer the tail bytes must be IN the memory row. Train-time only:
    # never computed in eval, so eval_loss stays form-identical to historical
    # runs (comparability); the aux head never enters inference.
    aux_recon_loss = torch.zeros((), device=device)
    if train and getattr(args, "summarizer_aux_recon", False) and out.get("memory") is not None:
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=args.amp and device.type == "cuda"):
            aux_logits = model.aux_recon_logits(out["memory"])
        aux_recon_loss = _ce(aux_logits, targets, slot_mask)
        loss = loss + args.summarizer_aux_weight * aux_recon_loss
    # Metrics stay on device (detached scalars); the training loop accumulates
    # them and only syncs to host at log time -- per-step .item() calls on
    # ~19 metrics were serializing the pipeline.
    metrics = {
        "loss": loss.detach(),
        "direct_loss": direct_loss.detach(),
        "completion_loss": completion_loss.detach(),
        "predict_loss": predict_loss.detach(),
        "predict_ce": predict_ce.detach(),
        "predict_byte_acc": predict_byte_acc.detach(),
        "direct_acc": _acc_tensor(out["logits_direct"].argmax(dim=-1), encoded_targets, encoded_slot_mask),
        "backbone_acc": _acc_tensor(out["logits_backbone"].argmax(dim=-1), comp_targets, comp_slot_mask),
        "backbone_masked_acc": _acc_tensor(out["logits_backbone"].argmax(dim=-1), comp_targets, comp_masked_slot),
        "backbone_unmasked_acc": _acc_tensor(out["logits_backbone"].argmax(dim=-1), comp_targets, unmasked_slot),
        "retention_truncated_slots": retention_trunc.detach().float(),
        "predict_cos": predict_cos.detach(),
        "cloze_loss": cloze_loss.detach(),
        "aux_recon_loss": aux_recon_loss.detach(),
        "cloze_byte_acc": cloze_metrics["cloze_byte_acc"],
        "cloze_exact": cloze_metrics["cloze_exact"],
        "cloze_count": cloze_metrics["cloze_count"],
        "retrieval_loss": retrieval_loss.detach(),
        "retrieval_byte_acc": retrieval_metrics["retrieval_byte_acc"],
        "retrieval_exact": retrieval_metrics["retrieval_exact"],
        "retrieval_count": retrieval_metrics["retrieval_count"],
        "retrieval_block_rate": retrieval_metrics["retrieval_block_rate"],
        "mask_rate": (byte_mask.float().sum() / valid.float().sum().clamp(min=1.0)).detach(),
        "truncated_tokens": chunks.pack_info["truncated_tokens"].float().sum().detach(),
        "cut_capacity_overflow": out["cut_overflow"].float().sum().detach(),
        "chunks_per_sample": chunks.chunk_mask.float().sum(dim=1).mean().detach(),
        "hard_cut_fraction": out["hard_cut_fraction"].detach(),
        "state_norm": out["state_norm"].detach(),
        "boundary_confidence_mean": out["boundary_confidence_mean"].detach(),
        "think_steps": torch.tensor(out["think_steps"], device=loss.device),
    }
    if slm_mode:
        # E80 补充 2: resident key-geometry dashboard (slm default-on; legacy
        # paths never gain these keys)
        metrics.update(_key_geometry_metrics(model, out, device))
    if codec_final and not train:
        # Eval n-scan (user-ruled 2026-08-11): subsample n of the C per-chunk
        # query rows uniformly (/n paging geometry, paged_boundaries) and serve
        # the WHOLE window from the kept rows -- a served chunk eats its
        # covering anchor row's full conditioning (shared final-state readout
        # + the ANCHOR's position embedding), so n measures how many
        # position-anchored query rows the window needs. n=last reproduces the
        # training form exactly (sanity anchor: equals backbone_acc).
        with torch.no_grad():
            c_max = int(chunks.chunk_mask.long().sum(dim=1).max().item())
            pos_c = model.chunk_pos.weight.unsqueeze(0)[:, : chunks.chunk_mask.size(1)]
            with torch.autocast("cuda", dtype=torch.bfloat16, enabled=args.amp and device.type == "cuda"):
                row_cond = model.decoder_in(out["content"]) + pos_c  # == cond_direct
                for tag, n in (("n1", 1), ("n4", 4), ("n8", 8), ("nlast", c_max)):
                    n_eff = min(n, max(c_max, 1))
                    boundary, serve = paged_boundaries(chunks.chunk_mask, n_eff)
                    anchors = row_cond.gather(
                        1, boundary.unsqueeze(-1).expand(-1, -1, row_cond.size(-1))
                    )
                    cond_n = anchors.gather(
                        1, serve.unsqueeze(-1).expand(-1, -1, row_cond.size(-1))
                    )
                    logits_n = model.decoder(cond_n, chunks.token_mask)
                    metrics[f"final_scan_acc_{tag}"] = _acc_tensor(logits_n.argmax(dim=-1), targets, slot_mask)
    return loss, metrics


@torch.no_grad()
def evaluate(model, eval_loader, args, device):
    model.eval()
    torch.manual_seed(args.eval_mask_seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(args.eval_mask_seed)
    _MASK_GENERATOR.manual_seed(args.eval_mask_seed)
    # cloze eval determinism (same seed family as the eval mask): fixed
    # splices per eval batch regardless of the training-time draw count.
    _CLOZE_GENERATOR.manual_seed(args.eval_mask_seed + _CLOZE_SEED_OFFSET)
    # retrieval eval determinism: same discipline, its own stream offset.
    _RETRIEVAL_GENERATOR.manual_seed(args.eval_mask_seed + _RETRIEVAL_SEED_OFFSET)
    rows = []
    for i, batch in enumerate(eval_loader):
        if i >= args.max_eval_batches:
            break
        _, metrics = step_model(model, batch, args, device, train=False)
        rows.append({k: float(v) for k, v in metrics.items()})
    model.train()
    merged = {}
    for key in rows[0]:
        merged[f"eval_{key}"] = sum(r[key] for r in rows) / len(rows)
    merged["eval_backbone_ppl"] = float(math.exp(min(merged["eval_completion_loss"], 20.0)))
    merged["eval_direct_ppl"] = float(math.exp(min(merged["eval_direct_loss"], 20.0)))
    return merged


def _add_s1_args(parser: argparse.ArgumentParser) -> None:
    """S1.0-specific CLI args on top of train_v36.build_parser (its defaults
    are drift-guarded against canonical_v36.json by
    tests/test_canonical_sync.py::test_v36_s1_layer_defaults_match_canonical)."""
    parser.add_argument("--predict-weight", type=float, default=1.0)
    parser.add_argument("--predict-mode", choices=["latent", "decode"], default="latent")
    parser.add_argument("--predict-latent-weight", type=float, default=0.1)
    parser.add_argument("--mask-mode", choices=["byte_span", "mixed"], default="mixed")
    parser.add_argument("--mask-char-frac", type=float, default=0.4)
    parser.add_argument("--mask-char-span-max", type=int, default=3)
    parser.add_argument(
        "--bpe-tokenizer-path",
        type=str,
        default="checkpoints/bpe_tokenizer_128k_v4/tokenizer.json",
    )
    parser.add_argument(
        "--codec-final-state",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="strict codec-retention arm (user-ruled 2026-08-11): every chunk "
        "row decodes from ONE read of the final KDA state S_final (no fresh "
        "per-chunk S_i reads); the backbone is excluded from the loss path; "
        "the predict task is disabled (weight forced 0, not computed); eval "
        "adds an n-scan {1,4,8,last} of subsampled query rows serving the "
        "whole window. Default off -- canonical runs are unaffected.",
    )
    parser.add_argument(
        "--cumulative-mask-retention",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="S39 stage-0c recipe fix (user-ruled 2026-08-17): completion row "
        "i restores the masked bytes of chunks 0..i (cumulative retention) "
        "instead of chunk i only, so the state machine/backbone get a "
        "non-zero retention training signal. Default ON (fixed recipe); "
        "--no-cumulative-mask-retention restores the pre-v36.8 zero-retention "
        "per-chunk targets for ablation. Direct and predict are unaffected.",
    )


def main() -> None:
    from tools.train.v3_6.train_v36 import build_parser

    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--config", default="")
    pre_args, _ = pre.parse_known_args()
    parser = build_parser()
    _add_s1_args(parser)
    if pre_args.config:
        parser.set_defaults(**json.loads(Path(pre_args.config).read_text(encoding="utf-8")))
    args = parser.parse_args()
    if not args.per_chunk_readout:
        raise SystemExit("S1.0 requires --per-chunk-readout")
    if getattr(args, "backbone_readout", "per_chunk") != "per_chunk" and args.predict_mode == "decode":
        raise SystemExit(
            "--backbone-readout final/paged supports --predict-mode latent only "
            "(decode CE is the E34-poisoned loss form)"
        )
    if getattr(args, "backbone_mode", "") == "draft" and args.predict_mode == "decode":
        raise SystemExit(
            "--backbone-mode draft supports --predict-mode latent only "
            "(decode CE is the E34-poisoned loss form)"
        )
    if getattr(args, "backbone_mode", "") == "slm":
        # v3.7 (consensus §2, user-ruled 2026-08-17): combinations that are
        # N/A in the new mode fail loudly, not silently.
        if args.codec_final_state:
            raise SystemExit(
                "--backbone-mode slm does not combine with --codec-final-state "
                "(the state machine is an optional per-channel interpreter in v3.7)"
            )
        if args.predict_mode == "decode":
            raise SystemExit(
                "--backbone-mode slm supports --predict-mode latent only "
                "(predict anchors the next chunk's decoder-aligned V row)"
            )
        if args.prefix_task:
            raise SystemExit("--backbone-mode slm does not combine with --prefix-task (N/A in v3.7)")
    if getattr(args, "cloze_prob", 0.0) > 0:
        # v3.7 cloze 检索回执 (user-ruled 2026-08-17): slm-only -- on legacy
        # xattn/paged/draft/attn paths (and the codec_final/paged/draft/
        # prefix_task combinations, which are non-slm or already rejected
        # above) fail loudly, not silently.
        if getattr(args, "backbone_mode", "") != "slm":
            raise SystemExit(
                "--cloze-prob>0 requires --backbone-mode slm (v3.7 cloze 检索回执); "
                "xattn/paged/draft/attn paths and codec_final/paged/draft/prefix_task "
                "combinations are N/A"
            )
        if not args.cloze_bank:
            raise SystemExit(
                "--cloze-prob>0 requires --cloze-bank <jsonl> "
                "(cloze 题库, tools/data/mine_cloze_bank.py contract)"
            )
        n_cloze_bank = _load_cloze_bank(args.cloze_bank)
        print(
            f"[s1] cloze 检索回执: bank={args.cloze_bank} entries={n_cloze_bank} "
            f"prob={args.cloze_prob} weight={args.cloze_weight}",
            flush=True,
        )
    _check_retrieval_args(args)
    if _retrieval_enabled(args):
        print(
            f"[s1] 自然检索任务 (招募臂): prob={args.retrieval_prob} "
            f"weight={args.retrieval_weight} block_prob(r)={args.retrieval_block_prob}",
            flush=True,
        )
    if args.codec_final_state:
        if not getattr(args, "state_channel", True):
            raise SystemExit("--codec-final-state requires --state-channel (this arm trains the state channel itself)")
        # predict is orthogonal to retention and stays OFF in this arm:
        # force the weight to 0 (it is never computed in step_model) and say
        # so in the log, per the preregistration.
        if args.predict_weight != 0:
            print("[s1] codec-final-state: predict task disabled (weight forced 0, not computed)", flush=True)
            args.predict_weight = 0.0
        print(
            "[s1] codec-final-state arm: direct+completion decode from ONE S_final "
            "readout (no fresh S_i reads); backbone excluded from the loss path",
            flush=True,
        )
    if args.mask_mode == "mixed":
        _load_bpe_tokenizer(args.bpe_tokenizer_path)
    _MASK_GENERATOR.manual_seed(args.seed)
    _CLOZE_GENERATOR.manual_seed(args.seed + _CLOZE_SEED_OFFSET)
    _RETRIEVAL_GENERATOR.manual_seed(args.seed + _RETRIEVAL_SEED_OFFSET)

    device = torch.device(args.device if args.device == "cpu" or torch.cuda.is_available() else "cpu")
    torch.manual_seed(args.seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(args.seed)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "resolved_config.json").write_text(json.dumps(vars(args), indent=2), encoding="utf-8")

    model = build_model(args).to(device)
    if args.eval_only:
        # S39 probes (e.g. --k-block-eval, user-ruled 2026-08-17): load one
        # checkpoint strict, run the standard eval pass, print JSON, exit.
        payload = torch.load(args.eval_only, map_location=device, weights_only=False)
        model.load_state_dict(payload["model"], strict=True)
        model.eval()
        _t, eval_loader = make_dataloaders(args)
        stats = evaluate(model, eval_loader, args, device)
        print(json.dumps(stats, ensure_ascii=False, indent=2), flush=True)
        return
    if args.init_checkpoint:
        payload = torch.load(args.init_checkpoint, map_location=device, weights_only=False)
        current = model.state_dict()
        compatible = {
            k: v for k, v in payload["model"].items() if k in current and current[k].shape == v.shape
        }
        init_prefixes = [p.strip() for p in args.init_prefixes.split(",") if p.strip()]
        if init_prefixes:
            compatible = {k: v for k, v in compatible.items() if any(k.startswith(p) for p in init_prefixes)}
        model.load_state_dict(compatible, strict=False)
        print(f"[s1] init: loaded={len(compatible)} skipped={len(payload['model']) - len(compatible)} prefixes={init_prefixes or 'ALL'}", flush=True)
    frozen = [p.strip() for p in args.freeze_prefixes.split(",") if p.strip()]
    if frozen:
        n = 0
        for name, param in model.named_parameters():
            if any(name.startswith(p) for p in frozen):
                param.requires_grad_(False)
                n += 1
        print(f"[s1] frozen params={n} prefixes={frozen}", flush=True)
    if args.codec_final_state:
        # the backbone never enters the loss path in this arm -- freeze it so
        # the optimizer state and any stray decay stay out of the variable set
        n_bb = 0
        for param in model.backbone.parameters():
            param.requires_grad_(False)
            n_bb += 1
        print(f"[s1] codec-final-state: backbone frozen (params={n_bb})", flush=True)
    trainable = [p for p in model.parameters() if p.requires_grad]
    opt = build_optimizer(args, iter(trainable))
    sched = _cosine_with_warmup(opt, args.warmup_steps, args.max_steps)
    train_loader, eval_loader = make_dataloaders(args)

    start_step = 0
    latest = out_dir / "latest.pt"
    if args.resume and latest.exists():
        payload = torch.load(latest, map_location=device, weights_only=False)
        model.load_state_dict(payload["model"])
        if args.save_optimizer and "optimizer" in payload:
            opt.load_state_dict(payload["optimizer"])
        start_step = int(payload.get("step", 0))
        if start_step > 0:
            sched.step(start_step)
        print(f"[s1] resumed from step {start_step}", flush=True)

    log_path = out_dir / "train_log.jsonl"
    model.train()
    t0 = time.time()
    nan_skips = 0
    step = start_step
    pending: dict[str, torch.Tensor] = {}
    pending_n = 0
    while step < args.max_steps:
        for batch in train_loader:
            if step >= args.max_steps:
                break
            loss, metrics = step_model(model, batch, args, device, train=True)
            if not bool(torch.isfinite(loss)):
                nan_skips += 1
                opt.zero_grad(set_to_none=True)
                step += 1
                sched.step()
                continue
            opt.zero_grad(set_to_none=True)
            loss.backward()
            grad = torch.nn.utils.clip_grad_norm_(trainable, args.grad_clip)
            opt.step()
            sched.step()
            step += 1
            for k, v in metrics.items():
                pending[k] = pending[k] + v if k in pending else v.clone()
            pending_n += 1
            if step % args.log_every == 0 or step == 1:
                row = {
                    "step": step,
                    "lr": float(opt.param_groups[0]["lr"]),
                    "grad": float(grad.item()),
                    "steps_per_sec": step / max(time.time() - t0, 1e-9),
                    "nan_skips": nan_skips,
                    **{k: float((v / pending_n).item()) for k, v in pending.items()},
                }
                _append_jsonl(log_path, row)
                pending = {}
                pending_n = 0
            if step % args.ckpt_every == 0:
                payload = {"step": step, "model": model.state_dict(), "args": vars(args)}
                if args.save_optimizer:
                    payload["optimizer"] = opt.state_dict()
                torch.save(payload, latest)
            if step % args.milestone_every == 0:
                torch.save({"step": step, "model": model.state_dict(), "args": vars(args)}, out_dir / f"step_{step:06d}.pt")

    payload = {"step": step, "model": model.state_dict(), "args": vars(args)}
    if args.save_optimizer:
        payload["optimizer"] = opt.state_dict()
    torch.save(payload, latest)

    eval_stats = evaluate(model, eval_loader, args, device)
    summary = {
        "run_id": args.run_id,
        "steps": step,
        "params": sum(p.numel() for p in model.parameters()),
        "elapsed_sec": time.time() - t0,
        "steps_per_sec": step / max(time.time() - t0, 1e-9),
        "nan_skips": nan_skips,
        "args": vars(args),
        **eval_stats,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
