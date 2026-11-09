# S07 search and reuse log

Date:2026-11-08. Public mechanism queries only. Read `PLAN.md` before work. Only S07 Markdown deliverables were intentionally written; no production changes, training, installation, commits, external upload, user-account browsing, custom temporary downloads or subagents.

## Actual scope and counts

- **28 works / 52 meaningful inventory records.** Existing CATALOG:15. CATALOG-absent candidates:13, of which2 already found in old recovery audits and11 newly found relative to the inspected old corpus. No global catalog additions or old-card status changes.
- **9 old evidence cards actually read in full as cards:** B08/W0351, B08/W0360, B22/W0511, B26/W0514, B14/W0355, B22/W0509, B24/W0038, B05/W0010, B14/W0356. These are reused reading, not9 new original FULL reads.
- **4 original papers partially inspected:** Char2Subword v3 §§3.1–3.3; ZeTT v2 §§2–3.2 plus located §5/AppB passages; Perceiver IO v3 §§3–4.1; Character-based NMT v1 abstract and §§2.5–2.6. Other fetched content is abstract/metadata or specification-level. **New FULL reads:0.** Receiving a large HTML response did not make it FULL.
- **8 successful live search queries**, all via Kimi Code Desktop built-in browser/Bing; **1 nondispatched TAB_NOT_ACTIVE error**, recovered by selecting our own tab then submitting the query. **28 FetchURL calls**, including one incomplete arXiv abstract extraction and one mistakenly guessed ACL identity subsequently excluded. No access denial was bypassed.
- Applicable docs/AGENTS search found no more specific instruction file. Initial/final `git status --short` used only for change-boundary inspection; parent survey/old corpus were already untracked and remain untouched outside our directory.

## Corpus inspected before new-claim synthesis

`docs/research/flued_multigranularity_survey_20261108/02_catalog/CATALOG.md`: beginning and targeted rows/identifier searches, not falsely claimed as human full reading of all543 rows. Title/stable-ID checks found no matching CATALOG entries for N01–N13; whole-directory recovery keyword search found Perceiver IO and distillation as prior recovery candidates.

Recovery reports actually read:
- `07_scope_recovery/07_BYTE_SURVEY/COVERAGE_AUDIT.md`
- `07_scope_recovery/07_BYTE_SURVEY/READING_RECOMMENDATIONS.md`
- `07_scope_recovery/06_COMPOSITION_TRANSFER/COVERAGE_AUDIT.md`
- Targeted search of `07_scope_recovery/03_ADDRESS_READOUT/SEARCH_LOG.md` and recommendations located Perceiver IO A05; not a claimed complete reread of that recovery stream.

The old reports motivated gaps but did not determine scientific inclusion. Actual cards supplied objectives, costs, transfer permissions and negative results; FLUED associations in old cards were not imported as organizing criteria.

## Exact live queries and outcome

| Query | Exact query text | Platform/provenance | Adopted result / exclusion / follow-up |
|---|---|---|---|
| Q01 | `character subword hybrid language model CharBERT Char2Subword byte distillation tokenizer transfer WECHSEL FOCUS ZeTT` | Built-in browser/Bing, DOM snapshot read | arXiv2010.12730,2011.01513; ACL WECHSEL. Fetch primary identities. Search date snippets such as “2 days ago” ignored for paper year. |
| Q02 | `FOCUS OFA ZeTT zero shot tokenizer transfer language model embedding initialization paper` | Same; first search attempt failed before dispatch because our tab was not active; activate then successful search/snapshot | ZeTT2405.07883 and FOCUS title; Fetch primary arXiv. A guessed ACL FOCUS URL returned unrelated scrambled-text paper; rejected. |
| Q03 | `"FOCUS" "OFA" "embedding" language models arxiv` | Same, DOM read | No useful OFA primary identification; mostly unrelated EO/graph material. Refine once. |
| Q04 | `"OFA" "embedding initialization" language` | Same, DOM read | OFA2311.08849; primary abs fetched. AngOFA and HyperOFA remain unverified leads, not added/counted. |
| Q05 | `"T-FREE" tokenizer free trigram language model` | Same, DOM read | arXiv2406.19223, title variants seen; fetch current and fixed v2 abs. Reject secondary summaries as quantitative evidence. |
| Q06 | `"Breaking the Token Ceiling" "Distilling" byte 2026` | Same, DOM read | Direct arXiv2609.12303 hit. Search engine AI summary explicitly not treated as proof of exact marginalization/scaling. Primary v1 abstract used. Already recovery N05, not new discovery. |
| Q07 | `"MIMICK" "Achieving Open Vocabulary" "Character" neural` | Same, DOM read | Weak broad result for hybrid NMT and embedding mimicry; formal ACL D17-1010 fetched separately. No new claims from unrelated iterative-refinement snippet. |
| Q08 | `"1511.04586" "title" Ling` | Same, DOM read | No decisive primary title in search. Fetch fixed HTML to verify; corrected title to **Character-based Neural Machine Translation**, not distinct referenced **Finding Function in Form**. Read targeted historical staged-training/auxiliary-supervision paragraphs. |

Three own background browser tabs were used:1373,1383,1691. Shared browser had many pre-existing/other-agent tabs; did not close or control those. Sidebar crowding (>10 tabs) was noted. Own tabs closed at completion.

## FetchURL audit (28 actual calls)

