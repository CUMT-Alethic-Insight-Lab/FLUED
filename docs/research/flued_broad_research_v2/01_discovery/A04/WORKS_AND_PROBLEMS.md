# A04 — Works, problems, mechanisms, and discriminating hypotheses

Date: 2026-11-09. Scope: deployed content use and causal measurement, not an endorsement of source retrieval or multigranularity. This is a discovery inventory, **not a set of new full-reading cards**.

## Evidence and identity contract

- **A** = primary abstract and metadata actually retrieved this round. **P** = specified primary正文/body sections selected and read this round, not FULL. **R-FULL/R-PARTIAL** = an actual existing card read and reused, preserving its version and restrictions; neither is another original-paper reading.
- **Recovered** means already in the previous A04 audit, or already cataloged but unread. **New-to-selected-catalogs** means no stable-ID/title match in the two inspected catalogs and the multigranularity final addendum index; it does not assert novelty in science or absence from every old narrative.
- A04-R01–R08 retain previous audit aliases N01–N08. W and BIW aliases are not reassigned. A04-N labels are local discovery handles, not global W identifiers.
- Twenty-four externally verified/recovered records appear below: eight prior discovery leads, four existing unread W records, and twelve new-to-selected-catalogs candidates. This is **not 24 new works or 24 full reads**. Two blocked 2027 search leads are excluded. Twelve existing cards are reused separately.
- Terminology anchors: probe（探针：额外训练、从表示预测属性的读出器）; native readout（原生读出：部署模型本身使用的查询和读出计算）; estimand（估计目标：给定输入、干预分布和评分定义的待测量）; activation patching（激活替换：把指定内部值替换后继续计算）; mediation（因果中介：区分经过指定中间变量与其他路径的效应）; interaction（交互：联合效应不等于各项独立效应之和）; OOD（分布外：干预输入或内部组合偏离自然运行分布）; faithfulness（机制忠实性：解释是否反映原模型产生输出的计算，具体定义须逐文说明）. These are inline explanations, not new project terminology registrations.

## I. Recovered discoveries: reverified, not rediscovered as new

### A04-R01 / previous N01 — Causal Mediation Analysis for Interpreting Neural NLP: The Case of Gender Bias

