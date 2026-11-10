# A06 — Executed search and original-source ledger

Date: 2026-11-09. Scope: component interaction, cross-host transplantation, compatibility, repair, controls and independent alternatives. This is a record of actual discovery, not a proposed future search.

## 1. Tools, privacy and source-depth discipline

Used actual `WebSearch`, `FetchURL`, local `Read`/`Grep`/`Glob`, and the Kimi Code Desktop built-in browser. No academic data-source plugin was used, so no academic API/skill was invoked. No new software, package, browser extension, paid access, authenticated login, source-code upload or internal-text search query was used.

All external search strings below are public paper/mechanism/venue terms. Internal documents were only read locally. No PDFs were downloaded: **there are no saved PDF paths or extracted PDF files to hand off**. Future authorized PDFs should be stored explicitly under `docs/research/flued_broad_research_v2/01_discovery/A06/sources/`, not Downloads or a temporary directory. Long FetchURL responses were automatically stored by the tool in session storage; these are not project-owned downloads and are not portable reading artifacts.

A page retrieved in full is not necessarily read in full. Actual consumption is reported below. Abstracts and snippets are never classified as full readings. Claims from the old audit are labeled inherited where not reverified; original full cards are reused, not reconstructed from snippets.

## 2. Local audit actually performed

Read:

- `../../PLAN.md`.
- `../../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md`.
- `../../../flued_multigranularity_survey_20261108/07_scope_recovery/06_COMPOSITION_TRANSFER/{COVERAGE_AUDIT,SEARCH_LOG,READING_RECOMMENDATIONS}.md`.
- Actual complete existing cards `03_reading/B16/W0337.md`, `B16/W0204.md`, `B06/W0210.md`, `B16/W0214.md` under the multigranularity survey, and `03_reading/R06/BIW-0122.md`, `R06/BIW-0126.md` under the byte survey.
- Targeted old main catalog rows for W0201/W0228 and keyword searches of both supplied catalog/inventory trees.

Additional-work duplicate check: case-insensitive stable-ID/title search across old `02_catalog/` and byte `02_inventory/` for `1511.05641|1606.04671|2209.04836|2505.20142|2506.20480|2306.01708|2212.04089|1611.09913|Functional Alignment Can Mislead|KLAS` returned no matches. This checks these inventories, **not all files, all web literature or concurrent new v2 catalogs**. Earlier N06 aliases remain recovered discoveries even though absent from the old central W catalog. No old survey counts or statuses were modified.

No more-specific docs AGENTS.md was found. Initial `git status --short` already showed the survey roots and bundles as untracked. Do not treat those as created by this stream or remove them.

## 3. Actual WebSearch strings (19 queries)

