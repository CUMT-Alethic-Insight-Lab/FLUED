"""R3 甲臂（对角护栏移植 = 恒等自读回声）冻结规格单源。

任务书：docs/versions/v3.7/FLUED_V3_7_R3_DELTANET_TRANSPLANT_DRAFT_20260914_CN.md
（冻结 v1.0，2026-09-14 用户终审签发；甲臂先行施工，前置门六件回执齐了点火）。
回执：outputs/r3_transplant_echo_20260914/R3_ECHO_RECEIPT_20260914.md。

构造（任务书 §2.1 主构造，逐字执行）：DeltaNet-50M 全部 24 层，每层状态读出处
加恒通旁路 ``o_t ← o_t + g_l · v_t``：
- ``v_t`` = 该层 v 投影输出，tap 点 = fla 0.5.1 ``fla/layers/delta_net.py`` 的
  ``v_conv1d`` 输出（line 213-218，use_short_conv 之后；β 门控由 ``b_proj``
  （line 240-241）产出、在 delta rule 核内（line 261-270 chunk / 250-259
  fused_recurrent）作用于写入——v 在 β 门控之前。tap 点经用户终审确认，不引入
  第二条旁路）；
- ``o_t`` = 状态读出，= delta rule 核返回的 o（line 261-270），``o_norm``
  （line 286）之前——o_norm/o_proj 是输出接口适配，不属于状态读取；
- ``g_l`` = 逐层可学标量门，init 1.0（通道从第 0 步起全强度可用 = 护栏结构
  先在性；可学衰减对应 FLUED 对角 softmax 权重的可学性）。全臂新增参数 = 24 个
  标量（每层 1 个），除此之外任何权重零新增、零改动。

施工形态（最小侵入）：零 fla 代码复制——``v_conv1d`` 挂 forward hook 捕获 v_t，
``o_norm`` 挂 forward pre-hook 做加法；旗标默认关 = 不挂任何 hook、不建任何
参数，模型与 R2 母列逐位不变（同种子同数据序下 loss 轨迹逐位一致为验收）。

坑 8 纪律：加载/初始化只走 strict 系 + 全键 loud-fail + 键集白名单
（= ``model.layers.{i}.attn.echo_gate``，i ∈ [0, 24)）；白名单外键被静默过滤
= 不点火。回声元数据随 config.json 字段 ``r3_echo`` 落盘（fla DeltaNetConfig
收 **kwargs，字段往返实测无损）；装载侧发现该字段即要求 strict 白名单重载。

超参/窗语义/种子纪律全部沿用 ``r2_spec.py``（本文件不复制任何数值锚，
R2 冻结文件不动）。
"""

from __future__ import annotations

import json
from pathlib import Path

import torch
from torch import nn

import tools.baselines.deltanet_r2.r2_spec as r2spec

# ---------------------------------------------------------------------------
# 回声件参数锚（任务书 §2.1：全臂新增 = 24 个标量，其余零新增零改动）
# ---------------------------------------------------------------------------

ECHO_GATE_INIT = 1.0
ECHO_PARAM_NAME = "echo_gate"
ECHO_CONFIG_FIELD = "r3_echo"

# tap 契约（fla 0.5.1 DeltaNet 层结构 loud-fail 检查项；结构漂移即停报）
_TAP_REQUIRED_ATTRS = ("v_conv1d", "o_norm", "o_proj")
_TAP_FORBIDDEN_ATTRS = ("g_proj",)  # use_gate=True 分支不在本 tap 契约内

# 参数锚：基座 48,152,896 + 每层 1 标量 × num_layers(24) = 48,152,920
ECHO_NUM_PARAMS = r2spec.R2_CONFIG["num_layers"]
EXPECTED_PARAM_COUNT_ECHO = r2spec.EXPECTED_PARAM_COUNT + ECHO_NUM_PARAMS


def echo_gate_keys(num_layers: int = ECHO_NUM_PARAMS) -> list[str]:
    """键集白名单（全臂新增键的穷举；白名单外新增键 = 坑 8 loud-fail）。"""
    return [f"model.layers.{i}.attn.{ECHO_PARAM_NAME}" for i in range(num_layers)]


def expected_param_count(echo: bool) -> int:
    return EXPECTED_PARAM_COUNT_ECHO if echo else r2spec.EXPECTED_PARAM_COUNT


# ---------------------------------------------------------------------------
# 回声数学语义（纯函数，单测③锚点）
# ---------------------------------------------------------------------------


