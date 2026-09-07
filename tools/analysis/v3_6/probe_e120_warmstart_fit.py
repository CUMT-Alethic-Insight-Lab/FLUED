"""E120 端到端点燃臂 —— d 格闭式温启动拟合 + t=0 仪器（9/03 晚预跑, 用户已批准;
任务书: docs/versions/v3.7/FLUED_V3_7_E120_END_TO_END_IGNITION_20260903_CN.md
§1 构造设计 + §3 冒烟四条款（t=0 仪器定义）+ §4 修订 v2 拟合预跑条款）。

两件产物, 同一批训练窗（对齐是硬要求, 明天冒烟直接复用）:
  (A) 闭式温启动拟合（fuzz_id 同款流程的 d 格版, 全闭式无梯度）:
      段1: V 通道 gates（write_head(memory)）的 KDA 自然态（trained_states
           fp32 参考递推, Q19 natural 列同通道）--ridge 解混(λ_unmix=1e-2,
           fuzz_id/Q19/E73 同档)--> v̂（写入内容估计, H*hv=1024 维）
      段2: v̂ --ridge 部署桥(λ_bridge=1.0, fuzz_id/Q19 λ_opt 同档)--> 生产
           读出行空间（桥目标 = 同基座同窗 readout_query/realign 自产生产行
           read_trained(state_machine, S_nat)→mean(nq), d_pack=1536 维）——
           把闭式内容方向映射进主干熟悉的行空间（E120 插入点 = 替换生产读出）。
      分窗 2-fold held-out 口径（统计主体）+ 全窗部署桥落盘（装载件, F4 两列分清）。
  (B) t=0 仪器（任务书 §3 冒烟条款修订 v2 钉死）: fuzz_id 家族线性字节探针——
      同一批训练窗上拟合「读出行→逐段字节内容」线性解码器（byte_probe, E73 A6
      同款闭式）; 在同一批窗上测 ridge 闭式行（held-out 桥映射行）的可解码率
      作为参照带基尺落盘——明天冒烟判读基尺 = 此值 −3pp。

基座 = v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b（Q15 收官正臂; 任务书
修订 v2 钉死, 无 b 的是 512B off-spec pilot 禁混排）。d 格: k/v_row_source
均为 state, 生产读出 = V 通道 state_machine 的 readout_query(nq=1, H=4, hk=128)
→ realign(LayerNorm(H*hv=1024) → Linear(1024→1536) → SiLU → Linear(1536→1536))
→ package (B,C,nq,d_pack) → v_rows = mean(nq) = backbone store V 行
（_slm_store_rows; direct 口经 decoder_in, 无 decoder_in_mem——结构在案）。

已申报口径偏差（不静默, fuzz_id F 系形态）:
  F1. 窗口 = fuzz_id F1 同款训练流窗构造（StreamingReconstructionDataset
      seed=42 前 32 窗 + 训练态掩码流复演）; 不含训练批循环层的 burst 拼接
      （_splice_burst 在批循环, 本基座 burst_prob=0.5; Q19 D2 同族口径差）。
      data_path 显式覆写为远端同语料路径（resolved_config 内是 Windows 盘
      路径, 远端跑必须 --data-path 覆写; 语料同源 corpus_v3.txt）。
  F2. 段1 解混通道 = d 格 V 通道（Q19 natural 列同通道同 λ）; K 通道
      （state_machine_k）不在本拟合作用域——E120 插入点 = 生产读出（V 通道）
      的行集, 温启动只换读出不动 K。
  F3. 桥目标 = 同基座同窗自产生产读出行 read_trained(state_machine, S_nat)
      →mean(nq)（fp32-manual 口径, E73 A1 同函数）; 窗 0 与 native
      _slm_store_rows（kda_impl 原样, cuda 上走 fla+amp）的逐位差落盘备查。
  F4. 统计主体 = 分窗 2-fold held-out（ridge_fit_predict 同函数）; 全窗部署
      桥单独落盘供训练器装载（fuzz_id F4 两列分清）。参照带基尺 byte_probe
      在 held-out 桥映射行上测（byte_probe 自带 2-fold, 无窗级泄漏）。
  F5. 部署探针 W = byte_probe 同闭式形态（截距 + λ=1.0, 258 维 onehot
      clamp）在 held-out 桥映射行全池拟合落盘; 一切 acc 读数全部出自
      byte_probe, 零新造打分逻辑。λ_bridge=1.0 系申报口径（fuzz_id/Q19
      λ_opt 同档; 任务书未钉死桥 λ）。

输出（outputs/e120_warmstart_fit_20260903/）:
  bridge_deploy.npz   部署桥 W（含截距行）/scale/lam + 两折 W 备查
                      （键形对应 b 格 bridge_*.npz: W/scale/lam, 但全部 d 格自产）
  q_ridge_dir.npz     段1 逐头主方向 q_ridge (H, hk) + lam_unmix/n_dirs/
                      mean_norm（键形对应 b 格 q20_ridge_dir.npz: q_ridge）
  probe_t0.npz        t=0 仪器部署件: 逐槽线性字节探针 W（held-out 桥映射行
                      全池拟合主件 W_probe + 生产行对照件 W_probe_prod）
  e120_warmstart_fit.json + SUMMARY.txt（段1 解混 cos / 桥拟合优度 / held-out
                      差 / 探针参照带读数 / n·种子·口径申报）

Usage:
  python tools/analysis/v3_6/probe_e120_warmstart_fit.py --device cuda \
    --data-path /workspace/corpus/corpus_v3.txt
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_e120_warmstart_fit.py \
    --device cpu --max-windows 2
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    byte_probe,
    load_model,
    read_trained,
    ridge_unmix,
    trained_states,
)
from tools.analysis.v3_6.probe_closed_form_readout import (  # noqa: E402
    ridge_fit_predict,
    row_cos,
)
from tools.analysis.v3_6.probe_decoder_fuzz_id import (  # noqa: E402
    LAM_UNMIX,
    apply_bridge,
    build_train_masks,
    build_train_windows,
    ridge_fit_all,
)
from tools.analysis.v3_6.probe_q20_ridge_direction import (  # noqa: E402
    principal_direction,
    ridge_readout_directions,
)

BASE_RUN = "checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b"  # E120 基座（修订 v2 钉死 25b）
OUT_DIR = "outputs/e120_warmstart_fit_20260903"
LAM_BRIDGE = 1.0  # 部署桥 ridge λ（fuzz_id/Q19 λ_opt 同档, F5 申报）
PROBE_SLOTS = 4  # 逐槽字节探针槽数（E73 A6 / Q19 同款 0-3）
PROBE_N_MIN = 40  # byte_probe 的槽样本下限（同款阈值, 部署 W 落盘同口径）

DECLARED_DEVIATIONS = [
    "F1: 窗口 = fuzz_id F1 同款训练流窗构造（seed=42 前 N 窗 + 训练态掩码流复演）; 不含训练"
    "批循环层的 burst 拼接（_splice_burst 在批循环, 本基座 burst_prob=0.5, Q19 D2 同族口径差）; "
    "data_path 显式覆写为远端同语料路径（resolved_config 内是 Windows 盘路径）。",
    "F2: 段1 解混通道 = d 格 V 通道（write_head(memory) gates 自然态, Q19 natural 列同通道同 λ）"
    "; K 通道（state_machine_k）不在作用域——E120 插入点 = 生产读出（V 通道 readout_query/realign）行集。",
    "F3: 桥目标 = 同基座同窗自产生产读出行 read_trained(state_machine, S_nat)→mean(nq)（fp32-manual"
    " 口径, E73 A1 同函数）; 窗 0 与 native _slm_store_rows（kda_impl 原样）逐位差落盘备查。",
    "F4: 统计主体 = 分窗 2-fold held-out（ridge_fit_predict 同函数）; 全窗部署桥单独落盘（fuzz_id F4"
    " 两列分清）。参照带基尺 = byte_probe 在 held-out 桥映射行上的 2-fold acc（无窗级泄漏）。",
    "F5: 部署探针 W = byte_probe 同闭式形态（截距+λ=1.0, onehot 258 clamp）全池拟合落盘; acc 读数"
    "全出 byte_probe, 零新造打分逻辑。λ_bridge=1.0 系申报口径（fuzz_id/Q19 λ_opt 同档; 任务书未钉死桥 λ）。",
]


# ---------------------------------------------------------------------------
# 逐窗采集: 前端 → V gates → 自然态 → 段1 解混 + 生产读出行 + 逐槽字节目标
# ---------------------------------------------------------------------------


@torch.no_grad()
def collect_window(model, ns, clean, byte_mask, device, wi):
    source = clean.masked_fill(byte_mask, MASK_ID)
    chunks, memory, _index = _front_end(model, source)
    n_real = int(chunks.chunk_mask[0].sum())
    gates_v = model.write_head(memory)  # V 通道 gates（d 格, F2）
    S_nat = trained_states(model.state_machine, gates_v, n_real)  # KDA 自然态 fp32 参考
    vh, cos_unmix = ridge_unmix(gates_v, S_nat, LAM_UNMIX)  # 段1: (1, n, H*hv)
    v_rows = read_trained(model.state_machine, S_nat)  # 生产读出行 (1, n, d_pack), F3

    # 窗 0 在岗断言: 手工生产读出行 vs native _slm_store_rows（kda_impl 原样）
    native_diff = None
    if wi == 0:
        native = model._slm_store_rows(chunks)[1][:, :n_real]
        native_diff = round(float((v_rows - native.float()).abs().max()), 6)
        print(f"[e120-wf] sanity window0: read_trained vs native v_rows max|Δ|={native_diff}", flush=True)

    # 逐槽字节探针目标（E73 A6 同款: clean 字节, slots 0-3）
    zeros = torch.zeros_like(byte_mask)
    base_targets, base_slot, _bm = s1.make_targets(
        clean, zeros, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    ys = base_targets[0, :n_real, :PROBE_SLOTS].cpu()
    y_valid = base_slot[0, :n_real, :PROBE_SLOTS].cpu()

    # 段1 ridge 读出方向云（q20_ridge_dir 同函数, V 通道 gates）
    dirs = ridge_readout_directions(gates_v, n_real, LAM_UNMIX).cpu()  # (H, n, hk)

    return {
        "window": wi,
        "n_real": n_real,
        "cos_unmix": round(cos_unmix, 4),
        "native_diff": native_diff,
        "vh": vh[0].float().cpu(),  # (n, H*hv)
        "v_rows": v_rows[0, :n_real].float().cpu(),  # (n, d_pack)
        "ys": ys,
        "y_valid": y_valid,
        "dirs": dirs,
    }


# ---------------------------------------------------------------------------
# t=0 仪器部署件: byte_probe 同闭式形态的全池拟合（F5, 只补 W 不改打分）
# ---------------------------------------------------------------------------


def fit_probe_deploy(X: torch.Tensor, ys: torch.Tensor, y_valid: torch.Tensor, lam: float = 1.0):
    """逐槽 one-vs-all ridge 线性字节探针的全池（全窗）拟合——闭式形态与
    byte_probe 内层逐位同款（截距 + λ、onehot(y.clamp(0,257), 258)、n<40 跳槽）,
    只是不分折（部署件标准做法, fuzz_id F4 同纪律）。Returns {slot: W (F+1, 258)}。"""
    out = {}
    for s in range(ys.size(1)):
        m = y_valid[:, s]
        x, y = X[m].float(), ys[m][:, s].long()
        n = x.size(0)
        if n < PROBE_N_MIN:
            continue
        x1 = torch.cat([x, torch.ones(n, 1)], dim=1)
        y1 = F.one_hot(y.clamp(min=0, max=257), 258).float()
        W = torch.linalg.solve(x1.T @ x1 + lam * torch.eye(x1.size(1)), x1.T @ y1)
        out[s] = W
    return out


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--base-run-dir", default=BASE_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=32, help="训练流窗数（fuzz_id F1 同口径默认 32）")
    p.add_argument("--data-path", default=None, help="语料路径覆写（远端跑必须: resolved_config 内是 Windows 盘路径）")
    p.add_argument("--out-dir", default=OUT_DIR)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, base_step = load_model(Path(args.base_run_dir), device)
    if args.data_path:
        ns.data_path = args.data_path  # F1: 语料路径覆写（窗流构造不变）
    # 接口断言（loud）: d 格 k/v 双状态机 + 生产读出在岗
    if getattr(ns, "backbone_mode", "") != "slm" or getattr(ns, "v_row_source", "") != "state":
        raise ValueError(f"{args.base_run_dir}: 预期 slm d 格 v_row_source='state', got {ns.v_row_source!r}")
    if getattr(ns, "k_row_source", "") != "state" or not hasattr(model, "state_machine_k"):
        raise ValueError(f"{args.base_run_dir}: 预期 k_row_source='state' + state_machine_k 在岗")
    if getattr(ns, "recurrence", "kda") != "kda":
        raise ValueError(f"{args.base_run_dir}: recurrence={ns.recurrence!r} != 'kda'")
    if not all(hasattr(model, a) for a in ("write_head", "state_machine")) or not hasattr(
        model.state_machine, "readout_query"
    ):
        raise ValueError(f"{args.base_run_dir}: V 通道 write_head/state_machine(+readout_query) 缺件")
    c = model.config
    dims = {
        "kda_heads": c.kda_heads,
        "kda_head_k": c.kda_head_k,
        "kda_head_v": c.kda_head_v,
        "hv_flat": c.kda_heads * c.kda_head_v,
        "d_pack": c.d_pack,
        "readout_queries": c.readout_queries,
    }
    print(
        f"[e120-wf] base={Path(args.base_run_dir).name} step={base_step} device={device.type} "
        f"seed={ns.seed} dims={dims} data={ns.data_path}",
        flush=True,
    )

    windows = build_train_windows(ns, args.max_windows)
    masks = build_train_masks(windows, ns)
    print(f"[e120-wf] {len(windows)} 训练流窗 + 训练态掩码就位（{time.time() - t0:.0f}s）", flush=True)

    recs = []
    for wi, (clean, byte_mask) in enumerate(zip(windows, masks)):
        recs.append(collect_window(model, ns, clean.to(device), byte_mask.to(device), device, wi))
        print(
            f"[e120-wf] window {wi} n_real={recs[-1]['n_real']} cos_unmix={recs[-1]['cos_unmix']:.3f}"
            f"（{time.time() - t0:.0f}s）",
            flush=True,
        )
    n_win = len(recs)
    vh_by_win = [r["vh"] for r in recs]
    vr_by_win = [r["v_rows"] for r in recs]
    cos_unmix_mean = round(sum(r["cos_unmix"] for r in recs) / n_win, 4)

    # (A) 部署桥: 分窗 2-fold held-out（统计主体）+ 全窗部署桥（装载件, F4）
    preds, folds = ridge_fit_predict(vh_by_win, vr_by_win, LAM_BRIDGE)
    cos_ho = [row_cos(preds[i], vr_by_win[i]) for i in range(n_win)]
    cos_heldout = round(sum(cos_ho) / n_win, 4)
    cos_heldout_std = round(float(np.std(cos_ho)), 4)
    W_all, scale_all = ridge_fit_all(vh_by_win, vr_by_win, LAM_BRIDGE)
    # 全窗桥逐窗自映射 cos（在岗对照, 不作统计主体）
    cos_in = [
        row_cos(apply_bridge(vh_by_win[i], W_all, scale_all), vr_by_win[i]) for i in range(n_win)
    ]
    cos_insample = round(sum(cos_in) / n_win, 4)

    # (B) t=0 仪器: byte_probe 三读数（同一批窗; acc 全出 byte_probe）
    ys_all = torch.cat([r["ys"] for r in recs])
    yv_all = torch.cat([r["y_valid"] for r in recs])
    mapped_ho = torch.cat([preds[i] for i in range(n_win)])  # held-out 桥映射行（参照带对象）
    bp_mapped = byte_probe(mapped_ho, ys_all, yv_all)  # ← 参照带基尺（F4）
    bp_vh = byte_probe(torch.cat(vh_by_win), ys_all, yv_all)  # 段1 产物（桥前, 诊断）
    bp_prod = byte_probe(torch.cat(vr_by_win), ys_all, yv_all)  # 生产行对照（在岗上限参照）

    # 部署探针 W（byte_probe 同闭式形态全池拟合, F5）
    W_probe = fit_probe_deploy(mapped_ho, ys_all, yv_all)
    W_probe_prod = fit_probe_deploy(torch.cat(vr_by_win), ys_all, yv_all)

    # 段1 主方向（q20_ridge_dir 同款, V 通道）
    dirs = [r["dirs"] for r in recs]
    q_ridge, dir_stats = principal_direction(dirs)
    n_dirs = int(sum(d.size(1) for d in dirs))

    # 落盘
    np.savez(
        out_dir / "bridge_deploy.npz",
        W=W_all.numpy().astype(np.float32),
        scale=np.float64(scale_all),
        lam=np.float64(LAM_BRIDGE),
        W_fold0=folds[0]["W"].numpy().astype(np.float32),
        scale_fold0=np.float64(folds[0]["scale"]),
        W_fold1=folds[1]["W"].numpy().astype(np.float32) if len(folds) > 1 else folds[0]["W"].numpy().astype(np.float32),
        scale_fold1=np.float64(folds[1]["scale"] if len(folds) > 1 else folds[0]["scale"]),
    )
    np.savez(
        out_dir / "q_ridge_dir.npz",
        q_ridge=q_ridge.numpy().astype(np.float32),
        lam_unmix=np.float64(LAM_UNMIX),
        n_dirs=np.int64(n_dirs),
        mean_norm=np.float64(dir_stats["mean_norm"]),
    )
    probe_slots = sorted(W_probe.keys())
    np.savez(
        out_dir / "probe_t0.npz",
        probe_slots=np.array(probe_slots, dtype=np.int64),
        W_probe=np.stack([W_probe[s] for s in probe_slots]).astype(np.float32),
        W_probe_prod=np.stack([W_probe_prod[s] for s in sorted(W_probe_prod.keys())]).astype(np.float32),
        probe_slots_prod=np.array(sorted(W_probe_prod.keys()), dtype=np.int64),
        lam=np.float64(1.0),
        feature_space=np.array("bridge_mapped_heldout"),  # W_probe 的特征空间标注
    )

    def _probe_brief(bp: dict) -> str:
        return " ".join(
            f"s{s}: acc={v['acc']:.4f}/maj={v['majority']:.4f}/n={v['n']}" for s, v in sorted(bp.items(), key=lambda kv: int(kv[0]))
        )

    ref_slot = "0"
    ref_acc = bp_mapped.get(ref_slot, {}).get("acc")
    ref_line = (
        f"参照带基尺（s{ref_slot}, byte_probe@held-out 桥映射行）: acc={ref_acc}"
        f" → 明天冒烟判读线 = {round(ref_acc - 0.03, 4) if ref_acc is not None else 'N/A'}（基尺 −3pp）"
        if ref_acc is not None
        else "参照带基尺: slot0 缺样本（n<40）, 看 json 逐槽表"
    )

    stats = {
        "probe": "E120 端到端点燃臂预跑 —— d 格闭式温启动拟合 + t=0 仪器",
        "spec": "docs/versions/v3.7/FLUED_V3_7_E120_END_TO_END_IGNITION_20260903_CN.md",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "base": {"run": Path(args.base_run_dir).name, "step": base_step, "seed": int(ns.seed)},
        "declared_deviations": DECLARED_DEVIATIONS,
        "dims": dims,
        "params": {
            "windows": n_win,
            "seed": int(ns.seed),
            "lam_unmix": LAM_UNMIX,
            "lam_bridge": LAM_BRIDGE,
            "probe_slots": PROBE_SLOTS,
            "data_path": ns.data_path,
            "stream": "train (seed=42 训练流窗 + 训练态掩码流, fuzz_id F1 构造; 无 burst 拼接, F1 申报)",
        },
        "stage1_unmix": {
            "cos_mean": cos_unmix_mean,
            "cos_per_window": [r["cos_unmix"] for r in recs],
            "n_rows": int(sum(r["n_real"] for r in recs)),
        },
        "bridge": {
            "lam": LAM_BRIDGE,
            "cos_heldout_mean": cos_heldout,
            "cos_heldout_std": cos_heldout_std,
            "cos_heldout_per_window": [round(x, 4) for x in cos_ho],
            "cos_insample_mean": cos_insample,
            "scale": round(scale_all, 6),
            "n_rows": int(sum(r["n_real"] for r in recs)),
            "note": "held-out = 分窗 2-fold（统计主体）; in-sample = 全窗桥自映射（在岗对照）; 部署件 = 全窗桥",
        },
        "t0_probe": {
            "ref_band_baseline": bp_mapped,
            "ref_band_note": "参照带基尺 = byte_probe@held-out 桥映射行（F4）; 判读线 = slot0 acc −3pp",
            "stage1_rows": bp_vh,
            "prod_rows": bp_prod,
            "deploy_slots": probe_slots,
        },
        "q_ridge": {
            "n_dirs": n_dirs,
            "mean_norm": round(dir_stats["mean_norm"], 6),
            "per_head_norm": [round(float(x), 6) for x in q_ridge.norm(dim=-1)],
        },
        "native_parity_window0": recs[0]["native_diff"],
        "per_window": [
            {"window": r["window"], "n_real": r["n_real"], "cos_unmix": r["cos_unmix"]} for r in recs
        ],
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "e120_warmstart_fit.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "E120 端到端点燃臂预跑 —— d 格闭式温启动拟合 + t=0 仪器（9/03 晚预跑）",
        f"日期 {stats['created']}  设备 {device.type}  训练流窗 {n_win}（fuzz_id F1 构造, seed={ns.seed}）",
        f"基座 {Path(args.base_run_dir).name} (step {base_step}) | λ_unmix={LAM_UNMIX} λ_bridge={LAM_BRIDGE}",
        f"维度: H={dims['kda_heads']} hk={dims['kda_head_k']} hv={dims['kda_head_v']} → "
        f"v̂ {dims['hv_flat']} 维 → 桥 → 生产行空间 d_pack={dims['d_pack']}（nq={dims['readout_queries']}）",
        f"行数: Σn_real={stats['stage1_unmix']['n_rows']} | 窗0 native 位差 max|Δ|={recs[0]['native_diff']}",
        "",
        "已申报口径偏差（不静默）:",
        *[f"  {d}" for d in DECLARED_DEVIATIONS],
        "",
        "== (A) 闭式温启动拟合 ==",
        f"  段1 解混 cos(v̂,v)（V 通道自然态, Q19 natural 列同口径）: 逐窗均值 {cos_unmix_mean}"
        f"（E73 oracle 态 ≈1 / b 格 fuzz_id 0.699 为跨格参照, 不可直接比）",
        f"  部署桥（v̂ → 生产读出行空间）held-out cos: {cos_heldout} ± {cos_heldout_std}"
        f"（分窗 2-fold, 统计主体）| 全窗桥自映射 cos {cos_insample}（在岗对照）",
        "",
        "== (B) t=0 仪器（fuzz_id 家族线性字节探针, acc 全出 byte_probe）==",
        f"  {ref_line}",
        f"  参照带（held-out 桥映射行, 逐槽）: {_probe_brief(bp_mapped)}",
        f"  段1 行桥前（诊断）: {_probe_brief(bp_vh)}",
        f"  生产行对照（在岗上限参照）: {_probe_brief(bp_prod)}",
        f"  段1 主方向: n_dirs={n_dirs} 均值范数 {dir_stats['mean_norm']:.4f} "
        f"逐头 ||q_ridge||: {' '.join(f'{x:.4f}' for x in stats['q_ridge']['per_head_norm'])}",
        "",
        "落盘件（键形对应 b 格装载形态, 全部 d 格自产——域移纪律: 不含任何 E118 b 格张量）:",
        "  bridge_deploy.npz (W/scale/lam + 两折备查), q_ridge_dir.npz (q_ridge/lam_unmix/n_dirs/mean_norm),",
        "  probe_t0.npz (逐槽探针 W: W_probe=桥映射行件[主] / W_probe_prod=生产行件[对照])",
        f"完整数据: {out_dir / 'e120_warmstart_fit.json'}",
    ]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
