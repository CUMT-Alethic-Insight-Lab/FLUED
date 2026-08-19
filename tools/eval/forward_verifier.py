"""fork 2 前向校验器（eval 期组件，2026-08-19；spec
docs/versions/v3.7/FLUED_V3_7_FORK2_MULTIVIEW_READOUT_20260819_CN.md §1.2）。

形态：decoder/检索器给出 top-L 候选 → **复用写入算子重放** ŝ_ℓ =
write(cand_ℓ) → 在测量空间比对 ‖Q·ŝ_ℓ − Q·ŝ_target‖，取最近者。校验器零
新学组件（写入算子已存在），Q = 播种正交帧（免训练，装饰律免疫，E66
教训）。

本文件的冒烟级最小实现（docstring 登记口径）：
- 候选 = 档案馆探针检索器的 top-L key 行对应的**段**；write(cand) = 该段的
  WriteHead 写值 v（K 通道：write_head_k(index_row)；V 通道：write_head
  (memory_row)）——写入算子的直接输出。
- target = 问句末段的写值（问句经同一冻结管线编码，取其末真实段的 index
  行过同一 WriteHead）。比对空间 = 写值空间经播种正交帧投影。
- 全状态范数比对被立项书明确禁用，未实现。

CLI 首测（hit@5→hit@1 兑换率初值，E78 的 0.42→0.17 缺口）：
  python tools/eval/forward_verifier.py --device cuda \
      --run-dir checkpoints/v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818
"""

from __future__ import annotations

import argparse
import heapq
import json
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID, PAD_ID  # noqa: E402

VERIFY_FRAME_SEED = 20260819_1000  # fork 2 verifier frame seed (pinned)
# Completion-pass constants (train_v36.py --verify-topl): bounded eval cost,
# all flag-gated (default off = zero overhead, bit-preserved legacy eval).
VERIFY_FRAME_DIM = 32  # measurement frame rows for the completion pass
VERIFY_MAX_CHUNKS_PER_SAMPLE = 8  # verify at most this many masked chunks per window


def seeded_frame(m: int, dim: int, seed: int = VERIFY_FRAME_SEED) -> torch.Tensor:
    """Seeded orthogonal measurement frame (m, dim) for verification-space
    comparisons. Deterministic under the pinned seed."""
    gen = torch.Generator().manual_seed(seed)
    q, _r = torch.linalg.qr(torch.randn(dim, m, generator=gen))
    return q.T.contiguous()  # (m, dim) orthonormal rows


def verify(candidates: torch.Tensor, target: torch.Tensor, frame: torch.Tensor):
    """Forward verification: pick the candidate nearest to the target in the
    measurement space ||Q c - Q t||. candidates (L, d), target (d,), frame
    (m, d). Returns (best_idx, dists (L,))."""
    proj_c = candidates.float() @ frame.T
    proj_t = target.float() @ frame.T
    dists = (proj_c - proj_t.unsqueeze(0)).norm(dim=-1)
    return int(dists.argmin()), dists


# ---------------------------------------------------------------------------
# completion-form verification (train_v36.py --verify-topl; spec §1.2 闭环的
# 补全路径形态: decoder top-L 段候选 → 写入算子重放 → 测量空间比对)
# ---------------------------------------------------------------------------


