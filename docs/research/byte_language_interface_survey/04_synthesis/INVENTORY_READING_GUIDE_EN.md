# Reading the byte-language-interface inventory

## 1. What this guide is for

The inventory is best read as a map of design decisions, not as a contest between tokenization and its absence. Its central subject is how a language system connects written symbols to computation, learning signals and generated outputs. An interface can admit every UTF-8 byte while running its expensive network on subwords; it can compose bytes into word representations while predicting only a fixed word vocabulary; it can predict bytes at every position without learning boundaries. Those are different solutions to different problems.

This guide explains how to move from a question to the relevant records, compare mechanisms without losing their experimental conditions, and organize a long survey around those comparisons. The companion [classification essay](CLASSIFICATION_EN.md) supplies a complete compact routing index for the 296 records, an overlapping problem hierarchy and a technique-oriented interpretation. The detailed canonical inventory remains [DETAILED_INVENTORY.md](../02_inventory/DETAILED_INVENTORY.md). Neither thematic draft replaces its individual problem → one-sentence solution → researcher-used technique entries.

The documentary population is **141 independent source entities**: 136 academic papers, including one screened proposal, one GPT-2 technical report, three standards and one official model introduction. Of these, 140 contribute records. There are **296 traceable records**, not 296 distinct scientific questions or experiments. The source-depth ledger contains **92 distinct scoped FULL sources**, two intentional narrow PARTIAL extractions, and other abstract/selected-passage reserves. These denominators come from [COUNTS](../02_inventory/COUNTS.md), not from adding citations or card appearances.

A particularly useful distinction is between a *parent question* and its *source-specific subfindings*. “How should a model spend computation along a byte stream?” is a parent question. A fixed patch construction, a learned router, a negative entropy diagnostic, a cache measurement and an optimization approximation are different records under it. Keeping those records separate preserves mechanisms and evidence; it does not make them independent replications.

## 2. Start with the right document and identifier

### 2.1 The short navigation chain

Use the following chain for a substantive claim:

**parent question → BIP record → BIW identity → carrying card → fixed source location → current correction.**

- [TAXONOMY](../02_inventory/TAXONOMY.md) provides twelve manually assigned, overlapping C01–C12 problem families and their complete record memberships.
- [DETAILED_INVENTORY](../02_inventory/DETAILED_INVENTORY.md) provides stable **BIP** record anchors, specific solutions, actual techniques, evidence conditions and provenance mappings.
- [WORK_CATALOG](../02_inventory/WORK_CATALOG.md) provides stable **BIW** source identities, versions, four interface units and carrying-card links. Historical W identifiers remain aliases, not additional works.
- [EVIDENCE_STATUS](../02_inventory/EVIDENCE_STATUS.md) states the source- and claim-specific ceiling.
- [AUTHOR_HANDOFF](../02_inventory/AUTHOR_HANDOFF.md) and [CLAIM_RULES](../05_review/CLAIM_RULES.md) state adopted corrections and the unresolved issues that matter to synthesis.

