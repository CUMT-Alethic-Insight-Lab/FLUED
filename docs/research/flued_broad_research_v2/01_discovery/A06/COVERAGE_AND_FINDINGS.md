# A06 — Component composition and cross-host transfer

Discovery revision: 2026-11-09. Governing scope: [PLAN](../../PLAN.md) and the original [follow-up questions, component composition section](../../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md). This is a specialist discovery result, **not the final broad-report synthesis, a preregistration, or authorization to train**.

Companion files: [works and problems](WORKS_AND_PROBLEMS.md), [search/source ledger](SEARCH_LOG.md), [precise reading handoff](READING_HANDOFF.md).

## 1. What was actually executed

- Read the previous `06_COMPOSITION_TRANSFER` audit, recommendations and search log, rather than resetting its discoveries to zero.
- Read six actual existing full cards: W0337, W0204, W0210, W0214, BIW-0122 and BIW-0126. Their IDs, versions, original scope and limitations are preserved below and in the work inventory. These are **six reused cards, not six newly full-read papers**.
- Revisited original public sources for all twelve previously recovered N06-01–12 works, sometimes advancing version-specific targeted reading, and verified ten additional relevant works against original public pages. Thus the focused external inventory has **22 entities = 12 recovered + 10 additional**, not 22 newly discovered papers and not 22 full readings. New classifications are relative to the two supplied catalogs; central catalog ownership/deduplication remains elsewhere.
- Verified accepted ICLR 2025/2026 proceedings sources for LoLCATs, GPTailor and KLAS. Separately obtained the official ICLR 2027 OpenReview group configuration. Four relevant 2027 search leads remain **forum/version/status verification blocked**; they are not counted among the 22 verified works.
- No new complete original-paper reading, experiments, code/checkpoint verification, downloads, installations, production edits, evidence-registry changes or commits. Large fetched HTMLs were read selectively; retrieval of a complete document is not full reading.

### Terminology used here

These are descriptive translations, not newly proposed project architecture names. **Model stitching / 模型表示拼接** means connecting a frozen source prefix to a frozen recipient suffix through a restricted learned interface. **Self-stitch / 同宿主自接** inserts the same interface into one model and is not synonymous with exact identity replay. **LoRA / 低秩适配** restricts trainable weight changes to products of low-rank matrices. **Factorial comparison / 因子交叉对照** varies multiple factors jointly to estimate dependence between their effects. **Effective capacity / 有效容量** means usable task/history information at a stated reader, precision and training budget, not simply parameter count. **Restorative intervention / 恢复性干预** tests whether a perturbation to an already demonstrated ability can be repaired. **Manufacturing intervention / 形成期干预** changes conditions while the ability is being learned. **Out-of-distribution interface / 分布外接口** produces recipient inputs unlike those encountered naturally. **Invariance / 表示不变性** identifies input changes a representation discards. English acronyms in paper titles remain source terminology.

## 2. Findings that change an experimental protocol

### 2.1 A self-connection is a substantive control, not an optional nicety

