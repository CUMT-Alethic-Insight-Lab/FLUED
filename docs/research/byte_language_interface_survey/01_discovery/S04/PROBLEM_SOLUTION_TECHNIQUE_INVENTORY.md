# S04 — Granular problem → solution → technique inventory

**51 records; 28 contributing works (29 screened).** Registry, exact titles/versions, units, training signals, causality, comparators and reading-depth limits: [WORKS](WORKS.md). Search provenance: [SEARCH_LOG](SEARCH_LOG.md). Missing-evidence queue: [READING_HANDOFF](READING_HANDOFF.md).

## How to read and integrate these records

Each record inherits the corresponding WORKS entry's stable version, exact units, learning signal, causal permissions, comparator/budget and reading depth unless a record narrows them. This is a relational schema, not missing data: both files must travel together into the central inventory. Unknown fields in WORKS remain unknown in the record. Every row below also provides a specific source location and local evidence/limit. `E` means a technique explicitly used by the authors; `A` marks our conceptual analogy or algebraic observation, never an author claim. Unmarked techniques are not inferred from model names.

**Evidence tiers:** `BYTE` = direct byte-interface source; `MIXED` = character/byte constituents with word/subword positions or output; `BACKGROUND` = generic word/subword theory/optimization, not byte-model evidence. `A-only` explicitly means an abstract-level candidate. `R-FULL` is reuse of an actual old FULL card, not a new full reading. New targeted readings remain `PARTIAL` even if substantial text was available. No source was reproduced or code-executed.

This is an initial evidence-informed grouping, **not algorithmic clustering**. Cluster labels: T tying axes/regularization; G head geometry/rank/scale; A interface adaptation; O training objectives/gradient control; C latent-use/collapse. Multi-label assignments are allowed. None presuppose source revisiting, a multigranularity design, or a FLUED failure mechanism.

## I. Small alphabets, sharing axes and parameter allocation

### S04-R001 — W0351 — Vocabulary parameters crowd out contextual computation [BYTE; T/A]
- **Prior problem:** In small mT5 sizes, the large subword embedding/softmax allocation dominates total parameters rather than the contextual network.
- **One-sentence solution:** Replace the subword vocabulary with a 256-byte alphabet plus special IDs and reallocate the parameter budget to network capacity.
- **Techniques:** E: learned byte lookup, pretrained encoder–decoder Transformer, span-corruption denoising; these supply representations and self-supervision, not a learned tokenizer.
- **Signal/behavior/units:** Byte corruption→missing-byte targets; full corrupted source is bidirectional, target generation causal.
- **Evidence/budget:** R-FULL W0351, TACL Table1/§3.1: ByT5 vocabulary-related share0.3% at Small vs mT5 85%; totals matched approximately by design, not FLOPs/text. This is parameter allocation evidence, **not a tying-on/off regularization experiment**.

### S04-R002 — W0351 — Longer byte strings change where encoder–decoder capacity is useful [BYTE; A]
- **Prior problem:** Retaining a symmetric subword encoder/decoder layout spends relatively much computation in a serial decoder after replacing tokens with bytes.
- **One-sentence solution:** Use an encoder-heavy 3:1 layer split while preserving the byte-to-byte training interface.
- **Techniques:** E: asymmetric depth allocation within the Transformer; cross-attention transfers source states to the causal decoder. No parameter inversion or block tying is established.
- **Evidence/budget:** R-FULL, §3/Table1 and §6/Table8: sizes use12/4,18/6 or36/12; a668M36/12 variant beats a718M24/24 variant in three reported tasks. Width/size also vary, so depth ratio is not isolated. Encoder-only savings cannot establish answer-generation latency.

### S04-R003 — W0351 — A generic “shared embedding” label conflates two different interfaces [BYTE; T]
- **Prior problem:** Encoder/decoder input-table sharing and decoder input/output sharing can be misreported as one architecture-wide switch.
- **One-sentence solution:** Specify separately the shared encoder/decoder input table and the decoder's independent output softmax table.
- **Techniques:** E (specific released configuration): `Bitransformer.shared_embedding=True`; `decoder/Unitransformer.shared_embedding_and_softmax_weights=False`. These are distinct parameter-sharing choices, not new optimization algorithms.
- **Evidence/budget:** R-FULL W0351 static check of **Large operative gin only**, matched to a fixed Mesh definition, not runtime execution. The gin is XNLI fine-tuning initialized from1M-step checkpoint. Fresh gin extraction and HF Small/Large requests failed here. Other sizes, ports, exact training dependency commit and actual tensor aliasing remain unverified.

### S04-R004 — W0351 — Equal parameter/position budgets do not equal equal text or inference work [BYTE; T/A]
- **Prior problem:** A tiny output alphabet can look computationally cheap while the model sees less original text and emits more serial units.
- **One-sentence solution:** Compare parameter allocation, original-text exposure and task-specific encode/decode time separately.
- **Techniques:** E: parameter-matched model family, task benchmark and throughput accounting; not an assistant-proposed model mechanism.
- **Evidence/budget:** R-FULL, §3.2/Table9–10:1M steps and1024 input positions, average4.1 UTF-8 bytes/subword; training throughput roughly0.75× mT5 on TPUv3-64. Long-output and classification time ratios differ substantially. Fixed-commit README confirms target189 for pretraining example, **not1024 target bytes**. No inference that untied byte heads cause these costs.

### S04-R005 — W0364 — Duplicate word tables add parameters and overfit [BACKGROUND; T]
- **Prior problem:** A word LM learns separate input and output vectors for the same vocabulary despite their related roles.
- **One-sentence solution:** Tie the input embedding and output classifier matrix in the recurrent LM.
- **Techniques:** E: hard parameter equality, LSTM and next-word CE; shared updates provide coupling rather than additional labels.
- **Evidence/budget:** PARTIAL v3 §3/§4.2, PTB/text8/IMDB/BBC; text says validation/test perplexity improves without comparable training improvement, consistent with reduced overfitting. Dropout and no-dropout models are separate settings. Exact table-body numbers not recovered. This is **word-vocabulary evidence**, not a demonstration that removing a256-row table regularizes equally.

