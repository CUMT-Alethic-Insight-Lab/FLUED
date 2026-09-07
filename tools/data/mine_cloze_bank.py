#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mine_cloze_bank.py — cloze 检索回执题库预挖（用户裁定 2026-08-17）。

口径（2026-08-17 用户裁定）：
- 任务形态：cloze 问答压检索压力——passage 中挖去一段 ~32B 连续切片作 answer，
  query = passage 中 answer 替换为恰好三个半角下划线 ``___``（其余逐字符不动）。
- 语料：P:/FLUED_corpus/corpus_v3/corpus_v3.txt 的**尾部 5%**（seek 到 95% 处，
  前进到下一换行后流式扫描；语料只读，绝不修改）。CPU 单进程。
  注意：corpus_v3 的行内换行以**字面两字符 ``\\n``** 存储（另有少量真换行作
  文档分隔）——"换行"判定两者都算：passage ≤3 行按真 ``\n`` 与字面 ``\\n``
  合计计数；answer 一律不得含真换行或字面转义序列（``\\n`` ``\\t`` ``\\r``
  ``\\"``），否则反斜杠会白捡符号判据、且 "\n\nN." 列表头属模板化内容。
- 条目构造：
  1. passage：连续文本 96–192 字节，UTF-8 完整（首尾截到字符边界，
     思路同 tools/eval/paging_harness.py::_snap_utf8 / tools/analysis/v3_6/
     probe_archive_addressing_v37.py 的字节 snap），允许换行但不超过 3 行；
  2. answer：passage 内连续切片，起点在 passage 的 25%–60% 字节区间（前后留
     上下文），snap 后 28–36 字节，不含换行；
  3. 特异性过滤（防"不用检索也能蒙"）：answer 至少满足一条——≥2 个数字 /
     专名样片段（含 ≥2 个大写字母的 token 如 NASA/GDP/U.S.，或 ≥2 个句中大写
     起首词如 "the Canadian government"）/ 含非常见符号（@ # % _ / = 等）；
     且 answer 不是纯常见虚词（the/of/的/了 类）；明显模板化片段（纯空白、纯
     标点、license boilerplate、"as an AI language model" 类）整条丢弃；
  4. 去重：passage 的 sha1 前 16 位入集合，重复丢弃。
- 输出契约（下游训练器按此读，勿改字段名）：JSONL 每行
  {"id": int 从0起, "passage": str, "answer": str, "query": str,
   "answer_bytes": int(answer 的 UTF-8 字节数)}
- 自检（本脚本末尾真跑，重读产物文件而非信任内存）：
  query.replace('___', answer, 1) == passage 逐条成立；answer_bytes∈[28,36]；
  passage 字节∈[96,192]；全库 sha1 无重复；抽 20 条落 spotcheck 文件人工抽查；
  统计（含数字/大写比例、长度分布、拒绝原因）落 stats json。

Usage:
  py -3.14 -X utf8 tools/data/mine_cloze_bank.py                 # 全量 50k 实挖
  py -3.14 -X utf8 tools/data/mine_cloze_bank.py --n 3000 \
      --out outputs/_cloze_calib.jsonl --spotcheck outputs/_cloze_calib_spot.txt \
      --stats outputs/_cloze_calib_stats.json                   # 小样本校准
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import time
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_CORPUS = Path("P:/FLUED_corpus/corpus_v3/corpus_v3.txt")
DEFAULT_OUT = Path("P:/FLUED_corpus/cloze_bank_v1.jsonl")
DEFAULT_SPOTCHECK = REPO_ROOT / "outputs" / "cloze_bank_v1_spotcheck.txt"
DEFAULT_STATS = REPO_ROOT / "outputs" / "cloze_bank_v1_stats.json"

TAIL_FRAC = 0.95  # 挖掘区 = 文件尾部 5%
PASSAGE_MIN_B, PASSAGE_MAX_B = 96, 192
ANSWER_MIN_B, ANSWER_MAX_B = 28, 36
ANS_START_LO, ANS_START_HI = 0.25, 0.60  # answer 起点占 passage 字节比例
READ_BLOCK = 8 << 20  # 8 MiB 流式块
GAP_MAX = 1200  # 条目间随机跳跃，去相关（过大会在 50k 指标下扫出尾部 5% 挖掘区）
ANSWER_TRIES = 8  # 每个 passage 的 answer 切片最大尝试次数（特异性命中率低，单次即弃会耗尽挖掘区）
MAX_LINES = 3
MIN_ALNUM_RATIO = 0.55  # passage 字母数字占比下限（挡纯空白/纯标点）
MIN_ANSWER_ALNUM = 4  # answer 至少含有的字母数字字符数

