# S01 — Search, source verification and reuse log

2026-11-08 · sol discovery/inventory · public mechanism/title queries only. No internal text uploaded, no installation/training/commit, no production changes. Assigned write boundary: this S01 directory only.

## Outcome and counting rules

- **33 distinct included works, 51 inventory records.** 13 reuse existing W IDs; H13 reuses old recovery N06;19 works are newly discovered relative to the checked old catalog **and** recovery audit. Absence from this old corpus is not a novelty claim about the field.
- **0 newly FULL-read papers.** Nine old FULL cards were actually read;10 primary-source targeted PARTIAL readings;14 abstract/metadata-only entries. Fetch success is not full reading. Inspecting one paper's references never upgrades another paper's depth.
- **11 WebSearch calls:**9 returned results,2 transient429 failures. **1 Scholar query** returned10 results after Skill/API-doc protocol; the documentation request first returned429 and a later single retry succeeded. **35 FetchURL calls:** public sources returned content;33 were relevant identity/method checks,2 revealed wrong candidate identities and were excluded. No access/authentication denial was bypassed.
- Scholar output CSV was created at the explicitly assigned absolute path, actually read, incorporated into the log below, then removed as a task-created intermediary. No external `/tmp` or Downloads files were created by S01. One large FetchURL response was automatically stored by the tool in its managed session output directory, not a requested/downloaded project intermediate; it was paginated/read only for CANINE §3.1–3.2.3 and is not a durable citation.

## 1. Prior corpus inspected before discovery

1. [New survey PLAN](../../PLAN.md) fully read. No nested AGENTS.md was found under docs/research.
2. [Old CATALOG](../../../flued_multigranularity_survey_20261108/02_catalog/CATALOG.md): opening111lines plus targeted stable-ID/title searches; **not** a full semantic reread of543records. Relevant W0004/5/6/8/10,W0351/2/6/9/60,W0509/11/14 records inspected. New H candidates checked by explicit arXiv IDs and title aliases; no matching entity lines. Stable ICML PDF/title H01 also checked by title family.
3. Actual old FULL card bodies read, not merely headers: [W0351](../../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md), [W0360](../../../flued_multigranularity_survey_20261108/03_reading/B08/W0360.md), [W0514](../../../flued_multigranularity_survey_20261108/03_reading/B26/W0514.md), [W0509](../../../flued_multigranularity_survey_20261108/03_reading/B22/W0509.md), [W0511](../../../flued_multigranularity_survey_20261108/03_reading/B22/W0511.md), [W0359](../../../flued_multigranularity_survey_20261108/03_reading/B14/W0359.md), [W0356](../../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md), [W0010](../../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md), [W0352](../../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md).
4. [07_BYTE_SURVEY/COVERAGE_AUDIT](../../../flued_multigranularity_survey_20261108/07_scope_recovery/07_BYTE_SURVEY/COVERAGE_AUDIT.md), [READING_RECOMMENDATIONS](../../../flued_multigranularity_survey_20261108/07_scope_recovery/07_BYTE_SURVEY/READING_RECOMMENDATIONS.md), [SEARCH_LOG](../../../flued_multigranularity_survey_20261108/07_scope_recovery/07_BYTE_SURVEY/SEARCH_LOG.md) fully read. H13=oldN06 is **reuse** even though absent CATALOG.
5. [08_GLOBAL_SCOPE/COVERAGE_AUDIT](../../../flued_multigranularity_survey_20261108/07_scope_recovery/08_GLOBAL_SCOPE/COVERAGE_AUDIT.md) read for scope drift and historical missing-read diagnoses. Targeted searches in other recovery files found no H01/H04/H06/H07/H15/H17/H18/H19/H20 identity hits; not a semantic audit of every recovery file.

## 2. Actual WebSearch queries and provenance

