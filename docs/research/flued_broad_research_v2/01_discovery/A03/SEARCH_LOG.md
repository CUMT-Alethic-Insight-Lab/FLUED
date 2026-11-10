# A03 — Public discovery and source-verification log

Date: 2026-11-09. Scope: native query/readout, K/V separation, read/write alignment, conditioning/normalization/rank/gates, slot/head independence, cross-layer writes and one-step/iterative reads. Public search terms only. No internal files/content were uploaded or used as external search queries.

## 1. Local evidence inspected and provenance

Read the v2 [PLAN.md](../../PLAN.md), canonical [FOLLOWUP_DIRECTIONS.md](../../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md), and the previous A03 [coverage audit](../../../flued_multigranularity_survey_20261108/07_scope_recovery/03_ADDRESS_READOUT/COVERAGE_AUDIT.md), [search log](../../../flued_multigranularity_survey_20261108/07_scope_recovery/03_ADDRESS_READOUT/SEARCH_LOG.md) and [reading recommendations](../../../flued_multigranularity_survey_20261108/07_scope_recovery/03_ADDRESS_READOUT/READING_RECOMMENDATIONS.md).

Used dedicated Glob/Grep/Read for both catalogs and actual cards, not a re-audit of every catalog row. Stable-ID checks covered the new discovery candidates; existing IDs retained include W0086, W0100, W0219, W0203 and W0240. The byte inventory exposed **BIW-0117 Perceiver IO**, whose actual full card was read; it must not be treated as a new unread paper just because the older A03 audit had not seen it.

