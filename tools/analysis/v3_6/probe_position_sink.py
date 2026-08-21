"""段内字节乱序探针（位置沉淀 vs 内容偏置，用户裁定追账项，2026-08-21，零训练）。

问题：memory 行的逐 slot 剖面段首集中（E88，头尾比 5.15×）是**位置沉淀**
（summarizer 池化按位置存——不管谁坐 slot0 都存它）还是**内容偏置**（存的
是内容身份驱动的——段首字节本来就是高信息量内容，乱序后沉淀跟着内容跑）？
判 LIM（lost-in-the-middle）同族病位。

设计：对每段，在**有效 span 内**打乱 span embeddings（嵌入随内容一起走），
只重跑 summarizer（DiT 块带 RoPE，位置敏感，乱序非平凡）；targets 按同一
排列同步乱序。然后在新 memory 行上按 E73-A6 口径（2-fold one-vs-all 岭
回归，real−garbage）复测逐 slot 剖面，与基线剖面同窗对照。

判词（赛前冻结于本 docstring）：
  乱序后头尾比仍 >2（与基线 5.15× 同族）→ **位置沉淀**：slot 位置决定存什么，
    与内容无关——summarizer 的池化结构病（fork 3 F3 池化臂的直接依据）；
  乱序后头尾比压到 <1.5（基线 >2）→ **内容偏置**：存什么由内容身份决定，
    段首集中只是"段首内容恰好高信息量"的倒影——fork 3 靶子改回内容选择；
  中间 → 混合，人工读表。

口径：c 格 v37_c_is（E88 同 checkpoint 同 16 窗同 mask），fp32 无 autocast，
checkpoint 只读硬冻结；乱序种子 20260821（每段独立 randperm）；garbage 纪律
同前（chunk 轴排列，种子 20260819）。基线臂必须复测 E88 memory 行剖面档级
（slot0-3 ≈ +0.53/+0.43/+0.34/+0.48，容差 ±0.02）作锚。

Usage:
  python tools/analysis/v3_6/probe_position_sink.py --device cuda
  CPU 冒烟: python tools/analysis/v3_6/probe_position_sink.py --device cpu --max-windows 2
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

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    byte_probe,
    load_model,
)

C_RUN = "checkpoints/v37_c_is_v371_20k_ctx4096_20260817"
OUT_DIR = "outputs/audit_measurements_20260819"
SHUFFLE_SEED = 20260821
PERM_SEED = 20260819  # garbage pairing — same convention as the localization package
# E88 memory-row anchor (tail_loss_localization.json, slots 0-3)
ANCHOR = {"0": 0.5276, "1": 0.4293, "2": 0.3417, "3": 0.4785}


@torch.no_grad()
def collect(model, windows, masks, device):
    """Per real chunk: (memory_base, memory_perm, targets_base, targets_perm).
    Permutation: per chunk over its valid span, applied to span_embeddings AND
    target bytes alike (content moves with its embedding); only the summarizer
    re-runs — encoder untouched, chunk grid frozen (no boundary confound)."""
    gen = torch.Generator().manual_seed(SHUFFLE_SEED)
    ggen = torch.Generator().manual_seed(PERM_SEED)
    out = {"mb_r": [], "mb_g": [], "mp_r": [], "mp_g": []}
    ys_b, ys_p, yv = [], [], []
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        chunks, memory, _index = _front_end(model, source)
        n = int(chunks.chunk_mask[0].sum())
        se = chunks.span_embeddings[0, :n]  # (n, span, d)
        tm = chunks.token_mask[0, :n]  # (n, span)
        bt, bs, _m = s1.make_targets(
            clean.to(device), torch.zeros_like(bm).to(device),
            chunks.chunk_ids, chunks.offsets, model.config.max_chunks, model.config.max_span,
        )
        tb, vb = bt[0, :n], bs[0, :n]
        # per-chunk permutation over the valid span
        se_p = se.clone()
        tb_p = tb.clone()
        for c in range(n):
            L = int(tm[c].sum())
            if L < 2:
                continue
            perm = torch.randperm(L, generator=gen).to(device)
            se_p[c, :L] = se[c, perm]
            tb_p[c, :L] = tb[c, perm]
        memory_p = model.summarizer(se_p.unsqueeze(0), tm.unsqueeze(0))[0].float()
        mb = memory[0, :n].float()
        perm_rows = torch.randperm(n, generator=ggen).to(device)  # garbage pairing, shared
        out["mb_r"].append(mb.cpu())
        out["mb_g"].append(mb[perm_rows].cpu())
        out["mp_r"].append(memory_p.cpu())
        out["mp_g"].append(memory_p[perm_rows].cpu())
        ys_b.append(tb.cpu())
        ys_p.append(tb_p.cpu())
        yv.append(vb.cpu())
    return ({k: torch.cat(v) for k, v in out.items()}, torch.cat(ys_b), torch.cat(ys_p), torch.cat(yv))


def _shape(diff: dict[str, float], head=(0, 4), tail=(16, 32)):
    def mean(lo, hi):
        vals = [diff[str(s)] for s in range(lo, hi) if str(s) in diff]
        return round(sum(vals) / len(vals), 4) if vals else None
    h, t = mean(*head), mean(*tail)
    return {
        "head_mean": h, "tail_mean": t,
        "head_over_tail": round(h / t, 3) if h is not None and t and t > 1e-9 else None,
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=C_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16)
    p.add_argument("--report-slots", type=int, default=32)
    p.add_argument("--out-dir", default=OUT_DIR)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, step = load_model(Path(args.run_dir), device)
    windows = build_eval_windows(ns, args.max_windows)
    masks = build_masks(windows, ns)
    print(f"[sink] model={Path(args.run_dir).name} step={step} device={device.type} windows={len(windows)} "
          f"({time.time() - t0:.0f}s)", flush=True)

    xs, yb, yp, yv = collect(model, windows, masks, device)
    print(f"[sink] rows={xs['mb_r'].size(0)} collected ({time.time() - t0:.0f}s); probes...", flush=True)

    def profile(x_key, y):
        pr = byte_probe(xs[f"{x_key}_r"], y, yv)
        pg = byte_probe(xs[f"{x_key}_g"], y, yv)
        return {s: round(pr[s]["acc"] - pg[s]["acc"], 4) for s in pr}

    prof_base = profile("mb", yb)
    prof_perm = profile("mp", yp)
    sh_base, sh_perm = _shape(prof_base), _shape(prof_perm)

    # anchor: base arm must reproduce the E88 memory-row profile slots 0-3 (±0.02)
    anchor_check = {s: {"ref": r, "got": prof_base.get(s),
                        "abs_delta": round(abs(prof_base.get(s, 0.0) - r), 4)} for s, r in ANCHOR.items()}
    anchor_ok = all(v["abs_delta"] <= 0.02 for v in anchor_check.values())

    rb, rp = sh_base["head_over_tail"], sh_perm["head_over_tail"]
    if rp is not None and rb is not None and rp > 2.0:
        verdict = "位置沉淀：乱序后头尾比仍 >2——池化按位置存、与内容无关（summarizer 池化结构病，fork 3 F3 池化臂直接依据）。"
    elif rp is not None and rb is not None and rb > 2.0 and rp < 1.5:
        verdict = "内容偏置：乱序后头尾比压平（<1.5）——存什么由内容身份决定，段首集中是内容倒影（fork 3 靶子改回内容选择）。"
    else:
        verdict = "中间形态——人工读表。"
    if not anchor_ok:
        verdict = "⚠ 基线臂锚校验失败（先查口径，判词作废）：" + verdict

    report = {
        "probe": "段内字节乱序探针：位置沉淀 vs 内容偏置（c 格 v37_c_is memory 行）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": Path(args.run_dir).name, "step": step},
        "params": {"windows": len(windows), "shuffle_seed": SHUFFLE_SEED, "perm_seed": PERM_SEED,
                   "eval_mask_seed": ns.eval_mask_seed},
        "protocol": "段内有效 span 乱序（嵌入随内容走）只重跑 summarizer（DiT 带 RoPE）；targets 同步乱序；"
        "E73-A6 2-fold ridge real−garbage；garbage=chunk 轴排列（两臂共享）",
        "anchor_check_vs_E88": {"ok": anchor_ok, "slots": anchor_check},
        "profile_base": {"real_minus_garbage": prof_base, "shape": sh_base},
        "profile_shuffled": {"real_minus_garbage": prof_perm, "shape": sh_perm},
        "verdict": verdict,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "probe_position_sink.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "段内字节乱序探针（位置沉淀 vs 内容偏置）— c 格 v37_c_is memory 行，16 窗",
        f"日期 {report['created']}  设备 {device.type}  乱序种子 {SHUFFLE_SEED}",
        "",
        f"锚校验（基线臂 vs E88 memory 剖面 slot0-3，容差 ±0.02）：{json.dumps(anchor_check)} -> {'OK' if anchor_ok else '✗'}",
        "",
        "逐 slot real−garbage：slot | 基线 | 乱序后",
    ]
    for s in range(min(args.report_slots, len(prof_base))):
        k = str(s)
        lines.append(f"  {s:>4d} | {prof_base.get(k, float('nan')):+.4f} | {prof_perm.get(k, float('nan')):+.4f}")
    lines += [
        "",
        f"形态：基线 head {sh_base['head_mean']} tail {sh_base['tail_mean']} 比 {sh_base['head_over_tail']}",
        f"      乱序 head {sh_perm['head_mean']} tail {sh_perm['tail_mean']} 比 {sh_perm['head_over_tail']}",
        "",
        "判词（赛前冻结于 docstring）：乱序后 比>2 → 位置沉淀；比<1.5 且基线>2 → 内容偏置；中间→人工。",
        f"判词：{verdict}",
        "",
        f"完整数据: {out_path}",
    ]
    summary_path = out_dir / "SUMMARY_position_sink.txt"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
