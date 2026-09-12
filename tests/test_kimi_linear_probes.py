"""Kimi-Linear 仪器单测（仪器在 tools/analysis/v3_6/probe_kimi_linear_*.py；
kimi122 跨架构复证臂，DeltaNet 臂 e122/dsr 的移植适配）。

覆盖（全部 mock 小张量，无 GPU、无 fla、无权重、无网络）：
(1) 层号工具 1 基表→0 基层号；(2) MLA SDPA shim 数学等价（含分块一致性）;
(3) fp32 KDA 边界态 vs 独立标量三重循环朴素参考（naive_recurrent_kda 语义）逐
边界一致 + initial_state 续算 + 部分末块；(4) 终态对拍哨兵（超阈 RuntimeError
响亮）；(5) L2 归一；(6) linear cache 快照/置零/恢复（FakeCache，含 None 槽响亮）；
(7) 解离计分位选择链（remote/local 判据、local-wins 冲突、重叠计数、确定性）;
(8) 窗 sums 与逐位 NLL 数学；(9) zero-layers 解析；(10) 三个 CLI --help 退出码。
"""

from __future__ import annotations

import math
import sys
from types import SimpleNamespace

import pytest
import torch

from tools.analysis.v3_6 import probe_kimi_linear_load as kload
from tools.analysis.v3_6 import probe_kimi_linear_state_surgery as ksurg
from tools.analysis.v3_6 import probe_kimi_linear_book as kbook
from tools.analysis.v3_6 import probe_kimi_linear_state_readout as kread


# ---------------------------------------------------------------------------
# 1. 层号工具
# ---------------------------------------------------------------------------


def test_kda_layer_indices_1based_to_0based():
    cfg = SimpleNamespace(linear_attn_config={
        "kda_layers": [1, 2, 4, 8], "full_attn_layers": [3, 5, 6, 7]})
    assert kload.kda_layer_indices(cfg) == [0, 1, 3, 7]
    assert kload.full_attn_layer_indices(cfg) == [2, 4, 5, 6]
    assert kload.kda_layer_indices(SimpleNamespace(linear_attn_config=None)) == []
    # 48B 真实口径：20 KDA + 7 MLA，交集空、并集满 27
    kda = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19, 21, 22, 23, 25, 26]
    full = [4, 8, 12, 16, 20, 24, 27]
    assert len(kload.kda_layer_indices(SimpleNamespace(linear_attn_config={
        "kda_layers": kda, "full_attn_layers": full}))) == 20
    assert not set(kda) & set(full)


# ---------------------------------------------------------------------------
# 2. MLA SDPA shim 数学等价
# ---------------------------------------------------------------------------


def test_sdpa_attention_forward_matches_eager_math():
    torch.manual_seed(0)
    b, h, q_len, d, dv = 1, 2, 5, 8, 6
    q = torch.randn(b, h, q_len, d)
    k = torch.randn(b, h, q_len, d)
    v = torch.randn(b, h, q_len, dv)
    scale = d ** -0.5
    mask = torch.zeros(1, 1, q_len, q_len)
    mask[..., :, :] = torch.where(
        torch.triu(torch.ones(q_len, q_len, dtype=torch.bool), 1),
        torch.tensor(-1e9), torch.tensor(0.0))
    out, w = kload.sdpa_attention_forward(None, q, k, v, attention_mask=mask,
                                          scaling=scale, q_chunk=3)
    # 手工 eager 数学：softmax(QKᵀ·scale + M)V
    attn = torch.softmax(q @ k.transpose(-1, -2) * scale + mask, dim=-1)
    ref = (attn @ v).transpose(1, 2)  # [B,q,H,dv]
    assert w is None and out.shape == ref.shape
    assert torch.allclose(out, ref, atol=1e-5)
    # 分块一致性：q_chunk 变化不改变逐位结果（softmax 行独立）
    out_full, _ = kload.sdpa_attention_forward(None, q, k, v,
                                               attention_mask=mask,
                                               scaling=scale, q_chunk=10**9)
    assert torch.allclose(out, out_full, atol=1e-6)
    # 无 mask（KDA 侧 linear_attn_mask=None 场景）
    out_nm, _ = kload.sdpa_attention_forward(None, q, k, v, scaling=scale)
    attn_nm = torch.softmax(q @ k.transpose(-1, -2) * scale, dim=-1)
    assert torch.allclose(out_nm, (attn_nm @ v).transpose(1, 2), atol=1e-5)


