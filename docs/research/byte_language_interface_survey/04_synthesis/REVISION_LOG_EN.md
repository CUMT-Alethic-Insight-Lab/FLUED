# Revision log: final English survey audit closeout

2026-11-09. This revision addresses both [FINAL_SURVEY_COVERAGE](../05_review/FINAL_SURVEY_COVERAGE.md) and [FINAL_SURVEY_RIGOR](../05_review/FINAL_SURVEY_RIGOR.md): **both P1 findings and all six P2 findings are addressed**. Identical finding numbers in the two reports refer to different items; the report prefix below disambiguates them. Changes are confined to the three English author files and this log. No inventory, source card, review, identifier, or canonical family assignment is changed.

## 1. Finding-to-change mapping

| Audit finding | Change and stable destination | Evidence and preserved condition | Status |
|---|---|---|---|
| **COVERAGE P1-01 — positive learned-hierarchy evidence** | Added H-Net's native quality comparison in [survey §6.4](SURVEY_EN.md#s06): XL BPE/two-stage accuracy 55.5%/58.2% at 0.69/0.69 GFLOPs/byte, space 57.1%/0.70, and one-stage 56.2%/0.72. Added Chinese and code controls; propagated the positive system result to executive-summary §5 and [OQ-02](OPEN_QUESTIONS_EN.md#oq02). Also added one direct BLT quality comparison in survey §6.5. | H-Net v2 §3/Tables 1–2/4 and [W0011 card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md). Approximately 1.3B versus 1.6B parameters, approximate text-per-batch/FLOP matching, and different domain budgets remain explicit. Code space/dynamic BPB is nearly tied. BLT uses the [conference-version W0010 card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md), §5.2/Appendix P: unequal byte exposures/rates and the older space arm's missing cross-attention prevent a boundary-only interpretation. No wall-time win is inferred. | Addressed |
| **COVERAGE P2-01 — CharT5 near-control** | Added a paragraph in [survey §4.5](SURVEY_EN.md#s04) and a short executive-summary §2 reference: 47,198 character entries with byte fallback; 1.23B total parameters, 36/12 layers, width 1,376, about 11% lexical parameters; XNLI 79.0%/79.7%, TyDiQA F1 87.6/87.7, GEM-XSum BLEU 11.2/11.5 for CharT5/ByT5-Large. | ByT5 arXiv:2105.13626v3 §6.4/Tables 7–8, using COVERAGE's recorded targeted primary-source check and the existing [W0351 card's](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md) formal-source ablation scope. This is a common-character/fallback hybrid, not unrestricted code-point-only processing. Changed width, parameter allocation, and per-text computation prevent an alphabet-only or statistical-equivalence claim. No new author whole-source reading is claimed. | Addressed |
| **COVERAGE P2-02 — phoneme error unit** | Replaced ambiguous “grapheme-to-phoneme error” in survey §4.5 with **phoneme error rate (PER)**, 1.8%/6.7%; separately named transliteration character error rate and morphology accuracy. Added the distinct 15.4%/43.5% word error rates. | ByT5 Table 5, W0351 metric/result passages, and COVERAGE's targeted v3 §4.4/Table 5 check. These are different supervised metrics, not interchangeable error units. Also closes the metric portion of RIGOR P2-01. | Addressed |
| **COVERAGE P2-03 — repeated audit procedure** | Kept the local MtPC qualification in [survey §8.4](SURVEY_EN.md#s08) and the probability-mass argument in §8.6; moved the worked numeric discard/restart diagnostic to [OQ-12](OPEN_QUESTIONS_EN.md#oq12). Replaced §14.3's repeated generic evidence-state reminders with a short bottleneck synthesis and shortened §15.3's procedural closeout to its concrete open specifications. | The residual-versus-bonus distinction, target transformations, possibility of equivalent retained correction state, and lack of a released-software verdict remain. The full finite-prefix example is retained in OQ-12; it was relocated, not erased. Useful consolidating tables and local scientific conditions remain intact. | Addressed |
| **RIGOR P1-01 — copy-bound protocol** | Rewrote [survey §12.8](SURVEY_EN.md#s12): input is fully ingested before copying; all input-dependent influence on deterministic output must pass through counted finite distinguishable state S; no source replay, external cache, earlier input-dependent output, or side channel outside S. Added success ≤ min(1, \|S\|/D^L) and the retained-bit necessary condition. Propagated the protocol to executive-summary §8 and [OQ-09](OPEN_QUESTIONS_EN.md#oq09), including experiment resource accounting. | [Repeat After Me W0061 card](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md), arXiv:2402.01032v2 §§2.1/2.3/Appendix D. The safe non-strict counting implication is used. Online echoing, replay-enabled systems, and uncounted caches do not inherit the state-only bound. Natural-language redundancy and query timing remain separate; distinguishable states are not equated with hidden width. | Addressed |
| **RIGOR P2-01 — ByT5 locations/devices** | Attached Table 5 to the task metrics; Table 9 and **TPUv3-64** to pretraining throughput; Table 10 and **TPUv3-32** to XNLI slowdown, both locally and in survey Table 6. Explicitly distinguished XSum's **TPUv3-128**. | W0351 card, Tables 5/9/10 of TACL 2022. XNLI is still a long-input, short-label task, not NER or evidence for a long-output-only slowdown. Fixed positions still expose unequal original text. PER/CER precision overlaps COVERAGE P2-02. | Addressed |
| **RIGOR P2-02 — fitted N exclusions** | Replaced “some components” in [survey §13.2](SURVEY_EN.md#s13) with local encoder/decoder and input/output embedding parameters; distinguished this fitted-N definition from the total-training-FLOP comparison that includes those modules. | [BIW-0047 card](../03_reading/R05/BIW-0047.md), v2 §3.1/Appendix B.1 versus §2.2/Appendix B.2. Fitted N is not whole-resident storage. Entropy-model pretraining/scoring remains an incompletely itemized lifecycle cost, not assumed zero or declared excluded from every compute formula. | Addressed |
| **RIGOR P2-03 — static-config provenance** | Expanded the ByT5 row in [survey Table 5/§10.2](SURVEY_EN.md#s10) with the mutable operative-gin URL, XNLI fine-tuning/million-step-checkpoint context, and pinned Mesh definition at commit 4758510b99614c51ecb56166faff9842befac193. | W0351's existing static check. The gin is not a pristine pretraining log; matching Mesh code does not establish the paper-runtime dependency revision. Runtime aliases and other sizes/ports remain unverified. No new live configuration or weight inspection was performed. | Addressed |

## 2. Additional bounded wording improvement

[OQ-01](OPEN_QUESTIONS_EN.md#oq01) now says that **this selected corpus** does not establish a general cheap causal value policy, rather than making an unqualified literature-wide absence claim. This adopts COVERAGE §8.2's scope recommendation. It does not withdraw the existing distinction between uncertainty, observed confidence, and incremental utility.

The H-Net and BLT additions show achieved benefits with their original controls; existing smoothing, estimator, teacher-cost, language/domain, and execution limitations are retained. The prior MYTE row/column correction, Hourglass residual qualification, dialect TP/IP attribution, MtPC optimized-wrapper uncertainty, and TokSuite Figure 6 restriction are unchanged.

## 3. Source and write boundaries

The author reread both final audits and five existing carrying cards: H-Net/W0011, BLT/W0010, ByT5/W0351, Repeat After Me/W0061, and Compute Optimal Tokenization/BIW-0047. H-Net's Table 1 parameter values and CharT5's detailed values also use COVERAGE's explicitly recorded targeted source checks. ByT5's formal TACL evidence and the separately identified arXiv-v3 CharT5 passage are cited at their own locations; byte-identical versions are not asserted.

No new FULL credit, discovery batch, subagent, public-source download, installation, training, paper-code execution, experiment, or Git commit/push was performed. The four write targets are:

- `04_synthesis/SURVEY_EN.md`
- `04_synthesis/EXECUTIVE_SUMMARY_EN.md`
- `04_synthesis/OPEN_QUESTIONS_EN.md`
- `04_synthesis/REVISION_LOG_EN.md`

All original headings and explicit anchors in the three author files are preserved exactly, including all sixteen survey sections, two appendices, eight numbered tables, and fifteen OQ identifiers. This keeps translation navigation stable; paragraph and line offsets naturally move.

## 4. Updated lengths

Counts use Python's whitespace-delimited `len(text.split())` on saved UTF-8 Markdown, including headings, navigation, tables, equations, and link syntax. They are reproducible length diagnostics, not a publisher's prose-only count. The before snapshot matches the SHA256 fingerprints recorded by the rigor audit.

| Deliverable | Audited before | Revised | Change |
|---|---:|---:|---:|
| SURVEY_EN.md | 19,450 | **19,941** | +491 |
| EXECUTIVE_SUMMARY_EN.md | 2,005 | **2,115** | +110 |
| OPEN_QUESTIONS_EN.md | 2,516 | **2,706** | +190 |

The survey remains a substantial long-form field treatment. Editorial deduplication did not replace detailed comparisons with an abridgment.

## 5. Verification and remaining questions

The three revised author files passed an in-memory standard-library check for UTF-8 decoding, replacement characters, whitespace, balanced fences, consistent Markdown table widths, duplicate explicit anchors, and all **242 local link/anchor references**. SHA256 comparisons of normalized complete heading lists and explicit-anchor lists match the audited before snapshot exactly for all three files. These checks test document structure, not paper software or empirical reproducibility.

**Final saved-file check: PASS.** All four files have **259 local link/anchor references, zero errors**, including the 242 in the three core deliverables. Checks also passed all eight audit-item mappings, sensitive claim wording, frozen 141/296 identity anchors, 62 new plus 30 reused FULL ledger identities with two separate narrow PARTIALs, eight numbered survey tables, fifteen OQ headings, unchanged heading/anchor fingerprints, and elementary copy-bound equality-case arithmetic. `git diff --check` exited 0. Application build/pytest is not relevant to these Markdown-only changes. No helper script or test output is retained. Git status was inspected; because the survey directory is already untracked, direct saved-file validation and the four explicit write targets—not Git status alone—define this task's verification boundary.

The scientific open items are deliberately not relabeled closed: MtPC's optimized stochastic wrapper, TokSuite's actual Figure 6 pipeline, MYTE's evaluated-set/aggregation bridge, and actual tokenizer/regex prefix stability still need their named artifacts or specifications. Closing the two writing audits does not establish those guarantees.
