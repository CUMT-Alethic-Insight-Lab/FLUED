# Final broad rigor recheck — scientific wording passed; original-source obligation remains open

**9 November 2026. Targeted recheck only. Owned output: this file.**

## 1. Decision and translation boundary

**PASS for the requested scientific-text repairs: FBR-01 P1, FBR-02 P1 and FBR-03 P2 are closed at the revised English wording/handoff level.** The revisions meet the actual conditions of [FINAL_BROAD_RIGOR_REVIEW §3](FINAL_BROAD_RIGOR_REVIEW.md), not merely its suggested keywords. No additional P0/P1/P2 wording defect is confirmed within these three rechecked packets.

**The revised five-file English bounded synthesis may enter complete Chinese translation from this rigor gate.** Translate the substantive six-axis report, all167 direction dispositions, summary, decision matrix, open evidence and revision log—not only the repaired paragraphs. Preserve the source-version restrictions and unfinished obligations in their main-text locations. Use the revised five final files, not the superseded thematic drafts or earlier snapshots.

**This does not complete the overall original task. Seventeen selected official manuscripts remain unread/unavailable, and their result adjudication and official/public edition comparison remain unfinished requirements.** Translation permission is not acceptance of reduced scope, new source-reading credit, or a declaration that the missing originals are unnecessary. The current broad synthesis is useful without pretending that the stronger recent-original requirement has been satisfied.

This is the follow-up to the previous41-packet/13-primary-work review, not a new broad audit of that entire sample or the780-cluster register. Additional revisions addressing coverage/navigation/selective execution are outside this three-finding scientific recheck; their separate review dispositions are not overridden. Chinese fidelity and any other independently required review remain separate checks. No translation has been performed here.

## 2. Inputs actually checked

Read the original three finding definitions and minimum repairs in [FINAL_BROAD_RIGOR_REVIEW](FINAL_BROAD_RIGOR_REVIEW.md):L29–73. Inspected the actual revised report passages and corresponding summary, matrix, open-evidence and revision-log entries. Reopened the three carrying cards at relevant lines and selected primary passages:

- **T02 public2604.16037v1:** actual [saved PDF](source_staging/R3_BR-R2-T02__2604.16037v1.pdf), pp.18 and21, parsed in memory; [card](../03_reading/V17/BR-R2-T02.md):L9–14. Algorithm1 and AppendixF are checked directly, not inferred solely from the repair log.
- **PSR public0912.2385v1:** [original saved text](../03_reading/V18/sources/BR-PSR-0912.2385v1.txt):L163–240 and297–311; [card](../03_reading/V18/BR-PSR-0912.2385.md):L15–28. The dimensions and three printed expressions are directly compared.
- **T05 public2607.22334v1:** [original saved text](../03_reading/V17/sources/BR-R2-T05__2607.22334v1.txt):L374–378,564–618,1571–1575; [card](../03_reading/V17/BR-R2-T05.md):L19–23. Checked fixed student identity, teacher/divergence, section locator, outcome and separate probe denominators.

Also checked the revised files' explicit17-body completion boundary and current dual-count descriptions. This pass does not newly acquire sources, refresh official status, inspect paper implementations, prove whole theorems, rerun the128-card hash census, or award FULL credits. The earlier wider review remains the evidence for its unchanged inspected claims; this receipt supersedes only its three outstanding wording repairs.

Locations below use physical lines in the revised files. `R`, `S`, `M`, `O`, `V` refer respectively to [REPORT](../04_synthesis/REPORT_EN.md), [SUMMARY](../04_synthesis/EXECUTIVE_SUMMARY_EN.md), [MATRIX](../04_synthesis/EXPERIMENT_DECISION_MATRIX_EN.md), [OPEN](../04_synthesis/OPEN_EVIDENCE_EN.md), and [REVISION_LOG](../04_synthesis/REVISION_LOG_EN.md). Earlier review line numbers are historical.

## 3. Item-by-item closure against original conditions

