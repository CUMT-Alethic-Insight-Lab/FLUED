"""E124 硬预算检索门（budget gate）单测（任务书冻结 v1.0, 2026-09-09）。

门语义（flued/v36/model.py SLMBackbone）: block-1 cross-read 上，部署查询先对
index(K) 行打分，按逐样本预算 k_b 取 top-k 命中的 memory(V) 行做可学 α-entmax
加权；未命中行权重结构性恰为零。预算 = round(n_real·(1-p) + k_final·p)
clamp[1, n_real]（rt_budget 绝对覆写优先）；全量预算（退火起点 p=0）整体
bypass 走 legacy SDPA 路径 = 门关逐位一致（条件创建纪律 + 冒烟条款①锚）。
α = 1 + softplus(e124_alpha_raw)，确定性常数初始化不耗 RNG 流（gate-on/off
两态其余权重逐位一致的可检前提）。a 格限定（k=index ∧ v=memory），其余格
响亮报错。

Covers: (1) 同 seed 关/开两模型 state_dict 仅差 backbone.e124_alpha_raw，且
退火起点（progress=0 全量预算）前向逐位一致；(2) 硬模式（rt_hard=True,
rt_budget=2）命中集寄存 last_e124_hit、top-k 构造命中数恰 = min(k, 候选数)、
非命中恰零（非零 ⊆ 命中集，条款①否决项）、命中集 ⊆ 因果候选集、α-entmax
命中集内稀疏化为设计行为（非零数 ≤ 命中数）、last_e124_k 记录；(3) 软模式
（rt_hard=False）backward 梯度通路：backbone.q_proj / backbone.align_k /
summarizer.index_ffn / e124_alpha_raw 均非零有限，且软门无离散命中集
（last_e124_hit is None）；(4) _e124_budget 退火曲线 p=0/0.5/1 与
rt_budget 覆写/上下限钳制；(5) 非 a 格（v_row_source="state"）构造期响亮报错。

夹具：tests.test_v37_slm.tiny_config（默认即 slm a 格 index/memory），
backbone 级直接调用（同 test_q15_circuit_rearing 口径：只验接线/代数）。
"""

from __future__ import annotations

import pytest
import torch

from flued.v36 import FLUEDV36
import tools.train.v3_6.train_v36_s1 as s1
from tests.test_v37_slm import tiny_config


def _backbone_io(cfg, bsz: int = 2, n: int = 5):
    torch.manual_seed(0)
    model = FLUEDV36(cfg)
    bb = model.backbone
    torch.manual_seed(1)  # 输入张量与构造用 RNG 解耦（两模型间逐位可比）
    k = torch.randn(bsz, n, cfg.d_mem)  # k_row_source=index -> align_k eats d_mem
    v = torch.randn(bsz, n, cfg.d_mem)
    cm = torch.ones(bsz, n, dtype=torch.bool)
    pos = torch.randn(1, n, cfg.d_backbone)
    return model, bb, k, v, cm, pos


# --- 1. 条件创建：state_dict 仅差 α 参数；退火起点 = 门关逐位一致 -------------------


def test_state_dict_differs_only_by_alpha_raw():
    cfg_off = tiny_config()
    cfg_on = tiny_config(e124_budget_gate=True)
    torch.manual_seed(0)
    m_off = FLUEDV36(cfg_off)
    torch.manual_seed(0)
    m_on = FLUEDV36(cfg_on)
    sd_off, sd_on = m_off.state_dict(), m_on.state_dict()
    only_on = set(sd_on) - set(sd_off)
    only_off = set(sd_off) - set(sd_on)
    assert only_on == {"backbone.e124_alpha_raw"} and only_off == set()
    common = set(sd_off) & set(sd_on)
    assert all(torch.equal(sd_off[k], sd_on[k]) for k in common)
    # α 初值: 1 + softplus(softplus^{-1}(α_init-1)) == α_init
    assert float(m_on.backbone.e124_alpha_value().detach()) == pytest.approx(2.0, abs=1e-6)


