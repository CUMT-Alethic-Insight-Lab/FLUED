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
   Q12 示例密集形态 (修订案 v3, 2026-08-22 冻结): ``--retrieval-examples``
   2–4 prepends that many COMPLETE examples (same 前文/答案是 format, answer
   visible and force-UNMASKED) before the query; query last (nothing is ever
   inserted after it). Anti-shortcut clauses are per-sample mechanical
   asserts (query answer never a byte-substring of any example; example
   source spans/contents distinct from the query's -- violations redraw up
   to N=8, then the sample stays inactive). Window budget (appendix A2②):
   source and query segments are never truncated; on overflow the EARLIEST
   examples are dropped first (drop rate recorded); a query pushed off the
   chunk grid is a construction defect (sample discarded, counted). Per-batch
   metrics: retrieval_budget_ratio / retrieval_examples / retrieval_drop_rate
   / retrieval_defect. Default 0 = the example-free form, bitwise-identical.
6. Q13 burstiness injection (v3.7 slm only, prereg
   docs/versions/v3.7/FLUED_V3_7_Q13_BURSTINESS_INJECTION_20260822_CN.md,
   frozen 2026-08-22): with probability ``--burst-prob`` one FRESH 32-64B
   corpus segment (random file offset via CorpusSampler -- 防背护栏: no fixed
   segment bank, (offset, length) registered process-wide, same-epoch repeats
   redraw up to N=8 then fail loudly) is inserted verbatim at R=3 random
   in-window positions (insertion widening). The last occurrence's trailing
   2-4 CJK chars are force-MASKED; the R-1 earlier occurrences are
   force-UNMASKED (它们是突发性本体). NO new loss term -- the codec three
   tasks already cover the masked tail (注入只改数据分布). Metrics:
   burst_tail_byte_acc / burst_tail_exact / burst_count / burst_tail_chars.
   Frozen values: R=3, tail 2-4 chars (--burst-repeat / --burst-tail-max-chars
   are parser-visible but out-of-range values fail loudly). Mutually
   exclusive with cloze AND retrieval (同窗只允许一种注入任务). Default off
   (``--burst-prob 0.0`` = zero intrusion, bitwise-identical legacy path).
   Q14 (修订案 2026-08-23): ``--burst-prior-sieve`` adds the construction-time
   bare-guess sieve (reference model frozen at the 开工 checkpoint, 裸猜
   byte_acc < 0.05 才录用, N=8 redraws, 全程不重筛), the burst_yield /
   burst_sieve_reject_rate log metrics (<70% yield prints a warning line --
   不静默放宽阈值), and the midpoint hook (at max_steps//2 the CURRENT model
   re-measures the rolling ledger of in-training segments; mean drift >0.02
   registers 先验侵蚀, per-segment table in out_dir/prior_erosion_midpoint.json).
   Default off = Q13 form, bitwise-identical.
   Q15 回路养成臂 (``--q15-circuit-rearing``, 任务书 2026-08-25 冻结, d 格限定):
   on top of Q14 -- 压缩区档 a 剔除 (``_burst_store_block``, occurrences 1..R-1
   的 store 行从遮蔽段尾首 chunk 起剔除, r 恒 1.0, train/eval 同开) + 过程奖励
   三件套 (全部 train-only): L_attend 注意力引导 (block-1 need_attn 手工注意力
   概率, T 掩码 = 源后目标行集, 逐样本 T∩src=∅ 机械断言), sg(g) 门控结果损失
   (echo 槽位从常规 completion 网格剔除防双重计分, eval 不动网格), L_couple
   反作弊孪生铰链 (head-tail swap 篡改, 孪生选择每条 splice 样本一抽
   _BURST_GENERATOR). codec 回调线 (§5): steps 800-1000 训练批
   direct_acc/backbone_acc 臂内自锚, 之后 log 事件窗均值退步 >2pp -> 三 λ 各
   x0.5 (下限 x0.25), 事件落 q15_callback_events.jsonl. 指标 q15_attend_mass /
   q15_attend_maxmass / q15_attend_chance / q15_attend_loss / q15_gate_mean /
   q15_echo_loss / q15_couple_loss / q15_twin_d / q15_twin_count (门 = §3.2
   修订 v1 单头超基线超出量: σ((maxmass−chance−δ)/s), δ=0.15 s=0.05 冻结),
   off/eval 零占位 schema 对齐.
7. Q18 v2 读出墙裁定臂 — B 计划 (``--q18-arm {A,Aprime}``, 2026-08-28 移植):
   A/A′ 臂从独立训练器 (train_q18_readout_wall.py) 移植进 s1 骨架。为什么
   移植: Q17/Q18 独立训练器双机双栈间歇楔死 (fresh 活 2-6K、resume 速楔、
   楔点随权重态; 事故簿 = Q18 任务书 §6), s1 骨架经 20K×多臂验证稳定——
   移植目的是稳定宿主, 机制一字不改 (流式双态读出/oracle 态/α 范数匹配/
   链重初始化/闭式温启动全部从独立训练器模块懒导入调用, 零复制)。形态:
   基座 --q18-base-ckpt strict 加载, 链范围 = Q17 修订 v1 足迹 A 从零 /
   A′ 温启动+零变化律自检, 其余全冻; 训练步委托 q17._q17_step (echo CE
   唯一损失, Q15 管束 burst R=3+末 2-4 字遮蔽+先验筛+store_block 全现成);
   A 40K / A′ 20K, LR 1e-3 + warmup 200 + cosine→0, 种子参数化; log
   schema 加 q18_arm/q18_seed。详见模块中部 Q18 节注记。

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
from collections import deque
from pathlib import Path

import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# 双模块陷阱护栏 (B 计划 2026-08-28 实测): 本文件作为脚本运行时模块名是
# __main__, Q18 模式懒导入的 train_q17_oracle_readout 再按包路径 import 本
# 模块会产生第二个实例——_BURST_SAMPLER/_MASK_GENERATOR 等进程级全局两边分
# 叉 (副本侧 sampler=None 即崩)。预注册规范名 → 全局唯一实例; 正常被 import
# 时 sys.modules 已有本键, setdefault 无操作。
sys.modules.setdefault("tools.train.v3_6.train_v36_s1", sys.modules[__name__])

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
# Q11 r 爬坡（prereg §4: {0 → 0.5 → 1.0}，每档 ≥5K 步）：main() 从
# --retrieval-block-ramp 解析填充，训练循环每步查表覆写 args 上的 r。
_RETRIEVAL_RAMP: list[tuple[int, float]] | None = None


def _parse_block_ramp(spec: str) -> list[tuple[int, float]]:
    """'0:0,0.5:5000,1.0:10000' -> [(0, 0.0), (5000, 0.5), (10000, 1.0)]
    (step, r) sorted by step; r applies from its step onward."""
    ramp = []
    for item in spec.split(","):
        r_s, step_s = item.split(":")
        ramp.append((int(step_s), float(r_s)))
    ramp.sort()
    for _s, r in ramp:
        if not 0.0 <= r <= 1.0:
            raise SystemExit(f"--retrieval-block-ramp r out of [0, 1]: {r}")
    return ramp


def _ramp_lookup(ramp: list[tuple[int, float]], step: int) -> float:
    r = ramp[0][1]
    for s, rr in ramp:
        if step >= s:
            r = rr
        else:
            break
    return r
_RETRIEVAL_QUERY_PRE = "\n前文'".encode("utf-8")
_RETRIEVAL_QUERY_POST = "'空格处是什么？".encode("utf-8")
_RETRIEVAL_ECHO_PROMPT = "\n答案是：".encode("utf-8")


def _retrieval_qa_block(frag: bytes, a_lo: int, a_hi: int, answer: bytes) -> bytes:
    """One 前文/答案是 block (Q12.1 format, identical for examples and the
    query): ``\\n前文'`` + frag with the answer span blanked to ``___`` +
    ``'空格处是什么？`` + ``\\n答案是：`` + answer. Examples keep the answer
    visible; the query's echo is force-MASKED downstream (mask overrides)."""
    return (
        _RETRIEVAL_QUERY_PRE
        + frag[:a_lo]
        + b"___"
        + frag[a_hi:]
        + _RETRIEVAL_QUERY_POST
        + _RETRIEVAL_ECHO_PROMPT
        + answer
    )
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
    exclusive with cloze (同窗只允许一种检索任务). Q12 示例密集形态
    (修订案 v3): --retrieval-examples is 0 (example-free form) or 2–4, and
    requires a live retrieval task."""
    r = float(getattr(args, "retrieval_block_prob", 0.0))
    if not 0.0 <= r <= 1.0:
        raise SystemExit(
            f"--retrieval-block-prob must lie in [0, 1] (档 a 掩码剔除比例 r, got {r})"
        )
    n_ex = int(getattr(args, "retrieval_examples", 0))
    if n_ex != 0 and not 2 <= n_ex <= 4:
        raise SystemExit(
            f"--retrieval-examples must be 0 (无示例形态) or 2–4 (Q12 示例密集形态, "
            f"修订案 v3 Q12.1), got {n_ex}"
        )
    if n_ex > 0 and not _retrieval_enabled(args):
        raise SystemExit("--retrieval-examples>0 requires --retrieval-prob>0 (Q12 示例密集形态)")
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


def _draw_retrieval_fragment(raw: bytes, n: int, answer_mode: str, generator: torch.Generator):
    """One fragment+answer draw (shared by the example-free and Q12 forms):
    32-64B contiguous in-window fragment (start uniform, snapped FORWARD to a
    UTF-8 char boundary, end snapped BACKWARD), then the answer segment inside
    it uniformly among the mode's candidates. Fixed draw order: frag_len,
    start, candidate index. Returns (start, end, frag, (a_lo, a_hi)) or None
    (no qualifying candidate; the candidate-index draw is then not consumed,
    same discipline as the legacy retry loop)."""
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
        return None
    ci = int(torch.randint(len(cands), (1,), generator=generator))
    return start, end, frag, cands[ci]


def _draw_retrieval_examples(raw: bytes, n: int, n_examples: int, answer_mode: str, generator: torch.Generator, capacity: int | None):
    """Q12 示例密集形态 (修订案 v3, 2026-08-22 冻结): one attempt = n_examples+1
    independent fragment+answer draws, then ONE role draw deciding which item
    is the query (示例/查询角色随机化; the rest are examples in drawn order).
    Anti-shortcut clauses (Q12.2, mechanical per-sample asserts): all K+1
    source spans pairwise distinct (span AND content -- so 示例来源段 ≠ 查询
    来源段 holds under any role assignment) and the query answer string never
    a byte-level substring of any example block; violations redraw up to
    _RETRIEVAL_MAX_RETRY (N=8), then the sample stays inactive.

    Window budget (appendix A2②): source and query segments are NEVER
    truncated; if the total (window + example blocks + query block) exceeds
    ``capacity`` bytes (the 4096B 窗 = chunk-grid byte capacity) the EARLIEST
    examples are dropped first (n_dropped recorded). The query block always
    goes last -- nothing is ever inserted after it; a query pushed off the
    chunk grid is a construction defect, caught downstream by the echo slot
    grid (sample discarded, counted in retrieval_defect).

    Returns (meta, new_row_bytes) or None."""
    for _attempt in range(_RETRIEVAL_MAX_RETRY):
        items = []
        for _ in range(n_examples + 1):
            item = _draw_retrieval_fragment(raw, n, answer_mode, generator)
            if item is None:
                break
            items.append(item)
        if len(items) < n_examples + 1:
            continue
        # role draw is consumed for EVERY candidate-complete attempt, before
        # the constraint checks (draw stream fixed in shape per attempt).
        qi = int(torch.randint(len(items), (1,), generator=generator))
        spans = [(s, e) for s, e, _, _ in items]
        if len(set(spans)) != len(spans):
            continue  # 示例来源段 ≠ 查询来源段 (span level)
        frags = [f for _, _, f, _ in items]
        if len(set(frags)) != len(frags):
            continue  # 示例与查询内容独立 (content level)
        q_start, q_end, q_frag, (qa_lo, qa_hi) = items[qi]
        q_answer = q_frag[qa_lo:qa_hi]
        ex_items = items[:qi] + items[qi + 1 :]
        ex_blocks = [
            _retrieval_qa_block(f, alo, ahi, f[alo:ahi]) for _, _, f, (alo, ahi) in ex_items
        ]
        if any(q_answer in blk for blk in ex_blocks):
            continue  # 查询答案字符串不得出现在任何示例中 (byte substring)
        # 窗口预算 (A2②): 溢出按最早示例先丢; 来源段与查询段永不截断
        n_dropped = 0
        if capacity:
            total = n + sum(len(blk) for blk in ex_blocks) + len(
                _retrieval_qa_block(q_frag, qa_lo, qa_hi, q_answer)
            )
            while ex_blocks and total > capacity:
                total -= len(ex_blocks[0])
                ex_blocks = ex_blocks[1:]
                ex_items = ex_items[1:]
                n_dropped += 1
        parts = []
        ex_metas = []
        cur = n
        for (s, e, f, (alo, ahi)), blk in zip(ex_items, ex_blocks):
            ans = f[alo:ahi]
            ex_metas.append(
                {
                    "source_span": (s, e),
                    "source_answer_span": (s + alo, s + ahi),
                    "echo_span": (cur + len(blk) - len(ans), cur + len(blk)),
                    "answer_b": ans,
                }
            )
            parts.append(blk)
            cur += len(blk)
        query_start = cur
        new = raw + b"".join(parts) + _retrieval_qa_block(q_frag, qa_lo, qa_hi, q_answer)
        meta = {
            "source_span": (q_start, q_end),
            "source_answer_span": (q_start + qa_lo, q_start + qa_hi),
            "query_start": query_start,
            "echo_span": (len(new) - len(q_answer), len(new)),
            "answer_b": q_answer,
            "examples": ex_metas,
            "n_examples": len(ex_metas),
            "n_dropped": n_dropped,
            "budget_ratio": len(new) / capacity if capacity else 0.0,
        }
        return meta, new
    return None


def _splice_retrieval(clean: torch.Tensor, prob: float, generator: torch.Generator, answer_mode: str = "cjk", n_examples: int = 0, capacity: int | None = None):
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

    ``n_examples`` (Q12 示例密集形态, 修订案 v3): 0 = the example-free form
    above (bitwise-identical); 2–4 = prepend that many complete examples
    (answer visible) before the query (see _draw_retrieval_examples for the
    anti-shortcut clauses and the window-budget drop rule). ``capacity`` is
    the window budget in bytes (chunk-grid byte capacity, the A2② 4096B 窗).

    Rows still without a candidate after N retries stay byte-identical and
    inactive (draws consumed, splice skipped; counted in the activation
    rate). Returns (new_clean, metas); metas[b] is None or
    {"source_span": (lo, hi), "source_answer_span": (lo, hi),
    "query_start": int, "echo_span": (lo, hi), "answer_b": bytes} -- the Q12
    form adds "examples" (per-example same-shape dicts), "n_examples",
    "n_dropped", "budget_ratio".
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
        if n_examples > 0:
            picked_ex = _draw_retrieval_examples(raw, n, n_examples, answer_mode, generator, capacity)
            if picked_ex is None:
                continue  # N retries exhausted: inactive (counted in activation rate)
            metas[b], spliced[b] = picked_ex
            continue
        picked = None
        for _attempt in range(_RETRIEVAL_MAX_RETRY):
            picked = _draw_retrieval_fragment(raw, n, answer_mode, generator)
            if picked is not None:
                break
        if picked is None:
            continue  # N retries exhausted: inactive (counted in activation rate)
        start, end, frag, (a_lo, a_hi) = picked
        answer = frag[a_lo:a_hi]
        tail = _retrieval_qa_block(frag, a_lo, a_hi, answer)
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
    the regular mask. Q12 示例密集形态 (修订案 v3): the overrides key off the
    QUERY spans (examples' source spans keep the regular mask -- their store
    rows are never excised either, 示例是脚手架，必须可读), and each example's
    echo answer is force-UNMASKED (示例的答案可见 -- a scaffold with a masked
    answer is not a complete demonstration)."""
    for b, m in enumerate(metas):
        if m is None:
            continue
        lo, hi = m["source_answer_span"]
        byte_mask[b, lo:hi] = False
        lo, hi = m["echo_span"]
        byte_mask[b, lo:hi] = True
        for ex in m.get("examples") or ():
            lo, hi = ex["echo_span"]
            byte_mask[b, lo:hi] = False
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

    Q12 示例密集形态 (修订案 v3): the metas' source_span/query_start are the
    QUERY's, so only the query's source chunks are excised; the examples'
    store rows are never excised (示例是脚手架，必须可读).
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


# ---------------------------------------------------------------------------
# Q13 突发性注入臂 (burstiness injection, prereg 2026-08-22 frozen:
# docs/versions/v3.7/FLUED_V3_7_Q13_BURSTINESS_INJECTION_20260822_CN.md)
# Data-layer only: no new loss term -- the codec three tasks already cover the
# masked tail (§2: 注入只改数据分布). E104 归因: 窗内基础复制回路从未形成,
# 注入逐字重复段 (R=3 成簇出现 = burstiness) 把 induction 回路催出来.
# ---------------------------------------------------------------------------

# Dedicated CPU generator, same discipline as _RETRIEVAL_GENERATOR: main()
# seeds from args.seed, evaluate() re-seeds from args.eval_mask_seed; its own
# offset decorrelates the burst draw stream from the mask/cloze/retrieval
# streams.
_BURST_GENERATOR = torch.Generator()
_BURST_SEED_OFFSET = 101_021
_BURST_SAMPLER = None  # CorpusSampler, opened by main() when --burst-prob>0
# Q13 §2 frozen values: repeat count R=3, masked tail = last 2-4 CJK chars.
_BURST_REPEAT_FROZEN = 3
_BURST_TAIL_MIN_CHARS = 2
_BURST_TAIL_MAX_CHARS = 4
# Q14 修订案 (2026-08-23 冻结, FLUED_V3_7_Q14_PRIOR_SIEVED_DEMAND_20260823_CN.md):
# 先验筛阈值 (裸猜 <0.05 才录用) 与中点复测漂移线 (>0.02 = 先验侵蚀) ——
# 不静默放宽, 阈值改动只走修订记录.
_BURST_SIEVE_THRESHOLD = 0.05
_BURST_MIDPOINT_DRIFT = 0.02
_BURST_SIEVE_MODEL = None  # Q14 参考模型, main() 在筛开时固定于开工 checkpoint


