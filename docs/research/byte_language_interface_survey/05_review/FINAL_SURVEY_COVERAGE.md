# Independent final survey coverage review

2026-11-09. Reviewed release: the 802-line English survey, its executive summary and open questions, and the current canonical inventory. Line references below refer to the saved files inspected in this review; stable section and BIP/BIW anchors remain authoritative if authors subsequently revise them.

## 1. Verdict and acceptance boundary

**Coverage is sufficient for an initial substantial, independent field survey. Recommend localized revision before final translation, not another discovery/full-reading campaign.** There is **no P0 blocker**, **one P1 balance issue**, and **three P2 improvements** below. The P1 concerns the treatment of an already-covered central family, not a missing architecture or a demand for experiments. No additional terra whole-paper reading is necessary to address these findings.

The survey is genuinely broader than a learned-patching catalog. Historical recurrent models, word-local composition, code-point encoders, byte denoisers, full-resolution attention, selective recurrence, sparse/hash attention, activation-memory techniques, latent workspaces, adaptive within-byte depth, causal hierarchies, output laws, pretrained conversion, and multilingual/task evaluation all have substantive roles. Its acceptance does **not** depend on coverage of a local multigranularity proposal, source revisiting, or a preferred future architecture. The absence of a project-implications chapter is not a defect under this independent-field assignment.

Its strongest organizing contribution is the separation of input, internal computation/state, output, and supervision. The problem–solution–technique classification actually drives much of the reasoning: boundary learning is separated from rate control; content aggregation from selected addresses; training signals from executable output laws; and storage savings from whole-system costs. It is not merely a list of names with taxonomy labels attached afterward.

The main imbalance is that some central recent hierarchical methods receive careful mechanism and limitation analysis but almost none of their own positive task-quality evidence. This is repairable using existing readings and the targeted check reported here. The most useful omitted near-control is also already inside ByT5: its character-vocabulary-with-byte-fallback ablation. Neither issue justifies postponing the entire survey for new broad reading.

## 2. What this reviewer actually inspected

### 2.1 Complete text and documentary checks

Read the complete [PLAN](../PLAN.md), [SURVEY_EN](../04_synthesis/SURVEY_EN.md), [EXECUTIVE_SUMMARY_EN](../04_synthesis/EXECUTIVE_SUMMARY_EN.md), [OPEN_QUESTIONS_EN](../04_synthesis/OPEN_QUESTIONS_EN.md), latest [CLAIM_RULES](CLAIM_RULES.md), [TAXONOMY](../02_inventory/TAXONOMY.md), [COUNTS](../02_inventory/COUNTS.md), [FINAL_AUTHOR_COUNTS](../02_inventory/FINAL_AUTHOR_COUNTS.md), [CLASSIFICATION_EN](../04_synthesis/CLASSIFICATION_EN.md), and [VALIDATION](../02_inventory/VALIDATION.md). Inspected the work/depth and detailed-record indexes, the evidence-status census, and the 18 current record bodies specified in §4. Earlier reviews are not treated as independent proof of the present survey's completeness.

Ran read-only Python recounts against the saved Markdown rather than accepting totals in earlier audit prose. Checked all 92 declared FULL carrying-card paths for existence and a declared FULL/full-reading marker. This is a status/identity reconciliation, **not independent reading of those 92 originals**. Checked the thirteen editorial home routes and both distinct relations whose totals happen to be 506. Verified that all eight discovery SEARCH_LOG files exist; did not replay their searches or audit every discovery exclusion.

The survey has 16 numbered sections plus two appendices. A whitespace-token count gives approximately 19,450 words including tables, links and navigation; this is a rough length diagnostic, not a publication word count.

### 2.2 Actual sampling and primary-source boundary

- **18 distinct BIP records / 18 distinct carrying works** were inspected for current problem, solution, technique role, four units, evidence conditions, and correspondence with their paper cards. The sample spans all twelve canonical C families through its overlapping tags.
- **22 distinct cards** were read: those 18, plus H-Net, ELMo, GPT-2, and Perceiver IO as supplementary checks. Reading a card does not create another original-paper FULL credit.
- **Two public primary-source pages received targeted checks in the built-in browser:** H-Net arXiv:2507.07955v2, especially experimental setup and Tables 1–4; and ByT5 arXiv:2105.13626v3, especially §4.4/Table 5 and §6.4/Tables 7–8. These are designated passage checks, not two new FULL rereadings. ByT5's versioned arXiv HTML was checked as such; no byte-identity certification against the separate formal TACL PDF is claimed.
- **Zero new FULL credits, zero executed paper implementations, zero reproduced experiments, zero new source downloads.** No new paper, record, or evidence-status promotion is requested.

