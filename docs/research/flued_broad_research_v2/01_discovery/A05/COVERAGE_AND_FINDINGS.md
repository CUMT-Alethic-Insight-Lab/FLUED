# A05 — Learning trajectories, coadaptation, and shortcuts

Date: 2026-11-09. Discovery and source recovery, not a final cross-axis synthesis, architecture selection, or experimental result.

## 1. Governing question and deliverables

Why does a compressed representation become—or fail to remain—a memory that the deployed model actually consumes? The governing scope is the learning-dynamics list in [FOLLOWUP_DIRECTIONS](../../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md), lines 99–122, not the multigranularity proposal. Source retrieval, utility routing, and retaining an original document are **not prerequisites** for the alternatives considered here.

This stream executed external discovery and checked original public sources. See [SEARCH_LOG](SEARCH_LOG.md), [WORKS_AND_PROBLEMS](WORKS_AND_PROBLEMS.md), and the prioritized [READING_HANDOFF](READING_HANDOFF.md). It recovered 11 prior recovery candidates, verified 11 additional works absent from the two canonical catalogs searched, and reused 10 actual scoped FULL cards without recounting them. These are provenance categories, not 32 new readings. **New FULL readings: zero.** Some new sources received substantive section reading; others remain abstract/metadata only. Three ICLR 2027 leads are separately blocked and excluded from the verified-work count.

Terminology: coadaptation means two jointly trained components changing representations to accommodate one another; gradient starvation means a strong predictive direction suppressing learning response to another direction; plasticity means capacity to learn from subsequent experience; a bypass is a path that can reduce the task loss without consuming the intended compressed content. Posterior collapse specifically concerns variational latent models and is not a synonym for deterministic memory non-use. In-context learning (ICL) means solving tasks using current contextual information without updating weights.

## 2. What was actually reused

The previous [learning-dynamics audit](../../../flued_multigranularity_survey_20261108/07_scope_recovery/05_LEARNING_DYNAMICS/COVERAGE_AUDIT.md) is useful but is not itself a substitute for reading cards. This pass directly read these existing cards:

| Existing identity | Actual card and fixed version | Substantive reusable evidence | Scope restriction retained |
|---|---|---|---|
| W0328 = BIW-0022 | [B16/W0328](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0328.md), 2001.06782v4, NeurIPS 2020 | Gradient direction, magnitude, and curvature are distinct; PCGrad has conditional local guarantees | Appendix A.3 necessity argument remains unaudited; no arbitrary-Adam or long-run guarantee |
| W0331 = BIW-0023 | [B16/W0331](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0331.md), 1812.02224v2 | Local descent can be slower; perfect-teacher gating can underperform adding the auxiliary loss | No guarantee about finite-budget generalization or content use |
| W0333 | [B16/W0333](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0333.md), 2011.09468v4, NeurIPS 2021 | Feature competition has an explicit learning-response mechanism | Fixed linearized features in key theory; test-environment tuning in a reported experiment; not a general deep-feature nonformation theorem |
| W0334 | [B16/W0334](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0334.md), 2403.03375v3 | Core and shortcut can emerge together; retrained-head access differs from deployed output; weak shortcuts can disappear | Preserve unresolved appendix norm-bound concern; do not invalidate empirical observations by association |
| W0336 | [B16/W0336](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0336.md), 2301.05217v3, ICLR 2023 | Mechanism formation can precede accuracy improvement; cleanup changes the winning computation | Fourier directions selected from the endpoint are retrospective, not blind early predictors |
| W0337 | [B16/W0337](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0337.md), 2404.07129v1 | Training-time restriction and endpoint head ablation answer different causal questions; initialization couples subcircuits | Clamping ideal behavior simplifies the learning problem and may alter activation distribution |
| W0023 = BIW-0018 | [B24/W0023](../../../flued_multigranularity_survey_20261108/03_reading/B24/W0023.md), 1911.05507v1 | Attention-response reconstruction and full-state reconstruction differ; auxiliary gradients can be isolated to the compressor | Different compression-rate tuning and BPTT unroll/batch choices prevent a pure equal-budget comparison |
| W0038 | [B24/W0038](../../../flued_multigranularity_survey_20261108/03_reading/B24/W0038.md), 2307.06945v4, ICLR 2024 | Mixed autoencoding/continuation pretraining, frozen base, later instruction tuning; multi-segment concatenation needs training | Does not establish universal stage ordering or causal use of every reconstructed detail |
| W0048 | [B24/W0048](../../../flued_multigranularity_survey_20261108/03_reading/B24/W0048.md), 2609.05152v2 | Teacher-success distillation then failure-set reinforcement; same-RL uncompressed control matters | No fully matched reverse-order/sample/compute control; preprint status, not presumed accepted |
| W0366 | [B14/W0366](../../../flued_multigranularity_survey_20261108/03_reading/B14/W0366.md), 2603.26663v1 | Tied input/output paths have unequal gradient norms early; direct gradient rescaling has mixed outcomes | Different corpora/model sizes and single runs; byte vocabulary and cosine head not factorially isolated |