# ---------------------------------------------------------------------------
# 3. fp32 KDA 边界态 vs 独立朴素参考
# ---------------------------------------------------------------------------


def _naive_boundary_states_ref(k, v, g, beta, chunk, initial_state=None):
    """独立标量三重循环参考（naive_recurrent_kda 语义；float64）。"""
    t_len, h, kd = k.shape
    vd = v.shape[-1]
    s = (torch.zeros(h, kd, vd, dtype=torch.float64) if initial_state is None
         else initial_state.clone().to(torch.float64))
    states = [s.clone()]
    for t in range(t_len):
        for hh in range(h):
            for kk in range(kd):
                s[hh, kk, :] *= math.exp(float(g[t, hh, kk]))
            ks = [sum(float(k[t, hh, x]) * float(s[hh, x, vv])
                      for x in range(kd)) for vv in range(vd)]
            for vv in range(vd):
                upd = float(v[t, hh, vv]) - ks[vv]
                for x in range(kd):
                    s[hh, x, vv] += float(beta[t, hh]) * float(k[t, hh, x]) * upd
        if (t + 1) % chunk == 0:
            states.append(s.clone())
    if t_len % chunk:
        states.append(s.clone())
    return torch.stack(states)


def test_kda_chunk_boundary_states_match_naive_reference():
    torch.manual_seed(1)
    t_len, h, kd, vd, chunk = 6, 2, 3, 4, 4
    k = torch.randn(t_len, h, kd)
    v = torch.randn(t_len, h, vd)
    g = -torch.rand(t_len, h, kd) * 0.5  # log 域衰减 ≤ 0
    beta = torch.rand(t_len, h)
    states = kload.kda_chunk_boundary_states(k, v, g, beta, chunk,
                                             apply_l2norm=False)
    ref = _naive_boundary_states_ref(k, v, g, beta, chunk)
    assert states.shape == ref.shape == (3, h, kd, vd)  # 1 + 边界@4 + 部分末块
    assert torch.allclose(states.double(), ref, atol=1e-4)
    # initial_state 续算
    s0 = torch.randn(h, kd, vd)
    states2 = kload.kda_chunk_boundary_states(k, v, g, beta, chunk,
                                              initial_state=s0,
                                              apply_l2norm=False)
    ref2 = _naive_boundary_states_ref(k, v, g, beta, chunk, initial_state=s0)
    assert torch.allclose(states2.double(), ref2, atol=1e-4)
    # 整除末块（T=8, chunk=4 → 3 槽无部分块）
    states3 = kload.kda_chunk_boundary_states(
        torch.randn(8, h, kd), torch.randn(8, h, vd),
        -torch.rand(8, h, kd) * 0.5, torch.rand(8, h), chunk, apply_l2norm=False)
    assert states3.shape[0] == 3


def test_kda_chunk_boundary_states_accepts_unit_batch_capture():
    """捕获直出带 B=1 batch 维（[1,T,H,*]）→ 入口挤掉；非 1 batch 响亮拒。"""
    torch.manual_seed(7)
    k = torch.randn(6, 2, 3)
    v = torch.randn(6, 2, 4)
    g = -torch.rand(6, 2, 3) * 0.5
    beta = torch.rand(6, 2)
    ref = kload.kda_chunk_boundary_states(k, v, g, beta, 4, apply_l2norm=False)
    got = kload.kda_chunk_boundary_states(
        k.unsqueeze(0), v.unsqueeze(0), g.unsqueeze(0), beta.unsqueeze(0),
        4, apply_l2norm=False)
    assert torch.equal(got, ref)
    with pytest.raises(ValueError, match="维度不符"):
        kload.kda_chunk_boundary_states(
            torch.randn(2, 6, 2, 3), v.unsqueeze(0), g.unsqueeze(0),
            beta.unsqueeze(0), 4, apply_l2norm=False)


def test_kda_l2norm_unit_norm():
    x = torch.randn(7, 3, 16)
    y = kload.kda_l2norm(x)
    assert y.dtype == torch.float32
    assert torch.allclose(y.norm(dim=-1), torch.ones(7, 3), atol=1e-5)


