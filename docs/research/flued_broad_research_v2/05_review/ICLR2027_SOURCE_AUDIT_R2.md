# ICLR 2027 source audit R2 — remaining records, blocked originals, and interface leads

**Snapshot:** 2026-11-09, Asia/Shanghai; timestamps below are UTC. **Scope:** a source/status/acquisition audit, not a full-paper reading or mathematical-results review. Authored only this report and the explicitly authorized `05_review/source_staging/` receipt/source files. R1, discovery registers, reading cards, shared registries, and ACCESS_DIAGNOSTIC were not changed.

## 1. Result and denominator

- **All 18 A08 records outside R1's independent sample were rechecked through ordinary official public search API responses. All 18 return `ICLR.cc/2027/Conference/Submission`.** Their note versions remain2 and note modification dates remain2026-10-05 UTC. They are submissions, not accepted papers.
- **Six previously BLOCKED bodies** across reading batches V08/V02/V07 were individually retested: six official PDF references by normal verified curl and six by ordinary FetchURL. **None was acquired.** Curl reported certificate-revocation-service failure before HTTP; FetchURL returned OpenReview verification challenges. These are different access failures and neither licenses a claim that the entire service or every legitimate mirror is unavailable.
- **One related lawful original was acquired:** W0086 / arXiv **2602.04852v3**, 1,545,609 bytes, saved under this audit's staging folder, SHA-256 verified, first-page title check passed. It is **not one of the six blocked originals**, not a certified copy of its anonymous forum PDF, and not a new FULL reading.
- **27 official search requests exposed33 distinct conference forums:** 20 A08 records (18 gap closures plus V02/V13 refreshes), nine relevant interface records, one adjacent quantization screen, two R1 status/collision controls, and one incidental withdrawn vision-memory result. Returned states: **31 submission, two withdrawn**. Counts are source records, not33 unique new works, not a venue census, and not acceptance counts.
- Among the interface records: **six titles absent from the two old identity catalogs**, one newly verified forum association for existing BIW-0028/W0356, and two already-known R1 forum refreshes. All remain metadata/abstract-screening evidence here.
- **Zero new FULL readings, zero official OpenReview PDFs downloaded, zero acceptance decisions established.** Full reading remains terra's task. One acquired PDF is an arXiv related-edition/control, not a workaround around an OpenReview challenge.

R1+R2 now provide individual metadata evidence for **all25 A08 active-register entries**. R2 freshly checks20 of them; the five R1-only records **V01,V05,V07,V20,V24** were not refreshed in R2. Do not present that union as one uncached contemporaneous venue listing. The three R1 withdrawn/desk-rejected broad controls were not refreshed here; Compiled Tokenizers was.

## 2. Inputs read before access attempts

Read [R1](ICLR2027_SOURCE_AUDIT.md), the shared [ACCESS_DIAGNOSTIC](ACCESS_DIAGNOSTIC.md), [V08 access diagnostic](../03_reading/V08/ACCESS_DIAGNOSTIC.md), V08/V02/V07 batch summaries, all six BLOCKED cards below, and the A08 work register. The access diagnostic documents that earlier Python automatic-proxy TLS EOF failures did **not** imply a general PDF outage: default Git Bash curl/direct requests succeeded for public arXiv/PMLR originals. R2 therefore tested that normal route instead of copying a global-inaccessibility conclusion.

| Reading batch | Card actually read | Exact blocked forum |
|---|---|---|
| V08 | [BR-A08-V02](../03_reading/V08/BR-A08-V02.md), Incentive | UUldzWxIL4 |
| V08 | [BR-A08-V14](../03_reading/V08/BR-A08-V14.md), Receiver State | 2M4nt7AFuD |
| V08 | [BR-A08-V22](../03_reading/V08/BR-A08-V22.md), Routing | 9vT48Lms48 |
| V08 | [BR-A08-V25](../03_reading/V08/BR-A08-V25.md), Predictive-State Bottlenecks | 58JxyfvZJj |
| V02 | [BR-A08-V04](../03_reading/V02/BR-A08-V04.md), SDG | lYWcLB1rAh |
| V07 | [BR-A08-V13](../03_reading/V07/BR-A08-V13.md), Cross-Model Stitching | 98Rbm5C5Bl |

