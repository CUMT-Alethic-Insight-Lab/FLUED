# S02 — Search and source-verification log

Work performed 2026-11-08–09. Scope: learned grouping/compression, local structure, causal boundary conditions, and reconstruction versus prediction signals. Public mechanism terms and public titles only; no internal documents sent to external services. This is targeted discovery, not a reproducible exhaustive systematic review.

## 1. Recovered local evidence before searching

Read the current survey `PLAN.md`. Read old CATALOG opening rows and targeted title/identifier matches across the complete catalogue; did not manually reread all543 entries. Read actual cards, not just a synthesis overview:

- `03_reading/B05/W0007.md`, `W0009.md`, `W0010.md`, `W0011.md`, `W0357.md`.
- `03_reading/B14/W0014.md`, `W0358.md`.
- `03_reading/B24/W0012.md`, `W0013.md`, `W0023.md`, `W0024.md`.
- `03_reading/B22/W0511.md` and `03_reading/B26/W0514.md`.

All paths above are under `docs/research/flued_multigranularity_survey_20261108/`. **13 actual cards read; 12 used as inventory works.** W0014 is contextual cross-stream reading only. No original card altered or reading level upgraded.

Read old recovery `07_scope_recovery/07_BYTE_SURVEY/{COVERAGE_AUDIT,READING_RECOMMENDATIONS,SEARCH_LOG}.md` and `01_COMPRESSION/COVERAGE_AUDIT.md`. These identify prior missing classic reads, causal-lag alternatives and objective contrasts. Old recovery already discovered Scratchpad Patching and AU-Net; they are reused discovery rather than fresh findings.

Initial instructions were later restated after an interruption/failure notice. Checking the assigned directory found **no previously landed S02 files**; the completed searches in this session were retained and not restarted. All four final files were then written only inside the assigned directory.

## 2. Actual successful online queries

**9 successful queries: 4 built-in-browser Bing searches, 5 WebSearch calls.** Results were inspected, and selected source identities/content verified with FetchURL. Browser searches remained background research; the user did not request search results to be displayed.

| Query | Platform | Exact query | Actual outcome / selection |
|---|---|---|---|
| Q01 | Built-in browser / Bing | `neural character language model learned segmentation segmental language models Kawakami 2019 Sun Deng 2018` | Primary arXiv/ACL results for SNLM and SLM; both already in CATALOG. ResearchGate/automated summaries not used as evidence. |
| Q02 | Built-in browser / Bing | `"Hourglass" "Fully Character-Level" "Lee" transformer pooling` | Overconstrained: mostly unrelated tutorial videos, no useful primary hit. Used known public IDs from historical mechanism knowledge and verified original sources; not counted as search-discovered evidence. |
| Q03 | Built-in browser / Bing | `"A vocabulary-free multilingual neural tokenizer"` | arXiv2204.10815, ACL and Amazon primary-author routes; selected original arXiv abstract. Search time label “22 hours” ignored in favor of v1history2022-04-22. |
| Q04 | Built-in browser / Bing | `"learned tokenization" "boundary" "2026" byte pooling entropy` | Found Dauncey/Wattenhofer RL tokenization; excluded personal blogs, topic summaries and DNA-specific tokenization from language evidence. |
| Q05 | WebSearch | `"You Can Learn Tokenization End-to-End with Reinforcement Learning"` | Confirmed original2602.13940, authors and alternate ETH/OpenReview venues. Conference snippets disagree, so publication-track claims not used; versioned arXiv is the evidence identity. |
| Q06 | WebSearch | `"Hierarchical Transformers Are More Efficient Language Models" "2110.13711"` | Confirmed title/identifier and author references; not used to infer result tables. Primary abs/HTML had already been fetched. |
| Q07 | WebSearch | `"Charformer" GBST causal convolution downsampling` | Found direct causal counterexample2205.14086 and later Subword-Delimited Downsampling. Original methods selected; generated review sites excluded. |
| Q08 | WebSearch | `"2205.14086" title` | Established exact title **Patching Leaks in the Charformer for Efficient Character-Level Generation**; later paper references it separately. |
| Q09 | WebSearch | `"Subword-Delimited Downsampling" "arxiv"` | Established separate2212.01304 identity and formal EMNLP2022 route. Other results such as2609.00463 remained unassessed leads, not counted as read/discovered inventory works. |

### Failed browser control requests, not completed searches

Two attempted `tab.search` calls returned `TAB_NOT_ACTIVE` because other parallel work changed control: (a) `character neural machine translation convolution pooling Lee Cho Hofmann 2017 fully character level translation dynamic pooling Hourglass shortening transformer 2021`; (b) `"differentiable" "tokenizer" "frontier" "Islam" 2022`. These queries were **not successfully executed** and are excluded from the9-query count. Activated the owned tab for Q02; later Q03/Q04 used separately owned background tabs. No user takeover or permission denial was bypassed.

Browser tabs created by this worker: `panel-tab-1375`, `panel-tab-1475`, `panel-tab-1481`. Existing70+ shared tabs were not closed or navigated; more than ten tabs make the sidebar crowded. Cleanup applies only to these owned tabs and is recorded below.

