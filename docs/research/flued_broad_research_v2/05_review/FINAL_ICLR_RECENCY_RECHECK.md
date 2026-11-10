# Final ICLR recency recheck — limited corrections and partial-results translation

**9 November 2026. Owned output: this file only.** This is a targeted recheck of the three P1 corrections, the T05 §4.3 locator, and the 17-missing/five-alternate source identities in the revised English deliverables. It is not a fresh conference survey, new original-paper reading batch, complete scientific review of any paper, proof certification, code validation, replication, or architecture-selection decision.

## 1. Decision

**PASS for the requested limited recheck and for carrying this recency material into a translation explicitly presented as partial research results.** All **3/3 prior P1 textual corrections and 1/1 citation correction** are implemented. All **17/17 missing-official identities and 5/5 independent alternate-edition identities** remain correctly separated. No new P0/P1/P2 correction is identified within this recheck's scope.

This closes the specified **reporting corrections**, not the underlying source problems or scientific questions:

- T02's actual skip/cap/feasibility implementation and split-law reconciliation remain unresolved.
- The predictive-state paper's printed initial-estimator discrepancy remains unresolved before literal reproduction; no implementation repair or empirical failure is established.
- T05's corrected numerical scope is one teacher/student/divergence/probe setting, not a result about all arms, all whitespace, or all cross-tokenizer distillation.
- **All 17 selected official manuscript bodies remain unread/unavailable at the inherited evidence snapshot. Their original-reading/result-adjudication gate stays OPEN.** Three public preprints do not reduce this count to14, and the two older formal/public alternates do not complete any of those17.

The user's latest instruction explicitly permits a **partial-results translation**. That authorization does not waive the17-body requirement or establish comprehensive ICLR coverage. Conversely, the17-body gate must not be turned into a new requirement to postpone an honestly labeled partial-results translation. This recency sign-off does not claim completion of other independent reviews or bilingual fidelity work.

## 2. Scope, inputs, and evidence provenance

### Final English files inspected at the relevant revised locations

| Short name | File and current physical lines checked |
|---|---|
| R | [REPORT_EN.md](../04_synthesis/REPORT_EN.md): L27–45 scope/count/reading definitions; L123 T05 locator; L287–297 predictive state; L908–915 T03/T05; L945–1004 recent section,17-row table and five-alternate table. Also checked conference/identity wording returned by targeted text search. |
| E | [EXECUTIVE_SUMMARY_EN.md](../04_synthesis/EXECUTIVE_SUMMARY_EN.md): complete current summary; especially L17–21,37,75–77. |
| M | [EXPERIMENT_DECISION_MATRIX_EN.md](../04_synthesis/EXPERIMENT_DECISION_MATRIX_EN.md): relevant current correction/boundary passages, especially M30 L74 and completion boundary L89. |
| O | [OPEN_EVIDENCE_EN.md](../04_synthesis/OPEN_EVIDENCE_EN.md): complete current document; especially L9–17,21–39,64–66,99–101. |
| V | [REVISION_LOG_EN.md](../04_synthesis/REVISION_LOG_EN.md): complete current log; especially L33–35,42–44,73–84. |

`L` identifies physical lines of this inspected Markdown snapshot, not publisher page/line numbering. Other revisions can move these locations; hashes in §7 pin this recheck's inputs.

Read the prior [FINAL_ICLR_RECENCY_REVIEW](FINAL_ICLR_RECENCY_REVIEW.md), especially its four correction contracts; current [RECENT_ORIGINAL_CLAIM_RULES](RECENT_ORIGINAL_CLAIM_RULES.md); relevant official identity/status rows in [source R3](ICLR2027_SOURCE_AUDIT_R3.md), L65–100; and current [COUNTS](../02_catalog/COUNTS.md), L1–30. Reopened the five alternate cards' edition/status passages: [R04](../03_reading/V01/BR-A01-R04.md), [W0143](../03_reading/V15/W0143.md), [T02](../03_reading/V17/BR-R2-T02.md), [T03](../03_reading/V17/BR-R2-T03.md), and [T05](../03_reading/V17/BR-R2-T05.md), including T05's treatment/teacher/student restrictions.

