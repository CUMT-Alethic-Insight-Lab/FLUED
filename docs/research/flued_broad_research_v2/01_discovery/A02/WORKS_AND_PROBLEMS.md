# A02 — State memory: works, problems, and discriminating hypotheses

Date: 2026-11-09. Discovery record, not the final broad-report synthesis. Read alongside [coverage](COVERAGE_AND_FINDINGS.md), [search provenance](SEARCH_LOG.md), and [reading handoff](READING_HANDOFF.md).

## Identity, evidence, and classification rules

The governing question is how a native recurrent memory writes, retains, edits, and ultimately supplies useful information when the original text is unavailable. A state-space model (SSM) uses recurrent state transitions; fast weights are sequence-dependent parameters; the delta rule writes prediction error rather than an uncorrected outer product. Out-of-distribution (OOD) means a specified departure from the training distribution, not merely a longer input.

Classification is multidimensional:

- **EU**: already cataloged, original full read still missing; **PA**: recovered from the previous A02 audit but outside its main W catalog; **NEW**: absent by stable ID/title from both inspected main catalogs. These are provenance classes, not quality scores.
- **A**: original abstract/metadata; **P**: explicitly bounded original-body reading; **RF**: actual existing full-reading card read and reused, without another original-paper read. Obtaining a full HTML response does not constitute reading its entirety. No new FULL reading claim is made here.
- **C/E/T/U**: respectively capacity bound, expressibility, trainability, and deployed task use. A work can address several, with different strength. Native recall accuracy is more than a linear probe but is still not general semantic dependence.
- **S0**: no original-text revisit in the examined mechanism; **S1**: bounded recent projected updates or exact exceptions; **S2**: stored pattern/target bank. None is automatically an external original-text store; S2 is nevertheless not fixed-size compressed-state memory.

Unless a formal venue is explicitly verified below, status is **public preprint, formal acceptance not verified**. Old catalog venue labels are identified as inherited, not newly authenticated. All performance statements describe authors' reports, not replications. Fixed arXiv links identify the examined version; no cross-version equivalence is assumed.

## 1. Thirteen already-cataloged works newly recovered or reverified

### E01 — W0199: Linear Transformers Are Secretly Fast Weight Programmers