def test_extract_sentinel_passes_and_fires():
    torch.manual_seed(2)
    t_len, h, kd, chunk = 8, 2, 4, 4
    k, v = torch.randn(t_len, h, kd), torch.randn(t_len, h, vd := 5)
    g, beta = -torch.rand(t_len, h, kd) * 0.3, torch.rand(t_len, h)
    states = kload.kda_chunk_boundary_states(k, v, g, beta, chunk,
                                             apply_l2norm=True)
    rec = {"k": k, "v": v, "g": g, "beta": beta, "l2": True,
           "kernel_final_state": states[-1].unsqueeze(0)}
    outs, verr = kload.extract_kda_boundary_states([rec], chunk, tol_rel=0.05)
    assert outs[0].shape == states.shape and verr[0]["rel_err"] < 1e-6
    bad = dict(rec, kernel_final_state=(states[-1] * 1.5).unsqueeze(0))
    with pytest.raises(RuntimeError, match="对拍失败"):
        kload.extract_kda_boundary_states([bad], chunk, tol_rel=0.05)


# ---------------------------------------------------------------------------
# 4. linear cache 快照/置零/恢复（FakeCache）
# ---------------------------------------------------------------------------


class FakeCache:
    def __init__(self):
        self.key_cache = [torch.randn(1, 2, 4, 8), None, torch.randn(1, 2, 3, 8)]
        self.value_cache = [torch.randn(1, 2, 4, 6), None, torch.randn(1, 2, 3, 6)]
        self.conv_states = [None, (torch.randn(1, 4, 2), torch.randn(1, 4, 2),
                                   torch.randn(1, 4, 2)), None]
        self.recurrent_states = [torch.randn(1, 2, 3, 3), torch.randn(1, 2, 3, 3),
                                 None]


def test_snapshot_zero_restore_fakecache():
    c = FakeCache()
    snap = kload.snapshot_linear_cache(c)
    # 置零层 0（recurrent 存在）与层 1；层 2 为 None → 响亮拒绝
    assert kload.zero_kda_recurrent_states(c, [0, 1]) == 2
    assert torch.all(c.recurrent_states[0] == 0)
    assert torch.all(c.recurrent_states[1] == 0)
    c.recurrent_states[2] = None
    with pytest.raises(RuntimeError, match="None"):
        kload.zero_kda_recurrent_states(c, [2])
    # conv 同置零开关
    c2 = FakeCache()
    conv_before = c2.conv_states[1][0].clone()
    kload.zero_kda_recurrent_states(c2, [1], conv_too=True)
    assert torch.all(c2.conv_states[1][0] == 0) and torch.all(conv_before != 0)
    # 恢复逐位一致（含 None 槽）
    kload.restore_linear_cache(c, snap)
    assert torch.equal(c.key_cache[0], snap["key_cache"][0])
    assert torch.equal(c.recurrent_states[0], snap["recurrent_states"][0])
    assert c.recurrent_states[2] is None and c.conv_states[0] is None
    assert torch.equal(c.conv_states[1][1], snap["conv_states"][1][1])


# ---------------------------------------------------------------------------
# 5. 解离计分位选择链
# ---------------------------------------------------------------------------


def _distinct_filler(n: int, start: int = 200) -> list[int]:
    return list(range(start, start + n))


def test_select_positions_pure_remote():
    # A=(30,31,32) 源@0（prefix），suffix 重复@40 → remote 尾位 {43,44}
    ids = _distinct_filler(64)
    ids[0:3] = [30, 31, 32]
    ids[40:43] = [30, 31, 32]
    remote, local, cnt = ksurg.select_dissociation_positions(
        ids, split=32, n=3, tail=2, remote_cut=8, local_cut=5)
    assert remote == {43: ((30, 31, 32), 40), 44: ((30, 31, 32), 40)}
    assert local == {} and cnt["n_remote"] == 2 and cnt["n_local"] == 0
    # prefix 内重复（@24）不计（< split）
    ids[24:27] = [30, 31, 32]
    remote2, _local2, _ = ksurg.select_dissociation_positions(
        ids, split=32, n=3, tail=2, remote_cut=8, local_cut=5)
    assert remote2 == remote