### S04-R006 — W0364 — Shared vectors must serve different input/output transformations [BACKGROUND; T/G]
- **Prior problem:** Direct tying may leave insufficient flexibility between the recurrent hidden state and a common embedding space, particularly without dropout.
- **One-sentence solution:** Insert an output-side projection and regularize that projection while retaining the tied table.
- **Techniques:** E: square hidden-space linear adapter `P`, output scores `V P h`, projection penalty (paper writes λ||P||₂), λ=.15 in reported experiments.
- **Evidence/budget:** PARTIAL §3/§4.2: projection regularization helps the small no-dropout configuration but not the large dropout configuration; joint PR+WT improves the small model. Projection, sharing and dropout must not be collapsed into one “tying benefit.” Full tables, penalty implementation and optimizer interactions need reading/code check; no byte test reported here.

### S04-R007 — W0364 — Cross-language input tables remain redundant even after decoder tying [BACKGROUND; T/A]
- **Prior problem:** A bilingual encoder–decoder can still store three large tables despite extensive source/target subword overlap.
- **One-sentence solution:** Build a joint vocabulary and share encoder input, decoder input and decoder output tables three ways.
- **Techniques:** E: BPE union vocabulary, three-way tying, attention-conditioned recurrent translation.
- **Evidence/budget:** PARTIAL §3/§4.3: EN–FR/EN–DE,89,500 BPE merge operations,300K Adadelta updates,500-d embeddings,1000 hidden; reported about52% parameter reduction with similar BLEU, versus28% for decoder-only tying. **Subword units, not bytes.** Sharing source/target tables is not sharing entire encoder/decoder blocks; bilingual union conditions and table details need full reading.

### S04-R008 — W0365 — One-hot supervision ignores similarity among target words [BACKGROUND; O/G]
- **Prior problem:** A next-word one-hot target communicates no relationship among plausible vocabulary alternatives.
- **One-sentence solution:** Add a temperature-smoothed KL objective whose target distribution is derived from similarity to the ground-truth word embedding.
- **Techniques:** E: embedding inner products, softmax temperature, self-contained knowledge transfer and auxiliary KL; no external teacher is necessary.
- **Evidence/budget:** PARTIAL v3 §3 Eqs3.1–3.7/§6.3, PTB and WikiText2 four-model factorial. AL can help smaller models more than RE, and relative utility changes with dataset size. The target is learned iteratively and may be uninformative initially. Byte identity has no established word-semantic metric; transferring this target construction to bytes is an **A analogy**, not tested evidence.

### S04-R009 — W0365 — Separate output spaces can duplicate embedding subspace learning [BACKGROUND; T/G]
- **Prior problem:** Under the paper's augmented loss, optimizing an independent classifier may relearn the input embedding's column space.
- **One-sentence solution:** Reuse the input matrix transpose as the output projection, allowing the recurrent network to absorb a hidden-space linear map.
- **Techniques:** E: high-temperature KL/logit matching, matrix-span analysis, reused embeddings (RE).
- **Evidence/budget:** PARTIAL §4 Eqs4.1–4.5: equal hidden/embedding dimension,zero bias,augmented-loss-only,zero training loss,full-rank/span conditions and high-temperature approximation. The argument reaches shared subspace up to a transform before motivating exact equality. **Not a theorem of universal tying optimality**, and not a fully normalized cosine-head theorem; independent proof audit remains undone.

### S04-R010 — W0365 — Auxiliary-target benefit and tying benefit are empirically confounded [BACKGROUND; T/O]
- **Prior problem:** A compound loss/framework can obscure whether improvement comes from supervision or parameter reuse.
- **One-sentence solution:** Train baseline, augmented-loss-only, reuse-only and their combination at each network size.
- **Techniques:** E: AL/RE/REAL factorial comparison, variational dropout and recurrent optimization; temperature/gradient-magnitude scaling controls the auxiliary signal.
- **Evidence/budget:** PARTIAL §6.1–6.3,200/650/1500 hidden; word PTB10K and WikiText233,278 vocabularies. Larger models gain mostly from RE, smaller/data-limited settings gain more from AL. Table3 includes51M REAL vs66M large baseline; not equal-parameter proof. These results motivate separating factors, not assuming256-class results.

## II. Shared-path gradients, output geometry and rank

### S04-R011 — W0366 — A tied matrix need not compromise equally between its two roles [BACKGROUND; T/O]
- **Prior problem:** Describing tying as balanced alignment hides potentially asymmetric input/output optimization.
- **One-sentence solution:** Analyze aligned representations and separately accumulated input-path/output-path gradients of the shared table.
- **Techniques:** E: identity/orthogonal/linear alignment, path-gradient norm decomposition, learned affine prediction probes.
- **Evidence/budget:** R-FULL v1 §§3–5: OLMo tied→untied output linear alignment.719 vs input.525; early1000 steps output gradient norm about70% of the sum of two norms. This is **not70% of Adam's actual update**. Different Dolma versions and other model-size/data differences weaken simple causal claims. Press/Wolf already analyzed output-like updates; not a newly discovered historical phenomenon or a byte result.

### S04-R012 — W0366 — Correcting gradient imbalance may hurt downstream behavior [BACKGROUND; T/O]
- **Prior problem:** If output-path dominance is observed, simply amplifying input gradients is tempting but may not improve the task.
- **One-sentence solution:** Multiply the input-path gradient and measure both geometry and downstream consequences rather than equating alignment with quality.
- **Techniques:** E: input-gradient×5 intervention during10K-step training, representation alignment and task evaluation.
- **Evidence/budget:** R-FULL §6/AppendixE Table7: alignment moves slightly toward input, but WikiText2 perplexity35.71→36.64 and BoolQ.576→.548 while PIQA.620→.631. Single-run conditions, not a statistically resolved universal intervention. No orthogonal byte-vocab/linear-vs-cosine experiment; the intervention is not merely untying.

