"""Draft-backbone vitality probes (research sweep 2026-08-08, arm A4).

Three diagnostics for the three-state drafting backbone (spec SS23), runnable
on any --backbone-mode draft checkpoint:

1. r-scan: force n_steps in a grid (default 1,2,4,8,16) and measure completion
   accuracy per T. HRM-autopsy criterion (arXiv:2510.00355): if T=1 already
   saturates, the loop has degenerated into a consistency model.
2. Perturbation sensitivity (Soft-Thinking probe, arXiv:2508.03440): inject
   gaussian noise into the thinking matrix at a middle round; if the final
   output barely moves, the loop is dead regardless of what think_steps says.
3. Per-round trajectory: ||h_t||, cos(h_t, h_{t-1}), effective rank over real
   slots -- the collapse signature in numbers (readout-blind-spot style,
   arXiv:2606.24898).

Usage:
  python probe_draft_vitality.py --data-path <corpus> --run-dir <run_dir>
      [--batches 2] [--r-scan 1 2 4 8 16] [--noise-scale 1.0]
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


def _erank(h: torch.Tensor, mask: torch.Tensor) -> float:
    """Effective rank of the thinking matrix over real slots."""
    x = h.float()[mask]  # (N, d)
    if x.size(0) < 2:
        return 1.0
    s = torch.linalg.svdvals(x)
    p = (s / s.sum().clamp(min=1e-12)).clamp(min=1e-12)
    return float(torch.exp(-(p * p.log()).sum()))


def _acc(logits: torch.Tensor, targets: torch.Tensor, slot_mask: torch.Tensor) -> float:
    m = slot_mask.bool()
    if not m.any():
        return 0.0
    return float(logits.argmax(dim=-1)[m].eq(targets[m]).float().mean())


@torch.no_grad()
def probe_run(run_dir: Path, data_path: str, args) -> dict:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_path"] = data_path
    cfg["data_manifest"] = ""
    if getattr(args, "kda_impl", ""):
        cfg["kda_impl"] = args.kda_impl  # CPU smoke runs need the torch fallback
    ns = Namespace(**cfg)
    if getattr(ns, "backbone_mode", "") != "draft":
        return {"run_dir": str(run_dir), "error": "not a draft run"}
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

    r_scan_rows = []
    perturb_rows = []
    traj_rows = []
    for bi, batch in enumerate(eval_loader):
        if bi >= args.batches:
            break
        clean = batch[0].to(device)
        if getattr(ns, "mask_mode", "byte_span") == "mixed":
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
            last = chunks.chunk_mask.long().sum(dim=1).clamp(min=1) - 1
            ar = torch.arange(content.size(0), device=device)
            readout = content[ar, last]

            targets, slot_mask, _ = make_targets(
                clean, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
            )

            def complete(h):
                logits = model.decoder(h + pos, chunks.token_mask)
                return _acc(logits.float(), targets, slot_mask), logits

            # 1. r-scan
            for t in args.r_scan:
                torch.manual_seed(1000 + bi)  # identical draft noise across T
                out_t, _ = model.backbone.think(
                    readout, memory, chunks.chunk_mask, pos, n_steps=t, content=content
                )
                acc_t, _ = complete(out_t)
                r_scan_rows.append({"batch": bi, "T": t, "acc": acc_t})

            # 2. perturbation at the middle round
            t0 = max(args.r_scan)
            torch.manual_seed(2000 + bi)
            h0, _ = model.backbone.think(
                readout, memory, chunks.chunk_mask, pos, n_steps=t0, content=content
            )
            acc0, logits0 = complete(h0)

            def hook(h, t):
                if t == t0 // 2:
                    g = torch.Generator(device="cpu").manual_seed(3000 + bi)
                    noise = torch.randn(h.shape, generator=g).to(h.device, h.dtype)
                    h = h + args.noise_scale * h.float().std().to(h.dtype) * noise
                return h

            torch.manual_seed(2000 + bi)
            h1, _ = model.backbone.think(
                readout, memory, chunks.chunk_mask, pos, n_steps=t0, content=content,
                round_hook=hook,
            )
            acc1, _ = complete(h1)
            m = chunks.chunk_mask
            cos = float(F.cosine_similarity(h0.float()[m], h1.float()[m], dim=-1).mean())
            perturb_rows.append(
                {"batch": bi, "T": t0, "acc_base": acc0, "acc_perturbed": acc1,
                 "delta_acc": acc0 - acc1, "cos_out": cos}
            )

            # 3. per-round trajectory (stats-only hook)
            traj = []

            def rec(h, t):
                if t == 0:
                    traj.append({"t": t, "norm": float(h.float()[m].norm(dim=-1).mean()),
                                 "cos_prev": None, "erank": _erank(h, m)})
                else:
                    prev = traj[-1]["_h"]
                    cos_t = float(F.cosine_similarity(h.float()[m], prev[m], dim=-1).mean())
                    traj.append({"t": t, "norm": float(h.float()[m].norm(dim=-1).mean()),
                                 "cos_prev": cos_t, "erank": _erank(h, m)})
                traj[-1]["_h"] = h.float().detach()
                return h

            torch.manual_seed(3000 + bi)
            model.backbone.think(
                readout, memory, chunks.chunk_mask, pos, n_steps=t0, content=content,
                round_hook=rec,
            )
            for row in traj:
                row.pop("_h")
                row["batch"] = bi
                traj_rows.append(row)

    def avg(rows, key, sel=None):
        vals = [r[key] for r in rows if sel is None or sel(r)]
        return sum(vals) / max(len(vals), 1)

    report = {
        "run_dir": run_dir.name,
        "step": int(payload.get("step", 0)),
        "r_scan": [
            {"T": t, "acc": round(avg(r_scan_rows, "acc", lambda r, t=t: r["T"] == t), 4)}
            for t in args.r_scan
        ],
        "perturbation": {
            "T": max(args.r_scan),
            "delta_acc": round(avg(perturb_rows, "delta_acc"), 4),
            "cos_out": round(avg(perturb_rows, "cos_out"), 4),
        },
        "trajectory": [
            {"t": t,
             "norm": round(avg(traj_rows, "norm", lambda r, t=t: r["t"] == t), 4),
             "cos_prev": (round(avg(traj_rows, "cos_prev", lambda r, t=t: r["t"] == t and r["cos_prev"] is not None), 4) if t > 0 else None),
             "erank": round(avg(traj_rows, "erank", lambda r, t=t: r["t"] == t), 3)}
            for t in range(max(args.r_scan))
        ],
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--data-path", required=True)
    parser.add_argument("--batches", type=int, default=2)
    parser.add_argument("--r-scan", type=int, nargs="+", default=[1, 2, 4, 8, 16])
    parser.add_argument("--noise-scale", type=float, default=1.0)
    parser.add_argument("--kda-impl", default="", help="override kda_impl (e.g. torch for CPU smoke)")
    args = parser.parse_args()
    report = probe_run(Path(args.run_dir), args.data_path, args)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
