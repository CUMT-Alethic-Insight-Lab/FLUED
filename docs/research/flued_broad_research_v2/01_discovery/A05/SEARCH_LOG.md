# A05 — Executed search, recovery, deduplication, and access log

Date: 2026-11-09. Scope: learning trajectories, early writer/reader coadaptation, initialization, feature competition, aligned-gradient negative transfer, auxiliary reconstruction, curvature, mechanism persistence, curricula and freeze schedules. This is executed discovery, not merely a plan.

## 1. Tool/data boundary and provenance

- Read [PLAN](../../PLAN.md), the canonical [FOLLOWUP_DIRECTIONS](../../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md), and all three previous `05_LEARNING_DYNAMICS` audit/search/recommendation files. Read actual relevant original cards; consult both canonical catalogs rather than repeating the old audit's novelty claim.
- External tools used: public **WebSearch**, **FetchURL**, and the **Kimi Code built-in browser**. No academic-specialist data-source tool/API was invoked, so no academic-source skill/API schema was required. No user Chrome/Edge session was used.
- Queries sent only public paper names, public IDs, mechanism terms, or venue names. No internal document, code, path, experiment number, result, or project identifier was uploaded. No paid access, installation, source-code execution, training, subagent, commit, or production edit.
- Browser access had an ordinary connection error, a shared-control error, and an OpenReview shell. These are logged separately from scientific findings. No CAPTCHA/authentication bypass attempted. Direct public FetchURL was used for the requested discovery as well; it is not claimed that failed browser pages were successfully read.
- No PDFs were manually downloaded. FetchURL returned parsed public PDF text; automatic tool response caches are not project evidence artifacts and not cited as permanent reading cards. Any later intentional PDF download must use an explicit path in the assigned project folder, never `/tmp` or Downloads.

## 2. Exact public search queries and outcomes

There were **18 WebSearch attempts: 16 returned search results, two returned HTTP 429**. Search results are discovery leads, not full reading or venue verification. Result lists were bounded by the tool; no offset/pagination interface was used and no claim of full query-result enumeration is made.

| Query | Exact submitted text | Outcome / scientific action |
|---|---|---|
| Q01 | `2025 2026 "learning dynamics" "in-context" "competition"` | Located 2412.01003, 2412.00104 and 2610.01054. Kept the first two after primary-source checks; excluded Task Operators from substantive training-trajectory additions. |
| Q02 | `"gradient" "aligned" "negative transfer" auxiliary learning curvature` | Mostly tangential model-merging/RL/domain hits. No result promoted merely by matching words. |
| Q03 | `"2026" "posterior collapse" "dynamics"` | Located AISTATS 2024 linear-VAE original, λ-VAE, GenFirst and unrelated bio/secondary material. Took only direct relevant originals; no biology experiment information used. |
| Q04 | `"2025" "2026" "curriculum" "induction heads"` | No precise curriculum mechanism selected; many unrelated or secondary hits. Do not infer curricula are exhausted. |
| Q05 | `"ForkMerge" "gradient" "consistent"` | Primary arXiv v3 and official NeurIPS 2023 PDF; checked §3.1 one-step/validation interpretation. |
| Q06 | `"2026" "learning dynamics" "encoder" "decoder" collapse` | Located 2605.06870 warm-up and λ-VAE; retained after original HTML/version checks. Unrelated software-decoder security hits excluded. |
| Q07 | `site:openreview.net "ICLR 2027" "learning dynamics"` | Search-indexed anonymous forum leads: rare counterexamples, state tracking, masked diffusion, mode dynamics, world models. Only rare-counterexample forum requested; other titles not treated as coverage. |
| Q08 | `site:openreview.net "ICLR 2027" "gradient starvation"` | PDF snippets led to anti-collapse and local-sufficiency forum requests. Official access blocked; not accepted or verified-submission records. |
| Q09 | `"train" "warm-starting" neural networks 2020 ash adams` | Found DASH/NeurIPS 2024 and background Ash–Adams citations. Kept DASH only after official PDF; did not create an unverified Ash–Adams work record. |
| Q10 | `"Dormant Neuron" "ReDo" 2023` | Found correct arXiv 2302.12902 and ICML 2023 PMLR original; used official abstract. |
| Q11 | `"Curriculum Learning" Bengio 2009 pdf` | HTTP 429. Not used as evidence, no invented result or source verification. Mechanism-specific schedules were already sourced; original general curriculum classic remains a follow-up if needed. |
| Q12 | `"Universal Language Model Fine-tuning" "gradual unfreezing"` | HTTP 429. One later legitimate retry Q14 returned results. |
| Q13 | `"2608.29335"` | Verified exact GenFirst title and primary PDF identity; not a venue claim. |
| Q14 | `"Universal Language Model Fine-tuning" "gradual unfreezing"` | Successful retry of Q12 after other work; official ACL PDF independently read for schedules and counterexample. |
| Q15 | `"1312.6120" "ICLR"` | Found Oxford institutional ICLR 2014 association. Primary arXiv identity/version checked; full institutional record not fetched, venue not independently audited. |
| Q16 | `"Directions of Curvature as an Explanation for Loss of Plasticity"` | Verified original v2/v3/v4 title variation and public arXiv originals. No final acceptance assumption. |
| Q17 | `"Competition Dynamics Shape Algorithmic Phases" "ICML"` | Ambiguous associations and citations, not reliable acceptance verification. Retain as versioned preprint. |
| Q18 | `"Differential learning kinetics" "2025"` | Located official ICLR 2025 proceedings; fetched it. No assumption about ICLR 2027. |

