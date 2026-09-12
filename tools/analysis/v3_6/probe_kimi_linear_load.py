"""Kimi-Linear-48B-A3B-Base 双卡装载与 KDA 状态仪器原语（kimi122 跨架构复证臂）。

为 moonshotai/Kimi-Linear-48B-A3B-Base（48B-A3B MoE，BF16 20 shards ≈98.25G）的
三件零训练仪器（必要性账 / 闭式读出 / KDA 状态置零解离）提供公共底座。移植自
tools/analysis/cross_arch/ 的 DeltaNet 仪器（agent-203/204 施工），命名同族。

模型事实（/l/models_hf 本地 ref 小件已读码验证，sha1 对上 HF MANIFEST）：
- KDA 层类 = ``KimiDeltaAttention``（modeling_kimi.py 内定义，fla.ops.kda 核）；
  全注意力层 = ``KimiMLAAttention``（DeepSeek-V3 式 MLA）。层号分布（1 基）：
  kda_layers = 全部 27 层去掉 full_attn_layers [4,8,12,16,20,24,27] → 20 KDA +
  7 MLA（3:1）。``config.is_kda_layer(i)`` 按 **1 基** 表查（i+1 in kda_layers）。
- 线性递归状态：``KimiDynamicCache.recurrent_states[layer_idx]``，由
  ``fla.ops.kda.chunk_kda(output_final_state=True)`` 写出，形状
  ``[B, HV=32, K=128, V=128]``（Kimi 48B 无 GVA，HV=H=32）。short conv 状态另存
  ``conv_states[layer_idx]``（三元组，kernel 4）。
- 递推式（fla/ops/kda/naive.py naive_recurrent_kda 语义，已逐行核对）：
  S ← S ⊙ exp(g_t)（K 维 fine-grained 门控）；
  S += (β·k_t) ⊗ (v_t − k_tᵀS)；o_t = q_tᵀS（o 与 scale 不影响 S，读出只需状态）。
  q,k 进核前逐 token L2 归一（use_qk_l2norm_in_kernel=True）。
- 环境要求（HF README）：python≥3.10、torch≥2.6、fla-core≥0.4.0、tiktoken；
  modeling_kimi 断言 transformers≥4.56.0（config 以 4.57.0 构建）。**坑**：
  KimiLinearModel.__init__ 无条件强制 ``config._attn_implementation =
  "flash_attention_2"``（MLA 走 ALL_ATTENTION_FUNCTIONS 注册表派发）——无
  flash-attn 的环境（含 CPU 冒烟）必须挂 SDPA 等价 shim，否则首前向即炸。

本模块只依赖 torch（transformers/fla 全部惰性 import），本地无卡无权重环境
可 import / 单测（同 e122/dsr 先例）。

硬件指纹纪律（AGENTS 坑 11/12）：所有体制判词一律「同机同 env 内成立」，
fingerprint 落 summary。
"""

from __future__ import annotations

from typing import Any, Optional

import torch

# Kimi-Linear-48B-A3B-Base 关键形状（config.json 固化，仪器内部断言用）
N_KDA_LAYERS = 20
N_FULL_ATTN_LAYERS = 7
KDA_HEADS = 32          # HV = H（无 GVA）
KDA_HEAD_DIM = 128      # K = V = 128
STATE_DIM_PER_BOUNDARY = KDA_HEADS * KDA_HEAD_DIM * KDA_HEAD_DIM  # 524288
DEFAULT_CHUNK_SIZE = 64


# ---------------------------------------------------------------------------
# 层号工具（1 基表 → 0 基层号；纯 python，单测覆盖）
# ---------------------------------------------------------------------------


def kda_layer_indices(config) -> list[int]:
    """config.linear_attn_config["kda_layers"]（1 基）→ 排序后的 0 基 KDA 层号。"""
    lat = getattr(config, "linear_attn_config", None)
    if not lat or lat.get("kda_layers") is None:
        return []
    return sorted(int(l) - 1 for l in lat["kda_layers"])


def full_attn_layer_indices(config) -> list[int]:
    """0 基全注意力（MLA）层号。"""
    lat = getattr(config, "linear_attn_config", None)
    if not lat or lat.get("full_attn_layers") is None:
        return []
    return sorted(int(l) - 1 for l in lat["full_attn_layers"])


# ---------------------------------------------------------------------------
# MLA SDPA shim（无 flash-attn 环境的数学等价后端）
# ---------------------------------------------------------------------------


