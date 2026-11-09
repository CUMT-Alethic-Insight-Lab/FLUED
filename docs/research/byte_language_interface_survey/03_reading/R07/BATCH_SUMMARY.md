# R07 — Multilingual evidence, negative controls and character tasks

## Completion

Six assigned distinct works read; **6 fresh FULL, 0 PARTIAL, 0 BLOCKED, 0 reused FULL**. FULL means the assigned fixed source's method, key results/figures and available carrying appendix were read, not that the results, software, proofs or weights were independently verified. Cards are English; each identifies its source version, scopes evidence, and links its inventory record(s). All original PDFs and UTF-8 text extractions are retained under [sources/](sources/); the CharBench author preprint is separately version-labeled.

| Work | Card | Reading depth | Main value / unresolved issue |
|---|---|---|---|
| BIW-0104 | [MYTE](BIW-0104.md) | FULL | Morphology-resource-dependent byte code; Santali unseen-script failure; source Table 4 versus Table 8 MT aggregate conflict; decomposed-text reversibility and perplexity equation unverified. |
| BIW-0105 | [XTREME-UP](BIW-0105.md) | FULL | Benchmark is scarce-data rather than zero-shot; 88 languages not 88 byte wins; autocomplete counterexamples; paper's 39-versus-70 MT evaluation-language inconsistency. |
| BIW-0106 | [Endangered-language NMT](BIW-0106.md) | FULL | Separate one-hot bytes, multilingual transfer and costly permutation ensemble; 800-byte filter and dev-as-test; no same-encoding ensemble control. |
| BIW-0107 | [Tokenizer-training imbalance](BIW-0107.md) | FULL | Separate tokenization and NMT sampling; byte fallback eliminates UNKs yet does not reliably prevent degradation; Latin contamination and multilingual Tamil counterexample. |
| BIW-0109 | [Synthetic and natural noise](BIW-0109.md) | FULL | Character/word models, not UTF-8 byte models; natural edits differ from synthetic corruptions; mixed-noise training trades specialization for broader coverage. |
| BIW-0114 | [CharBench](BIW-0114.md) | FULL | Positional correlations are model- and task-dependent, not causal tokenizer ablations; no native byte control; author-preprint appendix caption/plot-title mismatches. |

## Boundaries and follow-up

- Both embedding tying and output-head sharing are treated as separate axes in each card; only BIW-0106 clearly identifies removal of learned input byte embeddings and a separate learned byte-output projection. Others remain unknown when not established by the assigned paper.
- For MYTE, the Unicode normalization implementation and exact reversibility to original bytes need author code/version inspection before stronger claims. Table 9 extraction interleaves cells, so visually consult the PDF for individual numbers. Its Table 8/4 MT discrepancy and XTREME-UP's Table 1/text disagreement require author clarification or a fixed-version data/experiment audit.
- CharBench's numeric parser, excluded invalid responses, answer distribution and chance/majority floors need author artifact inspection; its separately sourced v3 appendix was read, but the complete preprint/proceedings version diff was not checked. Appendix plots swap task names relative to several captions.
- No model training, reproduction, independent proof checking, dependency installation, commit, shared survey-file edit, or paid source access. No older FULL card was credited as a fresh read. Automated structural verification checks files, links and status only; it does not validate scientific claims.
