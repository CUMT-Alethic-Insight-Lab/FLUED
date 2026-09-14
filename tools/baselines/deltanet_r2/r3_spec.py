"""R3 移植臂冻结规格单源（甲=对角护栏/恒等自读回声，乙=summarizer 双头构造，
丙=S0'' 段界器/c1 变长铺瓦）。

任务书：docs/versions/v3.7/FLUED_V3_7_R3_DELTANET_TRANSPLANT_DRAFT_20260914_CN.md
（冻结 v1.0，2026-09-14 用户终审签发；前置门六件回执齐了点火）。
甲臂回执：outputs/r3_transplant_echo_20260914/R3_ECHO_RECEIPT_20260914.md。
乙臂回执：outputs/r3_transplant_summ_20260914/R3_SUMM_RECEIPT_20260914.md。
丙臂施工（2026-09-14，本地 5080 承载；§9.6 承载机开口项对丙臂修订，用户指令）。

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


# ===========================================================================
# 乙节：summarizer 双头构造移植（任务书 §2.2 主构造，冻结 v1.0 逐字执行）
#
# 构造（单点摘要+双头全接）：
#   ① embedding 后、层栈前，对每个原生 64-token 块（=fla wy_fast.py:226 BT=64
#     原生铺瓦，r2_spec.NATIVE_CHUNK_TOKENS）的 span 特征过**共享参数**
#     summarizer，产出 m_c（memory 头）与 k_c（index 头）；
#   ② 值侧：全部 24 层每层 v_t ← m_c（所属块摘要替换原生 v 投影输出；q/k/β
#     原生保留——fla 0.5.1 中 β 由 b_proj(hidden_states) 产出、与 v 无关，
#     delta_net.py:251 实证）；
#   ③ 地址侧：块内 64 位置写址方向 k_t ← k_c 广播（读侧 q_t 原生）。
#
# 构造同构：直接 import 原件 ``flued.v36.model.DiTChunkSummarizer``（model.py:
# 391-475，canonical_v37 形态 type=dit/dit_layers=2/pool=qpool 4 位置锚定查询
# temp 16.0/backbone_mode=slm 创建 index_ffn 双头）——零重实现，参数化到宿主
# 320 维（输入域适配；byte encoder 不入件，件边界=池化+双头构造组）。
# tap 点：fla 0.5.1 ``delta_net.py:213-218`` k_conv1d/v_conv1d 的输出（proj 后
# 短卷积后、delta rule 核前；核内 use_qk_l2norm_in_kernel 对 k 的 L2 属宿主
# 原生写址处理，k_c 同受）。由 forward hook 替换输出（元组首元，ShortConvolution
# 恒返回 (x, final_state)）；旗标默认关 = 不挂任何 hook、不建任何参数，与 R2
# 母列逐位不变。
#
# 坑 8 纪律：新增参数全部在 ``model.r3_summ`` 模块内（键前缀
# ``model.r3_summ.*``）；加载/初始化只走 strict 系 + 全键 loud-fail + 键集
# 白名单（=模块自身 named_parameters 穷举）。元数据随 config.json 字段
# ``r3_summ`` 落盘；装载侧发现该字段即要求 strict 白名单重载。
#
# 边界注记：k/v tap 在 use_cache（生成/增量解码）路径下 conv_state 语义不保
# （替换值不经短卷积状态机）——本臂只支持全窗前向（训练与判决仪器均是），
# 生成路径不支持，如实登记。
# ===========================================================================

SUMM_CONFIG_FIELD = "r3_summ"
SUMM_ATTR = "r3_summ"  # 挂内层 model 的属性名 → 参数键前缀 model.r3_summ.*
SUMM_CHUNK_TOKENS = r2spec.NATIVE_CHUNK_TOKENS  # 64（宿主原生铺瓦粒度）

# 构造冻结常量（§2.2；宽度=宿主适配裁定，施工精算见 summ_param_count_analytic
# 与回执 §0.4：任务书钉死 d=320/heads=5/ffn 768；双头 FFN 隐宽取 768=宿主
# intermediate_size 同宽——原件 summarizer_hidden=1024 是 d_byte=384 体制的
# 内宽，随输入域 384→320 适配一并宿主化；qpool 4 锚查询 temp 16.0 原件常量
# 原值保留（DiTChunkSummarizer 类常量，测试核验）；d_mem=320=m_c/k_c 接头宽
# =宿主 v/k 投影宽（expand_v=expand_k=1.0））
SUMM_DIT_LAYERS = 2
SUMM_D = 320
SUMM_HEADS = 5
SUMM_FFN_DIM = 768
SUMM_HIDDEN = 768
SUMM_D_MEM = 320
SUMM_POOL_MODE = "qpool"

# tap 契约（fla 0.5.1 DeltaNet 层结构 loud-fail 检查项；结构漂移即停报）
_SUMM_TAP_REQUIRED = ("q_proj", "k_proj", "v_proj", "b_proj",
                      "q_conv1d", "k_conv1d", "v_conv1d")
_SUMM_TAP_FORBIDDEN = ("g_proj",)  # use_gate=True 分支不在本 tap 契约内


def _summ_cfg():
    """原件 DiTChunkSummarizer 的配置投影（canonical_v37 summarizer 形态 +
    宿主 320 维适配；SimpleNamespace 只供给 __init__ 实读的字段）。"""
    from types import SimpleNamespace
    return SimpleNamespace(
        d_byte=SUMM_D, nhead=SUMM_HEADS, ffn_dim=SUMM_FFN_DIM,
        summarizer_dit_layers=SUMM_DIT_LAYERS, summarizer_pool=SUMM_POOL_MODE,
        summarizer_hidden=SUMM_HIDDEN, d_mem=SUMM_D_MEM,
        backbone_mode="slm")  # slm → index_ffn 双头创建（v3.7 consensus §1.1）


def summ_param_count_analytic() -> int:
    """新增参数解析式精算（与 DiTChunkSummarizer(320,5,768,qpool,hidden=768,
    d_mem=320) 实例化互证；任务书 §2.2「≈2–3M 待施工精算」的精算=4,972,932
    ≈+10.3%，高于起草估计——混杂④参数量如实升级登记，归因由判死后自动触发
    的参数匹配对照列承接）。"""
    d, f, hid, dm = SUMM_D, SUMM_FFN_DIM, SUMM_HIDDEN, SUMM_D_MEM
    qn = 4  # QPOOL_QUERIES（build_summarizer 内对类常量 loud-fail 核验）
    block = (
        2 * d                    # norm1 (LN weight+bias)
        + d * 3 * d + d * d      # attn.qkv / attn.out（均无 bias）
        + 2 * d                  # norm2
        + d * 2 * f + 2 * f      # ff_in（含 bias）
        + f * d + d              # ff_out（含 bias）
        + d + d + d * d + d      # noise_cond.0 / noise_cond.2（含 bias）
        + 2                      # attn_scale / ff_scale
    )
    pw = d * qn                  # pool_width = qpool 拼接宽 1280
    head_ffn = (
        2 * pw                   # LayerNorm(pool_width)
        + pw * hid + hid         # Linear(pool_width, hidden)（含 bias）
        + hid * dm + dm          # Linear(hidden, d_mem)（含 bias）
    )
    return SUMM_DIT_LAYERS * block + qn * d + 2 * head_ffn


SUMM_NUM_PARAMS = summ_param_count_analytic()
EXPECTED_PARAM_COUNT_SUMM = r2spec.EXPECTED_PARAM_COUNT + SUMM_NUM_PARAMS


def expected_param_count_any(echo: bool, summ: bool) -> int:
    """参数锚三档/四档 loud-fail 用（--echo 与 --summ 训练器层互斥，本函数
    只为锚表达式统一；echo∧summ 组合不被任何合法路径调用）。"""
    n = r2spec.EXPECTED_PARAM_COUNT
    if echo:
        n += ECHO_NUM_PARAMS
    if summ:
        n += SUMM_NUM_PARAMS
    return n


def broadcast_per_chunk(pc: torch.Tensor, ref: torch.Tensor) -> torch.Tensor:
    """块内广播（值侧/地址侧共享形态，纯函数单测锚点）：
    pc: (B, C, D) 每块一个向量；ref: (B, T, D) 位置参照张量。
    返回 out (B, T, D)，out[b, t] = pc[b, t // SUMM_CHUNK_TOKENS]（逐位拷贝，
    非 Value 强插值；尾块不足 64 位置只影响 summarizer 侧 masking，广播侧
    t//64 映射恒在界内）。"""
    if pc.dim() != 3 or ref.dim() != 3 or pc.size(0) != ref.size(0) \
            or pc.size(2) != ref.size(2):
        raise RuntimeError(f"[r3] broadcast_per_chunk 形状不符：pc={tuple(pc.shape)} "
                           f"ref={tuple(ref.shape)}（停报）")
    t = ref.size(1)
    idx = torch.div(torch.arange(t, device=ref.device), SUMM_CHUNK_TOKENS,
                    rounding_mode="floor")
    out = pc.index_select(1, idx)
    if out.shape != ref.shape:
        raise RuntimeError(f"[r3] broadcast 广播后形状 {tuple(out.shape)} ≠ "
                           f"{tuple(ref.shape)}（C 与 T/64 不齐？停报）")
    return out


def _summ_tap_contract(model: nn.Module) -> nn.Module:
    """fla 0.5.1 结构契约核验（duck-type，真实结构漂移即停报）。"""
    base = getattr(model, "model", model)
    layers = getattr(base, "layers", None)
    emb = getattr(base, "embeddings", None)
    if layers is None or emb is None:
        raise RuntimeError("[r3] tap 契约不符：model.{embeddings,layers} 不存在"
                           "（非 fla DeltaNetForCausalLM 结构？）——停报")
    for i, lyr in enumerate(layers):
        attn = getattr(lyr, "attn", None)
        missing = [a for a in _SUMM_TAP_REQUIRED if attn is None or not hasattr(attn, a)]
        if attn is None or missing:
            raise RuntimeError(
                f"[r3] tap 契约不符 @layer {i}: 缺 {missing}（fla 层结构漂移？）——停报")
        forbidden = [a for a in _SUMM_TAP_FORBIDDEN if hasattr(attn, a)]
        if forbidden:
            raise RuntimeError(
                f"[r3] tap 契约不符 @layer {i}: 出现 {forbidden}（use_gate=True 分支"
                "不在本 tap 契约内）——停报")
    return base


# ---------------------------------------------------------------------------
# 去消融/对照件（§4 杀死档自动触发，2026-09-14 用户终审裁定）：
#   side 变体（乙-v2 仅值侧 / 乙-v3 仅地址侧）= 模块整体在场（参数锚不变），
#     只摘除另一头的 tap hook——头级归因（哪头的接线是凶手）；
#   ctrl（参数匹配对照列）= 同参数量同 tap 点、构造最简化的 pseudo 双头
#     （masked mean 池化 + LN + 双 MLP，无 DiT/qpool/双头 FFN 构造）——归因
#     「构造毒性 vs 参数量」。
# ---------------------------------------------------------------------------

PSEUDO_HIDDEN = 3878
PSEUDO_PAD = 56  # 零函数注册垫（1282*3878+1280=4,972,876，+56 精确匹配锚）


class PseudoDualHeadMLP(nn.Module):
    """参数匹配对照构造（归因「构造毒性 vs 参数量」）：与主构造同 tap 点同
    广播机制，summarizer 内部换成最简形态——masked mean 池化（v37.2 前旧
    口径池化，无可学查询）+ LN + 双 MLP 头。参数 = 1282×3878+1280+56(pad)
    = 4,972,932 与主构造精确匹配；pad 为零函数注册参数（不在前向图上、
    无梯度，AdamW 不更新——如实登记）。"""

    def __init__(self) -> None:
        super().__init__()
        self.pad = nn.Parameter(torch.zeros(PSEUDO_PAD))
        self.norm = nn.LayerNorm(SUMM_D)
        self.head_m = nn.Sequential(
            nn.Linear(SUMM_D, PSEUDO_HIDDEN), nn.SiLU(),
            nn.Linear(PSEUDO_HIDDEN, SUMM_D_MEM))
        self.head_k = nn.Sequential(
            nn.Linear(SUMM_D, PSEUDO_HIDDEN), nn.SiLU(),
            nn.Linear(PSEUDO_HIDDEN, SUMM_D_MEM))

    def forward_with_index(self, spans: torch.Tensor,
                           token_mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        bsz, chunks, span, dim = spans.shape
        valid = token_mask.reshape(bsz * chunks, span)
        h = spans.reshape(bsz * chunks, span, dim)
        denom = valid.sum(dim=1, keepdim=False).clamp(min=1).unsqueeze(-1).to(h.dtype)
        pooled = (h * valid.unsqueeze(-1).to(h.dtype)).sum(dim=1) / denom  # (B*C, d)
        memory = self.head_m(self.norm(pooled)).view(bsz, chunks, -1)
        index = self.head_k(self.norm(pooled)).view(bsz, chunks, -1)
        return memory, index


def build_summarizer(ctrl: bool = False):
    """构造选择：ctrl=False = 原件 DiTChunkSummarizer 零重实现（init 纪律随
    原件）；ctrl=True = 参数匹配 pseudo 双头。两者参数锚一致（53,125,828 = 基
    座 + SUMM_NUM_PARAMS）。"""
    if ctrl:
        pseudo = PseudoDualHeadMLP()
        n = sum(p.numel() for p in pseudo.parameters())
        if n != SUMM_NUM_PARAMS:
            raise RuntimeError(f"[r3] pseudo 参数 {n:,} ≠ 主构造锚 "
                               f"{SUMM_NUM_PARAMS:,}（参数匹配破坏）——停报")
        return pseudo
    from flued.v36.model import DiTChunkSummarizer
    summ = DiTChunkSummarizer(_summ_cfg())
    if not hasattr(summ, "index_ffn"):
        raise RuntimeError("[r3] summarizer 无 index_ffn（backbone_mode≠slm？）"
                           "——双头构造缺一头，停报")
    if (summ.QPOOL_QUERIES, summ.QPOOL_ANCHOR_TEMP) != (4, 16.0):
        raise RuntimeError("[r3] qpool 构造常量漂移（≠4 锚查询/temp 16.0）——停报")
    return summ


def _summ_param_keys(model: nn.Module) -> list[str]:
    return [k for k, _ in model.named_parameters()
            if f".{SUMM_ATTR}." in f".{k}"]


def attach_summ(model: nn.Module, enabled: bool, side: str = "both",
                ctrl: bool = False) -> list[str]:
    """旗标化挂接（§2.2 主构造 + §4 触发变体）。enabled=False：核验无
    summarizer 残留、不挂任何东西，返回 []（= 与 R2 母列逐位不变路径）。
    enabled=True：建 ``model.r3_summ`` 模块 + embedding 汇总 hook + tap 替换
    hook，返回新增键表（=模块 named_parameters 穷举，白名单本体）。
    side：both=双头全接（主构造）；value=仅值侧（乙-v2）；addr=仅地址侧
    （乙-v3）——模块整体在场参数锚不变，只摘除另一头 tap（头级归因）。
    ctrl：True=参数匹配 pseudo 双头（对照列，构造最简化）。"""
    if side not in ("both", "value", "addr"):
        raise RuntimeError(f"[r3] side={side!r} 非法（both|value|addr）——停报")
    if not enabled:
        base = getattr(model, "model", model)
        if getattr(base, SUMM_ATTR, None) is not None:
            raise RuntimeError(f"[r3] flag-off 但发现 {SUMM_ATTR} 残留模块——停报")
        if _summ_param_keys(model):
            raise RuntimeError(f"[r3] flag-off 但发现 summarizer 残留键 "
                               f"{_summ_param_keys(model)[:4]}…——停报")
        return []

    base = _summ_tap_contract(model)
    if hasattr(base, SUMM_ATTR):
        raise RuntimeError(f"[r3] 重复挂接：base.{SUMM_ATTR} 已存在——停报")
    summ = build_summarizer(ctrl=ctrl)
    ref = next(model.parameters())  # 对齐宿主当前 device/dtype：训练器路径（fp32
    # CPU 挂接、后随 model.to 迁移）与仪器路径（bf16 CUDA 已就位后 strict 重载）
    # 两条装载序都成立
    summ.to(device=ref.device, dtype=ref.dtype)
    base.r3_summ = summ  # 注册为子模块：model.to(device) 随全局迁移
    ctx: dict = {}

    def _embed_hook(_m, _inp, out):
        h = out  # (B, T, D) embedding 输出（层栈前 span 特征）
        bsz, t_len, dim = h.shape
        ch = SUMM_CHUNK_TOKENS
        n_chunk = (t_len + ch - 1) // ch
        pad = n_chunk * ch - t_len
        hp = torch.nn.functional.pad(h, (0, 0, 0, pad)) if pad else h
        spans = hp.reshape(bsz, n_chunk, ch, dim)
        valid = torch.ones(bsz, n_chunk, ch, dtype=torch.bool, device=h.device)
        if pad:
            valid[:, -1, ch - pad:] = False  # 尾块不足 64 位置（训练窗 2047 常态）
        m_c, k_c = summ.forward_with_index(spans, valid)
        ctx["m_c"], ctx["k_c"] = m_c, k_c
        return out

    def _replace_hook(which: str):
        def _hook(_mod, _inp, out):
            x = out[0] if isinstance(out, tuple) else out  # ShortConvolution
            pc = ctx.get(which)
            if pc is None:
                raise RuntimeError("[r3] k/v 替换 hook 先于 embedding 汇总 hook "
                                   "触发（hook 序漂移？）——停报")
            new = broadcast_per_chunk(pc, x).to(x.dtype)
            return (new, out[1]) if isinstance(out, tuple) else new
        return _hook

    hooks = [base.embeddings.register_forward_hook(_embed_hook)]
    for lyr in base.layers:
        attn = lyr.attn
        if side in ("both", "addr"):  # 地址侧：k_t ← k_c 块内广播
            hooks.append(attn.k_conv1d.register_forward_hook(_replace_hook("k_c")))
        if side in ("both", "value"):  # 值侧：v_t ← m_c 块内广播
            hooks.append(attn.v_conv1d.register_forward_hook(_replace_hook("m_c")))
    base._r3_summ_hooks = hooks

    got = _summ_param_keys(model)
    if not got:
        raise RuntimeError("[r3] 挂接后未发现 summarizer 参数——停报")
    return got  # = 白名单本体（model.r3_summ.* 穷举）


# ---------------------------------------------------------------------------
# config 元数据（summarizer 旗标随 checkpoint 落盘；fla DeltaNetConfig 收 **kwargs）
# ---------------------------------------------------------------------------


def stamp_summ_config(config, side: str = "both", ctrl: bool = False) -> None:
    config.r3_summ = {
        "enabled": True,
        "construction": ("param-matched pseudo dual-head (mean-pool + dual MLP)"
                         if ctrl else
                         "single-point summary + dual-head full wiring"),
        "side": side, "ctrl": ctrl,
        "dit_layers": SUMM_DIT_LAYERS, "d": SUMM_D, "heads": SUMM_HEADS,
        "ffn_dim": SUMM_FFN_DIM, "hidden": SUMM_HIDDEN, "d_mem": SUMM_D_MEM,
        "pool": SUMM_POOL_MODE, "chunk_tokens": SUMM_CHUNK_TOKENS,
        "num_params": SUMM_NUM_PARAMS,
        "tap": "k_conv1d/v_conv1d output (post proj+short-conv, pre delta-rule core)",
        "spec": "tools/baselines/deltanet_r2/r3_spec.py",
    }


def config_has_summ(config) -> bool:
    flag = getattr(config, SUMM_CONFIG_FIELD, None)
    return bool(flag and flag.get("enabled"))


def unstamp_summ_config(config) -> None:
    if getattr(config, SUMM_CONFIG_FIELD, None) is not None:
        delattr(config, SUMM_CONFIG_FIELD)


# ---------------------------------------------------------------------------
# 坑 8：strict 系加载 + 键集白名单 loud-fail（集合逻辑复用甲臂
# check_key_whitelist / read_state_dict，键名无关）
# ---------------------------------------------------------------------------


def strict_load_summ(model: nn.Module, model_dir: str | Path,
                     attach: bool = True, ctrl: bool = False) -> dict:
    """summarizer checkpoint 的唯一合法装载路径：attach（模块+hook+白名单；
    ctrl=True 挂参数匹配 pseudo 模块——键集随构造不同，必须与训练列一致）
    → 全量文件 state dict 三分校验 → ``load_state_dict(strict=True)`` 逐键重载。

    文件侧新增键必须与 summarizer 键集**集合全等**——任何白名单外键出现即响亮
    （坑 8：from_pretrained 对 model.r3_summ.* 是 unexpected key 默认静默丢弃，
    必须文件全量 strict 重载回训练终态）。"""
    if attach:
        attach_summ(model, True, ctrl=ctrl)
    sd = read_state_dict(model_dir)
    model_keys = set(model.state_dict())
    summ_keys = set(_summ_param_keys(model))
    if not summ_keys:
        raise RuntimeError("[r3] 模型无 summarizer 键却走 strict_load_summ"
                           "（旗标/路径错配）——停报")
    base_keys = model_keys - summ_keys
    extra_in_file = sd.keys() - base_keys
    if extra_in_file != summ_keys:
        raise RuntimeError(
            f"[r3] 文件新增键 ≠ summarizer 白名单：file-only="
            f"{sorted(extra_in_file)[:8]}… summ={sorted(summ_keys)[:8]}… ——不点火")
    report = check_key_whitelist(sd.keys(), model_keys, summ_keys)
    report["n_summ_keys"] = len(summ_keys)
    model.load_state_dict(sd, strict=True)
    return report


def attach_and_strict_reload_summ(model: nn.Module, model_dir: str | Path,
                                  ctrl: bool = False) -> dict:
    """评测侧装载器（仪器启动器调用）：from_pretrained 装出的模型接 summarizer
    （ctrl 按 checkpoint config 戳记选择构造）+ strict 白名单重载，返回报告
    （进仪器 fingerprint 留档）。"""
    report = strict_load_summ(model, model_dir, attach=True, ctrl=ctrl)
    report["spec"] = "tools/baselines/deltanet_r2/r3_spec.py"
    report["num_params"] = SUMM_NUM_PARAMS
    report["ctrl"] = ctrl
    return report


# ===========================================================================
# 丙节：S0'' 段界器 × c1 变长铺瓦（任务书 §2.3 主构造，冻结 v1.0 逐字执行）
#
# 构造（变长铺瓦臂）：按 S0'' 切点把 DeltaNet 的 WY 计算铺瓦从原生 BT=64
# 改为变长——把窗按切点分成 ~172.7 段/窗（E124 门②在册数 ≈24B/块，施工
# 直测复核），逐段调用 chunk_delta_rule 并以 initial_state/final_state 接力。
# chunked delta rule 是线性递归的代数精确重排：分段+状态传递在精确算术下
# 逐位等价，铺瓦粒度差仅 fp 结合序（预注册预期=不杀，函数恒等）。
#
# 实现路径（勘定结论，2026-09-14 本地 5080 fla 0.5.2 实证）：
#   - fla 0.5.2 ``chunk_delta_rule`` 暴露 initial_state/output_final_state，
#     backward 返回 dh0（initial_state 梯度）→ 逐段接力全链 BPTT 可导，
#     训练等价成立；零自写核（1–2 天 masked-tile 备选路径解除）；
#   - 接力态按 q.dtype（bf16）cast——与原生 chunk 间状态传递同精度语义
#     （fla/ops/common/chunk_delta_h.py chunk_gated_delta_rule_fwd_h:30
#     ``h = k.new_empty(...)`` 即 bf16 逐块状态；final_state 以 fp32 返回）；
#   - use_qk_l2norm_in_kernel 的 L2 为逐 token 行归一，分段不变量；
#   - 数学恒等实证：T=640 bf16 随机输入、66 段变长 vs 原生单调用，
#     max|Δo|=3.0e-3、max|Δht|=2.4e-2（bf16 累积舍入带内）、dq/dk/dv/dβ
#     相对差 ≤1.2e-2（bf16 噪声带，梯度链贯通无截断）。
#
# 施工形态（最小侵入）：patch ``fla.layers.delta_net.chunk_delta_rule`` 名字
# （fla 0.5.2 layers/delta_net.py:20 模块级 import、:261 层内调用点）；旗标
# 默认关 = 不 patch、不建任何东西、**零新增参数**（参数锚与 R2 母列全等
# 48,152,896）。计划（每窗段长表）由调用侧逐窗设置（训练器/评测启动器），
# wrapper 读取；plan=None 时 wrapper 逐位直通原生（对拍门原生路径同款）。
#
# 坑 8 纪律：零新增参数 → 键集白名单=空集；checkpoint 键集必须与基座全等
# （任何多出/缺失键 loud-fail）。元数据随 config.json 字段 ``r3_vtile`` 落盘。
# ===========================================================================

VTILE_CONFIG_FIELD = "r3_vtile"
VTILE_CHUNK_SIZE = 64  # 段内原生 BT（fla 仅收 16/32/64；恒 64=母列粒度）

# S0'' 段界器 ctx4096 口径（E124 门②在册：训练流 172.7 块/窗 n=1001、
# ≈24B/块；与 canonical_v37 的差恰为 seq_len 4096 + max_chunks 1024，
# 见 checkpoints/v37ks_a_gate2base_v373_20k_ctx4096_20260910/resolved_config）
VTILE_S0_SEQ_LEN = 4096
VTILE_S0_MAX_CHUNKS = 1024
VTILE_S0_FRONTEND_PREFIXES = ("byte_lookup.", "encoder_blocks.",
                              "segmentor_blocks.", "segmentor_head.")

# 计划/patch 上下文（模块级单例；训练器与启动器逐窗 set、前向毕 clear）
_VTILE: dict = {"patched": False, "orig": None, "plan": None}


def set_vtile_plan(seg_lens: list[int] | None) -> None:
    """设置当前窗的段长表（sum 必须等于前向 T；由 wrapper 在核入口复核）。
    None = 清计划（wrapper 逐位直通原生）。未挂接时设置 = 响亮停报。"""
    if not _VTILE["patched"]:
        raise RuntimeError("[r3-vtile] set_vtile_plan 于未挂接态调用（先 "
                           "attach_vtile）——停报")
    if seg_lens is not None:
        if not seg_lens or any((not isinstance(l, int)) or l <= 0 for l in seg_lens):
            raise RuntimeError(f"[r3-vtile] 非法计划 {seg_lens!r}（空/非正/非整）"
                               "——停报")
    _VTILE["plan"] = list(seg_lens) if seg_lens is not None else None


def clear_vtile_plan() -> None:
    """清计划（前向毕必调；防跨窗泄漏）。未挂接时调用为无害 no-op（评测
    启动器 finally 路径的对称性）。"""
    _VTILE["plan"] = None


def vtile_apply(orig, plan: list[int] | None, q, k, v, beta, **kwargs):
    """变长铺瓦核（纯函数，单测锚点）：plan=None 逐位直通原生；否则按段长表
    切 T 维、逐段 ``orig(...)`` 并以 initial_state/final_state 接力（bf16
    handoff）。cu_seqlens varlen 路径不在本臂契约内（响亮停报）。"""
    if plan is None:
        return orig(q, k, v, beta, **kwargs)
    if kwargs.get("cu_seqlens") is not None or kwargs.get("cu_seqlens_cpu") is not None:
        raise RuntimeError("[r3-vtile] cu_seqlens varlen 路径不在变长铺瓦契约内"
                           "（R2 训练/评测均为 batch=1 全窗前向）——停报")
    t_total = q.shape[1]
    if not plan or sum(plan) != t_total:
        raise RuntimeError(f"[r3-vtile] 计划与输入不齐：sum(plan)={sum(plan)} "
                           f"!= T={t_total}（plan[:8]={plan[:8]}…，共 {len(plan)} 段）"
                           "——停报")
    # 层调用点全 kwarg 传参（delta_net.py:261）——initial_state/output_final_state
    # 由本函数接管（层的 initial_state 用作接力起点 = cache 语义顺势正确）
    passthrough = {kk: vv for kk, vv in kwargs.items()
                   if kk not in ("output_final_state", "initial_state")}
    outs, h = [], kwargs.get("initial_state")
    hi = None
    ofs = [0]
    for l in plan:
        ofs.append(ofs[-1] + l)
    for s0, s1 in zip(ofs[:-1], ofs[1:]):
        oi, hi = orig(q[:, s0:s1], k[:, s0:s1], v[:, s0:s1], beta[:, s0:s1],
                      initial_state=h, output_final_state=True, **passthrough)
        outs.append(oi)
        # bf16 接力（= 原生 chunk 间状态精度语义；hi 为 fp32 时 cast 回 q.dtype）
        h = hi.to(q.dtype) if hi is not None else None
    if hi is None:
        raise RuntimeError("[r3-vtile] 末段未返回 final_state（核契约漂移？）——停报")
    o = torch.cat(outs, dim=1)
    return o, (hi if kwargs.get("output_final_state") else None)


def _vtile_patched_chunk_delta_rule(q=None, k=None, v=None, beta=None, **kwargs):
    """fla.layers.delta_net.chunk_delta_rule 名字的替身（挂接态）：读模块级
    计划上下文派发 vtile_apply。fla 层内调用点（delta_net.py:261）全 kwarg
    传参，本签名全收。"""
    return vtile_apply(_VTILE["orig"], _VTILE["plan"], q, k, v, beta, **kwargs)


def attach_vtile(model: nn.Module, enabled: bool) -> dict:
    """旗标化挂接。enabled=False：核验无 patch/计划残留、不挂任何东西（=与
    R2 母列逐位不变路径）。enabled=True：核验宿主 chunk 模式契约后 patch
    ``fla.layers.delta_net.chunk_delta_rule``（模块级名字；层调用点 :261）。
    零新增参数、零权重改动。"""
    if not enabled:
        if _VTILE["patched"]:
            raise RuntimeError("[r3-vtile] flag-off 但 patch 仍在（先 detach_"
                               "vtile）——停报")
        if _VTILE["plan"] is not None:
            raise RuntimeError("[r3-vtile] flag-off 但计划残留——停报")
        return {"patched": False, "n_params_added": 0}

    import fla.layers.delta_net as dn_mod
    if _VTILE["patched"]:
        raise RuntimeError("[r3-vtile] 重复挂接（patch 已在场）——停报")
    mode = getattr(getattr(model, "config", None), "attn_mode", None)
    if mode != "chunk":
        raise RuntimeError(f"[r3-vtile] 宿主 attn_mode={mode!r} ≠ 'chunk'"
                           "（wrapper 只覆盖 chunk 调用点 delta_net.py:261）——停报")
    _VTILE["orig"] = dn_mod.chunk_delta_rule
    _VTILE["patched"] = True
    _VTILE["plan"] = None
    dn_mod.chunk_delta_rule = _vtile_patched_chunk_delta_rule
    return {"patched": True, "n_params_added": 0,
            "tap": "fla.layers.delta_net.chunk_delta_rule (module-level name)",
            "chunk_size": VTILE_CHUNK_SIZE}


def detach_vtile() -> None:
    """摘 patch（对拍门同进程原生/vtile 双路切换用）。计划必须已清（响亮）。"""
    if not _VTILE["patched"]:
        return
    if _VTILE["plan"] is not None:
        raise RuntimeError("[r3-vtile] detach 时计划未清（跨窗泄漏风险）——停报")
    import fla.layers.delta_net as dn_mod
    if dn_mod.chunk_delta_rule is not _vtile_patched_chunk_delta_rule:
        raise RuntimeError("[r3-vtile] patch 场被第三方改写（无法安全还原）——停报")
    dn_mod.chunk_delta_rule = _VTILE["orig"]
    _VTILE["patched"] = False
    _VTILE["orig"] = None


# ---------------------------------------------------------------------------
# S0'' 切点 → token 计划（纯 Python 映射，确定性规约；单测锚点）
# ---------------------------------------------------------------------------


def byte_char_boundaries(raw: bytes) -> list[int]:
    """char_before[b] = len(decode(raw[:b], errors='replace'))，b ∈ [0, len(raw)]
    （len(raw)+1 项）——切点映射的唯一合法字符位语义（前缀解码）。

    - 净 utf-8 窗（严格解码探针通过）：增量解码快路径——多字节字符在末字节
      闭合，切点只落非续字节位（=字符边界），该处增量与前缀解码逐位相等；
    - 违例字节窗：逐前缀解码慢路径（精确但 O(n²)，仅违例窗触发；替换字符
      记账时点随前缀语义）。"""
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        return [len(raw[:b].decode("utf-8", "replace"))
                for b in range(len(raw) + 1)]
    import codecs
    dec = codecs.getincrementaldecoder("utf-8")("strict")
    out = [0]
    for byte in raw:
        out.append(out[-1] + len(dec.decode(bytes([byte]))))
    out[-1] += len(dec.decode(b"", True))
    return out


def token_plan_from_byte_cuts(cut_bytes, char_before, offsets, t_total: int,
                              first_token: int = 1):
    """byte 切点 → token 边界计划（映射规约，随 config.r3_vtile 落盘）：

    - byte 0 切点 = 窗起点标记（每窗必有，E124 hard_cut 首位恒真），非内容
      切点 → 跳过不映射；其余 byte 切点 b → 字符位 c = char_before[b]；
    - token 边界 = 首个 start_offset ≥ c 的 token 下标 t ∈ [first_token,
      t_total)（round-right：跨切点的 token 归左段——右段永不含切点前字节；
      first_token=1 跳过 BOS 特殊位）；
    - 去重；段长 = 相邻边界差（含 0 与 t_total 端点）。

    返回 (段长表, 统计 dict)：n_cuts_byte（byte 空间切点数，含窗起点标记，
    ≈172.7 直测复核量）、n_segments（token 空间段数 ≤ n_cuts_byte−1，合并
    只少不多）、seg_len_min/max/mean。"""
    if len(char_before) < 2:
        raise RuntimeError("[r3-vtile] char_before 空表（raw 空？）——停报")
    if t_total <= 0 or t_total > len(offsets):
        raise RuntimeError(f"[r3-vtile] t_total={t_total} 与 offsets {len(offsets)}"
                           "不齐——停报")
    bounds: set[int] = set()
    for b in cut_bytes:
        if not (0 <= b < len(char_before) - 1):
            raise RuntimeError(f"[r3-vtile] 切点 byte {b} 出界（窗长 "
                               f"{len(char_before) - 1}）——停报")
        if b == 0:
            continue  # 窗起点标记，非内容切点
        c = char_before[b]
        t = first_token
        while t < t_total and offsets[t][0] < c:
            t += 1
        if first_token <= t < t_total:
            bounds.add(t)
    ordered = sorted(bounds)
    edges = [0] + ordered + [t_total]
    plan = [hi - lo for lo, hi in zip(edges[:-1], edges[1:])]
    stats = {
        "n_cuts_byte": len(cut_bytes),
        "n_segments": len(plan),
        "seg_len_min": min(plan), "seg_len_max": max(plan),
        "seg_len_mean": round(sum(plan) / len(plan), 4),
    }
    return plan, stats


# ---------------------------------------------------------------------------
# S0'' 段界器装载与逐窗计划（训练器/评测启动器共用单源）
# ---------------------------------------------------------------------------


def load_s0_segmentor(s0_checkpoint: str, device: str = "cuda",
                      canonical_config_path: str | None = None):
    """S0'' 段界器装载（canonical_v37 init_checkpoint 锚，ctx4096 口径）：
    canonical_v37.json + {seq_len: 4096, max_chunks: 1024}（E124 门②在册
    172.7 块/窗运行口径）构建 FLUEDV36，前端四前缀键 strict 形状校验载入
    （E124 门①在册 199 键口径，实测数为准），前端 freeze + 全模 eval。

    前端键集 = byte_lookup/encoder_blocks/segmentor_blocks/segmentor_head
    （canonical_v37 freeze_prefixes）；缺键/形漂 loud-fail（坑 8）。"""
    import json
    from argparse import Namespace
    from pathlib import Path
    root = Path(__file__).resolve().parents[3]
    cfg_path = Path(canonical_config_path) if canonical_config_path \
        else root / "configs" / "canonical_v37.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg.update({"seq_len": VTILE_S0_SEQ_LEN, "max_chunks": VTILE_S0_MAX_CHUNKS,
                "data_manifest": "",
                # canonical_v37.json 缺的新 CLI 字段，按在册 ctx4096 运行口径
                # （checkpoints/v37ks_a_gate2base_v373_20k_ctx4096_20260910）
                "prefix_task": False, "prefix_positions": 4})
    if device == "cpu":
        cfg["kda_impl"] = "torch"
    from tools.train.v3_6.train_v36 import build_model
    model = build_model(Namespace(**cfg))
    payload = torch.load(s0_checkpoint, map_location="cpu", weights_only=False)
    sd = payload["model"] if isinstance(payload, dict) and "model" in payload else payload
    model_sd = model.state_dict()
    fe_keys = [kk for kk in model_sd if kk.startswith(VTILE_S0_FRONTEND_PREFIXES)]
    if not fe_keys:
        raise RuntimeError("[r3-vtile] 模型无前端键（V36Config 结构漂移？）——停报")
    missing = [kk for kk in fe_keys if kk not in sd]
    shape_bad = [kk for kk in fe_keys
                 if kk in sd and tuple(sd[kk].shape) != tuple(model_sd[kk].shape)]
    if missing or shape_bad:
        raise RuntimeError(
            "[r3-vtile] S0'' 前端键校验失败——"
            f"缺 {missing[:6]}{'…' if len(missing) > 6 else ''} / 形漂 "
            f"{shape_bad[:6]}{'…' if len(shape_bad) > 6 else ''} ——停报")
    model.load_state_dict({kk: sd[kk] for kk in fe_keys}, strict=False)
    reloaded = model.state_dict()
    for kk in fe_keys:
        if not torch.equal(reloaded[kk], sd[kk]):
            raise RuntimeError(f"[r3-vtile] 前端键 {kk} 载入后不逐位（strict=False "
                               "静默过滤事故形态）——停报")
    for p in model.parameters():
        p.requires_grad_(False)
    model.eval()
    print(f"[r3-vtile] S0'' 段界器就位：{len(fe_keys)} 前端键 strict 载入"
          f"（锚 {s0_checkpoint}，ctx4096 口径 max_chunks={VTILE_S0_MAX_CHUNKS}）",
          flush=True)
    return model.to(device)