def sdpa_attention_forward(module, query_states, key_states, value_states,
                           attention_mask=None, scaling=None, dropout: float = 0.0,
                           q_chunk: int = 1024, **kwargs):
    """eager/flash_attention_2 调用形参兼容的 SDPA 等价实现。

    数学等价性：Kimi MLA 的 4D additive causal mask（create_causal_mask 产物）
    直接作 SDPA ``attn_mask``（softmax(QKᵀ·scale + M)V）；mask 已编码因果性，
    故 is_causal=False。查询维分块（q_chunk）只为约束 math 后端的中间张量内存，
    逐块结果与整块逐位一致（softmax 行独立）。
    返回 (attn_output [B,q,H,dv], attn_weights=None)——与 eager 同形。
    输入约定与 eager/注册表派发一致：q,k,v 为 [B,H,q,dk|dv]（Kimi MLA 在调用前
    已 transpose(1,2)；不另做 flash-attn 式 [B,q,H,d] 转置）。"""
    qh = query_states
    kh = key_states
    vh = value_states
    if kh.shape[1] != qh.shape[1]:  # GQA 保护（Kimi 48B 不触发，保通用）
        n = qh.shape[1] // kh.shape[1]
        kh = kh.repeat_interleave(n, dim=1)
        vh = vh.repeat_interleave(n, dim=1)
    if scaling is None:
        scaling = qh.shape[-1] ** -0.5
    outs = []
    q_len = qh.shape[-2]
    for q0 in range(0, q_len, q_chunk):
        q = qh[..., q0:q0 + q_chunk, :]
        m = None
        if attention_mask is not None:
            m = attention_mask[..., q0:q0 + q_chunk, :]
        outs.append(torch.nn.functional.scaled_dot_product_attention(
            q, kh, vh, attn_mask=m, dropout_p=dropout, scale=scaling))
    attn = torch.cat(outs, dim=-2) if len(outs) > 1 else outs[0]
    return attn.transpose(1, 2), None


def install_kimi_mla_sdpa_shim() -> str:
    """flash-attn 缺席时，把 ALL_ATTENTION_FUNCTIONS["flash_attention_2"] 换成
    SDPA 等价 shim（进程内改注册表条目，不改任何库/远码文件）。modeling_kimi
    在 forward 时才查注册表，故构造后改条目即生效。返回实际后端名（落
    fingerprint）。flash-attn 可导入时不动注册表（原生后端优先）。"""
    try:
        import flash_attn  # noqa: F401
        return "flash-attn"
    except ImportError:
        pass
    import transformers.modeling_utils as _mm

    _mm.ALL_ATTENTION_FUNCTIONS["flash_attention_2"] = sdpa_attention_forward
    return "sdpa-shim"


# ---------------------------------------------------------------------------
# 模型/分词器装载（transformers 惰性 import；BF16；device_map 聚合）
# ---------------------------------------------------------------------------


def load_model_and_tokenizer(model_path: str, device: torch.device,
                             max_memory: Optional[dict] = None):
    """trust_remote_code 装载 KimiLinearForCausalLM + TikToken tokenizer。

    - BF16 全量；GPU 上 device_map="auto"（双卡聚合；accelerate 需要），
      max_memory 可传 {"0":"70GiB","1":"70GiB"} 类约束；CPU 冒烟 device_map="cpu"。
    - MLA 后端：flash-attn 在 → 原生；缺席 → SDPA shim（双臂同后端，对照内公平）。
    - tokenizer：TikTokenTokenizer（tiktoken.model 词表）；注意其 ``__call__``
      **不前置 BOS**（TikTokenTokenizer 未覆写 build_inputs_with_special_tokens），
      窗序列即裸 token——同卷事实，落 summary。
    返回 (model, tok, fingerprint)。"""
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    attn_backend = install_kimi_mla_sdpa_shim()
    tok = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    kw: dict[str, Any] = dict(trust_remote_code=True, dtype=torch.bfloat16)
    kw["device_map"] = "cpu" if device.type == "cpu" else "auto"
    if max_memory:
        kw["max_memory"] = max_memory
    model = AutoModelForCausalLM.from_pretrained(model_path, **kw)
    model.eval()

    gpus = []
    if torch.cuda.is_available():
        gpus = [torch.cuda.get_device_name(i)
                for i in range(torch.cuda.device_count())]
    fingerprint = {
        "model_path": str(model_path),
        "vocab_size": int(model.config.vocab_size),
        "num_hidden_layers": int(model.config.num_hidden_layers),
        "kda_layers_0based": kda_layer_indices(model.config),
        "full_attn_layers_0based": full_attn_layer_indices(model.config),
        "kda_state_shape": [KDA_HEADS, KDA_HEAD_DIM, KDA_HEAD_DIM],
        "dtype": "bfloat16",
        "attn_backend": attn_backend,
        "gpus": gpus,
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "fla": _fla_version(),
        "tokenizer_no_bos": True,
        "hardware_note": "体制判词一律「同机同 env 内成立」（AGENTS 坑 11/12 纪律）",
    }
    return model, tok, fingerprint


