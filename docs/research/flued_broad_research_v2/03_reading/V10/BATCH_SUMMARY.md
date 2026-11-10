# V10 — classic objective/collapse countercontrols

## Accounting and status

Seven assigned **distinct works**, seven canonical-ID cards: **6 FULL / 0 PARTIAL / 1 BLOCKED body**, counting each work once. Six arXiv targets and one PMLR target were assigned; five arXiv targets and the PMLR target plus its official supplement were acquired and fully read. No old FULL card or different edition was reused or newly credited. `BR-A01-R16 = LD-N08` is **one** blocked work, not two. `BIW-0094`'s formal CoNLL edition, `BR-A01-R16`'s formal NeurIPS edition, and formal counterparts of other arXiv versions were neither read nor established equal. No conference acceptance or state inference was made from submission metadata. No ICLR 2027 original was assigned to this classic-control batch.

| Work/card | Reading status | Exact edition / material |
|---|---|---|
| [BR-A01-R09](BR-A01-R09.md) | FULL | arXiv 1711.00937v2, main and appendix; linked speech samples not auditioned |
| [BIW-0094](BIW-0094.md) | FULL | arXiv 1511.06349v4, main and appendices, carrying Tables 2–4 visually inspected |
| [BIW-0095](BIW-0095.md) | FULL | arXiv 1702.08139v2, main and appendix, Table 2 visually inspected |
| [BR-A01-R15](BR-A01-R15.md) | FULL | arXiv 1611.02731v2, main and Apps A–E, Tables 1–5 and Fig.3 visually inspected |
| [BR-A01-R16](BR-A01-R16.md) | BLOCKED | 1911.02469v1: two incomplete verified HTTPS transfers; **full body/proofs/experiments missing** |
| [BR-A01-R17](BR-A01-R17.md) | FULL | formal PMLR 119 paper and official separate supplement, proofs and key figures inspected |
| [W0064](W0064.md) | FULL | arXiv 1808.07593v4, main and Apps A–C, proof steps and Fig.4 inspected |

FULL is whole-source reading of the listed edition and carrying appendices, not execution, replication, independent theorem certification or inspection of every illustrative pixel. A key mathematical limitation remains: R17's proposition 1 says there is a global minimum, while its supplementary comparator construction exhibits an energy tending to −∞; its local-minimum argument has a degenerate Hessian and a W-only gradient step, not independently certified as a full joint-neighborhood proof. W0064's empirical information quantities are estimators/bounds; its theoretical guarantees assume the given Markov/distribution conditions. R09's qualitative audio/video claims are author-attributed and not a task prerequisite to understanding the method or the comparisons used in the card.

## Cross-source discriminators — not target-host diagnoses

- **More latent activity is not necessarily more useful information.** Bowman shows a positive KL with worse standard language-model perplexity; Yang shows the smallest CNN decoder's KL is larger than the best-likelihood decoder's. KL also contains aggregate-prior mismatch. VQ's nominal constant KL, used-code entropy, task information and native output dependence are different quantities.
- **Decoder-context control is not a universal cure.** Yang reports both likelihood gains and a too-wide decoder losing them; Chen's intended local texture loss sometimes loses OMNIGLOT semantics. Word VAEs, Gaussian image VAEs and discrete speech/image models do not diagnose deterministic byte interfaces or establish that all memories are blind.
- **Optimization and objective are different hypotheses.** Dai's nonlinear counterexample and deterministic-autoencoder controls complement, but do not replace, the separately owned inference-lag work and blocked linear-VAE account. Fixed-step deep-image experiments do not make collapse inevitable; loss geometry alone cannot identify the target project's cause.
- **IB scalarization is not a representation impossibility.** W0064 shows a specific degeneracy for deterministic targets; useful codes may still exist, and empirical MI bounds are not measured physical storage. Task distortion, objective/schedule, native reader, training stabilization and non-retrieval state changes remain independent options. Evaluate task-specific exact content and causal output dependence under matched visibility, physical rate and compute.

