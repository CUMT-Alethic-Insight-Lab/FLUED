# Compression, task sufficiency, and native state memory

**English synthesis A/B · 9 November 2026 · evidence-bounded research comparison**

## 1. Scope and principal judgments

Compression and state maintenance are first-class research fields, not preliminary obstacles on a path toward source retrieval. The central questions are what information a representation must preserve, what an update actually retains or changes, and whether a trained native consumer can use the retained content. A model may fail because its objective rewards the wrong distinctions, its writes interfere, precision degrades, its legal query is inadequate, or its decoder prefers another path. These explanations imply different remedies.

This chapter owns the original **A.01–A.20**, **B.01–B.22**, and relation-comparison **R.11** directions. It preserves the six-axis organization: A compression/task sufficiency; B writing/retention/capacity; C addressing/native reading; D deployed use/causal measurement; E learning dynamics; F composition/host transfer. C–F enter where they distinguish an A/B explanation, rather than being absorbed into a single storage-to-use sequence. The authoritative coordinates come from the [167-direction list](../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md); §11 maps every owned member individually.

The evidence base comprises V01–V03/V10–V11, selected V06/V08/V09/V16–V18 cards, and version-scoped legacy cards. Their original reading scopes and the [reading audits R1](../05_review/READING_AUDIT_R1.md), [R2](../05_review/READING_AUDIT_R2.md), [original-scope audit](../05_review/ORIGINAL_SCOPE_AUDIT.md), and [coverage recheck R2](../05_review/COVERAGE_RECHECK_R2.md) govern interpretation. This synthesis reads and compares those cards; it does not claim new full-paper readings, replication, or independent proof certification. A source ambiguity is identified at its particular equation, protocol, or edition, not promoted into theorem refutation.

Five judgments organize the comparison:

1. **Sufficiency is relative to tasks, queries, readers, and loss.** Reconstruction, continuation, and answering later questions need not retain the same distinctions. None has an unconditional priority.
2. **Unknown-query exactness and bounded-task compression are compatible topics.** A finite state cannot losslessly encode unlimited independent random detail, while a bounded predictive task can admit a compact sufficient statistic.
3. **Writing rules impose different editing policies.** Addition accumulates evidence; residual writing corrects a present association; decay removes broadly; directional erase changes selected subspaces. Their benefits depend on whether old or new content should remain true.
4. **Capacity, precision, reachability, and consumption require different evidence.** A large matrix, low effective rank, successful oracle read, and good native task accuracy are four different observations.
5. **Several no-revisit alternatives remain credible.** Objective repair, protected exact payloads, covariance-aware writes, partitioning, legal query adaptation, nonlinear fast memory, and predictive-state learning should compete before any architecture is selected. Source-enabled methods compete under their additional access and cost contract.

## 2. What a sufficient representation promises

### 2.1 Specify the experiment before choosing a loss

Let history or context be \(C\), the representation produced before a later query be \(Z=E(C)\), the query be \(Q\), and the required answer be \(Y\). A useful comparison declares the task distribution, loss, query timing, retained channels, permitted reader family, and optimization opportunity. Prediction sufficiency concerns whether \(Z,Q\) support the relevant conditional answer distribution, not whether a reconstruction looks fluent. Exact reconstruction asks for all original distinctions; retrieval may ask for a particular binding; continuation may emphasize common local dependencies.

The query timing is substantive. A writer that already knows a requested identifier can filter a long stream for that identifier. A writer that must later answer any identifier cannot use the same filtering privilege. Query-last evaluation with unseen examples from an unchanged generator also differs from evaluation on new query families, such as relational joins after training only exact lookups.

[W0080](../../flued_multigranularity_survey_20261108/03_reading/B24/W0080.md), **2608.14528v1, §3 and Appendix D**, makes this contract explicit. Its finite-equivalence-class bit result assumes a fixed task, countable histories, deterministic encoding, and a common exogenous subsequent-input distribution. Its state includes accessible external files, not just the short prompt. In its independent-fair-bit example, writing before the randomly selected query has an information requirement that query-visible writing avoids. These are conditional results about all retained channels, not a recommendation to use external files or a universal language compression rate.

### 2.2 Task invariance can justify forgetting—and exclude a later task

[W0059](../../flued_multigranularity_survey_20261108/03_reading/B04/W0059.md), **2106.10800v5, §§3.2–3.3 and Appendix B.3**, first chooses an input equivalence relation. Its task family consists of predictions invariant within those equivalence classes. Under the stated countability, finite-entropy, log-loss, and asymptotic coding conditions, a maximal invariant characterizes the worst remaining task information. This gives a principled no-revisit route: discard distinctions the promised task family does not need.

A later question about a detail erased by that equivalence relation lies outside the promise. For example, an augmentation that removes a serial-number digit cannot support a theorem about later exact serial-number questions merely because it preserves object category. The useful conclusion is to expose the invariance contract and test its deployment relevance. The legacy card's Appendix B.5–B.6 restrictions remain: its reported local issues in extensions to arbitrary losses and mean-squared error do not invalidate the separately supported log-loss argument.

[BR-A01-R04](../03_reading/V01/BR-A01-R04.md), **2203.07004v2, §3, Tables 1–4**, supplies an empirical counterweight to aggressive invariance. Own-view reconstruction or an information incentive improves some visual transfers after contrastive training; reconstruction also hurts supervised CIFAR100→DTD transfer, 36.06% to 34.79%. Retaining more information can preserve private task signal or preserve nuisance. Those table values belong to the fully read arXiv v2; the formal CVPR edition's bearing tables remain incompletely aligned.

### 2.3 Available information is not the deployed consumer

[W0092](../../flued_multigranularity_survey_20261108/03_reading/B13/W0092.md), **2002.10689v1, §§2–4**, defines usable information through optimal log-loss within a specified predictive family. A deterministic preprocessing can make existing information easier for that family to extract without creating new Shannon information. This supports reader-side repair as a real alternative to increasing storage. It does not imply that a particular trained model reaches the family optimum.

[W0091](../../flued_multigranularity_survey_20261108/03_reading/B04/W0091.md), **2009.12789v2, §§2–3 and Appendices B–C**, similarly ties representation quality to a decoder family and known labels. Its exact generalization statements require strong finite-space, deterministic-label, family-closure, and exact-optimum assumptions; the card records tensions in the literal closure and bounded-loss conditions. Its conceptual contribution survives without importing an unconditional guarantee for ordinary softmax networks.

Accordingly, an A/B study should report separately: task information recoverable by a diagnostic reader; performance of an equal-permission trained reader; the native returned content; final answer dependence on that content; and task correctness. A successful stronger reader rules out complete loss for the tested targets under that reader's permissions. Failed readers alone do not prove information-theoretic loss. A correct native return can still be bypassed, redundantly used, or overridden under a source-authority policy.

## 3. Compression objectives, decoder non-use, and learning

### 3.1 Problem → solution → AI technique inventory

The table compares mechanisms, not a leaderboard. Each row states the supervision and consumer contract that makes its evidence relevant.

