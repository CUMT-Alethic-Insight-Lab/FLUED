"""E122 DeltaNet 跨架构复证仪器单测（仪器在
tools/analysis/cross_arch/probe_e122_deltanet_book.py；E122 母仪
tools/analysis/v3_6/probe_e122_necessity_book.py 的 token 级同构移植）。

Covers: (1) gram 打包 roundtrip + 保序; (2) 跨段扫描「出现段严格晚于最早出现
段」; (3) 稀有档分位选择（镜像 s1._d1_select_rare_grams，表外命中诚实计数）;
(4) 续尾选中位认领 + 重叠计数; (5) 红队域 = 家族**一切**出现区间; (6) 簇级
半分：移位兄弟源永不跨半; (7) 替换串三禁（家族/已用/原串）+ 窗内回避 + 候选
尽响亮; (8) 拼接缝家族禁（缝上产生家族成员的候选被拒，禁尽响亮）;
(9) 手术单同种子逐字段确定 + 窗长不变; (10) **诱饵域零压源对抗测试**——移位
兄弟源场景（对照簇源锚最近邻全是压线 gram：自身移位兄弟/别的簇的移位兄弟/
家族重复出现处），老贪心 87.6% 压中同款构造下新仪器零压源（多种子 × 独立
复算红队域双保险）+ 零合格响亮计数; (11) 全有或全无：处理簇源压保护区整簇
跳过、续尾位照常计分不虚报强命中; (12) ΔNLL 符号方向合成测试（stub 前向
代数：目标位当且仅当源内容在 → 处理位 ΔNLL=lnV>0 全强命中、对照位（源不动
+诱饵）ΔNLL=0、对比>0）; (13) bootstrap 可复现 + 判序 CI 在先。
"""

from __future__ import annotations

import json
import math
import random
from types import SimpleNamespace

import pytest
import torch

import tools.analysis.cross_arch.probe_e122_deltanet_book as dn

# ---------------------------------------------------------------------------
# 合成窗材料：filler 取值 0..29（步长 7 与 30 互素 → 未修补区每个 3-gram 唯一），
# 保留值 ≥30 归被测家族/诱饵材料——filler 永不撞家族 gram。
# ---------------------------------------------------------------------------

V_PACK = 64  # 打包基（全部合成 token < 64）
V_STUB = 64
N, TAIL, SEG = 3, 3, 32

A = (30, 31, 32)
A_TAIL = (33, 34, 35)
B = (40, 41, 42)
B_TAIL = (43, 44, 45)
T2 = (31, 32, 33)  # A 的移位兄弟（短语 30..33 的错位 3-gram），天然出现 @1/@61
T1 = (41, 42, 43)  # B 的移位兄弟，天然出现 @17/@97
P1 = (50, 51, 52)  # 一次性表内 gram（诱饵合格落点 @40）
P1B = (53, 54, 55)  # 第二诱饵落点 @76
# 替换池（全部 ∉ 窗、∉ 家族、缝安全）；容量 > 处理源数+诱饵数，已用值禁不耗尽
POOL = [(52, 51, 50), (51, 52, 51), (53, 51, 52), (56, 57, 58), (58, 57, 56),
        (57, 58, 57), (59, 56, 58), (60, 61, 60), (62, 63, 62), (59, 63, 61)]

BASE_TABLE = {A: 1, B: 1, T1: 1, T2: 1, P1: 1, P1B: 1}
TABLE_PACKED = {dn.pack_gram(g, V_PACK): c for g, c in BASE_TABLE.items()}


def _filler(n: int) -> list[int]:
    return [(i * 7 + 13) % 30 for i in range(n)]


def _base_ids() -> list[int]:
    """128 token 窗（seg=32 → 4 段）：短语 (30..33) 源@0/重复@60 → 簇 {A,T2}；
    短语 (40..43) 源@16/重复@96 → 簇 {B,T1}；P1@40、P1B@76 一次性表内落点。"""
    ids = _filler(128)
    ids[0:3] = list(A)
    ids[3:6] = list(A_TAIL)
    ids[16:19] = list(B)
    ids[19:22] = list(B_TAIL)
    ids[40:43] = list(P1)
    ids[60:63] = list(A)
    ids[63:66] = list(A_TAIL)
    ids[76:79] = list(P1B)
    ids[96:99] = list(B)
    ids[99:102] = list(B_TAIL)
    return ids


