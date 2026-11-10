# V03 batch summary — reachable memory, optimization and precision

## Disposition

Seven distinct assigned work records, seven fixed-edition original PDFs read, **7 FULL / 0 PARTIAL / 0 BLOCKED**. All seven cards include source version, limitations, original locations, key controls, prior-direction coordinates and proposed—not authorized—discriminators. This update reads the local originals' decision-bearing figures, tables, formulas and relevant appendices visually in addition to the previously read bodies. FULL means paper-reading coverage, not exhaustive pixel-by-pixel digitization, independent proof checking, code inspection or replication. Missing paper disclosures remain gaps, not invented facts.

| Canonical card | Edition | Progress and boundary |
|---|---|---|
| [W0088](W0088.md) | 2508.19029v2 | FULL v2: main and Appendix A plus key figures/tables; exact full LR grid and copy metric remain unspecified in the paper. |
| [W0213](W0213.md) | 2610.19709v1 | FULL v1: main, Appendix A, prompt and Figures 2–6; exact graph coordinates not digitized. |
| [BR-A02-P03](BR-A02-P03.md) | 2609.16183v1 | FULL v1: main, Tables 1–7, Figures 1–2 and Apps.A–C; same-version source conflicts retained. |
| [BR-A02-N01](BR-A02-N01.md) | 2609.38166v1 | FULL v1: main, Tables 1–6, key plots and derivations, Apps.A–E. |
| [BR-A02-N04](BR-A02-N04.md) | 2611.07552v1 | FULL v1: main, Figures 2–4, tables, proof text and App.B; generator/calibration description remains incomplete. |
| [W0226](W0226.md) | 2605.31163v5 | FULL v5: main and Apps.A–G, figures, key equations and proof text; prior v1 abstract is **not** v5 coverage. |
| [W0234](W0234.md) | 2501.00663v1 | FULL v1: main, Apps.A–C, key figures and formulas visually checked; theorem is stated without proof in this edition. |

**Reuse accounting:** zero existing FULL cards reused as fresh work; the earlier A02/A08 selected-section/abstract records were used as routing and explicitly extended in cards. No extra work counted for revisions. Edition accounting is **five v1, one v2, one v5** (seven works); no v1→v2 comparison was performed. A source PDF's receipt and text extraction do not by themselves meet FULL. No new 2027 acceptance, forum equivalence, author identity linkage, theorem certification, experimental replication or model training is claimed.

## Material conclusions and counterexamples

1. Finite capacity, training reachability, input visibility and reader ability are different claims. W0088's careful retuning and BR-A02-P03's curricula materially alter toy recall, but neither eliminates finite-bit limits nor establishes arbitrary query-last semantic retention. P03's bidirectional and causal streams have different visibility and no established advantage in the stated collision controls.
2. W0213's two-way target-digit gate patching is direct intervention evidence in pretrained Mamba, yet oracle positions/target flags expose privileged information. Query-first relevance across model **depth** is not a solution for unknown future query in **time**.
3. LeapQuant's rounding frequency and high-precision buffered records matter at fixed state shape; SPARE's calibrated subspace and compensated writes affect function, with dense degradation and uniform-rank NLL counterexamples. Neither recurrent-state-only MiB nor 8-bit payload is whole-model serving memory. SPARE's exactness requires all keys within the calibration basis.
4. W0226's uncertainty covariance changes write geometry at an extra state and compute cost; it has successful controlled high-overlap recall, but teacher distillation and next-token continuation are not equal-objective/compute comparisons. Its v5 Table7 values show held-out PPL ~2.8–3.8% worse than continued GDN depending on corpus/context, rather than inheriting the handoff's 2.5–2.7% assertion.
5. Titans' nonlinear fast network is a real alternative family, not merely retrieval: online regression, momentum and decay operate alongside optional local attention/persistent parameters and also target forecasting and DNA. Its single-needle, language and ablations do not establish exact unknown-query memory independent of other paths.
6. P03 same-v1 §4.2's p=.86 contradicts §10's repeated old −.32 decay claim; longer-length training in §§6–7 and directional parity constrain stale §§9–10 prose. W0088 and P03 use different tasks and cells, so their different convolution outcomes must be tested under matched conditions, not casually labeled errors.

## Gaps and next action

The original PDF does not fully enumerate W0088's per-configuration LR grid or define the copy accuracy aggregation; these remain reporting/artifact gaps. SPARE's calibration corpus and 4-choice generator details remain unreported in the paper. Titans v1 states Theorem 4.1 without a proof; absence of a supplied proof does not mean it is false. Its Appendix C Eq.32 uses M_t on the right where main Eq.13 uses M_{t−1}; §3.2 Eq.16's per-step vs chunk-boundary gradient notation also needs clarification rather than an invented correction. For any claim of learned exact-memory use, paper reading alone is not enough: a target-host study must separate retained bits, rounding frequency, distractor writes, local paths, reader permissions, legal query timing and counterfactual content. No code, proof correctness or experiment was independently verified or run.

## Source acquisition receipt

All downloads are public arXiv PDFs in this batch's `sources/` directory, named by ID and version; SHA-256 hashes are recorded in each card. `curl -L --fail` downloaded explicit version URLs, `pdftotext -enc UTF-8 -layout` created matching local text. Browser navigation returned `ERR_CONNECTION_CLOSED`; FetchURL supplied several HTML bodies but not W0226's PDF route, while direct public PDF retrieval succeeded. Titans initially timed out after a partial transfer; ordinary HTTP range resume completed the file. Its extracted text required replacement decoding; in this local follow-up its decision-bearing formulas were read directly from rendered PDF pages. No auth or challenge was bypassed. This follow-up made no network request: already installed PyMuPDF rendered selected local PDF pages, inspected using ReadMediaFile; individual cards give the coverage. Temporary page images were removed after inspection. Local source files are evidence inputs, not independent confirmation of author experiments. Text-only Windows PDF extraction produced some font warnings.
