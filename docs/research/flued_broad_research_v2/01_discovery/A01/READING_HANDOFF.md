# A01 — Prioritized original-reading handoff

2026-11-09. **Executed discovery is complete; the reading below is not claimed complete.** This is a 15-work priority queue, not a second FULL count. Use [WORKS_AND_PROBLEMS](WORKS_AND_PROBLEMS.md) for identity/classification, [SEARCH_LOG](SEARCH_LOG.md) for actual successful/blocked routes and [COVERAGE_AND_FINDINGS](COVERAGE_AND_FINDINGS.md) for hypotheses. The final broad synthesis remains unstarted by this specialist.

## 1. Instructions to the next reader/catalog owner

- Preserve W/BIW aliases and old N provenance. `A01-Rxx` is only a local discovery key. Merge versions by stable identity, not title resemblance or a repeated local alias.
- Reuse the eleven actual existing scoped FULL cards listed in WORKS_AND_PROBLEMS §3. Their original-paper reading counts do not increase because this pass read the cards. Preserve the identified theorem/proof limitations; FULL is a scope label, not correctness certification.
- For new originals, label **FULL / PARTIAL / BLOCKED** by what was actually read. A long retrieved HTML, abstract, press/project page, table caption or downloaded PDF is not automatically a full reading. Record sections/pages/appendices and unread figures/proofs separately.
- No mandatory source revisit assumption. Primary contract is irreversible compression before a specific later query. Label works with query-visible encoding, a growing retained sequence, a hidden residual source channel, or source-dependent fallback instead of using their scores as interchangeable fixed-state evidence.
- Extract separately: (i) source of supervision/teacher/labels, (ii) optimization and adaptation regime, (iii) aggregation grain and address/payload units, (iv) total stored bits, (v) deployed content dependence. Do not call all of these “latent training” and lose the causal distinctions.
- Temporary PDFs, if later fetched, belong only at the project paths below. They are **planned paths, not files created in this pass**. No `/tmp`, Downloads, arbitrary installation, code execution, paid resource or authentication bypass is authorized. Do not solve OpenReview verification checks through another identity/session.

## 2. Fifteen-work priority original-reading queue

The first eight resolve the most consequential objective/collapse/sufficiency forks; the remaining seven are specific implementation/controls branches. Ordering is information value, not recommendation to implement the method. Formal/preprint versions must remain separated until compared.

### 1 — A01-R01 / W0067 — Optimal Multitask Representations Under a Rate Constraint

- **Exact source:** https://arxiv.org/html/2610.30493v1 ; PDF https://arxiv.org/pdf/2610.30493v1 . v1, 2026-10-21; preprint, venue unverified.
- **Current depth:** selected §§2–6; no complete proofs/finite-bit appendix.
- **Missing question:** which conditions make specialist/generalist or task-allocation priorities reverse with rate, and when does a known fixed objective suffice? Does the operational finite-bit result track nominal MI, code budget, empirical entropy, or actual encoded size?
- **Read to:** Proposition 1 and its proof; specialist crossover; §4 frequency/precision construction and relative-regret denominator; Theorems 1–2 and proofs; CelebA/dSprites main experiments plus Appendix F (training, probe class, five seeds/paired bootstrap, entropy and exact compute).
- **Required output:** assumptions/quantifiers table; rate-axis table; fixed-pretext bounded-SNR positive control beside the negative example; distinguish theoretical optimum, fitted proxy and actually trained codes.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_2610.30493v1.pdf`.

### 2 — A01-R03 / old N06 — Fixing a Broken ELBO

- **Exact source:** https://proceedings.mlr.press/v80/alemi18a.html ; PDF https://proceedings.mlr.press/v80/alemi18a/alemi18a.pdf . ICML 2018 formal version.
- **Current depth:** official abstract/metadata only.
- **Missing question:** how can equal ELBO produce different input–latent information and useful representations, and which constraints actually force use by a powerful decoder?
- **Read to:** entire rate/distortion derivation, identical-ELBO construction, controlled-rate mechanism, powerful-decoder experiments and supplements. Verify which quantities are variational bounds, actual rates, reconstruction losses or task probes.
- **Required output:** objective degeneracy versus optimization-failure distinction; at least one original counterexample and its exact conditions. Do not substitute “same reconstruction” for “same ELBO”.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/pmlr_alemi18a_formal.pdf`.

