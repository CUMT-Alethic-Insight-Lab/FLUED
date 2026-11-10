# A08 — Executed searches and venue-access methodology

Access date: **2026-11-09, Asia/Shanghai**. Scope: broad memory, linear attention, fast weights, state-space models, native queries/readout, causal use, optimization/shortcuts, and component transfer. Detailed byte/interface discovery belongs to A07. No internal text, code, experiment data, manuscript or credentials were uploaded. All query strings below are public topic words or public paper titles. No academic-source plugin was used; therefore no scholar/arXiv plugin skill/API was invoked. Tools used: WebSearch, FetchURL, built-in Desktop browser, and read-only local catalog/card inspection.

## 1. Venue identity and decision chronology: actual official evidence

1. **Official CFP:** https://iclr.cc/Conferences/2027/CallForPapers — successful FetchURL. Identifies the 15th International Conference on Learning Representations; abstract deadline 2026-09-18, paper deadline 2026-09-25; reviews released 2026-11-05; author discussion through 2026-11-18; final decisions planned **2026-12-16**. These dates establish that this access falls in discussion, not a completed acceptance cycle. The CFP's policy text does not itself establish any individual paper's decision.
2. **Official group UI:** https://openreview.net/group?id=ICLR.cc/2027/Conference — FetchURL returned only `Loading`; no submission list. Built-in browser `browser.create_tab` returned `TAB_NOT_ACTIVE` after a control conflict; `browser.get_state` showed existing group tabs. Reading the already-loaded group page (`panel-tab-286`, document scope, maxChars=18000) returned 13 blocks: navigation, `Loading`, footer; `scanTruncated=false`, no cursor. This is an actual UI rendering limitation, **not evidence there are zero submissions or that the group is absent**. No other agent's unrelated research pages were read or closed.
3. **Official public group JSON:** https://api2.openreview.net/groups?id=ICLR.cc/2027/Conference — successful FetchURL, `count=1`, `fromCache=true`. Verified exact `id`, `readers=[everyone]`, official website/title, and:
   - `submission_id=ICLR.cc/2027/Conference/-/Submission`
   - `submission_venue_id=ICLR.cc/2027/Conference/Submission`
   - `withdrawn_venue_id=ICLR.cc/2027/Conference/Withdrawn_Submission`
   - `desk_rejected_venue_id=ICLR.cc/2027/Conference/Desk_Rejected_Submission`
   - `rejected_venue_id=ICLR.cc/2027/Conference/Rejected_Submission`
   - public submissions, withdrawals and desk rejections enabled.
   - Group webfield declares Active Submissions, Withdrawn Submissions, Desk Rejected Submissions and Recent Activity tabs. Presence of accepted-decision options in workflow configuration is **not an acceptance decision**.
4. **Official retrieval guidance:** https://docs.openreview.net/how-to-guides/data-retrieval-and-modification/how-to-get-all-submissions — successful FetchURL. It distinguishes all submissions by submission invitation from active/withdrawn/desk-rejected content.venueid filters. A guessed deeper docs URL `https://docs.openreview.net/reference/api-v2/entities/note/search-notes` returned HTTP404; one legitimate docs route above succeeded. No package was installed.

### Direct-list and direct-record limitations

Each following FetchURL returned `Complete the check below to continue to OpenReview` rather than data. No credentials, CAPTCHA solver, private session, alternative IP or authentication bypass was attempted:

- https://api2.openreview.net/notes?content.venueid=ICLR.cc/2027/Conference/Submission&limit=3&offset=0
- https://api2.openreview.net/notes?invitation=ICLR.cc/2027/Conference/-/Submission&limit=3&offset=0
- https://api2.openreview.net/notes?id=UUldzWxIL4
- https://api2.openreview.net/notes?id=b3lZofUyGC
- https://openreview.net/forum?id=b3lZofUyGC
- https://openreview.net/forum?id=rylDfnCqF7 (older ICLR2019 source)
- https://openreview.net/pdf/1b1c1f0bcf93d66c0326eb239f6480ca4d336635.pdf
- https://openreview.net/pdf/4b049a14ede5c22389997afeb1b72a99e81a7de5.pdf

The official **public search endpoint** independently returned public submission records, below. Its results verify only the returned metadata and abstract; it did not grant access to blocked full text, direct replies or private decisions. Do not represent a metadata recovery as overcoming the full-text wall. Direct-list failure means **no complete venue enumeration** was achieved.

