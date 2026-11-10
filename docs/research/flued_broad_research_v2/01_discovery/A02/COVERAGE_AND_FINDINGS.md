# A02 — State writing, retention, capacity, and interference

Date: 2026-11-09. Scope: native recurrent/linear/SSM/fast-weight memory and nonlinear associative alternatives. This is a completed discovery pass and question-level coverage assessment, **not** a final total-report synthesis, architecture selection, experiment registration, or claim of field exhaustion.

## 1. What was executed

Read the v2 [PLAN](../../PLAN.md), the original [FOLLOWUP_DIRECTIONS](../../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md), all three previous [state-memory audit artifacts](../../../flued_multigranularity_survey_20261108/07_scope_recovery/02_STATE_MEMORY/COVERAGE_AUDIT.md), relevant catalog entries and nine actual existing full-reading cards. Searched public sources and directly retrieved original proceedings/arXiv/OpenReview pages, with targeted body reading rather than metadata-only enumeration. See [SEARCH_LOG](SEARCH_LOG.md) for exact queries, failures and reading ranges.

The resulting [work inventory](WORKS_AND_PROBLEMS.md) contains **26 externally reverified/recovered work entities**: 13 existing-catalog works, four previous-audit candidates, and nine missing standalone entities/new-to-inspected-catalog works. The last class includes Longhorn, already discussed within an existing card; it is not a claim of first intellectual discovery. **Nine existing full-reading cards are reused separately, not counted as new full reads or new works.** Five OpenReview leads remain unverified and outside the 26. This is an observed useful set, not a quota or a field-size estimate.

No main-axis conclusion is conditioned on supporting a multigranularity/source-revisit proposal. No original text archive is required by the leading independent alternatives below. Stored pattern banks, bounded recent update buffers and compressed recurrent state are still different access/cost regimes.

## 2. Four meanings of “capacity” that must not replace one another

| Meaning | What counts as evidence | Available anchors | What it does not establish |
|---|---|---|---|
| **Finite-bit capacity bound** | Distinguishable finite states under specified source distribution, access passes and error criterion | W0061 existing card, exact uniform whole-string copying | Natural-language entropy, any specific BF16/FP32 effective capacity, or trained long-context task use |
| **Expressibility / representational existence** | A memory/read function or sequential circuit can implement the task under explicit assumptions | W0229 constructions; W0240/N08 nonlinear association; N07 regular-language expressibility | Optimizer reaches it, stable finite-precision deployment, unknown-query retention, or equal total storage |
| **Trainably reachable capacity** | Controlled training at fixed mechanism/state; failure versus success as optimization/coverage changes | E05 learning-rate/width/depth study; P03 curricula and seed outcomes; E12 optimizer analysis | Removal of finite-state bounds, broad OOD generalization, or no cost for hyperparameter search |
| **Accessible and actually used memory** | Native recall and correct-value dependence, ideally counterfactual answer reversal and no-binding controls | E06 bidirectional gate patches; P03 rebinding controls; N04 functional compression tests | That a probe/reconstruction/oracle reader is the deployed query, or that any score drop proves specific semantic use |

“Finite-feature” in W0212 means feature dimension, not floating-point precision. W0245's top-1 threshold assumes Gaussian embeddings and an available candidate target bank; its fixed-fraction list is not a constant-size return list. Atlas W0217's existing card flags proof/quantifier concerns; preserve them rather than quoting its title as a general capacity certificate.

## 3. Concrete findings newly sharpened by original sources

### 3.1 Residual writing reduces one kind of error, not every kind of interference

For an illustrative unit key with an explicit delta step,

`S' = S + beta (v - S k) k^T`,

so a query q changes by `beta (v - S k) (k^T q)`. This algebraic observation is ours, not a new empirical result: exact correction at k when beta=1 still changes other correlated queries. Repeated identical keys with contradictory values require a task-defined policy (first binding, latest binding, or context-sensitive choice); they cannot all be “correctly retained” under one unqualified label.

E01/W0199 supplies the original additive-versus-corrective lineage. E02/W0201 §3.1 explicitly combines decay and correction; its §3.2 negative retention case prevents “more forgetting is always better.” Existing W0229 separates covariance-aware regression from online residual SGD. W0212 supplies update-specific key/value interference geometry with explicit counterexamples, not a universal ban on correlated keys.

### 3.2 “Decouple erase and write” names at least three distinct changes

- **E03/W0202 GDN-2:** separate channel-wise erase and write **strengths**, with channel-wise decay.
- **P04/EDA:** independently choose **where** to erase, then perform the ordinary key-directed delta write.
- **E04/W0203 Dual DeltaNet:** reorganize addresses using **value-side** as well as key-side information.
- **N05/KronLSTM:** change matrix-space revision geometry so collateral effects depend on joint key/value overlap, per the inspected introduction and abstract.

