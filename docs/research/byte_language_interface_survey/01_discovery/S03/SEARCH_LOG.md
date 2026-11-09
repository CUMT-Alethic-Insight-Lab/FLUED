# S03 actual discovery and reuse log

2026-11-08 · sol · Scope: causal output/generation, dependent or independent multi-byte output, training-generation matching, original-text likelihood, prefix conditioning and UTF-8 streaming. English working inventory, no proposal validation. Only public mechanism queries were sent; no internal documents uploaded. No subagents, training, installs, code edits or commits.

## 1. Actual local inspection

- Read survey PLAN.md completely and checked for nested AGENTS.md under docs/research (none returned).
- CATALOG.md first 154 lines, then targeted complete-file searches for relevant title/ID aliases; did **not** claim all 543 entries manually read. Full-file search, rather than visible excerpt alone, determines no-match status.
- Read all three actual `07_scope_recovery/07_BYTE_SURVEY/{COVERAGE_AUDIT,READING_RECOMMENDATIONS,SEARCH_LOG}.md`, including local N01–N09 discovery provenance.
- Read full actual old cards: B05/W0007,W0009,W0010,W0011; B14/W0014,W0352,W0356; B08/W0351; B22/W0509,W0518. **10 old FULL cards reused, 0 new FULL readings.** These are complete card reads, not freshly completed paper reads.
- Read `07_scope_recovery/04_DEPLOYED_USE/COVERAGE_AUDIT.md` for evaluation scope boundaries. It is adjacent memory-methodology evidence, not a substitute original byte-generation source and not counted among 30 works.

## 2. Real online searches

Built-in Kimi Desktop browser/Bing used for public web search; only owned tabs 1376 and 1476 used. Shared browser control changed between calls: two tab.search calls returned TAB_NOT_ACTIVE; after activation, one query had already committed despite the error. Queries are counted by loaded result pages actually inspected, not raw failed calls. No login/verification challenge bypassed. Browser warnings showed >10 tabs crowding sidebar; only our two tabs are eligible for closing.

| Query | Exact submitted text | Actual result provenance, decision and exclusion |
|---|---|---|
| Q01 | `byte language model causal patch decoder scratchpad patching multi byte prediction joint likelihood 2026` | Bing original arXiv 2605.09630/NeurIPS listing; confirmed recovery Scratchpad rather than new discovery. AI summary mixed unsupported causal prose; ignored summary/aggregators and fetched original v1. |
| Q02 | `"language models" "prefix" "token" "probability" "byte" exact 2024 2025` | Bing original sources for Exact Byte, cross-tokenizer likelihood and distillation. Pursued Exact Byte as directly missing prefix-law mechanism; generic teaching pages/videos and broad tokenization overview excluded. Distillation belongs mainly to interface-transfer stream, not a new bulk queue here. |
| Q03 | `"Exact byte-level probabilities" tokenized language models` | Bing original arXiv 2410.09303 and GitHub/ICLR lineage. Read result metadata then abs/v2 HTML. Search GitHub date was nonsensical (2014), not used; arXiv history fixes 2024-10-11/2025-04-11. |
| Q04 | `"character" "generation" "blockwise parallel decoding" "multi-token prediction" language model` | Bing mostly visual-character/3D generation false positives. One structured-CFG-generation lead not pursued: not necessary for causal byte-output core. Narrowed query rather than count irrelevant hits. |
| Q05 | `"Blockwise Parallel Decoding" Stern 2018 "Speculative"` | Bing yielded secondary historical summaries and original-arXiv related work. Primary 1811.03115v1 independently fetched/read selected sections; no reliance on search summary's erroneous conflation of greedy and sampling distribution. |
| Q06 · arXiv API | `byte prediction speculative decoding` | Skill loaded, arxiv API docs fetched first, then search_papers with date_from=2018-01-01,date_to=2026-11-08,max_results=12. Eight results returned, mainly hardware false positives. Relevant Fast BLT/MtPC are reuse, not fresh works. Exact result was temporarily saved under assigned absolute directory; relevant metadata incorporated below, raw CSV removed before handoff. |