### 3 — A01-R14 / BIW-0096 — Lagging Inference Networks and Posterior Collapse

- **Exact source:** https://arxiv.org/html/1901.05534v2 ; PDF https://arxiv.org/pdf/1901.05534v2 . v2, 2019-01-28; formal version not reconciled.
- **Current depth:** original abstract/history plus existing partial recovery, not FULL.
- **Missing question:** what early training trajectory distinguishes inference lag from weak information supply or genuine generative-objective preference, and what does extra inference optimization cost at equal budgets?
- **Read to:** toy posterior-tracking analysis, aggressive-update algorithm/stopping criterion, text/image experiments, all relevant appendices, timing and monotone-annealing/autoregressive controls.
- **Required output:** update-count/compute accounting; latent information versus aggregate KL; evidence that intervention changes the proposed lag, not just a final loss.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_1901.05534v2.pdf`.

### 4 — A01-R16 — Don't Blame the ELBO! A Linear VAE Perspective on Posterior Collapse

- **Exact source:** https://proceedings.neurips.cc/paper/2019/hash/7e3315fe390974fcf25e44a9445bd821-Abstract.html ; formal PDF https://proceedings.neurips.cc/paper/2019/file/7e3315fe390974fcf25e44a9445bd821-Paper.pdf . NeurIPS 2019; PDF is a target not fetched in this pass.
- **Current depth:** official abstract only.
- **Missing question:** which marginal-likelihood local maxima already exist without the variational approximation, and which noise/rank/inference assumptions prevent or permit collapse?
- **Read to:** linear-VAE/pPCA correspondence, exact-inference/global solution, all landscape/noise results and nonlinear empirical tests with appendices.
- **Required output:** conditional theorem boundaries, not “ELBO never causes collapse”. Pair its linear positive result with A01-R17's nonlinear counterexamples before making a general causal statement.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/neurips2019_lucas_formal.pdf`.

### 5 — A01-R02 / old N02 — Autoencoding-Free Context Compression … (SAC)

- **Exact source:** https://arxiv.org/html/2510.08907v4 ; PDF https://arxiv.org/pdf/2510.08907v4 ; formal record https://proceedings.iclr.cc/paper_files/paper/2026/hash/dff28796c79e1a04c7a6182119ee899a-Abstract-Conference.html . ICLR 2026 publication verified; v4/formal equivalence open.
- **Current depth:** §§3–5 and ablation descriptions; numerical Table 5 not obtained.
- **Missing question:** is the AE penalty architecture-dependent when carrier selection, KV capacity, bidirectional visibility, pretraining/fine-tuning and total tokens are held fixed?
- **Read to:** all objective/component/selection ablations, exact Table 5 cells, Appendix A/B training costs, fine-tuned full-context reference, summarization and OOD results; formal/v4 correspondence.
- **Required output:** identify which cells isolate objective vs architecture and whether LM-only/AE-only/mixed exposure is matched; gradient angle is not a sufficient causal mechanism.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_2510.08907v4.pdf`.

### 6 — A01-R04 / old N01 — Rethinking Minimal Sufficient Representation in Contrastive Learning

- **Exact source:** https://openaccess.thecvf.com/content/CVPR2022/html/Wang_Rethinking_Minimal_Sufficient_Representation_in_Contrastive_Learning_CVPR_2022_paper.html ; PDF https://openaccess.thecvf.com/content/CVPR2022/papers/Wang_Rethinking_Minimal_Sufficient_Representation_in_Contrastive_Learning_CVPR_2022_paper.pdf . CVPR 2022 formal version.
- **Current depth:** official abstract only.
- **Missing question:** what is lost when future-task information is not shared by the two views, and does input-information regularization improve robustness at equal effective rate and training budget?
- **Read to:** formal assumptions/non-shared-information counterexample and supplements, regularizer implementation, augmentation/task comparisons, memory/compute/hyperparameter controls.
- **Required output:** separate pretext/view sufficiency from specified-task sufficiency; do not infer that all minimal sufficient representations are intrinsically defective.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/cvpr2022_wang_rethinking_formal.pdf`.