These are alternatives with different hypotheses, not interchangeable aliases or an established priority order. Abstract benchmarks do not decide which edit is needed in a particular host. An independent erase direction can still overlap useful queries; selecting a direction does not magically identify future-irrelevant content. Full equations, stability constraints and same-budget controls are still missing for these recent works.

### 3.3 Two kinds of late relevance must be separated

**Depth-late relevance:** E06/W0213 studies a query already given before the phonebook. Local flags, target-gate patches in both directions and layer probes indicate that relevance reaches useful gates too late across layers in the examined pretrained Mamba models. Privileged oracle gate scaling shows a controllable route, not a learned deployable policy.

**Time-late relevance:** the query becomes known only after writing the history. Here no current prediction-error or surprise statistic alone can know an arbitrary future query. W0061 is enough for a conditional finite-bit warning; none of the newly inspected papers proves optimal retention for an unrestricted future query distribution. Do not use the query-first flag repair as a solution to unknown-future-query compression.

A practical state-only route remains possible: give the write policy a better *causally available* summary of context, train delayed-query objectives, or reserve capacity for unknown relevance. That is a research hypothesis, not a reason to smuggle future queries into training-time/inference-time gates.

### 3.4 Some apparent architectural failures are trainability failures, but the correction is conditional

E05 original §§3–8 shows that finer learning-rate searches and width/depth choices can rescue recurrent associative recall and copying. Its convolution removal result is not identical to P03's larger matched-LR convolution effect: P03 explicitly retunes, narrows the delta-family convolution gap, and distinguishes its reference diagonal cell from the official Mamba-2 kernel. There is no defensible universal “convolution is essential” or “convolution is unnecessary” conclusion across these task/training settings.

P03 gives a particularly useful negative control: at fixed recurrent state, a cell can store many adjacent bindings yet fail on four bindings separated by distractors; curriculum changes seed success. Shaped versus success-gated schedules extend the demonstrated boundary, but toy length 512 and a few controlled task families do not establish arbitrary context extrapolation. Its shaped collision experiments find **no measurable causal-versus-bidirectional advantage**, undermining the tempting claim that native reverse scanning is itself the observed cure.

**Source inconsistency to preserve:** P03 §4.2's expanded decay test is nonsignificant (20 seeds, p=.86), while §10 still presents a −.32 decay tax as real. §9/§10 retain older length/directionality language despite §6/§7 updates. Prefer qualified specific results and request artifact/version reconciliation, not a clean headline assembled from contradictory passages.

### 3.5 Numerical precision is now an evidenced mechanism, not just an unfilled search label

N01/LeapQuant §4.4 exposes a substantial per-step BF16/INT8 degradation and a recovery from less-frequent quantization, compensators and smoothing. This directly fills part of the old audit's finite-precision gap. The remedy retains recent high-precision update tuples and compensator vectors; “8-bit state” is not total 1-byte-per-entry memory, and equal state shape is not equal storage.

N04/SPARE keeps recurrent states FP32 while reducing their rank. Its compressed retrieval degradation, heterogeneous-versus-uniform tradeoff, and write-compensation ablations show that rank loss is task-sensitive. N02's abstract-level report that low-rank heads can be important further blocks treating spectral energy as a direct measure of useful capacity. These papers motivate separate precision and rank controls, not a single “memory size” knob.

N05's bounded expected norm claim, HiPPO's function-approximation stability and delta-rule contractions address different mathematical objects. None was verified here as a uniform finite-precision guarantee for arbitrary content, stream length and queries.

### 3.6 Nonlinear association is essential, but not automatically fixed-state compression

E08/TTT, E09/Titans and existing Atlas W0217 store an adaptable function, offering state-only or bounded-replay alternatives to original-text retrieval. Inner objectives, function class, optimization steps and auxiliary states must be costed separately. W0217's negative recall comparisons and proof cautions prohibit declaring nonlinear capacity solved.

E10/W0240 and N08/Dense Associative Memory change associative dynamics/energy. E11's original practical study shows that ideal pattern capacity can coexist with metastable failures on correlated real inputs; pretrained encoding helps identity retrieval of latent reconstructions. However, the pattern matrix is still present. These are independent no-original-text-bank alternatives, **not evidence for constant-size state at exponential total bit capacity**. Unknown language-query generalization and online overwrite policies remain open.

## 4. Key subdirections mapped to actual next actions

Labels are deliberately nonexclusive: **S** = enough existing synthesis for a bounded claim; **R** = existing work/card needs reading or focused reconciliation; **D** = targeted discovery/source search; **X** = a genuinely new, not-yet-run discriminating experiment. “S” never means enough to select an architecture.