def s0_cut_bytes(segmentor, raw: bytes, device: str = "cuda") -> list[int]:
    """S0'' 直测：4096B 窗 → 预算后切点 byte 位置表（v36 ``_encode→_cuts``
    在册语义 = tau_cut 0.94 + utf8 续字节过滤 + capacity-safe，E124 hard_cut
    同款）。容量溢出（overflow>0）响亮停报——切点被截断即非在册口径。"""
    from flued.data import PAD_ID
    from flued.v34.model import _plastic_signed_confidence
    if len(raw) != VTILE_S0_SEQ_LEN:
        raise RuntimeError(f"[r3-vtile] 窗长 {len(raw)} ≠ S0'' 口径 "
                           f"{VTILE_S0_SEQ_LEN}——停报")
    ids = torch.frombuffer(bytearray(raw), dtype=torch.uint8).long() + 1  # PAD-offset
    ids = ids.unsqueeze(0).to(device)
    if (ids == PAD_ID).any():
        raise RuntimeError("[r3-vtile] 窗内出现 PAD_ID（bytes+1 编码下不可能）——停报")
    with torch.no_grad():
        logits, valid = segmentor.encode_boundary_logits(ids)
        confidence = _plastic_signed_confidence(logits)
        hard_cut, _utf8_cont, overflow = segmentor._cuts(ids, confidence, valid)
    if int(overflow.sum()) > 0:
        raise RuntimeError("[r3-vtile] S0'' 切点容量溢出（max_chunks/max_span "
                           "截断发生，非在册口径）——停报")
    pos = hard_cut[0].nonzero(as_tuple=True)[0].tolist()
    return pos