- **Identity/version/status:** Jesse Vig et al.; [arXiv:2004.12265v2](https://arxiv.org/abs/2004.12265v2), 2020-11-22; expanded preprint. A differently titled NeurIPS counterpart was noted previously; this pass does not equate its full text with v2. [PDF](https://arxiv.org/pdf/2004.12265v2).
- **Prior problem → one-sentence solution:** behavior-only and structure-only analyses do not specify information flow; apply causal mediation interventions to neurons/heads to separate direct and indirect effects of gender changes.
- **Borrowed AI mechanism / learning:** frozen pretrained Transformers, paired inputs, internal component interventions; gender-bias datasets, not a trained memory reader. Unit: text input → head/neuron activations → output bias score.
- **Evidence:** A, official abstract plus Atom metadata. The author reports sparse and synergistic/amplifying/suppressing effects; no equations or individual numerical claims are newly verified here.
- **Distinguishes / decision:** fixed additive component importance versus context-conditioned mediator effects. Use as the original neural-language mediation anchor; do not assume its treatment, output scale, or empirical near-additivity transfers to byte memory.

### A04-R02 / previous N02 — The Hydra Effect: Emergent Self-repair in Language Model Computations

- **Identity/version/status:** Thomas McGrath, Matthew Rahtz, Janos Kramar, Vladimir Mikulik, Shane Legg; [2307.15771v1](https://arxiv.org/abs/2307.15771v1), 2023-07-28; public preprint, conference status not established. [PDF](https://arxiv.org/pdf/2307.15771v1).
- **Problem → solution:** a small ablation effect may hide downstream compensation; measure how downstream computations respond to layer ablations during factual recall.
- **Mechanism / learning:** fixed pretrained-model forward computations, attention-layer ablation and late MLP counterbalancing; not retraining-based recovery. The abstract reports the effect even without dropout training.
- **Evidence:** A only in this round. Exact compensation definitions, models, fractions and appendices remain unread.
- **Distinguishes / decision:** never-used component versus active component whose removal triggers compensation. Log downstream changes and compare free continuation with explicitly constrained-path effects; static duplicate storage and dynamic compensation are not interchangeable explanations.

### A04-R03 / previous N03 — Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models

- **Identity/version/status:** Peter Hase, Mohit Bansal, Been Kim, Asma Ghandeharioun; [2301.04213v2](https://arxiv.org/abs/2301.04213v2), 2023-10-16; official arXiv metadata says NeurIPS 2023 Spotlight. [PDF](https://arxiv.org/pdf/2301.04213v2).
- **Problem → solution:** causal localization is often used to choose an editing location; directly compare localization scores with editing success across layers and editing formulations.
- **Mechanism / learning:** representation denoising versus weight editing; editing changes the system, unlike fixed-weight inference patching. Granularity: factual prompts, MLP layers, stored fact outputs.
- **Evidence:** A this round; prior audit's selected §§4–8 findings are inherited, not re-read. The abstract itself includes the exception that one editing formulation does relate to localization, while layer choice predicts performance better.
- **Distinguishes / decision:** information passing through an interface versus that interface being the best repair target. A successful readout repair cannot retrospectively certify that the old readout was the unique cause of failure.

### A04-R04 / previous N04 — ERASER: A Benchmark to Evaluate Rationalized NLP Models

- **Identity/version/status:** Jay DeYoung et al.; [ACL 2020 official record](https://aclanthology.org/2020.acl-main.408/), pp. 4443–4458, DOI 10.18653/v1/2020.acl-main.408. [Version-of-record PDF](https://aclanthology.org/2020.acl-main.408.pdf).
- **Problem → solution:** rationale evaluation uses incomparable tasks and definitions; assemble human supporting rationales and measures for human alignment and prediction faithfulness.
- **Mechanism / learning:** token/sentence rationale extraction, keep-only and removal comparisons, confidence/behavior scoring. Additional rationale supervision and access must be accounted for separately from the deployed reader.
- **Evidence:** A plus official bibliographic record; primary PDF formulas not read this round. The precise sign/label conventions must be verified before implementation.
- **Distinguishes / decision:** evidence plausibility/human agreement versus evidence actually influencing the model. Pair with R05 rather than importing rationale deletion as an unquestioned causal gold standard.

### A04-R05 / previous N05 — Goodhart's Law Applies to NLP's Explanation Benchmarks

- **Identity/version/status:** Jennifer Hsia, Danish Pruthi, Aarti Singh, Zachary C. Lipton; [2308.14272v1](https://arxiv.org/abs/2308.14272v1), 2023-08-28; preprint, venue not established. [HTML](https://arxiv.org/html/2308.14272v1), [PDF](https://arxiv.org/pdf/2308.14272v1).
- **Problem → solution:** explanation scores may improve without more faithful explanations; construct wrappers exploiting distinguishable rationale/complement distributions and a label-encoding attack on EVAL-X.
- **Mechanism / learning:** saliency-selected input subsets, out-of-support detection, confidence manipulation, evaluator retraining. These are counterexamples to the instrument, not better memory architectures.
- **Evidence:** A freshly retrieved; previous audit's selected §§1–4 is reusable as P-prior, not FULL. Official abstract confirms predictions/explanations on in-distribution test inputs can remain unchanged while scores inflate.
- **Distinguishes / decision:** genuine content dependence versus recognizing the evaluation intervention and altering confidence. Add untouched-input equivalence checks, label-leakage controls, and held-out intervention families; two deletion metrics do not automatically close the loophole.

### A04-R06 / previous N06 — Evaluating the Faithfulness of Importance Measures in NLP by Recursively Masking Allegedly Important Tokens and Retraining

- **Identity/version/status:** Andreas Madsen, Nicholas Meade, Vaibhav Adlakha, Siva Reddy; [2110.08412v3](https://arxiv.org/abs/2110.08412v3), 2022-10-31; preprint identity verified, formal venue not checked. [PDF](https://arxiv.org/pdf/2110.08412v3).
- **Problem → solution:** masking importance scores confounds redundancy and distribution shift; recursively mask selected tokens, retrain, and compare masking curves with random-token baselines.
- **Mechanism / learning:** repeated model training and iterative importance updates; relative area between curves summarizes the result. Unit: token subsets → retrained task model → task performance.
- **Evidence:** A only; abstract reports four measures, eight datasets, LSTM-attention and RoBERTa, with model/task-dependent conclusions.
- **Distinguishes / decision:** features needed by the original deployed model versus information a newly trained model can replace. Relevant if considering retrained no-memory controls, but not a substitute for fixed-weight dependence.

### A04-R07 / previous N07 — RelP: Faithful and Efficient Circuit Discovery in Language Models via Relevance Patching

- **Identity/version/status:** Farnoush Rezaei Jafari, Oliver Eberle, Ashkan Khakzar, Neel Nanda; [2508.21258v2](https://arxiv.org/abs/2508.21258v2), 2025-10-30; venue unresolved. [PDF](https://arxiv.org/pdf/2508.21258v2).
- **Problem → solution:** exact patching is costly and local-gradient approximations fail in nonlinear models; replace attribution-patching gradients with layer-wise relevance propagation coefficients.
- **Mechanism / learning:** relevance redistribution with chosen propagation rules; two forward passes and one backward pass per abstract, not a full evaluation cost account. Tested on residual/MLP outputs and sparse-feature circuits.
- **Evidence:** A; detailed controls and all model/task results unread. The headline correlation improvement is an author report and is not used as a cross-method ranking here.
- **Distinguishes / decision:** approximation error relative to exact patch scores versus invalidity of the exact patch estimand itself. Only prioritize after trustworthy exact controls become a demonstrated cost bottleneck.

### A04-R08 / previous N08 — The Curse of Multiple Mediators: Hidden Interaction Effects in Activation Patching

- **Identity/version/status:** Sankaran Vaidyanathan, David Arbour, Aaron Mueller, Scott Niekum, David Jensen; [2606.27510v1](https://arxiv.org/abs/2606.27510v1), 2026-06-25; preprint, venue unverified. [HTML](https://arxiv.org/html/2606.27510v1), [PDF](https://arxiv.org/pdf/2606.27510v1).
- **Problem → solution:** single-component rankings and sum-of-effects predictions miss conditional mechanisms; explicitly decompose noising/denoising and grouped intervention effects into context-dependent and cross-component interaction terms.
- **Mechanism / learning:** fixed-model exact patching, causal mediation algebra, smooth downstream approximations, grouped IOI interventions. §3.2's approximation requires twice differentiability; the finite-difference interaction itself does not.
- **Evidence:** P, §§2–5.3 and opening discussion selected this round; appendix proofs/full tables not read. §5.2: removing interaction from the ranking can miss context-specific heads; pairwise tests also miss effects visible against a whole name-mover group. §5.3 says independent functional modularity must not be assumed for arbitrary models.
- **Distinguishes / decision:** redundancy, conditional cooperation, and harmful countervailing paths. Preserve the four observable cells and actual recomputation contract before naming a quantity NIE/PIE. The paper's interpretation of “pure” effects as path-specific requires graph/structural assumptions; do not turn its terminology into a general guarantee of isolated memory-content causation.

## II. Existing cataloged but unread works: identity/protocol recovery

### A04-R09 / W0533 — Towards Best Practices of Activation Patching in Language Models: Metrics and Methods

- **Identity/version/status:** Fred Zhang, Neel Nanda; [2309.16042v2](https://arxiv.org/abs/2309.16042v2), 2024-01-17; previous catalog/official metadata associates ICLR 2024, not freshly checked on the venue site. [HTML](https://arxiv.org/html/2309.16042v2), [PDF](https://arxiv.org/pdf/2309.16042v2).
- **Problem → solution:** patching choices yield incompatible localization; compare Gaussian noise, symmetric token replacement, output metrics and joint sliding-window versus single-layer patches.
- **Mechanism / learning:** frozen LM forward interventions; no extra learned reader. §6's answer-pair logit difference can control a generic “boost all names” direction that a single target logit does not.
- **Evidence:** P, §§5–6 this round plus targeted §3/4 excerpts; no full card. §5 explicitly treats windows as joint effects, not localization of the middle layer alone. §6 also warns that which input token is corrupted changes which information is traced.
- **Distinguishes / decision:** target value versus target identity/position and generic output-class boosts. Prefer legitimate token counterfactuals where suitable, but its claim of avoiding OOD is not proof that a hybrid of two natural internal states is jointly on-manifold.

### A04-R10 / W0531 — RAVEL: Evaluating Interpretability Methods on Disentangling Language Model Representations

- **Identity/version/status:** Jing Huang, Zhengxuan Wu, Christopher Potts, Mor Geva; [2402.17700v2](https://arxiv.org/abs/2402.17700v2), 2024-08-26; preprint verified, venue not reverified. [PDF](https://arxiv.org/pdf/2402.17700v2).
- **Problem → solution:** changing one concept can alter entangled attributes; evaluate interpreters with multiple causal criteria and learn multitask distributed alignments.
- **Mechanism / learning:** Multi-task Distributed Alignment Search (多任务分布式对齐搜索：用多个属性的干预目标学习表征子空间), frozen Llama2-7B, entity/attribute representations and supervised interventions.
- **Evidence:** A; detailed train/test entity separation and non-target criteria remain unread, as in the old audit.
- **Distinguishes / decision:** ability to force a target answer versus selective target change with unrelated attributes preserved. It evaluates an intervention method, not automatically the unmodified model's natural use.

### A04-R11 / W0373 — Naturalistic Causal Probing for Morpho-Syntax

- **Identity/version/status:** Afra Amini, Tiago Pimentel, Clara Meister, Ryan Cotterell; [TACL 2023 official record](https://aclanthology.org/2023.tacl-1.23/), volume 11, pp.384–403, DOI 10.1162/tacl_a_00554. Existing arXiv alias 2205.07043v2; version-of-record is the recommended next read. [PDF](https://aclanthology.org/2023.tacl-1.23.pdf).
- **Problem → solution:** arbitrary hidden interventions can misrepresent linguistic causation; intervene on naturalistic sentence morphosyntax while retaining the remaining sentence.
- **Mechanism / learning:** input-level counterfactual construction, Spanish gender/number, multilingual BERT/RoBERTa/GPT-2 contextual representations; no compressed memory or source revisit.
- **Evidence:** A, official abstract and identity; no full primary reading.
- **Distinguishes / decision:** a naturally recomputed input effect versus arbitrary hidden-state perturbation. “Naturalistic” does not establish all downstream hidden hybrids are valid or all semantic attributes remain fixed.

### A04-R12 / W0370 — Information-Theoretic Probing with Minimum Description Length

- **Identity/version/status:** Elena Voita, Ivan Titov; [EMNLP 2020 record](https://aclanthology.org/2020.emnlp-main.14/), pp.183–196, DOI 10.18653/v1/2020.emnlp-main.14. [PDF](https://aclanthology.org/2020.emnlp-main.14.pdf).
- **Problem → solution:** similar probe accuracy can hide large differences in learning effort; measure label description length using variational and online coding.
- **Mechanism / learning:** supervised probe training, coding/model complexity and data-efficiency measures. Input: fixed representations; output/supervision: linguistic labels. Query/label permissions exceed an untrained native readout unless separately matched.
- **Evidence:** A plus official BibTeX; no full card.
- **Distinguishes / decision:** recoverable information requiring expensive supervision versus easily accessible information. A useful bridge between representational presence and reader learnability, not a causal-use certificate.

## III. Newly verified candidates relative to the selected catalogs

### A04-N01 — Transformer Circuit Faithfulness Metrics are not Robust

- **Identity/version/status:** Joseph Miller, Bilal Chughtai, William Saunders; [2407.08734v1](https://arxiv.org/abs/2407.08734v1), 2024-07-11; official arXiv comment says CoLM 2024 conference paper. [HTML](https://arxiv.org/html/2407.08734v1), [PDF](https://arxiv.org/pdf/2407.08734v1).
- **Problem → solution:** identical circuits obtain incompatible faithfulness scores; enumerate and vary graph granularity, node/edge/branch, replacement value, positions, direction, and circuit/complement.
- **Mechanism / learning:** exact ablations of existing language-model circuits and compiled Tracr controls; no new memory learner. **P:** §§3–6, without appendices or complete tables.
- **Concrete falsification:** §5's positional encoding is constant across resampled inputs, so resampling cannot remove it; zeroing can. A discovery algorithm can perfectly recover the circuit appropriate to one definition while appearing wrong against the other's reference. §4 distinguishes ratio-of-means from mean-of-ratios and exposes extreme per-example scores.
- **Distinguishes / decision:** unnecessary content path versus invariant information left intact by the chosen donor distribution. Specify the information varied and preserved; complement ablation and circuit restoration do not necessarily enforce the same path restrictions. This is a substantive counterexample, not merely “try more ablations.”

### A04-N02 — Many Circuits, One Mechanism: Input Variation and Evaluation Granularity in Circuit Discovery

- **Identity/version/status:** Alireza Bayat Makou, Jingcheng Niu, Subhabrata Dutta, Iryna Gurevych; [2606.06267v2](https://arxiv.org/abs/2606.06267v2), 2026-08-26; official arXiv journal reference says TMLR 2026, publisher/forum not checked. [v2 PDF](https://arxiv.org/pdf/2606.06267v2). Search surfaced the shorter title “Input Variation and Evaluation Granularity in Circuit Discovery”; one work, not two.
- **Problem → solution:** different discovered edge sets are mistaken for different computations; vary token frequency with task fixed and compare structure, functional transfer, and interchange interventions.
- **Mechanism / learning:** ACDC pruning, fixed Pythia models, frequency bands, copying, cross-condition circuit transfer. No source revisit. **P:** rendered v1-route introduction/§2.1 and A: locked v2 abstract/metadata. The HTML route's title matches the later title; version-sensitive quantitative claims use the v2 abstract only.
- **Evidence/limits:** v2 reports 75 circuits, five scales; ≥99% recovery from the shared core is qualified to models **above 70M**, and adds a smaller subject–verb-agreement replication. It explicitly does not test position/feature-level specialization. All full tables/positive sensitivity controls remain unread.
- **Distinguishes / decision:** representation/route change versus genuine functional specialization. Require repeated extractions and cross-condition functional tests before interpreting changed circuit overlap as loss or gain of memory use.

### A04-N03 — Mechanistic Interpretability as Statistical Estimation: A Variance Analysis

- **Identity/version/status:** Maxime Méloux, François Portet, Maxime Peyrard; [2510.00845v4](https://arxiv.org/abs/2510.00845v4), 2026-05-28; public preprint, venue not established. Earlier titles add “of EAP-IG”; do not count that as a second work. [HTML](https://arxiv.org/html/2510.00845v4), [PDF](https://arxiv.org/pdf/2510.00845v4).
- **Problem → solution:** a single extracted circuit hides sample and methodological variability; decompose exact per-input mediation, approximation noise, aggregation, and graph selection, with bootstrap/stability evaluation.
- **Mechanism / learning:** exact interventions, gradient/integrated-gradient approximations, resampling and pruning on GPT-2 Small/Llama-3.2-1B variants. **P:** §§1–6 selected; appendices/full tables unread.
- **Important limit:** §6.1 explicitly separates empirical instability from theoretical non-identifiability. §5.1 says exact computations are restricted to IOI, while its Figure 2 caption and §6.3 also mention Greater-Than; this internal scope inconsistency must be resolved before quoting exact-task coverage. The suggested Jaccard 0.8 / 100-bootstrap threshold is tentative, not a transferable gate.
- **Distinguishes / decision:** finite-sample/approximation instability versus truly nonunique mechanisms. Report structural and behavioral stability separately, on independently held-out examples.

### A04-N04 — Towards Faithful Natural Language Explanations: A Study Using Activation Patching in Large Language Models

- **Identity/version/status:** Wei Jie Yeo, Ranjan Satapathy, Erik Cambria; [EMNLP 2025 official record](https://aclanthology.org/2025.emnlp-main.529/), pp.10425–10447, DOI 10.18653/v1/2025.emnlp-main.529. [Formal PDF](https://aclanthology.org/2025.emnlp-main.529.pdf). arXiv alias 2410.14155v2, 2024-11-01, still says “under review”; that stale comment does not override the official proceedings.
- **Problem → solution:** persuasive explanations can be unfaithful and perturbation tests can be OOD; compare activation-patching causal-attribution profiles for an explanation and its answer.
- **Mechanism / learning:** causal mediation/patching, explanation generation, pretrained/alignment-tuned 2B–27B models. **A** only, including official bibliography; body unread.
- **Distinguishes / decision:** shared attribution pattern versus explanation text merely sounding supportive. Positive candidate for triangulation, **not a settled solution**: agreement of two patch-based profiles inherits patch-background and interaction assumptions and does not independently verify target-content correctness.

### A04-N05 — Right for the Wrong Reasons: Diagnosing Syntactic Heuristics in Natural Language Inference

- **Identity/version/status:** R. Thomas McCoy, Ellie Pavlick, Tal Linzen; [ACL 2019 official record](https://aclanthology.org/P19-1334/), pp.3428–3448, DOI 10.18653/v1/P19-1334. [PDF](https://aclanthology.org/P19-1334.pdf).
- **Problem → solution:** good benchmark accuracy may come from fallible heuristics; construct HANS examples breaking lexical-overlap, subsequence, and constituent heuristics.
- **Mechanism / learning:** controlled natural-language templates evaluated against pretrained/fine-tuned NLI systems; no internal patching. **A**, official abstract and bibliography; detailed template splits unread.
- **Distinguishes / decision:** genuine relational/semantic dependence versus shortcut accuracy. Borrow known-answer counterexamples with unchanged surface cues; do not treat HANS failure as proof of a particular internal location or as direct evidence about byte memory.

### A04-N06 — Causal Scrubbing: a method for rigorously testing interpretability hypotheses

- **Identity/version/status:** Redwood Research original author-posted protocol, 2022; [primary public article](https://www.alignmentforum.org/posts/JvZhhzycHu2Yd57RN/causal-scrubbing-a-method-for-rigorously-testing). This is a research post/sequence, not a verified peer-reviewed proceedings paper; exact revision hash unavailable.
- **Problem → solution:** ad-hoc ablations do not rigorously test a stated interpretation; derive behavior-preserving conditional resampling interventions from a graph correspondence and hypothesized invariances.
- **Mechanism / learning:** computational-graph rewriting, recursive conditional resampling, induction/parenthesis examples. **P:** returned introduction, setup, and opening §3; the extraction ends during §3.1, so later algorithm details, limitations and sequence appendices are not read.
- **Distinguishes / decision:** “this feature influences output” versus “these proposed invariances explain the behavior.” The primary setup expressly says its equivalence-class test is weaker than full representational correspondence and cannot eliminate all wrong hypotheses. Recursive path enumeration can be costly; do not promise exhaustive tests on a full recurrent LM.

### A04-N07 — FaithEval: Can Your Language Model Stay Faithful to Context, Even If “The Moon is Made of Marshmallows”

- **Identity/version/status:** Yifei Ming, Senthil Purushwalkam, Shrey Pandit, Zixuan Ke, Xuan-Phi Nguyen, Caiming Xiong, Shafiq Joty; [2410.03727v3](https://arxiv.org/abs/2410.03727v3), 2025-04-24. Official arXiv comment reports ICLR 2025 publication; forum not independently checked. [HTML](https://arxiv.org/html/2410.03727v3), [PDF](https://arxiv.org/pdf/2410.03727v3).
- **Problem → solution:** ordinary QA misses unsupported, inconsistent, and counterfactual context behavior; build separate controlled context tasks with construction and validation procedures.
- **Mechanism / learning:** LLM-generated minimally modified contexts/distractors, separate judging and task-dependent human validation, deterministic instruction-following evaluation. **P:** §3.1–3.3; appendices/results not fully read.
- **Concrete controls/limits:** “unknown” and “conflict” are explicitly instructed responses; counterfactual science contexts are fabricated to support an alternative option. Human validation is not uniform: inconsistent examples are fully human filtered; counterfactual validation uses string matching justified by a pilot. Accuracy accepts mention of an answer, so it is not whole-response truth or entailment verification.
- **Distinguishes / decision:** contextual compliance versus world-truth accuracy. Following a false stipulated context can be correct for this task and wrong for an open-world truth task: declare authority/answerability policy first, not after seeing results.

### A04-N08 — ClashEval: Quantifying the tug-of-war between an LLM's internal prior and external evidence

- **Identity/version/status:** Kevin Wu, Eric Wu, James Zou; [2404.10198v3](https://arxiv.org/abs/2404.10198v3), 2025-02-07; preprint, formal venue not established. Earlier title: “How faithful are RAG models? Quantifying the tug-of-war between RAG and LLMs' internal prior.” [HTML](https://arxiv.org/html/2404.10198v3), [PDF](https://arxiv.org/pdf/2404.10198v3).
- **Problem → solution:** a model can trivially pass “reject bad context” by ignoring all context; pair prior-only and contextual answers, testing both correct-prior/wrong-context and wrong-prior/correct-context cases.
- **Mechanism / learning:** fixed inference models, numerical multipliers/categorical perturbations, prior token probabilities, standard/strict/loose prompts; six domains, 1,294 questions in the selected methods. **P:** §§1,3–4.4; full tables/appendices unread.
- **Controls/limits:** quantify prior bias and context bias separately; multi-document distractor addition changes length/evidence quantity, not an isolated memory mechanism. Context construction involves GPT-4o; source content includes some nonpublic medical pages, so do not imply unrestricted full-dataset access or download those pages.
- **Distinguishes / decision:** calibrated evidence arbitration versus blanket credulity or blanket disregard. Pair “believe correct evidence” and “reject false evidence” rather than treating answer flips as universally desirable.

### A04-N09 — Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small

- **Identity/version/status:** Kevin Wang, Alexandre Variengien, Arthur Conmy, Buck Shlegeris, Jacob Steinhardt; [2211.00593v1](https://arxiv.org/abs/2211.00593v1), 2022-11-01; original preprint verified, conference identity not checked this round. [PDF](https://arxiv.org/pdf/2211.00593v1).
- **Problem → solution:** broad low-resolution descriptions do not explain an end-to-end natural behavior; characterize an IOI head circuit and test faithfulness, completeness and minimality.
- **Mechanism / learning:** fixed GPT-2 Small, causal interventions, task-template/name manipulations, 26 heads in seven classes per abstract. **A**; its grouped-backup discovery is referenced by selected R08 body, not newly verified from this original paper's full protocol.
- **Distinguishes / decision:** sufficient circuit behavior versus completeness of the original computation. Read original grouped/backup tests before implementing an exclusion-of-redundancy claim; N01/N02 show why copying a reported faithfulness score alone is insufficient.

### A04-N10 — Everything, Everywhere, All at Once: Is Mechanistic Interpretability Identifiable?

- **Identity/version/status:** Maxime Méloux, Silviu Maniu, François Portet, Maxime Peyrard; [2502.20914v1](https://arxiv.org/abs/2502.20914v1), 2025-02-28; official arXiv journal reference says ICLR 2025, venue forum not checked. [PDF](https://arxiv.org/pdf/2502.20914v1).
- **Problem → solution:** satisfying common explanation criteria may not uniquely identify a mechanism; enumerate circuits, interpretations, algorithms and subspace alignments for Boolean functions/small MLPs.
- **Mechanism / learning:** exhaustive toy-model explanation search and causal alignment, not a theorem that all full-scale LMs are uninterpretable. **A** only.
- **Distinguishes / decision:** a useful falsifiable/manipulable explanation versus a uniquely identified original algorithm. Preserve multiple compatible hypotheses when tests do not distinguish them; empirical instability alone does not establish the enumeration paper's identifiability result on another system.

### A04-N11 — Hypothesis Testing the Circuit Hypothesis in LLMs

- **Identity/version/status:** Claudia Shi, Nicolas Beltran-Velez, Achille Nazaret, Carolina Zheng, Adrià Garriga-Alonso, Andrew Jesson, Maggie Makar, David M. Blei; [2410.13032v1](https://arxiv.org/abs/2410.13032v1), 2024-10-16; preprint verified, NeurIPS association in search not promoted to verified venue. [HTML](https://arxiv.org/html/2410.13032v1), [PDF](https://arxiv.org/pdf/2410.13032v1).
- **Problem → solution:** “small circuit” claims lack common statistical tests; formalize preservation/localization/minimality criteria and test six literature circuits, including hard-coded positives.
- **Mechanism / learning:** reference distributions and hypothesis tests over intervened circuit performance; circuitry software is an artifact, not installed or executed here. **A** only.
- **Distinguishes / decision:** interpretation passing a calibrated test versus simply having a large restoration score. Synthetic known-circuit positives validate some instrument behavior but do not prove sensitivity to nonlinear redundancy; exact null hypotheses and power remain missing reading questions.

### A04-N12 — Certified Interventional Fidelity: Anytime-Valid, Adaptive Evaluation of Causal Claims in Mechanistic Interpretability

- **Identity/version/status:** Amir Asiaee; [UAI 2026 official PMLR record](https://proceedings.mlr.press/v337/asiaee26d.html), volume 337, pp.210–227, 17–21 August 2026. [Proceedings PDF](https://raw.githubusercontent.com/mlresearch/v337/main/assets/asiaee26d/asiaee26d.pdf).
- **Problem → solution:** repeatedly inspecting/adapting intervention evaluations undermines fixed-sample confidence claims; define a bounded-score causal estimand over input/intervention distributions and provide confidence intervals/sequences with adaptive sampling weights.
- **Mechanism / learning:** Hoeffding-style and variance-adaptive betting confidence sequences, bounded mixture importance weighting; MNIST abstractions and GPT-2 Small IOI applications. **A**, official abstract and full bibliography, PDF not read.
- **Distinguishes / decision:** stable population intervention effect versus sampling/optional-stopping artifact. High-priority 2026 protocol: it could change stopping rules and sampling, not merely add caveats. Certification is conditional on score bounds, sampling/support/weighting assumptions and a chosen intervention distribution; it cannot certify that the intervention isolates correct evidence.

## IV. Existing actual cards reused without recounting

All following card links resolve into the old projects. Metadata and FULL scope are inherited from the actual card, not newly certified by external reading. Each row states what it can and cannot distinguish.

| Alias; title and source/version/status | Actual card / depth | Prior problem → solution; borrowed mechanism | Distinguishing hypothesis / restriction |
|---|---|---|---|
| **W0369**, Designing and Interpreting Probes with Control Tasks; [1909.03368v1](https://arxiv.org/abs/1909.03368v1), EMNLP-IJCNLP 2019 | [B14/W0369](../../../flued_multigranularity_survey_20261108/03_reading/B14/W0369.md), R-FULL | Probe accuracy can reflect memorization → fixed word-type random-label control; supervised probe capacity/selectivity | Information extraction versus probe learning. Control is fixed by type, not fresh independent random labels per occurrence; not native use. |
| **W0372**, Amnesic Probing: Behavioral Explanation with Amnesic Counterfactuals; [TACL 2021 formal PDF](https://aclanthology.org/2021.tacl-1.10.pdf) | [B08/W0372](../../../flued_multigranularity_survey_20261108/03_reading/B08/W0372.md), R-FULL | Decodability need not imply use → iterative linear erasure, random-rank damage and label addback | Specific attribute damage versus generic destruction. Masked dependency erasure and same-rank random damage both reach 4.67; addback plus retraining changes the system. |
| **W0374**, How Reliable are Causal Probing Interventions?; [IJCNLP-AACL 2025 formal PDF](https://aclanthology.org/2025.ijcnlp-long.47.pdf), arXiv 2408.15510 alias | [B08/W0374](../../../flued_multigranularity_survey_20261108/03_reading/B08/W0374.md), R-FULL; partial cross-version comparisons inherited | Strong intervention can harm non-targets → independently trained validation probes, completeness/selectivity curves | Target manipulation versus collateral effects. Independent probes remain fallible on hidden OOD states. Earlier BERT-only conclusions differ from six-model formal version. |
| **W0530**, CausalGym: Benchmarking causal interpretability methods on linguistic tasks; [2402.12560v1](https://arxiv.org/abs/2402.12560v1), 2024 preprint; venue not inherited as verified | [B26/W0530](../../../flued_multigranularity_survey_20261108/03_reading/B26/W0530.md), R-FULL | Trainable interventions may manufacture behavior → arbitrary-label/random-initialization controls for learned subspace interventions | Surgical ability versus naturally deployed mechanism; require original task above chance. |
| **W0532**, LEACE: Perfect linear concept erasure in closed form; [2306.03819v4](https://arxiv.org/abs/2306.03819v4), 2025 revision, venue not checked here | [B26/W0532](../../../flued_multigranularity_survey_20261108/03_reading/B26/W0532.md), R-FULL within theoretical-text scope | Ad-hoc erasure can distort features → covariance-based whitening/projection with affine minimum-distortion criterion | Specified-distribution linear removal versus all nonlinear information or semantic deletion; numerical stabilization is not optional. |
| **W0534**, Is This the Subspace You Are Looking for? An Interpretability Illusion for Subspace Activation Patching; [2311.17030v2](https://arxiv.org/abs/2311.17030v2), old catalog associates ICLR 2024 | [B26/W0534](../../../flued_multigranularity_survey_20261108/03_reading/B26/W0534.md), R-FULL, stated scope | A direction can be controllable without natural causal use → dormant/zero-space-to-active-space construction and tests | Introduced causal influence versus original path. Card flags proof issues for independent review, not an established refutation. |
| **W0535**, A Reply to Makelov et al. (2023)'s “Interpretability Illusion” Arguments; [2401.12631v1](https://arxiv.org/abs/2401.12631v1), 2024 preprint | [B26/W0535](../../../flued_multigranularity_survey_20261108/03_reading/B26/W0535.md), R-FULL | Component boundaries need not define causal abstractions → distributed causal-alignment response plus held-out-template tests | Natural distributed abstraction versus overfit subspace. Pair with W0534; not independent replication. Probability improvement is not exchange-answer success. |
| **W0050**, Evaluating Compressed Memory: Dependence, Utility, and Content Benefit; [2610.19373v1](https://arxiv.org/abs/2610.19373v1), 2026-10-14 preprint, metadata reverified this round | [B03/W0050](../../../flued_multigranularity_survey_20261108/03_reading/B03/W0050.md), **R-PARTIAL** | Zeroing dependence can coexist with poor utility → separately trained no-memory/constant-input references plus correct/donor passages | Channel dependence versus trained-system utility versus document-specific gain. Missing external supporting_evidence.pdf/configuration detail forbids a fair nine-system ranking. |
| **W0383**, Barriers to Counterfactual Credit Attribution for Autoregressive Models; [2605.01425v1](https://arxiv.org/abs/2605.01425v1), 2026 preprint | [B13/W0383](../../../flued_multigranularity_survey_20261108/03_reading/B13/W0383.md), R-FULL, proofs read but not independently verified | Local credit may not compose → sequence-level conditional-distribution definition, counterexample and black-box complexity bound | Token attribution versus whole generated-sequence credit. Exact-output-preservation/black-box assumptions do not ban finite task interventions. |
| **W0384**, Evidence Contextualization and Counterfactual Attribution for Conversational QA over Heterogeneous Data with RAG Systems; [2412.10571v3](https://arxiv.org/abs/2412.10571v3), catalog associates WSDM 2025 | [B14/W0384](../../../flued_multigranularity_survey_20261108/03_reading/B14/W0384.md), R-FULL | Single-source deletion misses redundant evidence → DBSCAN clusters then remove clusters and regenerate | Duplicated evidence versus unique marginal contribution. Answer embedding change is not correctness; evaluation conditions on gold URL in top ten. |
| **BIW-0005 / W0005**, Charformer: Fast Character Transformers via Gradient-based Subword Tokenization; [2106.12672v3](https://arxiv.org/abs/2106.12672v3), 2022-02-23, ICLR 2022 per card | [R01/BIW-0005](../../../byte_language_interface_survey/03_reading/R01/BIW-0005.md), R-FULL | Fine-grained encoding is costly → learned soft block mixtures then fixed-stride reduction, denoising supervision | Learned byte grouping versus demonstrated remote semantic use: full corrupted-source encoder and autoregressive byte decoder do not establish prefix-safe deployment or causal content consumption. |
| **BIW-0006 / W0006**, MANTa: Efficient Gradient-Based Tokenization for Robust End-to-End Language Modeling; [2212.07284v1](https://arxiv.org/abs/2212.07284v1), 2022-12-14 preprint, venue not checked here | [R01/BIW-0006](../../../byte_language_interface_survey/03_reading/R01/BIW-0006.md), R-FULL | Fixed segmentation and byte cost → learned frontier probabilities, soft pooling and task denoising with capacity cap | End-to-end task learning versus evidence that a compressed stream is actually consumed. Decoder/local path and full-input visibility remain separate variables. |

## V. Problem-to-instrument inventory, independent of architecture

| Concrete problem | Appropriate primary evidence | What changes in evaluation | What remains a new experiment |
|---|---|---|---|
| Probe says content exists but deployment fails | W0369/W0530 + R12 | Account for reader supervision/complexity; compare native reader before adding an oracle | Same representation and budget, fixed native versus bounded supervised readout |
| Recovered content is not the target relation/value | R10 + N05/N07/N08 | Target-correct and non-target-preserved checks, not source-ID hits | Fresh entity/value binding and relation-sensitive counterfactuals |
| Large zeroing damage but no content-specific gain | W0050 + R05 | Donor, constant-training and no-memory comparators answer different questions | Fixed-weight matched natural donor and separate matched retraining study |
| Null ablation due to redundancy or self-repair | R02/R08/N09 | Conditional/grouped tests plus downstream continuation, not one knockout | Known duplicate, cooperative, and dynamically compensating route controls |
| Intervention answers a different task | R09/N01/N06 | Declare varied/preserved information, graph granularity and invariances | Positive assay and untouched-input equivalence in the actual host |
| High score has unstable denominator or sampling | N01/N03/N11/N12 | Raw effects plus uncertainty/stopping contract, separate selection/evaluation | Held-out paired input/intervention distribution and cluster-aware sampling |
| Different circuits mistaken for different deployed mechanisms | N02/N03/N10 | Structural and functional stability/transfer reported separately | Held-out frequency/query/length transfer with a positive sensitivity control |
| Explanation/citation looks convincing but computation ignores it | R04/N04/W0384/W0383 | Human evidence alignment, causal effect, and whole-answer correctness separate | Contradiction/deletion/irrelevant evidence consistency under the same answer policy |

No work above alone selects a FLUED architecture. No training, inference experiment, code verification, theorem certification, or new FULL original-paper reading was performed.
