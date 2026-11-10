# Final broad scientific-rigor review — independent, bounded sample

**9 November 2026. Assigned output: this file only.**

## 1. Release judgment

**The broad synthesis is substantively ready at a bounded six-axis scope, but the current English files need two local scientific-handoff repairs and one citation/population repair before final release.** The repairs are specified in §3: **0 current P0 claim violations confirmed; 2 P1 findings; 1 P2 finding**. This is not approval of every sentence, all 128 reading declarations as scientific truth, all 780 registered clusters, or an architecture choice.

The report genuinely restores compression/task sufficiency, native writing/retention/capacity, addressing/readout, deployed content use, learning dynamics, and host composition. Its positive results and reversing controls are substantive. Byte interfaces and multigranularity/source access do not replace the original broad list. The main conclusion is appropriately plural: objective, writer, precision, legal reader, learning history, companions, and richer source permissions remain competing explanations and remedies.

**The selected recent-original reading objective remains incomplete.** Seventeen intended official manuscripts remain unavailable; three independently FULL public editions do not complete those official sources. A bounded report can be delivered without asserting their results or conference-wide coverage. Completing the stronger original-body requirement needs lawful source access: a genuinely changed ordinary public route, a separately identifiable legitimate edition, or source files/access supplied through an authorized user channel. This review neither requests bypass nor silently treats the narrower deliverable as completion of that requirement. No new access is needed for the three local corrections below.

## 2. Actual check scope and notation

Read the [PLAN](../PLAN.md), complete five final English files, canonical [167-direction list](../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md), current [COUNTS](../02_catalog/COUNTS.md), current 128-row [READING_STATUS](../02_catalog/READING_STATUS.md), [QUESTION_COVERAGE](../02_catalog/QUESTION_COVERAGE.md), relevant current catalog/version overrides, [RECENT_ORIGINAL_CLAIM_RULES](RECENT_ORIGINAL_CLAIM_RULES.md), both scientific reading audits [R1](READING_AUDIT_R1.md)/[R2](READING_AUDIT_R2.md), original scope audit, coverage R2/R3 decision passages, source R1/R2 count/version/access passages, and complete [source R3](ICLR2027_SOURCE_AUDIT_R3.md). Historical audit snapshots were not mistaken for current card states.

The purposive scientific sample is **41 distinct claim packets carried by 41 actual cards**, distributed as A6/B7/C6/D5/E6/F4 plus seven cross-axis/interface/utility packets. These are selected claims, not 41 independent whole-paper rereadings. **Selected original passages from 13 distinct works** were independently reopened locally; §5 records the actual text/PDF locations. Other sampled claims are card-to-synthesis checks, explicitly distinguished in §4. No random sampling, catalog-wide error rate, proof certification, new FULL credit, paper implementation execution, or replication is claimed.

For compact exact locations:

- **R** = [REPORT_EN.md](../04_synthesis/REPORT_EN.md).
- **S** = [EXECUTIVE_SUMMARY_EN.md](../04_synthesis/EXECUTIVE_SUMMARY_EN.md).
- **M** = [EXPERIMENT_DECISION_MATRIX_EN.md](../04_synthesis/EXPERIMENT_DECISION_MATRIX_EN.md).
- **O** = [OPEN_EVIDENCE_EN.md](../04_synthesis/OPEN_EVIDENCE_EN.md).
- **V** = [REVISION_LOG_EN.md](../04_synthesis/REVISION_LOG_EN.md).
- `L` denotes the physical line in these saved files/extractions, not publisher line numbering. PDF page references are stated separately. Locations refer to the reviewed snapshot, whose five hashes appear in §8.
- **Valid scope** means the inspected sentence carries the relevant contract; it is not an endorsement of the entire source. **Source error/conflict** concerns what is actually printed in the original. **Reader error** concerns a card or synthesis misstatement. **Handoff omission** means an established restriction was lost between review and final synthesis, without assuming that every remaining sentence is false.

## 3. Required local corrections — exact claim, evidence, minimum fix

### FBR-01 — P1: T02's split-count law needs the already-established skip/feasibility qualification

**Final locations:** R:L968–970, especially the unqualified technique label “Dirichlet–multinomial split allocation”; O:L60–74 has no T02 sampler implementation row. V:L33 summarizes T02 integration but does not record this distinction. The T02 support, realized-split and theorem limits elsewhere are useful and should stay.

**Actual evidence:** [T02 card](../03_reading/V17/BR-R2-T02.md):L11–13 already qualifies the Pólya correspondence. [Recent rules](RECENT_ORIGINAL_CLAIM_RULES.md):L34–41 supplies a concrete counterexample. Independently reopened public **2604.16037v1 PDF pp.6,18,21**: Algorithm 1 counts attempts and skips an unsplittable selected token; Appendix F says the process “corresponds exactly” to a Pólya urn and gives `DirMult(N,1)`; p.6 claims preservation of STOCHASTOK's split-count law.

For canonical `[a,bc]`, vocabulary containing `a,b,c,bc`, and one attempt, actual counts are `(0,0)` or `(0,1)`, each with probability 1/2. `DirMult(1,(1,1))` instead gives `(1,0)` or `(0,1)`, each with probability 1/2. Conditioning the latter on feasibility gives `(0,1)` surely, which still does not reproduce the skipped-attempt algorithm. This is a **source distributional overclaim plus a final handoff omission**, not a new claim that all empirical results or implementations are invalid. R does not explicitly assert identical realized laws; the missing qualification matters because the source's mathematical technique is being carried into design comparisons.

**Minimum author fix:** append one sentence to R:L970:

> Appendix F's exact Dirichlet–multinomial correspondence is idealized: Algorithm 1 skips unsplittable selections, so the realized split-count law and the UNI sampler's feasibility/cap handling require reconciliation.

