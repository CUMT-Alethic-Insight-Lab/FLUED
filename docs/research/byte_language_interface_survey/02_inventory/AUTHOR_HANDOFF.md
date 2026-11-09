# Author handoff — independent byte-language interface survey

**Frozen author/translator release:** [FINAL_AUTHOR_COUNTS](FINAL_AUTHOR_COUNTS.md) and [VALIDATION](VALIDATION.md) give current verified counts, exact IDs and the R2 claim-rule adoption. Earlier receipt statistics inside historical sections are not the current cohort.

2026-11-09 · current corpus after R01–R10, FIELD_ADDENDUM and both independent audits. **Proceed with synthesis; do not restart discovery to fill a count.** This is an author-facing evidence guide, not the survey text.

## 1. Actual deliverable and counting contract

- **141 independent entities:** 136 academic papers (including one screened proposal), one GPT-2 technical report, three standards and one official model introduction. These are not 141 native-byte language models.
- **92 distinct scoped FULL sources:** 30 old carrying cards, 60 returned R01–R10 cards, and two field-addendum FULL cards. Their identity sets were explicitly reconciled, not merely added. ACT's older W0248 registration was abstract-only: retain that alias under BIW-0138, without counting another work or FULL.
- **Two intentional narrow PARTIAL extractions:** ELMo and the GPT-2 report. Their inspected historical/interface mechanisms are usable, but unexamined results elsewhere in those sources are not certified.
- **296 stable, traceable records:** original 283 merged source-backed records, three audit observations/questions, and ten field-addendum subfindings. These are source-specific questions, mechanisms, controls, negative observations, sharing specifications or reviewer exceptions — **not 296 (or 283) independent scientific problems, successful effects or experiments**. Parent questions overlap; no exhaustive unique-parent count is claimed.
- All original 423 discovery source IDs and 496 mapping edges remain intact. Ten new central extraction keys add ten edges. They do not retrospectively increase the discovery streams' original-row count.

Use [WORK_CATALOG](WORK_CATALOG.md) for identity/version/units, [DETAILED_INVENTORY](DETAILED_INVENTORY.md) for granular mechanisms and mappings, [EVIDENCE_STATUS](EVIDENCE_STATUS.md) for each source and record's ceiling, [TAXONOMY](TAXONOMY.md) for manual parent/subfinding organization, and [CORRECTION_LOG](CORRECTION_LOG.md) for adopted changes. Historical collapsed passages are provenance, not current alternative conclusions. A source-wide FULL label does not override a specific open implementation or formula question.

## 2. Topic-to-evidence guide

| Author topic | Primary carrying evidence | Distinctions to preserve |
|---|---|---|
| History and representation | R02 restricted-alphabet recurrent models, word-local CNN/highway, byte-input annotation and byte mLSTM; R09 deep attention and large plain-byte Transformer; GPT-2 narrow report | Restricted characters, code points, graphemes, UTF-8 bytes, words and merged byte-BPE are not interchangeable. Annotation events are not generated text bytes. |
| Encoders and sequence-to-sequence models | R01 CANINE, Charformer, MANTa, CharacterBERT, embeddingless NMT and Perceiver; old ByT5/MrT5/Local Byte Fusion; R03 character NMT and SDD | Full-source or masked bidirectional encoders do not establish online causal byte generation. Open inputs do not imply open prediction targets. |
| Compute placement and memory | R09 dense/sparse/segment-recurrent alternatives; ACT within-byte depth; Reformer LSH, reversible activations and FFN chunking; old MambaByte/DTP/BLT/H-Net; R05 scratchpads | Fine-position count, expensive-update frequency, internal transitions, training activations and persistent inference KV are separate resources. |
| Grouping and learning | R03 MEGABYTE/Hourglass/HM-RNN/SDD/segmental LM; R09 policy gradients; old rule, entropy, confidence, utility and novelty methods | Fixed rules, external boundaries, soft mixtures, hard partitions, deletion, state selection and posterior segmentation differ. A boundary does not identify the aggregation operator. |
| Output dependence and decoding | R04 marginal/prefix probabilities and speculative sampling; R05 LCA/MtPC/blockwise/diffusion; R10 AU-Net/T-FREE | Local AR joints, independent offsets, normalized circuits, noisy blocks, hidden predictive horizons and finite word dictionaries define different objects. |
| Sharing and adaptation | R08 historical tying/normalized heads; R06 byteification/distillation/ZeTT/Char2Subword; ELMo directional sharing | Input/output, encoder/decoder input, head/head, Q/K, cross-direction, cross-depth and initialization sharing are distinct axes; paper/config/code/runtime evidence levels differ. |
| Language and character competence | R07 MYTE/XTREME-UP/imbalance/noise/CharBench; R10 SpellingBee/Strawberry/dialect; old validity/parity/normalization evidence | Probe recoverability, task-supervised access, natural LM competence, legal scalars, intended scalars, original-string exactness and fairness are different outcomes. |