| Original problem | Proposed solution and borrowed AI technique | Learning, visibility, and retained object | Decision-bearing evidence and strongest limitation |
|---|---|---|---|
| Reconstruction may prioritize the wrong downstream distinctions | **W0067**: task-aware rate allocation using multitask information bottleneck, Gaussian rate–distortion analysis, and hard-bit encoders | Encoder knows a weighted task suite but not the task selected for a particular read; empirical downstream probes are newly fitted | [2610.30493v1, §§2–6, Apps. B–F](../03_reading/V01/W0067.md): common/moderate-precision versus rare/high-precision priorities reverse with rate. Task suite, Gaussian conditions, and fitted-reader risk are not arbitrary-query sufficiency. |
| Reconstruction pretraining may be unnecessary for a particular compression interface | **SAC / BR-A01-R02**: select contextual semantic anchors, add a learned anchor embedding, retain their layerwise KV; borrow LoRA and KV prompting | Bidirectional context compression, continuation pretraining and supervised QA; frozen decoder; growing per-layer KV | [2510.08907v4, Table 5 p.7, Table 20 p.23](../03_reading/V01/BR-A01-R02.md): LM-only beats mixed SAC on reported QA, but mixed wins QMSum and 500x comparisons are mixed. Not a universal reconstruction penalty. |
| A frozen LLM needs a readable compressed context | **ICAE / W0038**: learned memory tokens and encoder LoRA; mix reconstruction and continuation | Query-unaware context encoding, subsequent question at the decoder; instruction tuning adds teacher-generated data | [2307.06945v4, §3.2, Tables 3–5](../../flued_multigranularity_survey_20261108/03_reading/B24/W0038.md): mixed pretraining beats either single objective in that setup; random content reconstructs poorly; independently compressed segments need additional composition training. |
| Full hidden-state reconstruction may preserve irrelevant coordinates | **Compressive Transformer / W0023**: reconstruct attention responses instead; borrow FIFO memory, convolution, and stopped-gradient auxiliary training | Future queries unknown when old states enter compressed FIFO; recent fine-state cache remains | [1911.05507v1, §3.2, Table 5 p.6](../../flued_multigranularity_survey_20261108/03_reading/B24/W0023.md): attention reconstruction has favorable reported bpc; compression ratios and BPTT budgets differ across selected rows. Current-query response fidelity is not every future-query fidelity. |
| Finite-context LMs need longer usable history | **AutoCompressors / W0037**: train recurrent soft summaries with continuation loss and truncated backpropagation | Consumer adapts; all older summaries remain in forward context; summary count grows | [2305.14788v2, §3, Tables 1–5 pp.5–8](../03_reading/V01/W0037.md): useful long-context tradeoffs, but full attention wins some comparisons. Two-step gradient truncation does not imply two-step memory retention. |
| A document embedding is not directly usable by an LLM | **xRAG / W0055**: multimodal-style projector, document-generation pretraining, answer loss, and full-text teacher distillation | Frozen retriever and host; question after document embedding; persistent external index; one vector per retrieved document | [2405.13792v2, §§3,6, Tables 1–4 pp.6–9](../03_reading/V01/W0055.md): bridge training helps averages, with task reversals and weaker multi-hop boost. One token is neither one bit nor a fixed whole-corpus state. |
| Final-layer gist aggregation may omit accessible features | **ComprExIT / BR-A01-R08**: learned cross-layer mixing and Sinkhorn transport into slots | Question-unaware mode plus QA supervision; frozen feature extractor; local 128-token transport windows | [2602.03784v4, Tables 1–3 p.7, Table 8 p.17](../03_reading/V01/BR-A01-R08.md): stronger QA averages and useful allocation ablations; relation extraction loses to ICAE, optimization differs, and entity coverage is not binding preservation. |

[T05 / 2607.22334v1, §§3–4, Appendix C](../03_reading/V17/BR-R2-T05.md) sharpens A.16: byte-mediated distillation changes the supervision law, not representation sufficiency. Conditional refinement exactness, mass conservation, and realized-path lower bounds differ. Its whitespace ablation harms code while math remains stable (§5, Fig.3 pp.8–9); locally matched teacher targets can damage task function. Teacher scoring, masking and stopping belong in the objective comparison.

The SAC–ICAE comparison matters because both favorable and unfavorable reconstruction evidence exists. Their differences include carrier type, bidirectional access, decoder adaptation, data, stage doses, and rate. A synthesis that chooses one objective from either headline would discard the contrast that needs explanation. A direct experiment should fix the interface and compare objective × realized rate × consumer adaptation, with actual training exposure and compute reported separately.

W0067 adds a reason not to freeze that ranking even inside one task suite. Its controlled Gaussian example makes common, moderate-precision information attractive at low rate and rare, high-precision information worthwhile at higher rate. Its positive fixed-pretext result also survives: a task-informed pretext can have bounded regret under bounded task-information conditions. The paper therefore supports rate-sensitive design, not permanent objective instability or a universal reconstruction baseline.

Its empirical rate axes deserve particular care. Appendix F.1 Table 1 reports a Gaussian crossover around **16.8 nominal bits** and a hard-code crossover around **21.2 bits/image**. They are different experiments and quantities. A finite-sample entropy estimate capped by the number of test examples is not the physical payload of a 32-bit code. Separately fitted probes measure a particular accessible risk, not the Bayes-optimal task risk assumed in theory.

### 3.2 Decoder non-use has several mechanisms

An expressive autoregressive decoder may model local regularities without a latent. That observation does not identify whether the objective permits non-use, inference updates lag, deterministic reconstruction is difficult, or the consumer fails to integrate useful content.

| Mechanism hypothesis | Original intervention or analysis | Positive and reversing observations | Transfer boundary |
|---|---|---|---|
| The scalar objective does not identify useful latent allocation | [Broken ELBO / BR-A01-R03](../03_reading/V01/BR-A01-R03.md), formal ICML 2018, §2, Fig.4 p.8, supplement D | Equal ELBO can accompany different rates and reconstruction; a target-rate toy recovers known latent structure. Similar ELBO is not equal reconstruction, and the target rate uses privileged knowledge. | Stochastic variational models, not a theorem about deterministic recurrent non-use. |
| Decoder context makes the latent optional | [BIW-0095](../03_reading/V10/BIW-0095.md), 1702.08139v2, Table 2 p.5 | Yahoo field-15 CNN has KL 13.3 but worse NLL than field-125; field-187 nearly loses latent benefit. Initialized Yelp wide decoder is worse than the LM. | Word-based whole-document VAE; receptive field, depth, capacity, initialization, and dropout co-vary. |
| Training information or schedule changes latent incentives | [BIW-0094](../03_reading/V10/BIW-0094.md), 1511.06349v4, §§3–6, Tables 2–5 | KL annealing and word dropout help avoid zero-KL behavior; inputless VAE beats inputless RNN, not the ordinary strong RNN. More dropout can increase KL while degrading likelihood. | Weakening decoder training information is a treatment, not a cost-free representation improvement. |
| Local decoder factorization allocates global versus local detail | [VLAE / BR-A01-R15](../03_reading/V10/BR-A01-R15.md), 1611.02731v2, §§2–4, Tables 1–5 | Local autoregression can encourage global latent structure; plausible lossy examples sometimes lose semantics, and CIFAR likelihood trails PixelCNN++. | Image texture allocation does not identify which short exact language exceptions may be discarded. |
| Approximate inference cannot track the changing generator | [Lagging Inference / BIW-0096](../03_reading/V06/BIW-0096.md), 1901.05534v2, Algorithm 1, Tables 1–4,9 | Extra early encoder steps improve reported VAE outcomes; wall time is roughly 2.2–3.7× basic training, and slow annealing wins some single-run likelihood cells. | An inference-lag hypothesis with added compute; not a universal writer-extra schedule. |
| Deep autoencoder optimization itself is difficult | [BR-A01-R17](../03_reading/V10/BR-A01-R17.md), formal ICML 2020, §§3–5, supplement §§1–4 | Deterministic and variational depth sweeps degrade; annealing does not eliminate every problem. The source's local-minimum argument and unbounded comparator require careful separate interpretation. | Image models, equal updates rather than equal FLOPs; source proof-scope concerns are not theorem falsification. |

