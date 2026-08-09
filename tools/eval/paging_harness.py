"""Multi-page / archive evaluation harness for FLUED v3.6 (built 2026-08-09).

DESIGN DRAFT (user-ruled unattended task; read-only checkpoints, no training)
==============================================================================

Form: a long document (10KB-100KB+) is encoded as a SEQUENCE OF PAGES (windows
of W bytes, default the run's own ``seq_len``). Pages are encoded strictly in
order and the KDA state is CARRIED across pages through
``KDAStateMachine.stream_step`` -- turning the page archives the state, nothing
is dropped. Per page the deployment-faithful streaming loop is:

    source_w = mask(ids_w)            # 40/60 mixed mask, P0 protocol
    chunks_w = front_end(source_w)    # frozen byte embedder + segmentor
    memory_w = summarizer(chunks_w)   # one d_mem row per chunk (pre-state)
    gates_w  = write_head(memory_w)
    for i in real chunks of page w:   # carried state, O(C) per page
        package_i, state = stream_step(gates_i, state)
        content[i] = package_i        # readout of S right after chunk i

The page's direct path is decoded once (cond = decoder_in(content) + pos),
yielding the page codec metrics AND the per-chunk residual (decode CE). The
residual gate then selects the page's top-b hardest chunks whose VERBATIM
memory rows are appended to the PAGE-LEVEL CACHE: exact rows that never decay
across pages, addressed by GLOBAL chunk index (page offset + local index).

Backbone reads reuse the trained CrossReadBackbone store interface with no
model modification: the cache is materialized as a synthetic global memory
matrix (row g = cached row of global chunk g, zeros elsewhere) plus a
``cache_idx`` list of cached global indices. Because the backbone derives
visibility from ``cache_idx <= query_pos``, global indices reproduce the
training-time causality exactly, extended across pages: a query on page w sees
every archived row of pages < w and the causal (<= query) rows of page w. The
gist token = readout of the carried state after the page's last chunk (the
training form: gist = content[last], visible to all positions).

Three measurements:

1. PAGE DECAY CURVE: per page k, direct/backbone byte accuracy (all slots and
   masked-only) vs k -- codec fidelity as the carried state ages and the
   archive grows. The backbone curve is reported per cache budget.
2. REMOTE NEEDLE READBACK: a synthetic RULER-style needle ("The special magic
   number is: <7 digits>. ") is spliced into page --needle-window (0-based,
   default 1) at a known byte span and kept visible under the mask (E23:
   readback measures retention of ENCODED bytes). After encoding all pages the
   needle span is decoded three ways: direct (state-only, probe_paging_signal
   style: content_final + pos_j), backbone (query content_final + pos_j over
   the full archive store), and a self-query control (the needle chunk's OWN
   phase-1 readout as the query, causally capped at the chunk's global index
   -- exactly the trained query form; separates "remote-query interface"
   failure from "store content" failure). Reports byte acc, exact match, and
   the cache-hit rate of the needle chunks.
3. CACHE BUDGET SCAN: the page-level budget b (rows kept per page; -1 =
   unlimited) is swept with the SAME carried-state trajectory (encoding runs
   once; the residual is budget-independent), so budgets are paired. This is
   the courtroom for the "residual matrix vs verbatim rows" judgment.

S38B INTERFACE (residual second state S'): ``--entry-mode supp`` replaces
verbatim rows with S' readout rows. When the checkpoint carries the S38 heads
(``state_machine.supp_q``/``supp_out``) and ``supp_source="residual"``, the
harness carries a SECOND KDA state S' alongside S: after page w's direct
decode, ``write_w = sigmoid((resid - median)/temp)`` (detached, CUIB gating,
mirroring train_v36_s1) and S' is streamed over the same gates with
``beta * write_w`` (stream_step accepts the scaled beta verbatim). Page
entries are then ``supp_out(normalize(supp_q(content_i)) . S'_i)`` vectors
(d_pack) entering the store through the backbone's gist projections via the
existing ``supp``/``supp_idx`` arguments -- same global-index causality. The
budget scan then A/Bs "verbatim row per page entry" vs "S' row per page
entry" under identical selection. (Not smoked here: s36f/s36g2 predate the
S38 heads; smoke covers --entry-mode memory only.)

Honesty notes / limits:
- fp32, no autocast; batch 1, one sample at a time; checkpoints are loaded
  read-only. Keep the GPU footprint serial and small; pass --device cpu when
  a training run owns the GPU.
- Position embeddings stay page-LOCAL (chunk_pos has max_chunks entries;
  global positions would leave the trained grid after ~2 pages). Cross-page
  order information travels only through the carried state and the store
  causality integers -- a deliberate, documented deviation.
- The mask protocol matches training/P0 (the state is built from the masked
  source); the needle span is force-unmasked.
- A trailing partial page (< W bytes) is dropped; a doc must provide at least
  needle_window+2 full pages. Readback uses the FINAL state + full archive;
  "read after exactly page r" = truncate via --windows r+1.

Usage (smoke):
  python tools/eval/paging_harness.py \
      --run-dir checkpoints/s36f_ctx2048_20k_20260808 \
      --suites ruler/niah_single_1.jsonl --limit 2 --windows 5 \
      --budgets 5,-1 --needle-window 1
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from argparse import Namespace
from pathlib import Path

import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.train.v3_6.train_v36 import build_model  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402

EVAL_DATA = Path("E:/projects/FLUED/eval_data")
BYTE_OFFSET = 1  # data.py PAD-offset convention: byte b -> id b+1, PAD=0


def _load_model(run_dir: Path, device: torch.device):
    """resolved_config.json -> Namespace -> build_model -> latest.pt (read-only)."""
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_path"] = "unused"  # no dataloaders; pages come from eval files
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"  # fla kernels are GPU-only
    ns = Namespace(**cfg)
    if getattr(ns, "backbone_mode", "") != "xattn":
        raise ValueError(
            f"paging harness expects backbone_mode='xattn' (gist+cache store form), got {ns.backbone_mode!r}"
        )
    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed" and ns.mask_prob > 0:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    model = build_model(ns).to(device)
    payload = torch.load(run_dir / "latest.pt", map_location=device, weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    model.eval()
    return model, ns, int(payload.get("step", 0))


def _snap_utf8(bs: bytes, p: int) -> int:
    """Snap forward to a UTF-8 char start (continuation bytes are 10xxxxxx)."""
    while p < len(bs) and (bs[p] & 0xC0) == 0x80:
        p += 1
    return p


def _insert_needle(doc: bytes, window: int, needle_window: int, rng: random.Random):
    """Splice a RULER-style needle into the middle of page ``needle_window``."""
    digits = "".join(rng.choice("0123456789") for _ in range(7))
    needle = f"The special magic number is: {digits}. ".encode("ascii")
    p = _snap_utf8(doc, min(len(doc), needle_window * window + window // 2))
    return doc[:p] + needle + doc[p:], p, p + len(needle), needle


def _slice_gates(gates: dict, i: int, width: int) -> dict:
    """One chunk's write gates (probe_paging_signal slicing convention)."""
    return {
        kk: (vv[:, i : i + 1] if isinstance(vv, torch.Tensor) and vv.dim() >= 2 and vv.size(1) == width else vv)
        for kk, vv in gates.items()
    }


