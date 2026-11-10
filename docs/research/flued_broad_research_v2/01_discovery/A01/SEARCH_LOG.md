# A01 — Executed search and source-access log

**Executed:** 2026-11-09. This is an actual discovery log, not a search plan. Only public scholarly titles/concepts/IDs were sent externally; no project documents, internal observations, paths, unpublished configurations or code were uploaded. No academic data-source API was used, so no academic API/skill invocation was needed. Web work used WebSearch/FetchURL and the built-in Desktop browser; no personal logged-in browser or authentication bypass.

## 1. Local scope and reuse inspected

Read completely: v2 `PLAN.md`; canonical `07_scope_recovery/FOLLOWUP_DIRECTIONS.md`; previous `01_COMPRESSION/COVERAGE_AUDIT.md` and `READING_RECOMMENDATIONS.md`. The preceding audit's SEARCH_LOG was located but not reread; today's searches and access results below are independent events, not inherited successes.

Searched the old `02_catalog` and byte-interface `02_inventory` for compression, bottleneck, collapse, sufficiency, distortion, autoencoding and lagging inference. Read the relevant BIW-0094–0096 catalog blocks and the compression audit's five existing-unread/six discovery-lead metadata. Stable-ID/title dedup checked both full catalog texts for VLAE, Lucas, Dai, cyclical annealing, variance equalization, Boa and MemSafe; no match found for the seven new-to-catalog candidates. This does not search every prior discovery note or every parallel stream.

**Actual existing cards read in full in this pass (11):** W0059/B04, W0091/B04, W0092/B13, W0038/B24, W0023/B24, W0080/B24, W0061/B04, W0076/B13, W0011/B05, W0013/B24, and BIW-0006/R01. Scope/version and paths are in WORKS_AND_PROBLEMS §3. This is reuse of cards, not eleven new original-paper full reads. BIW-0094–96 remain partial catalog evidence; no nonexistent FULL card was substituted.

## 2. Exact external search queries

All are actual WebSearch calls, returned as bounded ranked lists. No date filter, pagination parameter, systematic venue scrape or exhaustive recall estimate was applied. Search timestamps/publication dates can be indexing dates (the 2021 ACL paper returned a 2026 timestamp); original version history/formal publication controls the record.

| Query | Exact public query string | Relevant result and disposition |
|---|---|---|
| Q01 | `"posterior collapse" "2026" variational autoencoder language decoder` | Found arXiv:2607.05531v1; fetched abstract and introduction. Many 2026-looking results were older papers/copyright dates; not treated as new work |
| Q02 | `"ICLR 2027" "compression" "latent" OpenReview` | Found venue-related leads and a public preprint referencing forum zKxUf16XnW. No snippet promoted to official acceptance |
| Q03 | `site:openreview.net/forum "ICLR 2027" "context compression"` | Found MpDEPJO8Aa, 1dBpTJv19B, Qit9HdVdT6 and other indexed forums. Three selected direct forum requests blocked |
| Q04 | `site:openreview.net/forum "ICLR 2027" "posterior collapse"` | Mostly unrelated results plus official group shell; no verified relevant collapse submission recovered. Not evidence of venue absence |
| Q05 | `site:openreview.net/forum "ICLR 2027" "sufficient" "compression"` | Returned compositional-generalization/typed-memory leads; no original content checked, so not substantive work records |
| Q06 | `"posterior collapse" "Don't Blame" linear VAE Lucas 2019` | Located NeurIPS 2019 original and arXiv:1911.02469; fetched official abstract |
| Q07 | `"Variational Lossy Autoencoder" "Information" Chen 2017` | Located arXiv:1611.02731 and secondary ICLR association. HTML invalid, original abstract succeeded; secondary venue claim not upgraded |
| Q08 | `"Avoiding Latent Variable Collapse" "2019" free bits` | Returned collapse references and NeurIPS/author material. Generative skip models remain a reserve lead; no original source recovery claimed |
| Q09 | `"Fix the Structural Bottleneck" "ComprExIT"` | Confirmed searchable title alias and public project location; not a substitute for resolving abs/HTML/PDF identity/version differences |
| Q10 | `"Autoencoding-Free Context Compression" "ICLR 2026"` | Located official proceedings hash dff28796c79e1a04c7a6182119ee899a and Boa, arXiv:2610.33006v1; fetched both official proceedings and Boa originals |
| Q11 | `"xRAG" site:proceedings.neurips.cc 2024` | Located official proceedings hash c5cf13bfd3762821ef7607e63ee90075; fetched formal abstract |
| Q12 | `"Learning source" "posterior collapse" "2026" latent` | No useful new original; no candidate admitted from generic/secondary results |
| Q13 | `"ICLR 2027" "rate" "sufficiency" compression` | Found arXiv:2609.32269 MemSafe. Original abstract/intro verified as preprint; apparent ICLR 2027 headings elsewhere not trusted as acceptance |

