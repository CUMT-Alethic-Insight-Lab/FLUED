# S04 — Sharing, geometry, and optimization: discovery log

Date: 2026-11-08. Role: sol discovery/inventory, not selected-paper full reader. Scope and delivery contract: [PLAN](../../PLAN.md). This is an independent account of researchers' interface-design problems, not validation of FLUED or of the earlier multigranularity proposal.

## Accounting and evidence rules

- **29 screened works**: 14 existing CATALOG works, 3 candidates already discovered in recovery audits but not in CATALOG, and **12 genuinely new discoveries relative to both those sources**. One of the 29 (S04-N14, Super Tiny Language Models) is screened as a proposal, not an empirical byte-tying result. Thus the inventory has 28 contributing works. Stable old W IDs are retained; local N IDs are not new global W IDs.
- **51 problem–solution–technique records**, including explicitly marked general background and abstract-only candidates; no numerical quota was used to invent missing evidence.
- **10 existing reading cards actually read**, all labeled FULL by their original readers, with their explicit scope limits preserved. **0 new FULL readings**. New source reading is abstract-only or PARTIAL/targeted, even where a fetch returned much more text.
- **16 WebSearch calls; 27 FetchURL calls (22 usable responses, 5 errors); one built-in-browser attempt blocked by a control race.** No academic data-source API was used; therefore no academic API skill or API-documentation lookup is claimed. Searches used public mechanism/model terms only, never internal documents.
- No downloads or conversion files were intentionally written. Fetch tools automatically paginated some long responses in their tool-result store; these were read only. All authored deliverables are in this assigned S04 directory.

## Reused corpus: actual inspection, not a catalog-only survey

The CATALOG was read at its beginning, then searched exactly for W0351–W0368, relevant byte and optimization terms, and every prospective new arXiv ID. The 543-work corpus count is not an S04 reading count. Inspected recovery audits: `07_scope_recovery/07_BYTE_SURVEY/{COVERAGE_AUDIT,READING_RECOMMENDATIONS}.md`, `05_LEARNING_DYNAMICS/COVERAGE_AUDIT.md`; exact-ID searches additionally located relevant entries in the learning-dynamics/global recovery logs and queues.

Paths below are relative to `docs/research/flued_multigranularity_survey_20261108/`.

| Existing card actually read | Evidence reused | Scope retained |
|---|---|---|
| `03_reading/B08/W0351.md` | ByT5 parameter allocation; encoder/decoder layer ratio; Large-only configuration check | Original TACL reading plus static code/config check; no all-sizes generalization |
| `03_reading/B14/W0366.md` | Output-path gradient predominance; mixed input-gradient intervention results | Subword/token experiments, single-run and model/data confounds |
| `03_reading/B05/W0010.md` | BLT local/global adaptation; separate entropy model to avoid competing objectives | ACL2025 version; selected appendix scope as stated in card |
| `03_reading/B05/W0011.md` | H-Net smoothing, straight-through estimator and ratio loss | v2; card labels FULL but explicitly does not read every appendix |
| `03_reading/B22/W0511.md` | MrT5 pretrained-interface adaptation and softmax1 | v3; bidirectional encoder, causal target decoder |
| `03_reading/B26/W0514.md` | Byte fusion vs parameter and inference costs | v3; word-span preprocessing and language exceptions |
| `03_reading/B14/W0356.md` | Byte curriculum; parameter/FLOP ranking reversal | v1; no code verification |
| `03_reading/B24/W0023.md` | Compressor-only auxiliary training and stop-gradient | v1; byte enwik8 and subword PG-19 results separated |
| `03_reading/B16/W0328.md` | Gradient surgery and restrictive guarantees | v4; preserve original audit concern about Appendix A.3 |
| `03_reading/B16/W0331.md` | Auxiliary-gradient gating and positive-direction counterexample | v2; not byte-model evidence |

Existing but previously unread works W0364/W0365/W0367/W0368 were newly checked online only within the targeted scopes below. Fetching them does not create fresh discoveries or FULL cards.

## Search queries and disposition

Platform for Q01–Q16: WebSearch (returned public search results). Source URLs were then checked with FetchURL rather than relying on snippets.