**Actual new work:** local comparison of revised text with those correction contracts; identity/count reconciliation; current-input hashing and documentation checks. **No new network calls, attempted metadata refreshes, verification-wall retries, acquisitions, whole-paper reads, PDF rendering, proof audit, paper-code execution, or experimental reproduction.** Source R3's successful metadata observations and the prior review's selected primary-passage checks remain attributed to those records, not rebranded as new observations here. This recheck earns **0 new FULL credits, 0 official-body completions, and 0 new acceptance/edition-equivalence confirmations**.

The four earlier thematic drafts are intermediate inputs, not the final five deliverables reviewed here. Their old pending T02/count language must not be substituted for the revised report during translation. This is a translation-input precaution, not a demand to edit those other owners' files or a new global scientific finding.

## 3. Correction-by-correction disposition

| Prior finding | Revised text inspected | Recheck result and residual boundary |
|---|---|---|
| **P1-01 — T02 split-count correspondence** | R L982 calls the allocation idealized; L984 explicitly distinguishes skipped unsplittable attempts from Appendix F's exact Pólya/Dirichlet–multinomial law, says feasible-count renormalization need not reproduce the realized law, and retains successful-split/skip/cap/feasibility clarification before equivalence/reproduction claims. O L64 adds the exact Algorithm1 p.18/Appendix F p.21 artifact row; E L77, M L74 and V L33/L77 propagate the restriction. | **CLOSED as a reporting omission.** Actual sampler implementation/equivalence is **not resolved**. No whole-paper invalidity, misconduct, code failure, or general absence of robustness is inferred. Reported positive and negative task cells and the existing public-edition FULL declaration remain separate. |
| **P1-02 — predictive-state initial estimator** | R L293 names printed `U_hat^T P_hat_H`, compares Eq.5a/Eq.10a, gives test-count/rank versus history-count dimensions, and withholds literal reproduction pending reconciliation. O L65 names the formula/source-artifact gate; E L37 and V L35/L78 preserve the caution. R L295 retains78/100 successes,22 loops, success-only18.2 actions and privileged A*; the2009 source is not a recent ICLR result. | **CLOSED as a disclosure omission.** This is a source-formula discrepancy, **not an inspected implementation repair** and not evidence the reported learner failed empirically. Code reconciliation, finite-data reliability, total cost and language transfer remain open. FULL is neither revoked nor upgraded to independent correctness certification. |
| **P1-03 — T05 numerical population/treatment scope** | R L913 specifies **GLM-Z1-9B teacher / fixed Qwen3.5-2B student / BPM-JSD no-mask**,49%→9%, **128 generations per checkpoint at temperature1.0**. It separates the80-program/1,799-position margin probe, same-mask/random-non-whitespace controls and headline best-divergence forward KL. E L75, M L74, O L66 and V L34/L79 retain the scope. | **CLOSED as a numeric-scope omission.** Not every teacher/divergence, not multi-training-seed uncertainty, and not the aggregate final benchmark result. Mass conservation remains distinct from conditional refinement exactness and realized-path spanning lower bounds; unrestricted byte-string law, EOS identity, all-whitespace semantics and total-cost advantage are not established. |
| **P2-01 — §5→§4.3 locator** | R L123 now says **§4.3, Fig.3 pp.8–9, Appendix H.2**. R L913 and E/M/O/V use the same corrected provenance. | **CLOSED as a citation correction.** No altered experimental outcome, extra paper read, or new correctness certification follows. |

The restrictions match the prior review and latest claim rules: [T02 §2.1](RECENT_ORIGINAL_CLAIM_RULES.md), [predictive state §5](RECENT_ORIGINAL_CLAIM_RULES.md), and [T05 §4.2](RECENT_ORIGINAL_CLAIM_RULES.md). Their scientific support is inherited from the earlier targeted original checks, not independently repeated end-to-end in this recheck.

**No source-error-to-comprehensive-review promotion:** fixing author/source formula or scope issues supports only those named corrections. It does not prove all remaining formulas, appendices, datasets, controls, costs or implementations correct; nor does finding a local error invalidate every empirical cell. The phrase “recheck passed” must always retain that limited object.

## 4. All17 official missing rows remain source-gated

The current R table is L958–974; O's matching table is L21–37. Each row still states **Submission snapshot**, **BLOCKED**, and **unknown official PDF edition**. The17 unique forum IDs match source R3's cohort exactly and appear once in each current table. Status here is inherited official-response metadata, not live verification.

