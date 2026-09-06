"""E122 跨段必要性账仪器单测（冻结预注册 v1.0 2026-09-06:
docs/versions/v3_7/FLUED_V3_7_E122_CROSSSEG_NECESSITY_20260906_CN.md; 仪器在
tools/analysis/v3_6/probe_e122_necessity_book.py）。

Covers: (1) b1 替换三匹配（长度/UTF-8 续字节结构/稀有表内）+ 候选域空响亮报错;
(2) 分段漂移剔除（位级 drift 检测 + 窗级 dropped_drift）; (3) d 格累积网格
字节位→(chunk,slot) 映射代数（与 make_cumulative_retention_targets 对拍 +
追加召回槽只装遮蔽字节的完备性）; (4) 坑 8 全键断言 loud fail; (5) 扫描器与
密度账同源 import 断言; (6) 对照手术统计匹配（同三匹配约束 + 保护区）; (7)
bootstrap 可复现（种子固定）; (8) 逐位 NLL 无梯度图 + fp32; (9) b2 行置换
（行存在性保留、源行只取非源行）; (10) 选择图与 D1 _d1_build_weight_map 同
语义对拍（合成窗）; (11) 合成冒烟: 目标位确需源 gram 的窗上 b1 ΔNLL=ln(258)
>0 且对照位 ΔNLL=0（stub 前向代数对拍, 不依赖语料/GPU/checkpoint）。
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


def _stub_forward(raw0: bytes, magic: tuple[bytes, ...], L: int = 6,
                  chunk: int = 16, drift_from: int | None = None):
    """stub 前向（仪器级代数, 非模型行为）：
    - 非 magic 出现处续尾的位置 → 置信预测 clean 真值（两臂逐位同 → ΔNLL=0）;
    - magic gram 出现处的 T 个续尾位：当该 gram 更早 chunk 的源出现处**内容仍在**
      （未被手术置换）→ 置信预测源出现处对应续尾（= 目标真值, NLL≈0）; 否则
      均匀分布（NLL=ln258）。
    即「目标位当且仅当源 gram 内容在」的代数化——b1 替换源后选中位（全部 T 个
    续尾）塌到均匀, 对照位（非续尾）两臂同为置信, ΔNLL 恒 0。"""

    def forward(model, source, ns):
        raw = bytes(int(x) - 1 for x in source[0].tolist())
        t_len = len(raw)
        chunks = _StubChunks(t_len, chunk, drift_from if raw != raw0 else None)
        c_max = int(chunks.chunk_ids.max()) + 1
        s_max = int(chunks.offsets.max()) + 1
        logits = torch.zeros(1, c_max, s_max, 258)
        uniform = set()  # 均匀分布位（源内容不在的续尾位）
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
            c, sl = t // chunk, t % chunk
            if t not in uniform:
                logits[0, c, sl, tgt] = 30.0
        return {"logits_direct": logits, "chunks": chunks}

    return forward


@pytest.mark.parametrize("seed", [0, 1, 2, 3])
def test_algebra_smoke_stub_b1_positive_control_zero(seed):
    """合成冒烟（预注册 §8.3 前置条件）：选中位 ΔNLL_b1 = ln258 > 0 且对照位
    ΔNLL_b1 = 0 的代数对拍。"""
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
    assert s["n_sel"] == 6 and s["n_strong"] == 6  # 6 个选中位全强命中
    sel_items = [it for it in rec["items"] if it["role"] == "selected"]
    ctl_items = [it for it in rec["items"] if it["role"] == "control"]
    assert {it["byte_pos"] for it in sel_items} == {70, 71, 72, 102, 103, 104}
    for it in sel_items:
        assert it["NLL_a"] < 1e-6
        assert abs(it["NLL_b1"] - LN_VOCAB) < 1e-6
        assert it["delta_b1"] == pytest.approx(LN_VOCAB, abs=1e-6)
    for it in ctl_items:
        assert it["delta_b1"] == 0.0  # 对照位两臂逐位同 logits → 严格 0
    assert s["ctl_d_b1"] == 0.0
    # 主判读量代数: 对比 = ln258 - 0 > 0, 强命中密度 = 6/窗
    assert s["sel_d_b1"] / s["n_sel"] == pytest.approx(LN_VOCAB, abs=1e-6)


def test_window_level_drift_drop():
    """b1 手术引发目标位上游分段漂移 → 整窗剔除（预注册 §3 卫生）。"""
    raw0, table = _smoke_window()
    idx = e122.build_pattern_index(table)
    clean = torch.tensor([[b + 1 for b in raw0]], dtype=torch.long)
    zero_mask = torch.zeros(1, len(raw0), dtype=torch.bool)
    ns = SimpleNamespace(max_chunks=16, max_span=16)
    scan = SimpleNamespace(ngram_len=6, tail=3, rare_quantile=1.0, strong_line=1.0)
    fwd = _stub_forward(raw0, (bytes([10] * 6), bytes([11] * 6)), drift_from=40)
    rec = e122.run_window(
        model=None, ns=ns, clean_ids=clean, byte_mask=zero_mask, table=table,
        scan=scan, arms={"a", "b1"}, rng=random.Random(0), pattern_index=idx,
        window_id=0, forward_fn=fwd,
    )
    assert rec["status"] == "dropped_drift"
    assert rec["items"] == []
    assert rec["counts"]["n_drift_positions"] > 0


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


# --- 6. 对照手术统计匹配 --------------------------------------------------------------


def test_control_surgery_stats_matched():
    raw0, table = _smoke_window()
    idx = e122.build_pattern_index(table)
    occ = e122.cross_chunk_occurrences(raw0, 6)
    rare, _off = s1._d1_select_rare_grams(occ, table, 1.0)
    sel, _ov = e122.select_tail_positions(occ, rare, 6, 3, len(raw0))
    n = len(raw0)
    protected = [(p, min(p + 6 + 3, n)) for _g, p in set(sel.values())]
    control_positions = [8, 30, 55, 80, 110, 120]
    plan = e122.plan_window_surgery(raw0, rare, sel, control_positions, table, idx,
                                    random.Random(0), 6, 3)
    # 全部替换（选中源 + 对照）同三匹配
    for g0, p0, r in plan.spans:
        assert len(r) == len(g0)
        assert e122.continuation_pattern(r) == e122.continuation_pattern(g0)
        assert r in table and r != g0
        assert raw0[p0:p0 + len(g0)] == g0
        assert plan.apply(raw0)[p0:p0 + len(r)] == r  # 应用后该处确实是替换串
    # 对照手术与选中手术同约束域（同图案桶、同表、同禁集纪律）→ 统计匹配;
    # 且不落在保护区（选中出现处+续尾）与对照位自身
    ctl_spans = [plan.spans[i] for i in plan.control_span.values()]
    assert ctl_spans, "合成窗必须至少有一个对照手术落点"
    for g0, p0, _r in ctl_spans:
        lo, hi = p0, p0 + len(g0)
        assert not any(lo < ph and pl < hi for pl, ph in protected)
    for q, i in plan.control_span.items():
        _g0, p0, _r = plan.spans[i]
        assert not (p0 <= q < p0 + len(plan.spans[i][2]))
    # 每个对照位要么有手术、要么如实计数（无合格出现处）
    assert plan.n_control_no_occurrence == len(control_positions) - len(plan.control_span)
    # 手术不改变窗长
    assert len(plan.apply(raw0)) == n
    # 同串多出现共用一个替换 gram（记录在 replacements）
    assert len(plan.replacements) <= len(plan.spans)
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