def test_select_positions_pure_local():
    # B=(40,41,42) 一对近邻出现 @50,@53（间隔 0 ≤ local_cut）→ local 尾位 {56,57}
    ids = _distinct_filler(64)
    ids[50:53] = [40, 41, 42]
    ids[53:56] = [40, 41, 42]
    remote, local, cnt = ksurg.select_dissociation_positions(
        ids, split=32, n=3, tail=2, remote_cut=8, local_cut=5)
    assert remote == {}
    assert local == {56: ((40, 41, 42), 53), 57: ((40, 41, 42), 53)}
    assert cnt["n_local"] == 2
    # 距离超 local_cut 的第二次出现不算 local：@50 与 @58（58−53=5 > 5 不行，用 6）
    ids2 = _distinct_filler(70)
    ids2[50:53] = [40, 41, 42]
    ids2[59:62] = [40, 41, 42]  # 59−53=6 > 5 → 非 local；59 > split → remote? s=50 ≥… s+n=53 > 32 → 非 remote
    remote2, local2, _ = ksurg.select_dissociation_positions(
        ids2, split=32, n=3, tail=2, remote_cut=8, local_cut=5)
    assert local2 == {} and remote2 == {}


def test_select_positions_local_wins_conflict():
    # 同 gram 三连出现（n=2 < tail=5，尾位带状重叠）：首现 remote、后现 local
    # → 冲突尾位 local 优先（保守口径：remote 集不得含任何有近旁证据的位）。
    # G=(7,8) @3（prefix 源）、@10、@12、@14；split=6、tail=5、remote_cut=5、
    # local_cut=1：p=10 纯 remote（尾位 12..16）；p=12 local（尾位 14..18，
    # 其中 14/15/16 压 remote → local-wins×3）；p=14 local（尾位 16..20，
    # 其中 16/17/18 已归 local → 重叠×3）。
    ids = _distinct_filler(24)
    ids[3:5] = [7, 8]
    ids[10:12] = [7, 8]
    ids[12:14] = [7, 8]
    ids[14:16] = [7, 8]
    remote, local, cnt = ksurg.select_dissociation_positions(
        ids, split=6, n=2, tail=5, remote_cut=5, local_cut=1)
    assert set(remote) == {12, 13}
    assert set(local) == {14, 15, 16, 17, 18, 19, 20}
    assert not set(remote) & set(local)  # 冲突位归 local，remote 集干净
    # 计数：p=10 remote 5；p=12 local 5（3 wins 压 remote）+p=14 local 5（3 ovl）
    # +交叉 gram (8,7)@13（相邻 span 衍生）local 5 全 ovl → overlap=3+5=8
    assert cnt == {"n_remote": 5, "n_local": 7, "n_overlap": 8,
                   "n_local_wins_over_remote": 3}


def test_select_positions_determinism():
    torch.manual_seed(3)
    ids = torch.randint(0, 50, (128,)).tolist()
    a = ksurg.select_dissociation_positions(ids, 64, 3, 3, 32, 8)
    b = ksurg.select_dissociation_positions(ids, 64, 3, 3, 32, 8)
    assert a == b


# ---------------------------------------------------------------------------
# 6. 窗 sums 与逐位 NLL 数学
# ---------------------------------------------------------------------------


def test_suffix_position_nll_matches_manual():
    torch.manual_seed(4)
    pre_row = torch.randn(50)
    suf_logits = torch.randn(1, 4, 50)
    suf_ids = [3, 7, 1, 9]
    nll = ksurg.suffix_position_nll(pre_row, suf_logits, suf_ids)
    assert len(nll) == 4
    assert nll[0] == -torch.log_softmax(pre_row.float(), -1)[3].item()
    assert nll[2] == -torch.log_softmax(suf_logits[0, 1].float(), -1)[1].item()


def test_build_window_sums_math():
    base = [None, 1.0, 2.0, 3.0, 4.0, 5.0]
    zero = [None, 1.5, 2.5, 9.0, 4.0, 7.0]
    remote = {2: (("a",), 1), 3: (("b",), 1)}
    local = {5: (("c",), 1)}
    sums = ksurg.build_window_sums(base, zero, remote, local)
    assert sums["n_sel"] == 2 and sums["sel_d_b1"] == pytest.approx(0.5 + 6.0)
    assert sums["n_ctl"] == 1 and sums["ctl_d_b1"] == pytest.approx(2.0)
    assert sums["n_strong"] == 1  # 仅 remote 位 Δ=6.0 ≥ 1 nat；local 位不计数
    # split ≠ 0：tails 键为全窗绝对位 t，nll 为 suffix 局部坐标（j = t − split）；
    # j 越界位跳过（split=3 时 t=2 → j=−1）
    sums2 = ksurg.build_window_sums(base, zero,
                                    {2: (("x",), 0), 4: (("a",), 1)},
                                    {5: (("c",), 1)}, split=3)
    assert sums2["n_sel"] == 1 and sums2["sel_d_b1"] == pytest.approx(0.5)
    assert sums2["n_ctl"] == 1 and sums2["ctl_d_b1"] == pytest.approx(0.5)