Other indexed titles from Q03, not opened and not counted: *In-Model Context Compression with Agentic Soft Token for Long-Horizon LLM Agents* (a4j6KMRWSL); *When Can Agents Forget Their Reasoning? ICLR for Long-Horizon Agent Context Compression* (KW0OmxsBUq); *BridgeComp: Prompt Compression via Reasoning …* (RM7paXamDX); *Risk-Controlled Evidence Selection for Retrieval-…* (UMvCtWwfNs); *Beyond Position Bias: Shifting Context Compression from …* (UVecrvuDvP). Their full titles, official state and actual claims require original access. They are not additional verified works.

## 3. Exact FetchURL access ledger

`OK-A` means metadata/abstract was read. `OK-P` means only listed selected body passages were read. `CHECK` means verification-page content, **not** a successful forum/paper read. `ERROR-PAGE` means the server returned a non-paper conversion page. Long HTML outputs were tool-truncated into saved text; targeted Read/Grep was used where stated, never equated with full reading.

| Event | Exact URL | Result and evidence ceiling |
|---|---|---|
| F01 | https://arxiv.org/html/2610.30493v1 | OK-P; returned ~120.8k characters. Read intro, §§2 definitions, §§4–5 results and §6.1; proofs/appendices not read completely |
| F02 | https://arxiv.org/html/2510.08907v4 | OK-P; returned ~59k characters. Read §§3–5 and ablation discussion; missing numeric table cells |
| F03 | https://arxiv.org/html/2602.03784v4 | OK-P; returned ~93.9k characters. Read intro and selected method/training/diagnostic sections including A.1.1–A.1.3; title/metadata reconciliation open |
| F04 | https://proceedings.mlr.press/v80/alemi18a.html | OK-A; formal ICML 2018 abstract/bibliography |
| F05 | https://arxiv.org/html/2607.05531v1 | OK-P intro only; returned ~76.7k characters; no complete theory/experiment read |
| F06 | https://openreview.net/forum?id=MpDEPJO8Aa | CHECK; human verification/sign-in suggestion, no forum original |
| F07 | https://openreview.net/forum?id=1dBpTJv19B | CHECK; no original |
| F08 | https://openreview.net/forum?id=zKxUf16XnW | CHECK; no original |
| F09 | https://openreview.net/forum?id=Qit9HdVdT6 | CHECK; no original |
| F10 | https://arxiv.org/abs/1901.05534v2 | OK-A; 2019-01-28 history and lagging-inference abstract |
| F11 | https://aclanthology.org/K16-1002/ | OK-A/metadata; formal CoNLL 2016 title/authors/pages/DOI; not body |
| F12 | https://arxiv.org/abs/1702.08139v2 | OK-A; dilation/context/latent tradeoff, version 2017-06-18 |
| F13 | https://arxiv.org/abs/1808.07593v4 | OK-A; three caveats, deterministic target conditions, 2019-02-08 |
| F14 | https://arxiv.org/abs/2504.13191v1 | OK-A; specified operating-point universality, MNIST, 2025-04-12 |
| F15 | https://arxiv.org/html/2305.14788v2 | Network error; paper not read through this route |
| F16 | https://arxiv.org/abs/2405.13792v2 | Network error; subsequently retried once |
| F17 | https://openaccess.thecvf.com/content/CVPR2022/html/Wang_Rethinking_Minimal_Sufficient_Representation_in_Contrastive_Learning_CVPR_2022_paper.html | OK-A; formal CVPR metadata/abstract |
| F18 | https://arxiv.org/abs/2305.14788v2 | OK-A; legitimate fallback for F15, original page explicitly says accepted EMNLP 2023 |
| F19 | https://arxiv.org/abs/2405.13792v2 | OK-A; one retry of F16 succeeded, 2024-12-09 history |
| F20 | https://arxiv.org/html/1611.02731v2 | ERROR-PAGE; conversion-error instructions, not original paper |
| F21 | https://proceedings.neurips.cc/paper/2019/hash/7e3315fe390974fcf25e44a9445bd821-Abstract.html | OK-A; original Lucas et al. abstract, formal venue |
| F22 | https://arxiv.org/abs/1711.00937v2 | OK-A; VQ-VAE abstract/history, v2 2018-05-30 |
| F23 | https://arxiv.org/html/2305.17295v2 | OK-P; ~54.6k characters. Read task-distortion formulation and Theorems 1–2/2.A with example; proof appendix not read |
| F24 | https://arxiv.org/abs/1611.02731v2 | OK-A; legitimate fallback for F20, 2017-03-04 |
| F25 | https://proceedings.mlr.press/v119/dai20c.html | OK-A; ICML 2020 original abstract/metadata |
| F26 | https://aclanthology.org/N19-1021/ | OK-A; NAACL 2019 cyclical annealing abstract/metadata |
| F27 | https://arxiv.org/abs/2607.05531v1 | OK-A; 2026-07-06 version history and abstract |
| F28 | https://arxiv.org/abs/2602.03784v4 | OK-A; 2026-06-18 history; code-status text differs from served HTML |
| F29 | https://arxiv.org/abs/2510.08907v4 | OK-A; 2026-03-11 history; first upload 2025-10-10 |
| F30 | https://arxiv.org/abs/2610.30493v1 | OK-A; 2026-10-21 history; no acceptance established |
| F31 | https://proceedings.iclr.cc/paper_files/paper/2026/hash/dff28796c79e1a04c7a6182119ee899a-Abstract-Conference.html | OK-A; official SAC ICLR 2026 proceedings original, not 2027 |
| F32 | https://proceedings.neurips.cc/paper_files/paper/2024/hash/c5cf13bfd3762821ef7607e63ee90075-Abstract-Conference.html | OK-A; official xRAG NeurIPS 2024 abstract/DOI |
| F33 | https://arxiv.org/html/2610.33006v1 | OK-P; ~52.7k characters. Read intro and selected method/learning/interface/ablation statements; no full appendices/tables |
| F34 | https://arxiv.org/abs/2610.33006v1 | OK-A; v1 2026-10-07 history, same method abstract |
| F35 | https://arxiv.org/abs/2305.17295v2 | OK-A; v2 2025-03-04 history; formal journal status unverified |
| F36 | https://arxiv.org/abs/2609.32269v1 | OK-A; v1 2026-09-26, both positive and negative sufficiency-estimation results |
| F37 | https://arxiv.org/html/2609.32269v1 | OK-P introduction/figure description only; ~80.6k characters returned, not a full read |
| F38 | https://openreview.net/pdf?id=1dBpTJv19B | CHECK; one legitimate public PDF-route retry of F07; no PDF obtained |
| F39 | https://openreview.net/pdf?id=zKxUf16XnW | CHECK; one legitimate public PDF-route retry of F08; no PDF obtained |
| F40 | https://openreview.net/pdf?id=Qit9HdVdT6 | CHECK; one legitimate public PDF-route retry of F09; no PDF obtained |

