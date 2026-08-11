"""S39 step-0 probe (spec §26, pre-registered 2026-08-10): archive addressing
(K side) x needle-position fidelity (V side) on FROZEN checkpoints, before any
S39 training arm is launched.

Design (fixed by the pre-registration; do not tweak here):

- K side (addressability): a light retriever — ONLY a query projection W_q
  (plus a key projection W_k in the low-rank key arm) is trained; the whole
  FLUED pipeline stays frozen. Keys are readout rows of the carried KDA state
  from the harness phase-1 stream: per-chunk (granularity 1) or one
  block-boundary readout per 4 chunks (granularity 4 — the "cross-chunk
  readout" key of form 1 / the coarse V object of form 2). The query is the
  entry-ID question encoded by the frozen pipeline (final state readout).
  Training = cross-entropy over the archive keys, positives = the key rows
  covering the needle CODE digits (strict needle-position form); hard
  negatives = same-template distractor entries ({4,16,64}) with different
  IDs/codes. Report top-1/3/5 hit (+ an entry-level diagnostic hit).
- V side (needle-position fidelity): zero training. Coarse arm = s22's /4
  paged readout (backbone_readout="paged", paged_reads=4 on 512B pages)
  decoding the needle code span through its own decoder; fine anchor =
  s36g2's per-chunk direct readout decode (upper bound); s22's own per-chunk
  direct decode is also reported (its 0.778-class anchor replicated on the
  needle span). Metrics: whole-span exact match + per-byte accuracy. The V
  side encodes each page with a FRESH KDA state (carry_state=False): both
  checkpoints were trained on single windows, so the fresh-state page is the
  in-distribution measurement of the readout FORM's needle-dilution ceiling
  ("上限提前判"); the carried-state/aging reading is the harness's 0.04
  finding and is not what this probe re-measures. The K side keeps the
  carried state (the archive IS the multi-page carried-state stream).

Harness reuse (tools/eval/paging_harness.py): _encode_window / _stream_window /
_snap_utf8 — the streaming page encode with carried KDA state and the P0 mixed
mask protocol are byte-identical to the harness. Minimal adaptations:
- Model loading is re-implemented (not ph._load_model) for two reasons: the
  harness restricts itself to xattn checkpoints while the V side needs the
  s22 mlp/paged checkpoint, and this probe HARD-freezes all parameters
  (requires_grad_(False)) so the front-end autograd graph can never be built
  (the harness relies on no_grad alone; hard-freeze is strictly safer over
  the long multi-doc encode).
- Needle format: the harness splices ONE English RULER needle into a fixed
  page; this probe splices 1 needle + D same-template distractors (Chinese
  archive template per the S39 pre-registration) at uniform random byte
  positions. Entries — needle AND distractors — are force-unmasked (the E23
  protocol extended to hard negatives, so distractors compete at full
  strength). Needle code span = the 6 ASCII digits (针位 span per spec).

Honesty notes: fp32, no autocast; batch-1 streaming encode; checkpoints
read-only; CE/softmax/normalize always computed after .float() (the fp16
entropy/log pitfall); chunk position embeddings stay page-local (harness
convention); queries are encoded UNMASKED (deployed queries are clean input —
documented approximation); a doc is skipped (resampled) if any page truncates
chunks or a needle digit lacks a valid (chunk, slot).

Usage:
  smoke: python tools/analysis/v3_6/probe_archive_addressing.py --smoke
  full:  python tools/analysis/v3_6/probe_archive_addressing.py
  v2 (K-side key-source variants, 2026-08-11 user-ruled follow-up):
         python tools/analysis/v3_6/probe_archive_addressing.py --side k --preset v2 \
             --report-name report_v2.json
         Three configs share one doc pool and ONE training seed (paired): full/g1
         boundary readout (control rerun), pooled/g4 (mean-pooled block readouts —
         does pooling rescue coarse keys from last-chunk dominance?), memrow/g1
         (pre-state summarizer rows — the form-3 "summarizer-direct K" question).
         Memory rows come straight from the harness encode path (_encode_window
         returns them); no model-code change was needed.
  v3 (coarse-key ceiling, 2026-08-11 user-ruled follow-up, K side only):
         python tools/analysis/v3_6/probe_archive_addressing.py --side k --preset v3 \
             --report-name report_v3.json
         Axis 1: pooled/g4 + learnable W_k, rank {32,64,128,256,512} (+ boundary
         full/g1 and pooled full/g4 anchors rerun same-batch). Axis 2: best rank
         at 4x budget with 4K/8K/12K/16K eval snapshots (saturation slope). Axis 3:
         semi-thawed key producer — a trainable COPY of state_machine.realign (the
         readout projection) + W_q, keys recomputed from the stored pre-realign
         reads every step; the checkpoint itself is never thawed. All configs share
         the v1/v2 doc pool and seed (1042).
"""

from __future__ import annotations

import argparse
import copy
import json
import random
import sys
import time
from argparse import Namespace
from pathlib import Path

import torch
import torch.nn.functional as F
from torch import nn

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
from flued.v36.model import paged_boundaries  # noqa: E402
from tools.train.v3_6.train_v36 import build_model  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
import tools.eval.paging_harness as ph  # noqa: E402

BYTE_OFFSET = 1  # data.py PAD-offset convention: byte b -> id b+1, PAD=0
CODE_DIGITS = 6


def _entry_bytes(eid: str, code: str) -> tuple[bytes, bytes, bytes]:
    """(prefix, code, suffix): code byte span = prefix..prefix+len(code)."""
    return (
        f"档案条目 {eid} 的校验码为 ".encode("utf-8"),
        code.encode("ascii"),
        "。".encode("utf-8"),
    )


def _query_bytes(eid: str) -> bytes:
    return f"条目 {eid} 的校验码是什么？".encode("utf-8")


# ---------------------------------------------------------------------------
# model loading (adapted from paging_harness._load_model; see docstring)
# ---------------------------------------------------------------------------


