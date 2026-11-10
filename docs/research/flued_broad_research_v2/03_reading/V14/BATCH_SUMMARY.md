# V14 — batch reading and source receipts

## Actual work counts

Seven assigned canonical works, seven cards: **6 FULL, 1 PARTIAL, 0 BLOCKED bodies**. FULL means original body and relevant available carrying appendices/readout evidence read, not independent proof, reproduction, code execution, complete visual digitization, or validation of every claimed mechanism. BIW-0100 has a fully read five-page body but remains PARTIAL because its separately linked preregistration and detailed deviation/run artifacts could not be obtained. **Seven distinct works, not eight:** W0367=BIW-0038, W0386=BIW-0040, W0387=BIW-0041. No previous FULL card is newly counted. MoCE v1 is one work and v2 is metadata-only, not another read. No ICLR 2027 acceptance is implied.

| Canonical work | Outcome | Exact edition / receipt | Main synthesis restriction |
|---|---|---|---|
| [W0367](W0367.md) | FULL | 2602.04556v2, 15 pp. | Orthonormal-column PIT requires V≥d; frozen Z default; scratch and 590M reversals. |
| [BIW-0092](BIW-0092.md) | FULL | 2410.01131v1, 21 pp. | nGPT bundles normalization, architecture, optimizer and scales; token speed ≠ wall-clock speed. |
| [BIW-0093](BIW-0093.md) | FULL | 1711.03953v3, 18 pp. | Rank theorem is for output distributions; text8 negative does not exonerate all byte models or memory. |
| [BIW-0100](BIW-0100.md) | PARTIAL | 2608.28151v1, 5 pp.; external preregistration/run ledger unavailable | Multi-cap is worse in clean specialist comparisons, more robust under specified corruption; same-cap slicing vs cross-cap throughput differ. |
| [W0386](W0386.md) | FULL | Formal D18-1531, 6 pp., plus separate one-page author supplement | Chinese character generative segmentation, transductive raw test data; supervised/rule variants not fully unsupervised. |
| [W0387](W0387.md) | FULL | Formal 2022.sigmorphon-1.5, 12 pp. | Bidirectional span conditioning ≠ causal streaming; English reversal and gold-selection distinction. |
| [BIW-0069](BIW-0069.md) | FULL | 2411.01474v1, 18 pp.; official history reports v2 | Byte→byte translation, not proven byte→nonbyte; OPUS and low-resource reversals; encoder-only contextualization. |

## Source and access provenance

All seven exact paper PDFs were downloaded into [sources/](sources/) using existing Git Bash curl with ordinary Schannel verification, HTTPS-only redirects, no proxy/trust/certificate/OS changes. Successful receipts were HTTP 200, curl exit 0, TLS verification result 0, proxy_used 0; signatures, trailing EOF, parser exit, first-page identity/version and individual SHA-256 values checked. BIW-0100's first connection timed out; one normal retry succeeded. `pdftotext -layout -enc UTF-8` produced full text files. Its BIW-0100 font warning and W0386 escaped math/surrogate bytes were not silently used as exact symbols; carrying tables and formulas were checked against PDF where needed. Saved rendered page images cover BIW-0100 pp.2–4, BIW-0069 pp.6,7,16, BIW-0093 pp.7,8,16, W0387 p.7. Numeric curves were not independently digitized.

W0386's separately linked author appendix [PDF](sources/W0386_appendix.pdf) was obtained from `https://api.github.com/repos/Edward-Sun/SLM/contents/Appendix.pdf?ref=master`, HTTP 200, verified TLS, Git blob `5729da99e893c4ec4462f635f42262ad815356ad`, SHA-256 `909b4152f6d6b2e00f126cd30c3b1782891a5d7940043a0e31d635e2ea687826`. The ordinary raw GitHub URL reset twice, not a denied/authentication endpoint; contents API is a public original path and was not a challenge bypass. Mutable repository edition is not independently dated to publication.

BIW-0100 preregistration and per-run artifacts: `https://api.github.com/repos/unseen1980/captok/contents/` returned HTTP 404 over verified HTTPS. No full original protocol/amendment history is claimed. Its paper does report the stop rule, post-stop additions and single-seed sensitivities; those statements are attributed to the paper rather than certified by a missing ledger. Built-in browser attempts to ordinary GitHub/arXiv landing pages failed with `ERR_CONNECTION_CLOSED`; ordinary verified Git Bash acquisition and metadata succeeded. MoCE official arXiv landing/history was saved separately; source PDF v1 is not silently replaced by v2.

## Cross-axis handoff

- **Interface geometry is not the same as state capability:** PIT imposes hidden-space inverse consistency under a restrictive dimension assumption; nGPT's normalized output is part of a full recipe, and softmax rank is an output distribution constraint. None demonstrates that long-range content is absent from state or used by a deployed reader.
- **Negative and positive controls both matter:** PIT from-scratch regressions, character MoS parity, shared-cap clean regression/typo robustness, English segmentation reversal and OPUS translation reversal constrain broad claims. Small-byte alphabets do not automatically prove all head variants equivalent or eliminate memory problems.
- **Four units cannot be conflated:** MoCE's byte system has byte input, byte-position internal contextualization, byte output and translated-text supervision; the separate subword baseline is not an automatically mixed byte-input/non-byte-output model. Character segmenters use different visibility and gold-selection permissions.
- **Independent non-revisit options remain viable:** fixed/learned causal local encoding without source recall, training/objective scheduling, head-only calibration or higher-capacity heads, state reform and causal native-readout tests; no single paper chooses the architecture. Explicitly match raw bytes, context, total compute, decoding, trainable tensors and supervision before causal attribution.
- This lane does not report RAM doses. If cited elsewhere, R1's correction is **nominal 500M; the displayed doses sum to 500.040M**, not exactly 500.000M.

## Verification and remaining gaps

Seven cards, their local references and source identities were checked; PDF integrity/hash/parse receipts are recorded above and in cards. Original-table row association was resolved visually for the indicated pages rather than trusting misaligned extraction. Scientific source code was not executed; no training, installed software, shared registry edit, commit or source deletion was performed. The preregistration ledger, MoCE v2 comparison, complete FLOP/exposure accounting and byte-native causal/retention trials remain open. Project software tests are not applicable to these documentation/source-reading deliverables.
