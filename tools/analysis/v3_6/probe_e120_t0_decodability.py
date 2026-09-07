"""E120 端到端点燃臂 —— t=0 零变化律检查件（任务书 §3 冒烟条款修订 v2 钉死:
docs/versions/v3.7/FLUED_V3_7_E120_END_TO_END_IGNITION_20260903_CN.md）。

测温启动读出行（t=0, 训练前）的逐段字节可解码率: 基座模型 + 探针侧接线
（E120WarmReadout 温启动 + config 开关走生产拼接点 _slm_store_rows）→ 与
预跑（probe_e120_warmstart_fit.py）同一批训练流窗上, 用落盘部署探针
（probe_t0.npz 键 W_probe, byte_probe 同闭式形态全池拟合）逐槽解码行字节,
判读线 = 参照带基尺（e120_warmstart_fit.json 键 t0_probe.ref_band_baseline
槽 0 acc, 预跑落盘 0.6078）−3pp = **0.5778**——slot0 acc ≥ 判读线 = 过线
（主判据槽 0; 其余槽只报告不作门）。生产行对照（W_probe_prod × 被替换的
生产读出行 read_trained）一并报告作在岗上限参照, 不作门。

零新造打分逻辑: 解码 = [row, 1] @ W 的 argmax（fit 脚本 fit_probe_deploy
的部署件应用形）; acc 口径、窗构造（build_train_windows/build_train_masks,
fuzz_id F1 同款）与预跑逐一对齐。

Usage（冒烟时接在点火前）:
  python tools/analysis/v3_6/probe_e120_t0_decodability.py --device cuda \
    --data-path /workspace/corpus/corpus_v3.txt
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_e120_t0_decodability.py \
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

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from flued.v36.model import E120WarmReadout  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    load_model,
    read_trained,
    trained_states,
)
from tools.analysis.v3_6.probe_decoder_fuzz_id import (  # noqa: E402
    build_train_masks,
    build_train_windows,
)

BASE_RUN = "checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b"  # E120 基座（修订 v2 钉死 25b）
FIT_DIR = "outputs/e120_warmstart_fit_20260903"
OUT_DIR = "outputs/e120_t0_check_20260903"
JUDGE_MARGIN = 0.03  # 判读线 = 基尺 −3pp（任务书 §3 修订 v2）
PROBE_SLOTS = 4  # 逐槽字节目标槽数（预跑同款 0-3）
REF_SLOT = "0"  # 主判据槽（预跑参照带基尺所在槽）


def judgment_line(baseline_acc: float) -> float:
    """判读线 = 参照带基尺 −3pp（round 4 位, 预跑 SUMMARY 同形）。"""
    return round(float(baseline_acc) - JUDGE_MARGIN, 4)


def load_deploy_probe(fit_dir: str | Path) -> tuple[list[int], torch.Tensor, torch.Tensor, float]:
    """装载 t=0 仪器部署件: Returns (slots, W_probe (S, F+1, 258) 主件,
    W_probe_prod (S', F+1, 258) 生产行对照件, 基尺 acc)。缺件/缺键响亮报错。"""
    fit = Path(fit_dir)
    ppath = fit / "probe_t0.npz"
    if not ppath.exists():
        raise SystemExit(f"[e120-t0] t=0 探针部署件缺席: {ppath}")
    z = np.load(ppath)
    for key in ("probe_slots", "W_probe", "W_probe_prod"):
        if key not in z:
            raise SystemExit(f"[e120-t0] {ppath}: 缺 {key} 键 (实际键集 {list(z.keys())})")
    slots = [int(s) for s in z["probe_slots"]]
    W_probe = torch.from_numpy(np.asarray(z["W_probe"], dtype=np.float32))
    W_probe_prod = torch.from_numpy(np.asarray(z["W_probe_prod"], dtype=np.float32))
    if W_probe.dim() != 3 or W_probe.size(0) != len(slots):
        raise SystemExit(f"[e120-t0] W_probe 形状不符: {tuple(W_probe.shape)} vs slots={slots}")
    jpath = fit / "e120_warmstart_fit.json"
    if not jpath.exists():
        raise SystemExit(f"[e120-t0] 预跑统计缺席: {jpath}")
    stats = json.loads(jpath.read_text(encoding="utf-8"))
    band = stats.get("t0_probe", {}).get("ref_band_baseline", {})
    if REF_SLOT not in band or "acc" not in band[REF_SLOT]:
        raise SystemExit(f"[e120-t0] {jpath}: t0_probe.ref_band_baseline 缺槽 {REF_SLOT} 基尺")
    return slots, W_probe, W_probe_prod, float(band[REF_SLOT]["acc"])


def decode_acc(rows: torch.Tensor, ys: torch.Tensor, y_valid: torch.Tensor, W: torch.Tensor) -> float | None:
    """部署探针解码 acc（fit 脚本 fit_probe_deploy 的应用形, 零新造打分）:
    rows (N, F), W (F+1, 258) → argmax([rows, 1] @ W) 对槽字节 id。槽内无有效
    样本返回 None。"""
    m = y_valid.bool()
    if int(m.sum()) == 0:
        return None
    x = rows[m].float()
    x1 = torch.cat([x, torch.ones(x.size(0), 1)], dim=1)
    if x1.size(1) != W.size(0):
        raise SystemExit(f"[e120-t0] 特征宽不符: rows {x1.size(1)} vs W {W.size(0)}")
    pred = (x1 @ W.float()).argmax(dim=-1)
    return float(pred.eq(ys[m].long()).float().mean())


def collect_rows(model, ns, clean: torch.Tensor, byte_mask: torch.Tensor, device: torch.device):
    """单窗采集（fuzz_id F1 同款窗构造）: 生产拼接点 v_rows（e120 开 = 温启动
    读出行, 主判据对象）+ 被替换的生产读出行（read_trained, 对照）+ 逐槽字节
    目标。Returns (e120_rows (n_real, d_pack), prod_rows (n_real, d_pack),
    ys, y_valid)。"""
    source = clean.masked_fill(byte_mask, MASK_ID)
    chunks, memory, _index = _front_end(model, source)
    n_real = int(chunks.chunk_mask[0].sum())
    e120_rows = model._slm_store_rows(chunks)[1][0, :n_real].float().cpu()  # 生产拼接点
    gates_v = model.write_head(memory)
    prod_rows = read_trained(model.state_machine, trained_states(model.state_machine, gates_v, n_real))[
        0, :n_real
    ].float().cpu()
    zeros = torch.zeros_like(byte_mask)
    base_targets, base_slot, _bm = s1.make_targets(
        clean, zeros, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    return (
        e120_rows,
        prod_rows,
        base_targets[0, :n_real, :PROBE_SLOTS].cpu(),
        base_slot[0, :n_real, :PROBE_SLOTS].cpu(),
    )


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--base-run-dir", default=BASE_RUN)
    p.add_argument("--fit-dir", default=FIT_DIR)
    p.add_argument("--out-dir", default=OUT_DIR)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=32, help="训练流窗数（fuzz_id F1 同口径默认 32, 冒烟直接复用预跑窗流）")
    p.add_argument("--data-path", default=None, help="语料路径覆写（远端跑必须: resolved_config 内是 Windows 盘路径）")
    args = p.parse_args()
    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, base_step = load_model(Path(args.base_run_dir), device)
    if args.data_path:
        ns.data_path = args.data_path
    # 探针侧接线（甲列同款纪律）: E120 读出件 + 温启动（loud-fail）+ config
    # 开关 → 生产拼接点 _slm_store_rows 整行走新读出链
    model.e120_readout = E120WarmReadout(model.config).to(next(model.parameters()).device)
    warm_note = s1._e120_warm_start(model, args.fit_dir)
    model.config.e120_readout_swap = True
    # 接口断言（loud, 预跑同款）: d 格 + 生产拼接点确实换源
    if not hasattr(model, "e120_readout") or not getattr(model.config, "e120_readout_swap", False):
        raise SystemExit("[e120-t0] 探针侧接线失败: e120_readout/config 开关不在岗")
    if getattr(ns, "backbone_mode", "") != "slm" or getattr(ns, "v_row_source", "") != "state":
        raise ValueError(f"[e120-t0] 预期 slm d 格 v_row_source='state', got {ns.v_row_source!r}")
    print(
        f"[e120-t0] base={Path(args.base_run_dir).name} step={base_step} device={device.type} "
        f"seed={ns.seed} 温启动[{warm_note}]",
        flush=True,
    )

    slots, W_probe, W_probe_prod, baseline = load_deploy_probe(args.fit_dir)
    prod_slots_path = Path(args.fit_dir) / "probe_t0.npz"
    prod_slots = [int(s) for s in np.load(prod_slots_path)["probe_slots_prod"]]
    line = judgment_line(baseline)
    print(f"[e120-t0] 基尺(s{REF_SLOT})={baseline:.4f} → 判读线={line:.4f}（基尺 −3pp）", flush=True)

    windows = build_train_windows(ns, args.max_windows)
    masks = build_train_masks(windows, ns)
    print(f"[e120-t0] {len(windows)} 训练流窗 + 训练态掩码就位（{time.time() - t0:.0f}s）", flush=True)

    e120_rows_all, prod_rows_all, ys_all, yv_all = [], [], [], []
    with torch.no_grad():
        for wi, (clean, byte_mask) in enumerate(zip(windows, masks)):
            r, pr, ys, yv = collect_rows(
                model, ns, clean.to(device), byte_mask.to(device), device
            )
            e120_rows_all.append(r)
            prod_rows_all.append(pr)
            ys_all.append(ys)
            yv_all.append(yv)
            print(f"[e120-t0] window {wi} n_real={r.size(0)}（{time.time() - t0:.0f}s）", flush=True)

    e120_rows = torch.cat(e120_rows_all)
    prod_rows = torch.cat(prod_rows_all)
    ys_cat, yv_cat = torch.cat(ys_all), torch.cat(yv_all)
    acc_e120, acc_prod = {}, {}
    for i, s in enumerate(slots):
        a = decode_acc(e120_rows, ys_cat[:, i], yv_cat[:, i], W_probe[i])
        if a is not None:
            acc_e120[str(s)] = round(a, 4)
    for i, s in enumerate(prod_slots):
        a = decode_acc(prod_rows, ys_cat[:, s], yv_cat[:, s], W_probe_prod[i])
        if a is not None:
            acc_prod[str(s)] = round(a, 4)

    main_acc = acc_e120.get(REF_SLOT)
    verdict = None if main_acc is None else ("PASS" if main_acc >= line else "FAIL")
    stats = {
        "probe": "E120 t=0 零变化律检查 —— 温启动读出行逐段字节可解码率",
        "spec": "docs/versions/v3.7/FLUED_V3_7_E120_END_TO_END_IGNITION_20260903_CN.md §3 冒烟条款(修订 v2)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "base": {"run": Path(args.base_run_dir).name, "step": base_step, "seed": int(ns.seed)},
        "fit_dir": str(args.fit_dir),
        "windows": len(windows),
        "warm_start": warm_note,
        "ref_baseline": baseline,
        "judgment_line": line,
        "acc_e120_rows": acc_e120,
        "acc_prod_rows": acc_prod,
        "main_slot": REF_SLOT,
        "verdict": verdict,
        "n_rows": int(e120_rows.size(0)),
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "e120_t0_decodability.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "E120 t=0 零变化律检查（温启动读出行逐段字节可解码率, 训练前）",
        f"基座 {Path(args.base_run_dir).name} (step {base_step}) | 窗数 {len(windows)} | Σn={stats['n_rows']}",
        f"温启动: {warm_note}",
        f"判读: 基尺(s{REF_SLOT})={baseline:.4f} → 判读线={line:.4f} | 实测 s{REF_SLOT}={main_acc} "
        f"→ {'过线 PASS' if verdict == 'PASS' else ('不过线 FAIL' if verdict == 'FAIL' else '槽样本缺席 N/A')}",
        f"逐槽(e120 行, 主件): {acc_e120}",
        f"逐槽(生产读出行, 在岗上限对照): {acc_prod}",
        f"落盘: {out_dir / 'e120_t0_decodability.json'}",
    ]
    print("\n".join(lines), flush=True)
    if verdict == "FAIL":
        raise SystemExit(f"[e120-t0] 判读不过线: s{REF_SLOT} acc={main_acc} < 判读线 {line}（冒烟拒发口径）")


if __name__ == "__main__":
    main()
