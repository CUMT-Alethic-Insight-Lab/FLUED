# Addressing, native readout, and task-correct causal use

## 1. Research question and evidence contract

A memory system must connect what was written to what a later task asks. That connection can fail because the query expresses the wrong target, the address selects the wrong association, the stored value is inadequate, the returned signal is poorly scaled, or subsequent computation relies on another route. These explanations require different interventions. They also permit different remedies: native query learning, better-conditioned associative updates, changed normalization, independent read queries, revised objectives, consumer adaptation, and additional computation over unchanged state all remain substantive alternatives to source revisiting.

This chapter covers the twenty addressing directions **C.01–C.20**, the twenty deployed-use directions **D.01–D.20**, and the assigned source-access comparisons **R.03–R.08/R.13** in the [canonical 167-direction list](../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md). It follows the [scope contract](../PLAN.md), [original-scope audit](../05_review/ORIGINAL_SCOPE_AUDIT.md), and [coverage recheck R2](../05_review/COVERAGE_RECHECK_R2.md). The latter permits bounded synthesis, not an architectural verdict. Nothing here establishes a defect in FLUED: identifying a cause requires a competent target host, a valid intervention, and controlled observations in that host.

Four properties organize the comparison without forming an automatic implication chain:

| Property | Operational evidence | Distinct competing explanation |
|---|---|---|
| Recoverable content | A declared external reader predicts held-out targets from state | The reader learned a supervised mapping unavailable to deployment |
| Correct native return | The deployed query/interface returns the intended association | A downstream route ignores or substitutes for that return |
| Content-specific dependence | Valid A↔B content changes produce the corresponding answer changes | Generic context, scale, source identity, or intervention artifacts drive the effect |
| Task-correct benefit | Answers satisfy the specified evidence-authority policy and improve absolute quality against a budgeted comparator | A system follows false evidence, changes confidence without correctness, or benefits from extra training rather than memory |

The distinction between information and a permitted consumer has a formal counterpart in **W0092**, which defines usable information through optimal risk within a specified predictive family. Its optimum is not the result of a particular trained reader, and its statistical bounds do not guarantee neural optimization. The distinction between dependence and usefulness is empirically explicit in **W0050**: post-training channel removal, separately trained no-memory references, and document-versus-constant-input training estimate different quantities. These sources support separating questions, not diagnosing the present host. [W0092 · 2002.10689v1 · §2–4, App.A][w0092]; [W0050 · 2610.19373v1 · §3, App.C][w0050].

Evidence citations name stable card IDs and locked editions. PDF pages are given where established by the carrying card; older HTML-based cards retain their exact section/equation/table locators rather than invented pagination. Newly read cards, reused older cards, partial supporting material, and pending recent originals remain separate. This chapter synthesizes those cards; it does not claim another round of full original reading, replication, or proof certification. The [reading audits R1](../05_review/READING_AUDIT_R1.md) and [R2](../05_review/READING_AUDIT_R2.md) govern source conflicts discussed below.

## 2. Native query formation and read/write agreement

### 2.1 What is the query allowed to know?

“Query” can denote an input-conditioned vector, a fixed learned output request, a controller state after several reads, or an oracle supplied with the target location. These have different permissions. A native causal query may use only the deployed prefix and state available at its formation point. A training-only posterior, future answer, bidirectional suffix, or known supporting span is additional information even when the final evaluation uses a causal model.

**BR-A03-D02**, Dynamic Neural Turing Machine, is a direct address-learning example. A controller compares a generated key with memory cells containing both globally learned address vectors and episode-specific content. The address vectors remain fixed within an episode; writable contents reset. The authors observed that the model could exploit the fixed addresses as extra weights while neglecting useful episode content. Reading a previously written location is therefore weaker than reading the intended fact. Its overlap penalty, next-input prediction auxiliary, and soft-to-discrete curriculum are distinct learning interventions. [BR-A03-D02 · 1607.00036v2 · §2–4, pp.15–19][d02].

The quantitative controls resist an easy architectural story. On bAbI, three-step discrete and soft D-NTM mean errors are 21.79% and 24.24%, against MemN2N 4.24% and DMN+ 2.81%. A feedforward discrete controller improves from 68.30% error to 37.79% with curriculum, but feedforward and recurrent treatments have unequal training duration. Table 7's discrete system passes copy and fails associative recall, whereas the soft system passes both under the paper's in-training-length criterion. Address learning is possible, optimization matters, and neither result supplies a generic recipe. The paper's read/write state indexing is unresolved; that is an algorithm-description gap, not evidence that the implemented system read future information. [BR-A03-D02 · v2 · §6–9, Tables 1,3,7, pp.15,19][d02].

**BR-A03-D11**, End-to-End Memory Networks, supplies a positive contrast. Answer supervision trains soft access without supporting-fact labels. Each hop scores input memories with the current internal query, returns a weighted sum of output memories, and updates the query. The language-model version starts from a constant query of 0.1, then becomes content-adaptive through returned information. Thus useful query formation need not begin with an elaborate query encoder. However, the model repeatedly accesses an explicit bank of up to 50 QA sentences or 200 LM words; it does not demonstrate closed fixed-state retention. [BR-A03-D11 · 1503.08895v5 · §2,4–5, pp.2–7][memn2n].

### 2.2 Agreement means binding, not merely geometric similarity

Read/write agreement has at least three meanings: selecting a location previously written, matching marginal query/key distributions, and recovering the correct key–value association. A permutation of identities can preserve marginal distributions while destroying bindings. Conversely, a coordinate change can preserve the function despite making raw query/key vectors look different. A useful test must change fact identity, position, and payload independently where the representation permits legal combinations.

**W0229** makes the association explicit: fit a prefix regressor to key–value pairs and evaluate it at the current query. Its MQAR construction uses short convolution to arrange a previous symbol as key and the current symbol as value/query. Success depends on this learned or constructed interface, not merely on allocating a state matrix. Under its orthogonal, one-to-one cue–response setup, a suitable regression construction solves recall; this is not a claim about arbitrary semantic queries. [W0229 · 2501.12352v3 · §3,6, Eqs.8–9,56–58][w0229].

The recent **BR-A03-D20** strengthens evidence for native content paths in pretrained GLA/GDN. Donor writes, pre-query state substitutions, and query-time output patching connect written answer content to later four-choice recall. With four facts, target transfers reach 61–89% while non-target breaks are 0.4–1.4%; equal-norm random and control-head updates do not reproduce the same pattern. The results demonstrate useful selective effects under the tested task, not independent KV slots: state-direction interventions also produce opposing collateral margin shifts. Crucially, output patching intervenes after query formation. It cannot establish that q itself was correctly formed or identify a q-only remedy. [BR-A03-D20 · 2609.33093v1 · §2–3, App.B–C][d20].

This source also preserves a substantive boundary: its free-vocabulary prose pilot achieves recipient 56.3/71.9% and donor 53.1/68.8% at the two filler settings, below its own 80% competence criterion. That number is an author-specific assay prerequisite, not a threshold adopted here. The controlled four-choice result remains positive; semantic prose use remains unestablished by that experiment. [BR-A03-D20 · v1 · App.F.2][d20].

### 2.3 Isolating query reachability

A discriminating same-bank comparison begins with actual native q, then a bounded q-only adapter trained on legal task inputs, an equally trained unchanged/self-interface control, and a stronger diagnostic reader. Correct-address or ridge oracles belong in a separate diagnostic lane. Their success can show that a tested target remains accessible under stronger permissions; it does not establish a deployable query. Failure of several finite readers does not prove information loss.

