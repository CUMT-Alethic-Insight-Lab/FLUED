# Original-source access handoff — 17 selected ICLR 2027 manuscripts

**Snapshot:** 2026-11-09, after the final bounded access check. **Purpose:** make the remaining original files easy to supply and verify. This is **a file-supply checklist, not a request that the user read or review seventeen papers**. Terra/the assigned readers will perform the readings after acquisition and verification. This document adds no scientific synthesis, result verdict, acceptance inference or new FULL reading.

## 1. Current result and last retry receipt

**No new original was recovered in this final check. All17 official conference manuscripts remain unacquired.** Three related lawful public preprints are already present and now have exact-edition FULL cards in V17, but their identity/equality with the anonymous conference manuscripts is unverified. For14 selected works no eligible alternative original has been established by the recorded bounded searches. These17 are a selected cohort, not every blocked item in the entire project.

Read [R3 access/source audit](ICLR2027_SOURCE_AUDIT_R3.md), its [manifest](source_staging/R3_manifest.json), and the updated [V17 summary](../03_reading/V17/BATCH_SUMMARY.md) before preparing this handoff. **Status update:** terra has since completed T02 arXiv2604.16037v1. R3's earlier “acquired, unread” statement was correct at R3's snapshot but is no longer its current reading status. This handoff preserves that chronology without modifying R3 or any card.

### Three representative route categories checked now

Normal existing Git Bash curl, unchanged proxy/trust, verified HTTPS/revocation settings, HTTPS-only redirects, bounded connect/total limits; no credentials, challenge interaction, disabled TLS, IP/identity rotation, or authentication workaround. HTTP error bodies were inspected without `--fail`; **curl0/HTTP403 is not acquisition success**. Responses stayed in memory; no download/error/temporary file was authored.

| Category / exact route | Observation, UTC | Disposition |
|---|---|---|
| Official PDF: `https://openreview.net/pdf/009f6f39ae30a457c722ce02faa53ee551f4b3b2.pdf` (T01) |13:18:30.862390; GET; curl0; HTTP403; TLS result0; proxy_used0;12,692 bytes `text/html`; no redirect. Rendered **Error403 / Access to this page is restricted. Please check that you are logged in to OpenReview and try again.** | No PDF. Generic restriction text does not establish per-paper permissions versus verification-layer cause. No repeat of this denial |
| Official public note API: `https://api2.openreview.net/notes?id=uILf1c6VDo` (V24) |13:18:24.289290; GET; curl0; HTTP403; TLS result0; proxy_used0;273 bytes JSON; **`ChallengeRequiredError` / Challenge verification required** | Explicit verification requirement. Challenge URL not followed or solved. No repeat |
| Already-associated lawful preprint download availability: `https://arxiv.org/pdf/2604.16037v1` (T02) |13:18:38.608849; HEAD; curl28, HTTP000, connect timeout15s; one ordinary HEAD retry13:19:20.113434 with connect20s gave curl35, HTTP000, **Recv failure: Connection was reset**. Both proxy_used0; no HTTP/PDF body received | Two bounded attempts; stopped. This is transport failure, not an arXiv403 or a proved outage. Existing validated local PDF remains usable; no new file recovered or full download claimed |

Thus **three route categories/four actual requests**, not seventeen repeated paper attempts. The public preprint timeout/reset warranted one normal retry; the official restriction/verification responses did not warrant repeated probing. Earlier R3 confirmed a representative normal forum redirect to a verification page and generic403s for both V24 locator/content-reference routes. Nothing in this final check resolves the17-body gap or authorizes bypass.

## 2. Where supplied PDFs should go — no directory created by this handoff

Suggested project-relative destination:

```text
docs/research/flued_broad_research_v2/03_reading/_provided/
```

The directory and filenames below are **proposed future destinations**, not files this audit has created. The user may supply any legitimately obtained official PDFs available to them, individually or in a batch; partial supply is useful. They are **not being asked to read the papers**, solve challenges for the agent, share credentials/cookies, or obtain unauthorized material. No action is required if they do not have lawful access.

Use each row's exact suggested basename for a conference manuscript. Preserve original bytes. If several revisions exist, keep them separately, for example append `__supplied-20261109__r1` before `.pdf`; do not overwrite an earlier supplied file. Never call a PDF `v2` merely because the OpenReview **note** has `version=2`. A separately published preprint must retain its own arXiv/publication ID/version rather than using an official-manuscript filename.

## 3. Route/status legend for the complete checklist

