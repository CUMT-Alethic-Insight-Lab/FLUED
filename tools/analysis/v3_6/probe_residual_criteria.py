"""Residual-criteria probe for the S36 residual-gated cache (HOLA/HAM).

Answers, on a trained xattn checkpoint (e.g. s31), BEFORE any S36 training:
  1. distribution of per-chunk residuals (is the mass concentrated enough for
     a budget to make sense?);
  2. rank correlation between each candidate write criterion and the per-chunk
     backbone completion error:
       - write residual ||e_i|| = ||v_i - S_{i-1}^T k_i|| from the delta update
         (HOLA; needs the torch KDA path -- we force kda_impl=torch here)
       - direct-decode CE per chunk (HAM-style prediction error, the online
         criterion S36 actually uses);
  3. how much backbone error mass the top-frac chunks cover for frac in a grid
     (the expected RD shape of the budget sweep).

Usage:
  python probe_residual_criteria.py --data-path <corpus> --run-dir <s31_dir> [--batches 2]
"""

from __future__ import annotations

import argparse
import json
import sys
from argparse import Namespace
from pathlib import Path

import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.train.v3_3.train_v33 import make_dataloaders, make_targets  # noqa: E402
from tools.train.v3_6.train_v36 import build_model  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402


def _spearman(a: torch.Tensor, b: torch.Tensor) -> float:
    ra = a.argsort().argsort().float()
    rb = b.argsort().argsort().float()
    ra = ra - ra.mean()
    rb = rb - rb.mean()
    return float((ra * rb).sum() / (ra.norm() * rb.norm()).clamp(min=1e-12))


