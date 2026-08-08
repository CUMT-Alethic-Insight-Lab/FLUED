#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P0 文档级评测集巡检脚本（eval_data 目录，数据本体不进 git）。

扫描输出目录下所有 `<dataset>/<file>.jsonl`（跳过 raw/），对每个文件报告：
条数、context UTF-8 字节长度分布（min/median/p90/max）、字段完整性，并抽样 2 条展示。

用法：
    python tools/eval/p0_inspect.py [--root PATH] [--no-samples]

默认 root：仓库根目录的上一级下的 `eval_data/`（即与 FLUED 仓库同级），
与 P0 建集选址一致（仓库 .gitignore 未忽略 data/，故数据集放在仓库外）。
"""
import argparse
import json
import os
import sys


def pct(sorted_vals, q):
    """最近秩百分位；sorted_vals 非空。"""
    k = max(0, min(len(sorted_vals) - 1, round(q * (len(sorted_vals) - 1))))
    return sorted_vals[k]


def fmt_bytes(n):
    if n >= 1 << 20:
        return f"{n / (1 << 20):.1f}MB"
    if n >= 1 << 10:
        return f"{n / (1 << 10):.1f}KB"
    return f"{n}B"


def shorten(text, limit=160):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit] + "…"


def inspect_file(path, show_samples=True):
    n = 0
    ctx_lens = []
    bad_schema = 0
    empty_q = 0
    empty_ans = 0
    samples = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                bad_schema += 1
                continue
            if not all(k in r for k in ("id", "source", "context", "question", "answers")):
                bad_schema += 1
            ctx = r.get("context") or ""
            ctx_lens.append(len(ctx.encode("utf-8")))
            if not r.get("question"):
                empty_q += 1
            if not r.get("answers"):
                empty_ans += 1
            if n == 0:
                samples.append(r)
            n += 1
    if n == 0:
        return None
    # 第二条抽样：中间位置的记录（重读文件取中位行，避免全量驻留内存 —— 行内容已在上面流式释放）
    mid = n // 2
    if mid > 0:
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i == mid:
                    samples.append(json.loads(line))
                    break
    ctx_lens.sort()
    stats = {
        "rows": n,
        "min": ctx_lens[0],
        "median": pct(ctx_lens, 0.5),
        "p90": pct(ctx_lens, 0.9),
        "max": ctx_lens[-1],
        "empty_q": empty_q,
        "empty_ans": empty_ans,
        "bad_schema": bad_schema,
    }
    if show_samples:
        stats["samples"] = samples
    return stats


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--root", default=os.path.join(os.path.dirname(repo_root), "eval_data"),
                    help="评测集输出目录（默认：与仓库同级的 eval_data/）")
    ap.add_argument("--no-samples", action="store_true", help="不展示抽样记录")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"[ERR] 目录不存在: {root}")
        return 1
    print(f"# P0 评测集巡检 | root = {root}\n")

    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != "raw"]
        for fn in sorted(filenames):
            if fn.endswith(".jsonl"):
                files.append(os.path.join(dirpath, fn))
    files.sort()
    if not files:
        print("[WARN] 未发现任何 .jsonl")
        return 0

    total_rows = 0
    total_bytes = 0
    header = f"{'file':<46} {'rows':>6} {'min':>8} {'median':>9} {'p90':>9} {'max':>9} {'emptyQ':>6} {'emptyA':>6}"
    print(header)
    print("-" * len(header))
    per_dataset = {}
    for path in files:
        rel = os.path.relpath(path, root)
        st = inspect_file(path, show_samples=not args.no_samples)
        if st is None:
            print(f"{rel:<46} EMPTY")
            continue
        total_rows += st["rows"]
        total_bytes += os.path.getsize(path)
        per_dataset.setdefault(os.path.dirname(rel), []).append(st["rows"])
        print(f"{rel:<46} {st['rows']:>6} {fmt_bytes(st['min']):>8} {fmt_bytes(st['median']):>9} "
              f"{fmt_bytes(st['p90']):>9} {fmt_bytes(st['max']):>9} {st['empty_q']:>6} {st['empty_ans']:>6}"
              + (f"  [bad_schema={st['bad_schema']}]" if st["bad_schema"] else ""))
        if not args.no_samples:
            for r in st.get("samples", []):
                print(f"  · sample id={r.get('id')} source={r.get('source')}")
                print(f"    question: {shorten(r.get('question', ''), 120) or '(空)'}")
                print(f"    answers:  {shorten(r.get('answers'), 120) or '(空)'}")
                print(f"    context:  {shorten(r.get('context'), 200)}")

    print("-" * len(header))
    print(f"TOTAL: {len(files)} files, {total_rows} rows, {fmt_bytes(total_bytes)}")
    print("\n## 数据集汇总")
    for ds in sorted(per_dataset):
        print(f"  {ds:<28} files={len(per_dataset[ds]):<3} rows={sum(per_dataset[ds])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