The routes below report **what was actually tried earlier or now**, not a command to retry everything. Every row has a successfully returned official public **search-API metadata** snapshot in R3, with domain `ICLR.cc/2027/Conference`, public readers, returned venueid `ICLR.cc/2027/Conference/Submission`, note version2, and note modification date2026-10-05 UTC. This is a metadata snapshot, **not acceptance, current decision-thread certification, PDF access proof or manuscript revision number**. Search URLs/terms and raw modification timestamps are in the [R3 manifest](source_staging/R3_manifest.json).

- **S:** public official `/notes/search`, exact record/title verified in R3. Direct note API is a different route and was not successfully fetched for every record.
- **P17:** the exact content-reference PDF URL in that row was individually requested by ordinary verified curl in V17; HTTP403, curl22 with `--fail`, no PDF. [V17 receipt summary](../03_reading/V17/BATCH_SUMMARY.md).
- **P18:** the row's exact PDF content reference was individually requested by ordinary verified curl in V18; HTTP403, curl22, no PDF. [V18 receipt summary](../03_reading/V18/BATCH_SUMMARY.md).
- **P18-L:** V18 individually requested public locator `https://openreview.net/pdf?id=uILf1c6VDo`, HTTP403. R3 then recovered its content reference and tested both forms; both403.
- **P-old:** R2 individually tested the row's exact content-reference PDF by normal curl (pre-HTTP Schannel revocation-service failure) and ordinary FetchURL (verification challenge), no body. Earlier/current failures are not interchangeable. [R2 individual ledger](ICLR2027_SOURCE_AUDIT_R2.md#4-six-blocked-originals-per-source-pdf-access-and-version-evidence).
- **R3-B:** B-Net exact PDF GET403, representative repeat403; its normal forum redirected to a verification page. Not all V17 papers were repeated.
- **R3-24:** V24 public locator and metadata-resolved content reference each403; direct public note API explicitly `ChallengeRequiredError`.
- **R3-02:** old Incentive exact PDF representative GET403. Other old-five PDFs were not individually repeated in R3.
- **F-PDF / F-API:** final T01 PDF and final V24 direct API checks in §1. No implication of an additional final per-row retry elsewhere.

**Shared current missing scope (M):** complete official submission PDF body, its exact edition/date and any revision relation to earlier sources, all body-dependent tables/figures/appendices, and any separately packaged supplement remain unavailable/unverified. No body-specific mathematical or experimental claim is validated from metadata. When a preprint exists, its own reading status is listed separately; it does not close M for the official manuscript. Supplied main PDFs may include appendices, but do not assume their separate attachments are included.

## 4. Complete17-file checklist

All forum IDs and PDF content references below were verified against the sanitized official metadata in the R3 manifest. Forum links identify the record even when rendering is challenged. Every proposed file belongs under `03_reading/_provided/` as specified in §2.