### S04-R013 — W0367 — Parameter tying does not ensure pseudo-inverse consistency [BACKGROUND; T/G]
- **Prior problem:** A shared table and its transpose do not generally compose to a hidden-space identity map.
- **One-sentence solution:** Factor embedding/unembedding through shared orthonormal-column memory with coupled inverse transforms.
- **Techniques:** E: `E=Z T^-1`, `Wout=T Z^T`, polar initialization,SPD/Cholesky transform and triangular solves; optional Stiefel retraction.
- **Evidence/budget:** PARTIAL v2 §4 Eqs4–13; reported256M–1.3B continued-training benefits but from-scratch trade-offs; all tables/appendix unread. **A dimensional feasibility check:** `Z∈R^(V×d), Z^T Z=I_d` requiresV≥d; a256-byte vocabulary withd>256 cannot satisfy this exact construction. Hidden-space consistency is not a guarantee of semantic identity or next-byte accuracy.

### S04-R014 — W0368 — Sparse lookup and dense classifier gradients need not fit one optimizer geometry [BACKGROUND; T/O; A-only]
- **Prior problem:** A tied vocabulary table receives sparse input and dense output contributions, unlike ordinary dense hidden matrices optimized by Muon.
- **One-sentence solution:** Use a support-aware finite-cap update for the tied table while retaining Muon's matrix update elsewhere and RMS-normalized1D updates.
- **Techniques:** E as explicitly described in v1 abstract: linear-minimization oracle,first-moment buffer,parameter-class-specific geometry; no second-moment state.
- **Evidence/budget:** ABSTRACT only, nine settings124M–1B/text/image/protein,claim~20% optimizer-state memory saving and~1% step overhead vs Hybrid Muon. No byte-text setting established. Full methods, supports/aliasing handling, matched budgets and uncertainty must be read before treating claims as corroborated results.

### S04-R015 — S04-N01 — Unconstrained tied-row norms influence output ranking [BACKGROUND; G/T]
- **Prior problem:** A dot-product tied classifier entangles direction and embedding magnitude, potentially privileging large-norm rows.
- **One-sentence solution:** Normalize the shared embedding columns/rows to unit length on both input and output uses.
- **Techniques:** E: L2-normalized shared embedding,Transformer/DynamicConv,CE with label smoothing; normalization imposes equal token-vector norm.
- **Evidence/budget:** PARTIAL v2 §2.2.1/§3.2,WMT16 En-De32K subwords; text reports up to+.6 BLEU Transformer-big and+.5 DynamicConv. Table bodies absent. The paper's unbiasedness reasoning assumes uniformly iid unit-sphere vectors/sparse-mixture representation; learned embeddings need not satisfy it. Hidden vectors are not necessarily unit norm, so this is not automatically a fully cosine-normalized head.

### S04-R016 — S04-N01 — Removing input-norm freedom can reduce representational flexibility [BACKGROUND; G]
- **Prior problem:** Normalizing the input and output table equally discards norm information that might help smaller embedding spaces.
- **One-sentence solution:** Preserve input vectors and normalize only the output classifier by squared row norm.
- **Techniques:** E: output weights `w_i/||w_i||²`; asymmetric input/output coupling without an independently learned vocabulary table.
- **Evidence/budget:** PARTIAL §§2.2.2/3.2,IWSLT14; text reports square normalization best in one Transformer setting but warns about overestimating very small-norm vectors. Direction labels in result prose are internally inconsistent with dataset setup; do not quote a language-direction table without PDF check. Not ordinary hard tying, not cosine, and no byte alphabet experiment.

### S04-R017 — S04-N01 — “Cosine head” can hide a retained confidence scale [BACKGROUND; G]
- **Prior problem:** Comparing head variants only by name may conflate row normalization, distance scoring and full cosine normalization.
- **One-sentence solution:** Score with normalized output rows while retaining hidden-vector magnitude as the example-dependent scale.
- **Techniques:** E: §2.2.4 Eq28 computes`w_i^T h/||w_i|| = cos(w_i,h)||h||`; E: separate distance-scoring alternative includes a row-norm-derived offset.
- **Evidence/budget:** PARTIAL,DynamicConv IWSLT text says the “cosine” variant+.41 BLEU. **A distinction:** no division by`||h||` in this equation, so it is not equal to a fixed-temperature cosine head even when argmax rankings agree under common rescaling. Full table/implementation check missing; no claim that this normalization wins on bytes.

### S04-R018 — S04-N02 — Unit-normalized output logits cannot freely control confidence [BACKGROUND; G]
- **Prior problem:** When output vectors and hidden states are unit norm, raw cosine logits lie in[-1,1], restricting softmax confidence.
- **One-sentence solution:** Learn vocabulary-indexed scale factors for the normalized output logits.
- **Techniques:** E: normalized input/output embeddings,unit hidden states,per-class vector`s_z` scaling before CE.
- **Evidence/budget:** PARTIAL nGPT v1 §2.1 Eqs1–3,0.5B/1B OpenWebText models. Tying is a separate choice; the text explicitly allows distinct input/output vectors. Other normalization changes co-occur, so no isolated cosine-head quality or byte-specific result. **A algebraic caution:** normalization without a scale and scaled normalized heads should never share one category.

### S04-R019 — S04-N02 — Parameter norms and optimizer step scales create convergence sensitivities [BACKGROUND; G/O]
- **Prior problem:** A global learning rate has different relative effects on parameters with different magnitudes, complicating normalized-network learning.
- **One-sentence solution:** Normalize parameter vectors and explicitly parameterize learnable block/logit scales with controlled effective update sizes.
- **Techniques:** E: hypersphere retraction,normalized residual interpolation,scale initialization/reparameterization,no weight decay/warmup in the proposed recipe.
- **Evidence/budget:** PARTIAL §§2.5–2.6/3.1: v1 reports4–20× fewer steps/tokens to comparable loss, but step cost60–80% higher at4K/8K context. Architecture/optimizer/scale changes all vary. These are not head-only or tying-only gains and not byte-training cost ratios.

