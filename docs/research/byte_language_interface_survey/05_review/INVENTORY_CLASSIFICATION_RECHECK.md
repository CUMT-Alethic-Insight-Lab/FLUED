# Inventory/classification P1 repair recheck

2026-11-09. Focused independent recheck of the owner's response to [INVENTORY_CLASSIFICATION_REVIEW](INVENTORY_CLASSIFICATION_REVIEW.md), P1-01 and P1-02. Only this recheck file was written; the inventory, original review, evidence cards and classification were not modified.

## Decision

**PASS — both P1 findings are closed. The inventory/classification materials may proceed to translation.** No remaining P0/P1 error was found within this repair scope. Translation must use the current active canonical fields and latest [CLAIM_RULES](CLAIM_RULES.md), not superseded historical extracts.

This is a repair recheck, not a second full inventory audit or fresh original-paper reading. It does not certify all literature claims, software behavior or mathematical proofs. It adds **zero FULL credits**, records, works or experiments. The original review remains the historical record of the pre-repair findings; this file supplies their current closure.

## 1. Scope and method

Checked the active BIP-0050 technique field; all **19 records belonging to the ten R09/R10 works**; their first problem/solution/technique/unit/learning/evidence/limit fields; their historical disclosures; current documentary counts; and the dialect correction against CLAIM_RULES §7. Revisited carrying-card passages for the repaired roles and results, including REINFORCE, Transformer-XL, SpellingBee, T-FREE, deep self-attention, plain byte scaling, Sparse Transformer, AU-Net and Strawberry. Existing cards supply the source evidence: this reviewer did not replace terra reading with inferred details or claim new original-source verification.

The 19-record repair cohort is:

`BIP-0095, 0096, 0097, 0098, 0099, 0108, 0124, 0142, 0143, 0164, 0165, 0229, 0230, 0233, 0236, 0237, 0238, 0261, 0265`.

Together with BIP-0050, these are **20 inspected repair records**, not 20 new sources. The focused read-only checks used in-memory Python and direct Markdown/card reads; no temporary script, network fetch, install, training or subagent was needed.

## 2. P1-01 closed: actual hybrid techniques are in the first field

