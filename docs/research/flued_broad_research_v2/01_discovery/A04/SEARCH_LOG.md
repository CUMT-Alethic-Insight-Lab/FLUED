# A04 — Executed search and source-verification log

Date: 2026-11-09. Scope: deployed content use, native readout versus probe recovery, correct evidence use, intervention validity, mediation/interaction, redundancy/self-repair, metric gaming, natural counterfactuals and uncertainty. Public search strings only; no internal project names, run identifiers, private documents, code or experiment values were uploaded.

## 1. Local recovery actually performed

Read:

- `docs/research/flued_broad_research_v2/PLAN.md`.
- `docs/research/flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md`.
- All three previous `07_scope_recovery/04_DEPLOYED_USE/` audit/log/recommendation documents.
- Actual cards `B14/W0369`, `B08/W0372`, `B08/W0374`, `B26/W0530`, `B26/W0532`, `B26/W0534`, `B26/W0535`, `B03/W0050`, `B13/W0383`, `B14/W0384`.
- Byte-interface actual cards `R01/BIW-0005` and `R01/BIW-0006`, preserving aliases W0005/W0006 and reading versions.

Searched the multigranularity `02_catalog/CATALOG.md` by selected W IDs, stable IDs, title aliases and mechanism phrases; searched `FINAL_ADDENDUM_INDEX.md` for new identities. Searched byte-interface `02_inventory/WORK_CATALOG.md` for these stable IDs/title aliases and causal-measurement terms. These are targeted deduplication searches, **not full reading of both catalogs** and not proof that an idea has never been mentioned in another old narrative. The broad initial byte-inventory mechanism search had 405 matches and returned only 50; that truncated result is not used as comprehensive negative evidence. Later exact identity searches returned no matches for the candidate identities.

No nested AGENTS.md was found under docs by the dedicated glob. Initial `git status --short` already showed the three survey directories and other pre-existing untracked material; none of that unrelated material was removed or edited.

## 2. Fourteen WebSearch queries actually executed

Search results were used for discovery only. Primary-page retrieval below determines evidence depth and verified metadata. Search timestamps/snippet publication dates were not treated as authoritative version dates.

| Query | Exact public string | Relevant outcome and decision |
|---|---|---|
| Q01 | `activation patching faithfulness self repair causal evaluation 2025 2026 language models` | EMNLP2025 explanation-patching paper N04; primary ACL page fetched. SAE/CoT papers were not pursued because shared patch evaluation would not close independent-content correctness. |
| Q02 | `naturalistic causal probing counterfactual evaluation language models 2022 2025` | W0373 formal TACL record recovered; causal-reasoning benchmark results excluded as measuring a different ability. |
| Q03 | `"ICLR 2027" "patching"` | Two exact OpenReview forum leads; forum/API/browser access blocked by verification. They are not counted as verified 2027 works. Unrelated road-patching results discarded. |
| Q04 | `"faithfulness" "circuit" "2025" "minimality" evaluation` | Input-variation and stability leads N02/N03, plus generic reviews. Primary original sources pursued rather than review recommendations. |
| Q05 | `"language models" "counterfactual" "context" "2026" evidence use` | Broad/noisy recent search; agent-trace and workspace leads did not become verified records. Not evidence that no recent grounded-use work exists. |
| Q06 | `"faithfulness" "circuit" "2024" "2025" "measure" ablation` | N01 robustness paper and a primary-author methodological lineage. N01's own body later read selectively. |
| Q07 | `"How Faithful" "RAG" counterfactual 2024 2025 context` | FaithEval/ClashEval references and newer training approaches; prioritize original measurement contracts rather than more architecture variants. |
| Q08 | `"Right for the Wrong Reasons" "2023" language models evidence` | Recovered the 2019 HANS original through citations; official ACL identity fetched rather than retaining mistaken query year. |
| Q09 | `"Causal Scrubbing" causal interpretation hypothesis 2022 Redwood` | Original author-posted protocol and primary PDF mirror surfaced; actual original post fetched, no peer-reviewed-venue assumption. |
| Q10 | `"FaithEval" arxiv benchmark faithful contexts` | Exact 2410.03727 identity, primary metadata and v3 body fetched. Third-party summaries not used for experiment details. |
| Q11 | `"How Faithful Are RAG Models"` | 2404.10198; official Atom later exposed updated title **ClashEval**. One work, not two. |
| Q12 | `"Interpretability in the Wild" "IOI" 2211` | Original 2211.00593 verified; abstract only in this round. Grouped-backup details remain original-reading work, not inferred from the title. |
| Q13 | `"Méloux" "2025" "non-identifiability" interpretability` | 2502.20914 original enumeration study N10; official metadata verified. Theory and empirical instability kept separate. |
| Q14 | `"faithfulness" "hypothesis tests" "Shi" "2024" circuits` | N11 original testing paper and N12 official PMLR UAI2026 protocol. Both fetched from primary sources; neither full-read. |