## 2. Exact official API searches and pagination actually executed

Common base URL:

`https://api2.openreview.net/notes/search?term=<URL-encoded text>&group=ICLR.cc/2027/Conference&limit=<n>&offset=<k>`

In this table, text inside quotes includes **literal double quotation marks**, encoded `%22`; plain spaces are `%20`. `group` is the exact string above, not an invitation or content.venueid filter. There was no explicit sort parameter. Returned ordering is the service's search ordering, not a chronological scan. Successful responses were bounded to the requested number of records, contained full abstracts in those records, and reported `fromCache=true`. No reported count is interpreted as a count of relevant papers, accepted works, or unique works read.

| Key | Exact `term` text | `limit,offset` actually fetched | Returned count / relevant results and limits |
|---|---|---|---|
| S01 | `linear attention` | 10,0 | 6811; V10,V01,HOLA,HaLA,V07,SPLA withdrawn,V08,LISA,V06,V03. Phrase was **not quoted**; broad noisy matching. Ten records read, not all 6811. |
| S02 | `linear attention` | 5,10 | 6811; LaLanD,V11,V09,ADLA,V04. Completes offsets0–14 only across S01/S02. |
| S03 | `fast weights` | 3,0 | First attempt network/extraction failure; **one exact retry** succeeded, count3906. Returned desk-rejected fast/slow geometry, V05, withdrawn GraspTTT. Three records, not corpus census. |
| S04 | `state space` | 3,0 | 10000; V12,Differential Attention for SSMs,SSD Attention Non-Collapse. A reported10000 may be a service cap; not independently validated as exact cardinality. |
| S05 | `model stitching` | 3,0 | 10000; FedSSP,V13,V14. Broad matching, three records only. |
| S06 | `shortcut learning` | 3,0 | 10000; V15,V16,Counterexample-Guided Shortcut Suppression. No pagination beyond first3. |
| S07 | `"associative recall"` | 5,0 | 44; V02,PAY AT THE EVENT,Five Invariants,V21,HOFA. Quote-sensitive query is much narrower than unquoted multiword terms. |
| S08 | `"posterior collapse"` | 3,0 | First attempt network/extraction failure; **one exact retry** succeeded, count7. V17,RST,SOLA withdrawn. Only first3 of7, not complete latent-variable coverage. |
| S09 | `causal memory` | 3,0 | 6293; CAUSEWAY,V18,V19. Broad matching, not all causality papers. |
| S10 | `"query"` | 3,0 | 3215; QART,MemSeeker,V20. Very broad; no native-readout completeness claim. Visual tokenizer details not developed because A07 owns interface discovery. |
| S11 | `"associative recall"` | 5,5 | 44; Spike-driven Hopfield,V22,ENGRAM,Selective but Not Broad withdrawn,HALA distance attribution. Together S07/S11 inspect offsets0–9 only. |
| S12 | `"linear attention"` | 3,0 | 196; V10,HOLA,V07. Compared with S01 count6811 to empirically show quote sensitivity. **Only first3 of196**; not first page of the same unquoted result set. |
| S13 | `"predictive state"` | 3,0 | 36; V24,V25,PreSTA video interface. Third result is not developed here. No pagination beyond3. |
| S14 | `"Functional Invariances for Low-Precision Linear Recurrences"` | 1,0 | 1; exact returned title is **LinQuant: Functional Invariances for Low-Precision Linear Recurrences**, V23. Search snippet's missing prefix was not treated as another work. |

Reconstructable exact examples:

- https://api2.openreview.net/notes/search?term=linear%20attention&group=ICLR.cc/2027/Conference&limit=10&offset=0
- https://api2.openreview.net/notes/search?term=linear%20attention&group=ICLR.cc/2027/Conference&limit=5&offset=10
- https://api2.openreview.net/notes/search?term=%22associative%20recall%22&group=ICLR.cc/2027/Conference&limit=5&offset=0
- https://api2.openreview.net/notes/search?term=%22associative%20recall%22&group=ICLR.cc/2027/Conference&limit=5&offset=5
- https://api2.openreview.net/notes/search?term=%22linear%20attention%22&group=ICLR.cc/2027/Conference&limit=3&offset=0
- https://api2.openreview.net/notes/search?term=%22predictive%20state%22&group=ICLR.cc/2027/Conference&limit=3&offset=0
- https://api2.openreview.net/notes/search?term=%22Functional%20Invariances%20for%20Low-Precision%20Linear%20Recurrences%22&group=ICLR.cc/2027/Conference&limit=1&offset=0

