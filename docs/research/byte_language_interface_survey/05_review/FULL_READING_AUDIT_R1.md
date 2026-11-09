# Independent full-reading evidence audit — R1

2026-11-09. Independent review, not synthesis and not a replacement for terra's selected-paper reading.

## 0. Scope, counts and decision

I read [PLAN](../PLAN.md), [DISCOVERY_CORRECTIONS](DISCOVERY_CORRECTIONS.md), all eight R01–R08 batch summaries, and **16 complete current reading cards: exactly two per batch**. I then checked selected original passages from **17 distinct papers**: the 16 sampled works plus TokSuite. Fourteen sampled papers were checked through their retained primary-source text extracts; the two R03 papers were checked through versioned public arXiv HTML because R03 had removed its local sources. TokSuite was an additional public-HTML check of model/training/evaluation definitions, **not a fresh verification of Appendix C.2 or Figure 6**. Selected stored page images were read for MYTE, XTREME-UP and LCA-MBP; opening the small overview contact sheet does not count as reading all papers pictured in it.

**New FULL papers credited by this reviewer: 0.** This is a targeted audit of terra's evidence, not seventeen independent full rereadings. The nine original papers and three code files reported in DISCOVERY_CORRECTIONS are that document's work, not additional sources independently audited here. No paper repositories, model weights, runtime aliases, generation experiments or figure pipelines were executed or authenticated.

**Decision:** the sampled cards generally carry substantive methods, evidence, negative results and relevant appendix material rather than abstract-only summaries. Two concrete card-level statements need correction (§2). A higher-priority, newly identified **sampling-contract concern** in the probabilistic-circuit paper needs to be added to its card (§4.1); it is not an established failure of released software. Several reported table/prose conflicts are real printed disagreements, but some apparent conflicts are denominator or experiment-scope differences (§3). None justifies globally invalidating a mechanism or rescinding FULL merely because an author omitted implementation details.

Classification throughout:

- **Confirmed correction:** an incorrect card statement or demonstrable overstatement, with a specific replacement.
- **Source disagreement / suspicion:** a printed inconsistency or conditional technical concern; the true run, intended specification or empirical consequence is unresolved.
- **Not reported / not verified:** absent information or a boundary of this review, not evidence of a negative value or a failed method.

Line numbers below refer to the cards as read in this audit; section and quoted-phrase locators remain usable if concurrent editing moves lines. Proposed edits are **not applied** to those cards or to the shared inventory.

## 1. Balanced sample and source-reading ledger

In the following table, “FULL-content check” means whether the card actually contains the material required for the survey's key interpretation. It does not certify another reader's historical actions or independently reproduce every plot/table. All sixteen cards were read from beginning to end. The original-source checks were limited to the stated passages.