Expected posterior/prior KL is not a direct measure of task content: it includes aggregate-posterior mismatch. Higher KL can accompany worse likelihood, while better likelihood can coexist with latent non-use. Conversely, some strong decoders do use useful latents. The relevant intervention changes content identity under controlled legal context, rather than merely driving KL upward.

The dedicated linear-landscape original **BR-A01-R16 / 1911.02469v1 remains body-blocked** in its [actual card](../03_reading/V10/BR-A01-R16.md). This chapter therefore does not import its theorem from its title. R17 and Broken ELBO support bounded alternatives to a lag-only explanation; exact R16 geometry remains a source gap.

### 3.3 Continuous codes, discrete codes, and scalarization

[VQ-VAE / BR-A01-R09](../03_reading/V10/BR-A01-R09.md), **1711.00937v2, §§2–4**, uses nearest-neighbor codebooks, straight-through gradients, commitment loss, and a separately learned prior. Constant categorical KL under a uniform prior removes one training pressure; it does not ensure task-relevant code use. Its CIFAR bound is worse than the continuous VAE comparator, and a supervised code-to-phoneme mapping is a post-hoc readout. Compare actual payload, entropy, dead codes, estimator, reader, and exact-content outcomes—not “discrete avoids collapse” against unmatched continuous vectors.

[W0013](../../flued_multigranularity_survey_20261108/03_reading/B24/W0013.md), **2512.21913v1, §§II–III**, adds learned gates and variable-length quantized units. Its lossless text fallback checks the source at encoding time; this is not later recovery of an omitted original. Equal vocabulary and equal achieved compression are different comparisons. It supplies a staged-tokenization example, not a staged-versus-joint causal verdict.

[W0064](../03_reading/V10/W0064.md), **1808.07593v4, §§3–4, Appendix B**, shows another distinction: with deterministic labels and unrestricted stochastic bottlenecks, the usual linear information-bottleneck scalarization need not trace all desired frontier points. The squared penalty addresses that particular geometry. It is not evidence that useful compressed states cannot exist, nor that estimated information coordinates alone select an architecture.

## 4. Exact detail, binding, order, and relations

### 4.1 Retention must be tested on distinctions, not semantic plausibility

Rare details, high-entropy identifiers, exceptions to a common rule, and rare output targets are different difficulty factors. A common identifier can have high entropy; a rare fact can be predictable from a template. A low-frequency output token can be difficult for the decoder even when the state preserves its identity. A clean test independently varies occurrence frequency, entropy, answer-token frequency, and task importance, holding rate and reader opportunity fixed.

ICAE's ordinary-text reconstruction versus structured-random and fully random failures is a useful anchor, not a complete exact-detail benchmark. Teacher-forced reconstruction also supplies earlier target tokens; it can look strong while the required later query needs a discarded binding. Measure exact strings separately from fluent paraphrase and semantic answers. Include unseen values, not only familiar names whose properties can be supplied from model parameters.

Binding and order require stronger contrasts than changing a bag of words. Preserve the same entities and values but permute which entity has which value, reverse a relation's roles, or alter within-segment order with boundaries fixed. Query both the original and changed association. If a representation tracks all values but not their assignments, a value inventory probe can succeed while the promised answer fails. Cross-segment composition needs its own training and test contract: ICAE's initially failed independent-segment concatenation shows that locally readable codes do not automatically compose.

### 4.2 Relation arity, reused relational content, and persistent identity

A relation can involve two or more arguments; a model can feed a relational result into later processing; a system can preserve a separately identifiable relation instance with roles and provenance. These are different capacities. Inference steps, network layers, object count, and state tensor order are additional dimensions. The [cross-axis ownership packet](../02_catalog/CROSS_AXIS_OWNERSHIP.md) assigns this distinction to A under R.11.

| Source and exact edition | Problem → solution → technique | What is actually represented and learned | Positive evidence and missing discriminating comparison |
|---|---|---|---|
| [W0542 / Relation Networks](../../flued_multigranularity_survey_20261108/03_reading/FINAL_RELATION/arxiv_1706.01427.md), 1706.01427v1, §§2,4–5, supplements A–F | Pairwise reasoning → shared pair function plus pooled readout → relational inductive bias | Question-conditioned ordered object pairs are summed; task supervision trains the encoder/readout | Strong CLEVR result; no independently addressed persistent edges. This is a necessary strong ordinary binary baseline, not a proof that pooling cannot compose relations. |
| [W0541 / Multi-layer RN](../../flued_multigranularity_survey_20261108/03_reading/FINAL_RELATION/arxiv_1811.01838.md), 1811.01838v1, §§2–3, Table 1 | Single pair aggregation may miss multi-step structure → compare per-object relation aggregates in another layer | Relation-bearing summaries become later inputs; individual pair identities were already pooled | Better two/three-fact tasks, but 4M versus 6M updates, added parameters and changed regularization. No isolated objectification effect. |
| [W0538 / Abstractors](../../flued_multigranularity_survey_20261108/03_reading/FINAL_RELATION/arxiv_2304.00195.md), 2304.00195v4, §§2–4, Fig.2(e), App.C | Sensory features may obscure abstract comparisons → relation cross-attention with symbol values | Repeated RCA layers retain original-object Q/K; feeding an Abstractor output into another Abstractor is a separate proposed interface | Useful sorting and math evidence; no dedicated net-effect experiment for Fig.2(e). Sensory bypass remains in math. |
| [W0537 / Relational Convolutions](../../flued_multigranularity_survey_20261108/03_reading/FINAL_RELATION/arxiv_2310.03240.md), 2310.03240v3, §§2–4, App.B Fig.13 | Compare relational patterns → groupwise relation templates, then use group vectors as later objects | Learned grouping and task labels support relations between relation-pattern summaries | Positive match-pattern and held-out-card-set results; deeper ordinary baselines are explored, not a fixed-resource arity×depth factorial. |
| [W0540 / Neural Logic Machines](../../flued_multigranularity_survey_20261108/03_reading/FINAL_RELATION/arxiv_1904.11694.md), 1904.11694v1, §2, App.B Table 4, App.D | Learn finite relational rules → expand/reduce tuple predicates with shared MLPs | Breadth is maximum predicate arity; depth is derivation layers; supervision includes curriculum and some auxiliary labels | Object-count generalization and trained rule tasks; varying task configurations do not isolate arity. Training graduation rates are incomplete, and no relation-instance lifecycle is supplied. |
| [W0539 / Slot Abstractors](../../flued_multigranularity_survey_20261108/03_reading/FINAL_RELATION/arxiv_2403.03458.md), 2403.03458v2, §§2,4, App.A | Scale visual relational reasoning → object slots plus relational attention and self-attention | Frozen or adapted visual slots, positional cues, candidate-answer scoring | Useful sample efficiency, but some full-data/held-out-combination results lose to baselines. Removing self-attention also removes feedforward work. |
| [W0543 / Dual Attention](../03_reading/V16/W0543.md), 2405.16727v3, §§2–4, App.B, Table 2 p.21 | Separate sensory and relational signals → concatenate ordinary and relational heads | Learned pair-comparison vectors and sender symbols are pooled; later layers can compare relation-bearing inputs | Positive nested-pattern and LM results, with competing methods and task reversals. No independent persistent relation IDs; grouped-query/symbolic components and compute also change. |

The strongest useful comparison keeps one fact pool and separately changes relation arity, relation-result reuse, inference depth, and retained-object identity. Include a tuned flat binary model, ordinary deeper attention/readout, and the proposed relation interface at matched information access and full resource budgets. Use role collisions and value-bag-matched bindings, followed by held-out relation compositions. Explicit provenance or revocation belongs in the test only if persistent relation identity is part of the promise. Existing evidence supports relational inductive biases and composition mechanisms; it does not require a new relation-object architecture for compression.