| # / key | Exact official title and forum | Exact official PDF URL | Already-tried public routes | Current missing scope | Suggested provided-file basename |
|---|---|---|---|---|---|
|01 /BR-R2-T01 | **Tokenization with Formal Guarantees: From Optimal Compression to Provable Bounds**; [FXLPTx7osi](https://openreview.net/forum?id=FXLPTx7osi) | https://openreview.net/pdf/009f6f39ae30a457c722ce02faa53ee551f4b3b2.pdf |S; P17; F-PDF now403 |M; no lawful alternate original established | `BR-R2-T01__OpenReview-FXLPTx7osi__official.pdf` |
|02 /BR-R2-T02 | **Stochasticity in Tokenization Improves Robustness**; [rIRkUxOleG](https://openreview.net/forum?id=rIRkUxOleG) | https://openreview.net/pdf/1772373f12cb1a74c048ab6d50f1f991ce2efe96.pdf |S; P17; metadata-linked attachment HEAD in R3 returned404, not proof absent; lawful arXiv route separately below |M; public arXivv1 FULL only; official/preprint equality and official attachment unresolved | `BR-R2-T02__OpenReview-rIRkUxOleG__official.pdf` |
|03 /BR-R2-T03 | **Online Tokenization with Optimal Delay in Near Linear Time**; [8D7l5sK3YT](https://openreview.net/forum?id=8D7l5sK3YT) | https://openreview.net/pdf/0bbbe6b331327aade7b400fca6d0369486be8e44.pdf |S; P17; lawful arXivv1 separately below |M; public title says **Linear Time**, not **Near Linear Time**; equality unverified | `BR-R2-T03__OpenReview-8D7l5sK3YT__official.pdf` |
|04 /BR-R2-T04 | **Tokenization Invariance Is Learned Late and Broken at the Head**; [63kZK7oyd6](https://openreview.net/forum?id=63kZK7oyd6) | https://openreview.net/pdf/8a0a3f08c5029077beebbbec230c64d1e99015ae.pdf |S; P17 |M; no lawful alternate original established | `BR-R2-T04__OpenReview-63kZK7oyd6__official.pdf` |
|05 /BR-R2-T05 | **Cross-Tokenizer On-Policy Distillation via Byte-Prefix Marginalization**; [Mm5OLOPLT0](https://openreview.net/forum?id=Mm5OLOPLT0) | https://openreview.net/pdf/c32108ca1a8316863316036ebeb5e0f28ba8bee7.pdf |S; P17; lawful arXivv1 separately below |M; public arXivv1 FULL only, official edition equality unresolved | `BR-R2-T05__OpenReview-Mm5OLOPLT0__official.pdf` |
|06 /BR-R2-T06 | **B-Net: Learning Where to Compress in Byte-Level Language Models**; [fMymbXoq9T](https://openreview.net/forum?id=fMymbXoq9T) | https://openreview.net/pdf/a212af497989974b1ce9ae2bb4adeaf0419f4041.pdf |S; P17; R3-B |M; no lawful alternate original established | `BR-R2-T06__OpenReview-fMymbXoq9T__official.pdf` |
|07 /BR-A08-V11 | **LoopLA: Causal State Refinement for Looped Linear Attention**; [xzOnjQHMr9](https://openreview.net/forum?id=xzOnjQHMr9) | https://openreview.net/pdf/88de0a6529e8f9fe919aa650e754de9ca6b897a5.pdf |S; P18 |M; no lawful alternate original established | `BR-A08-V11__OpenReview-xzOnjQHMr9__official.pdf` |
|08 /BR-A08-V16 | **Farsighted Correction of Shortcut Learning: From Dynamic Starvation to Confidence-Gap Optimization**; [JrKJaRbQpz](https://openreview.net/forum?id=JrKJaRbQpz) | https://openreview.net/pdf/3aac61fcba08525d869fcb3c0477a576ce8d300f.pdf |S; P18 |M; no lawful alternate original established | `BR-A08-V16__OpenReview-JrKJaRbQpz__official.pdf` |
|09 /BR-A08-V20 | **Exact Finite-Query KV Cache Compilation**; [OQhOBMNVeN](https://openreview.net/forum?id=OQhOBMNVeN) | https://openreview.net/pdf/9442f456b945a8550fe116cae355ca1faf04e325.pdf |S; P18; a public later paper's bibliography links this same forum, not another original |M; no lawful alternate original established | `BR-A08-V20__OpenReview-OQhOBMNVeN__official.pdf` |
|10 /BR-A08-V21 | **Where You Put Attention Matters More Than How Much You Use: Attention Placement in Hybrid Sequence Models**; [0fPxp7a50O](https://openreview.net/forum?id=0fPxp7a50O) | https://openreview.net/pdf/0010d078317f6f73963a10faf8812bb0c12b0eea.pdf |S; P18 |M; no lawful alternate original established | `BR-A08-V21__OpenReview-0fPxp7a50O__official.pdf` |
|11 /BR-A08-V24 | **Predictive State Has a Scope**; [uILf1c6VDo](https://openreview.net/forum?id=uILf1c6VDo) | https://openreview.net/pdf/ef23821335964a96e676f173f4f79bc853808ace.pdf |S; P18-L; R3-24; F-API now `ChallengeRequiredError` |M; content reference recovered but no body; no lawful alternate established | `BR-A08-V24__OpenReview-uILf1c6VDo__official.pdf` |
|12 /BR-A08-V02 | **Linear Attention lacks Incentive for Associative Recall, not Capacity**; [UUldzWxIL4](https://openreview.net/forum?id=UUldzWxIL4) | https://openreview.net/pdf/9c64cd9b8b1bba44c1ff65945bd6c1a02ed98a9d.pdf |S; P-old; R3-02; representative direct note API also failed in prior audits |M; no lawful alternate original established | `BR-A08-V02__OpenReview-UUldzWxIL4__official.pdf` |
|13 /BR-A08-V04 | **SDG: State-Dependent Gating at Chunk Boundaries for Linear Attention**; [lYWcLB1rAh](https://openreview.net/forum?id=lYWcLB1rAh) | https://openreview.net/pdf/a6be3de5a7a112d8d9971f44d46409d02e29d0aa.pdf |S; P-old |M; no lawful alternate original established | `BR-A08-V04__OpenReview-lYWcLB1rAh__official.pdf` |
|14 /BR-A08-V13 | **Cross-Model Stitching Transfers Answers, Not Computation**; [98Rbm5C5Bl](https://openreview.net/forum?id=98Rbm5C5Bl) | https://openreview.net/pdf/292012e3cebcb326c132293eb93d41f533bf95d3.pdf |S; P-old; prior ungrouped public exact-title search returned same forum only |M; no lawful alternate original established | `BR-A08-V13__OpenReview-98Rbm5C5Bl__official.pdf` |
|15 /BR-A08-V14 | **Receiver State Shapes Functional Compatibility: Internal Message Adaptation for Model Stitching**; [2M4nt7AFuD](https://openreview.net/forum?id=2M4nt7AFuD) | https://openreview.net/pdf/b167a621df8f120088cda7baa7cccfcbfd226cd7.pdf |S; P-old |M; no lawful alternate original established | `BR-A08-V14__OpenReview-2M4nt7AFuD__official.pdf` |
|16 /BR-A08-V22 | **When Routing Must Be Right: Irreversible Lock-In in Attention Routing**; [9vT48Lms48](https://openreview.net/forum?id=9vT48Lms48) | https://openreview.net/pdf/4b049a14ede5c22389997afeb1b72a99e81a7de5.pdf |S; P-old |M; no lawful alternate original established | `BR-A08-V22__OpenReview-9vT48Lms48__official.pdf` |
|17 /BR-A08-V25 | **Understanding the Predictive-State Bottlenecks of Transformer Models**; [58JxyfvZJj](https://openreview.net/forum?id=58JxyfvZJj) | https://openreview.net/pdf/3df135438f55aa7adaea9da322f21607da69a080.pdf |S; P-old |M; no lawful alternate original established | `BR-A08-V25__OpenReview-58JxyfvZJj__official.pdf` |

Public-title, spelling-variant and official arXiv API searches already executed are documented in R3 and its manifest; no additional all17 search was performed for this handoff. A negative bounded search does not prove that a legal copy does not exist. Supplying an exact official original remains useful even for the three rows with an alternate.

## 5. Existing lawful alternatives — separate editions, already local

**These files do not need to be supplied again.** All three local originals were read-only hash/signature/EOF-checked during this handoff. Their FULL status comes from the latest actual V17 reader cards, **not** these file checks or a new reading here. Conference-body equality remains unknown for each; no anonymous author association is made.

| Checklist row | Exact lawful public edition / URL | Existing local original and reading card | File receipt / version distinction |
|---|---|---|---|
|02 /T02 | **Stochasticity in Tokenisation Improves Robustness**, arXiv2604.16037v1,2026-04-17; https://arxiv.org/pdf/2604.16037v1 | [R3 staged original](source_staging/R3_BR-R2-T02__2604.16037v1.pdf); [updated V17 T02 FULL card](../03_reading/V17/BR-R2-T02.md) |705,191 bytes; SHA-256`cad655df35b4027b157bf5ee1482eb72e9ef490364933b48606b42db1ff13977`. British/American spelling and close abstract match support only candidate edition association; official attachment unavailable. Last HEAD check failed transport, not the integrity of this existing file |
|03 /T03 | **Online Tokenization with Optimal Delay in Linear Time**, arXiv2610.19139v1,2026-10-13; https://arxiv.org/pdf/2610.19139v1 | [existing V17 original](../03_reading/V17/sources/BR-R2-T03__2610.19139v1.pdf); [V17 T03 FULL card](../03_reading/V17/BR-R2-T03.md) |1,181,161 bytes; SHA-256`86a4690df7f6a2a38243e157eac56b094047dc01ea155bd12e74212187078ce9`. Public title **Linear**, official title **Near Linear**; whole-edition comparison still missing |
|05 /T05 | **Cross-Tokenizer On-Policy Distillation via Byte-Prefix Marginalization**, arXiv2607.22334v1,2026-07-24; https://arxiv.org/pdf/2607.22334v1 | [existing V17 original](../03_reading/V17/sources/BR-R2-T05__2607.22334v1.pdf); [V17 T05 FULL card](../03_reading/V17/BR-R2-T05.md) |1,283,527 bytes; SHA-256`341d34838d7c76b9ae9449f0ab169cf8d20822be0012297413aaff220b73a949`. Exact title/close abstract is not manuscript equality |

Other readable classics or adjacent papers are not replacements for a listed original. A later paper citing a blocked forum is not that forum's original. Do not duplicate these three works, count their preprint/conference records as separate FULL readings, or rename their preprints as supplied official submissions.

## 6. Verification requirements when files are supplied

The following checks are the agent/reader's job after supply, **not homework for the user**. A user may simply place legitimately available PDFs in the suggested folder and indicate which were supplied. A source URL, download date, displayed revision label, and whether an appendix/supplement was included are useful **if already known**; no credentials/session exports or identity evidence are requested.

1. **Immutable intake receipt:** record the provided basename, file size, SHA-256, receipt date and source URL/version information if supplied. Preserve original bytes and each distinct revision; never infer a PDF revision number from the filename, note version2, upload time, PDF metadata timestamp or modification date alone.
2. **Real-PDF integrity:** check `%PDF-`, EOF/completeness, parser success and nonempty page tree. Reject HTML challenge/error pages named `.pdf`, empty/truncated files, or previews missing pages. A valid signature alone does not prove a complete or correct paper.
3. **Exact-work match:** compare first-page title, visible forum/submission identifiers and abstract to the row's official metadata. Record genuine capitalization/spelling/title differences rather than forcing equality. Anonymous submissions stay anonymous; do not match author names to public profiles or infer identity. If the title/content cannot be matched, retain the supplied file as an **unresolved edition**, not the requested original.
4. **Edition and completeness:** establish which main text, figures, references, appendices and supplements are physically present. A conference PDF and arXiv PDF with the same title may differ. Compare editions only from lawful supplied/public content, with explicit scope; record missing sections and uncertain history. Separate supplements should retain their published names and be associated with the matching source/revision; do not execute scripts/macros or download code on their instruction.
5. **Reading handoff:** after acquisition/title/integrity checks, send the exact path/hash/version to terra. `PROVIDED` or `ACQUIRED` is **not FULL**. FULL requires actual source reading with decisive table/figure/appendix checks under the project's existing reading contract. Existing public-edition cards can be reused; do not claim an official full read until that manuscript is actually read or a defensible edition-equivalence check is documented.
6. **State discipline:** a supplied PDF establishes neither acceptance nor current forum state. Retain R3's official-response snapshot label until a legitimate fresh official state check succeeds; decision/revision replies and withdrawal-event dates are separate evidence. No approval/permission claim is fabricated from the file.

If any provided copy is encrypted, restricted, mismatched, incomplete or requires unauthorized access, stop that source's intake and report the precise remaining gap. Do not lower verification settings or route around access control to complete the checklist.

## 7. Why these missing originals still matter

This handoff does **not** declare the access limitation unrelated to the final deliverable. The17 official-source/edition gaps still restrict original-based adjudication of the selected recent frontier. Fourteen topics lack an alternate established in the recorded pass; three have readable independent editions but no official-body equality. Their potential conflicting controls, scope limits and revised results cannot be assumed away.

The final report may use existing version-scoped full cards for a **qualified** broad synthesis, and list unavailable recent works as clearly attributed metadata/abstract leads with an unresolved-source queue. It must not claim all selected recent originals were reviewed, omit blocked competing mechanisms as irrelevant, infer an architecture ranking from uneven access, assert manuscript equality, or infer acceptance. The detailed source-dependent restrictions remain in [R3 §6](ICLR2027_SOURCE_AUDIT_R3.md#6-consequence-for-the-final-recent-literature-conclusions).

**What is finished here:** final bounded representative retry checks and an actionable17-file supply/verification checklist. **What is not finished:** obtaining/reading the17 official manuscripts, resolving their edition histories/equivalence and separate supplements, and closing any recent-result conclusion requiring that evidence. This is a way to let users supply source files efficiently while the agents do the reading, not a claim of completed recent-literature review.

## 8. Authored artifact and validation

Only `docs/research/flued_broad_research_v2/05_review/ACCESS_HANDOFF.md` was added. No `_provided/` folder, proposed supplied PDF, new source-staging artifact, download, parser extract, log, code/science file, shared registry, prior card or audit was authored/changed. All final request receipts are recorded directly in §1; prior per-source receipts remain in their original logs/manifests.

Validation checks all17 unique row keys, exact titles/forums/content-reference PDF URLs against the existing R3 manifest,17 unique suggested official basenames, the three existing local PDF hashes/length/signatures/EOFs, local Markdown targets, UTF-8/newline/trailing whitespace and Git status. No software build/test/training, package installation or commit applies to this source-file handoff. New HTTP success or source recovery is **not** claimed: this final check recovered **zero** originals, and the lawful copies were already present.