Academic-source sequence: `Skill(kimi-datasource:kimi-datasource)` → `get_data_source_desc(arxiv)` → `call_data_source_tool(search_papers, ...)`; not an undocumented API call. API discovery exposed MtPC author Lorenzo Loconte missing from extracted HTML header; do not certify full author list until PDF check. Hardware-memory “bytes” (MoE, rANS accelerator, CPU branches) and tool-call sidecar results excluded from language-byte model count.

## 3. Original source verification: 25 FetchURL calls

24 returned usable primary text/metadata, 1 returned a verification wall. None count as new FULL reads. Two repeated same-source fragment/body fetches are duplicate access, not distinct works. Tool-generated long-output caches were read only in targeted ranges; no agent-created download/conversion intermediates outside assigned directory.

| Fetch | Actual URL | Actual reading/depth and decision |
|---|---|---|
| F01 | https://arxiv.org/html/2605.09630v1 | Long extracted text; targeted §3.1–3.2 read, selected §1/4/5 search hits; mask/commit semantics verified. Remaining experiment tables/appendices not fully read. P. |
| F02 | https://arxiv.org/html/2608.15454v2 | Long text; §2/3, §4.4 and §6.1–6.3 selected; cached KV note Appendix B. LCA threshold versus verified policy separated. P. |
| F03 | https://arxiv.org/html/2511.11346v2 | Long text; abstract, selected §2–4 and loss footnote/eq5. Circuit proofs and sampling algorithms not read. Composite likelihood explicit. P. |
| F04 | https://arxiv.org/html/2305.07185v2 | Long text; §2.1–2.4 and generation serial-path paragraph; selected PG19/striding claims. Full experiments/appendices unread. P. |
| F05 | https://hkunlp.github.io/blog/2025/evabyte/ | Full returned prose including training, MTP, speed caption and failure recipes; figures not visually read. Official introduction O; immutable revision unknown. |
| F06 | https://openreview.net/forum?id=6m8TxUKFUL | Verification wall. No content identity/claim used; guessed candidate locator excluded from works. No bypass or login attempt. |
| F07 | https://arxiv.org/abs/1811.03115 | Original abstract and v1 history; then F22 targeted text. |
| F08 | https://proceedings.mlr.press/v202/leviathan23a.html | Formal ICML abstract, author/title/page identity; algorithm/proof not read. A. |
| F09 | https://arxiv.org/abs/2302.01318 | Original abstract/v1 history; modified rejection scheme and Chinchilla setting only. A. |
| F10 | https://arxiv.org/abs/2404.19737 | Original abstract/v1 history; multi-offset objective/sample-efficiency only. A. |
| F11 | https://arxiv.org/abs/1308.0850 | Original abstract/history v1–v5; precise text alphabet not inspected. A. |
| F12 | https://arxiv.org/abs/1603.06147 | Original abstract/history v4; source subword/target character and four translation pairs. A. |
| F13 | https://arxiv.org/abs/2410.09303 | Original abstract/history v1/v2 fixes dates. A plus F14 P. |
| F14 | https://arxiv.org/html/2410.09303v2 | Long text; selected §3/4.1 hits and §4.2 read. Proof/experiments/consistent-tokenizer assumptions not fully read; keep exactness conditional. P. |
| F15 | https://aclanthology.org/2021.emnlp-main.161/ | Formal abstract; alternative-tokenization marginal study, not full estimator read. A. |
| F16 | https://arxiv.org/abs/2506.14761v1 | Original AU-Net abstract/history; no tensor/target permission inferred. A. |
| F17 | https://arxiv.org/abs/2110.13711 | Original Hourglass abstract and v2 history, plus F21 selected method. |
| F18 | https://arxiv.org/abs/2406.02657 | Original Block Transformer abstract/history v2; reported serving motivation/claim not accepted as controlled byte benchmark. A. |
| F19 | https://arxiv.org/abs/2401.10774 | Original Medusa abstract/v3 history; exact-versus-typical acceptance proof not read. A. |
| F20 | https://arxiv.org/abs/1808.04444v2 | Original abstract/v2 history; fixed-context/auxiliary-loss historical counterexample. A. |
| F21 | https://arxiv.org/html/2110.13711v2 | Long text; §2.2–2.3 actually read, future-shift and conditional independence argument. P, not full enwik8 ablations. |
| F22 | https://arxiv.org/html/1811.03115v1 | Returned body selected §2–6 and §7.1/7.3/7.4; precise subword MT, transformed p1 and distillation/timing caveats. P. |
| F23 | https://arxiv.org/html/2410.09303v2#S3 | Duplicate body fetch for §3 locator; no separate work/read; long latency but succeeded, no retry beyond this. |
| F24 | https://arxiv.org/abs/2503.09573 | Block Diffusion abstract/history v3; generic token units, likelihood objective/experiments remain uninspected. A. |
| F25 | https://www.rfc-editor.org/rfc/rfc3629.html | Original RFC text; §3/4 pp.4–6, §6/10 selected. Syntax/legality and scalar-vs-byte distinction; no learned method or model score. S. |