def test_anneal_start_bitwise_equals_gate_off():
    cfg_off = tiny_config()
    cfg_on = tiny_config(e124_budget_gate=True)
    _m0, bb_off, k, v, cm, pos = _backbone_io(cfg_off)
    _m1, bb_on, k2, v2, cm2, pos2 = _backbone_io(cfg_on)
    assert torch.equal(k, k2) and torch.equal(v, v2)  # 输入流逐位一致（前提非空）
    with torch.no_grad():
        out_off = bb_off(k, v, cm, pos)
        # rt 默认值 progress=0/hard=True → 全量预算 → bypass legacy 路径
        out_on = bb_on(k, v, cm, pos)
    assert torch.equal(out_off, out_on)
    assert bb_on.last_e124_k is not None
    assert float(bb_on.last_e124_k) == float(cm.sum(dim=1).float().mean())


# --- 2. 硬模式：未命中行结构性恰零 + 命中数 = min(k, 候选数) -------------------------


def test_hard_gate_exact_zeros_and_hit_count():
    n = 5
    _m, bb, k, v, cm, pos = _backbone_io(tiny_config(e124_budget_gate=True), n=n)
    bb.e124_rt_budget = 2  # 绝对覆写（RD 仪器口径）; rt_hard 默认 True
    with torch.no_grad():
        bb(k, v, cm, pos, need_attn=True)
    attn = bb.last_block1_attn
    assert attn is not None and attn.shape == (2, bb.nhead, n, n)
    hit = bb.last_e124_hit
    assert hit is not None and hit.shape == (2, bb.nhead, n, n)
    causal = ~torch.triu(torch.ones(n, n, dtype=torch.bool), diagonal=1)
    for i in range(n):  # 逐查询：候选 = 0..i（因果 ∩ 真实）
        h = hit[0, :, i, :]        # (H, n)；per-head top-k —— 预算 head 共享、
        nz = attn[0, :, i, :] > 0  # 命中集随各 head 分值独立（设计语义，勿断言跨头一致）
        assert (h.sum(dim=-1) == min(2, i + 1)).all()  # top-k 构造：命中数恰 = min(k, 候选数)
        assert bool((nz <= h).all())  # 结构性不可见：非命中恰零（条款①否决项）
        assert bool((h <= causal[i].unsqueeze(0)).all())  # 命中集 ⊆ 因果候选集
        # α-entmax 可零化命中集内低分行（设计行为，2026-09-11 冒烟复核换锚）：
        # 非零数 ≤ 命中数，不断言相等（「非零数恰=k」是 softmax 语义错误期望）
        assert bool((nz.sum(dim=-1) <= h.sum(dim=-1)).all())
        assert torch.allclose(attn[0, :, i, :].sum(dim=-1), torch.ones(bb.nhead), atol=1e-6)
    assert float(bb.last_e124_k) == 2.0
    # need_attn=False 时寄存槽保持 None（关态纪律）
    with torch.no_grad():
        bb(k, v, cm, pos)
    assert bb.last_block1_attn is None
    assert bb.last_e124_hit is None


# --- 3. 软模式：梯度通路审计（q_proj / align_k / index_ffn / α） ---------------------


def test_soft_gate_gradient_paths():
    cfg = tiny_config(e124_budget_gate=True, tau_cut=0.0)  # tau_cut=0 → 非退化 chunk 网格
    torch.manual_seed(0)
    model = FLUEDV36(cfg)
    bb = model.backbone
    bb.e124_rt_budget = 2
    bb.e124_rt_hard = False  # 软门（训练姿态）
    bb.e124_rt_temp = 1.0
    g = torch.Generator().manual_seed(1)
    ids = torch.randint(1, 257, (1, 96), generator=g)
    out = s1._slm_forward(model, ids, None)
    assert float(bb.last_e124_k) == 2.0  # 门确实激活（预算 < 真实块数）
    assert bb.last_e124_hit is None  # 软门无离散命中集（审计口纪律）
    loss = out["logits_backbone"].square().mean()
    loss.backward()
    targets = {
        "backbone.q_proj.weight": bb.q_proj.weight,
        "backbone.align_k.weight": bb.align_k.weight,
        "backbone.align_v.weight": bb.align_v.weight,
        "backbone.e124_alpha_raw": bb.e124_alpha_raw,
        "summarizer.index_ffn.0.weight": model.summarizer.index_ffn[0].weight,
    }
    for name, p in targets.items():
        assert p.grad is not None, f"{name}: 无梯度"
        assert bool(torch.isfinite(p.grad).all()), f"{name}: 梯度含非有限值"
        assert float(p.grad.abs().sum()) > 0.0, f"{name}: 梯度全零"


