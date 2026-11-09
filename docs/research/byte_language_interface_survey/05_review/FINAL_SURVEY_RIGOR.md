# Final independent rigor review of the English byte-language-interface survey

2026-11-09. Review target: the saved English field survey, not a local architecture proposal. **Only this report is changed by this review.**

## 1. Verdict and actual review scope

**Verdict: conditionally ready, with one bounded P1 qualification and three P2 presentation/provenance fixes; no P0 found in the inspected sample.** The survey is substantially evidence-led and field-centered. Its treatment of native bytes, character antecedents, encoder permissions, output laws, parameter axes, multilingual outcomes, and resource reversals is generally sound. It does not need to cover a preferred multigranularity proposal to pass this review.

The P1 concerns the assumptions attached to the finite-state copy bound, not the validity of that bound under its proper copying protocol. The P2 items concern nearby source locations, explicit parameter accounting, and static-configuration provenance. None requires training, new paper-wide reading, or rejecting a paper's empirical contribution. “Conditionally ready” is **not** verification of every number in the 802-line survey, and is not certification of software or exact stochastic decoding.

### What I actually inspected

- Read `PLAN.md`, all of `04_synthesis/SURVEY_EN.md` (802 lines), `EXECUTIVE_SUMMARY_EN.md` (77 lines), `OPEN_QUESTIONS_EN.md` (165 lines), and current `05_review/CLAIM_RULES.md`.
- Read `02_inventory/COUNTS.md`, `FINAL_AUTHOR_COUNTS.md`, and the complete taxonomy. Read the detailed inventory's introduction and targeted current entries, especially BIP-0103/0104, 0221, 0235, 0284–0286, and 0290–0294; mechanically recounted its entire canonical index. **I did not read all 13,522 lines of the detailed inventory as 296 fresh scientific audits.**
- Read **24 distinct carrying cards**, including **22 scoped-FULL cards and two intentional narrow PARTIAL cards**. The new reading-card set inspected here is BIW-0004, 0006, 0008, 0047, 0055, 0068, 0071, 0072, 0079, 0098, 0099, 0104, 0110, 0118, 0127, 0134, ACT/0138, Reformer/0139, ELMo/0140, and GPT-2/0141. Reused carrying cards are ByT5/W0351, Byte Language Models/W0356, Repeat After Me/W0061, and TokSuite/W0518.
- Checked **43 load-bearing claim packets** below. These are related claims, not 43 independent studies or effects. Four packets are explicitly mathematical/accounting derivations; most other packets are checked against the named card and its conditions. **Nine distinct original works** additionally received targeted primary-passage inspection, recorded in §4. This exceeds six original-source passages without pretending that all 24 originals were independently reread.
- Recomputed elementary conversions and bounds with standard-library Python, and independently recounted identity anchors, support classes, and taxonomy memberships. No model, trainer, checkpoint, tokenizer implementation, or paper experiment was executed.
- **New FULL reading credits: 0. New downloads: 0.** Existing retained original-paper extracts/page images were reused. The built-in browser was used for Hourglass and Repeat After Me. An attempted targeted TokSuite HTML inspection did not expose C.2's carrying paragraph in the returned viewport; its PDF/C.2 verification remains **attributed to R2**, not falsely counted as a fresh original check here.

### Sampling limits

This was purposive, risk-weighted sampling: quantitative likelihood/speed/scaling claims; sharing; causal grouping; exactness; multilingual row/column attribution; and selected transfer/competence counterexamples. It was not random sampling, a bibliography-wide forensic audit, a reproduction, a search for every missing predecessor, or an immutable-artifact review. A supported transcription below means that the cited source/card reports it under those conditions—not that its statistical reliability or runtime provenance was reproduced. Numbers outside the inspected packets receive **no new endorsement** from this review.

## 2. Prioritized findings and minimal fixes

Line references below refer to the saved review snapshot. `S` = `04_synthesis/SURVEY_EN.md`, `E` = `04_synthesis/EXECUTIVE_SUMMARY_EN.md`, `O` = `04_synthesis/OPEN_QUESTIONS_EN.md`.

### P0 — none found in this sample

No inspected central claim requires retraction of the field-survey thesis. In particular, the survey does not present TokSuite Figure 6 as validated BPB, MtPC's optimized wrapper as proved exact, MYTE's inconsistent MT summaries as one ranking, or all historical character work as native-byte generation.

### P1-01 — make the copy theorem's read/answer and memory assumptions explicit

