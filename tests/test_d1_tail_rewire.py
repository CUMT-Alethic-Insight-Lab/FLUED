"""E121 D1 跨段续尾损失重加权臂单测（任务书冻结 v1 2026-09-04:
docs/versions/v3.7/FLUED_V3_7_D1_CROSSSEG_TAIL_20260904_CN.md; 训练器旋钮在
tools/train/v3_6/train_v36_s1.py 的 --d1-tail-rewire 旗标族, 稀有表产品化在
tools/analysis/v3_6/build_d1_rare_table.py）。

Covers: (1) 旗标全关 = 逐位不变（关态 loss/metrics 与「无 d1 键的 legacy 命名空
间」逐位相等——参照 test_e120_readout_swap 既有模式）; (2) 权重图不进反向图
（任务书 §3 注记 3: no_grad 构造 + detach 双保险, 端到端 backward 后权重图
.grad 为 None, requires_grad 为 False）; (3) 分位数档命中集大小恒定（窗内命中
gram 数 × quantile, floor）; (4) 表外 gram = 非稀有且被计数; (5) 扫描器与密度
账同函数（import 同源断言, 任务书 §3 注记 1）; (6) 权重图接线代数（合成窗:
稀有命中处起 T 个续尾位 = w, 其余 = 1, 续尾 range 与密度账 supervised_count
同语义）; (7) w=1 恒等列: loss 逐位同基座 + 双仪表照常出数; (8) parser 默认关;
(9) 结构守卫响亮报错（累积网格 / markov / mid）。
Tiny a 格 slm CPU 模型 (kda_impl="torch", boundary_mode="uniform"), 只测接线
与代数, 不测训练行为。
"""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest
import torch

import tools.train.v3_6.train_v36_s1 as s1
from flued.v36 import FLUEDV36
from tests.test_v37_oracle_probe import _tiny_c_config
from tools.analysis.v3_6 import demand_density_book as ddb

DEVICE = torch.device("cpu")


def _tiny_a_config(**overrides):
    # a 格 (k=index, v=memory) + 16B chunk 粒度 (与密度账 CHUNK=16 对齐,
    # 训练器守卫 bytes_per_chunk==16 的同款口径)
    cfg = dict(k_row_source="index", v_row_source="memory",
               bytes_per_chunk=16, max_span=16, max_chunks=32)
    cfg.update(overrides)
    return _tiny_c_config(**cfg)


def _model(seed: int = 0, **overrides) -> FLUEDV36:
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_a_config(**overrides)).eval()


