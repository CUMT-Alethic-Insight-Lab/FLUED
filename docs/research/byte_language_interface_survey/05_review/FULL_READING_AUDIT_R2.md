# Independent targeted full-reading evidence audit — R2

2026-11-09. Independent red-team follow-up to [R1](FULL_READING_AUDIT_R1.md), under [PLAN](../PLAN.md). This is a claim audit, not synthesis, a replacement for terra's selected-paper reading, or an implementation reproduction. Adoption-ready prose is collected in [CLAIM_RULES](CLAIM_RULES.md).

## 1. Scope and verdict

I read R1, [DISCOVERY_CORRECTIONS](DISCOVERY_CORRECTIONS.md), all **14 new cards** in R09, R10 and FIELD_ADDENDUM, their three batch summaries, and the current MTPC, MYTE and Hourglass cards. I independently checked designated primary-source passages from **10 distinct works**: **2 R09, 2 R10, ACT, Reformer, MTPC, TokSuite, MYTE and Hourglass**. Reading cards is not counted as another original-source verification. The remaining six R09/R10 works and ELMo/GPT-2 were inspected at card level only in this follow-up.

**New FULL papers credited by this reviewer: 0.** The checks do not re-count versions, appendices, R1 readings, or discovery's code inspection. They do not certify every statement in the sampled FULL cards or another reader's historical actions.

### Decision summary

| Question | R2 decision | Consequence for survey authors |
|---|---|---|
| Do sampled R09/R10 claims have primary support? | Yes for the tabulated findings and boundaries in §2; **one new correction** concerns the dialect card's overconfident prose-sign attribution (§2.2). | Use bounded results, not a common matched-cost frontier; attribute dialect signs to the named table columns. |
| ACT and Reformer as alternatives to learned shortening? | Supported, with different compute interventions and evidence limits (§3). | ACT repeats work within a byte; Reformer retains positions and changes connectivity/training-memory execution. |
| MTPC rejection concern in R1? | **Retain and sharpen.** Fixed v2 text and visually inspected Algorithms 2–3 support a declared-algorithm concern; a literal discard-and-restart interpretation has an algebraic counterexample (§4). | Do not certify the optimized stochastic wrapper as target-law preserving. Do not declare the released implementation broken or published stochastic outputs demonstrably biased. |
| TokSuite C.2 versus Figure 6? | **Expression problem confirmed again in original PDF p.21; actual log-to-figure computation remains unknown** (§5). | Exclude Figure 6 as certification of equal cross-tokenizer BPB/training sufficiency pending its pipeline. Do not invalidate separate evaluations by association. |
| MYTE reversal? | **Exact row/column mapping resolved; current card still transposes the two means.** Main/appendix ranking difference remains unreconciled (§6). | Use explicit model names and table headers, not row position. Do not invent a reconciliation or a universal MT win/loss. |
| Hourglass within-group independence? | **R1 correction reconfirmed:** Appendix A.1/Table 9 explicitly retains the shifted-input residual (§7). | The shortened branch lacks current-group history, but the whole restricted model may still use the immediately previous symbol. |
| Are designated narrow PARTIALs failed full reads? | No (§8). | Preserve the ELMo/GPT-2 scope and missing sections without counting them FULL or treating them as access failures. |

The important unresolved claims are not unresolved because all source reading failed. They concern different evidence levels: a paper specification, an analyst derivation, missing artifact/run provenance, or genuinely unexamined sections. Their remedies differ.

## 2. Primary-source verification ledger: R09 and R10

Line locators refer to the retained extracts as read; version, section, table and quoted phrase provide stable backup if lines move. These are targeted passages, not fresh whole-paper readings.

### 2.1 R09: plain byte Transformer and fixed sparse attention

**R09 sample 1 — BIW-0071, Bridging the Gap for Tokenizer-Free Language Models.**