Add one O §4 row naming “T02 Algorithm 1 versus Appendix F, public v1” and the missing skip/cap/feasible-count implementation contract. Add this item to V's existing T02 correction cell. No new summary paragraph, global theory disclaimer, card downgrade, or further source acquisition is necessary. Keep the tested robustness positives, clean negatives and support controls unchanged.

### FBR-02 — P1: carry the PSR initial-estimator dimension error into the reproduction handoff

**Final locations:** R:L293–297, O:L13 and §4 table L60–74, V:L35. The final report correctly states rank/exploration/conditioning assumptions and success conditioning, but omits the distinct printed estimator problem identified by the latest review.

**Actual evidence:** [PSR original extraction](../03_reading/V18/sources/BR-PSR-0912.2385v1.txt):L163–180 defines `P_H` as a `|H|` vector and `P_(T,H)` as a `|T| × |H|` matrix; L202 gives Eq.5a `b_1 = U^T P_(T,H) 1_k`; L229–235 selects `U` as `|T| × n` and prints step3(a) `b_hat_1 = U_hat^T P_hat_H`. Feature Eq.10a, L303, returns to the moment-matrix expression. The actual PDF p.4 was reopened in memory and confirms the printed step3(a), not merely an extraction artifact. [Recent rules](RECENT_ORIGINAL_CLAIM_RULES.md):L121–127 records the same issue.

`(n × |T|)(|H| × 1)` is undefined when `|T| != |H|`. Equal set sizes do not make the two formulas generally equivalent. This is a **source formula error/inconsistency, not a false experimental result and not a failure to read the whole paper**. The current [carrying card](../03_reading/V18/BR-PSR-0912.2385.md):L15–22 does not certify every equation. Its FULL scope remains intact. The final's omission is an artifact/reproduction handoff problem; the conceptual learned-identification result remains usable.

**Minimum author fix:** append to R:L293:

> The printed initial-state estimator in §3 step3(a), `U_hat^T P_hat_H`, is dimensionally inconsistent with Eq.5a's test/history-moment formula; reconcile that expression before literal reproduction.

Add one O §4 row identifying step3(a), Eq.5a and Eq.10a, with equation/code clarification as the upgrade condition; add the issue to V:L35. Do not present `U_hat^T P_hat_(T,H) 1` as a verified code repair: it is the algebraically compatible reference expression, not an inspected implementation. S:L37's bounded planning summary needs no expansion. Keep **78 successes / 22 loops**, the success-only **18.2** mean, privileged A*, and the feature/operator/planner ledger unchanged.

### FBR-03 — P2: fix T05's section locator and attach the population to its headline failure

**Final locations:** R:L123 cites “§5, Fig.3 pp.8–9” for whitespace collapse; R:L899 and S:L75 quote **49%→9%** without the teacher/divergence/sample denominator in the sentence. The numerical values and warning are supported; this is not a scientific reversal.

**Actual evidence:** [T05 original](../03_reading/V17/sources/BR-R2-T05__2607.22334v1.txt):L564–570 is **§4.3 Whitespace Collapse**; L600–618 specifies **GLM-Z1-9B/BPM-JSD** and the mask comparison; L1571–1575 states **128 generations/checkpoint**, and **80 programs / 1,799 positions** for the distinct margin probe. §5 at L620 is the conclusion. [Actual card](../03_reading/V17/BR-R2-T05.md):L19–23 already names the pair and divergence. This is a **reader/synthesis citation error plus a quantitative population clarification**.

**Minimum author fix:** change R:L123 `§5` to `§4.3`. In the main quantitative sentence at R:L899, use:

> In the GLM-Z1-9B/BPM-JSD comparison, unmasked code pass falls 49%→9% in the 128-generation-per-checkpoint diagnostic (Fig.3, §4.3; Appendix H.2).

At S:L75 insert only “in one GLM-Z1-9B/JSD comparison” before the same numbers. No need to repeat every probe denominator in the summary or add another generic causality warning. Preserve the random-mask control, conditional exactness, realized-path lower bound and teacher costs.

### P0 boundary — open completion condition, not a newly found false claim

R:L936–960, S:L21 and O:L15–39 correctly retain **17 unavailable official bodies**. A statement that all selected recent originals were scientifically read, that conference-result coverage is complete, or that unavailable alternatives lose would require a P0 stop. Those statements are **not** made in the inspected final files. The existing stronger original-reading requirement cannot be marked complete by this review. Preserve its open status rather than adding another caveat to every chapter.

## 4. Forty-one actual card-to-claim checks

Each row is one distinct work-level packet. Source locations here are those actually recorded in the card unless the last column names an independently reopened primary packet **P01–P13** in §5. Repeated consequences of one paper are not additional sampled works.

### A — Compression/task sufficiency: six packets

