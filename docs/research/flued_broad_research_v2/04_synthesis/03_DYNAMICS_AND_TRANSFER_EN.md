# Learning Dynamics, Component Composition, and Transfer

## 1. What a final checkpoint cannot tell us

A model can fail to use a representation for several scientifically different reasons. The representation may never have contained the required distinction. A writer may have learned it before its reader learned a usable coordinate system. An initially useful route may have been replaced, repurposed, or made redundant. A transplant may preserve task information while violating the recipient's expectations about scale, normalization, timing, or companion paths. These explanations imply different interventions. They cannot be collapsed into a single verdict about compression, a dynamic router, or the need to revisit original text.

This chapter addresses all 22 learning-dynamics directions E.01–E.22 and all 19 composition/transfer directions F.01–F.19 in the [canonical 167-direction list](../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md). It also carries the assigned source-lifecycle questions R.09–R.10/R.12/R.16 and sequential-utility questions R.14–R.15, without allowing either to replace the main dynamics and transfer questions. Decoder masking and intermediate supervision connect to I.12; interface geometry and domain changes connect to the independent byte/interface investigation.

The evidence base combines completed V06–V07 and V13–V14 cards with earlier valid, version-scoped cards and the actual V17/V18 source returns distinguished in §13. These are reused readings, not new paper readings or replications performed for this chapter. [Coverage recheck R3](../05_review/COVERAGE_RECHECK_R3.md) updates the [R2 coverage assessment](../05_review/COVERAGE_RECHECK_R2.md); [reading audit R1](../05_review/READING_AUDIT_R1.md) and [reading audit R2](../05_review/READING_AUDIT_R2.md) retain their claim-specific corrections. Unavailable history, a missing supplement, source notation ambiguity, an officially blocked body, and an unperformed target-system comparison remain different gaps.

Four outcomes organize the comparison:

- **Acute dependence:** changing a component or its content immediately changes an already competent model.
- **Budgeted restoration:** specified adaptation recovers a demonstrated ability after a specified disruption.
- **Formation:** an ability emerges under a particular initialization, objective, data history, and schedule.
- **Practical selection:** a complete recipe reaches a favorable quality–resource frontier after development and adaptation.

Success on one outcome does not answer the others. A successful connector can be valuable without reproducing the sender's original computation. An unsuccessful repair can reveal an insufficient repair budget without establishing that the architecture cannot learn. A declining loss can coexist with declining dependence on a desired source. The useful conclusion from the literature is therefore a set of discriminating comparisons, not a preferred architecture selected from absent evidence.

## 2. Formation, disappearance, and the observability of history

### 2.1 Endpoint necessity is not formation necessity

The induction-head study gives a particularly direct separation. In a two-layer attention-only model trained on randomized-label Omniglot sequences, deleting individual heads at the endpoint often has little effect; retaining one important second-layer head can still support approximately 98% accuracy. Yet restricting formation to one second-layer head delays acquisition. Heads that are unnecessary individually in the mature network can contribute to how the network reaches that state. Parallel compensation and learning-history effects are both plausible, and they are different claims. [W0337, 2404.07129v1, §§3–5, Figs.4–6 and App.D](../../flued_multigranularity_survey_20261108/03_reading/B16/W0337.md).

The study's clamping interventions further separate previous-token transport, query–key matching, and value copying. More classes chiefly delay matching; more labels chiefly delay copying. These are concrete distinctions between learning an address and learning a returned value. They do not establish that every memory failure has the same bottleneck. Ideal clamping sometimes requires two forward passes and removes the need to superpose query/key and value representations. It changes the problem being learned, rather than merely observing it. Fixing a first layer trained under another seed also changes formation speed, making frozen pretrained features an active treatment rather than a neutral control.

A complementary example comes from modular arithmetic. Mechanistic progress measures reveal gradual formation before aggregate test accuracy improves: a restricted Fourier loss falls before ordinary test loss, while a residual memorization measure changes during cleanup. The crucial qualification is that the Fourier frequencies were identified from the endpoint model. They retrospectively describe the observed trajectory; they are not blind predictions of a new run's transition. Other seeds select different frequencies, and modulus and regularization change whether the reported stages appear. [W0336, 2301.05217v3, §§4–6, Fig.7 and App.C](../../flued_multigranularity_survey_20261108/03_reading/B16/W0336.md).

Together these works support recording mechanism-sensitive trajectories alongside task performance. They also show why an endpoint-selected probe can make history look more orderly than it was. A measure designed after seeing the successful final circuit should be labeled retrospective and assessed on independent runs before it becomes a selection rule.

### 2.2 “Never formed,” “not yet observed,” and “formed then retired” differ

Differential learning kinetics studies competition between contextual attention and weight-based memorization in a synthetic classifier. Its simplified analysis assumes additive independent circuit logits, large-dimensional limits, small initialization, and particular symmetry conditions. These assumptions differ from evidence for shared subcircuits discussed below. Its most transferable reporting contribution is the separation of runs that never acquire the skill within observation, runs that acquire it without observed transience, and runs with observed acquisition and decline. A finite run ending with the skill intact is right-censored, not evidence of permanent retention. [BR-A05-N06, 2412.00104v2, §3 and App.A.4–A.6](../03_reading/V06/BR-A05-N06.md).

Saved checkpoints similarly censor the onset and disappearance of a mechanism. If a dependency is absent at one saved time and present at the next, emergence lies somewhere between them, assuming the assay measures the same property. An ability present at both times could disappear and return between them. A missing early checkpoint cannot be replaced by a story inferred from final gradient alignment. Seed-specific latency distributions, unsuccessful runs, and incomplete histories should remain visible rather than selecting only runs whose endpoints support the favored account.

The language-model evidence makes the observable itself consequential. In controlled nonce morphology, prompt-control effects, candidate preference, four-choice accuracy, unrestricted construction, and external-task transfer emerge at different observed times. For OLMo-2-7B, a control-sign change is bracketed between 336B and 630B training tokens, earlier than fitted choice and exact-generation crossings. Other models reverse signs or already exceed a criterion at the first available checkpoint. Direct task fine-tuning can produce a different ordering. [BR-LD-N06, 2610.19113v1, §§3–6 and Apps.B/E/I/J](../03_reading/V06/BR-LD-N06.md).

That card remains PARTIAL because the paper explicitly refers to an external supplement that was not located; its body and included appendices are substantive, not blocked. Its temporal estimates are author-reported sparse-checkpoint/fitted quantities. They are useful evidence against one universal acquisition time, but neither their fitted crossings nor their study thresholds become local experimental gates.

## 3. Lag, initialization, and reader–writer coformation

### 3.1 Inference lag is a concrete alternative, not a generic diagnosis

Lagging Inference Networks studies a variational autoencoder: a Gaussian encoder approximates a moving model posterior while an autoregressive generator can fit data without depending strongly on the latent. Repeated early encoder updates, followed by ordinary joint training, improve activity and likelihood in the reported text and image settings without changing the evidence lower bound objective. This establishes an update-allocation explanation under a specific stochastic objective. It does not establish that deterministic compressed-state non-use is posterior collapse. [BIW-0096, 1901.05534v2, §§3–6, Algorithm 1 and Apps.A–G](../03_reading/V06/BIW-0096.md).

