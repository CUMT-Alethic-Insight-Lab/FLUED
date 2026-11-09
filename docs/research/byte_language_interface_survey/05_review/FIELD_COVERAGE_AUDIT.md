# Independent field-coverage and classification audit

2026-11-09 · independent sol review · documentary and targeted-source audit, not terra full reading.

## 1. Decision

**Start the long English survey now, with a bounded completion gate; do not call the corpus exhaustive or equate 283 records with 283 distinct field problems.** The eight streams and returned readings support a genuinely independent account of language interfaces. They no longer need a local project's architecture, source revisiting, or a compression proposal to supply their organizing questions.

Four representative omissions were checked against public originals: **Adaptive Computation Time, Reformer, ELMo, and GPT-2's input-representation report**. The first two expose substantive missing mechanisms; the latter two repair important historical/interface attribution. This is a small, directed coverage check, not a new systematic literature search. The minimum incremental reading recommendation is **two full-paper targets plus two narrow source extractions**, coordinated with—not substituted for—the existing terra queue (§8).

The main remaining classification risks are:

1. Treating computation allocation as predominantly sequence shortening, overlooking variable computation **within one byte step** and efficient full-resolution attention.
2. Counting source-specific mechanisms, evaluation cautions, negative observations, and reviewer questions as one homogeneous population of “problems.”
3. Letting valid links with wrong semantic labels propagate from reading cards into synthesis; the current central correction ledger has already recognized several such cases.
4. Mistaking a large multilingual inventory for demonstrated mixed-script streaming generation, or a byte alphabet for teacher-free training, exact Unicode preservation, or equitable text context.

These are manageable synthesis obligations, not reasons to restart discovery or postpone all writing until every reserve paper is read.

## 2. Inputs, snapshot, and accounting

Read the [PLAN](../PLAN.md), **all eight S01–S08 WORKS registers**, the complete canonical problem index and [TAXONOMY](../02_inventory/TAXONOMY.md), [COUNTS](../02_inventory/COUNTS.md), [READING_QUEUE](../02_inventory/READING_QUEUE.md), targeted detailed records, and all eight R01–R08 batch summaries. Eight individual returned cards were read for the issues below:

- [R01 CANINE](../03_reading/R01/BIW-0004.md), [Perceiver IO](../03_reading/R01/BIW-0117.md).
- [R02 Graves](../03_reading/R02/BIW-0053.md).
- [R03 segmental neural LM](../03_reading/R03/BIW-0042.md).
- [R05 probabilistic circuits](../03_reading/R05/BIW-0079.md).
- [R06 token-to-byte distillation](../03_reading/R06/BIW-0098.md).
- [R07 MYTE](../03_reading/R07/BIW-0104.md).
- [R08 byte-level simulation](../03_reading/R08/BIW-0108.md).

Batch summaries are separate inputs, not additional paper readings. Other batch-level findings below are attributed to their summaries or the central ledger, not an independent rereading of their papers.

During this audit the inventory owner integrated R01–R08. I therefore reread the updated COUNTS, relevant current records, [CORRECTION_LOG](../02_inventory/CORRECTION_LOG.md), the definitions and identity-ledger opening of [EVIDENCE_STATUS](../02_inventory/EVIDENCE_STATUS.md), and both [R09](../02_inventory/batches/R09.md)/[R10](../02_inventory/batches/R10.md) manifests. The **post-integration state**, not the earlier zero-completion manifest, is the decision baseline:

| Quantity | Current interpretation |
|---|---|
| 137 entities | 133 academic papers including one proposal-only, three standards, one official introduction; not 137 native byte LMs. |
| 283 + 3 = 286 BIP records | 283 merged source-backed records plus three audit extractions; stable record identifiers, not a field-problem census. |
| 423 source rows, 496 mapping edges | Provenance relations; neither independent effects nor additional papers. |
| 50 returned terra cards | Fifty distinct work IDs, batch sizes 6/7/7/6/6/6/6/6, all carrying FULL markers; structurally checked here. |
| 30 old scoped FULL, 80-work union | Current central identity reconciliation reports empty old/new intersection and 80 distinct scoped FULL sources; I do not claim to have independently reread all 80 originals. |
| 52 eligible complete-paper gaps | Ten selected in R09/R10, 42 deferred; selected does not mean completed or dispatched. |