### S04-R020 — S04-N03 — A single linear softmax can restrict conditional-distribution rank [BACKGROUND; G]
- **Prior problem:** Low-dimensional word classifiers can constrain the matrix of context-dependent log probabilities.
- **One-sentence solution:** Mix several softmax distributions instead of averaging hidden contexts before one softmax.
- **Techniques:** E per inspected introduction: discrete latent mixture components/mixture of softmaxes,word LM likelihood and matrix-factorization analysis.
- **Evidence/budget:** PARTIAL abstract/introduction,v3; PTB/WikiText2/1BWord positive results reported but theorem/ablations unread. **A scope check:** a256-way output with hidden width≥256 need not have the same basic low-rank obstruction as a10K–100K word vocabulary. This does not rule out other geometry/optimization limits, and does not show that tying creates all bottlenecks.

### S04-R021 — S04-N04 — Morphologically related words duplicate input parameters [MIXED; A/T; A-only]
- **Prior problem:** Word-level lookup tables cannot directly share spelling/morphology among related forms and cost many parameters.
- **One-sentence solution:** Compose each word's input vector from its characters before feeding a recurrent word-level LM.
- **Techniques:** E from abstract: character CNN,highway network,LSTM; shared composition reuses character features across words.
- **Evidence/budget:** ABSTRACT/history only,latest listed v4; PTB comparable quality with60% fewer parameters and reported multilingual morphology gains. **Output remains a word classifier**, so large output-vocabulary costs have not disappeared. Exact character inventories, output tying, segmentation preprocessing and fair parameter controls require full reading; no byte-to-byte conclusion.

## III. Auxiliary supervision and interface optimization in direct byte models

### S04-R022 — S04-N05 — Deep byte Transformers are difficult to optimize [BYTE/ASCII-CHARACTER; O]
- **Prior problem:** Naive models deeper than about10 Transformer layers showed slow convergence/poor quality in this setting.
- **One-sentence solution:** Add next-unit prediction losses at intermediate layers, then remove them progressively during training.
- **Techniques:** E: deep supervision with separate classifier heads and scheduled loss decay; not distillation from an external teacher.
- **Evidence/budget:** PARTIAL v2 “Intermediate Layer Losses”/“Training”/“Ablation Experiments”:64layers,~235M parameters,512context; intermediate losses end by half of4M planned steps,one layer every62.5K. Text8=27-character ASCII subset,enwik8=bytes,heads256classes for both. Ablations reuse tuned hyperparameters; table bodies incomplete. Training-only heads must be included in training parameter/cost counts, not inference counts.

### S04-R023 — S04-N05 — One final-position target wastes supervision per sampled context [BYTE/ASCII-CHARACTER; O]
- **Prior problem:** A stateless fixed-window predictor trained only on its final position extracts one labeled event per context.
- **One-sentence solution:** Train predictions at all positions under a causal mask, including short-context positions.
- **Techniques:** E: dense autoregressive teacher-forced supervision over the sequence; all-position losses retain equal weight,unlike decayed intermediate layers.
- **Evidence/budget:** PARTIAL “Multiple Positions”/Ablations; largest reported ablation gains include this target densification. Random512-position windows,no state passed across batches; training examples per batch increase but original text quantity does not. Evaluation uses final position and recomputes context; results are not KV-cached modern serving throughput. Separate this from gradient regularization or output-table tying.

### S04-R024 — S04-N05 — Next-unit-only supervision may not encourage useful future information [BYTE/ASCII-CHARACTER; O]
- **Prior problem:** A next-byte/character objective alone can leave future predictive structure weakly supervised.
- **One-sentence solution:** Attach extra classifiers for farther future targets during training, discarding them for inference.
- **Techniques:** E: multi-target prediction,independent target classifiers,extra-target loss weight.5; causal input masking retained.
- **Evidence/budget:** PARTIAL “Multiple Targets”/Training/Ablations; two targets per position in described64-layer setup. This trains predictive representations but does not define a joint future-byte distribution or an exact parallel sampler. Text8/enwik8 unit distinction persists. No observed tying state; no fabricated claim that future heads share an embedding or decoder backbone differently.

### S04-R025 — W0010 — Low-level byte processing and high-level patch computation need a learned interface [BYTE; A/G]
- **Prior problem:** Reducing global sequence length can lose spelling-level information and leave local/global representations poorly connected.
- **One-sentence solution:** Use local byte encoders/decoders and learned cross-attention to bridge patch and byte states, alongside byte n-gram features.
- **Techniques:** E: local causal attention,hash n-gram lookup,patch-query cross-attention pooling,global Transformer,decoder cross-attention and local byte states.
- **Evidence/budget:** R-FULL ACL2025 §3/§7/Table4–5; interface and n-gram ablations are important,so gains cannot be attributed only to entropy boundaries. Equal-FLOP8B runs differ in byte exposure/patch rates. A local bypass is not evidence of posterior collapse; tying/normalization of alphabet heads remains unknown.

### S04-R026 — W0010 — Joint segmentation and language objectives can compete [BYTE; O]
- **Prior problem:** Training an entropy-based patch selector together with the main LM might introduce competing objectives.
- **One-sentence solution:** Train the entropy LM independently and keep it separate from the main byte latent model.
- **Techniques:** E: external causal entropy estimator,threshold-based segmentation,non-joint training. This is supervision separation,not stopped gradients inside one shared table.
- **Evidence/budget:** R-FULL §4/§10 and AppendixO; default estimator100M/14layers/512window. Authors explicitly motivate separation to avoid auxiliary competition, but this is **not a measured gradient-conflict trajectory or an equal-budget joint-vs-separate causal ablation**. Estimator pretraining and per-byte inference require accounting beyond the principal main-model formula.

