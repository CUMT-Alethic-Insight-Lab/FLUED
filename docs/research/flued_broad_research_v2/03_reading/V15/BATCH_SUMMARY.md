# V15 batch — source lifecycle and omission/fallback control

## Scope and true count

Seven assigned canonical works, seven cards. **Five exact target editions FULL** (W0112, W0144, W0435, W0438, W0450); **one exact target remains PARTIAL** (W0339 v2, missing cited supplement); **one exact target is body BLOCKED by acquisition timeout** (W0143 NeurIPS proceedings). W0143 has a **separate FULL arXiv v1 preprint reading**, not a formal-edition read or an eighth work; equivalence to the formal proceedings remains unknown. W0339 is a continuation of the old B07 PARTIAL and its v1 appendix reuse is not a new work, a v2 supplement, or a FULL completion. Thus seven unique works; six independently read original bodies/editions (five target FULL plus preprint FULL) and one target PARTIAL; do not report seven new FULL target works.

| Card | Exact assigned edition | Outcome | Material limitation |
|---|---|---|---|
| [W0112](W0112.md) | 2310.08560v2 | FULL | Gold-presence task instruction, source/call accounting missing |
| [W0143](W0143.md) | NeurIPS 2023 formal PDF | BLOCKED; separate arXiv 2306.07174v1 FULL | Formal URL timed out twice; edition comparison unresolved |
| [W0144](W0144.md) | 2203.08913v1 | FULL | Physical storage precision and comprehensive duplicate/leakage controls unclear |
| [W0435](W0435.md) | 2312.05516v3 | FULL | Model/source-version lifecycle, measured same-quality and full tail costs unresolved |
| [W0438](W0438.md) | 2407.00079v5 | FULL | Dummy-model replay, version invalidation and full system costs unresolved |
| [W0339](W0339.md) | 2607.06507v2 | PARTIAL | v2 ρ definition, thresholds/calibration and history–action–continuation/teacher ledger cited to missing supplement |
| [W0450](W0450.md) | 2403.10081v3 | FULL | Confident misses/false alarms, hard budgets and source threshold-table discrepancy |

## Findings to carry forward

- Source-backed access is a real independent baseline, but it has additional storage, index, retrieval, reader and adaptation permissions. MemGPT DMR beats lossy summaries; document QA explicitly instructs it that the answer is in the store. The paper also records premature paging stops, and does not provide a complete failure/call ledger.
- LONGMEM's frozen encoder addresses same-encoder training drift; it does not prove cross-version refresh or deletion. Memorizing Transformers shows task-specific gains and negative token outcomes, with stale cache and ANN errors; neither establishes a closed fixed-state limit. The cache, index and retained inputs must be charged.
- Pensieve and Mooncake are placement/scheduling comparators, not learned semantic-memory solutions. Persisted raw content, cold fetch/recompute, CPU/GPU/network and rejected requests belong in costs; source/version invalidation and physical erasure require distinct evidence. Mooncake's reported traces use a dummy model, so quality equality is not measured.
- DynaKRAG's one-step support-proxy ranking and separate trajectory continuation gate are not a terminal rollout utility; its four-hop MuSiQue subgroup loses to S2G-RAG. DRAGIN has observed non-wins in Table 2 and uses speculative generated tokens to detect and rewind; neither supplies calibrated no-gold omission guarantees.
- Independent non-revisit paths (write/retention reform, training objective and native query/readout adaptation) remain valid alternatives, alongside strong flat/parallel/serial source-enabled baselines already assigned in `02_catalog/CROSS_AXIS_OWNERSHIP.md`. No all-memory-blindness or byte-interface exoneration follows. The R1 RAM correction, if discussed elsewhere, is nominal 500M with displayed stages summing **500.040M**, not exact 500.000M; RAM is not a V15 work.

## Acquisition and reading receipts

Existing Git Bash curl, ordinary Schannel validation and HTTPS-only redirects; all seven downloaded arXiv PDFs returned HTTP 200, TLS result 0, proxy 0 on successful request. Initial W0339 transfer timed out after 2,012,207/2,663,830 bytes and an ordinary bounded retry succeeded. Exact W0143 formal route timed out at connect twice; no certificate bypass or challenge workaround. Every retained PDF has `%PDF-`, final `%%EOF`, successful installed `pdftotext` parse and SHA-256 in its card; originals in `sources/`. `pdftotext` emitted font mismatch warnings for W0339 and W0438. Text extraction had invalid UTF-8 surrogate encodings; derived text normalized with surrogate-aware handling, preserving isolated invalid units as visible escapes, not guessed symbols. PDFs are unchanged. Visual page renders retained under `sources/` for W0143 p.8, W0339 p.6 and W0450 pp.7/15; carrying tables were inspected. No theorem proof/experimental execution is implied by FULL.

## Remaining work

Obtain the exact proceedings version of W0143 through ordinary trusted access and compare its methods, figures, appendices and results with v1; retrieve the actual v2 DynaKRAG supplement and teacher ledger or preserve PARTIAL. For stronger deployment conclusions, measure full per-action costs, failed/rejected attempts, version/invalidation and source-change answer dependence. These are research gaps, not completed experiments. This batch does not edit shared registries, other batches, production code or earlier cards.