# 非常见符号（裁定口径 "@、#、%、_、/、= 等"）。不含反斜杠：corpus_v3 的行内
# 换行是字面 "\n"，answer 切到其邻位会白捡一个无特异性的 "\"，故 answer 见
# 反斜杠一律整条拒（见 ANSWER_FORBIDDEN），符号判据也不再计入它。
UNUSUAL_SYMBOLS = set("@#%_/=&$+*~^<>|€£¥©®™°§µ")

# 句末标点（判"句中大写起首词"时用：大写词前一个非空白字符不是这些才算 mid-sentence）
SENT_END = set('.!?"\')]}>:')

# 明显模板化 / boilerplate（大小写不敏感）；命中即整条丢弃
BOILERPLATE_RE = re.compile(
    r"all rights reserved|terms of service|privacy policy|cookie policy"
    r"|mit license|gnu general public license|apache license|creative commons"
    r"|copyright \(c\)|permission is hereby granted|do not sell my personal"
    r"|subscribe to our newsletter|as an ai language|i cannot have personal",
    re.IGNORECASE,
)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")  # \n \t 之外的控制字符
CHAR_RUN_RE = re.compile(r"(.)\1{9,}", re.DOTALL)  # 同一字符连跑 ≥10（分隔线类）
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z.'-]*")
CAPWORD_RE = re.compile(r"[A-Z][a-z]{1,}")
WORD_SPLIT_RE = re.compile(r"[^0-9A-Za-z\u3400-\u9fff]+")
# corpus_v3 的行内换行是字面两字符 "\n"（反斜杠+n），另有少量真换行作文档分隔；
# 行数统计两者都算
LINEBREAK_RE = re.compile(r"\n|\\n")
# answer 内禁止出现的换行/转义序列（真 \n \r，字面 \n \t \r \" 转义，及反斜杠
# 本身——语料行内换行是字面 "\n"，切片紧邻会白捡无特异性的 "\" 碎片）
ANSWER_FORBIDDEN = ("\n", "\r", "\\n", "\\t", "\\r", '\\"', "\\")

STOPWORDS = {
    "the", "of", "a", "an", "and", "or", "to", "in", "on", "for", "with",
    "is", "are", "was", "were", "be", "been", "it", "its", "this", "that",
    "these", "those", "as", "at", "by", "from", "but", "not", "no", "so",
    "if", "then", "than", "into", "about", "over", "under", "between",
    "的", "了", "是", "在", "和", "与", "也", "都", "我", "你", "他", "她", "它",
}


# ---------------------------------------------------------------------------
# UTF-8 字节 snap（同 paging_harness._snap_utf8 思路：续字节为 10xxxxxx）
# ---------------------------------------------------------------------------
def _utf8_char_len(b0: int) -> int:
    if b0 < 0x80:
        return 1
    if b0 >= 0xF0:
        return 4
    if b0 >= 0xE0:
        return 3
    if b0 >= 0xC0:
        return 2
    return 0


def snap_head(bs: bytes) -> bytes:
    """前向截到字符边界：丢弃开头的续字节。"""
    i, n = 0, len(bs)
    while i < n and (bs[i] & 0xC0) == 0x80:
        i += 1
    return bs[i:]


def snap_tail(bs: bytes) -> bytes:
    """后向截到字符边界：末尾若是被截断的半个字符则整个丢弃。"""
    n = len(bs)
    i = n - 1
    while i >= 0 and (bs[i] & 0xC0) == 0x80:
        i -= 1
    if i < 0:
        return b""
    need = _utf8_char_len(bs[i])
    if need and i + need <= n:
        return bs[:n]
    return bs[:i]


# ---------------------------------------------------------------------------
# 特异性判据（answer 级，至少一条通过）
# ---------------------------------------------------------------------------
def crit_digits(ans: str) -> bool:
    return sum(1 for c in ans if c.isdigit()) >= 2


def crit_caps(ans: str) -> bool:
    """专名样片段：(i) 存在含 ≥2 个大写字母的 token（NASA/GDP/U.S./McDonald）；
    (ii) ≥2 个句中大写起首词（非 answer 开头、前一非空白字符非句末标点）。"""
    for tok in TOKEN_RE.findall(ans):
        if sum(1 for c in tok if c.isupper()) >= 2:
            return True
    interior = 0
    for m in CAPWORD_RE.finditer(ans):
        if m.start() == 0:
            continue
        j = m.start() - 1
        while j >= 0 and ans[j] in " \t":
            j -= 1
        if j >= 0 and ans[j] not in SENT_END:
            interior += 1
    return interior >= 2


