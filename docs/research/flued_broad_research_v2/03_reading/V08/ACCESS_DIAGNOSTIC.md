# V08 public-access diagnostic

Snapshot 2026-11-09. [Staging manifest](STAGING_MANIFEST.md) records version, paths, bytes, SHA-256 and reading scope. Earlier urllib direct requests failed TLS EOF; a previous normal request to each of four OpenReview PDFs returned a verification challenge. These outcomes are not a claim every possible legal route is inaccessible.

## Toolchain and security boundary

`curl 8.16.0` uses Windows Schannel; `pdftotext` and installed Python PDF rendering libraries are present; `pdftoppm`, `pdfinfo`, `mutool` were not on PATH. Normal HTTPS certificate **and revocation** verification remained enabled; no `--insecure`, `--ssl-no-revoke`, credentialed sessions, alternate identity, challenge solving or dependency installation. Files were staged only at `E:/projects/FLUED/FLUED/docs/research/flued_broad_research_v2/03_reading/V08/sources/`.

## Executed requests and outcomes

- Scratchpad `https://arxiv.org/pdf/2605.09630v2`: first curl 90 s connection timeout; one normal retry HTTP 200, 738498 bytes; 31-page parse and SHA verified. Previously v1 was FULL; this reads the genuinely updated v2 and does not add a work.
- Cross-lingual `https://arxiv.org/pdf/2609.19291v1`: first HTTP 200 timed out at 1293593/1556871 bytes; one clean full redownload HTTP 200, 1556871 bytes; 37-page parse and SHA verified.
- GlitchPatch `https://arxiv.org/pdf/2610.04399v1`: first HTTP 200 timed out at 1388916/1448746 bytes; second connection timed out; third normal retry HTTP 200, 1448746 bytes; 24-page parse and SHA verified. The incomplete prior bytes were overwritten by the complete response.
- PSR `https://web.eecs.umich.edu/~baveja/Papers/psr.pdf`: normal verified curl returned `CRYPT_E_REVOCATION_OFFLINE`, exit 35. No verification bypass. Earlier FetchURL read the full institutional manuscript text (revision unknown); institutional binary and figures have not been acquired by curl. Its [official NeurIPS 2001 proceedings abstract](https://proceedings.neurips.cc/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html) was read via FetchURL. Separately, two standard attempts to `https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf` failed connection; proceedings PDF version/equivalence is unverified.
- All four exact OpenReview PDF routes previously produced a verification challenge via ordinary public FetchURL and were not retried through another interface to get around it. The prior built-in-browser exact-title mirror searches failed connection. Each remains BLOCKED; inability to access is not proof no public copy exists.

All three acquired PDFs passed `%PDF-` and parser page-count checks, and were text-extracted in full with `pdftotext` and paginated Read. Selected plots/tables were rendered and inspected; specific pages and scientific limits are in the cards. The parser emitted embedded-font mismatch warnings, so table/plot evidence was visually cross-checked. No OpenReview body was synthesized from an abstract, and anonymous submission identities are not linked to arXiv authors. Venue status is the historical official API snapshot, not a current acceptance claim.
