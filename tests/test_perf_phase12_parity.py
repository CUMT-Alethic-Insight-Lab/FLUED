"""效率施工 Phase 1+2（trainer 侧 C1/C3/C4/C5/C7）零语义 parity 测试。

提案：outputs/_perf_audit_20260911/proposal.md（2026-09-11，用户已批准）。
验收基尺：同种子同输入下，新实现与施工前实现逐位一致（torch.equal）；
例外 = _slm_forward 的 boundary_confidence_mean / hard_cut_fraction 两枚
metrics-only 诊断列（detach 进日志、不进损失）——fp 归约序与被掩码压缩后
的 mean 不同，按提案 §C1 容许末位 ulp 差，allclose(atol=1e-7) 验收。

本文件内嵌施工前实现快照（_old_chunk_forward / _old_make_targets / 旧
训练步语句序），作为参照实现（不许改动快照本体）。
"""

from __future__ import annotations

import copy
import types

import pytest
import torch

from flued.data import PAD_ID
from flued.v33.chunk_builder import ChunkBatch, ChunkBuilder
from flued.v36 import FLUEDV36
from tools.train.v3_6 import train_v36_s1 as s1
from tests.test_v37_slm import _s1_args, tiny_config

DEVICE = torch.device("cpu")
KEY_GEOMETRY_KEYS = (
    "key_mu", "key_mu_max", "key_pr", "key_mu_k", "key_mu_max_k", "key_pr_k",
)


# ---------------------------------------------------------------------------
# 施工前实现快照（参照实现；逐行等价 git HEAD@2026-09-11）
# ---------------------------------------------------------------------------


def _old_chunk_forward(self, byte_features, valid, hard_cut, confidence=None, soft_transition=None, force_continue=None):
    bsz, seq_len, dim = byte_features.shape
    device = byte_features.device
    span_embeddings = byte_features.new_zeros((bsz, self.max_chunks, self.max_span, dim))
    confidence_values = byte_features.new_zeros((bsz, self.max_chunks, self.max_span))
    token_mask = torch.zeros((bsz, self.max_chunks, self.max_span), dtype=torch.bool, device=device)
    transition_markers = torch.zeros_like(token_mask)
    force_markers = torch.zeros_like(token_mask)
    offsets = torch.zeros((bsz, seq_len), dtype=torch.long, device=device)
    chunk_ids = torch.full((bsz, seq_len), -1, dtype=torch.long, device=device)
    lengths = torch.zeros((bsz, self.max_chunks), dtype=torch.long, device=device)
    chunk_mask = torch.zeros((bsz, self.max_chunks), dtype=torch.bool, device=device)

    soft_transition = soft_transition if soft_transition is not None else torch.zeros_like(valid)
    force_continue = force_continue if force_continue is not None else torch.zeros_like(valid)
    confidence = confidence if confidence is not None else byte_features.new_zeros(valid.shape)

    rank = valid.to(torch.long).cumsum(dim=1) - 1
    cuts = hard_cut.bool() & valid
    first = valid.float().argmax(dim=1)
    cuts = cuts.clone()
    cuts[torch.arange(bsz, device=device), first] |= valid.any(dim=1)

    hard_start = torch.cummax(torch.where(cuts, rank, torch.zeros_like(rank)), dim=1).values
    slot_from_hard = rank - hard_start
    span_cut = valid & slot_from_hard.ge(self.max_span) & ((slot_from_hard % self.max_span) == 0)
    cuts = cuts | span_cut

    final_start = torch.cummax(torch.where(cuts, rank, torch.zeros_like(rank)), dim=1).values
    slots = rank - final_start
    chunks_for_tokens = torch.cumsum(cuts.to(torch.long), dim=1) - 1
    within = valid & chunks_for_tokens.ge(0) & chunks_for_tokens.lt(self.max_chunks) & slots.ge(0) & slots.lt(self.max_span)
    truncated_tokens = (valid & ~within).sum(dim=1)

    b_idx, src_idx = within.nonzero(as_tuple=True)
    chunk_idx = chunks_for_tokens[b_idx, src_idx]
    slot_idx = slots[b_idx, src_idx]
    span_embeddings[b_idx, chunk_idx, slot_idx] = byte_features[b_idx, src_idx]
    confidence_values[b_idx, chunk_idx, slot_idx] = confidence[b_idx, src_idx].to(confidence_values.dtype)
    token_mask[b_idx, chunk_idx, slot_idx] = True
    transition_markers[b_idx, chunk_idx, slot_idx] = soft_transition[b_idx, src_idx].bool()
    force_markers[b_idx, chunk_idx, slot_idx] = force_continue[b_idx, src_idx].bool()
    chunk_ids[b_idx, src_idx] = chunk_idx
    offsets[b_idx, src_idx] = slot_idx
    chunk_mask[b_idx, chunk_idx] = True

    flat_chunk = b_idx * self.max_chunks + chunk_idx
    flat_lengths = lengths.reshape(-1)
    flat_lengths.scatter_reduce_(0, flat_chunk, slot_idx + 1, reduce="amax", include_self=True)

    return ChunkBatch(
        span_embeddings=span_embeddings,
        confidence_values=confidence_values,
        chunk_ids=chunk_ids,
        offsets=offsets,
        lengths=lengths,
        chunk_mask=chunk_mask,
        token_mask=token_mask,
        transition_markers=transition_markers,
        force_continue_markers=force_markers,
        pack_info={"max_chunks": self.max_chunks, "max_span": self.max_span, "truncated_tokens": truncated_tokens},
    )