def vtile_plan_for_window(segmentor, tok, raw: bytes, t_total: int,
                          device: str = "cuda") -> tuple[list[int], dict]:
    """窗字节 → (段长表, 统计)。S0'' 切点（byte 空间）→ token 边界映射；
    t_total = 前向 T（训练 = len(ids)-1，x/y 错位；评测 = len(ids)，仪器全
    序前向）。统计含 n_cuts_byte（≈172.7 直测复核量）与 token 空间段长分布。"""
    text = raw.decode("utf-8", errors="replace")
    enc = tok(text, return_offsets_mapping=True)
    offsets = [tuple(o) for o in enc["offset_mapping"]]
    cut_bytes = s0_cut_bytes(segmentor, raw, device)
    char_before = byte_char_boundaries(raw)
    return token_plan_from_byte_cuts(cut_bytes, char_before, offsets, t_total)


# ---------------------------------------------------------------------------
# 丙侧 config 元数据与坑 8 装载校验（零新增参数 → 键集=基座全等）
# ---------------------------------------------------------------------------


def stamp_vtile_config(config, extra: dict | None = None) -> None:
    config.r3_vtile = {
        "enabled": True,
        "construction": "variable-length WY tiling at S0'' cut points "
                        "(per-segment chunk_delta_rule + initial_state carry)",
        "chunk_size": VTILE_CHUNK_SIZE,
        "state_carry": "bf16 handoff (= native chunk-to-chunk precision)",
        "s0_seq_len": VTILE_S0_SEQ_LEN,
        "s0_max_chunks": VTILE_S0_MAX_CHUNKS,
        "mapping": "byte cut -> char (utf-8 replace incremental) -> first token "
                   "with start_offset >= c (round-right; byte-0 window-start "
                   "marker skipped; BOS skipped), dedupe",
        "n_params_added": 0,
        "spec": "tools/baselines/deltanet_r2/r3_spec.py",
        **(extra or {}),
    }