### 7 — A01-R05 / W0064 — Caveats for Information Bottleneck in Deterministic Scenarios

- **Exact source:** https://arxiv.org/abs/1808.07593v4 ; PDF https://arxiv.org/pdf/1808.07593v4 . v4, 2019-02-08.
- **Current depth:** abstract/history only; prior ICLR 2019 association not newly official-verified.
- **Missing question:** why can varying a linear IB multiplier fail even if informative points exist, and how far do the caveats extend to near-deterministic labels?
- **Read to:** all three caveats/proofs, replacement functional, near-deterministic extension and MNIST experiments.
- **Required output:** separate target determinism, finite/continuous representation assumptions, scalarization failure and empirical MI estimator artifacts.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_1808.07593v4.pdf`.

### 8 — A01-R06 / W0037 — Adapting Language Models to Compress Contexts

- **Exact source:** https://arxiv.org/abs/2305.14788v2 ; PDF https://arxiv.org/pdf/2305.14788v2 . v2, 2023-11-04; original page says accepted EMNLP 2023.
- **Current depth:** abstract/comments only; HTML network failure was not a body read.
- **Missing question:** how do continuation-only losses, recursive accumulation and consumer adaptation make summary vectors usable without AE, and where do long-context or task-transfer failures remain?
- **Read to:** complete algorithm/attention masks, randomized segmentation, gradient truncation, summary accumulation, LM/demo/reranking evaluations, training and inference accounting.
- **Required output:** who sees which context/query at write time; frozen versus changed weights; persistent summary growth; content-specific utility versus ordinary adapted-LM improvement.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_2305.14788v2.pdf`.

### 9 — A01-R07 / W0055 — xRAG

- **Exact source:** https://arxiv.org/abs/2405.13792v2 ; PDF https://arxiv.org/pdf/2405.13792v2 ; formal record https://proceedings.neurips.cc/paper_files/paper/2024/hash/c5cf13bfd3762821ef7607e63ee90075-Abstract-Conference.html . NeurIPS 2024 verified.
- **Current depth:** original/formal abstracts only.
- **Missing question:** with retriever and reader frozen, what training targets teach the bridge to deliver document-specific content rather than a useful generic prompt?
- **Read to:** pretraining and instruction/distillation stages, query visibility, bridge size, downstream and cross-backbone comparisons, source/incorrect-source/constant/no-source controls where present, teacher/corpus cost.
- **Required output:** exact content and adaptation contract; compare against existing W0050's scoped criticisms without pretending that an external evaluation replaces reading the original. W0050 remains PARTIAL and was not reread in this pass.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_2405.13792v2.pdf`.

### 10 — A01-R08 / old N04 — Context Compression via Explicit Information Transmission

- **Exact source:** https://arxiv.org/abs/2602.03784v4 ; PDF https://arxiv.org/pdf/2602.03784v4 ; served HTML https://arxiv.org/html/2602.03784v4 . v4, 2026-06-18; formal acceptance unverified.
- **Current depth:** selected method/training and Appendix A.1.1–A.1.3; source alignment unresolved.
- **Missing question:** do intermediate-feature retention and coordinated slots improve payload retention, reader compatibility, or just capacity/optimization? Is served HTML the same fixed-version artifact as the PDF/abs?
- **Read to:** **identity/version check first**, then cross-layer and transport equations, local-window restrictions, all Table 2 ablations and reconstruction/slot-rank diagnostics, complete NTP/SFT costs and appended experiments.
- **Required output:** reconcile title/author/code-release text without reconstructing identity from submitter; explain teacher-forced reconstruction's reader dependence. Distinguish attention-map diversity from preservation of exact relation bindings.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_2602.03784v4.pdf`.

### 11 — A01-R09 / old N03 — Neural Discrete Representation Learning

