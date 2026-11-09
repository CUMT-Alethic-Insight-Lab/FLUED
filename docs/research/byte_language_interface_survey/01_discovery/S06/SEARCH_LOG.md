# S06 search and reuse log — compute, scaling, and systems

2026-11-08. Discovery/inventory author: sol. This is an independent language-interface survey fragment, not a proposal validation or a new full-reading batch. Only files under this S06 directory were intentionally written.

## Accounting

- **29 independent works** in `WORKS.md`; **48 problem–solution–technique records** in the inventory.
- **22 works reuse old global W IDs**. Fifteen actual old FULL cards were opened and read, not merely counted from the catalog. Seven cataloged works lack those cards and remain abstract/partial here.
- **7 works lack a global W ID**: four were already discovered by recovery audits (N01–N04 below), and three are new to both the old catalog and searched recovery audits (N05–N07). Thus **3 genuinely fresh discoveries**, not seven. All N IDs are S06-local; assign canonical IDs centrally.
- New original-paper FULL readings: **0**. Current evidence distribution: **15 reused FULL cards, 6 targeted PARTIAL paper readings, 8 abstract-only verifications**. A successful fetch or a long HTML response is not a completed reading.
- **4 actual Bing searches** through Kimi Code Desktop's built-in browser; **23 FetchURL calls**, all returned text, including two excluded works and one mistaken identifier. Two additional attempted browser searches were rejected before navigation by `TAB_NOT_ACTIVE`; they are not successful searches. No academic API was used, so no academic-source skill/API invocation is claimed.

## Local corpus actually inspected

Read `PLAN.md` in the new survey. Read the old `02_catalog/CATALOG.md` opening and relevant exact search hits, rather than all 543 entities. Read recovery `07_BYTE_SURVEY/COVERAGE_AUDIT.md` and `READING_RECOMMENDATIONS.md` completely; read `04_DEPLOYED_USE/COVERAGE_AUDIT.md` to avoid turning general memory diagnostics into byte-interface systems evidence. Read `03_ADDRESS_READOUT/SEARCH_LOG.md` lines 62–73 to verify that Perceiver IO is earlier recovery discovery, not fresh.

Actual old cards read in full (paths relative to `docs/research/flued_multigranularity_survey_20261108/`):

- `03_reading/B05/{W0007,W0009,W0010,W0011,W0357}.md`
- `03_reading/B08/{W0351,W0360}.md`
- `03_reading/B14/{W0014,W0352,W0356,W0361}.md`
- `03_reading/B22/{W0511,W0518}.md`
- `03_reading/B24/W0023.md`
- `03_reading/B26/W0514.md`

These are 15 card readings, not 15 fresh original-paper readings. Their scoped FULL designation is retained exactly; original-code execution and reproduction remain absent.

Deduplication: exact IDs `1904.10509|1901.02860|1704.01444|2107.14795|1808.04444|2605.09630|2609.12303` yielded no work rows in CATALOG. Broader old-corpus search found Perceiver IO explicitly distinguished from W0107 and discovered in address/readout recovery; deep self-attention, Scratchpad Patching, and Breaking the Token Ceiling appear in byte-survey recovery. Recovery search for the three historical fresh IDs/titles found no discovery entry. Incidental references to Transformer-XL in other cards do not constitute an existing catalog entity.

## Exact online queries and provenance

All searches used the configured Bing engine, background tabs, public mechanism terms only. Search-result text was inspected with document snapshots; no internal document was uploaded.

| Query ID | Exact query | Observed relevant results and disposition |
|---|---|---|
| Q01 | `byte level language models compute scaling inference latency tokenization compute optimal tokenization` | arXiv 2605.01188; Byte Language Models; Meta BLT; Nature byteification. Fetched the compute-optimal primary work. Nature item is an unverified adjacent lead, not a counted work; adaptation is primarily S07. Blogs/videos excluded as evidence. |
| Q02 | `"Perceiver IO" "bytes" "language"` | arXiv and OpenReview Perceiver IO; DeepMind official repository; Hugging Face docs. Verified original HTML 2107.14795v3, not the original Perceiver W0107. Third-party GLUE score snippets were not used as primary evidence. |
| Q03 | `"byte" "language" "2026" "inference" "compute" tokenizer distillation scratchpad` | NeurIPS Scratchpad Patching; Nature byteification; generic inference surveys/blogs. Primary Scratchpad v1 inspected. Generic serving results excluded because they do not isolate a byte interface. NeurIPS listing alone is not a version equivalence check. |
| Q04 | `"Sparse Transformer" "Enwik8" "Time/Iter"` | Targeted historical timing-table search; primary arXiv 1904.10509v1 had already been fetched and its Table 2 / §7.2 inspected. Search text outcome recorded after snapshot; it does not upgrade paper depth. |

Two failed navigation attempts used `byte language modeling enwik8 S4 Perceiver IO Sparse Transformers deep self attention historical`; control had changed in a shared browser. One activation and one retry also lost control. Rather than repeatedly competing for a shared active tab, subsequent searches used atomic create-with-query and background reads. No denied access or authentication was bypassed.

## Fetch ledger and actual reading bounds

