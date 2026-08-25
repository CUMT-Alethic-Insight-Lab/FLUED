"""v3.7 Q17 oracle 状态读出训练臂 (任务书 2026-08-25 冻结;
spec: docs/versions/v3_7/FLUED_V3_7_Q17_ORACLE_READOUT_20260825_CN.md).
实现: tools/train/v3_6/train_q17_oracle_readout.py.

Covers: (1) oracle 构造数值断言 (玩具 gates 手算 cumsum k vᵀ; 自然态手算
KDA 递推; padded chunk 恒等); (2) α 缩放公式 (median 范数比, 只统计有效
chunk); (3) 退火档位表边界 + 抽签流确定性; (4) 读出数学镜像 (readout_query
梯度通, realign 冻); (5) 重初始化范围 (冻结参数与基座逐位相同 / 链参数
不同 / realign 保持基座值); (6) 基座+筛子双加载 (同权重全冻); (7) 收官
run dir schema 能被 probe_burst_route_q15 的 load_model 加载.
"""

from __future__ import annotations

import json

import pytest
import torch

from flued.v36 import FLUEDV36
from tests.test_v37_slm import tiny_config
from tools.train.v3_6 import train_q17_oracle_readout as q17
from tools.train.v3_6.train_v36 import build_model, build_parser


def _toy_gates(bsz=1, chunks=3, heads=1, hk=2, hv=2, pad_last=False):
    torch.manual_seed(0)
    gates = {
        "k": torch.randn(bsz, chunks, heads, hk),
        "v": torch.randn(bsz, chunks, heads, hv),
        "beta": torch.rand(bsz, chunks, heads),
        "alpha": torch.rand(1, heads, hk) * 0.4 + 0.6,
    }
    cm = torch.ones(bsz, chunks, dtype=torch.bool)
    if pad_last:
        cm[:, -1] = False
    return gates, cm


# --- 1. oracle/自然态构造数值断言 ---------------------------------------------------


def test_states_dual_oracle_is_cumsum():
    gates, cm = _toy_gates()
    S_nat, S_or = q17._q17_states_dual(gates, cm)
    assert S_nat.shape == S_or.shape == (1, 3, 1, 2, 2)
    # oracle = Σ_{j≤i} k_j v_jᵀ 手算
    for i in range(3):
        expect = sum(
            gates["k"][0, j, 0].unsqueeze(-1) * gates["v"][0, j, 0].unsqueeze(-2)
            for j in range(i + 1)
        )
        assert torch.allclose(S_or[0, i, 0], expect, atol=1e-6)


def test_states_dual_natural_matches_recurrence():
    gates, cm = _toy_gates()
    S_nat, _ = q17._q17_states_dual(gates, cm)
    # 手算 KDA 递推 (衰减 + delta 擦除), 与 probe trained_states 同款;
    # alpha[0, h] 是 (hk,) 逐 k 通道衰减 -> (hk, 1) 作用在 (hk, hv) 态上
    a = gates["alpha"][0].float()  # (H, hk)
    S = torch.zeros(2, 2)
    for i in range(3):
        ki = gates["k"][0, i, 0].float()
        vi = gates["v"][0, i, 0].float()
        bi = gates["beta"][0, i, 0].float()
        S = a[0].unsqueeze(-1) * S
        S = S - bi * ki.unsqueeze(-1) * (ki @ S).unsqueeze(-2)
        S = S + bi * ki.unsqueeze(-1) * vi.unsqueeze(-2)
        assert torch.allclose(S_nat[0, i, 0], S, atol=1e-6), i


def test_states_dual_padded_chunk_is_identity():
    gates, cm = _toy_gates(pad_last=True)
    S_nat, S_or = q17._q17_states_dual(gates, cm)
    # padded chunk 2: 自然态恒等步, oracle 不入累计 -> 两族都等于 chunk 1 的态
    assert torch.allclose(S_nat[0, 2], S_nat[0, 1], atol=1e-6)
    assert torch.allclose(S_or[0, 2], S_or[0, 1], atol=1e-6)


