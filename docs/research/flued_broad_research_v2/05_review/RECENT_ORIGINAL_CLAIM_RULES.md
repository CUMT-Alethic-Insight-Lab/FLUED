# Recent-original claim rules — independent targeted scientific review

9 November 2026. **Owned output: this file only.** This is a targeted review of four public originals and the current source/read ledger, not a bulk full-reading batch, independent replication, complete proof audit, venue census, novelty certificate, or architecture decision. It awards **zero new FULL reading credits**. Existing thematic drafts are inputs to check, not authorities overriding original passages.

## 1. Release judgment and evidence boundary

**A bounded scientific synthesis may use the three independently read V17 public preprints and the foundational V18 predictive-state learning paper. It may not describe the 17 unavailable selected official manuscripts as scientifically read, accepted, disproven, or exhausted by older alternatives.** T02 is no longer merely acquired/pending: its actual subsequent 37-page FULL public-edition card supersedes source R3's earlier acquisition-only snapshot. The official T02 body remains BLOCKED.

Keep four different records separate: official forum metadata/status, actual manuscript edition, substantive reading coverage, and independently verified result. A shared title or close abstract supports a candidate bibliographic relationship, **not anonymous-author identity, byte-identical manuscripts, shared appendices, or transfer of public-edition findings into an unread conference edition**. T03 even changes title from public *Linear Time* to official *Near Linear Time*.

The [current catalog](../02_catalog/READING_STATUS.md) reports 128 tasks, assigned-version 103 FULL / 6 PARTIAL / 19 BLOCKED, versus some-FULL-edition 108 / 5 / 15. These are attributed inventory fields, not this review's scientific approvals. The 17 official gaps are old six + V17 six + V18 five. Three independently FULL candidate public editions leave 14 works with no alternate established; they do **not** reduce 17 official gaps to 14. Source R3's 18 metadata checks overlap existing records and earn no scientific FULL credit. The adopted 50 official records are a selected status union, not 50 acceptances or a venue census.

### Inputs actually inspected

Read [PLAN](../PLAN.md), [SYNTHESIS_INPUTS](../02_catalog/SYNTHESIS_INPUTS.md), current sections of [COUNTS](../02_catalog/COUNTS.md), [READING_STATUS](../02_catalog/READING_STATUS.md), [OPEN_ITEMS](../02_catalog/OPEN_ITEMS.md), the complete [original 167-direction list](../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md), [original scope audit](ORIGINAL_SCOPE_AUDIT.md), current coverage R2/R3 decision passages, [reading audits R1](READING_AUDIT_R1.md)/[R2](READING_AUDIT_R2.md), [source audit R3](ICLR2027_SOURCE_AUDIT_R3.md), all four thematic drafts, and these four actual cards: [T02](../03_reading/V17/BR-R2-T02.md), [T03](../03_reading/V17/BR-R2-T03.md), [T05](../03_reading/V17/BR-R2-T05.md), [PSR](../03_reading/V18/BR-PSR-0912.2385.md). Historical count appendices are not a fresh census.

Independently inspected selected primary passages below. T02 was extracted directly from its local PDF in memory; T03/T05/PSR used existing PDF text, with a second installed PDF parser checking T02 proof pages and PSR p.4. No newly rendered image, whole-paper reread, paper implementation execution, fresh external metadata observation, or new source acquisition is claimed. Page references for T02/T05/PSR are PDF pages; T03 uses printed pages (PDF page = printed page + 1). `L` denotes a line in the linked saved extraction, not publisher line numbering.

