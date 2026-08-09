"""Segmentor behavior audit at long inputs (user-requested 2026-08-10, after
E51's cut_capacity_overflow=1.125 flag at 4096B).

The frontend (byte embedder + segmentor) is frozen S0'' across all S1 arms,
so this audit is arm-independent. Encodes long samples through _encode/_cuts
and reports: chunk-count distribution, chunk byte-length distribution, how
many samples exceed a given max_chunks cap, boundary confidence stats, and a
couple of printed segmentations with cut marks.

Usage:
  python tools/analysis/v3_6/audit_segmentor_longctx.py --run-dir checkpoints/s36f_ctx2048_20k_20260808 \
      --data-path <corpus> [--lengths 2048 4096] [--samples 64] [--show 2]
"""

from __future__ import annotations

import argparse
import json
import sys
from argparse import Namespace
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.train.v3_6.train_v36 import build_model  # noqa: E402


@torch.no_grad()
def audit(run_dir: Path, data_path: str, args) -> dict:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_path"] = data_path
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"
    ns = Namespace(**cfg)
    model = build_model(ns).to(device)
    payload = torch.load(run_dir / "latest.pt", map_location=device, weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    model.eval()

    raw = Path(data_path).read_bytes()
    report = {"run_dir": run_dir.name, "lengths": {}}
    for L in args.lengths:
        counts, lens, confs = [], [], []
        over = 0
        shown = 0
        examples = []
        for si in range(args.samples):
            start = (si * 7919) % max(1, len(raw) - L - 1)
            ids = torch.tensor([b + 1 for b in raw[start : start + L]], dtype=torch.long).unsqueeze(0).to(device)
            byte_states, confidence, valid, _ = model._encode(ids)
            hard_cut, utf8_cont, _ = model._cuts(ids, confidence, valid)
            n = int(hard_cut[0].sum())
            if n < 2:
                continue
            cut_pos = hard_cut[0].nonzero(as_tuple=True)[0].tolist()
            chunk_lens = [b - a for a, b in zip([0] + cut_pos, cut_pos + [int(valid[0].sum())])]
            counts.append(n)
            lens.extend(chunk_lens)
            confs.append(float(confidence[0][valid[0]].float().mean()))
            if n > args.cap:
                over += 1
            if shown < args.show:
                text = raw[start : start + L].decode("utf-8", errors="replace")
                marks = "".join(
                    ("|" if (i in set(cut_pos)) else "") + ch
                    for i, ch in enumerate(text[: 40 * 22])
                )
                examples.append(marks[:900])
                shown += 1
        counts_t = torch.tensor(counts, dtype=torch.float32)
        lens_t = torch.tensor(lens, dtype=torch.float32)
        report["lengths"][str(L)] = {
            "samples": len(counts),
            "chunks_per_sample": {
                "mean": round(float(counts_t.mean()), 2),
                "p50": round(float(counts_t.quantile(0.5)), 1),
                "p90": round(float(counts_t.quantile(0.9)), 1),
                "p99": round(float(counts_t.quantile(0.99)), 1),
                "max": int(counts_t.max()),
            },
            "over_cap": {"cap": args.cap, "count": over, "frac": round(over / max(len(counts), 1), 4)},
            "chunk_bytes": {
                "min": int(lens_t.min()),
                "p10": round(float(lens_t.quantile(0.1)), 1),
                "p50": round(float(lens_t.quantile(0.5)), 1),
                "p90": round(float(lens_t.quantile(0.9)), 1),
                "max": int(lens_t.max()),
                "mean": round(float(lens_t.mean()), 2),
            },
            "boundary_conf_mean": round(sum(confs) / max(len(confs), 1), 4),
            "examples": examples,
        }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--data-path", required=True)
    parser.add_argument("--lengths", type=int, nargs="+", default=[2048, 4096])
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--cap", type=int, default=320)
    parser.add_argument("--show", type=int, default=2)
    args = parser.parse_args()
    report = audit(Path(args.run_dir), args.data_path, args)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
