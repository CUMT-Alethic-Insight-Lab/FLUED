"""甲形态（跨段续尾损失重加权）需求密度账——零训练判别（下一季验证序第一关）。

口径（docs/research/FLUED_NEXT_SEASON_DEMAND_SPEC_20260904_CN.md §2 甲 + §3）：
  训练窗 seq_len=4096B、chunk=16B（bytes_per_chunk）。目标字节获重加权当且仅当：
  ① 它所延续的 L-gram 在本窗**严格更早的 chunk** 里出现过（源在上一段——窗内注意力
     够不到 chunk 内部细粒度，但状态行索引覆盖它）；
  ② 该 L-gram 语料级稀有（背景样本出现次数 ≤ 阈值；先验能蒙的串不算需求）。
  命中处起的 T 个续尾字节计入等效监督。
等效监督字节/窗 = 命中位置数 × T × 权重（权重=1 为基线，权重是旋钮直接乘）。
对照基线：Q13 突发性注入 ≈1.5 监督字节/窗（用户裁定数，需求规格 §1 第 4 条）。

用法：python tools/analysis/v3_6/demand_density_book.py --corpus <path> [--windows 3000]
      [--bg-mb 32] [--out-dir outputs/demand_density_book_20260904]
"""
import argparse
import json
import os
import random
import time

SEQ_LEN = 4096
CHUNK = 16
Q13_BASELINE_BPW = 1.5  # 监督字节/窗，Q13 突发性注入基线（用户裁定）


def cross_chunk_occurrences(window: bytes, ngram_len: int) -> dict[bytes, list[int]]:
    """单窗扫描：返回 {gram: [跨 chunk 重复出现的起始位置]}（条件①：出现 chunk 严格晚于
    该 gram 的最早出现 chunk）。同 chunk 内重复不计。"""
    first_chunk: dict[bytes, int] = {}
    occ: dict[bytes, list[int]] = {}
    for p in range(0, len(window) - ngram_len + 1):
        g = window[p:p + ngram_len]
        c = p // CHUNK
        fc = first_chunk.get(g)
        if fc is None:
            first_chunk[g] = c
        elif fc < c:
            occ.setdefault(g, []).append(p)
    return occ


def supervised_count(occ: dict[bytes, list[int]], rare_grams: set | None,
                     ngram_len: int, tail: int, win_len: int) -> int:
    """按稀有集 + 尾长聚合一窗的等效监督字节数（rare_grams=None 不过滤）。"""
    hits: set[int] = set()
    for g, ps in occ.items():
        if rare_grams is not None and g not in rare_grams:
            continue
        for p in ps:
            for t in range(p + ngram_len, min(p + ngram_len + tail, win_len)):
                hits.add(t)
    return len(hits)


def count_supervised_positions(window: bytes, ngram_len: int, tail: int,
                               rare_grams: set | None) -> tuple[int, set]:
    """测试用便捷封装：单窗 (命中字节数, 命中 gram 集)。"""
    occ = cross_chunk_occurrences(window, ngram_len)
    n = supervised_count(occ, rare_grams, ngram_len, tail, len(window))
    grams = {g for g in occ if rare_grams is None or g in rare_grams}
    return n, grams


def collect_candidates(windows: list[bytes], ngram_len: int) -> set[bytes]:
    cand: set[bytes] = set()
    for w in windows:
        cand |= cross_chunk_occurrences(w, ngram_len).keys()
    return cand


def background_counts(corpus_path: str, cand: set[bytes], ngram_len: int,
                      bg_mb: int, seed: int) -> dict[bytes, int]:
    """背景样本里只数候选集（内存有界）。4 段随机采样拼 bg_mb。"""
    counts = {g: 0 for g in cand}
    if not cand:
        return counts
    size = os.path.getsize(corpus_path)
    rng = random.Random(seed + 1)
    seg = max(bg_mb * 1024 * 1024 // 4, 1 << 20)
    with open(corpus_path, "rb") as f:
        for _ in range(4):
            f.seek(rng.randrange(0, max(size - seg - 1, 1)))
            bg = f.read(seg)
            for p in range(0, len(bg) - ngram_len + 1):
                g = bg[p:p + ngram_len]
                if g in counts:
                    counts[g] += 1
    return counts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--windows", type=int, default=3000)
    ap.add_argument("--bg-mb", type=int, default=32)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out-dir", default="outputs/demand_density_book_20260904")
    args = ap.parse_args()

    t0 = time.time()
    size = os.path.getsize(args.corpus)
    rng = random.Random(args.seed)
    windows: list[bytes] = []
    with open(args.corpus, "rb") as f:
        for _ in range(args.windows):
            f.seek(rng.randrange(0, size - SEQ_LEN - 1))
            w = f.read(SEQ_LEN)
            if len(w) == SEQ_LEN:
                windows.append(w)
    print(f"[density] 采样 {len(windows)} 窗 @4096B（{size/1e9:.1f}GB 语料）", flush=True)

    report: dict = {"corpus": args.corpus, "corpus_bytes": size,
                    "n_windows": len(windows), "seq_len": SEQ_LEN, "chunk": CHUNK,
                    "q13_baseline_bytes_per_window": Q13_BASELINE_BPW,
                    "bg_mb": args.bg_mb, "seed": args.seed, "cells": []}
    for L in (4, 6, 8):
        occs = [cross_chunk_occurrences(w, L) for w in windows]
        cand = set().union(*(o.keys() for o in occs)) if occs else set()
        bgc = background_counts(args.corpus, cand, L, args.bg_mb, args.seed)
        for thr in (0, 1, 3, 10, 30):
            rare = {g for g, n in bgc.items() if n <= thr}
            for T in (2, 3, 4):
                per_win = [supervised_count(o, rare, L, T, SEQ_LEN) for o in occs]
                mean_bpw = sum(per_win) / len(per_win)
                frac_hit = sum(1 for x in per_win if x > 0) / len(per_win)
                cell = {"ngram_len": L, "rarity_bg_max_count": thr, "tail": T,
                        "n_candidate_grams": len(cand), "n_rare_grams": len(rare),
                        "mean_supervised_bytes_per_window": round(mean_bpw, 3),
                        "frac_windows_with_hit": round(frac_hit, 4),
                        "vs_q13_baseline_x": round(mean_bpw / Q13_BASELINE_BPW, 2)}
                report["cells"].append(cell)
                print(f"[density] L={L} 稀有≤{thr} 尾{T}: {mean_bpw:.2f} 字节/窗 "
                      f"({cell['vs_q13_baseline_x']}×Q13) 命中窗率 {frac_hit:.2f} "
                      f"稀有gram {len(rare)}/{len(cand)}", flush=True)
    os.makedirs(args.out_dir, exist_ok=True)
    out = os.path.join(args.out_dir, "density_book.json")
    report["elapsed_sec"] = round(time.time() - t0, 1)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(f"[density] 落盘 {out}（{report['elapsed_sec']}s）")


if __name__ == "__main__":
    main()