Hold out source identities and bindings, not only phrasings. Evaluate exact cues, noisy approximate cues, paraphrases, role reversals, and relation joins separately. A q-only adapter that memorizes a small identity inventory has not solved shifted-query accessibility. This remains a direct experiment gap identified by C.06–C.08/C.18/C.20; neither more exact-key recall titles nor an oracle output rescue closes it. The relevant primary mechanisms are available, while the same-bank legal semantic comparison remains absent from the inspected packet. [W0092 · v1 · §2–4][w0092]; [BR-A03-D11 · v5 · §2,5][memn2n]; [BR-A03-D20 · v1 · §3, App.F][d20].

## 3. Address compression, payload grain, and replacement semantics

### 3.1 Four compression coordinates

Temporal grouping, feature width, numerical precision, and read-access structure should be recorded separately. Sharing a key across positions changes temporal address resolution. Truncating key features changes the scoring subspace. Quantizing keys changes numerical error. Sharing KV between heads or layers changes parameterization and storage duplication. None is synonymous with replacing token payloads by a summary.

**BR-A03-D19**, Thin Keys, Full Values, isolates feature-width reduction conceptually: retain full-width values, reduce query/key width, and optionally absorb an SVD factor into queries. For an approximated matrix `W_K ≈ AB`, the rearranged dot product is exact for `AB`, not for the discarded singular components. The source's subsequent equality notation needs this qualification, as do positional rotation, bias, and scale. Its finite-point projection argument and tiny retrieval task do not establish logarithmic key dimensions for arbitrary semantic queries. [BR-A03-D19 · 2603.04427v3 · §2–3, pp.2–8][thin].

Adaptation changes the apparent cost of this replacement. GPT-2 key-only rank 192 has roughly +26–27.6% raw relative perplexity, while matched-control QK fine-tuning reduces the reported gap to +1.8%. Query-only reduction at that rank is much worse, +181%. The fine-tuning uses three epochs over 10M WikiText-103 tokens; math repair adds 7,473 GSM8K examples. Those are informative recovery results, not training-free equivalence. With equal original K/V widths, removing 75% of key storage saves 37.5% of total KV, before other resources. The v3 conflicting GSM8K cells and v4 revised throughput figures remain edition-specific, not independent confirmations. [BR-A03-D19 · v3 · §3.1,3.4,8,11, Tables 8,18; v4 · §4.2, Table 11][thin].

### 3.2 Count-correct merging is a conditional operator identity

**BR-A03-D03**, Homogeneous Keys, Heterogeneous Values, merges adjacent low-attention positions using a diagonal-Fisher key approximation, sums values, and retains multiplicities. If keys within group g have already been made identical, softmax output can be written

`y(q) = Σ_g exp(q·k_g) Σ_(i∈g) v_i / Σ_g c_g exp(q·k_g)`.

Using mean values instead requires the corresponding count in the numerator. This is exact relative to the equalized-key bank; making unequal original keys identical is the approximation. The method needs a selective backward pass per compression chunk, and its inference gradient/label visibility remains an implementation-level clarification. [BR-A03-D03 · 2506.05410v2 · §3.1–3.3, Eqs.7–11, App.C p.22][asym].

Its MuSiQue 4×2 grid is useful evidence rather than a universal K/V ranking. Asymmetric values improve mean-key 18.93→21.86, cardinality-weighted 20.90→23.91, attention-weighted 14.99→23.83, and Fisher-derived 21.21→24.43. Yet cache-quality and peak-memory rankings differ: the reported Llama2-7B peak is 24,923 MB against H2O 22,479 and StreamingLLM 19,592. Appendix comparisons also have category-specific losses. This supports preserving value mass while changing addresses in that procedure; it does not supply a frozen-host K-only/V-only causal factorial. [BR-A03-D03 · v2 · §4.5–4.6, Fig.5/Table 4 pp.8–9, App.D p.23][asym].

The recurrent analogue needs a different derivation. Repeating a summary at many positions can repeatedly erase, correct, decay, or gate state. A single mass correction at read time does not match those transitions. DeltaNet writes a residual at each key, and GDN combines global decay with directional correction. Matching summary vectors while changing write frequency therefore changes the operator. Equal token counts, equal final norms, and equal numbers of logical facts are not interchangeable controls. [W0199 · 2102.11174v3 · §4.2, App.B][deltaold]; [W0201 · 2412.06464v3 · §3.1, Eq.10][gdn]; [W0228 · 2406.06484v6 · §2–3, App.B][deltanew].

### 3.3 A replacement factorial before a grain sweep

The following contrasts answer different questions and should precede attribution to block size:

| Treatment | Address path | Payload path | Main distinction |
|---|---|---|---|
| Exact replay | Original | Original | Does the intervention preserve the intact computation? |
| K-only | Altered/shared keys | Original position-specific values | Address degradation without intended payload loss |
| V-only | Original keys | Summary or donor values at specified positions | Payload replacement under unchanged scoring |
| Both | Same K alteration | Same V alteration | Interaction between address and payload changes |
| Count/update control | Declared mass or transition schedule | Same content as comparison | Repetition and normalization rather than grain |

A block-size-one replacement is not automatically identity if it introduces a projection, normalization, or different update order. Nor is every cross-world K/V combination valid: contextual keys and values may encode inseparable identity or positional information. Where legal binding cannot be preserved, call the result a joint interface perturbation rather than pure content damage. Grain then becomes a controlled axis: keep total bits, source permissions, update schedule, query family, and return width fixed where possible, and report which resource cannot be matched.

This design distinguishes replacement shock from grain and from adaptation. At each selected grain, record frozen performance and bounded repair, alongside equally adapted original/self-interface controls. Compare candidate improvement minus control improvement, not only recovery from the candidate's damaged start. No universal acceptable drop or training dose follows from these papers.

### 3.4 Separate routing changes from coadaptation

Merlin illustrates why routing and state reading need different query names. **W0210** builds fixed-length segment states plus first/second moments of dedicated routing keys. A dedicated routing query determines segment weights; a backbone query reads each segment state. Independent routing projections improve the tested comparison, but separate computation paths do not make the learned representations statistically independent. GDN Meanpool→Merlin improves 16K RULER 57.9→62.7, while one multi-key needle cell falls 48.4→45.0. Each arm is separately continued-trained, including synthetic recall/QA exposure, so this is a routing-design comparison under a common recipe rather than routing-only surgery on identical frozen values. [W0210 · 2610.37645v1 · §2–4, Table 2, App.C–E][merlin].

Its resource and timing details also matter. At 16K with 256-token segments, GDN state cache is 72.1× the single-state baseline versus 64× for position/mean routing; the additional moments are not the whole cost of multiple states. All visible segments are softly read, not sparsely skipped. The pseudocode uses a fixed segment denominator for a partial segment, unlike the main formula's observed-count normalization. That unresolved description limits exact online-normalization claims; it does not establish an implemented error. [W0210 · v1 · §3.1, App.C.5/D, Table 9][merlin].

GQA supplies an unusually direct replacement-by-adaptation contrast. Mean-pooling old KV heads, choosing one old head, and random new heads are compared after uptraining; at zero dose MQA degrades much more than GQA, and both improve with 5%, with smaller gains at 10%. Five percent costs approximately 600 TPUv3 chip-days beyond the original checkpoint and downstream fine-tuning. T5-XXL average development scores are MHA/GQA-8/MQA 47.2/47.1/46.6. This establishes a real recoverable conversion in an encoder–decoder host, not cheap arbitrary transplantation or a decoder-only result. [BR-A03-D12 · formal EMNLP 2023 · pp.4897–4900, Table 1/Figs.4–5][gqa].