### S04-R027 — W0011 — Hard selection makes rate learning unstable or gradient-poor [BYTE; O]
- **Prior problem:** Selecting discrete byte positions into a hierarchy provides no ordinary derivative through the selection decision.
- **One-sentence solution:** Combine probabilistic smoothing and a straight-through surrogate so the LM objective trains boundary confidence.
- **Techniques:** E: scaled cosine **router**,hard selected states,EMA dechunking,straight-through estimator; local residual carries fine states.
- **Evidence/budget:** R-FULL v2 §2/§3.3 Fig7,AppendixE; removing smoothing causes compression-rate fluctuations/performance loss. Selection is not genuinely differentiable and not mean pooling. **Cosine routing is not a cosine vocabulary head**; no tying status follows. Current implementation can be slower than isotropic baselines and lacks multiseed stability certification.

### S04-R028 — W0011 — Task loss alone can leave an undesirable processing rate [BYTE; O]
- **Prior problem:** A trainable router can choose too many or too few selected states for the desired compression/computation trade.
- **One-sentence solution:** Add a ratio loss linking empirical selected fraction and average boundary confidence to a target rate.
- **Techniques:** E: load/rate-balancing auxiliary loss,actual hard fractionF,mean probabilityG,target1/N,α=.03; main CE still learns prediction.
- **Evidence/budget:** R-FULL §2 Eq10/§3,byte exposure approximately matched and per-byte FLOPs adjusted via backbone depth. The loss is not a strict per-example quota; F≠G can yield values below the nominal balanced point. No claim that every auxiliary loss helps or that ratio regularization ensures semantic boundaries/latent use.

### S04-R029 — W0511 — Adapting a pretrained byte encoder must trade task signal against deletion [BYTE; A/O]
- **Prior problem:** A pretrained ByT5 interface remains expensive because every source byte traverses the full encoder.
- **One-sentence solution:** Continue pretraining with a learned deletion gate and a controlled deletion regularizer after early encoder layers.
- **Techniques:** E: soft attention masking in training,hard state deletion at inference,proportional–integral rate controller and denoising CE.
- **Evidence/budget:** R-FULL MrT5 v3 §3/§5/AppendixE:ByT5-Small,gate afterlayer3,5Ksteps×2^20positions,15languages; near50% deletion beats random/fixed deletion/pooling at matched approximate shortening but not no-deletion quality. Source is bidirectional/query-aware; output stays causal bytes. Inference saving depends on output length and historical pretraining cost.

### S04-R030 — W0511 — Ordinary softmax can erase the gate's absolute deletion signal [BYTE; G/O]
- **Prior problem:** Adding nearly uniform gate-related offsets can be canceled by softmax shift invariance, encouraging pathological all-delete behavior or inflated attention scores.
- **One-sentence solution:** Use softmax1 plus attention-score regularization so absolute attention mass matters during gate learning.
- **Techniques:** E: softmax1 denominator augmentation,gate-dependent masks,extra attention-score constraint (AppendixD).
- **Evidence/budget:** R-FULL §3 Eqs1–7/AppendixD; these are explicit optimization components,not merely faster packing. Their role is stabilizing deletion supervision,not norm control for vocabulary logits. All encoder states being soft-masked during training differs from a hard,information-free bottleneck; no automatic posterior-collapse identification.

### S04-R031 — W0514 — Byte embeddings need local composition before semantic translation [BYTE with external word spans in WSF; A]
- **Prior problem:** Dense byte translation lacks explicit local lexical composition and performs poorly in some source languages.
- **One-sentence solution:** Fuse short byte patterns with convolution or restrict local attention to supplied word spans before higher encoder layers.
- **Techniques:** E:1–4byte convolutions with repetition/weighted combination,nCF; WSF block attention using Moses word spans. Both retain full byte-length states.
- **Evidence/budget:** R-FULL v3 §3/§4/AppendixB; one-hot-byte44.1M vsBPE68.7M,5Ksteps faster training but slower validation inference on3090; Lao BLEU5.9dense/6.4nCF/6.5WSF vs9.2BPE. Not universal improvement,not persistent compression,not a tying-only effect; source preprocessing/800byte filtering count.

### S04-R032 — W0356 — Direct-byte learning can spend early training on very local dependencies [BYTE; O/A]
- **Prior problem:** Learning long-range language structure directly at every byte position can be optimization-inefficient.
- **One-sentence solution:** Begin with fixed four-byte averaged inputs and unordered four-byte-bag targets, then switch to ordinary next-byte prediction.
- **Techniques:** E: staged objective/granularity curriculum,byte n-gram hash features and wider local convolution.
- **Evidence/budget:** R-FULL v1 §2.1/AppendixA,first30% vsremaining70%steps. Same-parameter byte frontier wins do not imply same-FLOP wins: reported compute-optimal subword frontier remains better. Target/order changes plus convolution/hash differences prevent a pure curriculum or regularization attribution. This is neither learned segmentation nor evidence of a cosine/tied output choice.

### S04-R033 — W0023 — Auxiliary reconstruction can distort the main LM if allowed to update everything [BYTE and SUBWORD, separate tasks; O/A]
- **Prior problem:** A compressor needs learning signal after old states leave the ordinary gradient horizon, while full-state reconstruction need not preserve what attention consumes.
- **One-sentence solution:** Train the compressor with stopped-gradient attention-response reconstruction instead of propagating auxiliary gradients into the main network.
- **Techniques:** E: stop-gradient,learned convolutional compressor,attention reconstruction vs autoencoding; separate BPTT comparison extends gradient horizon.
- **Evidence/budget:** R-FULL v1 §3.2/Algorithms1–2,Table5:enwik8.973attention-conv vs.984autoencoding-conv; compression ratio selected per row and BPTT doubles unroll/halves batch. PG-19 subword results separate. Distinct budget/target changes mean no universal stop-gradient superiority or byte-interface causal diagnosis.

### S04-R034 — W0328 — Shared-task optimization can suffer conflict plus magnitude/curvature imbalance [BACKGROUND; O]
- **Prior problem:** Summed task gradients can interfere,especially with negative inner products,unequal norms and high positive curvature.
- **One-sentence solution:** Project a conflicting task gradient off the other task's direction before aggregating shared-parameter updates.
- **Techniques:** E: PCGrad pairwise projections,random task order,separate task backward passes.
- **Evidence/budget:** R-FULL v4 §2/Algorithm1:restricted convex/smooth or single-step guarantees,not all-task finite-budget improvement. Card reports supervised experiment ranges up to12h/10GB vs8h/6GB; not a universal ratio. **Not used in any byte system established here**; suggested byte-interface applicability would be A analogy. Negative cosine alone is not a complete diagnosis,and preserve the old AppendixA.3 audit concern.

