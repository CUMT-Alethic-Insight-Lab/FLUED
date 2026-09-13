"""R2 臂门③密度账（no-model 干跑）：E122 同源选择链在本臂体制的位点密度基线。

任务书 §3.3：两本账点火门（密度账+必要性账基线，起训前）。本仪器 = 密度账——
**import 复用** E122 必要性账仪器（tools/analysis/cross_arch/probe_e122_deltanet_book.py，
冻结口径 v1.0–v1.3a 的复证臂 token 同构）的选择链与手术单构造器，参数逐项取
仪器默认（窗 4096B / BOS / 截 2048 / seg 256 / n 3 / tail 3 / rare 0.2 /
pool 0.1 / 表 2048 窗），在无模型干跑下测：
- 窗非空率（sel>0）与每窗计分位密度（处理/对照）；
- 手术单可构造率（红队条款响亮断言全窗通过 = 语料上手术可行性）；
- 跨段稀有 gram 命中/表外计数。
不及格判据（教义：改语料/位点池不改剂量）：窗非空率塌、计分位密度塌、
手术单红队断言成片失败。

Usage:
  python tools/baselines/deltanet_r2/measure_r2_density.py \
      --corpus /workspace/corpus/corpus_v3.txt \
      --tokenizer-path /workspace/models/delta_net-1.3B-100B \
      --n-windows 500 --out-dir outputs/r2_deltanet50m_20260913/density
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

import torch  # noqa: F401  # 仪器模块顶层 import torch（cpu 即可，无前向）

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from tools.analysis.cross_arch import probe_e122_deltanet_book as e122

import tools.baselines.deltanet_r2.r2_spec as spec


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--corpus", required=True)
    p.add_argument("--tokenizer-path", required=True)
    p.add_argument("--n-windows", type=int, default=500)
    p.add_argument("--table-windows", type=int, default=2048)
    p.add_argument("--ngram-len", type=int, default=3, choices=[2, 3, 4])
    p.add_argument("--tail", type=int, default=3)
    p.add_argument("--segment-tokens", type=int, default=256)
    p.add_argument("--rare-quantile", type=float, default=0.2)
    p.add_argument("--pool-quantile", type=float, default=0.1)
    p.add_argument("--seed", type=int, default=spec.EVAL_SEED,
                   help="评测谱系种子（异于训练流，E121 纪律）")
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.tokenizer_path, trust_remote_code=True)
    v = tok.vocab_size
    if v != spec.R2_CONFIG["vocab_size"]:
        raise SystemExit(f"[r2-density] tokenizer 词表 {v} != 配置词表 "
                         f"{spec.R2_CONFIG['vocab_size']}（loud fail）")

    corpus = Path(args.corpus)
    table, table_scanned = e122.build_rare_table(
        tok, corpus, args.table_windows, spec.WINDOW_BYTES, args.ngram_len, v,
        spec.MAX_TOKENS)
    pool = e122.build_replacement_pool(table, args.ngram_len, v, args.pool_quantile)
    if not pool:
        raise SystemExit("[r2-density] 替换池为空（响亮拒绝）")
    print(f"[r2-density] 稀有表 {len(table)} gram（扫 {table_scanned} 窗），"
          f"池 {len(pool)}", flush=True)

    rng = random.Random(args.seed)
    scan = argparse.Namespace(
        ngram_len=args.ngram_len, tail=args.tail, segment_tokens=args.segment_tokens,
        rare_quantile=args.rare_quantile, pool_quantile=args.pool_quantile,
        max_draws=64, strong_line=1.0)
    max_byte_touched = 0
    sums = {"n_windows": 0, "n_used": 0, "n_empty": 0, "n_plan_fail": 0,
            "n_sel": 0, "n_ctl": 0, "n_decoys": 0, "n_hit_grams": 0,
            "n_offtable": 0, "n_truncated": 0}
    sel_per_win: list[int] = []
    plan_errors: list[str] = []

    with corpus.open("rb") as f:
        for wi in range(args.n_windows):
            f.seek(wi * spec.WINDOW_BYTES)
            raw = f.read(spec.WINDOW_BYTES)
            if len(raw) < spec.WINDOW_BYTES:
                break
            max_byte_touched = max(max_byte_touched, (wi + 1) * spec.WINDOW_BYTES)
            ids, full_len = e122.tokenize_window(
                tok, spec.window_text(raw), spec.MAX_TOKENS)
            if full_len > spec.MAX_TOKENS:
                sums["n_truncated"] += 1
            sums["n_windows"] += 1

            occ = e122.cross_segment_occurrences(ids, args.ngram_len, args.segment_tokens)
            rare, offtable = e122.select_rare_grams(occ, table, args.rare_quantile, v)
            sel, _ov = e122.select_tail_positions(occ, rare, args.ngram_len, args.tail, len(ids))
            sums["n_hit_grams"] += len(occ)
            sums["n_offtable"] += offtable
            if not sel:
                sums["n_empty"] += 1
                continue
            try:
                treat, ctrl, _tc, _cc = e122.split_selected_clusters(
                    sel, ids, rng, args.ngram_len)
                plan = e122.plan_window_surgery(
                    ids, sel, treat, ctrl, table, pool, rng, args.ngram_len,
                    args.tail, v, max_draws=64)
            except Exception as ex:  # 红队断言/池尽 = 手术不可构造，如实计数不静默
                sums["n_plan_fail"] += 1
                if len(plan_errors) < 20:
                    plan_errors.append(f"win{wi}: {type(ex).__name__}: {ex}")
                continue
            n_sel = sum(1 for t, (g, _p) in sel.items() if g in treat)
            n_ctl = sum(1 for t, (g, _p) in sel.items() if g in ctrl)
            sums["n_used"] += 1
            sums["n_sel"] += n_sel
            sums["n_ctl"] += n_ctl
            sums["n_decoys"] += len(plan.decoys)
            sel_per_win.append(n_sel)
            if (wi + 1) % 100 == 0:
                print(f"[r2-density] {wi+1}/{args.n_windows} 窗 "
                      f"({time.time()-t0:.0f}s)", flush=True)

    sel_sorted = sorted(sel_per_win)
    summary = {
        "probe": "R2 门③密度账（E122 同源选择链 no-model 干跑，参数=仪器默认）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "corpus": str(corpus),
        "tokenizer_path": args.tokenizer_path,
        "params": {
            "n_windows": args.n_windows, "table_windows": args.table_windows,
            "ngram_len": args.ngram_len, "tail": args.tail,
            "segment_tokens": args.segment_tokens,
            "rare_quantile": args.rare_quantile, "pool_quantile": args.pool_quantile,
            "seed": args.seed,
            "window_bytes": spec.WINDOW_BYTES, "max_tokens": spec.MAX_TOKENS,
        },
        "rare_table": {"n_grams": len(table), "pool_size": len(pool),
                       "windows_scanned": table_scanned},
        "totals": sums,
        "sel_per_window": {
            "mean": (sum(sel_per_win) / len(sel_per_win)) if sel_per_win else None,
            "p50": (sel_sorted[len(sel_sorted)//2] if sel_sorted else None),
            "min": (sel_sorted[0] if sel_sorted else None),
            "max": (sel_sorted[-1] if sel_sorted else None),
        },
        "windows_used_rate": (sums["n_used"] / sums["n_windows"]) if sums["n_windows"] else None,
        "plan_fail_examples": plan_errors,
        "gate_note": "不及格判据：窗非空率塌 / 计分位密度塌 / 红队断言成片失败——按教义改语料/位点池不改剂量",
        "eval_seed_lineage": "种子取评测谱系（≠训练流 42）",
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
