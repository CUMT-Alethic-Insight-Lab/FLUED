# A02 — Executed public search and source log

Date: 2026-11-09. Specialist ownership: `docs/research/flued_broad_research_v2/01_discovery/A02/` only. All search terms below are public titles, IDs or mechanism descriptions; no internal files/results were uploaded. No academic data-source API, account, payment, install, training or code from papers was used.

## 1. Local recovery and deduplication actually performed

Read `PLAN.md`, the canonical `FOLLOWUP_DIRECTIONS.md`, and previous `07_scope_recovery/02_STATE_MEMORY/{COVERAGE_AUDIT,SEARCH_LOG,READING_RECOMMENDATIONS}.md`. Inspected the old catalog W0199–W0247 region and relevant W0086/byte aliases, plus byte inventory corrections. Read nine actual evidence cards, not just a catalog's FULL labels: W0229/B06, W0212/B06, W0245/B21, W0061/B04, W0217/B16, W0204/B16, W0214/B16, W0352/B14 and BIW-0108/R08. Those paths, versions and precise reuse limits are in [WORKS_AND_PROBLEMS](WORKS_AND_PROBLEMS.md) and [READING_HANDOFF](READING_HANDOFF.md).

Scoped searches of both main catalog files checked stable IDs/title aliases for 2609.38166, 2611.07552, 2602.04852, 2602.02195, 2610.26834, 2609.36529, HJ8W1Q-0Z, 1606.01164, 2503.14456 and 2407.14207. W0086=2602.04852 was already cataloged and retained as E13; the other nine become local N01–N09, subject to central deduplication. Longhorn was already cited inside W0229's card, hence missing-entity recovery rather than a novel conceptual discovery. The four prior N02-1..4 candidates are P01..P04, not fresh discoveries. No old W/BIW alias was renamed or new global ID assigned.

No claim of scanning every source-card paragraph, every catalog supplement or all six axes. The relevant `docs/` search found no additional `AGENTS.md`.

## 2. Eleven exact WebSearch queries, in execution order

| Query | Public search string | Useful results and disposition |
|---|---|---|
| Q01 | `linear recurrent memory numerical precision quantization long context delta rule stability 2026` | Triadic attention and KronLSTM; original arXiv pages obtained later. Vendor/secondary results not treated as evidence. |
| Q02 | `associative memory correlated patterns unlearning pseudoinverse Storkey 1997 capacity neural networks` | Storkey/pseudoinverse historical leads. Not fetched/read: no historical-capacity claim or added work record made from snippets. |
| Q03 | `2026 state space associative recall curriculum fixed state recurrences Anatomy interference wall` | Previous-audit Anatomy recovered; fixed v1 body then directly inspected. Not counted as new work. |
| Q04 | `2026 nonlinear associative memory test time learning selective erase memory late relevance` | T²Mem robotics lead. Not original-verified, not inventoried as evidence or included in the 26. Search scarcity is not field absence. |
| Q05 | `"linear attention" "precision" "recurrent state" numerical stability` | SPARE, DeltaLog, KalmaNet supplement. SPARE body original inspected and its references led to LeapQuant/rank diagnostics. DeltaLog/KalmaNet not added from snippets. |
| Q06 | `"state space models" "quantization" "state" precision long context` | Quamba and formal-venue leads. Not read: weight/activation quantization must not automatically be called recurrent-state quantization. N01 is the directly relevant source actually pursued. |
| Q07 | `"fast weights" "1992" Schmidhuber learning store memories` | Public original 1992 mirror and Gated Fast Weights ICLR-2018 PDF lead. The latter obtained and original negative results inspected; 1992 full original not obtained/read, no standalone evidence record. |
| Q08 | `"Dense Associative Memory" "pattern recognition" 2016 Krotov Hopfield` | Official NIPS 2016 proceedings metadata/abstract obtained. Recent thermal/finite-size analyses and blogs left as unverified leads, not counted. |
| Q09 | `"ICLR 2027" "memory" "delta" site:openreview.net/forum` | Five highly relevant forum leads, four directly challenge-blocked. Search snippets do not verify venue membership or acceptance. See §5. |
| Q10 | `"RWKV-7" "Expressive" arxiv` | Official 2503.14456v2 author/title/version and abstract obtained. No inference from secondary summaries. |
| Q11 | `"Longhorn" "state space" online learning arxiv` | Official 2407.14207v1 obtained; treated as missing catalog entity related to already-read W0229. |

