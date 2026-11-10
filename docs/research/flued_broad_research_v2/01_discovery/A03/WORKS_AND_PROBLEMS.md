# A03 — Native addressing/readout: works and problems

Date: 2026-11-09. Discovery-stage specialist inventory, not the final broad-report synthesis. Scope: the addressing/native-readout list in the canonical follow-up directions, independently of whether a multigranularity architecture is eventually selected.

## Evidence and identity contract

- **N** = absent from both supplied work catalogs by stable-ID searches; new to this inventory, not a novelty claim about the field. **A** = recovered from the preceding A03 audit, not new discovery. **U** = existing W-ID with no full card identified in the supplied catalog; newly reverified/recovered, not a new work. **R** = actual existing full card read and reused below.
- **M** = official metadata/abstract only. **P** = specified original-method/results passages read; incomplete paper. **R-FULL** = reuse of a card's declared full scope at its locked version, not a new full reading or independent certification. No work is newly declared FULL in this pass.
- The D01–D21 identifiers are local A03 record keys, not replacements for W/BIW IDs. There are **21 externally reverified/recovered work records: 11 N, 5 A, 5 U**. Twelve separately listed R records reuse actual full cards. These are work/provenance counts, not reading counts.
- Venue evidence is independent of arXiv version evidence. “Preprint; venue not verified here” does not mean rejected or unpublished. No work below is asserted to be an accepted ICLR 2027 paper.
- Every mechanistic statement below is either an author claim within the stated reading scope or explicitly marked **inference**. No paper implementation, experiment, or proof was independently reproduced.

## I. Recovered classical and recent gaps

### D01 — Neural Turing Machines [A; prior audit A01; P]

