# V09 batch summary — public recent originals

## Accounting and source scope

**Eight distinct assigned works, eight source-edition cards: 7 FULL, 1 PARTIAL, 0 body-BLOCKED.** Seven are newly acquired public arXiv v1 PDFs; W0086's arXiv v3 PDF is reused from the independent R2 audit and newly read here, not acquired twice. V19's public body was read, but its separately mentioned construction supplement is not in the manuscript PDF or identifiable in the official arXiv source-archive file listing; it remains PARTIAL. No anonymous OpenReview body was acquired or reattempted. All anonymous venue associations below are separately audited **ICLR 2027 conference submissions**, not established acceptances; title association is not proof that the separately accessible manuscript editions match. No author identities were linked into anonymous venue records.

| Canonical ID | Source edition | Reading | Key boundary |
|---|---|---|---|
| [BR-A03-D20](BR-A03-D20.md) | 2609.33093v1 | FULL | donor output mediation is not query-formation intervention; failed prose competence gate |
| [BR-A02-N05](BR-A02-N05.md) | 2610.26834v1 | FULL | scalar pair recognition vs vector recall; i.i.d. fixed-step norm theorem |
| [BR-A02-N03](BR-A02-N03.md) | 2609.36529v1 | FULL | two-query tensor is E× recurrent state, not free capacity or an explicit relation |
| [W0086](W0086.md) | 2602.04852v3 | FULL | v3 is a newly read edition, same work as differently titled v1, not an additional work |
| [BR-A08-V23](BR-A08-V23.md) | 2610.39418v1 | FULL | production low-bit prefill, not a long-horizon low-bit retention test |
| [BR-A08-V18](BR-A08-V18.md) | 2610.02070v1 | FULL | union exposure/actual retrieval indicator tension; oracle pool; query utility is not a retention policy |
| [BR-A08-V19](BR-A08-V19.md) | 2608.30198v1 | PARTIAL | missing dataset-construction supplement; successful-injection selection and oracle repair |
| [BR-A08-V17](BR-A08-V17.md) | 2607.17674v1 | FULL | adapted decoder can still see prompt/prefix; fidelity metric measures valid traces, not full distribution equality |

The V18 source itself presents an important qualification to its broad design claim: an assigned-exposure count is fixed, but union with deterministic retrieval means the actual retrieval indicator can be one even without assignment, and a high-ranked item may lack an exclusion arm (App. H.1). The card records this source-level tension rather than silently declaring the estimator or all empirical results invalid. V19's main body has no embedded supplementary construction section. The exact public [source archive](sources/2608.30198v1.eprint) contains a single manuscript TeX, bibliographic/style files and four figure PDFs; no standalone supplemental item is identified by the archive listing. A Desktop browser navigation to the arXiv abstract failed `ERR_CONNECTION_CLOSED`; this does not establish that the supplement cannot be found elsewhere.

## Acquisition and evidence receipts

Normal Git Bash curl 8.16.0/Schannel, unchanged system settings, HTTPS-only redirects, normal certificate and revocation verification: seven exact-version `https://arxiv.org/pdf/<id>v1` requests returned HTTP 200, curl exit 0, TLS verification result 0, proxy used 0. Three initial connection timeouts (2610.02070, 2608.30198, 2607.17674) each succeeded on one ordinary retry. W0086 v3 was read from R2's separately verified saved bytes. All eight PDF signatures and final EOF markers checked; parser was existing `pdftotext -layout -enc UTF-8`, exit 0. Xpdf gave font warnings on some files; 2609.33093 extraction required UTF-8 surrogate normalization, with isolated units escaped rather than invented. Text is navigational, not a proof of formatting correctness. Triadic Table 1 and Kronecker Table 1 were visually inspected via existing PyMuPDF rendering and ReadMediaFile; other claims are constrained to readable original text, captions and tables. Figures were not universally digitized. No experiments, training, installs, source execution, authentication bypass, certificate relaxation, shared edits or commits.

| Exact local PDF | Bytes | SHA-256 |
|---|---:|---|
| [2609.33093v1](sources/2609.33093v1.pdf) | 684283 | `ac98f014c0835aeef04e3f65cfd5a83132f7f1b4c9a3e08053bd9abe8ab2e4b4` |
| [2610.26834v1](sources/2610.26834v1.pdf) | 838945 | `9edee9d16aa4e922540c82c3c17c74204b71c2326800a2209dc4dba3683e7516` |
| [2609.36529v1](sources/2609.36529v1.pdf) | 1376522 | `5c2a9c30d59cfe4e66cdd0905534eb06ea33dbd5c796d6567e57d6e7abfb9400` |
| [2602.04852v3, R2-owned](../../05_review/source_staging/W0086__2602.04852v3.pdf) | 1545609 | `66573f7ea8d8e515ae222165858cdc8d50abbf789e9b95a3842700dc25681159` |
| [2610.39418v1](sources/2610.39418v1.pdf) | 644809 | `9f88e2e8f1bcb7f9152933a344804e22382d8e610ecee0e1d185543d59f9e0b2` |
| [2610.02070v1](sources/2610.02070v1.pdf) | 612262 | `5b298624c26d5b2091fba07b2bbe48b0652feb5e2aadd70b4a74f0276c8fe282` |
| [2608.30198v1](sources/2608.30198v1.pdf) | 535182 | `234dce1909d7ffdf7a31844e3252fd973d768bedc1c46eea8729a6e994587bc8` |
| [2607.17674v1](sources/2607.17674v1.pdf) | 2186489 | `bdaa0e78cea7ab77940ddee3389d28306198ab23b8d9c2457e74de79e22d1254` |

## Synthesis handoff and unresolved work

These readings cover independently useful non-retrieval options: change recurrent writes, shape or prune state, adapt query/readout, change the learning objective, or improve quantization; explicit source retrieval and hybrid attention are additional alternatives rather than the report's scope. Comparisons are task, model, precision and budget specific; do not infer universal recurrent-memory blindness, byte-interface exoneration, equal FLOPs from equal tokens, or architectural selection readiness. V18 randomized exposure must be evaluated with actual arm support and candidate-selection cost; V19 requires its exact supplement to finish construction, evaluator and repair-cost auditing. Forum/preprint body equivalence, current venue decisions, independent code and theorem verification remain unestablished. The separate RAM audit correction, if discussed elsewhere, is nominal 500M with the displayed row doses summing to **500.040M**, not exact 500.000M.