| Original state-memory subdirection | Available substantive coverage | Existing unread / new-search gap | Concrete next action and what would distinguish it |
|---|---|---|---|
| Raw feature vs residual/error writing; delta vs addition | **S:** W0229 regression/card and E02 inspected formula | **R:** E01 original controls, W0228 parallelization; E03/E04 only abstract | Compare fixed projected KV and update-order under matched state; repeat-key correction and unrelated-query damage separately (**X**) |
| Independent write/forget strengths | **S:** E02 equations, retention/filtering contrast | **R:** E03 original gate equations and ablations | Recover whether gate axes, parameters or normalization co-vary; only then equal-budget strength-only contrast (**R→X**) |
| Independent selective erase vs global decay | **S:** mechanism distinctions now explicit | **R:** P04 full original, E03/E04; **D:** task-defined stale/obsolete association controls | Preserve first/latest/context-tagged policies separately; useful-old versus obsolete-old erasures with independent address overlap (**X**) |
| Overwriting vs cumulative interference | **S:** W0212 fixed outer-product analysis, W0229 nonstationary RLS negative, E02 haystack cases | **R:** originals of newer edit mechanisms | Hold delay fixed, add correlated distractor writes vs no writes; then same key versus new key at equal load (**X**) |
| Correlated/nearby keys and conflicting values | **S:** W0212 joint Gram caveats; N05 joint-overlap motivation | **R:** E01, E04, N05 controlled originals | Independently vary key correlation and value correlation, not just random-key load; ground truth policy explicit (**X**) |
| Late relevance and unknown importance at write | **S:** E06 depth-late query-first mechanism | **R:** E06 full task/patch controls; E09 surprise objective; **D:** temporal unknown-query objectives | Cross query-first/query-last and local flag/no flag; no future information to production gates (**X**) |
| Finite precision and long-stream numerical error | **S:** W0061 true finite-bit caveat; N01 new original negative/repair | **R:** N01 full derivation/long-context/error-control data | Match total bytes including buffers; compare FP32/BF16/INT8, quantization frequency and norms on identical state updates (**X**) |
| Rank and effective versus nominal capacity | **S:** N04 functional compression tradeoffs, W0245 model restrictions | **R:** E13 theorem, N02 importance probes, N04 calibration transfer | Same rank budget with key-space rotation, content-specific answers and OOD key/query directions, not only NLL (**X**) |
| Multi-state/head/partition allocation | **S:** W0204/W0214 actual cards show active versus total-budget mismatch | **R:** N03 original tensor-state controls; **D:** byte-matched competing organizations | Match all persistent state/projection/route costs and compare one matrix, several matrices, sparse arrays, triadic state (**X**) |
| Long delay versus item load versus interference | **S:** P03 orthogonalized task construction and binding controls | **R:** P03 artifact reconciliation; E07 original MQAR generator | Three independently varied axes plus matched no-binding floors; do not equate longer context with more stored independent items (**X**) |
| OOD queries and state accessibility | **S:** W0212 explicitly only exact keys; E11 cross-modal query branch is relevant but partial | **R:** E11 remaining heteroassociation/appendix; **D:** held-out symbols, query noise/paraphrase, composition | Separate unseen symbols, longer gaps, key noise, binding distribution, semantic paraphrase; no single OOD score (**D→X**) |
| Linear versus nonlinear state | **S:** W0229 taxonomy and W0217 negative/cost caveats | **R:** E08/E09/P01 full originals; N08 energy assumptions | Match learned parameters, fast-state bits, inner steps and recent replay; retain linear and MLP baseline at equal training exposure (**X**) |
| Predictive state / task-related memory | **S:** P02 measure-dependent approximation clarifies a different objective | **D:** original predictive-state representation literature not systematically searched in this pass | Need a source-grounded mapping from prediction-sufficient statistics to delayed fact queries before claiming coverage; remains a real discovery gap |
| Upper bound versus reachable capacity | **S:** W0061/W0245/W0212 restrictions and E05/P03 counterexamples | **R:** E12 proof/one-step versus multi-step settings | Native versus oracle reader and optimizer/curriculum crossing at same state; prove only necessary conditions under stated distributions (**R→X**) |
| Curriculum and trainable capacity | **S:** E05 tuning and P03 original schedule/seed controls | **R:** full P03 artifacts and E05 appendix; byte BIW-0108 is a methodological control, not a memory result | Report solution probability and failure seeds; allocate comparable tuning budgets and test held-out distributions (**X**) |
| Exact long memory without original-text revisit | **S:** finite-bit impossibility for unrestricted uniform copy, not unrestricted tasks; actual state-only alternatives exist | **R:** nonlinear/sparse state variants, E01 basic controls | Bounded task family, total bits and query distribution declared; explore update/retention/learning/numerics before asserting source retrieval is necessary (**X**) |
| “Stored” → native read → final content-specific use | **S:** E06 patch/reader distinction, P03 rebinding, N04 recall | **D:** state-only semantic content-use evaluations matching these mechanisms | Correct/incorrect naturally matched binding replacement, answer reversal and address-preserved content control; probes are diagnostics only (**X**) |