| Original finding | Revised evidence inspected | Original condition tested | Result |
|---|---|---|---|
| **FBR-01 / P1 — T02 skipped attempts versus exact count law** | R:L982–984;S:L77;M:L74;O:L64;V:L33,77 | Disclose Algorithm1/AppendixF mismatch, actual realized count versus nominal attempts, feasibility/cap gate; preserve empirical positives and public-edition FULL | **PASS — scientific wording/handoff fixed.** Actual sampler/equivalence clarification remains open. |
| **FBR-02 / P1 — PSR initial-estimator dimensions** | R:L293–297;S:L37;O:L13,65;V:L35,78 | Name printed step3(a), dimensions and Eq.5a/Eq.10a conflict; no invented implementation repair or inferred empirical failure; retain success denominator/resources | **PASS — scientific wording/handoff fixed.** Literal source equation/code reconciliation remains open. |
| **FBR-03 / P2 — T05 locator/population** | R:L123,912–913;S:L75;M:L74;O:L66;V:L34,79 | Correct §5→§4.3; attach GLM-Z1-9B/BPM-JSD and128-generation/checkpoint population; distinguish margin probe; preserve other results/probability limits | **PASS — citation and population fixed.** No additional source acquisition needed for these quotations. |

### 3.1 T02: the repair does not quietly assume that feasibility conditioning solves the issue

The source's Algorithm1 p.18 sets a bounded number of attempts, samples a current token, and changes the sequence only when a valid split exists. AppendixF p.21 nevertheless says the process “corresponds exactly” to a Pólya urn and draws `DirMult(N,1)` to preserve its split-count distribution. The two statements are not unconditionally equivalent.

The original review's elementary case remains applicable: canonical `[a,bc]` with vocabulary `a,b,c,bc`, one attempt, yields no split or a split of `bc`, each with probability1/2. `DirMult(1,(1,1))` puts probability1/2 on an infeasible split of `a` instead of no split; renormalizing to feasible counts forces the `bc` split and still disagrees. This is a source-law applicability problem, not evidence that the paper's reported training cells are fabricated or reversed.

The revised R:L982 now labels the distributional technique **idealized**. R:L984 explicitly states that skipped unsplittable attempts are not unconditionally described by the claimed exact law, that feasible-count renormalization need not recover the realized law, and that successful-split assumptions plus skip/cap/feasibility handling need reconciliation before equivalence/reproduction. O:L64 records the corresponding artifact gate; V:L77 records the repair and remaining obligation. This satisfies the original P1 without claiming that merely counting successes is a sufficient general implementation fix.

The existing same-decoded-text support restrictions, local attacker scope, clean negatives and one-layer aligned-substitution bound remain in R:L982–992. Official T02 remains BLOCKED while the public preprint stays FULL. No reader/card downgrade or general robustness theorem is introduced. **No further correction is required for FBR-01.**

### 3.2 PSR: source formula error is not equated with empirical failure

Original text L163–180 defines `P_H` as a history-count vector and `P_(T,H)` as a test-count by history-count matrix. Its left singular-vector matrix `U` has shape `|T| × n`. Eq.5a at L202 uses `U^T P_(T,H) 1_k`, step3(a) at L235 prints `U_hat^T P_hat_H`, and feature Eq.10a at L303–309 uses the moment matrix with the feature constant-vector construction.

Thus the printed step3(a) product has dimensions `(n × |T|)(|H| × 1)` and is undefined when the cardinalities differ. Equal cardinalities do not generally turn it into the Eq.5a expression. This is a printed source inconsistency, not a newly observed implementation failure.

Revised R:L293 names the actual printed expression, both reference equations, and the unequal-cardinality failure. It explicitly leaves literal reproduction to reconciliation and disclaims an inspected code repair or empirical-failure inference. O:L65 additionally preserves the equal-size qualification and the prohibition on presenting a dimension-compatible expression as a verified code repair. V:L78 records that boundary.