| Query | Exact query | Relevant provenance and decision |
|---|---|---|
| Q01 | `byte language models weight tying cosine output head embedding small vocabulary` | arXiv 2405.14159 and 2608.28151. STLM turned out to be a proposal; nested-vocabulary work is byte-level BPE, not pure byte generation. Both distinctions survive screening. Excluded tutorial/aggregator claims. |
| Q02 | `ByT5 tie_word_embeddings config google byt5 small large shared embedding softmax` | ByT5 paper and official-model leads. No valid configuration conclusion from snippets; targeted configuration fetches attempted, old Large-specific card retained. |
| Q03 | `weight tying small vocabulary character language models regularization Inan Press Wolf` | Press/Wolf primary source, AWD-LSTM lead. Prioritize original tying papers; do not count their word-vocabulary results as byte evidence. AWD-LSTM not added merely for breadth. |
| Q04 | `character aware neural language models Kim Jernite Sontag Rush 2016 highway output word embeddings` | Primary AAAI/arXiv 1508.06615. Retain as character-input/word-output antecedent, not byte-to-byte. |
| Q05 | `byte models encoder decoder adaptation pretrained language model cross tokenizer embeddings distillation` | arXiv 2604.07466 and 2602.01007, both new relative to old catalog/recovery. Distinct removable-head vs actual byte-model conversion mechanisms. |
| Q06 | `cosine softmax language model output embeddings normalization weight tying softmax bottleneck` | Softmax-bottleneck and recent LM-head leads. Retain original 1711.03953 via citation-following; do not treat generic classifier limitations as proof of a 256-class bottleneck. |
| Q07 | `byte language model "tied" "embedding" H-Net MambaByte EvaByte` | Mostly MambaByte papers or secondary pages; **no version-specific tying evidence established**. Do not infer from architecture names. |
| Q08 | `"cosine" "language modeling" "softmax" normalization embeddings head` | Primary arXiv 2001.07885v2; explicit normalization alternatives inspected. Its so-called cosine variant normalizes output rows only. |
| Q09 | `"byte" "weight tying" "EvaByte"` | No usable primary configuration evidence. Keep EvaByte tying unknown; no extra work counted. |
| Q10 | `"Variational Lossy Autoencoder" text character decoder collapse` | Found 1702.08139v2. Original VLAE is image work, so not retained as byte evidence; retain dilated-decoder **word-level** VAE as explicit background. |
| Q11 | `"nGPT" "normalized" output logits hypersphere 2024` | Primary arXiv 2410.01131v1. Retain normalization and logit-scale mechanism as background, not a byte ablation. |
| Q12 | `"byte" "tied embeddings" language model` | Primary 2605.29459. Kronecker input representation is compatible with BPE; retain mixed-interface candidate, not pure-byte generation. |
| Q13 | `"Bolmo" byte model 2025 2026` | Primary 2512.15586v2 and official repository. Read version-specific adaptation/rank/ablation passages. |
| Q14 | `"SpaceByte" "weight" "tying"` | No usable primary tie configuration; unrelated OLMo hit excluded. No inference of SpaceByte tying status. |
| Q15 | `"MambaByte" "tied"` | Primary MambaByte and later Bolmo/Nature leads, but not a tie specification. No new work or all-byte-model claim from this query. |
| Q16 | `"ByT5" "tie_word_embeddings" "false"` | Generic issue/docs and a blog snippet. These are **not** evidence about an official checkpoint. No all-size ByT5 conclusion adopted. |

## Fetch ledger

`PARTIAL` means specified passages only, not method+all tables+appendices. Repeated abs/HTML fetches are one work. Exact date/version is only asserted when the fixed-version URL or returned history establishes it.

