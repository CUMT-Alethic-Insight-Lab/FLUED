# V18 — source reading and access summary

## Scope and counts

Six distinct assigned source tasks; **1 FULL** (the public 2009 arXiv v1 PSR learning paper); **0 PARTIAL; 5 BLOCKED original bodies** (V11, V16, V20, V21, V24). Each has its canonical-ID card with the precise route, status, unresolved scientific questions, and failure. The five official records were verified independently in the earlier R1/R2 audits and are **ICLR 2027 submissions, not accepted papers**. V11/V16/V21 are in R2; V20/V24 are R1-only, not freshly refreshed here. Paper/PDF revision and decision status remain unknown; note version 2 is not a PDF version. Anonymous authors remain anonymous. The five body tasks remain open; the PSR original is not a substitute for their different questions. No inference of blanket OpenReview unavailability.

| Work | Disposition | Original evidence or gap |
|---|---|---|
| [BR-PSR-0912.2385](BR-PSR-0912.2385.md) | FULL, arXiv 0912.2385v1, 2009-12-12 | all 10 pages and both figures; finite-rank/coverage and 78/100 successes are essential qualifications |
| [BR-A08-V11](BR-A08-V11.md) | BLOCKED | LoopLA; exact PDF returned HTTP 403 |
| [BR-A08-V16](BR-A08-V16.md) | BLOCKED | Farsighted Correction; exact PDF returned HTTP 403 |
| [BR-A08-V20](BR-A08-V20.md) | BLOCKED | Exact Finite-Query KV Cache Compilation; exact PDF returned HTTP 403 |
| [BR-A08-V21](BR-A08-V21.md) | BLOCKED | attention placement; exact PDF returned HTTP 403 |
| [BR-A08-V24](BR-A08-V24.md) | BLOCKED | Predictive State Has a Scope; public forum PDF locator returned HTTP 403; content reference unavailable |

## Acquisition and version evidence

Normal Git Bash curl `/mingw64/bin/curl`, unchanged proxy/trust and revocation settings, HTTPS-only redirect policy, connect limit 15 seconds and total limit 90/120 seconds. Each of the five individually requested URLs is recorded on its card; each returned curl exit 22, HTTP 403, TLS result 0 and proxy 0, zero retained body. These are HTTP denials, not timeouts or the previous revocation-offline failure; no retries through other OpenReview endpoints or identities, no challenge bypass, certificates disabled, or system changes. A 403 is not grounds for a transient retry. PSR v1 succeeded HTTP 200, curl 0, TLS result 0, proxy 0; 2,673,711 bytes, valid PDF header and EOF, 10 pages, strict-UTF8 text extraction with existing `pdftotext`. SHA-256 and exact project-local paths are in its card. Its two figure-bearing pages were rendered with already-installed PyMuPDF and inspected visually; temporary renders removed. All source downloads remain within `V18/sources/`.

Public-title searches in Kimi's built-in browser for all five titles returned `ERR_CONNECTION_CLOSED`; V21's initial parallel request lost tab control and a separate retry also returned `ERR_CONNECTION_CLOSED`. No search-results content was obtained. A separate public arXiv API query was normally retrieved over verified curl:

`https://export.arxiv.org/api/query?search_query=all%3ALoopLA%20OR%20all%3A%22Farsighted%20Correction%20of%20Shortcut%20Learning%22%20OR%20all%3A%22Exact%20Finite-Query%20KV%20Cache%20Compilation%22%20OR%20all%3A%22Where%20You%20Put%20Attention%20Matters%22%20OR%20all%3A%22Predictive%20State%20Has%20a%20Scope%22&start=0&max_results=30`

Returned totalResults=0, start=0, max_results=30. This one compound query is bounded, not five validated exhaustive exact-title searches and not proof a public preprint/mirror does not exist. No legitimate independently identified related version was recovered. The safe next step is a separately identifiable public author preprint or public mirror searched without de-anonymization, or a normally accessible official PDF; record its exact version and read it without assuming equality to the forum manuscript. No content claim was made from title or abstract alone.

## Main transferable evidence and gaps

The PSR paper's conditional consistency and real closed-loop trial extend existence-only arguments, not universal compression or language memory guarantees. The learned policy's 18.2 steps is only over 78 successful trials; 22 of 100 failed. A privileged-geometry A* comparator and unreported overall costs limit interpretation. Rich feature banks, exploration, SVD, operator storage and planner computation matter alongside deployed state dimension. No other batch source supplies body-verified results; loop timing/matched-FLOP, shortcut mechanism and controls, finite-query theorem quantifiers/held-out behavior, attention placement/path use, and pair-state scope/equal-bit controls remain unresolved. See each card for direction mapping and required carry-through.

No shared catalog, evidence registry, code, model training, installation, subagent, commit or challenge bypass was involved. These are source/documentation deliverables; software build/test and independent experimental reproduction are not applicable.