R:L295 still reports **78/100 successes,22 looping failures,18.2 actions averaged only over successes**, privileged A*, and the feature/moment/operator/planning resources accompanying five coordinates. S:L37 preserves those distinctions. Rank, exploration, conditioning and approximate suffix-history sampling remain in R:L293. **No further correction is required for FBR-02.** The P1 writing requirement is closed; the paper's algorithm-description issue is not thereby resolved.

### 3.3 T05: outcome, treatment and denominators now travel together

The actual original heading at text L564 is **§4.3 Whitespace Collapse**, not §5. Fig.3's caption at L600 specifies **GLM-Z1-9B BPM-JSD**. L609–618 reports49%→9%, the otherwise-identical mask comparison, and the failed random non-whitespace mask control. AppendixH.2 at L1571–1575 gives **128 generations per checkpoint at temperature1.0** for graded pass/error diagnostics and separately **80 programs/1,799 positions** for the margin probe. L374–378 identifies **Qwen3.5-2B as the common student** across teacher pairs.

R:L123 now cites §4.3 and labels the result teacher/student/divergence-specific. R:L913 carries the teacher, student, BPM-JSD no-mask arm,128-generation/checkpoint diagnostic and temperature. It explicitly separates the margin probe, rejects an all-arm or multi-training-seed interpretation, and retains the mask/random-mask contrast. S:L75 and M:L74 carry the same scoped numerical quotation; O:L66 and V:L79 match.

The main probability distinctions are retained: mass conservation is not unrestricted string-probability exactness; conditional refinement and realized-path spans differ; the main Table1 best-divergence arm is forward KL rather than this JSD failure arm. These qualifications do not erase the actual code failure or positive results. **No further correction is required for FBR-03.**

For translation, “fixed student” here means **the same student-model identity across the compared teacher/objective settings**, not that its weights remain frozen during distillation. Do not translate it as a frozen-student training condition.

## 4. Three different statuses must remain separate

| Status | Recheck conclusion | What this does not establish |
|---|---|---|
| **Scientific wording of the two P1s and T05 P2** | **Passed.** The author-side omissions/citation defect are repaired in the reviewed English snapshot. | T02's exact runtime count-law equivalence or PSR's literal estimator implementation has been validated. |
| **Translation readiness from this targeted rigor gate** | **Yes.** The revised five final English files can be translated in full as a bounded scientific synthesis with open obligations. | Chinese fidelity is already checked, every other audit is overridden, or this is a new whole-report scientific certification. |
| **Overall original task / selected official-original reading** | **Not complete.**17 intended official bodies and dependent result/edition adjudication remain open. | Three public alternates or the50-record metadata union fulfill17 official body reads; report/translation delivery implies user acceptance of reduced scope. |

The original wider review's sample boundary also remains unchanged:41 purposive claim packets/13 primary works are not endorsement of780 clusters. This targeted recheck adds no paper-reading credits or replication evidence.

### 4.1 Completion boundary remains visible, not relegated to an appendix

The revised files explicitly state the outstanding original-task obligation:

- **R:L954**, alongside the17-row official-body table at L958–974: legitimate original availability or authorized source provision followed by actual reading is still needed; delivery does not complete the overall task or presume reduced-scope acceptance.
- **S:L21:** the17 official-body readings/result adjudications remain an unfinished requirement.
- **M:L89:** proposed experiments and the delivered synthesis do not substitute for actual legitimate sources and reading.
- **O:L9:** the gap is an unfinished original-task obligation, not a limitation silently accepted in exchange for the report; O:L21–37 names all17 sources.
- **V:L84,88–92:** the original-body obligation remains incomplete, and static validation does not itself supply independent review or bilingual fidelity.

The three scientific repairs therefore **do not close the17-body gap**. The named public T02/T03/T05 editions remain usable at their own versions, not certified anonymous-manuscript equivalents. PSR2009 remains foundational, not a recent ICLR2027 result. The current count distinction **103/6/19 assigned editions versus108/5/15 some-FULL-source works** remains visible in R:L41 and S:L17; no new work or official completion is claimed for these edits.

