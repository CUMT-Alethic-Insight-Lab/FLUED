# Open questions: evidence already available and what would settle the remainder

## 1. Purpose and evidence classes

This agenda accompanies [SURVEY_EN](SURVEY_EN.md), not a proposed implementation or an authorization to run experiments. It distinguishes three kinds of open item:

- **Research comparison:** existing evidence motivates a question, but a controlled or deployment-relevant experiment is still needed.
- **Artifact or specification closure:** the paper has been read; a named algorithm branch, metric pipeline, population, or preprocessing contract remains unknown. Another broad reading batch or training run is not the appropriate default remedy.
- **Thinly sampled outcome:** the corpus contains related mechanisms but insufficient direct evaluation of the desired behavior. Missing evidence is not a measured failure.

The survey's evidence base contains 141 entities, 296 traceable records, and 92 distinct scoped FULL sources, with two additional intentional narrow historical extractions. Those counts do not certify software, independent effects, or every outcome below. Stable BIW/BIP identifiers and source versions remain unchanged; [CLAIM_RULES](../05_review/CLAIM_RULES.md) governs the affected claims.

## 2. Research comparisons

<a id="oq01"></a>
### OQ-01. Can a cheap causal policy learn incremental computational value?

**What is known.** BLT chooses patches using a separate causal entropy model; SOMBRERO learns observed-next-byte confidence targets; utility and novelty studies use loss-layout or future-repetition signals. ACT earlier allocates within-byte effort and shows that effort traces need not track immediate uncertainty. The controlled SOMBRERO ladder attributes much gain to smoothing, while utility policies improve selected forced-prefix targets without comparable free-generation success ([survey §§5–6](SURVEY_EN.md#s06); [BIP-0054](../02_inventory/DETAILED_INVENTORY.md#BIP-0054), [0156–0157](../02_inventory/DETAILED_INVENTORY.md#BIP-0156), [0162–0163](../02_inventory/DETAILED_INVENTORY.md#BIP-0162), [0289](../02_inventory/DETAILED_INVENTORY.md#BIP-0289)).

**What remains unestablished.** This selected corpus does not establish a general cheap prefix-only policy that estimates the marginal benefit of an extra expensive update across tasks, languages, and domains. Whole-layout loss differences are not clean single-boundary effects, and confidence enrichment is not task utility.

**Experiment needed.** Compare rules, own/separate-model uncertainty, observed-target training supervision, and direct value labels under matched realized rates, local/trunk capacity, retained text, and tuning budgets. Use single-added-update interventions where feasible, with held-out task utility rather than only boundary enrichment. Test forced-prefix intermediates and free generation separately; transfer the policy to new domains without silently changing its training boundary distribution.

**Deciding evidence.** A value policy should improve held-out quality at matched complete cost, or reduce measured cost at predeclared quality, without unstable rates or worst-group regressions. Failure on one domain would delimit that policy, not prove utility learning impossible.

<a id="oq02"></a>
### OQ-02. Are gains due to boundaries, aggregation, or contextual capacity?

**What is known.** DTP averages completed character spans; H-Net selects contextual states; BLT uses attention aggregation; MEGABYTE concatenates fixed patches. H-Net's XL two-stage system improves reported average accuracy to 58.2% from BPE's 55.5% at 0.69 GFLOPs/byte, against a strong space control at 57.1%/0.70 and with unequal parameter counts. That positive system result does not isolate layout from aggregation or capacity ([survey §6.4](SURVEY_EN.md#s06)). DTP's mean/endpoint comparison and H-Net's alternative aggregators occur under different encoders and budgets. MANTa needs a capacity bottleneck to avoid near-byte-rate grouping ([BIP-0010](../02_inventory/DETAILED_INVENTORY.md#BIP-0010), [0026](../02_inventory/DETAILED_INVENTORY.md#BIP-0026), [0152–0154](../02_inventory/DETAILED_INVENTORY.md#BIP-0152)).

**Experiment needed.** Cross fixed/rule/learned layouts with mean, contextual endpoint, concatenation/projection, and attention operators in a shared backbone. Match realized length distributions, not merely target mean rate. Hold local receptive field and representation width explicit. Include changed-boundary tests for repeated spellings, exact identifiers, and group-edge positions.

**Deciding evidence.** A boundary-quality effect requires a layout advantage that survives the same operator and rate; an aggregation effect requires benefit under the same layout. Exact reconstruction or copying must be measured independently of next-byte loss. This would explain compatible existing findings rather than force them into a universal pooling ranking.

<a id="oq03"></a>
### OQ-03. What is the best allocation among positions, edges, state, and depth?

**What is known.** Full-resolution dense models, sparse attention, Reformer, selective recurrence, fixed latent arrays, grouping, and ACT change different resources. Sparse Transformer's strided pattern is cheaper by its iteration quantity but worse in BPB; ACT's byte result is training-only and near-tied; reversible activations address training memory rather than inference KV ([survey §5](SURVEY_EN.md#s05)).

**Experiment needed.** Construct complementary equal-retained-text and equal-complete-compute comparisons, tuning each family within an equal search budget. Separately vary stored state, attention connectivity, expensive-update frequency, and within-position depth. Measure training memory, original-text context, task quality, and serving rather than infer all from asymptotics.

**Deciding evidence.** A Pareto frontier over quality, training time/memory, and matched-workload serving would establish operating regimes. No single scalar should collapse those resources. ACT needs held-out byte evidence before any modern byte-quality benefit is credited to its adaptive-depth route.

<a id="oq04"></a>
### OQ-04. When does transient refresh pay for freshness?

**What is known.** Scratchpad Patching refreshes an observed partial patch without adding permanent states. At p=16, NLU rises 48.0→54.2 while the validation-FLOP saving factor shrinks 5.7×→2.9×. Some patchifier or dense-refresh conditions regress ([BIW-0076](../03_reading/R05/BIW-0076.md), v1 §§3–5/Appendix E; [BIP-0105–0107](../02_inventory/DETAILED_INVENTORY.md#BIP-0105)).

**Experiment needed.** Compare fixed refresh schedules and learned/entropy triggers at matched training and inference cost, preserving the same committed layout. Include partial prompts, varying output lengths, batched request arrivals, and cache pressure. Record transient workspace and trigger-model work as well as persistent KV.

**Deciding evidence.** Freshness should improve matched-quality request cost or a declared latency target once scheduling overhead is included. Smaller persistent state alone does not settle it. A trigger that helps long exact dependencies but not average likelihood could still be useful if that outcome is predeclared.

<a id="oq05"></a>
### OQ-05. Can dependent drafts remain cheap enough to be useful?

**What is known.** Local AR preserves block dependence with serial local sampling. Independent heads propose cheaply but may combine incompatible alternatives. MtPC introduces normalized circuit dependence, yet head sizes and higher-rank sampling can reverse acceptance-based expectations. LCA also loses throughput with more candidates in a reported condition ([survey §8](SURVEY_EN.md#s08)).

**Experiment needed.** Sweep head structure, rank, candidate length, shared/private layers, and batch under a fixed target model and actual cache implementation. Separate greedy matching, exact stochastic correction, and approximate confidence policies. Include EOS and prefill rather than only fixed-length continuation.

**Deciding evidence.** Compare request-level speed and peak resident memory at matched target law or explicitly matched task quality. Report accepted bytes per cycle together with drafting, verification, rejection, and cache costs. The MtPC wrapper-law item below must be resolved before labeling its optimized stochastic arm exact.

<a id="oq06"></a>
### OQ-06. Which sharing and readout choices help small alphabets?

**What is known.** Large-vocabulary word/subword tying supplies background, not a byte-specific verdict. Byte literature includes tied and untied specifications on different axes. One-hot byte NMT reveals a dropout interaction; row normalization, cosine scale, and dimensional rank arguments have distinct implications ([survey §10](SURVEY_EN.md#s10); [BIP-0139](../02_inventory/DETAILED_INVENTORY.md#BIP-0139), [0184–0199](../02_inventory/DETAILED_INVENTORY.md#BIP-0184)).

**Experiment needed.** Within one byte model, compare tied, untied, and transformed readouts at matched contextual capacity and complete parameter convention, with separately tuned learning rates/scales. Match token-erasure semantics, not just dropout probabilities. Measure path-specific gradient norms, calibration, strict likelihood, and downstream behavior over several independent runs.

**Deciding evidence.** A benefit should survive tuning and semantics controls and name the actual matrix axis. Static specifications should be checked against trained aliases if storage claims depend on them. Normalized-head algebra motivates the experiment but cannot substitute for it.

<a id="oq07"></a>
### OQ-07. What must checkpoint conversion preserve, and at what adaptation cost?

**What is known.** Char2Subword separates static imitation from frozen-host contextual training. Bolmo aligns after four layers and benefits from a stage whose removal is not catastrophic; another token-to-byte recipe has a severe direct-distillation control. Cross-tokenizer byte supervision can lose instruction behavior, and an intermediate token-output stage is not a complete byte conversion ([survey §11](SURVEY_EN.md#s11)).

**Experiment needed.** Cross static/contextual/logit alignment and freezing schedules within the same host, retaining original pretraining as an inherited resource. Match conversion bytes and global work in separate views. Evaluate original general tasks, instruction following, new surface tasks, and output validity after each actual interface transition, not only a final average.

**Deciding evidence.** Successful conversion should preserve a predeclared behavior set at lower total adaptation cost or add new capability without unacceptable losses. A vector-distance decrease or retained backbone parameter correspondence is insufficient. Host-specific negatives are informative rather than grounds for a universal staging rule.

## 3. Thinly sampled user-facing outcomes

<a id="oq08"></a>
### OQ-08. Can mixed-script routing remain genuinely online?

**Available evidence.** MAGNET changes per-script rates but assumes one script for the sequence. Character-aware code-mixed understanding and broad multilingual byte tasks do not establish prefix-only mixed-script generation. MYTE leaves an unseen script uncompressed even while compressing English.

**Needed evaluation.** Use naturally mixed scripts and controlled insertions, explicitly distinguishing scripts absent from tokenizer induction from scripts absent from model training. Test prefixes ending inside UTF-8 scalars, rapid script switches, borrowed names, numerals, and punctuation. Trace every preprocessing feature to the observed prefix and compare worst-group quality at matched retained context.

**What would settle it.** A fixed-artifact streaming argument plus direct generated-task evidence and measured rate/cost distributions. A single-script selector's absence of a mixed-script test is not proof that all byte routing fails ([survey §12](SURVEY_EN.md#s12)).

<a id="oq09"></a>
### OQ-09. Do coverage and local loss translate to exact multilingual strings?

**Available evidence.** Byte fallback can remove unknowns without preventing translation collapse. Partial UTF-8 progress can greatly exceed strict validity. The finite-state counting bound concerns deterministic copying begun only after ingestion of a uniform random string, with all input-dependent influence on later output contained in the counted retained state. It excludes source replay, uncounted external caches, output written during ingestion, and any other side channel outside that state. Natural-language redundancy changes the source distribution; online echoing changes the protocol. Attention maps and probe decoding are not generated long-copy measurements.

**Needed evaluation.** Generate long natural multilingual spans and random controls with source substitution/removal, query-before/query-after conditions, distractors, and boundary offsets. Declare whether answers begin after ingestion and count every retained source/cache or output channel; arms permitting replay or external access require their own storage, access, and pass budgets rather than inheriting the state-only bound. Score exact original bytes, complete legality, intended scalars, and an additional task-authorized canonical/grapheme equivalence. Log raw outputs before repair and classify incomplete termination separately.

**What would settle it.** Whole-string success curves against original-text distance and persistent-state cost, with clean floors and several seeds. This directly tests fidelity without presupposing rereading or external memory as the preferred remedy ([BIP-0063–0065](../02_inventory/DETAILED_INVENTORY.md#BIP-0063), [0235](../02_inventory/DETAILED_INVENTORY.md#BIP-0235)).

<a id="oq10"></a>
### OQ-10. Does finer access improve character algorithms and numeracy?

**Available evidence.** SpellingBee shows recoverability and a bounded null initialization result; Strawberry accelerates supervised learning without demonstrating mastery; CharBench separates counting from position. Non-ASCII arithmetic is thinly covered.

**Needed evaluation.** Factor representation access, explicit character training, general LM training, and output alphabet. Include same-task subword baselines with matched augmentation. Separate transcription from arithmetic, vary carry-chain length and grouping direction, and add non-ASCII digits, locale separators, combining sequences, and explicit index units. Publish chance/majority floors and parser failures.

**What would settle it.** Improvements in generated task accuracy under matched budgets, not only probe readability or earlier crossing of a very low onset threshold. Report whether the benefit transfers to natural instructions and unseen forms ([survey §12.7](SURVEY_EN.md#s12)).

<a id="oq11"></a>
### OQ-11. What does a user experience under batched byte serving?

**Available evidence.** Existing studies mix training step times, FLOP estimates, fixed-length batch-one continuations, uncached verification, and weight-traffic proxies. Modern matched-quality concurrency, first-complete-scalar, and tail-latency evidence is limited.

**Needed evaluation.** Fix hardware/precision and task quality; replay prompt/output distributions with several batch/concurrency settings. Include preprocessing, all resident teachers/drafters/verifiers, prefill, EOS, partial prompts, Unicode buffering, rejection, and repair. Measure request p50/p95 or another predeclared tail percentile, first byte, first complete scalar, stable displayed unit, total throughput, and peak resident memory.

**What would settle it.** An end-to-end frontier on the workload, not accepted bytes or theoretical update count. Distinguish throughput optimization from interactive latency; one may improve while the other worsens ([survey §13](SURVEY_EN.md#s13)).

## 4. Artifact and specification closure: no new training implied

<a id="oq12"></a>
### OQ-12. Does MtPC's optimized stochastic wrapper preserve its named target law?

**Already supported.** The v2 circuit is normalized, Algorithm 3 specifies ordinary residual correction, and reported throughput is a measured observation under its stated device/batch/prefill/EOS conditions.

**Still open.** Algorithm 2's partial-acceptance branch does not clearly distinguish optional all-accepted bonus from required post-rejection correction or specify retained residual state.

**Finite-prefix diagnostic.** Suppose the first proposal is deterministic and accepted, and at the next position p=(.5,.5), q=(.9,.1). Accepted mass is min(p,q)=(.5,.1), with rejection probability .4. Proper residual correction contributes (0,.4), recovering (.5,.5). Discarding that correction and restarting an ordinary target-law cycle instead contributes .4p=(.2,.2), producing (.7,.3). This is an analyst counterexample to the specified discard-and-ordinary-restart interpretation, not released-code execution. Retained residual state or another equivalent correction protocol could avoid it; retained accepted-prefix hidden state alone does not specify that protocol.

**Closure evidence.** Immutable code and paper-run linkage; all zero/partial/all-accepted branches; emitted outputs and retained probability/cache state; actual transformed p/q; finite-prefix probability argument. Until then say optimized stochastic exactness is unverified, not that software is broken. Timings are not invalidated by association ([CLAIM_RULES §3](../05_review/CLAIM_RULES.md#3-mtpc-exact-source-level-qualification-not-a-software-verdict)).

<a id="oq13"></a>
### OQ-13. What computation produced TokSuite Figure 6?

**Already supported.** V2 C.2 prints CE/log₂|V|, which is not general bits-per-original-byte conversion. Separately inspected trainer files log token CE, but they do not identify every plotting transformation.

**Still open.** The actual run→log→plot computation and provenance. Wrong explanatory wording does not prove the figure executed that formula, and a reviewer-supplied correct formula does not repair the original figure.

**Closure evidence.** Immutable plot/evaluation code; raw field/log base; effective scored labels and matching original-byte totals; EOS/PAD/prompt/overlap treatment; language/example weighting and smoothing; run-to-figure mapping. Until then do not use Figure 6 to certify equality or sufficient training. Separate option ranking, the four-tokenizer text control, and the Gemma-only exact-byte side evaluation retain their own status ([CLAIM_RULES §4](../05_review/CLAIM_RULES.md#4-toksuite-exclude-an-unverified-figure-inference-not-the-whole-study)).

<a id="oq14"></a>
### OQ-14. How do MYTE's reported evaluated populations and aggregates relate?

**Already settled.** Table 8 columns are low-resource then overall: MyT5 21.1/21.8 and ByT5 21.9/23.1. The transcription correction needs no new full read. Main Table 4 separately gives MyT5 20.4 versus ByT5 20.1 on its low-resource summary.

**Still open.** Run/population/aggregation linkage, including C.2's fourteen names against fifteen columns and Maltese/Shona versus Marathi naming. Parallel-English-byte normalization remains different from target-byte BPB.

**Closure evidence.** Named evaluated language lists and run IDs for each table, raw per-language metrics, aggregation weights, and explicit score/log/normalization contract. Do not average tables or select a preferred sign. An author/artifact explanation, not new model training, is the first remedy ([CLAIM_RULES §5](../05_review/CLAIM_RULES.md#5-myte-explicitly-anchor-both-model-row-and-aggregate-column)).

<a id="oq15"></a>
### OQ-15. Are actual boundary and preprocessing features prefix-stable?

**Already supported.** Causal masks do not certify upstream preprocessing. Generic BPE examples refute universal prefix stability; the actual Llama guide, right-shifted BPE control, and AU-Net regex were not thereby measured to leak.

**Closure evidence.** Name an immutable tokenizer/regex and exact feature construction, including specials and end-of-input behavior. Give a prefix argument or exhaustive finite-rule reasoning where possible; pair it with adversarial extension tests at actual merge/regex boundaries. Identify any delayed decision or permitted buffering. Runtime traces should be linked to the claimed experiment if empirical causality depends on them.

**Boundary of the conclusion.** Training-only future labels can validly teach a prefix-only policy. Actual held-out full-string side information is a different permission. Missing proof is not a software verdict; a toy counterexample is not a leak-rate estimate ([survey §7](SURVEY_EN.md#s07)).

## 5. Prioritization and stop rules

| Priority class | First action | Completion criterion | What not to do |
|---|---|---|---|
| Existing guarantee needed for a headline | Resolve OQ-12–15 with named artifacts/specifications | The exact affected branch/event/population is documented | Restart broad discovery or infer runtime from a FULL label |
| Mechanism attribution | OQ-01–07 under matched realized controls | The proposed cause survives its strongest alternative explanation | Compare unrelated literature averages as one experiment |
| Missing user-facing outcome | OQ-08–11 with direct generated/serving tests | A predeclared outcome and resource frontier is measured | Call absent evidence a demonstrated failure |
| Coverage expansion | Add a source only for a missing mechanism or decisive control | Identity, scope, and new evidential role are explicit | Increase paper counts as an end in itself |

The existing selected corpus is sufficient for the long survey; these questions are not a requirement to postpone it until every unknown disappears. Whole-source reading, implementation verification, statistical identification, and experimental reproduction are different tasks. An unreported field can remain unreported, a theoretical assumption can remain conditional, and a narrow historical extraction can remain narrow. The research value lies in choosing the smallest decisive evidence for the question actually being asked.
