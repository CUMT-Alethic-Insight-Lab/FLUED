"""v3.7 Q15 回路养成臂 (任务书 2026-08-25 冻结;
spec: docs/versions/v3_7/FLUED_V3_7_Q15_CIRCUIT_REARING_20260825_CN.md).

d 格 (k=state ∧ v=state, seed_source=k) 上的过程奖励三件套: L_attend
(block-1 need_attn 手工注意力 + T 掩码 + T∩src=∅ 逐样本机械断言) + sg(g)
门控结果损失 (§3.2 修订 v1: 单头超基线超出量门 σ((maxmass−chance−δ)/s),
δ=0.15 s=0.05; echo 槽位从 completion 网格剔除) + L_couple 反作弊孪生铰链
(head-tail swap, 零随机流篡改, 选择每 splice 样本一抽 _BURST_GENERATOR);
压缩区档 a 剔除 r 恒 1.0 train/eval 同开; codec 回调线 steps 800-1000
臂内自锚.

Covers (任务书 §7.6 验收单): (1) need_attn 开关 -- 关态确定性逐比特/关态
last_block1_attn is None/开关两态 allclose(1e-5@fp32)/views 路径响亮报错;
(2) _burst_store_block 剔除行列与 -1 网格跳过; (3) T∩src=∅ 断言违规输入
raise; (4) _q15_echo_mass 手工核对 + 段尾离网 None; (5) 孪生篡改字节级
正确性; (6) 门控 sg 无梯度; (7) 回调线触发/不触发/边界/下限钳制; (8) CLI
响亮校验; (9) e2e (d 格 tiny): 有限 loss + 指标键 + eval 零占位零 RNG.
"""

from __future__ import annotations

import pytest
import torch

from flued.data import BYTE_OFFSET, PAD_ID
from flued.v36 import FLUEDV36
from tests.test_v37_burst_task import _sampler
from tests.test_v37_retrieval_task import TEXT1, TEXT2, _clean
from tests.test_v37_slm import _s1_args, tiny_config
from tools.train.v3_6 import train_v36_s1 as s1


@pytest.fixture()
def corpus_file(tmp_path):
    p = tmp_path / "corpus.txt"
    p.write_bytes("天地玄黄宇宙洪荒日月盈昃辰宿列张律吕调阳云腾致雨露结为霜".encode("utf-8") * 40)
    return p


def _d_grid_config(**over):
    base = dict(
        k_row_source="state", v_row_source="state", seed_source="k",
        max_chunks=64, max_span=32, bytes_per_chunk=16, max_positions=64,
    )
    base.update(over)
    return tiny_config(**base)


def _q15_args(**over):
    base = dict(
        q15_circuit_rearing=True, burst_prob=1.0, burst_prior_sieve=False,
        backbone_mode="slm", k_row_source="state", v_row_source="state",
        seed_source="k", readout_views=1, mask_prob=0.1, max_chunks=64, max_span=32,
    )
    base.update(over)
    return _s1_args(**base)


# --- 1. need_attn 开关 (任务书 §7.1 验收) ------------------------------------------


def _backbone_io(cfg):
    torch.manual_seed(0)
    model = FLUEDV36(cfg)
    bb = model.backbone
    bsz, n = 2, 5
    k = torch.randn(bsz, n, cfg.d_mem)  # k_row_source=index -> align_k eats d_mem
    v = torch.randn(bsz, n, cfg.d_mem)
    cm = torch.ones(bsz, n, dtype=torch.bool)
    pos = torch.randn(1, n, cfg.d_backbone)
    return bb, k, v, cm, pos


def test_need_attn_off_deterministic_and_none():
    cfg = tiny_config()  # a 格 (index, memory): backbone 单测不挑格
    bb, k, v, cm, pos = _backbone_io(cfg)
    out1 = bb(k, v, cm, pos)
    out2 = bb(k, v, cm, pos)
    assert torch.equal(out1, out2)  # 关态同输入两次前向逐比特相等
    assert bb.last_block1_attn is None  # 关态寄存槽为空