WebSearch gives a bounded relevance-ranked result set; no pagination/whole-year or exhaustive venue sweep was executed. No counts of all search hits, all 2026 papers or all ICLR submissions are inferred.

## 3. FetchURL attempts: exact URLs and actual outcomes

The following ledger records **42 FetchURL attempts**: 33 returned scholarly page/PDF text, eight returned only OpenReview verification challenges and one returned an OpenReview loading shell. “Returned” does not mean complete reading or an intact mathematical extraction. URLs grouped into a row still correspond to the separate attempts explicitly numbered.

| Attempt | Exact public URL | Outcome and actual use |
|---|---|---|
| F01 | https://openreview.net/forum?id=2XDUbuZOTH | Verification wall; no forum content/status. |
| F02 | https://openreview.net/forum?id=jGFgYdNkmI | Verification wall; no full title/version/status. |
| F03 | https://openreview.net/forum?id=jFQZrrDREJ | Verification wall; no original method evidence. |
| F04 | https://openreview.net/forum?id=QvfwNCiyPg | Verification wall; no complete title/version/status. |
| F05 | https://arxiv.org/html/2611.07552v1 | Original SPARE main text and Appendix A/B returned; inspected main sections and implementation/accounting text. No independent proof/code or graph audit. |
| F06 | https://arxiv.org/html/2609.16183v1 | Long original response saved by tool; targeted §§3.2–10 inspected via Read; identified discussion/result inconsistencies, no complete appendix/figure certification. |
| F07 | https://arxiv.org/abs/2609.38166v1 | LeapQuant metadata/abstract/history, 2026-09-29. |
| F08 | https://arxiv.org/abs/2602.04852v1 | W0086 v1 abstract/history; later versions exist, not read as identical. |
| F09 | https://arxiv.org/abs/2602.02195v1 | State Rank Dynamics metadata/abstract, 2026-02-02. |
| F10 | https://arxiv.org/abs/2610.26834v1 | KronLSTM metadata/abstract/history, 2026-10-19. Not a venue certification. |
| F11 | https://arxiv.org/abs/2609.36529v1 | Triadic attention abstract/history, 2026-09-29. |
| F12 | https://arxiv.org/html/2610.19709v1 | Original Beyond State Capacity text returned; targeted §§3–6, discussion, patch/probe details read. Not all sections/appendices. |
| F13 | https://proceedings.mlr.press/v139/schlag21a.html | Official ICML 2021 metadata/abstract/BibTeX; no PDF-body read. |
| F14 | https://arxiv.org/html/2412.06464v3 | GDN original body returned; §§3.1–3.2 read, remainder only located/search navigation. |
| F15 | https://arxiv.org/html/2508.19029v2 | Revisiting original body returned; §§3–8 read, appendices not read. |
| F16 | https://arxiv.org/abs/2606.26560v1 | EDA author list/abstract/history; metadata includes Xiao Li, unlike HTML extraction. |
| F17 | https://arxiv.org/abs/2605.22791v1 | GDN-2 abstract/history. |
| F18 | https://arxiv.org/abs/2610.38578v1 | Dual DeltaNet abstract/history. |
| F19 | https://arxiv.org/abs/2504.13173v1 | MIRAS abstract/history. |
| F20 | https://arxiv.org/abs/2407.04620v4 | TTT author list/abstract/history, version 2025-08-31. |
| F21 | https://arxiv.org/abs/2501.00663v1 | Titans abstract/history; actual first submission 2024-12-31. |
| F22 | https://arxiv.org/abs/2008.02217v3 | Hopfield Networks abstract/author/history. The abstract's exponential pattern count is not fixed-total-byte storage. |
| F23 | https://proceedings.neurips.cc/paper/2016/hash/eaae339c4d89fc102edd9dbdb6a28915-Abstract.html | Official Dense Associative Memory proceedings abstract; no original full reading. |
| F24 | https://arxiv.org/html/2609.38166v1 | LeapQuant original text; introduction, targeted §3.2/Fig.3 and §4.4 Tables 2–3 inspected; rest not called FULL. |
| F25 | https://arxiv.org/abs/2008.07669v2 | HiPPO abstract/history; prior-audit candidate recovered. |
| F26 | https://arxiv.org/abs/2312.04927v1 | Zoology abstract/history; original full controls still unread. |
| F27 | https://arxiv.org/abs/2603.26554v2 | Spectral-optimizer capacity abstract/history; one-step/multi-step distinction retained. |
| F28 | https://openreview.net/pdf?id=HJ8W1Q-0Z | Original anonymous ICLR-2018 under-review PDF text returned; §§1–6/limitations inspected, numeric table cells/figures not fully recovered. No author identification or final decision verification. |
| F29 | https://arxiv.org/html/2409.16408v2 | Hopfield encoded-representation original body; §§1–3.1 and beginning §3.2 read. Returned excerpt stops early in heteroassociation; no full-read claim. |
| F30 | https://arxiv.org/abs/2611.07552v1 | SPARE history fixes v1 at 2026-11-05, not search display's Nov 6. |
| F31 | https://arxiv.org/abs/2503.14456v2 | RWKV-7 abstract/author/version history. |
| F32 | https://arxiv.org/abs/2407.14207v1 | Longhorn abstract/history; later v5 exists but not read. |
| F33 | https://openreview.net/group?id=ICLR.cc/2027/Conference | Only “OpenReview / Login / Loading” shell; not venue-paper coverage. |
| F34 | https://arxiv.org/abs/2508.19029v2 | Revisiting version/history reconfirmed after body inspection. |
| F35 | https://arxiv.org/abs/2610.19709v1 | Beyond State Capacity version/history reconfirmed, v1 2026-10-14. |
| F36 | https://openreview.net/pdf?id=2XDUbuZOTH | One legitimate alternative official PDF route for F01, also verification-wall blocked. Stop, no circumvention. |
| F37 | https://arxiv.org/html/2610.26834v1 | Large KronLSTM body obtained but only introduction/Fig.1 inspected; no claim to read the long theorem appendices. |
| F38 | https://arxiv.org/html/2606.26560v1 | EDA body obtained; only introduction inspected, not equation/experimental full verification. |
| F39 | https://arxiv.org/abs/2609.16183v1 | Anatomy official fixed-v1 abstract/history reconfirmed after checking inconsistencies. |
| F40 | https://openreview.net/pdf?id=jGFgYdNkmI | One alternative official PDF route after F02, also verification-wall blocked. |
| F41 | https://openreview.net/pdf?id=jFQZrrDREJ | One alternative official PDF route after F03, also verification-wall blocked. |
| F42 | https://openreview.net/pdf?id=QvfwNCiyPg | One alternative official PDF route after F04, also verification-wall blocked. |