def segment_candidates(slot_logprobs: torch.Tensor, topl: int) -> torch.Tensor:
    """Top-L joint byte assignments for one chunk's masked slots. The decoder
    decodes slots in parallel (non-AR), so a segment candidate's score is the
    SUM of per-slot log-probs; best-first search over the sorted per-slot
    choices yields the exact top-L ("beam 即可", spec §1.2). slot_logprobs
    (n_masked, V) -> returns (L, n_masked) byte ids; row 0 = per-slot argmax
    (the greedy candidate)."""
    n, vocab = slot_logprobs.shape
    k = min(topl, vocab)
    scores, orders = slot_logprobs.float().topk(k, dim=-1)  # sorted desc
    scores_l, orders_l = scores.tolist(), orders.tolist()

    def node_score(node: tuple) -> float:
        return sum(scores_l[i][node[i]] for i in range(n))

    start = (0,) * n
    heap = [(-node_score(start), start)]
    visited = {start}
    out = []
    while heap and len(out) < topl:
        _neg, node = heapq.heappop(heap)
        out.append([orders_l[i][node[i]] for i in range(n)])
        for i in range(n):
            if node[i] + 1 < k:
                nxt = node[:i] + (node[i] + 1,) + node[i + 1 :]
                if nxt not in visited:
                    visited.add(nxt)
                    heapq.heappush(heap, (-node_score(nxt), nxt))
    return torch.tensor(out, dtype=torch.long)


def verify_chunk(cand_vals: torch.Tensor, target: torch.Tensor, frame: torch.Tensor, correct: torch.Tensor) -> dict:
    """Per-chunk hit accounting for the completion pass. cand_vals (L, d) are
    the replayed write values of the top-L candidates; target (d,) is the
    chunk's trained state readout (what the chain actually claims the segment
    holds); correct (L,) bool marks candidates whose masked bytes are all the
    clean bytes. The false-peak flag (伪峰): the verifier picked a WRONG
    candidate while a correct one sat in the top-L."""
    best, _dists = verify(cand_vals, target, frame)
    hitl = bool(correct.any())
    return {
        "hit1_before": float(bool(correct[0])),
        "hitl": float(hitl),
        "hit1_after": float(bool(correct[best])),
        "false_peak": float((not bool(correct[best])) and hitl),
    }


@torch.no_grad()
def _replay_write_values(model, source_row: torch.Tensor, fills: list[tuple[torch.Tensor, torch.Tensor]]) -> torch.Tensor:
    """Write-operator replay with a FIXED timetable (spec §1.2 写入算子重放):
    each fill = (byte positions (P,), candidate byte ids (P,)) applied to a
    clone of the masked source row; the batch of completed windows is encoded
    and rebuilt into chunks with the ORIGINAL window's hard_cut (candidate
    bytes only change span CONTENT, never the boundary timetable). Returns
    the WriteHead values (N_fills, C, H, hv)."""
    windows = []
    for pos_t, cand_bytes in fills:
        w = source_row[0].clone()
        w[pos_t] = cand_bytes
        windows.append(w)
    windows = torch.stack(windows)  # (N, T)
    byte_states_c, confidence_c, valid_c, _ = model._encode(windows)
    # original timetable from the masked source row itself
    _bs, confidence_o, valid_o, _ = model._encode(source_row)
    hard_cut_o, _utf8_o, _ = model._cuts(source_row, confidence_o, valid_o)
    utf8_c = windows.ge(129) & windows.le(192) & valid_c  # id space: byte 0x80-0xBF -> id 129-192
    chunks_c = model.chunk_builder(byte_states_c, valid_c, hard_cut_o.expand(windows.size(0), -1), confidence_c)
    chunks_c = model.bridge(chunks_c, byte_states_c, confidence_c, valid_c, utf8_c)
    memory_c, _index_c = model.summarizer.forward_with_index(chunks_c.span_embeddings, chunks_c.token_mask)
    return model.write_head(memory_c)["v"]