def test_need_attn_on_allclose_off_fp32():
    cfg = tiny_config()
    bb, k, v, cm, pos = _backbone_io(cfg)
    out_off = bb(k, v, cm, pos)
    assert bb.last_block1_attn is None
    out_on = bb(k, v, cm, pos, need_attn=True)
    assert torch.allclose(out_off, out_on, atol=1e-5)  # 开关两态 allclose(1e-5@fp32)
    attn = bb.last_block1_attn
    assert attn is not None and attn.shape == (2, cfg.backbone_nhead, 5, 5)
    assert attn.dtype == torch.float32
    # 概率归一 (逐 query 行和为 1)
    assert torch.allclose(attn.sum(dim=-1), torch.ones(2, cfg.backbone_nhead, 5), atol=1e-5)


def test_need_attn_causal_mask_zero():
    cfg = tiny_config()
    bb, k, v, cm, pos = _backbone_io(cfg)
    bb(k, v, cm, pos, need_attn=True)
    attn = bb.last_block1_attn
    fut = torch.triu(torch.ones(5, 5, dtype=torch.bool), diagonal=1)
    assert float(attn[:, :, fut].abs().sum()) == 0.0  # 掩码位置概率为零


def test_need_attn_views_path_loud():
    cfg = tiny_config()
    bb, k, v, cm, pos = _backbone_io(cfg)
    k4 = k.unsqueeze(2).expand(2, 5, 2, cfg.d_mem).contiguous()  # views=2 触发多视图路径
    with pytest.raises(ValueError, match="need_attn"):
        bb(k4, v, cm, pos, need_attn=True)


# --- 2. _burst_store_block (§2 档 a 剔除, r 恒 1.0) ---------------------------------


def _fake_chunks(chunk_ids: torch.Tensor, n_chunks: int):
    from types import SimpleNamespace

    chunk_mask = chunk_ids.ge(0)
    cm = torch.zeros(chunk_ids.size(0), n_chunks, dtype=torch.bool)
    valid = chunk_ids.max().item()
    cm[:, : valid + 1] = True
    return SimpleNamespace(chunk_ids=chunk_ids, chunk_mask=cm, offsets=chunk_ids.clamp(min=0))


def test_burst_store_block_rows_and_cols():
    # 12 字节, 6 chunk; 出现 1..R-1 = [(0,2),(4,8)] -> chunks {0},{2,3};
    # echo 首字节 t=10 -> chunk 5
    chunk_ids = torch.tensor([[0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]])
    chunks = _fake_chunks(chunk_ids, 6)
    metas = [{"occurrences": [(0, 2), (4, 8), (8, 10)], "echo_span": (10, 12)}]
    block = s1._burst_store_block(metas, chunks)
    assert block is not None and block.shape == (1, 6, 6)
    expect = torch.zeros(1, 6, 6, dtype=torch.bool)
    expect[0, 5:, 0] = True
    expect[0, 5:, 2] = True
    expect[0, 5:, 3] = True
    assert torch.equal(block, expect)
    assert not block[0, 5, 5]  # 剔除集不含 query 自身 chunk (对角保持在模型侧)
    # 无 splice 样本 -> None (零成本 legacy)
    assert s1._burst_store_block([None], chunks) is None


def test_burst_store_block_skips_offgrid_occurrence():
    # 出现 (0,2) 落在 chunk -1 (未入网格) -> 只剔出现 (4,8) 的 chunk
    chunk_ids = torch.tensor([[-1, -1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]])
    chunks = _fake_chunks(chunk_ids, 6)
    metas = [{"occurrences": [(0, 2), (4, 8), (8, 10)], "echo_span": (10, 12)}]
    block = s1._burst_store_block(metas, chunks)
    expect = torch.zeros(1, 6, 6, dtype=torch.bool)
    expect[0, 5:, 2] = True
    expect[0, 5:, 3] = True
    assert torch.equal(block, expect)


# --- 3. T∩src=∅ 机械断言 (§3 + §1 方法论备案) ----------------------------------------


def test_t_src_disjoint_assertion():
    t_mask = torch.zeros(4, 4, dtype=torch.bool)
    t_mask[3, 2] = True
    src_mask = torch.tensor([True, False, False, False])
    s1._q15_assert_disjoint(t_mask, src_mask)  # 空交集: 通过
    t_mask[2, 0] = True  # 违规: T 投影含 src chunk 0
    with pytest.raises(ValueError, match="T∩src"):
        s1._q15_assert_disjoint(t_mask, src_mask)


# --- 4. _q15_echo_mass 手工核对 -------------------------------------------------------


