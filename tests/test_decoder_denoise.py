"""decoder 去噪臂单测（任务书 2026-08-29 冻结 v1.1 + 修订 v2 同日裁定:
docs/versions/v3.7/FLUED_V3_7_DECODER_DENOISE_20260829_CN.md; 训练器旋钮在
tools/train/v3_6/train_v36_s1.py 的 --decoder-denoise-* 旗标族）。

Covers: (1) 默认关 = legacy 路径逐位不变（扰动函数零调用 + direct 腿手工复算
逐位一致 + train=True 也不触发）; (2) 扰动只进 direct 腿——backbone 腿
logits 与 predict 锚 (v_rows) 逐位未动, direct logits 确实变化; (3) eval
(train=False) 永不扰动; (4) 课程边界 step 4999/5000/9999/10000 s 档前缀
切片切换与 m̂ 列激活（含 mhat_start 覆写）; (5) m̂ 列整行替换语义（选中行 ==
λopt 部署桥直算 m̂, 非加性）; (6) 冻结清单：仅 decoder 可训, decoder_in_mem/
chunk_pos/backbone/写入侧/tied byte_lookup 全冻; (7) step_model 计数列与
干净水位仪表; (8) 修订 v2 标量倍率语义：s 只乘 ε 项（s=0.5 vs s=2.0 同 seed
下残差恰 4 倍）。
Tiny 随机初始化 b 格 (k=state, v=memory) CPU 模型, boundary_mode="uniform"
保持分块确定; 只测接线与代数, 不测训练行为。
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
import torch

from flued.v36 import FLUEDV36
import tools.train.v3_6.train_v36_s1 as s1
from tests.test_v37_oracle_probe import _tiny_c_config

DEVICE = torch.device("cpu")


def _tiny_b_config(**overrides):
    # b 格 (k=state, v=memory): write_head_k/state_machine_k/decoder_in_mem 在岗
    return _tiny_c_config(k_row_source="state", v_row_source="memory", **overrides)


def _model(seed: int = 0) -> FLUEDV36:
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_b_config()).eval()


def _ids(seed: int = 1, t: int = 96):
    g = torch.Generator().manual_seed(seed)
    return torch.randint(1, 257, (1, t), generator=g)


def _denoise_args(**overrides):
    args = SimpleNamespace(
        decoder_denoise=True,
        decoder_denoise_p_noise=0.5,
        decoder_denoise_p_mhat=0.25,
        decoder_denoise_row_frac=0.5,
        decoder_denoise_mhat_start=10000,
        decoder_denoise_step=0,
        decoder_denoise_s_ladder="0.5,1.0,2.0",
    )
    for k, v in overrides.items():
        setattr(args, k, v)
    return args


@pytest.fixture
def fake_fuzz():
    """注入玩具前置测量产物 (修订 v2 单部署桥采样器), 用后恢复全局。"""
    d_mem, feat = 96, 2 * 32 + 1  # d_mem; H*hv + 截距行
    W = torch.randn(feat, d_mem, generator=torch.Generator().manual_seed(5)) * 0.02
    fuzz = {
        "W": W,
        "scale": 1.0,
        "chol": torch.eye(d_mem) * 0.1,
        "rho": 0.8,
        "lam": 1.0,
        "tag": "opt",
    }
    old = s1._DENOISE_FUZZ
    s1._DENOISE_FUZZ = fuzz
    try:
        yield fuzz
    finally:
        s1._DENOISE_FUZZ = old


# --- 1. 默认关 = legacy 路径逐位不变 -----------------------------------------


def test_off_bit_identical_and_perturb_never_called():
    model, ids = _model(), _ids()
    called = []
    orig = s1._decoder_denoise_perturb
    s1._decoder_denoise_perturb = lambda *a, **k: called.append(1)
    try:
        # 无旗标属性的 args (= CLI 默认关), train=True 也不许触发
        out = s1._slm_forward(model, ids, SimpleNamespace(), train=True)
    finally:
        s1._decoder_denoise_perturb = orig
    assert not called, "关态调用了扰动函数"
    assert out["denoise_stats"] is None
    # direct 腿 = decoder_in_mem(v_rows)+pos→decoder 手工复算, 逐位一致
    n = out["chunks"].chunk_mask.size(1)
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n]
    ref = model.decoder(model.decoder_in_mem(out["v_rows"]) + pos, out["chunks"].token_mask)
    assert torch.equal(ref, out["logits_direct"])


def test_parser_defaults_off():
    from tools.train.v3_6.train_v36 import build_parser

    parser = build_parser()
    s1._add_s1_args(parser)
    args = parser.parse_args([])
    assert args.decoder_denoise is False
    assert args.decoder_denoise_fuzz_id == ""
    assert args.decoder_denoise_p_noise == 0.5
    assert args.decoder_denoise_p_mhat == 0.25
    assert args.decoder_denoise_row_frac == 0.5
    assert args.decoder_denoise_mhat_start == 10000
    assert args.decoder_denoise_s_ladder == "0.5,1.0,2.0"


# --- 2. 扰动只进 direct 腿 ---------------------------------------------------


def test_perturbation_only_touches_direct_leg(fake_fuzz):
    model, ids = _model(), _ids()
    out_off = s1._slm_forward(model, ids, SimpleNamespace())
    s1._DENOISE_GENERATOR.manual_seed(123)
    args = _denoise_args(decoder_denoise_p_noise=1.0, decoder_denoise_row_frac=1.0)
    out_on = s1._slm_forward(model, ids, args, train=True)
    # predict 锚 (v_rows) 与 backbone 腿逐位未动
    assert torch.equal(out_off["v_rows"], out_on["v_rows"])
    assert torch.equal(out_off["logits_backbone"], out_on["logits_backbone"])
    # direct 腿确实被扰动
    assert not torch.equal(out_off["logits_direct"], out_on["logits_direct"])
    st = out_on["denoise_stats"]
    assert st is not None
    assert st["noise_frac"] > 0.99 and st["mhat_frac"] == 0.0 and st["clean_frac"] < 0.01
    assert st["grade"] == 0.5  # step 0 课程 = 仅 s=0.5 轻档


def test_eval_never_perturbed(fake_fuzz):
    model, ids = _model(), _ids()
    out_off = s1._slm_forward(model, ids, SimpleNamespace())
    args = _denoise_args(decoder_denoise_p_noise=1.0, decoder_denoise_row_frac=1.0)
    out_eval = s1._slm_forward(model, ids, args, train=False)
    assert out_eval["denoise_stats"] is None
    assert torch.equal(out_off["logits_direct"], out_eval["logits_direct"])


# --- 3. 课程边界 -------------------------------------------------------------


def test_curriculum_boundaries():
    ladder = [0.5, 1.0, 2.0]
    cases = [
        (0, [0.5], False),
        (4999, [0.5], False),
        (5000, [0.5, 1.0], False),
        (9999, [0.5, 1.0], False),
        (10000, [0.5, 1.0, 2.0], True),
        (20000, [0.5, 1.0, 2.0], True),
    ]
    for step, s_grades, mhat in cases:
        g, m = s1._denoise_curriculum(step, 10000, ladder)
        assert g == s_grades and m == mhat, (step, g, m)
    # mhat_start 覆写: 三档 10K 起开, m̂ 列由旗标独立控制
    g, m = s1._denoise_curriculum(10000, 15000, ladder)
    assert g == [0.5, 1.0, 2.0] and m is False
    g, m = s1._denoise_curriculum(15000, 15000, ladder)
    assert m is True


# --- 4. m̂ 列整行替换语义 -----------------------------------------------------


def test_mhat_column_replaces_whole_rows(fake_fuzz):
    from tools.analysis.v3_6.probe_decoder_fuzz_id import mhat_from_window

    model, ids = _model(), _ids()
    out0 = s1._slm_forward(model, ids, SimpleNamespace())
    chunks, v_rows, index = out0["chunks"], out0["v_rows"], out0["index"]
    args = _denoise_args(
        decoder_denoise_p_noise=0.0, decoder_denoise_p_mhat=1.0,
        decoder_denoise_row_frac=1.0, decoder_denoise_mhat_start=0,
        decoder_denoise_step=10000,
    )
    s1._DENOISE_GENERATOR.manual_seed(7)
    v_dec, st = s1._decoder_denoise_perturb(model, v_rows, chunks, index, args)
    real = chunks.chunk_mask
    # 全实行被替换; 替换值 == λopt 部署桥直算 m̂ (非加性, 固定桥不抽档)
    mhat = mhat_from_window(model, index.float(), real, fake_fuzz["W"], fake_fuzz["scale"])
    n = mhat.size(1)
    assert torch.allclose(v_dec[0, :n], mhat[0], atol=1e-5)
    assert st["mhat_frac"] == 1.0 and st["noise_frac"] == 0.0 and st["clean_frac"] == 0.0
    # v_rows 本体不动 (不许原地改)
    assert torch.equal(v_rows, out0["v_rows"])


def test_noise_column_formula(fake_fuzz):
    """列① 合成式 (修订 v2): ṽ = ρ·m + s·ε (范数匹配后加性, s 只乘 ε 项,
    撞行归替换列)。"""
    model, ids = _model(), _ids()
    out0 = s1._slm_forward(model, ids, SimpleNamespace())
    chunks, v_rows, index = out0["chunks"], out0["v_rows"], out0["index"]
    args = _denoise_args(
        decoder_denoise_p_noise=1.0, decoder_denoise_p_mhat=0.0,
        decoder_denoise_row_frac=1.0, decoder_denoise_step=0,
    )
    s1._DENOISE_GENERATOR.manual_seed(11)
    v_dec, st = s1._decoder_denoise_perturb(model, v_rows, chunks, index, args)
    real = chunks.chunk_mask
    assert st["noise_frac"] == 1.0 and st["clean_frac"] == 0.0
    assert st["grade"] == 0.5  # step 0 课程 = 仅 s=0.5 轻档
    # 扰动后行 != 原行, 且范数向 ρ 倍收缩方向移动 (玩具 chol=0.1I 小噪声)
    assert not torch.equal(v_dec[real], v_rows[real])
    assert torch.allclose(v_dec[~real], v_rows[~real])  # padded 行不动
    assert torch.equal(v_rows, out0["v_rows"])  # 本体不动
    # 修订 v2 标量倍率语义: 同 seed 下 s=0.5 vs s=2.0 抽签序列一致 (档选择
    # 与 z 抽取与 s 值无关), 实数行残差恰 4 倍
    rho = fake_fuzz["rho"]
    for ladder, scale in (("0.5", 0.5), ("2.0", 2.0)):
        a = _denoise_args(
            decoder_denoise_p_noise=1.0, decoder_denoise_p_mhat=0.0,
            decoder_denoise_row_frac=1.0, decoder_denoise_step=0,
            decoder_denoise_s_ladder=ladder,
        )
        s1._DENOISE_GENERATOR.manual_seed(11)
        vd, st_l = s1._decoder_denoise_perturb(model, v_rows, chunks, index, a)
        assert st_l["grade"] == scale
        eps = vd[real] - rho * v_rows[real].float()
        if scale == 0.5:
            eps_ref = eps
        else:
            assert torch.allclose(eps, 4.0 * eps_ref, atol=1e-6)


# --- 5. 冻结清单 -------------------------------------------------------------


def test_freeze_only_decoder_trainable():
    model = _model()
    n_train, n_frozen = s1._decoder_denoise_freeze(model)
    assert n_train > 0 and n_frozen > 0
    # 端口链/前端/写入侧全冻
    assert model.decoder_in_mem.weight.requires_grad is False
    assert model.chunk_pos.weight.requires_grad is False
    for mod in (model.backbone, model.summarizer, model.write_head_k, model.state_machine_k):
        assert all(not p.requires_grad for p in mod.parameters())
    # tied 字节表: 同一参数对象, 按 E31/E34 裁定固定公尺不许被误训
    assert model.decoder.byte_lookup is model.byte_lookup
    assert model.byte_lookup.embedding.weight.requires_grad is False
    # decoder 自身参数不许被误冻 (E116 坑的反向钉死)
    assert model.decoder.slot.requires_grad is True
    assert model.decoder.scale.requires_grad is True
    assert all(p.requires_grad for p in model.decoder.blocks.parameters())


# --- 6. step_model 计数列 + 干净水位仪表 --------------------------------------


def test_step_model_denoise_metrics(fake_fuzz):
    model = _model()
    ids = _ids()
    base = dict(
        mask_prob=0.0, mask_span_min=1, mask_span_max=8, mask_mode="byte_span",
        max_chunks=32, max_span=16, task1_loss_weight=1.0, task2_loss_weight=1.0,
        predict_weight=1.0, predict_mode="latent", amp=False,
    )
    # p 全 0: 扰动机构在册但零触发 —— clean_frac=1 且干净行 acc == 混合 direct_acc
    args = SimpleNamespace(**base, **vars(_denoise_args(
        decoder_denoise_p_noise=0.0, decoder_denoise_p_mhat=0.0)))
    loss, metrics = s1.step_model(model, (ids,), args, DEVICE, train=True)
    assert float(metrics["denoise_clean_frac"]) == 1.0
    assert float(metrics["denoise_noise_frac"]) == 0.0
    assert float(metrics["denoise_mhat_frac"]) == 0.0
    assert float(metrics["denoise_grade"]) == -1.0
    assert float(metrics["denoise_direct_clean_acc"]) == float(metrics["direct_acc"])
    # 触发形态: p_noise=1, row_frac=1 → 计数列非零, 干净水位仪表有读数
    args2 = SimpleNamespace(**base, **vars(_denoise_args(
        decoder_denoise_p_noise=1.0, decoder_denoise_p_mhat=0.0, decoder_denoise_row_frac=1.0)))
    s1._DENOISE_GENERATOR.manual_seed(23)
    loss2, metrics2 = s1.step_model(model, (ids,), args2, DEVICE, train=True)
    assert float(metrics2["denoise_noise_frac"]) == 1.0
    assert float(metrics2["denoise_clean_frac"]) == 0.0
    assert float(metrics2["denoise_grade"]) == 0.5  # step 0 仅 s=0.5 轻档
    assert torch.isfinite(loss2)