| # | Final line / load-bearing claim | Actual card, edition and carrying lines | Adjudication / minimum correction |
|---|---|---|---|
| 01 | R:L115,127–129: objective priority reverses with rate; nominal Gaussian rate, hard bits and empirical entropy differ | [W0067](../03_reading/V01/W0067.md):L5–13, **2610.30493v1**, §4/App.F.1 Table1 | **Valid scope.** 16.8182 nominal-bit and 21.2035 bits/image crossovers are not interchangeable. Five seeds share splits; pointwise bootstrap is not simultaneous or physical bit capacity. Card check only; no fix. |
| 02 | R:L116,125: SAC LM-only wins selected QA but mixed wins QMSum | [SAC](../03_reading/V01/BR-A01-R02.md):L3–13, **2510.08907v4**, Tables5/20 | **Valid scope.** Keeps opposite summarization cell and 500x mixed comparisons; frozen decoder/bidirectional encoder/layerwise growing KV are named. Not a universal reconstruction penalty. Card check only; no fix. |
| 03 | R:L97: preserving private information helps some transfers, hurts CIFAR100→DTD 36.06→34.79 | [R04](../03_reading/V01/BR-A01-R04.md):L3–11, **2203.07004v2** | **Valid version.** The numbers are public-v2 Table4, not certified CVPR-table equality. Formal PARTIAL/public FULL is retained. Card check only; no fix. |
| 04 | R:L119: two-step gradient truncation does not mean two-step memory retention | [AutoCompressors](../03_reading/V01/W0037.md):L7–13, **2305.14788v2**, §3.1 | **Valid scope.** All older summaries remain in forward context; consumer adapts; full attention wins selected cells. Not fixed-total-state evidence. Card check only; no fix. |
| 05 | R:L138,144: more KL can yield worse likelihood; wide decoder can lose latent benefit | [BIW-0095](../03_reading/V10/BIW-0095.md):L7–15, **1702.08139v2**, Table2 | **Valid scope.** Word-level stochastic VAE, unequal receptive-field/depth/dropout/pretraining; KL is not exact-content use. Card check only; no fix. |
| 06 | R:L248–250: success ≤ min(1, |S|/D^L), not a blanket language-memory impossibility | [W0061](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md):L7–11,19–27, **2402.01032v2**, §2/App.D | **Valid non-strict correction.** Uniform independent strings, deterministic one-pass post-input state, whole-string success; precision/all cross-time channels count. Card plus elementary counting check, not a fresh original-page check. No fix. |

### B — State writing/retention/capacity: seven packets

| # | Final line / claim | Actual card, edition and carrying lines | Adjudication / minimum correction |
|---|---|---|---|
| 07 | R:L173–187: residual writing and correlated-key collateral term | [W0199](../03_reading/V02/W0199.md):L7–13, **2102.11174v3**, §4.2/App.B | **Valid algebra and scope.** `(M+β(v−Mk)k^T)q−Mq=β(v−Mk)(k^Tq)`; unit keys concern exact target replacement, not this identity's validity. Orthogonal preservation is not general interference freedom. Card plus algebra; no fix. |
| 08 | R:L196: passkey 98.8/91.8 versus essay-number 18.6/92.2 reverses DeltaNet/GDN ranking | [W0201](../03_reading/V02/W0201.md):L7–11, **2412.06464v3**, Table2 | **Valid scope.** Separate tasks/lengths, scalar decay versus delta, convolution/norm/gating and hybrid paths remain visible. No isolated semantic-filter effect. Card check only; no fix. |
| 09 | R:L234: .561/.518 p=.86 conflicts with stale −.32; curriculum 6/6 versus0/6 is trained length | [Anatomy](../03_reading/V03/BR-A02-P03.md):L7–13, **2609.16183v1** | **Confirmed source conflict**, correctly reported; no new reader error. **P01**. No fix to those final sentences. |
| 10 | R:L283: Titans Eq.13/32 indexing, Eq.16 gradient-state and unlocated proof | [Titans](../03_reading/V03/W0234.md):L7–13, **2501.00663v1** | **Confirmed source formula/index conflict and algorithm ambiguity**, not observed code failure or theorem falsity. **P02**. Keep current bounded treatment. |
| 11 | R:L256: LeapQuant 1.19 bytes/element excludes ~8KiB active buffer | [LeapQuant](../03_reading/V03/BR-A02-N01.md):L5–13, **2609.38166v1**, §4.3 | **Valid complete-ledger distinction.** Boundary storage and per-active-request buffer are different. **P05**. No fix. |
| 12 | R:L257: controlled LinQuant carry FP32/read copy INT8; production prefill differs | [LinQuant](../03_reading/V09/BR-A08-V23.md):L7–11, **2610.39418v1**, §4/App.B/E/F | **Valid numerical scope.** Exact transforms precede rounding and have decay/initial-state constraints; prefill is not repeated low-bit decode. **P06**. No fix. |
| 13 | R:L293–297: learned PSR identification/planning,78 successes,18.2 success-only actions | [PSR learning](../03_reading/V18/BR-PSR-0912.2385.md):L15–28, **0912.2385v1** | **Valid empirical denominator and resource scope; missing source-formula handoff. P07/FBR-02.** Five coordinates do not price kernels, moments, SVD, reward fit and planner. |

### C — Addressing/native readout: six packets