| Work and actual public edition | Local primary source; targeted locations checked | PDF bytes / SHA-256 independently recomputed |
|---|---|---|
| T02, *Stochasticity in Tokenisation Improves Robustness*, [2604.16037v1](https://arxiv.org/pdf/2604.16037v1), 17 April 2026 | [PDF](source_staging/R3_BR-R2-T02__2604.16037v1.pdf): pp.2–8,12–15,18–25,27,30,33; sampling/support, scoring, attack, theory, costs and countercontrols | 705191 / `cad655df35b4027b157bf5ee1482eb72e9ef490364933b48606b42db1ff13977` |
| T03, *Online Tokenization with Optimal Delay in Linear Time*, [2610.19139v1](https://arxiv.org/pdf/2610.19139v1), 13 October 2026 | [Text](../03_reading/V17/sources/BR-R2-T03__2610.19139v1.txt): L711–757,2338–2387, throughput/table locators; Defs.4.7–4.9, Thm.1.1, §§6.1–6.2/Table6 | 1181161 / `86a4690df7f6a2a38243e157eac56b094047dc01ea155bd12e74212187078ce9` |
| T05, *Cross-Tokenizer On-Policy Distillation via Byte-Prefix Marginalization*, [2607.22334v1](https://arxiv.org/pdf/2607.22334v1), 24 July 2026 | [Text](../03_reading/V17/sources/BR-R2-T05__2607.22334v1.txt): L220–368,596–638,862–952,970–1028,1044–1197,1571–1575; definitions, conditional normalization, proof conditions, algorithm and code failure | 1283527 / `341d34838d7c76b9ae9449f0ab169cf8d20822be0012297413aaff220b73a949` |
| *Closing the Learning-Planning Loop with Predictive State Representations*, [0912.2385v1](https://arxiv.org/pdf/0912.2385v1), December 2009 | [Text](../03_reading/V18/sources/BR-PSR-0912.2385v1.txt): L115–259,284–341,480–544,550–639; rank, estimation, normalization, resource ledger and success denominator | 2673711 / `0951f68c2a76fe5e0a159afd182c0209ac0011f0723cea3526f329b731bed65e` |

## 2. T02: string-preserving segmentation robustness, not a general byte-memory cure

### 2.1 Exact support and what “uniform” means

The relevant support is `T_V(x)`: vocabulary-valid token sequences concatenating to **the same string x** (p.2). Changing token IDs/boundaries is not changing the underlying question, applying arbitrary text corruption, or testing semantic memory. Appendix B.2 pp.13–14 canonically tokenizes answer candidates and scores their conditional probabilities; typical random evaluation averages ten query tokenizations over 500 examples. Appendix B.4 uses a different in-context sampling estimand. Neither evaluates arbitrary output-tokenization invariance or full text-distribution equality.

| Sampler | Correct bounded description | Prohibited extension |
|---|---|---|
| STOCHASTOK | Algorithm1 p.18 samples a current token, attempts a valid two-way split, and skips unsplittable choices. `K=min(Kmax,ceil(alpha*canonical_length))` counts attempts. Successful splits and normalized realized expansion are separate. | Alpha fixes actual length/exposure, or every valid segmentation has positive probability. Pairwise reachability can exclude valid three-way segmentations (p.5). |
| STOCHASTOK-UNI | §5.1 p.6 samples per-canonical-token split counts, then uniformly samples feasible segmentations **conditional on those counts**. It stays within original token boundaries. Subtree-leaf weighting supplies conditional uniformity. | Globally uniform over `T_V(x)`, or full whole-string support across canonical boundaries. Fig.4's broad “full support” caption must be scoped by §5.1's explicit restriction. |
| UNIFORM-K | §5.1 p.6 uses a multi-rooted decision diagram to sample uniformly on the declared whole-string token-edit-distance-k support; it can cross canonical boundaries. | Same per-token split distribution as the other samplers, every k feasible for every string, or a production streaming/prefix-stability guarantee. |
| UNIFORM | Uniform on the declared whole-string valid-tokenization set, not on split counts, raw texts, model predictions or equal-length sequences. | Equivalent cost/exposure to a fixed nominal-alpha method; the paper says it substantially increases splits and compute. |

**Confirmed mathematical scope failure, not an implementation accusation:** Appendix F p.21 says STOCHASTOK's split-count vector “corresponds exactly” to a Pólya urn and hence `DirMult(N,1)`. Algorithm1's skipped attempts make this false without additional successful-split/feasibility assumptions. A finite counterexample is canonical `[a,bc]`, vocabulary containing `a,b,c,bc`, one attempt. With probability 1/2 the unsplittable `a` is chosen and realized counts are `(0,0)`; with probability 1/2 `bc` splits and counts are `(0,1)`. `DirMult(1,(1,1))` instead assigns 1/2 each to `(1,0)` and `(0,1)`, including an infeasible split of `a` and excluding no-split output. Rejection/renormalization onto feasible counts gives `(0,1)` with probability one and **still does not reproduce** the printed attempt algorithm. A cap at maximum feasible splits can also alter the law. This elementary calculation was checked with exact rational arithmetic; it is not a test of the authors' code or a measurement of the effect in their reported corpora.

Consequently, say “uses an idealized split-count correspondence; runtime skip/cap/feasibility handling requires clarification” rather than “same realized split distribution by construction.” Uniform probabilities must be normalized on the actual declared feasible support; do not silently remove impossible outcomes and retain the old distributional claim. T02's existing card appropriately flags feasibility; this review makes its limitation concrete rather than overturning its empirical cells.

**Prefix terminology:** T02 preserves the decoded string, but supplies no every-future-suffix commit theorem. It must not inherit T03's stable-prefix guarantee. Conversely, byte-prefix probability normalization belongs to T05 below; it is not a guarantee proved by T02.

### 2.2 Threat model and the adversarial denominator

§2 p.3 and Algorithm2 p.18 define an adaptive local search using correct/wrong answer-option scores; the asymmetric token edit costs are insertion1/deletion0. The attack changes valid encodings of the same string, normally starts canonically, and stops at a local optimum. Appendix G.2.3 p.30 tests ten iterations with radius2/radius4 and canonical/uniform-random starts. These are not exhaustive worst-case certificates, attacks on every public serving API, or hidden-future-text attacks. A service accepting only raw text through an enforced canonical tokenizer has a different attack surface.

- **Positive retained:** Fig.5 p.8 reports Llama-1b/Language Game canonical-trained accuracy **94.0% clean → 6.1% attacked**; UNIFORM-K alpha-fine1 is **94.8% → 69.6%**. This is a substantial tested improvement with remaining errors, not immunity. The corresponding 29.8-point random-query drop in Table2 p.7 is an absolute percentage-point change, not a relative percent loss.
- **Reversing attack control retained:** Fig.11 p.27 shows severe failures on canonically pretrained Tiny-LLM under random-start attacks; many stochastic-alpha cells are 0.00–0.04. Do not omit the distinct UNIFORM arm or recast this as every stochastic setting having the same value.
- **Attribution qualification:** Fig.15/§G.2.3 p.30 holds two-way support fixed while varying uniformity and separately expands support. The authors report no significant benefit for uniformity on that fixed support and stronger benefits from expanded support under harder attacks. This qualifies an unqualified “uniformity causes robustness” explanation. It neither proves equality of same-support methods nor proves support is the sole cause everywhere.
- **Clean negatives retained:** Table8 p.25 canonical OpenWebText token perplexity **29.77→53.06**; Table9 canonical ARC-E **.378→.330**, COPA **.660→.610**; TokSuite canonical aggregate **.3746→.3623**. Per-token perplexities on different segmentations are not directly comparable byte-normalized likelihoods. Comparisons using the same canonical validation segmentation remain meaningful within that metric.
- **Resource restriction:** §§4.3/5.1, Tables4–7 pp.12–13, and Fig.18 p.33 do not establish matched raw-byte exposure, realized lengths, teacher/search work or FLOPs. Alpha and BPE-dropout probability induce different actual split budgets. “No additional inference cost” is conditional on returning to the same deterministic tokenizer/model execution, not on longer stochastic inputs or contexts being free.

### 2.3 Theorem6.2: what is and is not established

§6.1 pp.7–8 and Appendix E pp.19–20 present a weight-norm/Lipschitz upper bound proportional to `sqrt(k)` for a **one-layer**, bounded-embedding, 1-Lipschitz-activation classifier-like model. The pivotal step Eqs.18–20 subtracts equal-shape one-hot matrices and counts at most k changed **aligned columns**, each of norm `sqrt(2)`. This is an aligned-substitution argument. Variable-length splitting changes the number of columns; insertion/deletion can shift arbitrarily many later positions. The written step does not establish the paper's full variable-length threat set without a common-domain alignment/padding and positional argument. Calling the one-layer case “without loss of generality” does not supply a reduction for deep models.

Furthermore, the bound contains model norms, not a theorem comparing stochastic-trained versus canonical-trained weights. No proved ordering of those norms/risks follows from sampling uniformity alone. Unit-normalized last-token representation distances (Appendix B.5 pp.14–15; main p.8 says 10k tokens whereas B.5 says 1,000 common words) are empirical geometry, not a certified local/global Lipschitz constant, classification-margin guarantee or functional causal explanation.

**Safe report sentence:**

> In public 2604.16037v1, stochastic tokenization improves tested same-string input-segmentation robustness, including a large but incomplete gain under a local score-aware attacker. Expanded-support controls, clean-task regressions, realized split budgets and one-layer aligned-substitution proof limits prevent a general uniformity-only, cost-free or deep-model robustness guarantee.

**Do not write:** “proved stochastic training reduces worst-case risk,” “uniform over all segmentations” for STOCHASTOK-UNI, “byte interfaces solve the attack,” “robust semantic memory,” or “recommended default for the target host.”

## 3. T03: stable prefixes, delay, and the measured implementation are different claims

Defs.4.7–4.9, printed pp.12–13, text L711–740 define stable output `z` at input x by `z <= Tok(xy)` for **every continuation y, including empty**. `Tok_stable(x)` is the longest such prefix. Delay k requires

`Tok_stable(x[:-k]) <= z <= Tok_stable(x)`.

Here k counts input-alphabet characters, not emitted tokens, GPU time or transport chunks. Stability is stronger than equality with `Tok(x)` at an isolated prefix; offline tokenization can change when more text arrives. End-of-input flush uses the fact that no continuation remains and must be distinguished from pre-flush commitments. Nothing here independently certifies arbitrary partial UTF-8 byte transport, special-token modes or normalization in a particular production implementation.

Theorem1.1 (printed p.13, L755–757) is a conditional worst-case lower bound unless P=NP for polynomial preprocessing/total time over tokenizer/regex parameters, also covering `o(mt)` delay. It is not hardness of every fixed tokenizer on every practical string. The constructive bounds have regex, merge-list, longest-token and special-token assumptions; “optimal” concerns the stated asymptotic delay comparator, not universal best wall time.

**Decisive source disclosure:** §6.2 printed pp.40–41, L2362–2387, explicitly says measured code uses simple backtracking and invokes incremental, **not online**, BPE only after a pretoken boundary resolves. It can retain an arbitrarily long unfinished pretoken even for bounded-lookback patterns. §6.1 Claim6.3 additionally gives unbounded generalized lookback for adversarial CL100K/O200K whitespace. The caveat is present in the original, not an accusation invented by the reader.

The first-token **formed** speedups 7.9–34.8x are tokenizer measurements; Table6 lets optimized serial gigatoken win English and several code cells (e.g. r50k English 331.1 versus 298.7 MiB/s). Measured approximately flat RSS over selected 1–128 MiB inputs is not a worst-case constant-memory theorem or end-to-end model serving result.

**Safe report sentence:**

> Public 2610.19139v1 formalizes offline-equivalent stable-prefix emission with parameterized delay bounds; its throughput-oriented measured implementation deliberately waits for completed pretokens, so the strongest theoretical delay/memory claims do not transfer automatically to those benchmarks.

**Do not write:** “all learned segmentors are prefix-safe,” “every BPE stream is NP-hard,” “constant memory for arbitrary inputs,” “34.8x model latency improvement,” or “the anonymous Near Linear Time edition was read.” This sharpens I.08–I.09/I.24–I.28 and resource comparisons, not native semantic query formation or retained-memory sufficiency.

## 4. T05: conservation, prefix conditioning, refinement exactness, and spanning lower bounds

### 4.1 The exact quantity must be named

§3.2 Eqs.2–5 pp.4–5 and Appendix C pp.16–17 distinguish the following:

1. Teacher next-token distribution `q(w)` induces a **finite-teacher-token pushforward** through `phi(w)`, the longest student-token byte prefix of `bytes(w)`, plus residual. A partition of teacher outcomes conserves mass exactly in real arithmetic.
2. Prefix mass `pi(c)=sum_{w: c is a prefix of bytes(w)} q(w)` is not itself a distribution over all c: nested prefixes overlap. Node differences `rho(c)=pi(c)-sum_b pi(cb)` or disjoint longest-prefix routing prevent duplicate credit. In the paper's worked example q={a:.2,at:.5,ate:.2,bit:.1}, the four raw prefix masses sum to **1.9**, whereas disjoint scatter masses sum to **1** (Appendix D pp.17–18, text L1170–1193). Exact rational arithmetic confirms this elementary distinction.
3. For an interior row after observed prefix r, restrict to compatible teacher tokens and divide by **positive** `pi(r)`, then scatter remaining bytes (Eq.5/A.6/D.1; L278–289,911–922,1135–1147). Zero compatible mass makes conditioning undefined; a numerical floor/truncation is an additional implementation contract, not this exact probability identity. Normalization is not permission to discard unmatched outcomes and silently renormalize the rest.
4. Proposition C.2 assumes **A1 lossless concatenative byte decoding**, **A2 idealized greedy longest-prefix student segmentation**, alignment and a refinement regime. Actual BPE merge priority can violate A2; the source acknowledges no proved error bound despite reported position-level checks (L1053–1063,1090–1123). An observed realized chunk is not by itself a universal guarantee for every counterfactual continuation.
5. A student token spanning several teacher tokens receives a product along the **realized teacher path** times terminal prefix mass (Eq.6/A.5). Other teacher segmentations can spell the same bytes, so it lower-bounds unrestricted byte mass; mass-neutral reallocation preserves normalization without summing those missing paths. Rows that neither start at nor reach a sync point are excluded.

A simple **extension counterexample**, not a refutation of the finite-token pushforward: let teacher first-token mass be q(a)=q(ab)=1/2, with teacher continuation b certain after a; student vocabulary contains a,ab,b and greedily takes ab. Isolated-token scatter gives a and ab probability1/2 each. The whole generated stream begins ab with probability1 and student first token is ab with probability1. Thus conservation and A1/A2 alone do not make the isolated-token law the unrestricted whole-stream first-token law. The absent universal no-crossing/refinement condition is material. This calculation was independently checked with exact fractions; no actual tokenizer or paper code was executed.

**Safe exactness wording:** “Mass-preserving teacher-next-token pushforward; exact for the specified conditional/refinement cases under A1/A2; realized-path lower bound for spanning cases.” The reported >99% realized-position share (Table D.2) is a corpus frequency, not a bound on total mass error, counterfactual coverage, deployment frequency or sequence-level semantic fidelity.

### 4.2 Function-level counterexample and limits of causal wording

§4.3 pp.8–9/Fig.3, text L600–618, reports **GLM-Z1-9B pair/BPM-JSD** unmasked code pass **49%→9%**, block-indentation errors **84%**, while math remains stable. The otherwise identical whitespace mask removes about3.5% of aligned code rows and prevents that collapse. Mask-matched random non-whitespace removal does not rescue the same code-tail reward (0.11 versus0.17). Appendix H.2, L1571–1575 gives 128 generations per checkpoint for pass/error diagnostics and 80 programs/1,799 positions for margins. These denominators should travel with a precise quantitative quotation.

This is strong targeted evidence that the mask choice matters in that training comparison. It is not proof that all whitespace bytes carry no content: indentation demonstrably carries program structure. The source's “only segmentation noise” explanation is an interpretation, not universal information theory. It does not show that all exact distillation must collapse, nor that mass normalization was mathematically wrong.

Keep best-divergence/checkpoint selection and task negatives in view: Table1's aggregate wins are not every dataset winning; the default JSD is not the headline best forward-KL arm. Bootstrap resampling is not multi-training-seed uncertainty. Masked/excluded rows still count in the loss normalizer (Eq.9 L363–368). Stop mass uses explicit tokenizer/config/template sets and a separate forward-KL bridge, not a universal end-of-text identity. Student histories and teacher-rendered templates, teacher full-vocabulary scoring, rollout caps and selection all remain costs/permissions. No end-to-end FLOP or language-memory advantage follows from matched prompt/update counts.

**Safe report sentence:**

> Public 2607.22334v1 offers normalized cross-tokenizer supervision with explicitly conditional exactness and realized-path approximations. Its whitespace ablation shows a substantial code-function failure without masking in one teacher/student/JSD setting, warning that local probability fidelity and downstream utility are separate outcomes.

**Do not write:** “exact teacher byte-string probabilities at all positions,” “99% globally exact,” “prefix sums can simply be renormalized,” “whitespace has no semantics,” “all divergences/teachers collapse,” “EOS equivalence is proved,” or “distillation establishes remote semantic memory use.” Relevant directions are A.16/F.17–F.18/I.01–I.03/I.10–I.11/I.24–I.28; it does not close mixed-interface architecture or native-consumption questions.

## 5. Learned predictive state: identification is real, unconditional near-optimality is not

The 2009 public original is **foundational, not a recent ICLR2027 result**. It is distinct from the 2001 diagram-qualified source and all unread recent predictive-scope/bottleneck manuscripts.

§§2.1–3.1 pp.3–5, text L132–259/284–341, require finite system linear dimension, sufficiently rich history/test features preserving rank, invertible `U^T R` (or its feature analogue), and convergent empirical moments. Actions in tests are interventions, not observed future answers (p.2, L119–127). State updates normalize by a conditional-event probability. Small denominators/near-singular moments are genuine numerical qualifications; this review does not attribute a measured conditioning ablation to the paper. Reset sampling supplies the required exploration histories; suffix-history sampling from an unresettable stationary stream is explicitly approximate because interventions change later histories (L208–219). Finite estimates can yield negative probabilities; suggested thresholding is not exactness or a general finite-sample guarantee.

**Confirmed printed estimator inconsistency, not a whole-method refutation:** p.4 §3 step3(a) prints `b_hat_1=U_hat^T P_hat_H`, whereas p.3 Eq.5a defines `b_1=U^T P_(T,H) 1_k`; the feature version p.5 Eq.10a uses `U^T P_(T,H) e`. With `U` of shape `|T| x n` and `P_H` a `|H|` vector, the printed step3(a) is dimensionally undefined when `|T| != |H|`. Even for equal sizes it is generally not the earlier moment formula. The p.4 expression was confirmed using two local PDF text parsers. This is a source notation/formula correction requiring clarification before literal algorithm reproduction; no source code was inspected and no empirical failure is inferred. The carrying card does not claim to have certified every equation, so its FULL label is unaffected.

The experiment is an actual learned-model/closed-loop example, not merely existence: §5.2 pp.7–8 uses 10,000 seven-pair trajectories (2,000 for centers,8,000 for estimates), 2,000 history and2,000 test kernels,500 observation kernels,six actions and selected rank5. Moment matrices, projected operators, SVD/pseudoinversion, reward regression and the8,000-point planner accompany five deployed coordinates. A small coordinate vector is not a five-number total system or equal-resource language comparison.

**Denominator is decisive:** Fig.2D p.8 caption (L571–576) marks **18.2 actions as averaged over the78 successful paths**. §5.4 p.9 (L622–635) states **78/100 successes and22 alternating-action loop failures**. A*'s13.9 uses true configuration unavailable to the learned policy; random walk is507.8. Do not multiply18.2 by.78 to invent an all-trial path mean, assign failed trials zero steps, or silently censor them. Without a failure horizon/penalty ledger the unconditional path-length/cost comparison is unidentified. Suggested lookahead/randomization is not tested recovery in this result.

**Safe report sentence:**

> In public0912.2385v1, spectral predictive-state identification under rank/exploration assumptions supports a visual-navigation planning example with78/100 successes;18.2 actions is success-conditional, with22 loop failures and a privileged A* comparator. This narrows the existence-versus-learning gap without establishing arbitrary-query language sufficiency or equal-resource closed-loop superiority.

This improves B.19 and informs A.06–A.08, but does not establish differentiable writer/reader coformation, unknown semantic-query transfer, durable relation identity, or a diagnosis of the target host.

## 6. Stale draft handoff — record, do not edit other owners' files

The drafts already integrate T03/T05/PSR in substantial bounded form; a blanket assertion that all four still treat all V17/V18 as pending is itself stale. Their remaining **T02** handling, however, predates the actual card completed at19:59:28+08:00. The following source positions are an observed snapshot, not a claim about future concurrent revisions:

| Read-only draft / location | Stale or overbroad statement | Required author action |
|---|---|---|
| [A/B](../04_synthesis/01_COMPRESSION_AND_STATE_EN.md), §12, L364–366 | “two independent recent preprints”; T02 reading “in progress” | Cite the now-FULL public2604.16037v1 with §2 restrictions; retain all17 official gaps. |
| [C/D](../04_synthesis/02_ADDRESSING_AND_CAUSAL_USE_EN.md), §12.1 L288; §12.2 L304–305 | Two-public-preprint snapshot; broad T02 “no verified robustness result” language and only T03/T05 edition distinction | Distinguish official T02 no-result evidence from actual public-edition results; add T02 to the separate edition field without treating it as native query/content-use evidence. |
| [E/F](../04_synthesis/03_DYNAMICS_AND_TRANSFER_EN.md), §13.1 L318,324 | Two public FULLs; T02 grouped with “no independent body identified/no body-read empirical result” | Separate T02 from T01/T04/T06; use only actual segmentation-training findings, not gradient-starvation or native-memory causal claims. |
| [Cross-axis/recent](../04_synthesis/04_CROSS_AXES_AND_RECENT_EN.md), L5,175,188,193,201,225 | Acquired/unread T02 table row, pending source gate and two-FULL-plus-one-acquired formulation | Replace the stale public-edition status and integrate support/clean-negative/attack/theorem limits; keep official source gap. |
| [Coverage R3](COVERAGE_RECHECK_R3.md), §§1/3/7 | Two-recent-preprint/three-completed-edition snapshot | Treat as historical review timing, not a veto on T02's subsequent read; this review adds targeted original checks, not a new global coverage judgment. |
| [Source R3](ICLR2027_SOURCE_AUDIT_R3.md), §§1/5–7 | Acquired-only/pending T02 at its own snapshot | Preserve as acquisition provenance, but use current actual card for scientific reading status. Do not rewrite its zero-FULL audit credit. |

The four thematic drafts are not silently approved in their uninspected scientific details by these corrections. Their nearest relevant claims about T03 implementation, T05 conditionality and PSR success conditioning are corroborated at the selected original passages. Other R1/R2 restrictions, original167 residuals and strongest reversing controls remain binding.

## 7. Official frontier: result-level exclusions and safe recent disclosure

[Source R3](ICLR2027_SOURCE_AUDIT_R3.md) supplies dated metadata/access observations, not this review's fresh network results. Its representative PDF403s, forum verification and API challenge do not prove one common per-file root cause for17 manuscripts. A404 HEAD on one T02 attachment is route/method-specific, not proof absent/private supplementary material. No repeated denied-route requests or identity matching are needed to deliver this file.

For the other14 works without a FULL alternate established, retain a **metadata/abstract-attributed candidate description only**:

- T01 formal tokenization: no theorem about predictive/task sufficiency or certified downstream superiority from the title.
- T04 late/head invariance: no body-supported conclusion that heads generally localize tokenization damage or head-only repair is sufficient.
- T06 B-Net: no prefix-safe controller, attainable online rate, causal-generation or matched-cost superiority claim.
- V18 LoopLA/Farsighted Correction/finite-query compilation/attention placement/predictive scope: no loop equivalence, general shortcut remedy, minimum-slot theorem, unknown-query exactness, placement winner or equal-bit scope cure imported from abstracts.
- Earlier Incentive/SDG/routing/predictive bottleneck/two stitching sources: do not promote proposed incentive, gate, lock-in, rank or receiver mechanisms into validated results. Keep the competing hypotheses visible rather than treating unavailable papers as negative evidence.

A full reading, if later possible, still would not automatically certify its proof, implementation, controls, all-system costs or target-host transport. No architecture follows from accessible sources winning an access-conditioned comparison. Same-title independent preprints must not be used to deanonymize forums.

**Replacement disclosure suitable for the final English report:**

> Our recent source index comprises selected official submission-metadata snapshots and edition-scoped public evidence, not acceptance decisions or a comprehensive ICLR2027 results survey. Seventeen selected official manuscripts remain unread/unavailable through the ordinary routes tested. Three related public preprints—2604.16037v1,2610.19139v1 and2607.22334v1—have independent FULL reading cards; the2009 predictive-state learning paper is a separate foundational completion. We cite scientific results only at the actual read editions. Title/abstract relationships establish neither manuscript equality nor anonymous-author identity. Unavailable alternatives remain potential counterevidence, and claim-specific theorem, artifact, cost and target-system gaps remain open.

## 8. Validation, limits, and ownership receipt

Only `docs/research/flued_broad_research_v2/05_review/RECENT_ORIGINAL_CLAIM_RULES.md` is authored. All drafts/cards/catalogs/source audits/source PDFs/text/project guidance remain untouched. No subagents, installs, training, checkpoint operations, project experiments, external downloads/queries, registry changes, commits or pushes occurred. Local in-memory exact-rational toy calculations are applicability checks, not empirical experiments or executions of paper implementations.

Validation performed: recomputed the four primary-PDF lengths/SHA-256 values; checked T02's finite skipped-attempt/feasibility-renormalization counterexample, T05 overlapping-prefix/scatter and unrestricted-stream extension arithmetic, and PSR78+22 denominator arithmetic. Static deliverable checks cover strict UTF-8, final newline, trailing whitespace, relative Markdown file targets, required editions/conditions and read-only input snapshot comparison. Git status is inspected for unintended artifacts. The v2 root was already untracked and concurrent writers exist, so status does not attribute their work to this reviewer. No temporary files/scripts/images were created. Build/pytest do not apply to this Markdown-only review and were not run; original results were not independently reproduced.

**Still open:**17 official bodies and their edition relationships/decisions; actual implementation of T02 skip/cap/feasible-count sampling and theorem extension; T03 production prefix/flush/transport behavior; T05 counterfactual refinement/true BPE probability error, numerical zero-mass handling and complete cost ledger; PSR initial-estimator reconciliation/finite-data reliability and all-trial planning costs; all target-host semantic-query, native-content-use, history and equal-resource discriminators. The two confirmed source-formula/scope issues are narrow and substantiated; neither licenses a whole-paper invalidity or reader-misconduct claim.