Tensor state is a separate issue. [Triadic Linear Attention](../03_reading/V09/BR-A02-N03.md), **2609.36529v1, §2**, binds a value to two learned keys. Flattening their tensor product yields a larger joint-key matrix representation; nothing assigns those axes semantic relation-instance identity. Its higher-order state belongs primarily to the capacity-allocation comparison below.

## 5. Native writing is an editing policy

### 5.1 Addition, residual correction, and covariance

Use a value-by-key state \(M\) so the read is \(Mq\). Additive writing uses \(M^+=M+vk^\top\). A residual update instead uses

\[
M^+=M+\beta(v-Mk)k^\top.
\]

It reads the current prediction at the write key and corrects toward the new value. For unit keys, the immediate change at another query is

\[
\Delta(Mq)=\beta(v-Mk)(k^\top q).
\]

This elementary identity explains both the attraction and the limitation: orthogonal addresses avoid collateral change from this substep; correlated ones do not. Repeated identical keys with latest-binding truth favor correction, while first-binding truth can make that same correction destructive. An erase mechanism needs a definition of stale content before erasure quality can be assessed.

[W0199](../03_reading/V02/W0199.md), **2102.11174v3, §4.2 and Appendix B**, supplies the foundational residual-writing example and its orthonormal-key preservation condition. [W0228](../03_reading/V11/W0228.md), **2406.06484v6, §§2–3 and Appendix B**, makes the recurrence practical through WY/UT factorization and triangular solves. This changes the computation schedule, not ideal capacity. It preserves the chosen input-conditioned recurrence in real arithmetic; finite-precision agreement is a separate question.

[W0229](../../flued_multigranularity_survey_20261108/03_reading/B06/W0229.md), **2501.12352v3, §§3–4**, separates regression weights, function class, and optimizer. An exact linear least-squares memory uses both key–value cross-statistics and the key Gram matrix; additive linear attention corresponds to dropping a covariance correction, while one-sample residual writing is not the full-prefix optimum. Better covariance treatment is therefore a native no-revisit alternative. Its unweighted recursive least-squares comparator also adapts poorly after a process change (§5): retaining all past evidence optimally under one weighting can be the wrong policy under nonstationarity.

### 5.2 Write/forget/erase mechanisms compared

| Problem | Solution and AI technique | Native operation and learned signal | Evidence, cost, and counterexample |
|---|---|---|---|
| Addition repeatedly reinforces an already fitted binding | **W0199 / W0228**: delta correction; online least-mean-squares and chunk factorization | Input-derived K/V/Q and learned strength; current key reads old value before correction; next-token outer loss | [W0199 §6, Apps.B,D](../03_reading/V02/W0199.md); [W0228 Table 1 p.8](../03_reading/V11/W0228.md). Rebinding helps; feature map, normalization, convolution and state expansion matter. FAVOR+ update failures and task losses survive. |
| Targeted correction cannot rapidly clear an entire obsolete state | **GDN / W0201**: combine scalar decay with delta writing | Decay old state, correct at current key, read updated state; short convolutions, output normalization and gate remain | [2412.06464v3, §§3–4, Table 2, App.B](../03_reading/V02/W0201.md). At 8K passkey DeltaNet/GDN are 98.8/91.8; at 4K essay-number 18.6/92.2. Task-dependent ranking, not isolated semantic filtering. |
| Write and overwrite strengths are tied | **GDN-2 / W0202**: independent channel gates; local proximal-style objective | Channel decay; erase read uses a channel-reweighted key; write direction remains the original key; next-token learning | [2605.22791v1, §3, Tables 4–5 pp.8–9](../03_reading/V02/W0202.md). Channel scalarization hurts selected averages; erase range expansion is not uniformly useful. FP32 state and convolution/hybrid caches count. Not a freely independent erase address. |
| Stale content may lie away from the new write address | **EDA / BR-A02-P04**: learned directional erase before delta | Decay → erase along projected normalized e → correction along k → native read; erase and write generally do not commute | [2606.26560v1, §3.3 Eq.8, §4.5 Fig.2](../03_reading/V02/BR-A02-P04.md). Useful task averages, but older raw-key recall favors KDA; small local perturbation does not prove useful stale-fact removal. Extra substep/projections and full-attention hybrid paths remain. |
| Key-side correction does not explicitly reorganize value-feature distribution | **Dual DeltaNet / W0203**: add value-side correction; two-sided associative memory | Value-selected read follows key correction; its read is not a guaranteed inverse semantic address | [2610.38578v1, §3, Tables 3,5–6 pp.7–9](../03_reading/V02/W0203.md). Average gains coexist with essay-number regressions and slower reported prefill+decode. Two updates, selector and coupled tiling add work. |
| Correlated observations need history-dependent correction geometry | **Bayesian Layers / W0226**: Kalman-style mean and covariance | Learned input-conditioned auxiliary dynamics/noise; innovation updates memory mean using covariance-directed gain; q reads updated mean | [2605.31163v5, §2, Apps.B–G](../03_reading/V03/W0226.md). Strong constructed high-overlap stress, but supplied read keys, unequal tuning and extra dense covariance. Model-based optimality is conditional, not real-world uncertainty calibration. |

These are genuinely different interventions. Independent strengths do not equal independent addresses; selective erase does not equal global decay; value-side reorganization does not equal an invertible relation store. A learned projection's weak cosine with the write key is descriptive geometry, not evidence that it targets the right obsolete fact.

Bayesian Layers makes a particularly informative distinction. Under its linear-Gaussian design model, the posterior mean and covariance are sufficient for its specified regression problem. Resetting predicted covariance to an isotropic matrix recovers a delta-shaped update while discarding accumulated geometry. Testing dense, diagonal, and reset covariance on a common stream can therefore locate a mechanism. It must charge \(D^2\) covariance state, FP32 arithmetic, and chunk history. Its layerwise teacher-fitted conversion and ordinary continued-training comparator differ in exposure, objective, and trainable modules; they cannot establish a clean transplant coefficient.

### 5.3 What should remain true after a conflicting write?

Three truth policies expose different failures:

- **First binding:** a later mention is distractor or misinformation; protect the original.
- **Latest binding:** a later event is a legitimate update; correct the original.
- **Context-tagged binding:** both versions are valid under different time, role, or source tags; retain enough information to answer the requested version.

Addition, residual correction, and erasure should be compared on all applicable policies. Querying only the newest binding can conceal destruction of useful neighbors; querying only old keys can penalize legitimate updates. After every controlled conflict, score the corrected association, unrelated old associations, near-key associations, and explicitly tagged historical associations. A multi-state solution additionally needs a consistency policy when the same identity routes to different states.

Prediction error is also not future relevance. An unusual but useless string can generate a large residual; a familiar relation can become essential only after a later question. Error-driven memory is a plausible learning signal, not a measured value-of-retention oracle.

## 6. Retention, interference, and late relevance

### 6.1 Separate time, writes, and load

A long sequence changes several variables simultaneously: elapsed update steps, number of distinct associations, total writes, similarity of distractors, repeated conflicts, and distance from training lengths. To distinguish mechanisms, keep an association fixed and vary these axes independently. A no-write interval tests persistence without new interference; equally long unrelated writes add load; near-key writes probe crosstalk; repeated conflicting writes probe truth policy. If the actual recurrence always decays on every token, “no write” must specify whether its transition/decay still executes.