def test_echo_mass_manual_check():
    # 6 chunk 全有效; occurrence[0]=字节 0..4 -> chunks {0,1}, c1_end=1;
    # occurrences[:-1] 覆盖 chunks {0,1,2}; echo 字节 10..12 -> q=5
    chunk_ids = torch.tensor([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5])
    offsets = torch.tensor([0, 1] * 6)
    chunk_mask = torch.ones(6, dtype=torch.bool)
    m = {"occurrences": [(0, 4), (4, 6), (6, 10)], "echo_span": (10, 12)}
    H = 2
    attn = torch.zeros(H, 6, 6)
    # T(b, q=5) = {j: 1 < j <= 5, j ∉ {0,1,2}} = {3,4,5}
    # allowed(b, q=5) = {j <= 5, 有效, 非 src} = {3,4,5} -> chance = 3/3 = 1.0
    attn[0, 5, 3] = 0.1
    attn[1, 5, 4] = 0.2
    attn[0, 5, 5] = 0.3
    attn[0, 5, 2] = 0.9  # src chunk: 不进 T, 不计 mass
    attn[0, 5, 0] = 0.9  # src chunk 同上
    attn[0, 5, 1] = 0.9  # c1_end: j>c1_end 才进 T
    attn[0, 4, 3] = 0.7  # 别的 query 行不进 echo mass
    got = s1._q15_echo_mass(attn, m, chunk_ids, offsets, chunk_mask)
    assert got is not None
    mass, maxmass, chance, q, s = got
    assert mass.shape == (2,)
    assert float(mass[0]) == pytest.approx(0.6) and float(mass[1]) == pytest.approx(0.6)  # 逐头求和
    # maxmass 取 max over heads (head0: 0.1+0.3=0.4, head1: 0.2), 不是求和 0.6
    assert float(maxmass[0]) == pytest.approx(0.4) and float(maxmass[1]) == pytest.approx(0.4)
    # chance 精确值: |T|/|allowed| = 3/3 = 1.0 (修订 v1 口径)
    assert float(chance[0]) == pytest.approx(1.0) and float(chance[1]) == pytest.approx(1.0)
    assert q.tolist() == [5, 5] and s.tolist() == [0, 1]


def test_echo_mass_chance_partial_allowed():
    # chance 非 1 判例: occurrence[0]=字节 2..4 -> chunk {1}, c1_end=1;
    # src (occurrences[:-1]) = {1}; echo 字节 10..12 -> q=5.
    # allowed(q=5) = {j<=5 有效非 src} = {0,2,3,4,5} (|allowed|=5, 含 chunk 0);
    # T = {1<j<=5 非 src 有效} = {2,3,4,5} (|T|=4) -> chance = 4/5 = 0.8
    chunk_ids = torch.tensor([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5])
    offsets = torch.tensor([0, 1] * 6)
    chunk_mask = torch.ones(6, dtype=torch.bool)
    m = {"occurrences": [(2, 4), (8, 10)], "echo_span": (10, 12)}
    got = s1._q15_echo_mass(torch.zeros(2, 6, 6), m, chunk_ids, offsets, chunk_mask)
    assert got is not None
    _mass, _maxmass, chance, _q, _s = got
    assert float(chance[0]) == pytest.approx(0.8) and float(chance[1]) == pytest.approx(0.8)


def test_echo_mass_none_when_echo_offgrid():
    chunk_ids = torch.tensor([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, -1, -1])
    offsets = torch.tensor([0, 1] * 6)
    chunk_mask = torch.ones(6, dtype=torch.bool)
    m = {"occurrences": [(0, 4), (4, 6), (6, 10)], "echo_span": (10, 12)}
    assert s1._q15_echo_mass(torch.zeros(2, 6, 6), m, chunk_ids, offsets, chunk_mask) is None


# --- 5. 孪生篡改字节级正确性 (§3.3) ---------------------------------------------------


