"""招募臂逐条目 Δ 仪表（Q11 预注册 §3/§5，2026-08-22，零训练纯评测）。

逐条目 Δ = acc（答案｜来源段在状态中完好） − acc（答案｜来源段置乱）。
四臂（同窗同 splice 同 mask 同计分器，eval 流 48 窗，逐条目全量记录）：

  A 完好+剔除：来源段原样，档 a store_block 剔除（r=1.0 语义）——Δ 主臂；
  B 置乱+剔除：来源段字符级置乱（UTF-8 整字符排列，字节长不变，spans 不变）
    ——Δ 的减数（先验：纯猜条目置乱前后不变，Δ≈0）；
  C 完好+不剔除：V 旁路完好基线——有效性门（基线−先验 ≥0.10 且 p<0.01，
    不满足则任务理解层失败，臂作废重跑不许判负）；
  D 遮蔽+剔除：来源段全程遮蔽（MASK_ID）——裸猜先验分布，仅描述性。

判读（预注册）：Δ = A−B 均值 + 95% CI（逐条目差）；Δ>0（CI 不含 0）→
招募点燃（c 主臂非零）；CI 含 0 → 判死路径（转 ASCII 对照臂复测）。
有效性门不过 → 判词作废。判读矩阵的 B 臂（位置先验键）判决另格。

计分：echo 槽位 byte_acc + 归一化 exact（大小写折叠/全词命中，cloze 同
schema）；逐条目记录 answer/位置/窗号（终考修订 1 纪律）。

Usage:
  python tools/analysis/v3_6/probe_retrieval_delta.py --device cuda --run-dir checkpoints/v37ks_b_sm_retrieval_cjk_20k_ctx4096_20260822
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_retrieval_delta.py --device cpu --max-windows 4
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    load_model,
)

DEFAULT_RUN = "checkpoints/v37ks_b_sm_retrieval_cjk_20k_ctx4096_20260822"
OUT_DIR = "outputs/retrieval_delta_20260822"
SPLICE_SEED = 20260822
GATE_MARGIN = 0.10  # 有效性门（预注册）


def _char_shuffle(frag: bytes, gen: torch.Generator) -> bytes:
    """UTF-8 char-level permutation, byte-level split (no decode): length and
    char boundaries preserved exactly — only the character ORDER is destroyed."""
    chunks: list[bytes] = []
    i = 0
    while i < len(frag):
        lead = frag[i]
        size = 1 if lead < 0x80 else (2 if lead < 0xE0 else (3 if lead < 0xF0 else 4))
        chunks.append(frag[i : i + size])
        i += size
    perm = torch.randperm(len(chunks), generator=gen).tolist()
    return b"".join(chunks[j] for j in perm)


@torch.no_grad()
def run_arm(model, ids, metas, arm: str, device, mask_seed: int):
    """One arm over one spliced window: forward (with/without store_block),
    score echo byte_acc + exact. arm in {A, B, C, D} (see module docstring).
    mask_seed is per-window and SHARED by all four arms (same mask per window)."""
    gen = torch.Generator().manual_seed(SPLICE_SEED + 1)
    ids = ids.clone()
    if arm == "B" and metas is not None:
        lo, hi = metas["source_span"]
        frag = bytes(int(x) - 1 for x in ids[lo:hi].tolist())  # PAD-offset: byte = id-1
        shuffled = _char_shuffle(frag, gen)
        ids[lo:hi] = torch.tensor([b + 1 for b in shuffled], dtype=ids.dtype)
    ids = ids.unsqueeze(0).to(device)
    byte_mask = s1.make_mixed_mask(
        ids.cpu(), 0.05, char_frac=0.4, char_span_max=3,
        tokenizer=s1._BPE_TOKENIZER, generator=torch.Generator().manual_seed(mask_seed),
    ).to(device)
    byte_mask = s1._retrieval_mask_overrides(byte_mask, [metas])
    if arm == "D" and metas is not None:
        lo, hi = metas["source_span"]
        byte_mask[0, lo:hi] = True  # 来源段全程遮蔽（盖过答案词的 unmask 覆写）
    source = ids.masked_fill(byte_mask, MASK_ID)
    store_block = None
    if arm in ("A", "B", "D"):
        chunks, _m, _i = _front_end(model, source)
        block, _rate = s1._retrieval_store_block([metas], chunks, 1.0, torch.Generator().manual_seed(SPLICE_SEED + 2))
        store_block = block
    out = model(source, store_block=store_block)
    chunks = out.chunks
    slot, active = s1._cloze_slot_grid([metas], chunks.chunk_ids, chunks.offsets, model.config.max_chunks, model.config.max_span)
    if not bool(active[0]):
        return None  # echo truncated out of the grid: item inactive
    targets, _sm, _m2 = s1.make_targets(
        ids, torch.zeros_like(byte_mask), chunks.chunk_ids, chunks.offsets,
        model.config.max_chunks, model.config.max_span,
    )
    pred = out.logits_backbone.argmax(dim=-1)
    echo = slot[0]
    hits = (pred[0][echo] == targets[0][echo])
    byte_acc = float(hits.float().mean()) if int(echo.sum()) else 0.0
    exact = bool(hits.all()) and int(echo.sum()) > 0
    return {"byte_acc": byte_acc, "exact": exact, "n_echo": int(echo.sum())}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=DEFAULT_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=48)
    p.add_argument("--out-dir", default=OUT_DIR)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, step = load_model(Path(args.run_dir), device)
    if s1._BPE_TOKENIZER is None:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    windows = build_eval_windows(ns, args.max_windows * 2)  # oversample: inactive rows skipped
    print(f"[delta] model={Path(args.run_dir).name} step={step} device={device.type} ({time.time() - t0:.0f}s)", flush=True)

    gen = torch.Generator().manual_seed(SPLICE_SEED)
    items = []
    for wi, clean in enumerate(windows):
        if len(items) >= args.max_windows:
            break
        spliced, metas = s1._splice_retrieval(clean, 1.0, gen, getattr(ns, "retrieval_answer_mode", "cjk"))
        m = metas[0]
        if m is None:
            continue
        ids = spliced[0]
        rec = {"window": wi, "answer": m["answer_b"].decode("utf-8", errors="replace"),
               "source_span": list(m["source_span"]), "query_start": m["query_start"]}
        skip = False
        for arm in ("A", "B", "C", "D"):
            r = run_arm(model, ids, m, arm, device, 1042 + wi)
            if r is None:
                skip = True
                break
            rec[arm] = r
        if skip:
            continue
        rec["delta"] = round(rec["A"]["byte_acc"] - rec["B"]["byte_acc"], 4)
        items.append(rec)
        if len(items) % 8 == 0:
            print(f"[delta] items {len(items)}/{args.max_windows} ({time.time() - t0:.0f}s)", flush=True)

    n = len(items)
    mean = lambda arm, k: sum(r[arm][k] for r in items) / max(n, 1)
    acc = {arm: round(mean(arm, "byte_acc"), 4) for arm in ("A", "B", "C", "D")}
    exact = {arm: round(sum(1 for r in items if r[arm]["exact"]) / max(n, 1), 4) for arm in ("A", "B", "C", "D")}
    deltas = [r["delta"] for r in items]
    delta_mean = sum(deltas) / max(n, 1)
    sd = (sum((d - delta_mean) ** 2 for d in deltas) / max(n - 1, 1)) ** 0.5 if n > 1 else 0.0
    ci = 1.96 * sd / (n ** 0.5) if n else 0.0
    gate_diff = acc["C"] - acc["B"]
    # 二项检验（有效性门）：C 的 exact 命中数对 B（同 n 两比率正态近似 z）
    ec = sum(1 for r in items if r["C"]["exact"])
    eb = sum(1 for r in items if r["B"]["exact"])
    p_pool = (ec + eb) / max(2 * n, 1)
    z = (ec / max(n, 1) - eb / max(n, 1)) / max((p_pool * (1 - p_pool) * 2 / max(n, 1)) ** 0.5, 1e-9)
    p_binom = 0.5 * math.erfc(z / math.sqrt(2))
    gate_ok = gate_diff >= GATE_MARGIN and p_binom < 0.01

    if not gate_ok:
        verdict = (f"有效性门未过：完好旁路基线−先验 = {gate_diff:.4f} < {GATE_MARGIN} 或 p={p_binom:.4f} ≥ 0.01"
                   "——任务理解层失败，臂作废重跑（不许判负）。")
    elif delta_mean > 0 and (delta_mean - ci) > 0:
        verdict = (f"招募点燃：逐条目 Δ = {delta_mean:.4f} ± {ci:.4f}（95% CI 不含 0，n={n}）——"
                   "c 主臂（CJK）Δ 非零，K 通道在自然检索形态下被招募。")
    else:
        verdict = (f"Δ = {delta_mean:.4f} ± {ci:.4f}（CI 含 0，n={n}）——c 主臂判零路径，"
                   "转 ASCII 对照臂复测（两臂皆零才引用结构性判词）。")

    report = {
        "probe": "招募臂逐条目 Δ 仪表（Q11 预注册 §3/§5）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": Path(args.run_dir).name, "step": step},
        "params": {"n_items": n, "splice_seed": SPLICE_SEED, "answer_mode": getattr(ns, "retrieval_answer_mode", "cjk")},
        "arms": {"A": "完好+剔除（Δ 主臂）", "B": "置乱+剔除（Δ 减数/先验）",
                 "C": "完好+不剔除（有效性门基线）", "D": "全程遮蔽+剔除（裸猜先验，描述性）"},
        "byte_acc": acc, "exact": exact,
        "delta": {"mean": round(delta_mean, 4), "ci95": round(ci, 4)},
        "validity_gate": {"C_minus_B": round(gate_diff, 4), "margin": GATE_MARGIN,
                          "p_binom_exact": round(p_binom, 6), "ok": gate_ok},
        "verdict": verdict,
        "items": items,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "retrieval_delta.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "招募臂逐条目 Δ 仪表（Q11 v2，c 主臂 CJK 小片段）",
        f"日期 {report['created']}  设备 {device.type}  n={n}  checkpoint={Path(args.run_dir).name}",
        "",
        f"byte_acc：A 完好+剔除 {acc['A']:.4f} | B 置乱+剔除 {acc['B']:.4f} | C 完好+不剔 {acc['C']:.4f} | D 遮蔽（先验） {acc['D']:.4f}",
        f"exact   ：A {exact['A']:.4f} | B {exact['B']:.4f} | C {exact['C']:.4f} | D {exact['D']:.4f}",
        "",
        f"有效性门：C−B = {gate_diff:.4f}（线 {GATE_MARGIN}），二项 p={p_binom:.4f}（线 0.01）-> {'过' if gate_ok else '未过'}",
        f"逐条目 Δ = {delta_mean:.4f} ± {ci:.4f}（95% CI）",
        "",
        f"判词：{verdict}",
        "",
        f"完整数据: {out_path}",
    ]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