No PDF bytes were manually downloaded or written. Formal PDF links elsewhere are accurate **targets**, not claims that the source was fetched. Future approved downloads must use the explicit project paths in READING_HANDOFF, never `/tmp` or Downloads. Tool-managed text-result storage is not represented as a manually curated source archive or a PDF artifact.

## 4. Built-in browser checks and ICLR 2027 coverage ceiling

1. Created a background Desktop-browser tab for https://openreview.net/group?id=ICLR.cc/2027/Conference. The tab title was “ICLR 2027 Conference | OpenReview”, but a document snapshot showed only OpenReview/Login/Loading/footer, no papers or official status list. This verifies the page shell/title, **not the group membership inventory**.
2. Attempted navigation of that tab to MpDEPJO8Aa; tool returned `TAB_NOT_FOUND`. It disappeared before navigation; cause unknown. This is a transient tool-state failure, not proof of a nonexistent forum.
3. Created one replacement background tab directly at https://openreview.net/forum?id=MpDEPJO8Aa. It redirected to `openreview.net/challenge?...` and showed “Verifying your browser”. No challenge was solved or bypassed; no sign-in attempted. Closed only that self-created replacement tab. No other source/user/parallel-work tabs were closed.
4. Remaining three selected forums received exactly one additional public PDF-route attempt each (F38–F40), also verification pages. Stop rather than repeatedly probing or circumventing the check.

