"""DeltaNet 线性状态读出探针仪器单测（仪器在
tools/analysis/cross_arch/probe_deltanet_state_readout.py；E122 必要性账的
表示侧配套第二把尺子）。

Covers: (1) 样本构造：边界认领确定性（min t）、近程目标位、远程源「整体在
边界前」条款（s+n ≤ b，含边界恰好的合法 case 与越界作废计数）;
(2) fp32 chunk 边界态 vs 逐 token 朴素递推参考（naive.delta_rule_recurrence
语义）逐边界一致 + 零填充终态不变; (3) ridge 探针合成回收：状态线性编码目标
嵌入时 real 探针 cos/top-1 高、对照（打乱配对重训）塌到基线、uplift>0 显著、
特异性（real 探针 × 测试端置换配对）塌回; (4) 符号翻转置换检验方向 + 确定性;
(5) 窗劈分确定性/互斥穷尽 + 距离桶边界 + 全流程两次运行逐字段一致。
"""

from __future__ import annotations

import json
import random

import pytest
import torch

import tools.analysis.cross_arch.probe_deltanet_state_readout as dsr

# ---------------------------------------------------------------------------
# 1. 样本构造
# ---------------------------------------------------------------------------


def _ids_64() -> list[int]:
    ids = [(i * 7 + 13) % 30 for i in range(64)]  # filler（步长 7 与 30 互素）
    ids[0:3] = [30, 31, 32]   # A 源 @0
    ids[8:11] = [50, 51, 52]  # B 源 @8
    ids[21:24] = [60, 61, 62]  # C 源 @21
    ids[24:27] = [60, 61, 62]  # C 重复 @24
    ids[30:33] = [63, 62, 61]  # D 源 @30
    ids[40:43] = [30, 31, 32]  # A 重复 @40
    ids[56:59] = [50, 51, 52]  # B 重复 @56
    return ids


A = (30, 31, 32)
B = (50, 51, 52)
C = (60, 61, 62)
D = (63, 62, 61)
CS = 8


def _sel() -> dict[int, tuple[tuple, int]]:
    return {43: (A, 40), 44: (A, 40), 45: (A, 40),   # A 续尾 → 边界 b=40
            59: (B, 56), 60: (B, 56),                 # B 续尾 → 边界 b=56
            28: (C, 24),                              # C 续尾 → 边界 b=24（源恰好整体在边界前）
            34: (D, 33)}                              # D 续尾 → 边界 b=32（源越界 → 远程作废）


def test_build_window_samples_designation_and_remote_validity():
    ids = _ids_64()
    samples, skipped = dsr.build_window_samples(
        ids, _sel(), n=3, chunk_size=CS, remote_js=(0, 1, 2))
    assert skipped == 1  # D 源 (30..33) 越过边界 b=32 → 远程作废计数
    bounds = [s["boundary"] for s in samples]
    assert bounds == [24, 32, 40, 56]  # 按 chunk 升序、确定性
    by_b = {s["boundary"]: s for s in samples}
    # designated = 该边界内最小 t 的 gram
    assert by_b[24]["gram"] == list(C) and by_b[24]["tail_pos"] == 28
    assert by_b[32]["gram"] == list(D) and by_b[40]["gram"] == list(A)
    assert by_b[56]["gram"] == list(B) and by_b[56]["tail_pos"] == 59
    # 近程目标 = 边界前第 lag token
    for b, s in by_b.items():
        for lag in (1, 2, 3):
            assert s["near"][lag] == (b - lag, ids[b - lag])
    # 远程目标 = designated 源第 j token，距离 = b − (s+j)；C 源 @21，s+n=24≤24 ✓
    assert by_b[24]["remote"] == [(0, 21, 60, 3), (1, 22, 61, 2), (2, 23, 62, 1)]
    assert by_b[40]["remote"] == [(0, 0, 30, 40), (1, 1, 31, 39), (2, 2, 32, 38)]
    assert by_b[56]["remote"] == [(0, 8, 50, 48), (1, 9, 51, 47), (2, 10, 52, 46)]
    assert by_b[32]["remote"] == [] and by_b[32]["source_pos"] == 30  # D 越界
    # 近程不受远程作废影响
    assert by_b[32]["near"][1] == (31, ids[31])


