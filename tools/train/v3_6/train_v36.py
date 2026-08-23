"""FLUED v3.6 trainer: whole-prompt single-readout codec training.

Two mask-native tasks share the global span decoder: task 1 decodes from the
readout package directly (precise restore), task 2 routes the package through
the backbone (full restore); the strict masked-source protocol (5%, span 1-8,
mask before encode) is native to both. Boundary is dynamic by default
(tau_cut over segmentor confidence with UTF-8 continuation guard and
capacity-safe cuts); canonical runs take over a S0-pretrained
byte_lookup/encoder/segmentor via --init-checkpoint + --freeze-prefixes.

Guards per run: truncated_tokens == 0, NaN skip counter, pre-clip grad norm.
Artifacts per run dir: resolved_config.json, train_log.jsonl, latest.pt,
step_XXXX.pt milestones, summary.json.
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
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.train.v3_3.train_v33 import (  # noqa: E402
    _append_jsonl,
    _cosine_with_warmup,
    _safe_acc,
    build_optimizer,
    make_byte_mask,
    make_dataloaders,
    make_targets,
)
from flued.data import MASK_ID, PAD_ID  # noqa: E402
from flued.v36 import FLUEDV36, V36Config  # noqa: E402


def build_model(args: Namespace) -> FLUEDV36:
    return FLUEDV36(
        V36Config(
            d_byte=args.d_byte,
            encoder_layers=args.encoder_layers,
            segmentor_layers=args.segmentor_layers,
            nhead=args.nhead,
            ffn_dim=args.ffn_dim,
            d_mem=args.d_mem,
            summarizer_slots=args.summarizer_slots,
            summarizer_hidden=args.summarizer_hidden,
            kda_heads=args.kda_heads,
            kda_head_k=args.kda_head_k,
            kda_head_v=args.kda_head_v,
            write_hidden=args.write_hidden,
            kda_tau_max=args.kda_tau_max,
            readout_queries=args.readout_queries,
            d_pack=args.d_pack,
            d_backbone=args.d_backbone,
            backbone_layers=args.backbone_layers,
            backbone_nhead=args.backbone_nhead,
            backbone_ffn=args.backbone_ffn,
            backbone_mode=getattr(args, "backbone_mode", "attn"),
            backbone_readout=getattr(args, "backbone_readout", "per_chunk"),
            paged_reads=getattr(args, "paged_reads", 4),
            think_steps_min=getattr(args, "think_steps_min", 1),
            think_steps_max=getattr(args, "think_steps_max", 16),
            think_visibility=getattr(args, "think_visibility", "readout"),
            think_stop_cos=getattr(args, "think_stop_cos", 0.995),
            draft_init=getattr(args, "draft_init", "noise"),
            draft_inject=getattr(args, "draft_inject", "cross"),
            draft_depth_dist=getattr(args, "draft_depth_dist", "uniform"),
            draft_trunc_bptt=getattr(args, "draft_trunc_bptt", 0),
            draft_sandwich=getattr(args, "draft_sandwich", False),
            draft_mem_pos=getattr(args, "draft_mem_pos", False),
            draft_intermediate_weight=getattr(args, "draft_intermediate_weight", 0.0),
            decoder_markov=getattr(args, "decoder_markov", 0),
            xcache_frac=getattr(args, "xcache_frac", 1.0),
            xcache_gist=getattr(args, "xcache_gist", False),
            k_row_source=getattr(args, "k_row_source", "memory"),
            v_row_source=getattr(args, "v_row_source", "memory"),
            k_pos_inject=getattr(args, "k_pos_inject", False),
            k_block_eval=getattr(args, "k_block_eval", False),
            seed_source=getattr(args, "seed_source", "v"),
            to_k_center=getattr(args, "to_k_center", False),
            to_k_whiten=getattr(args, "to_k_whiten", False),
            pos_prior_keys=getattr(args, "pos_prior_keys", False),
            summarizer_pool=getattr(args, "summarizer_pool", "mean"),
            summarizer_aux_recon=getattr(args, "summarizer_aux_recon", False),
            summarizer_aux_weight=getattr(args, "summarizer_aux_weight", 0.1),
            split_trunk=getattr(args, "split_trunk", False),
            readout_views=getattr(args, "readout_views", 1),
            xcache_supp=getattr(args, "xcache_supp", 0),
            supp_source=getattr(args, "supp_source", "state"),
            residual_gate_temp=getattr(args, "residual_gate_temp", 1.0),
            paged_cache_rows=getattr(args, "paged_cache_rows", 1),
            decoder_hidden=args.decoder_hidden,
            decoder_layers=args.decoder_layers,
            max_chunks=args.max_chunks,
            max_span=args.max_span,
            bytes_per_chunk=args.bytes_per_chunk,
            tau_cut=args.tau_cut,
            tau_trans=args.tau_trans,
            boundary_mode=args.boundary_mode,
            boundary_temperature=args.boundary_temperature,
            boundary_bridge_gradient_scale=args.boundary_bridge_gradient_scale,
            max_positions=args.max_positions,
            per_chunk_readout=args.per_chunk_readout,
            summarizer_type=args.summarizer_type,
            summarizer_dit_layers=args.summarizer_dit_layers,
            prefix_task=args.prefix_task,
            prefix_positions=args.prefix_positions,
            kda_impl=args.kda_impl,
            recurrence=getattr(args, "recurrence", "kda"),
            state_channel=getattr(args, "state_channel", True),
        )
    )


def _ce(logits: torch.Tensor, targets: torch.Tensor, select: torch.Tensor) -> torch.Tensor:
    picked_logits = logits[select]
    picked_targets = targets[select]
    if picked_targets.numel() == 0:
        return logits.sum() * 0.0
    return F.cross_entropy(picked_logits.float(), picked_targets.clamp(min=0, max=257), ignore_index=PAD_ID)


def step_model(model, batch, args, device, train: bool):
    clean = batch[0].to(device)
    valid = clean.ne(PAD_ID)
    byte_mask = make_byte_mask(valid, args.mask_prob, args.mask_span_min, args.mask_span_max)
    source = clean.masked_fill(byte_mask, MASK_ID)
    with torch.autocast("cuda", dtype=torch.bfloat16, enabled=args.amp and device.type == "cuda"):
        out = model(source)
    targets, slot_mask, masked_slot = make_targets(
        clean, byte_mask, out.chunks.chunk_ids, out.chunks.offsets, args.max_chunks, args.max_span
    )
    direct_loss = _ce(out.logits_direct, targets, slot_mask)
    backbone_loss = _ce(out.logits_backbone, targets, slot_mask)
    loss = args.task1_loss_weight * direct_loss + args.task2_loss_weight * backbone_loss
    unmasked_slot = slot_mask & ~masked_slot
    if getattr(args, "prefix_task", False) and out.prefix:
        d_losses, b_losses = [], []
        for i, ld, lb in out.prefix:
            t_i = targets[:, : i + 1]
            sm_i = slot_mask[:, : i + 1]
            d_losses.append(_ce(ld, t_i, sm_i))
            b_losses.append(_ce(lb, t_i, sm_i))
        direct_loss = torch.stack(d_losses).mean()
        backbone_loss = torch.stack(b_losses).mean()
        loss = args.task1_loss_weight * direct_loss + args.task2_loss_weight * backbone_loss
    metrics = {
        "loss": float(loss.item()),
        "direct_loss": float(direct_loss.item()),
        "backbone_loss": float(backbone_loss.item()),
        "direct_acc": _safe_acc(out.logits_direct.argmax(dim=-1), targets, slot_mask),
        "backbone_acc": _safe_acc(out.logits_backbone.argmax(dim=-1), targets, slot_mask),
        "backbone_masked_acc": _safe_acc(out.logits_backbone.argmax(dim=-1), targets, masked_slot),
        "backbone_unmasked_acc": _safe_acc(out.logits_backbone.argmax(dim=-1), targets, unmasked_slot),
        "direct_masked_acc": _safe_acc(out.logits_direct.argmax(dim=-1), targets, masked_slot),
        "truncated_tokens": float(out.chunks.pack_info["truncated_tokens"].float().sum().item()),
        "cut_capacity_overflow": float(out.aux["cut_capacity_overflow"]),
        "chunks_per_sample": float(out.chunks.chunk_mask.float().sum(dim=1).mean().item()),
        "hard_cut_fraction": float(out.aux["hard_cut_fraction"].item()),
        "state_norm": float(out.state_norm.item()),
        "boundary_confidence_mean": float(out.aux["boundary_confidence_mean"].item()),
    }
    if getattr(args, "prefix_task", False) and out.prefix:
        last_i = out.prefix[-1][0]
        for i, _ld, lb in out.prefix:
            t_i = targets[:, : i + 1]
            sm_i = slot_mask[:, : i + 1]
            bucket = int(round(8 * i / max(last_i, 1)))
            metrics[f"prefix_acc_q{bucket}"] = _safe_acc(lb.argmax(dim=-1), t_i, sm_i)
    return loss, metrics


@torch.no_grad()
def evaluate(model, eval_loader, args, device):
    model.eval()
    torch.manual_seed(args.eval_mask_seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(args.eval_mask_seed)
    rows = []
    for i, batch in enumerate(eval_loader):
        if i >= args.max_eval_batches:
            break
        _, metrics = step_model(model, batch, args, device, train=False)
        rows.append(metrics)
    verify_rows = {}
    if getattr(args, "verify_topl", 0) > 0:
        # fork 2 forward-verification pass (default off; re-iterates the eval
        # loader with the same reseed so the byte masks are identical)
        from tools.eval.forward_verifier import verify_completion_eval

        verify_rows = verify_completion_eval(model, eval_loader, args, device)
    model.train()
    merged = {}
    for key in rows[0]:
        merged[f"eval_{key}"] = sum(r[key] for r in rows) / len(rows)
    merged["eval_backbone_ppl"] = float(math.exp(min(merged["eval_backbone_loss"], 20.0)))
    merged["eval_direct_ppl"] = float(math.exp(min(merged["eval_direct_loss"], 20.0)))
    merged.update(verify_rows)
    return merged


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="")
    parser.add_argument("--run-id", default="v36_v0")
    parser.add_argument("--out-dir", default="checkpoints/v36_v0")
    parser.add_argument("--data-path", default="")
    parser.add_argument("--data-manifest", default="")
    parser.add_argument("--streaming-train", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--streaming-eval", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--stream-samples-per-worker", type=int, default=50000)
    parser.add_argument("--seq-len", type=int, default=512)
    parser.add_argument("--stride", type=int, default=512)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-steps", type=int, default=20000)
    parser.add_argument("--max-eval-batches", type=int, default=16)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--prefetch-factor", type=int, default=2)
    parser.add_argument("--eval-max-lines", type=int, default=20000)
    parser.add_argument("--max-lines", type=int, default=200000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--eval-mask-seed", type=int, default=1042)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--amp", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--d-byte", type=int, default=384)
    parser.add_argument("--encoder-layers", type=int, default=3)
    parser.add_argument("--segmentor-layers", type=int, default=9)
    parser.add_argument("--nhead", type=int, default=6)
    parser.add_argument("--ffn-dim", type=int, default=1152)
    parser.add_argument("--d-mem", type=int, default=512)
    parser.add_argument("--summarizer-slots", type=int, default=4)
    parser.add_argument("--summarizer-hidden", type=int, default=1024)
    parser.add_argument("--kda-heads", type=int, default=4)
    parser.add_argument("--kda-head-k", type=int, default=128)
    parser.add_argument("--kda-head-v", type=int, default=256)
    parser.add_argument("--write-hidden", type=int, default=1024)
    parser.add_argument("--kda-tau-max", type=float, default=256.0)
    parser.add_argument("--readout-queries", type=int, default=1)
    parser.add_argument("--d-pack", type=int, default=1536)
    parser.add_argument("--d-backbone", type=int, default=384)
    parser.add_argument("--backbone-layers", type=int, default=3)
    parser.add_argument("--backbone-nhead", type=int, default=8)
    parser.add_argument("--backbone-ffn", type=int, default=1024)
    parser.add_argument("--backbone-mode", choices=["attn", "mlp", "xattn", "draft", "paged_xattn", "slm"], default="attn")
    parser.add_argument(
        "--backbone-readout",
        choices=["per_chunk", "final", "paged"],
        default="per_chunk",
        help="final = k=1 backbone interface (only the final state readout); "
        "paged = /n paging (one causal read per sub-page boundary)",
    )
    parser.add_argument("--paged-reads", type=int, default=4)
    parser.add_argument("--paged-cache-rows", type=int, default=1)
    parser.add_argument("--think-steps-min", type=int, default=1)
    parser.add_argument("--think-steps-max", type=int, default=16)
    parser.add_argument(
        "--think-visibility",
        choices=["readout", "readout_memory"],
        default="readout",
        help="draft backbone (spec SS23): readout = thinking sees only the k=1 "
        "readout (arm A); readout_memory = thinking may also cross-read "
        "pre-state memory rows (arm B); causal honesty sits at the input level",
    )
    parser.add_argument("--think-stop-cos", type=float, default=0.995)
    parser.add_argument("--draft-init", choices=["noise", "content_seed"], default="noise")
    parser.add_argument("--draft-inject", choices=["cross", "concat"], default="cross")
    parser.add_argument("--draft-depth-dist", choices=["uniform", "poisson"], default="uniform")
    parser.add_argument("--draft-trunc-bptt", type=int, default=0)
    parser.add_argument("--draft-sandwich", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--draft-mem-pos", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--draft-intermediate-weight", type=float, default=0.0)
    parser.add_argument(
        "--decoder-markov",
        type=int,
        default=0,
        help="rank of the DSpark-style bigram Markov head on the decoder "
        "(0=off; teacher-forced protocol, arms comparable only among themselves; "
        "wired in train_v36_s1.py only)",
    )
    parser.add_argument("--xcache-frac", type=float, default=1.0)
    parser.add_argument(
        "--xcache-gist",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="S36: prepend the k=1 final readout as a gist token to the "
        "cross-read store; with --xcache-frac<1 the memory rows are "
        "residual-gated (HOLA/HAM)",
    )
    parser.add_argument(
        "--k-row-source",
        choices=["memory", "state", "index"],
        default="memory",
        help="S39 stage-1 taxonomy: K source for the xattn store rows -- "
        "memory = pre-state memory rows (default, existing behavior); "
        "state = per-chunk state readouts (content) via a dedicated projection; "
        "index = summarizer index rows (v3.7 slm mode only)",
    )
    parser.add_argument(
        "--v-row-source",
        choices=["memory", "state"],
        default="memory",
        help="S39 stage-1 taxonomy: V source for the xattn store rows "
        "(same convention as --k-row-source)",
    )
    parser.add_argument(
        "--k-pos-inject",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="S39 a+pos arm: add sinusoidal (segment order, window-relative "
        "start byte) key-row features to the K side through a zero-init "
        "scalar gate; legacy/xattn path requires --k-row-source/--v-row-source "
        "memory; v3.7 slm path requires k=index and v=memory (model raises "
        "otherwise)",
    )
    parser.add_argument(
        "--k-block-eval",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="S39 K-block eval probe (user-ruled 2026-08-17): zero the aligned "
        "K rows at eval so block-1 cross-attention is uniform -- tests whether "
        "the slm backbone actually reads the index channel. Eval-time only.",
    )
    parser.add_argument(
        "--seed-source",
        choices=["v", "k"],
        default="v",
        help="S39 K-seed arm (user-ruled 2026-08-17): which aligned row seeds "
        "the slm backbone hidden state -- v = V/memory row (default, "
        "consensus §1.3); k = index row, forcing content through K/V "
        "retrieval (index channel becomes load-bearing)",
    )
    parser.add_argument(
        "--to-k-center",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="E75 key-decollapse hard constraint (2026-08-18): WriteHead "
        "subtracts a running center (EMA 0.99, detached, BatchNorm-style cold "
        "start) from the to_k output pre-normalization; eval uses the frozen "
        "buffer (persistent=False -- old checkpoints load strict-clean and "
        "stats re-estimate online from zero). Covers both WriteHead instances. "
        "Default off = bit-preserved legacy paths.",
    )
    parser.add_argument(
        "--to-k-whiten",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Q10 hard-constraint gate (user-ruled 2026-08-20): WriteHead "
        "whitens the to_k output pre-normalization — k <- (k - EMA_mean) @ "
        "(EMA_cov + eps I)^{-1/2} (eigh, fp32, refreshed every training "
        "step). Superset of --to-k-center (includes de-meaning; do not stack "
        "the two flags). E79 showed de-mean-only surgery slowly re-collapses "
        "(mu 0.690 -> 0.811); whitening crushes pairwise |cos| toward ~0 by "
        "construction. Same buffer discipline as --to-k-center (persistent="
        "False; fresh eval processes start with identity whitening until a "
        "training-mode forward warms the buffers). Default off = bit-"
        "preserved legacy paths.",
    )
    parser.add_argument(
        "--pos-prior-keys",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="recruitment-arm B (user-ruled 2026-08-22, prereg §2): write "
        "keys = FIXED random vectors per absolute chunk position (seeded "
        "table, content-independent strong prior) — the diagnostic arm "
        "answering 'is position the true index?'. Values/beta stay "
        "content-driven; only the key path is replaced. Default off = "
        "bit-preserved legacy paths.",
    )
    parser.add_argument(
        "--summarizer-pool",
        choices=["mean", "qpool", "poswmean"],
        default="mean",
        help="fork 3 F3 (user-ruled 2026-08-22, E92 position-sink evidence): "
        "DiT summarizer pooling form — mean = masked mean (default, "
        "bit-preserved); qpool = 4 position-anchored attention queries "
        "(anti-slot-collapse Gaussian bias); poswmean = zero-param "
        "position-weighted mean (F3z SGPT-family control).",
    )
    parser.add_argument(
        "--summarizer-aux-recon",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="fork 3 F2 (user-ruled 2026-08-21): train-time-only auxiliary "
        "per-slot byte-reconstruction head on the summarizer's memory rows "
        "(the H-obj arm: the tail bytes never enter the memory row, E89/E95). "
        "Small head (2-layer MLP + slot table, ~1.9M params — scout capacity "
        "cap against decoder explain-away); removed at inference. Verdict "
        "lines are the probe profiles, never the aux loss. Default off = "
        "bit-preserved legacy paths.",
    )
    parser.add_argument(
        "--summarizer-aux-weight",
        type=float,
        default=0.1,
        help="fork 3 F2: weight of the auxiliary reconstruction loss on top "
        "of the main tasks (pre-registered 0.1).",
    )
    parser.add_argument(
        "--split-trunk",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="E79 split-trunk (2026-08-18): WriteHead holds two independent "
        "trunks (trunk_k -> to_k; trunk_v -> to_v/to_beta/to_b/to_w) so "
        "to_k-side training dynamics (e.g. --to-k-center) cannot deform value "
        "content through a shared trunk. Default off = shared trunk, "
        "bit-preserved legacy paths. Composes with --to-k-center.",
    )
    parser.add_argument(
        "--readout-views",
        type=int,
        default=1,
        help="fork 2 multi-view readout (2026-08-19): m>1 expands each state "
        "channel's backbone-store rows to m measurement rows per chunk read "
        "with a seeded orthogonal frame (training-free, seed pinned in "
        "flued/v36/model.py); direct/predict paths bit-untouched. Default 1 = "
        "bit-preserved legacy behavior.",
    )
    parser.add_argument(
        "--verify-topl",
        type=int,
        default=0,
        help="fork 2 forward verification (2026-08-19, spec §1.2): at eval, "
        "take the completion decoder's exact top-L per-chunk segment "
        "candidates, replay each through the frozen write operator (original "
        "timetable), and pick the nearest to the chunk's trained state "
        "readout in a seeded-frame measurement space; reports "
        "eval_verify_hit1_before/after, eval_verify_hitl and the false-peak "
        "rate. 0 = off (default, bit-preserved legacy eval). Wired in "
        "train_v36.py evaluate() only; slm + --v-row-source state grids.",
    )
    parser.add_argument(
        "--cloze-prob",
        type=float,
        default=0.0,
        help="v3.7 slm cloze 检索回执 (user-ruled 2026-08-17): per-window "
        "probability of splicing one --cloze-bank passage into the window's "
        "first 60%% (UTF-8-snapped offset) and appending "
        "'\\n'+query+'\\n答案是：'+answer at the tail; the passage answer is "
        "force-UNMASKED (E23), the echo answer force-MASKED, byte CE on the "
        "echo slots rides the completion conditioning. Wired in "
        "train_v36_s1.py only, slm mode only; default 0.0 = off, "
        "bitwise-identical legacy path.",
    )
    parser.add_argument(
        "--cloze-weight",
        type=float,
        default=0.3,
        help="loss weight of the cloze task; added ON TOP of the three main "
        "tasks (their weights are untouched)",
    )
    parser.add_argument(
        "--cloze-bank",
        type=str,
        default="",
        help="cloze bank JSONL ({\"id\",\"passage\",\"answer\",\"query\",\"answer_bytes\"}; "
        "tools/data/mine_cloze_bank.py contract); required when --cloze-prob>0",
    )
    parser.add_argument(
        "--retrieval-prob",
        type=float,
        default=0.0,
        help="v3.7 自然检索任务 (招募臂, prereg "
        "docs/versions/v3.7/FLUED_V3_7_RECRUITMENT_ARM_NATURAL_RETRIEVAL_20260821_CN.md): "
        "per-window probability of picking one 32-64B in-window fragment, "
        "blanking one ASCII word W in the tail question "
        "('前文'<F with W -> ___>'空格处是什么？') and appending "
        "'答案是：'+W as the echo; the echo is force-MASKED, the source W "
        "force-UNMASKED (it must enter the state), byte CE on the echo slots "
        "rides the completion conditioning. Wired in train_v36_s1.py only, "
        "slm mode only, mutually exclusive with --cloze-prob>0; default 0.0 "
        "= off, bitwise-identical legacy path.",
    )
    parser.add_argument(
        "--retrieval-weight",
        type=float,
        default=1.0,
        help="loss weight of the natural retrieval task; added ON TOP of the "
        "three main tasks (their weights are untouched)",
    )
    parser.add_argument(
        "--retrieval-block-prob",
        type=float,
        default=0.0,
        help="r = 档 a 掩码级剔除比例 (prereg §4): per spliced sample, "
        "probability of excising the source fragment's store rows from every "
        "query position at/after the question's first chunk (store_block "
        "thread, SLMBackbone), forcing K->state->readout. Must lie in [0, 1]; "
        "preregistered ramp {0 -> 0.5 -> 1.0}.",
    )
    parser.add_argument(
        "--retrieval-answer-mode",
        choices=["cjk", "ascii"],
        default="cjk",
        help="Q11 v2 (user-ruled 2026-08-21): answer granularity — cjk = "
        "2–4 char small segment from non-boundary runs (main arm, activation "
        "~1.0); ascii = maximal [A-Za-z]{3,10} word (control/replication arm). "
        "Both retry fragment draws up to N=8 before marking the row inactive.",
    )
    parser.add_argument(
        "--retrieval-block-ramp",
        type=str,
        default="",
        help="Q11 r 爬坡 (prereg §4): 'r:step,r:step,...' schedule, e.g. "
        "'0:0,0.5:5000,1.0:10000' — r applies from its step onward (each tier "
        ">=5K steps per prereg). Empty = fixed --retrieval-block-prob.",
    )
    parser.add_argument(
        "--retrieval-examples",
        type=int,
        default=0,
        help="Q12 示例密集型招募臂 (修订案 v3, 2026-08-22 冻结): 2–4 = per "
        "sample prepend that many COMPLETE examples (same 前文/答案是 format, "
        "answer visible + force-unmasked) before the one masked-answer query; "
        "example/query roles randomized, query answer never a byte-substring "
        "of any example, example source spans/contents distinct from the "
        "query's (violations redraw up to N=8, then inactive); window budget "
        "(A2②): source/query never truncated, overflow drops the earliest "
        "examples first (retrieval_drop_rate), query pushed off the chunk "
        "grid = construction defect (retrieval_defect); per-batch occupancy "
        "logged as retrieval_budget_ratio. 0 = the example-free form, "
        "bitwise-identical. Requires --retrieval-prob>0; same slm-only and "
        "cloze-mutex rules.",
    )
    parser.add_argument(
        "--burst-prob",
        type=float,
        default=0.0,
        help="Q13 突发性注入臂 (prereg "
        "docs/versions/v3_7/FLUED_V3_7_Q13_BURSTINESS_INJECTION_20260822_CN.md, "
        "frozen 2026-08-22): per-window probability of inserting ONE fresh "
        "32-64B corpus segment (random file offset, 防背护栏: (偏移,长度) "
        "进程级登记, 同 epoch 重复采中重抽 N=8 后响亮报错, 严禁固定段库) "
        "verbatim at R=3 random in-window positions; the last occurrence's "
        "trailing 2-4 CJK chars are force-MASKED, the R-1 earlier "
        "occurrences force-UNMASKED. No new loss term (注入只改数据分布); "
        "metrics burst_tail_byte_acc/burst_tail_exact/burst_count/"
        "burst_tail_chars. Wired in train_v36_s1.py only, slm mode only, "
        "mutually exclusive with --cloze-prob>0 and --retrieval-prob>0; "
        "default 0.0 = off, bitwise-identical legacy path.",
    )
    parser.add_argument(
        "--burst-repeat",
        type=int,
        default=3,
        help="Q13 frozen value R=3 (prereg §2 逐字重复插入 3 次) — "
        "parser-visible for logging, any other value fails loudly.",
    )
    parser.add_argument(
        "--burst-tail-max-chars",
        type=int,
        default=4,
        help="Q13 frozen range: masked tail = last 2-4 CJK chars of the R-th "
        "occurrence (per-sample draw); out-of-[2,4] values fail loudly.",
    )
    parser.add_argument(
        "--xcache-supp",
        type=int,
        default=0,
        help="S38: number of supplementary content-conditioned state readouts "
        "for the hardest uncached chunks (requires --xcache-gist)",
    )
    parser.add_argument("--supp-source", choices=["state", "residual"], default="state")
    parser.add_argument("--residual-gate-temp", type=float, default=1.0)
    parser.add_argument("--decoder-hidden", type=int, default=1024)
    parser.add_argument("--decoder-layers", type=int, default=3)
    parser.add_argument("--max-chunks", type=int, default=64)
    parser.add_argument("--max-span", type=int, default=64)
    parser.add_argument("--bytes-per-chunk", type=int, default=16)
    parser.add_argument("--tau-cut", type=float, default=0.94)
    parser.add_argument("--tau-trans", type=float, default=0.75)
    parser.add_argument("--boundary-mode", choices=["dynamic", "uniform"], default="dynamic")
    parser.add_argument("--boundary-temperature", type=float, default=0.15)
    parser.add_argument("--boundary-bridge-gradient-scale", type=float, default=0.1)
    parser.add_argument("--max-positions", type=int, default=64)
    parser.add_argument("--per-chunk-readout", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--summarizer-type", choices=["slot", "dit"], default="dit")
    parser.add_argument("--summarizer-dit-layers", type=int, default=2)
    parser.add_argument("--prefix-task", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--prefix-positions", type=int, default=4)
    parser.add_argument("--kda-impl", choices=["torch", "fla"], default="fla")
    parser.add_argument(
        "--recurrence",
        choices=["kda", "gdn2"],
        default="kda",
        help="state-machine write rule: kda = shared scalar beta gates both "
        "erase and write (default, canonical); gdn2 = erase/write gate "
        "decoupling (per-K-channel erase gate b + per-V-channel write gate w "
        "replace beta; decay and delta form unchanged) -- S39 stage-2 "
        "single-variable arm (S39_STAGED_MATRIX_PLAN_20260817 appendix A)",
    )
    parser.add_argument(
        "--state-channel",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="off = R1 relative baseline: per-chunk readout straight from the "
        "write, no serial KDA state channel (spec section 4)",
    )
    parser.add_argument("--eval-only", default="", help="path to a checkpoint; run evaluate() on it and exit")
    parser.add_argument("--mask-prob", type=float, default=0.05)
    parser.add_argument("--mask-span-min", type=int, default=1)
    parser.add_argument("--mask-span-max", type=int, default=8)
    parser.add_argument("--task1-loss-weight", type=float, default=1.0)
    parser.add_argument("--task2-loss-weight", type=float, default=1.0)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--weight-decay", type=float, default=0.01)
    parser.add_argument("--optimizer", default="fused_adamw")
    parser.add_argument("--warmup-steps", type=int, default=200)
    parser.add_argument(
        "--lr-const-after-resume",
        type=float,
        default=0.0,
        help="Q12 40K 延长臂（用户冻结 2026-08-22）：resume 后不复用旧 cosine "
        "尾段——重置 base lr 后 re-warmup --lr-rewarmup 步、随后恒定本值至 "
        "max-steps。0 = 常规 cosine 调度。",
    )
    parser.add_argument(
        "--lr-rewarmup",
        type=int,
        default=200,
        help="--lr-const-after-resume 的 re-warmup 步数（冻结 200）。",
    )
    parser.add_argument("--grad-clip", type=float, default=1.0)
    parser.add_argument("--log-every", type=int, default=20)
    parser.add_argument("--ckpt-every", type=int, default=1000)
    parser.add_argument("--milestone-every", type=int, default=3000)
    parser.add_argument("--save-optimizer", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--init-checkpoint", default="")
    parser.add_argument("--init-prefixes", default="", help="comma-separated; only load matching prefixes from init checkpoint (rest stays freshly initialized)")
    parser.add_argument("--freeze-prefixes", default="")
    return parser


def main() -> None:
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--config", default="")
    pre_args, _ = pre.parse_known_args()
    parser = build_parser()
    if pre_args.config:
        parser.set_defaults(**json.loads(Path(pre_args.config).read_text(encoding="utf-8")))
    args = parser.parse_args()
    if getattr(args, "cloze_prob", 0.0) > 0:
        raise SystemExit(
            "--cloze-prob>0 is wired in the S1 trainer only: run "
            "tools/train/v3_6/train_v36_s1.py (v3.7 slm cloze 检索回执, "
            "user-ruled 2026-08-17)"
        )
    if getattr(args, "retrieval_prob", 0.0) > 0:
        raise SystemExit(
            "--retrieval-prob>0 is wired in the S1 trainer only: run "
            "tools/train/v3_6/train_v36_s1.py (v3.7 自然检索任务, 招募臂 "
            "prereg 2026-08-21)"
        )
    if getattr(args, "burst_prob", 0.0) > 0:
        raise SystemExit(
            "--burst-prob>0 is wired in the S1 trainer only: run "
            "tools/train/v3_6/train_v36_s1.py (Q13 突发性注入臂, prereg 2026-08-22)"
        )

    device = torch.device(args.device if args.device == "cpu" or torch.cuda.is_available() else "cpu")
    torch.manual_seed(args.seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(args.seed)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "resolved_config.json").write_text(json.dumps(vars(args), indent=2), encoding="utf-8")

    model = build_model(args).to(device)
    if args.eval_only:
        payload = torch.load(args.eval_only, map_location=device, weights_only=False)
        model.load_state_dict(payload["model"], strict=True)
        model.eval()
        _t, eval_loader = make_dataloaders(args)
        stats = evaluate(model, eval_loader, args, device)
        print(json.dumps(stats, ensure_ascii=False, indent=2), flush=True)
        return
    if args.init_checkpoint:
        payload = torch.load(args.init_checkpoint, map_location=device, weights_only=False)
        current = model.state_dict()
        compatible = {
            k: v for k, v in payload["model"].items() if k in current and current[k].shape == v.shape
        }
        init_prefixes = [p.strip() for p in args.init_prefixes.split(",") if p.strip()]
        if init_prefixes:
            compatible = {
                k: v for k, v in compatible.items() if any(k.startswith(p) for p in init_prefixes)
            }
        model.load_state_dict(compatible, strict=False)
        print(
            f"[v36] init from {args.init_checkpoint}: loaded={len(compatible)} skipped={len(payload['model']) - len(compatible)} prefixes={init_prefixes or 'ALL'}",
            flush=True,
        )
    frozen = [p.strip() for p in args.freeze_prefixes.split(",") if p.strip()]
    if frozen:
        n_frozen = 0
        for name, param in model.named_parameters():
            if any(name.startswith(prefix) for prefix in frozen):
                param.requires_grad_(False)
                n_frozen += 1
        print(f"[v36] frozen params={n_frozen} prefixes={frozen}", flush=True)
    trainable = [p for p in model.parameters() if p.requires_grad]
    opt = build_optimizer(args, iter(trainable))
    sched = _cosine_with_warmup(opt, args.warmup_steps, args.max_steps)
    train_loader, eval_loader = make_dataloaders(args)

    start_step = 0
    latest = out_dir / "latest.pt"
    if args.resume and latest.exists():
        payload = torch.load(latest, map_location=device, weights_only=False)
        model.load_state_dict(payload["model"])
        if args.save_optimizer and "optimizer" in payload:
            opt.load_state_dict(payload["optimizer"])
        start_step = int(payload.get("step", 0))
        if start_step > 0:
            sched.step(start_step)
        print(f"[v36] resumed from step {start_step}", flush=True)

    log_path = out_dir / "train_log.jsonl"
    model.train()
    t0 = time.time()
    nan_skips = 0
    step = start_step
    while step < args.max_steps:
        for batch in train_loader:
            if step >= args.max_steps:
                break
            loss, metrics = step_model(model, batch, args, device, train=True)
            if not torch.isfinite(loss):
                nan_skips += 1
                opt.zero_grad(set_to_none=True)
                step += 1
                sched.step()
                continue
            opt.zero_grad(set_to_none=True)
            loss.backward()
            grad = torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip)
            opt.step()
            sched.step()
            step += 1
            if step % args.log_every == 0 or step == 1:
                row = {
                    "step": step,
                    "lr": float(opt.param_groups[0]["lr"]),
                    "grad": float(grad.item()),
                    "steps_per_sec": step / max(time.time() - t0, 1e-9),
                    "nan_skips": nan_skips,
                    **metrics,
                }
                _append_jsonl(log_path, row)
            if step % args.ckpt_every == 0:
                payload = {"step": step, "model": model.state_dict(), "args": vars(args)}
                if args.save_optimizer:
                    payload["optimizer"] = opt.state_dict()
                torch.save(payload, latest)
            if step % args.milestone_every == 0:
                torch.save({"step": step, "model": model.state_dict(), "args": vars(args)}, out_dir / f"step_{step:06d}.pt")
        else:
            continue
        break

    payload = {"step": step, "model": model.state_dict(), "args": vars(args)}
    if args.save_optimizer:
        payload["optimizer"] = opt.state_dict()
    torch.save(payload, latest)

    eval_stats = evaluate(model, eval_loader, args, device)
    summary = {
        "run_id": args.run_id,
        "steps": step,
        "params": sum(p.numel() for p in model.parameters()),
        "elapsed_sec": time.time() - t0,
        "steps_per_sec": step / max(time.time() - t0, 1e-9),
        "nan_skips": nan_skips,
        "args": vars(args),
        **eval_stats,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