def config_has_vtile(config) -> bool:
    flag = getattr(config, VTILE_CONFIG_FIELD, None)
    return bool(flag and flag.get("enabled"))


def verify_vtile_reload(model: nn.Module, model_dir: str | Path) -> dict:
    """丙 checkpoint 唯一合法装载校验（零新增参数特化）：config 戳记在场 +
    文件键集与模型键集**集合全等**（任何多出/缺失键 loud-fail，坑 8）+ 参数
    锚与 R2 母列全等 + 全量 strict 重载（对齐训练终态）。"""
    if not config_has_vtile(model.config):
        raise RuntimeError("[r3-vtile] checkpoint config 无 r3_vtile 戳记"
                           "（旗标/路径错配）——停报")
    sd = read_state_dict(model_dir)
    model_keys = set(model.state_dict())
    if set(sd) != model_keys:
        extra = sorted(set(sd) - model_keys)[:8]
        miss = sorted(model_keys - set(sd))[:8]
        raise RuntimeError(f"[r3-vtile] 键集与基座不全等（丙零新增参数）："
                           f"file-only={extra} model-only={miss} ——不点火")
    n = sum(p.numel() for p in model.parameters())
    if n != r2spec.EXPECTED_PARAM_COUNT:
        raise RuntimeError(f"[r3-vtile] 参数锚 {n:,} ≠ 母列锚 "
                           f"{r2spec.EXPECTED_PARAM_COUNT:,}（丙零新增参数）——停报")
    model.load_state_dict(sd, strict=True)
    return {"n_keys": len(model_keys), "n_params_added": 0,
            "expected_param_count": r2spec.EXPECTED_PARAM_COUNT,
            "spec": "tools/baselines/deltanet_r2/r3_spec.py"}


def attach_and_reload_vtile(model: nn.Module, model_dir: str | Path,
                            s0_checkpoint: str, device: str = "cuda") -> dict:
    """评测侧装载器（仪器启动器调用）：attach patch + verify_vtile_reload +
    S0'' 段界器就位（随报告返回，启动器持有以逐窗设计划）。"""
    attach = attach_vtile(model, True)
    report = verify_vtile_reload(model, model_dir)
    segmentor = load_s0_segmentor(s0_checkpoint, device=device)
    report.update(attach)
    report["segmentor"] = segmentor
    return report
