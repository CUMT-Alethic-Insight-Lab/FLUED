"""H-sup 梯度余弦探针单测（tools/analysis/v3_6/probe_h_sup_gradcos.py）。

Covers:
  (1) 参数组前缀在 tiny d 格模型上的匹配（非空/边界正确：kda_write_v 不吃
      write_head_k，readout 两组恰为两枚 readout_query，summarizer 头组互斥）；
  (2) window_losses 与 step_model(train=False) eval 姿态的逐位 parity（同种子
      同掩码，byte_span 口径，tiny d 格 CPU）——「逐位复用训练器机器」的硬守卫；
  (3) measure_window 的 N/A 纪律：backbone / K 通道（write_head_k /
      state_machine_k.readout_query / index_ffn）direct 结构性零梯度 → cos 为
      None 不报错；双路径组（summarizer/kda_write_v/readout_query_v/encoder/
      decoder/byte_lookup）cos 有限且 ∈ [-1, 1]；
  (4) _cos64 代数（同向=1/反向=-1/正交=0/零范数或缺失=None）；
  (5) bootstrap_ci95 确定性与退化形态（常数列 CI 宽度 0）；
  (6) 判读尺 verdict 的机械映射（实锤/正交/同向/混合/N/A 五种形态）；
  (7) 基座全键全形校验 loud-fail（缺键/形不符/冗键三形态 + 干净通过）。
Tiny 随机初始化 d 格 (k=state, v=state) CPU 模型 (kda_impl="torch",
boundary_mode="uniform")；只测接线与代数，不测训练行为。
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
import torch

import tools.train.v3_6.train_v36_s1 as s1
from tools.analysis.v3_6 import probe_h_sup_gradcos as probe
from tools.train.v3_3.train_v33 import make_byte_mask
from tests.test_e120_readout_swap import _ids, _tiny_d_config
from flued.data import MASK_ID
from flued.v36 import FLUEDV36

DEVICE = torch.device("cpu")

_STEP_NS = SimpleNamespace(
    mask_prob=0.15, mask_span_min=1, mask_span_max=8, mask_mode="byte_span",
    max_chunks=32, max_span=16, task1_loss_weight=1.0, task2_loss_weight=1.0,
    predict_weight=1.0, predict_mode="latent", amp=False,
    cumulative_mask_retention=True,
)


def _model(seed: int = 0) -> FLUEDV36:
    torch.manual_seed(seed)
    model = FLUEDV36(_tiny_d_config()).eval()
    for p in model.parameters():
        p.requires_grad_(True)
    model._front_end_frozen_reset()
    return model


def _masked_source(t: int = 96, mask_prob: float = 0.15, seed: int = 7):
    clean = _ids(seed=seed, t=t)
    torch.manual_seed(1234)
    byte_mask = make_byte_mask(clean.ne(0), mask_prob, 1, 8)
    source = clean.masked_fill(byte_mask, MASK_ID)
    return clean, byte_mask, source


# --- 1. 参数组前缀匹配 -------------------------------------------------------


def test_group_prefixes_cover_tiny_d_model():
    model = _model()
    groups = probe.build_param_groups(model)
    assert set(groups) == set(probe.GROUP_PREFIXES)
    for g, members in groups.items():
        assert members, f"组 {g} 空"
    # 边界：kda_write_v 只吃 write_head.*，不吃 write_head_k.*
    names_v = {n for n, _ in groups["kda_write_v"]}
    names_k = {n for n, _ in groups["kda_write_k"]}
    assert names_v and names_k and names_v.isdisjoint(names_k)
    assert all(n.startswith("write_head.") for n in names_v)
    assert all(n.startswith("write_head_k.") for n in names_k)
    # readout 两组恰为两枚 readout_query 参数
    assert [n for n, _ in groups["readout_query_v"]] == ["state_machine.readout_query"]
    assert [n for n, _ in groups["readout_query_k"]] == ["state_machine_k.readout_query"]
    # summarizer 头组互斥且并入 headline
    hv = {n for n, _ in groups["summarizer_head_v"]}
    hk = {n for n, _ in groups["summarizer_head_k"]}
    headline = {n for n, _ in groups["summarizer"]}
    assert hv and hk and hv.isdisjoint(hk) and hv | hk <= headline
    # backbone 组在岗（结构对照），segmentor/decoder_in/chunk_pos 不在任何组（未测件）
    assert any(n.startswith("backbone.") for n, _ in groups["backbone"])
    union = {n for members in groups.values() for n, _ in members}
    assert not any(n.startswith(("segmentor", "decoder_in", "chunk_pos", "bridge")) for n in union)


def test_group_empty_prefix_loud_fail():
    model = _model()
    broken = dict(probe.GROUP_PREFIXES)
    broken["nonexistent_group"] = ("no_such_module.",)
    saved = probe.GROUP_PREFIXES
    try:
        probe.GROUP_PREFIXES = broken
        with pytest.raises(ValueError, match="nonexistent_group"):
            probe.build_param_groups(model)
    finally:
        probe.GROUP_PREFIXES = saved


# --- 2. 与 step_model eval 姿态逐位 parity -----------------------------------


def test_window_losses_match_step_model_eval():
    model = _model()
    clean = _ids(seed=3, t=96)
    # step_model 内部自己造掩码（byte_span 走全局 torch RNG）——同种子复演
    torch.manual_seed(99)
    _loss, metrics = s1.step_model(model, (clean,), _STEP_NS, DEVICE, train=False)
    torch.manual_seed(99)
    byte_mask = make_byte_mask(clean.ne(0), _STEP_NS.mask_prob, 1, 8)
    source = clean.masked_fill(byte_mask, MASK_ID)
    direct_loss, completion_loss = probe.window_losses(model, source, clean, byte_mask, _STEP_NS, DEVICE)
    assert float(direct_loss.detach()) == float(metrics["direct_loss"])
    assert float(completion_loss.detach()) == float(metrics["completion_loss"])
    assert torch.isfinite(direct_loss) and torch.isfinite(completion_loss)


# --- 3. measure_window 的 N/A 纪律 -------------------------------------------


def test_measure_window_na_discipline():
    model = _model()
    clean, byte_mask, source = _masked_source()
    groups = probe.build_param_groups(model)
    row = probe.measure_window(model, source, clean, byte_mask, _STEP_NS, DEVICE, groups)
    assert row["direct_loss"] > 0 and row["completion_loss"] > 0
    g = row["groups"]
    # 结构对照：direct 不过 backbone → direct 零梯度 → N/A（cos None, 范数 None）
    assert g["backbone"]["cos"] is None
    assert g["backbone"]["grad_norm_direct"] is None
    assert g["backbone"]["n_with_both_grads"] == 0
    assert g["backbone"]["grad_norm_completion"] is not None  # completion 照过 backbone
    # K 通道三组：completion-only，direct 结构性零梯度 → N/A
    for grp in ("kda_write_k", "readout_query_k", "summarizer_head_k"):
        assert g[grp]["cos"] is None, grp
        assert g[grp]["grad_norm_direct"] is None, grp
        assert g[grp]["grad_norm_completion"] is not None, grp
    # 双路径组：cos 有限 ∈ [-1, 1]，两侧范数俱在，逐层明细键数 == 组内张量数
    for grp in (
        "summarizer_shared", "summarizer_head_v",
        "kda_write_v", "readout_query_v",
        "encoder_blocks", "decoder", "byte_lookup",
    ):
        a = g[grp]
        assert a["cos"] is not None and -1.0 <= a["cos"] <= 1.0, grp
        assert a["grad_norm_direct"] is not None and a["grad_norm_direct"] > 0, grp
        assert a["grad_norm_completion"] is not None and a["grad_norm_completion"] > 0, grp
        assert a["n_with_both_grads"] == a["n_tensors"], grp
        assert len(a["layer_cos"]) == a["n_tensors"], grp
    # headline summarizer：含 completion-only 的 index_ffn 头——交集口径不含该 6 枚,
    # 逐层余弦在其键上为 None；另有每枚 DiT block 的 noise_cond.0.weight 双侧恰零
    # 梯度（noise 输入恒零，输入侧权重零范数 → cos 未定义；bias 与下游层有真梯度），
    # 同属 N/A 家族（结构 N/A 与零范数 N/A 两形态）
    a = g["summarizer"]
    n_head_k = g["summarizer_head_k"]["n_tensors"]
    assert a["cos"] is not None and -1.0 <= a["cos"] <= 1.0
    assert a["grad_norm_direct"] is not None and a["grad_norm_direct"] > 0
    assert a["n_with_both_grads"] == a["n_tensors"] - n_head_k
    none_keys = {k for k, v in a["layer_cos"].items() if v is None}
    structural = {k for k in none_keys if k.startswith("summarizer.index_ffn.")}
    zero_norm = none_keys - structural
    assert structural and len(structural) == n_head_k
    assert zero_norm and all(k.endswith(".noise_cond.0.weight") for k in zero_norm)


# --- 4. _cos64 代数 ----------------------------------------------------------


def test_cos64_algebra():
    a = torch.randn(64, dtype=torch.float32)
    b = torch.randn(64, dtype=torch.float32)
    assert probe._cos64(a, a) == pytest.approx(1.0, abs=1e-12)
    assert probe._cos64(a, -a) == pytest.approx(-1.0, abs=1e-12)
    x = torch.zeros(64)
    x[0] = 1.0
    y = torch.zeros(64)
    y[1] = 1.0
    assert probe._cos64(x, y) == pytest.approx(0.0, abs=1e-12)
    assert probe._cos64(torch.zeros(8), b[:8]) is None
    assert probe._cos64(None, b) is None
    assert probe._cos64(a, None) is None


# --- 5. bootstrap CI ---------------------------------------------------------


def test_bootstrap_ci95_deterministic_and_degenerate():
    vals = [0.1, -0.2, 0.05, -0.3, 0.0, 0.15, -0.1, 0.02]
    lo1, hi1 = probe.bootstrap_ci95(vals, n_boot=500, seed=1)
    lo2, hi2 = probe.bootstrap_ci95(vals, n_boot=500, seed=1)
    assert (lo1, hi1) == (lo2, hi2)  # 同种子逐位复演
    assert lo1 <= sum(vals) / len(vals) <= hi1
    c_lo, c_hi = probe.bootstrap_ci95([0.42] * 16, n_boot=100, seed=1)
    assert c_lo == c_hi == pytest.approx(0.42)  # 常数列 CI 宽度 0
    assert probe.bootstrap_ci95([], n_boot=100, seed=1) == (None, None)


# --- 6. 判读尺机械映射 --------------------------------------------------------


def _gs(summarizer, kda_write_v, readout_query_v):
    def entry(mean, lo, hi):
        return {"n": 8, "cos_mean": mean, "cos_ci95": [lo, hi], "frac_negative": 0.5}
    return {
        "summarizer": entry(*summarizer),
        "kda_write_v": entry(*kda_write_v),
        "readout_query_v": entry(*readout_query_v),
        "decoder": entry(0.9, 0.8, 0.95),
        "backbone": {"n": 0},  # 结构对照 N/A 形态
    }


def test_verdict_ruler():
    neg = (-0.3, -0.45, -0.15)
    pos = (0.4, 0.25, 0.55)
    zero = (0.02, -0.1, 0.12)
    v = probe.verdict(_gs(neg, neg, neg))
    assert v["h_sup"] == "升级已验证"
    assert v["per_group"]["summarizer"]["class"] == "negative_solid"
    assert v["per_group"]["backbone"]["class"] == "na"
    assert probe.verdict(_gs(zero, zero, zero))["h_sup"] == "证伪（正交）"
    assert probe.verdict(_gs(pos, pos, pos))["h_sup"] == "证伪（同向）"
    mixed = probe.verdict(_gs(neg, zero, neg))
    assert mixed["h_sup"] == "混合（不升级）"
    assert mixed["per_group"]["kda_write_v"]["class"] == "ci_contains_zero"


# --- 7. 基座全键全形校验 loud-fail --------------------------------------------


def test_audit_payload_full_key_shape():
    from pathlib import Path

    model = _model()
    sd = model.state_dict()
    ck = Path("dummy_ckpt")
    probe.audit_payload_full_key_shape(model, dict(sd), ck)  # 干净通过
    # 缺键
    missing = {k: v for k, v in sd.items() if not k.startswith("write_head.to_k")}
    with pytest.raises(SystemExit, match="全键全形校验失败"):
        probe.audit_payload_full_key_shape(model, missing, ck)
    # 形不符
    bad_shape = dict(sd)
    key = "write_head.to_v.weight"
    bad_shape[key] = torch.zeros(1, 1)
    with pytest.raises(SystemExit, match="全键全形校验失败"):
        probe.audit_payload_full_key_shape(model, bad_shape, ck)
    # 冗键
    extra = dict(sd)
    extra["ghost.param"] = torch.zeros(1)
    with pytest.raises(SystemExit, match="全键全形校验失败"):
        probe.audit_payload_full_key_shape(model, extra, ck)
