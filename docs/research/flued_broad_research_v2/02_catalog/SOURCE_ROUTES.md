# Next-round source acquisition routes and edition separation

2026-11-09. Source-route screening, **zero new FULL reads by the catalog owner**. The browser search attempt returned `ERR_CONNECTION_CLOSED`; a bounded public WebSearch/FetchURL fallback recovered the seven public originals below. No login/challenge was solved, no anonymous-author lookup was used, and no paper download/install was performed here. Tool-managed extracted text is not a project PDF archive. Reading a title/abstract and inspecting body presence is not reading the entire returned document.

## 1. High-relevance recent public bodies

Every HTML URL below returned substantive original main/body/appendix text in this catalog continuation. Only title/abstract and presence of substantive sections were screened; no numerical result or theorem is adjudicated. PDF URLs are **normal exact-version acquisition targets**, not already saved PDFs. Version/date history beyond the fixed suffix is inherited where noted, not freshly re-audited.

| Existing conservative work cluster | Anonymous forum metadata provenance | Independently available original source edition / route | Public-body observation and version boundary | Assignment |
|---|---|---|---|---|
| BR-A03-D20 | b3lZofUyGC; official audit Q15 active note2, modified2026-10-05 UTC | [HTML2609.33093v1](https://arxiv.org/html/2609.33093v1); [PDF](https://arxiv.org/pdf/2609.33093v1) | Body returned; earlier A03 partial. Same public title supports provisional cluster only; no forum/PDF equality or author crosswalk. | V09 |
| BR-A02-N05 | 2XDUbuZOTH; A08-V03 active snapshot only, outside independent audit sample | [HTML2610.26834v1](https://arxiv.org/html/2610.26834v1); [PDF](https://arxiv.org/pdf/2610.26834v1) | Body/large appendix returned; earlier introduction only. No author identities attached to anonymous record. | V09 |
| BR-A02-N03 | vFAVe0yppt; A08-V09 active snapshot only | [HTML2609.36529v1](https://arxiv.org/html/2609.36529v1); [PDF](https://arxiv.org/pdf/2609.36529v1) | Substantive body returned; earlier abstract only. Triadic and RunningTensor remain different works. | V09 |
| BR-A08-V23 | 6egpMpGwZE; A08 official active snapshot only | [HTML2610.39418v1](https://arxiv.org/html/2610.39418v1); [PDF](https://arxiv.org/pdf/2610.39418v1) | Exact title/abstract and body substantiate a **candidate edition relation**. HTML heading omits LinQuant prefix; do not count another work or presume exact anonymous manuscript. | V09 |
| BR-A08-V18 | Gj3NCR6Hge; A08 official active snapshot only | [HTML2610.02070v1](https://arxiv.org/html/2610.02070v1); [PDF](https://arxiv.org/pdf/2610.02070v1) | Causal Memory Policy title/abstract and body returned. Estimator/self-normalization and future retention need full critical read, not a name match conclusion. | V09 |
| BR-A08-V19 | KUAlW7DbIh; A08 official active snapshot only | [HTML2608.30198v1](https://arxiv.org/html/2608.30198v1); [PDF](https://arxiv.org/pdf/2608.30198v1) | Exact title/body returned; text references supplemental construction details. Find actual supplement; main text availability does not imply complete carrying material. | V09 |
| BR-A08-V17 | edyITivJJW; A08 official active snapshot only | [HTML2607.17674v1](https://arxiv.org/html/2607.17674v1); [PDF](https://arxiv.org/pdf/2607.17674v1) | Exact title/abstract/body returned. Provisional relation only; latent-use objective/response visibility require whole-source audit. | V09 |
| W0086 / A08-V07 | 3uKKt21Vry; independent audit Q18 active note2 | [abs2602.04852v3](https://arxiv.org/abs/2602.04852v3); [PDFv3](https://arxiv.org/pdf/2602.04852v3) | v3 metadata/history independently checked in source audit, **body route not re-fetched here**. v1 title/abstract is not v3 reading. | V09 |

Public arXiv author names may appear in retrieved originals; they are deliberately not carried into anonymous forum rows. Relationships above are title/abstract/subject associations, not proof of identical bodies. The reader must attach claims to the actual received edition and compare before transporting conference-specific numbers or statements. The public preprint can satisfy its independent scientific reading task while the original OpenReview body remains unavailable.

## 2. Exact bounded discovery queries

Public queries actually sent in this continuation:

- `"Fast Weights in Fast Weights" arxiv`
- `"Linear Attention lacks Incentive" arxiv`
- `"Turnip: Tokenizers" arxiv`
- `"Causal Memory Policy" arxiv`
- `"How Linear Attention Remembers" arxiv`
- `"Kronecker Delta Rule" arxiv`
- `"Triadic Linear Attention" arxiv`
- `"LinQuant" "recurrences" arxiv`
- `"When Errors Become Memories" arxiv`
- `"Uncovering Latent Reasoning Strategies" arxiv`

No pagination or venue census. Fast Weights, Incentive and Turnip did **not** yield a verified own-preprint body; reference-list arXiv IDs and same-title workshop records were not misassigned. They remain earlier reservations/reserves, not silently replaced by new batch tasks. No third-party summary supplies scientific findings.

## 3. Standard acquisition instructions for all V09–V16 readers

Read [ACCESS_DIAGNOSTIC](../05_review/ACCESS_DIAGNOSTIC.md) first. Existing Git Bash curl was found at `/mingw64/bin/curl`; existing `pdftotext` is available. Ordinary defaults previously produced the successful direct verified route. Do not change proxy settings, trust stores, certificates, identity/IP or revocation checks. Do not use `-k` or install converters. A denial/challenge is not a timeout and must not be retried through alternate identities/endpoints to evade it.

From the project root, after the coordinator assigns a batch, use only its project-owned explicit `03_reading/Vxx/sources/<stable-id>__<edition>.pdf.part` destination:

```bash
curl --location --fail --silent --show-error \
  --proto '=https' --proto-redir '=https' \
  --connect-timeout 15 --max-time 120 \
  --output 'docs/research/flued_broad_research_v2/03_reading/Vxx/sources/EXACT_ID__EDITION.pdf.part' \
  --write-out 'http=%{http_code} tls=%{ssl_verify_result} proxy=%{proxy_used} url=%{url_effective}\n' \
  'https://PUBLIC_HOST/EXACT_VERSION.pdf'
```

This is a template, not a performed download. First inspect the official landing page when a PDF link is uncertain; do not guess proceedings-shaped paths over the actual linked `raw.githubusercontent.com/mlresearch/...` asset. At most one ordinary bounded retry for a transient timeout; prior challenge and certificate-revocation failures stay explicit. Confirm curl exit0, HTTP200 (or legitimate completed206 range continuation), successful TLS, expected title/version, PDF signature, final EOF, parser success and SHA-256 before declaring an acquisition. Preserve raw PDFs; derived text surrogate/font damage and visual evidence need separate checks. Never equate downloaded bytes or a successful HEAD request with a FULL paper read.

All older sources in V10–V16 use exact known public source/edition targets from the catalogs/discovery records. Unless marked BODY_OBSERVED above, their URLs are **registered acquisition routes, not freshly tested or acquired in this continuation**. If an old source’s carrying supplement is missing, return PARTIAL plus precise gap; do not fill it from another edition. Existing staging evidence and cards stay read-only.

## Current R2 and V17/V18 route override —2026-11-09

Earlier route/body observations above are historical screening,not current V09 full-reading forecasts. ActualV01–V16 cards are reconciled in READING_STATUS;V09 public-original sources were independently read at their declared editions,while corresponding anonymous PDF equality remains unknown. No new network/acquisition call was made by the catalog owner in this integration.

R2 now independently supports all25 A08 active metadata sources acrossR1/R2,not one uncached listing. Its6 retested anonymous original bodies still failed:normal curl certificate-revocation-service offline before HTTP,and ordinary FetchURL verification challenge are different observations. The successful W0086 arXivv3 receipt and subsequentV09 FULL do not recover its anonymous forum bytes. Do not repeat challenged routes,relax TLS/revocation,use credentials or infer missing public sources globally.

Newly registeredR2 T01–T06 PDF references in [V17](batches/V17.md) were **not individually tested inR2**. Assign their normal original-body acquisition/read obligations rather than marking them BLOCKED by analogy or removing them from recent mainline coverage. [V18](batches/V18.md) similarly selects6 still-unread high-value broad recent bodies. Exact forum/note2/status/PDF-unknown fields remain separate from acquired bytes,read scope and accepted decisions. A legitimate public preprint may be read independently with its own edition;no title/abstract association certifies manuscript equality or author identities.

The sourceR2 manifest has33 returned forums including overlaps and2 adjacent non-core screens;only6 new byte-work candidates and1 existing W0356 forum association enter the adopted core source union. The two methods named GlitchPatch remain different:local token-path substitution DbzLzs5VL7 versus head-row/shared-adapter Echoing/Rvz6kIZAcg.

## Recovery minimum-primary addition

COVERAGE_RECHECK_R2§7 independently verified public abstract/history for Closing the Learning-Planning Loop with Predictive State Representations,arXiv0912.2385v1,2009-12-12. Normal exact-source target:https://arxiv.org/pdf/0912.2385v1 ;body not acquired/read by this catalog continuation. V18 assigns learned spectral identification/exploration/conditioning/planning,not another known-dynamics PSR existence theorem. No ICLR2027 association or formal-edition equality inferred.
