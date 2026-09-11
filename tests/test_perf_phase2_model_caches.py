"""效率优化 Phase 2 模型侧单测（2026-09-11 施工单 β：C2/C6/C8）。

提案：outputs/_perf_audit_20260911/proposal.md §2（C2 _rope 缓存 / C6 valid
浮点副本下传 / C8 因果掩码·字节表·冻结标志缓存）。全部为「零语义变化」的
可检锚：缓存命中 vs 现算 torch.equal、多 dtype/device 键隔离、valid_f 下传
新旧路径前向逐位 + 梯度逐位、byte table 缓存在权重原地更新（_version 自增）
后正确失效。全部 CPU 小形状。
"""

from __future__ import annotations

import pytest
import torch
import torch.nn.functional as F

from flued.v34.model import (
    DiTStyleBlock,
    ParallelAttention,
    QueryPool,
    _ROPE_CACHE,
    _plastic_signed_confidence,
    _rope,
)
from flued.v36.model import (
    FLUEDV36,
    GlobalSpanDecoder,
    PlainByteLookup,
    SLMBackbone,
    V36Config,
    _CAUSAL_MASK_CACHE,
    _causal_keep_mask,
)


@pytest.fixture(autouse=True)
def _seed_and_clean_caches():
    torch.manual_seed(0)
    _ROPE_CACHE.clear()
    _CAUSAL_MASK_CACHE.clear()
    yield
    _ROPE_CACHE.clear()
    _CAUSAL_MASK_CACHE.clear()


def _tiny_config(**overrides) -> V36Config:
    """与 tests/test_v37_probe.py 同款小配置（CPU 可跑、slm a 格合法）。"""
    cfg = dict(
        d_byte=64, encoder_layers=2, segmentor_layers=2, nhead=4, ffn_dim=128,
        d_mem=96, summarizer_slots=2, summarizer_hidden=128,
        kda_heads=2, kda_head_k=16, kda_head_v=32, write_hidden=128,
        readout_queries=1, d_pack=64, d_backbone=64,
        backbone_layers=3, backbone_nhead=4, backbone_ffn=128,
        decoder_hidden=128, decoder_layers=2,
        max_chunks=32, max_span=16, bytes_per_chunk=8, max_positions=64,
        per_chunk_readout=True, summarizer_type="dit", backbone_mode="slm",
        boundary_mode="uniform", kda_impl="torch",
        k_row_source="index", v_row_source="memory",
    )
    cfg.update(overrides)
    return V36Config(**cfg)