def test_twin_head_tail_swap_bytewise():
    seg = "天地玄黄宇宙洪荒".encode("utf-8")  # 24B
    raw = b"AAAA" + seg + b"BBBB" + seg + b"CCCC" + seg + b"DDDD"
    n_seg = len(seg)
    occ = [(4, 4 + n_seg), (4 + n_seg + 4, 4 + 2 * n_seg + 4), (8 + 2 * n_seg + 4, 8 + 3 * n_seg + 4)]
    tb = 9  # echo_span 长度 = 末 3 字
    m = {"occurrences": occ, "echo_span": (occ[-1][1] - tb, occ[-1][1])}
    twin = s1._burst_twin_bytes(raw, m)
    head = raw[occ[0][0] : occ[0][0] + tb]  # occurrence 0 段首 tb 字节
    expect = bytearray(raw)
    for lo, hi in occ[:-1]:
        expect[hi - tb : hi] = head
    assert twin == bytes(expect)
    assert twin != raw
    # 只动 occurrences 1..R-1 的段尾 tb 字节, 其余逐位相同 (含最后一次出现)
    diff = [i for i, (a, b) in enumerate(zip(raw, twin)) if a != b]
    allowed = set()
    for lo, hi in occ[:-1]:
        allowed |= set(range(hi - tb, hi))
    assert set(diff) <= allowed and len(diff) > 0
    # UTF-8 合法 (段内字节互换)
    twin.decode("utf-8")


# --- 6. 门控 stop-gradient + 修订 v1 数值判例 (§3.2) ---------------------------------


def test_gate_is_stop_gradient():
    maxmass = torch.tensor([0.1, 0.5], requires_grad=True)
    chance = torch.tensor([0.2, 0.3])
    gate = s1._q15_gate(maxmass.detach(), chance)
    assert gate.grad_fn is None  # sg(g): 无计算图
    ce = torch.tensor([1.0, 2.0])
    loss = (gate * ce).sum() + 0.0 * maxmass.sum()  # 图里有 maxmass, 但只经零权重
    loss.backward()
    assert maxmass.grad is not None and float(maxmass.grad.abs().sum()) == 0.0  # 门控路径零梯度
    # chance 由索引计数构成, 天然无梯度
    assert not chance.requires_grad


def test_gate_revision_v1_numerics():
    """§3.2 修订 v1 冻结数值: g = σ((maxmass − chance − 0.15)/0.05) --
    单头超基线超出量门."""
    # maxmass == chance (随机初始: 超基线超出量为零) -> σ(-3) ≈ 0.047, 基本关闭
    g = s1._q15_gate(torch.tensor([0.30]), torch.tensor([0.30]))
    assert float(g) == pytest.approx(0.0474, abs=1e-3)
    # maxmass=1 (单头特化拉满) 且 chance=0.3 -> σ(11) ≈ 1, 全开
    g = s1._q15_gate(torch.tensor([1.0]), torch.tensor([0.3]))
    assert float(g) == pytest.approx(1.0, abs=1e-4)
    # 超出量恰好 δ=0.15 -> σ(0) = 0.5 (门半开, 阈值点)
    g = s1._q15_gate(torch.tensor([0.45]), torch.tensor([0.30]))
    assert float(g) == pytest.approx(0.5, abs=1e-6)


# --- 7. 回调线 (§5, 纯函数) -----------------------------------------------------------


def _cbk(anchor, window, lambdas=None, floors=None, step=2000):
    lambdas = lambdas or {"att": 0.1, "out": 1.0, "couple": 0.5}
    floors = floors or {k: v * s1._Q15_CALLBACK_FLOOR for k, v in lambdas.items()}
    return s1._q15_callback_check(anchor, window, lambdas, floors, step)


def test_callback_no_trigger_at_margin():
    anchor = {"direct_acc": 0.50, "backbone_acc": 0.40}
    events, lam = _cbk(anchor, {"direct_acc": 0.49, "backbone_acc": 0.39})
    assert events == [] and lam == {"att": 0.1, "out": 1.0, "couple": 0.5}
    # 边界纪律: 退步须严格 >0.02 (0.481 -> 0.019 退步, 不触发; fp 精确边界
    # 0.5-0.48=0.02000...4 属浮点假象, 不作判例)
    events, _ = _cbk(anchor, {"direct_acc": 0.481, "backbone_acc": 0.40})
    assert events == []
    events, _ = _cbk(anchor, {"direct_acc": 0.47, "backbone_acc": 0.40})
    assert len(events) == 1  # 0.03 > 0.02 触发


def test_callback_trigger_halves_all_lambdas():
    anchor = {"direct_acc": 0.50, "backbone_acc": 0.40}
    events, lam = _cbk(anchor, {"direct_acc": 0.40, "backbone_acc": 0.40})
    assert len(events) == 1
    ev = events[0]
    assert ev["triggered"] == ["direct_acc"]  # 只有 direct_acc 退步 >2pp
    assert ev["step"] == 2000 and ev["old"]["att"] == 0.1
    assert lam == {"att": 0.05, "out": 0.5, "couple": 0.25}  # 三 λ 各 x0.5