All other actual URLs follow the same explicit template and table parameters. No hidden `page`, no `offset>14`, no `limit=1000`, no all-venue scrape, and no automatic pagination were executed. Search count10000 is a **coverage warning**, not permission to announce that the venue contains10000 relevant works. Matching semantics beyond observed quote sensitivity were not documented/experimentally established (do not assert Boolean AND or OR). Returned records can be active, withdrawn, or desk-rejected: status must be checked **per record**. In our inspected selected records domain/group matched, but search-group correctness for unseen pages was not audited.

### What was actually retained

WORKS_AND_PROBLEMS contains25 active-forum records,7 separately verified recent/recovered primary controls,3 official status controls, and8 existing scoped-card reuse entries. These are **different cohorts**, not a sum of new papers or new full reads. The25 active rows include a candidate existing W0086 match, so even that table is not25 globally new works. Other public search hits above are screening metadata only, not fully developed problem records or additional reading claims. No arXiv/anonymous-forum identity matching by author was attempted.

## 3. Exact WebSearch discovery queries

Search engine output has no stable pagination contract exposed by WebSearch. These are the actual query strings, with returned snippets used for discovery only. No manual search-result page2 was requested. Every adopted scientific claim comes from official search JSON, a primary arXiv page/body, or an explicitly reused card, not from these snippets.

| Query | Actual result/use |
|---|---|
| `site:openreview.net/group?id=ICLR.cc/2027 Conference` | No useful exact group result; noisy other-venue groups. A negative indexed result is not group absence. Direct official group/CFP later succeeded. |
| `ICLR 2027 OpenReview submissions linear attention memory delta` | Mixed secondary deadline/count claims and other-year papers; not accepted as venue evidence. No claimed60000/23759 totals inherited. |
| `2026 linear attention state memory erasing writing learning capacity benchmark` | EDA primary arXiv plus EMNLP/ICLR2026 leads; only EDA followed as adopted source. Other venue leads not independently status-verified. |
| `2026 recurrent models associative recall query first beyond state capacity` | Anatomy,W0213,Memory by Design,DART,RunningTensor leads. Relevant selected primary URLs fetched below; no extra source claims from blogs. |
| `2026 shortcut learning dynamics in context learning model stitching memory` | Broad noisy results; anonymous PDF lead alone not enough to identify a work. Used targeted official searches instead. |
| `site:openreview.net/forum "ICLR 2027" "memory"` | Agent-memory forums including Continuous Memory Machines; not main adoption criterion and not a census. |
| `site:openreview.net/forum "ICLR 2027" "linear"` | V02,V23 and irrelevant linear optimization/probes; followed official metadata, not snippets. |
| `site:openreview.net/forum "ICLR 2027" "stitching"` | V13 among trajectory/image stitching false positives; official S05 verified proper model-stitching metadata. |
| `site:openreview.net/forum "ICLR 2027" "shortcut"` | Many task-specific shortcuts and wrong-rule lead; adopted S06 instead of counting keyword matches. |
| `"Lagging Inference Networks" ICLR 2019 OpenReview` | Found public author bibliography and rylDfnCqF7 lead; direct forum blocked. Prior recovery's venue association retained with limitation, not freshly decision-certified. |
| `"Predictive Representations of State" 2001 Littman Sutton Singh` | Institutional PSR-family references; then actual original author PDF fetched. No modern summary used to certify original theorem/learning claim. |

## 4. Primary FetchURL checks outside official ICLR2027 search

