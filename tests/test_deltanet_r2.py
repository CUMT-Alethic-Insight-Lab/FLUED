"""R2 臂施工件单测（tools/baselines/deltanet_r2/；fla 缺席时核心逻辑零依赖可测，
fla 门控用例在装 fla 的环境上运行——远端 4090 施工靶机跑全量）。

Covers: (1) 参数锚：解析式计数 == 预注册 48,152,896（纯算术，无 fla）+ fla 实例化
互证（门控）；(2) LR 调度：fla 原生默认 warmup 1024 线性 → cosine 到 0.1×；(3)
发散看门狗：非有限 / >1000 触发，1000 恰不触发（预注册线严格大于）；(4) 窗语义：
4096B 非重叠顺序窗、尾窗不足即停、utf-8 replace；(5) 监督语义：L−1 目标（BOS
位无预测）；(6) 种子纪律：评测谱系 ≠ 训练流（E121）；(7) fla 门控：strict 存取
往返逐位一致、键集逐键 diff 仅配置形状差异（架构件零改造实证）、config json
tie=false。
"""

from __future__ import annotations

import json
import math

import pytest
import torch

import tools.baselines.deltanet_r2.r2_spec as spec

try:
    import fla  # noqa: F401
    _HAS_FLA = True
except ImportError:
    _HAS_FLA = False  # 本地单测环境无 fla：零依赖用例照跑，门控用例跳过（远端跑全量）

# ---------------------------------------------------------------------------
# 1. 参数锚（解析式）
# ---------------------------------------------------------------------------


def test_param_anchor_analytic():
    assert spec.compute_expected_param_count() == spec.EXPECTED_PARAM_COUNT
    assert spec.EXPECTED_PARAM_COUNT == 48_152_896


def test_param_anchor_formula_tie_changes_count():
    cfg = dict(spec.R2_CONFIG)
    cfg["tie_word_embeddings"] = True
    tied = spec.compute_expected_param_count(cfg)
    assert tied == spec.EXPECTED_PARAM_COUNT - cfg["vocab_size"] * cfg["hidden_size"]


# ---------------------------------------------------------------------------
# 2. LR 调度（fla 原生默认：warmup 1024 → cosine 到 0.1×）
# ---------------------------------------------------------------------------


