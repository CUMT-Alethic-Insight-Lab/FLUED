"""E124 仓内 entmax_bisect vs 官方 entmax 包 一次性数值对拍（任务书冻结 v1.0 §6
施工可行性定论①：仓内实现，零新依赖——官方包只装在 _pkg 临时目录供本对拍，
不进项目依赖、不进训练/测试 env；仓内测试 tests/test_e124_entmax.py 自包含）。

对拍面：输出值 / dL/dz / dL/dα（官方包 backward 支持 α 梯度，Correia et al.
2019）；网格 = α ∈ {1.2, 1.5, 2.0, 3.0} × dtype {fp32, fp64} × 遮蔽 {无, -inf
遮蔽} × 随机形状。产物：同目录 parity_report.json + 本脚本。

用法（训练 env python）：
  python tools/analysis/v3_6/e124_entmax_parity_check.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import torch  # 先载 env 的 torch（sys.modules 缓存优先于下面的 _pkg 路径）

_PKG = str(Path(__file__).resolve().parents[3] / "outputs" / "e124_entmax_parity" / "_pkg")
sys.path.append(_PKG)  # append 不 prepend：torch 已缓存，只有 entmax 从这里解析

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

from entmax import entmax_bisect as ref_entmax_bisect  # noqa: E402  官方参照
from flued.v36.sparsemap import entmax_bisect as ours_entmax_bisect  # noqa: E402


def _rand(*shape, seed: int, scale: float = 3.0, dtype=torch.float64):
    g = torch.Generator().manual_seed(seed)
    return torch.randn(*shape, generator=g, dtype=dtype) * scale


def main() -> None:
    torch.manual_seed(0)
    cases = []
    worst = {"out": 0.0, "dz": 0.0, "da": 0.0}
    seed = 100
    for alpha_v in (1.2, 1.5, 2.0, 3.0):
        for dtype in (torch.float32, torch.float64):
            for masked in (False, True):
                for shape in ((7, 23), (2, 3, 17)):
                    seed += 1
                    z0 = _rand(*shape, seed=seed, dtype=dtype)
                    if masked:
                        z0[..., : max(1, shape[-1] // 3)] = float("-inf")
                    w = _rand(*shape, seed=seed + 5000, scale=1.0, dtype=dtype)
                    # --- 输出对拍 ---
                    p_ref = ref_entmax_bisect(z0, alpha_v)
                    p_our = ours_entmax_bisect(z0, alpha_v)
                    d_out = float((p_ref - p_our).abs().max())
                    # --- dL/dz 对拍（同一上游梯度 w）---
                    zr = z0.clone().requires_grad_(True)
                    zo = z0.clone().requires_grad_(True)
                    (ref_entmax_bisect(zr, alpha_v) * w).sum().backward()
                    (ours_entmax_bisect(zo, alpha_v) * w).sum().backward()
                    d_dz = float((zr.grad - zo.grad).abs().max())
                    # --- dL/dα 对拍（α 可学，同一上游梯度）---
                    ar = torch.tensor(alpha_v, dtype=dtype, requires_grad=True)
                    ao = torch.tensor(alpha_v, dtype=dtype, requires_grad=True)
                    (ref_entmax_bisect(z0, ar) * w).sum().backward()
                    (ours_entmax_bisect(z0, ao) * w).sum().backward()
                    d_da = float(abs(ar.grad.item() - ao.grad.item()))
                    cases.append({
                        "alpha": alpha_v, "dtype": str(dtype).split(".")[-1],
                        "masked": masked, "shape": list(shape),
                        "max_abs_out": d_out, "max_abs_dz": d_dz, "abs_dalpha": d_da,
                    })
                    worst["out"] = max(worst["out"], d_out)
                    worst["dz"] = max(worst["dz"], d_dz)
                    worst["da"] = max(worst["da"], d_da)
    tol = {"float32": 2e-5, "float64": 1e-12}
    fails = [c for c in cases
             if c["max_abs_out"] > tol[c["dtype"]] or c["max_abs_dz"] > tol[c["dtype"]]
             or c["abs_dalpha"] > (1e-4 if c["dtype"] == "float32" else 1e-10)]
    report = {
        "ref": "entmax==1.3 (pip --target outputs/e124_entmax_parity/_pkg，隔离目录)",
        "ours": "flued/v36/sparsemap.py::entmax_bisect",
        "n_cases": len(cases), "worst": worst, "tolerance": tol,
        "pass": not fails, "fails": fails, "cases": cases,
        "torch": torch.__version__,
    }
    out = Path(__file__).resolve().parents[3] / "outputs" / "e124_entmax_parity" / "parity_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"n_cases": len(cases), "worst": worst, "pass": not fails,
                      "report": str(out)}, ensure_ascii=False), flush=True)
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