# --- 2. α 缩放公式 (任务书 §1 条件 2) -------------------------------------------------


def test_alpha_scale_median_ratio():
    # 3 chunk 全有效, 手造范数: nat [2,2,2] (median 2), or [100,200,300]
    # (median 200) -> α = 0.01
    S_nat = torch.zeros(1, 3, 1, 2, 2)
    S_or = torch.zeros(1, 3, 1, 2, 2)
    for i, (nn, no) in enumerate([(2.0, 100.0), (2.0, 200.0), (2.0, 300.0)]):
        S_nat[0, i, 0, 0, 0] = nn
        S_or[0, i, 0, 0, 0] = no
    cm = torch.ones(1, 3, dtype=torch.bool)
    S_or_s, alpha = q17._q17_alpha_scale(S_nat, S_or, cm)
    assert float(alpha[0]) == pytest.approx(0.01)
    assert torch.allclose(S_or_s, S_or * 0.01)
    # padded chunk 不进 median: 把 chunk 2 打 pad 且给极端范数; 有效集
    # {100, 200} 两个, torch.median 偶数档取低中位 = 100 -> α = 2/100 = 0.02
    cm2 = cm.clone()
    cm2[0, 2] = False
    S_or2 = S_or.clone()
    S_or2[0, 2, 0, 0, 0] = 1e9
    _, alpha2 = q17._q17_alpha_scale(S_nat, S_or2, cm2)
    assert float(alpha2[0]) == pytest.approx(0.02)


# --- 3. 退火档位表 + 抽签流确定性 --------------------------------------------------------


def test_anneal_p_tiers():
    assert q17._q17_anneal_p(0) == 1.0
    assert q17._q17_anneal_p(1999) == 1.0
    assert q17._q17_anneal_p(2000) == 0.75
    assert q17._q17_anneal_p(3999) == 0.75
    assert q17._q17_anneal_p(4000) == 0.5
    assert q17._q17_anneal_p(7999) == 0.25
    assert q17._q17_anneal_p(8000) == 0.0
    assert q17._q17_anneal_p(9999) == 0.0
    assert q17._q17_anneal_p(10**6) == 0.0  # 超界钳末档


def test_anneal_draw_stream_deterministic():
    def draws(seed, p):
        g = torch.Generator().manual_seed(seed)
        return [float(torch.rand((), generator=g)) < p for _ in range(8)]

    a = draws(42, 0.75)
    assert a == draws(42, 0.75)  # 同种子同 p 逐比特
    assert a != draws(42, 0.25) or a != draws(43, 0.75)  # 非退化


# --- 4/5/6. 读出链范围与加载 (tiny d 格) -----------------------------------------------


