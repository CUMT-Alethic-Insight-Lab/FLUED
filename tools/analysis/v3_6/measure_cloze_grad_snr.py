"""E0-f 双对象 cloze 检索梯度 SNR（零训练测量，2026-08-19，审计前置项测量 2）。

问题（逃逸梯度退化假说）：c 格 cloze 检索回执的损失梯度是否真正回传到
**写入键零件**？手术格（v37ks：to_k_center + K-seed + cloze 训练 20K）的
设计意图就是强行打通这条路；未手术格（v371，cloze 未训）若写入键零件
梯度死、旁路零件活，则"梯度从旁路逃逸、写入键从未收到检索信号"坐实。

对象（完整训练 checkpoint，只读硬冻结底座 + 测点叶子开 requires_grad）：
  1. checkpoints/v37_c_is_v371_20k_ctx4096_20260817（未手术 c 格）
  2. checkpoints/v37ks_c_is_v372_cloze_tokcenter_20k_ctx4096_20260818（手术 c 格）

损失构造：s1 的 cloze 管线原样复用（_splice_cloze prob=1.0 强制每窗一单 ->
make_mixed_mask -> _cloze_mask_overrides -> _slm_forward ->
_completion_target_grids（c 格 = 累积保持格）-> _cloze_slot_grid ->
_cloze_loss_and_metrics），逐窗单独 backward（step_model 的完整多任务损失
不走，只取 cloze_loss 一条——这正是假设要隔离的检索信号通路）。

测点（梯度范数 + 跨 batch SNR = mean(norm)/std(norm)；另报逐 batch 梯度
向量的平均成对余弦 = 方向稳定性——范数活着但方向乱 = 噪声而非信号）：
  写入键零件: wh_to_k_w      = write_head.to_k.weight
              wh_trunk_last  = write_head.trunk.1.{weight,bias}（WriteHead trunk
              末层 Linear，E75/E79 的"trunk"；to_k/to_v 共享）
              backbone_last  = backbone.self_blocks.1.*（主干末层，E82 口径）
  旁路零件:   decoder_first  = decoder.blocks.0.*（decoder 首层；c 格无
              decoder_in_mem 模块——v=state 格结构性不建，状态字典已核实）
  结构对照:   decoder_in     = decoder_in.{weight,bias}（c 格 direct 路径接口，
              cloze 损失只走 backbone 补全路径 -> 期望精确零，验证图接线）

口径：fp32、无 autocast、kda_impl=torch（探针主口径，E73 先例）；eval 模式；
eval 窗 = StreamingReconstructionDataset(seed+9999) 前 N 窗（两格同窗同种）；
mask/cloze 抽签流 = evaluate() 的播种纪律（_MASK_GENERATOR=1042,
_CLOZE_GENERATOR=1042+101003，逐窗顺序消费）。手术格的 to_k_center buffer
按 E75 口径先用语料暖批（persistent=False 新进程冷启动），随后回 eval
冻结测量——k_center 是常数平移，不改 d k/d W 的局部通路但改前向值，暖批
保部署形态保真。

判读（用户裁定）：手术格写入键活/未手术格死 ⇒ 逃逸梯度退化坐实；
都活 ⇒ 推翻"梯度从未到达"叙事（问题在更下游）；都死 ⇒ 推翻"手术打通
梯度"叙事（cloze 信号两格都没到写入键）。

Usage:
  python tools/analysis/v3_6/measure_cloze_grad_snr.py --device cuda
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from argparse import Namespace
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import build_eval_windows, load_model  # noqa: E402
import tools.analysis.v3_6.probe_archive_addressing_v37 as archive_probe  # noqa: E402
import tools.eval.paging_harness as ph  # noqa: E402

RUNS = [
    ("c-unsurgered-v371", "checkpoints/v37_c_is_v371_20k_ctx4096_20260817"),
    ("c-tokcenter-v372", "checkpoints/v37ks_c_is_v372_cloze_tokcenter_20k_ctx4096_20260818"),
]

# measurement point name -> (module getter, param filter). Aggregate grad norm
# = sqrt(sum of per-tensor squared norms) over the point's tensors.
def _points(model):
    return {
        "wh_to_k_w": [model.write_head.to_k.weight],
        "wh_trunk_last": [model.write_head.trunk[1].weight, model.write_head.trunk[1].bias],
        "backbone_last": list(model.backbone.self_blocks[-1].parameters()),
        "decoder_first": list(model.decoder.blocks[0].parameters()),
        "decoder_in": list(model.decoder_in.parameters()),
    }


def _collect_grads(points: dict) -> tuple[dict[str, float], dict[str, torch.Tensor]]:
    norms, vecs = {}, {}
    for name, params in points.items():
        grads = [p.grad for p in params]
        if all(g is None for g in grads):
            norms[name] = 0.0  # not in the loss graph (structural zero)
            vecs[name] = None
            continue
        parts = [torch.zeros_like(p) if g is None else g.detach().float() for p, g in zip(params, grads)]
        flat = torch.cat([t.reshape(-1) for t in parts])
        norms[name] = float(flat.norm())
        vecs[name] = flat
    return norms, vecs


def run_cell(label: str, run_dir: str, args, windows, device, t0: float) -> dict:
    model, ns, step = load_model(Path(run_dir), device)
    # fp32 torch-KDA main line (E73 probe convention; fla is the training kernel)
    model.config.kda_impl = "torch"
    for m in (model.state_machine, getattr(model, "state_machine_k", None)):
        if m is not None:
            m.c.kda_impl = "torch"
    # measured leaves only: autograd skips every graph branch that leads to no
    # requested leaf (values identical to a full-requires-grad backward).
    points = _points(model)
    for params in points.values():
        for p in params:
            p.requires_grad_(True)
    # E75 warm-buffer protocol for to_k_center checkpoints (no-op otherwise)
    hay_args = Namespace(data_path=ns.data_path, eval_data_root=str(ph.EVAL_DATA), suite="ruler/niah_single_1.jsonl")
    _src, hay_fn = archive_probe.make_haystack_fn(hay_args)
    archive_probe._warm_k_center(model, hay_fn, ns.seq_len, device)

    if s1._BPE_TOKENIZER is None:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    if s1._CLOZE_BANK is None:
        n_bank = s1._load_cloze_bank(args.cloze_bank)
        print(f"[E0f] cloze bank loaded: {n_bank} entries", flush=True)
    # evaluate()'s exact seed discipline for the mask/cloze draw streams
    s1._MASK_GENERATOR.manual_seed(ns.eval_mask_seed)
    s1._CLOZE_GENERATOR.manual_seed(ns.eval_mask_seed + s1._CLOZE_SEED_OFFSET)

    per_batch = []
    grad_vecs: dict[str, list] = {name: [] for name in points}
    for bi in range(args.batches):
        clean = windows[bi]
        clean_s, metas = s1._splice_cloze(clean, s1._CLOZE_BANK, 1.0, s1._CLOZE_GENERATOR)  # prob=1: every window carries one instance
        clean_s = clean_s.to(device)
        byte_mask = s1.make_mixed_mask(
            clean_s.cpu(), ns.mask_prob,
            char_frac=getattr(ns, "mask_char_frac", 0.4),
            char_span_max=getattr(ns, "mask_char_span_max", 3),
            tokenizer=s1._BPE_TOKENIZER, generator=s1._MASK_GENERATOR,
        )
        byte_mask = s1._cloze_mask_overrides(byte_mask, metas).to(device)
        source = clean_s.masked_fill(byte_mask, MASK_ID)
        out = s1._slm_forward(model, source, ns)
        chunks = out["chunks"]
        comp_targets, _comp_slot, _comp_masked, _trunc = s1._completion_target_grids(
            clean_s, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span, True
        )
        cloze_slot, cloze_active = s1._cloze_slot_grid(metas, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span)
        if not bool(cloze_active.any()):
            per_batch.append({"batch": bi, "skipped": "echo truncated out of grid"})
            print(f"[E0f] {label} batch {bi}: echo truncated, skipped", flush=True)
            continue
        cloze_loss, cloze_metrics = s1._cloze_loss_and_metrics(out["logits_backbone"], comp_targets, cloze_slot, cloze_active)
        model.zero_grad(set_to_none=True)
        cloze_loss.backward()
        norms, vecs = _collect_grads(points)
        for name in points:
            if vecs[name] is not None:
                grad_vecs[name].append(vecs[name])
        per_batch.append(
            {
                "batch": bi,
                "cloze_loss": round(float(cloze_loss.detach()), 4),
                "cloze_byte_acc": round(float(cloze_metrics["cloze_byte_acc"]), 4),
                "cloze_exact": round(float(cloze_metrics["cloze_exact"]), 4),
                "grad_norm": {k: round(v, 8) for k, v in norms.items()},
            }
        )
        brief = " ".join(f"{k}={v:.3e}" for k, v in norms.items())
        print(f"[E0f] {label} batch {bi}: loss={float(cloze_loss.detach()):.3f} acc={float(cloze_metrics['cloze_byte_acc']):.3f} | {brief} ({time.time() - t0:.0f}s)", flush=True)

    summary = {}
    for name in points:
        norms = [b["grad_norm"][name] for b in per_batch if "grad_norm" in b]
        if not norms:
            summary[name] = {"n": 0}
            continue
        mean = sum(norms) / len(norms)
        std = math.sqrt(sum((x - mean) ** 2 for x in norms) / len(norms))
        vecs = grad_vecs[name]
        cos = None
        if len(vecs) >= 2 and any(float(v.norm()) > 0 for v in vecs):
            vn = [v / v.norm().clamp(min=1e-20) for v in vecs]
            sims = [float((vn[i] * vn[j]).sum()) for i in range(len(vn)) for j in range(i + 1, len(vn))]
            cos = round(sum(sims) / len(sims), 4)
        summary[name] = {
            "n": len(norms),
            "mean": round(mean, 8),
            "std": round(std, 8),
            "snr": round(mean / std, 4) if std > 0 else None,
            "min": round(min(norms), 8),
            "max": round(max(norms), 8),
            "grad_cos_mean": cos,
        }
    result = {
        "label": label,
        "run": Path(run_dir).name,
        "step": step,
        "to_k_center": bool(getattr(model.config, "to_k_center", False)),
        "seed_source": getattr(ns, "seed_source", "v"),
        "points": summary,
        "per_batch": per_batch,
        "window_valid_bytes_first_batch": int(windows[0].ne(0).sum()) if args.batches else 0,
    }
    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--batches", type=int, default=8, help="cloze windows per cell (batch_size=1)")
    p.add_argument("--cloze-bank", default="P:/FLUED_corpus/cloze_bank_v1.jsonl")
    p.add_argument("--out-dir", default="outputs/audit_measurements_20260819")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    # same corpus windows for both cells (dataset seed+9999, identical data/seq_len)
    from argparse import Namespace as _NS

    win_ns = _NS(data_path="P:/FLUED_corpus/corpus_v3/corpus_v3.txt", seq_len=4096, batch_size=1, max_eval_batches=16, seed=42)
    windows = build_eval_windows(win_ns, args.batches)
    print(f"[E0f] {len(windows)} windows ready ({time.time() - t0:.0f}s)", flush=True)

    results = [run_cell(label, run, args, windows, device, t0) for label, run in RUNS]

    report = {
        "probe": "E0-f 双对象 cloze 检索梯度 SNR (escape-gradient degradation test)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "regime": "fp32, no autocast, kda_impl=torch, eval mode; cloze prob=1.0 forced; "
        "mask/cloze draw streams = evaluate() seed discipline (1042 / 1042+101003); "
        "to_k_center buffer warmed per E75 protocol (surgical cell only)",
        "loss": "s1 cloze 管线: _splice_cloze -> mixed mask + overrides -> _slm_forward -> "
        "cumulative completion grid -> _cloze_loss_and_metrics; cloze_loss alone backward",
        "points_legend": {
            "wh_to_k_w": "write_head.to_k.weight (写入键投影)",
            "wh_trunk_last": "write_head.trunk.1 (WriteHead trunk 末层 Linear, to_k/to_v 共享)",
            "backbone_last": "backbone.self_blocks.1 (主干末层)",
            "decoder_first": "decoder.blocks.0 (旁路: decoder 首层; c 格无 decoder_in_mem 模块)",
            "decoder_in": "decoder_in (结构对照: c 格 cloze 路径不经此 -> 期望精确零)",
        },
        "batches_per_cell": args.batches,
        "results": results,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "e0f_cloze_grad_snr.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[E0f] report -> {out_path} ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