The predictive-state and semantic-OOD gaps are not filled by adding titles from neighboring literatures. The appropriate disposition is targeted source discovery, not “sufficient” or “field exhausted.”

## 5. Independent alternatives under no original-text revisit

| Route | Representative verified/reused evidence | Saved object and information permissions | Best discriminating question before architecture selection |
|---|---|---|---|
| Error-corrective/implicit regression | E01/E02, N06; W0229 | Fixed matrix, plus covariance/inverse statistics if RLS used; no source text | Is failure correlated-key bias, unstable updates, or unavailable relevance? |
| Independent retention/erase/edit geometry | E03/E04/P04/N05 | Matrix plus gates/projections; future queries unavailable | Can targeted removal spare still-useful overlapping facts under equal total cost? |
| Neural fast state / nonlinear associative function | E08/E09/P01; W0217 | Adaptable linear/MLP weights; optimizer state and bounded replay vary | Does benefit survive matched fast bits, inner update count and training budget? |
| Sparse/partitioned same-scale state | W0204/W0214, N03 | Multiple matrices, array slots or tensor state; not text sources | Is gain due to isolation/addressing or simply larger total state? |
| Time-weighted signal statistics | P02; W0229 | Polynomial coefficients or weighted regression statistics | Are these sufficient for the intended query family rather than just reconstruction? |
| Trainability/objective repair | E05/P03/N09; BIW-0108 as intervention caution | Same state, altered training/curriculum and use constraints | Does learning become reliable across seeds and held-out symbols without new memory? |
| Numerical/rank allocation reform | N01/N02/N04/E13 | Compressed states, shared bases; N01 bounded projected-update buffer | Can physical-byte savings preserve the rare low-energy binding, not only NLL? |
| Nonlinear pattern/prototype association | E10/E11/N08 | Stored latent patterns, prototypes or higher-order interactions; no raw text but bank cost may grow | What is the true storage budget and failure basin for correlated/OOD queries? |

These routes are not mutually exclusive; combinations require interaction controls. A state-only method need not reproduce arbitrary source text to solve a bounded task, but it cannot promise arbitrary exact unknown queries below an applicable finite-bit lower bound.

## 6. Minimal experiment questions for a later authorized phase — none executed

1. **Write rule × geometry:** fixed projected keys/values, additive/delta/implicit and newer edits; independently vary key overlap, value overlap, same-key update policy. Read old and new associations immediately and after matched interference. Distinguishes fitting bias from collateral overwrite.
2. **Relevance availability × timing:** query-first/query-last, local oracle flag only as a diagnostic, learned gate versus gate repair; hold load/gap fixed. Distinguishes capacity pressure from depth-late selection. An oracle arm is never a deployable solution.
3. **Load × delay × distractor similarity:** independent grid, rebinding/no-binding floors and full seeds; repeat with controlled curriculum and tuning budgets. Distinguishes forgetting, interference and failure to learn binding.
4. **Physical bytes × precision × rank:** charge state, optimizer, compensators, replay and bases; compare the same updates/readout under rank reduction and quantization separately. Distinguishes information budget from numerical execution failure.
5. **Accessible versus used:** an offline optimal/native-readout comparison plus address-preserving correct/wrong value substitution and target-answer reversal. Distinguishes extractable state information, reader mismatch and actual final content dependence.
6. **Linear versus nonlinear versus partitioned:** equal total retained bits and exposure, with separate active-read budget. Distinguishes function class, optimization, allocation and mere storage expansion.

Any budget thresholds, seed counts or stopping gates would be proposals requiring later authorization. No training, code execution of papers, production changes or internal evidence-registry updates occurred in this discovery pass.

## 7. What is and is not ready for the coordinating report

Ready: bounded synthesis of update-specific interference, query-timing distinctions, active-versus-total state accounting, trainability counterexamples, and a real new precision/rank evidence branch. The original audit's finite-precision gap is narrowed, not closed.

Not ready: choosing a single architecture; a proof of arbitrary no-revisit long memory; claims of OOD semantic accessibility or content-specific deployed dependence; authoritative ICLR 2027 status for blocked leads; a complete critical review of nonlinear-memory theorems. The [12-work full-read queue](READING_HANDOFF.md) names exact missing questions and avoids recounting existing cards.