- **Exact source:** https://arxiv.org/abs/1711.00937v2 ; PDF https://arxiv.org/pdf/1711.00937v2 ; formal target https://proceedings.neurips.cc/paper/7210-neural-discrete-representation-learning.pdf . v2 2018-05-30; NeurIPS 2017 association must be version-aligned before numeric citation.
- **Current depth:** abstract/history only in this pass; prior audit partial reading does not make today's pass FULL.
- **Missing question:** what exactly removes the conventional posterior-collapse incentive, and what remains vulnerable to limited codebook use or irrelevant latent content?
- **Read to:** complete quantization/commitment/straight-through loss, prior fitting, strong-decoder experiments and continuous-VAE controls, capacity/cost definitions.
- **Required output:** posterior collapse vs codebook collapse vs actual task use; learned prior/decoder/quantization confounds and effective-bit accounting.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_1711.00937v2.pdf`.

### 12 — A01-R11 / old N05 — Rate-Distortion Theory in Coding for Machines and its Applications

- **Exact source:** https://arxiv.org/html/2305.17295v2 ; PDF https://arxiv.org/pdf/2305.17295v2 . v2, 2025-03-04; formal journal status not verified.
- **Current depth:** selected §II theory and illustrative equivalence construction.
- **Missing question:** under which output-feasibility and codec conditions are input/feature/direct representations equivalent in task distortion, and why can finite learned decoders break practical equivalence?
- **Read to:** full §II–III, Appendix A proofs, supervised/unsupervised distinction, distortion-layer design and task experiments; fixed PDF author/title metadata.
- **Required output:** loss object, source/target availability, quantifiers and resource exclusions; ideal class-equivalent reconstruction is not source reconstruction.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_2305.17295v2.pdf`.

### 13 — A01-R15 — Variational Lossy Autoencoder

- **Exact source:** https://arxiv.org/abs/1611.02731v2 ; PDF https://arxiv.org/pdf/1611.02731v2 . v2, 2017-03-04; official formal venue still to verify if cited.
- **Current depth:** abstract only; HTML conversion-error page is not readable source content.
- **Missing question:** when is local decoder predictability supposed to remove information from the global code, and how does a coding argument distinguish desired omission from failed latent learning?
- **Read to:** full information-preference/coding argument, chosen decoder receptive field, free-bit/rate mechanism if present, density/representation experiments, limitations and supplements.
- **Required output:** explicit objective-dependent definition of “irrelevant”; contrast image texture with exact identifiers or later-task private details rather than treating all omitted detail alike.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_1611.02731v2.pdf`.

### 14 — A01-R20 — Linear-Time Context Compression with State-Space Encoding

- **Exact source:** https://arxiv.org/html/2610.33006v1 ; PDF https://arxiv.org/pdf/2610.33006v1 . v1, 2026-10-07; preprint, no verified venue match.
- **Current depth:** selected architecture/training/interface/ablation passages.
- **Missing question:** how much benefit comes from distillation timing, per-layer KV capacity, pretrained SSM and visible query, rather than compression architecture alone?
- **Read to:** complete input construction and causal alignment, Mamba/pretraining provenance, LM vs distillation stage order, embedding vs KV ablation, Table 6 controls, full latency including compression/teacher cost, context/rate scaling.
- **Required output:** write-time query-visible flags per experiment, stored slots growing with input length, total per-layer KV bytes and cross-host bridge capacity; no comparison to constant-state lower bounds without matching the contract.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_2610.33006v1.pdf`.

### 15 — A01-R21 — Before Answering: Evidence Sufficiency under Size-Matched Memory Construction

- **Exact source:** https://arxiv.org/html/2609.32269v1 ; PDF https://arxiv.org/pdf/2609.32269v1 . v1, 2026-09-26; preprint, no verified ICLR 2027 forum.
- **Current depth:** abstract and introductory figure only.
- **Missing question:** is sufficiency detection learning evidence requirements rather than paragraph count, answerability priors or task-specific annotation artifacts, and what survives query/domain shift?
- **Read to:** size-matching proposition/construction, exact supervision labels and permitted reference answers, cross-encoder/mean/set comparisons, held-out/negative transfer, gating risk–coverage/calibration and seeds.
- **Required output:** distinguish source evidence present, estimator score and reader correctness; preserve worse unanswerable/SQuAD2.0/domain-transfer cases and low-coverage limits. Do not interpret abstention as recovering discarded bits.
- **Planned local PDF:** `docs/research/flued_broad_research_v2/01_discovery/A01/sources/arxiv_2609.32269v1.pdf`.

