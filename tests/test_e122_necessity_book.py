"""E122 跨段必要性账仪器单测（冻结预注册 v1.0 2026-09-06:
docs/versions/v3_7/FLUED_V3_7_E122_CROSSSEG_NECESSITY_20260906_CN.md; 仪器在
tools/analysis/v3_6/probe_e122_necessity_book.py）。

Covers: (1) b1 替换三匹配（长度/UTF-8 续字节结构/稀有表内）+ 候选域空响亮报错;
(2) 分段漂移「重映射续计分」语义（裁定 2026-09-06: 整窗剔除废止——术后新格位
取数对拍 + drifted 标记）; (3) d 格累积网格
字节位→(chunk,slot) 映射代数（与 make_cumulative_retention_targets 对拍 +
追加召回槽只装遮蔽字节的完备性）; (4) 坑 8 全键断言 loud fail; (5) 扫描器与
密度账同源 import 断言; (6) v1.2 同体半分手术统计匹配（同三匹配约束 + 两半
保护区 + 对照源不动 + 诱饵最近合格）+ 半分确定性/均衡性; (7)
bootstrap 可复现（种子固定）; (8) 逐位 NLL 无梯度图 + fp32; (9) b2 行置换
（行存在性保留、源行只取非源行）; (10) 选择图与 D1 _d1_build_weight_map 同
语义对拍（合成窗）; (11) 合成冒烟: 目标位确需源 gram 的窗上处理位 b1
ΔNLL=ln(258)>0 且对照位（源不动+诱饵）ΔNLL=0（stub 前向代数对拍, 不依赖
语料/GPU/checkpoint）; (12) b2 源 chunk 内计分位剔除标记（对角自读污染,
裁定 2026-09-06; v1.2 起行手术只处置处理半源 chunk, split_override 钉死分组）。
"""

from __future__ import annotations

import math
import random
from types import SimpleNamespace

import pytest
import torch

import tools.analysis.v3_6.probe_e122_necessity_book as e122
import tools.analysis.v3_6.demand_density_book as ddb
import tools.train.v3_6.train_v36_s1 as s1
from flued.data import MASK_ID

LN_VOCAB = math.log(258)


@pytest.fixture(autouse=True)
def _reset_d1_table():
    yield
    s1._D1_RARE_TABLE = None


def _synth_grid(t: int, chunk: int = 16):
    idx = torch.arange(t)
    return idx.view(1, -1) // chunk, idx.view(1, -1) % chunk


def _counter_filler(n: int) -> bytearray:
    # 7 与 256 互素 → 未修补区每个 6-gram 唯一（不污染选择图）
    return bytearray((i * 7 + 13) % 256 for i in range(n))


# --- 1. b1 替换三匹配 -------------------------------------------------------------


def test_pick_replacement_three_matches():
    g = b"ab\xbf\xbecd"  # 图案 F F T T F F
    c1 = b"xy\x80\x80zw"  # 同长度同图案、表内
    c2 = b"qr\x80\x81zw"  # 同长度同图案、表内
    other_pattern = b"\xbf" * 6  # 同长度但图案不同——不许被选中
    table = {g: 0, c1: 1, c2: 2, other_pattern: 3}
    idx = e122.build_pattern_index(table)
    rng = random.Random(0)
    for _ in range(32):
        r = e122.pick_replacement(g, idx, rng)
        assert len(r) == len(g)  # 匹配一: 长度
        assert e122.continuation_pattern(r) == e122.continuation_pattern(g)  # 匹配二: 续位图案
        assert r in table and r != g  # 匹配三: 表内且非原串
        assert r != other_pattern
    # 窗内回避: c1 已在窗内时不再被抽中（另有同图案候选可用）
    window = b"...." + c1 + b"...."
    for _ in range(32):
        assert e122.pick_replacement(g, idx, rng, window=window) != c1
    # 禁集耗尽 → 响亮报错
    with pytest.raises(ValueError, match="候选"):
        e122.pick_replacement(g, idx, rng, forbidden=frozenset({c1, c2}))
    # 表内同图案只有原串自己 → 候选域空响亮报错
    lonely = e122.build_pattern_index({g: 0, other_pattern: 1})
    with pytest.raises(ValueError, match="候选"):
        e122.pick_replacement(g, lonely, rng)


# --- 2. 分段漂移剔除 ---------------------------------------------------------------


def test_drifted_positions_bit_level():
    ca, oa = _synth_grid(64)
    cb, ob = ca.clone(), oa.clone()
    assert e122.drifted_positions(ca, oa, cb, ob, [0, 17, 63]) == []
    cb[0, 40:] += 1  # 位 40 起上游分段漂移
    assert e122.drifted_positions(ca, oa, cb, ob, [0, 17]) == []  # 上游位不受影响
    assert e122.drifted_positions(ca, oa, cb, ob, [41, 63]) == [41, 63]
    ob2 = oa.clone()
    ob2[0, 33] += 1  # 槽位漂移同样算数
    assert e122.drifted_positions(ca, oa, cb, ob2, [33]) == [33]


