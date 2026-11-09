# Independent inventory and classification red-team review

2026-11-09. Independent documentary review of the byte-language-interface survey. Only this file is this reviewer's deliverable. Source records, evidence cards and syntheses were not edited.

## 1. Verdict and review boundary

**Conditional pass: no P0 found; two bounded P1 repairs remain in the active inventory fields.** The catalog, overlapping taxonomy and exclusive navigation routes reconcile. The sampled records generally answer a concrete prior-work difficulty with a specific response and named researcher-used techniques. The strongest remaining weakness is not missing papers or inflated family totals: it is the coexistence of current evidence with obsolete or incomplete short fields that a reader can reasonably treat as canonical.

The classification essay and reading guide are substantively stronger than those inconsistent fields. They distinguish native bytes, code points, character-composed word models, byte-BPE, hybrid outputs and standards, and do not claim 296 independent scientific problems. No sampled analyst analogy was promoted to an author-implemented module. Reviewer exceptions are explicitly identified, although they must remain exceptions when exporting the problem–solution table.

### What was actually checked

- Read [PLAN](../PLAN.md), [TAXONOMY](../02_inventory/TAXONOMY.md), [COUNTS](../02_inventory/COUNTS.md), [CLASSIFICATION_EN](../04_synthesis/CLASSIFICATION_EN.md), [INVENTORY_READING_GUIDE_EN](../04_synthesis/INVENTORY_READING_GUIDE_EN.md), the latest [CLAIM_RULES](CLAIM_RULES.md), and the author handoff.
- Read the index and active problem, one-sentence solution and researcher-used-technique fields for **all 296 records**. This is not a claim to have independently verified every carrying result in the much longer repeated evidence blocks.
- Stratified semantic check of **64 records across all 12 families and 36 source entities**: 60 records against 32 existing reading cards, three against their normative catalog/source mappings, and one against the targeted TokSuite correction. The 32 cards comprise 30 scoped-FULL carrying sources and two designated narrow-PARTIAL sources. Their existing reading credits are not this reviewer's credits.
- The 64 sampled records comprise 56 scoped-FULL-supported records, four narrow-PARTIAL records, three normative records and one correction-PARTIAL/open-computation record. These are not 64 independent experiments.
- Directly inspected the retained original dialect-paper passage at [R10/sources/BIW-0134.txt](../03_reading/R10/sources/BIW-0134.txt), lines 270–319, to check the TP/IP referent. Other detailed checks below are **card-attributed**, not fresh original-paper verification.
- Ran read-only, in-memory Python checks over the saved Markdown for record fields, IDs, support classes, memberships, home-route ranges and provenance edges. No generated script, download, installation, training, reproduction or subagent was used.

**P0** here means a central unsupported/fabricated method or result, consequential evidence pooling, or a broken count/partition that undermines the inventory. **P1** means a material, localized fidelity or current-field contradiction that should be repaired before releasing/exporting the detailed inventory. No exhaustive source-verification or runtime certification is implied by the absence of P0.

A concurrent owner updated the inventory during this review. The final source check at approximately **03:20–03:23 UTC+08:00** confirmed that the earlier dialect TP-conflict assertion had been corrected. That observation is recorded as closed below, not counted as an open defect. Anchors and quoted field names are authoritative locators; line numbers describe the inspected snapshot and may move.

## 2. Structural reconciliation

### 2.1 IDs, fields, counts and provenance

| Check | Independently observed result | Interpretation |
|---|---:|---|
| Unique sequential BIP headings | 296, exactly BIP-0001–0296 | No missing/duplicate record ID |
| Required problem / solution / technique / attribution fields | 296 / 296 / 296 / 296 | Field presence passes; semantic adequacy still requires the checks below |
| Unique BIW anchors | 141 | Entity count, not native-byte model count |
| BIW entities contributing indexed records | 140 | Consistent with proposal-only exclusion |
| Active support census | 145 new FULL; 88 reused FULL; 53 A/P; 3 normative; 2 introduction; 4 narrow PARTIAL; 1 correction-PARTIAL/open | 296 total; 233 scoped-FULL-supported records |
| Historical reverse-ledger source keys | 423 rows, 423 unique keys | No duplicated historical key in the saved ledger |
| Historical source-to-BIP edges | 496 | Distinct relation from family membership |
| Field-addendum extraction keys | 10 unique | Adds 10 edges: combined 433 keys / 506 edges |
| Family membership union | 296 records | Every BIP has at least one family |
| Overlapping family memberships | 506 | Not 506 independent problems |
| Index tags versus taxonomy memberships | Zero discrepancies | All 296 tag sets agree |
| Active record tag lists versus index tags | Zero discrepancies | No body/index classification drift |
| Exclusive home-route partition | 296 assignments, 296 unique IDs, no omissions/duplicates | Thirteen routes are navigation, not another scientific taxonomy |

