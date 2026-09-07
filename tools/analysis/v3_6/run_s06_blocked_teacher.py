"""S06 blocked teacher labeling driver (user-ruled 2026-08-17).

Why blocked: char-exact regeneration of a full 4096B window is beyond the
teacher (observed keep rate ~10%); ~768B blocks sit in the proven keep-rate
regime of the S05 pipeline. Blocks are line-aligned, so every block boundary
is itself a legal segment boundary under the S06 code rules; stitching block
boundaries + byte offsets reproduces full-window 4096B annotations.

Resume-safe: per-block results append to block_results.jsonl; reruns skip
completed (window, block) pairs. Failed blocks land in block_failures.jsonl
and can be retried by rerunning with --retry-failures.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "bs", str(Path(__file__).resolve().with_name("build_s0_teacher_dataset.py"))
)
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)


def split_blocks(text: str, max_bytes: int = 768) -> list[str]:
    """Line-aligned blocks; a single line longer than max_bytes is its own block."""
    lines = text.split("\n")
    blocks: list[str] = []
    cur: list[str] = []
    cur_bytes = 0
    for line in lines:
        b = len(line.encode("utf-8")) + (1 if cur else 0)  # re-joined \n
        if cur and cur_bytes + b > max_bytes:
            blocks.append("\n".join(cur))
            cur, cur_bytes = [line], len(line.encode("utf-8"))
        else:
            cur.append(line)
            cur_bytes += b
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def label_block(text: str, exemplars, endpoint: str, model: str, timeout: int, api_key: str, attempts: int):
    last = ""
    for _ in range(attempts):
        try:
            last = bs.call_teacher(endpoint, model, bs.build_prompt(exemplars, text), timeout, api_key)
        except Exception as exc:  # noqa: BLE001
            last = f"__error__ {exc}"
            if "429" in str(exc):
                # rate-limited: back off instead of burning the attempt budget
                time.sleep(30)
                continue
        boundaries = bs.validate_and_convert(text, last)
        if boundaries is not None:
            return boundaries, last
    return None, last


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples-file", required=True)
    ap.add_argument("--rules-file", required=True)
    ap.add_argument("--candidates", required=True, help="jsonl with {\"index\",\"text\"} 4096B windows (or a block_failures.jsonl with --retry-failures)")
    ap.add_argument("--retry-failures", action="store_true")
    ap.add_argument("--endpoint", default="https://api.moonshot.cn/v1")
    ap.add_argument("--api-key-file", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--attempts", type=int, default=2)
    ap.add_argument("--max-block-bytes", type=int, default=768)
    ap.add_argument("--out-dir", required=True)
    cli = ap.parse_args()

    out_dir = Path(cli.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if cli.rules_file:
        bs._QUOTE_RULES = Path(cli.rules_file).read_text(encoding="utf-8")  # noqa: SLF001
    exemplars = bs.parse_exemplars(Path(cli.samples_file), 12)
    api_key = Path(cli.api_key_file).read_text(encoding="utf-8").strip()
    print(f"[s06] exemplars={len(exemplars)} rules={len(bs._QUOTE_RULES)} chars", flush=True)  # noqa: SLF001

    block_path = out_dir / "block_results.jsonl"
    done_pairs = set()
    if block_path.exists():
        for line in block_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                done_pairs.add((r["window"], r["block"]))
        print(f"[s06] resume: {len(done_pairs)} blocks already done", flush=True)

    jobs = []  # (window_idx, block_idx, block_text, base_offset, n_blocks)
    if cli.retry_failures:
        for line in Path(cli.candidates).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            pair = (r["window"], r["block"])
            if pair not in done_pairs:
                jobs.append((r["window"], r["block"], r["text"], r["base_offset"], r["n_blocks"]))
    else:
        for line in Path(cli.candidates).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            blocks = split_blocks(r["text"], cli.max_block_bytes)
            base = 0
            for bi, btext in enumerate(blocks):
                if (r["index"], bi) not in done_pairs:
                    jobs.append((r["index"], bi, btext, base, len(blocks)))
                base += len(btext.encode("utf-8")) + 1  # +1 for the \n between blocks
        # note: split("\n")/join round-trips exactly, so base offsets are exact
    rng = random.Random(7)
    rng.shuffle(jobs)
    print(f"[s06] block jobs={len(jobs)}", flush=True)

    fail_path = out_dir / "block_failures.jsonl"
    kept = failed = 0
    t0 = time.time()
    with block_path.open("a", encoding="utf-8") as sink, fail_path.open("a", encoding="utf-8") as fsink:
        with ThreadPoolExecutor(max_workers=cli.workers) as pool:
            futs = {
                pool.submit(label_block, j[2], exemplars, cli.endpoint, cli.model, cli.timeout, api_key, cli.attempts): j
                for j in jobs
            }
            for fut in as_completed(futs):
                w, bi, btext, base, nb = futs[fut]
                boundaries, last = fut.result()
                if boundaries is None:
                    failed += 1
                    fsink.write(json.dumps({"window": w, "block": bi, "base_offset": base, "n_blocks": nb,
                                            "text": btext, "last_output": last[:400]}, ensure_ascii=False) + "\n")
                    fsink.flush()
                else:
                    kept += 1
                    sink.write(json.dumps({"window": w, "block": bi, "base_offset": base, "n_blocks": nb,
                                           "boundaries_bytes": boundaries}, ensure_ascii=False) + "\n")
                    sink.flush()
                done = kept + failed
                if done % 100 == 0:
                    print(f"[s06] {done}/{len(jobs)} kept={kept} failed={failed} {done / max(time.time() - t0, 1e-9):.1f}/s", flush=True)
    print(f"[s06] DONE kept={kept} failed={failed}", flush=True)


if __name__ == "__main__":
    main()