class _StubChunks:
    def __init__(self, t: int, chunk: int = 16, shift_from: int | None = None):
        idx = torch.arange(t)
        self.chunk_ids = idx.view(1, -1) // chunk
        if shift_from is not None:
            self.chunk_ids = self.chunk_ids + (idx.view(1, -1) >= shift_from).long()
        self.offsets = idx.view(1, -1) % chunk
        self.chunk_mask = torch.ones(1, t, dtype=torch.bool)
        self.token_mask = self.chunk_mask


def _smoke_window():
    """合成窗（代数对拍用）：magic gram g/h 的最早出现（chunk 0/1）续尾字节 ==
    严格更晚 chunk 重复出现（chunk 4/6）续尾字节——目标位「确需源 gram」。
    u 为表内但窗内仅一次出现（无重复 → 无选中位，专供对照手术落点）。
    g2/h2/u2 为同长度同续位图案的表内替换候选。"""
    raw = _counter_filler(128)
    g, h, u = bytes([10] * 6), bytes([11] * 6), bytes([12] * 6)
    g2, h2, u2 = bytes([13] * 6), bytes([14] * 6), bytes([15] * 6)
    raw[0:6] = g
    raw[6:9] = b"\x20\x21\x22"  # g 首现续尾
    raw[16:22] = h
    raw[22:25] = b"\x30\x31\x32"  # h 首现续尾
    raw[40:46] = u
    raw[64:70] = g
    raw[70:73] = b"\x20\x21\x22"  # g 重复出现续尾（选中位 70-72）
    raw[96:102] = h
    raw[102:105] = b"\x30\x31\x32"  # h 重复出现续尾（选中位 102-104）
    return bytes(raw), {g: 0, h: 1, u: 2, g2: 3, h2: 4, u2: 5}


