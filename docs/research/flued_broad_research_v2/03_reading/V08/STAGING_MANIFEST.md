# V08 staging manifest

Staging root: `E:/projects/FLUED/FLUED/docs/research/flued_broad_research_v2/03_reading/V08/sources/`. All three downloaded PDFs were fetched with ordinary verified TLS, begin `%PDF-`, and open completely in the existing PDF library. SHA-256 is of acquired bytes. Extracted text uses `pdftotext -enc UTF-8 -layout`; font mismatch warnings mean diagrams and important cells were visually checked as rendered pages. No code, checkpoints, model execution, or installations.

| Work and edition/source URL | Local PDF; bytes; SHA-256 | Outcome |
|---|---|---|
| BIW-0076 [arXiv 2605.09630v2](https://arxiv.org/pdf/2605.09630v2), 2026-11-06 | `sources/BIW-0076-arxiv-v2.pdf`; 738498; `e693ea212bc2211224ea4debb10aa709534d4c09a0c3915e4cd91f86de95cea1` | 31 pages; full PDF text, Figures 1–15, Tables 1–4; existing v1 FULL reused separately |
| BR-A07-N07 [arXiv 2609.19291v1](https://arxiv.org/pdf/2609.19291v1), 2026-09-16 | `sources/BR-A07-N07-arxiv-v1.pdf`; 1556871; `e52f078836467408cbda58571a3faf2328522c71552f361d15127e4ebe8eeb3c` | 37 pages; full PDF text; main and appendix figures and central tables visually checked |
| BR-A07-N09 [arXiv 2610.04399v1](https://arxiv.org/pdf/2610.04399v1), 2026-10-03 | `sources/BR-A07-N09-arxiv-v1.pdf`; 1448746; `67114b602b839d186e27b142d348e089c48dc11be9ad4d46fb143bb2fbfb576a` | 24 pages; full PDF text, all seven figures and key tables visually checked |
| BR-A08-R07 [institutional manuscript](https://web.eecs.umich.edu/~baveja/Papers/psr.pdf), 2001, revision unknown | No local PDF | Schannel `CRYPT_E_REVOCATION_OFFLINE`; did not disable verification. Previous FetchURL extracted full institutional text, not a local download. |
| BR-A08-R07 [NeurIPS 2001 proceedings route](https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf) | No local PDF | Two normal connection attempts failed; separately identified edition and byte equivalence not established. Proceedings abstract page read via FetchURL. |
| BR-A08-V02 [official PDF](https://openreview.net/pdf/9c64cd9b8b1bba44c1ff65945bd6c1a02ed98a9d.pdf) | None | Prior normal request returned challenge; no bypass, body blocked |
| BR-A08-V22 [official PDF](https://openreview.net/pdf/4b049a14ede5c22389997afeb1b72a99e81a7de5.pdf) | None | Prior normal request returned challenge; no bypass, body blocked |
| BR-A08-V25 [official PDF](https://openreview.net/pdf/3df135438f55aa7adaea9da322f21607da69a080.pdf) | None | Prior normal request returned challenge; no bypass, body blocked |
| BR-A08-V14 [official PDF](https://openreview.net/pdf/b167a621df8f120088cda7baa7cccfcbfd226cd7.pdf) | None | Prior normal request returned challenge; no bypass, body blocked |

Each acquired PDF has a matching `*.txt` layout extraction. Selected `*-p<N>.png` files are page renderings made with the installed PDF library solely for figure/table reading; N is the one-based PDF page. These derivative images and texts do not add works or independent experiments. OpenReview note v2 is metadata revision, not arXiv v2 or a known PDF edition.
