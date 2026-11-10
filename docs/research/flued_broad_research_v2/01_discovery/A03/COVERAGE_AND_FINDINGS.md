# A03 — Coverage and findings: addressing and native readout

Date: 2026-11-09. This is one discovery-axis deliverable, **not** the broad report or its architecture selection. Companion files: [work/problem inventory](WORKS_AND_PROBLEMS.md), [query/source log](SEARCH_LOG.md), [prioritized reading handoff](READING_HANDOFF.md).

## 1. Scope restored and work actually executed

The governing question is: **given the state that will actually be available at deployment, can the native consumer form an adequate query, recover the intended association, and use its content for the task?** A source-revisit interface is one optional change in information permissions, not the definition of this question. The canonical axis is the addressing/native-readout section of [FOLLOWUP_DIRECTIONS.md](../../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md), not the multigranularity proposal's hypotheses.

Executed in this pass:

- Read the v2 plan and all three preceding [03_ADDRESS_READOUT](../../../flued_multigranularity_survey_20261108/07_scope_recovery/03_ADDRESS_READOUT/COVERAGE_AUDIT.md) audit artifacts; inspect both supplied work catalogs and actual relevant cards.
- Read and reuse **12 actual full cards**, keeping W/BIW identities, source versions and limitations. This is no increase in their original full-reading count.
- Execute **13 public WebSearch queries**, 32 FetchURL requests, and Desktop built-in-browser checks. Reverify/recover **21 work records**: 11 absent from both catalogs, five already in the earlier A03 audit, five existing unread W records. There is no new FULL declaration. See exact request/depth boundaries in the log.
- Recover current 2026 evidence on causal recurrent-memory access, low-rank head-specific KV, key-only factorization, rank pruning, asymmetric calibration, value-side reorganization and recurrent-to-attention utility prediction. Recover classical access/training controls rather than only newer retrieval systems.
- Write proposals for discriminating experiments, **without running experiments, training, code, or production edits**. No registry/default/threshold changes.

This is meaningful expansion rather than a count target. The 21-work discovery set and 12 reused cards are different provenance classes; abstract verification does not imply original full reading, independent proof, artifact verification or venue acceptance.

### Corrections to the earlier audit

1. **Perceiver IO is no longer an unread gap:** the byte survey has the actual [BIW-0117 full card](../../../byte_language_interface_survey/03_reading/R01/BIW-0117.md), locked to 2107.14795v3. Reuse it, not a new full read of the same work. Its byte language experiment is bidirectional masked prediction, not causal byte generation.
2. **Two AsymKV works must not be merged:** Cui/Xu's local-KV merging paper (2506.05410) and Tao/Yu/Zhou's quantization paper (COLING 2025) alter different error operators and report different sensitivities. The shared name does not make their claims contradictory or interchangeable.
3. **Query diversity can survive shared keys:** GQA and LRKV make independent q and independent KV distinguishable. Conversely MoM's multiple states use a shared q; counting memories or the word “head” is inadequate.
4. **Native read-path evidence is still not a query-formation experiment:** the recent causal paper D20 patches query-time outputs and states, not q alone. It improves the causal toolbox without closing the native-query gap by assertion.

## 2. Multidimensional coverage matrix

Action columns are independent: **S** = existing evidence adequate for a bounded mechanism synthesis; **U** = existing literature still unread; **N** = genuinely new/recovered original search contribution; **E** = project-specific discriminating experiment remains necessary. Several can apply simultaneously. “S” never means enough evidence to select a production architecture.