The positive results carry meaningful costs and countercontrols. Typical aggressive phases use 30–100 inner updates. Reported aggressive/basic wall-time ratios are 2.20×, 3.73×, and 2.19×, not a uniform two-to-three-times range. The Yelp inner-update sweep changes both likelihood and time; practical convergence can stop aggressive mode earlier than a fixed iteration count. Slow KL annealing also avoids collapse, with some single-run likelihood cells slightly better than the unannealed aggressive comparison. Thus the evidence favors taking lag seriously, not selecting encoder-extra updates without an opportunity-budget comparison.

For a writer–reader system, the analogous hypotheses should be kept separate. The writer might supply inadequate content; the reader might learn too slowly; or both might keep changing coordinates so that neither sees a stationary problem. A frozen writer with an adapted reader tests accessibility under a new training permission. It does not reconstruct the original coformation history. Cross-time writer/reader combinations can reveal compatibility variation, but they also create unfamiliar interfaces. Same-time self-connections are needed before interpreting cross-time failures as harmful coadaptation.

A strong comparison between lag and objective-landscape explanations remains source-limited. The identified linear-likelihood alternative [BR-A01-R16=LD-N08, 1911.02469v1](../03_reading/V10/BR-A01-R16.md) is still body-blocked at the audited edition. Existing variational counterexamples already prevent a universal lag claim, but the missing original cannot be filled with its title. The unresolved question is which objective and optimization conditions make extra inference updates effective, not whether every unused representation has an encoder that is behind.

### 3.2 Equal functions can have unequal learning dynamics

The exact deep-linear analysis shows why parameter count and initial predictions are incomplete controls. With output `W₂W₁x`, rescaling the factors can preserve their product while changing internal feature evolution. The analysis solves gradient-flow dynamics for whitened inputs and a specified balanced-factor relation; aligned-mode solutions impose additional assumptions. Different encoder/decoder scale allocations can produce different apparent lazy and feature-learning behavior even when the initial input–output function agrees. A nearly unchanged kernel can conceal a smaller task-structured component that is learning. [BR-LD-N07, 2409.14623v2, §§3–6 and Apps.A–D](../03_reading/V13/BR-LD-N07.md).

Its transfer examples are equally permission-specific. In a toy semantic hierarchy, an additional output row learns from one labeled item while other weights remain frozen. Generalization depends on the learned representation and factor balance. This is a controlled illustration of initialization and receiver accessibility, not evidence that rescaling a nonlinear Adam-trained language interface repairs it.

The complete exact-v2 HTML, raw tables, and carrying figures are now read; it is stale to call this a missing-figure source. PDF alignment and several local notation discrepancies remain unresolved. Those discrepancies limit reliance on the affected algebraic steps, rather than independently refuting the main theorem. For practical comparisons, record initial function, intermediate activation scale, parameterization, and optimizer state separately. Rebalancing factors changes the geometry seen by the optimizer, even where their product agrees.

### 3.3 Early damage is selective, not universal irreversibility

Critical Learning Periods tests temporary deprivation rather than merely comparing endpoints. Early blurred images can leave substantial finite-horizon impairment after clean images return, and a fixed learning-rate control argues against annealing as the sole cause. But vertical flips and label permutations recover near baseline, while fixed random-noise inputs have milder residual effects than blur. Not every early deviation creates the same long-lived deficit. Fisher-based sensitivity co-varies with the effect but is not proof of a unique structural cause. [BR-LD-N03, 1711.08856v3, §§2–4, Figs.1–5 and Apps.A–C](../03_reading/V13/BR-LD-N03.md).

This comparison suggests a useful distinction: an early signal can steer feature allocation in a way later training does not readily undo, while other disruptions are mostly remappable coordinates. A restoration horizon is part of that finding. Finite recovery failure does not imply that no learning rate, task order, or longer budget could recover. Conversely, a recoverable label permutation does not show that lost fine detail is similarly recoverable. For memory formation, task-specific corruption, permutation, and no-information controls distinguish selective learning-history effects from generic disruption.

## 4. Feature competition, useful bypasses, and changing roles

### 4.1 Competition does not require a universal easy-first chronology

Gradient Starvation formalizes a mechanism in which a strong predictive direction reduces learning response along another direction under cross-entropy. Its central theory concerns fixed linearized features in a restricted binary setting; it is not a theorem that deep internal representations never form. The empirical remedy still learns color in colored-MNIST experiments while changing the balance of evidence. Its large worst-group gains coexist with lower mean accuracy in CelebA, and one reported tuning setup uses the test environment. [W0333, 2011.09468v4, §§2–4 and Apps.A–B](../../flued_multigranularity_survey_20261108/03_reading/B16/W0333.md).

Complexity Matters supplies an important reversal. A simple strongly correlated shortcut can slow the core feature, yet more complex settings permit core and shortcut learning together. Retraining the last layer on balanced data can expose accessible core information before the deployed output uses it. Weak spurious features can later disappear, whereas strongly correlated ones persist in the reported horizon. The same literature therefore supports delayed core learning, simultaneous learning, and selective forgetting under different conditions. [W0334, 2403.03375v3, §§2–5, Figs.2–6 and Apps.A–D](../../flued_multigranularity_survey_20261108/03_reading/B16/W0334.md).

This matters for compressed interfaces. Local completion, an easy decoder path, and remote semantic dependence may not turn on in a neat sequence. A learned external probe can reveal latent information without showing that the original reader consumes it. Early stopping based on a supposed shortcut-only phase can misidentify examples when features form together. Difficulty, correlation, entropy, output frequency, and task diversity should be distinct variables; “harder” is not an adequate substitute for their specification.

### 4.2 An early competitor can help the desired mechanism form

Strategy Coopetition offers stronger history interventions than a generic shortcut narrative. Its task supports exemplar-based contextual mapping, weight-based classification, and a hybrid context-constrained strategy. The later hybrid still requires the correct label to appear in context. Declining exemplar mapping is consequently not equivalent to complete context non-use. [BR-LD-N05, 2503.05631v2, §§2–5, Figs.1–4](../03_reading/V06/BR-LD-N05.md).

Shared components make the learning interaction nontrivial. Components taken from an intermediate competitor-only checkpoint accelerate contextual learning, whereas early and late competitor checkpoints do not. The reported helpful range spans 9.8M–31.5M competitor-training sequences. Continuing a mature competitor does not recover the desired contextual mapping within the observed run. Other configurations show resurgence, and exact exemplar matching can preserve the contextual strategy. These outcomes reject both “a bypass is always harmful” and “once displaced, a mechanism can never return.” They do not establish equal-compute superiority, since the helpful components bring additional pretraining history.

The comparison with Differential Learning Kinetics is informative rather than redundant. The latter analyzes an independent additive-circuit model and a regularization-dependent decline; Strategy Coopetition emphasizes reuse of shared copying machinery with a changed earlier computation. Both can generate transient performance, but they imply different interventions. Suppressing a competitor may protect a target route in one setting and deprive it of a useful forming component in another. Timed attenuation followed by restoration, compared with an equally disruptive unrelated attenuation, is more discriminating than permanent deletion alone.

### 4.3 Better training-distribution loss can accompany worse contextual generalization

