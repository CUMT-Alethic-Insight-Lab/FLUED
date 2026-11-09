# R06 — Byteification and pretrained-interface transfer: reading handoff

## Completion and source ledger

Six distinct frozen-manifest works were newly read; **6 FULL, 0 PARTIAL, 0 BLOCKED, 0 previously read FULL reused**. FULL means the locked paper's methods, principal experiments, key numerical/visual evidence, and relevant author-provided appendices were read. It does not mean that proofs, released code, checkpoints, runtime tensor aliases, or experiments were independently verified. All six versioned public arXiv PDFs were downloaded directly, without a fallback or access-wall bypass, to `sources/BIW-xxxx.pdf`, then converted by the installed `pdftotext -enc UTF-8 -layout` to matching `.txt` files. Rendering used installed PyMuPDF; images were temporary. 0103's conversion emitted font/graphics warnings; relevant graphs, conversion diagram and pseudocode were visually examined. PDF page/section/table and visual-scope specifics are in each card.

| Work / card | Locked PDF | Scope and principal inventory links |
|---|---|---|
| [BIW-0097](BIW-0097.md), Bolmo | [2512.15586v2](https://arxiv.org/pdf/2512.15586v2) | FULL §§1–8, Appendices A–F; BIP-0206–0209 |
| [BIW-0098](BIW-0098.md), Distilling Token-Trained Models | [2602.01007v1](https://arxiv.org/pdf/2602.01007v1) | FULL §§1–8, Appendices A–E; BIP-0210–0212 |
| [BIW-0099](BIW-0099.md), Cross-Tokenizer LLM Distillation | [2604.07466v1](https://arxiv.org/pdf/2604.07466v1) | FULL §§1–6, Appendices A–C; BIP-0213–0214 |
| [BIW-0103](BIW-0103.md), Breaking the Token Ceiling | [2609.12303v1](https://arxiv.org/pdf/2609.12303v1) | FULL §§1–10, Appendices A–G; BIP-0113–0114 |
| [BIW-0126](BIW-0126.md), Zero-Shot Tokenizer Transfer | [2405.07883v2](https://arxiv.org/pdf/2405.07883v2) | FULL §§1–7, Appendices A–K; BIP-0255–0257 |
| [BIW-0122](BIW-0122.md), Char2Subword | [2010.12730v3](https://arxiv.org/pdf/2010.12730v3) | FULL §§1–6, Appendices A–B; BIP-0247–0250 |

## High-value handoffs, not endorsements

- The 0098 severe no-alignment ablation and 0097's noncatastrophic stage-2-only ablation answer different recipe-specific comparisons. The latter adds 6.5B source tokens for approximate global FLOP matching but does not match memory or schedules.
- 0099 ordinarily removes its temporary ten-position byte distillation head and serves the student tokenizer, whereas its BPE→byte experiment actually changes the deployed tokenizer. Source contradictions: §4 describes Q/V-only LoRA and a 260-class byte vocabulary; Table 4 states seven LoRA target projections and 261 classes. Runtime configuration remains unverified.
- 0103's EOT conversion exactly represents **marked** token events under its assumptions; it is not automatically the marginal conditioned on an unmarked byte prefix. Appendix F.1 pseudocode does not show the EOT input preprocessing necessary to implement the marked method; implementation behavior is unknown. The headline 4-point advantage is an extrapolated six-task average, not observed gain, and validation dataset 2 at LR 1e-3 reverses the predicted token-vs-EOT ranking. The paper reports no matched-serving-cost result.
- 0126's zero-shot target transfer uses a costly pretrained hypernetwork, and the reported >16% XLM-R speedup is calculated from length rather than directly timed. Byte-conversion preservation is measured on English pretokens, not universally.
- 0122 is a character-composer/mBERT **encoder** antecedent, not a byte generator. Hybrid mode retains the original lookup table. Contextual MLM updates the composer through a frozen host and fixed original output table; downstream freezing permissions are not stated precisely.
- Do not infer input/output embedding tying from model family: each card distinguishes known teacher/source/host and head axes from unknown actual parameter aliasing. Original teacher pretraining, storage/I/O and serving/cache budgets are often missing; cards name the gaps rather than filling them from assumptions.

## Verification boundary

Completed text extraction was paginated to the end, and selected diagrams/plots and extracted tables were examined visually. Sections and figures are cited in each card. No external packages were installed, no training or code reproduction was run, and no files outside this batch were edited. Files are research notes rather than runnable software; no project tests were run.
