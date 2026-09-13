"""R2 必要性账（DeltaNet-50M，池化 +0.1040 nat）的 UTF-8 位置分层复算（纯后处理）。

问题（用户审计单）：池化对比量（contrast，处理臂平均 ΔNLL 减对照臂平均 ΔNLL）
+0.1040 nat 的内容依赖是否由「高地板/易猜」类别（纯 ASCII、整字 CJK token）
承载，而难猜类别（跨 token 的 UTF-8 字节碎片）在零水位？做法：把每个**被计分
目标 token**（token_pos 处的 token，注意不是 gram 语境里的 id——仪器语义
probe_e122_deltanet_book.select_tail_positions：计分位 = 稀有 gram 跨段重复出现
处之后的续尾 token）按其解码字节组成分类，逐类复用**仪器自家**
bootstrap_contrast（tools/analysis/cross_arch/probe_e122_deltanet_book.py，
种子 424243 谱系、n_boot=2000、窗级重抽样，判读量定义零改动）出对比量点估+CI。

与判决件的血缘（复算封印）：items.jsonl 未记录被计分 token id，本脚本按仪器
同款窗定义（corpus[w*4096,(w+1)*4096) → utf-8 errors=replace → tokenizer 默认
加 BOS → ids[:2048]）重分词还原，并逐 item 校验 gram@repeat_pos、
source_pos==find_first、delta_b1==NLL_b1−NLL_a、强命中线；校验非全过即响亮
停报（不绕道）。同窗流先复算不分层对比量，须与各块 summary.json 及
necessity_pooled_seen.json 逐位一致（同种子同累加序 → 同 RNG 流）。

taxonomy（token 解码字节组成，详见产物 README）：
  ascii         纯 ASCII：全部字节 < 0x80
  cjk_whole     整字：≥1 个多字节 UTF-8 字符在 token 内完整闭合、无残缺字节
                （可含 ASCII 字节前后缀；语料中多字节字符以 CJK 为主）
  cjk_frag_lead 首字节碎片：token 以多字节字符的 lead 字节开头但续字节未闭合
  cjk_frag_cont 续字节碎片：token 以续字节（0x80–0xBF）开头（lead 在上一 token）
  other_bytes   严格 UTF-8 结构违例或特殊 token（预期 0，非零响亮计数）

Usage:
  python tools/baselines/deltanet_r2/stratify_utf8_necessity.py \
      --closing-dir outputs/r2_deltanet50m_20260913/closing \
      --blocks b0 b1 b2 b3 unseen --pooled-blocks b0 b1 b2 b3 \
      --corpus /workspace/corpus/corpus_v3.txt \
      --tokenizer-path <模型 checkpoint 目录（tokenizer 与仪器 --model-path 同源）> \
      --out-dir outputs/r2_deltanet50m_20260913/utf8_strat
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

CLASSES = ("ascii", "cjk_whole", "cjk_frag_lead", "cjk_frag_cont", "other_bytes")

BOOTSTRAP_SEED = 424243  # 池化判决件与各块 summary 的 bootstrap 种子（谱系统一）
N_BOOT = 2000
STRONG_LINE = 1.0

SPACES = "▁"  # sentencepiece 空位标记 → 0x20
_SPECIAL_PIECE_BYTES = {"<s>": b"<s>", "</s>": b"</s>"}  # 字面文本路径可能产生
_TRUNC_RE = re.compile(r"ids\[:(\d+)\]")


def load_e122():
    """仪器模块加载（判读量函数单点复用；transformers/torch 只在远端运行态需要）。"""
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from tools.analysis.cross_arch import probe_e122_deltanet_book as e122
    return e122


# ---------------------------------------------------------------------------
# taxonomy：piece → bytes → 类别
# ---------------------------------------------------------------------------


def piece_to_bytes(piece: str) -> bytes:
    """sentencepiece piece → 原始字节。三条规则：空位标记 ▁→0x20；字节回退
    <0xNN>→单字节 NN；其余按 UTF-8 编码。特殊 piece 按字面文本字节映射
    （<unk> 无字面语义 → 响亮拒绝：byte_fallback 词表下正常数据不应出现）。"""
    if piece == "<unk>":
        raise ValueError("piece=<unk>（byte_fallback 词表下不应出现，响亮拒绝）")
    if piece in _SPECIAL_PIECE_BYTES:
        return _SPECIAL_PIECE_BYTES[piece]
    if len(piece) == 6 and piece.startswith("<0x") and piece.endswith(">"):
        return bytes([int(piece[3:5], 16)])
    return piece.replace(SPACES, " ").encode("utf-8")


def parse_utf8_structure(b: bytes) -> dict:
    """字节串的 UTF-8 结构扫描：{'starts_mid': 首字节是续字节（lead 在上一
    token；开头的连续续字节串同属上一字符）, 'lead_open': 尾部多字节字符未闭合
    （缺续字节）, 'n_mb': token 内完整闭合的多字节字符数, 'n_ascii': ASCII
    字节数, 'invalid': 严格结构违例（非法 lead 取值/字符闭合后再现续字节）}。"""
    starts_mid = False
    n_mb = 0
    n_ascii = 0
    invalid = False
    need = 0

    def _lead_need(x: int) -> int:
        if 0xC2 <= x <= 0xDF:
            return 1
        if 0xE0 <= x <= 0xEF:
            return 2
        if 0xF0 <= x <= 0xF4:
            return 3
        return 0  # 非法 lead

    i = 0
    while i < len(b):
        x = b[i]
        if need > 0:
            if 0x80 <= x <= 0xBF:
                need -= 1
                if need == 0:
                    n_mb += 1
            else:
                invalid = True
                need = 0
        elif x < 0x80:
            n_ascii += 1
        elif 0xC2 <= x <= 0xF4:  # 合法 lead 区间
            need = _lead_need(x)
        elif 0x80 <= x <= 0xBF:
            if i == 0:
                # token 开头的连续续字节串同属上一 token 打开的字符
                starts_mid = True
                while i + 1 < len(b) and 0x80 <= b[i + 1] <= 0xBF:
                    i += 1
            else:
                invalid = True  # 字符已闭合（或 ASCII）后的无主续字节
        else:  # 0xC0/0xC1/0xF5..0xFF 非法 lead
            invalid = True
        i += 1
    return {"starts_mid": starts_mid, "lead_open": need > 0, "n_mb": n_mb,
            "n_ascii": n_ascii, "invalid": invalid}


def classify_token_bytes(b: bytes) -> str:
    """taxonomy 判类（优先级：invalid > starts_mid > lead_open > 有完整多字节 >
    纯 ASCII）。返回 CLASSES 之一。"""
    st = parse_utf8_structure(b)
    if st["invalid"]:
        return "other_bytes"
    if st["starts_mid"]:
        return "cjk_frag_cont"
    if st["lead_open"]:
        return "cjk_frag_lead"
    if st["n_mb"] >= 1:
        return "cjk_whole"
    return "ascii"


def build_vocab_class_table(tokenizer) -> dict[int, dict]:
    """全词表 id → {piece, bytes_hex, class}（预计算一次；词表组成进产物供
    「该类 token 在 BPE 词表里的多寡」参照）。<unk> 是合法词表条目（只是不应
    出现在数据里）→ 归 other_bytes、bytes_hex 置空；若它真出现在窗流中，
    字节往返校验会因空拼接失配响亮。"""
    table = {}
    for i in range(len(tokenizer)):
        piece = tokenizer.convert_ids_to_tokens(i)
        if piece == "<unk>":
            table[i] = {"piece": piece, "bytes_hex": "", "class": "other_bytes"}
            continue
        bts = piece_to_bytes(piece)
        table[i] = {"piece": piece, "bytes_hex": bts.hex(),
                    "class": classify_token_bytes(bts)}
    return table


# ---------------------------------------------------------------------------
# 窗还原 + 逐 item 校验（复算封印；非全过即响亮）
# ---------------------------------------------------------------------------


def verify_corpus_prefix(corpus: Path, n_bytes: int, expect_sha256: str) -> None:
    """语料前缀 SHA256 对锚（各块 summary.corpus.scored_prefix_sha256）。"""
    h = hashlib.sha256()
    with corpus.open("rb") as f:
        remain = n_bytes
        while remain:
            chunk = f.read(min(1 << 20, remain))
            if not chunk:
                raise RuntimeError(f"语料不足 {n_bytes}B（前缀锚无法核验，停报）")
            h.update(chunk)
            remain -= len(chunk)
    got = h.hexdigest()
    if got != expect_sha256:
        raise RuntimeError(f"语料前缀 SHA256 不符：got={got} expect={expect_sha256}（停报）")


def reconstruct_window_ids(tok, corpus: Path, window_id: int, window_bytes: int,
                           max_tokens: int) -> tuple[list[int], bool, str]:
    """仪器同款窗还原：字节窗 → utf-8 errors=replace → tokenize（默认加 BOS）
    → 截断 max_tokens。返回 (ids, 是否截断, 窗文本)。"""
    with corpus.open("rb") as f:
        f.seek(window_id * window_bytes)
        raw = f.read(window_bytes)
    if len(raw) < window_bytes:
        raise RuntimeError(f"窗 {window_id} 语料不足 {window_bytes}B（停报）")
    text = raw.decode("utf-8", errors="replace")
    ids_full = list(tok(text)["input_ids"])
    return ids_full[:max_tokens], len(ids_full) > max_tokens, text


def verify_items_against_window(e122, items: list[dict], ids: list[int],
                                n: int, tail: int, max_tokens: int) -> None:
    """逐 item 对还原窗校验（复算封印）：gram@repeat_pos 逐 id 相等；
    source_pos == find_first；token_pos 在续尾区间 [p+n, p+n+tail) 且窗内；
    delta_b1 == NLL_b1 − NLL_a（JSON double 往返精确）；strong 与强线一致；
    role ∈ {selected, control}。任何违例 RuntimeError 响亮停报。"""
    first_cache: dict[tuple, int] = {}
    for it in items:
        t = it["token_pos"]
        p = it["repeat_pos"]
        g = tuple(it["gram"])
        if tuple(ids[p:p + n]) != g:
            raise RuntimeError(
                f"win{it['window_id']} pos{t}: gram@repeat_pos 不符 "
                f"item={it['gram']} ids={ids[p:p + n]}（重分词还原失败，停报）")
        if g not in first_cache:
            first_cache[g] = e122.find_first(ids, g)
        if first_cache[g] != it["source_pos"]:
            raise RuntimeError(
                f"win{it['window_id']} pos{t}: source_pos {it['source_pos']} != "
                f"find_first {first_cache[g]}（停报）")
        if not (p + n <= t < min(p + n + tail, len(ids)) and t < max_tokens):
            raise RuntimeError(f"win{it['window_id']} pos{t}: token_pos 不在续尾区间（停报）")
        if it["delta_b1"] != it["NLL_b1"] - it["NLL_a"]:
            raise RuntimeError(f"win{it['window_id']} pos{t}: delta_b1 与 NLL 差不符（停报）")
        if it["strong"] != (it["delta_b1"] >= STRONG_LINE):
            raise RuntimeError(f"win{it['window_id']} pos{t}: strong 与强线不符（停报）")
        if it["role"] not in ("selected", "control"):
            raise RuntimeError(f"win{it['window_id']} pos{t}: role 非法 {it['role']}（停报）")


def verify_window_bytes_roundtrip(class_table: dict, ids: list[int], text: str) -> None:
    """piece→bytes 映射的实证封印：跳过 BOS 后逐 token 字节拼接 ==「空格 + 窗文本」
    或 ==窗文本（二者取一，须全字节精确）。前导空格 = LLaMA 系 sentencepiece
    add_dummy_prefix 的 dummy 前缀；实测（b2 窗 1455）：文本本身以空白开头时
    SP 不再加 dummy 前缀，此时拼接==文本字节。两种形态都对不上才是映射失真
    （▁/字节回退/UTF-8 编码任一弄错都过不了）。无截断窗上 100% 必过；截断窗
    跳过（尾部 token 被截）。违例响亮。计分类别不受影响（被计分位 ≥3）。"""
    buf = bytearray()
    for i in ids[1:]:
        buf += bytes.fromhex(class_table[i]["bytes_hex"])
    text_b = text.encode("utf-8")
    if bytes(buf) not in (b" " + text_b, text_b):
        raise RuntimeError("piece→bytes 拼接 != 空格+窗文本/窗文本字节"
                           "（taxonomy 映射失真，停报）")


# ---------------------------------------------------------------------------
# 分层 sums / 贡献分解 / 地板类比（全部报数，判读权主会话）
# ---------------------------------------------------------------------------


def new_sums() -> dict:
    return {"n_sel": 0, "sel_d_b1": 0.0, "n_strong": 0, "n_ctl": 0, "ctl_d_b1": 0.0}


def accumulate_item(sums: dict, it: dict) -> None:
    """与 pool_necessity_blocks.py 同一累加语义：selected→n_sel/sel_d_b1/
    n_strong，control→n_ctl/ctl_d_b1（逐位文件序累加，保 RNG 流一致）。"""
    if it["role"] == "selected":
        sums["n_sel"] += 1
        sums["sel_d_b1"] += it["delta_b1"]
        sums["n_strong"] += int(it["strong"])
    else:
        sums["n_ctl"] += 1
        sums["ctl_d_b1"] += it["delta_b1"]


def stratified_window_sums(records: list[dict]) -> dict[str, dict[int, dict]]:
    """类标注 records（文件序）按被计分 token 类别分层的逐窗 sums。
    返回 {class: {window_id: sums}}（窗键按首现序 = 文件序）。"""
    strata: dict[str, dict[int, dict]] = {c: {} for c in CLASSES}
    for r in records:
        s = strata[r["class"]].setdefault(r["window_id"], new_sums())
        accumulate_item(s, r)
    return strata


def contribution_decomposition(records: list[dict]) -> dict:
    """对比量的逐类加和分解（精确可加：Σ_c contrib_c == 全体对比量）：
    contrib_c = Σ_{处理,c} δ/N_sel − Σ_{对照,c} δ/N_ctl。"""
    n_sel = sum(1 for r in records if r["role"] == "selected")
    n_ctl = len(records) - n_sel
    sel_d: Counter = Counter()
    ctl_d: Counter = Counter()
    for r in records:
        (sel_d if r["role"] == "selected" else ctl_d)[r["class"]] += r["delta_b1"]
    contrib = {c: sel_d[c] / n_sel - ctl_d[c] / n_ctl for c in CLASSES}
    return {"n_sel": n_sel, "n_ctl": n_ctl, "contrib": contrib}


def floor_analogs(class_table: dict, class_token_counts: dict[str, Counter],
                  records: list[dict]) -> dict:
    """各类「盲猜地板」的 BPE 类比读数（报数不判读）：
    uniform_lnV_nat = ln(V)（类无关参照）；unigram_entropy_nat = 计分窗全 token
    流内该类的经验单字（unigram）边际熵（自然对数，nat）；uniform_within_class_nat
    = ln(窗流内该类 type 数)（类内均匀盲猜地板）；mean_NLL_a_nat = 该类被计分位
    术前基线 NLL 均值（模型自身经验易猜度）。"""
    out: dict = {"uniform_lnV_nat": math.log(len(class_table))}
    for c in CLASSES:
        cnt = class_token_counts.get(c) or Counter()
        n_c = sum(cnt.values())
        h = 0.0
        if n_c:
            for v in cnt.values():
                pr = v / n_c
                h -= pr * math.log(pr)
        sel_nll = [r["NLL_a"] for r in records if r["class"] == c]
        out[c] = {
            "n_tokens_windows": n_c,
            "n_types_windows": len(cnt),
            "unigram_entropy_nat": h if n_c else None,
            "uniform_within_class_nat": math.log(len(cnt)) if cnt else None,
            "mean_NLL_a_nat": (sum(sel_nll) / len(sel_nll)) if sel_nll else None,
        }
    return out


def class_token_counts_of(class_table: dict, window_ids: list[list[int]]) -> dict[str, Counter]:
    """窗 token 流（跳 BOS）的类别计数：{class: Counter(token_id)}。"""
    out: dict[str, Counter] = {c: Counter() for c in CLASSES}
    for ids in window_ids:
        for i in ids[1:]:
            out[class_table[i]["class"]][i] += 1
    return out


def merge_class_token_counts(parts: list[dict[str, Counter]]) -> dict[str, Counter]:
    merged: dict[str, Counter] = {c: Counter() for c in CLASSES}
    for part in parts:
        for c in CLASSES:
            merged[c].update(part.get(c, ()))
    return merged


# ---------------------------------------------------------------------------
# 单块处理 + 主流程
# ---------------------------------------------------------------------------


def load_block_items(block_dir: Path) -> list[dict]:
    items = []
    with (block_dir / "items.jsonl").open(encoding="utf-8") as f:
        for line in f:
            items.append(json.loads(line))
    return items


def stratify_block(block: str, items: list[dict], summary: dict, tok,
                   class_table: dict, e122, corpus: Path, map_fh) -> dict:
    """单块：前缀锚核验 → 窗还原+逐 item 校验+字节往返 → 类标注 → 分层 sums →
    逐类 bootstrap+地板类比+贡献分解 → 不分层复算须与 summary.contrast_b1 逐位
    一致。返回块级产物（含供池化复用的类标注 records 摘要）。"""
    corpus_meta = summary["corpus"]
    params = summary["params"]
    n, tail = params["ngram_len"], params["tail"]
    m = _TRUNC_RE.match(summary["window_definition"]["truncation"])
    if not m:
        raise RuntimeError(f"[{block}] truncation 字段无法解析 max_tokens（停报）")
    max_tokens = int(m.group(1))
    verify_corpus_prefix(corpus, corpus_meta["scored_prefix_bytes"],
                         corpus_meta["scored_prefix_sha256"])

    by_window: dict[int, list[dict]] = defaultdict(list)
    for it in items:
        by_window[it["window_id"]].append(it)

    records: list[dict] = []
    window_streams: list[list[int]] = []
    for wid in sorted(by_window):
        ids, truncated, text = reconstruct_window_ids(
            tok, corpus, wid, corpus_meta["window_bytes"], max_tokens)
        verify_items_against_window(e122, by_window[wid], ids, n, tail, max_tokens)
        if not truncated:
            verify_window_bytes_roundtrip(class_table, ids, text)
        window_streams.append(ids)
        for it in by_window[wid]:
            tid = ids[it["token_pos"]]
            meta = class_table[tid]
            records.append({"block": block, "window_id": wid, "role": it["role"],
                            "class": meta["class"], "delta_b1": it["delta_b1"],
                            "NLL_a": it["NLL_a"], "strong": it["strong"]})
            map_fh.write(json.dumps({
                "block": block, "window_id": wid, "token_pos": it["token_pos"],
                "role": it["role"], "scored_token_id": tid, "piece": meta["piece"],
                "bytes_hex": meta["bytes_hex"], "class": meta["class"],
                "NLL_a": it["NLL_a"], "NLL_b1": it["NLL_b1"],
                "delta_b1": it["delta_b1"], "strong": it["strong"],
            }, ensure_ascii=False) + "\n")

    # 不分层复算对锚（同种子同累加序 → 同 RNG 流 → 须逐位一致）
    win_sums: dict[int, dict] = {}
    for r in records:  # records 本身按 (窗升序, 文件序) 排列
        accumulate_item(win_sums.setdefault(r["window_id"], new_sums()), r)
    rerun = e122.bootstrap_contrast(list(win_sums.values()), N_BOOT, BOOTSTRAP_SEED)
    expect = summary["contrast_b1"]
    for key in ("point", "ci95_lo", "ci95_hi"):
        if rerun[key] != expect[key]:
            raise RuntimeError(f"[{block}] 不分层复算 {key}={rerun[key]!r} != "
                               f"summary {expect[key]!r}（复算封印破裂，停报）")

    # 逐类 bootstrap + 贡献分解 + 地板类比
    comp = contribution_decomposition(records)
    strata_sums = stratified_window_sums(records)
    mean_sel = sum(r["delta_b1"] for r in records if r["role"] == "selected") / comp["n_sel"]
    mean_ctl = sum(r["delta_b1"] for r in records if r["role"] == "control") / comp["n_ctl"]
    counts = class_token_counts_of(class_table, window_streams)
    strata_out = {}
    for c in CLASSES:
        sl = list(strata_sums[c].values())
        ns = sum(s["n_sel"] for s in sl)
        nc = sum(s["n_ctl"] for s in sl)
        entry: dict = {"n_sel": ns, "n_ctl": nc,
                       "mean_sel_delta": (sum(s["sel_d_b1"] for s in sl) / ns) if ns else None,
                       "mean_ctl_delta": (sum(s["ctl_d_b1"] for s in sl) / nc) if nc else None,
                       "n_strong": sum(s["n_strong"] for s in sl),
                       "point": None, "ci95": None, "ci_excludes_zero": None,
                       "n_boot_valid": 0,
                       "contribution": {"contrib": comp["contrib"][c],
                                        "share_of_contrast": None}}
        if ns and nc:
            boot = e122.bootstrap_contrast(sl, N_BOOT, BOOTSTRAP_SEED)
            entry.update({"point": boot["point"],
                          "ci95": [boot["ci95_lo"], boot["ci95_hi"]],
                          "ci_excludes_zero": boot["ci_excludes_zero"],
                          "n_boot_valid": boot["n_boot_valid"]})
        entry["contribution"]["share_of_contrast"] = (
            comp["contrib"][c] / rerun["point"]) if rerun["point"] else None
        strata_out[c] = entry
    return {
        "n_windows": len(window_streams), "n_sel": comp["n_sel"], "n_ctl": comp["n_ctl"],
        "mean_sel": mean_sel, "mean_ctl": mean_ctl,
        "contrast_point_rerun": rerun["point"],
        "ci95_rerun": [rerun["ci95_lo"], rerun["ci95_hi"]],
        "strata": strata_out,
        "floors": floor_analogs(class_table, counts, records),
        "_records": records,
        "_counts": counts,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--closing-dir", required=True)
    p.add_argument("--blocks", nargs="+", required=True,
                   help="块名（<closing-dir>/necessity_final_<块名>）")
    p.add_argument("--pooled-blocks", nargs="+", required=True,
                   help="进池化判决件的块名（顺序=判决件聚合序）")
    p.add_argument("--pooled-json", default=None,
                   help="池化判决件 JSON（默认 <closing-dir>/necessity_pooled_seen.json）")
    p.add_argument("--corpus", required=True)
    p.add_argument("--tokenizer-path", required=True,
                   help="checkpoint 目录（tokenizer 与仪器 --model-path 同源）")
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    from transformers import AutoTokenizer

    closing = Path(args.closing_dir)
    corpus = Path(args.corpus)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pooled_json = Path(args.pooled_json) if args.pooled_json else \
        closing / "necessity_pooled_seen.json"
    t0 = time.time()

    tok = AutoTokenizer.from_pretrained(args.tokenizer_path, trust_remote_code=True)
    class_table = build_vocab_class_table(tok)
    e122 = load_e122()
    vocab_comp = Counter(m["class"] for m in class_table.values())

    blocks_out: dict[str, dict] = {}
    with (out_dir / "items_class_map.jsonl").open("w", encoding="utf-8") as map_fh:
        for b in args.blocks:
            bdir = closing / f"necessity_final_{b}"
            items = load_block_items(bdir)
            summary = json.loads((bdir / "summary.json").read_text(encoding="utf-8"))
            print(f"[strat] {b}: {len(items)} items，窗还原+逐条校验中…", flush=True)
            blk = stratify_block(b, items, summary, tok, class_table, e122,
                                 corpus, map_fh)
            records = blk.pop("_records")
            blocks_out[b] = blk
            blocks_out[b]["_records"] = records  # 池化复用，不进 JSON
            print(f"[strat] {b}: rerun={blk['contrast_point_rerun']:+.6f} "
                  f"对锚一致 ({time.time() - t0:.0f}s)", flush=True)

    # ---- 池化（判决件口径）：--pooled-blocks 顺序聚合，先不分层复算对锚 ----
    pooled_records: list[dict] = []
    for b in args.pooled_blocks:
        pooled_records.extend(blocks_out[b]["_records"])  # (窗升序, 文件序) × 块序
    win_sums: dict[tuple, dict] = {}
    for r in pooled_records:
        accumulate_item(win_sums.setdefault((r["block"], r["window_id"]), new_sums()), r)
    rerun = e122.bootstrap_contrast(list(win_sums.values()), N_BOOT, BOOTSTRAP_SEED)
    pooled_expect = json.loads(pooled_json.read_text(encoding="utf-8"))["pooled"]
    if rerun["point"] != pooled_expect["contrast_point"] or \
            [rerun["ci95_lo"], rerun["ci95_hi"]] != pooled_expect["ci95"]:
        raise RuntimeError(f"池化复算 {rerun['point']!r}/"
                           f"{[rerun['ci95_lo'], rerun['ci95_hi']]!r} != 判决件 "
                           f"{pooled_expect['contrast_point']!r}/"
                           f"{pooled_expect['ci95']!r}（复算封印破裂，停报）")

    comp = contribution_decomposition(pooled_records)
    total = rerun["point"]
    if abs(sum(comp["contrib"].values()) - total) > 1e-9:
        raise RuntimeError("逐类贡献加和 != 池化对比量（>1e-9，停报）")
    strata_sums = stratified_window_sums(pooled_records)
    pooled_strata = {}
    for c in CLASSES:
        sl = list(strata_sums[c].values())
        ns = sum(s["n_sel"] for s in sl)
        nc = sum(s["n_ctl"] for s in sl)
        entry = {"n_sel": ns, "n_ctl": nc,
                 "mean_sel_delta": (sum(s["sel_d_b1"] for s in sl) / ns) if ns else None,
                 "mean_ctl_delta": (sum(s["ctl_d_b1"] for s in sl) / nc) if nc else None,
                 "n_strong": sum(s["n_strong"] for s in sl),
                 "point": None, "ci95": None, "ci_excludes_zero": None,
                 "n_boot_valid": 0,
                 "contribution": {"contrib": comp["contrib"][c],
                                  "share_of_contrast": comp["contrib"][c] / total}}
        if ns and nc:
            boot = e122.bootstrap_contrast(sl, N_BOOT, BOOTSTRAP_SEED)
            entry.update({"point": boot["point"],
                          "ci95": [boot["ci95_lo"], boot["ci95_hi"]],
                          "ci_excludes_zero": boot["ci_excludes_zero"],
                          "n_boot_valid": boot["n_boot_valid"]})
        pooled_strata[c] = entry
    pooled_floors = floor_analogs(
        class_table,
        merge_class_token_counts([blocks_out[b]["_counts"] for b in args.pooled_blocks]),
        pooled_records)

    for b in args.blocks:
        blocks_out[b].pop("_records", None)
        blocks_out[b].pop("_counts", None)

    out = {
        "probe": "R2 必要性账 +0.1040 nat 的 UTF-8 位置分层复算（纯后处理，"
                 "bootstrap=仪器自家函数，种子 424243 谱系，判读量定义零改动）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "lineage": {
            "bootstrap_fn":
                "tools/analysis/cross_arch/probe_e122_deltanet_book.py:bootstrap_contrast",
            "seed": BOOTSTRAP_SEED, "n_boot": N_BOOT,
            "pooled_source": pooled_json.name + " 口径（判决件，池化复算已逐位对锚）",
            "scoring_semantics":
                "计分位=稀有 gram 跨段重复处之后的续尾 token（select_tail_positions）；"
                "被计分目标=token_pos 处 token（非 gram 内 id）；重分词还原+逐 item "
                "校验（gram@repeat_pos / source_pos==find_first / delta==NLL 差 / "
                "强线）全过；piece→bytes 拼接==窗文本字节全窗过",
            "tokenizer_path": args.tokenizer_path,
        },
        "vocab_composition": dict(vocab_comp),
        "blocks": blocks_out,
        "pooled_seen": {
            "blocks": args.pooled_blocks,
            "n_sel": comp["n_sel"], "n_ctl": comp["n_ctl"],
            "mean_sel": sum(r["delta_b1"] for r in pooled_records
                            if r["role"] == "selected") / comp["n_sel"],
            "mean_ctl": sum(r["delta_b1"] for r in pooled_records
                            if r["role"] == "control") / comp["n_ctl"],
            "contrast_point_rerun": rerun["point"],
            "ci95_rerun": [rerun["ci95_lo"], rerun["ci95_hi"]],
            "strata": pooled_strata,
            "floors": pooled_floors,
            "note": "单块 unseen 为同带对照，不进池化判决件；逐类 verdict 不出"
                    "（判读权主会话）",
        },
    }
    (out_dir / "strata_summary.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out["pooled_seen"]["strata"], ensure_ascii=False, indent=2))
    print(f"[strat] done ({time.time() - t0:.0f}s) → {out_dir / 'strata_summary.json'}")


if __name__ == "__main__":
    main()