# --- 4. _e124_budget 退火曲线与覆写/钳制 -------------------------------------------


def test_budget_anneal_and_override():
    _m, bb, _k, _v, _cm, _pos = _backbone_io(tiny_config(e124_budget_gate=True))
    cm = torch.ones(2, 11, dtype=torch.bool)  # n_real = 11
    bb.e124_rt_k_final = 9
    bb.e124_rt_progress = 0.0
    assert bb._e124_budget(cm).tolist() == [11, 11]  # 全量 = bypass
    bb.e124_rt_progress = 0.5
    assert bb._e124_budget(cm).tolist() == [10, 10]  # round(11·0.5 + 9·0.5)
    bb.e124_rt_progress = 1.0
    assert bb._e124_budget(cm).tolist() == [9, 9]  # 终点 k_final
    bb.e124_rt_budget = 3
    assert bb._e124_budget(cm).tolist() == [3, 3]  # 绝对覆写优先
    bb.e124_rt_budget = 100
    assert bb._e124_budget(cm).tolist() == [11, 11]  # 上限钳到 n_real
    bb.e124_rt_budget = 0
    assert bb._e124_budget(cm).tolist() == [1, 1]  # 下限钳到 1


# --- 5. 非 a 格响亮报错 --------------------------------------------------------------


def test_non_a_grid_loud():
    with pytest.raises(ValueError, match="e124_budget_gate"):
        FLUEDV36(tiny_config(e124_budget_gate=True, v_row_source="state"))
    with pytest.raises(ValueError, match="e124_budget_gate"):
        FLUEDV36(tiny_config(e124_budget_gate=True, k_row_source="state"))
    with pytest.raises(ValueError, match="e124_alpha_init"):
        FLUEDV36(tiny_config(e124_budget_gate=True, e124_alpha_init=1.0))


# --- 6. 基座审计（⑤ loud-fail）：冻结差集精确相等 + 白名单 + 漂移响亮 ------------------


def test_e124_audit_frozen_sets_and_whitelist(tmp_path, monkeypatch):
    from types import SimpleNamespace

    import tools.train.v3_6.train_v36_s1 as s1

    model = FLUEDV36(tiny_config(e124_budget_gate=True))
    cur = model.state_dict()
    victim_absent = "decoder_in_mem.weight"   # 现行有、基座缺席
    victim_shape = "chunk_pos.weight"         # 形不符
    victim_extra = "ghost.extra"              # 基座冗键
    payload = {k: v for k, v in cur.items()
               if k not in ("backbone.e124_alpha_raw", victim_absent)}
    payload[victim_shape] = torch.zeros(3)    # 同键异形
    payload[victim_extra] = torch.zeros(1)
    base = tmp_path / "base.pt"
    torch.save({"model": payload}, base)
    args = SimpleNamespace(init_checkpoint=str(base))
    monkeypatch.setattr(s1, "_E124_EXPECT_ABSENT", frozenset({victim_absent}))
    monkeypatch.setattr(s1, "_E124_EXPECT_SHAPE_BAD", frozenset({victim_shape}))
    monkeypatch.setattr(s1, "_E124_EXPECT_EXTRA", frozenset({victim_extra}))
    # 差集恰 = 冻结期望（白名单 alpha_raw 缺席基座不计）→ 通过
    s1._e124_audit_init_checkpoint(model, args)
    # 漂移（冗键集不符）→ 响亮
    monkeypatch.setattr(s1, "_E124_EXPECT_EXTRA", frozenset({"ghost.other"}))
    with pytest.raises(SystemExit):
        s1._e124_audit_init_checkpoint(model, args)