| Actual URL(s) | Access and evidence depth |
|---|---|
| https://arxiv.org/abs/2609.16183v1 ; https://arxiv.org/html/2609.16183v1 | Abstract/history success; HTML68981-character extracted result saved automatically by tool to its session result area. Actual selected reading: §4.2–6, §9; headers/keyword search elsewhere. **P, not full**; figures, full appendices and companion paper not fully inspected. |
| https://arxiv.org/abs/2610.19709v1 ; https://arxiv.org/html/2610.19709v1 | Abstract/history success; HTML53957-character result automatically saved by tool. Actual selected reading: §5–6 and Limitations, selected introduction/relevance/probe hits. **P, not full**; complete dataset/table/probe appendices not read. |
| https://arxiv.org/abs/2605.31163v5 | Success; abstract and history v1–v5; selected source is v5 2026-10-14, not search engine's v4 2026-10-07. A-depth, W0226 reuse. |
| https://arxiv.org/abs/2606.26560v1 | Success; abstract/history, v1 2026-06-25, A-depth. Already previous axis-recovery candidate, not globally new. |
| https://arxiv.org/abs/2607.07706v1 | Success; abstract/history, v1 2026-07-08, A-depth this session. Earlier transfer audit contains body excerpts, not automatically another FULL. |
| https://arxiv.org/abs/1901.05534v1 | Success; abstract/history also lists v2. Main record explicitly says v1 this session; BIW-0096 and older selected v2 evidence retained separately, not merged into a fictitious full read. |
| https://arxiv.org/abs/2504.13173v1 | Success; MIRAS original title **It's All Connected: A Journey Through Test-Time Memorization, Attentional Bias, Retention, and Online Optimization**, v1 2025-04-17, A-depth. Screening/recovered design framework, not extra full work in adopted32-row register. |
| https://proceedings.neurips.cc/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html ; https://proceedings.neurips.cc/paper_files/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html | Both returned PSR abstract/introduction text, not a complete structured bibliographic page. Use institutional original below for title/definition/statement; do not invent revision metadata from hash. |
| https://web.eecs.umich.edu/~baveja/Papers/psr.pdf | Successful original manuscript extraction; title/author header, definition, Theorem1 statement and §3 conclusion inspected. Proof text was delivered but not independently checked; **selected P, not FULL**. |

**No PDF was downloaded by the agent.** FetchURL's session-owned automatic text-result storage is tool infrastructure, not a user-directed `/tmp`/Downloads PDF path. If later full-text acquisition is authorized, explicit destination must be `docs/research/flued_broad_research_v2/01_discovery/A08/sources/` (or the reading owner's assigned project folder), with version/hash/URL retained. This session created no `sources/`, script, log dump or binary artifact.

## 5. Local audit and dedup performed

Read PLAN and FOLLOWUP_DIRECTIONS, seven matching older coverage audits (six axes plus global), prior global SEARCH_LOG, old identity/version register, and current BIW catalog opening/current Charformer card. Exact catalog searches included selected new titles, arXiv IDs, and aliases. Stable old hits: W0086, W0213, W0226; BIW-0096 for Lagging. Existing reading inputs actually opened: W0229 first85lines; full short cards W0333,W0337,W0050,W0092,W0192,W0534 and BIW-0005. No all-card semantic audit or global count recomputation was performed. Older global counts are historical, not certified here.

Important correction: old six-axis audits predate newer BIW full cards. Their unread CANINE/Charformer/MANTa/MEGABYTE labels must not override current byte evidence. Conversely, FULL in an existing card does not establish that the old synthesis actually used it, nor that this session reread its original paper.

## 6. Reproducibility limits and legitimate continuation

- Source access is **partial**: official venue/group identity and selected public records verified; UI/list/direct full-text access limited. No arbitrary claim of venue-wide or field-wide saturation.
- Search is **English and mechanism-led**, not a systematic review. It has first-page/relevance-ranking bias, likely title/abstract vocabulary bias, no citation-network closure, no non-English search, and incomplete date/track coverage. Latest arXiv versions and future venue decisions must be refreshed before publication.
- Exact phrase searches reduce noise but miss synonyms and title variants; broad unquoted searches return huge capped sets. Neither count is a denominator for six-axis coverage.
- Reviews were not read. Anonymous records' abstracts describe author claims; a public review could contextualize contention, not supply experimental ground truth.
- A next venue pass should use documented official enumeration if public access works, iterate offset until exhausted, record per-page counts/duplicate IDs/statuses, and save minimal public metadata within its assigned project folder. If enumeration remains blocked, retain the explicit partial-coverage label rather than reconstructing a whole venue from search-engine snippets.
- One/two legitimate routes were used for specific failures (network retry once for S03/S08; official docs alternate; public original/author institutional source for older works). Verification challenges were not repeatedly hammered or bypassed.

## 7. Deliverable validation

Only the four requested Markdown files under A08 are agent-authored deliverables. A read-only Python check verified UTF-8, unique active V01–V25/local R01–R07 register keys,25 official forum rows, local Markdown file-link targets, and absence of replacement characters. `git diff --check` and `git status --short` were inspected. The broad v2 research root and unrelated bundles/draft were already untracked before writing; no deletion or modification of those other files. No training, model execution, installation, paid access, commit, production edit or test/build output. This documentation task was not verified by pytest; citation/source boundaries were verified directly as above.