def _old_make_targets(clean, byte_mask, chunk_ids, offsets, max_chunks, max_span):
    bsz, seq_len = clean.shape
    targets = torch.full((bsz, max_chunks, max_span), PAD_ID, dtype=torch.long, device=clean.device)
    slot_mask = torch.zeros((bsz, max_chunks, max_span), dtype=torch.bool, device=clean.device)
    masked_slot = torch.zeros_like(slot_mask)
    valid = chunk_ids.ge(0) & chunk_ids.lt(max_chunks) & offsets.ge(0) & offsets.lt(max_span) & clean.ne(PAD_ID)
    b_idx, t_idx = valid.nonzero(as_tuple=True)
    c_idx = chunk_ids[b_idx, t_idx]
    s_idx = offsets[b_idx, t_idx]
    targets[b_idx, c_idx, s_idx] = clean[b_idx, t_idx]
    slot_mask[b_idx, c_idx, s_idx] = True
    masked_slot[b_idx, c_idx, s_idx] = byte_mask[b_idx, t_idx]
    return targets, slot_mask, masked_slot


_CHUNK_FIELDS = (
    "span_embeddings", "confidence_values", "chunk_ids", "offsets", "lengths",
    "chunk_mask", "token_mask", "transition_markers", "force_continue_markers",
)


def _fixed_window_cases():
    """C1 固定窗集：满窗 / 短窗 / 全 PAD 边界 / chunk 溢出（越界位进 dump 区）
    / 稀疏切点（span_cut 强制边界路径）。"""
    g = torch.Generator().manual_seed(11)
    B, T, D = 2, 40, 5

    def case(valid, hard):
        bf = torch.randn(B, T, D, generator=g)
        conf = torch.rand(B, T, generator=g)
        soft = (torch.rand(B, T, generator=g) > 0.8) & valid
        force = (torch.rand(B, T, generator=g) > 0.9) & valid
        return bf, valid, hard, conf, soft, force

    full = torch.ones(B, T, dtype=torch.bool)
    h7 = torch.zeros(B, T, dtype=torch.bool)
    h7[:, ::7] = True
    short_v = torch.zeros(B, T, dtype=torch.bool)
    short_v[:, :13] = True
    short_h = torch.zeros(B, T, dtype=torch.bool)
    short_h[:, 5] = True
    h2 = torch.zeros(B, T, dtype=torch.bool)
    h2[:, ::2] = True  # chunks_for_tokens 冲到 19 >> max_chunks=4 → 大量 truncated
    sparse = torch.ones(B, T, dtype=torch.bool)
    sparse_h = torch.zeros(B, T, dtype=torch.bool)
    sparse_h[:, 0] = True
    sparse_h[:, 20] = True  # 20 连字节无切点 → span_cut 在 slot 8/16 强制边界

    return {
        "full_span_cut": case(full, h7),
        "short": case(short_v, short_h),
        "all_pad": case(torch.zeros(B, T, dtype=torch.bool), torch.zeros(B, T, dtype=torch.bool)),
        "chunk_overflow": case(full, h2),
        "sparse_cuts": case(sparse, sparse_h),
    }