The first attempted built-in-browser query was `learning dynamics gradient starvation auxiliary reconstruction in context learning transience 2025 2026`. It failed with `ERR_CONNECTION_CLOSED`; it is **not** one of the 16 successful WebSearch results.

## 3. Original-source FetchURL requests: what was actually available

38 FetchURL requests are listed below. “HTML” may return a long bounded preview plus a tool cache; that is not proof of full reading. Scientific scope is recorded individually in [WORKS_AND_PROBLEMS](WORKS_AND_PROBLEMS.md).

| Request | Exact public URL | Returned content / used scope |
|---|---|---|
| F01 | https://arxiv.org/html/2610.01054v1 | Network fetch failure. One legitimate alternate route F09 succeeded; work excluded on scope, not access. |
| F02 | https://proceedings.mlr.press/v238/ichikawa24a.html | Official AISTATS 2024 metadata/abstract, author list and proceedings/PDF anchor. A05-N01, A only. |
| F03 | https://arxiv.org/abs/2608.29335 | GenFirst abstract and v1 2026-08-29 history. N03, A; original PDF later supplied method sections. |
| F04 | https://openreview.net/group?id=ICLR.cc/2027/Conference | Login/Loading shell, not conference inventory or authenticated data. |
| F05 | https://openreview.net/forum?id=3us1m0de0C | Verification challenge, no paper/status read. A05-L01 blocked. |
| F06 | https://openreview.net/forum?id=ndfEYtpRRb | Verification challenge, no exact full title/revision/status read. A05-L02 blocked. |
| F07 | https://openreview.net/forum?id=aez0aKWAOB | Verification challenge, no paper/status read. A05-L03 blocked. |
| F08 | https://arxiv.org/abs/2605.06870 | Abstract and version history through v3 2026-09-27. N02. |
| F09 | https://arxiv.org/abs/2610.01054v1 | Task Operators abstract/history success after F01 failure. Mechanism concerns compressing inference-time contextual transformations, not pretraining acquisition; excluded from the retained training inventory. |
| F10 | https://arxiv.org/html/2607.05531v1 | Long original HTML. Read abstract, §3.1–3.2/proposition conditions; equations raise review questions. N04, P, not FULL. |
| F11 | https://arxiv.org/html/2301.12618v3 | Long original HTML. Read §3 definitions/§3.1–3.2/Fig.2 caption via exact excerpts; LD-N04, P. |
| F12 | https://arxiv.org/html/2605.06870v3 | Long original HTML. Read §3.3 theorem statement, §§4–5, captions, Appendix B/settings and β=0 excerpt via direct text/search. N02, P. |
| F13 | https://arxiv.org/html/2608.29335v1 | Network fetch failure. Legitimate public PDF F31 succeeded, no further retries. |
| F14 | https://arxiv.org/abs/2412.01003 | Original abstract and v1–v4 dates. N05, later HTML excerpt reading. |
| F15 | https://arxiv.org/abs/2412.00104 | Original abstract and v1/v2 dates. N06, later HTML/proceedings. |
| F16 | https://aclanthology.org/P18-1031/ | ACL official abstract; no claim of full method from abstract. N07; PDF F30 later. |
| F17 | https://proceedings.mlr.press/v202/sokar23a.html | ICML 2023 formal metadata/abstract, correct 2302.12902 alias from search. N08, A only. |
| F18 | https://arxiv.org/abs/2410.23495 | DASH abstract/history v1/v2. N09; official PDF F34 later. |
| F19 | https://arxiv.org/abs/1312.6120 | Original exact-linear-dynamics abstract/history through v3. N10, A only. |
| F20 | https://arxiv.org/html/2503.05631v2 | Long HTML, includes style-warning extraction artifacts. Read Fig.1/abstract/introduction and note late appendix MLP resurgence excerpt; no full re-reading. LD-N05, recovered P. |
| F21 | https://arxiv.org/html/2409.14623v2 | Long original HTML, read abstract/introduction; previous assumption-level recovery retained. LD-N07, not all 200k+ characters read. |
| F22 | https://arxiv.org/html/1901.05534v2 | Long original HTML, fresh abstract/introduction; previous selected-section P preserved, not upgraded. LD-N01/BIW-0096. |
| F23 | https://arxiv.org/html/2610.19113v1 | Long original HTML, fresh abstract/introduction/Fig.1 and release/change-plan paragraph; recovered selected-section P retained. External supplement not fully read. |
| F24 | https://arxiv.org/abs/1911.02469v1 | Original linear-VAE abstract/version. LD-N08; prior P not counted as fresh FULL. |
| F25 | https://arxiv.org/abs/1812.07956v5 | Lazy-training original abstract/version history. LD-N09, A only. |
| F26 | https://arxiv.org/abs/2311.08360v3 | Transient ICL original abstract/history. LD-N10, A only; paired with later LD-N05 revision of mechanism interpretation. |
| F27 | https://iclr.cc/virtual/2026/poster/10008648 | Official residual-feature-integration abstract. LD-N11, A only, guarantee restricted by target distribution class/logarithmic factors. |
| F28 | https://proceedings.mlr.press/v38/lee15a.html | Deeply-Supervised Nets formal AISTATS metadata/abstract. LD-N02; recovered P not upgraded. |
| F29 | https://arxiv.org/abs/1711.08856v3 | Critical-period title/abstract/history including recoverable high-level perturbations. LD-N03. |
| F30 | https://aclanthology.org/P18-1031.pdf | Parsed official proceedings PDF; read §§3.2–3.3/5, freeze/rate controls and Table 7 textual interpretation. N07, P; missing table cells not fabricated. |
| F31 | https://arxiv.org/pdf/2608.29335v1 | Parsed original PDF after F13 failure. Read §§3–5.2; formula/duplication defects; returned text only extends into later results, not full appendices. N03, P. |
| F32 | https://arxiv.org/html/2412.00104v2 | Long HTML. Read §§3.2–3.4 by excerpt plus abstract/appendix captions; additive ansatz/large-D limits. N06, P. |
| F33 | https://arxiv.org/html/2412.01003v4 | Long HTML. Read abstract/introduction and late optimization/diversity emergence discussion; main experiments not fully read. N05, limited P. |
| F34 | https://proceedings.neurips.cc/paper_files/paper/2024/file/4c5ce1fc8895076f49935951a630be5c-Paper-Conference.pdf | Parsed formal DASH PDF. Read §§2–5 and abstract; appendices incomplete/unread. N09, P; formal title confirmed. |
| F35 | https://arxiv.org/abs/2312.00246 | Original curvature abstract/history through v4. Abstract-page title differs from pinned HTML. N11. |
| F36 | https://arxiv.org/html/2312.00246v2 | Long original HTML. Read §§3–4/figures' captions, empirical-Fisher approximation and rank counterexamples. N11, P; formal publication unknown. |
| F37 | https://arxiv.org/abs/2607.05531v1 | λ-VAE original abstract and v1 2026-07-06 history; no venue verified. |
| F38 | https://proceedings.iclr.cc/paper_files/paper/2025/hash/187f9ba4cd5a59477305ac712282a1cd-Abstract-Conference.html | Official ICLR 2025 abstract record for Differential learning kinetics. N06; version-to-proceedings diff unperformed. |

