"""先验盲猜地板：补全形态（0.3185/0.0722 去水分，2026-08-19 审计前置项测量 3b）。

档案馆 null-state 探针（--null-state）只覆盖 hit@1/hit@k 口径（E78 0.17 线）；
E87/E86 的头条数 0.3185（手术 c 格 40K 复训饱和）/ 0.0722（未手术 c 格加固
复训饱和）是**补全形态 byte_acc**——它的"只凭 LM 先验答"地板须在同一补全
评测上把状态/接口输入置空来量。本脚本对两个复训对象（复训包叠回冻结底座）
跑同一 16 窗 eval seed 1042 补全评测，五臂：
  real        原态对照（必须逐位复现 E87 0.3185 / E86 0.0722 —— 布线校验）
  shuffle_V   V 行（状态读出行）跨 chunk 置乱——状态通道内容毁掉，K 直通保留
  zero_V      V 行全零
  shuffle_KV  K 行（index 直通）与 V 行同时置乱——纯先验地板
  zero_KV     同时全零（最严地板；backbone 只见位置嵌入与零存储）
每窗一个独立播种置换（确定性）。置空点在 realign 之后的 v_rows / 入 backbone
的 k_rows 上（retrain_readout_chain._chain_logits 的同形路径）。

判读：real − zero_KV = 存储内容的总贡献；real − null_V = 状态通道贡献
（c 格 K 直通是承重旁路，E86 附录 A 口径）；zero_KV 即 0.3185 的"水分"上限。

Usage:
  python tools/analysis/v3_6/measure_completion_prior_floor.py --device cuda
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
    build_eval_windows,
    build_masks,
    load_model,
)
from tools.train.v3_6.retrain_readout_chain import _chain_logits, _states_for  # noqa: E402
import tools.analysis.v3_6.probe_archive_addressing_v37 as archive_probe  # noqa: E402
import tools.eval.paging_harness as ph  # noqa: E402
from argparse import Namespace  # noqa: E402

PACKAGES = [
    (
        "retrain-unsurgered-c",
        "checkpoints/retrain_readout_c_v371_completion_ubb_hardened_20260819/retrained_readout.pt",
        0.0722,  # E86 natural_full saturation
    ),
    (
        "retrain-tokcenter-c-40k",
        "checkpoints/retrain_readout_c_tokcenter_40k_20260819/retrained_readout.pt",
        0.3185,  # E87 plateau
    ),
]
ARMS = ["real", "shuffle_V", "zero_V", "shuffle_KV", "zero_KV"]


def overlay(model, pkg: dict) -> None:
    """Same module overlay as retrain_readout_chain.load_retrain_state."""
    modules = pkg["modules"]
    model.state_machine.realign.load_state_dict(modules["realign"])
    model.decoder_in.load_state_dict(modules["decoder_in"])
    model.decoder.load_state_dict(modules["decoder"], strict=False)  # byte_lookup stripped by construction
    if "backbone" in modules:
        model.backbone.load_state_dict(modules["backbone"])


@torch.no_grad()
def _chain_logits_nulled(model, chunks, n_real: int, S: torch.Tensor, k_rows: torch.Tensor, arm: str, gen: torch.Generator) -> torch.Tensor:
    """retrain_readout_chain._chain_logits with the store rows nulled AFTER the
    readout (realign output shuffled/zeroed across chunks; K rows likewise).
    Identical downstream path otherwise (backbone -> +pos -> decoder)."""
    sm = model.state_machine
    q = sm.readout_query.float()
    reads = torch.einsum("qhk,bnhkv->bnqhv", q, S.float())
    read = reads.reshape(S.size(0), n_real, q.size(0), -1).to(S.dtype)
    v_rows = sm.realign(read).mean(dim=2)  # (B, n, d_pack)
    k_rows = k_rows[:, :n_real]
    if arm.startswith("shuffle"):
        perm = torch.randperm(n_real, generator=gen).to(v_rows.device)
        v_rows = v_rows[:, perm]
        if arm == "shuffle_KV":
            perm_k = torch.randperm(n_real, generator=gen).to(k_rows.device)
            k_rows = k_rows[:, perm_k]
    elif arm.startswith("zero"):
        v_rows = torch.zeros_like(v_rows)
        if arm == "zero_KV":
            k_rows = torch.zeros_like(k_rows)
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_real]
    backbone_out = model.backbone(k_rows, v_rows, chunks.chunk_mask[:, :n_real], pos)
    return model.decoder(backbone_out + pos, chunks.token_mask[:, :n_real])


@torch.no_grad()
def eval_arm(model, ns, windows, masks, device, arm: str) -> float:
    """completion_acc over the 16-window eval-seed-1042 protocol (natural
    states, full store minus the nulled rows) — _eval_acc's natural/full cell
    with the null transform inserted."""
    gen = torch.Generator().manual_seed(777)
    hits = slots = 0
    for clean, bm in zip(windows, masks):
        clean, bm = clean.to(device), bm.to(device)
        source = clean.masked_fill(bm, MASK_ID)
        chunks, n_real, S, k_rows = _states_for(model, source, False)
        if arm == "real":
            logits = _chain_logits(model, chunks, n_real, S, k_rows)
        else:
            logits = _chain_logits_nulled(model, chunks, n_real, S, k_rows, arm, gen)
        targets, slot_mask, _m, _t = s1.make_cumulative_retention_targets(
            clean, bm, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
        )
        pred = logits.argmax(dim=-1)
        sel = slot_mask[:, :n_real]
        hits += int((pred.eq(targets[:, :n_real]) & sel).sum())
        slots += int(sel.sum())
    return round(hits / max(slots, 1), 4)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--eval-windows", type=int, default=16)
    p.add_argument("--out-dir", default="outputs/audit_measurements_20260819")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    results = []
    windows = masks = None
    for label, pkg_path, expected in PACKAGES:
        pkg = torch.load(pkg_path, map_location="cpu", weights_only=False)
        model, ns, step = load_model(Path(pkg["args"]["run_dir"]), device)
        overlay(model, pkg)
        # E75 warm-buffer protocol: the 40K/20K retrains ran with a LIVE
        # k_center EMA (training mode); a fresh process starts cold (buffer
        # zero = centering off), so warm it or the real arm cannot reproduce
        # the reported plateaus. No-op when to_k_center is off.
        hay_args = Namespace(data_path=ns.data_path, eval_data_root=str(ph.EVAL_DATA), suite="ruler/niah_single_1.jsonl")
        _src, hay_fn = archive_probe.make_haystack_fn(hay_args)
        archive_probe._warm_k_center(model, hay_fn, ns.seq_len, device)
        if windows is None:
            windows = build_eval_windows(ns, args.eval_windows)
            masks = build_masks(windows, ns)
            print(f"[floor] {len(windows)} eval windows ready ({time.time() - t0:.0f}s)", flush=True)
        arms = {}
        for arm in ARMS:
            arms[arm] = eval_arm(model, ns, windows, masks, device, arm)
            print(f"[floor] {label} {arm}: {arms[arm]:.4f} ({time.time() - t0:.0f}s)", flush=True)
        repro_ok = abs(arms["real"] - expected) < 0.005
        results.append(
            {
                "label": label,
                "package": Path(pkg_path).parent.name,
                "pkg_step": pkg["step"],
                "arms": arms,
                "expected_real": expected,
                "real_arm_reproduces": repro_ok,
                "state_channel_share": round(arms["real"] - arms["zero_V"], 4),
                "store_total_share": round(arms["real"] - arms["zero_KV"], 4),
                "prior_floor": arms["zero_KV"],
            }
        )
        if not repro_ok:
            print(f"[floor][WARN] {label}: real arm {arms['real']} != expected {expected} — check wiring", flush=True)
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    report = {
        "probe": "补全形态先验盲猜地板 (0.3185/0.0722 去水分, null-store completion eval)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "protocol": "16 eval windows (seed 42+9999), eval masks (seed 1042), natural states, "
        "completion clean cumulative grid — retrain_readout_chain._eval_acc natural/full cell "
        "with store-row nulling after the readout",
        "arms_legend": {
            "real": "原态对照 (must reproduce E87 0.3185 / E86 0.0722)",
            "shuffle_V": "V 状态行跨 chunk 置乱 (K 直通保留)",
            "zero_V": "V 状态行全零",
            "shuffle_KV": "K/V 同时置乱 (纯先验)",
            "zero_KV": "K/V 同时全零 (最严先验地板)",
        },
        "results": results,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "completion_prior_floor.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[floor] report -> {out_path} ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
