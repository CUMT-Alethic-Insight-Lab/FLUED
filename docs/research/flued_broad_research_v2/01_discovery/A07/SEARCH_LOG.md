# A07 — Executed search, source-access and version-check log

**Date:** 2026-11-09. **Scope:** ICLR 2027 byte/codepoint/character, hybrid supervision, tokenization/segmentation/patching, byte decoding and multilingual interfaces; existing BIW141 comparison and targeted recent-version recovery. A08 handles broader topics and central venue map. This log reports actions actually taken, not a proposed search plan.

[Findings](COVERAGE_AND_FINDINGS.md) · [identities/problems](WORKS_AND_PROBLEMS.md) · [reading handoff](READING_HANDOFF.md).

## 1. Tools, boundaries and depth

- Used actual **WebSearch**, **FetchURL**, the **built-in Kimi Code Desktop browser** (`mcp__desktop_browser__run`), repository Read/Grep/Glob and read-only Git status. No academic data-source tool was used, so no scholar/arXiv data-source API invocation or plugin installation was needed. arXiv was read directly as public web content.
- Search terms below contain public venue, paper-title and field terms only; no internal text/data was uploaded. No external project-source upload, author deanonymization, paid access, install, training, subprocess agent, commit/push, production edit or evidence-registry change.
- Auth/challenge/login responses were treated as unavailable content. Normal public group/notes API and PDF/HTML/arXiv routes are logged separately. No CAPTCHA/challenge was solved or circumvented.
- **No manual PDFs were downloaded.** Future PDF destinations are explicitly reserved under `docs/research/flued_broad_research_v2/01_discovery/A07/sources/` in READING_HANDOFF. Tool-managed text-extraction caches are not archived PDF deliverables and are not represented as local paper files.
- WebSearch returns a bounded ranked subset; no total results or complete page traversal is exposed. Official snippets are indexed official evidence, not live forum/decision checks. Source bodies were requested for relevant results; failures and limits are below. No abstract or snippet was promoted to FULL.

## 2. Local scope recovery and dedup actually performed

Read the governing `PLAN.md` and original `FOLLOWUP_DIRECTIONS.md`, the older byte-axis `COVERAGE_AUDIT.md` and `READING_RECOMMENDATIONS.md`. The old audit has since been superseded in several reading statuses by the independent byte survey.

Read the BIW catalog opening/current entity index and relevant targeted sections (not all 5,734 lines); exact-title and stable-ID content searches checked both:

- `docs/research/byte_language_interface_survey/02_inventory/WORK_CATALOG.md`;
- `docs/research/flued_multigranularity_survey_20261108/02_catalog/CATALOG.md`.

Executed exact content searches for `Turnip|Retokenize|GlitchPatch|PriorBPB|ByteMark|BridgeSTOP|Who Gets|Regularizing Tokenization|Separating Script|Constructive Prediction|LEAD:` and for `Why Pretraining Fails|Cross-Lingual Knowledge|2609.19291|2609.34065|2610.04399|2610.14427`: no matching catalog row returned. These checks support “not in the two current identity registers,” not “not mentioned anywhere in every prior discovery note.”

Actual reused full-card text read: BIW-0103/R06; BIW-0078/R09; BIW-0076/R05; BIW-0079/R05; BIW-0108/R08; BIW-0004/R01; BIW-0008/R03; BIW-0077/R10; BIW-0035/R08; BIW-0080/R04; W0352/B14; W0518/B22. Additional current catalog sections inspected for BIW-0015, 0028, 0097/0098/0099. This is **reuse/card inspection**, not twelve newly read papers or original-paper recertification.

The v1 saved primary text `byte_language_interface_survey/03_reading/R05/sources/BIW-0076.txt` was searched for `500M`, `100B`, `Table 4`, seed/latency terms and its C.2/D passages directly read, for comparison with v2. No existing card/catalog was modified.

## 3. Exact WebSearch queries issued

