"""E124 切点钉死（cuts_override）单测（用户裁定 2026-09-10：内容缺席、结构不动）。

背景：「遮蔽不动分段」的旧假设在锚定段界器基座上被体制级证伪（遮蔽扰动
encoder 状态翻转切点，实测漂移率 95%，诊断 outputs/_diag_e124_mask_drift_20260910.json）。
cuts_override 线程让遮蔽前向复用干净窗预算的切点：chunk 网格（身份/数量/坐标）
锁定，byte_states/confidence 仍随遮蔽响应。

Covers: (1) cuts_override=None 与传「模型自产干净切点」两种调用逐位一致
（条件创建纪律：默认 = 旧路径）; (2) 遮蔽前向 + 钉死 → chunk_ids/offsets/
chunk_mask 与干净基线逐位一致（验收硬判据；夹具上未钉死对照确漂移，判据非空），
且 span_embeddings/confidence 仍随遮蔽响应（内容缺席半）; (3) shape/dtype 不符
与非 slm 支路一律响亮报错。

小模型夹具：动态段界器 tau_cut=0.0（随机初始化下 confidence 跨阈 ≈ 半数位，
窗得 23 chunk 的非退化网格），CPU、kda_impl="torch"，与 test_v37_oracle_probe
同款「只验接线/代数、不依赖训练行为」口径。
"""

from __future__ import annotations

import pytest
import torch

from flued.v36 import FLUEDV36, V36Config
import tools.train.v3_6.train_v36_s1 as s1


def _tiny_cfg(**overrides):
    cfg = dict(
        d_byte=64, encoder_layers=2, segmentor_layers=2, nhead=4, ffn_dim=128,
        d_mem=96, summarizer_slots=2, summarizer_hidden=128,
        kda_heads=2, kda_head_k=16, kda_head_v=32, write_hidden=128,
        readout_queries=1, d_pack=64, d_backbone=64,
        backbone_layers=3, backbone_nhead=4, backbone_ffn=128,
        decoder_hidden=128, decoder_layers=2,
        max_chunks=32, max_span=16, bytes_per_chunk=8, max_positions=64,
        per_chunk_readout=True, summarizer_type="dit", backbone_mode="slm",
        boundary_mode="dynamic", tau_cut=0.0, kda_impl="torch",
        k_row_source="index", v_row_source="state",
    )
    cfg.update(overrides)
    return V36Config(**cfg)


def _model(seed: int = 0, **kw) -> FLUEDV36:
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_cfg(**kw)).eval()


def _ids(seed: int = 1, t: int = 96):
    g = torch.Generator().manual_seed(seed)
    return torch.randint(1, 257, (1, t), generator=g)


def _clean_cuts(model, ids):
    """模型自产干净切点（= 仪器/落盘脚本口径：_encode → _cuts）。"""
    _bs, conf, valid, _ = model._encode(ids)
    hard_cut, _u8, _of = model._cuts(ids, conf, valid)
    return hard_cut, conf


def _mask(t: int = 96, s: int = 8, e: int = 24) -> torch.Tensor:
    m = torch.zeros(1, 1, 1, t, dtype=torch.bool)
    m[0, 0, 0, s:e] = True
    return m


# --- 1. None = 与传模型自产干净切点逐位一致 --------------------------------------


def test_none_vs_self_produced_cuts_bitwise():
    model = _model()
    ids = _ids()
    with torch.no_grad():
        out_ref = s1._slm_forward(model, ids, None)
        hard_cut, _conf = _clean_cuts(model, ids)
        out_ov = s1._slm_forward(model, ids, None, cuts_override=hard_cut)
    # 网格与读数面全部逐位一致（自产切点 = 现算切点，override 是恒等替换）
    assert torch.equal(out_ref["chunks"].chunk_ids, out_ov["chunks"].chunk_ids)
    assert torch.equal(out_ref["chunks"].offsets, out_ov["chunks"].offsets)
    assert torch.equal(out_ref["chunks"].chunk_mask, out_ov["chunks"].chunk_mask)
    assert torch.equal(out_ref["logits_direct"], out_ov["logits_direct"])
    assert torch.equal(out_ref["logits_backbone"], out_ov["logits_backbone"])


# --- 2. 遮蔽前向 + 钉死 → 网格与干净基线逐位一致（验收硬判据） ---------------------


def test_masked_pinned_grid_equals_clean_baseline():
    model = _model()
    ids = _ids()
    mask = _mask()
    with torch.no_grad():
        out_clean = s1._slm_forward(model, ids, None)
        hard_cut, conf_clean = _clean_cuts(model, ids)
        # 非空前提（现象学钉死）：本夹具上未钉死的遮蔽前向确实漂移——
        # 判据② 不是恒真空话
        out_drift = s1._slm_forward(model, ids, None, attn_block_mask=mask)
        assert not torch.equal(out_drift["chunks"].chunk_ids, out_clean["chunks"].chunk_ids)
        # 钉死 → chunk 网格（身份/坐标/数量）与干净基线逐位一致
        out_pin = s1._slm_forward(model, ids, None, attn_block_mask=mask,
                                  cuts_override=hard_cut)
        assert torch.equal(out_pin["chunks"].chunk_ids, out_clean["chunks"].chunk_ids)
        assert torch.equal(out_pin["chunks"].offsets, out_clean["chunks"].offsets)
        assert torch.equal(out_pin["chunks"].chunk_mask, out_clean["chunks"].chunk_mask)
        # 内容缺席半：byte_states/confidence 仍随遮蔽响应（结构不动 ≠ 全窗冻结）
        _bs_m, conf_m, _v, _l = model._encode(ids, attn_block_mask=mask)
        assert not torch.equal(conf_m, conf_clean)
        assert not torch.equal(out_pin["chunks"].span_embeddings,
                               out_clean["chunks"].span_embeddings)


# --- 3. 校验不符与非 slm 支路响亮报错 ----------------------------------------------


def test_cuts_override_loud_validation():
    model = _model()
    ids = _ids()
    hard_cut, _conf = _clean_cuts(model, ids)
    good = torch.zeros(1, ids.size(1), dtype=torch.bool)
    # shape 不符
    with pytest.raises(ValueError, match="cuts_override"):
        s1._slm_forward(model, ids, None,
                        cuts_override=torch.zeros(1, ids.size(1) + 1, dtype=torch.bool))
    with pytest.raises(ValueError, match="cuts_override"):
        s1._slm_forward(model, ids, None, cuts_override=hard_cut[:, :1])
    # dtype 不符
    with pytest.raises(ValueError, match="cuts_override"):
        s1._slm_forward(model, ids, None, cuts_override=good.long())
    # 非 slm 前向支路不支持（响亮报错，不静默忽略）
    model_attn = _model(backbone_mode="attn")
    with pytest.raises(ValueError, match="cuts_override"):
        s1.s1_forward(model_attn, ids, None, cuts_override=good)
