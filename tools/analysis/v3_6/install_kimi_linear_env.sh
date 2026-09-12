#!/bin/bash
# Kimi-Linear-48B-A3B-Base 仪器环境安装（AutoDL 实例 /root/miniconda3 base env；幂等）。
# 基础镜像：PyTorch 2.8.0 / Python 3.12 / CUDA 12.8（torch 已带，不动）。
set -euo pipefail
PIP=/root/miniconda3/bin/pip
PY=/root/miniconda3/bin/python

echo "[1/4] pip 升级"
$PIP install -U pip

echo "[2/4] 核心依赖（transformers pin <5：v5 _tied_weights_keys dict 化雷；fla 钉 0.4.0：完整包才有 fla.layers 且 fused_kda_gate 旧签名，见 requirements 裁定）"
$PIP install -U "transformers>=4.57.0,<5" "flash-linear-attention==0.4.0" "fla-core==0.4.0" tiktoken einops packaging accelerate

echo "[3/4] flash-attn（可选；失败不阻塞——仪器自动 SDPA 数学等价 shim；源码编译 ~30min，赶时间可 Ctrl-C 跳过）"
$PIP install flash-attn --no-build-isolation \
  || echo "[warn] flash-attn 未装成，MLA 走 SDPA shim（fingerprint 记录实际后端）"

echo "[4/4] 校验"
$PY - <<'EOF'
import torch, transformers
print("torch", torch.__version__, "| cuda_available", torch.cuda.is_available())
print("transformers", transformers.__version__)
assert transformers.__version__.startswith("4."), "transformers 必须 4.x（见 README 坑2）"
import fla
print("fla", getattr(fla, "__version__", "?"))
assert fla.__version__ == "0.4.0", "fla 必须钉 0.4.0（fused_kda_gate 签名漂移，见 requirements 裁定）"
from fla.layers.utils import get_unpad_data, index_first_axis, pad_input  # noqa: F401
print("fla.layers.utils OK")
from fla.ops.kda import chunk_kda, fused_recurrent_kda  # noqa: F401
print("fla.ops.kda OK")
from fla.ops.kda.gate import fused_kda_gate
import inspect
sig = str(inspect.signature(fused_kda_gate))
assert "g_bias" in sig, f"fused_kda_gate 签名不符（应含 g_bias）: {sig}"
print("fused_kda_gate 签名 OK:", sig)
import tiktoken
print("tiktoken OK")
EOF
echo "INSTALL_DONE"