@torch.no_grad()
def _encode_window(model, source: torch.Tensor):
    """Front-end + chunking + summarizer + write head for one page."""
    byte_states, confidence, valid, _ = model._encode(source)
    hard_cut, utf8_cont, _ = model._cuts(source, confidence, valid)
    chunks = model.chunk_builder(byte_states, valid, hard_cut, confidence)
    chunks = model.bridge(chunks, byte_states, confidence, valid, utf8_cont)
    memory = model.summarizer(chunks.span_embeddings, chunks.token_mask)
    gates = model.write_head(memory)
    return chunks, memory, gates


@torch.no_grad()
def _stream_window(model, gates: dict, width: int, n_real: int, state: torch.Tensor):
    """Carried-state streaming over one page (O(C)); returns per-chunk readouts
    content (1, n_real, d_pack) and the carried state."""
    cols = []
    for i in range(n_real):
        package_i, state = model.state_machine.stream_step(_slice_gates(gates, i, width), state)
        cols.append(package_i[:, 0].mean(dim=1))  # (1, d_pack), nq-mean like the batched path
    return torch.stack(cols, dim=1), state


@torch.no_grad()
def _supp_window(model, gates: dict, width: int, content_w: torch.Tensor, resid_w: torch.Tensor, state2: torch.Tensor):
    """S38B streaming analogue of read_residual: carry S' across pages with
    CE-gated write weights; returns per-chunk supp rows (1, C, d_pack)."""
    sm = model.state_machine
    c = model.config
    temp = getattr(c, "residual_gate_temp", 1.0)
    med = resid_w.nanmedian(dim=1, keepdim=True).values.nan_to_num(0.0)
    write_w = torch.sigmoid((resid_w - med) / temp).detach()  # (1, C) — CUIB gating
    rows = []
    for i in range(content_w.size(1)):
        gates_i = _slice_gates(gates, i, width)
        gates_i["beta"] = gates_i["beta"] * write_w[:, i : i + 1].unsqueeze(-1).to(gates_i["beta"].dtype)
        _, state2 = sm.stream_step(gates_i, state2)
        q_i = F.normalize(
            sm.supp_q(content_w[:, i : i + 1]).view(1, c.kda_heads, c.kda_head_k).float(), dim=-1
        )
        read_i = torch.einsum("bhk,bhkv->bhv", q_i, state2)
        rows.append(sm.supp_out(read_i.reshape(1, c.kda_heads * c.kda_head_v).to(content_w.dtype)))
    return torch.stack(rows, dim=1), state2