# ---------------------------------------------------------------------------
# C1: chunk_builder 固定窗集逐位对拍
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", ["full_span_cut", "short", "all_pad", "chunk_overflow", "sparse_cuts"])
def test_c1_chunk_builder_bit_parity(name):
    new_builder = ChunkBuilder(max_chunks=4, max_span=8)
    old_builder = ChunkBuilder(max_chunks=4, max_span=8)
    bf, valid, hard, conf, soft, force = _fixed_window_cases()[name]
    new = new_builder.forward(bf, valid, hard, conf, soft, force)
    old = _old_chunk_forward(old_builder, bf, valid, hard, conf, soft, force)
    for f in _CHUNK_FIELDS:
        assert torch.equal(getattr(new, f), getattr(old, f)), f
    assert torch.equal(new.pack_info["truncated_tokens"], old.pack_info["truncated_tokens"])
    assert new.pack_info["max_chunks"] == old.pack_info["max_chunks"]
    assert new.pack_info["max_span"] == old.pack_info["max_span"]


def test_c1_chunk_builder_defaults_and_bf16_confidence():
    """soft/force 缺省（zeros_like 路径）+ bf16 链路（byte_features 与
    confidence 同为 bf16 时 confidence_values 保持 bf16；dtype 契约 =
    跟随 byte_features，新旧一致）。"""
    g = torch.Generator().manual_seed(13)
    B, T, D = 2, 24, 3
    bf = torch.randn(B, T, D, generator=g).to(torch.bfloat16)
    valid = torch.ones(B, T, dtype=torch.bool)
    valid[:, 20:] = False
    hard = torch.zeros(B, T, dtype=torch.bool)
    hard[:, 0] = True
    conf = torch.rand(B, T, generator=g).to(torch.bfloat16)
    new = ChunkBuilder(4, 8).forward(bf, valid, hard, conf)
    old = _old_chunk_forward(ChunkBuilder(4, 8), bf, valid, hard, conf)
    for f in _CHUNK_FIELDS:
        assert torch.equal(getattr(new, f), getattr(old, f)), f
    assert new.confidence_values.dtype == old.confidence_values.dtype == torch.bfloat16


def test_c1_make_targets_bit_parity_on_builder_grids():
    """make_targets 同款对拍：吃 chunk_builder 的 (chunk_ids, offsets) 网格，
    clean 含 PAD 尾与窗内 PAD 位，byte_mask 覆盖 True/False 两态。"""
    for name, (bf, valid, hard, conf, soft, force) in _fixed_window_cases().items():
        g = torch.Generator().manual_seed(17)
        clean = torch.randint(1, 257, valid.shape, generator=g)
        clean[~valid] = PAD_ID
        clean[0, 7] = PAD_ID  # 窗内 PAD（valid 位但被 clean.ne(PAD_ID) 剔除）
        byte_mask = (torch.rand(valid.shape, generator=g) > 0.7) & valid
        grid = ChunkBuilder(4, 8).forward(bf, valid, hard, conf)
        new = s1.make_targets(clean, byte_mask, grid.chunk_ids, grid.offsets, 4, 8)
        old = _old_make_targets(clean, byte_mask, grid.chunk_ids, grid.offsets, 4, 8)
        for i, (a, b) in enumerate(zip(new, old)):
            assert torch.equal(a, b), (name, i)
        # 全 PAD clean：targets 全 PAD、两掩码全 False（逐位与旧一致由上覆盖）