A BIW reference answers “which source?” A BIP reference answers “which extracted question, mechanism, control or exception?” Cite both when a work contains several materially different findings. For example, [BIW-0008](../02_inventory/WORK_CATALOG.md#BIW-0008) identifies MEGABYTE, whereas [BIP-0014](../02_inventory/DETAILED_INVENTORY.md#BIP-0014) identifies causal alignment and [BIP-0284](../02_inventory/DETAILED_INVENTORY.md#BIP-0284) identifies a local input/output sharing specification. These should not become three independent demonstrations of the same architectural benefit.

Current card-grounded sections take precedence over collapsed historical discovery extracts. Where a card itself contains a superseded reading, use the later named correction: most importantly MYTE aggregate columns, Hourglass's shifted residual, the dialect metric referent, MtPC's optimized sampler and TokSuite's Figure 6. Historical text explains provenance; it is not a menu of equally valid interpretations.

### 2.2 Reading depth is a permission, not a score

A scoped FULL card means that its fixed source and relevant carrying sections were read. It does not establish the actual software path, reproduce the result, prove every argument, or fill unreported fields. Thus MtPC can have a FULL card while its optimized stochastic wrapper remains unverified. Conversely, a deliberately narrow extraction can support a valuable historical statement without certifying an entire paper.

Two designated PARTIAL cases illustrate the latter. [ELMo, BIW-0140](../03_reading/FIELD_ADDENDUM/arxiv_1802.05365v2.md), covers v2 §§1–3.4 and Table 1: character composition at word positions, contextual layer mixing, transfer and directional sharing. Sections 4–6 and the supplement were not fully audited. [GPT-2, BIW-0141](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md), covers official-report p.4 §§2.2–2.3 and adjacent §3.1: the 256-byte base, merged BPE pieces and category constraints. The remaining report and benchmark results lie outside that extraction. Neither is a failed FULL assignment, and neither licenses a whole-source cost or performance conclusion.

The 296-row support census is 233 scoped-FULL-supported records, four narrow-PARTIAL-supported records, 53 discovery A/P records, three normative records, two official-introduction records and one open metric-computation question. These are support classes for records, not counts of verified effects. The official EvaByte introduction and the three standards retain their documentary kinds; the proposal-only source contributes no achieved experiment.

## 3. Read an interface as four units, not one model name

Before comparing a pair of systems, write **input / internal / output / supervision**. The internal field should identify expensive positions or persistent state, not merely say “hidden vectors.” The supervision field should identify corruption selection, teacher boundaries or auxiliary labels as well as the final target alphabet.

| Interface route | Input | Internal computation | Output and supervision | Good entry point |
|---|---|---|---|---|
| Native byte chain | Individual bytes | Byte positions, recurrent state, or byte-plus-patch hierarchy | Next-byte categorical events, with any specials explicit | [BIW-0071](../03_reading/R09/BIW-0071.md), §2; [BIP-0142](../02_inventory/DETAILED_INVENTORY.md#BIP-0142) |
| Code-point encoder | Unicode code points | Local code-point states, stride-four global states, restored task positions | Task labels; bucketed code points or removable subword pretraining targets | [CANINE card](../03_reading/R01/BIW-0004.md), §§3.1–3.2 |
| Byte seq2seq denoiser | Corrupted source bytes | Full-source encoder states; causal target decoder states | Reconstructed byte/sentinel spans | [MANTa card](../03_reading/R01/BIW-0006.md), §§3.1–3.2 |
| Character-composed word LM | Characters inside externally segmented words | One recurrent position per word | Fixed word classes and next-word cross-entropy | [BIW-0055](../03_reading/R02/BIW-0055.md), Model/Fig.1 |
| Byte-complete subword LM | Merged byte-BPE symbols | One position per merged symbol | Next merged vocabulary item | [GPT-2 narrow card](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md), §2.2–2.3 |
| Sparse lexical hybrid | Rule-split word-like units and trigram features | One backbone position per complete unit | Candidate-dictionary units; multilabel feature training | [T-FREE card](../03_reading/R10/BIW-0127.md), §§3.1–3.2/Algorithms 1–5 |

“Character” must be resolved further where possible. A restricted alphabet in a cleaned corpus, a Unicode code point, a user-perceived grapheme cluster and a UTF-8 byte are different units. [RFC 3629, BIW-0090](../02_inventory/WORK_CATALOG.md#BIW-0090) defines byte-sequence legality; [UAX #15, BIW-0115](../02_inventory/WORK_CATALOG.md#BIW-0115) distinguishes normalization equivalences; [UAX #29, BIW-0116](../02_inventory/WORK_CATALOG.md#BIW-0116) supplies versioned grapheme segmentation. They define instruments and distinctions, not empirical model successes.

Open input support is also not open generation. Character-Aware Neural Language Models can construct vectors from spellings, but the reported output is a fixed word softmax with UNK. CharacterBERT similarly combines local byte composition with word-position understanding and a temporary word prediction vocabulary; see [BIW-0066](../03_reading/R01/BIW-0066.md), §§2–3 and [BIP-0136–0138](../02_inventory/DETAILED_INVENTORY.md#BIP-0136). T-FREE can hash a new input word, yet generation scores a finite candidate dictionary. These are useful hybrid designs, not defective implementations of an assumed byte-output goal.

## 4. Six reading routes through the field

### Route A: Why change the lexical interface?

Start with [C01](../02_inventory/TAXONOMY.md#C01), then contrast three remedies for lexical rigidity: byte-complete subword construction, local spelling composition and native byte prediction. The important question is where the lexical dependency was removed and where it remained.

A historical comparison between Character-Aware LM and GPT-2 is especially clarifying. The former replaces the input word table with character CNN/max-pooling/highway composition while retaining word-time recurrence and word output. The latter retains a large learned piece vocabulary but starts from all 256 byte values. These are nearly opposite ways to combine low-level coverage with higher-level computation. The GPT-2 extraction establishes a 50,257-piece vocabulary and a 1,024-model-token context, not 1,024 bytes; the Character-Aware card establishes a fixed word classifier, not unrestricted spelling generation.

Then read [CANINE](../03_reading/R01/BIW-0004.md). Hash embeddings address the storage and coverage problem of a Unicode code-point lookup. They permit collisions; they do not prove useful knowledge of unseen scripts. CANINE's local attention and strided convolution address long inputs separately. CANINE-S additionally shows that subword supervision may be a training-only resource. A deployed tokenizer-free encoder therefore need not be free of subword-derived learning signals.

This route should lead into multilingual allocation rather than a universal-coverage conclusion. [BIP-0061](../02_inventory/DETAILED_INVENTORY.md#BIP-0061) asks how many positions parallel meanings consume; [BIP-0221](../02_inventory/DETAILED_INVENTORY.md#BIP-0221) studies morphology-derived coding. Representability, effective text context and language utility belong in adjacent paragraphs, not one shared metric.

### Route B: How are fine symbols composed, and what is actually shortened?

Use [C02](../02_inventory/TAXONOMY.md#C02) before [C03](../02_inventory/TAXONOMY.md#C03). This prevents a boundary-first account from concealing the aggregation operator. Compare CNN/max pooling, mean pooling, concatenation, cross-attention, contextual end-state selection, deletion survivors and fixed latent arrays.

Character-Aware LM provides a concrete early optimization lesson: in its PTB large configuration, two highway layers yield 78.9 perplexity versus 84.6 without highway, whereas an ordinary one-layer MLP yields 92.6 (Table 7). This is evidence for gated feature transformation in that character-to-word setup, not a byte-LM result. The same card reports approximately 1,500 versus 3,000 word tokens/s for character versus word input, so parameter savings did not make local composition free.

Charformer and MANTa then separate two forms of differentiability. [Charformer](../03_reading/R01/BIW-0005.md), §2.1, mixes candidate block representations at each byte position and applies a final fixed stride. Its soft width preferences are not a coherent hard partition. [MANTa](../03_reading/R01/BIW-0006.md), §3.1, approximates cumulative frontier-count membership with a Gaussian, applies order-sensitive depthwise convolution/max pooling, and caps retained blocks at one quarter of input length. Section 6.1 reports degeneration toward one block per byte without the bottleneck; it does not provide a quantified matched ablation to invent.

Follow [BIP-0010](../02_inventory/DETAILED_INVENTORY.md#BIP-0010) to Dynamic Token Pooling and [BIP-0026](../02_inventory/DETAILED_INVENTORY.md#BIP-0026) to H-Net. DTP explicitly averages completed character spans; H-Net directly selects already contextualized states. Neither operation establishes lossless inversion. [Local Byte Fusion, BIP-0070](../02_inventory/DETAILED_INVENTORY.md#BIP-0070) is a useful contrast because local fusion restores byte resolution rather than shortening the persistent sequence. Perceiver IO, [BIP-0121](../02_inventory/DETAILED_INVENTORY.md#BIP-0121), compresses deep work into fixed latent slots without requiring contiguous segment identities.

### Route C: Is segmentation necessary for efficient byte computation?

Read [C04](../02_inventory/TAXONOMY.md#C04) with the nonhierarchical counterexamples intact. A historical progression from recurrent characters to hierarchical bytes is one strand, not the entire field.

[BIW-0071](../03_reading/R09/BIW-0071.md) scales a plain 40-layer causal byte Transformer, retaining one position per byte. Its reported 23.0 word-normalized perplexity concerns the processed lm1b corpus, which already contains word preprocessing and UNK replacements; it is neither untouched raw-text evidence nor a matched-compute comparison with every word model. Nevertheless, it directly challenges the claim that a learned compressor is necessary to obtain competitive byte likelihood.

[Sparse Transformer](../03_reading/R09/BIW-0118.md) and [Reformer](../03_reading/FIELD_ADDENDUM/arxiv_2001.04451v2.md) retain sequence positions while changing connectivity and execution. Sparse Transformer's enwik8 Table 2 reports dense/fixed/strided BPB of 1.00/0.99/1.13 with Time/Iter 1.31/0.55/0.35; the header gives no time unit. The fast strided negative matters: fewer interactions did not preserve language quality. Reformer separately addresses approximate attention, depth-dependent training activations and feed-forward intermediates. Its execution chunks are not learned text segments.

[ACT](../03_reading/FIELD_ADDENDUM/arxiv_1603.08983v6.md) adds another axis: repeated recurrent transitions **within** each byte. Its Wikipedia results are training-set errors, fairly similar with and without ACT; punctuation and XML traces motivate effort-versus-uncertainty questions but do not establish held-out byte gains. Pair [BIP-0287–0289](../02_inventory/DETAILED_INVENTORY.md#BIP-0287) with [BIP-0054](../02_inventory/DETAILED_INVENTORY.md#BIP-0054), rather than treating ACT as an early boundary detector.

Finally, [scratchpad patching](../03_reading/R05/BIW-0076.md), §3, changes refresh frequency without changing committed patch count. It aggregates the observed partial patch, calls the trunk and overwrites a transient cache entry. Persistent cache, transient workspace and total computation therefore need separate accounting. This route gives the long report alternatives to compression, not merely variants of it.

### Route D: What makes a grouped predictor causal and a multi-byte decoder coherent?

Join [C05](../02_inventory/TAXONOMY.md#C05), [C06](../02_inventory/TAXONOMY.md#C06) and [C11](../02_inventory/TAXONOMY.md#C11). Trace convolution, pooling, residuals, restoration and preprocessing as well as attention masks.

[MEGABYTE](../03_reading/R03/BIW-0008.md), §2.2/Eqs.2–6, shifts the global input by a patch and the local input by a byte. Its small local Transformer supplies a dependent autoregressive patch joint. Teacher-forced parallel scoring is not independent parallel generation. [Hourglass, BIP-0103/0104](../02_inventory/DETAILED_INVENTORY.md#BIP-0103), requires an additional k−1 shift before shortening. Without fine-resolution Transformer layers, the shortened branch lacks current-group history, but the direct shifted-input residual still carries the immediately preceding symbol. Appendix A.1's copying restriction is specific; a blanket independence claim is wrong.

[Patching Leaks](../03_reading/R03/BIW-0074.md) is a particularly strong mechanism-and-failure pairing. In its 100-symbol independent-random diagnostic, chance is 1%; a naively grouped decoder predicts early block positions near perfectly through future access. Removing convolutional lookahead alone leaves n-gram overlap leakage. Larger padding can remove leakage yet fail translation: German→English factor-two BLEU is 0.04 for that padding arm, versus 25.49 for overlap removal (Table 2). Correct information flow and useful prediction horizons are separate requirements.

For emission, compare local autoregression, independent future classifiers, normalized circuit drafts, diffusion and verifier-based decoding. [MtPC](../03_reading/R05/BIW-0079.md), §3/Appendix B, supplies dependent normalized drafts; its training uses overlapping-window composite likelihood. Its optimized cached Algorithm 2 has **unverified stochastic target-law preservation** because the described state reuse does not clearly distinguish an all-accepted bonus from post-rejection residual correction. Ordinary Algorithm 3's rejection identity does not close that wrapper. The [current rule](../05_review/CLAIM_RULES.md#3-mtpc-exact-source-level-qualification-not-a-software-verdict) is a source-level qualification, not a reproduced software bug.

### Route E: How can an existing model be reused across interfaces?

Read [C09](../02_inventory/TAXONOMY.md#C09) with [C07](../02_inventory/TAXONOMY.md#C07) and [C08](../02_inventory/TAXONOMY.md#C08). Separate static vector imitation, contextual alignment, token-logit distillation, byte-probability conversion, task training and actual byte-output conversion.

[Char2Subword](../03_reading/R06/BIW-0122.md), §§2–3, fits direction, magnitude, neighborhoods and vocabulary identity, then trains through a frozen contextual host. [Bolmo](../03_reading/R06/BIW-0097.md), §3.2.1, aligns representations after four frozen host layers rather than only their inputs. Frozen parameters still require backward computation into the new interface. Bolmo retains a subword-suffix input lookup and learns a byte-plus-boundary output; it is not a pure byte-only parameterization. Its stage-two-only control is not catastrophic: stage one helps, particularly at 1B, but the gap narrows after extra global computation (§6.2/Fig.6). This is a more informative result than declaring a universal need for alignment.

[BIW-0098](../03_reading/R06/BIW-0098.md) distinguishes an intermediate byte-input/token-output stage from final byte decoding. [BIW-0099](../03_reading/R06/BIW-0099.md) uses a common byte supervision space for cross-tokenizer distillation; that common alphabet does not automatically preserve instruction following. [Zero-Shot Tokenizer Transfer](../03_reading/R06/BIW-0126.md) predicts embeddings with a hypernetwork across tokenizers rather than replacing generation with a raw-byte chain.

Sharing must be named by axis. MEGABYTE specifies local byte input/output tying; LCA specifies a common projection between prediction heads; Reformer specifies shared Q/K projections; ELMo specifies representation sharing between directions and softmax sharing between directions. The [sharing register](../02_inventory/TAXONOMY.md#version--and-axis-specific-sharing-register-current) preserves evidence layers. Unknown input/output sharing in BLT or H-Net stays unknown; architectural ancestry is not a tensor-alias inspection.

### Route F: Does finer access improve real language behavior?

Use [C10](../02_inventory/TAXONOMY.md#C10) before constructing any claim about robustness, fairness or character competence. Split representability, learned information, usable task access and generated correctness.

[SpellingBee](../03_reading/R10/BIW-0110.md), §2/Table 1, trains an external decoder of frozen token embeddings. Recoverable spelling is evidence against a simplistic “opaque IDs contain no spelling” assertion. It is not the host's natural spelling ability. The separate spelling-initialization experiment changes masked-LM losses by less than 0.01 after 1,000 updates in the reported run (§5/Fig.2). That is a bounded null intervention, not proof that spelling never helps. Pair it with [Strawberry](../03_reading/R10/BIW-0113.md) and [CharBench](../03_reading/R07/BIW-0114.md), which ask different questions about task-supervised character access and counting versus positioning.

Noise evidence also needs its actual process. [Synthetic and Natural Noise](../03_reading/R07/BIW-0109.md), Tables 6–7, contrasts order-invariant means, character CNNs and mixed-noise training. Invariance protects against scrambling while losing distinctions and clean quality; a mixture improves broad coverage while not matching each specialist. Its “natural” noise is reconstructed from edit lexicons, not a naturally noisy parallel test corpus. These character/word experiments are antecedents, not native-byte robustness measurements.

For multilingual work, keep language sampling, code length, task labels and adaptation permissions separate. MYTE's current [BIP-0221](../02_inventory/DETAILED_INVENTORY.md#BIP-0221) must use Appendix Table 8's low-resource/overall means: MyT5 21.1/21.8, ByT5 21.9/23.1. Both favor ByT5, whereas main Table 4's low-resource 20.4 versus 20.1 favors MyT5. The evaluated sets/aggregations remain unresolved; do not manufacture one reconciled ranking. Its reported English-byte denominator uses parallel English UTF-8 length, not each target language's bytes, and its morphology-derived codes are not raw UTF-8.

## 5. Three comparison habits that prevent false synthesis

### 5.1 Name the probability event before its denominator

For matching scored events, convert nats to bits per original byte as

`score = summed_negative_log_probability_nats / (matching_original_bytes × ln 2)`.

If only mean cross-entropy is available, multiply by the actual number of scored labels, excluding ignored/padded labels according to the loss. Specify prompts, terminal events, normalization and repeated or overlapping scoring. A denominator change does not marginalize alternate token paths or create a normalized joint from auxiliary objectives.

Keep five objects distinct: a native byte chain, a canonical token path normalized by bytes, a completed-string sum over tokenizations, a raw-byte-prefix cover event, and a marked byte-plus-boundary process. Canonical-path byte normalization can be useful and legitimate when labeled. [BIW-0080](../03_reading/R04/BIW-0080.md) studies completed-text marginalization; [Exact Byte Probabilities](../03_reading/R04/BIW-0088.md), §4/Appendix A, studies compatible prefix covers. The latter's canonical-support assumptions matter: suppressing noncanonical softmax mass changes the original neural distribution. Almost-sure termination is also stronger than positive EOS probability at each finite prefix.

TokSuite v2 C.2's printed CE/log₂|V| expression is not a general BPB conversion. The actual run→log→Figure 6 transformation remains unknown. Exclude Figure 6 as certification of equal cross-tokenizer BPB or equal training sufficiency while retaining separately supported option ranking and the four-tokenizer text-stream control; see [BIP-0286](../02_inventory/DETAILED_INVENTORY.md#BIP-0286) and [CLAIM_RULES §4](../05_review/CLAIM_RULES.md#4-toksuite-exclude-an-unverified-figure-inference-not-the-whole-study).

### 5.2 Match a vector of resources, not the word “budget”

Record original/unique/repeated/retained text; original-text context; model positions; total and trunk parameters; training-only modules; training FLOPs; teacher/preprocessing cost; and inference hardware, precision, batch, prefill, output size, cache and quality. Equal steps, equal positions, equal text, equal parameters and equal FLOPs answer different questions.

MEGABYTE's Table 6 takes 132→93 seconds for 8,192 generated bytes: about 29.5% less elapsed time or 1.42× rate, with different model sizes and contexts and unspecified timing hardware/batch/cache in that comparison. Its best quoted Table 8 PG19 score uses four times basic scoring work. MANTa's 2.61 versus 9.06 seconds is a training-step comparison on 16 V100s, not generation latency. ByT5 Table 10 measures **XNLI**, not NER, among its tasks; a long-input/single-digit-output task can still be slow. These conditions identify what was learned rather than cancel the findings.

MtPC makes the distinction between proxy and cost especially concrete. Its L40S, batch-one, prefill-excluded EvaByte sampling comparison gives acceptance 5.19/5.88/6.02 and throughput 176.3/191.0/182.3 bytes/s for factorized/rank-32/rank-128 drafts (Table 1). Higher acceptance is not necessarily faster. EOS suppression, large circuit heads and conversion costs delimit this measurement. A cross-paper table should therefore compare reported frontiers and mechanisms, not sort all systems by an apparently common speed number.

### 5.3 Keep a finding's type attached

A boundary-enrichment diagnostic, random-sequence leakage test, controlled ablation, external probe, statistical correlation, conditional theorem and software reproduction establish different things. Report an empirical negative under its actual contract: DTP whitespace matching learned routes in English but not Finnish; leak-free padding failing translation; MANTa's no-bottleneck degeneration; larger draft rank slowing generation; language- or host-specific transfer reversals. Do not convert an unmeasured outcome into a failure.

The same discipline resolves apparent duplicate records. [BIP-0274/0275](../02_inventory/DETAILED_INVENTORY.md#BIP-0274) define and correct a prefix-event mismatch; [BIP-0111/0182/0278](../02_inventory/DETAILED_INVENTORY.md#BIP-0111) develop compatible conversion, incremental cost and ensembling. They are linked subquestions, not five independent confirmations of “tokenization bias.” Likewise [BIP-0284/0285/0294](../02_inventory/DETAILED_INVENTORY.md#BIP-0284) are sharing specifications and [BIP-0286](../02_inventory/DETAILED_INVENTORY.md#BIP-0286) is a review exception, not four author-solved scientific problems.

### 5.4 Build small comparison packets rather than a universal leaderboard

A comparison packet consists of a parent question, two or three carrying sources, the mechanism difference, the strongest relevant control and the outcome that remains unresolved. This format is more useful to a survey integrator than a long table whose columns silently change meaning between rows. Three packets illustrate how to assemble one from this inventory.

**History reuse versus recomputation.** Begin with [Transformer-XL, BIW-0119/BIP-0238](../03_reading/R09/BIW-0119.md), formal §§3.1–3.3 and Table 9, then connect [BIP-0099](../02_inventory/DETAILED_INVENTORY.md#BIP-0099) and the Sparse Transformer/Reformer routes. Transformer-XL concatenates stopped-gradient prior-segment states with current states, using relative positions to avoid reset-position ambiguity. It does not update its weights simply because hidden state persists, and its memory is a stored sequence rather than a fixed-size recurrent vector. Its reported 1,874× evaluation comparison at attention length 3,800 is against from-scratch full-window recomputation, not modern matched-cache batched serving. The contribution is a principled reuse mechanism; the headline ratio describes the selected baseline. Next ask whether sparsity reduces connectivity, reversibility reduces training activations, or segmentation reduces trunk positions. These are alternative savings with different retained state, not three measures of one memory quantity.

**Lexical discovery versus useful computation boundaries.** Pair [Segmental Neural LM, BIW-0042/BIP-0149](../03_reading/R03/BIW-0042.md), §§2–4/Appendix F, with DTP and H-Net. The segmental model sums over permitted character segmentations using dynamic programming, mixes spelling and lexical-memory generation, and regularizes expected segment lengths. Its MAP segmentation is recovered after the whole sentence; its reported boundary evaluation uses the union of train/validation/test. DTP delays completed-segment summaries for causal prediction, while H-Net selects contextual states for fewer expensive updates. A favorable lexical F1, a lower next-character loss and a better quality/FLOP frontier therefore test different claims. Their common interest is variable units; their differences are the latent probability model, the deployed decision clock and the supervised or implicit criterion of usefulness. Preserve the segmental model's closed-character filtering and optional pretrained image features when discussing structure discovery.

**Parallel prediction versus exact generation.** Pair MEGABYTE §2.4 with [Blockwise Parallel Decoding, BIW-0082](../03_reading/R05/BIW-0082.md), §§2–4, and the [speculative-sampling originals, BIW-0083](../03_reading/R04/BIW-0083.md) and [BIW-0084](../03_reading/R04/BIW-0084.md). Local autoregression gives a dependent patch joint but retains serial local decisions. Independent proposal heads can be evaluated in parallel and accepted by longest greedy agreement; that preserves a named greedy trajectory under the specified verifier, not arbitrary sampling. Stochastic preservation instead requires proposal/target acceptance ratios and rejection-residual correction using the actual distributions. A confidence or top-k relaxation changes the policy. This packet should conclude with acceptance and measured throughput separately, naming whether the preserved target is an original backbone, a newly trained autoregressive path or an external verifier. It should not advertise all of these as the same kind of exact acceleration.

When building further packets, follow a source's version chain rather than silently pooling revisions. Transformer-XL's formal main paper and separately identified arXiv-v3 appendix remain one work, with their version boundary explicit. GPT-2's official report is not revision-pinned. Paper-level sharing belongs to the named equations, whereas a mutable configuration belongs to its inspected model/port. These distinctions make a comparison reusable: an integrator can update a specific artifact-dependent conclusion without rewriting the conceptual account or inflating the number of works.

## 6. From inventory to a long report

A useful report order is: **units and history → lexical composition → full-resolution and state-based alternatives → grouping and its learning signals → causal availability → output distributions and decoding → sharing/optimization → pretrained adaptation → multilinguality/robustness/competence → resource and evaluation methodology → open problems**. This order lets each chapter inherit explicit contracts rather than repeatedly redefine “byte model.” Place probability accounting near the first likelihood comparison and return to its algorithmic consequences in decoding; place budget conditions beside each result rather than isolating them in an appendix.

Within a chapter, organize a small comparison around one parent question, explain what each technique contributes, present the strongest relevant control and negative, then identify the residual limitation. For example, a composition chapter can compare highway-gated CNN features, contextual selected states and cross-attention pooling without ranking their unrelated benchmark numbers. A compute chapter should place ACT and sparse attention beside hierarchy, because they vary different resources. An adaptation chapter should contrast static and contextual matching before discussing distilled byte targets.

The final gap discussion should distinguish thin evidence from demonstrated failure. Current thin areas include general mixed-script causal routing, unseen-script generation, grapheme-preserving long exact copy, non-ASCII numeracy, and matched-quality batched serving with first-complete-scalar and tail latency. Classical context-mixing/compression history is selective. ACT lacks held-out byte evidence in its reported Wikipedia experiment; Reformer's largest runs lack equally large full-attention controls. These are concrete boundaries for a selected survey, not reasons to restart discovery for a larger count.

No local architecture or preferred multigranularity mechanism is required to make the field coherent. The recurring questions are coverage, useful representation, legal information flow, computation allocation, learnability, coherent output and credible evaluation. Any local-project implications belong after that independent account, if an integrator includes them at all.
