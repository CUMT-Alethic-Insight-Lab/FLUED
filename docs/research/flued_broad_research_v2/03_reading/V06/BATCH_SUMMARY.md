# V06 — batch summary and access receipt

Seven assigned distinct works; **6 FULL, 1 PARTIAL, 0 BLOCKED** after the access-diagnostic recovery. FULL means the locked paper's substantive main body and carrying appendices were read, not proof verification, reproduction, formal-edition equality or code execution. PARTIAL includes a substantially readable body with a missing carrying component. No work is counted twice for editions. Six FULLs are newly read in this batch, including BIW-0096 v2 and GenFirst v1 completed during recovery; earlier discovery's selected passages were routing inputs, not old FULL cards. **No v1 FULL was reused or silently upgraded to v2 FULL.** No ICLR 2027 acceptance or forum identity is claimed.

| Canonical ID | Locked edition | Status and read scope | Important remaining gap |
|---|---|---|---|
| [BIW-0096](BIW-0096.md) | 1901.05534v2 | FULL: HTML §§1–7/A–G and all original table rows | Two recovery PDF timeouts; raw original HTML tables close the scientific reading gap. Equal-compute comparison remains unresolved. |
| [BR-LD-N04](BR-LD-N04.md) | 2301.12618v3 | FULL: PDF pp.1–23, §§1–6/A–D | Equal-compute and independent test evidence still a research need; proceedings-edition equivalence unverified. |
| [BR-LD-N05](BR-LD-N05.md) | 2503.05631v2 | FULL: PDF pp.1–20, §§1–8/A–E | Larger-host and full training-opportunity controls remain empirical questions; formal edition unaligned. |
| [BR-A05-N02](BR-A05-N02.md) | 2605.06870v3 | FULL: PDF pp.1–23, §§1–5/A–D | Nonlinear theorem transfer, assigned-payload rank and equal-FLOP controls unproved; HTML/PDF author-line mismatch unresolved. |
| [BR-A05-N03](BR-A05-N03.md) | 2608.29335v1 | FULL: PDF pp.1–39, §§1–7/A–D; method and Table 2 visually inspected | Table 2 schedules have different total epoch budgets; §5.1/Table 17 vs Appendix C.1 reverse text-to-image variant labels. |
| [BR-A05-N06](BR-A05-N06.md) | 2412.00104v2 | FULL: PDF pp.1–21, §§1–5/A.1–A.6 | Formal ICLR 2025 edition vs v2 not compared; theoretical conclusions limited to stated ansatz. |
| [BR-LD-N06](BR-LD-N06.md) | 2610.19113v1 | PARTIAL: HTML §§1–8 and A–P; PDF acquired for supplement inspection | Paper Appendix O explicitly mentions a separate supplement; no locator or attachment found, so its contents remain **not located/read**, not proven unprovided. |

## Cross-paper findings

1. **Formation is not the endpoint.** The VAE study provides an encoder-lag alternative under a variational objective, not an equal-compute general cure. CIWL in Strategy Coopetition still requires a correct context label; a later-dominant competitor can help a shared component form while suppressing the target later. Nguyen–Reddy instead models independent additive circuits; their results are not interchangeable. Every case is bounded by its task, initialization, architecture and intervention.
2. **Schedule mechanisms differ.** The VQ paper delays a quantizer to protect effective directions; GenFirst jointly adjusts prior/entropy weights with fixed reconstruction weights and later frozen-prior training. Its main Table 2 compares 640 vs 320 total epochs and is not equal-compute proof. Neither determines a particular memory architecture. VQ's β=0 random-unused-code example also makes raw all-codebook PCA rank an unreliable proxy for transmitted payload.
3. **Local signals are not deployment outcomes.** ForkMerge's one-step common-checkpoint cosine/validation contrast is not an all-history shortcut test. The language-model study separates prompt control from candidate choice, unassisted answer construction and transfer, and retains negative transfer/precision controls. Validation-selected branches and adaptation require their data and compute permissions accounted for.
4. **Next work:** locate/read the language-model paper's explicitly referenced supplement; it was not located in the main PDF or narrow repository search. Do not infer nonexistence or bypass access controls. Resolve GenFirst's within-paper variant-label discrepancy before assigning numerical outcomes. Target-host causes require new authorized experiments with matched exposure and optimization budget, fixed windows, natural content interventions and all seeds.

