# S02 — Detailed problem → solution → AI-technique inventory

**56 records / 32 works.** Read together with [WORKS.md](WORKS.md), which supplies each work’s exact title, stable source/version, publication family, four units, causal contract and actual reading scope. These are normalized, linked records: **each row inherits those work-level fields**, with row-specific evidence, comparator, budget and limits below. No absent numeric cell is reconstructed from a plot or abstract.

`R` = reused original FULL card, actually inspected here; **not a fresh FULL reading**. `P` = primary-source partial reading; `A` = primary abstract only. Old card paths below expand under `docs/research/flued_multigranularity_survey_20261108/`. No code execution or replication. All techniques listed in the “technique and role” field are **explicit author-used mechanisms at the stated depth**, not claims that the authors borrowed them from a particular predecessor. Cluster tags are **our conceptual classification**, not author terminology or proof of ancestry. We introduce no extra analogy as a factual implementation claim.

## 1. Compression-derived segmentation and probabilistic alternatives

### W0404 — Description-length gain, 1999 [A]

Contract: orthographic segmentation; actual digital encoding unknown; offline whole-utterance search. [Institutional abstract](https://scholars.cityu.edu.hk/en/publications/unsupervised-learning-of-word-boundary-with-description-length-ga/), pp.1–6 identity only, not inspected paper pages.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-001 / compression objective | Unsegmented text offers no directly observed lexical units. | Select the utterance segmentation maximizing description-length gain of its component segments. | Minimum description length supplies the segment goodness measure and search objective; **no neural technique claimed**. | Institutional abstract reports lexical correspondence and Brown-corpus experiments; numerical accuracy, search cost, baselines and online constraints unknown. Historical counterexample to treating all boundary learning as a post-2020 neural invention. |

### W0001 — BPE subwords [A]

Contract: original character-to-subword NMT, not raw-byte BPE. [1508.07909v5 abstract](https://arxiv.org/abs/1508.07909v5); full merge algorithm not newly inspected.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-002 / merge prior | Fixed word vocabularies cannot represent novel names, compounds and inflections in translation. | Encode rare and unknown words as smaller subword sequences, including compression-derived BPE units. | BPE supplies corpus-derived segmentation; neural translation learns prediction over those units, **not a gradient over merge decisions**. | Abstract reports +1.1/+1.3 BLEU over dictionary backoff for WMT15 EN–DE/EN–RU; total preprocessing/training budget not inspected. Exact word-splitting and merge inventory require method read; no inference that this paper used UTF-8 byte atoms. |

### W0002 — Unigram segmentation sampling [A]

Contract: sampled subword strings and translation targets. [ACL2018 abstract](https://aclanthology.org/P18-1007/); no section-level claim beyond abstract.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-003 / segmentation uncertainty | A unique deterministic segmentation hides ambiguity and can make NMT brittle out of domain. | Train with multiple subword segmentations sampled probabilistically rather than one fixed path. | Unigram language-model segmentation supports sampling; stochastic segmentation is a data regularizer for translation loss. | Abstract reports especially low-resource/out-of-domain gains; no matched compute or numerical table inspected. This is not continuous hidden-state pooling or exact marginal training of a neural boundary policy. |

### W0016 — Hierarchical Multiscale RNN [P]

Contract: character-symbol causal LM; lower recurrent states summarize spans, upper states update less often. [v7 §§3.2–3.3, §4.1](https://arxiv.org/html/1609.01704v7).

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-004 / learned update clock | Fixed-rate multiscale RNNs cannot synchronize upper updates with variable-length linguistic units. | Learn binary layerwise boundaries selecting UPDATE, COPY or FLUSH/EJECT operations. | LSTM gates accumulate local state; COPY preserves it between updates; FLUSH sends a summary upward and resets local memory; next-character NLL trains the hierarchy without boundary labels. | §4.1/table1: authors’ layer-normalized PTB LSTM1.29 versus HM-LSTM step1.25 BPC, not a byte-scale or equal-FLOP comparison. Text8 has27 symbols. Reset/summary is not invertible span storage; boundary visualizations are qualitative. |
| S02-005 / discrete optimization | Hard boundary states block ordinary backpropagation. | Use a straight-through estimator with a gradually sharpened hard-sigmoid surrogate. | Biased surrogate gradient permits discrete forward choices; slope annealing reduces forward/backward discrepancy as an optimization heuristic. | PTB table1: step+slope1.24, soft/sampled variants1.27 BPC; authors omit slope annealing on larger datasets because schedules are difficult. No unbiasedness or global-optimality claim; no modern wall-clock boundary-cost study. |

### S02-N01 — Fully character-level translation [P]

Contract: character source → fixed-stride source summaries → target characters; **full source visible**, target causal. [1610.03017v3 §§3.3–4.2,5.2,7](https://arxiv.org/html/1610.03017v3).

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-006 / local composition | Character inputs lengthen attention and recurrent processing enough to make NMT impractical. | Run convolutional filters and stride-five max pooling before the source recurrent encoder. | Multiwidth CNN extracts character n-grams; max pooling reduces positions; highway layers regulate feature flow; bidirectional GRU models longer dependencies; translation NLL jointly trains all. | §§4.1/7: pooling5; TitanX12GB; character training about35% slower than bpe2char, rather than “free character input.” Byte/codepoint conversion not reported as a byte model. Different source-length filtering (450characters versus50subwords) weakens same-text exposure claims. |
| S02-007 / local structure | Hard fixed segmentation can cut through useful character patterns at arbitrary boundaries. | Let convolutions cross pooling-cell boundaries so each pooled source segment retains salient overlapping n-grams. | Width1–8 convolutions produce overlapping receptive fields despite nonoverlapping stride cells; max pooling chooses task-useful patterns, not a learned variable boundary. | §4.1 explicitly gives a pattern spanning adjacent cells. Qualitative rare-word/code-switching examples do not independently isolate this mechanism. Moses preprocessing and ISO-9 Russian transliteration remain external priors; complete source access does not transfer to online byte patches. |

### W0386 — Segmental LM for Chinese [P]

Contract: Chinese **characters**; past-context generator, full-observed-sentence posterior segmentation. [1810.03167v1 §§2.2–2.4,3.1–3.3](https://arxiv.org/html/1810.03167v1).

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-008 / latent segmentation | Unlabelled Chinese sentences lack a single gold segmentation to train a segment-generating model. | Maximize sentence likelihood summed over candidate segmentations and recover the best segmentation by dynamic programming. | Context LSTM initializes a segment-decoder LSTM; segment-end symbols terminate units; bounded-length forward DP sums probabilities, Viterbi-style DP finds the maximum. | Equations4–9; K=2/3/4; table1 PKU80.2/79.8/79.2 F1, showing larger maximum segments are not uniformly better. “Linear” algorithm statement is conditional on bounded K and segment scoring. No demonstration of global-model compression speed or prefix-invariant posterior boundaries. |
| S02-009 / objective mismatch | Good generative segmentation may disagree with human annotation conventions. | Add a small guideline-labelled subset or explicit particle-splitting postprocessing when matching a particular segmentation standard. | Supervised likelihood supplies guideline information; rule postprocessing supplies a separate linguistic prior. | Table2 SLM-4 PKU79.2→87.5 with1024 labelled sentences; adding rules to that variant drops to87.3. Unlabelled training includes test text and character embeddings from Gigaword; neither a held-out LM generalization result nor a label-free result for the stronger row. |

### W0401 — Segmental neural language model [A]

[ACL2019 abstract](https://aclanthology.org/P19-1645/); method HTML inaccessible. Character sequence, latent word-like grouping; visual conditioning is optional additional information.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-010 / predictive grouping | Word discovery trained in isolation does not jointly learn sentence usage or grounded meaning. | Jointly learn latent word-like units and predictive language distributions, optionally conditioning on visual context. | Segmental neural LM couples lexical discovery with prediction; visual representation provides grounding context. Exact mixture, DP, regularization and optimization remain unknown at abstract depth. | Abstract reports predictive distributions better than character LSTM and segmentation competitive with nonparametric Bayesian models; no budget or numeric table checked. Do not borrow W0386’s implementation as this paper’s mechanism. |

### W0387 — Masked segmental LM [A]

[2022.sigmorphon-1.5 abstract](https://aclanthology.org/2022.sigmorphon-1.5/); exact digital encoding unknown.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-011 / context permission | Recurrent segmental models limit scalable use of contextual evidence for segmentation. | Replace recurrent segment modeling with a span-masked Transformer that uses bidirectional context. | Masking and attention enable unsupervised/lightly supervised segmentation from a language-model objective. | Abstract: Chinese segmentation better, English similar to recurrent SLM; no scaling throughput or table inspected. Bidirectional masking solves a different task than prefix-causal generation; inferred units are not automatically useful compression boundaries. |

## 2. Encoder compression, differentiable assignment and local order

### W0022 — Funnel-Transformer [A]

[2006.03236v1 abstract](https://arxiv.org/abs/2006.03236v1); WordPiece scope also explicit in CANINE §3.1 footnote.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-012 / length-depth allocation | Maintaining full subword resolution in every layer wastes computation on sequence-level tasks. | Progressively shorten hidden sequences and reinvest savings in depth/width, restoring positions when token prediction is needed. | Hierarchical encoder compression plus decoder reconstruction of per-token **representations**; pretraining and task losses train the network. | Abstract reports comparable/fewer FLOPs and stronger sequence tasks; exact pooling and budgets uninspected. Restoring hidden resolution is not proving original text reconstruction, and this is not learned byte segmentation. |

### W0004 — CANINE [P]

Contract: Unicode codepoints, **not bytes**; bidirectional compressed encoder and task-specific restoration. [v4 §§3.1–3.2/table1](https://arxiv.org/html/2103.06874v4).

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-013 / efficient character context | Direct codepoint Transformer stacks have too many positions for practical deep contextualization. | Contextualize locally, downsample by strided convolution, run the deep stack on short states, then restore character positions for tasks that need them. | Multiple hash embeddings cover Unicode; local128-character attention composes features; stride4 convolution shortens; repeated coarse features concatenate with early features before convolution/final attention. | §3.1:2048codepoints→512states; table1 mBERT179M versus CANINE-S127M, speed9000 versus6400examples/s. Parameter savings do not imply faster than mBERT. Authors explicitly avoid a direct residual h_init→h_up; concatenation is not interchangeable with residual addition. |
| S02-014 / supervision-unit separation | Character input alone gives weak pretraining, but fixed tokenization need not remain a deployed interface. | Use either shuffled autoregressive masked-character prediction or subword prediction during pretraining, then discard that auxiliary prediction interface. | CANINE-C predicts bucketed codepoint targets; CANINE-S uses masked subwords as a soft prior; targeted upsampling computes only queried masked-position outputs. | §3.2/table1: CANINE-C+n-grams57.0 MinSpan versus mBERT51.3, whereas CANINE-S52.5; do not collapse +5.7 and +1.2 or the abstract’s other metric. Whitespace masking still adds a prior; shuffled masked autoregression does not make the encoder a left-to-right generator. |

### W0005 — Charformer [P, v2 mechanism / v3 identity]

Contract:256-byte input/output, encoder GBST, span denoising. [v2 §2.1–2.2](https://arxiv.org/html/2106.12672v2); not an inspected v3 mechanism.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-015 / soft block composition | Fixed subword lexicons cannot adapt segmentation to task gradients. | Score candidate local blocks of several lengths and softly mix them at each byte position before fixed-rate downsampling. | Mean-pooled candidate blocks; learned linear block scoring; softmax mixture; final stride mean pooling; span-denoising gradients train scores. | §2.1 equations1–5. Learned block preference is **not a hard variable-length partition**: final compression rate is fixed. §3.1 uses1Msteps/batch64/1024bytes and matched-size byte baselines; not all tall-model comparisons have equal architecture or parameters. |
| S02-016 / order and alignment | Plain means lose within-block order and strided enumeration misses offset substrings. | Precede block averaging with convolution, with explicit offset enumeration as a costlier alternative. | 1-D convolution contextualizes neighboring positions and supplies order-sensitive information; optional self-attention-like calibration couples block scores. | §2.1.1/2.1.4, not a causal mask guarantee. Discontinuous morphology remains a stated limitation. Parameter/FLOP changes from calibration and convolution must be counted; decoder causality later challenged directly by N05. |

### W0006 — MANTa [P]

Contract: bytes→soft blocks→byte/sentinel span decoder; [2212.07284v1 §§3.1–3.2,6.1–6.4,Limitations](https://arxiv.org/html/2212.07284v1).

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-017 / differentiable partition | Hard frontiers obstruct task-gradient learning of explicit variable blocks. | Predict frontier probabilities and convert cumulative boundary counts into soft byte-to-block memberships. | Sliding-window Transformer predicts Bernoulli frontiers; Gaussian approximation to Poisson-binomial cumulative count gives differentiable membership; denoising CE trains tokenizer and LM together. | §3.1.1–3.1.2. Approximate soft assignment is not unbiased discrete optimization or a streaming guarantee. Only English small/base50–200M models tested; large-scale and multilingual benefits are not established by the paper’s suggestions. |
| S02-018 / local order | An unordered weighted byte pool could give the same result for different byte orders. | Apply depthwise convolution to membership-weighted embeddings before per-block max pooling. | Depthwise1-D CNN preserves local order; max pooling selects features; linear projection maps to the LM’s input width. | §3.1.3; §6.4 says tested kernel variations showed no significant pretraining difference. Distinguish learned boundary probabilities from the independently parameterized aggregator; no claim that every order is injectively preserved. |
| S02-019 / rate collapse | Optimizing denoising alone often learns one block per byte rather than useful compression. | Truncate the block sequence to at most one quarter of the input length so fitting all input information incentivizes longer blocks. | Hard length bottleneck supplies pressure in addition to task gradients; separate smaller tokenizer learning rate stabilizes training. | §6.1 explicitly calls truncation essential and reports degeneration without it. §5: training faster than dense byte baselines, still2.3× slower than T5; ByT5 comparison is time-matched with different steps. Byte-by-byte output remains a generation bottleneck, so encoder compression does not solve decoding cost. |

### S02-N02 — Hourglass [P]

Contract: fixed-rate causal hierarchy, enwik8 characters/symbols; [2110.13711v2 §§2.1–2.3/algorithm1](https://arxiv.org/html/2110.13711v2).

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-020 / causal pooling | A coarse vector reused for several predictions can leak later fine positions even when the coarse Transformer is causally masked. | Shift fine activations an additional k−1 positions before shortening by k. | Explicit alignment shift makes pooled inputs precede every fine target they condition; average/linear/attention shortening are separate choices. | Algorithm1 and §2.2; appendix proof not read. A coarse causal attention mask alone is insufficient. Efficiency experiments exist but not newly table-read; no numerical speed claim here. |
| S02-021 / within-block dependence | A model with only coarse states can accidentally make current-block targets conditionally independent. | Keep fine-resolution Transformer layers and restore coarse outputs through upsampling plus a fine path. | U-Net-style residual structure retains local autoregressive information; linear/attention upsampling differentiates fine output positions. | §2.2 derives reduced expressivity without vanilla layers; §2.3 compares restoration designs conceptually. This is a modeling-factorization issue, not merely an accuracy problem with bad boundaries. Whole experiment/appendix evidence missing. |

### S02-N03 — Vocabulary-free neural tokenizer [A]

Contract: character-based task tokenizer, not verified byte generation; [2204.10815v1 abstract](https://arxiv.org/abs/2204.10815).

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-022 / teacher-derived segmentation | Frequency-derived multilingual subwords underrepresent low-resource word diversity and cannot adapt to tasks. | Pretrain a character tokenizer by distilling heuristic segmentation over unique multilingual words, then allow task learning. | Segmentation distillation supplies boundary prior; unique-word sampling expands lexical diversity; downstream task supervision adapts the tokenizer. | Abstract reports NLI/code-switching/noise gains; architecture, discrete/soft gradient estimator, fine-tuning scope and teacher costs unknown. MANTa’s Related Work calls it imitation, but its own abstract claims end-to-end task learning; full read must reconcile, not repeat the narrower secondary description. |

## 3. Causal dynamic pooling: signal, aggregation and rate are separate

### W0007 — Dynamic Token Pooling [R]

Contract: **character** causal LM with completed-segment delay; source `03_reading/B05/W0007.md`, actual original reading2211.09761v2 §§3–5, tables1–2/figure3.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-023 / boundary supervision | Fixed-stride character pooling ignores the variability of useful local units. | Predict boundaries from external unigram segmentation or local peaks of the model’s own conditional entropy. | Causal MLP imitates offline SentencePiece-Unigram labels, or own-model entropy peaks generate labels; binary CE trains boundaries. | text8 Unigram1.134BPC/5×, entropy1.138/4.1×, fixed4×1.166; roughly41M parameters. Rates differ, so not a boundary-only matched-rate result. Offline labels can inspect more text than the online policy; entropy is not observed-target surprisal and is not BLT’s separate teacher. |
| S02-024 / task-driven boundaries | External boundaries may not minimize the main prediction loss. | Jointly sample hard Gumbel-sigmoid boundaries and transmit an approximate LM gradient through soft assignments. | Hard stochastic relaxation supplies biased gradients; a binomial boundary-count prior discourages every character becoming a separate segment. | §§3.3/4: text8 Gumbel1.136BPC/4.6×, with instability acknowledged. Training/evaluation sampling path needs code clarification. Average-rate control is not exact per-example quota; training-speed measurement is not full online generation latency. |
| S02-025 / aggregation versus boundary | A chosen boundary does not specify how much within-span content reaches the deep model. | Mean-pool completed spans, repeat deep outputs back to fine positions, and add the early fine path. | Contiguous pooling aggregates states; delayed availability preserves causality; high-resolution residual supports each next-character prediction. | Table2 mean pooling beats last-state sampling for tested boundaries. Contrasts with H-Net’s contextual-state selection; not proof mean aggregation is universally superior. Only completed spans are available; cannot use the current unfinished span’s future bytes. |

### W0008 — MEGABYTE [P]

Contract: raw bytes and fixed patches; [2305.07185v2 §§2.1–2.2](https://arxiv.org/html/2305.07185v2).

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-026 / fixed grouping control | Large feedforward and attention layers at every byte make very long sequences expensive. | Concatenate fixed patch byte embeddings and run the large global network per patch with a small local byte decoder. | Reshaping/concatenation builds order-sensitive patch inputs; global/local causal Transformers divide long-range and within-patch modeling; next-byte CE trains both. | §2 gives architecture, not a learned boundary. Patch-embedder concatenation described as lossless does not make all downstream states invertible. Abstract’s million-byte/multimodal evidence is not a million-byte language-quality guarantee; full compute tables not read. |
| S02-027 / two-level causal alignment | A patch representation contains bytes that its own local decoder must not see in advance. | Shift global inputs by one patch and local inputs by one byte, then condition current local predictions only on previous patches and their own prefix. | Two distinct padding/offset operations enforce causal factorization; separate local positional components retain current-patch dependence. | Equations2–4 and Figure2 description inspected. Training parallelization across observed patches is not unrestricted simultaneous sampling of unknown future patches; generation algorithm and speed experiments still need full read. |

### W0009 — SpaceByte [R]

Contract: raw bytes, fixed observed-byte rule; `03_reading/B05/W0009.md`, v3 §2/AppendixC, table1.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-028 / fixed-rule control | Fixed intervals waste global updates at unhelpful positions, but learning or a teacher adds overhead. | Invoke the global model after selected spacelike bytes and let a local causal path handle the remaining bytes. | Deterministic byte-class rule allocates computation; selected contextual states enter the global Transformer, not an arithmetic mean over completed words. | At10^19 trainingFLOPs: PG19 SpaceByte1.009 versus fixedP1.112 and SentencePiece0.989BPB; arXiv/GitHub favor SpaceByte over that subword baseline. Different frontier points/rates and model sizes remain. UTF-8 lead bytes can trigger before a whole character is complete; continuation bytes do not. Chinese preliminary weakness and variable-batch cost remain. |

### W0010 — BLT [R]

Contract: bytes/hashed n-grams, separate entropy teacher, formal ACL2025; `03_reading/B05/W0010.md`, §§2–5,7,AppendixH/P.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-029 / teacher entropy | A constant patch size cannot adjust compute to the local unpredictability of a byte stream. | Use a separately trained causal byte LM’s next-byte entropy to choose patch starts. | Default100M entropy teacher; global entropy threshold or entropy-difference rule sets rate; preprocessing for training and online scoring for generation. | Separate teacher deliberately not jointly trained (§10); thresholds tuned, including downstream changes. Not end-to-end learning of boundaries from main-LM loss. FLOP formula does not separately include default teacher pretraining/per-byte inference; no free-teacher assumption. |
| S02-030 / adaptive aggregation | Compressing byte spans needs more expressive content aggregation than a fixed uncontextualized mean. | Build patch latents by cross-attending from pooled queries to contextual byte states and decode through a local path plus global cross-attention. | Local causal encoder, hashed3–8gram byte embeddings, patch cross-attention, global Transformer and local byte decoder each have distinct roles. | §7 tables4–5 show cross-attention and n-grams matter. Local windows may cross patches; masks/offsets prevent future access. Boundary and aggregator gains cannot be merged into a single “entropy works” result; exact raw-byte preservation not established. |
| S02-031 / budget confounding | Reported superiority of one boundary family can reflect different text exposure or architecture. | Compare patch rules while recording actual average patch length, training bytes, architecture and teacher costs separately. | Author experiments include space/fixed/entropy variants and compute-constrained scaling; this row inventories the **comparison design**, not a new algorithm. | §5.2:8Bspace sees~6Tbytes, entropy~4.5Tbytes, Llama3~4Tbytes under equal trainingFLOPs; AppendixP space version lacked cross-attention. Evidence supports a model-system frontier, not clean identification of boundary signal alone. |

### W0011 — H-Net [R]

Contract: causal bytes, learned contextual-state selection; `03_reading/B05/W0011.md`, §§2.1–2.4/3.3,AppendixE.1.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-032 / learned state routing | Fixed rules and separately pretrained patchers need not align with the main model’s objective. | Learn a cosine-based boundary score over adjacent contextual states and send selected states to a slower backbone. | Query/key projections and thresholded cosine change route already-contextualized states; straight-through approximation supplies boundary gradients; LM trains the full system. | XL near-matchedGFLOPs/byte: BPE0.69/55.5%avg; space0.70/57.1%; one-stage0.72/56.2%; two-stage0.69/58.2%. One-stage is not uniformly stronger than space. Same corpus/approximate FLOPs, not identical parameter count. |
| S02-033 / rate stability | Discrete routing and repeated expansion can destabilize compression and learning. | Smooth selected outputs with a probability-weighted EMA and add a target-rate loss. | EMA exposes continuous gradients; actual hard-selection fraction and mean boundary probability enter a load-balancing-style ratio term; residual fine path helps decoding. | Figure7 removing smoothing destabilizes rate and quality; ratio loss is not an exact constraint and can fall below its nominal reference when F≠G. Current implementation can train~2× slower than isotropic models and may OOM in variable batches; theoretical FLOPs do not certify speed. |
| S02-034 / aggregation sufficiency | It is unclear whether a learned boundary must explicitly pool every state inside its span. | Let the encoder concentrate useful history in the boundary state and compare direct selection with mean/max/cross-attention aggregation. | Contextual encoder performs implicit aggregation before hard selection; AppendixE.1 varies the explicit aggregation operator at fixed dynamic boundaries. | Authors report direct selection roughly comparable in this setting, unlike DTP’s last-state disadvantage. No contradiction: encoder, routing gradients and tasks differ. Neither experiment proves boundary and aggregator are universally interchangeable or lossless. |

### W0012 — SOMBRERO [R]

Contract: causal bytes, current-model next-byte targets; `03_reading/B24/W0012.md`, §§3–4/table1/table2.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-035 / explicit boundary target | Implicit task gradients may not provide a clear target for which positions deserve a new global update. | Regress boundary probability toward one minus the current model’s probability of the observed next byte, with stop-gradient through that target. | Confidence-aware boundary loss, sigmoid routing, byte-level smoothing, LM loss and ratio regulation supply separate learning signals. | Matched~5×target/1.95GFLOPs per byte/50ksteps/839Bbytes: H-Net0.6701→smoothing0.6571; sigmoid0.6578; +CAB0.6568BPB. Most gain in this ladder is not CAB alone. Training targets use next byte; deployed policy still prefix-only. |
| S02-036 / proxy counterexample | More boundaries at surprising positions may look desirable without improving model utility. | Measure boundary enrichment against shifted-boundary nulls and compare it with actual LM/downstream performance. | Surprise-enrichment diagnostic quantifies alignment; cyclic shifts preserve boundary pattern/rate. It is an author diagnostic, not intervention proof. | Larger model H-Net0.6126 versus Sombrero0.6128BPB, enrichment1.998 versus3.133; downstream average0.473 versus0.463. More enrichment does not imply lower BPB or better tasks. Table/prose numeric tension and colored random-retrieval examples need original-page recheck. |

## 4. Reconstruction, deletion, fusion and merge controls

### W0013 — GQ-VAE [R]

Contract: short character/byte sequences, exact encoding unresolved; offline full-input tokenizer; `03_reading/B24/W0013.md`, §§II–III/figures3–6.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-037 / reconstruction grouping | Fixed-length quantized codes cannot flexibly allocate a code to variable text spans. | Jointly learn quantized codes, retention gates, decoded character windows and output lengths. | VQ codebook and straight-through quantization provide discrete content; gate-rate penalty encourages compression; character reconstruction, length and commitment losses shape the tokenizer. | TinyStories pre-split by regex into≤16characters, max decode10;18M downstream LM. Equal vocabulary and equal compression experiments differ; code quality is not a causal byte-LM boundary result or a long-context language-system result. |
| S02-038 / exactness and fallback | A learned reconstruction tokenizer can make irreversible spelling errors. | Check decoded chunks against the original during encoding and fall back to character units when reconstruction mismatches. | Reconstruction verification/fallback supplies exact text encoding; staged dictionary construction then downstream code LM is explicit. | Figure3 reports<7%compression loss after fallback relative to BPE; equal3.85bytes/token comparison changes BPE vocabulary to3250. No matched total tokenizer+LM FLOPs, deployment latency or multilingual evidence; this is encode-time original access, not proof all latent values are inherently invertible. |

### W0511 — MrT5 [R]

Contract: bidirectional source byte encoder, byte decoder; `03_reading/B22/W0511.md`, §3/equations1–7/§§5–6/A–J.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-039 / deletion optimization | A pretrained byte encoder processes many redundant positions, but hard deletion cannot be trained directly. | Learn a soft deletion mask after encoder layer3, then hard-delete states for later inference. | Denoising CE plus deletion regularization; proportional-integral controller targets deletion fraction; softmax1 avoids mask-translation invariance, with extra attention-score regularization. | Soft-training/hard-inference transition matters; surviving states may already contain deleted-byte information. Not literal contiguous-span averaging, and not a causal next-byte route because source context is bidirectional and can include the question. |
| S02-040 / task-versus-runtime | Better compression than random deletion might still lose task quality or leave long outputs expensive. | Evaluate deletion against no deletion, random/fixed rules and pooling at similar shortening, while measuring encoder and decoder costs separately. | Author baseline design distinguishes learned deletion from boundary pooling; operation-count model separates encoder, autoregressive decoder and cross-attention. | Target50%:44.29→29.99ms single sequence; TyDiQA69.90/79.58→68.27/77.73EM/F1 with33.31%runtime reduction. Deletion beats matched deletion controls but not no-deletion denoising quality; long outputs amortize away source savings. ByT5 prior training not free. |

### W0514 — Local Byte Fusion [R]

Contract: full source bytes, Moses preprocessing, causal target byte generation; `03_reading/B26/W0514.md`, §3/§4.3/AppendixB.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-041 / fusion without shortening | Dense byte representations may fail to expose useful short-range lexical patterns to higher translation layers. | Fuse local1–4byte features with convolutions and weighted expansion while retaining the original sequence length. | nCF uses shallow contextualization and multiscale convolutions; translation CE learns combination weights. This is a **local representation mechanism**, not persistent sequence compression. | Table3 Lao→EN BPE9.2, densebyte5.9,nCF6.4BLEU: fusion helps its byte baseline but not BPE. AppendixB training and inference rankings differ; do not equate byte feature fusion with speedup. |
| S02-042 / structural prior | Generic local byte windows may mix across word boundaries unhelpfully. | Constrain byte attention to externally specified word spans. | WSF uses block attention masks derived from word spans; translation CE trains representations within the supplied structure. | §4.3 all variants Moses-pretokenized, source/target>800bytes filtered; lack of whitespace may require additional segmentation. The paper does not prove universal tokenizer independence. Exact benefit over nCF varies, and zero-shot subword-vocabulary disadvantage is a separate baseline confound. |

### W0023 — Compressive Transformer [R]

Contract: old recurrent hidden memories, character or subword LM by task; `03_reading/B24/W0023.md`, §§3.1–3.2,5.2/tables5,8,9. Adjacent objective evidence, not a new input tokenizer.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-043 / consumer-aligned compression | Reconstructing every old hidden feature may preserve information irrelevant to the future attention reader. | Train a compressor to reconstruct attention responses to old memory rather than the entire old hidden state. | Convolution/pooling compresses FIFO-evicted states; auxiliary attention-response reconstruction stops gradients through main states/attention and trains the compressor. | Table5 convolution+attention0.973 versus convolution+AE0.984BPC; each row selects best c=2/3/4, so not strict equal-rate evidence. BPTT comparator changes unroll/batch. Task-aligned response is neither exact text reconstruction nor a guarantee for arbitrary future queries. |
| S02-044 / capacity counterexample | More compressed-memory slots can be assumed to monotonically improve usable history. | Report performance while varying memory allocation rather than treating stored-state count as utility. | Dual FIFO memory and attention to recent fine/old coarse states are used; memory-size sweep tests allocation. | AppendixB: enwik8 compressed slots3072→4096 worsens0.97→1.00; WikiText1536→2048 worsens17.1→17.7PPL. Different evaluation allocation does not identify why; no claim of a universal optimal memory size. End-to-end compressor maintenance/latency absent. |

### W0024 — Token Merging (ToMe) [R]

Contract: **vision/audio patch tokens, not language bytes**; `03_reading/B24/W0024.md`, v3 §3/§4.1/AppendixD–E.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-045 / similarity merge | Pruning tokens discards potentially useful content and dynamic token counts complicate batching. | Merge a fixed number of feature-similar token pairs per layer using bipartite soft matching. | Key-feature cosine similarity chooses matches; fixed r controls token count; gather/scatter operations implement aggregation, optionally with fine-tuning. | MAE ViT-L,r8:matching84.25%/182.9images/s versus random pruning79.22%/184.4; original85.96%/93.3 onV100fp32/optimizedbatch. Noncontiguous, noncausal visual matching cannot be imported as a language causal segmentation result. |
| S02-046 / aggregate mass | Repeated means and attention can misweight groups representing different numbers of original patches. | Weight merged values by accumulated patch count and adjust attention with log group size. | Size-weighted aggregation conserves represented mass; proportional attention compensates multiplicity; merge ancestry supports visualization. | §4.1 weighted84.25 versus unweighted83.57%; AppendixE tracks original membership for displays. Ancestry is not recovery of original values; there is no demonstrated exact inversion or text-order preservation. |

## 5. When entropy, novelty and computational utility disagree

### W0357 — Boundary dependence [R]

Contract: causal BLT-style byte patches, offline future-target scoring; `03_reading/B05/W0357.md`, §§3–10/tables1–6.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-047 / compute value | A small patcher can assign low uncertainty to positions where a larger model still needs fresh computation. | Fit a past-byte lookup table to losses under alternative boundary layouts, then combine utility-derived and entropy boundaries. | Offline layout-difference proxy or single-added-boundary scoring supplies utility labels; context table amortizes decisions into prefix-only lookup. | BLT1B true-prefix computed-value accuracy at~10%rate:entropy19.0%, entropy+dependence67.1%; dependence alone67.8% but finalanswers4.8% versus entropy51.4%. Large-model labels are **whole-layout differences**, not single-action causal effects. End-to-end GSM8K~2% or less; offline scoring/teacher cost not fully charged. |

### W0358 — Novelty patching [R]

Contract: future text labels during training, only prior two bytes during deployment; `03_reading/B14/W0358.md`, §§3–6/tables1–5.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-048 / repetition prior | Entropy peaks can miss newly computed results whose local format is predictable. | Start patches where a learned lookup table predicts that upcoming text is unlikely to repeat recent context. | LZ77-inspired longest-repeat statistic within128bytes, capped16, supplies labels; empirical averages by prior-two-byte context form the rule with rare-context backoff. | At~11%rate/50M/three seeds, computed values57.5 versus20.7%; finalanswers89.5 versus59.9%. Teacher-free does not mean supervision-free: offline target uses future training text. True-prefix completion, not unrestricted solution generation; same author/pipeline as W0357. |
| S02-049 / proxy and transfer failures | A boundary rule’s success on one target can conceal worse overall likelihood and sensitivity to train/inference mismatch. | Evaluate novelty on overall BPB and other domains and test swapping boundary rules after training. | Authors compare novelty/entropy/H-Net and context-aware predictors; post-training rule swaps test coadaptation. | Math50M overallBPB1.446 versus entropy1.416; code1.684 versus1.649; novelty-trained12M finalanswer73.6%→0–0.5% under swapped rule. A richer128byte predictor can cover more results and perform worse. Neither novelty nor entropy is a universal computation-value oracle. |

### S02-R01 — Scratchpad Patching [A]

Contract: causal bytes, persistent patches versus transient partial-patch states; [2605.09630v1 abstract](https://arxiv.org/abs/2605.09630v1). Reused recovery candidate, not new discovery.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-050 / state freshness | Larger completed patches leave predictions inside the current patch conditioned on a stale global representation. | Insert temporary summaries of already seen within-patch bytes to refresh context without increasing persistent patch-cache count. | Transient scratchpad aggregation and entropy-based triggers decouple computation frequency from persistent patch size; next-byte modeling remains the task. | Abstract reports16bytepatches with16×smaller patchKV and3–4×less inference compute near byte baseline; exact baseline/cache accounting, transient cost, matchedFLOPs and wall-clock uninspected. Crucial competing explanation to “boundary placement alone causes compression quality”; full method read needed. |

### S02-R02 — Autoregressive U-Nets [A]

Contract: bytes→word/word-pair/up-to-four-word hierarchy; [2506.14761v1 abstract](https://arxiv.org/abs/2506.14761v1); reused recovery candidate.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-051 / prediction horizon | A fixed token interface fixes both input granularity and how far each predictive step reaches. | Build a byte-to-word hierarchy and assign deeper stages predictions further into the future. | Autoregressive U-Net, learned embeddings and multiscale prediction objectives allocate fine/local and coarse/longer-horizon work. | Abstract says carefully compute-tuned shallow hierarchies tie BPE and deeper ones trend favorably; word-boundary source, objectives, shifts, joint factorization and actual budget not read. Do not call all grouping learned because embeddings are learned, or call word hierarchy semantic evidence without method. |

### S02-N04 — Reinforcement-learned tokenization [P]

Contract: causal UTF-8 bytes, sampled boundary-state selection and distribute/add fine path; [2602.13940v4 §§2.2–2.7](https://arxiv.org/html/2602.13940v4), selected §4 and AppendixD snippets inspected by targeted search, not complete experiments.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-052 / discrete policy gradient | Straight-through boundary gradients optimize a surrogate rather than the expected loss of actual discrete choices. | Sample boundary actions and optimize their expected prediction loss with a score-function gradient alongside ordinary LM backpropagation. | REINFORCE/stochastic-computation-graph derivation supplies a discrete policy gradient; selected byte states and simple repeat/add upsampling avoid requiring a special differentiable aggregator. | §2.3 concerns expected log likelihood/lower bound, not an unconditional global optimum. §4 snippets:~147Mmodels,4096bytes, target1/5; comparisons with fixed intervals, two straight-through methods and BPE-guided layout. Full tables, stochastic policy evaluation and convergence proof not read. |
| S02-053 / credit and variance | A one-sample policy gradient over long byte streams is too noisy to train usefully. | Subtract an early-exit prediction baseline and discount later rewards before assigning credit to boundary actions. | Auxiliary early-byte prediction estimates action-independent difficulty; time discounting reduces variance **while adding bias**; batch-mean-logit rate pressure limits all-byte boundaries. | §§2.4–2.6, γ0.99 in inspected snippet; desideratum<0.1%extra pretraining compute is not verified realized wall-clock. §4.2 says task accuracy near chance/noisy, so reports continuationBPB instead; not demonstrated broad reasoning accuracy. BPE-guidance leakage fix in AppendixD.1 is an author claim needing a prefix-invariance audit. |

## 6. Direct causal counterexamples and structural preservation

### S02-N05 — Patching Leaks in Charformer [P]

Contract: title says character, **AppendixB.2 says UTF-8 bytes**; causal translation decoder with full source; [2205.14086v1 §§2–4,AppendixA/B](https://arxiv.org/html/2205.14086v1).

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-054 / leakage diagnostic | Putting encoder GBST in a causally masked decoder can still expose future bytes. | Test next-symbol prediction on independent random sequences after the downsampling/upsampling path and identify above-chance positions. | Random-target diagnostic isolates information leakage; convolution and cross-block n-gram averages are explicit leak sources. | §2.1 uses100symbol vocabulary/chance1%, and reports worst-case75%positions leaked; table cells not independently recovered. This is stronger than trusting a downstream causal attention mask. Does not impugn GBST’s intended bidirectional encoder use. |
| S02-055 / failed causal repair | Preventing future access by larger padding can make the remaining prediction horizon too difficult. | Compare extra padding, removing overlapping n-grams and causal n-gram masks instead of assuming all leak-free fixes are equally useful. | Sinusoidal positional embeddings remove convolutional lookahead; restricted n-grams or block-aware masks remove averaging lookahead; local LSTM head restores fine next-byte predictions. | §§2/4:two-block padding fails to learn translation; removing leaking n-grams beats masking, but convolutional Lee-style downsampling wins quality and GBST wins some speed. UTF-8; V10032GB; source filter≤256Englishcharacters. Leakage-free does not imply quality-equivalent, and exact numerical MT tables are missing from extraction. |

### S02-N06 — Subword-Delimited Downsampling [A]

Contract: [formal2022.findings-emnlp.69 abstract](https://aclanthology.org/2022.findings-emnlp.69/), [2212.01304v1](https://arxiv.org/abs/2212.01304v1). Exact byte/character implementation still to inspect in this paper rather than borrowing N05’s encoding.

| Record / cluster | Specific prior problem | One-sentence solution | Explicit technique and role; signal | Evidence, comparator/budget and remaining limits |
|---|---|---|---|---|
| S02-056 / local structure preservation | Naive character downsampling sacrifices translation quality even when it saves computation. | Inform downsampling with subword-delimited structure rather than treating every fixed local group as equally suitable. | External subword segmentation supplies a grouping prior; neural downsampling and translation learning operate on retained character detail. Exact aggregation/length normalization mechanisms unknown at abstract depth. | Abstract reports superiority to existing downsampling and promising subword comparisons; no matched training budget, whole-source length, numerical table or decoder factorization read. Distinct later work from N05, not a rewrite that retroactively invalidates its earlier negative controls. |

## 7. Cross-record classification dimensions for the next owner

These are analyst classification axes, not additional evidence records:

1. **What changes?** Boundary positions (DTP/H-Net), content aggregation (MANTa/BLT), hidden-sequence length (Funnel/MrT5), update frequency (SpaceByte/HM-RNN), persistent state count versus temporary refresh (Scratchpad), or output horizon (AU-Net). A method can have multiple labels.
2. **Where does the signal come from?** Corpus compression statistics/MDL; external subword segmentation; current-model entropy; separate teacher entropy; observed-target probability/confidence; boundary-layout utility; repetition/novelty targets; pure task gradient; reconstruction/codebook losses; or policy-gradient task returns. Entropy, surprisal, confidence error and utility are distinct quantities.
3. **What is the representation?** Uncontextualized concatenation, mean/max/CNN pool, attention latent, contextual boundary-state selection, deletion of contextual positions, or quantized code. “Boundary chosen” does not identify which representation was built.
4. **What can see future context?** Full-source bidirectional encoder, offline labels, full-sentence posterior segmentation, current-prefix policy, completed-span value, or original text at encode-time verification. Training-label lookahead is not deployment lookahead, but a deployment layout computed offline from the full test string can leak.
5. **What was controlled?** Same corpus, same actual text, same parameters, same average compression, same segment-length distribution, same training FLOPs, same inference FLOPs, same teacher budget, or same end-to-end latency. None entails all the others.

The field supports multiple successful contracts. It does **not** currently support a common causal verdict that semantic-looking boundaries, entropy enrichment, exact character reconstruction or more stored states necessarily dominate alternatives at matched complete budgets.
