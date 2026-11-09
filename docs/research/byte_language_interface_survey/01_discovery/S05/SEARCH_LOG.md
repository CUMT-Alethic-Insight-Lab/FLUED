# S05 search and reuse log

2026-11-08. Discovery/inventory specialist; no bulk new FULL reading, model runs, installs, production edits, commits, or outside-directory authored files. Searches used public mechanism terms only. Automatic tool-result caches are harness-managed; no download/conversion script was used.

## 1. Scope and baseline inspection

Read `../../PLAN.md`. No nested `AGENTS.md` was found under `docs/` with the dedicated glob. Consulted the old catalog header/first 167 lines, then **targeted title/stable-ID searches across the catalog**, rather than claiming a manual complete catalog read. Old catalog location: `../../../flued_multigranularity_survey_20261108/02_catalog/CATALOG.md`.

Read the actual complete card text, not only overview counts, for these **15 works**:

- B05/W0009.
- B08/W0351, W0360, W0363.
- B14/W0352, W0355, W0356, W0359, W0361.
- B22/W0509, W0516, W0518.
- B26/W0510, W0514.
- B04/W0061.

All paths resolve under `../../../flued_multigranularity_survey_20261108/03_reading/`. Their existing FULL labels describe the original cards' declared ranges; this task adds **zero fresh FULL paper reads**. W0004 CANINE is a catalog/abstract reuse, not a sixteenth read card.

Recovery audits read in full:

- `../../../flued_multigranularity_survey_20261108/07_scope_recovery/07_BYTE_SURVEY/COVERAGE_AUDIT.md`.
- Its `READING_RECOMMENDATIONS.md`.
- `../../../flued_multigranularity_survey_20261108/07_scope_recovery/08_GLOBAL_SCOPE/COVERAGE_AUDIT.md`.

These supply recovery-prior discovery for MYTE (N02), XTREME-UP (N07), and marginal-tokenisation likelihood (N08); our local R01/R02/R03 are **reuse**, not new discoveries. A further targeted stable-ID/title search over all `07_scope_recovery/` found no earlier entries for the thirteen fresh papers below. This is scoped de-duplication against catalog + inspected recovery audits, not semantic review of all 543 works/cards.

## 2. Actual online searches

**Six completed searches with returned results: four Scholar API searches and two rendered Bing searches.** A browser-control collision caused one failed create-tab and one failed tab-search call; they did not yield search evidence. No denial/authentication wall was bypassed.

Academic-source protocol: invoked `kimi-datasource:kimi-datasource`, obtained live `scholar` API documentation, then called `scholar_search` with its documented parameters. Browser searches used the built-in Kimi Code Desktop browser, not the user's Chrome/Edge. One research tab was reused; it was not shown because watching browser work was not requested.

| Search | Platform and exact query | Returned provenance and disposition |
|---|---|---|
| Q01 | Scholar `byte subword multilingual robustness`; years2015–2026,10results,English | Primary ACL hits: Zhang/Xu BMNMT (2022.coling-1.388), tokenizer imbalance (2022.amta-research.8), Char2Subword; other candidates included Hinglish/Indonesian/Springer/Elsevier works and parity-awareBPE. Accepted first two after original FetchURL checks; adjacent hybrid works left to relevant stream; unverified venue hits not promoted. |
| Q02 | Bing `byte subword multilingual spelling numeracy evaluation tokenization papers` | Rendered result snapshot yielded original arXiv2604.27263 *Decoupling...*, ACL BMNMT, and an unresolved *When Multilingual Evaluation Assumptions Fail* hit. Accepted Decoupling after fixed-version source check; unresolved hit uncounted. |
| Q03 | Scholar `character tokenization spelling numeracy language models`; years2015–2026,10requested,English | Returned original ACL SpellingBee, Tokenization Falling Short, Strawberry Problem; original arXiv2402.14903; AAAI CharBench; also BrokenTokens, letter-counting article and broad historical review. Accepted the five named original-verified works; others uncounted. Scholar date for BrokenTokens mixed2026 listing and2025 proceedings: no inference made from it. |
| Q04 | Bing `"Fully Character-Level Neural Machine Translation" "Character-Aware Neural Language Models"` | Rendered result snapshot identified1610.03017v3 and a Kim etal. reference. Original arXiv abs/version checks accepted both; character-level rather than byte evidence retained. |
| Q05 | Scholar `"Byte-based neural machine translation"`;3results,English | Original ACL W17-4123, NAACL2025MoCE, AAAI2020byte-level subwords. W17-4123 verified and accepted; other two adjacent candidates uncounted rather than padded rows. |
| Q06 | Scholar `"Neural Machine Translation without Embeddings"`;2requested,English | Original ACL2021.naacl-main.17, Shaham/Levy; accepted after fetching original page. |