Competition Dynamics trains autoregressive models on mixtures of Markov chains and fits their outputs with four candidate algorithms. A context-generalizing bigram-inference phase can precede a training-matrix-based phase: in-distribution performance improves while behavior on fresh transition matrices worsens. At higher diversity, the context-sensitive phase persists within the available budget; changing state count, width, or transition encoding changes the observed sequence. [BR-A05-N05, 2412.01003v4, §§2–4, Figs.5–8 and Apps.C/I](../03_reading/V13/BR-A05-N05.md).

Here “retrieval” refers to weighting learned training transition matrices, not navigating an external document store. The behavioral mixture predicts held-out trends and includes arbitrary-algorithm negative controls, but does not uniquely identify a circuit among correlated or omitted strategies. Its strongest contribution is that task distribution and representation can alter which competent strategy wins. It does not show every sufficiently trained model becomes context-blind.

For target histories, the informative trajectory jointly records clean task risk, correct-versus-wrong-content dependence, native returns, and shifted-query behavior. A falling loss with falling targeted dependence could indicate replacement, redundancy, improved local inference, or a changed meaning of the assay. The morphology study's negative transfer after adapters and ineffective selected-head penalties reinforce this point: reducing an attention pattern need not teach novel answer construction, and improving one diagnostic need not transfer to external compositional tasks.

## 5. Auxiliary targets, bottleneck timing, and decoder masking

### 5.1 “Add reconstruction” names several different treatments

Compressive Transformers distinguish full-state reconstruction from reconstruction of the attention response to old states. The auxiliary gradients stop at the compressor in the principal setup; a separate longer-unroll comparison lets the primary loss reach it. Attention-response reconstruction gives the strongest listed Enwik8 cell, but rows select their best compression rate and the backpropagation comparison changes unroll and batch size. Larger compressed memory also sometimes worsens evaluation. The evidence concerns a task-dependent target and gradient destination, not a universal reconstruction prescription. [W0023, 1911.05507v1, §3.2, Table 5 and App.B](../../flued_multigranularity_survey_20261108/03_reading/B24/W0023.md).

ICAE supplies a favorable mixed-objective example that should survive negative reconstruction arguments. Its autoencoding-plus-continuation pretraining improves judged outcomes over either single objective at the tested slot count, followed by instruction tuning. The frozen host still loses quality relative to raw context, random strings reconstruct poorly, and independently compressed segments require additional multi-segment training before concatenation works. Thus reconstruction can help establish a usable interface while leaving exact-detail and composition failures. [W0038, 2307.06945v4, §3.2, Tables 3–5 and §3.3.3](../../flued_multigranularity_survey_20261108/03_reading/B24/W0038.md).

Deeply-Supervised Nets is different again: companion classifiers receive class labels at hidden layers, improving several image-classification results. They add heads and backward work and may be attenuated before deployment. The local theory assumes compatible optima and regularity conditions and compares convergence bounds, not actual universal convergence. It neither reconstructs old states nor demonstrates large-causal-LM semantic-memory use. [BR-LD-N02, formal AISTATS 2015, pp.562–570, §§2–3 and appendix](../03_reading/V13/BR-LD-N02.md).

For I.12, a strong output decoder could improve spelling or local completion while masking a weak trunk. The required comparison allocates encoder, trunk, and decoder capacity explicitly, with remote-content outcomes separate from output legality. The inspected vision supervision and stochastic word-level results do not supply that dedicated large-scale causal byte-model comparison. Direct large-causal-LM intermediate supervision remains a precise primary-evidence and empirical gap.

### 5.2 Apparently opposite schedules address different bottlenecks

Continuous First, Discrete Later delays vector quantization so weaker latent directions can form. Its linear rate–distortion channel explains one mode-suppression mechanism under Gaussian and balanced-factor assumptions. Image comparisons exchange continuous and discrete steps within a 100k-step total, while audio comparisons use a common 100-epoch total. Positive reconstruction results coexist with an audio test-clean PESQ reversal at K=4096. All-codebook PCA rank can be inflated by unused random vectors; assigned-code behavior and utilization are necessary companions. [BR-A05-N02, 2605.06870v3, §§3–4, Tables 1–4 and Apps.A–D](../03_reading/V06/BR-A05-N02.md).

GenFirst instead gives a generative prior greater relative influence before reconstruction refinement. Reconstruction weights remain fixed; prior and entropy weights decrease together. This is not a reconstruction-free first stage. Its headline schedule comparison runs 500+140 epochs against constant/cosine controls at 320 epochs. Guided generation FID improves, while cosine and frozen-VAE reconstruction FID can be better. Other variants include substantial subsequent frozen-VAE prior training and decoder fine-tuning. [BR-A05-N03, 2608.29335v1, §4.3, Table 2 p.10 and App.C pp.20–24](../03_reading/V06/BR-A05-N03.md).

These are positive recipe results for different obstacles, not competing universal stage-order theorems. Quantization can suppress useful directions early; reconstruction can also create a latent distribution difficult for a prior. Equal steps do not necessarily equal FLOPs, and GenFirst's doubled epoch exposure prevents isolating order alone. Its within-paper text-to-image variant-label conflict should remain unresolved where relevant rather than silently assigning numbers. A future schedule comparison would need constant and reversed orders, common final rate, entropy treatment, exposure, and separate evaluation-prior budgets. None is selected here.

## 6. Same-sign gradients, scale, curvature, and plasticity

### 6.1 Positive cosine is weaker than optimization benefit

For primary loss gradient `g` and auxiliary gradient `v`, a positive inner product says that a sufficiently small step along `−v` decreases the primary training loss to first order at the measured point. It says nothing by itself about the held-out loss, the magnitude of the combined step, or the history of content use. A scalar cosine also discards blockwise scale and can conceal cancellation between components.

The local diagnostic is

\[
\Delta L_{\mathrm{primary}}\approx
 g^\top\Delta\theta+
 \tfrac12\Delta\theta^\top H\Delta\theta.
\]

The realized update `Δθ` is not generally a scalar multiple of the current raw gradient. Momentum, adaptive preconditioning, clipping, weight decay, and mixed-precision step skipping can change it. Without saved optimizer state, recomputing gradients does not recover the historical update. Even with that state, a local training-loss approximation is distinct from validation benefit and from natural content dependence.

Adapting Auxiliary Losses Using Gradient Similarity contains its own decisive negatives. A locally descending auxiliary direction can slow primary learning. In the perfect-teacher experiment, cosine gating can underperform simply adding the auxiliary, and rotated-MNIST gating remains worse than primary-only in some cells. These findings limit the use of sign as a decision criterion without denying the method's useful cases. [W0331, 1812.02224v2, §4, Fig.4 and Apps.B/F](../../flued_multigranularity_survey_20261108/03_reading/B16/W0331.md).

PCGrad adds a joint role for direction, magnitude, and curvature. Its guarantees are conditional local results, not guarantees for arbitrary Adam trajectories or every task. In several-task projection, random order matters; the resulting gradients need not all be pairwise nonconflicting. A questioned necessity argument in its appendix remains a proof-review issue, not an independently established theorem refutation. [W0328, 2001.06782v4, §§2–3 and Apps.A/H](../../flued_multigranularity_survey_20261108/03_reading/B16/W0328.md).

### 6.2 Validation transfer and full-history mechanisms need different evidence