| Batch / sampled card | Primary material actually checked in this review | FULL-content check and safe interpretation |
|---|---|---|
| R01 [BIW-0004, CANINE](../03_reading/R01/BIW-0004.md) | [v4 text](../03_reading/R01/sources/BIW-0004.txt), Table 2 extraction and caption, §4.1–4.2, Table 7 extraction; original [2103.06874v4](https://arxiv.org/pdf/2103.06874v4). Table extraction is interleaved, so this review does not independently recertify each Table 2 cell. | Contains codepoints, C versus S supervision, stride, task readout, throughput, negative NER results and appendix deltas. The distinction between +2.8 SELECTP and +5.7 MINSPAN is essential and present. No byte-generation inference. |
| R01 [BIW-0005, Charformer](../03_reading/R01/BIW-0005.md) | [v3 text](../03_reading/R01/sources/BIW-0005.txt), §2.1.2–2.2, §3 footnote 5, §4.1, Table 1, multilingual calibration statement and §7.4 loop. Original [2106.12672v3](https://arxiv.org/pdf/2106.12672v3). | Contains soft candidate mixtures, fixed final pooling, full-source calibration visibility, actual byte/sentinel convention, scaled architecture and non-wins. Appendix illustrative-loop discrepancy is explicitly scoped; actual training code is not certified. |
| R02 [BIW-0058, ByteNet](../03_reading/R02/BIW-0058.md) | [v2 text](../03_reading/R02/BIW-0058.txt), abstract, §§5–6 and Tables 2–4, original [1610.10099v2](https://arxiv.org/pdf/1610.10099v2). | Contains restricted Wiki byte alphabet versus MT characters, masked target/unmasked source distinction, receptive field, EOS and conflicting metrics. No relevant appendix is claimed. Retain theoretical linear complexity separately from measured serving speed. |
| R02 [BIW-0057, Bytes-to-Spans](../03_reading/R02/BIW-0057.md) | [v2 text](../03_reading/R02/BIW-0057.txt), Figure 1 caption, §3–5, recurrent-sharing passage and vocabulary/invalid-output paragraphs; original [1512.00103v2](https://arxiv.org/pdf/1512.00103v2). | Contains UTF-8 input, annotation-event output, whole-window visibility, shared recurrent parameters, DROP and overlapping windows, task/language negatives. It does not turn recurrent sharing into embedding/readout tying. |
| R03 [BIW-0008, MEGABYTE](../03_reading/R03/BIW-0008.md) | Public [2305.07185v2 HTML](https://arxiv.org/html/2305.07185v2), §2.2 Eqs. 2–6, §2.3–3, §4.1, Tables 2–3/6–8 and adjacent interpretation. No fresh Appendix D rereading here. | Contains both shifts, within-patch autoregression, explicit local tying, equal-byte/approximately equal-forward-time protocol and 1×/2×/4× scoring. Million-byte language claims are correctly excluded. The retained Appendix D negative is a card-level item, not freshly recertified here. |
| R03 [BIW-0072, Hourglass](../03_reading/R03/BIW-0072.md) | Public [2110.13711v2 HTML](https://arxiv.org/html/2110.13711v2), §2/Algorithm 1, §3.3, Tables 1–2/4–8, Appendices A–D. | Contains extra shift, pooling operands, full-resolution path, overlapping evaluation and hardware/repeats. **Correct the blanket independence sentence using the residual explicitly retained in A.1 (§2.2 below).** |
| R04 [BIW-0088, Exact Byte Probabilities](../03_reading/R04/BIW-0088.md) | [v2 text](../03_reading/R04/sources/BIW-0088.txt), §2.1–3.2.2, §4.1.1, Algorithm 3 extraction and source references to invalid-encoding support; original [2410.09303v2](https://arxiv.org/pdf/2410.09303v2). | Contains prefix covers, canonical support, noncanonical neural mass, mask/renormalize distribution change, EOS qualification, model-call versus system cost and comparator-specific gains. The formal-version wall is honestly separate from locked-v2 FULL. No independent theorem certification. |
| R04 [BIW-0083, Speculative Decoding](../03_reading/R04/BIW-0083.md) | [official-paper text](../03_reading/R04/sources/BIW-0083.txt), §2.2–3.4, Algorithm 1 and overlap/runtime assumptions; [official PDF](https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf). | Contains adjusted p/q, rejection residual, bonus token, exact-law versus identical samples, i.i.d. efficiency assumption and non-byte timings. Preserve the distinction between correctness assumptions and the extra assumptions used only for a speed estimate. |
| R05 [BIW-0015, LCA-MBP](../03_reading/R05/BIW-0015.md) | [v2 text](../03_reading/R05/sources/BIW-0015.txt), §3/Algorithm 1, shared output matrix, Table 1, Appendix B Tables 3–5 and adjacent cache/prose statements. Original [2608.15454v2](https://arxiv.org/pdf/2608.15454v2). Appendix p.13 checked at readable resolution in the [stored contact sheet](../03_reading/R05/sources/key-pages.jpg). | Contains tensor/target shifts, duplicated past-segment inputs, absence of conditioning on sampled peers, threshold versus self/external verification, explicit readout sharing, uncached condition and candidate-count negative. The printed 78–84% disagreement is real (§3). |
| R05 [BIW-0079, probabilistic circuits](../03_reading/R05/BIW-0079.md) | [v2 text](../03_reading/R05/sources/BIW-0079.txt), main Table 1/metrics, EOS limitation, Appendix B normalization, C head cost and F Algorithms 2–3 plus cache rationale. Original [2511.11346v2](https://arxiv.org/pdf/2511.11346v2). | Contains normalized joint rather than independent offsets, distinct sharing axes, head size, acceptance/throughput counterexamples and EOS suppression. **Add the residual-versus-bonus issue in §4.1 before treating the optimized cached algorithm as exact.** |
| R06 [BIW-0099, Cross-Tokenizer Distillation](../03_reading/R06/BIW-0099.md) | [v1 text](../03_reading/R06/sources/BIW-0099.txt), §3.1 footnote, Figure 1 removal statement, §4 training setup, Appendix B Table 4, C cost/reference settings. Original [2604.07466v1](https://arxiv.org/pdf/2604.07466v1). | Contains removable training interface versus actual byte deployment arm, parallel heads versus byte conditionals, pruned teacher approximation, conflicting LoRA/vocabulary descriptions and offline teacher cost. This is meaningful FULL content, not a claim of verified exact byte distillation. |
| R06 [BIW-0103, Breaking the Token Ceiling](../03_reading/R06/BIW-0103.md) | [v1 text](../03_reading/R06/sources/BIW-0103.txt), §2.2 marked sequence/example, Tables 1/3/5–7, Appendix E Table 22–23 and F.1 code. Original [2609.12303v1](https://arxiv.org/pdf/2609.12303v1). | Contains marked versus unmarked events, hidden teacher cost, observed versus extrapolated quality and appendix implementation ambiguity. “Exact for marked history” is the right bounded interpretation. This review did not redo all scaling fits or visually recertify Table 21's individual cells. |
| R07 [BIW-0104, MYTE](../03_reading/R07/BIW-0104.md) | [v2 text](../03_reading/R07/sources/BIW-0104.txt), §3.2, §5.1–5.3/Eq.1, Appendix A normalization, B.3/C.2 and Tables 4/8. Stored [p.15](../03_reading/R07/sources/BIW-0104-p15.png), [p.16](../03_reading/R07/sources/BIW-0104-p16.png), [p.17](../03_reading/R07/sources/BIW-0104-p17.png) read; p.17 resolves column order. Original [2403.10691v2](https://arxiv.org/pdf/2403.10691v2). | Contains codebook/resource dependence, normalization uncertainty, unseen-script negative, English-byte denominator and downstream losses. **The two Table 8 aggregate columns are transposed in the card (§2.1).** Missing minus sign is not proof that the experiments computed negative surprisal. |
| R07 [BIW-0105, XTREME-UP](../03_reading/R07/BIW-0105.md) | [v2 text](../03_reading/R07/sources/BIW-0105.txt), §3.2–3.3/Table 1 and footnote 8; [stored p.3](../03_reading/R07/sources/BIW-0105-p3.png) visually checked for benchmark headings. Original [2305.11938v2](https://arxiv.org/pdf/2305.11938v2). | Contains scarce-data rather than zero-shot design, upstream ASR/OCR resources, per-task averages versus 88-language scope, preliminary autocomplete negatives and normalization. Keep benchmark population, baseline subset and pre-subsampling data-card sizes distinct. |
| R08 [BIW-0108, Byte-level Simulation](../03_reading/R08/BIW-0108.md) | [v2 text](../03_reading/R08/sources/BIW-0108.txt), §4.2 and §5 experimental setup/throughput/boundaries, especially §5.2–5.3. Original [2604.27263v2](https://arxiv.org/pdf/2604.27263v2). | Contains offline labels, missing prefix-consistency proof, changed target density, withdrawal evaluation and fixed-backbone costs. Its generic causality caution is warranted; this review does not establish a concrete leakage rate for the actual Llama tokenizer. |
| R08 [BIW-0049, Beyond Text Compression](../03_reading/R08/BIW-0049.md) | [official-paper text](../03_reading/R08/sources/BIW-0049.txt), §2.2/Table 1, Appendix A Tables 7–10 and tying entry, Table 3 extraction; [official PDF](https://aclanthology.org/2025.acl-long.1546.pdf). | Contains same text subset versus tokenizer-specific token counts, unequal total parameters, actual tied-table specification, task-dependent ranks, model-token speed and ambiguous TFLOPs. Printed 2050/1540 h disagreement is not evidence of a mechanism failure. |

**Seventeenth primary source:** public [TokSuite v2](https://arxiv.org/html/2512.20757v2), especially §3.2–3.3, §4.3 and §7: untied embeddings, common initialization rather than shared trained parameters, unequal raw-byte exposure at equal tokens, byte-length-normalized option likelihood and acknowledged entangled tokenizer factors. HTML pagination hit a scan limit before C.2; no new Appendix C.2/PDF/plotting-code check is claimed. The previous C.2 finding and its fixed-code provenance remain attributed to DISCOVERY_CORRECTIONS §5.

## 2. Confirmed corrections to current cards

### 2.1 MYTE: LR and overall MT means are reversed in the card

**Edit location:** [R07/BIW-0104.md](../03_reading/R07/BIW-0104.md), line 20, Results/controls fourth bullet; phrase `average LR/overall MT 21.8/21.1 ... 23.1/21.9`. Also clarify its last language-list clause.

**Direct evidence:** Table 8 on original PDF p.17 / stored `BIW-0104-p17.png` has headers **AVG LR, AVG**, in that order. MyT5 is **21.1, 21.8**; ByT5 is **21.9, 23.1**. The text extraction's table header has the same order. This is a card transcription error, not an uncertain model result. Correcting it does **not** remove the disagreement with main Table 4: the latter's low-resource MT summary is ByT5 20.1, MyT5 20.4.

**Usable replacement:**

> Appendix B Table 8 reports low-resource/overall MT means of 21.1/21.8 for MyT5 and 21.9/23.1 for ByT5. Both favor ByT5, unlike main Table 4's low-resource summary (20.4 versus 20.1 in favor of MyT5). The paper does not identify a subset or aggregation change that reconciles these summaries. Table 8 also includes Maltese (`mt`) and Shona (`sn`), whereas C.2 names Marathi and omits Shona; C.2 lists fourteen language names, against fifteen language columns in Table 8. Treat the actual evaluated set and reconciliation as unresolved.

The aggregate discrepancy is a **source-reporting question**. Do not choose a preferred sign for the survey, silently average the two tables, or conclude that transcoding cannot work. If an MT numeric summary is necessary before clarification, state which table and population label it uses.

### 2.2 Hourglass: blanket within-group independence ignores its shifted input residual

**Edit location:** [R03/BIW-0072.md](../03_reading/R03/BIW-0072.md), line 13, sentence beginning `With no full-resolution Transformer layer ...`.

The card closely follows main §2.2's simplified factorization, but **Appendix A.1 explicitly retains the one-step-shifted input embeddings through the residual**. Table 9 and its explanation say prediction can use both shortened embeddings and the embedding of the immediately previous input symbol. Consequently, absence of a fine-resolution Transformer layer does not by itself make every position independent of all previous symbols in its group: the direct shifted embedding can transmit a dependence on the preceding symbol. What the appendix actually demonstrates is inability to solve its particular two-position-back copying construction, not complete absence of every within-group dependence.

**Usable replacement:**

> Without fine-resolution Transformer layers, the shortened branch lacks access to current-group history; the direct shifted-input residual can still convey the immediately previous symbol. Appendix A.1 shows a concrete copying dependency that this restricted access cannot express. A fine-resolution attention layer removes that restriction in the construction; this is not a guarantee of learned performance on arbitrary tasks.

The additional k−1 shift and visibility audit of pooling inputs remain valid design obligations. This correction refines an expressivity claim; it does not show that Hourglass leaks future targets or fails at causal generation.

## 3. Reader-reported conflicts: same estimand or different scope?

| Work / card location | What was independently checked | Audit classification and usable statement |
|---|---|---|
| CANINE, R01/0004:15 and R01 summary:20 | v4 §4.2 prints n-gram deltas +3.8/+6.9; Table 2/7 extractions carry +4.9/+5.7. +2.8 is CANINE-S SELECTP; +5.7 is C+n-grams MINSPAN. | **Two different issues.** +2.8 versus abstract +5.7 is an **arm/metric difference**, not a contradiction. The n-gram prose versus tabulated deltas is an actual printed disagreement. Keep the card's table-specific attribution and disclose the prose difference; no mechanism-failure claim. This review did not rerender Table 2. |
| Charformer, R01/0005:9 | §7.4 really loops over `range(1, self.max_subword_block_width)`; method describes 1≤b≤M. The same simplified listing explicitly omits calibration. | **Illustrative-code/specification discrepancy**, not certified experimental off-by-one bug. Use: “The paper specifies candidate widths through M; its simplified appendix listing has an exclusive upper bound. Actual training/configuration remains unverified.” |
| ByteNet, R02/0058:16 | Same v2 abstract reports BLEU 22.85/25.53 and bpc .380/.389; Tables 2/4 extraction gives 23.75/26.26 and .521/.532 on named 2014/2015 tests. | **Printed result disagreement with no stated reconciliation.** Character-versus-byte terminology is a separate unit problem and does not numerically reconcile two BLEU pairs. Quote versioned table results as table results, not the abstract's digits. No conclusion about convolutional mechanism validity follows. |
| LCA, R05/0015:17 | Appendix B p.13 Table 5 explicitly labels n=7 and self/external verification, with self 45.85–46.36%, external 47.97–52.04%. Nearby prose explicitly refers to Table 5 but says 78–84%. Table 4 is a different, n=3 setting. | **Real table/prose disagreement for the stated Table 5 context.** Candidate-count changes can explain Table 4 versus Table 5 differences; they do not repair the adjoining prose that expressly describes Table 5. Use table-specific rates with the discrepancy, not a blended range. Actual acceptance denominator/run provenance remains unverified. |
| Cross-tokenizer distillation, R06/0099:13 | §4 says rank-64 query/value updates with all other backbone weights frozen, and 260 byte classes; Table 4 lists Q/K/V/O/gate/up/down and 261 classes, with caption “all experiments.” | **Actual description disagreement**, not established different experiment scopes. The source does not name a scope split that resolves it. Preserve both specifications, label actual LoRA modules/vocabulary unknown, and do not infer that the distillation objective fails. |
| EOT pseudocode, R06/0103:11 | §2.2 explicitly inserts EOT into modeled sequences. Appendix F.1 changes output alphabet size with `use_eot`; the function consumes caller-supplied `token_to_bytes`, `lengths` and `gold`. | **Missing preprocessing contract, not demonstrated missing mechanism.** The function can represent EOT if those inputs already contain it; no append inside the function is required in that case. Use “EOT preprocessing is not shown in the listing” rather than “the implementation omits EOT.” |
| MYTE, R07/0104:19–20 | Eq.1 extraction lacks a minus sign; text calls the measure Bit-per-English-Byte and reports positive scores. Table 4/8 population labels and C.2 language list inspected as above. | Missing minus sign is a **notation/sign discrepancy**, with actual log base/scoring unresolved. Main versus appendix MT numbers remain **unreconciled**, even after fixing the card's column order. Overall versus LR means must not be compared as identical; the proper LR-to-LR comparison still differs. |
| XTREME-UP, R07/0105:15 | Table 1 is explicitly subsampled training data; §3.2 explains the annotation budget. §3.3 says 93 total languages, 39 UL evaluation and footnote 8 says baseline trained on 39 UL pairs. Table 1 shows 70 UL +23 HL. | **499 versus selected mean 120 training examples is a data-card/subsampling distinction**, not a contradiction. **93 total versus 39 baseline pairs is also a scope distinction.** 70 UL benchmark population versus prose's 39 UL evaluation is an unresolved release/baseline-scope mismatch; a subset is plausible but not documented sufficiently to assert which languages entered each final table. Do not claim the benchmark itself had only 39 languages or that 70 baseline evaluations are proven. |
| Tokenizer scaling, R08/0049:13 | Table 1 and Table 7 text extractions disagree on the tiktoken 2.7B-arm H100-hour entry, 2050 versus 1540. Both tables describe pretraining cost. | **Printed accounting disagreement**, not resolved by token/sec, model scale or fine-tuning epochs. State both values and omit an exact cost ranking dependent on this cell. TFLOPs without a clear operation denominator must not become total training FLOPs. A fresh visual table check was not performed here. |

The table intentionally separates **confirmed existence of inconsistent reporting** from the unknown answer to “which number or implementation generated the published result?” The latter requires an author clarification or fixed artifact/run audit.

## 4. Suspicions and qualification gaps needing action

### 4.1 Highest priority: MTPC cached Algorithm 2 may discard a required rejection correction

**Locations for addition:** [R05/BIW-0079.md](../03_reading/R05/BIW-0079.md), line 17 / BIP-0173; [R05/BATCH_SUMMARY](../03_reading/R05/BATCH_SUMMARY.md), line 21 source-issue list. Primary source [2511.11346v2](https://arxiv.org/pdf/2511.11346v2), Appendix F pp.19–21; retained text lines 1130–1178 and 1220–1240.

The existing card rightly requires actual transformed proposal conditionals, but its phrase “normally drops the bonus token” is **not enough to qualify Algorithm 2**. Appendix F says the optimized shared-state procedure sacrifices the last “free” token when any draft tokens were accepted. It points to Algorithm 3's final-token block, which includes **two different distributions**:

1. If all n proposals are accepted, the extra token is an ordinary bonus from the target.
2. If a proposal is rejected, the next token is drawn from the positive residual `(p−q)+`, normalized. That token supplies the correction needed for exactness.

Dropping an optional all-accepted bonus is not the same operation as dropping a rejection correction. The optimized pseudocode does not explicitly say that a residual distribution is retained across cycles, or separate “all accepted” from “some accepted then rejected.” A literal interpretation that discards the correction whenever at least one draft was accepted and then restarts sampling can be biased.

**Bounded algebraic diagnostic, not a reproduction:** take n=2. The first position is deterministic and accepted under identical target and draft. At the second position take `p=(0.5,0.5)` and `q=(0.9,0.1)`. Accepted proposal mass is `min(p,q)=(0.5,0.1)` and rejection mass is 0.4. Proper residual sampling adds `(0,0.4)` and recovers p. Discarding that residual and restarting from an ordinary fresh target-law cycle adds `0.4p=(0.2,0.2)`, producing `(0.7,0.3)` instead. A retained correction state or a different actual protocol could avoid this interpretation.

**Status:** the unsafe literal interpretation has a concrete counterexample. **Whether the paper's implementation actually does this is unknown.** This is a source-level algorithm-contract concern, not a verdict that measured software outputs are biased. The pseudocode may be incomplete or use overloaded acceptance variables. Greedy and stochastic modes must also be separated.

**Usable addition:**

> Algorithm 3 describes ordinary target-preserving residual correction. The optimized shared-state Algorithm 2 omits a final verifier token when proposals have been accepted, but the paper does not clearly distinguish an optional all-accepted bonus from a required post-rejection correction, or show retained residual state. Exact stochastic target-law preservation of this optimization is therefore unverified; a literal discard-and-restart reading need not preserve the law. This does not establish a bug in the released implementation or negate the measured throughput figures.

**Closure evidence requested of the existing reader/artifact owner:** fixed implementation/version and rejection branch; emitted/cached state after 0, 1…n−1 and n acceptances; any residual carry-over; actual transformed p/q; finite-prefix distribution argument for the optimized wrapper. No new training is needed. Do not launch a new full-reading batch just to relabel an already FULL card.

### 4.2 Exact byte conversion: termination and canonical support are separate assumptions

**Location:** R04/BIW-0088:8–10. §2.1 states positive EOS probability at every finite prefix and then calls sequences effectively finite. Positive hazards alone do not imply almost-sure termination: hazards can shrink so fast that survival has positive probability. The card already avoids certifying that implication. State almost-sure termination as an additional assumption for the completed-sequence/countability setup; do not infer that finite-prefix cover computations automatically fail.

§3.2.2 explicitly acknowledges positive noncanonical mass in trained softmax models and then assumes provably nonexistent encodings have zero probability. The card correctly carries this important qualification. This is not a new discovery of a hidden contradiction: masking and renormalizing deliberately changes the neural distribution while improving valid-path likelihood under the stated support. Do not say “exact raw-softmax detokenization for arbitrary tokenizers” without accounting for noncanonical paths, normalization and special symbols.

**Usable sentence:**

> The cover construction is exact for its stated lossless canonical-support process; applying support correction to a generic softmax LM changes that LM's distribution. Termination and tokenizer-compatibility assumptions should be stated separately from the finite-prefix identity.

### 4.3 Offline BPE starts are not automatically prefix-computable

**Location:** R08/BIW-0108:17–18; source §5.3 claims starts do not leak future bytes, while the setup obtains BPE annotations from complete sequences. The card's caution is justified, but must remain a conditional concern about the actual experiment, not an asserted measured leak.

A generic BPE example establishes why the inference needs proof: give merge `bc` higher priority than `ab`. Tokenizing `ab` can produce `[ab]`, whereas `abc` can produce `[a,bc]`; the start flag at `b` changes with future `c`. This is an analyst's toy counterexample to a universal property, **not a test of the actual Llama-3 tokenizer**. Repeated subword positions inherit the same concern. Byte-level causal masking does not erase side information already placed in inputs.

**Usable sentence:**

> The intervention uses offline subword-start annotations. Its deployment-time causality depends on prefix-stability of those annotations under the actual tokenizer, which the paper does not establish. Training-only withdrawal results remain a different claim and need not imply a causal online interface.

### 4.4 EOT: marked exactness does not establish unmarked marginal preservation

**Location:** R06/BIW-0103:9–11. Preserve the card's event distinction. Its source example reallocates token-termination mass to EOT; this is a coherent marked-history objective, not proof of an unmarked next-byte marginal after all hidden marker placements/token histories are integrated out. F.1 can be correct given pre-expanded caller inputs (§3); absence of that preprocessing in the listing is not a demonstrated runtime defect.

**Usable sentence:**

> EOT preserves the teacher's conditional mass in the explicitly marked sequence representation. It adds modeled boundary events and processing cost; removing or hiding the markers defines another probability question. The appendix function's caller-side EOT expansion remains unspecified in the listing, not proven absent from the implementation.

The reported four-point advantage remains an **extrapolation**, not a four-point observed matched-budget gain. Table 7's data/storage ratios and an extra marked sequence unit per teacher token are not a full accounting of teacher inference, pretraining, I/O or serving cost.

### 4.5 TokSuite BPB closure is still open, not independently reclosed here

**Adoption location:** DISCOVERY_CORRECTIONS §5, especially its central note; any future synthesis use of Figure 6 or the older W0518 FULL label. The prior reviewer reports the `CE / log₂|V|` wording in both v2 HTML and PDF p.21 and inspects three fixed trainer files, but does not identify Figure 6's actual transformation. This audit freshly checked §3.3/§4.3 only; its browser document scan did not reach C.2, so **the earlier PDF and code findings are attributed, not counted again**.

The dimensional objection is valid independently of that provenance: vocabulary-size normalization is not conversion to bits per original byte. However, an incorrect explanatory sentence can coexist with correct plotting code. Do not report an established Figure 6 implementation bug or invalidate every multiple-choice result.

**Usable sentence:**

> Figure 6's log-to-BPB transformation remains unverified. The previously documented C.2 wording is not a general BPB conversion and should not certify equal cross-tokenizer training sufficiency; the separately specified byte-normalized option-ranking protocol and text-budget controls require their own evaluation.

## 5. Cross-paper statements that are safe to synthesize

### 5.1 Units, probability and BPB

For a stated set of scored events with total negative log probability `L_nats`, scored-event count N and matching original-byte denominator B:

```text
byte-normalized event score = L_nats / (B ln 2)
                           = CE_mean_nats * N / (B ln 2)
```

N must count the events actually averaged by CE, excluding padding/unscored prompts and accounting for repeated or overlapping targets. If logs are already in bits, do not divide by ln 2 again. Auxiliary losses, label smoothing and multi-window composite objectives are not automatically ordinary sequence NLL.

The numerator must name its probability event:

- Native causal byte-chain likelihood is not the same event as a selected canonical token path, an unmarked string marginal, a raw-prefix conditional, a marked EOT path or a denoising target conditioned on corrupted full text.
- A deterministic canonical token-path code length **can legitimately be normalized by bytes and reported transparently**. It need not equal the sum of probabilities of all paths decoding to the same text. Do not incorrectly ban all byte-normalized subword scores; distinguish the label and estimand.
- MYTE explicitly uses **parallel English UTF-8 length** (Eq.1 also includes a +1 convention), not each target language's raw-byte length. It is not interchangeable with the usual per-target-byte score. The missing minus sign and unspecified log base should be reported as unresolved specification details, not converted into an empirical failure claim.
- The MTPC auxiliary objective is overlapping-window composite likelihood; acceptance or window NLL cannot simply become byte-chain BPB. LCA threshold acceptance does not manufacture a target-law guarantee.
- Restricted Hutter/Wiki byte alphabets, MT characters, Unicode codepoints, span labels and subword tokens remain separate units even if papers casually call several of them “characters” or “tokens.”

### 5.2 Three different meanings of acceptance

| Evidence | Acceptance object | What cannot be substituted for it |
|---|---|---|
| LCA threshold policy | Fraction of candidate bytes admitted by the confidence threshold and left-to-right stopping rule | Correctness probability, distribution overlap, exact target-law preservation |
| Strict speculative sampling | p/q rejection test at the actual conditional prefix, with residual correction | Greedy string-match rate, top-1 agreement, deterministic identity of random draws |
| MTPC reported μacc | Mean drafted tokens accepted **per cycle**, explicitly in [0,n] | A percentage unless the denominator n and cycle averaging are specified; also not throughput |

Leviathan's i.i.d. acceptance assumption is used for the capped-geometric expected yield and speed formula, **not needed to justify the elementary residual identity at a fixed context**. Higher acceptance can lose wall-clock speed because proposer/head cost, cache handling and rejected work change. The MTPC Table 1 example (CP rank 32 versus 128) and LCA candidate-count negative are suitable concrete evidence; no universal acceptance-to-speed law follows.

### 5.3 Sharing: only assert the axis actually evidenced

| Sampled evidence | Safe axis and evidence level | Still unknown or different |
|---|---|---|
| MEGABYTE Eqs.4/6 | Same named local byte matrix in local input lookup and output projection; **paper specification** | Global/local table identity, layer tying, runtime storage alias |
| LCA §3 | Shared vocabulary output matrix across the two decoder heads; **paper specification** | Input/output tying; shared decoder-layer parameters across the two heads |
| Bytes-to-Spans §3 | One recurrent LSTM parameter set for input/output phases, and multilingual task-model sharing; **paper statement** | Byte input table tied to event classifier; single joint POS/NER model |
| MTPC | Shared lower trunk, optional private LoRA layers; position/component-indexed readouts | A tied byte input/output table or a free small draft; exact optimized sampler (§4.1) |
| Beyond Text Compression Table 8 | Input/output embeddings tied in this study; **paper configuration** | General result for a 256-byte output alphabet or runtime alias verification |
| TokSuite §3.2–3.3 | Untied embeddings; same initial values for shared token strings across separately trained models | Shared evolving parameters, synchronized model weights or the original ByT5 encoder–decoder architecture |

A family name is not evidence for a tying switch. Unknown tying does not mean no tying. Paper formulas, stated configuration, fixed-code inspection and weight/runtime aliasing remain distinct evidence levels; this review performs only the first two where listed.

### 5.4 Cost and causality: preserve the actual controls

- **MEGABYTE:** §4.1 matches per-byte forward time by tuning architectures and then trains equal byte exposure. Table 6 gives 132 versus 93 seconds for 8192 generated bytes: about **29.5% lower elapsed time**, or **1.42× throughput** for that fixed amount of output. The paper's “40% faster” is compatible with a rate interpretation, not a 40% time reduction. Do not call it a mathematical contradiction. Table 8's best 0.8751 score costs four times the basic scoring work; it is not a free single-pass deployment score.
- **Hourglass:** training steps/s and peak memory, plus 4096-byte overlapping test windows scoring the final 128, are not measured cached serving throughput. The shift must cover all information entering the shortened representation, not just a query tensor; implementation visibility still needs inspection.
- **Charformer/CANINE:** encoder-side full-context grouping/supervision does not establish a prefix-only generator. Fixed stride is not a learned variable hard segmentation. Multilingual text/context approximations do not establish exact example alignment.
- **LCA:** threshold and verified policies differ; Appendix B explicitly drops KV caching for its speculative-acceptance results. External FxT verification adds a resident model; reported 2.1–2.3× must retain that reference/setup rather than becoming a general cached byte-serving claim.
- **MTPC:** large head projections, adapter/cache components, English filtering, EOS suppression and excluded prefill are material conditions. A normalized circuit can model dependent draft bytes; normalization alone does not certify the wrapper's rejection protocol.
- **Distillation:** source/teacher pretraining, offline probability queries and storage are separate from student adaptation. BLD's reported ~10.4 s per 100–150-byte sample/four RTX3090 precomputation is an offline teacher operation, not student serving latency. The ordinary removable interface does not turn its student into a deployed byte generator.
- **Byte simulation:** the grouped stage changes raw context, embedding composition and scored-target density together. “Four times the bytes” is not four times the supervised bytes or an isolated causal estimate of throughput alone.
- **Tokenizer comparisons:** same source-text epoch, same token budget, same parameter count, same sequence positions, matched FLOPs and equal end-to-end wall time are different controls. Beyond Text Compression's 100B GPT-2-token-defined source subset is not 100B tokens under every tokenizer. None of these controls can be silently substituted for another.

## 6. Not reported, not verified, and FULL closure

The sample does **not** justify blanket downgrading sixteen cards to PARTIAL because code, EOS edge cases or missing author budgets were not recovered. PLAN defines FULL as substantive paper and relevant appendix reading, not reproduction. Most cards explicitly meet that content test: methods plus numbers, comparators, negative evidence, key appendix caveats, units and budget boundaries are present. Conversely, a FULL label cannot certify an exact sampler, prove actual weight aliases or fill a method-contract gap.

| Category | Examples from this sample | Appropriate status / owner action |
|---|---|---|
| Required card correction | MYTE aggregate order; Hourglass independence overstatement | Correct the indicated sentences; no new FULL credit. |
| Critical claim qualification missing | MTPC optimized sampler's treatment of rejection residuals | Add §4.1 before asserting exact optimized stochastic decoding; source remains FULL, guarantee remains unverified. |
| Author omitted or contradicted details | LCA acceptance/prose denominator; BLD actual modules/classes; MYTE evaluated MT subset | Mark actual experiment unknown; request fixed run/config or clarification only if the numeric claim is needed. |
| Not verified by source reading | Actual trained embedding aliases; implementation EOT expansion; actual Llama-prefix stability; p/q after decoding transforms | Do not infer runtime state from family, formulas or pseudocode. Fixed artifact inspection is follow-up, not work silently credited here. |
| Budget not reported sufficiently | Total teacher pretraining/inference; total FLOPs versus nominal operation counts; raw-byte exposure; concurrency/prefill/EOS-serving behavior | Keep cells unknown rather than zero; restrict the headline to reported conditions. |
| Prior evidence still open | TokSuite Figure 6 transformation/run mapping | Keep DISCOVERY_CORRECTIONS T1 open. This review neither independently closes it nor substitutes a newly correct formula for the original plotting chain. |
| Audit reproducibility inconvenience | R03 removed its downloaded sources after reading | Public locked sources still permit checking and were used here. Do not equate removed local PDFs with proof that reading never happened. Retaining versioned sources would reduce re-audit friction, but is not a new counting rule. |
| Outside this sample | Remaining R01–R08 cards; exhaustive visual appendix recertification; original broader survey | No coverage/completion claim. Two cards per batch is a balanced spot check, not a random sample with an estimated error rate. |

**Recommended next actions, without creating new agents or experiments:**

1. Existing card owners adopt the two confirmed corrections and the MTPC guarantee qualification. Central owner propagates them to BIP-0221, BIP-0103/0104 and BIP-0173 if those records carry the affected statements.
2. Before an exact-sampling synthesis claim, resolve MTPC's partial-acceptance/rejection branch with fixed code or an author-level algorithm statement. Distinguish this from LCA threshold approximation and from Algorithm 3's ordinary residual identity.
3. Before a precise multilingual MT conclusion, reconcile MYTE Table 4 with the correctly ordered LR column of Table 8 and the language list. Before a numerical acceptance/cost claim, keep LCA and tiktoken table discrepancies explicit.
4. Keep the existing TokSuite log-to-figure request open. Do not count this audit as another full reading or an implementation audit.

## 7. Delivery and verification boundary

Only this Markdown file is written by this task. No inventory, card, batch summary, PLAN, production code or project-wide evidence registry is changed; proposed locations above are adoption instructions. No installations, training, commits, uploads, paid resources or subagents. No temporary downloads or renders were created. Original local extracts were reused read-only; one new built-in-browser tab was reused for three public versioned papers and closed afterward. Existing tabs were left untouched; the browser already had more than ten tabs, which can crowd the sidebar.

Verification is structural: UTF-8/readability, sixteen sampled-card links with two cards in each R01–R08, local Markdown-link existence, and repository status. No build or pytest run is appropriate for this literature-only deliverable. The algebraic examples are explicit analytic diagnostics, not executions of paper software. Structural checks do not validate the scientific content or establish that other authors have adopted these changes.

**Bottom line:** retain the useful selected-reading evidence, fix two specific card statements, add one high-priority conditional sampling-contract concern, preserve genuine source disagreements at their stated scope, and leave unreported runtime/budget fields unknown. Reporting defects and incomplete pseudocode are not automatic mechanism failures.

### Checks actually run

A read-only Python standard-library check passed UTF-8 decoding/no replacement characters, all **41 local-link references**, and **exactly two unique sampled cards in every R01–R08 batch**. The arithmetic in §4.1 was checked directly: discard-and-restart gives `(0.7, 0.3)` to floating-point precision, while residual correction gives `(0.5, 0.5)`. No paper code was run. `git status --short` before and after shows the same pre-existing untracked directory-level entries; because this survey tree is untracked, status alone cannot establish per-file provenance or exclude concurrent changes. This task's only write operation target was this audit file. The checks created no logs, test outputs or temporary files.