[Yosinski, N06-01, v1 §2/§4.1](https://arxiv.org/html/1411.1792v1) explicitly distinguishes BnB (same-task copied lower layers frozen, upper layers **reinitialized and retrained**) from AnB (lower layers from the other task), with BnB+/AnB+ allowing all layers to learn. Middle-layer BnB failure demonstrates a co-adaptation/relearning cost that exists without cross-task transfer. **Important correction to a loose reading of the prior audit:** BnB is not reconnecting both original intact halves; its upper layers are randomized. It cannot replace a same-checkpoint exact replay or intact self-stitch.

[Mai, N06-04, v3 §4.1](https://arxiv.org/html/2603.12433v3) supplies the more directly applicable modern control: identical learned stitch module, stitch position, objective and downstream data in source→source and recipient→recipient models. The paper compares those to cross-model composition. This advances beyond an unqualified warning that transfer is hard.

**Operational consequence (our inference):** use three distinct baselines: untouched/exact replay; intact self-stitch with the candidate interface; same-task relearning after a reset, if a reset is part of the transplant. A failure in any one baseline has a different interpretation.

### 2.2 There is positive evidence for repairing a failed frozen composition

[Mai v3 §3.2–4](https://arxiv.org/html/2603.12433v3) finds that local feature matching and direct task-loss training can fail, especially for shallow stitches. Matching the recipient's final/penultimate features before task fine-tuning works substantially better while keeping both original networks frozen. The paper uses self-stitch controls to test whether improvement is only extra interface capacity. Its §5.2 also reports a weaker CLIP source failing to match a stronger recipient: repair is not universally successful.

[LoLCATs, N06-07, v3 §3.1–3.2/Table 2](https://arxiv.org/html/2410.10254v3) compares attention transfer and low-rank adjusting. For Llama-3-8B/T2R, validation perplexities are 1539.39 without either, 79.33 after transfer alone, 16.05 after LoRA alone, and 4.11 after both. Crucially, single-stage training uses four epochs and the combined recipe two plus two, approximately equal total training steps. **This is a practical staged-intervention design, not a perfectly resource-balanced 2×2 causal experiment:** the untrained cell has no training exposure, and the LoRA dose differs across trained cells. It supports a budgeted strategy comparison and motivates a separately specified factorial design; one should not calculate a mechanism interaction coefficient from these four numbers as though every cell had the same dose.

**Operational consequence:** one failed local-MSE adapter does not establish intrinsic content loss. Compare local matching, downstream feature matching and task supervision under separately stated teacher, data and update budgets; evaluate the naturally composed chain, not only teacher-fed block inputs.

### 2.3 A core mechanism's apparent advantage depends on its companion components

[The Key to Going Linear, N06-12, v1 §3–4/App. C](https://arxiv.org/html/2607.07706v1) first freezes all original parameters, leaves Q/K/V unchanged, and trains only replacement parameters for 10M tokens. It then adds fixed-budget local/prefix cache allocation and projection adaptations. The authors report that GLA–GDN differences nearly disappear after short convolutions. They explicitly reduce the LoRA learning rate for stability and perform no hyperparameter sweep. This is directly relevant evidence for **core update × companion projection × adaptation budget**, not a universal ranking of update rules.

[MOHAWK, N06-08, v2 §4](https://arxiv.org/html/2408.10189v2) provides a complementary counterexample: its transplant initialization sets convolution to identity, opens a gate to one, and removes pre-output normalization/post-convolution activation that are useful in a from-scratch Mamba-2 block. The transplant package is deliberately different from the native training package. Its same-architecture Phi→Phi distillation control is another useful recovery-validity check.

**Operational consequence:** specify the minimal complete block: update, projections, normalization, output gate, short convolution, position handling and local path. Cross core A/B with companion package on/off rather than transferring an undocumented bundle and naming only its central recurrence.

### 2.4 Stage deletion must return its opportunity budget

[RAM migration, N06-10, v1 §5.3/Table 4 and Appendix Table 12 discussion](https://arxiv.org/html/2610.11214v1) compares head→block→whole-model restoration with whole-model-only restoration under 500M tokens. When a stage is removed, its tokens are reassigned to whole-model recovery. The text reports that intermediate stages improve downstream performance even where Wiki perplexity is similar. Current HTML extraction misses table cells, so this stream independently verifies the **budget rule and directional author result**, not the old audit's numerical cells.

This work is **not** W0214 (RAM-Net 2602.11958v2). Architecture-family connection does not make them two versions of the same work.

**Operational consequence:** compare training schedules with a budget ledger. A deletion that simply removes its training cannot tell whether the stage or additional training mattered. Matched token count still does not match teacher FLOPs, wall time or optimizer state.

### 2.5 Successful stitching can be useful without measuring semantic sameness

[Bansal, N06-02](https://arxiv.org/html/2106.07682v1) gives a positive forward-compatibility test. [Balogh, N06-03](https://arxiv.org/html/2412.11299v1) shows task-loss stitching can rank another layer as more similar than a layer to itself and attributes this to unusual recipient representations. [Smith, A06-X04, ICML 2025](https://proceedings.mlr.press/v267/smith25a.html) reports successful stitching even from representations based on different cues/modalities and clustered noise. These are reasons to reject **successful task fit ⇒ original representations contain/use the same information**, not reasons to reject practical learned interfaces.

[Invariance-aware stitching, A06-X05, v2 §2–3](https://arxiv.org/html/2505.20142v2) adds a constructive response: compare alignments on inputs optimized to be nearly indistinguishable at the source representation while examining downstream compatibility. It holds stitch initialization fixed across standard and invariance-aware comparisons. Its backward notion concerns input preimages, not backpropagation. The ICLR 2026 forum with a related but different title/author list could not be inspected; **no automatic identity or accepted-venue merge is made**.

**Operational consequence:** report at least two outcomes: “a budgeted connector achieves the task” and “the intended content survives and causally matters.” Cross correct vs plausible wrong content with matched addresses/positions; hold out new bindings and query distributions; use constant/random sources to detect a connector learning the answer route itself. The precise language-model intervention remains a new experiment, not a transferred visual result.

### 2.6 Recent ICLR evidence is actionable, but search optimization is not a factorial effect estimate

- **LoLCATs: accepted ICLR 2025**, [official proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/72163d1c3c1726f1c29157d06e9e93c1-Abstract-Conference.html). Supports staged output alignment plus limited adaptation with a useful equal-step comparison.
- **GPTailor: accepted ICLR 2026**, [official proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5c99f2254833533c2a8ca0e0be04d77e-Abstract-Conference.html), [v1 §4.4](https://arxiv.org/html/2506.20480v1). Its search-space ablations compare removal alone, selection+removal and the full selection/merging/removal space. The reported selection+removal outcome can be worse than removal alone, whereas full merging helps. These are **outcomes of separately optimized search spaces**: expanding a feasible set cannot worsen its exact optimum, so the observed degradation also admits finite search/optimization effects. Do not call it proof that selection is intrinsically harmful.
- **KLAS: accepted ICLR 2026**, [official proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/e9f0ce998bede73f8068985f3deeab9a-Abstract-Conference.html), [arXiv v1](https://arxiv.org/abs/2605.29259v1). KL-based stitch selection produces accuracy–efficiency options at the stated same fine-tuning cost. This is verified metadata/abstract evidence only; exact search accounting and protocols need full reading.

The official [ICLR 2027 group API](https://api2.openreview.net/groups?id=ICLR.cc/2027/Conference) confirms `ICLR.cc/2027/Conference/-/Submission`, public submissions, and distinct active/withdrawn/desk-rejected venue IDs. This **does not verify an individual paper's membership or status**. The four 2027 leads in the ledger remain pending because official forums/notes returned verification pages or 403. No anonymous identities were researched or joined to arXiv.

## 3. Mapping the actual subdirections to the right next action

Categories are multidimensional and may coexist: **S** = enough existing synthesis/card material for a bounded statement; **U** = existing but unread primary details; **N** = new/recovered original search evidence needs selected reading; **E** = genuinely new controlled experiment needed for the project. None means architecture selection is settled.

| Original subdirection | Coverage now | Concrete missing piece / discriminating action |
|---|---|---|
| Frozen-host component transplant | N: N06-02/04/07/12; S: BIW-0122/0126 | Fix trainable set; intact self-stitch vs cross-stitch; no original-text access through connector. |
| Adaptive-host component transplant | N: N06-01/08/10; S: BIW-0126 explicitly separates frozen and full-model continuation | Connector-only, local projection and full-host curves need separate causal claims and costs. |
| Same-host self-connection | N: Mai §4.1; N: Yosinski provides a different reset/relearning control | Exact replay, intact self-stitch, reset/relearn must not be collapsed. |
| Cross-model representation compatibility | N: Bansal, Mai, KLAS; counterexamples Balogh/Smith | Compare practical fit, original feature match and content-specific generalization. |
| Interface mismatch vs intrinsic harm | N: Mai + MOHAWK + Key to Going Linear; E | Recovery by restricted alignment supports mismatch; failure after a finite search only rejects the tested repair class/budget. |
| Component × adaptation budget | N: LoLCATs and RAM migration | Fully specified equal-dose cells or budgeted schedule estimand; fit curves, not one final score. |
| Component × host structure | N: MOHAWK, Key; S: byte-interface cards | Same input text/task/source permissions per host; conduct within-host factorials before cross-host contrasts. |
| Non-additive single vs combined effects | N: GPTailor/TIES; S: W0337/W0214; E | Original, A, B, AB on the same metric; optimize/search each arm transparently, do not infer fixed-piece effects from search winners. |
| Missing companion component | U: W0201/W0228; N: MOHAWK/Key | Read real block ablations, then an authorized static interface check; this stream has not inspected local implementation. |
| Parameter count vs effective capacity | S: W0204/0214; N: Collins, Net2Net | Match total state bits separately from active access; account for rank/precision/readout/functional initialization. |
| Parameter increment vs optimization difficulty | N: Melis, Collins, Net2Net; S: BIW-0126 | Equal trainable parameters does not equal equal conditioning; report both fixed-contract and equal-development-budget comparisons. |
| Connector transform vs semantic transform | N: Balogh/Smith/invariance-aware stitching; S: BIW-0122 | Correct/wrong content crossed with fixed addressing; test cue changes/new bindings, not only task labels. |
| Manufacturing failure vs repair failure | S: W0337; N: MOHAWK/LoLCATs; E | Show original checkpoint had ability, break it, restore it; independently intervene during formation. |
| Break an already positive host | S: W0337; N: Hydra/Rushing; E | Bidirectional natural-content or component perturbations plus non-target controls; do not select only initial failure examples. |
| Restorative intervention in original host | N: Mai/N06-10; E | Reinsert original component/exact replay; compare restricted repair on same damaged examples. |
| Acute disturbance vs long adaptation | N: Yosinski/Melis/LoLCATs; S: BIW-0126 | Record t=0 and learning curve/forgetting, matched continuation baseline, separate total history. |
| Input-domain changes during architecture transfer | S: BIW-0122/0126; N: Yosinski/progressive networks | Match raw text coverage and targets; conversion changes segmentation/positions/context and may alter tasks. |
| Task/budget changes during transfer | N: Melis/Collins/KLAS; S: W0204/0214 | Quality, targeted content use, total resident state and per-step cost separate; do not equate perplexity with recall. |
| Conditions for transportable causal conclusions | N + E | State the tested source/recipient family, stage, intervention class, reader, seed/data and budget; test host×component interaction rather than claim universality. |

## 4. Candidate protocol, now anchored in actual originals

This section is an **analyst design**, not an experiment run or a preregistered gate. No thresholds or seed counts are prescribed.

### 4.1 Identify the outcome before making the comparison

Distinguish four questions:

1. **Acute dependence:** does an already functioning model immediately lose performance when a component is changed?
2. **Budgeted restoration:** can a specified legal adaptation class recover that loss within an explicit budget?
3. **Formation:** can the ability emerge when the component is present from the stated training stage?
4. **Deployment selection:** which complete model/training recipe gives the best quality–resource frontier after equal development effort?

A success on (2) need not show original features were semantically identical. Failure on (2) does not establish impossibility on (3). Optimizing (4) does not isolate a single-component effect.

### 4.2 A small staged factorial design rather than one enormous matrix

**Stage 0, validity:** untouched host; exact tensor replay; original component reinserted; intact self-stitch with same interface/position. Where surgery resets part of a network, add the corresponding same-task reset/relearn baseline. Stop interpreting transplant quality if the relevant validity anchor fails.

**Stage 1, within-host interactions:** for each host separately, compare original, A-only, B-only and AB. A might change state payload/writing and B the addressing/return path, but an interface that cannot physically separate these must say so. Cross these with no adaptation and one predefined connector-only budget. Use the same trainable-parameter envelope and training opportunity for matched sham/original-component controls.

**Stage 2, local repair:** for informative failures compare local feature matching, downstream feature matching and task-loss adaptation; hold frozen halves fixed. Separately vary a companion package (normalization/gate/convolution/position mapping) if it is the named hypothesis. Return deleted-stage token/step budgets to an allowed baseline. Include teacher computation and tuning trials in costs.

**Stage 3, transport:** repeat the informative cells in the other host using the same raw-content coverage, task family, validity test and resource contract. A difference-in-differences is evidence of host interaction only at that specified scale, not a domain-free mechanism ranking.

For a quality-higher-is-better outcome Q, predeclare the scale and calculate `I_AB = Q_AB - Q_A - Q_B + Q_original`. Calculate a separate interaction for content-specific use. Accuracy, log loss and perplexity have different scales: interaction values are not invariant under conversion. Repeated paired data windows and independent donor/recipient seeds help distinguish donor/recipient variation from evaluation noise. Hardware/environment fingerprints remain part of a from-scratch result; this literature search supplies no cross-hardware equivalence certificate.

### 4.3 Separating interface repair from answer learning

- Restrict connector visibility: no discarded original text, future answer, extra labels or external source content unless all arms have that permission.
- Fit on training inputs only; evaluate held-out bindings/identifiers, unseen query distributions and non-target behaviors.
- Compare correct content, same-type/length plausible wrong content, constant content and a high-fidelity positive payload while keeping legal addresses/positions fixed. A shuffled key–value mapping is an address intervention, not a pure content control.
- Record local matching error, downstream error under natural composition, targeted answer dependence and broad quality. Teacher-fed local MSE is diagnostic, not deployment success.
- Report natural downstream compensation as part of total deployed effect. A separate fixed-path/normalization experiment can diagnose compensation, but must not replace the natural effect.

### 4.4 Capacity and cost ledger

Record total/frozen/trainable/active parameters; optimizer memory; total resident and active state elements × precision; connector rank and input/output dimensions; text bytes and sequence positions; teacher and student forward/backward work; adaptation tokens/steps; tuning trials; elapsed device time; prefill/decode costs; and original training history. No single scalar matches all of these.

Net2Net supplies an especially useful caution: more parameters can initially represent exactly the same function, while symmetry breaking and subsequent optimization change usable capacity. Collins supplies empirical memory/parameter-capacity tasks, **not a universal five-bits-per-parameter law for modern language models**. W0204 and W0214 already show why activity-matched state and total resident state are different contracts.

## 5. Independent alternatives that do not require source revisiting

| Route | Evidence anchor | Independent unresolved test |
|---|---|---|
| Fixed-granularity state plus restricted native-reader adaptation | LoLCATs; Mai; BIW-0122 | Does held-out content dependence recover without more state or text access? |
| Companion-aware update reform | Key to Going Linear; MOHAWK; existing unread GDN/DeltaNet | Does convolution/gating explain the transplant failure, or merely replace the intended content path? |
| Separate write/read allocation in a fixed state array | W0214 reused full card | Same total state bits and total read/write quota; test conflicts/missed co-location. No original-source address is assumed. |
| Independent route metadata and fixed compressed values | W0210 reused full card | Freeze one value bank and cross routing rules; existing independently continued-training comparisons do not do this. |
| Function-preserving surgery followed by adaptation | Net2Net; Git Re-Basin | Can an invertible/identity control distinguish coordinate mismatch from content destruction before compression is introduced? |
| Shared-origin weight-delta composition rather than state-interface transfer | Task Arithmetic; TIES; GPTailor | Same-base donors vs independently trained hosts; isolate coefficient/sign/search interference from actual incompatible capability. |
| Frozen feature reuse plus a bounded new branch | Progressive Neural Networks | Random frozen source branch and matched added capacity; source reuse vs learning entirely in the new branch. No retrieval required. |
| Training-stage alignment instead of final-checkpoint repair only | W0337; MOHAWK; BIW-0126 | Compare formation and restoration histories without confusing failure to repair with failure to learn. |

These routes compete with multigranularity/source retrieval; they are not subordinate implementation details of that proposal.

## 6. What remains open

The literature now supports a concrete validity/repair/interaction protocol, not an architecture verdict. Remaining work is selected primary full reading, unresolved ICLR 2027 forum verification, exact version comparison where noted, and project-specific controlled interventions after separate authorization. Current negative results cannot be interpreted without knowing the actual local component package and training permissions; this stream deliberately did not inspect or modify production code. Field coverage is selective, with no exhaustion claim and no fabricated acceptance/reading count.
