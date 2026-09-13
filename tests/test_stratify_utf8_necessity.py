"""R2 必要性账 UTF-8 位置分层复算单测（脚本在
tools/baselines/deltanet_r2/stratify_utf8_necessity.py；仪器在
tools/analysis/cross_arch/probe_e122_deltanet_book.py，判读量函数零改动复用）。

Covers: (1) piece→bytes 三规则（▁→0x20 / 字节回退 <0xNN> / UTF-8 编码；
<unk> 响亮拒绝）；(2) taxonomy 判类（ascii / cjk_whole / cjk_frag_lead /
cjk_frag_cont / other_bytes，严格 UTF-8 结构 + 优先级）；(3) 全词表类表构建
（<unk> 归 other_bytes 不炸）；(4) 逐 item 校验复算封印（gram@repeat_pos /
source_pos==find_first / 续尾区间 / delta==NLL 差 / 强线 / role，违例响亮）；
(5) piece→bytes 拼接==窗文本字节（映射实证封印）；(6) 分层窗 sums 与仪器
pool 同款累加语义；(7) 贡献分解精确可加（Σ_c contrib == 全体对比量，份额
Σ==1）；(8) 地板类比读数（单字熵手算对账）；(9) 仪器血缘常量（种子 424243 /
n_boot 2000 / 判读量函数即 e122.bootstrap_contrast）。
"""

from __future__ import annotations

import math
from types import SimpleNamespace

import pytest

import tools.analysis.cross_arch.probe_e122_deltanet_book as dn
import tools.baselines.deltanet_r2.stratify_utf8_necessity as st

# ---------------------------------------------------------------------------
# 合成材料：VocabTableStub 以 bytes 直接当 piece 语义（单测不过真 tokenizer）
# ---------------------------------------------------------------------------


def _table(ids_bytes: dict[int, bytes]) -> dict[int, dict]:
    return {i: {"piece": repr(b), "bytes_hex": b.hex(),
                "class": st.classify_token_bytes(b)}
            for i, b in ids_bytes.items()}


# --- 1. piece→bytes ----------------------------------------------------------


def test_piece_to_bytes_rules():
    assert st.piece_to_bytes("▁") == b" "
    assert st.piece_to_bytes("▁hell") == b" hell"
    assert st.piece_to_bytes("<0xE6>") == b"\xe6"
    assert st.piece_to_bytes("<0x00>") == b"\x00"
    assert st.piece_to_bytes("获") == "获".encode("utf-8")
    assert st.piece_to_bytes("<s>") == b"<s>"  # 字面文本路径
    assert st.piece_to_bytes("</s>") == b"</s>"
    with pytest.raises(ValueError, match="<unk>"):
        st.piece_to_bytes("<unk>")


# --- 2. taxonomy 判类 ---------------------------------------------------------


def test_classify_ascii_and_whole():
    assert st.classify_token_bytes(b"abc 123") == "ascii"
    # 空字节串（unk 的空 hex 占位）无多字节 → ascii 桶；真出现在数据时由
    # 字节往返校验响亮（空拼接 != 文本字节），类桶无碍
    assert st.classify_token_bytes(b"") == "ascii"
    assert st.classify_token_bytes("你".encode()) == "cjk_whole"
    assert st.classify_token_bytes("获".encode()) == "cjk_whole"
    assert st.classify_token_bytes("，。".encode()) == "cjk_whole"  # 多字闭合
    assert st.classify_token_bytes("a你".encode()) == "cjk_whole"  # ASCII 前缀混合
    assert st.classify_token_bytes(b"\xf0\x9f\x98\x80") == "cjk_whole"  # 4 字节 emoji


def test_classify_fragments_precedence():
    # 首字节碎片：lead 开头、续字节未闭合（用户规格「首字节」）
    assert st.classify_token_bytes(b"\xe6") == "cjk_frag_lead"
    assert st.classify_token_bytes(b"\xe8\x8e") == "cjk_frag_lead"  # 缺 1 续字节
    assert st.classify_token_bytes(b"\xf0\x9f") == "cjk_frag_lead"
    # 续字节碎片：续字节开头（lead 在上一 token）（用户规格「续字节」）
    assert st.classify_token_bytes(b"\xb7") == "cjk_frag_cont"
    assert st.classify_token_bytes(b"\xad\x8e") == "cjk_frag_cont"
    # 优先级：starts_mid > lead_open（ starts_mid 先判）
    assert st.classify_token_bytes(b"\xad\xe6") == "cjk_frag_cont"
    # 严格违例 → other_bytes：非法 lead（0xC0/0xFF）、无主续字节
    assert st.classify_token_bytes(b"\xc0\x80") == "other_bytes"
    assert st.classify_token_bytes(b"\xff") == "other_bytes"
    assert st.classify_token_bytes(b"\xe6\x41") == "other_bytes"  # lead 后接非续字节
    assert st.classify_token_bytes(b"\xe8\x8e\xb7\x80") == "other_bytes"  # 闭合后无主续字节