| Query | Exact public search string | Decision / result |
|---|---|---|
| Q01 | `site:openreview.net "ICLR 2026" "stitching"` | Found GPTailor, KLAS and invariance-aware forum; excluded trajectory/image-stitching papers without a relevant model-interface protocol. |
| Q02 | `site:openreview.net "ICLR 2027" "linear" "distillation"` | Found WRilIg5UPY candidate; only snippet, official verification pending. Unrelated image-generation/agent results not adopted. |
| Q03 | `site:openreview.net "ICLR 2027" "stitching"` | Mostly graph expressivity, trajectory or visual scene stitching; not treated as component-transplant coverage. No confirmed new relevant paper from this query alone. |
| Q04 | `site:openreview.net "ICLR 2027" "transplant"` | Found OFVWcaGfdi, TkiAbEpo95 and QlvNqskhdY leads; preserved as blocked candidates, not scientific evidence. |
| Q05 | `model stitching 2025 2026 component transfer frozen networks feature matching functional alignment ICLR` | Found invariance-aware v2, Smith ICML 2025 and Mai CVPR 2026; followed original pages. |
| Q06 | `ICLR 2025 2026 model merging ablation interaction TIES DARE task arithmetic low rank transplant` | Broad model-merging hits mainly surveys/secondary pages; no effect claims adopted from them. Redirected to named originals Q17/Q18. |
| Q07 | `"Functional Alignment Can Mislead" ICML 2025` | Located official ICML poster and later PMLR source, confirming original counterexample metadata. |
| Q08 | `"Git Re-Basin" ICLR 2023 permutation merging` | Located arXiv v6; used original symmetry formulation rather than third-party summary. |
| Q09 | `"Net2Net" "ICLR 2016" function preserving` | Located stable 1511.05641 through citations; original v4 fetched. No secondary result used for experimental numbers. |
| Q10 | `"Progressive Neural Networks" 2016 lateral transfer frozen` | Located original 1606.04671v4; used random frozen-source control and source/target protocol. |
| Q11 | `"LoLCATs" "ICLR 2025" site:iclr.cc` | Located official proceedings abstract/PDF endpoints; proceedings abstract fetched and v3 body used separately. |
| Q12 | `"Model Stitching" "ICLR 2026" "Invariance"` | Found related ICLR forum and current repository/ICML claim; title/author/venue mismatch retained as unresolved, not silently merged. |
| Q13 | `"Model Stitching by Invariance-aware Functional Latent Alignment" site:proceedings.iclr.cc` | No independently matching proceedings entity in returned results. Unrelated references do not resolve identity. |
| Q14 | `"GPTailor" site:proceedings.iclr.cc/paper_files/paper/2026` | Located official accepted-paper abstract/PDF; accepted ICLR 2026 verified. |
| Q15 | `"KLAS: Using Similarity" site:iclr.cc` | Located official ICLR 2026 poster and proceedings PDF; reconstructed matching official abstract endpoint and fetched it successfully. |
| Q16 | `"GPTailor" arxiv` | Located 2506.20480v1 original body; read optimization and search-space ablation passages. |
| Q17 | `"TIES-Merging" 2306.01708 original` | Search biased toward secondary summaries; fetched known stable original ID and official NeurIPS source instead. |
| Q18 | `"Editing Models with Task Arithmetic" ICLR 2023` | Located 2212.04089 and OpenReview identifier; used original versioned arXiv, not unverified citation snippets. |
| Q19 | `"KLAS: Using Similarity to Stitch Neural Networks" arxiv` | Located 2605.29259v1; official history resolves inconsistent search-display date. |

Search responses were bounded ranked results with no total-recall guarantee; no search-engine pagination or comprehensive venue dump was performed. No claim of exhaustive ICLR 2027 coverage is made. A result returned only in a citation list is not treated as original-source verification.

## 4. Successful primary-source retrievals and actual reading scope

Each listed URL was actually fetched in this stream. Repeated entity versions are not distinct works. Rows intentionally distinguish metadata from selective body reading.