| # | Final line / claim | Actual card, edition and carrying lines | Adjudication / minimum correction |
|---|---|---|---|
| 14 | R:L333–335: fixed address weights can shortcut mutable content; discrete recall fails | [D-NTM](../03_reading/V04/BR-A03-D02.md):L7–15, **1607.00036v2**, §§2–9/Table7 | **Valid scope.** Read-order index ambiguity is not future-information leakage. Address overlap is not association correctness; unequal controller doses retained. Card only; no fix. |
| 15 | R:L367–375: count-correct merge exact after keys are equalized, not before | [Homogeneous Keys](../03_reading/V04/BR-A03-D03.md):L7–15, **2506.05410v2**, Eqs.7–11 | **Valid operator identity.** Sum-value numerator/count denominator is correct; mean values need numerator multiplicity. Backward/gradient visibility and peak-memory negatives retained. Card plus algebra; no fix. |
| 16 | R:L416–418: QKNorm temperature removal24.53 versus33.24; main comparison bundled | [QKNorm](../03_reading/V04/BR-A03-D13.md):L7–17, **formal Findings EMNLP2020**, Tables2/6 | **Valid scope.** Direction, temperature, V norm and LayerNorm/warmup are separate. No universal head-count/default claim. Card only; no fix. |
| 17 | R:L432–436: LRKV independent Q/shared-base KV; 48/72≠52.6% | [LRKV](../03_reading/V04/BR-A03-D17.md):L7–19, **2601.11471v3**, Tables7/8/12 | **Source arithmetic/position ambiguity**, preserved rather than silently repaired. 48/72=66.7%; per-scale ranks partly explain different main-table claims, not every appendix ratio. Card plus arithmetic, no new original-page inspection; no fix. |
| 18 | R:L345–353,509: D20 target transfer61–89%, low non-target breaks; output patch does not isolate q | [How Linear Attention Remembers](../03_reading/V09/BR-A03-D20.md):L7–15, **2609.33093v1** | **Valid scope.** Held-out four-choice intervention, failed prose-competence gate and possible recurrent influence on earlier writes survive. No native semantic-query conclusion. Card only; no fix. |
| 19 | R:L337,446: MemN2N learns adaptive hops, retains explicit bank/restart selection/pathfinding failure | [MemN2N](../03_reading/V11/BR-A03-D11.md):L7–19, **1503.08895v5**, §2/Table1 | **Valid scope.** 25.8/15.6/13.3 errors are not an equal-compute reread factorial; pathfinding90.2% error remains. Constant initial LM q is compatible with later adaptive q. Card only; no fix. |

### D — Deployed use/causal measurement/statistics: five packets

| # | Final line / claim | Actual card, edition and carrying lines | Adjudication / minimum correction |
|---|---|---|---|
| 20 | R:L467: RAVEL high Iso90.2 with Cause8.8, verb MDAS49.5<DAS51.8 | [RAVEL](../03_reading/V05/W0531.md):L9–21, **2402.17700v2**, Table6 | **Valid scope.** Learned donor/label intervention, separate entity/context holdouts and unresolved site-selection wording are explicit. Not spontaneous native access. Card only; no fix. |
| 21 | R:L515–517: FaithEval context authority and answer mention differ from world truth | [FaithEval](../03_reading/V12/BR-A04-N07.md):L7–11, **2410.03727v3**, §3/App.A | **Valid scope.** Unknown list includes “not”; clean-context prompt regressions retained. No exclusive full-answer endorsement from mention score. Card only; no fix. |
| 22 | R:L517: ClashEval .608 conditional versus.304 aggregate; half-rate is a hypothesis | [ClashEval](../03_reading/V12/BR-A04-N08.md):L7–11, **2404.10198v3**, Tables2–4 | **Valid caution, not false-number accusation.** .608/2=.304, .041/2=.0205 and(.327+.903)/2=.615 fit balanced strata but do not reconstruct code. Both bias directions/calibration cost retained. Card plus arithmetic; no fix. |
| 23 | R:L525, S:L53, M:L33: non-rejection not equality; TypeII unstudied | [Circuit tests](../03_reading/V12/BR-A04-N11.md):L15–35, **2410.13032v1**, §3/5/App.E | **Valid statistical scope. P10** confirms explicit TypeII disclosure. Ties, sign-versus-magnitude and source pass-mark conflicts remain separate. No fix. |
| 24 | R:L527–529: CIF certifies a fixed bounded mean; adaptive sampling not uniformly better | [CIF](../03_reading/V05/BR-A04-N12.md):L9–23, **formal UAI2026**, §§2–3/Apps.C–G | **Valid scope.** Predictable proposal/support/weights and selection control; clipping changes estimand;102 versus1875 is not universal savings. Card-level formula check, not independent proof audit; no fix. |

### E — Learning dynamics: six packets

| # | Final line / claim | Actual card, edition and carrying lines | Adjudication / minimum correction |
|---|---|---|---|
| 25 | R:L571–577: inference-lag is a VAE explanation with extra encoder work | [Lagging Inference](../03_reading/V06/BIW-0096.md):L7–20, **1901.05534v2** | **Valid scope.**30–100 updates and2.20/3.73/2.19× wall time; slow annealing negatives preserved. Complete HTML carrying tables are legitimate read edition, not PDF failure=unread. Card only; no fix. |
| 26 | R:L661–663: ForkMerge common25k checkpoint one-step validation ≠ whole-history diagnosis | [ForkMerge](../03_reading/V06/BR-LD-N04.md):L7–20, **2301.12618v3**, Fig.2/App.B | **Valid scope.** Branches, validation selection and optimizer state count; interpolation is not exact multistep single-weight training. Card only; no fix. |
| 27 | R:L605–609: intermediate competitor helps formation; late contextual strategy still requires label | [Coopetition](../03_reading/V06/BR-LD-N05.md):L9–18, **2503.05631v2**, Fig.4 | **Valid scope.**9.8M–31.5M history is extra opportunity; resurgence and early/late negatives reject universal irreversible bypass claims. Card only; no fix. |
| 28 | R:L635–637: GenFirst640 versus320 epochs, generation/reconstruction reversal | [GenFirst](../03_reading/V06/BR-A05-N03.md):L13–22, **2608.29335v1**, Table2/App.C | **Valid budget/source distinction.** Reconstruction remains on; prior/entropy weights co-change; variant labels unresolved. Positive recipe remains, order-only coefficient absent. Card only; no fix. |
| 29 | R:L667–671: curvature proxy rank not Hessian/usable memory or exclusive cause | [Curvature](../03_reading/V13/BR-A05-N11.md):L13–16, **2312.00246v2** | **Valid version/scope.** Not renamed v4; per-example gradient Gram rank≤sample count; tanh/rank and leaky-ReLU/update countercontrols retained. Card only; no fix. |
| 30 | R:L613–617: ID loss improves while fresh-Markov-matrix generalization worsens | [Competition Dynamics](../03_reading/V13/BR-A05-N05.md):L7–16, **2412.01003v4** | **Valid scope.** “Retrieval” means trained transition matrices, not external documents; mixture fit is not unique circuit identity; diversity/horizon reversal retained. Card only; no fix. |