## Acquisition and scope receipts

Downloaded with normal existing Git Bash curl, HTTPS-only redirects and unchanged Schannel certificate/revocation validation. All seven saved PDFs (six papers plus R17 supplement) returned curl 0 / HTTP 200 / TLS verification result 0 / proxy_used 0, had `%PDF-` header and `%%EOF`, and parsed using existing `pdftotext -layout -enc UTF-8` exit 0. Requests used the exact linked source URLs in cards. SHA-256 below records bytes received, not a guarantee of equivalence between editions; text is derived and math extraction can omit symbols. Key tables/figures were checked in the original rendered PDFs, not inferred only from layout text.

| Saved PDF in `sources/` | Bytes | SHA-256 |
|---|---:|---|
| `BR-A01-R09__1711.00937v2.pdf` | 3,174,661 | `d62036803c190a82718b718f59a87adb2be8b586e4887a394ad0cef15c56301e` |
| `BIW-0094__1511.06349v4.pdf` | 498,526 | `b44c9758ee3a862048682b0cbf154984eefb87523df1c4d9a0d18d8968d017d2` |
| `BIW-0095__1702.08139v2.pdf` | 698,679 | `9fc40fd5c5fac02a08891dfb939ccdd173565adce72249adfea281071526d39b` |
| `BR-A01-R15__1611.02731v2.pdf` | 2,392,268 | `717c685fdd7ed18cae250c226a3d25452f33d12f1aba857c2800aac622d38099` |
| `BR-A01-R17__pmlr-v119-dai20c.pdf` | 406,015 | `be9b07b79ec8aecf16693c9722b1240492c47866d41c8aabc5bf291074d049fe` |
| `BR-A01-R17__pmlr-v119-dai20c-supp.pdf` | 387,937 | `3c5f9a9af7593805ed778dcb12c2d32f8df1676a76fe26c230174862706cda11` |
| `W0064__1808.07593v4.pdf` | 984,331 | `45391e265434bf2dff0740d5e53fb6b29d315b91275187bc41984904e4d8dca4` |

R09 and W0064 initially had connection timeouts; each completed on its one normal retry. R16's initial HTTP 200 stalled after 2,143,931/4,729,106 bytes; a normal range resume returned HTTP 206 but stalled with 407,634 bytes still missing. Partial removed, no body claim; exact acquisition/proof gaps are in its card. Browser navigation to the official R17 landing page returned `ERR_CONNECTION_CLOSED`; normal verified curl retrieved that page and its officially linked supplement. This does not imply a general browser or PMLR outage. No OpenReview wall, credential, proxy/certificate setting, package install or external temporary directory was used.

### R16-only acquisition follow-up

No reusable PDF or FULL reading was found by filename searches for `1911.02469`, `BR-A01-R16`, and `LD-N08`, or content search of the reading batches/staging. Earlier discovery notes record selected-section v1 reading, not a saved complete source or FULL card. A single further user-authorized, longer normal curl attempt to the locked v1 URL used a 30-second connection timeout and 420-second overall timeout. It failed at **30.015 seconds**, curl **28**, HTTP **000**, `proxy_used=0`, **0 downloaded bytes**; the reported TLS verification result 0 is not a success receipt when the connection never completed. No certificate validation was disabled. Counts remain **6 FULL / 0 PARTIAL / 1 BLOCKED body**; the existing six FULL originals were not reread. R16's earlier two transfers are retained as history above, not conflated with this new connection failure. The failed connection does not prove unavailability or denial.

R1's RAM correction remains **nominal 500M; displayed stage doses sum 500.040M**, not 500.000M; RAM is not an additional V10 read. Relevant unresolved work is R16 v1's full body and proof, formal-edition comparisons only if needed, and independently authorized code/experiment validation. Equal bits, independent content/address interventions, and native causal consumption remain proposed discriminators, not completed project experiments.
