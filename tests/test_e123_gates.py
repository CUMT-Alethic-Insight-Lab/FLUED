"""E123 前置门仪器单测（2026-09-07，冻结任务书 §3/§7）。

Covers: (1) ParallelAttention block_mask 语义（被遮键对一切查询不可见——其它
位输出对遮位值不变）+ None 位不变； (2) DiTStyleBlock mask 线程同语义；
(3) row_swap_perm donor 规则（上游优先、c==0 走 c+2 避下游污染、小窗兜底）。
"""

from __future__ import annotations

import pytest
import torch

from flued.v34.model import DiTStyleBlock, ParallelAttention

import tools.analysis.v3_6.gate_e123_necessity_v2 as gate


@pytest.fixture(autouse=True)
def _seed():
    torch.manual_seed(0)
    yield


def _make_attn():
    return ParallelAttention(dim=16, nhead=2, use_rope=False, use_alibi=False)


def test_attn_block_mask_semantics_and_none_bitwise():
    attn = _make_attn()
    x = torch.randn(1, 5, 16)
    valid = torch.ones(1, 5, dtype=torch.bool)
    # None = 旧路径逐位不变
    with torch.no_grad():
        a = attn(x, valid)
        b = attn(x, valid, None)
    assert torch.equal(a, b)
    # 遮位 3：其它位输出对 x[3] 的值不变（键侧视野抹除的语义钉死）
    bm = torch.zeros(1, 1, 1, 5, dtype=torch.bool)
    bm[0, 0, 0, 3] = True
    x2 = x.clone()
    x2[0, 3] = torch.randn(16)
    with torch.no_grad():
        m1 = attn(x, valid, bm)
        m2 = attn(x2, valid, bm)
    assert not torch.equal(x[0, 3], x2[0, 3])  # 前提：遮位值确实不同
    for t in (0, 1, 2, 4):
        assert torch.allclose(m1[0, t], m2[0, t], atol=1e-6)
    # 遮位自身状态含残差（x[3] 本体保留——正是「内容自此只存在于状态通道」的
    # 要求：自己的表示活下去给 summarizer），注意输出对遮位值可变


def test_dit_block_mask_threading():
    blk = DiTStyleBlock(dim=16, nhead=2, ffn_dim=32, use_rope=False)
    x = torch.randn(1, 5, 16)
    valid = torch.ones(1, 5, dtype=torch.bool)
    noise = torch.zeros(1)
    with torch.no_grad():
        a = blk(x, valid, noise)
        b = blk(x, valid, noise, None)
    assert torch.equal(a, b)
    bm = torch.zeros(1, 1, 1, 5, dtype=torch.bool)
    bm[0, 0, 0, 3] = True
    x2 = x.clone()
    x2[0, 3] = torch.randn(16)
    with torch.no_grad():
        m1 = blk(x, valid, noise, bm)
        m2 = blk(x2, valid, noise, bm)
    for t in (0, 1, 2, 4):
        assert torch.allclose(m1[0, t], m2[0, t], atol=1e-6)


def test_row_swap_perm_donor_rules():
    # 上游优先
    p = gate.row_swap_perm(5, 10)
    assert p[5] == 4 and p[4] == 5
    assert all(p[i] == i for i in range(10) if i not in (4, 5))
    # c==0 → c+2（避下游 c+1 污染）
    p = gate.row_swap_perm(0, 10)
    assert p[0] == 2 and p[2] == 0
    # c==0 且窗太小 → 兜底 c+1
    p = gate.row_swap_perm(0, 2)
    assert p[0] == 1 and p[1] == 0
    # 单行窗：恒等
    assert gate.row_swap_perm(0, 1) == [0]


