# V01 — Task sufficiency and objective alignment: resumed full-reading handoff

## Counts and edition scope

Seven distinct assigned works: **6 FULL at the assigned locked edition, 1 PARTIAL at the assigned locked edition, 0 BLOCKED.** In addition, the single PARTIAL work has a separately read **FULL arXiv v2** original; this is **not an eighth work or a seventh locked-edition completion**. A01 prior work was abstract or selected-section evidence; none of these seven was a prior FULL reset. FULL means original paper and relevant substantive appendices read, with bearing tables/figures inspected; it does not mean proof checking, code review, independent numerical replication, experimental validation or acceptance of all author claims.

| Work | Assigned edition and status | Actual new source coverage and important qualification |
|---|---|---|
| [W0067](W0067.md) | **FULL**, 2610.30493v1 | 39-page PDF acquired after earlier timeout; §§1–7, proof A–E and experiment appendix F read; Figures 3–5/14–15 and Tables 1–3 key evidence recovered. |
| [BR-A01-R02](BR-A01-R02.md) | **FULL**, 2510.08907v4 | Staged 23-page PDF, methods/results/A–D; p.7 Table 5 and p.23 Table 20 visually checked. Formal ICLR 2026 paper remains a distinct, not byte-certified edition. |
| [BR-A01-R03](BR-A01-R03.md) | **FULL**, ICML 2018 formal | Official 10-page main and 11-page supplement, including bounds/proofs and main Figures 2–4, were read; main versus supplementary caption discrepancy recorded. |
| [BR-A01-R04](BR-A01-R04.md) | **PARTIAL**, CVPR 2022 formal | Formal body/supplement previously read as extracted text; formal bearing tables did not extract and direct verified PDF acquisition failed revocation lookup. Separately, arXiv 2203.07004v2 **FULL**, pp.1–14 including main tables/figures and A–D; no cross-edition table equivalence asserted. |
| [W0037](W0037.md) | **FULL**, 2305.14788v2 | PDF §§1–7/A–F and main Tables 1–5 recovered; decoder adaptation, growing state, cost and negative comparisons retained. |
| [W0055](W0055.md) | **FULL**, 2405.13792v2 | PDF §§1–7/A–H and Tables 1–4, 9–11; bearing performance, training and costs recovered; formal NeurIPS version remains separate. |
| [BR-A01-R08](BR-A01-R08.md) | **FULL**, 2602.03784v4 PDF | Staged pp.1–27, substantive §§1–7/A.1–A.9 including proof and load-bearing tables; PDF/HTML figure numbering and code-status discrepancy are retained. Venue/acceptance remains unverified. |

The word **v2** above is either an explicitly stated arXiv edition or this broad-research revision as context; never count versions as separate scientific works. Existing selected readings are provenance, not fresh FULL credit. All task-direction mapping, controls and recommended discriminators remain in the cards.

## Acquisition and verification receipt

First consulted [ACCESS_DIAGNOSTIC](../../05_review/ACCESS_DIAGNOSTIC.md) and [staging manifest](../_source_staging/access_recovery_20261109/manifest.json); reused its two existing R02/R08 originals, not duplicate downloads. Existing Git Bash curl/Schannel used normal verified HTTPS with `--location --fail --proto '=https' --proto-redir '=https'`, bounded timeouts and explicit absolute paths under V01. Successful six local PDFs reported HTTP 200, TLS result 0 and `proxy_used=0`; signatures, EOF and parseability checked, then SHA-256 recorded in their cards. W0067 succeeded on its first request in this continuation despite the earlier diagnostic timeouts. W0037 first had a connection timeout then succeeded on its one retry. No system proxy settings or certificate verification were modified.

The formal CVF main and supplement URLs each produced curl exit 35 `CRYPT_E_REVOCATION_OFFLINE`, HTTP 000: certificate revocation service unavailable. Neither TLS nor revocation was relaxed; the normally public arXiv-v2 alternative succeeded and was labeled separately. Earlier official CVF body and supplement text had been read via FetchURL, but its tables were not available there. This is a version-specific access/visualization gap, not evidence CVF is unavailable to everyone or the editions differ. No login, challenge, 403, anonymity linkage, package installation, source code execution, training, shared-table editing, or commit.

The staged PDF texts were read with pagination. New PDFs were parsed with existing PyMuPDF; AutoCompressors emitted a MuPDF color-space warning when extracting/rendering, so its bearing tables were verified visually on rendered PDF pages. Extracted text files in `sources/` are reading aids, not independent originals; PDF checksums and exact source URLs take precedence. Temporary rendered PNG page views were used only to read the figures and then removed. Two prior R02/R08 staging hashes remain as recorded in the shared read-only manifest.

## What changed scientifically

- **SAC has a concrete architecture-dependent counterexample:** at 15×, its in-domain / out-of-domain F1 is 54.95/39.26 for LM-only, versus 51.73/37.23 for AE+LM; 500x's objective ablation changes sign by metric/rate. QMSum mixed 15.32 exceeds LM-only 14.95, while GovReport reverses. Exposure and KV/bidirectional contracts still differ from other architectures.
- **W0067's fixed-pretext guarantee is bounded and task-aware:** newly recovered Appendix F Table 1 shows a reference threshold, but states fitted components violate its exact isotropy conditions; it is not an empirical certificate. Nominal MI, binary budget, estimated entropy and probe risk remain distinct. dSprites' role swap supports the designed frequency/precision contrast but does not establish generality.
- **A clean ELBO is not equal reconstruction:** Broken ELBO's main Figure 4d visually shows near-equal ELBO with different reconstructions; its supplemental caption says zero semantic encoders among twelve β=1 models while the main caption says one. No independent recount was made.
- **Native consumption is not an inferred latent capacity:** xRAG's Table 3 shows benefits of its host-specific bridge training, with one no-pretraining WebQA improvement despite lower four-task average. AutoCompressor's Table 5 exposes a real quality–throughput tradeoff against top-10 full-passage REPLUG, alongside large offline state.
- **ComprExIT's PDF theorem is only an upper bound:** Appendix A.7 applies a Wasserstein triangle inequality under finite first moments; it does not prove mismatch grows or that exact fact bindings survive. The PDF's windowed Sinkhorn, task-tuned readers, uneven effective compression and incomplete full-cost matching limit attribution.
- **Contrastive-view evidence has a source boundary:** arXiv v2 Table 1 shows VGGFlower transfer 42.81→54.16 with reconstruction while source CIFAR10 is essentially unchanged; Table 4 supplies negative transfers. View-private task information may matter, but extra input information also retains noise, and table numbers must remain v2-scoped until formal alignment is checked.

## Remaining follow-up

1. If a normally verified CVF route becomes available, visually inspect formal main Tables 1–4 and compare its supplement to arXiv v2 before upgrading the **assigned formal edition**; do not bypass revocation or silently assign preprint cells to proceedings.
2. Reconcile ComprExIT's PDF/abstract code-status wording and current release only if relevant, without associating an anonymous forum or inferring an acceptance decision. Use fixed-PDF figure numbers.
3. Proposed experiments in cards—matched-bit objective factorials, true/wrong/constant content swaps, same-state native versus stronger reader, and equal-opportunity adaptation—were **not run or authorized**. These sources support bounded broad synthesis, not selection of a single memory or retrieval architecture.