The browser had more than ten existing tabs (approximately 81 other tabs), making the sidebar crowded; ownership was preserved and only the known self-created replacement was closed. No new persistent tab is intentionally left by this pass.

**No verified ICLR 2027 original paper in this axis pass.** Search-index associations are provisional submission leads only; actual anonymous forum title, revision date, invitation/group and decision/withdrawal status are missing. No conference count, acceptance inference, author match, deanonymization or review-based experimental finding was fabricated. The independent venue stream may later supply verified originals; it must preserve today's access limitations as provenance rather than silently relabeling them.

## 5. Source issues and stop decisions

- **SAC:** official 2026 publication verified through proceedings, but v4/formal numerical identity remains open. Table-cell omission blocks specific ablation numbers, not the fact that original ablation discussion exists.
- **ComprExIT:** exact arXiv version history verified; served HTML title prefix, author presentation and code-release text are not safely reconciled with abs. Keep original-page observations separate until fixed PDF confirmation. Never use the submitter as a substitute author list.
- **Boa:** HTML author/affiliation formatting malformed; no reconstructed author order. Context length/stride implies growing retained sequence, which changes a constant-state comparison regardless of author metadata.
- **VLAE:** bad HTML has one successful original-abstract fallback; not falsely logged as FULL or unavailable paper.
- **AutoCompressors/xRAG:** each initial network failure received one legitimate retry/alternative route, successful; no unbounded retries.
- **Search pagination:** 13 bounded queries, 40 FetchURL calls and the browser operations above. No entire arXiv category or OpenReview group was enumerated. No claim of systematic review, all-2026 coverage or field exhaustion.
- **Local tools:** four initial Grep calls used an invalid `C` key, were rejected before search, and were corrected to `-C`. They are local invocation errors, not external source failures or successful evidence checks.

## 6. Deliverable verification boundary

This is documentation/research work; pytest/model builds do not verify source conclusions and were not run. Final static checks validate four requested UTF-8 files, local links/card paths, record/queue identifiers, and directory scope. No tests/training, production code/config changes, installs, paid access, commit/push or evidence-registry edits were made. Initial git status already contained untracked old/new survey roots, bundles and another research document; those were left untouched. Final validation results are reported in the handoff and appended below if needed.

### Final static verification (completed)

Read-only Python validation passed: exactly the four requested files in A01; all decode as UTF-8 without replacement characters; all local Markdown links resolve; ordered R01–R21 records occur exactly once as work headings; priority headings are exactly 1–15; query ledger has Q01–Q13; fetch ledger has F01–F40; all 11 reused card paths exist. File lengths were approximately 22.4k, 22.7k, 15.0k and 40.1k characters before this verification note. No validator script, log, PDF or test artifact was created. `git status --short` was checked before and after; final status still lists the untracked v2 root plus pre-existing unrelated bundles/research document. Other survey roots changed status during parallel work; this agent did not modify/delete them or run git-mutating commands. No additional AGENTS.md was found under docs. Only these four A01 Markdown files were authored by this pass.