@torch.no_grad()
def _decode(model, cond: torch.Tensor, token_mask: torch.Tensor) -> torch.Tensor:
    return model.decoder(cond, token_mask)


def _accs(logits: torch.Tensor, targets: torch.Tensor, slot_mask: torch.Tensor, masked_slot: torch.Tensor):
    pred = logits.argmax(-1)
    return float(s1._acc_tensor(pred, targets, slot_mask)), float(s1._acc_tensor(pred, targets, masked_slot))


def _resid(logits: torch.Tensor, targets: torch.Tensor, slot_mask: torch.Tensor) -> torch.Tensor:
    """Per-chunk mean direct-decode CE (the S36/S37 residual gate criterion)."""
    ce = F.cross_entropy(
        logits.float().reshape(-1, logits.size(-1)),
        targets.reshape(-1).clamp(min=0, max=257),
        reduction="none",
        ignore_index=s1.PAD_ID,
    ).reshape(targets.shape)
    return (ce * slot_mask.float()).sum(-1) / slot_mask.float().sum(-1).clamp(min=1.0)


def _build_store(sel_rows: dict, g_total: int, dim: int, device: torch.device):
    """Materialize the synthetic global store: row g of a (1, G, d) matrix is
    the cached entry of global chunk g (zeros elsewhere); the returned index
    list carries the cached global indices (the backbone derives visibility
    from the VALUES, so global indices give cross-page causality)."""
    store = torch.zeros(1, g_total, dim, device=device)
    idx = sorted(sel_rows)
    for g in idx:
        store[0, g] = sel_rows[g]
    cache_idx = torch.tensor([idx], dtype=torch.long, device=device) if idx else torch.zeros(1, 0, dtype=torch.long, device=device)
    return store, cache_idx


@torch.no_grad()
def _backbone_cond(model, content, store, cache_idx, gist, query_pos, entry, supp_store=None, supp_idx=None):
    """One CrossReadBackbone call over the archive store -> conditioning rows."""
    pos = model.chunk_pos.weight.unsqueeze(0)[:, : content.size(1)]
    g_mask = torch.ones(1, store.size(1), dtype=torch.bool, device=store.device)
    if entry == "supp":
        # S38B: no verbatim rows -- the store travels via the gist projections
        out = model.backbone(
            content, store, g_mask, pos, cache_idx=cache_idx, gist=gist, query_pos=query_pos,
            supp=supp_store, supp_idx=supp_idx,
        )
    else:
        out = model.backbone(content, store, g_mask, pos, cache_idx=cache_idx, gist=gist, query_pos=query_pos)
    return out + pos