| Query | Exact submitted text | Returned evidence / exclusion |
|---|---|---|
| Q01 | `character aware neural language models Kim Jernite Sontag Rush 2016 highway CNN characters word vocabulary` | AAAI primary PDF and related slides; selected arXiv identity/method checks, not lecture slides as evidence. H04. |
| Q02 | `early byte level neural language model Sutskever Martens Hinton 2011 generating text multiplicative recurrent neural networks bytes Graves 2013` | ICML official proceedings and Toronto author/teaching copies; verified official PDF H01. Search's character wording retained, not mislabeled bytes. Graves followed from primary historical chain. |
| Q03 | `"UTF-8" "neural" "2016" "byte" language models Gillick` | H06 Byte-to-Span, H10 early byte NMT, H14 byte subwords; speech and lecture results excluded from language evidence. |
| Q04 | `"tokenization" "embedding-free" "QRNN" "byte"` | **HTTP429 network failure**, no evidentiary result, no repeat of identical query. Subsequent narrower independent query Q09 addressed a different mechanism scope. |
| Q05 | `"Character-level" "Convolutional Networks" "Text Classification" alphabet 70 2015` | arXiv v3 and NeurIPS original. H03 primary methods checked. Secondary summaries not used. |
| Q06 | `"byte" "language models" "2025" "noise" tokenizer free input encoder` | **HTTP429 network failure**; no result treated as absence. Recent evidence instead includes verified H18 plus existing2026 cards, not a completeness claim. |
| Q07 | `"Fully Character-Level Neural Machine Translation" Lee Cho Hofmann` | H08 arXiv/author/ACL identities; source-CNN/max-pooling mechanism verified by primary abstract. |
| Q08 | `"A Character-Level Decoder" "Neural Machine Translation"` | H09 exact1603.06147v4 identified; four-pair mixed source/target interface. |
| Q09 | `"embedding-free" "byte" language model` | Local Byte Fusion citation, Shaham/Levy lead, MoCE H18; unrelated image embedding-free methods and unverified repository priority claims excluded. |
| Q10 | `Shaham Levy 2021 neural machine translation without embeddings bytes one hot` | H17 NAACL official page/PDF and2008.09396 alias; read primary mechanism and dropout counterexample. |
| Q11 | `"Bridging the Gap for Tokenizer-Free Language Models"` | H20 official arXiv/author identities; primary §2 confirms UTF-8 bytes even though abstract says character-based. |

No paid academic search, author-contact request or publication upload was attempted. Browser control was unnecessary for these public fetches; the instruction to use the built-in browser rather than a personal-session bridge remains respected. WebSearch and FetchURL provided the requested targeted public-source access.

## 3. Academic data-source protocol and result handling

- Invoked **kimi-datasource:kimi-datasource Skill**, explicitly for public academic discovery.
- `get_data_source_desc(name="scholar")`: first429; one later retry succeeded. Read current `scholar_search` API parameter contract before calling it. No fallback source was queried.
- Actual API: `scholar_search(query="byte character neural language models", start_year=2011, end_year=2026, num_results=10, hl="en", file_path="E:/projects/FLUED/FLUED/docs/research/byte_language_interface_survey/01_discovery/S01/scholar_history.csv")`.
- Ten returned titles: ByT5; *Hierarchical autoregressive transformers: Combining byte-and word-level processing for robust, adaptable language models*; *Sampling from your language model one byte at a time*; *Retrofitting language models to operate over bytes*; *Comparing neural- and N-gram-based language models for word segmentation*; *Neural machine translation with byte-level subwords*; SpaceByte; *Training multilingual pre-trained language model with byte-level subwords*; CharBERT; *Large Byte Model: Teaching Language Models About Compiled Code*.
- Selected H14 byte-subwords and H16 CharBERT for S01 primary verification; ByT5/SpaceByte are existing works. Hierarchical autoregressive/adaptation/sampling entries are adjacent-stream leads, not newly verified S01 included works. Nature retrofit URL and date were **not independently verified** and are not used for a claim or new count. Compiled-code bytes are excluded as language evidence. Scholar citation counts are not used as quality evidence.