The sample is purposeful and cross-family, not random or statistically representative. This review does not independently verify every numeric statement, paper identity, theorem, runtime alias, implementation branch, or the full coverage of literature outside the selected register. Those limits are material to the verdict.

## 3. Prioritized findings: exact claim, evidence, and minimum repair

Priority meanings: P0 would prevent acceptance as an independent initial survey; P1 should be repaired before final translation/publication; P2 is a localized precision, coverage, or editing improvement that does not require holding the survey for new research. Only this review file is edited; the actions below are recommendations to the relevant owners.

### P0 — None found

No missing major family, local-project inclusion rule, inflated independent-experiment count, universal byte-superiority conclusion, or unsupported claim that the paper-reading process certified software was found at a level that blocks this selected initial survey. This is not a statement that every paper claim has been independently verified.

### P1-01 — Restore representative positive quality evidence for the central learned-hierarchy family

**Affected locations:** `04_synthesis/SURVEY_EN.md:254`, `:276`, `:284–286`, `:355`, and especially the H-Net-only efficiency entry at `:667`; the executive summary's grouping account at `04_synthesis/EXECUTIVE_SUMMARY_EN.md:33–35` inherits the imbalance.

**Current treatment/claim:** H-Net's selection, smoothing, surrogate gradient and rate mechanism are explained; BLT supplies the separate entropy-teacher contrast. H-Net's quantitative appearances are mainly its role as the comparator in SOMBRERO/REINFORCE and a statement that the implementation can train about twice as slowly. BLT mainly appears through entropy policy, teacher cost and decoder structure. The reader is not shown a representative native H-Net task-quality result, and receives little direct evidence for why these central recent hierarchy systems are attractive beyond their mechanisms.

**Why this matters:** This is selective emphasis rather than a false number. A survey whose explicit purpose is to explain solutions should show an achieved benefit alongside the strongest control, not make the method's principal quality evidence discoverable only by following its card. The very specific weak or unfavorable comparisons elsewhere make the omission more consequential. A general concluding sentence about useful hierarchies at `SURVEY_EN.md:764` does not replace a source-conditioned positive example.