@torch.no_grad()
def run_sample(model, ns, ctx_bytes: bytes, sample_seed: int, args, device) -> dict | None:
    W = args.window_bytes
    rng = random.Random(sample_seed)
    doc, n0, n1, needle = _insert_needle(ctx_bytes, W, args.needle_window, rng)
    n_pages = min(args.windows, len(doc) // W)
    if n_pages < args.needle_window + 2:
        return None  # too short: needle page + at least one interference page required
    doc = doc[: n_pages * W]

    entry = args.entry_mode
    state = model.state_machine.init_stream_state(1, device)
    state2 = model.state_machine.init_stream_state(1, device) if entry == "supp" else None

    # ---- phase 1: streaming encode (once; shared by all budgets) ----
    pages = []
    chunk_offset = 0
    for w in range(n_pages):
        raw = doc[w * W : (w + 1) * W]
        ids = torch.tensor([b + BYTE_OFFSET for b in raw], dtype=torch.long).unsqueeze(0)
        gen = torch.Generator().manual_seed(sample_seed * 100_003 + w)
        byte_mask = s1.make_mixed_mask(
            ids, ns.mask_prob, char_frac=ns.mask_char_frac, char_span_max=ns.mask_char_span_max,
            tokenizer=s1._BPE_TOKENIZER, generator=gen,
        )
        if w == args.needle_window:
            byte_mask[0, n0 - w * W : n1 - w * W] = False  # needle stays visible (E23)
        ids = ids.to(device)
        byte_mask = byte_mask.to(device)
        source = ids.masked_fill(byte_mask, s1.MASK_ID)
        chunks, memory, gates = _encode_window(model, source)
        n_real = int(chunks.chunk_mask[0].sum())
        if n_real < 2:
            return None
        content_w, state = _stream_window(model, gates, memory.size(1), n_real, state)
        tm = chunks.token_mask[:, :n_real]
        targets, slot_mask, masked_slot = s1.make_targets(
            ids, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
        )
        targets, slot_mask, masked_slot = targets[:, :n_real], slot_mask[:, :n_real], masked_slot[:, :n_real]
        pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_real]
        logits_d = _decode(model, model.decoder_in(content_w) + pos, tm)
        resid = _resid(logits_d, targets, slot_mask)  # (1, n_real)
        d_acc, d_acc_m = _accs(logits_d, targets, slot_mask, masked_slot)
        supp_w = None
        if entry == "supp":
            supp_w, state2 = _supp_window(model, gates, memory.size(1), content_w, resid, state2)
        page = {
            "w": w, "n_real": n_real, "offset": chunk_offset,
            "content": content_w, "memory": memory[:, :n_real], "supp": supp_w,
            "resid": resid[0], "tm": tm, "targets": targets, "slot_mask": slot_mask,
            "masked_slot": masked_slot, "d_acc": d_acc, "d_acc_m": d_acc_m,
            "state_norm": float(state.norm(dim=(-2, -1)).mean()),
            "truncated": int(chunks.pack_info["truncated_tokens"].sum()),
        }
        if w == args.needle_window:
            page["chunk_ids"] = chunks.chunk_ids
            page["offsets"] = chunks.offsets
            page["ids"] = ids
        pages.append(page)
        chunk_offset += n_real

    g_total = chunk_offset
    content_final = pages[-1]["content"][:, -1]  # (1, d_pack) — archive-end state readout

    # ---- phase 2: per-budget store replay (paired; encoding NOT redone) ----
    entry_dim = model.config.d_mem if entry == "memory" else model.config.d_pack
    sels = {b: {} for b in args.budgets}
    codec_rows = []
    for p in pages:
        row = {
            "window": p["w"], "n_real": p["n_real"],
            "direct_acc": round(p["d_acc"], 4), "direct_acc_masked": round(p["d_acc_m"], 4),
            "state_norm": round(p["state_norm"], 2), "truncated_tokens": p["truncated"],
            "backbone": {},
        }
        for b in args.budgets:
            k = p["n_real"] if b < 0 else min(b, p["n_real"])
            top = p["resid"][: p["n_real"]].topk(k).indices.tolist()
            for j in top:
                g = p["offset"] + j
                sels[b][g] = (p["memory"] if entry == "memory" else p["supp"])[0, j]
            G = p["offset"] + p["n_real"]
            store, cache_idx = _build_store(sels[b], G, entry_dim, device)
            if entry == "supp":
                mem_ph = torch.zeros(1, G, model.config.d_mem, device=device)
                empty = torch.zeros(1, 0, dtype=torch.long, device=device)
                cond_b = _backbone_cond(
                    model, p["content"], mem_ph, empty, p["content"][:, -1],
                    torch.arange(p["offset"], G, device=device).unsqueeze(0),
                    entry, supp_store=store, supp_idx=cache_idx,
                )
            else:
                cond_b = _backbone_cond(
                    model, p["content"], store, cache_idx, p["content"][:, -1],
                    torch.arange(p["offset"], G, device=device).unsqueeze(0), entry,
                )
            logits_b = _decode(model, cond_b, p["tm"])
            b_acc, b_acc_m = _accs(logits_b, p["targets"], p["slot_mask"], p["masked_slot"])
            row["backbone"][str(b)] = {
                "acc": round(b_acc, 4), "acc_masked": round(b_acc_m, 4), "cache_rows": len(sels[b]),
            }
        codec_rows.append(row)

    # ---- needle readback from the archive end ----
    np_ = pages[args.needle_window]
    woff = args.needle_window * W
    lo, hi = n0 - woff, n1 - woff
    cid, off, ids_nw = np_["chunk_ids"][0], np_["offsets"][0], np_["ids"][0]
    needle_chunks = sorted({int(cid[t]) for t in range(lo, hi) if 0 <= int(cid[t]) < np_["n_real"]})
    # per-chunk (slot, target) pairs over the needle span
    pairs = {}
    for j in needle_chunks:
        pts = [(int(off[t]), int(ids_nw[t])) for t in range(lo, hi) if int(cid[t]) == j and 0 <= int(off[t]) < model.config.max_span]
        if pts:
            pairs[j] = pts

    def readback(cond_fn):
        correct, total = 0, 0
        for j, pts in pairs.items():
            mask_j = np_["tm"][:, j : j + 1]
            logits = _decode(model, cond_fn(j), mask_j)
            for s, tgt in pts:
                correct += int(int(logits[0, 0, s].argmax()) == tgt)
                total += 1
        return (correct / total) if total else 0.0

    pos_w = model.chunk_pos.weight
    direct_needle = readback(lambda j: model.decoder_in(content_final.unsqueeze(1)) + pos_w[j : j + 1].unsqueeze(0))
    readback_rows = {}
    for b in args.budgets:
        store, cache_idx = _build_store(sels[b], g_total, entry_dim, device)
        qp = torch.tensor([[g_total]], dtype=torch.long, device=device)  # archive end: see everything

        # readback query for needle chunk j: the final state readout + pos[j],
        # over the full archive store (direct analogue of probe_paging_signal)
        def cond_fn(j):  # noqa: E731
            pos_j = pos_w[j : j + 1].unsqueeze(0)
            g_mask = torch.ones(1, g_total, dtype=torch.bool, device=device)
            if entry == "supp":
                mem_ph = torch.zeros(1, g_total, model.config.d_mem, device=device)
                empty = torch.zeros(1, 0, dtype=torch.long, device=device)
                out = model.backbone(
                    content_final.unsqueeze(1), mem_ph, g_mask, pos_j,
                    cache_idx=empty, gist=content_final, query_pos=qp,
                    supp=store, supp_idx=cache_idx,
                )
            else:
                out = model.backbone(
                    content_final.unsqueeze(1), store, g_mask, pos_j,
                    cache_idx=cache_idx, gist=content_final, query_pos=qp,
                )
            return out + pos_j

        bb_needle = readback(cond_fn)

        # self-query control arm: the needle chunk's OWN phase-1 readout as the
        # query (exactly the trained query form), causally capped at the chunk's
        # global index. Separates "remote-query interface" failure from "store
        # content" failure in the budget scan.
        def cond_selfq(j):  # noqa: E731
            pos_j = pos_w[j : j + 1].unsqueeze(0)
            g_j = np_["offset"] + j
            q = np_["content"][:, j : j + 1]
            qp_j = torch.tensor([[g_j]], dtype=torch.long, device=device)
            g_mask = torch.ones(1, store.size(1), dtype=torch.bool, device=device)
            if entry == "supp":
                mem_ph = torch.zeros(1, store.size(1), model.config.d_mem, device=device)
                empty = torch.zeros(1, 0, dtype=torch.long, device=device)
                out = model.backbone(
                    q, mem_ph, g_mask, pos_j, cache_idx=empty, gist=content_final,
                    query_pos=qp_j, supp=store, supp_idx=cache_idx,
                )
            else:
                out = model.backbone(
                    q, store, g_mask, pos_j, cache_idx=cache_idx, gist=content_final,
                    query_pos=qp_j,
                )
            return out + pos_j

        sq_needle = readback(cond_selfq)
        hit = [g for g in (np_["offset"] + j for j in pairs) if g in sels[b]]
        readback_rows[str(b)] = {
            "needle_direct_acc": round(direct_needle, 4),
            "needle_backbone_acc": round(bb_needle, 4),
            "needle_selfq_backbone_acc": round(sq_needle, 4),
            "needle_exact": int(bb_needle == 1.0),
            "cache_hit": round(len(hit) / max(len(pairs), 1), 4),
            "cache_rows": len(sels[b]),
        }

    return {
        "n_pages": n_pages, "chunks_total": g_total,
        "needle": {
            "window": args.needle_window, "span": [n0, n1], "text": needle.decode("ascii"),
            "chunks_local": needle_chunks, "chunks_global": [np_["offset"] + j for j in needle_chunks],
        },
        "codec": codec_rows,
        "readback": readback_rows,
    }