**Exact location/claim:** [S:615](../04_synthesis/SURVEY_EN.md#s12): “for a uniform length-L sequence over D symbols, a deterministic single-read system with distinguishable state set S has whole-string success at most |S|/D^L.” Related agenda shorthand: O:94–98. The following S:615 sentence excludes rereading/external memory/growing state, but the quoted proposition does not explicitly say that **the answer is generated after ingestion and depends only on the retained state**.

**Evidence:** [Repeat After Me card, lines 7–9](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md); [current BIP-0235, lines 10553–10555](../02_inventory/DETAILED_INVENTORY.md#BIP-0235); [original v2 §2.1 and §2.3](https://arxiv.org/html/2402.01032v2#S2.SS1). The source defines an input prompt followed by an autoregressively generated answer, and a finite-state update/output system. The bound concerns that protocol, not all single-pass transducers.

**Why the qualification matters:** a system can echo symbols to an output stream while reading them, with constant working state and success one; its already-written output is then an additional information channel. Likewise, a cache of source positions cannot be excluded from the memory count merely by calling only the recurrent vector “state.” This is a scope omission in a mathematically load-bearing statement, not a claim that the cited lower bound fails for its actual task.

**Supported minimal replacement:**

> For a uniform length-L input over D symbols, suppose copying begins only after the complete input has been read, and every input-dependent influence on subsequent output is contained in a retained state from a finite distinguishable set S. Then deterministic whole-string success is at most min(1, |S|/D^L). With b = log₂|S| retained bits, success at least 1−ε requires b ≥ L log₂D + log₂(1−ε). Rereading, an externally retained source/cache, or output written during ingestion changes the premises and must be accounted for separately.

The existing statement about natural-language redundancy and query timing should remain. Do not replace it with “all recurrent models fail to copy,” or import the paper's separate attention-construction issues into this independent counting argument. **Closure:** one local wording change; no new terra batch needed.

### P2-01 — attach exact ByT5 tables and devices to quantitative claims

**Exact locations/claims:** S:171 reports transliteration/G2P/morphology numbers and approximately .75× pretraining throughput; S:664 reports the 6.4–9.5× XNLI slowdown. The preceding citation at S:169 names §§3/6, whereas the carrying task and efficiency evidence is Tables 5, 9, and 10. S:674 links the card, but the hardware is not in the efficiency-table row itself.

**Evidence:** [ByT5 card, lines 13–15 and 23](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md); [TACL original](https://aclanthology.org/2022.tacl-1.17.pdf), Tables 5/9/10. This review checked the card, not those original tables afresh.

**Minimal fix:** append “Table 5” to the three task numbers; “Table 9, TPUv3-64” to the pretraining-throughput claim; and “Table 10, TPUv3-32 for XNLI” to the slowdown row. XSum uses a different TPU count, so do not apply the XNLI device annotation indiscriminately. Preserve **phoneme error rate** for G2P and **character error rate** for transliteration. The reported values are card-supported; this is a locator/condition improvement, not a numerical correction.

### P2-02 — replace vague first-law parameter exclusions with the named components

**Exact location/claim:** S:632: “First-law parameter counts exclude some components, while total-compute comparisons include local modules and embeddings.”

**Evidence:** [Compute Optimal Tokenization card, line 9](../03_reading/R05/BIW-0047.md); original v2 §3.1/Appendix B.1–B.2. Its first-law N excludes local encoder/decoder and input/output embedding parameters, while the reported total-compute comparison includes local modules and embeddings. The distinction is already conceptually correct in the survey.

**Minimal replacement:**

> In the first scaling law, N excludes local encoder/decoder and input/output embeddings; the reported total-training-FLOP comparison nevertheless includes local modules and embeddings. Entropy-model pretraining and scoring are not a fully itemized lifecycle budget.

This prevents “excluded from fitted N” being misread as “excluded from every FLOP budget” or “whole resident model.” Do not demand measured latency from a study explicitly offering operation-based operating points.

### P2-03 — retain the residual provenance limit on ByT5's static configuration

**Exact locations/claim:** S:460 and S:471: the Large XNLI configuration has shared encoder/decoder inputs and untied decoder input/output, on released static-configuration plus Mesh-definition evidence. The narrow model/task scope is correct, but the table does not explicitly retain the mutable gin URL and unverified paper-runtime dependency revision.

**Evidence:** [ByT5 card, line 21](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md), [current sharing register, lines 713–715](../02_inventory/TAXONOMY.md#version--and-axis-specific-sharing-register-current). The cited gin is an XNLI fine-tuning configuration initialized from a million-step checkpoint; it is not a pristine pretraining execution log. The matched Mesh definition has a fixed commit, but that does not prove the paper used exactly that dependency revision.

**Minimal fix:** add to that row's limitation: “Mutable operative-gin artifact; matched Mesh definition is pinned, paper-runtime revision and aliases unverified.” Do **not** replace the row with a universal “ByT5 is untied” statement or treat a current HF Small config as an independent replication of the original Large run. No runtime inspection was performed here.

## 3. Claim-by-claim evidence ledger

**Evidence codes:** `C` = carrying-card/current-register verification; `P01`–`P09` = this review's independent original-passage check in §4; `D` = transparent analyst derivation. “Keep” means retain the stated limited claim, not certify the entire study. Each row preserves the scientific event and the condition most likely to change its interpretation.

| # | Exact survey location and claim inspected | Specific carrying evidence | Assessment, condition, and minimal action |
|---|---|---|---|
| 01 | S:120–122; E:21: character-aware word LM has 78.9 PTB PPL/19M versus 85.4/20M. | [BIW-0055](../03_reading/R02/BIW-0055.md), lines 7–9/14, v4 Model/Table 3. `C` | **Keep.** Inputs are characters inside supplied words; outputs are fixed word classes. The ≈60% saving belongs to the separate published 52M comparator, not the 20M control; S explicitly gets this right. Not raw-byte likelihood. |
| 02 | S:122; E:21: no-highway/two-highway/MLP PPL 84.6/78.9/92.6; about 1500 versus 3000 word tokens/s. | [BIW-0055](../03_reading/R02/BIW-0055.md), lines 16–17, Table 7/Further Observations. `C` | **Keep.** Optimization and composition vary together. Speed is training word-token rate, not end-to-end byte serving; caching trades work for memory. No error bar or general necessity theorem is supplied. |
| 03 | S:124, 468: ELMo shares representations and softmax across directions, not character-input/word-output tables. | [ELMo designated PARTIAL](../03_reading/FIELD_ADDENDUM/arxiv_1802.05365v2.md), lines 3/11–13, v2 §§3.1–3.4; BIP-0293/0294. `C` | **Keep.** Word-time directional LSTMs remain separate. The survey does not infer UTF-8 serialization or certify §§4–6/supplement from this narrow extraction. |
| 04 | S:130–132: GPT-2 uses byte-based BPE, 50,257 merged symbols and 1024 model-token context. | [GPT-2 designated PARTIAL](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md), lines 3/7–15, official report p.4 §§2.2–2.3. `C` | **Keep.** The alphabet begins with bytes; model positions/outputs are merged pieces. Category constraints and space exception are report-specific. No benchmark/frontier endorsement follows from the narrow historical read. |
| 05 | S:169: ByT5 changes mean corruption span to 20 bytes and roughly 3:1 encoder/decoder layers. | [W0351](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md), lines 7/11, §§3/6. `C` | **Keep.** Byte encoder–decoder denoising, not unconditional causal-LM evidence. Recipe/capacity changes are not effects forced by the alphabet. |
| 06 | S:171: Large transliteration 10.5 versus 18.1, G2P 1.8 versus 6.7, morphology 89.7 versus 75.7. | [W0351](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md), line 23, Table 5. `C` | **Keep with P2-01 locator.** Different supervised metrics: transliteration CER, phoneme error rate, morphology accuracy. Not a common causal likelihood score, nor three independent pretraining interventions. |
| 07 | S:171/664: ≈.75× pretraining throughput; XNLI 6.4–9.5× slower. | [W0351](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md), lines 13–15, Tables 9/10. `C` | **Keep with P2-01 devices.** Fixed 1024 input positions expose unequal text, about 4.1 bytes/mT5 piece in the mixture. XNLI has short labels; long generated output alone cannot explain its slowdown. |
| 08 | S:460–471: ByT5 Large XNLI shares encoder/decoder inputs but unties decoder softmax. | [W0351](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md), line 21; [sharing register](../02_inventory/TAXONOMY.md#version--and-axis-specific-sharing-register-current). `C` | **Keep only at static named-config scope; P2-03.** No other-size, port, pristine-pretraining, exact-dependency, or runtime-alias claim. Unknown elsewhere is not untied/tied by inheritance. |
| 09 | S:177–179: CANINE is code-point hashing plus stride-four hierarchy, with C/S objectives differing. | [BIW-0004](../03_reading/R01/BIW-0004.md), lines 7–10, v4 §3/Figures 1–2. `C` | **Keep.** Hash collisions are accepted. Bucketed C targets are not exact code-point probabilities. S imports subword supervision that can be discarded at deployment. Not a byte generator. |
| 10 | S:181: CANINE CoNLL F1 74.0→86.7 with n-grams, mBERT 87.8; 127M→167M. | [BIW-0004](../03_reading/R01/BIW-0004.md), lines 15–16, Tables 2/5/7. `C` | **Keep.** Lexical memorization and capacity change with n-grams. +2.8 SELECTP and +5.7 MINSPAN belong to different arms; survey avoids a false version story and retains unresolved prose/table deltas. |
| 11 | S:183: CANINE-S/mBERT/full-length-character throughput 6400/9000/900 examples/s. | [BIW-0004](../03_reading/R01/BIW-0004.md), lines 14/20, Table 2, 64 TPUv3. `C` | **Keep.** This is pretraining throughput; shortening need not beat subwords. Increasing stride trades QA for speed, not a free efficiency win. |
| 12 | S:268: MANTa Gaussian cumulative membership is approximate and L/4 cap prevents per-byte degeneration. | [BIW-0006](../03_reading/R01/BIW-0006.md), lines 7–13, v1 §3.1/§6.1/Appendix D. `C` | **Keep.** Soft membership is not exact segmentation marginalization; excess block representations can be truncated. Qualitative degeneration is reported, not a quantified matched ablation. |
| 13 | S:270/665: MANTa 2.61 versus byte-T5 9.06 and subword-T5 1.13 seconds/step. | [BIW-0006](../03_reading/R01/BIW-0006.md), line 15, Table 5. `C` | **Keep.** Sixteen V100s; training update time, not decoding. Byte/subword lengths and schedules differ. 9.06/2.61≈3.47, not exactly 4×, and survey avoids the exaggerated ratio. |
| 14 | S:307: MEGABYTE uses global one-patch and local one-byte shifts. | [BIW-0008](../03_reading/R03/BIW-0008.md), line 9, v2 §2.2/Eqs.2–6. `C` | **Keep.** Current local emissions see previous patches and emitted current-patch bytes. The paper-level causal factorization does not certify partial-prompt, EOS, or cache implementation. |
| 15 | S:353/461: MEGABYTE locally factors a dependent byte joint and specifies local input/output matrix reuse. | [BIW-0008](../03_reading/R03/BIW-0008.md), lines 9–11/25, Eqs.4/6/Table 8; [BIP-0284](../02_inventory/DETAILED_INVENTORY.md#BIP-0284). `C` | **Keep.** Local decisions remain serial; global/local tables and blocks are not thereby tied. The best quoted Table 8 combination costs 4× scoring work. No tensor alias was tested. |
| 16 | S:666: 8192 generated bytes take 132→93 seconds, about 29.5% less elapsed time or 1.42× rate. | [BIW-0008](../03_reading/R03/BIW-0008.md), line 24, Table 6. `C`, `D` | **Keep.** Arithmetic checked: 1−93/132=.29545; 132/93=1.41935. Models, context, and quality differ; timing hardware/batch/cache are incomplete. Not a modern matched-quality serving claim. |
| 17 | S:309; E:39: Hourglass shortened branch lacks current-group history, but shifted residual carries the previous symbol. | [BIW-0072](../03_reading/R03/BIW-0072.md), lines 11–13; **current** BIP-0103/0104 and CLAIM_RULES §6. `C`, `P07` | **Keep latest wording, not stale card shorthand.** Original Appendix A.1 explicitly names the residual. The particular two-position-back copy limitation is neither blanket independence nor leakage. One fine attention layer repairs the construction, not arbitrary learned accuracy. |
| 18 | S:200/401; E:25: lm1b 836M plain-byte model ≈.874 BPB→23.0 word PPL. | [BIW-0071](../03_reading/R09/BIW-0071.md), lines 7–21, v1 §3.2/Tables 1–2/Eq.3. `C`, `P05`, `D` | **Keep.** 2^(.874×826189/159658)=22.9867. Same processed corpus/event count; EOS/newlines included as described. Rare-word UNK replacement remains. Final stride-one rescoring is not cached serving. |
| 19 | S:206: sparse dense/fixed/strided BPB 1.00/.99/1.13 and Time/Iter 1.31/.55/.35 at 12288. | [BIW-0118](../03_reading/R09/BIW-0118.md), lines 15–19, v1 §7.2/Table 2. `C`, `P06` | **Keep.** Original table confirms numbers and gives no time unit. No seconds/serving inference. Fastest strided text arm is worse; million-position demonstration is audio. |
| 20 | S:208–210; E:27: Reformer separately changes connectivity, activation reconstruction, and FFN execution. | [Reformer card](../03_reading/FIELD_ADDENDUM/arxiv_2001.04451v2.md), lines 11–15/24–27; BIP-0290–0292. `C` | **Keep.** All positions remain. Reversible F/G need not themselves invert; reconstruction is training activation accounting, not removal of optimizer/parameters/inference KV. Shared QK is not lexical tying. No new original reread in this review. |
| 21 | S:226; E:27: ACT allocates within-byte transitions; Wikipedia evidence is training-only and near-tied. | [ACT card](../03_reading/FIELD_ADDENDUM/arxiv_1603.08983v6.md), lines 7–19, v6 §§2.2/3.5. `C` | **Keep.** 256-class next-byte setup, not segmentation. Stopping-count derivatives are approximated; ponder is not measured time/energy. No exact graph-coordinate digitization or held-out gain is endorsed. |
| 22 | S:557: MYTE uses language-specific Morfessor resources and fixed morphology-derived code bytes. | [BIW-0104](../03_reading/R07/BIW-0104.md), lines 9–13, v2 §3. `C`, `P02` | **Keep.** Not native UTF-8 bytes, gold morphology, or jointly learned neural routing. Original-byte reversibility after normalization is not established. |
| 23 | S:557: seen low-resource non-Latin length 305→145; English 131→109; Ol Chiki Santali 365→365 and ratio 2.80→3.35. | [BIW-0104](../03_reading/R07/BIW-0104.md), line 17, Table 2. `C` | **Keep at card/Table 2 scope.** The parity worsening comes from English compression; Santali does not grow in absolute length. The 99 rows are not 99 downstream wins or independently trained models. Table 2 was not visually rechecked here. |
| 24 | S:559; E:55; O:141: MYTE main and appendix MT means have different signs. | [BIW-0104](../03_reading/R07/BIW-0104.md), line 20 **superseded transcription**; [current BIP-0221](../02_inventory/DETAILED_INVENTORY.md#BIP-0221), CLAIM_RULES §5. `C`, `P02` | **Keep current correction.** Table 8 MyT5 LR/overall=21.1/21.8, ByT5=21.9/23.1; Table 4 LR=20.4 versus 20.1. Fifteen columns versus fourteen C.2 names remain unresolved. No synthetic reconciled ranking or experimental invalidation. |
| 25 | S:561: MYTE denominator is parallel English UTF-8 plus its +1 convention; sign/log base unclear. | [BIW-0104](../03_reading/R07/BIW-0104.md), line 19; original v2 §5.2/Eq.1. `C`, `P02` | **Keep.** A missing printed minus does not establish negative-surprisal software. This is not ordinary target-language-byte BPB. Survey appropriately does not promote the headline 13.4→4.6 to a verified native-byte likelihood gain. |
| 26 | S:579–581; E:57: dialect TP/IP correlations are task/model-dependent, not causal fairness evidence. | [BIW-0134](../03_reading/R10/BIW-0134.md), lines 21–35 **with current CLAIM_RULES §7**. `C`, `P03` | **Keep corrected metric attribution.** DI TP Phi +.638/mBERT +.4836/Llama −.380; IP Phi −.413/Llama +.268. Later positive Llama sentence can refer to IP. No effective paired n, significance, equal-compute intervention, or glyph-proven corruption follows. |
| 27 | S:365: MtPC specifies normalized dependent circuit drafts; overlapping discounted-window objective is composite likelihood. | [BIW-0079](../03_reading/R05/BIW-0079.md), lines 7–11, v2 §3/Appendices B–C. `C` | **Keep.** Smooth sums and decomposable products support circuit queries; this does not certify an outer decoding wrapper. Composite overlapping targets are not once-per-byte chain NLL. |
| 28 | S:367/670; E:43: rank 32→128 acceptance 5.88→6.02 but rate 191.0→182.3 bytes/s; 16-byte tree projection ≈730M versus 21M FF. | [BIW-0079](../03_reading/R05/BIW-0079.md), lines 16/21, Table 1/Appendix C Table 2/Appendix K. `C`, `P01` | **Keep.** Original extract confirms acceptance/throughput and projection counts. EvaByte/L40S, batch one, prefill excluded, EOS suppressed. Projection size is not circuit node count or all resident system memory. |
| 29 | S:369/381; E:43; O:121–127: optimized MtPC Algorithm 2 exactness is unverified. | [BIW-0079](../03_reading/R05/BIW-0079.md), line 17 plus current CLAIM_RULES §3; v2 Appendix F Algorithms 2–3. `C`, `P01`, `D` | **Keep.** Algorithm 3 distinguishes rejection residual from all-accepted bonus; Algorithm 2's drop branch does not. Literal discard/restart counterexample recomputes to (.7,.3), conditional on that interpretation. No released-code bias, greedy mismatch, circuit failure, or invalid throughput is established. |
| 30 | S:392–401; E:63: bits/original-byte = L_nats/(B ln2) = CE_mean×N/(B ln2). | Current CLAIM_RULES §2.2, BIP-0286; [BIW-0071](../03_reading/R09/BIW-0071.md), line 15, as concrete same-event conversion. `C`, `D` | **Keep.** N must be actual CE-averaged labels, B corresponding scored original bytes; no padding/prompt/double-window denominator substitution. Bits-based logs need no ln2 conversion. Canonical-path normalization is not alternative-tokenization marginalization. |
| 31 | S:379–381: speculative acceptance min(1,p/q) plus normalized positive residual restores target mass. | The ordinary identity is also described by [BIW-0079](../03_reading/R05/BIW-0079.md), line 17, Algorithm 3, and CLAIM_RULES §3. `C`, `P01`, `D` | **Keep.** At a fixed prefix, accepted mass=min(p,q), rejection mass=Σ(p−q)+. q must be the actual proposal; zero-q points are not sampled, and p/q transforms must match actual temperature/filtering. This identity alone cannot prove optimized cache/state composition. |
| 32 | S:477–483: row normalization versus full cosine, and unscaled-logit confidence bound ≈2.8% at V=256. | Formula is explicitly analyst accounting; [TAXONOMY C07](../02_inventory/TAXONOMY.md#C07), BIP-0197, supplies its partial-background role. `D` | **Keep only as derivation.** For logits in [−1,1], max softmax ≤ e²/(e²+255)=.0281607. Learned scalar/per-class scales or hidden norms change premises. Not a diagnosis of nGPT or a measured byte-head result. No fresh reading of nGPT is claimed. |
| 33 | S:452; E:47: tying saves Vd=524288 parameters at V=256,d=2048. | Analyst accounting; [sharing taxonomy](../02_inventory/TAXONOMY.md#C07) explicitly distinguishes table axes. `D` | **Keep.** Two independent V×d tables versus one, excluding bias/bridges/specials; not measured memory or performance. If vocabulary includes specials, use actual V. Parameter storage in bytes also needs dtype and runtime storage/alias convention. |
| 34 | S:615; O:94–98: finite-state whole-string copy bound. | [W0061](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md), lines 7–9; BIP-0235; original v2 §§2.1/2.3. `C`, `P09`, `D` | **P1-01.** Add post-ingestion answer and all-input-dependent-information-through-state premises. Non-strict counting bound is supportable; do not endorse the original strict inequality at equality boundaries. No natural-language impossibility or finite-real-coordinate→fixed-bit-memory shortcut. |
| 35 | S:487–489: embeddingless NMT headline changes after token-dropout matching; authors report ≈.45 BLEU worse into English. | [BIW-0068](../03_reading/R01/BIW-0068.md), lines 13–18/26–47; NAACL §6/Table 4. `C`, `P08` | **Keep as the authors' reported mean.** Printed Table 4 rounded cells support the direction; their simple mean gap is .47, compatible with rounding and not proof of an erroneous underlying .45. Token dropout was validation-selected, not an otherwise fixed single-model toggle. |
| 36 | S:632–634: scaling sweep 988 latent+320 subword, ≈50M–6.7B, 4B–1.1T bytes, 5×10^18–2×10^21 FLOPs; optimum 3.69→3.33. | [BIW-0047](../03_reading/R05/BIW-0047.md), lines 9/13–14, v2 §§2.2/3.4/Appendix B. `C`, `P04` | **Keep with P2-02 accounting.** Optima are fitted operating points, not a language-universal constant; fit initialization/Hessian uncertainty is not training-seed replication. No numerical confidence interval is invented here. |
| 37 | S:634: at ≈2.1×10^9 inference FLOPs/byte, 3.3B/T4 HellaSwag 74.1 versus 6.7B/T8 68.2. | [BIW-0047](../03_reading/R05/BIW-0047.md), line 15; original §3.5. `C`, `P04` | **Keep.** This is an operation-based, task-specific operating point; other task rankings differ. Not measured latency or memory equality. |
| 38 | S:636; E:65: recent Byte Language Models uses 3:1 DeltaNet/softmax-attention hybrid; byte parameter frontier and subword FLOP frontier differ. | [W0356](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md), lines 5–8, plus current [sharing/accounting register](../02_inventory/TAXONOMY.md#version--and-axis-specific-sharing-register-current) and current BIP-0050 correction. `C` | **Keep at card/current-correction scope.** Not an all-attention backbone; N includes output, excludes input/hash. Hash n-grams, convolution width, and four-byte curriculum co-vary. No original v1 or runtime reread in this review; no whole-resident-memory frontier endorsed. |
| 39 | S:524–526: staged token-to-byte distillation 20B-byte control has LAMBADA 70.7/31.2 and HellaSwag 73.6/46.7; JBP/MBP task reversals. | [BIW-0098](../03_reading/R06/BIW-0098.md), lines 9–19, v1 Tables 3–4. `C` | **Keep.** Stage 1 outputs teacher tokens, not final bytes. Severe direct-distillation failure belongs to that configuration. Predicted second-byte proxy is neither true lookahead nor exact verification. Not a universal staging law. |
| 40 | S:530–532: cross-tokenizer byte interface is usually temporary; actual byte conversion loses MMLU 60.50→39.06 and IFEval 66.31→25.43. | [BIW-0099](../03_reading/R06/BIW-0099.md), lines 9–19, v1 Tables 1–3/Appendix C. `C` | **Keep.** Ten parallel heads are not within-token sampled conditionals; teacher paths are pruned approximations. About 10.4s/sample on four 3090s is offline teacher computation, not student decode latency. Class-count/LoRA source disagreements remain unresolved. |
| 41 | S:538–540: T-FREE is rule-split/candidate-limited; binary distinct-trigram sets need not be injective. | [BIW-0127](../03_reading/R10/BIW-0127.md), lines 7–16, v2 §§3.1–3.2/Algorithms 1–5/§7. `C`, `D` | **Keep.** 500K+prompt and 80K English+20K German are different stated regimes. BCE features are not normalized word-training probabilities. `aaaa`/`aaaaa` set example is conditional analyst reasoning, not measured released-code collision. |
| 42 | S:603: SpellingBee GPT-2 EM 32.9→16.5 under filtering; injected spelling EM 93.5 with <.01 MLM-loss difference after 1000 updates. | [BIW-0110](../03_reading/R10/BIW-0110.md), lines 17–21, formal Table 1/§5/Figure 2. `C` | **Keep.** Probe recovery is not host instruction competence; initialization intervention is a separate run and a bounded null. No universal proof that explicit spelling never helps follows. |
| 43 | S:429/644; E:63; O:130–136: quarantine TokSuite Figure 6 without discarding separate option/text controls. | [W0518](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md), lines 4–14; BIP-0285/0286 and CLAIM_RULES §4 for C.2 correction. `C` | **Keep, attribution-only primary status here.** Printed CE/log₂V is not BPB; actual figure computation remains unknown. Four-text-control token totals 104.86/114.89/100.23/169.80B are card-supported, not equal FLOPs or byte-arm coverage. Exact-byte side evaluation is Gemma-only/40 examples, not fourteen-way exact scoring. |

## 4. Independently inspected original-source passages

These are **targeted source checks**, not nine fresh FULL reads. Retained extracts are primary-paper text, not reviewer prose; page images preserve important row/column alignment. Public URLs are given for verification. Original-source numerals are reports, not independently reproduced measurements.

### P01. MtPC v2: performance and the two different final-token branches

Source: [arXiv:2511.11346v2](https://arxiv.org/pdf/2511.11346v2), Appendix F pp.19–21, Algorithms 2–3; [retained original extract](../03_reading/R05/sources/BIW-0079.txt), lines 1132–1146 and 1152–1240. Also independently read Table 1/Appendix K numerical extract lines 398–400/1411–1416 and Appendix C lines 1027–1043.

The source says it will “sacrifice the last ‘free’ token,” and Algorithm 2's else branch says “Accept n tokens (drop ‘free’ token).” Algorithm 3, however, has `s<n` residual `max(0,p−q)` in lines 25–29 and ordinary target bonus in lines 30–31. These have different probability roles. This directly supports **unverified optimized-wrapper exactness**, not a software-bug verdict. The inspected performance rows give rank32 5.88/191.0 and rank128 6.02/182.3 acceptance/bytes-per-second, supporting the real cost reversal independently of the guarantee discussion.

### P02. MYTE v2: row/column identity, populations, and Eq.1 denominator

Source: [arXiv:2403.10691v2](https://arxiv.org/pdf/2403.10691v2), [PDF p.17 image](../03_reading/R07/sources/BIW-0104-p17.png), [p.7 image](../03_reading/R07/sources/BIW-0104-p7.png), and [original extract](../03_reading/R07/sources/BIW-0104.txt), lines 303–330.

Table 8 visibly orders columns **AVG LR, AVG**, and rows **MyT5, ByT5**: 21.1/21.8 and 21.9/23.1. Table 4 instead orders baseline first and reports 20.1/20.4 for low-resource MT. The page's C.2 prose lists fourteen language names; Table 8 has fifteen language columns including `mt` and `sn`. The survey uses the corrected mapping, unlike its stale card line 20. The original §5.2 passage explicitly says normalization uses English-sentence UTF-8 length, and Eq.1 prints a positive sum of logs without a minus. Supported conclusion: the scoring contract and aggregation bridge remain unclear; **not** that runs calculated negative loss or that morphology encoding failed.

### P03. Dialect formal source: metric referent, coefficients, and uncertainty ceiling

Source: [EMNLP 2025 formal PDF](https://aclanthology.org/2025.emnlp-main.1224.pdf), [original Table 8 image p.24009](../03_reading/R10/sources/BIW-0134-p18.png), [original extract](../03_reading/R10/sources/BIW-0134.txt), lines 270–319.

The source explicitly first describes Llama TP as the “expected negative correlation,” then discusses higher IP and a positive Llama relation. Table 8 separately gives DI TP −.380 and IP +.268. This makes a definite TP prose contradiction unjustified. Original table coefficients match S:579; it does not provide effective paired n, uncertainty, or significance in those cells. The different signs are worth reporting, but do not identify a causal tokenizer effect.

### P04. Compute Optimal Tokenization v2: sweep sizes, fitted optima, and inference operating point

Source: [arXiv:2605.01188v2](https://arxiv.org/pdf/2605.01188v2), [original extract](../03_reading/R05/sources/BIW-0047.txt), lines 281–286, 306–330, 520–523, and 585–590.

§2.2 says “988 latently and 320 subword tokenized models,” sizes “50M to 6.7B,” data “4B to 1.1T bytes,” and exact training-FLOP accounting unless otherwise stated. §3.4 prints 3.69 at 10^20 and 3.33 at 2×10^21. §3.5 prints approximately 2.1×10^9 FLOPs/byte and 74.1% versus 68.2%. These support the survey's operation-based claims, not a latency curve or system-memory comparison. The fitted-first-law N exclusions are card-checked, rather than independently reconstructed from every appendix equation here.

### P05. Bridging the Gap v1: benchmark event counts and expensive scoring

Source: [arXiv:1908.10322v1](https://arxiv.org/pdf/1908.10322v1), [original extract](../03_reading/R09/sources/BIW-0071.txt), lines 67–78, 102–109, 127–137, and 143–164.

The original reports around 836M parameters, test 159,658 word events and 826,189 byte events; the table caption explicitly includes word EOS and byte newlines. It states rare words are replaced by UNK and final test uses stride one. The metric passage defines information through `−log₂ P(text;model)`: the legitimate conversion holds for the same scored probability event, not arbitrary separately trained token/byte models. The survey's .874→23.0 calculation is numerically correct, with processed-text limitations retained.

### P06. Sparse Transformer v1: quality–iteration reversal, not invented seconds

Source: [arXiv:1904.10509v1](https://arxiv.org/pdf/1904.10509v1), Table 2/§7.2; [original extract](../03_reading/R09/sources/BIW-0118.txt), lines 365–377 and 416–427.

The table header is “Bits per byte Time/Iter,” without a time unit. Its 12,288-context enwik8 rows are dense 1.00/1.31, fixed .99/.55, strided 1.13/.35. This independently supports S:206's quality/cost reversal, including its refusal to label seconds. It does not supply cached-serving measurements. Modality limitations on million-position evidence remain card-supported.

### P07. Hourglass v2: residual access and all-path alignment

Source: [original v2 §2.2/Algorithm 1](https://arxiv.org/html/2110.13711v2#S2.SS2), [Appendix A.1/Table 9](https://arxiv.org/html/2110.13711v2#A1.SS1), read through paginated built-in-browser DOM text.

Appendix A.1 says prediction can use “shortened embeddings and input token embeddings shifted right by 1 from the residual connection.” Table 9 explains why the chosen third-position repeated letter is not recoverable from those available features. Algorithm 1 applies the extra k−1 shift before shortening; attention pooling includes full-resolution K/V as well as pooled Q. S:309 is therefore more precise than the source's broad reduced-expressivity prose and the stale blanket-independence sentence in card line 13. It does not turn a capacity restriction into a leak.

### P08. Embeddingless NMT formal source: token-dropout selection and direction reversal

Source: [NAACL 2021 paper](https://aclanthology.org/2021.naacl-main.17.pdf), §6/Table 4; [p.5 image](../03_reading/R01/sources/BIW-0068-p5.png) and [original text](../03_reading/R01/sources/BIW-0068.txt), lines 254–281.

The original says the reevaluation allows token dropout “as a potential hyperparameter,” and reports almost identical byte-model results out of English but a .45 BLEU average decline from removing embeddings into English. The displayed Table 4 has the same direction. A simple average of its rounded into-English learned/fixed byte cells is .47; this does not identify the unrounded mean or prove a reporting error. The supported synthesis is **a regularization/recipe interaction**, not intrinsic fixed-coordinate superiority or a claimed exact replicated mean.

### P09. Repeat After Me v2: finite distinguishable state and post-prompt answer

Source: [v2 §2.1](https://arxiv.org/html/2402.01032v2#S2.SS1), [§2.3/Theorem 2.7](https://arxiv.org/html/2402.01032v2#S2.SS3), independently read in the built-in browser.

The setting defines input as the “prompt” and output as the generated “answer.” The generalized state-space model uses a **finite set S**, update `u:S×D→S`, and readout `r:S→D`. The source's theorem prints strict error `>1−|S|/D^L`; the card correctly separates the safe non-strict counting implication from that boundary wording. My replacement is an independently checked pigeonhole argument: at most one exact answer per retained deterministic state, hence at most |S| successful uniform inputs. It does not certify the paper's separate Transformer construction. A viewport attempt at Appendix D did not expose its proof text, so **fresh full proof-appendix reading is not claimed**.

## 5. Mathematical and resource-accounting checks

### 5.1 Entropy, surprise, confidence, and BPB

The synthesis's distinctions at S:282–290 are scientifically appropriate. For a prefix c and byte distribution p, predictive entropy is

`H_bits(X|c) = −Σ_x p(x|c) log₂ p(x|c)`.

Observed surprisal is `−log₂ p(x_observed|c)`, not entropy. The SOMBRERO training target `1−stopgrad p(x_observed|c)` is a dimensionless probability-complement/confidence target, **not** a number of bits. It can use an observed training label without a deployment policy reading the future. A monotone transform of observed confidence is still not a predictive-entropy expectation or a causal estimate of computation value. The survey does not mistakenly equate those signals.

S:392–399's loss formula is dimensionally correct provided the CE is natural-log NLL for the named events, N is its effective averaging count, and B is the corresponding byte count. If CE is already in bits, remove ln2; if it is per token, keep N/B; if it is label-smoothed, auxiliary/composite, or an ELBO, do not silently rename it ordinary byte-chain NLL. For a uniform vocabulary with one event per byte, entropy is log₂V bits; dividing that entropy by log₂V would give one, not the correct log₂V BPB. This is why TokSuite's printed vocabulary normalization is not a general conversion, independently of what its figure code actually did.

An unfinished raw prefix, completed-string marginal, canonical token path, and marked byte/boundary history have different numerators. A correct unit conversion cannot erase those event differences. S:390–440 and E:63 retain this distinction; the unverified TokSuite figure receives no numerical BPB endorsement here.

### 5.2 Exactness and author-printed mistakes

The acceptance/residual identity passes the fixed-prefix mass check. The analyst example at S:381 also passes arithmetic: accepted mass (.5,.1), rejection .4, correct residual contribution (0,.4), versus an ordinary-restart contribution (.2,.2), yielding (.7,.3) only for the specified discard/restart interpretation. No executed sampler was tested.

The survey correctly separates three issues:

1. a normalized draft distribution;
2. the inner speculative rejection identity;
3. a complete outer algorithm with correct partial/all-accept state and cache behavior.

Passing the first two does not prove the third. Conversely, unclear or mistaken printed pseudocode does not by itself establish a released implementation bug or invalidate measured throughput. The same standard is correctly applied to MYTE's sign/log-base and aggregate discrepancies, TokSuite's metric wording, and the dialect pronoun/referent issue.

### 5.3 Geometry and memory budgets

- **Table parameter arithmetic:** 256×2048=524,288 parameters saved by one lexical-table tie under the stated two-versus-one-table convention. This is not 524,288 bytes: dtype, optimizer states, gradients, master copies, and actual aliases determine training/resident storage.
- **Cosine bound:** `e²/(e²+255)=.028160687`, or about 2.816%. It requires every unscaled logit in [−1,1]. Learned scale/hidden magnitude changes the premise. S:481 labels it analyst reasoning and exempts trainable-scale nGPT from a mistaken diagnosis.
- **Rank:** a full-row-rank V×d map with d≥V is onto logit space. Producing the requisite hidden state and learning the task are separate. `ZᵀZ=I_d` for V×d Z requires V≥d. These are algebraic dimension conditions, not accuracy results.
- **Copy capacity:** the P1 replacement supplies the missing protocol premise and maps distinguishable states to bits, rather than equating hidden width with actual memory. An ideal real-valued vector with unlimited distinguishability is not a fixed finite-bit state. Original-source weights do not become per-example memory unless they are updated or otherwise encode that example.
- **No invalid explicit serving-memory equation found:** the three core documents do not offer a numerical all-system KV/resident-memory formula to validate. Their qualitative decomposition is appropriate. They do not infer total peak memory from just compressed position count, fitted N, or reversible activations.
- **Safe supplementary budget template, if the author wants one:** peak inference storage is parameters + persistent KV/recurrent state + auxiliary model state + transient workspace, with shared storage counted once and simultaneous peaks measured rather than assumed additive. For a conventional homogeneous unquantized KV cache only, `2 × batch × cached_positions × layers × KV_heads × head_dim × bytes_per_element` is a conditional cache estimate; it is **not** a formula for recurrent/hybrid models, training memory, or complete resident cost. This is analyst bookkeeping, not a source-backed quantitative result to insert as a new empirical claim.

Reformer activation reconstruction, MANTa execution caches, persistent patch KV, draft adapters, output projections, and teacher precomputation belong on distinct axes. S:208–243, 367, 626, 638, 654–676 and O:38–60/112–116 generally respect that boundary. No generic demand for an unmeasured “complete memory win” should be imposed on studies not claiming one.

## 6. Independent documentary recount and reading-depth discipline

A standard-library Python recount of the saved files, rather than reliance on an earlier audit's pass label, produced:

| Object | Independently observed result | Limit of the check |
|---|---:|---|
| Canonical BIW anchors | 141 unique, exactly 0001–0141 | Does not by itself establish bibliographic deduplication quality. |
| Canonical BIP anchors/index rows | 296 unique, exactly 0001–0296; 296 index rows | Not independent experiments or uniquely solved problems. |
| R01–R10 card files | 60 files, 60 unique BIW filenames | Whole card contents/identity were not all reread here. |
| NEW-FULL-supported records | 145 | Documentary status labels, not verified effects. |
| REUSED-FULL-supported records | 88 | Existing reading support, not new reads. |
| Other record classes | 53 discovery A/P; 3 normative; 2 introduction; 1 open correction; 4 narrow PARTIAL | Sum with the FULL classes is 296. |
| Manual C01–C12 memberships | 35/37/43/43/14/35/33/53/37/60/33/83 | Overlapping memberships, not 506 independent questions. |
| Membership total/union | 506 memberships; union 296 BIP IDs | Different relation from the separate 506 provenance edges. |

The survey's release arithmetic is internally consistent: 136 academic papers + one research report + three standards + one introduction = 141 entities; 137 research documents is the paper+report subtotal. The claimed scoped-FULL union 62 new +30 reused =92 is consistent with the frozen reconciliation, and 60 R01–R10 files plus ACT/Reformer explains the 62. **I did not independently reconstruct all 30 reused identity joins or all 506 provenance edges**, so those portions remain attributed to `FINAL_AUTHOR_COUNTS` rather than falsely re-certified by this recount.

The two intentional historical extractions remain PARTIAL: ELMo §§1–3.4/Table 1; GPT-2 p.4 §§2.2–2.3/adjacent §3.1. This survey does not inflate them to FULL, describe them as blocked reads, or claim unexamined sections lack budgets. Conversely, MtPC and MYTE can remain FULL source readings with an open sampler guarantee or scoring/aggregation issue. FULL is not mathematical, runtime, or lifecycle-cost certification.

## 7. Latest-rule compliance and facts deliberately not endorsed

### The five sensitive cases

- **MtPC:** S:369/381, E:43, O:121–127 preserve the current source/specification-versus-runtime distinction. Keep that qualification anywhere exact optimized stochastic decoding is mentioned. No fixed implementation branch/run mapping was inspected here.
- **TokSuite:** S:429/644, E:63, O:130–136 quarantine the affected Figure 6 inference and preserve separate option ranking/text controls. The actual figure computation and plotting provenance remain unknown. This review does not recertify the three previously inspected trainer files or assume no uninspected plotting conversion exists.
- **MYTE:** S:559–561, E:55, O:141–145 use the current row/column correction, not stale card line 20. Language-set and aggregation linkage remain open. A printed-sign issue is not an experiment-failure diagnosis.
- **Hourglass:** S:309 and E:39 retain the residual-path qualification and all-operand shift requirement, not stale blanket-independence shorthand. The tested expressivity restriction is not leakage.
- **Dialect:** S:579–581 and E:57 name TP/IP and do not manufacture the old definite sign contradiction. Correlation direction is preserved; significance, effective paired n, causality, and irreversible Unicode loss are not invented.

### Unverified or insufficiently sourced facts remain unverified

I found no inspected paragraph that turns an explicit “unknown” into a zero cost or a measured negative. In particular, the survey leaves BLT/H-Net unspecified lexical-sharing switches unknown; does not infer all-ByT5 behavior from a single Large configuration; does not turn independent byte-offset heads into an AR joint; and does not equate an external probe's spelling readout with the host following instructions.

No new numerical endorsement is given to uninspected individual table cells, exact graph coordinates, error bars/seed counts absent from the cards, all 141 bibliographic identities, total teacher costs, peak memory, EOS/partial-prompt behavior, or batched serving. General thinness claims about mixed-script online routing, unseen-script competence, non-ASCII arithmetic, and long multilingual exact copy describe this selected corpus, not impossibility theorems about the field.

Some geometry/gradient/VAE background is deliberately PARTIAL and used for definitions or conditional algebra. This review has not promoted it to decisive native-byte empirical evidence. Classical compression coverage remains selective. Neither additional proposal coverage nor a complete statistical-compression history is an acceptance condition for this independent survey.

## 8. Closure, additional reading, and verification record

### What is actually needed next

1. Apply the local P1 copy-bound qualification; add the three P2 locator/accounting/provenance clarifications if preparing a polished release. These are author edits proposed here, **not performed by this reviewer**.
2. Preserve the current claim rules when translating. In particular, do not translate “unverified optimized-wrapper exactness” into “broken released code,” or swap MYTE's aggregate columns/rows back to the stale card values.
3. If a future version wants stronger positive claims, obtain the relevant **artifacts**, not another broad paper batch: MtPC's run-linked branches/probability/cache state; TokSuite's log→plot transformation; MYTE's table/run/language aggregation mapping; or actual tokenizer/regex prefix-stability evidence.

**Additional terra reading truly needed for the current field-survey acceptance? No.** The one material wording correction follows from the already available source setting and elementary counting; the three P2 fixes already have carrying evidence. The unresolved high-risk questions concern artifact/specification linkage or absent outcome measurements, not unread paper sections that a fresh FULL badge would close. This does not mean the reviewer replaced terra or that every claim is certified. If an uninspected A/P source is later promoted to a deciding quantitative pillar, that specific claim—not all remaining reserves—should receive targeted reading.

### Checks actually run

- `PYTHONDONTWRITEBYTECODE=1 python - <<'PY' ... PY`: PASS for 141/296 unique sequential identity anchors, 296 status-index rows, 60 distinct R01–R10 card filenames, all twelve family membership counts, total 506/union296, and elementary arithmetic. Output's console encoding garbled an em dash in one status label; the UTF-8 source text was read correctly and the class/count stayed unambiguous.
- Independently recomputed: lm1b PPL 22.9866566; cosine confidence .0281606871; table parameters 524288; MEGABYTE elapsed-time reduction .2954545 and rate ratio 1.4193548; MtPC literal-interpretation example (.7,.3). These are arithmetic checks, not experiments.
- Review-target snapshot SHA256: `SURVEY_EN.md` = `b81b86ba784e0e65a14d148f19efb21236c608108143a73944dc3ce1598b794e`; `EXECUTIVE_SUMMARY_EN.md` = `62f9a51b13fad092e73d9f27affca847aed7e1bf49a5840c5a83d5d7325c4bbc`; `OPEN_QUESTIONS_EN.md` = `5fe44c8639928263e0908bdf27226dd39e2e26fc6ef437f0083f54623e713a23`.
- No application build/pytest is relevant to this documentation-only review. No training, installation, source-code changes, author-file edits, commits, or subagents were used. Existing untracked project/research material was present before this task and was left alone.

Final saved-report validation: **PASS** — 43 sequential claim rows; 78 parsed Markdown link destinations with all local file targets present; UTF-8/whitespace clean; all three reviewed synthesis SHA256 hashes unchanged. `git diff --check -- <assigned report>` returned exit 0, although the research directory is untracked and the direct Python check is the meaningful content check. Final `git status --short` showed the same pre-existing top-level untracked research directories/files; this task created only the assigned report and no helper scripts or test output. The sole browser tab created for this review was closed. Such structural checks cannot prove the cited papers' empirical results.
