"""E121 D1 稀有度频率表产品化（离线预计算）。

任务书（唯一事实源）: docs/versions/v3.7/FLUED_V3_7_D1_CROSSSEG_TAIL_20260904_CN.md
（冻结 v1, 2026-09-04）。施工注记 1（字面执行）: 候选收集与背景计数**直接 import**
密度账仪器核心函数（collect_candidates / background_counts / cross_chunk_occurrences）,
本脚本零复制改写——diff 里只有调用接线。

流程: 语料采样 ~50K 窗（4096B, seed 42, 与 demand_density_book.main 同款流式偏移
采样）→ collect_candidates 收集跨 chunk 重复 gram 候选并集（L=6, chunk=16）→
background_counts 在固定 256MB 背景样本（seed 42, 函数内固定 4 段偏移）对候选集
计数 → 落盘 npz（grams 'S6' + counts int64）+ meta.json（窗数/背景大小/seed/
候选数/语料 SHA256/覆盖率统计）。

用法: python tools/analysis/v3_6/build_d1_rare_table.py \
        [--corpus P:\\FLUED_corpus\\corpus_v3\\corpus_v3.txt] [--windows 50000] \
        [--bg-mb 256] [--ngram-len 6] [--seed 42] \
        [--out-dir outputs/d1_rare_table_l6_20260904]
"""
import argparse
import hashlib
import json
import random
import time
from pathlib import Path

import numpy as np

import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# 密度账同源（任务书 §3 注记 1）: 核心函数只 import, 不复制改写
from tools.analysis.v3_6.demand_density_book import (  # noqa: E402
    CHUNK,
    SEQ_LEN,
    background_counts,
    collect_candidates,
    cross_chunk_occurrences,
)


def _sha256_file(path: str, chunk: int = 1 << 24) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def _sample_windows(corpus_path: str, n_windows: int, seed: int) -> list[bytes]:
    """与 demand_density_book.main 同款流式随机偏移采样（4096B 窗）。"""
    size = Path(corpus_path).stat().st_size
    rng = random.Random(seed)
    windows: list[bytes] = []
    with open(corpus_path, "rb") as f:
        for _ in range(n_windows):
            f.seek(rng.randrange(0, size - SEQ_LEN - 1))
            w = f.read(SEQ_LEN)
            if len(w) == SEQ_LEN:
                windows.append(w)
    return windows