def _aggregate(samples: list[dict], budgets: list[int]) -> dict:
    by_w: dict[int, list[dict]] = {}
    for s in samples:
        for row in s["codec"]:
            by_w.setdefault(row["window"], []).append(row)
    codec_agg = {}
    for w, rows in sorted(by_w.items()):
        agg = {
            "n": len(rows),
            "direct_acc": round(sum(r["direct_acc"] for r in rows) / len(rows), 4),
            "direct_acc_masked": round(sum(r["direct_acc_masked"] for r in rows) / len(rows), 4),
        }
        for b in budgets:
            agg[f"backbone_acc_b{b}"] = round(sum(r["backbone"][str(b)]["acc"] for r in rows) / len(rows), 4)
        codec_agg[str(w)] = agg
    needle_agg = {}
    for b in budgets:
        rows = [s["readback"][str(b)] for s in samples]
        needle_agg[str(b)] = {
            "n": len(rows),
            "needle_direct_acc": round(sum(r["needle_direct_acc"] for r in rows) / len(rows), 4),
            "needle_backbone_acc": round(sum(r["needle_backbone_acc"] for r in rows) / len(rows), 4),
            "needle_selfq_backbone_acc": round(sum(r["needle_selfq_backbone_acc"] for r in rows) / len(rows), 4),
            "needle_exact": round(sum(r["needle_exact"] for r in rows) / len(rows), 4),
            "cache_hit": round(sum(r["cache_hit"] for r in rows) / len(rows), 4),
        }
    return {"codec_by_window": codec_agg, "needle_by_budget": needle_agg}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--suites", nargs="+", default=["ruler/niah_single_1.jsonl"],
                        help="JSONL suites under --eval-data-root with a 'context' field (haystacks)")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--windows", type=int, default=20, help="max pages per document")
    parser.add_argument("--window-bytes", type=int, default=0, help="page size; 0 = run's seq_len")
    parser.add_argument("--budgets", type=str, default="5,10,-1", help="page-level cache rows per page; -1 = unlimited")
    parser.add_argument("--needle-window", type=int, default=1, help="0-based page index the needle is spliced into")
    parser.add_argument("--entry-mode", choices=["memory", "supp"], default="memory",
                        help="page-entry kind: verbatim memory rows (S36) | S' residual rows (S38B)")
    parser.add_argument("--eval-data-root", default=str(EVAL_DATA))
    parser.add_argument("--seed", type=int, default=1042)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    args.budgets = [int(x) for x in args.budgets.split(",")]

    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    model, ns, step = _load_model(Path(args.run_dir), device)
    if args.window_bytes <= 0:
        args.window_bytes = ns.seq_len
    if args.entry_mode == "supp" and not hasattr(model.state_machine, "supp_q"):
        raise ValueError("--entry-mode supp requires an S38 checkpoint with supp heads (supp_q/supp_out)")

    report = {
        "run_dir": Path(args.run_dir).name, "step": step, "device": device.type,
        "window_bytes": args.window_bytes, "budgets": args.budgets,
        "needle_window": args.needle_window, "entry_mode": args.entry_mode,
        "mask_prob": ns.mask_prob, "samples": [], "skipped": 0,
    }
    for suite in args.suites:
        path = Path(args.eval_data_root) / suite
        with path.open(encoding="utf-8") as fh:
            rows = [json.loads(line) for _, line in zip(range(args.limit), fh)]
        for i, row in enumerate(rows):
            ctx = row["context"].encode("utf-8")
            if len(ctx) < args.window_bytes * (args.needle_window + 2):
                report["skipped"] += 1
                continue
            sample = run_sample(model, ns, ctx, args.seed + i, args, device)
            if sample is None:
                report["skipped"] += 1
                continue
            sample["id"] = row.get("id", f"{suite}:{i}")
            sample["suite"] = suite
            report["samples"].append(sample)
            print(f"[paging] {suite} #{i}: {sample['n_pages']} pages, {sample['chunks_total']} chunks", file=sys.stderr, flush=True)
    report["aggregate"] = _aggregate(report["samples"], args.budgets) if report["samples"] else {}
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text, flush=True)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
