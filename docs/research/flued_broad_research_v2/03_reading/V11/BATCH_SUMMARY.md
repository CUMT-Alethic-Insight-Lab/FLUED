# V11 — native state and addressing: batch reading summary

## Counts and reading boundary

**Seven assigned original works, seven target editions acquired and read: 7 FULL / 0 PARTIAL / 0 BLOCKED.** FULL denotes the original paper body and decision-bearing appendices/proof steps and tables were read, not independent mathematical proof, source-code execution or experiment replication. The cited external UCI per-dataset CSV for W0240 was not acquired; its per-dataset cells are not carried. Not all illustrative/qualitative figures were inspected at pixel level. No supplements beyond those actually in the PDFs are represented as acquired. The seven are seven distinct works, not seven additional papers plus old versions. Older W0199/W0201 and W0088 results are referenced only as prior existing work, not reread or newly counted; the GQA formal EMNLP edition supersedes a prior partial arXiv-v3 reading for this target and is one work, not an extra independent study. Formal/proceedings equality is not assumed for separately versioned arXiv PDFs. No ICLR 2027 acceptance or anonymous identity inference is involved.

| Canonical ID | Target edition and card | Pages | Critical observation |
|---|---|---:|---|
| W0228 | [DeltaNet, arXiv v6](W0228.md) | 25 | Exact real-arithmetic delta-to-chunk factorization; L2/SiLU, conv, state size, and external attention hybrid matter. 1.3B retrieval negatives and length extrapolation survive. |
| W0060 | [Zoology, arXiv v1](W0060.md) | 69 | MQAR and rare recurring bigram slice; Theorem 4.4 is an existence upper bound, not a universal width lower bound; hybrid sees source. |
| W0219 | [MHLA, arXiv v2](W0219.md) | 22 | Learned block-index mixing differs from input-conditioned routing; extra block state; causal intra-block mask and extending the mixing matrix remain unclear. |
| W0100 | [Slot Attention, arXiv v2](W0100.md) | 27 | Slot-axis competition plus input-axis weighted mean, shared GRU, iterative set grouping; visual/full-image, not causal closed text memory. |
| W0240 | [Hopfield, arXiv v3](W0240.md) | 94 | Separation/near-query conditions and distinct fixed-point/one-step errors; explicit pattern bank counts toward physical storage. External UCI CSV not read. |
| BR-A03-D11 | [End-to-End Memory Networks, arXiv v5](BR-A03-D11.md) | 11 | Adaptive hops read an explicit fact/word bank; initial LM query is constant; 10-restart selection and equal-extra-compute control matter. |
| BR-A03-D12 | [GQA, formal EMNLP 2023](BR-A03-D12.md) | 7 | Independent Q/shared KV and checkpoint uptraining can recover quality, but zero-dose failures, 600 TPUv3 chip-days and encoder–decoder-only scope limit transfer. |

## Provenance and visual inspection

All seven downloads used existing Git Bash curl, ordinary Schannel HTTPS and revocation/certificate verification, `--location --fail --proto '=https' --proto-redir '=https'`, 15-second connection and 120-second total limits. Every request completed exit 0, HTTP 200, `tls=0`, `proxy=0`, with effective URL the requested public original. PDF signature and trailing EOF were checked, `pdftotext -layout -enc UTF-8` exited 0, first-page title/version checked, lengths and SHA-256 recomputed below. PDFs are original received bytes, not modified. The extractor used was already installed; generated UTF-8 text retains undecodable raw byte sequences as visible `\\xNN` escapes rather than guessing. W0060 emitted `Unknown character collection 'Adobe-Korea1'`; key carried table rows were visually checked. Not every formula symbol is faithfully extracted: use the original PDF for equations.

| ID | bytes | PDF SHA-256 |
|---|---:|---|
| W0228 | 474845 | `8efd24a5338429187d4990b082d72a3b463531a24c9b5385c54d63bce9e599ba` |
| W0060 | 3249054 | `4601ced8a55e2a3bdc826613ad4875d519a97cf90673b0767b8790a100813c1a` |
| W0219 | 8695036 | `41e2b680fda067e28dd035e44874b9576adc7ab8231a5a09147587dc430acb97` |
| W0100 | 3437358 | `ff310f9ee610ce0bad20bfc7517cb730b19e11b8f45195cd548b510616164b1f` |
| W0240 | 16562362 | `48cecc1d10cea553538fe8d1e2f1bf7378bed6b1233b2857384f5081ac2f7579` |
| BR-A03-D11 | 654484 | `8eddaf2a441092955d10aa34a9f2b690aaaecee9097a47693366e0c5b8ff36a0` |
| BR-A03-D12 | 221556 | `c52de1d3339174fbf93b588aa4cc9bf36092c865f2358ece3999de152f57455c` |

Visual evidence retained under [sources](sources/): W0228 p.8; W0060 pp.3,10; W0219 pp.9–11; W0100 p.6; D11 p.6; D12 pp.3–4. These images identify the actual checked carrying tables/figures, not every illustration. W0240's carried results and definitions were legible in extracted main/appendix prose and tables; no visual page is asserted for it. No source paper code was executed.

## Synthesis guardrails and unresolved items

- Distinct query vectors, physical stored values, block position/group allocation, write-time access and final content use are separate axes. W0219's source calls index-based coefficients dynamic per query in an appendix, contrary to its displayed block-index formula; its main language data/dose and Appendix D also disagree. App. C omits the within-block causal mask in its printed matrix formula and does not define unlimited group-index extension. Do not silently fill those gaps.
- W0060's v1 synthetic grid establishes empirical results for its training/search regime, not the failure of every later retuned recurrence. The exact theoretical existence constructions and the one-way finite-bit indexing lower bound are different statements. The 82% quantity is a capped weighted log-loss gap on a heuristic slice, not the fraction of all errors proven to depend causally on recalled content. Full/selected attention hybrids can access source KV.
- W0240's high pattern count includes the whole explicit bank and assumes geometry, probability and proximal queries. Slot Attention accesses the entire image; memory networks access their recent fact bank; neither establishes equal-bit, no-revisit causal text-memory superiority. W0228 attention hybrids also carry cache/source permissions. GQA retains token KV and supplies encoder cross-attention; it is not a recurrent fixed-memory experiment.
- D11's prose reports task-16 53.6% while its Table 1 reports 52.1%; D12 Figure 3 labels time `ms`, whereas Table 1 and Figure 6 label seconds. W0240 Appendix A.1.8 forgetting update omits the bias displayed in its energy. These source conflicts are not silently repaired. No RAM result is calculated in this batch; if reused elsewhere, the independently corrected nominal 500M ledger sums to **500.040M**, not exactly 500.000M.
- Cross-direction alternatives remain open: independent native-query repair, state-writing/normalization change, iterative computation without added reads, fixed-bit state partitioning, learned objectives and host adaptation. Test alongside permissible source-retrieval alternatives, controlling source availability, physical bytes, computation, optimization and evaluation visibility. No evidence here proves all memory paths blind, exonerates a byte interface, or selects an architecture.

## Verification and ownership

Seven Markdown cards, this summary, seven PDFs, seven derived texts and ten visually inspected page renders are under `03_reading/V11/` only. Public original acquisition and file/Markdown integrity are checked; tests, training, experiments, package installations, system settings, subagents, commits, and shared registry edits are outside this task. No assertion of project-wide reading totals or venue coverage is made.
