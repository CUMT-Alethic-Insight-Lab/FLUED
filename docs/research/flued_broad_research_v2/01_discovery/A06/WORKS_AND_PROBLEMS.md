# A06 — Works, prior problems, interventions and distinguishing hypotheses

2026-11-09. This inventory is an axis-specific input to the single-owner catalog, not a replacement catalog or a final-report synthesis. See [coverage](COVERAGE_AND_FINDINGS.md), [sources](SEARCH_LOG.md), and [reading queue](READING_HANDOFF.md).

## Classification and counting rules

Classification is multidimensional: **provenance** (existing full card / existing unread catalog / previously recovered discovery / additional discovery), **depth** (original abstract/metadata / targeted original body / inherited scoped full card), **role** (positive protocol / counterexample / measurement / alternative), and **stage** (formation / acute damage / restoration / deployment selection). Venue and version are separate fields. None implies another.

- **N06-01–12** preserve the previous composition audit's actual aliases. They were absent from its main catalog but were already found in the old axis audit; they are recovered discoveries, not new to the project today.
- **A06-X01–X10** are local discovery locators only. Stable IDs/titles had no matches in the supplied old `02_catalog` and byte `02_inventory` searches; these are additional relative to those inventories, subject to central cross-stream deduplication. Do not assign global W IDs here.
- Six existing full cards were actually read and reused, separately below. Two already cataloged unread host papers are retained as specific gaps. Do not count aliases or versions as additional works, or reused full cards as new readings.
- A fetched HTML may be complete in tool storage while the research reading remains targeted. **No original-paper FULL status was added by this stream.** No reported result was replicated.

## A. Twelve previously recovered works, externally revisited

### N06-01 — How transferable are features in deep neural networks?

