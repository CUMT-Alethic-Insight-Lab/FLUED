# Final coverage revision recheck — translation clearance

2026-11-09. A bounded recheck of [REVISION_LOG_EN](../04_synthesis/REVISION_LOG_EN.md) and the three revised final English deliverables against this reviewer's [FINAL_SURVEY_COVERAGE](FINAL_SURVEY_COVERAGE.md). This is not another field investigation or a fresh whole-source audit.

## 1. Decision

**The coverage-review lane is cleared for complete Chinese translation. Residual P0: 0. Residual P1: 0. All three coverage P2 items are closed at the requested scope.** The earlier P1 was a balance omission, not a missing-family or experimental blocker; the author has supplied direct positive evidence without removing the relevant controls.

The log's four COVERAGE entries at `04_synthesis/REVISION_LOG_EN.md:9–12` correspond to actual changes in the saved author text. They are not merely completion declarations. No additional terra full reading, discovery batch, model experiment, or author-text change is required by this coverage recheck.

This decision closes **COVERAGE P1-01/P2-01/P2-02/P2-03 only**. The author's separate RIGOR entries are visible in the log but are not independently signed off by this reviewer. Clearance here does not certify paper code, runtime aliases, stochastic-wrapper correctness, or a common-resource frontier.

## 2. Finding-by-finding disposition

All locations below refer to the revised files inspected for this recheck.

| Original coverage finding | Actual saved revision and propagation | Disposition |
|---|---|---|
| **P1-01: representative positive hierarchy evidence** | `SURVEY_EN.md:280–282` adds the XL H-Net quality comparison, strong space/one-stage controls, parameter counts, approximate training matching, and separate Chinese/code results. `SURVEY_EN.md:292` adds a conference-version BLT comparison with unequal exposures and the older space arm's missing cross-attention. The positive H-Net system result appears in `EXECUTIVE_SUMMARY_EN.md:35` and `OPEN_QUESTIONS_EN.md:29`, retaining the distinction from boundary-only attribution. | **Closed.** Positive achieved quality is now visible in the scholarly narrative, not only in cards or comparator losses. |
| **P2-01: CharT5 near-control** | `SURVEY_EN.md:173` names 47,198 character entries, single-character SentencePiece, byte fallback, 1.23B total parameters, 36/12 layers, width 1,376, approximately 11% lexical parameters, and the three task comparisons. It explicitly rejects pure-byte/code-point-only classification, isolated-alphabet causation and statistical equivalence. `EXECUTIVE_SUMMARY_EN.md:13` includes the hybrid and changed capacity allocation without repeating all numbers. | **Closed.** This near-control is incorporated with its actual interface and confounds. OQ does not need another numeric repetition to close this item. |
| **P2-02: explicit G2P error unit** | `SURVEY_EN.md:171` now states transliteration **CER 10.5%/18.1%**, G2P **PER 1.8%/6.7%**, morphology **accuracy 89.7%/75.7%**, and separate G2P **word error rates 15.4%/43.5%**, in ByT5/mT5 order. Table 5 and the versioned source/card are identified. | **Closed.** The original issue was underspecification, not an incorrect number or sign. No need to insert these metrics into every companion file. |
| **P2-03: duplicated audit procedure** | The local MtPC qualification remains at `SURVEY_EN.md:377`; §8.6 preserves the probability-mass distinction and links to OQ-12 at `:387–389`. The worked numerical diagnostic is now at `OPEN_QUESTIONS_EN.md:127`, with equivalent correction-state and no-software-verdict qualifications. Survey §14.3 ends with a short bottleneck synthesis at `:724`; §15.3's artifact discussion is condensed at `:763`. | **Closed.** Useful deduplication occurred without hiding the main scientific limitation in an appendix or deleting the diagnostic. Useful consolidating tables and methodological/translation safeguards remain, appropriately. |

The additional bounded improvement at `OPEN_QUESTIONS_EN.md:20` also adopts the earlier scope recommendation: it now says **“This selected corpus does not establish…”**, not that no paper anywhere has a general utility policy.

## 3. Audit of the added positive numbers and their attribution

### 3.1 H-Net: a positive system result, not an isolated router experiment

The revised main paragraph at `SURVEY_EN.md:280` preserves the following pairing:

| XL system | Average downstream accuracy | Reported GFLOPs/byte |
|---|---:|---:|
| BPE Transformer | 55.5% | 0.69 |
| H-Net(space) | 57.1% | 0.70 |
| H-Net, one stage | 56.2% | 0.72 |
| H-Net, two stages | 58.2% | 0.69 |

