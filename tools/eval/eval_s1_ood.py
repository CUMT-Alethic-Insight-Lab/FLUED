"""OOD re-eval of a run's final checkpoint on a different corpus (v4/v5):
translates internal evidence into externally checkable form -- same S1.0
metrics, new data path. Only latest.pt (final), not milestones.

Usage:
  python tools/eval/eval_s1_ood.py --data-path <new_corpus.txt> run_dir [run_dir ...]
"""

from __future__ import annotations

import argparse
import json
import sys
from argparse import Namespace
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.train.v3_3.train_v33 import make_dataloaders  # noqa: E402
from tools.train.v3_6.train_v36 import build_model  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402


def eval_ood(run_dir: Path, data_path: str, device: torch.device) -> dict:
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_path"] = data_path
    cfg["data_manifest"] = ""
    ns = Namespace(**cfg)
    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed":
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    model = build_model(ns).to(device)
    payload = torch.load(run_dir / "latest.pt", map_location=device, weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    _, eval_loader = make_dataloaders(ns)
    metrics = s1.evaluate(model, eval_loader, ns, device)
    keep = (
        "eval_direct_acc", "eval_backbone_acc", "eval_backbone_unmasked_acc",
        "eval_backbone_masked_acc", "eval_predict_cos", "eval_state_norm",
        "eval_direct_ppl", "eval_backbone_ppl", "eval_chunks_per_sample",
        "eval_cut_capacity_overflow", "eval_truncated_tokens",
    )
    row = {"run_dir": run_dir.name, "ood_data": data_path, "step": int(payload.get("step", 0))}
    row.update({k: round(float(metrics[k]), 6) for k in keep if k in metrics})
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dirs", nargs="+")
    parser.add_argument("--data-path", required=True)
    args = parser.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    for rd in args.run_dirs:
        row = eval_ood(Path(rd), args.data_path, device)
        print(json.dumps(row, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
