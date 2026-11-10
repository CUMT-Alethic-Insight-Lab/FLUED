# A05 — Versioned works, prior problems, mechanisms, and discriminating hypotheses

Date: 2026-11-09. This is an axis-specific discovery inventory, not a new global catalog. No new W/BIW IDs are assigned. **LD-N01–11 preserve the previous learning-dynamics recovery aliases. A05-N01–11 are local additions.** Stable identifiers, not title variants or multiple versions, define a work.

## Evidence and classification conventions

- **R**: recovered from the previous A05 audit/search log. Not new to the research effort. **C**: existing canonical catalog entry. **N**: absent from the two canonical work catalogs under the stable-ID/title searches performed; local novelty only, not scientific novelty or a claim about every uncataloged file.
- **A**: original abstract/version/official metadata read. **P**: specified original sections read, not full reading. **RF**: existing actual scoped FULL card reused, not a newly completed reading. Merely fetching a long HTML/PDF is not P or FULL for every section.
- **T/E** describe theory and empirical evidence supplied by authors, not independent verification. “Distinguishes” below means a useful experimental contrast, not that the cited work identifies the local cause.
- Visibility and units are explicit where relevant. Most learning-dynamics works do not have a retrieval source, index, or eviction mechanism. Their lack of source revisit is not an omission to repair.

There are **22 recovered/additional works** in §§1–2 (11 R, 11 N), **10 RF W-card reuses plus one separate RF byte card** in §3, seven catalog-unread references in §4, and three blocked anonymous ICLR 2027 leads in §5. These categories are not a total of new full readings. New FULL count is zero.

## 1. Recovered prior candidates, with fresh checks where available

### LD-N01 = BIW-0096 — Lagging Inference Networks and Posterior Collapse in Variational Autoencoders