def test_build_vocab_class_table_unk_survives():
    class _Tok:
        def __len__(self):
            return 4

        def convert_ids_to_tokens(self, i):
            return ["<unk>", "<s>", "获", "<0xAD>"][i]
    tab = st.build_vocab_class_table(_Tok())
    assert tab[0]["class"] == "other_bytes" and tab[0]["bytes_hex"] == ""
    assert tab[1]["class"] == "ascii"  # b"<s>" 全 ASCII 字节
    assert tab[2]["class"] == "cjk_whole"
    assert tab[3]["class"] == "cjk_frag_cont"
    assert st.floor_analogs(tab, {}, [])["uniform_lnV_nat"] == pytest.approx(math.log(4))


# --- 3. 逐 item 校验（复算封印） -----------------------------------------------


N, TAIL = 3, 3


def _synthetic_window():
    """128 token 窗：gram A=(7,8,9) 源@10、重复@60，续尾 63..65 计分。"""
    ids = [(i * 7 + 13) % 7 for i in range(128)]
    ids[10:13] = [7, 8, 9]
    ids[60:63] = [7, 8, 9]
    return ids


def _synthetic_items(ids):
    items = []
    for t in (63, 64, 65):
        na, nb = 2.0, 2.5
        items.append({"window_id": 0, "token_pos": t, "role": "selected",
                      "gram": [7, 8, 9], "repeat_pos": 60, "source_pos": 10,
                      "NLL_a": na, "NLL_b1": nb, "delta_b1": nb - na,
                      "strong": (nb - na) >= 1.0})
    return items


def _e122_stub():
    return SimpleNamespace(find_first=dn.find_first)


def test_verify_items_pass_and_failures_are_loud():
    ids = _synthetic_window()
    items = _synthetic_items(ids)
    st.verify_items_against_window(_e122_stub(), items, ids, N, TAIL, 2048)  # 全过
    for field, bad in (("gram", [7, 8, 0]), ("source_pos", 11),
                       ("token_pos", 66), ("NLL_b1", 3.0), ("strong", True),
                       ("role", "decoy")):
        broken = [dict(it) for it in items]
        broken[0][field] = bad
        with pytest.raises(RuntimeError, match="停报"):
            st.verify_items_against_window(_e122_stub(), broken, ids, N, TAIL, 2048)


def test_verify_window_bytes_roundtrip_loud():
    # 往返封印不变式：concat(ids[1:]) == " "+文本 或 ==文本（前导空格 = LLaMA 系
    # sentencepiece add_dummy_prefix；实测文本以空白开头时 SP 不加 dummy 前缀）
    tab = _table({1: b" ", 2: "你".encode(), 3: " 你".encode()})
    ids = [1, 1, 2]  # ids[0]=BOS 跳过；token 流 = ▁ + 你，文本「你」无前导空格
    st.verify_window_bytes_roundtrip(tab, ids, "你")       # dummy 前缀形态
    st.verify_window_bytes_roundtrip(tab, [1, 3], " 你")   # 文本自带前导空格形态
    with pytest.raises(RuntimeError, match="失真"):
        st.verify_window_bytes_roundtrip(tab, ids, "  你好")  # 文本不符 → 失配


# --- 4. 分层 sums / 贡献分解 / 地板类比 ----------------------------------------


def _records():
    return [
        {"block": "b0", "window_id": 0, "role": "selected", "class": "ascii",
         "delta_b1": 1.0, "NLL_a": 3.0, "strong": True},
        {"block": "b0", "window_id": 0, "role": "control", "class": "ascii",
         "delta_b1": 0.5, "NLL_a": 3.0, "strong": False},
        {"block": "b0", "window_id": 1, "role": "selected", "class": "ascii",
         "delta_b1": 0.0, "NLL_a": 3.0, "strong": False},
        {"block": "b0", "window_id": 1, "role": "selected", "class": "cjk_whole",
         "delta_b1": 2.0, "NLL_a": 6.0, "strong": True},
        {"block": "b0", "window_id": 1, "role": "control", "class": "cjk_whole",
         "delta_b1": 0.25, "NLL_a": 6.0, "strong": False},
        {"block": "b0", "window_id": 2, "role": "selected", "class": "cjk_frag_cont",
         "delta_b1": 4.0, "NLL_a": 9.0, "strong": True},
        {"block": "b0", "window_id": 2, "role": "control", "class": "cjk_frag_lead",
         "delta_b1": 1.0, "NLL_a": 9.0, "strong": False},
    ]


