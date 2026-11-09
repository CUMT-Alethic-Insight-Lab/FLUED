# R04 batch summary — probability events and speculative sampling

Six assigned works, **6 fresh FULL readings**, 0 reused FULL, 0 partial, 0 blocked against their *locked source versions*. FULL refers to source reading, not independent proof/code/weight verification. Existing discovery records were used as reading questions, not counted as fresh reads. All files, sources and temporary conversion/rendering work were kept within this batch directory; no experiments, training, installs, commits or shared files.

| Work | Card | Status | Primary BIP links | Main scope or unresolved qualification |
|---|---|---|---|---|
| Marginal likelihood, Cao & Rimell 2021 | [BIW-0080](BIW-0080.md) | FULL | 0109, 0272, 0273 | Completed-document path sum; word-denominated PPL; EOS/normalization and consistency-restricted support unspecified. |
| Exact byte-level probabilities, Phan et al. 2025 | [BIW-0088](BIW-0088.md) | FULL | 0111, 0182, 0278 | v2 published-paper header checked; independent OpenReview PDF bytewise comparison unverified due to verification wall; unmasked noncanonical mass is essential. |
| Understanding and Mitigating Tokenization Bias, Phan et al. 2024 | [BIW-0132](BIW-0132.md) | FULL | 0274, 0275 | Generic character alphabet; MPE and BPE methods; canonical zero-mass assumption and mask/renormalize effects. |
| Causal Estimation of Tokenisation Bias, Lesci et al. 2025 | [BIW-0133](BIW-0133.md) | FULL | 0276, 0277 | Local regression discontinuity under continuity/functional-form assumptions; near-cutoff counts and numeric CIs unreported. |
| Speculative Decoding, Leviathan et al. 2023 | [BIW-0083](BIW-0083.md) | FULL | 0110 | Exact target distribution in ideal arithmetic, not same pseudorandom trajectory; T5 result is not byte latency. |
| Speculative Sampling, Chen et al. 2023 | [BIW-0084](BIW-0084.md) | FULL | 0110 | Independent work; distributed Chinchilla, separately trained 4B draft, finite numerics. |

## Cross-card distinctions for inventory maintainers

1. **Different events:** BIW-0080 sums model probabilities of alternative tokenizations of a completed document, subject to proposal/support and termination assumptions. BIW-0132 and BIW-0088 condition on a raw-prefix cylinder and use tokenizer-induced canonical support. BIW-0133 estimates a local counterfactual vocabulary-membership effect, not either prefix-event conversion. Do not merge all three into “tokenization bias” without defining the estimand.
2. **Exactness is conditional:** deterministic tokenizer-induced distributions exclude invalid tokenizations; a raw softmax token LM can assign them positive mass. Masking/renormalization changes its distribution even when canonical-token likelihood improves. Arbitrary tokenizer normalization, token symbols, EOS and pretokenization need explicit compatibility checks.
3. **Claims and negatives:** In BIW-0088, 84.3−66.5 = 17.8 percentage points pass@10 is SPM byte vs unhealed token baseline, not a gain over healing; HumanEval 42.1−38.4 = 3.7 points compares ensemble against the best single *token* score. GSM8K ensemble underperforms its stronger member. BIW-0133's 2.88 nats is a local regression estimate and not a per-item effect.
4. **Two independent speculative-sampling works share the exact target-law mechanism, not experimental evidence:** BIW-0083 uses existing T5 checkpoints on one TPU-v4; BIW-0084 trains a shallow draft for a distributed 16-TPU-v4 70B deployment. No result is a byte-serving benchmark. Their p/q symbols are reversed.
5. **Missing budgets/axes:** Cards explicitly identify unreported training exposure, FLOPs, latency/memory, sample counts, and sharing axes. Do not infer shared embeddings, multi-byte heads, or equal training costs from architecture names.

## Retrieval and verification

The six locked public PDFs were downloaded with `curl` to explicit `R04/sources/BIW-<id>.pdf` paths, then `pdftotext -enc UTF-8 -layout` to matching text files. Texts were read through continuation pages, including all relevant appendices. The extractor emitted invalid mathematical glyphs for several PDFs; affected crucial algorithm/proof pages and key tables/figures were rendered from the original PDF with the locally installed PyMuPDF and visually checked. Remaining extraction artifacts do not imply source/code verification; consult the linked original PDFs and exact locators in cards. Source v1 history for BIW-0084 and v2 history for BIW-0088 were checked on arXiv; the ICLR2025 label occurs in the latter's PDF header. An OpenReview verification page was encountered when attempting an independent formal-version check; it was not bypassed. No claim of formal-PDF bit identity is made.