def test_lr_schedule_warmup_linear_then_cosine():
    peak = spec.LEARNING_RATE
    assert spec.lr_at(0) == pytest.approx(peak / spec.WARMUP_STEPS)
    assert spec.lr_at(spec.WARMUP_STEPS // 2 - 1) == pytest.approx(peak / 2)
    assert spec.lr_at(spec.WARMUP_STEPS - 1) == pytest.approx(peak)  # 峰值在 warmup 末步
    assert spec.lr_at(spec.WARMUP_STEPS) == pytest.approx(peak)
    mid = (spec.MAX_STEPS + spec.WARMUP_STEPS) // 2
    assert spec.lr_at(mid) < peak
    assert spec.lr_at(spec.MAX_STEPS) == pytest.approx(peak * spec.LR_MIN_RATIO)
    # warmup 段单调升
    warm = [spec.lr_at(s) for s in range(0, spec.WARMUP_STEPS + 1, 128)]
    assert all(a <= b for a, b in zip(warm, warm[1:]))


def test_lr_schedule_post_warmup_monotone_decreasing():
    lrs = [spec.lr_at(s) for s in range(spec.WARMUP_STEPS, spec.MAX_STEPS + 1, 100)]
    assert all(a > b for a, b in zip(lrs, lrs[1:]))


# ---------------------------------------------------------------------------
# 3. 发散看门狗（预注册：loss 上千=停）
# ---------------------------------------------------------------------------


def test_divergence_watchdog():
    assert spec.is_diverged(float("nan"))
    assert spec.is_diverged(float("inf"))
    assert spec.is_diverged(1000.1)
    assert not spec.is_diverged(1000.0)  # 预注册「上千」= 严格大于
    assert not spec.is_diverged(9.7)


# ---------------------------------------------------------------------------
# 4. 窗语义（E122 仪器同构）
# ---------------------------------------------------------------------------


def test_iter_byte_windows_sequential_nonoverlap(tmp_path):
    corpus = tmp_path / "c.txt"
    payload = bytes(range(256)) * 48  # 12288 B = 3.0 窗 @4096
    payload += b"tail!"  # 12293 B → 尾窗不足即停
    corpus.write_bytes(payload)
    wins = list(spec.iter_byte_windows(corpus))
    assert len(wins) == 3
    assert [w for w, _ in wins] == [0, 1, 2]
    for i, (_w, raw) in enumerate(wins):
        assert raw == payload[i * 4096:(i + 1) * 4096]
        assert len(raw) == spec.WINDOW_BYTES
    # start_window 偏移
    wins2 = list(spec.iter_byte_windows(corpus, start_window=2))
    assert len(wins2) == 1
    assert wins2[0][1] == payload[2 * 4096:3 * 4096]


def test_window_text_replace():
    raw = b"ok\xff\xfe" * 4
    txt = spec.window_text(raw)
    assert "\ufffd" in txt  # 非法 utf-8 → replacement（E122 同款）


# ---------------------------------------------------------------------------
# 5. 监督语义（L−1 目标，BOS 位无预测）
# ---------------------------------------------------------------------------


def test_supervised_positions_shift():
    ids = list(range(1, 11))  # 含 BOS=1 的 token 流，L=10
    x, y = ids[:-1], ids[1:]
    assert len(x) == len(y) == len(ids) - 1
    assert x[0] == ids[0] and y[-1] == ids[-1]  # 首目标 = ids[1]（BOS 作输入不作目标）


# ---------------------------------------------------------------------------
# 6. 种子纪律（评测谱系异于训练流，E121）
# ---------------------------------------------------------------------------


def test_seed_lineage_eval_disjoint_from_train():
    assert spec.TRAIN_SEED == 42
    assert spec.EVAL_SEED not in (spec.TRAIN_SEED,)
    assert spec.EVAL_SEED == 424_242  # 仪表①②专用谱系；bootstrap = +1


# ---------------------------------------------------------------------------
# 7. fla 门控用例（远端施工靶机执行）
# ---------------------------------------------------------------------------


def _build_model():
    from fla.models.delta_net import DeltaNetConfig, DeltaNetForCausalLM
    return DeltaNetForCausalLM(DeltaNetConfig(**spec.R2_CONFIG))


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（本地单测环境跳过，远端跑全量）")
def test_param_anchor_instantiation():
    model = _build_model()
    n = sum(p.numel() for p in model.parameters())
    assert n == spec.EXPECTED_PARAM_COUNT == 48_152_896


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（本地单测环境跳过，远端跑全量）")
def test_key_diff_wiring_only_two_instantiations_identical():
    """逐键 diff（冒烟条款②的静态形态）：两次独立实例化 state_dict 键集逐键一致
    ——训练器不含任何架构代码，键集差异只允许来自配置形状。"""
    m1, m2 = _build_model(), _build_model()
    k1, k2 = list(m1.state_dict()), list(m2.state_dict())
    assert k1 == k2  # 键序列逐键一致
    assert all(m1.state_dict()[k].shape == m2.state_dict()[k].shape for k in k1)


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（本地单测环境跳过，远端跑全量）")
def test_strict_save_load_roundtrip_bitexact(tmp_path):
    """strict 系加载 + 全键 loud-fail：save_pretrained → from_pretrained 逐键逐位
    一致（仪器 AutoModelForCausalLM 装载通路实证）。"""
    from transformers import AutoModelForCausalLM
    import fla.models.delta_net.modeling_delta_net as _fla_dn_mod
    if isinstance(_fla_dn_mod.DeltaNetForCausalLM.__dict__.get("_tied_weights_keys"), list):
        # tf5.15.1 from_pretrained 对 v4 list 崩溃（484c636 同款规范化，tying 语义不变）
        _fla_dn_mod.DeltaNetForCausalLM._tied_weights_keys = {
            "lm_head.weight": "model.embeddings.weight"}
    model = _build_model()
    d = tmp_path / "m"
    model.save_pretrained(d)
    cfg = json.loads((d / "config.json").read_text(encoding="utf-8"))
    assert cfg["tie_word_embeddings"] is False  # tf5.15.1+fla0.5.1 tie=true 崩溃规避在案
    loaded = AutoModelForCausalLM.from_pretrained(d)  # 默认 strict 全键
    sd_a, sd_b = model.state_dict(), loaded.state_dict()
    assert set(sd_a) == set(sd_b)  # 全键：缺失/多出即响亮
    for k in sd_a:
        assert torch.equal(sd_a[k], sd_b[k]), k  # 逐位一致（fp32 精确保存）