| # / current R line | Official work label | Official forum identity | Rechecked disposition |
|---|---|---|---|
| 1 /L958 | Incentive | `UUldzWxIL4` | BLOCKED; no independent alternate established; no body-level “not capacity” verdict. |
| 2 /L959 | SDG | `lYWcLB1rAh` | BLOCKED; no alternate established; chunk/serial gate and matched-work claims withheld. |
| 3 /L960 | Cross-Model Stitching | `98Rbm5C5Bl` | BLOCKED; no alternate established; title does not certify answer-versus-computation transfer. |
| 4 /L961 | Receiver State | `2M4nt7AFuD` | BLOCKED; no alternate established; receiver repair remains an abstract-screened hypothesis. |
| 5 /L962 | Routing Lock-In | `9vT48Lms48` | BLOCKED; no alternate established; general irreversibility not imported. |
| 6 /L963 | Predictive-State Bottlenecks | `58JxyfvZJj` | BLOCKED; no alternate established;2001/2009 foundations do not replace this official result. |
| 7 /L964 | T01 Formal Guarantees | `FXLPTx7osi` | BLOCKED; no alternate established; corpus compression certificate not downstream sufficiency. |
| 8 /L965 | T02 Stochasticity | `rIRkUxOleG` | BLOCKED official; separate public2604.16037v1 FULL declaration, candidate relationship only. |
| 9 /L966 | T03 Online Tokenization | `8D7l5sK3YT` | BLOCKED official; separate public2610.19139v1 FULL declaration; **Near Linear Time** versus **Linear Time** remains explicit. |
| 10 /L967 | T04 Late/Head Invariance | `63kZK7oyd6` | BLOCKED; no alternate established; no general head-localization or head-only remedy. |
| 11 /L968 | T05 Byte-Prefix Distillation | `Mm5OLOPLT0` | BLOCKED official; separate public2607.22334v1 FULL declaration, no manuscript equivalence. |
| 12 /L969 | T06 B-Net | `fMymbXoq9T` | BLOCKED; no alternate established; no online-rate/prefix-safe controller guarantee. |
| 13 /L970 | LoopLA | `xzOnjQHMr9` | BLOCKED; no alternate established; no body-supported free loop/refinement gain. |
| 14 /L971 | Farsighted Correction | `JrKJaRbQpz` | BLOCKED; no alternate established; starvation/proxy/remedy results source-gated. |
| 15 /L972 | Finite-Query Compilation | `OQhOBMNVeN` | BLOCKED; no alternate established; no unknown-future-query exactness or minimum-slot theorem imported. |
| 16 /L973 | Attention Placement | `0fPxp7a50O` | BLOCKED; no alternate established; scaffold versus final recurrent/attention answer path unresolved. |
| 17 /L974 | Predictive Scope | `uILf1c6VDo` | BLOCKED despite recovered PDF reference; no alternate established; no equal-bit scope cure or language transfer. |

The cohort remains **old6 +V17six +V18five =17**, not every unread submission across the research program. The14-without-an-alternate count is a different field: public T02/T03/T05 do not supply the official bytes. Missing bodies remain possible counterevidence, not evidence against the authors or a reason to declare accessible approaches the winners.

### Identity/status controls retained

- **T02:** official American spelling *Tokenization* versus public British spelling *Tokenisation* and close abstracts support only a candidate edition relationship; no anonymous-author identification or shared-appendix inference.
- **T03:** official *Near Linear Time* versus read public *Linear Time* is not silently normalized into manuscript equality.
- **T05:** same title/abstract does not establish identical official body, appendices or revisions. Numerical claims are tied to public2607.22334v1.
- **GlitchPatch collision:** R L976 keeps `DbzLzs5VL7` local retokenization/public FULL separate from `Rvz6kIZAcg` output-head/shared-adapter, still abstract-only.
- **Compiled Tokenizers:** R L976 keeps withdrawn status at the inherited audit snapshot, notev2 and **2026-11-08 10:45:24.749 UTC note modification**, not a verified withdrawal-event date or scientific falsification.
- **Common17 metadata:** source R3 L65–78 supplies `ICLR.cc/2027/Conference/Submission`, notev2 and5 October2026 UTC modification dates. Notev2 is not PDFv2; public note readers do not certify body availability; cached search is not a full live decision/revision thread.
- **Access histories:** R L952/O L17 correctly distinguish V17/V18 individual403 observations, earlier transport/revocation failures, generic PDF restrictions and representative verification gates. No one common per-file root cause or current network condition is established here. No need to repeat the wall attempts.

## 5. All five independent alternate editions remain separate

