# Independent ICLR 2027 venue and source audit

**Audit date:** 2026-11-09, Asia/Shanghai. **Assigned artifact:** this file only. **Scope:** source identity, official venue/state, version provenance, access limitations, and reading requirements. This is not a mathematical-results review, a new full-reading batch, an acceptance prediction, or a venue census.

## 1. Executive finding and counts

**24 previously claimed conference records were independently returned by the official public OpenReview search API:** all 14 A07 venue-register entries (N01–N13 plus BIW-0103), seven selected A08 active-register entries, and its three status controls. Their API-observed states are **20 active submissions, three withdrawn submissions, and one desk-rejected submission**. One additional relevant active submission was recovered while checking a name collision; it is separate from the 24-record audit denominator. One same-title workshop record was checked as a venue control, not an extra ICLR paper.

- **Material status correction:** Compiled Tokenizers (`CixpFoiooB`) is returned as **Withdrawn_Submission**, with note last-modified date **2026-11-08 UTC**. A07's earlier indexed submission association is genuine, but its current-state-unknown field must not remain the latest source status after this audit. This is a later metadata recovery, not evidence that A07 invented the record.
- **Source upgrades, not reading upgrades:** every A07 official-PDF-only/indexed forum lead now has a matching official API record in the correct conference domain. Their methods/results do not become paper-read or independently verified through this recovery.
- **Year/venue separation:** 2026 submission timestamps and BibTeX `year=2026` are compatible with **ICLR 2027**. Turnip's separate **ODI 2026 Poster** is not the conference decision. TokSuite is formally **ICML 2026**, not a verified ICLR 2027 submission.
- **Version correction:** OpenReview note `version:2` is not arXiv v2 or proof of a second PDF edition. Scratchpad Patching has a genuine **arXiv v2, 2026-11-06**; the existing full card remains **v1, 2026-05-10**. Selected v2 changes were independently checked, including a new visual recovery of **Table 4**.
- **Unclosed:** live thread/decision replies, withdrawal-event timestamps, complete submission revision histories, paper-body equivalence across repositories, and venue-wide coverage. **Zero new full-paper readings; zero ICLR 2027 acceptances established.**

The remaining **18 of A08's 25 active-register records were not independently rechecked here**. Their A08 evidence is not invalidated, but this audit does not certify that entire table. Counts above are forum records, not unique scientific works or total field coverage.

## 2. Inputs, access boundary, and venue identity

### Local inputs actually inspected

Read [PLAN](../PLAN.md), A07/A08 [search logs](../01_discovery/A07/SEARCH_LOG.md), [A08 log](../01_discovery/A08/SEARCH_LOG.md), and both [work registers](../01_discovery/A07/WORKS_AND_PROBLEMS.md), [A08 register](../01_discovery/A08/WORKS_AND_PROBLEMS.md). Also read A07 coverage and handoff; the existing [BIW-0076 full v1 card](../../byte_language_interface_survey/03_reading/R05/BIW-0076.md), selected saved v1 original passages, and the existing [BIW-0103 full v1 card](../../byte_language_interface_survey/03_reading/R06/BIW-0103.md). Exact-title/stable-ID catalog searches supported only the specific dedup checks stated below, not an all-card audit.

### Independently retrieved official context