No exhaustive engine pagination was attempted; tools returned bounded ranked result sets. Fourteen queries are fourteen searches, not fourteen screened corpora. Search breadth covers selected classics through 2026, not all papers in the last twelve months or the complete ICLR2027 program.

## 3. Primary retrieval: what was obtained, not merely requested

### 3.1 Recovered prior leads and existing unread works

| Actually fetched public URL | Result / depth / use |
|---|---|
| https://arxiv.org/abs/2004.12265 | Success, abstract/history; v2 dated2020-11-22. R01, not full original. |
| https://arxiv.org/abs/2307.15771 | Success, abstract/history; only v1 dated2023-07-28. R02, no numerical compensation claims. |
| https://arxiv.org/abs/2301.04213v2 | Success, abstract/history; R03. NeurIPS2023 Spotlight checked in official Atom, not through a forum this round. |
| https://aclanthology.org/2020.acl-main.408/ | Success, abstract and full formal bibliography/PDF link. R04, PDF not read. |
| https://arxiv.org/abs/2308.14272 | Success, abstract/history; R05, v1. Prior audit's body selection inherited, not reread as FULL. |
| https://arxiv.org/abs/2110.08412 | Success, abstract/history through v3; R06. No original full reading. |
| https://arxiv.org/abs/2508.21258v2 | Success, abstract/history, R07. Exact-AP approximation claim and pass count treated as author-reported. |
| https://arxiv.org/abs/2606.27510 | Success, abstract/history; R08, v1. |
| https://arxiv.org/html/2606.27510v1 | Success, large text saved automatically by the tool; actually selected §§2–5.3 plus introduction/opening discussion, not appendix proof/full tables. R08=P. |
| https://arxiv.org/abs/2309.16042v2 | Success, abstract/history; W0533/R09, v2. |
| https://arxiv.org/html/2309.16042v2 | Success, large text saved automatically; actually read §§5–6 and targeted method/result excerpts. Not FULL, no new W0533 full card. |
| https://arxiv.org/abs/2402.17700v2 | Success, abstract/history; W0531/R10, v2 dated2024-08-26. No full body read. |
| https://aclanthology.org/2023.tacl-1.23/ | Success, formal metadata/abstract/PDF link; W0373/R11. Original venue TACL2023 established, distinct from old2022 preprint date. |
| https://aclanthology.org/2020.emnlp-main.14/ | Success, abstract; W0370/R12, learning-effort versus accuracy distinction. |
| https://aclanthology.org/2020.emnlp-main.14.bib | Success, exact title, Elena Voita/Ivan Titov, EMNLP2020, DOI/pages. Not a full reading. |

### 3.2 New-to-selected-catalogs original sources