class CorpusSampler:
    """Q13 随机段现采器 (防背护栏, prereg §3 冻结): every segment is drawn
    FRESH from the corpus by random file offset -- 严禁任何形式的固定段库.
    Each drawn segment is registered as (file_offset, length) in a
    process-level set; a repeat draw within the same epoch redraws up to
    _RETRIEVAL_MAX_RETRY (N=8) times, then fails loudly (机械断言).

    Draw order on the generator (fixed): offset, then length. The seek lands
    anywhere, so the read window is UTF-8 snapped (start forward, end
    backward, same discipline as the retrieval fragment draw); a segment that
    cannot be snapped/decoded counts as a failed attempt WITHOUT registering.
    """

    def __init__(self, path: str, seg_min: int = 32, seg_max: int = 64):
        self._path = str(path)
        self._fh = open(self._path, "rb")
        self._size = Path(self._path).stat().st_size
        self._seg_min = seg_min
        self._seg_max = seg_max
        if self._size < seg_max + 8:
            raise ValueError(f"CorpusSampler: corpus too small ({self._size}B): {self._path}")
        self._seen: set[tuple[int, int]] = set()
        # Q14 中点复测钩 (修订案 §2.1): 滚动 ledger, 最近 <=2000 个已用段
        # (实际 spliced 的段), 逐段记录 (段字节, 尾字节数, 筛时裸猜基准).
        self.ledger: deque = deque(maxlen=2000)

    def note_used(self, seg: bytes, tail_bytes: int, prior_baseline: float | None) -> None:
        """Register one actually-spliced segment in the rolling ledger (Q14
        臂中点复测用: 同一批在训片段). prior_baseline = 筛时参考模型实测裸猜率
        (筛关时为 None, 该条目不参与中点漂移对比)."""
        self.ledger.append(
            {"seg": bytes(seg), "tail_bytes": int(tail_bytes), "prior_baseline": prior_baseline}
        )

    def reset_epoch(self) -> None:
        """同 epoch 内不重复的登记簿在新 epoch 开始时清空."""
        self._seen.clear()

    def draw(self, generator: torch.Generator) -> tuple[bytes, tuple[int, int]] | None:
        """One fresh 32-64B UTF-8-snapped segment + its (offset, length)
        registration key; raises RuntimeError when N=8 redraws keep hitting
        already-registered (offset, length) pairs."""
        for _attempt in range(_RETRIEVAL_MAX_RETRY):
            off = int(torch.randint(0, self._size - self._seg_max - 1, (1,), generator=generator))
            seg_len = int(torch.randint(self._seg_min, self._seg_max + 1, (1,), generator=generator))
            key = (off, seg_len)
            if key in self._seen:
                continue  # 同 epoch 重复采中同一段: 重抽 (上限 N=8)
            self._fh.seek(off)
            raw = self._fh.read(seg_len + 8)  # slack for the boundary snap
            start = 0
            while start < len(raw) and (raw[start] & 0xC0) == 0x80:
                start += 1
            end = min(start + seg_len, len(raw))
            # UTF-8 snap: end backward to a char boundary (retrieval discipline)
            while end > start and end < len(raw) and (raw[end] & 0xC0) == 0x80:
                end -= 1
            seg = raw[start:end]
            if end - start < self._seg_min // 2:
                continue  # snap ate too much: failed attempt, unregistered
            try:
                seg.decode("utf-8")
            except UnicodeDecodeError:
                continue
            self._seen.add(key)
            return seg, key
        raise RuntimeError(
            "CorpusSampler: 同 epoch 内重复采中段/无效段超过 N=8 次重抽 "
            "(Q13 防背护栏, prereg §3) -- 响亮报错, 不静默放行"
        )


def _burst_enabled(args) -> bool:
    return float(getattr(args, "burst_prob", 0.0)) > 0.0


def _check_burst_args(args) -> None:
    """Loud CLI validation for the Q13 burst task: the frozen values are not
    negotiable (R 只能是 3, tail 只能 2-4 字); a live task is slm-only and
    mutually exclusive with cloze AND retrieval (同窗只允许一种注入任务)."""
    r = int(getattr(args, "burst_repeat", _BURST_REPEAT_FROZEN))
    if r != _BURST_REPEAT_FROZEN:
        raise SystemExit(f"--burst-repeat is frozen at R=3 (Q13 预注册 §2), got {r}")
    tmax = int(getattr(args, "burst_tail_max_chars", _BURST_TAIL_MAX_CHARS))
    if not _BURST_TAIL_MIN_CHARS <= tmax <= _BURST_TAIL_MAX_CHARS:
        raise SystemExit(
            f"--burst-tail-max-chars must lie in [2, 4] (Q13 预注册 §2 末 2-4 个 CJK 字符), got {tmax}"
        )
    if not _burst_enabled(args):
        if bool(getattr(args, "burst_prior_sieve", False)):
            raise SystemExit(
                "--burst-prior-sieve requires --burst-prob>0 (Q14 先验筛只挂在 burst 形态上)"
            )
        return
    if getattr(args, "backbone_mode", "") != "slm":
        raise SystemExit(
            "--burst-prob>0 requires --backbone-mode slm (Q13 突发性注入臂, prereg "
            "2026-08-22); xattn/paged/draft/attn paths are N/A"
        )
    if float(getattr(args, "cloze_prob", 0.0)) > 0 or float(getattr(args, "retrieval_prob", 0.0)) > 0:
        raise SystemExit(
            "--burst-prob>0 is mutually exclusive with --cloze-prob>0 and "
            "--retrieval-prob>0 (同窗只允许一种注入任务)"
        )


