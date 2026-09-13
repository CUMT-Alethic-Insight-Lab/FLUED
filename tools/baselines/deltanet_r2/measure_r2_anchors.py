"""R2 臂门②锚直测（坑 9：换臂换体制必换锚——分母锚全部在本臂体制直测）。

在 DeltaNet-50M 本体训练体制（corpus_v3 顺序字节窗 4096B + Mistral 32K BPE +
BOS + 截 2048）下直测：
- tokens/窗 与 监督 token/窗（= L−1；BOS 位无预测）分布；
- 原生分块语义锚：fla chunk 模式原生粒度 64 token
  （fla/ops/delta_rule/wy_fast.py:226  BT = 64，WY 表示硬编码；
  fla/layers/delta_net.py:261 chunk_delta_rule 调用点）→ chunks/窗 = ceil(L/64)；
- 盲猜地板：unigram（token 边缘分布）熵，nats/token，于语料前缀直测；
  另报均匀地板 ln(V)；
- 一切我们体制在册数（166/172.7、24B/块、54.8 B/窗等）不引、不借、不作分母。

Usage:
  python tools/baselines/deltanet_r2/measure_r2_anchors.py \
      --corpus /workspace/corpus/corpus_v3.txt \
      --tokenizer-path /workspace/models/delta_net-1.3B-100B \
      --n-windows 512 --floor-windows 4096 \
      --out-dir outputs/r2_deltanet50m_20260913/anchors
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import tools.baselines.deltanet_r2.r2_spec as spec


def pct(sorted_vals: list[int], q: float) -> int:
    if not sorted_vals:
        return 0
    i = min(len(sorted_vals) - 1, max(0, int(q * (len(sorted_vals) - 1))))
    return sorted_vals[i]


def dist_stats(vals: list[int]) -> dict:
    s = sorted(vals)
    n = len(s)
    return {"n": n, "mean": (sum(s) / n) if n else None,
            "min": s[0] if s else None, "p05": pct(s, 0.05), "p50": pct(s, 0.50),
            "p95": pct(s, 0.95), "max": s[-1] if s else None}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--corpus", required=True)
    p.add_argument("--tokenizer-path", required=True)
    p.add_argument("--n-windows", type=int, default=512,
                   help="tokens/窗 与 chunks/窗 分布的测量窗数")
    p.add_argument("--floor-windows", type=int, default=4096,
                   help="盲猜地板（unigram 熵）的计数前缀窗数")
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()
    if args.n_windows > args.floor_windows:
        raise SystemExit("--n-windows 须 ≤ --floor-windows（分布样本 ⊆ 地板前缀）")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.tokenizer_path, trust_remote_code=True)

    counts: Counter[int] = Counter()
    n_tok_win: list[int] = []
    n_sup_win: list[int] = []
    n_chunk_win: list[int] = []
    n_truncated = 0
    measured = 0

    for w, raw in spec.iter_byte_windows(args.corpus, spec.WINDOW_BYTES):
        if measured >= args.floor_windows:
            break
        full_ids = list(tok(spec.window_text(raw))["input_ids"])
        ids = full_ids[:spec.MAX_TOKENS]
        if len(full_ids) > spec.MAX_TOKENS:
            n_truncated += 1
        if measured < args.n_windows:
            n_tok_win.append(len(ids))
            n_sup_win.append(max(0, len(ids) - 1))   # BOS 位无预测
            n_chunk_win.append(math.ceil(len(ids) / spec.NATIVE_CHUNK_TOKENS))
        counts.update(ids)
        measured += 1
        if measured % 512 == 0:
            print(f"[r2-anchor] {measured}/{args.floor_windows} 窗 "
                  f"({time.time()-t0:.0f}s)", flush=True)

    # 盲猜地板：unigram 熵（nats/token）
    total = sum(counts.values())
    h = sum(-(c / total) * math.log(c / total) for c in counts.values())
    summary = {
        "probe": "R2 门②锚直测（坑 9：分母锚全部本体制直测）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "corpus": str(args.corpus),
        "window_definition": {
            "window": f"corpus[w*{spec.WINDOW_BYTES} : (w+1)*{spec.WINDOW_BYTES}] 顺序字节窗",
            "decode": "utf-8 errors=replace",
            "tokenize": "tokenizer 默认 special tokens（Mistral 系加 BOS）",
            "truncation": f"ids[:{spec.MAX_TOKENS}]",
            "supervised_tokens": "L−1（BOS 位无预测；无 padding，逐位计 CE）",
            "native_chunk": {
                "tokens_per_chunk": spec.NATIVE_CHUNK_TOKENS,
                "evidence": "fla/ops/delta_rule/wy_fast.py:226  BT = 64（fla 0.5.1，WY 表示硬编码）；"
                            "fla/layers/delta_net.py:261 chunk 模式调用 chunk_delta_rule",
                "chunks_per_window": "ceil(L/64)",
            },
        },
        "params": {"n_windows_dist": args.n_windows,
                   "floor_windows": args.floor_windows,
                   "tokenizer_path": args.tokenizer_path},
        "tokens_per_window": dist_stats(n_tok_win),
        "supervised_tokens_per_window": dist_stats(n_sup_win),
        "native_chunks_per_window": dist_stats(n_chunk_win),
        "n_windows_truncated": n_truncated,
        "blind_floor": {
            "unigram_entropy_nats_per_token": h,
            "unigram_ppl": math.exp(h),
            "uniform_floor_lnV_nats": math.log(spec.R2_CONFIG["vocab_size"]),
            "vocab_used": len(counts),
            "tokens_counted": total,
        },
        "tokens_per_byte": (sum(n_tok_win) / (args.n_windows * spec.WINDOW_BYTES)) if args.n_windows else None,
        "no_borrow_note": "166/172.7、24B/块、54.8 B/窗等我们体制在册数未引用、未借用、未作分母",
        "env": {"torch": __import__("torch").__version__,
                "gpu": __import__("torch").cuda.get_device_name(0)
                if __import__("torch").cuda.is_available() else "cpu",
                "tokenizer_path": args.tokenizer_path},
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