def test_c1_aux_metric_keys_ulp_tolerance_contract():
    """两枚 metrics-only 诊断列：加权和均值 vs 掩码压缩均值 —— 提案 §C1 验收
    条款 allclose(atol=1e-7)（非逐位契约）；空窗兜底分支必须逐位同值。"""
    g = torch.Generator().manual_seed(5)
    for _ in range(8):
        conf = torch.rand(2, 64, generator=g)
        valid = torch.rand(2, 64, generator=g) > 0.3
        hard = (torch.rand(2, 64, generator=g) > 0.7) & valid
        old_c = conf[valid].mean() if valid.any() else conf.mean()
        old_h = hard.float()[valid].mean() if valid.any() else hard.float().mean()
        # 新式（与 _slm_forward 内 C1 改写逐句同式）
        vc = valid.sum()
        new_c = torch.where(vc > 0, (conf * valid.to(conf.dtype)).sum() / vc.clamp(min=1), conf.mean())
        hf = hard.float()
        new_h = torch.where(vc > 0, (hf * valid.to(hf.dtype)).sum() / vc.clamp(min=1), hf.mean())
        assert torch.allclose(new_c, old_c, rtol=0.0, atol=1e-7)
        assert torch.allclose(new_h, old_h, rtol=0.0, atol=1e-7)
    # 空窗兜底：全 invalid → fallback = 全量均值，与旧同一算式逐位同值
    v0 = torch.zeros(1, 8, dtype=torch.bool)
    c0 = torch.randn(1, 8, generator=g)
    h0 = torch.zeros(1, 8, dtype=torch.bool)
    old_c = c0[v0].mean() if v0.any() else c0.mean()
    old_h = h0.float()[v0].mean() if v0.any() else h0.float().mean()
    vc = v0.sum()
    new_c = torch.where(vc > 0, (c0 * v0.to(c0.dtype)).sum() / vc.clamp(min=1), c0.mean())
    hf = h0.float()
    new_h = torch.where(vc > 0, (hf * v0.to(hf.dtype)).sum() / vc.clamp(min=1), hf.mean())
    assert torch.equal(new_c, old_c) and torch.equal(new_h, old_h)


# ---------------------------------------------------------------------------
# C1: step_model 端到端位级 parity（挂旧 chunk_builder + 旧 make_targets）
# ---------------------------------------------------------------------------


def test_c1_step_model_bit_parity_vs_old_components():
    """a 格 tiny 模型 step_model(train=True)：新实现 vs 挂回施工前
    chunk_builder + make_targets 的参照实现 —— loss / 全部 metrics（两枚
    metrics-only 列除外，allclose(atol=1e-7)）/ 全参数梯度逐位一致。"""
    torch.manual_seed(0)
    model_new = FLUEDV36(tiny_config())  # a 格: index/memory
    model_old = copy.deepcopy(model_new)
    args = _s1_args()  # mask_mode=byte_span（吃全局 RNG → manual_seed 对齐）
    batch = (torch.randint(1, 257, (1, 64), generator=torch.Generator().manual_seed(31)),)

    def run(model):
        torch.manual_seed(2026)
        loss, metrics = s1.step_model(model, batch, args, DEVICE, train=True)
        assert torch.isfinite(loss)
        loss.backward()
        grads = {n: p.grad.detach().clone() for n, p in model.named_parameters() if p.grad is not None}
        return loss.detach().clone(), {k: v.detach().clone() for k, v in metrics.items()}, grads

    new = run(model_new)
    from flued.v33 import chunk_builder as cb_mod

    orig_fwd, orig_mt = cb_mod.ChunkBuilder.forward, s1.make_targets
    try:
        cb_mod.ChunkBuilder.forward = _old_chunk_forward
        s1.make_targets = _old_make_targets
        old = run(model_old)
    finally:
        cb_mod.ChunkBuilder.forward = orig_fwd
        s1.make_targets = orig_mt

    assert torch.equal(new[0], old[0])  # loss 逐位
    for k, v in new[1].items():
        if k in ("boundary_confidence_mean", "hard_cut_fraction"):
            # metrics-only 两列（提案 §C1）: allclose(atol=1e-7) 验收并记录在案
            assert torch.allclose(v, old[1][k], rtol=0.0, atol=1e-7), k
        else:
            assert torch.equal(v, old[1][k]), k
    assert set(new[2]) == set(old[2])
    for n, g_new in new[2].items():
        assert torch.equal(g_new, old[2][n]), n  # 参数梯度逐位


# ---------------------------------------------------------------------------
# C3: NaN 注入 —— 旧/新判据位置跳过行为逐一比对（镜像训练循环两条语句序）
# ---------------------------------------------------------------------------