The byte survey adds an actual trajectory card: [BIW-0113](../../../byte_language_interface_survey/03_reading/R10/BIW-0113.md), EMNLP 2025 proceedings, *The Strawberry Problem*. It is reused separately as a byte-interface bridge, not counted among the 10 W-card reuses above. Its onset threshold is **0.5% exact match, not 50%**. A direct character side channel changes information access as well as learning speed, so it is not a pure optimizer intervention. BIW-0114 (CharBench) was checked but not retained as training-dynamics evidence: it is predominantly endpoint observational evaluation.

Correction to prior novelty language: LD-N01 (*Lagging Inference Networks*) already has alias **BIW-0096**, selected-primary/recovery status in the byte catalog but no FULL card. It must not be reintroduced as a wholly new work.

## 3. Findings that materially change the questions

### 3.1 Encoder lag, bad objective geometry, and content loss must be separated

[LD-N01](https://arxiv.org/html/1901.05534v2) explicitly follows the mismatch between amortized inference and the moving model posterior, then uses extra inference-network updates. This is a concrete training-order alternative without adding a memory hierarchy. [LD-N08](https://arxiv.org/abs/1911.02469v1) supplies a counterexample to a blanket strong-decoder/KL explanation: linear models and likelihood geometry can already exhibit collapse-related stationary behavior. [A05-N01](https://proceedings.mlr.press/v238/ichikawa24a.html) adds a minimal-VAE learning-dynamics analysis: beyond a regularization threshold, longer training alone does not avoid collapse; annealing can affect speed.

**Author result versus our inference:** these sources concern variational objectives, not the actual deterministic compressor. Our transferable inference is only that optimization rate, objective-induced equilibria, and representational capacity require different tests. A frozen-checkpoint probe cannot by itself establish an encoder-lag cause. Equal-compute continuation with different writer/reader update allocations is a new experiment.

### 3.2 Recent bottleneck work argues for mechanism-specific curricula, not “always pretrain reconstruction”

[Continuous First, Discrete Later, 2605.06870v3](https://arxiv.org/html/2605.06870v3), revised September 2026, identifies low-variance latent modes suppressed by early vector quantization. Its §4.1/Table 1 explicitly exchanges AE steps for VQ steps within a common 100k-step budget; §4.2 uses a fixed 100-epoch audio budget. The method delays quantization, not the learning rate. Its linear rate-distortion model does not prove permanent mode death for an arbitrary continuous compressor.

In contrast, [GenFirst, 2608.29335v1](https://arxiv.org/pdf/2608.29335v1), August 2026, gives the generative objective greater relative influence **before** reconstruction refinement. It attributes this to generation being slower than reconstruction. In §4.3, reconstruction-related weights stay fixed while prior and entropy weights decrease together; the method is not literally a reconstruction-free first stage. The diffusion instantiation also contains a later frozen-VAE/prior-only phase, so not all reported performance is produced by joint training alone.

These are not contradictions to be resolved by choosing a slogan. They target different bottlenecks—quantization suppressing modes versus reconstruction anchoring a difficult-to-model distribution. **Which obstacle exists here is empirical.** Neither requires revisiting original source text at deployment.

### 3.3 Same-direction gradients do not settle negative transfer

[LD-N04/ForkMerge §3.1](https://arxiv.org/html/2301.12618v3) compares one-step updates from the same intermediate parameters and evaluates transfer on validation data. Negative transfer can accompany highly consistent gradients, while a conflicting auxiliary update can regularize. This directly separates local training descent from validation benefit; it does **not** show two losses remain aligned through an entire run while jointly reinforcing a particular unwanted memory policy.

W0331 already supplies local slow-descent and imperfect gating counterexamples. W0328 adds curvature and scale. Therefore “final cosine is positive” is enough to reject only a narrow contemporaneous global-gradient antagonism claim. It cannot reject earlier starvation, blockwise antagonism, common shortcut reinforcement, optimizer-state effects, or poor generalization.

For a small update \(\Delta\theta\), the diagnostic decomposition is

\[
L_{\rm main}(\theta+\Delta\theta)-L_{\rm main}(\theta)
\approx g_{\rm main}^{\top}\Delta\theta
+\tfrac12\Delta\theta^{\top}H_{\rm main}\Delta\theta.
\]

This is a local Taylor diagnostic, not a global guarantee. For Adam, raw task-gradient cosine is not the cosine of the preconditioned, momentum-dependent update. Validation content dependence is a third, separate outcome.

### 3.4 Formed, retained, and repurposed mechanisms are different histories

[LD-N05/Strategy Coopetition](https://arxiv.org/html/2503.05631v2) is stronger than the earlier statement that ICL disappears: late behavior can be **context-constrained in-weights learning**, still requiring contextual label clues. Shared downstream circuitry can survive while its role changes. Removing the competing strategy at formation can impair the desired strategy's development; therefore a bypass can initially help and later replace a mechanism.

[A05-N05/Competition Dynamics](https://arxiv.org/html/2412.01003v4) uses a mixture-of-Markov-chains sequence task with multiple possible algorithms. Context length, diversity, and training duration can change the dominant algorithm. [A05-N06/Differential learning kinetics](https://arxiv.org/html/2412.00104v2) contrasts a learning-rate explanation with a limited-memorization-capacity explanation. Its reduced additive-circuit ansatz is not identical to the shared-subcircuit result in LD-N05; different task/model assumptions must remain visible.

[LD-N06/How Language Models Develop ICL](https://arxiv.org/html/2610.19113v1), October 2026, distinguishes prompt control, preference between candidate answers, free construction, and transfer. Reading those as one acquisition time would erase the result. Its appendix records post-plan changes and an external supplement not fully inspected here; thresholds cannot be copied into local gates.

### 3.5 Rank, inactivity, and curvature are competing diagnostics—not interchangeable verdicts

[A05-N02](https://arxiv.org/html/2605.06870v3) makes latent spectrum useful for a particular bottleneck. [A05-N08/ReDo](https://proceedings.mlr.press/v202/sokar23a.html) motivates monitoring dormant units in reinforcement learning. But [A05-N11/Directions of Curvature](https://arxiv.org/html/2312.00246v2), §§3–4, includes counterexamples to update norm and representation rank as sufficient explanations. Full-rank feature regularization can coexist with continued plasticity loss. Its large-model curvature diagnostic is an empirical-Fisher/per-sample-gradient Gram approximation, **not an exact Hessian**; proxy rank is also capped by sample count.

[A05-N09/DASH](https://proceedings.neurips.cc/paper_files/paper/2024/file/4c5ce1fc8895076f49935951a630be5c-Paper-Conference.pdf) supplies a stationary expanding-data setting in which dormant-unit and other nonstationary-plasticity remedies need not work. Its discrete feature/noise theory is not exact SGD dynamics. These counterexamples prevent interpreting any single collapsed-rank or dormant-unit plot as the cause of non-use.

### 3.6 Initialization and unfreezing are independent routes

[LD-N07](https://arxiv.org/html/2409.14623v2) studies relative encoder/decoder layer scales in a balanced deep-linear setting; [A05-N10/Saxe](https://arxiv.org/abs/1312.6120v3) supplies the original restricted exact dynamics and sequential mode-learning background. They justify examining initialization rather than assuming capacity failure. They do not guarantee that rescaling an Adam-trained nonlinear memory repairs it.

[A05-N07/ULMFiT](https://aclanthology.org/P18-1031.pdf), §§3.3/5, provides a real freezing/unfreezing control family: last-layer only, full, chain-thaw, and gradual unfreezing. Importantly, its text reports gradual unfreezing alone as similar to full fine-tuning, while learning-rate choices and the combination matter. It is an original counterexample to claiming that gradual unfreezing universally dominates.

## 4. Coverage decision by key subdirection

Labels describe the **next evidence action**, not field exhaustion. S = adequate existing synthesis material; U = existing but unread; D = newly recovered/discovered source reading; E = genuinely new local experiment. Several rows require more than one.

| Original subdirection | Adequate existing material | Unread existing / new source gap | What saved checkpoints can test without continuation | What requires a new experiment |
|---|---|---|---|---|
| Early inference lag; encoder/decoder speed mismatch | W0337, W0366 support coupled formation, not VAE lag | D: LD-N01, LD-N08, N01 | Track latent recoverability, reader sensitivity, writer/reader gradient scales at saved times | E: writer-extra vs reader-extra vs joint updates with matched compute and preserved initialization |
| Reader/writer coformation | W0337; W0334 readout separation | D: N06, LD-N05 | Same-time payload probes and native-query diagnostics; content interventions on fixed windows | E: fixed writer + consumer adaptation; freeze/thaw crossover; compare same-time and cross-time interfaces |
| Initialization and layer scale | W0337; W0366 | D: LD-N07, LD-N09, N10 | Saved initial activations/parameter scales, feature drift, query-key/value norms if t=0 retained | E: paired initialization/parameterization arms; optimizer changes separated from function/activation scale |
| Feature competition/starvation | S: W0333/W0334 | U: W0332 *Pitfalls of Simplicity Bias*; D: N06/N09 | Fixed holdout core/shortcut probes, loss-conditioned gradients; do not infer absent unmeasured features | E: controlled shortcut correlation/difficulty and bypass timing, same total data exposure |
| Easy features first; complex dependence later | W0334 refutes universal ordering; W0336 shows latent progress | D: LD-N06, N05/N06; byte card BIW-0113 | Multi-metric onset curves rather than one accuracy threshold | E: training-task diversity/difficulty curricula with fixed final test and matched cumulative exposure |
| Bypass helps optimization vs replaces target mechanism | W0337 formation/endpoint distinction | D: LD-N05/N05 | Per-time natural-content substitution with local path intact or evaluation-masked; test role replacement | E: temporary bypass attenuation and restoration; random equal-strength control; formation persistence |
| Auxiliary reconstruction; deep supervision | S: W0023/W0038/W0048 are materially different objectives | D: LD-N02; N02/N03 supply opposite schedule rationales | Reconstructability versus native consumption; per-loss block gradients; frozen-current function only | E: early-only/late-only/continuous auxiliary, gradient stop/routing, direct intermediate task supervision |
| Same-direction negative transfer; cosine/benefit mismatch | S: W0331/W0328 | D: LD-N04; U: W0327/0329/0330 if algorithm selection pursued | Recompute raw and preconditioned directions, gradient scales, local curvature on same data | E: matched continuation trajectories and validation content benefit; cannot infer all-history alignment |
| Multi-loss curvature and optimizer dynamics | W0328 local conditional results | D: N11; D: N09 stationary contrast | Directional finite differences/Hessian-vector diagnostics; gradient-Gram proxy with fixed sample count | E: resumed optimizer-state retention/reset control; distinguish preconditioning from representation bottleneck |
| Loss decreases while content use declines | W0334/W0336 indicate distinct readout/feature trajectories | D: LD-N10 paired with LD-N05; LD-N06 | Plot same-window loss, correct-vs-wrong-content dependence, probes, native readout over time | E only if missing history or testing which intervention preserves use |
| Mechanism emergence, disappearance, repurposing | S: W0336/W0337 | D: LD-N05/N05/N06 | Saved checkpoints distinguish visible transient behavior from endpoint failure; absence between sparse snapshots remains unknown | E: dense-save continuation, permanence controls, fixed validation-based stopping or regularization |
| Stage changes and freeze/unfreeze readaptation | W0038/W0048; no universal ordering | D: N07/N03/N09; LD-N03 | Before/after saved transition snapshots, activation distribution shifts, native dependency | E: matched schedule order/duration, frozen/joint/gradual baselines, adaptation budgets |
| Multiple seeds, full history vs final point | W0336 key frequencies vary; W0337 formation timing varies | D: N06 predicts broad latency distribution | Same evaluation windows within and across saved seeds/hardware; censored onset intervals | E: new paired seeds if not retained, same hardware/environment per comparison |

Existing unread W sources retain their original identities: [W0327 GradNorm](https://proceedings.mlr.press/v80/chen18a.html), [W0329 CAGrad](https://arxiv.org/abs/2110.14048), [W0330 Nash-MTL](https://arxiv.org/abs/2202.01017), [W0332 Pitfalls](https://arxiv.org/abs/2006.07710v2), [W0335 Grokking](https://arxiv.org/abs/2201.02177v1), [W0338 induction emergence](https://arxiv.org/abs/2511.01033v2), and [W0344 Shortcut Learning](https://arxiv.org/abs/2004.07780v5). Their metadata/abstract status was recovered from the existing catalog, not newly elevated to full reading.

## 5. Checkpoint-first discrimination contract

This is a proposed analysis sequence, **not executed**. No checkpoint inventory or tensor load was performed here; existence and compatibility of actual saved times are unverified.

1. **Recover observability first.** List exact available timepoints, resolved configuration, training byte count, data cursor, seed, host/environment, stage flags, and whether optimizer/scaler/RNG state survives. Do not infer history that was not saved. Sparse checkpoints give interval-censored onset/disappearance, not a precise transition time.
2. **Use one fixed evaluation stream per comparison.** Compare matched local/remote content tasks, same windows and floor controls, long delays and multiple pages where relevant. Training seed must not silently change the examination set; hardware differences must not be interpreted as a schedule effect.
3. **Track four different observables.** (a) representation/probe access; (b) unmodified native reader returning the right content; (c) final prediction dependence under same-type natural content replacement; (d) task risk. A probe may need fitting—this is a new supervised analysis with its own budget, not “no training whatsoever.” It must not be silently reported as a zero-training checkpoint measurement.
4. **Separate diagnosis costs.** Forward-only substitutions and activations are checkpoint evaluation; task-gradient recomputation and curvature require backward passes but no parameter updates; new probes require fitting; resumed writer/reader adaptation is new training. Optimizer-dependent actual-update attribution is unavailable if optimizer history was not retained. Reinitializing missing Adam state is a different experiment, not recovery of the original update.
5. **Separate path changes from content changes.** Keep addresses/shape/norm and unrelated content controls as matched as practical. Cross-check full path masking against natural wrong-content replacement; a mask can create an abnormal input. A cross-time payload-reader splice changes interface distribution; include same-time self-splice and identity controls before calling it coadaptation failure.
6. **Do not select the best historical mechanism using test labels.** Define metrics/direction families on separate analysis data, hold out seeds/windows, retain negative/null checkpoints, and report the whole observed trajectory. Endpoint-selected circuit directions are descriptive.

A useful qualitative decision matrix is: probe and native use both absent → compatible with missing information **or** weak diagnostics; probe present/native read absent → reader/address/optimization gap candidate; native read present/final content dependence absent → consumer bypass candidate; dependence peaks then falls while loss improves → mechanism replacement candidate. None uniquely identifies cause without matched interventions.

## 6. Independent alternatives with no deployment source revisit

| Alternative | Hypothesis it tests | Smallest discriminating control; what would refute the simple version |
|---|---|---|
| Two-time-scale writer/consumer optimization | Writer initially cannot supply usable features before consumer learns a bypass | Same compute devoted to writer-extra, consumer-extra, or ordinary joint training; failure of writer-extra with an independently usable payload weakens the lag explanation |
| Frozen payload, native consumer adaptation | Information survives but original deployed reader did not learn it | Fixed payload, same reader family, same supervision and budget; strong external probe alone is insufficient |
| Temporary bypass weakening then restoration | Early error reduction starves the harder path, but the bypass is useful later | Equal-magnitude random attenuation and normal bypass; track persistence after restoration; slower formation without bypass is a relevant counterexample |
| Task-related auxiliary with isolated gradients | Full-state reconstruction directs the wrong component toward irrelevant fidelity | Full-state vs attention-response vs direct intermediate content supervision; stop-gradient destination separated; same auxiliary data/compute |
| Delayed bottleneck/rate pressure | Early rate restriction suppresses slower information dimensions | Soft/continuous or weak-rate phase then same final bottleneck; reverse order and constant-rate controls; not automatic support for VQ if the architecture is continuous |
| Consumer-first objective pressure | Easy reconstruction fixes an interface before prediction can shape it | Constant-total-budget stage order with entropy/scale held consistent where applicable; GenFirst does not justify dropping needed information |
| Relative initialization / learning-rate balancing | Same nominal capacity lies in a poorly feature-learning parameterization | Match initial function and activation variance where feasible; change one scale or optimizer axis at a time |
| Diversity and anti-shortcut curriculum | Existing samples permit an easier strategy that outpaces general context use | Match cumulative data, label balance, difficulty, and final distribution; new task diversity also changes statistical support |
| Plasticity maintenance or selective refresh | A once-adaptable component loses ability to learn at a stage boundary | Compare optimizer-only reset, selective refresh, ordinary continuation, and from-scratch within matched budgets; preserve previous-task performance |
| Persistence-aware checkpoint choice or regularization | Desired use is transient rather than never formed | Predefined held-out content metric and ordinary loss-based selection; no test-based cherry-picking; report generation/task-quality tradeoffs |

These are competing hypotheses, not instructions to implement all arms. Literature discovery is sufficient to keep them live; it is not sufficient to select one.

## 7. Recent-source and venue boundaries

Recent additions include September 2026 VQ warm-up revision, August 2026 GenFirst, July 2026 variance-equalization VAE, and October 2026 language-model checkpoint diagnostics. W0366 and W0048 already supply 2026 sources through existing full cards. Historical controls span exact linear dynamics, deep supervision, lagging inference, feature competition, and gradual unfreezing.

The λ-VAE source, 2607.05531v1, is retained as a **critical-reading** candidate, not a new unified explanation. Its §3.2 equates information through a deterministic continuous encoder with an entropy expression; finite/discrete versus differential-information assumptions need checking. Its decay-model propositions and empirical threshold must not become a universal diagnostic. GenFirst PDF extraction contains duplicated text and incomplete formula rendering; qualitative schedule details were readable, proofs and exact equations are not certified.

ICLR 2027 official group and three forums were requested, but the group rendered a loading shell and forums a browser-verification challenge. Search-engine-indexed anonymous submission labels are not official acceptance verification. These leads remain blocked; no author deanonymization, acceptance claim, review-based experimental fact, or exhaustive venue coverage is asserted.

## 8. Remaining work and delivery boundary

Priority is the 13-item precise reading queue, then deciding which checkpoint analyses are actually observable. Remaining blind spots include optimizer-noise/momentum-specific dynamics, language-model deep supervision at scale, and exact multi-loss curvature guarantees. The new literature does not directly establish an all-history same-direction FLUED shortcut mechanism. No experiment, training, production change, source upload, install, paid access, or commit was performed. This folder is a discovery handoff; final broad-report synthesis remains with the designated report owners.