ForkMerge directly compares one-step updates from the same target-trained 25k-iteration checkpoint and measures validation gain. It shows why local cosine is an incomplete proxy: aligned gradients can generalize poorly, while a conflicting regularizing update can help. Its later branching-and-merging procedure uses additional branches, repeated validation selection, optimizer state, and search. Multi-step interpolation is not algebraically identical to a single trajectory with an intermediate loss weight. [BR-LD-N04, 2301.12618v3, §3.1, Fig.2 p.4 and Apps.A/B](../03_reading/V06/BR-LD-N04.md).

The useful inference is narrow and important. A positive endpoint cosine can reject only the measured contemporaneous directional-conflict account. It cannot reject earlier starvation, harmful scale, blockwise disagreement, shared shortcut reinforcement, or generalization failure. Conversely, a negative cosine is not sufficient evidence of harmful transfer. Matching a common starting checkpoint improves local interpretation but does not establish that two losses remained aligned throughout training or caused a particular historical memory policy.

### 6.3 Rank and update norms are diagnostics, not exclusive causes

Directions of Curvature studies continual supervised learning and supplies counterexamples to several simple diagnoses. Leaky-ReLU networks can lose plasticity while update norms increase. Tanh feature rank can fall without comparable impairment, and rank-promoting regularization can coexist with deterioration. A distributional regularizer improves several harder cases but changes weights, geometry, and learning simultaneously. [BR-A05-N11, 2312.00246v2, §§3–6 and Apps.B/C](../03_reading/V13/BR-A05-N11.md).

Its practical curvature matrix is a per-example-gradient Gram proxy with rank capped by sample count, not an exact Hessian. Validation against the Hessian is restricted to a small projected problem and weakens later. Correlated rank change plus successful regularization does not establish an exclusive curvature cause. The reading is exact v2, not the later renamed v4.

The synthesis therefore leaves optimizer noise, momentum, preconditioning, and writer–reader coformation in large causal hosts as substantive gaps. Another gradient-surgery name would not recover missing optimizer history. Where a tractable checkpoint exists, directional finite differences and Hessian-vector products can test local approximations without updates. Establishing whether preserved plasticity prevents later loss of content use requires a separately authorized training comparison and retention of earlier-task quality.

## 7. Frozen composition, self-connection, and semantic compatibility

### 7.1 Three self-controls answer three questions

An untouched model or exact tensor replay tests whether extraction and reinsertion preserve the original computation. An intact self-stitch inserts the proposed connector between the original halves and tests the connector's own burden. Reset-and-relearn deliberately randomizes a region and asks whether the surviving representation supports relearning. Calling all three “self-connection” conceals the causal contrast.

Yosinski's BnB baseline copies and freezes lower layers from the target-trained model but randomizes and retrains the upper layers. Its middle-layer penalty and recovery after fine-tuning demonstrate relearning/coadaptation costs, not failure of intact replay. Cross-task AnB adds task and source-history differences. Similar versus dissimilar task splits also differ in class counts and difficulty. [BR-N06-01, 1411.1792v1, §2 Fig.1, §4 and Apps.A–C](../03_reading/V07/BR-N06-01.md).

Mai supplies the closer modern self-stitch: the same trainable connector type, site, objective, and data are used within and across foundation models. Self-stitch improvements themselves show that an inserted learned module can improve the receiver, so its contribution must be separated from cross-source information. Identical connector initialization seeds are not specified in the inspected protocol. [BR-N06-04, 2603.12433v3, §§3–5 and App.A](../03_reading/V07/BR-N06-04.md).

### 7.2 Frozen halves can be compatible after a learned interface

Bansal operationalizes directional compatibility: freeze sender and receiver, fit a restricted bridge on the recipient's labeled task, then evaluate held-out performance. Independently trained models can stitch with small penalties, stronger sources can improve weaker recipients, and deep random sources generally fare worse. But random early layers can also stitch well; fully randomized labels are an exception; extensive receiver fine-tuning can conceal distinctions. Missing bridge schedule, initialization, and batch-normalization details limit precise quantitative transport. [BR-N06-02, 2106.07682v1, §§2–6, Figs.2–3 and App.B](../03_reading/V13/BR-N06-02.md).

Mai shows why one failed adapter is weak evidence of intrinsic component harm. At a shallow DINOv2→SigLIP2 stitch, task-loss training gives 25.1%, local feature matching 49.4%, and final-feature matching 51.4%, compared with source/recipient linear probes of 46.7%/53.5%. Both original models remain frozen. Matching the recipient's final features backpropagates through its suffix and brings stronger teacher access than local matching. A weaker CLIP sender can still fail. These are practical compatibility gains with bounded failure cases, not information-preservation guarantees.

### 7.3 Task-fit success is not shared original semantics

Smith constructs successful stitches between different cues and from label-coded random clusters. The synthetic noise is structured: one prototype per class is shared between training and test, with independent sample noise around it. Therefore the bridge can learn class information without an image-derived sender. It is not a demonstration that arbitrary fresh noise contains labels. Cross-domain directions also differ, and random senders do not always work. [BR-A06-X04, formal ICML 2025, §§4–5, Table 1 and Apps.A/B/G](../03_reading/V07/BR-A06-X04.md).

Invariance-aware stitching offers a constructive response by generating inputs nearly indistinguishable to the sender and checking receiver consistency. It often exposes incompatibility hidden by ordinary stitching, but uses input inversion and sometimes receiver outputs/internal features. Its explicit ViT identity failure and residual shortcut use prevent treating the improved score as semantic ground truth. Standard and invariance-aware training also differ in batch-normalization statistics and augmentation. [BR-A06-X05, 2505.20142v2, §§2–3 and Apps.B/F](../03_reading/V13/BR-A06-X05.md).

Practical fit and content preservation should consequently be reported separately. A coordinate connector should retain its utility on new bindings, conflicting cues, and legal content substitutions, not merely predict familiar class labels. Constant, random, weak-source, self, and cue-disjoint inputs test whether the connector has learned an answer route of its own. Success can reject content-loss accounts for the tested targets and repair class; failure rejects only that bounded repair. Neither supplies a host-independent semantic certificate.

## 8. Attention migration: stages, companions, and reversing outcomes

### 8.1 LoLCATs is a meaningful strategy comparison with unequal stage doses

LoLCATs first trains feature maps against teacher attention outputs and then adapts the assembled linearized stack with low-rank updates. During transfer, teacher outputs feed later layers, suppressing upstream student-chain errors. Local matching and natural-chain prediction are therefore different measurements. The hybrid also retains a recent exact-KV window; it is not a pure recurrent state with no companion channel. [BR-N06-07, 2410.10254v3, §§3.1–3.3 and App.A](../03_reading/V07/BR-N06-07.md).

The audited Table 2 comparison must be stated exactly. Llama-3-8B Hedgehog without transfer starts at perplexity 2448.01 and reaches 9.02 after four LoRA epochs. With transfer it starts at 60.86 and reaches 3.90 after two transfer epochs plus two LoRA epochs. Mistral's corresponding values are 561.47→4.87 and 18.94→3.04. The planned total-step/epoch envelope is intentionally matched; dismissing it as wholly unmatched would erase a legitimate recipe comparison. But LoRA dose differs, and early stopping/best-validation selection leave realized work incompletely specified. These cells cannot estimate equal-stage-dose effects or interaction coefficients. [Reading audit R1, §3.4](../05_review/READING_AUDIT_R1.md).

