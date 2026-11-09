# Claim rules for the byte-language-interface survey

2026-11-09. Adoption rules from the independent [R2 evidence audit](FULL_READING_AUDIT_R2.md), read together with [R1](FULL_READING_AUDIT_R1.md) and [PLAN](../PLAN.md). This file gives author-ready wording and prohibited inferences; it does not change reading cards, inventories or completion counts. R2 performed designated primary-source checks on 10 works and takes **0 new FULL credits**.

## 1. Claim form and evidence states

A substantive comparison should identify **work/version → input/internal/output/supervision units → probability or task event → measured result → population/budget → source location**. Put each material condition once beside the affected conclusion. Do not bury the useful finding in repeated generic caveats, or use a caveat to excuse an unsupported headline.

Keep the following evidence states separate:

| State | What it establishes | What it does not establish |
|---|---|---|
| Paper specification | What the fixed text/formula/pseudocode declares | The exact implementation, trained tensor aliases or executed run |
| Analyst derivation | A consequence or counterexample under explicit assumptions | That the authors ran that interpretation or suffered measured harm |
| Fixed configuration/static code | Behavior or switches at a named immutable artifact revision | That the artifact generated the paper's result, or a runtime alias without checking it |
| Run-linked runtime verification | A behavior in the identified actual run | A universal property across ports, versions, decoding transforms or hardware |
| Reporting discrepancy | Different printed values/descriptions for the stated contexts | Which value generated the experiment; that the mechanism failed |
| Unknown/not verified | The boundary of available evidence or this review | A negative value, absence of a mechanism, access failure or broken software |

**Reusable wording:** “The paper specifies X; its actual implementation/run behavior was not verified.” Use “not reported in the examined scope” for a narrow read, and “not examined” when the relevant part was never read. Reserve “not reported in the paper” for a sufficiently complete source inspection.

**Prohibited:** converting a formula into a runtime claim; inferring an actual bug from missing pseudocode; treating an analyst toy example as a reproduction; declaring a whole study invalid from a single unclear field. Equally, do not treat FULL as a certificate of a theorem, sampler or software implementation.

## 2. Units, probability objects and normalization

### 2.1 Name all four interfaces

Use separate fields for **input, internal positions, output and supervision**. Character, code point, grapheme, UTF-8 byte, learned code byte, subword, word and annotation event are not synonyms.

Examples that may be written:

