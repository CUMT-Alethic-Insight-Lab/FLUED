# Problem / solution / AI-technique records

Snapshot2026-11-09. This is an evidence-routing inventory, **not final scholarly synthesis**. Records are traceable observations/questions, not independent scientific problems, experiments or successful effects. Work identity is deduplicated in [CATALOG](CATALOG.md), but overlapping axis records remain as provenance. A/P source scopes and actual failures are retained verbatim below. Author claims are not independent replication.

All record-relative links have been rebased from the carrying discovery files. Questions needing a new experiment remain questions; no architecture decision or numerical gate is adopted.

<a id="a01-r01"></a>
## A01-R01 — A01-R01 — W0067 — Optimal Multitask Representations Under a Rate Constraint: An Information Bottleneck Analysis

Canonical cluster: **W0067**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:2610.30493v1](https://arxiv.org/abs/2610.30493v1), 2026-10-21; [original HTML](https://arxiv.org/html/2610.30493v1). Nicholas Stiles and Gregory W. Wornell. **Existing-W unread**; no official venue acceptance verified; treat as preprint.
- **Prior problem:** an objective that exposes useful factors without a rate constraint may allocate a limited representation budget poorly across downstream tasks.
- **One-sentence solution:** formulate a multitask information bottleneck and compare rate-conditioned optimal covariance allocations with fixed Gaussian pretext objectives.
- **Borrowed mechanisms / learning:** Gaussian information bottleneck, covariance optimization and finite-bit neural bottlenecks with straight-through gradients; known task mixture supplies the relevance signal. Writer sees X, not task index; task-specific reader sees the index. Whole-vector content, no source lookup or local address hierarchy.
- **Evidence:** **A+P**, original §§2.1–2.3 definitions/Proposition 1, §§4–5 examples/Theorems 1–2, §6.1 setup/results and selected introduction. Main proofs, dSprites details and finite-bit appendix not fully read. Reoptimized heads/common frozen features and rate sweeps are relevant controls; five fitted seeds are stated for learned codes. Reported Gaussian and B-bit axes are not interchangeable with storage bytes.
- **Distinguishes:** fixed-objective ranking versus objective × rate interaction; task frequency versus precision; universal failure versus the bounded-SNR positive guarantee. Does not establish language-model deployment optimality.

<a id="a01-r02"></a>
## A01-R02 — A01-R02 — old N02 — Autoencoding-Free Context Compression for LLMs via Contextual Semantic Anchors (SAC)

Canonical cluster: **BR-A01-R02**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:2510.08907v4](https://arxiv.org/abs/2510.08907v4), 2026-03-11, first version 2025-10-10; [v4 HTML](https://arxiv.org/html/2510.08907v4); [official ICLR 2026 proceedings entry](https://proceedings.iclr.cc/paper_files/paper/2026/hash/dff28796c79e1a04c7a6182119ee899a-Abstract-Conference.html). **Existing-audit lead**. Proceedings entry verifies ICLR 2026 publication; formal PDF versus arXiv v4 not compared. Not an ICLR 2027 submission claim.
- **Prior problem:** appended learned compression tokens and full-source reconstruction may be poorly aligned with downstream use.
- **Solution:** select original context tokens as marked anchors, encode bidirectionally and expose their per-layer KV representations to a frozen decoder, trained with continuation and then QA rather than mandatory AE.
- **Mechanisms / learning:** LoRA encoder, shared anchor embedding, uniform chunk-middle selection, bidirectional attention, continuation pretraining and task-label fine-tuning. Writer encodes context without the later question. Persistent payload is per-layer KV, not merely K single-layer vectors; full-context attention during writing is not causal prefix streaming.
- **Evidence:** **A+P**, §§3–5 and surrounding ablation descriptions; Table 5 cells missing from extracted text. Original text reports architecture-specific AE disadvantage and mixed results in another architecture. Frozen target, same-data baseline recipe, anchor/mask/selection ablations are relevant, but full training-cost and numeric ablation audit remains open.
- **Distinguishes:** objective mismatch versus carrier/interface mismatch; learned boundaries necessary versus fixed anchors adequate in this setting. Gradient cosine near zero does not prove causally harmful interference.

<a id="a01-r03"></a>
## A01-R03 — A01-R03 — old N06 — Fixing a Broken ELBO

Canonical cluster: **BR-A01-R03**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [ICML 2018/PMLR 80:159–168](https://proceedings.mlr.press/v80/alemi18a.html); [formal PDF](https://proceedings.mlr.press/v80/alemi18a/alemi18a.pdf). Alemi et al. **Existing-audit lead**, published conference paper; no arXiv/formal version merge performed.
- **Prior problem:** maximizing marginal likelihood or its evidence lower bound does not uniquely select a useful latent representation.
- **Solution:** characterize rate–distortion tradeoffs and constrain information rate to select latent behavior that ELBO alone leaves unspecified.
- **Mechanisms / learning:** variational information bounds, stochastic latent encoder/decoder, controlled rate rather than a single scalar ELBO score. Reconstruction is the training signal; no retrieval addresses or later-query model established by this abstract.
- **Evidence:** **A**, official abstract and bibliographic record only. It explicitly reports identical-ELBO families with different latent properties and powerful-decoder examples; exact constructions and experimental controls are queued, not verified here.
- **Distinguishes:** good generative score versus informative/useful latent code; objective degeneracy versus merely training an encoder longer. Does not prove equal ELBO means equal reconstruction or equal task utility.

<a id="a01-r04"></a>
## A01-R04 — A01-R04 — old N01 — Rethinking Minimal Sufficient Representation in Contrastive Learning

Canonical cluster: **BR-A01-R04**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [CVPR 2022 formal page](https://openaccess.thecvf.com/content/CVPR2022/html/Wang_Rethinking_Minimal_Sufficient_Representation_in_Contrastive_Learning_CVPR_2022_paper.html), pp.16041–16050; [formal PDF](https://openaccess.thecvf.com/content/CVPR2022/papers/Wang_Rethinking_Minimal_Sufficient_Representation_in_Contrastive_Learning_CVPR_2022_paper.pdf). Wang, Guo, Deng and Lu. **Existing-audit lead**; published conference version, not a fresh reading of the arXiv variant.
- **Prior problem:** information shared by augmented views need not include all later-task-relevant information.
- **Solution:** retain additional input information as a regularizer rather than learning only the minimal view-shared representation.
- **Mechanisms / learning:** contrastive positive-view prediction and input-information regularization; augmentation supplies supervision, future task labels are unavailable. Whole-sample representation, not query-conditioned retrieval.
- **Evidence:** **A**, official abstract. The claim assumes non-shared task-relevant information; proofs, regularizer implementation, augmentation controls and matched training budgets remain unread.
- **Distinguishes:** sufficient for a pretext/view versus sufficient for an eventual task; augmentation-defined invariance versus task-universal retention. Not proof that every minimal sufficient statistic is harmful.

<a id="a01-r05"></a>
## A01-R05 — A01-R05 — W0064 — Caveats for Information Bottleneck in Deterministic Scenarios

Canonical cluster: **W0064**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:1808.07593v4](https://arxiv.org/abs/1808.07593v4), 2019-02-08. **Existing-W unread**. Prior audit associates ICLR 2019; this pass verifies the arXiv abstract/history, not a formal venue decision.
- **Prior problem:** sweeping the ordinary IB Lagrange multiplier can fail to reveal the full IB curve when labels are deterministic functions of inputs.
- **Solution:** identify three caveats and propose an alternative functional capable of recovering the curve in those cases.
- **Mechanisms / learning:** information-bottleneck tradeoff analysis; known target Y, not unknown future queries. MNIST is the stated demonstration.
- **Evidence:** **A**, original abstract/history; near-deterministic extension and trivial-solution claims are author results pending full proof reading.
- **Distinguishes:** failure of a particular linear scalarization versus absence of informative compressed representations; estimated compression curves versus actual task-preservation mechanisms.

<a id="a01-r06"></a>
## A01-R06 — A01-R06 — W0037 — Adapting Language Models to Compress Contexts (AutoCompressors)

Canonical cluster: **W0037**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:2305.14788v2](https://arxiv.org/abs/2305.14788v2), 2023-11-04; [PDF](https://arxiv.org/pdf/2305.14788v2). **Existing-W unread**. Original page explicitly says accepted to EMNLP 2023; formal-version comparison not done.
- **Prior problem:** long LM contexts are expensive and finite, but learned summaries need to be consumable by the model itself.
- **Solution:** adapt the LM to recursively accumulate continuous summary vectors used as soft prompts for subsequent segments.
- **Mechanisms / learning:** unsupervised continuation LM loss, segmentation and summary accumulation, adapted pretrained OPT/Llama-2. Prior segments become vectors before later segment prediction; detailed gradient truncation/randomization remains to read.
- **Evidence:** **A**, original abstract/comments/history. HTML request failed, legitimate abstract route succeeded. Perplexity, compressed demonstrations and reranking are distinct author evaluations, not all equivalent consumption tests.
- **Distinguishes:** AE is necessary versus prediction-only latent training can work; frozen-consumer versus joint adaptation. No fixed-total-state or arbitrary-detail guarantee.

<a id="a01-r07"></a>
## A01-R07 — A01-R07 — W0055 — xRAG: Extreme Context Compression for Retrieval-augmented Generation with One Token

Canonical cluster: **W0055**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:2405.13792v2](https://arxiv.org/abs/2405.13792v2), 2024-12-09; [official NeurIPS 2024 entry](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c5cf13bfd3762821ef7607e63ee90075-Abstract-Conference.html). **Existing-W unread**; formal publication verified, formal/v2 numerical equivalence unverified.
- **Prior problem:** a retrieval embedding is normally used only to find a document, and raw document processing dominates reader cost.
- **Solution:** learn a modality bridge that lets a frozen reader consume frozen document embeddings without their textual counterpart.
- **Mechanisms / learning:** dense retrieval features, multimodal-style projection/alignment, bridge-only training; original abstract does not establish the complete target mixture. One document-level vector, not an exact item-addressable memory.
- **Evidence:** **A**, arXiv and formal abstracts. The original bridge-training data/objectives and matched controls still need full reading. Claimed FLOP/quality gains are not adopted as fair system rankings.
- **Distinguishes:** insufficient representation versus consumer-interface mismatch; whole-backbone adaptation necessary versus bridge-only sufficient on some tasks. Retrieval chooses the document, but consumption of its embedding need not revisit source text.

<a id="a01-r08"></a>
## A01-R08 — A01-R08 — old N04 — Context Compression via Explicit Information Transmission (ComprExIT)

Canonical cluster: **BR-A01-R08**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:2602.03784v4](https://arxiv.org/abs/2602.03784v4), 2026-06-18; [served HTML](https://arxiv.org/html/2602.03784v4), whose heading adds *Fix the Structural Bottleneck*. **Existing-audit lead**; formal venue/acceptance not verified.
- **Source-integrity restriction:** abs text says code will be released upon acceptance; served HTML says code is available and displays a different apparent author presentation from the submitter/history cues. A submitter is not an author list; do not resolve identities by inference. Fixed PDF must adjudicate title/author/code-status alignment before final catalog promotion.
- **Prior problem:** multiple compression slots may redundantly aggregate the same source regions, and final-layer-only states may dilute intermediate evidence.
- **Solution:** aggregate across frozen layers and coordinate token-to-slot transmission using an entropy-regularized transport plan.
- **Mechanisms / learning:** cross-layer feature aggregation, learned anchors/projection and Sinkhorn normalization; selected text specifies local windows (example T=128), not unconstrained global transport. Question-unaware NTP then QA training; payload consists of compressed slots.
- **Evidence:** **A+P**, selected method/experiment passages and Appendix A.1.1–A.1.3. Reconstruction diagnostic feeds the frozen decoder gist states, a reproduce prompt and teacher-forced original tokens. It measures this reader's conditional NLL, not decoder-independent information loss. Attention correlation/effective rank are allocation diagnostics, not content-use interventions.
- **Distinguishes:** overlapping aggregation versus capacity shortage; intermediate readability versus information disappearance. Treat numeric superiority as provisional until fixed-source reconciliation and full ablation reading.

<a id="a01-r09"></a>
## A01-R09 — A01-R09 — old N03 — Neural Discrete Representation Learning (VQ-VAE)

Canonical cluster: **BR-A01-R09**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:1711.00937v2](https://arxiv.org/abs/1711.00937v2), 2018-05-30; [NeurIPS 2017 formal PDF target](https://proceedings.neurips.cc/paper/7210-neural-discrete-representation-learning.pdf). **Existing-audit lead**. This pass verified arXiv metadata/abstract; formal PDF was not newly fetched or compared.
- **Prior problem:** continuous stochastic latent models with powerful autoregressive decoders often fail to use latent codes.
- **Solution:** learn discrete codes by vector quantization with a learned prior rather than the conventional continuous posterior/prior setup.
- **Mechanisms / learning:** vector-quantized codebook and learned generative prior; full commitment/straight-through training equations remain unread in this pass. Images, speech and video are stated applications, not an unknown-query language benchmark.
- **Evidence:** **A**. Claim to circumvent a particular posterior-collapse failure is verified as the authors' claim, not a universal no-collapse guarantee.
- **Distinguishes:** stochastic-posterior information penalty versus discretization/training changes. Codebook collapse, posterior collapse and deployed ignorance require separate measures; equal slot dimensions are not equal effective bits.

<a id="a01-r10"></a>
## A01-R10 — A01-R10 — W0066 — Universal Representations for Classification-enhanced Lossy Compression

Canonical cluster: **W0066**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:2504.13191v1](https://arxiv.org/abs/2504.13191v1), 2025-04-12; [PDF target](https://arxiv.org/pdf/2504.13191v1). **Existing-W unread**; no formal publication verified.
- **Prior problem:** reusing a single encoder over multiple reconstruction/classification or perception operating points may cost task fidelity.
- **Solution:** study universal encoders across these specified constraints and compare reuse against individually optimized encoders.
- **Mechanisms / learning:** rate–distortion–classification/perception formulation and trained image encoders; MNIST, known task/constraint family. Not arbitrary future query universality.
- **Evidence:** **A**, original abstract/history; reported classification-distortion penalty and comparatively small perception penalty remain to quantify from original tables.
- **Distinguishes:** one encoder universal across operating points versus specialist reoptimization; universality across constraints versus across unseen tasks.

<a id="a01-r11"></a>
## A01-R11 — A01-R11 — old N05 — Rate-Distortion Theory in Coding for Machines and its Applications

Canonical cluster: **BR-A01-R11**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:2305.17295v2](https://arxiv.org/abs/2305.17295v2), 2025-03-04; [v2 HTML](https://arxiv.org/html/2305.17295v2). **Existing-audit lead**. Formal journal metadata not verified; do not fill it from secondary citations. Complete author order requires fixed PDF because HTML extraction omits its first-name header.
- **Prior problem:** input reconstruction distortion need not describe fidelity for a fixed downstream machine task.
- **Solution:** formulate task-output distortion for full-input, split-feature and direct-to-feature coding, and analyze their ideal rate–distortion relationship.
- **Mechanisms / learning:** learned image coding, task model splitting, feature/task distortion; the ideal construction knows the task model, not every possible later query. The full-input decoder may output a class-equivalent prototype, not the original image.
- **Evidence:** **A+P**, §II definitions/Theorems 1–2/2.A and example; all proofs and detailed empirical results unread. Equivalence requires feasible task-output/image conditions and asymptotic optimal codecs; finite learned interfaces can differ substantially.
- **Distinguishes:** input MSE versus task distortion; ideal equivalence versus practical reader/codec restrictions. Does not make feature interfaces cost-free.

<a id="a01-r12"></a>
## A01-R12 — A01-R12 — BIW-0094 — Generating Sentences from a Continuous Space

Canonical cluster: **BIW-0094**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [CoNLL 2016 formal record](https://aclanthology.org/K16-1002/), pp.10–21, DOI 10.18653/v1/K16-1002; existing partial target [arXiv:1511.06349v4](https://arxiv.org/pdf/1511.06349v4). **Existing-BIW partial**, not a new W record. Formal/arXiv text comparison not performed.
- **Prior problem:** sentence-level continuous latent variables can be ignored by an autoregressive word decoder.
- **Solution:** use a sentence VAE with KL annealing and decoder word dropout to encourage latent use.
- **Mechanisms / learning:** full-sentence recognition, Gaussian latent, LSTM autoregressive decoder and ELBO. Source is training text; whole-sentence latent has no content addresses.
- **Evidence:** fresh **metadata** plus existing **P §3.1/§4** in the BIW catalog, not a FULL card or fresh body reading. Prior evidence notes nonzero KL does not automatically beat an ordinary LM.
- **Distinguishes:** autoregressive bypass versus latent information; generative likelihood versus representation utility; stochastic word-text result versus deterministic byte-state analogy.

<a id="a01-r13"></a>
## A01-R13 — A01-R13 — BIW-0095 — Improved Variational Autoencoders for Text Modeling using Dilated Convolutions

Canonical cluster: **BIW-0095**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:1702.08139v2](https://arxiv.org/abs/1702.08139v2), 2017-06-18; [PDF target](https://arxiv.org/pdf/1702.08139v2). **Existing-BIW partial**. Formal venue not independently verified here.
- **Prior problem:** a strong sequential decoder can predict from its local context rather than the global latent.
- **Solution:** vary the receptive field of a dilated CNN decoder to control its local contextual capacity.
- **Mechanisms / learning:** Gaussian sentence latent, recognition network, causal dilated convolutions, ELBO; 20K-word vocabulary per existing record, not byte input.
- **Evidence:** fresh **A/history**, reuse of existing **P §§2.2–2.3/3.2–3.3**. The contextual-capacity/latent-use tradeoff is directly in the original abstract; complete labeling/generation controls unread.
- **Distinguishes:** decoder receptive-field effect versus inevitable uselessness of a latent; best likelihood versus best downstream representation.

<a id="a01-r14"></a>
## A01-R14 — A01-R14 — BIW-0096 — Lagging Inference Networks and Posterior Collapse in Variational Autoencoders

Canonical cluster: **BIW-0096**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:1901.05534v2](https://arxiv.org/abs/1901.05534v2), 2019-01-28; [body target](https://arxiv.org/html/1901.05534v2). **Existing-BIW partial**; prior recovery associates ICLR 2019, not newly venue-verified here.
- **Prior problem:** early inference networks fail to track the changing true model posterior, encouraging the generator to ignore latent codes.
- **Solution:** aggressively optimize the inference network before generator updates, using estimated latent–observation information to control the schedule.
- **Mechanisms / learning:** amortized inference, extra encoder optimization and ELBO, text/image benchmarks. Extra steps are optimization work, not new supervision.
- **Evidence:** fresh **A/history** and existing partial recovery, not a FULL card. Existing 2–3× timing note is a scoped prior observation, not fresh cost validation.
- **Distinguishes:** unavailable learning signal versus update imbalance; new architecture needed versus better inference optimization. Fixed-compute superiority remains open.

<a id="a01-r15"></a>
## A01-R15 — A01-R15 — Variational Lossy Autoencoder

Canonical cluster: **BR-A01-R15**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:1611.02731v2](https://arxiv.org/abs/1611.02731v2), 2017-03-04; [PDF target](https://arxiv.org/pdf/1611.02731v2). **Catalog-absent candidate**. ICLR 2017 appears in secondary search but no official decision was read; retain arXiv status in this inventory.
- **Prior problem:** unsupervised representations should sometimes retain global structure while discarding local texture that an autoregressive model can handle.
- **Solution:** design VAE plus autoregressive decoder/prior architecture to control which information the global latent must encode.
- **Mechanisms / learning:** neural autoregression (RNN/MADE/PixelCNN families) with variational latent coding; image density-estimation targets, not later-query labels.
- **Evidence:** **A**. v2 HTML returns conversion-error instructions rather than the paper; one legitimate abs fallback succeeded. Coding-argument details and free-bit controls remain unread.
- **Distinguishes:** decoder ignorance as an accidental failure versus selective information omission as an explicit task objective. Desired omission must be reanchored if exact strings are downstream targets.

<a id="a01-r16"></a>
## A01-R16 — A01-R16 — Don't Blame the ELBO! A Linear VAE Perspective on Posterior Collapse

Canonical cluster: **BR-A01-R16**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [NeurIPS 2019 official entry](https://proceedings.neurips.cc/paper/2019/hash/7e3315fe390974fcf25e44a9445bd821-Abstract.html); associated [arXiv:1911.02469](https://arxiv.org/abs/1911.02469) from search, version not independently reconciled. **Catalog-absent candidate**, formal conference paper.
- **Prior problem:** collapse is often attributed solely to variational regularization or a powerful nonlinear decoder.
- **Solution:** analyze linear VAEs through probabilistic PCA and compare ELBO and marginal-likelihood stationary structure.
- **Mechanisms / learning:** linear Gaussian latent model and exact variational inference, with selected nonlinear empirical extensions described in the abstract.
- **Evidence:** **A**, original official abstract. It states no additional ELBO spurious local maxima in the analyzed linear model and identifies principal-component global recovery with exact inference; proofs/noise assumptions not read.
- **Distinguishes:** marginal-likelihood geometry versus ELBO-induced pathology. Linear-model theorem is not a theorem about arbitrary deep sequence decoders.

<a id="a01-r17"></a>
## A01-R17 — A01-R17 — The Usual Suspects? Reassessing Blame for VAE Posterior Collapse

Canonical cluster: **BR-A01-R17**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [ICML 2020/PMLR 119:2313–2322](https://proceedings.mlr.press/v119/dai20c.html); [formal PDF target](https://proceedings.mlr.press/v119/dai20c/dai20c.pdf). Dai, Wang and Wipf. **Catalog-absent candidate**, published conference paper.
- **Prior problem:** accounts centered only on KL pressure understate bad minima in nonlinear encoder–decoder loss surfaces.
- **Solution:** analyze how nonlinear perturbations and depth create collapse/truncation minima beyond narrow affine-model guarantees.
- **Mechanisms / learning:** Gaussian VAE/deep autoencoder optimization geometry; controlled nonlinear constructions, not source-retrieval augmentation.
- **Evidence:** **A**, official abstract/metadata only; exact construction and nuisance conditions queued.
- **Distinguishes:** regularization-only explanation versus loss-surface risk; benign linear setting versus nonlinear counterexample. It refines, rather than universally falsifies, other collapse explanations.

<a id="a01-r18"></a>
## A01-R18 — A01-R18 — Cyclical Annealing Schedule: A Simple Approach to Mitigating KL Vanishing

Canonical cluster: **BR-A01-R18**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [NAACL 2019 formal record](https://aclanthology.org/N19-1021/), pp.240–250, DOI 10.18653/v1/N19-1021; [PDF target](https://aclanthology.org/N19-1021.pdf). Fu et al. **Catalog-absent candidate**, published conference paper.
- **Prior problem:** early weak latent codes cause autoregressive decoder training to settle into KL-vanishing behavior.
- **Solution:** repeatedly raise the KL weight through warm-restart cycles so previously learned codes seed subsequent training.
- **Mechanisms / learning:** time-varying ELBO weighting; language modeling, dialogue and semi-supervised classification. Changes optimization schedule, not source labels or aggregation grain.
- **Evidence:** **A**, official abstract/metadata. Complete schedule-length, compute and baselines must be read before claiming dominance over monotone annealing or inference-heavy updates.
- **Distinguishes:** formation-path dependence versus fixed-capacity failure; improved latent information versus simply longer/more favorable training.

<a id="a01-r19"></a>
## A01-R19 — A01-R19 — Variance Equalization for Posterior Collapse (search alias: λ-VAE)

Canonical cluster: **BR-A01-R19**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:2607.05531v1](https://arxiv.org/abs/2607.05531v1), 2026-07-06; [served HTML](https://arxiv.org/html/2607.05531v1). Girum Demisse. **Catalog-absent candidate**, preprint; no venue/ICLR 2027 match verified.
- **Prior problem:** reconstruction/KL gradient imbalance and information loss during stochastic sampling can both favor uninformative latents.
- **Solution:** change the reparameterization noise exponent per dimension while retaining the original posterior-variance KL penalty.
- **Mechanisms / learning:** stochastic VAE reparameterization and rate/reconstruction tradeoff control; standard image benchmarks. No language-memory query channel or addressing experiment.
- **Evidence:** **A+P introduction only**, not the theory/body/appendix despite long HTML retrieval. Up-to-2.8× capacity and BPD statements are author abstract claims, not locally audited results.
- **Distinguishes:** representation computed by an encoder versus information surviving sampling; gradient-magnitude mechanism versus decoder architecture alone. Transfer to deterministic latent interfaces is a hypothesis, not a result.

<a id="a01-r20"></a>
## A01-R20 — A01-R20 — Linear-Time Context Compression with State-Space Encoding (Boa Compressor)

Canonical cluster: **BR-A01-R20**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:2610.33006v1](https://arxiv.org/abs/2610.33006v1), 2026-10-07; [served HTML](https://arxiv.org/html/2610.33006v1). **Catalog-absent candidate**, preprint; no venue acceptance verified. HTML author/affiliation layout is malformed; do not fill full author order from submitter or presentation cues.
- **Prior problem:** Transformer-based soft compression can cost enough prefill time to erase single-query savings.
- **Solution:** learn a Mamba-2 compressor with strided hidden states and per-layer KV projections for a frozen Transformer, followed by teacher-distribution fine-tuning.
- **Mechanisms / learning:** pretrained SSM, fixed stride, KV-space bridge, LM pretraining then answer-token KL distillation. Retains `ceil(L/r)` slots, growing with L; not one constant-size state. Query-aware online discussion and experimental input visibility must be checked separately.
- **Evidence:** **A+P**, introduction, selected §§3–5 training/interface/ablation passages; full tables, latency implementation and appendices unread. Text states 10B-token LM pretraining then 500k QA pairs, fixed target and shared baseline pretraining budget, with early stopping. These are author design statements, not a full cost audit.
- **Distinguishes:** consumer-distillation target versus token reconstruction; interface placement versus encoder expressivity; cheap recurrent writer versus a fixed-state all-detail impossibility. Query-aware advantages cannot certify a query-unknown contract.

<a id="a01-r21"></a>
## A01-R21 — A01-R21 — Before Answering: Evidence Sufficiency under Size-Matched Memory Construction (MemSafe)

Canonical cluster: **BR-A01-R21**. [Carrying source record](../01_discovery/A01/WORKS_AND_PROBLEMS.md).

- **Identity:** [arXiv:2609.32269v1](https://arxiv.org/abs/2609.32269v1), 2026-09-26; [served HTML](https://arxiv.org/html/2609.32269v1). **Catalog-absent candidate**, preprint. Search mentions ICLR 2027 contexts but no official matching forum/decision verified; no acceptance claim.
- **Prior problem:** detecting insufficient compressed memory can be made spuriously easy when deleting evidence also reduces memory size.
- **Solution:** hold memory size matched across integrity states and train a query–unit cross-encoder plus set-transformer sufficiency estimator.
- **Mechanisms / learning:** supervised evidence-integrity/localization labels, cross-encoding, set aggregation and calibrated abstention gate. Query sees remaining memory; this diagnoses support, not reconstruction of missing facts. Not itself a compression writer.
- **Evidence:** **A+P introductory figure description**, not full reading. Abstract includes paragraph-count shortcut, frozen-cross-encoder control, five-seed multi-hop results, weaker unanswerable/OOD performance and low-coverage gating limits. Exact statistical construction/proofs and calibration coverage still to read.
- **Distinguishes:** evidence sufficiency versus memory-size shortcut; confidence versus support detection; unsupported answer avoidance versus restoring irrecoverable information. Clinical result was not pursued; no biological procedures or data were accessed.

<a id="a02-e01"></a>
## A02-E01 — E01 — W0199: Linear Transformers Are Secretly Fast Weight Programmers

Canonical cluster: **W0199**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [ICML 2021, PMLR 139:9355–9366 proceedings](https://proceedings.mlr.press/v139/schlag21a.html), officially verified; associated arXiv 2102.11174v3 is the same work, not necessarily identical text. **EU/A; T,E; S0**. Full PDF not read this round.
- **Prior problem → one-sentence solution:** additive outer products superpose incompatible associations → replace the purely additive instruction with a delta-like correction and a learned update rate.
- **Borrowed AI mechanisms and learning:** slow neural controller, key/value projections, fast-weight outer products, prediction-error update, learned learning rate and attention feature map; slow parameters learn by gradient descent, fast state is programmed during the sequence. Current content is available, future queries are not.
- **Distinguishing hypothesis/limits:** asks whether correcting a current mapping is preferable to accumulating raw features, rather than assuming more storage is necessary. The original repeated-key/nonorthogonal-key controls, normalization, state budget and synthetic failure regimes remain a priority read. Abstract superiority is not a general capacity theorem.

<a id="a02-e02"></a>
## A02-E02 — E02 — W0201: Gated Delta Networks: Improving Mamba2 with Delta Rule

Canonical cluster: **W0201**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2412.06464v3 HTML](https://arxiv.org/html/2412.06464v3), 2025-03-06 version from existing version register; **EU/P**, this round §§3.1–3.2, equations and S-NIAH discussion. ICLR 2025 is inherited catalog status; venue decision not newly checked. **T,U; S0** for recurrent variant; hybrids change permissions.
- **Problem → solution:** global decay rapidly forgets useful content while ungated correction can retain too much → combine scalar decay with residual key-directed writing.
- **Mechanisms/learning/units:** `S_t = alpha S_(t-1)(I-beta kk^T)+beta vk^T`; token projections, short convolution, output gate, outer-loop next-token training and inner online regression interpretation. The residual is measured against the decayed old prediction. No future answer labels at write time.
- **Original controls and discriminant:** §3.2 distinguishes repeated synthetic haystack, essay distractors, and UUID values: decay hurts the easy retention setting, while clearance helps in realistic distractors. These are separately trained models, not a clean same-weight edit; token format, distractor load and payload difficulty differ. Tests retention-versus-filtering, not “forgetting always helps.” Appendix component ablations and full state/compute accounting remain unread.

<a id="a02-e03"></a>
## A02-E03 — E03 — W0202: Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention

Canonical cluster: **W0202**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2605.22791v1](https://arxiv.org/abs/2605.22791v1), 2026-05-21, **EU/A; E,T,U; S0**.
- **Problem → solution:** one scalar edit rate ties removal of old associations to commitment of new values → separate channel-wise erase and write gates while retaining channel-wise decay.
- **Mechanisms/learning:** gated online regression/fast weights, asymmetric erase factors and chunkwise WY parallelization; language-model training of projections/gates, recurrent content update at each token.
- **Hypothesis/limits:** independent edit strengths can matter even when erase and write addresses remain linked. The abstract reports 1.3B/100B-token comparisons and multi-key RULER gains; no independent-address advantage, equal total bytes, or task-specific causal isolation follows. Compare equations against EDA, not just names.

<a id="a02-e04"></a>
## A02-E04 — E04 — W0203: Dual DeltaNet: Value-Side Memory Reorganization for Linear Attention

Canonical cluster: **W0203**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2610.38578v1](https://arxiv.org/abs/2610.38578v1), 2026-10-28, **EU/A; E,T,U; S0**.
- **Problem → solution:** correcting a key's value ignores the distribution of related value features across addresses → add a value-side delta operation to key-side correction.
- **Mechanisms/learning:** Kimi Delta Attention (KDA, a channel-decayed delta-rule recurrence), value-feature selector, two-sided regression-style reads, rank-two recurrence, chunkwise training; learned token projections and end-to-end LM objective.
- **Hypothesis/limits:** tests interference involving joint key/value geometry rather than keys alone. Abstract aggregate wins and modest overhead are not proof that value reorganization preserves every old association; update-order, equal-budget ablations, long-flow stability and independent content substitutions are missing.

<a id="a02-e05"></a>
## A02-E05 — E05 — W0088: Revisiting associative recall in modern recurrent models

Canonical cluster: **W0088**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2508.19029v2 metadata](https://arxiv.org/abs/2508.19029v2), 2025-10-10; [body](https://arxiv.org/html/2508.19029v2) §§3–8 read in this round, appendices not read. **EU/P; T,E,U; S0**.
- **Problem → solution:** architecture comparisons can mistake poorly tuned learning for representational inability → use finer learning-rate searches, width/depth scaling and component ablations on recall/copying.
- **Mechanisms/learning:** supervised synthetic associative binding/copying, Adam, Mamba/Hyena/attention/DeltaNet, convolution and gating ablations. Queries and training/test distributions are task-defined; no source revisit is needed for the recurrent candidates.
- **Controls/negative findings:** recurrent success occupies narrow learning-rate regions; some tuned one-layer Mamba variants recall without convolution, whereas one-layer attention fails until local construction is added. Width and depth are not interchangeable parameter matching. Three-seed figures, synthetic tasks, and unverified appendices limit generalization; “DeltaNet stabilizes because Householder mixing avoids gradient decay” is the authors' hypothesis, not an established causal theorem. Distinguishes optimization failure from immutable capacity.

<a id="a02-e06"></a>
## A02-E06 — E06 — W0213: Beyond State Capacity: Why Retrieval Breaks in Mamba

Canonical cluster: **W0213**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2610.19709v1 metadata](https://arxiv.org/abs/2610.19709v1), 2026-10-14; [HTML](https://arxiv.org/html/2610.19709v1), this round targeted §§3–6, §8 discussion and Appendix B patch/probe descriptions. **EU/P; T,U,E; S0**. Not a full read.
- **Problem → solution:** query-first retrieval still fails even though only a compact answer need be retained → trace relevance through representations and gates and use controlled local flags and bidirectional gate patching to localize the bottleneck.
- **Mechanisms/learning:** pretrained Mamba, local relevance marker, linear diagnostic probes, counterfactual gate replacement, oracle gate scaling; no newly trained production architecture. The flag and oracle indices are privileged experimental information, not deployable query discovery.
- **Controls/discriminant:** replacing target-digit gates in both directions transfers performance between flagged/unflagged prompts; probe relevance appears before gates align, and critical early/middle layers precede adequate alignment. This demonstrates an actionable gating failure in the tested models, not unique necessity of one causal explanation or success of a learned repair. Gate control is not general nonlinear-memory capacity, and query-first is not unknown-future-query retention.

<a id="a02-e07"></a>
## A02-E07 — E07 — W0060: Zoology: Measuring and Improving Recall in Efficient Language Models

Canonical cluster: **W0060**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2312.04927v1](https://arxiv.org/abs/2312.04927v1), 2023-12-08; **EU/A; T,U; S0/S2 by comparator**. Formal venue not newly verified.
- **Problem → solution:** easy single-query synthetic recall misses the LM gap → introduce multi-query associative recall (MQAR) and inspect recall-associated LM errors and sparse hybrids.
- **Mechanisms/learning:** supervised synthetic bindings, pretrained gated-convolution LMs, sparse input-dependent attention as a separate remedy. The attention remedy retains accessible historical representations and is not a pure fixed-state solution.
- **Hypothesis/limits:** asks which task exposes missing recall rather than generic perplexity. Abstract “82%” and “97.4%” have paper-specific denominators; original stratification and training/search budgets still need full reading. E05 is an original counterexample to interpreting an older tuning grid as an impossibility result.

<a id="a02-e08"></a>
## A02-E08 — E08 — W0242: Learning to (Learn at Test Time): RNNs with Expressive Hidden States

Canonical cluster: **W0242**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2407.04620v4](https://arxiv.org/abs/2407.04620v4), 2025-08-31; **EU/A; E,T,U; S0/S1 depending on mini-batch implementation**.
- **Problem → solution:** fixed recurrent hidden representations may be too weak → make hidden state the weights of a linear model or two-layer multilayer perceptron (MLP), updated by self-supervised test-time training (TTT).
- **Mechanisms/learning:** nested learning, reconstruction/denoising-style inner supervision from current sequence views, outer learned projections/initialization; the original objective and batching need full verification. Input/query/content units are token projections, not raw source documents.
- **Hypothesis/limits:** separates a richer learned state function from a larger static vector. Abstract reports improved context-dependent perplexity and MLP memory-I/O difficulties; it does not establish long-delay exact recall, OOD query robustness, or semantic consumption. Count fast-model parameters, gradients, buffers and optimizer state, not only the recurrent tensor.

<a id="a02-e09"></a>
## A02-E09 — E09 — W0234: Titans: Learning to Memorize at Test Time

Canonical cluster: **W0234**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2501.00663v1](https://arxiv.org/abs/2501.00663v1), actually submitted 2024-12-31; **EU/A; E,T,U; S0/S1 plus local attention by variant**.
- **Problem → solution:** local attention is precise but cannot itself retain arbitrarily old context → learn a neural long-term memory during sequence processing and combine it with short-term attention in three architectures.
- **Mechanisms/learning:** neural associative memory and test-time learning; gradient-surprise, momentum and forgetting are prior-audit mechanism leads whose exact equations and ablations remain to be read, not certified by the abstract. Outer LM/task training co-adapts memory and attention.
- **Hypothesis/limits:** can nonlinear memory and update dynamics improve learned retention without an original-text archive? Reported >2M needle tests do not establish high-load unknown-query exact retention, and a surprising write need not be useful to a later query. Local attention and persistent components must be budgeted.

<a id="a02-e10"></a>
## A02-E10 — E10 — W0240: Hopfield Networks is All You Need

Canonical cluster: **W0240**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2008.02217v3](https://arxiv.org/abs/2008.02217v3), 2021-04-28; ICLR 2021 inherited from catalog, not newly decision-verified. **EU/A; C,E,U; S2**.
- **Problem → solution:** classical associative networks have limited pattern storage → continuous-state energy and attention-equivalent updates admit stronger retrieval/storage regimes.
- **Mechanisms/learning:** energy-based associative retrieval, softmax-like similarity, learned prototypes or stored patterns; query update can converge to a single pattern, a subset average, or a global average.
- **Hypothesis/limits:** nonlinear read dynamics can change basins and retrieval error, but exponential pattern capacity is not fixed-total-byte state capacity: patterns/keys are explicit arguments. Exact theorem separation/radius/precision assumptions remain unread. E11 supplies a practical negative control to abstract capacity rhetoric.

<a id="a02-e11"></a>
## A02-E11 — E11 — W0241: Modern Hopfield Networks meet Encoded Neural Representations — Addressing Practical Considerations

Canonical cluster: **W0241**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2409.16408v2 HTML](https://arxiv.org/html/2409.16408v2), version date 2024-10-30 inherited from audit; this round §§1–3.1 and opening §3.2 read, later sections/appendix not obtained in the returned excerpt. **EU/P; U,E; S2**.
- **Problem → solution:** real correlated high-dimensional patterns create metastable mixtures despite attractive ideal capacity → encode patterns with a pretrained autoencoder before associative storage and decode after recall.
- **Mechanisms/learning:** vector-quantized/variational autoencoders, energy-based iterative cleanup, similarity/temperature selection, language-to-image heteroassociation. The pattern matrix remains stored; this is no raw-text archive but not a bounded compressed-state substitute.
- **Controls/negative findings:** §3.1 compares raw images, several encoder/decoder families, dot/L2 similarities, and kernel-memory alternatives; raw/ kernel variants can fail on 6,000-image banks. “Perfect recall” here concerns identity of stored encoded reconstructions, not exact original pixels. Separability changes, decoder distortion and bank bytes cannot be erased from the comparison. Distinguishes ideal random-pattern theorem from correlated-data usability; not yet evidence for OOD language-query generalization.

<a id="a02-e12"></a>
## A02-E12 — E12 — W0232: Sharp Capacity Scaling of Spectral Optimizers in Learning Associative Memory

Canonical cluster: **W0232**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2603.26554v2](https://arxiv.org/abs/2603.26554v2), 2026-04-28; **EU/A; C,T; static training memory, not a deployment fast-state mechanism**.
- **Problem → solution:** optimizer-dependent factual recovery can be mistaken for an architecture capacity difference → characterize one-step Muon, stochastic gradient descent (SGD), and Newton recovery on a linear associative-memory model.
- **Mechanisms/learning:** Gaussian input/output embeddings, logistic loss, power-law frequency, spectral preconditioning; multi-step analysis uses a thresholded-gradient approximation.
- **Hypothesis/limits:** a fixed parameterized memory can have different early reachable capacity under different optimizers. Abstract says Muon and SGD ultimately converge to the information-theoretic limit at comparable speeds in the analyzed setting; do not convert its one-step advantage into a larger universal storage upper bound or an established online-memory recipe.

<a id="a02-e13"></a>
## A02-E13 — E13 — W0086: The Key to State Reduction in Linear Attention: A Rank-based Perspective / later catalog title On State Reduction in Linear Attention

Canonical cluster: **W0086**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2602.04852v1](https://arxiv.org/abs/2602.04852v1), 2026-02-04; source history also lists v3 2026-09-29, not read as equivalent. **EU/A; C,U; S0**.
- **Problem → solution:** trained state often has low effective rank → analyze query-noise amplification and prune key/query channels with rank-revealing QR and other structured methods.
- **Mechanisms/learning:** post-training matrix diagnostics and hardware-compatible structured pruning; learned language-model state is the object, not retraining a new memory.
- **Hypothesis/limits:** distinguishes nominal tensor size from accessible effective rank. Abstract says 50% key/query channels can be removed with marginal perplexity cost; that does not imply rare exact bindings are redundant. N02 and N04 below make rank-versus-use and memory-quality comparisons more specific.

<a id="a02-p01"></a>
## A02-P01 — P01 — prior N02-1: It's All Connected: A Journey Through Test-Time Memorization, Attentional Bias, Retention, and Online Optimization (MIRAS)

Canonical cluster: **BR-A02-P01**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2504.13173v1](https://arxiv.org/abs/2504.13173v1), 2025-04-17, **PA/A; E,T,U; S0/S1 by instance**.
- **Problem → solution:** architecture discussions conflate memory structure, fitting objective and forgetting → factor design into memory architecture, inner objective, retention regularization and learning algorithm.
- **Mechanisms/learning:** associative regression, non-L2 inner losses, retention regularizers, approximate online optimizers, outer-trained sequence models Moneta/Yaad/Memora.
- **Hypothesis/limits:** tests whether retaining useful state requires changing an objective/regularizer rather than adding a source store. Framework unification is not evidence that each regularizer improves long-delay retention; exact objectives, stability assumptions and equal-budget negatives remain unread.

<a id="a02-p02"></a>
## A02-P02 — P02 — prior N02-2: HiPPO: Recurrent Memory with Optimal Polynomial Projections

Canonical cluster: **BR-A02-P02**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2008.07669v2](https://arxiv.org/abs/2008.07669v2), 2020-10-23, **PA/A; C,E,T,U; S0**. NeurIPS 2020 status not freshly authenticated here; quote the public version rather than asserting a new venue check.
- **Problem → solution:** incremental history summaries depend on fragile timescale choices → project history onto polynomial bases under an explicit time-importance measure.
- **Mechanisms/learning:** online function approximation, Legendre projection, controlled recurrent dynamics integrated into a learned RNN; signal/trajectory and permuted-MNIST supervision.
- **Hypothesis/limits:** stable sufficient statistics may be a better target than exact-history reconstruction. Optimality is for a function-approximation objective, not arbitrary delayed facts; OOD timescale classification is not OOD key/query binding. Discretization and finite-precision robustness need original proof/experiment review.

<a id="a02-p03"></a>
## A02-P03 — P03 — prior N02-3: Anatomy of Associative Recall in Fixed-State Recurrences: A Matched-State Decomposition, an Interference Wall, and a Curriculum That Breaks It

Canonical cluster: **BR-A02-P03**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2609.16183v1 metadata](https://arxiv.org/abs/2609.16183v1), 2026-09-14; [HTML](https://arxiv.org/html/2609.16183v1), this round §§3.2–10 plus selected floor/rebinding text; no complete appendix/figure/table inspection. **PA/P; T,U; S0 for causal cells**; bidirectional denoisers have different query visibility.
- **Problem → solution:** load, distance, local binding and optimization are confounded → hold recurrent state at 1,024 elements in the constrained setting, toggle components and change distance curricula.
- **Mechanisms/learning:** masked synthetic MQAR, convolution/rank-one/diagonal/decay factorial, fresh random values, first-binding collision targets, supervised distance ramps, success-gated schedule; outer training only, no external text memory.
- **Controls/discriminant:** rebinding scored against the old answer defeats salience shortcuts; separate load and gap tests, learning-rate sweeps, matched-state official-kernel comparison, seed lock-in rates and state-tracking guardrail are substantive. Tuned convolution gaps are smaller than matched-LR gaps. Causal and bidirectional shaped-curriculum arms reach directional parity, countering the tempting “query-first for free” explanation.
- **Important internal conflict:** §4.2 reports no measurable decay mean effect at 20 seeds (p=.86), while §10 still calls a −.32 decay tax real; §9/§10 retain outdated length-boundary and directionality phrasing despite §6/§7 extensions. Do not quote discussion summaries over the qualified results. First-binding collision is not latest-value replacement. Companion LM/OOD claims are second-hand here and are not counted as another paper.

<a id="a02-p04"></a>
## A02-P04 — P04 — prior N02-4: Erase-then-Delta Attention: Decoupling Erase and Write Addresses in Delta-Rule Linear Attention

Canonical cluster: **BR-A02-P04**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2606.26560v1](https://arxiv.org/abs/2606.26560v1), 2026-06-25; [HTML](https://arxiv.org/html/2606.26560v1) obtained but only opening motivation inspected. **PA/A plus introduction; E,T,U; S0**. Author metadata use abstract page (Xiao Li first), since extracted HTML omits the first name.
- **Problem → solution:** an edit at the write key cannot independently remove a stale association elsewhere → perform a learned direction-specific erase before the ordinary delta corrective write.
- **Mechanisms/learning:** independent erase-address projection, targeted rank-one suppression, residual write, learned gates and next-token pretraining; token-granularity recurrent memory, not document navigation.
- **Hypothesis/limits:** independent addresses differ from E03's independent channel-wise strengths and E04's value-side reorganization. Abstract claims dense/MoE and long-context gains; directions, contractions, added parameters and cleanup probes require full reading. No conclusion that it knows future relevance or safely deletes all stale facts.

<a id="a02-n01"></a>
## A02-N01 — N01 — LeapQuant: Efficient Linear Attention with Accurate Recurrent State Quantization

Canonical cluster: **BR-A02-N01**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2609.38166v1 metadata](https://arxiv.org/abs/2609.38166v1), 2026-09-29; [HTML](https://arxiv.org/html/2609.38166v1), introduction, targeted §3.2, Fig.3 description and §4.4/Tables 2–3 read. **NEW/P; U/numerics; S1**.
- **Problem → solution:** recurrent re-quantization compounds rounding errors and state outliers → quantize only at window boundaries, retain recent higher-precision updates and high-precision compensator vectors, and smooth residuals.
- **Mechanisms/learning/permissions:** training-free mixed precision, low-rank outlier representation and windowed recurrence; default p=16, r=4 FP16 compensators (8 at 4-bit), FP32 scales. The buffer holds recent projected updates, not an unlimited original-text archive. It must still be charged as storage and replay work.
- **Original negatives/controls:** Qwen3.5-9B §4.4 AIME/LiveCodeBench reports FP32 87.9/64.1, per-step BF16 72.1/49.6, per-step INT8 7.1/9.2; per-window INT8 restores 82.4/60.6, then compensators/smoothing restore 87.9/64.1. Larger p=32 slows kernels without further quality gain; r=16 exposes overhead and can be slower than FP32. These are author-reported ordered additions, not all interactions of a full factorial.
- **Hypothesis/limits:** finite-dimensional geometry is not finite-precision behavior; failure can come from repeated rounding at fixed shape. Matched state MSE and long reasoning accuracy do not isolate old-fact retention, and hybrid attention can carry part of task use. 1.19 bytes/element boundary state excludes the separately charged active update buffer.

<a id="a02-n02"></a>
## A02-N02 — N02 — State Rank Dynamics in Linear Attention LLMs

Canonical cluster: **BR-A02-N02**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2602.02195v1](https://arxiv.org/abs/2602.02195v1), 2026-02-02; **NEW/A; U/diagnostics; S0**.
- **Problem → solution:** state size obscures head-specific dynamics → characterize low/high effective-rank groups and propose joint rank-norm pruning.
- **Mechanisms/learning:** singular-spectrum diagnostics, head probes/ablation and zero-shot pruning of pretrained models; rank patterns are reported as acquired during pretraining.
- **Hypothesis/limits:** low rank need not mean low importance: abstract claims low-rank heads are indispensable for reasoning and high-rank heads redundant. This directly warns against discarding low-energy heads by generic capacity intuition. Causal specificity, norm/rank interactions, original task suite and persistent-state versus attention-KV accounting remain unread.

<a id="a02-n03"></a>
## A02-N03 — N03 — Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling

Canonical cluster: **BR-A02-N03**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2609.36529v1](https://arxiv.org/abs/2609.36529v1), 2026-09-29; **NEW/A; E,T,U; S0**.
- **Problem → solution:** larger matrix states can require costly projection/parameter growth → write key × second-key × value into a third-order state and read with two query contractions.
- **Mechanisms/learning:** tensor-product binding, delta/forget gates and chunkwise parallelization; token projections learned by LM training.
- **Hypothesis/limits:** parameter-efficient expansion and factorized addressing might allocate capacity differently from wider heads or more matrices. An E-dimensional second key multiplies state by E; extra capacity is not free or equal-total-byte evidence. Need same-state, same-query-function and same-training comparisons, not a “3D beats 2D” class claim.

<a id="a02-n04"></a>
## A02-N04 — N04 — SPARE: Fast Linear Attention Decoding with Compact Recurrent States

Canonical cluster: **BR-A02-N04**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2611.07552v1](https://arxiv.org/abs/2611.07552v1), official v1 history **2026-11-05** (search result displays Nov 6); [HTML](https://arxiv.org/html/2611.07552v1), §§1–6, theorem statement and Appendix B implementation/accounting text inspected; no independent code, graph digitization or proof audit. **NEW/P; U/numerics; S0**.
- **Problem → solution:** dense recurrent state traffic persists despite fixed-length memory → operate in a fixed key subspace, allocate heterogeneous per-head ranks and compensate projected write strength.
- **Mechanisms/learning:** training-free key principal-component analysis (PCA), state-spectrum budget allocation, bounded inverse projected-norm compensation, packed GPU state kernels; calibration on model inputs, not future answer labels. Online states remain FP32.
- **Original controls/negatives:** pure 1.3B GDN, 24×8 heads, key/value width 256; compares coordinate pruning and uniform ranks at matched recurrent-state bytes without recovery fine-tuning. At 12 MiB, reported retrieval 60.35% versus coordinate-pruning 33.20%; compressed models still degrade relative to Dense. Uniform ranks can give slightly better NLL at small budgets; some coordinate-pruned points win on individual tasks. Four-choice synthetic retrieval is 512 prompts, with ablations at depths 64/128, not arbitrary long unknown queries.
- **Hypothesis/limits:** preserving dominant spectral energy is neither sufficient nor necessary for exact content. The exactness theorem assumes every key stays in the fixed subspace; real calibration/OOD shift violates that premise. Shared bases, convolution state and workspaces sit outside per-request recurrent-state numbers. Peak batch-512 speedups do not establish continuous-serving throughput or general memory capacity.

<a id="a02-n05"></a>
## A02-N05 — N05 — Kronecker Delta Rule for Long Context Linear Attention (KronLSTM)

Canonical cluster: **BR-A02-N05**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2610.26834v1](https://arxiv.org/abs/2610.26834v1), 2026-10-19; [HTML](https://arxiv.org/html/2610.26834v1) introduction/Fig.1 motivation only inspected. **NEW/A plus introduction; E,T,U; S0**. An indexed OpenReview same-title lead exists, but official forum/PDF is challenge-blocked; **no ICLR 2027 status or cross-version identity certification**.
- **Problem → solution:** a delta update can perturb associations sharing a key → revise a single matrix-space direction so interference depends on both key and value overlap.
- **Mechanisms/learning:** Kronecker-product association, rank-one matrix-space revision, Markov-chain/steady-state analysis, end-to-end LM training. Norm-boundedness is an author theoretical claim under unread assumptions.
- **Hypothesis/limits:** memory editing geometry rather than raw state expansion may reduce collateral damage. A bounded expected norm does not guarantee every finite-precision trajectory, low-probability binding or OOD query. Need nonorthogonal key/value controlled data and direct comparison to E04's two-sided edit before choosing a mechanism.

<a id="a02-n06"></a>
## A02-N06 — N06 — Longhorn: State Space Models are Amortized Online Learners

Canonical cluster: **BR-A02-N06**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2407.14207v1](https://arxiv.org/abs/2407.14207v1), 2024-07-19; versions through v5 exist but are not read here. **NEW/A; E,T,U; S0**. It was cited inside W0229's existing card, but had no standalone entry in either inspected catalog; this is recovery of a missing work entity, not discovery of an unknown idea.
- **Problem → solution:** ad hoc recurrence design hides its optimization assumptions → derive an implicit online-regression update and amortize it as an SSM layer.
- **Mechanisms/learning:** implicit/proximal online learning, quadratic regression, learned token-dependent projections and outer sequence-model training.
- **Hypothesis/limits:** stable conservative updates may differ from explicit delta-SGD at identical functional state. W0229 already interprets the mechanism; newly verifying Longhorn does not count that interpretation twice. Full original key correlations, changing targets and costs remain unread.

<a id="a02-n07"></a>
## A02-N07 — N07 — RWKV-7 “Goose” with Expressive Dynamic State Evolution

Canonical cluster: **BR-A02-N07**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [2503.14456v2](https://arxiv.org/abs/2503.14456v2), 2025-03-30; **NEW/A; E,T,U; S0**.
- **Problem → solution:** efficient recurrence needs richer dynamic transitions → generalize delta updates with vector gates, in-context rates and relaxed value replacement.
- **Mechanisms/learning:** gated fast/matrix state, trainable token mixing and multilingual LM training, regular-language/state-tracking analysis.
- **Hypothesis/limits:** expressible sequential algorithms can differ without extra source permissions. “Recognize all regular languages” and a conditional circuit-complexity comparison do not mean unlimited random-fact storage, learned exact retrieval or greater bit capacity. Compared model training tokens/data differ; no controlled claim that the update rule alone causes multilingual performance is made.

<a id="a02-n08"></a>
## A02-N08 — N08 — Dense Associative Memory for Pattern Recognition

Canonical cluster: **BR-A02-N08**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [NIPS 2016 official proceedings version](https://proceedings.neurips.cc/paper/2016/hash/eaae339c4d89fc102edd9dbdb6a28915-Abstract.html), formal proceedings verified; associated arXiv 1606.01164 is not an additional work. **NEW/A; C,E,U; S2/learned pattern representation**.
- **Problem → solution:** classical associative pattern storage and recognition are limited → use higher-order energy interactions and a duality with unusual feedforward activations.
- **Mechanisms/learning:** energy-based memory, rectified high-degree polynomial features, feature-matching/prototype interpolation; XOR and MNIST are the abstract's example evaluations.
- **Hypothesis/limits:** nonlinear associative computation is an independent alternative to linear state rules, but the count of neurons is not a total parameter/bit budget. No original-text archive is required; stored prototypes/interactions still cost memory. Full basin/capacity assumptions and online trainability remain unread.

<a id="a02-n09"></a>
## A02-N09 — N09 — Gated Fast Weights for Associative Retrieval

Canonical cluster: **BR-A02-N09**. [Carrying source record](../01_discovery/A02/WORKS_AND_PROBLEMS.md).

- **Source/version/status/depth:** [official OpenReview PDF HJ8W1Q-0Z](https://openreview.net/pdf?id=HJ8W1Q-0Z), unnumbered PDF headed **“Under review as a conference paper at ICLR 2018”**, anonymous authors; **NEW/P**, extracted §§1–6 and limitations, numeric table cells/curves not fully recovered. Final venue decision/version date unknown. No attempt to identify authors. **T,U; S0**.
- **Problem → solution:** fast-weight programs can learn only trivial outputs on complex sparse query supervision → generate an elementwise gate and candidate weight matrices separately, blending the new program with the old one.
- **Mechanisms/learning:** slow recurrent controller, fast recurrent network, outer-product gate/candidate, post-activation layer normalization, shared embedding/output, one-step delayed writes to discourage a slow-path prediction bypass; truncated backpropagation with Nadam.
- **Original negatives/controls:** §4 reports earlier feedforward/recurrent fast-weight variants failed to predict nontrivial outputs despite searches; all-token accuracy is misleading because blanks dominate, so nonblank partial accuracy/BPC is reported. Keys 2–4 symbols, single-symbol values, 1–10 writes per query; training unroll 32, batch 256. A common chosen LR across models follows initial searches, not tuning-invariant proof.
- **Hypothesis/limits:** trainable memory and useful memory differ even in the original fast-weight lineage; gating, normalization and forcing use may change learnability. §§5–6 explicitly report backward storage of all changing matrices and substantial wall-time overhead. No general extrapolation to modern LM OOD query use.

<a id="a03-d01"></a>
## A03-D01 — D01 — Neural Turing Machines [A; prior audit A01; P]

Canonical cluster: **BR-A03-D01**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Alex Graves, Greg Wayne, Ivo Danihelka. [1410.5401v2](https://arxiv.org/html/1410.5401v2), 2014-12-10; [PDF](https://arxiv.org/pdf/1410.5401v2). Technical report/preprint; formal venue not verified. Official Atom confirms the three authors and version.

**Prior problem:** recurrent hidden-state capacity does not make variable binding and long algorithmic access easy to learn. **One-sentence solution:** attach a differentiable memory matrix with controller-produced read/write weightings combining content matching and relative location shifts. **Borrowed mechanisms/roles:** cosine attention supplies content addresses; interpolation, circular convolution and sharpening implement address movement; LSTM-inspired erase/add gates separate removal from insertion. Controller and addresses learn from supervised sequence cross-entropy, not gold memory locations.

**Evidence read:** original §§3.1–3.4, §4.1 and part of §4.2. A feedforward controller's simultaneous access is constrained by head count; a recurrent controller can retain previous reads. Copy extrapolation eventually wraps the 128-slot memory; repeat-count extrapolation can miss termination. These are author-reported limits, not general language-memory guarantees.

**Distinguishes:** content vs positional address formation; simultaneous independent heads vs serial computation; read/write alignment vs mere storage. **Transfer/cost:** finite matrix and dense soft attention; no original-source revisit. Position generalization, access width and controller recurrence must be separately controlled.

<a id="a03-d02"></a>
## A03-D02 — D02 — Dynamic Neural Turing Machine with Soft and Hard Addressing Schemes [A; prior audit A02; P]

Canonical cluster: **BR-A03-D02**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Caglar Gulcehre, Sarath Chandar, Kyunghyun Cho, Yoshua Bengio. [1607.00036v2](https://arxiv.org/html/1607.00036v2), 2017-03-17; [PDF](https://arxiv.org/pdf/1607.00036v2). Metadata title says “Soft and Hard”; HTML heading says “Continuous and Discrete.” Same work/version, not two papers. Venue not independently verified.

**Prior problem:** fixed linear location shifts restrict learned access, and a recurrent controller can ignore dynamic memory. **Solution:** partition each cell into a learned fixed address and writable content, train continuous or discrete access, and regularize read/write consistency. **Borrowed mechanisms:** cosine addressing, learned least-recently-used correction, REINFORCE with variance reduction, continuous-to-discrete curriculum, auxiliary next-input prediction. Main loss is task likelihood; the address part is a slow parameter, not runtime-written content.

**Evidence read:** §§2–4.3 and §§6.1–6.3/Table 1; extraction ends at §6.4. §4.3 explicitly reports an address-as-extra-weights shortcut that ignores content. Its consistency penalty aligns reading with historical write weights, not with gold semantic identity. Table 1/§6.3 also acknowledge a gap to MemN2N/DMN+; discrete feedforward access is hard to train and uses longer training.

**Distinguishes:** a query can exist yet fail to read dynamic content; alignment/optimization can fail without changing granularity. **Cost/failure:** taskwise bAbI training, finite 120 cells in the discussed setup, extra regularizers and curriculum; not equal-compute proof that a consistency loss repairs arbitrary native readers.

<a id="a03-d03"></a>
## A03-D03 — D03 — Homogeneous Keys, Heterogeneous Values: Exploiting Local KV Cache Asymmetry for Long-Context LLMs [A; prior audit A03; P]

Canonical cluster: **BR-A03-D03**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Wanyun Cui and Mingwei Xu. [2506.05410v2](https://arxiv.org/html/2506.05410v2), 2025-11-06; [PDF](https://arxiv.org/pdf/2506.05410v2). [Official NeurIPS 2025 poster entry](https://neurips.cc/virtual/2025/poster/117046) retrieved. This is the **merging AsymKV**, not D16's quantization AsymKV.

**Prior problem:** adjacent attention keys can be similar while values differ; uniform KV merging confounds selection and payload error. **Solution:** merge approximately homogeneous keys, sum values, and retain cardinalities in attention normalization. **Borrowed mechanisms:** second-order Taylor/Newton reasoning, diagonal Fisher approximation, adjacent-cache merging, count-aware normalization. No weight fine-tuning is required, but key gradients are computed during compression.

**Evidence read:** §§3.1–3.3, §4.6 description; §§3.2 equations (7)–(11) explicitly rechecked. The exact identity holds **after keys have been replaced by identical embeddings**. The original distinct-key replacement remains approximate. §3.1 drops gradient terms for stability; §3.3.2 states selective gradient computation. §4.6 crosses four key-merge schemes with same-rule vs asymmetric value merging; complete numerical tables/appendices remain unread.

**Distinguishes:** content loss vs address loss vs repeated softmax mass. **Transfer/cost:** exact equality concerns a particular attention operator, not recovery of original individual values, and not repeated delta-rule writes. Integer counts, gradient construction and retained cache bytes belong in the cost ledger.

<a id="a03-d04"></a>
## A03-D04 — D04 — Reducing Transformer Key-Value Cache Size with Cross-Layer Attention [A; prior audit A04; P]

Canonical cluster: **BR-A03-D04**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** William Brandon et al. [2405.12981v1](https://arxiv.org/html/2405.12981v1), 2024-05-21; [PDF](https://arxiv.org/pdf/2405.12981v1). Official Atom confirms five authors. Preprint; formal venue not verified.

**Prior problem:** independent per-layer KV caches multiply persistent memory. **Solution:** let several query-producing layers reuse KV computed by an earlier layer. **Borrowed mechanisms:** multi-query/grouped-query sharing extended along depth; ordinary autoregressive training from scratch learns the altered architecture.

**Evidence read:** §2.1–2.3 and abstract/results overview. Shared KV has fewer writers but still multiple readers; this is not multiple layers writing into a common summary. §2.3 notes that each consuming layer still rereads shared KV from memory, so reduced storage does not automatically reduce decode attention bandwidth.

**Distinguishes:** writer independence vs query independence vs residual/value mixing across depth. **Cost/failure:** compare resident KV bytes, projections, communication and repeated reads, not just number of cached layers. Full training/quality frontiers and appendix controls remain unread.

<a id="a03-d05"></a>
## A03-D05 — D05 — The Devil in Linear Transformer [A; prior audit A06; M]

Canonical cluster: **BR-A03-D05**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Zhen Qin et al. [EMNLP 2022 official record](https://aclanthology.org/2022.emnlp-main.473/), pp. 7025–7041, DOI 10.18653/v1/2022.emnlp-main.473; [PDF](https://aclanthology.org/2022.emnlp-main.473.pdf). Official proceedings version is the reading target, not an unspecified arXiv revision.

**Prior problem:** linear transformers suffer unstable attention gradients and dilution over long sequences. **Solution:** replace the problematic scaling with normalization and use early diagonal/local attention. **Borrowed mechanisms:** normalization for stable optimization plus a locality prior; these are separate interventions. **Learning:** end-to-end task training, as stated in the abstract; exact schedules/ablations not read.

**Depth:** official abstract and bibliography only. Unbounded-gradient theorem, denominator assumptions and complete ablations are **unread**.

**Distinguishes:** numerical/training failure and broad attention dilution from irreversible content loss. It cannot yet establish which normalization alone improves address binding, or whether the early-local mechanism explains a result. No source revisit required; no universal fix inferred.

<a id="a03-d06"></a>
## A03-D06 — D06 — MHLA: Restoring Expressivity of Linear Attention via Token-Level Multi-Head [U = W0219; P]

Canonical cluster: **W0219**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Kewei Zhang et al. [2601.07832v2](https://arxiv.org/html/2601.07832v2), 2026-01-14; [PDF](https://arxiv.org/pdf/2601.07832v2). Preprint; venue not verified. Existing catalog already contains W0219, so not new.

**Prior problem:** a shared global linear-attention summary can collapse query-specific representational diversity. **Solution:** partition along the token dimension, compute local summaries and mix them with a learned coefficient matrix. **Borrowed mechanisms:** multi-head factorization moved to token groups; blockwise matrix multiplication; learned position-indexed coefficients. These heads are not automatically independent channel heads or arbitrary learned slot addresses.

**Evidence:** metadata/abstract and method §4.1–4.2 recovered from current HTML and the prior audit; appendix causal/streaming details not fully read. Static learned coefficients should not be silently relabeled input-generated routing. Complexity's constants depend on the number of groups; the extracted profiling discussion mentions the regime M²<N.

**Distinguishes:** avoiding one global summary vs learning better native queries vs adding state. **Cost/failure:** causal masking, group count, current-block visibility and matched resident state need full reading before a generative-memory comparison.

<a id="a03-d07"></a>
## A03-D07 — D07 — On State Reduction in Linear Attention [U = W0086; M]

Canonical cluster: **W0086**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Philipp Nazari and T. Konstantin Rusch, [2602.04852v3](https://arxiv.org/abs/2602.04852v3), 2026-09-29; [PDF](https://arxiv.org/pdf/2602.04852v3). Preprint; venue not verified. Both authors recovered from official Atom.

**Prior problem:** trained recurrent states may underuse nominal capacity. **Solution:** analyze key/value-induced state rank and structurally prune key/query projections using rank-revealing QR while preserving fast-kernel shapes. **Borrowed mechanisms:** structured pruning, matrix rank analysis, QR factorization; post-pretraining reduction rather than adding a retrieval hierarchy.

**Evidence:** original abstract/history/Atom only. Authors claim states can often be halved with modest perplexity cost; retrieval-specific failures and pruning adaptation details are unread.

**Distinguishes:** actual task-relevant rank deficiency vs harmless redundancy. **Boundary:** low rank is not automatically lost information, and perplexity retention is not proof of preserved rare-identifier recall. Exact rank object and finite-precision conditions must be read. Nominal matrix size is not trained usable capacity.

<a id="a03-d08"></a>
## A03-D08 — D08 — Dual DeltaNet: Value-Side Memory Reorganization for Linear Attention [U = W0203; M]

Canonical cluster: **W0203**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Yixiao Qian et al. [2610.38578v1](https://arxiv.org/abs/2610.38578v1), 2026-10-28; [PDF](https://arxiv.org/pdf/2610.38578v1). Six authors confirmed by official Atom; preprint, venue not verified.

**Prior problem:** key-side delta corrections do not explicitly reorganize how related values occupy addresses. **Solution:** add a complementary value-side read/update to KDA, with a two-sided delta rule and rank-2 recurrence. **Borrowed mechanisms:** associative-memory residual correction, dual matrix views Sᵀk and Se, chunkwise parallelization. Main language-model training and selector learning particulars remain unread.

**Evidence:** abstract and version identity only. “Strongest overall” is the authors' abstract claim, not an audited ranking. **Distinguishes:** write-side interference/reorganization from coarse query granularity, with no source revisit. Need the value-selector inputs, leakage permissions, separate key/value update ablations, rank/cost and negative results before recommending it.

<a id="a03-d09"></a>
## A03-D09 — D09 — Hopfield Networks is All You Need [U = W0240; P]

Canonical cluster: **W0240**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Hubert Ramsauer et al. [2008.02217v3](https://arxiv.org/html/2008.02217v3), 2021-04-28; [PDF](https://arxiv.org/pdf/2008.02217v3). Existing catalog records ICLR 2021; this pass verifies arXiv version, not the decision forum anew.

**Prior problem:** classical associative-memory dynamics and modern attention need a common continuous retrieval formulation. **Solution:** define a log-sum-exp energy and continuous update with attention-shaped association. **Borrowed mechanisms:** energy minimization, concave-convex procedure, softmax, learned query/key/value projections. Hopfield layers can be trained inside downstream architectures; the theorem does not guarantee the native query is learned.

**Evidence read:** §2 equations (1)–(10), definitions and Theorems 1–5; proofs/remaining experiments unread. One-step closeness requires sufficient pattern separation and a nearby query; convergence can be to global averaging or metastable clusters rather than the desired fact. Explicit stored patterns remain in the operator.

**Distinguishes:** single-step retrieval sufficiency under basin conditions vs iterative query refinement; approximation error vs wrong attraction basin. **Boundary:** exponential patterns in feature dimension is not a constant-total-bits language-memory guarantee, and arbitrary independently projected KV recurrence does not automatically inherit the same energy descent.

<a id="a03-d10"></a>
## A03-D10 — D10 — Object-Centric Learning with Slot Attention [U = W0100; M; original HTML blocked]

Canonical cluster: **W0100**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Francesco Locatello et al. [2006.15055v2 PDF](https://arxiv.org/pdf/2006.15055v2), 2020-10-14. Official Atom verifies title, eight authors, version and author comment “NeurIPS 2020”; formal proceedings not separately opened. HTML failed twice, initial attempt plus one retry.

**Prior problem:** distributed visual representations do not explicitly separate compositional objects. **Solution:** produce exchangeable slots that specialize through competitive attention over multiple rounds. **Borrowed mechanisms:** iterative attention and competition; training on object discovery/property prediction, per official abstract.

**Evidence:** official abstract/metadata only. GRU update, normalization direction and full ablations are not newly verified and are deliberately left for reading.

**Distinguishes:** multiple slot vectors vs independently bound slots and one-shot vs iterative assignment. **Boundary:** object-centric bidirectional perception does not establish causal streaming text-memory behavior or independent queries at deployment. This is a recovered unread classic, not an existing full card.

<a id="a03-d11"></a>
## A03-D11 — D11 — End-To-End Memory Networks [N; P]

Canonical cluster: **BR-A03-D11**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, Rob Fergus. [1503.08895v5](https://arxiv.org/html/1503.08895v5), 2015-11-24; [PDF](https://arxiv.org/pdf/1503.08895v5); [official NIPS 2015 proceedings entry](https://proceedings.neurips.cc/paper/5846-end-to-end-memory-networks). No matching stable ID in either supplied catalog.

**Prior problem:** discrete supporting-fact supervision and one-shot access limit flexible memory reasoning. **Solution:** train differentiable memory reads end-to-end from answer supervision and update the query across hops. **Borrowed mechanisms:** separate address/output embeddings, softmax attention, recurrent query updates u(k+1)=u(k)+o(k), adjacent or layerwise weight tying, linear-start curriculum. Supporting-fact labels are not required for its main model.

**Evidence read:** §§2.1–2.2, §§4.1–4.4/Table 1, §5's query construction and stated limitations. In the language-model arm the initial query is a fixed 0.1 vector, not the current token's hidden state. Multi-hop gains coexist with hard task failures; more hops do not monotonically improve every row. Ten restarts and choosing a best run on some settings constrain the evidence.

**Distinguishes:** adaptive query computation vs additional parameter depth vs seeing more source. **Cost/failure:** all memory entries remain available and repeated hops cost extra computation; original task setup is not a fixed compressed-state model. Control by repeating the first read, adding a compute-matched non-reading network, and holding memory fixed.

<a id="a03-d12"></a>
## A03-D12 — D12 — GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints [N; P]

Canonical cluster: **BR-A03-D12**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Joshua Ainslie et al. [2305.13245v3](https://arxiv.org/html/2305.13245v3); [EMNLP 2023 official entry](https://aclanthology.org/2023.emnlp-main.298/), [PDF](https://aclanthology.org/2023.emnlp-main.298.pdf). Version number locked; exact v3 date not independently recovered in this pass.

**Prior problem:** full KV-head diversity costs decode bandwidth, while one KV head can degrade quality and stability. **Solution:** share KV within query-head groups and adapt mean-pooled MHA checkpoints with additional pretraining. **Borrowed mechanisms:** grouped parameter sharing, checkpoint averaging and continued pretraining. Native query heads remain distinct even when KV are shared.

**Evidence read:** §§2–3.3 and Appendix A. Original uptraining proportion sweep compares zero/5%/10%; MQA needs adaptation to become useful, while GQA fares better immediately. Mean/first/random initialization are compared. §3.1 reports roughly 600 TPUv3 chip-days for 5% adaptation: “small fraction” is not a free repair. Only encoder-decoder hosts tested; XXL from-scratch counterpart missing.

**Distinguishes:** replacement shock vs permanent representational loss, and independent q vs independent KV. **Counterexample:** D19's blanket statement that GQA must be designed before pretraining conflicts with this original conversion study. The correction does not imply any desired conversion is cheap or guaranteed.

<a id="a03-d13"></a>
## A03-D13 — D13 — Query-Key Normalization for Transformers [N; P]

Canonical cluster: **BR-A03-D13**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Alex Henry et al. [2010.04245v1](https://arxiv.org/html/2010.04245v1), 2020; [Findings of EMNLP 2020 official entry](https://aclanthology.org/2020.findings-emnlp.379/), pp. 4246–4253; [PDF](https://aclanthology.org/2020.findings-emnlp.379.pdf).

**Prior problem:** unrestricted query/key norms may arbitrarily saturate softmax in low-resource translation. **Solution:** normalize q and k per head and learn the logit scale, leaving values unnormalized by this operation. **Borrowed mechanisms:** cosine attention, learned temperature and initialization based on training sequence lengths. Supervision is bilingual sequence likelihood; other normalization choices also change in the main comparison.

**Evidence read:** §§2–4 and Appendix C discussion. The largest ablation drop is reported when learned scale g is removed; normalized logits in [-1,1] can be too diffuse. Main comparison also switches ScaleNorm to LayerNorm; do not attribute the entire average BLEU gain to q/k directions alone. Tables were not fully numerically extracted, and authors call the proposed explanation conjectural.

**Distinguishes:** geometry/direction vs scale vs training saturation, not content compression. **Cost/transfer:** tiny added scale parameter but new training/retuning requirements; low-resource translation is not long-delay exact recall. Normalization without scale is an essential negative control.

<a id="a03-d14"></a>
## A03-D14 — D14 — Alignment Attention by Matching Key and Query Distributions [N; P]

Canonical cluster: **BR-A03-D14**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Shujian Zhang, Xinjie Fan, Huangjie Zheng, Korawat Tanwisuth, Mingyuan Zhou. [2110.12567v1](https://arxiv.org/html/2110.12567v1), 2021-10-25; [PDF](https://arxiv.org/pdf/2110.12567v1). Official Atom says NeurIPS 2021; [official proceedings PDF search result](https://proceedings.neurips.cc/paper/2021/file/6fd6b030c6afec018415662d0db43f9d-Paper.pdf) not fully read.

**Prior problem:** learned q/k projections may induce poorly matched distributions. **Solution:** add unsupervised within-head distribution alignment to existing attention. **Borrowed mechanisms:** adversarial discriminator with gradient reversal, entropy-regularized optimal transport/Sinkhorn, or bidirectional conditional transport. Task objectives coexist with alignment loss; the model does not receive gold dynamic read/write associations through this loss.

**Evidence read:** §2.3 methods and selected experimental description. **Our inference/counterexample:** identical marginal q/k distributions can coexist with a permutation of semantic bindings. Marginal alignment is therefore not the same as D02's read/write consistency, shared q/k weights, or correct paired addressing.

**Distinguishes:** distribution mismatch as a trainable interface problem vs absence of target information. **Cost/failure:** discriminator/transport and alignment coefficient affect training; results on language understanding/VQA do not establish causally deployed memory access. Need collapse, paired-matching and alternative normalization controls.

<a id="a03-d15"></a>
## A03-D15 — D15 — Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free [N; P]

Canonical cluster: **BR-A03-D15**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Zihan Qiu et al. [2505.06708v1](https://arxiv.org/html/2505.06708v1), 2025-05-10; [PDF](https://arxiv.org/pdf/2505.06708v1). Preprint identity verified; NeurIPS 2025 oral is a search/author-repository pointer, not independently venue-certified in this record.

**Prior problem:** gating benefits are commonly entangled with routing, head design and other architectural changes. **Solution:** systematically compare gate positions and forms, finding head-specific query-dependent sigmoid gating after attention effective in the tested models. **Borrowed mechanisms:** multiplicative gates, sparsity and nonlinear value/output composition, standard language-model training.

**Evidence read:** §§1–2.2, Table 1 and §3.2.1, selected appendix discussion. Gates after q/k, v, attention output and final projection are distinct variants. Gains can persist in a single-expert configuration, a direct warning against attributing all benefit to expert routing. Sparse output gating can modulate consumption without changing which keys were matched.

**Distinguishes:** address selection vs returned content magnitude/nonlinearity; more heads vs head-specific gates. **Cost/failure:** elementwise gating may add appreciable projection parameters; headwise controls are smaller. Full matched budgets, sink metrics and long-context results need remaining original reading. No proof that low attention mass or a zero gate means missing content.

<a id="a03-d16"></a>
## A03-D16 — D16 — AsymKV: Enabling 1-Bit Quantization of KV Cache with Layer-Wise Asymmetric Quantization Configurations [N; M]

Canonical cluster: **BR-A03-D16**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Qian Tao, Wenyuan Yu, Jingren Zhou. [COLING 2025 official entry](https://aclanthology.org/2025.coling-main.158/), pp. 2316–2328; [PDF](https://aclanthology.org/2025.coling-main.158.pdf). Proceedings version is authoritative here; arXiv 2410.13212 is a related reference not independently read.

**Prior problem:** equal key/value quantization settings ignore unequal output sensitivity. **Solution:** use layerwise asymmetric bit configurations to protect the more sensitive key side. **Borrowed mechanisms:** activation/cache quantization and attention-output error analysis; exact calibration/training method is unread.

**Evidence:** official abstract/metadata only; authors report up to 75% decoder layers at one bit under their tested settings, not an all-layer/all-model guarantee. **Distinguishes:** precision errors in logits vs values. **Important non-equivalence:** its greater key-quantization sensitivity does not contradict D03's local-key merging observation or D19's key-feature redundancy; error operators differ. This is a second work named AsymKV, not another version of D03.

<a id="a03-d17"></a>
## A03-D17 — D17 — Low-Rank Key Value Attention [N; P]

Canonical cluster: **BR-A03-D17**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** James O'Neill, Robert Clancy, Mariia Matskevichus, Fergal Reid. Initially fetched [2601.11471v1](https://arxiv.org/html/2601.11471v1), 2026-01-16; official Atom exposed [v3](https://arxiv.org/html/2601.11471v3), 2026-04-07, subsequently fetched for updated methods/analysis. [v3 PDF](https://arxiv.org/pdf/2601.11471v3). Same work, not two entries. Venue unverified; the keyword “ICML” is not acceptance.

**Prior problem:** complete KV sharing can remove useful head differences while independent caches duplicate structure. **Solution:** use a shared dense KV component plus cached head-specific low-rank residuals. **Borrowed mechanisms:** low-rank additive factorization, jointly trained projections, operator-space head-diversity analysis using Wq Wkᵀ and centered Gram matrices. This is activation/cached-feature design, not merely a LoRA weight adapter.

**Evidence:** v1 methods/§6.3 targeted; v3 §3 and §4.3 targeted passages and appendix headings. Author analysis finds query specialization can partly compensate for shared keys; raw K-weight similarity alone misses this. Rank, query freedom and total state remain different axes. Version v3 clarifies fewer training steps vs per-step speedup.

**Source cautions:** v3 introduction says 2.6 GB exceeds 5 GB, an obvious arithmetic contradiction; do not inherit this motivation. v1 and v3 have different headline scales and analysis metrics, so do not splice their numbers. **Distinguishes:** independent query operators vs distinct cached KV, with finite residual rank. Full cost/position-compatibility validation and causal binding controls remain unread.

<a id="a03-d18"></a>
## A03-D18 — D18 — DynaCalKV: Key-Value Cache Compression via Head Grouping and Adaptive Rank Allocation [N; P]

Canonical cluster: **BR-A03-D18**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Tan T. Nguyen and Quan V. Dang. [2607.24331v1](https://arxiv.org/html/2607.24331v1), 2026-07-27; [PDF](https://arxiv.org/pdf/2607.24331v1). Preprint; venue unverified.

**Prior problem:** fixed head groups/rank budgets ignore nonuniform redundancy, and K/V need different approximations. **Solution:** cluster key heads by centered kernel alignment and adapt group ranks while separately calibrating value factorization. **Borrowed mechanisms:** SVD, Fisher-based layer allocation, CKA clustering, greedy budget adjustment and alternating closed-form least squares for values. Calibration uses WikiText-2; the target model need not be fully retrained.

**Evidence read:** §§III-B–D and §IV setup/limitations/LongBench discussion. All long-context methods nearly fail on SmolLM2, so authors omit that uninformative comparison. Long-context degradation is substantially worse on the tested GQA Llama than the MHA Qwen host; this is not a same-model causal test of GQA itself because host architecture and pretraining differ.

**Distinguishes:** compressible key-head redundancy vs already-shared head overcompression; calibration vs end-to-end adaptation. **Cost/failure:** offline calibration, factors and actual compressed cache/parameter budgets are distinct; performance tables are not all fully extracted. Not evidence that CKA predicts semantic binding or exact-memory survival.

<a id="a03-d19"></a>
## A03-D19 — D19 — Thin Keys, Full Values: Reducing KV Cache via Low-Dimensional Attention Selection [N; P]

Canonical cluster: **BR-A03-D19**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Hengshuai Yao, Xing Chen, Ahmed Murtadha, Guan Wang (official Atom; HTML extraction omits Chen). [2603.04427v3](https://arxiv.org/html/2603.04427v3), 2026-03-18; [v3 abstract/history](https://arxiv.org/abs/2603.04427v3), [PDF](https://arxiv.org/pdf/2603.04427v3). Atom latest v4 is 2026-03-28; v4 **not read**, do not upgrade v3 results. Preprint, venue not verified.

**Prior problem:** equal q/k/v feature widths may overallocate selection dimensions. **Solution:** factor key projections and absorb the complementary transform into query projections while retaining full values, optionally adapting q/k only. **Borrowed mechanisms:** truncated SVD, low-dimensional selection, parameter-restricted fine-tuning; from-scratch and post-training settings both appear.

**Evidence read:** §§2.1–2.3, §3.1/3.4, §§8.1–8.4, §6 limitations, selected §11. The source compares positional copy vs randomized content lookup; it also uses identically fine-tuned uncompressed controls, and exposes greater reasoning sensitivity and data-domain-dependent repair.

**Our cautions:** §2.3 writes exact score equality after Wk≈AB, but truncation is approximate unless discarded directions are immaterial. Johnson–Lindenstrauss distance preservation needs distortion/margin/query-set assumptions; it is not a universal log-N guarantee for all future query rankings. The no-GQA-conversion statement is contradicted by D12. Rotation/position transformations and logit scale must be checked before transferring algebra to an actual implementation.

**Distinguishes:** selection width vs value width vs interface adaptation; frozen failure vs recoverable reader mismatch. Savings in key cache are not equal to total KV savings, and LM perplexity is not exact-string retrieval.

<a id="a03-d20"></a>
## A03-D20 — D20 — How Linear Attention Remembers [N; P]

Canonical cluster: **BR-A03-D20**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Kichang Lee, JaeYeon Park, Songkuk Kim, JeongGil Ko. [2609.33093v1](https://arxiv.org/html/2609.33093v1), 2026-09-27; [PDF](https://arxiv.org/pdf/2609.33093v1). Preprint; venue not verified.

**Prior problem:** performance/probes do not identify how pretrained recurrent states actually write, retain and read facts. **Solution:** combine a recurrent contribution decomposition with donor-write, pre-query state and query-output interventions in pretrained GLA/GDN. **Borrowed mechanisms:** causal activation patching, content-consistent donor swaps, norm-matched controls, development/confirmation splits and source-cluster uncertainty. No additional fine-tuning.

**Evidence read:** original §§2.3–4.2, discussion/limitations; targeted appendix prose-pilot conclusion. Selective multi-fact editing coexists with nonadditive/cross-fact coupling. Holding sequence length fixed while varying fact load separates load from elapsed distance. In tested hybrids the immediate recalled identity lies mostly in full-attention KV, but recurrent contributions to earlier query/KV formation are not excluded.

**Critical boundary:** query-time **output** mediation is not an isolated intervention on q formation. Four-choice conditional-likelihood recall differs from free generation; the prose pilot fails a competence prerequisite and receives no downstream causal analysis. **Distinguishes:** write loss vs retention vs deployed read pathway, and nominal “independent slots” vs interacting support. Full appendix/artifact audit and broader relational tasks remain open.

<a id="a03-d21"></a>
## A03-D21 — D21 — GateSight: Recurrent Memory Anticipates Attention Memory for Query-Agnostic KV Eviction in Hybrid LLMs [N; P]

Canonical cluster: **BR-A03-D21**. [Carrying source record](../01_discovery/A03/WORKS_AND_PROBLEMS.md).

**Identity:** Junjie Li, Jiong Lou, Jie Li. [2610.14754v1](https://arxiv.org/html/2610.14754v1), 2026-10-10; [PDF](https://arxiv.org/pdf/2610.14754v1). Title/prefix corrected from official Atom; preprint, venue unverified.

**Prior problem:** before future questions arrive, how can a hybrid model decide which full-attention entries to retain? **Solution:** predict future KV output influence from recurrent write/decay/value-magnitude signals using per-head small networks and a gate-derived layer budget. **Borrowed mechanisms:** rollout-generated influence targets, exact local leave-one-out formulas with other variables fixed, ridge vs nonlinear predictors, cache compaction. Training uses generic documents and sampled model continuations; serving inputs do not include the later question.

**Evidence read:** §§2–4 targeted and experiment/cost descriptions. Their utility is ungated layer-output change over model continuations, not answer-specific causal correctness. The nonlinear model improves high-utility-tail recall despite slightly lower global rank correlation, warning against one scalar diagnostic. The second host's estimator is retrained with the same recipe, not transferred unchanged.

**Distinguishes:** useful control/selection signals in recurrent computation vs the recurrent state directly storing the final answer. Thus it need not contradict D20. **Cost/failure:** offline labeling/training, host-specific estimators and physical release count; current-query-agnostic is not future-distribution-invariant. It retains token KV, so this is a finite-cache comparator, not a closed-state recovery guarantee.

<a id="a04-r01"></a>
## A04-R01 — A04-R01 / previous N01 — Causal Mediation Analysis for Interpreting Neural NLP: The Case of Gender Bias

Canonical cluster: **BR-A04-R01**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Jesse Vig et al.; [arXiv:2004.12265v2](https://arxiv.org/abs/2004.12265v2), 2020-11-22; expanded preprint. A differently titled NeurIPS counterpart was noted previously; this pass does not equate its full text with v2. [PDF](https://arxiv.org/pdf/2004.12265v2).
- **Prior problem → one-sentence solution:** behavior-only and structure-only analyses do not specify information flow; apply causal mediation interventions to neurons/heads to separate direct and indirect effects of gender changes.
- **Borrowed AI mechanism / learning:** frozen pretrained Transformers, paired inputs, internal component interventions; gender-bias datasets, not a trained memory reader. Unit: text input → head/neuron activations → output bias score.
- **Evidence:** A, official abstract plus Atom metadata. The author reports sparse and synergistic/amplifying/suppressing effects; no equations or individual numerical claims are newly verified here.
- **Distinguishes / decision:** fixed additive component importance versus context-conditioned mediator effects. Use as the original neural-language mediation anchor; do not assume its treatment, output scale, or empirical near-additivity transfers to byte memory.

<a id="a04-r02"></a>
## A04-R02 — A04-R02 / previous N02 — The Hydra Effect: Emergent Self-repair in Language Model Computations

Canonical cluster: **BR-A04-R02**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Thomas McGrath, Matthew Rahtz, Janos Kramar, Vladimir Mikulik, Shane Legg; [2307.15771v1](https://arxiv.org/abs/2307.15771v1), 2023-07-28; public preprint, conference status not established. [PDF](https://arxiv.org/pdf/2307.15771v1).
- **Problem → solution:** a small ablation effect may hide downstream compensation; measure how downstream computations respond to layer ablations during factual recall.
- **Mechanism / learning:** fixed pretrained-model forward computations, attention-layer ablation and late MLP counterbalancing; not retraining-based recovery. The abstract reports the effect even without dropout training.
- **Evidence:** A only in this round. Exact compensation definitions, models, fractions and appendices remain unread.
- **Distinguishes / decision:** never-used component versus active component whose removal triggers compensation. Log downstream changes and compare free continuation with explicitly constrained-path effects; static duplicate storage and dynamic compensation are not interchangeable explanations.

<a id="a04-r03"></a>
## A04-R03 — A04-R03 / previous N03 — Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models

Canonical cluster: **BR-A04-R03**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Peter Hase, Mohit Bansal, Been Kim, Asma Ghandeharioun; [2301.04213v2](https://arxiv.org/abs/2301.04213v2), 2023-10-16; official arXiv metadata says NeurIPS 2023 Spotlight. [PDF](https://arxiv.org/pdf/2301.04213v2).
- **Problem → solution:** causal localization is often used to choose an editing location; directly compare localization scores with editing success across layers and editing formulations.
- **Mechanism / learning:** representation denoising versus weight editing; editing changes the system, unlike fixed-weight inference patching. Granularity: factual prompts, MLP layers, stored fact outputs.
- **Evidence:** A this round; prior audit's selected §§4–8 findings are inherited, not re-read. The abstract itself includes the exception that one editing formulation does relate to localization, while layer choice predicts performance better.
- **Distinguishes / decision:** information passing through an interface versus that interface being the best repair target. A successful readout repair cannot retrospectively certify that the old readout was the unique cause of failure.

<a id="a04-r04"></a>
## A04-R04 — A04-R04 / previous N04 — ERASER: A Benchmark to Evaluate Rationalized NLP Models

Canonical cluster: **BR-A04-R04**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Jay DeYoung et al.; [ACL 2020 official record](https://aclanthology.org/2020.acl-main.408/), pp. 4443–4458, DOI 10.18653/v1/2020.acl-main.408. [Version-of-record PDF](https://aclanthology.org/2020.acl-main.408.pdf).
- **Problem → solution:** rationale evaluation uses incomparable tasks and definitions; assemble human supporting rationales and measures for human alignment and prediction faithfulness.
- **Mechanism / learning:** token/sentence rationale extraction, keep-only and removal comparisons, confidence/behavior scoring. Additional rationale supervision and access must be accounted for separately from the deployed reader.
- **Evidence:** A plus official bibliographic record; primary PDF formulas not read this round. The precise sign/label conventions must be verified before implementation.
- **Distinguishes / decision:** evidence plausibility/human agreement versus evidence actually influencing the model. Pair with R05 rather than importing rationale deletion as an unquestioned causal gold standard.

<a id="a04-r05"></a>
## A04-R05 — A04-R05 / previous N05 — Goodhart's Law Applies to NLP's Explanation Benchmarks

Canonical cluster: **BR-A04-R05**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Jennifer Hsia, Danish Pruthi, Aarti Singh, Zachary C. Lipton; [2308.14272v1](https://arxiv.org/abs/2308.14272v1), 2023-08-28; preprint, venue not established. [HTML](https://arxiv.org/html/2308.14272v1), [PDF](https://arxiv.org/pdf/2308.14272v1).
- **Problem → solution:** explanation scores may improve without more faithful explanations; construct wrappers exploiting distinguishable rationale/complement distributions and a label-encoding attack on EVAL-X.
- **Mechanism / learning:** saliency-selected input subsets, out-of-support detection, confidence manipulation, evaluator retraining. These are counterexamples to the instrument, not better memory architectures.
- **Evidence:** A freshly retrieved; previous audit's selected §§1–4 is reusable as P-prior, not FULL. Official abstract confirms predictions/explanations on in-distribution test inputs can remain unchanged while scores inflate.
- **Distinguishes / decision:** genuine content dependence versus recognizing the evaluation intervention and altering confidence. Add untouched-input equivalence checks, label-leakage controls, and held-out intervention families; two deletion metrics do not automatically close the loophole.

<a id="a04-r06"></a>
## A04-R06 — A04-R06 / previous N06 — Evaluating the Faithfulness of Importance Measures in NLP by Recursively Masking Allegedly Important Tokens and Retraining

Canonical cluster: **BR-A04-R06**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Andreas Madsen, Nicholas Meade, Vaibhav Adlakha, Siva Reddy; [2110.08412v3](https://arxiv.org/abs/2110.08412v3), 2022-10-31; preprint identity verified, formal venue not checked. [PDF](https://arxiv.org/pdf/2110.08412v3).
- **Problem → solution:** masking importance scores confounds redundancy and distribution shift; recursively mask selected tokens, retrain, and compare masking curves with random-token baselines.
- **Mechanism / learning:** repeated model training and iterative importance updates; relative area between curves summarizes the result. Unit: token subsets → retrained task model → task performance.
- **Evidence:** A only; abstract reports four measures, eight datasets, LSTM-attention and RoBERTa, with model/task-dependent conclusions.
- **Distinguishes / decision:** features needed by the original deployed model versus information a newly trained model can replace. Relevant if considering retrained no-memory controls, but not a substitute for fixed-weight dependence.

<a id="a04-r07"></a>
## A04-R07 — A04-R07 / previous N07 — RelP: Faithful and Efficient Circuit Discovery in Language Models via Relevance Patching

Canonical cluster: **BR-A04-R07**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Farnoush Rezaei Jafari, Oliver Eberle, Ashkan Khakzar, Neel Nanda; [2508.21258v2](https://arxiv.org/abs/2508.21258v2), 2025-10-30; venue unresolved. [PDF](https://arxiv.org/pdf/2508.21258v2).
- **Problem → solution:** exact patching is costly and local-gradient approximations fail in nonlinear models; replace attribution-patching gradients with layer-wise relevance propagation coefficients.
- **Mechanism / learning:** relevance redistribution with chosen propagation rules; two forward passes and one backward pass per abstract, not a full evaluation cost account. Tested on residual/MLP outputs and sparse-feature circuits.
- **Evidence:** A; detailed controls and all model/task results unread. The headline correlation improvement is an author report and is not used as a cross-method ranking here.
- **Distinguishes / decision:** approximation error relative to exact patch scores versus invalidity of the exact patch estimand itself. Only prioritize after trustworthy exact controls become a demonstrated cost bottleneck.

<a id="a04-r08"></a>
## A04-R08 — A04-R08 / previous N08 — The Curse of Multiple Mediators: Hidden Interaction Effects in Activation Patching

Canonical cluster: **BR-A04-R08**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Sankaran Vaidyanathan, David Arbour, Aaron Mueller, Scott Niekum, David Jensen; [2606.27510v1](https://arxiv.org/abs/2606.27510v1), 2026-06-25; preprint, venue unverified. [HTML](https://arxiv.org/html/2606.27510v1), [PDF](https://arxiv.org/pdf/2606.27510v1).
- **Problem → solution:** single-component rankings and sum-of-effects predictions miss conditional mechanisms; explicitly decompose noising/denoising and grouped intervention effects into context-dependent and cross-component interaction terms.
- **Mechanism / learning:** fixed-model exact patching, causal mediation algebra, smooth downstream approximations, grouped IOI interventions. §3.2's approximation requires twice differentiability; the finite-difference interaction itself does not.
- **Evidence:** P, §§2–5.3 and opening discussion selected this round; appendix proofs/full tables not read. §5.2: removing interaction from the ranking can miss context-specific heads; pairwise tests also miss effects visible against a whole name-mover group. §5.3 says independent functional modularity must not be assumed for arbitrary models.
- **Distinguishes / decision:** redundancy, conditional cooperation, and harmful countervailing paths. Preserve the four observable cells and actual recomputation contract before naming a quantity NIE/PIE. The paper's interpretation of “pure” effects as path-specific requires graph/structural assumptions; do not turn its terminology into a general guarantee of isolated memory-content causation.

<a id="a04-r09"></a>
## A04-R09 — A04-R09 / W0533 — Towards Best Practices of Activation Patching in Language Models: Metrics and Methods

Canonical cluster: **W0533**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Fred Zhang, Neel Nanda; [2309.16042v2](https://arxiv.org/abs/2309.16042v2), 2024-01-17; previous catalog/official metadata associates ICLR 2024, not freshly checked on the venue site. [HTML](https://arxiv.org/html/2309.16042v2), [PDF](https://arxiv.org/pdf/2309.16042v2).
- **Problem → solution:** patching choices yield incompatible localization; compare Gaussian noise, symmetric token replacement, output metrics and joint sliding-window versus single-layer patches.
- **Mechanism / learning:** frozen LM forward interventions; no extra learned reader. §6's answer-pair logit difference can control a generic “boost all names” direction that a single target logit does not.
- **Evidence:** P, §§5–6 this round plus targeted §3/4 excerpts; no full card. §5 explicitly treats windows as joint effects, not localization of the middle layer alone. §6 also warns that which input token is corrupted changes which information is traced.
- **Distinguishes / decision:** target value versus target identity/position and generic output-class boosts. Prefer legitimate token counterfactuals where suitable, but its claim of avoiding OOD is not proof that a hybrid of two natural internal states is jointly on-manifold.

<a id="a04-r10"></a>
## A04-R10 — A04-R10 / W0531 — RAVEL: Evaluating Interpretability Methods on Disentangling Language Model Representations

Canonical cluster: **W0531**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Jing Huang, Zhengxuan Wu, Christopher Potts, Mor Geva; [2402.17700v2](https://arxiv.org/abs/2402.17700v2), 2024-08-26; preprint verified, venue not reverified. [PDF](https://arxiv.org/pdf/2402.17700v2).
- **Problem → solution:** changing one concept can alter entangled attributes; evaluate interpreters with multiple causal criteria and learn multitask distributed alignments.
- **Mechanism / learning:** Multi-task Distributed Alignment Search (多任务分布式对齐搜索：用多个属性的干预目标学习表征子空间), frozen Llama2-7B, entity/attribute representations and supervised interventions.
- **Evidence:** A; detailed train/test entity separation and non-target criteria remain unread, as in the old audit.
- **Distinguishes / decision:** ability to force a target answer versus selective target change with unrelated attributes preserved. It evaluates an intervention method, not automatically the unmodified model's natural use.

<a id="a04-r11"></a>
## A04-R11 — A04-R11 / W0373 — Naturalistic Causal Probing for Morpho-Syntax

Canonical cluster: **W0373**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Afra Amini, Tiago Pimentel, Clara Meister, Ryan Cotterell; [TACL 2023 official record](https://aclanthology.org/2023.tacl-1.23/), volume 11, pp.384–403, DOI 10.1162/tacl_a_00554. Existing arXiv alias 2205.07043v2; version-of-record is the recommended next read. [PDF](https://aclanthology.org/2023.tacl-1.23.pdf).
- **Problem → solution:** arbitrary hidden interventions can misrepresent linguistic causation; intervene on naturalistic sentence morphosyntax while retaining the remaining sentence.
- **Mechanism / learning:** input-level counterfactual construction, Spanish gender/number, multilingual BERT/RoBERTa/GPT-2 contextual representations; no compressed memory or source revisit.
- **Evidence:** A, official abstract and identity; no full primary reading.
- **Distinguishes / decision:** a naturally recomputed input effect versus arbitrary hidden-state perturbation. “Naturalistic” does not establish all downstream hidden hybrids are valid or all semantic attributes remain fixed.

<a id="a04-r12"></a>
## A04-R12 — A04-R12 / W0370 — Information-Theoretic Probing with Minimum Description Length

Canonical cluster: **W0370**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Elena Voita, Ivan Titov; [EMNLP 2020 record](https://aclanthology.org/2020.emnlp-main.14/), pp.183–196, DOI 10.18653/v1/2020.emnlp-main.14. [PDF](https://aclanthology.org/2020.emnlp-main.14.pdf).
- **Problem → solution:** similar probe accuracy can hide large differences in learning effort; measure label description length using variational and online coding.
- **Mechanism / learning:** supervised probe training, coding/model complexity and data-efficiency measures. Input: fixed representations; output/supervision: linguistic labels. Query/label permissions exceed an untrained native readout unless separately matched.
- **Evidence:** A plus official BibTeX; no full card.
- **Distinguishes / decision:** recoverable information requiring expensive supervision versus easily accessible information. A useful bridge between representational presence and reader learnability, not a causal-use certificate.

<a id="a04-n01"></a>
## A04-N01 — A04-N01 — Transformer Circuit Faithfulness Metrics are not Robust

Canonical cluster: **BR-A04-N01**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Joseph Miller, Bilal Chughtai, William Saunders; [2407.08734v1](https://arxiv.org/abs/2407.08734v1), 2024-07-11; official arXiv comment says CoLM 2024 conference paper. [HTML](https://arxiv.org/html/2407.08734v1), [PDF](https://arxiv.org/pdf/2407.08734v1).
- **Problem → solution:** identical circuits obtain incompatible faithfulness scores; enumerate and vary graph granularity, node/edge/branch, replacement value, positions, direction, and circuit/complement.
- **Mechanism / learning:** exact ablations of existing language-model circuits and compiled Tracr controls; no new memory learner. **P:** §§3–6, without appendices or complete tables.
- **Concrete falsification:** §5's positional encoding is constant across resampled inputs, so resampling cannot remove it; zeroing can. A discovery algorithm can perfectly recover the circuit appropriate to one definition while appearing wrong against the other's reference. §4 distinguishes ratio-of-means from mean-of-ratios and exposes extreme per-example scores.
- **Distinguishes / decision:** unnecessary content path versus invariant information left intact by the chosen donor distribution. Specify the information varied and preserved; complement ablation and circuit restoration do not necessarily enforce the same path restrictions. This is a substantive counterexample, not merely “try more ablations.”

<a id="a04-n02"></a>
## A04-N02 — A04-N02 — Many Circuits, One Mechanism: Input Variation and Evaluation Granularity in Circuit Discovery

Canonical cluster: **BR-A04-N02**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Alireza Bayat Makou, Jingcheng Niu, Subhabrata Dutta, Iryna Gurevych; [2606.06267v2](https://arxiv.org/abs/2606.06267v2), 2026-08-26; official arXiv journal reference says TMLR 2026, publisher/forum not checked. [v2 PDF](https://arxiv.org/pdf/2606.06267v2). Search surfaced the shorter title “Input Variation and Evaluation Granularity in Circuit Discovery”; one work, not two.
- **Problem → solution:** different discovered edge sets are mistaken for different computations; vary token frequency with task fixed and compare structure, functional transfer, and interchange interventions.
- **Mechanism / learning:** ACDC pruning, fixed Pythia models, frequency bands, copying, cross-condition circuit transfer. No source revisit. **P:** rendered v1-route introduction/§2.1 and A: locked v2 abstract/metadata. The HTML route's title matches the later title; version-sensitive quantitative claims use the v2 abstract only.
- **Evidence/limits:** v2 reports 75 circuits, five scales; ≥99% recovery from the shared core is qualified to models **above 70M**, and adds a smaller subject–verb-agreement replication. It explicitly does not test position/feature-level specialization. All full tables/positive sensitivity controls remain unread.
- **Distinguishes / decision:** representation/route change versus genuine functional specialization. Require repeated extractions and cross-condition functional tests before interpreting changed circuit overlap as loss or gain of memory use.

<a id="a04-n03"></a>
## A04-N03 — A04-N03 — Mechanistic Interpretability as Statistical Estimation: A Variance Analysis

Canonical cluster: **BR-A04-N03**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Maxime Méloux, François Portet, Maxime Peyrard; [2510.00845v4](https://arxiv.org/abs/2510.00845v4), 2026-05-28; public preprint, venue not established. Earlier titles add “of EAP-IG”; do not count that as a second work. [HTML](https://arxiv.org/html/2510.00845v4), [PDF](https://arxiv.org/pdf/2510.00845v4).
- **Problem → solution:** a single extracted circuit hides sample and methodological variability; decompose exact per-input mediation, approximation noise, aggregation, and graph selection, with bootstrap/stability evaluation.
- **Mechanism / learning:** exact interventions, gradient/integrated-gradient approximations, resampling and pruning on GPT-2 Small/Llama-3.2-1B variants. **P:** §§1–6 selected; appendices/full tables unread.
- **Important limit:** §6.1 explicitly separates empirical instability from theoretical non-identifiability. §5.1 says exact computations are restricted to IOI, while its Figure 2 caption and §6.3 also mention Greater-Than; this internal scope inconsistency must be resolved before quoting exact-task coverage. The suggested Jaccard 0.8 / 100-bootstrap threshold is tentative, not a transferable gate.
- **Distinguishes / decision:** finite-sample/approximation instability versus truly nonunique mechanisms. Report structural and behavioral stability separately, on independently held-out examples.

<a id="a04-n04"></a>
## A04-N04 — A04-N04 — Towards Faithful Natural Language Explanations: A Study Using Activation Patching in Large Language Models

Canonical cluster: **BR-A04-N04**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Wei Jie Yeo, Ranjan Satapathy, Erik Cambria; [EMNLP 2025 official record](https://aclanthology.org/2025.emnlp-main.529/), pp.10425–10447, DOI 10.18653/v1/2025.emnlp-main.529. [Formal PDF](https://aclanthology.org/2025.emnlp-main.529.pdf). arXiv alias 2410.14155v2, 2024-11-01, still says “under review”; that stale comment does not override the official proceedings.
- **Problem → solution:** persuasive explanations can be unfaithful and perturbation tests can be OOD; compare activation-patching causal-attribution profiles for an explanation and its answer.
- **Mechanism / learning:** causal mediation/patching, explanation generation, pretrained/alignment-tuned 2B–27B models. **A** only, including official bibliography; body unread.
- **Distinguishes / decision:** shared attribution pattern versus explanation text merely sounding supportive. Positive candidate for triangulation, **not a settled solution**: agreement of two patch-based profiles inherits patch-background and interaction assumptions and does not independently verify target-content correctness.

<a id="a04-n05"></a>
## A04-N05 — A04-N05 — Right for the Wrong Reasons: Diagnosing Syntactic Heuristics in Natural Language Inference

Canonical cluster: **BR-A04-N05**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** R. Thomas McCoy, Ellie Pavlick, Tal Linzen; [ACL 2019 official record](https://aclanthology.org/P19-1334/), pp.3428–3448, DOI 10.18653/v1/P19-1334. [PDF](https://aclanthology.org/P19-1334.pdf).
- **Problem → solution:** good benchmark accuracy may come from fallible heuristics; construct HANS examples breaking lexical-overlap, subsequence, and constituent heuristics.
- **Mechanism / learning:** controlled natural-language templates evaluated against pretrained/fine-tuned NLI systems; no internal patching. **A**, official abstract and bibliography; detailed template splits unread.
- **Distinguishes / decision:** genuine relational/semantic dependence versus shortcut accuracy. Borrow known-answer counterexamples with unchanged surface cues; do not treat HANS failure as proof of a particular internal location or as direct evidence about byte memory.

<a id="a04-n06"></a>
## A04-N06 — A04-N06 — Causal Scrubbing: a method for rigorously testing interpretability hypotheses

Canonical cluster: **BR-A04-N06**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Redwood Research original author-posted protocol, 2022; [primary public article](https://www.alignmentforum.org/posts/JvZhhzycHu2Yd57RN/causal-scrubbing-a-method-for-rigorously-testing). This is a research post/sequence, not a verified peer-reviewed proceedings paper; exact revision hash unavailable.
- **Problem → solution:** ad-hoc ablations do not rigorously test a stated interpretation; derive behavior-preserving conditional resampling interventions from a graph correspondence and hypothesized invariances.
- **Mechanism / learning:** computational-graph rewriting, recursive conditional resampling, induction/parenthesis examples. **P:** returned introduction, setup, and opening §3; the extraction ends during §3.1, so later algorithm details, limitations and sequence appendices are not read.
- **Distinguishes / decision:** “this feature influences output” versus “these proposed invariances explain the behavior.” The primary setup expressly says its equivalence-class test is weaker than full representational correspondence and cannot eliminate all wrong hypotheses. Recursive path enumeration can be costly; do not promise exhaustive tests on a full recurrent LM.

<a id="a04-n07"></a>
## A04-N07 — A04-N07 — FaithEval: Can Your Language Model Stay Faithful to Context, Even If “The Moon is Made of Marshmallows”

Canonical cluster: **BR-A04-N07**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Yifei Ming, Senthil Purushwalkam, Shrey Pandit, Zixuan Ke, Xuan-Phi Nguyen, Caiming Xiong, Shafiq Joty; [2410.03727v3](https://arxiv.org/abs/2410.03727v3), 2025-04-24. Official arXiv comment reports ICLR 2025 publication; forum not independently checked. [HTML](https://arxiv.org/html/2410.03727v3), [PDF](https://arxiv.org/pdf/2410.03727v3).
- **Problem → solution:** ordinary QA misses unsupported, inconsistent, and counterfactual context behavior; build separate controlled context tasks with construction and validation procedures.
- **Mechanism / learning:** LLM-generated minimally modified contexts/distractors, separate judging and task-dependent human validation, deterministic instruction-following evaluation. **P:** §3.1–3.3; appendices/results not fully read.
- **Concrete controls/limits:** “unknown” and “conflict” are explicitly instructed responses; counterfactual science contexts are fabricated to support an alternative option. Human validation is not uniform: inconsistent examples are fully human filtered; counterfactual validation uses string matching justified by a pilot. Accuracy accepts mention of an answer, so it is not whole-response truth or entailment verification.
- **Distinguishes / decision:** contextual compliance versus world-truth accuracy. Following a false stipulated context can be correct for this task and wrong for an open-world truth task: declare authority/answerability policy first, not after seeing results.

<a id="a04-n08"></a>
## A04-N08 — A04-N08 — ClashEval: Quantifying the tug-of-war between an LLM's internal prior and external evidence

Canonical cluster: **BR-A04-N08**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Kevin Wu, Eric Wu, James Zou; [2404.10198v3](https://arxiv.org/abs/2404.10198v3), 2025-02-07; preprint, formal venue not established. Earlier title: “How faithful are RAG models? Quantifying the tug-of-war between RAG and LLMs' internal prior.” [HTML](https://arxiv.org/html/2404.10198v3), [PDF](https://arxiv.org/pdf/2404.10198v3).
- **Problem → solution:** a model can trivially pass “reject bad context” by ignoring all context; pair prior-only and contextual answers, testing both correct-prior/wrong-context and wrong-prior/correct-context cases.
- **Mechanism / learning:** fixed inference models, numerical multipliers/categorical perturbations, prior token probabilities, standard/strict/loose prompts; six domains, 1,294 questions in the selected methods. **P:** §§1,3–4.4; full tables/appendices unread.
- **Controls/limits:** quantify prior bias and context bias separately; multi-document distractor addition changes length/evidence quantity, not an isolated memory mechanism. Context construction involves GPT-4o; source content includes some nonpublic medical pages, so do not imply unrestricted full-dataset access or download those pages.
- **Distinguishes / decision:** calibrated evidence arbitration versus blanket credulity or blanket disregard. Pair “believe correct evidence” and “reject false evidence” rather than treating answer flips as universally desirable.

<a id="a04-n09"></a>
## A04-N09 — A04-N09 — Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small

Canonical cluster: **BR-A04-N09**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Kevin Wang, Alexandre Variengien, Arthur Conmy, Buck Shlegeris, Jacob Steinhardt; [2211.00593v1](https://arxiv.org/abs/2211.00593v1), 2022-11-01; original preprint verified, conference identity not checked this round. [PDF](https://arxiv.org/pdf/2211.00593v1).
- **Problem → solution:** broad low-resolution descriptions do not explain an end-to-end natural behavior; characterize an IOI head circuit and test faithfulness, completeness and minimality.
- **Mechanism / learning:** fixed GPT-2 Small, causal interventions, task-template/name manipulations, 26 heads in seven classes per abstract. **A**; its grouped-backup discovery is referenced by selected R08 body, not newly verified from this original paper's full protocol.
- **Distinguishes / decision:** sufficient circuit behavior versus completeness of the original computation. Read original grouped/backup tests before implementing an exclusion-of-redundancy claim; N01/N02 show why copying a reported faithfulness score alone is insufficient.

<a id="a04-n10"></a>
## A04-N10 — A04-N10 — Everything, Everywhere, All at Once: Is Mechanistic Interpretability Identifiable?

Canonical cluster: **BR-A04-N10**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Maxime Méloux, Silviu Maniu, François Portet, Maxime Peyrard; [2502.20914v1](https://arxiv.org/abs/2502.20914v1), 2025-02-28; official arXiv journal reference says ICLR 2025, venue forum not checked. [PDF](https://arxiv.org/pdf/2502.20914v1).
- **Problem → solution:** satisfying common explanation criteria may not uniquely identify a mechanism; enumerate circuits, interpretations, algorithms and subspace alignments for Boolean functions/small MLPs.
- **Mechanism / learning:** exhaustive toy-model explanation search and causal alignment, not a theorem that all full-scale LMs are uninterpretable. **A** only.
- **Distinguishes / decision:** a useful falsifiable/manipulable explanation versus a uniquely identified original algorithm. Preserve multiple compatible hypotheses when tests do not distinguish them; empirical instability alone does not establish the enumeration paper's identifiability result on another system.

<a id="a04-n11"></a>
## A04-N11 — A04-N11 — Hypothesis Testing the Circuit Hypothesis in LLMs

Canonical cluster: **BR-A04-N11**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Claudia Shi, Nicolas Beltran-Velez, Achille Nazaret, Carolina Zheng, Adrià Garriga-Alonso, Andrew Jesson, Maggie Makar, David M. Blei; [2410.13032v1](https://arxiv.org/abs/2410.13032v1), 2024-10-16; preprint verified, NeurIPS association in search not promoted to verified venue. [HTML](https://arxiv.org/html/2410.13032v1), [PDF](https://arxiv.org/pdf/2410.13032v1).
- **Problem → solution:** “small circuit” claims lack common statistical tests; formalize preservation/localization/minimality criteria and test six literature circuits, including hard-coded positives.
- **Mechanism / learning:** reference distributions and hypothesis tests over intervened circuit performance; circuitry software is an artifact, not installed or executed here. **A** only.
- **Distinguishes / decision:** interpretation passing a calibrated test versus simply having a large restoration score. Synthetic known-circuit positives validate some instrument behavior but do not prove sensitivity to nonlinear redundancy; exact null hypotheses and power remain missing reading questions.

<a id="a04-n12"></a>
## A04-N12 — A04-N12 — Certified Interventional Fidelity: Anytime-Valid, Adaptive Evaluation of Causal Claims in Mechanistic Interpretability

Canonical cluster: **BR-A04-N12**. [Carrying source record](../01_discovery/A04/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** Amir Asiaee; [UAI 2026 official PMLR record](https://proceedings.mlr.press/v337/asiaee26d.html), volume 337, pp.210–227, 17–21 August 2026. [Proceedings PDF](https://raw.githubusercontent.com/mlresearch/v337/main/assets/asiaee26d/asiaee26d.pdf).
- **Problem → solution:** repeatedly inspecting/adapting intervention evaluations undermines fixed-sample confidence claims; define a bounded-score causal estimand over input/intervention distributions and provide confidence intervals/sequences with adaptive sampling weights.
- **Mechanism / learning:** Hoeffding-style and variance-adaptive betting confidence sequences, bounded mixture importance weighting; MNIST abstractions and GPT-2 Small IOI applications. **A**, official abstract and full bibliography, PDF not read.
- **Distinguishes / decision:** stable population intervention effect versus sampling/optional-stopping artifact. High-priority 2026 protocol: it could change stopping rules and sampling, not merely add caveats. Certification is conditional on score bounds, sampling/support/weighting assumptions and a chosen intervention distribution; it cannot certify that the intervention isolates correct evidence.

<a id="ld-n01"></a>
## LD-N01 — LD-N01 = BIW-0096 — Lagging Inference Networks and Posterior Collapse in Variational Autoencoders

Canonical cluster: **BIW-0096**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [1901.05534v2](https://arxiv.org/abs/1901.05534v2), 2019-01-28; ICLR 2019 according to prior recovery/PDF identity. [Pinned HTML](https://arxiv.org/html/1901.05534v2). R + C: byte catalog BIW-0096 already marks selected-primary/recovery, no FULL card.
- **Prior problem:** the inference encoder may fail to track the generator's changing true posterior at the beginning, encouraging the decoder to ignore the latent variable.
- **One-sentence solution:** aggressively update the inference network before generator updates, with mutual-information-dependent control of the aggressive phase.
- **Borrowed AI mechanisms:** amortized variational inference, ELBO optimization, alternating/two-time-scale training, mutual-information monitoring; the schedule changes optimization rather than the memory architecture.
- **Evidence depth:** fresh A and HTML abstract/introduction; prior P covered §§2–4/6 selectively, not all appendix experiments. T/E in variational text/image models. No new FULL claim.
- **Units/visibility/controls:** observations → stochastic latent posterior → autoregressive observations; encoder has observed input during inference training. Compare aggressive inference with ordinary training and other collapse remedies; equal-step is not automatically equal-compute.
- **Distinguishing hypothesis:** delayed writer/inference learning versus a representation that is intrinsically insufficient. A deterministic compressor has no true variational posterior; transfer is an optimization analogy, not identity.

<a id="ld-n02"></a>
## LD-N02 — LD-N02 — Deeply-Supervised Nets

Canonical cluster: **BR-LD-N02**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [PMLR 38:562–570](https://proceedings.mlr.press/v38/lee15a.html), AISTATS 2015 final proceedings; [official PDF](https://proceedings.mlr.press/v38/lee15a.pdf); arXiv alias 1409.5185. R, absent from the two searched canonical catalogs.
- **Prior problem:** final-layer classification supervision provides indirect learning signals to intermediate layers and may leave them hard to optimize or insufficiently discriminative.
- **One-sentence solution:** add companion discriminative objectives at hidden layers alongside the output objective.
- **Borrowed AI mechanisms:** deep supervision, layer-local classifiers, stochastic optimization and attenuated/thresholded companion objectives; not an autoencoding loss.
- **Evidence depth:** fresh official A; recovered P on §§2.1–2.3/3.1, local strong-convex/common-optimum assumptions, not all proofs/tables. T/E in vision classification.
- **Units/visibility/cost:** images → hidden representations → class labels, with extra training heads and target labels available at intermediate layers; no query or source retrieval. Extra heads/backprop must be counted even if discarded at inference.
- **Distinguishing hypothesis:** poorly supervised intermediate feature formation versus insufficient reconstruction. Local theory is not a guarantee for arbitrary nonconvex byte models.

<a id="ld-n03"></a>
## LD-N03 — LD-N03 — Critical Learning Periods in Deep Networks / arXiv title: Critical Learning Periods in Deep Neural Networks

Canonical cluster: **BR-LD-N03**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [1711.08856v3](https://arxiv.org/abs/1711.08856v3), 2019-02-25; ICLR 2019 per prior recovery. R; title variant retained rather than split into works.
- **Prior problem:** a temporary early stimulus deficit can leave a persistent performance deficit after normal inputs are restored.
- **One-sentence solution:** study timed input deprivation and recovery, relating the trajectory to Fisher-information connectivity/plasticity.
- **Borrowed AI mechanisms:** staged data perturbation, representation/plasticity diagnostics, Fisher information; primarily an explanatory experiment, not a deployable memory module.
- **Evidence depth:** fresh A confirms recovery counterexample; recovered P on early blur, constant-learning-rate controls, Fisher interpretation; no FULL or independent irreversibility proof.
- **Controls/limits:** low-level visual degradation differs from flips/label permutations, which can recover. Onset, duration, network size and finite recovery horizon matter; “all early errors are irreversible” is contradicted.
- **Distinguishing hypothesis:** early path-dependent formation versus a reversible stage/interface disturbance. Requires timed continuation to establish causation locally.

<a id="ld-n04"></a>
## LD-N04 — LD-N04 — ForkMerge: Mitigating Negative Transfer in Auxiliary-Task Learning

Canonical cluster: **BR-LD-N04**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [2301.12618v3](https://arxiv.org/html/2301.12618v3), 2023-11-16; NeurIPS 2023, [official proceedings PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/60f9118a849e8e9a0c67e2a36ad80ebf-Paper-Conference.pdf). R.
- **Prior problem:** coordinating gradient conflicts may miss auxiliary-task negative transfer arising in validation/generalization rather than training descent.
- **One-sentence solution:** periodically fork branches with different task weights and merge them using target validation performance.
- **Borrowed AI mechanisms:** auxiliary-task learning, validation-driven task-weight search, parameter interpolation/branch merging; branch cost and validation-label permissions are part of the method.
- **Evidence depth:** fresh P, §3 definitions/§3.1–3.2 and Fig.2 caption. Fig.2 takes **one update from common intermediate parameters**, not independent full trajectories with all-history aligned gradients.
- **Controls/limits:** target Painting/Quickdraw in DomainNet, other domains auxiliary; L2 regularization contrast; task weight changes the fitted mixture. Validation transfer gain and training gradient cosine measure different objects.
- **Distinguishing hypothesis:** “aligned gradients imply no negative transfer” versus a generalization mismatch; not a proof that two aligned local objectives jointly cause the same compressed-content shortcut.

<a id="ld-n05"></a>
## LD-N05 — LD-N05 — Strategy Coopetition Explains the Emergence and Transience of In-Context Learning

Canonical cluster: **BR-LD-N05**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [2503.05631v2](https://arxiv.org/html/2503.05631v2), 2025-03-10; ICML 2025 venue association recovered, exact proceedings/arXiv version equivalence unverified. R.
- **Prior problem:** ICL can emerge and disappear; a binary “context versus weights” explanation hides the role of contextual constraints and shared circuitry.
- **One-sentence solution:** distinguish context-constrained in-weights learning from general ICL and trace their cooperating and competing subcircuits across training.
- **Borrowed AI mechanisms:** mechanistic circuit decomposition, evaluator contrasts, formation-time clamping, simplified dynamical models.
- **Evidence depth:** fresh P for Fig.1 and beginning; recovered P §§2–5; appendices not completed. Synthetic Omniglot two-layer attention-only model, not a general language-model result.
- **Controls/counterexample:** late hybrid still needs label clues in context; downstream circuit survives with a changed role; an eventually competing strategy can help the desired strategy form. MLP variants can show resurgence, cautioning against asymptotic universal claims.
- **Distinguishing hypothesis:** absent mechanism versus repurposed mechanism; bypass always harmful versus stage-dependent cooperation.

<a id="ld-n06"></a>
## LD-N06 — LD-N06 — How Language Models Develop In-Context Learning (body prefix: From Copying to Composition)

Canonical cluster: **BR-LD-N06**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [2610.19113v1](https://arxiv.org/html/2610.19113v1), 2026-10-13; preprint, formal venue/status not verified. R, not a newly discovered work in this pass.
- **Prior problem:** accuracy does not identify when task-relevant prompt control, answer preference, output construction and transfer develop.
- **One-sentence solution:** make copying and applying prompt definitions predict different answers, then follow checkpoints and matched task-practice interventions.
- **Borrowed AI mechanisms:** controlled compositional diagnostic, content-source interventions, checkpoint trajectories, synthetic/rewritten-document fine-tuning.
- **Evidence depth:** fresh P abstract/introduction/Fig.1 and release/change-plan paragraphs; recovered P §§5–8 and appendix restrictions. External supplement incomplete/unread; no FULL.
- **Units/controls/cost:** token LMs, prompt definitions and conflicting examples; distinguish choosing candidates from generating the correct string. Matched ordinary-document fine-tuning is not the same as definition exercises. Appendix O reports approximately 320 H100 GPU-hours; post-plan changes are explicitly recorded in P.
- **Distinguishing hypothesis:** contextual control exists before answer mastery versus no usable mechanism; removing copying does not automatically teach construction or transfer. Exact thresholds and all supplement outcomes remain unverified.

<a id="ld-n07"></a>
## LD-N07 — LD-N07 — From Lazy to Rich: Exact Learning Dynamics in Deep Linear Networks

Canonical cluster: **BR-LD-N07**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [2409.14623v2](https://arxiv.org/html/2409.14623v2), 2025-03-04; preprint version pinned, final venue/version relation unverified. R.
- **Prior problem:** absolute initialization scale alone does not characterize how relative encoder/decoder scale determines feature evolution.
- **One-sentence solution:** derive exact deep-linear learning solutions for layer-relative λ-balanced initializations spanning static-feature and feature-learning regimes.
- **Borrowed AI mechanisms:** matrix gradient flow, balanced factorization, neural-tangent-kernel/representation dynamics.
- **Evidence depth:** fresh A/introduction; recovered P for assumptions including whitened inputs and balanced layers; extensive appendix uncompleted.
- **Units/limits:** real-vector regression/representations, no source-index lifecycle. Linear maps still have nonlinear parameter dynamics; function matching, parameter matching, and activation matching are distinct.
- **Distinguishing hypothesis:** capacity bottleneck versus an initialization/parameterization that prevents useful representation change. No direct guarantee for nonlinear Adam training.

<a id="ld-n08"></a>
## LD-N08 — LD-N08 — Don't Blame the ELBO! A Linear VAE Perspective on Posterior Collapse

Canonical cluster: **BR-A01-R16**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [1911.02469v1](https://arxiv.org/abs/1911.02469v1), 2019-11-06; NeurIPS 2019 as recovered from official proceedings. R.
- **Prior problem:** collapse is often attributed exclusively to the variational bound or a powerful autoregressive decoder.
- **One-sentence solution:** analyze linear VAEs through probabilistic PCA and distinguish marginal-likelihood stationary geometry from additional effects of approximate inference.
- **Borrowed AI mechanisms:** linear Gaussian latent models, probabilistic PCA, exact variational inference, stationary-point/stability analysis.
- **Evidence depth:** fresh A; recovered P §§3–4/6 and A.1; proofs not independently verified, not FULL.
- **Controls/limits:** observation-noise setting and fixed versus learned noise change stationary behavior. Exact-inference global optimum results do not certify arbitrary stochastic nonlinear trajectories.
- **Distinguishing hypothesis:** inference lag alone versus an objective/likelihood geometry that already supports latent non-use. Counterexample to universal blame, not a local diagnosis.

<a id="ld-n09"></a>
## LD-N09 — LD-N09 — On Lazy Training in Differentiable Programming

Canonical cluster: **BR-LD-N09**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [1812.07956v5](https://arxiv.org/abs/1812.07956v5), 2020-01-07 revision; NeurIPS 2019 per recovered record. R.
- **Prior problem:** low training error near initialization is often explained solely by enormous network width.
- **One-sentence solution:** analyze scaling-induced linearization and bound the distance between original and linearized optimization paths.
- **Borrowed AI mechanisms:** kernel-limit analysis, parameter scaling, gradient-flow comparison.
- **Evidence depth:** fresh A/version history only; original proofs/body unread in this stream. T plus author-reported vision experiments.
- **Limits/cost:** good training fit need not imply useful newly learned features; scaling can change numerical/optimization behavior while preserving nominal capacity. No automatic recommendation to shrink or enlarge every layer.
- **Distinguishing hypothesis:** unused memory because there is insufficient capacity versus because feature formation is suppressed by optimization regime.

<a id="ld-n10"></a>
## LD-N10 — LD-N10 — The Transient Nature of Emergent In-Context Learning in Transformers

Canonical cluster: **BR-LD-N10**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [2311.08360v3](https://arxiv.org/abs/2311.08360v3), 2023-12-11; NeurIPS 2023 per recovery. R.
- **Prior problem:** treating a newly emerged ICL capability as permanently retained hides potential late replacement during continued loss improvement.
- **One-sentence solution:** track synthetic-task ICL through extended training and test regularization for greater persistence.
- **Borrowed AI mechanisms:** long-horizon checkpoint evaluation, competing-strategy tasks, L2 regularization.
- **Evidence depth:** fresh original A/version; not full original reading. Read together with LD-N05's later, more specific mechanism account.
- **Controls/limits:** both contextual and weight-based solutions can fit training data; late behavior must not be described as universally context-free after the later hybrid-strategy finding.
- **Distinguishing hypothesis:** never formed versus formed then displaced while loss continues downward; establishes an existence example, not a general inevitability.

<a id="ld-n11"></a>
## LD-N11 — LD-N11 — Residual Feature Integration is Sufficient to Prevent Negative Transfer

Canonical cluster: **BR-LD-N11**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [ICLR 2026 official poster/abstract](https://iclr.cc/virtual/2026/poster/10008648), [2505.11771](https://arxiv.org/abs/2505.11771); preprint may include REFINE prefix. **Preprint revision number not freshly established**; official conference abstract is the operative source. R.
- **Prior problem:** transferred source features can harm target learning under distribution shift.
- **One-sentence solution:** retain frozen source features and learn a target-side residual encoder for signals the source representation missed.
- **Borrowed AI mechanisms:** frozen feature transfer, residual feature integration, nonparametric convergence analysis.
- **Evidence depth:** fresh official A only; theory/proofs and precise target distribution class remain unread.
- **Limits/cost:** guarantee described as no worse convergence rate than scratch up to logarithmic factors within an informative distribution class, not every finite-budget target task. Target-side capacity/adaptation is additional and must be counted.
- **Distinguishing hypothesis:** preserving a fixed useful route necessarily prevents adaptation versus complementary residual learning; this is a cross-axis transfer control, not evidence that every local bypass is benign.

<a id="a05-n01"></a>
## A05-N01 — A05-N01 — Learning Dynamics in Linear VAE: Posterior Collapse Threshold, Superfluous Latent Space Pitfalls, and Speedup with KL Annealing

Canonical cluster: **BR-A05-N01**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [PMLR 238:1936–1944](https://proceedings.mlr.press/v238/ichikawa24a.html), AISTATS 2024 final proceedings; [PDF](https://proceedings.mlr.press/v238/ichikawa24a/ichikawa24a.pdf). N; Yuma Ichikawa and Koji Hukushima.
- **Prior problem:** neither static optima nor the statement “train longer” specifies when a VAE learns useful dimensions, overfits surplus latents, or collapses.
- **One-sentence solution:** derive a large-input-dimension deterministic limit for minimal-VAE learning and analyze fixed points and KL-annealed trajectories.
- **Borrowed AI mechanisms:** dynamical mean-field/large-dimensional analysis, latent regularization, annealing.
- **Evidence depth:** A from formal metadata/abstract, not full proof reading. Author T: collapse threshold, surplus-latent overfitting, schedule-dependent convergence.
- **Units/controls/limits:** minimal linear generative/recognition vectors; not byte/source retrieval. The schedule may accelerate convergence without defeating a limiting regularization threshold. Exact assumptions, comparison compute, and full equations remain reading questions.
- **Distinguishing hypothesis:** finite optimization delay versus a stable objective-induced collapsed regime; increasing nominal latent capacity may worsen the trajectory.

<a id="a05-n02"></a>
## A05-N02 — A05-N02 — Continuous First, Discrete Later: VQ-VAEs Without Dimensional Collapse

Canonical cluster: **BR-A05-N02**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [2605.06870v3](https://arxiv.org/html/2605.06870v3), 2026-09-27; v1 2026-05-07. Preprint; no official venue/acceptance established. N.
- **Prior problem:** increasing vector-quantization codebook size or using every code can fail to improve reconstruction because the learned representation occupies very few directions.
- **One-sentence solution:** train an unquantized autoencoder until enough modes develop, then introduce quantization within the same total training-step/epoch budget.
- **Borrowed AI mechanisms:** sequential mode learning from Saxe-style autoencoders, rate-distortion reverse water-filling, PCA spectra, delayed quantization, k-means initialization/EMA/respawn.
- **Evidence depth:** fresh P §3.3 theorem statement, §§4–5, Table 1/2 captions, Appendix B settings and β=0 counterexample text. Not all proofs, numeric tables, plots or code; not FULL.
- **Units/cost:** image/audio latents, not language bytes; 100k-step image ablation and 100-epoch audio comparison exchange AE and VQ steps. Audio uses one seed and roughly seven days on two H200s/run. Equal steps is not independently verified equal FLOPs.
- **Controls/counterexample:** respawn-only and larger-codebook controls; removing commitment can raise codebook PCA dimension merely because unused random codes remain, without better reconstruction. Warm-up is not a learning-rate ramp. The diagonal Gaussian rate-distortion theorem is not a nonlinear-memory permanence theorem.
- **Distinguishing hypothesis:** actual nominal capacity shortage versus an early training restriction that prevents weak modes from forming. Rank must be measured on utilized payloads, not arbitrary unassigned vectors.

<a id="a05-n03"></a>
## A05-N03 — A05-N03 — GenFirst: Generation Before Reconstruction for Stable End-to-End Latent Generative Modeling

Canonical cluster: **BR-A05-N03**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [2608.29335v1](https://arxiv.org/abs/2608.29335), 2026-08-29; [PDF](https://arxiv.org/pdf/2608.29335v1) has internal date September 1. Preprint, formal venue unknown. N; date discrepancy recorded rather than silently normalized.
- **Prior problem:** reconstruction-optimized latents may be difficult for a generative prior; naive end-to-end training can collapse, and fast reconstruction can dominate slower distribution learning.
- **One-sentence solution:** preserve posterior entropy and give the generative objective early relative priority, then reduce prior/entropy weights to refine reconstruction.
- **Borrowed AI mechanisms:** continuous autoregressive priors, Gaussian-mixture heads, flow matching, posterior-entropy preservation, staged objective weighting and later frozen-encoder training.
- **Evidence depth:** fresh P PDF §§3.1–3.3/4.3/5.1–5.2; formula extraction incomplete/duplicated and later pages/appendices not fully examined. Not FULL or numerical certification.
- **Controls/cost:** constant weighting/cosine/PI comparisons; larger latent/VAE/prior controls do not remove the reported tradeoff. In §4.3 reconstruction weights remain fixed; prior and entropy weights decrease together. Diffusion pipeline subsequently freezes VAE for prior-only training—include that budget. Some headline outcomes include additional stages and different initializations.
- **Distinguishing hypothesis:** reconstruction-first necessarily helps versus reconstruction anchoring the wrong latent geometry; compare with N02 rather than treating the two schedules as interchangeable.

<a id="a05-n04"></a>
## A05-N04 — A05-N04 — λ-VAE: Variance Equalization for Posterior Collapse

Canonical cluster: **BR-A01-R19**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [2607.05531v1](https://arxiv.org/abs/2607.05531v1), 2026-07-06; [HTML](https://arxiv.org/html/2607.05531v1) heading omits λ-VAE prefix. Preprint, venue unverified. N; Girum Demisse.
- **Prior problem:** reconstruction/regularization gradient imbalance and information lost at stochastic sampling may jointly make collapse cheap.
- **One-sentence solution:** scale sampling noise using per-dimension exponents while retaining the original variance in the KL penalty.
- **Borrowed AI mechanisms:** Gaussian reparameterization, per-dimension gradient-balance analysis, information-theoretic objective and posterior variance control.
- **Evidence depth:** fresh P §§3.1–3.2 and proposition assumptions, not empirical tables/appendix proof completion. Author T/E; not an independently established unified account.
- **Controls/limits:** specified decay exponent controls the gradient-ratio argument; the reported operative threshold is model/dataset-specific. The deterministic continuous-encoder information/entropy equalities in §3.2 require explicit mathematical auditing; continuous differential entropy does not automatically obey discrete identities. The asymmetric sampling modification must also be checked for what distribution/objective is actually optimized.
- **Distinguishing hypothesis:** gradient-force imbalance versus loss between computed representation and sampled code. Not directly applicable to a deterministic compressor with no such sampling step.

<a id="a05-n05"></a>
## A05-N05 — A05-N05 — Competition Dynamics Shape Algorithmic Phases of In-Context Learning

Canonical cluster: **BR-A05-N05**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [2412.01003v4](https://arxiv.org/html/2412.01003v4), 2025-05-02; v1 2024-12-01. Preprint verified; publication status not certified from ambiguous search associations. N.
- **Prior problem:** distinct synthetic ICL studies can support conflicting mechanisms because model behavior mixes multiple algorithms.
- **One-sentence solution:** train on finite mixtures of Markov chains and decompose behavior into fuzzy retrieval/inference using unigram/bigram contextual statistics.
- **Borrowed AI mechanisms:** Markov sequence generators, explicit algorithm baselines, checkpoint phase analysis, context-length/task-diversity sweeps.
- **Evidence depth:** fresh A and P introduction plus Appendix discussion distinguishing optimization-limited from diversity-limited emergence; detailed experiments and appendix not fully read.
- **Units/visibility:** symbolic sequence next-token prediction; “retrieval” here is an algorithmic behavioral baseline, not permission to revisit a stored source corpus. Multiple algorithms see the same causal sequence prefix but use different statistics.
- **Distinguishing hypothesis:** longer context/training necessarily strengthens one memory computation versus causing algorithm replacement. Source-level causal attribution and exact mixture-identification uncertainty remain reading tasks.

<a id="a05-n06"></a>
## A05-N06 — A05-N06 — Differential learning kinetics govern the transition from memorization to generalization during in-context learning

Canonical cluster: **BR-A05-N06**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [2412.00104v2](https://arxiv.org/html/2412.00104v2), 2024-12-12; [ICLR 2025 official proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/187f9ba4cd5a59477305ac712282a1cd-Abstract-Conference.html). N; Alex Nguyen and Gautam Reddy. Formal version differs potentially; not a completed version comparison.
- **Prior problem:** a diversity threshold for ICL is often read as exceeding the capacity to memorize, without analyzing the relative rates of competing solutions.
- **One-sentence solution:** reduce a synthetic transformer to memorization and attention-based generalization circuits and explain threshold/onset statistics through their differential learning kinetics.
- **Borrowed AI mechanisms:** additive-logit independence ansatz, scalar query/key and value order parameters, gradient-flow approximations, memorization scaling.
- **Evidence depth:** fresh P §§3.2–3.4, including large-dimension and small-initialization assumptions; full appendix and experimental controls unread. Theory/empirical source, not replication.
- **Controls/limits:** reduced model separates MLP memorization and attention ICL; retains contextual-label fluctuations in the expansion. Appendix plots include seeds that never acquire ICL, acquired-but-not-yet-transient runs, and observed transience—these are censored outcomes, not interchangeable negatives.
- **Distinguishing hypothesis:** limited parameter capacity versus a race between solutions; counterpoint to LD-N05 because independence is an ansatz here, not a universal rejection of shared circuits.

<a id="a05-n07"></a>
## A05-N07 — A05-N07 — Universal Language Model Fine-tuning for Text Classification

Canonical cluster: **BR-A05-N07**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [ACL 2018 P18-1031](https://aclanthology.org/P18-1031/), pp.328–339; [official PDF](https://aclanthology.org/P18-1031.pdf). N; Jeremy Howard and Sebastian Ruder. Use the proceedings version, not an assumed arXiv equivalence.
- **Prior problem:** aggressive fine-tuning forgets transferred language knowledge, while cautious adaptation can underfit or learn slowly.
- **One-sentence solution:** combine task LM adaptation and classifier training with layer-dependent learning rates, a slanted-triangular rate schedule, and gradual unfreezing.
- **Borrowed AI mechanisms:** AWD-LSTM transfer, discriminative layer rates, staged thawing, pooled document representations, supervised classification.
- **Evidence depth:** fresh P §§3.2–3.3/5 and Table 7 discussion; all table cells/appendix/source code not read, not FULL.
- **Controls/counterexample:** last-layer only, full, chain-thaw, gradual unfreezing, and rate schedules. Gradual unfreezing alone is reported similar to full; last-layer only underfits; benefits are not universally attributable to freezing. Validation tunes epochs, different rates apply, and bidirectional results use a separately trained model.
- **Distinguishing hypothesis:** fixed-feature consumer adaptation sufficient versus needing coordinated representation readaptation; freeze schedule versus learning-rate confounding.

<a id="a05-n08"></a>
## A05-N08 — A05-N08 — The Dormant Neuron Phenomenon in Deep Reinforcement Learning

Canonical cluster: **BR-A05-N08**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [PMLR 202:32145–32168](https://proceedings.mlr.press/v202/sokar23a.html), ICML 2023; arXiv alias 2302.12902. N; Ghada Sokar, Rishabh Agarwal, Pablo Samuel Castro, Utku Evci.
- **Prior problem:** neurons can become inactive during reinforcement-learning training, reducing usable network expressivity.
- **One-sentence solution:** detect and recycle dormant neurons throughout learning with ReDo.
- **Borrowed AI mechanisms:** activation-utility monitoring, selective weight reinitialization and continued training.
- **Evidence depth:** official A only; reset details, replay/update-ratio controls and old-skill retention need full reading.
- **Limits/cost:** RL target/data nonstationarity differs from stationary language modeling. Dormancy is not equivalent to information loss, low representation rank, or missing curvature; compare N09/N11. Resets can erase useful features and require recovery computation.
- **Distinguishing hypothesis:** unused units and declining trainability versus unchanged active representation with a consumer bypass. Not an automatic instruction to recycle memory units.

<a id="a05-n09"></a>
## A05-N09 — A05-N09 — DASH: Warm-Starting Neural Network Training in Stationary Settings without Loss of Plasticity

Canonical cluster: **BR-A05-N09**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [NeurIPS 2024 official PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/4c5ce1fc8895076f49935951a630be5c-Paper-Conference.pdf), [2410.23495v2](https://arxiv.org/abs/2410.23495), 2024-11-01. N; proceedings version operative for section claims, exact arXiv diff not checked.
- **Prior problem:** warm-starting can generalize worse than scratch even as new samples arrive from a stationary distribution.
- **One-sentence solution:** selectively shrink weight directions judged to encode noise while preserving learned feature directions at data-expansion boundaries.
- **Borrowed AI mechanisms:** discrete feature/noise learning model, gradient/weight alignment, per-neuron direction-aware shrinking, expanding-data curricula.
- **Evidence depth:** fresh P §§2–5; proofs/appendices not fully read. The abstract framework is deliberately not an exact hypothesis-class SGD theorem.
- **Controls/counterexample/cost:** cold/warm/shrink-and-perturb, stationary chunks, train-to-99.9% stopping, steps-to-convergence reporting. Dormant-unit revival/normalization/nonstationary fixes need not transfer; strong standard-training settings approach rather than beat cold-start performance. Repeated gradient estimation and return-to-convergence are not free.
- **Distinguishing hypothesis:** data-distribution shift is necessary for plasticity loss versus path-dependent learning under stationary data. Not a local proof that memorized noise explains compressor behavior.

<a id="a05-n10"></a>
## A05-N10 — A05-N10 — Exact solutions to the nonlinear dynamics of learning in deep linear neural networks

Canonical cluster: **BR-A05-N10**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [1312.6120v3](https://arxiv.org/abs/1312.6120v3), 2014-02-19; ICLR 2014 association via [Oxford institutional record](https://ora.ox.ac.uk/objects/uuid:49f24917-64cc-4d41-ba52-7aabc67662ce) found in search; institutional full record not fetched in this pass, so venue is not independently re-audited. N; Andrew M. Saxe, James L. McClelland, Surya Ganguli.
- **Prior problem:** a linear input-output map can still have nonlinear, slow or abrupt parameter-learning dynamics as depth/initialization change.
- **One-sentence solution:** solve restricted deep-linear gradient dynamics and compare random, orthogonal and unsupervised-pretrained initial conditions.
- **Borrowed AI mechanisms:** singular-mode decomposition, gradient flow, orthogonal initialization and layerwise pretraining.
- **Evidence depth:** fresh A/version only; formal solutions and conditions await reading.
- **Limits:** exact linear dynamics do not identify nonlinear model circuits. Sequential mode formation and finite depth delays are existence/conditional results, not evidence of an actual byte-memory bottleneck.
- **Distinguishing hypothesis:** endpoint capacity failure versus a slow trajectory through learnable modes; original baseline for LD-N07/N02 rather than treating their ideas as isolated recent inventions.

<a id="a05-n11"></a>
## A05-N11 — A05-N11 — Directions of Curvature as an Explanation for Loss of Plasticity

Canonical cluster: **BR-A05-N11**. [Carrying source record](../01_discovery/A05/WORKS_AND_PROBLEMS.md).

- **Identity/version/status:** [2312.00246v2](https://arxiv.org/html/2312.00246v2), 2024-02-17. The abstract-page record uses *Curvature explains loss of plasticity* and lists v4 2024-10-05; title/version drift is retained, not silently equated. Preprint; no formal acceptance verified. N.
- **Prior problem:** shrinking update norms, dead units and feature-rank reduction do not consistently explain failure to learn successive tasks.
- **One-sentence solution:** test counterexamples and track loss of curvature directions, proposing a distributional regularizer to preserve plasticity.
- **Borrowed AI mechanisms:** task-switch benchmarks, activation controls, Hessian effective-rank diagnostics, empirical-Fisher/per-example-gradient Gram approximation, distributional regularization.
- **Evidence depth:** fresh P §§3–4 and Fig.1/2 captions, plus abstract; not full experiments/proofs. Curvature co-occurrence and regularizer evidence are author observations, not exclusive-cause proof.
- **Controls/counterexamples:** ReLU/leaky-ReLU/tanh/identity with 200 epochs/task; update norm can rise while plasticity falls; feature-rank regularization can fail despite higher rank. Proxy Hessian rank is sample-limited and not exact; Fisher, empirical Fisher, Gauss–Newton and Hessian are distinct.
- **Distinguishing hypothesis:** simple inactive/rank-poor representation versus an optimization-landscape limitation. Supplies a counter-control to adopting N02/N08 diagnostics universally.

<a id="n06-01"></a>
## N06-01 — N06-01 — How transferable are features in deep neural networks?

Canonical cluster: **BR-N06-01**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [arXiv:1411.1792v1](https://arxiv.org/html/1411.1792v1), 2014-11-06; Yosinski et al.; NeurIPS 2014 association inherited from prior audit, original experiment text freshly checked, proceedings not re-audited. **Provenance/depth:** recovered discovery; targeted §§2–4.3 and Appendix A, not FULL.

- **Prior problem:** apparent feature non-transferability can conflate task specialization with breaking jointly learned dependencies.
- **One-sentence solution:** cross same-task versus cross-task copied lower layers with frozen versus fine-tuned copied weights, while reinitializing and relearning the upper layers.
- **Borrowed mechanisms / learning:** convolutional feature reuse, frozen transfer and gradient fine-tuning; ImageNet label cross-entropy. Input units are image pixels/features, not byte segments; no memory addressing or original-source retrieval.
- **Controls/evidence:** BnB, AnB, BnB+, AnB+, random lower-layer controls and more-distant task splits; same-task middle-layer deficits can disappear when copied layers adapt. **BnB randomizes the upper network**, so it is not exact replay of the original pair of halves.
- **Distinguishes:** specificity vs relearning/co-adaptation cost; frozen compatibility vs plastic recovery.
- **Cost/failure/transfer:** original lower-model training plus continuation must be counted; App. A uses 450k iterations per normal run. Fine-tuning restoration does not identify which local component caused a deficit or prove byte-model transfer.

<a id="n06-02"></a>
## N06-02 — N06-02 — Revisiting Model Stitching to Compare Neural Representations

Canonical cluster: **BR-N06-02**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [arXiv:2106.07682v1](https://arxiv.org/html/2106.07682v1), 2021-06-14; Bansal, Nakkiran and Barak; NeurIPS 2021 association inherited. **Provenance/depth:** recovered; original abstract/introduction revisited, detailed connector training/appendix not newly audited.

- **Prior problem:** geometric similarity measures need not show whether another model can actually consume a representation.
- **Solution:** freeze two original half-networks and train a simple intervening layer to test task-preserving forward compatibility.
- **Mechanisms/learning/units:** affine/interface transformation trained with task supervision; image feature maps, source prefix and recipient suffix; no query-time source revisit.
- **Evidence/controls:** authors report compatible good networks across initialization/objectives, and improved weaker models supplied with stronger prefixes. This stream does not independently certify every connector constraint or training table.
- **Distinguishes:** a useful restricted interface exists vs raw coordinates are incompatible; it does not establish shared information cues.
- **Cost/failure:** connector data, tuning and original training remain costs; unrestricted connectors risk learning task solutions rather than exposing old semantics. Pair with N06-03 and A06-X04, not a stand-alone similarity certificate.

<a id="n06-03"></a>
## N06-03 — N06-03 — How not to Stitch Representations to Measure Similarity: Task Loss Matching versus Direct Matching

Canonical cluster: **BR-N06-03**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [arXiv:2412.11299v1](https://arxiv.org/html/2412.11299v1), 2024-12-15; Balogh and Jelasity; AAAI 2025 association from prior official metadata, not freshly proceedings-verified. **Provenance/depth:** recovered; targeted abstract, introduction and matching formulation; OOD detector appendix returned but not fully audited.

- **Prior problem:** high task accuracy of a stitched model is routinely interpreted as original functional similarity.
- **Solution:** compare task-loss-optimized affine stitching with direct activation-distance matching and sanity checks on layer correspondence/self-similarity.
- **Mechanisms/learning/units:** affine maps, least-squares/pseudoinverse direct matching, downstream task optimization and distribution diagnostics over image features.
- **Evidence:** task-loss matching can rate distant layers, including another layer versus itself, unexpectedly highly; authors connect this to unusual recipient activations. These are measurement counterexamples, not proof practical learned composition has no value.
- **Distinguishes:** original representation equivalence vs task-specific rerouting; high score vs natural interface distribution.
- **Cost/failure:** direct matching penalizes all coordinate errors, including possibly irrelevant subspaces; it need not be the best deployment interface. Detector validity and exact training must be read before treating OOD scores as ground truth.

<a id="n06-04"></a>
## N06-04 — N06-04 — Revisiting Model Stitching in the Foundation Model Era

Canonical cluster: **BR-N06-04**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [arXiv:2603.12433v3](https://arxiv.org/html/2603.12433v3), 2026-06-02 per previous version audit; [official CVPR 2026 PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Mai_Revisiting_Model_Stitching_In_the_Foundation_Model_Era_CVPR_2026_paper.pdf) located by search, not newly full-read. Old audit used v1; this stream uses **v3 targeted text**, no line-by-line version equivalence claim. **Provenance/depth:** recovered/version-advanced; §§3.2–5.3 plus selected source/control discussion.

- **Prior problem:** heterogeneous vision foundation models may fail to compose under local feature matching or direct downstream training, even with small local errors.
- **Solution:** pretrain only the stitch on recipient final features, then task-fine-tune it while original source/recipient remain frozen.
- **Mechanisms/learning/units:** teacher feature distillation, per-position linear/MLP interfaces or a LoRA-enabled source layer, downstream supervision; image tokens/maps, no byte or source-address contract.
- **Controls/evidence:** §4.1 inserts identical stitch modules at identical positions, objectives and data in both self-models. §5.3 compares interface families, and §5.2 reports a weaker CLIP source still failing to match stronger recipients. Gains are not guaranteed by adding interface expressiveness.
- **Distinguishes:** local alignment error vs downstream sensitivity; extra capacity vs cross-model complementarity; interface/optimization failure vs potentially missing source information.
- **Cost/failure:** teacher final-feature computation and two-stage training are extra supervision; exact matched compute/seed intervals remain full-read questions. Authors' information-loss explanation for the weaker source is not an independent impossibility proof.

<a id="n06-05"></a>
## N06-05 — N06-05 — The Hydra Effect: Emergent Self-repair in Language Model Computations

Canonical cluster: **BR-A04-R02**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [arXiv:2307.15771v1](https://arxiv.org/abs/2307.15771v1), 2023-07-28; McGrath et al.; preprint, accepted venue not verified. **Provenance/depth:** recovered; original abstract/history only.

- **Prior problem:** component ablation effects can be masked by later computation changing its response.
- **Solution:** analyze attention-layer compensation and late MLP counterbalancing through causal interventions in factual recall.
- **Mechanisms/learning/units:** activation ablation and downstream response analysis in pretrained token LMs; no additional training intervention certified at this depth.
- **Evidence:** authors report compensation, even without training dropout, and relatively localized coupling. Configuration/scope is not a newly read result table.
- **Distinguishes:** absent causal contribution vs naturally compensated contribution.
- **Cost/failure:** not a transplant recipe or an equal-compute architecture comparison. Prefer N06-06 for systematic follow-up before operationalizing compensation controls.

<a id="n06-06"></a>
## N06-06 — N06-06 — Explorations of Self-Repair in Language Models

Canonical cluster: **BR-N06-06**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [ICML 2024, PMLR 235:42836–42855](https://proceedings.mlr.press/v235/rushing24a.html), formal proceedings verified; prior targeted text [2402.15390v2](https://arxiv.org/html/2402.15390v2) was not freshly reread here. **Provenance/depth:** recovered; official metadata and abstract freshly verified, prior body claims remain bounded by old audit.

- **Prior problem:** narrow-example self-repair observations may not describe broad prompt distributions or different model families.
- **Solution:** measure how attention-head ablations are compensated across broad distributions/families and separate candidate mechanisms.
- **Mechanisms/units:** activation ablation, direct/total effects, LayerNorm scaling and anti-erasure neurons; token LM activations.
- **Evidence:** official abstract reports repair is imperfect, noisy and sometimes overcorrecting, with scaling and sparse anti-erasure contributions.
- **Distinguishes:** small total effect because a component is unused vs because downstream computation compensates; mean compensation vs prompt variability.
- **Cost/failure:** not evidence that a fixed-downstream diagnostic equals deployed total damage. Exact resampling, multi-head and distribution controls are queued, not already certified.

<a id="n06-07"></a>
## N06-07 — N06-07 — LoLCATs: On Low-Rank Linearizing of Large Language Models

Canonical cluster: **BR-N06-07**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [2410.10254v3](https://arxiv.org/html/2410.10254v3), 2025-03-05; **accepted ICLR 2025**, [official proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/72163d1c3c1726f1c29157d06e9e93c1-Abstract-Conference.html). **Provenance/depth:** recovered; §§3.1–3.3 opening and Table 2 read; no FULL.

- **Prior problem:** replacing pretrained softmax attention by linear attention can badly degrade quality; full-model restoration is expensive.
- **Solution:** first fit new attention feature maps to teacher attention outputs, then compensate remaining errors using low-rank projection updates.
- **Mechanisms/learning/units:** MSE feature distillation under teacher-fed layer inputs; causal next-token cross-entropy with LoRA; kernel features and window+linear variants; token hidden states/QKV, not original-text lookup.
- **Evidence/control:** Table 2 compares transfer/no transfer and LoRA/no LoRA. Llama-3-8B T2R gives 1539.39/79.33 before adjusting without/with transfer, and 16.05/4.11 after adjusting. Combined training uses 2+2 epochs versus 4 for a single stage. Original weights frozen in matching; LoRA updates specified Q/K/V/O in adjustment.
- **Distinguishes:** one-stage failure vs staged repair; attention approximation vs adaptation compatibility.
- **Cost/failure:** the table is an equal-total-step **strategy** comparison, not equal-dose 2×2 mechanistic interaction estimation. The untrained baseline and different adjustment doses matter. Teacher cost, natural-chain accumulation and final long-context content use need separate accounting.

<a id="n06-08"></a>
## N06-08 — N06-08 — Transformers to SSMs: Distilling Quadratic Knowledge to Subquadratic Models

Canonical cluster: **BR-N06-08**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [2408.10189v2](https://arxiv.org/html/2408.10189v2), 2025-02-08 per old version audit; v1 had shorter title. Current text verified, accepted-venue status not independently certified. **Provenance/depth:** recovered/version-advanced; targeted §4 and selected §5/control passages.

- **Prior problem:** strong Transformer training investment is difficult to reuse in subquadratic sequence models.
- **Solution:** MOHAWK matches sequence-mixing matrices, then block outputs, then whole-model outputs in stages.
- **Mechanisms/learning/units:** structured-matrix approximation, feature MSE, inherited teacher weights, logit distillation; causal token sequence mixers, no original-source revisit.
- **Evidence/controls:** convolution initially identity, gate opened to one, output normalization and post-convolution activation removed for transplant alignment; native from-scratch helpful components need not remain helpful in this history. Same-architecture Phi→Phi control resets attention while inheriting the other weights.
- **Distinguishes:** architecture capacity vs transplant conditioning; missing/mismatched companions vs central mixer; local/block alignment vs composed error.
- **Cost/failure:** teacher pretraining and staged exposure are not free; not all stage ablations have been verified equal-total-budget in this stream. The paper's scratch/transfer comparisons do not randomize pretraining history.

<a id="n06-09"></a>
## N06-09 — N06-09 — Data Efficient Any Transformer-to-Mamba Distillation via Attention Bridge

Canonical cluster: **BR-N06-09**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [2510.19266v4](https://arxiv.org/abs/2510.19266v4), 2026-09-16; first submitted 2025-10-22. Current abstract calls method Cross-architecture distillation via Attention Bridge (CAB). No accepted venue independently verified. **Provenance/depth:** recovered; fresh original abstract/history; previous targeted introduction not upgraded.

- **Prior problem:** direct intermediate features from attention and state-space models may not match structurally; output-only distillation misses useful intermediate guidance.
- **Solution:** use a lightweight bridge and flexible layer alignment to supervise Mamba's token-dependent state projections from attention-related teacher representations.
- **Mechanisms/units:** cross-architecture feature distillation and learned alignment over token-level states; image classification and language modeling are both claimed.
- **Evidence:** original abstract reports improvements under limited supervision and no inference-time bridge overhead. Actual intervention tables were not read.
- **Distinguishes:** missing correspondence/interface vs intrinsically non-transferable knowledge; output-only vs intermediate supervision.
- **Cost/failure:** bridge training/teacher passes remain costs; “Any” in the title is not arbitrary-host coverage. Not promoted above MOHAWK without extracting incremental controls.

<a id="n06-10"></a>
## N06-10 — N06-10 — Bridging KV-Cache Quantization and Linear Attention: From Theory to Pretrained Weight Migration

Canonical cluster: **BR-N06-10**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [2610.11214v1](https://arxiv.org/html/2610.11214v1), 2026-10-08; preprint; distinct from W0214. **Provenance/depth:** recovered; targeted introduction, §5.3 and appendix staged-ablation discussion. Current extraction omits numerical table cells.

- **Prior problem:** aggregation into recurrent state and per-entry KV quantization are different compression regimes; pretrained Transformer weights need a recoverable bridge.
- **Solution:** use soft discrete-address assignments and a soft-quantized intermediate construction for head→block→whole-model RAM-Net migration.
- **Mechanisms/learning/units:** codebook/soft address overlap, low-rank adapters and staged distillation/recovery; token Q/K/V to addressable continuous slots; no retained original-text retrieval.
- **Evidence/control:** fixed 500M-token Qwen2.5-1.5B pipeline comparison, removing head/block stages reallocates their tokens to whole-model recovery. Authors report lower task scores without intermediate stages even when Wiki PPL remains similar. Numerical cells in the prior audit are **not independently reverified here**.
- **Distinguishes:** benefit of staged objective vs simply more tokens; PPL restoration vs downstream restoration.
- **Cost/failure:** equal tokens does not equal teacher FLOPs/wall time; restricted overlap approximation is not a global full-attention identity or a universal migration guarantee.

<a id="n06-11"></a>
## N06-11 — N06-11 — On the State of the Art of Evaluation in Neural Language Models

Canonical cluster: **BR-N06-11**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [1707.05589v2](https://arxiv.org/html/1707.05589v2), 2017-11-20; Melis, Dyer and Blunsom; version text verified, ICLR 2018 association not freshly proceedings-verified. **Provenance/depth:** recovered; targeted §5.1 and §7, with returned main text inspected for scope.

- **Prior problem:** architecture rankings conflate capacities, regularization and uneven tuning effort.
- **Solution:** tune regularization/optimization and embedding-vs-recurrent parameter allocation within defined model-size budgets and rerun selected configurations.
- **Mechanisms/learning/units:** black-box Gaussian-process tuning, recurrent LMs, tied embeddings and down-projections; word LM plus Enwik8 character setting, not one universal interface.
- **Evidence/control:** §5.1 lets tuner trade embedding and hidden size inside a parameter budget; §7.1 evaluates individual features, **not their combinations**; §7.2 checks rerun variability.
- **Distinguishes:** parameter count vs allocation/trainability; fixed-default result vs optimized model family.
- **Cost/failure:** substantial tuning expense, thousands of evaluations in some settings. This is not a cheap full-factorial recipe and its historical PPL noise thresholds do not transfer to this project.

<a id="n06-12"></a>
## N06-12 — N06-12 — The Key to Going Linear: Analysis-Driven Transformer Linearization

Canonical cluster: **BR-N06-12**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [2607.07706v1](https://arxiv.org/html/2607.07706v1), public first submission 2026-07-08 in prior metadata; HTML header says February 2026, not used as public-release date. Preprint; no accepted venue verified. **Provenance/depth:** recovered; targeted §3–4 and App. C implementation/budget.

- **Prior problem:** post-hoc linearization bundles many simultaneous changes and obscures which state update preserves pretrained attention.
- **Solution:** compare replacement mechanisms with an initially fully frozen original backbone, then add explicitly controlled structural/limited-adaptation changes.
- **Mechanisms/learning/units:** delta-rule versus gated/kernelized accumulation, causal next-token CE, local/prefix cache routing, short convolution and LoRA; token recurrent states/QKV.
- **Evidence/control:** 10M tokens/2,500 iterations, 4,096-length packing; QKV unchanged in strict core comparison. Constant 64 cache slots can be divided into 56 local+8 prefix. §4 reports GLA/GDN gap nearly vanishing with short convolutions; LoRA uses smaller learning rate for stability. App. C: no sweep, three stated seeds.
- **Distinguishes:** core-rule effects conditional on companions and projection plasticity; strict frozen-host ranking vs adapted-host ranking.
- **Cost/failure:** implementations differ greatly in elapsed time (authors report ~1h GLA/GDN vs ~8h Hedgehog on H100 in this setup). Equal tokens and identical defaults do not equal equal optimization opportunity. First-order analysis is not global long-sequence task equivalence.

<a id="a06-x01"></a>
## A06-X01 — A06-X01 — Net2Net: Accelerating Learning via Knowledge Transfer

Canonical cluster: **BR-A06-X01**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [1511.05641v4](https://arxiv.org/html/1511.05641v4); Chen, Goodfellow and Shlens; ICLR 2016 association, locked v4 body independently read selectively, proceedings not rechecked. **Depth/role/stage:** targeted §§2.1–2.4/3 and App. A; positive control and restoration/formation alternative, not FULL.

- **Prior problem:** architectural expansion incurs destructive transient loss and repeatedly starts optimization from scratch.
- **Solution:** initialize wider/deeper students with function-preserving transformations of an already trained network before continuation.
- **Mechanisms/learning/units:** duplicate hidden units and compensate outgoing weights; insert identity layers subject to nonlinearity constraints; normal supervised continuation. Image hidden units/maps, not byte compression.
- **Evidence/controls:** random-padding/random-initialization controls; §2.1 also reports unsuccessful hidden-feature prediction relative to a strong batch-normalized baseline. ReLU identity condition is explicit; sigmoid insertion is not generically identity. Symmetry-breaking noise makes exact preservation approximate.
- **Distinguishes:** surgery implementation damage vs extra parameters; initial functional capacity vs later learned usable capacity; benefit of a matching objective vs strong baseline optimization.
- **Cost/limits:** source pretraining and continuation must be counted. App. A uses smaller student learning rate. Increasing parameter count alone is not a clean increase in effective task information at t=0. Cannot declare a learned lossy compressor “identity” merely because its output length is unchanged.

<a id="a06-x02"></a>
## A06-X02 — A06-X02 — Progressive Neural Networks

Canonical cluster: **BR-A06-X02**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [1606.04671v4](https://arxiv.org/html/1606.04671v4), version associated with 2022 revision, originally 2016; Rusu et al.; accepted venue not verified. **Depth/role/stage:** targeted §§2–3/5.1–5.3 and limitations; constructive alternative, formation/transfer.

- **Prior problem:** sequential fine-tuning destroys old features and forces the recipient to use a potentially harmful source initialization.
- **Solution:** freeze old task columns, add a new trainable column and learned lateral adapters that may reuse or ignore old features.
- **Mechanisms/learning/units:** A3C reinforcement learning, nonlinear lateral adapters, per-source scaling, Fisher/perturbation sensitivity; image-observation control policies, not text retrieval.
- **Evidence/controls:** target-only, source-pretrained output-only, source-pretrained fully fine-tuned, and randomly initialized frozen-source multi-column baselines. §5.1 reports top three of 25 sampled seed/hyperparameter jobs and learning-curve area, not unconditional all-run means.
- **Distinguishes:** useful pretrained content vs generic extra branch capacity; source feature reuse vs new learning; frozen reuse vs destructive adaptation.
- **Cost/limits:** total parameters grow, task label selects inference column, some negative transfer remains. Do not import “no forgetting” as a guarantee if old pathways are modified or routing changes. A bounded extra branch is an alternative to any original-source revisit.

<a id="a06-x03"></a>
## A06-X03 — A06-X03 — Git Re-Basin: Merging Models Modulo Permutation Symmetries

Canonical cluster: **BR-A06-X03**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [2209.04836v6](https://arxiv.org/html/2209.04836v6); Ainsworth, Hayase and Srinivasa; ICLR 2023 association, proceedings not independently re-fetched. **Depth/role/stage:** targeted §2–3 and abstract/limitations; coordinate-control alternative, post-training composition.

- **Prior problem:** incompatible coordinate order can make equivalent hidden functions look distant and naive weight interpolation fail.
- **Solution:** choose hidden-unit permutations to align independently trained equivalent-architecture models before merging.
- **Mechanisms/learning/units:** activation matching, weight matching and permutation symmetry; existing network weights, no language-source access.
- **Evidence/control:** §2 gives function-preserving paired incoming/outgoing permutations; authors also discuss a counterexample to the universal single-basin hypothesis. Exact known permutation recovery is mentioned in appendix but not independently tested here.
- **Distinguishes:** coordinate mismatch vs different function/content; pure representation relabeling vs actual semantic intervention.
- **Cost/limits:** matching cost and architecture constraints remain. Grouped operations, tied/shared parameters and normalization can restrict legal permutations; no automatic rotation/permutation certificate for a different recurrence or compressed state.

<a id="a06-x04"></a>
## A06-X04 — A06-X04 — Functional Alignment Can Mislead: Examining Model Stitching

Canonical cluster: **BR-A06-X04**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [ICML 2025, PMLR 267:55972–55998](https://proceedings.mlr.press/v267/smith25a.html); Smith, Mannering and Marcu; formal venue and official PDF endpoint verified. **Depth/role/stage:** original proceedings abstract only; counterexample, post-training measurement.

- **Prior problem:** successful functional alignment is interpreted as capturing the same information.
- **Solution:** deliberately stitch representations trained on different cues/tasks/modalities, including clustered random noise, to test the implication.
- **Mechanisms/units:** frozen-half stitching plus learned connection; exact connector details not read; vision feature representations and artificial sources.
- **Evidence:** official abstract explicitly reports successful stitching in these cases; it is not a newly audited effect-size table.
- **Distinguishes:** useful predictive compatibility vs original shared information/invariances.
- **Cost/limits:** actual random-noise construction, held-out sampling and label leakage controls require full reading. “Clustered random noise” must not be paraphrased as arbitrary fresh i.i.d. noise preserving all semantic information. Queue this precise missing question, not a blanket dismissal of stitching.

<a id="a06-x05"></a>
## A06-X05 — A06-X05 — Grounding Functional Similarity by Invariance-Aware Model Stitching

Canonical cluster: **BR-A06-X05**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [2505.20142v2](https://arxiv.org/html/2505.20142v2), 2026-06-01; v1 first submitted 2025-05-26 per [official history](https://arxiv.org/abs/2505.20142v2). **Depth/role/stage:** targeted §§2–3 and Appendix D; positive diagnostic protocol, no FULL. **Venue: unresolved for this exact version**. Related ICLR 2026 forum hJvcbkf2nO has different searched title/author list; current repo advertises ICML 2026, but that is not independent venue verification. Do not merge claims/status by name resemblance.

- **Prior problem:** forward stitching can exploit predictive cues while ignoring source/recipient invariance differences; direct matching can instead over-penalize irrelevant subspaces.
- **Solution:** test forward–backward compatibility using inputs optimized to be nearly identical in the source representation and alignment objectives spanning internal recipient layers.
- **Mechanisms/learning/units:** representation inversion from noise, frozen image models, affine stitch initialized by pseudoinverse on 500 samples, feature-distillation hints up to the penultimate layer. The backward direction is about input preimages, **not gradient propagation**.
- **Evidence/control:** same initialization across ordinary and invariance-aware stitching, cue variants and shortcut availability; FuLA does not use output-level hints in the stated implementation. §2.3.1 explicitly notes approximate input inversions and an assumed unique optimal forward compatibility.
- **Distinguishes:** forward predictive compatibility vs shared discarded/preserved cues; local matching vs downstream sensitive subspaces.
- **Cost/limits:** inversion is extra optimization and may create unnatural inputs. This suggests a natural counterfactual-cue test for language, not permission to assume continuous image inversion works over valid bytes. Full reading must audit inverse-domain validity and robustness.

<a id="a06-x06"></a>
## A06-X06 — A06-X06 — GPTailor: Large Language Model Pruning Through Layer Cutting and Stitching

Canonical cluster: **BR-A06-X06**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** **accepted ICLR 2026**, [official proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5c99f2254833533c2a8ca0e0be04d77e-Abstract-Conference.html); targeted [2506.20480v1](https://arxiv.org/html/2506.20480v1), 2025-06-25. No claim the preprint equals final proceedings page for page. **Depth/role/stage:** §§3.4/4.3–4.4 selective; practical multi-component deployment search.

- **Prior problem:** single-model pruning discards complementary ability emphasized in related fine-tunes.
- **Solution:** jointly search layer removal, donor-layer selection and layer merging to assemble a compact model.
- **Mechanisms/learning/units:** zero-order configuration search with SMAC/random-forest surrogate and multi-fidelity calibration evaluation; pretrained token-model layers, no original-source retrieval.
- **Evidence/control:** §4.4 reports full search 48.55 average, removal-only 44.83 and selection+removal 43.20 in its 7B setting; selection without merging is not a reliable improvement. §4.2/4.3 specifies 500 search trials, calibration-size fidelity and adaptive resource allocation.
- **Distinguishes:** useful joint integration vs naive mix-and-match; search optimization capacity vs component feasibility.
- **Cost/limits:** donor fine-tunes, calibration labels, search compute and expanded space must be charged. Nested search-space optimum cannot worsen mathematically; observed worse searched result can reflect finite optimization and is not proof donor selection inherently harms a fixed model. This is not an identified full-factorial interaction coefficient.

<a id="a06-x07"></a>
## A06-X07 — A06-X07 — KLAS: Using Similarity to Stitch Neural Networks for Improved Accuracy-Efficiency Tradeoffs

Canonical cluster: **BR-A06-X07**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** **accepted ICLR 2026**, [official proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/e9f0ce998bede73f8068985f3deeab9a-Abstract-Conference.html); [2605.29259v1](https://arxiv.org/abs/2605.29259v1), 2026-05-28. Search gave one inconsistent 2025 date for HTML: official history is used instead. **Depth/role/stage:** official abstract/history only, practical deployment selection, not FULL.

- **Prior problem:** heuristic stitch-site/model-pair selection yields weak accuracy–compute tradeoffs.
- **Solution:** rank promising binary stitches by intermediate KL-divergence-based similarity before fine-tuning.
- **Mechanisms/learning/units:** representation similarity, candidate selection among O(k²n²) possibilities, stitch fine-tuning; vision features and ImageNet classification.
- **Evidence/control:** original abstract claims improved tradeoff at the same fine-tuning cost as baselines, up to 1.21 percentage points or 1.33× fewer FLOPs in stated comparisons. Search overhead, training permissions and exact controlled budgets not yet read.
- **Distinguishes:** bad site selection vs no compatible composition; practical efficient search vs intrinsic representation equivalence.
- **Cost/limits:** abstract-level same-cost claim is not a certified complete development-budget ledger. No transfer to language tasks is assumed.

<a id="a06-x08"></a>
## A06-X08 — A06-X08 — TIES-Merging: Resolving Interference When Merging Models

Canonical cluster: **BR-A06-X08**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [2306.01708v2](https://arxiv.org/html/2306.01708v2), 2023-10-27; **NeurIPS 2023**, [official proceedings](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1644c9af28ab7916874f6fd6228a9bcf-Abstract-Conference.html). **Depth/role/stage:** targeted introduction, formulation and sign-interference discussion; §7.3 ablations located, not fully read. Composition alternative/counterexample.

- **Prior problem:** merging several fine-tunes loses value through many low-magnitude updates and conflicting update signs.
- **Solution:** trim task deltas, elect a common coordinate sign and average only sign-consistent changes.
- **Mechanisms/learning/units:** sparse weight-delta selection, sign voting and coefficient scaling over common-base model weights; pre-existing task fine-tunes provide learning, not a new state-read mechanism.
- **Evidence/control:** sign conflicts persist after trimming and grow with task count; comparisons include full and parameter-efficient fine-tuning. Exact component-ablation numbers remain unread.
- **Distinguishes:** composition failure from parameter interference vs each single capability being bad; unit norm/parameter count vs coordinate-wise conflict.
- **Cost/limits:** coefficient/density selection and original donor fine-tuning are costs. Update signs are parameterization-dependent; this is not a universal causal explanation of interference in arbitrary independently trained hosts.

<a id="a06-x09"></a>
## A06-X09 — A06-X09 — Editing Models with Task Arithmetic

Canonical cluster: **BR-A06-X09**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [2212.04089v3](https://arxiv.org/html/2212.04089v3), 2023-03-31; [official abstract/history](https://arxiv.org/abs/2212.04089v3); ICLR 2023 association, forum decision not freshly inspected. **Depth/role/stage:** targeted abstract/introduction and task-vector formulation; further experiments not fully read. Positive/negative weight intervention alternative.

- **Prior problem:** adapting a pretrained model separately for every behavior does not expose a cheap compositional edit operation.
- **Solution:** form fine-tuned-minus-base weight vectors and add, negate or combine them to steer task behavior.
- **Mechanisms/learning/units:** task-vector subtraction/addition, coefficient selection and shared pretrained coordinate system; existing language/vision model weights, not a text-memory representation.
- **Evidence/control:** original text reports target degradation under vector negation with relatively preserved control tasks, and multi-task improvements by addition. Not a proof of general linear skill additivity.
- **Distinguishes:** selective acute capability modification vs broad destruction; combining shared-origin deltas vs transplanting representations from unrelated bases.
- **Cost/limits:** donor training and coefficient selection remain relevant; cross-base delta transport cannot be presumed meaningful. Non-additive outcomes should be measured with same original base and individual-delta controls.

<a id="a06-x10"></a>
## A06-X10 — A06-X10 — Capacity and Trainability in Recurrent Neural Networks

Canonical cluster: **BR-A06-X10**. [Carrying source record](../01_discovery/A06/WORKS_AND_PROBLEMS.md).

**Source/version/status:** [1611.09913v3](https://arxiv.org/html/1611.09913v3), 2017-03-03; [history](https://arxiv.org/abs/1611.09913); Collins, Sohl-Dickstein and Sussillo; ICLR 2017 association not independently proceedings-verified. **Depth/role/stage:** targeted §1.1–1.2 and original abstract, main capacity tables/proofs not full-read. Optimization/capacity control, formation.

- **Prior problem:** observed recurrent-architecture advantages can arise from storing task information in weights, history in state, or trainability rather than unique primitives.
- **Solution:** separately stress parameter/task and hidden-state/history capacity across architectures/depths with intensive hyperparameter optimization.
- **Mechanisms/learning/units:** controlled recurrent tasks, Gaussian-process tuning, fixed parameter envelopes with differing hidden widths; synthetic sequences and recurrent units, not a modern language-model capacity theorem.
- **Evidence/control:** §1.2 holds parameter budgets approximately fixed, chooses width accordingly, and reports hundreds–thousands of complete training runs per condition; original abstract describes similar measured capacities despite training-difficulty differences.
- **Distinguishes:** nominal parameters vs state width/useful capacity; inability to optimize vs representational impossibility.
- **Cost/limits:** source calls total expense CPU-millennia. Empirical “~5 bits per parameter” and “one real number per unit” are task/protocol observations, not finite-precision universal storage bounds. The expensive search is a methodological anchor, not a local execution recommendation.

<a id="a07-n01"></a>
## A07-N01 — Turnip: Tokenizers Are Secretly Context Compressors for Transformers

Canonical cluster **BR-A07-N01**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Specific prior problem:** a fixed tokenizer fixes context compression, whereas byte models must decide how much local information to package before an expensive Transformer consumes it.
- **One-sentence proposed solution:** formulate tokenization as constrained predictive compression and introduce a context-dependent neural tokenizer pipeline integrated with existing language models (author claim from official indexed abstract, not a verified theorem/implementation).
- **Borrowed AI mechanisms / learning:** neural encoding, an entropy model and a Transformer language model/decoder are explicitly mentioned by the PDF index; one indexed passage says encoder/entropy run on every byte and LM/decoder on every token. Exact objective, estimator, discrete representation, cache and teacher requirements are **unread**. Do not infer that it is simply H-Net with another router.
- **Units / visibility:** byte front end and compressed internal units are supported; exact output alphabet, compression reversibility, prefix-stability and supervision units remain unknown.
- **Evidence depth:** M-index + S-index only; original full text inaccessible here. No reported performance number is adopted.
- **Hypothesis distinguished:** whether the chief bottleneck is a fixed lexical interface/context-compression objective rather than unavailable source memory. Need comparison against fixed patches, external entropy boundaries and learned boundaries at matched persistent count and compute.

<a id="a07-n02"></a>
## A07-N02 — MRT: Regularizing Tokenization with Morphology for Low-Resource Indic Languages

Canonical cluster **BR-A07-N02**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** corpus-statistics-only BPE/Unigram/WordPiece can produce tokens crossing morpheme boundaries in low-resource Indic languages.
- **Proposed solution:** regularize tokenizer construction with morphology rather than optimize corpus compression alone; the exact regularizer and data source are not yet read.
- **Mechanisms / learning:** subword segmentation plus morphology-based prior; indexed PDF mentions nine Indic languages, tokenizer-invariant BPC and downstream POS probes. Morphological supervision, lexicon/parser requirements and low-resource leakage must be extracted, not guessed.
- **Units / visibility:** surface text → subword units → LM/probe output, apparently not a pure byte-to-byte system. The paper cites MYTE, but citation is not evidence that its own input is morphology-encoded bytes.
- **Depth:** S-index; no experiment table/full read.
- **Distinguishes:** linguistic boundary supervision vs sequence-length/compression advantage, with MYTE and learned task-driven boundaries as different controls.

<a id="a07-n03"></a>
## A07-N03 — Separating Script and Vocabulary Effects in Multilingual Tokenization Cost

Canonical cluster **BR-A07-N03**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** cross-language token bills conflate script/orthographic compactness with learned vocabulary allocation.
- **Proposed solution:** separately analyze script and vocabulary contributions to multilingual tokenization cost (author framing from title/indexed passages).
- **Mechanisms / learning:** diagnostic accounting of characters/tokens and orthography, not a verified new neural architecture. Exact counterfactual intervention and parallel-text controls unknown. An indexed passage references fifteen languages; sample composition is unread.
- **Units / visibility:** characters, tokens and cross-language text spans; bytes vs codepoints vs graphemes must be recovered explicitly.
- **Depth:** S-index. No causal attribution or numeric effect adopted.
- **Distinguishes:** “byte coverage makes languages fair” from “the script itself changes positions per semantic content,” independently of source access.

<a id="a07-n04"></a>
## A07-N04 — Compiled Tokenizers: Training Language Models on Schema-Specific Action Spaces

Canonical cluster **BR-A07-N04**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** generic language vocabularies are not aligned with a schema-specific output action space, such as legal SQL identifiers/types.
- **Proposed solution:** Type-Constrained Tokenization compiles a database schema into tokenization and training (official PDF indexed description).
- **Mechanisms / learning:** schema/type constraints and a learned LM; exact interaction with constrained decoding, tokenizer recompilation, embedding initialization and task supervision is unread. Do not attribute an unspecified grammar engine or guarantee.
- **Units / visibility:** text/question and schema-specific actions; hybrid structured-output interface, not demonstrated byte-native generation. A schema known before decoding is privileged task information, not future target text.
- **Depth:** M-index + S-index; no full text or table verification.
- **Distinguishes:** task-aligned output coding vs more latent capacity or retrieval. Important for exact identifiers and host/interface transfer, not a generic language-model leaderboard comparison.

<a id="a07-n05"></a>
## A07-N05 — PriorBPB: Reducing the Target Length Confound of Bits-per-Byte While Improving Accuracy Prediction

Canonical cluster **BR-A07-N05**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** changing the denominator from tokens to UTF-8 bytes does not eliminate answer-length confounds or the difference between mean per-item ratios and corpus BPB.
- **Proposed solution:** estimate a marginal per-byte cost curve and integrate it under one shared length prior instead of each task's length distribution.
- **Mechanisms / learning:** a statistical evaluation operator, not a trained byte compressor. The [public research blog, 2026-10-13](https://aleph-alpha.com/en/blog/priorbpb/) was read (P); it explains least-squares overhead/rate decomposition, per-byte accumulation and a shared survival-weighted prior. This is **not full reading of either paper edition**.
- **Evidence / controls:** blog explicitly contrasts a task-local prior, corpus BPB and mean-of-ratios; it notes survivorship bias and residual dependence on the selected prior. Its claim of closer accuracy correlation across model families is author-reported. Template mismatch is a hypothesis, not established cause. Its text labels the geometric parameter using both mean/median language; exact parameterization must be checked in the original paper before implementation.
- **Units / visibility:** teacher-forced gold-answer token surprisals redistributed over answer bytes. A byte denominator does not make the numerator a marginalized string probability; combine with BIW-0080, do not substitute one fix for the other.
- **Depth:** M-index + P public blog; official full paper blocked; same-ID title change/discrepancy unresolved.
- **Distinguishes:** a seeming loss/accuracy or inverse-scaling anomaly due to metric composition from a genuine loss of usable content. Does not alone measure necessary use of memory.

<a id="a07-n06"></a>
## A07-N06 — ByteMark: A Unified Byte-Level Watermark for Detection Across Language Models

Canonical cluster **BR-A07-N06**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** a detector whose signal depends on one model's token IDs or embedding pipeline may fail when the source tokenizer/model is unknown.
- **Proposed solution:** define the keyed watermark signal over the published UTF-8 byte stream so one detector can read outputs of heterogeneous participating tokenizers.
- **Mechanisms / learning:** keyed pseudorandom byte-context selection and candidate-token logit bias; a byte-level public carrier, **not retraining the model as a byte LM**. Selected original [v1 HTML §3.1–3.2](https://arxiv.org/html/2610.14427v1) was read; only experiment/limitation search passages were inspected, not the full evaluation.
- **Controls / limits:** tokenizer/embedding replacement and participating-model continuation are author-reported tests; non-participating rewriting and shared-key exposure are explicit limitations. No security proof certified, no general robustness or byte-model language-quality claim.
- **Depth:** A + P + M-index. v1 date 2026-10-10 is verified in history.
- **Distinguishes:** an interface invariant at the public string level from apparent representation transfer tied to hidden/token coordinates. Adjacent to host-transfer evaluation, lower priority than core LM mechanisms.

<a id="a07-n07"></a>
## A07-N07 — Why Pretraining Fails to Share Cross-Lingual Knowledge

Canonical cluster **BR-A07-N07**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** multilingual models may acquire knowledge separately across languages even during pretraining.
- **Proposed solution:** diagnose with bilingual pretraining on identical language/text/segmentation mapped into disjoint token spaces, then test simple word-wise translation into a shared space.
- **Mechanisms / learning:** controlled next-token pretraining of 360M/7B models, synthetic vocabulary remapping and a word-wise alignment intervention (primary abstract). This is a vocabulary-overlap/control route, not source retrieval or a learned byte segmenter.
- **Units / visibility:** identical source text/segmentation with shared vs disjoint token IDs; downstream cross-lingual knowledge probes. Effective text exposure, initialization, tied heads, translation resource and evaluation construction need the full original.
- **Evidence:** [v1 abstract/history](https://arxiv.org/abs/2609.19291) retrieved. “Up to 12.6% of native learning efficiency / 14× baseline” is an **author abstract claim**, not independently table-checked and not adopted as a universal transfer law.
- **Depth:** A + M-index, not FULL. Venue-posting and arXiv dates differ legitimately.
- **Distinguishes:** lexical input/output code partition as a cause of compartmentalization vs lack of semantic memory capacity; synthetic identical-text controls make this unusually high-priority for interface hypotheses.

<a id="a07-n08"></a>
## A07-N08 — Who Gets a Token, and What Does It Carry? Unequal Name Support and Concept Access in Large Language Models

Canonical cluster **BR-A07-N08**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** socially matched names need not be lexically comparable model inputs; one may be atomic while another requires composition.
- **Proposed solution:** map atomic name support and use NameTrace to measure task-aligned concept accessibility and downstream leverage on matched names.
- **Mechanisms / learning:** [v1 original §§1–4 selected passages](https://arxiv.org/html/2609.34065v1): tokenizer mapping; logistic access analysis; centered-kernel-alignment geometry; model-probability readout over weighted adjective axes; matched development/evaluation split. Later hidden-state interventions are reported by the abstract but their full protocol was not read.
- **Evidence:** §2 reports 497,583 single-word name surfaces, 12 tokenizers, representation experiments on 200 matched pairs across eight strata. §4 explicitly says name-specific pretraining exposure is unobserved and **does not isolate atomicity causally**. Do not turn a matched observational association into proof that one extra token causes a social outcome.
- **Units / visibility:** name strings, tokenization, hidden-layer task directions and constrained downstream choices. Not byte-native training; intervention use/access must not be conflated with normal deployed readout.
- **Depth:** A + P; S-index venue lead only. No original FULL.
- **Distinguishes:** lexical access vs usable conceptual representation vs final output leverage, with an explicit observational/causal boundary useful for the deployed-use axis.

<a id="a07-n09"></a>
## A07-N09 — GlitchPatch: Repairing Glitch Tokens in Frozen Language Models via Local Retokenization

Canonical cluster **BR-A07-N09**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** global BPE merge deletion can fix bad tokens but damage normal tokens sharing intermediate merge nodes; frozen models cannot easily accept internal repairs.
- **Proposed solution:** find behaviorally validated replacement token-ID paths offline, then locally substitute only matched anomalous tokens in canonical token sequences at runtime.
- **Mechanisms / learning:** Behavioral Path Optimization, equivalent string-preserving tokenizations, graph/path proposal search and behavioral validation, followed by a compiled lookup table; no model-parameter/activation modification. Primary [v1 abstract/history](https://arxiv.org/abs/2610.04399) and selected [HTML §§1–3 opening / §2](https://arxiv.org/html/2610.04399v1) were read; full algorithm and evaluations remain unread. A final extraction passage also explicitly distinguishes graph proposal cost from full-context model log probability.
- **Evidence / counterexample:** abstract reports non-monotonic fix rate with decomposition granularity and monotonic collateral damage for global edits, motivating local rather than “always split more.” Ten-model/six-tokenizer/85.10% fix figures are **abstract claims**, not checked tables. A 0% regression result is tied to the defined test, not all future inputs.
- **Units / visibility:** same published bytes, different input token-ID sequence; frozen LM output remains normal tokens. Offline behavioral search cost and rule match runtime must both be counted.
- **Depth:** A + P; official venue PDF/forum full retrieval blocked.
- **Distinguishes:** input path/interface defects repairable without new latent storage from host semantic incapacity. Pair with learned retokenization and unchanged-canonical-input controls.

<a id="a07-n10"></a>
## A07-N10 — Learning to Retokenize: Improving Downstream Performance of Frozen Language Models

Canonical cluster **BR-A07-N10**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** a frozen LM's canonical deterministic segmentation may be suboptimal for downstream tasks, especially character-sensitive ones.
- **Proposed solution:** learn a retokenization policy for a frozen host (title/indexed table-level claim), rather than assume model weights must change.
- **Mechanisms / learning:** exact estimator, reward, training set, search strategy, allowable token paths and training/inference budgets **not established**. No claim that it uses REINFORCE simply because BIW-0078 does.
- **Units / visibility:** equivalent input token paths and frozen language model, exact byte preservation and output contract still need original verification. Indexed Table 1 compares canonical/hand-designed/learned tokenization; its cells were not read.
- **Depth:** S-index only; no abstract/full paper certification.
- **Distinguishes:** improving input composition at fixed host parameters from changing encoder/decoder learning dynamics; compare local GlitchPatch vs global task-adaptive retokenization under the same search budget.

<a id="a07-n11"></a>
## A07-N11 — BridgeSTOP: Bridging Streaming Tokenization and LLM Prefill

Canonical cluster **BR-A07-N11**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** streaming tokenizer efficiency may not propagate into actual language-model prefill efficiency.
- **Proposed solution:** bridge streaming tokenization and prefill rather than optimize tokenizer sequence shortening in isolation (indexed original statement).
- **Mechanisms / learning:** system-level streaming/prefill coordination. Exact tokenizer algorithm, KV invalidation/reuse, scheduling and learning requirements unread; do not attribute a specific kernel or claim a measured speedup.
- **Units / visibility:** arriving text chunks, tokenizer outputs and prefill states. Prefix revisions, delayed boundaries and partial UTF-8 handling are central missing contracts.
- **Depth:** S-index only; PDF fetched but challenged; no arXiv match established.
- **Distinguishes:** apparent compression benefit from true end-to-end latency benefit; source retention is not necessary to frame this failure mode.

<a id="a07-n12"></a>
## A07-N12 — LEAD: Models Know the Language, but Token Preferences Do Not Always Follow

Canonical cluster **BR-A07-N12**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** knowing a requested language need not align next-token preferences with that language, especially when tokens end partway through multibyte characters.
- **Proposed solution:** a language-aware token-preference intervention named LEAD; the actual intervention rule, expansion of the acronym and training requirements remain unread and must not be invented.
- **Mechanisms / learning:** indexed PDF explicitly identifies **left partial units**, byte sequences beginning but not completing a multibyte character, and includes a code-switching impact table. Exact filtering/logit treatment and language detector are unknown.
- **Units / visibility:** token candidates, UTF-8 partial units, language preference and legitimate code-switching. Not sufficient to classify as byte-native generation or a universal validity constraint.
- **Depth:** S-index only; date/current state unknown.
- **Distinguishes:** output legality/local completion preference from semantic-language competence and long-range memory consumption. Needs legitimate code-switching and script-balanced controls.

<a id="a07-n13"></a>
## A07-N13 — Constructive Prediction: The Role of Lexical Code Organization in Language Modeling

Canonical cluster **BR-A07-N13**. [Carrying record](../01_discovery/A07/WORKS_AND_PROBLEMS.md).

- **Prior problem:** title indicates lexical code organization in language modeling; indexed abstract begins “Character …”. Exact problem is **not established**.
- **One-sentence solution:** **unknown until original accessible abstract/method is read**; no architecture claim inferred from the title.
- **Mechanisms, units, learning source, costs, controls:** unknown. Character/interface relevance is provisional; could be excluded after triage.
- **Depth:** S-index title/header only. Listed for recoverability, not counted as a substantive verified mechanism or architecture alternative.
- **Hypothesis to test for relevance:** whether coding/lexical representation can change compositional prediction without changing persistent memory; this is our triage question, not the paper's established finding.

<a id="a08-v01"></a>
## A08-V01 — How Linear Attention Remembers

Canonical cluster **BR-A03-D20**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V01 | Shared recurrent storage makes it unclear where facts are written, retained and consumed → analytically decompose memory and intervene on writes/read pathways. | Pretrained GLA/GDN; causal editing and pathway analysis of learned state. | Claims load harms recall/editability more than elapsed context in the tested range, with cross-fact coupling; hybrid recall shifts to full-attention KV. Distinguishes **interference vs elapsed-time decay**, and **hybrid rescue vs recurrent-path use**. Intervention selectivity and natural wrong-value controls unverified. |

<a id="a08-v02"></a>
## A08-V02 — Linear Attention lacks Incentive for Associative Recall, not Capacity

Canonical cluster **BR-A08-V02**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V02 | Similar LM loss masks a precise prefix-matching recall deficit → change pretraining repetition while retaining architecture, token count and optimization-step count. | In-context repetition; training-distribution design, synthetic MQAR capacity scaling. | Claims large latent recall capacity and improved recall at slight general-LM cost. Distinguishes **training incentive vs insufficient nominal state**. Same tokens/steps is not established same FLOPs, data information, or semantic generalization. |

<a id="a08-v03"></a>
## A08-V03 — Kronecker Delta Rule for Long Context Linear Attention

Canonical cluster **BR-A02-N05**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V03 | Delta-rule correction can disturb unrelated stored associations → correct a scalar key–value association along one matrix-space direction. | Kronecker/rank-one memory revision, xLSTM-style linear recurrence; learned slow projections. | Claims bounded expected norm and reduced interference. Distinguishes **update geometry vs larger memory**. Norm stability does not prove fact retention or use; assumptions and same-state-bit comparisons require body. |

<a id="a08-v04"></a>
## A08-V04 — SDG: State-Dependent Gating at Chunk Boundaries for Linear Attention

Canonical cluster **BR-A08-V04**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V04 | Token-only gates cannot condition forgetting on what memory already holds → derive chunk-boundary elementwise gates from the change in state. | State feedback plus chunk-parallel recurrence; ordinary LM pretraining. | Claims gains across GDN/KDA/GDN-2/Mamba-3 and a fixed-gate proximal interpretation. Distinguishes **write-time token relevance vs memory-aware forgetting**. Gate computation and chunk-boundary causality need inspection. |

<a id="a08-v05"></a>
## A08-V05 — Fast Weights in Fast Weights: Towards Bridging Parallel and Sequential Test-Time Learning

Canonical cluster **BR-A08-V05**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V05 | Chunk-parallel test-time training ignores earlier within-chunk updates → combine chunk-level first-layer fast weights with exact token-level output-memory updates and feature transport. | Backward-error/Hessian–gradient analysis; delta rule, WY solve, causal linear-attention feature transport. | Claims improvements over LaCT at 340M–1B and a feature-transport ablation. Distinguishes **inner-update approximation error vs memory function class/capacity**. Small-step expansion is not arbitrary-step exactness; count inner states/compute. |

<a id="a08-v06"></a>
## A08-V06 — GABA: Geometry-Aware Bilinear Attention for Linear Transformers

Canonical cluster **BR-A08-V06**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V06 | Enlarging state leaves an output-channel-shared contraction bottleneck → use output-conditioned low-rank bilinear readout and constrained global/local fusion. | Bilinear attention, low-rank refinement and contrast-guided branch interactions; supervised vision training. | Claims ImageNet gains with essentially unchanged model FLOPs. Distinguishes **readout geometry vs stored amount**. Bidirectional vision is a transfer hypothesis, not a causal byte-LM result; isolate its two changes. |

<a id="a08-v07"></a>
## A08-V07 — On State Reduction in Linear Attention

Canonical cluster **W0086**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V07 | Trained recurrent states may underuse nominal rank → structurally prune query/key matrices using rank-revealing QR. | Post-training structured pruning; theoretical K/V rank analysis. | Claims halved state with minor next-token degradation. Counterexample candidate to **low rank necessarily being the active bottleneck**. Average NTP may hide rare exact-detail harm; pair with recall-specific and precision tests. |

<a id="a08-v08"></a>
## A08-V08 — RunningTensor: Generalizing Linear Attention to Higher-Order Recurrent States

Canonical cluster **BR-A08-V08**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V08 | A matrix state only stores second-order interactions → update a higher-order tensor and read it using multiple query contractions. | Tensor outer products, recurrent/parallel forms; synthetic recall and time-series training. | Claims order-three proof-of-concept gains. Distinguishes **representation order vs one-vector query limitations**. State grows as W^o; equal width is not equal bytes or memory capacity. |

<a id="a08-v09"></a>
## A08-V09 — Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling

Canonical cluster **BR-A02-N03**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V09 | Increasing state with full new projections is costly → add a second key/query axis with two projections and retain gated/delta chunk training. | Triadic outer-product fast weights; two-query readout. | Claims improved long-context LM/recall against other enlargement schemes. Distinguishes **parameter-efficient state allocation vs simply more state**. Match total state, optimizer state and bandwidth, not only parameter count. |

<a id="a08-v10"></a>
## A08-V10 — Sliced-Linear Attention: Beyond the Finite-Feature Bottleneck of Linear Attention

Canonical cluster **BR-A08-V10**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V10 | Fixed finite-feature kernels impose a rank bottleneck → multiply by a learned one-dimensional Laplace interaction computed by sorting/scans. | Kernel design, associative retrieval, quasi-linear algorithms. | Claims sharp finite-key retrieval and a continuous recurrent dimension lower bound. Distinguishes **kernel-feature rank vs fixed-memory universality**. Sorting/scans may require context-dependent retained information; do not label constant-state from near-linear time. |

<a id="a08-v11"></a>
## A08-V11 — LoopLA: Causal State Refinement for Looped Linear Attention

Canonical cluster **BR-A08-V11**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V11 | Looped layers do not necessarily refine their recurrent memory across passes → carry and consolidate state across tokens and loops with causal draft-and-consolidate. | Jacobi-style approximation and chunk commits; 1B GDN trained on 100B tokens. | Abstract explicitly says matched-parameter improvement but **slightly weaker overall at matched FLOPs**, with some long-context advantage. Counterexample to **extra iteration being a free architectural gain**. Extra passes must not gain future visibility. |

<a id="a08-v12"></a>
## A08-V12 — SURCO: Survivor Compensation for Recurrent-State Pruning of State Space Models

Canonical cluster **BR-A08-V12**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V12 | Pruning removes directions without compensating surviving readouts → solve output-space least squares after fixing the mask and allocate state by layer. | Gram/conditional-necessity analysis; closed-form readout reweighting, post-training calibration. | Claims better retained quality and physically materialized throughput/memory gains. Distinguishes **lost state vs recoverable readout mismatch**. Training-free is not calibration-free; reconstruction of dense outputs is not proof of native content preservation. |

<a id="a08-v13"></a>
## A08-V13 — Cross-Model Stitching Transfers Answers, Not Computation

Canonical cluster **BR-A08-V13**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V13 | Stitching success is interpreted as transferred computation → test answer presence, source depth and serial answer-token production across donor/recipient pairs. | Task-supervised linear activation mapping; frozen-model grafting and ablations. | Claims transferred precomputed answers, not measurable transfer of producing computation, with redundant high-dimensional encoding of low-rank signal. Distinguishes **answer-channel compatibility vs mechanism compatibility**. Gold-label supervision and donor answer availability are stronger permissions than ordinary component transfer. |

<a id="a08-v14"></a>
## A08-V14 — Receiver State Shapes Functional Compatibility: Internal Message Adaptation for Model Stitching

Canonical cluster **BR-A08-V14**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V14 | Equal baseline accuracy is taken to imply equal receiver compatibility → perturb receiver states and adapt internal attention messages with frozen models/stitch. | Receiver-conditioned CLS-message adaptation; parameter-efficient vision adaptation. | Claims 0.02M-parameter recovery and parameter-matched controls. Distinguishes **receiver state × mismatch interaction vs source defect**. Vision CLS pathways do not transfer verbatim to causal LMs; check self-stitch and matched damage. |

<a id="a08-v15"></a>
## A08-V15 — The Role of Data-Reuse on Shortcut Learning with Linear Networks

Canonical cluster **BR-A08-V15**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V15 | Population-gradient dynamics omit finite-dataset reuse → model shortcut/core/sample-specific learning under repeated full-batch updates. | Linear networks, non-rigorous dynamical mean-field approximation, ridge regularization. | Explicitly non-rigorous theory; ridge may suppress an interpolation peak yet increase shortcut/core ratio. Distinguishes **smooth loss/generalization changes vs actual core acquisition**. Finite-data linear regimes are not a universal deep-LM theorem. |

<a id="a08-v16"></a>
## A08-V16 — Farsighted Correction of Shortcut Learning: From Dynamic Starvation to Confidence-Gap Optimization

Canonical cluster **BR-A08-V16**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V16 | Falling loss conceals starvation of desired features → reinject counterfactual causal gradients or confidence-gap proxies. | Empirical neural tangent kernel, trajectory analysis and counterfactual auxiliary objectives. | Claims dynamic-starvation bounds and competitive six-benchmark results. Distinguishes **objective satisfied by shortcut vs target mechanism formed**. Verify theorem assumptions, proxy exactness, required groups/counterexamples and budget before recommending a method. |

<a id="a08-v17"></a>
## A08-V17 — Uncovering Latent Reasoning Strategies in Language Models

Canonical cluster **BR-A08-V17**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V17 | A pretrained generator can reproduce responses without a new latent route → weight variational reconstruction pressure by base-model surprisal/information gain. | Latent-variable router/generator, variational objectives, multi-strategy algorithmic benchmark. | Claims strategy-aligned codes and active latent exploration. Distinguishes **decoder bypass/objective incentive vs latent capacity**. Strategy labels, answer-token visibility and preservation of base distribution require body; VAE collapse is not automatically deterministic-memory collapse. |

<a id="a08-v18"></a>
## A08-V18 — Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval

Canonical cluster **BR-A08-V18**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V18 | Never-retrieved memories have unidentifiable utility → reserve retrieval slots for randomized memories with known propensities. | Causal positivity, balanced retrieval interventions, inverse propensity weighting. | Claims utility identification improves but identified per-query utility does not decide retention. Distinguishes **retriever omission vs content uselessness**, and **current utility vs future retention value**. The abstract's self-normalization/unbiasedness language needs exact estimator checking. This is external-store methodology, not a closed-state solution. |

<a id="a08-v19"></a>
## A08-V19 — When Errors Become Memories: Causal Pathway Tracing in Multi-Turn Memory-Augmented LLMs

Canonical cluster **BR-A08-V19**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V19 | Response-only evaluation misses latent propagation of earlier errors → separate memory-update and question-feedback paths using four counterfactual trajectories. | Dynamic structural causal model, paired restoration and probability/probe/natural-response measurements. | Claims errors persist after disappearing from natural responses and joint repair reduces residual propagation. Distinguishes **stored trace vs natural behavior**, **memory path vs feedback path**. Cross-world validity, interaction background and non-target effects are unread. |

<a id="a08-v20"></a>
## A08-V20 — Exact Finite-Query KV Cache Compilation

Canonical cluster **BR-A08-V20**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V20 | Successful fitted compression does not certify minimum slots → characterize exact output preservation on a finite protected query set. | Affine geometry of attention-ratio constraints; query-aware cache compilation. | Claims conditional slot laws and exact protected-token continuation in FP32. Distinguishes **finite known-query sufficiency vs arbitrary future-query preservation**. Known trace/query rank and realizability are substantive permissions; no unknown-query guarantee. |

<a id="a08-v21"></a>
## A08-V21 — Where You Put Attention Matters More Than How Much You Use: Attention Placement in Hybrid Sequence Models

Canonical cluster **BR-A08-V21**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V21 | Hybrid comparisons vary how much attention, not where → compare attention placement with fixed six-block parameter count and post-training removal. | Hybrid recurrent/attention composition; parity, ordered group task and MQAR. | Claims placement affects tasks differently; attention removal barely changes parity but destroys recall. Distinguishes **formation scaffold vs inference-time resource**, **placement interaction vs quantity**. Equal parameters does not establish equal all-resource budgets. |

<a id="a08-v22"></a>
## A08-V22 — When Routing Must Be Right: Irreversible Lock-In in Attention Routing

Canonical cluster **BR-A08-V22**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V22 | Router failures are blamed only on top-k nondifferentiability → shift the timing of identical correct-routing windows and measure marginal utility during formation. | Synthetic MQAR, oracle routing windows, REINFORCE and training-history interventions. | Claims early lock-in despite unbiased routing gradient and a long stable correct router that does not recover performance. Distinguishes **missing early utility signal vs insufficient capacity/discrete gradient alone**. Oracle timing, later recovery budget and negative mechanism prediction require full text. |

<a id="a08-v23"></a>
## A08-V23 — LinQuant: Functional Invariances for Low-Precision Linear Recurrences

Canonical cluster **BR-A08-V23**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V23 | Native recurrent operands quantize poorly despite correct full-precision formulas → apply function-preserving rotations/rescalings/factor placements before low-precision prefill. | Seven algebraic invariances; SSDi8 augmentation and recurrent-kernel quantization. | Claims better PPL at matched latency on Mamba-2/Nemotron-H. Distinguishes **numerical geometry vs semantic capacity**. Prefill quantization is not demonstrated long-horizon quantized-state retention or exact-detail recall. |

<a id="a08-v24"></a>
## A08-V24 — Predictive State Has a Scope

Canonical cluster **BR-A08-V24**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V24 | Shared states alias relation histories with different futures → share update rules but keep pair-addressed recurrent state. | Temporal graph forecasting, random-effects/Bayes-risk analysis, frozen-bank address derangements. | Claims predictive benefits and address–content correspondence effects. Distinguishes **state scope/aliasing vs shared update quality**. Address cardinality grows with pairs; not fixed total memory or source revisit. |

<a id="a08-v25"></a>
## A08-V25 — Understanding the Predictive-State Bottlenecks of Transformer Models

Canonical cluster **BR-A08-V25**. [Carrying record](../01_discovery/A08/WORKS_AND_PROBLEMS.md). **Author abstract claims only; no body read.**

| V25 | Latent-state count is confused with predictive dimension → separate them in hidden-Markov generators and control width, readout and causal belief-subspace interventions. | Exact filtering constructions, predictive-state rank, calibrated probes and spectral training analysis. | Claims near-Bayes width transition tracks predictive rank and low-variance modes are suppressed below it. Distinguishes **task-sufficient rank vs arbitrary historical detail/rank**, **capacity vs output parameterization**. Controlled contractive HMMs do not certify language state learning. |

## Persistent restriction navigation

[Old claim restrictions](../../flued_multigranularity_survey_20261108/05_review/CLAIM_RESTRICTIONS.md) and [byte evidence status](../../byte_language_interface_survey/02_inventory/EVIDENCE_STATUS.md) retain source-scoped restrictions. No new FULL or experimental result is produced here.

## R2 byte6 source-screened records —not FULL or final synthesis

Original metadata/abstract only,official API-observed active2027 Submission note2. Body untested/unread,actual PDF edition unknown;authors remain anonymous. Mechanism descriptions below are attributed abstract proposals,not independently verified findings. V17 must recover the originals.

<a id="r2-t01"></a>
### BR-R2-T01 —Tokenization with Formal Guarantees: From Optimal Compression to Provable Bounds

- Stable source:`openreview:FXLPTx7osi`;official note2,modified2026-10-05T20:36:04.382+00:00,active Submission#38781;[R2 audit](../05_review/ICLR2027_SOURCE_AUDIT_R2.md).
- Actual body route:https://openreview.net/pdf/009f6f39ae30a457c722ce02faa53ee551f4b3b2.pdf;reference only,not acquired/hash-verified/full-read.
- Prior problem:Heuristic vocabulary compression lacks optimization certificates.
- One-sentence proposed solution/borrowed technique:Author abstract proposes graph-flow mixed-integer formulation and shortest-path/Lagrangian relaxation.
- Learning source/estimator,units/visibility,controls,full results/cost/failure/transfer conditions:**unknown at body depth** until actual original read.
- Precise evidence question:Recover exact objective,overlap constraints,bound quantifiers,solver/scale budget and any demonstrated LM link;compression bound is not task sufficiency.
- Source question links and minimum read:[V17](batches/V17.md);do not turn abstract novelty into an architecture conclusion.

<a id="r2-t02"></a>
### BR-R2-T02 —Stochasticity in Tokenization Improves Robustness

- Stable source:`openreview:rIRkUxOleG`;official note2,modified2026-10-05T17:31:08.512+00:00,active Submission#6777;[R2 audit](../05_review/ICLR2027_SOURCE_AUDIT_R2.md).
- Actual body route:https://openreview.net/pdf/1772373f12cb1a74c048ab6d50f1f991ce2efe96.pdf;reference only,not acquired/hash-verified/full-read.
- Prior problem:Canonical segmentation can create alternate-tokenization brittleness.
- One-sentence proposed solution/borrowed technique:Author abstract proposes stochastic-tokenization training/fine-tuning and perturbation tests.
- Learning source/estimator,units/visibility,controls,full results/cost/failure/transfer conditions:**unknown at body depth** until actual original read.
- Precise evidence question:Recover sampling support/distribution,exact byte preservation,clean-score negatives and exposure/length/compute controls.
- Source question links and minimum read:[V17](batches/V17.md);do not turn abstract novelty into an architecture conclusion.

<a id="r2-t03"></a>
### BR-R2-T03 —Online Tokenization with Optimal Delay in Near Linear Time

- Stable source:`openreview:8D7l5sK3YT`;official note2,modified2026-10-05T18:30:48.591+00:00,active Submission#11755;[R2 audit](../05_review/ICLR2027_SOURCE_AUDIT_R2.md).
- Actual body route:https://openreview.net/pdf/0bbbe6b331327aade7b400fca6d0369486be8e44.pdf;reference only,not acquired/hash-verified/full-read.
- Prior problem:Sequential tokenization delays streaming emission.
- One-sentence proposed solution/borrowed technique:Author abstract proposes online tokenization with low-delay guarantees.
- Learning source/estimator,units/visibility,controls,full results/cost/failure/transfer conditions:**unknown at body depth** until actual original read.
- Precise evidence question:Recover comparator/assumptions,adversarial prefixes,flush,partial UTF8,memory and real pipeline latency;title does not imply prefill gain.
- Source question links and minimum read:[V17](batches/V17.md);do not turn abstract novelty into an architecture conclusion.

<a id="r2-t04"></a>
### BR-R2-T04 —Tokenization Invariance Is Learned Late and Broken at the Head

- Stable source:`openreview:63kZK7oyd6`;official note2,modified2026-10-05T20:03:19.716+00:00,active Submission#26364;[R2 audit](../05_review/ICLR2027_SOURCE_AUDIT_R2.md).
- Actual body route:https://openreview.net/pdf/8a0a3f08c5029077beebbbec230c64d1e99015ae.pdf;reference only,not acquired/hash-verified/full-read.
- Prior problem:Retokenization failures may differ across trunk and output head and training time.
- One-sentence proposed solution/borrowed technique:Author abstract proposes checkpoint probes,mean correction and head-versus-trunk adaptation.
- Learning source/estimator,units/visibility,controls,full results/cost/failure/transfer conditions:**unknown at body depth** until actual original read.
- Precise evidence question:Recover random/pooling/probe and equal-budget controls,source/label access,actual string probability,all-history and negative cases.
- Source question links and minimum read:[V17](batches/V17.md);do not turn abstract novelty into an architecture conclusion.

<a id="r2-t05"></a>
### BR-R2-T05 —Cross-Tokenizer On-Policy Distillation via Byte-Prefix Marginalization

- Stable source:`openreview:Mm5OLOPLT0`;official note2,modified2026-10-05T16:57:39.933+00:00,active Submission#1302;[R2 audit](../05_review/ICLR2027_SOURCE_AUDIT_R2.md).
- Actual body route:https://openreview.net/pdf/c32108ca1a8316863316036ebeb5e0f28ba8bee7.pdf;reference only,not acquired/hash-verified/full-read.
- Prior problem:Cross-tokenizer supervision may lose or misalign teacher probability mass.
- One-sentence proposed solution/borrowed technique:Author abstract proposes longest-student-prefix mapping with residual category and multi-teacher-token treatment.
- Learning source/estimator,units/visibility,controls,full results/cost/failure/transfer conditions:**unknown at body depth** until actual original read.
- Precise evidence question:Recover EOS/alphabet/history/partial bytes,exact-versus-bound assumptions and teacher costs;not automatically marked-EOT or unmarked-byte exactness.
- Source question links and minimum read:[V17](batches/V17.md);do not turn abstract novelty into an architecture conclusion.

<a id="r2-t06"></a>
### BR-R2-T06 —B-Net: Learning Where to Compress in Byte-Level Language Models

- Stable source:`openreview:fMymbXoq9T`;official note2,modified2026-10-05T20:20:16.031+00:00,active Submission#32922;[R2 audit](../05_review/ICLR2027_SOURCE_AUDIT_R2.md).
- Actual body route:https://openreview.net/pdf/a212af497989974b1ce9ae2bb4adeaf0419f4041.pdf;reference only,not acquired/hash-verified/full-read.
- Prior problem:Learned byte boundaries may miss realized target compression rates.
- One-sentence proposed solution/borrowed technique:Author abstract proposes causal-convolution scoring plus adaptive threshold control.
- Learning source/estimator,units/visibility,controls,full results/cost/failure/transfer conditions:**unknown at body depth** until actual original read.
- Precise evidence question:Recover controller timing/visibility,prefix legality,boundary/content/rate separability,all-state/compute and multilingual controls.
- Source question links and minimum read:[V17](batches/V17.md);do not turn abstract novelty into an architecture conclusion.