A scoped FULL is source-reading completion, not proof validation, reproducibility, runtime tensor identity, or complete reporting of every cost. This audit adds **zero new FULL credits** and assigns no new BIW/BIP numbers.

## 3. Coverage against an independent byte-interface field

“Covered” below means a route is identifiable and can be discussed at its actual evidence depth. It does not mean every comparison or implementation is closed.

| Field axis | Present anchors and useful distinctions | Assessment and minimum remaining obligation |
|---|---|---|
| Historical character antecedents | Sutskever's restricted-alphabet multiplicative RNN, Graves's character/observed-byte experiments, character CNNs, character-to-word composition, ByteNet, historical character NMT, MDL segmentation. | Substantially repaired by R02/R03. Do not begin history with BLT. Add ELMo as a named contextual-representation antecedent; classical statistical compression is still selective rather than a traced lineage. |
| Pure bytes versus hybrids | Raw-byte LM/NMT, byte-input annotation, word-local byte CNN, byte-BPE, fallback, MYTE transcoding, byte+boundary/EOT, character–subword adaptation, T-FREE. | Broad coverage. Separate deployed alphabet from preprocessing and teacher provenance. GPT-2 is missing as a directly registered historical byte-BPE anchor, despite repeated references to its descendants. |
| Encoder / sequence-to-sequence / decoder | CANINE, CharacterBERT and Perceiver; ByT5/MANTa/Charformer/byte NMT; dense, recurrent, sparse and hierarchical causal LMs. | All three families exist. R01 closes the previously important encoder-original gap. Source-full translation is not streaming-source generation; masked reconstruction is not causal pretraining. |
| Input / internal / output / supervision units | CANINE-C bucket labels versus CANINE-S subwords; CharacterBERT's word-local UTF-8 and closed word MLM; serialized byte-offset labels; byte+boundary classes; temporary cross-tokenizer byte heads. | Strong taxonomy. Make the tuple visible in survey comparison tables, not only behind links. Also record tokenizer/teacher use during training separately from deployment. |
| Local composition and grouping | CNN/highway, recurrence, attention pooling, fixed concatenation, soft candidate mixtures, cumulative soft assignments, contextual-state selection, deletion, fixed latent arrays, quantized codes. | Strong. A boundary does not identify the aggregation operator. Full-length fusion, survivor deletion, and explicit span aggregation are not synonyms for compression. |
| Causal chunking and state freshness | Hourglass shifts; MEGABYTE global/local shifts; completed DTP groups; H-Net; scratchpad masks; failed causal Charformer repairs; offline BPE hints. | Strong after R03/R05. Retain upstream convolution/pooling permissions, partial groups, and train/deploy boundary differences. Partial-prompt and termination behavior often remain unreported. |
| Multi-byte prediction and generation | Local AR, independent offset heads, normalized probabilistic circuits, confidence acceptance, exact-greedy verification, exact target-law sampling, block diffusion. | Strong mechanism diversity. Generic multi-token-prediction origin BIW-0085 remains shallow; do not assume it has no byte experiments just because discovery did not inspect them. Distinguish auxiliary training benefits from an executable joint sampler. |
| Sharing and general theory | Press/Wolf, Inan, normalization, output-rank constraints, gradient diagnostics; direct MEGABYTE local I/O sharing, LCA head/head sharing and untied byte arms. | Good conditional foundation, not a byte-specific tying theorem. Add cross-direction sharing for ELMo and query/key projection sharing for Reformer only on their actual axes. Algebraic invertibility and shared parameters remain different claims. |
| Optimization and concrete AI methods | Deep/all-position/future supervision, span corruption, highway gates, Hessian-free optimization, straight-through/Gumbel, EMA/rate loss, staged imitation/distillation, LoRA, hypernetworks, circuit mixtures, auxiliary-gradient controls. | Rich but partly background-heavy. ACT adds halting, recurrent internal steps and a computation penalty; REINFORCE's full original remains R09. Morfessor's actual unsupervised resource-based role is now established by R07, not merely “morphology teacher.” |
| Efficiency beyond compression | Dense byte stacks, sparse Transformer, recurrent state, compressed history, fixed latent arrays, parameter/text/FLOP distinctions, training/decode reversals. | Substantive, but Reformer is an identifiable missing full-resolution route. Depth-dependent activation memory, FFN chunking, and approximate attention should not disappear into “fewer tokens.” Historical nonhierarchical originals are correctly prioritized in R09. |
| Multilinguality, robustness and fairness | Parallel-content lengths, adaptive script rates, MYTE, endangered-language NMT, XTREME-UP, language-imbalance controls, natural versus synthetic noise, normalization, dialects, byte legality. | Broad but uneven. Code-switching appears as a claim/gap, not general causal-router evidence. Include the actual code-mixed Char2Subword task results without turning them into byte-generation results. Grapheme-preserving generation, unseen scripts, non-ASCII arithmetic and long multilingual exact copy remain thin. |
| Negative evidence and methodology | PAQ beating an early neural model; dropout-controlled reversal; leak-free but poor grouping; same-FLOP subword wins; language/host failures; rank reversals; cost reversals; exactness/metric counterexamples. | Strong. Keep genuine negative results distinct from missing experiments, source conflicts, and unverified artifacts. TokSuite Figure 6 is quarantined centrally, not a reason to discard all its task results. |