## 4. Actual FetchURL ledger (35 calls)

The relevant reading range is stated; rows list actual URLs, not imagined reads. Metadata fields missing from extracted author lists were not reconstructed from arXiv submitter names. HTML often drops first authors and table values; numerical claims not visible in prose are left unknown.

| Fetch | Actual URL | Verification / actual use |
|---|---|---|
| F01 | https://arxiv.org/abs/1508.06615 | H04 abstract/history; v4 2015-12-01. |
| F02 | https://arxiv.org/abs/1512.00103 | H06 bytes→span abstract/history; v2 2016-04-02. |
| F03 | https://arxiv.org/abs/1308.0850 | H02 abstract/history through v5 2014-06-05; no text-method reading. |
| F04 | https://arxiv.org/html/1509.01626v3 | H03 targeted §2–5 incl. alphabet/OOV, Sogou preprocessing, non-evidence of misspelling robustness. Not FULL; tables incomplete. |
| F05 | https://icml.cc/2011/papers/524_icmlpaper.pdf | H01 targeted optimization, multiplicative method, alphabet, training/comparator sections; numerical result table incomplete. |
| F06 | https://arxiv.org/abs/1508.02096 | H05 composition abstract/history v2. |
| F07 | https://arxiv.org/abs/1610.10099 | H07 ByteNet character LM/MT abstract/history v2. |
| F08 | https://arxiv.org/abs/1603.01354 | **Excluded identity mismatch:** *End-to-end Sequence Labeling via Bi-directional LSTM-CNNs-CRF*; not the intended character-decoder paper. No S01 work/record credited. |
| F09 | https://arxiv.org/abs/1606.04586 | **Excluded identity mismatch:** semi-supervised convolutional classification paper, not a byte/character NMT source. No S01 credit. |
| F10 | https://aclanthology.org/W17-4123/ | H10 exact title, authors,2017workshop, pp.154–158, abstract. |
| F11 | https://arxiv.org/abs/1610.03017 | H08 character source/target, CNN pooling, v3. |
| F12 | https://arxiv.org/abs/1603.06147 | H09 exact corrected title and mixed subword-input/character-output abstract, v4. |
| F13 | https://arxiv.org/abs/1602.02410 | H11 large-LM abstract/history v2; no isolation of char-CNN contribution. |
| F14 | https://arxiv.org/abs/1704.01444 | H12 byte-recurrent identity/history v2. |
| F15 | https://arxiv.org/abs/1808.04444v2 | H13 dense fixed-context/auxiliary-loss abstract; recovery N06 **not fresh discovery**. |
| F16 | https://aclanthology.org/2021.naacl-main.17/ | H17 official abstract: one-hot byte interfaces and decoder-dropout finding. |
| F17 | https://arxiv.org/abs/1909.03341 | H14 byte-derived subword abstract/version history v2. |
| F18 | https://arxiv.org/abs/2010.10392 | H15 CharacterBERT identity/history v3. |
| F19 | https://aclanthology.org/2020.coling-main.4/ | H16 CharBERT identity, exact author list and hybrid noisy-LM abstract; distinct from H15. |
| F20 | https://arxiv.org/abs/2411.01474 | H18 MoCE abstract/history v2=2025-02-07. |
| F21 | https://arxiv.org/abs/2103.06874v4 | W0004 abstract/history; abstract says2.8F1. |
| F22 | https://arxiv.org/abs/2106.12672v3 | W0005 implementation explicitly **byte**; v3. |
| F23 | https://arxiv.org/abs/2212.07284 | W0006v1=2022-12-14; abstract only here. |
| F24 | https://arxiv.org/abs/2305.07185v2 | W0008 local/global patches; language evidence separated from audio/images. |
| F25 | https://arxiv.org/html/2010.10392v3 | H15 targeted §3/§4setup/§5.1/5.4/5.5: crucial fn6 **UTF-8 bytes**, top100KMLM and out-of-vocabulary-never-masked restriction. |
| F26 | https://aclanthology.org/2021.naacl-main.17.pdf | H17 targeted §2–6: fixed input/output maps,3scalars, filtering/batch setup, post-dropout ranking reversal; tables not fully read. |
| F27 | https://arxiv.org/html/1508.06615v4 | H04 targeted full Model subsections, setup/Table3, highway discussion and runtime paragraph; other tables missing, not FULL. |
| F28 | https://arxiv.org/html/1909.03341v2 | H14 encoding/decoding, contextualization, noisy alphabets and script-transfer prose; table cells incomplete. |
| F29 | https://arxiv.org/html/1512.00103v2 | H06 §1/§3–5/§6.3 and selected result prose; segment-level non-LM output contract. |
| F30 | https://arxiv.org/abs/1808.09943 | H19 deep character baseline and conditional-computation abstract;v1. |
| F31 | https://arxiv.org/abs/2401.13660v3 | W0352 abs version and COLM2024comment recheck; old FULL card remains evidence source. |
| F32 | https://arxiv.org/abs/1908.10322v1 | H20 exact identity/history. |
| F33 | https://arxiv.org/html/2103.06874v4 | W0004 saved long response; targeted §3.1–3.2.3 paginated actual read. HTML headline5.7 differs from abs2.8; no numerical headline propagated. Experiments/appendices not read. |
| F34 | https://arxiv.org/html/1908.10322v1 | H20 §2–4: confirmed rawUTF-8bytes,836M/40layers, lm1b preprocessing, conversion and context costs. Probes/tables not fully audited. |
| F35 | https://arxiv.org/html/1704.01444v2 | H12 §2–4 targeted: UTF-8 bytes, fixed state, compute, domain ceiling and clamping; figures/tables incomplete. |