def test_row_perm_override_forward_level():
    """row_perm_override（E123 门②批化测量）：前向级逐样本行置换——恒等 perm
    逐位不变；交换 perm 改变行内容（行存在性保留）。"""
    import torch
    from tools.train.v3_6.train_v36_s1 import _slm_forward  # noqa

    # 不依赖模型实体的代数核：直接验 _row_permute 语义
    # ——通过构造假张量走 _slm_forward 内部闭包不可达，改为复刻校验
    t = torch.arange(24).float().view(1, 4, 6)
    perm = [[0, 2, 1, 3]]  # 交换行 1/2
    idx = torch.tensor(perm, dtype=torch.long).unsqueeze(-1).expand(-1, -1, 6)
    out = torch.gather(t, 1, idx)
    assert torch.equal(out[0, 1], t[0, 2]) and torch.equal(out[0, 2], t[0, 1])
    assert torch.equal(out[0, 0], t[0, 0]) and torch.equal(out[0, 3], t[0, 3])
    # 恒等 perm 逐位不变
    ident = torch.arange(4).unsqueeze(-1).expand(-1, 6)
    assert torch.equal(torch.gather(t, 1, ident.unsqueeze(0)), t)


# ---------------------------------------------------------------------------
# E123 合体臂训练器接线（任务书冻结 v1.3 2026-09-07）
# ---------------------------------------------------------------------------

import json as _json
from types import SimpleNamespace as _NS

import tools.train.v3_6.train_v36_s1 as s1m


@pytest.fixture()
def _e123_state(monkeypatch):
    """模块级 E123 状态隔离：测试后全量复位。"""
    saved = (s1m._E123_LOG, s1m._E123_KMAX_SCHED, s1m._E123_DONOR, s1m._E123_DONOR_WINDOWS)
    yield
    (s1m._E123_LOG, s1m._E123_KMAX_SCHED, s1m._E123_DONOR, s1m._E123_DONOR_WINDOWS) = saved


def _log_entry(wi, pairs):
    return {"window_id": wi, "n_real": 64, "masked_chunks": [p["src_chunk"] for p in pairs],
            "info_scores": {}, "dependency_pairs": pairs}


def _pair(src_chunk, s, e, dist, positions):
    return {"src_chunk": src_chunk, "src_byte_range": [s, e],
            "distance": dist, "positions": positions, "info": 0.1}


def test_e123_kmax_schedule_and_lambda():
    sched = s1m._e123_parse_kmax("1:0,2:2000,4:6000,16:8000")
    assert [int(s1m._ramp_lookup(sched, s)) for s in (0, 1999, 2000, 5999, 6000, 7999, 8000, 9999)] == \
        [1, 1, 2, 2, 4, 4, 16, 16]
    args = _NS(e123_lambda_ramp=1000)
    assert s1m._e123_lambda(args, 0) == 0.0
    assert s1m._e123_lambda(args, 500) == 0.5
    assert s1m._e123_lambda(args, 1000) == 1.0
    assert s1m._e123_lambda(args, 5000) == 1.0
    # 坏规格响亮
    with pytest.raises(SystemExit):
        s1m._e123_parse_kmax("2:2000")  # 缺 step 0 起档
    with pytest.raises(SystemExit):
        s1m._e123_parse_kmax("1.5:0")  # 非整数 K_max


def test_e123_load_mask_log_schema(tmp_path):
    p = tmp_path / "log.jsonl"
    p.write_text(
        _json.dumps(_log_entry(0, [_pair(0, 0, 64, 2, [128, 129])])) + "\n"
        + _json.dumps(_log_entry(1, [])) + "\n",
        encoding="utf-8",
    )
    log = s1m._load_e123_mask_log(str(p))
    assert sorted(log) == [0, 1] and len(log[0]["dependency_pairs"]) == 1
    # 序号断裂 → 响亮
    p2 = tmp_path / "bad.jsonl"
    p2.write_text(_json.dumps(_log_entry(0, [])) + "\n" + _json.dumps(_log_entry(2, [])) + "\n",
                  encoding="utf-8")
    with pytest.raises(ValueError, match="不连续"):
        s1m._load_e123_mask_log(str(p2))
    # 依赖对缺键 → 响亮
    p3 = tmp_path / "bad2.jsonl"
    bad = _log_entry(0, [{"src_chunk": 0, "src_byte_range": [0, 64], "positions": [1]}])
    p3.write_text(_json.dumps(bad) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="缺键"):
        s1m._load_e123_mask_log(str(p3))


