"""R2 臂冻结规格（单源）。任务书 v1.0 §2/§3/§9 的全部数值锚在此登记，
训练器 / 锚直测 / 测试一律 import 本模块，禁止散落复制（坑 8：显式旗标全带）。

参数锚裁定注记（施工回执同文）：任务书文本「expand ratio 3」与预注册参数数
48,152,896 冲突——fla 0.5.1 DeltaNetConfig 全家族实例化扫描下，48,152,896 在
本规模（d_model=320 / heads=5 / layers=24 / untied / vocab=32000）有且仅有
expand_k=1.0 / expand_v=1.0 / use_gate=False / use_short_conv=True /
intermediate_size=768 一解；且母本 fla-hub/delta_net-1.3B-100B config.json
实为 expand_k=1 / expand_v=1（fla-hub 拉取在案）。参数数是预注册硬锚、本配置
同为其唯一解并逐旗标母本同构 → 按 48,152,896 施行，「expand ratio 3」按笔误
升级报告待主会话销案。
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterator

# ---------------------------------------------------------------------------
# 冻结配置（母本 = fla-hub/delta_net-1.3B-100B config.json，hf-mirror 拉取；
# 仅 hidden/heads/intermediate 缩放，其余旗标逐项母本同构）
# ---------------------------------------------------------------------------

EXPECTED_PARAM_COUNT = 48_152_896  # 预注册硬锚（实例化不符即停报）

PARENT_MODEL_ID = "fla-hub/delta_net-1.3B-100B"

R2_CONFIG: dict = {
    "hidden_size": 320,
    "num_heads": 5,
    "num_layers": 24,
    "expand_k": 1.0,
    "expand_v": 1.0,
    "use_gate": False,
    "use_short_conv": True,
    "conv_size": 4,
    "intermediate_size": 768,
    "hidden_act": "swish",
    "qk_activation": "silu",
    "qk_norm": "l2",
    "use_beta": True,
    "allow_neg_eigval": False,
    "norm_eps": 1e-6,
    "fuse_norm": True,
    "use_output_norm": True,
    "attn_mode": "chunk",
    "attn": None,
    "attnres_block_size": None,
    "vocab_size": 32000,
    "max_position_embeddings": 2048,
    "tie_word_embeddings": False,  # tf5.15.1+fla0.5.1 下 tie=true post_init 崩溃在案
    "bos_token_id": 1,
    "eos_token_id": 2,
    "pad_token_id": 2,
}

# ---------------------------------------------------------------------------
# 窗语义（与 E122 必要性账仪器逐字同构 = 同卷对拍成立的前提；
# instruments: tools/analysis/cross_arch/probe_e122_deltanet_book.py
#   窗 w = corpus[w*4096 : (w+1)*4096]，utf-8 errors=replace，tokenizer 默认加
#   special tokens（Mistral 系加 BOS），截 2048）
# ---------------------------------------------------------------------------

WINDOW_BYTES = 4096
MAX_TOKENS = 2048
# fla 0.5.1 原生分块粒度：fla/ops/delta_rule/wy_fast.py:226  BT = 64（WY 表示
# 分块硬编码）；fla/layers/delta_net.py:261 chunk 模式调 chunk_delta_rule。
NATIVE_CHUNK_TOKENS = 64

# ---------------------------------------------------------------------------
# 预算与训练超参（fla 原生默认并声明出处）
# 出处 1（LR 主锚）：fla 库官方训练文档 examples/training.md
#   （github.com/fla-org/flash-linear-attention）：「By default, the learning
#   rate is set to 3e-4 with a cosine scheduler」+ from-scratch 范例
#   AdamW(eps 1e-15) / warmup 1024 / cosine(lr_min 0.1) / max_norm 1.0 /
#   skip_nan_inf / seed 42 / steps 20480（与本臂 20K 同档）。
# 出处 2（betas/weight_decay 显式声明）：flame（fla 官方训练框架，
#   torchtitan 基）预训练默认 betas (0.9, 0.95)、weight_decay 0.1。
# 任务书 §9.3 裁定：沿用 fla 原生默认并声明；发散看门狗预注册
#   （loss 上千=停，4x@2e-4 前科形态）；44M 1e-4 安全格登记备选（不降格）。
# ---------------------------------------------------------------------------

MAX_STEPS = 20_000
LEARNING_RATE = 3e-4
WARMUP_STEPS = 1024
LR_MIN_RATIO = 0.1
ADAM_BETAS = (0.9, 0.95)
ADAM_EPS = 1e-15
WEIGHT_DECAY = 0.1
GRAD_CLIP = 1.0

# 发散看门狗（任务书 §9.3 预注册：predict_loss 上千=停）
DIVERGENCE_LINE = 1000.0

# 种子纪律（任务书 §6 / E121 教训：评测种子异于训练流，异源钉死）
TRAIN_SEED = 42
EVAL_SEED = 424_242  # 仪表①②评测/手术/bootstrap 种子（bootstrap = EVAL_SEED+1）

LOG_EVERY = 20
CKPT_EVERY = 1_000
MILESTONE_STEPS = (500, 5_000, 10_000, 15_000, 20_000)


# ---------------------------------------------------------------------------
# 窗迭代与编码（训练器与锚直测共用；E122 仪器同构）
# ---------------------------------------------------------------------------


def iter_byte_windows(corpus: str | Path, window_bytes: int = WINDOW_BYTES,
                      start_window: int = 0) -> Iterator[tuple[int, bytes]]:
    """语料顺序切非重叠窗（窗 w = 字节 [w*W,(w+1)*W)）；尾窗不足整窗即停
    （E122 仪器「语料前缀尽」同款语义）。返回 (窗序号, 原始字节)。"""
    with Path(corpus).open("rb") as f:
        f.seek(start_window * window_bytes)
        w = start_window
        while True:
            raw = f.read(window_bytes)
            if len(raw) < window_bytes:
                return
            yield w, raw
            w += 1


def window_text(raw: bytes) -> str:
    """窗字节 → 文本（utf-8 errors=replace；E122 仪器同构）。"""
    return raw.decode("utf-8", errors="replace")


def lr_at(step: int) -> float:
    """fla 原生默认调度：线性 warmup → cosine 衰减到 LR_MIN_RATIO×峰值。

    step 从 0 计（step=0 时 lr=0，首次优化器 step 前按 warmup 内插）。"""
    if step < WARMUP_STEPS:
        return LEARNING_RATE * (step + 1) / WARMUP_STEPS
    t = (step - WARMUP_STEPS) / max(1, MAX_STEPS - WARMUP_STEPS)
    t = min(1.0, t)
    cos = 0.5 * (1.0 + math.cos(math.pi * t))
    return LEARNING_RATE * (LR_MIN_RATIO + (1.0 - LR_MIN_RATIO) * cos)


def is_diverged(loss: float) -> bool:
    """发散看门狗（预注册：非有限 或 >1000 → 停）。"""
    return not math.isfinite(loss) or loss > DIVERGENCE_LINE


def normalize_tied_weights_keys() -> bool:
    """tf5.15.1 兼容 shim（484c636 同款，tying 语义不变）：fla 0.5.1 的
    DeltaNetForCausalLM._tied_weights_keys 是 v4 list，而 transformers 5.15.1 的
    save_pretrained 与 from_pretrained 都无条件走 _get_tied_weight_keys
    （modeling_utils.py:382 对 list 调 .keys() 崩溃）——save/load 之前必须规范化。
    规范化目标 = 等价 dict 映射 {"lm_head.weight": "model.embeddings.weight"}。
    返回是否发生了规范化；无 fla 环境（本地单测）返回 False。"""
    try:
        import fla.models.delta_net.modeling_delta_net as _m
    except ImportError:
        return False
    if isinstance(_m.DeltaNetForCausalLM.__dict__.get("_tied_weights_keys"), list):
        _m.DeltaNetForCausalLM._tied_weights_keys = {
            "lm_head.weight": "model.embeddings.weight"
        }
        print("[r2] fla DeltaNetForCausalLM._tied_weights_keys list→dict 已规范化"
              "（tf5.15.1 save/load 兼容，tying 语义不变）")
        return True
    return False


def compute_expected_param_count(cfg: dict = R2_CONFIG) -> int:
    """解析式参数计数（fla 0.5.1 DeltaNetForCausalLM 结构的纯算术镜像；
    与实例化互证——实例化数必须等于本函数返回值 = EXPECTED_PARAM_COUNT）。"""
    hidden, heads, layers = cfg["hidden_size"], cfg["num_heads"], cfg["num_layers"]
    key_dim = int(hidden * cfg["expand_k"])
    value_dim = int(hidden * cfg["expand_v"])
    head_v = value_dim // heads
    conv_size = cfg["conv_size"] if cfg["use_short_conv"] else 0
    inter = cfg["intermediate_size"]

    emb = cfg["vocab_size"] * hidden
    head = 0 if cfg["tie_word_embeddings"] else emb

    per_layer = 0
    per_layer += hidden * key_dim          # q_proj
    per_layer += hidden * key_dim          # k_proj
    per_layer += hidden * value_dim        # v_proj
    per_layer += hidden * heads            # b_proj（use_beta=True）
    if cfg["use_short_conv"]:              # q/k/v 短卷积（无 bias）
        per_layer += (key_dim + key_dim + value_dim) * conv_size
    if cfg["use_gate"]:                    # 本臂 False 分支不进
        per_layer += hidden * value_dim
    per_layer += head_v                    # o_norm（RMSNorm(head_v_dim)）
    per_layer += value_dim * hidden        # o_proj
    per_layer += hidden                    # attn_norm
    per_layer += hidden                    # mlp_norm
    per_layer += 3 * hidden * inter        # gate/up/down proj（swiglu，无 bias）

    total = emb + head + layers * per_layer + hidden  # + final norm
    return total