| Current R line / carrying card | Incomplete assigned source | Actual independent public FULL declaration | Recheck |
|---|---|---|---|
| L998 /[R04](../03_reading/V01/BR-A01-R04.md), L3 | CVPR2022 formal **PARTIAL** | **2203.07004v2** | PASS. Quote public-v2 tables only; formal table/edition equality still unverified. Not an ICLR2027 completion. |
| L999 /[W0143](../03_reading/V15/W0143.md), L3 | NeurIPS2023 formal **BLOCKED** | **2306.07174v1** | PASS. Public LONGMEM reading does not complete the assigned proceedings bytes or certify equality. Not an ICLR2027 completion. |
| L1000 /[T02](../03_reading/V17/BR-R2-T02.md), L3–5 | Official rIRkUxOleG **BLOCKED** | **2604.16037v1** | PASS. Existing37-page/Appendices A–G reading declaration supersedes acquisition-only history; no official upgrade. |
| L1001 /[T03](../03_reading/V17/BR-R2-T03.md), L3–5 | Official8D7l5sK3YT **BLOCKED** | **2610.19139v1** | PASS. Public stable-prefix theory/implementation claims stay public-edition scoped; title difference/equality gap retained. |
| L1002 /[T05](../03_reading/V17/BR-R2-T05.md), L3–5 | Official Mm5OLOPLT0 **BLOCKED** | **2607.22334v1** | PASS. Actual public conditional-mass/functional-probe evidence remains usable only within its restrictions. |

These are **five alternate edition fields on existing works**, not five additional works, five formal completions, five ICLR bodies or new FULL credits earned by this recheck. The 2009 learned predictive-state paper is a separate foundational completion, not a sixth alternate or recent ICLR result.

Current attributed counts remain **128 tasks;103 FULL/6 PARTIAL/19 BLOCKED assigned editions;108/5/15 some-FULL-source work view**. The50-record official metadata union remains **46 active +3 withdrawn +1 desk-rejected snapshots**, not50 read originals, a simultaneous venue census or acceptance list. **Zero ICLR2027 acceptance decisions are established.** This recheck confirms consistency of the specified identities/count fields; it does not repeat the entire register or audit all128 cards scientifically.

## 6. Partial-coverage and translation contract

The inspected final deliverables continue to separate:

1. **Selected official metadata:** identity and dated submission/status snapshots, not body-supported scientific results or current decisions.
2. **Independently read public editions:** actual source-edition reading declarations and bounded claims, not anonymous manuscript equality or acceptance.
3. **Metadata/abstract-only competitors:** research hypotheses and source-dependent questions, not verified methods, theorems, negative findings, or irrelevant alternatives.
4. **Foundational completions:** PSR2009 and older alternatives are useful evidence, not newly read ICLR2027 papers or substitutes for the17 missing official bodies.
5. **Local correction/recheck work:** source-formula and scope reporting, not comprehensive paper review, proof validity, implementation repair, experimental reproduction or target-host diagnosis.

These boundaries are visible in R L39–45,76,950–954,980–1004; E L17–21/75–77; M L74/89; O L9–17/39/60/99; V L33–44/73–84. A targeted search of the five final files' ICLR/acceptance/comprehensive/identity wording found no contrary claim in this recheck. This is a wording/source-boundary check, not independent scientific validation of every ICLR-adjacent sentence or paper in the report.

**Translation may carry the revised English as partial research results, subject to the following fidelity rules:**

- Keep the main recent heading/limitations explicitly **selected/partial**, never translate them as a complete, exhaustive or comprehensive ICLR2027 survey.
- Carry the **17-body OPEN gate** prominently in the main report and executive limitations. Translate3 public counterparts/14 without alternate as different fields; do not turn either into14 official gaps.
- Preserve the five exact arXiv versions, official forum IDs, candidate relationships, T02/T03 title differences, unknown official revisions, notev2/PDFv2 distinction, status snapshot dates, and unknown withdrawal-event dates.
- Preserve the3 correction scopes: idealized T02 count law versus runtime attempts; printed PSR estimator versus uninspected code; one GLM-Z1-9B/Qwen3.5-2B BPM-JSD probe with128 generations/checkpoint versus separate80/1,799 margins and headline forward-KL results. Keep §4.3/Fig.3/Appendix H.2 intact.
- “FULL” means an existing source-edition reading declaration, not “fully verified,” “fully reproduced,” “accepted,” or “this recheck reviewed the whole paper.” “Correction closed” means the reporting omission is repaired, not the source artifact/question resolved.
- Preserve clean negatives, attacks/proof assumptions, implementation/theory distinctions, teacher/full-cost gaps and target-host nontransfer limits. Do not strengthen a conditional public claim into an official conference finding.
- Translate the current final report/summary/matrix/open-evidence/log, not stale passages copied back from intermediate thematic drafts. Other review lanes and eventual bilingual fidelity checks are not certified by this recency recheck.