The **92 distinct scoped-FULL source union** is the declared reconciled source-depth total in COUNTS; this review did not independently reread those 92 originals or recreate every historical reading receipt. The checks above independently verify the current record-level support census and structural denominators, not new FULL completion.

### 2.2 All twelve families and sample coverage

Counts were recomputed from TAXONOMY tables, not copied only from CLASSIFICATION_EN.

| Family | All memberships | Distinct works | Sampled record memberships |
|---|---:|---:|---:|
| C01 Units/coverage | 35 | 27 | 11 |
| C02 Composition | 37 | 27 | 10 |
| C03 Segmentation/priors | 43 | 32 | 7 |
| C04 Compute/history | 43 | 28 | 11 |
| C05 Causal availability | 14 | 10 | 6 |
| C06 Output/decoding | 35 | 25 | 7 |
| C07 Sharing/geometry | 33 | 24 | 11 |
| C08 Optimization | 53 | 38 | 10 |
| C09 Adaptation | 37 | 18 | 7 |
| C10 Task/language utility | 60 | 44 | 9 |
| C11 Probability | 33 | 20 | 7 |
| C12 Budget/evidence | 83 | 53 | 15 |

Sample memberships overlap too. They must not be added to obtain the 64 sampled records.

The thirteen home-route counts independently resolve to **20, 22, 21, 38, 31, 22, 22, 26, 14, 29, 30, 16, 5**, in the order printed in CLASSIFICATION_EN §3. Their sum is 296. A home route need not equal the first C label or contain every secondary technique: for example, BIP-0110 can have a probability-interface home and decoding tags without contradiction. No erroneous exclusive-versus-multilabel identification was found.

## 3. Open P1 findings and exact repairs

### P1-01 — Active researcher-technique field omits the defining hybrid backbone

