# A04 — Deployed content use and causal measurement: coverage and findings

2026-11-09 · Specialist discovery only. Governing scope: [PLAN](../../PLAN.md) and the canonical [follow-up questions](../../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md), especially its deployed-use section. The multigranularity proposal and the byte-interface survey supply reusable evidence; neither governs the six broad axes. This is **not the final report synthesis** and does not register an experimental decision.

## 1. Work actually completed

1. Read the prior A04 audit, search log and recommendations; inspected the matching catalog identities and final addendum index, and searched the byte-interface inventory for overlapping causal protocols.
2. Read **12 actual old cards: 11 scoped FULL cards and one PARTIAL**. Reuse preserves their original versions and scope; reading a card is not another original-paper FULL read. Two of these are independent byte-interface cards, preserving BIW/W aliases.
3. Executed fourteen public WebSearch queries and retrieved official arXiv, ACL, PMLR and OpenReview sources. Selected primary body sections were read for intervention taxonomy, multiple mediators, statistical stability, natural-context tasks and conditional resampling. Newly completed original FULL reads: **zero**.
4. Registered 24 externally verified/recovered candidate records in [WORKS_AND_PROBLEMS](WORKS_AND_PROBLEMS.md): eight prior audit discoveries, four existing-but-unread works, twelve new-to-the-inspected-catalogs candidates. These classes must not be added together as 24 newly discovered works. Two blocked ICLR 2027 leads are separate and excluded.
5. Produced a fifteen-work reading queue with exact missing questions. No downloads, training, model calls, installations, production edits, old-document edits, commits or paid access.

The previous A04 audit already established many sound distinctions. The contribution here is recovery plus genuinely broader protocols and counterexamples, not rewriting that audit's warnings as new discoveries.

## 2. Evidence coordinates: reading is not using

The following are distinct properties, not a ladder whose levels automatically imply each other:

| Property | Positive evidence required | What does not establish it |
|---|---|---|
| Content recoverable by an external probe | Held-out target recovery with supervised-reader permissions and capacity/data controls | Reconstruction quality, random-label memorization, a strong oracle allowed future context |
| Native readout returns the target | Actual deployed query and interface return the correct value/relation before answer generation | A source ID hit, attention weight, a forced address, a separately trained lens |
| Prediction depends on target content | Fixed-weight, independently checked content A↔B interventions yield predicted answer changes, with non-target integrity and controls | Zeroing damage alone; output-class confidence changes; arbitrary steering |
| Dependency is task-correct | Correct evidence/answer verified under the declared authority policy; wrong/irrelevant evidence and unanswerability tested separately | Any answer flip, any increase in donor F1, agreement with an unverified source |
| Memory is useful relative to alternatives | Absolute task quality and a suitably budgeted reference system, including training/serving permissions | A within-model intervention effect or a separately trained reference interpreted as the same quantity |

W0369/W0530 support the first distinction; W0372/W0374/W0532 qualify interventions; W0050 separates channel dependence, trained-system utility and content benefit. Their actual versioned cards are linked in the works file. These axes also apply to non-retrieval recurrent state without any source identifier.

## 3. What the new evidence changes, beyond generic caveats

### 3.1 Specify what the intervention can remove, not just what vector it changes

**N01, Transformer Circuit Faithfulness Metrics are not Robust**, §§3–5, provides a decisive counterexample. Positional information constant across a donor distribution survives resampling but is destroyed by zeroing. The “correct circuit” differs accordingly. Thus a null donor intervention may mean the target property never varied in the donors, not that the model ignored that property. Conversely, a large zeroing effect may concern position, output-class priors or generic signal scale rather than the target fact.

Its six-part intervention specification is operationally valuable: graph granularity, node/edge/branch, value, token positions, direction, and circuit/complement. Add the output metric and clean/donor distributions. **Decision change:** an intervention record must say what information is changed and preserved and must include a positive control demonstrating sensitivity to the proposed target.

A further §3 distinction matters: restoring circuit edges can let clean information reach other edges, while corrupting the complement can enforce different restrictions. The two cannot automatically be called the same sufficiency test.

### 3.2 Smaller, more natural counterfactuals are helpful but not unconditionally better

W0533/R09 §6 recommends symmetric token replacements over Gaussian noise where suitable. W0373/R11 supplies a naturalistic input-level route. These reduce one source of intervention mismatch, but a hybrid state assembled from two natural runs may still be unnatural jointly.

R08, **The Curse of Multiple Mediators**, §§3,5.2–5.3, adds the opposite failure: very close symmetric replacements can eliminate the condition needed to expose duplicate-token and context-specific mechanisms. Its examples show that simply removing interaction terms also drops genuinely conditional computation. **Decision change:** choose counterfactual families by the claim being tested, not by a universal minimum-distance rule. Include both semantically matched value changes and carefully designed relation/identity changes; report their different targets instead of averaging them into one score.