### F — Composition/host transfer: four packets

| # | Final line / claim | Actual card, edition and carrying lines | Adjudication / minimum correction |
|---|---|---|---|
| 31 | R:L713–717,S:L67: LoLCATs2transfer+2LoRA versus4LoRA | [LoLCATs](../03_reading/V07/BR-N06-07.md):L7–13, **2410.10254v3**, Table2 | **Valid meaningful total-envelope comparison, unequal stage doses. P04.** Teacher-fed local stage, early stopping, cache and passkey-format failure remain. No reversal or added warning needed. |
| 32 | R:L733–748,S:L67: RAM stage/metric reversals and500.040M | [RAM migration](../03_reading/V07/BR-N06-10.md):L11–15, **2610.11214v1**, Tables4/6/12 | **Reader arithmetic error corrected in final; source nominal discrepancy remains. P03.** The carrying card still prints500.000; this review does not edit it. Quality cells survive. No further final arithmetic repair. |
| 33 | R:L703–707: successful stitch can decode shared class prototypes, not arbitrary noise semantics | [Smith](../03_reading/V07/BR-A06-X04.md):L7–13, **formal ICML2025** | **Valid constructive counterexample.** Train/test share class prototypes with fresh sample noise; sender task/cues differ; random-source failures retained. Card only; no fix. |
| 34 | R:L727–729: strict GLA/GDN LAMBADA28.26/44.67 becomes68.70/69.01 with convolution | [Key to Going Linear](../03_reading/V07/BR-N06-12.md):L7–13, **2607.07706v1**, Tables1/3 | **Valid companion-dependent observation.** Strict versus relaxed permissions, reduced LoRA rate, added local/prefix cache and weak retrieval-heavy results remain. Not convolution universally explains failure. Card only; no fix. |

### Cross-axis utility, recent originals and independent interface: seven packets

| # | Final line / claim | Actual card, edition and carrying lines | Adjudication / minimum correction |
|---|---|---|---|
| 35 | R:L799,858–860: CMP random assignment differs from realized retrieval; missing excluded arm | [CMP](../03_reading/V09/BR-A08-V18.md):L7–13, **2610.02070v1**, Eq.5/6/App.C/H | **Valid source design/identification tension. P08.** Constant weights cancel only in nonempty actual arms; no blanket rejection of estimator family. No fix. |
| 36 | R:L866,M:L72: DR permits adaptive logging for bias, not unsupported/new-continuation value | [DR evaluation](../03_reading/V16/W0315.md):L6–13, **1103.4601v2** | **Valid estimator scope. P09.** Fresh iid contexts/reward vectors, independent nuisance fitting and support; stationary-logger variance simplification not imposed on whole paper. No fix. |
| 37 | R:L968–978,S:L77: T02 same-string robustness, support, clean negatives and one-layer theorem | [T02](../03_reading/V17/BR-R2-T02.md):L9–36, **2604.16037v1** | Empirical/theorem restrictions **valid**; precise split-count source issue lost in final. **P11/FBR-01.** No official-edition upgrade. |
| 38 | R:L897,S:L75: T03 stable-prefix theory differs from measured pretoken-waiting code | [T03](../03_reading/V17/BR-R2-T03.md):L9–25, **2610.19139v1** | **Valid theory/implementation split. P12.** Conditional family-level hardness, input-character delay and first-formed tokenizer timing are not every fixed tokenizer or serving speed. No fix. |
| 39 | R:L123,899,S:L75: T05 conditional mass mapping and49→9 code failure | [T05](../03_reading/V17/BR-R2-T05.md):L9–23, **2607.22334v1** | **Valid scientific distinction; citation/population repair P13/FBR-03.** Finite-token pushforward, interior conditioning and realized-path spanning mass are not unrestricted string law. |
| 40 | R:L881–885: Scratchpad v2 fixed-data gains coexist with matched-FLOP H-Net regression | [Scratchpad](../03_reading/V08/BIW-0076.md):L3–20, **2605.09630v2** | **Valid version update.** One work/one update;500M .7425>.7283 BPB;2B/400B reverses; one run/cell, local residual and unmeasured serving retained. Card only; no fix. |
| 41 | R:L758,915,919: MoCE is byte→byte, not mixed output; Ted/OPUS reverse | [MoCE](../03_reading/V14/BIW-0069.md):L3–11, **2411.01474v1** | **Valid science and corrected final title.** Card's “title exactly as above” remains an old reader editorial error; final restores full title. v2/camera-ready metadata is not read v2 numerical evidence. Card only; no final repair. |

## 5. Independently reopened original passages — thirteen distinct works

These are primary PDF/text passages actually inspected during this review, not citations copied from prior audit conclusions. Saved text is sufficient for these checks; no fresh network provenance or newly rendered image is claimed. Existing installed PyMuPDF parsed T02/Titans/PSR selected PDF pages in memory. Text links retain exact editions from their carrying cards. A selected passage check does not certify all proofs, tables or code in the source.