def _select(ids: list[int]):
    occ = dn.cross_segment_occurrences(ids, N, SEG)
    rare, off = dn.select_rare_grams(occ, TABLE_PACKED, 1.0, V_PACK)
    sel, ov = dn.select_tail_positions(occ, rare, N, TAIL, len(ids))
    return occ, rare, sel


def _scan(seg: int = SEG) -> SimpleNamespace:
    return SimpleNamespace(ngram_len=N, tail=TAIL, segment_tokens=seg,
                           rare_quantile=1.0, strong_line=1.0, max_draws=64)


def _stub_forward(ids0: list[int], magic: tuple[tuple, ...], seg: int = SEG):
    """stub 前向（仪器级代数，非模型行为）：位置 t 的预测行 = logits[t-1]。
    magic gram 出现处的 T 个续尾位：当该 gram 最早出现处**内容仍在**（未被手术
    置换）且源在严格更早段 → 置信预测输入自身真值（NLL≈0）；否则均匀分布
    （NLL=lnV）。即「目标位当且仅当源 gram 内容在」的代数化——处理源被替换后
    其重复续尾塌到均匀，对照位（源不动+诱饵）两臂同为置信 ΔNLL≡0。置信 logit
    打在**当前输入序列**自身 token 上，诱饵换 token 不破坏置信。"""
    def forward(model, ids: list[int]) -> list:
        tk = len(ids)
        uniform: set[int] = set()
        for m in magic:
            first0 = dn.find_first(ids0, m)
            intact = ids[first0:first0 + N] == list(m)
            start = 0
            while True:
                i = -1
                for q in range(start, tk - N + 1):
                    if tuple(ids[q:q + N]) == m:
                        i = q
                        break
                if i == -1:
                    break
                if not (intact and first0 // seg < i // seg):
                    uniform.update(range(i + N, min(i + N + TAIL, tk)))
                start = i + 1
        logits = torch.zeros(1, tk, V_STUB)
        for j in range(tk - 1):
            if (j + 1) not in uniform:
                logits[0, j, ids[j + 1]] = 30.0
        lg = logits[0]
        out: list = [None]
        for t in range(1, tk):
            logp = torch.log_softmax(lg[t - 1].float(), dim=-1)
            out.append(float(-logp[ids[t]]))
        return out

    return forward


LN_V = math.log(V_STUB)


# --- 1. gram 打包 ------------------------------------------------------------


def test_pack_gram_roundtrip_and_order():
    for g in (A, B, T1, P1, (0, 0, 5), (63, 63, 63)):
        h = dn.pack_gram(g, V_PACK)
        assert dn.unpack_gram(h, len(g), V_PACK) == g
    # 同长度下打包保字典序（替换池按 (计数, 打包) 排序 = (计数, gram 字典序)）
    assert dn.pack_gram((30, 31, 32), V_PACK) < dn.pack_gram((30, 31, 33), V_PACK)
    assert dn.pack_gram((30, 63, 0), V_PACK) < dn.pack_gram((31, 0, 0), V_PACK)


# --- 2. 跨段扫描 -------------------------------------------------------------


def test_cross_segment_occurrences_segment_rule():
    ids = _filler(96)
    ids[0:3] = list(A)
    ids[20:23] = list(A)  # 同段（seg 0）重复 → 不计
    ids[70:73] = list(A)  # 严格更晚段（seg 2）→ 计
    occ = dn.cross_segment_occurrences(ids, N, SEG)
    assert occ.get(A) == [70]
    # filler（周期 30） gram (20,27,4) @1/31/61/91：首现 seg0，@31 同段不计，
    # @61/@81 严格更晚段计入——「同段重复不计」用真实数据再验一遍
    g = tuple(_filler(5)[1:4])
    assert g == (20, 27, 4)
    assert occ.get(g) == [61, 91]
    # 空窗/极短窗不炸
    assert dn.cross_segment_occurrences([1, 2], N, SEG) == {}


def test_select_rare_grams_quantile_off_table():
    g1, g2, g3 = (60, 61, 62), (61, 62, 60), (62, 60, 61)
    occ = {g1: [10], g2: [20], g3: [30]}
    table = {dn.pack_gram(g1, V_PACK): 5, dn.pack_gram(g2, V_PACK): 1}
    rare, off = dn.select_rare_grams(occ, table, 0.5, V_PACK)
    assert rare == {g2} and off == 1  # k=1：最稀有档；g3 表外诚实计数
    rare, off = dn.select_rare_grams(occ, table, 1.0, V_PACK)
    assert rare == {g1, g2} and off == 1
    # 平局按 (计数, gram) 稳定排序
    table2 = {dn.pack_gram(g1, V_PACK): 1, dn.pack_gram(g2, V_PACK): 1}
    rare, _ = dn.select_rare_grams(occ, table2, 0.5, V_PACK)
    assert rare == {g1}  # 同计数取 gram 字典序最小
    assert dn.select_rare_grams({}, table, 1.0, V_PACK) == (set(), 0)


def test_tail_positions_claim_and_overlap():
    occ = {A: [10, 40], B: [12]}
    sel, ov = dn.select_tail_positions(occ, {A, B}, N, TAIL, 64)
    # A(先到先认领) tails 13,14,15 与 43,44,45；B tails 15(被认领→重叠),16,17
    assert {13, 14, 15, 43, 44, 45, 16, 17} == set(sel)
    assert sel[15] == (A, 10) and sel[16] == (B, 12) and ov == 1


# --- 3. 红队域与源定位 ---------------------------------------------------------


def test_find_first_and_family_occurrence_spans_all():
    ids = _filler(50)
    ids[10:13] = list(A)
    ids[30:33] = list(A)
    assert dn.find_first(ids, A) == 10
    assert dn.find_first(ids, B) == -1
    # 红队条款域 = 家族**一切**出现区间（不止最早出现处）
    assert dn.family_occurrence_spans(ids, {A}, N) == [(10, 13), (30, 33)]


# --- 4. 簇级半分：移位兄弟永不跨半 ----------------------------------------------


def test_split_shifted_siblings_never_split():
    ids = _base_ids()
    _occ, rare, sel = _select(ids)
    assert rare == {A, T2, B, T1}
    # 移位家族源 span 重叠 → 同簇：{A,T2} 与 {B,T1}
    clusters = dn.build_source_clusters(sel, ids, N)
    assert sorted(sorted(c) for c in clusters) == [sorted([A, T2]), sorted([B, T1])]
    for seed in range(8):
        treat, ctrl, tcl, ccl = dn.split_selected_clusters(sel, ids, random.Random(seed), N)
        assert (A in treat) == (T2 in treat)  # 移位兄弟永不跨半
        assert (A in treat) != (B in treat)
        assert not (treat & ctrl) and (treat | ctrl) == frozenset({A, T2, B, T1})
        assert len(tcl) == 1 and len(ccl) == 1


# --- 5. 替换串挑选 -------------------------------------------------------------


def test_pick_replacement_bans_and_loud_exhaustion():
    ids = _base_ids()
    window_grams = {tuple(ids[p:p + N]) for p in range(len(ids) - N + 1)}
    families = {A, T2, B, T1}
    pool = [POOL[0], POOL[1], P1, A]  # P1 在窗内（回避）、A 是家族成员（禁）
    rng = random.Random(0)
    for _ in range(32):
        r = dn.pick_replacement(B, pool, rng, families, set(), ids, 40, N,
                                window_grams)
        assert r in (POOL[0], POOL[1])  # 家族禁 + 原串禁 + 窗内回避全生效
    # 禁尽 → 响亮，不静默回退
    with pytest.raises(ValueError, match="候选尽"):
        dn.pick_replacement(B, [A], random.Random(0), families, set(), ids, 40, N,
                            window_grams)
    with pytest.raises(ValueError, match="候选尽"):
        dn.pick_replacement(B, [POOL[0]], random.Random(0), families,
                            {POOL[0]}, ids, 40, N, window_grams)  # 已用值禁
    # 窗内回避：候选全在窗内时 max_draws 后如实接受最后一个合格抽样
    in_window_only = [P1]
    r = dn.pick_replacement(B, in_window_only, random.Random(0), families, set(),
                            ids, 40, N, window_grams, max_draws=8)
    assert r == P1  # P1 非家族非原串 → 抽满后如实接受（与 E122 同语义）


def test_pick_replacement_seam_family_rejected():
    buf = _filler(40)
    buf[20:23] = [60, 61, 62]
    f19 = buf[19]
    F1 = (f19, 61, 62)  # 把 R1=(61,62,63) 放进 @20 → 缝上 @19 处出现 F1
    families = {F1}
    window_grams = {tuple(buf[p:p + N]) for p in range(len(buf) - N + 1)}
    pool = [(61, 62, 63), POOL[0]]  # R1 直禁全过但缝禁被拒
    for seed in range(32):
        r = dn.pick_replacement((60, 61, 62), pool, random.Random(seed), families,
                                set(), buf, 20, N, window_grams)
        assert r == POOL[0]  # 缝上产生家族成员的候选永不被选中
    # 缝禁尽 → 响亮
    with pytest.raises(ValueError, match="候选尽"):
        dn.pick_replacement((60, 61, 62), [(61, 62, 63)], random.Random(0),
                            families, set(), buf, 20, N, window_grams)


# --- 6. 手术单确定性 -----------------------------------------------------------


def test_plan_deterministic_same_seed():
    ids = _base_ids()
    _occ, _rare, sel = _select(ids)
    kw = dict(treat_clusters=[frozenset([A, T2])], ctrl_clusters=[frozenset([B, T1])])
    p1 = dn.plan_window_surgery(ids, sel, frozenset({A, T2}), frozenset({B, T1}),
                                TABLE_PACKED, POOL, random.Random(11), N, TAIL,
                                V_PACK, **kw)
    p2 = dn.plan_window_surgery(ids, sel, frozenset({A, T2}), frozenset({B, T1}),
                                TABLE_PACKED, POOL, random.Random(11), N, TAIL,
                                V_PACK, **kw)
    assert p1.spans == p2.spans
    assert p1.decoys == p2.decoys
    assert p1.replacements == p2.replacements
    assert p1.n_source_overlap_skipped == p2.n_source_overlap_skipped
    assert p1.apply(ids) == p2.apply(ids)
    applied = p1.apply(ids)
    assert len(applied) == len(ids)  # token-for-token 等长替换：窗长不变
    # 计分位与对照源内容在术后窗原样
    assert applied[63:66] == list(A_TAIL) and applied[99:102] == list(B_TAIL)
    assert applied[16:19] == list(B)  # 对照源不动
    # 异种子计划仍合法（诱饵不压红队域、处理源整体灭活）
    for seed in (12, 13, 14):
        p3 = dn.plan_window_surgery(ids, sel, frozenset({A, T2}), frozenset({B, T1}),
                                    TABLE_PACKED, POOL, random.Random(seed), N, TAIL,
                                    V_PACK, **kw)
        fam = dn.family_occurrence_spans(ids, {A, T2, B, T1}, N)
        for d in p3.decoys:
            assert all(dn.span_gap((d["start"], d["end"]), fs) > 0 for fs in fam)
        ap3 = p3.apply(ids)
        assert ap3[0:3] != list(A) and ap3[1:4] != list(T2)  # 处理簇源灭活
    # run_window 端到端同种子逐位可复现
    stub = _stub_forward(ids, (A, T2, B, T1))
    r1 = dn.run_window(None, ids, _scan(), random.Random(5), TABLE_PACKED, POOL,
                       V_PACK, 0, forward_fn=stub)
    r2 = dn.run_window(None, ids, _scan(), random.Random(5), TABLE_PACKED, POOL,
                       V_PACK, 0, forward_fn=stub)
    assert json.dumps(r1["items"]) == json.dumps(r2["items"])


# --- 7. 诱饵域零压源对抗测试（E122 红队血训的第一天条款）------------------------


def test_decoy_domain_zero_press_adversarial():
    """移位兄弟源场景（老贪心 87.6% 压中的同款几何）：对照簇 {B,T1} 源锚 @16 的
    最近邻表内出现处全是压线 gram——T1@17（自身移位兄弟，span (17,20) 压 B 源
    (16,19)）、T2@1（别簇移位兄弟，span (1,4) 压 A 源 (0,3)）、家族重复出现处
    （A@60/A@0/B@96/T1@97/T2@61）。新仪器必须全部拒之域外，诱饵只落真正合格处
    （P1@40、P1B@76）；多种子 × 独立复算红队域双保险，压源即失败。"""
    ids = _base_ids()
    _occ, _rare, sel = _select(ids)
    fam_spans = dn.family_occurrence_spans(ids, {A, T2, B, T1}, N)  # 独立复算
    assert (17, 20) in fam_spans and (1, 4) in fam_spans  # 对抗构造确在域内
    for seed in range(8):
        plan = dn.plan_window_surgery(ids, sel, frozenset({A, T2}), frozenset({B, T1}),
                                      TABLE_PACKED, POOL, random.Random(seed), N,
                                      TAIL, V_PACK,
                                      treat_clusters=[frozenset([A, T2])],
                                      ctrl_clusters=[frozenset([B, T1])])
        assert plan.n_control_no_decoy == 0
        starts = sorted(d["start"] for d in plan.decoys)
        assert starts == [40, 76]  # 拒绝 @17/@1 等全部压线近邻，只落真合格处
        applied = plan.apply(ids)
        for d in plan.decoys:
            dspan = (d["start"], d["end"])
            # 双保险 1：计划自带审计距离
            assert d["gap_to_nearest_family_span"] > 0
            assert d["gap_to_nearest_source_span"] > 0
            assert d["gap_to_nearest_scoring_pos"] > 0
            # 双保险 2：独立复算红队域零压源
            assert all(dn.span_gap(dspan, fs) > 0 for fs in fam_spans)
            assert all(t not in sel for t in range(d["start"], d["end"]))
            # 诱饵落点处术后确为替换串、且替换串非家族成员
            assert tuple(applied[d["start"]:d["end"]]) == tuple(d["replacement"])
            assert tuple(d["replacement"]) not in {A, T2, B, T1}
        # 对照簇源内容原样（压源即毁对照——红队条款的存在理由）
        assert applied[16:22] == ids[16:22]
        # 处理簇源整体灭活、计分位真值原样
        assert applied[0:4] != ids[0:4]
        assert applied[63:66] == ids[63:66] and applied[99:102] == ids[99:102]


def test_decoy_adjacent_to_family_span_is_legal_not_press():
    """条款语义锁定（2026-09-11 远端首跑实证）：诱饵落点与家族出现区间**相邻**
    （gap=0 但不重叠）不违规——落点不毁任何家族内容即零压源（E122 `_overlaps`
    同款语义）；压线重叠才 RuntimeError。构造：唯一合格落点 P1@(93,96) 紧贴
    对照簇 B 重复出现区间 (96,99) 的左沿。"""
    ids = _base_ids()
    ids[40:43] = _filler(128)[40:43]  # 抹掉原 P1@40，让 @93 成唯一域外落点
    ids[93:96] = list(P1)  # 唯一合格落点，紧贴 B 重复 (96,99) 左沿
    table = {dn.pack_gram(g, V_PACK): 1 for g in (A, T2, B, T1, P1)}
    occ = dn.cross_segment_occurrences(ids, N, SEG)
    rare, _off = dn.select_rare_grams(occ, table, 1.0, V_PACK)
    sel, _ov = dn.select_tail_positions(occ, rare, N, TAIL, len(ids))
    fam_spans = dn.family_occurrence_spans(ids, {A, T2, B, T1}, N)
    assert (96, 99) in fam_spans  # 邻居确在红队域内
    assert all(dn.span_gap((93, 96), fs) >= 0 for fs in fam_spans)
    assert not dn._overlaps((93, 96), fam_spans)  # 相邻但不重叠 → 合格
    plan = dn.plan_window_surgery(ids, sel, frozenset({A, T2}), frozenset({B, T1}),
                                  table, POOL, random.Random(0), N, TAIL, V_PACK,
                                  treat_clusters=[frozenset([A, T2])],
                                  ctrl_clusters=[frozenset([B, T1])])
    assert [d["start"] for d in plan.decoys] == [93]  # 相邻落点合法 placement
    d = plan.decoys[0]
    assert d["gap_to_nearest_family_span"] == 0  # 相邻如实进审计距离字段
    assert d["gap_to_nearest_scoring_pos"] > 0  # 计分位仍不得压
    applied = plan.apply(ids)
    assert applied[96:99] == list(B)  # 家族内容原样（零压源本体）
    assert tuple(applied[93:96]) == tuple(d["replacement"])


def test_decoy_no_eligible_site_counts_honest():
    """诱饵合格域为空 → n_control_no_decoy 诚实计数（不虚设落点、不静默）。"""
    ids = _base_ids()
    table_small = {dn.pack_gram(g, V_PACK): 1 for g in (A, T2, B, T1)}  # 无域外表内 gram
    _occ, _rare, sel = _select(ids)
    plan = dn.plan_window_surgery(ids, sel, frozenset({A, T2}), frozenset({B, T1}),
                                  table_small, POOL, random.Random(0), N, TAIL,
                                  V_PACK,
                                  treat_clusters=[frozenset([A, T2])],
                                  ctrl_clusters=[frozenset([B, T1])])
    assert plan.decoys == [] and plan.n_control_no_decoy == 1
    applied = plan.apply(ids)
    assert applied[16:22] == ids[16:22]  # 对照源仍原样
    assert applied[0:4] != ids[0:4]  # 处理簇照常灭活


# --- 8. 全有或全无（保护区整簇跳过）---------------------------------------------


def test_all_or_nothing_protected_skip():
    """处理簇源压两半的重复出现处+续尾保护区（E122 同款）→ 整簇跳过：源不动、
    续尾位照常计分（如实稀释）、stub 代数下不虚报强命中。"""
    G = (45, 46, 47)
    seg = 16
    ids = _filler(96)
    ids[8:11] = list(B)   # B 源 @8（seg 0）
    ids[31:34] = list(B)  # B 重复 @31（seg 1）→ 保护区 (31,37)
    ids[34:37] = list(G)  # G 源 @34（seg 2）压保护区
    ids[50:53] = list(P1)  # 诱饵合格落点
    ids[70:73] = list(G)  # G 重复 @70（seg 4，跨段 ✓）
    table = {dn.pack_gram(g, V_PACK): 1 for g in (B, G, P1)}
    occ = dn.cross_segment_occurrences(ids, N, seg)
    rare, _off = dn.select_rare_grams(occ, table, 1.0, V_PACK)
    sel, _ov = dn.select_tail_positions(occ, rare, N, TAIL, len(ids))
    plan = dn.plan_window_surgery(ids, sel, frozenset({G}), frozenset({B}), table,
                                  POOL, random.Random(0), N, TAIL, V_PACK,
                                  treat_clusters=[frozenset({G})],
                                  ctrl_clusters=[frozenset({B})])
    assert plan.n_source_overlap_skipped == 1  # 整簇跳过
    assert G not in plan.replacements
    assert plan.apply(ids)[34:37] == list(G)  # 源不动
    stub = _stub_forward(ids, (G, B), seg=seg)
    rec = dn.run_window(None, ids, _scan(seg=seg), random.Random(0), table, POOL,
                        V_PACK, 0, forward_fn=stub,
                        split_override=(frozenset({G}), frozenset({B})))
    assert rec["status"] == "ok"
    s = rec["sums"]
    assert s["n_sel"] == 3  # G 续尾位照常计分（如实稀释）
    assert s["n_strong"] == 0  # 源未动 → 不虚报强命中
    assert all(abs(it["delta_b1"]) < 1e-6 for it in rec["items"])
    assert rec["counts"]["n_treatment_clusters_skipped"] == 1


# --- 9. ΔNLL 符号方向合成测试 ---------------------------------------------------


def test_delta_nll_sign_direction_stub():
    """合成冒烟（E122 预注册 §8.3 前置条件的 token 同构）：处理位 ΔNLL=lnV>0 且
    全强命中；对照位（源不动+等量诱饵）ΔNLL=0；主判读量对比>0 且 bootstrap CI
    不含 0。stub 前向代数：「目标位可预测当且仅当源 gram 内容在」。"""
    ids = _base_ids()
    stub = _stub_forward(ids, (A, T2, B, T1))
    rec = dn.run_window(None, ids, _scan(), random.Random(0), TABLE_PACKED, POOL,
                        V_PACK, 0, forward_fn=stub,
                        split_override=(frozenset({A, T2}), frozenset({B, T1})))
    assert rec["status"] == "ok"
    s = rec["sums"]
    sel_items = [it for it in rec["items"] if it["role"] == "selected"]
    ctl_items = [it for it in rec["items"] if it["role"] == "control"]
    assert {it["token_pos"] for it in sel_items} == {63, 64, 65, 66}
    assert {it["token_pos"] for it in ctl_items} == {99, 100, 101, 102}
    assert s["n_sel"] == 4 and s["n_ctl"] == 4
    for it in sel_items:  # 源灭活 → 续尾塌到均匀
        assert it["NLL_a"] < 1e-6
        assert abs(it["NLL_b1"] - LN_V) < 1e-6
        assert it["delta_b1"] == pytest.approx(LN_V, abs=1e-6)
        assert it["strong"] is True
    assert s["n_strong"] == 4
    for it in ctl_items:  # 对照源不动（诱饵在别处）→ 严格 0
        assert it["delta_b1"] == pytest.approx(0.0, abs=1e-6)
        assert it["decoy_start"] == 40  # 离簇源锚 @16 最近的合格落点
        assert it["decoy_n_spans"] == 2  # 簇级等量诱饵（P1@40 + P1B@76）
    # 审计字段：源 span / 家族域 / 诱饵距离全落盘且零违例
    audit = rec["audit"]
    assert audit["zero_press_violations"] == 0
    roles = {tuple(sp["gram"]): sp["role"] for sp in audit["source_spans"]}
    assert roles[A] == "treatment" and roles[T2] == "treatment"
    assert roles[B] == "control" and roles[T1] == "control"
    replaced = {tuple(sp["gram"]): sp["replaced"] for sp in audit["source_spans"]}
    assert replaced[A] and replaced[T2] and not replaced[B] and not replaced[T1]
    assert len(audit["decoy_landings"]) == 2
    assert all(d["gap_to_nearest_family_span"] > 0 for d in audit["decoy_landings"])
    # 主判读量代数：对比 = lnV − 0 > 0，单窗 bootstrap CI 即点估计（不含 0）
    assert s["sel_d_b1"] / s["n_sel"] == pytest.approx(LN_V, abs=1e-6)
    assert s["ctl_d_b1"] / s["n_ctl"] == pytest.approx(0.0, abs=1e-6)
    boot = dn.bootstrap_contrast([s], n_boot=200, seed=1)
    assert boot["point"] == pytest.approx(LN_V, abs=1e-6)
    assert boot["ci_excludes_zero"]
    # 极短窗 → empty 不炸
    assert dn.run_window(None, [1, 2], _scan(), random.Random(0), TABLE_PACKED,
                         POOL, V_PACK, 0, forward_fn=stub)["status"] == "empty"


# --- 10. bootstrap 可复现 + 判序 ------------------------------------------------


def test_bootstrap_reproducible_and_verdict():
    ws = [{"n_sel": 5, "sel_d_b1": 5.0 * i + 3.0, "n_ctl": 4, "ctl_d_b1": 0.1 * i}
          for i in range(20)]
    a = dn.bootstrap_contrast(ws, n_boot=500, seed=7)
    b = dn.bootstrap_contrast(ws, n_boot=500, seed=7)
    assert a == b  # 种子固定 → 逐分位可复现
    c = dn.bootstrap_contrast(ws, n_boot=500, seed=8)
    assert (a["ci95_lo"], a["ci95_hi"]) != (c["ci95_lo"], c["ci95_hi"])
    assert a["ci_excludes_zero"] and a["point"] > 0 and a["n_boot_valid"] == 500
    empty_ctl = [{"n_sel": 3, "sel_d_b1": 1.0, "n_ctl": 0, "ctl_d_b1": 0.0}]
    d = dn.bootstrap_contrast(empty_ctl, n_boot=50, seed=7)
    assert d["point"] is None and not d["ci_excludes_zero"]
    # 判序 CI 在先（E122 收官裁定同构）：噪声级读数不误入反常格
    assert "剂量未落" in dn.verdict(0.01, {"point": 0.01, "ci_excludes_zero": False})
    assert "反常" in dn.verdict(0.01, {"point": -0.2, "ci_excludes_zero": True})
    assert "强" in dn.verdict(1.2, {"point": 1.1, "ci_excludes_zero": True})
    assert "弱" in dn.verdict(0.4, {"point": 0.3, "ci_excludes_zero": True})
    assert dn.verdict(None, {"point": None, "ci_excludes_zero": False}) == "无读数"
