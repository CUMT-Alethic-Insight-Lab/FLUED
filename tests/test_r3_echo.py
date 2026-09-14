"""R3 甲臂（恒等自读回声）施工件单测。

任务书：docs/versions/v3.7/FLUED_V3_7_R3_DELTANET_TRANSPLANT_DRAFT_20260914_CN.md
（冻结 v1.0 §2.1/§3）。三件必备测试（施工规格）：
① flag-off 逐位/逐键不变（默认关 = 与 R2 母列逐位不变）；
② 回声门键集白名单 loud-fail（坑 8：strict 加载、白名单外静默过滤=不点火）；
③ g_l 数学语义（g=0 时逐位等于母列）。

mock 替身复刻 fla 0.5.1 ``fla/layers/delta_net.py`` 的调用序（v_conv1d 输出
→ delta rule 核读出 o → o_norm），本地无 fla 全部可测；fla 门控用例在装 fla
的环境上运行（远端 4090 施工靶机跑全量）。
"""

from __future__ import annotations

import json

import pytest
import torch
from torch import nn

import tools.baselines.deltanet_r2.r2_spec as r2spec
import tools.baselines.deltanet_r2.r3_spec as r3

try:
    import fla  # noqa: F401
    _HAS_FLA = True
except ImportError:
    _HAS_FLA = False  # 本地单测环境无 fla：零依赖用例照跑，门控用例跳过（远端跑全量）


# ---------------------------------------------------------------------------
# mock 替身：fla DeltaNet 层调用序（v_conv1d 先于核；o_norm 紧随核后）
# ---------------------------------------------------------------------------


class _VConv(nn.Module):
    """ShortConvolution 替身：可辨识变换（×2），供「捕获的是 conv 输出」断言。"""

    def forward(self, x, **kw):
        return x * 2.0


class _ONorm(nn.Module):
    """RMSNorm 替身：可辨识变换（×3），证明 pre-hook 改的是 o_norm 的输入。"""

    def forward(self, o):
        return o * 3.0


class _Attn(nn.Module):
    """fla DeltaNet 层的调用序替身（不 import fla）：o_core 常数 = 状态读出。"""

    def __init__(self, dim: int = 8):
        super().__init__()
        self.v_proj = nn.Linear(dim, dim, bias=False)
        self.v_conv1d = _VConv()
        self.o_norm = _ONorm()
        self.o_proj = nn.Linear(dim, dim, bias=False)
        self.core_value = 3.0

    def forward(self, x):
        v = self.v_conv1d(self.v_proj(x))  # fla delta_net.py:213-218 对应
        o = torch.full_like(v, self.core_value)  # delta rule 读出替身 :261-270
        o = self.o_norm(o)  # :286 对应（pre-hook 在此注入回声）
        return self.o_proj(o), None, None