This remains an independent field survey. A local-project implication may be one bounded final section, never the source inclusion rule or organizing necessity.

## 3. Confirmed corrections the author must use

### MYTE: correct aggregates, retain the real disagreement

[BIW-0104](WORK_CATALOG.md#BIW-0104) / [BIP-0221](DETAILED_INVENTORY.md#BIP-0221): Appendix B Table 8 has columns **AVG LR, AVG**, with MyT5 **21.1 / 21.8** and ByT5 **21.9 / 23.1**. The earlier card transposed them. Both appendix aggregates favor ByT5, whereas main Table 4's low-resource **20.4 versus 20.1** favors MyT5. Do not average tables or choose a convenient sign. Table 8 includes Maltese (`mt`) and Shona (`sn`); C.2 instead names Marathi and omits Shona, listing fourteen names against fifteen language columns. The evaluated population and aggregation reconciliation remain unresolved.

The reported Bit-per-English-Byte denominator is **parallel English UTF-8 length**, with the source's +1 convention, not each target language's bytes. Missing minus sign / unspecified log base is a notation/scoring-contract question, not proof the experiments computed negative surprisal. Morfessor uses language-specific frequency/lexicon resources; MYTE code bytes are not raw UTF-8, and original-byte reversibility after normalization is not established.

### Hourglass: shifted residual prevents a blanket independence claim

[BIW-0072](WORK_CATALOG.md#BIW-0072) / [BIP-0104](DETAILED_INVENTORY.md#BIP-0104): without fine-resolution Transformer layers, the shortened branch lacks current-group history, **but the direct one-step-shifted input residual can still carry the immediately preceding symbol**. Appendix A.1 demonstrates a specific two-position-back copying restriction, not complete within-group independence. Fine-resolution attention removes that restriction in the construction, not a guarantee of learned arbitrary-task accuracy. The extra k−1 shift must still cover every shortening input, including attention keys and values.

### Other adopted corrections

- ByT5 Table 10 measures **XNLI**, not NER. Long sentence-pair input with a single-digit output can still be slow; the XNLI ratio alone cannot establish a long-output cause. NER timings belong to W0360's separate V100 study.
- W0356 is a **3:1 Gated DeltaNet / Gated Softmax Attention hybrid**, where “flat” means no explicit local–global–local hierarchy. Input/output embeddings are untied; fitted N includes output but excludes input/hash tables. Preserve the subword advantage at the reported training-FLOP frontier, without calling the parameter count a full resident budget or FLOPs a wall-time measure.
- MEGABYTE local byte I/O sharing, LCA head-to-head unembedding, TokSuite's untied causal byte-tokenizer arm, Reformer Q/K and ELMo cross-direction sharing are different paper-level specifications. Runtime tensor aliases remain unverified.
- CANINE +2.8 SELECTP (S) and +5.7 MINSPAN (C+n-grams) differ by arm/metric, not an abstract/HTML version flip. Separate prose/table n-gram deltas still conflict. Charformer's illustrative exclusive-width loop is not a verified training-code bug.
- The EOT listing may receive already-expanded caller inputs. Say **preprocessing is not shown**, not **the implementation omits EOT**. Marked-history exactness does not establish an unmarked-prefix marginal.
- MEGABYTE 132→93 seconds for 8,192 bytes is about **29.5% less elapsed time or 1.42× rate**. “40% faster” can be rate language, not a 40% time reduction. Its best quoted scoring result costs four times the basic scoring work.
- XTREME-UP 499 data-card examples versus a selected mean of 120, and 93 total languages versus 39 baseline pairs, are scope differences. The 70-UL benchmark population versus prose's 39-UL evaluation remains insufficiently documented; neither seventy baseline evaluations nor a thirty-nine-language-only benchmark is established.

These adoptions refer to [FULL_READING_AUDIT_R1](../05_review/FULL_READING_AUDIT_R1.md), [FIELD_COVERAGE_AUDIT](../05_review/FIELD_COVERAGE_AUDIT.md), the cards and prior DISCOVERY_CORRECTIONS. The inventory owner did not silently modify source cards.

## 4. Citation boundaries that remain OPEN

### MtPC optimized stochastic wrapper

[BIW-0079](WORK_CATALOG.md#BIW-0079) supports dependent normalized circuit drafts, overlapping-window composite training, and measured head-cost/throughput comparisons. **Do not assert that optimized cached Algorithm 2 has established exact stochastic target-law preservation.** Algorithm 3's ordinary rejection/residual identity is separate from the wrapper: an optional all-accepted bonus is not a required post-rejection positive-residual draw. The optimization does not clearly show this distinction or retained correction state.

The audit's deterministic-first-position example yields `(0.7,0.3)` instead of target `(0.5,0.5)` under literal discard-and-restart. It is an analyst counterexample to one reading, **not a measured released-software bug**. A fixed rejection-branch/state contract, residual carry-over and actual transformed p/q are needed before an exact-wrapper claim. Retain measured throughput under its device, batch, EOS suppression, excluded prefill, head size and adapter conditions; do not invalidate it by association. This is not a new FULL-reading task.

### TokSuite Figure 6

[BIW-0051](WORK_CATALOG.md#BIW-0051) / [BIP-0286](DETAILED_INVENTORY.md#BIP-0286): the C.2 CE/log₂V wording is confirmed in PDF p.21 and HTML. The fixed three-file trainer path logs token CE in nats, but the original **run→log→Figure 6 transformation remains unverified**. Quarantine that figure as evidence of cross-tokenizer equal BPB or equal training/capability sufficiency. Neither a proven plotting implementation bug nor all-task invalidity follows. Ordinary option ranking and the four-tokenizer text-budget control are separate evidence. The extra exact-byte option evaluation is Gemma-tokenizer-only, forty examples taking hours, not fourteen-way exact scoring.

### Prefix, output and termination qualifications

Exact Byte covers refer to a compatible lossless canonical-support process; correcting noncanonical softmax mass changes the original neural distribution. Almost-sure termination is separate from positive EOS hazard at every finite prefix. Offline BPE start flags, repeated RoPE, one-byte-shifted guides and AU-Net's regex need actual prefix-stability evidence for online causal claims; toy counterexamples are not measured leak rates for those actual tokenizers. T-FREE binary trigram sets need not be injective, and hashing an unseen input word does not enable generation outside a finite candidate dictionary.

## 5. Metrics and resource accounting for comparison tables

| Object | Required label / condition | Shortcut to avoid |
|---|---|---|
| Byte-normalized event score | NLL_nats/(matching original bytes×ln2); count actual scored labels, EOS, prompts, PAD and overlapping windows | CE/log₂V; auxiliary, composite-window or denoising-bound loss called ordinary byte-chain NLL |
| Probability event | Native byte chain, canonical token path, completed-string marginal, raw-prefix cover, marked EOT process, or full-source denoising | A denominator change asserted to change the event; or banning transparently labeled byte-normalized canonical-path scores |
| Text unit | Restricted character, code point, grapheme, UTF-8 byte, alternate code, byte-BPE, word or label | Model title substituted for actual units; enwik8 evidence generalized to all Unicode behavior |
| Competence | Clean ability and floors, noise process, whole-string EM, CP/grapheme edits, strict legality, intended scalar, probe EM | Partial byte progress = complete valid Unicode = intended character = correct answer; attention map = causal copying |
| Training resources | Retained/unique/repeated text, original context, positions, total/trunk/training-only parameters, FLOPs, teachers and preprocessing | Equal tokens/steps/positions/parameters/FLOPs treated interchangeably; omitted teacher/drafter costs called zero |
| Serving resources | Measured versus proxy, hardware/precision/batch, prefix/output bytes, KV/peak memory, prefill/EOS and matched quality | Accepted positions, ponder count, weight traffic or synthetic attention time called end-to-end serving speed |
| Evaluation permissions | Fixed weights, hidden-state persistence, test-time weight updates, overlapping rescoring, source/suffix visibility | Dynamic weight adaptation called only a cache; 1,874× uncached-window comparison called modern batched serving |
| Statistical evidence | Population, control, seeds, correlations, uncertainty and local RD assumptions | Language cells called independent training seeds; correlation called isolated causation; missing evidence called a negative finding |

Put a condition once adjacent to the affected result. Preserve substantive negatives and controls: PAQ, dropout matching, leak-free failed padding, MANTa bottleneck, language/host/FLOP reversals, rank/cost nonmonotonicity, slower higher-acceptance cases, and natural/synthetic noise trade-offs.

## 6. Full-read, narrow-read and unread sources

### Completed scoped FULL

All ninety-two identities and their carrying versions are listed in EVIDENCE_STATUS. Navigate by R01–R10, the thirty old cards, ACT and Reformer. This set includes encoders, translation, probability algorithms, background theory and non-language controls; it is not ninety-two experiments on native byte generation.

### Intentional narrow extractions

| Work / stable mapping | Actually read | Safe use | Not established |
|---|---|---|---|
| ELMo / BIW-0140 / FAD-ELMO | v2 §§1–3.4 and Table 1 | Character-composed word positions, word targets, layer mixture/scale, frozen transfer and directional sharing | Exact UTF-8 implementation; complete §§4–6/supplement results/cost/protocol; not a byte LM |
| GPT-2 report / BIW-0141 / FAD-GPT2 | Official p4 §§2.2–2.3, adjacent §3.1 | 256-byte base→merged BPE, category/space policy, 50,257 pieces and 1,024 model-token context | Whole benchmark report, matched raw-byte frontier/cost, complete prefix/EOS behavior; PDF is not revision-pinned |

### Other A/P claims: no current FULL

The following forty-two prior academic reserves retain their original source-depth ceiling. This handoff requests **no new batch**. A bounded identity/mechanism lead may be cited as A/P; a deciding quantitative claim requires its genuinely missing evidence or should be omitted. In particular, do not infer “no byte experiment” for BIW-0085 from the experiment split not having been inspected.

| Work | Current scope ceiling | Related traceable record(s) |
|---|---|---|
| [BIW-0001](WORK_CATALOG.md#BIW-0001) — Neural Machine Translation of Rare Words with Subword Units | A: abstract/metadata | [BIP-0001](DETAILED_INVENTORY.md#BIP-0001) |
| [BIW-0002](WORK_CATALOG.md#BIW-0002) — Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates | A: abstract/metadata | [BIP-0002](DETAILED_INVENTORY.md#BIP-0002) |
| [BIW-0003](WORK_CATALOG.md#BIW-0003) — SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing | A: abstract/metadata | [BIP-0242](DETAILED_INVENTORY.md#BIP-0242), [BIP-0243](DETAILED_INVENTORY.md#BIP-0243) |
| [BIW-0017](WORK_CATALOG.md#BIW-0017) — Funnel-Transformer: Filtering out Sequential Redundancy for Efficient Language Processing | A: abstract/metadata | [BIP-0151](DETAILED_INVENTORY.md#BIP-0151) |
| [BIW-0026](WORK_CATALOG.md#BIW-0026) — Beyond Language Models: Byte Models are Digital World Simulators | A: abstract/metadata | [BIP-0282](DETAILED_INVENTORY.md#BIP-0282) |
| [BIW-0038](WORK_CATALOG.md#BIW-0038) — Rethinking Weight Tying: Pseudo-Inverse Tying for LM Stable Training and Updates | P: selected primary/recovery | [BIP-0192](DETAILED_INVENTORY.md#BIP-0192) |
| [BIW-0039](WORK_CATALOG.md#BIW-0039) — AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models | A: abstract/metadata | [BIP-0193](DETAILED_INVENTORY.md#BIP-0193) |
| [BIW-0040](WORK_CATALOG.md#BIW-0040) — Unsupervised Neural Word Segmentation for Chinese via Segmental Language Modeling | P: selected primary/recovery | [BIP-0147](DETAILED_INVENTORY.md#BIP-0147), [BIP-0148](DETAILED_INVENTORY.md#BIP-0148) |
| [BIW-0041](WORK_CATALOG.md#BIW-0041) — A Masked Segmental Language Model for Unsupervised Natural Language Segmentation | A: abstract/metadata | [BIP-0150](DETAILED_INVENTORY.md#BIP-0150) |
| [BIW-0054](WORK_CATALOG.md#BIW-0054) — Character-level Convolutional Networks for Text Classification | P: selected primary/recovery | [BIP-0084](DETAILED_INVENTORY.md#BIP-0084), [BIP-0125](DETAILED_INVENTORY.md#BIP-0125) |
| [BIW-0056](WORK_CATALOG.md#BIW-0056) — Finding Function in Form: Compositional Character Models for Open Vocabulary Word Representation | A: abstract/metadata | [BIP-0128](DETAILED_INVENTORY.md#BIP-0128) |
| [BIW-0060](WORK_CATALOG.md#BIW-0060) — A Character-Level Decoder without Explicit Segmentation for Neural Machine Translation | A: abstract/metadata | [BIP-0089](DETAILED_INVENTORY.md#BIP-0089) |
| [BIW-0061](WORK_CATALOG.md#BIW-0061) — Byte-based Neural Machine Translation | A: abstract/metadata | [BIP-0090](DETAILED_INVENTORY.md#BIP-0090) |
| [BIW-0062](WORK_CATALOG.md#BIW-0062) — Exploring the Limits of Language Modeling | A: abstract/metadata | [BIP-0133](DETAILED_INVENTORY.md#BIP-0133) |
| [BIW-0065](WORK_CATALOG.md#BIW-0065) — Neural Machine Translation with Byte-Level Subwords | P: selected primary/recovery | [BIP-0134](DETAILED_INVENTORY.md#BIP-0134), [BIP-0135](DETAILED_INVENTORY.md#BIP-0135) |
| [BIW-0067](WORK_CATALOG.md#BIW-0067) — CharBERT: Character-aware Pre-trained Language Model | A: abstract/metadata | [BIP-0100](DETAILED_INVENTORY.md#BIP-0100), [BIP-0101](DETAILED_INVENTORY.md#BIP-0101) |
| [BIW-0069](WORK_CATALOG.md#BIW-0069) — MoCE: Adaptive Mixture of Contextualization Experts for Byte-based Neural Machine Translation | A: abstract/metadata | [BIP-0140](DETAILED_INVENTORY.md#BIP-0140) |
| [BIW-0070](WORK_CATALOG.md#BIW-0070) — Revisiting Character-Based Neural Machine Translation with Capacity and Compression | A: abstract/metadata | [BIP-0141](DETAILED_INVENTORY.md#BIP-0141) |
| [BIW-0073](WORK_CATALOG.md#BIW-0073) — A Vocabulary-Free Multilingual Neural Tokenizer for End-to-End Task Learning | A: abstract/metadata | [BIP-0155](DETAILED_INVENTORY.md#BIP-0155) |
| [BIW-0085](WORK_CATALOG.md#BIW-0085) — Better & Faster Large Language Models via Multi-token Prediction | A: abstract/metadata | [BIP-0176](DETAILED_INVENTORY.md#BIP-0176) |
| [BIW-0086](WORK_CATALOG.md#BIW-0086) — Block Transformer: Global-to-Local Language Modeling for Fast Inference | A: abstract/metadata | [BIP-0180](DETAILED_INVENTORY.md#BIP-0180) |
| [BIW-0087](WORK_CATALOG.md#BIW-0087) — Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads | A: abstract/metadata | [BIP-0181](DETAILED_INVENTORY.md#BIP-0181) |
| [BIW-0092](WORK_CATALOG.md#BIW-0092) — nGPT: Normalized Transformer with Representation Learning on the Hypersphere | P: selected primary/recovery | [BIP-0197](DETAILED_INVENTORY.md#BIP-0197), [BIP-0198](DETAILED_INVENTORY.md#BIP-0198) |
| [BIW-0093](WORK_CATALOG.md#BIW-0093) — Breaking the Softmax Bottleneck: A High-Rank RNN Language Model | P: selected primary/recovery | [BIP-0199](DETAILED_INVENTORY.md#BIP-0199) |
| [BIW-0094](WORK_CATALOG.md#BIW-0094) — Generating Sentences from a Continuous Space | P: selected primary/recovery | [BIP-0202](DETAILED_INVENTORY.md#BIP-0202), [BIP-0203](DETAILED_INVENTORY.md#BIP-0203) |
| [BIW-0095](WORK_CATALOG.md#BIW-0095) — Improved Variational Autoencoders for Text Modeling using Dilated Convolutions | P: selected primary/recovery | [BIP-0204](DETAILED_INVENTORY.md#BIP-0204) |
| [BIW-0096](WORK_CATALOG.md#BIW-0096) — Lagging Inference Networks and Posterior Collapse in Variational Autoencoders | P: selected primary/recovery | [BIP-0205](DETAILED_INVENTORY.md#BIP-0205) |
| [BIW-0100](WORK_CATALOG.md#BIW-0100) — Nested Byte-Level Vocabularies Are Cheap to Deploy and Expensive to Share: A Pre-Registered Negative Result | P: selected primary/recovery | [BIP-0215](DETAILED_INVENTORY.md#BIP-0215) |
| [BIW-0101](WORK_CATALOG.md#BIW-0101) — Kronecker Embeddings: Byte-Level Structured Token Representations for Parameter-Efficient Language Models | A: abstract/metadata | [BIP-0216](DETAILED_INVENTORY.md#BIP-0216) |
| [BIW-0111](WORK_CATALOG.md#BIW-0111) — Tokenization counts: the impact of tokenization on arithmetic in frontier LLMs | P: selected primary/recovery | [BIP-0231](DETAILED_INVENTORY.md#BIP-0231) |
| [BIW-0112](WORK_CATALOG.md#BIW-0112) — Tokenization Falling Short: On Subword Robustness in Large Language Models | A: abstract/metadata | [BIP-0232](DETAILED_INVENTORY.md#BIP-0232) |
| [BIW-0120](WORK_CATALOG.md#BIW-0120) — Character-based Neural Machine Translation | P: selected primary/recovery | [BIP-0244](DETAILED_INVENTORY.md#BIP-0244), [BIP-0263](DETAILED_INVENTORY.md#BIP-0263), [BIP-0264](DETAILED_INVENTORY.md#BIP-0264) |
| [BIW-0121](WORK_CATALOG.md#BIW-0121) — Achieving Open Vocabulary Neural Machine Translation with Hybrid Word-Character Models | A: abstract/metadata | [BIP-0245](DETAILED_INVENTORY.md#BIP-0245) |
| [BIW-0123](WORK_CATALOG.md#BIW-0123) — WECHSEL: Effective initialization of subword embeddings for cross-lingual transfer of monolingual language models | A: abstract/metadata | [BIP-0251](DETAILED_INVENTORY.md#BIP-0251) |
| [BIW-0124](WORK_CATALOG.md#BIW-0124) — FOCUS: Effective Embedding Initialization for Monolingual Specialization of Multilingual Models | A: abstract/metadata | [BIP-0252](DETAILED_INVENTORY.md#BIP-0252) |
| [BIW-0125](WORK_CATALOG.md#BIW-0125) — OFA: A Framework of Initializing Unseen Subword Embeddings for Efficient Large-scale Multilingual Continued Pretraining | A: abstract/metadata | [BIP-0253](DETAILED_INVENTORY.md#BIP-0253), [BIP-0254](DETAILED_INVENTORY.md#BIP-0254) |
| [BIW-0128](WORK_CATALOG.md#BIW-0128) — Mimicking Word Embeddings using Subword RNNs | A: abstract/metadata | [BIP-0262](DETAILED_INVENTORY.md#BIP-0262) |
| [BIW-0129](WORK_CATALOG.md#BIW-0129) — Byte Pair Encoding is Suboptimal for Language Model Pretraining | A: abstract/metadata | [BIP-0266](DETAILED_INVENTORY.md#BIP-0266) |
| [BIW-0130](WORK_CATALOG.md#BIW-0130) — Unpacking Tokenization: Evaluating Text Compression and its Correlation with Model Performance | A: abstract/metadata | [BIP-0267](DETAILED_INVENTORY.md#BIP-0267) |
| [BIW-0135](WORK_CATALOG.md#BIW-0135) — BPE-Dropout: Simple and Effective Subword Regularization | A: abstract/metadata | [BIP-0271](DETAILED_INVENTORY.md#BIP-0271) |
| [BIW-0136](WORK_CATALOG.md#BIW-0136) — Deduplicating Training Data Makes Language Models Better | A: abstract/metadata | [BIP-0279](DETAILED_INVENTORY.md#BIP-0279) |
| [BIW-0137](WORK_CATALOG.md#BIW-0137) — Long Range Arena: A Benchmark for Efficient Transformers | P: selected primary/recovery | [BIP-0280](DETAILED_INVENTORY.md#BIP-0280), [BIP-0281](DETAILED_INVENTORY.md#BIP-0281) |


The three standards define units/instruments, not additional observed model failures. EvaByte stays an official introduction, not a paper FULL; Super Tiny Language Models stays proposal-only, not an achieved experiment. These forty-two plus ELMo are forty-three academic papers without whole-source FULL; GPT-2 adds one technical report. That is a depth inventory, **not forty-four mandatory reads**.

## 7. Readiness and stop rule

**Ready:** a serious independent selected long survey, with historical, encoder, seq2seq, causal/full-resolution/hierarchical, within-byte computation, hybrid output, adaptation, multilingual and methodological anchors. No further substantive omission requiring another batch was established here.

**Not justified:** claims of exhaustiveness, universal byte superiority, or a common resource/quality leaderboard. Classical context mixing/compression history is selective. ACT's byte errors are training-set-only. Reformer's largest models lack equally large full-attention controls. ELMo/GPT-2 remain deliberately narrow. General mixed-script causal routing, unseen-script generation, grapheme-preserving long exact copy, non-ASCII numeracy, and matched-quality batch serving / first-complete-scalar / tail latency remain thin evidence, not proven failures.

Before release, use corrected MYTE/Hourglass statements, retain MtPC/TokSuite restrictions, label source versions and all four units, preserve teacher/evaluation permissions and subgroup/metric uncertainty, and organize the 296 detailed records under overlapping parent questions without inventing an independent-problem count. Absent fields in read sources stay unreported; unexamined runtime stays unverified. Bound remaining scope once in a clear gap section rather than repeating warnings or commissioning endless rereads. The inventory owner has not written the survey itself.

## Final R2 adoption and frozen author/translator contract

Frozen synthesis release:141source entities,296traceable records,12manual multi-label families with506record–family memberships. The other506is a provenance-edge count, not the same relation. Source identity/FULL sets and both relations were actually recounted. No BIW/BIP ID, title, source mapping or family assignment is changed by this claim-only closeout. For translation/synthesis, preserve IDs exactly and reference FINAL_AUTHOR_COUNTS/VALIDATION; do not dynamically renumber, merge, split or reassign records.

Current R2 adoption — dialect TP and IP must be named separately. Appendix F Table 8 gives DI TP correlations +0.638 (Phi), +0.4836 (mBERT), −0.380 (Llama), and DI IP −0.413 (Phi), +0.268 (Llama). Section5.2 explicitly describes Llama TP as negative; the later positive sentence follows IP discussion and may refer to IP. The earlier definite “TP prose contradicts the table” assertion is withdrawn, not a confirmed source conflict. Coefficients and task-dependent associations are unchanged. Effective paired n/significance are not reported in Table8; no causal fairness or Unicode-corruption conclusion follows. Decoder4-bitLoRA and encoderfulltuning are different budgets. T8 whole-source reading is complete; runtime/tokenizer artifacts remain unverified.

R2 reconfirms MYTE v2 Table8 row/column mapping: MyT5 low-resource/overall21.1/21.8; ByT5 low-resource/overall21.9/23.1. Do not follow the baseline-first convention of Table4 and swap model labels. MainTable4 instead reports MyT520.4 versusByT520.1 for its LRsummary; sets/aggregation and the14-name/15-column language population remain unresolved. Cite each table/population, not a fabricated single MT ranking. The parallel-English-byte denominator is not target-languageBPB; sign/log-base uncertainty is not evidence of failed scoring software.

R2 reconfirms Hourglass v2 AppendixA.1/Table9: only the shortened branch lacks current-group history; the shifted-input residual can convey the immediately previous symbol. The particular two-position-back copy limitation is not blanket within-group independence and not evidence of a causal leak. One fine-resolution attention layer removes that restriction in the construction, not every dependency/learned-accuracy guarantee. Extra k−1 shifting must respect all pooling information paths includingQ/K/V.

R2/CLAIM_RULES boundary — MtPC v2 AppendixF: Algorithm3 pp21 lines25–29 draw normalized positive residual when s<n; lines30–31 draw an ordinary target bonus when s=n. Optimized Algorithm2 p20 describes dropping the final verifier token after any acceptance and keeping a shared hidden state, without separating those two roles or specifying retained correction probability state. A literal partial-acceptance discard-and-ordinary-restart interpretation need not preserve the stochastic target law; exact optimized-wrapper preservation remains UNVERIFIED. The analyst two-symbol example yields(.7,.3)rather than(.5,.5)under that interpretation, not an executed sampler or a measured released-code bug. Do not infer greedy mismatch, circuit failure, invalid throughput or actual software bias. Closure needs fixed run-linked branches/state/cache and actual transformed p/q, not a repeatFULL.

R2 independently visually reconfirms TokSuite v2 C.2/PDFp21 printed CE/log₂(vocabulary size), not a general BPB conversion. Figure6 actual log-to-BPB transformation and paper-run provenance remain UNKNOWN: do not claim it implements the printed formula, is repaired by a reviewer formula, or certifies equal cross-tokenizerBPB/training sufficiency. The prior three-file static inspection at0db0ba5648a4fa4efae010a94f69fc1042a354aa is attributed to DISCOVERY_CORRECTIONS, not repeated byR2. Separate option ranking, Gemma-only exact-byte side evaluation and the four-tokenizer text control are not invalidated. Runtimeplotclosure still needs immutable plotcode/logfields/eventbyte totals/weighting/smoothing/EOS/PAD/prompt/overlap/run mapping.

Authority: [CLAIM_RULES](../05_review/CLAIM_RULES.md) and [FULL_READING_AUDIT_R2](../05_review/FULL_READING_AUDIT_R2.md). R2 is a targeted passage audit with **0 new FULL credits**, not a replacement for terra. Canonical bibliographic/record IDs are now a fixed handoff contract.
