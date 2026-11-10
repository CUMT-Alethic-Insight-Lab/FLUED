# ICLR 2027 source audit R3 — bounded retries, unavailable originals, and safe synthesis limits

**Snapshot:** 2026-11-09; request timestamps are UTC. **Purpose:** independently diagnose the reported V17/V18 HTTP403s, look for lawful publicly identifiable editions without deanonymization, and state what the remaining source gaps permit in the final recent-literature report. This audit is **not** a new full-paper reading, mathematical-result adjudication, or acceptance inference.

## 1. Decision for the coordinator

**A qualified broad review can be delivered; a claim that the selected recent ICLR2027 mechanisms have all been original-paper-reviewed cannot.** The source-acquisition/reading gap is still substantive, not merely missing venue labels. Do not mark that completion condition done or silently remove unavailable competing mechanisms from the report.

### True counts for this bounded cohort

| Count | Actual disposition at R3 |
|---|---|
| New V17 official originals | **6 unavailable**: T01–T06 |
| New V18 official originals | **5 unavailable**: A08-V11,V16,V20,V21,V24 |
| Earlier six BLOCKED official originals | **6 remain unavailable**: A08-V02,V04,V13,V14,V22,V25; only V02 received a new representative PDF check, not all six |
| Total selected official originals not obtained | **17 distinct forums**, no official-PDF acquisition in R3 |
| Existing independently read lawful preprints | **2**: T03 arXiv2610.19139v1 and T05 arXiv2607.22334v1, already FULL in V17 at their own source scope; reused, not reread/recounted |
| Newly recovered lawful candidate edition | **1**: T02 arXiv2604.16037v1, acquired/title-checked only; **terra full reading pending** |
| Remaining cohort works without a lawful alternate established in this pass | **14**: T01,T04,T06; all five V18 official works; earlier six. This is bounded search failure, not proof of nonexistence |
| Fresh official metadata checks | **18**: all17 cohort forums still return conference submission status; one additional Compiled Tokenizers control still returns withdrawn |
| New FULL readings / accepted decisions established | **0 /0** |

Even for T02/T03/T05, **official anonymous manuscript equivalence remains unverified**. The17 official-PDF gaps do not shrink to14 merely because independent preprints exist. Conversely, saying all17 scientific topics are wholly unread would erase the two existing exact-edition preprint cards. Keep venue-record, source-edition, acquired-file and full-reading counts separate.

**Concrete recovery:** V17's T02 search missed the public British-spelling title *Stochasticity in Tokenisation Improves Robustness*. Exact spelling refinement recovered arXiv2604.16037v1; its title variant and substantive abstract match support a lawful candidate relationship. The PDF now has a verified acquisition receipt, not a new FULL card or a revealed anonymous identity.

## 2. Inputs and permitted boundary

Read [R2](ICLR2027_SOURCE_AUDIT_R2.md), [V17 summary](../03_reading/V17/BATCH_SUMMARY.md), [V18 summary](../03_reading/V18/BATCH_SUMMARY.md), the six V17 cards and the T03/T05 version/provenance sections; inspected the V18 exact-route/card access passages and existing R2 old-six ledger. R1/R2, ACCESS_DIAGNOSTIC, discovery/catalog records, reading cards and shared registries were left unchanged.

Used ordinary public HTTPS with certificate **and revocation** checks enabled, unchanged proxy/trust settings, existing curl/pdftotext, official public API/metadata and separately published arXiv originals. No login, credentials, author/profile crosswalk, WAF/challenge solving, TLS/revocation relaxation, IP/identity rotation, installation, training, source-code execution from papers, subagent, or commit. Public author names incidentally present on public search/source pages were not used or reproduced to identify anonymous forums.

[Manifest](source_staging/R3_manifest.json) retains sanitized requests/results and the acquired source's hash. Only this report and two R3-owned staging files were authored; existing R2 staging and V17 source files were read-only.

## 3. What the403s actually show

### Diagnostic method and representative requests