class _Block(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.attn = _Attn(dim)


class _MockModel(nn.Module):
    def __init__(self, n_layers: int = 3, dim: int = 8):
        super().__init__()
        self.model = nn.Module()
        self.model.layers = nn.ModuleList([_Block(dim) for _ in range(n_layers)])

    def forward(self, x):
        for lyr in self.model.layers:
            x, _, _ = lyr.attn(x)
        return x


def _echo_params(model) -> dict[str, torch.Tensor]:
    return {k: p for k, p in model.named_parameters()
            if k.split(".")[-1] == r3.ECHO_PARAM_NAME}


# ---------------------------------------------------------------------------
# 0. 参数锚（纯算术）
# ---------------------------------------------------------------------------


def test_param_anchor_echo_constants():
    assert r2spec.EXPECTED_PARAM_COUNT == 48_152_896
    assert r3.ECHO_NUM_PARAMS == r2spec.R2_CONFIG["num_layers"] == 24
    assert r3.EXPECTED_PARAM_COUNT_ECHO == 48_152_920
    assert r3.expected_param_count(False) == 48_152_896
    assert r3.expected_param_count(True) == 48_152_920


def test_echo_gate_keys_whitelist_shape():
    keys = r3.echo_gate_keys()
    assert len(keys) == 24
    assert keys[0] == "model.layers.0.attn.echo_gate"
    assert keys[23] == "model.layers.23.attn.echo_gate"
    assert len(set(keys)) == 24


# ---------------------------------------------------------------------------
# ① flag-off 逐位/逐键不变
# ---------------------------------------------------------------------------


def test_flag_off_no_params_no_hooks_bitwise():
    torch.manual_seed(0)
    plain = _MockModel()
    torch.manual_seed(0)  # 同种子重建（权重逐位同源）
    flagged = _MockModel()
    keys_before = list(flagged.state_dict())
    got = r3.attach_echo(flagged, False)
    assert got == []
    assert list(flagged.state_dict()) == keys_before  # 键集逐键不变
    assert not _echo_params(flagged)
    x = torch.randn(2, 5, 8)
    with torch.no_grad():
        assert torch.equal(plain(x), flagged(x))  # 逐位不变
    # 二次调用仍逐位一致（无 hook 残留、无状态泄漏）
    with torch.no_grad():
        assert torch.equal(plain(x), flagged(x))


def test_flag_on_adds_exactly_whitelist_keys():
    torch.manual_seed(0)
    plain, flagged = _MockModel(), _MockModel()
    n_plain = sum(p.numel() for p in plain.parameters())
    keys = r3.attach_echo(flagged, True)
    assert keys == r3.echo_gate_keys(3)
    assert set(_echo_params(flagged)) == set(keys)
    assert sum(p.numel() for p in flagged.parameters()) == n_plain + 3
    assert all(p.item() == r3.ECHO_GATE_INIT == 1.0 for p in _echo_params(flagged).values())


# ---------------------------------------------------------------------------
# ② 键集白名单 loud-fail（坑 8）
# ---------------------------------------------------------------------------


def test_whitelist_check_missing_key_loudfail():
    keys = {"a", "b"}
    with pytest.raises(RuntimeError, match="坑 8"):
        r3.check_key_whitelist(file_keys={"a"}, model_keys=keys, echo_keys=set())


def test_whitelist_check_extra_key_loudfail():
    with pytest.raises(RuntimeError, match="白名单外多出键"):
        r3.check_key_whitelist(file_keys={"a", "junk"}, model_keys={"a"},
                               echo_keys=set())


def test_whitelist_check_exact_pass():
    rep = r3.check_key_whitelist(
        file_keys={"a", "model.layers.0.attn.echo_gate"},
        model_keys={"a", "model.layers.0.attn.echo_gate"},
        echo_keys={"model.layers.0.attn.echo_gate"})
    assert rep["n_echo_keys"] == 1 and rep["echo_keys"] == ["model.layers.0.attn.echo_gate"]


def _write_sd(tmp_path, sd, name="model.safetensors"):
    from safetensors.torch import save_file
    save_file({k: v.contiguous() for k, v in sd.items()}, str(tmp_path / name))
    return tmp_path


def test_strict_reload_restores_trained_gate_bitexact(tmp_path):
    torch.manual_seed(0)
    src = _MockModel()
    r3.attach_echo(src, True)
    with torch.no_grad():  # 模拟训练后门值漂移
        for p in _echo_params(src).values():
            p.fill_(0.5)
    d = _write_sd(tmp_path, src.state_dict())

    torch.manual_seed(0)
    fresh = _MockModel()  # 未挂接（strict_load_echo 内建 attach，init 1.0 → 被文件覆盖）
    rep = r3.strict_load_echo(fresh, d)
    assert rep["n_echo_keys"] == 3
    for (k_a, v_a), (k_b, v_b) in zip(src.state_dict().items(),
                                      fresh.state_dict().items()):
        assert k_a == k_b and torch.equal(v_a, v_b), k_a  # 逐位一致
    assert all(p.item() == 0.5 for p in _echo_params(fresh).values())


def test_strict_reload_loudfail_missing_echo_key_in_file(tmp_path):
    torch.manual_seed(0)
    model = _MockModel()
    r3.attach_echo(model, True)
    sd = dict(model.state_dict())
    sd.pop("model.layers.1.attn.echo_gate")
    d = _write_sd(tmp_path, sd)
    torch.manual_seed(0)
    victim = _MockModel()  # strict_load_echo 内建 attach 后对文件三分校验
    with pytest.raises(RuntimeError, match="不点火"):
        r3.strict_load_echo(victim, d)


def test_strict_reload_loudfail_junk_key_in_file(tmp_path):
    torch.manual_seed(0)
    model = _MockModel()
    sd = dict(model.state_dict())
    sd["model.layers.0.attn.evil_gate"] = torch.zeros(4)
    d = _write_sd(tmp_path, sd)
    torch.manual_seed(0)
    victim = _MockModel()
    with pytest.raises(RuntimeError, match="不点火"):
        r3.strict_load_echo(victim, d)


def test_strict_reload_loudfail_file_missing_entirely(tmp_path):
    torch.manual_seed(0)
    model = _MockModel()
    r3.attach_echo(model, True)
    with pytest.raises(RuntimeError, match="无权重文件"):
        r3.strict_load_echo(model, tmp_path, attach=False)


def test_flag_off_model_rejects_echo_strict_path(tmp_path):
    torch.manual_seed(0)
    model = _MockModel()  # 未挂回声
    _write_sd(tmp_path, model.state_dict())  # 权重文件在、回声键不在
    with pytest.raises(RuntimeError, match="无回声键"):
        r3.strict_load_echo(model, tmp_path, attach=False)


def test_config_stamp_roundtrip():
    class _Cfg:
        pass

    cfg = _Cfg()
    assert not r3.config_has_echo(cfg)
    r3.stamp_echo_config(cfg, num_layers=24)
    assert r3.config_has_echo(cfg)
    assert cfg.r3_echo["enabled"] is True
    assert cfg.r3_echo["keys"] == r3.echo_gate_keys()
    assert json.loads(json.dumps(cfg.r3_echo))["num_params"] == 24  # json 可落盘
    r3.unstamp_echo_config(cfg)
    assert not r3.config_has_echo(cfg)


# ---------------------------------------------------------------------------
# ③ g_l 数学语义（g=0 逐位等于母列）+ tap 点契约
# ---------------------------------------------------------------------------


def test_echo_add_semantics_g0_bitwise():
    o, v = torch.randn(2, 3, 2, 4), torch.randn(2, 3, 8)
    g = torch.tensor(0.0)
    assert torch.equal(r3.echo_add(o, v, g), o)  # g=0 → 逐位等于母列
    o_nan = o.clone()
    o_nan[0, 0, 0, 0] = float("nan")
    assert torch.isnan(r3.echo_add(o_nan, v, g)[0, 0, 0, 0])  # NaN 直通不被 g=0 洗白（语义如实）


def test_echo_add_semantics_g1_and_reshape():
    o, v = torch.randn(2, 3, 2, 4), torch.randn(2, 3, 8)
    assert torch.equal(r3.echo_add(o, v, torch.tensor(1.0)), o + v.reshape(o.shape))
    g = torch.nn.Parameter(torch.tensor(2.0))
    assert torch.allclose(r3.echo_add(o, v, g), o + 2.0 * v.reshape(o.shape))


def test_echo_add_dtype_promotion_bf16():
    o = torch.randn(2, 3, 2, 4, dtype=torch.bfloat16)
    v = torch.randn(2, 3, 8, dtype=torch.bfloat16)
    g = torch.tensor(1.0, dtype=torch.float32)  # 训练态 fp32 标量门
    out = r3.echo_add(o, v, g)
    assert out.dtype == torch.bfloat16  # 0 维标量不升位（autocast 语义一致）


def test_gate_zero_forward_bitwise_equal_mother_mock():
    torch.manual_seed(0)
    plain = _MockModel()
    torch.manual_seed(0)
    gated = _MockModel()
    r3.attach_echo(gated, True, gate_init=0.0)  # 测试专用：g=0 语义探针
    x = torch.randn(2, 5, 8)
    with torch.no_grad():
        assert torch.equal(plain(x), gated(x))  # g=0 → 逐位等于母列（挂接态）


def test_gate_one_forward_uses_conv_output_not_proj_output():
    """tap 点契约实证：捕获的 v_t = v_conv1d 输出（短卷积后），非 v_proj 原输出。

    v_proj=I（v_proj 输出=层输入 h）、_VConv ×2、o_core=3、o_norm ×3、o_proj=I
    → 每层 h ← 3·(3 + 2h)；若 tap 错到短卷积前则 h ← 3·(3 + 1h)，必然不同。"""
    torch.manual_seed(0)
    m = _MockModel(dim=8)
    with torch.no_grad():
        for lyr in m.model.layers:
            lyr.attn.o_proj.weight.copy_(torch.eye(8))
            lyr.attn.v_proj.weight.copy_(torch.eye(8))
    r3.attach_echo(m, True, gate_init=1.0)
    x = torch.randn(2, 5, 8)
    h_conv, h_pre = x, x
    for _ in range(3):
        h_conv = 3.0 * (3.0 + 2.0 * h_conv)  # tap = conv 输出（正确形态）
        h_pre = 3.0 * (3.0 + 1.0 * h_pre)  # tap = v_proj 原输出（反事实）
    with torch.no_grad():
        assert torch.allclose(m(x), h_conv, atol=1e-5)
        assert not torch.allclose(m(x), h_pre, atol=1e-3)  # tap 点错则必不同


def test_gradient_flows_to_gate():
    torch.manual_seed(0)
    m = _MockModel()
    r3.attach_echo(m, True)
    loss = m(torch.randn(2, 5, 8)).square().sum()
    loss.backward()
    grads = [p.grad for p in _echo_params(m).values()]
    assert all(g is not None and torch.isfinite(g).all() for g in grads)
    assert any(g.abs() > 0 for g in grads)  # 至少部分层门有非零梯度


def test_double_attach_loudfail():
    m = _MockModel()
    r3.attach_echo(m, True)
    with pytest.raises(RuntimeError, match="重复挂接"):
        r3.attach_echo(m, True)


def test_flag_off_after_attach_loudfail():
    m = _MockModel()
    r3.attach_echo(m, True)
    with pytest.raises(RuntimeError, match="回声残留"):
        r3.attach_echo(m, False)


# ---------------------------------------------------------------------------
# fla 门控用例（远端 4090 施工靶机执行全量）
# ---------------------------------------------------------------------------


def _build_model():
    from fla.models.delta_net import DeltaNetConfig, DeltaNetForCausalLM
    return DeltaNetForCausalLM(DeltaNetConfig(**r2spec.R2_CONFIG))


def _same_seed_build(echo: bool, gate_init: float = r3.ECHO_GATE_INIT):
    torch.manual_seed(r2spec.TRAIN_SEED)
    m = _build_model()
    keys = r3.attach_echo(m, echo, gate_init=gate_init)
    if echo:  # 镜像训练器 build_model：回声元数据随 config 落盘
        r3.stamp_echo_config(m.config, num_layers=len(keys))
    return m, keys


_HAS_FLA_CUDA = _HAS_FLA and torch.cuda.is_available()


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（本地跳过，远端跑全量）")
def test_param_anchor_instantiation_both_flags():
    m, keys = _same_seed_build(echo=False)
    assert sum(p.numel() for p in m.parameters()) == 48_152_896
    m2, keys2 = _same_seed_build(echo=True)
    assert sum(p.numel() for p in m2.parameters()) == 48_152_920
    assert keys2 == r3.echo_gate_keys() and keys == []


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（本地跳过，远端跑全量）")
def test_key_diff_two_instantiations_echo_on_identical():
    m1, _ = _same_seed_build(echo=True)
    m2, _ = _same_seed_build(echo=True)
    k1, k2 = list(m1.state_dict()), list(m2.state_dict())
    assert k1 == k2  # 键序列逐键一致
    assert all(m1.state_dict()[k].shape == m2.state_dict()[k].shape for k in k1)
    # echo-on 键集 == R2 母列键集 + 白名单（恰好多 24 键，无任何其他差异）
    torch.manual_seed(r2spec.TRAIN_SEED)
    m0 = _build_model()
    assert set(k1) - set(m0.state_dict()) == set(r3.echo_gate_keys())
    assert set(m0.state_dict()) - set(k1) == set()


@pytest.mark.skipif(not _HAS_FLA_CUDA, reason="fla triton 核需 CUDA（本地跳过，远端 4090 跑全量）")
def test_flag_off_forward_bitwise_vs_pure_fla():
    torch.manual_seed(r2spec.TRAIN_SEED)
    a = _build_model().cuda()
    torch.manual_seed(r2spec.TRAIN_SEED)
    b = _build_model().cuda()
    r3.attach_echo(b, False)  # 旗标关：挂接函数走 no-op 分支
    assert torch.equal(a.state_dict()["model.embeddings.weight"],
                       b.state_dict()["model.embeddings.weight"])
    x = torch.randint(3, 32000, (1, 96), device="cuda")
    with torch.no_grad():
        assert torch.equal(a(input_ids=x).logits, b(input_ids=x).logits)  # 逐位不变


@pytest.mark.skipif(not _HAS_FLA_CUDA, reason="fla triton 核需 CUDA（本地跳过，远端 4090 跑全量）")
def test_gate_zero_forward_bitwise_equal_mother_fla():
    """测试③真机形态：g=0 时逐位等于母列（同 init 同输入同 dtype）。"""
    torch.manual_seed(r2spec.TRAIN_SEED)
    a = _build_model().cuda()
    b, _ = _same_seed_build(echo=True, gate_init=0.0)
    b = b.cuda()
    x = torch.randint(3, 32000, (1, 96), device="cuda")
    with torch.no_grad():
        assert torch.equal(a(input_ids=x).logits, b(input_ids=x).logits)


@pytest.mark.skipif(not _HAS_FLA_CUDA, reason="fla triton 核需 CUDA（本地跳过，远端 4090 跑全量）")
def test_echo_forward_differs_and_gate_grads_finite():
    a, _ = _same_seed_build(echo=False)
    a = a.cuda()
    b, _ = _same_seed_build(echo=True, gate_init=1.0)
    b = b.cuda()
    x = torch.randint(3, 32000, (1, 96), device="cuda")
    la = a(input_ids=x).logits.float().square().sum()
    lb = b(input_ids=x).logits
    assert not torch.equal(la.detach(), lb.detach())  # 回声确实改变前向
    lb.float().square().sum().backward()
    grads = [p.grad for k, p in b.named_parameters()
             if k.split(".")[-1] == r3.ECHO_PARAM_NAME]
    assert len(grads) == 24
    assert all(g is not None and torch.isfinite(g).all() for g in grads)


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（本地跳过，远端跑全量）")
def test_save_roundtrip_strict_reload_bitexact(tmp_path):
    """坑 8 全链：save 带 echo 键 → from_pretrained 静默丢弃（事故形态复现）
    → attach+strict 白名单重载逐位复原 + config 字段往返。"""
    from transformers import AutoModelForCausalLM
    r2spec.normalize_tied_weights_keys()
    m, _ = _same_seed_build(echo=True)
    with torch.no_grad():  # 模拟训练后门值 ≠ init
        for k, p in m.named_parameters():
            if k.split(".")[-1] == r3.ECHO_PARAM_NAME:
                p.fill_(0.75)
    d = tmp_path / "echo_ckpt"
    m.save_pretrained(d)
    cfg = json.loads((d / "config.json").read_text(encoding="utf-8"))
    assert cfg["r3_echo"]["enabled"] is True  # 回声元数据随 config 落盘
    sd_file = r3.read_state_dict(d)
    assert set(r3.echo_gate_keys()) <= set(sd_file)

    loaded = AutoModelForCausalLM.from_pretrained(d)
    assert r3.config_has_echo(loaded.config)
    assert not any(k.split(".")[-1] == r3.ECHO_PARAM_NAME
                   for k in loaded.state_dict())  # 坑 8 事故形态：静默丢弃实证

    r3.attach_and_strict_reload(loaded, d)
    src_sd, got_sd = m.state_dict(), loaded.state_dict()
    assert set(src_sd) == set(got_sd)
    for k in r3.echo_gate_keys():
        assert torch.equal(src_sd[k], got_sd[k].to(src_sd[k].dtype)), k  # 门值逐位复原
        assert float(got_sd[k]) == 0.75