The long-context countercontrol is as important as perplexity recovery. At 8192 tokens, Alpaca-only linearization achieves 0% exact passkey retrieval across placement deciles, whereas passkey-format training produces 100%; extrapolation to 10240 fails. Format-specific adaptation can rescue trained-length behavior without guaranteeing general long-range retention. Teacher passes, low-rank training, cache state, and selection costs travel with the recovery result.

### 8.2 MOHAWK changes the block as well as the objective

MOHAWK aligns mixing matrices, then teacher-fed block outputs, then assembled-model output distributions. Its migration initialization makes convolution identity-like, opens a gate, and removes normalization/activation incompatible with the copied block. Components beneficial in a from-scratch state-space model are not automatically suitable in a pretrained transplant. The pure model uses 80M+160M+2.76B=3B tokens; the hybrid retains four full-attention layers and their growing KV. [BR-N06-08, 2408.10189v2, §4 and §§5.4–5.7](../03_reading/V07/BR-N06-08.md).

The 5B-token strategy table favors the full stage sequence, but matches tokens rather than teacher/student FLOPs. Its same-architecture Phi→Phi control resets attention and relearns it, rather than replaying intact weights. That strengthens evidence for staged restoration while leaving exact-replay validity a separate question. Offline matrix fitting with many per-sample optimization steps tests representational fit under stronger permissions, not native deployed content access.

### 8.3 Companion paths can change an apparent recurrence ranking

The Key to Going Linear first freezes original Q/K/V and the host, training only new mechanism parameters on 10M tokens. Strict Llama LAMBADA scores are 28.26 for gated linear attention and 44.67 for the gated delta network. With short convolution they become 68.70 and 69.01; MMLU likewise nearly converges. A large strict-regime gap can almost vanish after a companion changes. [BR-N06-12, 2607.07706v1, Tables 1/3 pp.7–8 and Apps.B/C](../03_reading/V07/BR-N06-12.md).

This does not establish that convolution explains every transfer failure. Local/prefix caches add retained channels, low-rank adaptation uses a reduced learning rate for instability, and no equal-tuning/FLOP comparison is established. Retrieval-heavy tasks remain weak even with larger cache variants. The evidence requires naming the complete package—recurrence, projections, normalization, gates, convolution, position handling, cache, and output fusion—before attributing a transplant outcome to its central update equation.

### 8.4 RAM rankings depend on stage and metric

RAM migration progressively aligns projections, head outputs, blocks, the propagated stack, and the full model. Removed stages return their token opportunity to full-model recovery, a stronger control than simply deleting training. Yet trainable sets and losses differ, and teacher work remains additional. [BR-N06-10, 2610.11214v1, Table 6 p.22 and Tables 4/12 pp.9/26](../03_reading/V07/BR-N06-10.md).

| Qwen2.5-1.5B comparison | Wiki perplexity, lower better | Six-task average, higher better | Consequence |
|---|---:|---:|---|
| Complete, nominal 500M tokens | 16.33 | 68.1 | Better final pair than full-only |
| Full-only, nominal 500M | 16.82 | 66.6 | Final recipe loses this comparison |
| Without head recovery | 16.31 | 66.9 | Slightly better perplexity, worse task average |
| Pattern-free initialization | 16.17 | 67.6 | Better perplexity does not win task average |
| Complete at 56.4M | 77.56 | 51.7 | Early full-only wins both metrics |
| Full-only at 56.4M | 23.90 | 61.2 | Acute/early ranking reverses final ranking |
| Complete at 154.7M | 19.44 | 65.6 | Task average wins while perplexity loses |
| Full-only at 154.7M | 19.35 | 64.7 | Metric-dependent intermediate ordering |

The exact ledger correction is **reported nominal 500M; displayed doses sum to 500.040M**: `7.209+49.152+61.440+36.864+345.375`. The card's exact “500.000M” assertion is a reader arithmetic error, distinct from the source's nominal/row reconciliation. It does not invalidate the quality cells. [Reading audit R1, §3.3](../05_review/READING_AUDIT_R1.md).

Mass-aware reading closer to the theoretical construction can improve initial distribution matching yet generally worsen final perplexity. Likewise head-output error can improve without matching attention distributions. These reversals favor separate local, chain, task, and long-context outcomes. They do not isolate whether staged training preserves original content, teaches alternative task behavior, or provides a better optimization path.

## 9. Capacity controls, host interactions, and manufacture versus repair

### 9.1 Parameter matching leaves important quantities unmatched

A trainable-parameter count is not a state-capacity measure. Record total and active parameters, resident state bits, precision, local cache, read width, fast optimizer state, teacher access, training exposure, and tuning effort separately. Equal active state can coexist with greater total resident memory. Equal tokens can mean unequal raw text after changing the tokenizer. Equal epochs can hide different losses, teacher passes, early stopping, or stage permissions.

Interface geometry illustrates why initialization and feasibility matter. Pseudo-Inverse Tying improves some continued-training cells but worsens all three reported random-initialized Llama-like models and the continued GPT-590M comparison. Its construction requires a vocabulary matrix with orthonormal columns, hence V≥d; it is not directly feasible as written for 257 symbols with wider hidden states. Frozen vocabulary factors, additional quadratic-size metric work, and nonidentical initial functions further affect interpretation. [W0367=BIW-0038, 2602.04556v2, §§3–4 and App.B](../03_reading/V14/W0367.md). Neither favorable geometric consistency nor a small vocabulary establishes memory retention or natural use.

MoCE provides a separate domain-sensitive composition example. The exact audited title is **MoCE: Adaptive Mixture of Contextualization Experts for Byte-based Neural Machine Translation**. Its v1 byte model has byte inputs and byte outputs, with local contextualization in the encoder—not a byte-input/nonbyte-output interface. Ted-59 favors its adapted byte model, whereas OPUS-100 favors the subword baseline; active-expert count changes compute. Shared encoder/decoder embeddings do not identify the effect of tying independently. [BIW-0069, 2411.01474v1, Tables 3–5 and App.B](../03_reading/V14/BIW-0069.md); [reading audit R2, §3.5](../05_review/READING_AUDIT_R2.md). The later v2/camera-ready comment is metadata, not a reading of v2 results.

### 9.2 Host interaction is a within-host comparison before a cross-host conclusion

For a quality outcome Q, the four-cell quantity `Q_AB−Q_A−Q_B+Q_original` describes nonadditivity on a declared host, background, and metric. It is not invariant to changing accuracy into log loss or perplexity, and it does not identify unique causal information shares. Separately optimized architecture-search winners are not fixed-component cells. Better search results can reflect search opportunity rather than an intrinsic interaction.

A transport claim should first establish the original, A, B, and AB contrasts within each competent host, at specified adaptation permissions. Only informative cells need cross-host repetition. Raw content, source permissions, target family, initial ability, trainable sets, and resource contract must remain explicit. A difference across hosts can then support a bounded interaction, rather than a universal recurrence ranking. Seed/window and hardware/environment fingerprints are part of from-scratch formation evidence; the literature supplies no certificate that those dimensions can be ignored.