| Fetch | Source URL | Outcome / actual use |
|---|---|---|
| F01 | https://arxiv.org/html/1608.05859v3 | Usable; targeted §3 update rules/projection regularization and §4.2–4.3 findings; some table bodies absent in extraction. PARTIAL, no new FULL. |
| F02 | https://arxiv.org/html/1611.01462v3 | Usable; §3–4 loss and assumptions, §6.1–6.3 experiment design, Table 3 text, Appendix A/B inspected selectively. No independent proof audit; PARTIAL. |
| F03 | https://huggingface.co/google/byt5-small/raw/main/config.json | Network error; no configuration facts extracted. |
| F04 | https://huggingface.co/google/byt5-large/raw/main/config.json | Network error; no configuration facts extracted. |
| F05 | https://storage.googleapis.com/t5-data/pretrained_models/byt5/large/operative_config.gin | Extraction error; not a fresh successful verification. Earlier W0351 static check remains explicitly reused evidence. |
| F06 | https://arxiv.org/html/2405.14159v1 | Usable; §4–5 and conclusion establish proposal status, BPE-delimited pooling, no measured tying-only byte result. |
| F07 | https://arxiv.org/html/2604.07466v1 | Usable, long result paginated. Read §3.2, §4/Table 1–3, §5 and Appendix A description; method/counterexamples, not all appendices. PARTIAL. |
| F08 | https://arxiv.org/html/2602.01007v1 | Usable, paginated. Read §4.1–4.2, §5 setup and §6 descriptions; appendix budgets/table bodies not fully read. PARTIAL. |
| F09 | https://arxiv.org/html/2602.04556v2 | Usable, paginated. Read §4 equations (4)–(13), abstract and selected discussion/result caveats. PARTIAL; authors' extraction incomplete. |
| F10 | https://arxiv.org/html/2610.01395v1 | Network error; legitimate abs fallback F21 succeeded; not bypassing an access denial. |
| F11 | https://arxiv.org/html/2608.28151v1 | Usable; §II–III design, §IV–VI findings inspected; table bodies not returned. PARTIAL. |
| F12 | https://arxiv.org/html/2001.07885v2 | Usable; §2.2.1–2.2.4 equations and §3.1–3.2 text inspected. Table bodies absent; conditional/theoretical claims not independently certified. PARTIAL. |
| F13 | https://arxiv.org/html/2410.01131v1 | Usable; §2.1 and §2.6, §3.1 setup and runtime caveat inspected. Later text/appendices not read; PARTIAL. |
| F14 | https://arxiv.org/html/1702.08139v2 | Usable; §2.2–2.3 and §3.2–3.3 word-level decoder/context sweep inspected. PARTIAL, not all classification/clustering results. |
| F15 | https://arxiv.org/abs/1511.06349 | Usable; history v1–v4 and abstract; later method check F25. |
| F16 | https://arxiv.org/abs/1901.05534 | Usable; abstract and history v1/v2; prior recovery method inspection reused, not falsely newly performed. |
| F17 | https://arxiv.org/html/1711.03953v3 | Usable, paginated; abstract/introduction identifying matrix-factorization issue and mixture-of-softmaxes solution. Method proof/experiment/appendix incomplete. PARTIAL. |
| F18 | https://arxiv.org/html/2512.15586v2 | Usable, paginated; §3.2.1–3.2.2, §5.2, §6.2, Appendix E rank paragraph; §3.1/§6.1 snippets also inspected. Large experiment tables/causality appendix not fully read. PARTIAL. |
| F19 | https://arxiv.org/abs/1808.04444v2 | Usable; fixed-version history and abstract. Later targeted body F24. |
| F20 | https://arxiv.org/abs/1508.06615 | Usable; abstract/history, latest listed v4; no full-body mechanism audit. ABSTRACT. |
| F21 | https://arxiv.org/abs/2610.01395v1 | Usable; fixed version abstract/comments; author list not reliably extracted. ABSTRACT only. |
| F22 | https://arxiv.org/abs/2605.29459v1 | Usable; abstract/history; claims are abstract-reported only. |
| F23 | https://huggingface.co/google/byt5-small/resolve/main/config.json | Second legitimate public route, network error. No more HF retries or mirror substitution. |
| F24 | https://arxiv.org/html/1808.04444v2 | Usable; Auxiliary Losses, Training, Evaluation and Ablation Experiments sections inspected. Discovered text8/enwik8 unit distinction explicitly in source. PARTIAL; full tables not available in extraction. |
| F25 | https://arxiv.org/html/1511.06349v4 | Usable, paginated; §3.1 and §4 inspected directly. All imputation/generation/appendices not read. PARTIAL. |
| F26 | https://arxiv.org/html/2609.12303v1 | Usable, paginated; §1.1, §2.1–2.2, §3.1–3.2 inspected. Scaling curves/table bodies/storage appendix incomplete. PARTIAL. |
| F27 | https://raw.githubusercontent.com/google-research/byt5/7d4efdddf7049a2aadfe65d032f264553508916e/README.md | Usable fixed-commit README. Confirms Large pretraining example inputs=1024/targets=189, XNLI example inputs=2048/targets=56, and model/config references; **does not itself prove tying settings**. |

Built-in browser: one `browser.create_tab` for the public ByT5-Small config page failed with `TAB_NOT_ACTIVE` (control changed). No user takeover was overridden; stopped browser attempts to avoid competing with other streams. Existing Large-specific evidence remains usable, but fresh all-size HF verification remains open.

## De-duplication and exclusions

Exact-ID search of CATALOG found no matches for N01–N15. Recovery search found N05=byte-audit N06, N08=learning-dynamics LD-N01/global N2, and N15=byte-audit N05: **these three are reuse, not new discovery**. Other N IDs had no matching stable ID/title in the inspected old catalog/recovery scope. Coordinator should still de-duplicate against concurrent S streams.

Excluded from substantive evidence: generic tying tutorials; model-name-only tying claims; interpreting BPE's name as pure-byte units; image VLAE as language data; STLM abstract's 90–95% reduction as completed experimental evidence; Nature/version claims about Bolmo that were search leads but not fetched/compared; all claims that every byte model is untied. No source gap was filled from memory as if read.

## Verification performed

Deliverable validation uses a read-only Python check of file presence, record IDs/counts, work references, local Markdown links and English text, followed by Git status. No build/test/training is relevant to a literature-only Markdown deliverable; none run. Existing untracked corpora, bundle files and other streams are untouched. Final validation result is recorded in READING_HANDOFF.
