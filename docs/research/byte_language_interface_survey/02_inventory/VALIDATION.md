# Validation — frozen author and translator handoff

2026-11-09 · documentary verification only. This ledger distinguishes source reading, claim adjudication, structural checks and scientific/runtime verification. Final counts are in [FINAL_AUTHOR_COUNTS](FINAL_AUTHOR_COUNTS.md).

## 1. Inputs and write boundary

Read latest [CLAIM_RULES](../05_review/CLAIM_RULES.md), [FULL_READING_AUDIT_R2](../05_review/FULL_READING_AUDIT_R2.md) and the complete [CLASSIFICATION_EN](../04_synthesis/CLASSIFICATION_EN.md). R2 is a targeted original-passage audit of ten works, with zero new FULL credit; it does not replace terra or certify all records. This closeout performs no new paper-reading credit, model training, execution of paper software, experiment, network lookup, dependency install, agent dispatch, Git commit or push.

Only `02_inventory/` is written. Source cards, old cards, reviewer files and synthesis classification are read-only. Ninety-seven external input files were SHA256-compared with their start-of-closeout hashes: three supplied review/classification documents, sixty R01–R10 cards, thirty old cards and four field cards. They are unchanged. Other shared repository changes cannot be ruled out by Git status alone; the specific write boundary and checked input hashes are the evidence here.

## 2. Exact frozen identities and relations — PASS

| Check | Saved-deliverable result |
|---|---|
| Canonical work IDs/titles |141 sequential unique BIWs; exact same IDs and titles as pre-closeout |
| Canonical record IDs/titles |296 sequential unique BIPs; exact same IDs and titles as pre-closeout |
| Record→work / family / status |Every one of the 296 canonical relation is identical to pre-closeout; no dynamic ID/tag/status change |
| Contributing work union |140 entities; proposal-only BIW-0102 contributes none |
| Historical provenance |423 source-ID rows, 496 edges, exact reverse-ledger text unchanged |
| New addendum provenance |10 central FAD keys, 10 edges; combined 433 keys / 506 edges, unchanged |
| Manual multi-label families |12 families; record union 296; 506 distinct record–family pairs |
| Family source unions |Exact twelve record/work count pairs match CLASSIFICATION_EN |
| Editorial home routes |13 disjoint routes, 296 records exactly once; navigation only, not new canonical tags |
| Entity source genres |136 academic papers, 1 official research report, 3 standards, 1 official introduction = 141 |
| Record source genres |289 academic-paper, 2 report, 3 standard, 2 introduction = 296; academic/research subtotal 291 |
| New/old FULL identity sets |62 new ∩ 30 old = ∅; explicit union 92 |
| Cohort evolution |Prior 80 plus 12 distinct later FULL identities = 92; no reading-status changes from R2 |
| Intentional narrow partials |ELMo BIW-0140 / GPT-2 BIW-0141 explicitly PARTIAL, outside all 92 FULL identities |

The twelve family counts are 35/37/43/43/14/35/33/53/37/60/33/83. Their sum of 506 is separate from the coincidentally equal provenance-edge count. Exact family/work pairs are in FINAL_AUTHOR_COUNTS; summed family-work counts are not distinct papers.

### Frozen relation fingerprints

These SHA256 values identify the normalized UTF-8 canonical JSON/text relations used by the temporary validator; they are not hashes of the entire mutable prose files. JSON uses sorted keys, compact separators and unescaped Unicode. The provenance fingerprint covers the exact normalized-read text following `SOURCE_MAP`, including the appended field mapping. Future English/Chinese prose edits must not alter these relations without explicit central-owner review; the synthesis stage is not authorized to renumber them.

| Frozen object | SHA256 |
|---|---|
| `BIW_ID_TITLE` | `7e85d8e039c71b192911ecd24537685694d2e0f21eebe43b278569dbd6600e18` |
| `BIP_ID_TITLE_WORK_TAG_STATUS` | `6dcdfe977758bf6ea9ada6adface45c0b586c69ca0cef8864d0baeebf2f6107d` |
| `PROVENANCE_LEDGER_TEXT` | `a3e8dfdbb16cd48219dbd8ca8023daf5e84f40df2fe0f2075521cc8194ee73d4` |
| `FAMILY_MEMBERSHIP` | `92f72987bb3bcb06505ba86f6bcdb1addbdcdbe3bc2d73802cc466e89858d301` |

## 3. R2 claim propagation — PASS, no card edits