def _stub_forward(raw0: bytes, magic: tuple[bytes, ...] = (), L: int = 6,
                  chunk: int = 16, drift_from: int | None = None,
                  confident_all: bool = False):
    """stub 前向（仪器级代数, 非模型行为）：
    - 默认：非 magic 出现处续尾的位置 → 置信预测 clean 真值（两臂逐位同 →
      ΔNLL=0）; magic gram 出现处的 T 个续尾位：当该 gram 更早 chunk 的源出现
      处**内容仍在**（未被手术置换）→ 置信预测源出现处对应续尾（= 目标真值,
      NLL≈0）; 否则均匀分布（NLL=ln258）。即「目标位当且仅当源 gram 内容在」
      的代数化——b1 替换源后选中位（全部 T 个续尾）塌到均匀, 对照位（非续尾）
      两臂同为置信, ΔNLL 恒 0。
    - confident_all=True：全部位置置信（配 drift_from 用, 专测术后格位取数）。
    置信 logit 恒打在 stub 自己返回网格的 (chunk_ids[t], offsets[t]) 上——术后
    分段漂移时即新格位; 探针若错读术前格位会拿到全零 logits（NLL=ln258）。"""

    def forward(model, source, ns):
        raw = bytes(int(x) - 1 for x in source[0].tolist())
        t_len = len(raw)
        chunks = _StubChunks(t_len, chunk, drift_from if raw != raw0 else None)
        c_max = int(chunks.chunk_ids.max()) + 1
        s_max = int(chunks.offsets.max()) + 1
        logits = torch.zeros(1, c_max, s_max, 258)
        uniform = set()  # 均匀分布位（源内容不在的续尾位）
        if not confident_all:
            for m in magic:
                first0 = raw0.find(m)
                occs = []
                pos = 0
                while True:
                    i = raw.find(m, pos)
                    if i == -1:
                        break
                    occs.append(i)
                    pos = i + 1
                intact = raw[first0 : first0 + len(m)] == raw0[first0 : first0 + len(m)]
                for p in occs:
                    if not (intact and first0 // chunk < p // chunk):
                        uniform.update(range(p + L, min(p + L + 3, t_len)))
        for t in range(t_len):
            tgt = raw0[t] + 1
            c = int(chunks.chunk_ids[0, t])  # stub 自己的术后网格坐标
            sl = int(chunks.offsets[0, t])
            if t not in uniform:
                logits[0, c, sl, tgt] = 30.0
        # b2 读数面=backbone（探针裁定 2026-09-06：direct 面对非源 chunk 行手术
        # 恒等 0）——stub 同张量充当两面（confident_all 下 ΔNLL_b2≡0 符合预期）
        return {"logits_direct": logits, "logits_backbone": logits, "chunks": chunks}

    return forward


@pytest.mark.parametrize("seed", [0, 1, 2, 3])
def test_algebra_smoke_stub_b1_positive_control_zero(seed):
    """合成冒烟（预注册 §8.3 前置条件 + v1.2 同体半分）：处理位 ΔNLL_b1=ln258>0
    且对照位（源不动+诱饵替换）ΔNLL_b1=0 的代数对拍。"""
    raw0, table = _smoke_window()
    idx = e122.build_pattern_index(table)
    clean = torch.tensor([[b + 1 for b in raw0]], dtype=torch.long)
    zero_mask = torch.zeros(1, len(raw0), dtype=torch.bool)
    ns = SimpleNamespace(max_chunks=8, max_span=16)
    scan = SimpleNamespace(ngram_len=6, tail=3, rare_quantile=1.0, strong_line=1.0)
    fwd = _stub_forward(raw0, (bytes([10] * 6), bytes([11] * 6)))
    rec = e122.run_window(
        model=None, ns=ns, clean_ids=clean, byte_mask=zero_mask, table=table,
        scan=scan, arms={"a", "b1"}, rng=random.Random(seed), pattern_index=idx,
        window_id=0, forward_fn=fwd,
    )
    assert rec["status"] == "ok"
    s = rec["sums"]
    sel_items = [it for it in rec["items"] if it["role"] == "selected"]
    ctl_items = [it for it in rec["items"] if it["role"] == "control"]
    # v1.2 半分: g/h 一处理一对照 → 3+3, 并集不变
    assert {it["byte_pos"] for it in sel_items + ctl_items} == {70, 71, 72, 102, 103, 104}
    assert s["n_sel"] == 3 and s["n_ctl"] == 3
    assert s["n_strong"] == 3  # 处理半 3 位全强命中
    assert len(rec["split"]["treatment_clusters"]) == 1
    assert len(rec["split"]["control_clusters"]) == 1
    for it in sel_items:
        assert it["NLL_a"] < 1e-6
        assert abs(it["NLL_b1"] - LN_VOCAB) < 1e-6
        assert it["delta_b1"] == pytest.approx(LN_VOCAB, abs=1e-6)
    for it in ctl_items:
        assert it["delta_b1"] == 0.0  # 对照源不动（诱饵=u@40 非 magic）→ 严格 0
        assert it["decoy_gram"] == bytes([12] * 6).hex()  # 唯一合格诱饵 u@40
        assert it["decoy_pos"] == 40
    assert s["ctl_d_b1"] == 0.0
    # 主判读量代数: 对比 = ln258 - 0 > 0
    assert s["sel_d_b1"] / s["n_sel"] == pytest.approx(LN_VOCAB, abs=1e-6)


def test_drift_remap_scores_at_post_grid():
    """漂移门（裁定 2026-09-06：重映射续计分, 整窗剔除废止）：分段漂移窗不剔除,
    逐位 drifted 标记正确, 且 NLL 在**术后新格位**取数——置信 logit 打在 stub
    术后网格坐标上, 探针若错读术前格位会拿到全零 logits（NLL=ln258）。"""
    raw0, table = _smoke_window()
    idx = e122.build_pattern_index(table)
    clean = torch.tensor([[b + 1 for b in raw0]], dtype=torch.long)
    zero_mask = torch.zeros(1, len(raw0), dtype=torch.bool)
    ns = SimpleNamespace(max_chunks=16, max_span=16)
    scan = SimpleNamespace(ngram_len=6, tail=3, rare_quantile=1.0, strong_line=1.0)
    fwd = _stub_forward(raw0, confident_all=True, drift_from=40)
    rec = e122.run_window(
        model=None, ns=ns, clean_ids=clean, byte_mask=zero_mask, table=table,
        scan=scan, arms={"a", "b1"}, rng=random.Random(0), pattern_index=idx,
        window_id=0, forward_fn=fwd,
    )
    assert rec["status"] == "ok"  # 不再整窗剔除
    assert rec["items"]
    by_pos = {it["byte_pos"]: it for it in rec["items"]}
    assert 70 in by_pos and 102 in by_pos  # 选中位照常计分
    for it in rec["items"]:
        t = it["byte_pos"]
        assert it["drifted"] is (t >= 40)  # 位 40 起 chunk_ids +1 → 格位变化
        assert it["NLL_b1"] < 1e-6  # 术后格位上的置信读数（错格位 = ln258）
        assert it["delta_b1"] == pytest.approx(0.0, abs=1e-6)
    # 分层和: 本窗全部计分位 drifted, 全部进 drifted 层
    s = rec["sums"]
    assert s["n_sel_drift"] == s["n_sel"] and s["n_sel_nodrift"] == 0
    assert s["n_ctl_drift"] == s["n_ctl"] and s["n_ctl_nodrift"] == 0


def test_b2_own_chunk_exclusion_flagged():
    """b2 污染剔除（裁定 2026-09-06）× v1.2 半分：行手术只处置**处理半**源
    chunk。split_override 钉死 h 为处理（源 @41-46 落 chunk 2）→ g（对照）续尾
    38-40 在被置换 chunk 2 内 = 剔除, h 续尾 78-80（chunk 4）保留, b1 照常计。"""
    raw = _counter_filler(96)
    g, h, u = bytes([10] * 6), bytes([11] * 6), bytes([12] * 6)
    g2, h2, u2 = bytes([13] * 6), bytes([14] * 6), bytes([15] * 6)
    raw[0:6] = g
    raw[6:9] = b"\x20\x21\x22"       # g 首现续尾（chunk 0）
    raw[16:22] = bytes([9] * 6)      # 一次性非表内 gram 占位（无重复 → 无选中位）
    raw[32:38] = g                   # g 重复（chunk 2）
    raw[38:41] = b"\x20\x21\x22"     # g 续尾 38-40 → chunk 2
    raw[41:47] = h                   # h 首现（chunk 2）
    raw[47:50] = b"\x30\x31\x32"     # h 首现续尾
    raw[56:62] = u                   # 诱饵手术落点（chunk 3, 无重复）
    raw[72:78] = h                   # h 重复（chunk 4）
    raw[78:81] = b"\x30\x31\x32"     # h 续尾 78-80 → chunk 4
    raw0 = bytes(raw)
    table = {g: 0, h: 1, u: 2, g2: 3, h2: 4, u2: 5}
    idx = e122.build_pattern_index(table)
    clean = torch.tensor([[b + 1 for b in raw0]], dtype=torch.long)
    zero_mask = torch.zeros(1, len(raw0), dtype=torch.bool)
    ns = SimpleNamespace(max_chunks=8, max_span=16)
    scan = SimpleNamespace(ngram_len=6, tail=3, rare_quantile=1.0, strong_line=1.0)

    class _PatchableModel:
        def _slm_store_rows(self, chunks, with_views=False):
            r = torch.zeros(1, 6, 4)
            if with_views:
                return r, r, torch.zeros(()), r, r, None, None
            return r, r, torch.zeros(()), r, r

    fwd = _stub_forward(raw0, confident_all=True)
    rec = e122.run_window(
        model=_PatchableModel(), ns=ns, clean_ids=clean, byte_mask=zero_mask,
        table=table, scan=scan, arms={"a", "b1", "b2"}, rng=random.Random(0),
        pattern_index=idx, window_id=0, forward_fn=fwd,
        split_override=(frozenset({h}), frozenset({g})),  # 钉死: h 处理 / g 对照
    )
    assert rec["status"] == "ok"
    by_pos = {it["byte_pos"]: it for it in rec["items"]}
    assert {it["byte_pos"] for it in rec["items"] if it["role"] == "selected"} == {78, 79, 80}
    assert {it["byte_pos"] for it in rec["items"] if it["role"] == "control"} == {38, 39, 40}
    for t in (38, 39, 40):  # 对照 g 续尾在被置换源 chunk 2 内 → b2 剔除, b1 照常
        it = by_pos[t]
        assert it["b2_own_chunk_excluded"] is True
        assert it["NLL_b2"] is None and it["delta_b2"] is None
        assert it["NLL_b1"] is not None and it["delta_b1"] is not None
    for t in (78, 79, 80):  # 处理 h 续尾在 chunk 4（未置换）→ b2 保留
        it = by_pos[t]
        assert it["b2_own_chunk_excluded"] is False
        assert it["NLL_b2"] is not None
    assert rec["counts"]["n_b2_own_chunk_control"] == 3
    assert rec["counts"]["n_b2_own_chunk_selected"] == 0
    # 对照 g 的诱饵 = u@56（唯一非选中表内 gram 出现处）；源 g@0 保持不动
    assert by_pos[38]["decoy_gram"] == u.hex() and by_pos[38]["decoy_pos"] == 56
    s = rec["sums"]
    assert s["n_sel"] == 3 and s["n_ctl"] == 3
    assert s["n_sel_b2"] == 3 and s["n_ctl_b2"] == 0  # 只有处理 h 续尾进 b2 分层
    assert s["n_strong"] == 0  # confident_all stub: 两臂同为置信 → ΔNLL≡0（本测只验剔除标记）


# --- 3. d 格累积网格映射代数 ---------------------------------------------------------


def test_byte_to_grid_slots_matches_cumulative_grid():
    # T=70 → row 4 为部分行（6 字节）：遮蔽字节的追加召回槽只有落进部分行才装得下
    t, c_max, s_max = 70, 8, 16
    clean = torch.randint(1, 257, (1, t))
    mask = torch.zeros(1, t, dtype=torch.bool)
    mask[0, 33] = True
    mask[0, 34] = True  # chunk 2 内两个遮蔽字节
    chunk_ids, offsets = _synth_grid(t)
    c_map, s_map, valid = e122.byte_to_grid_slots(chunk_ids, offsets, mask, c_max, s_max)
    source = clean.masked_fill(mask, MASK_ID)
    enc_t, enc_slot, _enc_masked, trunc = s1.make_cumulative_retention_targets(
        source, mask, chunk_ids, offsets, c_max, s_max
    )
    # 追加召回槽: row 3（满行, 自身 16 槽占满）装不下 → 计截断; row 4（部分行）
    # 装得下 → 2 个召回槽成真
    assert int(trunc) == 2
    own = set()
    for b in range(t):
        c, sl = int(c_map[0, b]), int(s_map[0, b])
        # 自身槽对拍: 累积格在该槽的 as-encoded 靶 == 该字节源 id, 且计分
        assert enc_t[0, c, sl] == source[0, b]
        assert bool(enc_slot[0, c, sl])
        # valid = 网格内且非 mask 命中
        assert bool(valid[0, b]) == (not bool(mask[0, b]))
        own.add((c, sl))
    # 完备性: 累积格每个计分槽要么是某合法字节的自身槽, 要么是遮蔽字节的追加
    # 召回槽（靶 = MASK_ID）→ 剔除 mask 命中后自身槽计分即穷尽未遮蔽字节
    for c in range(c_max):
        for sl in range(s_max):
            if bool(enc_slot[0, c, sl]):
                assert (c, sl) in own or enc_t[0, c, sl] == MASK_ID
    # 追加召回槽真实存在（row > 源 chunk 才有, 且只装遮蔽字节）
    recalled = [
        (c, sl) for c in range(c_max) for sl in range(s_max)
        if bool(enc_slot[0, c, sl]) and (c, sl) not in own
    ]
    assert recalled, "累积格语义下遮蔽字节必须有追加召回槽"
    assert all(enc_t[0, c, sl] == MASK_ID for c, sl in recalled)


# --- 4. 坑 8 全键断言 ---------------------------------------------------------------


def test_cell_keys_loud_fail():
    good = dict(
        seed_source="k", k_row_source="state", v_row_source="state",
        summarizer_pool="qpool", backbone_mode="slm",
    )
    e122.assert_cell_keys(SimpleNamespace(**good))  # 全对 → 通过
    e122.assert_cell_keys(SimpleNamespace(**good), SimpleNamespace(**good))
    # 缺键（build_model 会兜底默认——正是要拦的静默漂移）
    missing = {k: v for k, v in good.items() if k != "seed_source"}
    with pytest.raises(ValueError, match="seed_source"):
        e122.assert_cell_keys(SimpleNamespace(**missing))
    with pytest.raises(ValueError, match="键缺失"):
        e122.assert_cell_keys(SimpleNamespace(**missing))
    # 错值（兜底默认值混进 resolved_config 的同款形态）
    with pytest.raises(ValueError, match="summarizer_pool"):
        e122.assert_cell_keys(SimpleNamespace(**{**good, "summarizer_pool": "mean"}))
    with pytest.raises(ValueError, match="v_row_source"):
        e122.assert_cell_keys(SimpleNamespace(**{**good, "v_row_source": "memory"}))
    # 装载后 model.config 二次断言同样响亮
    with pytest.raises(ValueError, match="model\\.config"):
        e122.assert_cell_keys(SimpleNamespace(**good), SimpleNamespace(**{**good, "seed_source": "v"}))


# --- 5. 扫描器同源 import -----------------------------------------------------------


def test_scanner_same_source_import():
    assert e122.cross_chunk_occurrences is ddb.cross_chunk_occurrences  # 密度账同源
    assert e122.s1 is s1  # 选择档/表装载/mask 纪律 = D1 训练器同模块对象
    # 行为同源抽查: 同窗扫描逐位一致
    win = bytes(_counter_filler(256))
    assert e122.cross_chunk_occurrences(win, 6).keys() == ddb.cross_chunk_occurrences(win, 6).keys()


# --- 6. 半分手术统计匹配（v1.3a 簇级） -------------------------------------------------


def _cluster_window():
    """簇级构造窗：7 字节短语 P 在 0/64 两处出现 → 移位 gram 家族 p0g=P[0:6]、
    p1g=P[1:7] 源 span (0,6)/(1,7) 重叠成簇；q 在 16/96 两处 = 独立簇；
    r1@40 一次性表内 gram（诱饵合格域）。"""
    raw = _counter_filler(128)
    p0g = bytes([21, 22, 23, 24, 25, 26])
    p1g = bytes([22, 23, 24, 25, 26, 27])
    q = bytes([31] * 6)
    r1, r2, r3 = bytes([41] * 6), bytes([42] * 6), bytes([43] * 6)
    raw[0:7] = p0g + bytes([27])   # p0g@0, p1g@1（chunk 0）
    raw[64:71] = p0g + bytes([27])  # 重复（chunk 4）→ 跨 chunk 选中
    raw[16:22] = q
    raw[96:102] = q                # q 重复（chunk 6）
    raw[40:46] = r1                # 一次性 → 不选中，诱饵候选
    r4, r5 = bytes([44] * 6), bytes([45] * 6)  # 同图案桶扩充（禁集耗尽防）
    table = {p0g: 0, p1g: 1, q: 2, r1: 3, r2: 4, r3: 5, r4: 6, r5: 7}
    return bytes(raw), table, (p0g, p1g, q, r1)


def test_split_clusters_deterministic_balanced():
    """v1.3a 簇级半分：源 span 重叠链并簇（移位家族同簇、永不跨半），簇间洗牌
    对半、同种子可复现。"""
    raw, table, (p0g, p1g, q, _r1) = _cluster_window()
    occ = e122.cross_chunk_occurrences(raw, 6)
    rare, _off = s1._d1_select_rare_grams(occ, table, 1.0)
    sel, _ov = e122.select_tail_positions(occ, rare, 6, 3, len(raw))
    assert {g for g, _p in sel.values()} == {p0g, p1g, q}
    clusters = e122.build_source_clusters(sel, raw, 6)
    assert sorted(sorted(c) for c in clusters) == sorted([sorted([p0g, p1g]), sorted([q])])
    t1, c1, tcl1, ccl1 = e122.split_selected_clusters(sel, raw, random.Random(42), 6)
    t2, c2, _, _ = e122.split_selected_clusters(sel, raw, random.Random(42), 6)
    assert t1 == t2 and c1 == c2  # 同种子同分组（可复现）
    assert not (t1 & c1) and (t1 | c1) == frozenset({p0g, p1g, q})
    assert len(tcl1) == 1 and len(ccl1) == 1  # 簇级对半
    for seed in range(8):  # 簇完整性：移位家族永不跨半
        tt, cc, _, _ = e122.split_selected_clusters(sel, raw, random.Random(seed), 6)
        assert (p0g in tt) == (p1g in tt)
        assert (q in tt) != (p0g in tt)


def test_cluster_surgery_union_coverage_and_all_or_nothing():
    """v1.3a 处理簇联合替换：移位家族全体成员源 span 都被替换（短语源整体灭活，
    接缝后写覆盖）；任一成员压保护区 → 整簇跳过（全有或全无）；对照簇源不动、
    等量诱饵在最近合格处。"""
    raw, table, (p0g, p1g, q, r1) = _cluster_window()
    idx = e122.build_pattern_index(table)
    occ = e122.cross_chunk_occurrences(raw, 6)
    rare, _off = s1._d1_select_rare_grams(occ, table, 1.0)
    sel, _ov = e122.select_tail_positions(occ, rare, 6, 3, len(raw))
    plan = e122.plan_window_surgery(
        raw, rare, sel, frozenset({p0g, p1g}), frozenset({q}), table, idx,
        random.Random(0), 6, 3,
        treat_clusters=[frozenset({p0g, p1g})], ctrl_clusters=[frozenset({q})],
    )
    applied = plan.apply(raw)
    # 接缝语义（后写覆盖）：p0g 替换只剩首字节，p1g 替换整体在位 → union 全覆盖
    assert applied[0:1] == plan.replacements[p0g][0:1]
    assert applied[1:7] == plan.replacements[p1g]
    assert applied[0:7] != raw[0:7]  # 短语源整体灭活
    assert plan.n_source_overlap_skipped == 0
    assert applied[16:22] == q  # 对照源不动
    # 对照簇 1 成员 → 1 处诱饵 = 唯一合格出现处 r1@40
    assert plan.decoy_span.get(q) is not None and len(plan.decoy_span[q]) == 1
    g2, p2, _r = plan.spans[plan.decoy_span[q][0]]
    assert g2 == r1 and p2 == 40
    # 全有或全无：构造 B 簇源压 A 簇重复保护区 → 整簇跳过
    raw2 = _counter_filler(128)
    a, b = bytes([51] * 6), bytes([52] * 6)
    raw2[0:6] = a
    raw2[64:70] = a              # A 重复（chunk 4）→ 保护区 (64,73)
    raw2[70:76] = b              # B 源 (70,76) 压 A 保护区 [70,73) 但不毁 A 本体
    raw2[96:102] = b             # B 重复（chunk 6）
    raw2 = bytes(raw2)
    table2 = {**table, a: 8, b: 9}  # 沿用簇窗大桶（禁集耗尽防）
    occ2 = e122.cross_chunk_occurrences(raw2, 6)
    rare2, _ = s1._d1_select_rare_grams(occ2, table2, 1.0)
    sel2, _ov2 = e122.select_tail_positions(occ2, rare2, 6, 3, len(raw2))
    assert {g for g, _p in sel2.values()} == {a, b}
    plan2 = e122.plan_window_surgery(
        raw2, rare2, sel2, frozenset({b}), frozenset({a}), table2, idx,
        random.Random(0), 6, 3,
        treat_clusters=[frozenset({b})], ctrl_clusters=[frozenset({a})],
    )
    assert plan2.n_source_overlap_skipped == 1  # B 簇整簇跳过
    assert b not in plan2.replacements
    assert plan2.apply(raw2)[70:76] == b  # 未动


def test_split_half_surgery_stats_matched():
    """v1.3a 簇级同体半分手术单（用户裁定 2026-09-06）：处理簇源联合替换+对照
    簇等量诱饵同三匹配同保护；对照源保持不动；诱饵=离簇源锚最近合格非选中
    表内出现处。"""
    raw0, table = _smoke_window()
    idx = e122.build_pattern_index(table)
    occ = e122.cross_chunk_occurrences(raw0, 6)
    rare, _off = s1._d1_select_rare_grams(occ, table, 1.0)
    sel, _ov = e122.select_tail_positions(occ, rare, 6, 3, len(raw0))
    n = len(raw0)
    protected = [(p, min(p + 6 + 3, n)) for _g, p in set(sel.values())]
    treat, ctrl, tcl, ccl = e122.split_selected_clusters(sel, raw0, random.Random(0), 6)
    plan = e122.plan_window_surgery(raw0, rare, sel, treat, ctrl, table, idx,
                                    random.Random(0), 6, 3,
                                    treat_clusters=tcl, ctrl_clusters=ccl)
    # 全部替换（处理源 + 诱饵）同三匹配
    for g0, p0, r in plan.spans:
        assert len(r) == len(g0)
        assert e122.continuation_pattern(r) == e122.continuation_pattern(g0)
        assert r in table and r != g0
        assert raw0[p0:p0 + len(g0)] == g0
        assert plan.apply(raw0)[p0:p0 + len(r)] == r  # 应用后该处确实是替换串
    # 全部 span 不压保护区（两半的重复出现处+续尾，处理源与诱饵同受约束）
    for g0, p0, _r in plan.spans:
        lo, hi = p0, p0 + len(g0)
        assert not any(lo < ph and pl < hi for pl, ph in protected)
    applied = plan.apply(raw0)
    # 处理簇：全体成员源被替换（全有或全无）
    for c in tcl:
        replaced = [g for g in c if g in plan.replacements]
        assert not replaced or len(replaced) == len(c)
        for g in replaced:
            p0 = raw0.find(g)
            assert applied[p0:p0 + 6] == plan.replacements[g]
    # 对照簇：源不动、诱饵数=簇成员数、诱饵非任何选中串
    assert plan.decoy_span and set(plan.decoy_span) <= set(ctrl)
    sel_originals = {gg for gg, _p in sel.values()}
    for g, sis in plan.decoy_span.items():
        p0 = raw0.find(g)
        assert applied[p0:p0 + 6] == g  # 对照源不动
        cluster_of_g = next(c for c in ccl if g in c)
        assert len(sis) == len(cluster_of_g)  # 等量诱饵
        for si in sis:
            g2, _p2, _r = plan.spans[si]
            assert g2 not in sel_originals
    # 合成窗唯一合格诱饵 = u@40
    for g, sis in plan.decoy_span.items():
        assert all(plan.spans[si][0] == bytes([12] * 6) and plan.spans[si][1] == 40
                   for si in sis)
    # 手术不改变窗长
    assert len(applied) == n
    # 同串多出现共用一个替换 gram（记录在 replacements）
    for g0, _p0, r in plan.spans:
        assert plan.replacements[g0] == r


# --- 7. bootstrap 可复现 -------------------------------------------------------------


def test_bootstrap_reproducible():
    ws = [
        {"n_sel": 5, "sel_d_b1": 5.0 * i + 3.0, "n_ctl": 4, "ctl_d_b1": 0.1 * i}
        for i in range(20)
    ]
    a = e122.bootstrap_contrast(ws, n_boot=500, seed=7)
    b = e122.bootstrap_contrast(ws, n_boot=500, seed=7)
    assert a == b  # 种子固定 → 逐分位可复现
    c = e122.bootstrap_contrast(ws, n_boot=500, seed=8)
    assert (a["ci95_lo"], a["ci95_hi"]) != (c["ci95_lo"], c["ci95_hi"])  # 异种子异流
    assert a["ci_excludes_zero"] and a["point"] > 0
    assert a["n_boot_valid"] == 500
    # 对照侧空窗全占时 contrast 无定义 → 不虚报 CI
    empty_ctl = [{"n_sel": 3, "sel_d_b1": 1.0, "n_ctl": 0, "ctl_d_b1": 0.0}]
    d = e122.bootstrap_contrast(empty_ctl, n_boot=50, seed=7)
    assert d["point"] is None and not d["ci_excludes_zero"]


# --- 8. 逐位 NLL：无梯度图 + fp32 -----------------------------------------------------


def test_nll_no_grad_fp32():
    torch.manual_seed(0)
    chunk_ids, offsets = _synth_grid(32, chunk=8)
    positions = [0, 5, 17]
    targets = [7, 100, 33]
    logits = torch.randn(1, 4, 8, 258, requires_grad=True)
    nll = e122.gather_nll(logits, chunk_ids, offsets, positions, targets)
    assert len(nll) == 3
    assert all(math.isfinite(x) and x >= 0 for x in nll)
    # 冻结模型确定性读数：不开第二梯度源（输出为 python float, 无图可回传）
    assert logits.grad is None
    # 逐位对拍: 手工 CE 同值
    picked = logits[0, 0, 0].detach().float()
    ref = torch.nn.functional.cross_entropy(
        picked.unsqueeze(0), torch.tensor([7]), reduction="none"
    )
    assert nll[0] == pytest.approx(float(ref), abs=1e-6)
    # 半精度 logits → 内部强制 fp32 后同值（fp16 熵/log 下溢坑的对偶守卫）
    nll_half = e122.gather_nll(logits.detach().half(), chunk_ids, offsets, positions, targets)
    assert all(abs(a - b) < 1e-3 for a, b in zip(nll, nll_half))


# --- 9. b2 行置换 -------------------------------------------------------------------


def test_build_row_perm_properties():
    perm = e122.build_row_perm({2, 5}, 8)
    assert len(perm) == 8
    assert perm[2] not in (2, 5) and perm[5] not in (2, 5) and perm[2] != perm[5]
    assert all(perm[i] == i for i in range(8) if i not in (2, 5))  # 非源行不动
    # 源行的供体全部来自非源行、互不相同（轮转）；行数不变 = 行存在性保留
    donors = [perm[i] for i in (2, 5)]
    assert len(set(donors)) == 2 and set(donors) <= {0, 1, 3, 4, 6, 7}
    assert len(perm) == 8
    assert e122.build_row_perm(set(), 4) == [0, 1, 2, 3]
    with pytest.raises(ValueError, match="非源真实 chunk"):
        e122.build_row_perm({0, 1, 2}, 3)


def test_patch_store_rows_perm_views():
    class _M:
        def _slm_store_rows(self, chunks, with_views=False):
            r = torch.arange(24).float().view(1, 6, 4)
            if with_views:
                return r, r + 100, torch.tensor(1.0), r + 200, r + 300, r + 400, None
            return r, r + 100, torch.tensor(1.0), r + 200, r + 300

    chunks = SimpleNamespace(chunk_mask=torch.ones(1, 6, dtype=torch.bool))
    perm = e122.build_row_perm({0, 3}, 6)
    m = _M()
    restore = e122.patch_store_rows_perm(m, perm)
    k_rows, v_rows, sn, mem, index, k_store, v_store = m._slm_store_rows(chunks, with_views=True)
    # 源行被同窗其他行替换（内容错误、行存在性保留）
    assert torch.equal(k_rows[0, 0], torch.arange(perm[0] * 4, perm[0] * 4 + 4).float())
    assert torch.equal(k_rows[0, 3], torch.arange(perm[3] * 4, perm[3] * 4 + 4).float())
    assert perm[0] not in (0, 3) and perm[3] not in (0, 3)
    assert torch.equal(k_rows[0, 1], torch.arange(4, 8).float())  # 非源行不动
    assert torch.equal(v_rows[0, 0], k_rows[0, 0] + 100)  # v_rows 同置换
    assert torch.equal(k_store[0, 0], k_rows[0, 0] + 400)  # views 同置换
    assert v_store is None  # None 通道原样穿透
    assert torch.equal(mem[0, 0], torch.arange(200, 204).float())  # memory/index 不动
    assert float(sn) == 1.0
    restore()
    assert "_slm_store_rows" not in m.__dict__  # 还原 = 删实例属性（_patch_state_zero 同款）
    k2, v2, _sn2, _mem2, _idx2 = m._slm_store_rows(chunks)  # 还原后类方法生效
    assert torch.equal(k2[0, 0], torch.arange(4).float())


# --- 10. 选择图与 D1 _d1_build_weight_map 同语义对拍 ------------------------------------


def test_selection_matches_d1_weight_map():
    raw = _counter_filler(256)
    grams = {i: bytes([200 + i]) * 6 for i in range(6)}
    for i, g in grams.items():
        raw[16 * i + 2:16 * i + 8] = g     # 最早出现: chunk i (0..5)
        raw[160 + 8 * i:166 + 8 * i] = g   # 严格更晚 chunk 的重复命中
    raw = bytes(raw)
    clean = torch.tensor([[b + 1 for b in raw]], dtype=torch.long)
    chunk_ids, offsets = _synth_grid(256)
    s1._D1_RARE_TABLE = {grams[i]: 5 - i for i in range(6)}  # g5 最稀有
    args = SimpleNamespace(d1_w=2.0, d1_ngram_len=6, d1_tail=3, d1_rare_quantile=0.2,
                           max_chunks=32, max_span=16)
    with torch.no_grad():
        _wmap, sel_grid, _stats = s1._d1_build_weight_map(clean, chunk_ids, offsets, args)
    # E122 侧: 同一扫描器 + 同档选择 + 同续尾 range + 同映射
    occ = e122.cross_chunk_occurrences(raw, 6)
    rare, off = s1._d1_select_rare_grams(occ, s1._D1_RARE_TABLE, 0.2)
    assert off == 0
    sel, ov = e122.select_tail_positions(occ, rare, 6, 3, 256)
    assert ov == 0
    zero_mask = torch.zeros(1, 256, dtype=torch.bool)
    c_map, s_map, valid = e122.byte_to_grid_slots(chunk_ids, offsets, zero_mask, 32, 16)
    assert bool(valid.all())
    mine = {(int(c_map[0, t]), int(s_map[0, t])) for t in sel}
    d1 = {(int(r[1]), int(r[2])) for r in sel_grid.nonzero().tolist()}
    assert mine == d1  # 选择图逐格同语义（D1 加权训练的同一批位点）
    assert mine == {(12, 14), (12, 15), (13, 0)}  # g5 重复 @200 → 续尾 206-208


def test_cell_keys_relaxed_mode_a_grid():
    """坑 8 放宽档（a 格副基座，冻结预注册 §3）：行源三键允许世代差，但五键
    存在性+通用键（seed_source/backbone_mode）值断言不放宽。"""
    a_grid = dict(seed_source="k", k_row_source="index", v_row_source="memory",
                  summarizer_pool="qpool", backbone_mode="slm")
    e122.assert_cell_keys(SimpleNamespace(**a_grid), strict=False)  # a 格通过
    with pytest.raises(ValueError, match="k_row_source"):  # strict 档仍拒
        e122.assert_cell_keys(SimpleNamespace(**a_grid))
    bad_universal = dict(a_grid, seed_source="v")
    with pytest.raises(ValueError, match="seed_source"):  # 通用键不放宽
        e122.assert_cell_keys(SimpleNamespace(**bad_universal), strict=False)
    missing = {k: v for k, v in a_grid.items() if k != "v_row_source"}
    with pytest.raises(ValueError, match="键缺失"):  # 存在性不放宽
        e122.assert_cell_keys(SimpleNamespace(**missing), strict=False)