### 9.3 Manufacturing and restoring are different histories

An already competent host can be damaged, exactly restored, or repaired through a restricted alternative. This establishes an ability before the intervention and supports acute-dependence and restoration questions. A from-scratch model lacking the ability does not supply that anchor. Failure to manufacture may reflect optimization, task exposure, or capacity; failure to repair may reflect a narrow connector or insufficient adaptation. They are not interchangeable evidence.

Frozen, connector-only, projection-adapted, and full-host treatments should therefore be named separately. Char2Subword's contextualization through frozen mBERT can worsen embedding-neighborhood agreement before re-approximation improves it; downstream freeze permissions are incompletely specified. [BIW-0122, 2010.12730v3, §§3–5 and Fig.4](../../byte_language_interface_survey/03_reading/R06/BIW-0122.md). Zero-Shot Tokenizer Transfer has a trained per-host hypernetwork despite its name, optional full-host continuation, and substantial task/language failures. Its untied-GPT-2 instability without an anchor is not a theorem against untied hosts. [BIW-0126, 2405.07883v2, §§3–5 and Apps.B/F/J](../../byte_language_interface_survey/03_reading/R06/BIW-0126.md).

A recovery curve should include immediate disruption, bounded repair, clean-model continuation, and preservation of non-target abilities. Returning a deleted stage's opportunity and counting teacher construction make a schedule comparison stronger. They do not turn it into a content-preservation or equal-FLOP proof. Architecture selection ultimately concerns complete frontiers; causal attribution concerns controlled components. Both are useful, but require different comparisons.

## 10. Source placement and lifecycle are composition obligations

Closed-state reform and source-enabled memory have different information-access contracts. If original content remains available, the system also acquires lifecycle obligations: source→summary→index→KV→answer-cache→backup dependencies, model versions, timestamps, authorized refresh, and completion evidence. A graph link to an episode is not proof that all derived objects become fresh or disappear when that episode changes.

Provenance as Dependency Analysis gives a precise model-specific distinction between conservative dependency and actual influence. A safe dependency set can include irrelevant inputs; its explicit `R−R` example retains provenance although the result is empty. Correct conservative propagation supports invalidation without certifying causal consumption. It applies to the specified calculus, not automatically to a neural summary. [W0420, 0708.2173v2, §§3–5](../../flued_multigranularity_survey_20261108/03_reading/B19/W0420.md).

Datalog maintenance adds a useful cost reversal: a small input deletion can trigger much larger backward checking, while recursive support cannot be preserved merely by counting cyclic derivations. Optimized maintenance distinguishes nonrecursive support, overdeletion, and rederivation. That is a model for making support explicit, not a guarantee that learned summaries possess such support graphs. [W0425, 1711.03987v2, §§3–6 and App.A](../../flued_multigranularity_survey_20261108/03_reading/B19/W0425.md).

DELF distinguishes synchronous invisibility, read-time descendant masking, asynchronous deletion, recovery logs, and expiring backups. Its strong completed-deletion statistics do not cover every initiated request unconditionally, and undeclared references can escape the graph. Lethe addresses delayed cleanup inside a storage engine, under resource and scheduling conditions, not all replicas, backups, or underlying-device erasure. [W0429, formal USENIX Security 2020, §§4–6](../../flued_multigranularity_survey_20261108/03_reading/B19/W0429.md); [W0431, 2006.04777v4, §§3–5](../../flued_multigranularity_survey_20261108/03_reading/B19/W0431.md). Logical invalidation, lawful recomputation, and physical deletion remain separate outcomes.

Neural systems introduce representation staleness as well. Memorizing Transformers normalizes queries and keys to reduce stale-coordinate mismatch as weights change but explicitly does not eliminate it; larger memory sometimes ceases to help or hurts individual tokens. [W0144, 2203.08913v1, §3 and Apps.A–B](../03_reading/V15/W0144.md). Zep retains original episodes, temporal facts, and community summaries, yet its source links were not directly evaluated and complete deletion propagation is unspecified. [W0118, 2501.13956v1, §§2–4](../../flued_multigranularity_survey_20261108/03_reading/B10/W0118.md).

Placement must also include cold/hot traffic and reuse. Denning's working-set model motivates measuring active sets and reentry traffic, not assuming equal-cost semantic objects or future locality. CacheGen shows a hardware/bandwidth-dependent choice between transporting compressed KV and recomputing from text; arithmetic coding is lossless only relative to quantized symbols. Its text fallback requires source and usable prior context. [W0432, CACM 1968, pp.324–328](../../flued_multigranularity_survey_20261108/03_reading/B20/W0432.md); [W0434, 2310.07240v6, §§5–7](../../flued_multigranularity_survey_20261108/03_reading/B20/W0434.md).

Mooncake supplies substantial scheduling evidence, but all reported experiments use a LLaMA2-70B-shaped dummy model. Throughput and rejected-request counts are system outcomes, not measured answer-quality equivalence. Prefix hashes alone do not establish model/source-version invalidation. [W0438, 2407.00079v5, §§6–8](../03_reading/V15/W0438.md). No source-placement winner follows without construction, source and derived-state bytes, update fan-out, transfers, rejected work, tail latency, and repeated-query amortization. Selective persistent writes, selective execution, and reuse of stale computation must likewise remain distinct; skipping work requires a freshness/reentry contract, not merely a sparse-update equation.

## 11. Sequential utility: retain the question without redefining dynamics

A current action score, a feature's coalition allocation, and the value of an adaptive continuation policy are different objects. This distinction matters to R.14–R.15, but it should not turn the chapter's learning-history questions into router-utility questions.

Howard's bidding example shows positive complementarity even for independent underlying variables: joint information value exceeds the sum of separate values under the specified action/payoff structure. Blackwell's comparison concerns ideal decision rules able to simulate or ignore richer free observations; a fixed deployed reader need not realize those rules. [W0476, Information Value Theory, 1966, pp.23–26](../../flued_multigranularity_survey_20261108/03_reading/B17/W0476.md); [W0478, Equivalent Comparisons of Experiments, 1953, §§2–5](../../flued_multigranularity_survey_20261108/03_reading/B17/W0478.md).

A complementary pair can have zero individual benefit and positive joint benefit. Informational Substitutes supplies an XOR example; adaptive-submodular guarantees instead require diminishing conditional marginal value at the relevant histories and the stated budget assumptions. Ordinary independence of observations is insufficient. The inherited entropy-sign issue should be handled locally: `I(E;B|A)=H(B|A)−H(B|E,A)`. A reversed printed sign is not an independent refutation of the intended substitute theorem. [W0483, 1703.08636v1, §§2/4/5](../../flued_multigranularity_survey_20261108/03_reading/B17/W0483.md); [W0303, 1003.3967v5, §§3–5](../../flued_multigranularity_survey_20261108/03_reading/B12/W0303.md); [reading audit R2, §4](../05_review/READING_AUDIT_R2.md).

Learning to Select Computations explicitly distinguishes stopping after one computation from beneficial continuation. Its learned policy often beats myopic alternatives, but blinkered comparison cells can win and offline fitting is amortized. Selection itself can cost more than the computation selected. [W0301, 1711.06892v3, §§2–5](../03_reading/V16/W0301.md). SAGE allocates a nonlinear coalition value; additive allocations do not make action rewards additive, and practical marginal replacement changes its conditional theoretical game. [W0304, 2004.00668v2, §§2–3 and Supp.D/E](../03_reading/V16/W0304.md).