The paper's algebraic finite differences can be recorded directly; interpreting every “pure” effect as isolated path-specific memory causation requires additional graph assumptions and independent scrutiny. We do not certify its proofs or adopt its universal rhetoric.

### 3.3 Pairwise interaction is a minimum screen, not a completeness certificate

R08 §5.2 reports backup effects weak in individual-pair tests but larger against an entire functional group. R02/Hydra distinguishes downstream adaptive response from pre-existing static duplicated information. N09/IOI is the original grouped-backup protocol to read next.

**Decision change:** after a small pairwise screen, test at least one semantically justified whole-route group and inspect downstream responses. A zero single-path effect cannot rule out natural contribution. A positive group effect does not uniquely distinguish static redundancy from dynamic compensation without continuation measurements.

### 3.4 Structural changes need functional checks

N02, **Many Circuits, One Mechanism**, varies token-frequency conditions while holding the task fixed. Its locked v2 abstract reports broad cross-condition edge transfer and an effective shared core despite distinct edge sets. It explicitly does not resolve specialization within token positions or internal features. N03 separately quantifies sampling, approximation and selection instability.

**Decision change:** neither changing circuit overlap during training nor low overlap across hosts establishes that the deployed mechanism changed. Pair structural differences with task-conditioned transfer/interchange tests, repeated extractions and a positive sensitivity control. Conversely, similar output behavior alone does not prove identical computation. This is relevant to axes E/F without making source retrieval the default repair.

### 3.5 Statistical uncertainty is not just another error bar

N12, **Certified Interventional Fidelity**, is an official UAI 2026 protocol candidate. Its primary abstract explicitly models the input/intervention distribution and provides anytime-valid confidence sequences, including adaptive intervention sampling under weighting assumptions. N11 supplies criterion-specific circuit hypothesis tests; N03 supplies sampling and estimator-instability analysis.

**Decision change:** if an evaluation is repeatedly inspected or interventions are adaptively chosen, a conventional fixed-sample interval is not automatically valid. Either fix the sample/interventions and hold out evaluation, or full-read N12 before adopting a sequential rule. Its bounded-score requirements do not automatically cover raw unbounded logit differences, negative log likelihood, or unstable recovery ratios.

N03's empirical instability is not proof of theoretical non-identifiability; N10's exhaustive toy enumeration provides a separate kind of evidence. Both still allow useful falsifiable explanations without uniqueness.

### 3.6 Context faithfulness and correct evidence use can require opposite answer behavior

N07/FaithEval's §3 instructs models to answer from context, say “unknown” for unsupported questions and “conflict” for inconsistent contexts. Its counterfactual task deliberately makes the context support world-false answers. N08/ClashEval instead asks whether a model arbitrates between correct prior/incorrect context and incorrect prior/correct context. A model that always ignores evidence trivially avoids one failure while failing the other.

**Decision change:** declare whether a source is authoritative by task construction or fallible evidence requiring arbitration. Do not use unconditional answer-flip rate as “correct content consumption.” Include separate axes for stipulated-world compliance, world-truth correctness, abstention/conflict detection, and source-specific causal effects.

N07 is also a concrete warning about evaluation gold: counterfactual contexts use string matching after a human pilot, not the same full human-validation process as inconsistent contexts; answer-mention accuracy is weaker than whole-answer entailment.

### 3.7 A convincing explanation or a high intervention score can be engineered

R05/Goodhart constructs inflated ERASER/EVAL-X scores without improving original-input explanations. W0530 shows learned interventions can act on arbitrary targets or random-initialized systems; W0534/W0535 contest what constitutes a legitimate distributed abstraction. N04's causal-attribution-profile agreement is a useful new triangulation candidate, not an independent answer-correctness gold standard, because both profiles depend on patch assumptions.

**Decision change:** test whether the evaluation is identifying the desired original mechanism or only recognizing its own intervention distribution. Keep untouched-input equivalence, arbitrary-target and randomized-model controls, held-out templates/entities, and explicit evaluation-label permissions. These controls are not all mandatory in every experiment: choose those addressing the mechanism and intervention family actually used.

## 4. Subdirection closure map

Labels: **S** = adequate existing substantive evidence to synthesize the stated limited claim; **U** = existing but unread or partially read original; **N** = new/recovered primary evidence to add/read; **E** = genuinely new empirical work needed. Multiple labels are intentional: literature adequacy is not architecture-selection adequacy.

