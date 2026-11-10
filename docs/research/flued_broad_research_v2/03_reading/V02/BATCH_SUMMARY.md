# V02 batch summary — recovery and original reading

## Actual coverage

Eight distinct assigned works: **7 FULL, 0 PARTIAL, 1 BLOCKED**. FULL denotes reading the specified original paper, including decision-bearing tables, relevant derivations and appendices, not independent verification, experiment replication or a code audit. No previous FULL card was reused; prior A02 selected GDN and EDA passages were extended, not separately counted. Papers read at source v1 are not v1→v2 source updates. W0242 is new source-v4 reading; its authors state all experiments are from v1, but we did not independently diff every change or reuse a v1 FULL card. W0199's 12-page formal proceedings paper is read alongside its 16-page arXiv v3; A–F appendix references are to v3, not an asserted identical formal supplement.

| Work | Edition and actual reading | Principal residual question |
|---|---|---|
| [W0199](W0199.md) | ICML 2021 formal pp.1–12 plus arXiv v3 pp.1–16 including A–F | Nonorthogonal-key collateral versus the Appendix B orthogonal-key ideal; FAVOR+ NaN negative |
| [W0201](W0201.md) | arXiv v3 pp.1–22, A–B, main tables and S.1/S.2, figures | Retention/filtering mechanisms and total live state, not demonstrated frozen-host transfer |
| [W0202](W0202.md) | arXiv v1 pp.1–21, A–E, Tables 1–5 and Fig.2 | Separate gate strengths versus projection/decay/compute, all live bytes |
| [W0203](W0203.md) | arXiv v1 pp.1–12, A–C, Tables 1–8 and Fig.3 | Value-side mechanism versus second update/extra compute; 340M task and selector reversals |
| [BR-A02-P04](BR-A02-P04.md) | arXiv v1 pp.1–14, A–B, Tables 1–5 and Fig.2 | First/latest truth and collateral retention; worse raw old-key recall |
| [BR-A02-P01](BR-A02-P01.md) | arXiv v1 pp.1–26, A–C and Prop.3.2, Tables 2–5 and figures | Model-size nomenclature discrepancy; loss/retention/fast bits not factorial matched |
| [W0242](W0242.md) | arXiv v4 pp.1–33, A–C and main/appendix figures | Matched physical fast bits and old-fact causal use, not just perplexity |
| [BR-A08-V04](BR-A08-V04.md) | Official anonymous note metadata/abstract only | **BLOCKED** original body; PDF revision and current official state unknown |

## Acquisition and integrity

Read [access diagnostic](../../05_review/ACCESS_DIAGNOSTIC.md) and [staging manifest](../_source_staging/access_recovery_20261109/manifest.json) before use. W0199 formal and W0202 v1 are pre-existing staged originals. Six exact-version arXiv PDFs (W0199 v3 plus the five remaining public works) were obtained with ordinary Git Bash `curl`, unchanged proxy/trust settings and HTTPS verification, explicit absolute paths in this batch. Four first attempts timed out at connection; a single ordinary retry per affected source succeeded. The other two succeeded on first attempt. Every accepted response reported curl exit 0, HTTP 200, TLS verification 0, proxy_used 0, PDF signature/EOF, nonempty page tree and successful `pdftotext`; exact URLs, byte lengths, SHA-256 and parsed page counts are in [manifest](sources/manifest.json) and [W0199 receipt](sources/W0199__2102.11174v3.receipt.json). Derived text normalizes malformed UTF-8 surrogate sequences; original PDFs remain authoritative. No system proxy, CA, credential, authentication or wall setting was changed. Rendered key pages were read for ambiguous tables and plotted results; no numerical data was invented from abstract-only material.

SDG's official PDF had prior challenge/inaccessibility: no repeat, bypass, identity inference or acceptance inference. The inherited active ICLR 2027 submission metadata is a snapshot; note version 2 is not PDF version 2. An accessible body and a fresh official state check remain necessary.

## Decision-bearing results and limits

- W0199 Appendix B protects a separate **orthogonal** key during rebinding; it does not establish that correlated old facts are unaffected. Repeated-key truth is latest binding, not first. In v3 Appendix D.2, FAVOR+ plus delta yielded NaNs; increased feature width did not improve the cited LM setup.
- W0201 Table 2 contrasts 8K repeated-passkey retention (DeltaNet 98.8, GDN 91.8, Mamba2 30.4) against 4K essay-number (18.6, 92.2, 56.2). This supports task-dependent tradeoffs, not isolated causal semantic filtering. Hybrid order and local convolution materially affect outcomes.
- W0202 separates channel strengths while retaining a write-key factor; EDA adds a separately projected erase address; Dual DeltaNet adds a value-side read. They are not equivalent operations. W0203's 340M 4096-token essay-number score falls to 14.4 versus KDA 40.6 despite higher aggregate NIAH; its learned selector also loses to ungated selector on 340M real retrieval. Extra compute and widths remain alternative explanations.
- EDA's aggregate RULER is higher but 128K score 44.22 trails GDN 45.16. KDA wins its raw old-key recall probe. Erase replay is local readout perturbation, not identified deletion of obsolete facts. Every recurrent EDA comparison includes full-attention layers.
- MIRAS Table 2 contains individual losses despite broad prose claims; Table 5 model-size labels differ from main text. Its block approximation evaluates gradients at the prior boundary. TTT's b=16 mini-batch and dual form have a speed/quality tradeoff; nonlinear MLP underperforms at short matched FLOPs and has higher wall-clock. Longer-context PPL is not old-fact causal use.

**Follow-up, not an experiment authorization:** cross update rule, rates, decay, projections and inner steps under matched *total* live bytes/precision, local and attention paths, compute and tuning. Separately vary write load, elapsed no-write time, key/value similarity and first/latest truth; measure new and older target outcomes and final-answer content dependence. This informs broad research and does not choose an architecture.

## Verification

PDF hashes/integrity and exact version strings were checked at acquisition, substantive extracted texts were read through their continuations, and key pages were visually inspected against extraction. `FULL` is source-reading coverage only. No training, package installation, foreign code, shared table edit, system setting change or commit was performed. Unread official SDG is explicitly retained as BLOCKED.