The API saved four raw CSVs in this assigned directory using explicit absolute project paths (`scholar_results.csv`, `scholar_spelling.csv`, `scholar_history.csv`, `scholar_embeddingless.csv`). These were temporary query records; their meaningful provenance is preserved above and the CSVs were removed after deliverable checks so the handoff contains only the four requested Markdown files.

### Browser collision record

- Initial create-tab query `byte level language models multilingual robustness tokenization spelling numeracy character 2025 2026`: `TAB_NOT_ACTIVE`, no result inspected.
- First create-tab retry used the narrower Q02 and succeeded; exact rendered text inspected.
- Attempted `tab.search` query `language models tokenization spelling numeracy arithmetic byte character "2024" "2025"`: `TAB_NOT_ACTIVE`, not counted. Activated this task's tab and subsequently issued Q04 successfully. Other agents' tabs were never closed.
- The profile had >10 tabs already open; to avoid adding sidebar clutter, this task reused one research tab and closed it at completion.

## 3. Source/identity/version verification register

`A` abstract/identity; `P` selected original methods/results; `N` normative sections. Fetching a whole source did **not** make it FULL reading.

| Source actually fetched | Verified / inspected; remaining boundary |
|---|---|
| https://aclanthology.org/2022.coling-1.388/ and https://aclanthology.org/2022.coling-1.388.pdf | Title/authors/year/pages verified; P original§§3–4,§5.4 and related result prose. Random-byte ensemble aligns permuted output distributions; IndCorpus dev-as-test and800B training filter identified. Table images and all appendix specifics not read, no fresh FULL. |
| https://aclanthology.org/2022.amta-research.8/ | A title/authors/year/pages/abstract. Search snippet's byte-fallback negative result not promoted without original body reading. |
| https://aclanthology.org/2024.acl-long.804/ and https://arxiv.org/abs/2403.10691v2 | A original MYTE identity,99-language claim; fixedv2 is2024-11-11 and associated ACL2024 DOI. Abstract check repeated once; no version-difference comparison. |
| https://arxiv.org/abs/2305.11938v2 | A XTREME-UP title/scope/authors/history; fixedv2 is2023-05-24. Repeated fetch confirmed same evidence, not another work or deeper read. |
| https://aclanthology.org/2021.emnlp-main.161/ | A marginal-likelihood work andOOD claim. No estimator equations/variance/table verification. |
| https://arxiv.org/abs/2604.27263v1 ; https://arxiv.org/abs/2604.27263v2 ; https://arxiv.org/html/2604.27263v2 | A version history first checked, then P §§2.2,5.1–5.6,8 and figure descriptions. v1Apr29/v2May14,2026; English-centric limitation explicit. HTML duplicates numeric math glyphs (e.g.4 displayed44), interpreted from equations/prose, **not** new numerical results. Appendix tables missing, curves not visually digitized. Submitter names differ acrossversions; not used as author roster. |
| https://arxiv.org/abs/1610.03017v3 | A fixed2017-06-13version and TACL identity; character CNN/maxpool shared multilingual encoder. Exact character inventory/decoder mechanism awaits full read. |
| https://arxiv.org/abs/1508.06615 and https://arxiv.org/abs/1508.06615v4 | A title/character-input,word-output distinction; latest listedv4Dec1,2015. No paper-method/experiment full read. |
| https://arxiv.org/abs/1711.02173 and https://arxiv.org/abs/1711.02173v2 | A character-NMT noise counterexample and robustness responses; fixedv2Feb24,2018. No per-language table inspected. |
| https://aclanthology.org/2022.naacl-main.373/ and https://aclanthology.org/2022.naacl-main.373.pdf | A identity; P §§2–3/5 and associated result prose: frozen-embedding spelling probe, held-out/filter/random controls,24hMLM intervention. Table images/appendices not comprehensively checked; extracted architecture language internally loose so only transformer probe is claimed. |
| https://arxiv.org/abs/2402.14903 and https://arxiv.org/html/2402.14903v1 | A fixedv1Feb22,2024; P only opening/title/Fig1caption. Later controls and appendices not read. GPTMarch2023 grouping intervention is not a retrained byte-versusSW experiment. |
| https://aclanthology.org/2024.findings-emnlp.86/ | A exact title/author/year/pages, reported BPE-dropout mitigation. |
| https://aclanthology.org/2025.emnlp-main.1434/ | A StrawberryProblem original abstract,19tasks,percolation account,unspecified architectural modification. No invented implementation detail. |
| https://ojs.aaai.org/index.php/AAAI/article/view/40615 | A CharBench authors,DOI,volume/pages,2026-03-14publication and counting/position result distinction. No language/floor derivation from percentages. |
| https://aclanthology.org/W17-4123/ | A direct byte–character historical NMT,2017,authors/pages/DOI; no actual encoding/pairs confirmed from body. |
| https://aclanthology.org/2021.naacl-main.17/ | A one-hotbyte/dropout response,EN→10languages. Training costs/sequence filters uninspected. |
| https://arxiv.org/abs/2103.06874v4 | A CANINE original fixedversion and optional subword-supervision distinction;2022-05-18. No card invented. |
| https://www.rfc-editor.org/rfc/rfc3629.html | N §§1,3–4,7,10; fixedRFC3629Nov2003. ExactASCII/lead/continuation grammar, invalid ranges,normalization examples. Not a model paper or learned technique. |
| https://www.unicode.org/reports/tr15/tr15-57.html | N Unicode17.0.0rev57,2025-07-30; §§1.1–1.2 and compatibility-loss warning targeted through cached-result Read/Grep. Rest of large annex not read. |
| https://www.unicode.org/reports/tr29/tr29-47.html | N Unicode17.0.0rev47,2025-08-17; intro,conformance,§3/Table1a targeted through cached-result Read/Grep. Boundary-rule implementation and entire annex not read. |
| https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-3/ | Auxiliary N C8–C10 only; extraction truncated beforeUTF8D92. Do not claim complete chapter/encoding-definition inspection; RFC source supplies inspected syntax. Not counted separately fromU01 reference family. |

