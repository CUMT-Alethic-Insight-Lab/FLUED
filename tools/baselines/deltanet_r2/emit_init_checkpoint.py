"""R2 臂初始检查点发射器：未训练 DeltaNet-50M 以 HF 格落盘（save_pretrained）。

用途：门③必要性账「起训前基线」（随机初始化直测 ≈0 族）与门⑤仪器回归需要
AutoModelForCausalLM.from_pretrained 可载的模型目录——本脚本产出之。
发射即核参数锚（≠ 48,152,896 loud fail 停报）。

Usage:
  python tools/baselines/deltanet_r2/emit_init_checkpoint.py \
      --tokenizer-path /workspace/models/delta_net-1.3B-100B \
      --out-dir outputs/r2_deltanet50m_20260913/init_50m
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import tools.baselines.deltanet_r2.r2_spec as spec


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--tokenizer-path", required=True)
    p.add_argument("--seed", type=int, default=spec.TRAIN_SEED)
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    import fla  # noqa: F401  # 注册 fla 模型类
    from fla.models.delta_net import DeltaNetConfig, DeltaNetForCausalLM

    torch.manual_seed(args.seed)
    model = DeltaNetForCausalLM(DeltaNetConfig(**spec.R2_CONFIG))
    n = sum(p.numel() for p in model.parameters())
    if n != spec.EXPECTED_PARAM_COUNT:
        raise RuntimeError(f"[r2-init] 参数锚不符：{n:,} != "
                           f"{spec.EXPECTED_PARAM_COUNT:,}——停报")
    spec.normalize_tied_weights_keys()  # save_pretrained 前置（tf5.15.1 list 崩溃在案）

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(out_dir)
    for f in ("tokenizer.json", "tokenizer.model", "tokenizer_config.json",
              "special_tokens_map.json"):
        src = Path(args.tokenizer_path) / f
        if src.exists():
            shutil.copy2(src, out_dir / f)
    (out_dir / "init_manifest.json").write_text(json.dumps({
        "param_count": n, "expected": spec.EXPECTED_PARAM_COUNT,
        "seed": args.seed, "config": spec.R2_CONFIG,
        "dtype_saved": "float32",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[r2-init] 已发射 {out_dir} params={n:,}")


if __name__ == "__main__":
    main()