def echo_add(o: torch.Tensor, v: torch.Tensor, g: torch.Tensor) -> torch.Tensor:
    """恒等自读回声：o_t ← o_t + g_l · v_t。

    o: 状态读出 (B, T, H, D)；v: v 投影输出 (B, T, H·D)（reshape 到 o 的形状，
    expand_v=1.0 下 value_dim = H·D 逐位对应）；g: 0 维标量门。g=0 时逐位等于
    o（有限值域）；dtype 遵循 PyTorch 提升（0 维标量 × 维度张量同行别不升位，
    autocast bf16 下加法保持 bf16）。"""
    if v.shape != o.shape:
        v = v.reshape(o.shape)
    return o + g * v


# ---------------------------------------------------------------------------
# tap 契约核验与挂接
# ---------------------------------------------------------------------------


def _echo_attn_layers(model: nn.Module) -> list[nn.Module]:
    """按结构契约取出 24 个 DeltaNet 层的 attn 模块（duck-type，不 import fla
    ——本地无 fla 环境可测；真实结构由 tap 契约检查 loud-fail 兜底）。"""
    base = getattr(model, "model", model)
    layers = getattr(base, "layers", None)
    if layers is None:
        raise RuntimeError("[r3] tap 契约不符：model.model.layers 不存在（非 fla "
                           "DeltaNetForCausalLM 结构？）——停报")
    attns = []
    for i, lyr in enumerate(layers):
        attn = getattr(lyr, "attn", None)
        missing = [a for a in _TAP_REQUIRED_ATTRS if not hasattr(attn, a)]
        if attn is None or missing:
            raise RuntimeError(
                f"[r3] tap 契约不符 @layer {i}: 缺 {missing}（fla 层结构漂移？）——停报")
        forbidden = [a for a in _TAP_FORBIDDEN_ATTRS if hasattr(attn, a)]
        if forbidden:
            raise RuntimeError(
                f"[r3] tap 契约不符 @layer {i}: 出现 {forbidden}（use_gate=True 分支"
                "不在本 tap 契约内）——停报")
        attns.append(attn)
    return attns


def _model_echo_keys(model: nn.Module) -> list[str]:
    return [k for k, _ in model.named_parameters()
            if k.split(".")[-1] == ECHO_PARAM_NAME]


def attach_echo(model: nn.Module, enabled: bool,
                gate_init: float = ECHO_GATE_INIT) -> list[str]:
    """旗标化挂接。enabled=False：核验无回声残留、不挂任何东西，返回 []
    （= 与 R2 母列逐位不变路径）。enabled=True：逐层挂 g_l + hook 对，返回
    新增键表（须与 echo_gate_keys() 逐键一致，否则 loud fail）。"""
    if not enabled:
        leftover = _model_echo_keys(model)
        if leftover:
            raise RuntimeError(f"[r3] flag-off 但发现回声残留键 {leftover}——停报")
        return []

    attns = _echo_attn_layers(model)
    for i, attn in enumerate(attns):
        if hasattr(attn, ECHO_PARAM_NAME):
            raise RuntimeError(f"[r3] layer {i} 已有 {ECHO_PARAM_NAME}（重复挂接？）——停报")
        ref = attn.o_proj.weight
        attn.echo_gate = nn.Parameter(
            torch.full((), float(gate_init), dtype=ref.dtype, device=ref.device))

        def _v_hook(_mod, _inp, output, _attn=attn):
            # fla 0.5.1 ShortConvolution.forward 恒返回 (x, final_state) 元组
            # （层内 `v, conv_state_v = self.v_conv1d(...)` 双值解包，delta_net.py:213-218）
            v = output[0] if isinstance(output, tuple) else output
            _attn._r3_echo_v = v  # v_t：use_short_conv 之后、β 门控之前
            return output

        def _o_pre_hook(_mod, args, _attn=attn):
            o = args[0]
            return (echo_add(o, _attn._r3_echo_v, _attn.echo_gate),)

        attn._r3_echo_hooks = [
            attn.v_conv1d.register_forward_hook(_v_hook),
            attn.o_norm.register_forward_pre_hook(_o_pre_hook),
        ]

    got = sorted(_model_echo_keys(model))
    want = sorted(echo_gate_keys(len(attns)))
    if got != want:
        raise RuntimeError(f"[r3] 回声键集与白名单不符：\n  got={got}\n  want={want}")
    return echo_gate_keys(len(attns))  # canonical 数值序（sorted 只用于集合校验）


# ---------------------------------------------------------------------------
# config 元数据（回声旗标随 checkpoint 落盘；fla DeltaNetConfig 收 **kwargs）
# ---------------------------------------------------------------------------


def stamp_echo_config(config, num_layers: int = ECHO_NUM_PARAMS) -> None:
    config.r3_echo = {
        "enabled": True,
        "gate_init": ECHO_GATE_INIT,
        "param_name": ECHO_PARAM_NAME,
        "num_params": num_layers,
        "tap": "v_conv1d output (post short-conv, pre beta) -> add before o_norm",
        "spec": "tools/baselines/deltanet_r2/r3_spec.py",
        "keys": echo_gate_keys(num_layers),
    }


