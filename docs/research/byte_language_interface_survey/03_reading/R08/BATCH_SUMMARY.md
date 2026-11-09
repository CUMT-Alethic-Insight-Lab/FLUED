# R08 — Full reading handoff

**Completed:** 6 distinct newly read FULL papers / 6 assigned; 0 PARTIAL, 0 BLOCKED, 0 reused FULL. FULL denotes reading each locked paper's main methods, reported experiments and relevant available appendices, including visual inspection of crucial plots/tables where text extraction interleaved columns. It is not independent mathematical proof, executable reproduction, source-code audit, or a check that claims and original runs match.

| Card | Exact source | Main inventory backlinks | Principal boundary |
|---|---|---|---|
| [BIW-0131](BIW-0131.md) | EMNLP 2024 official PDF pp. 678–702 | [BIP-0268](../../02_inventory/DETAILED_INVENTORY.md#BIP-0268), [BIP-0269](../../02_inventory/DETAILED_INVENTORY.md#BIP-0269) | subword LMs; equal token budgets change original-text exposure; apparent discrepancy in number of 1.3B rows |
| [BIW-0049](BIW-0049.md) | ACL 2025 official PDF pp. 32155–32173 | [BIP-0074](../../02_inventory/DETAILED_INVENTORY.md#BIP-0074) | no pure-byte arm; small-to-large rank agreement depends on task; conflicting H100-hour entry |
| [BIW-0108](BIW-0108.md) | arXiv:2604.27263v2, 14 May 2026 | [BIP-0115–0120](../../02_inventory/DETAILED_INVENTORY.md#BIP-0115), [BIP-0270](../../02_inventory/DETAILED_INVENTORY.md#BIP-0270) | byte intervention; offline BPE starts and positions not proved prefix-consistent; group throughput also changes target density |
| [BIW-0035](BIW-0035.md) | arXiv:1608.05859v3, 21 Feb 2017 | [BIP-0184–0186](../../02_inventory/DETAILED_INVENTORY.md#BIP-0184) | word LM/BPE translation; tying harms word2vec skip-gram; projection interacts with dropout |
| [BIW-0036](BIW-0036.md) | arXiv:1611.01462v3, 11 Mar 2017 | [BIP-0187–0189](../../02_inventory/DETAILED_INVENTORY.md#BIP-0187) | conditional subspace argument is not equality of matrices; factorial changes parameter budget |
| [BIW-0091](BIW-0091.md) | arXiv:2001.07885v2, 24 Jan 2020 | [BIP-0194–0196](../../02_inventory/DETAILED_INVENTORY.md#BIP-0194) | word/subword translation, row-only 'cosine' retains hidden-state norm; language-direction inconsistency |

## Recurring interpretation constraints

1. Full-article availability does not close unknowns in the article. Exact original-text budget/context, EOS, seeds, compute and serving protocols are frequently unreported. A nominal isoflop design or a published model parameter count is not a measured systems cost. Where tokenizer units differ, token throughput is not raw-text throughput.
2. Head axes are distinct: BIW-0049 explicitly ties decoder input to output embedding; BIW-0035 tests that axis and an additional three-way translation axis; BIW-0036 equates word input/classifier transposes; BIW-0091 changes effective input/output vectors even if the underlying parameters are shared. BIW-0131 and BIW-0108 do not state the corresponding tying arrangement. None of the historical word/subword experiments is a controlled test for a small-byte classifier.
3. Compression is useful for context/processing efficiency but is not sufficient to predict task quality: BIW-0131's English controls and BIW-0049's task-specific cross-scale ranking both show counterexamples. Neither study estimates a causal universal hierarchy of tokenizers.
4. Where BIW-0108 says starts and repeated positions are causal, this batch does not certify that offline tokenizer prefixes are stable or that arbitrary-prefix inference can obtain the annotation. Training-only benefit and privileged-label evaluation are separate conditions.
5. The public PDF and UTF-8 text extraction for each locked source are retained in [sources/](sources/) with exact BIW filenames. Figures were rendered locally using already installed PyMuPDF; selected images were read and discarded after inspection. No third-party code executed, installs, model training, changes to shared files, uploads, commits, or code verification.