**Chronology correction, without editing R1:** [V08's later summary](../03_reading/V08/BATCH_SUMMARY.md) now records a FULL Scratchpad Patching **v2 update**, FULL public-arXiv cross-lingual and GlitchPatch reads, and a separately qualified PSR paper-text read. R1's selected-v2 scope accurately describes R1, but is no longer the newest project-wide reading status. Reuse the V08 exact-version cards; R2 does not recount their work or newly certify their experiments. The six anonymous bodies above remain a separate unresolved cohort.

## 3. Current official metadata: the18 missing A08 checks

Every row below was actually returned by a public official API search in R2. Checked `id=forum`, exact title, `domain=ICLR.cc/2027/Conference`, public readers, conference submission invitation, number, `content.venueid`, human-readable venue, note version, creation/modification timestamps, and official PDF reference. Every row has:

```text
domain = ICLR.cc/2027/Conference
readers = [everyone]
submission invitation = ICLR.cc/2027/Conference/-/Submission
content.venueid = ICLR.cc/2027/Conference/Submission
content.venue = ICLR 2027 Conference Submission
note version = 2
cdate = tcdate; mdate = tmdate
```

**Current state in this table: official API-observed submission. Decision replies and exact PDF revision/date: not retrieved/unknown.** Note v2 does not mean PDF v2. Most responses expose `fromCache=true`; V10 and V17 omit the flag. Flag absence is not `false` and public search metadata is not a complete live thread. Creation date is the returned note creation time, not final manuscript upload. Exact raw timestamps and all PDF references are preserved in the sanitized [R2 manifest](source_staging/R2_manifest.json); no author identities or profile fields are retained.

| A08 key | Exact title / official forum | Submission # | Created UTC | Note modified UTC,2026-10-05 |
|---|---|---:|---|---|
| V03 | [Kronecker Delta Rule for Long Context Linear Attention](https://openreview.net/forum?id=2XDUbuZOTH) | 25475 | 2026-09-16 | 20:00:49.757 |
| V04 | [SDG: State-Dependent Gating at Chunk Boundaries for Linear Attention](https://openreview.net/forum?id=lYWcLB1rAh) | 6796 | 2026-08-31 | 17:31:17.478 |
| V06 | [GABA: Geometry-Aware Bilinear Attention for Linear Transformers](https://openreview.net/forum?id=8JN5Qezfyj) | 17684 | 2026-09-14 | 19:25:48.666 |
| V08 | [RunningTensor: Generalizing Linear Attention to Higher-Order Recurrent States](https://openreview.net/forum?id=f7bdAVAC2e) | 40557 | 2026-09-18 | 20:41:35.753 |
| V09 | [Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling](https://openreview.net/forum?id=vFAVe0yppt) | 48263 | 2026-09-18 | 21:01:26.909 |
| V10 | [Sliced-Linear Attention: Beyond the Finite-Feature Bottleneck of Linear Attention](https://openreview.net/forum?id=7v4LREwPhX) | 42956 | 2026-09-18 | 20:47:54.788 |
| V11 | [LoopLA: Causal State Refinement for Looped Linear Attention](https://openreview.net/forum?id=xzOnjQHMr9) | 943 | 2026-08-20 | 16:56:32.122 |
| V12 | [SURCO: Survivor Compensation for Recurrent-State Pruning of State Space Models](https://openreview.net/forum?id=utN1p2r5r2) | 45334 | 2026-09-18 | 20:54:29.709 |
| V14 | [Receiver State Shapes Functional Compatibility: Internal Message Adaptation for Model Stitching](https://openreview.net/forum?id=2M4nt7AFuD) | 46280 | 2026-09-18 | 20:56:50.283 |
| V15 | [The Role of Data-Reuse on Shortcut Learning with Linear Networks](https://openreview.net/forum?id=7Lje1KCKrE) | 1619 | 2026-08-20 | 16:58:40.069 |
| V16 | [Farsighted Correction of Shortcut Learning: From Dynamic Starvation to Confidence-Gap Optimization](https://openreview.net/forum?id=JrKJaRbQpz) | 13342 | 2026-09-10 | 18:46:00.744 |
| V17 | [Uncovering Latent Reasoning Strategies in Language Models](https://openreview.net/forum?id=edyITivJJW) | 33735 | 2026-09-17 | 20:22:07.566 |
| V18 | [Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval](https://openreview.net/forum?id=Gj3NCR6Hge) | 7528 | 2026-09-01 | 17:39:10.400 |
| V19 | [When Errors Become Memories: Causal Pathway Tracing in Multi-Turn Memory-Augmented LLMs](https://openreview.net/forum?id=KUAlW7DbIh) | 16103 | 2026-09-13 | 19:11:50.314 |
| V21 | [Where You Put Attention Matters More Than How Much You Use: Attention Placement in Hybrid Sequence Models](https://openreview.net/forum?id=0fPxp7a50O) | 3220 | 2026-08-22 | 17:03:20.090 |
| V22 | [When Routing Must Be Right: Irreversible Lock-In in Attention Routing](https://openreview.net/forum?id=9vT48Lms48) | 34378 | 2026-09-17 | 20:23:34.338 |
| V23 | [LinQuant: Functional Invariances for Low-Precision Linear Recurrences](https://openreview.net/forum?id=6egpMpGwZE) | 52450 | 2026-09-19 | 21:11:02.146 |
| V25 | [Understanding the Predictive-State Bottlenecks of Transformer Models](https://openreview.net/forum?id=58JxyfvZJj) | 9339 | 2026-09-04 | 18:06:02.727 |

The two R1-overlap blocked-body refreshes also return public conference submissions, anonymous note v2, with unchanged metadata references:

| A08 key / forum | Submission # | Created UTC | Modified UTC |
|---|---:|---|---|
| [V02 / UUldzWxIL4](https://openreview.net/forum?id=UUldzWxIL4) | 50948 | 2026-09-19 | 2026-10-05 21:07:52.098 |
| [V13 /98Rbm5C5Bl](https://openreview.net/forum?id=98Rbm5C5Bl) | 40828 | 2026-09-18 | 2026-10-05 20:42:15.522 |

No changed state was observed within these20 A08 records. Their abstract claims are not independently checked results. A September19 UTC creation date does not establish an AOE-deadline violation, and a2026 creation/BibTeX year does not change the2027 venue group.

## 4. Six BLOCKED originals: per-source PDF access and version evidence

### Normal direct-client diagnosis, not a global outage claim

Used existing Git Bash curl, unchanged proxy/trust settings, HTTPS-only request/redirect protocols, ordinary certificate **and revocation** checks, 15-second connect limits, and bounded total request limits. No credentials, `-k`, insecure SSL contexts, `--ssl-no-revoke`, alternate identities/IPs, challenge solving, or installation.

The representative direct API request `https://api2.openreview.net/notes?id=UUldzWxIL4` returned **curl35, HTTP000, proxy_used0, Schannel `CRYPT_E_REVOCATION_OFFLINE`**. This fails before an HTTP response; it is not a403, a proof of a missing public note, or the old automatic Python-proxy failure. `ssl_verify_result=0` alone is not success when curl exits35.

For Incentive, the first normal query-PDF request `https://openreview.net/pdf?id=UUldzWxIL4` produced localized curl output that the receipt parser could not decode as UTF-8; no PDF was validated or retained. A separate normal request to the official metadata's exact content reference yielded the explicit curl35/HTTP000/zero-byte receipt below. A subsequent console-encoding error did not change that request outcome. Neither scripting error was treated as successful acquisition, and no extra download was hidden in the count.

### Exact references and paired observations

Each exact URL below was requested once by normal curl in its content-reference form, and once by ordinary FetchURL in this round. Prior reading-card challenge results were not silently reused as current observations. The new public response metadata still points to the same reference recorded on the cards; that is **reference equality, not independently computed PDF hash/content equality**.

| Work / reading batch | Current official PDF reference, exact URL | Curl observation | Ordinary public FetchURL observation | Legitimate counterpart/version comparison established? |
|---|---|---|---|---|
| BR-A08-V02 / V08 | https://openreview.net/pdf/9c64cd9b8b1bba44c1ff65945bd6c1a02ed98a9d.pdf |35; HTTP000; proxy0; bytes0; revocation service offline | Verification challenge | **No**; no exact public original/mirror recovered |
| BR-A08-V04 / V02 | https://openreview.net/pdf/a6be3de5a7a112d8d9971f44d46409d02e29d0aa.pdf | Same verified failure category | Verification challenge | **No** |
| BR-A08-V13 / V07 | https://openreview.net/pdf/292012e3cebcb326c132293eb93d41f533bf95d3.pdf | Same verified failure category | Verification challenge | **No**; ungrouped exact-title official search returned only the same forum |
| BR-A08-V14 / V08 | https://openreview.net/pdf/b167a621df8f120088cda7baa7cccfcbfd226cd7.pdf | Same verified failure category | Verification challenge | **No** |
| BR-A08-V22 / V08 | https://openreview.net/pdf/4b049a14ede5c22389997afeb1b72a99e81a7de5.pdf | Same verified failure category | Verification challenge | **No** |
| BR-A08-V25 / V08 | https://openreview.net/pdf/3df135438f55aa7adaea9da322f21607da69a080.pdf | Same verified failure category | Verification challenge | **No** |

The challenge pages were not interacted with or retried. Curl's earlier failure was not a challenge response. These two ordinary retrieval observations are retained separately, not described as a successful alternate path through a wall. No incomplete `.part` file remains and no challenge HTML was renamed as PDF or text-extracted as a paper.

### Bounded legal-version discovery

A built-in-browser search attempt for the exact Incentive title plus `arxiv` failed `ERR_CONNECTION_CLOSED`. Six public exact-title/phrase searches were then issued through WebSearch (queries in §7); they returned irrelevant papers and/or metadata aggregators, **not an established exact legitimate public body for these six works**. No author identity matching was attempted. Aggregator snippets were not upgraded to a paper or venue source, and unrelated arXiv IDs were not adopted. This is a negative result of this bounded discovery pass, not proof that no legal counterpart exists.

**Disposition:** all six remain **body BLOCKED in R2**; official association/status is now refreshed, but PDF revision/date, full revision history, supplements, and cross-edition equivalence remain unknown. Normal downloading remains the required route if public availability/trusted transport recovers. Do not disable TLS/revocation checking, use login, or call metadata recovery a full-text recovery.

## 5. Successful lawful related-edition control and staging manifest

The same ordinary curl client successfully downloaded [arXiv2602.04852v3](https://arxiv.org/pdf/2602.04852v3), the previously identified related edition for **W0086 / A08-V07, On State Reduction in Linear Attention**. This distinguishes the OpenReview-specific transport/challenge observations from a blanket public-source outage. It does not diagnose which revocation infrastructure failed, change system proxy settings, or grant access to an OpenReview body.

| Item | Verified receipt |
|---|---|
| Requested/effective URL | `https://arxiv.org/pdf/2602.04852v3` / same |
| Retrieval UTC | 2026-11-09 07:43:55.149868 |
| HTTP/curl/TLS/proxy |200 /0 / verification result0 / proxy_used0 |
| MIME / byte count | `application/pdf` /1,545,609 |
| PDF integrity | `%PDF-` signature; final `%%EOF` present |
| Saved original | [W0086__2602.04852v3.pdf](source_staging/W0086__2602.04852v3.pdf) |
| SHA-256 | `66573f7ea8d8e515ae222165858cdc8d50abbf789e9b95a3842700dc25681159` |
| Parse/title check | Existing `pdftotext -f 1 -l 1 -layout -enc UTF-8 PDF -`, exit0; **On State Reduction in Linear Attention** found on first page |
| Actual reading scope | Acquisition/title verification only; no new full read, no derived full-text file, no scientific-result conclusion |

**Version relationship:** R1 already checked public arXiv history throughv3 (2026-09-29) and the old-title alias on stable arXiv ID2602.04852. R2 preserves that provenance and now locks physicalv3 bytes. The anonymous OpenReview record `3uKKt21Vry` was **not redownloaded or refreshed in R2**; its body is not available for a two-way comparison. Therefore this is a **lawful related version, equivalence still unresolved**, not “conference PDFv2 equals arXivv3.” A preprint's public author list is not attached to the anonymous forum.

**Manifest:** [R2_manifest.json](source_staging/R2_manifest.json) preserves sanitized33-record metadata, raw timestamps, exact27 query URLs/counts/returned IDs, six per-source curl observations, six FetchURL challenge observations, the separate representative API/query-route diagnostics, mirror-discovery queries, and the successful arXiv byte/hash/title receipt. It omits author/profile fields. Only the manifest and this one PDF are retained under `source_staging/`; failed partials and no-longer-needed diagnostics were not left as files. No PDF was altered.

## 6. Recent tokenizer/byte-source recovery, without paper-result adjudication

A07's14 venue records were audited in R1, not a limit on further interface discovery. R2 screened the first five official search results each for quoted `tokenization` and `byte`, plus the first five requested for `tokenizer-free` (one returned). Seven particularly relevant forum associations not independently established in R1 are below. All have correct2027 conference domain, public readers, submission invitation, active submission venueid/label, **note version2**, and note modified2026-10-05 UTC. PDF edition unknown; their PDF URLs in the manifest were **not downloaded/tested individually**. Do not label those untested bodies BLOCKED merely because the six other OpenReview URLs failed.

| R2 source key | Exact title / official forum | Submission # / created UTC | Modified UTC,2026-10-05 | Source/reading disposition |
|---|---|---|---|---|
| T01 | [Tokenization with Formal Guarantees: From Optimal Compression to Provable Bounds](https://openreview.net/forum?id=FXLPTx7osi) |38781 /2026-09-18 |20:36:04.382 | Metadata/abstract; no matching title in two old catalogs |
| T02 | [Stochasticity in Tokenization Improves Robustness](https://openreview.net/forum?id=rIRkUxOleG) |6777 /2026-08-31 |17:31:08.512 | Metadata/abstract; no matching title in two old catalogs |
| T03 | [Online Tokenization with Optimal Delay in Near Linear Time](https://openreview.net/forum?id=8D7l5sK3YT) |11755 /2026-09-08 |18:30:48.591 | Metadata/abstract; no matching title in two old catalogs |
| T04 | [Tokenization Invariance Is Learned Late and Broken at the Head](https://openreview.net/forum?id=63kZK7oyd6) |26364 /2026-09-16 |20:03:19.716 | Metadata/abstract; no matching title in two old catalogs |
| T05 | [Cross-Tokenizer On-Policy Distillation via Byte-Prefix Marginalization](https://openreview.net/forum?id=Mm5OLOPLT0) |1302 /2026-08-20 |16:57:39.933 | Metadata/abstract; no matching title in two old catalogs |
| T06 | [B-Net: Learning Where to Compress in Byte-Level Language Models](https://openreview.net/forum?id=fMymbXoq9T) |32922 /2026-09-17 |20:20:16.031 | Metadata/abstract; no matching title in two old catalogs |
| T07 | [Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation](https://openreview.net/forum?id=nDmrZCYWto) |15085 /2026-09-12 |19:02:29.397 | **Existing BIW-0028/W0356**, newly established official forum association; not another work/read |

The exact-title/ID checks searched the two old catalogs plus the v2 root for the six missing titles. “Missing from checked catalogs” is not scientific novelty or proof of absence from every unpublished note. No global work IDs or shared registry rows were created.

### Abstract-attributed mechanisms and what terra must recover

These are screening descriptions of the **authors' stated approaches**, not independently verified mathematical or empirical findings. No performance numbers from these abstracts are adopted.

| Source | Original problem → author-proposed approach, at abstract scope | Requires legitimate original-paper reading before substantive synthesis |
|---|---|---|
| T01 | Heuristic vocabulary compression lacks optimization certificates → graph-flow mixed-integer formulation and shortest-path/Lagrangian relaxation | Exact token-selection objective, overlap constraints, what is bounded, scale/solver budgets, and whether corpus compression predicts any LM outcome; no theorem endorsed here |
| T02 | Canonical-tokenization training may be brittle to alternate segmentations → stochastic-tokenization training/fine-tuning and perturbation evaluation | Uniform-sampling support/distribution, byte/string preservation, train/test perturbations, exposure/length/compute matching, clean-performance exceptions |
| T03 | Sequential tokenizer stages delay streaming output → an online-tokenization formulation and low-delay algorithm | Delay's comparator and assumptions, tokenization equivalence, adversarial prefixes/end flush, memory definition, hardware/timing protocol; tokenizer latency is not automatically end-to-end serving latency |
| T04 | Retokenization errors may differ between trunk representation and output head → checkpoint probes, mean correction, head versus matched trunk adaptation | Probe/random-direction and pooling controls, task-specificity, tokenization/string likelihood definitions, adapter permissions, pretraining exposure, full prediction registry and negative cases; title is not a proved general localization |
| T05 | Cross-tokenizer distillation can lose or misalign teacher mass → longest-student-prefix mapping with residual category and a separate multi-teacher-token treatment | Exact alphabet/history/EOS/partial-byte cases, assumptions for exactness, otherwise-bound direction, teacher-query cost, and whether targets equal unmarked-byte marginals; **do not equate it with BIW-0103's marked EOT exactness** |
| T06 | Learned boundaries may fail to realize the requested compression rate → causal-convolution scorer plus adaptive threshold control | Controller's train/generate visibility and update timing, whole-sequence statistics/prefix legality, boundaries/rate separability, all-state/compute/tuning matching, English/Chinese controls; no guarantee inferred from “causal” |
| T07 | Bytes lengthen sequences without fixed lexical abstractions → token-superposition/hash inputs and analysis of learned local collection | Reuse actual **2610.05978v1** card with its corrected hybrid architecture/cost limits; compare forum body before declaring edition equality; accepted speculative candidates are not wall-clock speed |

For T07, independently fetched [arXiv2610.05978v1 abstract/history](https://arxiv.org/abs/2610.05978v1) again displaysv1 **2026-10-05 08:29:08 UTC**, exact title and closely matching abstract. The existing [BIW catalog](../../byte_language_interface_survey/02_inventory/WORK_CATALOG.md#BIW-0028) points to the version-scoped [W0356 full card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md). This establishes a **title/abstract-supported association**, not author linkage or body equality. Reuse that card; do not requeue an already-read original merely to increase counts. Its arXiv body was not downloaded/reread in R2.

### Other returned records and status controls

- **T08 BridgeSTOP / `gbaS4smhnV`**, #8108: submission, notev2, created2026-09-02, modified2026-10-05 17:44:12.401 UTC. **T09 Breaking the Token Ceiling / `O1JpRRUeGW`**, #49116: submission, notev2, created2026-09-18, modified2026-10-05 21:03:33.030 UTC. These are R1-known entities returned again by the topic searches, not new works/readings.
- **C01 Compiled Tokenizers / `CixpFoiooB`**, #7019: **Withdrawn_Submission**, notev2, modified2026-11-08 10:45:24.749 UTC, unchanged from R1. Exact withdrawal-event date remains **unknown**; do not turn `mdate` into that date or infer rejection reasons.
- **C02 Echoing Is Not All You Need / `Rvz6kIZAcg`**, #57049: submission, notev2, modified2026-10-05 21:20:09.899 UTC. The R1 GlitchPatch method-name collision remains; this is not the local-retokenization forum `DbzLzs5VL7` and no version merge is justified.
- **X01 Byte-Constrained Layer-Wise Quantization with Cost-Normalized Sensitivity / `EutVjE5fM2`**, #7932: submission, notev2, modified2026-10-05 17:43:09.580 UTC. Byte **storage accounting**, not a byte-language interface; retained as an adjacent search screen, not a new core interface paper.
- **X02 HHF: Attention-Guided Frame Memory for Streaming3D Reconstruction / `CcJBIXPAEx`**, #36817: **Withdrawn_Submission**, notev2, modified2026-10-05 16:41:21.033 UTC. Returned on continuation of the quoted Causal Memory Policy query, not an exact-title match. It is a vision-memory screening record, not adopted scientific evidence and not CMP's status. No withdrawal-event date retrieved.

All these states are record-specific. A withdrawn search neighbor never changes the state of the intended active paper. Anonymous active identities remain anonymous even where another public record exposes named authors.

## 7. Exact search/access scope and pagination

All exact URLs, term strings, requested limits/offsets, reported counts and returned IDs are in [R2_manifest.json](source_staging/R2_manifest.json). Queries used only public paper titles/topic terms. No private manuscript, project data, or credentials were uploaded.

### Official metadata queries actually executed

Common grouped template:

```text
https://api2.openreview.net/notes/search?term=<percent-encoded literal quoted text>&group=ICLR.cc/2027/Conference&limit=1&offset=0
```

For20 A08 records: full exact title for **V02,V03,V04,V06,V13,V15,V17,V25**; the following exact quoted terms for the rest:

| Key | Literal term |
|---|---|
| V08 | `"RunningTensor"` |
| V09 | `"Triadic Linear Attention"` |
| V10 | `"Sliced-Linear Attention"` |
| V11 | `"LoopLA"` |
| V12 | `"SURCO"` |
| V14 | `"Receiver State Shapes Functional Compatibility"` |
| V16 | `"Farsighted Correction of Shortcut Learning"` |
| V18 | `"Causal Memory Policy"` |
| V19 | `"When Errors Become Memories"` |
| V21 | `"Where You Put Attention Matters More Than How Much You Use"` |
| V22 | `"When Routing Must Be Right"` |
| V23 | `"LinQuant"` |

All20 requested one result at offset0. Reported count1 except V18 count2. V18 offset1 was separately fetched and inspected (X02), completing **that narrow reported two-result set**, not a memory-literature census. Quote-sensitive search is not necessarily exact-title-only matching.

Additional seven API calls:

| Literal term | Group / limit,offset | Actual count / coverage |
|---|---|---|
| `"tokenization"` | ICLR2027 /5,0 |232; only first5 inspected: T01,T08,T02,T03,T04 |
| `"byte"` | ICLR2027 /5,0 |176; only first5 inspected: T05,T06,X01,T09,T07 |
| `"tokenizer-free"` | ICLR2027 /5,0 |1; T07 again, no extra entity |
| `"Causal Memory Policy"` | ICLR2027 /1,1 |2; X02 only on this page |
| `"Cross-Model Stitching Transfers Answers, Not Computation"` | **No group parameter** /5,0 |1; same V13, no extra public edition established |
| `"Compiled Tokenizers"` | ICLR2027 /1,0 |1; C01 |
| `"Echoing Is Not All You Need"` | ICLR2027 /1,0 |1; C02 |

No other pagination, sort, all-venue listing or automatic enumeration. The232/176 numbers are service-reported matches, not unique relevant works, accepted papers, or a denominator this audit has exhausted. Matching title/abstract terms can recover adjacent modalities and methods; each returned venueid was checked individually.

### Bounded mirror-discovery queries

After the built-in-browser connection failure, these six WebSearch strings were issued exactly once each:

```text
"Linear Attention lacks Incentive for Associative Recall, not Capacity" arxiv
"SDG" "State-Dependent Gating" arxiv
"Cross-Model Stitching Transfers Answers, Not Computation" arxiv
"Receiver State Shapes Functional Compatibility" arxiv
"When Routing Must Be Right" arxiv
"Understanding the Predictive-State Bottlenecks of Transformer Models" arxiv
```

No exact eligible body/version was established from those results. Metadata aggregators and irrelevant arXiv papers were not scientific or identity evidence. No author-profile queries, inferred arXiv identities, mirror scraping, or challenge retries. The report relies on returned official records and the lawful acquired arXiv PDF, not these search snippets.

## 8. Author-facing source rules and terra handoff

1. **Metadata association, file acquisition, edition comparison and full reading are separate tasks.** The18 missing metadata checks are now closed at official-response scope; the six body tasks are not. Do not change their cards to FULL, or infer results from their abstracts/titles.
2. **A cached official API response is not a complete live identity/history.** Record access date, exact domain/forum/venueid, note version and modification time; retain unknown decision replies, manuscript revision and withdrawal-event date. Refresh before publication.2026 submission dates/BibTeX fields do not imply ICLR2026.
3. **Failure labels must name client and layer.** Old Python automatic-proxy EOF, current curl certificate-revocation failure, browser connection closure and OpenReview verification challenge are not interchangeable. A successful ordinary arXiv download falsifies a blanket public-source-outage description, not the individual OpenReview blockers.
4. **Keep the security boundary:** normal public routes only; no TLS/revocation relaxation, credentialed access, challenge solving or repeated endpoint variation to get around a challenge. A legal related preprint can be read independently but is not silently substituted for an anonymous conference edition.
5. **Preserve version-scoped existing work:** W0086v3 acquired only for source/version handoff; BIW-0028/W0356v1 already has a scoped full card; BIW-0103v1 and V08's later exact-version cards are reused at their own editions. Notev2 is never arXivv2/PDFv2. Shared method names or changed titles are not dedup keys.
6. **Prioritize missing body acquisition and reads:** the six blocked originals; then the six newly catalog-missing interface titles in §6, particularly the rate-control, cross-tokenizer probability and output-head studies. Terra must recover original methods, assumptions, controls, negative cases, units/visibility and full resource accounting. No theorem, causal diagnosis, mechanism superiority, or architecture selection is adjudicated by this source audit.
7. **Report real coverage:**33 returned forums include repeated known works and two adjacent screens. Seven relevant newly established interface associations contain only six catalog-missing titles; the seventh is an existing paper. They do not add seven FULL readings, and the acquired related-edition PDF is not one of the six failed originals.

## 9. Artifact verification and remaining gaps

Authored paths:

- `docs/research/flued_broad_research_v2/05_review/ICLR2027_SOURCE_AUDIT_R2.md`
- `docs/research/flued_broad_research_v2/05_review/source_staging/R2_manifest.json`
- `docs/research/flued_broad_research_v2/05_review/source_staging/W0086__2602.04852v3.pdf`

Foreground validation recomputes the staged PDF SHA-256/length/signature/EOF, validates its first-page parser/title receipt, verifies33 unique metadata IDs (31 submission/two withdrawn),20 A08 records including exactly18 R1-gap closures,27 query receipts, six individual curl/PDF checks and six FetchURL challenge checks, strict JSON/UTF-8 and local Markdown targets, and absence of `.part` files. Git status and whitespace checks are inspected. No project build/test/training is relevant to this documentation/source-acquisition task; no install, source-code execution from papers, subagents, system configuration change, source-registry/card edit or commit was performed.

**Remaining:** six blocked anonymous bodies; exact manuscript revision and complete edit history for those works; no legitimate mirror/version counterpart established for them; W0086 and BIW-0028 forum/preprint body-equivalence comparisons; original bodies and full reads for the six new interface leads; direct decision replies and exact withdrawal-event dates; the uninspected keyword-search remainder; and five A08 R1-only records not refreshed in R2. None is represented as complete, and no acceptance is inferred.