V17/V18 reported curl22 with HTTP403 using `--fail`. For R3 diagnostics, `--fail` was deliberately omitted so the **HTTP error body could be inspected**. Thus curl exit0 with HTTP403 means a completed diagnostic HTTP exchange, **not successful paper retrieval**. HTTPS-only redirects, bounded timeouts, certificate and revocation checks remained enabled; all representative curl receipts reported TLS result0 and `proxy_used=0`. No error/challenge page was renamed to PDF or passed off as paper text.

Only representative URLs were re-requested: one V17 paper, one V18 paper using its public locator and then its metadata-resolved content reference, and one earlier BLOCKED paper. A single repeated V17 content request confirmed its error text. No loop over all eleven/seventeen PDFs, no endless retry and no route variation intended to defeat a challenge.

| Representative route actually requested | Observed response | Supported interpretation / limit |
|---|---|---|
| `https://openreview.net/pdf/a212af497989974b1ce9ae2bb4adeaf0419f4041.pdf` — V17 T06 B-Net | GET403; `text/html`;12,692 bytes; no redirect; title **Error403 \| OpenReview**. One bounded repeat returned the same code/size and rendered restriction text | A genuine HTTP denial, not a failed TLS handshake or a PDF parser error. Body says “Access to this page is restricted. Please check that you are logged in to OpenReview and try again.” This generic template **does not distinguish** document-specific permissions from an access-control/verification layer |
| `https://openreview.net/forum?id=fMymbXoq9T` — same paper's normal public forum | One redirect to `/challenge?redirect=...`; final HTTP200 HTML,4,787 bytes, **Verifying your browser** and “Complete the check below” | Direct confirmation of a browser-verification gate on the forum route; final200 is **not** forum metadata or a paper. No interaction with the challenge |
| `https://openreview.net/pdf?id=uILf1c6VDo` — V18 V24 public locator | GET403; same generic Error403 template/size; no PDF | The reported public-locator denial is reproducible; not evidence that the forum is absent |
| `https://api2.openreview.net/notes?id=uILf1c6VDo` — normal public note API | HTTP403 JSON,271 bytes: **`ChallengeRequiredError`**, message “Challenge verification required,” a public challenge URL | Explicit API-level verification requirement, **not** a `NotFoundError` or a per-paper authorization explanation. Challenge URL was not followed to solve it |
| `https://openreview.net/pdf/ef23821335964a96e676f173f4f79bc853808ace.pdf` — V24's reference recovered from official search metadata | GET403; same generic restriction template/size as the locator | Fixes the metadata-reference gap on the V18 card, **not the body gap**. A content-reference URL does not make access successful; the public locator was not the only problem |
| `https://openreview.net/pdf/9c64cd9b8b1bba44c1ff65945bd6c1a02ed98a9d.pdf` — earlier A08-V02 Incentive | GET403;12,692-byte HTML; **Error403 \| OpenReview**, not PDF | Contemporary old-cohort representative has the same HTTP-denial class as the new cohort. Its previous R2 pre-HTTP revocation failure is **not** the error observed now |
| HEAD of metadata-linked T02 supplementary path `https://openreview.net/attachment/da32260c2016ab2efdf4f5875a890e5e0b66c20f.zip` | HTTP404; `text/html`; Content-Length header11,910; no ZIP downloaded | A separate attachment/method/path result, **not another confirmed challenge**. Does not prove attachment inexistence, staleness, or private access; HEAD behavior and artifact visibility remain unresolved. No guessed filenames or private endpoints followed |

Exact timestamps, selected safe headers, response markers/text and URLs are in the manifest. Cookies/credentials were neither used nor preserved. `server: nginx` identifies a response header, not the internal component responsible for denial.

### Answer to “wall, URL error, or permissions?”

- **Verified verification wall:** the representative forum redirect and API `ChallengeRequiredError` establish an actual gate on those routes.
- **Verified generic PDF403:** representative PDF bodies are access-restriction pages, not valid PDF bytes. Their wording alone cannot identify whether each PDF is behind a verification policy, a document permission rule, or another access layer. Public note `readers=[everyone]` is not a separately inspected PDF access-control list.
- **V24 reference corrected:** its current metadata provides the content reference that V18 did not recover. Both locator and resolved reference still403. Do not report a mere missing/incorrect guessed PDF URL as the resolved root cause.
- **No blanket service outage:** official public search responses remain usable, public arXiv sources are accessible, and the new arXiv PDF ultimately downloaded. Old Python automatic-proxy EOF, R2 Schannel revocation-offline, today's HTTP403 and today's explicit verification challenge are different observations.
- **Earlier six:** R2 documented individual failures for all six; R3 retested **one PDF representative** and refreshed metadata/search discovery for all six. This supports a shared current access-barrier **hypothesis** across cohorts, not a demonstrated common root cause for every artifact. The five un-retested old PDFs are not falsely counted as new R3 attempts.