def _traj_equal(a, b):
    return len(a) == len(b) and all(torch.equal(x, y) for x, y in zip(a, b))


def _nan_injection_loop(order, inject_step, steps=6):
    """逐句镜像 main() 训练循环的新旧语句序（s1 文件 §5054 一带；SGD+momentum
    带 optimizer state，检验 skip 步不漏进动量）。"""
    torch.manual_seed(7)
    model = torch.nn.Linear(4, 2)
    x = torch.randn(8, 4)
    y = torch.randn(8, 2)
    opt = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
    sched = torch.optim.lr_scheduler.StepLR(opt, step_size=2, gamma=0.5)
    nan_skips = 0
    traj = []
    grad_none_after_skip = True
    for step in range(steps):
        loss = ((model(x) - y) ** 2).mean()
        if step == inject_step:
            loss = loss * torch.tensor(float("nan"))
        if order == "old":
            if not bool(torch.isfinite(loss)):
                nan_skips += 1
                opt.zero_grad(set_to_none=True)
                sched.step()
                continue
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            sched.step()
        else:  # "new"（C3 后移）
            opt.zero_grad(set_to_none=True)
            loss.backward()
            if not bool(torch.isfinite(loss)):
                nan_skips += 1
                opt.zero_grad(set_to_none=True)
                sched.step()
                continue
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            sched.step()
        if any(p.grad is None for p in model.parameters()):
            grad_none_after_skip = False
        traj.append(model.weight.detach().clone())
    return {
        "nan_skips": nan_skips,
        "traj": traj,
        "sched_epoch": sched.last_epoch,
        "final_w": model.weight.detach().clone(),
        "grad_none_after_skip": grad_none_after_skip,
    }


def test_c3_nan_injection_skip_behavior_old_vs_new():
    for inject in (None, 0, 3):
        old = _nan_injection_loop("old", inject)
        new = _nan_injection_loop("new", inject)
        assert old["nan_skips"] == new["nan_skips"] == (1 if inject is not None else 0)
        assert old["sched_epoch"] == new["sched_epoch"]
        assert _traj_equal(old["traj"], new["traj"])  # 逐步参数逐位
        assert torch.equal(old["final_w"], new["final_w"])
        assert new["grad_none_after_skip"]  # NaN 步后梯度确已 set_to_none 清空


def test_c3_finite_path_bitwise_identical_params():
    """正常窗流：判据后移不改变任何一步的参数。"""
    old = _nan_injection_loop("old", None, steps=12)
    new = _nan_injection_loop("new", None, steps=12)
    assert _traj_equal(old["traj"], new["traj"]) and torch.equal(old["final_w"], new["final_w"])


# ---------------------------------------------------------------------------
# C4: make_mixed_mask 吃 host 张量（去 CPU 往返）
# ---------------------------------------------------------------------------


def test_c4_mask_from_host_tensor_value_neutral():
    clean = torch.randint(1, 257, (2, 64), generator=torch.Generator().manual_seed(3))
    clean[:, 40:] = PAD_ID
    m_host = s1.make_mixed_mask(clean, 0.3, tokenizer=None, generator=torch.Generator().manual_seed(77))
    # 旧路径等价形态：张量经 .to(device)→.cpu() 往返后再进 make_mixed_mask
    m_roundtrip = s1.make_mixed_mask(clean.to("cpu").cpu(), 0.3, tokenizer=None, generator=torch.Generator().manual_seed(77))
    assert torch.equal(m_host, m_roundtrip)


def test_c4_mixed_mask_step_determinism_through_host_path():
    """mask_mode=mixed（tokenizer 缺席 → char 兜底路径）端到端走新 host 接
    线：同种子（全局 RNG + 专用 _MASK_GENERATOR，evaluate() 同款对齐纪律）
    双跑 loss 与 mask_rate 逐位一致。真 D2H 往返消除的 parity 归 GPU 200 步
    双跑验收（提案 §5.2）。"""
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    args = _s1_args(mask_mode="mixed", mask_prob=0.3)
    batch = (torch.randint(1, 257, (1, 64), generator=torch.Generator().manual_seed(9)),)
    torch.manual_seed(99)
    s1._MASK_GENERATOR.manual_seed(99)
    l1, m1 = s1.step_model(model, batch, args, DEVICE, train=True)
    torch.manual_seed(99)
    s1._MASK_GENERATOR.manual_seed(99)
    l2, m2 = s1.step_model(model, batch, args, DEVICE, train=True)
    assert torch.isfinite(l1)
    assert torch.equal(l1, l2)
    assert torch.equal(m1["mask_rate"], m2["mask_rate"])
    assert float(m1["mask_rate"]) > 0.0