### S04-R035 — W0331 — An auxiliary objective can reduce main loss locally yet waste training budget [BACKGROUND; O]
- **Prior problem:** Fixed auxiliary weights may cause negative transfer,but local gradient agreement is also an imperfect proxy for long-term benefit.
- **One-sentence solution:** Gate auxiliary shared updates by nonnegative gradient similarity while evaluating downstream main-task performance separately.
- **Techniques:** E:cosine gate `g+max(0,cos(g,v))v`,binary practical variants,private auxiliary heads continue training.
- **Evidence/budget:** R-FULL v2 §2–4/AppendixB/F:positive descent direction can slow convergence; perfect-teacher gating can trail direct addition; rotatedMNIST gate still trails main-only. Extra per-task gradients/teacher costs not fully closed. No theorem that positive cosine rules out historical competition or guarantees useful byte representations; not a byte implementation result.

## IV. Latent-use and posterior-collapse antecedents (explicitly not byte evidence)

### S04-R036 — S04-N06 — A strong autoregressive decoder can ignore a stochastic global latent [BACKGROUND; C/O]
- **Prior problem:** A sentence VAE can reach near-zero posterior/prior KL and behave like an ordinary LM without using its latent sentence representation.
- **One-sentence solution:** Ramp the KL penalty from zero to one so representation formation is initially less costly.
- **Techniques:** E:VAE reparameterization,LSTM decoder,KL cost annealing; temporarily changes the training objective rather than proving latent semantics.
- **Evidence/budget:** PARTIAL v4 §3.1/§4,word-levelPTB; without annealing/word dropout ordinary-LM-like behavior and zeroKL recur. With interventions standard VAE remains slightly worse than LM under reported likelihood accounting. VAE variational bound vs exact-LM likelihood differ. **Not the definition of deterministic byte-state failure**,nor a universal claim that all early decoder bypasses are irreversible.

### S04-R037 — S04-N06 — Latent-use improvement can trade off with language-model quality [BACKGROUND; C/O]
- **Prior problem:** Merely increasing posteriorKL can be mistaken for improved representation or generation quality.
- **One-sentence solution:** Weaken teacher-forced decoder history using word dropout and examine both latent dependence and likelihood.
- **Techniques:** E:replace previous-word inputs withUNK,including a historyless limit; distinct from ordinary embedding dropout,which the source reports did not help latent use.
- **Evidence/budget:** PARTIAL §3.1/§4:word dropout forces more latent reliance but the baseline comparison changes as decoder history disappears; ordinary full-history LM can remain stronger. No byte/character setting established. More latent information is not by itself a task-performance guarantee; later generation experiments/keep-rate sweeps need full reading before precise broader claims.

### S04-R038 — S04-N07 — Decoder contextual capacity controls how much a VAE needs its latent [BACKGROUND; C/A]
- **Prior problem:** A full-history LSTM may overpower latent conditioning,whereas a bag-of-words decoder underfits sequence structure.
- **One-sentence solution:** Sweep a causal dilated CNN's receptive field to balance local history modeling and latent conditioning.
- **Techniques:** E:dilated causal residual CNN,LSTM recognition,Gaussian latent concatenated at each decoder position,ELBO and KL annealing.
- **Evidence/budget:** PARTIAL v2 §§2.2–2.3/3.2–3.3,20K **word** vocabulary,Yahoo/Yelp100Ktrain,40epochs,fields15/63/125/187. Yahoo latentKL13.3small→.7verylarge; intermediateVAE+encoderinitPPL63.9vsLM66.2. Capacity/parameters and encoder initialization co-vary; classification and LM optima differ. This is language-background evidence,not byte posterior-collapse confirmation.

### S04-R039 — S04-N08 — Inference-network lag can cause collapse without a new capacity bottleneck [BACKGROUND; C/O; A-only fresh]
- **Prior problem:** Early approximate inference may fail to track the changing true posterior,encouraging the generator to ignore latent information.
- **One-sentence solution:** Aggressively update the inference network before each generator update according to a mutual-information criterion.
- **Techniques:** E per abstract and reused recovery passages:two-timescale alternating optimization,MI monitoring,extra inference steps; no new latent architecture.
- **Evidence/budget:** Fresh abs/history v2 plus old LD-N01/globalN2 targeted recovery,not a new full read. Prior recovery reports2–3×ordinaryVAE training time; equal-total-update/time details and full appendices missing. Applies to stochastic VAE posteriors,not automatically deterministic byte compressors. Extra optimization is not a free regularizer.

## V. Adaptation of pretrained token models: direct recent byte evidence and counterexamples

### S04-R040 — S04-N09 — Matching raw embedding distance may not ensure downstream compatibility [BYTE↔SUBWORD; A/G]
- **Prior problem:** A new local byte encoder can approximate source token embeddings yet propagate differently through a frozen pretrained backbone.
- **One-sentence solution:** Match representations after a small prefix of the frozen backbone rather than matching only static embeddings.
- **Techniques:** E:representation distillation through frozen layers,model-stitching-inspired objective,L2 distance,teacher subword boundaries for aligned pooling.
- **Evidence/budget:** PARTIAL Bolmo v2 §3.2.1:n=4reported better trade than n=0; source global model frozen but gradients pass through firstn layers. Stage1~43Bbytes,1B/7Bmodels; full table/ablation extraction pending. **Frozen parameters do not imply zero backward cost**. This mechanism requires temporary token boundary supervision,despite final byte interface.