**Non-omissions:** The corpus need not absorb every speech, vision, file-byte, generic optimizer, generic mixture-of-experts, or memory architecture paper. A named technique's presence in broader AI does not create an obligation to claim a byte-text application. Conversely, “not a new architecture” is not a reason to omit a real interface or evaluation mechanism.

## 4. Targeted online checks: four representative omissions

All four sources below were actually opened in Kimi Code Desktop's built-in browser. Reformer and ACT were selected because their mechanisms are not supplied by another recent patching paper; ELMo and GPT-2 were selected because the inventory already relies on their lineage without a dedicated primary entry. No general web query or document upload was used.

### 4.1 Adaptive Computation Time: a substantive missing byte mechanism

**Alex Graves, _Adaptive Computation Time for Recurrent Neural Networks_, [1603.08983v6](https://arxiv.org/html/1603.08983v6), 21 February 2017.** Inspected abstract, method §2–2.2, experiment setup, and §3.5/§4; not a new FULL/figure audit.

- §3.5 explicitly states **one byte per input timestep and next byte as target**, a 256-way softmax, raw Wikipedia Unicode text including markup, and 500-byte subsequences. It is not merely an author title containing “character.”
- A recurrent transition and output map are reused for several internal computations before consuming the next byte. A learned halting unit and weighted state/output aggregation determine how much to compute; a ponder-cost penalty discourages excessive work.
- This varies **internal depth/time per fine symbol** rather than predicting groups that reduce the sequence length. The current C04 question can accommodate it, but the registered work/mechanism inventory does not actually instantiate the route.
- The paper reports **no large language-model gain**, only similar error and suggestive allocation patterns; §3.5's errors are on the **training set**, not a held-out quality frontier. Boundary-like pauses and entropy contrasts are qualitative evidence, not proof of semantic segmentation or a serving speedup.
- §2.2 explicitly approximates derivatives by ignoring halting discontinuities. Do not repeat the abstract's differentiability language as a global smoothness theorem.

**Missing question:** Can compute be allocated by repeated causal state refinement at a byte, without shortening input, and does the added work improve held-out utility? This cannot be filled by H-Net's boundary rate, a scratchpad refresh, or an entropy teacher alone. The early entropy-versus-computational-effort discussion also prevents accidentally presenting that conceptual distinction as invented in 2026.

### 4.2 Reformer: an efficiency and sharing-axis omission

**Nikita Kitaev, Łukasz Kaiser, Anselm Levskaya, _Reformer: The Efficient Transformer_, [2001.04451v2](https://arxiv.org/html/2001.04451v2), 18 February 2020.** Inspected introduction, §§2–3, experiment descriptions in §5, and selected appendix text. Curves and implementation were not independently checked; no new FULL credit.

- The paper actually evaluates **enwik8 with 64K positions**, besides distinct image and synthetic-copy tasks. It offers full-resolution sequence processing, not learned byte segmentation.
- **Locality-sensitive hashing attention** approximates attention lookup; **reversible residual layers** reconstruct activations for backward computation; **chunked feed-forward computation** lowers intermediate activation memory. These solve different costs and should be recorded separately.
- Query/key projections share a map in the LSH setup, with normalized keys and source-position masking. That is neither lexical input/output tying nor an inverse encoder–decoder. The paper separately discusses embedding/output sharing in translation settings.
- More hash rounds change quality and cost. The largest models lack equally large full-attention baselines under the available memory budget (§5); do not translate feasibility into a modern matched-quality batch-serving frontier.
- I do not certify the original code's incremental-prefix behavior or infer unrestricted multilingual coverage from enwik8.

**Missing question:** Can a byte-length sequence retain every position while reducing attention and training-activation costs, and what approximation or recomputation does that require? Sparse Transformer partially covers the first half; it does not substitute for the reversible/FFN-memory mechanism.

### 4.3 ELMo: attribution and contextual-transfer coverage, not a new byte LM

**Matthew E. Peters et al., _Deep contextualized word representations_, [1802.05365v2](https://arxiv.org/html/1802.05365v2), 22 March 2018.** Inspected §§1–3.4 and the layer-combination/task descriptions; no complete experiment/appendix audit.

- Character-CNN/highway composition feeds **word-position** bidirectional LMs; supervision predicts words, not a raw-byte output stream. Exact character-to-byte implementation is not established from these inspected paper passages.
- The downstream representation is a learned **task-specific mixture of layers**, with a learned scale; the pretrained LM is frozen when attached to task networks, after any separately described domain adaptation.
- §3.1 explicitly shares token-representation parameters **between forward/backward directions**, and likewise shares their softmax parameters, while keeping directional LSTMs distinct. This is not a declaration that input composition and softmax are the same matrix.

CharacterBERT's ELMo-style CNN/highway role is already acknowledged. Therefore ELMo is **a missing primary lineage entry and contextual-transfer mechanism**, not evidence that convolution or word-local composition was absent from the corpus. One concise primary-source extraction can close it; a full new benchmark-reading batch is unnecessary unless the survey makes its numerical transfer results central.

### 4.4 GPT-2: the byte-BPE middle ground should have a primary historical anchor

**Alec Radford et al., _Language Models are Unsupervised Multitask Learners_, [official 2019 report](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf).** Visually read PDF **p.4, §2.2 Input Representation**, its continuation, and adjacent §2.3/§3.1 context. The official file is not revision-pinned; no full-report or performance audit is claimed.

The report explicitly contrasts codepoint-based BPE with a **256-byte base alphabet**, learned merges and restrictions against merging across character categories, with a space exception. It also reports preliminary standard-byte-LM underperformance on WebText without a complete matched-compute experiment in that passage. Its output vocabulary remains merged symbols, not 256 next-byte classes; the adjacent model description gives 50,257 vocabulary entries. Its broad string-probability prose must be qualified by the later canonical-path/prefix-event literature already read in R04.

**Missing question/lineage:** How did byte-complete *subword* coverage become a practical alternative to both restricted character vocabularies and fully byte-stepped LMs? The 2016 BPE translation paper does not itself document this later byte alphabet. Wang/Cho/Gu byte-subword NMT remains a separate included work, not a duplicate of GPT-2.

## 5. Are concrete AI techniques missing or merely hard to find?

The inventory is much richer than a list of byte-model names. It should, however, expose an explicit **technique → role → source → evidence** index in the eventual synthesis, rather than require readers to reconstruct it from hundreds of prose rows. This is a recommendation to the existing synthesis owner, not a request to create another file here.

| Technique group | What the corpus actually supports | Audit action |
|---|---|---|
| Composition | Character/byte CNN, max pooling, highway carry/transform, local recurrent encoders, n-gram hashes, cross-attention. | Covered. Preserve whether the operation retains full resolution or creates shorter positions. ELMo adds contextual layer mixing, not another CNN invention. |
| Boundary learning | Soft mixtures/assignments; Gumbel/straight-through; explicit teachers; own entropy; rate priors/controllers; score-function policy learning. | Covered as a discovery taxonomy. REINFORCE's genuine full-method gap is already in R09; do not present a biased practical variance-reduction scheme as automatically unbiased. |
| Compute and memory | Recurrence/SSMs, sparse edges, latent arrays, compressed history, local/global trunks, transient refresh. | Add ACT internal-step allocation and Reformer LSH/reversibility/FFN chunking. Activation memory and KV memory need different fields. |
| Output dependence | Local autoregression, independent future heads, mixture/HMM/tree circuits, denoising diffusion, rejection/correction, greedy and approximate acceptance. | Covered. A probabilistic circuit's normalization, overlapping-window training loss, and verifier policy are three distinct facts. |
| Optimization/transfer | Hessian-free training, deep supervision, noise/dropout, staged imitation, fixed-host backpropagation, logit/representation distillation, hypernetworks, LoRA. | Covered. Dynamic evaluation that **updates weights at test time** is present in the Graves card but insufficiently elevated as an evaluation permission, distinct from hidden-state persistence. |
| Statistical/unsupervised methods | MDL, unigram segmentation, semi-Markov DP, lexicon/spelling mixtures, morphology induction, ranking/proxy models. | Do not mislabel these all as neural components. MYTE's Morfessor/resource pipeline and R03's semiring/DP are real methods, not generic “end-to-end learning.” |
| General theory/background | Word-level tying, output rank, normalized geometry, VAE posterior collapse and multi-task gradient methods. | Keep as conditional explanatory background. Their large record footprint does not establish tiny-byte-alphabet experiments or a deterministic compression failure mechanism. |

A further MoCE read could clarify attention-head contextualization experts, but its title is not permission to declare that a general sparse FFN mixture-of-experts architecture has been evaluated. Likewise, no requirement arises to import every contemporary optimizer, quantization scheme, or retrieval mechanism without a direct role in an included text interface.

## 6. The 283-record question: useful inventory, not 283 independent questions

### 6.1 What has genuinely improved

The work-level deduplication is substantial and credible at the structural level: 250 appearances resolve to 137 entities; shared titles/versions are not new papers. The 423→283 source-row consolidation is not merely relabeling each stream's list. ByT5 exposure/cost, BLT teacher, H-Net rate/scheduling, and several UTF-8 records have clear cross-stream joins. Two exact-speculative-sampling papers appropriately share [BIP-0110](../02_inventory/DETAILED_INVENTORY.md#BIP-0110) while retaining separate work identities and results.

However, “problem/mechanism/evidence record” is a broader object than “distinct research problem.” Those meanings should not be exchanged in the headline. Counts of cluster memberships also overlap; their sums cannot supply a problem total.

### 6.2 Residual synonym/parent–child candidates

These are editorial consolidation candidates for survey prose, **not an instruction to delete stable records or provenance**. A different work or a different proposed remedy does not automatically create a different parent problem.

| Records / family | Judgment | Smallest faithful treatment |
|---|---|---|
| [BIP-0274](../02_inventory/DETAILED_INVENTORY.md#BIP-0274) and [0275](../02_inventory/DETAILED_INVENTORY.md#BIP-0275) | Strongest same-parent case: prefix-event mismatch and its persistence under ideal training/correction. The updated records reproduce the same carrying card passages. | One survey question with a counterexample, persistence condition, and algorithm subfinding. Keep both source IDs, but do not advertise two independent failure modes. |
| [BIP-0074](../02_inventory/DETAILED_INVENTORY.md#BIP-0074), [0267](../02_inventory/DETAILED_INVENTORY.md#BIP-0267), [0268](../02_inventory/DETAILED_INVENTORY.md#BIP-0268) | Expensive tokenizer selection, intrinsic proxies, and compression insufficiency share a parent problem. Cross-scale prediction and minimum-token counterexamples are genuinely distinct evidence. | One parent question, separate studies/controls. Do not merge numerical results or call the papers one experiment. |
| [BIP-0054](../02_inventory/DETAILED_INVENTORY.md#BIP-0054), [0157](../02_inventory/DETAILED_INVENTORY.md#BIP-0157), [0162](../02_inventory/DETAILED_INVENTORY.md#BIP-0162) | Computational utility versus local unpredictability is one broad question. Direct utility labels, next-byte-confidence targets and repetition/novelty rules are different mechanisms. | Group under one question with distinct label sources and results. ACT supplies an earlier relevant comparison, not proof of direct intellectual borrowing. |
| [BIP-0247](../02_inventory/DETAILED_INVENTORY.md#BIP-0247) versus [0249](../02_inventory/DETAILED_INVENTORY.md#BIP-0249) | Not simply synonyms: static geometry imitation versus contextual host compatibility. | Keep the distinction, but cite geometry fitting and contextual MLM as stages of one interface-transfer problem; repeated full-card paragraphs are shared evidence, not extra experiments. |
| [BIP-0063](../02_inventory/DETAILED_INVENTORY.md#BIP-0063) versus [0112](../02_inventory/DETAILED_INVENTORY.md#BIP-0112) | Standard's definition and model's partial/strict evaluation concern the same legality contract but are different source types. | One definition with an empirical test attached. A normative UTF-8 statement is not a second observed model failure. |
| [BIP-0284](../02_inventory/DETAILED_INVENTORY.md#BIP-0284), [0285](../02_inventory/DETAILED_INVENTORY.md#BIP-0285), [0286](../02_inventory/DETAILED_INVENTORY.md#BIP-0286) | Two architecture-specification observations plus a reviewer metric question, not three author-solved field problems. | Keep as sharing evidence and an audit exception; separate their type from problem families in the final inventory introduction. |

Other obvious shared parents include order-sensitive aggregation (0152/0153), boundary-gradient estimation (0009/0146/0164), and training versus generation efficiency (0012/0041/0069/0073). Their **mechanisms and empirical contracts should remain separate**; eliminating all repetition by collapsing them into one generic efficiency row would lose information.

**No defensible corrected unique-problem number is supplied here.** An exhaustive parent-level semantic recoding was not performed, and changing 283 to another precise number on these samples would manufacture certainty. The useful delivery is “286 traceable records organized into a smaller set of overlapping research questions,” followed by an explicit parent/subfinding explanation.

### 6.3 Classification and joining defects, including already corrected ones

The current [CORRECTION_LOG, backlink semantics](../02_inventory/CORRECTION_LOG.md) explicitly recognizes the following issues. They should be treated as **centrally adopted corrections**, not newly unresolved accusations:

- CANINE card's numbered findings attach downsampling to 0003, supervision to 0004 and n-gram evidence to 0005; canonical meanings are 0003 hash coverage, 0004 downsampling, 0005 supervision.
- Perceiver card's output-query paragraph links 0122, whose canonical meaning is word-selected masking; output queries belong to 0258. Its latent-capacity paragraph links 0123, whose canonical meaning is approximate content matching.
- MtPC card's 0172 heading discusses acceptance/cost, while canonical 0172 concerns overlapping-window drafting; 0173 is the capacity/latency record. Generation-law and cost facts must be joined by content, not by list position.

The owner has wisely retained IDs and used whole-card context. **Residual risk:** reusing the same entire card passage under several BIPs is evidence replication in the document, not new evidential independence. The final survey must quote the relevant subclaim and canonical question, rather than automatically ingesting every linked paragraph as row-specific evidence. Also distinguish a topic's classification from whether its paragraph explicitly contains a word such as “causal”: repeated subword positions are primarily an interface/position intervention, not automatically a new leakage problem merely because they carry C05.

## 7. Real problem gaps versus ordinary unknowns

| Question not adequately promoted in the current problem structure | Evidence available now | What is actually missing |
|---|---|---|
| Can extra recurrent computation within a byte improve utility without grouping bytes? | ACT primary passages in §4.1. | A registered representative and a separate compute-depth distinction; not another boundary-rate row. |
| Can full-resolution byte modeling reduce attention and activation-memory costs without sequence shortening? | Reformer primary passages in §4.2; Sparse Transformer already registered. | LSH/reversible/FFN-memory mechanisms and their approximation/recomputation tradeoffs. |
| Do evaluations adapt model weights, only recurrent state, or neither? | Graves card: static versus online-weight-updated evaluation and different scores. | An explicit evaluation-permission axis. It changes the scored learner and test-time work, not just cache capacity. No new paper is needed to surface it. |
| Can lexical memorization help without reintroducing a fixed input/output interface? | CANINE n-gram rescue and added parameters; segmental LM lexicon/spelling mixture; byte-level n-gram interventions. | A visible composition–memorization comparison across mechanisms. Input coverage, parameter capacity and target vocabulary must remain separate. |
| What is the deployment output event when boundaries or EOT markers are generated jointly with bytes? | R06 byte+boundary/EOT summaries and marked-versus-unmarked warning. | A parent output-event question joining those sources with prefix probabilities, rather than dispersing them only into adaptation and budget rows. The mechanism is already in the corpus. |
| Does a user receive an exact original string, normalized string, valid scalar stream, or task-correct answer? | Standards, ByT5 postprocessing, MYTE normalization uncertainties, legality/correctness tests. | End-to-end presentation/accounting synthesis; especially incomplete scalars, invalid-byte repair, and byte-offset versus grapheme offsets. No evidence yet supports a universal preservation guarantee. |
| What does latency mean for bursty byte outputs and incomplete characters? | Existing per-byte costs and sparse partial-prefix reports. | Matched-quality batched serving, prefill, first complete scalar, tail latency and partial-prompt/EOS contracts. This is largely **missing evidence**, not proof a method fails. |
| Are compression, spelling competence and language fairness robust to mixed scripts and unseen scripts? | R07 MYTE unseen-script non-gain, XTREME-UP task reversals; Char2Subword code-mixed encoder tasks; MAGNET's selector restriction. | General causal mixed-script generator and broader task evidence. Existing positive/negative cells do not establish that generalization. |

Classical context modeling/compression history remains a selective background gap. The MDL and PAQ comparisons provide a legitimate floor; they do not constitute a primary history of context mixing, variable-order prediction and coding. A compact contextual paragraph or an explicit scope limitation suffices for a neural-interface survey. Do not turn this into an unrequested full compression survey.

Unreported hardware, missing EOS details after a proper full read, an untested runtime alias, and unresolved author-table disagreements are **not each new scholarly problems requiring another FULL pass**. The updated EVIDENCE_STATUS distinction between unreported, unverified, source-conflict and not-applicable is appropriate and should survive into prose.

## 8. Minimum reading and integration queue

### 8.1 Incremental queue produced by this audit

These are recommendations to the coordinator/terra, not launched assignments. No existing FULL is repeated.

| Priority | Target and requested depth | Exact purpose and stop rule |
|---|---|---|
| 1 | **ACT**, [v6 PDF](https://arxiv.org/pdf/1603.08983v6), new full reading of the text-interface contribution. | Verify halting/state aggregation, approximate gradients, computation penalty, byte experiment and training-set-only negative. Stop at reported evidence; do not demand a new held-out run. |
| 2 | **Reformer**, [v2 PDF](https://arxiv.org/pdf/2001.04451v2), new full reading. | Separate LSH, reversible activation memory, FFN chunking, QK sharing, enwik8/copy experiments and baseline feasibility. Preserve code/serving unknowns rather than repeat-reading for them. |
| 3 | **ELMo**, [v2](https://arxiv.org/html/1802.05365v2), narrow primary extraction, not compulsory new FULL. | Register word-local character input, word supervision, layer mixing, frozen task integration and directional sharing. Exact byte implementation remains unknown unless independently inspected. |
| 4 | **GPT-2 report**, [official PDF](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf), narrow p.4 §2.2 extraction. | Register byte-complete BPE plus category/space merge policy as a subword interface. No need to reread all benchmark results or manufacture a historical performance frontier. |

This is **two new full-paper targets and two narrow extractions**, not four newly completed FULLs. The inspected passages already permit scoped drafting; wider quantitative comparisons wait for the relevant reader.

### 8.2 Reconcile with the queue already owned elsewhere

The existing R09/R10 ten-work manifests are not ignored or duplicated:

- R09's Al-Rfou, Choe, Sparse Transformer, Transformer-XL and REINFORCE route are well chosen. In particular the first two stop a patch-centric history; the last closes a genuinely different boundary-optimization method. Keep their current ownership.
- R10's U-Net horizons and T-FREE output mechanism address structural questions, not mere recency. Spelling Bee/Strawberry/CharBench and dialect work should adjudicate competing explanations, without making each paper a new generic “tokenization hurts characters” problem.
- **BIW-0085, _Better & Faster Large Language Models via Multi-token Prediction_**, still A-level in the inspected register, deserves a bounded source check for its actual byte-versus-token experiments and role in the multi-byte lineage. Escalate to a full read only if its quantitative training/generation claims will carry the chapter. Do not state “no byte experiment” from the present unknown.
- MoCE can remain a labeled A-level extension unless the synthesis claims detailed coverage of adaptive contextualization experts. T-FREE already has R10 ownership; no second assignment.
- No need to read all 42 other deferred papers before drafting, and no repetition of R01–R08 solely because a reported field remains unknown. Additional sources should add a missing mechanism, competing explanation or decisive control, not a higher work count.

## 9. Long-survey readiness and release conditions

**Readiness now: YES for long-form synthesis.** Historical, encoder, seq2seq, causal generation, adaptation, multilingual and negative-evidence chapters can proceed in parallel with the bounded missing reads. **Readiness for an exhaustive/fully adjudicated final survey: NO.** Exhaustiveness is neither supported nor necessary for a serious selected survey.

Recommended independent organization:

1. Representation and historical interfaces, including byte-complete subwords and word-local composition.
2. What is learned/predicted: objectives, four units, teachers, and probability events.
3. Computation: full-resolution, recurrent state, sparse attention, latent/hierarchical grouping and adaptive within-byte work.
4. Generation: causal alignment, output dependence, multi-byte sampling and verification.
5. Parameter sharing, optimization and pretrained adaptation, with byte-specific evidence separated from background theory.
6. Tasks/languages, robustness, fairness, exact text preservation and resource frontiers.
7. Open evidence and limits; only then a bounded local-project implication section.

Before final release, require:

- A parent-question explanation of what the 286 records count; no 283-independent-problem or 137-byte-model headline.
- Latest integrated cards/corrections, canonical semantic joins, and no wholesale paragraph-to-row independence assumption.
- ACT/Reformer included at completed or explicitly scoped depth; ELMo/GPT-2 historical/interface attribution repaired.
- The R09/R10 claims used substantively in the final comparisons either have their planned evidence or are accurately restricted; no blanket demand that all ten are needed to begin prose.
- Preserve decisive negatives: no-truncation degeneration, leak-free poor models, dropout controls, language/host and matched-FLOP reversals, real speed/cost conditions, source conflicts. Quarantine TokSuite Figure 6 as currently directed by the central correction ledger.
- No invented common cost/quality frontier or universal byte advantage. Give a condition once adjacent to its claim; avoid repetitive defensive paragraphs that crowd out actual comparisons.

## 10. Source access, limits, and verification

### Actual online activity

| Source | Public route actually used | Actual scope |
|---|---|---|
| Reformer | `https://arxiv.org/abs/2001.04451`, then fixed `https://arxiv.org/html/2001.04451v2` | Primary method/experiment text and selected appendix text; no visual curve or code certification. |
| ACT | `https://arxiv.org/html/1603.08983v6` | Primary method, setup and byte experiment/conclusion; synthetic-task text also returned, not promoted to byte-language evidence. |
| ELMo | `https://arxiv.org/html/1802.05365v2` | Primary contextual/transfer/sharing method passages; no exact input-encoding implementation or full result audit. |
| GPT-2 | Official OpenAI PDF linked above | PDF p.4 §2.2 and continuation visually inspected, adjacent context; no new full-report reading. |

All requests were direct known-source visits: **four work entities, zero broad search queries**. One screenshot capture timed out and succeeded on the next attempt. A text-snapshot continuation initially combined incompatible arguments; it was corrected. Shared browser control occasionally required reactivating this task's own tab, not touching another agent's page. The PDF viewer did not honor the page fragment as expected; ordinary scrolling reached p.4 without an alternate source or bypass. No login/paywall/certificate wall was bypassed.

Only one task-owned background browser tab was created and it was closed. The browser reported more than ten shared tabs, which crowds the sidebar; the other tabs were left untouched. No PDFs, extracts, screenshots, temporary scripts, or downloads were deliberately written into the workspace by this reviewer; browser-managed captures are not additional project deliverables.

### Deliverable checks and boundaries

A read-only Python structural check of saved files reported **137 distinct BIW anchors, 286 distinct BIP anchors, 50 returned cards with 50 distinct BIW IDs**, the expected eight batch sizes, all fifty with FULL markers and all present in the catalog. This checks documentary structure, not reading quality, semantic mappings or scientific truth. A final local-link/explicit-anchor/UTF-8/table/whitespace check is applied to this report before handoff; no build or pytest is appropriate to a single Markdown research report.

**The only file authored by this task is this report.** No shared inventory, reading card, PLAN, AGENTS, project state, term registry or source code was changed. No agents were dispatched, no training/reproduction/install occurred, no commit/push was made, and no background computation remains. This is an independent field audit and a minimum follow-up recommendation, not a replacement for terra's selected full readings.