@torch.no_grad()
def probe(run_dir: Path, data_path: str, args) -> dict:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_path"] = data_path
    cfg["data_manifest"] = ""
    cfg["kda_impl"] = "torch"  # the fla kernel does not expose per-chunk states
    ns = Namespace(**cfg)
    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed":
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    model = build_model(ns).to(device)
    payload = torch.load(run_dir / "latest.pt", map_location=device, weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    model.eval()
    _, eval_loader = make_dataloaders(ns)
    torch.manual_seed(ns.eval_mask_seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(ns.eval_mask_seed)
    s1._MASK_GENERATOR.manual_seed(ns.eval_mask_seed)

    rows = []
    for bi, batch in enumerate(eval_loader):
        if bi >= args.batches:
            break
        clean = batch[0].to(device)
        if getattr(ns, "mask_mode", "mixed") == "mixed":
            byte_mask = s1.make_mixed_mask(
                clean.cpu(), ns.mask_prob, char_frac=ns.mask_char_frac,
                char_span_max=ns.mask_char_span_max, tokenizer=s1._BPE_TOKENIZER,
                generator=s1._MASK_GENERATOR,
            ).to(device)
        else:
            byte_mask = s1.make_byte_mask(clean.ne(0), ns.mask_prob, ns.mask_span_min, ns.mask_span_max)
        source = clean.masked_fill(byte_mask, s1.MASK_ID)
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device.type == "cuda"):
            byte_states, confidence, valid, _ = model._encode(source)
            hard_cut, utf8_cont, _ = model._cuts(source, confidence, valid)
            chunks = model.chunk_builder(byte_states, valid, hard_cut, confidence)
            chunks = model.bridge(chunks, byte_states, confidence, valid, utf8_cont)
            memory = model.summarizer(chunks.span_embeddings, chunks.token_mask)
            gates = model.write_head(memory)
            package, _ = model.state_machine(gates, chunks.chunk_mask)
            content = package.mean(dim=2)
            n_chunks = chunks.chunk_mask.size(1)
            pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_chunks]
            cond_direct = model.decoder_in(content) + pos
            logits_direct = model.decoder(cond_direct, chunks.token_mask)
            backbone_out = model.backbone(content, memory, chunks.chunk_mask, pos)
            logits_backbone = model.decoder(backbone_out + pos, chunks.token_mask)
        targets, slot_mask, _ = make_targets(
            clean, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
        )

        def per_chunk_ce(logits):
            ce = F.cross_entropy(
                logits.float().reshape(-1, logits.size(-1)),
                targets.reshape(-1).clamp(min=0, max=257),
                reduction="none",
                ignore_index=0,
            ).reshape(targets.shape)
            return (ce * slot_mask.float()).sum(dim=-1) / slot_mask.float().sum(dim=-1).clamp(min=1.0)

        direct_ce = per_chunk_ce(logits_direct)
        backbone_ce = per_chunk_ce(logits_backbone)

        # HOLA write residual: ||v_i - S_{i-1}^T k_i|| replayed on the torch
        # recurrence (fp32), padded chunks contribute 0
        k, v, beta, alpha = gates["k"], gates["v"], gates["beta"], gates["alpha"]
        keep = chunks.chunk_mask
        kf, vf = k.float(), v.float()
        state = k.new_zeros(k.size(0), k.size(2), k.size(3), v.size(-1), dtype=torch.float32)
        alpha_eff = 1.0 - keep.float().view(*keep.shape, 1, 1, 1) + keep.float().view(*keep.shape, 1, 1, 1) * gates["alpha"][0].float().unsqueeze(0).unsqueeze(-1)
        write_resid = v.new_zeros(v.size(0), v.size(1), dtype=torch.float32)
        for i in range(v.size(1)):
            ki = kf[:, i]
            ai = alpha_eff[:, i]
            state = ai * state
            kTs = torch.einsum("bhk,bhkv->bhv", ki, state)
            err = vf[:, i] - kTs
            write_resid[:, i] = err.norm(dim=-1).mean(dim=-1)  # mean over heads
            bi = beta.float()[:, i] * keep.float()[:, i].unsqueeze(-1)
            state = state - bi.view(k.size(0), k.size(2), 1, 1) * ki.unsqueeze(-1) * kTs.unsqueeze(-2)
            state = state + bi.view(k.size(0), k.size(2), 1, 1) * ki.unsqueeze(-1) * vf[:, i].unsqueeze(-2)

        m = chunks.chunk_mask
        for b in range(clean.size(0)):
            n_real = int(m[b].sum())
            for i in range(n_real):
                rows.append(
                    {
                        "batch": bi,
                        "sample": b,
                        "chunk": i,
                        "frac_pos": i / max(n_real - 1, 1),
                        "write_resid": float(write_resid[b, i]),
                        "direct_ce": float(direct_ce[b, i]),
                        "backbone_ce": float(backbone_ce[b, i]),
                    }
                )

    wr = torch.tensor([r["write_resid"] for r in rows])
    dc = torch.tensor([r["direct_ce"] for r in rows])
    bc = torch.tensor([r["backbone_ce"] for r in rows])
    report = {
        "run_dir": run_dir.name,
        "n_chunks_scored": len(rows),
        "spearman": {
            "write_resid_vs_backbone_ce": round(_spearman(wr, bc), 4),
            "direct_ce_vs_backbone_ce": round(_spearman(dc, bc), 4),
            "write_resid_vs_direct_ce": round(_spearman(wr, dc), 4),
        },
        "resid_distribution": {
            "write_resid_p50/p90/p99": [round(float(wr.quantile(q)), 3) for q in (0.5, 0.9, 0.99)],
            "direct_ce_p50/p90/p99": [round(float(dc.quantile(q)), 3) for q in (0.5, 0.9, 0.99)],
        },
        # backbone error mass covered by the top-frac chunks under each criterion
        "error_mass_coverage": {
            crit: {
                str(f): round(float(
                    bc[crit_scores >= crit_scores.quantile(1.0 - f)].sum() / bc.sum().clamp(min=1e-12)
                ), 4)
                for f in (0.25, 0.5, 0.75)
            }
            for crit, crit_scores in (("write_resid", wr), ("direct_ce", dc))
        },
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--data-path", required=True)
    parser.add_argument("--batches", type=int, default=2)
    args = parser.parse_args()
    report = probe(Path(args.run_dir), args.data_path, args)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