def test_distance_bucket_and_split_determinism():
    assert dsr.distance_bucket(0, 32, 192) == "near"
    assert dsr.distance_bucket(31, 32, 192) == "near"
    assert dsr.distance_bucket(32, 32, 192) == "mid"
    assert dsr.distance_bucket(191, 32, 192) == "mid"
    assert dsr.distance_bucket(192, 32, 192) == "remote"
    a = dsr.split_windows(list(range(40)), 0.5, seed=42)
    b = dsr.split_windows(list(range(40)), 0.5, seed=42)
    assert a == b
    tr, te = a
    assert len(tr) == 20 and len(te) == 20
    assert not set(tr) & set(te) and sorted(tr + te) == list(range(40))
    c = dsr.split_windows(list(range(40)), 0.5, seed=43)
    assert c != a  # 异种子异劈


# ---------------------------------------------------------------------------
# 2. fp32 chunk 边界态 vs 逐 token 朴素递推
# ---------------------------------------------------------------------------


def _token_loop_states(k: torch.Tensor, v: torch.Tensor, beta: torch.Tensor,
                       chunk_size: int) -> torch.Tensor:
    """naive.delta_rule_recurrence 语义的逐 token 参考（fp32）。
    k/v [T,H,K/V]，beta [T,H] → [NS+1,H,K,V]（每 chunk 边界一个）。"""
    t_len, h, kd = k.shape
    vd = v.shape[-1]
    s = torch.zeros(h, kd, vd)
    out = [s.clone()]
    for t in range(t_len):
        k_t, v_t, b_t = k[t].float(), v[t].float(), beta[t].float()
        pred = (s * k_t.unsqueeze(-1)).sum(-2)          # [H,V] = Sᵀk
        v_new = (v_t - pred) * b_t.unsqueeze(-1)
        s = s + k_t.unsqueeze(-1) * v_new.unsqueeze(-2)
        if (t + 1) % chunk_size == 0:
            out.append(s.clone())
    return torch.stack(out)