Together, these studies motivate three distinct outcome curves: acute frozen replacement, recovery under a specified adaptation dose, and independently trained performance. A grain comparison must hold the adaptation opportunity within each curve; a routing comparison must disclose whether its value states also changed during training. Positive recovery can reject an intrinsic-loss explanation for tested content under that repair class. Failed bounded repair rejects that class and budget, not every possible reader. Neither outcome substitutes for comparing untouched-model continuation and original-content positive controls.

[merlin]: ../../flued_multigranularity_survey_20261108/03_reading/B06/W0210.md

## 4. Conditioning, normalization, scale, and gates

### 4.1 A better-conditioned system need not be a better native reader

In **W0229**, full linear least squares uses key Gram correction; basic additive attention substitutes an identity approximation. The distinction concerns the covariance of key dimensions and associated value statistics, not deletion of a few token positions. Gram inversion can improve a fixed regression problem, but the paper's switching nonstationary process gives a reversing control: unweighted RLS adapts poorly after dynamics change, whereas query-local regression adapts better. Retaining all old statistics can be harmful when the desired mapping changes. Its local-linear method also incurs substantial storage and solve costs and is not presented as a practical long-sequence implementation. [W0229 · 2501.12352v3 · §4–5, Eqs.10–13,42–55][w0229].

**W0212** further specifies when key geometry predicts retrieval. Its fixed additive outer-product memory queries the exact stored key and measures value cosine. With orthogonal unit values, interference depends on squared kernel overlaps; correlated values require their joint Gram matrix and can reinforce or cancel interference. ResNet→ViT prediction error falls from 0.113460 using key-only geometry to 0.004209 with joint value geometry. A CIFAR100 PCA-plus-whitening transformation changes the reported limiting cosine from 0.652 to 0.996, but simultaneously changes dimension and geometry. Appendix F finds no universal advantage from learned orthogonal addresses or sparse synthetic codes. [W0212 · 2610.09056v1 · §III–V, App.C–F][geometry].

These are meaningful conditional results, not finite-precision theorems or noisy-query guarantees. A low condition number, high spectral concentration, or improved ridge reconstruction must be paired with target-sensitive native returns. **W0086** illustrates why average language quality is insufficient: after 50% GDN state reduction and recovery, WikiText perplexity improves 16.8→16.3, but LAMBADA worsens 9.7→12.0 and 4K RULER falls 38.8→27.5. State rank, average prediction risk, and retained rare associations measure different things. [W0086 · 2602.04852v3 · Tables 1,4, App.F][prune].

### 4.2 Normalize directions and control temperature independently

**BR-A03-D13**, QKNorm, replaces unbounded dot products with unit-norm q/k cosine scores and a learned scale. Its largest ablation is informative: removing learned g gives 24.53 BLEU against 33.24 for the full setting; normalizing V as well gives 32.34. Without scale, many candidates compete through logits restricted to a narrow interval. Directional normalization can therefore make attention too diffuse even when it improves numerical behavior. [BR-A03-D13 · formal Findings EMNLP 2020 · pp.4248–4253, Tables 2,6][qknorm].

The main reported +0.928 average BLEU comparison also changes LayerNorm/ScaleNorm and warmup, so it is not a normalization-only causal estimate. Its head-count sweep is nonmonotonic: 2/4/8/16/32 heads yield 32.40/33.16/33.24/32.42/32.30 in the specified translation task. Neither eight heads nor its sequence-length-derived temperature initializer becomes a default for a different memory system. [BR-A03-D13 · formal edition · pp.4250–4253, Tables 2,4–6][qknorm].

For whitening or centering, distinguish a paired coordinate transformation from a functional change. If the scoring inner product is to remain invariant under an invertible key transform, the query must receive the compatible inverse-transpose transform. State and output conventions may need corresponding changes. One-sided whitening deliberately changes similarity. Fit statistics on training sources only; otherwise test-distribution information enters the operator. Measure logits, angular margins, norms, denominator mass, return amplitude, and final content dependence separately.

### 4.3 Gates can alter consumption without altering addresses

**BR-A03-D15** places a query-dependent, head-specific sigmoid after the attention-weighted return. That gate does not change the current softmax logits. In its MoE ablation, baseline perplexity is 6.026, output-elementwise gating 5.761, headwise gating 5.792, value gating 5.820, q gating 5.981, and k gating 6.016. A one-expert value-gating control reaches 5.808, showing that routing among multiple experts is not required for the observed gain. [BR-A03-D15 · 2505.06708v1 · §2–3, Tables 1,6][gated].

Output gating and value gating also differ: first-token attention changes from baseline .467 to .048 with output gating, but remains .297 with value gating despite reduced large activations. These observations separate candidate mechanisms; they do not prove that a particular fact was used. Long-context results require an additional 80B-token continuation. A useful target-host test holds logits and bank fixed, changes the post-read gate, includes a matched-return-norm control, and asks whether correct-versus-wrong value dependence changes. Stronger stability or lower sink attention alone cannot identify content consumption. [BR-A03-D15 · v1 · §4, Tables 4–5, App.A][gated].

## 5. Slots, heads, depth, and iterative reading

### 5.1 Independence has several resource meanings

Independent q vectors, independent KV projections, independent resident states, independent write policies, and independent semantic contents should not be counted as the same capacity. GQA retains H query heads while sharing G KV groups. LRKV retains independent queries and combines a full-width shared KV base with head-specific low-rank corrections. MoM has multiple state matrices but uses a shared q after linear mixing. For a shared linear read, mixing states before reading is algebraically equivalent to mixing their reads. A change in that setting cannot be credited to query diversity that is not present. [BR-A03-D12 · formal EMNLP 2023 · pp.4896–4898][gqa]; [BR-A03-D17 · 2601.11471v3 · §3, Eqs.2–9][lrkv]; [W0204 · 2502.13685v4 · §3.2–3.3][mom].

MoM's active-state-matched comparison improves mean recall 26.32→28.16, but SQuAD falls 30.03→29.69 and NQ 17.74→16.60. Activity matching does not match total resident state, projections, or parameters. Triadic attention increases recurrent state by factor E and binds values to two keys, with scores factoring into two query–key products. Its E=4 GDN recall 31.1 exceeds base 26.2 and larger-head 28.5, while a hybrid comparison favors larger-KV recall 45.3 over Triadic 44.5. The tensor can be flattened into a joint-key matrix; tensor order does not demonstrate a persistent relation object. [W0204 · v4 · Tables 4,9–10][mom]; [BR-A02-N03 · 2609.36529v1 · §2–3, Tables 1,3][triadic].

LRKV's useful design should be separated from its unresolved cache ledger. Appendix G prints 48/72 MB beside 52.6%, although that displayed ratio is 66.7%; other displayed MB ratios also disagree with percentages. Per-scale ranks elsewhere partly explain main-table percentages but not the appendix's separate rank-64 description. Rotation through factor matrices likewise needs an implementation-compatible construction. These are source arithmetic/positional ambiguities, not proof that low-rank sharing is invalid. [BR-A03-D17 · v3 · pp.24–25,29, Tables 7,8,12][lrkv].