A = abstract/identity/history only. P = selected original-paper text, **not FULL**. Excluded = not in 29-work count. Source sections below are what were inspected, not a promise that other sections were read.

| Fetch ID | URL actually fetched | Outcome / use |
|---|---|---|
| F01 | https://arxiv.org/abs/2605.01188v2 | A; history v2 2026-05-26. |
| F02 | https://arxiv.org/abs/2305.07185v2 | A; MEGABYTE v2 2023-05-19; million-byte capability not equivalent to million-byte language evaluation. |
| F03 | https://arxiv.org/abs/2108.01073 | **Excluded mistaken ID:** resolves to SDEdit, not Perceiver IO. No claims imported; correct Perceiver ID obtained from existing recovery and Q02. |
| F04 | https://arxiv.org/abs/1808.04444v2 | A; deep self-attention identity/history v2 2018-12-10. |
| F05 | https://arxiv.org/abs/2605.09630v1 | A; Scratchpad v1 2026-05-10. |
| F06 | https://arxiv.org/abs/2609.12303v1 | A; byte distillation v1 2026-09-11; asymptotic forecasts explicitly distinguished from observed results. |
| F07 | https://arxiv.org/abs/2103.06874v4 | A; CANINE v4 2022-05-18. |
| F08 | https://arxiv.org/abs/2106.12672v3 | A; Charformer v3 2022-02-23. |
| F09 | https://aclanthology.org/2025.acl-long.1546/ | A; Beyond Text Compression, ACL 2025 pp.32155–32173, DOI 10.18653/v1/2025.acl-long.1546. |
| F10 | https://arxiv.org/abs/2212.07284 | A; MANTa history shows v1 only, 2022-12-14. |
| F11 | https://arxiv.org/abs/1904.10509 | A; Sparse Transformers history v1 2019-04-23. |
| F12 | https://arxiv.org/abs/2111.00396 | A; S4 latest history v3 2022-08-05; excluded from counted byte evidence after F13. |
| F13 | https://arxiv.org/html/2111.00396v3 | P, excluded: §4.3/Fig.8 ties advertised 60× language generation to **WikiText-103 tokens**, not byte LM. LRA Text is not autoregressive byte LM. Use MambaByte as direct SSM-byte evidence instead; no transfer of S4's 60× number. |
| F14 | https://arxiv.org/html/2107.14795v3 | P: §4.1, read/process/write overview; exact local pagination of the language section; selected appendix-F architecture hits, not all appendix tables. 2048 UTF-8 bytes vs 512 SentencePiece; 256 latents; 15% whitespace-word masking. |
| F15 | https://arxiv.org/html/2605.01188v2 | P: §2.1–2.2, §3.1–3.2 parameter-definition passage, selected §3.5 result and §7.2 limitations; appendix header/hits only. Full fitting/uncertainty/compute appendix remains missing. |
| F16 | https://arxiv.org/html/2605.09630v1 | P: §§2–3.2, §4.1 setup and result narrative, §5.1–5.3, limitations; selected appendix-A/C.2 hits. Trunk-cache mask read precisely; table cells/appendix evidence not fully audited. |
| F17 | https://arxiv.org/abs/1901.02860 | A; Transformer-XL v3 history 2019-06-02. |
| F18 | https://arxiv.org/abs/1704.01444 | A; review mLSTM v2 history 2017-04-06. |
| F19 | https://arxiv.org/html/1904.10509v1 | P: §§3–5.6, Table 1–2 and §7.2 text experiment; nontext experiment conclusions not used as byte-language results. No full appendix/code audit. |
| F20 | https://arxiv.org/abs/2608.15454v2 | A; multi-byte prediction v2 2026-08-21; mask/throughput claims remain unverified below abstract. |
| F21 | https://arxiv.org/html/1704.01444v2 | P: §§2–3, §4 opening and §4.3 capacity-ceiling discussion; not all downstream tables/appendices. 38B bytes, one month/4 Titan X, persistent state across truncated-gradient batches. |
| F22 | https://arxiv.org/html/1808.04444v2 | P: model/auxiliary-loss sections, dataset/training/evaluation prose, results and word-comparison prose. Crucial tables absent from extracted rendering; no full figure/table verification. enwik8=bytes, text8=27-symbol characters. |
| F23 | https://aclanthology.org/P19-1285/ | A; official Transformer-XL title/authors, ACL2019 pp.2978–2988, DOI 10.18653/v1/P19-1285. No formal/preprint content diff. |

Tool-created large-response captures were read with targeted Read/Grep pagination; they are tool-managed captures, not downloaded deliverables. No manually created intermediate files, installations, training, production edits, or commits.

## Deliberate exclusions and stopping rule

- Do not turn FlashAttention, generic KV offload, or general efficient-memory papers into byte-interface findings without a byte experiment. Sparse Transformers is included because original enwik8 timings and mechanisms are directly inspected; Transformer-XL is bounded to its enwik8/text8 evidence.
- Do not substitute S4's word/token generation speed for MambaByte's measured byte experiment.
- Existing recovery discoveries count as reuse even though they were not yet in CATALOG. Newness means corpus newness, not scholarly novelty or independent replication.
- Stop discovery here and hand off the 8 genuinely missing high-value full reads. Remaining work is evidence completion, not accumulating model names.