def _splice_burst(clean: torch.Tensor, prob: float, generator: torch.Generator, sampler: CorpusSampler, repeat: int = _BURST_REPEAT_FROZEN, tail_max_chars: int = _BURST_TAIL_MAX_CHARS, sieve_model=None, stats: dict | None = None):
    """Q13 突发性注入 (prereg §2): per selected window, draw ONE fresh 32-64B
    corpus segment (``sampler`` -- random file offset, 防背登记) and insert it
    verbatim at R=3 uniformly random in-window positions (insertion widening,
    same legality as cloze/retrieval; positions UTF-8 snapped forward, not
    fixed at window head/tail). The LAST occurrence in byte order is the R-th
    occurrence: its trailing 2-4 non-boundary chars (k drawn per sample, UTF-8
    boundary by construction) are the masked tail; the R-1 earlier occurrences
    stay fully visible (它们是突发性本体, 遮蔽即自毁需求).

    Q14 先验筛 (修订案 2026-08-23 §2.1, ``sieve_model`` 非 None 时启用):
    each structurally accepted candidate segment then passes the bare-guess
    measurement (_burst_prior_guess_acc on the reference model frozen at the
    开工 checkpoint): 裸猜 byte_acc < 0.05 才录用, otherwise the candidate is
    rejected and redrawn (same N=8 cap, exhausted = inactive). The reference
    model is read-only for the whole run (筛子基准不随训练重筛); the accepted
    segment's measured baseline lands in the sampler's rolling ledger for the
    midpoint re-measurement.

    Per-row draw order on ``generator`` (fixed): selection uniform, then per
    segment attempt: the sampler's (offset, length) draws and the tail char
    count k; on a segment whose tail has no qualifying 2-4 char run (or which
    the sieve rejects), redraw up to _RETRIEVAL_MAX_RETRY (N=8) then leave
    the row inactive. After a good segment: R insertion positions.

    ``stats`` (optional mutable bag) accumulates {"drawn", "spliced",
    "sieve_measured", "sieve_rejected"} for the burst_yield /
    burst_sieve_reject_rate log metrics. Returns (new_clean, metas);
    metas[b] is None or {"seg_offset": int, "seg_len": int, "occurrences":
    [(lo, hi)]*R in byte order, "echo_span": (lo, hi) (the masked tail, cloze
    slot-grid compatible), "answer_b": bytes, "tail_chars": int}. The (offset,
    length) registration lives in the sampler's seen set; the probe's
    窗内副本存在 audit column reads ``occurrences``.
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
        if stats is not None:
            stats["drawn"] += 1  # 抽中样本 (产出率分母)
        raw = bytes(int(i) - BYTE_OFFSET for i in ids[:n].tolist())
        seg = None
        seg_key = None
        tail_bytes = 0
        tail_chars = 0
        prior_baseline = None
        for _attempt in range(_RETRIEVAL_MAX_RETRY):
            got = sampler.draw(generator)  # raises after N=8 防背 collisions
            if got is None:
                continue
            cand, cand_key = got
            # 段尾遮蔽 (Q13 §2): 末 k 个字符 (k 每样本抽 2..tail_max_chars),
            # 全部非边界字符 (与 Q11 v2 同规, 不用比例制不用字节数)
            k = int(torch.randint(_BURST_TAIL_MIN_CHARS, tail_max_chars + 1, (1,), generator=generator))
            text = cand.decode("utf-8")  # sampler guarantees decodable
            if len(text) < k + 2:  # the masked tail must not eat the whole segment
                continue
            tail = text[-k:]
            if any(ch in _BOUNDARY_CHARS for ch in tail):
                continue
            tail_b = sum(len(ch.encode("utf-8")) for ch in tail)
            # Q14 先验筛 (修订案 §2.1): 裸猜 <0.05 才录用, 否则重抽 (N=8 沿用)
            if sieve_model is not None:
                acc = _burst_prior_guess_acc(sieve_model, cand, tail_b)
                if stats is not None:
                    stats["sieve_measured"] += 1
                if acc is None or acc >= _BURST_SIEVE_THRESHOLD:
                    if stats is not None:
                        stats["sieve_rejected"] += 1
                    continue
                prior_baseline = acc
            seg = cand
            seg_key = cand_key
            tail_bytes = tail_b
            tail_chars = k
            break
        if seg is None:
            continue  # N retries exhausted: inactive (counted in burst activation)
        positions = sorted(
            int(torch.randint(0, n + 1, (1,), generator=generator)) for _ in range(repeat)
        )
        # UTF-8 snap forward, then insert (widen) in position order
        parts = []
        occ: list[tuple[int, int]] = []
        prev = 0
        shift = 0
        for p in positions:
            while p < n and (raw[p] & 0xC0) == 0x80:
                p += 1
            parts.append(raw[prev:p])
            parts.append(seg)
            occ.append((p + shift, p + shift + len(seg)))
            shift += len(seg)
            prev = p
        parts.append(raw[prev:])
        new = b"".join(parts)
        last_lo, last_hi = occ[-1]
        metas[b] = {
            "seg_offset": seg_key[0],  # 段（文件偏移，长度）登记 -- 探针审计列用
            "seg_len": seg_key[1],
            "occurrences": occ,
            "echo_span": (last_hi - tail_bytes, last_hi),
            "answer_b": new[last_hi - tail_bytes : last_hi],
            "tail_chars": tail_chars,
        }
        spliced[b] = new
        if stats is not None:
            stats["spliced"] += 1
        sampler.note_used(seg, tail_bytes, prior_baseline)  # Q14 滚动 ledger
    out = clean
    if spliced:
        new_width = max([width] + [len(r) for r in spliced.values()])
        out = clean.new_full((bsz, new_width), PAD_ID)
        out[:, :width] = clean
        for b, r in spliced.items():
            out[b] = PAD_ID
            out[b, : len(r)] = torch.tensor([x + BYTE_OFFSET for x in r], dtype=clean.dtype)
    return out, metas


@torch.no_grad()
def _burst_prior_guess_acc(model, seg: bytes, tail_bytes: int) -> float | None:
    """Q14 裸猜测量 (修订案 §2.1): the segment alone as the whole document
    (无前次出现、无上下文), its trailing ``tail_bytes`` masked, fp32 eval
    (model mode toggled and restored); returns the per-byte accuracy over the
    masked tail slots. None when the tail never lands on the chunk grid
    (callers treat as a rejected candidate)."""
    device = next(model.parameters()).device
    ids = torch.tensor([[b + BYTE_OFFSET for b in seg]], dtype=torch.long, device=device)
    n = ids.size(1)
    if n <= tail_bytes:
        return None
    mask = torch.zeros_like(ids, dtype=torch.bool)
    mask[0, n - tail_bytes :] = True
    source = ids.masked_fill(mask, MASK_ID)
    was_training = model.training
    model.eval()
    try:
        out = model(source)
    finally:
        if was_training:
            model.train()
    chunks = out.chunks
    t = torch.arange(n - tail_bytes, n, device=device)
    j = chunks.chunk_ids[0, t]
    s = chunks.offsets[0, t]
    if not bool((j.ge(0) & s.ge(0)).all()):
        return None
    pred = out.logits_backbone.argmax(dim=-1)
    hits = pred[0, j, s] == ids[0, n - tail_bytes :]
    return float(hits.float().mean())


def _window_burstiness(clean_row_bytes: bytes, gram: int = 12) -> float:
    """窗内突发性密度 (任务书 FLUED_V3_7_LR_SCALE_2X2_20260826_CN §1 新增仪表,
    2026-08-26 冻结): 窗内重复 >=12 字节子串的字节覆盖率 —— 12-gram 计数,
    出现 >=2 次的 gram 覆盖的字节占窗长比例. 纯 CPU 函数; 只在 log 事件
    调用 (逐步不算, 成本≈零), 无条件常开 (不加旗标, 任务书 §1 口径).
    离线复算仪表: tools/analysis/v3_6/measure_stream_burstiness.py 同口径."""
    n = len(clean_row_bytes)
    if n < gram:
        return 0.0
    counts: dict[bytes, int] = {}
    for i in range(n - gram + 1):
        g = clean_row_bytes[i : i + gram]
        counts[g] = counts.get(g, 0) + 1
    diff = [0] * (n + 1)
    for i in range(n - gram + 1):
        if counts[clean_row_bytes[i : i + gram]] >= 2:
            diff[i] += 1
            diff[i + gram] -= 1
    covered = 0
    cur = 0
    for i in range(n):
        cur += diff[i]
        if cur > 0:
            covered += 1
    return covered / n


def _batch_data_burstiness(clean: torch.Tensor) -> float:
    """log 事件的 data_burstiness 行键 (任务书 §1, 无条件常开): 当前批
    各 row 有效前缀 (非 PAD) 的 _window_burstiness 均值. 输入取 step_model
    注入任务之前的原始批 (canonical 2x2 臂 cloze/retrieval/burst 全关),
    测的是语料流窗本身的喂养形态."""
    burst_sum = 0.0
    burst_n = 0
    for row_ids in clean:
        valid_ids = row_ids[row_ids.ne(PAD_ID)]
        burst_sum += _window_burstiness((valid_ids - BYTE_OFFSET).to(torch.uint8).cpu().numpy().tobytes())
        burst_n += 1
    return burst_sum / max(burst_n, 1)


def _burst_yield_alarm(step: int, yield_val: float) -> None:
    """Q14 产出率报警 (修订案 §2.2): 产出率 <70% 打警告行 -- 不静默放宽阈值,
    阈值改动只走修订记录 (ASCII 词激活率塌方的前车)."""
    if yield_val < 0.70:
        print(
            f"[s1][WARN] Q14 产出率报警: step={step} burst_yield={yield_val:.4f} < 0.70 "
            "-- 不静默放宽阈值, 阈值改动只走修订记录",
            flush=True,
        )


def _burst_prior_midpoint_check(model, args, device, out_dir: Path) -> None:
    """Q14 臂中点复测钩 (修订案 §2.1): at max_steps//2, re-measure the
    bare-guess rate of the SAME in-training segments (CorpusSampler rolling
    ledger) with the CURRENT model, per-segment against the sieve baseline
    (参考模型实测值, recorded at sieve time). drift = cur - base; 均值漂移
    >0.02 = 先验侵蚀登记行 (print). The per-segment table always lands in
    out_dir/prior_erosion_midpoint.json (判读分列由收官时做)."""
    ledger = list(_BURST_SAMPLER.ledger) if _BURST_SAMPLER is not None else []
    rows = []
    for ent in ledger:
        base = ent.get("prior_baseline")
        if base is None:
            continue  # 筛关时的条目无基准, 不参与漂移对比
        cur = _burst_prior_guess_acc(model, ent["seg"], ent["tail_bytes"])
        if cur is None:
            continue
        rows.append(
            {
                "seg_len": len(ent["seg"]),
                "tail_bytes": ent["tail_bytes"],
                "prior_at_init": round(base, 6),
                "prior_at_midpoint": round(cur, 6),
                "drift": round(cur - base, 6),
            }
        )
    drift_mean = sum(r["drift"] for r in rows) / len(rows) if rows else 0.0
    erosion = drift_mean > _BURST_MIDPOINT_DRIFT
    payload = {
        "probe": "Q14 臂中点先验复测 (修订案 §2.1)",
        "step": int(args.max_steps) // 2,
        "n_segments": len(rows),
        "drift_mean": round(drift_mean, 6),
        "drift_line": _BURST_MIDPOINT_DRIFT,
        "prior_erosion": erosion,
        "items": rows,
    }
    (Path(out_dir) / "prior_erosion_midpoint.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if erosion:
        print(
            f"[s1][WARN] Q14 先验侵蚀登记: 臂中点裸猜率漂移 {drift_mean:.4f} > {_BURST_MIDPOINT_DRIFT} "
            f"(n={len(rows)}) -- 对应条目判读时单独分列 "
            f"({Path(out_dir) / 'prior_erosion_midpoint.json'})",
            flush=True,
        )
    else:
        print(
            f"[s1] Q14 臂中点先验复测: 漂移 {drift_mean:.4f} (线 {_BURST_MIDPOINT_DRIFT}, n={len(rows)}), "
            "无先验侵蚀",
            flush=True,
        )


def _burst_mask_overrides(byte_mask: torch.Tensor, metas: list) -> torch.Tensor:
    """Q13 mask discipline (prereg §2), applied AFTER the regular mask: the
    R-th occurrence's tail is force-MASKED (the induction training signal:
    complete the tail by copying from an earlier occurrence); the R-1 earlier
    occurrences are force-UNMASKED whole (它们是突发性本体, 遮蔽即自毁需求 --
    they must enter the state). Everything else keeps the regular mask."""
    for b, m in enumerate(metas):
        if m is None:
            continue
        lo, hi = m["echo_span"]
        byte_mask[b, lo:hi] = True
        for lo, hi in m["occurrences"][:-1]:
            byte_mask[b, lo:hi] = False
    return byte_mask


def _burst_metrics(logits_backbone: torch.Tensor, comp_targets: torch.Tensor, burst_slot: torch.Tensor, active: torch.Tensor, metas: list):
    """Q13 仪表 (no loss term -- 注入只改数据分布, the codec three tasks
    already cover the masked tail): per-byte acc and normalized exact over the
    masked tail slots (same completion conditioning, same _ascii_casefold
    normalization as the retrieval echo), burst_count = batch hit rate,
    burst_tail_chars = mean masked tail length in chars over active samples."""
    pred = logits_backbone.argmax(dim=-1)
    hit = pred.eq(comp_targets) & burst_slot
    byte_acc = hit.float().sum() / burst_slot.float().sum().clamp(min=1.0)
    hit_norm = _ascii_casefold(pred).eq(_ascii_casefold(comp_targets)) & burst_slot
    exact_per = (hit_norm | ~burst_slot).flatten(1).all(dim=1) & active
    exact = exact_per.float().sum() / active.float().sum().clamp(min=1.0)
    chars = [float(m["tail_chars"]) for b, m in enumerate(metas) if m is not None and bool(active[b])]
    tail_chars = torch.tensor(
        sum(chars) / len(chars) if chars else 0.0, device=logits_backbone.device
    )
    return {
        "burst_tail_byte_acc": byte_acc.detach(),
        "burst_tail_exact": exact.detach(),
        "burst_count": active.float().mean().detach(),
        "burst_tail_chars": tail_chars.detach(),
    }


# ---------------------------------------------------------------------------
# Q15 回路养成臂 (过程奖励 + 反作弊对偶, 任务书 2026-08-25 冻结:
# docs/versions/v3_7/FLUED_V3_7_Q15_CIRCUIT_REARING_20260825_CN.md)
# d 格 (k=state ∧ v=state, seed_source=k) 限定 -- §1 裁定: b 格下 block-1 的
# V 侧是 memory 行, L_attend 会焊在"地址对但读不到内容"的路径上 (奖励焊错
# 位置不是次优, 是预定结论). 三件套损失全部 train-only, 零新架构参数.
# ---------------------------------------------------------------------------

# 初值汇总 (任务书 §3.4, 全部冻结)
_Q15_TWIN_P = 0.25  # 孪生选择概率 (作用于已 splice 样本, 不摊给非任务样本)
_Q15_TWIN_M = 0.1  # 铰链边际 m
_Q15_GATE_DELTA = 0.15  # 门控 δ (§3.2 修订 v1: 单头超基线超出量, 替代原 τ=0.25 标定)
_Q15_GATE_S = 0.05  # 门控 s
_Q15_EPS = 1e-6  # L_attend 的 ε
_Q15_LAMBDA_ATT = 0.1  # λ_att (λ_out 继承 task2_loss_weight, 不写死数字)
_Q15_LAMBDA_COUPLE = 0.5  # λ_couple
# 回调线 (§5): 臂内自锚 steps 800-1000, 退步 >2pp 触发, 降权 x0.5/次,
# 下限 x0.25 (初值倍数)
_Q15_ANCHOR_RANGE = (800, 1000)
_Q15_CALLBACK_MARGIN = 0.02
_Q15_CALLBACK_DECAY = 0.5
_Q15_CALLBACK_FLOOR = 0.25


def _q15_enabled(args) -> bool:
    return bool(getattr(args, "q15_circuit_rearing", False))


def _check_q15_args(args) -> None:
    """Q15 响亮校验 (任务书 §7.5): 主开关要求 burst 开 + 先验筛开 + slm +
    d 格 (k=state ∧ v=state) + seed_source=k + readout_views==1; 与
    cloze/retrieval 的互斥沿用 burst 既有校验 (_check_burst_args)."""
    if not _q15_enabled(args):
        return
    if not _burst_enabled(args):
        raise SystemExit("--q15-circuit-rearing requires --burst-prob>0 (Q15 建在 Q13/Q14 burst 构造上)")
    if not bool(getattr(args, "burst_prior_sieve", False)):
        raise SystemExit("--q15-circuit-rearing requires --burst-prior-sieve (任务书 §2: 先验筛保留)")
    if getattr(args, "backbone_mode", "") != "slm":
        raise SystemExit("--q15-circuit-rearing requires --backbone-mode slm (任务书 §7.5)")
    if getattr(args, "k_row_source", "") != "state" or getattr(args, "v_row_source", "") != "state":
        raise SystemExit(
            "--q15-circuit-rearing requires d 格 (k_row_source=state 且 v_row_source=state; "
            "任务书 §1 裁定: b 格下 L_attend 焊在结构性无答案路径上)"
        )
    if getattr(args, "seed_source", "") != "k":
        raise SystemExit("--q15-circuit-rearing requires --seed-source k (任务书 §1 d 格裁定)")
    if int(getattr(args, "readout_views", 1)) != 1:
        raise SystemExit(
            "--q15-circuit-rearing requires readout_views==1 (views 路径不支持 need_attn 手工注意力)"
        )


def _burst_store_block(metas: list, chunks):
    """Q15 §2 压缩区激励改造 (档 a 语义, r 恒 1.0, 零随机抽): per spliced
    sample, excise the store rows covered by occurrences 1..R-1 (第 1..R-1 次
    出现的并集 chunk) from every query position at/after the masked tail's
    first chunk (qc = echo_span 首字节所在 chunk) -- the answer then reaches
    the tail only through the state channel. 剔除是任务构造本体, train/eval
    同开 (§7.2). Returns None when no sample is spliced (零成本 legacy 路径)."""
    chunk_ids = chunks.chunk_ids
    n_chunks = chunks.chunk_mask.size(1)
    block = None
    for b, m in enumerate(metas):
        if m is None:
            continue
        src = [chunk_ids[b, lo:hi] for lo, hi in m["occurrences"][:-1]]
        src = [c[c.ge(0)] for c in src]
        src = [c for c in src if c.numel()]
        if not src:
            continue  # 早次出现全部未入网格 (容量) -- 无可剔行
        src_chunks = torch.unique(torch.cat(src))
        elo, _ehi = m["echo_span"]
        tail = chunk_ids[b, elo:]
        q_chunks = tail[tail.ge(0)]
        if q_chunks.numel() == 0:
            continue  # 遮蔽段尾被挤出网格 -- 无 query 可剔 (slot 网格会计弃用)
        qc = int(q_chunks[0])  # chunks 字节序: 首个有效 = 段尾首字节 chunk
        if block is None:
            block = torch.zeros(
                chunk_ids.size(0), n_chunks, n_chunks, dtype=torch.bool, device=chunk_ids.device
            )
        block[b, qc:, src_chunks] = True
    return block


def _q15_assert_disjoint(t_mask: torch.Tensor, src_mask: torch.Tensor) -> None:
    """逐样本机械断言 (任务书 §3 + §1 方法论备案首次执行): 奖励靶点行集 T
    与掩码剔除集 src_chunks 交集必须为空, 违反即响亮报错."""
    if bool((t_mask.any(dim=0) & src_mask).any()):
        raise ValueError(
            "Q15 T∩src≠∅: 奖励靶点行集与掩码剔除集相交 (任务书 §3 机械断言) -- "
            "构造缺陷, 样本构造器须修正, 不静默放行"
        )


def _q15_echo_mass(attn_b: torch.Tensor, m: dict, chunk_ids_b: torch.Tensor, offsets_b: torch.Tensor, chunk_mask_b: torch.Tensor):
    """One spliced sample's T 掩码 + per-echo-byte attention mass (任务书 §3.1)
    + 门输入 (§3.2 修订 v1).

    T(b, q) = {j : c1_end < j <= q, j ∉ src_chunks(b), chunk j valid}, c1_end
    = 第 1 次出现的末 chunk. mass_i = Σ_h Σ_{j∈T(b,q_i)} A[h, q_i, j] -- 逐头
    求和而非全头均值 (L_attend 公式不变, 允许单头特化成回路). 门输入
    (修订 v1, 单头超基线超出量): maxmass_i = max_h Σ_{j∈T} A[h, q_i, j]
    (逐头 T 质量的 max over heads, 不是求和); chance_i = |T(b,q_i)| /
    |allowed(b,q_i)|, allowed = {j ≤ q_i ∧ chunk_mask 有效 ∧ j ∉ src_chunks}
    (对角已在集内 -- echo chunk 永不属于 src, 不用特判), 由索引计数构成,
    天然无梯度. Returns (mass, maxmass, chance, q_chunks, slots) -- 三个
    (n_echo,) 张量 + 位置; None when the echo never lands on the grid
    (样本不计入三件套, burst slot 网格的 active 判定同款)."""
    n_chunks = int(chunk_mask_b.size(0))
    src = [chunk_ids_b[lo:hi] for lo, hi in m["occurrences"][:-1]]
    src = [c[c.ge(0)] for c in src]
    src = [c for c in src if c.numel()]
    src_mask = torch.zeros(n_chunks, dtype=torch.bool, device=chunk_ids_b.device)
    if src:
        src_mask[torch.unique(torch.cat(src))] = True
    occ0_lo, occ0_hi = m["occurrences"][0]
    c0 = chunk_ids_b[occ0_lo:occ0_hi]
    c0 = c0[c0.ge(0)]
    c1_end = int(c0.max()) if c0.numel() else -1  # 第 1 次出现的末 chunk
    elo, ehi = m["echo_span"]
    t = torch.arange(elo, ehi, device=chunk_ids_b.device)
    q = chunk_ids_b[t]
    s = offsets_b[t]
    if not bool((q.ge(0) & s.ge(0)).all()):
        return None
    jj = torch.arange(n_chunks, device=chunk_ids_b.device)
    causal = jj.view(1, -1) <= jj.view(-1, 1)  # (C, C): [query, store_row]
    allowed = causal & chunk_mask_b.view(1, -1) & ~src_mask.view(1, -1)  # §3.2v1 allowed 集
    t_mask = allowed & (jj.view(1, -1) > c1_end)
    _q15_assert_disjoint(t_mask, src_mask)
    # mass per query chunk: Σ_h Σ_j A[h, q, j]·T[q, j]; maxmass: max_h Σ_j
    mass_head_q = (attn_b * t_mask.unsqueeze(0).to(attn_b.dtype)).sum(dim=2)  # (H, C)
    mass_per_q = mass_head_q.sum(dim=0)  # (C,) 逐头求和 (L_attend 用)
    maxmass_per_q = mass_head_q.max(dim=0).values  # (C,) 单头最大 (门输入)
    # chance (修订 v1): |T| / |allowed| 逐 query chunk, 纯索引计数无梯度
    chance_per_q = t_mask.sum(dim=1).float() / allowed.sum(dim=1).clamp(min=1).float()
    return mass_per_q[q], maxmass_per_q[q], chance_per_q[q], q, s


def _q15_gate(maxmass: torch.Tensor, chance: torch.Tensor) -> torch.Tensor:
    """Q15 §3.2 修订 v1 门 (冻结 δ=0.15, s=0.05): g = σ((maxmass − chance −
    δ)/s) -- 单头 T 质量超出该位置均匀基线 δ 才开门; 随机初始 max-head
    mass ≈ chance+涨落 -> 门基本关闭, 单头特化 (max→1) 门全开.
    stop-gradient 在调用侧 (反捷径条款: 不 detach 模型可压小 g 把损失幅度
    趋零, 与 L_attend 对拉形成退化路径)."""
    return torch.sigmoid((maxmass - chance - _Q15_GATE_DELTA) / _Q15_GATE_S)


def _burst_twin_bytes(raw: bytes, m: dict) -> bytes:
    """Q15 §3.3 反作弊对偶的孪生篡改 (机械确定性, 零随机流): copy the row and
    replace, for each of occurrences 1..R-1, the tail tb bytes (tb = echo_span
    长度) with occurrence 0's HEAD tb bytes (head-tail swap, UTF-8 合法 by
    construction -- 段内字节互换). 只动这些字节, 其余逐位相同."""
    tb = m["echo_span"][1] - m["echo_span"][0]
    occ0_lo = m["occurrences"][0][0]
    head = raw[occ0_lo : occ0_lo + tb]
    buf = bytearray(raw)
    for _lo, hi in m["occurrences"][:-1]:
        buf[hi - tb : hi] = head
    return bytes(buf)


def _q15_callback_check(anchor: dict, window: dict, lambdas: dict, floors: dict, step: int):
    """Q15 codec 回调线 (任务书 §5, 臂内自锚, 纯函数): 窗均值 (log 事件的
    direct_acc/backbone_acc) 任一较锚退步 >0.02 -> 三个 λ 各 x0.5, 下限为
    初值 x0.25 (floors). Returns (事件列表, 新 lambdas); 事件含
    step/触发项/旧值/新值, 调用侧逐次落盘 q15_callback_events.jsonl."""
    triggered = [
        k for k in ("direct_acc", "backbone_acc") if anchor[k] - window[k] > _Q15_CALLBACK_MARGIN
    ]
    if not triggered:
        return [], lambdas
    new = {k: max(v * _Q15_CALLBACK_DECAY, floors[k]) for k, v in lambdas.items()}
    event = {
        "step": step,
        "triggered": triggered,
        "anchor": {k: round(anchor[k], 6) for k in triggered},
        "window": {k: round(window[k], 6) for k in triggered},
        "old": dict(lambdas),
        "new": dict(new),
    }
    return [event], new


# ---------------------------------------------------------------------------
# decoder 去噪臂 (任务书 2026-08-29 冻结 v1.1 + 修订 v2 同日用户裁定:
# docs/versions/v3.7/FLUED_V3_7_DECODER_DENOISE_20260829_CN.md) — slm 系
# decoder direct 口 (decoder_in_mem) 的分布内模糊练钝; 可训练范围终审钉死
# = 仅 decoder
# ---------------------------------------------------------------------------

_DENOISE_GENERATOR = torch.Generator()
_DENOISE_SEED_OFFSET = 101_087  # 独立抽签流 (与 mask/cloze/retrieval/burst/q18 偏移不混)
_DENOISE_FUZZ = None  # main() 装载的前置测量产物 (probe_decoder_fuzz_id 落盘, 单部署桥)

# 课程里程碑 (任务书 §1 修订 v2 冻结; 扰动强度只升不降, 中途降档 = 改判读
# 条件须重新预注册): 0–5K 只 s=0.5 / 5K–10K 加 s=1.0 / 10K 起三档均匀 +
# m̂ 列激活 (后者由 --decoder-denoise-mhat-start 旗标控制, 默认与三档开启
# 同步)。档语义修订 v2: λ 桥档作废 (实测三档 cos 极差 0.008 ≪ 档内 std
# 0.08, 档间不可分的课程是假课程), 改为部署桥 (λopt=1.0) 残差采样器的标量
# 倍率 s∈{0.5,1.0,2.0}, s=1.0 恰是部署分布本身。
_DENOISE_MID_START = 5_000
_DENOISE_FULL_START = 10_000


def _decoder_denoise_enabled(args) -> bool:
    return bool(getattr(args, "decoder_denoise", False))


def _denoise_s_ladder(args) -> list[float]:
    """解析 --decoder-denoise-s-ladder (CSV 标量倍率档, 修订 v2): 每步解析
    (3 元素成本可忽略), 空档/非正数响亮报错。"""
    ladder = [float(x) for x in str(getattr(args, "decoder_denoise_s_ladder", "0.5,1.0,2.0")).split(",")]
    if not ladder or any(s <= 0 for s in ladder):
        raise ValueError(f"--decoder-denoise-s-ladder 非法: {ladder} (须为正数 CSV)")
    return ladder


def _denoise_curriculum(step: int, mhat_start: int, ladder: list[float]):
    """课程查表 (任务书 §1 修订 v2 冻结, 纯函数, 测试同用): Returns (本步可
    用 s 档列表 = ladder 前缀切片, m̂ 列是否激活)。"""
    if step < _DENOISE_MID_START:
        return ladder[:1], False
    if step < _DENOISE_FULL_START:
        return ladder[:2], False
    return ladder, step >= mhat_start


def _load_decoder_denoise_fuzz(fuzz_dir: str) -> dict:
    """装载前置测量产物 (probe_decoder_fuzz_id 落盘目录) 中的部署桥
    (λopt=1.0) 单采样器 (修订 v2: λ 三档作废, under/over 桥留在落盘目录不
    装载)。W/scale + 噪声采样件 (Cholesky L + ρ) 同桥同源; 找不到恰好一个
    λ=1.0 档响亮报错, 不静默降级。"""
    import numpy as np

    d = Path(fuzz_dir)
    stats = json.loads((d / "fuzz_stats.json").read_text(encoding="utf-8"))
    grade_map = stats["grade_map"]  # light/mid/heavy -> opt/under/over (实测定序)
    hits = []
    for grade, tag in grade_map.items():
        b = np.load(d / f"bridge_{grade}.npz")
        if float(b["lam"]) == 1.0:
            hits.append(grade)
    if len(hits) != 1:
        raise SystemExit(
            f"[s1][denoise] fuzz_id={fuzz_dir}: 部署桥 (lam=1.0) 命中 {len(hits)} 档 ({hits}), "
            "预期恰好 1 —— 检查前置测量产物完整性"
        )
    grade = hits[0]
    b = np.load(d / f"bridge_{grade}.npz")
    c = np.load(d / f"resid_chol_{grade}.npz")
    return {
        "W": torch.from_numpy(np.asarray(b["W"], dtype=np.float32)),
        "scale": float(b["scale"]),
        "chol": torch.from_numpy(np.asarray(c["L"], dtype=np.float32)),
        "rho": float(c["rho"]),
        "lam": float(b["lam"]),
        "tag": grade_map[grade],
    }


def _decoder_denoise_freeze(model) -> tuple[int, int]:
    """可训练范围钉死 = 仅 decoder (任务书 2026-08-29 终审确认项①):
    decoder_in_mem/chunk_pos/backbone/写入侧 (summarizer/WriteHead/状态机)/前端
    全冻。tied byte_lookup: named_parameters 去重后只在模型级名字出现一次
    (decoder.byte_lookup 是同一参数的别名, 不命中 "decoder." 前缀) —— 按
    E31/E34 裁定字节表是固定公尺 (decoder/table geometry must not be
    trainable), 留在冻结侧正是裁定语义; decoder 自身参数 (slot/blocks/scale)
    不许被误冻 (E116 同类坑的反向: prefix 清单会误冻 tied 嵌入, 这里是显式
    白名单, 两个方向都钉死)。Returns (n_trainable, n_frozen)。"""
    n_train = n_frozen = 0
    for name, param in model.named_parameters():
        if name.startswith("decoder."):
            param.requires_grad_(True)
            n_train += 1
        else:
            param.requires_grad_(False)
            n_frozen += 1
    return n_train, n_frozen


def _decoder_denoise_perturb(model, v_rows: torch.Tensor, chunks, index: torch.Tensor, args):
    """direct 口扰动副本 (任务书 §1 修订 v2 三列, train-only; 调用侧已保证
    b 格端口在岗 + 旗标开 + train)。Returns (v_rows_dec, stats); v_rows 本
    体不动。

    列① 统计匹配噪声: batch 级 p_noise 触发, 触发时随机 row_frac 实 chunk
    行, s 档于课程允许集内均匀抽; 合成式 ṽ = ρ·m + s·ε, ε = z @ Lᵀ
    (z~N(0,I); L/ρ 来自部署桥 (λopt=1.0) 前置测量的「范数匹配后残差」收缩
    Cholesky, 探针 F5 口径; ρ 固定实测值, s 只乘 ε 项, s=1.0 恰是部署分布)。
    列② m̂ 整行替换: batch 级 p_mhat 触发 (mhat_start 前不激活), 选中行整行
    替换为同窗 m̂ (K 态段1 解混 + 部署桥, 固定 λopt 桥不抽档, 非加性)。撞行
    时替换列覆盖噪声列 (整行替换语义, 实现层申报; 计数把撞行归替换列)。
    列③ 干净行 = 两列都未碰的行 (p 的补集 + 未触发 batch), 水位护栏在训仪表。
    全部常量化构造 (no_grad): 扰动值是常数, direct 腿梯度链形态不变。
    """
    fuzz = _DENOISE_FUZZ
    step = int(getattr(args, "decoder_denoise_step", 0))
    s_grades, mhat_on = _denoise_curriculum(
        step, int(getattr(args, "decoder_denoise_mhat_start", _DENOISE_FULL_START)), _denoise_s_ladder(args)
    )
    g = _DENOISE_GENERATOR
    device = v_rows.device
    real = chunks.chunk_mask  # (B, C) bool
    with torch.no_grad():
        # .float() 对 fp32 输入是别名不复制 —— 必须显式 clone, 任何情况下都
        # 不许原地改 v_rows (backbone 腿与 predict 锚吃它, 任务书 §3.2)
        v_dec = v_rows.float().clone()
        noise_sel = torch.zeros_like(real)
        mhat_sel = torch.zeros_like(real)
        s_hit = None

        # 列① 统计匹配噪声 (修订 v2: 标量倍率 s 只乘 ε 项)
        if float(torch.rand((), generator=g)) < float(args.decoder_denoise_p_noise):
            gi = int(torch.randint(len(s_grades), (), generator=g))
            s_hit = s_grades[gi]
            sel = (torch.rand(real.shape, generator=g) < float(args.decoder_denoise_row_frac)).to(device) & real
            if bool(sel.any()):
                L = fuzz["chol"].to(device)
                rho = fuzz["rho"]
                z = torch.randn(int(sel.sum()), v_rows.size(-1), generator=g).to(device)
                v_dec[sel] = rho * v_dec[sel] + s_hit * (z @ L.T)
                noise_sel = sel

        # 列② m̂ 整行替换 (10K 里程碑前不激活; batch-1 形态, ridge_unmix 逐窗;
        # 固定 λopt 部署桥不抽档 —— m̂ 列零域移, 任务书修订 v2)
        if mhat_on and float(torch.rand((), generator=g)) < float(args.decoder_denoise_p_mhat):
            sel = (torch.rand(real.shape, generator=g) < float(args.decoder_denoise_row_frac)).to(device) & real
            if bool(sel.any()):
                if v_rows.size(0) != 1:
                    raise ValueError("decoder-denoise m̂ 列只支持 batch_size=1 (ridge_unmix 逐窗形态)")
                # 延迟导入: 关态零依赖零导入成本 (条件创建纪律)
                from tools.analysis.v3_6.probe_decoder_fuzz_id import mhat_from_window

                with torch.autocast(device.type, enabled=False):
                    mhat = mhat_from_window(model, index.float(), real, fuzz["W"], fuzz["scale"])
                n = mhat.size(1)
                idx = sel[0, :n].nonzero(as_tuple=True)[0]
                if idx.numel():
                    v_dec[0, idx] = mhat[0, idx]
                    mhat_sel[0, idx] = True

        noise_sel = noise_sel & ~mhat_sel  # 撞行归替换列 (上面申报的覆盖语义)
        n_real = real.float().sum().clamp(min=1.0)
        stats = {
            "noise_frac": float(noise_sel.float().sum() / n_real),
            "mhat_frac": float(mhat_sel.float().sum() / n_real),
            "clean_frac": float((real & ~noise_sel & ~mhat_sel).float().sum() / n_real),
            "grade": float(s_hit) if s_hit is not None else -1.0,  # 修订 v2: 命中的 s 值, 未触发 = -1.0
            "clean_rows": (real & ~noise_sel & ~mhat_sel),  # (B, C) bool, step_model 干净水位仪表用
        }
    return v_dec.to(v_rows.dtype), stats


# ---------------------------------------------------------------------------
# Q20 多槽读出臂 (multi-slot readout, E119; 任务书冻结 v1 2026-08-29:
# docs/versions/v3.7/FLUED_V3_7_Q20_MULTISLOT_READOUT_20260829_CN.md) — b 格
# K 通道压缩状态 → decoder direct 口的读出端扩宽; 可训练范围 = 仅新增多槽
# 读出件 (k 槽查询 + 拼接投影 / CG 臂的可学段 2 投影), 端口 (decoder_in_mem)
# 与 decoder/backbone/写入侧全冻在 E118 收官态——端口作固定基板 = 「端口仍
# 是损耗源」前提的实验化身。默认全关 = 旧路径逐位不变。
# ---------------------------------------------------------------------------


def _multislot_readout_enabled(args) -> bool:
    return bool(getattr(args, "multislot_readout", False))


def _multislot_readout_rows(model, index: torch.Tensor, chunk_mask: torch.Tensor) -> torch.Tensor:
    """Q20 direct 腿读出行生产 (任务书 §3.3): index 行 → write_head_k gates →
    多槽读出件 → (B, C, d_mem) fp32 行。写入侧全冻 (本臂白名单 = 仅读出件):
    gates 在 no_grad 下复算 (常数件, 梯度只经读出件); autocast 关闭 + fp32,
    与探针 q20_k 列行生产同链 (串联测零域移, 去噪臂 m̂ 列同款纪律)。"""
    with torch.autocast(index.device.type, enabled=False):
        with torch.no_grad():
            gates_k = model.write_head_k(index.float())
        return model.multislot_readout(gates_k, chunk_mask)


def _multislot_readout_freeze(model) -> tuple[int, int]:
    """可训练范围钉死 = 仅多槽读出件 (任务书 §1 终审裁定项④)。
    (_decoder_denoise_freeze 的反向先例: 那里白名单是 decoder.*, 这里是
    multislot_readout.*。) tied byte_lookup 同账: named_parameters 去重后只在
    模型级名字出现一次 (decoder.byte_lookup 是同一参数的别名, 不命中白名单
    前缀) —— 按 E31/E34 裁定字节表是固定公尺, 留在冻结侧正是裁定语义;
    读出件自身参数不许被误冻 (两个方向都钉死)。Returns (n_trainable, n_frozen)。"""
    n_train = n_frozen = 0
    for name, param in model.named_parameters():
        if name.startswith("multislot_readout."):
            param.requires_grad_(True)
            n_train += 1
        else:
            param.requires_grad_(False)
            n_frozen += 1
    return n_train, n_frozen


def _multislot_readout_warm_start(model, fuzz_dir: str) -> str:
    """温启动初始化 (任务书 §1 终审裁定项④, 零变化律可判读性前提):
    - 投影 ← fuzz_id 落盘的 λopt=1.0 部署桥 W (折叠 RMS 预条件 scale 与截距
      行); k>1 臂只装槽 0 块、其余槽块置零 (t=0 各 k 臂读数相同, 零变化律
      对读干净)。
    - k 槽臂槽 0 ← ridge 段 1 主方向 (q20_ridge_dir.npz 落盘件,
      tools/analysis/v3_6/probe_q20_ridge_direction.py 产出); k>1 臂其余槽
      保留构造时随机初始化, 并与已有槽逐头 Gram-Schmidt 正交化。
    - CG 臂无槽查询, 只装段 2 投影。
    缺件/键不齐/形状不符响亮报错 (SystemExit), 不静默降级。Returns 日志注记。"""
    import numpy as np

    from flued.v36.model import CGRidgeReadout

    ms = model.multislot_readout  # 旗标开才创建 (main() 校验链已保证)
    c = model.config
    heads, hk, hv, d_mem = c.kda_heads, c.kda_head_k, c.kda_head_v, c.d_mem
    fuzz = _load_decoder_denoise_fuzz(fuzz_dir)  # λopt=1.0 部署桥 (loud-fail 内建)
    W, scale = fuzz["W"].float(), float(fuzz["scale"])  # (H*hv+1, d_mem), 末行截距
    if W.shape != (heads * hv + 1, d_mem):
        raise SystemExit(
            f"[s1][q20] 部署桥形状不符: W{tuple(W.shape)} != ({heads * hv + 1}, {d_mem}) —— "
            "fuzz_id 产物与本模型 H*hv/d_mem 不匹配, 检查 --multislot-readout-fuzz-id"
        )
    with torch.no_grad():
        if isinstance(ms, CGRidgeReadout):
            ms.proj.weight.copy_((W[:-1] / scale).T)
            ms.proj.bias.copy_(W[-1])
            return f"cg 臂: 段2 投影 <- 部署桥 (scale={scale:.4f})"
        # k 槽臂: 槽 0 <- ridge 段 1 主方向 (loud-fail 装载)
        ridge_path = Path(fuzz_dir) / "q20_ridge_dir.npz"
        if not ridge_path.exists():
            raise SystemExit(
                f"[s1][q20] ridge 段 1 主方向缺席: {ridge_path} —— 先对基座跑 "
                "tools/analysis/v3_6/probe_q20_ridge_direction.py 落盘 (不静默降级为随机初始化)"
            )
        z = np.load(ridge_path)
        if "q_ridge" not in z:
            raise SystemExit(f"[s1][q20] {ridge_path}: 缺 q_ridge 键 (实际键集 {list(z.keys())})")
        q_ridge = torch.from_numpy(np.asarray(z["q_ridge"], dtype=np.float32))
        if q_ridge.shape != (heads, hk):
            raise SystemExit(f"[s1][q20] q_ridge 形状不符: {tuple(q_ridge.shape)} != ({heads}, {hk})")
        ms.slot_query[0].copy_(q_ridge)
        # 其余槽: 构造时随机初始化保留, 与已有槽逐头 Gram-Schmidt 正交化
        basis = [F.normalize(ms.slot_query[0], dim=-1)]
        for j in range(1, ms.k):
            qj = ms.slot_query[j]
            for b in basis:
                qj = qj - (qj * b).sum(dim=-1, keepdim=True) * b
            ms.slot_query[j].copy_(qj)
            basis.append(F.normalize(ms.slot_query[j], dim=-1))
        # 投影: 槽 0 块 <- 部署桥 (折叠 scale), 其余槽块置零, 偏置 <- 截距行
        w = ms.proj.weight.view(d_mem, ms.k, heads * hv)
        w[:, 0].copy_((W[:-1] / scale).T)
        if ms.k > 1:
            w[:, 1:].zero_()
        ms.proj.bias.copy_(W[-1])
    return f"k={ms.k} 臂: 槽0<-ridge 主方向 + {ms.k - 1} 正交随机槽, 投影槽0块<-部署桥 (scale={scale:.4f})"


# ---------------------------------------------------------------------------
# E120 端到端点燃臂 (d 格 Δ 补测; 任务书冻结 v1+修订 v2 2026-09-03:
# docs/versions/v3_7/FLUED_V3_7_E120_END_TO_END_IGNITION_20260903_CN.md)
# ---------------------------------------------------------------------------


def _e120_enabled(args) -> bool:
    return bool(getattr(args, "e120_readout_swap", False))


def _e120_freeze_all(model) -> tuple[int, int]:
    """甲列冻结语义 (纯插拔, eval-only/探针侧): 全模型冻结——含新件
    e120_readout.* (温启动即最终态, 无可训参数)。Returns (n_trainable=0,
    n_frozen)。tied byte_lookup 同账: named_parameters 去重后只出现一次,
    冻结是全集, 无别名敞口。"""
    n_frozen = 0
    for _name, param in model.named_parameters():
        param.requires_grad_(False)
        n_frozen += 1
    return 0, n_frozen


def _e120_unfreeze_all(model) -> tuple[int, int]:
    """乙列解冻语义 (主格): 全模型解冻——含新件 e120_readout.* 与被替换的
    生产读出链外件 (后者无梯度通路, 留在原值)。freeze_prefixes 已在 main()
    旗标校验段清空 (25b 配方继承的前端冻结不进本臂), 这里是确定性兜底。
    Returns (n_trainable, n_frozen=0)。"""
    n_train = 0
    for _name, param in model.named_parameters():
        param.requires_grad_(True)
        n_train += 1
    return n_train, 0


def _e120_warm_start(model, fit_dir: str) -> str:
    """E120 温启动初始化 (任务书 §1: 温启动源 = d 格基座自产状态上的闭式解,
    预跑 probe_e120_warmstart_fit.py 落盘):
    - slot_query[0] ← ridge 段 1 主方向 (q_ridge_dir.npz 键 q_ridge, (H, hk));
    - proj ← 部署桥 (bridge_deploy.npz 键 W/scale: 折叠 RMS 预条件 scale +
      末行截距; 应用形 = apply_bridge 同款 [v̂/scale, 1] @ W)。
    缺目录/缺文件/缺键/形状不符响亮报错 (SystemExit), 不静默降级——t=0 必须
    就是 E119 定型档, 零变化律判读才有基尺。Returns 日志注记。"""
    import numpy as np

    rd = model.e120_readout  # 旗标开才创建 (main() 校验链已保证)
    c = model.config
    heads, hk, hv, d_pack = c.kda_heads, c.kda_head_k, c.kda_head_v, c.d_pack
    fit = Path(fit_dir)
    if not fit.is_dir():
        raise SystemExit(
            f"[s1][e120] 温启动产物目录缺席: {fit} —— 先跑 "
            "tools/analysis/v3_6/probe_e120_warmstart_fit.py 落盘 (不静默降级为随机初始化)"
        )
    bridge_path = fit / "bridge_deploy.npz"
    if not bridge_path.exists():
        raise SystemExit(f"[s1][e120] 部署桥缺席: {bridge_path}")
    z = np.load(bridge_path)
    for key in ("W", "scale", "lam"):
        if key not in z:
            raise SystemExit(f"[s1][e120] {bridge_path}: 缺 {key} 键 (实际键集 {list(z.keys())})")
    W = torch.from_numpy(np.asarray(z["W"], dtype=np.float32))
    scale = float(z["scale"])
    if W.shape != (heads * hv + 1, d_pack):
        raise SystemExit(
            f"[s1][e120] 部署桥形状不符: W{tuple(W.shape)} != ({heads * hv + 1}, {d_pack}) —— "
            "fit 产物与本模型 H*hv/d_pack 不匹配, 检查 --e120-fit-dir"
        )
    ridge_path = fit / "q_ridge_dir.npz"
    if not ridge_path.exists():
        raise SystemExit(f"[s1][e120] ridge 段 1 主方向缺席: {ridge_path}")
    zr = np.load(ridge_path)
    if "q_ridge" not in zr:
        raise SystemExit(f"[s1][e120] {ridge_path}: 缺 q_ridge 键 (实际键集 {list(zr.keys())})")
    q_ridge = torch.from_numpy(np.asarray(zr["q_ridge"], dtype=np.float32))
    if q_ridge.shape != (heads, hk):
        raise SystemExit(f"[s1][e120] q_ridge 形状不符: {tuple(q_ridge.shape)} != ({heads}, {hk})")
    with torch.no_grad():
        rd.slot_query[0].copy_(q_ridge)
        rd.proj.weight.copy_((W[:-1] / scale).T)
        rd.proj.bias.copy_(W[-1])
    return (
        f"slot_query<-q_ridge 主方向 (||q||={float(q_ridge.norm()):.4f}), "
        f"proj<-部署桥 (scale={scale:.4f}, λ={float(z['lam']):.1f})"
    )


# ---------------------------------------------------------------------------
# Q18 v2 读出墙裁定臂 — B 计划 (2026-08-28): A/A′ 臂移植进 s1 骨架
# ---------------------------------------------------------------------------
# 为什么移植 (任务书 §6 楔死事故簿): Q17/Q18 独立训练器在双机双栈上间歇楔死
# (日志停摆+主线程 100% CPU+GPU 忙; fresh 活 2-6K 步, resume 速楔, 楔点随权重
# 态; 全录 docs/versions/v3.7/FLUED_V3_7_Q18_V2_READOUT_WALL_20260827_CN.md
# §6), s1 骨架经 20K×多臂 (Q12-Q15) 验证稳定——移植目的是稳定宿主, 机制一字
# 不改: 流式双态读出 (_q17_stream_encode/_q17_stream_channel)/oracle 态构造/
# α 范数匹配/链重初始化/闭式温启动全部从独立训练器模块 import 调用 (懒导入护
# 栏: train_q17_oracle_readout 顶层 import 本模块, s1 顶层反向 import 会成
# 环), 本节只有挂接控制流, 零机制复制。
#
# 形态 (与独立训练器逐项对齐): 模型从 --q18-base-ckpt (Q15 正臂 run dir)
# strict 加载; 链范围 = realign×2+readout_query×2+align_k/align_v (在
# backbone 内)+backbone+decoder_in+decoder (Q17 修订 v1 足迹), A 臂固定种子
# 从零 / A′ 臂 Q19 闭式温启动 (q18._q18_warmstart + 零变化律自检, 不过响亮
# 退出臂作废), 其余全冻; 训练步把 SLM store 行换成流式双态读出行 (A 臂与
# A′ oracle 列 p≡1.0 / natural 列 p≡0.0), 损失 = echo CE (唯一); eval
# (train=False) 走标准 s1 路径——独立训练器收官 eval 就是 s1.evaluate 全形
# 态, 逐一对齐。预算 A 40K / A′ 20K (--q18-steps 覆写), LR 1e-3 + warmup
# 200 + cosine→0 (强制覆写, 独立训练器硬编码同款), batch=1, 种子参数化。

_Q18_CONFIG_EXCLUDE = frozenset({
    # IO/运行时键不回填: out_dir/run_id 继承基座会把续跑写进基座 run dir
    # (事故级); init_checkpoint 是基座自己的 S0 起点 (Q18 链初始化在 strict
    # 基座之上做, 不回链 S0); eval_only/config 是本层旗标。
    "out_dir", "run_id", "init_checkpoint", "init_prefixes", "eval_only", "config",
})

_Q18_DEPS = None  # (q17 模块, q18 模块) 懒导入缓存


def _q18_enabled(args) -> bool:
    return bool(getattr(args, "q18_arm", ""))


def _q18_deps():
    """懒导入独立训练器模块 (循环护栏: train_q17_oracle_readout 顶层 import
    本模块, s1 顶层反向 import 会成环; 首次调用后缓存)。"""
    global _Q18_DEPS
    if _Q18_DEPS is None:
        from tools.train.v3_6 import train_q17_oracle_readout as q17m
        from tools.train.v3_6 import train_q18_readout_wall as q18m

        _Q18_DEPS = (q17m, q18m)
    return _Q18_DEPS


def _q18_base_config_defaults(base_ckpt: str) -> dict:
    """基座 run dir 的 resolved_config.json → parser defaults (窗规格/管束/
    模型形态全部继承基座——独立训练器 _q17_load_models 的 cfg 同源); IO/运
    行时键剔除 (_Q18_CONFIG_EXCLUDE); data_manifest 强制空 (独立训练器同款)。"""
    cfg_path = Path(base_ckpt) / "resolved_config.json"
    if not cfg_path.exists():
        raise SystemExit(
            f"--q18-base-ckpt {base_ckpt}: resolved_config.json 缺席 (预期 Q15 正臂 run dir)"
        )
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg["data_manifest"] = ""
    return {k: v for k, v in cfg.items() if k not in _Q18_CONFIG_EXCLUDE}


def _q18_validate_args(args) -> None:
    """旗标响亮校验: 不合法组合点火前 SystemExit, 不静默降级。"""
    base = Path(args.q18_base_ckpt) if args.q18_base_ckpt else None
    if base is None or not (base / "resolved_config.json").exists():
        raise SystemExit("--q18-arm 需要 --q18-base-ckpt <Q15 正臂 run dir> (resolved_config.json 可读)")
    if not (base / "latest.pt").exists():
        raise SystemExit(f"--q18-base-ckpt {args.q18_base_ckpt}: latest.pt 缺席")
    if getattr(args, "backbone_mode", "") != "slm" or getattr(args, "v_row_source", "") != "state":
        raise SystemExit(
            "Q18 预期 d 格基座 (backbone_mode='slm', v_row_source='state'), got "
            f"backbone_mode={getattr(args, 'backbone_mode', None)!r} "
            f"v_row_source={getattr(args, 'v_row_source', None)!r}"
        )
    if args.q18_arm == "Aprime":
        donor = Path(args.q18_donor_ckpt)
        if not (donor / "resolved_config.json").exists() or not (donor / "latest.pt").exists():
            raise SystemExit(
                "A′ 臂温启动需要 --q18-donor-ckpt <b 格 v371 run dir> (Q19 D1 donor "
                f"端口方案), got {args.q18_donor_ckpt!r}"
            )
    if args.eval_only:
        raise SystemExit("Q18 模式不组合 --eval-only (收官 eval 由训练主循环尾部承担, 独立训练器同形态)")
    if float(getattr(args, "cloze_prob", 0.0)) > 0.0 or float(getattr(args, "retrieval_prob", 0.0)) > 0.0:
        raise SystemExit("Q18 模式不组合 cloze/retrieval (Q15 管束只有 burst; 独立训练器同口径)")


def _q18_seed_streams(args) -> None:
    """抽签流 (任务书 §4 可复现; 独立训练器 _seed_streams 同 discipline):
    mask/burst 流 + 退火抽签流 (Q18 独立偏移, 与 Q17 的 101_033 不混)。
    A′ 温启动/零变化律自检消耗抽签流后必须重调本函数 (RNG 隔离)。"""
    _q17m, q18m = _q18_deps()
    _MASK_GENERATOR.manual_seed(args.seed)
    _BURST_GENERATOR.manual_seed(args.seed + _BURST_SEED_OFFSET)
    q18m._Q18_GENERATOR.manual_seed(args.seed + q18m._Q18_SEED_OFFSET)


def _q18_setup_chain(model, args, device, out_dir: Path, resuming: bool):
    """链初始化 (机制零复制): 全冻 → A 臂固定种子从零 (Q17 修订 v1 足迹) /
    A′ 臂 Q19 闭式温启动 + 零变化律自检 (不过响亮退出, 臂作废重查不许判负)
    → 解冻链。resume 跳过初始化 (latest.pt 回放覆盖链权重, 独立训练器同款)。
    Returns warmstart report (A 臂/resume 为 None)。"""
    q17m, q18m = _q18_deps()
    for p_ in model.parameters():
        p_.requires_grad_(False)
    warm_report = None
    if not resuming and args.q18_arm == "A":
        q17m._q17_reinit_readout_chain(model, args, args.seed)
    elif not resuming:
        donor, dns, donor_step = q18m.load_model(Path(args.q18_donor_ckpt), device)
        # D1 接口断言 (Q19 同款, loud): donor 必须有 decoder_in_mem 且 v=memory
        if getattr(dns, "v_row_source", "") != "memory" or not hasattr(donor, "decoder_in_mem"):
            raise ValueError(
                f"{args.q18_donor_ckpt}: donor 缺 decoder_in_mem "
                f"(v_row_source={getattr(dns, 'v_row_source', None)!r})"
            )
        for k in ("max_chunks", "max_span"):
            if getattr(args, k) != getattr(dns, k):
                raise ValueError(f"base/donor {k} 不一致: {getattr(args, k)} vs {getattr(dns, k)}")
        print(f"[s1][q18] donor={Path(args.q18_donor_ckpt).name} step={donor_step}", flush=True)
        warm_report = q18m._q18_warmstart(
            model, donor, args, device, args.q18_warmstart,
            int(args.q18_calib_windows), float(args.lam_unmix), float(args.lam_stage2),
        )
        (out_dir / "warmstart_report.json").write_text(
            json.dumps(warm_report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        del donor  # 标定完即释放 (16GB 显存纪律)
        if device.type == "cuda":
            torch.cuda.empty_cache()
        # 零变化律自检 (任务书 §1 预注册; 考场口径 Q18-D7): 温启动后首步 fine
        # 细格 acc 必须过阈, 不过响亮退出——初始化没接通, 臂作废重查不许判负
        p_col = q18m._q18_course_p(args.q18_arm, args.q18_warmstart, 0)
        zc_mean, zc_accs = q18m._q18_zero_change_check(
            model, args, device, p_col, int(args.q18_zc_windows), float(args.q18_zc_threshold)
        )
        warm_report["zero_change"] = {
            "threshold": float(args.q18_zc_threshold),
            "windows": int(args.q18_zc_windows),
            "metric": "fine 细格全槽 as-encoded acc, 判官=backbone 腿 (Q18-D7)",
            "backbone_accs": [round(a, 4) for a in zc_accs["backbone"]],
            "direct_accs": [round(a, 4) for a in zc_accs["direct"]],
            "mean": round(zc_mean, 4),
        }
        (out_dir / "warmstart_report.json").write_text(
            json.dumps(warm_report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(
            f"[s1][q18] 零变化律自检通过: 首步细格 acc(backbone)={zc_mean:.4f} > {args.q18_zc_threshold}",
            flush=True,
        )
        _q18_seed_streams(args)  # 检查后重 seed 训练流 (RNG 隔离声明落到实处)
    trainable = q17m._q17_unfreeze_chain(model)
    print(
        f"[s1][q18] arm={args.q18_arm} "
        f"{'温启动 ' + args.q18_warmstart if args.q18_arm == 'Aprime' else '从零重初始化'} "
        f"(seed={args.seed}), 可训练参数 {sum(p_.numel() for p_ in trainable)}"
        + (" (resume: 跳过链初始化)" if resuming else ""),
        flush=True,
    )
    return warm_report


def _q18_train_step(model, batch, args, device):
    """Q18 训练步: 整体委托 q17._q17_step (流式双态读出 + echo CE, 机制零复
    制——splice/遮蔽/抽签流全部读本模块全局, 与独立训练器同一数据源)。
    Returns (loss_or_None, metrics-tensor-dict); loss=None = echo 离网 (burst
    未激活窗), 调用侧步进照走不参训 (独立训练器同款)。"""
    q17m, q18m = _q18_deps()
    p = q18m._q18_course_p(args.q18_arm, getattr(args, "q18_warmstart", "oracle"), 0)  # 课程断言: 恒定
    loss, m = q17m._q17_step(model, batch[0], args, device, p, q18m._Q18_GENERATOR)
    metrics = {k: torch.tensor(float(v), device=device) for k, v in m.items()}
    if loss is None:
        return None, metrics
    metrics["loss"] = loss.detach()
    return loss, metrics


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


def s1_forward(model, source: torch.Tensor, args, clean=None, byte_mask=None, retrieval_metas=None, burst_metas_q15=None, store_block_override=None, need_attn: bool = False, train: bool = False) -> dict:
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
            model, source, args, clean=clean, byte_mask=byte_mask, retrieval_metas=retrieval_metas,
            burst_metas_q15=burst_metas_q15, store_block_override=store_block_override,
            need_attn=need_attn, train=train,
        )
    if retrieval_metas is not None or burst_metas_q15 is not None or store_block_override is not None:
        raise ValueError(
            "retrieval/burst store_block threading requires backbone_mode='slm' (v3.7); "
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


def _slm_forward(model, source: torch.Tensor, args, clean=None, byte_mask=None, retrieval_metas=None, burst_metas_q15=None, store_block_override=None, need_attn: bool = False, train: bool = False) -> dict:
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

    Q15 (任务书 2026-08-25 §2/§7.1): ``store_block_override`` 给了就直接用
    (优先级最高, 预留给调用侧自带网格的用法); 否则 ``burst_metas_q15`` 在本
    函数内建 burst store_block (``_burst_store_block``, r 恒 1.0 零随机抽,
    train/eval 同开 -- 剔除是任务定义) -- 构造点在此而非 step_model, 因为
    chunk 网格只在这里存在; 再否则走 legacy retrieval 路径. ``need_attn``
    线进 backbone block-1 手工注意力, 概率随 ``block1_attn`` 键带出 (关时
    None). ``train`` 只喂 decoder 去噪臂 (任务书 2026-08-29): True 且旗标开
    时 direct 腿吃扰动副本; False (默认/eval) = 零扰动, 旧路径逐位不变。
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
    if store_block_override is not None:
        store_block = store_block_override  # Q15: 调用侧直接给, 优先级最高
    elif burst_metas_q15 is not None:
        # Q15 §2 压缩区激励改造: 第 1..R-1 次出现覆盖的 store 行档 a 剔除
        store_block = _burst_store_block(burst_metas_q15, chunks)
    elif retrieval_metas is not None:
        store_block, retrieval_block_rate = _retrieval_store_block(
            retrieval_metas, chunks, float(getattr(args, "retrieval_block_prob", 0.0)), _RETRIEVAL_GENERATOR
        )
    # fork 2: multi-view store rows when readout_views > 1 (classic rows otherwise)
    backbone_out = model.backbone(
        k_store if k_store is not None else k_rows,
        v_store if v_store is not None else v_rows,
        chunks.chunk_mask, pos, chunk_byte_off=chunk_byte_off,
        store_block=store_block,
        need_attn=need_attn,
    )
    cond_backbone = backbone_out + pos
    dec_in = model.decoder_in if model.config.v_row_source == "state" else model.decoder_in_mem
    # decoder 去噪臂 (任务书 FLUED_V3_7_DECODER_DENOISE_20260829_CN.md §1, 冻结
    # v1.1): 扰动只发生在 direct 腿的输入副本上——v_rows 本体不动 (上面的
    # backbone 腿与 step_model 的 predict 锚都吃它)。默认关 = 零随机流零行为
    # 变化 (条件创建纪律同 decoder_in_mem 先例: 旧路径逐位不变); train=False
    # (eval) 永不扰动。
    denoise_stats = None
    v_rows_direct = v_rows
    if _decoder_denoise_enabled(args) and train and model.config.v_row_source == "memory":
        v_rows_direct, denoise_stats = _decoder_denoise_perturb(model, v_rows, chunks, index, args)
    # Q20 多槽读出臂 (multi-slot readout, E119; 任务书冻结 v1 §3.3): train 态
    # 旗标开时构造 q20_rows 喂 direct 腿——v_rows 本体不动 (上面的 backbone
    # 腿与 step_model 的 predict 锚照吃它), 副本机制与去噪臂同位同纪律;
    # 默认关 = 旧路径逐位不变。不与去噪臂同开 (main() 响亮校验); 旗标开而
    # 模型缺件 (配置未开) = AttributeError 响亮暴露, 不静默落旧路径。
    q20_engaged = 0.0
    if _multislot_readout_enabled(args) and train and model.config.v_row_source == "memory":
        v_rows_direct = _multislot_readout_rows(model, index, chunks.chunk_mask)
        q20_engaged = 1.0
    cond_direct = dec_in(v_rows_direct) + pos
    logits_direct = model.decoder(cond_direct, chunks.token_mask)
    logits_backbone = model.decoder(cond_backbone, chunks.token_mask)
    return {
        "logits_direct": logits_direct,
        "logits_backbone": logits_backbone,
        "logits_backbone_mid": None,
        "content": None,  # content channel retired in slm mode (consensus §4)
        "backbone_out": backbone_out,
        "v_rows": v_rows,  # decoder-side V source rows (the predict anchor, §1.4)
        "denoise_stats": denoise_stats,  # decoder 去噪臂扰动计数 (None = 关/eval, 旧路径不变)
        "q20_engaged": q20_engaged,  # Q20 多槽读出臂接通计 (1.0 = 本前向 direct 腿吃了读出行; 关态/eval 零占位)
        "memory": memory,
        "index": index,  # summarizer K rows (resident key-geometry metrics, E80 补充 2)
        "retrieval_block_rate": retrieval_block_rate,  # 档 a excision hit rate (0.0 when off)
        "block1_attn": model.backbone.last_block1_attn,  # Q15 need_attn 概率 (None when off)
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
            mus.append(off.mean())
            mx.append(off.max())
            try:
                eig = torch.linalg.eigvalsh(G).clamp(min=0.0)
                prs.append(eig.sum() ** 2 / eig.square().sum().clamp(min=1e-12) / kh.size(0))
            except torch._C._LinAlgError:
                # dashboard must never kill training: degenerate states (e.g.
                # runaway state_norm at hot LR) make eigh fail to converge —
                # report a placeholder, not a crash (2026-08-22 40K 延长臂教训)
                prs.append(torch.zeros((), device=kh.device))
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
    if _q18_enabled(args) and train:
        # Q18 v2 读出墙裁定臂 (B 计划移植): 训练步整体委托独立训练器机制
        # (_q18_train_step → q17._q17_step, echo CE 唯一损失); eval
        # (train=False) 走下方标准 s1 路径——独立训练器收官 eval 即
        # s1.evaluate 全形态, 逐一对齐。
        return _q18_train_step(model, batch, args, device)
    clean = batch[0]
    q15_on = _q15_enabled(args)
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
            int(getattr(args, "retrieval_examples", 0)),
            # A2② 窗 = chunk-grid byte capacity (canonical 64x64 = 4096B)
            int(args.max_chunks) * int(args.max_span),
        )
    burst_metas = None
    if _burst_enabled(args):
        # Q13 突发性注入臂 (prereg 2026-08-22): slm-only; the legacy
        # xattn/paged/draft/attn paths and simultaneously live cloze/retrieval
        # tasks are N/A and must fail loudly, not silently.
        if getattr(model.config, "backbone_mode", "") != "slm":
            raise ValueError(
                "burst (--burst-prob>0) requires backbone_mode='slm' (Q13 突发性注入臂); "
                "legacy xattn/paged/draft/attn paths are N/A"
            )
        if cloze_metas is not None or retrieval_metas is not None:
            raise ValueError(
                "burst (--burst-prob>0) is mutually exclusive with cloze (--cloze-prob>0) "
                "and retrieval (--retrieval-prob>0) (同窗只允许一种注入任务)"
            )
        if _BURST_SAMPLER is None:
            raise ValueError(
                "burst corpus sampler not loaded: main() opens --data-path via "
                "CorpusSampler before training/eval (Q13 防背护栏: 每窗现采随机段)"
            )
        burst_stats = {"drawn": 0, "spliced": 0, "sieve_measured": 0, "sieve_rejected": 0}
        clean, burst_metas = _splice_burst(
            clean, float(args.burst_prob), _BURST_GENERATOR, _BURST_SAMPLER,
            int(getattr(args, "burst_repeat", 3)),
            int(getattr(args, "burst_tail_max_chars", 4)),
            # Q14 先验筛: 参考模型 (开工 checkpoint 固定基准) 只在旗标开时挂载
            sieve_model=_BURST_SIEVE_MODEL if bool(getattr(args, "burst_prior_sieve", False)) else None,
            stats=burst_stats,
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
    if burst_metas is not None:
        # Q13 discipline (see _burst_mask_overrides): the R-th occurrence's
        # tail force-masked, the R-1 earlier occurrences force-unmasked.
        byte_mask = _burst_mask_overrides(byte_mask, burst_metas)
    source = clean.masked_fill(byte_mask, MASK_ID)
    with torch.autocast("cuda", dtype=torch.bfloat16, enabled=args.amp and device.type == "cuda"):
        out = s1_forward(
            model, source, args, clean=clean, byte_mask=byte_mask, retrieval_metas=retrieval_metas,
            # Q15: 剔除是任务定义, train/eval 同开 (§7.2); need_attn 只在训练
            # 前向开 (L_attend 的奖励靶点, eval 零成本零形态变化)
            burst_metas_q15=burst_metas if q15_on else None,
            need_attn=q15_on and train,
            train=train,  # decoder 去噪臂: direct 腿扰动只在训练前向 (关态零影响)
        )
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
    # burst echo slot 网格在这里算一次, 供三处共用: Q15 §3.2 的 echo 剔除
    # (train-only, eval 不动网格)、Q15 三件套、burst 指标块.
    burst_slot = burst_active = None
    if burst_metas is not None:
        burst_slot, burst_active = _cloze_slot_grid(
            burst_metas, chunks.chunk_ids, chunks.offsets, args.max_chunks, args.max_span
        )
        if q15_on and train:
            # Q15 §3.2: echo 槽位从常规 completion 网格剔除 (防双重计分;
            # codec 覆盖由门控结果损失接续 -- g→1 等价全覆盖, g→0 段尾暂不
            # 被任何项覆盖, 条件覆盖即设计)
            comp_slot_mask = comp_slot_mask & ~burst_slot
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
        # Q12 示例密集形态 (修订案 v3 / 附录 A2②): window-budget and
        # construction-defect gauges; all-zero in the example-free form
        # (metas carry no budget fields there).
        "retrieval_budget_ratio": torch.zeros((), device=device),
        "retrieval_examples": torch.zeros((), device=device),
        "retrieval_drop_rate": torch.zeros((), device=device),
        "retrieval_defect": torch.zeros((), device=device),
    }
    if retrieval_metas is not None:
        retrieval_slot, retrieval_active = _cloze_slot_grid(
            retrieval_metas, chunks.chunk_ids, chunks.offsets, args.max_chunks, args.max_span
        )
        retrieval_loss, _retrieval_rm = _retrieval_loss_and_metrics(
            out["logits_backbone"], comp_targets, retrieval_slot, retrieval_active
        )
        # keep the pre-initialized Q12 budget gauges (setdefault zeros) — the
        # loss helper returns only the base keys, and splice-free batches
        # would otherwise KeyError downstream
        retrieval_metrics.update(_retrieval_rm)
        retrieval_metrics["retrieval_block_rate"] = torch.tensor(
            out.get("retrieval_block_rate", 0.0), device=device
        )
        # Q12 budget gauges (A2②): means over the spliced samples; the
        # defect count is the 查询段被挤到窗沿 弃用计数 -- spliced but the
        # query echo never fully landed on the chunk grid (the per-sample
        # causal-visibility assert lives in the slot grid itself).
        spliced = [(b, m) for b, m in enumerate(retrieval_metas) if m is not None]
        if spliced:
            n_sp = float(len(spliced))
            n_ex = sum(int(m.get("n_examples", 0)) for _, m in spliced)
            n_dr = sum(int(m.get("n_dropped", 0)) for _, m in spliced)
            retrieval_metrics["retrieval_budget_ratio"] = torch.tensor(
                sum(float(m.get("budget_ratio", 0.0)) for _, m in spliced) / n_sp, device=device
            )
            retrieval_metrics["retrieval_examples"] = torch.tensor(n_ex / n_sp, device=device)
            retrieval_metrics["retrieval_drop_rate"] = torch.tensor(
                n_dr / (n_ex + n_dr) if (n_ex + n_dr) else 0.0, device=device
            )
            retrieval_metrics["retrieval_defect"] = torch.tensor(
                sum(0.0 if bool(retrieval_active[b]) else 1.0 for b, _ in spliced) / n_sp,
                device=device,
            )

    # Q13 突发性注入臂 (prereg 2026-08-22 §2): NO new loss term -- 注入只改
    # 数据分布, the codec three tasks already cover the masked tail. Metrics
    # only, zero placeholders keep the log schema aligned when off.
    burst_metrics = {
        "burst_tail_byte_acc": torch.zeros((), device=device),
        "burst_tail_exact": torch.zeros((), device=device),
        "burst_count": torch.zeros((), device=device),
        "burst_tail_chars": torch.zeros((), device=device),
        # Q14 (修订案 2026-08-23 §2.2): 先验筛拒收率与产出率 (激活率 =
        # 激活样本/抽中样本); 筛关时 reject_rate 恒 0, 任务关时双双零占位.
        "burst_sieve_reject_rate": torch.zeros((), device=device),
        "burst_yield": torch.zeros((), device=device),
    }
    if burst_metas is not None:
        # burst_slot/burst_active 已在 comp 网格处算好 (Q15 §3.2 剔除共用)
        burst_metrics.update(
            _burst_metrics(out["logits_backbone"], comp_targets, burst_slot, burst_active, burst_metas)
        )
        # Q14 §2.2 产出率入册: 无抽中样本的批次是空泡 (yield 记 1.0, 不计失败)
        drawn = burst_stats.get("drawn", 0)
        measured = burst_stats.get("sieve_measured", 0)
        burst_metrics["burst_sieve_reject_rate"] = torch.tensor(
            burst_stats["sieve_rejected"] / measured if measured else 0.0, device=device
        )
        burst_metrics["burst_yield"] = torch.tensor(
            burst_stats["spliced"] / drawn if drawn else 1.0, device=device
        )

    # Q15 回路养成臂三件套 (任务书 2026-08-25 §3, 全部 train-only; eval 零
    # 占位, 网格不动 -- §7.2 形态纪律). λ 每步从 args 读 (回调线 §5 原地降权).
    q15_metrics = {
        "q15_attend_mass": torch.zeros((), device=device),
        "q15_attend_maxmass": torch.zeros((), device=device),  # §3.2v1: 门所见单头最大 T 质量
        "q15_attend_chance": torch.zeros((), device=device),  # §3.2v1: 均匀基线 (判读矩阵基线读数)
        "q15_attend_loss": torch.zeros((), device=device),
        "q15_gate_mean": torch.zeros((), device=device),
        "q15_echo_loss": torch.zeros((), device=device),
        "q15_couple_loss": torch.zeros((), device=device),
        "q15_twin_d": torch.zeros((), device=device),
        "q15_twin_count": torch.zeros((), device=device),
    }
    attend_loss = torch.zeros((), device=device)
    echo_loss = torch.zeros((), device=device)
    couple_loss = torch.zeros((), device=device)
    if q15_on and train and burst_metas is not None:
        attn = out.get("block1_attn")
        if attn is None:
            raise ValueError(
                "Q15 train forward requires need_attn=True (block1_attn missing) -- "
                "L_attend 的奖励靶点缺席, 响亮报错不静默"
            )
        masses, maxmasses, chances, ces = [], [], [], []
        for b, m in enumerate(burst_metas):
            if m is None or not bool(burst_active[b]):
                continue
            got = _q15_echo_mass(
                attn[b], m, chunks.chunk_ids[b], chunks.offsets[b], chunks.chunk_mask[b]
            )
            if got is None:
                continue
            mass_i, maxmass_i, chance_i, q_i, s_i = got
            masses.append(mass_i)
            maxmasses.append(maxmass_i)
            chances.append(chance_i)
            logit_i = out["logits_backbone"][b, q_i, s_i].float()  # (n_echo, V)
            ces.append(F.cross_entropy(logit_i, comp_targets[b, q_i, s_i], reduction="none"))
        if masses:
            # §3.1: mass 逐 echo 字节 (逐头求和, L_attend 公式不变). §3.2
            # 修订 v1: 门输入 = 单头超基线超出量 (max_h T 质量 − 该位置均匀
            # 基线 chance); g 取 stop-gradient (反捷径条款, 实现层改写已入册:
            # 不 detach 模型可压小 g 把损失幅度趋零). chance 由索引计数构成,
            # 天然无梯度.
            mass = torch.cat(masses)
            maxmass = torch.cat(maxmasses)
            chance = torch.cat(chances)
            ce = torch.cat(ces)
            attend_loss = (-torch.log(mass + _Q15_EPS)).mean()
            gate = _q15_gate(maxmass.detach(), chance)
            echo_loss = (gate * ce).mean()
            q15_metrics["q15_attend_mass"] = mass.detach().mean()
            q15_metrics["q15_attend_maxmass"] = maxmass.detach().mean()
            q15_metrics["q15_attend_chance"] = chance.mean()
            q15_metrics["q15_attend_loss"] = attend_loss.detach()
            q15_metrics["q15_gate_mean"] = gate.mean()
            q15_metrics["q15_echo_loss"] = echo_loss.detach()
        # §3.3 反作弊对偶: 孪生选择消耗 _BURST_GENERATOR 每条 splice 样本一抽
        # (固定顺序, 同 retrieval block 抽取纪律); 篡改本身零随机流; twin 前向
        # 带梯度但只取 logits_backbone 供铰链, 不进任何 codec 损失/指标 (§7.3)
        twin_sel = []
        for b, m in enumerate(burst_metas):
            if m is None:
                continue
            u = float(torch.rand((), generator=_BURST_GENERATOR))
            if u >= _Q15_TWIN_P or not bool(burst_active[b]):
                continue
            twin_sel.append(b)
        if twin_sel:
            width = clean.size(1)
            twin_clean = clean.new_full((len(twin_sel), width), PAD_ID)
            for i, b in enumerate(twin_sel):
                raw = bytes(int(x) - BYTE_OFFSET for x in clean[b].tolist() if int(x) != PAD_ID)
                tb = _burst_twin_bytes(raw, burst_metas[b])
                twin_clean[i, : len(tb)] = torch.tensor(
                    [x + BYTE_OFFSET for x in tb], dtype=clean.dtype
                )
            twin_source = twin_clean.masked_fill(byte_mask[twin_sel], MASK_ID)  # 同一 byte_mask 子集
            with torch.autocast("cuda", dtype=torch.bfloat16, enabled=args.amp and device.type == "cuda"):
                twin_out = s1_forward(
                    model, twin_source, args,
                    burst_metas_q15=[burst_metas[b] for b in twin_sel],
                    need_attn=False,
                )
            twin_metas = [burst_metas[b] for b in twin_sel]
            twin_slot, twin_active = _cloze_slot_grid(
                twin_metas, twin_out["chunks"].chunk_ids, twin_out["chunks"].offsets,
                args.max_chunks, args.max_span,
            )
            ds = []
            for i, b in enumerate(twin_sel):
                if not bool(twin_active[i]):
                    continue
                p_clean = torch.softmax(out["logits_backbone"][b][burst_slot[b]].float(), dim=-1)
                p_twin = torch.softmax(twin_out["logits_backbone"][i][twin_slot[i]].float(), dim=-1)
                if p_clean.size(0) != p_twin.size(0):
                    continue  # 篡改改了分段导致槽数不一致 -- 条目跳过, 不计入铰链
                # ½·‖softmax(clean)−softmax(twin)‖₁ 逐 echo 槽位 (∈[0,1])
                ds.append(0.5 * (p_clean - p_twin).abs().sum(dim=-1).mean())
            q15_metrics["q15_twin_count"] = torch.tensor(
                len(ds) / clean.size(0), device=device
            )
            if ds:
                d = torch.stack(ds)
                couple_loss = torch.clamp(_Q15_TWIN_M - d, min=0.0).mean()  # m=0.1 冻结
                q15_metrics["q15_couple_loss"] = couple_loss.detach()
                q15_metrics["q15_twin_d"] = d.detach().mean()

    lam_att = float(getattr(args, "q15_lambda_att", _Q15_LAMBDA_ATT))
    lam_out = getattr(args, "q15_lambda_out", None)
    lam_out = float(args.task2_loss_weight) if lam_out is None else float(lam_out)  # λ_out 继承 task2_loss_weight
    lam_couple = float(getattr(args, "q15_lambda_couple", _Q15_LAMBDA_COUPLE))
    loss = (
        args.task1_loss_weight * direct_loss
        + args.task2_loss_weight * completion_loss
        + args.predict_weight * predict_loss
        + getattr(args, "cloze_weight", 0.3) * cloze_loss
        + getattr(args, "retrieval_weight", 1.0) * retrieval_loss
        + lam_att * attend_loss
        + lam_out * echo_loss
        + lam_couple * couple_loss
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
        "retrieval_budget_ratio": retrieval_metrics["retrieval_budget_ratio"],
        "retrieval_examples": retrieval_metrics["retrieval_examples"],
        "retrieval_drop_rate": retrieval_metrics["retrieval_drop_rate"],
        "retrieval_defect": retrieval_metrics["retrieval_defect"],
        "burst_tail_byte_acc": burst_metrics["burst_tail_byte_acc"],
        "burst_tail_exact": burst_metrics["burst_tail_exact"],
        "burst_count": burst_metrics["burst_count"],
        "burst_tail_chars": burst_metrics["burst_tail_chars"],
        "burst_sieve_reject_rate": burst_metrics["burst_sieve_reject_rate"],
        "burst_yield": burst_metrics["burst_yield"],
        "q15_attend_mass": q15_metrics["q15_attend_mass"],
        "q15_attend_maxmass": q15_metrics["q15_attend_maxmass"],
        "q15_attend_chance": q15_metrics["q15_attend_chance"],
        "q15_attend_loss": q15_metrics["q15_attend_loss"],
        "q15_gate_mean": q15_metrics["q15_gate_mean"],
        "q15_echo_loss": q15_metrics["q15_echo_loss"],
        "q15_couple_loss": q15_metrics["q15_couple_loss"],
        "q15_twin_d": q15_metrics["q15_twin_d"],
        "q15_twin_count": q15_metrics["q15_twin_count"],
        "mask_rate": (byte_mask.float().sum() / valid.float().sum().clamp(min=1.0)).detach(),
        "truncated_tokens": chunks.pack_info["truncated_tokens"].float().sum().detach(),
        "cut_capacity_overflow": out["cut_overflow"].float().sum().detach(),
        "chunks_per_sample": chunks.chunk_mask.float().sum(dim=1).mean().detach(),
        "hard_cut_fraction": out["hard_cut_fraction"].detach(),
        "state_norm": out["state_norm"].detach(),
        "boundary_confidence_mean": out["boundary_confidence_mean"].detach(),
        "think_steps": torch.tensor(out["think_steps"], device=loss.device),
    }
    # decoder 去噪臂计数列 (任务书 2026-08-29 §1 修订 v2 + 冒烟条款): 扰动触发
    # 比例 (noise/m̂/clean 行占比 + 命中 s 档, grade 列 = s 值, -1 哨兵 = 未触发)
    # + 干净行 direct acc ——混合 direct_acc 在扰动臂下天然回落, 干净行读数才是
    # §2 有效性门的判读面。关态/eval = 零占位, log schema 对齐 (本文件臂列惯例)。
    denoise_metrics = {
        "denoise_noise_frac": torch.zeros((), device=device),
        "denoise_mhat_frac": torch.zeros((), device=device),
        "denoise_clean_frac": torch.zeros((), device=device),
        "denoise_grade": torch.full((), -1.0, device=device),
        "denoise_direct_clean_acc": torch.zeros((), device=device),
    }
    dn = out.get("denoise_stats")
    if dn is not None:
        denoise_metrics["denoise_noise_frac"] = torch.tensor(dn["noise_frac"], device=device)
        denoise_metrics["denoise_mhat_frac"] = torch.tensor(dn["mhat_frac"], device=device)
        denoise_metrics["denoise_clean_frac"] = torch.tensor(dn["clean_frac"], device=device)
        denoise_metrics["denoise_grade"] = torch.tensor(dn["grade"], device=device)
        clean_slot = encoded_slot_mask & dn["clean_rows"].unsqueeze(-1)
        denoise_metrics["denoise_direct_clean_acc"] = _acc_tensor(
            out["logits_direct"].argmax(dim=-1), encoded_targets, clean_slot
        )
    metrics.update(denoise_metrics)
    # Q20 多槽读出臂接通计 (E119 冒烟条款① 旋钮接通仪表): 本前向 direct 腿
    # 是否吃了多槽读出行 (train 态旗标开才 1; 关态/eval = 零占位, log schema
    # 对齐本文件臂列惯例)
    metrics["q20_engaged"] = torch.tensor(float(out.get("q20_engaged", 0.0)), device=device)
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
    # burst eval determinism: same discipline, its own stream offset.
    _BURST_GENERATOR.manual_seed(args.eval_mask_seed + _BURST_SEED_OFFSET)
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
    # --- Q18 v2 读出墙裁定臂 (B 计划 2026-08-28): A/A′ 臂移植进 s1 骨架 ---
    # 机制与动机见模块中部 Q18 节注记; 默认全关 (q18_arm="" = 零侵入,
    # canonical 路径逐比特不变)。
    parser.add_argument(
        "--q18-arm", choices=["", "A", "Aprime"], default="",
        help="Q18 臂: A=预算终审 (从零 40K); Aprime=闭式温启动双列 (20K); 空=关",
    )
    parser.add_argument(
        "--q18-warmstart", choices=["oracle", "natural"], default="oracle",
        help="A′ 列: oracle 态 (p≡1.0) / natural 态 (p≡0.0, 生产判词)",
    )
    parser.add_argument(
        "--q18-base-ckpt", default="",
        help="Q15 正臂收官 run dir (基座: resolved_config 回填 defaults + latest.pt strict 加载)",
    )
    parser.add_argument(
        "--q18-donor-ckpt", default="checkpoints/v37ks_b_sm_v371_20k_ctx4096_20260817",
        help="A′ donor 端口 (b 格 v371 冻结组件, Q19 D1 方案)",
    )
    parser.add_argument(
        "--q18-steps", type=int, default=0,
        help="0 = 臂默认 (A: 40K, A′: 20K); >0 覆写 (冒烟/奇偶校验)",
    )
    parser.add_argument("--q18-calib-windows", type=int, default=16, help="A′ 标定窗数 (16 = Q19 协议)")
    parser.add_argument("--q18-zc-windows", type=int, default=8, help="零变化律自检窗数")
    parser.add_argument(
        "--q18-zc-threshold", type=float, default=0.15,
        help="零变化律阈值 (任务书 §1 预注册 0.15; train_q18_readout_wall._Q18_ZC_THRESHOLD 同值)",
    )
    parser.add_argument(
        "--q18-no-sieve", action="store_true",
        help="关先验筛 (独立训练器楔死急诊单 B-2 移植保留; 默认开 = 参考臂同口径)",
    )
    parser.add_argument("--lam-unmix", type=float, default=1e-2, help="A′ 段1 ridge 解混 λ (Q19 同档)")
    parser.add_argument("--lam-stage2", type=float, default=1.0, help="A′ 段2/收尾 ridge λ (相对预条件后, Q19 同档)")
    # --- decoder 去噪臂 (任务书 2026-08-29 冻结 v1.1: docs/versions/v3.7/
    # FLUED_V3_7_DECODER_DENOISE_20260829_CN.md) ---
    # direct 口 (decoder_in_mem) 分布内模糊练钝, 可训练范围 = 仅 decoder。
    # 默认全关 = 旧路径逐位不变 (条件创建纪律同 decoder_in_mem 先例);
    # 噪声参数只来自前置测量 (probe_decoder_fuzz_id 落盘), 不许拍脑袋。
    parser.add_argument(
        "--decoder-denoise",
        action="store_true",
        help="decoder 去噪臂总开关 (默认关 = 旧路径逐位不变; 要求 slm + v_row_source=memory)",
    )
    parser.add_argument(
        "--decoder-denoise-fuzz-id", default="",
        help="前置测量产物目录 (probe_decoder_fuzz_id 落盘; 修订 v2 只装载 λopt=1.0 部署桥 + 残差 Cholesky + ρ)",
    )
    parser.add_argument(
        "--decoder-denoise-p-noise", type=float, default=0.5,
        help="列① 统计匹配噪声 batch 级触发概率 (任务书 §1 冻结 0.5)",
    )
    parser.add_argument(
        "--decoder-denoise-p-mhat", type=float, default=0.25,
        help="列② m̂ 整行替换 batch 级触发概率 (任务书 §1 冻结 0.25)",
    )
    parser.add_argument(
        "--decoder-denoise-row-frac", type=float, default=0.5,
        help="触发时随机选中的实 chunk 行比例 (任务书 §1 冻结 0.5)",
    )
    parser.add_argument(
        "--decoder-denoise-mhat-start", type=int, default=10000,
        help="m̂ 列激活步 (任务书 §1 冻结 10K 里程碑; 课程 5K/10K 档切换为常量)",
    )
    parser.add_argument(
        "--decoder-denoise-s-ladder", default="0.5,1.0,2.0",
        help="噪声强度档 = 部署桥 (λopt=1.0) 残差采样器的标量倍率 CSV (任务书 §1 修订 v2 "
             "冻结 0.5,1.0,2.0; 课程 0–5K 取第 1 档 / 5K–10K 前 2 档 / 10K 起全档均匀)",
    )
    # --- Q20 多槽读出臂 (multi-slot readout, E119; 任务书 2026-08-29 冻结 v1:
    # docs/versions/v3.7/FLUED_V3_7_Q20_MULTISLOT_READOUT_20260829_CN.md) ---
    # b 格 K 通道 post-state → decoder direct 口的读出端扩宽; 可训练范围 = 仅
    # 新增多槽读出件, 端口/decoder/backbone/写入侧全冻在 E118 收官态。
    # 默认全关 = 旧路径逐位不变 (--decoder-denoise-* 先例)。
    parser.add_argument(
        "--multislot-readout",
        action="store_true",
        help="Q20 多槽读出臂总开关 (默认关 = 旧路径逐位不变; 要求 slm b 格 + --init-checkpoint E118 基座)",
    )
    parser.add_argument(
        "--multislot-readout-k",
        choices=["1", "4", "8", "cg"],
        default="4",
        help="槽位扫描档 (任务书 §5.1 裁定 {1,4,8}) | cg = CG 结构内化对照臂 (T=8 步可微 CG 段1 + 可学段2 投影, 无 k 轴)",
    )
    parser.add_argument(
        "--multislot-readout-fuzz-id",
        default="outputs/decoder_denoise_fuzz_id_20260829",
        help="温启动产物目录 (ridge 段1主方向 q20_ridge_dir.npz + λopt=1.0 部署桥; 缺件响亮报错不静默降级)",
    )
    # --- E120 端到端点燃臂 (任务书 2026-09-03 冻结 v1+修订 v2) ---
    # d 格 V 通道生产读出替换: k=1 温启动读出件 (E119 定型档) 读 V 通道
    # post-state → 部署桥投影 → 生产读出行空间 d_pack (v_rows 整行换源)。
    # 默认关 = 旧路径逐位不变 (--multislot-readout-* 先例)。
    parser.add_argument(
        "--e120-readout-swap",
        action="store_true",
        help="E120 端到端点燃臂总开关 (d 格 V 通道生产读出替换; 默认关 = 旧路径逐位不变; "
             "要求 slm d 格 + config 显式 q15_circuit_rearing=false; 训练态需 --init-checkpoint 25b 基座)",
    )
    parser.add_argument(
        "--e120-fit-dir",
        default="outputs/e120_warmstart_fit_20260903",
        help="温启动产物目录 (probe_e120_warmstart_fit.py 落盘: bridge_deploy.npz + q_ridge_dir.npz; "
             "缺件/缺键/形不符响亮报错不静默降级)",
    )
    parser.add_argument(
        "--e120-random-init",
        action="store_true",
        help="E120 随机初始化对照列 (修订 v3 2026-09-04 用户裁定: 裁 3 读数 b 格 k=1 t=0 温启动 "
             "0.0598 < 随机 0.1173, E119「温启动承重」降级为待本列判决的开放假说; 显式豁免 "
             "温启动装载, 保持 trunc_normal 0.02 随机初始化; 仅乙列训练态可用, 甲列 eval-only 响亮拒绝)",
    )


def main() -> None:
    from tools.train.v3_6.train_v36 import build_parser

    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--config", default="")
    pre.add_argument("--q18-base-ckpt", default="")
    pre_args, _ = pre.parse_known_args()
    parser = build_parser()
    _add_s1_args(parser)
    if pre_args.config:
        parser.set_defaults(**json.loads(Path(pre_args.config).read_text(encoding="utf-8")))
    if pre_args.q18_base_ckpt:
        # Q18 模式 (B 计划 2026-08-28): 基座 resolved_config 回填 defaults
        # (窗规格/管束/模型形态继承基座; IO/运行时键剔除, 见 _Q18_CONFIG_EXCLUDE)
        parser.set_defaults(**_q18_base_config_defaults(pre_args.q18_base_ckpt))
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
    q18_on = _q18_enabled(args)
    if q18_on:
        # Q18 v2 读出墙裁定臂 (B 计划 2026-08-28): 旗标响亮校验 + 冻结配方
        # 覆写 (任务书 §1, 独立训练器硬编码同款: LR 1e-3 + warmup 200 +
        # cosine→0, batch=1, 预算 A 40K / A′ 20K)。课程 p 恒定 (A/oracle 列
        # ≡1.0, natural 列 ≡0.0), 训练步内在 _q18_train_step 现查。
        _q18_validate_args(args)
        args.lr = 1e-3
        args.warmup_steps = 200
        args.max_steps = int(args.q18_steps) or (40_000 if args.q18_arm == "A" else 20_000)
        if args.batch_size != 1:
            print(f"[s1][q18] batch_size 覆写 {args.batch_size} -> 1 (Q17 同款冻结)", flush=True)
            args.batch_size = 1
        tag = "q18a" if args.q18_arm == "A" else f"q18ap_{args.q18_warmstart}"
        if "--run-id" not in sys.argv:
            args.run_id = f"v37ks_d_{tag}_s{args.seed}_{args.max_steps // 1000}k_s1host_20260828"
        if "--out-dir" not in sys.argv:
            args.out_dir = f"checkpoints/{args.run_id}"
        print(
            f"[s1][q18] B 计划移植臂: arm={args.q18_arm} "
            f"{'温启动 ' + args.q18_warmstart if args.q18_arm == 'Aprime' else '从零'} "
            f"预算={args.max_steps} LR={args.lr} warmup={args.warmup_steps} "
            f"基座={args.q18_base_ckpt} out={args.out_dir}",
            flush=True,
        )
    denoise_on = _decoder_denoise_enabled(args)
    if denoise_on:
        # decoder 去噪臂 (任务书 2026-08-29 冻结 v1.1): 响亮校验——端口臂只在
        # slm b/a 格 (v_row_source=memory → decoder_in_mem 在岗) 有意义; 现役
        # canonical 是 attn 模式结构性无此端口, d 格 v=state 同理 (Q19 D1)。
        if q18_on:
            raise SystemExit(
                "--decoder-denoise 不组合 Q18 臂 (Q18 训练步整体委托独立机制, direct 腿不经 _slm_forward)"
            )
        if getattr(args, "backbone_mode", "") != "slm" or getattr(args, "v_row_source", "memory") != "memory":
            raise SystemExit(
                "--decoder-denoise requires --backbone-mode slm + v_row_source=memory "
                "(decoder_in_mem 端口臂; attn/d 格结构性无此端口)"
            )
        if not args.decoder_denoise_fuzz_id:
            raise SystemExit(
                "--decoder-denoise requires --decoder-denoise-fuzz-id <前置测量产物目录> "
                "(probe_decoder_fuzz_id 落盘; 噪声参数只来自前置测量, 不许拍脑袋)"
            )
    q20_on = _multislot_readout_enabled(args)
    if q20_on:
        # Q20 多槽读出臂 (任务书冻结 v1): 响亮校验——b 格限定 (K 通道状态机 +
        # d_mem 端口同在, 现役 canonical attn 模式结构性无此链); 微调臂需
        # E118 基座; 不与去噪臂同开 (基座已是练钝态, denoise 旗标关——任务书
        # §3.1); 不组合 Q18 (训练步整体委托独立机制, direct 腿不经
        # _slm_forward)。模型侧创建校验 (recurrence/档位) 在 build_model。
        if denoise_on:
            raise SystemExit("--multislot-readout 不与 --decoder-denoise 同开 (基座已是 E118 练钝态, 任务书 §3.1)")
        if q18_on:
            raise SystemExit(
                "--multislot-readout 不组合 Q18 臂 (Q18 训练步整体委托独立机制, direct 腿不经 _slm_forward)"
            )
        if (
            getattr(args, "backbone_mode", "") != "slm"
            or getattr(args, "k_row_source", "") != "state"
            or getattr(args, "v_row_source", "memory") != "memory"
        ):
            raise SystemExit(
                "--multislot-readout requires --backbone-mode slm + k_row_source=state + v_row_source=memory "
                "(b 格: 读出对象 = K 通道 post-state, 落口 = decoder_in_mem d_mem 端口)"
            )
        if not args.init_checkpoint:
            raise SystemExit(
                "--multislot-readout 需要 --init-checkpoint <E118 收官 latest.pt> (读出端扩宽是微调臂, 非从零)"
            )
    e120_on = _e120_enabled(args)
    if e120_on:
        # E120 端到端点燃臂 (任务书冻结 v1+修订 v2): 响亮校验——d 格限定 (K/V
        # 双状态机, 读出对象 = V 通道 post-state, 落口 = 生产读出行空间); 乙列
        # 显式关 q15_circuit_rearing (修订 v2 写死: 生产环境无过程奖励拐杖,
        # q15_lambda_* 三枚随总开关失活 keep-inert); 不与 denoise/Q18/Q20 同开
        # (Q20=b 格 K 通道 direct 口扩宽, 两臂对象互斥); 训练态 (乙列) 需
        # init-checkpoint (25b 基座, 修订 v2 钉死), eval-only 态即甲列。
        if denoise_on:
            raise SystemExit(
                "--e120-readout-swap 不与 --decoder-denoise 同开 (denoise 端口臂是 b 格 v_row_source=memory 专属)"
            )
        if q18_on:
            raise SystemExit(
                "--e120-readout-swap 不组合 Q18 臂 (训练步整体委托独立机制, direct 腿不经 _slm_forward)"
            )
        if q20_on:
            raise SystemExit(
                "--e120-readout-swap 不与 --multislot-readout 同开 (Q20=b 格 K 通道 direct 口扩宽, "
                "E120=d 格 V 通道生产读出替换, 两臂读出对象互斥)"
            )
        if (
            getattr(args, "backbone_mode", "") != "slm"
            or getattr(args, "k_row_source", "") != "state"
            or getattr(args, "v_row_source", "") != "state"
        ):
            raise SystemExit(
                "--e120-readout-swap requires --backbone-mode slm + k_row_source=state + v_row_source=state "
                "(d 格: 读出对象 = V 通道 post-state, 落口 = 生产读出行空间)"
            )
        if getattr(args, "q15_circuit_rearing", False):
            raise SystemExit(
                "--e120-readout-swap 需要显式关闭 q15_circuit_rearing (修订 v2 写死: 生产环境无过程奖励拐杖; "
                "CLI 无 false 档, 必须经 config 传 q15_circuit_rearing=false, 如 configs/v3_7_e120_d25b.json)"
            )
        if not args.eval_only and not args.init_checkpoint:
            raise SystemExit(
                "--e120-readout-swap 需要 --init-checkpoint <25b 收官 latest.pt> (乙列微调臂, 非从零) "
                "或 --eval-only <基座 latest.pt> (甲列纯插拔)"
            )
        if getattr(args, "e120_random_init", False) and args.eval_only:
            raise SystemExit(
                "--e120-random-init 仅乙列训练态可用 (甲列语义 = 温启动件纯插拔测 Δ, "
                "随机件插拔不在判读表四格内)"
            )
        # 乙列解冻语义 (任务书 §1 两臂同测: 全模型解冻, 含新件): 基座配方继承的
        # freeze_prefixes (前端冻结) 在本臂清空, resolved_config 落盘最终语义
        if getattr(args, "freeze_prefixes", ""):
            print(
                f"[s1][e120] freeze_prefixes 覆写 {args.freeze_prefixes!r} -> '' (乙列全模型解冻)",
                flush=True,
            )
            args.freeze_prefixes = ""
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
            f"weight={args.retrieval_weight} block_prob(r)={args.retrieval_block_prob}"
            + (
                f" examples={int(args.retrieval_examples)} (Q12 示例密集形态, 修订案 v3)"
                if int(getattr(args, "retrieval_examples", 0)) > 0
                else ""
            ),
            flush=True,
        )
    if getattr(args, "retrieval_block_ramp", ""):
        global _RETRIEVAL_RAMP
        _RETRIEVAL_RAMP = _parse_block_ramp(args.retrieval_block_ramp)
        print(f"[s1] retrieval r 爬坡 (prereg §4): {_RETRIEVAL_RAMP}", flush=True)
    _check_burst_args(args)
    _check_q15_args(args)
    if _q15_enabled(args):
        # Q15 回路养成臂 (任务书 2026-08-25 冻结): λ 初值 (§3.4) 落 args
        # 属性, step_model 每步读, 回调线 (§5) 原地降权. λ_out 继承
        # task2_loss_weight (不作新自由度).
        args.q15_lambda_att = _Q15_LAMBDA_ATT
        args.q15_lambda_out = float(args.task2_loss_weight)
        args.q15_lambda_couple = _Q15_LAMBDA_COUPLE
        print(
            f"[s1] Q15 回路养成臂 (d 格): λ_att={args.q15_lambda_att} "
            f"λ_out={args.q15_lambda_out}(继承 task2) λ_couple={args.q15_lambda_couple} "
            f"p_twin={_Q15_TWIN_P} δ/s={_Q15_GATE_DELTA}/{_Q15_GATE_S} m={_Q15_TWIN_M}",
            flush=True,
        )
    if _burst_enabled(args):
        # Q13 突发性注入臂 (prereg 2026-08-22): the corpus sampler opens
        # --data-path for random-offset fresh segment draws (防背护栏: 严禁
        # 固定段库; (偏移, 长度) 进程级登记, 同 epoch 重复采中重抽 N=8 后响亮报错).
        global _BURST_SAMPLER
        _BURST_SAMPLER = CorpusSampler(args.data_path)
        print(
            f"[s1] Q13 突发性注入臂: prob={args.burst_prob} R={int(args.burst_repeat)} "
            f"tail=2-{int(args.burst_tail_max_chars)}字 sampler={args.data_path} "
            f"({_BURST_SAMPLER._size}B)",
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
    _BURST_GENERATOR.manual_seed(args.seed + _BURST_SEED_OFFSET)
    _DENOISE_GENERATOR.manual_seed(args.seed + _DENOISE_SEED_OFFSET)  # 无条件播种; 关态零抽取零影响
    if q18_on:
        # Q18 抽签流 (退火抽签 Q18 独立偏移 101_077, 与 Q17 的 101_033 不混)
        # + mask/burst 重断言——独立训练器 _seed_streams 同 discipline
        _q18_seed_streams(args)

    device = torch.device(args.device if args.device == "cpu" or torch.cuda.is_available() else "cpu")
    if q18_on and device.type != "cuda" and getattr(args, "kda_impl", "") != "torch":
        # 独立训练器 _q17_load_models 同款: fla kernels GPU-only
        print(f"[s1][q18] kda_impl 覆写 {args.kda_impl} -> torch (非 CUDA 设备)", flush=True)
        args.kda_impl = "torch"
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
        if e120_on:
            # E120 甲列 (纯插拔, eval-only): 基座全键全形校验豁免 e120_readout.*
            # 新件键 → 温启动 (t=0 即最终态) → 全模型冻结含新件 → 标准 eval。
            # 路由消融/Δ 仪器在探针侧 (probe_burst_route_q15 同族), 本处只保证
            # 冻结语义与温启动装载响亮。
            _cur = model.state_dict()
            _bad = [
                k
                for k in _cur
                if not k.startswith("e120_readout.")
                and (k not in payload["model"] or payload["model"][k].shape != _cur[k].shape)
            ]
            _extra = [k for k in payload["model"] if k not in _cur]
            if _bad or _extra:
                raise SystemExit(
                    f"[s1][e120] 甲列基座全键全形校验失败: {len(_bad)} 键缺失/形不符 + {len(_extra)} 冗键 "
                    f"(如 {(_bad + _extra)[:5]}) —— --eval-only 的 ckpt 与现行 config 架构漂移"
                )
            model.load_state_dict(payload["model"], strict=False)
            _warm = _e120_warm_start(model, args.e120_fit_dir)
            n_train, n_frozen = _e120_freeze_all(model)
            print(
                f"[s1][e120] 甲列纯插拔 (eval-only): fit_dir={args.e120_fit_dir} 温启动[{_warm}] | "
                f"全模型冻结: trainable={n_train} frozen={n_frozen}",
                flush=True,
            )
        else:
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
    q18_warm_report = None
    q18_base_step = 0
    q18_base_payload = None
    if q18_on:
        # Q18 基座 strict 加载 (独立训练器 _q17_load_models 同款) + 链初始化
        # (A 从零 / A′ 温启动+零变化律自检, 机制零复制); init_checkpoint 已
        # 经 _Q18_CONFIG_EXCLUDE 剔除——Q18 的初始化面 = 基座 + 链, 不回链 S0。
        q18_base_payload = torch.load(
            Path(args.q18_base_ckpt) / "latest.pt", map_location=device, weights_only=False
        )
        model.load_state_dict(q18_base_payload["model"], strict=True)
        q18_base_step = int(q18_base_payload.get("step", 0))
        print(f"[s1][q18] 基座 strict 加载: {args.q18_base_ckpt} step={q18_base_step}", flush=True)
        q18_warm_report = _q18_setup_chain(
            model, args, device, out_dir,
            resuming=bool(args.resume and (out_dir / "latest.pt").exists()),
        )
    frozen = [p.strip() for p in args.freeze_prefixes.split(",") if p.strip()]
    if frozen and not q18_on:
        # Q18 模式跳过本块: 冻结面由 _q18_setup_chain 全权定义 (独立训练器
        # 没有 freeze_prefixes 概念)。基座 Q15 配方的 byte_lookup 前缀会把
        # tied 嵌入 (decoder.byte_lookup 与模型级 byte_lookup 同一参数) 重
        # 新冻结——而独立训练器里它经 decoder 在链上参训; 奇偶校验实测该差
        # 异造成 +0.2 系统性 loss 偏移 (2026-08-28), 故必须跳过。
        n = 0
        for name, param in model.named_parameters():
            if any(name.startswith(p) for p in frozen):
                param.requires_grad_(False)
                n += 1
        print(f"[s1] frozen params={n} prefixes={frozen}", flush=True)
    if denoise_on:
        # decoder 去噪臂 (任务书终审钉死): 装载前置测量产物 + 可训练范围 =
        # 仅 decoder (_decoder_denoise_freeze 是显式白名单, 终态不受
        # freeze_prefixes 内容影响——它先跑, 这里是确定性覆写)。
        # 基座全键校验 (2026-08-29 冒烟事故入例): init_checkpoint 的通用加载
        # 是静默形状过滤 (compatible dict), 而 parser 现行默认可能与老基座
        # 架构漂移 (v37.1 基座无 summarizer_pool 键 → 现行默认 qpool 会静默
        # 改 summarizer 架构, 段 3 端口直连报废) —— 本臂是端口微调臂, 基座
        # 必须全键全形加载, 不齐响亮退出, 不许静默训一个残缺基座。
        if not args.init_checkpoint:
            raise SystemExit("--decoder-denoise 需要 --init-checkpoint <基座 latest.pt> (端口练钝是微调臂, 非从零)")
        _dn_payload = torch.load(args.init_checkpoint, map_location="cpu", weights_only=False)["model"]
        _dn_cur = model.state_dict()
        _dn_bad = [k for k in _dn_cur if k not in _dn_payload or _dn_payload[k].shape != _dn_cur[k].shape]
        if _dn_bad:
            raise SystemExit(
                f"[s1][denoise] 基座全键校验失败: {len(_dn_bad)} 键缺失/形不符 (如 {_dn_bad[:5]}) —— "
                "检查 --config 来源与基座的架构漂移 (典型: summarizer_pool 现行默认 qpool vs v37.1 基座 mean, "
                "需显式 --summarizer-pool mean)"
            )
        del _dn_payload, _dn_cur
        global _DENOISE_FUZZ
        _DENOISE_FUZZ = _load_decoder_denoise_fuzz(args.decoder_denoise_fuzz_id)
        n_train, n_frozen = _decoder_denoise_freeze(model)
        print(
            f"[s1][denoise] decoder 去噪臂: fuzz_id={args.decoder_denoise_fuzz_id} "
            f"p_noise={args.decoder_denoise_p_noise} p_mhat={args.decoder_denoise_p_mhat} "
            f"row_frac={args.decoder_denoise_row_frac} mhat_start={args.decoder_denoise_mhat_start} "
            f"s_ladder={_denoise_s_ladder(args)} | "
            f"仅 decoder 可训: trainable={n_train} frozen={n_frozen} "
            f"(decoder_in_mem/chunk_pos/backbone/写入侧/tied byte_lookup 全冻)",
            flush=True,
        )
    if q20_on:
        # Q20 多槽读出臂 (任务书冻结 v1 §3.1/§3.3): 基座 = E118 收官 (端口练
        # 钝态)。基座全键全形校验 (去噪臂冒烟事故入例的 loud-fail 同款, 豁免
        # multislot_readout.* 新件键——它们由温启动装载, 双向核对) → 温启动
        # (缺件响亮报错) → 冻结白名单 = 仅多槽读出件 (终态不受
        # freeze_prefixes 内容影响——它先跑, 这里是确定性覆写)。
        _q20_payload = torch.load(args.init_checkpoint, map_location="cpu", weights_only=False)["model"]
        _q20_cur = model.state_dict()
        _q20_bad = [
            k
            for k in _q20_cur
            if not k.startswith("multislot_readout.")
            and (k not in _q20_payload or _q20_payload[k].shape != _q20_cur[k].shape)
        ]
        _q20_extra = [k for k in _q20_payload if k not in _q20_cur]
        if _q20_bad or _q20_extra:
            raise SystemExit(
                f"[s1][q20] 基座全键全形校验失败: {len(_q20_bad)} 键缺失/形不符 + {len(_q20_extra)} 冗键 "
                f"(如 {(_q20_bad + _q20_extra)[:5]}) —— 检查 --config 来源与基座的架构漂移 "
                "(典型: summarizer_pool 现行默认 qpool vs v37.1 基座 mean, 需显式 --summarizer-pool mean)"
            )
        del _q20_payload, _q20_cur
        warm_note = _multislot_readout_warm_start(model, args.multislot_readout_fuzz_id)
        n_train, n_frozen = _multislot_readout_freeze(model)
        print(
            f"[s1][q20] 多槽读出臂 (E119): k={args.multislot_readout_k} fuzz_id={args.multislot_readout_fuzz_id} "
            f"温启动[{warm_note}] | 仅多槽读出件可训: trainable={n_train} frozen={n_frozen} "
            f"(decoder/decoder_in_mem/backbone/写入侧/tied byte_lookup 全冻在 E118 收官态)",
            flush=True,
        )
    if e120_on:
        # E120 端到端点燃臂乙列 (任务书 §1 两臂同测): 基座 = 25b 收官 (修订 v2
        # 钉死, 无 b 后缀的 512B off-spec pilot 禁混排)。基座全键全形校验 (去噪
        # 臂冒烟事故入例的 loud-fail 同款, 豁免 e120_readout.* 新件键——它们由
        # 温启动装载, 双向核对) → 温启动 (缺件/缺键/形不符响亮报错) → 乙列全
        # 模型解冻 (freeze_prefixes 已在旗标校验段清空, 这里确定性兜底)。
        _e120_payload = torch.load(args.init_checkpoint, map_location="cpu", weights_only=False)["model"]
        _e120_cur = model.state_dict()
        _e120_bad = [
            k
            for k in _e120_cur
            if not k.startswith("e120_readout.")
            and (k not in _e120_payload or _e120_payload[k].shape != _e120_cur[k].shape)
        ]
        _e120_extra = [k for k in _e120_payload if k not in _e120_cur]
        if _e120_bad or _e120_extra:
            raise SystemExit(
                f"[s1][e120] 基座全键全形校验失败: {len(_e120_bad)} 键缺失/形不符 + {len(_e120_extra)} 冗键 "
                f"(如 {(_e120_bad + _e120_extra)[:5]}) —— 检查 --config 来源与基座的架构漂移 "
                "(典型: summarizer_pool 现行默认 qpool vs v37.1 基座 mean, 需显式 --summarizer-pool mean)"
            )
        del _e120_payload, _e120_cur
        if getattr(args, "e120_random_init", False):
            # 随机对照列 (修订 v3 2026-09-04, 修订 v2 ④ 提前并入主批): 显式豁免温
            # 启动装载——读出件保持 __init__ 的 trunc_normal(0.02) 随机初始化,
            # 单变量 = 初始化 (其余配置逐键同乙列)。裁 3 已证 b 格 t=0 温启动
            # 0.0598 < 随机 0.1173, E119「温启动承重」开放假说由本列判决。
            warm_note = "随机初始化对照 (显式豁免温启动装载, 修订 v3)"
        else:
            warm_note = _e120_warm_start(model, args.e120_fit_dir)
        n_train, n_frozen = _e120_unfreeze_all(model)
        print(
            f"[s1][e120] 端到端点燃臂乙列: fit_dir={args.e120_fit_dir} 初始化[{warm_note}] | "
            f"全模型解冻: trainable={n_train} frozen={n_frozen} "
            f"(q15_circuit_rearing=off 修订 v2, 被替换的生产读出链外无梯度通路)",
            flush=True,
        )
    if q18_on:
        # Q18 先验筛参考模型 = 基座第二次独立加载 (E101 教训, 独立训练器同
        # 款: 固定, 设备驻留, 全程只读); --q18-no-sieve 时卸载 (楔死急诊单
        # B-2 移植保留)。注意: 本块必须覆盖/取代下方 Q14 标准筛块 (标准块在
        # q18 模式跳过——它没有基座 ckpt 可载, 只会造随机初始化筛子)。
        global _BURST_SIEVE_MODEL
        _BURST_SIEVE_MODEL = None
        if not args.q18_no_sieve:
            _BURST_SIEVE_MODEL = build_model(args).to(device)
            _BURST_SIEVE_MODEL.load_state_dict(q18_base_payload["model"], strict=True)
            for p_ in _BURST_SIEVE_MODEL.parameters():
                p_.requires_grad_(False)
            _BURST_SIEVE_MODEL.eval()
            print("[s1][q18] 先验筛参考模型: 基座第二次独立加载, 固定驻留", flush=True)
    if bool(getattr(args, "burst_prior_sieve", False)) and not q18_on:
        # Q14 先验筛基准 (修订案 2026-08-23 §2.1): 参考模型 = 与开工 checkpoint
        # 同一份 -- canonical 配置随机初始化 (同种子复演 step-0 初始化抽签, 全局
        # RNG 状态先存后还) 叠加 init_checkpoint 的同口径部分加载; requires_grad
        # False + eval + 驻训练设备 (GPU——驻 CPU 的 fla kernel 崩、torch 递推
        # CPU 前向 ~10× 减速, 两次教训 2026-08-23), 全程只读, 训练中不重筛.
        # (global 声明已随 Q18 块上移至本函数首个使用点——同一函数内重复
        # 声明在使用点之后是 SyntaxError)
        rng_state = torch.get_rng_state()
        torch.manual_seed(args.seed)
        _BURST_SIEVE_MODEL = build_model(args).to(device)
        torch.set_rng_state(rng_state)
        if args.init_checkpoint:
            payload = torch.load(args.init_checkpoint, map_location="cpu", weights_only=False)
            current = _BURST_SIEVE_MODEL.state_dict()
            compatible = {
                k: v for k, v in payload["model"].items() if k in current and current[k].shape == v.shape
            }
            init_prefixes = [p.strip() for p in args.init_prefixes.split(",") if p.strip()]
            if init_prefixes:
                compatible = {k: v for k, v in compatible.items() if any(k.startswith(p) for p in init_prefixes)}
            _BURST_SIEVE_MODEL.load_state_dict(compatible, strict=False)
        for p_ in _BURST_SIEVE_MODEL.parameters():
            p_.requires_grad_(False)
        _BURST_SIEVE_MODEL.eval()
        print(
            f"[s1] Q14 先验筛: 参考模型固定于开工 checkpoint "
            f"(init={args.init_checkpoint or '无(纯随机初始化)'}, 阈值 {_BURST_SIEVE_THRESHOLD}, 全程不重筛)",
            flush=True,
        )
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
    if float(getattr(args, "lr_const_after_resume", 0.0)) > 0 and start_step > 0:
        # Q12 40K 延长臂（用户冻结 2026-08-22）：不复用旧 cosine 尾段——
        # 重置 base lr 后 re-warmup lr_rewarmup 步、随后恒定 lr_const_after_resume
        for g in opt.param_groups:
            g["lr"] = args.lr
        _target = float(args.lr_const_after_resume) / args.lr
        _rew = int(getattr(args, "lr_rewarmup", 200))

        def _const_lambda(s, _t=_target, _r=_rew, _s0=start_step):
            rel = s - _s0
            if rel < _r:
                return _t * (rel + 1) / _r
            return _t

        sched = torch.optim.lr_scheduler.LambdaLR(opt, _const_lambda)
        sched.step(start_step)
        print(
            f"[s1] LR 覆写（用户冻结 40K 延长）：re-warmup {_rew} 步 → 恒定 {args.lr_const_after_resume}（不复用 cosine 尾段）",
            flush=True,
        )
        print(f"[s1] resumed from step {start_step}", flush=True)

    log_path = out_dir / "train_log.jsonl"
    model.train()
    t0 = time.time()
    nan_skips = 0
    step = start_step
    pending: dict[str, torch.Tensor] = {}
    pending_n = 0
    # Q14 臂中点复测钩 (修订案 §2.1): 只在先验筛开时武装
    midpoint_done = False
    midpoint_armed = bool(getattr(args, "burst_prior_sieve", False)) and _burst_enabled(args) and not q18_on
    # Q15 codec 回调线 (任务书 §5, 臂内自锚): 锚 = steps 800-1000 训练批
    # direct_acc/backbone_acc 均值 (post-warmup 自锚; 训练中无周期 eval,
    # 只能用训练批读数); resume 越过锚窗时锚缺席, 监控自动解除 (不静默伪造锚)
    q15_anchor_sum = {"direct_acc": 0.0, "backbone_acc": 0.0}
    q15_anchor_n = 0
    q15_anchor = None
    q15_lambdas = q15_floors = None
    if _q15_enabled(args) and not q18_on:
        q15_lambdas = {
            "att": args.q15_lambda_att, "out": args.q15_lambda_out, "couple": args.q15_lambda_couple
        }
        q15_floors = {k: v * _Q15_CALLBACK_FLOOR for k, v in q15_lambdas.items()}
    # decoder 去噪臂 codec 护栏 (任务书 §2 有效性门: 干净行水位回落 >2pp 触发,
    # 沿用 Q15 §5 自锚回调设施): 锚 = steps 800-1000 训练批「干净行 direct acc +
    # backbone acc」均值 (backbone 腿永不被扰动; direct 侧读干净行仪表——混合
    # direct_acc 在扰动臂下随课程天然回落, 不是水位判读面); step>1000 后每个
    # log 事件查窗均值, 任一退步 >0.02 → p_noise/p_mhat 各 x0.5 (下限初值
    # x0.25), 事件落 denoise_callback_events.jsonl。锚窗缺席 (resume 越过/
    # 冒烟 <800 步) 时监控自动解除, 不静默伪造锚。anchor 字典键仍名
    # "direct_acc" (_q15_callback_check 的固定键名, 值是干净行口径)。
    denoise_anchor_sum = {"direct_acc": 0.0, "backbone_acc": 0.0}
    denoise_anchor_n = 0
    denoise_anchor = None
    denoise_ps = denoise_floors = None
    if denoise_on:
        denoise_ps = {
            "p_noise": float(args.decoder_denoise_p_noise),
            "p_mhat": float(args.decoder_denoise_p_mhat),
        }
        denoise_floors = {k: v * _Q15_CALLBACK_FLOOR for k, v in denoise_ps.items()}
    while step < args.max_steps:
        for batch in train_loader:
            if step >= args.max_steps:
                break
            if _RETRIEVAL_RAMP is not None:
                args.retrieval_block_prob = _ramp_lookup(_RETRIEVAL_RAMP, step)
            if denoise_on:
                args.decoder_denoise_step = step  # 去噪课程查表步 (本 run 内 0 基; eval 路径不消费)
            loss, metrics = step_model(model, batch, args, device, train=True)
            if loss is None:
                # Q18 echo 离网 (burst 未激活窗): 步进照走不参训 (独立训练器
                # 同款; legacy 路径永不返回 None —— 零行为变化)
                step += 1
                sched.step()
                continue
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
            if _q15_enabled(args) and not q18_on and _Q15_ANCHOR_RANGE[0] <= step <= _Q15_ANCHOR_RANGE[1]:
                # Q15 回调线锚窗 (§5): steps 800-1000 累计训练批读数
                q15_anchor_sum["direct_acc"] += float(metrics["direct_acc"])
                q15_anchor_sum["backbone_acc"] += float(metrics["backbone_acc"])
                q15_anchor_n += 1
                if step == _Q15_ANCHOR_RANGE[1]:
                    q15_anchor = {k: v / q15_anchor_n for k, v in q15_anchor_sum.items()}
                    print(f"[s1] Q15 回调线锚 (steps 800-1000 均值): {q15_anchor}", flush=True)
            if denoise_on and _Q15_ANCHOR_RANGE[0] <= step <= _Q15_ANCHOR_RANGE[1]:
                # decoder 去噪臂回调线锚窗 (任务书 §2, Q15 §5 同设施): steps
                # 800-1000 累计「干净行 direct acc + backbone acc」
                denoise_anchor_sum["direct_acc"] += float(metrics["denoise_direct_clean_acc"])
                denoise_anchor_sum["backbone_acc"] += float(metrics["backbone_acc"])
                denoise_anchor_n += 1
                if step == _Q15_ANCHOR_RANGE[1]:
                    denoise_anchor = {k: v / denoise_anchor_n for k, v in denoise_anchor_sum.items()}
                    print(f"[s1][denoise] 回调线锚 (steps 800-1000 均值): {denoise_anchor}", flush=True)
            if step % args.log_every == 0 or step == 1:
                # 数据运气仪表 (任务书 FLUED_V3_7_LR_SCALE_2X2_20260826_CN §1,
                # 无条件常开): 当前批原始流窗的窗内突发性密度 (重复 >=12B
                # 子串字节覆盖率), 逐 log 事件在册 —— 只在 log 步计算,
                # 成本≈零. 测的是 step_model 注入任务之前的原始语料窗
                # (canonical 2x2 臂 cloze/retrieval/burst 全关).
                row = {
                    "step": step,
                    "lr": float(opt.param_groups[0]["lr"]),
                    "grad": float(grad.item()),
                    "steps_per_sec": step / max(time.time() - t0, 1e-9),
                    "nan_skips": nan_skips,
                    "data_burstiness": _batch_data_burstiness(batch[0]),
                    **{k: float((v / pending_n).item()) for k, v in pending.items()},
                }
                if q18_on:
                    # Q18 log schema (B 计划): 臂/种子入每行 (独立训练器同款)
                    row["q18_arm"] = args.q18_arm
                    row["q18_seed"] = int(args.seed)
                    if args.q18_arm == "Aprime":
                        row["q18_warmstart"] = args.q18_warmstart
                _append_jsonl(log_path, row)
                pending = {}
                pending_n = 0
                # Q14 产出率报警 (修订案 §2.2): <70% 打警告行, 不静默放宽阈值
                if _burst_enabled(args):
                    _burst_yield_alarm(step, row.get("burst_yield", 1.0))
                # Q15 回调线监控 (§5): step>1000 后每个 log 事件查窗均值
                if q15_anchor is not None and step > _Q15_ANCHOR_RANGE[1]:
                    events, q15_lambdas = _q15_callback_check(
                        q15_anchor,
                        {"direct_acc": row["direct_acc"], "backbone_acc": row["backbone_acc"]},
                        q15_lambdas, q15_floors, step,
                    )
                    for ev in events:
                        args.q15_lambda_att = q15_lambdas["att"]
                        args.q15_lambda_out = q15_lambdas["out"]
                        args.q15_lambda_couple = q15_lambdas["couple"]
                        _append_jsonl(out_dir / "q15_callback_events.jsonl", ev)
                        print(
                            f"[s1][Q15] 回调线降权 step={step} 触发项={ev['triggered']} "
                            f"λ: {ev['old']} -> {ev['new']}",
                            flush=True,
                        )
                # decoder 去噪臂回调线监控 (任务书 §2 有效性门, Q15 §5 同设施):
                # 退步 >0.02 → p_noise/p_mhat 各 x0.5 (扰动强度刹车, 非课程降档)
                if denoise_anchor is not None and step > _Q15_ANCHOR_RANGE[1]:
                    events, denoise_ps = _q15_callback_check(
                        denoise_anchor,
                        {"direct_acc": row["denoise_direct_clean_acc"], "backbone_acc": row["backbone_acc"]},
                        denoise_ps, denoise_floors, step,
                    )
                    for ev in events:
                        args.decoder_denoise_p_noise = denoise_ps["p_noise"]
                        args.decoder_denoise_p_mhat = denoise_ps["p_mhat"]
                        _append_jsonl(out_dir / "denoise_callback_events.jsonl", ev)
                        print(
                            f"[s1][denoise] 回调线降权 step={step} 触发项={ev['triggered']} "
                            f"p: {ev['old']} -> {ev['new']}",
                            flush=True,
                        )
            if midpoint_armed and not midpoint_done and step >= args.max_steps // 2:
                # Q14 臂中点复测钩: 当前模型 x 同一批在训片段 (滚动 ledger);
                # >= 判定: 中点步恰好 NaN-skip 时顺延一步, 不静默丢钩
                midpoint_done = True
                _burst_prior_midpoint_check(model, args, device, out_dir)
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
    if q18_on:
        # Q18 收官 schema (B 计划): 臂/种子/基座入册; A′ 附温启动报告
        summary["q18_arm"] = args.q18_arm
        summary["q18_seed"] = int(args.seed)
        summary["q18_base_ckpt"] = str(args.q18_base_ckpt)
        summary["q18_base_step"] = q18_base_step
        if args.q18_arm == "Aprime":
            summary["q18_warmstart"] = args.q18_warmstart
            summary["warmstart_report"] = q18_warm_report
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