| Canonical subdirection | Existing substantive coverage to reuse | Existing unread / newly recovered original gap | Action and concrete unresolved question |
|---|---|---|---|
| Content vs positional addresses | W0214 mixes positional shifts/content addresses; BIW-0117 uses output positions/tasks | D01 NTM, D02 D-NTM; D19 positional vs content tasks | **S+N+E:** randomize fact position separately from key identity; does a learned positional shortcut break unseen bindings? |
| Per-position vs block-shared addresses | W0197's per-query/head vs shared selection; W0174 keeps token-level values | D03's count-aware merges; D06/W0219 token groups | **S+U+E:** first isolate address sharing with original V and fixed payload permissions, then sweep temporal block size |
| Independent effects of address/content compression | W0197/W0174 make index/payload separation explicit | D03 merging, D16 quantization, D18 calibration, D19 feature-rank reduction | **S+N+E:** temporal granularity, rank and precision are three different compression coordinates; cross K and V interventions at each |
| Value replacement vs key broadcast | Existing audit has the right causal concern but no decisive project-local test | D03 exact equal-key/count identity; D19 keeps full V | **N+E:** K-only change, V-only replacement and their interaction; count/frequency matched comparisons before attributing failure to block size |
| Read/write address alignment | W0214 independently addresses reading/writing and reports quota imbalance | D02 observed content-ignoring shortcut; D14 marginal q/k matching | **S+N+E:** same-slot mass need not mean same fact; use paired identity permutations and donor-value answer flips |
| Native query formation | W0229's bigram construction; W0210's route-q vs read-q; BIW-0117 output-query types | D01/D02 controller formation, D11 query recurrence, D20 read-output mediation | **S+N+E:** trace actual q inputs and formation stage; compare q-only adapters with matched unmodified controls |
| Query-time visibility | Existing cards distinguish causal prefix, bidirectional masked input and fixed learned q | D21 is future-question-agnostic at serving but rollout-supervised offline | **S+N+E:** no future answer/target identity may leak through diagnostics labeled native; report stronger oracle permissions separately |
| Query expressivity vs retrieval target complexity | W0229 exact bigram construction vs regression; W0092 consumer-family optimum | D19 fixed-offset copy vs content match; D11 relational multi-hop tasks | **S+N+E:** exact lookup, noisy similarity and relation composition need separate tasks, not one recall average |
| Key conditioning / stable inversion | W0229 Gram correction; W0212 fixed-write key/value geometry | D07/W0086 low-rank state reduction; D18 calibrated factorizations | **S+U+E:** compare Gram-conditioned prediction error with deployed q margin, not only an effective-rank scalar |
| Key normalization / address separability | W0212 geometry conditions; W0214 temperatures | D13 QKNorm, D05 TransNormer, D15 gating | **N+E:** norm-only, angle-changing and temperature-only controls; normalization can stabilize or dilute |
| Decentering / whitening | W0212 explicitly limits its PCA+whitening findings | D14 distribution matching; D18 CKA/calibration are related but not whitening | **S+N+E:** use fit-on-training-only means/covariances and co-transform q and stored K/state; K-only whitening changes the function |
| q/k/v scale coupling | W0229 output norm; W0237 shared denominator | D03 cardinality, D13 learned g, D15 gate locations | **S+N+E:** measure logit margins, entropy, read norm, residual-stream norm and gradients separately |
| Gate effects on addressing vs returned content | W0210 routing-mixture gate; W0214 write/read controls | D15 contrasts post-q/k, value, attention-output and final-output gates | **S+N+E:** keep key scores fixed while changing consumption gate; a suppressed return is not missing storage |
| Independent vs shared slot addressing | W0204 shared-q multi-state route; W0214 per-head slot arrays | D10/W0100 competitive slots (original unread), D20 cross-fact coupling | **S+U+E:** independent storage locations, independent queries and learned semantic independence are distinct |
| Multi-head readout specialization / capacity | W0197's selection sharing controls; W0287's multihead negative result | D12 GQA, D17 LRKV, D18 host-dependent head compression | **S+N+E:** fix total bits, write bank and return width, then vary q independence, K/V independence and fusion |
| Independent layerwise writes vs reused summary | W0287 depth-source sums; W0289 mixed historical values replace originals | D04 CLA single KV writer/multiple readers; D11 layerwise vs adjacent tying | **S+N+E:** distinguish fewer writers, shared destinations, depth mixing and shared parameters; compare these contracts, not just layer count |
| Readout initialization / learning reachability | W0214 initial biases/temperatures; W0092 no optimization guarantee | D02 curriculum, D11 linear start, D12 conversion init, D19 matched q/k fine-tuning | **S+N+E:** frozen failure, adapter recovery and jointly learned success are different outcomes |
| Offline best readout vs native deployment | W0229 analytic/ridge vs online; W0092 family-optimal vs trained consumer | D20 deployed causal path; D21 predictor-tail vs global correlation | **S+N+E:** report native behavior first, then equal-permission trained readers, then oracle upper diagnostics |
| One-step vs iterative retrieval | BIW-0117 reads one latent array with distinct queries; W0229 local/global regressors | D09/W0240 conditional one-step theorem; D10/W0100 iteration; D11 hop comparisons; D02 multistep access | **U+N+E:** adaptive q updates vs repeated same read vs equal-compute non-read transform; hold accessible bank unchanged |
| Exact, approximate and relational queries | W0212 exact stored-key restriction; W0229 cue-response construction | D09 basin/cluster averaging; D11 multi-hop; D19 identity-selection tests | **S+N+E:** type the query/task, preserve answer-independent inputs and measure relational binding, not only nearest-key accuracy |