- **Source/version/status/depth:** [ICML 2021, PMLR 139:9355–9366 proceedings](https://proceedings.mlr.press/v139/schlag21a.html), officially verified; associated arXiv 2102.11174v3 is the same work, not necessarily identical text. **EU/A; T,E; S0**. Full PDF not read this round.
- **Prior problem → one-sentence solution:** additive outer products superpose incompatible associations → replace the purely additive instruction with a delta-like correction and a learned update rate.
- **Borrowed AI mechanisms and learning:** slow neural controller, key/value projections, fast-weight outer products, prediction-error update, learned learning rate and attention feature map; slow parameters learn by gradient descent, fast state is programmed during the sequence. Current content is available, future queries are not.
- **Distinguishing hypothesis/limits:** asks whether correcting a current mapping is preferable to accumulating raw features, rather than assuming more storage is necessary. The original repeated-key/nonorthogonal-key controls, normalization, state budget and synthetic failure regimes remain a priority read. Abstract superiority is not a general capacity theorem.

### E02 — W0201: Gated Delta Networks: Improving Mamba2 with Delta Rule

- **Source/version/status/depth:** [2412.06464v3 HTML](https://arxiv.org/html/2412.06464v3), 2025-03-06 version from existing version register; **EU/P**, this round §§3.1–3.2, equations and S-NIAH discussion. ICLR 2025 is inherited catalog status; venue decision not newly checked. **T,U; S0** for recurrent variant; hybrids change permissions.
- **Problem → solution:** global decay rapidly forgets useful content while ungated correction can retain too much → combine scalar decay with residual key-directed writing.
- **Mechanisms/learning/units:** `S_t = alpha S_(t-1)(I-beta kk^T)+beta vk^T`; token projections, short convolution, output gate, outer-loop next-token training and inner online regression interpretation. The residual is measured against the decayed old prediction. No future answer labels at write time.
- **Original controls and discriminant:** §3.2 distinguishes repeated synthetic haystack, essay distractors, and UUID values: decay hurts the easy retention setting, while clearance helps in realistic distractors. These are separately trained models, not a clean same-weight edit; token format, distractor load and payload difficulty differ. Tests retention-versus-filtering, not “forgetting always helps.” Appendix component ablations and full state/compute accounting remain unread.

### E03 — W0202: Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention

- **Source/version/status/depth:** [2605.22791v1](https://arxiv.org/abs/2605.22791v1), 2026-05-21, **EU/A; E,T,U; S0**.
- **Problem → solution:** one scalar edit rate ties removal of old associations to commitment of new values → separate channel-wise erase and write gates while retaining channel-wise decay.
- **Mechanisms/learning:** gated online regression/fast weights, asymmetric erase factors and chunkwise WY parallelization; language-model training of projections/gates, recurrent content update at each token.
- **Hypothesis/limits:** independent edit strengths can matter even when erase and write addresses remain linked. The abstract reports 1.3B/100B-token comparisons and multi-key RULER gains; no independent-address advantage, equal total bytes, or task-specific causal isolation follows. Compare equations against EDA, not just names.

### E04 — W0203: Dual DeltaNet: Value-Side Memory Reorganization for Linear Attention

- **Source/version/status/depth:** [2610.38578v1](https://arxiv.org/abs/2610.38578v1), 2026-10-28, **EU/A; E,T,U; S0**.
- **Problem → solution:** correcting a key's value ignores the distribution of related value features across addresses → add a value-side delta operation to key-side correction.
- **Mechanisms/learning:** Kimi Delta Attention (KDA, a channel-decayed delta-rule recurrence), value-feature selector, two-sided regression-style reads, rank-two recurrence, chunkwise training; learned token projections and end-to-end LM objective.
- **Hypothesis/limits:** tests interference involving joint key/value geometry rather than keys alone. Abstract aggregate wins and modest overhead are not proof that value reorganization preserves every old association; update-order, equal-budget ablations, long-flow stability and independent content substitutions are missing.

### E05 — W0088: Revisiting associative recall in modern recurrent models

- **Source/version/status/depth:** [2508.19029v2 metadata](https://arxiv.org/abs/2508.19029v2), 2025-10-10; [body](https://arxiv.org/html/2508.19029v2) §§3–8 read in this round, appendices not read. **EU/P; T,E,U; S0**.
- **Problem → solution:** architecture comparisons can mistake poorly tuned learning for representational inability → use finer learning-rate searches, width/depth scaling and component ablations on recall/copying.
- **Mechanisms/learning:** supervised synthetic associative binding/copying, Adam, Mamba/Hyena/attention/DeltaNet, convolution and gating ablations. Queries and training/test distributions are task-defined; no source revisit is needed for the recurrent candidates.
- **Controls/negative findings:** recurrent success occupies narrow learning-rate regions; some tuned one-layer Mamba variants recall without convolution, whereas one-layer attention fails until local construction is added. Width and depth are not interchangeable parameter matching. Three-seed figures, synthetic tasks, and unverified appendices limit generalization; “DeltaNet stabilizes because Householder mixing avoids gradient decay” is the authors' hypothesis, not an established causal theorem. Distinguishes optimization failure from immutable capacity.

### E06 — W0213: Beyond State Capacity: Why Retrieval Breaks in Mamba

- **Source/version/status/depth:** [2610.19709v1 metadata](https://arxiv.org/abs/2610.19709v1), 2026-10-14; [HTML](https://arxiv.org/html/2610.19709v1), this round targeted §§3–6, §8 discussion and Appendix B patch/probe descriptions. **EU/P; T,U,E; S0**. Not a full read.
- **Problem → solution:** query-first retrieval still fails even though only a compact answer need be retained → trace relevance through representations and gates and use controlled local flags and bidirectional gate patching to localize the bottleneck.
- **Mechanisms/learning:** pretrained Mamba, local relevance marker, linear diagnostic probes, counterfactual gate replacement, oracle gate scaling; no newly trained production architecture. The flag and oracle indices are privileged experimental information, not deployable query discovery.
- **Controls/discriminant:** replacing target-digit gates in both directions transfers performance between flagged/unflagged prompts; probe relevance appears before gates align, and critical early/middle layers precede adequate alignment. This demonstrates an actionable gating failure in the tested models, not unique necessity of one causal explanation or success of a learned repair. Gate control is not general nonlinear-memory capacity, and query-first is not unknown-future-query retention.

### E07 — W0060: Zoology: Measuring and Improving Recall in Efficient Language Models

- **Source/version/status/depth:** [2312.04927v1](https://arxiv.org/abs/2312.04927v1), 2023-12-08; **EU/A; T,U; S0/S2 by comparator**. Formal venue not newly verified.
- **Problem → solution:** easy single-query synthetic recall misses the LM gap → introduce multi-query associative recall (MQAR) and inspect recall-associated LM errors and sparse hybrids.
- **Mechanisms/learning:** supervised synthetic bindings, pretrained gated-convolution LMs, sparse input-dependent attention as a separate remedy. The attention remedy retains accessible historical representations and is not a pure fixed-state solution.
- **Hypothesis/limits:** asks which task exposes missing recall rather than generic perplexity. Abstract “82%” and “97.4%” have paper-specific denominators; original stratification and training/search budgets still need full reading. E05 is an original counterexample to interpreting an older tuning grid as an impossibility result.

### E08 — W0242: Learning to (Learn at Test Time): RNNs with Expressive Hidden States

- **Source/version/status/depth:** [2407.04620v4](https://arxiv.org/abs/2407.04620v4), 2025-08-31; **EU/A; E,T,U; S0/S1 depending on mini-batch implementation**.
- **Problem → solution:** fixed recurrent hidden representations may be too weak → make hidden state the weights of a linear model or two-layer multilayer perceptron (MLP), updated by self-supervised test-time training (TTT).
- **Mechanisms/learning:** nested learning, reconstruction/denoising-style inner supervision from current sequence views, outer learned projections/initialization; the original objective and batching need full verification. Input/query/content units are token projections, not raw source documents.
- **Hypothesis/limits:** separates a richer learned state function from a larger static vector. Abstract reports improved context-dependent perplexity and MLP memory-I/O difficulties; it does not establish long-delay exact recall, OOD query robustness, or semantic consumption. Count fast-model parameters, gradients, buffers and optimizer state, not only the recurrent tensor.

### E09 — W0234: Titans: Learning to Memorize at Test Time

- **Source/version/status/depth:** [2501.00663v1](https://arxiv.org/abs/2501.00663v1), actually submitted 2024-12-31; **EU/A; E,T,U; S0/S1 plus local attention by variant**.
- **Problem → solution:** local attention is precise but cannot itself retain arbitrarily old context → learn a neural long-term memory during sequence processing and combine it with short-term attention in three architectures.
- **Mechanisms/learning:** neural associative memory and test-time learning; gradient-surprise, momentum and forgetting are prior-audit mechanism leads whose exact equations and ablations remain to be read, not certified by the abstract. Outer LM/task training co-adapts memory and attention.
- **Hypothesis/limits:** can nonlinear memory and update dynamics improve learned retention without an original-text archive? Reported >2M needle tests do not establish high-load unknown-query exact retention, and a surprising write need not be useful to a later query. Local attention and persistent components must be budgeted.

### E10 — W0240: Hopfield Networks is All You Need

- **Source/version/status/depth:** [2008.02217v3](https://arxiv.org/abs/2008.02217v3), 2021-04-28; ICLR 2021 inherited from catalog, not newly decision-verified. **EU/A; C,E,U; S2**.
- **Problem → solution:** classical associative networks have limited pattern storage → continuous-state energy and attention-equivalent updates admit stronger retrieval/storage regimes.
- **Mechanisms/learning:** energy-based associative retrieval, softmax-like similarity, learned prototypes or stored patterns; query update can converge to a single pattern, a subset average, or a global average.
- **Hypothesis/limits:** nonlinear read dynamics can change basins and retrieval error, but exponential pattern capacity is not fixed-total-byte state capacity: patterns/keys are explicit arguments. Exact theorem separation/radius/precision assumptions remain unread. E11 supplies a practical negative control to abstract capacity rhetoric.

### E11 — W0241: Modern Hopfield Networks meet Encoded Neural Representations — Addressing Practical Considerations

- **Source/version/status/depth:** [2409.16408v2 HTML](https://arxiv.org/html/2409.16408v2), version date 2024-10-30 inherited from audit; this round §§1–3.1 and opening §3.2 read, later sections/appendix not obtained in the returned excerpt. **EU/P; U,E; S2**.
- **Problem → solution:** real correlated high-dimensional patterns create metastable mixtures despite attractive ideal capacity → encode patterns with a pretrained autoencoder before associative storage and decode after recall.
- **Mechanisms/learning:** vector-quantized/variational autoencoders, energy-based iterative cleanup, similarity/temperature selection, language-to-image heteroassociation. The pattern matrix remains stored; this is no raw-text archive but not a bounded compressed-state substitute.
- **Controls/negative findings:** §3.1 compares raw images, several encoder/decoder families, dot/L2 similarities, and kernel-memory alternatives; raw/ kernel variants can fail on 6,000-image banks. “Perfect recall” here concerns identity of stored encoded reconstructions, not exact original pixels. Separability changes, decoder distortion and bank bytes cannot be erased from the comparison. Distinguishes ideal random-pattern theorem from correlated-data usability; not yet evidence for OOD language-query generalization.

### E12 — W0232: Sharp Capacity Scaling of Spectral Optimizers in Learning Associative Memory

- **Source/version/status/depth:** [2603.26554v2](https://arxiv.org/abs/2603.26554v2), 2026-04-28; **EU/A; C,T; static training memory, not a deployment fast-state mechanism**.
- **Problem → solution:** optimizer-dependent factual recovery can be mistaken for an architecture capacity difference → characterize one-step Muon, stochastic gradient descent (SGD), and Newton recovery on a linear associative-memory model.
- **Mechanisms/learning:** Gaussian input/output embeddings, logistic loss, power-law frequency, spectral preconditioning; multi-step analysis uses a thresholded-gradient approximation.
- **Hypothesis/limits:** a fixed parameterized memory can have different early reachable capacity under different optimizers. Abstract says Muon and SGD ultimately converge to the information-theoretic limit at comparable speeds in the analyzed setting; do not convert its one-step advantage into a larger universal storage upper bound or an established online-memory recipe.

### E13 — W0086: The Key to State Reduction in Linear Attention: A Rank-based Perspective / later catalog title On State Reduction in Linear Attention

- **Source/version/status/depth:** [2602.04852v1](https://arxiv.org/abs/2602.04852v1), 2026-02-04; source history also lists v3 2026-09-29, not read as equivalent. **EU/A; C,U; S0**.
- **Problem → solution:** trained state often has low effective rank → analyze query-noise amplification and prune key/query channels with rank-revealing QR and other structured methods.
- **Mechanisms/learning:** post-training matrix diagnostics and hardware-compatible structured pruning; learned language-model state is the object, not retraining a new memory.
- **Hypothesis/limits:** distinguishes nominal tensor size from accessible effective rank. Abstract says 50% key/query channels can be removed with marginal perplexity cost; that does not imply rare exact bindings are redundant. N02 and N04 below make rank-versus-use and memory-quality comparisons more specific.

## 2. Four prior-audit candidates recovered, not newly discovered

### P01 — prior N02-1: It's All Connected: A Journey Through Test-Time Memorization, Attentional Bias, Retention, and Online Optimization (MIRAS)

- **Source/version/status/depth:** [2504.13173v1](https://arxiv.org/abs/2504.13173v1), 2025-04-17, **PA/A; E,T,U; S0/S1 by instance**.
- **Problem → solution:** architecture discussions conflate memory structure, fitting objective and forgetting → factor design into memory architecture, inner objective, retention regularization and learning algorithm.
- **Mechanisms/learning:** associative regression, non-L2 inner losses, retention regularizers, approximate online optimizers, outer-trained sequence models Moneta/Yaad/Memora.
- **Hypothesis/limits:** tests whether retaining useful state requires changing an objective/regularizer rather than adding a source store. Framework unification is not evidence that each regularizer improves long-delay retention; exact objectives, stability assumptions and equal-budget negatives remain unread.

### P02 — prior N02-2: HiPPO: Recurrent Memory with Optimal Polynomial Projections

- **Source/version/status/depth:** [2008.07669v2](https://arxiv.org/abs/2008.07669v2), 2020-10-23, **PA/A; C,E,T,U; S0**. NeurIPS 2020 status not freshly authenticated here; quote the public version rather than asserting a new venue check.
- **Problem → solution:** incremental history summaries depend on fragile timescale choices → project history onto polynomial bases under an explicit time-importance measure.
- **Mechanisms/learning:** online function approximation, Legendre projection, controlled recurrent dynamics integrated into a learned RNN; signal/trajectory and permuted-MNIST supervision.
- **Hypothesis/limits:** stable sufficient statistics may be a better target than exact-history reconstruction. Optimality is for a function-approximation objective, not arbitrary delayed facts; OOD timescale classification is not OOD key/query binding. Discretization and finite-precision robustness need original proof/experiment review.

### P03 — prior N02-3: Anatomy of Associative Recall in Fixed-State Recurrences: A Matched-State Decomposition, an Interference Wall, and a Curriculum That Breaks It

- **Source/version/status/depth:** [2609.16183v1 metadata](https://arxiv.org/abs/2609.16183v1), 2026-09-14; [HTML](https://arxiv.org/html/2609.16183v1), this round §§3.2–10 plus selected floor/rebinding text; no complete appendix/figure/table inspection. **PA/P; T,U; S0 for causal cells**; bidirectional denoisers have different query visibility.
- **Problem → solution:** load, distance, local binding and optimization are confounded → hold recurrent state at 1,024 elements in the constrained setting, toggle components and change distance curricula.
- **Mechanisms/learning:** masked synthetic MQAR, convolution/rank-one/diagonal/decay factorial, fresh random values, first-binding collision targets, supervised distance ramps, success-gated schedule; outer training only, no external text memory.
- **Controls/discriminant:** rebinding scored against the old answer defeats salience shortcuts; separate load and gap tests, learning-rate sweeps, matched-state official-kernel comparison, seed lock-in rates and state-tracking guardrail are substantive. Tuned convolution gaps are smaller than matched-LR gaps. Causal and bidirectional shaped-curriculum arms reach directional parity, countering the tempting “query-first for free” explanation.
- **Important internal conflict:** §4.2 reports no measurable decay mean effect at 20 seeds (p=.86), while §10 still calls a −.32 decay tax real; §9/§10 retain outdated length-boundary and directionality phrasing despite §6/§7 extensions. Do not quote discussion summaries over the qualified results. First-binding collision is not latest-value replacement. Companion LM/OOD claims are second-hand here and are not counted as another paper.

### P04 — prior N02-4: Erase-then-Delta Attention: Decoupling Erase and Write Addresses in Delta-Rule Linear Attention

- **Source/version/status/depth:** [2606.26560v1](https://arxiv.org/abs/2606.26560v1), 2026-06-25; [HTML](https://arxiv.org/html/2606.26560v1) obtained but only opening motivation inspected. **PA/A plus introduction; E,T,U; S0**. Author metadata use abstract page (Xiao Li first), since extracted HTML omits the first name.
- **Problem → solution:** an edit at the write key cannot independently remove a stale association elsewhere → perform a learned direction-specific erase before the ordinary delta corrective write.
- **Mechanisms/learning:** independent erase-address projection, targeted rank-one suppression, residual write, learned gates and next-token pretraining; token-granularity recurrent memory, not document navigation.
- **Hypothesis/limits:** independent addresses differ from E03's independent channel-wise strengths and E04's value-side reorganization. Abstract claims dense/MoE and long-context gains; directions, contractions, added parameters and cleanup probes require full reading. No conclusion that it knows future relevance or safely deletes all stale facts.

## 3. Nine verified new-to-inspected-catalog candidates

These IDs are local A02 references only; a central owner must deduplicate against all streams before assigning global W IDs. No new global IDs or FULL counts are assigned.

### N01 — LeapQuant: Efficient Linear Attention with Accurate Recurrent State Quantization

- **Source/version/status/depth:** [2609.38166v1 metadata](https://arxiv.org/abs/2609.38166v1), 2026-09-29; [HTML](https://arxiv.org/html/2609.38166v1), introduction, targeted §3.2, Fig.3 description and §4.4/Tables 2–3 read. **NEW/P; U/numerics; S1**.
- **Problem → solution:** recurrent re-quantization compounds rounding errors and state outliers → quantize only at window boundaries, retain recent higher-precision updates and high-precision compensator vectors, and smooth residuals.
- **Mechanisms/learning/permissions:** training-free mixed precision, low-rank outlier representation and windowed recurrence; default p=16, r=4 FP16 compensators (8 at 4-bit), FP32 scales. The buffer holds recent projected updates, not an unlimited original-text archive. It must still be charged as storage and replay work.
- **Original negatives/controls:** Qwen3.5-9B §4.4 AIME/LiveCodeBench reports FP32 87.9/64.1, per-step BF16 72.1/49.6, per-step INT8 7.1/9.2; per-window INT8 restores 82.4/60.6, then compensators/smoothing restore 87.9/64.1. Larger p=32 slows kernels without further quality gain; r=16 exposes overhead and can be slower than FP32. These are author-reported ordered additions, not all interactions of a full factorial.
- **Hypothesis/limits:** finite-dimensional geometry is not finite-precision behavior; failure can come from repeated rounding at fixed shape. Matched state MSE and long reasoning accuracy do not isolate old-fact retention, and hybrid attention can carry part of task use. 1.19 bytes/element boundary state excludes the separately charged active update buffer.

### N02 — State Rank Dynamics in Linear Attention LLMs

- **Source/version/status/depth:** [2602.02195v1](https://arxiv.org/abs/2602.02195v1), 2026-02-02; **NEW/A; U/diagnostics; S0**.
- **Problem → solution:** state size obscures head-specific dynamics → characterize low/high effective-rank groups and propose joint rank-norm pruning.
- **Mechanisms/learning:** singular-spectrum diagnostics, head probes/ablation and zero-shot pruning of pretrained models; rank patterns are reported as acquired during pretraining.
- **Hypothesis/limits:** low rank need not mean low importance: abstract claims low-rank heads are indispensable for reasoning and high-rank heads redundant. This directly warns against discarding low-energy heads by generic capacity intuition. Causal specificity, norm/rank interactions, original task suite and persistent-state versus attention-KV accounting remain unread.

### N03 — Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling

- **Source/version/status/depth:** [2609.36529v1](https://arxiv.org/abs/2609.36529v1), 2026-09-29; **NEW/A; E,T,U; S0**.
- **Problem → solution:** larger matrix states can require costly projection/parameter growth → write key × second-key × value into a third-order state and read with two query contractions.
- **Mechanisms/learning:** tensor-product binding, delta/forget gates and chunkwise parallelization; token projections learned by LM training.
- **Hypothesis/limits:** parameter-efficient expansion and factorized addressing might allocate capacity differently from wider heads or more matrices. An E-dimensional second key multiplies state by E; extra capacity is not free or equal-total-byte evidence. Need same-state, same-query-function and same-training comparisons, not a “3D beats 2D” class claim.

### N04 — SPARE: Fast Linear Attention Decoding with Compact Recurrent States

- **Source/version/status/depth:** [2611.07552v1](https://arxiv.org/abs/2611.07552v1), official v1 history **2026-11-05** (search result displays Nov 6); [HTML](https://arxiv.org/html/2611.07552v1), §§1–6, theorem statement and Appendix B implementation/accounting text inspected; no independent code, graph digitization or proof audit. **NEW/P; U/numerics; S0**.
- **Problem → solution:** dense recurrent state traffic persists despite fixed-length memory → operate in a fixed key subspace, allocate heterogeneous per-head ranks and compensate projected write strength.
- **Mechanisms/learning:** training-free key principal-component analysis (PCA), state-spectrum budget allocation, bounded inverse projected-norm compensation, packed GPU state kernels; calibration on model inputs, not future answer labels. Online states remain FP32.
- **Original controls/negatives:** pure 1.3B GDN, 24×8 heads, key/value width 256; compares coordinate pruning and uniform ranks at matched recurrent-state bytes without recovery fine-tuning. At 12 MiB, reported retrieval 60.35% versus coordinate-pruning 33.20%; compressed models still degrade relative to Dense. Uniform ranks can give slightly better NLL at small budgets; some coordinate-pruned points win on individual tasks. Four-choice synthetic retrieval is 512 prompts, with ablations at depths 64/128, not arbitrary long unknown queries.
- **Hypothesis/limits:** preserving dominant spectral energy is neither sufficient nor necessary for exact content. The exactness theorem assumes every key stays in the fixed subspace; real calibration/OOD shift violates that premise. Shared bases, convolution state and workspaces sit outside per-request recurrent-state numbers. Peak batch-512 speedups do not establish continuous-serving throughput or general memory capacity.

### N05 — Kronecker Delta Rule for Long Context Linear Attention (KronLSTM)

- **Source/version/status/depth:** [2610.26834v1](https://arxiv.org/abs/2610.26834v1), 2026-10-19; [HTML](https://arxiv.org/html/2610.26834v1) introduction/Fig.1 motivation only inspected. **NEW/A plus introduction; E,T,U; S0**. An indexed OpenReview same-title lead exists, but official forum/PDF is challenge-blocked; **no ICLR 2027 status or cross-version identity certification**.
- **Problem → solution:** a delta update can perturb associations sharing a key → revise a single matrix-space direction so interference depends on both key and value overlap.
- **Mechanisms/learning:** Kronecker-product association, rank-one matrix-space revision, Markov-chain/steady-state analysis, end-to-end LM training. Norm-boundedness is an author theoretical claim under unread assumptions.
- **Hypothesis/limits:** memory editing geometry rather than raw state expansion may reduce collateral damage. A bounded expected norm does not guarantee every finite-precision trajectory, low-probability binding or OOD query. Need nonorthogonal key/value controlled data and direct comparison to E04's two-sided edit before choosing a mechanism.

### N06 — Longhorn: State Space Models are Amortized Online Learners

- **Source/version/status/depth:** [2407.14207v1](https://arxiv.org/abs/2407.14207v1), 2024-07-19; versions through v5 exist but are not read here. **NEW/A; E,T,U; S0**. It was cited inside W0229's existing card, but had no standalone entry in either inspected catalog; this is recovery of a missing work entity, not discovery of an unknown idea.
- **Problem → solution:** ad hoc recurrence design hides its optimization assumptions → derive an implicit online-regression update and amortize it as an SSM layer.
- **Mechanisms/learning:** implicit/proximal online learning, quadratic regression, learned token-dependent projections and outer sequence-model training.
- **Hypothesis/limits:** stable conservative updates may differ from explicit delta-SGD at identical functional state. W0229 already interprets the mechanism; newly verifying Longhorn does not count that interpretation twice. Full original key correlations, changing targets and costs remain unread.

### N07 — RWKV-7 “Goose” with Expressive Dynamic State Evolution

- **Source/version/status/depth:** [2503.14456v2](https://arxiv.org/abs/2503.14456v2), 2025-03-30; **NEW/A; E,T,U; S0**.
- **Problem → solution:** efficient recurrence needs richer dynamic transitions → generalize delta updates with vector gates, in-context rates and relaxed value replacement.
- **Mechanisms/learning:** gated fast/matrix state, trainable token mixing and multilingual LM training, regular-language/state-tracking analysis.
- **Hypothesis/limits:** expressible sequential algorithms can differ without extra source permissions. “Recognize all regular languages” and a conditional circuit-complexity comparison do not mean unlimited random-fact storage, learned exact retrieval or greater bit capacity. Compared model training tokens/data differ; no controlled claim that the update rule alone causes multilingual performance is made.

### N08 — Dense Associative Memory for Pattern Recognition

- **Source/version/status/depth:** [NIPS 2016 official proceedings version](https://proceedings.neurips.cc/paper/2016/hash/eaae339c4d89fc102edd9dbdb6a28915-Abstract.html), formal proceedings verified; associated arXiv 1606.01164 is not an additional work. **NEW/A; C,E,U; S2/learned pattern representation**.
- **Problem → solution:** classical associative pattern storage and recognition are limited → use higher-order energy interactions and a duality with unusual feedforward activations.
- **Mechanisms/learning:** energy-based memory, rectified high-degree polynomial features, feature-matching/prototype interpolation; XOR and MNIST are the abstract's example evaluations.
- **Hypothesis/limits:** nonlinear associative computation is an independent alternative to linear state rules, but the count of neurons is not a total parameter/bit budget. No original-text archive is required; stored prototypes/interactions still cost memory. Full basin/capacity assumptions and online trainability remain unread.

### N09 — Gated Fast Weights for Associative Retrieval

- **Source/version/status/depth:** [official OpenReview PDF HJ8W1Q-0Z](https://openreview.net/pdf?id=HJ8W1Q-0Z), unnumbered PDF headed **“Under review as a conference paper at ICLR 2018”**, anonymous authors; **NEW/P**, extracted §§1–6 and limitations, numeric table cells/curves not fully recovered. Final venue decision/version date unknown. No attempt to identify authors. **T,U; S0**.
- **Problem → solution:** fast-weight programs can learn only trivial outputs on complex sparse query supervision → generate an elementwise gate and candidate weight matrices separately, blending the new program with the old one.
- **Mechanisms/learning:** slow recurrent controller, fast recurrent network, outer-product gate/candidate, post-activation layer normalization, shared embedding/output, one-step delayed writes to discourage a slow-path prediction bypass; truncated backpropagation with Nadam.
- **Original negatives/controls:** §4 reports earlier feedforward/recurrent fast-weight variants failed to predict nontrivial outputs despite searches; all-token accuracy is misleading because blanks dominate, so nonblank partial accuracy/BPC is reported. Keys 2–4 symbols, single-symbol values, 1–10 writes per query; training unroll 32, batch 256. A common chosen LR across models follows initial searches, not tuning-invariant proof.
- **Hypothesis/limits:** trainable memory and useful memory differ even in the original fast-weight lineage; gating, normalization and forcing use may change learnability. §§5–6 explicitly report backward storage of all changing matrices and substantial wall-time overhead. No general extrapolation to modern LM OOD query use.

## 4. Nine actual existing full-reading cards reused — no new reading count

The linked cards themselves were read in this round. Their declared FULL scope is not independently recertified; limits and version choices are retained. The metadata/status below are inherited from those cards unless stated otherwise. These works are not part of the 26 recovered/new public-source work entities above.

| Existing identity, source, version and actual card | Prior problem → one-sentence solution; borrowed mechanisms and learning | Evidence depth, permissions, discriminant and limitations |
|---|---|---|
| **W0229**, *Test-time regression: a unifying framework for designing sequence models with associative memory*, [2501.12352v3](https://arxiv.org/html/2501.12352v3), 2025-05-02; [B06 card](../../../flued_multigranularity_survey_20261108/03_reading/B06/W0229.md); public preprint, venue unverified | Correlated key statistics and update rules are conflated → factor weighting/function class/optimizer; least squares, Gram inverse, recursive least squares (RLS), SGD, kernel regression; slow projections learned, causal prefix updates | **RF; S0** for parametric branches, S2 for nonparametric. Card §§3–6/App.A includes nonstationary negative result: unweighted global RLS adapts poorly after a switch. Original MQAR construction/orthogonal embedding assumptions retained. Distinguishes covariance correction from more state and adaptation from retention. |
| **W0212**, *A Geometry-Based Capacity Theory for Finite-Feature Associative Memory*, [2610.09056v1](https://arxiv.org/html/2610.09056v1), 2026-10-06; [B06 card](../../../flued_multigranularity_survey_20261108/03_reading/B06/W0212.md); preprint | Fixed additive storage confounds finite-feature noise with key overlap → model both and include value Gram geometry; random Fourier features and Hebbian writes, no end-to-end LM learning | **RF; C; S0** matrix. Exact stored-key queries, cosine output, fixed update; not delta/noisy query/finite-precision theorem. Appendix F negative controls: value rotation alone no gain, learned orthogonal addresses not reliably better than direct noisy MLP. Distinguishes update-specific geometry from universal capacity. |
| **W0245**, *Sharp Capacity Thresholds in Linear Associative Memory: From Top-1 Retrieval to Tail-Average Learning*, [2605.05189v2](https://arxiv.org/html/2605.05189v2), 2026-08-19; [B21 card](../../../flued_multigranularity_survey_20261108/03_reading/B21/W0245.md); preprint | All-pair top-1 and list retrieval impose different demands → derive sharp thresholds in a Gaussian linear-scoring model; optimized matrix, margin/statistical analysis | **RF; C; S2** complete target bank available for scores. Fixed-fraction list is not fixed-small-k; data-chosen matrix is not learned native reader. Existing proof caveats remain, no theorem certification. |
| **W0061**, *Repeat After Me: Transformers are Better than State Space Models at Copying*, [2402.01032v2](https://arxiv.org/abs/2402.01032v2), 2024; [B04 card](../../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md); formal venue not newly checked | Post-query uniform exact copying overloads bounded state → count distinguishable states and compare attention constructions; synthetic copy training | **RF; C,E,T,U; S0 vs accessible history**. Whole-string error, uniform source, single pass and true finite state; safe bound is nonstrict success ≤ state-count/string-count. Query-first successes and repeated-n-gram failures are material controls. Card's formal construction cautions not erased. |
| **W0217**, *Atlas: Learning to Optimally Memorize the Context at Test Time*, [2505.23735v1](https://arxiv.org/pdf/2505.23735v1), 2025-05-29; [B16 card](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0217.md); preprint | One-pass regression underfits recent associations → repeatedly optimize a neural memory on a causal recent-KV window; inner regression and spectral optimization, outer LM training | **RF; E,T,U; S1**, recent KV plus optimizer buffers. Card flags proof rank-step/independence quantifier doubts; not a verdict of total theorem falsity. Atlas recall mean 43.70 vs Transformer 53.55 in cited table; not uniformly superior. Distinguishes nonlinear function class, replay and optimizer effects. |
| **W0204**, *MoM: Linear Sequence Modeling with Mixture-of-Memories*, [2502.13685v4](https://arxiv.org/pdf/2502.13685v4), 2025-11-18; [B16 card](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0204.md); preprint | All writes interfere in one state → route to a sparse subset of matrices, leave unselected states unchanged; top-k learned routing and balance loss | **RF; T,U; S0**. Shared same-step write/read route plus always-updated shared state, not arbitrary independent readers. Active-state matching is not total-state matching; repeated-key cross-slot consistency untested. Some tasks degrade. |
| **W0214**, *RAM-Net: Linear-Time Sequence Modeling with Sparsely Addressable State*, [2602.11958v2](https://arxiv.org/pdf/2602.11958v2), 2026-10-06; [B16 card](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0214.md); preprint | Large state accesses are costly and aggregated writes collide → independent top-k read/write addresses over a fixed array; factorized addresses, LM training | **RF; T,U; S0**. Total 26.2M state elements vs GDN 8.5M at cited scale, not equal total bytes. Some difficult needles fail; balancing write addresses can harm (S-NIAH-2 83.7→11.3 in cited ablation). Tests address alignment/collision, not free capacity. |
| **W0352 / BIW-0025**, *MambaByte: Token-free Selective State Space Model*, [2401.13660v3](https://arxiv.org/html/2401.13660v3); [B14 actual card](../../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md); COLM 2024 inherited | Long byte streams are expensive → byte-level selective recurrence plus optional subword drafting; next-byte LM | **RF; T,U; S0** recurrence. Approximate per-byte FLOPs/exposure, fixed-state byte feasibility and robustness do not prove long exact recall. Drafting has extra model and top-3 acceptance is not exact target-law preservation. |
| **BIW-0108**, *Decoupling the Benefits of Subword Tokenization for Language Model Training via Byte-level Simulation*, [2604.27263v2](https://arxiv.org/pdf/2604.27263v2), 2026-05-14; [R08 actual card](../../../byte_language_interface_survey/03_reading/R08/BIW-0108.md); preprint | Tokenization bundles several interventions → simulate input capacity, grouping, hints, positions and targets separately in a byte-resolution LM; temporary curricula, n-gram lookup, CE | **RF; T,U; byte cross-axis control**, not new native-memory evidence. Four-byte training changes exposure AND target density; temporary subword head has negative outcomes and transition confounds. Borrow intervention separation, not a proven recurrence cure. |

Other previous-audit cards (W0207/W0237 bounded exact exceptions; W0208/W0210 snapshots/multiple states) remain valid leads with prior-audit status only; they were not reread or counted here. Their titles are not promoted into fresh evidence records.

## 5. ICLR 2027 leads: deliberately unverified, outside the 26 verified-work set

The official [group](https://openreview.net/group?id=ICLR.cc/2027/Conference) rendered only a loading shell; forum fetches returned a browser-verification wall. Search snippets are navigation, not venue verification. No reviews, decisions, complete abstracts, author identities or accepted status were certified. These are **search leads**, not evidence of a mechanism's success.

| Indexed title / official URL | Exact version and status | Potential problem / solution / borrowed mechanism from snippet only | Missing discriminant |
|---|---|---|---|
| *Kronecker Delta Rule for Long Context Linear Attention*, [forum 2XDUbuZOTH](https://openreview.net/forum?id=2XDUbuZOTH) | Forum/PDF blocked; indexed date 2026-09-16 is not a verified version. Same-title relationship to N05 pending | Targeted edits / Kronecker memory revision | Verify official group, submission identity/version and decision state before merging forum with arXiv; no author crosswalk |
| *DeltaTTT: Layerwise Optimization for Nonlinear Recurrent Memory*, [jFQZrrDREJ](https://openreview.net/forum?id=jFQZrrDREJ) | Blocked; indexed submission/date only; no acceptance inference | Nonlinear-memory optimization / layerwise TTT, mechanism details unknown | Does it solve nested optimization rather than add capacity? Need actual original objective/controls |
| *When Does Momentum Help Online Associative Memory …*, [jGFgYdNkmI](https://openreview.net/forum?id=jGFgYdNkmI) | Blocked; title truncation retained; version/venue status unknown | Momentum versus delta / optimizer-state memory, exact method unknown | Is any advantage due to an extra state tensor, a distribution assumption or trainability? |
| *CHARTA: A Recurrent Language Model with Routed …*, [QvfwNCiyPg](https://openreview.net/forum?id=QvfwNCiyPg) | Blocked; exact complete title/version/status unknown | Routed delta-rule state / conditional memory writes, snippet only | Same total state versus same active state? Unknown |
| *Fast Residual Memory for Test-Time Training of Latent …*, [JvQYIoQxQ0](https://openreview.net/forum?id=JvQYIoQxQ0) | Search lead only, not fetched; exact full title/version/status unknown | Residual writes plus learned gates / delta-rule fast state, snippet only | Task domain, causal visibility, original controls unknown |

Not a systematic ICLR 2027 census: one targeted web query, no venue pagination, four directly blocked forums. No anonymous submission is deanonymized by matching public author lists.