def crit_symbols(ans: str) -> bool:
    return any(c in UNUSUAL_SYMBOLS for c in ans)


def is_pure_stopword(ans: str) -> bool:
    words = [w for w in WORD_SPLIT_RE.split(ans.lower()) if w]
    return bool(words) and all(w in STOPWORDS for w in words)


# ---------------------------------------------------------------------------
# 条目构造
# ---------------------------------------------------------------------------
def make_entry(pending: bytes, rng: random.Random):
    """从 pending 头部取一个候选 passage 并构造条目；返回 (entry|None, reason, consumed)。"""
    n0 = len(pending)
    want = min(rng.randint(PASSAGE_MIN_B, PASSAGE_MAX_B), n0)
    raw = snap_tail(snap_head(pending[:want]))
    consumed = want  # 无论成败都前进（含 gap 在外层加）
    if len(raw) < PASSAGE_MIN_B:
        return None, "passage_too_short_after_snap", consumed
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, "utf8_decode", consumed

    # 行数：真换行与字面 "\n" 都算换行；超过 3 行则在第 3 个换行处截断
    # （截后不足 96B 丢弃）。截断保留原文逐字符不动。
    breaks = list(LINEBREAK_RE.finditer(text))
    if len(breaks) > MAX_LINES - 1:
        text = text[: breaks[MAX_LINES - 1].start()]
        raw = text.encode("utf-8")
        if len(raw) < PASSAGE_MIN_B:
            return None, "passage_too_short_after_linecut", consumed
    if not (PASSAGE_MIN_B <= len(raw) <= PASSAGE_MAX_B):
        return None, "passage_len", consumed

    if CONTROL_RE.search(text):
        return None, "control_chars", consumed
    if "___" in text:  # 会破坏 replace 契约
        return None, "contains_blank_token", consumed
    if CHAR_RUN_RE.search(text):
        return None, "char_run", consumed
    n_alnum = sum(1 for c in text if c.isalnum())
    if n_alnum / max(1, len(text)) < MIN_ALNUM_RATIO:
        return None, "low_alnum_ratio", consumed
    if BOILERPLATE_RE.search(text):
        return None, "boilerplate", consumed

    # ---- answer 切片：起点 ∈ [25%, 60%]，snap 后 28–36B，不含换行 ----
    # 同一 passage 最多试 ANSWER_TRIES 个切片（plain prose 里特异性命中率低，
    # 单次即弃会耗尽尾部 5% 挖掘区），第一个通过的切片胜出。
    L = len(raw)
    lo, hi = int(ANS_START_LO * L), int(ANS_START_HI * L)
    if hi < lo:
        return None, "answer_window", consumed
    last_reason = "low_specificity"
    for _try in range(ANSWER_TRIES):
        s0 = lo + rng.randrange(hi - lo + 1)
        head = snap_head(raw[s0:])
        s0 = L - len(head)  # snap 后的绝对起点
        if s0 > 0 and raw[s0 - 1] == 0x5C:  # 起点紧邻反斜杠 = 从 "\n" 的 'n' 起切，转义碎片
            last_reason = "answer_escape_fragment"
            continue
        alen = rng.randint(ANSWER_MIN_B, ANSWER_MAX_B)
        ans_b = snap_tail(raw[s0 : s0 + alen])
        if not (ANSWER_MIN_B <= len(ans_b) <= ANSWER_MAX_B):
            last_reason = "answer_len"
            continue
        if s0 + len(ans_b) > L:
            last_reason = "answer_overflow"
            continue
        try:
            ans = ans_b.decode("utf-8")
        except UnicodeDecodeError:
            last_reason = "answer_utf8"
            continue
        if any(seq in ans for seq in ANSWER_FORBIDDEN):
            last_reason = "answer_newline_or_escape"
            continue
        if sum(1 for c in ans if c.isalnum()) < MIN_ANSWER_ALNUM:
            last_reason = "answer_low_alnum"
            continue
        if not (crit_digits(ans) or crit_caps(ans) or crit_symbols(ans)):
            last_reason = "low_specificity"
            continue
        if is_pure_stopword(ans):
            last_reason = "pure_stopword"
            continue

        # ---- query：answer 原样替换为恰好三个半角下划线，其余逐字符不动 ----
        ci0 = len(raw[:s0].decode("utf-8"))  # s0 在字符边界上
        ci1 = ci0 + len(ans)
        if text[ci0:ci1] != ans:  # 构造不变量防御（理论上不可能触发）
            last_reason = "span_misalign"
            continue
        query = text[:ci0] + "___" + text[ci1:]

        return {
            "passage": text,
            "answer": ans,
            "query": query,
            "answer_bytes": len(ans_b),
            "_sha": hashlib.sha1(raw).hexdigest()[:16],
            "_passage_bytes": len(raw),
        }, "ok", consumed
    return None, last_reason, consumed