def config_has_echo(config) -> bool:
    flag = getattr(config, ECHO_CONFIG_FIELD, None)
    return bool(flag and flag.get("enabled"))


def unstamp_echo_config(config) -> None:
    if getattr(config, ECHO_CONFIG_FIELD, None) is not None:
        delattr(config, ECHO_CONFIG_FIELD)


# ---------------------------------------------------------------------------
# 坑 8：strict 系加载 + 键集白名单 loud-fail
# ---------------------------------------------------------------------------


def check_key_whitelist(file_keys, model_keys, echo_keys) -> dict:
    """键集三分校验（纯集合逻辑，单测②锚点）：缺失/多出/白名单契合任一破即
    RuntimeError 响亮——白名单外键被静默过滤 = 不点火。"""
    f, m, w = set(file_keys), set(model_keys), set(echo_keys)
    missing = sorted(m - f)
    unexpected = sorted(f - m)
    absent_echo = sorted(w - f)
    if missing or unexpected or absent_echo:
        raise RuntimeError(
            "[r3] 坑 8 loud-fail（回声 strict 白名单校验）——"
            f"缺失键 {missing[:8]}{'…' if len(missing) > 8 else ''} / "
            f"白名单外多出键 {unexpected[:8]}{'…' if len(unexpected) > 8 else ''} / "
            f"白名单缺席 {absent_echo[:8]}{'…' if len(absent_echo) > 8 else ''} ——不点火")
    return {"n_file_keys": len(f), "n_model_keys": len(m), "n_echo_keys": len(w),
            "echo_keys": sorted(w)}


def read_state_dict(model_dir: str | Path) -> dict[str, torch.Tensor]:
    """checkpoint 目录 → 全量 state dict（safetensors 单文件/分片，或 .bin）。"""
    d = Path(model_dir)
    idx = d / "model.safetensors.index.json"
    sd: dict[str, torch.Tensor] = {}
    if idx.exists():
        shards = sorted(set(json.loads(idx.read_text(encoding="utf-8"))["weight_map"].values()))
        from safetensors.torch import load_file
        for s in shards:
            sd.update(load_file(str(d / s)))
    elif (d / "model.safetensors").exists():
        from safetensors.torch import load_file
        sd = load_file(str(d / "model.safetensors"))
    elif (d / "pytorch_model.bin").exists():
        sd = torch.load(d / "pytorch_model.bin", map_location="cpu", weights_only=True)
    else:
        raise RuntimeError(f"[r3] {d} 无权重文件（model.safetensors/index/bin 皆缺）——停报")
    return sd


def strict_load_echo(model: nn.Module, model_dir: str | Path,
                     attach: bool = True) -> dict:
    """回声 checkpoint 的唯一合法装载路径：attach（键集=白名单）→ 全量文件
    state dict 三分校验 → ``load_state_dict(strict=True)`` 逐键重载。

    回声键从已挂接模型自身派生（attach_echo 已对白名单穷举 loud-fail），故本
    函数对真实 24 层与单测 mock 同一条路径。文件侧新增键必须与回声键**集合
    全等**——任何白名单外键出现即响亮（坑 8：静默过滤=不点火）。

    背景（坑 8 事故形态）：echo 键对 AutoModelForCausalLM.from_pretrained 是
    unexpected key，默认加载路径会**静默丢弃**——装载后必须以文件全量 state dict
    strict 重载，门值才与训练终态逐位一致。"""
    if attach:
        attach_echo(model, True)
    sd = read_state_dict(model_dir)
    model_keys = set(model.state_dict())
    echo_keys = {k for k in model_keys if k.split(".")[-1] == ECHO_PARAM_NAME}
    if not echo_keys:
        raise RuntimeError("[r3] 模型无回声键却走 strict_load_echo（旗标/路径错配）——停报")
    base_keys = model_keys - echo_keys
    extra_in_file = sd.keys() - base_keys
    if extra_in_file != echo_keys:
        raise RuntimeError(
            f"[r3] 文件新增键 ≠ 回声白名单：file-only={sorted(extra_in_file)[:8]}… "
            f"echo={sorted(echo_keys)[:8]}… ——不点火")
    report = check_key_whitelist(sd.keys(), model_keys, echo_keys)
    model.load_state_dict(sd, strict=True)
    return report


def attach_and_strict_reload(model: nn.Module, model_dir: str | Path) -> dict:
    """评测侧装载器（仪器启动器调用）：from_pretrained 装出的模型接回声 +
    strict 白名单重载，返回报告（进仪器 fingerprint 留档）。"""
    report = strict_load_echo(model, model_dir, attach=True)
    report["spec"] = "tools/baselines/deltanet_r2/r3_spec.py"
    report["gate_init"] = ECHO_GATE_INIT
    return report