| Actually fetched public URL | Result / exact scope |
|---|---|
| https://arxiv.org/abs/2407.08734 | Success, abstract/history. N01; full first-author identity checked via Atom because HTML extraction omitted Joseph Miller. Official comment associates CoLM2024. |
| https://arxiv.org/html/2407.08734v1 | Success. Selected §§3–6 including node/edge/branch, invariant positional encoding, ratio aggregation and circuit/complement distinction. Appendices and all tables not read. |
| https://arxiv.org/html/2606.06267v1 | **First request network error; one same-URL retry succeeded.** Large text saved by tool. Actually read introduction and §2.1, not the whole 101-page later version. The rendered title is the later long title; quantitative version-sensitive claims are bounded to the separately verified v2 abstract. |
| https://arxiv.org/abs/2606.06267v2 | Success, locked v2 abstract/history. N02; core≥99% claim explicitly qualified to models above70M; SVA replication and untested position/feature-level specialization recorded. |
| https://arxiv.org/abs/2510.00845 | Success, abstract/history through v4. N03. Earlier-title suffix “of EAP-IG” is an alias, not another work. |
| https://arxiv.org/html/2510.00845v4 | Success, full retrieved text available; actually selected §§1–6, appendices uncompleted. Exact-CMA task coverage inconsistency between §5.1 and figure/limitations recorded for the next reader. |
| https://aclanthology.org/2025.emnlp-main.529/ | Success, official abstract. N04, no primary body full reading. |
| https://aclanthology.org/2025.emnlp-main.529.bib | Success, Wei Jie Yeo/Ranjan Satapathy/Erik Cambria, formal EMNLP2025 pages10425–10447/DOI. This proceedings record overrides stale arXiv “under review” as venue evidence, without claiming texts identical. |
| https://aclanthology.org/P19-1334/ | Success, HANS original abstract. N05. |
| https://aclanthology.org/P19-1334.bib | Success, full title, authors, ACL2019, pages3428–3448, DOI. Not an original full read. |
| https://www.alignmentforum.org/posts/JvZhhzycHu2Yd57RN/causal-scrubbing-a-method-for-rigorously-testing | Success, author-posted primary text. N06, returned introduction/setup and opening §3, ending during §3.1; later algorithm/limitations/sequence not read. No formal venue or immutable revision inferred. |
| https://arxiv.org/abs/2410.03727 | Success, abstract/history through v3. N07. |
| https://arxiv.org/html/2410.03727v3 | Success, large text saved by tool; §3.1–3.3 explicitly read. Different human/string validation protocols and answer-mention accuracy recorded. Results/appendices not completed. |
| https://arxiv.org/abs/2404.10198 | Success, abstract/history through v3; extraction still showed an older title. N08 identity corrected using official Atom. |
| https://arxiv.org/html/2404.10198v3 | Success, main text extracted. Actually used §§1,3–4.4, not full tables/appendices. Kept prior-bias/context-bias conditions and paywalled-original-data caveat. |
| https://arxiv.org/abs/2211.00593 | Success, abstract/history; N09, v1. Original detailed grouped-backup protocol not read. |
| https://arxiv.org/abs/2502.20914 | Success, abstract/history; N10, v1. Toy enumeration scope retained. |
| https://arxiv.org/abs/2410.13032 | Success, abstract/history; N11, v1. Search venue association not promoted to verified acceptance. |
| https://proceedings.mlr.press/v337/asiaee26d.html | Success, official UAI2026/PMLR337 record, full bibliography/abstract and proceedings PDF link. N12, PDF not read. Bounded score/adaptive weighting/anytime-valid claims are abstract-level and pending assumptions check. |

Large FetchURL output artifacts are automatically managed session **text** results, not project PDF downloads or new reading cards. Only selected ranges were opened with Read/Grep. No claim of full reading follows from fetching a long document.

### 3.3 Official metadata batches, exact queries and result bounds

These are direct public HTTP requests with FetchURL, not an academic-data-source plugin call. No scholar/arxiv data-source tool was used; therefore no plugin skill/API-documentation workflow was invoked. No source code or internal content was sent as a query.

1. `https://export.arxiv.org/api/query?id_list=2407.08734,2606.06267,2510.00845,2410.03727,2404.10198,2211.00593,2610.19373`
   - Success; Atom `totalResults=7`, `startIndex=0`, `itemsPerPage=10`; seven entries, not a paginated search corpus.
   - Verified current author/title/version records, title changes for N02/N03/N08, W0050v1 date2026-10-14, N02 journal reference TMLR2026, N07 official comment ICLR2025, N01 comment CoLM2024.
   - These publication associations are explicitly provenance-tagged, not independent inspections of each venue forum.
2. `https://export.arxiv.org/api/query?id_list=2502.20914,2410.13032,2410.14155,2004.12265,2307.15771,2301.04213,2308.14272,2110.08412,2508.21258&max_results=10`
   - Success; Atom `totalResults=9`, `startIndex=0`, `itemsPerPage=10`; nine entries, no missing pagination.
   - Full authors/versions, R03 NeurIPS2023 comment, N10 ICLR2025 journal reference; N04 arXivv2's old “under review” contrasted with official EMNLP2025 proceedings, not mistaken for current nonpublication.

## 4. ICLR2027: group verified, relevant forums not verified

### Official venue/group response