**Identity:** Alex Graves, Greg Wayne, Ivo Danihelka. [1410.5401v2](https://arxiv.org/html/1410.5401v2), 2014-12-10; [PDF](https://arxiv.org/pdf/1410.5401v2). Technical report/preprint; formal venue not verified. Official Atom confirms the three authors and version.

**Prior problem:** recurrent hidden-state capacity does not make variable binding and long algorithmic access easy to learn. **One-sentence solution:** attach a differentiable memory matrix with controller-produced read/write weightings combining content matching and relative location shifts. **Borrowed mechanisms/roles:** cosine attention supplies content addresses; interpolation, circular convolution and sharpening implement address movement; LSTM-inspired erase/add gates separate removal from insertion. Controller and addresses learn from supervised sequence cross-entropy, not gold memory locations.

**Evidence read:** original §§3.1–3.4, §4.1 and part of §4.2. A feedforward controller's simultaneous access is constrained by head count; a recurrent controller can retain previous reads. Copy extrapolation eventually wraps the 128-slot memory; repeat-count extrapolation can miss termination. These are author-reported limits, not general language-memory guarantees.

**Distinguishes:** content vs positional address formation; simultaneous independent heads vs serial computation; read/write alignment vs mere storage. **Transfer/cost:** finite matrix and dense soft attention; no original-source revisit. Position generalization, access width and controller recurrence must be separately controlled.

### D02 — Dynamic Neural Turing Machine with Soft and Hard Addressing Schemes [A; prior audit A02; P]

**Identity:** Caglar Gulcehre, Sarath Chandar, Kyunghyun Cho, Yoshua Bengio. [1607.00036v2](https://arxiv.org/html/1607.00036v2), 2017-03-17; [PDF](https://arxiv.org/pdf/1607.00036v2). Metadata title says “Soft and Hard”; HTML heading says “Continuous and Discrete.” Same work/version, not two papers. Venue not independently verified.

**Prior problem:** fixed linear location shifts restrict learned access, and a recurrent controller can ignore dynamic memory. **Solution:** partition each cell into a learned fixed address and writable content, train continuous or discrete access, and regularize read/write consistency. **Borrowed mechanisms:** cosine addressing, learned least-recently-used correction, REINFORCE with variance reduction, continuous-to-discrete curriculum, auxiliary next-input prediction. Main loss is task likelihood; the address part is a slow parameter, not runtime-written content.

**Evidence read:** §§2–4.3 and §§6.1–6.3/Table 1; extraction ends at §6.4. §4.3 explicitly reports an address-as-extra-weights shortcut that ignores content. Its consistency penalty aligns reading with historical write weights, not with gold semantic identity. Table 1/§6.3 also acknowledge a gap to MemN2N/DMN+; discrete feedforward access is hard to train and uses longer training.

**Distinguishes:** a query can exist yet fail to read dynamic content; alignment/optimization can fail without changing granularity. **Cost/failure:** taskwise bAbI training, finite 120 cells in the discussed setup, extra regularizers and curriculum; not equal-compute proof that a consistency loss repairs arbitrary native readers.

### D03 — Homogeneous Keys, Heterogeneous Values: Exploiting Local KV Cache Asymmetry for Long-Context LLMs [A; prior audit A03; P]

**Identity:** Wanyun Cui and Mingwei Xu. [2506.05410v2](https://arxiv.org/html/2506.05410v2), 2025-11-06; [PDF](https://arxiv.org/pdf/2506.05410v2). [Official NeurIPS 2025 poster entry](https://neurips.cc/virtual/2025/poster/117046) retrieved. This is the **merging AsymKV**, not D16's quantization AsymKV.

**Prior problem:** adjacent attention keys can be similar while values differ; uniform KV merging confounds selection and payload error. **Solution:** merge approximately homogeneous keys, sum values, and retain cardinalities in attention normalization. **Borrowed mechanisms:** second-order Taylor/Newton reasoning, diagonal Fisher approximation, adjacent-cache merging, count-aware normalization. No weight fine-tuning is required, but key gradients are computed during compression.

**Evidence read:** §§3.1–3.3, §4.6 description; §§3.2 equations (7)–(11) explicitly rechecked. The exact identity holds **after keys have been replaced by identical embeddings**. The original distinct-key replacement remains approximate. §3.1 drops gradient terms for stability; §3.3.2 states selective gradient computation. §4.6 crosses four key-merge schemes with same-rule vs asymmetric value merging; complete numerical tables/appendices remain unread.

**Distinguishes:** content loss vs address loss vs repeated softmax mass. **Transfer/cost:** exact equality concerns a particular attention operator, not recovery of original individual values, and not repeated delta-rule writes. Integer counts, gradient construction and retained cache bytes belong in the cost ledger.

### D04 — Reducing Transformer Key-Value Cache Size with Cross-Layer Attention [A; prior audit A04; P]

**Identity:** William Brandon et al. [2405.12981v1](https://arxiv.org/html/2405.12981v1), 2024-05-21; [PDF](https://arxiv.org/pdf/2405.12981v1). Official Atom confirms five authors. Preprint; formal venue not verified.

**Prior problem:** independent per-layer KV caches multiply persistent memory. **Solution:** let several query-producing layers reuse KV computed by an earlier layer. **Borrowed mechanisms:** multi-query/grouped-query sharing extended along depth; ordinary autoregressive training from scratch learns the altered architecture.

**Evidence read:** §2.1–2.3 and abstract/results overview. Shared KV has fewer writers but still multiple readers; this is not multiple layers writing into a common summary. §2.3 notes that each consuming layer still rereads shared KV from memory, so reduced storage does not automatically reduce decode attention bandwidth.

**Distinguishes:** writer independence vs query independence vs residual/value mixing across depth. **Cost/failure:** compare resident KV bytes, projections, communication and repeated reads, not just number of cached layers. Full training/quality frontiers and appendix controls remain unread.

### D05 — The Devil in Linear Transformer [A; prior audit A06; M]

**Identity:** Zhen Qin et al. [EMNLP 2022 official record](https://aclanthology.org/2022.emnlp-main.473/), pp. 7025–7041, DOI 10.18653/v1/2022.emnlp-main.473; [PDF](https://aclanthology.org/2022.emnlp-main.473.pdf). Official proceedings version is the reading target, not an unspecified arXiv revision.

**Prior problem:** linear transformers suffer unstable attention gradients and dilution over long sequences. **Solution:** replace the problematic scaling with normalization and use early diagonal/local attention. **Borrowed mechanisms:** normalization for stable optimization plus a locality prior; these are separate interventions. **Learning:** end-to-end task training, as stated in the abstract; exact schedules/ablations not read.

**Depth:** official abstract and bibliography only. Unbounded-gradient theorem, denominator assumptions and complete ablations are **unread**.

**Distinguishes:** numerical/training failure and broad attention dilution from irreversible content loss. It cannot yet establish which normalization alone improves address binding, or whether the early-local mechanism explains a result. No source revisit required; no universal fix inferred.

### D06 — MHLA: Restoring Expressivity of Linear Attention via Token-Level Multi-Head [U = W0219; P]

**Identity:** Kewei Zhang et al. [2601.07832v2](https://arxiv.org/html/2601.07832v2), 2026-01-14; [PDF](https://arxiv.org/pdf/2601.07832v2). Preprint; venue not verified. Existing catalog already contains W0219, so not new.

**Prior problem:** a shared global linear-attention summary can collapse query-specific representational diversity. **Solution:** partition along the token dimension, compute local summaries and mix them with a learned coefficient matrix. **Borrowed mechanisms:** multi-head factorization moved to token groups; blockwise matrix multiplication; learned position-indexed coefficients. These heads are not automatically independent channel heads or arbitrary learned slot addresses.

**Evidence:** metadata/abstract and method §4.1–4.2 recovered from current HTML and the prior audit; appendix causal/streaming details not fully read. Static learned coefficients should not be silently relabeled input-generated routing. Complexity's constants depend on the number of groups; the extracted profiling discussion mentions the regime M²<N.

**Distinguishes:** avoiding one global summary vs learning better native queries vs adding state. **Cost/failure:** causal masking, group count, current-block visibility and matched resident state need full reading before a generative-memory comparison.

### D07 — On State Reduction in Linear Attention [U = W0086; M]

**Identity:** Philipp Nazari and T. Konstantin Rusch, [2602.04852v3](https://arxiv.org/abs/2602.04852v3), 2026-09-29; [PDF](https://arxiv.org/pdf/2602.04852v3). Preprint; venue not verified. Both authors recovered from official Atom.

**Prior problem:** trained recurrent states may underuse nominal capacity. **Solution:** analyze key/value-induced state rank and structurally prune key/query projections using rank-revealing QR while preserving fast-kernel shapes. **Borrowed mechanisms:** structured pruning, matrix rank analysis, QR factorization; post-pretraining reduction rather than adding a retrieval hierarchy.

**Evidence:** original abstract/history/Atom only. Authors claim states can often be halved with modest perplexity cost; retrieval-specific failures and pruning adaptation details are unread.

**Distinguishes:** actual task-relevant rank deficiency vs harmless redundancy. **Boundary:** low rank is not automatically lost information, and perplexity retention is not proof of preserved rare-identifier recall. Exact rank object and finite-precision conditions must be read. Nominal matrix size is not trained usable capacity.

### D08 — Dual DeltaNet: Value-Side Memory Reorganization for Linear Attention [U = W0203; M]

**Identity:** Yixiao Qian et al. [2610.38578v1](https://arxiv.org/abs/2610.38578v1), 2026-10-28; [PDF](https://arxiv.org/pdf/2610.38578v1). Six authors confirmed by official Atom; preprint, venue not verified.

**Prior problem:** key-side delta corrections do not explicitly reorganize how related values occupy addresses. **Solution:** add a complementary value-side read/update to KDA, with a two-sided delta rule and rank-2 recurrence. **Borrowed mechanisms:** associative-memory residual correction, dual matrix views Sᵀk and Se, chunkwise parallelization. Main language-model training and selector learning particulars remain unread.

**Evidence:** abstract and version identity only. “Strongest overall” is the authors' abstract claim, not an audited ranking. **Distinguishes:** write-side interference/reorganization from coarse query granularity, with no source revisit. Need the value-selector inputs, leakage permissions, separate key/value update ablations, rank/cost and negative results before recommending it.

### D09 — Hopfield Networks is All You Need [U = W0240; P]

**Identity:** Hubert Ramsauer et al. [2008.02217v3](https://arxiv.org/html/2008.02217v3), 2021-04-28; [PDF](https://arxiv.org/pdf/2008.02217v3). Existing catalog records ICLR 2021; this pass verifies arXiv version, not the decision forum anew.

**Prior problem:** classical associative-memory dynamics and modern attention need a common continuous retrieval formulation. **Solution:** define a log-sum-exp energy and continuous update with attention-shaped association. **Borrowed mechanisms:** energy minimization, concave-convex procedure, softmax, learned query/key/value projections. Hopfield layers can be trained inside downstream architectures; the theorem does not guarantee the native query is learned.

**Evidence read:** §2 equations (1)–(10), definitions and Theorems 1–5; proofs/remaining experiments unread. One-step closeness requires sufficient pattern separation and a nearby query; convergence can be to global averaging or metastable clusters rather than the desired fact. Explicit stored patterns remain in the operator.

**Distinguishes:** single-step retrieval sufficiency under basin conditions vs iterative query refinement; approximation error vs wrong attraction basin. **Boundary:** exponential patterns in feature dimension is not a constant-total-bits language-memory guarantee, and arbitrary independently projected KV recurrence does not automatically inherit the same energy descent.

### D10 — Object-Centric Learning with Slot Attention [U = W0100; M; original HTML blocked]

**Identity:** Francesco Locatello et al. [2006.15055v2 PDF](https://arxiv.org/pdf/2006.15055v2), 2020-10-14. Official Atom verifies title, eight authors, version and author comment “NeurIPS 2020”; formal proceedings not separately opened. HTML failed twice, initial attempt plus one retry.

**Prior problem:** distributed visual representations do not explicitly separate compositional objects. **Solution:** produce exchangeable slots that specialize through competitive attention over multiple rounds. **Borrowed mechanisms:** iterative attention and competition; training on object discovery/property prediction, per official abstract.

**Evidence:** official abstract/metadata only. GRU update, normalization direction and full ablations are not newly verified and are deliberately left for reading.

**Distinguishes:** multiple slot vectors vs independently bound slots and one-shot vs iterative assignment. **Boundary:** object-centric bidirectional perception does not establish causal streaming text-memory behavior or independent queries at deployment. This is a recovered unread classic, not an existing full card.

## II. Newly verified candidates, controls, and counterexamples

### D11 — End-To-End Memory Networks [N; P]

**Identity:** Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, Rob Fergus. [1503.08895v5](https://arxiv.org/html/1503.08895v5), 2015-11-24; [PDF](https://arxiv.org/pdf/1503.08895v5); [official NIPS 2015 proceedings entry](https://proceedings.neurips.cc/paper/5846-end-to-end-memory-networks). No matching stable ID in either supplied catalog.

**Prior problem:** discrete supporting-fact supervision and one-shot access limit flexible memory reasoning. **Solution:** train differentiable memory reads end-to-end from answer supervision and update the query across hops. **Borrowed mechanisms:** separate address/output embeddings, softmax attention, recurrent query updates u(k+1)=u(k)+o(k), adjacent or layerwise weight tying, linear-start curriculum. Supporting-fact labels are not required for its main model.

**Evidence read:** §§2.1–2.2, §§4.1–4.4/Table 1, §5's query construction and stated limitations. In the language-model arm the initial query is a fixed 0.1 vector, not the current token's hidden state. Multi-hop gains coexist with hard task failures; more hops do not monotonically improve every row. Ten restarts and choosing a best run on some settings constrain the evidence.

**Distinguishes:** adaptive query computation vs additional parameter depth vs seeing more source. **Cost/failure:** all memory entries remain available and repeated hops cost extra computation; original task setup is not a fixed compressed-state model. Control by repeating the first read, adding a compute-matched non-reading network, and holding memory fixed.

### D12 — GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints [N; P]

**Identity:** Joshua Ainslie et al. [2305.13245v3](https://arxiv.org/html/2305.13245v3); [EMNLP 2023 official entry](https://aclanthology.org/2023.emnlp-main.298/), [PDF](https://aclanthology.org/2023.emnlp-main.298.pdf). Version number locked; exact v3 date not independently recovered in this pass.

**Prior problem:** full KV-head diversity costs decode bandwidth, while one KV head can degrade quality and stability. **Solution:** share KV within query-head groups and adapt mean-pooled MHA checkpoints with additional pretraining. **Borrowed mechanisms:** grouped parameter sharing, checkpoint averaging and continued pretraining. Native query heads remain distinct even when KV are shared.

**Evidence read:** §§2–3.3 and Appendix A. Original uptraining proportion sweep compares zero/5%/10%; MQA needs adaptation to become useful, while GQA fares better immediately. Mean/first/random initialization are compared. §3.1 reports roughly 600 TPUv3 chip-days for 5% adaptation: “small fraction” is not a free repair. Only encoder-decoder hosts tested; XXL from-scratch counterpart missing.

**Distinguishes:** replacement shock vs permanent representational loss, and independent q vs independent KV. **Counterexample:** D19's blanket statement that GQA must be designed before pretraining conflicts with this original conversion study. The correction does not imply any desired conversion is cheap or guaranteed.

### D13 — Query-Key Normalization for Transformers [N; P]

**Identity:** Alex Henry et al. [2010.04245v1](https://arxiv.org/html/2010.04245v1), 2020; [Findings of EMNLP 2020 official entry](https://aclanthology.org/2020.findings-emnlp.379/), pp. 4246–4253; [PDF](https://aclanthology.org/2020.findings-emnlp.379.pdf).

**Prior problem:** unrestricted query/key norms may arbitrarily saturate softmax in low-resource translation. **Solution:** normalize q and k per head and learn the logit scale, leaving values unnormalized by this operation. **Borrowed mechanisms:** cosine attention, learned temperature and initialization based on training sequence lengths. Supervision is bilingual sequence likelihood; other normalization choices also change in the main comparison.

**Evidence read:** §§2–4 and Appendix C discussion. The largest ablation drop is reported when learned scale g is removed; normalized logits in [-1,1] can be too diffuse. Main comparison also switches ScaleNorm to LayerNorm; do not attribute the entire average BLEU gain to q/k directions alone. Tables were not fully numerically extracted, and authors call the proposed explanation conjectural.

**Distinguishes:** geometry/direction vs scale vs training saturation, not content compression. **Cost/transfer:** tiny added scale parameter but new training/retuning requirements; low-resource translation is not long-delay exact recall. Normalization without scale is an essential negative control.

### D14 — Alignment Attention by Matching Key and Query Distributions [N; P]

**Identity:** Shujian Zhang, Xinjie Fan, Huangjie Zheng, Korawat Tanwisuth, Mingyuan Zhou. [2110.12567v1](https://arxiv.org/html/2110.12567v1), 2021-10-25; [PDF](https://arxiv.org/pdf/2110.12567v1). Official Atom says NeurIPS 2021; [official proceedings PDF search result](https://proceedings.neurips.cc/paper/2021/file/6fd6b030c6afec018415662d0db43f9d-Paper.pdf) not fully read.

**Prior problem:** learned q/k projections may induce poorly matched distributions. **Solution:** add unsupervised within-head distribution alignment to existing attention. **Borrowed mechanisms:** adversarial discriminator with gradient reversal, entropy-regularized optimal transport/Sinkhorn, or bidirectional conditional transport. Task objectives coexist with alignment loss; the model does not receive gold dynamic read/write associations through this loss.

**Evidence read:** §2.3 methods and selected experimental description. **Our inference/counterexample:** identical marginal q/k distributions can coexist with a permutation of semantic bindings. Marginal alignment is therefore not the same as D02's read/write consistency, shared q/k weights, or correct paired addressing.

**Distinguishes:** distribution mismatch as a trainable interface problem vs absence of target information. **Cost/failure:** discriminator/transport and alignment coefficient affect training; results on language understanding/VQA do not establish causally deployed memory access. Need collapse, paired-matching and alternative normalization controls.

### D15 — Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free [N; P]

**Identity:** Zihan Qiu et al. [2505.06708v1](https://arxiv.org/html/2505.06708v1), 2025-05-10; [PDF](https://arxiv.org/pdf/2505.06708v1). Preprint identity verified; NeurIPS 2025 oral is a search/author-repository pointer, not independently venue-certified in this record.

**Prior problem:** gating benefits are commonly entangled with routing, head design and other architectural changes. **Solution:** systematically compare gate positions and forms, finding head-specific query-dependent sigmoid gating after attention effective in the tested models. **Borrowed mechanisms:** multiplicative gates, sparsity and nonlinear value/output composition, standard language-model training.

**Evidence read:** §§1–2.2, Table 1 and §3.2.1, selected appendix discussion. Gates after q/k, v, attention output and final projection are distinct variants. Gains can persist in a single-expert configuration, a direct warning against attributing all benefit to expert routing. Sparse output gating can modulate consumption without changing which keys were matched.

**Distinguishes:** address selection vs returned content magnitude/nonlinearity; more heads vs head-specific gates. **Cost/failure:** elementwise gating may add appreciable projection parameters; headwise controls are smaller. Full matched budgets, sink metrics and long-context results need remaining original reading. No proof that low attention mass or a zero gate means missing content.

### D16 — AsymKV: Enabling 1-Bit Quantization of KV Cache with Layer-Wise Asymmetric Quantization Configurations [N; M]

**Identity:** Qian Tao, Wenyuan Yu, Jingren Zhou. [COLING 2025 official entry](https://aclanthology.org/2025.coling-main.158/), pp. 2316–2328; [PDF](https://aclanthology.org/2025.coling-main.158.pdf). Proceedings version is authoritative here; arXiv 2410.13212 is a related reference not independently read.

**Prior problem:** equal key/value quantization settings ignore unequal output sensitivity. **Solution:** use layerwise asymmetric bit configurations to protect the more sensitive key side. **Borrowed mechanisms:** activation/cache quantization and attention-output error analysis; exact calibration/training method is unread.

**Evidence:** official abstract/metadata only; authors report up to 75% decoder layers at one bit under their tested settings, not an all-layer/all-model guarantee. **Distinguishes:** precision errors in logits vs values. **Important non-equivalence:** its greater key-quantization sensitivity does not contradict D03's local-key merging observation or D19's key-feature redundancy; error operators differ. This is a second work named AsymKV, not another version of D03.

### D17 — Low-Rank Key Value Attention [N; P]

**Identity:** James O'Neill, Robert Clancy, Mariia Matskevichus, Fergal Reid. Initially fetched [2601.11471v1](https://arxiv.org/html/2601.11471v1), 2026-01-16; official Atom exposed [v3](https://arxiv.org/html/2601.11471v3), 2026-04-07, subsequently fetched for updated methods/analysis. [v3 PDF](https://arxiv.org/pdf/2601.11471v3). Same work, not two entries. Venue unverified; the keyword “ICML” is not acceptance.

**Prior problem:** complete KV sharing can remove useful head differences while independent caches duplicate structure. **Solution:** use a shared dense KV component plus cached head-specific low-rank residuals. **Borrowed mechanisms:** low-rank additive factorization, jointly trained projections, operator-space head-diversity analysis using Wq Wkᵀ and centered Gram matrices. This is activation/cached-feature design, not merely a LoRA weight adapter.

**Evidence:** v1 methods/§6.3 targeted; v3 §3 and §4.3 targeted passages and appendix headings. Author analysis finds query specialization can partly compensate for shared keys; raw K-weight similarity alone misses this. Rank, query freedom and total state remain different axes. Version v3 clarifies fewer training steps vs per-step speedup.

**Source cautions:** v3 introduction says 2.6 GB exceeds 5 GB, an obvious arithmetic contradiction; do not inherit this motivation. v1 and v3 have different headline scales and analysis metrics, so do not splice their numbers. **Distinguishes:** independent query operators vs distinct cached KV, with finite residual rank. Full cost/position-compatibility validation and causal binding controls remain unread.

### D18 — DynaCalKV: Key-Value Cache Compression via Head Grouping and Adaptive Rank Allocation [N; P]

**Identity:** Tan T. Nguyen and Quan V. Dang. [2607.24331v1](https://arxiv.org/html/2607.24331v1), 2026-07-27; [PDF](https://arxiv.org/pdf/2607.24331v1). Preprint; venue unverified.

**Prior problem:** fixed head groups/rank budgets ignore nonuniform redundancy, and K/V need different approximations. **Solution:** cluster key heads by centered kernel alignment and adapt group ranks while separately calibrating value factorization. **Borrowed mechanisms:** SVD, Fisher-based layer allocation, CKA clustering, greedy budget adjustment and alternating closed-form least squares for values. Calibration uses WikiText-2; the target model need not be fully retrained.

**Evidence read:** §§III-B–D and §IV setup/limitations/LongBench discussion. All long-context methods nearly fail on SmolLM2, so authors omit that uninformative comparison. Long-context degradation is substantially worse on the tested GQA Llama than the MHA Qwen host; this is not a same-model causal test of GQA itself because host architecture and pretraining differ.

**Distinguishes:** compressible key-head redundancy vs already-shared head overcompression; calibration vs end-to-end adaptation. **Cost/failure:** offline calibration, factors and actual compressed cache/parameter budgets are distinct; performance tables are not all fully extracted. Not evidence that CKA predicts semantic binding or exact-memory survival.

### D19 — Thin Keys, Full Values: Reducing KV Cache via Low-Dimensional Attention Selection [N; P]

**Identity:** Hengshuai Yao, Xing Chen, Ahmed Murtadha, Guan Wang (official Atom; HTML extraction omits Chen). [2603.04427v3](https://arxiv.org/html/2603.04427v3), 2026-03-18; [v3 abstract/history](https://arxiv.org/abs/2603.04427v3), [PDF](https://arxiv.org/pdf/2603.04427v3). Atom latest v4 is 2026-03-28; v4 **not read**, do not upgrade v3 results. Preprint, venue not verified.

**Prior problem:** equal q/k/v feature widths may overallocate selection dimensions. **Solution:** factor key projections and absorb the complementary transform into query projections while retaining full values, optionally adapting q/k only. **Borrowed mechanisms:** truncated SVD, low-dimensional selection, parameter-restricted fine-tuning; from-scratch and post-training settings both appear.

**Evidence read:** §§2.1–2.3, §3.1/3.4, §§8.1–8.4, §6 limitations, selected §11. The source compares positional copy vs randomized content lookup; it also uses identically fine-tuned uncompressed controls, and exposes greater reasoning sensitivity and data-domain-dependent repair.

**Our cautions:** §2.3 writes exact score equality after Wk≈AB, but truncation is approximate unless discarded directions are immaterial. Johnson–Lindenstrauss distance preservation needs distortion/margin/query-set assumptions; it is not a universal log-N guarantee for all future query rankings. The no-GQA-conversion statement is contradicted by D12. Rotation/position transformations and logit scale must be checked before transferring algebra to an actual implementation.

**Distinguishes:** selection width vs value width vs interface adaptation; frozen failure vs recoverable reader mismatch. Savings in key cache are not equal to total KV savings, and LM perplexity is not exact-string retrieval.

### D20 — How Linear Attention Remembers [N; P]

**Identity:** Kichang Lee, JaeYeon Park, Songkuk Kim, JeongGil Ko. [2609.33093v1](https://arxiv.org/html/2609.33093v1), 2026-09-27; [PDF](https://arxiv.org/pdf/2609.33093v1). Preprint; venue not verified.

**Prior problem:** performance/probes do not identify how pretrained recurrent states actually write, retain and read facts. **Solution:** combine a recurrent contribution decomposition with donor-write, pre-query state and query-output interventions in pretrained GLA/GDN. **Borrowed mechanisms:** causal activation patching, content-consistent donor swaps, norm-matched controls, development/confirmation splits and source-cluster uncertainty. No additional fine-tuning.

**Evidence read:** original §§2.3–4.2, discussion/limitations; targeted appendix prose-pilot conclusion. Selective multi-fact editing coexists with nonadditive/cross-fact coupling. Holding sequence length fixed while varying fact load separates load from elapsed distance. In tested hybrids the immediate recalled identity lies mostly in full-attention KV, but recurrent contributions to earlier query/KV formation are not excluded.

**Critical boundary:** query-time **output** mediation is not an isolated intervention on q formation. Four-choice conditional-likelihood recall differs from free generation; the prose pilot fails a competence prerequisite and receives no downstream causal analysis. **Distinguishes:** write loss vs retention vs deployed read pathway, and nominal “independent slots” vs interacting support. Full appendix/artifact audit and broader relational tasks remain open.

### D21 — GateSight: Recurrent Memory Anticipates Attention Memory for Query-Agnostic KV Eviction in Hybrid LLMs [N; P]

**Identity:** Junjie Li, Jiong Lou, Jie Li. [2610.14754v1](https://arxiv.org/html/2610.14754v1), 2026-10-10; [PDF](https://arxiv.org/pdf/2610.14754v1). Title/prefix corrected from official Atom; preprint, venue unverified.

**Prior problem:** before future questions arrive, how can a hybrid model decide which full-attention entries to retain? **Solution:** predict future KV output influence from recurrent write/decay/value-magnitude signals using per-head small networks and a gate-derived layer budget. **Borrowed mechanisms:** rollout-generated influence targets, exact local leave-one-out formulas with other variables fixed, ridge vs nonlinear predictors, cache compaction. Training uses generic documents and sampled model continuations; serving inputs do not include the later question.

**Evidence read:** §§2–4 targeted and experiment/cost descriptions. Their utility is ungated layer-output change over model continuations, not answer-specific causal correctness. The nonlinear model improves high-utility-tail recall despite slightly lower global rank correlation, warning against one scalar diagnostic. The second host's estimator is retrained with the same recipe, not transferred unchanged.

**Distinguishes:** useful control/selection signals in recurrent computation vs the recurrent state directly storing the final answer. Thus it need not contradict D20. **Cost/failure:** offline labeling/training, host-specific estimators and physical release count; current-query-agnostic is not future-distribution-invariant. It retains token KV, so this is a finite-cache comparator, not a closed-state recovery guarantee.

## III. Actual full-card reuse ledger — no recount

All twelve cards below were read in this pass. Each link points to the actual card, not a catalog summary. Venue labels here are inherited from the locked card unless stated unknown, not independently recertified. The card's detailed limitations remain authoritative.

| Existing ID / exact title and version / card | Venue status / evidence | Prior problem → one-sentence solution / borrowed mechanism and learning | A03 distinction and claim restriction |
|---|---|---|---|
| **W0229**, Test-time regression: a unifying framework for designing sequence models with associative memory, [2501.12352v3](https://arxiv.org/html/2501.12352v3), 2025-05-02; [actual card](../../../flued_multigranularity_survey_20261108/03_reading/B06/W0229.md) | Venue unknown here; R-FULL, §3–6 and appendix scope in card | Confounded memory designs → separate regression weights, function class and optimizer; least squares, Gram correction, online SGD/delta, local kernel regression; causal prefix supplies online examples, LM supplies slow-parameter learning | Bigram q/k/v construction itself can make MQAR solvable; oracle/ridge reads do not certify learned native q or affordable deployment |
| **W0212**, A Geometry-Based Capacity Theory for Finite-Feature Associative Memory, [2610.09056v1](https://arxiv.org/html/2610.09056v1), 2026-10-06; [card](../../../flued_multigranularity_survey_20261108/03_reading/B06/W0212.md) | Preprint; R-FULL | Key-only capacity claims ignore value correlations → model key overlap jointly with value Gram; Hebbian outer product, random Fourier features, whitening analysis; mostly fixed representations rather than causal LM learning | Exact stored-key queries and fixed additive writes; correlated values can help or hurt; no general theorem for delta, noisy q, finite bits or learned consumption |
| **W0214**, RAM-Net: Linear-Time Sequence Modeling with Sparsely Addressable State, [2602.11958v2 PDF](https://arxiv.org/pdf/2602.11958v2), 2026-10-06; [card](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0214.md) | Venue unknown; R-FULL; same work as older title | Dense state access → independent sparse read/write addresses in fixed per-head arrays; product address factors, top-K, temperatures, positional shifts, LM training | Total residency is not active elements; read/write quota imbalance and address collision are real failures; not fixed-total-bits superiority |
| **W0204**, MoM: Linear Sequence Modeling with Mixture-of-Memories, [2502.13685v4 PDF](https://arxiv.org/pdf/2502.13685v4), 2025-11-18; [card](../../../flued_multigranularity_survey_20261108/03_reading/B16/W0204.md) | Venue unknown; R-FULL | Single-state interference → route updates among matrices plus shared state; top-k routing, dedicated K/V, load balancing, LM gradients | Shared q and same write/read route do not establish independent read heads; linear read/mix order can be algebraically equivalent; active budget differs from total state |
| **W0210**, Multi-State Linear Attention with Generalized Second-Order Routing, [2610.37645v1](https://arxiv.org/html/2610.37645v1), 2026-10-27; [card](../../../flued_multigranularity_survey_20261108/03_reading/B06/W0210.md) | Preprint; R-FULL | Segment mean keys miss query-dependent spread → dedicated routing q/k plus first/second moments; moment statistics, temperatures and gate; LM continuation plus synthetic tasks | Routing q is not state-reading q; separately trained routes do not isolate frozen-bank effects; read all states and growing memory; partial-segment normalization question preserved |
| **W0237**, LoLA: Low-Rank Linear Attention With Sparse Caching, [2505.23666v3](https://arxiv.org/html/2505.23666v3), 2026-06-13; [card](../../../flued_multigranularity_survey_20261108/03_reading/B06/W0237.md) | Card PDF says TMLR 06/2026; R-FULL | Uniform compression loses exceptional associations → retain high-self-recall-error KV with linear state/window; error-based selection, teacher-learned features, shared normalization denominator | Residual/self-recall difficulty is not future utility; exact exceptions cannot be recovered after eviction; cached projections are not original source |
| **W0287**, Attention Residuals, [2603.15031v1 PDF](https://arxiv.org/pdf/2603.15031v1), 2026; [card](../../../flued_multigranularity_survey_20261108/03_reading/B07/W0287.md) | Technical report; R-FULL | Fixed depth aggregation → learned content-conditioned depth weights from fixed pseudoqueries; RMS-normalized keys, softmax, layer-group sums, LM training | Fixed q is not current-input q; depth blocks are not source blocks; multihead variant not automatically better; all sublayers still execute |
| **W0289**, Depth-Attention: Cross-Layer Value Mixing for Language Models, [2606.05014v2](https://arxiv.org/html/2606.05014v2), 2026-06-13; [card](../../../flued_multigranularity_survey_20261108/03_reading/B15/W0289.md) | Preprint; R-FULL | Layer-isolated value streams → dynamically mix earlier/current values at the same position; depth softmax, value replacement, next-token training | Mixed values replace originals; keys retained; not independent multiwriter common memory; uniform vs dynamic mixing is a useful existing control |
| **W0197**, Landmark Attention / Random-Access Infinite Context Length for Transformers, [2305.16300v2](https://arxiv.org/html/2305.16300v2), 2023-11-20; [card](../../../flued_multigranularity_survey_20261108/03_reading/B01/W0197.md) | NeurIPS 2023 inherited; R-FULL | Long-context full scans → learned block gates followed by original token-KV reads; grouped softmax and per-query/head selection, LM training | Landmark's own final value weight is zero; coarse address is not coarse payload; shared-selection controls show a trade-off, not closed-state recovery |
| **W0174**, HISA: Efficient Hierarchical Indexing for Fine-Grained Sparse Attention, [2603.28458v5](https://arxiv.org/html/2603.28458v5), 2026-11-03; [card](../../../flued_multigranularity_survey_20261108/03_reading/B01/W0174.md) | Preprint; R-FULL plus scoped earlier-version checks | Expensive token index scanning → block-mean coarse index then token reranking; inherited indexer, fixed pooling, no new training | Values stay token-level latent KV; candidate-pool confounds and long-position misses remain. Use as address/payload separation reference, not governing architecture |
| **W0092**, A Theory of Usable Information Under Computational Constraints, [2002.10689v1 PDF](https://arxiv.org/pdf/2002.10689v1), 2020; [card](../../../flued_multigranularity_survey_20261108/03_reading/B13/W0092.md) | ICLR 2020 inherited; R-FULL | Shannon information ignores consumer limits → compare best risks inside a specified predictor family; constrained prediction and generalization analysis | Family optimum ≠ trained reader ≠ actual causal consumption; deterministic preprocessing can improve accessibility without restoring discarded information |
| **BIW-0117**, Perceiver IO: A General Architecture for Structured Inputs & Outputs, [2107.14795v3 PDF](https://arxiv.org/pdf/2107.14795v3), 2022-03-15; [actual byte-survey card](../../../byte_language_interface_survey/03_reading/R01/BIW-0117.md) | ICLR 2022 inherited; R-FULL, PDF pp.i–xxix with language-specific scope | Latent bottleneck lacks flexible output indexing → output queries read the same latent array; learned positional/task queries, cross-attention and task learning | Position-specific language queries see bidirectional masked-input latents, not causal history; no source revisit after encoding. Earlier audit's A05 unread recommendation is superseded by this actual full card, without a new full count |

## IV. Problem-oriented inventory, independent of a hierarchy proposal

| Problem | Substantive reused evidence | Newly recovered evidence | Distinguishing hypothesis / next action |
|---|---|---|---|
| Who forms the query, and what can it see? | W0229, W0210, W0287, BIW-0117 | D01, D02, D11, D14, D20 | Native-q deficiency vs unavailable information; hold bank/content/visibility fixed, vary only q formation and allowed adaptation |
| Address and content compression are conflated | W0197, W0174, W0237 | D03, D16, D18, D19 | Fine K/coarse V vs coarse K/fine V, then error operator and count normalization; do not collapse feature rank, temporal granularity and bits |
| Read/write semantic binding is not guaranteed | W0214, W0204 | D02, D14, D20 | Coaddressing and marginal distribution matching are different; test paired-binding permutations and causal content changes |
| Conditions/rank/gates can disable a usable payload | W0229, W0212, W0287 | D05, D07, D13, D15, D17 | Direction vs norm vs Gram conditioning vs gate placement; rank alone cannot localize the failure |
| More slots/heads can change several budgets at once | W0204, W0214, W0197 | D06, D10, D12, D17, D18, D20 | Independent q, independent K/V, separate physical state, nonlinear fusion and total bits are separate factors |
| Layerwise writing differs from depth mixing | W0287, W0289 | D04, D11 | Independent writers vs shared writer/multiple queries vs mixed values; no current paper certifies arbitrary multiwriter shared-summary transfer |
| More reads can mean reasoning or just more compute | W0229, BIW-0117 | D02, D09, D10, D11 | Adaptive query update vs repeated same read vs compute-matched non-reading transform; no extra information permission |
| A frozen replacement can fail although an adapted interface works | W0210 and byte-survey protocol caveats | D12, D18, D19 | Compare change-minus-control improvement across matched adaptation budgets; no borrowing the control threshold from a different stage/host |

For exact missing reading questions and discriminating experiments, continue with [READING_HANDOFF.md](READING_HANDOFF.md) and [COVERAGE_AND_FINDINGS.md](COVERAGE_AND_FINDINGS.md). Query/source failures and version boundaries are in [SEARCH_LOG.md](SEARCH_LOG.md).