def _fla_version() -> str:
    try:
        import fla
        return getattr(fla, "__version__", "unknown")
    except ImportError:
        return "absent"


def tokenize_window(tok, text: str, max_tokens: int) -> tuple[list[int], int]:
    """窗文本 → token ids（与 e122.tokenize_window 同一调用形：``tok(text)``
    默认 special tokens 行为；Kimi 不加 BOS），截到 max_tokens。"""
    ids = list(tok(text)["input_ids"])
    return ids[:max_tokens], len(ids)


def kimi_modeling_module(model):
    """trust_remote_code 动态模块句柄（monkeypatch 目标；进程内，不改文件）。"""
    import sys
    name = type(model).__module__
    mod = sys.modules.get(name)
    if mod is None or not hasattr(mod, "chunk_kda"):
        raise RuntimeError(f"modeling 模块解析失败: {name}（无 chunk_kda 全局名）")
    return mod


# ---------------------------------------------------------------------------
# KDA chunk_kda 捕获（monkeypatch；模型行为零改动）
# ---------------------------------------------------------------------------


class KdaChunkCapture:
    """monkeypatch modeling_kimi.chunk_kda（层模块全局名，forward 内调用点）。

    原函数照常执行并原样返回（模型行为零改动）；旁路留存每层 (k, v, g, beta)
    （pre-L2 原始捕获，detach 后搬 CPU bf16）+ 核返回的 final_state（fp32，
    哨兵对拍用）。q 不留存（状态只依赖 k,v,g,beta；内存减半）。"""

    def __init__(self):
        self.records: list[dict] = []
        self._mod = None
        self._orig = None

    def __enter__(self):
        if self._mod is None:
            raise RuntimeError("KdaChunkCapture 需先 bind(model) 再 with")
        self._orig = self._mod.chunk_kda
        cap = self

        def wrapper(*args, **kw):
            o, st = cap._orig(*args, **kw)
            rec = {
                "k": kw["k"].detach().to("cpu", torch.bfloat16),
                "v": kw["v"].detach().to("cpu", torch.bfloat16),
                "g": kw["g"].detach().to("cpu", torch.bfloat16),
                "beta": kw["beta"].detach().to("cpu", torch.bfloat16),
                "l2": bool(kw.get("use_qk_l2norm_in_kernel", False)),
                "kernel_final_state": st.detach().float().cpu(),
            }
            cap.records.append(rec)
            return o, st

        self._mod.chunk_kda = wrapper
        return self

    def __exit__(self, *exc):
        self._mod.chunk_kda = self._orig
        return False

    def bind(self, model) -> "KdaChunkCapture":
        self._mod = kimi_modeling_module(model)
        return self


# ---------------------------------------------------------------------------
# fp32 KDA 状态数学（纯 torch，单测对拍逐 token 朴素递推）
# ---------------------------------------------------------------------------


def kda_l2norm(x: torch.Tensor) -> torch.Tensor:
    """逐 token 头维 L2 归一（fla use_qk_l2norm_in_kernel 的 fp32 重算）。"""
    x = x.float()
    return x / x.norm(dim=-1, keepdim=True).clamp_min(1e-12)


def kda_state_recurrence_step(s: torch.Tensor, k_i: torch.Tensor,
                              v_i: torch.Tensor, g_i: torch.Tensor,
                              beta_i: torch.Tensor) -> torch.Tensor:
    """单步 KDA 状态更新（naive_recurrent_kda 语义，G=1）。
    s [H,K,V]；k_i [H,K]；v_i [H,V]；g_i [H,K]（log 域）；beta_i [H]。
    S ← S·exp(g)ᵀ列 + (βk) ⊗ (v − kᵀS)。"""
    s = s * g_i.exp().unsqueeze(-1)
    k_s = torch.einsum("hk,hkv->hv", k_i, s)
    upd = v_i - k_s
    return s + torch.einsum("hk,hv->hkv", beta_i.unsqueeze(-1) * k_i, upd)