| Canonical A04 subdirection | Classification and usable evidence | Exact next missing question / discriminating endpoint |
|---|---|---|
| Probe recoverability versus native readout | S: W0369/W0530; U: W0370/R12 | Can a bounded reader recover content unavailable to the unchanged native query, without future/label leakage? E: same-state reader comparison. |
| Native readout versus predictive dependence | S: W0372/W0374/W0050 | When the returned value is held correctly observable, does selective A↔B replacement alter the final answer? E, not more generic probes. |
| Source hit versus actual evidence use | S: W0384 restrictions; N: N07/N08 | Does the answer track the content, not source identity, rank, or merely token overlap? E: preserve identity and perturb content. |
| Correct-content versus generic-context dependence | S: W0050; N: N07/N08 | Does equally formatted irrelevant/donor evidence confer the same benefit; what authority policy determines correctness? E. |
| Copying versus semantic use | S: prior W0061/W0192 audit evidence, not re-read as cards here; N: N05/N02 | Can the same stored relation support paraphrase, role swap and multi-fact queries, not merely exact-string continuation? E. |
| Self/local/remote contribution | N: R08/N01; S: W0050 distinctions | Which paths are fixed versus allowed to recompute after intervention? E: conditional local×remote tests with observed native readout. |
| Activation-patch OOD | S: W0374/W0534/W0535; U: W0533; N: N01 | Which non-target changes and target assay failures occur across natural-input and internal-hybrid interventions? E; no universal density threshold. |
| Zero/shuffle abnormality | S: W0372/W0050; N: N01 | Does the control match scale/position/format yet actually vary the target property? E; rank matching alone is insufficient. |
| Natural content versus latent replacement | U: W0373; N: N06/N07/N08 | Do end-to-end counterfactual inputs and local state swaps agree on a defined target while differing in recomputation scope? E. |
| Content replacement versus addressing damage | U: W0533; S: W0534 restrictions | Can target value vary under fixed key/address and separately key/binding vary under fixed payload, without an invalid pairing? E; classify mixed-state failures as ambiguous. |
| Mediation and path interaction | N: R01/R08/N11 | Which background and outcome scale define the effect; are graph assumptions adequate for a path-specific interpretation? Read before making mediation claims. |
| Redundant routes and failed single ablation | S: W0384 limited clusters; N: R02/R08/N09 | Does joint removal reveal backup routes? E: pairwise plus justified group tests, not complete exponential search. |
| Self-repair/compensation | N: R02; U: original N09 controls | Does downstream target-related computation rise after damage at fixed weights, versus merely surviving duplicated content? E. |
| Necessity plus sufficiency | N: N01/N11/N06 | Do destruction and restoration preserve the same pathways/background? Read original nulls and graph contract; E host calibration. |
| Intervention granularity | U: W0533; N: N01/N02 | Does edge-level testing implement the declared interface/route claim, or accidentally retain all outgoing edges? E instrument equivalence. |
| Metric gaming | S: W0530/W0534-W0535; N: R04/R05 | Can an intervention-aware wrapper or label-encoded rationale improve the score without improved original behavior? U/N full reads; E assay test. |
| Intervention score versus real performance | S: W0050; N: N01/N07/N08 | Do raw effects, absolute task accuracy, full-answer correctness, and trained-reference utility agree or diverge? E. |
| Deletion/contradiction/answer-flip consistency | N: N07/N08; U: W0373 | Under a declared authority rule, when should the response flip, abstain, or remain unchanged? E paired semantic gold. |
| Negative content/unrelated sources | S: W0050/W0374; N: N05/N01 | Are negative controls non-answer-containing and matched in the nuisance dimensions that matter, and is the assay sensitive to a known positive? E. |
| Continuous tracking during training | N: N02/N03/N12, not a direct longitudinal result | Can fixed held-out item families and evaluation rules distinguish use changes from extraction noise and repeated-testing artifacts? E; no training launched. |

The earlier axis audit is adequate for the S-only conceptual distinctions. The missing operational protocols are not “the field is insufficient”; they are specific U/N dependencies. Actual failure localization and repair choice remain E.

## 5. Proposed minimal falsification families — not experiments run

These are design candidates for later authorization. They add no new architecture and no assumption of access to original text at deployment.

### F1. Content use without identity or lexical matching

Construct paired closed-world records with fresh names/values and a known relation. Change only the queried fact in a logically consistent alternative world; preserve an unrelated fact as a negative endpoint. Use exact-string, paraphrase and role-reversed questions on the same stored state. Keep paired original-input answers as semantic gold; record visibility timing so the encoder never receives future queries or labels unless the experiment explicitly grants them.

**Falsifies:** source-ID confidence, lookup-by-surface-overlap, or generic channel boosts masquerading as target-content use. Include an unchanged-content paraphrase and an irrelevant same-format fact change. Match raw-byte length when feasible; otherwise explicitly model length/position changes rather than implying exact control.

### F2. Natural total effect versus internal-interface effect