def _tiny_d_run_dir(tmp_path):
    """合成 tiny d 格 run dir (resolved_config + latest.pt)."""
    import tools.train.v3_6.train_v36_s1 as s1

    parser = build_parser()
    s1._add_s1_args(parser)  # resolved_config 需含 S1 层键 (bpe_tokenizer_path 等)
    args = parser.parse_args([])
    for k, v in dict(
        d_byte=64, encoder_layers=2, segmentor_layers=2, nhead=4, ffn_dim=128,
        d_mem=96, summarizer_slots=2, summarizer_hidden=128, kda_heads=2,
        kda_head_k=16, kda_head_v=32, write_hidden=128, readout_queries=1,
        d_pack=64, d_backbone=64, backbone_layers=3, backbone_nhead=4,
        backbone_ffn=128, decoder_hidden=128, decoder_layers=2, max_chunks=8,
        max_span=16, bytes_per_chunk=8, max_positions=8, per_chunk_readout=True,
        summarizer_type="dit", backbone_mode="slm", k_row_source="state",
        v_row_source="state", seed_source="k", kda_impl="torch",
        mask_mode="byte_span",  # 测试 run dir 不依赖 128k tokenizer
        data_path="corpus.txt",
    ).items():
        setattr(args, k, v)
    torch.manual_seed(0)
    model = build_model(args)
    d = tmp_path / "q15b_fake"
    d.mkdir()
    (d / "resolved_config.json").write_text(
        json.dumps(vars(args), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    torch.save({"step": 20000, "model": model.state_dict(), "args": vars(args)}, d / "latest.pt")
    return d, args


def test_load_models_base_and_sieve_frozen_identical(tmp_path):
    run_dir, _ = _tiny_d_run_dir(tmp_path)
    model, sieve, ns, step = q17._q17_load_models(run_dir, torch.device("cpu"))
    assert step == 20000
    assert ns.backbone_mode == "slm" and ns.k_row_source == "state" and ns.v_row_source == "state"
    # 双对象同权重 (基座 ckpt 第二次独立加载), 全部冻结
    for p1, p2 in zip(model.parameters(), sieve.parameters()):
        assert torch.equal(p1, p2)
        assert not p1.requires_grad and not p2.requires_grad


def test_reinit_chain_scope(tmp_path):
    run_dir, args = _tiny_d_run_dir(tmp_path)
    model, _sieve, ns, _ = q17._q17_load_models(run_dir, torch.device("cpu"))
    before = {k: v.clone() for k, v in model.state_dict().items()}
    q17._q17_reinit_readout_chain(model, ns, seed=42)
    after = model.state_dict()
    # 链参数抽查 (合成基座未训练: LayerNorm/零初始化偏置新旧同值是初始化
    # 语义而非 bug, 不在断言集 -- 抽数据依赖的大权重键)
    must_change = [
        "backbone.q_proj.weight", "backbone.self_blocks.0.q.weight",
        "decoder.blocks.0.attn.qkv.weight",
        "state_machine.readout_query", "state_machine_k.readout_query",
        # 修订 v1: realign×2 读出投影本体在链上, 同一足迹从零 (realign.0 是
        # LayerNorm 恒定初始化新旧同值, 抽 Linear 层 realign.3)
        "state_machine.realign.3.weight", "state_machine_k.realign.3.weight",
        # 注: 本 fixture d_pack==d_backbone -> decoder_in 是 Identity 无参
        # (model.py:2085), 不在抽查集; 真配置 1536!=384 有真 Linear.
    ]
    for k in must_change:
        assert not torch.equal(before[k], after[k]), k  # 链参数已重初始化
    # tied-embedding 护栏: decoder.byte_lookup 与模型级 byte_lookup 同一参数
    # (model.py:2086), 任务书冻结面覆盖 -- 必须逐位不动
    assert torch.equal(before["byte_lookup.embedding.weight"], after["byte_lookup.embedding.weight"])
    assert torch.equal(
        before["decoder.byte_lookup.embedding.weight"], after["decoder.byte_lookup.embedding.weight"]
    )
    for k in before:
        if k.startswith(("backbone.", "decoder.", "decoder_in.", "decoder_in_mem.",
                         "state_machine.readout_query", "state_machine_k.readout_query",
                         "state_machine.realign.", "state_machine_k.realign.")):  # 修订 v1
            continue  # 链上 (LN/零偏置新旧同值不断言)
        assert torch.equal(before[k], after[k]), k  # 其余 (含前端/写头) 逐位不动
    # 重初始化可复现: 同种子再建同值
    model2, _s, _n, _ = q17._q17_load_models(run_dir, torch.device("cpu"))
    q17._q17_reinit_readout_chain(model2, ns, seed=42)
    assert torch.equal(model.state_dict()["backbone.q_proj.weight"], model2.state_dict()["backbone.q_proj.weight"])


def test_readout_math_mirrors_state_machine():
    """读出数学镜像: 手造 S 与 query, _q17_readout == einsum+realign 手算;
    readout_query 与 realign 梯度通 (修订 v1 链范围), S 不进图 (状态不经梯度)."""
    torch.manual_seed(0)
    cfg = tiny_config(k_row_source="state", v_row_source="state", seed_source="k")
    model = FLUEDV36(cfg)
    sm = model.state_machine
    S = torch.randn(1, 3, cfg.kda_heads, cfg.kda_head_k, cfg.kda_head_v)
    package = q17._q17_readout(sm, S)
    q = sm.readout_query.float()
    read = torch.einsum("qhk,bchkv->bcqhv", q, S).reshape(1, 3, q.size(0), -1)
    expect = sm.realign(read.to(next(sm.realign.parameters()).dtype))
    assert torch.allclose(package, expect, atol=1e-6)
    assert package.shape == (1, 3, cfg.readout_queries, cfg.d_pack)
    package.mean(dim=2).sum().backward()
    assert sm.readout_query.grad is not None
    assert sm.readout_query.grad.abs().sum() > 0
    assert all(p.grad is not None for p in sm.realign.parameters())  # 修订 v1


def test_realign_reinit_and_training_update(tmp_path):
    """修订 v1: realign×2 重初始化后与基座不同; 训练一步后参数确实更新;
    冻结面 (write_head/summarizer) 一步后仍无梯度."""
    run_dir, _args = _tiny_d_run_dir(tmp_path)
    model, _s, ns, _ = q17._q17_load_models(run_dir, torch.device("cpu"))
    base = {k: v.clone() for k, v in model.state_machine.realign.state_dict().items()}
    base_k = {k: v.clone() for k, v in model.state_machine_k.realign.state_dict().items()}
    q17._q17_reinit_readout_chain(model, ns, seed=42)
    after_reinit = model.state_machine.realign.state_dict()
    assert any(not torch.equal(base[k], after_reinit[k]) for k in base)  # 重初始化后与基座不同
    assert any(not torch.equal(base_k[k], model.state_machine_k.realign.state_dict()[k]) for k in base_k)
    trainable = q17._q17_unfreeze_chain(model)
    assert any(p is q for p in trainable for q in model.state_machine.realign.parameters())
    before_step = {k: v.clone() for k, v in model.state_machine.realign.state_dict().items()}
    cfg = ns  # tiny d 格 (max_chunks=8 网格)
    S = torch.randn(1, 3, ns.kda_heads, ns.kda_head_k, ns.kda_head_v)
    loss = q17._q17_readout(model.state_machine, S).mean()
    opt = torch.optim.SGD(trainable, lr=1e-1)
    opt.zero_grad()
    loss.backward()
    opt.step()  # 训练一步
    after_step = model.state_machine.realign.state_dict()
    assert any(not torch.equal(before_step[k], after_step[k]) for k in before_step)  # 参数确实更新
    assert all(p.grad is None for p in model.write_head.parameters())  # 冻结面无梯度
    assert all(p.grad is None for p in model.summarizer.parameters())


# --- 7. 收官 schema 兼容 (probe_burst_route_q15 的 load_model) -------------------------


def test_run_dir_schema_loadable_by_probe_loader(tmp_path):
    """收官 run dir (resolved_config 照抄基座 + latest.pt 全模型 state_dict)
    必须能被 probe_burst_route_q15 的 load_model 加载 (条件 3 收官兼容)."""
    from tools.analysis.v3_6.probe_oracle_write_verdict import load_model

    run_dir, _args = _tiny_d_run_dir(tmp_path)
    # 模拟 Q17 收官: 照抄 resolved_config + 全模型 state_dict 存 latest.pt
    out = tmp_path / "q17_out"
    out.mkdir()
    (out / "resolved_config.json").write_text(
        (run_dir / "resolved_config.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    model, _s, _n, _ = q17._q17_load_models(run_dir, torch.device("cpu"))
    torch.save({"step": 10000, "model": model.state_dict(), "args": {}}, out / "latest.pt")
    loaded, ns, step = load_model(out, torch.device("cpu"))
    assert step == 10000 and ns.backbone_mode == "slm"
    for p1, p2 in zip(loaded.parameters(), model.parameters()):
        assert torch.equal(p1, p2)  # strict 加载逐位一致