- **Identity/version/status:** [1901.05534v2](https://arxiv.org/abs/1901.05534v2), 2019-01-28; ICLR 2019 according to prior recovery/PDF identity. [Pinned HTML](https://arxiv.org/html/1901.05534v2). R + C: byte catalog BIW-0096 already marks selected-primary/recovery, no FULL card.
- **Prior problem:** the inference encoder may fail to track the generator's changing true posterior at the beginning, encouraging the decoder to ignore the latent variable.
- **One-sentence solution:** aggressively update the inference network before generator updates, with mutual-information-dependent control of the aggressive phase.
- **Borrowed AI mechanisms:** amortized variational inference, ELBO optimization, alternating/two-time-scale training, mutual-information monitoring; the schedule changes optimization rather than the memory architecture.
- **Evidence depth:** fresh A and HTML abstract/introduction; prior P covered §§2–4/6 selectively, not all appendix experiments. T/E in variational text/image models. No new FULL claim.
- **Units/visibility/controls:** observations → stochastic latent posterior → autoregressive observations; encoder has observed input during inference training. Compare aggressive inference with ordinary training and other collapse remedies; equal-step is not automatically equal-compute.
- **Distinguishing hypothesis:** delayed writer/inference learning versus a representation that is intrinsically insufficient. A deterministic compressor has no true variational posterior; transfer is an optimization analogy, not identity.

### LD-N02 — Deeply-Supervised Nets

- **Identity/version/status:** [PMLR 38:562–570](https://proceedings.mlr.press/v38/lee15a.html), AISTATS 2015 final proceedings; [official PDF](https://proceedings.mlr.press/v38/lee15a.pdf); arXiv alias 1409.5185. R, absent from the two searched canonical catalogs.
- **Prior problem:** final-layer classification supervision provides indirect learning signals to intermediate layers and may leave them hard to optimize or insufficiently discriminative.
- **One-sentence solution:** add companion discriminative objectives at hidden layers alongside the output objective.
- **Borrowed AI mechanisms:** deep supervision, layer-local classifiers, stochastic optimization and attenuated/thresholded companion objectives; not an autoencoding loss.
- **Evidence depth:** fresh official A; recovered P on §§2.1–2.3/3.1, local strong-convex/common-optimum assumptions, not all proofs/tables. T/E in vision classification.
- **Units/visibility/cost:** images → hidden representations → class labels, with extra training heads and target labels available at intermediate layers; no query or source retrieval. Extra heads/backprop must be counted even if discarded at inference.
- **Distinguishing hypothesis:** poorly supervised intermediate feature formation versus insufficient reconstruction. Local theory is not a guarantee for arbitrary nonconvex byte models.

### LD-N03 — Critical Learning Periods in Deep Networks / arXiv title: Critical Learning Periods in Deep Neural Networks

- **Identity/version/status:** [1711.08856v3](https://arxiv.org/abs/1711.08856v3), 2019-02-25; ICLR 2019 per prior recovery. R; title variant retained rather than split into works.
- **Prior problem:** a temporary early stimulus deficit can leave a persistent performance deficit after normal inputs are restored.
- **One-sentence solution:** study timed input deprivation and recovery, relating the trajectory to Fisher-information connectivity/plasticity.
- **Borrowed AI mechanisms:** staged data perturbation, representation/plasticity diagnostics, Fisher information; primarily an explanatory experiment, not a deployable memory module.
- **Evidence depth:** fresh A confirms recovery counterexample; recovered P on early blur, constant-learning-rate controls, Fisher interpretation; no FULL or independent irreversibility proof.
- **Controls/limits:** low-level visual degradation differs from flips/label permutations, which can recover. Onset, duration, network size and finite recovery horizon matter; “all early errors are irreversible” is contradicted.
- **Distinguishing hypothesis:** early path-dependent formation versus a reversible stage/interface disturbance. Requires timed continuation to establish causation locally.

### LD-N04 — ForkMerge: Mitigating Negative Transfer in Auxiliary-Task Learning

- **Identity/version/status:** [2301.12618v3](https://arxiv.org/html/2301.12618v3), 2023-11-16; NeurIPS 2023, [official proceedings PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/60f9118a849e8e9a0c67e2a36ad80ebf-Paper-Conference.pdf). R.
- **Prior problem:** coordinating gradient conflicts may miss auxiliary-task negative transfer arising in validation/generalization rather than training descent.
- **One-sentence solution:** periodically fork branches with different task weights and merge them using target validation performance.
- **Borrowed AI mechanisms:** auxiliary-task learning, validation-driven task-weight search, parameter interpolation/branch merging; branch cost and validation-label permissions are part of the method.
- **Evidence depth:** fresh P, §3 definitions/§3.1–3.2 and Fig.2 caption. Fig.2 takes **one update from common intermediate parameters**, not independent full trajectories with all-history aligned gradients.
- **Controls/limits:** target Painting/Quickdraw in DomainNet, other domains auxiliary; L2 regularization contrast; task weight changes the fitted mixture. Validation transfer gain and training gradient cosine measure different objects.
- **Distinguishing hypothesis:** “aligned gradients imply no negative transfer” versus a generalization mismatch; not a proof that two aligned local objectives jointly cause the same compressed-content shortcut.

### LD-N05 — Strategy Coopetition Explains the Emergence and Transience of In-Context Learning

- **Identity/version/status:** [2503.05631v2](https://arxiv.org/html/2503.05631v2), 2025-03-10; ICML 2025 venue association recovered, exact proceedings/arXiv version equivalence unverified. R.
- **Prior problem:** ICL can emerge and disappear; a binary “context versus weights” explanation hides the role of contextual constraints and shared circuitry.
- **One-sentence solution:** distinguish context-constrained in-weights learning from general ICL and trace their cooperating and competing subcircuits across training.
- **Borrowed AI mechanisms:** mechanistic circuit decomposition, evaluator contrasts, formation-time clamping, simplified dynamical models.
- **Evidence depth:** fresh P for Fig.1 and beginning; recovered P §§2–5; appendices not completed. Synthetic Omniglot two-layer attention-only model, not a general language-model result.
- **Controls/counterexample:** late hybrid still needs label clues in context; downstream circuit survives with a changed role; an eventually competing strategy can help the desired strategy form. MLP variants can show resurgence, cautioning against asymptotic universal claims.
- **Distinguishing hypothesis:** absent mechanism versus repurposed mechanism; bypass always harmful versus stage-dependent cooperation.

### LD-N06 — How Language Models Develop In-Context Learning (body prefix: From Copying to Composition)

- **Identity/version/status:** [2610.19113v1](https://arxiv.org/html/2610.19113v1), 2026-10-13; preprint, formal venue/status not verified. R, not a newly discovered work in this pass.
- **Prior problem:** accuracy does not identify when task-relevant prompt control, answer preference, output construction and transfer develop.
- **One-sentence solution:** make copying and applying prompt definitions predict different answers, then follow checkpoints and matched task-practice interventions.
- **Borrowed AI mechanisms:** controlled compositional diagnostic, content-source interventions, checkpoint trajectories, synthetic/rewritten-document fine-tuning.
- **Evidence depth:** fresh P abstract/introduction/Fig.1 and release/change-plan paragraphs; recovered P §§5–8 and appendix restrictions. External supplement incomplete/unread; no FULL.
- **Units/controls/cost:** token LMs, prompt definitions and conflicting examples; distinguish choosing candidates from generating the correct string. Matched ordinary-document fine-tuning is not the same as definition exercises. Appendix O reports approximately 320 H100 GPU-hours; post-plan changes are explicitly recorded in P.
- **Distinguishing hypothesis:** contextual control exists before answer mastery versus no usable mechanism; removing copying does not automatically teach construction or transfer. Exact thresholds and all supplement outcomes remain unverified.

### LD-N07 — From Lazy to Rich: Exact Learning Dynamics in Deep Linear Networks

- **Identity/version/status:** [2409.14623v2](https://arxiv.org/html/2409.14623v2), 2025-03-04; preprint version pinned, final venue/version relation unverified. R.
- **Prior problem:** absolute initialization scale alone does not characterize how relative encoder/decoder scale determines feature evolution.
- **One-sentence solution:** derive exact deep-linear learning solutions for layer-relative λ-balanced initializations spanning static-feature and feature-learning regimes.
- **Borrowed AI mechanisms:** matrix gradient flow, balanced factorization, neural-tangent-kernel/representation dynamics.
- **Evidence depth:** fresh A/introduction; recovered P for assumptions including whitened inputs and balanced layers; extensive appendix uncompleted.
- **Units/limits:** real-vector regression/representations, no source-index lifecycle. Linear maps still have nonlinear parameter dynamics; function matching, parameter matching, and activation matching are distinct.
- **Distinguishing hypothesis:** capacity bottleneck versus an initialization/parameterization that prevents useful representation change. No direct guarantee for nonlinear Adam training.

### LD-N08 — Don't Blame the ELBO! A Linear VAE Perspective on Posterior Collapse

- **Identity/version/status:** [1911.02469v1](https://arxiv.org/abs/1911.02469v1), 2019-11-06; NeurIPS 2019 as recovered from official proceedings. R.
- **Prior problem:** collapse is often attributed exclusively to the variational bound or a powerful autoregressive decoder.
- **One-sentence solution:** analyze linear VAEs through probabilistic PCA and distinguish marginal-likelihood stationary geometry from additional effects of approximate inference.
- **Borrowed AI mechanisms:** linear Gaussian latent models, probabilistic PCA, exact variational inference, stationary-point/stability analysis.
- **Evidence depth:** fresh A; recovered P §§3–4/6 and A.1; proofs not independently verified, not FULL.
- **Controls/limits:** observation-noise setting and fixed versus learned noise change stationary behavior. Exact-inference global optimum results do not certify arbitrary stochastic nonlinear trajectories.
- **Distinguishing hypothesis:** inference lag alone versus an objective/likelihood geometry that already supports latent non-use. Counterexample to universal blame, not a local diagnosis.

### LD-N09 — On Lazy Training in Differentiable Programming

- **Identity/version/status:** [1812.07956v5](https://arxiv.org/abs/1812.07956v5), 2020-01-07 revision; NeurIPS 2019 per recovered record. R.
- **Prior problem:** low training error near initialization is often explained solely by enormous network width.
- **One-sentence solution:** analyze scaling-induced linearization and bound the distance between original and linearized optimization paths.
- **Borrowed AI mechanisms:** kernel-limit analysis, parameter scaling, gradient-flow comparison.
- **Evidence depth:** fresh A/version history only; original proofs/body unread in this stream. T plus author-reported vision experiments.
- **Limits/cost:** good training fit need not imply useful newly learned features; scaling can change numerical/optimization behavior while preserving nominal capacity. No automatic recommendation to shrink or enlarge every layer.
- **Distinguishing hypothesis:** unused memory because there is insufficient capacity versus because feature formation is suppressed by optimization regime.

### LD-N10 — The Transient Nature of Emergent In-Context Learning in Transformers

- **Identity/version/status:** [2311.08360v3](https://arxiv.org/abs/2311.08360v3), 2023-12-11; NeurIPS 2023 per recovery. R.
- **Prior problem:** treating a newly emerged ICL capability as permanently retained hides potential late replacement during continued loss improvement.
- **One-sentence solution:** track synthetic-task ICL through extended training and test regularization for greater persistence.
- **Borrowed AI mechanisms:** long-horizon checkpoint evaluation, competing-strategy tasks, L2 regularization.
- **Evidence depth:** fresh original A/version; not full original reading. Read together with LD-N05's later, more specific mechanism account.
- **Controls/limits:** both contextual and weight-based solutions can fit training data; late behavior must not be described as universally context-free after the later hybrid-strategy finding.
- **Distinguishing hypothesis:** never formed versus formed then displaced while loss continues downward; establishes an existence example, not a general inevitability.

### LD-N11 — Residual Feature Integration is Sufficient to Prevent Negative Transfer

- **Identity/version/status:** [ICLR 2026 official poster/abstract](https://iclr.cc/virtual/2026/poster/10008648), [2505.11771](https://arxiv.org/abs/2505.11771); preprint may include REFINE prefix. **Preprint revision number not freshly established**; official conference abstract is the operative source. R.
- **Prior problem:** transferred source features can harm target learning under distribution shift.
- **One-sentence solution:** retain frozen source features and learn a target-side residual encoder for signals the source representation missed.
- **Borrowed AI mechanisms:** frozen feature transfer, residual feature integration, nonparametric convergence analysis.
- **Evidence depth:** fresh official A only; theory/proofs and precise target distribution class remain unread.
- **Limits/cost:** guarantee described as no worse convergence rate than scratch up to logarithmic factors within an informative distribution class, not every finite-budget target task. Target-side capacity/adaptation is additional and must be counted.
- **Distinguishing hypothesis:** preserving a fixed useful route necessarily prevents adaptation versus complementary residual learning; this is a cross-axis transfer control, not evidence that every local bypass is benign.

## 2. Additional verified works absent from the searched canonical catalogs

### A05-N01 — Learning Dynamics in Linear VAE: Posterior Collapse Threshold, Superfluous Latent Space Pitfalls, and Speedup with KL Annealing

- **Identity/version/status:** [PMLR 238:1936–1944](https://proceedings.mlr.press/v238/ichikawa24a.html), AISTATS 2024 final proceedings; [PDF](https://proceedings.mlr.press/v238/ichikawa24a/ichikawa24a.pdf). N; Yuma Ichikawa and Koji Hukushima.
- **Prior problem:** neither static optima nor the statement “train longer” specifies when a VAE learns useful dimensions, overfits surplus latents, or collapses.
- **One-sentence solution:** derive a large-input-dimension deterministic limit for minimal-VAE learning and analyze fixed points and KL-annealed trajectories.
- **Borrowed AI mechanisms:** dynamical mean-field/large-dimensional analysis, latent regularization, annealing.
- **Evidence depth:** A from formal metadata/abstract, not full proof reading. Author T: collapse threshold, surplus-latent overfitting, schedule-dependent convergence.
- **Units/controls/limits:** minimal linear generative/recognition vectors; not byte/source retrieval. The schedule may accelerate convergence without defeating a limiting regularization threshold. Exact assumptions, comparison compute, and full equations remain reading questions.
- **Distinguishing hypothesis:** finite optimization delay versus a stable objective-induced collapsed regime; increasing nominal latent capacity may worsen the trajectory.

### A05-N02 — Continuous First, Discrete Later: VQ-VAEs Without Dimensional Collapse

- **Identity/version/status:** [2605.06870v3](https://arxiv.org/html/2605.06870v3), 2026-09-27; v1 2026-05-07. Preprint; no official venue/acceptance established. N.
- **Prior problem:** increasing vector-quantization codebook size or using every code can fail to improve reconstruction because the learned representation occupies very few directions.
- **One-sentence solution:** train an unquantized autoencoder until enough modes develop, then introduce quantization within the same total training-step/epoch budget.
- **Borrowed AI mechanisms:** sequential mode learning from Saxe-style autoencoders, rate-distortion reverse water-filling, PCA spectra, delayed quantization, k-means initialization/EMA/respawn.
- **Evidence depth:** fresh P §3.3 theorem statement, §§4–5, Table 1/2 captions, Appendix B settings and β=0 counterexample text. Not all proofs, numeric tables, plots or code; not FULL.
- **Units/cost:** image/audio latents, not language bytes; 100k-step image ablation and 100-epoch audio comparison exchange AE and VQ steps. Audio uses one seed and roughly seven days on two H200s/run. Equal steps is not independently verified equal FLOPs.
- **Controls/counterexample:** respawn-only and larger-codebook controls; removing commitment can raise codebook PCA dimension merely because unused random codes remain, without better reconstruction. Warm-up is not a learning-rate ramp. The diagonal Gaussian rate-distortion theorem is not a nonlinear-memory permanence theorem.
- **Distinguishing hypothesis:** actual nominal capacity shortage versus an early training restriction that prevents weak modes from forming. Rank must be measured on utilized payloads, not arbitrary unassigned vectors.

### A05-N03 — GenFirst: Generation Before Reconstruction for Stable End-to-End Latent Generative Modeling

- **Identity/version/status:** [2608.29335v1](https://arxiv.org/abs/2608.29335), 2026-08-29; [PDF](https://arxiv.org/pdf/2608.29335v1) has internal date September 1. Preprint, formal venue unknown. N; date discrepancy recorded rather than silently normalized.
- **Prior problem:** reconstruction-optimized latents may be difficult for a generative prior; naive end-to-end training can collapse, and fast reconstruction can dominate slower distribution learning.
- **One-sentence solution:** preserve posterior entropy and give the generative objective early relative priority, then reduce prior/entropy weights to refine reconstruction.
- **Borrowed AI mechanisms:** continuous autoregressive priors, Gaussian-mixture heads, flow matching, posterior-entropy preservation, staged objective weighting and later frozen-encoder training.
- **Evidence depth:** fresh P PDF §§3.1–3.3/4.3/5.1–5.2; formula extraction incomplete/duplicated and later pages/appendices not fully examined. Not FULL or numerical certification.
- **Controls/cost:** constant weighting/cosine/PI comparisons; larger latent/VAE/prior controls do not remove the reported tradeoff. In §4.3 reconstruction weights remain fixed; prior and entropy weights decrease together. Diffusion pipeline subsequently freezes VAE for prior-only training—include that budget. Some headline outcomes include additional stages and different initializations.
- **Distinguishing hypothesis:** reconstruction-first necessarily helps versus reconstruction anchoring the wrong latent geometry; compare with N02 rather than treating the two schedules as interchangeable.

### A05-N04 — λ-VAE: Variance Equalization for Posterior Collapse

- **Identity/version/status:** [2607.05531v1](https://arxiv.org/abs/2607.05531v1), 2026-07-06; [HTML](https://arxiv.org/html/2607.05531v1) heading omits λ-VAE prefix. Preprint, venue unverified. N; Girum Demisse.
- **Prior problem:** reconstruction/regularization gradient imbalance and information lost at stochastic sampling may jointly make collapse cheap.
- **One-sentence solution:** scale sampling noise using per-dimension exponents while retaining the original variance in the KL penalty.
- **Borrowed AI mechanisms:** Gaussian reparameterization, per-dimension gradient-balance analysis, information-theoretic objective and posterior variance control.
- **Evidence depth:** fresh P §§3.1–3.2 and proposition assumptions, not empirical tables/appendix proof completion. Author T/E; not an independently established unified account.
- **Controls/limits:** specified decay exponent controls the gradient-ratio argument; the reported operative threshold is model/dataset-specific. The deterministic continuous-encoder information/entropy equalities in §3.2 require explicit mathematical auditing; continuous differential entropy does not automatically obey discrete identities. The asymmetric sampling modification must also be checked for what distribution/objective is actually optimized.
- **Distinguishing hypothesis:** gradient-force imbalance versus loss between computed representation and sampled code. Not directly applicable to a deterministic compressor with no such sampling step.

### A05-N05 — Competition Dynamics Shape Algorithmic Phases of In-Context Learning

- **Identity/version/status:** [2412.01003v4](https://arxiv.org/html/2412.01003v4), 2025-05-02; v1 2024-12-01. Preprint verified; publication status not certified from ambiguous search associations. N.
- **Prior problem:** distinct synthetic ICL studies can support conflicting mechanisms because model behavior mixes multiple algorithms.
- **One-sentence solution:** train on finite mixtures of Markov chains and decompose behavior into fuzzy retrieval/inference using unigram/bigram contextual statistics.
- **Borrowed AI mechanisms:** Markov sequence generators, explicit algorithm baselines, checkpoint phase analysis, context-length/task-diversity sweeps.
- **Evidence depth:** fresh A and P introduction plus Appendix discussion distinguishing optimization-limited from diversity-limited emergence; detailed experiments and appendix not fully read.
- **Units/visibility:** symbolic sequence next-token prediction; “retrieval” here is an algorithmic behavioral baseline, not permission to revisit a stored source corpus. Multiple algorithms see the same causal sequence prefix but use different statistics.
- **Distinguishing hypothesis:** longer context/training necessarily strengthens one memory computation versus causing algorithm replacement. Source-level causal attribution and exact mixture-identification uncertainty remain reading tasks.

### A05-N06 — Differential learning kinetics govern the transition from memorization to generalization during in-context learning

- **Identity/version/status:** [2412.00104v2](https://arxiv.org/html/2412.00104v2), 2024-12-12; [ICLR 2025 official proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/187f9ba4cd5a59477305ac712282a1cd-Abstract-Conference.html). N; Alex Nguyen and Gautam Reddy. Formal version differs potentially; not a completed version comparison.
- **Prior problem:** a diversity threshold for ICL is often read as exceeding the capacity to memorize, without analyzing the relative rates of competing solutions.
- **One-sentence solution:** reduce a synthetic transformer to memorization and attention-based generalization circuits and explain threshold/onset statistics through their differential learning kinetics.
- **Borrowed AI mechanisms:** additive-logit independence ansatz, scalar query/key and value order parameters, gradient-flow approximations, memorization scaling.
- **Evidence depth:** fresh P §§3.2–3.4, including large-dimension and small-initialization assumptions; full appendix and experimental controls unread. Theory/empirical source, not replication.
- **Controls/limits:** reduced model separates MLP memorization and attention ICL; retains contextual-label fluctuations in the expansion. Appendix plots include seeds that never acquire ICL, acquired-but-not-yet-transient runs, and observed transience—these are censored outcomes, not interchangeable negatives.
- **Distinguishing hypothesis:** limited parameter capacity versus a race between solutions; counterpoint to LD-N05 because independence is an ansatz here, not a universal rejection of shared circuits.

### A05-N07 — Universal Language Model Fine-tuning for Text Classification

- **Identity/version/status:** [ACL 2018 P18-1031](https://aclanthology.org/P18-1031/), pp.328–339; [official PDF](https://aclanthology.org/P18-1031.pdf). N; Jeremy Howard and Sebastian Ruder. Use the proceedings version, not an assumed arXiv equivalence.
- **Prior problem:** aggressive fine-tuning forgets transferred language knowledge, while cautious adaptation can underfit or learn slowly.
- **One-sentence solution:** combine task LM adaptation and classifier training with layer-dependent learning rates, a slanted-triangular rate schedule, and gradual unfreezing.
- **Borrowed AI mechanisms:** AWD-LSTM transfer, discriminative layer rates, staged thawing, pooled document representations, supervised classification.
- **Evidence depth:** fresh P §§3.2–3.3/5 and Table 7 discussion; all table cells/appendix/source code not read, not FULL.
- **Controls/counterexample:** last-layer only, full, chain-thaw, gradual unfreezing, and rate schedules. Gradual unfreezing alone is reported similar to full; last-layer only underfits; benefits are not universally attributable to freezing. Validation tunes epochs, different rates apply, and bidirectional results use a separately trained model.
- **Distinguishing hypothesis:** fixed-feature consumer adaptation sufficient versus needing coordinated representation readaptation; freeze schedule versus learning-rate confounding.

### A05-N08 — The Dormant Neuron Phenomenon in Deep Reinforcement Learning

- **Identity/version/status:** [PMLR 202:32145–32168](https://proceedings.mlr.press/v202/sokar23a.html), ICML 2023; arXiv alias 2302.12902. N; Ghada Sokar, Rishabh Agarwal, Pablo Samuel Castro, Utku Evci.
- **Prior problem:** neurons can become inactive during reinforcement-learning training, reducing usable network expressivity.
- **One-sentence solution:** detect and recycle dormant neurons throughout learning with ReDo.
- **Borrowed AI mechanisms:** activation-utility monitoring, selective weight reinitialization and continued training.
- **Evidence depth:** official A only; reset details, replay/update-ratio controls and old-skill retention need full reading.
- **Limits/cost:** RL target/data nonstationarity differs from stationary language modeling. Dormancy is not equivalent to information loss, low representation rank, or missing curvature; compare N09/N11. Resets can erase useful features and require recovery computation.
- **Distinguishing hypothesis:** unused units and declining trainability versus unchanged active representation with a consumer bypass. Not an automatic instruction to recycle memory units.

### A05-N09 — DASH: Warm-Starting Neural Network Training in Stationary Settings without Loss of Plasticity

- **Identity/version/status:** [NeurIPS 2024 official PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/4c5ce1fc8895076f49935951a630be5c-Paper-Conference.pdf), [2410.23495v2](https://arxiv.org/abs/2410.23495), 2024-11-01. N; proceedings version operative for section claims, exact arXiv diff not checked.
- **Prior problem:** warm-starting can generalize worse than scratch even as new samples arrive from a stationary distribution.
- **One-sentence solution:** selectively shrink weight directions judged to encode noise while preserving learned feature directions at data-expansion boundaries.
- **Borrowed AI mechanisms:** discrete feature/noise learning model, gradient/weight alignment, per-neuron direction-aware shrinking, expanding-data curricula.
- **Evidence depth:** fresh P §§2–5; proofs/appendices not fully read. The abstract framework is deliberately not an exact hypothesis-class SGD theorem.
- **Controls/counterexample/cost:** cold/warm/shrink-and-perturb, stationary chunks, train-to-99.9% stopping, steps-to-convergence reporting. Dormant-unit revival/normalization/nonstationary fixes need not transfer; strong standard-training settings approach rather than beat cold-start performance. Repeated gradient estimation and return-to-convergence are not free.
- **Distinguishing hypothesis:** data-distribution shift is necessary for plasticity loss versus path-dependent learning under stationary data. Not a local proof that memorized noise explains compressor behavior.

### A05-N10 — Exact solutions to the nonlinear dynamics of learning in deep linear neural networks

- **Identity/version/status:** [1312.6120v3](https://arxiv.org/abs/1312.6120v3), 2014-02-19; ICLR 2014 association via [Oxford institutional record](https://ora.ox.ac.uk/objects/uuid:49f24917-64cc-4d41-ba52-7aabc67662ce) found in search; institutional full record not fetched in this pass, so venue is not independently re-audited. N; Andrew M. Saxe, James L. McClelland, Surya Ganguli.
- **Prior problem:** a linear input-output map can still have nonlinear, slow or abrupt parameter-learning dynamics as depth/initialization change.
- **One-sentence solution:** solve restricted deep-linear gradient dynamics and compare random, orthogonal and unsupervised-pretrained initial conditions.
- **Borrowed AI mechanisms:** singular-mode decomposition, gradient flow, orthogonal initialization and layerwise pretraining.
- **Evidence depth:** fresh A/version only; formal solutions and conditions await reading.
- **Limits:** exact linear dynamics do not identify nonlinear model circuits. Sequential mode formation and finite depth delays are existence/conditional results, not evidence of an actual byte-memory bottleneck.
- **Distinguishing hypothesis:** endpoint capacity failure versus a slow trajectory through learnable modes; original baseline for LD-N07/N02 rather than treating their ideas as isolated recent inventions.

### A05-N11 — Directions of Curvature as an Explanation for Loss of Plasticity

- **Identity/version/status:** [2312.00246v2](https://arxiv.org/html/2312.00246v2), 2024-02-17. The abstract-page record uses *Curvature explains loss of plasticity* and lists v4 2024-10-05; title/version drift is retained, not silently equated. Preprint; no formal acceptance verified. N.
- **Prior problem:** shrinking update norms, dead units and feature-rank reduction do not consistently explain failure to learn successive tasks.
- **One-sentence solution:** test counterexamples and track loss of curvature directions, proposing a distributional regularizer to preserve plasticity.
- **Borrowed AI mechanisms:** task-switch benchmarks, activation controls, Hessian effective-rank diagnostics, empirical-Fisher/per-example-gradient Gram approximation, distributional regularization.
- **Evidence depth:** fresh P §§3–4 and Fig.1/2 captions, plus abstract; not full experiments/proofs. Curvature co-occurrence and regularizer evidence are author observations, not exclusive-cause proof.
- **Controls/counterexamples:** ReLU/leaky-ReLU/tanh/identity with 200 epochs/task; update norm can rise while plasticity falls; feature-rank regularization can fail despite higher rank. Proxy Hessian rank is sample-limited and not exact; Fisher, empirical Fisher, Gauss–Newton and Hessian are distinct.
- **Distinguishing hypothesis:** simple inactive/rank-poor representation versus an optimization-landscape limitation. Supplies a counter-control to adopting N02/N08 diagnostics universally.

## 3. Reuse, not new papers or readings

The actual cards below were read in this pass. Each card fixes reading scope and version; old FULL does not mean code, theorem or effect reproduction.

| ID and stable title/version/status | Prior problem → one-sentence solution; borrowed mechanisms | Evidence / hypothesis and restrictions |
|---|---|---|
| W0328 = BIW-0022, [Gradient Surgery for Multi-Task Learning, 2001.06782v4](https://arxiv.org/pdf/2001.06782v4), NeurIPS 2020 | Harmful multi-task optimization → project conflicting shared gradients; taskwise backprop, vector projection | RF [card](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0328.md); direction/scale/curvature vs conflict alone; retain A.3 audit limitation |
| W0331 = BIW-0023, [Adapting Auxiliary Losses Using Gradient Similarity, 1812.02224v2](https://arxiv.org/pdf/1812.02224v2), 2020 revision, formal venue unverified | Harmful auxiliaries → gate by current gradient alignment; cosine weighting/private heads | RF [card](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0331.md); local descent vs finite-budget improvement; Appendix B/F and perfect-teacher counterexamples |
| W0333, [Gradient Starvation: A Learning Proclivity in Neural Networks, 2011.09468v4](https://arxiv.org/pdf/2011.09468v4), NeurIPS 2021 | Strong feature suppresses weaker response → decouple through output-logit regularization; linearized/dual analysis | RF [card](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0333.md); formation starvation vs full network information absence; test-environment tuning caveat |
| W0334, [Complexity Matters: Dynamics of Feature Learning in the Presence of Spurious Correlations, 2403.03375v3](https://arxiv.org/pdf/2403.03375v3), 2024 preprint version | Unknown core/shortcut chronology → vary feature difficulty/correlation and follow native/retrained readout; controlled Boolean tasks | RF [card](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0334.md); simultaneous formation/forgetting counterexamples; appendix mathematical issue retained |
| W0336, [Progress measures for grokking via mechanistic interpretability, 2301.05217v3](https://arxiv.org/pdf/2301.05217v3), ICLR 2023 | Accuracy hides gradual circuit progress → Fourier circuit projections/ablations across checkpoints | RF [card](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0336.md); mechanism progress vs performance jump; endpoint-selected frequencies are retrospective |
| W0337, [What needs to go right for an induction head? A mechanistic study of in-context learning circuits and their formation, 2404.07129v1](https://arxiv.org/pdf/2404.07129v1), 2024 preprint version | Compound induction circuit forms abruptly → disentangle transport/matching/copying with clamping and training controls | RF [card](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0337.md); formation vs endpoint necessity, compensation and initialization; clamping simplifies task |
| W0023, [Compressive Transformers for Long-Range Sequence Modelling, 1911.05507v1](https://arxiv.org/html/1911.05507v1), 2019 preprint version, ICLR 2020 work | Old activations exceed memory budget → compress FIFO history and train compressor with state/attention reconstruction; stop-gradient, BPTT | RF [card](../../../flued_multigranularity_survey_20261108/03_reading/B24/W0023.md); objective/gradient destination vs stronger reconstruction; rates and unroll differ |
| W0038, [In-context Autoencoder for Context Compression in a Large Language Model, 2307.06945v4](https://arxiv.org/html/2307.06945v4), ICLR 2024 | Frozen LM cannot directly consume compact context → learn LoRA encoder and memory tokens with AE+continuation then instruction training | RF [card](../../../flued_multigranularity_survey_20261108/03_reading/B24/W0038.md); reconstructability vs deployed QA/combination; extra multi-segment training matters |
| W0048, [Compression Beyond the Uncompressed: A Two-Stage Training Recipe for Soft Context Compression in RAG, 2609.05152v2](https://arxiv.org/pdf/2609.05152v2), 2026 preprint | Distillation inherits teacher failures → distill successes then apply answer-reward GRPO to failures | RF [card](../../../flued_multigranularity_survey_20261108/03_reading/B24/W0048.md); stage/data-selection effects vs compression advantage; matched-RL full source remains stronger |
| W0366, [Weight Tying Biases Token Embeddings Towards the Output Space, 2603.26663v1](https://arxiv.org/html/2603.26663v1), 2026 preprint | Shared input/output table shaped unequally → analyze path gradients/alignment and input-gradient scaling | RF [card](../../../flued_multigranularity_survey_20261108/03_reading/B14/W0366.md); path gradient scale vs representation capacity; mixed outcomes/single runs, not a byte/cosine factorial |
| BIW-0113, [The Strawberry Problem: Emergence of Character-level Understanding in Tokenized Language Models](https://aclanthology.org/2025.emnlp-main.1434.pdf), EMNLP 2025 proceedings pp.28252–28263 | Character access develops late in token LMs → add block-causal character Transformer/cross-attention under supervised transformations | RF [actual card](../../../byte_language_interface_survey/03_reading/R10/BIW-0113.md); delayed learnability vs inaccessible interface; 0.5% onset, extra input channel/parameters and synthetic objectives confound pure optimization |

## 4. Existing catalog-unread sources: retain identity and do not inflate discovery

These entries were recovered from canonical catalogs/audit, not freshly full-read. Version/venue below is the existing record, not a new source certification. They are selectively useful only if the missing question becomes decision-relevant.

| Identity, title, version/venue anchor | Prior problem → proposed solution / borrowed mechanism | Evidence and distinguishing question |
|---|---|---|
| W0327, [GradNorm: Gradient Normalization for Adaptive Loss Balancing in Deep Multitask Networks](https://proceedings.mlr.press/v80/chen18a.html), ICML 2018 final | Different task learning speeds → normalize/adapt gradient magnitudes; adaptive loss weights | Existing A, body unread; relative learning speed/scale vs gradient direction; budget/private-head updates need checking |
| W0329, [Conflict-Averse Gradient Descent for Multi-task Learning](https://arxiv.org/abs/2110.14048), NeurIPS 2021 record | Worst task can lose under shared updates → trade mean gradient improvement against conflict aversion; multi-objective descent | Existing A, body unread; worst-task guarantee vs desired content mechanism, local vs long-run conditions |
| W0330, [Multi-Task Learning as a Bargaining Game](https://arxiv.org/abs/2202.01017), ICML 2022 record | Task weights depend on arbitrary loss scales → use bargaining-based shared-gradient combination | Existing A, body unread; scale fairness vs main-task performance and content dependence |
| W0332, [The Pitfalls of Simplicity Bias in Neural Networks](https://arxiv.org/abs/2006.07710v2), NeurIPS 2020 work / v2 record | Simple predictive rules harm robust generalization → controlled simplicity-bias diagnosis and mitigation comparisons | Existing A, body unread; causal role of feature simplicity vs correlation; prefer original results to survey rhetoric |
| W0335, [Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets](https://arxiv.org/abs/2201.02177v1), 2022 preprint | Test generalization appears far after fitting → document delayed algorithmic generalization under extended training | Existing A; delayed performance vs capacity saturation; not an architecture prescription |
| W0338, [On the Emergence of Induction Heads for In-Context Learning](https://arxiv.org/abs/2511.01033v2), 2026-01-08 revision, preprint record | Unknown formation conditions → theoretical induction-head emergence analysis | Existing A; exact formation assumptions vs W0337 experimental model; not read sufficiently to import theorem |
| W0344, [Shortcut Learning in Deep Neural Networks](https://arxiv.org/abs/2004.07780v5), 2023 revision / Nature Machine Intelligence DOI 10.1038/s42256-020-00257-z | Benchmark success masks spurious solutions → organize shortcut concepts and evaluation failures | Existing A, survey; vocabulary/navigation, not original proof of a particular training pathway |

## 5. ICLR 2027 anonymous leads: identity/status verification blocked

Official group requested: [ICLR.cc/2027/Conference](https://openreview.net/group?id=ICLR.cc/2027/Conference). Fetch and built-in-browser DOM returned an unloaded shell, not a usable venue inventory. All three forums below returned verification challenges through the public Fetch route. Their titles/labels are search-index leads only. **Not accepted-paper records, not full readings, not part of the 22 verified/recovered works.** No author matching or deanonymization attempted.

| Local lead | Search-indexed title / stable forum / version-status limit | Potential prior problem and mechanism to verify; hypothesis | Depth |
|---|---|---|---|
| A05-L01 | [How Rare Counterexamples Change What Models Learn](https://openreview.net/forum?id=3us1m0de0C); snippet labels ICLR 2027 Conference Submission, date 2026-09-18; official revision/status unavailable | Whether rare anti-shortcut examples change acquisition or merely endpoint accuracy; method/solution/borrowed technique **not verified**, do not infer from title | Search only; forum challenge; no acceptance assertion |
| A05-L02 | [WHEN ANTI-COLLAPSE OBJECTIVES HAVE COL…](https://openreview.net/forum?id=ndfEYtpRRb); search PDF snippet says under review at ICLR 2027; **full exact title and revision unknown** | Whether anti-collapse objectives themselves admit collapsed solutions; concrete solution/technique unknown pending original source | Search only; forum challenge; no substantive finding used |
| A05-L03 | [When Local Sufficiency Fails at Finite Budgets](https://openreview.net/forum?id=aez0aKWAOB); search PDF snippet says under review at ICLR 2027; official version/date/status unknown | Whether a locally sufficient path fails under finite optimization; actual formulation/solution/borrowed mechanism unknown | Search only; forum challenge; no identity inference or acceptance claim |

Other broad-query hits (e.g. state-tracking learning dynamics, world-model dynamics, masked diffusion) were not enrolled solely because of venue keywords. The separate venue specialist can supply an officially verified forum record later; this stream must not manufacture coverage from search snippets.