Compute paired natural runs A/B, then test original-state replay, A→B swap, B→A swap, irrelevant donor and same-state replay at each reachable interface. Separate payload, key/address, returned readout and downstream integration. Report both end-to-end recomputation and local interface replacement. Do not hold an address fixed if the intervention invalidates its content binding without marking the mixed state.

**Falsifies:** an apparent content-specific patch effect caused only by address disruption or output-class bias. Nulls require positive assay sensitivity. Natural-state marginals do not make the cross-world joint mixture natural.

### F3. Local/remote redundancy and compensation

For two well-defined available routes, evaluate `Y00`, `Y10`, `Y01`, `Y11` under the same background and score, where 1 denotes retaining a specified route's target information. Compute `Y11 - Y10 - Y01 + Y00` as a background-specific interaction contrast, **not a uniquely attributable information share**. Choose one whole-route group based on independent functional evidence, and monitor downstream target reconstruction/readout after ablation.

**Falsifies:** “no single-path damage means unused memory.” Static OR-like duplicates, AND-like cooperation and induced compensation can share some outcome cells; use downstream responses/controlled continuation to distinguish them. Pairwise tests alone do not exclude higher-order backup.

### F4. Correctness and authority policy

Run two separate contracts: (a) authoritative synthetic-world evidence, including logically consistent counterfactuals; (b) fallible external evidence with independently verified truth. Include correct evidence/wrong prior, wrong evidence/correct prior, no answer, conflict and irrelevant evidence. The desired endpoint is stipulated-world adherence in (a), appropriate arbitration in (b).

**Falsifies:** blanket evidence disregard, blanket copying, and “every flip is good” metrics. Do not penalize adherence to a world-false stipulation as the same failure as blind belief in a false external source.

### F5. Instrument validity and uncertainty

Require same-state replay near identity; known positive path and invariant negative property; raw per-example effects; answer-pair scores and final-answer accuracy; and matched intervention distributions. Use distinct discovery and evaluation items. If selection is adaptive, full-read N12 and choose bounded scores/sampling assumptions or lock the evaluation in advance. Report clustered uncertainty at the independent document/entity level; no arbitrary numeric gate is proposed here.

**Falsifies:** hooks that damage the baseline, a donor distribution unable to vary the target, metric-only confidence hacks, and sampling-dependent claims. A confidence sequence certifies its declared estimand, not semantic isolation or architecture optimality.

## 6. Independent alternatives without source revisit

These are competing hypotheses, not recommendations already selected:

| Alternative | Fixed constraint | Discriminating predicted result |
|---|---|---|
| Improve native query/readout training on a fixed flat state | Same stored information, no original-text access | Probe success converts to selective deployed use; no need for a retrieval tree. |
| Change write supervision toward future task information | Same state bits and deployment reader capacity | Content-specific dependence and absolute task quality improve together, not just zeroing sensitivity. |
| Repair key/value or entity/relation binding | Same number of slots/heads and same content budget | Value and relation counterfactuals succeed without extra source permission. |
| Rebalance local path and remote-state integration | Same evidence and overall optimization budget | Native readout remains correct while final integration becomes content-sensitive; removing the local path is not assumed universally beneficial. |
| State precision/partition/erase policy reform | Closed storage contract, no source copy retained | Reduced interference raises target-correct returns at matched delays/loads, while readout/consumer tests stay fixed. |
| Extra iterative computation over unchanged state | Same stored bytes; added compute explicitly charged | Better reasoning/use without improved stored information; not misattributed to more access. |
| Adaptation at the existing interface | Frozen versus bounded-adaptation comparison | Distinguish interface incompatibility from missing content; repair success does not prove old localization. |
| Build a calibrated evaluation instrument | Known tiny information paths, redundant and cooperative positives, false-evidence controls | Validity improves even if no production component is changed; an independent research contribution. |

## 7. Limits and handoff

- Recent emphasis includes 2026 multiple-mediators, stability revision, input-variation/granularity, official UAI statistical protocol, and the existing October compressed-memory paper. Discovery is not exhaustive across venues, languages, multimodal settings or all causal-inference literature.
- The official OpenReview ICLR 2027 group was verified through its public group response. Two highly relevant forum leads returned verification challenges through forum/API; one browser attempt also showed the challenge. Their title/status/version are **not verified as official forum evidence**, no acceptance is inferred, and no author deanonymization was attempted.
- No original new FULL reads, proofs independently certified, code executed, model experiments or final synthesis. W0050 remains PARTIAL; unavailable supporting material is inherited from its actual card, not newly searched to closure here.
- Scope owner may synthesize the qualified S claims now. Read the prioritized U/N protocols before implementing or claiming a reliable diagnostic. Architecture choice still requires the E experiments, under a separately authorized budget and matched host/seed/hardware/task conditions.