# ---------------------------------------------------------------------------
# 挖掘主循环：seek 到 95%，前进到下一换行，流式扫描
# ---------------------------------------------------------------------------
def mine(args) -> tuple[list[dict], Counter, dict]:
    rng = random.Random(args.seed)
    size = args.corpus.stat().st_size
    region_start = int(size * TAIL_FRAC)
    entries: list[dict] = []
    seen: set[str] = set()
    reject: Counter = Counter()
    n_candidates = 0
    t0 = time.time()

    with args.corpus.open("rb") as fh:
        fh.seek(region_start)
        fh.readline()  # 跳到下一整行，避免从半个字符/半行开始
        pos = fh.tell()
        pending = b""
        eof = False
        while len(entries) < args.n and n_candidates < args.max_candidates:
            if not eof and len(pending) < PASSAGE_MAX_B + 64:
                block = fh.read(min(READ_BLOCK, size - pos))
                if block:
                    pos += len(block)
                    pending += block
                else:
                    eof = True
            if len(pending) < PASSAGE_MIN_B:
                break
            n_candidates += 1
            entry, reason, consumed = make_entry(pending, rng)
            reject[reason] += 1
            advance = consumed + rng.randrange(GAP_MAX)
            pending = pending[advance:] if advance < len(pending) else b""
            if entry is not None:
                if entry["_sha"] in seen:
                    reject["duplicate"] += 1
                    continue
                seen.add(entry["_sha"])
                entries.append(entry)
            if len(entries) % 10000 == 0 and entries and reject["ok"] == len(entries):
                print(f"[mine] ... {len(entries)}/{args.n}", file=sys.stderr)
        meta = {
            "source_path": str(args.corpus),
            "source_size_bytes": size,
            "region": f"tail {1 - TAIL_FRAC:.0%} (seek {TAIL_FRAC:.0%})",
            "region_start_byte": region_start,
            "scanned_until_byte": pos,
            "candidates": n_candidates,
            "accepted": len(entries),
            "rejected": {k: v for k, v in reject.most_common() if k != "ok"},
            "elapsed_sec": round(time.time() - t0, 1),
            "seed": args.seed,
        }
    return entries, reject, meta