Summary of access outcomes: two network fetch failures (F01/F13), both recovered through one alternate public route; four non-content OpenReview responses (F04–F07); 32 substantive public content responses, many only abstract/metadata. No inaccessible source was silently labeled full. Public official PDF URLs found through search but not themselves requested (e.g. ForkMerge's NeurIPS PDF) are supplementary identity anchors, not claimed new reading.

## 4. Built-in-browser operations and limitations

1. Created a background research search tab with the public query above; operation returned `NAVIGATION_FAILED / ERR_CONNECTION_CLOSED`.
2. Requested a background tab for `https://openreview.net/group?id=ICLR.cc/2027/Conference`; operation returned `TAB_NOT_ACTIVE / Browser control changed`.
3. Read browser state to recover actual loaded tabs rather than retrying a control mutation blindly. A group-matching loaded tab (`panel-tab-288`) existed.
4. Read its document DOM text: `OpenReview.net`, `Login`, `Loading`, footer; `scanTruncated=false`, `truncated=false`, no cursor. This confirms a loaded shell, **not** paper inventory/venue status.

No tab activation/switching, unrelated-tab modification, user-session login or CAPTCHA interaction followed. The new research tabs may remain; no successful close is claimed. There was no browser user-takeover event. Shared-control failure is a tool-control limitation, not an access refusal by the paper's authors.

For the three individual forums, ordinary FetchURL hit a verification challenge. No credential route was available or authorized here; access was stopped rather than cycling mirrors, automating a challenge or assuming PDF snippets prove status. Official group/forum revision/decision verification remains for a legitimate accessible route, not a claimed completed task. The inventory explicitly marks these leads blocked.

## 5. Recovery, deduplication and card audit

### 5.1 Exact sources used

- Old `02_catalog/CATALOG.md`, matching W rows; previous `05_LEARNING_DYNAMICS` audit/recommendations/search log.
- Byte `02_inventory/WORK_CATALOG.md`, matching title/ID entries and alias corrections; relevant `03_reading` cards rather than inferred FULL from a global count.
- Actual W cards read: `B16/W0328`, `W0331`, `W0333`, `W0334`, `W0336`, `W0337`; `B24/W0023`, `W0038`, `W0048`; `B14/W0366`.
- Actual byte cards read: `R10/BIW-0113` retained for learning onset/interface access; `R07/BIW-0114` checked but excluded from training-trajectory support.
- A speculative request to `03_reading/R04/BIW-0029.md` returned missing; exact glob for BIW-0029 found no card. No evidence or FULL state was inferred. Existing aliases were then checked directly in the catalog instead of guessing card locations.

### 5.2 Dedup keys and findings

Exact ID/title searches against both catalogs included:

`2608.29335 | 2605.06870 | 2607.05531 | ichikawa24 | 2412.01003 | 2412.00104 | Curriculum Learning | 1801.06146 | 2302.12902 | 2410.23495 | 1312.6120 | 1711.08856 | 2301.12618 | 2503.05631 | 2610.19113 | 2409.14623 | 1911.02469 | 1812.07956 | 2311.08360 | 2505.11771 | 1409.5185`.

Additional title/ID searches over catalog directories covered `2312.00246`, `Curvature explains`, `GenFirst`, `DASH`, `ULMFiT`, and `Exact solutions to`. These are finite searches, not semantic proof that no alias exists anywhere.

- **11 prior recovery works retained with LD-N aliases**, not new discoveries. LD-N01 has existing **BIW-0096** selected-primary/recovery status. It is not new to both corpora.
- **11 additional work records A05-N01–11** were not found under the tested keys in the canonical catalogs. Their scope-relevance is substantial, but novelty is local and provisional pending catalog-owner merge.
- **10 W scoped-FULL reuses**, plus the separate **BIW-0113 FULL reuse**, do not increase reading-completion counts. Alias confirmation: W0328=BIW-0022, W0331=BIW-0023, W0023=BIW-0018, W0038=BIW-0020, W0366=BIW-0037.
- **Seven existing catalog-unread W references** are explicitly labeled existing A/unread, not novel candidates. W0338's January 2026 revision is already in the prior corpus.
- **Three blocked ICLR 2027 leads** are not counted among the 22 verified/recovered work records and cannot support scientific claims.
- New FULL readings: **0**; code reproduction: **0**; local checkpoint evaluations: **0**; new training experiments: **0**.

### 5.3 Actual exclusions and unresolved coverage

- **Capturing In-Context Learning Dynamics with Task Operators, 2610.01054v1**: accessed original abstract after HTML failure; “dynamics” here primarily concerns replaying inference-time contextual transformations. Excluded from retained acquisition-history works. Does not disprove its utility for a different axis.
- General curriculum classic query Q11 failed; no source was fabricated. Current queue instead contains mechanism-specific schedule contrasts and an original freeze-schedule study. General curriculum theory and LM-scale deep supervision remain targeted expansion opportunities.
- ReDo is A only and not evidence that dormant-unit recycling fixes stationary LM plasticity; DASH/curvature counterexamples are preserved.
- λ-VAE is retained with explicit mathematical reservations, not endorsed as a unified theory.
- No evidence directly establishes that the local two objectives stay aligned throughout training while jointly promoting the same bypass. ForkMerge supplies a local/validation counterexample, not that stronger proposition.
- No complete venue enumeration, official ICLR 2027 revision/decision verification, optimizer-noise/momentum survey, full paper/code audit, or field-exhaustion claim.

## 6. Artifact verification

Only the four requested Markdown files are owned by this stream, under `01_discovery/A05/`. Executed read-only Python validation passed: exactly four UTF-8 artifacts, zero replacement characters, 22 ordered unique LD/A05 retained-work IDs with all six required descriptive fields, 15 ordered queue entries, 18 search rows, 38 fetch rows, and zero broken local Markdown file links. `git status --short --untracked-files=all -- docs/research/flued_broad_research_v2/01_discovery/A05` lists exactly these four new Markdown files; no task-created script/log/PDF/test output requires cleanup. These checks do not constitute scientific replication. No project test/build was run for this documentation-only discovery deliverable.
