"""Q20 多槽读出臂温启动件 —— ridge 段 1 主方向落盘探针（E119; 任务书冻结 v1
§1 终审裁定项④: docs/versions/v3.7/FLUED_V3_7_Q20_MULTISLOT_READOUT_20260829_CN.md
「k=1 槽查询以 fuzz_id 落盘的 ridge 段 1 主方向温启动」）。

背景（施工注记补记, 2026-09-01）: 任务书假设该主方向已随 fuzz_id 产物落盘,
实测 `outputs/decoder_denoise_fuzz_id_20260829/` 只有部署桥
(bridge_{light,mid,heavy}.npz: W/scale/lam) 与残差 Cholesky
(resid_chol_*.npz: L/rho)——段 1 方向当时是在线计算的, 未落盘。本探针补建
这条产物链。

数学（ridge_unmix 的逐段读出方向, 键空间等价形）: 段 1 解混在 chunk i 的
own-chunk 回收行是 v̂_i = c_iᵀ S_i, 其中逐段 ridge 读出方向
  c_i = K_iᵀ(K_iK_iᵀ+λI)⁻¹e_i = (K_iᵀK_i+λI)⁻¹k_i,
K_i = 前 i+1 个写入键 (write_head_k gates, 单位范数行), λ=λ_unmix=1e-2
(fuzz_id 同口径)。本探针在训练流窗口 (fuzz_id F1 口径: seed=ns.seed 前 N 窗
+ 训练态掩码流) 收集全部 (窗, i, h) 的 c_i, 逐头取方向云第一主方向 (top
right singular vector, 符号对齐均值方向), 按 ||c_i|| 均值定标——t=0 读出
量级对 ridge 段 1 产出 (零变化律 t=0 ≥ 0.427 的可判读性前提)。

落盘（<out-dir>/q20_ridge_dir.npz, out-dir 默认 = fuzz_id 目录）:
  q_ridge   (H, hk) float32  逐头主方向 (均值范数定标)
  lam_unmix float64          段 1 解混 λ (1e-2)
  n_dirs    int64            方向云样本数 (Σ窗 n_real × 仅计数一次/头)
  mean_norm float64          ||c_i|| 全头全窗均值 (定标量)
  元数据进 SUMMARY.txt (基座/窗数/逐头范数统计)

Usage:
  python tools/analysis/v3_6/probe_q20_ridge_direction.py \
    --base-run-dir checkpoints/v37ks_b_sm_denoise_v2_20k_ctx4096_20260829 --device cuda
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_q20_ridge_direction.py --device cpu --max-windows 2
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    load_model,
)
from tools.analysis.v3_6.probe_decoder_fuzz_id import (  # noqa: E402
    LAM_UNMIX,
    OUT_DIR,
    build_train_masks,
    build_train_windows,
)

BASE_RUN = "checkpoints/v37ks_b_sm_denoise_v2_20k_ctx4096_20260829"  # E118 收官 (Q20 基座, 任务书 §3.1)
# 注: 写入侧在 E118 臂全程冻结, E68/E118 的 write_head_k 逐位相同——方向云取
# 自哪个基座等价; 默认取 E118 (臂的实际基座, 出处干净)。


@torch.no_grad()
def ridge_readout_directions(gates: dict, n_real: int, lam: float) -> torch.Tensor:
    """逐段 ridge 读出方向 c_i = (K_iᵀK_i + λI)⁻¹ k_i (ridge_unmix 的
    own-chunk 回收方向的键空间等价形, 推导见模块 docstring)。Returns
    (H, n_real, hk) fp32。batch-1 eval 形 (fuzz_id 探针同约定)。"""
    k = gates["k"].float()
    assert k.size(0) == 1, "eval form is batch-1"
    H, hk = k.size(2), k.size(3)
    out = []
    for h in range(H):
        K = k[0, :n_real, h]  # (n, hk), 单位范数行
        G = torch.einsum("ni,nj->nij", K, K).cumsum(dim=0)  # G_i = K_iᵀK_i
        A = G + lam * torch.eye(hk, device=K.device, dtype=torch.float32)
        c = torch.linalg.solve(A, K.unsqueeze(-1)).squeeze(-1)  # (n, hk): c_i
        out.append(c)
    return torch.stack(out)  # (H, n, hk)


@torch.no_grad()
def collect_directions(model, ns, windows, masks, device) -> list[torch.Tensor]:
    """逐窗前端 → K gates → 逐段 ridge 读出方向 (H, n, hk) 列表 (fp32 CPU)。"""
    dirs = []
    for wi, (clean, byte_mask) in enumerate(zip(windows, masks)):
        source = clean.to(device).masked_fill(byte_mask.to(device), MASK_ID)
        _chunks, _memory, index = _front_end(model, source)
        n_real = int(_chunks.chunk_mask[0].sum())
        gates_k = model.write_head_k(index.float())
        dirs.append(ridge_readout_directions(gates_k, n_real, LAM_UNMIX).cpu())
    return dirs


def principal_direction(dirs: list[torch.Tensor]) -> tuple[torch.Tensor, dict]:
    """方向云 → 逐头第一主方向: C_h (N, hk) 的 top right singular vector
    (符号对齐均值方向), 按 ||c_i|| 均值定标。Returns (q_ridge (H, hk), stats)。"""
    H = dirs[0].size(0)
    flat = torch.cat([d.permute(1, 0, 2) for d in dirs], dim=0)  # (Σn, H, hk)
    mean_norm = float(flat.norm(dim=-1).mean())
    q = torch.empty_like(dirs[0][:, 0])
    for h in range(H):
        C = flat[:, h].double()
        _u, _s, vt = torch.linalg.svd(C, full_matrices=False)
        u = vt[0].float()
        if float(u @ C.mean(dim=0).float()) < 0:
            u = -u
        q[h] = u * mean_norm
    return q, {"mean_norm": mean_norm}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--base-run-dir", default=BASE_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=32, help="训练流窗数 (fuzz_id F1 同口径默认 32)")
    p.add_argument("--out-dir", default=OUT_DIR, help="落盘目录 (默认 = fuzz_id 产物目录)")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, base_step = load_model(Path(args.base_run_dir), device)
    if getattr(ns, "k_row_source", "") != "state" or not hasattr(model, "write_head_k"):
        raise ValueError(f"{args.base_run_dir}: 预期 k_row_source='state' + write_head_k 在岗 (b 格)")
    print(f"[q20-ridge-dir] base={Path(args.base_run_dir).name} step={base_step} device={device.type}", flush=True)

    windows = build_train_windows(ns, args.max_windows)
    masks = build_train_masks(windows, ns)
    dirs = collect_directions(model, ns, windows, masks, device)
    q_ridge, st = principal_direction(dirs)
    H = q_ridge.size(0)
    norms = q_ridge.norm(dim=-1)
    print(
        f"[q20-ridge-dir] {len(dirs)} 窗方向云 Σn={sum(d.size(1) for d in dirs)} | "
        f"逐头 ||q_ridge||: {' '.join(f'{float(x):.4f}' for x in norms)} "
        f"(方向云均值范数 {st['mean_norm']:.4f})（{time.time() - t0:.0f}s）",
        flush=True,
    )

    npz_path = out_dir / "q20_ridge_dir.npz"
    np.savez(
        npz_path,
        q_ridge=q_ridge.numpy().astype(np.float32),
        lam_unmix=np.float64(LAM_UNMIX),
        n_dirs=np.int64(sum(d.size(1) for d in dirs)),
        mean_norm=np.float64(st["mean_norm"]),
    )
    summary = [
        "Q20 多槽读出臂温启动件 —— ridge 段 1 主方向（任务书冻结 v1 §1 终审裁定项④）",
        f"日期 {time.strftime('%Y-%m-%d %H:%M:%S')}  设备 {device.type}",
        f"基座 {Path(args.base_run_dir).name} (step {base_step}) | 训练流窗 {len(dirs)} (fuzz_id F1 口径) | λ_unmix={LAM_UNMIX}",
        f"方向云: Σn={sum(d.size(1) for d in dirs)} 段 × {H} 头 | 均值范数 {st['mean_norm']:.4f}",
        f"逐头 ||q_ridge||: {' '.join(f'{float(x):.4f}' for x in norms)}",
        f"落盘: {npz_path} (q_ridge (H,hk) + lam_unmix + n_dirs + mean_norm)",
    ]
    (out_dir / "q20_ridge_dir_SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary), flush=True)


if __name__ == "__main__":
    main()