### Cross-axis obligations, not a new governing proposal

- Compression/task sufficiency (axis A): fine addressing cannot recover an unrepresented independent detail. Conversely an oracle probe success does not certify deployable sufficiency.
- State retention/interference (axis B): a query can be correct while a subsequent overlapping write destroys its binding; D20 and W0229 separate this from read-time matching.
- Actual use (axis D): matching/source weight is not content dependence. Natural donor-value replacements with expected answer changes are stronger than arbitrary zeroing alone.
- Learning dynamics (axis E): D02/D11/D12 provide optimization/init/curriculum counterexamples to immediate architectural rejection.
- Composition/transfer (axis F): D18's host differences and D21's host-specific retraining demand explicit adaptation/host budgets. No cross-paper score comparison establishes transfer.

## 3. Original findings that materially change interpretation

### 3.1 Closed recurrent memory can be causally read, without behaving as independent KV slots

[How Linear Attention Remembers, D20](https://arxiv.org/html/2609.33093v1) §§2.3–4.2 is the strongest newly located direct native-use evidence in this discovery set. In pretrained pure GLA/GDN models, content-consistent donor writes influence later recall; pre-query state swaps and query-time output patches support a linked write–retain–read path. Norm-matched random/control-head interventions do not reproduce the same answer shift. These are stronger than an offline probe.

But selective editing does not imply independent storage: fact-direction components can have opposing collateral effects, and blocking one head can hurt more than blocking many because of nonadditive interactions. Load and distance are varied separately. These findings make **interference geometry and actual read pathways** first-class alternatives to “the granularity is too coarse.”

**Limits:** main evaluation is four-choice likelihood recall with selected competent models/components; the free-vocabulary prose pilot does not meet its competence prerequisite. The pure/hybrid comparison uses separately trained released checkpoints. It does not isolate q-only formation, nor prove all natural-language tasks use the same circuit.

### 3.2 Three meanings of “asymmetric K/V” must remain separate

- [D03](https://arxiv.org/html/2506.05410v2) approximates local keys and exactly aggregates values **relative to the equalized-key operator**, with count-aware normalization.
- [D16](https://aclanthology.org/2025.coling-main.158/) says key **quantization error** is more harmful in its tested settings.
- [D19](https://arxiv.org/html/2603.04427v3) and [D18](https://arxiv.org/html/2607.24331v1) exploit **feature/subspace redundancy**, with adaptation/calibration and host-dependent failure.

These do not support a universal ordering “keys are easier/harder to compress than values.” A logit perturbation, replacing temporal addresses, and truncating a trained subspace have different error propagation. This is enough to improve the synthesis taxonomy now; selecting a particular K/V policy still requires experiments.

### 3.3 Normalization is not synonymous with better addresses

[D13](https://arxiv.org/html/2010.04245v1) normalizes q/k and learns the logit scale. Removing that scale is its strongest reported ablation loss; cosine logits can be too diffuse. Main baseline differences include LayerNorm vs ScaleNorm. [D05](https://aclanthology.org/2022.emnlp-main.473/) separately targets unstable gradients and early-layer dilution, but only its abstract is verified here.

**Inference:** when stored content looks recoverable but native output is weak, measure at least direction, norm, temperature, denominator and downstream gate before adding more memory. A whitening transform can make a linear system easier to solve while simultaneously destroying the existing q-to-key convention if applied only to one side.

### 3.4 Alignment has at least three non-equivalent meanings

1. D02: reading locations previously written, to discourage using fixed address embeddings as a parameter shortcut.
2. D14: matching marginal q/k distributions, through adversarial or transport regularization.
3. W0229/W0212: conditioning or separating the joint key/value association geometry.

A permutation of identities can preserve the marginal q/k distributions while breaking the desired binding. High read/write overlap can select the wrong semantic entry. An orthogonal state direction need not be causally independent. Hence “alignment improved” must specify which observable and which functional binding changed.

### 3.5 Shared K/V does not make all queries identical; multiple states do not ensure independent queries

[D12 GQA](https://arxiv.org/html/2305.13245v3) preserves distinct q heads while sharing grouped K/V; [D17 LRKV](https://arxiv.org/html/2601.11471v3) adds head-specific low-rank residuals and studies q/k bilinear operators. Conversely W0204 uses shared q across multiple matrix states. If reading is linear with the same q, mixing states and then reading can be equivalent to reading then mixing. An independent-q or nonlinear-fusion arm is needed to make this test nontrivial.

This also protects against overclaiming: D17's weight/operator diversity is not itself demonstrated semantic binding independence, and its introduction has a numerical contradiction (2.6 GB claimed greater than 5 GB). Use its specific operator design and controls, not its unchecked headline rhetoric.

### 3.6 Replacement failure and adaptation success cannot be collapsed

D12 explicitly converts MHA checkpoints by mean-pooling heads and then adapts them. Zero-step, 5% and 10% uptraining curves show markedly different behavior for MQA and GQA. D19 likewise compares q/k-only fine-tuning against identically fine-tuned uncompressed controls and reports domain-sensitive repair. These are original precedents for a **replacement-by-adaptation interaction**, not permission to explain every failure away as insufficient training.

The immediate frozen effect measures interface disruption; the matched adapted effect measures reachable performance under a named budget. D19's claim that GQA cannot be converted after pretraining is contradicted by D12's original purpose. D19's exact-equality notation also follows an approximate truncated-SVD factorization, so equality must not be quoted unconditionally.

### 3.7 Cross-layer sharing, depth mixing and multiple writers are different experiments

CLA (D04) has one writer's KV reused by multiple layers with their own queries. Attention Residuals (W0287) mixes same-position depth outputs, with fixed learned pseudoqueries. Depth-Attention (W0289) replaces values with mixtures and retains keys. None alone isolates multiple independent layerwise writes into the same compressed bank. Reducing the count of resident KV copies also does not automatically reduce the number of reads or bandwidth.

### 3.8 Iteration can refine an address, perform reasoning, or amplify a wrong attractor

[D09 Hopfield](https://arxiv.org/html/2008.02217v3) conditions one-step recovery on separation/query proximity; averaging and metastable minima are genuine alternatives. [D11 MemN2N](https://arxiv.org/html/1503.08895v5) updates the query across hops, with learning, tying and initialization choices; not every task row improves with more hops. Slot Attention's actual update/normalization is still unread here. None justifies a blanket “iterative retrieval beats one-step” claim.

**Needed:** equal bank permissions, repeated-first-read and equal-compute no-read controls, plus query noise/relational depth sweeps. An extra read and an extra computation are different causal changes.

### 3.9 Predictive recurrent control does not contradict attention-carried answer identity

[D21 GateSight](https://arxiv.org/html/2610.14754v1) predicts future token-KV utility from recurrent gates/magnitudes. Its supervision is sampled continuation-layer influence, not answers; serving scores use no future question. This can coexist with D20's finding that the tested hybrid answer identity is carried immediately in KV. One measures useful control signals; the other measures a storage/read causal boundary. Neither says recurrent computation is generally unnecessary.

## 4. Minimal discriminating experiment proposals — not executed or preregistered

These proposals diagnose alternative causes. They do not alter any project threshold, canonical configuration or registry. All thresholds, if later proposed, must be calibrated to the actual stage, host, seed window stream and hardware environment; do not transplant an external number. First establish task competence and exact replay.

### E1. True replay anchor and factorial K/V replacement

For one fixed host, checkpoint, causal window stream, query formation and update schedule:

| Arm | Address path | Payload path | Primary question |
|---|---|---|---|
| Identity | Original K / original address semantics | Original V | Is the intervention wiring itself faithful? A new projection or normalization at block size 1 is not identity |
| K-only | Shared/coarse K, same V/time positions | Original V | Does address replacement alone hurt? |
| V-only | Original K | Same summary V broadcast to original positions | Does payload replacement alone hurt? |
| Both | Same K manipulation as K-only | Same V manipulation as V-only | Is there an interaction that single-arm repair misses? |

Record K/query norms, key Gram spectrum, score/selection distributions, V/read norms, gate values, update counts and next-output changes. Include **length-/format-matched natural donor values**, irrelevant donors and self-replacement. When donor content changes the true answer, require the predicted answer change rather than merely a loss increase. This distinguishes address damage, content damage and arbitrary abnormal activation effects.

Only after these are characterized should temporal block size be swept. A C64-to-C8 gain alone changes granularity, number of addresses, writes and often total state; it cannot decide which factor mattered.

### E2. Broadcast multiplicity and operator semantics, separately from temporal granularity

Keep the summary and query fixed. Compare per-original-position copies, one write per block, and an explicitly count-/mass-matched representation. For softmax equal keys and values summed within group g,

`y(q) = sum_g exp(q·k_g) * sum_{i in g} v_i / sum_g c_g * exp(q·k_g)`.

This identity assumes equal keys **within each group** at the comparison boundary; it is not an identity for the original unequal keys. With mean values instead of sums, multiply the numerator by c_g as well.

For a recurrent delta update, repeated writes also apply repeated erasure/correction and state transitions: there is no automatic softmax count identity. Compare update frequency and elapsed-step decay explicitly, rather than rescaling the final output and calling the updates matched. Include identical-summary duplicate blocks to expose accidental frequency advantages.

**Discriminates:** repeated-mass distortion vs destructive overwrite vs genuine absence of detail. Report all three, not one “broadcast ablation.”

### E3. Native query formation and supervision permissions

Freeze a single written bank and evaluate the same held-out source/identity/query distribution with:

1. Actual deployed q, with its exact local/context inputs recorded.
2. A q-only adapter of named capacity trained only from permitted task loss, with no future answer or target identity in its input.
3. A same-budget uncompressed/self-interface q adapter as a control for generic adaptation benefit.
4. A flexible separately trained readout, with its added parameters, labels and compute declared.
5. Correct-address and analytic/ridge diagnostics, explicitly **stronger-permission** ceilings rather than deployment arms.

Cross q with native vs known-good bank where the feature spaces are compatible; if not, a connector is a separate intervention and must be measured. A q adapter's success on a finite benchmark does not prove arbitrary future-query sufficiency. Holdout must exclude source/identifier memorization.

**Interpretation:** oracle succeeds/native fails localizes a usable opportunity under stronger permissions, not a learned solution. Equal-permission q-adapter repair supports a reachability/interface hypothesis. All readers failing does not by itself prove information loss if their approximation/optimization is weak.

### E4. Conditioning, normalization, rank and gate location

Separate three stages: matching logits/addresses, state/value retrieval, downstream consumption. Use a small staged comparison rather than changing them simultaneously:

- Original operator; norm-only changes; temperature-only changes; norm+learned-temperature; centering/whitening fit on training sources only.
- Paired coordinate transformations of K and q (and state where necessary) vs one-sided transformation, to separate coordinate repair from a genuinely different similarity function.
- Same-state Gram/ridge-conditioned diagnostic vs deployable online preconditioner; report any extra sufficient statistics/solve costs.
- Gate before q/k scores vs gate after retrieved value vs final residual gate; compare both unclipped and scale-matched outputs.
- Effective state rank, score-matrix rank and query-sensitive directions separately. Causal masking can change matrix rank; an unmasked low-rank QK product is not a proof about the masked attention matrix.

Measure functional content-selective changes, not just condition number, entropy or rank. D07 is a counterexample route to “low rank must be bad”; D13 is a counterexample to “unit norms alone must be good.”

### E5. Slots, heads and independent access under fixed resources

First hold the **same written bank** and total returned width fixed: shared q/linear mixing; independent q per partition; independent q plus nonlinear post-read fusion. Where all branches are linear with the same q, verify the expected equivalence before interpreting a difference.

Then compare banks with equal total state bits and declared precision: one wide state vs several narrower states; independent K/V projections vs shared K/V with distinct q; fully separate vs shared writes. Equal active elements, equal resident bytes, equal parameter count and equal compute are different matches; do not claim all simultaneously unless actually achieved.

Tasks must include repeated keys with conflicting values, near-neighbor keys, multiple independently queried facts and relational joins. Measure read/write coaddressing, semantic confusion, target flip and collateral damage. Independent allocated slots are not automatically independently learned facts.

### E6. Depth/writer/read sharing

Hold accessible history and resource ledger fixed or separately report the changed frontier:

- Independent layerwise banks/writers/queries.
- One earlier writer, shared KV, independent layer queries (CLA-like).
- Multiple writers into one bank with named update ordering.
- Same-position depth value/residual mixing (W0289/W0287-like), not relabeled shared-memory writing.

Use same-host self-splice/replay controls and explicitly report old-summary staleness, writer interference, query specialization and all rereads. If shared-bank updates change causal ordering, that is another factor, not a harmless implementation choice.

### E7. One-step vs iterative read without information privilege expansion

Fix the bank, stored content and initial q. Compare one read; repeat the identical q and aggregate; recurrently update q from previous returned content; add an equal-compute transformation without extra reads. Separate tied and untied query-update parameters or match their counts. Do not silently add original source access in the iterative arm.

Vary cue noise, distractor overlap and relational composition depth. Track whether iterations improve address margin or merely sharpen an incorrect attractor; exact matching, approximate completion and multi-relation joins have different success conditions. Include non-target factual collateral and latency/temporary states.

### E8. Replacement × adaptation × granularity

Apply a staged factorial rather than a single adapted candidate vs frozen baseline. For each selected granularity and replacement operator, compare frozen, connector/q-only, reader-only, writer-only and joint adaptation, with matched unchanged/self-interface controls. A reduced first-stage set can prioritize frozen and q-only before any joint training is authorized.

Keep identical training bytes, window stream, steps/compute, initialization protocol and evaluation sources within each contrast; report any budget that cannot be matched. Analyze candidate improvement **minus** control improvement, not recovery relative to its own disrupted t=0 alone. Track early, intermediate and final content dependence as well as task loss. No universal acceptable-drop or adaptation-budget number is set here.

## 5. Independent alternatives that do not require revisiting source text

These are competing mechanisms, not an ordered recommendation or approved experiments.

| Alternative | Changes and direct evidence | Missing discriminator / unavoidable cost |
|---|---|---|
| Improve native query formation | W0229 bigram construction, BIW-0117 output-query permission examples, D02/D11 controller/query training | Same frozen bank and equal-permission q-only repair; more supervision cannot be hidden |
| Separate key and value design | D03 merging, D16 bit allocation, D18/D19 rank/subspace choices | Error operator and adaptation matter; no universal K/V compression order |
| Condition/precondition closed-state reads | W0229 regression/Gram; W0212 joint geometry; D13 scales | Statistics/solves and online learnability; cannot recover discarded independent detail |
| Fix read/write training alignment or shortcut | D02 observed fixed-address shortcut and curriculum; D14 distribution alignment | Pairwise semantic binding vs marginal closeness; auxiliary loss can itself create a shortcut |
| Redistribute finite memory into independent access paths | W0214/W0204 plus D12/D17 head diversity; D20 interference controls | Fixed total bits vs active state and true independence; collisions and optimization remain |
| Change value-side writing/retention | D08 two-sided delta candidate, W0229 residual correction, D20 overlap interventions | D08 full original unread; isolate overwrite, decay and alignment, not only end-task average |
| Add explicit finite internal exceptions | W0237 exact projected KV exceptions with shared denominator | This adds information to state but not original-text revisit; eviction, selection and total bytes remain |
| Iteratively refine queries over the same closed bank | D09, D11; D10 unread classic | Extra read vs extra compute; wrong basins and incomplete retained evidence |
| Alter depth communication / writer reuse | D04, W0287/W0289 | Fewer stored copies may still require many reads; no proven universal shared-summary writer |
| Change objectives/staging rather than memory topology | D02 regularizers/curriculum, D11 linear start, D12/D19 adaptation controls | Must show task/content dependence survives without a privileged route; adaptation benefit is host/budget-specific |

## 6. Coverage limits and decision boundary

**Enough to synthesize now:** distinct q types/visibility; address/payload/precision/rank compression; separate read/write bindings; conditional normalization/geometry; sharing along token/head/depth axes; frozen replacement vs adaptation; closed-bank iterative alternatives.

**Not enough to choose an architecture:** no paper establishes the exact cause of this project's native-readout failure. E1–E8 remain new empirical questions, not missing citations. The literature does not eliminate closed-state repair, non-retrieval write reform, query-objective changes, or a finite exception cache.

**Still unread or incomplete:** priority original queue has 15 works with precise questions. Slot Attention HTML failed twice; abstract/metadata is all that is claimed. D05/D07/D08/D16 remain abstract-level. Other new papers are targeted partial reading, not FULL. Venue revisions and implementations are not exhaustively audited.

**ICLR 2027:** official group URL was requested, but the built-in browser returned a verification challenge and FetchURL returned a loading shell; one relevant official forum also returned a challenge. Search-index candidates are retained only as **unverified leads**, with no author matching/deanonymization, no acceptance assumption and no claim of venue-wide coverage. See log/handoff for exact links and state.

The stopping point is an actionable axis-level coverage and experiment map, not field exhaustion, final architecture selection or final total-report synthesis.
