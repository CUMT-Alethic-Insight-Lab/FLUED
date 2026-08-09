"""Paging-signal probe (TODO section 4, user-ruled measurement before deciding
byte-budget paging vs gated paging): measure how long the KDA state keeps an
early chunk decodable as more chunks are written -- the prefix decay curve
extended to 64/128+ chunks, per domain.

Method (deployment-faithful): the sample is encoded INCREMENTALLY -- chunk by
chunk through stream_step with a carried state. At checkpoints i, the fixed
readout query reads S_i and the decoder tries to restore probe chunk j (j<i)
from q*S_i + pos_j. acc(j|i) vs distance d=i-j is the retention curve; the
per-sample knee d* (first d where acc < threshold*max) feeds the paging-point
variance across samples and domains. Low variance -> byte-budget paging is
safe; high variance -> a gated MLP is justified.

Inputs: --run-dir (checkpoint, e.g. a long-context S36 arm) and one or more
--samples "label=path" where path is a UTF-8 text file or a JSONL with a
"context" field (P0 eval format). Each file = one domain row set.

Usage:
  python probe_paging_signal.py --data-path <corpus> --run-dir <arm> \
      --samples general=E:/projects/FLUED/eval_data/longbench/narrativeqa.jsonl \
      --max-chunks 192 --limit 3
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

from flued.v33.chunk_builder import ChunkBuilder  # noqa: E402
from tools.train.v3_6.train_v36 import build_model  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402

BYTE_OFFSET = 1  # data.py PAD-offset convention: byte b -> id b+1, PAD=0


def _load_texts(path: Path, limit: int) -> list[bytes]:
    if path.suffix == ".jsonl":
        rows = []
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                rows.append(json.loads(line)["context"].encode("utf-8"))
                if len(rows) >= limit:
                    break
        return rows
    return [path.read_bytes()[: 1 << 22]]


@torch.no_grad()
def probe(run_dir: Path, data_path: str, args) -> dict:
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
    max_chunks = args.max_chunks
    builder = ChunkBuilder(max_chunks, ns.max_span)

    reports = []
    for spec in args.samples:
        label, _, p = spec.partition("=")
        texts = _load_texts(Path(p), args.limit)
        rows = []
        for raw in texts:
            ids = torch.tensor([b + BYTE_OFFSET for b in raw], dtype=torch.long).unsqueeze(0).to(device)
            if ids.size(1) < 64:
                continue
            byte_states, confidence, valid, _ = model._encode(ids)
            hard_cut, utf8_cont, _ = model._cuts(ids, confidence, valid)
            chunks = builder(byte_states, valid, hard_cut, confidence)
            chunks = model.bridge(chunks, byte_states, confidence, valid, utf8_cont)
            memory = model.summarizer(chunks.span_embeddings, chunks.token_mask)
            gates = model.write_head(memory)
            n_real = int(chunks.chunk_mask[0].sum())
            n_use = min(n_real, max_chunks)
            if n_use < 8:
                continue
            trunc = int(chunks.pack_info["truncated_tokens"].sum())
            # incremental encoding with a carried state (deployment form)
            state = model.state_machine.init_stream_state(1, device)
            contents = []
            for i in range(n_use):
                gates_i = {
                    kk: (vv[:, i : i + 1] if isinstance(vv, torch.Tensor) and vv.dim() >= 2 and vv.size(1) == memory.size(1) else vv)
                    for kk, vv in gates.items()
                }
                package_i, state = model.state_machine.stream_step(gates_i, state)
                contents.append(package_i[:, 0].mean(dim=1))  # (d_pack,)
            n_chunks = chunks.chunk_mask.size(1)
            pos = model.chunk_pos.weight.unsqueeze(0)
            # checkpoints and probe positions (early chunks are the paging cargo)
            checks = sorted({c for c in (4, 8, 16, 24, 32, 48, 64, 96, 128, 160, n_use) if c <= n_use})
            probes = [j for j in (1, 8, 16, 32, 48) if j < n_use]
            # decode probe chunk j from the state after i writes
            for i in checks:
                content_i = contents[i - 1].unsqueeze(0)  # (1, 1, d_pack)
                cond_base = model.decoder_in(content_i)
                for j in probes:
                    if j > i:
                        continue
                    mask_j = chunks.token_mask[:, j : j + 1]
                    if not mask_j.any():
                        continue
                    cond = cond_base + pos[:, j : j + 1]
                    logits = model.decoder(cond, mask_j)
                    # chunk j's byte targets straight from the chunked mapping:
                    # positions whose chunk_ids == j, in slot order (consecutive)
                    pos_in_chunk = (chunks.chunk_ids[0] == j).nonzero(as_tuple=True)[0]
                    tgt = ids[0, pos_in_chunk]
                    pred = logits[0, 0].argmax(dim=-1)[: tgt.size(0)]
                    valid_j = tgt.ne(0)
                    acc = float(pred[valid_j].eq(tgt[valid_j]).float().mean()) if valid_j.any() else 0.0
                    rows.append({"i": i, "j": j, "dist": i - j, "acc": round(acc, 4)})
            rows.append({"state_norm_final": float(state.norm(dim=(-2, -1)).mean()), "truncated_tokens": trunc})
        reports.append({"label": label, "rows": rows})

    # aggregate: acc by distance per domain + knee d* per sample
    out = {"run_dir": run_dir.name, "domains": {}}
    for rep in reports:
        by_d: dict[int, list[float]] = {}
        for r in rep["rows"]:
            if "acc" in r:
                by_d.setdefault(r["dist"], []).append(r["acc"])
        curve = {str(d): round(sum(v) / len(v), 4) for d, v in sorted(by_d.items())}
        out["domains"][rep["label"]] = {"curve": curve}
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--data-path", required=True)
    parser.add_argument("--samples", nargs="+", required=True, help="label=path entries")
    parser.add_argument("--max-chunks", type=int, default=192)
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()
    report = probe(Path(args.run_dir), args.data_path, args)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