### 5.2 Fewer writers are not fewer reads

Cross-Layer Attention has one KV producer for a group of layers and separate q projections in later readers. It reduces duplicated persistent cache, while each reader still accesses the shared bank. At 1B, MQA-CLA2 and narrower-head MQA both use 5,120 bytes/token, with perplexities 13.60 and 13.81 before the separately reported learning-rate sweep. At 3B, a tuned CLA2 setting gives 9.34 versus memory-matched MQA 9.48, but downstream results have mixed winners. End-to-end serving acceleration is unmeasured. This is one-writer/many-reader sharing, not independent layers writing a common summary or mixing residuals across depth. [BR-A03-D04 · 2405.12981v1 · §2–4, Tables 1,3,5–8][cla].

MHLA instead retains multiple block summaries and applies learned block-index mixtures. Its coefficients are not shown as an input-conditioned router. Its printed intra-block expression lacks an explicit token-triangular mask, while prose describes incremental inference; therefore actual token causality needs implementation/prefix evidence, not an accusation of demonstrated leakage. Main and appendix training-data descriptions also conflict. Its unmasked rank argument cannot simply be transferred through causal masking, which can increase matrix rank. [W0219 · 2601.07832v2 · §4, App.C–D/G, pp.9–11][mhla].

### 5.3 Iteration can refine, reason, or converge to the wrong answer

MemN2N's 1/2/3-hop joint bAbI errors of 25.8/15.6/13.3% are positive adaptive-read evidence; path-finding nevertheless remains at 90.2% error in the specified three-hop setting. Ten restarts are selected rather than averaged, and equal-extra-compute nonread controls are absent. Slot Attention shows another mechanism: competition is normalized over slots, then a weighted mean over input positions updates each slot through a shared GRU. More test slots/iterations can improve image grouping, but increase storage/compute; one Tetrominoes run stuck in stripes is excluded from the reported aggregate. Neither is a fixed-bit causal text-memory superiority result. [BR-A03-D11 · v5 · p.6, Table 1][memn2n]; [W0100 · 2006.15055v2 · §2–4, p.6, App.B–C][slots].

Hopfield attention supplies conditional one-step recovery bounds with separated patterns and sufficiently close queries. Its explicit pattern bank costs O(Nd); correlated clusters can produce averaging or metastable states. Feeding arbitrary independent values back as new queries does not automatically inherit the original energy-decreasing dynamics. [W0240 · 2008.02217v3 · §2, App.A.1.4–A.1.8/A.4][hopfield].

A clean iteration comparison fixes the same bank and initial q: one read; repeated identical-q reads; adaptive q updates from previous returns; and equally costly transformation without another read. Separate parameter tying, fusion width, and temporary states. Exact lookup, noisy completion, and relational joins should each be scored. Improved output with unchanged address margins can reflect reasoning rather than better access; sharper wrong margins can reflect attractor amplification.

## 6. Probe evidence, restorative interventions, and deployed use

### 6.1 Probe success is a learning result with its own budget

MDL probing measures label-coding cost conditional on representations, not only endpoint accuracy. In **W0370**, an ELMo layer-0 probe obtains real/control accuracies 93.7/96.3%, yet online codelengths are 173/302 kbits; at layer 1 they are 96/515 kbits. A control task can be memorized accurately while requiring substantially more supervision. Random contextual layers also retain pretrained lexical embeddings, so they are not fully random-input baselines. Probe architecture, labels, spans, training, selection, and seeds must travel with recoverability claims. [W0370 · formal EMNLP 2020 · §2–4, PDF p.6/Table 1, App.B][mdl].

Restorative tests strengthen some causal claims but can change the system. In **W0372**, amnesic projections remove linearly recoverable properties and compare same-rank random damage. For masked dependency, targeted and random projections both reach 4.67% from 56.98%, removing 820 dimensions; adding gold labels and retraining reaches only 20.46%. That condition does not establish target-specific damage beyond random destruction. Conversely, coarse-POS label addback exceeds the original baseline, demonstrating that new labels and adaptation can add capability rather than merely restore a clean interface. [W0372 · formal TACL 2021 · §2.3,5–7, Tables 1–2][amnesic].

**W0374** improves intervention validation through independently trained target and non-target probes. Its formal six-model study finds completeness–selectivity tradeoffs, with nonlinear counterfactual methods usually stronger but late BERT AlterRep exceptions. In that BERT setting, AlterRep reliability .8346 exceeds FGSM .5518; these are independently optimized intervention strengths, not equal perturbation norms. Independence from the surgery probe is valuable, yet hidden-state gold after intervention remains unavailable and unmeasured properties may change. The older BERT-only conclusions cannot be spliced into the later multi-model study as one unchanged experiment. [W0374 · formal IJCNLP-AACL 2025 · §3–6, App.C.1–C.5][reliability].

### 6.2 A successful learned intervention need not reveal native access

RAVEL trains a subspace intervention with donor activations and counterfactual labels while freezing the base model. Cause changes a target attribute; Iso preserves enumerated non-target attributes. MDAS improves aggregate disentanglement over DAS, but verb-Entity gives 49.5 versus 51.8, with Iso 90.2 and Cause only 8.8. High preservation can coexist with almost no intended target change. Entity and context holdouts are separate, not joint; source wording about layer selection remains unresolved. [W0531 · 2402.17700v2 · §2–4, pp.17–19, Tables 4,6][ravel].

The recent latent-strategy source provides a complementary learning route. **BR-A08-V17** adapts a decoder with a latent pseudo-token, a response-aware training posterior, and surprisal-weighted reconstruction. Inference routing sees only input, but the decoder still sees input and previous output. Its valid-trace fidelity is not equality of full response distributions; inverse-surprisal controls and lost low-surprisal fidelity delimit the objective. This is evidence for changing training incentives under a specified task, not proof of a bottleneck-only memory or spontaneous latent use in an unchanged host. [BR-A08-V17 · 2607.17674v1 · §3–5, Apps.D–F][latent].

The useful sequence of questions is consequently: what content can a declared reader recover; what does native read return; what causal change follows a legal content substitution; and does that change improve the task? Success at one stage motivates the next measurement rather than replacing it.

## 7. Natural counterfactuals and negative controls

Natural input changes and internal substitutions answer complementary questions. A natural A/B pair recomputes the whole system and estimates the effect of a task-valid changed world. A local state swap holds other parts fixed and targets a particular interface, at the cost of a potentially unnatural hybrid. Agreement strengthens interpretation; disagreement can reveal recomputation, binding mismatch, or intervention artifacts rather than choosing a winner by fiat.

**W0373** makes naturalism operational rather than rhetorical. Spanish gender/number interventions repair dependent determiners, adjectives, verbs, and contractions through dependency-tree transformations. Gender analysis restricts animate nouns because fixed-lemma positivity fails for many lexicalized genders. Even grammatical changes can be semantically implausible. One native speaker's check finds 73% accuracy over 100 transformations, with 76% gender and 70% number. Its backdoor argument requires the stated graph, positivity, valid transformation, and sampling assumptions; those do not make heuristic outputs perfect. [W0373 · formal TACL 2023 · §3–5, Apps.B–C, PDF pp.9–12][natural].