[W0212](../../flued_multigranularity_survey_20261108/03_reading/B06/W0212.md), **2610.09056v1, §§III–V and Appendices B–F**, analyzes a narrower but useful case: fixed additive outer-product storage queried at the exact stored key. For orthogonal values, squared key-kernel overlaps determine the returned-value cosine; finite random features add another approximation term. With correlated values, the value Gram matrix can amplify or cancel interference. Thus correlated keys are not a universal no-storage theorem. The result concerns finite features, not finite arithmetic precision, and does not cover arbitrary noisy semantic queries or trained delta writes.

Its Appendix F countercontrols matter: rotating orthogonal values does not create capacity, and learned orthogonal addressing or sparse synthetic codes do not have general advantage in the reported comparisons. Better-looking key geometry alone is insufficient. The experiment should independently manipulate key overlap and value overlap, keeping semantic truth and output discrimination fixed.

### 6.2 Trainability can reverse a benchmark diagnosis

[Zoology / W0060](../03_reading/V11/W0060.md), **2312.04927v1, §3 and Appendix E**, improves the measurement of multi-query recall with fresh key–value bindings and varied query positions. Its real-text rare-bigram slice is 6.4% of validation tokens; the reported 82% concerns a weighted log-loss-gap statistic, not 82% of all mistakes or a causal allocation of language ability. Its finite-state indexing argument requires explicit bit precision when translated from matrix elements.

[Revisiting / W0088](../03_reading/V03/W0088.md), **2508.19029v2, §2 and Appendix A**, finds strong sensitivity to learning rate, width, depth, and components. A parameter-matched 150M Mamba copying comparison changes from 16% to 100% under a different width/depth layout. That success refutes the particular observed failure as an unavoidable consequence of parameter count; it does not erase finite-bit limits. The reported program exceeds 3,000 runs and roughly 20,000 GPU-hours, so best-tuned accuracy and tuning efficiency should both be visible. Complete grid and copy-metric details remain reporting gaps.

[Anatomy / BR-A02-P03](../03_reading/V03/BR-A02-P03.md), **2609.16183v1, §§4–7, Tables 1–7**, adds within-cell controls, rebinding, first-binding collisions, and curriculum success rates. A success-gated length-512 curriculum reaches 6/6 reported successes where the time ramp reaches 0/6. Those lengths are trained, not extrapolated. Matched recurrent elements exclude some local history, and a reverse masked stream can see a query before the haystack. The source's expanded decay comparison is approximately .561 versus .518, p=.86, while §10 retains an older −.32 claim; the [R1 source check](../05_review/READING_AUDIT_R1.md) confirms this same-version conflict. Use the experiment-specific result rather than silently choosing rhetoric.

These studies preserve multiple causes: inadequate capacity, difficult binding formation, sparse supervision, local feature construction, and fragile optimization. A fair comparison uses the same generator and exam stream, equal per-arm search opportunity, complete failed seeds, and explicit training versus extrapolation lengths. A successful curriculum is evidence for reachable task solutions under that curriculum, not unrestricted memory.

### 6.3 Depth-late relevance is not time-late relevance

[W0213](../03_reading/V03/W0213.md), **2610.19709v1, §§3–6 and Appendix A**, studies query-first phonebook retrieval. Relevance becomes linearly separable earlier than the relevant gates; target-digit gate interventions can break or rescue performance. The interventions use the known locations of all ten answer digits. A separate state probe uses professions, not the same ten-digit task.

This is informative evidence for a mismatch between available relevance and native gating under a query-first contract. It neither trains a deployable target detector nor solves retention when relevance is unknown until after writing. For genuinely time-late relevance, reveal the question after the same history has been encoded, randomize which previously mundane fact matters, and include semantic reformulations and joins. Query-first, query-last, and an oracle relevance flag should be separate arms. Shifted semantic/query-family retention remains a substantive evidence gap, not a deficit repaired by additional exact-key titles.

## 7. Bits, precision, rank, and memory layout

### 7.1 A finite-bit bound and its legitimate alternatives

For uniform independent length-\(L\) strings over \(D\) symbols, a deterministic one-pass system with \(|S|\) possible post-input states can correctly reproduce at most \(|S|\) different complete strings. Hence whole-string success is at most \(|S|/D^L\), capped by one. [W0061](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md), **2402.01032v2, §2 and Appendix D**, gives this counting argument. Its safe non-strict error inequality should be used rather than the source's strict boundary wording.

This is a useful restriction, not a reason to reject compact native memory. A bounded set of likely questions, compressible natural data, approximate answers, known task statistics, growing state, or query-first filtering changes the promise. Retaining a pattern bank or original KV changes the total state/access contract. Nonlinear fast weights do not escape finite-bit counting if every history-derived channel is included. Conversely, finite real-valued dimension is not a finite-bit budget until precision and representable states are specified.

### 7.2 Precision and subspace efficiency interventions

| Intervention | What it changes | Actual evidence and costs | What remains to test |
|---|---|---|---|
| [LeapQuant / BR-A02-N01](../03_reading/V03/BR-A02-N01.md), 2609.38166v1, §3, Tables 1–3, App.B | Reduce repeated state quantization using a low-bit boundary, recent higher-precision updates, low-rank compensators, and smoothing | Useful hybrid-model quality recovery. Reported 1.19 bytes/state element excludes about 8 KiB/head/layer active update buffer for the stated 128×128 state, plus refitting/workspace. Four-bit results degrade. | Separate precision from requantization frequency and extra retained records; test long-delay native binding, not only quality averages. |
| [LinQuant / BR-A08-V23](../03_reading/V09/BR-A08-V23.md), 2610.39418v1, §§2–3, Apps.B–F | Function-preserving rotations/scalings and factor redistribution improve quantizer operands | Controlled carry is FP32 with an INT8 read copy; production prefill has a different low-precision contract. Gram solves remain FP32. Some transformations require commuting decay and correctly transformed initial state. | Repeated low-bit carry and decode, not prefill alone; verify the target host's decay, convolution, and normalization respect the transformation conditions. |
| [SPARE / BR-A02-N04](../03_reading/V03/BR-A02-N04.md), 2611.07552v1, §3, Tables 1–2, App.A | Project state onto calibrated key subspaces and allocate ranks heterogeneously | Conditional exactness requires every key in the retained span. Dense retrieval 70.51% becomes 56.84%/60.35% for H32/H64. Bases, convolution state and workspace are outside quoted per-request state. | Rare low-energy directions, shifted queries, and compensation at fixed basis/rank; score exact content and full service bytes. |
| [W0086](../03_reading/V09/W0086.md), 2602.04852v3, §3, Apps.A,F–G | Slice Q/K and convolution channels using calibrated rank-revealing QR, optionally recover with adaptation/distillation | Stable-rank evidence supports spectral concentration, not unused facts. Recovered GDN WikiText improves while LAMBADA and RULER worsen; batch-1 speedup is much smaller than batch-64. | Task-sensitive preservation versus spectral energy; equal adaptation and full live-state accounting, including hybrid compensation. |

A low-energy direction can encode a rare critical distinction. High spectral energy can represent common redundant content. Effective rank, matrix rank, condition number, empirical code entropy, and physical bytes should therefore be separate columns, not interchangeable capacity measures.

### 7.3 One state, many states, heads, and slots

[MoM / W0204](../../flued_multigranularity_survey_20261108/03_reading/B16/W0204.md), **2502.13685v4, §3, Tables 4,6 and Appendices C,G**, partitions writes across selected states plus an always-updated shared state. The same routing determines active writes and reads. A shared query reads the mixture; linearity makes mixing before versus after reading equivalent. Matching active state does not match all resident states, projections, and routing. Helpful averages coexist with task regressions and load-balance sensitivity.