Recent Causal Memory Policy makes exposure an explicit measurement intervention, but its union of deterministic and randomized retrieval slots separates assignment from realized inclusion. An item can have 90 inclusions and no exclusions, so assignment alone does not establish both-arm support. A constant inverse-propensity weight canceling in a normalized mean does not repair that design. The public arXiv edition reports better evidence discrimination alongside some answer-quality harm, weak held-out-query transfer, and oracle-enriched candidate pools. [BR-A08-V18, 2610.02070v1, §§3–4, Apps.C/H](../03_reading/V09/BR-A08-V18.md). This ID identifies the paper, not reading batch V18.

Doubly robust evaluation can reduce bias under independently fitted nuisance estimates and suitable action support; it cannot reveal unsupported actions or identify future retention value from a one-step reward. [W0315, 1103.4601v2, §§2–4](../03_reading/V16/W0315.md). DynaKRAG's readable v2 body reports useful quality/call tradeoffs, but immediate supporting-document-recall labels and a separate continuation gate do not establish terminal action values; its actual v2 supplement/teacher ledger remains missing. [W0339, 2607.06507v2, Method and Tables 1–2](../03_reading/V15/W0339.md).

A meaningful future policy comparison would specify the continuation, displaced evidence, support, complementary pairs, negative utilities, failed calls, truncation, and all teacher/search costs. Those requirements preserve a real research direction without implying that a learned router is the solution to formation, capacity, or transfer failure.

## 12. Existing-checkpoint diagnostics versus new training

The following is a proposed separation of evidence actions, not authorization to execute them. No checkpoint inventory, tensor evaluation, probe fitting, continuation, or experiment was performed for this chapter.

### 12.1 What existing artifacts may make observable

First inventory exact timepoints, resolved configurations, data exposure/cursor, stage flags, seed, model version, hardware/environment, and optimizer/scaler/RNG availability. Report missing periods explicitly. A model-only checkpoint can support forward evaluation and fresh gradient calculations, but cannot recover the historical Adam update without the relevant state.

| Evidence action | What it can establish | Required boundary |
|---|---|---|
| Fixed held-out forward evaluation across saved times | Observed quality, native returns, and content-dependence trajectories | Same examination stream and scoring; sparse times censor transitions |
| Natural correct/wrong-content substitutions | Specific sensitivity under a declared authority and intervention contract | Match legal addresses, shape and nuisances; check non-target damage and a known-positive assay |
| Exact replay, original-component reinsertion, self-splice | Surgery validity and immediate interface burden | Distinguish intact replay from reset/relearn; control recomputation/background |
| Activation, scale, spectrum and assigned-code summaries | Candidate changes in representation and conditioning | Rank/attention/norm alone is not content use; track sample-count and unused-code artifacts |
| Recomputed task gradients and local curvature without updates | Current directional/scale relations and local approximations | Backward work is not forward-only; raw gradients are not missing historical updates |
| Cross-time interfaces without fitting | Compatibility of specified saved sender/receiver pairs | Same-time self-splices first; hybrid distributions can invalidate a causal reading |

Selection of checkpoints, circuit directions, donors, or metrics should use analysis data distinct from the final evaluation. Keep negative checkpoints and unsuccessful seeds. Report actual task performance beside intervention effects; a large effect on a damaged hybrid is not automatically useful natural dependence.

### 12.2 Fitting and adaptation are additional learning

Training an external probe is supervised analysis with labels and fitting costs, even when the main model stays frozen. It belongs neither in forward-only diagnostics nor in native unmodified use. Connector fitting, receiver calibration, hypernetwork construction, and low-rank repair likewise add learning permissions. An oracle readout can show recoverability for tested targets but cannot establish that the original deployed query found them.

New-training comparisons would be needed to establish causal lag, formation benefit, or recoverability beyond the observed artifacts. Candidate contrasts include writer-extra/reader-extra/joint updates; fixed-writer receiver adaptation; early/late/continuous auxiliary supervision; timed bypass attenuation and restoration; matched-function initialization; optimizer-state retention/reset; and original/A/B/AB packages within each host. Constant/reversed schedules and unchanged/self-interface continuation return opportunity to meaningful controls. Equal compute, exposure, teacher access, and final bottleneck are separate matching objectives and should not be silently substituted for one another.

These contrasts test different hypotheses and need not all be run. A cheaper checkpoint diagnostic may rule out a proposed comparison or expose a broken instrument first. Missing history is not automatically a reason to launch training, and no budget, seed count, acceptance threshold, or architecture is fixed by this chapter.

## 13. Coverage disposition and remaining decision gaps

The evidence now supports substantial E/F synthesis rather than another generic title expansion. It does not settle the target host. The following map keeps every assigned original direction discoverable while identifying the remaining discriminator.

| Original coordinates | Substantive treatment here | Remaining scientific decision |
|---|---|---|
| E.01–E.04 | §§2–3: lag, coformation, scale, initialization and selective early damage | Equal-opportunity writer/reader histories; nonlinear optimizer transport; actual initial-state availability |
| E.05–E.08 | §4: starvation, simultaneous learning, early facilitation and later substitution | Target-specific features and content-sensitive histories; timed interventions rather than endpoint chronology |
| E.09–E.10; I.12 | §5: distinct reconstruction targets, deep supervision and decoder masking | Direct large-causal-LM intermediate supervision and explicit trunk/decoder allocation |
| E.11–E.14 | §6: aligned-gradient harm, magnitude, cosine/benefit and curvature proxies | Optimizer-state/noise/preconditioning primaries and actual update histories; validation and content benefit separately |
| E.15–E.18 | §§2/4/5: falling loss/use, retirement, stage shifts and curricula | Censored transitions, shifted-query outcomes, constant/reverse schedules and exposure control |
| E.19–E.22 | §§2–6/12: timing, freeze/readaptation, whole history and seeds | Persistence after restoration, clean continuation, unsuccessful seeds and missing-history limits |
| F.01–F.04 | §§7–8: frozen/adapted transplant, replay/self-stitch/reset, compatibility | Exact local surgery validity, connector protocol and target-host semantics |
| F.05–F.09 | §§7–9: mismatch/defect, adaptation dose, host and component interactions, companions | Matched within-host packages and recovery curves; then informative host transport |
| F.10–F.12 | §§6–9: parameter/capacity, optimization and coordinate/semantic transforms | Physical state/teacher/tuning ledgers, initial function and new-binding connector tests |
| F.13–F.16 | §§2/7–9: manufacture, damage, restoration and acute/long-term outcomes | Competent original anchor; matched repair and formation histories with non-target retention |
| F.17–F.19 | §§9–10: domain, task/budget changes and transport conditions | Same raw content, permissions, recipient ability, stage, seed/windows and environment |
| R.09–R.10/R.12/R.16 | §10: placement, invalidation, selective update and complete frontier | Dependency/freshness protocol, legal rebuilding, real bytes/I/O/failed work and workload amortization |
| R.14–R.15 | §11: local, coalition and continuation utility | Supported closed-loop outcomes and complementary actions at full cost |