**Current locator:** [BIP-0050](../02_inventory/DETAILED_INVENTORY.md#BIP-0050), `DETAILED_INVENTORY.md:2238–2256`; researcher-technique field at line 2245 in the inspected snapshot.

The first active field now identifies:

- Resolution-preserving **3:1 Gated DeltaNet / Gated Softmax Attention** mixing, distinguishing gated recurrent layers from attention layers.
- Hashed **5–8-byte n-gram** inputs.
- Wider DeltaNet convolution **4→16**.
- Initial four-byte mean-input/unordered-bag curriculum followed by next-byte cross-entropy.
- The absence of an explicit local–global–local hierarchy, without misreading “dense” as full softmax attention in every layer.

These are actual source-attributed techniques and roles, not analyst analogy. The co-varying interventions remain explicitly **not a tokenizer-only comparison**. The same-parameter byte advantage versus same-training-FLOP subword advantage and parameter/FLOP exclusions remain intact; no isolated causal benefit is assigned to one added technique.

The superseded “Dense byte Transformer+hash n-grams” wording remains at line 2264 **inside a closed-by-default historical disclosure** beginning at line 2258. It is not a competing active canonical technique. A short-field export now obtains the hybrid identity directly, satisfying the original closure criterion. Carrying authority remains the fixed-source correction already cited in the record, [W0356 card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md) and current author handoff; no additional original read is claimed here.

## 3. P1-02 closed: completed evidence replaces obsolete active ceilings

Every one of the 19 R09/R10 records now has **exactly one active** problem, solution, technique, four-unit tuple, learning contract, evidence/budget field and limits field before its historical disclosure. The former active discovery/integration material is enclosed by:

> Superseded discovery and integration field sets — historical only; current canonical fields are above

All 20 inspected records have balanced `<details>` nesting; none has a premature closing tag or an unclosed historical block. Thus nested old “current” headings stay historical rather than escaping into the active record.

### Demonstrated original examples

| Record / current heading line | Rechecked current content | Result |
|---|---|---|
| [BIP-0238](../02_inventory/DETAILED_INVENTORY.md#BIP-0238), line 10774 | Stopped-gradient per-layer segment memories, relative positions and causal current/cached K/V are specified. Reported model sizes and 363×/1,874× **uncached evaluation** comparisons replace abstract-only unknowns. Timing hardware/batch/precision, actual aliases and serving details remain appropriately unreported/unverified. | Closed; consistent with [Transformer-XL card](../03_reading/R09/BIW-0119.md), §§3.1–3.3/Tables 2/9. |
| [BIP-0229](../02_inventory/DETAILED_INVENTORY.md#BIP-0229), line 10129 | Frozen uncontextualized type embeddings → independently trained Transformer spelling probe → character sequences → spelling CE. Type/filter controls and completed Table 1/Appendix E evidence are explicit. Probe recoverability is not host spelling behavior. | Closed; consistent with [SpellingBee card](../03_reading/R10/BIW-0110.md), §§2–3/Table 1/Appendix E. |
| [BIP-0230](../02_inventory/DETAILED_INVENTORY.md#BIP-0230), line 10230 | The distinct **spelling-initialization intervention** now has subword-input/masked-subword-output RoBERTa units. The pretask is neither a continuing loss nor an inference probe. The <0.01 loss separation after 1,000 updates remains a bounded reported null. | Closed; distinct from BIP-0229 and consistent with the same card's §5/Figure 2. |
| [BIP-0164/0165](../02_inventory/DETAILED_INVENTORY.md#BIP-0164), lines 7339/7438 | Completed table/appendix evidence, ordinary LM plus score-function terms, sampled boundaries, early-exit baseline, rate pressure and γ=.99 discount are named. Discount bias, unclear evaluation sampling, the same-batch baseline and unverified actual BPE-guide prefix stability remain qualified. | Closed; consistent with [REINFORCE card](../03_reading/R09/BIW-0078.md), §§2–4/Appendices A/D.1. No proof or implementation guarantee inferred from FULL. |
| [BIP-0261](../02_inventory/DETAILED_INVENTORY.md#BIP-0261), line 11740 | Rule-split complete units, binary hashed trigrams, sigmoid multilabel BCE and finite-candidate dictionary outputs now appear in the primary fields. Dictionary regimes, feature-training versus candidate-decoding distributions and unfinished-unit/Unicode uncertainty remain separate. | Closed; consistent with [T-FREE card](../03_reading/R10/BIW-0127.md), §§3.1–3.2/Algorithms 1–5. No native-byte or unrestricted novel-word output claim. |

### Additional upgraded records

The sweep is not limited to the five originally demonstrated examples:

- **0095–0099/0265:** deep full-resolution attention, scheduled layer losses, all-position supervision, future-offset heads, uncached scoring and corpus accounting retain different roles. Future supervision does not become future input or an exact joint sampler.
- **0142/0143:** plain byte scaling and processed-corpus byte/word count conversion remain distinct; UNK-replaced/sentence-shuffled LM1B is not untouched raw-text evidence.
- **0236/0237:** sparse connectivity and practical kernels/initialization/recomputation remain distinct. Table 2's Time/Iter retains its **unspecified unit**, strided quality deterioration and non-serving scope.
- **0108:** AU-Net uses rule-derived groups and shifted expansion under **one next-byte objective**, not independently supervised word heads. Actual regex prefix stability remains unverified, not a measured leakage verdict.
- **0233:** Strawberry names its block-causal character channel, consumed-token visibility and token outputs; percolation remains explanatory analysis rather than another implemented module. The onset threshold is **0.5%**, not 50%.
- **0124:** descriptive dialect parity correlations and unequal encoder/decoder adaptation remain explicit; see §4.

Six diagnostic stale phrases from the original P1 were searched across the saved inventory, including “Gradient-stop details not read here,” “full hyperparameter/figure review still missing,” and the T-FREE mechanism “need full read” request. **Every hit is inside historical disclosure at positive nesting depth; none is active.** Retaining this superseded provenance is acceptable and must not be mistaken for an unfinished assignment. Real runtime/Unicode/cost unknowns were not improperly erased.

## 4. Dialect wording matches latest CLAIM_RULES

The first active [BIP-0124](../02_inventory/DETAILED_INVENTORY.md#BIP-0124) evidence and limits fields now explicitly preserve [CLAIM_RULES §7](CLAIM_RULES.md#7-new-r10-clarification-do-not-manufacture-a-dialect-tp-prose-contradiction):

- DI **TP**: Phi **+0.638**, mBERT **+0.4836**, Llama **−0.380**.
- DI **IP**: Phi **−0.413**, Llama **+0.268**.
- The later positive Llama sentence can refer to IP; a **definite TP-sign contradiction is withdrawn**, not treated as a confirmed source conflict.
- No paired-n/significance, causal fairness effect or irreversible Unicode corruption is inferred. Quantized decoder LoRA and full encoder tuning remain different resource conditions.

This qualification is also present in [FINAL_AUTHOR_COUNTS](../02_inventory/FINAL_AUTHOR_COUNTS.md). Translate the named metrics and uncertainty, not the superseded card wording.

## 5. Statistics and classification: no repair-driven inflation

The following were independently recomputed from current saved documents, rather than accepted only from the owner's closure claim:

| Object | Rechecked result |
|---|---|
| Stable BIP sequence | **296**, exactly 0001–0296, no duplicate/missing ID |
| Catalog BIW anchors | **141** |
| Active support classes | **145** new FULL + **88** reused FULL + **53** discovery A/P + **3** normative + **2** introduction + **4** narrow PARTIAL + **1** correction-PARTIAL/open = **296** |
| FULL-supported records | **233**, not independent experiments |
| Overlapping family counts C01–C12 | **35/37/43/43/14/35/33/53/37/60/33/83**, total **506**; union **296** |
| Index/body/taxonomy tag agreement | No discrepancy |
| Thirteen exclusive home routes | **296 assignments / 296 unique IDs**, no omissions or duplication |
| Historical reverse ledger | **423 source keys / 496 edges** |
| Field-addendum extraction keys | **10 unique keys / 10 edges**; combined **433 keys / 506 provenance edges** |

Family-membership edges and provenance edges remain different relations despite their equal 506 totals. Counts agree with [COUNTS](../02_inventory/COUNTS.md) and [FINAL_AUTHOR_COUNTS](../02_inventory/FINAL_AUTHOR_COUNTS.md). The declared **92-source scoped-FULL union** and **140 contributing entities** are unchanged handoff totals from the prior reconciliation; this narrow recheck did not redo the entire historical receipt/identity audit. No repair creates another FULL or promotes the deliberate ELMo/GPT-2 partials.

## 6. Translation permission and retained limits

**The two inventory/classification P1 blockers are cleared; translation can begin without another repair round or broad reading batch.** Preserve stable IDs, record types, four units, actual technique roles and source-specific uncertainty. Historical disclosures are provenance, not alternate current conclusions; they must never override active canonical fields. Translation of any retained historical material must preserve its superseded label.

This permission does **not** close unrelated guarantees: MtPC optimized stochastic-wrapper preservation and TokSuite's actual Figure 6 computation remain open under CLAIM_RULES. Such explicitly bounded unknowns are not evidence of broken software and do not require declaring the entire inventory untranslatable.

**Verification:** focused in-memory checks passed for the 19-record cohort's single active field sets, historical-only stale hits, balanced disclosures for all 20 repair records, current support census, record/tag/family relations, home partition and provenance counts. The saved 103-line review passed all 18 local-link existence checks, Markdown table-width, UTF-8 and trailing-whitespace checks. `git diff --check -- docs/research/byte_language_interface_survey/05_review/INVENTORY_CLASSIFICATION_RECHECK.md` exited 0; targeted Git status shows this sole intended new deliverable. Because the survey is untracked, the direct saved-file checks are substantive and Git's whitespace check is supplementary. No application build/pytest is relevant to this documentary-only recheck. No inventory/checklist, source card, earlier review, synthesis or production file was edited.