**Stop rule:** normal representative retries/route checks have now characterized the failure sufficiently. Do not request every denied PDF again just to increment attempts. A future new official public file, legitimate published edition, or genuinely changed normal-access condition can justify a bounded refresh; repeated403/challenge responses do not justify bypass.

## 4. Official status and version snapshot

All17 selected forums were independently returned in R3 by official public search queries, each at `limit=1,offset=0`, reported count1. Checked `id=forum`, title, domain, public readers, submission invitation, venueid, note version, modification time and PDF reference. All17 still expose:

```text
domain: ICLR.cc/2027/Conference
readers: [everyone]
submission invitation: ICLR.cc/2027/Conference/-/Submission
content.venueid: ICLR.cc/2027/Conference/Submission
content.venue: ICLR 2027 Conference Submission
note version: 2
```

Their note modification dates remain **2026-10-05 UTC**. No change of the returned venue state, note version, modification timestamp or PDF reference was observed versus the earlier audits. Some responses expose `fromCache=true`; others omit it. These are **official-response snapshots**, not uncached live-thread/decision certification. Note version2 is not PDFv2. Manuscript revision/date, decision replies, public review contents and PDF equivalence remain unverified.

| Cohort / key | Exact title / official forum | Note modified UTC,2026-10-05 | Source disposition |
|---|---|---|---|
| V17 T01 | [Tokenization with Formal Guarantees: From Optimal Compression to Provable Bounds](https://openreview.net/forum?id=FXLPTx7osi) |20:36:04.382 | Official original unavailable; no lawful alternate established |
| V17 T02 | [Stochasticity in Tokenization Improves Robustness](https://openreview.net/forum?id=rIRkUxOleG) |17:31:08.512 | Official original unavailable; new British-spelling arXivv1 acquired, unread |
| V17 T03 | [Online Tokenization with Optimal Delay in Near Linear Time](https://openreview.net/forum?id=8D7l5sK3YT) |18:30:48.591 | Official original unavailable; existing FULL public arXivv1 has **Linear**, not **Near Linear**, in title |
| V17 T04 | [Tokenization Invariance Is Learned Late and Broken at the Head](https://openreview.net/forum?id=63kZK7oyd6) |20:03:19.716 | Official original unavailable; no lawful alternate established |
| V17 T05 | [Cross-Tokenizer On-Policy Distillation via Byte-Prefix Marginalization](https://openreview.net/forum?id=Mm5OLOPLT0) |16:57:39.933 | Official original unavailable; existing FULL public arXivv1 reused |
| V17 T06 | [B-Net: Learning Where to Compress in Byte-Level Language Models](https://openreview.net/forum?id=fMymbXoq9T) |20:20:16.031 | Official original unavailable; no lawful alternate established |
| V18 V11 | [LoopLA: Causal State Refinement for Looped Linear Attention](https://openreview.net/forum?id=xzOnjQHMr9) |16:56:32.122 | Official original unavailable; no lawful alternate established |
| V18 V16 | [Farsighted Correction of Shortcut Learning: From Dynamic Starvation to Confidence-Gap Optimization](https://openreview.net/forum?id=JrKJaRbQpz) |18:46:00.744 | Same source gap |
| V18 V20 | [Exact Finite-Query KV Cache Compilation](https://openreview.net/forum?id=OQhOBMNVeN) |20:43:32.295 | Same source gap; a later public paper's citation links this same forum, not a recovered original |
| V18 V21 | [Where You Put Attention Matters More Than How Much You Use: Attention Placement in Hybrid Sequence Models](https://openreview.net/forum?id=0fPxp7a50O) |17:03:20.090 | Same source gap |
| V18 V24 | [Predictive State Has a Scope](https://openreview.net/forum?id=uILf1c6VDo) |19:47:12.375 | Metadata PDF reference recovered; original still unavailable |
| Earlier V02 | [Linear Attention lacks Incentive for Associative Recall, not Capacity](https://openreview.net/forum?id=UUldzWxIL4) |21:07:52.098 | Still source-blocked; one new current PDF representative403 |
| Earlier V04 | [SDG: State-Dependent Gating at Chunk Boundaries for Linear Attention](https://openreview.net/forum?id=lYWcLB1rAh) |17:31:17.478 | Prior body gap retained; no new R3 PDF attempt |
| Earlier V13 | [Cross-Model Stitching Transfers Answers, Not Computation](https://openreview.net/forum?id=98Rbm5C5Bl) |20:42:15.522 | Same retained gap |
| Earlier V14 | [Receiver State Shapes Functional Compatibility: Internal Message Adaptation for Model Stitching](https://openreview.net/forum?id=2M4nt7AFuD) |20:56:50.283 | Same retained gap |
| Earlier V22 | [When Routing Must Be Right: Irreversible Lock-In in Attention Routing](https://openreview.net/forum?id=9vT48Lms48) |20:23:34.338 | Same retained gap |
| Earlier V25 | [Understanding the Predictive-State Bottlenecks of Transformer Models](https://openreview.net/forum?id=58JxyfvZJj) |18:06:02.727 | Same retained gap |

**One status control outside the17:** [Compiled Tokenizers](https://openreview.net/forum?id=CixpFoiooB) again returns `ICLR.cc/2027/Conference/Withdrawn_Submission`, notev2, modified **2026-11-08 10:45:24.749 UTC**, unchanged from R1/R2. Withdrawal-event date remains unknown; `mdate` is not that event date. No acceptance or scientific-invalidity inference. Search-indexed “under review” snippets must not override the returned withdrawal state.

## 5. Independent lawful-version discovery and exact source handoff

### Newly recovered T02: spelling refinement, not author matching

Starting from a public exact-title search, a spelling variant lead was followed to [arXiv2604.16037](https://arxiv.org/abs/2604.16037). The primary page and a separately retrieved official arXiv title query establish:

- Public title: **Stochasticity in Tokenisation Improves Robustness**.
- Requested/observed edition: **2604.16037v1**, posted **2026-04-17 13:05:46 UTC**; onlyv1 displayed in the fetched history.
- Its abstract closely matches the anonymous record's problem/setup, stochastic pretraining/fine-tuning, perturbation evaluation and claimed outcome language, with spelling/wording differences. Those are **bibliographic-content association facts**, not R3 validation of the scientific claims.
- No anonymous authors are identified. A near-matching title/abstract and a matching first page do not establish that the conference PDF contains the same experiments, appendices or revisions.

**Ordinary transient retry succeeded:** first HTTPS200 transfer timed out after120 seconds with488,570 of705,191 advertised bytes. The incomplete file was discarded. One clean ordinary redownload, unchanged verification/proxy behavior and240-second total limit, completed; no range trick, wall bypass or credential was used. This is an appropriate retry of an incomplete public transfer, not a retry loop through a403/challenge.

| Acquisition field | Verified value |
|---|---|
| Requested/effective URL | `https://arxiv.org/pdf/2604.16037v1` /same |
| Successful retrieval UTC |2026-11-09 11:46:47.396489 |
| Curl/HTTP/TLS/proxy |0 /200 /verification result0 /proxy_used0 |
| MIME/bytes | `application/pdf` /705,191 |
| SHA-256 | `cad655df35b4027b157bf5ee1482eb72e9ef490364933b48606b42db1ff13977` |
| Original saved | [R3_BR-R2-T02__2604.16037v1.pdf](source_staging/R3_BR-R2-T02__2604.16037v1.pdf) |
| Integrity/title | `%PDF-`, final`%%EOF`; existing `pdftotext` first-page parse exit0, British-spelling title found |
| Reading status | **ACQUIRED, NOT FULL**; first-page acquisition/title check only; no derived whole-text file or scientific table/proof reading |

**Terra handoff:** read this exact publicv1 independently, keeping the conference original BLOCKED. Recover sampling distribution/support, string preservation, perturbation permissions, clean negatives, exposure/sequence-length/compute matching and costs before any result-level use. The previous T02 card's bounded-search failure is historical; do not preserve it as “no public alternate exists,” and do not change it to FULL merely because the file now exists. R3 does not edit that card.

### Existing T03/T05 readings: reuse at their real editions

| Work | Primary public edition independently rechecked | Existing source/card actually reused | Permitted scope / unresolved relation |
|---|---|---|---|
| T03 | [arXiv2610.19139v1](https://arxiv.org/abs/2610.19139), posted2026-10-13 20:08:40 UTC; fetched history showsv1; title **Online Tokenization with Optimal Delay in Linear Time** | [V17 T03 card](../03_reading/V17/BR-R2-T03.md); existing PDF bytes/hash recomputed, SHA-256`86a4690df7f6a2a38243e157eac56b094047dc01ea155bd12e74212187078ce9` | Reuse its existing publicv1 FULL scope and caveats; no new read or copy. Anonymous forum title says **Near Linear Time**; matching abstract is not whole-edition equivalence |
| T05 | [arXiv2607.22334v1](https://arxiv.org/abs/2607.22334), posted2026-07-24 14:12:54 UTC; fetched history showsv1; same full title and closely matching abstract | [V17 T05 card](../03_reading/V17/BR-R2-T05.md); existing PDF SHA-256 recomputed`341d34838d7c76b9ae9449f0ab169cf8d20822be0012297413aaff220b73a949` | Reuse exact publicv1 FULL card; do not write “official submission fully read” or merge EOT/prefix-probability conditions across papers |

T03/T05 source files remain in their existing V17 folder. They were not duplicated into R3 staging or counted as new acquisitions. Their source-level reading restrictions travel with any scientific synthesis; this audit neither re-proves nor newly adjudicates their results.

### Negative searches and a citation lead that did not recover the original

- Independently issued **18 bounded WebSearch queries**: the six interface titles/phrases; the British T02 spelling refinement; all five V18 titles/phrases; and all six earlier blocked titles. Exact strings are in the manifest. Only publicly returned title/content associations were followed; no author/profile searching or name triangulation.
- Independently issued **15 individual official arXiv title queries**, `start=0,max_results=5`: five V18 titles, six old titles, and T01/T02-British/T04/T06. All returned valid Atom with curl0 and empty stderr. Fourteen reported0 matches; the British T02 query reported exactly1, the recoveredv1. This is not a field census or proof that alternate titles/other legal repositories contain no copy.
- WebSearch re-found the already-read public T03/T05 preprints. T01/T04/T06, the five V18 works and the earlier six had no eligible original/alternate established by this pass. Search snippets from official PDFs, aggregators, generated reviews or acceptance-prediction sites were **not** paper-reading or decision evidence.
- An exact V20 search found a public later paper, [arXiv2610.36520v1](https://arxiv.org/html/2610.36520v1). A normal FetchURL network failure received one exact retry; the retry succeeded. Only the bibliography/target-title location was inspected: reference[2] names *Exact Finite-Query KV Cache Compilation*, lists it anonymously and links **the same OpenReview forum OQhOBMNVeN**. It supplies neither an alternate original nor permission to identify its authors. No new reading credit, theorem/result endorsement, or source substitution comes from that citation.

## 6. Consequence for the final recent-literature conclusions

The core risk is **access-conditioned evidence selection**: accessible preprints could appear to win against unread competing mechanisms simply because their limitations and experiments are visible. Source unavailability is not a negative experimental result, evidence of low quality, redundancy, or irrelevance. The review must retain these alternatives and their original broad questions.

| Unclosed source family | What the final report may safely say now | What cannot be claimed from the available source scope | Required evidence before upgrade |
|---|---|---|---|
| T01 formal tokenization optimization | A verified2027 submission proposes an optimization/certification approach; list it as an abstract-screened competing objective | That its guarantees establish predictive/task sufficiency, outperform learned interfaces, or close rate/content tradeoffs | Exact objective/constraints, assumptions, bounds, solver scale/cost, baselines and any downstream tests from an original |
| T02 stochastic tokenization | A lawful independentv1 has been acquired and is awaiting reading; the submission abstract motivates an interface-training alternative | A robust causal improvement or cost-neutral solution established by this review; acquisition is not validation | Terra's exact-edition full read, perturbation/string/exposure controls, clean-task and resource negatives |
| T04 tokenization invariance/head localization | A verified anonymous source raises a trunk-versus-head/learning-time hypothesis | That output heads are generally the bottleneck, internal semantic content survives retokenization, or head-only repair is the recommended fix | Probe/pooling/random-direction controls, task specificity, timeline, exact likelihood definitions, matched adaptation and failures |
| T06 B-Net | A verified source proposes separating boundary scoring from compression-rate control | That its controller is prefix-safe, realizes online rate constraints without future information, or proves a superior learned-boundary architecture | Controller timing/visibility, realized boundaries and rate, objective, supervision, same-data/compute/state controls and language negatives |
| V11 loop-state refinement | An abstract-screened alternative to changing source storage exists | Free or generally superior gains from extra iterations; safe causal/chunk semantics or matched-cost superiority | Original method/approximation, state commits, visibility, equal-FLOP and all-resource/quality comparisons |
| V16 shortcut correction | A verified source proposes counterfactual/confidence-gap objectives | General dynamic-starvation/proxy theorems, deep-model causal repair, or target-project diagnosis | Exact assumptions/proofs, label/group/counterexample permissions, controls, budgets and negative cases |
| V20 finite-query compilation | A verified source studies finite protected-query exactness; it remains a distinct sufficiency question | Unknown-future-query preservation, whole-language exact memory, a certified deployed compression gain, or a theorem verified here | Original quantifiers, key realizability/rank, protected-query visibility, numerical precision and out-of-query behavior |
| V21 attention placement | A verified source compares component arrangement rather than only quantity | That one layout universally wins, or terminal ablation alone proves formation-time causal dependence | Original tasks, placement controls, equal budgets, seeds, removal/repair design and architecture limits |
| V24 predictive state scope | A verified source studies pair-addressed temporal-graph histories; keep it distinct from fixed-total-memory language modeling | A source-free fixed-state cure, a universal content/address causal result, or equal-total-bit advantage | Exact address/state cardinality, update/read permissions, derangement controls and costs/transfer scope |
| Earlier Incentive/SDG/Routing/Belief-rank sources | Preserve incentive, memory-feedback, formation timing and predictive-rank alternatives as metadata-only research leads | Capacity is not limiting, a new gate is causally sufficient, early lock-in is generally irreversible, or low-variance modes are causally discarded in language models | Original task generators, controls, capacity/precision/visibility/budget accounting, assumptions, negative results and held-out tests |
| Earlier two stitching sources | Preserve donor-answer transfer and receiver-state repair as separately posed transfer questions | That all successful stitches transfer answers rather than computation, or a receiver adapter proves general component portability | Original donor/receiver/answer-visibility permissions, self/random/source controls, adaptation and held-out budgets, scope-specific failures |

This table is an **evidence-permission audit**, not a conclusion that the blocked authors' results are wrong. “Requires paper reading” does not imply that full reading alone will prove the proposed mechanism or settle FLUED; target-project causal/empirical questions remain separate.

### Safe deliverable now

The authors can deliver a clearly labeled **qualified broad synthesis** containing:

1. Mechanism/resource/control comparisons supported by **already completed exact-version full cards**, with their recorded failures, limits and modality distinctions. Reused classics/public preprints do not receive new counts.
2. A separate **ICLR2027 official-response source index**: exact domain/forum/state snapshot, anonymity preserved, note version distinct from paper edition, explicit access/reading status. This audit supports identities/status snapshots, not acceptance or conference-wide coverage.
3. An explicitly tagged **metadata/abstract candidate frontier** for unread recent works, including blocked alternatives rather than excluding them. Mechanism descriptions must remain author-attributed, not reported as body-verified results or scored equally with fully read originals.
4. A **source-gated research matrix**: competing hypotheses and the controls needed to distinguish them, without selecting an architecture or asserting a latest-literature winner on unread evidence.
5. The two public V17 full cards at their independent editions, plus the new T02 acquired-source handoff marked **unread**. No official-manuscript equivalence asserted.
6. A concrete unresolved queue listing the17 official originals, three candidate public-edition relationships,14 works without an alternate established, and the specific recent claims that cannot yet be closed.

**Unsafe completion wording:** “all recent key originals have been read,” “ICLR2027 coverage complete,” “latest studies establish the recommended architecture,” “the blocked alternatives offer no counterevidence,” “official PDFv2 was fully read,” or any acceptance prediction/inference. Do not quietly downgrade the intended deliverable to a merely bibliographic report and call the original full-reading objective complete. The main coordinator must retain the gap visibly and, where completion requires those originals, state that the recent-result adjudication remains open.

### Suggested disclosure for the English final report

> Our recent-ICLR source index is based on official public metadata snapshots, not acceptance decisions. Seventeen selected conference originals remain unavailable through the ordinary public routes tested. Two related public preprints have version-scoped full-reading cards; a third candidate edition has been acquired but remains unread. We therefore separate body-supported synthesis from abstract-screened recent leads and do not use the unavailable works to certify a mechanistic or architectural ranking. Title/abstract associations do not establish anonymous-author identity or manuscript equality. Coverage is bounded, and current-source adjudication remains incomplete.

The17 is this audit's **selected cohort**, not the count of every blocked paper across the entire research project. Update it only when the owner has a reconciled source/read ledger, not by adding overlapping reading-batch/source counts.

## 7. Retry discipline, audit receipt, and remaining work

### Bounded request ledger

- **Eight normal OpenReview curl requests** in R3: four initial representative GETs (three PDFs and one note API), one forum GET, one resolved V24 PDF GET, one bounded repeated B-Net PDF GET for error-body confirmation, and one metadata-linked attachment HEAD. Four PDF paths/locator forms were exercised, with one repeated content path; this is **not** eleven/seventeen per-paper retests.
- **Eighteen official search calls**: each of the17 selected forums plus the Compiled Tokenizers status control; one result requested/returned per query, no pagination or venue enumeration.
- **Eighteen WebSearch calls** and **fifteen arXiv title-API calls**, exact public titles/phrases only; bounded ranked results or first five requested, no all-field completeness claim. No second academic aggregator/data-source identity linkage was used.
- Three public arXiv abstract/history pages checked: T02/T03/T05. One derivative citation-location HTML route: a network failure then one exact normal retry, bibliography-only use.
- T02 original download: one partial timeout then one clean ordinary successful retry, both receipts retained. No repeated403/challenge download loop. No new full-paper reading.

The [R3_manifest.json](source_staging/R3_manifest.json) records exact query URLs, returned title/forum/venueid/version/modification fields without author/profile data, representative access receipts, public source histories/searches, the failed and successful download attempts, and existing-source hash reuse. It does not claim to be a raw complete venue archive.

### Files authored and validation

Only these R3-owned paths were added:

- `docs/research/flued_broad_research_v2/05_review/ICLR2027_SOURCE_AUDIT_R3.md`
- `docs/research/flued_broad_research_v2/05_review/source_staging/R3_manifest.json`
- `docs/research/flued_broad_research_v2/05_review/source_staging/R3_BR-R2-T02__2604.16037v1.pdf`

A foreground validator checks strict JSON/UTF-8,18 unique official metadata IDs with17 submission/one withdrawn state, the17-row selected-source table,18 official query/18 web query/15 arXiv query receipts, six initial representative plus two additional diagnostic records, two download-attempt receipts with exactly one complete new PDF, SHA-256/byte length/signature/EOF, first-page parser/title receipt, existing T03/T05 hashes, local Markdown targets and absence of `.part` files. Git status and whitespace checks are inspected; untracked-file direct validation matters because an empty tracked diff alone is insufficient. No project build/test/training applies to this source/documentation audit.

**Still open:** all17 official manuscript bodies and their exact edition histories; PDF-specific root cause/permissions versus verification attribution; T02 full reading; body-equivalence checks for all three candidate preprints; eligible originals/alternates for the14 remaining works; supplements; direct decisions/review contents and exact withdrawal-event dates; uninspected discovery results; and final recent-result claims listed in §6. The source audit and bounded retry task can be handed off, but **the underlying recent-original reading and result-adjudication objective is not complete**.