Some long FetchURL responses were auto-saved in ordinary session tool-result text storage. Read/Grep was used only to navigate and inspect those returned public texts. No deliberate local PDF download, script or research-source cache was created; future allowed PDF destinations are explicit in the handoff.

## 4. Built-in browser checks and retries

Used Kimi Code Desktop's built-in browser, not a personal Chrome/Edge session or WebBridge. Initial create-tab request for the official ICLR group returned `TAB_NOT_ACTIVE`; one state recovery found background research tabs. A temporary group/forum research tab (`panel-tab-294`) was selected for this check. Two bounded document snapshots of the group showed only a persistent loading shell; title alone said “ICLR 2027 Conference | OpenReview” and did not expose paper membership or decisions. Navigating that tab to `forum?id=2XDUbuZOTH` reached the official browser-verification challenge. The research tab was closed. No CAPTCHA/login/account intervention or authentication workaround was attempted.

For the key forum, FetchURL forum, one browser route and one alternative official PDF route all failed to expose content; do not retry indefinitely. Each of the other three directly attempted forums was retried once through its official PDF URL (F40–F42), also returning a challenge. A dedicated venue owner can reassess availability later. This is a coverage limitation, not a finding that their mechanisms fail or that the venue has no relevant papers.

## 5. ICLR 2027 exact status boundary