Activation-patching evidence quantifies why corruption choice matters. In **W0533**, Gaussian noise yields factual peaks 2–5× sharper than symmetric replacement, while arithmetic tasks can show the reverse. For one IOI contrast, logit difference detects positive heads 9.6/9.9/10.0 and negative heads 10.7/11.10, whereas probability detects only positive 9.9. Joint 3/5/10-layer windows also exceed summed single-layer effects by 1.40/1.75/1.59 in the specified comparison. A joint window cannot localize its whole effect to the midpoint layer. [W0533 · 2309.16042v2 · §3–6, pp.4–7,19/Table 4][patching].

The compiled X-Proportion counterexample in **BR-A04-N01** is especially decisive for null interpretation: positional information constant across donors survives resampling but is removed by zeroing. The appropriate ground-truth circuit changes with the intervention. A donor distribution that never varies the target feature cannot establish that the feature is unused. Restoration and complement destruction also restrict different paths; the operator must match the claimed necessity or sufficiency. [BR-A04-N01 · 2407.08734v1 · §3–5, pp.6,20–21][robust].

A practical semantic control family is:

| Intervention | Desired endpoint under a declared closed world | Confound addressed |
|---|---|---|
| Replace target value consistently, preserve key and unrelated fact | Answer follows new value; unrelated answer remains stable | Target-content specificity |
| Paraphrase unchanged fact | Semantic answer stays invariant | Surface matching rather than content |
| Swap relation roles with the same value bag | Answer changes according to binding | Bag-of-values shortcut |
| Change irrelevant same-format fact | Target answer stays invariant | Generic channel/scale sensitivity |
| Delete all supporting evidence | Abstention or declared no-answer behavior | Prior guessing mistaken for evidence use |
| Add a contradiction | Conflict handling under the specified policy | Unconditional copying |
| Same-state replay and donor-positive recovery | Intact function and detectable intended effect | Broken or insensitive assay |

Match length, position, byte/script class, and norm where relevant, but report residual differences instead of claiming an impossible perfect match. Screen negative donors for actual answer content; W0050's donor paragraphs were not guaranteed answer-free. A natural donor marginal does not certify the joint hybrid, and a norm-matched random vector is not a semantic counterfactual. Both remain useful when named accurately. [W0050 · v1 · §5.2, Apps.K/Q/S][w0050]; [W0374 · formal edition · §3–4][reliability].

## 8. Mediation, redundancy, and self-repair

For two specified routes A/B under one background and score, record all four outcomes and compute `I = Y11 − Y10 − Y01 + Y00`. This is exact background-specific nonadditivity. It is not a unique share of information, proof of global increasing returns, or proof of a particular backup mechanism. Static duplicates, conjunctive cooperation, saturation, and downstream compensation can produce overlapping patterns.

**BR-A04-R08** shows why noising and denoising need not agree. For clean a, corrupt b, and mediator M, its four structural evaluations give a restoration effect, a destruction effect, and their interaction. L9H9 has restoration +2.575, interaction −2.338, and noising +.237 logit-difference units. Individual backup-pair effects reach only 7.1% of its interaction, while some group contrasts are much larger. Table 2 gives L11H2 pair/group interactions +.013/−.596, even changing sign. Exact finite differences require no differentiability; interpreting a local mixed-Hessian approximation requires smoothness and local scope, and path-specific language requires the stated graph/freezing convention. [BR-A04-R08 · 2606.27510v1 · §3–5, pp.17–18, Tables 1–3][mediators].

The original IOI circuit supplies a concrete redundant-route control. Ablating three name movers reduces logit difference only about 5% because other heads compensate. Its 87% fidelity result does not establish completeness: greedy mixed-group tests expose a gap up to 3.09 against baseline 3.56, despite random/group tests looking stronger. Group-conditioned minimality is therefore different from unconditional single-node necessity. The selected groups and thresholds also need independent evaluation if transported into a new assay. [BR-A04-N09 · 2211.00593v1 · §3–4, pp.10–11, Apps.J–M][ioi].

Hydra distinguishes a component's direct contribution from the total effect after downstream reaction at fixed weights. At layer 23, r²=.92 with slope .69 describes variance explained and incomplete logit compensation, not 92% restored task accuracy. Attention-response r²=.13 and MLP-response .87 further separate responses. Its outcome is the intact model's preferred token, not necessarily a verified fact. Thus compensation is observed in that host, but semantic identity restoration requires an additional task-correct test. [BR-A04-R02 · 2307.15771v1 · pp.9–14, Figs.7–8][hydra].

**BR-A08-V19** extends factorial entry interventions to evolving memory and simulated question feedback. Later trajectories evolve independently; it is not an intervention fixing every later path. Of 144 constructions, only successful-corruption/clean-counterfactual cases remain: 125 and 120 for the two hosts. In one oracle repair comparison, residual probe effect changes .178 without repair to .129 question-only, .053 memory-only, and .003 jointly. This is meaningful restoration under access to clean counterfactual dialogue/memory, not a deployable correction policy. The construction supplement remains missing, so the source stays PARTIAL despite its read body. [BR-A08-V19 · 2608.30198v1 · §4–5, Table 2][errors].

For D.06, distinguish current-position self contribution, nearby context, and genuinely remote evidence before combining them into a route score. In a write-before-read recurrence, the current token can enter the state immediately; a correct output need not demonstrate retention of an old fact. Query text may also repeat the answer or provide an easy local completion. A proposed local×remote factorial should preserve the question's meaning while independently varying local answer leakage and the remote binding. Record whether recomputing local context also changes remote KV construction or q. If those channels cannot be varied independently, report a joint treatment instead of additive self/local/remote information shares. BR-A03-D20's hybrid boundary result—over 99% of its normalized pre-query donor effect lies in KV—does not exclude recurrent influence on earlier writes or subsequent queries. [W0199 · 2102.11174v3 · §4.2][deltaold]; [BR-A03-D20 · 2609.33093v1 · §4, App.A][d20].

A target-host redundancy test should first demonstrate competence, then compare individual routes, a functionally justified whole-route group, and matched random groups. Observe the initial returned content and downstream target-related changes. Holding downstream variables fixed estimates another effect than allowing natural compensation; report both when feasible. Pairwise screens guide group selection but do not certify exhaustive mediation. Rescue after damage narrows explanations for that repair class; it does not uniquely reconstruct the original cause or its training history.

## 9. Correct use requires an authority policy and an honest score

FaithEval and ClashEval ask different questions. FaithEval instructs models to follow supplied context, say unknown when unsupported, and conflict when evidence disagrees. Its counterfactual context deliberately supports a world-false answer. ClashEval treats erroneous sources as a hazard and tests both correct-prior/wrong-source and wrong-prior/correct-source strata. A system that always follows context can succeed under one stipulation and fail under the other. [BR-A04-N07 · 2410.03727v3 · §3, Apps.A–D][faith]; [BR-A04-N08 · 2404.10198v3 · §3, pp.6,9][clash].

The numbers show the cost of collapsing these contracts. FaithEval reports GPT-4o closed-book 96.3% versus counterfactual 47.5%, while conflict prompting reduces normal-context GPT-4o .85→.83 and Claude .90→.85. Its answer-mention matching, including a permissive unknown keyword list containing “not,” is weaker than whole-response entailment or exclusive endorsement. ClashEval's GPT-4o chooses wrong context .608 when its prior is correct, and correct context .903 in the reverse stratum. Aggregate context bias .304 is plausibly half the conditional rate under balanced strata, but exact code/denominators remain unreconciled. Calibration improves aggregate accuracy .615→.754 while prior bias rises .021→.085. These are tradeoffs, not universal truth recognition. [BR-A04-N07 · v3 · pp.6–9, Table 1, App.A][faith]; [BR-A04-N08 · v3 · Tables 2–4, p.9][clash]; [reading audit R2 · §3.4](../05_review/READING_AUDIT_R2.md).