def _probe_coverage(corpus_path: str, table: dict[bytes, int], ngram_len: int,
                    n_probe: int, seed: int) -> dict:
    """独立探针窗（seed+1, 与建表采样流不重叠）上的覆盖率统计：表外 gram 份额
    即训练期 d1_offtable_grams 仪表的先验期望（诚实边界注记, 任务书 §3）。"""
    wins = _sample_windows(corpus_path, n_probe, seed + 1)
    n_hit = n_off = 0
    per_win_off_frac = []
    for w in wins:
        occ = cross_chunk_occurrences(w, ngram_len)
        grams = list(occ.keys())
        off = sum(1 for g in grams if g not in table)
        n_hit += len(grams)
        n_off += off
        per_win_off_frac.append(off / len(grams) if grams else 0.0)
    return {
        "probe_windows": len(wins),
        "probe_seed": seed + 1,
        "mean_hit_grams_per_window": round(n_hit / max(len(wins), 1), 3),
        "offtable_gram_share": round(n_off / max(n_hit, 1), 6),
        "mean_offtable_frac_per_window": round(sum(per_win_off_frac) / max(len(per_win_off_frac), 1), 6),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=r"P:\FLUED_corpus\corpus_v3\corpus_v3.txt")
    ap.add_argument("--windows", type=int, default=50000)
    ap.add_argument("--bg-mb", type=int, default=256)
    ap.add_argument("--ngram-len", type=int, default=6)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--probe-windows", type=int, default=500)
    ap.add_argument("--out-dir", default="outputs/d1_rare_table_l6_20260904")
    ap.add_argument("--skip-sha256", action="store_true", help="调试用; 正式产物必须带 SHA256")
    args = ap.parse_args()

    t0 = time.time()
    L = int(args.ngram_len)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[d1-table] 采样 {args.windows} 窗 @{SEQ_LEN}B (seed={args.seed}) ...", flush=True)
    # 候选阶段检查点 (~50 分钟纯 Python 扫描): 崩在下游 (npz/SHA256/probe) 时
    # 原地续跑, 不重付扫描成本
    cp_path = out_dir / "_candidates.pkl"
    if cp_path.exists():
        import pickle

        with cp_path.open("rb") as f:
            cp = pickle.load(f)
        if cp.get("ngram_len") != L:
            raise SystemExit(
                f"[d1-table] 候选检查点 ngram_len={cp.get('ngram_len')} 与现跑 L={L} 不符 "
                f"(删 {cp_path} 重扫)"
            )
        cand = set(cp["grams"])
        windows = []
        print(f"[d1-table] 候选检查点续跑: {len(cand)} gram（跳过采样/扫描）", flush=True)
    else:
        windows = _sample_windows(args.corpus, int(args.windows), int(args.seed))
        print(f"[d1-table] 实采 {len(windows)} 窗（{time.time() - t0:.0f}s）", flush=True)
        print(f"[d1-table] collect_candidates L={L} chunk={CHUNK}（密度账同源 import）...",
              flush=True)
        cand = collect_candidates(windows, L)
        import pickle

        with cp_path.open("wb") as f:
            pickle.dump({"ngram_len": L, "grams": sorted(cand)}, f)
        print(f"[d1-table] 候选 gram {len(cand)}（{time.time() - t0:.0f}s, 检查点已落）",
              flush=True)

    print(f"[d1-table] background_counts bg={args.bg_mb}MB seed={args.seed}（固定 4 段偏移）...", flush=True)
    counts = background_counts(args.corpus, cand, L, int(args.bg_mb), int(args.seed))
    print(f"[d1-table] 背景计数完成（{time.time() - t0:.0f}s）", flush=True)

    # gram 用 2D uint8 矩阵存 (N, L) —— 'S6' dtype 会把尾随 NUL 当终止符截断
    # (语料含零字节, 全 NUL gram 会被塌成 b'' 造成查表 KeyError)
    grams_sorted = sorted(counts.keys())
    grams_arr = np.frombuffer(b"".join(grams_sorted), dtype=np.uint8).reshape(-1, L)
    counts_arr = np.array([counts[g] for g in grams_sorted], dtype=np.int64)

    vals = np.sort(counts_arr)
    meta = {
        "task_book": "docs/versions/v3.7/FLUED_V3_7_D1_CROSSSEG_TAIL_20260904_CN.md",
        "arm": "E121 D1 跨段续尾损失重加权 50M 短臂（稀有度频率表）",
        "corpus": str(args.corpus),
        "corpus_bytes": Path(args.corpus).stat().st_size,
        "n_windows": len(windows),
        "seq_len": SEQ_LEN,
        "chunk": CHUNK,
        "ngram_len": L,
        "bg_mb": int(args.bg_mb),
        "seed": int(args.seed),
        "n_candidates": int(len(grams_arr)),
        "bg_count_zero": int((counts_arr == 0).sum()),
        "bg_count_le3": int((counts_arr <= 3).sum()),
        "bg_count_quantiles": {
            "p50": int(np.quantile(vals, 0.50)),
            "p90": int(np.quantile(vals, 0.90)),
            "p99": int(np.quantile(vals, 0.99)),
            "max": int(vals[-1]),
        },
        "elapsed_sec": 0.0,
    }
    if not args.skip_sha256:
        print("[d1-table] 计算语料 SHA256 ...", flush=True)
        meta["corpus_sha256"] = _sha256_file(args.corpus)
    print("[d1-table] 探针窗覆盖率统计（seed+1 独立流）...", flush=True)
    meta["probe_coverage"] = _probe_coverage(
        args.corpus, counts, L, int(args.probe_windows), int(args.seed)
    )

    npz_path = out_dir / f"d1_rare_table_l{L}.npz"
    np.savez(npz_path, grams=grams_arr, counts=counts_arr)
    meta["elapsed_sec"] = round(time.time() - t0, 1)
    (out_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(
        f"[d1-table] 落盘 {npz_path} + meta.json | 候选 {meta['n_candidates']} "
        f"| 背景零计数 {meta['bg_count_zero']} | 探针表外份额 "
        f"{meta['probe_coverage']['offtable_gram_share']} | {meta['elapsed_sec']}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
