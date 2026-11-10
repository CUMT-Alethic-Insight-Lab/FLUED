# V07 — Host transfer, companions and budgeted repair

## Counts and edition scope

Eight canonical tasks: **7 FULL paper readings; 0 PARTIAL; 1 BLOCKED body**. FULL means the declared edition's main paper and relevant appendices were read, not that code, experiments or proofs were independently reproduced or verified. Some figure trends are taken from captions/prose rather than digitized curves; this is stated in the affected cards. Previously recorded A06/A08 selections were PARTIAL or metadata-only, so none is double-counted as an earlier FULL. v1 material is not relabeled v2; source edition and venue are distinct.

| Canonical work | Actual locked edition and disposition |
|---|---|
| [BR-N06-12](BR-N06-12.md) | FULL 2607.07706v1 pp.1–22 including A–D; theory not independently proved |
| [BR-N06-07](BR-N06-07.md) | FULL 2410.10254v3 pp.1–58 including A–E; ICLR 2025 association separate |
| [BR-N06-04](BR-N06-04.md) | FULL 2603.12433v3 including supplementary A–B; CVPR formal edition selectively compared, not equivalent/redlined in full |
| [BR-N06-10](BR-N06-10.md) | FULL 2610.11214v1 pp.1–27 including A–B; Tables 4 and 12 visually checked |
| [BR-N06-08](BR-N06-08.md) | FULL 2408.10189v2 pp.1–23 including A–C; v1→v2 exhaustive redline not done |
| [BR-N06-01](BR-N06-01.md) | FULL 1411.1792v1 main/supplement; experimental replication not done |
| [BR-A06-X04](BR-A06-X04.md) | FULL formal ICML 2025 PMLR paper pp.1–27 including A–G |
| [BR-A08-V13](BR-A08-V13.md) | BLOCKED: anonymous official ICLR 2027 active submission at prior audited snapshot; note v2, PDF revision unknown, not accepted |

## Decision-bearing conclusions

- **Different interventions matter.** Yosinski BnB resets and retrains upper layers; it is not intact replay. Mai self-stitch inserts the same trainable connector at the same site, but the exact initial random seed match is unspecified and extra supervision/teacher cost matters. Smith shows that trained stitching can map different cues and even label-coded random clusters; compatibility is not proof of common semantic content. Smith's train/test noise share class prototypes, while their individual noise samples differ; fresh unseen prototypes/classes were not established.
- **Companions change apparent rankings.** Key to Going Linear's strict frozen-QKV Llama GLA/GDN LAMBADA is 28.26/44.67 (Table 1), but 68.70/69.01 with short convolution (Table 3 and Appendix B.3). LoRA uses a smaller rate. A 64-token cache is an additional retained channel, and equal tuning/FLOPs are not established.
- **Teacher-fed fit is not natural-chain recovery.** LoLCATs and MOHAWK use teacher-fed internal matches before assembled student continuation. LoLCATs Table 2 compares four epochs of one stage against two plus two, not equal-dose factorial coefficients. Its 8K passkey score is 0% after Alpaca-only migration versus 100% after training on passkey-formatted examples; 10K-context extrapolation remains a failure (B.5.2). MOHAWK Table 3's 5B-token stage comparisons do not equalize per-stage compute or original teacher pretraining; its same-architecture Phi→Phi resets attention.
- **RAM's stage and metric distinction is now quantified.** On Qwen2.5-1.5B at 500M tokens, complete versus full-only migration gives PPL 16.33 vs 16.82 and Avg 68.1 vs 66.6; removing the head stage gives PPL 16.31 but Avg 66.9. At 56.4M, full-only exceeds staged recovery in both PPL and Avg; at 154.7M staged Avg is higher despite slightly worse PPL. Appendix Table 12 shows these are different stage objectives/parameter permissions. The 500M-token ledger is not an equal-FLOP/teacher-compute control.
- These papers do not diagnose the target host or select an architecture. Original directions across state, objectives, interface, native use and source-enabled alternatives remain in scope.

## Acquisition receipt and remaining gaps

Read `05_review/ACCESS_DIAGNOSTIC.md` and staging `manifest.json`; used staged exact-edition PDF/text for Smith and LoLCATs, without modifying the shared staging area. Downloaded five remaining arXiv PDFs in `V07/sources/` by ordinary Git Bash curl with HTTPS/TLS checks, no certificate/system/login changes; verified signatures/EOF, `pdftotext` and SHA-256 (per-card values). Initial two connection timeouts recovered by one normal retry. RAM download timed out twice with HTTP 200; a normal HTTP range continuation returned 206, and the complete PDF passed signature/EOF/parser checks. Rendered and checked PDF pp.9/26 with installed PyMuPDF; the screenshots are retained in `sources/`. Key and MOHAWK text normalization combined surrogate pairs and preserved isolated symbols as visible escapes; Key has eight isolated escapes, MOHAWK zero. No external code was executed.

OpenReview submission body remains blocked as documented by the independent audit; no challenge retry, login, author linkage or acceptance inference. Its unresolved paper-specific methods and controls remain in its card. The Mai formal-edition comparison is selected, not an exhaustive equivalence comparison; do not equate old v1 and v3 claims. Remaining substantive work is empirical/proof verification only when explicitly authorized, plus access to the anonymous body if it becomes normally public. No training, package installation, subagents, commit or shared-table edits.