The following are verbatim query strings, grouped by purpose. Some returned mainly noise, bibliography hits or unrelated tokenization modalities; those results were not converted into included works. Repeated routes/queries are visible as separate lines where material; no exact-call-count performance claim is made from this transcription.

### 3.1 Official venue/interface discovery

```text
site:openreview.net ICLR 2027 tokenization byte character language
site:openreview.net "ICLR 2027" "byte"
site:openreview.net/forum "ICLR 2027" "tokenization"
site:openreview.net "ICLR 2027" "byte-level" "language"
site:openreview.net "ICLR 2027" "character" "tokenizer"
site:openreview.net "ICLR 2027" "patch" "byte"
site:openreview.net "ICLR 2027" "codepoint"
site:openreview.net "ICLR 2027" "tokenizer-free"
site:openreview.net "ICLR 2027" "segmentation" "language"
site:openreview.net "ICLR 2027" "hybrid" "tokenization"
site:openreview.net "ICLR 2027" "multilingual" "tokenizer"
site:openreview.net "ICLR 2027" "byte decoding"
site:openreview.net/forum "ICLR 2027" "UTF-8"
"ICLR 2027" "learned tokenization"
"ICLR 2027" "multi-byte"
"ICLR 2027" "H-Net" "chunking"
"ICLR 2027" "Byte Latent Transformer"
"ICLR 2027" "character-level language"
"ICLR 2027" "learned segmentation"
"ICLR 2027" "byte models"
"ICLR 2027" "tokenization" "compression"
"ICLR 2027" "code point"
"ICLR 2027" "byte" "token-free"
"ICLR 2027" "tokenization-free"
```

**Yield:** Turnip, byte distillation, MRT, script/cost, Compiled Tokenizers, PriorBPB, ByteMark, cross-lingual knowledge, frozen retokenization, GlitchPatch, name access, BridgeSTOP, LEAD and lexical-code leads. **Noise:** image segmentation, time-series patching, finance tokens, music/MIDI, quantization bytes, detector papers containing only “byte-identical,” references to BLT/ByT5 rather than new byte architectures, cryptocurrency tokenization. These do not fill the interface map. No new verified raw-codepoint causal generator was recovered.

### 3.2 Forum-locator and metadata probes (including failed search refinements)

```text
site:openreview.net/forum?id=tlYzFXxkji
site:openreview.net/forum?id=tKqgR3uW7u
site:openreview.net/forum?id=FPNRyuXJC0
"TURNIP" "Tokenizers Are Secretly"
"MRT" "Regularizing Tokenization"
"Separating Script and Vocabulary"
"Learning to Retokenize" "2027"
"TokSuite" "2027"
"Distilling Smaller, Stronger Byte Models" "2027"
site:openreview.net/forum "Turnip" "2026"
site:openreview.net/forum "MRT" "Regularizing"
site:openreview.net/forum "Separating Script"
site:openreview.net/forum "Breaking the Token Ceiling"
site:openreview.net/forum "Learning to Retokenize"
site:openreview.net/forum "GlitchPatch"
site:openreview.net/forum "Who Gets a Token"
"tlYzFXxkji" "Abstract"
"tKqgR3uW7u" "Abstract"
"FPNRyuXJC0" "Abstract"
"O1JpRRUeGW"
"vfj1rb7yk1"
site:openreview.net "MRT: Regularizing" "September"
site:openreview.net "GlitchPatch" "ICLR"
site:openreview.net "Who Gets a Token" "ICLR"
site:openreview.net "Why Pretraining Fails" "modified"
"Turnip" "tlYzFXxkji" "modified"
"PriorBPB" "Submission" "modified"
"ByteMark" "Submission" "modified"
"Compiled Tokenizers" "modified"
```