## Acquisition provenance and exact failures

Source copies below were downloaded directly by `curl --fail --location` from `https://arxiv.org/pdf/<edition>` into this batch's `sources/` and text extracted with `pdftotext -enc UTF-8 -layout`. SHA-256 of retained complete PDFs:

| Edition | SHA-256 |
|---|---|
| 2301.12618v3 | `b38c4414522338f97e5168a57b5d438983d0bfa20d3eff2dfdcc630668f21a34` |
| 2503.05631v2 | `7b3634ec192553bd03cc8fc643f216aa62fd981ee86b13d3d28d2f12d4ff6462` |
| 2605.06870v3 | `b0d4b87b82a27e3772d0d7416c7fa2ae6534cb0dfb3cb4f65da1904f34ed2187` |
| 2412.00104v2 | `49144ae276328df580ccf4a7ce747620919d28558b127a972c1f47f9689155b3` |

- `https://arxiv.org/pdf/1901.05534v2`: curl timeout 35 s after 65,536/2,761,340 bytes; its HTML was readable with absent table cells.
- `https://arxiv.org/pdf/2503.05631v2`: initial 35 s timeout at 423,918/1,818,293 bytes; a single normal retry succeeded. The HTML extraction ended at Appendix C heading; complete PDF supplied C–E.
- `https://arxiv.org/html/2608.29335v1`: HTTP 404. `https://arxiv.org/pdf/2608.29335v1`: initial connection timeout, then one normal retry timed out after 110 s at 1,966,080/16,030,715 bytes.
- `https://arxiv.org/pdf/2610.19113v1`: 35 s timeout at 704,512/1,379,397 bytes. Its main HTML and embedded A–P were read; an external supplement remains unavailable in this assignment.
- Initial three incomplete downloads were removed rather than left as purported PDFs; the fourth was replaced by the successful retry. Historical errors above are retained and do not describe current coverage.

### Recovery after ACCESS_DIAGNOSTIC

Used the diagnostic's normal Git Bash curl/Schannel route, without proxy, system, trust-store or certificate changes. GenFirst v1 PDF returned HTTP 200/TLS 0/proxy 0, 16,030,715 bytes, SHA-256 `366167d8caea1d8990c326d87222090a898a82f54aa222ad5b9e2ccad4719f78`; language-model v1 PDF returned 200/0/0, 1,379,397 bytes, SHA-256 `f9af2b12b21f98a6a001b9439ae1b03e38759ede2eaa06d6800e789c30636e5f`. Both signatures, EOF and PDF parsing succeeded. GenFirst extraction warned of a font mismatch; UTF-8 surrogate normalization preserves isolated values as literal escapes. Visual checks used locally installed PyMuPDF; temporary images were removed.

BIW PDF `https://arxiv.org/pdf/1901.05534v2` returned 200/0/0 but timed out at 120 s after 2,066,816/2,761,340 bytes and, on one retry, at 180 s after 2,182,720 bytes. In contrast, the same edition's `https://arxiv.org/html/1901.05534v2` returned 200/0/0, 308,081 bytes; its actual HTML table rows were extracted and read, closing the table gap without representing a PDF download as successful.

For the language-model supplement, the paper says one is released, but its PDF has no embedded file or specific supplement link. GitHub's public repository API `https://api.github.com/search/repositories?q=2610.19113` and `https://api.github.com/search/repositories?q=%22How%20Language%20Models%20Develop%20In-Context%20Learning%22` both returned HTTP 200, `total_count=0`, `incomplete_results=false`; this does not establish global absence. Browser search attempts produced `ERR_CONNECTION_CLOSED`. No guessed private source, alternate identity, or verification bypass was used. The supplement remains not located and unread, not known to be unprovided.

No installations, foreign code, training, checkpoint evaluation, shared-table edits, subagents or commits were performed.
