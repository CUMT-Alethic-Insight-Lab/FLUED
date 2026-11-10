# A01 — Works, problems, mechanisms and discriminating hypotheses

2026-11-09. Local keys `A01-R01`–`A01-R21` identify discovery records, **not new global W IDs**. Existing W/BIW and old N aliases remain authoritative. Version variants are not counted as independent works. All public access events are in [SEARCH_LOG](SEARCH_LOG.md). This inventory is not a full-reading ledger.

## 1. Classification rules

- **Existing-W unread:** original paper is in the old W catalog, with no applicable FULL card found; this pass recovers the source but does not promote it to FULL.
- **Existing-audit lead:** one of the previous compression audit's six N records; new relative to that earlier W catalog, **not newly discovered today**.
- **Existing-BIW partial:** actual BIW record with partial primary-source scope, not a full card.
- **Catalog-absent candidate:** no stable-ID/title match in the two specified catalogs in this pass. Cross-stream dedup remains necessary; absence is not global novelty.
- **Evidence A:** official abstract/metadata only. **P:** explicitly selected original passages. **RF:** reuse of an actual existing scoped FULL card, retaining all its restrictions. **Blocked:** no original content acquired. Downloading/returning long HTML does not mean that it was all read.

The multidimensional labels are independent: a new source can have shallow evidence, a reused source can carry strong conditional evidence, and a relevant paper can still be unsuitable as a fixed-bit, query-unknown comparator.

## 2. Twenty-one externally recovered or newly verified works

### A01-R01 — W0067 — Optimal Multitask Representations Under a Rate Constraint: An Information Bottleneck Analysis

