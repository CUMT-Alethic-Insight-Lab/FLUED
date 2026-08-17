# FLUED: Fluid Language Unified Encoder-Decoder

> **当前状态唯一事实源：[`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)**（默认配置、
> 证据注册表、闸门与待裁定队列；凡与历史文档冲突以该文为准）。

**FLUED** is an Alethic Insight research project on tokenizer-free language interfaces.

The project studies whether a raw byte stream can be translated into a compact,
decoder-compatible latent representation before it reaches a language-model
backbone.  The goal is not simply to replace BPE with another tokenizer.  The
central question is:

```text
Can a learnable byte-to-latent interface reduce the backbone's alignment burden
while preserving reversible byte-level input/output behavior?
```

FLUED is currently published as a research archive and architecture record.  It
contains code, experiments, failed directions, corrected evaluation protocols,
and the versioned implementation and ablation archive.  The current mainline is
v3.6 (KDA generation: whole-prompt compression to a single readout package);
see `docs/CURRENT_STATE.md` for the live evidence registry.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/pytorch-cu128-red.svg)](https://pytorch.org/)

## Current Public Position

FLUED should be read as a research exploration, not as a claim of state-of-the-art
language-model performance.

Current defensible claims:

1. FLUED v1 showed a historical positive signal: E1v5 learned non-uniform
   differentiable byte boundaries, and an older E3 run reported FLUED `1.2114`
   BPB versus BPE `1.4786` BPB.
2. FLUED v2 learns stable differentiable byte-boundary behavior under denoising
   reconstruction.
3. A fair 2048-original-byte downstream comparison shows FLUED v2 is stable, but
   still behind the BPE baselines on bits-per-byte.
4. v3.2.1 strict masked-source training is the first FLUED v3-family result that
   clearly makes a small latent backbone outperform a byte baseline.
5. v3.4 (historical wrap-up line, see `docs/versions/v3.4/`) implemented
   parallel per-chunk memory, marginal coding-rate boundary selection, plain
   byte lookup (structured lookup lost the corrected 20K same-budget
   comparison), and hard readout emission with real backbone compaction.
6. In a corrected 38M / 20K single-seed probe, normalized historical
   other-chunk memory reached `96.89%` reconstruction and `35.76` masked-byte
   completion perplexity at `0.58` actual latent/byte. This is a historical
   v3.4 result; the memory line was later closed (E7/E13, no measurable gain
   across 512–4096B).
7. CBIU (historical v3.4 emit-utility line) showed a learnable but weak
   emit-action value signal: the MLP-64 controller reached `AUC=0.584`,
   `Spearman=0.240`, `ECE=0.149` with about 40% fewer actual latents than the
   legacy target. It did not pass the boundary-takeover admission bar.
   The shared approximate-inverse decoder remains the largest blocker: at a
   matched `0.20` latent/byte budget it reached `21.00%` reconstruction /
   `43.37` PPL versus `40.92%` / `30.83` for an independent decoder.

Non-claims:

1. FLUED does not currently beat BPE as a production tokenizer replacement.
2. FLUED does not currently beat BLT, H-Net, ByteFlow, Bolmo, or other recent
   tokenizer-free systems.
3. The current-memory/self-memory branch is closed. Historical v3.4 read only
   normalized summaries of other chunks; the memory line was later closed
   (E7/E13).
4. The historical v1 BPB signal should not be treated as reproduced under the
   current fair 2048-original-byte / 100K downstream protocol.

## Research Timeline

| Stage | Main idea | What we learned |
| --- | --- | --- |
| v0.4 / v1 | Soft boundary autoencoder over raw bytes | Minimum hypothesis succeeded: E1v5 reached recon_acc 0.9999, m/n 0.379, bp_std 0.443, and a historical E3 run showed 1.2114 BPB vs BPE 1.4786; reconstruction alone was still not enough. |
| v2 | 328M denoising reconstruction with tied inverse decoder and type-aware boundary priors | Stable E1 reconstruction and three-seed consistency, but compression control and downstream BPB remained weak. |
| v3 / v3.1 | Small language-codec prototypes with readout latent, summary memory, and minimal backbone tests | Memory appeared useful in early clean-codec tests, but the evidence was not leakage-safe enough. |
| v3.2 | Factorized byte seed, memory-free boundary, memory-conditioned interpreter, causal memory branch | The architecture boundary became clearer, but memory did not show universal gain. |
| v3.2.1 | Strict masked-source codec and paired backbone evaluation | Masked-source training produced the strongest validated latent-interface result. |
| v3.3 | Byte-to-latent decision interface | Current architecture target for public documentation and future implementation. |
| v3.4 | Parallel memory, marginal coding rate, position/AR probes, hard emit control | Corrected 20K tests favor normalized no-self historical memory; current-memory helps early but plateaus lower. 2026-07-16 attribution matrices: hard emit collapses capacity before the boundary switch; memory usage weight 0.05 is the first rate-distortion improvement. 2026-07-17 CBIU three rounds: learnable emit-action utility, not yet calibrated enough for boundary takeover. |
| v3.5 | Staged freeze L0-L5 and offline counterfactual utility datasets (v3.4 wrap-up series) | Independent-decoder codec saturates (recon 0.993, two seeds); quantile budget annealing is the first smooth compression mechanism; class-level additive factor model (27 params) is the best L3 form but misses the AUC admission bar; 14-arm long-context memory ablation shows zero gain at 512-4096B. |
| v3.6 | KDA generation (S36): encoder produces a single gist readout per 512-byte page; cross-attention backbone queries segment states with strict causality and a residual-gated verbatim cache | Mainline S36: per-segment query + k=1 gist readout + residual-gated exact cache (criterion = direct decoding CE). Strongest single-seed engineering numbers: s36g2 (4096B, batch 4) backbone **0.8134** (highest to date); s36a (512B) backbone **0.7981**; P0 RULER needle retrieval **0.848**; v4 out-of-domain three-arm replication consistent. The 0.206 plateau root cause is a fixed single-query addressing wall (E50); storage is redundant at 512B/2048B and becomes valuable at 4096B (+1.78pp, E55). Baseline anchors: H-Net reproduction **0.653** BPB, KDA-LM **1.80**, GDN-2 **1.828**. Current default: `configs/canonical_v36.json`; trainer entrypoint `tools/train/v3_6/train_v36_s1.py`. In progress: S39 archive content-addressed remote query interface (spec §26). |

See [docs/research/FLUED_RESEARCH_RETROSPECTIVE_CN.md](docs/research/FLUED_RESEARCH_RETROSPECTIVE_CN.md)
for the full v1-v3.3 narrative; v3.4 evidence is indexed separately below.

## Key Results

### Historical v1 Signals

v1 should be read as a minimum-hypothesis result: differentiable byte boundaries
can be learned and decoded back to bytes, but this did not prove semantic
tokenization or production replacement for BPE.

| Result | Value | Interpretation |
| --- | ---: | --- |
| E1v5 reconstruction accuracy | 0.9999 | Near-lossless codec behavior |
| E1v5 m/n | 0.379 | About 2.64x compression |
| E1v5 bp_std | 0.443 | Non-collapsed boundary distribution |
| Historical E3 FLUED BPB | 1.2114 | Older downstream positive signal |
| Historical E3 BPE BPB | 1.4786 | Historical comparison baseline |

This is a historical result, not the current fair downstream conclusion.

### v2 Reconstruction Stability

All v2 A-class runs used `latent_consistency_weight=0`, mixed clean/denoising
reconstruction, fixed 512-byte chunks, and a 328M tied Transformer autoencoder.

| Seed | Eval Acc | m/n | bp_std | CJK bp |
| --- | ---: | ---: | ---: | ---: |
| 42 | 0.9991 | 0.470 | 0.407 | 0.122 |
| 123 | 0.9993 | 0.498 | 0.391 | 0.182 |
| 999 | 0.9996 | 0.491 | 0.394 | 0.092 |
| Mean | 0.9993 +/- 0.0005 | 0.486 +/- 0.028 | 0.397 +/- 0.016 | 0.132 +/- 0.090 |

Important correction: a latent-consistency mean-squared-error objective was
tested and rejected.  It caused loss spikes, boundary collapse, and catastrophic
forgetting.

### Fair Downstream D1 Comparison

The fair downstream comparison controls the original-byte context budget
(`2048` original bytes) and training steps (`100K`).  Lower BPB is better.

| Method | Context Budget | Steps | BPB | KV / 1KB | Interpretation |
| --- | --- | ---: | ---: | ---: | --- |
| BPE-8K | 2048 original bytes | 100K | **0.8066** | 164.0 | Current strongest baseline |
| BPE-16K | 2048 original bytes | 100K | 0.8165 | 149.1 | Fair byte-denominator fix applied |
| BPE-32K | 2048 original bytes | 100K | 0.8205 | 135.6 | Fair byte-denominator fix applied |
| FLUED v2 | 2048 original bytes | 100K | 0.8732 | 546.1 | Stable, but behind BPE |
| BLT theta=0.3 | 2048 original bytes | 100K | 2.3996 | 554.9 | Reproduction is weak; not a BLT claim |

The older fixed-token BPE runs are not valid for fair comparison because
`--max-seq-len 2048` meant 2048 BPE tokens, not 2048 original bytes.

### v3.2.1 Strict Masked-Source Backbone

This is the most important v3-family validation.  Masking happens on the byte
input before FLUED sees the sequence; the small backbone only sees FLUED readout
latents.

| Run | family | memory | mask_acc | delta_acc vs byte | byte_CE | delta_CE vs byte |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| v3.2.1 no-memory masked 15k | v32 | false | **0.1898** | **+0.0458** | **3.1424** | **+0.2358** |
| v3.2.1 memory masked 15k | v32 | true | 0.1897 | +0.0457 | 3.1473 | +0.2308 |
| v3.1 codec10k pool-MFL | v31 | false | 0.1468 | +0.0028 | 3.4551 | -0.0770 |
| v3.2 stage3 memory 10k | v32 | true | 0.1458 | +0.0018 | 3.4666 | -0.0885 |
| byte baseline | byte | false | 0.1440 | 0.0000 | 3.3782 | 0.0000 |

Interpretation:

```text
v3.2.1 masked-source codec is the first route that clearly reduces the small
backbone's masked-byte completion difficulty.
```

## FLUED v3.4 Architecture

v3.4 kept FLUED as a reversible byte-to-latent interface while moving memory
construction off the serial critical path. It introduced parallel per-chunk
memory summaries, marginal coding-rate boundary selection, plain byte lookup,
and hard readout emission with real backbone compaction. The corrected 20K probe
and the 5K structural screen established historical validation points for the
v3-family interface, but they are not the current mainline. Details, raw logs,
and the document reading order remain in the version-frozen v3.4 index.

See the [v3.4 documentation index](docs/versions/v3.4/README.md) for CBIU
results, attribution matrices, the corrected 20K memory comparison, and the 5K
structural screen. Documents dated before 2026-07-14 describe pre-correction
implementations and must be read together with the self-audit and correction
reports.

## Public Documentation Map

| Document | Purpose |
| --- | --- |
| [Documentation index](docs/README.md) | Versioned map and evidence status |
| [Research retrospective](docs/research/FLUED_RESEARCH_RETROSPECTIVE_CN.md) | v1-v3.3 reasoning, failures, and iteration process |
| [v3.4 doc index](docs/versions/v3.4/README.md) | Current v3.4 reading order and evidence status |
| [CBIU three-round results](docs/versions/v3.4/FLUED_V3_4_CBIU_THREE_ROUND_RESULTS_20260717_CN.md) | Latest emit-utility evidence and admission bar |
| [v3.4 attribution matrices](docs/versions/v3.4/FLUED_V3_4_ATTRIBUTION_MATRICES_RESULTS_20260716_CN.md) | Two-stage failure, memory usage weights, interventions |
| [v3.4 post-migration report](docs/versions/v3.4/FLUED_V3_4_POST_MIGRATION_EXPERIMENTS_20260715_CN.md) | Corrected 20K defaults (plain lookup, decoder, memory) |
| [v3-family checkpoint audit](docs/research/evidence/v3-family/FLUED_V3_FULL_METRIC_TABLE_REEVALUATION_CN.md) | Strict historical checkpoint re-evaluation |
| [v2 rebuild](docs/versions/v2/FLUED_REBUILD.md) | v2 semantic rebuild notes |

## Repository Map

```text
flued/model.py                         FLUED v2 model
flued/v33/                             v3.3 byte-to-latent interface prototype
flued/v34/                             v3.4 rate/emit and parallel-memory extension
flued/v36/                             v3.6 KDA-generation current mainline
flued/e1_stage_a.py                    v2 denoising reconstruction trainer
flued/e3_train.py                      downstream language-model training
flued/e3_downstream.py                 FLUED/BPE/BLT downstream wrappers
tools/*/v3_0...v3_6/                   versioned experiment utilities
tools/train/v3_6/                      current v3.6 training entrypoint
tools/baselines/                       BPE/BLT/H-Net baseline reproductions
configs/canonical_v36.json             current canonical default
configs/v3_3/, configs/v3_4/           versioned experiment matrices
docs/versions/                         version-frozen design and result records
results/v3.4/5k_ablation/              v3.4 public raw logs and curve artifacts
results/v3.4/memory_position_20k_20260713/ v3.4 corrected P3/P4 logs and threshold trajectories
results/v3.6/rd_frontier_20260802/     v3.6 RD frontier public artifacts
```

## Quick Start

Install a CUDA-compatible PyTorch stack and run a CPU smoke test:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu128
pip install tokenizers numpy tqdm
python -m flued.e1_stage_a --preset smoke_cpu
```

Run the current v3.6 canonical smoke test:

```bash
python tools/train/v3_6/train_v36_s1.py \
  --config configs/canonical_v36.json \
  --data-path /path/to/corpus.txt \
  --out-dir outputs/v36_smoke \
  --device cpu --max-steps 2
```

Run the current v3.6 20K route:

```bash
python tools/train/v3_6/train_v36_s1.py \
  --config configs/canonical_v36.json \
  --data-path /path/to/corpus.txt \
  --out-dir outputs/v36_default
```

The v3.4 historical route (single-seed 38M / 20K probe, see
`docs/versions/v3.4/`):

```bash
python tools/train/v3_4/train_v34_pos_ar_probe.py \
  --config configs/v3_4/v34_default_38m_20k.json \
  --data-path /path/to/corpus.txt \
  --out-dir outputs/v34_default_38m_20k
```

Run the v3.4 matrix on GPU (historical ablation line):

```bash
python tools/launcher/v3_4/run_v34_pos_ar_matrix.py \
  --matrix configs/v3_4/v34_rate_emit_all_ablation_5k.json \
  --out-root outputs/v34_5k \
  --batch-size 8
```

Rebuild the v3.4 public curve summary:

```bash
python tools/analysis/v3_4/analyze_v34_5k_curves.py \
  --root outputs/v34_5k --out-dir outputs/v34_5k/analysis
```

Representative v2 E1 run:

```bash
python -m flued.e1_stage_a \
  --preset class300m_16gb \
  --data-path /path/to/corpus_v3.txt \
  --ckpt-dir checkpoints/e1_v2_seed42 \
  --max-steps 50000 \
  --seq-len 512 \
  --stride 256 \
  --grad-accum-steps 12 \
  --denoise-prob 0.7 \
  --corrupt-rate 0.15 \
  --latent-consistency-weight 0 \
  --amp --amp-dtype bf16
```

## Known Limitations

1. v2 soft assignment still builds a full `[B, T, T]` matrix internally.
2. Compression control is weak; target compression does not reliably control
   the final `m/n`.
3. v3.4 evidence is still one seed, 20K steps, 512-byte sequences, and a 38M
   FLUED probe rather than the planned 300M / 4096-byte scale.
4. L2 marginal rate and hard emit reorganize substantially between 9K and 12K;
   semantic boundary quality is not established by long-context downstream tasks.
5. The memory line is closed (E7/E13): no measurable gain across 512–4096B,
   with the gate learning to shut itself off and an 11–26% throughput tax.
6. The current public claim is a traceable research process and executable
   architecture, not benchmark dominance.

## License

MIT. See [LICENSE](LICENSE).