[Merlin / W0210](../../flued_multigranularity_survey_20261108/03_reading/B06/W0210.md), **2610.37645v1, §§2–4, Appendix C.5**, stores independently built segment states and separate first/second moments for routing. It grows state with segments and softly reads all visible segments. Route-Q and state-read-Q are distinct. Separately continued-training routing arms do not freeze the same written content; partial-segment normalization and moment-to-softmax interpretation remain source limitations.

[Triadic / BR-A02-N03](../03_reading/V09/BR-A02-N03.md), **2609.36529v1, Tables 1–3**, expands state through a second key axis. It compares matched expanded state and approximate parameter counts, often by reducing MLP width; a hybrid larger-KV comparator wins one recall average. State tables assume two-byte entries while an example kernel uses FP32 state. The E-fold state expansion is real even when projection-parameter overhead is small.

[Slot Attention / W0100](../03_reading/V11/W0100.md), **2006.15055v2, §2 and Appendix B**, adds competitive assignments and GRU refinement over a fully visible image. More slots or test iterations add resources; one failed stripe-segmentation seed is excluded from a reported aggregate. It establishes a useful allocation mechanism, not causal streaming or fixed-bit text superiority. [GQA / BR-A03-D12](../03_reading/V11/BR-A03-D12.md), **formal EMNLP 2023, §2, Figures 4–6**, separately demonstrates distinct queries over shared KV with recovery training; distinct Q is not independent stored content.

The missing comparison is now concrete: cross layout, total bits, query independence, read width, routing metadata, and active update cost. A single wider state, partitioned states, and multiple queries over the same state should each receive appropriate tuning. No inspected result selects the winner at matched complete resources.

## 8. Nonlinear fast memory and predictive state

### 8.1 Learning the memory function at test time

[TTT / W0242](../03_reading/V02/W0242.md), **2407.04620v4, §§2–3 and Appendix A**, makes a sequence's fast state the weights of a linear model or MLP. Input-derived key and value views define a self-supervised inner regression loss; a separate query view reads the updated model. Outer next-token training learns projections, initialization, and rates. This separates the architectural memory function from the algorithm that learns its sequence-specific contents.

The equivalence to simple unnormalized linear attention has specific assumptions: linear function, zero initialization, a particular batch gradient update, and learning rate. The practical residual, normalized, mini-batch models are different operators. Chunk gradients evaluated at a boundary state do not become exact sequential gradients merely because outputs are causal. TTT-MLP offers nonlinear storage but also more fast weights, worse practical wall time in some settings, and nonmonotone long-context behavior. Its state ledger includes convolution history and chunk buffers, not only one weight matrix.

[Titans / W0234](../03_reading/V03/W0234.md), **2501.00663v1, §§3–5, Tables 2,5**, adds gradient momentum, learned decay, persistent input-independent parameters, and alternative local-attention interfaces. Its useful needle and perplexity results establish a serious no-revisit fast-memory candidate, including a neural-memory-only variant. Hybrid success cannot identify which branch supplied the answer. The main Eq.13 uses the previous memory, whereas Appendix C Eq.32 prints the current memory on both sides; Eq.16's gradient-state convention also needs clarification. The expressivity theorem's proof was not located in this edition. These are source/algorithm gaps, not evidence that the implemented model or theorem is false.

[MIRAS / BR-A02-P01](../03_reading/V02/BR-A02-P01.md), **2504.13173v1, §§3–6, Appendices B–C**, broadens the design beyond squared error: choose memory architecture, associative loss, retention regularizer, and optimizer separately. Huber-like loss can reduce sensitivity to outliers; different norms or simplex/KL geometry change what is retained. Rare critical events can also resemble outliers. The useful experiment distinguishes irrelevant noise from valuable exceptions rather than assuming robust loss is always beneficial. Framework equivalences assume stated convex regularizers and minimizers; nonlinear chunk implementations approximate different sequential updates. Auxiliary fast state and hybrid KV remain real costs.

### 8.2 Predictive state is a bounded sufficiency alternative

[BR-A08-R07 / Predictive Representations of State](../03_reading/V08/BR-A08-R07.md), **institutional manuscript associated with NeurIPS 2001, §§1–3, revision unknown**, represents state by probabilities of selected future action–observation tests. Under known finite-POMDP dynamics, the construction selects a finite spanning core and expresses future tests through that core. Updating predictions uses normalized ratios, not a globally linear transition. Positive conditioning probability and well-conditioned test vectors matter.

Predictively equivalent histories may discard different details; the diagram-qualified known-model construction does not promise arbitrary-query reconstruction. **History-based learning now has direct primary evidence.**

[BR-PSR-0912.2385 / Closing the Learning-Planning Loop with Predictive State Representations](../03_reading/V18/BR-PSR-0912.2385.md), **0912.2385v1, §§2–4 pp.3–6**, estimates history/test moments, identifies transformed predictive coordinates/operators through SVD and pseudoinverses, separately regresses rewards, then plans. Author consistency requires finite predictive rank, rich tests/history features, nonsingular moments and convergent estimates. Reset sampling supplies intervention trajectories; suffix sampling from an unresettable exploration stream is explicitly approximate. This is coverage-conditioned identification from histories, not oracle dynamics or off-support identification. Finite estimates can predict negative probabilities; proposed thresholding is no exactness guarantee.

In simulated visual navigation, **78/100 trials succeed; mean 18.2 actions covers successes only**; 22 trials loop (§5.4, Fig.2D pp.8–9). A*'s 13.9-action comparator knows true configuration. Five deployed coordinates accompany 2,000 kernels each for histories/tests, 500 observation kernels, moment/operator estimation, reward regression and 8,000 planning points (§5.2). This foundational 2009 result supports learned state and closed-loop use in that environment—not equal-resource superiority, language transfer or arbitrary-query retention.

Compare oracle known-dynamics, history-estimated and neural filters in the same environment. Vary rank, exploration coverage, rare conditioning events, precision and horizon; separately score predictive risk, historical-detail recovery and all-trial planning success. This distinguishes sufficient state, identification, numerical filtering and planner failure.

### 8.3 A nonlinear read need not be fixed-state storage

[Hopfield / W0240](../03_reading/V11/W0240.md), **2008.02217v3, §2 and Appendices A.1,A.4**, provides attention-equivalent nonlinear pattern retrieval with separation and attraction-neighborhood conditions. The stored pattern bank costs O(Nd) elements. Exponentially many admissible patterns as a function of associative dimension is not exponentially long history at constant total bits. Correlated patterns can average, and a query outside the desired attraction region can converge incorrectly. Arbitrary value feedback also need not preserve the pattern-space energy dynamics.

[MemN2N / BR-A03-D11](../03_reading/V11/BR-A03-D11.md), **1503.08895v5, §§2,4–5, Table 1 p.6**, demonstrates trainable adaptive queries across an explicit bank. Its positive multi-hop results retain bank access, additional computation, and restart selection. It is an important reader comparator, not evidence that fixed compressed state gained capacity. Repeat-same-query and equal-compute nonread depth are needed to isolate the benefit of adaptive rereading.

## 9. Compare native no-revisit routes directly

The following are eligible solution families, not selected architectures. A design hypothesis becomes stronger when its predicted discriminator succeeds at the promised task and budget, rather than when a competing literature body is unavailable.