This pass verifies the continuing disclosure, not a fresh network/access census. To complete the stronger requirement, lawful original files/access must actually become available and be read at declared editions, with the related claims re-adjudicated. A genuinely changed ordinary public route, legitimate independently identifiable edition or authorized user-provided source can support that work. No bypass, anonymous-author matching or repeated challenge probing is authorized. If a bounded deliverable is accepted separately, that acceptance must be explicit; this recheck does not make that decision for the user.

### 4.2 Translation carry-forward requirements

Translate the revised five-file snapshot identified in §5, preserving:

1. The **full six-axis and167-direction scope**, including the independent interface and alternative-route sections. Do not replace the broad report by the byte survey or proposal, or omit unresolved directions because they lack a final answer.
2. **T02:** attempts versus realized successful splits; canonical-token conditional support versus whole-string support; idealized count law versus actual skipped-attempt process; source-law clarification versus reported empirical result.
3. **PSR:** printed formula inconsistency versus learned-identification evidence; positive-probability/rank/exploration assumptions; success-only18.2 with78 successes/22 failures; full resource ledger rather than “five numbers solve the task.”
4. **T05:** one GLM-Z1-9B/Qwen3.5-2B BPM-JSD no-mask setting;128 generations/checkpoint versus80 programs/1,799 margin positions; pass-rate diagnostic versus aggregate best-forward-KL result; conditional conservation/refinement versus unrestricted byte law.
5. The **17 missing official bodies as an unfinished task requirement** in the main report and summary, with actual public/official edition distinctions, not just a translated footnote. Do not render “bounded-ready for translation” as “the overall research task is complete.”

No further generic caution paragraph is required for these three findings. A later translation fidelity check should verify these exact distinctions and numerical denominators. This document does not perform that translation or fidelity check.

## 5. Snapshot, verification and ownership

The targeted English snapshot is identified by SHA-256:

| File under `04_synthesis/` | Rechecked SHA-256 |
|---|---|
| REPORT_EN.md | `8a9428deb35fa26eb54d05df6136f99d63af621f5eab31c047718fa1515f88d0` |
| EXECUTIVE_SUMMARY_EN.md | `bbde1489b4537f6c4f6ffc2bdea33c42c2c4002c276af30b69731902f7fccd01` |
| EXPERIMENT_DECISION_MATRIX_EN.md | `f4807a7ec936ad21ea505ab0d475e317f64879879282c48d7c4019fd0acc92b8` |
| OPEN_EVIDENCE_EN.md | `433234712cd25d0274bf8fcca1c5abcb758bdece862dbe9f4bb6d236e90d6d3a` |
| REVISION_LOG_EN.md | `903f6c1d4ae3f0af283f09a3ff820ffe2a1907d940c39cd1cda2c160a1b0cce5` |

Verification covers actual revised finding locations, the three selected original-source packets, presence of17 distinct official-body rows, this file's strict UTF-8/newline/whitespace and local Markdown targets, and unchanged five English-file hashes during this review. The previous wider audit's128 hashes/167 coverage checks are not falsely recounted as new scientific validation. Repository status is checked for unintended artifacts; the research root and unrelated proposal/bundles were already untracked at entry.

Only **`docs/research/flued_broad_research_v2/05_review/FINAL_BROAD_RIGOR_RECHECK.md`** is authored. Report, summary, matrix, open evidence, revision log, cards, originals and prior reviews remain untouched. No subagents, installations, downloads/network queries, model fitting/training, checkpoints, paper-code execution, commits or pushes. Existing local PDF parsing created no new persistent source or rendered image. Software build/pytest is not applicable to this review-only Markdown deliverable and was not run.

**Final disposition: two P1 scientific-handoff repairs and the T05 P2 correction PASS; revised bounded five-file translation may proceed from this rigor gate;17 official-original readings/result adjudications and overall task completion remain OPEN.**