### S04-R041 — S04-N09 — A low-width local adapter can impose a rank ceiling on transferred features [BYTE↔SUBWORD; A/G]
- **Prior problem:** Mapping narrow local states to wide global inputs by a linear upprojection/padding restricts possible representation rank.
- **One-sentence solution:** Give the local representation interface sufficient dimensional capacity to emulate the source embedding geometry.
- **Techniques:** E:source-embedding singular-value analysis and local model dimension choice; no low-rank assumption forced on all vocabulary entries.
- **Evidence/budget:** PARTIAL §3.1 footnote/AppendixE paragraph:high-rank structure in most examined input/output tables,exception Qwen3-4B-Base input. **A algebraic observation:** rank bound belongs to the linear adapter,not the number256 of primitive byte types once contextual composition is allowed. Exact dimensions,source matrices and local-width ablation still need full reading; no universal minimum-width recommendation.

### S04-R042 — S04-N09 — Random local modules can disrupt a pretrained global network [BYTE↔SUBWORD; A/O]
- **Prior problem:** Jointly training a pretrained backbone with random encoder/decoder/head interfaces can cause destructive early updates and slow iteration.
- **One-sentence solution:** First train local modules against a frozen global model,then train the full byte model end-to-end.
- **Techniques:** E:boundaryBCE,representation matching,temperature-modulated patch-likelihood distillation,byteCE and staged unfreezing; Stage1loss weights4/1/1/1.
- **Evidence/budget:** PARTIAL §3.2/§6.2:stage2-only gets+6.5Btokens (~17%) for approximate FLOP matching of9.8Bstage1tokens. Stage1 helps,especially1B,but **not strictly necessary and omission is not catastrophic**. Memory mismatch ignored and schedule matters. This is a direct counterexample to promoting all alignment curricula into universal prerequisites.

### S04-R043 — S04-N09 — Reusing post-training weights can fail when interface spaces drift [BYTE↔SUBWORD; A/G]
- **Prior problem:** A byteified backbone retains parameter correspondence with its token ancestor,but its local interfaces may be incompatible with that ancestor's post-trained layers.
- **One-sentence solution:** Transfer the ancestor's backbone weight delta by task arithmetic only when resetting its embeddings to the base space preserves behavior.
- **Techniques:** E:backbone task-vector addition,embedding-reset compatibility check; local byte modules remain in base spaces.
- **Evidence/budget:** PARTIAL §5.2:IFEval31.1baseBolmo→67.4merged vs66.9sourcepost-trained; source base35.4. Existing RL checkpoint cost is not zero—**additional byte post-training** is zero. Source explicitly says compatibility not always holds; AppendixD not fully read. Geometry consistency is an empirical transfer condition,not source-query access or guaranteed tied-table benefit.

### S04-R044 — S04-N10 — Joint boundary/semantic losses can destabilize token-to-byte conversion [BYTE↔SUBWORD; A/O]
- **Prior problem:** A byte encoder,semantic backbone and tokenizer-emulating router need mismatched representations,sequence lengths and objectives aligned simultaneously.
- **One-sentence solution:** Train encoder embedding alignment,then token-distribution distillation,then router boundaries with the backbone frozen.
- **Techniques:** E:boundary-state L2 against teacher embeddings,teacher-forced tokenKL,tokenizer-label boundaryBCE,sequential freezing curriculum.
- **Evidence/budget:** PARTIAL v1 §4.2.1 Eq2–4,30Bbytesstage1; final stage1 output remains **subword tokens**,not bytes. §6.1 describes severe no-alignment degradation in this recipe. Author states joint-loss competition but no measured gradient-cosine trajectory was inspected. Bolmo's more nuanced stage2-only result R042 must remain a counterexample,not averaged into a universal claim.

### S04-R045 — S04-N10 — A token-output intermediate is not yet a deployable byte-to-byte model [BYTE↔SUBWORD; A/O]
- **Prior problem:** Successful byte-input distillation can still rely on the teacher's token classifier for generation.
- **One-sentence solution:** Replace the token head with dechunking/byte-decoder modules,adapt those alone,then unfreeze the full model for next-byte training.
- **Techniques:** E:head-only adaptation,staged unfreezing,causally shifted upsampling,next-byteCE; later stage consumes95Bbytes,total125B.
- **Evidence/budget:** PARTIAL §4.2.2/§5 setup; author reports broader model-family retention,full metric tables not independently read. Tokenizer/teacher development costs are historical prerequisites. Stage1quality must not be quoted as final-byte performance,and95B extra bytes cannot be ignored when comparing to another conversion method's first stage.

### S04-R046 — S04-N10 — A lookahead router needs future-like information unavailable during generation [BYTE; A/O]
- **Prior problem:** Byte-boundary prediction uses current/next hidden-state similarity during prefill,but actual future bytes cannot condition an autoregressive generator.
- **One-sentence solution:** Predict the byte/boundary jointly or train a next-next-byte auxiliary head to provide a proxy future embedding.
- **Techniques:** E:512class joint-byte/boundary prediction (JBP),alternativeMBP auxiliary head,next-next-byte supervision,shifted dechunking; **router cosine is not output cosine**.
- **Evidence/budget:** PARTIAL §4.1.1–4.1.3/§6.2 descriptions; JBP reportedly stronger on harder reasoning despite mixed common-sense differences. Exact causal indexing and exposure bias require full diagram/appendix audit. These are different prediction distributions/heads,not synonymous “multi-byte” rows,and do not establish an exact joint sampler for independent future predictions.

### S04-R047 — S04-N11 — Token-level distillation has no common classifier coordinates across tokenizers [MIXED; A/O]
- **Prior problem:** Teacher/student vocabulary logits cannot be KL-matched directly when token boundaries and alphabets differ.
- **One-sentence solution:** Attach an auxiliary byte interface to the student and match teacher probabilities converted into that common alphabet.
- **Techniques:** E:approximate teacher token→byte marginalization,10parallel260class linear projections,next-byteCE+byteKL+next-tokenCE,rank64Q/VLoRA.
- **Evidence/budget:** PARTIAL v1 §3.2/§4 setup/Table1–3,1B–8Bfamilies,Tulu3/OpenMath. Main CTD deployment **removes byte heads and remains token-level**; only first10bytes of longer tokens supervised. Student heads lack within-token autoregressive conditioning while teacher targets can condition on previous bytes. Not evidence of exact whole-string distribution equivalence or all-byte deployment.

