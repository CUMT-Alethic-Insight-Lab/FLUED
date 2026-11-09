# R01 — Selected-paper reading batch summary

## Accounting and source log

Six distinct assigned works; **6 new FULL, 0 PARTIAL, 0 BLOCKED**, 0 reused old FULL cards. `FULL` means the fixed source was read through method, experiments, relevant appendices and key visual evidence for this language-interface task; it does not assert independent experimental or implementation verification. No new inventory/BIP IDs were allocated and no shared inventory was modified.

| Work | Card | Locked public source/version | Scope and notes |
|---|---|---|---|
| BIW-0004 | [CANINE](BIW-0004.md) | [2103.06874v4](https://arxiv.org/pdf/2103.06874v4) | Entire 18-page PDF, Appendix A, Table 2 visual; codepoints, not bytes. |
| BIW-0005 | [Charformer](BIW-0005.md) | [2106.12672v3](https://arxiv.org/pdf/2106.12672v3) | Entire 20-page PDF including §7 appendix and score plot; v2→v3 exhaustive comparison remains unverified. |
| BIW-0006 | [MANTa](BIW-0006.md) | [2212.07284v1](https://arxiv.org/pdf/2212.07284v1) | Entire 12-page PDF, Appendices A–D, visual robustness and segmentation. |
| BIW-0066 | [CharacterBERT](BIW-0066.md) | [2010.10392v3](https://arxiv.org/pdf/2010.10392v3) | Entire 13-page PDF including Appendix A visual numerical results; UTF-8 within pre-segmented words. |
| BIW-0068 | [Embeddingless NMT](BIW-0068.md) | [NAACL 2021 pp.181–186](https://aclanthology.org/2021.naacl-main.17.pdf) | Entire six-page paper; Tables 1–4 visually checked; no appendix. |
| BIW-0117 | [Perceiver IO](BIW-0117.md) | [2107.14795v3](https://arxiv.org/pdf/2107.14795v3) | Entire 29-page PDF, Appendix F language emphasis, visual Table 1 and Figure 7. Non-language supplementary demonstration video not viewed. |

All six direct public URLs succeeded on first download; no wall, mirror substitution, or version substitution. Local fixed PDFs, UTF-8 `pdftotext -layout` extracts, and selected original-page renders are in [`sources/`](sources/). Initial extraction used an incompatible default encoding and was regenerated with `-enc UTF-8`; the Perceiver PDF produced malformed-number warnings, but relevant tables and language text were recovered and checked as noted. No browser control, installations, training, paid services, third-party source execution, commits, or shared-file writes.

## High-value corrections for the central inventory

- CANINE v4 Table 2: +2.8 F1 is CANINE-S on SELECTP; abstract +5.7 is CANINE-C+n-grams on MINSPAN. The prose also contains inconsistent +3.8/+6.9 claims for that n-gram arm; Table 2 and Appendix Table 7 give +4.9/+5.7. See [BIW-0004](BIW-0004.md).
- Charformer softly mixes local candidates then performs fixed downsampling; its appendix's simplified illustrative code excludes the nominal upper bound 4, unlike the conceptual method and Figure 3. Training code/config needs separate verification. Baseline 81.4 vs byte T5 81.5 GLUE is not a universal win. See [BIW-0005](BIW-0005.md).
- MANTa's learned soft byte-block assignment is capped to L/4, a hard bottleneck: no-truncation degeneration is reported qualitatively. DEV-only synthetic noise does not show a broad separation; adaptation is important. Its training speed is not byte-generation latency. See [BIW-0006](BIW-0006.md).
- CharacterBERT inputs are UTF-8 within externally segmented word tokens, with capped local length and a closed top-100k word MLM head. ClinicalSTS reverses the favorable medical comparison; Figure 7's y-axis is accuracy despite prose calling its ~5-point difference F1. See [BIW-0066](BIW-0066.md).
- Embeddingless NMT's apparent 19/20 advantage before explicit token-dropout control does not survive as a general result: fixed one-hot dropout itself drops whole target input tokens and xx→English reverses on average after control. Paper's `softmax_d` leaves unused-coordinate/special-token handling unresolved. See [BIW-0068](BIW-0068.md).
- Perceiver IO is bidirectional masked reconstruction, not autoregressive byte generation. Byte BERT 20M vs Perceiver 201M is near FLOP-matched, not parameter-matched; language experiment hardware is not specified in the language sections. ImageNet's weight sharing cannot be extrapolated to language. See [BIW-0117](BIW-0117.md).

## Outstanding questions

Exact input/output tying for most reported runs, checkpoint aliases and code behavior, normalization/EOS/invalid-output handling where absent, exact raw-text alignment, comprehensive FLOP accounting and inference/serving budgets remain unknown as indicated in each card. No independent proof, code execution, model weights, external validation or additional language/video supplement inspection was attempted. Central inventory owner should decide the follow-up and integrate the explicit BIP links; the batch does not claim to resolve the wider survey's coverage.