| Primary packet | Actual original/version and location reopened | Decisive passage or datum; independent conclusion |
|---|---|---|
| **P01** | [Anatomy2609.16183v1 text](../03_reading/V03/sources/2609.16183v1.txt), L250–257,299–311,696–698,728–730; §§4.2/10, PDF pp.5/12 | “0.561 vs…0.518…p=0.86” and “nothing left of the −0.32” coexist with “decay costs −0.32.” This is a real same-version source conflict; final R:L234 handles it correctly. Intro L39–43/55–59 reports512 training6/6 versus0/6; it does not establish extrapolation. |
| **P02** | [Titans2501.00663v1 text](../03_reading/V03/sources/W0234_2501.00663v1.txt), L330–332,375–388,595–597,1447–1451; actual PDF pp.6,7,26 additionally parsed | Main Eq.13 is `M_t=(1−α_t)M_(t−1)+S_t`; Appendix Eq.32 uses `M_t` on the right. Eq.16 prints previous-state versus boundary-state gradients across its equality. Source conflict/notation convention is confirmed, not implemented error. Proof absence remains “not located in this edition” inherited from the card/audit; this targeted check did not perform a new complete proof search. |
| **P03** | [RAM2610.11214v1 text](../03_reading/V07/sources/BR-N06-10__2610.11214v1.txt), L1489–1501,1734–1750; Tables6/12, PDF pp.22/26; Table4 L533–537 | Five displayed stage doses sum to **500.040**, while caption/final row say500M/500.0. Quality pairs16.33/68.1 versus16.82/66.6 and early77.56/51.7 versus23.90/61.2 corroborate final reversals. Exact sum was recomputed with Decimal; no missing-stage dose was invented. |
| **P04** | [LoLCATs2410.10254v3 staged text](../03_reading/_source_staging/access_recovery_20261109/BR-N06-07__2410.10254v3.txt), L370–386; Table2, PDF p.6 | Source explicitly says “2 with attention transfer,4 without, for equal total steps”; values2448.01→9.02 versus60.86→3.90 match. It is valid to preserve strategy superiority and withhold equal-stage-dose attribution simultaneously. |
| **P05** | [LeapQuant2609.38166v1 text](../03_reading/V03/sources/2609.38166v1.txt), L93–99,247–265,576–580; §4.3, PDF p.8 | “1.19 bytes per element” concerns boundary state including scales/compensators; a separate FP16 update buffer is “around8KiB per head per layer” for128×128. Final does not hide that retention channel. |
| **P06** | [LinQuant2610.39418v1 text](../03_reading/V09/sources/2610.39418v1.txt), L495–502,631–633,657–680; controlled/production experiment passages | “end-of-chunk states are passed in FP32…copy to an INT8 readout”; production uses INT8 recurrent prefill/W4A8. Final's distinction is sourced, not an assertion that all experiments use FP32 carry. |
| **P07** | [PSR0912.2385v1 text](../03_reading/V18/sources/BR-PSR-0912.2385v1.txt), L163–180,202–239,303–307,571–576,622–635; actual PDF p.4 also parsed | Eq.5a versus step3(a) dimension mismatch is printed. Fig.2D explicitly averages “only…78 successful paths”; prose reports22 looping failures and privileged A*. Thus formula clarification and success conditioning are distinct, both necessary. |
| **P08** | [CMP2610.02070v1 text](../03_reading/V09/sources/2610.02070v1.txt), L335–399,1241–1250,2158–2206; Eq.5/6/App.C.2/H.1 | Retrieval is `top-(B−k) union E`; Z denotes actual retrieved membership. H.1 says “90 inclusions and no exclusions…the Hájek estimate is undefined.” A fixed assignment count cannot manufacture that missing contrast. Source itself discloses a symmetric design; this is not a rejection of randomized exposure as a family. |
| **P09** | [DR1103.4601v2 text](../03_reading/V16/sources/W0315__1103.4601v2.txt), L54–85,125–178; §§2–3/Eq.1–2 | Logging may depend on history; nuisances are fixed independently of evaluation sample. Product-error bias derivation retains h. Final correctly avoids the stronger stationary-logger restriction on all bias claims and makes no off-support rescue claim. |
| **P10** | [Circuit-tests2410.13032v1 text](../03_reading/V12/sources/BR-A04-N11.txt), L595–600; §5 | “did not empirically study the Type II error” directly supports the final's statistical limitation. This primary check does not independently derive all five tests or reconcile every App.E pass mark. |
| **P11** | [T022604.16037v1 PDF](source_staging/R3_BR-R2-T02__2604.16037v1.pdf), pp.6,18–21 parsed directly | P.18 loops over K attempts and skips unsplittable selections; p.21 calls it “exactly” Pólya/DirMult. Pp.19–20 subtract aligned one-hot matrices and count changed substitution columns despite variable-length threat set. The first yields FBR-01; final's one-layer/variable-length theorem qualification already handles the second correctly. |
| **P12** | [T032610.19139v1 text](../03_reading/V17/sources/BR-R2-T03__2610.19139v1.txt), L2338–2387; printed pp.40–41, §6.1/6.2 | Source explicitly calls measured BPE “incremental (but not online),” waits for completed pretokens and allows arbitrarily long unfinished pretokens. Final correctly separates theorems, measured code and serving. |
| **P13** | [T052607.22334v1 text](../03_reading/V17/sources/BR-R2-T05__2607.22334v1.txt), L564–618,1044–1123,1571–1575; §4.3/App.C/H.2, PDF pp.8–9/16–17 | A1/A2/refinement and unbounded true-BPE approximation gap are explicit; spanning law is realized-path. The actual failure is GLM-Z1-9B BPM-JSD with128 generations/checkpoint, not every teacher/loss. §5 is conclusion, confirming FBR-03. |

## 6. Formulas, budgets and statistical interpretations

### 6.1 Algebra that is sound in the final

