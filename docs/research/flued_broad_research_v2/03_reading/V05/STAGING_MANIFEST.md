# V05 public original staging manifest

2026-11-09. Staging directory: `E:/projects/FLUED/FLUED/docs/research/flued_broad_research_v2/03_reading/V05/sources/`. Ordinary `curl --fail --location` to the exact URLs below returned HTTP 200, and each response passed `%PDF-` signature checking and `pdftotext -layout`. Same-basename `.txt` files are extracted layout text. No version matching is inferred from a different repository. A SHA-256 describes bytes acquired, not a publisher signature. W0533 first timed out at 75 s after a partial response; a normal longer-timeout retry succeeded. See [diagnostic](ACCESS_DIAGNOSTIC.md).

| Locked source | URL | PDF bytes | SHA-256 |
|---|---|---:|---|
| `2309.16042v2.pdf` | https://arxiv.org/pdf/2309.16042v2 | 1332169 | `8ba9f928e321ad2f319bf0ac62ae582d8a70befbe88d0f85773302d64252d396` |
| `2606.27510v1.pdf` | https://arxiv.org/pdf/2606.27510v1 | 610276 | `a1d2764732ffb1aa7fea8d1d574864e8a0c7fa64f5d48ac9305747275bccc339` |
| `2407.08734v1.pdf` | https://arxiv.org/pdf/2407.08734v1 | 1362210 | `11c6989fe5c4d62d813e9d5f9838c57524dee4186448049437b49df1510e0a71` |
| `asiaee26d.pdf` | https://raw.githubusercontent.com/mlresearch/v337/main/assets/asiaee26d/asiaee26d.pdf | 804544 | `1b5076d1ae2ca301c08ae07a3f70eba2525c06f6457691152562e738d7a24213` |
| `2307.15771v1.pdf` | https://arxiv.org/pdf/2307.15771v1 | 2799263 | `1992c30a6ac485b61f689487d35b70ad39ce1f6b7a38979b4ac67164423f2091` |
| `2308.14272v1.pdf` | https://arxiv.org/pdf/2308.14272v1 | 1032545 | `3b8f4213dddd2a68a9de577077f195e7b7edfc92408ced7c3a7f4f610845f3df` |
| `2402.17700v2.pdf` | https://arxiv.org/pdf/2402.17700v2 | 2864571 | `ecfa8751460cba075141f791f5e0e67ae82a9fff26e2115bf5e2820f898ce57d` |

Text was regenerated with `pdftotext -enc UTF-8 -layout` and normalized to valid UTF-8. All except Hydra have zero decoding replacement characters; `2307.15771v1.txt` has 6,090 replacement characters concentrated in mathematical glyphs, so do not use it alone for formulas. The `*_pN.png` files are selective page renderings made locally with existing PyMuPDF; N is PDF page number, not necessarily printed page number. These renderings are supporting reading artifacts, not independent scientific verification.