- **Identity:** [arXiv:2610.30493v1](https://arxiv.org/abs/2610.30493v1), 2026-10-21; [original HTML](https://arxiv.org/html/2610.30493v1). Nicholas Stiles and Gregory W. Wornell. **Existing-W unread**; no official venue acceptance verified; treat as preprint.
- **Prior problem:** an objective that exposes useful factors without a rate constraint may allocate a limited representation budget poorly across downstream tasks.
- **One-sentence solution:** formulate a multitask information bottleneck and compare rate-conditioned optimal covariance allocations with fixed Gaussian pretext objectives.
- **Borrowed mechanisms / learning:** Gaussian information bottleneck, covariance optimization and finite-bit neural bottlenecks with straight-through gradients; known task mixture supplies the relevance signal. Writer sees X, not task index; task-specific reader sees the index. Whole-vector content, no source lookup or local address hierarchy.
- **Evidence:** **A+P**, original §§2.1–2.3 definitions/Proposition 1, §§4–5 examples/Theorems 1–2, §6.1 setup/results and selected introduction. Main proofs, dSprites details and finite-bit appendix not fully read. Reoptimized heads/common frozen features and rate sweeps are relevant controls; five fitted seeds are stated for learned codes. Reported Gaussian and B-bit axes are not interchangeable with storage bytes.
- **Distinguishes:** fixed-objective ranking versus objective × rate interaction; task frequency versus precision; universal failure versus the bounded-SNR positive guarantee. Does not establish language-model deployment optimality.

### A01-R02 — old N02 — Autoencoding-Free Context Compression for LLMs via Contextual Semantic Anchors (SAC)

- **Identity:** [arXiv:2510.08907v4](https://arxiv.org/abs/2510.08907v4), 2026-03-11, first version 2025-10-10; [v4 HTML](https://arxiv.org/html/2510.08907v4); [official ICLR 2026 proceedings entry](https://proceedings.iclr.cc/paper_files/paper/2026/hash/dff28796c79e1a04c7a6182119ee899a-Abstract-Conference.html). **Existing-audit lead**. Proceedings entry verifies ICLR 2026 publication; formal PDF versus arXiv v4 not compared. Not an ICLR 2027 submission claim.
- **Prior problem:** appended learned compression tokens and full-source reconstruction may be poorly aligned with downstream use.
- **Solution:** select original context tokens as marked anchors, encode bidirectionally and expose their per-layer KV representations to a frozen decoder, trained with continuation and then QA rather than mandatory AE.
- **Mechanisms / learning:** LoRA encoder, shared anchor embedding, uniform chunk-middle selection, bidirectional attention, continuation pretraining and task-label fine-tuning. Writer encodes context without the later question. Persistent payload is per-layer KV, not merely K single-layer vectors; full-context attention during writing is not causal prefix streaming.
- **Evidence:** **A+P**, §§3–5 and surrounding ablation descriptions; Table 5 cells missing from extracted text. Original text reports architecture-specific AE disadvantage and mixed results in another architecture. Frozen target, same-data baseline recipe, anchor/mask/selection ablations are relevant, but full training-cost and numeric ablation audit remains open.
- **Distinguishes:** objective mismatch versus carrier/interface mismatch; learned boundaries necessary versus fixed anchors adequate in this setting. Gradient cosine near zero does not prove causally harmful interference.

### A01-R03 — old N06 — Fixing a Broken ELBO

- **Identity:** [ICML 2018/PMLR 80:159–168](https://proceedings.mlr.press/v80/alemi18a.html); [formal PDF](https://proceedings.mlr.press/v80/alemi18a/alemi18a.pdf). Alemi et al. **Existing-audit lead**, published conference paper; no arXiv/formal version merge performed.
- **Prior problem:** maximizing marginal likelihood or its evidence lower bound does not uniquely select a useful latent representation.
- **Solution:** characterize rate–distortion tradeoffs and constrain information rate to select latent behavior that ELBO alone leaves unspecified.
- **Mechanisms / learning:** variational information bounds, stochastic latent encoder/decoder, controlled rate rather than a single scalar ELBO score. Reconstruction is the training signal; no retrieval addresses or later-query model established by this abstract.
- **Evidence:** **A**, official abstract and bibliographic record only. It explicitly reports identical-ELBO families with different latent properties and powerful-decoder examples; exact constructions and experimental controls are queued, not verified here.
- **Distinguishes:** good generative score versus informative/useful latent code; objective degeneracy versus merely training an encoder longer. Does not prove equal ELBO means equal reconstruction or equal task utility.

### A01-R04 — old N01 — Rethinking Minimal Sufficient Representation in Contrastive Learning

- **Identity:** [CVPR 2022 formal page](https://openaccess.thecvf.com/content/CVPR2022/html/Wang_Rethinking_Minimal_Sufficient_Representation_in_Contrastive_Learning_CVPR_2022_paper.html), pp.16041–16050; [formal PDF](https://openaccess.thecvf.com/content/CVPR2022/papers/Wang_Rethinking_Minimal_Sufficient_Representation_in_Contrastive_Learning_CVPR_2022_paper.pdf). Wang, Guo, Deng and Lu. **Existing-audit lead**; published conference version, not a fresh reading of the arXiv variant.
- **Prior problem:** information shared by augmented views need not include all later-task-relevant information.
- **Solution:** retain additional input information as a regularizer rather than learning only the minimal view-shared representation.
- **Mechanisms / learning:** contrastive positive-view prediction and input-information regularization; augmentation supplies supervision, future task labels are unavailable. Whole-sample representation, not query-conditioned retrieval.
- **Evidence:** **A**, official abstract. The claim assumes non-shared task-relevant information; proofs, regularizer implementation, augmentation controls and matched training budgets remain unread.
- **Distinguishes:** sufficient for a pretext/view versus sufficient for an eventual task; augmentation-defined invariance versus task-universal retention. Not proof that every minimal sufficient statistic is harmful.

### A01-R05 — W0064 — Caveats for Information Bottleneck in Deterministic Scenarios

- **Identity:** [arXiv:1808.07593v4](https://arxiv.org/abs/1808.07593v4), 2019-02-08. **Existing-W unread**. Prior audit associates ICLR 2019; this pass verifies the arXiv abstract/history, not a formal venue decision.
- **Prior problem:** sweeping the ordinary IB Lagrange multiplier can fail to reveal the full IB curve when labels are deterministic functions of inputs.
- **Solution:** identify three caveats and propose an alternative functional capable of recovering the curve in those cases.
- **Mechanisms / learning:** information-bottleneck tradeoff analysis; known target Y, not unknown future queries. MNIST is the stated demonstration.
- **Evidence:** **A**, original abstract/history; near-deterministic extension and trivial-solution claims are author results pending full proof reading.
- **Distinguishes:** failure of a particular linear scalarization versus absence of informative compressed representations; estimated compression curves versus actual task-preservation mechanisms.

### A01-R06 — W0037 — Adapting Language Models to Compress Contexts (AutoCompressors)

- **Identity:** [arXiv:2305.14788v2](https://arxiv.org/abs/2305.14788v2), 2023-11-04; [PDF](https://arxiv.org/pdf/2305.14788v2). **Existing-W unread**. Original page explicitly says accepted to EMNLP 2023; formal-version comparison not done.
- **Prior problem:** long LM contexts are expensive and finite, but learned summaries need to be consumable by the model itself.
- **Solution:** adapt the LM to recursively accumulate continuous summary vectors used as soft prompts for subsequent segments.
- **Mechanisms / learning:** unsupervised continuation LM loss, segmentation and summary accumulation, adapted pretrained OPT/Llama-2. Prior segments become vectors before later segment prediction; detailed gradient truncation/randomization remains to read.
- **Evidence:** **A**, original abstract/comments/history. HTML request failed, legitimate abstract route succeeded. Perplexity, compressed demonstrations and reranking are distinct author evaluations, not all equivalent consumption tests.
- **Distinguishes:** AE is necessary versus prediction-only latent training can work; frozen-consumer versus joint adaptation. No fixed-total-state or arbitrary-detail guarantee.

### A01-R07 — W0055 — xRAG: Extreme Context Compression for Retrieval-augmented Generation with One Token

- **Identity:** [arXiv:2405.13792v2](https://arxiv.org/abs/2405.13792v2), 2024-12-09; [official NeurIPS 2024 entry](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c5cf13bfd3762821ef7607e63ee90075-Abstract-Conference.html). **Existing-W unread**; formal publication verified, formal/v2 numerical equivalence unverified.
- **Prior problem:** a retrieval embedding is normally used only to find a document, and raw document processing dominates reader cost.
- **Solution:** learn a modality bridge that lets a frozen reader consume frozen document embeddings without their textual counterpart.
- **Mechanisms / learning:** dense retrieval features, multimodal-style projection/alignment, bridge-only training; original abstract does not establish the complete target mixture. One document-level vector, not an exact item-addressable memory.
- **Evidence:** **A**, arXiv and formal abstracts. The original bridge-training data/objectives and matched controls still need full reading. Claimed FLOP/quality gains are not adopted as fair system rankings.
- **Distinguishes:** insufficient representation versus consumer-interface mismatch; whole-backbone adaptation necessary versus bridge-only sufficient on some tasks. Retrieval chooses the document, but consumption of its embedding need not revisit source text.

### A01-R08 — old N04 — Context Compression via Explicit Information Transmission (ComprExIT)

- **Identity:** [arXiv:2602.03784v4](https://arxiv.org/abs/2602.03784v4), 2026-06-18; [served HTML](https://arxiv.org/html/2602.03784v4), whose heading adds *Fix the Structural Bottleneck*. **Existing-audit lead**; formal venue/acceptance not verified.
- **Source-integrity restriction:** abs text says code will be released upon acceptance; served HTML says code is available and displays a different apparent author presentation from the submitter/history cues. A submitter is not an author list; do not resolve identities by inference. Fixed PDF must adjudicate title/author/code-status alignment before final catalog promotion.
- **Prior problem:** multiple compression slots may redundantly aggregate the same source regions, and final-layer-only states may dilute intermediate evidence.
- **Solution:** aggregate across frozen layers and coordinate token-to-slot transmission using an entropy-regularized transport plan.
- **Mechanisms / learning:** cross-layer feature aggregation, learned anchors/projection and Sinkhorn normalization; selected text specifies local windows (example T=128), not unconstrained global transport. Question-unaware NTP then QA training; payload consists of compressed slots.
- **Evidence:** **A+P**, selected method/experiment passages and Appendix A.1.1–A.1.3. Reconstruction diagnostic feeds the frozen decoder gist states, a reproduce prompt and teacher-forced original tokens. It measures this reader's conditional NLL, not decoder-independent information loss. Attention correlation/effective rank are allocation diagnostics, not content-use interventions.
- **Distinguishes:** overlapping aggregation versus capacity shortage; intermediate readability versus information disappearance. Treat numeric superiority as provisional until fixed-source reconciliation and full ablation reading.

### A01-R09 — old N03 — Neural Discrete Representation Learning (VQ-VAE)

- **Identity:** [arXiv:1711.00937v2](https://arxiv.org/abs/1711.00937v2), 2018-05-30; [NeurIPS 2017 formal PDF target](https://proceedings.neurips.cc/paper/7210-neural-discrete-representation-learning.pdf). **Existing-audit lead**. This pass verified arXiv metadata/abstract; formal PDF was not newly fetched or compared.
- **Prior problem:** continuous stochastic latent models with powerful autoregressive decoders often fail to use latent codes.
- **Solution:** learn discrete codes by vector quantization with a learned prior rather than the conventional continuous posterior/prior setup.
- **Mechanisms / learning:** vector-quantized codebook and learned generative prior; full commitment/straight-through training equations remain unread in this pass. Images, speech and video are stated applications, not an unknown-query language benchmark.
- **Evidence:** **A**. Claim to circumvent a particular posterior-collapse failure is verified as the authors' claim, not a universal no-collapse guarantee.
- **Distinguishes:** stochastic-posterior information penalty versus discretization/training changes. Codebook collapse, posterior collapse and deployed ignorance require separate measures; equal slot dimensions are not equal effective bits.

### A01-R10 — W0066 — Universal Representations for Classification-enhanced Lossy Compression

- **Identity:** [arXiv:2504.13191v1](https://arxiv.org/abs/2504.13191v1), 2025-04-12; [PDF target](https://arxiv.org/pdf/2504.13191v1). **Existing-W unread**; no formal publication verified.
- **Prior problem:** reusing a single encoder over multiple reconstruction/classification or perception operating points may cost task fidelity.
- **Solution:** study universal encoders across these specified constraints and compare reuse against individually optimized encoders.
- **Mechanisms / learning:** rate–distortion–classification/perception formulation and trained image encoders; MNIST, known task/constraint family. Not arbitrary future query universality.
- **Evidence:** **A**, original abstract/history; reported classification-distortion penalty and comparatively small perception penalty remain to quantify from original tables.
- **Distinguishes:** one encoder universal across operating points versus specialist reoptimization; universality across constraints versus across unseen tasks.

### A01-R11 — old N05 — Rate-Distortion Theory in Coding for Machines and its Applications

- **Identity:** [arXiv:2305.17295v2](https://arxiv.org/abs/2305.17295v2), 2025-03-04; [v2 HTML](https://arxiv.org/html/2305.17295v2). **Existing-audit lead**. Formal journal metadata not verified; do not fill it from secondary citations. Complete author order requires fixed PDF because HTML extraction omits its first-name header.
- **Prior problem:** input reconstruction distortion need not describe fidelity for a fixed downstream machine task.
- **Solution:** formulate task-output distortion for full-input, split-feature and direct-to-feature coding, and analyze their ideal rate–distortion relationship.
- **Mechanisms / learning:** learned image coding, task model splitting, feature/task distortion; the ideal construction knows the task model, not every possible later query. The full-input decoder may output a class-equivalent prototype, not the original image.
- **Evidence:** **A+P**, §II definitions/Theorems 1–2/2.A and example; all proofs and detailed empirical results unread. Equivalence requires feasible task-output/image conditions and asymptotic optimal codecs; finite learned interfaces can differ substantially.
- **Distinguishes:** input MSE versus task distortion; ideal equivalence versus practical reader/codec restrictions. Does not make feature interfaces cost-free.

### A01-R12 — BIW-0094 — Generating Sentences from a Continuous Space

- **Identity:** [CoNLL 2016 formal record](https://aclanthology.org/K16-1002/), pp.10–21, DOI 10.18653/v1/K16-1002; existing partial target [arXiv:1511.06349v4](https://arxiv.org/pdf/1511.06349v4). **Existing-BIW partial**, not a new W record. Formal/arXiv text comparison not performed.
- **Prior problem:** sentence-level continuous latent variables can be ignored by an autoregressive word decoder.
- **Solution:** use a sentence VAE with KL annealing and decoder word dropout to encourage latent use.
- **Mechanisms / learning:** full-sentence recognition, Gaussian latent, LSTM autoregressive decoder and ELBO. Source is training text; whole-sentence latent has no content addresses.
- **Evidence:** fresh **metadata** plus existing **P §3.1/§4** in the BIW catalog, not a FULL card or fresh body reading. Prior evidence notes nonzero KL does not automatically beat an ordinary LM.
- **Distinguishes:** autoregressive bypass versus latent information; generative likelihood versus representation utility; stochastic word-text result versus deterministic byte-state analogy.

### A01-R13 — BIW-0095 — Improved Variational Autoencoders for Text Modeling using Dilated Convolutions

- **Identity:** [arXiv:1702.08139v2](https://arxiv.org/abs/1702.08139v2), 2017-06-18; [PDF target](https://arxiv.org/pdf/1702.08139v2). **Existing-BIW partial**. Formal venue not independently verified here.
- **Prior problem:** a strong sequential decoder can predict from its local context rather than the global latent.
- **Solution:** vary the receptive field of a dilated CNN decoder to control its local contextual capacity.
- **Mechanisms / learning:** Gaussian sentence latent, recognition network, causal dilated convolutions, ELBO; 20K-word vocabulary per existing record, not byte input.
- **Evidence:** fresh **A/history**, reuse of existing **P §§2.2–2.3/3.2–3.3**. The contextual-capacity/latent-use tradeoff is directly in the original abstract; complete labeling/generation controls unread.
- **Distinguishes:** decoder receptive-field effect versus inevitable uselessness of a latent; best likelihood versus best downstream representation.

### A01-R14 — BIW-0096 — Lagging Inference Networks and Posterior Collapse in Variational Autoencoders

- **Identity:** [arXiv:1901.05534v2](https://arxiv.org/abs/1901.05534v2), 2019-01-28; [body target](https://arxiv.org/html/1901.05534v2). **Existing-BIW partial**; prior recovery associates ICLR 2019, not newly venue-verified here.
- **Prior problem:** early inference networks fail to track the changing true model posterior, encouraging the generator to ignore latent codes.
- **Solution:** aggressively optimize the inference network before generator updates, using estimated latent–observation information to control the schedule.
- **Mechanisms / learning:** amortized inference, extra encoder optimization and ELBO, text/image benchmarks. Extra steps are optimization work, not new supervision.
- **Evidence:** fresh **A/history** and existing partial recovery, not a FULL card. Existing 2–3× timing note is a scoped prior observation, not fresh cost validation.
- **Distinguishes:** unavailable learning signal versus update imbalance; new architecture needed versus better inference optimization. Fixed-compute superiority remains open.

### A01-R15 — Variational Lossy Autoencoder

- **Identity:** [arXiv:1611.02731v2](https://arxiv.org/abs/1611.02731v2), 2017-03-04; [PDF target](https://arxiv.org/pdf/1611.02731v2). **Catalog-absent candidate**. ICLR 2017 appears in secondary search but no official decision was read; retain arXiv status in this inventory.
- **Prior problem:** unsupervised representations should sometimes retain global structure while discarding local texture that an autoregressive model can handle.
- **Solution:** design VAE plus autoregressive decoder/prior architecture to control which information the global latent must encode.
- **Mechanisms / learning:** neural autoregression (RNN/MADE/PixelCNN families) with variational latent coding; image density-estimation targets, not later-query labels.
- **Evidence:** **A**. v2 HTML returns conversion-error instructions rather than the paper; one legitimate abs fallback succeeded. Coding-argument details and free-bit controls remain unread.
- **Distinguishes:** decoder ignorance as an accidental failure versus selective information omission as an explicit task objective. Desired omission must be reanchored if exact strings are downstream targets.

### A01-R16 — Don't Blame the ELBO! A Linear VAE Perspective on Posterior Collapse

- **Identity:** [NeurIPS 2019 official entry](https://proceedings.neurips.cc/paper/2019/hash/7e3315fe390974fcf25e44a9445bd821-Abstract.html); associated [arXiv:1911.02469](https://arxiv.org/abs/1911.02469) from search, version not independently reconciled. **Catalog-absent candidate**, formal conference paper.
- **Prior problem:** collapse is often attributed solely to variational regularization or a powerful nonlinear decoder.
- **Solution:** analyze linear VAEs through probabilistic PCA and compare ELBO and marginal-likelihood stationary structure.
- **Mechanisms / learning:** linear Gaussian latent model and exact variational inference, with selected nonlinear empirical extensions described in the abstract.
- **Evidence:** **A**, original official abstract. It states no additional ELBO spurious local maxima in the analyzed linear model and identifies principal-component global recovery with exact inference; proofs/noise assumptions not read.
- **Distinguishes:** marginal-likelihood geometry versus ELBO-induced pathology. Linear-model theorem is not a theorem about arbitrary deep sequence decoders.

### A01-R17 — The Usual Suspects? Reassessing Blame for VAE Posterior Collapse

- **Identity:** [ICML 2020/PMLR 119:2313–2322](https://proceedings.mlr.press/v119/dai20c.html); [formal PDF target](https://proceedings.mlr.press/v119/dai20c/dai20c.pdf). Dai, Wang and Wipf. **Catalog-absent candidate**, published conference paper.
- **Prior problem:** accounts centered only on KL pressure understate bad minima in nonlinear encoder–decoder loss surfaces.
- **Solution:** analyze how nonlinear perturbations and depth create collapse/truncation minima beyond narrow affine-model guarantees.
- **Mechanisms / learning:** Gaussian VAE/deep autoencoder optimization geometry; controlled nonlinear constructions, not source-retrieval augmentation.
- **Evidence:** **A**, official abstract/metadata only; exact construction and nuisance conditions queued.
- **Distinguishes:** regularization-only explanation versus loss-surface risk; benign linear setting versus nonlinear counterexample. It refines, rather than universally falsifies, other collapse explanations.

### A01-R18 — Cyclical Annealing Schedule: A Simple Approach to Mitigating KL Vanishing

- **Identity:** [NAACL 2019 formal record](https://aclanthology.org/N19-1021/), pp.240–250, DOI 10.18653/v1/N19-1021; [PDF target](https://aclanthology.org/N19-1021.pdf). Fu et al. **Catalog-absent candidate**, published conference paper.
- **Prior problem:** early weak latent codes cause autoregressive decoder training to settle into KL-vanishing behavior.
- **Solution:** repeatedly raise the KL weight through warm-restart cycles so previously learned codes seed subsequent training.
- **Mechanisms / learning:** time-varying ELBO weighting; language modeling, dialogue and semi-supervised classification. Changes optimization schedule, not source labels or aggregation grain.
- **Evidence:** **A**, official abstract/metadata. Complete schedule-length, compute and baselines must be read before claiming dominance over monotone annealing or inference-heavy updates.
- **Distinguishes:** formation-path dependence versus fixed-capacity failure; improved latent information versus simply longer/more favorable training.

### A01-R19 — Variance Equalization for Posterior Collapse (search alias: λ-VAE)

- **Identity:** [arXiv:2607.05531v1](https://arxiv.org/abs/2607.05531v1), 2026-07-06; [served HTML](https://arxiv.org/html/2607.05531v1). Girum Demisse. **Catalog-absent candidate**, preprint; no venue/ICLR 2027 match verified.
- **Prior problem:** reconstruction/KL gradient imbalance and information loss during stochastic sampling can both favor uninformative latents.
- **Solution:** change the reparameterization noise exponent per dimension while retaining the original posterior-variance KL penalty.
- **Mechanisms / learning:** stochastic VAE reparameterization and rate/reconstruction tradeoff control; standard image benchmarks. No language-memory query channel or addressing experiment.
- **Evidence:** **A+P introduction only**, not the theory/body/appendix despite long HTML retrieval. Up-to-2.8× capacity and BPD statements are author abstract claims, not locally audited results.
- **Distinguishes:** representation computed by an encoder versus information surviving sampling; gradient-magnitude mechanism versus decoder architecture alone. Transfer to deterministic latent interfaces is a hypothesis, not a result.

### A01-R20 — Linear-Time Context Compression with State-Space Encoding (Boa Compressor)

- **Identity:** [arXiv:2610.33006v1](https://arxiv.org/abs/2610.33006v1), 2026-10-07; [served HTML](https://arxiv.org/html/2610.33006v1). **Catalog-absent candidate**, preprint; no venue acceptance verified. HTML author/affiliation layout is malformed; do not fill full author order from submitter or presentation cues.
- **Prior problem:** Transformer-based soft compression can cost enough prefill time to erase single-query savings.
- **Solution:** learn a Mamba-2 compressor with strided hidden states and per-layer KV projections for a frozen Transformer, followed by teacher-distribution fine-tuning.
- **Mechanisms / learning:** pretrained SSM, fixed stride, KV-space bridge, LM pretraining then answer-token KL distillation. Retains `ceil(L/r)` slots, growing with L; not one constant-size state. Query-aware online discussion and experimental input visibility must be checked separately.
- **Evidence:** **A+P**, introduction, selected §§3–5 training/interface/ablation passages; full tables, latency implementation and appendices unread. Text states 10B-token LM pretraining then 500k QA pairs, fixed target and shared baseline pretraining budget, with early stopping. These are author design statements, not a full cost audit.
- **Distinguishes:** consumer-distillation target versus token reconstruction; interface placement versus encoder expressivity; cheap recurrent writer versus a fixed-state all-detail impossibility. Query-aware advantages cannot certify a query-unknown contract.

### A01-R21 — Before Answering: Evidence Sufficiency under Size-Matched Memory Construction (MemSafe)

- **Identity:** [arXiv:2609.32269v1](https://arxiv.org/abs/2609.32269v1), 2026-09-26; [served HTML](https://arxiv.org/html/2609.32269v1). **Catalog-absent candidate**, preprint. Search mentions ICLR 2027 contexts but no official matching forum/decision verified; no acceptance claim.
- **Prior problem:** detecting insufficient compressed memory can be made spuriously easy when deleting evidence also reduces memory size.
- **Solution:** hold memory size matched across integrity states and train a query–unit cross-encoder plus set-transformer sufficiency estimator.
- **Mechanisms / learning:** supervised evidence-integrity/localization labels, cross-encoding, set aggregation and calibrated abstention gate. Query sees remaining memory; this diagnoses support, not reconstruction of missing facts. Not itself a compression writer.
- **Evidence:** **A+P introductory figure description**, not full reading. Abstract includes paragraph-count shortcut, frozen-cross-encoder control, five-seed multi-hop results, weaker unanswerable/OOD performance and low-coverage gating limits. Exact statistical construction/proofs and calibration coverage still to read.
- **Distinguishes:** evidence sufficiency versus memory-size shortcut; confidence versus support detection; unsupported answer avoidance versus restoring irrecoverable information. Clinical result was not pursued; no biological procedures or data were accessed.

## 3. Existing scoped FULL cards actually reused — no repeat full-reading count

Paths below are relative to `docs/research/`. The exact original card is the evidence source for this pass. Formal status not directly verified in this pass is explicitly left at the card's level. These are not among the 21 external recoveries above.

| ID / stable title-version-source / original status | Actual reusable card | Prior problem → one-sentence solution; mechanisms / learning source | What the evidence distinguishes and its ceiling |
|---|---|---|---|
| **W0059**, *Lossy Compression for Lossless Prediction*, [2106.10800v5](https://arxiv.org/abs/2106.10800v5), 2022-01-28; card associates NeurIPS 2021 | `flued_multigranularity_survey_20261108/03_reading/B04/W0059.md` | Unknown member of a fixed invariant task family → encode a maximum-invariant-related statistic; augmentation/contrastive or reconstruction objectives and entropy model | RF: task-family sufficient vs arbitrary future sufficient. Finite-entropy/log-loss conditions; card's MSE proof objections retained |
| **W0091**, *Learning Optimal Representations with the Decodable Information Bottleneck*, [2009.12789v2](https://arxiv.org/abs/2009.12789v2), 2021-07-16; old catalog NeurIPS 2020 | `flued_multigranularity_survey_20261108/03_reading/B04/W0091.md` | Stored features need a restricted reader → optimize label-decodable information and suppress class-conditional nuisance labels; supervised predictors/adversarial heads | RF: family-readable vs unrestricted information vs actually learned use. Exact-optimum/family assumptions and flagged proof steps limit theorem transfer |
| **W0092**, *A Theory of Usable Information Under Computational Constraints*, [2002.10689v1](https://arxiv.org/abs/2002.10689v1), ICLR 2020 per card | `flued_multigranularity_survey_20261108/03_reading/B13/W0092.md` | Shannon information ignores reader limits → define improvement between predictor-family optimal log losses; controlled predictors and deterministic preprocessing | RF: existing information made usable vs information created; optional ignorance/bounded-loss assumptions. Not native-model causal evidence |
| **W0038 / BIW-0020**, *In-context Autoencoder for Context Compression in a Large Language Model*, [2307.06945v4](https://arxiv.org/html/2307.06945v4), ICLR 2024 per card | `flued_multigranularity_survey_20261108/03_reading/B24/W0038.md` | Few slots must support later tasks → LoRA context encoder plus frozen decoder, AE+continuation then QA; writer question-unaware | RF: reconstruction/prediction complementarity in its setup; random-text and multi-segment failures. Not proof of exact recovery or task-content dependence |
| **W0023**, *Compressive Transformers for Long-Range Sequence Modelling*, [1911.05507v1](https://arxiv.org/html/1911.05507v1), 2019 preprint version; formal venue not rechecked | `flued_multigranularity_survey_20261108/03_reading/B24/W0023.md` | Old states must be discarded → compress evicted FIFO states using pooling/conv and state/attention reconstruction; next-token LM | RF: task response reconstruction vs full-state reconstruction, BPTT vs auxiliary stop-gradient; selected c values and changed BPTT budget prohibit clean universal ranking |
| **W0080**, *Handover of In-Context Learning State Across Session Boundaries*, [2608.14528v1](https://arxiv.org/html/2608.14528v1), 2026 preprint; card flags header/history date mismatch | `flued_multigranularity_survey_20261108/03_reading/B24/W0080.md` | State written before future input → characterize task-conditional equivalence and total handover budget; theoretical sufficient statistics and finite-bit examples | RF: capacity floor vs writer/consumer gaps; external files count. Exogenous-query/countable-support qualifications; no training effectiveness evidence |
| **W0061**, *Repeat After Me: Transformers are Better than State Space Models at Copying*, [2402.01032v2](https://arxiv.org/abs/2402.01032v2), 2024 preprint; venue not rechecked | `flued_multigranularity_survey_20261108/03_reading/B04/W0061.md` | Uniform random-string copy needs adequate state → counting lower bound and attention construction plus synthetic training | RF: query-before vs query-after, capacity vs optimization. Whole-string/error/finite-state assumptions; card flags formal inequalities/construction issues |
| **W0076**, *Fundamental Limits of Prompt Compression: A Rate-Distortion Framework for Black-Box Language Models*, [2407.15504v2](https://arxiv.org/pdf/2407.15504v2), 2024-12-11; catalog NeurIPS 2024 | `flued_multigranularity_survey_20261108/03_reading/B13/W0076.md` | Source length is not task loss → optimize hard-prompt expected-rate/task-distortion curve for fixed reader; LP/dual and query-aware selector | RF: unknown vs visible query and variable-rate allocation; short candidate enumeration/beam approximations, not exact global bounds on long language |
| **W0011**, *Dynamic Chunking for End-to-End Hierarchical Sequence Modeling*, [2507.07955v2](https://arxiv.org/html/2507.07955v2), 2025 preprint; formal status not rechecked | `flued_multigranularity_survey_20261108/03_reading/B05/W0011.md` | Fixed units allocate computation poorly → select contextual boundary vectors, smooth/upsample and optimize LM plus rate term; straight-through route | RF: learned boundary vs aggregation vs rate; direct selection comparable to tested pools. Residual bypass, cost and untested rare-detail limits retained |
| **W0013**, *A gated quantized VAE for learning variable length tokens*, [2512.21913v1](https://arxiv.org/html/2512.21913v1), 2025 preprint | `flued_multigranularity_survey_20261108/03_reading/B24/W0013.md` | Fixed quantized length vs variable text units → jointly learn gate/codebook/character decoder then create tokenizer with checked fallback | RF: continuous/discrete and rate/content distinction. Reconstruction checked using original text during encoding; no post-disposal source recovery, toy data and unmatched budgets |
| **BIW-0006**, *MANTa: Efficient Gradient-Based Tokenization for Robust End-to-End Language Modeling*, [2212.07284v1](https://arxiv.org/pdf/2212.07284v1), 2022-12-14; formal status not rechecked | `byte_language_interface_survey/03_reading/R01/BIW-0006.md` | Byte compute and inflexible units → soft frontier membership plus order-sensitive depthwise-conv/max blocks and hard L/4 cap, trained by span denoising | RF: rate enforcement vs content training; cap prevents all-byte degeneration qualitatively. Full-source corrupted encoder, not causal streaming; no clean all-task superiority |

## 4. Problem-level inventory for synthesis routing

| Problem key (local, not a new registered scientific term) | Relevant work keys | Competing explanation / genuinely missing test |
|---|---|---|
| A01-P01: reconstruction-target mismatch | R01–R04, R06–R08, R11, R20; W0038/W0023 | Source detail retention can help, hurt or waste rate depending on task, architecture and consumer; equal-rate/compute target crossing |
| A01-P02: unknown query and irreversible loss | R01/R04/R10; W0059/W0061/W0080 | Fixed task-family compression vs task shift vs arbitrary independent bits; no requirement to retain a source store |
| A01-P03: decoder ignorance | R03/R07/R12–R20; W0091/W0092 | Objective preference, autoregressive context, inference lag, loss-surface minima and interface mismatch need different controls |
| A01-P04: rate-dependent priority | R01/R05/R10/R11 | Fixed surrogate target vs rate-conditioned allocation; actual finite bits vs MI proxy; rare precision demands vs common coarse tasks |
| A01-P05: source of learning vs method of learning | R02/R06/R14/R18/R20; W0023/BIW-0006 | Teacher/labels/continuation targets vs update count/freezing/stop-grad/schedule; no automatic inference from final gradient cosine |
| A01-P06: aggregation and content-address grain | R02/R08/R09/R20; W0011/W0013/BIW-0006 | More slots, cross-layer states or KV may buy extra bits/interface capacity; total-bit and readout controls absent |
| A01-P07: sufficient support vs confident output | R21; W0076/W0092 | Size/norm/length shortcut and query support vs calibrated answer risk; abstention cannot restore missing content |
| A01-P08: exact rare strings, binding and order | R04/R08/R09; W0061/W0038/BIW-0006 | Average text scores conceal errors; conditioned exact-match and fact-swapping tests required, not a broad claim that no literature exists |

## 5. ICLR 2027 unresolved leads — not verified works or accepted papers

The official group shell was reachable but did not render the conference records; direct forums returned verification checks. The following searchable titles are **search-index leads only**. Forum version, original abstract/method, anonymous author state and submission/withdrawal/decision status could not be certified. No identity matching or deanonymization was attempted. Their problem/solution/mechanism fields are deliberately unfilled rather than guessed from a title.

| Candidate title as indexed | Exact official URL attempted | Why relevant / required next verification |
|---|---|---|
| *Fixed RAG Compression Can Distort Reader Comparisons* | https://openreview.net/forum?id=MpDEPJO8Aa | Reader × compression interaction; read official forum/modified date/status then original controls |
| *Anchored Context Distillation for Latent-Observation …* (index truncates title) | https://openreview.net/forum?id=1dBpTJv19B | Latent adaptation and distillation; full official title/version/status first |
| *Predicting output preservation and first divergence under KV-cache compression* (cited title in a public preprint) | https://openreview.net/forum?id=zKxUf16XnW | Predictive distortion/failure onset; original forum title/version/status not verified |
| *Beyond Token Savings: A Systematic Study of Context Compression in LLM Agents* | https://openreview.net/forum?id=Qit9HdVdT6 | Task-completion vs latent/task sufficiency; establish original task/source permissions before inclusion |

These entries are access gaps, not evidence that ICLR 2027 lacks relevant work. The wider venue stream should reconcile them once official public access is available. Other unvisited search hits remain in SEARCH_LOG, not promoted here.