@torch.no_grad()
def verify_completion_eval(model, eval_loader, args, device) -> dict:
    """--verify-topl L eval pass (fork 2 §1.2, completion form; eval-time only,
    zero new learned components). Per eval window, per masked chunk:
    1. the completion decoder's per-slot logits give the exact top-L segment
       candidates (segment_candidates; unmasked slots fixed to the source —
       only masked bytes vary);
    2. each candidate is replayed through the frozen write operator with the
       ORIGINAL timetable (masked-source window with the chunk's masked bytes
       filled -> encoder -> summarizer -> WriteHead value);
    3. the target is the chunk's TRAINED state readout (pre-realign flat
       H*hv, torch-reference states — the probe line's口径), and the verifier
       picks the candidate nearest in the seeded-frame measurement space.
    Scope guard: slm + v_row_source='state' grids only (the completion path's
    state channel; the b-grid archive-form verification is this module's CLI).
    fp32, no autocast. Returns eval_verify_* metrics; hitl >= hit1_before
    holds per chunk by construction."""
    if getattr(args, "backbone_mode", "") != "slm" or getattr(args, "v_row_source", "") != "state":
        raise ValueError("--verify-topl requires the slm completion path with v_row_source='state'")
    from tools.train.v3_3.train_v33 import make_byte_mask, make_targets
    from tools.analysis.v3_6.probe_oracle_write_verdict import trained_states

    topl = int(getattr(args, "verify_topl", 0))
    if topl <= 0:
        return {}
    model.eval()
    # reproduce evaluate()'s mask discipline exactly: one reseed, per-batch draws
    torch.manual_seed(args.eval_mask_seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(args.eval_mask_seed)
    sm = model.state_machine
    frame = seeded_frame(VERIFY_FRAME_DIM, model.config.kda_heads * model.config.kda_head_v).to(device)
    rows = []
    for i, batch in enumerate(eval_loader):
        if i >= args.max_eval_batches:
            break
        clean = batch[0].to(device)
        valid = clean.ne(PAD_ID)
        byte_mask = make_byte_mask(valid, args.mask_prob, args.mask_span_min, args.mask_span_max)
        source = clean.masked_fill(byte_mask, MASK_ID)
        for b in range(clean.size(0)):
            src_b, clean_b, bm_b = source[b : b + 1], clean[b : b + 1], byte_mask[b : b + 1]
            out = model(src_b)
            chunks = out.chunks
            n_real = int(chunks.chunk_mask[0].sum())
            targets, _slot_mask, masked_slot = make_targets(
                clean_b, bm_b, chunks.chunk_ids, chunks.offsets, args.max_chunks, args.max_span
            )
            gates = model.write_head(out.memory)
            states = trained_states(sm, gates, n_real)  # (1, n, H, hk, hv) fp32
            q = sm.readout_query.float()
            reads = torch.einsum("qhk,bnhkv->bnqhv", q, states).reshape(1, n_real, q.size(0), -1)
            sel = [j for j in range(n_real) if bool(masked_slot[0, j].any())][:VERIFY_MAX_CHUNKS_PER_SAMPLE]
            # build candidates for every selected chunk first, then ONE batched replay
            per_chunk, fills, fill_index = [], [], {}
            for j in sel:
                slot_idx = masked_slot[0, j].nonzero(as_tuple=True)[0]
                logits = out.logits_backbone[0, j, slot_idx].float().clone()  # (n_m, V)
                logits[..., PAD_ID] = -float("inf")
                if logits.size(-1) > MASK_ID:
                    logits[..., MASK_ID] = -float("inf")
                cands = segment_candidates(logits.log_softmax(dim=-1), topl)  # (L, n_m)
                clean_bytes = targets[0, j, slot_idx].cpu()
                correct = (cands == clean_bytes.unsqueeze(0)).all(dim=1)
                per_chunk.append((j, cands, correct, reads[0, j, 0]))
                pos_t = (bm_b[0] & (chunks.chunk_ids[0] == j)).nonzero(as_tuple=True)[0]
                # map each masked byte position to its row in the candidate
                # matrix (cands rows are indexed by MASKED-SLOT ORDER, not raw
                # slot id): slot id s -> position in slot_idx
                slot_pos = {int(s): p for p, s in enumerate(slot_idx.tolist())}
                row_of_t = torch.tensor([slot_pos[int(s)] for s in chunks.offsets[0, pos_t].tolist()])
                for l in range(cands.size(0)):
                    fill_index[(j, l)] = len(fills)
                    fills.append((pos_t, cands[l][row_of_t].to(device)))
            if not fills:
                continue
            v_all = _replay_write_values(model, src_b, fills)  # (N, C, H, hv)
            for j, cands, correct, target in per_chunk:
                cand_vals = torch.stack(
                    [v_all[fill_index[(j, l)], j].reshape(-1) for l in range(cands.size(0))]
                ).float()
                rows.append(verify_chunk(cand_vals, target, frame, correct.to(device)))
    n = len(rows)
    if n == 0:
        return {
            "eval_verify_hit1_before": 0.0,
            "eval_verify_hit1_after": 0.0,
            "eval_verify_hitl": 0.0,
            "eval_verify_false_peak": 0.0,
            "eval_verify_chunks": 0,
            "eval_verify_topl": topl,
        }
    hitl_sum = sum(r["hitl"] for r in rows)
    return {
        "eval_verify_hit1_before": round(sum(r["hit1_before"] for r in rows) / n, 4),
        "eval_verify_hit1_after": round(sum(r["hit1_after"] for r in rows) / n, 4),
        "eval_verify_hitl": round(hitl_sum / n, 4),
        "eval_verify_false_peak": round(sum(r["false_peak"] for r in rows) / max(hitl_sum, 1.0), 4),
        "eval_verify_chunks": n,
        "eval_verify_topl": topl,
    }


# ---------------------------------------------------------------------------
# CLI first measurement: hit@5 -> hit@1 conversion on the archive probe form
# ---------------------------------------------------------------------------


@torch.no_grad()
def _write_values(model, rows: torch.Tensor, channel: str) -> torch.Tensor:
    """write(cand): the WriteHead's value output for the given store input
    rows (n, d_mem) -> (n, H*hv)."""
    wh = model.write_head_k if channel == "k" else model.write_head
    gates = wh(rows.unsqueeze(0))
    v = gates["v"][0]
    return v.reshape(v.size(0), -1)


@torch.no_grad()
def _query_write_value(model, query: bytes, channel: str, device) -> torch.Tensor:
    """The question through the same frozen pipeline; write value of its last
    real chunk (the entry ID sits at the question tail)."""
    import tools.analysis.v3_6.probe_archive_addressing_v37 as probe

    ids = torch.tensor([b + probe.BYTE_OFFSET for b in query], dtype=torch.long).unsqueeze(0).to(device)
    chunks, memory, index = probe._encode_window(model, ids)
    n_real = int(chunks.chunk_mask[0].sum())
    rows = index if channel == "k" else memory
    return _write_values(model, rows[0, n_real - 1 : n_real], channel)[0]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default="checkpoints/v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818")
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--pages", type=int, default=4)
    p.add_argument("--train-docs", type=int, default=12)
    p.add_argument("--eval-docs", type=int, default=12)
    p.add_argument("--level", type=int, default=64, help="distractor level (E78 gap was at D=64)")
    p.add_argument("--topl", type=int, default=5)
    p.add_argument("--steps", type=int, default=1000, help="retriever training steps")
    p.add_argument("--seed", type=int, default=1042)
    p.add_argument("--out-dir", default="outputs/forward_verifier_20260819")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    import tools.analysis.v3_6.probe_archive_addressing as base
    import tools.analysis.v3_6.probe_archive_addressing_v37 as probe

    run_dir = Path(args.run_dir)
    hay_args = argparse.Namespace(
        data_path="P:/FLUED_corpus/corpus_v3/corpus_v3.txt",
        eval_data_root=str(probe.ph.EVAL_DATA),
        suite="ruler/niah_single_1.jsonl",
    )
    source_name, hay_fn = probe.make_haystack_fn(hay_args)
    model, ns, step = probe.load_model(run_dir, device)
    probe._warm_k_center(model, hay_fn, ns.seq_len, device)  # no-op unless to_k_center
    channel = "k" if ns.k_row_source == "state" else "v"
    print(f"[verifier] model={run_dir.name} step={step} channel={channel} haystack={source_name}", flush=True)

    train_set, eval_set = [], []
    for i in range(args.train_docs):
        enc = probe.build_and_encode(model, ns, ns.seq_len, args.pages, args.level, hay_fn, device, args.seed + i)
        if enc is not None:
            train_set.append(enc)
    for i in range(args.eval_docs):
        enc = probe.build_and_encode(model, ns, ns.seq_len, args.pages, args.level, hay_fn, device, args.seed + 10_000 + args.level * 1_000 + i)
        if enc is not None:
            eval_set.append(enc)
    for enc in train_set + eval_set:
        base.prep_k_index(enc, [1], device)
    k_dim = model.config.d_pack if ns.k_row_source == "state" else model.config.d_mem
    cfg = {"key_type": "full", "rank": None, "gran": 1, "key_src": "memrow", "d_query": k_dim, "d_key": k_dim, "seed": args.seed}
    args_ns = argparse.Namespace(lr=1e-3, steps=args.steps, batch_docs=4, log_every=10**9)
    retr, loss_log = base.train_retriever(cfg, train_set, args_ns, device, args.seed)
    print(f"[verifier] retriever trained loss {loss_log[0]['loss']:.2f}->{loss_log[-1]['loss']:.2f} "
          f"train={len(train_set)} eval={len(eval_set)} ({time.time() - t0:.0f}s)", flush=True)

    frame = seeded_frame(32, model.config.kda_heads * model.config.kda_head_v).to(device)
    rows = []
    for enc in eval_set:
        keys = enc["k_rows"]
        s = retr.scores(enc["query"], keys)
        order = torch.argsort(s.float(), descending=True).tolist()
        pos = set(enc["pos_code"][1].tolist())
        top = order[: args.topl]
        hit_l = float(any(p in pos for p in top))
        hit1_before = float(order[0] in pos)
        # verifier rescore of the top-L candidates by write-replay
        cand_vals = _write_values(model, enc["index_rows"][top].float(), channel)
        tgt = _query_write_value(model, probe._query_bytes(enc["eid"]), channel, device)
        best, dists = verify(cand_vals, tgt, frame)
        hit1_after = float(top[best] in pos)
        rows.append({
            "eid": enc["eid"], "hit1_before": hit1_before, f"hit{args.topl}": hit_l,
            "hit1_after": hit1_after, "picked": top[best],
            "margin": round(float(dists.median() - dists.min()), 4),
        })
    n = len(rows)
    agg = {
        "n_docs": n,
        "hit1_before": round(sum(r["hit1_before"] for r in rows) / n, 4),
        f"hit{args.topl}_before": round(sum(r[f"hit{args.topl}"] for r in rows) / n, 4),
        "hit1_after_verify": round(sum(r["hit1_after"] for r in rows) / n, 4),
        # 伪峰率: verifier picked a WRONG row while the true row was in top-L
        "false_peak_rate": round(
            sum(float(r["hit1_after"] == 0.0 and r[f"hit{args.topl}"] > 0) for r in rows)
            / max(sum(r[f"hit{args.topl}"] for r in rows), 1),
            4,
        ),
    }
    print(f"[verifier] {agg}", flush=True)
    report = {
        "probe": "fork 2 forward verifier first measurement (hit@5 -> hit@1 conversion)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "checkpoint": {"run": run_dir.name, "step": step},
        "params": {"pages": args.pages, "level": args.level, "topl": args.topl, "eval_docs": n, "retriever_steps": args.steps},
        "form": "write-replay: candidates' WriteHead value vectors vs the query's last-chunk write value, "
        "compared under a seeded orthogonal frame (32 x H*hv)",
        "aggregate": agg,
        "docs": rows,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / f"verify_{run_dir.name}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[verifier] report -> {out_path}", flush=True)


if __name__ == "__main__":
    main()