### Rejected source guesses / access errors

- `https://aclanthology.org/2017.tacl-1.28/` returned404, not used; found correct historical work by original arXiv1610.03017v3 search afterward.
- `https://arxiv.org/abs/1511.04596` is a heat-conduction paper, rejected immediately, not counted. Correct Character-Aware work verified at1508.06615v4.
- Three Grep calls initially used schema key `C` rather than `-C` and failed validation; corrected calls were used. No source absence inferred from these failures.
- No authentication-wall workaround, paid resource, download, conversion or external code upload.

## 4. De-duplication and numbers

Stable identifiers and title fragments were checked over the **whole old catalog** with dedicated Grep. Fresh candidate batch included2604.27263,1711.02173,2402.14903,2022.coling-1.388,2022.amta-research.8,2022.naacl-main.373,2024.findings-emnlp.86,2025.emnlp-main.1434,AAAI40615,1508.06615,1610.03017,W17-4123 and2021.naacl-main.17; zero matching works found. Recovery-prior candidates2403.10691,2305.11938 and2021.emnlp-main.161 were also catalog-absent but explicitly found in the byte recovery audit, so marked **R**, not **N**.

Deliverable counts: **35 works =16catalog reuse +3recovery reuse +13fresh academic +3normative specifications; 54 inventory records; 0 fresh FULL paper reads; 10 prioritized missing-evidence full-reading handoffs**. The old-card reuse is15actual card reads, not the old corpus's total FULL count.

## 5. Verification

Static validation checks local source links, work/record cardinality, unique IDs and all35works' presence in inventory; search-log provenance, partial-reading labels and the10-paper queue checked. `git status --short` obtained before final validation to distinguish pre-existing untracked survey/corpus/bundle files; only this assignedS05directory was authored. No training/build/test execution was appropriate to this documentation-only discovery task. Final command results are recorded in READING_HANDOFF.md.