1. [ICLR 2027 CFP](https://iclr.cc/Conferences/2027/CallForPapers): abstract deadline 2026-09-18 AOE; paper deadline 2026-09-25 AOE; reviews 2026-11-05; discussion 2026-11-05–18; final decisions **planned for 2026-12-16**. Schedule is context, not any paper's decision.
2. [Official group JSON](https://api2.openreview.net/groups?id=ICLR.cc/2027/Conference): `count=1`, `id=domain=ICLR.cc/2027/Conference`, `readers=[everyone]`, `public_submissions=true`, and `fromCache=true`. It registers:
   - submission invitation `ICLR.cc/2027/Conference/-/Submission`;
   - active venue ID `ICLR.cc/2027/Conference/Submission`;
   - withdrawn venue ID `ICLR.cc/2027/Conference/Withdrawn_Submission`;
   - desk-rejected venue ID `ICLR.cc/2027/Conference/Desk_Rejected_Submission`;
   - rejected venue ID `ICLR.cc/2027/Conference/Rejected_Submission`.
   Public-withdrawn/public-desk-rejected flags and separate UI tabs are configured. Accepted-option strings in group configuration are workflow choices, not decisions.
3. Built-in Desktop browser, existing group tab `panel-tab-286`, document text snapshot `text-bfcd242c-a16f-419e-a11d-c0979dacabe8`: navigation, **Loading**, footer; 13 blocks, no submission metadata, no continuation. A page title/group shell is not an enumerated list.

### Normal direct-route tests and stop rule

| Exact normal route | Result in this audit | Handling |
|---|---|---|
| `https://api2.openreview.net/notes?id=b3lZofUyGC` | “Complete the check below to continue to OpenReview” | Tested once; direct-note access logged blocked; no retry/bypass |
| `https://openreview.net/forum?id=CixpFoiooB` | Same verification challenge | Tested once; no challenge interaction or login |
| Official public `/notes/search` queries in §4 | Usable JSON metadata/abstract records | Read publicly returned fields; do not represent this as access to blocked threads/PDFs |
| `https://arxiv.org/html/2605.09630v2` | First FetchURL network failure; one exact retry succeeded, long extracted body | Selected passages read, not entire body |
| Scratchpad v2 built-in-browser screenshot after scrolling | One `PAGE_NOT_READY`; one capture retry succeeded | Visual Table 4 check, not a PDF/full-paper read |

No credentials, private sessions, CAPTCHA solving, challenge bypass, alternate-IP routing, installs, training, subagents, commits, or registry edits. The available data-source skill was consulted: it offers no OpenReview source; no data-source API/OAuth-backed lookup was invoked. Official public HTTP metadata supplied the venue evidence directly. No public review text was read. No PDF was manually downloaded. Automatic tool text/screenshot receipts are session infrastructure, not extra authored project artifacts.

## 3. Record-level official metadata audit

### Common fields and limits applying to every row below

Each record was actually returned, not inferred from a search-engine snippet. Checked fields: exact `title`, `id == forum`, `domain`, `readers`, submission invitation, submission `number`, `content.venueid`, `content.venue`, `cdate/tcdate`, `mdate/tmdate`, `version`, and `content.pdf` reference. All 24 have `domain=ICLR.cc/2027/Conference`, `readers=[everyone]`, the conference submission invitation, and **note `version=2`**. For each inspected record, `cdate=tcdate` and `mdate=tmdate`.

**Version for every row:** official note v2; current PDF edition number/date **unknown**. A returned content-addressed PDF pathname identifies a metadata reference, not proof that those bytes were retrieved, hashed, fully read, or equal to arXiv. Most search responses say `fromCache=true`; PriorBPB, ByteMark, and Selective but Not Broad responses omit that flag. Omission is not `false`. These are **official API-observed states at the audit snapshot**, not a guarantee of uncached/live-thread completeness.

`Active` below expands to both `content.venueid=ICLR.cc/2027/Conference/Submission` and `content.venue=ICLR 2027 Conference Submission`. `Withdrawn` and `Desk rejected` expand to the corresponding exact IDs in §2 and human-readable venue labels. **Decision-reply content was not retrieved for any row.** Active is not accepted; withdrawal/desk rejection is not a scientific falsification. Dates are **UTC**, not silently converted to AOE or local time. `Created` means the returned note creation date, not necessarily final PDF upload time.

### A07: all 14 claimed venue records

| Audit key / A07 key | Exact official title and forum | Submission # | Created UTC | API-observed state; note last modified UTC | Audit disposition |
|---|---|---:|---|---|---|
| Q01 / N01 | [Turnip: Tokenizers Are Secretly Context Compressors for Transformers](https://openreview.net/forum?id=tlYzFXxkji) | 49442 | 2026-09-18 | Active; 2026-10-05 21:04:18.008 | Indexed association upgraded to official metadata; workshop kept separate |
| Q02 / N02 | [MRT: Regularizing Tokenization with Morphology for Low-Resource Indic Languages](https://openreview.net/forum?id=tKqgR3uW7u) | 22052 | 2026-09-15 | Active; 2026-10-05 19:51:44.046 | Previously PDF-only lead now has a verified forum/domain |
| Q03 / N03 | [SEPARATING SCRIPT AND VOCABULARY EFFECTS IN MULTILINGUAL TOKENIZATION COST](https://openreview.net/forum?id=FPNRyuXJC0) | 39838 | 2026-09-18 | Active; 2026-10-05 20:39:48.550 | Preserve official uppercase title; capitalization is not another entity |
| Q04 / N04 | [Compiled Tokenizers: Training Language Models on Schema-Specific Action Spaces](https://openreview.net/forum?id=CixpFoiooB) | 7019 | 2026-08-31 | **Withdrawn; 2026-11-08 10:45:24.749** | Material current-state update; withdrawal event date remains unverified |
| Q05 / N05 | [PriorBPB: Reducing the Target Length Confound of Bits-per-Byte While Improving Accuracy Prediction](https://openreview.net/forum?id=kB8Lwd90Io) | 47880 | 2026-09-18 | Active; 2026-10-05 21:00:26.926 | API confirms **Target Length**; indexed PDF/blog **Answer Length** relation still unresolved |
| Q06 / N06 | [ByteMark: A Unified Byte-Level Watermark for Detection Across Language Models](https://openreview.net/forum?id=losZJYZ6xK) | 43860 | 2026-09-18 | Active; 2026-10-05 20:50:26.818 | Metadata upgrade only; separate arXiv v1 is not the forum PDF's certified edition |
| Q07 / N07 | [Why Pretraining Fails to Share Cross-Lingual Knowledge](https://openreview.net/forum?id=A4XoBLOXvg) | 4637 | 2026-08-25 | Active; 2026-10-05 17:11:25.120 | Earlier forum date than arXiv is not a contradiction |
| Q08 / N08 | [Who Gets a Token, and What Does It Carry? Unequal Name Support and Concept Access in Large Language Models](https://openreview.net/forum?id=NpBoc9jkFs) | 27599 | 2026-09-17 | Active; 2026-10-05 20:06:07.961 | Previously PDF lead now official forum metadata; no causal-result upgrade |
| Q09 / N09 | [GlitchPatch: Repairing Glitch Tokens in Frozen Language Models via Local Retokenization](https://openreview.net/forum?id=DbzLzs5VL7) | 28236 | 2026-09-17 | Active; 2026-10-05 20:07:51.969 | Distinguish different GlitchPatch method name in §5 |
| Q10 / N10 | [Learning to Retokenize: Improving Downstream Performance of Frozen Language Models](https://openreview.net/forum?id=vfj1rb7yk1) | 34899 | 2026-09-17 | Active; 2026-10-05 20:24:40.427 | Official abstract recovered; policy estimator/results still require paper |
| Q11 / N11 | [BridgeSTOP: Bridging Streaming Tokenization and LLM Prefill](https://openreview.net/forum?id=gbaS4smhnV) | 8108 | 2026-09-02 | Active; 2026-10-05 17:44:12.401 | Official identity/abstract recovered; serving claims not independently audited |
| Q12 / N12 | [LEAD: Models Know the Language, but Token Preferences Do Not Always Follow](https://openreview.net/forum?id=s2yS6VAWIP) | 22030 | 2026-09-15 | Active; 2026-10-05 19:51:38.996 | Abstract supplies **Language Evidence-Aware Decoding**; no need to invent acronym expansion |
| Q13 / N13 | [Constructive Prediction: The Role of Lexical Code Organization in Language Modeling](https://openreview.net/forum?id=DXrf6mhnGR) | 2886 | 2026-08-22 | Active; 2026-10-05 17:02:30.793 | Title-only lead now metadata/abstract-screened; not FULL or theorem-certified |
| Q14 / BIW-0103 | [Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models](https://openreview.net/forum?id=O1JpRRUeGW) | 49116 | 2026-09-18 | Active; 2026-10-05 21:03:33.030 | Reuse existing **2609.12303v1** card; forum-paper equivalence remains unproved |

### A08: seven active records plus three status controls

| Audit key / A08 key | Exact official title and forum | Submission # | Created UTC | API-observed state; note last modified UTC | Audit disposition |
|---|---|---:|---|---|---|
| Q15 / V01 | [How Linear Attention Remembers](https://openreview.net/forum?id=b3lZofUyGC) | 29987 | 2026-09-17 | Active; 2026-10-05 20:12:17.082 | A08 identity/status confirmed at metadata level |
| Q16 / V02 | [Linear Attention lacks Incentive for Associative Recall, not Capacity](https://openreview.net/forum?id=UUldzWxIL4) | 50948 | 2026-09-19 | Active; 2026-10-05 21:07:52.098 | UTC date does not establish an AOE-deadline violation |
| Q17 / V05 | [Fast Weights in Fast Weights: Towards Bridging Parallel and Sequential Test-Time Learning](https://openreview.net/forum?id=bZXUddyKmp) | 34679 | 2026-09-17 | Active; 2026-10-05 20:24:13.998 | Abstract includes literal unexpanded LaTeX; do not reconstruct a missing method name |
| Q18 / V07 | [On State Reduction in Linear Attention](https://openreview.net/forum?id=3uKKt21Vry) | 49833 | 2026-09-18 | Active; 2026-10-05 21:05:08.928 | W0086 candidate identity; no second-work count by title change |
| Q19 / V13 | [Cross-Model Stitching Transfers Answers, Not Computation](https://openreview.net/forum?id=98Rbm5C5Bl) | 40828 | 2026-09-18 | Active; 2026-10-05 20:42:15.522 | Metadata confirmed; scientific interpretation still abstract-level |
| Q20 / V20 | [Exact Finite-Query KV Cache Compilation](https://openreview.net/forum?id=OQhOBMNVeN) | 41337 | 2026-09-18 | Active; 2026-10-05 20:43:32.295 | Metadata confirmed, not a proof check |
| Q21 / V24 | [Predictive State Has a Scope](https://openreview.net/forum?id=uILf1c6VDo) | 20416 | 2026-09-15 | Active; 2026-10-05 19:47:12.375 | Metadata confirmed; temporal-graph domain remains explicit |
| Q22 / status control | [Spectral Polynomial Linear Attention (SPLA): polynomial singular-value maps for gated linear models](https://openreview.net/forum?id=PnohHgtyLv) | 13057 | 2026-09-10 | **Withdrawn; 2026-11-06 15:51:16.375** | A08 state/modification date confirmed; withdrawal-event timestamp unknown |
| Q23 / status control | [Selective but Not Broad: Retrieval Capacity and Accessibility in State-Space Models](https://openreview.net/forum?id=8EzQDRLyfM) | 2754 | 2026-08-21 | **Withdrawn; 2026-11-06 13:21:30.681** | A08 state/modification date confirmed; withdrawal-event timestamp unknown |
| Q24 / status control | [The Geometry of Fast and Slow Weights In A Shared Address Space](https://openreview.net/forum?id=b3OUmaj4gm) | 26724 | 2026-09-16 | **Desk rejected; 2026-10-15 08:48:22.686** | A08 state/modification date confirmed; decision reasons/event not retrieved |

### Withdrawal-date precision: do not substitute `mdate` for the event

| Forum | Raw returned `mdate=tmdate` (Unix milliseconds) | What is verified | Exact withdrawal/desk-rejection event date |
|---|---:|---|---|
| CixpFoiooB | 1794134724749 | Withdrawn status; last modified 2026-11-08 UTC | **Unknown**: no withdrawal reply/edit history retrieved |
| PnohHgtyLv | 1793980276375 | Withdrawn status; last modified 2026-11-06 UTC | **Unknown** |
| 8EzQDRLyfM | 1793971290681 | Withdrawn status; last modified 2026-11-06 UTC | **Unknown** |
| b3OUmaj4gm | 1792054102686 | Desk-rejected status; last modified 2026-10-15 UTC | **Unknown** |

Write “withdrawn; note last modified [date]; withdrawal-event date unavailable,” not “withdrew on [date].” In each case the matching status invitation is present, but invitation membership contains no event timestamp. Receipt on November 9 establishes that the API exposed the state on this audit date; cache uncertainty prevents a stronger live-history claim.

## 4. Executed official search queries and coverage accounting

Each Q key below is an audit identifier, **not chronological execution order**. The precise template used was:

```text
https://api2.openreview.net/notes/search?term=<percent-encoded quoted text>&group=ICLR.cc/2027/Conference&limit=<n>&offset=<k>
```

Terms include literal double quotes (`%22`); spaces were `%20`, colons `%3A`, commas `%2C`. No sort parameter, author query, credentials, or hidden pagination. Query success alone was insufficient: returned domain, forum, title and status were inspected per row.

| Key | Exact term including quotes | limit,offset | Returned records/count |
|---|---|---|---|
| Q01 | `"Turnip: Tokenizers Are Secretly Context Compressors for Transformers"` | 1,0 | tlYzFXxkji; count1 |
| Q02 | `"MRT: Regularizing Tokenization with Morphology for Low-Resource Indic Languages"` | 1,0 | tKqgR3uW7u; count1 |
| Q03 | `"Separating Script and Vocabulary Effects in Multilingual Tokenization Cost"` | 1,0 | FPNRyuXJC0; count1 |
| Q04 | `"Compiled Tokenizers: Training Language Models on Schema-Specific Action Spaces"` | 1,0 | CixpFoiooB; count1 |
| Q05 | `"PriorBPB"` | 2,0 | kB8Lwd90Io; count1 |
| Q06 | `"ByteMark: A Unified Byte-Level Watermark for Detection Across Language Models"` | 1,0 | losZJYZ6xK; count1 |
| Q07 | `"Why Pretraining Fails to Share Cross-Lingual Knowledge"` | 1,0 | A4XoBLOXvg; count1 |
| Q08 | `"Who Gets a Token, and What Does It Carry"` | 1,0 | NpBoc9jkFs; count1 |
| Q09 | `"GlitchPatch"` | 1,0 **and 1,1** | DbzLzs5VL7 then Rvz6kIZAcg; count2 on both pages; both inspected |
| Q10 | `"Learning to Retokenize: Improving Downstream Performance of Frozen Language Models"` | 1,0 | vfj1rb7yk1; count1 |
| Q11 | `"BridgeSTOP: Bridging Streaming Tokenization and LLM Prefill"` | 1,0 | gbaS4smhnV; count1 |
| Q12 | `"LEAD: Models Know the Language, but Token Preferences Do Not Always Follow"` | 1,0 | s2yS6VAWIP; count1 |
| Q13 | `"Constructive Prediction: The Role of Lexical Code Organization in Language Modeling"` | 1,0 | DXrf6mhnGR; count1 |
| Q14 | `"Breaking the Token Ceiling"` | 1,0 | O1JpRRUeGW; count1 |
| Q15 | `"How Linear Attention Remembers"` | 1,0 | b3lZofUyGC; count1 |
| Q16 | `"Linear Attention lacks Incentive for Associative Recall, not Capacity"` | 1,0 | UUldzWxIL4; count1 |
| Q17 | `"Fast Weights in Fast Weights"` | 1,0 | bZXUddyKmp; count1 |
| Q18 | `"On State Reduction in Linear Attention"` | 1,0 | 3uKKt21Vry; count1 |
| Q19 | `"Cross-Model Stitching Transfers Answers, Not Computation"` | 1,0 | 98Rbm5C5Bl; count1 |
| Q20 | `"Exact Finite-Query KV Cache Compilation"` | 1,0 | OQhOBMNVeN; count1 |
| Q21 | `"Predictive State Has a Scope"` | 1,0 | uILf1c6VDo; count1 |
| Q22 | `"Spectral Polynomial Linear Attention"` | 1,0 | PnohHgtyLv; count1 |
| Q23 | `"Selective but Not Broad"` | 1,0 | 8EzQDRLyfM; count1 |
| Q24 | `"The Geometry of Fast and Slow Weights In A Shared Address Space"` | 1,0 | b3OUmaj4gm; count1 |

Direct reproducibility examples actually fetched:

- [Q04, Compiled Tokenizers](https://api2.openreview.net/notes/search?term=%22Compiled%20Tokenizers%3A%20Training%20Language%20Models%20on%20Schema-Specific%20Action%20Spaces%22&group=ICLR.cc/2027/Conference&limit=1&offset=0)
- [Q09 page 0](https://api2.openreview.net/notes/search?term=%22GlitchPatch%22&group=ICLR.cc/2027/Conference&limit=1&offset=0) and [page 1](https://api2.openreview.net/notes/search?term=%22GlitchPatch%22&group=ICLR.cc/2027/Conference&limit=1&offset=1)
- [Q15, How Linear Attention Remembers](https://api2.openreview.net/notes/search?term=%22How%20Linear%20Attention%20Remembers%22&group=ICLR.cc/2027/Conference&limit=1&offset=0)
- [Q23, withdrawn control](https://api2.openreview.net/notes/search?term=%22Selective%20but%20Not%20Broad%22&group=ICLR.cc/2027/Conference&limit=1&offset=0)
- Cross-venue control: [same exact quoted Turnip title, **no group parameter**, limit5, offset0](https://api2.openreview.net/notes/search?term=%22Turnip%3A%20Tokenizers%20Are%20Secretly%20Context%20Compressors%20for%20Transformers%22&limit=5&offset=0), returned exactly two records: tlYzFXxkji and He8w9GBiKF, count2.

Thus **26 public search requests** were executed: 24 initial record queries, one GlitchPatch continuation, and one Turnip cross-venue control. They expose **25 distinct conference forums** (24 claimed + one newly screened) and one workshop forum; Turnip's repeated conference return is not another record. Only GlitchPatch required a second page, and its reported two matches were both inspected. This completes that narrow returned query, **not the venue or the topic**. No venue enumeration was attempted in this audit; earlier A07/A08 enumeration failures remain gaps, not successful pages inherited here. No external WebSearch snippets were needed for these independent confirmations.

## 5. Year collisions, version duplicates, and one relevant missed record

### Turnip: same title, different official venue records

The cross-venue official search returns:

- `tlYzFXxkji`: domain `ICLR.cc/2027/Conference`, venue ID ending `/Submission`, anonymous conference record, note v2.
- `He8w9GBiKF`: domain `NeurIPS.cc/2026/Workshop/ODI`, venue ID `NeurIPS.cc/2026/Workshop/ODI`, venue label **ODI 2026 Poster**, note v2, and a different PDF reference.

This corroborates A07's warning. The workshop label belongs only to its own record; do not transfer it to the anonymous conference forum, merge PDF editions, or count two scientific works merely because two forums exist. Public workshop author fields were not reproduced or used to identify anonymous conference authors. Conference BibTeX's `year=2026` is a submission-year field, not evidence that its venue is ICLR 2026.

### TokSuite: wrong-year/venue hazard correctly excluded by A07

[Official PMLR record](https://proceedings.mlr.press/v306/altintas26a.html), independently fetched, identifies **Proceedings of the 43rd International Conference on Machine Learning**, PMLR **306:2134–2179, 2026**, title *TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior*. Calendar/navigation keyword matches do not create an ICLR 2027 forum. Retain its existing version-scoped card for science; this formal metadata check is not another paper read.

### Existing W0086: title evolution is not a new entity

Old catalog row W0086 already maps **arXiv:2602.04852** to *On State Reduction in Linear Attention*, with earlier title *The Key to State Reduction in Linear Attention: A Rank-based Perspective*. Independently fetched [v3 abstract/history](https://arxiv.org/abs/2602.04852v3) lists v1 2026-02-04, v2 2026-02-12, v3 **2026-09-29**. Q18 matches the current title and closely related abstract, but **body/version equality is not established**. Keep the candidate mapping and do not allocate a duplicate work from the old title or from note version2. Named arXiv authors are not attached to the anonymous forum.

### PriorBPB and existing byte cards: preserve edition boundaries

- Q05 independently confirms **Target Length** in current returned forum metadata. A07's **Answer Length** PDF/blog wording remains a version/title discrepancy, not a separately established new paper. Its workshop locator `fiMZJJzZ7g` is inherited from A07, **not independently fetched here**. No assertion that blog, workshop, conference PDF and forum metadata are byte-identical.
- BIW-0103's full card is **2609.12303v1**. Its exact title and substantive abstract support a provisional source association with Q14, not paper-body equivalence. Reuse the card within v1 scope; do not relabel it “OpenReview PDF fully read” or count another FULL.
- A07 records the Multi-Token→Multi-Byte title transition for **2511.11346v1→v2**. This audit does not freshly verify that history; retain the existing fixed-v2 card/provenance rather than duplicating the entity or claiming another independent check.

### One additional source-screened record: a GlitchPatch method-name collision

[Echoing Is Not All You Need: Semantically Guided Repair of Glitch Tokens](https://openreview.net/forum?id=Rvz6kIZAcg), returned on Q09 offset1, is **not** the local-retokenization paper `DbzLzs5VL7`.

- Exact official fields: `id=forum=Rvz6kIZAcg`, domain `ICLR.cc/2027/Conference`, submission **57049**, readers everyone, conference submission invitation, `content.venueid=ICLR.cc/2027/Conference/Submission`, venue label **ICLR 2027 Conference Submission**, note version2, created **2026-09-19 07:55:52.337 UTC**, modified **2026-10-05 21:20:09.899 UTC**; PDF metadata reference `/pdf/fdf41aa132eeabec6194e644393cbef71c9a92c8.pdf`. Decision replies/PDF edition unknown.
- **Abstract-level problem/approach only:** distinguish echo repair from functional/semantic token use; its abstract calls its framework **GlitchPatch** but describes output-head-row correction and selective shared-adapter learning, unlike Q09's local input retokenization. No numeric repair rate or method superiority is adopted here.
- Exact title/ID searches found no match in the two old identity catalogs (`byte_language_interface_survey/02_inventory/WORK_CATALOG.md` and `flued_multigranularity_survey_20261108/02_catalog/CATALOG.md`). That supports a catalog gap only, not novelty or absence from all discovery streams.
- **Action:** candidate source/reading handoff for the catalog owner; keep separate forum/title and method-mechanism fields. Full paper needed for semantic-assessment criteria, correction versus adapter permissions, context/target leakage, old-vocabulary collateral tests, and total adaptation/inference cost. No source registry was edited.

This is one additional active forum, not another version of the retokenization paper and not new FULL credit. The collision demonstrates why a method name or search count cannot be the dedup key.

## 6. Scratchpad Patching v1→v2 evidence audit

### Provenance and reading scope

[arXiv history](https://arxiv.org/abs/2605.09630) independently returns **v1 2026-05-10 16:18:22 UTC** and **v2 2026-11-06 17:01:55 UTC**. The existing BIW-0076 card explicitly covers v1 §§1–7/Appendices A–E, pp.1–23; it is reused, not reread for another FULL. Saved v1 original text was inspected around B.3, C.2, D and H-Net demonstration passages; exact searches for `500M`, `100B`, `Table 4`, seed/latency and the four explicit FLOP multipliers did not recover those additions. This is targeted comparison, not an exhaustive redline or proof of every omission.

Selected [v2 primary HTML](https://arxiv.org/html/2605.09630v2) passages independently inspected: §4.2, §4.3, §7 limitations, B.3, C.2/Table4 caption, D, E.2–E.4. The extraction omitted Table4 cells. A built-in-browser visit to [C.2](https://arxiv.org/html/2605.09630v2#A3.SS2), followed by one scroll, **visually recovered all twelve cells**, screenshot `visual-cc62d09c-d79e-4ab3-94c4-90cf97e33dc2` ([session receipt](kimi-file://f_mcp_0dfd3e0974e322945036a7329de0c16b7c5c3d2be44563252578163e37f7b83b)). This is an HTML visual check, not PDF visual certification or a full v2 reading. The only tab created for this check was closed. No binary was added to the project.

### Confirmed additions/clarifications versus retained evidence

| Item | v1 evidence actually inspected | v2 primary location/evidence | Correct author-facing disposition |
|---|---|---|---|
| Scale/data extension | C.2 saved text says all models roughly2B, approximately400B bytes; no matching 500M/100B/Table4 text found | A gives reduced 500M dimensions; C.2/Table4 and D add 500M/2B at approximately100B bytes; main2B/400B remains | Genuine added comparison coverage; do not say all v2 results use one size/budget |
| Table4 numeric evidence | No Table4 in saved v1 extraction | C.2 rendered table, transcribed below; §4.2 prose agrees on its500M three relevant cells | A07's missing-cell gap is closed **for this audit**; paper-wide changed figures remain unchecked |
| Seed scope | C.2/D passages do not specify seed variance | C.2: “Each configuration, including the main2B /400B-byte runs, is a single training run; we do not report seed variance”; Table4 “Each cell is one training run” | New explicit disclosure, not new statistical replication or an assertion that v1 established multi-seed results |
| Serving resources | v1 full card already restricts cache/FLOP numbers to estimates and leaves latency unestablished | D explicitly: “Serving latency and throughput are not measured”; inference FLOPs/byte and **trunk** KV-cache reduction are analytical proxies | Stronger explicit limitation; not newly measured speed/memory evidence; retain the old card's caution |
| Training-FLOP accounting | Targeted v1 search did not find the four explicit multiplier strings | §4.3: SP/non-SP multipliers **1.74× fixed-p8,1.49× SpaceByte,1.47× entropy,1.41× H-Net**; inference ratios are separately labeled | Addition/quantification; avoid mixing training/inference ratios or whole-model/cache definitions |
| H-Net behavior | v1 full card already records the matched-FLOP failure and the router-coupling hypothesis | v2 §5.1/limitations retain this limitation; no new causal mechanism certification | Retained counterexample, **not a newly discovered v2 result** and not proof the suggested mechanism caused it |
| H-Net thresholds/checkpoints | v1 B.3 already sets main H-Net threshold2.5; v1 Fig.13 demonstration explicitly uses1.5 vs experiments2.5 | v2 B.3 additionally specifies a **separate H-Net checkpoint trained at1.5 for inference-frequency Fig.8**; E.4 Fig.13 retains the demo/main distinction | Do not call the2.5/main versus1.5/demo distinction itself new. The separate trained-checkpoint statement is the important clarification |
| Figure/section location | v1 card references inference controls §5.3/Figs.9–10 and patch behavior E.3 | v2 inference-frequency §5.2/Fig.8; patch-size variation E.3/Fig.12; patchification behavior E.4 | Version-specific pointers required; never copy old figure numbers into v2 citations |

**Table4 visual transcription — validation BPB, not a new result analysis:**

| Model | 500M parameters,100B bytes | 2B parameters,100B bytes | 2B parameters,400B bytes |
|---|---:|---:|---:|
| Byte-level | 0.7283 | 0.6933 | 0.6366 |
| Tokenizer-based | 0.7509 | 0.7063 | 0.6465 |
| Fixed (p=8) | 0.7833 | 0.7295 | 0.6691 |
| Fixed (p=8)+SP | 0.7425 | 0.6920 | 0.6345 |

Caption: approximately100B-byte runs use50,000 steps and sequence batch256; main runs batch1,024; each cell one run. This transcription establishes what evidence v2 supplies; it does not adjudicate model superiority, statistical robustness, deployment gains, or applicability to FLUED.

**Required integration:** preserve full-v1 provenance; attach a **selected v2 update** rather than changing the old card to FULL v2. Read the rest of changed method/results/figures and PDF only if a paper-wide current-version synthesis is required. The v2 NeurIPS checklist is not evidence of a venue decision. No independently verified ICLR 2027 forum for Scratchpad Patching was established here.

## 7. Author/source-status rules and paper-read gate

### Required source-status discipline

1. Store **work identity, venue-record identity, source edition, status snapshot, and reading scope separately**. Deduplicate stable arXiv IDs across revisions and preserve separate forum/track records. Match titles/abstracts provisionally without attaching public author identities to anonymous submissions.
2. Use five distinct source labels in prose: **official API metadata retrieved**, **official page rendered**, **search-indexed official association**, **primary abstract/selected paper passages**, and **version-scoped full card reused**. None is a synonym for another. A returned cached official API record is stronger than an external index snippet, but is not a full live thread or complete identity/version history.
3. For an ICLR row, record exact domain/group, forum, title, current returned venueid/label, note version, creation/modification dates, anonymous status, source URL and access date. Add decision/withdrawal-event evidence only when actually retrieved. Inaccessible fields stay **unknown**, not “none.”
4. Keep note version, PDF content reference, arXiv version, and publication edition distinct. A changed title on one stable ID is not automatically a new work; two methods sharing a name are not automatically one work. Do not treat a content-addressed URL as a locally verified cryptographic digest.
5. **Submission never means acceptance.** An indexed under-review header can survive withdrawal. Workshop poster status never transfers to the main conference. Metadata status neither validates nor falsifies scientific findings.
6. Do not date withdrawal from `mdate`. Refresh official state before publication; if direct event access remains challenged, keep the event-date gap. Do not solve challenges, use credentials, or repeatedly vary blocked endpoints to simulate exhaustive access.
7. Keep **field coverage, work count, source editions, venue records, metadata screens, selected reads, and full reads** as different counts. This audit closes selected identity checks, not broad scientific coverage or architecture selection.

### Which claims require paper reading rather than metadata

| Cohort | Permissible now | Still requires actual original-paper reading/version comparison |
|---|---|---|
| A07 N01–N13 | Verified official association/status; exact abstract-attributed motivation/approach, explicitly labeled as author claims | Objective/estimator, causality/prefix legality, algorithm/units, controls, full numeric tables, negative cases, supervision and cost |
| N02 MRT / N10 retokenizer / N11 BridgeSTOP / N12 LEAD / N13 Constructive Prediction | Newly recovered abstract can replace “unknown abstract” screening status | MRT suffix prior provenance/regularizer; retokenizer reward/policy estimator and byte preservation; streaming rollback/KV/prefill costs; LEAD subspace/intervention and language-label permissions; lexical-code construction, external-embedding source and reassignment controls. Abstracts do not certify these |
| N05 PriorBPB | Forum title/state and author abstract available | Resolve Target/Answer title editions; paper estimator/parameterization, uncertainty, length-prior/tail controls. Blog is a different partial source, not FULL paper |
| A08 rechecked V01,V02,V05,V07,V13,V20,V24 | Correct forum/status/version metadata; abstract-attributed questions | Intervention validity, theorem assumptions/proofs, exact task scope, budget matching, complete experiments and failure cases; no capacity, causal-use, or transfer conclusion adjudicated here |
| A08 withdrawn/desk-rejected controls | Correct status metadata and modification dates | Scientific claims require the same body/appendix standard as active papers. Reasons/event dates need their own official replies; paper reading alone will not establish current status |
| BIW-0103 | Reuse actual full **arXiv v1** card within its existing restrictions | Official PDF↔arXiv equivalence or material edition differences before presenting the card as a conference-paper full read |
| BIW-0076 | Full v1 reused; selected v2 update, Table4 visually recovered | Remaining changed figures/sections and paper-wide v2 synthesis; actual serving speed requires measurements, not more metadata or a theoretical inference |
| Rvz6kIZAcg new collision candidate | Official active submission, note v2, abstract-screened relevance | Full semantics/repair protocol, adapter/correction permissions, collateral controls, cost and generalization; do not merge with local retokenization |

**Priority source repairs for the synthesis/catalog owners (not edits performed here):** adopt Compiled Tokenizers' withdrawn status with date precision; upgrade A07 venue confidence while keeping reading depth unchanged; keep Turnip/TokSuite year/track boundaries; protect PriorBPB and W0086/BIW-0103 version mappings; add the GlitchPatch method-name collision to triage; integrate Scratchpad v2 as an update rather than another work/full read. No mathematical result or architectural winner is selected by this audit.

## 8. Verification receipt and remaining limits

Only `docs/research/flued_broad_research_v2/05_review/ICLR2027_SOURCE_AUDIT.md` was authored. No source registry, prior card, discovery register, PLAN, AGENTS, production code, or unrelated file was changed. Initial Git status already contained the untracked v2 research root and unrelated drafts/bundles; other agents may concurrently add their assigned artifacts.

A foreground standard-library Python check validates UTF-8, newline/trailing whitespace, 24 unique claimed-record rows, Q01–Q24 query rows, their 20/3/1 state split, all twelve Table4 numeric cells, expected source-control identifiers, and local Markdown file targets. UTC conversions used `datetime.fromtimestamp(milliseconds/1000, timezone.utc)` on returned metadata. Git status and whitespace checks were inspected. No software tests/build/training were relevant or run for this Markdown-only source audit. These artifact checks do not certify scientific results, live decision completeness, or venue-wide exhaustiveness.

Remaining gaps are explicit: 18 A08 active rows outside this independent sample; direct official thread/decision and revision-history access; exact withdrawal/desk-rejection event timestamps; unverified official-PDF/arXiv body equivalence; substantive original readings for new candidates; unchanged/newer histories outside the targeted checks; and a full current-version Scratchpad reading if needed. The threshold of at least12 independently audited claimed records is exceeded without presenting the unclosed fields as verified.
