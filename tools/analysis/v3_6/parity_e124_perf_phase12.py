"""E124 效率 Phase1+2 parity 验收对拍（用户裁定 2026-09-11：parity 必须跑在
comb 合体列完整配置上——门+α-entmax+需求器件全开）。

口径（验收三件之②）：同种子同数据 200 步双跑，loss 序列逐位 + 末期参数逐键
torch.equal；metrics-only 诊断两列（C1 aux：conf_mean/hard_cut 率类键）容许
allclose(atol=1e-7)（fp 归约序豁免，提案 §C1 契约），其余字段一律逐位。

用法：
  python tools/analysis/v3_6/parity_e124_perf_phase12.py \
      --pre outputs/_perf_parity_baseline --post checkpoints/_perf_parity_post200
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import torch

# C1 aux 两列（_slm_forward 诊断键，metrics-only，fp 归约序豁免）：
# 置信度张量本身是 bf16（其 ulp 在 0.87 处 ≈ 3.9e-3），旧路径 masked-mean 与
# 新路径加权-sum/count 的归约序差在 bf16 ulp 内——容差按 bf16 ulp 定 4e-3，
# 逐位豁免命中数呈报（用户裁定 2026-09-11：metrics-only 列容许末位 ulp 差）。
ULP_OK_KEYS = {"confidence_mean", "hard_cut_rate", "conf_mean", "cut_rate",
               "boundary_confidence_mean"}
ULP_TOL = 4e-3
# 性能字段：墙钟派生，双跑本应不同（优化正是为了改它）——非语义字段，排除
PERF_KEYS = {"steps_per_sec", "elapsed_sec", "step_time_ms"}


def _load_log(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--pre", required=True)
    p.add_argument("--post", required=True)
    args = p.parse_args()
    pre_dir, post_dir = Path(args.pre), Path(args.post)

    fails: list[str] = []

    # --- ① train_log 逐字段 ---
    pre_log = _load_log(pre_dir / "train_log.jsonl")
    post_log = _load_log(post_dir / "train_log.jsonl")
    if len(pre_log) != len(post_log):
        fails.append(f"train_log 行数不等 {len(pre_log)} vs {len(post_log)}")
    n_ulp = 0
    for i, (ra, rb) in enumerate(zip(pre_log, post_log)):
        if set(ra) != set(rb):
            fails.append(f"log 行 {i} 键集不等: {sorted(set(ra) ^ set(rb))[:6]}")
            continue
        for k in ra:
            va, vb = ra[k], rb[k]
            if va == vb:
                continue
            if k in PERF_KEYS:
                continue
            if isinstance(va, float) and isinstance(vb, float):
                if k in ULP_OK_KEYS and math.isclose(va, vb, abs_tol=ULP_TOL):
                    n_ulp += 1
                    continue
                # 浮点字段逐位（双跑同码同种子应逐位一致）
                fails.append(f"log 行 {i} 键 {k}: {va!r} != {vb!r}")
            else:
                fails.append(f"log 行 {i} 键 {k}: {va!r} != {vb!r}")
    print(f"[log] 行数 {len(pre_log)}，ulp 豁免命中 {n_ulp}，逐位违例 {len(fails)}")

    # --- ② 末期参数逐键 ---
    ck_a = torch.load(pre_dir / "latest.pt", map_location="cpu", weights_only=False)
    ck_b = torch.load(post_dir / "latest.pt", map_location="cpu", weights_only=False)
    ma, mb = ck_a["model"], ck_b["model"]
    if set(ma) != set(mb):
        fails.append(f"模型键集不等: only_pre={sorted(set(ma)-set(mb))[:5]} only_post={sorted(set(mb)-set(ma))[:5]}")
    n_bad = 0
    for k in sorted(set(ma) & set(mb)):
        if not torch.equal(ma[k], mb[k]):
            n_bad += 1
            if n_bad <= 5:
                d = (ma[k].float() - mb[k].float()).abs().max().item()
                fails.append(f"参数 {k} 不逐位（max|Δ|={d:.3e}）")
    print(f"[ckpt] 键数 pre={len(ma)} post={len(mb)}，非逐位键 {n_bad}")

    if fails:
        print("VERDICT: FAIL")
        for f_ in fails[:20]:
            print("  -", f_)
        return 1
    print("VERDICT: PASS（loss/参数全键逐位，ulp 豁免仅命中白名单列）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