1. **Copy bound, R:L248–250.** After a deterministic one-pass encoder, each possible post-input state determines one output string. At most `|S|` of `D^L` equiprobable complete strings can be reproduced, so success≤`min(1,|S|/D^L)`. The non-strict inequality permits equality. For target success `1−ε>0`, the necessary bit condition is `log2|S| ≥ L log2 D + log2(1−ε)`. This elementary check does not certify the original paper's separate Transformer construction. Growing state, compressible/nonuniform tasks, approximate answers and query-first filtering change the promise; hidden caches must enter S.
2. **Delta collateral, R:L173–185.** Right multiplication by q yields the printed residual term exactly for fixed M,k,v,q,β. Orthogonality suppresses that substep's collateral term; it is not a trained semantic-address guarantee. Unit normalization matters for reading the new value back at k.
3. **Equal-key softmax merging, R:L367–375.** Group g contributes `exp(q·k_g) sum_i v_i` to the numerator and `c_g exp(q·k_g)` to the denominator. The displayed identity is correct after equalization. It is not a theorem for making unequal keys equal or for recurrent erase/decay transitions.
4. **Four-cell interaction, R:L499,762.** `Y11−Y10−Y01+Y00` is a background/metric-specific finite difference. It does not uniquely divide information or imply global/adaptive increasing returns. Final preserves that boundary.
5. **Local loss expansion, R:L643–653.** The first/second-order expression is a local approximation, not an exact training-trajectory identity. Positive raw inner product describes a sufficiently small descent step at that point. Momentum, preconditioning, clipping, decay and skipped steps make the actual update a different object. No missing historical optimizer state is reconstructed.
6. **T05 probability scope, R:L899.** Partitioning finite teacher next-token outcomes conserves mass; overlapping nested prefix masses are not themselves a probability distribution over all prefixes. The source's example has raw prefix masses summing1.9 but disjoint token scatter summing1. Exact conditional/refinement claims need their declared support/positive normalization; spanning paths do not sum every teacher continuation. The final does not assert unrestricted exactness.

The T02 skipped-attempt and PSR dimensional issues in §3 are the two remaining mathematical handoff corrections. They should be fixed locally rather than multiplying generic caveats across unrelated results.

### 6.2 Resource conclusions

- **RAM:** nominal500M and displayed500.040M are both reported accurately by the final. The still-incorrect card exact sum is a known reader error, not a reason to discard task scores or invent corrected source rows.
- **LoLCATs:** planned total epoch/step envelope is a genuine comparison. Stage doses, teacher forwards, early-stopped realized work and recent KV are not matched just by that envelope. Final does not unfairly call all training unmatched.
- **GenFirst:**640 versus320 epochs and later prior/decoder stages leave an order-only attribution unidentified; generation positives survive. It is not evidence all staged methods fail.
- **State precision:** boundary bytes, buffers, bases, Gram/covariance state and fast optimizer state are carried as resources, not erased by a nominal low-bit/rank label. LinQuant's controlled FP32 carry is not generalized to its production prefill; neither is presented as long-horizon decode proof.
- **Scratchpad/T03:** transient computation, committed trunk KV, tokenizer first-formed output, full-model serving memory and latency remain separate. Lower BPB or tokenizer delay does not establish remote content consumption.

No numerical run length, sample size, architecture threshold or training authorization follows from these checks. M:L13–18 correctly distinguishes source review, forward computation, backward analysis, fitted diagnostics and new main-model training. The proposed comparisons are not reported as executed.

### 6.3 Statistical conclusions

R:L523–531 and M:L24,33 correctly keep estimand, donor/reference law, ties, power and selection separate. Circuit-test non-rejection is not magnitude equivalence or a positive proof of non-use. CIF's fixed bounded mean and predictable support-weighted sampling do not validate semantic donors; clipping can suppress negative/over-recovery values. Source/entity clustering and discovery/evaluation separation are proposed, not already demonstrated on the target host.

CMP's constant-propensity cancellation is algebra, not identification. Both nonempty actual arms and compatible backgrounds matter. Its source's zero-exclusion example is decisive against a blanket treatment-support guarantee, not against every reported measurement. DR's independent nuisance fitting/support assumptions do not turn model extrapolation into observed counterfactual data. Neither source identifies future retention or a new continuation policy from one-step rewards.

The ClashEval half-rate arithmetic is a plausible denominator reconciliation, not verified matcher/code. The final correctly avoids charging the source with false point estimates. T05 bootstrap is not multi-training-seed uncertainty; the final's task-negative and selection warnings should remain alongside the population repair in FBR-03.

## 7. Counts, versions, original scope and the unavailable-body gap

### 7.1 Independent accounting checks

A read-only validator parsed the **current128 actual card receipt rows**, resolved all128 unique card paths, and recomputed their SHA-256 values. **All128 matched their recorded digests.** This validates the snapshot and accounting, not whether every FULL declaration is scientifically warranted.

| Quantity checked | Result / interpretation |
|---|---|
| Current assigned edition rows | **103 FULL +6 PARTIAL +19 BLOCKED=128**;128 distinct task/card paths |
| Alternate FULLs among incomplete assigned sources | Exactly **5**: R04 public2203.07004v2;W0143 public2306.07174v1;T02 public2604.16037v1;T03 public2610.19139v1;T05 public2607.22334v1 |
| Some-FULL-source work view | **108 FULL-work /5 PARTIAL-work /15 BLOCKED-work**; one PARTIAL and four BLOCKED assigned sources move categories in this view, adding zero works |
| Original completions versus old work update |108 includes107 new original-work completions plus1 Scratchpad update;281+107=388 is inherited/new ledger union, not388 independently verified studies |
| Registered clusters |780=632+140+1+6+1 follows current catalog/count overrides; no whole-register identity or source-truth audit performed here |
| Metadata source union |50=46 active+3 withdrawn+1 desk-rejected is an attributed, deduplicated status union; R3's18 checks overlap it and are not18 additions or FULL reads |
| Official body gaps |17=old6+V17six+V18five. Three public alternate FULLs leave14 works without an alternate established, **not14 official gaps** |
| Acceptance decisions |0 established; active submission, notev2, PDF edition, arXiv revision, modification time and withdrawal-event time remain distinct |