def _args(**overrides) -> SimpleNamespace:
    base = dict(
        mask_prob=0.0, mask_span_min=1, mask_span_max=8, mask_mode="byte_span",
        max_chunks=32, max_span=16, bytes_per_chunk=16,
        task1_loss_weight=1.0, task2_loss_weight=1.0,
        predict_weight=1.0, predict_mode="latent", amp=False,
        # D1 旗标族 (默认全关)
        d1_tail_rewire=False, d1_w=2.0, d1_rare_table="",
        d1_rare_quantile=0.2, d1_ngram_len=6, d1_tail=3,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def _ids(seed: int = 1, t: int = 256):
    g = torch.Generator().manual_seed(seed)
    return torch.randint(1, 257, (1, t), generator=g)


def _write_table(tmp_path, table: dict[bytes, int]) -> str:
    grams = np.array(sorted(table.keys()), dtype="S6")
    counts = np.array([table[bytes(g)] for g in grams], dtype=np.int64)
    p = tmp_path / "d1_rare_table_test.npz"
    np.savez(p, grams=grams, counts=counts)
    return str(p)


@pytest.fixture(autouse=True)
def _reset_d1_table():
    yield
    s1._D1_RARE_TABLE = None


# --- 1. 旗标全关 = 逐位不变 ------------------------------------------------------


def test_off_bitwise_identical_to_legacy_namespace():
    """旗标全关 vs 无 d1 键的 legacy 命名空间: loss + 全部公共 metrics 逐位相等,
    且关态不新增任何 metrics 键 (零侵入)。"""
    torch.manual_seed(7)
    model = _model(seed=3)
    ids = _ids()
    legacy_args = SimpleNamespace(**{
        k: v for k, v in vars(_args()).items() if not k.startswith("d1_")
    })
    off_args = _args()  # d1_* 键在, 但全关
    loss_leg, m_leg = s1.step_model(model, (ids,), legacy_args, DEVICE, train=True)
    loss_off, m_off = s1.step_model(model, (ids,), off_args, DEVICE, train=True)
    assert torch.equal(loss_leg, loss_off)
    assert set(m_leg) == set(m_off)
    assert not any(k.startswith("d1_") for k in m_off)
    for k in m_leg:
        assert torch.equal(m_leg[k], m_off[k]), k


# --- 2. 权重图不进反向图 (任务书 §3 注记 3) ---------------------------------------


def test_weight_map_detached_no_grad_path(tmp_path, monkeypatch):
    """端到端: no_grad 构造 + detach 双保险——builder 产物 requires_grad=False /
    grad_fn=None / 对其反向响亮拒绝; 真实训练步 backward 后捕获的权重图 .grad
    仍为 None (漏接 = 整臂作废的梯度通路不存在)。"""
    s1._load_d1_rare_table(_write_table(tmp_path, {b"abcdef": 0}))
    args = _args(d1_tail_rewire=True, d1_w=2.0)
    # builder 直查
    captured = {}
    orig = s1._d1_build_weight_map

    def spy(clean, chunk_ids, offsets, a):
        wmap, sel, stats = orig(clean, chunk_ids, offsets, a)
        captured["wmap"] = wmap
        return wmap, sel, stats

    monkeypatch.setattr(s1, "_d1_build_weight_map", spy)
    torch.manual_seed(7)
    model = _model(seed=3)
    loss, _m = s1.step_model(model, (_ids(),), args, DEVICE, train=True)
    wmap = captured["wmap"]
    assert not wmap.requires_grad
    assert wmap.grad_fn is None
    with pytest.raises(RuntimeError):
        wmap.backward(torch.ones_like(wmap))
    loss.backward()
    assert wmap.grad is None
    # 权重图数值域: 要么 1.0 要么 w, 不出现别的计价
    uniq = torch.unique(wmap)
    assert set(uniq.tolist()) <= {1.0, 2.0}


# --- 3. 分位数档命中集大小恒定 ----------------------------------------------------


def test_quantile_tier_constant_size():
    """命中集大小 = 窗内命中 gram 数 × quantile (floor), 取计数最稀有者。"""
    occ = {bytes([97 + i]) * 6: [i * 100] for i in range(10)}
    table = {g: 10 - i for i, g in enumerate(occ.keys())}  # 计数 = 10..1
    rare, off = s1._d1_select_rare_grams(occ, table, 0.2)
    assert off == 0
    assert len(rare) == 2  # floor(10 × 0.2)
    counts = {table[g] for g in rare}
    assert counts == {1, 2}  # 最稀有两档
    rare25, _ = s1._d1_select_rare_grams(
        {bytes([97 + i]) * 6: [i] for i in range(25)},
        {bytes([97 + i]) * 6: i for i in range(25)}, 0.2)
    assert len(rare25) == 5  # floor(25 × 0.2)
    # 命中数不足一档: floor(4 × 0.2)=0 → 空集 (恒定比率语义, 不设下限)
    rare4, off4 = s1._d1_select_rare_grams(
        {bytes([97 + i]) * 6: [i] for i in range(4)},
        {bytes([97 + i]) * 6: i for i in range(4)}, 0.2)
    assert rare4 == set() and off4 == 0


# --- 4. 表外 gram = 非稀有且被计数 ------------------------------------------------


def test_offtable_gram_nonrare_counted():
    occ = {bytes([97 + i]) * 6: [i * 100] for i in range(10)}
    table = {bytes([97 + i]) * 6: i for i in range(7)}  # 后 3 个 gram 表外
    rare, off = s1._d1_select_rare_grams(occ, table, 0.2)
    assert off == 3  # 表外计数落日志 (诚实边界)
    assert len(rare) == 2  # 大小仍按全部命中数 × 0.2
    assert rare <= set(table.keys())  # 表外 gram 永不入稀有集
    # 全表外: 稀有集空, 计数如实
    rare_none, off_none = s1._d1_select_rare_grams(occ, {}, 0.2)
    assert rare_none == set() and off_none == 10


# --- 5. 扫描器与密度账同函数 (任务书 §3 注记 1) ------------------------------------


def test_scanner_same_source_as_density_book():
    import tools.analysis.v3_6.build_d1_rare_table as builder

    # 训练器在线扫描 = 密度账仪器核心函数对象本身 (零复制改写)
    assert s1.cross_chunk_occurrences is ddb.cross_chunk_occurrences
    # 离线建表脚本同源 (collect_candidates / background_counts)
    assert builder.collect_candidates is ddb.collect_candidates
    assert builder.background_counts is ddb.background_counts
    assert builder.cross_chunk_occurrences is ddb.cross_chunk_occurrences
    # 行为同源抽查: 同一窗扫描结果与密度账逐位一致
    win = bytes(range(256)) * 16
    assert s1.cross_chunk_occurrences(win, 6).keys() == \
        ddb.cross_chunk_occurrences(win, 6).keys()


# --- 6. 权重图接线代数 (合成窗) ----------------------------------------------------


def _counter_filler(n: int) -> bytearray:
    # 7 与 256 互素 → 窗内每个 6-gram 唯一, filler 自身零命中 (不污染分位数档)
    return bytearray((i * 7 + 13) % 256 for i in range(n))


def _synth_grid(t: int, chunk: int = 16):
    idx = torch.arange(t)
    return idx.view(1, -1) // chunk, idx.view(1, -1) % chunk


def test_weight_map_wiring_synthetic_window():
    """6 个受控跨 chunk 重复 gram + 分位档 0.2 → 命中集恰 1 (最稀有者); 其续尾
    T=3 个字节位 = w, 其余 = 1; 续尾 range 与密度账 supervised_count 同语义
    (p+L .. p+L+T-1, 窗沿截断)。"""
    raw = _counter_filler(256)
    grams = {i: bytes([200 + i]) * 6 for i in range(6)}
    for i, g in grams.items():
        raw[16 * i + 2:16 * i + 8] = g     # 最早出现: chunk i (0..5)
        raw[160 + 8 * i:166 + 8 * i] = g   # 严格更晚 chunk 的重复命中
    clean = torch.tensor([[b + 1 for b in raw]], dtype=torch.long)
    chunk_ids, offsets = _synth_grid(256)
    # 计数: g5 最稀有 (0) → 分位档 0.2×6 → floor 1 → 只选 g5
    s1._D1_RARE_TABLE = {grams[i]: 5 - i for i in range(6)}
    args = _args(d1_tail_rewire=True, d1_w=2.0)
    with torch.no_grad():
        wmap, sel, stats = s1._d1_build_weight_map(clean, chunk_ids, offsets, args)
    assert stats["hit_grams"] == 6
    assert stats["offtable_grams"] == 0
    assert stats["weighted_positions"] == 3  # g5 重复 @p=200 → 续尾 206,207,208
    assert sel.view(-1).nonzero().flatten().tolist() == [206, 207, 208]
    assert wmap.view(-1)[206:209].tolist() == [2.0, 2.0, 2.0]
    assert float((wmap == 1.0).float().sum()) == 32 * 16 - 3
    assert set(torch.unique(wmap).tolist()) == {1.0, 2.0}


def test_weight_map_tail_clipped_at_window_end():
    """窗沿命中 (p=250, chunk 15) 续尾 256..258 全越窗 → 0 加权位
    (supervised_count 同款截断语义)。"""
    raw = _counter_filler(256)
    g = bytes([200]) * 6
    raw[2:8] = g       # 最早出现 chunk 0
    raw[250:256] = g   # 重复 @p=250, 续尾全越窗
    clean = torch.tensor([[b + 1 for b in raw]], dtype=torch.long)
    chunk_ids, offsets = _synth_grid(256)
    s1._D1_RARE_TABLE = {g: 0}
    # q=1.0: 单命中 gram 也入选 (接线测试与档大小解耦)
    with torch.no_grad():
        _w, sel, stats = s1._d1_build_weight_map(
            clean, chunk_ids, offsets, _args(d1_tail_rewire=True, d1_rare_quantile=1.0)
        )
    assert stats["hit_grams"] == 1 and stats["weighted_positions"] == 0
    assert not bool(sel.any())


def test_weight_map_early_chunk_only_no_hit():
    """同 chunk 内重复不计 (条件①: 出现 chunk 严格晚于最早出现 chunk)。"""
    raw = _counter_filler(256)
    g = bytes([200]) * 6
    raw[3:9] = g    # chunk 0
    raw[5:11] = g   # 仍是 chunk 0 → 不命中
    clean = torch.tensor([[b + 1 for b in raw]], dtype=torch.long)
    chunk_ids, offsets = _synth_grid(256)
    s1._D1_RARE_TABLE = {g: 0}
    with torch.no_grad():
        _w, _s, stats = s1._d1_build_weight_map(
            clean, chunk_ids, offsets, _args(d1_tail_rewire=True, d1_rare_quantile=1.0)
        )
    assert stats["hit_grams"] == 0 and stats["weighted_positions"] == 0


# --- 7. w=1 恒等列: loss 逐位同基座 + 双仪表出数 -----------------------------------


def test_w1_identity_bitwise_with_gauges(tmp_path):
    """w=1 对照列: 损失走未改 _ce 路径逐位同关态; d1_acc_* 双仪表照常有数
    (拟加权位选择图与 w 解耦——同窗同分布判读基准, 任务书 §2)。"""
    s1._load_d1_rare_table(_write_table(tmp_path, {b"abcdef": 0}))
    torch.manual_seed(7)
    model = _model(seed=3)
    ids = _ids()
    loss_off, m_off = s1.step_model(model, (ids,), _args(), DEVICE, train=True)
    loss_w1, m_w1 = s1.step_model(model, (ids,), _args(d1_tail_rewire=True, d1_w=1.0), DEVICE, train=True)
    assert torch.equal(loss_off, loss_w1)
    for k, v in m_off.items():
        assert torch.equal(v, m_w1[k]), k
    for key in ("d1_acc_weighted", "d1_acc_unweighted"):
        assert key in m_w1 and 0.0 <= float(m_w1[key]) <= 1.0
    # 随机字节窗拟加权位可为空集 → weighted 侧 0.0 占位、unweighted 侧 = 全体
    assert float(m_w1["d1_acc_weighted"]) == 0.0


# --- 8. parser 默认关 --------------------------------------------------------------


def test_parser_defaults_off():
    from tools.train.v3_6.train_v36 import build_parser

    parser = build_parser()
    s1._add_s1_args(parser)
    args = parser.parse_args([])
    assert args.d1_tail_rewire is False
    assert args.d1_w == 2.0
    assert args.d1_rare_table == ""
    assert args.d1_rare_quantile == 0.2
    assert args.d1_ngram_len == 6
    assert args.d1_tail == 3


# --- 9. 结构守卫响亮报错 ------------------------------------------------------------


def test_structural_guards_loud_fail(tmp_path):
    """累积网格 / markov 两种破坏 byte→slot 对应的臂形态, 响亮拒绝不静默。"""
    s1._load_d1_rare_table(_write_table(tmp_path, {b"abcdef": 0}))
    d1_args = _args(d1_tail_rewire=True, d1_w=2.0)
    torch.manual_seed(7)
    model_a = _model(seed=3)
    # 累积网格 (d 格 coarse V): step_model 内守卫
    model_d = FLUEDV36(_tiny_a_config(v_row_source="state")).eval()
    with pytest.raises(ValueError, match="per-chunk completion grids"):
        s1.step_model(model_d, (_ids(),), d1_args, DEVICE, train=True)
    # markov 头重构 codec CE: 同款响亮拒绝
    with pytest.raises(ValueError, match="decoder-markov"):
        s1.step_model(model_a, (_ids(),), _args(d1_tail_rewire=True, decoder_markov=2), DEVICE, train=True)


def test_rare_table_loader_loud_fail(tmp_path):
    with pytest.raises(SystemExit, match="rare table 缺席"):
        s1._load_d1_rare_table(str(tmp_path / "missing.npz"))
    bad = tmp_path / "badkey.npz"
    np.savez(bad, grams=np.array([b"abcdef"], dtype="S6"))
    with pytest.raises(SystemExit, match="缺键"):
        s1._load_d1_rare_table(str(bad))
    badshape = tmp_path / "badshape.npz"
    np.savez(badshape, grams=np.array([b"abcdef"], dtype="S6"),
             counts=np.zeros(2, dtype=np.int64))
    with pytest.raises(SystemExit, match="形不符"):
        s1._load_d1_rare_table(str(badshape))
    ok = tmp_path / "ok.npz"
    np.savez(ok, grams=np.array([b"abcdef", b"zzzzzz"], dtype="S6"),
             counts=np.array([0, 3], dtype=np.int64))
    assert s1._load_d1_rare_table(str(ok)) == 2
    assert s1._D1_RARE_TABLE[b"abcdef"] == 0 and s1._D1_RARE_TABLE[b"zzzzzz"] == 3


def test_rare_table_loader_uint8_nul_safe(tmp_path):
    """build_d1_rare_table.py 主形态 (N, L) uint8 矩阵: 含 NUL 字节的 gram 无损
    往返 ('S6' dtype 会把尾随 \\x00 截断——第一次建表实测踩坑, 语料确有零字节)。"""
    g_nul = b"ab\x00\x00\x00\x00"
    grams = np.frombuffer(b"abcdef" + g_nul, dtype=np.uint8).reshape(2, 6)
    ok = tmp_path / "uint8.npz"
    np.savez(ok, grams=grams, counts=np.array([0, 7], dtype=np.int64))
    assert s1._load_d1_rare_table(str(ok)) == 2
    assert s1._D1_RARE_TABLE[g_nul] == 7
    assert s1._D1_RARE_TABLE[b"abcdef"] == 0