ERASER supplies deletion/retention metrics for the original predicted class, not gold correctness: comprehensiveness measures confidence lost when the rationale is removed; sufficiency measures how much confidence is lost when only the rationale remains. These can reveal useful behavior without identifying its semantics. Goodhart's counterexample trains a detector to recognize intervention cases and manipulates those scores. Detector accuracy ranges 77.5–99.8%, and some untouched-input F1 scores change, so perfect preservation is conditional, not universal. Nevertheless the concrete inflation demonstrates that optimizing the evaluator can diverge from improving explanation. [BR-A04-R04 · formal ACL 2020 · §4.2, PDF p.8][eraser]; [BR-A04-R05 · 2308.14272v1 · §3–4, pp.15–17, Tables 2–6][goodhart].

W0050 contributes a positive anchor: QASPER document-input training yields 19.98 F1 against trained constant input 12.54 and shared zero input 6.82, with reported content benefit +7.43 [6.15,8.75]. Both genuine document benefit and non-document channel effects exist. Its gold supplied evidence does not test retrieval, and its unequal training references plus missing supporting PDF preclude a clean nine-system ranking. Dependence, content specificity, absolute quality, and reference-system utility should be reported side by side. [W0050 · 2610.19373v1 · §3–5, Apps.C/J/O][w0050].

## 10. Source-enabled navigation, omissions, and fair competitors

### 10.1 Fixed fine access remains a strong baseline

Source retention grants information unavailable to a closed compressed state, so compare explicit permission contracts before comparing frontiers. Within a source-enabled contract, retain strong flat retrieval, original-value fine chunks, and stronger readers before attributing gains to hierarchy or learned granularity.

SSA selects gist-addressed blocks and then attends to their original token KV. Hierarchical SSA adds meta-gists but does not uniformly win: at 32× continued training, SSA scores 44.07 versus H-SSA 42.56; after fine-tuning the order reverses, 43.35 versus 44.94. Selected gist-plus-original 53.39 versus original-only 52.76 is a small setup-specific comparison, not proof that every gist detail is consumed. Its decode implementation also scans all-position byte metadata despite ideal logarithmic routing analysis. [W0162 · 2604.20920v2 · §3–4, Tables 3,6–7, App.A–B][ssa].

ReadAgent compares parallel page selection and sequential rereading. QuALITY gist-only 77.52% improves to parallel one-page 84.13%, parallel two-page 86.16%, and sequential up-to-six 87.17%, against full text 85.83% and neural top-three retrieval 83.41%. These are meaningful positives for selected original access, but not equal-call comparisons. On QMSum, sequential 46.57 versus parallel 39.09 uses up to six times the selection requests. The reported 20.4% processed-word saving is amortized over multiple questions per document, not a universal serving saving. [W0138 · 2402.09727v3 · §3–4, Tables 1–4, App.I][readagent].

### 10.2 Backtracking is real; calibrated omission recovery remains open

MemWalker can return to a parent and choose another branch. Its 15.0/18.6/18.8% backtracking-path proportions and corresponding final correctness 70.0/59.6/79.0% describe attempted paths, not recall of all initially missed evidence. Original QuALITY last-context 70.1% exceeds MemWalker 67.4%; a strong retrieval/navigation comparison must retain that negative. ReadAgent explicitly reports summary omissions, premature no-reread decisions, and hallucinations. [W0139 · 2310.05029v1 · §3–5, Tables 2–4][walker]; [W0138 · v3 · §5, App.H–I][readagent].

Self-Route falls back to long context when the model says unanswerable. Its table-level GPT-4o average 48.89 slightly exceeds long-context 48.67, while Gemini 46.41 trails 49.70. The paper does not measure confidently accepted cases that should have fallen back. Its paraphrased PassKey RAG collapse 80.34→4.58, against long-context 65.25→69.32, is a direct query-formulation countercontrol rather than evidence that all flat retrieval fails. [W0185 · 2407.16833v2 · Tables 1,3,7, §5.2][selfroute].

DRAGIN legally uses provisional generated tokens to detect a need, rewinds, retrieves, and regenerates. That is extra speculative work, not future ground truth. Llama-13B Hotpot improves EM/F1 .263/.3706→.314/.4238 over single-round retrieval; IIRC reverses .196/.2303→.185/.2221, and 7B StrategyQA no-retrieval .659 exceeds DRAGIN .641. Retrieval counts differ across methods and tasks. Entropy/attention is an observable trigger, not calibrated detection of evidence absent from the current representation; confident misses, irrelevant reads, and hard-cap failures remain required denominators. Its threshold/label table tension stays unresolved. [W0450 · 2403.10081v3 · pp.7,15, Tables 2–3,9, App.D][dragin].

Mnemis shows a different competitor: similarity retrieval plus hierarchical graph navigation reaches 93.3 versus similarity-only 89.1 in the specified LoCoMo comparison, but its global-only 87.7 is averaged over 1,387 returned questions rather than all 1,540. Build prompts reach tens of millions of tokens, and hierarchy construction and selection incur additional calls. Raw-chat search supplies another strong alternative, with ReFind macro-average 58.2 versus single BM25 48.8, yet multi-hop update integration only 8.8 and much larger processed-token budgets than a generic iterative comparator. Neither summary structures nor raw search receive a free cost advantage. [W0449 · formal ACL 2026 · pp.23914–23928, Tables 3–4][mnemis]; [W0124 · 2608.12888v1 · §4–5, Tables 2,11][raw].

A strong-reranker study also prevents treating candidate-pool elaboration as the default improvement: full F1 .548 versus no-RAPTOR .523 has test significance but reversed development direction, so it fails that study's stability rule. Removing graph expansion gives .542, not a proven equivalence to .548. Its no-reranker collapse additionally mixes incompatible score sources, so it does not isolate reranker quality alone. [W0156 · 2606.28367v1 · §5–8, Tables 2–3][rerank].

### 10.3 Utility identification is not omission confidence

Random exposure can reveal low-ranked useful items, but **BR-A08-V18** unions assigned items with deterministic retrieval; assigned exposure and realized inclusion differ. Appendix H.1 has 90 inclusions and zero exclusions for one item. The resulting support gap qualifies identification claims, not the entire estimator family. Exposure AUC improves .542→.664 in an oracle-enriched candidate pool, while mean answer F1 changes .223→.197. Current-query marginal value depends on displaced items and companions; it is not a future-retention or closed-loop policy certificate. [BR-A08-V18 · 2610.02070v1 · §3, Apps.C/E/H][cmp].

For R.03–R.08/R.13, the unresolved comparison is precise: same source pool, fixed-fine original values versus learned grouping; flat versus hierarchy; parallel versus serial access; observable no-gold trigger; confidently wrong stops; unnecessary fallback; and complete construction, reading, regeneration, and failure costs. Include equal-compute no-read and same-source stronger-reader arms. If two hidden worlds yield identical observed summaries but require different answers, an omission detector needs some additional discriminating observation or must retain uncertainty. This is a statement about that observation contract, not a universal theorem that source revisiting is necessary.

## 11. Statistical validity and training-time tracking

