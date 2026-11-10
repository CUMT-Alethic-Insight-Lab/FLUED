# V05 batch summary — intervention and deployed-use instruments

## Counts and reading scope, 2026-11-09

Seven distinct assigned works: **7 newly completed FULL paper reads, 0 PARTIAL, 0 BLOCKED**; seven locked PDFs staged. FULL here means the substantive original body, relevant appendices/proof text and claim-bearing tables/figures were read at the specified edition. It does **not** mean independent proof verification, code execution, data replication or that every decorative/redundant plot was inspected pixel by pixel. No prior FULL v1 card was promoted to v2 and no edition is counted as another work.

The exact formerly missing visual scope and its disposition are listed in [REMAINING_FIGURE_AUDIT.md](REMAINING_FIGURE_AUDIT.md); additions in the current pass are recorded on each card. Remaining source ambiguities and unperformed replications are scientific limitations, not unread-paper status.

| Canonical work | Locked edition | Actual completed original reading and key visual checks | Specific remaining evidence limitation |
|---|---|---|---|
| [W0533](W0533.md) | arXiv:2309.16042v2 | §§1–8, Apps. A–I, pp.1–27; Figs. 2–5,9–12,26–31 and Tables 1–5 | §3 49% accuracy vs App. B 49% correct-token probability; Fig.26 caption/panel corruption label mismatch. Other repetitive plots not inspected pixelwise |
| [BR-A04-R08](BR-A04-R08.md) | arXiv:2606.27510v1 | §§1–6, App. A proofs/B.1–B.3, pp.1–18; Figs. 1–4, Tables 1–3 | Path-specific language and Taylor approximation require declared graph and smoothness/locality; proof read but not independently certified |
| [BR-A04-N01](BR-A04-N01.md) | arXiv:2407.08734v1 | §§1–7, Apps. A–F, pp.1–22; Figs. 2–5,9–12 and Tables 1–4 | Exact Reverse ground-truth edge set not enumerated in card; ROC overlap is not a general learned-model proof |
| [BR-A04-N12](BR-A04-N12.md) | formal UAI 2026, PMLR v337:210–227 | §§1–6, supplement A–G including proof text; printed pp.213–214,216–217,224–225,227 key equations, Tables 1–3/5–7 and Figs. 2,5–7 | Fixed-estimand assumptions and adaptive selection remain distinct; numerical results and proofs not independently verified |
| [BR-A04-R02](BR-A04-R02.md) | arXiv:2307.15771v1 | §§1–6, App. A, pp.1–21; Figs. 1–3,5–8, direct/total and toy/compensation equations | PDF text corrupts many mathematical glyphs; cross-checked the relevant definitions with locked HTML and original page renderings; no broad semantic/host generalization |
| [BR-A04-R05](BR-A04-R05.md) | arXiv:2308.14272v1 | §§1–5, Apps. A–B, pp.1–17; Figs. 1–4 and Tables 1–6 | Table 3 gives overall case-detector accuracy, not error specifically on original inputs; appendix F1 varies in some datasets |
| [W0531](W0531.md) | arXiv:2402.17700v2 | §§1–6, limitations, Apps. A–C.2, pp.1–19; Figs. 2–4 and Tables 2,5–6 | §4.2 versus App. C layer-selection wording remains ambiguous; locked PDF table numbering differs from earlier HTML |

**Reuse.** W0050 is a separate [PARTIAL legacy input](../../../flued_multigranularity_survey_20261108/03_reading/B03/W0050.md), not one of the seven assignments or a new FULL; its external supporting-evidence PDF remains missing. W0533 and W0531 are established W aliases. Prior discovery had selected passages or abstracts only; this batch completes the original locked editions and does not claim independent replication.

## Access, provenance and visual audit

[ACCESS_DIAGNOSTIC](ACCESS_DIAGNOSTIC.md) corrects the previous overgeneralization from urllib/browser failures: normal curl with inherited network environment and TLS verification fetched all seven targets. The [staging manifest](STAGING_MANIFEST.md) records exact URLs, absolute staging path, byte lengths and SHA-256. `sources/` retains the seven PDFs and seven text extractions; `*_pN.png` are locally rendered PDF pages used in the audit. Hydra extraction contains replacement characters, so relevant equations and figures were checked against version-matched HTML and PDF images. No 403/challenge was bypassed, no proxy or TLS settings modified, and no foreign code, installations, training, shared tables, subagents or commits were used.

## Conclusions for bounded synthesis

1. A clean donor or naturally worded corruption does not certify a realistic joint patched state. W0533's p.19 Table 4 shows that S1/IO versus S2 corruption traces different information; joint windows do not localize their central layer.
2. BR-A04-R08's exact four-cell effects differ from its local mixed-Hessian approximation. Table 2's group interactions can exceed and even reverse pair effects; neither eliminates higher-order search or guarantees a natural path-specific explanation.
3. BR-A04-N01's X-Proportion toy preserves invariant position under resampling but not zeroing; restoration, complement corruption and normalization choices specify distinct estimands. Fig.12 shows node search can perform worse than edge search on the same toy.
4. BR-A04-R02's Fig.7 layer-23 r²=.92 with slope=.69 indicates variance explained versus incomplete logit compensation, not 92% recovered accuracy. Fig.8's layer-23 attention and MLP response r²=.13/.87 illustrates why a single null ablation is not a no-use certificate.
5. BR-A04-R05's Tables 1–3 quantify metric inflation and imperfect routing; original-input F1 changes in some appendix datasets, and Movies integrated-gradient sufficiency slightly decreases (−.08→−.09). These qualify, rather than erase, the concrete Goodhart counterexamples.
6. W0531's Cause–Iso and entity/context split results demonstrate supervised intervention ability, not unmodified native content use. Its verb-Entity MDAS 49.5 is below DAS 51.8, and several attributes remain entangled.
7. BR-A04-N12's anytime guarantee is for a fixed declared estimand with bounded scores, support and predictable proposals; adaptive hypothesis selection requires separate correction. Adaptive sampling is not uniformly faster than i.i.d.; the five-seed failure-exclusion medians are 118 versus 88. Clipping changes the target and cannot certify semantic fidelity.

Each card contains proposed minimal discrimination and mappings to prior directions; none authorizes training or selects an architecture. The main coverage here is deployed-use measurement (D.01–D.20), with explicit C/E/F boundary conditions; broader research need not reduce to retrieval or multigranularity.

## Follow-up

Retain the specific source-level tensions above, unavailable W0050 supplement, and raw-versus-normalized effects. Where a downstream conclusion depends on exact Reverse edges, RAVEL layer-selection implementation or original-input-specific detector confusion, obtain those artifacts or design a separate targeted test. Independent validation of proofs, code, empirical results or target-host causal claims remains outside this paper-reading assignment.