## 3. Disposition of every old compression recommendation

All eleven were externally recovered in this pass. None was silently treated as already synthesized, none requires adopting source retrieval, and none was promoted from abstract/partial to FULL.

| Old recommendation | Today's record | Disposition |
|---|---|---|
| W0067 | R01 | Priority 1; selected body recovered, complete proof/finite-bit read still needed |
| N02 SAC | R02 | Priority 5; 2026 formal publication verified, Table 5/full-budget missing |
| N06 Broken ELBO | R03 | Priority 2; official abstract only |
| N01 Rethinking | R04 | Priority 6; official abstract only |
| W0064 | R05 | Priority 7; original abstract/history |
| W0037 | R06 | Priority 8; original abstract/comments, body request failed |
| W0055 | R07 | Priority 9; arXiv/formal abstracts, no original full card |
| N04 ComprExIT | R08 | Priority 10; source reconciliation is an explicit prerequisite, not an inferred author match |
| N03 VQ-VAE | R09 | Priority 11; abstract/history only here, older partial provenance retained |
| W0066 | R10 | **Reserve**, not dropped: https://arxiv.org/pdf/2504.13191v1 . Read next if the rate/operating-point result is used to justify a universal encoder; MNIST/classification/perception constraints and reuse penalties must be quantified |
| N05 Coding for Machines | R11 | Priority 12; conditional theorem statements recovered, proofs/empirics missing |

Other precise reserves: **R17 Dai et al.**, https://proceedings.mlr.press/v119/dai20c/dai20c.pdf (read with priority-4 Lucas before any general landscape claim); **R18 cyclical annealing**, https://aclanthology.org/N19-1021.pdf (if schedule intervention is proposed); **R19 variance equalization**, https://arxiv.org/pdf/2607.05531v1 (recent sampling mechanism; theoretical novelty/universality and language transfer unverified); **BIW-0094/0095** original targets in WORKS_AND_PROBLEMS (decoder-context controls). Additional sources are reserves because they answer narrower next questions, not because their fields are exhausted.

## 4. Verified-existing synthesis inputs: reuse rather than reread

The next scientific writer can already state, with qualifications:

- W0059 v5 + W0080 v1 + W0061 v2: specified task family versus arbitrary later exact detail, query timing, finite-bit counting and all-source-channel accounting.
- W0091 v2 + W0092 v1: consumer-family accessibility is distinct from unrestricted information and actual trained use; preserve the original card's theorem/proof warnings.
- W0038 v4 + W0023 v1: original target ablations and old-state compression; include positive evidence for AE+LM in ICAE, not an anti-AE one-way narrative.
- W0011 v2 + BIW-0006 v1 + W0013 v1: boundary choice, within-segment aggregation, rate control, code type and teacher/source fallback are different mechanisms.

Do **not** reopen full reads of these just to inflate a count. Revisit a particular original location only if the new synthesis makes a stronger claim than the scoped card supports. Unread but relevant W0062/W0065/W0093/W0094/W0095 remain theory reserves from the previous audit; they were not all reverified today and are not included in the 21-work verified count.

## 5. Official-venue handoff and actual remaining limits

Official group URL: https://openreview.net/group?id=ICLR.cc/2027/Conference . A loading shell was observed; no membership/pagination inventory was accessible. Four exact forum/PDF access gaps are listed in WORKS_AND_PROBLEMS §5 and SEARCH_LOG F06–F09/F38–F40. Preserve anonymous identity and record title, modified date, invitation/group and actual state on future successful access. An arXiv heading or search engine's “Conference Submission” is not a verified acceptance.

No new full reading, independent proof validation, code replication or local experiment was completed. No missing latent content was measured on FLUED. The experiment obligations in COVERAGE_AND_FINDINGS are genuinely new work, not conclusions awaiting only more citations. Architecture choices and numerical thresholds remain undecided.
