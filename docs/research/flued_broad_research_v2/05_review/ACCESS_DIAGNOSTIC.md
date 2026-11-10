# Public-original access diagnostic and staging

Date: 2026-11-09. Acquisition recovery only; **no new FULL readings, card changes, scientific verification, or registry updates**.

## Result

**12 representative priority works attempted across V01/V02/V04/V05/V07/V08; 10 PDF originals staged, with 10 derived text files.** Total PDF bytes: 19,015,457. Two sources remain unstaged for specific failures below. This is a bounded recovery batch, not an attempt to download all approximately 50 assignments.

- Staging directory: `../03_reading/_source_staging/access_recovery_20261109/`.
- Machine-readable inventory: [manifest.json](../03_reading/_source_staging/access_recovery_20261109/manifest.json). Each successful entry records work ID, locked edition, exact requested/effective URL, PDF SHA-256, project-relative PDF/text paths, byte count, retrieval timestamp, HTTP/TLS/proxy receipt, text hash, parser exit, and first-page title-substring check. Previous failed timeout attempts are retained.
- All 10 successful downloads: HTTP 200, curl exit 0, `ssl_verify_result=0`, `proxy_used=0`, PDF signature and final EOF marker present, existing `pdftotext` exit 0, expected title phrase found on the first extracted page. Hashes were recomputed from saved bytes.
- Text extraction and title checks establish usable acquisition, not complete reading, visual inspection, proof correctness, or equality between different editions. PDF binaries were not altered.

## What was checked before recovery

Read all six requested `BATCH_SUMMARY.md` files and representative cards in their respective V01/V02/V04/V05/V07/V08 directories. They repeatedly recorded standard-library Python `SSL: UNEXPECTED_EOF_WHILE_READING`, built-in-browser `ERR_CONNECTION_CLOSED`, incomplete FetchURL extraction, and no saved PDFs. V05 BR-A04-N12 and V07 BR-A06-X04 also recorded a distinct HTTP 404 for guessed proceedings-shaped PDF paths. Those guessed paths were not reused.

FetchURL was used for the official PMLR pages for W0199, BR-A04-N12, and BR-A06-X04. They confirmed the formal records and actual linked PDF URLs. For the latter two, the official URLs are the public `raw.githubusercontent.com/mlresearch/...` assets, not the 404 proceedings-shaped paths. No third-party code was executed from those repositories.

### Independent control requests

Ordinary public controls, tested before staging:

- arXiv: `https://arxiv.org/pdf/1411.1792v1`.
- PMLR: `https://proceedings.mlr.press/v139/schlag21a/schlag21a.pdf`.

| Client / request setup | arXiv control | PMLR control |
|---|---|---|
| Existing Git Bash curl 8.16.0, Schannel, unchanged defaults | HTTP 200, 492,537 bytes, TLS verification result 0 | HTTP 200, 1,326,478 bytes, TLS verification result 0 |
| Python 3.14.0, OpenSSL 3.0.18, ordinary `urllib.request.urlopen` | TLS unexpected EOF | TLS unexpected EOF |
| Same Python/OpenSSL, per-opener `ProxyHandler({})`, otherwise default verified HTTPS | HTTP 200, `%PDF-1.5` prefix | HTTP 200, `%PDF-1.5` prefix |

An additional curl PMLR control explicitly reported `proxy_used=0`, HTTP 200, TLS verification result 0, and the same byte count. Python's automatically discovered proxy mapping had `http`, `https`, and `ftp` keys, all with `http` URL scheme. Only the keys and schemes were printed; no proxy endpoint, user information, credentials, or secret file was inspected. Python's default SSL context reported 81 X.509 certificates, including 62 CA certificates.

**Diagnosis:** the previous Python failure is reproducibly associated with its automatically selected proxy path, not a universal public-PDF outage, a demonstrated missing-CA error, or a 403 response. The same Python TLS runtime and default certificate validation succeed on normal direct requests. Existing curl uses the working direct route and Windows Schannel trust. The exact failing proxy component, its configuration provenance, and the browser's internal route were not inspected; do not claim they were diagnosed. The browser was not repaired or retested in this recovery.

## Actionable standard route