**Evidence independently checked here:** [H-Net v2 §3/Table 2](https://arxiv.org/html/2507.07955v2#S3) gives, at the XL budget, BPE Transformer average downstream accuracy **55.5** and two-stage H-Net **58.2**, both at reported **0.69 GFLOPs/byte**. Its strong H-Net(space) control gives **57.1** at **0.70**, while one-stage H-Net gives **56.2** at **0.72**. Table 1 lists approximately **1.3B versus 1.6B parameters** for the BPE and two-stage models: this is not equal-parameter evidence. The setup uses the same FineWeb-Edu subset, 8,192 byte positions versus 1,792 GPT-2 tokens, with approximately matched text-per-batch and paper-estimated FLOPs. This does not certify identical retained examples, wall time, or a boundary-only causal effect. Table 4 also gives a direct Chinese comparison, including XWinograd-zh **59.9/62.9/66.3** for BPE/space/two-stage, and essentially tied space/dynamic code BPB **0.3163/0.3161**. These details are already present in the [H-Net card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md), lines 14–17.

**BLT evidence available without new broad reading:** the [conference-version BLT card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md), lines 13–15, already records an 8B equal-training-FLOP comparison, unequal byte exposures/rates, downstream wins and a multilingual reversal. Its cross-attention/version confound at line 14 must stay attached if a boundary claim is made. These BLT passages are card-attributed in this review, not newly primary-verified.

**Minimum repair:** Add one compact achieved-quality comparison in the existing H-Net/BLT discussion, preferably the H-Net Table 2 result with the space and parameter controls in the same paragraph. If expanding BLT, use one version-specific direct result and its actual budget; do not repeat every experiment. Keep the current cost and estimator limits. A brief executive-summary adjustment can then retain the positive evidence without duplicating the numbers. **No additional terra read or experiment is needed.**

### P2-01 — Include the unusually relevant character-vocabulary/byte-fallback near-control

**Affected locations:** `04_synthesis/SURVEY_EN.md:56–60` and `:167–173`; the discussion of changing base encodings at `:553–565` does not supply this same-model alternative.

**Current treatment/omission:** The survey correctly distinguishes code points, bytes, byte-BPE and lexical hybrids, but the ByT5 discussion compares mostly with mT5 and explains the byte recipe. It omits ByT5's own CharT5 ablation: a substantial character vocabulary with byte fallback. CANINE is not a replacement for that near-control because its encoder, masked targets and task interface differ.

**Primary source checked:** [ByT5 v3 §6.4 and Tables 7–8](https://arxiv.org/html/2105.13626v3#S6.SS4) specify **47,198 character entries**, SentencePiece constrained to single-character pieces, and **byte fallback**, so this is not an unrestricted code-point-only model and not a pure byte-step model. CharT5 has **1.23B** total parameters, **36/12** encoder/decoder layers, **d_model=1376**, and about **11%** vocabulary-related parameters. Table 8 gives CharT5 versus ByT5-Large **79.0/79.7 XNLI**, **87.6/87.7 TyDiQA F1**, and **11.2/11.5 GEM-XSum BLEU**. Width and per-text computation differ; the results do not isolate alphabet alone or establish equivalence statistically.

**Why it matters:** This is a strong, directly relevant engineering alternative already in an examined source: shorten non-ASCII text with common scalar-like entries while retaining coverage through fallback. Its near-competitive task results make the representation continuum more concrete than a bytes-versus-large-subwords binary. The survey otherwise handles hybrids well, so this is a localized omission rather than a missing field family.

**Minimum repair:** One short paragraph or table note in §4.5, naming fallback, capacity redistribution and the near-competitive result. There is no need to create a new source entity or claim another FULL. This targeted check is enough for the bounded observation; a new broad reading batch is not justified.

### P2-02 — Name the grapheme-to-phoneme error unit explicitly

**Exact location/claim:** `04_synthesis/SURVEY_EN.md:171`: “grapheme-to-phoneme error 1.8 versus 6.7,” adjacent to explicitly named transliteration character error and morphology accuracy.

**Evidence:** [ByT5 v3 §4.4/Table 5](https://arxiv.org/html/2105.13626v3#S4.SS4) labels grapheme-to-phoneme results **WER/PER**. The Large numbers **1.8 and 6.7 are phoneme error rates (PER)**, not word error rates; the corresponding word error rates are **15.4 and 43.5**. The [existing ByT5 card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md), lines 19 and 23, already distinguishes this.

**Assessment:** The survey's numbers are correct, and it does not explicitly call these two numbers character error. The problem is an underspecified metric, not a confirmed numerical or sign error. A preliminary progress note from this review described a metric-label error too strongly; this final finding supersedes that shorthand.

**Minimum repair:** Specify “phoneme error rate” and a percent convention beside these values. Keep transliteration CER, G2P PER, and inflection accuracy separate. No additional reading is needed.

### P2-03 — Reduce duplicated audit procedure in the main scholarly narrative, not material conditions

**Affected locations:** `04_synthesis/SURVEY_EN.md:369` and `:381` state the MtPC wrapper qualification and then its worked analyst counterexample; `:716`, `:755`, `:781`, `:793`, and `:802` revisit evidence-type or open-guarantee boundaries. The corresponding artifact agenda is fully developed in `04_synthesis/OPEN_QUESTIONS_EN.md:118–165`.

**Current treatment/claim:** The qualification is scientifically relevant and correctly bounded. But the survey repeatedly returns to the review workflow and the distinction between a derivation and a software verdict after it has been made locally and in the methodology. This adds a modest audit-report tone to an otherwise coherent field account.

**Evidence/standard:** [PLAN](../PLAN.md), lines 61–62, and [CLAIM_RULES](CLAIM_RULES.md), line 7, request clear positive prose with a material condition once beside its claim. This is an editorial judgment based on the text, not a new paper-source dispute.

**Minimum repair:** Retain §8's local warning and the distinct probability-law argument. Consider relocating the numerical discard/restart toy example or some procedural closure detail to the linked claim rules/open-question item, and trimming repeated generic evidence-state reminders in late summary prose. Do not remove assumptions, turn “unverified” into “broken,” or hide the limitation only in an appendix. Tables that intentionally consolidate earlier results, such as the efficiency table, are useful repetition and need not be deleted. This is a P2 polish item, not grounds to shorten the survey arbitrarily or reopen its evidence campaign.

## 4. Cross-family inventory-to-card sample

All inventory locations below are within `02_inventory/DETAILED_INVENTORY.md`. These are **18 current-record inspections**, not 18 freshly read original papers. Each linked card was read, and its declared scope was kept separate from the reviewer’s own primary-source checks.

| BIP / inventory lines | Carrying card / family role | Correspondence with English synthesis and finding |
|---|---|---|
| [0003](../02_inventory/DETAILED_INVENTORY.md#BIP-0003), 386–434 | [CANINE](../03_reading/R01/BIW-0004.md), C01/C07 | Hash coverage/collisions, code-point input, distinct C/S targets and optional lexical memorization reach §4.6 accurately. Card's local BIP numbering is not used to override canonical problem identity. |
| [0007](../02_inventory/DETAILED_INVENTORY.md#BIP-0007), 583–629 | [MANTa](../03_reading/R01/BIW-0006.md), C02/C03/C08 | Soft cumulative membership, Gaussian approximation, order-sensitive composition and hard length cap all reach §6.3; no exact segmentation marginal is claimed. |
| [0014](../02_inventory/DETAILED_INVENTORY.md#BIP-0014), 868–909 | [MEGABYTE](../03_reading/R03/BIW-0008.md), C05/C06 | The global-patch and local-byte shifts are separate in §7.1; local autoregression is not independent bulk output. |
| [0019](../02_inventory/DETAILED_INVENTORY.md#BIP-0019), 1065–1101 | [BLT/W0010](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md), C03/C04 | Separate causal entropy teacher, threshold alternatives and lifecycle placement are retained. Direct positive quality evidence is underrepresented: P1-01. |
| [0035](../02_inventory/DETAILED_INVENTORY.md#BIP-0035), 1674–1710 | [Compressive Transformer/W0023](../../flued_multigranularity_survey_20261108/03_reading/B24/W0023.md), C04/C08/C12 | Consumer-aligned attention-response reconstruction and stopped gradients reach §5.3; separately selected compression rates and altered BPTT controls are not called a clean fixed-budget effect. |
| [0039](../02_inventory/DETAILED_INVENTORY.md#BIP-0039), 1825–1863 | [ByT5/W0351](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md), C07 | Table 5 correctly scopes encoder/decoder input sharing and decoder I/O nonsharing to the Large XNLI static configuration. No runtime alias or all-port claim. |
| [0044](../02_inventory/DETAILED_INVENTORY.md#BIP-0044), 2019–2055 | [MambaByte/W0352](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md), C04/C12 | §5.4 gives a genuine full-resolution selective-state alternative and retains unequal training-byte totals; top-three verification is not exact target sampling. |
| [0050](../02_inventory/DETAILED_INVENTORY.md#BIP-0050), 2237–2275 | [Byte Language Models/W0356](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md), C04/C12 | Current first technique field and §13.2 name the 3:1 DeltaNet/attention hybrid, co-varying hashes/convolution/curriculum and active-N exclusions. Not misdescribed as all-attention. |
| [0081](../02_inventory/DETAILED_INVENTORY.md#BIP-0081), 3401–3441 | [2011 MRNN](../03_reading/R02/BIW-0052.md), C02/C04 | §3.1 explains symbol-conditioned factor transitions rather than learned segmentation; transformed-character units and the PAQ control stay explicit. |
| [0085](../02_inventory/DETAILED_INVENTORY.md#BIP-0085), 3562–3603 | [Character-Aware LM](../03_reading/R02/BIW-0055.md), C01/C02/C07 | §3.4 retains external word segmentation, CNN/highway composition, word-time LSTM and fixed-word output. Highway ablations drive interpretation, not just the architecture name. |
| [0102](../02_inventory/DETAILED_INVENTORY.md#BIP-0102), 4539–4581 | [Embeddingless NMT](../03_reading/R01/BIW-0068.md), C01/C07 | §10.4 retains fixed coordinates versus trainable sharing, uncertain extra-coordinate output handling, and the decisive token-dropout control. Strong alternative explanation is not omitted. |
| [0111](../02_inventory/DETAILED_INVENTORY.md#BIP-0111), 4999–5045 | [Exact Byte](../03_reading/R04/BIW-0088.md), C01/C11 | §9.3 distinguishes canonical support, raw neural softmax, renormalization and termination; enumeration/caches do not disappear under a model-call bound. Positive task illustration could be expanded, but is not needed to establish the methodological role. |
| [0171](../02_inventory/DETAILED_INVENTORY.md#BIP-0171), 7763–7811 | [MtPC](../03_reading/R05/BIW-0079.md), C06 | §8 preserves normalized dependence, composite windows, head costs and measured throughput. Current claim rules supersede the card's older wrapper shorthand; no software bias is certified. |
| [0189](../02_inventory/DETAILED_INVENTORY.md#BIP-0189), 8521–8570 | [Inan et al.](../03_reading/R08/BIW-0036.md), C07 | §10.1 uses the AL/RE/combined factorial comparison to separate supervision from table reuse. Conditional column-space theory is not turned into table equality or direct byte evidence. |
| [0206](../02_inventory/DETAILED_INVENTORY.md#BIP-0206), 9195–9237 | [Bolmo](../03_reading/R06/BIW-0097.md), C09 | §11.3 distinguishes static geometry from functional alignment through frozen layers; suffix lookup, conversion bytes and noncatastrophic no-stage-one control remain. |
| [0221](../02_inventory/DETAILED_INVENTORY.md#BIP-0221), 9795–9842 | [MYTE](../03_reading/R07/BIW-0104.md), C03 | §12.2 distinguishes external Morfessor/coding from raw UTF-8 and neural boundary learning; unsupported-script relative worsening is correctly not an absolute-length increase. Current survey follows corrected LR/overall ordering, not the stale card transcription. |
| [0229](../02_inventory/DETAILED_INVENTORY.md#BIP-0229), 10128–10228 | [SpellingBee](../03_reading/R10/BIW-0110.md), C10 | §12.7 distinguishes frozen-type probe decoding from host competence and the separate initialization intervention. Filters and bounded null results remain explanatory. |
| [0290](../02_inventory/DETAILED_INVENTORY.md#BIP-0290), 12959–12975 | [Reformer](../03_reading/FIELD_ADDENDUM/arxiv_2001.04451v2.md), C04/C05/C07/C12 | §5.2 separates LSH connectivity, reversibility and FFN execution chunks; Q/K sharing is not lexical tying, and training memory is not inference-cache elimination. |

The four supplementary cards were [H-Net](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md), [ELMo](../03_reading/FIELD_ADDENDUM/arxiv_1802.05365v2.md), [GPT-2](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md), and [Perceiver IO](../03_reading/R01/BIW-0117.md). ELMo/GPT-2 remain designated PARTIAL originals; their card reads add no FULL credit. Perceiver's 20M byte-BERT versus 201M byte-Perceiver comparison is explicitly unequal-capacity evidence, as the survey states.

## 5. All sixteen sections: coverage and explanatory structure

| Section / survey lines | Independent-field coverage judgment | Remaining concern or useful boundary |
|---|---|---|
| 1. Scope, 29–49 | Adequate. Defines the interface broadly and explicitly rejects a preferred local architecture as an inclusion rule. Counts are qualified. | Treat corpus sufficiency as a selected-survey judgment, not exhaustive recall. |
| 2. Units/four interfaces, 52–93 | Strong. Byte/scalar/code point/grapheme/restricted characters/subwords are distinct; input/internal/output/supervision have an operational table. | Add the CharT5 near-control where mechanisms are discussed, not necessarily another table row: P2-01. |
| 3. History, 96–134 | Adequate for the declared neural scope: 2011 MRNN, Graves, byte mLSTM, word composers, ELMo, byte-BPE. Classical PAQ is a real unfavorable control. | PPM/context mixing/arithmetic coding history is selective and explicitly acknowledged; no initial-survey blocker. Historical word composition is not relabeled byte generation. |
| 4. Encoders/conditional generation, 137–191 | Broad and substantive: annotation, character NMT/ByteNet, fusion/SDD, CharacterBERT, ByT5, CANINE, fixed latent workspace. Explains actual technique jobs. | P2-01 and P2-02. Full-source permissions remain distinct from left-to-right target permissions. |
| 5. Full-resolution alternatives, 194–245 | Strong. Dense byte attention, plain large byte LM, fixed sparsity, LSH, reversible storage, FFN chunks, segment recurrence, old-memory compression, selective state and within-byte depth prevent patch-centric framing. | No requirement to add every generic long-context architecture. Modern serving and exact recall remain separate outcomes. |
| 6. Grouping, 248–298 | Strong mechanism taxonomy: layout/content/rate; fixed/rule/external; soft membership; biased surrogates versus sampled gradients; entropy/confidence/utility; lexical discovery/deletion/codes. | P1-01: local positive hierarchy evidence needs more weight. GQ-VAE is brief but linked, not wholly missing. |
| 7. Causal paths/freshness, 301–331 | Strong. All operands, source/target time axes, shifts, legal but ineffective repair, training labels versus test features, and transient refresh are separated. | Actual regex/tokenizer prefix stability remains an artifact question, not proof of leakage. No blanket Hourglass within-group independence is asserted. |
| 8. Causal outputs, 334–383 | Strong. Local AR, marginals, circuits, diffusion and verification have different laws and costs; future-loss training is not an executable sampler. | P2-03 concerns presentation density only. MtPC optimized-wrapper law remains explicitly open; no reason to recertify it through another FULL. |
| 9. Scored events, 386–441 | Strong. Native chains, canonical paths, string marginals, raw prefixes, marked histories, option scores and denoising bounds are not collapsed by a byte denominator. | Some positive applications are abbreviated, but this chapter's methodological function is clear. TokSuite does not invalidate unrelated study arms. |
| 10. Sharing/optimization, 444–495 | Strong. Lexical axes, head/head, Q/K, directional and recurrent sharing are different; formulas, scale/rank assumptions and dropout controls matter. | Byte-specific causal evidence for tying is genuinely limited, appropriately open. Background PCGrad/VAE leads are not claimed as demonstrated byte repairs. |
| 11. Objectives/hybrids/conversion, 498–542 | Strong. Geometry, contextual compatibility, token-output stages, actual byte deployment, teacher laws and finite candidate outputs are distinguished. | Preserving instruction function remains an empirical target, not inferred from backbone correspondence. |
| 12. Multilingual/robustness/competence, 545–617 | Broad. Length allocation, external codes, internal rates, data imbalance, scarce annotation, dialect metrics, noise, Unicode, probes, arithmetic and long copy receive distinct instruments. | English/ASCII and serving evidence gaps are acknowledged; they are not failures of every byte model. Positive recent hierarchy robustness could accompany P1-01 if kept compact. |
| 13. Compute/data/serving, 620–676 | Strong. Exposure, packing, parameter conventions, FLOPs, training steps, resident auxiliary models and request latency are distinct. Counter-frontiers resist universal claims. | No common-hardware quality frontier exists in this corpus; that prevents a universal ranking, not publication of a comparative survey. |
| 14. Consolidated classification, 679–716 | Useful synthesis. Six editorial parents, twelve overlapping canonical families, thirteen navigation routes and actual researcher techniques remain distinct. Negative controls change the explanation. | Trim repeated evidence-state reminders if needed; do not remove the classification, which is part of the requested deliverable. |
| 15. Evaluation/frontier, 719–755 | Adequate. Separates mechanism, training-frontier and deployment-frontier experiments; units and statistical sampling differ. | Artifact closure is correctly separated from new experimental evidence. Open outcomes do not become compulsory survey acceptance experiments. |
| 16. Conclusion, 758–764 | Coherent and appropriately conditional. No universal byte/subword winner; returns to redistribution of work. | A more balanced central hierarchy example would strengthen the positive synthesis without changing its thesis. |

Appendix A is the correct home for count/depth details; Appendix B appropriately preserves translation-sensitive distinctions. Neither is counted as a seventeenth substantive section. The executive summary is a real summary rather than a replacement for the long text. The open-question file usefully separates research comparisons, thinly sampled outcomes and specific artifact closure.

## 6. Does classification drive the writing, or just catalog names?

**It drives the writing in substantive places.** Examples with traceable mechanisms and controls:

1. **Local composition/optimization:** §3.4 explains why CNN, pooling and highway gates serve different roles and uses the MLP/highway comparison to reject an alphabet-only explanation.
2. **Representation versus clock/output:** §4 places CharacterBERT, CANINE, ByT5 and Perceiver on different internal/output/supervision contracts rather than treating all token-free inputs as generative byte evidence.
3. **Compute alternatives:** §5 and Table 2 classify resource changes—positions, edges, stored history, within-byte depth and activations—rather than making all efficient sequence methods descendants of patching.
4. **Grouping:** §6 distinguishes the decision gradient from the rate constraint and the content operator. The same segmentation label does not substitute for these mechanisms.
5. **Output:** §8 asks which dependence is modeled and what actually samples it. Circuits, independent heads, local AR and diffusion are not just catalog entries under “multi-byte.”
6. **Sharing and learning:** §10 uses factorial supervision/reuse and dropout controls; §11 separates matching vectors from preserving contextual function.
7. **Utility:** §12 distinguishes coverage, parity, learned noise tolerance, probe recoverability and generated task success. §13 rejects token length and acceptance as sufficient system objectives.

The method-by-method subsections in chapters 3–4 are reasonable historical/method expositions inside this framework. Their presence does not make the work a name catalog. The weakest balance is not lack of taxonomy but lack of direct positive evidence for some central hierarchical entries, addressed in P1-01.

The taxonomy does not claim an empirical clustering algorithm. The manual multi-label assignments and disjoint editorial navigation are described honestly. A record about a reviewer question, standard or parameter specification is not presented as another researcher-solved AI problem. That distinction is important because the original user asked for detailed problems, solutions and techniques, not inflated rows.

## 7. Counts and methodology: independent recount results

The following were recomputed from saved indexes/ledgers with read-only standard-library Python, not inferred from assignment totals.

| Object | Independent result | English claim assessment |
|---|---:|---|
| Sequential unique BIW anchors | 141, BIW-0001–0141 | Matches §1.2/Appendix A and executive summary. This is documentary identity count, not 141 independent empirical replications. |
| Source genres | 136 academic/proposal papers; 1 report; 3 standards; 1 introduction | Total 141; “137 research documents” is correct when report and papers are combined. Proposal is not achieved experiment. |
| Sequential unique BIP anchors/index rows | 296, BIP-0001–0296 | No missing or duplicate IDs in the saved index. Wording explicitly says records, not independent scientific problems. |
| Contributing-source union | 140 | Proposal-only BIW-0102 is absent from record-source union. |
| Declared source depths | 62 NF, 30 RF, 29 A, 13 selected P, 2 intentional narrow P, 1 proposal P, 3 N, 1 O | Exhausts 141. Two intentional partials are not silently promoted to FULL. |
| FULL identity union/card paths | 92 distinct; 62 new/30 reused; all 92 paths exist and declare full reading | Matches claim. Marker/path existence does not certify the originals' reading or every result. |
| Current record support classes | 145 new-FULL + 88 reused-FULL + 53 discovery A/P + 3 normative + 2 introduction + 1 correction/open computation + 4 narrow-PARTIAL | Total 296; 233 scoped-FULL-supported records, not 233 independently successful experiments. |
| Canonical family memberships | 506 distinct BIP/C pairs | Family counts 35/37/43/43/14/35/33/53/37/60/33/83 match taxonomy. |
| Family-specific source unions | 27/27/32/28/10/25/24/38/18/44/20/53 | All twelve pairs match FINAL_AUTHOR_COUNTS and classification. Do not sum these as independent works. |
| Editorial navigation routes | 13; 296 memberships, 296 unique BIPs; exact coverage 1–296 | Correct disjoint navigation claim, not another natural-category census. |
| Historical reverse provenance | 423 source-key rows, 496 BIP edges | Matches documentary ledger. |
| Field reverse provenance | 10 FAD rows, 10 BIP edges | Combined 433 keys/506 edges. This 506 is different from family membership. |
| Discovery search logs | Eight files exist, S01–S08 | Supports presence of documentary search streams; execution quality/completeness was not independently replayed. |

**No count inflation found in the current three English deliverables.** `SURVEY_EN.md:41`, `:771–781`, `EXECUTIVE_SUMMARY_EN.md:7`, and `OPEN_QUESTIONS_EN.md:11` distinguish records, source entities, scoped reading and reproduction. Methodology is a selected narrative synthesis with documentary reconciliation, not an exhaustive systematic search or quantitative meta-analysis. It does not claim learned embedding clustering. The reviewer likewise adds no FULL credit.

The full identity count is stronger than an assignment count because it joins actual registered IDs and available card paths, but it is weaker than independent verification that every source scope was read. The English text generally respects precisely that distinction. This report does not rerun earlier validators' reported 10,000-plus link checks or certify all of their historical hash comparisons.

## 8. Strong alternatives, universal claims and open gaps

### 8.1 Alternatives that are actually present

The strongest obvious alternative explanations are not broadly missing: dictionary-disabled PAQ constrains a neural-only history; whitespace/rules constrain learned-boundary claims; full-resolution models challenge mandatory compression; sparse/hash attention and recurrence address different resources; matched token dropout changes embeddingless NMT interpretation; ordinary noise training challenges alphabet-only robustness; BPE/subwords can lead on training-compute frontiers; stage-two-only Bolmo limits universal staging claims; and finite candidate outputs are explicitly a legitimate task-specific choice.

The one especially useful omitted near-control is CharT5 with byte fallback (P2-01). Stochastic subword regularization/BPE-dropout and classical statistical segmentation could be expanded in a future edition, but catalog coverage plus the explicitly selective scope does not make their fuller exposition a current acceptance requirement. No claim here establishes that such alternatives have been exhaustively compared or defeated.

### 8.2 Universals and prior audit issues

The present long survey does not assert that all character models are bytes, all byte models are tokenizer/teacher-free on every axis, segmentation is necessary, independent future heads define a correlated sampler, coverage ensures robustness, tying universally helps bytes, or compression/acceptance ensures speed. Those were independently evaluated as propositions while reading the text, not waived because CLAIM_RULES exists.

The latest MYTE, Hourglass, dialect TP/IP, MtPC and TokSuite qualifications are visible at the affected English claims. This review checked textual propagation and sampled carrying cards, but **did not independently reverify those five originals**. The MYTE card's stale aggregate ordering and MtPC card's earlier shorthand illustrate why the current correction authority must be followed; a FULL label is not enough. The English author appears to have followed it. No old audit issue is declared mathematically or operationally closed merely by that propagation.

Some broad open-question sentences, such as `OPEN_QUESTIONS_EN.md:20`, should be read under its stated selected-corpus scope, not as proof that no other paper anywhere has a utility policy. The surrounding limits generally supply that reading; maintaining “in this corpus” when editing such sentences is preferable to strengthening them into literature-wide absence claims.

### 8.3 Which missing evidence blocks what?

| Gap | Does it block this initial selected survey? | What it actually blocks / appropriate first action |
|---|---|---|
| Full PPM/context-mixing/arithmetic-coding history | No; selective neural scope is declared. | An exhaustive history of compression would require new historical work. Do not pretend PAQ is that whole history. |
| Held-out adaptive-depth byte benefit beyond ACT's training result | No. | A positive modern quality claim for that route needs held-out experiments, not rereading the same training-only evidence. |
| Boundary versus aggregation causal attribution | No. | A universal operator/router ranking needs shared-backbone, matched-rate controls. The survey currently rejects such a ranking. |
| Byte-specific tied/untied causal ablations | No. | A recommended tying default requires actual controlled byte experiments and exact axis/optimization semantics. More generic word-tying papers do not substitute. |
| Mixed-script prefix-only generation, unseen-script knowledge, grapheme-preserving long copy, non-ASCII arithmetic | No, while explicitly open. | Those capability claims require direct generated outcome tests and careful units/populations. They are not acceptance experiments for a literature survey. |
| Modern matched-quality batched serving including Unicode buffering and tails | No. | Universal latency/serving superiority is unsupported. Workload-linked measurements, not another FLOP table, are needed. |
| MtPC optimized wrapper law, TokSuite Figure 6 pipeline, MYTE population/aggregate linkage, actual guide/regex prefix stability | No under current bounded wording. | The corresponding exactness/comparability/online claims need the named artifact, specification or author clarification. Another broad FULL batch is the wrong default remedy. |
| Representative positive hierarchy result and CharT5 near-control | Local writing repair only. | Existing cards plus the two targeted checks above suffice. No new source entity, training run or whole-paper terra batch. |

## 9. Recommended closeout and verification record

1. Address P1-01 in the existing main discussion; do not invent a matched-parameter or runtime win. Add the strong space control and retain reported budget limitations.
2. Incorporate P2-01 if making the byte/code-point/hybrid comparison maximally useful; specify fallback and changed capacity. Correct the metric precision in P2-02.
3. Apply P2-03 only where it removes duplicated procedure rather than scientific conditions. Preserve the long structure and all source-sensitive distinctions for translation.
4. Keep explicit open items open. Freeze counts/IDs unless the inventory owner authorizes a real documentary update. Do not treat this review as new source reading or a blanket proof/code audit.

**Verification performed:** Two read-only Python here-document checks exited successfully. They recounted IDs, genres, support states, 92 available FULL-card paths, twelve family memberships/source unions, thirteen routes, provenance rows/edges, and discovery-log existence. The sampled records/cards and complete English narrative were manually read as described above. Public browser passage checks were limited to the two stated works; the single browser tab created for them was closed, leaving unrelated tabs alone. No PDF or conversion intermediate was downloaded. Application build/pytest is not relevant to this documentation-only review and was not run.

**Write boundary:** This task creates only `05_review/FINAL_SURVEY_COVERAGE.md`. It does not rewrite English author text, inventories, cards, claim rules, production code or project state. No subagent, installation, training, commit or push was used. The repository already contained untracked survey and unrelated artifacts at the first status check; they are not this review's output and are left untouched. A final saved-report structural/link/whitespace check and repository status inspection accompany delivery.

**Bottom line:** Accept the independent scope and breadth; make the small balance/precision improvements rather than demand all unknowns disappear. **Additional terra full reading is not genuinely needed for initial survey acceptance or the proposed repairs.** Any future expansion should name a missing mechanism or decisive control first, not pursue a paper-count target.