| Original URL(s) actually fetched | Result and actual use |
|---|---|
| https://arxiv.org/html/1411.1792v1 | Successful original body; §§2–4.3 and training appendix selectively read. Verified reset/relearn meaning of BnB and frozen/adaptive controls. Not FULL. |
| https://arxiv.org/html/2106.07682v1 | Successful long response; abstract/introduction used. Method training budget/appendix not newly full-read. |
| https://arxiv.org/html/2412.11299v1 | Successful long response; abstract, introduction and matching rationale. Detector appendix not fully audited. |
| https://arxiv.org/html/2603.12433v3 | Successful long response; §§3.2–5.3 and self-stitch/weak-source controls consumed. Local matching vs final matching, interface families; table cells not exhaustively recovered. |
| https://arxiv.org/abs/2307.15771v1 | Successful original abstract/history only. Hydra not counted as full reading. |
| https://proceedings.mlr.press/v235/rushing24a.html | Successful official ICML 2024 metadata, abstract and stable formal PDF link. Did not read full PDF. |
| https://arxiv.org/html/2410.10254v3 | Successful body; §§3.1–3.3 opening and Table 2 cells read. Both stages, trainable sets and 2+2 vs 4 epoch control confirmed. |
| https://proceedings.iclr.cc/paper_files/paper/2025/hash/72163d1c3c1726f1c29157d06e9e93c1-Abstract-Conference.html | Successful official LoLCATs proceedings abstract; ICLR 2025 formal publication confirmed. Version difference from v3 not fully compared. |
| https://arxiv.org/html/2408.10189v2 | Successful long response; §4 and selected §5/control passages read using saved output search. Gate/convolution identity initialization, removed norm/nonlinearity, same-architecture recovery control confirmed. Full tables/appendix not audited. |
| https://arxiv.org/abs/2510.19266v4 | Successful CAB abstract/history; first submission and v4 dates verified. No new body/table reading. |
| https://arxiv.org/html/2610.11214v1 | Successful long response; §5.3 and Appendix Table 12 discussion located/read. Tokens reassigned after stage removal confirmed. HTML omits numerical table cells: no fresh certification of old exact values. |
| https://arxiv.org/html/1707.05589v2 | Successful after a very slow response; targeted §5.1/§7 read. No retry, no reproduction. Single-feature rather than factorial scope confirmed. |
| https://arxiv.org/html/2607.07706v1 | Successful long response; strict frozen training, §4 and App. C read. 10M tokens, QKV freeze, cache split, convolution/LoRA caveat and no-sweep policy confirmed. Table cells omitted: directional prose not numeric full-table verification. |
| https://arxiv.org/html/1511.05641v4 | Successful original body; §§2.1–2.4/3 and App. A selectively read. Positive/negative baselines and function-preserving constraints inspected. No original FULL claim. |
| https://arxiv.org/html/1606.04671v4 | Successful body; §§2–3/5.1–5.3/limitations read for frozen columns, random-source control, new capacity, top-3-of-25 selection and negative-transfer discussion. Figure points not independently extracted. |
| https://arxiv.org/html/2209.04836v6 | Successful long response; §2 symmetry and §3 matching premise, abstract/limitations. No independent theorem/counterexample proof verification. |
| https://icml.cc/virtual/2025/poster/44458 | Successful original conference abstract, Smith work; later formal PMLR metadata below adopted. |
| https://proceedings.mlr.press/v267/smith25a.html | Successful formal ICML 2025 metadata/abstract and PDF endpoint. Full paper still unread; clustered-noise construction specifically queued. |
| https://arxiv.org/html/2505.20142v2 | Successful long response; §2–3 and App. D selectively inspected. Approximate identically represented inputs, pseudoinverse initialization, internal hints and assumptions recorded. |
| https://arxiv.org/abs/2505.20142v2 | Successful official history: v1 2025-05-26, v2 2026-06-01. Does not verify association to related ICLR forum. |
| https://proceedings.iclr.cc/paper_files/paper/2026/hash/5c99f2254833533c2a8ca0e0be04d77e-Abstract-Conference.html | Successful accepted GPTailor ICLR 2026 proceedings abstract. |
| https://arxiv.org/html/2506.20480v1 | Successful long response; §3.4/§4.3–4.4 optimization, trial budget, calibration and ablation prose read. Not final-PDF equivalence or full-table audit. |
| https://proceedings.iclr.cc/paper_files/paper/2026/hash/e9f0ce998bede73f8068985f3deeab9a-Abstract-Conference.html | Successful official KLAS ICLR 2026 abstract; accepted status separate from arXiv metadata. |
| https://arxiv.org/abs/2605.29259v1 | Successful original abstract/history: v1 2026-05-28. No full reading; contradicts a search-display 2025 date. |
| https://arxiv.org/abs/2306.01708v2 | Successful TIES abstract/history; v2 2023-10-27. |
| https://arxiv.org/html/2306.01708v2 | Successful long body; introduction, sign conflicts, formulation and §7.2–7.4 selective text. §7.2 changes update direction on an already successful model and contrasts top-magnitude vs bottom-magnitude deltas; §7.4 uses multitask sign oracle (extra information, not a legal no-data baseline). Full ablation table not independently extracted. |
| https://proceedings.neurips.cc/paper_files/paper/2023/hash/1644c9af28ab7916874f6fd6228a9bcf-Abstract-Conference.html | Successful official TIES NeurIPS 2023 abstract/DOI 10.52202/075280-0310; author full-read/replication not implied. |
| https://arxiv.org/abs/2212.04089v3 | Successful task-arithmetic abstract/history; v3 2023-03-31. |
| https://arxiv.org/html/2212.04089v3 | Successful long body; abstract/introduction/formulation used, not all experiments. |
| https://arxiv.org/abs/1611.09913 | Successful capacity/trainability abstract/history, latest v3 2017-03-03. |
| https://arxiv.org/html/1611.09913v3 | Successful body; §1.1–1.2 and original abstract read, intensive tuning/parameter-envelope protocol confirmed. Results tables not FULL-read. |
| https://api2.openreview.net/groups?id=ICLR.cc/2027/Conference | Successful public JSON, count=1/fromCache=true. Official group ID/domain/title and active/withdrawn/desk-rejected identifiers confirmed. No individual note status established. |