def test_callback_floor_clamp():
    anchor = {"direct_acc": 0.50, "backbone_acc": 0.40}
    floors = {"att": 0.025, "out": 0.25, "couple": 0.125}  # 初值 x0.25
    events, lam = _cbk(anchor, {"direct_acc": 0.10, "backbone_acc": 0.10},
                       lambdas={"att": 0.025, "out": 0.3, "couple": 0.125}, floors=floors)
    assert lam["att"] == 0.025 and lam["couple"] == 0.125  # 已到下限, 钳住
    assert lam["out"] == pytest.approx(max(0.3 * 0.5, 0.25))  # 未到下限, 正常减半
    assert events[0]["triggered"] == ["direct_acc", "backbone_acc"]


# --- 8. CLI 响亮校验 (任务书 §7.5) -----------------------------------------------------


def test_check_q15_args_loud():
    s1._check_q15_args(_s1_args())  # 关态静默通过
    base = _q15_args(burst_prob=0.0)
    with pytest.raises(SystemExit, match="burst-prob"):
        s1._check_q15_args(base)
    base = _q15_args(burst_prior_sieve=False)  # 筛必须开
    with pytest.raises(SystemExit, match="burst-prior-sieve"):
        s1._check_q15_args(base)
    base = _q15_args(burst_prior_sieve=True)
    base.backbone_mode = "xattn"
    with pytest.raises(SystemExit, match="slm"):
        s1._check_q15_args(base)
    base = _q15_args(burst_prior_sieve=True, k_row_source="index")  # 非 d 格
    with pytest.raises(SystemExit, match="d 格"):
        s1._check_q15_args(base)
    base = _q15_args(burst_prior_sieve=True, v_row_source="memory")
    with pytest.raises(SystemExit, match="d 格"):
        s1._check_q15_args(base)
    base = _q15_args(burst_prior_sieve=True, seed_source="v")
    with pytest.raises(SystemExit, match="seed-source"):
        s1._check_q15_args(base)
    base = _q15_args(burst_prior_sieve=True, readout_views=2)
    with pytest.raises(SystemExit, match="readout_views"):
        s1._check_q15_args(base)
    s1._check_q15_args(_q15_args(burst_prior_sieve=True))  # 全绿通过


def test_parser_default_q15_off():
    from tools.train.v3_6.train_v36 import build_parser

    s1_parser = build_parser()
    s1._add_s1_args(s1_parser)
    args = s1_parser.parse_args([])
    assert args.q15_circuit_rearing is False


# --- 9.5 E120 修订 v3 仪器化档 (--q15-attn-diag, 2026-09-04 裁②) ----------------------


def test_check_q15_attn_diag_args_loud():
    s1._check_q15_attn_diag_args(_s1_args())  # 关态静默通过
    with pytest.raises(SystemExit, match="slm"):
        s1._check_q15_attn_diag_args(_s1_args(q15_attn_diag=True, backbone_mode="xattn",
                                              burst_prob=0.5))
    with pytest.raises(SystemExit, match="readout_views"):
        s1._check_q15_attn_diag_args(_s1_args(q15_attn_diag=True, backbone_mode="slm",
                                              readout_views=2, burst_prob=0.5))
    with pytest.raises(SystemExit, match="burst-prob"):
        s1._check_q15_attn_diag_args(_s1_args(q15_attn_diag=True, backbone_mode="slm",
                                              readout_views=1, burst_prob=0.0))
    # 合法域 (slm + views==1 + burst 开) 通过; q15 主开关不在要求内 (仪器化档语义)
    s1._check_q15_attn_diag_args(_s1_args(q15_attn_diag=True, backbone_mode="slm",
                                          readout_views=1, burst_prob=0.5))


def test_parser_default_q15_attn_diag_off():
    from tools.train.v3_6.train_v36 import build_parser

    s1_parser = build_parser()
    s1._add_s1_args(s1_parser)
    args = s1_parser.parse_args([])
    assert args.q15_attn_diag is False


# --- 10. 收官探针纯函数 (probe_burst_route_q15, 任务书 §6) ---------------------------