**Source/version/status:** [arXiv:1411.1792v1](https://arxiv.org/html/1411.1792v1), 2014-11-06; Yosinski et al.; NeurIPS 2014 association inherited from prior audit, original experiment text freshly checked, proceedings not re-audited. **Provenance/depth:** recovered discovery; targeted §§2–4.3 and Appendix A, not FULL.

- **Prior problem:** apparent feature non-transferability can conflate task specialization with breaking jointly learned dependencies.
- **One-sentence solution:** cross same-task versus cross-task copied lower layers with frozen versus fine-tuned copied weights, while reinitializing and relearning the upper layers.
- **Borrowed mechanisms / learning:** convolutional feature reuse, frozen transfer and gradient fine-tuning; ImageNet label cross-entropy. Input units are image pixels/features, not byte segments; no memory addressing or original-source retrieval.
- **Controls/evidence:** BnB, AnB, BnB+, AnB+, random lower-layer controls and more-distant task splits; same-task middle-layer deficits can disappear when copied layers adapt. **BnB randomizes the upper network**, so it is not exact replay of the original pair of halves.
- **Distinguishes:** specificity vs relearning/co-adaptation cost; frozen compatibility vs plastic recovery.
- **Cost/failure/transfer:** original lower-model training plus continuation must be counted; App. A uses 450k iterations per normal run. Fine-tuning restoration does not identify which local component caused a deficit or prove byte-model transfer.

### N06-02 — Revisiting Model Stitching to Compare Neural Representations

**Source/version/status:** [arXiv:2106.07682v1](https://arxiv.org/html/2106.07682v1), 2021-06-14; Bansal, Nakkiran and Barak; NeurIPS 2021 association inherited. **Provenance/depth:** recovered; original abstract/introduction revisited, detailed connector training/appendix not newly audited.

- **Prior problem:** geometric similarity measures need not show whether another model can actually consume a representation.
- **Solution:** freeze two original half-networks and train a simple intervening layer to test task-preserving forward compatibility.
- **Mechanisms/learning/units:** affine/interface transformation trained with task supervision; image feature maps, source prefix and recipient suffix; no query-time source revisit.
- **Evidence/controls:** authors report compatible good networks across initialization/objectives, and improved weaker models supplied with stronger prefixes. This stream does not independently certify every connector constraint or training table.
- **Distinguishes:** a useful restricted interface exists vs raw coordinates are incompatible; it does not establish shared information cues.
- **Cost/failure:** connector data, tuning and original training remain costs; unrestricted connectors risk learning task solutions rather than exposing old semantics. Pair with N06-03 and A06-X04, not a stand-alone similarity certificate.

### N06-03 — How not to Stitch Representations to Measure Similarity: Task Loss Matching versus Direct Matching

**Source/version/status:** [arXiv:2412.11299v1](https://arxiv.org/html/2412.11299v1), 2024-12-15; Balogh and Jelasity; AAAI 2025 association from prior official metadata, not freshly proceedings-verified. **Provenance/depth:** recovered; targeted abstract, introduction and matching formulation; OOD detector appendix returned but not fully audited.

- **Prior problem:** high task accuracy of a stitched model is routinely interpreted as original functional similarity.
- **Solution:** compare task-loss-optimized affine stitching with direct activation-distance matching and sanity checks on layer correspondence/self-similarity.
- **Mechanisms/learning/units:** affine maps, least-squares/pseudoinverse direct matching, downstream task optimization and distribution diagnostics over image features.
- **Evidence:** task-loss matching can rate distant layers, including another layer versus itself, unexpectedly highly; authors connect this to unusual recipient activations. These are measurement counterexamples, not proof practical learned composition has no value.
- **Distinguishes:** original representation equivalence vs task-specific rerouting; high score vs natural interface distribution.
- **Cost/failure:** direct matching penalizes all coordinate errors, including possibly irrelevant subspaces; it need not be the best deployment interface. Detector validity and exact training must be read before treating OOD scores as ground truth.

### N06-04 — Revisiting Model Stitching in the Foundation Model Era

**Source/version/status:** [arXiv:2603.12433v3](https://arxiv.org/html/2603.12433v3), 2026-06-02 per previous version audit; [official CVPR 2026 PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Mai_Revisiting_Model_Stitching_In_the_Foundation_Model_Era_CVPR_2026_paper.pdf) located by search, not newly full-read. Old audit used v1; this stream uses **v3 targeted text**, no line-by-line version equivalence claim. **Provenance/depth:** recovered/version-advanced; §§3.2–5.3 plus selected source/control discussion.

- **Prior problem:** heterogeneous vision foundation models may fail to compose under local feature matching or direct downstream training, even with small local errors.
- **Solution:** pretrain only the stitch on recipient final features, then task-fine-tune it while original source/recipient remain frozen.
- **Mechanisms/learning/units:** teacher feature distillation, per-position linear/MLP interfaces or a LoRA-enabled source layer, downstream supervision; image tokens/maps, no byte or source-address contract.
- **Controls/evidence:** §4.1 inserts identical stitch modules at identical positions, objectives and data in both self-models. §5.3 compares interface families, and §5.2 reports a weaker CLIP source still failing to match stronger recipients. Gains are not guaranteed by adding interface expressiveness.
- **Distinguishes:** local alignment error vs downstream sensitivity; extra capacity vs cross-model complementarity; interface/optimization failure vs potentially missing source information.
- **Cost/failure:** teacher final-feature computation and two-stage training are extra supervision; exact matched compute/seed intervals remain full-read questions. Authors' information-loss explanation for the weaker source is not an independent impossibility proof.

### N06-05 — The Hydra Effect: Emergent Self-repair in Language Model Computations

**Source/version/status:** [arXiv:2307.15771v1](https://arxiv.org/abs/2307.15771v1), 2023-07-28; McGrath et al.; preprint, accepted venue not verified. **Provenance/depth:** recovered; original abstract/history only.

- **Prior problem:** component ablation effects can be masked by later computation changing its response.
- **Solution:** analyze attention-layer compensation and late MLP counterbalancing through causal interventions in factual recall.
- **Mechanisms/learning/units:** activation ablation and downstream response analysis in pretrained token LMs; no additional training intervention certified at this depth.
- **Evidence:** authors report compensation, even without training dropout, and relatively localized coupling. Configuration/scope is not a newly read result table.
- **Distinguishes:** absent causal contribution vs naturally compensated contribution.
- **Cost/failure:** not a transplant recipe or an equal-compute architecture comparison. Prefer N06-06 for systematic follow-up before operationalizing compensation controls.

### N06-06 — Explorations of Self-Repair in Language Models

**Source/version/status:** [ICML 2024, PMLR 235:42836–42855](https://proceedings.mlr.press/v235/rushing24a.html), formal proceedings verified; prior targeted text [2402.15390v2](https://arxiv.org/html/2402.15390v2) was not freshly reread here. **Provenance/depth:** recovered; official metadata and abstract freshly verified, prior body claims remain bounded by old audit.

- **Prior problem:** narrow-example self-repair observations may not describe broad prompt distributions or different model families.
- **Solution:** measure how attention-head ablations are compensated across broad distributions/families and separate candidate mechanisms.
- **Mechanisms/units:** activation ablation, direct/total effects, LayerNorm scaling and anti-erasure neurons; token LM activations.
- **Evidence:** official abstract reports repair is imperfect, noisy and sometimes overcorrecting, with scaling and sparse anti-erasure contributions.
- **Distinguishes:** small total effect because a component is unused vs because downstream computation compensates; mean compensation vs prompt variability.
- **Cost/failure:** not evidence that a fixed-downstream diagnostic equals deployed total damage. Exact resampling, multi-head and distribution controls are queued, not already certified.

### N06-07 — LoLCATs: On Low-Rank Linearizing of Large Language Models

**Source/version/status:** [2410.10254v3](https://arxiv.org/html/2410.10254v3), 2025-03-05; **accepted ICLR 2025**, [official proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/72163d1c3c1726f1c29157d06e9e93c1-Abstract-Conference.html). **Provenance/depth:** recovered; §§3.1–3.3 opening and Table 2 read; no FULL.

- **Prior problem:** replacing pretrained softmax attention by linear attention can badly degrade quality; full-model restoration is expensive.
- **Solution:** first fit new attention feature maps to teacher attention outputs, then compensate remaining errors using low-rank projection updates.
- **Mechanisms/learning/units:** MSE feature distillation under teacher-fed layer inputs; causal next-token cross-entropy with LoRA; kernel features and window+linear variants; token hidden states/QKV, not original-text lookup.
- **Evidence/control:** Table 2 compares transfer/no transfer and LoRA/no LoRA. Llama-3-8B T2R gives 1539.39/79.33 before adjusting without/with transfer, and 16.05/4.11 after adjusting. Combined training uses 2+2 epochs versus 4 for a single stage. Original weights frozen in matching; LoRA updates specified Q/K/V/O in adjustment.
- **Distinguishes:** one-stage failure vs staged repair; attention approximation vs adaptation compatibility.
- **Cost/failure:** the table is an equal-total-step **strategy** comparison, not equal-dose 2×2 mechanistic interaction estimation. The untrained baseline and different adjustment doses matter. Teacher cost, natural-chain accumulation and final long-context content use need separate accounting.

### N06-08 — Transformers to SSMs: Distilling Quadratic Knowledge to Subquadratic Models

**Source/version/status:** [2408.10189v2](https://arxiv.org/html/2408.10189v2), 2025-02-08 per old version audit; v1 had shorter title. Current text verified, accepted-venue status not independently certified. **Provenance/depth:** recovered/version-advanced; targeted §4 and selected §5/control passages.

- **Prior problem:** strong Transformer training investment is difficult to reuse in subquadratic sequence models.
- **Solution:** MOHAWK matches sequence-mixing matrices, then block outputs, then whole-model outputs in stages.
- **Mechanisms/learning/units:** structured-matrix approximation, feature MSE, inherited teacher weights, logit distillation; causal token sequence mixers, no original-source revisit.
- **Evidence/controls:** convolution initially identity, gate opened to one, output normalization and post-convolution activation removed for transplant alignment; native from-scratch helpful components need not remain helpful in this history. Same-architecture Phi→Phi control resets attention while inheriting the other weights.
- **Distinguishes:** architecture capacity vs transplant conditioning; missing/mismatched companions vs central mixer; local/block alignment vs composed error.
- **Cost/failure:** teacher pretraining and staged exposure are not free; not all stage ablations have been verified equal-total-budget in this stream. The paper's scratch/transfer comparisons do not randomize pretraining history.

### N06-09 — Data Efficient Any Transformer-to-Mamba Distillation via Attention Bridge

**Source/version/status:** [2510.19266v4](https://arxiv.org/abs/2510.19266v4), 2026-09-16; first submitted 2025-10-22. Current abstract calls method Cross-architecture distillation via Attention Bridge (CAB). No accepted venue independently verified. **Provenance/depth:** recovered; fresh original abstract/history; previous targeted introduction not upgraded.

- **Prior problem:** direct intermediate features from attention and state-space models may not match structurally; output-only distillation misses useful intermediate guidance.
- **Solution:** use a lightweight bridge and flexible layer alignment to supervise Mamba's token-dependent state projections from attention-related teacher representations.
- **Mechanisms/units:** cross-architecture feature distillation and learned alignment over token-level states; image classification and language modeling are both claimed.
- **Evidence:** original abstract reports improvements under limited supervision and no inference-time bridge overhead. Actual intervention tables were not read.
- **Distinguishes:** missing correspondence/interface vs intrinsically non-transferable knowledge; output-only vs intermediate supervision.
- **Cost/failure:** bridge training/teacher passes remain costs; “Any” in the title is not arbitrary-host coverage. Not promoted above MOHAWK without extracting incremental controls.

### N06-10 — Bridging KV-Cache Quantization and Linear Attention: From Theory to Pretrained Weight Migration

**Source/version/status:** [2610.11214v1](https://arxiv.org/html/2610.11214v1), 2026-10-08; preprint; distinct from W0214. **Provenance/depth:** recovered; targeted introduction, §5.3 and appendix staged-ablation discussion. Current extraction omits numerical table cells.

- **Prior problem:** aggregation into recurrent state and per-entry KV quantization are different compression regimes; pretrained Transformer weights need a recoverable bridge.
- **Solution:** use soft discrete-address assignments and a soft-quantized intermediate construction for head→block→whole-model RAM-Net migration.
- **Mechanisms/learning/units:** codebook/soft address overlap, low-rank adapters and staged distillation/recovery; token Q/K/V to addressable continuous slots; no retained original-text retrieval.
- **Evidence/control:** fixed 500M-token Qwen2.5-1.5B pipeline comparison, removing head/block stages reallocates their tokens to whole-model recovery. Authors report lower task scores without intermediate stages even when Wiki PPL remains similar. Numerical cells in the prior audit are **not independently reverified here**.
- **Distinguishes:** benefit of staged objective vs simply more tokens; PPL restoration vs downstream restoration.
- **Cost/failure:** equal tokens does not equal teacher FLOPs/wall time; restricted overlap approximation is not a global full-attention identity or a universal migration guarantee.

### N06-11 — On the State of the Art of Evaluation in Neural Language Models

**Source/version/status:** [1707.05589v2](https://arxiv.org/html/1707.05589v2), 2017-11-20; Melis, Dyer and Blunsom; version text verified, ICLR 2018 association not freshly proceedings-verified. **Provenance/depth:** recovered; targeted §5.1 and §7, with returned main text inspected for scope.

- **Prior problem:** architecture rankings conflate capacities, regularization and uneven tuning effort.
- **Solution:** tune regularization/optimization and embedding-vs-recurrent parameter allocation within defined model-size budgets and rerun selected configurations.
- **Mechanisms/learning/units:** black-box Gaussian-process tuning, recurrent LMs, tied embeddings and down-projections; word LM plus Enwik8 character setting, not one universal interface.
- **Evidence/control:** §5.1 lets tuner trade embedding and hidden size inside a parameter budget; §7.1 evaluates individual features, **not their combinations**; §7.2 checks rerun variability.
- **Distinguishes:** parameter count vs allocation/trainability; fixed-default result vs optimized model family.
- **Cost/failure:** substantial tuning expense, thousands of evaluations in some settings. This is not a cheap full-factorial recipe and its historical PPL noise thresholds do not transfer to this project.

### N06-12 — The Key to Going Linear: Analysis-Driven Transformer Linearization

**Source/version/status:** [2607.07706v1](https://arxiv.org/html/2607.07706v1), public first submission 2026-07-08 in prior metadata; HTML header says February 2026, not used as public-release date. Preprint; no accepted venue verified. **Provenance/depth:** recovered; targeted §3–4 and App. C implementation/budget.

- **Prior problem:** post-hoc linearization bundles many simultaneous changes and obscures which state update preserves pretrained attention.
- **Solution:** compare replacement mechanisms with an initially fully frozen original backbone, then add explicitly controlled structural/limited-adaptation changes.
- **Mechanisms/learning/units:** delta-rule versus gated/kernelized accumulation, causal next-token CE, local/prefix cache routing, short convolution and LoRA; token recurrent states/QKV.
- **Evidence/control:** 10M tokens/2,500 iterations, 4,096-length packing; QKV unchanged in strict core comparison. Constant 64 cache slots can be divided into 56 local+8 prefix. §4 reports GLA/GDN gap nearly vanishing with short convolutions; LoRA uses smaller learning rate for stability. App. C: no sweep, three stated seeds.
- **Distinguishes:** core-rule effects conditional on companions and projection plasticity; strict frozen-host ranking vs adapted-host ranking.
- **Cost/failure:** implementations differ greatly in elapsed time (authors report ~1h GLA/GDN vs ~8h Hedgehog on H100 in this setup). Equal tokens and identical defaults do not equal equal optimization opportunity. First-order analysis is not global long-sequence task equivalence.

## B. Ten additional original works verified this stream

### A06-X01 — Net2Net: Accelerating Learning via Knowledge Transfer

**Source/version/status:** [1511.05641v4](https://arxiv.org/html/1511.05641v4); Chen, Goodfellow and Shlens; ICLR 2016 association, locked v4 body independently read selectively, proceedings not rechecked. **Depth/role/stage:** targeted §§2.1–2.4/3 and App. A; positive control and restoration/formation alternative, not FULL.

- **Prior problem:** architectural expansion incurs destructive transient loss and repeatedly starts optimization from scratch.
- **Solution:** initialize wider/deeper students with function-preserving transformations of an already trained network before continuation.
- **Mechanisms/learning/units:** duplicate hidden units and compensate outgoing weights; insert identity layers subject to nonlinearity constraints; normal supervised continuation. Image hidden units/maps, not byte compression.
- **Evidence/controls:** random-padding/random-initialization controls; §2.1 also reports unsuccessful hidden-feature prediction relative to a strong batch-normalized baseline. ReLU identity condition is explicit; sigmoid insertion is not generically identity. Symmetry-breaking noise makes exact preservation approximate.
- **Distinguishes:** surgery implementation damage vs extra parameters; initial functional capacity vs later learned usable capacity; benefit of a matching objective vs strong baseline optimization.
- **Cost/limits:** source pretraining and continuation must be counted. App. A uses smaller student learning rate. Increasing parameter count alone is not a clean increase in effective task information at t=0. Cannot declare a learned lossy compressor “identity” merely because its output length is unchanged.

### A06-X02 — Progressive Neural Networks

**Source/version/status:** [1606.04671v4](https://arxiv.org/html/1606.04671v4), version associated with 2022 revision, originally 2016; Rusu et al.; accepted venue not verified. **Depth/role/stage:** targeted §§2–3/5.1–5.3 and limitations; constructive alternative, formation/transfer.

- **Prior problem:** sequential fine-tuning destroys old features and forces the recipient to use a potentially harmful source initialization.
- **Solution:** freeze old task columns, add a new trainable column and learned lateral adapters that may reuse or ignore old features.
- **Mechanisms/learning/units:** A3C reinforcement learning, nonlinear lateral adapters, per-source scaling, Fisher/perturbation sensitivity; image-observation control policies, not text retrieval.
- **Evidence/controls:** target-only, source-pretrained output-only, source-pretrained fully fine-tuned, and randomly initialized frozen-source multi-column baselines. §5.1 reports top three of 25 sampled seed/hyperparameter jobs and learning-curve area, not unconditional all-run means.
- **Distinguishes:** useful pretrained content vs generic extra branch capacity; source feature reuse vs new learning; frozen reuse vs destructive adaptation.
- **Cost/limits:** total parameters grow, task label selects inference column, some negative transfer remains. Do not import “no forgetting” as a guarantee if old pathways are modified or routing changes. A bounded extra branch is an alternative to any original-source revisit.

### A06-X03 — Git Re-Basin: Merging Models Modulo Permutation Symmetries

**Source/version/status:** [2209.04836v6](https://arxiv.org/html/2209.04836v6); Ainsworth, Hayase and Srinivasa; ICLR 2023 association, proceedings not independently re-fetched. **Depth/role/stage:** targeted §2–3 and abstract/limitations; coordinate-control alternative, post-training composition.

- **Prior problem:** incompatible coordinate order can make equivalent hidden functions look distant and naive weight interpolation fail.
- **Solution:** choose hidden-unit permutations to align independently trained equivalent-architecture models before merging.
- **Mechanisms/learning/units:** activation matching, weight matching and permutation symmetry; existing network weights, no language-source access.
- **Evidence/control:** §2 gives function-preserving paired incoming/outgoing permutations; authors also discuss a counterexample to the universal single-basin hypothesis. Exact known permutation recovery is mentioned in appendix but not independently tested here.
- **Distinguishes:** coordinate mismatch vs different function/content; pure representation relabeling vs actual semantic intervention.
- **Cost/limits:** matching cost and architecture constraints remain. Grouped operations, tied/shared parameters and normalization can restrict legal permutations; no automatic rotation/permutation certificate for a different recurrence or compressed state.

### A06-X04 — Functional Alignment Can Mislead: Examining Model Stitching

**Source/version/status:** [ICML 2025, PMLR 267:55972–55998](https://proceedings.mlr.press/v267/smith25a.html); Smith, Mannering and Marcu; formal venue and official PDF endpoint verified. **Depth/role/stage:** original proceedings abstract only; counterexample, post-training measurement.

- **Prior problem:** successful functional alignment is interpreted as capturing the same information.
- **Solution:** deliberately stitch representations trained on different cues/tasks/modalities, including clustered random noise, to test the implication.
- **Mechanisms/units:** frozen-half stitching plus learned connection; exact connector details not read; vision feature representations and artificial sources.
- **Evidence:** official abstract explicitly reports successful stitching in these cases; it is not a newly audited effect-size table.
- **Distinguishes:** useful predictive compatibility vs original shared information/invariances.
- **Cost/limits:** actual random-noise construction, held-out sampling and label leakage controls require full reading. “Clustered random noise” must not be paraphrased as arbitrary fresh i.i.d. noise preserving all semantic information. Queue this precise missing question, not a blanket dismissal of stitching.

### A06-X05 — Grounding Functional Similarity by Invariance-Aware Model Stitching

**Source/version/status:** [2505.20142v2](https://arxiv.org/html/2505.20142v2), 2026-06-01; v1 first submitted 2025-05-26 per [official history](https://arxiv.org/abs/2505.20142v2). **Depth/role/stage:** targeted §§2–3 and Appendix D; positive diagnostic protocol, no FULL. **Venue: unresolved for this exact version**. Related ICLR 2026 forum hJvcbkf2nO has different searched title/author list; current repo advertises ICML 2026, but that is not independent venue verification. Do not merge claims/status by name resemblance.

- **Prior problem:** forward stitching can exploit predictive cues while ignoring source/recipient invariance differences; direct matching can instead over-penalize irrelevant subspaces.
- **Solution:** test forward–backward compatibility using inputs optimized to be nearly identical in the source representation and alignment objectives spanning internal recipient layers.
- **Mechanisms/learning/units:** representation inversion from noise, frozen image models, affine stitch initialized by pseudoinverse on 500 samples, feature-distillation hints up to the penultimate layer. The backward direction is about input preimages, **not gradient propagation**.
- **Evidence/control:** same initialization across ordinary and invariance-aware stitching, cue variants and shortcut availability; FuLA does not use output-level hints in the stated implementation. §2.3.1 explicitly notes approximate input inversions and an assumed unique optimal forward compatibility.
- **Distinguishes:** forward predictive compatibility vs shared discarded/preserved cues; local matching vs downstream sensitive subspaces.
- **Cost/limits:** inversion is extra optimization and may create unnatural inputs. This suggests a natural counterfactual-cue test for language, not permission to assume continuous image inversion works over valid bytes. Full reading must audit inverse-domain validity and robustness.

### A06-X06 — GPTailor: Large Language Model Pruning Through Layer Cutting and Stitching

**Source/version/status:** **accepted ICLR 2026**, [official proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5c99f2254833533c2a8ca0e0be04d77e-Abstract-Conference.html); targeted [2506.20480v1](https://arxiv.org/html/2506.20480v1), 2025-06-25. No claim the preprint equals final proceedings page for page. **Depth/role/stage:** §§3.4/4.3–4.4 selective; practical multi-component deployment search.

- **Prior problem:** single-model pruning discards complementary ability emphasized in related fine-tunes.
- **Solution:** jointly search layer removal, donor-layer selection and layer merging to assemble a compact model.
- **Mechanisms/learning/units:** zero-order configuration search with SMAC/random-forest surrogate and multi-fidelity calibration evaluation; pretrained token-model layers, no original-source retrieval.
- **Evidence/control:** §4.4 reports full search 48.55 average, removal-only 44.83 and selection+removal 43.20 in its 7B setting; selection without merging is not a reliable improvement. §4.2/4.3 specifies 500 search trials, calibration-size fidelity and adaptive resource allocation.
- **Distinguishes:** useful joint integration vs naive mix-and-match; search optimization capacity vs component feasibility.
- **Cost/limits:** donor fine-tunes, calibration labels, search compute and expanded space must be charged. Nested search-space optimum cannot worsen mathematically; observed worse searched result can reflect finite optimization and is not proof donor selection inherently harms a fixed model. This is not an identified full-factorial interaction coefficient.

### A06-X07 — KLAS: Using Similarity to Stitch Neural Networks for Improved Accuracy-Efficiency Tradeoffs

**Source/version/status:** **accepted ICLR 2026**, [official proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/e9f0ce998bede73f8068985f3deeab9a-Abstract-Conference.html); [2605.29259v1](https://arxiv.org/abs/2605.29259v1), 2026-05-28. Search gave one inconsistent 2025 date for HTML: official history is used instead. **Depth/role/stage:** official abstract/history only, practical deployment selection, not FULL.

- **Prior problem:** heuristic stitch-site/model-pair selection yields weak accuracy–compute tradeoffs.
- **Solution:** rank promising binary stitches by intermediate KL-divergence-based similarity before fine-tuning.
- **Mechanisms/learning/units:** representation similarity, candidate selection among O(k²n²) possibilities, stitch fine-tuning; vision features and ImageNet classification.
- **Evidence/control:** original abstract claims improved tradeoff at the same fine-tuning cost as baselines, up to 1.21 percentage points or 1.33× fewer FLOPs in stated comparisons. Search overhead, training permissions and exact controlled budgets not yet read.
- **Distinguishes:** bad site selection vs no compatible composition; practical efficient search vs intrinsic representation equivalence.
- **Cost/limits:** abstract-level same-cost claim is not a certified complete development-budget ledger. No transfer to language tasks is assumed.

### A06-X08 — TIES-Merging: Resolving Interference When Merging Models

**Source/version/status:** [2306.01708v2](https://arxiv.org/html/2306.01708v2), 2023-10-27; **NeurIPS 2023**, [official proceedings](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1644c9af28ab7916874f6fd6228a9bcf-Abstract-Conference.html). **Depth/role/stage:** targeted introduction, formulation and sign-interference discussion; §7.3 ablations located, not fully read. Composition alternative/counterexample.

- **Prior problem:** merging several fine-tunes loses value through many low-magnitude updates and conflicting update signs.
- **Solution:** trim task deltas, elect a common coordinate sign and average only sign-consistent changes.
- **Mechanisms/learning/units:** sparse weight-delta selection, sign voting and coefficient scaling over common-base model weights; pre-existing task fine-tunes provide learning, not a new state-read mechanism.
- **Evidence/control:** sign conflicts persist after trimming and grow with task count; comparisons include full and parameter-efficient fine-tuning. Exact component-ablation numbers remain unread.
- **Distinguishes:** composition failure from parameter interference vs each single capability being bad; unit norm/parameter count vs coordinate-wise conflict.
- **Cost/limits:** coefficient/density selection and original donor fine-tuning are costs. Update signs are parameterization-dependent; this is not a universal causal explanation of interference in arbitrary independently trained hosts.

### A06-X09 — Editing Models with Task Arithmetic

**Source/version/status:** [2212.04089v3](https://arxiv.org/html/2212.04089v3), 2023-03-31; [official abstract/history](https://arxiv.org/abs/2212.04089v3); ICLR 2023 association, forum decision not freshly inspected. **Depth/role/stage:** targeted abstract/introduction and task-vector formulation; further experiments not fully read. Positive/negative weight intervention alternative.

- **Prior problem:** adapting a pretrained model separately for every behavior does not expose a cheap compositional edit operation.
- **Solution:** form fine-tuned-minus-base weight vectors and add, negate or combine them to steer task behavior.
- **Mechanisms/learning/units:** task-vector subtraction/addition, coefficient selection and shared pretrained coordinate system; existing language/vision model weights, not a text-memory representation.
- **Evidence/control:** original text reports target degradation under vector negation with relatively preserved control tasks, and multi-task improvements by addition. Not a proof of general linear skill additivity.
- **Distinguishes:** selective acute capability modification vs broad destruction; combining shared-origin deltas vs transplanting representations from unrelated bases.
- **Cost/limits:** donor training and coefficient selection remain relevant; cross-base delta transport cannot be presumed meaningful. Non-additive outcomes should be measured with same original base and individual-delta controls.

### A06-X10 — Capacity and Trainability in Recurrent Neural Networks

**Source/version/status:** [1611.09913v3](https://arxiv.org/html/1611.09913v3), 2017-03-03; [history](https://arxiv.org/abs/1611.09913); Collins, Sohl-Dickstein and Sussillo; ICLR 2017 association not independently proceedings-verified. **Depth/role/stage:** targeted §1.1–1.2 and original abstract, main capacity tables/proofs not full-read. Optimization/capacity control, formation.

- **Prior problem:** observed recurrent-architecture advantages can arise from storing task information in weights, history in state, or trainability rather than unique primitives.
- **Solution:** separately stress parameter/task and hidden-state/history capacity across architectures/depths with intensive hyperparameter optimization.
- **Mechanisms/learning/units:** controlled recurrent tasks, Gaussian-process tuning, fixed parameter envelopes with differing hidden widths; synthetic sequences and recurrent units, not a modern language-model capacity theorem.
- **Evidence/control:** §1.2 holds parameter budgets approximately fixed, chooses width accordingly, and reports hundreds–thousands of complete training runs per condition; original abstract describes similar measured capacities despite training-difficulty differences.
- **Distinguishes:** nominal parameters vs state width/useful capacity; inability to optimize vs representational impossibility.
- **Cost/limits:** source calls total expense CPU-millennia. Empirical “~5 bits per parameter” and “one real number per unit” are task/protocol observations, not finite-precision universal storage bounds. The expensive search is a methodological anchor, not a local execution recommendation.

## C. Reuse actual existing full cards — no new reading count

All six card files were read completely this stream. FULL below is the card's declared original scope, **not a new complete original-paper read or reproduction**. Relative links point to existing immutable cards.

| Existing ID / fixed title-version / original URL / venue status | Actual card and evidence depth | Prior problem → one-sentence solution; borrowed mechanism/learning | Distinguishing hypothesis; controls, cost and remaining boundary |
|---|---|---|---|
| **W0337**, What needs to go right for an induction head? A mechanistic study of in-context learning circuits and their formation; **2404.07129v1**; [original](https://arxiv.org/html/2404.07129v1); venue not reverified | [B16/W0337](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0337.md): FULL pp.1–9, App. A–I per card | Final-head ablation confounds formation and redundancy → compare continuous ideal-behavior clamping/formation interventions with endpoint deletion. Borrowed mechanism: causal activation control in a two-layer attention model using frozen visual features and contextual randomized labels. | Formation dependence vs endpoint necessity; App. D fixed pretrained frontends vary by seed, clamping can simplify QK/V coexistence, idealization not natural interface. Extra forward passes not fully compute-matched. No source revisit. |
| **W0204**, MoM: Linear Sequence Modeling with Mixture-of-Memories; **2502.13685v4**, 2025-11-18; [original](https://arxiv.org/pdf/2502.13685v4); venue not reverified | [B16/W0204](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0204.md): FULL main+App. A–I | Single recurrent state suffers capacity/interference → route each input among several recurrent matrix states plus shared memory. Mechanisms: top-k routing, specialized K/V projections, balance auxiliary loss and LM training. | Multi-state benefit vs larger active single state; activity-matched enlarged single-state controls do not match total resident state/projections. Mixed task outcomes and extra total memory remain. Useful fixed-state alternative, not original-text retrieval. |
| **W0210**, Multi-State Linear Attention with Generalized Second-Order Routing; **2610.37645v1**, 2026-10-27; [original](https://arxiv.org/html/2610.37645v1); venue not reverified | [B06/W0210](../../../flued_multigranularity_survey_20261108/03_reading/B06/W0210.md): FULL main/App. B–E, algorithm/cost scopes per card | Mean routing loses relevant key variation → store segment-key first/second moments and combine mean/variance softmax routing. Mechanisms: dedicated routing projections, query-conditioned gating, continued LM+synthetic QA training; fixed 256-token state segments. | Address statistics vs value preservation; comparisons continue-train separate models, **not one fixed value bank with only routing changed**. Extra matrix memory/projections; partial-segment normalization discrepancy in paper remains unresolved. No source pointers. |
| **W0214**, RAM-Net: Linear-Time Sequence Modeling with Sparsely Addressable State; **2602.11958v2**, 2026-10-06; [original](https://arxiv.org/pdf/2602.11958v2); venue not reverified | [B16/W0214](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0214.md): FULL main pp.1–10/App. A–C | Dense recurrent state access and interference → independently choose sparse read/write addresses in a fixed continuous-valued array. Mechanisms: product-structured addresses, top-k search, learned write/read gates from causal LM loss. | Same total read+write quota with different allocation can strongly differ; active state is not total resident state. Conflicts and missed co-location persist. Original title change is same work, but **2610.11214 is a different migration work**. |
| **BIW-0122**, Char2Subword: Extending the Subword Embedding Space Using Robust Character Compositionality; **2010.12730v3**, 2021-09-24; [original](https://arxiv.org/pdf/2010.12730v3); card does not certify venue | [R06/BIW-0122](../../../byte_language_interface_survey/03_reading/R06/BIW-0122.md): FULL §§1–6/App. A–B | Novel character composer may not fit pretrained lexical geometry → imitate embeddings with multiple geometry/identity losses, then contextual MLM through frozen mBERT and optional re-approximation. Mechanisms: character Transformer/pooling, neighbor matching, noisy spelling training, fixed subword output table. | Static local match vs contextual host compatibility; contextualization can reduce neighbor fidelity and later re-approximation changes it. Hybrid route retains old lookup table and is not full storage saving. Character-input/subword supervision, not byte-to-byte generation. |
| **BIW-0126**, Zero-Shot Tokenizer Transfer; **2405.07883v2**, 2025-10-28; [original](https://arxiv.org/pdf/2405.07883v2); card notes NeurIPS 2024, version equivalence not assumed | [R06/BIW-0126](../../../byte_language_interface_survey/03_reading/R06/BIW-0126.md): FULL 22pp/App. A–K | Replacing tokenization repeatedly retrains hosts/embeddings → train a per-host hypernetwork to produce target input/output embeddings across sampled tokenizers. Mechanisms: embedding warmup, shared-token anchors, frozen-host LM training, optional full-host continuation. | Frozen interface vs adaptive-host transfer; manually untied GPT-2 diverges without anchor while tied does not. Changed text/token coverage, substantial hypernetwork training, incomplete transfer and multilingual losses remain. Zero-shot refers to target tokenizer, not untrained adapter. |

## D. Existing unread primary papers — do not pretend they are new discoveries

| Existing work/version/source/status | Specific problem and mechanism | Why still unread; distinguishing question |
|---|---|---|
| **W0201 — Gated Delta Networks: Improving Mamba2 with Delta Rule**, 2412.06464v3; [HTML](https://arxiv.org/html/2412.06464v3); ICLR 2025 association in prior audit, original body not freshly fetched here | Prior state updates trade selective forgetting against delta correction → combine gating and delta-rule memory updates with a complete sequence-model block. Borrowed mechanisms include delta learning, projections, gates/convolution/normalization subject to primary extraction. | No independent registered full card in prior audit. Read §3.4 and full component tables before claiming the project's actual transplant included the proper companion package; local code was not inspected. |
| **W0228 — Parallelizing Linear Transformers with the Delta Rule over Sequence Length**, 2406.06484v6; [PDF](https://arxiv.org/pdf/2406.06484v6); title/version inherited from existing catalog, not newly certified | Delta-rule recurrence creates a sequential bottleneck → parallel training formulation makes the update practically trainable. No exact kernel/normalization comparison is certified at this depth. | Read actual base DeltaNet interface if it, not GDN, is the recipient. Distinguish the central update from the full block and optimization recipe. Do not relabel GDN evidence as proof about all DeltaNet variants. |

## E. ICLR 2027 leads — intentionally excluded from verified-work counts

The [official group API](https://api2.openreview.net/groups?id=ICLR.cc/2027/Conference) was retrieved and confirms venue identifiers, but individual note/forum access was blocked. These titles are **search-returned candidate strings**, not certified title/version/status metadata. Anonymous identities are not inferred. No candidate is described as accepted, or as a demonstrated experimental result.

| Lead / stable forum URL | Why worth verification; proposed problem/solution to check, not established fact | Depth / distinguishing hypothesis / gate |
|---|---|---|
| **The Delta Is Not the Skill: Zero-Prior Elicita…** [OFVWcaGfdi](https://openreview.net/forum?id=OFVWcaGfdi) | Search snippet mentions cross-base LoRA transplantation; could distinguish a portable delta from host-native elicitation. Exact untruncated title and actual proposed mechanism unknown. | Snippet only; direct forum challenge, note API 403. Verify official title, version/date, venueid and status before reading/quoting. No attempt to identify anonymous authors. |
| **Weight Quantization and KV-Cache Eviction Do Not …** [QlvNqskhdY](https://openreview.net/forum?id=QlvNqskhdY) | Search snippet mentions a transplant cell and interaction Δ; potentially a directly relevant two-intervention protocol. Must inspect full paper rather than assume title completion or factorial fairness. | Snippet only; forum/API challenge. Exact title/status/version unresolved; hypothesis: damage interactions vs separate weight/state effects. |
| **The Key Handoff: Retrieval in Hybrid Language …** [TkiAbEpo95](https://openreview.net/forum?id=TkiAbEpo95) | Search snippet describes donor/recipient residual transplant; potentially key/address vs payload handoff. Despite retrieval wording, relevance is intervention design, not adopting source retrieval. | Snippet only; forum/API challenge. Need donor matching, same-host and negative-source controls plus venue/status. |
| **Initializing Linear Vision Transformers** [WRilIg5UPY](https://openreview.net/forum?id=WRilIg5UPY) | PDF search snippet mentions output-matching distillation to initialize linear ViTs; potentially recent constructive repair evidence. | Snippet only; forum challenge. Need official forum metadata/PDF version, initialization controls and downstream adaptation budget. No causal/acceptance claim. |

**Do not use these four to inflate recent accepted-work coverage.** They are precise, searchable unresolved source gaps, not a basis for a 2027 scientific conclusion.