R:L41–45,936–988;S:L17–21;O:L9–17;V:L30–44 reconcile these denominators correctly. There is no detected inflation from edition pairing, source audit, Scratchpad update or public preprint acquisition. Historical paragraphs in CATALOG/COUNTS are not added a second time. Report use of780 is an inventory boundary, not a scientific endorsement.

### 7.2 Exact167-direction preservation versus scientific closure

Read the canonical list and compared its eight ordered groups with the final crosswalk. Programmatic checks found **167 unique final direction anchors** with exact totals **A20/B22/C20/D20/E22/F19/I28/R16**, and each of the167 original Chinese bullets occurs exactly once in the catalog's exact-text packets. Current catalog has167 individual disposition rows. These are structural/accountability checks, not167 source-validated answers.

The final report independently carries the latest PSR/T02 completion where older catalog residual wording is stale. R:L1071 explicitly no longer treats learned identification as wholly unread;R:L1169/L1184 use the actual T02/T03 editions;R:L1177 retains mixed byte/nonbyte output as unresolved. Neighboring questions retain distinct meaning: rarity versus entropy/identifier/order/binding; query-first versus time-late relevance; independent q versus independent content; probe/native/use/correctness; formation versus endpoint; self-replay versus reset/relearning. The original broad questions therefore survive in substance, not just matching section counts.

The main axes have viable native no-original-return mechanisms, and G–J preserve source/fallback, lifecycle, relations and utility without turning them into B/E/F replacements. The independent byte section keeps four units and small-head/remote-use gaps. No architectural winner follows from accessible literature defeating unavailable alternatives. The user-authorized substantial rewrite is reflected by the structure and comparisons; this review does not substitute the earlier byte survey or multigranularity proposal for that deliverable.

### 7.3 Honest recent-source completion

Final R:L944–960 and O:L21–37 name all17 bodies, including incentive, SDG, two transfer, routing lock-in, predictive bottleneck/scope, six interface candidates, loop refinement, farsighted correction, finite-query compilation and attention placement. Each remains a submission snapshot with unknown exact official manuscript edition. T03's **Linear Time** public title versus **Near Linear Time** official title is preserved. T02 spelling/abstract and T05 matching-title relationships do not establish manuscript equality or anonymous identities. PSR2009 is foundational, not a recent ICLR result. R3's acquisition-only T02 snapshot is appropriately superseded by the actual later FULL card, without awarding R3 reading credit.

**What can be delivered now:** a broad source-linked synthesis of read editions, selected official submission metadata, explicit unadjudicated recent alternatives, and conditional experiment decisions. This is scientifically useful and does not require waiting for every unrelated source gap.

**What cannot be marked complete:** the stronger selected-official-original full-reading/result-adjudication objective, exhaustive recent conference coverage, a novelty certificate or an all-cost architectural ranking. Completing those particular source-dependent claims needs the missing legitimate originals and edition comparison. An authorized user-supplied manuscript or legitimate changed access condition could help; access to an account cannot be assumed and a challenge is not permission to bypass. Alternatively, a bounded deliverable may be accepted expressly with that requirement still open, not silently lowered.

No fresh external metadata, denied-route retry, author matching, or paper download was performed by this review. Source R1/R2/R3 are the provenance for official observations; this is not a new live venue check. Their actual query limits, caches and per-paper access distinctions remain relevant.

## 8. Ownership, snapshot and verification receipt

Only **`docs/research/flued_broad_research_v2/05_review/FINAL_BROAD_RIGOR_REVIEW.md`** is authored. No author file, card, catalog, source PDF/text, project guide, evidence registry or older report is edited. No subagents, installs, network acquisition, training, checkpoint operations, paper-code execution, commits or pushes. In-memory PDF parsing and exact Decimal/Fraction applicability calculations created no script, rendered image, log or other persistent artifact.

Five final English input SHA-256 values checked during review:

| File | Reviewed SHA-256 |
|---|---|
| REPORT_EN.md | `880b96add23f90ba0f0f82832668d11c4a80d40c1815981de8b47511f35ba516` |
| EXECUTIVE_SUMMARY_EN.md | `e89cb06d97d0743e45c251f7832026b7222511bb3ee853a9a08d77ccfa932e1e` |
| EXPERIMENT_DECISION_MATRIX_EN.md | `977ac9472c5d9f29810cf79b1562b356ba03ab901633fd626375365de7ca744f` |
| OPEN_EVIDENCE_EN.md | `cdf772225dbeae3d103930d7c26fe258bb3cfb02e80f06ded692a4f8d0cfcc39` |
| REVISION_LOG_EN.md | `43daa3cd396b84bae6aa111ea0d269d7552bcec2d1f0c5e398099890e5dcc571` |

Verification covers this file's strict UTF-8, final newline/trailing whitespace, local Markdown targets,41 unique sample rows/actual card links,13 distinct original-source packets,128 receipt hashes/dual counts,167 original bullets/anchors, elementary ledger/algebra checks, and final repository status. These checks do not validate every paper result. Software build/pytest is not relevant to this Markdown-only review and was not run. The entire v2 research root and unrelated proposal/bundles were already untracked at entry; Git status cannot attribute concurrent writers' files, and they are left untouched.

**Final disposition:** **bounded-ready in substance; needs FBR-01/FBR-02 and the small FBR-03 repair before the current English release is signed off.** After those changes, no broad rewrite or extra title quota is indicated by this sample. The17 official bodies and local experiments remain open, and this document grants neither comprehensive scientific coverage nor architecture-selection readiness.