A/P/S indicate inspected depth, not server response size. A page containing a linked PDF is not a PDF reading.

| # | Requested URL | Result and use |
|---|---|---|
| F01 | https://arxiv.org/abs/2010.12730 | A; Char2Subword abstract/history v1→v3. |
| F02 | https://arxiv.org/abs/2011.01513 | A; CharBERT v1. |
| F03 | https://aclanthology.org/2022.naacl-main.293/ | A; formal WECHSEL. |
| F04 | https://arxiv.org/abs/2405.07883 | A; ZeTT v1 and2025 v2 history; versions not assumed equivalent. |
| F05 | https://aclanthology.org/2023.emnlp-main.550/ | **Wrong guessed identity**: scrambled-text resilience paper, not FOCUS. Excluded, no work/record count. |
| F06 | https://arxiv.org/abs/1604.00788 | A; hybrid word-character NMT; v2 history. |
| F07 | https://arxiv.org/abs/1508.06615 | A; character-aware LM, word-output explicitly stated; v4 history. |
| F08 | https://arxiv.org/abs/1511.04586 | A; character-based NMT mechanism; title extraction missing, later F28 verifies. |
| F09 | https://arxiv.org/abs/2305.14481 | A; correct FOCUS identity/history v2. |
| F10 | https://arxiv.org/abs/2107.14795 | A; Perceiver IO, v3 history. |
| F11 | https://arxiv.org/abs/2609.12303v1 | A; byte distillation, v1. |
| F12 | https://arxiv.org/abs/2103.06874v4 | A; CANINE primary optional subword prior confirmed. |
| F13 | https://arxiv.org/abs/2106.12672v3 | A; Charformer actual byte interface confirmed despite character title. |
| F14 | https://arxiv.org/abs/2212.07284v1 | A; MANTa fixed v1 identity. |
| F15 | https://arxiv.org/abs/2311.08849 | A; OFA v2 history. |
| F16 | https://arxiv.org/html/2405.07883v2 | Long response tool-saved automatically; P §§2–3.2 read using paginated tool-output Read; §5 byte-conversion and AppB paragraph located. Most tables/appendices unread. |
| F17 | https://arxiv.org/html/2010.12730v3 | Long response tool-saved automatically; P §§3.1–3.3 read. Author extraction malformed, no guessed author list. |
| F18 | https://arxiv.org/html/2107.14795v3 | Long response tool-saved automatically; P §§3–4.1 read, remaining text unread. |
| F19 | https://raw.githubusercontent.com/google/sentencepiece/master/README.md | Current moving README inspected; historical/date-sensitive quantitative claims not used. Switched to tagged schema F20 for fallback semantics and defaults. Not another work. |
| F20 | https://raw.githubusercontent.com/google/sentencepiece/v0.2.0/src/sentencepiece_model.proto | S; `byte_fallback` default false, normalization/whitespace controls inspected. Tagged implementation, no runtime verification. |
| F21 | https://arxiv.org/abs/2406.19223 | A; T-FREE;v2 history. |
| F22 | https://aclanthology.org/D17-1010/ | A; formal MIMICK work. |
| F23 | https://arxiv.org/abs/1508.07909v5 | A; original character-based BPE NMT, not byte-based. |
| F24 | https://arxiv.org/abs/1804.10959v1 | **Incomplete extracted page**: navigation/footer only. Do not treat as abstract read; use F26 formal abstract. |
| F25 | https://arxiv.org/abs/1808.06226v1 | A; SentencePiece2018 original abstract. |
| F26 | https://aclanthology.org/P18-1007/ | A; formal Subword Regularization, resolves F24. |
| F27 | https://arxiv.org/abs/2406.19223v2 | A; fixed-version T-FREE metadata. |
| F28 | https://arxiv.org/html/1511.04586v1 | P title/abstract and §§2.5–2.6; corrected prior title misassociation; staged training and IBM4 auxiliary alignment are explicit. Whole response not claimed FULL. |

No academic data API was used; therefore no academic source Skill/API-doc call was applicable. Built-in browser complied with the browser-specific instruction; WebBridge was not invoked because the user did not request Chrome/Edge or logged-in sessions.

## Count reproducibility and limits

`WORKS.md` has15 W rows and13 local N rows. `PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md` has R01–R52 exactly once as table records, spanning all28 work IDs. Existing-source rows are not new discovery. Perceiver IO is distinct from W0107 Perceiver, but is already recovery-discovered. Byte distillation N11 is already recovery-discovered. New-to-old-corpus status is a scope claim about inspected catalog/recovery, not global novelty.

Potential later expansion: Fast Vocabulary Transfer, embedding reset/relearning, OFA follow-ups, cross-tokenizer distillation beyond byte students, and further denoising objectives. They remain leads, not invented mechanism records. The initial breadth expectation is met without counting them.

## Delivery verification

A read-only Python validation passed: exactly4 deliverable files,15 unique W rows+13 unique N rows,52 unique contiguous record IDs R01–R52, and every one of28 works represented. No validation artifacts were created. Final `git status --short` has the same top-level untracked entries as the initial status; the only intentionally authored paths are the four S07 Markdown files. No software tests/builds were applicable to this documentation-only discovery assignment. Two initial own-tab close attempts failed with TAB_NOT_ACTIVE; selecting each tab before closing succeeded. All three own tabs were closed; other tabs were left alone.