- Card: [R09/BIW-0071](../03_reading/R09/BIW-0071.md), especially “Corpus, probability object and controls.”
- Primary: [1908.10322v1](https://arxiv.org/pdf/1908.10322v1), §§2–3.2, Table 1, Eq.3; retained [text](../03_reading/R09/sources/BIW-0071.txt), lines **55–109 and 125–176**. Table 2 extraction is interleaved; I do not use it to freshly certify every comparator row.
- Checked: 40-layer causal Transformer, 256 possible byte values, roughly 836M parameters; stride-one final testing recomputes a complete 512-byte context. Development scores the second half of windows with stride 256, with reported 0.874055 versus 0.87413 BPB. The dataset is pretokenized and replaces rare words with UNK. Table 1 explicitly counts **159,658 test word events including EOS** and **826,189 bytes including newlines**. Eq.3 converts BPB by their ratio.
- Assessment: the card correctly separates byte interface from untouched original data, sampled byte exposure from unique corpus size, and parallel window scoring from cached generation. The probability conversion is bookkeeping for the **same scored event**, not equality of separately trained models' text marginals. The small rounded BPB-to-PPL calculation is consistent with approximately 23 word perplexity.
- Safe wording: “A large plain byte Transformer was competitive on the processed, sentence-shuffled LM1B benchmark; its byte likelihood was re-expressed per word using matching corpus event counts. This is not an equal-compute or raw-text deployment comparison.”
- Prohibited inference: “Tokenizer-free means no preprocessing”; “23 word perplexity proves an equally cheap raw-text model”; “a common byte denominator automatically marginalizes alternate tokenizations.”

**R09 sample 2 — BIW-0118, Generating Long Sequences with Sparse Transformers.**

- Card: [R09/BIW-0118](../03_reading/R09/BIW-0118.md), “Evidence and costs.”
- Primary: [1904.10509v1](https://arxiv.org/pdf/1904.10509v1), §7.2, Tables 1–3; retained [text](../03_reading/R09/sources/BIW-0118.txt), lines **358–435**. The source's modality distinction was also checked in the following §7.4 passage.
- Checked: at 12,288-position enwik8 context, Table 2 gives dense **1.00 BPB / 1.31 Time/Iter**, fixed sparse **0.99 / 0.55**, and strided sparse **1.13 / 0.35**. The header supplies no time unit. Adjacent §7.2 explicitly says strided attention failed to do well on this text dataset; Table 3 changes the number of positions scored in parallel to increase minimum evaluation context. The million-position demonstration is audio, not language.
- Assessment: the negative strided result and the unidentified Time/Iter unit are correctly retained. Neither sparse edges nor a smaller iteration number proves a serving improvement. This is a full-position alternative, not learned patching.
- Safe wording: “Fixed sparse attention preserved text quality in the reported comparison, whereas the strided pattern had worse BPB despite a smaller reported iteration-time value. Table 2 does not identify the time unit or establish cached decoding latency.”
- Prohibited inference: “All sparse patterns improve language likelihood”; attaching seconds to those entries; “million-byte language generation”; universal throughput claims from theoretical interaction counts.

### 2.2 R10: candidate-limited sparse lexical coding and dialect associations

**R10 sample 1 — BIW-0127, T-FREE.**

- Card: [R10/BIW-0127](../03_reading/R10/BIW-0127.md), “Interface, probability, and collision contract.”
- Primary: [2406.19223v2](https://arxiv.org/pdf/2406.19223v2), §§3.1–3.2/4.1, Appendix A Algorithms 2–5 and Limitations; retained [text](../03_reading/R10/sources/BIW-0127.txt), lines **189–252, 659–739 and 533–543**. Stored [p.4](../03_reading/R10/sources/BIW-0127-p4.png) and [p.6](../03_reading/R10/sources/BIW-0127-p6.png) were read visually for the splitting/encoding description and the 80k English + 20k German dictionary.
- Checked: rule-based splitting; padded trigrams; binary feature accumulation; multi-label BCE; candidate scores from a compiled dictionary and sigmoid activations. Algorithm 5 normalizes candidate scores and takes argmax. §3.2 describes 500k common training words plus prompt additions; §4.1 gives the evaluation's 80k English + 20k German regime. The paper asserts noncolliding word encodings after noncolliding trigrams, but its Limitations explicitly says repeated trigrams are accumulated only once.
- Analytical check: `_aaaa_` and `_aaaaa_` have the same **distinct** length-three substrings, `{_aa, aaa, aa_}`. Under Algorithm 2's binary set rule they produce the same union of trigram hash features, even assuming unique per-trigram codes. This refutes a universal injectivity claim for that stated representation. It is **not a collision measurement in released software**, nor proof that benchmark words were affected. Runtime length features, fallback splits or a different encoding would need separate artifact evidence.
- Assessment: the card correctly distinguishes input encodability from candidate-limited output and generic representation noninjectivity from empirical harm. Its wording “byte-wise” versus character examples is appropriately not resolved by assumption.
- Safe wording: “T-FREE avoids a learned subword vocabulary but uses rule-based units, binary trigram features and dictionary-selected whole-unit outputs. Its stated binary aggregation does not guarantee distinct encodings for all words; actual collision rates and implementation handling were not verified.”
- Prohibited inference: open-ended spelling outside the candidate set; native next-byte likelihood; dictionary-independent normalized word likelihood from BCE alone; measured collision damage or broken released software.

**R10 sample 2 — BIW-0134, dialect tokenization/representation biases.**

- Card: [R10/BIW-0134](../03_reading/R10/BIW-0134.md), “Actual task-dependent correlations and scope” and “Glyph example.”
- Primary: [EMNLP 2025 formal PDF](https://aclanthology.org/2025.emnlp-main.1224.pdf), §5.2–5.3, pp.23997–23999, Appendix F **Table 8 p.24009**; retained [text](../03_reading/R10/sources/BIW-0134.txt), lines **270–383**. Stored [p.18](../03_reading/R10/sources/BIW-0134-p18.png) was read visually because extraction interleaves model/task rows.
- Confirmed Table 8 DI correlations: tokenization parity **+0.638 Phi-3.5, −0.380 Llama-3.2, +0.4836 mBERT**; Phi DI information parity **−0.413**. The same table's TC/EQA overall tokenization-parity correlations are negative. The table does not provide effective paired sample sizes or significance estimates for these cells.
- Precision about the prose conflict: §5.2 first correctly describes **negative TP–DI correlation for Llama**; the next-page sentence “the correlation is positive in Llama-3.2” follows discussion of **IP**, for which Table 8 gives **+0.268**. Thus that sentence is **not unambiguously a contradiction of the TP table**. The current card/batch summary's categorical assertion that it calls the **TP** relation positive is too strong. It may refer to IP, or its referent may be ambiguous. Use the named table columns, not an asserted source-sign error. This follow-up proposes the clarification but does not edit the card.
- §5.3 explicitly allows reassembly into correct Unicode on decoding. Latin-looking displayed pieces do not establish a broken or lossy codec. No actual tokenizer artifact or round trip was run.
- Safe wording: “Appendix F Table 8 reports task- and model-dependent associations: DI tokenization-parity correlations are positive for Phi and mBERT but negative for Llama, whereas Phi DI information parity is negative. A later positive-correlation sentence can refer to Llama's IP result; the table's explicit columns should determine attribution. These associations do not isolate a causal tokenizer effect.”
- Prohibited inference: “The source definitively contradicts its own TP sign”; statistical significance from r alone; causal fairness improvement from fragmentation; irreversible Unicode corruption from printed glyphs.

**New R2 correction:** unlike the three old issues carried from R1, the dialect prose-reference clarification above is a newly identified overstatement in the R10 card/summary. It does not change any of the tabulated correlations or the closure of the substantive T8 source-reading gap.

## 3. FIELD_ADDENDUM: targeted ACT and Reformer checks

### 3.1 ACT: adaptive depth at an unchanged byte position

Card: [ACT](../03_reading/FIELD_ADDENDUM/arxiv_1603.08983v6.md). Primary: [1603.08983v6](https://arxiv.org/html/1603.08983v6), **§2.2 “Error Gradients”** and **§3.5 “Wikipedia Character Prediction.”** Both passages were read in versioned HTML; this is not a new full read of all synthetic experiments.

§2.2 explicitly says the ponder cost is discontinuous when N(t) changes and that gradients ignore these discontinuities by treating N(t) as constant. This supports the card's qualification of “differentiable,” without establishing training failure. §3.5 explicitly supplies **one byte per input timestep, next byte as target, 256-class softmax**, 500-byte sequences with reset state, and training-set error reporting. It says ACT/non-ACT errors are fairly similar and the benefit of extra computation appears slight for this task.

Safe wording:

> ACT learns how much recurrent computation to perform before advancing one byte; it does not shorten the byte stream. In its Wikipedia experiment, errors are reported on training data and are broadly similar with and without ACT. Its practical gradient ignores discontinuities in the halting step count, and ponder cost is not measured serving latency.

Do not call punctuation-associated ponder peaks learned segmentation boundaries, a held-out BPB gain, or a globally smooth exact gradient of the discrete stopping time. No new quantitative curve reading or held-out test was performed here.

### 3.2 Reformer: three resource interventions, not semantic chunks

Card: [Reformer](../03_reading/FIELD_ADDENDUM/arxiv_2001.04451v2.md). Primary: [2001.04451v2](https://arxiv.org/html/2001.04451v2), **§2 shared-QK/LSH/causal masking, §3 Eqs.7–10, §5 and Figure 5 caption**, plus Appendix A's duplicate-count/masking description. Two document snapshots were paginated to their end; the displayed complexity-table extraction is malformed and is not used to certify exact cells.

Confirmed distinctions:

1. LSH approximates which positions attend, using hashes, sorting and chunks; it does not merge text positions. Shared query/key projections are a **projection-sharing axis**, not lexical input/output tying.
2. Reversible paired residuals reconstruct activations for backward computation. The component attention and feed-forward functions do not themselves need to be invertible. This is not evidence of a tied generative encoder/decoder or eliminated inference cache.
3. Position-wise FFN chunking changes peak execution intermediates while retaining the position-wise computation. It is not semantic chunking or fewer byte predictions.
4. §2 says the full-attention baselines use memory-efficient recomputation, not necessarily a naively materialized quadratic matrix. §5/Figure 5 right describes attention evaluation as sequence length varies with total token count fixed, not incremental autoregressive serving. The largest Reformer runs lack equally large full-attention baselines; the reported longer tuned enwik8 run reaches 1.05 bits/dim.

Safe wording:

> Reformer retains sequence positions while approximating attention connectivity and reducing depth-dependent training-activation storage through reversible blocks and feed-forward chunking. Its attention-evaluation scaling and byte-text results do not establish matched-quality cached-serving speedups; QK sharing is separate from embedding/readout tying.

The card's exact enwik8 encoding/output-alphabet unknown remains appropriate: the dataset name alone is not a fresh certification of a 256-way readout. Paper causal masks are a specification, not an implementation/cache audit.

## 4. MTPC: declared algorithm, derivation and implementation are separate

### 4.1 What the actual fixed original says

Card: [R05/BIW-0079](../03_reading/R05/BIW-0079.md), BIP-0173. Primary: **[2511.11346v2](https://arxiv.org/pdf/2511.11346v2), Appendix F pp.19–21**; retained [text](../03_reading/R05/sources/BIW-0079.txt), lines **1130–1240**. I read that entire range and additionally read the public PDF's **Algorithm 2 p.20 and Algorithm 3 p.21 visually**, including the rejection and final-token branches. The relevant wording is in the PDF, not just extraction damage.

- Appendix F p.19 says only the zero-acceptance case keeps the “free” verifier token; after any acceptance, the verifier's last shared state seeds the next draft.
- Algorithm 2 p.20 says “Obtain up to n+1 tokens from speculative decoding,” then branches on **0 tokens accepted**. The else branch says **“Accept n tokens (drop ‘free’ token)”** and retains the hidden state for the last accepted token. It does not explicitly carry a residual distribution into the next cycle. The reuse of n in that branch is also ambiguous against the earlier fixed window n; it should not silently become a precise implementation specification.
- Algorithm 3 p.21 lines **14–23** count accepted proposals s. Lines **25–29**, for **s<n**, sample from the normalized positive residual `max(p−q,0)`. Lines **30–31**, for **s=n**, sample an ordinary target token. Line **33** returns the accepted prefix plus that final token. The Appendix F reference to “lines 23–30” does not erase the two different distributions in the final block.

Even reading Algorithm 2 charitably as retaining **s accepted proposals**, not all n proposals regardless of rejection, its described omission conflates an all-accepted bonus with a post-rejection correction. That is the source-level objection. It does not depend on proving an erroneous array index in released code.

### 4.2 What can be derived without running the implementation

At a fixed prefix, let target and actual proposal conditionals be p and q. Proposal-and-accept mass for symbol y is

```text
a(y) = q(y) min(1, p(y)/q(y)) = min(p(y), q(y)).
R    = 1 − Σ_y a(y).
r(y) = [p(y) − q(y)]_+ / R, if R>0.
a(y) + R r(y) = p(y).
```

Thus the rejection residual supplies the missing target mass. An optional all-accepted bonus is not this residual. The ratios must use the actual transformed proposal and the target policy intended for preservation; a normalized multi-byte circuit by itself does not prove the wrapper correct.

**Finite-prefix counterexample to a specified interpretation, not to measured software:** take a two-proposal window. Proposal 1 is deterministic and accepted under identical target/draft conditionals. At position 2 let `p=(0.5,0.5)` and `q=(0.9,0.1)`. Accepted mass is `(0.5,0.1)` and rejection probability is `0.4`. Emitting the proper correction adds `(0,0.4)`, recovering `(0.5,0.5)`. If the partially accepted cycle discards that correction and **restarts an ordinary fresh target-law cycle at the retained prefix**, its next-symbol contribution is instead `0.4p=(0.2,0.2)`, giving `(0.7,0.3)` overall.

This demonstrates that the stated discard-and-ordinary-restart interpretation **need not** preserve the target law. It is not a claim that every cache optimization without an immediately emitted correction must fail. Retained residual state, an equivalent correction protocol, or a different actual wrapper can change the conclusion. Keeping only a hidden state for the accepted prefix is not, on its own, a stated record of the rejected proposal/correction law.

### 4.3 What remains unknown

No fixed implementation, rejection branch, checkpoint or run trace was inspected or executed in R2. **The released implementation's behavior is unknown, not demonstrated broken.** The card's FULL status is not rescinded: reading a source does not certify its correctness or require reproducing all software. Greedy identity is separate from stochastic distribution preservation; this sampling counterexample is not a proof of a greedy mismatch.

Safe author wording:

> The circuit supplies a normalized dependent draft, and Algorithm 3 specifies ordinary speculative residual correction. The optimized shared-state Algorithm 2 describes dropping the final verifier token after any proposal acceptance without distinguishing the all-accepted bonus from a post-rejection correction or specifying retained residual state. A literal discard-and-ordinary-restart reading need not preserve the stochastic target law. Exactness of the optimized wrapper remains unverified; this does not establish an error in released software or invalidate the reported throughput measurements.

Prohibited: “MTPC's implementation is biased/broken”; “the residual is optional because the draft is normalized”; “Algorithm 3 proves Algorithm 2”; “the timing results therefore vanish”; applying a stochastic argument to greedy output identity without a separate argument.

**Closure evidence:** fixed code/version and run linkage; partial acceptance (`0<s<n`), zero acceptance and all-accepted branches; emitted symbols, retained probability state and cache alignment; actual p/q transformations; and a finite-prefix law argument for the optimized protocol. A new training run is neither needed nor authorized. Until closure, replace the existing card's “normally drops the bonus token” shorthand with the bounded paragraph above wherever an exact stochastic guarantee is invoked.

## 5. TokSuite: the expression is checked; Figure 6 computation is not

Primary: **[2512.20757v2 PDF p.21, Appendix C.2 and Figure 6](https://arxiv.org/pdf/2512.20757v2#page=21)**. I visually read the C.2 paragraph and the complete displayed Figure 6/caption in this follow-up. C.2 says BPB normalizes cross-entropy by **`log₂|V|`**, and uses similar curves to suggest comparable training and attribute downstream differences to tokenizers. Figure 6 is labeled “Bit-per-Byte (BPB) during training”; reading its label/curves does not identify its computation.

For a matching set of scored events, total negative log probability `L_nats`, valid scored-event count N and original-byte denominator B:

```text
byte-normalized event score = L_nats / (B ln 2)
                           = CE_mean_nats × N / (B ln 2).
```

A vocabulary-size factor does not supply the token-to-byte event ratio. A uniform model on 256 individual byte values has **8 bits/byte**; dividing its bit-valued CE by `log₂256=8` gives 1, not 8. A wrong explanatory expression can coexist with a correct plot, so this calculation does **not** identify what Figure 6 actually used.

[DISCOVERY_CORRECTIONS §5.1](DISCOVERY_CORRECTIONS.md) already reports a static inspection of three files at commit **0db0ba5648a4fa4efae010a94f69fc1042a354aa**: trainer `loss/out`, model loss call, and natural-log token cross-entropy helper. **That code evidence is attributed, not independently repeated or counted here.** It did not locate Figure 6's plotting transformation, raw logs, byte counts, smoothing/aggregation or paper-run commit mapping. R2 supplies no new fixed plotting artifact. Those missing links remain genuinely unknown, not an assertion that the whole repository lacks a conversion.

Safe author wording:

> TokSuite v2 C.2 describes a vocabulary-size normalization that is not a general conversion to bits per original byte. The wording is present in the PDF, but Figure 6's actual log-to-BPB transformation and run provenance remain unverified. We do not use that figure to certify cross-tokenizer BPB equality or equal training sufficiency. This does not by itself invalidate the separately defined option-ranking evaluation or the four-tokenizer source-text control.

Prohibited: “Figure 6 is proven to divide by log₂|V|”; “the figure is repaired because we supplied the right formula”; all TokSuite task scores are invalid; similar correctly computed BPB alone proves equal downstream capability or isolates tokenizer causality.

**Closure evidence:** original plotting/evaluation code, immutable revision, log fields and bases, valid event and byte totals, PAD/EOS/prompt/repeated-target accounting, language/sample weighting, smoothing, and run→figure mapping. Canonical token-path scores can legitimately be byte-normalized if labeled as such; a changed denominator does not turn them into marginalized string or arbitrary byte-prefix probabilities. Keep the numerator's event identity explicit.

## 6. MYTE: resolve the row/column mapping, retain the source-summary gap

Card: [R07/BIW-0104](../03_reading/R07/BIW-0104.md), Results fourth bullet, still reads “LR/overall ... 21.8/21.1 ... 23.1/21.9” at review time. Primary: [2403.10691v2](https://arxiv.org/pdf/2403.10691v2). I visually read the retained **[p.17 Table 8](../03_reading/R07/sources/BIW-0104-p17.png)**, including its language columns/C.2 continuation, and **[p.7 Table 4](../03_reading/R07/sources/BIW-0104-p7.png)**.

Table 8 puts **MyT5 first and ByT5 second**, unlike Table 4's baseline-first row order. Its last columns are **AVG LR, AVG**, in that order:

| Printed Table 8 model row | AVG LR | AVG |
|---|---:|---:|
| MyT5 | 21.1 | 21.8 |
| ByT5 | 21.9 | 23.1 |

Both Table 8 aggregates favor ByT5. The current card has the **two aggregate columns reversed**, not evidence that the model names in the PDF should be swapped. Table 4 separately gives **ByT5 20.1, MyT5 20.4** under its low-resource MT summary. The exact row/column transcription is settled. **The relationship of the reported populations/aggregations remains unreconciled**: an LR label alone does not certify identical evaluated populations across tables, and no documented bridge justifies silently replacing one summary with the other.

C.2 names fourteen languages; Table 8 has fifteen language columns including **`mt` (Maltese)** and **`sn` (Shona)**. C.2 instead names **Marathi** and omits Shona. This supports retaining an evaluated-set question, not choosing which set actually ran. No new runtime evidence was recovered. R1's separate Eq.1 sign/log-base qualification is retained by reference, not freshly checked here.

Safe author wording:

> MYTE v2 Appendix B Table 8 reports low-resource/overall MT means of 21.1/21.8 for MyT5 and 21.9/23.1 for ByT5. Both favor ByT5, whereas main Table 4's low-resource summary is 20.4 versus 20.1 in favor of MyT5. The reported sets/aggregations are not reconciled, and the appendix language list also differs. We therefore attribute each number to its table rather than report a single resolved MT ranking.

Prohibited: reverse the model rows by following baseline-first convention; call 21.8 the MyT5 LR mean; compare an overall mean with an LR mean as identical; silently average tables; infer no useful multilingual compression from an MT reporting gap. MYTE code bytes, target UTF-8 bytes and parallel-English-byte normalization remain different units.

## 7. Hourglass: residual dependence survives the simplified independence argument

Card: [R03/BIW-0072](../03_reading/R03/BIW-0072.md), architecture paragraph still contains the blanket conditional-independence sentence at review time. Primary: **[2110.13711v2](https://arxiv.org/html/2110.13711v2), §2.2, Algorithm 1, Appendix A.1 and Table 9**. The original HTML was paginated to the carrying appendix after a viewport snapshot cut off its explanation.

Main §2.2 writes a simplified no-fine-layer factorization through prior shortened groups. **A.1 explicitly includes input embeddings shifted by one through the residual.** Table 9's caption says the model can use both those residual inputs and shortened embeddings. In the `L#L` example, prediction of the copied L at position 3 gets the immediately previous `#` and an old shortened state, but not the needed L two positions back. Adding a local fine-resolution attention layer can express that particular dependency.

Therefore the paper supports a **restricted-context expressivity limitation**, not independence from every earlier symbol in the current group for the architecture with that residual. The source's main-text simplification and appendix must be read together. This is not evidence of future leakage or a failed causal generator.

Safe author wording:

> Without fine-resolution Transformer layers, the shortened branch lacks current-group history, while the shifted-input residual can still convey the immediately previous symbol. Appendix A.1 exhibits a copying dependency that this restricted access cannot express; a fine-resolution attention layer removes that restriction in the construction, not a guarantee of learned success on arbitrary tasks.

Prohibited: “All within-group symbols are conditionally independent given past groups” as a blanket description of the residual architecture; “one fine layer guarantees every long-range dependency”; inferring a causal-mask bug from this expressivity example. The separate k−1 shift obligation remains; all pooling information paths must respect visibility, not only queries.

## 8. Reading depth: designated partial scope is not failed full reading

The [FIELD_ADDENDUM summary](../03_reading/FIELD_ADDENDUM/BATCH_SUMMARY.md) distinguishes **2 FULL + 2 designated PARTIAL**. This audit preserves that accounting but does not independently certify every full-reading action.

| Evidence situation | Accurate status and consequence |
|---|---|
| [ELMo](../03_reading/FIELD_ADDENDUM/arxiv_1802.05365v2.md): designated §§1–3.4/Table 1 extraction | PARTIAL by design. §§4–6 and supplement are not fully audited. Character-composed word input/word output and directional sharing can be used within the stated scope; no full-paper or byte-generation credit. R2 read the card, not the original anew. |
| [GPT-2](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md): designated report p.4 §§2.2–2.3/adjacent §3.1 | PARTIAL by design. Rest of report, results and appendix remain outside that check. Byte-based BPE is not raw next-byte output. Do not say the full report omits a budget merely because that budget was not examined. R2 read the card only. |
| A requested complete read stops before method/experiments/relevant appendix | PARTIAL, with exactly the unread range named; BLOCKED only when an actual access obstacle applies. Do not relabel this as a completed designated narrow assignment after the fact. |
| Full source read, but authors omit a runtime detail or publish ambiguous pseudocode | Source reading can remain FULL; the affected guarantee is unknown or qualified. MTPC exact optimized sampling is the present example. |
| Complete paper read, but no code/weights/run provenance checked | Paper reading does not imply runtime certification. The implementation field remains unverified, not “false” or “failed full read.” |
| R2's designated passage audit | Targeted independent check; **0 new FULL**. It neither closes unexamined terra scopes nor downgrades a source solely because a separate artifact claim remains unknown. |

For the six nonsampled R09/R10 originals, the newly supplied cards are useful evidence records, but this audit does not independently verify their entire source claims. In particular AU-Net prefix stability, the REINFORCE BPE guide, Strawberry scaling and the SpellingBee intervention remain attributed to their cards here, not promoted to newly checked results.

## 9. Adoption queue and remaining closure

Only these two review files are written. The following are **instructions to the existing owners**, not claims of edits already applied.

1. **Correct the new R10 prose-sign attribution.** In BIW-0134's paragraph after the correlation table and R10 summary item 2, replace the categorical TP contradiction claim with: “Table 8 explicitly gives Llama DI TP −0.380 and IP +0.268; a later positive-correlation sentence may refer to IP. Attribute signs to the named columns rather than assert a definite contradiction.” Keep all coefficients and task-dependent findings.
2. **Apply the still-outstanding MYTE and Hourglass card fixes** from §§6–7 and propagate only to affected inventory/synthesis statements. Do not add works or FULL counts.
3. **Add MTPC's optimized-sampling qualification** to BIW-0079/BIP-0173 wherever exactness is asserted. Keep circuit normalization, measured acceptance and throughput distinct from wrapper-law verification.
4. **Keep TokSuite T1 open.** A fresh PDF expression check is progress in provenance, not recovery of the actual plotting pipeline. Withhold the Figure 6 equality/training-sufficiency inference; do not erase independent evaluations.
5. **Preserve the meaningful new negative evidence:** Sparse Transformer strided text quality; ACT's training-only near-tie; T-FREE candidate dependence/noninjectivity qualification; task-dependent dialect signs. No common matched-quality serving comparison is established by combining these sources.
6. **Do not replace terra's full reading with this audit.** Request a narrowly specified artifact clarification only when the affected guarantee is needed; avoid another whole-paper read just to discover that an author never reported a runtime field.

## 10. Access and verification record

Original-source access used public, version-locked URLs or existing project-assigned extracts/page images. No web searches were necessary: the supplied cards already fixed the source identities. No installation, training, experiment, third-party paper-code execution, commits, uploads, new downloads or conversion files were used. The probability examples are analytic checks; a standard-library arithmetic check is not a software reproduction.

One new built-in-browser tab was reused for ACT, Reformer, Hourglass, TokSuite and the MTPC PDF, then closed. Other tabs were left untouched. The existing browser had 73 tabs; more than ten crowds the sidebar. Reformer and Hourglass text snapshots were followed with their continuation cursors. One malformed cursor request was corrected; it did not produce source evidence. Two HTML screenshot attempts timed out on separate documents. TokSuite HTML scanning did not expose C.2; the normal public PDF viewer then allowed direct reading of p.21 and Figure 6. No authentication/access controls were bypassed. Browser-managed screenshot caches are not project download artifacts and are not counted as retained sources.

Deliverable verification is UTF-8 decoding, local-link existence, explicit sample counts, required issue coverage, arithmetic and repository-status observation; no build or pytest run is appropriate for these two literature-review documents. Because the survey tree was already untracked, `git status` cannot itself prove per-file provenance or rule out concurrent edits. This task's write targets are exactly **FULL_READING_AUDIT_R2.md** and **CLAIM_RULES.md**; all cards, inventory, PLAN, R1 and project-wide registries remain untouched by this task.

**Bottom line:** the audit supports useful bounded field evidence, confirms the two outstanding R1 card corrections and the source-level MTPC concern, retains TokSuite's unknown figure pipeline, and newly corrects an overconfident attribution of the dialect paper's “positive” sentence. None of these findings establishes a broken released implementation or supplies missing full-reading/serving evidence.

### Checks actually run

A read-only Python 3.14 standard-library check passed UTF-8 decoding/no replacement characters, balanced fenced blocks, required issue coverage, **49 local Markdown links** and the cross-document heading anchors used here. It confirmed **exactly two explicitly designated R09 original-source samples and two R10 samples**. Arithmetic returned the MTPC interpretation's `(0.7, 0.3)` versus corrected `(0.5, 0.5)`, identical distinct trigram sets for the two T-FREE strings, and `22.986657` word perplexity from rounded LM1B BPB/event counts. These checks validate document structure and the stated small analytic examples, not paper software or empirical results. They created no project files or logs. Repository status was checked before and after; the pre-existing untracked directory-level entries remained, so no per-file concurrency guarantee is inferred from Git status.