### S04-R048 — S04-N11 — Cheap cross-interface heads do not guarantee capability retention [BYTE-transfer experiment; A/G]
- **Prior problem:** A common byte supervision space may bridge classifiers but fail to preserve instruction following or token-pretrained knowledge after conversion.
- **One-sentence solution:** Evaluate tokenizer transfer and actual byte conversion separately against SFT and competing distillation baselines.
- **Techniques:** E:FastVocabularyTransfer input/head initialization,LoRA distillation,independent task-level evaluation; no claim of new geometry regularizer.
- **Evidence/budget:** PARTIAL §4.1–4.3 Tables1–3:Llama3.2-3B→Qwen tokenizer IFEval30.58BLD vs62.83MinED/58.51ALM+SFT; BPE→byte MMLU39.06BLD vs60.50original and39.84MinED. Cheap heads optimize losses but do not uniformly rescue behavior. Teacher logit precomputation/storage/beam approximation and seed controls need full reading.

### S04-R049 — S04-N12 — Shared nested vocabulary capacity can cost quality despite exact slicing [MIXED/BPE; T/O]
- **Prior problem:** One model serving several nested subword alphabets may dilute per-cap learning,even when deployment row-slicing is mathematically exact.
- **One-sentence solution:** Train across prefix-nested vocabularies and separately ablate cap labels,output masking and specialist training.
- **Techniques:** E:multi-cap sampling,control tokens,restricted softmax,row slicing,paired-seed factorial controls; embeddings/output head untied in main design.
- **Evidence/budget:** PARTIAL v1 §§II–VI,3.1M/10.6Mbody,200Mtokens/run:reported~3.64%/2.96%BPBpenalties32K/8K but robustness benefits. Tying sensitivity reportedly improves all caps,not full details. **This is byte-level BPE,not256byte generation; multi-cap sharing is not input/output tying.** Equal token counts/context do not equal bytes; rank/regularization attribution remains incomplete.

### S04-R050 — S04-N13 — Large input vocabularies can be parameterized from byte structure without changing token positions [MIXED; T/G/A; A-only]
- **Prior problem:** A BPE input table uses one learned row per token and can encode orthographic variants inefficiently.
- **One-sentence solution:** Replace learned lookup rows with deterministic byte/position features and a shared learned projection while retaining the BPE tokenizer.
- **Techniques:** E as abstract-reported:Kronecker factorization,fixed byte encoder,linear projection,on-the-fly reconstruction; still a token LM objective.
- **Evidence/budget:** ABSTRACT v1:nanoGPT124M,3seeds,2.5Btokens;claims2.5±.2%lower validation loss thanBPE-tied and91–94%frontier **input-side** saving. Output-head capacity/tying and matched total parameters not yet verified; byte-near semantic-far confusions acknowledged. Not evidence that pure byte vocabulary solves output cost or tying regularization.

### S04-R051 — S04-N15 — Teacher token probabilities lose mass under naive byte conversion [BYTE and BYTE+BOUNDARY; A/O/G]
- **Prior problem:** Prefix-matching marginalization that ignores already-terminated tokens cannot preserve later-byte probabilities from a single teacher pass.
- **One-sentence solution:** Either accept approximate prefix-renormalized targets or add an explicit end-of-token symbol to preserve termination mass in the marked byte representation.
- **Techniques:** E:Marginalize-It vsEnd-Of-Token probability conversion,teacher distribution distillation,dense byte Transformer; exactness concerns the **marked representation**,not an unmarked-byte marginal magically obtained for free.
- **Evidence/budget:** PARTIAL v1 §§2/3:1.28Blayerparams,token1.81Btotal,byte1.28B;markedstream~30.94%extra compute/data,≤1Tbytes. Low-compute token advantage and fitted high-compute byte ceilings coexist. Full scaling fits,teacher/storage costs and special cases unread. Small alphabet lowers classifier/logit storage,but efficiency,regularization and extra computation remain different explanations.

## Cross-record classification guide and unresolved comparisons

| Mechanism cluster | Representative records | What is established | Missing discriminating evidence |
|---|---|---|---|
| T — table sharing and parameter allocation | R001/R003/R005/R007/R009/R049 | Alphabet size/table sharing/depth sharing are distinct design axes; positive historical word/subword results exist | A broad byte-specific tied/untied census with fixed checkpoint/code versions; matched geometry/optimizer/total-parameter tests |
| G — normalized/readout geometry and rank | R013/R015–R020/R041/R050 | Row normalization/full cosine/scale/transformed tying are not synonyms; narrow linear adapters can bound rank | Byte-head geometry experiments; per-class vs scalar temperature controls; byte-vocabulary feasibility of orthogonal-memory proposals |
| A — pretrained interface compatibility | R002/R025/R029/R040–R048 | Actual byte conversion may require encoder/decoder/boundary alignment; token-only and byte-only endpoints must be distinguished | Full latest Bolmo and competing-distillation tables/causal diagrams; exact stage costs and matched extra-training comparisons |
| O — signal routing and optimization history | R022–R035/R042/R044–R047 | Authors use deep supervision,loss separation,stop-gradient,ratio control,curricula and auxiliary heads for different purposes | Gradient histories vs conjectured competition; training-only parameter/FLOP accounting; matched schedule and seed controls |
| C — latent-use background | R036–R039 | Decoder capacity and inference lag can change stochastic latent use; nonzeroKL need not improve LM | No direct translation to deterministic-byte failures without actual posterior/objective correspondence |

**Synthesis guardrails:** Report byte-specific mechanisms positively in their own task contracts. Do not turn background caveats into a field-wide negative verdict. The strongest missing experiment in the *literature evidence* is a matched small-alphabet tying/geometry/optimizer study; this statement is not a recommendation to run unauthorized experiments. Next action is the bounded selected-reading queue, not production edits or training.
