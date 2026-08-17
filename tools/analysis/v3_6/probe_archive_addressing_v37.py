"""S39 step-0 probe — v3.7 slm adaptation (archive addressing K side x
needle-position fidelity V side) on FROZEN v3.7 checkpoints.

v37 适配版：原预注册设计不动（tools/analysis/v3_6/probe_archive_addressing.py
保持冻结），本文件只替换"被测接口"。与原探针的差异点：

1. **被测对象 = slm store 行**（v3.7 架构共识 §1，用户裁定 2026-08-17）：
   summarizer 直产 index(K)/memory(V) 双通道行；每个 "state" 通道经该 cell
   自己的 WriteHead+KDAStateMachine 逐段加工。keys = 该 cell 的 K 源行——
   k=index：每 chunk 的 index 行（d_mem）；k=state：K 通道状态机每 chunk
   读出 K~（d_pack，state 跨页携带）。一律 gran=1 每 chunk 一行——原探针的
   gran-4/粗粒度臂在 v37 下 N/A（v37 的粗粒度形态本身就是 state 通道）。
2. **Query**：问句过同一冻结管线（不 mask，同原探针的 documented
   approximation），取末位 K 源行——k=index 取最后真实 chunk 的 index 行
   （"末行"），k=state 取 K 通道吃完问句后的读出（"末态"，fresh state，
   问句是独立输入）。a 格没有全局状态，content 通道已退役（共识 §4），
   这是 K 源空间内唯一自洽的问句压缩形式。
3. **V 侧解码路径**：零训练，走该 cell 自己的 v3.7 decoder 条件（共识
   §1.4 三任务同一套 V）：direct = decoder_in_mem(memory 行)/decoder_in(Ṽ
   状态行) + 页内 chunk 位置嵌入；backbone = SLM 补全行 + 位置（页内因果，
   即训练形态）。取代原探针的 coarse paged/direct_fine 臂（paged 读出与
   s22/s36 双 checkpoint 结构在 slm 下均 N/A）。
4. **state 跨页携带对两侧同时成立**：一份携带态档案馆编码同时服务 K/V
   两侧（原探针 V 侧用 fresh-state 单页口径——那是 s22/s36 单窗训练形态
   的上限判读；v37 四格同为单窗训练，但本探针按 v37 版设计统一取携带态
   档案馆形态。单窗 trained、多页携带 ⇒ 第 2 页起的 state 行是
   out-of-training-distribution，判读时须带此限定）。
5. **needle 模板**：英文 7 位数字（"Archive entry QX-####: the special
   magic number is: #######."），干扰项同模板不同 ID/code，档位
   {4,16,64}；haystack 默认 corpus_v3.txt。正例 = 覆盖 needle 数字段的
   key 行（entry 级为诊断），与原口径同构。
6. **单 checkpoint 运行**：K/V 两侧测同一 cell；跨 cell（a/b/c/d）横向比
   在各份 report 之间进行（命令行见文件尾 usage）。

V 侧双臂同一性核查（2026-08-17 取证，结论：非 bug，口径不变）：
实跑后曾报"direct 与 backbone 臂 byte_acc 逐位相同"。取证脚本
outputs/s39_addressing_probe_v37_20260817/cond_sensitivity_forensics.py
（结果 cond_sensitivity_a_grid.json，a 格 20k checkpoint，CPU）：
(a) needle chunk 的 cond 清零 → 数字 byte_acc 0.71/0.57 → **0.00**，且与
base 预测的逐位一致率 0.00；(b) cond 跨 doc 置换（同 (页,chunk) 位、同位
置嵌入、内容错误）→ byte_acc **0.00**；(c) 两臂 cond 行 cosine ≈0.955–0.969。
结论：该 decode 形态 100% 由 cond 决定——GlobalSpanDecoder 是并行段解码，
只见 cond 行 + chunk 有效槽位 mask，**从不接触任何 byte 上下文**（训练侧
direct/补全任务同形，make_targets 全槽位 CE、无 teacher forcing），因此
不存在"模板上下文可见主导预测"的泄漏通道，也无需再 mask 模板尾。两臂
数字接近的根因是几何的：共享 decoder + 共享重建目标 + 同一 V 源 ⇒ 两个
cond 被训到近平行（cos~0.96），余弦读出下 argmax 只在边际字节上分叉——
full 报告每格 36 docs 中 8–16 个 per-doc byte_acc 不同、arm 级差 ≤3pp，
这正是"同目标训练相关"而非接线别名（别名会使 per-doc 差异为 0/36）。
因此 V 侧维持原 decode 口径，不做 mask 改造。

复用（import 自原探针与 harness，未改一字）：base.load_model（hard-freeze
+ eval + CPU 强制 torch KDA）、base.Retriever / train_retriever /
eval_retriever / prep_k_index / positive_keys——为此 enc["memory"] 别名指向
K 源行（extract_keys("memrow") 的机械适配；k=state 格该行实为状态读出，
不是 pre-state summarizer 行，别名仅为复用，见 encode_document 注释）；
ph._slice_gates / ph._snap_utf8；s1.make_mixed_mask（P0 mixed mask 协议，
条目含 needle 与干扰项一律 force-unmask，E23 扩展到硬负例）。

Honesty notes（与原探针一致）：fp32，无 autocast；batch-1 流式编码；
checkpoint 只读且全参数 requires_grad_(False)（W_q 是探针私有，唯一被训）；
CE/softmax/normalize 一律 .float() 后计算（fp16 entropy/log 坑）；chunk 位置
嵌入保持页内（harness 约定）；任一页面截断 chunk 或 needle 数字缺合法
(chunk, slot) 的 doc 直接重采样。

Usage:
  smoke (CPU, a 格): py -3.14 -X utf8 tools/analysis/v3_6/probe_archive_addressing_v37.py \
      --smoke --device cpu --run-dir checkpoints/_smoke_v37_a_20260817
  full  (单 cell):   python tools/analysis/v3_6/probe_archive_addressing_v37.py \
      --run-dir checkpoints/v37_a_im_v371_20k_ctx4096_20260817
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
from flued.v36.model import chunk_byte_offsets  # noqa: E402
import tools.analysis.v3_6.probe_archive_addressing as base  # noqa: E402
import tools.eval.paging_harness as ph  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402

BYTE_OFFSET = base.BYTE_OFFSET  # data.py PAD-offset convention: byte b -> id b+1, PAD=0
CODE_DIGITS = 7  # v37 needle: 7 ASCII digits (原探针中文模板为 6 位)


def _entry_bytes(eid: str, code: str) -> tuple[bytes, bytes, bytes]:
    """(prefix, code, suffix): code byte span = prefix..prefix+len(code)."""
    return (
        f"Archive entry {eid}: the special magic number is: ".encode("ascii"),
        code.encode("ascii"),
        b".",
    )


def _query_bytes(eid: str) -> bytes:
    return f"What is the special magic number of archive entry {eid}?".encode("ascii")


# ---------------------------------------------------------------------------
# model loading / haystack source
# ---------------------------------------------------------------------------


def load_model(run_dir: Path, device: torch.device):
    """v37: only slm checkpoints are probed (base.load_model hard-freezes all
    parameters, sets eval, and forces the torch KDA impl off-GPU)."""
    return base.load_model(run_dir, device, ("slm",))


def make_haystack_fn(args):
    """corpus_v3.txt slice reader (v37 训练语料); missing -> the xattn probe's
    RULER jsonl fallback verbatim."""
    path = Path(args.data_path)
    if path.is_file():
        size = path.stat().st_size

        def read_corpus(nbytes: int, rng: random.Random) -> bytes:
            raw = b""
            with path.open("rb") as fh:
                for _ in range(8):
                    fh.seek(rng.randrange(0, max(1, size - nbytes - 1)))
                    raw = fh.read(nbytes)
                    raw = raw[ph._snap_utf8(raw, 0) :]
                    if len(raw) >= nbytes // 2:
                        break
            return raw

        return f"corpus:{path.name}", read_corpus

    blob_path = Path(args.eval_data_root) / args.suite
    with blob_path.open(encoding="utf-8") as fh:
        blob = "\n\n".join(json.loads(line)["context"] for line in fh).encode("utf-8")

    def read_blob(nbytes: int, rng: random.Random) -> bytes:
        off = rng.randrange(0, max(1, len(blob) - nbytes - 1))
        return blob[off : off + nbytes]

    return f"ruler_fallback:{args.suite}", read_blob


# ---------------------------------------------------------------------------
# document construction: 1 needle + n_distr same-template entries spliced at
# uniform random positions (UTF-8 snapped, non-overlapping) — same algorithm
# as the frozen probe, v37 English template
# ---------------------------------------------------------------------------


def build_document(base_text: bytes, n_distr: int, rng: random.Random):
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
    base_text = base_text[: max(0, len(base_text) - total)]
    while base_text and (base_text[-1] & 0xC0) == 0x80:  # snap the tail to a char boundary
        base_text = base_text[:-1]
    margin = max(len(pre) + len(code_b) + len(suf) for pre, code_b, suf in (e["parts"] for e in entries)) + 8
    if len(base_text) <= margin * (len(entries) + 1):
        return None
    # insertion points with min separation `margin` so entries never share a chunk
    points = []
    for _ in range(len(entries)):
        for _try in range(64):
            cand = rng.randrange(0, len(base_text) - margin)
            if all(abs(cand - q) >= margin for q in points):
                points.append(cand)
                break
        else:
            return None
    points.sort()
    doc = b""
    prev = 0
    for e, p in zip(entries, points):
        p = max(ph._snap_utf8(base_text, p), prev)
        pre, code_b, suf = e["parts"]
        doc += base_text[prev:p] + pre
        e["code_lo"] = len(doc)
        doc += code_b + suf
        e["code_hi"] = e["code_lo"] + len(code_b)
        e["lo"] = e["code_lo"] - len(pre)
        e["hi"] = len(doc)
        prev = p
        del e["parts"]
    doc += base_text[prev:]
    return doc, entries


# ---------------------------------------------------------------------------
# frozen v37 streaming encode: per page -> (memory, index) rows -> per-channel
# direct passthrough or carried-state KDA streaming
# ---------------------------------------------------------------------------


@torch.no_grad()
def _encode_window(model, source: torch.Tensor):
    """v37 page encode: front end + chunking + the summarizer's TWO heads
    (memory = V 标准行, index = K 行; 共识 §1.1). ph._encode_window 的 v37 版
    （原版调 model.write_head，a 格没有 state machine，会断）。"""
    byte_states, confidence, valid, _ = model._encode(source)
    hard_cut, utf8_cont, _ = model._cuts(source, confidence, valid)
    chunks = model.chunk_builder(byte_states, valid, hard_cut, confidence)
    chunks = model.bridge(chunks, byte_states, confidence, valid, utf8_cont)
    memory, index = model.summarizer.forward_with_index(chunks.span_embeddings, chunks.token_mask)
    return chunks, memory, index


@torch.no_grad()
def _stream_channel(sm, gates: dict, width: int, n_real: int, state: torch.Tensor):
    """Carried-state streaming of ONE channel over one page (ph._stream_window
    with the state machine passed explicitly: v37 has one WriteHead+KDA pair
    per ENGAGED state channel — state_machine_k eats the index rows,
    state_machine eats the memory rows). Returns rows (1, n_real, d_pack) and
    the carried state."""
    cols = []
    for i in range(n_real):
        package_i, state = sm.stream_step(ph._slice_gates(gates, i, width), state)
        cols.append(package_i[:, 0].mean(dim=1))  # (1, d_pack), nq-mean like the batched path
    return torch.stack(cols, dim=1), state


@torch.no_grad()
def encode_query(model, query: bytes, device: torch.device) -> torch.Tensor:
    """The question compressed by the SAME frozen pipeline, in the K source's
    own space: k=index -> the last real chunk's index row (d_mem, "末行");
    k=state -> the K channel's readout after the final chunk (d_pack, "末态",
    fresh state — the query is a standalone input). Encoded UNMASKED (same
    documented approximation as the frozen probe)."""
    ids = torch.tensor([b + BYTE_OFFSET for b in query], dtype=torch.long).unsqueeze(0).to(device)
    chunks, _memory, index = _encode_window(model, ids)
    n_real = int(chunks.chunk_mask[0].sum())
    if model.config.k_row_source == "state":
        gates = model.write_head_k(index)
        state = model.state_machine_k.init_stream_state(1, device)
        rows, _ = _stream_channel(model.state_machine_k, gates, index.size(1), n_real, state)
        return rows[0, -1]  # (d_pack,)
    return index[0, n_real - 1]  # (d_mem,)


@torch.no_grad()
def encode_document(model, ns, doc: bytes, entries: list, window: int, device: torch.device, mask_seed: int):
    """One archive = n_pages pages through the frozen pipeline. State channels
    carry their KDA state ACROSS pages (the archive IS the multi-page
    carried-state stream — both K and V sides read this one encoding, v37
    ruling; see the module docstring diff 4). Direct channels are stateless
    per chunk. Also runs the page-local SLM backbone (the trained completion
    form) so the V side can decode through it."""
    n_pages = len(doc) // window
    if n_pages < 2:
        return None
    doc = doc[: n_pages * window]
    cfg = model.config
    k_state = cfg.k_row_source == "state"
    v_state = cfg.v_row_source == "state"
    state_k = model.state_machine_k.init_stream_state(1, device) if k_state else None
    state_v = model.state_machine.init_stream_state(1, device) if v_state else None
    k_cols, v_cols, bb_cols, metas = [], [], [], {}
    chunk_offset = 0
    for w in range(n_pages):
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
        chunks, memory, index = _encode_window(model, source)
        n_real = int(chunks.chunk_mask[0].sum())
        if n_real < 2 or int(chunks.pack_info["truncated_tokens"].sum()) > 0:
            return None
        width = memory.size(1)
        if k_state:
            k_rows_w, state_k = _stream_channel(model.state_machine_k, model.write_head_k(index), width, n_real, state_k)
        else:
            k_rows_w = index[:, :n_real]
        if v_state:
            v_rows_w, state_v = _stream_channel(model.state_machine, model.write_head(memory), width, n_real, state_v)
        else:
            v_rows_w = memory[:, :n_real]
        # SLM completion rows, page-local causal — the trained regime
        # (_forward_slm runs the backbone over one window's store)
        pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_real]
        cbo = chunk_byte_offsets(chunks.token_mask[:, :n_real]) if getattr(cfg, "k_pos_inject", False) else None
        bb_w = model.backbone(k_rows_w, v_rows_w, chunks.chunk_mask[:, :n_real], pos, chunk_byte_off=cbo)
        k_cols.append(k_rows_w[0].to(torch.bfloat16))  # (n_real, d_mem|d_pack)
        v_cols.append(v_rows_w[0].to(torch.bfloat16))
        bb_cols.append(bb_w[0].to(torch.bfloat16))  # (n_real, d_backbone)
        if touched:
            metas[w] = {
                "offset": chunk_offset,
                "n_real": n_real,
                "chunk_ids": chunks.chunk_ids[0].cpu(),
                "offsets": chunks.offsets[0].cpu(),
                "tm": chunks.token_mask[0, :n_real].cpu(),
            }
        chunk_offset += n_real

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
    k_rows = torch.cat(k_cols, dim=0)  # (G, d_k) bf16, device
    enc = {
        "k_rows": k_rows,
        "v_rows": torch.cat(v_cols, dim=0),  # (G, d_v) bf16
        "backbone": torch.cat(bb_cols, dim=0),  # (G, d_backbone) bf16
        # ALIAS: the frozen probe's train/eval loops read per-chunk keys via
        # extract_keys(key_src="memrow") -> enc["memory"]; pointing it at the K
        # source rows reuses those loops verbatim. For k=state cells these rows
        # are state readouts (NOT pre-state summarizer rows) — the alias is
        # purely mechanical.
        "memory": k_rows,
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
        "query": encode_query(model, _query_bytes(needle["eid"]), device).to(torch.bfloat16),
    }
    return enc


# ---------------------------------------------------------------------------
# V side: decode the needle code span through the cell's own decoder paths
# ---------------------------------------------------------------------------


@torch.no_grad()
def _decode_units(model, enc, cond_fn, device: torch.device) -> tuple[int, int]:
    """cond_fn(w, j) -> (1, 1, d_backbone) conditioning row for page w chunk j.
    (base._decode_units with an explicit device — the v37 enc dict carries no
    'content' key.)"""
    correct, total = 0, 0
    by_chunk: dict[tuple[int, int], list] = {}
    for w, j, slot, tgt in enc["code_units"]:
        by_chunk.setdefault((w, j), []).append((slot, tgt))
    for (w, j), units in by_chunk.items():
        tm = enc["metas"][w]["tm"][j : j + 1].unsqueeze(0).to(device)
        logits = model.decoder(cond_fn(w, j), tm)
        pred = logits[0, 0].argmax(dim=-1)
        for slot, tgt in units:
            correct += int(int(pred[slot]) == tgt)
            total += 1
    return correct, total


@torch.no_grad()
def v_side_doc(model, enc, device: torch.device) -> dict:
    """Zero-training needle code-span decode (共识 §1.4: direct conditions on
    the V source rows — decoder_in_mem for v=memory, decoder_in for v=state;
    completion reads the SLM backbone output). Page-local chunk positions, the
    harness convention."""
    dec_in = model.decoder_in if model.config.v_row_source == "state" else model.decoder_in_mem

    def direct_cond(w, j):
        m = enc["metas"][w]
        g = m["offset"] + j
        return dec_in(enc["v_rows"][g : g + 1].float().unsqueeze(0)) + model.chunk_pos.weight[j : j + 1].unsqueeze(0)

    def backbone_cond(w, j):
        m = enc["metas"][w]
        g = m["offset"] + j
        return enc["backbone"][g : g + 1].float().unsqueeze(0) + model.chunk_pos.weight[j : j + 1].unsqueeze(0)

    out = {}
    for arm, fn in (("direct", direct_cond), ("backbone", backbone_cond)):
        correct, total = _decode_units(model, enc, fn, device)
        out[arm] = {"exact": float(correct == total and total > 0), "byte_acc": round(correct / max(total, 1), 4), "n_bytes": total}
    return out


# ---------------------------------------------------------------------------
# orchestration
# ---------------------------------------------------------------------------


def build_and_encode(model, ns, window, pages, n_distr, hay_fn, device, seed, max_tries=4):
    rng = random.Random(seed)
    for _ in range(max_tries):
        raw = hay_fn(window * pages + (1 << 16), rng)
        # bound the haystack to the requested doc length: build_document only
        # shaves off the entry bytes, so the input must already be ~window*pages
        built = build_document(raw[: window * pages], n_distr, rng)
        if built is None:
            continue
        doc, entries = built
        enc = encode_document(model, ns, doc, entries, window, device, rng.randrange(1 << 30))
        if enc is not None:
            enc["n_distr"] = n_distr
            return enc
    return None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--smoke", action="store_true", help="small fast mechanism check (2 pages, tiny pools)")
    p.add_argument("--side", choices=["both", "k", "v"], default="both")
    p.add_argument("--run-dir", default="checkpoints/v37_a_im_v371_20k_ctx4096_20260817",
                   help="one v37 cell per run; cross-cell comparison is across reports")
    p.add_argument("--data-path", default="P:/FLUED_corpus/corpus_v3/corpus_v3.txt")
    p.add_argument("--eval-data-root", default=str(ph.EVAL_DATA))
    p.add_argument("--suite", default="ruler/niah_single_1.jsonl", help="fallback haystack jsonl under eval-data-root")
    p.add_argument("--out-dir", default="outputs/s39_addressing_probe_v37_20260817")
    p.add_argument("--pages", type=int, default=0, help="pages per doc at the checkpoint's seq_len; 0 = 2 smoke / 4 full")
    p.add_argument("--train-docs", type=int, default=0, help="0 = 6 smoke / 48 full")
    p.add_argument("--eval-docs", type=int, default=0, help="per distractor level; 0 = 2 smoke / 12 full")
    p.add_argument("--steps", type=int, default=0, help="retriever steps; 0 = 100 smoke / 3000 full")
    p.add_argument("--batch-docs", type=int, default=4)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--levels", default="", help="distractor counts, comma-separated; empty = 4 smoke / 4,16,64 full")
    p.add_argument("--log-every", type=int, default=100)
    p.add_argument("--seed", type=int, default=1042)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--report-name", default="", help="report filename under out-dir (default: report[_smoke]_<run>.json)")
    args = p.parse_args()
    mode = "smoke" if args.smoke else "full"
    pages = args.pages or (2 if args.smoke else 4)
    n_train = args.train_docs or (6 if args.smoke else 48)
    n_eval = args.eval_docs or (2 if args.smoke else 12)
    args.steps = args.steps or (100 if args.smoke else 3000)
    levels = [int(x) for x in args.levels.split(",")] if args.levels else ([4] if args.smoke else [4, 16, 64])
    granularities = [1]  # v37 keys are per-chunk rows by construction

    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    timing: dict[str, float] = {}
    t_start = time.time()

    run_dir = Path(args.run_dir)
    source_name, hay_fn = make_haystack_fn(args)
    print(f"[probe] mode={mode} device={device.type} haystack={source_name} pages={pages} levels={levels}", flush=True)

    model, ns, step = load_model(run_dir, device)
    grid = f"k={ns.k_row_source},v={ns.v_row_source},seed={getattr(ns, 'seed_source', 'v')}"
    print(f"[probe] model={run_dir.name} step={step} seq_len={ns.seq_len} grid=({grid})", flush=True)

    # ---- encode doc pools (one carried-state archive per doc) ----
    t0 = time.time()
    train_set, eval_sets = [], {}
    if args.side in ("both", "k"):
        for i in range(n_train):
            enc = build_and_encode(model, ns, ns.seq_len, pages, levels[i % len(levels)], hay_fn, device, args.seed + i)
            if enc is not None:
                train_set.append(enc)
            if (i + 1) % max(1, n_train // 4) == 0:
                print(f"[probe] train docs {len(train_set)}/{i + 1} ({time.time() - t0:.0f}s)", flush=True)
    for L in levels:
        eval_sets[L] = []
        for i in range(n_eval):
            enc = build_and_encode(model, ns, ns.seq_len, pages, L, hay_fn, device, args.seed + 10_000 + L * 1_000 + i)
            if enc is not None:
                eval_sets[L].append(enc)
        print(f"[probe] eval docs D={L}: {len(eval_sets[L])}/{n_eval} ({time.time() - t0:.0f}s)", flush=True)
    all_encs = train_set + [e for docs in eval_sets.values() for e in docs]
    for enc in all_encs:
        base.prep_k_index(enc, granularities, device)
    if args.side in ("both", "k") and (len(train_set) < args.batch_docs or any(not eval_sets[L] for L in levels)):
        counts = {L: len(eval_sets[L]) for L in levels}
        raise RuntimeError(f"doc pool too small: train={len(train_set)} eval={counts} — check the haystack source")
    timing["encode_sec"] = round(time.time() - t0, 1)

    # ---- K side: train the probe-private W_q, eval top-1/3/5 ----
    k_results = []
    if args.side in ("both", "k"):
        t0 = time.time()
        k_dim = model.config.d_pack if ns.k_row_source == "state" else model.config.d_mem
        cfg = {"key_type": "full", "rank": None, "gran": 1, "key_src": "memrow",  # "memrow" -> enc["memory"] alias
               "d_query": k_dim, "d_key": k_dim, "seed": args.seed}
        retr, loss_log = base.train_retriever(cfg, train_set, args, device, args.seed)
        row = {
            "key_type": cfg["key_type"],
            "key_src": f"k_rows({ns.k_row_source})",
            "granularity": 1,
            "train_loss_first": loss_log[0]["loss"],
            "train_loss_last": loss_log[-1]["loss"],
            "loss_log": loss_log,
            "levels": {str(L): base.eval_retriever(retr, eval_sets[L], cfg) for L in levels},
        }
        k_results.append(row)
        brief = " | ".join(
            f"D={L} hit@1/3/5={row['levels'][str(L)]['hit1']:.2f}/{row['levels'][str(L)]['hit3']:.2f}/{row['levels'][str(L)]['hit5']:.2f}(rand {row['levels'][str(L)]['rand1']:.3f})"
            for L in levels
        )
        print(f"[K][{row['key_src']}/g1] loss {row['train_loss_first']:.2f}->{row['train_loss_last']:.2f} {brief}", flush=True)
        timing["k_side_sec"] = round(time.time() - t0, 1)

    # ---- V side: needle code-span decode, direct + SLM-backbone arms ----
    v_results: dict[str, dict] = {}
    if args.side in ("both", "v"):
        t0 = time.time()
        for L in levels:
            rows = []
            for enc in eval_sets[L]:
                rows.append({"eid": enc["eid"], **v_side_doc(model, enc, device)})
            arms = {}
            for arm in ("direct", "backbone"):
                n = len(rows)
                arms[arm] = {
                    "exact": round(sum(r[arm]["exact"] for r in rows) / max(n, 1), 4),
                    "byte_acc": round(sum(r[arm]["byte_acc"] for r in rows) / max(n, 1), 4),
                    "n_docs": n,
                    "n_bytes": sum(r[arm]["n_bytes"] for r in rows),
                }
            v_results[str(L)] = {"arms": arms, "docs": rows}
            print(
                f"[V][D={L}] direct exact={arms['direct']['exact']:.2f} byte={arms['direct']['byte_acc']:.2f} | "
                f"backbone exact={arms['backbone']['exact']:.2f} byte={arms['backbone']['byte_acc']:.2f}",
                flush=True,
            )
        timing["v_side_sec"] = round(time.time() - t0, 1)
        if device.type == "cuda":
            torch.cuda.empty_cache()
    timing["total_sec"] = round(time.time() - t_start, 1)

    report = {
        "probe": "S39 step-0 archive addressing/fidelity — v3.7 slm adaptation",
        "mode": mode,
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data_source": source_name,
        "checkpoints": {"cell": {"run": run_dir.name, "step": step, "grid": grid}},
        "params": {
            "pages": pages, "train_docs": len(train_set), "eval_docs_per_level": {str(L): len(eval_sets[L]) for L in levels},
            "steps": args.steps, "batch_docs": args.batch_docs, "lr": args.lr, "levels": levels,
            "granularities": granularities, "seed": args.seed,
        },
        "protocol": {
            "entry": "Archive entry QX-####: the special magic number is: #######.",
            "query": "What is the special magic number of archive entry QX-####?",
            "positives": "key rows covering the needle CODE digits (hit*_entry = entry-level diagnostic)",
            "key_row": "per-chunk K source row (k=index: summarizer index row, d_mem; k=state: K-channel "
            "carried-state readout K~, d_pack); gran=1 only",
            "query_form": "last real chunk's K source row of the unmasked question (末行 / K 通道末态)",
            "v_arms": "direct = decoder_in_mem/decoder_in(V row) + page-local chunk pos; backbone = SLM "
            "completion row + pos (page-local causal, the trained form)",
            "mask": "P0 mixed mask; needle AND distractor entries force-unmasked (E23)",
            "state": "state channels carried ACROSS pages for BOTH sides (one archive encoding; v37 ruling — "
            "pages 2+ of state channels are out of the single-window training distribution)",
            "freeze": "checkpoint read-only, all params requires_grad_(False); W_q is probe-private",
        },
        "k_side": k_results,
        "v_side": v_results,
        "timing_sec": timing,
    }
    default_name = f"report{'_smoke' if args.smoke else ''}_{run_dir.name}.json"
    out_path = out_dir / (args.report_name or default_name)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[probe] report -> {out_path} (total {timing['total_sec']}s)", flush=True)


if __name__ == "__main__":
    main()
