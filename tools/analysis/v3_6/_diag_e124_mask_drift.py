# E124 门②前置诊断：遮蔽器件在新体制（S0'' 锚段界器）下的分段漂移率
# 假设：attn_block_mask 经 _encode 的 encoder_blocks 扰动隐状态 → segmentor 读
# 扰动后状态 → 临界切点翻转。老基座（from-scratch 塌缩态段界器）从不翻转。
# 三问：①基线自身确定性 ②漂移率 ③漂移位置相对被遮块（上游/下游/n_real 变否）
import json
import random
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from flued.data import MASK_ID, PAD_ID  # noqa: E402
from tools.analysis.v3_6.probe_e122_necessity_book import assert_cell_keys  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    build_eval_windows,
    build_masks,
    load_model,
)
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402

CKPT = "checkpoints/v37ks_a_gate2base_v373_20k_ctx4096_20260910"
N_WINDOWS = 30
N_BLOCKS = 4
SEED = 42


def chunk_map(out):
    return out["chunks"].chunk_ids, out["chunks"].offsets, int(out["chunks"].chunk_mask[0].sum())


def main() -> None:
    device = torch.device("cuda")
    model, ns, step = load_model(Path(CKPT), device)
    assert_cell_keys(ns, model.config, strict=False)
    ns.burst_prob = 0
    ns.cloze_prob = 0
    ns.retrieval_prob = 0
    ns.data_path = r"P:\FLUED_corpus\corpus_v3\corpus_v3.txt"
    windows = build_eval_windows(ns, N_WINDOWS)
    masks = build_masks(windows, ns)
    rng = random.Random(SEED)

    det_pairs = 0
    det_bad = 0
    surg = 0
    drift = 0
    drift_nreal_changed = 0
    drift_upstream = 0
    drift_positions = []
    t0 = time.time()
    for batch, mbatch in zip(windows, masks):
        for j in range(batch.size(0)):
            ids = batch[j]
            cut = int(ids.ne(PAD_ID).sum())
            clean = ids[:cut].unsqueeze(0).to(device)
            byte_mask = mbatch[j][:cut].unsqueeze(0).to(device)
            source_a = clean.masked_fill(byte_mask.bool(), MASK_ID)

            out1 = s1.s1_forward(model, source_a, ns)
            ca1, _, nr1 = chunk_map(out1)
            out2 = s1.s1_forward(model, source_a, ns)
            ca2, _, nr2 = chunk_map(out2)
            det_pairs += 1
            if not bool((ca1 == ca2).all()) or nr1 != nr2:
                det_bad += 1

            pool = list(range(nr1 - 1))
            for c in rng.sample(pool, min(N_BLOCKS, len(pool))):
                mask_b = torch.zeros(1, 1, 1, clean.size(1), dtype=torch.bool, device=device)
                for t in range(clean.size(1)):
                    if int(ca1[0, t]) == c:
                        mask_b[0, 0, 0, t] = True
                out_b = s1.s1_forward(model, source_a, ns, attn_block_mask=mask_b)
                cb, _, nrb = chunk_map(out_b)
                surg += 1
                if not bool((cb == ca1).all()) or nrb != nr1:
                    drift += 1
                    if nrb != nr1:
                        drift_nreal_changed += 1
                    # 首个漂移字节位置对应的 chunk id（基线口径）
                    diff = (cb != ca1).nonzero()
                    first_t = int(diff[0, 1]) if diff.numel() else -1
                    first_chunk = int(ca1[0, first_t]) if first_t >= 0 else -1
                    drift_positions.append({"c": c, "first_drift_chunk": first_chunk, "nr_delta": nrb - nr1})
                    if first_chunk >= 0 and first_chunk < c:
                        drift_upstream += 1
        if det_pairs >= N_WINDOWS:
            break
    report = {
        "ckpt": CKPT, "step": step,
        "windows": det_pairs, "surgeries": surg,
        "baseline_nondeterministic": det_bad,
        "drift_count": drift, "drift_rate": round(drift / max(surg, 1), 4),
        "drift_nreal_changed": drift_nreal_changed,
        "drift_first_cut_upstream_of_masked_chunk": drift_upstream,
        "drift_cases_head": drift_positions[:10],
        "timing_sec": round(time.time() - t0, 1),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