| Route | Defect it could address | What remains resident and what is learned | Most informative competing explanation |
|---|---|---|---|
| Task-aligned continuous or discrete compression | Objective-induced omission | Bounded payload; writer and consumer trained with declared labels/teachers | Gain comes from more adaptation or different rate, not better retained distinctions. |
| Additive, residual, gated, or directional editing | Conflicting writes, stale associations | Matrix state, gates and local buffers; outer loss learns update policy | Extra projections, normalization, or local context explain gains; useful old facts are erased. |
| Covariance-aware native memory | Correlated-key regression error | Mean plus covariance/statistics, with filtering arithmetic | Larger state or supplied read keys, rather than correction geometry, explain success. |
| Partitioned or tensor-product state | Allocation/interference under heterogeneous content | All states, joint-key axes, route metadata and projections | More total bits or narrower MLP, rather than layout, changes the frontier. |
| Native query/readout adaptation on unchanged state | Retained content is inaccessible | Same frozen state; restricted reader update and explicit supervision | Adapter learns answer priors or gains stronger query information. |
| Nonlinear fast-weight memory | Insufficient memory-function class or update flexibility | Fast network, optimizer state, rates, buffers and any local KV | Extra fast bits, inner steps or local path—not nonlinearity—carry the benefit. |
| Predictive-state learning | Full history is unnecessary for a bounded future-test family | Learned predictive coordinates and filtering parameters | Unknown-process identification, conditioning or query-family scope breaks the construction. |
| Protected exact payload plus learned task state | Rare identifiers or exceptions need exact retention | Explicit bounded exact channel plus learned summary; candidate design, not an evaluated source result here | Protected-item selection needs future labels, or exact storage consumes the relevant budget. |
| Accumulating compressed segments | A fixed overwrite state loses distinct histories | Growing summaries and adapted reader, as in AutoCompressors/Merlin | Improvement comes from growth and repeated access rather than compression quality alone. |
| Source-enabled bank, flat retrieval, or hierarchy | Later queries need details not in the retained code | Source/index/KV plus access policy and reader; additional permissions | Fresh information or more calls explains advantage; omission/fallback and lifecycle remain unmeasured. |

“Without original-source return” need not mean constant memory: growing compressed state is a different no-original-return contract from one bounded recurrent state. Likewise, holding a source bank outside the GPU does not make its storage or access free. For fair comparison, report fixed-state and growing-state frontiers separately, then compare source-enabled methods under their larger information-access contract. Hierarchy is one source-policy option; neither its necessity nor its net benefit follows from a native-state failure.

## 10. Rival hypotheses and minimal discriminating experiments

These are proposed scientific comparisons, not authorization or frozen numerical acceptance rules. Sample sizes, effect margins, and adaptation doses should follow task importance, observed variability, and the intended claim. Shared seeds/exam windows and environment fingerprints prevent unrelated data or hardware changes from masquerading as mechanism effects.

| Rival hypotheses | Smallest informative contrast | Observation that changes the explanation | Remaining ambiguity |
|---|---|---|---|
| Objective discards content vs consumer cannot read it | Same saved code: native consumer, equal-permission bounded reader repair, stronger diagnostic reader; correct/wrong code swaps | Strong reader recovers held-out identity, while native repair succeeds without new state | Diagnostic success covers tested targets; all readers failing is not a loss proof. |
| Reconstruction is harmful vs rate/interface/adaptation differs | One carrier: reconstruction/continuation/mixed × realized rate × frozen/bounded-adapted consumer | Objective ranking reverses within matched cells or across rates | Teacher labels, optimization dose, and content-use validity still matter. |
| Decoder shortcut vs inference lag vs AE optimization failure | Common initialization and total work: encoder-extra, decoder-extra, ordinary joint, and deterministic reconstruction control | Writer-extra helps without changing objective; or deterministic counterpart fails too | Multiple mechanisms can coexist; KL alone cannot distinguish them. |
| Time decay vs write interference | Fixed target and gap: transition-only interval, unrelated writes, near-key writes | Damage follows elapsed transition vs number/similarity of writes | Disabling writes may alter native dynamics; preserve transition definitions. |
| Correction helps rebinding vs destroys first truth | Same K/V stream and starting state; first/latest/context-tagged targets; additive/delta/erase variants | New binding improves with selective collateral cost or systematic policy reversal | Projection/gate learning requires separately budgeted retraining. |
| Correlated keys vs correlated values | Independent key-overlap × value-overlap manipulation; identical write and read contracts | Failure tracks joint geometry rather than key similarity alone | Synthetic geometry need not reproduce semantic identity ambiguity. |
| Numerical accumulation vs too few retained directions | Same ideal update: precision × requantization frequency; independent basis/rank sweep | Higher precision fixes long-delay errors without extra rank, or restored direction fixes exact identity | Buffers/compensators and changed closed-loop coefficients must count. |
| Better layout vs more state or stronger queries | One/many states × equal complete bits × shared/distinct Q × common return width | A layout benefit survives total-state and reader matching | Routing, scheduling, tuning and active costs can still differ. |
| Nonlinear capacity vs more inner work | Linear/MLP memory at equal total fast bytes and trained/serving work; vary inner-step timing | Nonlinear advantage survives matched local paths and work | A finite tested family does not demonstrate universal capacity. |
| Intrinsic inability vs difficult formation | Same generator/cell with equal search opportunity; constant, reverse and success-gated curricula | Solution probability improves across independent seeds, including failed runs | Trained-length success is not length or semantic extrapolation. |
| Adaptive reading vs extra computation | Same retained bank: one read, fixed-query repeats, adaptive repeats, equally deep no-read processing | Only adaptive querying improves held-out joins and content dependence | Bank access is still stronger than closed-state storage. |
| Relational composition vs explicit relation-instance benefit | Same facts; strong binary/flat baseline; separate arity, nesting, depth, identities and resources | Benefit is specific to retained identity/reuse rather than ordinary depth | Provenance/revocation claims require their own persistent-state tests. |

Before interpreting any comparison, establish task competence and assay sensitivity using identity replay, sham modification, high-fidelity content positives, and held-out natural content changes. Wrong-content replacements should alter the intended target while preserving legal addresses and non-target facts; incompatible hybrid key/value bindings are not clean evidence of content loss. Observe actual returns and final outputs. Redundant paths may require grouped interventions, and downstream compensation can conceal a single-path contribution. These are C/D conditions on interpreting A/B results, not alternative explanations to omit.

Keep three evidence levels visible in the resulting report. **Theory** establishes an existence result, bound, equivalence, or optimum under stated assumptions. **Learning** establishes what a procedure reaches with actual data, tuning, and history. **Native use** establishes that a legal deployed computation depends on the required retained content. Neither a theorem nor a trained probe supplies the last measurement automatically; native accuracy alone also does not identify which retained channel was used.

## 11. Mapping to the original 167-direction scope

The coordinates below preserve every owned member separately. **S** means substantive scoped evidence supports a bounded distinction; **P** means identified source completion is pending; **A** means a protocol/edition/resource artifact needs checking; **L** means a precise primary-evidence gap; **X** means a new controlled comparison is required. S is not scientific closure. Evidence packets and exact editions are in §§2–8; proposed discriminators are in §10.

### A — Compression and task sufficiency: 20 members