## 5. Deduplication and source/version findings

- H01 is fixed ICML2011proceedings; no arXiv number invented. H02's first2013version and accessed latest v5(2014) are not separate papers.
- H03 v3 notes earlier *Text Understanding from Scratch*; treated as related version history, not counted twice. H04 preprint2015/AAAI2016 counted once. H08 preprint2016/TACL2017 counted once.
- H14 first2019/AAAI2020 counted once, with actual units **BBPE subwords**. H17 first2020/NAACL2021 counted once, official PDF selected over mixing changing arXiv prose.
- H15 title says characters, but inspected §3.1fn6 says UTF-8 bytes,263types; §§3.2/5.1.1 retain a temporary100Kword MLM classifier. This is a material unit/supervision correction, not a reason to relabel the model a raw-byte generator.
- H20 abstract says character-based, but inspected §2 specifies UTF-8 bytes and256output values. H07 ByteNet remains character-labeled because its concrete alphabets were not inspected.
- W0004 abstract/HTML numerical mismatch and W0509 old-card abs/PDF mismatch remain unresolved; preserve explicit fixed-source caveat, do not select favorable number. Charformer is byte-level despite title. CANINE is codepoint-level and uses **learned** hash embeddings.

## 6. Stop rule and honest gaps

Substantive S01 coverage now includes early recurrent/CNN/highway routes, byte-to-span labeling, word-local byte composition, mixed source/target interfaces, embedding-free byte translation, byte-derived subwords, adaptive local attention and dense/nonhierarchical counterexamples through2026. Additional generic search would be less valuable than selected primary full reads. This does not claim exhaustive classic history, grapheme-level coverage or2026currency. Next work is the10-paper handoff, preserving adequate old FULL cards rather than rereading all modern headline models.

## 7. Delivery validation

Final static validation is reported after file generation: counts/ID uniqueness, all four deliverables present, work→record links resolved, old-card relative links resolved, new IDs absent from old catalog, no replacement characters, whitespace check and git-status inspection. No training or repository tests are relevant to this literature-only deliverable. Existing untracked survey directories/bundles were left untouched. The temporary Scholar CSV was removed by exact assigned path after incorporation; final directory contains only the four requested Markdown files.