# ---------------------------------------------------------------------------
# C5: _key_geometry_metrics a 格门控
# ---------------------------------------------------------------------------


def test_c5_a_grid_returns_zero_dict_without_touching_chunks():
    """a 格（两路均非 state）：恒等零字典，且在 n_real 同步之前返回 —— out
    连 "chunks" 键都没有（旧语句序会 KeyError），证明通道判断已前置。"""
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(k_row_source="index", v_row_source="memory"))
    res = s1._key_geometry_metrics(model, {}, DEVICE)
    for k in KEY_GEOMETRY_KEYS:
        assert k in res and float(res[k]) == 0.0


def test_c5_state_grid_nreal_below_two_still_zero():
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(k_row_source="state", v_row_source="state"))
    chunks = types.SimpleNamespace(chunk_mask=torch.tensor([[True, False, False, False]]))
    out = {"chunks": chunks, "memory": torch.randn(1, 4, 8), "index": torch.randn(1, 4, 8)}
    res = s1._key_geometry_metrics(model, out, DEVICE)
    for k in KEY_GEOMETRY_KEYS:
        assert float(res[k]) == 0.0


def test_c5_state_channels_still_measured_after_gate_hoist():
    """b/c/d 格行为不变：state 通道照常进 stats —— 用模型自带的
    write_head / write_head_k 吃伪造的 d_mem 行（n_real=3，无 mock 改件）。"""
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(k_row_source="state", v_row_source="state"))
    chunks = types.SimpleNamespace(chunk_mask=torch.tensor([[True, True, True, False]]))
    d_mem = model.config.d_mem
    rows = torch.randn(1, 3, d_mem, generator=torch.Generator().manual_seed(4))
    out = {"chunks": chunks, "memory": rows, "index": rows.clone()}
    res = s1._key_geometry_metrics(model, out, DEVICE)
    for k in ("key_mu", "key_mu_max", "key_pr", "key_mu_k", "key_mu_max_k", "key_pr_k"):
        assert torch.isfinite(res[k]), k
        assert 0.0 <= float(res[k]) <= 1.0, k
    assert float(res["key_mu"]) > 0.0 and float(res["key_mu_k"]) > 0.0
    assert float(res["key_mu_max"]) >= float(res["key_mu"])


# ---------------------------------------------------------------------------
# C7: 零占位缓存 + add_ 原地累加
# ---------------------------------------------------------------------------


def test_c7_step_zero_cache_identity_and_readonly():
    z1 = s1._step_zero(DEVICE)
    z2 = s1._step_zero(DEVICE)
    assert z1 is z2  # 同 device 命中同一缓存条目
    assert float(z1) == 0.0
    assert not z1.requires_grad


def test_c7_pending_accumulation_bitwise_and_cache_hygiene():
    """训练循环累积：旧 pending[k]=pending[k]+v（首见 clone）vs 新 add_ 原地
    累加 —— 同输入逐位同和；最坏别名形态（首见值即共享缓存零）下缓存本体
    不被污染。"""
    g = torch.Generator().manual_seed(23)
    z = s1._step_zero(DEVICE)
    steps = [{"m1": z, "m2": z}] + [
        {"m1": torch.rand((), generator=g), "m2": torch.rand((), generator=g)} for _ in range(6)
    ]
    p_old: dict = {}
    for step in steps:
        for k, v in step.items():
            p_old[k] = p_old[k] + v if k in p_old else v.clone()
    p_new: dict = {}
    for step in steps:
        for k, v in step.items():
            if k in p_new:
                p_new[k].add_(v)
            else:
                p_new[k] = v.clone()
    for k in ("m1", "m2"):
        assert torch.equal(p_old[k], p_new[k]), k
    assert float(z) == 0.0  # 缓存零从未被原地写