def test_stratified_window_sums_matches_pool_semantics():
    strata = st.stratified_window_sums(_records())
    a = strata["ascii"][0]
    # 与 pool_necessity_blocks 同一累加语义（selected→n_sel/sel_d_b1/n_strong）
    assert a == {"n_sel": 1, "sel_d_b1": 1.0, "n_strong": 1,
                 "n_ctl": 1, "ctl_d_b1": 0.5}
    assert strata["cjk_frag_cont"][2]["n_sel"] == 1
    assert strata["cjk_frag_lead"][2]["n_ctl"] == 1
    assert "cjk_whole" in strata and 0 not in strata["cjk_whole"]  # 窗 0 无整字


def test_contribution_decomposition_exactly_additive():
    recs = _records()
    comp = st.contribution_decomposition(recs)
    total = (sum(r["delta_b1"] for r in recs if r["role"] == "selected") / comp["n_sel"]
             - sum(r["delta_b1"] for r in recs if r["role"] == "control") / comp["n_ctl"])
    assert abs(sum(comp["contrib"].values()) - total) < 1e-12
    assert abs(sum(comp["contrib"].values()) / total - 1.0) < 1e-12
    # 类别缺席（other_bytes 无记录）→ contrib=0 且不炸
    assert comp["contrib"]["other_bytes"] == 0.0


def test_floor_analogs_entropy_handcheck():
    tab = _table({1: b"a", 2: b"b", 3: "你".encode(), 4: b"\xad"})
    counts = {"ascii": {1: 3, 2: 1}, "cjk_whole": {3: 4}}
    floors = st.floor_analogs(tab, counts, [
        {"class": "ascii", "NLL_a": 2.0}, {"class": "ascii", "NLL_a": 4.0}])
    # 手算：ascii 流 {a:3, b:1} → H = -(0.75 ln0.75 + 0.25 ln0.25)
    h = -(0.75 * math.log(0.75) + 0.25 * math.log(0.25))
    assert floors["ascii"]["unigram_entropy_nat"] == pytest.approx(h)
    assert floors["ascii"]["uniform_within_class_nat"] == pytest.approx(math.log(2))
    assert floors["ascii"]["n_tokens_windows"] == 4
    assert floors["ascii"]["mean_NLL_a_nat"] == 3.0
    assert floors["cjk_whole"]["unigram_entropy_nat"] == 0.0  # 单 type → 0 熵
    assert floors["cjk_frag_cont"]["n_tokens_windows"] == 0
    assert floors["cjk_frag_cont"]["unigram_entropy_nat"] is None
    assert floors["uniform_lnV_nat"] == pytest.approx(math.log(4))


def test_merge_class_token_counts():
    parts = [{"ascii": {1: 2}}, {"ascii": {1: 1, 2: 1}, "cjk_whole": {3: 5}}]
    merged = st.merge_class_token_counts(parts)
    assert merged["ascii"] == {1: 3, 2: 1}
    assert merged["cjk_whole"] == {3: 5}


# --- 5. 仪器血缘（复用封印） ----------------------------------------------------


def test_instrument_lineage_constants():
    assert st.BOOTSTRAP_SEED == 424243  # 池化判决件种子谱系
    assert st.N_BOOT == 2000
    assert st.STRONG_LINE == dn.STRONG_LINE_NAT
    assert st.CLASSES == ("ascii", "cjk_whole", "cjk_frag_lead",
                          "cjk_frag_cont", "other_bytes")
    # 判读量路径即仪器自家函数（同输入同输出，含种子复现性）
    ws = [{"n_sel": 5, "sel_d_b1": 5.0 * i + 3.0, "n_ctl": 4, "ctl_d_b1": 0.1 * i}
          for i in range(20)]
    assert st.load_e122().bootstrap_contrast(ws, 500, 7) == \
        dn.bootstrap_contrast(ws, 500, 7)


def test_truncation_regex():
    assert st._TRUNC_RE.match("ids[:2048]").group(1) == "2048"
    assert st._TRUNC_RE.match("ids[:]") is None