**BR-A04-N11** turns circuit claims into explicit tests against input and random-circuit references. Its sign-balance test is not a magnitude-equivalence test; exact ties make it inapplicable in a compiled example. Its independence null can remain unrefuted because of low power, and the paper explicitly does not study Type II error. Random-reference superiority is not reproduction of the intact model. The v1 Table 1/App.E conflicts over pass marks and docstring minimality remain source ambiguities rather than corrected results. No inspected positive establishes nonlinear conditional-redundancy sensitivity. [BR-A04-N11 · 2410.13032v1 · §3–5, pp.5–9,15,17,21–22][testing].

**BR-A04-N12**, Certified Interventional Fidelity, addresses a different problem: confidence for a fixed bounded mean over declared input/intervention laws. Predictable adaptive proposals require support and recorded weights; changing the selected circuit or target after inspection requires additional selection control. Its clipped recovery score changes the estimand by hiding negative effects and over-recovery. Raw gaps and denominator handling remain necessary. [BR-A04-N12 · formal UAI 2026 · pp.212–214, Apps.C–D][cif].

The reported sample savings are conditional: one IOI certification uses 102 betting versus 1,875 Hoeffding samples, while failure-exclusion medians are 88 i.i.d., 201 static-adaptive, and 118 history-adaptive; a borderline condition takes 1,217 i.i.d. versus 3,800 history-adaptive. Adaptive sampling is not uniformly better. Statistical precision cannot validate semantic donors or rescue an insensitive score. [BR-A04-N12 · formal edition · pp.217,227, Tables 3,6][cif].

D.20 therefore remains a longitudinal experiment obligation. Track the same held-out source/binding families across available checkpoints: native return quality; correct/wrong-content dependence; task-correct answers; collateral effects; and fixed instrument controls. Separate discovery items from evaluation items and preserve clustering by source/entity. Treat checkpoint, hypothesis, and intervention selection explicitly; use fixed evaluation or a justified sequential method. Sparse snapshots censor onset and disappearance, and missing history cannot be inferred from endpoint non-use. A decline in a circuit score can reflect extraction instability, changed reference sensitivity, replacement, or compensation rather than lost content.

## 12. Decision map and precise remaining gaps

The evidence supports mechanisms and discriminators, not a preferred architecture:

| Competing explanation | Cheapest informative contrast | Interpretation boundary |
|---|---|---|
| Wrong q versus inadequate retained content | Same-bank native, equal-permission q repair, stronger diagnostic reader | Repair supports accessibility for tested targets; failed readers do not prove erasure |
| Address damage versus payload loss | Replay/K-only/V-only/both with legal bindings | Invalid mixed joints remain ambiguous |
| Grain versus repeated update/mass | Fixed summary with frequency/count-correct operators | Softmax count identities do not match delta transitions |
| Conditioning versus scale/gate failure | Paired-coordinate, temperature, norm, and post-read controls | Improved spectrum alone is not native content use |
| More independent access versus more storage | Same-bank q diversity first; then equal-bit layouts | Active-state matching is not total-bit matching |
| Better iteration versus extra computation | Adaptive read/fixed-q repeat/equal-compute no-read | Gains may be reasoning rather than access |
| Non-use versus redundant/compensating use | Single and justified group interventions plus downstream response | A four-cell interaction is not a unique information share |
| Missing evidence versus poor authority handling | Valid source swaps, no-answer/conflict, both prior/source truth directions | Any answer flip is not necessarily correct |
| Useful navigation versus extra source/calls | Strong flat, fixed-fine, parallel/serial and full cost ledger | Source retention changes the information contract |

Closed-state alternatives remain live: task-sensitive writing and retention; improved legal query formation; paired q/k conditioning; independent read queries over a shared bank; count-correct aggregation; post-read integration; objectives that reward target content; and bounded adaptation of the existing interface. Their costs include statistics, parameters, training labels, optimization opportunity, repeated reads, and transient state. Source-enabled flat or hierarchical access competes under an explicitly richer retention contract. Absence of an inspected decisive comparison is a reason to preserve alternatives, not select one.

For navigation, the complete C/D direction coverage is explicit below. Section coverage means a bounded synthesis or specified unresolved test, not a solved question.

| Canonical coordinates | Distinct questions retained | Main sections |
|---|---|---|
| C.01–C.05 | Content/position; per-position/block; address/payload compression; K/V controls; read/write binding | 2–3, 5 |
| C.06–C.08 | Native q formation; visible information; query expressivity versus target complexity | 2, 6 |
| C.09–C.13 | Conditioning; normalization; centering/whitening; scale coupling; gate location | 4 |
| C.14–C.17 | Slot access; head specialization; layer writers/reuse; initialization/reachability | 3.4, 5 |
| C.18–C.20 | Offline/native gap; iteration; exact/approximate/relational targets | 2.3, 5–6 |
| D.01–D.05 | Probe/native; return/final use; hit/use; specific/generic context; copying/semantics | 1, 6–7, 9 |
| D.06–D.10 | Self/local/remote; hybrid shift; zero/shuffle; natural/latent changes; content/address damage | 3, 7–8 |
| D.11–D.15 | Mediation; redundancy; compensation; necessity/sufficiency; intervention grain | 7–8, 11 |
| D.16–D.20 | Metric gaming; task-quality divergence; deletion/contradiction; negative controls; training trajectories | 7, 9–11 |

### 12.1 Returned evidence and its C/D scope

**Evidence snapshot, 9 November 2026:** [coverage recheck R3](../05_review/COVERAGE_RECHECK_R3.md) supersedes the earlier blanket V17/V18 pending description. The returns contain two fully read independent recent preprints and one fully read 2009 predictive-state learning original. Separately, six V17 and five V18 official anonymous bodies each have recorded HTTP 403 dispositions; none was acquired. Those access receipts establish source status, not scientific findings or manuscript equality. [V17 returned summary](../03_reading/V17/BATCH_SUMMARY.md); [V18 returned summary](../03_reading/V18/BATCH_SUMMARY.md).

**BR-R2-T03**, public *Online Tokenization with Optimal Delay in Linear Time*, defines stable output as the token prefix unchanged under every possible continuation, providing a precise comparator for commit/flush and causal-interface claims. Its practical measured implementation nevertheless waits for a completed pretoken, unlike the strongest low-delay construction; an unfinished pretoken can grow arbitrarily. Reported first-formed-token speedups of 7.9–34.8× are tokenizer measurements, not end-to-end model latency, and optimized serial gigatoken wins several throughput cells. This sharpens the interface-permission and cost checks in §§3/10 without supplying learned query formation, memory-addressing, or content-use evidence. The official title says **Near Linear Time**, so even title equality is absent. [BR-R2-T03 · 2610.19139v1 · printed pp.3,13–16,40–41, §7/Tables 1,3,6][online].

**BR-R2-T05**, public *Cross-Tokenizer On-Policy Distillation via Byte-Prefix Marginalization*, makes teacher/student supervision alignment explicit: a byte trie partitions teacher next-token mass into student-prefix cells plus residual mass. Conditional exactness assumes lossless concatenative byte decoding and idealized greedy longest-prefix student segmentation; cross-teacher-token spanning uses a realized-path lower bound, not unrestricted byte-string probability. Its whitespace control is directly relevant to D's distinction between local matching and task function: unmasked code pass falls 49%→9%, with 84% block-indentation errors; mask-matched random removal does not recover the same code-tail result. The 20k-prompt math/code adaptation, masked rows, teacher passes, stopping treatment and 62–90% cap rates in one pair limit transfer. These findings sharpen supervision/interface controls in §6, not remote semantic memory or native consumption. [BR-R2-T05 · 2607.22334v1 · pp.3–9,15–18,27, App.C/H][bpm].

