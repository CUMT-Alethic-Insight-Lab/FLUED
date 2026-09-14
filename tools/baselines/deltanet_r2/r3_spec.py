"""R3 移植臂冻结规格单源（甲=对角护栏/恒等自读回声，乙=summarizer 双头构造）。

任务书：docs/versions/v3.7/FLUED_V3_7_R3_DELTANET_TRANSPLANT_DRAFT_20260914_CN.md
（冻结 v1.0，2026-09-14 用户终审签发；前置门六件回执齐了点火）。
甲臂回执：outputs/r3_transplant_echo_20260914/R3_ECHO_RECEIPT_20260914.md。
乙臂回执：outputs/r3_transplant_summ_20260914/R3_SUMM_RECEIPT_20260914.md。

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


def build_summarizer():
    """原件构造零重实现：import flued.v36.model.DiTChunkSummarizer 实类实例化
    （init 纪律随原件：pool_queries trunc_normal std=0.02，其余默认 init）。"""
    from flued.v36.model import DiTChunkSummarizer
    summ = DiTChunkSummarizer(_summ_cfg())
    if not hasattr(summ, "index_ffn"):
        raise RuntimeError("[r3] summarizer 无 index_ffn（backbone_mode≠slm？）"
                           "——双头构造缺一头，停报")
    if (summ.QPOOL_QUERIES, summ.QPOOL_ANCHOR_TEMP) != (4, 16.0):
        raise RuntimeError("[r3] qpool 构造常量漂移（≠4 锚查询/temp 16.0）——停报")
    return summ


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


def _summ_param_keys(model: nn.Module) -> list[str]:
    return [k for k, _ in model.named_parameters()
            if f".{SUMM_ATTR}." in f".{k}"]


def attach_summ(model: nn.Module, enabled: bool) -> list[str]:
    """旗标化挂接（§2.2 主构造）。enabled=False：核验无 summarizer 残留、不挂
    任何东西，返回 []（= 与 R2 母列逐位不变路径）。enabled=True：建
    ``model.r3_summ`` 模块 + embedding 汇总 hook + 每层 k/v 替换 hook，返回
    新增键表（=模块 named_parameters 穷举，白名单本体）。"""
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
    summ = build_summarizer()
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
        hooks.append(attn.k_conv1d.register_forward_hook(_replace_hook("k_c")))
        hooks.append(attn.v_conv1d.register_forward_hook(_replace_hook("m_c")))
    base._r3_summ_hooks = hooks

    got = _summ_param_keys(model)
    if not got:
        raise RuntimeError("[r3] 挂接后未发现 summarizer 参数——停报")
    return got  # = 白名单本体（model.r3_summ.* 穷举）


# ---------------------------------------------------------------------------
# config 元数据（summarizer 旗标随 checkpoint 落盘；fla DeltaNetConfig 收 **kwargs）
# ---------------------------------------------------------------------------


def stamp_summ_config(config) -> None:
    config.r3_summ = {
        "enabled": True,
        "construction": "single-point summary + dual-head full wiring",
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
                     attach: bool = True) -> dict:
    """summarizer checkpoint 的唯一合法装载路径：attach（模块+hook+白名单）
    → 全量文件 state dict 三分校验 → ``load_state_dict(strict=True)`` 逐键重载。

    文件侧新增键必须与 summarizer 键集**集合全等**——任何白名单外键出现即响亮
    （坑 8：from_pretrained 对 model.r3_summ.* 是 unexpected key 默认静默丢弃，
    必须文件全量 strict 重载回训练终态）。"""
    if attach:
        attach_summ(model, True)
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


def attach_and_strict_reload_summ(model: nn.Module, model_dir: str | Path) -> dict:
    """评测侧装载器（仪器启动器调用）：from_pretrained 装出的模型接 summarizer
    + strict 白名单重载，返回报告（进仪器 fingerprint 留档）。"""
    report = strict_load_summ(model, model_dir, attach=True)
    report["spec"] = "tools/baselines/deltanet_r2/r3_spec.py"
    report["num_params"] = SUMM_NUM_PARAMS
    return report