**Yield/limits:** exact URL-as-site probes often returned irrelevant popular OpenReview pages; they are not evidence for the requested IDs. Title/index refinements recovered official forum labels/dates for five new candidates and a partial modification field for Turnip. `Why Pretraining Fails` and PriorBPB return a full modified-date field; ByteMark/Compiled Tokenizers do not. “Modified 05 …” on Turnip remains truncated, not silently completed to another paper's date. Searching TokSuite with 2027 recovered its actual **ICML 2026** official session; not an ICLR 2027 discovery.

### 3.3 Title matching, alternate original-source discovery and problem expansion

```text
"GlitchPatch"
"Who Gets a Token, and What Does It Carry"
"Turnip: Tokenizers Are Secretly" arxiv
"MRT: Regularizing Tokenization" arxiv
"Separating Script" "Tokenization Cost" arxiv
"Learning to Retokenize" language model
"GlitchPatch" arxiv
"PriorBPB"
"Compiled Tokenizers"
"ByteMark" "watermark"
"LEAD" "Models Know the Language"
"BridgeStop" "tokenization"
"Compiled Tokenizers" "Schema"
"LEAD: Models Know" arxiv
"BridgeSTOP: Bridging Streaming Tokenization and LLM Prefill" arxiv
"Learning to Retokenize" "vfj1rb7yk1"
"Constructive Prediction" "Lexical"
"Why Pretraining Fails to Share Cross-Lingual Knowledge"
site:openreview.net "CONSTRUCTIVE PREDICTION: THE ROLE OF LEXICAL"
"MRT: Regularizing Tokenization with Morphology for Low-Resource Indic Languages"
```

**Yield/limits:** arXiv originals for GlitchPatch, names, ByteMark and cross-lingual knowledge; official PriorBPB research blog and distinct workshop locator; expanded full titles for frozen retokenization and constructive lexical prediction. No confirmed arXiv original for Turnip/MRT/script-cost/retokenization/BridgeSTOP/LEAD in these results. Reference-list arXiv numbers (for example in Turnip) were **not** taken as that paper's own arXiv identity. Search results displaying same-title public author names were not used to identify anonymous conference authors. Prediction-market pages and generated-review sites were not used as venue/scientific evidence.

## 4. Official group, listing and browser access — exact routes and results