**BR-PSR-0912.2385** now supplies learned identification rather than existence alone: spectral estimates recover transformed predictive state under finite-rank, rich-feature/history coverage and nonsingular moment assumptions, followed by closed-loop planning. Future tests specify action interventions; they do not reveal realized future observations. The learned policy succeeds in 78/100 trials, with 18.2 actions averaged only over those successes; 22 trials fail. A five-dimensional deployed coordinate vector accompanies 2,000×2,000 moments, observation operators, reward regression and an 8,000-point planner. This is a useful prediction-versus-control and conditioning example for §§2/4/9, not a causal language-reader result, arbitrary-query guarantee, or recent ICLR advance. [BR-PSR-0912.2385 · 0912.2385v1 · pp.2–6,7–9/Figs.1–2][psrlearn].

[online]: ../03_reading/V17/BR-R2-T03.md
[bpm]: ../03_reading/V17/BR-R2-T05.md
[psrlearn]: ../03_reading/V18/BR-PSR-0912.2385.md

### 12.2 Remaining source and decision gaps

- **Scientific experiment gaps:** same-bank causal query formation for shifted semantic/relational queries; exact binding preservation under grain changes; fixed-total-bit slot/head comparisons; independently calibrated grouped-redundancy sensitivity; and longitudinal task-correct content dependence in the target host. The three returned editions do not close these comparisons. In particular, a non-rejected test without a sensitive semantic/grouped positive does not establish absence of native use.
- **Artifact/description gaps:** D-NTM state order; key-merge gradient visibility; LRKV/Thin Keys rotation and cache/score reconciliation; MHLA masking/index extension and data dose; RAVEL site selection; ClashEval prompts/matcher/denominators; and W0050/V19 carrying supplements. More generic titles do not repair these fields.
- **Missing official bodies relevant to C/D:** [T04 head/late invariance](../03_reading/V17/BR-R2-T04.md), [LoopLA](../03_reading/V18/BR-A08-V11.md), [finite-query compilation](../03_reading/V18/BR-A08-V20.md), [attention placement](../03_reading/V18/BR-A08-V21.md), [predictive scope](../03_reading/V18/BR-A08-V24.md), and [Farsighted Correction](../03_reading/V18/BR-A08-V16.md) remain body-unread. They could change head/trunk localization, iterative-compute, protected-query exactness, hybrid pathway, binding/scope or longitudinal-incentive comparisons. No proposed remedy, theorem or result is imported from their titles/abstracts. The other blocked V17 bodies—formal tokenization T01, stochastic tokenization T02, and B-Net T06—likewise supply no verified compression, robustness or causal-rate result. These are named source gaps, not evidence that the corresponding ideas are covered by older work or cannot alter the synthesis. [Coverage R3 · §4](../05_review/COVERAGE_RECHECK_R3.md).
- **Venue/edition gaps:** T03/T05 science is cited only at the independently read public editions; their official bodies remain unavailable, and matching title/abstract information does not certify equality or anonymous identity. The official audits establish selected submission metadata, not acceptance or a complete ICLR 2027 results survey. PSR is a foundational completion, not a replacement for missing recent bodies. [ICLR source audit R2 · §1,3–6](../05_review/ICLR2027_SOURCE_AUDIT_R2.md); [coverage R3 · §3–4](../05_review/COVERAGE_RECHECK_R3.md).

The appropriate next decision is which unresolved fork most constrains the actual use case and can be measured validly at lowest cost. Thresholds, budgets, and intervention tolerances must be calibrated to that host, task, stage, seed/window stream, and environment. This chapter specifies comparisons; it neither authorizes experiments nor freezes their numerical acceptance rules.

## Evidence links

These links resolve to the actual carrying cards. Editions and claim locations are stated in the text; old scoped readings retain their original limitations.

[w0092]: ../../flued_multigranularity_survey_20261108/03_reading/B13/W0092.md
[w0050]: ../../flued_multigranularity_survey_20261108/03_reading/B03/W0050.md
[d02]: ../03_reading/V04/BR-A03-D02.md
[memn2n]: ../03_reading/V11/BR-A03-D11.md
[w0229]: ../../flued_multigranularity_survey_20261108/03_reading/B06/W0229.md
[d20]: ../03_reading/V09/BR-A03-D20.md
[thin]: ../03_reading/V04/BR-A03-D19.md
[asym]: ../03_reading/V04/BR-A03-D03.md
[deltaold]: ../03_reading/V02/W0199.md
[gdn]: ../03_reading/V02/W0201.md
[deltanew]: ../03_reading/V11/W0228.md
[geometry]: ../../flued_multigranularity_survey_20261108/03_reading/B06/W0212.md
[prune]: ../03_reading/V09/W0086.md
[qknorm]: ../03_reading/V04/BR-A03-D13.md
[gated]: ../03_reading/V04/BR-A03-D15.md
[gqa]: ../03_reading/V11/BR-A03-D12.md
[lrkv]: ../03_reading/V04/BR-A03-D17.md
[mom]: ../../flued_multigranularity_survey_20261108/03_reading/B16/W0204.md
[triadic]: ../03_reading/V09/BR-A02-N03.md
[cla]: ../03_reading/V04/BR-A03-D04.md
[mhla]: ../03_reading/V11/W0219.md
[slots]: ../03_reading/V11/W0100.md
[hopfield]: ../03_reading/V11/W0240.md
[mdl]: ../03_reading/V12/W0370.md
[amnesic]: ../../flued_multigranularity_survey_20261108/03_reading/B08/W0372.md
[reliability]: ../../flued_multigranularity_survey_20261108/03_reading/B08/W0374.md
[ravel]: ../03_reading/V05/W0531.md
[latent]: ../03_reading/V09/BR-A08-V17.md
[natural]: ../03_reading/V12/W0373.md
[patching]: ../03_reading/V05/W0533.md
[robust]: ../03_reading/V05/BR-A04-N01.md
[mediators]: ../03_reading/V05/BR-A04-R08.md
[ioi]: ../03_reading/V12/BR-A04-N09.md
[hydra]: ../03_reading/V05/BR-A04-R02.md
[errors]: ../03_reading/V09/BR-A08-V19.md
[faith]: ../03_reading/V12/BR-A04-N07.md
[clash]: ../03_reading/V12/BR-A04-N08.md
[eraser]: ../03_reading/V12/BR-A04-R04.md
[goodhart]: ../03_reading/V05/BR-A04-R05.md
[ssa]: ../../flued_multigranularity_survey_20261108/03_reading/B01/W0162.md
[readagent]: ../../flued_multigranularity_survey_20261108/03_reading/B02/W0138.md
[walker]: ../../flued_multigranularity_survey_20261108/03_reading/B02/W0139.md
[selfroute]: ../../flued_multigranularity_survey_20261108/03_reading/B11/W0185.md
[dragin]: ../03_reading/V15/W0450.md
[mnemis]: ../../flued_multigranularity_survey_20261108/03_reading/B21/W0449.md
[raw]: ../../flued_multigranularity_survey_20261108/03_reading/B03/W0124.md
[rerank]: ../../flued_multigranularity_survey_20261108/03_reading/B03/W0156.md
[cmp]: ../03_reading/V09/BR-A08-V18.md
[testing]: ../03_reading/V12/BR-A04-N11.md
[cif]: ../03_reading/V05/BR-A04-N12.md
