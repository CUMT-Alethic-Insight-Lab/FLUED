"""R3 丙前置特有件：函数恒等对拍门（零训练；任务书 §2.3，冻结 v1.0 逐字执行）。

R2 母列 20K ckpt 上同窗对拍原生 BT=64 vs 变长铺瓦的 NLL——对拍不过=实现有
bug，**不许点火**。

协议（预注册，2026-09-14 施工回执同文；E121 逐位/容差双档先例）：
- 逐位档：挂接态 plan=None 直通 vs 未挂接原生，窗 0 逐 token NLL 必须逐位
  相等（同进程同码，仅多一层直通 wrapper——直通不洁即实现污染，响亮停）。
- 容差档（判决）：全部对拍窗 ``|ΔNLL_mean| ≤ TOL``，
  ``TOL = max(10 × max_w |Δ_uniform64,w| over calibration, 0.02 nat/token)``。
  _uniform64 = 变长铺瓦以均匀 64-token 段运行——与原生同铺瓦网格，其差隔离
  「接力 handoff bf16 cast」单一机制；S0'' 计划仅把边界密度提到 ~5×（段均
  ~12 token），线性放大界取 10×；0.02 nat/token 绝对地板防 calibration 退化
  （bf16 logits 噪声量级 ~1e-2 nat）。
- NLL 语义与仪器零漂：``token_nll`` 直接复用仪器本体（全 ids 前向、fp32
  log_softmax、位置 0 无预测）；窗/分词语义 = r2_spec（BOS + 截 2048）。

Usage:
  python tools/baselines/deltanet_r2/probe_r3_vtile_parity.py \
      --model-path outputs/r2_mother_20k_local_20260914/mother20k_latest \
      --corpus P:/FLUED_corpus/corpus_v3/corpus_v3.txt \
      --n-windows 40 --out-dir outputs/r3_transplant_vtile_20260914/parity_gate
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import tools.analysis.cross_arch.probe_e122_deltanet_book as e122  # noqa: E402
import tools.baselines.deltanet_r2.r2_spec as r2spec  # noqa: E402
import tools.baselines.deltanet_r2.r3_spec as r3  # noqa: E402

TOL_FLOOR = 0.02          # nat/token 绝对地板（预注册）
TOL_CALIB_MULT = 10.0     # _uniform64 校准带线性放大界（预注册）


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--model-path", required=True, help="R2 母列 20K ckpt 目录")
    p.add_argument("--corpus", required=True)
    p.add_argument("--s0-checkpoint", default=None,
                   help="S0'' 段界器权重（缺省读 canonical_v37 init_checkpoint）")
    p.add_argument("--n-windows", type=int, default=40)
    p.add_argument("--start-window", type=int, default=0)
    p.add_argument("--calibration-windows", type=int, default=8)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--device", default="cuda")
    return p.parse_args()


def _mean_token_nll(model, ids: list[int], device) -> tuple[float, list[float | None]]:
    """仪器 token_nll 语义零漂复用：全 ids 前向、fp32 log_softmax。"""
    x = torch.tensor([ids], dtype=torch.long, device=device)
    with torch.no_grad():
        per = e122.token_nll(model(x).logits, ids)
    vals = [v for v in per[1:] if v is not None]
    return sum(vals) / len(vals), per


def _uniform64_plan(t_total: int) -> list[int]:
    """均匀 64 段计划（=原生铺瓦网格；校准专用，与 S0'' 无关）。"""
    plan = [r3.VTILE_CHUNK_SIZE] * (t_total // r3.VTILE_CHUNK_SIZE)
    rem = t_total - sum(plan)
    if rem:
        plan.append(rem)
    return plan


def _resolve_s0(path: str | None) -> str:
    if path:
        p = Path(path)
    else:
        cfg = json.loads((Path(__file__).resolve().parents[3] / "configs"
                          / "canonical_v37.json").read_text(encoding="utf-8"))
        p = Path(cfg["init_checkpoint"])
    if not p.exists():
        raise SystemExit(f"[r3-vtile-parity] S0'' 权重缺席：{p}——停报")
    return str(p)


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    device = args.device
    t0 = time.time()

    model, tok, fp = r3.load_model_and_tokenizer_local(args.model_path,
                                                       torch.device(device))
    if r3.config_has_vtile(model.config):
        raise SystemExit("[r3-vtile-parity] 底物带 r3_vtile 戳记（应为母列）——停报")
    s0_ckpt = _resolve_s0(args.s0_checkpoint)
    segmentor = r3.load_s0_segmentor(s0_ckpt, device=device)

    def window_ids(w: int) -> tuple[bytes, list[int]]:
        with Path(args.corpus).open("rb") as f:
            f.seek(w * r2spec.WINDOW_BYTES)
            raw = f.read(r2spec.WINDOW_BYTES)
        if len(raw) < r2spec.WINDOW_BYTES:
            raise SystemExit(f"[r3-vtile-parity] 窗 {w} 不足整窗——停报")
        ids, _full = e122.tokenize_window(tok, raw.decode("utf-8", errors="replace"),
                                          r2spec.MAX_TOKENS)
        return raw, ids

    # ---- 逐位档：直通洁净性（窗 0）----
    raw0, ids0 = window_ids(args.start_window)
    nll_native_pre, per_pre = _mean_token_nll(model, ids0, device)
    attach_report = r3.attach_vtile(model, True)
    _mean_token_nll(model, ids0, device)  # plan=None 直通（wrapper 路径）
    # 直通必须逐位：重算一次拿 per-token 对照
    x0 = torch.tensor([ids0], dtype=torch.long, device=device)
    with torch.no_grad():
        per_passthrough = e122.token_nll(model(x0).logits, ids0)
    bitwise = per_passthrough == per_pre
    if not bitwise:
        raise SystemExit("[r3-vtile-parity] 逐位档 FAIL：直通 wrapper 污染前向"
                         "（plan=None ≠ 未挂接）——实现有 bug，不点火")
    print(f"[r3-vtile-parity] 逐位档 PASS（直通 = 原生，窗 0 逐 token 逐位相等）",
          flush=True)

    # ---- 校准档（前 C 窗：_uniform64 vs 原生 = handoff cast 单一机制带）----
    calib: list[dict] = []
    for wi in range(args.start_window, args.start_window + args.calibration_windows):
        raw, ids = window_ids(wi)
        t_total = len(ids)
        nll_nat, _ = _mean_token_nll(model, ids, device)
        plan_u = _uniform64_plan(t_total)
        r3.set_vtile_plan(plan_u)
        try:
            nll_uni, _ = _mean_token_nll(model, ids, device)
        finally:
            r3.clear_vtile_plan()
        calib.append({"window": wi, "t_total": t_total, "nll_native": nll_nat,
                      "nll_uniform64": nll_uni,
                      "d_abs": abs(nll_uni - nll_nat)})
    d_max = max(c["d_abs"] for c in calib)
    tol = max(TOL_CALIB_MULT * d_max, TOL_FLOOR)
    print(f"[r3-vtile-parity] 校准带 max|Δ_uniform64| = {d_max:.3e} → "
          f"TOL = {tol:.4f} nat/token", flush=True)

    # ---- 容差档（判决）：全部 N 窗 S0'' 计划 vs 原生 ----
    gate: list[dict] = []
    all_pass = True
    for wi in range(args.start_window, args.start_window + args.n_windows):
        raw, ids = window_ids(wi)
        t_total = len(ids)
        nll_nat, _ = _mean_token_nll(model, ids, device)
        plan, stats = r3.vtile_plan_for_window(segmentor, tok, raw,
                                               t_total=t_total, device=device)
        r3.set_vtile_plan(plan)
        try:
            nll_vt, _ = _mean_token_nll(model, ids, device)
        finally:
            r3.clear_vtile_plan()
        d_abs = abs(nll_vt - nll_nat)
        ok = d_abs <= tol
        all_pass &= ok
        gate.append({"window": wi, "t_total": t_total, "nll_native": nll_nat,
                     "nll_vtile": nll_vt, "d_abs": d_abs, "within_tol": ok,
                     **stats})
        print(f"[r3-vtile-parity] win {wi:5d} T={t_total} native {nll_nat:.6f} "
              f"vtile {nll_vt:.6f} |Δ| {d_abs:.3e} {'OK' if ok else 'FAIL'} "
              f"(cuts_byte {stats['n_cuts_byte']} segs {stats['n_segments']})",
              flush=True)

    d_all = [g["d_abs"] for g in gate]
    cuts = [g["n_cuts_byte"] for g in gate]
    segs = [g["n_segments"] for g in gate]
    summary = {
        "probe": "R3 丙前置特有件：函数恒等对拍门（原生 BT=64 vs 变长铺瓦，零训练）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model_path": args.model_path,
        "model_fingerprint": fp,
        "s0_checkpoint": s0_ckpt,
        "protocol": {
            "bitwise_clause": "plan=None 直通 vs 未挂接，窗 0 逐 token 逐位相等",
            "tolerance_clause": f"TOL = max({TOL_CALIB_MULT}×max|Δ_uniform64|_calib, "
                                f"{TOL_FLOOR}) nat/token，全窗 |ΔNLL_mean| ≤ TOL",
            "tol": tol, "tol_floor": TOL_FLOOR, "tol_calib_mult": TOL_CALIB_MULT,
            "calibration_windows": args.calibration_windows,
            "n_windows": args.n_windows, "start_window": args.start_window,
        },
        "bitwise_passthrough_pass": bitwise,
        "calibration": calib,
        "gate": {
            "pass": all_pass,
            "n_windows": len(gate),
            "max_d_abs": max(d_all), "mean_d_abs": sum(d_all) / len(d_all),
            "median_d_abs": sorted(d_all)[len(d_all) // 2],
            "per_window": gate,
        },
        "s0_direct_check": {
            "n_cuts_byte_mean": sum(cuts) / len(cuts),
            "n_cuts_byte_min": min(cuts), "n_cuts_byte_max": max(cuts),
            "n_segments_token_mean": sum(segs) / len(segs),
            "registered_reference": "E124 门②在册 172.7 段/窗（byte 空间，训练流）",
            "note": "token 空间段数 ≤ byte 空间切点数（多 byte 切点可并入同一 "
                    "token 边界）；直测复核按 byte 空间量对照在册数",
        },
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "parity_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in
                      ("bitwise_passthrough_pass", "gate", "s0_direct_check")},
                     ensure_ascii=False, indent=2), flush=True)
    if not all_pass:
        print("[r3-vtile-parity] 容差档 FAIL——对拍不过=实现有 bug，不许点火",
              flush=True)
        return 2
    print("[r3-vtile-parity] 对拍门 PASS（逐位档+容差档全过）", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