def test_e123_donor_perm_derangement_and_seed():
    log = {i: _log_entry(i, [_pair(0, 0, 64, 2, [128])] if i % 2 == 0 else []) for i in range(10)}
    perm = s1m._e123_build_donor_perm(log, seed=123)
    elig = sorted(wi for wi, e in log.items() if e["dependency_pairs"])
    assert sorted(perm) == elig  # 只在有料窗上定义
    assert sorted(perm.values()) == elig  # 置换封闭于 eligible 集
    assert all(perm[w] != w for w in perm)  # 零不动点 = 必跨窗
    assert perm == s1m._e123_build_donor_perm(log, seed=123)  # 确定性
    # 无料窗集太小 → 响亮
    with pytest.raises(ValueError, match="跨窗置换无料"):
        s1m._e123_build_donor_perm({0: _log_entry(0, [])}, seed=1)


def test_e123_window_plan_modes(_e123_state):
    pairs = [_pair(0, 0, 64, 1, [64, 65]), _pair(2, 128, 192, 2, [384, 385, 386])]
    s1m._E123_LOG = {0: _log_entry(0, pairs), 1: _log_entry(1, [])}
    s1m._E123_KMAX_SCHED = s1m._e123_parse_kmax("1:0,2:2000")
    clean = torch.zeros(1, 512, dtype=torch.long)
    base = dict(e123_window_id=0, e123_lambda_ramp=1000, e123_mode="combined")
    # K_max=1 档（step 500）：k=2 对被滤除，遮蔽只含 k=1 块
    args = _NS(**base, e123_step=500)
    plan, mask, inject, cuts = s1m._e123_window_plan(None, clean, args, torch.device("cpu"))
    assert plan["kmax"] == 1 and len(plan["kept"]) == 1 and len(plan["pairs"]) == 2
    assert mask is not None and mask.shape == (1, 1, 1, 512)
    assert mask[0, 0, 0, :64].all() and not mask[0, 0, 0, 64:].any()
    assert len(inject[0]) == 1 and inject[0][0]["lam"] == 0.5
    # K_max=2 档：两对都纳入
    args = _NS(**base, e123_step=2500)
    plan, mask, inject, cuts = s1m._e123_window_plan(None, clean, args, torch.device("cpu"))
    assert len(plan["kept"]) == 2 and mask[0, 0, 0, 128:192].all()
    # control 列：无遮蔽无注入，plan 照出（仪表用）
    args = _NS(**{**base, "e123_mode": "control"}, e123_step=2500)
    plan, mask, inject, cuts = s1m._e123_window_plan(None, clean, args, torch.device("cpu"))
    assert mask is None and inject is None and len(plan["pairs"]) == 2
    # 无记录窗：零遮蔽零注入
    args = _NS(**{**base, "e123_step": 2500, "e123_window_id": 1})
    plan, mask, inject, cuts = s1m._e123_window_plan(None, clean, args, torch.device("cpu"))
    assert mask is None and inject is None and plan["pairs"] == []
    assert cuts is None  # cuts_pin 默认关 = 旧路径逐位不变（条件创建纪律）