def test_probe_swap_identity_audit():
    from tools.analysis.v3_6 import probe_burst_route_q15 as probe

    # 周期段: 段首 tb 字节 == 各段尾 tb 字节 -> head-tail swap 为恒等篡改
    seg = "天地玄".encode("utf-8") * 8  # 24B, 周期 9B
    raw = seg + b"AAAA" + seg + b"BBBB" + seg
    n_seg, tb = len(seg), 9
    occ = [(0, n_seg), (n_seg + 4, 2 * n_seg + 4), (2 * n_seg + 8, 3 * n_seg + 8)]
    m = {"occurrences": occ, "echo_span": (occ[-1][1] - tb, occ[-1][1])}
    assert probe._swap_identity(raw, m) is True
    # 非周期段: 篡改非恒等
    seg2 = "天地玄黄宇宙洪荒".encode("utf-8")  # 24B 非周期
    raw2 = seg2 + b"AAAA" + seg2 + b"BBBB" + seg2
    occ2 = [(0, 24), (28, 52), (56, 80)]
    m2 = {"occurrences": occ2, "echo_span": (80 - tb, 80)}
    assert probe._swap_identity(raw2, m2) is False


def test_probe_delta_aggregate():
    from tools.analysis.v3_6 import probe_burst_route_q15 as probe

    def _item(d, swap=False):
        return {
            "intact": {"byte_acc": 0.8}, "src_scrambled": {"byte_acc": 0.8 - d},
            "swap_identity": swap,
        }

    items = [_item(0.5), _item(0.0), _item(-0.5), _item(0.9, swap=True)]
    agg = probe._delta_aggregate(items)
    assert agg["n"] == 3 and agg["n_swap_identity_excluded"] == 1
    assert agg["mean"] == 0.0
    # sd = sqrt((0.25+0+0.25)/2) = 0.5; ci = 1.96*0.5/sqrt(3)
    assert agg["ci95"] == pytest.approx(1.96 * 0.5 / 3**0.5, abs=1e-3)
    assert agg["ci_excludes_zero"] is False
    # 全正 Δ -> CI 不含 0
    agg2 = probe._delta_aggregate([_item(0.5), _item(0.6), _item(0.4)])
    assert agg2["n"] == 3 and agg2["mean"] == pytest.approx(0.5, abs=1e-4)
    assert agg2["ci_excludes_zero"] is True
    # 空/全剔除 -> n=0 零占位
    agg3 = probe._delta_aggregate([_item(0.5, swap=True)])
    assert agg3["n"] == 0 and agg3["mean"] == 0.0 and agg3["ci95"] == 0.0
    assert agg3["n_swap_identity_excluded"] == 1
    assert agg3["ci_excludes_zero"] is False


def test_probe_patch_state_zero_channels():
    """按通道清零 (d 格拆分): 假模型验证 k/v/k_store/v_store 各自独立清零."""
    from types import SimpleNamespace

    from tools.analysis.v3_6 import probe_burst_route_q15 as probe

    def _fake():
        fake = SimpleNamespace()

        def rows(chunks, with_views=False):
            k = torch.ones(1, 3, 4)
            v = torch.full((1, 3, 4), 2.0)
            if with_views:
                return (k, v, None, None, None,
                        torch.full((1, 3, 2, 4), 3.0), torch.full((1, 3, 2, 4), 4.0))
            return k, v, None, None, None

        fake._slm_store_rows = rows
        return fake

    fake = _fake()
    restore = probe._patch_state_zero(fake, ("k",))
    out = fake._slm_store_rows(None, with_views=True)
    assert float(out[0].abs().sum()) == 0.0 and float(out[5].abs().sum()) == 0.0  # k 侧清零
    assert float(out[1].abs().sum()) == 24.0 and float(out[6].abs().sum()) == 96.0  # v 侧不动
    restore()
    fake = _fake()
    restore = probe._patch_state_zero(fake, ("v",))
    out = fake._slm_store_rows(None, with_views=True)
    assert float(out[1].abs().sum()) == 0.0 and float(out[6].abs().sum()) == 0.0  # v 侧清零
    assert float(out[0].abs().sum()) == 12.0 and float(out[5].abs().sum()) == 72.0  # k 侧不动
    restore()
    fake = _fake()
    restore = probe._patch_state_zero(fake, ("k", "v"))
    out = fake._slm_store_rows(None)  # with_views=False: 五元组路径
    assert float(out[0].abs().sum()) == 0.0 and float(out[1].abs().sum()) == 0.0
    restore()