| Route/action | Result actually observed | Retry/pagination interpretation |
|---|---|---|
| [Official CFP](https://iclr.cc/Conferences/2027/CallForPapers) via FetchURL | Full relevant call text, dates, double-blind policy | M-live; only this official schedule used, not third-party projected dates |
| [Group UI](https://openreview.net/group?id=ICLR.cc/2027/Conference) via FetchURL | Login/loading shell only | Not a submission list or source count |
| Built-in browser `browser.create_tab` for group | `TAB_NOT_ACTIVE` control-change error | Followed once with `browser.get_state`; no repeated control fighting |
| Built-in browser `page.text.snapshot`, document scope, group page | OpenReview/loading/footer text only, not usable paper metadata | Browser route confirms unresolved rendered-content gap; no challenge interaction |
| [Group API](https://api2.openreview.net/groups?id=ICLR.cc/2027/Conference) via FetchURL | JSON, group count1, readers everyone, `public_submissions=true`, registered venue IDs and invitation; `fromCache=true` | Official group configuration verified, not note enumeration |
| [Public notes search](https://api2.openreview.net/notes/search?term=byte&content.venueid=ICLR.cc%2F2027%2FConference%2FSubmission&limit=100) | Only a code-fence fragment in tool result | No valid JSON, result count or pagination token; **not zero matches** |
| [Active notes page0](https://api2.openreview.net/notes?content.venueid=ICLR.cc%2F2027%2FConference%2FSubmission&limit=1000&offset=0) | Verification challenge | **0 usable list pages**; no offset1000/page1 requested, no claim of exhaustive active/withdrawn/desk-rejected coverage |
| [Public submissions listing](https://openreview.net/submissions?venue=ICLR.cc%2F2027%2FConference&search=byte) | Verification challenge | Normal alternative public listing also unavailable; no pagination followed |

The notes API is an official public metadata route, not a credentialed workaround. A challenge response was not treated as successful retrieval. The group UI's existence is separately verified by its API and the official call, not by the blank UI alone.

## 5. Individual official-source attempts

All URLs below were actually fetched and returned the same verification message, not paper/forum content, unless a result is explicitly given elsewhere. Indexed official snippets may still exist and are labeled separately in the work register.

### 5.1 Forum fetches

```text
https://openreview.net/forum?id=tlYzFXxkji
https://openreview.net/forum?id=tKqgR3uW7u
https://openreview.net/forum?id=FPNRyuXJC0
https://openreview.net/forum?id=CixpFoiooB
https://openreview.net/forum?id=kB8Lwd90Io
https://openreview.net/forum?id=losZJYZ6xK
https://openreview.net/forum?id=A4XoBLOXvg
https://openreview.net/forum?id=DbzLzs5VL7
https://openreview.net/forum?id=NpBoc9jkFs
```

### 5.2 Public API note fetches

```text
https://api2.openreview.net/notes?id=tlYzFXxkji
https://api2.openreview.net/notes?id=tKqgR3uW7u
https://api2.openreview.net/notes?id=FPNRyuXJC0
```

### 5.3 Official paper fetches

```text
https://openreview.net/pdf?id=tlYzFXxkji
https://openreview.net/pdf?id=s2yS6VAWIP
https://openreview.net/pdf?id=gbaS4smhnV
https://openreview.net/pdf?id=vfj1rb7yk1
https://openreview.net/pdf?id=FPNRyuXJC0
https://openreview.net/pdf?id=tKqgR3uW7u
https://openreview.net/pdf?id=DXrf6mhnGR
https://openreview.net/pdf?id=O1JpRRUeGW
```

PDF-only candidates with no successful forum retrieval remain unverified locators in the register. No revisions endpoint was successfully fetched; a Turnip revision-history **search result** saying “No revisions to display” was not taken as proof that the underlying paper never changed. No anonymous author names, profile routes or public review content were reproduced.

## 6. Primary arXiv and other original-source fetches

| Exact route(s) | Result / evidence actually used | Depth and version handling |
|---|---|---|
| [2609.12303](https://arxiv.org/abs/2609.12303) | Abstract/history; v1 2026-09-11 only displayed | Existing BIW-0103; actual full v1 card reused. No new version/reading credit |
| [2610.04399](https://arxiv.org/abs/2610.04399) | Abstract/history; v1 2026-10-03 | N09 A; title match to official PDF, no author matching |
| [2610.04399v1 HTML](https://arxiv.org/html/2610.04399v1) | First fetch network error; one retry succeeded with long body | Selected §§1–2 and opening of3 read; final extraction passage inspected. **P**, not entire paper |
| [2609.34065](https://arxiv.org/abs/2609.34065) | Abstract/history, v1 2026-09-28 | N08 A |
| [2609.34065v1 HTML](https://arxiv.org/html/2609.34065v1) | Long original body; selected §§1–4 passages read from tool extraction | N08 P: setup, matching and explicit observational-not-isolated-causation statement; appendices/intervention protocol not fully read |
| [2610.14427v1 HTML](https://arxiv.org/html/2610.14427v1) | Long original body; selected §3.1–3.2 and searched experiment/limitations passages | N06 P; no full table/security proof certification |
| [2610.14427v1 abstract/history](https://arxiv.org/abs/2610.14427v1) | Abstract and v1 2026-10-10 history | Stable version pinned; forum revision remains unknown |
| [2609.19291](https://arxiv.org/abs/2609.19291) | Abstract/history, v1 2026-09-16 | N07 A; identical-language/disjoint-token control and abstract claims, not inspected full experiments |
| [2605.09630 current](https://arxiv.org/abs/2605.09630) | v1 2026-05-10; **v2 2026-11-06** | Real later edition absent from v1 card |
| [2605.09630v2 HTML](https://arxiv.org/html/2605.09630v2) | Selected §§4–5/7, B.3/C.2/D/E.4 read; Table4 HTML cells absent in extract | P version update: 500M/100B runs, single runs, no measured serving latency and checkpoint-specific trigger. No whole-version FULL or exhaustive diff |
| [2602.13940](https://arxiv.org/abs/2602.13940) | v1–v4 histories, latest displayed v4 2026-09-14 | Existing BIW-0078 full v4 card already current |
| [2511.11346](https://arxiv.org/abs/2511.11346) | v1 2025-11-14, v2 2026-06-02 | Existing MTPC full v2 card; v1 Multi-Token title is not a new entity |
| [2608.15454](https://arxiv.org/abs/2608.15454) | v1 2026-08-16, v2 2026-08-21 | Existing BIW-0015 full-card provenance already current; no new read |
| [2610.05978](https://arxiv.org/abs/2610.05978) | Abstract/history v1 2026-10-05 | Existing BIW-0028 corrected catalog/card remains version source; abstract not full read |
| [2512.15586 current](https://arxiv.org/abs/2512.15586) then [v2](https://arxiv.org/abs/2512.15586v2) | First route network error; fixed-v2 normal retry succeeded, histories v1 2025-12-17 / v2 2026-02-09 | Existing Bolmo card v2; no newer edition displayed in fetched history, no 2027 venue inferred |
| [2506.14761 current](https://arxiv.org/abs/2506.14761) then [v1](https://arxiv.org/abs/2506.14761v1) | First route network error; fixed-v1 retry succeeded, history v1 2025-06-17 | Existing AU-Net full v1 card reused; no automatic ICLR association |
| [PriorBPB research blog](https://aleph-alpha.com/en/blog/priorbpb/) | Original public post dated2026-10-13; formula, controls, limitations and separate workshop locator | P **blog**, not official submission/full paper. No author identities carried to anonymous record; workshop not conference acceptance |
| [Official ICML2026 session68663](https://icml.cc/virtual/2026/session/68663) | TokSuite entry/abstract among session papers | Supports non-2027 classification together with existing formal PMLR306 metadata; no new scientific FULL |

Long FetchURL bodies were paged/searched selectively, not exhaustively read. Their tool truncation/cache notices were respected: claims only use opened passages or displayed abstracts, not unseen remainder. No manually created source PDF/text files are claimed.

## 7. Findings from failed routes are findings about access, not about science

- A blank listing/search result does **not** establish that ICLR 2027 has no byte papers.
- A forum label in an indexed official page is a useful submission record, but does not close current status/revision verification.
- An indexed PDF header is weaker still; it cannot certify membership in the official group's active cohort.
- A title/abstract match to arXiv gives a separately versioned scientific source; it does not reveal the anonymous authors or guarantee identical submission content.
- No raw-codepoint/hybrid architecture found in this bounded pass is a **search gap**, not a negative field census.
- The most actionable new source-version fact is Scratchpad Patching v2. Several purported missing classics are already read in the later BIW survey, so rereading them for counts would misrepresent work completed.

## 8. Artifact and verification receipt

Authored only four Markdown files under this specialist-owned folder: `COVERAGE_AND_FINDINGS.md`, `SEARCH_LOG.md`, `WORKS_AND_PROBLEMS.md`, `READING_HANDOFF.md`. No final total-report synthesis, catalog merge, old-card edit or venue-map edit. A foreground Python validation passed: exact four required files, all local Markdown links resolve, all thirteen local candidate records and thirteen priority reading rows present, UTF-8/newline/trailing-whitespace checks pass, and no downloaded PDF exists under A07. `git diff --check -- <A07>` returned exit0; because the folder is untracked, the direct content validator, not that empty tracked diff, supplies the whitespace/link check. Post-write `git status --short -- <A07>` reports only the new A07 directory. No code build/test suite was run for this documentation-only discovery task. Initial Git status already contained untracked survey roots and bundles; those unrelated artifacts are not modified or deleted by A07. These checks validate artifacts and references, not scientific correctness or live venue completeness.