All thirteen affected BIPs and five affected work entries contain the final claim-rule adoption, matched by canonical work meaning rather than reader list position:

| Work / claim | Canonical BIPs checked | Result |
|---|---|---|
| [BIW-0134](WORK_CATALOG.md#BIW-0134) | [BIP-0124](DETAILED_INVENTORY.md#BIP-0124) | Final R2 qualification present |
| [BIW-0104](WORK_CATALOG.md#BIW-0104) | [BIP-0221](DETAILED_INVENTORY.md#BIP-0221) | Final R2 qualification present |
| [BIW-0072](WORK_CATALOG.md#BIW-0072) | [BIP-0103](DETAILED_INVENTORY.md#BIP-0103), [BIP-0104](DETAILED_INVENTORY.md#BIP-0104) | Final R2 qualification present |
| [BIW-0079](WORK_CATALOG.md#BIW-0079) | [BIP-0171](DETAILED_INVENTORY.md#BIP-0171), [BIP-0172](DETAILED_INVENTORY.md#BIP-0172), [BIP-0173](DETAILED_INVENTORY.md#BIP-0173) | Final R2 qualification present |
| [BIW-0051](WORK_CATALOG.md#BIW-0051) | [BIP-0077](DETAILED_INVENTORY.md#BIP-0077), [BIP-0078](DETAILED_INVENTORY.md#BIP-0078), [BIP-0079](DETAILED_INVENTORY.md#BIP-0079), [BIP-0080](DETAILED_INVENTORY.md#BIP-0080), [BIP-0285](DETAILED_INVENTORY.md#BIP-0285), [BIP-0286](DETAILED_INVENTORY.md#BIP-0286) | Final R2 qualification present |

- Dialect: table TP/IP signs unchanged; categorical TP-prose contradiction withdrawn. The later positive Llama sentence may refer to IP (+0.268), while TP is −0.380. Coefficients do not establish significance, paired sample count or causal fairness. Owned historical copies explicitly identify withdrawn/pending attributions rather than leave them as unqualified current assertions; original cards remain untouched.
- MYTE: model rows and aggregate columns are explicit;21.1/21.8MyT5 versus21.9/23.1ByT5 inTable8, separate fromTable4's20.4versus20.1LRsummary. Population/aggregation reconciliation remains open.
- Hourglass: shifted-input residual preserves the immediately preceding symbol. Specific copying restriction is not blanket within-group independence, a leak, or an arbitrary dependency/learning guarantee.
- MtPC: ordinary Algorithm 3 residual correction and optimized Algorithm 2 wrapper are different claims. Literal partialaccept/discard/restart concern is an analyst derivation, not an implementation reproduction or measured software bias. Exact optimized stochastic law remains unverified; normalized circuits, reported acceptance and throughput retain their separate scope. A stochastic counterexample is not a proven greedy mismatch.
- TokSuite: R2 reconfirms printed PDF wording, not actual Figure 6 computation. Prior three-file static-code evidence is attributed. Figure 6 cannot certify equal cross-tokenizer BPB/training sufficiency; the plot pipeline remains unknown, not a verified implementation error. Other evaluations remain separately supported.

All author/translator ledgers link the latest review authority. Paper specification, analyst derivation, immutable static artifact and run-linked runtime evidence are distinct. Actual technique use and analogy are not equated; intentional narrow reads are not FULL or failed full assignments.

## 4. Check commands and saved-file validation

Executed `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 python _validate_closeout.py` in the owned directory. It reads actual saved Markdown/card identities, verifies frozen relations and explicit counts, checks external-input hashes and then checks this ledger together with the other deliverables. Temporary helper scripts and JSON snapshots are removed after final validation; they are not maintained project tooling.

The final UTF-8, links/anchors, table widths, ID uniqueness, source-map equality, protected external-input hashes and whitespace results are reported below after the checker completes. `git diff --check -- docs/research/byte_language_interface_survey/02_inventory` is supplementary: these deliverables are untracked, so direct saved-file validation rather than Git diff alone covers their contents. No application build or pytest is appropriate for documentary-only edits.

Final deliverables: 20 Markdown files — eight prior central documents, new FINAL_AUTHOR_COUNTS and VALIDATION, and ten batch manifests R01–R10. No new work, BIP or reading batch was created. The detailed inventory remains complete; synthesis/translation must preserve its fixed ID and mapping contract.

## Actual checker result

**PASS:** 20 Markdown files; 141 stable BIWs; 296 stable BIPs; thirteen affected BIP claim adoptions; twelve families / 506 memberships; thirteen disjoint home routes / 296 records; 433 provenance keys / 506 edges; 62 new plus 30 reused scoped FULL identities / 92 distinct sources; two separate intentional narrow PARTIALs. All 97 protected external-input hashes are unchanged. Saved UTF-8, whitespace, table widths and 10,745 local Markdown links / applicable canonical anchors passed. FULL counts and source-genre partitions remain unchanged. These are documentary checks, not scientific proof or runtime verification.

`git diff --check -- docs/research/byte_language_interface_survey/02_inventory` also exited 0 without diagnostics; direct saved-file validation, not Git alone, covers untracked Markdown bytes. Final owned-directory status and file listing are checked after deleting the three temporary Python helpers and two owned JSON snapshots. Only twenty intended Markdown files remain; no background task, training/test output or new source download was created.

This closeout writes the eight central files WORK_CATALOG.md, DETAILED_INVENTORY.md, TAXONOMY.md, COUNTS.md, READING_QUEUE.md, EVIDENCE_STATUS.md, CORRECTION_LOG.md and AUTHOR_HANDOFF.md, plus new FINAL_AUTHOR_COUNTS.md and VALIDATION.md, all under02_inventory. Ten existing batch manifests are retained unchanged. No reading card, review, classification file, production source, stable ID, canonical membership or provenance relation was modified.

## Latest P1 repair validation — active fields, not appended overrides

2026-11-09 · adopts [INVENTORY_CLASSIFICATION_REVIEW](../05_review/INVENTORY_CLASSIFICATION_REVIEW.md) P1-01/P1-02. Only the detailed inventory and these correction/validation logs are edited; the carrying cards, work catalog, classification, fixed IDs/titles, source mappings, support classes and family tags remain unchanged. No source was newly read in FULL, no new work/record/reading credit was allocated, and no experiment or software reproduction was performed.

### P1-01: active hybrid technique — closed

BIP-0050's first **Researcher-used techniques and exact roles** field now explicitly identifies the resolution-preserving 3:1 Gated DeltaNet / Gated Softmax Attention backbone, recurrent versus attention role, 5–8-byte hashes, DeltaNet convolution4→16, four-byte mean/unordered-bag curriculum and next-byte CE. “Dense” is not substituted for full softmax attention. The same-parameter versus same-training-FLOP reversal, active-N exclusions, causal units and all historical source/correction evidence are retained; no single intervention is assigned causal credit.

### P1-02: every R09/R10 current record swept — closed

All nineteen records attached to the ten returned R09/R10 works were read against their completed cards and replaced with **one active canonical field set**: one problem, solution, technique, four-unit tuple, learning/causal contract, evidence/budget and limits. Their old discovery-depth/unknown field sets and prior appended integration material are preserved only inside an explicitly superseded historical disclosure. This is not another appended tail correction: a top-down short-field export now receives the current card-attributed result directly.

The sweep includes the five demonstrated review examples and fourteen additional affected records. In particular BIP-0229 uses the frozen-type-embedding spelling-probe tuple, whereas BIP-0230 uses spelling-pretrained initialization of a subword-input/masked-subword-output RoBERTa. BIP-0238 states stopped-gradient per-layer memories and the actual uncached comparison. BIP-0164/0165 state completed table/appendix findings but retain unclear evaluation policy and biased practical estimator/prefix-guide limitations. BIP-0261 states finite candidate-selected outputs and multilabel BCE, retaining Unicode/unfinished-unit/code uncertainty. AU-Net has one byte objective, Strawberry has its actual block-causal channel, and the dialect TP/IP referent correction remains in the first field set.

### Current repair locations

All lines below are observed in the saved repaired Markdown; stable BIP anchors are authoritative if lines later move. The first field set, not historical excerpts, is the export contract.

| Record | Work | Saved heading line / repair scope |
|---|---|---|
| [BIP-0050](DETAILED_INVENTORY.md#BIP-0050) | BIW-0028 | `DETAILED_INVENTORY.md:2238` — active technique only |
| [BIP-0095](DETAILED_INVENTORY.md#BIP-0095) | BIW-0064 | `DETAILED_INVENTORY.md:3990` — entire primary current field set |
| [BIP-0096](DETAILED_INVENTORY.md#BIP-0096) | BIW-0064 | `DETAILED_INVENTORY.md:4086` — entire primary current field set |
| [BIP-0097](DETAILED_INVENTORY.md#BIP-0097) | BIW-0064 | `DETAILED_INVENTORY.md:4181` — entire primary current field set |
| [BIP-0098](DETAILED_INVENTORY.md#BIP-0098) | BIW-0064 | `DETAILED_INVENTORY.md:4276` — entire primary current field set |
| [BIP-0099](DETAILED_INVENTORY.md#BIP-0099) | BIW-0064 | `DETAILED_INVENTORY.md:4371` — entire primary current field set |
| [BIP-0108](DETAILED_INVENTORY.md#BIP-0108) | BIW-0077 | `DETAILED_INVENTORY.md:4802` — entire primary current field set |
| [BIP-0124](DETAILED_INVENTORY.md#BIP-0124) | BIW-0134 | `DETAILED_INVENTORY.md:5580` — entire primary current field set |
| [BIP-0142](DETAILED_INVENTORY.md#BIP-0142) | BIW-0071 | `DETAILED_INVENTORY.md:6375` — entire primary current field set |
| [BIP-0143](DETAILED_INVENTORY.md#BIP-0143) | BIW-0071 | `DETAILED_INVENTORY.md:6472` — entire primary current field set |
| [BIP-0164](DETAILED_INVENTORY.md#BIP-0164) | BIW-0078 | `DETAILED_INVENTORY.md:7339` — entire primary current field set |
| [BIP-0165](DETAILED_INVENTORY.md#BIP-0165) | BIW-0078 | `DETAILED_INVENTORY.md:7438` — entire primary current field set |
| [BIP-0229](DETAILED_INVENTORY.md#BIP-0229) | BIW-0110 | `DETAILED_INVENTORY.md:10129` — entire primary current field set |
| [BIP-0230](DETAILED_INVENTORY.md#BIP-0230) | BIW-0110 | `DETAILED_INVENTORY.md:10230` — entire primary current field set |
| [BIP-0233](DETAILED_INVENTORY.md#BIP-0233) | BIW-0113 | `DETAILED_INVENTORY.md:10399` — entire primary current field set |
| [BIP-0236](DETAILED_INVENTORY.md#BIP-0236) | BIW-0118 | `DETAILED_INVENTORY.md:10580` — entire primary current field set |
| [BIP-0237](DETAILED_INVENTORY.md#BIP-0237) | BIW-0118 | `DETAILED_INVENTORY.md:10679` — entire primary current field set |
| [BIP-0238](DETAILED_INVENTORY.md#BIP-0238) | BIW-0119 | `DETAILED_INVENTORY.md:10774` — entire primary current field set |
| [BIP-0261](DETAILED_INVENTORY.md#BIP-0261) | BIW-0127 | `DETAILED_INVENTORY.md:11740` — entire primary current field set |
| [BIP-0265](DETAILED_INVENTORY.md#BIP-0265) | BIW-0064 | `DETAILED_INVENTORY.md:11954` — entire primary current field set |

### Verification and limitations

A direct saved-file checker confirms 296 unchanged sequential record IDs/titles, 141 unchanged catalog identities, unchanged record→work/tag/status relations, 506 unchanged family memberships and the exact same source reverse ledger (423historicalkeys/496edges plus10FADkeys/10edges). All nineteen repaired records have exactly one active unit, learning, evidence, limit and technique field; no superseded A/P reading ceiling or already-satisfied full-read request remains in those fields. Unreported fields and unverified runtime/actual prefix behavior are deliberately retained, not declared failures or completed by reading alone. MtPC/TokSuite unrelated open guarantees are unchanged.

Source cards are attributed evidence, not freshly reproduced tables or independently certified proofs. Only DETAILED_INVENTORY.md, CORRECTION_LOG.md and VALIDATION.md change as final deliverables. Temporary owned structuring/check scripts and snapshots are removed after verification; no production edit, installation, training, network lookup, agent dispatch, commit or push.

**Actual latest check:** `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 python _verify_repair.py` — PASS on all twenty saved Markdown files; current-field uniqueness/semantic assertions for nineteen records, BIP-0050 hybrid technique, frozen identity/source/tag/status relations, fourteen read-only external input hashes, UTF-8/table/whitespace checks and 10,881 local links/applicable anchors. `git diff --check -- docs/research/byte_language_interface_survey/02_inventory` is supplementary because the artifacts are untracked. No application build/pytest or original experiment was run.