### 13.1 Return-aware evidence snapshot — 9 November 2026

[Coverage recheck R3](../05_review/COVERAGE_RECHECK_R3.md) supersedes the former blanket description of V17/V18 as pending. The actual [V17 return](../03_reading/V17/BATCH_SUMMARY.md) contains two FULL independent public-preprint readings while all six official anonymous bodies remain BLOCKED. The [V18 return](../03_reading/V18/BATCH_SUMMARY.md) contains one FULL foundational PSR learning original and five BLOCKED official bodies. These are source-reading dispositions, not independent replications or three completed conference manuscripts. Each of the eleven official-body requests returned HTTP 403; that access evidence replaces their earlier untested/pending status without supplying scientific results.

| Carrying source | Actual reading now available | Official-body gap and consequence for E/F |
|---|---|---|
| [BR-R2-T03](../03_reading/V17/BR-R2-T03.md) | FULL independent **2610.19139v1**, *Online Tokenization with Optimal Delay in Linear Time* | Official **8D7l5sK3YT** body BLOCKED; its title says **Near Linear Time**. Candidate relationship only; no manuscript equality. Streaming/resource distinctions can be cited from the public edition, not as conference findings. |
| [BR-R2-T05](../03_reading/V17/BR-R2-T05.md) | FULL independent **2607.22334v1**, *Cross-Tokenizer On-Policy Distillation via Byte-Prefix Marginalization* | Official **Mm5OLOPLT0** body BLOCKED. Matching title/abstract does not establish edition equality. The read supervision/alignment controls sharpen F.17–F.18 without certifying native semantic-memory transfer. |
| [T01](../03_reading/V17/BR-R2-T01.md), [T02](../03_reading/V17/BR-R2-T02.md), [T04](../03_reading/V17/BR-R2-T04.md), [T06](../03_reading/V17/BR-R2-T06.md) | Official metadata/abstract screening only; no independent body identified in the readers' bounded searches | All four official bodies BLOCKED. T02 has **no body-read empirical result here**. Sampling/fairness, late head localization, and boundary/rate-control effects remain unverified rather than newly negative or positive evidence. |
| [BR-PSR-0912.2385](../03_reading/V18/BR-PSR-0912.2385.md) | FULL **0912.2385v1**, *Closing the Learning-Planning Loop with Predictive State Representations* | A **2009 foundational completion**, with no ICLR 2027 association. Learned identification is no longer an existence-only source gap; language transfer and writer–reader coformation remain unanswered. |
| [LoopLA/V11](../03_reading/V18/BR-A08-V11.md), [Farsighted Correction/V16](../03_reading/V18/BR-A08-V16.md), [Finite-Query Compilation/V20](../03_reading/V18/BR-A08-V20.md), [Attention Placement/V21](../03_reading/V18/BR-A08-V21.md), [Predictive Scope/V24](../03_reading/V18/BR-A08-V24.md) | Metadata verified at the earlier official-audit snapshots; all five bodies unread | Individual HTTP 403 dispositions, not pending untested requests. No loop, dynamic-starvation remedy, finite-query theorem, placement result, or scope mechanism is imported from these titles. |

### 13.2 What the completed editions add

The T05 public edition provides a concrete interface-transfer warning relevant to §9. It maps teacher probabilities through shared response bytes, with conditional normalization for interior prefixes and a realized-path lower bound for tokens spanning teacher tokens. Partition-mass conservation is not exact unrestricted byte-string probability; the stated exactness assumptions idealize greedy longest-prefix segmentation. Student rollouts, teacher templates, masked alignment rows, and stopping rules are part of the learning contract. Its whitespace ablation reports code pass falling from 49% to 9% without the mask while math remains stable, with a mask-matched random-removal control that does not recover code-tail reward. This is evidence that local alignment choices can disrupt downstream function, not a T02 stochastic-tokenization result or a general causal account of interface robustness. Teacher scoring, rollout caps, checkpoint selection, and missing full-compute accounting limit the recipe comparison. [BR-R2-T05, 2607.22334v1, pp.3–9, Apps.C/D/H](../03_reading/V17/BR-R2-T05.md).

T03 sharpens the placement/streaming accounting in §10: a stable emitted prefix must survive every continuation, and theoretical delay is not wall-clock delivery time. The measured implementation waits for completed pretokens, unlike the strongest low-delay construction; an unfinished pretoken can grow arbitrarily. Observed memory and tokenizer first-token speed therefore do not establish end-to-end serving speed or a learned segmentor's prefix legality. These are useful resource/interface controls, not evidence about training-time memory formation. [BR-R2-T03, 2610.19139v1, Defs.4.7–4.9 and §6.2 pp.40–41](../03_reading/V17/BR-R2-T03.md).

The PSR original adds actual identification and closed-loop planning under finite-rank, sufficiently rich feature/test sets and exploration coverage. Its small deployed coordinate vector does not erase moment matrices, kernels, learned operators, reward regression, or planning cost. The reported 18.2-step mean is conditional on 78 successful trials; 22 of 100 fail. This repairs an existence-only account of predictive-state learning but does not establish differentiable writer–reader coformation, arbitrary future-query sufficiency, or language-host transfer. [BR-PSR-0912.2385, 0912.2385v1, §§2–5 pp.3–9](../03_reading/V18/BR-PSR-0912.2385.md).

### 13.3 Remaining mechanism and transport gaps

Farsighted Correction remains a particularly relevant **unread** source for E.05–E.16: its dynamic-starvation definitions, causal-gradient versus confidence-gap proxy, labels, histories, and equal-opportunity controls are unknown. Attention Placement remains an **unread** discriminator between a temporary formation scaffold, a final answer path, and compensation for recurrent-state limitations. Their cards now document access failure; they do not establish results for or against the explanations in §§3–9. LoopLA, finite-query compilation, and predictive scope likewise retain their specific algorithm, cost, and generalization gaps.

The [ICLR source audits R1](../05_review/ICLR2027_SOURCE_AUDIT.md) and [R2](../05_review/ICLR2027_SOURCE_AUDIT_R2.md) establish selected official-submission metadata, not acceptance or body equivalence. The two earlier anonymous stitching/receiver bodies also remain blocked; the later V17/V18 denials do not freshly retest those earlier blockers. This chapter offers selected verified submissions plus version-scoped public evidence, not a comprehensive ICLR 2027 results survey. Anonymous identities are not inferred from related public editions.

Three high-value gaps survive the returns: complete optimizer/history evidence for coformation; direct large-causal-LM intermediate supervision and decoder allocation; and legal semantic/query-family transfer with preserved content, rather than only synthetic exact-key or class-label success. Source-specific artifacts remain narrower: the V06 external supplement, affected linear-dynamics notation/PDF alignment, stitching schedule/BN details, RAM ledger reconciliation, and equal-cost teacher/stage accounting. These call for different follow-up actions.

The central judgment is positive: learning history, initialization, objective timing, companion-aware repair, and native receiver adaptation are scientifically live alternatives to adding source access. Source-enabled systems remain legitimate competitors with lifecycle and sequential-policy costs. Evidence should decide among them through their reversing controls and explicit permissions, not by treating one endpoint failure, one cosine, one successful stitch, or one unavailable recent paper as an architectural verdict.
