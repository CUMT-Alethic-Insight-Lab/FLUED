# R09 — Batch summary

Five distinct assigned works; **5 scoped FULL, 0 PARTIAL, 0 BLOCKED**. These are new readings of the five reserved identities, not additional credits for versions, appendices or prior scoped FULLs. FULL means substantive source reading, not code execution, proof certification, visual recertification of every qualitative figure, or completion of unreported fields. The Transformer-XL ACL formal PDF does not include the cited appendix; the carrying Appendix A–C was read from separately labeled arXiv v3 HTML, without asserting complete source identity. The source cards explicitly label these and other scope boundaries.

| Work | Card | Central semantic records | Main carrying evidence |
|---|---|---|---|
| BIW-0064 | [Deep causal attention](BIW-0064.md) | 0095–0099, 0265 | Tables 1–5: full byte resolution and independent auxiliary ablations, 512-window uncached scoring, cleaned text8 versus raw-byte enwik8 |
| BIW-0071 | [Large byte Transformer](BIW-0071.md) | 0142–0143 | Tables 1–3: 836M, 23.0 lm1b PPL, UNK-preprocessed corpus, exact word/byte event-count conversion, stride-1 test versus stride-256 development |
| BIW-0118 | [Sparse Transformer](BIW-0118.md) | 0236–0237 | §7.2 Tables 1–3: fixed 0.99, dense 1.00, strided 1.13 BPB; system implementation and published Time/Iter with no stated unit |
| BIW-0119 | [Transformer-XL](BIW-0119.md) | 0238 | Formal §§3–4/Tables 2,6–9; v3 Appendix A–C: stop-gradient memory, relative positions, byte versus word contexts, single-GPU uncached-baseline comparison |
| BIW-0078 | [Score-function boundary policy](BIW-0078.md) | 0164–0165 | §§2–4, Appendix A/D and Tables 1–3: expected conditional objective, biased discounting, actual rates, correct-answer BPB and a bounded causal concern for BPE guidance |

## Findings for integration

1. Three genuine full-resolution alternatives to learned grouping are demonstrated: dense byte self-attention with auxiliary training, fixed sparse edges supported by specialized kernels, and segment-recurrent attention with a per-layer cache. Their likelihoods, token units, context lengths, model parameters and cost conditions differ; no common quality/cost frontier is established.
2. The numerical byte-to-word conversion requires matching scored events and corpus counts. Neither a cleaned LM1B corpus with UNK nor a canonical-token-path score automatically represents a raw-text marginal. Keep text8 restricted characters, enwik8 bytes, and word-level RECL distinct.
3. Child et al. Table 2 reports **Time/Iter** without a stated time unit, and does not provide generation/serving latency. Avoid inferring seconds. Transformer-XL's 1,874× result compares per-token evaluation with an uncached, from-scratch-window baseline on one GPU; it is not a general serving speedup.
4. The REINFORCE paper's ideal score-function identity concerns an expected conditional objective; actual γ=.99 discount intentionally biases credit assignment. Its BPE-guided offline labels are shifted by one byte. A generic ranked-merge counterexample in the card shows why the asserted removal of all future lookahead requires actual-tokenizer prefix stability; it does **not** prove a leak in the published experiment. Correct-answer BPB is not downstream accuracy.
5. Audit-derived disciplines applied: do not confuse dynamic **weight** evaluation with recurrent-state persistence; distinguish conditional and marginal output events, input/output from other sharing axes, source conflict from omission, and training activation memory from cached serving. Other R1 card corrections are outside this batch's ownership and were not edited here.

## Source access and residual boundaries

All five locked PDFs were obtained publicly within this directory, with UTF-8 text extracts retained in [sources](sources/). The first arXiv fetch timed out once before succeeding. The first additional Transformer-XL arXiv-v3 PDF request timed out; the bounded retry succeeded, and the PDF and UTF-8 extract are retained. The formal PDF and arXiv appendix are distinguished rather than silently merged. Browser pagination covered Appendix C, and the complete v3 Appendix A–E text was then read from the extract; illustrative plots were not independently measured. The PDF conversion reported a font mismatch warning for one source; versioned HTML separately resolved the two interleaved numeric tables quoted in cards 0071 and 0078.

Unreported after source reading: general EOS/invalid-byte handling, several model weight-tying/actual cache implementations, comparable all-system FLOPs and serving latency. Unverified: actual BPE-guide prefix stability and code/runtime behavior. These are not claims of failure and do not, by themselves, require repeating an already completed source reading. No training, installs, third-party code, uploads, shared inventory edits, commits or subagents were used.