The unversioned abs fetches above are not silently current-version full reads: WORKS and handoff say which version history was observed and fix the requested PDF version for future full reading. Extracted math frequently duplicates rendered/TeX numerals (e.g. “1616” for 16); inventory does not copy doubled values. Extracted author headers can omit first/equal authors, so complete author lists are withheld when not independently checked.

## 4. De-duplication and counts

Full CATALOG search used stable IDs and aliases: `2410.09303|1811.03115|2211.17192|2302.01318|2404.19737|1308.0850|1603.06147|2110.13711|2406.02657|2401.10774|1808.04444|2605.09630|2511.11346|2506.14761|2109.02550|EvaByte`, followed by `2503.09573|Block Diffusion|Block Transformer|Hourglass|Graves|Deep Autoregressive|Speculative Decoding|multi-token prediction` and `3629|Yergeau|UTF-8, a transformation`. Name “Graves” matched unrelated W0248 ACT; LayerSkip/WaveFront matched existing different works, not these entities. No W ID invented for an absent candidate.

- **12 existing W entities:** W0007/8/9/10/11/14/15/0351/0352/0356/0509/0518.
- **6 recovery-reused entities:** Scratchpad, MtPC, AU-Net, Deep Character Self-Attention, marginal-tokenization likelihood, EvaByte official introduction. Absent CATALOG but not new to inspected corpus recovery.
- **12 additional entities:** Graves generation, character-decoder NMT, Hourglass, Stern blockwise, Leviathan speculation, Chen speculation, Gloeckle MTP, Block Transformer, Medusa, Exact Byte, Block Diffusion, RFC3629. Eleven academic, one standard. Their direct-source identity/depth is logged above; this does not mean no earlier bibliography ever mentioned them.
- Total **30 works/source entities; 51 substantive inventory records**; no separate entity for versions, two Fast BLT policies, four MtPC circuits, heads or aliases. No fresh FULLs.

## 5. Scope stop and unresolved evidence

Stopped broad search once distinct mechanisms and direct missing evidence were identified, rather than filling arbitrary quotas. Selected full reading belongs to terra: eight precise priorities in READING_HANDOFF.md. Main unresolved contracts: LCA head factorization/mask/target offsets and caching; MtPC exact sampler/target law and actual hardware; practical validity assumptions of Exact Byte vs general tokenization marginals; MEGABYTE strided-evaluation/online budget; first-complete-scalar/grapheme streaming measures. No public source here closes a universal serving comparison.

Final verification is structural: unique S03 record IDs/work references, all four requested Markdown files, assigned-directory-only authored files, no temporary CSV remaining. No build/tests/training needed for a research-only Markdown deliverable; source claims are not reproduction-certified.

### Completion checks

- Python structural assertions passed: exactly four Markdown deliverables; R01–R51 present in order, no duplicate IDs; 12 W + 18 local N entities = 30.
- Assigned-path `git status --short` reports only the new S03 directory. Temporary arXiv CSV deleted by its exact authorized path; no downloaded PDF/conversion files created by this agent.
- Both owned browser tabs (1376, 1476) closed successfully after activation; no shared/user tabs closed. A first close attempt returned TAB_NOT_ACTIVE, then activation/close succeeded.