Use the existing Git Bash curl (the tested executable is Git's `mingw64/bin/curl.exe`) without changing proxy settings, trust stores, or certificate checks. In this shell its normal defaults produced `proxy_used=0`.

Example, from the project root, targeting a new explicit filename within the authorized staging directory:

```bash
curl --location --fail --silent --show-error \
  --proto '=https' --proto-redir '=https' \
  --connect-timeout 15 --max-time 120 \
  --output 'docs/research/flued_broad_research_v2/03_reading/_source_staging/access_recovery_20261109/NEW_WORK__EXACT_EDITION.pdf.part' \
  --write-out 'http=%{http_code} tls=%{ssl_verify_result} proxy=%{proxy_used} url=%{url_effective}\n' \
  'https://PUBLIC_HOST/EXACT_VERSION.pdf'
```

The example is a template, not an existing source URL. Confirm curl exit 0, HTTP 200, successful TLS verification, `%PDF-` signature, final `%%EOF`, and successful parsing before renaming the partial to `.pdf`; then compute SHA-256. Do not overwrite the staged originals. Do not treat `ssl_verify_result=0` alone as success: the revocation-failed request below also emitted that field but had a nonzero curl exit and HTTP 000.

No `-k`, certificate-validation override, revocation relaxation, alternate identity/IP, system setting change, new CA bundle, or installation was used. Python's direct-opener control was process-local, not a system proxy change; staging consistently used curl. There was no access denial or challenge on the successful requests.

## Staged originals and exact file inventory

Every stem below has both a `.pdf` and a `.txt` file under `03_reading/_source_staging/access_recovery_20261109/`. The only other staging file is `manifest.json`. Exact URLs and full hashes are in that manifest.

| Work ID | Source edition | Filename stem | PDF page breaks reported by text parser |
|---|---|---|---:|
| BR-A01-R02 | arXiv 2510.08907v4 | `BR-A01-R02__2510.08907v4` | 23 |
| BR-A01-R08 | arXiv 2602.03784v4 | `BR-A01-R08__2602.03784v4` | 27 |
| W0199 | Formal ICML 2021, PMLR 139 | `W0199__pmlr-v139-schlag21a` | 12 |
| W0202 | arXiv 2605.22791v1 | `W0202__2605.22791v1` | 21 |
| BR-A03-D19 | arXiv 2603.04427v3 | `BR-A03-D19__2603.04427v3` | 17 |
| W0533 | arXiv 2309.16042v2 | `W0533__2309.16042v2` | 27 |
| BR-A04-N12 | Formal UAI 2026, PMLR 337 | `BR-A04-N12__pmlr-v337-asiaee26d` | 18 |
| BR-A06-X04 | Formal ICML 2025, PMLR 267 | `BR-A06-X04__pmlr-v267-smith25a` | 27 |
| BR-N06-07 | arXiv 2410.10254v3 | `BR-N06-07__2410.10254v3` | 58 |
| BIW-0076 | arXiv 2605.09630v2 | `BIW-0076__2605.09630v2` | 31 |

These cover objective alignment, recurrent updates, native addressing, causal-intervention measurement, host repair/transfer, and byte interfaces. W0199 is the formal PDF, not a claim to have acquired arXiv v3 or a separate supplement. D19 is v3, not the selectively discussed v4. Scratchpad is the requested v2. PMLR formal paths are not immutable revision IDs, and `main` asset URLs can change; SHA-256 locks the actual received bytes. An arXiv suffix pins the requested edition, without independently certifying all server-side version history.

Bounded acquisition observation for BR-A01-R08: the saved first page reads **“Fix the Structural Bottleneck: Context Compression via Explicit Information Transmission”**, includes the `2602.03784v4` date line, and says code is available. This gives a concrete PDF for the previously flagged discrepancy; it does **not** resolve the abstract/HTML relationship, compare complete editions, or associate any anonymous submission with public author identities. Existing card uncertainty is intentionally unchanged.

### Derived text limitations

The already installed Xpdf `pdftotext` is version 4.00. Its `-layout -enc UTF-8` output for BR-A01-R02, BR-A01-R08, and W0202 contained UTF-8-encoded surrogate code units rather than strict UTF-8 for some mathematical characters. Valid surrogate pairs were combined into Unicode. Isolated units were retained as visible backslash-u hex escapes (14 for R02; 0 for R08; 240 for W0202), not silently replaced with guessed formulas. The manifest records raw extraction hashes, normalization, escape counts, and final text hashes. All final `.txt` files decode strictly as UTF-8. Consult the unchanged PDFs for mathematical notation.

BIW-0076's parser returned exit 0 but warned `Mismatch between font type and embedded font file`; that warning remains in the manifest. Derived text is a convenience, not a substitute for visual tables, figures, and formula inspection.

## Remaining precise blockers and stop rule

| Work | Exact URL | Observed failure / disposition |
|---|---|---|
| W0067 | `https://arxiv.org/pdf/2610.30493v1` | Initial request: HTTP 200, TLS verified, but 55-second transfer timeout after 16,384 of 917,467 advertised bytes. One bounded retry with 120-second total limit then failed at the 15-second connection timeout. No PDF retained; source availability was not disproved. |
| BR-A08-R07 | `https://web.eecs.umich.edu/~baveja/Papers/psr.pdf` | curl exit 35, HTTP 000: Schannel `CRYPT_E_REVOCATION_OFFLINE (0x80092013)`; certificate revocation checking could not reach its revocation service. No relaxation, bypass, or repeated attempts. Manuscript revision remains unknown. |

Four initial arXiv transfers had HTTP 200 but incomplete transfers at the initial 55-second limit. They received at most one ordinary longer retry each, never an authentication workaround: R08, W0533, and LoLCATs then succeeded; W0067 did not. Failed partial files were removed, and no incomplete PDF was given a successful hash claim. Stop here rather than claiming all sources recovered or endlessly retrying. Future authorized recovery can retry W0067 under a healthy normal connection or seek an exact-version public original; R07 needs an ordinarily trusted, revocation-checkable institutional or official proceedings route. No such alternate was asserted verified here.

OpenReview verification-wall cases were not retried or bypassed. No anonymous-author lookup, identity linkage, login, public-API author harvesting, or acceptance inference was performed. The recovery batch intentionally prioritizes normally downloadable public originals.

## Verification and scope boundary

- Recomputed all 20 PDF/text SHA-256 values; checked all 10 first-page expected-title phrases and parser exits; strict UTF-8 validation passed after the explicitly recorded normalization.
- Verified exactly 21 staging files (10 PDFs, 10 texts, one manifest), with no `.part` leftovers. This diagnostic is the only authored file outside that owned staging directory.
- Inspected staged first-page extracts for acquisition checks only. No full reading, table transcription, proof checking, execution of source code, experiment, or software-test claim is made. Project software tests/builds are not applicable to public-source staging.
- No existing cards, batch summaries, catalog, shared registries, production code, checkpoints, system configuration, package installation, subagents, or commits were changed. Other preexisting untracked project files were left alone.