These values match the prior targeted primary check recorded in [the original coverage report](FINAL_SURVEY_COVERAGE.md#p1-01--restore-representative-positive-quality-evidence-for-the-central-learned-hierarchy-family) and the [existing H-Net card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md), lines 14–17, carrying [arXiv:2507.07955v2 §3/Tables 1–2/4](https://arxiv.org/html/2507.07955v2#S3). This recheck reread the relevant card passages; it does not claim another fresh original-source verification.

The critical restrictions are present beside the new result:

- BPE has approximately **1.3B** parameters and two-stage H-Net **1.6B**: the text explicitly says **not equal-parameter evidence**.
- The shared FineWeb-Edu subset and **8,192-byte versus 1,792-GPT-2-token** examples are stated. Text per batch and paper-estimated FLOPs are **approximately matched**, not certified identical retained examples.
- The conclusion is explicitly about the **complete hierarchical system under that budget**. The author rejects an isolated learned-boundary effect and a wall-time speed claim.
- The source table's per-byte operation quantity is not promoted into a measured whole-lifecycle or matched-quality serving benchmark.
- Including the space and one-stage controls prevents the misleading inference that every learned variant beats the strong rule. In particular, one-stage accuracy **56.2%** is below space **57.1%** in the quoted setting.

The observed two-stage/BPE difference is **2.7 percentage points**, not a universal percentage gain; the author wisely leaves the raw values rather than amplifying them through a relative-gain headline. The main comparison does not borrow the English budget to certify the Chinese/code runs.

At `SURVEY_EN.md:282`, Chinese XWinograd **59.9%/62.9%/66.3%** and code BPB **0.3376/0.3163/0.3161** remain in BPE/space/two-stage order. The paragraph explicitly changes to Llama-3 BPE and domain-adjusted depths/budgets. It states that dynamic and space are nearly tied on code. **No overstrong cross-budget or cross-domain causal attribution was found.**

The shorter executive summary (`:35`) retains approximate text/FLOP matching, unequal parameters and no boundary-only or wall-time inference. OQ-02 (`:29–33`) uses the positive system result as motivation for, not completion of, the still-needed boundary/aggregation/capacity attribution experiment. This propagation is proportionate to the companion files' functions.

### 3.2 BLT: newly visible quality with exposure/version controls

`SURVEY_EN.md:292` gives the near-monotonic 8B variant's **four-of-seven** downstream wins and the Appendix P ARC-Easy **68.9%/67.2%/67.4%** entropy/space/BPE comparison. These correspond to the [conference-version BLT card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md), lines 13–15, which carries [ACL 2025 §5.2/Table 1 and Appendix P/Table 10](https://aclanthology.org/2025.acl-long.453.pdf).

The same paragraph states approximately **4T/4.5T/6T bytes** for Llama/entropy/space, different patch rates, the early space implementation without cross-attention, and contributions from local attention, n-grams and threshold changes. It therefore does **not** transform the paper's equal-training-FLOP comparison into equal data, complete lifecycle-cost equality, a boundary-only treatment effect, or measured serving superiority. The new BLT claims are card-attributed; this recheck did not reopen the conference original.

### 3.3 CharT5: an engineering alternative, not alphabet equivalence

`SURVEY_EN.md:173` preserves CharT5/ByT5-Large ordering: **79.0%/79.7% XNLI**, **87.6/87.7 TyDiQA F1**, and **11.2/11.5 GEM-XSum BLEU**. This matches the prior targeted [ByT5 arXiv:2105.13626v3 §6.4/Tables 7–8 check](https://arxiv.org/html/2105.13626v3#S6.SS4) recorded in [the original review](FINAL_SURVEY_COVERAGE.md#p2-01--include-the-unusually-relevant-character-vocabularybyte-fallback-near-control).

“Near-competitive results in this setup” is a descriptive comparison, not a statistical equivalence claim. The text explicitly names changed width, capacity allocation, and computation per original text. Byte fallback is retained as part of the representation contract. No equal-compute, pure-code-point, or raw-byte-step inference was added. Formal TACL and arXiv-v3 evidence are individually identified rather than certified byte-identical by association.

## 4. What remains open, and what does not need more work

**Residual coverage P0/P1: none. Residual coverage P2: none requiring action before translation.** The original field-breadth verdict remains in force; this pass does not resample the 18 records, repeat the 22-card survey, recount the entire inventory, or run new public searches. No new FULL credit or evidence upgrade is earned by the textual repair.

The author has not relabeled MtPC's optimized-wrapper law, TokSuite's actual Figure 6 computation, MYTE's population/aggregation linkage, or actual tokenizer/regex prefix stability as closed. Their open wording remains at the relevant main/summary/OQ passages inspected. Such artifact and specification questions are not prerequisites for translating a survey that represents them honestly.

`04_synthesis/04_MULTILINGUAL_EVALUATION_EN.md:79` still has the older generic “grapheme-to-phoneme error” wording. That thematic working draft is **not one of the three revised final deliverables**. This is not a new P1 or an instruction to expand this repair; it means translators should use the final survey as the source of truth rather than importing an older draft paragraph. The metric label in the final survey is now precise.

The revision log also claims closure of a separate RIGOR review. This report verifies the four COVERAGE entries and their interacting new numbers, not the other reviewer's copy-bound or static-config sign-off. Do not cite this report as independent closure of both audit lanes.

## 5. Conditions for proceeding with translation

**Proceed now from this coverage-review lane; no additional author revision is a prerequisite.** Translation should meet these preservation conditions:

1. Use the revised `SURVEY_EN.md`, `EXECUTIVE_SUMMARY_EN.md`, and `OPEN_QUESTIONS_EN.md`, not the pre-revision survey or overlapping thematic drafts. Preserve all sixteen main sections, appendices, tables and OQ anchors; produce a complete translation rather than another summary.
2. Preserve all comparator orders, percent versus percentage-point meanings, task metrics, and units. In particular PER is **phoneme error rate**, CER is **character error rate**, and G2P word error is a third metric.
3. Translate approximate matching as approximate. Retain H-Net's parameter difference, strong space control, system-level attribution and domain-specific budgets; retain BLT's unequal exposure/version controls; retain CharT5's fallback and capacity/compute differences. Do not replace these with “same budget proves learned boundaries/bytes are better.”
4. Keep the MtPC residual/bonus distinction and “unverified, not a measured code bug” status despite the toy example's relocation. Preserve the other named open specifications and the distinction between scoped FULL reading and reproduction.
5. Preserve the unchanged source/record/depth accounting: **141 entities, 296 records, 92 distinct scoped FULL sources (62 new + 30 reused), plus two intentional narrow PARTIALs**. This recheck adds no new paper or reading credit.
6. Treat any separate rigor/bilingual review as its own sign-off; coverage clearance here is not a substitute for it.

These are translation-fidelity conditions, not demands for new experiments or another reading campaign.

## 6. Recheck scope, frozen inputs and verification

This pass read the complete 55-line revision log and the complete revised executive summary and open questions. It inspected only the affected survey ranges and nearby inference/methodology/translation paragraphs, rather than rereading all 810 survey lines. It reread designated H-Net, BLT and ByT5 card passages and used the explicitly recorded targeted source checks from the first review. **No new browser visit, download, full-paper read, paper-code execution, training or subagent was used.**

Read-only Python verified the author's current length diagnostics: survey **19,941**, executive summary **2,115**, and open questions **2,706** whitespace-delimited words. The survey still has **16** numbered sections and `s01`–`s16` explicit anchors; OQ still has **15** numbered question headings. This confirms the present document structure and counts, not the author's unavailable before-snapshot hash comparison or every claim in its separate validator.

The following SHA256 values identify the exact inputs inspected and the translation-ready coverage snapshot:

| File under `04_synthesis/` | SHA256 |
|---|---|
| `SURVEY_EN.md` | `45cbcf639e1d5f598f823619313190ef8c2d64725ee5df95517fb754cb55e685` |
| `EXECUTIVE_SUMMARY_EN.md` | `14317c35e9b1318b26e0d6218c7dc6c7eb5d02d619f20de5d5f530bf7633903b` |
| `OPEN_QUESTIONS_EN.md` | `814b75b0c01da61a3df072d7d047d79c982a6495b869d1d7f79b7e46870691e0` |
| `REVISION_LOG_EN.md` | `c3bfa14aa6de861ea091d75a04bde053003b51029982f55129aaf352141c4a76` |

Only `05_review/FINAL_SURVEY_COVERAGE_RECHECK.md` is created by this task. Author text, inventories, original review, source cards and production files remain read-only. Direct saved-report UTF-8/whitespace/table/local-link checks and comparison of these four input hashes accompany delivery. Repository status is checked, but its already-untracked survey directory is not by itself proof of per-file ownership. Application build/pytest is not relevant to this documentary-only recheck and is not run.

**Final disposition: coverage revisions accepted; translation permitted with the preservation conditions above; no residual P0/P1 and no additional terra full reading required.**