## 3. Forty FetchURL attempts and what was actually inspected

**40 attempts; 4 explicit failures; 2 nominally successful but unusable footer/tool extractions; 34 useful source responses.** A useful fetch is not a full read. Long generated tool outputs were paged only for specified methods/selected snippets; remaining sections are still unread. No deliberate download/conversion/intermediate files were created, and no software installed.

| Fetch | Exact URL | Outcome and actual evidence scope |
|---|---|---|
| F01 | https://aclanthology.org/P19-1645/ | SNLM formal abstract/authors/pages. |
| F02 | https://aclanthology.org/D18-1531/ | Chinese SLM formal abstract; no method claims from this page alone. |
| F03 | https://arxiv.org/abs/1609.01704v7 | HM-RNN abstract/version history. |
| F04 | https://arxiv.org/abs/2103.06874v4 | CANINE abstract/history; kept separate from n-gram-enhanced HTML headline. |
| F05 | https://arxiv.org/abs/2106.12672v3 | Charformer v3abstract/history; method later inspected in v2 only. |
| F06 | https://arxiv.org/abs/2212.07284 | MANTa abstract; sole v1history. |
| F07 | https://arxiv.org/abs/2305.07185v2 | MEGABYTE abstract/history. |
| F08 | https://arxiv.org/abs/2110.13711 | Hourglass abstract and v1/v2history. |
| F09 | https://arxiv.org/abs/1610.03017 | Fully character-level NMT abstract and v1–v3history. |
| F10 | https://arxiv.org/abs/2610.22100v1 | Novelty paper abstract/history; mechanisms primarily reuse actual old FULL card. |
| F11 | https://arxiv.org/abs/2605.09630v1 | Scratchpad abstract/history; no new full read. |
| F12 | https://arxiv.org/abs/2506.14761v1 | AU-Net abstract/history; no new full read. |
| F13 | https://arxiv.org/html/2212.07284v1 | MANTa primary §§3.1–3.2,5,6.1–6.4/Limitations; unextracted table cells and appendices not certified. |
| F14 | https://arxiv.org/html/2106.12672v3 | **Network failure** after long timeout; no usable primary v3method. |
| F15 | https://arxiv.org/html/2110.13711v2 | Hourglass long output; explicitly read §§2.1–2.3/algorithm1 and §3.1opening, not remaining results/appendix. |
| F16 | https://arxiv.org/html/1609.01704v7 | HM-RNN §§1–3.3,4.1 character experiments/tables1–2/boundary discussion; handwriting remainder not used. |
| F17 | https://arxiv.org/html/1610.03017v3 | CharacterNMT §§3.3–5.5 and selected cost/preprocessing/analysis text. Tables mostly extraction captions; not numerically reconstructed. |
| F18 | https://arxiv.org/html/1811.09353v2 | **Network failure**; SNLM remains abstract-only here. |
| F19 | https://aclanthology.org/2022.sigmorphon-1.5/ | MSLM formal abstract/authors/pages; bidirectional context explicit. |
| F20 | https://arxiv.org/abs/2006.03236v1 | Funnel abstract/history only. |
| F21 | https://aclanthology.org/W99-0701/ | **Footer only**; no evidence about MDL mechanism from this fetch. |
| F22 | https://arxiv.org/abs/2204.10815 | Neural tokenizer primary abstract/history. |
| F23 | https://arxiv.org/html/2204.10815v1 | **404**; no primary method read. |
| F24 | https://scholars.cityu.edu.hk/en/publications/unsupervised-learning-of-word-boundary-with-description-length-ga/ | Author-institution description-length-gain abstract and1999bibliography; legitimate alternative to F21. |
| F25 | https://arxiv.org/abs/1508.07909v5 | BPE-NMT original abstract/history; character-based subword context, not modern byteBPE. |
| F26 | https://arxiv.org/abs/1804.10959v1 | **Bibliographic tools/footer only**; replaced with formal abstract F28. |
| F27 | https://arxiv.org/html/2305.07185v2 | Long MEGABYTE output; method §2.1–2.2, figures/equations text and introduction only. Other tables/appendices not read. |
| F28 | https://aclanthology.org/P18-1007/ | Subword regularization formal abstract; no full optimization read. |
| F29 | https://arxiv.org/abs/1402.3511v1 | ClockworkRNN abstract/history. Audio/TIMIT tasks, intentionally **not counted as text-model work**. |
| F30 | https://arxiv.org/html/2103.06874v4 | Long CANINE output; paged §3.1–3.2 and table1; full experiments/appendices unread. |
| F31 | https://arxiv.org/html/1810.03167v1 | SLM §§2–3/equations4–9/tables1–2/preprocessing; no FULL claim. |
| F32 | https://arxiv.org/abs/2602.13940v1 | RL abstract/history, versions1–4. v1date2026-02-15; v4date2026-09-14. |
| F33 | https://arxiv.org/html/2602.13940v1 | **Network failure**; later v4legitimate primary version used instead. |
| F34 | https://aclanthology.org/2022.findings-emnlp.69/ | Subword-Delimited Downsampling formal title/abstract. |
| F35 | https://arxiv.org/abs/2205.14086 | Patching Leaks abstract/history; byte units not known until AppendixB.2 in F38. |
| F36 | https://arxiv.org/html/2106.12672v2 | Charformer v2long output; explicitly paged §2.1–2.2 and §3.1setup. v2/v3difference unknown. |
| F37 | https://aclanthology.org/2022.findings-emnlp.69.bib | Formal authors/title/DOI/pages981–992. |
| F38 | https://arxiv.org/html/2205.14086v1 | Patching Leaks §§2–4,AppendixB.2–B.3 and leakage-diagnostic text; tables mostly missing numeric cells. |
| F39 | https://arxiv.org/html/2602.13940v4 | Long RL output; paged §§2.1–2.4, then targeted search snippets §§2.5–2.7/4/AppendixD including cost/rate/BPE shift; **not complete method/experiments/appendix**. |
| F40 | https://arxiv.org/abs/2212.01304v1 | Confirms distinct Subword-Delimited Downsampling title/abstract and2022-12-02v1history. |