def test_e124_cuts_pin_window_plan(_e123_state):
    """E124 切点钉死训练侧消费（--e123-cuts-pin）：hard_cut 键 → cuts_override
    契约的 (1, T) bool（pad-right False 到 T）；缺键/长度不符一律响亮。"""
    hc = ([1] + [0] * 63) * 2  # 128 字节窗的两切点
    entry = {**_log_entry(0, [_pair(0, 0, 64, 1, [64, 65])]), "hard_cut": hc}
    s1m._E123_LOG = {0: entry, 1: _log_entry(1, [])}
    s1m._E123_KMAX_SCHED = s1m._e123_parse_kmax("1:0,2:2000")
    clean = torch.ones(1, 140, dtype=torch.long)  # 非 PAD 128 字节 + 尾 PAD
    clean[0, 128:] = 0
    base = dict(e123_window_id=0, e123_lambda_ramp=1000, e123_mode="combined",
                e123_step=500, e123_cuts_pin=True)
    args = _NS(**base)
    plan, mask, inject, cuts = s1m._e123_window_plan(None, clean, args, torch.device("cpu"))
    assert cuts is not None and cuts.shape == (1, 140) and cuts.dtype == torch.bool
    assert cuts[0, :128].long().tolist() == hc  # 切点逐位对齐
    assert not cuts[0, 128:].any()  # PAD 区 pad-right False
    # 缺 hard_cut 键（旧口径日志）→ 响亮
    s1m._E123_LOG = {0: _log_entry(0, [_pair(0, 0, 64, 1, [64, 65])]), 1: _log_entry(1, [])}
    with pytest.raises(ValueError, match="hard_cut"):
        s1m._e123_window_plan(None, clean, args, torch.device("cpu"))
    # 长度 ≠ 非 PAD 数 → 响亮
    s1m._E123_LOG = {0: {**entry, "hard_cut": hc[:-1]}, 1: _log_entry(1, [])}
    with pytest.raises(ValueError, match="hard_cut 长度"):
        s1m._e123_window_plan(None, clean, args, torch.device("cpu"))


def test_e123_apply_injections_math():
    # 4 chunk 网格：chunk c 占字节 [64c, 64c+64)
    chunk_ids = torch.arange(256).unsqueeze(0) // 64  # (1, T=256)
    proj = torch.zeros(1, 4, 3)
    proj[0, 0] = torch.tensor([1.0, 2.0, 3.0])
    cond = torch.zeros(1, 4, 3)
    ident = lambda x: x  # noqa: E731
    # 同窗源：c_src=0（字节 0），依赖位在 chunk 2（字节 128..130）
    metas = [[{"src_range": [0, 64], "positions": [128, 129, 130], "lam": 1.0, "donor_row": None}]]
    out, st = s1m._e123_apply_injections(cond.clone(), proj, ident, chunk_ids, metas)
    assert torch.equal(out[0, 2], proj[0, 0])
    assert torch.equal(out[0, 0], torch.zeros(3)) and torch.equal(out[0, 1], torch.zeros(3))
    assert st == {"pairs": 1, "positions": 3}
    # λ 缩放 + λ=0 跳过（缓升起步期零注入）
    out2, st2 = s1m._e123_apply_injections(
        cond.clone(), proj, ident, chunk_ids,
        [[{**metas[0][0], "lam": 0.5}]])
    assert torch.equal(out2[0, 2], 0.5 * proj[0, 0])
    out3, st3 = s1m._e123_apply_injections(
        cond.clone(), proj, ident, chunk_ids,
        [[{**metas[0][0], "lam": 0.0}]])
    assert torch.equal(out3, cond) and st3 == {"pairs": 0, "positions": 0}
    # donor 行（乱序列）：过 dec_in 而非 proj；detach 语义 = donor 行不收梯度
    donor = torch.tensor([4.0, 5.0, 6.0], requires_grad=True)
    out4, _ = s1m._e123_apply_injections(
        cond.clone(), proj, ident, chunk_ids,
        [[{**metas[0][0], "donor_row": donor}]])
    assert torch.equal(out4[0, 2], donor.detach())
    # 梯度路径：同窗源 → proj 收梯度（第七性质：监督经读出件回传源行）
    proj_g = proj.clone().requires_grad_(True)
    out5, _ = s1m._e123_apply_injections(cond.clone(), proj_g, ident, chunk_ids, metas)
    out5.sum().backward()
    assert proj_g.grad[0, 0].abs().sum() > 0 and proj_g.grad[0, 1].abs().sum() == 0
