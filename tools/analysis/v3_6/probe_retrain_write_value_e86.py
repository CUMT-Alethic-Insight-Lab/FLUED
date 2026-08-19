"""E86 双对象黑板探针复测（零训练，2026-08-19，审计前置项测量 1）。

对两个**读出链复训产物**复跑 E73-A6 同款闭式字节探针（写值 v -> slot0-3
字节 id 的 one-vs-all 岭回归，16 窗 eval seed 1042 同口径）：
  1. retrain_readout_c_v371_completion_ubb_hardened_20260819（未手术 c 格复训版，
     fork 1 补全形态 + 加固，E86 载体）
  2. retrain_readout_c_tokcenter_40k_20260819（手术 c 格 40K 复训版，E87 载体）

加载方式（retrain_readout_chain.py 的保存结构）：复训产物是"读出链参数包"
{realign, decoder_in, decoder（剔共享 byte_lookup）, backbone} 的 state_dict，
须叠回其 source_run 的冻结底座才是完整的"复训后对象"。写值 v 产线
（summarizer memory 行 -> write_head.to_v(trunk(...))）不在复训包内、全程
冻结——探针目标张量与 realign/decoder/backbone 的复训无接线关系（to_k_center
的 k_center buffer 只碰 to_k 支路，v 支路 buffer-independent，见
measure_write_value_probe.py 口径注记）。因此本测量同时是两层核对：
  (a) 未手术对象的 v-probe 必须逐位复现 E73-A6（0.6185/0.3727/0.3223/0.6092）
      ——同窗同种同协议，叠包不动写值产线的布线校验；
  (b) 手术对象（v37ks 底座，to_k_center 从 0 步在岗、共享 trunk）的 v-probe
      是首次实测——E79 在 b 格坐实的"共享 trunk 手术误伤"（v-probe 腰斩）
      是否也在 c 格成立。
判读（用户裁定）：复训对象仍 ~0.6 档 ⇒ 写值信息在、"爬不高"（0.19/0.3185
平台）是优化/接口形态问题而非信息缺失。

对照基线：E73-A6（未复训 c 格，16 窗同口径）v 0.6185/0.3727/0.3223/0.6092、
m（上限对照）0.7096/0.4628/0.3809/0.6273（outputs/oracle_write_verdict_20260818/
oracle_write_verdict.json mechanism.byte_probe_from_v/from_m）。

纪律：checkpoint 与复训包一律只读；fp32；零训练（ridge 为闭式代数）。
Usage:
  python tools/analysis/v3_6/probe_retrain_write_value_e86.py --device cuda
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    build_eval_windows,
    build_masks,
    byte_probe,
    load_model,
)
from tools.analysis.v3_6.measure_write_value_probe import collect  # noqa: E402

PACKAGES = [
    ("retrain-unsurgered-c", "checkpoints/retrain_readout_c_v371_completion_ubb_hardened_20260819/retrained_readout.pt"),
    ("retrain-tokcenter-c-40k", "checkpoints/retrain_readout_c_tokcenter_40k_20260819/retrained_readout.pt"),
]
# E73-A6 reference (c-grid V channel, 16 eval windows, seed 1042 protocol)
E73_A6 = {
    "v": {"0": 0.6185, "1": 0.3727, "2": 0.3223, "3": 0.6092},
    "m": {"0": 0.7096, "1": 0.4628, "2": 0.3809, "3": 0.6273},
    "majority": {"0": 0.2138, "1": 0.0377, "2": 0.0423, "3": 0.1825},
}


def overlay_retrained_modules(model, pkg: dict) -> dict:
    """Load the retrained readout-chain package onto the frozen base model —
    the exact mirror of retrain_readout_chain.load_retrain_state's module part
    (no optimizer/RNG here). Returns per-module max|delta| vs the base weights
    as a wiring sanity (the overlay must actually change something)."""
    modules = pkg["modules"]
    deltas = {}
    for name, loader in (
        ("realign", model.state_machine.realign),
        ("decoder_in", model.decoder_in),
        ("decoder", model.decoder),
        ("backbone", model.backbone),
    ):
        if name not in modules:
            continue
        before = {k: v.detach().clone() for k, v in loader.state_dict().items()}
        if name == "decoder":
            loader.load_state_dict(modules[name], strict=False)  # byte_lookup rows stripped by construction
        else:
            loader.load_state_dict(modules[name])
        after = loader.state_dict()
        deltas[name] = round(
            max(float((after[k].float() - before[k].float()).abs().max()) for k in before), 6
        )
    return deltas


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16, help="16 = the E73/training final-eval protocol")
    p.add_argument("--out-dir", default="outputs/audit_measurements_20260819")
    p.add_argument("--packages", nargs="*", default=[r for _, r in PACKAGES])
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    results = []
    windows = masks = None
    for pkg_path in args.packages:
        pkg = torch.load(pkg_path, map_location="cpu", weights_only=False)
        src_run = pkg["args"]["run_dir"]
        label = next((lab for lab, r in PACKAGES if r == pkg_path), Path(pkg_path).parent.name)
        model, ns, step = load_model(Path(src_run), device)
        deltas = overlay_retrained_modules(model, pkg)
        print(
            f"[E86] {label}: base={Path(src_run).name} step={step} + pkg step={pkg['step']} "
            f"overlay max|Δ|={deltas} ({time.time() - t0:.0f}s)",
            flush=True,
        )
        # fork-1 structural fact: decoder_in is NOT in the completion loss path
        # (cond = backbone_out + pos), so it gets zero gradient in retraining and
        # its overlay delta is exactly 0.0 — expected, not broken wiring. The
        # trained modules (realign/decoder/backbone) must actually move.
        if any(deltas.get(k, 1.0) == 0.0 for k in ("realign", "decoder", "backbone")):
            raise RuntimeError(f"{label}: overlay changed nothing in {deltas} — wiring broken")
        if windows is None:
            windows = build_eval_windows(ns, args.max_windows)
            masks = build_masks(windows, ns)
            print(f"[E86] {len(windows)} eval windows + masks ready ({time.time() - t0:.0f}s)", flush=True)
        channel, rows_name, xs_v, xs_in, ys, yvalid = collect(model, windows, masks, device)
        row = {
            "label": label,
            "package": str(Path(pkg_path).parent.name),
            "source_run": Path(src_run).name,
            "base_step": step,
            "pkg_step": pkg["step"],
            "overlay_max_abs_delta": deltas,
            "channel": channel,
            "input_rows": rows_name,
            "to_k_center": bool(getattr(model.config, "to_k_center", False)),
            "split_trunk": bool(getattr(model.config, "split_trunk", False)),
            "probe_from_write_value": byte_probe(xs_v, ys, yvalid),
            "probe_from_input_rows": byte_probe(xs_in, ys, yvalid),
        }
        results.append(row)
        pv = row["probe_from_write_value"]
        print(
            f"[E86] {label}: v-probe slots0-3 acc="
            + "/".join(f"{pv[s]['acc']:.4f}" for s in sorted(pv))
            + f" (majority {'/'.join(f'{pv[s]['majority']:.4f}' for s in sorted(pv))}) ({time.time() - t0:.0f}s)",
            flush=True,
        )
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    report = {
        "probe": "E86 双对象黑板探针复测 (retrained readout-chain objects, E73-A6 protocol)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "windows": args.max_windows,
        "note": "写值 v 产线（summarizer -> write_head.to_v(trunk)）不在复训包内、全程冻结；"
        "to_k_center buffer 只碰 to_k 支路，v-probe 是 buffer-independent。"
        "复训包叠回 source_run 冻结底座后测量（overlay max|Δ| 已校验非零）。",
        "e73_a6_reference": E73_A6,
        "results": results,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "e86_write_value_probe.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[E86] report -> {out_path} ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