# ---------------------------------------------------------------------------
# 自检（重读产物文件，不信任内存）+ spotcheck + stats
# ---------------------------------------------------------------------------
def verify_bank(out_path: Path, spot_path: Path, stats_path: Path, meta: dict) -> bool:
    rows = []
    with out_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    errors = []
    seen_sha: set[str] = set()
    n_digit = n_upper = 0
    len_hist: Counter = Counter()
    crit_ct: Counter = Counter()
    passage_lens = []
    prev_id = -1
    for r in rows:
        rid, p, a, q, ab = r["id"], r["passage"], r["answer"], r["query"], r["answer_bytes"]
        if rid != prev_id + 1:
            errors.append(f"id 不连续: {rid} after {prev_id}")
        prev_id = rid
        if set(r.keys()) != {"id", "passage", "answer", "query", "answer_bytes"}:
            errors.append(f"id {rid}: 字段集合 {sorted(r.keys())} 不合契约")
        if q.replace("___", a, 1) != p:
            errors.append(f"id {rid}: replace 契约失败")
        if q.count("___") != 1:
            errors.append(f"id {rid}: query 中 ___ 出现 {q.count('___')} 次")
        if ab != len(a.encode("utf-8")):
            errors.append(f"id {rid}: answer_bytes 字段与实际不符")
        if not (ANSWER_MIN_B <= ab <= ANSWER_MAX_B):
            errors.append(f"id {rid}: answer_bytes={ab} 越界")
        pb = len(p.encode("utf-8"))
        if not (PASSAGE_MIN_B <= pb <= PASSAGE_MAX_B):
            errors.append(f"id {rid}: passage 字节 {pb} 越界")
        if any(seq in a for seq in ANSWER_FORBIDDEN):
            errors.append(f"id {rid}: answer 含换行/转义序列")
        if len(LINEBREAK_RE.findall(p)) > MAX_LINES - 1:
            errors.append(f"id {rid}: passage 超过 {MAX_LINES} 行")
        sha = hashlib.sha1(p.encode("utf-8")).hexdigest()[:16]
        if sha in seen_sha:
            errors.append(f"id {rid}: sha1 重复")
        seen_sha.add(sha)
        if any(c.isdigit() for c in a):
            n_digit += 1
        if any(c.isupper() for c in a):
            n_upper += 1
        len_hist[ab] += 1
        passage_lens.append(pb)
        if crit_digits(a):
            crit_ct["digits>=2"] += 1
        if crit_caps(a):
            crit_ct["caps"] += 1
        if crit_symbols(a):
            crit_ct["symbols"] += 1

    n = len(rows)
    ok = not errors
    # ---- 抽 20 条人工抽查样本 ----
    spot_rng = random.Random(20260817)
    picks = spot_rng.sample(rows, min(20, n))
    lines = [
        "cloze_bank_v1 spotcheck — 2026-08-17 预挖口径，20 条随机抽查（seed 20260817）",
        f"产物: {out_path}  总条目: {n}  自检: {'PASS' if ok else 'FAIL'}",
        "",
    ]
    for r in picks:
        lines.append(f"--- id {r['id']} ---")
        lines.append(f"passage ({len(r['passage'].encode('utf-8'))}B): {r['passage']}")
        lines.append(f"answer  ({r['answer_bytes']}B): {r['answer']}")
        lines.append(f"query   : {r['query']}")
        lines.append("")
    spot_path.parent.mkdir(parents=True, exist_ok=True)
    spot_path.write_text("\n".join(lines), encoding="utf-8")

    stats = {
        "built_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "script": "tools/data/mine_cloze_bank.py",
        "spec": "2026-08-17 用户裁定：cloze 检索回执；尾部5%语料；answer 28-36B；passage 96-192B；sha1[:16] 去重",
        "n_entries": n,
        "verify": {
            "ok": ok,
            "n_errors": len(errors),
            "errors_head": errors[:20],
            "sha1_duplicates": n - len(seen_sha),
        },
        "answer_stats": {
            "frac_has_digit": round(n_digit / max(1, n), 4),
            "frac_has_upper": round(n_upper / max(1, n), 4),
            "answer_bytes_hist": {str(k): len_hist[k] for k in sorted(len_hist)},
            "criteria_pass": dict(crit_ct),
        },
        "passage_bytes": {
            "min": min(passage_lens) if passage_lens else 0,
            "max": max(passage_lens) if passage_lens else 0,
            "mean": round(sum(passage_lens) / max(1, n), 1),
        },
        "mining": meta,
    }
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    stats_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    return ok


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="cloze 检索回执题库预挖（2026-08-17 口径）")
    ap.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--spotcheck", type=Path, default=DEFAULT_SPOTCHECK)
    ap.add_argument("--stats", type=Path, default=DEFAULT_STATS)
    ap.add_argument("--n", type=int, default=50000)
    ap.add_argument("--seed", type=int, default=20260817)
    ap.add_argument("--max-candidates", type=int, default=2_000_000)
    args = ap.parse_args(argv)

    if not args.corpus.is_file():
        print(f"[FATAL] 语料不存在: {args.corpus}", file=sys.stderr)
        return 2

    entries, reject, meta = mine(args)
    print(
        f"[mine] candidates={meta['candidates']} accepted={meta['accepted']} "
        f"elapsed={meta['elapsed_sec']}s rejects={meta['rejected']}",
        file=sys.stderr,
    )
    if len(entries) < args.n:
        print(f"[WARN] 只挖到 {len(entries)}/{args.n} 条（挖掘区候选耗尽）", file=sys.stderr)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="\n") as fh:
        for i, e in enumerate(entries):
            row = {
                "id": i,
                "passage": e["passage"],
                "answer": e["answer"],
                "query": e["query"],
                "answer_bytes": e["answer_bytes"],
            }
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"[write] {args.out} ({len(entries)} 条)", file=sys.stderr)

    ok = verify_bank(args.out, args.spotcheck, args.stats, meta)
    print(f"[verify] {'PASS' if ok else 'FAIL'}; spotcheck={args.spotcheck}; stats={args.stats}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