| Coordinate | Original question | Evidence route and residual |
|---|---|---|
| A.01 | Reconstruction vs predictive sufficiency | S+X: §3 SAC/ICAE/W0067; compare objective at equal rate and consumer opportunity. |
| A.02 | Reconstruction vs retrieval sufficiency | S+X: §3 xRAG/ICAE; fix later-query and source permissions. |
| A.03 | Strong decoder ignores latent | S+X: §3.2 context-width and content-swap controls, not KL ranking. |
| A.04 | Autoregressive posterior collapse | S+P: Broken ELBO/lag/R17; R16 body pending; deterministic non-use is distinct. |
| A.05 | Latent information vs actual use | S+X: §2.3 restricted reader, native return and final dependence. |
| A.06 | Unknown-query irreversible compression | S+L+X: §2 task-family/bit bounds; genuinely new query families remain open. |
| A.07 | Task fidelity without source return | S+X: §§2,8–9; declare promised tasks and every retained channel. |
| A.08 | Query-distribution shift | S+L+X: §§2,6.3; semantic/family shift is not new examples alone. |
| A.09 | Rare details and exceptions | S+L+X: §4.1 rarity × entropy × importance contrasts. |
| A.10 | Numbers, identifiers, exact strings | S+X: §4.1 exact identity separately from fluency/output frequency. |
| A.11 | Relation bindings | S+X: §4 value-bag-matched role/binding permutations. |
| A.12 | Within-segment order and position | S+X: §4 fixed-boundary order contrasts and relative-position targets. |
| A.13 | One vs many slots at fixed bits | S+X: §7.3 complete state/metadata and reader-width matching. |
| A.14 | Heads vs slots at fixed capacity | S+X: §7.3 separate distinct Q, stored content and fusion. |
| A.15 | Continuous vs discrete codes | S+X: §3.3 actual payload/estimator/reader, including dead codes. |
| A.16 | Reconstruction/prediction/retrieval supervision | S+X: §3 target/teacher costs and T05 supervision counterexample; no universal ranking. |
| A.17 | Rate learning vs content learning | S+P+X: W0067 and §3.3; official B-Net body blocked. |
| A.18 | Boundaries vs within-segment aggregation | S+P+X: §3 transport/pooling; replay boundaries; official B-Net body blocked. |
| A.19 | Compressor–backbone coadaptation | S+X: §3 frozen/bounded/joint consumers and unchanged-interface adaptation. |
| A.20 | Staged vs end-to-end training | S+A+X: §§3,8; matched stage opportunity, teacher ledger and reverse order. |

### B — State writing, retention, and capacity: 22 members

| Coordinate | Original question | Evidence route and residual |
|---|---|---|
| B.01 | Raw vs residual writes | S+X: §5 W0199/W0228 on identical projected K/V. |
| B.02 | Prediction-error updates | S+X: §§5,8; present surprise vs later usefulness and inner optimizer. |
| B.03 | Delta vs addition | S+X: §5 repeated/novel keys, truth policy and collateral outputs. |
| B.04 | Independent write/forget strength | S+X: §5 GDN/GDN-2; strength is not free erase addressing. |
| B.05 | Selective erase vs global decay | S+X: §5 EDA/DDN; stale and valuable-old counterfactuals. |
| B.06 | Overwrite vs accumulated interference | S+X: §6.1 no-write delay vs additional writes. |
| B.07 | Correlated-key crosstalk | S+X: §§5–6 joint key/value geometry; orthogonal example is conditional. |
| B.08 | Repeated/near keys with conflicting values | S+X: §5.3 first/latest/context-tagged truth and old/new scores. |
| B.09 | Relevance appears after writing | S+L+X: §6.3 query-last/time-late, not oracle depth-late rescue. |
| B.10 | Importance unknown when writing | S+L+X: §§5.3,6.3 retention without future relevance labels. |
| B.11 | Capacity vs precision | S+A+X: §7.2 physical carry, compensators, buffers and update frequency. |
| B.12 | Rank vs effective capacity | S+A+X: §7.2 low-energy critical directions and task-sensitive reading. |
| B.13 | States/heads/partition allocation | S+X: §7.3 total bits vs active costs and address independence. |
| B.14 | Long-delay retention | S+X: §6 training length, no-write gap and extrapolation separated. |
| B.15 | Multi-item retrieval degradation | S+X: §6 same generator, load and equal tuning opportunity. |
| B.16 | Growing distractor interference | S+X: §6 distractor number/similarity/conflicts and no-binding floors. |
| B.17 | OOD query accessibility | S+L+X: §§6–7 identity novelty, noise, paraphrase and composition separately. |
| B.18 | Linear vs nonlinear state | S+A+P+X: §8 TTT/Titans/MIRAS; full fast state and pending recent update evidence. |
| B.19 | Predictive state/task memory | S+P+L+X: §8.2 history-learned identification now read; exploration/conditioning/language transfer open; recent scope bodies blocked. |
| B.20 | Capacity bound vs reachable capacity | S+A+P+X: §§6–8 finite bits beside retuned successes; update details pending. |
| B.21 | Memory curricula | S+X: §6.2 success probability, complete seeds and equal-exposure schedules. |
| B.22 | Exact long memory without original return | S+L+X: §§7–9 bounded-task success vs unrestricted random-copy limit. |

**R.11** is covered in §4.2 and the relation discriminator: S+X, with W0537–W0543 and a strong ordinary binary/flat baseline. Its unresolved question is the same-fact-pool effect of arity, relation-result reuse, persistent identity, and depth at declared resources.

The other 124 coordinates remain with their accountable chapters, not silently certified here. Important interfaces are C.06–C.08/C.18–C.20 for legal native querying; D.01–D.02/D.07–D.15 for content-use assay validity; E.01–E.03/E.09–E.10/E.17–E.22 for formation and schedules; F.05–F.11 for adaptation and companion budgets; I.06–I.12/I.20–I.27 for causal byte grouping, decoder allocation and remote exact content; and R.01/R.12–R.13/R.16 for access contracts, selective updates and complete cost. Their global dispositions remain in [QUESTION_COVERAGE](../02_catalog/QUESTION_COVERAGE.md), not a claim that this chapter answers all 167.

## 12. Returned evidence and remaining source-gated decisions

**Updated 9 November 2026 against [coverage R3](../05_review/COVERAGE_RECHECK_R3.md) and [source audit R3](../05_review/ICLR2027_SOURCE_AUDIT_R3.md).** V17/V18 have returned: two independent recent preprints and the foundational PSR-learning original have full-reading cards. PSR identification now informs §8.2; T05 supervision informs §3.1. [T03, 2610.19139v1, §6.2](../03_reading/V17/BR-R2-T03.md) supplies a stable-prefix comparator, but measured code waits for completed pretokens; its theoretical delay bound does not certify a learned compressor or end-to-end serving latency.

**Seventeen selected official ICLR 2027 manuscript bodies remain unavailable**, not seventeen experimentally disproven mechanisms. The cohort combines six earlier blockers, six V17 interface originals, and five V18 broad originals. The audits' official metadata snapshots establish submission status, not acceptance, body equality, or a venue census. T03/T05 public editions do not complete their anonymous official editions. **T02's independent 2604.16037v1 has been acquired; terra reading is in progress. No result is anticipated here.**

Remaining A/B source gates are concrete: Incentive and routing/shortcut work for learning versus capacity; SDG/LoopLA for update timing and matched work; B-Net/formal compression for rate and content; T04 for head/trunk localization; finite-query compilation for protected versus unknown queries; predictive-scope/bottleneck originals for rank/address assumptions; attention placement for recurrent versus attention-path use. Their titles cannot back a mechanism or architectural ranking. [R3's complete cohort table](../05_review/ICLR2027_SOURCE_AUDIT_R3.md) also preserves the two transfer-body gaps.

R16 and those recent bodies are **source gaps**. Exact doses, carry precision, calibration and notation are **artifact gaps**. Learned PSR no longer has an existence-only account, but finite-data conditioning, exploration transfer, semantic query-family shift, equal-total-bit layout superiority and target-host native use remain **experimental gaps**. Bounded synthesis can proceed without choosing an architecture from missing evidence.