def kda_chunk_boundary_states(k: torch.Tensor, v: torch.Tensor,
                              g: torch.Tensor, beta: torch.Tensor,
                              chunk_size: int = DEFAULT_CHUNK_SIZE,
                              initial_state: Optional[torch.Tensor] = None,
                              apply_l2norm: bool = True) -> torch.Tensor:
    """fp32 chunk 边界态（状态专用：o/scale 不影响 S，不重算）。

    k [T,H,K]（捕获原态；apply_l2norm=True 时先逐 token L2）、v [T,H,V]、
    g [T,H,K]（log 域 fine-grained 门控）、beta [T,H] → states [NS+1,H,K,V]，
    states[c] = 恰好消费 token < c·chunk_size 后的状态；末槽 = 终态（T 非整
    chunk 时末槽为部分 chunk 态，如实标注由调用方处理）。"""
    if apply_l2norm:
        k = kda_l2norm(k)
    k = k.transpose(0, 1).float()      # [H,T,K]
    v = v.transpose(0, 1).float()      # [H,T,V]
    g = g.transpose(0, 1).float()      # [H,T,K]
    beta = beta.transpose(0, 1).float()  # [H,T]
    h, t_len, _kd = k.shape
    vd = v.shape[-1]
    s = k.new_zeros(h, k.shape[-1], vd)
    if initial_state is not None:
        s = s + initial_state.float()
    states = [s.clone()]
    for i in range(t_len):
        s = kda_state_recurrence_step(s, k[:, i], v[:, i], g[:, i], beta[:, i])
        if (i + 1) % chunk_size == 0:
            states.append(s.clone())
    if t_len % chunk_size:
        states.append(s.clone())  # 部分末块终态（与核 final_state 对拍的槽位）
    return torch.stack(states)


def extract_kda_boundary_states(records: list[dict], chunk_size: int,
                                tol_rel: float
                                ) -> tuple[list[torch.Tensor], list[dict]]:
    """capture.records → 每层边界态 [NS+1,H,K,V]（fp32）。

    哨兵（前提验证，dsr 同款）：与核自身 final_state（wrapper 旁路留存）对拍
    相对 Frobenius 误差，超阈 RuntimeError 响亮停机——状态递推式/gate 语义若与
    安装版 fla 不符，在这里响，绝不静默产错状态。"""
    outs, verr = [], []
    for i, rec in enumerate(records):
        states = kda_chunk_boundary_states(
            rec["k"], rec["v"], rec["g"], rec["beta"], chunk_size,
            apply_l2norm=rec["l2"])
        kern = rec["kernel_final_state"][0]
        rel = ((states[-1] - kern).norm() / kern.norm().clamp_min(1e-8)).item()
        verr.append({"layer": i, "rel_err": rel})
        if rel > tol_rel:
            raise RuntimeError(
                f"KDA 状态抽取对拍失败：layer {i} fp32 边界态终态 vs 核 final_state "
                f"相对误差 {rel:.4g} > {tol_rel}（递推式/gate 语义与安装版 fla "
                f"不符，前提不成立，响亮停机）")
        outs.append(states)
    return outs, verr


# ---------------------------------------------------------------------------
# KimiDynamicCache 手术原语（置零/快照/恢复；duck-typed，单测用 FakeCache）
# ---------------------------------------------------------------------------


def _clone_opt(t: Optional[torch.Tensor]) -> Optional[torch.Tensor]:
    return None if t is None else t.detach().clone()


def snapshot_linear_cache(cache) -> dict:
    """深拷贝 linear cache 三类可变槽（MLA KV / KDA conv / KDA recurrent）。
    suffix 前向会改写全部三类——基线臂恢复靠它。"""
    return {
        "key_cache": [_clone_opt(t) for t in cache.key_cache],
        "value_cache": [_clone_opt(t) for t in cache.value_cache],
        "conv_states": [
            None if c is None else tuple(_clone_opt(t) for t in c)
            for c in cache.conv_states],
        "recurrent_states": [_clone_opt(t) for t in cache.recurrent_states],
    }


def restore_linear_cache(cache, snap: dict) -> None:
    cache.key_cache = list(snap["key_cache"])
    cache.value_cache = list(snap["value_cache"])
    cache.conv_states = [
        None if c is None else tuple(c) for c in snap["conv_states"]]
    cache.recurrent_states = list(snap["recurrent_states"])


def zero_kda_recurrent_states(cache, layers: list[int],
                              conv_too: bool = False) -> int:
    """置零指定 KDA 层的递归状态（手术臂）。返回实际置零层数。
    conv_too=True 连同 short conv 状态置零（默认 False：conv 只携带 ≤kernel-1
    个近邻 token，不属长程通道；置零会在 suffix 首几个 token 引入非受控扰动）。
    断言槽位已存在（必须先跑过 prefix 前向），None 槽响亮拒绝。"""
    n = 0
    for l in layers:
        r = cache.recurrent_states[l]
        if r is None:
            raise RuntimeError(
                f"layer {l} recurrent_state 为 None（须先跑 prefix 前向再手术）")
        cache.recurrent_states[l] = torch.zeros_like(r)
        n += 1
        if conv_too and cache.conv_states[l] is not None:
            cache.conv_states[l] = tuple(torch.zeros_like(t)
                                         for t in cache.conv_states[l])
    return n