- `https://openreview.net/group?id=ICLR.cc/2027/Conference`: FetchURL returned loading/login chrome, not enough to establish venue content.
- `https://api2.openreview.net/groups?id=ICLR.cc/2027/Conference`: **success**, one public group. Fields include title *The Fifteenth International Conference on Learning Representations*, subtitle *ICLR2027*, website `https://iclr.cc/Conferences/2027`, `public_submissions=true`, submission venue ID `ICLR.cc/2027/Conference/Submission`, and separate withdrawn/desk-rejected/rejected venue IDs.
- The group defines possible acceptance options; **their existence is not evidence of a decision for any paper**. No accepted-work count or complete submission coverage follows from this group lookup.

### Exact leads and blocked legitimate routes

| Search-discovered lead | Actual attempts | What is and is not verified |
|---|---|---|
| “What Can Activation-Patching Evidence Establish?” — https://openreview.net/forum?id=7IkH0oITID | Forum FetchURL → verification challenge. One public-note API route `https://api2.openreview.net/notes?id=7IkH0oITID` → same challenge. One built-in-browser create attempt returned TAB_NOT_ACTIVE after control changed; state inspection showed its created tab at the verification page; read-only DOM snapshot confirmed the challenge. | Search snippet suggests ICLR2027 Submission31674, but **forum title/version/date/membership/status not verified from forum content**. Do not count as confirmed submission or acceptance; do not infer authors. |
| “All the Facts, Still the Wrong Answer: Integration Gaps in…” — https://openreview.net/forum?id=mXDeixZEEw | Forum FetchURL → verification challenge. One public-note API route `https://api2.openreview.net/notes?id=mXDeixZEEw` → same challenge. | Search snippet suggests ICLR2027 Submission46351 and multimodal integration/probing; exact complete title, revision and status remain unverified. No author search or arXiv identity matching performed. |

No challenge solving, sign-in, authentication bypass, paid retrieval or deanonymization. These are **lead-only records excluded from the24 verified/recovered candidates**. There is no assertion of field or venue exhaustion. Browser state contained other streams' existing tabs; none were edited/closed. The failed create left a challenge tab (`panel-tab-291` at inspection); it was not navigated or used to bypass verification. Browser work used the built-in desktop browser, not Chrome/Edge/WebBridge.

## 5. Deduplication and scope decisions

- Eight previous audit discoveries N01–N08 retain aliases as A04-R01–R08; not “new papers discovered today.” They were reverified against primary sources.
- Existing W0533, W0531, W0373 and W0370 are A04-R09–R12; newly recovered evidence, not new entities. All remain incomplete original reads.
- N01–N12 are new candidates relative to exact-identity searches of the two selected catalogs plus final addendum. Count=12 within this provenance definition; no global W-ID allocation or shared catalog edit.
- N02: short search title versus long v2 title; one entity. N03: title with/without “of EAP-IG”; one entity. N08: *How faithful are RAG models?* versus *ClashEval*; one entity. N04: EMNLP2025 proceedings and 2410.14155v2; one work, text equivalence unverified.
- New mechanistic-method papers were selected only where they change an evaluation decision: donor invariants, path leakage, interaction/background, structural/function separation, reference hypotheses or sequential validity. Reviews, generic caution lists, and additional architecture names did not qualify by themselves.
- Independent source-free directions were retained: native reader improvement, task-matched writing, binding repair, local/remote integration, state precision/interference, extra computation, bounded interface adaptation, and instrument calibration.

## 6. Stop conditions, limits, and files owned

Stop here because primary discovery now covers specific missing protocols and falsifications; further progress on these claims requires original reading or target-host empirical tests, not more generic caveat papers. This does not mean the field is exhausted. Recent OOD/interaction, measurement validity and context-authority work may still be missed by ranked web search; two particularly relevant2027 forums remain blocked.

No newly completed original FULL reading; no paid/model API calls, no downloads/training/code execution/installation/commit. W0050's supplemental-material gap is inherited from its actual PARTIAL card; this round did not repeat that supplement search or assert it remains forever unavailable.

Only the assigned directory was written:

- `docs/research/flued_broad_research_v2/01_discovery/A04/COVERAGE_AND_FINDINGS.md`
- `docs/research/flued_broad_research_v2/01_discovery/A04/SEARCH_LOG.md`
- `docs/research/flued_broad_research_v2/01_discovery/A04/WORKS_AND_PROBLEMS.md`
- `docs/research/flued_broad_research_v2/01_discovery/A04/READING_HANDOFF.md`

Document validation uses local read-only Python checks for required artifacts, unique work headings, queue size, and relative Markdown-link targets. No test/training build output is required or generated for these Markdown-only research deliverables. Final repository status is checked without modifying pre-existing untracked materials.
