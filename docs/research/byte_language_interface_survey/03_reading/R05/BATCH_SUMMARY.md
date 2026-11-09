# R05 — Selected-paper full-reading handoff

## Completion and provenance

Six assigned distinct works, **6 fresh FULL / 0 PARTIAL / 0 BLOCKED**; no pre-existing FULL was counted or reused. Each locked arXiv PDF was downloaded directly to this directory's [sources](sources/) using public HTTPS, extracted with installed `pdftotext -enc UTF-8 -layout`, read in full text pages with continuations, and reviewed at the substantive-method, experiment and carrying-appendix level. Selected key figures/tables were visually checked via installed PyMuPDF/Pillow, using [key-pages.jpg](sources/key-pages.jpg), without executing third-party code or installing software. Read depth means source reading, **not** implementation validation, replication, independent proof verification, or exhaustive extraction of every plotted point. The 2018 v1 paper has no appendix.

| Card | Version | New depth | Key evidence and exceptions |
|---|---|---|---|
| [BIW-0015](BIW-0015.md) | 2608.15454v2 | FULL | Learned past-only segment-aligned MBP; output-table sharing does not specify input tying. Threshold vs self vs external verification and uncached caveat distinguished. Appendix B Table 5 conflicts with adjoining acceptance prose. |
| [BIW-0079](BIW-0079.md) | 2511.11346v2 | FULL | Normalized probabilistic circuits, window/mixture output axes, speculative target preservation conditions, acceptance vs actual throughput, head costs and English/EOS filters. PDF author header differs from extracted HTML. |
| [BIW-0076](BIW-0076.md) | 2605.09630v1 | FULL | Causal transient scratchpads refresh partial patches without attending other scratchpads; encoder entropy head and no-gradient-to-encoder; FLOP-matched H-Net exception. |
| [BIW-0047](BIW-0047.md) | 2605.01188v2 | FULL | 988+320 models; global fitted parameter convention vs total FLOPs, language-specific results, tokenizer/character/byte distinctions and unreported entropy-model accounting. |
| [BIW-0082](BIW-0082.md) | 1811.03115v1 | FULL | Subword translation and pixel comparison, longest exact greedy prefix of modified p1, independent branches sharing a projection, beam distillation costs, higher accepted block can slow wall clock. |
| [BIW-0089](BIW-0089.md) | 2503.09573v3 | FULL | Subword, not byte, comparator: autoregressive block factorization + within-block masked diffusion, NELBO bounds, data-driven noise schedules and EOS/entropy stopping. |

## Cross-card implications for inventory maintainers

- Parallel emission is not one probability contract: confidence-threshold LCA, exact-greedy block verification, exact-distribution speculative sampling (under its conditional-probability assumptions), and block diffusion have distinct verifiers, training losses, temporal dependencies and output distributions. Keep [BIP-0032–0034](../../02_inventory/DETAILED_INVENTORY.md#BIP-0032), [BIP-0171–0173](../../02_inventory/DETAILED_INVENTORY.md#BIP-0171), [BIP-0177–0179](../../02_inventory/DETAILED_INVENTORY.md#BIP-0177), [BIP-0183](../../02_inventory/DETAILED_INVENTORY.md#BIP-0183) distinct.
- Shared output projection, per-offset/per-mixture projections, shared decoder trunk, input/output embedding tying and draft/verifier layer reuse are distinct axes. Unknown is not no-sharing.
- Persistent trunk cache compression is not system peak memory, update FLOPs, encoder/decoder caches, or measured end-to-end latency. Preserve the H-Net compute-matched negative, latent/subword budgeting convention and dataset/teacher/auxiliary preprocessing costs under [BIP-0105–0107](../../02_inventory/DETAILED_INVENTORY.md#BIP-0105) and [BIP-0239–0241](../../02_inventory/DETAILED_INVENTORY.md#BIP-0239).
- Source issues worth subsequent author/code checks: BIW-0015 Table 5 versus 78–84% prose; its LCA depth/algorithm indexing and KV-cache behavior; BIW-0079 actual temperature/top-p-transformed proposal conditional and EOS-enabled usage; BIW-0047 amortized entropy model and resident cost; BIW-0089 partial-block prompt conditioning. Figures without numerical source tables were not reconstructed and should be cited qualitatively.

## Scope and verification

No survey, shared inventory, plan, source code or production file was edited. All six exact-version public PDFs and UTF-8 extracts are retained under R05 only; `key-pages.jpg` is the image used for figure checks. Claims in cards identify source section/page/table, controls and unknowns. No training, code execution of paper repositories, external upload, new dependencies, commit or push. File/link/status verification recorded in final handoff; Markdown cards are research artifacts, not a test or build deliverable.