@pytest.mark.parametrize("t_len,cs", [(48, 16), (32, 16), (64, 64), (24, 8)])
def test_chunk_boundary_states_match_token_loop(t_len: int, cs: int):
    torch.manual_seed(t_len * 100 + cs)
    h, kd, vd = 2, 8, 6
    k = torch.nn.functional.normalize(torch.randn(t_len, h, kd), dim=-1)
    v = torch.randn(t_len, h, vd)
    beta = torch.rand(t_len, h)
    mine = dsr.delta_rule_chunk_boundary_states(k, v, beta, cs)
    ref = _token_loop_states(k, v, beta, cs)
    assert mine.shape == ref.shape == ((t_len + cs - 1) // cs + 1, h, kd, vd)
    assert torch.allclose(mine, ref, atol=1e-3, rtol=1e-3)


def test_chunk_boundary_states_padding_keeps_final_state():
    """T 非整 chunk：零填充（β=0 → 无更新）终态 == 逐 token 跑满 T 的终态。"""
    torch.manual_seed(7)
    t_len, cs, h, kd, vd = 50, 16, 2, 8, 6
    k = torch.nn.functional.normalize(torch.randn(t_len, h, kd), dim=-1)
    v = torch.randn(t_len, h, vd)
    beta = torch.rand(t_len, h)
    mine = dsr.delta_rule_chunk_boundary_states(k, v, beta, cs)
    # 参考：逐 token 全程跑（终态独立于边界记录点）
    s = torch.zeros(h, kd, vd)
    bounds = [s.clone()]
    for t in range(t_len):
        kt, vt, bt = k[t].float(), v[t].float(), beta[t].float()
        pred = (s * kt.unsqueeze(-1)).sum(-2)
        v_new = (vt - pred) * bt.unsqueeze(-1)
        s = s + kt.unsqueeze(-1) * v_new.unsqueeze(-2)
        if (t + 1) % cs == 0:
            bounds.append(s.clone())
    ref = torch.stack(bounds)
    assert mine.shape[0] == 5 and ref.shape[0] == 4  # mine 多一个 pad 末边界
    assert torch.allclose(mine[:-1], ref, atol=1e-3, rtol=1e-3)
    assert torch.allclose(mine[-1], s, atol=1e-3, rtol=1e-3)  # pad 无更新


# ---------------------------------------------------------------------------
# 3. ridge 探针合成回收 + 对照塌回
# ---------------------------------------------------------------------------


def _synthetic_probe_world(n_win: int = 10, per_win: int = 9, d: int = 32,
                           e_dim: int = 8, seed: int = 0):
    """状态线性编码目标嵌入的合成世界：每个样本一行状态 x，三个探针目标
    （near_lag1 / remote_j0 / remote_j1）各挂一套线性映射 W。返回
    (x_by_win, samples_by_win, emb)。"""
    torch.manual_seed(seed)
    n = n_win * per_win
    x_all = torch.randn(n, d)
    ys = {}
    for key in ("near1", "r0", "r1"):
        w = torch.randn(d, e_dim) / 8.0
        ys[key] = x_all @ w + 0.02 * torch.randn(n, e_dim)
    emb = torch.randn(1000, e_dim) * 1e-3
    x_by_win, samples_by_win = {}, {}
    dists = [10, 100, 300]  # 覆盖 near/mid/remote 三桶
    for w in range(n_win):
        rows = slice(w * per_win, (w + 1) * per_win)
        x_by_win[w] = x_all[rows].clone()
        samples = []
        for i in range(per_win):
            gi = w * per_win + i
            tid_n, tid_r0, tid_r1 = 100 + gi, 400 + gi, 700 + gi
            emb[tid_n] = ys["near1"][gi]
            emb[tid_r0] = ys["r0"][gi]
            emb[tid_r1] = ys["r1"][gi]
            dist = dists[gi % 3]
            samples.append({
                "chunk": i, "boundary": i * 8, "tail_pos": i * 8 + 3,
                "gram": [1, 2, 3], "repeat_pos": i * 8, "source_pos": 0,
                "near": {1: (0, tid_n), 2: (0, 999), 3: (0, 998)},
                "remote": [(0, 0, tid_r0, dist), (1, 0, tid_r1, dist + 1)],
            })
        samples_by_win[w] = samples
    return x_by_win, samples_by_win, emb


def test_ridge_recovery_control_uplift_and_specificity():
    x_by_win, samples_by_win, emb = _synthetic_probe_world(n_win=16, per_win=6)
    tr, te = dsr.split_windows(sorted(x_by_win), 0.5, seed=7)
    # λ 取小：单测 D=32 与 N 同量级、特征值 MP 散布大，λ=1 的非均匀收缩会压 cos
    # 读数（生产 D=262144 ≫ N 特征值聚集在 1，默认 λ=1 无此效应——口径见 summary）
    res = dsr.run_layer_probes(
        x_by_win, samples_by_win, tr, te, emb, lam=0.01, seed=42, layer=0,
        near_lags=(1,), n_remote_js=2, near_cut=32, remote_cut=192, n_perm=256)

    near = res["near_lag1"]
    assert near["cos"]["real"] > 0.9       # 线性内容被 real 探针回收
    assert near["cos"]["uplift"] > 0.6     # 对照（打乱配对重训）塌回 → uplift 大
    assert near["cos"]["ctrl"] < 0.6
    assert near["cos"]["perm"]["p"] <= 0.05
    assert near["acc"]["real"] > 0.9       # 嵌入最近邻 top-1 全对
    assert near["acc"]["uplift"] > 0.5
    assert near["chance"] == pytest.approx(1 / near["n_candidates"])
    assert near["cos_real_shuffled_test"] < near["cos"]["real"] - 0.5  # 特异性

    for jname in ("remote_j0", "remote_j1"):
        r = res[jname]
        assert r["cos"]["real"] > 0.9
        assert r["cos"]["uplift"] > 0.6
        assert r["cos"]["perm"]["p"] <= 0.05
        assert r["acc"]["real"] > 0.9
        # 距离桶：合成距离覆盖三桶，计数守恒
        buckets = r["by_distance"]
        assert set(buckets) == {"near", "mid", "remote"}
        assert sum(b["n"] for b in buckets.values()) == r["test_n"]
        # 线性编码与距离无关 → 各桶 real cos 都高（桶分层不翻转结论）
        assert all(b["cos_real"] > 0.85 for b in buckets.values())

    # 本世界全窗有 remote → 该探针 train/test 全量（排除语义另测）
    assert res["remote_j0"]["train_n"] == len(tr) * 6
    assert res["remote_j0"]["test_n"] == len(te) * 6


def test_remote_windows_without_source_excluded_honestly():
    """部分窗远程目标作废（remote 空）→ 这些窗从该探针的 train/test 排除，
    近程探针不受影响。"""
    x_by_win, samples_by_win, emb = _synthetic_probe_world(n_win=6, per_win=4,
                                                           d=16, e_dim=8)
    for w in (1, 4):  # 两个窗全部远程作废
        for s in samples_by_win[w]:
            s["remote"] = []
    tr, te = dsr.split_windows(sorted(x_by_win), 0.5, seed=3)
    res = dsr.run_layer_probes(
        x_by_win, samples_by_win, tr, te, emb, lam=0.01, seed=42, layer=0,
        near_lags=(1,), n_remote_js=1, near_cut=32, remote_cut=192, n_perm=64)
    assert res["near_lag1"]["train_n"] == len(tr) * 4  # 近程不受影响
    invalid = {1, 4}
    exp_tr = len([w for w in tr if w not in invalid]) * 4
    exp_te = len([w for w in te if w not in invalid]) * 4
    assert res["remote_j0"]["train_n"] == exp_tr  # 作废窗从 train/test 双侧诚实排除
    assert res["remote_j0"]["test_n"] == exp_te
    assert res["remote_j0"]["test_n"] > 0 and res["remote_j0"]["train_n"] > 0
    # 剩余窗照常回收（本测重点=排除记账；回收强度主测已盖，12 样本小世界阈值放宽）
    assert res["remote_j0"]["cos"]["real"] > 0.7


# ---------------------------------------------------------------------------
# 4. 符号翻转置换检验：方向 + 确定性
# ---------------------------------------------------------------------------


def test_signflip_direction_and_determinism():
    all_pos = dsr.signflip_p([3.0, 2.0, 4.0, 1.0, 5.0, 2.5, 3.5, 1.5], 999, 0)
    # 全正 → 只有随机抽到的恒等置换追平观测（保守 +1 约定）→ p 落底
    assert all_pos["p"] < 0.01
    zeros = dsr.signflip_p([0.0] * 12, 999, 0)
    assert zeros["p"] == 1.0  # 零差 → 无证据
    mixed = dsr.signflip_p([1.0, -1.0] * 8, 2001, 0)
    assert mixed["p"] > 0.2  # 均值 0 → 不显著
    slightly_pos = dsr.signflip_p([0.1, -0.05] * 10, 4999, 0)
    assert slightly_pos["p"] > 0.05  # 弱信号不误报
    a = dsr.signflip_p([1.0, 2.0, 0.5, 0.3, 2.0, 1.0], 500, 11)
    b = dsr.signflip_p([1.0, 2.0, 0.5, 0.3, 2.0, 1.0], 500, 11)
    assert a == b  # 同种子逐字段确定
    assert a["n_windows"] == 6 and a["obs"] == pytest.approx(6.8 / 6)
    assert dsr.signflip_p([], 100, 0) is None


# ---------------------------------------------------------------------------
# 5. 端到端确定性（探针核：同输入两次运行逐字段一致）
# ---------------------------------------------------------------------------


def test_layer_probes_end_to_end_deterministic():
    x_by_win, samples_by_win, emb = _synthetic_probe_world(
        n_win=6, per_win=4, d=32, seed=5)
    tr, te = dsr.split_windows(sorted(x_by_win), 0.5, seed=9)
    kw = dict(near_lags=(1, 3), n_remote_js=2, near_cut=32, remote_cut=192,
              n_perm=64)
    r1 = dsr.run_layer_probes(x_by_win, samples_by_win, tr, te, emb, 1.0, 42, 3,
                              **kw)
    r2 = dsr.run_layer_probes(x_by_win, samples_by_win, tr, te, emb, 1.0, 42, 3,
                              **kw)
    assert json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)
    # 层号进种子：不同层 ctrl/p 序列不同（不共享随机流）
    r_other = dsr.run_layer_probes(x_by_win, samples_by_win, tr, te, emb, 1.0,
                                   42, 4, **kw)
    assert (r_other["near_lag1"]["cos"]["ctrl"]
            != r1["near_lag1"]["cos"]["ctrl"]) or (
        r_other["near_lag1"]["cos"]["perm"]["p"]
        != r1["near_lag1"]["cos"]["perm"]["p"])


def test_parse_int_list():
    assert dsr.parse_int_list("all") is None
    assert dsr.parse_int_list(" ALL ") is None
    assert dsr.parse_int_list("0,5,23") == [0, 5, 23]
    assert dsr.parse_int_list("7") == [7]
    with pytest.raises(SystemExit):
        dsr.parse_int_list(" , ")