def test_bootstrap_contrast_sign_separation():
    # remote 全正、local 全负 → contrast > 0 且 CI 不含 0
    wins = [{"n_sel": 2, "sel_d_b1": 2.0, "n_strong": 0, "n_ctl": 2, "ctl_d_b1": -2.0}
            for _ in range(8)]
    boot = kbook.e122.bootstrap_contrast(wins, n_boot=200, seed=1)
    assert boot["point"] > 0 and boot["ci_excludes_zero"]


# ---------------------------------------------------------------------------
# 7. zero-layers 解析与仪器模块口径
# ---------------------------------------------------------------------------


def test_resolve_zero_layers():
    kda = [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18, 20, 21, 22, 24, 25]
    assert ksurg.resolve_zero_layers("kda", kda, 27) == kda
    assert ksurg.resolve_zero_layers("early", kda, 27) == [0, 1, 2, 4, 5, 6, 8]
    assert ksurg.resolve_zero_layers("mid", kda, 27) == [9, 10, 12, 13, 14, 16, 17]
    assert ksurg.resolve_zero_layers("deep", kda, 27) == [18, 20, 21, 22, 24, 25]
    assert ksurg.resolve_zero_layers("3,7", kda, 27) == [3, 7]
    with pytest.raises(SystemExit):
        ksurg.resolve_zero_layers("", kda, 27)


def test_readout_module_wiring():
    # 仪器口径一致性：状态维、复用 dsr 探针核心、probe-layers 解析拒绝 MLA 层
    assert kload.STATE_DIM_PER_BOUNDARY == 32 * 128 * 128
    assert hasattr(kread.dsr, "probe_one") and hasattr(kread.dsr, "run_layer_probes")
    kda = [0, 1, 3]
    assert kread.parse_int_list("kda", kda) == kda
    assert kread.parse_int_list("1,2", kda) == [1, 2]
    with pytest.raises(SystemExit, match="MLA"):
        kread.parse_int_list("all", kda)
    with pytest.raises(SystemExit):
        kread.parse_int_list("", kda)


def test_map_states_to_layers_capture_order():
    # 捕获序（20 条 records）→ 绝对层号（含空洞的 KDA 层表）：绝对层号直接索引
    # states_all 会在层 24/25 处 IndexError（2026-09-13 连夜实证）
    kda = [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18, 20, 21, 22, 24, 25]
    states = [torch.full((1,), float(i)) for i in range(len(kda))]
    m = kread.map_states_to_layers(kda, states)
    assert set(m) == set(kda)
    assert m[25].item() == 19.0 and m[24].item() == 18.0 and m[0].item() == 0.0
    with pytest.raises(RuntimeError, match="捕获层数"):
        kread.map_states_to_layers(kda, states[:19])


def test_kbook_reuses_e122_machinery():
    # 必要性账 = e122 选择/手术/判读原样复用（不复制不分叉的结构性断言）
    for fn in ("run_window", "plan_window_surgery", "bootstrap_contrast",
               "build_rare_table", "build_replacement_pool", "verdict",
               "cross_segment_occurrences", "select_tail_positions"):
        assert hasattr(kbook.e122, fn), fn
    assert kbook.STRONG_LINE_NAT == kbook.e122.STRONG_LINE_NAT == 1.0


# ---------------------------------------------------------------------------
# 8. CLI --help 冒烟（argparse 层，无模型/语料 IO）
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("mod", ["kbook", "kread", "ksurg"])
def test_cli_help_exits_zero(mod):
    module = {"kbook": kbook, "kread": kread, "ksurg": ksurg}[mod]
    old = sys.argv
    try:
        sys.argv = ["prog", "--help"]
        with pytest.raises(SystemExit) as ei:
            module.main()
        assert ei.value.code == 0
    finally:
        sys.argv = old