**Exact affected location:** [DETAILED_INVENTORY, BIP-0050](../02_inventory/DETAILED_INVENTORY.md#BIP-0050), active **Researcher-used techniques and exact roles**, inspected line 2243:

> Dense byte Transformer+hash n-grams; first30%fixed4-byte averaged-input/next-bag objective then70%next-byte CE; widened local convolution.

The same record's active unit tuple and central correction correctly identify a **3:1 Gated DeltaNet / Gated Softmax Attention hybrid**. Thus this is not a finding that the entire record or source is misclassified; it is a failure of the specific field promised to name the actual AI techniques and roles. “Dense” can mean non-MoE and must not be silently interpreted as full softmax attention. A short-field export currently drops the selective recurrent component that explains the backbone's computation and convolution.

**Carrying evidence:** [old W0356 scoped card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md), §2.1/Appendix A as attributed there; [AUTHOR_HANDOFF §3](../02_inventory/AUTHOR_HANDOFF.md#other-adopted-corrections), hybrid correction; BIP-0050's own central correction cites fixed **2610.05978v1 §§1/2.1 and Appendix A.4**. CLASSIFICATION_EN §4.12 already uses the correct hybrid identity.

**Repair, without a new read or count:** Replace only the active short technique field with wording such as:

> Resolution-preserving 3:1 Gated DeltaNet/Gated Softmax Attention hybrid; hashed 5–8-byte n-gram inputs; wider DeltaNet convolution; an initial four-byte mean-input/unordered-bag curriculum followed by next-byte cross-entropy. These co-varying interventions are not a tokenizer-only comparison.

Keep the existing same-parameter versus same-training-FLOP reversal and fitted-parameter exclusions. Historical text may remain collapsed and marked superseded. Do not infer that a particular intervention alone caused the frontier change.

**Closure criterion:** An export of just problem/solution/technique/units identifies the same hybrid backbone as the detailed correction and classification essay.

### P1-02 — Obsolete discovery ceilings remain in active fields above completed card findings

**Why material:** [INVENTORY_READING_GUIDE_EN §2](../04_synthesis/INVENTORY_READING_GUIDE_EN.md#2-start-with-the-right-document-and-identifier) correctly says current card-grounded findings supersede collapsed history. The examples below are **not only inside collapsed history**: they remain in the first active field set, alongside a NEW-FULL status, before a second current block supplies the completed evidence. This makes current machine extraction and ordinary top-down reading disagree. It also risks unnecessary repeat terra assignments, contrary to the stop rule.

| Record and exact active field | Still says | Carrying completed evidence | Minimal repair |
|---|---|---|---|
| [BIP-0238](../02_inventory/DETAILED_INVENTORY.md#BIP-0238), technique/units/evidence; inspected lines 10395–10399 | “Gradient-stop details not read here”; cache treatment not newly read; configuration/parameters/procedure unknown | [R09/BIW-0119](../03_reading/R09/BIW-0119.md), lines 7–17; formal §§3.1–3.3, Tables 2/9; separate arXiv-v3 appendix | Say the card reports stopped-gradient per-layer segment memories and relative positions. Retain genuinely unreported timing hardware/batch/precision, not parameters and benchmark baseline already supplied. Distinguish card attribution from fresh reviewer reading. |
| [BIP-0229](../02_inventory/DETAILED_INVENTORY.md#BIP-0229), units/evidence; inspected lines 9872–9874 | A designated “P” passage check, incomplete table/appendix verification, table cells not independently verified | [R10/BIW-0110](../03_reading/R10/BIW-0110.md), lines 3, 13–21; §§2–3/Table 1/Appendix E | Replace the active tuple with frozen subword embedding → independent spelling probe → characters → spelling CE; attribute held-out-type/filter results to the completed card. No claim that this reviewer reran or freshly verified the table. |
| [BIP-0230](../02_inventory/DETAILED_INVENTORY.md#BIP-0230), units/evidence; inspected lines 9949–9951 | Reuses the probe-oriented partial tuple and says full hyperparameter/figure review is missing | [R10/BIW-0110](../03_reading/R10/BIW-0110.md), lines 9, 20–21; §5/Figure 2 | Give the intervention's own tuple: subword-input RoBERTa, spelling-pretrained embedding initialization, masked-subword targets; retain the bounded null, <0.01 loss separation after 1,000 updates in the reported run. |
| [BIP-0164](../02_inventory/DETAILED_INVENTORY.md#BIP-0164), evidence; inspected line 7132 | “Full tables, stochastic policy evaluation and convergence proof not read” | [R09/BIW-0078](../03_reading/R09/BIW-0078.md), lines 3, 13–27; Table 1/3, Appendices A/D.1 | Attribute the completed table evidence and policy-evaluation uncertainty separately. Do not convert source reading into proof certification; actual deterministic-versus-sampled evaluation remains unclear. |
| [BIP-0261](../02_inventory/DETAILED_INVENTORY.md#BIP-0261), learning/evidence/limits; inspected lines 11340–11342 | Output realization unknown; causal details uninspected; dictionary/open-vocabulary mechanism “need full read,” abstract/A depth | [R10/BIW-0127](../03_reading/R10/BIW-0127.md), lines 7–16, 20–24; §§3.1–3.2/Algorithms 1–5 | State rule-split complete units, multilabel feature BCE and finite-candidate dictionary output in the primary fields. Keep exact byte/Unicode handling and unfinished-unit continuation unverified; remove the already-satisfied full-read request. |

**Repair pattern:** Keep **one active canonical field set per record**. Move superseded discovery fields into the existing historical disclosure, or replace their values with the completed card-attributed finding. “Not independently reverified by this reviewer” is permissible; it is not equivalent to “unknown,” “not read in the carrying source,” or “needs FULL.” No whole-source FULL counter should change.

**Closure criterion:** Extract the first active units/learning/evidence/limits fields without reading later prose; they should agree with the record's declared support, carrying card and latest correction. Repeat this sweep for the other newly upgraded R09/R10 records; the table is a demonstrated set, not an exhaustive stale-string census.

## 4. A consequential observation closed during review

The initially inspected BIP-0124 active finding repeated the R10 card's categorical claim that a positive Llama DI sentence contradicted negative TP. [CLAIM_RULES §7](CLAIM_RULES.md#7-new-r10-clarification-do-not-manufacture-a-dialect-tp-prose-contradiction) withdraws that certainty: the original §5.2 first says Llama TP is negative, then discusses IP before the positive sentence.

The retained original text, lines 279–289, supports that referent qualification. **The final recheck finds the BIP-0124 active text and final R2 adoption now corrected.** CLASSIFICATION_EN §4.11 also preserves the qualification. This is not an outstanding P1 against the current inventory. The original card's earlier wording remains historical evidence, not authority over the later correction.

Correct reusable result: DI TP correlations are **+0.638 Phi, +0.4836 mBERT, −0.380 Llama**; Llama DI IP is **+0.268**. Attribute each coefficient to its metric; do not manufacture a definite TP contradiction, significance, causal fairness effect or Unicode-corruption measurement.

## 5. Card-backed semantic spot checks

The following table enumerates **60 distinct card-backed BIP records**. The grouped cells are source-sharing conveniences; every listed BIP was checked for its separate problem/solution/technique object. Four additional normative/targeted checks follow. “Pass” means faithful at the stated card/correction scope, not a reproduced result.

| BIP records / families touched | Problem → one-sentence response; actual techniques and roles | Evidence card and carrying location | Audit result / condition |
|---|---|---|---|
| 0003 · C01/C07 | Large/excluding Unicode lookup → concatenate multiple hash embeddings; learned buckets provide finite-table coverage | [CANINE](../03_reading/R01/BIW-0004.md), §3.1, lines 7–10 | Pass: code points, not UTF-8 bytes; collisions and task heads retained. |
| 0006 · C02/C03/C08 | Rigid segmentation/expensive byte encoding → mix scored candidate-width means before fixed reduction; linear scores, softmax and denoising gradients | [Charformer](../03_reading/R01/BIW-0005.md), §2.1, lines 7–15 | Pass: soft per-position preferences are not an exact sampled partition; source-full encoder. |
| 0007, 0153, 0154 · C02/C03/C08 | Hard frontiers → Gaussian cumulative-membership approximation; lost order → depthwise CNN/max composition; all-byte degeneration → L/4 bottleneck | [MANTa](../03_reading/R01/BIW-0006.md), §3.1/§6.1/Appendix D, lines 7–15 | Pass: three genuinely different mechanism/negative subfindings, one source; not three independent effects. |
| 0013, 0014, 0015, 0284 · C04/C05/C06/C07/C11/C12 | Cost → global/local hierarchy; visibility → separate patch/byte shifts; dependence → local AR; sharing → reuse local embedding in output | [MEGABYTE](../03_reading/R03/BIW-0008.md), §2.2 Eqs.2–6/§2.4, lines 9–18 | Pass: concatenation, dependent joint and paper-level local tying are distinct objects; no runtime alias certification. |
| 0050 · C04/C12 | Parameter efficiency mistaken for compute efficiency → fit both frontiers, retaining recipe changes | [W0356](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md), §2.2/Fig.1/Appendices A–C; current inventory correction | P1-01: short technique field should explicitly name the 3:1 hybrid; same-FLOP subword win is preserved. |
| 0074 · C10/C12 | Expensive tokenizer selection/unreliable compression proxy → small/large comparison and pairwise ranking; logistic/SVM/Platt/Bradley–Terry have actual analysis roles | [Beyond Text Compression](../03_reading/R08/BIW-0049.md), §5/Tables 3/5/6, lines 7–17 | Pass: no pure-byte arm; translation rank transfer does not imply reliable ranking on every task. |
| 0081, 0082 · C02/C04/C08/C12 | Weak symbol-conditioned transition → factored multiplicative RNN; difficult optimization → Hessian-free/Gauss–Newton/structural damping | [Generating Text with RNNs](../03_reading/R02/BIW-0052.md), §§2–3.3/5.2, lines 7–18 | Pass: restricted transformed-character alphabet; PAQ negative retained; not byte-LM evidence. |
| 0085, 0126 · C01/C02/C07 | Rare-word statistical isolation → character CNN/max features; poor ordinary MLP transform → gated highway carry/transform | [Character-Aware LM](../03_reading/R02/BIW-0055.md), Model/Fig.1/Table 7, lines 7–17 | Pass: word-position LSTM and fixed word output; 84.6/78.9/92.6 large-PTB PPL comparisons keep their proper arms. |
| 0102, 0139 · C01/C07/C10/C12 | Possibly unnecessary learned byte table → fixed one-hot maps; apparent gain → decoder-token-dropout control | [Embeddingless NMT](../03_reading/R01/BIW-0068.md), §§2–3/6, Tables 2–4, lines 7–18 | Pass: byte translation and direct coordinates, but softmax_d/special handling unresolved; post-control reversal prevents unconditional benefit. |
| 0103, 0104 · C04/C05/C06 | Pooling visibility → extra k−1 shift on all operands; shortened-path restriction → fine-resolution attention plus causal residual | [Hourglass](../03_reading/R03/BIW-0072.md), §2.2/Appendix A.1–A.2; [CLAIM_RULES §6](CLAIM_RULES.md#6-hourglass-restrict-the-independence-claim-to-the-information-path) | Pass with current correction: previous symbol survives shifted residual; no blanket within-group independence. |
| 0109 · C11 | Canonical token-path score omits alternatives → estimate compatible-path sum; importance sampling/tokenizer proposal | [Marginal likelihood](../03_reading/R04/BIW-0080.md), §§2–4, lines 7–16 | Pass: finite-sample log estimator/support qualifications retained; not a native-byte architecture. |
| 0111 · C01/C11 | Mid-token prefix differs from canonical-token condition → sum valid prefix covers; token-to-byte probability conversion | [Exact Byte Probabilities](../03_reading/R04/BIW-0088.md), §4/Appendix A, lines 7–11 | Pass: exactness belongs to compatible canonical-support/corrected process; renormalization is not original neural-law preservation. |
| 0124 · C10/C12 | One fragmentation rank hides task dependence → separate TP/IP/task/adaptation; Pearson and quantized LoRA are actual methods | [Dialect study](../03_reading/R10/BIW-0134.md), §§3–5/Table 8, plus latest CLAIM_RULES §7 | Pass after concurrent repair: metric referent, correlations and unequal tuning permissions remain explicit. |
| 0129, 0130, 0131 · C01/C06/C10 | Language-specific pipeline → raw-byte annotation; huge triple classifier → serial start/length/label; local/edge failures → byte dropout/overlap | [Multilingual Processing from Bytes](../03_reading/R02/BIW-0057.md), §§3–5/Tables 3–4, lines 7–20 | Pass: annotation events, not generated text bytes; recurrent read/write sharing is not lexical tying. |
| 0136, 0137 · C01/C02/C12 | WordPiece fragmentation → local byte CNN/highway at word positions; open inputs → temporary top-100K word MLM head | [CharacterBERT](../03_reading/R01/BIW-0066.md), §§3.1–3.2, lines 7–15 | Pass: external words, local cap and excluded rare-word masking retained; not raw-stream byte generation. |
| 0149 · C03 | Lexical discovery disconnected from language use → semi-Markov marginalization, spelling/lexicon mixture and length penalty; optional VGG19 grounding | [Segmental Neural LM](../03_reading/R03/BIW-0042.md), §§2–4/Appendix F, lines 9–23 | Pass: latent likelihood, full-sentence MAP and union-of-splits segmentation F1 distinguished; character filtering/image budget retained. |
| 0164, 0165 · C08 | Surrogate boundary derivative → score-function policy gradient; excessive variance → early-exit baseline/discounting/rate pressure | [REINFORCE tokenizer](../03_reading/R09/BIW-0078.md), §§2.2–2.7/Appendix A, lines 7–27 | Mechanisms pass; P1-02 stale evidence ceiling remains. Discounting adds bias; ideal identity is not implemented-estimator certification. |
| 0166, 0167 · C05 | Masked decoder can still leak → random-symbol test; leak removal may harm prediction horizon → compare padding/overlap/masks/local LSTM | [Patching Leaks](../03_reading/R03/BIW-0074.md), Tables 1–3, lines 9–20 | Pass: independent 100-symbol diagnostic is separated from UTF-8 translation; leak-free failed padding retained. |
| 0171, 0172, 0173 · C06/C12 | Independent drafts incoherent → circuits; arbitrary start → overlapping discounted windows; larger draft costly → structure/rank/LoRA trade-off | [MtPC](../03_reading/R05/BIW-0079.md), §3/Appendices B–C/F/Table 1; CLAIM_RULES §3 | Pass with explicit boundary: circuit normalization/composite objective/throughput do not close optimized Algorithm 2 stochastic exactness. |
| 0184 · C07 | Duplicate word representations → hard input/output table sharing | [Press/Wolf](../03_reading/R08/BIW-0035.md), §§2–4/Table 5, lines 7–20 | Pass: word/BPE evidence only; not a controlled 256-byte tying benefit. |
| 0187, 0188, 0189 · C07 | One-hot target → embedding-derived KL; duplicated classifier span → reuse; conflated causes → AL/RE/REAL factorial arms | [Inan et al.](../03_reading/R08/BIW-0036.md), §§3–6/Appendix A, lines 9–29 | Pass: theorem's conditional shared subspace is not exact table equality; reuse is a separate imposed constraint. |
| 0206, 0207, 0208 · C07/C09 | Static imitation mismatch → four-layer functional alignment; rank restriction → sufficient local width; destructive start → frozen-interface stage then full updates | [Bolmo](../03_reading/R06/BIW-0097.md), §3.2.1/§6.2/Appendix E, lines 9–26 | Pass: retained suffix table makes parameterization hybrid; stage-two-only control is not catastrophic. |
| 0221 · C03 | Unequal encoding allocation → externally induced Morfessor/codebook and span denoising | [MYTE](../03_reading/R07/BIW-0104.md), §§3–5/Appendices A–C; CLAIM_RULES §5 | Pass with correction: learned code bytes ≠ UTF-8; MyT5 LR/overall 21.1/21.8 versus ByT5 21.9/23.1, not the card's transposed ordering. |
| 0228 · C10 | Character access still brittle → mean-character invariance or mixed-noise CNN training | [Noise NMT](../03_reading/R07/BIW-0109.md), §6/Tables 6–7, lines 9–24 | Pass: noise-type training mixture is not inference model ensemble; character/word/subword arms not native-byte results. |
| 0229, 0230 · C08/C10 | Unknown recoverable spelling → external probe; assumed utility → spelling-initialization intervention | [SpellingBee](../03_reading/R10/BIW-0110.md), §§2–5/Table 1/Fig.2, lines 7–21 | Distinct questions pass; P1-02 concerns stale fields and the reused probe tuple, not the genuine null intervention. |
| 0238 · C04 | Fragmented/recomputed context → stopped-gradient segment memories and relative position | [Transformer-XL](../03_reading/R09/BIW-0119.md), §§3.1–3.3/Tables 2/9, lines 7–17 | P1-02 active fields lag card; 1,874× comparison is uncached evaluation, not modern serving. |
| 0247, 0249 · C02/C09 | Bad static geometry → cosine/L2/neighborhood/identity terms; contextual incompatibility → frozen-host MLM and re-approximation | [Char2Subword](../03_reading/R06/BIW-0122.md), §§3.1–3.2, lines 9–24 | Pass: “representation distillation” remains labeled analogy, actual losses named; character antecedent, not byte decoder. |
| 0261 · C02 | Large/biased lexical tables → sparse trigram hashes, summed rows and candidate scoring | [T-FREE](../03_reading/R10/BIW-0127.md), §§3.1–3.2/Algorithms 1–5, lines 7–24 | Current mechanism passes; P1-02 active output/depth fields lag. Noninjectivity example remains analyst reasoning, not measured collision rate. |
| 0287, 0288, 0289 · C03/C04/C08/C10/C12 | Fixed work → repeated within-byte transitions; discontinuous/unbounded halting → ponder/max/approximate derivative; uncertainty proxy → trace diagnostic | [ACT](../03_reading/FIELD_ADDENDUM/arxiv_1603.08983v6.md), §2.2/§3.5, lines 7–23 | Pass: repeated computation is not segmentation; byte errors are training-set-only; traces are not a validated utility oracle. |
| 0290, 0291, 0292 · C04/C05/C07/C08/C12 | Attention cost → LSH; depth activations → reversible streams; FFN peak → position execution chunks | [Reformer](../03_reading/FIELD_ADDENDUM/arxiv_2001.04451v2.md), §§2–3/Appendix A, lines 11–27 | Pass: three distinct resource objects; Q/K sharing ≠ lexical tying; no inference-KV elimination claim. |
| 0293, 0294 · C02/C07/C09/C10 | Static word context → contextual layer mixture; duplicate directional lexical interfaces → share representation/softmax across directions | [ELMo narrow card](../03_reading/FIELD_ADDENDUM/arxiv_1802.05365v2.md), §§3.1–3.4, lines 3–19 | Pass within designated PARTIAL: words are the clock/output; directional sharing ≠ input/output equality. |
| 0295, 0296 · C01/C03/C11 | Large/incomplete alphabet → byte-base BPE; redundant word-punctuation entries → category/space merge constraints | [GPT-2 narrow card](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md), report p.4 §§2.2–2.3, lines 3–19 | Pass within designated PARTIAL: 50,257 merged outputs/1,024 model tokens, not 256-way byte prediction or byte context. |

### Four additional boundary checks

| Record | Evidence inspected | Result |
|---|---|---|
| [BIP-0112](../02_inventory/DETAILED_INVENTORY.md#BIP-0112) | [BIW-0090 catalog](../02_inventory/WORK_CATALOG.md#BIW-0090), RFC 3629 §§3–4/selected security passages | Pass as normative instrument: octets/validation state/scalars/no learning. Legality is not intended-character or task correctness. No new original-standard read claimed. |
| [BIP-0217](../02_inventory/DETAILED_INVENTORY.md#BIP-0217) | [BIW-0116 catalog](../02_inventory/WORK_CATALOG.md#BIW-0116), UAX #29 rev.47 §§1–3/Table 1a mapping | Pass as versioned grapheme/offset instrument with tailoring, not empirical model performance. No full-annex credit. |
| [BIP-0218](../02_inventory/DETAILED_INVENTORY.md#BIP-0218) | [BIW-0115 catalog](../02_inventory/WORK_CATALOG.md#BIW-0115), UAX #15 rev.57 §§1.1–1.2 mapping | Pass: canonical/compatibility equivalence and original-byte preservation separated; deterministic normalization is explicitly non-AI. |
| [BIP-0286](../02_inventory/DETAILED_INVENTORY.md#BIP-0286) | Latest CLAIM_RULES §4 and active targeted correction | Pass as reviewer exception, not author solution: correct event/byte formula is reviewer accounting; actual Figure 6 transformation remains unknown. Ordinary option ranking/text control not invalidated. |

## 6. Required conceptual red-team tests

### 6.1 Does the schema really answer the user's three questions?

**For author-mechanism rows, generally yes at the sampled depth.** The sampled solutions identify operational changes: hash tables, explicit pooling operators, shifted operands, a named loss or learning schedule, an altered projection, an independent probe, or an output correction. This is materially more useful than a paper-title list with “use deep learning” in every technique column.

However, the 296 records deliberately contain different types. BIP-0284 is a sharing specification; BIP-0286 is an analyst's unresolved metric exception; BIP-0112/0217/0218 are normative instruments; BIP-0289 is a diagnostic. They must not be advertised as four or five researcher-solved scientific problems merely because their fields are headed “problem” and “solution.” The current record boundaries and classification prose mostly make this clear.

For table exports, preserve a compact **record type and agent of action**: author mechanism, author evaluation/control, specification, normative instrument, or reviewer exception. In BIP-0286 the field title “Researcher-used techniques” contains reviewer accounting, but the immediately following attribution explicitly says so. I therefore do **not** count this as a demonstrated author-usage fabrication. A role-aware export should carry that attribution or use “reviewer recommendation” rather than detach the formula from its qualifier.

The two P1 findings address the places where extracting those otherwise useful short fields would still lose or contradict actual mechanisms/evidence.

### 6.2 Method analogy versus actual usage

No demonstrated analogy-to-implementation promotion was found in the sample:

- Char2Subword actually uses cosine/L2/neighborhood/identity losses; “representation distillation” is explicitly an analyst analogy, not an extra teacher-logit module.
- T-FREE actually uses regex splitting, trigram features and candidate scoring. The repeated-trigram counterexample is labeled analyst reasoning, not observed software failure or an author-added mechanism.
- MtPC actually uses circuits and draft adaptation. The discarded-correction toy argument is an analyst qualification, not a measured code bug.
- Reformer actually reconstructs activations and chunks execution. Neither is called learned semantic segmentation or an encoder/decoder tied inverse.
- ACT actually learns repeated work within bytes. A family relationship to later utility-based boundaries is not attributed as an author boundary detector or a genealogical borrowing claim.

The broad-field placement of PCGrad/VAE/vision merging in CLASSIFICATION_EN is explicitly adjacent/background. This review did not freshly verify those originals and does not turn their inclusion into evidence that any particular byte researcher implemented them.

### 6.3 Synonymous inflation versus useful subfindings

No current headline claims 296 distinct scientific problems. DETAILED_INVENTORY's opening, TAXONOMY, COUNTS and both synthesis files repeatedly distinguish parent questions from source-specific records. Reuse of one card paragraph is explicitly denied evidential independence.

The sampled multirow sources have substantive distinctions:

- MANTa: differentiable membership, order-sensitive content and compression-pressure failure are not synonyms.
- MEGABYTE: allocation, temporal legality, dependent output and a tying specification are different technical objects, but not four independent architecture wins.
- Inan et al.: auxiliary soft supervision, reuse/theory and factorial attribution deserve separate rows under a common parent.
- SpellingBee: probe decodability and a null initialization intervention answer different questions.
- Reformer: attention interactions, depth-dependent activation storage and FFN intermediates are genuinely distinct resource problems.
- ACT: mechanism, halting optimization and effort/uncertainty diagnostic share one parent, not three successful byte-quality experiments.
- BIP-0284/0285/0286 and ELMo's sharing record are specifications/review exceptions, not additional solved problems.

No renumbering, forced one-paper/one-row merge, or invented exhaustive count of semantic parent problems is warranted. Consolidate exposition while retaining subfinding IDs and evidence dependence.

### 6.4 Unit/source-kind pooling

The sampled classifications and syntheses pass the requested separation test:

| Evidence kind | Checked examples | Permitted contribution, not pooled conclusion |
|---|---|---|
| Native byte causal interfaces | MEGABYTE; ACT's Wikipedia task; enwik8 Transformer-XL arm | Mechanisms/likelihood under each source's actual exposure, scoring and task regime |
| Byte encoders/seq2seq | MANTa; embeddingless NMT; byte annotation | Conditional restoration, translation or annotation, not unconditional native-byte LM performance |
| Code-point interface | CANINE | Hash coverage/task encoding, not UTF-8 next-byte generation |
| Character antecedents | 2011 multiplicative RNN; Character-Aware LM; segmental LM | Historical composition, optimization and lexical discovery, not raw-byte evidence |
| Word/subword/probe output | CharacterBERT; ELMo; SpellingBee | Open input, frozen transfer or probe information, not unrestricted byte output |
| Byte-complete merged symbols | GPT-2 | BPE coverage/history, not one prediction per byte |
| Hybrid / alternative code | Bolmo; T-FREE; MYTE | Explicit inherited lexical tables, candidate units or morphology codes, not a pure-byte common frontier |
| Standards / reviewer analysis | RFC/UAX; TokSuite metric exception | Definitions/accounting boundaries, not paper experiments or empirically achieved remedies |

“Pure” is not a single safe aggregate label: byte-only deployment, byte-only parameterization, teacher-free training and next-byte probability are different properties. The four-unit tuple and teacher/pipeline fields are the right basis for comparisons. Nothing here licenses summing source kinds as byte-model successes or comparing unrelated PPL/BPB/accuracy values as one leaderboard.

## 7. Release recommendation and verification

1. **Do not commission another broad reading batch to repair these findings.** The necessary carrying evidence already exists; zero new FULL credits arise from this review.
2. Before releasing/exporting the detailed inventory, repair P1-01 and P1-02 in the responsible owner's files, preserving existing IDs, depth distinctions and source mappings. This reviewer has not performed those edits.
3. Retain the now-adopted dialect referent correction; MYTE's corrected aggregate ordering; Hourglass's residual qualification; MtPC's open optimized-wrapper guarantee; and TokSuite's unknown Figure 6 computation. These are different issues with different evidence, not one global paper-validity verdict.
4. Keep the valid overlapping taxonomy and disjoint home-route map. Preserve record type and analyst attribution in any downstream table/translation, rather than deleting substantive diagnostics or relabeling every row an author solution.

**Verification performed:** in-memory Python extraction/reconciliation on the saved Markdown, direct card reads at the locations tabulated above, and final source rechecks after observing concurrent inventory updates. The structural checks passed: 296 sequential records, 141 entities, 140 contributing entities, 506 family memberships, 296 unique home assignments, consistent tag maps, and 423 historical keys/496 edges plus ten field keys/edges. The saved review's validation passed: 32 card-source groups enumerate exactly 60 distinct records, all 62 local link targets exist, Markdown table widths agree, UTF-8 has no replacement characters, and no trailing whitespace was found. Final inventory checks confirmed both P1 examples remain and the dialect referent correction is adopted. `git diff --check -- docs/research/byte_language_interface_survey/05_review/INVENTORY_CLASSIFICATION_REVIEW.md` exited 0; because this survey is untracked, direct saved-file validation is the substantive check. Targeted Git status shows the intended review as one new file. These checks test documentary structure, not original results or implementations.

No application build or pytest was run because this is a Markdown-only review with no production changes. No temporary helper, dependency, source download or test output was created by this reviewer. Only `05_review/INVENTORY_CLASSIFICATION_REVIEW.md` was written; proposed repairs remain explicit follow-up, not silently completed work.