def load_model(run_dir: Path, device: torch.device, allow_modes: tuple[str, ...]):
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_path"] = "unused"  # no dataloaders; pages come from built docs
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"  # fla kernels are GPU-only
    ns = Namespace(**cfg)
    if getattr(ns, "backbone_mode", "") not in allow_modes:
        raise ValueError(f"{run_dir.name}: backbone_mode={ns.backbone_mode!r} not in {allow_modes}")
    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed" and ns.mask_prob > 0:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    model = build_model(ns).to(device)
    payload = torch.load(run_dir / "latest.pt", map_location=device, weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    for p in model.parameters():  # hard-freeze: no autograd graph anywhere in the pipeline
        p.requires_grad_(False)
    model.eval()
    return model, ns, int(payload.get("step", 0))


def load_k_model(primary: Path, fallback: Path, device: torch.device):
    try:
        model, ns, step = load_model(primary, device, ("xattn",))
        return model, ns, step, primary.name
    except Exception as exc:  # checkpoint/config mismatch -> documented fallback
        print(f"[probe] K primary {primary.name} failed: {exc}; falling back to {fallback.name}", file=sys.stderr, flush=True)
        model, ns, step = load_model(fallback, device, ("xattn",))
        return model, ns, step, fallback.name


# ---------------------------------------------------------------------------
# haystack source: v4 long-doc shards (P:), RULER jsonl fallback
# ---------------------------------------------------------------------------


def make_haystack_fn(args):
    root = Path(args.data_root)
    shards = sorted(root.glob("corpus_v4_*.txt")) if root.is_dir() else []
    if shards:
        sizes = [p.stat().st_size for p in shards]

        def read_shard(nbytes: int, rng: random.Random) -> bytes:
            raw = b""
            for _ in range(8):
                i = rng.randrange(len(shards))
                off = rng.randrange(0, max(1, sizes[i] - nbytes - 1))
                with shards[i].open("rb") as fh:
                    fh.seek(off)
                    raw = fh.read(nbytes)
                raw = raw[ph._snap_utf8(raw, 0) :]
                if len(raw) >= nbytes // 2:
                    break
            return raw

        return "v4_shards", read_shard

    path = Path(args.eval_data_root) / args.suite
    with path.open(encoding="utf-8") as fh:
        blob = "\n\n".join(json.loads(line)["context"] for line in fh).encode("utf-8")

    def read_blob(nbytes: int, rng: random.Random) -> bytes:
        off = rng.randrange(0, max(1, len(blob) - nbytes - 1))
        return blob[off : off + nbytes]

    return f"ruler_fallback:{args.suite}", read_blob


# ---------------------------------------------------------------------------
# document construction: 1 needle + n_distr same-template entries spliced at
# uniform random positions (UTF-8 snapped, non-overlapping)
# ---------------------------------------------------------------------------


def build_document(base: bytes, n_distr: int, rng: random.Random):
    specs = [True] + [False] * n_distr  # first entry is the needle
    used_ids, used_codes, entries = set(), set(), []
    for is_needle in specs:
        while True:
            eid = f"QX-{rng.randrange(10000):04d}"
            code = f"{rng.randrange(10**CODE_DIGITS):0{CODE_DIGITS}d}"
            if eid not in used_ids and code not in used_codes:
                used_ids.add(eid)
                used_codes.add(code)
                break
        pre, code_b, suf = _entry_bytes(eid, code)
        entries.append({"eid": eid, "code": code, "needle": is_needle, "parts": (pre, code_b, suf)})
    total = sum(len(pre) + len(code_b) + len(suf) for pre, code_b, suf in (e["parts"] for e in entries))
    base = base[: max(0, len(base) - total)]
    while base and (base[-1] & 0xC0) == 0x80:  # snap the tail to a char boundary
        base = base[:-1]
    margin = max(len(pre) + len(code_b) + len(suf) for pre, code_b, suf in (e["parts"] for e in entries)) + 8
    if len(base) <= margin * (len(entries) + 1):
        return None
    # insertion points with min separation `margin` so entries never share a chunk
    points = []
    for _ in range(len(entries)):
        for _try in range(64):
            cand = rng.randrange(0, len(base) - margin)
            if all(abs(cand - q) >= margin for q in points):
                points.append(cand)
                break
        else:
            return None
    points.sort()
    doc = b""
    prev = 0
    for e, p in zip(entries, points):
        p = max(ph._snap_utf8(base, p), prev)
        pre, code_b, suf = e["parts"]
        doc += base[prev:p] + pre
        e["code_lo"] = len(doc)
        doc += code_b + suf
        e["code_hi"] = e["code_lo"] + len(code_b)
        e["lo"] = e["code_lo"] - len(pre)
        e["hi"] = len(doc)
        prev = p
        del e["parts"]
    doc += base[prev:]
    return doc, entries


# ---------------------------------------------------------------------------
# frozen streaming encode (harness phase 1 verbatim) + entry/chunk mapping
# ---------------------------------------------------------------------------


def _raw_hook(sink: list):
    """Capture the pre-realign KDA read row (kda_heads*kda_head_v) per stream_step."""

    def hook(module, inputs):
        sink.append(inputs[0].detach().reshape(-1, inputs[0].size(-1))[0].to(torch.bfloat16))

    return hook


@torch.no_grad()
def encode_query(model, query: bytes, device: torch.device, capture_raw: list | None = None) -> torch.Tensor:
    """Whole-question compression: final state readout of the clean query."""
    ids = torch.tensor([b + BYTE_OFFSET for b in query], dtype=torch.long).unsqueeze(0).to(device)
    chunks, memory, gates = ph._encode_window(model, ids)
    n_real = int(chunks.chunk_mask[0].sum())
    state = model.state_machine.init_stream_state(1, device)
    handle = None
    if capture_raw is not None:
        handle = model.state_machine.realign.register_forward_pre_hook(_raw_hook(capture_raw))
    try:
        content, _ = ph._stream_window(model, gates, memory.size(1), n_real, state)
    finally:
        if handle is not None:
            handle.remove()
    return content[0, -1]  # (d_pack,)


@torch.no_grad()
def encode_document(model, ns, doc: bytes, entries: list, window: int, device: torch.device, mask_seed: int, carry_state: bool = True, capture_raw: bool = False):
    n_pages = len(doc) // window
    if n_pages < 2:
        return None
    doc = doc[: n_pages * window]
    state = model.state_machine.init_stream_state(1, device)
    cols, mem_cols, metas = [], [], {}
    raw_rows: list = []
    raw_handle = None
    if capture_raw:
        # v3 semi-thawed arm: keep the pre-realign reads so a trainable COPY
        # of the readout head can recompute keys on the fly (the loaded model
        # itself is never thawed).
        raw_handle = model.state_machine.realign.register_forward_pre_hook(_raw_hook(raw_rows))
    chunk_offset = 0
    try:
        for w in range(n_pages):
            if not carry_state:
                # V-side form: each page encoded with a FRESH state — the single-
                # window regime s22/s36 were trained in. Isolates the readout-form
                # dilution question from cross-page state aging (the carried-state
                # readback number is already the harness's 0.04 finding).
                state = model.state_machine.init_stream_state(1, device)
            raw = doc[w * window : (w + 1) * window]
            ids = torch.tensor([b + BYTE_OFFSET for b in raw], dtype=torch.long).unsqueeze(0)
            gen = torch.Generator().manual_seed(mask_seed * 100_003 + w)
            byte_mask = s1.make_mixed_mask(
                ids,
                ns.mask_prob,
                char_frac=getattr(ns, "mask_char_frac", 0.4),
                char_span_max=getattr(ns, "mask_char_span_max", 3),
                tokenizer=s1._BPE_TOKENIZER,
                generator=gen,
            )
            touched = False
            for e in entries:
                lo = max(e["lo"] - w * window, 0)
                hi = min(e["hi"] - w * window, window)
                if lo < hi:
                    byte_mask[0, lo:hi] = False  # entries (needle AND distractors) stay visible (E23)
                    touched = True
            ids = ids.to(device)
            source = ids.masked_fill(byte_mask.to(device), MASK_ID)
            chunks, memory, gates = ph._encode_window(model, source)
            n_real = int(chunks.chunk_mask[0].sum())
            if n_real < 2 or int(chunks.pack_info["truncated_tokens"].sum()) > 0:
                return None
            content_w, state = ph._stream_window(model, gates, memory.size(1), n_real, state)
            cols.append(content_w[0].to(torch.bfloat16))  # (n_real, d_pack)
            mem_cols.append(memory[0, :n_real].to(torch.bfloat16))  # (n_real, d_mem) — pre-state summarizer rows
            if touched:
                metas[w] = {
                    "offset": chunk_offset,
                    "n_real": n_real,
                    "chunk_ids": chunks.chunk_ids[0].cpu(),
                    "offsets": chunks.offsets[0].cpu(),
                    "tm": chunks.token_mask[0, :n_real].cpu(),
                }
            chunk_offset += n_real
    finally:
        if raw_handle is not None:
            raw_handle.remove()
    if capture_raw and len(raw_rows) != chunk_offset:
        return None  # hook/alignment failure — skip the doc rather than misalign keys
    content = torch.cat(cols, dim=0)  # (G, d_pack) bf16, device

    def span_chunks(lo: int, hi: int) -> list[int]:
        out = set()
        for w, m in metas.items():
            p_lo = max(lo - w * window, 0)
            p_hi = min(hi - w * window, window)
            if p_lo >= p_hi:
                continue
            for t in range(p_lo, p_hi):
                j = int(m["chunk_ids"][t])
                if 0 <= j < m["n_real"]:
                    out.add(m["offset"] + j)
        return sorted(out)

    needle = next(e for e in entries if e["needle"])
    code_units = []
    for t in range(needle["code_lo"], needle["code_hi"]):
        w = t // window
        m = metas.get(w)
        if m is None:
            return None
        j = int(m["chunk_ids"][t - w * window])
        slot = int(m["offsets"][t - w * window])
        if not (0 <= j < m["n_real"]) or not (0 <= slot < model.config.max_span):
            return None
        code_units.append((w, j, slot, doc[t] + BYTE_OFFSET))  # target = PAD-offset id of the digit byte
    enc = {
        "content": content,
        "memory": torch.cat(mem_cols, dim=0),  # (G, d_mem) bf16 — form-3 key source
        "g_total": chunk_offset,
        "n_pages": n_pages,
        "window": window,
        "metas": metas,
        "code_chunks": span_chunks(needle["code_lo"], needle["code_hi"]),
        "entry_chunks": span_chunks(needle["lo"], needle["hi"]),
        "code_units": code_units,
        "eid": needle["eid"],
        "code": needle["code"],
        "doc": doc,
        "entries": [{k: e[k] for k in ("eid", "code", "needle", "lo", "hi", "code_lo", "code_hi")} for e in entries],
    }
    if capture_raw:
        qraw: list = []
        enc["query"] = encode_query(model, _query_bytes(needle["eid"]), device, capture_raw=qraw).to(torch.bfloat16)
        enc["query_raw"] = qraw[-1]  # pre-realign read of the query's final chunk
        enc["reads"] = torch.stack(raw_rows, dim=0)  # (G, kda_heads*kda_head_v) bf16
    else:
        enc["query"] = encode_query(model, _query_bytes(needle["eid"]), device).to(torch.bfloat16)
    return enc


# ---------------------------------------------------------------------------
# K side: key geometry + the light retriever (W_q [+ W_k] only)
# ---------------------------------------------------------------------------


def block_boundary_index(g_total: int, gran: int, device: torch.device) -> torch.Tensor:
    """Key row of block b = the state readout right after the block's last
    chunk (one cross-chunk readout per `gran` chunks; gran=1 = per-chunk)."""
    return torch.tensor(
        [min(b + gran, g_total) - 1 for b in range(0, g_total, gran)], dtype=torch.long, device=device
    )


def positive_keys(entry_chunks: list[int], code_chunks: list[int], gran: int) -> tuple[list[int], list[int]]:
    return (
        sorted({c // gran for c in code_chunks}),
        sorted({c // gran for c in entry_chunks}),
    )


def pooled_block_keys(content: torch.Tensor, gran: int) -> torch.Tensor:
    """Mean-pool the `gran` per-chunk readouts of each block into one key
    (S39 v2 variant: does pooling rescue the coarse granularity from the
    last-chunk dominance of the block-boundary key?). Same block index space
    as block_boundary_index, so positives are shared."""
    g_total = content.size(0)
    n_full = g_total // gran
    parts = [content[: n_full * gran].view(n_full, gran, -1).mean(dim=1)]
    if g_total % gran:
        parts.append(content[n_full * gran :].mean(dim=0, keepdim=True))
    return torch.cat(parts, dim=0)


def extract_keys(enc: dict, cfg: dict) -> torch.Tensor:
    """Key matrix for one config: boundary = state readout after each block's
    last chunk; pooled = mean of the block's per-chunk readouts; memrow =
    pre-state summarizer memory rows (gran must be 1)."""
    src = cfg.get("key_src", "boundary")
    if src == "memrow":
        assert cfg["gran"] == 1, "memrow keys are per-chunk (gran=1)"
        return enc["memory"]
    if src == "pooled":
        return pooled_block_keys(enc["content"], cfg["gran"])
    return enc["content"][enc["kidx"][cfg["gran"]]]


class Retriever(nn.Module):
    """Query projection (+ key projection for the low-rank arm); cosine scores.
    Query space is always d_pack (the question's final state readout); the key
    space is d_pack for readout keys, d_mem for memrow keys."""

    def __init__(self, d_query: int, d_key: int, key_type: str, rank: int):
        super().__init__()
        self.key_type = key_type
        self.wq = nn.Linear(d_query, d_key if key_type == "full" else rank, bias=False)
        self.wk = None if key_type == "full" else nn.Linear(d_key, rank, bias=False)

    def scores(self, query: torch.Tensor, keys: torch.Tensor) -> torch.Tensor:
        qv = F.normalize(self.wq(query.float()), dim=-1)
        kv = keys.float() if self.wk is None else self.wk(keys.float())
        return F.normalize(kv, dim=-1) @ qv


def train_retriever(cfg: dict, train_set: list, args, device: torch.device, seed: int):
    torch.manual_seed(seed)
    retr = Retriever(cfg["d_query"], cfg["d_key"], cfg["key_type"], cfg["rank"] or 0).to(device)
    opt = torch.optim.Adam(retr.parameters(), lr=args.lr)
    rng = random.Random(seed)
    log = []
    for step in range(1, args.steps + 1):
        loss = torch.zeros((), device=device)
        for _ in range(args.batch_docs):
            d = train_set[rng.randrange(len(train_set))]
            keys = extract_keys(d, cfg)
            logp = F.log_softmax(retr.scores(d["query"], keys).float(), dim=0)
            loss = loss - logp[d["pos_code"][cfg["gran"]]].mean()
        loss = loss / args.batch_docs
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % args.log_every == 0 or step == args.steps:
            log.append({"step": step, "loss": round(float(loss.detach()), 4)})
    return retr, log


def train_budget(cfg: dict, train_set: list, args, device: torch.device, seed: int, eval_sets: dict, levels: list, milestones=(4000, 8000, 12000, 16000)):
    """v3 axis 2: 4x budget on the best learned-rank pooled config; eval
    snapshot at each milestone -> the saturation trajectory. Same seed and
    per-step rng consumption as train_retriever, so the 4K milestone exactly
    reproduces the rank-axis 4000-step numbers (built-in consistency check)."""
    torch.manual_seed(seed)
    retr = Retriever(cfg["d_query"], cfg["d_key"], cfg["key_type"], cfg["rank"] or 0).to(device)
    opt = torch.optim.Adam(retr.parameters(), lr=args.lr)
    rng = random.Random(seed)
    rows, done = [], 0
    for m in milestones:
        for _ in range(m - done):
            loss = torch.zeros((), device=device)
            for _ in range(args.batch_docs):
                d = train_set[rng.randrange(len(train_set))]
                keys = extract_keys(d, cfg)
                logp = F.log_softmax(retr.scores(d["query"], keys).float(), dim=0)
                loss = loss - logp[d["pos_code"][cfg["gran"]]].mean()
            loss = loss / args.batch_docs
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
        done = m
        row = {"steps": m, "loss": round(float(loss.detach()), 4), "levels": {}}
        for L in levels:
            row["levels"][str(L)] = eval_retriever(retr, eval_sets[L], cfg)
        rows.append(row)
        brief = " | ".join(
            f"D={L} hit@1/3/5={row['levels'][str(L)]['hit1']:.2f}/{row['levels'][str(L)]['hit3']:.2f}/{row['levels'][str(L)]['hit5']:.2f}"
            for L in levels
        )
        print(f"[K][budget r{cfg['rank']}][{m}] loss {row['loss']:.2f} {brief}", flush=True)
    return rows


def train_semi_thawed(realign_src: nn.Module, d_pack: int, train_set: list, args, device: torch.device, seed: int):
    """v3 axis 3 (key-producer plasticity): train a COPY of the readout head
    (state_machine.realign — the projection producing the state readouts that
    become keys) end-to-end on the retrieval loss, plus W_q; pooled/g4
    full-rank keys recomputed from the stored pre-realign reads every step.
    The loaded checkpoint itself is never modified (copy trained, then
    discarded)."""
    realign_t = copy.deepcopy(realign_src).to(device)
    for param in realign_t.parameters():
        param.requires_grad_(True)
    torch.manual_seed(seed)
    wq = nn.Linear(d_pack, d_pack, bias=False).to(device)
    opt = torch.optim.Adam(list(realign_t.parameters()) + list(wq.parameters()), lr=args.lr)
    rng = random.Random(seed)
    log = []
    for step in range(1, args.steps + 1):
        loss = torch.zeros((), device=device)
        for _ in range(args.batch_docs):
            d = train_set[rng.randrange(len(train_set))]
            keys = pooled_block_keys(realign_t(d["reads"].float()), 4)
            qv = F.normalize(wq(realign_t(d["query_raw"].float())), dim=-1)
            s = F.normalize(keys, dim=-1) @ qv
            logp = F.log_softmax(s.float(), dim=0)
            loss = loss - logp[d["pos_code"][4]].mean()
        loss = loss / args.batch_docs
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % args.log_every == 0 or step == args.steps:
            log.append({"step": step, "loss": round(float(loss.detach()), 4)})

    def score_fn(d):
        keys = pooled_block_keys(realign_t(d["reads"].float()), 4)
        qv = F.normalize(wq(realign_t(d["query_raw"].float())), dim=-1)
        return F.normalize(keys, dim=-1) @ qv

    return realign_t, wq, log, score_fn


@torch.no_grad()
def eval_retriever(retr: Retriever | None, eval_set: list, cfg: dict, ks=(1, 3, 5), score_fn=None) -> dict:
    gran = cfg["gran"]
    rows = []
    for d in eval_set:
        s = score_fn(d) if score_fn is not None else retr.scores(d["query"], extract_keys(d, cfg))
        order = torch.argsort(s.float(), descending=True).tolist()
        pos_code, pos_entry = set(d["pos_code"][gran].tolist()), set(d["pos_entry"][gran].tolist())
        row = {"n_keys": len(order), "n_pos": len(pos_code)}
        for k in ks:
            row[f"hit{k}"] = float(any(p in pos_code for p in order[:k]))
            row[f"hit{k}_entry"] = float(any(p in pos_entry for p in order[:k]))
        row["best_rank"] = min(i for i, p in enumerate(order) if p in pos_code) + 1
        rows.append(row)
    n = len(rows)
    kbar = sum(r["n_keys"] for r in rows) / n
    pbar = sum(r["n_pos"] for r in rows) / n

    def chance(k: int) -> float:  # random-ranking hit probability with P positives in K keys
        kk, pp = int(round(kbar)), max(1, int(round(pbar)))
        miss = 1.0
        for i in range(min(k, kk - pp)):
            miss *= 1.0 - pp / (kk - i)
        return 1.0 - miss

    out = {"n_docs": n, "n_keys_mean": round(kbar, 1), "n_pos_mean": round(pbar, 2),
           "best_rank_mean": round(sum(r["best_rank"] for r in rows) / n, 2)}
    for k in ks:
        out[f"hit{k}"] = round(sum(r[f"hit{k}"] for r in rows) / n, 4)
        out[f"hit{k}_entry"] = round(sum(r[f"hit{k}_entry"] for r in rows) / n, 4)
        out[f"rand{k}"] = round(chance(k), 4)
    return out


# ---------------------------------------------------------------------------
# V side: decode the needle code span (coarse paged readout / direct anchors)
# ---------------------------------------------------------------------------


@torch.no_grad()
def _decode_units(model, enc, cond_fn) -> tuple[int, int]:
    """cond_fn(w, j) -> (1, 1, d_backbone) conditioning row for page w chunk j."""
    correct, total = 0, 0
    by_chunk: dict[tuple[int, int], list] = {}
    for w, j, slot, tgt in enc["code_units"]:
        by_chunk.setdefault((w, j), []).append((slot, tgt))
    for (w, j), units in by_chunk.items():
        tm = enc["metas"][w]["tm"][j : j + 1].unsqueeze(0).to(enc["content"].device)
        logits = model.decoder(cond_fn(w, j), tm)
        pred = logits[0, 0].argmax(dim=-1)
        for slot, tgt in units:
            correct += int(int(pred[slot]) == tgt)
            total += 1
    return correct, total


@torch.no_grad()
def v_side_doc(v_model, v_ns, v_enc, k_model, k_enc) -> dict:
    out = {}
    # coarse arm: s22 /4 paged readout (page-local geometry, trained form)
    d_pack = v_model.config.d_pack

    def coarse_cond(w, j):
        m = v_enc["metas"][w]
        content_w = v_enc["content"][m["offset"] : m["offset"] + m["n_real"]].float().unsqueeze(0)
        mask_w = torch.ones(1, m["n_real"], dtype=torch.bool, device=content_w.device)
        boundary, serve = paged_boundaries(mask_w, v_ns.paged_reads)
        reads = content_w.gather(1, boundary.unsqueeze(-1).expand(-1, -1, d_pack))
        paged = v_model.backbone(reads)
        pos = v_model.chunk_pos.weight.unsqueeze(0)[:, : m["n_real"]]
        cond_all = paged.gather(1, serve.unsqueeze(-1).expand(-1, -1, paged.size(-1))) + pos
        return cond_all[:, j : j + 1]

    def v_direct_cond(w, j):
        m = v_enc["metas"][w]
        g = m["offset"] + j
        return v_model.decoder_in(v_enc["content"][g : g + 1].float().unsqueeze(0)) + v_model.chunk_pos.weight[j : j + 1].unsqueeze(0)

    def k_direct_cond(w, j):
        m = k_enc["metas"][w]
        g = m["offset"] + j
        return k_model.decoder_in(k_enc["content"][g : g + 1].float().unsqueeze(0)) + k_model.chunk_pos.weight[j : j + 1].unsqueeze(0)

    for arm, model, enc, fn in (
        ("coarse_paged", v_model, v_enc, coarse_cond),
        ("direct_v", v_model, v_enc, v_direct_cond),
        ("direct_fine", k_model, k_enc, k_direct_cond),
    ):
        correct, total = _decode_units(model, enc, fn)
        out[arm] = {"exact": float(correct == total and total > 0), "byte_acc": round(correct / max(total, 1), 4), "n_bytes": total}
    return out


# ---------------------------------------------------------------------------
# orchestration
# ---------------------------------------------------------------------------


def build_and_encode(model, ns, window, pages, n_distr, hay_fn, device, seed, max_tries=4, carry_state=True, capture_raw=False):
    rng = random.Random(seed)
    for _ in range(max_tries):
        raw = hay_fn(window * pages + (1 << 16), rng)
        # bound the haystack to the requested doc length: build_document only
        # shaves off the entry bytes, so the input must already be ~window*pages
        built = build_document(raw[: window * pages], n_distr, rng)
        if built is None:
            continue
        doc, entries = built
        enc = encode_document(model, ns, doc, entries, window, device, rng.randrange(1 << 30), carry_state=carry_state, capture_raw=capture_raw)
        if enc is not None:
            enc["n_distr"] = n_distr
            return enc
    return None


def prep_k_index(enc: dict, granularities: list[int], device: torch.device) -> None:
    enc["kidx"], enc["pos_code"], enc["pos_entry"] = {}, {}, {}
    for gran in granularities:
        enc["kidx"][gran] = block_boundary_index(enc["g_total"], gran, device)
        pc, pe = positive_keys(enc["entry_chunks"], enc["code_chunks"], gran)
        enc["pos_code"][gran] = torch.tensor(pc, dtype=torch.long, device=device)
        enc["pos_entry"][gran] = torch.tensor(pe, dtype=torch.long, device=device)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--smoke", action="store_true", help="small fast mechanism check")
    p.add_argument("--side", choices=["both", "k", "v"], default="both")
    p.add_argument("--k-run-dir", default="checkpoints/s36g2_ctx4096_b4_20k_20260809")
    p.add_argument("--k-fallback-dir", default="checkpoints/s36a_xcache_gist_full_20k_20260808")
    p.add_argument("--v-run-dir", default="checkpoints/s22_paged4_mlp_20k_20260807")
    p.add_argument("--data-root", default="P:/FLUED_corpus/FLUED_corpus_v4/shards")
    p.add_argument("--eval-data-root", default=str(ph.EVAL_DATA))
    p.add_argument("--suite", default="ruler/niah_single_1.jsonl", help="fallback haystack jsonl under eval-data-root")
    p.add_argument("--out-dir", default="outputs/s39_addressing_probe_20260810")
    p.add_argument("--pages", type=int, default=0, help="pages per doc at the K checkpoint's seq_len; 0 = 4 smoke / 8 full")
    p.add_argument("--train-docs", type=int, default=0, help="0 = 12 smoke / 48 full")
    p.add_argument("--eval-docs", type=int, default=0, help="per distractor level; 0 = 4 smoke / 12 full")
    p.add_argument("--steps", type=int, default=0, help="retriever steps per config; 0 = 400 smoke / 3000 full")
    p.add_argument("--batch-docs", type=int, default=4)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--levels", default="4,16,64", help="distractor counts")
    p.add_argument("--log-every", type=int, default=100)
    p.add_argument("--seed", type=int, default=1042)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument(
        "--preset",
        choices=["standard", "v2", "v3"],
        default="standard",
        help="v2 = K-side key-source variants (boundary/pooled/memrow). v3 = coarse-key ceiling: "
        "learnable W_k rank sweep on pooled/g4 {32..512} + full-rank anchors, 4x budget trajectory "
        "on the best rank, and the semi-thawed readout-head arm (plasticity test).",
    )
    p.add_argument("--report-name", default="", help="report filename under out-dir (default: report.json / report_smoke.json)")
    p.add_argument("--budget-milestones", default="4000,8000,12000,16000", help="v3 axis-2 eval snapshots (steps)")
    args = p.parse_args()
    mode = "smoke" if args.smoke else "full"
    pages = args.pages or (4 if args.smoke else 8)
    n_train = args.train_docs or (12 if args.smoke else 64)
    n_eval = args.eval_docs or (4 if args.smoke else 16)
    args.steps = args.steps or (400 if args.smoke else 4000)
    levels = [int(x) for x in args.levels.split(",")]
    granularities = [1, 4]
    if args.preset == "v2":
        # paired seeds: cfg["seed"] identical across the three configs
        configs = [
            {"key_type": "full", "rank": None, "gran": 1, "key_src": "boundary", "seed": args.seed},
            {"key_type": "full", "rank": None, "gran": 4, "key_src": "pooled", "seed": args.seed},
            {"key_type": "full", "rank": None, "gran": 1, "key_src": "memrow", "seed": args.seed},
        ]
    elif args.preset == "v3":
        # axis 1 (rank sweep on pooled/g4 with learnable W_k) + full-rank anchors;
        # axis 2 (budget) and axis 3 (semi-thawed readout head) run as follow-ons below
        configs = [
            {"key_type": "full", "rank": None, "gran": 1, "key_src": "boundary", "seed": args.seed, "axis": "anchor"},
            {"key_type": "full", "rank": None, "gran": 4, "key_src": "pooled", "seed": args.seed, "axis": "anchor"},
        ] + [
            {"key_type": "lowrank", "rank": r, "gran": 4, "key_src": "pooled", "seed": args.seed, "axis": "rank"}
            for r in (32, 64, 128, 256, 512)
        ]
    elif args.smoke:
        configs = [
            {"key_type": "full", "rank": None, "gran": 4},
            {"key_type": "lowrank", "rank": 64, "gran": 1},
            {"key_type": "lowrank", "rank": 32, "gran": 4},
        ]
    else:
        configs = [{"key_type": "full", "rank": None, "gran": g} for g in granularities] + [
            {"key_type": "lowrank", "rank": r, "gran": g} for g in granularities for r in (32, 64, 128, 256)
        ]

    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    timing: dict[str, float] = {}
    t_start = time.time()

    source_name, hay_fn = make_haystack_fn(args)
    print(f"[probe] mode={mode} device={device.type} haystack={source_name} pages={pages} levels={levels}", flush=True)

    k_model, k_ns, k_step, k_name = load_k_model(Path(args.k_run_dir), Path(args.k_fallback_dir), device)
    print(f"[probe] K model={k_name} step={k_step} seq_len={k_ns.seq_len}", flush=True)
    v_model = v_ns = v_step = None
    if args.side in ("both", "v"):
        v_model, v_ns, v_step = load_model(Path(args.v_run_dir), device, ("mlp", "xattn"))
        print(f"[probe] V model={Path(args.v_run_dir).name} step={v_step} seq_len={v_ns.seq_len} paged_reads={v_ns.paged_reads}", flush=True)

    # ---- encode doc pools (K checkpoint) ----
    t0 = time.time()
    train_set, eval_sets = [], {}
    capture_raw = args.preset == "v3"  # semi-thawed arm needs pre-realign reads
    if args.side in ("both", "k"):
        for i in range(n_train):
            enc = build_and_encode(k_model, k_ns, k_ns.seq_len, pages, levels[i % len(levels)], hay_fn, device, args.seed + i, capture_raw=capture_raw)
            if enc is not None:
                train_set.append(enc)
            if (i + 1) % max(1, n_train // 4) == 0:
                print(f"[probe] train docs {len(train_set)}/{i + 1} ({time.time() - t0:.0f}s)", flush=True)
        for L in levels:
            eval_sets[L] = []
            for i in range(n_eval):
                enc = build_and_encode(k_model, k_ns, k_ns.seq_len, pages, L, hay_fn, device, args.seed + 10_000 + L * 1_000 + i, capture_raw=capture_raw)
                if enc is not None:
                    eval_sets[L].append(enc)
            print(f"[probe] eval docs D={L}: {len(eval_sets[L])}/{n_eval} ({time.time() - t0:.0f}s)", flush=True)
        for enc in train_set + [e for docs in eval_sets.values() for e in docs]:
            prep_k_index(enc, granularities, device)
        if len(train_set) < args.batch_docs or any(not eval_sets[L] for L in levels):
            counts = {L: len(eval_sets[L]) for L in levels}
            raise RuntimeError(f"doc pool too small: train={len(train_set)} eval={counts} — check the haystack source")
    timing["encode_k_sec"] = round(time.time() - t0, 1)

    # ---- K side: train + eval per config ----
    k_results = []
    if args.side in ("both", "k"):
        t0 = time.time()
        d_pack, d_mem = k_model.config.d_pack, k_model.config.d_mem
        for ci, cfg in enumerate(configs):
            cfg = {**cfg, "d_query": d_pack, "d_key": d_mem if cfg.get("key_src") == "memrow" else d_pack}
            retr, loss_log = train_retriever(cfg, train_set, args, device, cfg.get("seed", args.seed + 31 * ci))
            row = {
                "key_type": cfg["key_type"],
                "key_src": cfg.get("key_src", "boundary"),
                "axis": cfg.get("axis", "sweep"),
                "rank": cfg["rank"],
                "granularity": cfg["gran"],
                "train_loss_first": loss_log[0]["loss"],
                "train_loss_last": loss_log[-1]["loss"],
                "loss_log": loss_log,
                "levels": {},
            }
            for L in levels:
                row["levels"][str(L)] = eval_retriever(retr, eval_sets[L], cfg)
            k_results.append(row)
            tag = f"{cfg.get('key_src', 'boundary')}:{cfg['key_type']}{'' if cfg['rank'] is None else cfg['rank']}/g{cfg['gran']}"
            brief = " | ".join(
                f"D={L} hit@1/3/5={row['levels'][str(L)]['hit1']:.2f}/{row['levels'][str(L)]['hit3']:.2f}/{row['levels'][str(L)]['hit5']:.2f}(rand {row['levels'][str(L)]['rand1']:.3f})"
                for L in levels
            )
            print(f"[K][{tag}] loss {row['train_loss_first']:.2f}->{row['train_loss_last']:.2f} {brief}", flush=True)
        timing["k_side_sec"] = round(time.time() - t0, 1)

    # ---- v3 follow-on axes: budget trajectory + semi-thawed readout head ----
    k_budget, k_semi = None, None
    if args.preset == "v3" and args.side in ("both", "k"):
        # axis 2: best learned-rank pooled config at 4x budget. Selection rule
        # (fixed a priori): max hit5@D64 + hit5@D16, tie -> hit1@D16, then lower rank.
        t0 = time.time()
        pairs = [(c, r) for c, r in zip(configs, k_results) if c.get("axis") == "rank"]
        best_cfg, best_row = max(
            pairs,
            key=lambda cr: (
                cr[1]["levels"]["64"]["hit5"] + cr[1]["levels"]["16"]["hit5"],
                cr[1]["levels"]["16"]["hit1"],
                -(cr[0]["rank"] or 10**9),
            ),
        )
        print(f"[K][v3] budget axis picks rank={best_cfg['rank']} (axis-1 hit5 D16={best_row['levels']['16']['hit5']} D64={best_row['levels']['64']['hit5']})", flush=True)
        bcfg = {**best_cfg, "d_query": d_pack, "d_key": d_pack}
        milestones = tuple(int(x) for x in args.budget_milestones.split(","))
        k_budget = {
            "config": {"key_src": best_cfg["key_src"], "key_type": best_cfg["key_type"], "rank": best_cfg["rank"], "granularity": best_cfg["gran"]},
            "milestones": train_budget(bcfg, train_set, args, device, args.seed, eval_sets, levels, milestones=milestones),
        }
        # axis 3: semi-thawed readout head (plasticity). Only a COPY of
        # state_machine.realign + W_q train; the checkpoint stays frozen.
        realign_t, wq, semi_log, semi_score_fn = train_semi_thawed(
            k_model.state_machine.realign, d_pack, train_set, args, device, args.seed
        )
        semi_cfg = {"gran": 4}
        k_semi = {
            "unfrozen": "state_machine.realign (copy) + W_q",
            "key": "pooled/g4 full-rank, recomputed from pre-realign reads each step",
            "train_loss_first": semi_log[0]["loss"],
            "train_loss_last": semi_log[-1]["loss"],
            "loss_log": semi_log,
            "levels": {str(L): eval_retriever(None, eval_sets[L], semi_cfg, score_fn=semi_score_fn) for L in levels},
        }
        brief = " | ".join(
            f"D={L} hit@1/3/5={k_semi['levels'][str(L)]['hit1']:.2f}/{k_semi['levels'][str(L)]['hit3']:.2f}/{k_semi['levels'][str(L)]['hit5']:.2f}"
            for L in levels
        )
        print(f"[K][semi-thawed pooled/g4] loss {k_semi['train_loss_first']:.2f}->{k_semi['train_loss_last']:.2f} {brief}", flush=True)
        del realign_t, wq  # disposable arm — nothing persists
        timing["v3_axes_sec"] = round(time.time() - t0, 1)

    # ---- V side: needle code-span decode, both granularities ----
    v_results: dict[str, dict] = {}
    if args.side in ("both", "v"):
        t0 = time.time()
        if not eval_sets:  # side=v: build the eval pool here (K model still provides the fine anchor)
            for L in levels:
                eval_sets[L] = []
                for i in range(n_eval):
                    enc = build_and_encode(k_model, k_ns, k_ns.seq_len, pages, L, hay_fn, device, args.seed + 10_000 + L * 1_000 + i)
                    if enc is not None:
                        eval_sets[L].append(enc)
        for L in levels:
            rows = []
            for i, k_enc in enumerate(eval_sets[L]):
                # V side is measured with a FRESH state per page (the single-
                # window regime both checkpoints were trained in): the question
                # is the readout FORM's needle-dilution ceiling, not cross-page
                # state aging (harness already owns the carried-state number).
                v_enc = encode_document(
                    v_model, v_ns, k_enc["doc"], k_enc["entries"], v_ns.seq_len, device,
                    args.seed + 20_000 + L * 1_000 + i, carry_state=False,
                )
                k_fresh = encode_document(
                    k_model, k_ns, k_enc["doc"], k_enc["entries"], k_ns.seq_len, device,
                    args.seed + 30_000 + L * 1_000 + i, carry_state=False,
                )
                if v_enc is None or k_fresh is None:
                    continue
                rows.append({"eid": k_enc["eid"], **v_side_doc(v_model, v_ns, v_enc, k_model, k_fresh)})
                del v_enc, k_fresh
                if device.type == "cuda":
                    torch.cuda.empty_cache()
            arms = {}
            for arm in ("coarse_paged", "direct_v", "direct_fine"):
                n = len(rows)
                arms[arm] = {
                    "exact": round(sum(r[arm]["exact"] for r in rows) / max(n, 1), 4),
                    "byte_acc": round(sum(r[arm]["byte_acc"] for r in rows) / max(n, 1), 4),
                    "n_docs": n,
                    "n_bytes": sum(r[arm]["n_bytes"] for r in rows),
                }
            v_results[str(L)] = {"arms": arms, "docs": rows}
            print(
                f"[V][D={L}] coarse exact={arms['coarse_paged']['exact']:.2f} byte={arms['coarse_paged']['byte_acc']:.2f} | "
                f"direct_s22 byte={arms['direct_v']['byte_acc']:.2f} | direct_s36g2 exact={arms['direct_fine']['exact']:.2f} byte={arms['direct_fine']['byte_acc']:.2f}",
                flush=True,
            )
        timing["v_side_sec"] = round(time.time() - t0, 1)
    timing["total_sec"] = round(time.time() - t_start, 1)

    report = {
        "probe": "S39 step-0 archive addressing/fidelity (spec §26)",
        "mode": mode,
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data_source": source_name,
        "checkpoints": {
            "k": {"run": k_name, "step": k_step},
            "v": ({"run": Path(args.v_run_dir).name, "step": v_step} if v_model is not None else None),
        },
        "params": {
            "pages": pages, "train_docs": len(train_set), "eval_docs_per_level": {str(L): len(eval_sets[L]) for L in levels},
            "steps": args.steps, "batch_docs": args.batch_docs, "lr": args.lr, "levels": levels,
            "granularities": granularities, "seed": args.seed, "preset": args.preset,
        },
        "protocol": {
            "entry": "档案条目 QX-#### 的校验码为 ######。", "query": "条目 QX-#### 的校验码是什么？",
            "positives": "key rows covering the needle CODE digits (hit*_entry = entry-level diagnostic)",
            "key_row": "boundary = block-boundary state readout (gran=1 per-chunk; gran=4 one per 4 chunks); "
            "pooled = mean of the block's per-chunk readouts; memrow = pre-state summarizer memory row (per-chunk)",
            "mask": "P0 mixed mask; needle AND distractor entries force-unmasked (E23)",
            "state": "K side: carried across pages (archive form); V side: fresh per page (trained single-window regime)",
        },
        "k_side": k_results,
        "k_budget_axis": k_budget,
        "k_semi_thawed_axis": k_semi,
        "v_side": v_results,
        "timing_sec": timing,
    }
    default_name = "report_smoke.json" if args.smoke else "report.json"
    out_path = out_dir / (args.report_name or default_name)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[probe] report -> {out_path} (total {timing['total_sec']}s)", flush=True)


if __name__ == "__main__":
    main()
