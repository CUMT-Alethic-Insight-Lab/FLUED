# V04 — native addressing and returned content: batch handoff

## Counts and scope

Seven assigned distinct works; **seven scoped FULL, zero PARTIAL/BLOCKED**: [D02](BR-A03-D02.md), [D03](BR-A03-D03.md), [D04](BR-A03-D04.md), [D13 formal edition](BR-A03-D13.md), [D15](BR-A03-D15.md), [D17](BR-A03-D17.md), [D19 v3](BR-A03-D19.md). The six formerly partial works were completed in this recovery; D15's prior FULL was not reread. FULL means original paper reading at the stated edition, not independent verification of code, proofs, experiments, every plotted numeric point or replication. Thin Keys v3→v4 is a version comparison within one work, not an eighth work. D13's formal edition is not asserted byte-identical to arXiv v1. No older-survey FULL card was reused for these six: A03 discovery previously read selected sections, not FULL.

## Acquisition and limits

Recovery followed [access diagnostic](../../05_review/ACCESS_DIAGNOSTIC.md) and its staged manifest. D19 v3 was read from its previously staged PDF/text without redownloading. Normal existing curl with certificate verification fetched five other requested originals plus D19 v4 into [sources](sources/), using exact edition URLs in cards; each successful transfer reported HTTP 200, TLS verification 0, proxy_used 0, PDF signature/EOF and successful pdftotext. D02/D03/D04 required one ordinary retry after connection timeouts; D17 retried once after 120-second transfer timeout. PDF hashes are in cards. Local existing PyMuPDF rendered key pages; images are retained as named receipts in sources, with relevant pages visually read. D03 text conversion preserved two isolated Unicode surrogates as literal escapes; equations were checked against PDF. No certificate or revocation relaxation, system-proxy change, access-denial bypass, install or foreign code. D15 remained its previous HTML-based scoped FULL; its figure claims follow captions/prose rather than digitization.

The original paper texts and relevant appendices are read, but the publications do not fully specify D02 read ordering, D03 gradient label/visibility or D17/D19 positional implementations. Missing implementation details are research gaps, not unread-paper claims. D19 v4's full body was read and selected changes compared; a complete visual redline is not claimed.

## Findings that matter beyond a single candidate architecture

- **Writing, address and reading are distinct:** D02's trained fixed addresses can be used as model weights rather than episode contents; its read/write-overlap penalty, next-input prediction and annealed soft→hard curriculum are different treatments. The source's read-order/indexing remains unresolved.
- **Merging is conditional:** D03's value sum and counts exactly reproduce output after keys have been made identical; identical-key conversion itself is approximate. Its 4×2 MuSiQue merge grid supports but does not isolate a general causal K-only/V-only claim.
- **State sharing is not fewer reads:** D04 reuses one producer's KV with separate layer queries, saving persistent bytes while each layer still rereads the bank. LR tuning matters and downstream benchmarks have mixed winners.
- **Normalization differs from scale and use:** D13's largest reported ablation loss occurs without learnable temperature, and its main baseline also changes ScaleNorm/LayerNorm. Translation improvements do not establish long-delay recall.
- **Matching differs from consumption:** D15's query-dependent output gate modulates the weighted return, not the current attention logits. Head-specific gates and the 1-expert control strengthen the gating explanation but do not isolate actual use of an individual fact.
- **Head identity is not KV independence:** D17 shares a full-rank base, adds rank-limited per-head residuals and keeps per-head Q; learned operator diversity is not itself a native causal-use experiment. Its written rank/cache arithmetic and rotation handling need reconciliation before deployment conclusions.
- **Feature rank is not token count or bit precision:** D19's approximate SVD can be exactly rearranged only for its approximation, while position rotation and score margins need explicit treatment. v3 and v4 report different scope/throughput numbers and remain one work. Existing multi-head-to-GQA checkpoint uptraining contradicts an absolute no-conversion claim, but its cost is not established here.

## Follow-up priority

1. Distinguish paper-read completion from substantive open gaps: D02 state-version indexing; D03 inference gradient supervision/label permissions and count update implementation; D17 formula/cache-shape inconsistencies and RoPE handling; D19 incompatible same-table/other-table math scores and position/scale handling. D04 serving latency was not measured. Seek code or author clarification only if authorized and needed; no independent implementation check was performed.
2. Keep positive/negative controls, unknown query visibility and all resident/transient state separate. Candidate new experiments are specified per card; none were run. A fixed-bank q-only comparison, correct/wrong-value swap, per-layer writer/reader decomposition, count-correct merge factorial, and identical-opportunity adaptation answer different questions and cannot be collapsed to one architecture test.
3. Keep all 167 original direction IDs explicit; this batch particularly informs C.01–C.19 and selected B/D/E/F/R directions cited in cards. Its task domains range from translation and language-model training to dynamic episodic reasoning; none alone closes byte-native long-range semantic use or selects a host architecture.

## Reproducibility boundary

Only `03_reading/V04/` is owned and written; no shared catalog, source registry, past cards, training runs, installs, commits, or checkpoints changed. Source observations are attributed to the locked editions; no ICLR 2027 submission was treated as accepted or deanonymized. Numerical values are author-reported as quoted; source conflicts are preserved. Local Markdown/identifier checks and Git status are run as artifact validation, not as scientific verification.