Failures were not hidden by relabelling a different version as the failed one. F36 explicitly supplies v2method while F05 supplies v3identity. F39 explicitly supplies v4method after v1HTML failure. No repeated failed request was used to bypass permissions or authentication.

## 4. Deduplication and true new counts

Searched complete old CATALOG for exact arXiv IDs and distinctive titles/aliases, then checked relevant recovery text. The old catalogue and recovery discoveries are different sets.

| Local key | Source identity | Old CATALOG | Inspected old recovery | Count decision |
|---|---|---|---|---|
| S02-N01 |1610.03017v3 / Fully Character-Level NMT | No corresponding entity found | No discovery entry found | Fresh1 |
| S02-N02 |2110.13711v2 / Hourglass | No corresponding entity found | No discovery entry found | Fresh2 |
| S02-N03 |2204.10815v1 / Vocabulary-Free Neural Tokenizer | No corresponding entity found | No discovery entry found | Fresh3 |
| S02-N04 |2602.13940v4 / RL Tokenization | No corresponding entity found | No discovery entry found | Fresh4 |
| S02-N05 |2205.14086v1 / Patching Leaks | No corresponding entity found | No discovery entry found | Fresh5 |
| S02-N06 |2212.01304v1 / Subword-Delimited Downsampling | No corresponding entity found | No discovery entry found | Fresh6 |
| S02-R01 |2605.09630v1 / Scratchpad Patching | Absent | Already07_BYTE_SURVEY/N01 | Reused discovery1 |
| S02-R02 |2506.14761v1 / AU-Net | Absent | Already07_BYTE_SURVEY/N03 | Reused discovery2 |

The other24 works retain old W IDs. Thus **32works, 8catalogue-absent candidates, 6fresh discoveries, 56records, 0fresh FULL**. Mentioned but unassessed candidates, mere references in Related Work, alternative versions and Clockwork’s nontext experiments do not increase these counts.

## 5. Methodological decisions and stopping point

- No specialist academic data API was needed: direct public primary sites, WebSearch and FetchURL sufficed. Consequently no data-source skill or API call was made, and no removed skill name was invoked.
- Historical character methods were recovered before weighting recent byte systems. Neural latent segmentation, fixed grouping, task gradients, teacher labels, reconstruction, deletion, local fusion and vision merging are distinct mechanisms, not aliases counted as separate innovations.
- Search result dates were not publication evidence. Titles/IDs/versions were fixed on arXiv or formal bibliography; conference snippets were not promoted to verified venue claims.
- Reading depth is deliberately limited: 10prioritized missing FULL reads in READING_HANDOFF, 12reused adequate cards, and explicit source gaps. Full-page fetches and selected snippets do not become FULL.
- No training/build/pytest is relevant to this literature deliverable. Verification checks exact work/record counts, references/paths and four-file ownership instead. No generated test logs or deliberate temporary files need cleanup.

### Final artifact validation

Python read-only validation passed: exactly the four requested Markdown files; valid UTF-8; 32 unique work entries (24 W-ID, 6 fresh, 2 recovery); contiguous unique S02-001–S02-056 records; 40 logged fetch attempts; 9 successful queries; 10 selected-reading priorities; all explicitly referenced old card paths exist. Exact-ID search reconfirmed that all eight catalogue-absent candidates are absent from the old CATALOG. `git status --short -- docs/research/byte_language_interface_survey/01_discovery/S02` shows only the new untracked assigned directory. No test/build outputs or deliberate temporary files were created. These checks do not certify scientific claims or upgrade reading depth.

Cleanup attempt: closing each of the three owned browser tabs returned `TAB_NOT_ACTIVE` after parallel agents changed control. They may remain open (`panel-tab-1375`, `panel-tab-1475`, `panel-tab-1481`); no other tabs were touched. This non-content limitation does not affect the files or counts.