Query Q09 yielded these official public forum URLs:

- https://openreview.net/forum?id=2XDUbuZOTH — indexed title *Kronecker Delta Rule for Long Context Linear Attention*; forum content unverified. Public arXiv source was independently read without building an author crosswalk.
- https://openreview.net/forum?id=jFQZrrDREJ — indexed *DeltaTTT: Layerwise Optimization for Nonlinear Recurrent Memory*; blocked.
- https://openreview.net/forum?id=jGFgYdNkmI — indexed title truncates *When Does Momentum Help Online Associative Memory …*; blocked.
- https://openreview.net/forum?id=QvfwNCiyPg — indexed title truncates *CHARTA: A Recurrent Language Model with Routed …*; blocked.
- https://openreview.net/forum?id=JvQYIoQxQ0 — indexed title truncates *Fast Residual Memory for Test-Time Training of Latent …*; search lead only, not fetched.

**Zero fully verified ICLR 2027 group+forum+version/status records in this pass.** Search snippets saying “Conference Submission” do not satisfy the contract. None is called accepted, and no anonymous identity was resolved. Formal coverage remains a handoff to the venue stream; no OpenReview API pagination or conference census was performed.

## 6. Source-quality corrections carried forward

- **Anatomy same-version internal disagreement:** §§4/6/7 expanded controls qualify or negate earlier decay, length-boundary and directional claims still present in §§9–10. Recheck the precise results and artifacts before synthesis; do not smooth contradictions into certainty.
- **Precision versus rank:** LeapQuant reduces rounding frequency using extra high-precision storage; SPARE reduces state dimension but keeps FP32. Neither is merely a “smaller state” result.
- **Search date versus version date:** SPARE official v1 Nov 5, not search display Nov 6. Titans actual first submission Dec 31, 2024, not inferred from 2501.
- **Author extraction:** EDA abstract metadata includes its first author; HTML extraction omits the first name. No anonymous forum was identified using this discrepancy.
- **Titles/versions:** W0086 title changed by later version; RAM-Net W0214's actual reused v2 card title takes precedence over the old catalog's early title. No duplicate work is created from title changes.
- **Full-read scope:** nine existing cards reused, no new FULL papers registered. Original HTML availability is not a reading-depth certificate. The anonymous 2018 PDF has unrecovered table/graph content and is P, not FULL.

## 7. Verification and deliverable boundary

Only these four English Markdown files are authored in A02: `COVERAGE_AND_FINDINGS.md`, `SEARCH_LOG.md`, `WORKS_AND_PROBLEMS.md`, `READING_HANDOFF.md`. No catalog, old card, previous audit, production code, terminology registry, CURRENT_STATE, experiment or report-synthesis file is edited. No subagents, training, paid access, dependency installation or git mutation.

At session start the research trees and several unrelated bundles were already untracked. They are not ours to clean up. Executed Python static checks **PASS**: exactly four UTF-8 nonempty files, all 30 relative Markdown links resolve, work headings total 26 (13 E / 4 P / 9 N), queue priorities are contiguous 1–15, query rows 11 and fetch ledger contiguous F01–F42. Scoped `git status --short --untracked-files=all -- docs/research/flued_broad_research_v2/01_discovery/A02` lists exactly the four intended Markdown files, with no generated cache, script, log or PDF in A02. Repository-wide status changed outside A02 during parallel work; no outside changes were authored or cleaned up here. Markdown-only discovery did not run model tests or a build. These checks do not reproduce paper experiments or certify proofs.