def _valid2d(bsz: int, seq: int) -> torch.Tensor:
    valid = torch.ones(bsz, seq, dtype=torch.bool)
    valid[0, seq // 2:] = False
    valid[1, -1] = False
    return valid


# --- C2: _rope cos/sin 缓存 ---------------------------------------------------


def test_rope_cache_hit_bitwise_matches_fresh():
    for dim in (8, 16):
        x = torch.randn(2, 7, dim)
        pos = torch.arange(7)
        fresh = _rope(x, pos)  # 旧路径现算，不进缓存
        hit = _rope(x, pos, cache_key=f"t1:{dim}")  # 首调建缓存
        again = _rope(x, pos, cache_key=f"t1:{dim}")  # 二调命中
        assert torch.equal(fresh, hit)
        assert torch.equal(fresh, again)
    # 4D（注意力头排布）同验：基表 (seq, dim) 逐位 = 现算
    x4 = torch.randn(2, 3, 7, 8)
    pos4 = torch.arange(7)
    assert torch.equal(_rope(x4, pos4), _rope(x4, pos4, cache_key="t1:4d"))


def test_rope_cache_key_isolates_dtype_and_device():
    x32 = torch.randn(1, 5, 8)
    pos = torch.arange(5)
    a = _rope(x32, pos, cache_key="iso")
    b = _rope(x32.double(), pos, cache_key="iso")
    assert a.dtype == torch.float32 and b.dtype == torch.double
    # 键隔离：各自命中各自表项，均与现算逐位一致
    assert torch.equal(a, _rope(x32, pos))
    assert torch.equal(b, _rope(x32.double(), pos))
    assert ("iso", 8, x32.device, torch.float32) in _ROPE_CACHE
    assert ("iso", 8, x32.device, torch.double) in _ROPE_CACHE
    # 不同 key 字符串互不串
    assert ("other", 8, x32.device, torch.float32) not in _ROPE_CACHE
    assert torch.equal(_rope(x32, pos, cache_key="other"), a)
    # device 轴同理（无 CUDA 时 CPU 单设备天然隔离）
    if torch.cuda.is_available():
        xc = x32.detach().to("cuda")
        c = _rope(xc, pos, cache_key="iso")
        assert ("iso", 8, xc.device, torch.float32) in _ROPE_CACHE
        assert torch.equal(c, _rope(xc, pos))
        assert torch.equal(a, _rope(x32, pos, cache_key="iso"))  # CPU 表项不受扰


def test_parallel_attention_rope_cache_repeat_bitwise():
    attn = ParallelAttention(dim=16, nhead=4, use_rope=True, use_alibi=True).eval()
    x = torch.randn(2, 9, 16)
    valid = _valid2d(2, 9)
    with torch.no_grad():
        a = attn(x, valid)  # 首跑建 pa:{seq} 缓存
        b = attn(x, valid)  # 二跑命中
    assert torch.equal(a, b)


def test_query_pool_rope_cache_repeat_bitwise():
    pool = QueryPool(dim=16, slots=4, nhead=4, use_position=True).eval()
    spans = torch.randn(2, 3, 6, 16)
    token_mask = torch.ones(2, 3, 6, dtype=torch.bool)
    token_mask[0, 1, 4:] = False
    with torch.no_grad():
        a = pool(spans, token_mask)  # 首跑建 qp_q/qp_k 缓存
        b = pool(spans, token_mask)  # 二跑命中
    assert torch.equal(a, b)


# --- C6: valid 浮点副本一次计算沿链下传 ---------------------------------------


def test_parallel_attention_valid_f_bitwise():
    attn = ParallelAttention(dim=16, nhead=4, use_rope=True, use_alibi=True).eval()
    x = torch.randn(2, 9, 16)
    valid = _valid2d(2, 9)
    with torch.no_grad():
        old = attn(x, valid)
        new = attn(x, valid, valid_f=valid.unsqueeze(-1).to(x.dtype))
        # dtype 不齐的 valid_f 必须回落现算，不得污染输出数值/dtype
        wrong = attn(x, valid, valid_f=valid.unsqueeze(-1).to(torch.float64))
    assert torch.equal(old, new)
    assert torch.equal(old, wrong)
    # E123 block_mask 通路 + 缓存命中二跑同验
    bm = torch.zeros(2, 1, 1, 9, dtype=torch.bool)
    bm[1, 0, 0, 2] = True
    with torch.no_grad():
        m1 = attn(x, valid, bm, valid_f=valid.unsqueeze(-1).to(x.dtype))
        m2 = attn(x, valid, bm, valid_f=valid.unsqueeze(-1).to(x.dtype))
    assert torch.equal(m1, m2)


def test_dit_block_valid_f_bitwise():
    blk = DiTStyleBlock(dim=16, nhead=4, ffn_dim=32, use_rope=True, use_alibi=False).eval()
    x = torch.randn(2, 9, 16)
    valid = _valid2d(2, 9)
    noise = torch.tensor([0.0, 0.5])
    with torch.no_grad():
        old = blk(x, valid, noise)
        new = blk(x, valid, noise, valid_f=valid.unsqueeze(-1).to(x.dtype))
        wrong = blk(x, valid, noise, valid_f=valid.unsqueeze(-1).to(torch.float64))
    assert torch.equal(old, new)
    assert torch.equal(old, wrong)


def test_valid_f_grad_flow_bitwise_matches_old_path():
    a1 = ParallelAttention(dim=16, nhead=4, use_rope=True, use_alibi=False)
    a2 = ParallelAttention(dim=16, nhead=4, use_rope=True, use_alibi=False)
    a2.load_state_dict(a1.state_dict())
    x1 = torch.randn(2, 9, 16, requires_grad=True)
    x2 = x1.detach().clone().requires_grad_(True)
    valid = _valid2d(2, 9)
    o_old = a1(x1, valid)
    o_new = a2(x2, valid, valid_f=valid.unsqueeze(-1).to(x2.dtype))
    assert torch.equal(o_old, o_new)
    o_old.square().mean().backward()
    o_new.square().mean().backward()
    assert torch.equal(x1.grad, x2.grad)
    for (n1, p1), (n2, p2) in zip(a1.named_parameters(), a2.named_parameters()):
        assert n1 == n2
        assert torch.equal(p1.grad, p2.grad)


def test_v36_encode_chain_bitwise_vs_oldpath_reference():
    torch.manual_seed(7)
    model = FLUEDV36(_tiny_config()).eval()
    tokens = torch.randint(1, 256, (2, 24))
    tokens[0, :5] = 0  # PAD 位 → valid 含 False，掩码乘法有真实区分度
    with torch.no_grad():
        byte_states, confidence, valid, logits = model._encode(tokens)
        # 参照 = 旧路径逐块现算（valid_f=None 走块内 .to）
        x = model.byte_lookup(tokens)
        noise = x.new_zeros(tokens.size(0))
        for block in model.encoder_blocks:
            x = block(x, valid, noise, None)
        ref_byte_states = x
        for block in model.segmentor_blocks:
            x = block(x, valid, noise)
        ref_logits = model.segmentor_head(x).squeeze(-1)
    assert torch.equal(byte_states, ref_byte_states)
    assert torch.equal(logits, ref_logits)
    assert torch.equal(confidence, _plastic_signed_confidence(ref_logits))


# --- C8: 因果掩码 / 字节表 / 冻结标志缓存 --------------------------------------


def test_causal_keep_mask_values_and_entry_identity():
    keep, eye = _causal_keep_mask(6, torch.device("cpu"))
    assert torch.equal(keep, ~torch.triu(torch.ones(6, 6, dtype=torch.bool), diagonal=1))
    assert torch.equal(eye, torch.eye(6, dtype=torch.bool))
    keep2, eye2 = _causal_keep_mask(6, torch.device("cpu"))
    assert keep2 is keep and eye2 is eye  # 同 (n, device) 命中同一表项


def test_slm_backbone_forward_bitwise_with_and_without_mask_cache():
    cfg = _tiny_config(backbone_layers=3)
    torch.manual_seed(17)
    bb = SLMBackbone(cfg).eval()
    bsz, n = 2, 8
    k = torch.randn(bsz, n, cfg.d_mem)
    v = torch.randn(bsz, n, cfg.d_mem)
    chunk_mask = torch.ones(bsz, n, dtype=torch.bool)
    chunk_mask[0, 5:] = False
    pos = torch.randn(1, n, cfg.d_backbone)
    store_block = torch.zeros(bsz, n, n, dtype=torch.bool)
    store_block[0, 3, 2] = True
    with torch.no_grad():
        o1 = bb(k, v, chunk_mask, pos, store_block=store_block)  # 建缓存
        _CAUSAL_MASK_CACHE.clear()
        o2 = bb(k, v, chunk_mask, pos, store_block=store_block)  # 清后现算
        o3 = bb(k, v, chunk_mask, pos, store_block=store_block)  # 命中
    assert torch.equal(o1, o2)
    assert torch.equal(o2, o3)


def test_byte_table_cache_hit_and_version_invalidation():
    cfg = _tiny_config()
    torch.manual_seed(13)
    lookup = PlainByteLookup(cfg.d_byte)
    dec = GlobalSpanDecoder(cfg, lookup).eval()
    for p in dec.parameters():
        p.requires_grad_(False)
    cond = torch.randn(2, 5, cfg.d_backbone)
    token_mask = torch.ones(2, 5, cfg.max_span, dtype=torch.bool)
    token_mask[1, :, 8:] = False
    with torch.no_grad():
        out1 = dec(cond, token_mask)
    key1 = (lookup.embedding.weight._version, cond.device, cond.dtype)
    assert key1 in dec._byte_table_cache
    w1, table1 = dec._byte_table_cache[key1]
    fresh1 = F.normalize(lookup(torch.arange(258)).to(cond.dtype), dim=-1)
    assert torch.equal(table1, fresh1)  # 缓存值 = 现算
    with torch.no_grad():
        out2 = dec(cond, token_mask)  # 命中路径
    assert torch.equal(out1, out2)
    assert dec._byte_table_cache[key1][1] is table1  # 命中未重建
    # 权重原地更新 → _version 自增 → 缓存必须失效并装新值
    with torch.no_grad():
        lookup.embedding.weight.add_(0.25)
        out3 = dec(cond, token_mask)
    key3 = (lookup.embedding.weight._version, cond.device, cond.dtype)
    assert key3[0] != key1[0]
    assert key3 in dec._byte_table_cache
    w3, table3 = dec._byte_table_cache[key3]
    assert w3 is lookup.embedding.weight
    fresh3 = F.normalize(lookup(torch.arange(258)).to(cond.dtype), dim=-1)
    assert torch.equal(table3, fresh3)  # 失效后重装的是新表现算值
    assert not torch.equal(table3, table1)
    assert not torch.equal(out3, out2)  # 前向吃到的确实是新表


def test_byte_table_cache_bypassed_when_weight_trainable():
    cfg = _tiny_config()
    torch.manual_seed(23)
    lookup = PlainByteLookup(cfg.d_byte)  # requires_grad 默认 True
    dec = GlobalSpanDecoder(cfg, lookup).eval()
    cond = torch.randn(2, 5, cfg.d_backbone)
    token_mask = torch.ones(2, 5, cfg.max_span, dtype=torch.bool)
    with torch.no_grad():
        out = dec(cond, token_mask)
    assert not dec._byte_table_cache  # 可训表整体旁路：每前向现算（梯度序不变）
    assert torch.isfinite(out).all()
    # 冻结→解冻的运行期翻转：缓存里绝不能剩旧表给可训权重喂无梯度张量
    for p in dec.parameters():
        p.requires_grad_(False)
    with torch.no_grad():
        dec(cond, token_mask)  # 先建冻结缓存
    assert dec._byte_table_cache
    cached_before = dict(dec._byte_table_cache)
    keys_before = set(cached_before)
    for p in dec.parameters():
        p.requires_grad_(True)
    out_g = dec(cond, token_mask)
    out_g.sum().backward()
    assert lookup.embedding.weight.grad is not None  # 梯度经表回流通路完好
    # 解冻态不读也不写缓存：表项集合与对象均保持原样（旧表项允许滞留，门在读侧）
    assert set(dec._byte_table_cache) == keys_before
    assert all(dec._byte_table_cache[k] is cached_before[k] for k in keys_before)


def test_front_end_frozen_cache_and_reset():
    torch.manual_seed(29)
    model = FLUEDV36(_tiny_config()).eval()
    assert model._front_end_frozen() is False  # 默认全可训（首查即缓存 False）
    for p in model.parameters():
        p.requires_grad_(False)
    # 冻结面 setup 期已变 → 显式 reset 后重扫（运行期不变量 + 安全阀语义）
    model._front_end_frozen_reset()
    assert model._front_end_frozen() is True
    assert model._front_end_frozen() is True  # 缓存命中
    tokens = torch.randint(1, 256, (1, 32))
    bs, conf, _valid, _lg = model._encode(tokens)
    assert not bs.requires_grad and not conf.requires_grad  # 冻结语义不变
    # 运行期解冻必须再经显式 reset，判定才翻新
    for p in model.parameters():
        p.requires_grad_(True)
    model._front_end_frozen_reset()
    assert model._front_end_frozen() is False