Actual reused full cards read: W0229, W0212, W0214, W0204, W0210, W0237, W0287, W0289, W0197, W0174, W0092 and BIW-0117. Their declared source-specific scopes remain inherited, not newly certified. Full links, versions and restrictions are in [WORKS_AND_PROBLEMS.md](WORKS_AND_PROBLEMS.md#iii-actual-full-card-reuse-ledger--no-recount).

No applicable nested AGENTS.md was found under `docs/` by the dedicated glob check. Initial git status already had the two earlier survey roots, the broad-v2 root, another research Markdown and bundle files untracked. None of those preexisting artifacts was removed or edited. Ownership here is only `01_discovery/A03/`.

## 2. Actual external search queries — 13

Tool: built-in WebSearch for Q01–Q13. Only the returned bounded result list was examined; there was no search-engine pagination, systematic date-filter census or guarantee of all indexed works. Search snippets are discovery leads, never substitutes for original text or official venue state. Metadata dates from snippets were discarded where original history/Atom was available.

| Query | Exact public query | Useful leads / exclusions |
|---|---|---|
| Q01 | `linear attention native query key alignment 2026 memory retrieval query learning` | How Linear Attention Remembers; Alignment Attention. Continued to original arXiv. 3D reconstruction search hit excluded from native language-memory mechanism inventory |
| Q02 | `2026 attention query key normalization rank collapse gating memory retrieval` | Low-Rank Key Value Attention; future cross-model handoff and video-state leads appeared. Cross-host handoff left to composition stream, not imported from snippet |
| Q03 | `2026 key value separate compression asymmetric low rank attention AsymKV` | DynaCalKV; Cui/Xu merging AsymKV; distinct Tao/Yu/Zhou quantization AsymKV; official NeurIPS poster. Aggregator conflation of two AsymKV papers not accepted |
| Q04 | `2026 cross layer shared KV independent query writes memory attention` | GateSight, CLA-related pointers, existing Attention Residuals. Blogs used only as leads, not mechanistic evidence |
| Q05 | `2026 iterative retrieval associative memory query refinement Hopfield memory language models` | Vision Hopfield/Adaptive Hopfield leads; not admitted from snippet. Filled actual gap with original Hopfield and MemN2N reads instead of a list of unverified recent titles |
| Q06 | `site:openreview.net "ICLR 2027" "query" "memory"` | Official group link and agent-memory forum/PDF candidates. Most hits are higher-level episodic-agent memory, not native recurrent readout; not expanded simply for venue count |
| Q07 | `"Thin Keys, Full Values"` | 2603.04427 v2/v3 and latest-PDF pointers; fixed v3 original fetched, latest v4 noted but not read |
| Q08 | `"Query-Key Normalization" "2020"` | 2010.04245 and Findings official record. Later QKNorm variants not needed before recovering original scale ablation |
| Q09 | `"Gated Attention for Large Language Models"` | 2505.06708; author repository says NeurIPS2025 oral, not independently upgraded to official venue status here |
| Q10 | `"Alignment Attention by Matching Key and Query Distributions"` | 2110.12567 and NeurIPS proceedings PDF pointer; original HTML/Atom used for methods and identity |
| Q11 | `site:openreview.net/forum "ICLR 2027" "linear attention" "query"` | Mass-Aware Fusion of Sparse and Low-rank Attention; Representative Attention for Vision Transformers. Official forum fetch attempted for the former and blocked by verification |
| Q12 | `"GQA: Training Generalized Multi-Query Transformer Models"` | 2305.13245; EMNLP 2023 official page. Original explicitly contradicts no-post-training-conversion claim found in Thin Keys |
| Q13 | `"End-To-End Memory Networks" NeurIPS 2015` | 1503.08895 and original NIPS 2015 proceedings; multiple-hop query and linear-start/init controls recovered |

No academic data-source plugin was used, so there was no scholarly API/skill interface to initialize. Public arXiv Atom is fetched as an official HTTP source, not a paid scholarly service. No external embedding or source-code upload, browser-extension skill, installed scraping framework, paid access or code execution was used.

## 3. FetchURL request ledger — all 32 calls

“M/P” labels below describe what was actually read, not what happened to be returned. Large HTML may be completely fetched but only selected passages examined; it remains P. Where output exceeded tool limits, dedicated Read/Grep was used on the automatically retained text for the listed sections. No manual PDF download occurred.

| Request | Exact URL | Outcome and actual scope |
|---|---|---|
| F01 | https://arxiv.org/html/2609.33093v1 | Success, large text; D20. Read §§2.3–4.2, discussion/limitations and targeted prose-pilot conclusion; not whole appendices |
| F02 | https://arxiv.org/html/2601.11471v1 | Success, large text; D17 initial v1. Targeted method/head-operator analysis §6.3; later v3 separately fetched, same work |
| F03 | https://arxiv.org/html/2607.24331v1 | Success; D18. Read method §§III-B–D, setup and failure/LongBench discussion; tables not all extracted, P |
| F04 | https://arxiv.org/html/2610.14754v1 | Success after slow response, large text; D21. Targeted §§2–4 utility/labels/predictors, selected experiment/cost passages; P |
| F05 | https://aclanthology.org/2025.coling-main.158/ | Success; D16 formal metadata/abstract only, M |
| F06 | https://openreview.net/forum?id=fsYcvdtKHd | Verification challenge, not paper/forum content. Do not claim submission/status/acceptance verified |
| F07 | https://arxiv.org/html/2603.04427v3 | Success; D19. Read §§2.1–2.3, §3.1/3.4, §§8.1–8.4, limitations and selected reasoning/repair discussion; P |
| F08 | https://aclanthology.org/2020.findings-emnlp.379/ | Success; D13 official abstract/record, not full reading. Original methods fetched later |
| F09 | https://arxiv.org/html/2110.12567v1 | Success, large text; D14. Read §2.3 alignment methods, selected experiment descriptions; P |
| F10 | https://arxiv.org/html/2505.06708v1 | Success, large text; D15. Read §§1–2.2, Table 1/§3.2.1 and selected appendix discussion; P |
| F11 | https://arxiv.org/html/1607.00036v2 | Success, extraction ends at §6.4; D02. Read §§2–4.3, §§6.1–6.3/Table 1. Later tasks unread |
| F12 | https://arxiv.org/html/2506.05410v2 | Success, large text; D03. Read §§3.1–3.3, §4.6 description; §3.2 equations rechecked with dedicated Read |
| F13 | https://arxiv.org/html/2405.12981v1 | Success, large text; D04. §2.1–2.3 and overview, not complete experiments |
| F14 | https://arxiv.org/abs/2602.04852v3 | Success; D07/W0086 original abstract/version history only |
| F15 | https://arxiv.org/abs/2610.38578v1 | Success; D08/W0203 original abstract/history only |
| F16 | https://export.arxiv.org/api/query?id_list=2609.33093,2601.11471,2607.24331,2610.14754,2603.04427,2110.12567,2505.06708&max_results=7 | Success; all 7 requested entries, start=0, totalResults=7. Metadata only; latest LRKV v3 and Thin Keys v4 detected |
| F17 | https://openreview.net/group?id=ICLR.cc/2027/Conference | Loading/login shell, not a conference listing. No venue coverage inference |
| F18 | https://arxiv.org/html/2008.02217v3 | Success, very large text; D09/W0240. Read §2 equations (1)–(10), Theorems 1–5 and basin/averaging discussion; proofs/rest unread |
| F19 | https://arxiv.org/html/2006.15055v2 | Network fetch failure; Slot Attention original unavailable through this route |
| F20 | https://arxiv.org/html/1503.08895v5 | Success; D11. Read §§2.1–2.2, §§4.1–4.4/Table 1, §5's query/training details and limitations; not all appendix/figure/table evidence |
| F21 | https://arxiv.org/html/2305.13245v3 | Success; D12. Read §§2–3.3, limitations and Appendix A. Native head sharing, conversion and adaptation sweep verified; not every figure value extracted |
| F22 | https://arxiv.org/html/2601.07832v2 | Success, large text; D06/W0219. Metadata/method §4.1–4.2 recovered with prior audit; causal appendix/full experiments not completed |
| F23 | https://aclanthology.org/2022.emnlp-main.473/ | Success; D05 abstract and official bibliography only |
| F24 | https://neurips.cc/virtual/2025/poster/117046 | Success, official poster abstract; confirms D03 venue entry, not another reading or a second work |
| F25 | https://arxiv.org/html/2006.15055v2 | One same-URL retry, network failure again. No further HTML retries; Atom F30 supplies abstract identity only |
| F26 | https://arxiv.org/html/1410.5401v2 | Success; D01 §§3.1–3.4, §4.1 and part §4.2. Response ends during repeat-copy material, not FULL |
| F27 | https://arxiv.org/html/2010.04245v1 | Success; D13 original §§2–4 and Appendix C discussion read. All tables/figures not independently audited |
| F28 | https://aclanthology.org/2023.emnlp-main.298/ | Success; D12 official abstract/record; no new separate work |
| F29 | https://proceedings.neurips.cc/paper/5846-end-to-end-memory-networks | Success; D11 original proceedings entry/abstract, not a second paper |
| F30 | https://export.arxiv.org/api/query?id_list=2602.04852,2610.38578,2601.07832,1607.00036,1410.5401,2006.15055,2008.02217,1503.08895,2405.12981&max_results=9 | Success; all 9 requested entries, start=0, totalResults=9. Full author/version metadata, no original method proof |
| F31 | https://arxiv.org/html/2601.11471v3 | Success, large text; D17 v3 method/§4.3 operator/compensation and cost clarification targeted. Not whole paper; v1/v3 claims not spliced |
| F32 | https://arxiv.org/abs/2603.04427v3 | Success; version/date history confirms v3 2026-03-18 and later v4 03-28. v4 body not read |

**Accounting:** 32 requests; two network failures (same Slot Attention HTML twice), two successful HTTP/text responses that are unusable as scholarly evidence (OpenReview challenge/loading shell), and 28 substantive source responses. This is a request count, not 28 papers or full reads. Twenty-one D records are backed by original metadata/text; twelve R records reuse actual full cards without new source fetching/counts.

## 4. Built-in Desktop browser actions and limit

User required the Desktop built-in browser for web/browser tasks; no Chrome/Edge extension or personal logged-in browser was used.

1. `browser.create_tab` requested the official group `https://openreview.net/group?id=ICLR.cc/2027/Conference`. It returned `TAB_NOT_ACTIVE` / “Browser control changed.” The operation did not yield a reliable new owned tab handle, so the same action was not blindly repeated.
2. `browser.get_state` recovered available tab state. Existing background tabs already included official group URLs; no other conversation's tabs were navigated, edited or closed.
3. Read-only `page.text.snapshot` on existing group tab `panel-tab-294`, document scope/maxChars=10000, returned **“Verifying your browser / Please complete the verification above / Sign in to skip this check.”** No pagination/truncation and no actual paper listing. Snapshot ID was `text-bdd06eae-da75-44f4-9f2d-68fa92752834`.
4. FetchURL F17 was a second legitimate public group route, but only returned a loading shell. F06's official forum likewise challenged. No API backdoor, authentication workaround, challenge-solving, author-profile matching or repeated polling followed.

Consequently this stream does **not** verify an ICLR2027 group listing, an official submission invitation or a paper decision. It only verifies that the official URLs were attempted and unavailable in this session. The distinction matters: search-index “ICLR2027” text is not the required official group/forum/status verification.

## 5. Search leads not admitted as verified ICLR2027 works

| Indexed lead | Public URL | What is known / missing |
|---|---|---|
| Mass-Aware Fusion of Sparse and Low-rank Attention | https://openreview.net/forum?id=fsYcvdtKHd | Q11 title lead; actual official forum F06 challenged. Need exact official title/version/date/group/status and original equations. No identity/acceptance inferred |
| Representative Attention for Vision Transformers | https://openreview.net/forum?id=I0YNpRTZmT | Q11 title lead only, forum not opened here. Submission-like snippet date/status is not treated as verified metadata |

Other Q06 memory-agent hits are not promoted into the inventory because they did not resolve the native-state mechanism gap. No claim that the field or venue lacks further relevant work. No deanonymization or cross-matching of anonymous submissions with named arXiv authors occurred.

## 6. Version/claim corrections to preserve

- D03 merging AsymKV and D16 quantization AsymKV are different titles/authors/stable sources. Do not deduplicate by short method name.
- D17 LRKV v1 2026-01-16 and v3 2026-04-07 are one work. v3 changes scale/headline analyses; fewer training steps is not a measured per-step speedup. Original introduction's “2.6 GB exceeds 5 GB” is false arithmetic, not a finding to borrow.
- D19 Thin Keys v3 is locked to 2026-03-18. v4 exists, but full-read scope is not silently moved to it. Its truncated-SVD approximation does not justify unconditional exact equality, and its claim excluding GQA conversion conflicts with D12's original uptraining method.
- D02 metadata title vs HTML heading differ at the same ID; do not split. D06/W0219 token-dimensional “heads” are not automatically independently querying channel heads. W0214's changed title is the same stable work, not a new paper.
- D07 first/second authors are both confirmed by F30, improving the older audit's incomplete author record without modifying the old file.
- D20 donor read-output mediation is not a q-only formation intervention; four-choice performance and its failed prose pilot stay separate. D21 predictive utility uses sampled futures for offline labels and per-host retraining; “query-agnostic” is a serving permission, not universal distribution independence.

## 7. Storage, tools, and verification boundaries

No manual PDF download, shell network downloader, software installation, paid access, model training, benchmark reproduction or source-code execution. Tool-generated large-text caches are automatically retained outside the project; they were read only and are not deliverables. Future authorized PDFs must use explicit stable-version paths under `E:/projects/FLUED/FLUED/docs/research/flued_broad_research_v2/01_discovery/A03/sources/`, not `/tmp` or Downloads.

Final deliverable verification **passed** using a local read-only `python -c` Markdown check: all four requested files decode as UTF-8 without replacement characters; all **41 local Markdown links** resolve; D01–D21 are unique and sequential; the **12 reused-card rows**, **15 priority-queue rows**, **13 search-query rows** and **32 Fetch request rows** match the declared counts. `git status --short --untracked-files=all -- docs/research/flued_broad_research_v2/01_discovery/A03` lists exactly the four requested Markdown files; the validation produced no files. Project tests/training are not applicable to a documentation-only discovery task and were not run. No new report/scaffolding files were created for validation.

No claim of venue completeness, full-field exhaustion, architecture selection, new experiment results or final total-report synthesis is made.