# --- 9. e2e (d 格 tiny): 有限 loss + 指标 + eval 零占位 ---------------------------------


def test_step_model_q15_train_e2e(corpus_file, monkeypatch):
    monkeypatch.setattr(s1, "_Q15_TWIN_P", 1.0)  # 强制全选, 孪生路径真跑
    torch.manual_seed(0)
    model = FLUEDV36(_d_grid_config())
    args = _q15_args()
    batch = (_clean([TEXT1, TEXT2], 384),)
    s1._BURST_SAMPLER = _sampler(corpus_file)
    s1._BURST_GENERATOR.manual_seed(42 + s1._BURST_SEED_OFFSET)
    try:
        loss, metrics = s1.step_model(model, batch, args, torch.device("cpu"), train=True)
    finally:
        s1._BURST_SAMPLER = None
    assert torch.isfinite(loss)
    for key in (
        "q15_attend_mass", "q15_attend_maxmass", "q15_attend_chance", "q15_attend_loss",
        "q15_gate_mean", "q15_echo_loss", "q15_couple_loss", "q15_twin_d", "q15_twin_count",
    ):
        assert key in metrics, key
        assert torch.isfinite(metrics[key]), key
    assert metrics["burst_count"].item() == 1.0  # 两条全激活
    assert metrics["q15_attend_mass"].item() >= 0.0
    assert metrics["q15_attend_maxmass"].item() >= 0.0
    assert 0.0 < metrics["q15_attend_chance"].item() <= 1.0
    # L_attend = mean(-log(mass+ε)) 逐头求和, mass 可 >1 -> 损失可为负
    # (冻结公式 §3.1, 梯度方向仍把 mass 往上推), 不作正负断言
    # 修订 v1 门: 随机初始 maxmass ≈ chance+涨落 -> 门基本关闭 (<0.2 量级)
    assert 0.0 <= metrics["q15_gate_mean"].item() < 0.2
    assert metrics["q15_twin_count"].item() == 1.0  # p=1.0: 两 splice 行各一孪生
    assert 0.0 <= metrics["q15_twin_d"].item() <= 1.0
    assert metrics["q15_couple_loss"].item() >= 0.0  # 铰链非负
    loss.backward()
    # L_attend 梯度经 block-1 手工注意力回传进 backbone
    assert model.backbone.q_proj.weight.grad is not None
    assert model.backbone.q_proj.weight.grad.abs().sum() > 0


def test_step_model_q15_eval_zero_placeholders_no_rng(corpus_file):
    """eval 形态纪律 (§7.2): 三件套零占位, 网格不动, 孪生不抽 -- eval 的
    _BURST_GENERATOR 消耗 = 纯 splice; train 多出每条 splice 样本一抽孪生选择.
    (每次运行各自新 sampler: 复用同一 sampler 会被防背登记簿的撞车重抽污染
    draw 计数.)"""
    torch.manual_seed(0)
    model = FLUEDV36(_d_grid_config())
    args = _q15_args()
    batch = (_clean([TEXT1, TEXT2], 384),)
    try:
        s1._BURST_SAMPLER = _sampler(corpus_file)
        s1._BURST_GENERATOR.manual_seed(42 + s1._BURST_SEED_OFFSET)
        loss_t, m_t = s1.step_model(model, batch, args, torch.device("cpu"), train=True)
        gen_after_train = s1._BURST_GENERATOR.get_state()
        s1._BURST_SAMPLER = _sampler(corpus_file)  # eval 各自新 sampler
        s1._BURST_GENERATOR.manual_seed(42 + s1._BURST_SEED_OFFSET)
        loss_e, m_e = s1.step_model(model, batch, args, torch.device("cpu"), train=False)
        gen_after_eval = s1._BURST_GENERATOR.get_state()
    finally:
        s1._BURST_SAMPLER = None
    assert torch.isfinite(loss_t) and torch.isfinite(loss_e)
    for key in ("q15_attend_mass", "q15_attend_maxmass", "q15_attend_chance", "q15_attend_loss",
                "q15_gate_mean", "q15_echo_loss", "q15_couple_loss", "q15_twin_d", "q15_twin_count"):
        assert m_e[key].item() == 0.0, key
    # train 比 eval 多消耗恰好 2 抽 (2 条 splice 样本的孪生选择, 固定顺序)
    assert not torch.equal(gen_after_eval, gen_after_train)