**Additional direct intervention extraction:** TIES §7.2 is a useful “damage a positive model” protocol: independently flip directions of high-magnitude task updates with probability p, versus bottom-magnitude updates, then evaluate. §7.4's multitask sign vector is a deliberately more-informed restorative reference. A project analogue must make the repair information budget explicit; it cannot call the oracle free. This is selective original-body evidence, not an abstract inference.

## 5. OpenReview/venue access failures, legitimate alternatives and stopping

These were public access problems, not invitations to bypass checks. No challenge-solving, credential use, proxy or identity research was attempted. At most the ordinary forum and official public API routes were used for a lead; after failure, it remains blocked.

| Attempted URL | Actual result / consequence |
|---|---|
| https://openreview.net/group?id=ICLR.cc/2027/Conference | Fetch returned login/loading shell, not conference content. Built-in browser create returned `TAB_NOT_ACTIVE` because shared control changed. Later read-only DOM inspection of a loaded group tab also showed only loading shell. Public group API above succeeded, so group existence/configuration is verified, not paper membership. |
| https://openreview.net/forum?id=hJvcbkf2nO and https://api2.openreview.net/notes?id=hJvcbkf2nO | Both returned browser-verification page. Related title/author/venue mismatch with arXiv 2505.20142v2 remains unresolved. |
| https://openreview.net/forum?id=iTaQmRWa7Y and https://api2.openreview.net/notes?id=iTaQmRWa7Y | Both verification pages. Legitimate independent official proceedings abstract succeeded; KLAS acceptance verified without claiming forum was read. |
| https://openreview.net/forum?id=yCTpYe3UOL and https://api2.openreview.net/notes?id=yCTpYe3UOL | Both verification pages. Legitimate independent official GPTailor proceedings succeeded. |
| https://api2.openreview.net/notes?id=QlvNqskhdY and https://openreview.net/forum?id=QlvNqskhdY | Both verification pages. ICLR 2027 candidate title completion, version/date, venueid and status remain unverified. |
| https://api2.openreview.net/notes?id=OFVWcaGfdi and https://openreview.net/forum?id=OFVWcaGfdi | API HTTP 403; ordinary forum verification page. No further retry or alternate proxy. No claim of accepted/pending/withdrawn actual status. |
| https://api2.openreview.net/notes?id=TkiAbEpo95 and https://openreview.net/forum?id=TkiAbEpo95 | Both verification pages. Candidate remains snippet-only. |
| https://openreview.net/forum?id=WRilIg5UPY | Verification page. No repeated failed fetching; candidate remains snippet-only. |
| https://iclr.cc/virtual/2026/papers.html | Returned unrelated Ukrainian network/DNS-configuration warning, not a paper list. Treated as failed content retrieval. Did not follow its instructions or modify network settings; official proceedings pages used instead. |

Browser operations were limited to the built-in browser: attempted create, state inspection, read-only text snapshot. No private-browser skill, user Chrome/Edge or signed-in session was used. The shared browser contained many unrelated tabs; none were modified/closed. The failed create did not give a confirmed owned tab ID, so no speculative cleanup of another worker's tab was performed.

## 6. Official ICLR 2027 facts versus non-facts

The successful public group response identifies:

- `id` and `domain`: `ICLR.cc/2027/Conference`.
- Title: The Fifteenth International Conference on Learning Representations; subtitle ICLR 2027.
- Submission invitation: `ICLR.cc/2027/Conference/-/Submission`.
- Active submission venueid: `ICLR.cc/2027/Conference/Submission`.
- Withdrawn and desk-rejected venueids distinct from active; `public_submissions=true`.
- The configuration contains accept-option strings. These are **workflow configuration, not acceptance decisions on any candidate**.

No forum JSON body, version/revision history, decision note or PDF body was successfully obtained for the four 2027 candidates. There was no paginated submission search, no count of the venue's relevant submissions, and no deanonymization. Retrying actual forum/status retrieval when public access works is an explicit source-resolution task in the handoff, not hidden behind an inflated “verified 2027” count.

## 7. Reading and coverage limits

Twenty-two externally revisited/additional entities were substantively selected; six original full cards were reused; two known unread host papers are explicit gaps. This is not a new central total. Venue uncertainty remains for several arXiv-only associations. No all-field exhaustion, architecture-selection, implementation correctness, full-theorem audit or experimental-replication claim is supported. The precise 14-item full-read queue is in [READING_HANDOFF](READING_HANDOFF.md); known full cards need only focused reuse, not a second full-read count.