The user's partial-results translation permission is now explicit. The prior English reminders not to *presume* acceptance of reduced scope are compatible with this instruction: translation of the bounded available component is allowed; completion of the missing-original component is still not claimed. No author-file edit is required from this recheck merely to restate that permission.

### What remains source-gated versus scientifically unmeasured

| Remaining item | Gate retained |
|---|---|
|17 official bodies, actual versions/appendices and their claims | Legitimately available originals or authorized source provision followed by actual reading. No repeated verification-wall probing, credential bypass or anonymous-author matching. This is **not a prerequisite to translating clearly labeled partial results**. |
|Official/public equality, decisions and exact status-event history | Actual ordinary-access body/history evidence if later needed; otherwise keep unknown. No new network evidence here. |
|T02 sampler implementation; PSR estimator/code; T05 real-BPE/zero-mass/stop/mask/cost details | Source/artifact clarification for stronger claims, not whole-paper condemnation or proof the reported empirical cells are false. |
|Byte-native semantic/exact retention, legal same-state query repair, learning history, complete costs and architecture/host comparisons | Separately scoped scientific measurements and valid artifacts/controls. Literature correction cannot supply these outcomes; no experiment or training authorized. |

## 7. Verification, snapshot, and ownership

**Only authored file:** `docs/research/flued_broad_research_v2/05_review/FINAL_ICLR_RECENCY_RECHECK.md`. All five author files, earlier reviews, source rules/audits, cards, catalog, project guidance and code remain read-only. No network access, source downloads, subagents, installs, model/checkpoint execution, training, commits or pushes.

Read-only structural checks passed:

- 17 unique official IDs in R exactly match O and source R3; all17 R rows retain BLOCKED/Submission snapshot/unknown official-edition fields.
- 5 alternate rows retain exactly2203.07004v2,2306.07174v1,2604.16037v1,2610.19139v1,2607.22334v1 and incomplete assigned targets.
- 167 report direction anchors remain unique, with20/22/20/20/22/19/28/16 totals. This membership check is not167 scientific conclusions or a fresh broad-coverage audit.
- The revised3 P1 locations and §4.3 locator match their named correction contracts; review-file checks cover UTF-8, final newline/trailing whitespace, local links, finding/table counts and unchanged input hashes. Git status and `git diff --check` are inspected before handoff.

| Read-only revised English input | SHA-256 at this recheck |
|---|---|
| REPORT_EN.md | `8a9428deb35fa26eb54d05df6136f99d63af621f5eab31c047718fa1515f88d0` |
| EXECUTIVE_SUMMARY_EN.md | `bbde1489b4537f6c4f6ffc2bdea33c42c2c4002c276af30b69731902f7fccd01` |
| EXPERIMENT_DECISION_MATRIX_EN.md | `f4807a7ec936ad21ea505ab0d475e317f64879879282c48d7c4019fd0acc92b8` |
| OPEN_EVIDENCE_EN.md | `433234712cd25d0274bf8fcca1c5abcb758bdece862dbe9f4bb6d236e90d6d3a` |
| REVISION_LOG_EN.md | `903f6c1d4ae3f0af283f09a3ff820ffe2a1907d940c39cd1cda2c160a1b0cce5` |

The prior review, recent claim rules and source R3 also remained unchanged at their captured hashes. Repository status already contained the untracked research root, unrelated proposal and four bundles; status alone cannot attribute other concurrent writers' files. No task-created scripts, logs, binaries, downloads or test outputs are retained. Software build/pytest does not apply to this documentation-only recheck and was not run.

**Final boundary:** the specified3 P1 reporting omissions and1 citation error are repaired;17/17 missing and5/5 alternate identities pass. **Proceed with the recency component as explicitly partial research results for translation. Keep the17-official-original gate OPEN. Do not convert this local recheck, or the treatment of author/source errors, into comprehensive paper/conference review or overall task completion.**
