# A01 — Compression and task sufficiency: recovered scope and discovery findings

**Date:** 2026-11-09. **Deliverable:** axis discovery, not the final broad-report synthesis or an architecture decision. **Ownership:** this directory only. See [work records](WORKS_AND_PROBLEMS.md), [search/access log](SEARCH_LOG.md), and [prioritized reading handoff](READING_HANDOFF.md).

## 1. Governing question and evidence boundary

What information should an irreversible state representation preserve when its specific future query is unknown, and why might information that is retained still fail to support the deployed task? This question is independent of whether the eventual solution uses source retrieval. The governing list is `flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md`, compression items 1–21; neither a hierarchy proposal nor a source-revisit requirement selects the literature.

This pass read the previous compression audit and its complete 11-work recommendation list, checked both named catalogs, read **11 actual existing scoped reading cards**, and externally verified/recovered **21 targeted works** at explicitly heterogeneous depths. The 21 are 5 existing W records, 6 previous compression-audit discovery records, 3 existing BIW partial records, and 7 catalog-absent candidates (new relative to the inspected catalogs, not a claim of scientific novelty or absence from every parallel stream). None is a new FULL reading. The eleven reused cards are not counted again as newly read papers. Four ICLR 2027 forum leads were attempted but blocked; they are not included in the 21 verified works.

There is enough evidence to rebuild the conceptual distinctions and articulate competing experiments. There is **not** enough to select a universal objective, latent type, slot layout, or training schedule. OpenReview availability also prevents a defensible conference-wide coverage claim.

## 2. Findings that change the research fork

### 2.1 Query unknown is not the same as task family unknown

**Reused original evidence:** W0059, *Lossy Compression for Lossless Prediction*, arXiv:2106.10800v5, protects a preselected family of invariant tasks. Its maximum invariant partitions the inputs by a specified equivalence relation; it does not preserve every conceivable later question. Its log-loss result needs the stated countability/finite-entropy and asymptotic coding conditions. The old card contains concrete concerns about its MSE extension, so that extension must not carry an unconditional claim. W0080, arXiv:2608.14528v1, independently distinguishes task-conditional prediction-equivalence classes and counts every history-derived channel; its quotient theorem requires external-query conditions, not arbitrary history-dependent query selection.

**Our conditional inference:** if two source histories share a code but a permitted later query requires different outputs, that code is not sufficient for that task family. If the allowed queries separate every history, exact universal sufficiency demands an injective code on the relevant support. Conversely, if many histories are equivalent for the permitted tasks, an irreversible statistic may be exactly sufficient. Both statements can hold without source retrieval.

W0061's uniform-random-string counting bound and W0080's independent-bit example establish genuine worst-case capacity obstructions, not universal incompressibility of natural text. A phone number, identifier, exception, order relation, or entity–value binding is an informative stress case precisely when it is unpredictable from the rest of the history and belongs to the promised query family. Testing only semantic averages silently changes that promise.

### 2.2 Reconstruction, prediction, and retrieval relevance are different distortions

Reconstructing the source, predicting a continuation, preserving an answer, approximating a teacher distribution, and reproducing an attention response are distinct objectives. A reconstruction decoder can exploit source-prefix regularities under teacher forcing; a low average reconstruction loss does not certify exact restoration of a rare field or deployment-time accessibility.

The strongest existing counterweight to an anti-reconstruction narrative is **W0038/BIW-0020 (ICAE), v4**: its scoped original card reports benefits of mixed reconstruction and continuation over either alone in the studied setup, while random structured content reconstructs poorly and independently compressed segments require additional multi-segment training. **W0023, v1 (Compressive Transformers)** instead trains compression using attention-response reconstruction, with stop-gradient choices and unequal BPTT/c-ratio settings that prevent a universal objective ranking.