- “ACT's Wikipedia model advances through individual bytes and allocates extra transitions within a byte.” [ACT §3.5](https://arxiv.org/html/1603.08983v6#S3.SS5).
- “T-FREE uses rule-derived units and candidate-selected whole-unit outputs, not native next-byte prediction.” [T-FREE §§3.1–3.2, Algorithms 1–5](https://arxiv.org/pdf/2406.19223v2); [card](../03_reading/R10/BIW-0127.md).
- “ELMo is a character-composed word-position/word-output antecedent; GPT-2's byte-based BPE predicts merged symbols.” These are **card-attributed designated partial checks**, not fresh original-source verifications in R2: [ELMo](../03_reading/FIELD_ADDENDUM/arxiv_1802.05365v2.md), [GPT-2](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md).
- “Sparse Transformer and Reformer retain positions while changing attention connectivity/execution; neither thereby learns byte segmentation.” [Sparse Transformer §7.2](https://arxiv.org/pdf/1904.10509v1); [Reformer §§2–3](https://arxiv.org/html/2001.04451v2).

**Prohibited:** raw-byte language-model evidence from a character probe or byte-complete subword vocabulary; a Unicode readout alphabet inferred only from an enwik8 label; native UTF-8-byte likelihood from MYTE's learned code bytes; task accuracy from gold-answer BPB.

### 2.2 Valid byte-normalized accounting

For the **same scored events** and matching byte denominator:

```text
L_nats = −Σ_i ln q(e_i | c_i)
score_bits_per_original_byte = L_nats / (B ln 2)
                             = CE_mean_nats × N / (B ln 2).
```

N is the effective count in that CE average, not padded array length. B must correspond to the scored original text, with prompt, EOS, normalization, repeated-window and masking conventions stated. If logs are already bits, omit division by ln 2. Aggregate matching loss totals and byte totals; do not silently average differently weighted per-example ratios. Auxiliary/composite/smoothed objectives must not become ordinary NLL without recovering the relevant numerator.

**Safe wording:** “We report the canonical token-path negative log probability normalized by matching original-byte count.” This can be legitimate transparent accounting. It does **not** imply marginalization over all tokenizations decoding to the text. A marked boundary-event path, a denoising conditional, a native byte chain, a completed-string marginal and an arbitrary partial-token byte-prefix conditional remain different probability objects.

For [BIW-0071](../03_reading/R09/BIW-0071.md), [1908.10322v1 §3.2/Table 1/Eq.3](https://arxiv.org/pdf/1908.10322v1) permits re-expression of the **same processed-corpus likelihood** as `PPL_word = 2^(BPB × 826189/159658)`, using word-EOS and byte-newline conventions. It does not restore rare words already replaced by UNK or establish a raw-original-text marginal.

**Prohibited:** CE divided by vocabulary-size logarithm as a general BPB conversion; alternate-tokenization probability sums obtained by merely changing a denominator; English-byte normalization substituted for target-language-byte normalization; equal units equated with equal exposure or compute.

## 3. MTPC: exact source-level qualification, not a software verdict

**Evidence:** [2511.11346v2 Appendix F pp.19–21, Algorithms 2–3](https://arxiv.org/pdf/2511.11346v2); [retained extract lines 1130–1240](../03_reading/R05/sources/BIW-0079.txt); [R2 §4](FULL_READING_AUDIT_R2.md#4-mtpc-declared-algorithm-derivation-and-implementation-are-separate). Algorithm 2 p.20 and Algorithm 3 p.21 were also visually checked in the original PDF.

### Author-ready paragraph

> MTPC's circuit supplies a normalized dependent draft, and Algorithm 3 specifies ordinary speculative residual correction. Its optimized shared-state Algorithm 2 describes dropping the final verifier token after any proposal acceptance without distinguishing the all-accepted bonus from a post-rejection correction or specifying retained residual state. A literal discard-and-ordinary-restart reading need not preserve the stochastic target law. Exactness of the optimized wrapper remains unverified; this does not establish an error in released software or invalidate the reported throughput measurements.

### Required distinctions

- **Declared Algorithm 3:** proposals are accepted by actual conditional p/q; for `s<n`, its lines 25–29 sample normalized `(p−q)+`; for `s=n`, lines 30–31 sample an ordinary target bonus. The two branches have different mathematical roles.
- **Declared Algorithm 2:** zero acceptances keep a verifier token; the else branch drops a “free” token and keeps the last accepted shared state. It does not explicitly describe correction-state carry-over. Its “Accept n tokens” wording is ambiguous against the fixed draft window; do not repair the notation and certify the result without saying so.
- **Derivation:** with accepted mass `min(p,q)`, the residual restores target mass. R2's deterministic-first-proposal/two-symbol example gives `(0.7,0.3)` rather than `(0.5,0.5)` under a specified partial-acceptance discard-and-ordinary-restart interpretation. This is analytic, not an executed paper sampler.
- **Actual implementation:** no fixed code branch/run has been verified in R2. It might implement a different or corrected protocol. Its behavior is **unknown**.

### Prohibited inferences

“MTPC's released code is broken/biased”; measured output bias; a failure of normalized probabilistic circuits; proof of the optimized wrapper from the ordinary Algorithm 3 identity alone; a greedy mismatch established by the stochastic counterexample; invalidated timings from an unverified law guarantee. Conversely, normalization of the draft and good acceptance do not close the wrapper guarantee.

### What would close the guarantee

Identify fixed implementation/version and paper-run linkage; show all of zero-, partial- and all-accepted branches, actual output/correction state and cache alignment; name target/proposal transforms; give a finite-prefix probability argument. No training or new generation experiment is required by this review. Until then, keep the qualification attached wherever “exact stochastic decoding” is asserted. The source may remain FULL while this guarantee remains open.

## 4. TokSuite: exclude an unverified figure inference, not the whole study

**Evidence:** [2512.20757v2 PDF p.21 C.2/Figure 6](https://arxiv.org/pdf/2512.20757v2#page=21), freshly read visually in R2; [DISCOVERY_CORRECTIONS §5](DISCOVERY_CORRECTIONS.md) for previously inspected trainer files at immutable commit `0db0ba5648a4fa4efae010a94f69fc1042a354aa`. The three-file static-code inspection is **attributed prior evidence**, not repeated by R2.

### Author-ready paragraph

> TokSuite v2 C.2 describes BPB using cross-entropy normalized by log₂|V|, which is not a general conversion to bits per original byte. The wording is present in the PDF, but Figure 6's actual transformation and paper-run provenance remain unverified. We therefore do not use Figure 6 to certify cross-tokenizer BPB equality or equal training sufficiency. This issue does not by itself invalidate the separately defined option-ranking evaluation or the four-tokenizer source-text control.

### Prohibited inferences

- Figure 6 **actually** implements the printed normalization merely because the text says so.
- The figure is now validated/repaired because a reviewer supplied the correct BPB expression.
- The three inspected trainer files lack byte normalization, therefore no plotting conversion exists anywhere.
- The public inspected commit necessarily generated the paper's runs.
- Similar loss curves, even with correct units, prove equal downstream ability or isolate tokenization as the only causal difference.
- Every multiple-choice result, exact-byte side evaluation or exposure control is invalid because C.2 has a metric-description problem.

**Open closure:** immutable plotting code plus raw log fields/base, event and byte totals, language weighting, EOS/PAD/prompt/overlap accounting, smoothing and run→figure mapping. Until supplied, say **“actual Figure 6 computation unknown,” not “established Figure 6 implementation error.”**

## 5. MYTE: explicitly anchor both model row and aggregate column

**Evidence:** [2403.10691v2](https://arxiv.org/pdf/2403.10691v2), [p.17 Table 8/C.2](../03_reading/R07/sources/BIW-0104-p17.png), [p.7 Table 4](../03_reading/R07/sources/BIW-0104-p7.png); [R2 §6](FULL_READING_AUDIT_R2.md#6-myte-resolve-the-rowcolumn-mapping-retain-the-source-summary-gap).

### Author-ready paragraph

> Appendix B Table 8 reports low-resource/overall MT means of 21.1/21.8 for MyT5 and 21.9/23.1 for ByT5. Both favor ByT5, unlike main Table 4's low-resource summary of 20.4 versus 20.1 in favor of MyT5. The relationship between the reported sets/aggregations remains unresolved, and the appendix language list also differs. We attribute each result to its table rather than claim a single reconciled MT ranking.

Table 8 has **MyT5 first, ByT5 second** and **AVG LR before AVG**. Table 4 has baseline-first rows. The current card's LR/overall means are transposed; do not silently swap model labels as an alternative “repair.” `mt` and `sn` in Table 8 are Maltese and Shona, not Marathi and an omitted column. C.2's fourteen names do not directly match the fifteen language columns.

**Prohibited:** 21.8 as MyT5's LR mean; comparing overall to LR as if the same average; averaging the two tables to manufacture agreement; selecting whichever sign suits the narrative; declaring morphology-driven transcoding useless from inconsistent MT summaries. The sign/log-base issue in Eq.1 remains a separately attributed R1 qualification, not evidence that reported experiments computed negative surprisal. MYTE's parallel-English-byte denominator is not ordinary per-target-UTF-8-byte BPB.

**Closure:** author/artifact clarification of evaluated language sets, aggregation and runs. The row/column transcription correction itself is already closed and does not require another full read.

## 6. Hourglass: restrict the independence claim to the information path

**Evidence:** [2110.13711v2 §2.2, Algorithm 1, Appendix A.1/Table 9](https://arxiv.org/html/2110.13711v2#A1.SS1); [card](../03_reading/R03/BIW-0072.md). R2 read the carrying appendix explanation, not just its example table.

### Author-ready paragraph

> Without fine-resolution Transformer layers, Hourglass's shortened branch lacks current-group history; its shifted-input residual can still convey the immediately previous symbol. Appendix A.1 gives a copying dependency that this restricted access cannot express. A fine-resolution attention layer removes that restriction in the construction, not a guarantee of learned success on arbitrary tasks.

**Prohibited:** blanket within-group conditional independence for the architecture that retains the residual; no access to **any** within-group history; arbitrary dependency/accuracy guarantees from one fine layer; causal leakage inferred from the copying failure. Retain the extra k−1 shift before shortening and check all pooling operands/information paths when making a causality statement. Expressivity and information leakage are different questions.

## 7. New R10 clarification: do not manufacture a dialect TP prose contradiction

**Evidence:** [formal dialect paper §5.2 pp.23997–23998 and Appendix F Table 8 p.24009](https://aclanthology.org/2025.emnlp-main.1224.pdf), [retained text lines 270–319](../03_reading/R10/sources/BIW-0134.txt), [Table 8 image](../03_reading/R10/sources/BIW-0134-p18.png). This refines the current [BIW-0134 card](../03_reading/R10/BIW-0134.md) and [R10 summary item 2](../03_reading/R10/BATCH_SUMMARY.md); those files are not edited here.

### Author-ready paragraph

> The dialect study reports task-dependent correlations rather than a causal tokenizer intervention. In Table 8, DI tokenization-parity correlations are +0.638 for Phi, +0.4836 for mBERT and −0.380 for Llama; Llama DI information parity is +0.268 and Phi's is −0.413. A later sentence describing a positive Llama correlation follows discussion of information parity, so it does not unambiguously contradict the TP column. We attribute each sign to its named metric.

§5.2 first explicitly says the Llama TP relation is negative. The next-page positive sentence can refer to IP. The old categorical source-conflict assertion must therefore be weakened to that referent distinction; the actual table coefficients do not change.

**Prohibited:** definite TP sign contradiction from an ambiguous pronoun/referent; significance or effective paired n inferred from available language counts; fragmentation causally improves fairness; printed Latin-like byte symbols prove irreversible corruption. §5.3 itself says decoding may reassemble proper Unicode. Tokenization parity, information parity and task score are different measures, and adapter/full-tuning budgets must not become equal-compute controls.

## 8. ACT and Reformer: keep positive mechanisms and real evidence limits

### ACT

**Author-ready:**

> ACT learns repeated recurrent computation within each byte position rather than shorter byte segments. Its Wikipedia experiment reports training-set errors that are fairly similar with and without ACT. The gradient treatment ignores stopping-count discontinuities; the ponder penalty is not measured wall-clock or serving cost.

Source: [1603.08983v6 §2.2/§3.5](https://arxiv.org/html/1603.08983v6), [card](../03_reading/FIELD_ADDENDUM/arxiv_1603.08983v6.md).

**Prohibited:** held-out byte-quality gain; punctuation peaks as validated semantic boundaries; globally exact smooth differentiation of the discrete halting count; count proxy as energy/latency; declaring the method broken because its gradient is approximate.

### Reformer

**Author-ready:**

> Reformer retains sequence positions while approximating attention connectivity, reconstructing activations with reversible residual blocks and chunking position-wise feed-forward execution. These address attention and training-memory costs, not learned segmentation. Its attention-evaluation timing is not a matched-quality cached-serving benchmark, and shared QK projections do not establish lexical input/output tying.

Source: [2001.04451v2 §§2–3/§5/Figure 5](https://arxiv.org/html/2001.04451v2), [card](../03_reading/FIELD_ADDENDUM/arxiv_2001.04451v2.md).

**Prohibited:** semantic chunks from execution chunks; reversible components individually invertible; no inference cache because training activations can be reconstructed; every large run has an equally large full-attention control; approximate attention guarantees all exact nearest neighbors; all baseline attention matrices were naively materialized. Keep this distinct from R09's fixed-pattern Sparse Transformer.

## 9. Costs, causality, sharing and association: cross-paper rules

### Cost controls

Write “equal source-text exposure,” “equal model positions,” “equal total parameters,” “equal active parameters under the paper's convention,” “estimated training FLOPs,” or “measured wall time” only when that specific control is present. None substitutes for another. Report teacher/tokenizer preprocessing, draft/head size, prefill, cache, resident verifier, precision, device and concurrency when material to the affected result. Unknown is not zero.

**Source-backed example:** [Sparse Transformer Table 2/§7.2](../03_reading/R09/sources/BIW-0118.txt) gives dense/fixed/strided text BPB **1.00/0.99/1.13** and Time/Iter **1.31/0.55/0.35**, with no time unit in the header. Retain the strided negative, do not label seconds or serving latency, and do not generalize its audio million-position demonstration to language. [BIW-0071 §2.2](../03_reading/R09/sources/BIW-0071.txt) describes expensive full-window rescoring; development stride is scoring parallelism, not cached generation.

**Prohibited:** asymptotic attention complexity as all-system serving speed; higher acceptance as necessarily higher throughput; training bytes/s or steps/s as decode latency; a literature table as a controlled causal architecture comparison.

### Causality and offline side information

Causal attention does not prove that preprocessing features are prefix-computable. Distinguish information from the current consumed symbol, future source input, full encoder context and future target. A generic ranked-BPE counterexample refutes a universal prefix-stability claim but does not measure leakage under an actual tokenizer. R09's REINFORCE BPE-guide and R10's AU-Net regex cautions are **card-attributed here**, not newly tested artifacts. Request a prefix argument or fixed-artifact evidence before making a definitive online-causality claim; do not call the published implementation leaky merely because the proof is absent.

### Sharing axes

State the exact pair: input↔output table, two output heads, Q↔K projection, directional representation/softmax, recurrent transition, cross-depth block, shared backbone, adapter, or runtime tensor alias. Reformer QK sharing is not lexical tying; reversible reconstruction is not an encoder/decoder tied inverse. ELMo's designated partial card reports representation and softmax sharing **between directions**, not character-input↔word-output tying. Family inheritance, common initialization and unknown settings must not become shared trained storage or a controlled finding that tying improves bytes.

### Associations and negative findings

A measured association, selected qualitative trace, probe readout and randomized intervention establish different things. Preserve source-specific negative results without promoting them to impossibility theorems. Do not turn a missing measurement into a negative experiment, or erase an inconvenient negative with an unrelated positive budget.

## 10. Reading/completion language

| Situation | Author wording | Forbidden substitution |
|---|---|---|
| Designated ELMo narrow check | “PARTIAL by design: §§1–3.4/Table 1; §§4–6 and supplement not fully audited.” | Failed full read, blocked source, or FULL paper credit |
| Designated GPT-2 narrow check | “PARTIAL by design: report p.4 §§2.2–2.3/adjacent §3.1; remaining report/results/appendix outside scope.” | The whole report lacks a budget because that part was not inspected |
| Requested full read actually incomplete | “PARTIAL: [specific unread sections]; [actual obstacle if any].” | Retroactively renaming an incomplete full assignment as a completed narrow assignment |
| Full paper read, runtime omitted/unverified | “FULL source reading; implementation/guarantee X remains unknown.” | Paper-reading failure, empirical mechanism failure, or runtime certification |
| R2 passage verification | “Independent targeted verification of designated passages; 0 new FULL.” | Replacement for terra, ten fresh full rereadings, or global closure of inventory coverage |
| Source error/referent ambiguity corrected | “Correct the named claim and propagate to affected rows without new work/FULL credits.” | Inflated counts, unrelated card rewrites, or automatic study invalidation |

R2 read all fourteen new cards, but checked original passages for only two R09 and two R10 works plus ACT/Reformer and the four old-issue works. The other six R09/R10 originals and ELMo/GPT-2 are **not independently reverified by R2**. Keep that sampling boundary when reporting adoption or closure.

## 11. Final author checklist

Before accepting an affected paragraph, verify:

1. The claim has an actual versioned source and carrying location, not just a family name or FULL badge.
2. Input/internal/output/supervision units and probability event are explicit where they change the conclusion.
3. Row labels, column labels, task population and denominator match the quoted number.
4. Source specification, analyst derivation and implementation/run evidence have not been merged.
5. Budget and causality conditions sit beside the claim; missing fields remain unknown.
6. MTPC optimized stochastic exactness and TokSuite's actual Figure 6 conversion remain open unless their distinct closure evidence is supplied.
7. MYTE's aggregate order and Hourglass's residual qualification are corrected; the dialect positive-correlation referent is not overclaimed as a definite TP contradiction.
8. Designated partial reading is neither inflated to FULL nor misreported as a failed full read. This review does not replace terra.
9. Field-centered synthesis remains the organizing purpose; any FLUED implications are a final bounded section, not a mechanism verdict inferred from these papers.

Only this file and FULL_READING_AUDIT_R2.md are this task's deliverables. Proposed adoptions elsewhere remain the existing owners' work; no training, reproduction, production edit or broader-survey repair is claimed.
