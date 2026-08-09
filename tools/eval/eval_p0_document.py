"""P0 document-level evaluation harness (built 2026-08-08, put to use 2026-08-09).

Translates the internal S1.0 metrics onto externally legible document suites
(E:/projects/FLUED/eval_data). Two measurements per checkpoint:

1. document codec: direct/backbone byte accuracy + PPL on the first window
   (seq_len from the run's own resolved_config) of each context, standard
   40/60 mixed mask -- same protocol as training eval, new document sources;
2. needle-span completion (RULER niah + any sample whose answers appear
   verbatim in context): crop a window around the answer, mask exactly the
   answer's bytes, measure backbone accuracy on those positions only -- the
   external form of "retrieval from the compressed representation".

Usage:
  python tools/eval/eval_p0_document.py --run-dir <arm> [--suites longbench/2wikimqa.jsonl ...]
      [--needle-suites ruler/niah_single_1.jsonl] [--limit 32]
"""

from __future__ import annotations

import argparse
import json
import sys
from argparse import Namespace
from pathlib import Path

import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.train.v3_6.train_v36 import build_model  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402

EVAL_DATA = Path("E:/projects/FLUED/eval_data")


def _ids_from_text(text: str, seq_len: int, offset: int = 0) -> torch.Tensor:
    raw = text.encode("utf-8")[offset : offset + seq_len]
    return torch.tensor([b + 1 for b in raw], dtype=torch.long).unsqueeze(0)


def _forward_acc(model, ns, ids, byte_mask, device, score_mask=None):
    """One-window forward -> (direct_acc, backbone_acc, backbone_acc_on_score).

    byte_mask: positions masked OUT of the encoder input. score_mask: slot
    positions the backbone is scored on (defaults to the masked slots -- the
    completion protocol). For needle retrieval, byte_mask=zeros (needle stays
    visible) and score_mask=needle span (readback of encoded content)."""
    source = ids.masked_fill(byte_mask, s1.MASK_ID)
    with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device.type == "cuda"):
        out = s1.s1_forward(model, source, ns, clean=ids, byte_mask=byte_mask)
    chunks = out["chunks"]
    targets, slot_mask, masked_slot = s1.make_targets(
        ids, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    enc_targets, enc_slot_mask, _ = s1.make_targets(
        source, torch.zeros_like(byte_mask), chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    d_acc = s1._acc_tensor(out["logits_direct"].argmax(-1), enc_targets, enc_slot_mask)
    b_acc = s1._acc_tensor(out["logits_backbone"].argmax(-1), targets, slot_mask)
    if score_mask is not None:
        _, _, score_slot = s1.make_targets(
            ids, score_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
        )
        masked_slot = score_slot
    b_masked = s1._acc_tensor(out["logits_backbone"].argmax(-1), targets, masked_slot)
    return float(d_acc), float(b_acc), float(b_masked), out


@torch.no_grad()
def eval_run(run_dir: Path, args, device) -> dict:
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_path"] = "unused"  # dataloaders not needed; windows come from files
    cfg["data_manifest"] = ""
    ns = Namespace(**cfg)
    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed":
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    model = build_model(ns).to(device)
    payload = torch.load(run_dir / "latest.pt", map_location=device, weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    model.eval()
    torch.manual_seed(ns.eval_mask_seed)
    s1._MASK_GENERATOR.manual_seed(ns.eval_mask_seed)
    seq_len = ns.seq_len

    report = {"run_dir": run_dir.name, "codec": {}, "needle": {}}

    for suite in args.suites:
        path = EVAL_DATA / suite
        rows = []
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                rows.append(json.loads(line))
                if len(rows) >= args.limit:
                    break
        d_accs, b_accs = [], []
        for row in rows:
            text = row["context"]
            if len(text.encode("utf-8")) < 256:
                continue
            ids = _ids_from_text(text, seq_len).to(device)
            valid = ids.ne(0)
            byte_mask = s1.make_mixed_mask(
                ids.cpu(), ns.mask_prob, char_frac=ns.mask_char_frac,
                char_span_max=ns.mask_char_span_max, tokenizer=s1._BPE_TOKENIZER,
                generator=s1._MASK_GENERATOR,
            ).to(device)
            d, b, _, _ = _forward_acc(model, ns, ids, byte_mask, device)
            d_accs.append(d)
            b_accs.append(b)
        if d_accs:
            report["codec"][suite] = {
                "n": len(d_accs),
                "direct_acc": round(sum(d_accs) / len(d_accs), 4),
                "backbone_acc": round(sum(b_accs) / len(b_accs), 4),
            }

    for suite in args.needle_suites:
        path = EVAL_DATA / suite
        rows = []
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                rows.append(json.loads(line))
                if len(rows) >= args.limit:
                    break
        hits, accs = [], []
        for row in rows:
            ctx_bytes = row["context"].encode("utf-8")
            ans = (row.get("answers") or [""])[0]
            if not ans:
                continue
            pos = ctx_bytes.find(ans.encode("utf-8"))
            if pos < 0:
                continue
            # window ending just after the answer (needle near the end = the
            # hardest case for the carried state)
            end = min(len(ctx_bytes), pos + len(ans) + 8)
            start = max(0, end - seq_len)
            ids = _ids_from_text(row["context"], seq_len, offset=start).to(device)
            mask = torch.zeros_like(ids, dtype=torch.bool)
            a0, a1 = pos - start, pos - start + len(ans.encode("utf-8"))
            if a0 < 0 or a1 > ids.size(1):
                continue
            mask[0, a0:a1] = True
            # retrieval protocol (fixed 2026-08-09): the needle stays VISIBLE
            # in the input -- masking it would measure inference of
            # never-encoded bytes (E23: that is not retrieval). We score
            # readback accuracy on the needle positions only.
            zero_mask = torch.zeros_like(ids, dtype=torch.bool)
            _, _, b_masked, _ = _forward_acc(model, ns, ids, zero_mask, device, score_mask=mask)
            hits.append(1)
            accs.append(b_masked)
        if accs:
            report["needle"][suite] = {
                "n": len(accs),
                "needle_acc": round(sum(accs) / len(accs), 4),
            }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--suites", nargs="+", default=["longbench/2wikimqa.jsonl", "longbench/narrativeqa.jsonl"])
    parser.add_argument("--needle-suites", nargs="+", default=["ruler/niah_single_1.jsonl", "ruler/niah_multikey_1.jsonl"])
    parser.add_argument("--limit", type=int, default=32)
    args = parser.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    report = eval_run(Path(args.run_dir), args, device)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