**Freshly checked original text:** [SAC v4](https://arxiv.org/html/2510.08907v4), §§3–5, reports that reconstruction hurts its own architecture, including mixed AE+LM versus LM alone. Its existing-baseline results are not evidence that all reconstruction supervision hurts. SAC changes carriers, bidirectional encoding and per-layer KV conditioning as well as the training recipe. The paper's near-zero AE/LM gradient cosine is a diagnostic; orthogonality alone does not establish harmful interference or identify capacity theft as the cause. Numeric Table 5 cells did not survive this extraction and were not invented.

**New recent alternative:** [Boa v1](https://arxiv.org/html/2610.33006v1) trains a Mamba encoder and per-layer KV projections against a frozen consumer, using LM pretraining followed by answer-position teacher-distribution matching. Its selected method/ablation passages make objective timing and interface capacity separate candidates. Its retained sequence grows as `ceil(L/r)`; it is not a counterexample to fixed-total-state capacity bounds, and its discussion of query-aware online compression must not be imported as query-unknown evidence without checking actual input construction.

### 2.3 Rate can change which objective is preferable

**Recovered unread priority W0067**, [arXiv:2610.30493v1](https://arxiv.org/html/2610.30493v1), is directly about objective choice, not hierarchical retrieval. Selected §§2–6 now verify the following author results:

- The shared writer does not observe the task index; a task-dependent decoder does. Gaussian task channels and a mutual-information constraint permit a covariance benchmark.
- A partially aligned specialist can beat a reconstruction generalist at low rates and lose at higher rates because it omits useful directions.
- A fixed Gaussian pretext fixes relative allocation ordering. A constructed family with increasing task signal-to-noise ratio produces arbitrarily large **relative** regret, normalized by the optimum distortion. This is not an arbitrary-natural-language impossibility theorem.
- A **positive control** matters: bounded task SNR and a known weighted task-information matrix give a uniform approximation bound for an appropriately chosen fixed pretext. The paper does not show every task mixture requires rate-dependent objectives.
- CelebA uses common frozen ResNet features, PCA/whitening, four evaluation attributes and reoptimized compression heads. Gaussian nominal rate and learned B-bit codes are different budget axes. Probe excess NLL is subject to estimation/approximation, not native LLM dependence.

The proofs, implementation, full finite-bit entropy accounting and dSprites appendices remain unread. Nonetheless, the primary research obligation is now sharper: **objective × rate × consumer-adaptation interactions**, not a single AE-versus-LM contest at one compression ratio.

[Universal Representations for Classification-enhanced Lossy Compression v1](https://arxiv.org/abs/2504.13191v1) also reports operating-point reuse penalties in classification–reconstruction tradeoffs, with a comparatively favorable perception example. It concerns a specified task/constraint family and MNIST, not unknown arbitrary queries.

### 2.4 Retained information, accessible information and actual use are not synonyms

The **existing** W0092 v1 and W0091 v2 cards already establish consumer-family dependence. A deterministic transformation can make retained information easier for a restricted reader to decode without increasing Shannon information. Their family-optimal quantities are not the gain of a particular trained backbone. W0091's exact sufficient/minimal representation theorem has strong finite-space, label and predictor-family conditions; the original card flags endpoint/closure and proof-step issues. Do not generalize it into a guarantee about a softmax head learned by SGD.

A useful formal contract is a writer `Z ~ E(.|X)` that cannot see the later query Q and has no residual source access. Under `Y ⟂ Z | (X,Q)`, finite relevant entropies, and optimal probabilistic log-loss prediction,

`R_Bayes(Z,Q) - R_Bayes(X,Q) = I(Y; X | Z,Q)`.

This is a conditional identity, not a measurable compression score for an arbitrary neural network. A deployed predictor also incurs a reader-family approximation gap and a training/adaptation gap relative to that family's population optimum. Source informativeness, writer quality under budget, family accessibility and achieved consumer performance must be measured separately. Query exogeneity is not needed for this identity but is needed for the particular W0080 prediction-equivalence theorem cited above.

**Sanity counterexample:** if a permitted deployment decoder exactly recovers X from Z within the allowed resource budget, composing it with the original task solver recovers the same task performance. Failure of a different direct reader is then an interface/computation/optimization issue, not information-theoretic loss. Average BLEU or teacher-forced likelihood is not that exact-recovery premise.

### 2.5 A strong decoder ignoring latents has several mechanisms

Use **posterior collapse** narrowly: a stochastic variational posterior degenerates toward its prior, eliminating input-dependent latent information. It is not a synonym for every deterministic summary bypass, unbalanced slot usage, or downstream failure.

The external originals recover alternatives rather than a single slogan:

- **BIW-0094**, Bowman et al., CoNLL 2016: sentence VAE, autoregressive word decoder, KL scheduling/word dropout; useful historical observation and decoder-context controls, not a deterministic-byte result.
- **BIW-0095**, Yang et al., arXiv:1702.08139v2: dilated CNN context length changes the decoder-context/latent-use tradeoff. Best likelihood and best representation task need not be the same operating point.
- **BIW-0096**, He et al., arXiv:1901.05534v2: lagging inference updates are a moving-target optimization explanation, with additional updates and real compute costs.
- **Fixing a Broken ELBO**, ICML 2018: equal evidence-lower-bound scores can correspond to different rate/distortion/representation behavior; objective score alone does not choose useful codes.
- **Variational Lossy Autoencoder**, arXiv:1611.02731v2: architectural allocation deliberately lets an autoregressive decoder handle local detail while latents represent global structure. Discarding texture can be a design goal, but discarding identifiers is unacceptable if identifiers are promised tasks.
- **Don't Blame the ELBO!**, NeurIPS 2019: the linear-VAE/pPCA analysis places collapse-related local maxima in marginal likelihood itself, with no additional ELBO spurious maxima in that model. This is an essential counterexample to 'KL is always the sole cause.'
- **The Usual Suspects?**, ICML 2020: small nonlinear decoder perturbations/deeper models can introduce bad minima and information truncation. This does not contradict the conditional linear result.
- **Cyclical Annealing**, NAACL 2019: warm-restart KL schedules compete with inference-update and decoder-capacity interventions; any gain must include extra schedules/updates and held-out latent utility.
- **Variance Equalization for Posterior Collapse**, arXiv:2607.05531v1 (2026): a recent proposal separates reconstruction/KL gradient imbalance from sampling-related information loss and modifies noise scaling. Verified abstract/introduction only; its image experiments and proposed algebra are not evidence of a universal language-memory cure.

For a conventional VAE, `E_X KL(q(Z|X)||p(Z)) = I_q(X;Z) + KL(q(Z)||p(Z))`. Thus positive average KL can reflect aggregate-prior mismatch even when input information is zero; positive KL is not proof of useful latent content. Conversely, a decoder may ignore informative Z, so decoder ignorance does not logically imply posterior collapse. In deterministic compression, use direct content interventions/consumer comparisons rather than importing a stochastic KL diagnosis.

### 2.6 Learning source, optimization and aggregation grain must be disentangled

| Dimension | What actually changes | Illustrative evidence | Required non-confounded comparison |
|---|---|---|---|
| Learning source/target | Original bytes, continuation, task labels, full-context teacher outputs, attention responses, positive views | ICAE; Compressive Transformer; W0059; SAC; Boa | Same histories, query permissions and exposure; teacher/label costs explicit |
| Optimization method | End-to-end vs staged; frozen consumer; extra inference steps; stop-gradient; straight-through estimator; loss scheduling | BIW-0096; cyclical annealing; W0011; W0023 | Same effective compute or quality–compute curve; distinguish signal absence from optimization lag |
| Aggregation grain | Boundary vector, mean/max/conv pool, multiple slots, per-layer KV, cross-layer features | W0011; BIW-0006; SAC; ComprExIT | Fix total persistent bits and consumer/adaptation budget, not only slot count |
| Rate learning | Target boundary density, actual hard truncation, learned quantization/entropy | W0011; BIW-0006; W0013 | Separately report realized rate and retained content at that rate |
| Content learning | Which details/relations are retained inside the selected segments | W0067; W0059; task losses | Fixed boundaries then swap aggregation/targets; fixed aggregation then swap boundaries |

The reused **MANTa/BIW-0006 v1** card is especially useful: byte denoising trains a soft frontier/assignment system, order-sensitive convolution/max pooling forms the blocks, and a hard `L/4` cap prevents the tendency toward one block per byte. Task loss alone does not certify rate control. **W0011 v2 (H-Net)** selects contextual boundary vectors, not necessarily mean-pools a segment; its smoothing, straight-through gradient and rate loss have separate effects. **W0013 v1** combines gated quantization with character reconstruction, then uses original-source checks and character fallback while constructing a tokenizer; that fallback is not latent-only recovery after source disposal.

## 3. Subdirection-level coverage and next action

Classifications are multidimensional: `S` enough existing scoped evidence for conditional synthesis; `U` existing original remains unread; `N` new/targeted search useful; `E` genuinely new controlled experiment required. S does not mean architecture selection is justified or the field is exhausted.

| Recovered subdirection | Adequate existing synthesis inputs | Unread/recovered or new source | Remaining question and action |
|---|---|---|---|
| Reconstruction vs prediction | W0038 v4; W0023 v1 | SAC; W0067; Boa | S+U+E: target × rate × adaptation crossover, with equal content/compute |
| Reconstruction vs retrieval/answer sufficiency | W0076 v2; W0059 v5 | xRAG/W0055; Rethinking Minimal Sufficient Representation | S+U+E: answer-relevant private detail/relational evidence absent from pretext |
| Query unknown; no source return | W0080 v1; W0061 v2; W0059 v5 | W0067; W0066 | S+U+E: fixed family vs shifted family vs independent exact details; no retrieval prerequisite |
| Decoder ignorance; stochastic posterior collapse | Reader-family theory; BIW-0094–96 partial records | Broken ELBO; VLAE; Lucas; Dai; cyclical; variance equalization | U+N+E: objective degeneracy, lag and local minima must receive different controls |
| Latent information vs actual usage | W0091 v2; W0092 v1; ICAE | xRAG/Boa bridging; ComprExIT diagnostics | S+U+E: fixed-state strong reader vs deployed reader vs content-specific output effect |
| Query-distribution shift | W0059's excluded-task counterexample | Rethinking; W0066; MemSafe transfer negatives | S+U+E: family holdout, not only new examples from same task |
| Rare details, numbers, identifiers, exact strings | W0061; ICAE random-text failure | No new fair latent-only numeric benchmark established here | S+E; N remains targeted: exception frequency × entropy × exact-match risk |
| Relation bindings, local order, relative position | MANTa order-sensitive aggregation; ICAE multi-segment failure | ComprExIT coordination is a candidate, not binding proof | S+U+E: permute bindings/order at fixed bag of values and total bits |
| One slot vs multiple slots; heads at fixed total capacity | Reader-family theory gives distinctions, not clean ranking | ComprExIT; Boa KV/embedding ablation | U+E: same effective bits, metadata and readout capacity; no matching evidence found, not nonexistence |
| Continuous vs discrete latents | W0013 scoped example and fallback limitation | VQ-VAE; W0067 finite-bit branch | S+U+E: quantization/straight-through/training/codebook effects separated |
| Reconstruction/prediction/retrieval supervision | W0038; W0023 | AutoCompressors; xRAG; SAC; Boa | S+U+E: target visibility and consumer adaptation held fixed |
| Rate learning vs content learning | H-Net; MANTa; W0013 | W0067 operating-rate dependence | S+U+E: hold one fixed while varying the other |
| Boundary learning vs within-segment aggregation | H-Net E.1; MANTa local composition | SAC fixed anchors; ComprExIT local transport | S+U+E: fixed boundary replay and learned-boundary arm under same budget |
| Joint adaptation vs frozen/staged | ICAE frozen target; H-Net end-to-end | AutoCompressors; xRAG; lagging inference; Boa | S+U+E: no zero-cost bridge assumption; early disruption vs final adapted quality |

## 4. Independent alternatives that do not require source revisiting

These are **competing candidates**, not adopted project terms or new architecture rulings.

1. **Consumer-constrained task distortion:** train a compressed state to match deployed predictions, teacher distributions or attention responses; compare that target with source reconstruction. W0023, W0076, xRAG and Boa provide different contracts.
2. **Rate-aware multi-task allocation:** permit the target mixture or capacity allocation to depend on the deployment budget. W0067 supplies a conditional mechanism and a bounded-SNR fixed-objective control, not a turnkey language recipe.
3. **Latent-only interface adaptation:** freeze a good backbone and learn a bridge or KV projections; compare with jointly adapted and constant-prefix controls. Bridge-only training can be worthwhile without adding a source channel.
4. **Inference/decoder co-training schedule:** extra inference updates, KL schedules, decoder-context restriction, or staged warmup; each addresses a different collapse explanation and incurs a different optimization budget.
5. **Quantized states with explicit rate and utilization checks:** compare discrete codes, quantized continuous states and continuous slots under equal stored bits. Monitor codebook usage separately from posterior information and native output dependence.
6. **Order-/binding-preserving aggregation:** keep local order or multiple independently addressable slots, and aggregate intermediate features only if fixed-total-budget controls support it. More slots by themselves can merely buy capacity.
7. **Exception-sensitive task weighting or a small fully counted residual:** retain low-frequency exact fields explicitly within the irreversible state. This is a proposed experiment, not a verified literature winner; residual bytes and metadata count against the same budget.
8. **Sufficiency-aware abstention:** admit that a query is unsupported and abstain rather than fabricate. MemSafe is relevant to detection and benchmark shortcuts; abstention does not recover discarded facts and need not trigger a source revisit.

## 5. Minimal discriminating experiment obligations — not executed

| Hypotheses to distinguish | Smallest informative design | Essential controls / interpretation |
|---|---|---|
| Bits lost vs reader cannot decode | Freeze the writer/state; compare a strong trained reader, deployed reader and budgeted bridge | Add a genuine identity representation; charge readout compute. Strong-reader success rules out loss for that tested target, not all targets |
| Content dependence vs learned constant benefit | Correct state, same-type wrong-history state, trained constant state, no state | Match length/norm/type; measure answer flips tied to substituted facts and collateral damage |
| Objective mismatch vs optimizer lag | Same source/architecture/rate; AE, continuation, task and teacher losses; standard vs encoder-heavy updates | Equal total updates/compute or full learning curves; nonzero KL is not sufficient success |
| Compression objective is rate-independent | Cross several actual bit budgets with objective mixtures | Report task-wise tails and ranking reversals, not just aggregate NLL |
| Finer grain helps independently | One wide slot vs several narrow slots; fixed total quantized bits; same boundary replay | Match metadata, parameters, adaptation and readout compute; separate addressing from payload |
| Safe average but rare facts erased | Common semantics plus random identifiers, numbers, negated exceptions, binding swaps and order swaps | Condition risk on fact frequency/entropy; fixed query-unknown writer; held-out task families |
| Stage schedule protects content vs suppresses learning | Frozen, bridge-only, staged and end-to-end arms with common initialization | Compare equal adaptation budgets; track full training history and multiple seeds, not just final loss |

No numerical go/no-go threshold is preregistered. No training, production/evidence-registry edits, installation, paid access, commit or new experiment was performed. The final broad-report synthesis remains with the coordinating workflow.
