# Below the token: a survey of byte-language interfaces, computation, learning, and evaluation

## Abstract

Language models connect written text to computation through several interfaces, not one tokenization decision. Bytes, Unicode code points, restricted character alphabets, merged subwords, and word-local spelling representations provide different coverage and sequence lengths. Their internal processing units, output events, and supervision can differ again. This survey traces the resulting field from recurrent character models and character-composed word representations through byte encoders, sequence-to-sequence denoisers, full-resolution causal models, learned grouping, structured multi-byte prediction, and pretrained interface conversion. Its central argument is that a small alphabet redistributes rather than eliminates work: lexical storage becomes local composition, longer contextual sequences, additional output decisions, boundary estimation, or transfer training. The literature supplies multiple alternatives to sequence shortening, including selective recurrence, sparse connectivity, segment-state reuse, reversible activation reconstruction, fixed latent workspaces, and adaptive computation within a byte. We compare the learning signals and information paths of grouping methods, distinguish local autoregressive joints from parallel marginals and dependent circuit drafts, and examine when decoding preserves a named target. Weight sharing, readout geometry, auxiliary objectives, and distillation are analyzed on their actual parameter and probability axes. Multilingual coverage, position parity, robustness, character competence, Unicode validity, exact copying, and task quality are treated as separate outcomes. Detailed counterexamples show why compression, parameter economy, acceptance, and local likelihood cannot substitute for matched-resource or matched-quality evidence. The result is a problem–solution–technique account of a diverse field, not a universal ranking of bytes against subwords.

## Contents

1. [Scope, evidence, and the organizing questions](#s01)
2. [Text units and the four interfaces](#s02)
3. [Historical routes below the word](#s03)
4. [Local composition, encoders, and conditional generation](#s04)
5. [Full-resolution computation and alternatives to segmentation](#s05)
6. [Learning groups: content, boundaries, and rate](#s06)
7. [Causal availability and state freshness](#s07)
8. [Output dependence and multi-byte generation](#s08)
9. [Probability interfaces and comparable likelihoods](#s09)
10. [Sharing, readout geometry, and optimization](#s10)
11. [Objectives, hybrids, and pretrained conversion](#s11)
12. [Multilingual allocation, robustness, and competence](#s12)
13. [Compute, data exposure, and serving](#s13)
14. [A consolidated problem–solution–technique taxonomy](#s14)
15. [Evaluation design and the research frontier](#s15)
16. [Conclusion](#s16)
17. [Appendix A: methodology, evidence depth, and reference navigation](#appendix-a)
18. [Appendix B: translation and terminology contract](#appendix-b)

<a id="s01"></a>
## 1. Scope, evidence, and the organizing questions

### 1.1 What is a byte-language interface?

A language interface specifies how written material enters a learned system, how its positions or states are organized, what the system predicts, and what teaches it. A byte interface changes at least one of those connections to use byte-valued symbols or byte-indexed events. It need not change all of them. A multilingual annotator can read UTF-8 and emit span labels; a word encoder can compose bytes but retain a word clock; a causal model can predict every byte while doing expensive computation only at selected positions; a distillation method can use bytes only as a temporary comparison space between incompatible vocabularies. Each is relevant, but none should stand in for the others.

The field is consequently larger than a contest between fixed tokenizers and learned tokenizers. Early character models addressed sparse lexical statistics and recurrent optimization. Character-to-word composers shared spelling features without removing words. Byte-complete subwords addressed coverage while preserving compressed sequence positions. Encoders and denoisers made fine-resolution pretraining practical under full-source visibility. Causal hierarchies addressed the frequency of expensive updates, while parallel output methods addressed the number of those updates needed during generation. Adaptation methods asked whether knowledge could survive a change of interface. Evaluation work exposed differences between admitting a string, knowing it, manipulating it, scoring it, and producing it correctly.

This survey is independent of any local model project. It does not use a preferred multigranularity architecture, source-revisiting mechanism, or proposed experiment as its inclusion rule. Its main questions are: **what is represented; what is composed or retained; where computation occurs; what information is available; how learning is stabilized; what output law is defined; and what evidence establishes utility at a stated cost?** These questions connect the field without assuming a common destination.

### 1.2 Documentary scope and interpretation

The supporting corpus contains **141 independent source entities: 137 research documents—136 academic papers/preprints and one technical report—plus three standards and one official model introduction**. The academic set includes one screened proposal that contributes no achieved experiment. Its **296 traceable records** describe source-specific questions, mechanisms, controls, negative findings, sharing specifications, and review exceptions, not 296 independent scientific problems or successful experiments. **Ninety-two distinct sources have scoped FULL reading support: 62 new and 30 reused. Two additional historical sources have intentional narrow PARTIAL extractions.** FULL means substantive source reading in the recorded scope, not reproduction, proof certification, or verification of the executed software. The exact identity and support reconciliation is in [FINAL_AUTHOR_COUNTS](../02_inventory/FINAL_AUTHOR_COUNTS.md); methodological detail is confined to Appendix A.

The account is selective rather than exhaustive. It includes character antecedents, nonbyte decoding originals, general parameter-sharing theory, and adjacent compression methods where they explain an actual interface choice. These are labeled by role. Neither a standard nor an external probe becomes an additional native-byte language-model result. The evidence is sufficiently broad for a substantial field survey, but it does not define a single common-hardware, common-data quality frontier. Classical context-mixing and statistical compression history remains selective.

### 1.3 Three recurrent separations

Three separations organize the argument. First, **representation is not computation**. All-byte coverage can coexist with subword positions, word positions, fixed latent slots, or a byte-level recurrent state. Second, **computation is not the output law**. A patch-level trunk can feed an autoregressive local decoder, independent future classifiers, a normalized dependent draft, or an iterative denoiser. Third, **accessible information is not usable competence**. A spelling can be decoded from frozen embeddings without the host following a spelling instruction; a model can emit legal Unicode that is not the intended character; low local loss can coexist with poor long exact copy.

These distinctions are explanatory rather than merely cautionary. They identify why methods work in particular regimes. A gated word composer helps because it changes both parameter sharing and the optimization path. A coarse state helps if it preserves information the consumer needs. A circuit draft helps if its dependence raises useful acceptance enough to pay for head and sampling cost. A byte model helps a surface-sensitive task when training and inference actually exploit the newly exposed detail. The strongest comparisons therefore join a mechanism with its control and its applicable budget, rather than awarding a vote to an alphabet.

<a id="s02"></a>
## 2. Text units and the four interfaces

### 2.1 Byte, scalar, grapheme, and learned symbol

A byte is an eight-bit storage unit. UTF-8 encodes a Unicode scalar value in one to four bytes. A Unicode code point is an index in the Unicode code space; surrogate code points are not Unicode scalar values and cannot occur in legal UTF-8. A grapheme cluster approximates a user-perceived character and can contain several code points. A paper's “character” may instead denote a small restricted alphabet after lowercasing, transliteration, or unknown-symbol replacement. A subword is a variable-length vocabulary entry. Starting a vocabulary from bytes does not make its merged entries single bytes.

These distinctions change the task. A byte prefix can stop inside a scalar and still be extendable to valid UTF-8. A complete valid scalar can be the wrong scalar. A combining sequence can be canonically equivalent to a precomposed form without sharing its original bytes. A grapheme-level edit can correspond to several code-point or byte edits. The standards supply instruments, not learned-model results: [RFC 3629 §§3–4, BIW-0090](https://www.rfc-editor.org/rfc/rfc3629.html), [UAX #15 revision 57 §§1.1–1.2, BIW-0115](https://www.unicode.org/reports/tr15/tr15-57.html), and [UAX #29 revision 47 §§1–3, BIW-0116](https://www.unicode.org/reports/tr29/tr29-47.html).

Coverage also has several meanings. A byte-complete code can represent arbitrary byte strings, including malformed text. A scalar interface can represent valid Unicode text without accepting arbitrary binary input. A learned hash interface can map an unseen code point to a vector while admitting collisions. A normalizing tokenizer can cover its processed domain while failing exact original-string round trips. An open input composer can encode an unseen word even if its output classifier cannot generate that word. Each contract can be useful; the relevant comparison must state the domain it promises to preserve.

### 2.2 The four-unit description

For every substantial comparison, identify **input / internal positions or state / output / supervision**. “Internal” should name where expensive context processing occurs, not merely say hidden vectors. “Supervision” should include corruption selection, external boundaries, teacher distributions, and auxiliary labels as well as the final prediction alphabet.

The following abbreviations retain their ordinary technical meanings: language model (LM), convolutional neural network (CNN), long short-term memory network (LSTM), byte-pair encoding (BPE), masked language modeling (MLM), cross-entropy (CE), negative log-likelihood (NLL), bits per byte (BPB), and floating-point operations (FLOPs). A key/value (KV) cache stores past attention keys and values; autoregressive (AR) prediction conditions on previously observed or generated outputs. These abbreviations do not resolve a paper's actual alphabet, probability event, or resource convention.

**Table 1. Representative four-interface contracts.** This is a mechanism map, not a leaderboard.

| Family and representative | Input | Internal positions or state | Output events | Supervision and visibility |
|---|---|---|---|---|
| Character-aware word LM, BIW-0055 | Characters within supplied words | CNN/max/highway, then word-time LSTM | Fixed-vocabulary words | Next-word likelihood |
| Byte span annotator, BIW-0057 | UTF-8 windows | Recurrent read phase followed by annotation phase | Start, length, label, STOP | Supervised annotation after full-window reading |
| GPT-2, BIW-0141 | Merged byte-BPE pieces | Merged-piece Transformer positions | Next merged piece | Causal next-piece prediction; narrow historical extraction |
| CharacterBERT, BIW-0066 | UTF-8 bytes within supplied words | Local byte composition, word-position BERT | Frequent-word MLM classes or task labels | Masked words and next-sentence training |
| CANINE, BIW-0004 | Unicode code points | Local positions, stride-four states, restored positions | Bucket/subword pretraining labels or task outputs | Bidirectional masked source; C and S variants differ |
| ByT5, BIW-0024 | UTF-8 bytes and special symbols | Byte encoder and target decoder | Reconstructed bytes/sentinels or task text | Span denoising; full corrupted source and causal target |
| Perceiver IO, BIW-0117 | Bytes or subwords | Fixed latent compute array | Masked identities or queried task outputs | Whole-word-selected masking and full-source encoding |
| Plain byte Transformer, BIW-0071 | Processed-corpus bytes | One deep position per byte | Next byte | Causal likelihood |
| MEGABYTE, BIW-0008 | Bytes | Global fixed patches and local byte positions | Locally autoregressive bytes | Causal byte likelihood with two resolution shifts |
| H-Net, BIW-0011 | Bytes | Contextual selected states and hierarchical backbone | Bytes | Language loss, smoothing, and rate control |
| MYTE, BIW-0104 | Morphology-derived code bytes | Alternate-code encoder/decoder positions | Alternate-code task strings | External codebook and denoising/task labels |
| T-FREE, BIW-0127 | Rule-split units and trigram features | Whole-unit Transformer positions | Candidate-dictionary units | Multi-label feature prediction |

Carrying sources are [BIW-0055](../03_reading/R02/BIW-0055.md), [0057](../03_reading/R02/BIW-0057.md), [0141](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md), [0066](../03_reading/R01/BIW-0066.md), [0004](../03_reading/R01/BIW-0004.md), [ByT5/W0351](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md), [0117](../03_reading/R01/BIW-0117.md), [0071](../03_reading/R09/BIW-0071.md), [0008](../03_reading/R03/BIW-0008.md), [H-Net/W0011](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md), [0104](../03_reading/R07/BIW-0104.md), and [0127](../03_reading/R10/BIW-0127.md). Subsequent sections give their versioned method and experiment locations.

The table makes hybrids ordinary rather than exceptional. A model can be byte-only at deployment but use subword labels during training. It can be vocabulary-free on input but candidate-limited on output. It can have a byte alphabet and a word-based corruption process. “Pure byte” is therefore too ambiguous to carry a scientific conclusion without qualification. Useful descriptions name the relevant purity: native next-byte outputs, no external segmenter at inference, no lexical lookup, or no teacher during training.

### 2.3 The unit of context and the unit of cost

A context of 1,024 model symbols is not a context of 1,024 bytes, scalars, graphemes, or words. Under byte-BPE it can contain several times more original text than under direct bytes, and that ratio changes by language and domain. Internal compression adds another distance: two positions in the trunk can be far apart in bytes but close in grouped states. Positional encoding then expresses distances on that internal clock unless explicitly modified.

This has statistical and systems consequences. Longer original-text exposure can supply more training information, but a compressed representation can also lose detail. Fewer positions can reduce attention and cache work, but irregular routing can waste hardware. More byte decisions can increase serial output latency even with a small head. When comparing interfaces, context length should therefore be stated in original text and model positions, with the transformation between them measured rather than assumed.

<a id="s03"></a>
## 3. Historical routes below the word

### 3.1 Recurrent strings and the classical compression baseline

Early neural string models did not begin with a theory of learned tokenization. They replaced fixed-order context statistics with learned distributed state. Sutskever, Martens, and Hinton's *Generating Text with Recurrent Neural Networks* used factorized multiplicative transitions: the current symbol chooses a combination of shared low-rank transition components that transforms recurrent history. Hessian-free optimization, Gauss–Newton products, and structural damping addressed difficult recurrent gradients. The mechanism is a concrete architectural and optimization antecedent, not a boundary detector ([BIW-0052](../03_reading/R02/BIW-0052.md), official 2011 paper §§2–3, Eqs.3–9; [BIP-0081–0082](../02_inventory/DETAILED_INVENTORY.md#BIP-0081)).

The actual alphabet comprised 85 allowed characters plus an unknown symbol under corpus-specific transformations. Its bits per character are not probabilities of arbitrary original UTF-8. The comparison with classical methods also resists a simple neural-progress narrative. At roughly matched 100 MB training data, the multiplicative RNN beat the sequence memoizer but lost to dictionary-disabled PAQ on all three reported corpora. Wikipedia was 1.60 versus 1.51 bits per transformed character. Distributed recurrence was promising without having displaced a strong compressor under that protocol (source §5/Table 1).

This historical control matters because it identifies the real advance: a reusable trainable state with general representation-learning potential, not an immediate universal compression victory. It also reminds later surveys that a neural model's loss improvement over another neural baseline does not exhaust the relevant comparison space. The present corpus uses PAQ and description-length segmentation as selected anchors; it does not reconstruct the full history of context mixing or arithmetic coding.

### 3.2 LSTM state, gradient horizons, and test-time adaptation

Graves's *Generating Sequences With Recurrent Neural Networks* separates several units within one paper. PTB uses a 49-class character task and a 10,000-class word task; Wikipedia uses 205 observed one-byte symbols, including parts of multibyte encodings. Stacked LSTMs, skip connections, gradient clipping, and truncated backpropagation enable causal next-symbol prediction. Forward state persists across contiguous 100-byte pieces even though the gradient stops at piece boundaries. A short gradient horizon therefore need not imply equally short forward history ([BIW-0053](../03_reading/R02/BIW-0053.md), arXiv:1308.0850v5 §§2–3).

The same paper's dynamic evaluation changes weights on evaluation data. Its Wikipedia validation loss falls from 1.67 static to 1.33 dynamic bits per byte, but the learner and its test-time work have changed. This is not simply a bigger hidden-state cache. Modern comparisons should distinguish fixed weights, persistent recurrent or cached state, and online parameter updates. The character/word comparisons also do not equalize every parameter, data, and compute quantity. The enduring contribution is the separation of long state persistence, trainable recurrent transitions, and adaptive evaluation, not a single isolated alphabet effect (source §3.2/Table 2; [BIP-0083](../02_inventory/DETAILED_INVENTORY.md#BIP-0083)).

### 3.3 Byte recurrence as unsupervised representation learning

Radford, Jozefowicz, and Sutskever's byte multiplicative LSTM trained 4,096 units on more than 38 billion Amazon-review bytes, using weight normalization, Adam, persistent state, and truncated gradients. The reported single-epoch run took about a month on four Pascal Titan X GPUs. Frozen final cell states then supported supervised linear classifiers. Next-byte pretraining did not require sentiment labels, but downstream classification still did. Selected hidden-unit interventions changed generated sentiment, providing stronger evidence than a correlation between one unit and a label ([BIW-0063](../03_reading/R02/BIW-0063.md), arXiv:1704.01444v2 §§3–4.5; [BIP-0091–0094](../02_inventory/DETAILED_INVENTORY.md#BIP-0091)).

Its failures are equally instructive. Features plateaued with larger Yelp training sets, lost to an n-gram classifier there, and transferred less successfully to relatedness and paraphrase. Domain mismatch, document-final-state bias, and readout capacity were proposed explanations, not separately isolated causes. A universal byte alphabet supported useful in-domain features without making them universal semantic representations. The modern problem of preserving pretrained behavior through a new interface has an early counterpart here: surface coverage and transferable function are not the same achievement.

### 3.4 Character-composed words and contextual transfer

A parallel route shared spelling statistics while keeping word positions. Kim et al.'s *Character-Aware Neural Language Models* applies character embeddings, multi-width CNNs, max-over-time pooling, and highway gates inside externally segmented words. A word-time LSTM predicts a fixed word vocabulary. CNNs detect reusable local patterns, pooling makes a single lexical vector, and highway gates choose transformed versus carried features. An unseen input spelling can receive a vector, but the reported word softmax still cannot generate every unseen form ([BIW-0055](../03_reading/R02/BIW-0055.md), arXiv:1508.06615v4, Model/Figure 1).

The large PTB character-input model obtains 78.9 perplexity with about 19M parameters versus 85.4 for the authors' roughly 20M word-input baseline. Its often-cited approximately 60% saving uses a different published 52M comparator, not that 20M baseline. Table 7 further shows 84.6 without highway, 78.9 with two highway layers, and 92.6 with an ordinary one-layer MLP. The gates are a substantive part of the solution, not ornament around a character alphabet. Training is slower—about 1,500 versus 3,000 word tokens/s—and composition caching exchanges computation for memory. Input-table removal has not removed word-output cost ([BIP-0085/0126/0127](../02_inventory/DETAILED_INVENTORY.md#BIP-0085)).

ELMo extends this route to contextual representations. Character-CNN/highway composition supplies word-position inputs; separate forward and backward LSTMs contextualize them; a downstream task learns a scaled, softmax-weighted mixture of layers. Representation parameters are shared between directions, as are softmax parameters, while directional LSTMs remain separate. This is not character-input/word-output matrix equality. These historical claims use the designated narrow extraction of arXiv:1802.05365v2 §§1–3.4/Table 1; exact UTF-8 implementation and the complete later transfer evaluation lie outside it ([BIW-0140](../03_reading/FIELD_ADDENDUM/arxiv_1802.05365v2.md), [BIP-0293–0294](../02_inventory/DETAILED_INVENTORY.md#BIP-0293)).

The route contributes two ideas still central to bytes: compose spelling into a useful representation, and expose several contextual layers rather than assume one final vector is ideal for every task. Neither requires native byte generation. Historical character work should be credited for those ideas without being relabeled as evidence for a 256-way byte language model.

### 3.5 Byte-complete subwords as a different compromise

GPT-2's official report provides an influential intermediate interface. It begins with a 256-byte alphabet, learns frequent adjacent merges, and restricts merges across character categories, with a space exception, to avoid using vocabulary entries for many redundant lexical-punctuation combinations. The LM predicts 50,257 merged symbols, and its context is 1,024 model tokens. The supporting extraction is report p.4 §§2.2–2.3 and adjacent §3.1, not a full audit of the report's benchmark results ([BIW-0141](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md), [BIP-0295–0296](../02_inventory/DETAILED_INVENTORY.md#BIP-0295)).

This route removes dependence on an observed character inventory while keeping a large output vocabulary and relatively short computation sequence. It is neither an all-byte-step model nor merely a defective approximation to one. Coverage and amortized lexical prediction are its intended combination. The earlier character-based BPE translation lineage and later byte-based BPE should not be collapsed: the same merge algorithm can operate on different atomic alphabets. Nor should the report's preliminary raw-byte observation be promoted into a matched-compute frontier that the examined passage does not supply.

The historical picture is thus plural. Recurrent streams, word-local composition, contextual transfer, byte-complete merged vocabularies, and later hierarchical bytes solve overlapping but distinct problems. The sequence is not a ladder in which each later model makes all earlier interfaces obsolete.

<a id="s04"></a>
## 4. Local composition, encoders, and conditional generation

### 4.1 Raw-byte annotation changes the output problem

Gillick et al.'s *Multilingual Language Processing From Bytes* reads 60-byte UTF-8 windows with a compact LSTM and serializes annotations as start, length, label, and STOP. Serializing avoids a huge joint classifier over all span triples. The approximately 900K-parameter task model shares recurrent parameters between reading and annotation phases and across languages. Byte dropout discourages memorizing local strings; overlapping windows reduce edge effects ([BIW-0057](../03_reading/R02/BIW-0057.md), arXiv:1512.00103v2 §§3–6; [BIP-0129–0131](../02_inventory/DETAILED_INVENTORY.md#BIP-0129)).

The entire window is visible before labels are emitted, so it is not causal text generation. Invalid or incomplete annotations are ignored rather than excluded by a formal grammar. Window overlap roughly doubles long-text input processing and does not guarantee every arbitrarily long span is covered. Multilingual gains vary, and an annotated code-switching test is absent. The contribution is a common compact annotation interface, not a demonstration that every multilingual operation becomes easy once input is bytes.

### 4.2 Source composition in translation

Lee, Cho, and Hofmann's character NMT composes source characters using width-one-to-eight convolutions, stride-five max pooling, four highway layers, and a bidirectional GRU; an attention-based target GRU emits characters. Overlapping convolutional receptive fields can capture substrings across fixed pooling cells even though the grid is not learned. Its finite alphabets, Moses processing, and Russian ISO-9 transliteration identify it as a character antecedent, not raw UTF-8 evidence ([BIW-0059](../03_reading/R03/BIW-0059.md), arXiv:1610.03017v3 §4/Figure 1).

The multilingual model improves all four reported test2 directions over its multilingual BPE-to-character comparator, but bilingual Finnish and Russian comparisons reverse. Different length filters retain different examples, and multilingual training adds English target exposure. The result demonstrates successful local composition under a full-source translation objective. It does not isolate pooling, alphabet, and data as independent causes. Its Finnish character-to-character BLEU of 13.10 versus 13.98 for BPE-to-character is a useful specific counterexample to a universal finer-input advantage.

ByteNet instead preserves resolution with dilated convolutions. Unmasked source convolution supports full-source encoding; masked target convolution allows parallel teacher-forced scoring. The translation task uses restricted English/German characters, while the Hutter LM task uses byte-valued Wikipedia symbols. Linear fixed-depth operation structure is not parallel ancestral emission: an unknown next target still depends on previous generated targets. Table/prose result discrepancies in arXiv:1610.10099v2 remain source-reporting issues rather than evidence that dilation failed ([BIW-0058](../03_reading/R02/BIW-0058.md), §§2–6/Tables 2–4; [R1 §3](../05_review/FULL_READING_AUDIT_R1.md)).

### 4.3 Fusion is not necessarily shortening

Local Byte Fusion adds multiscale local features and restores the byte sequence length. Its convolutional arm composes local patterns; its word-span arm restricts attention using externally supplied boundaries. The latter is hybrid structural information, while neither automatically reduces the persistent position count. Lao-to-English BPE scores 9.2 BLEU versus dense bytes 5.9 and fusion arms 6.4/6.5. A fixed-update training advantage coexists with slower inference and no equal-epoch advantage ([BIW-0048/W0514](../../flued_multigranularity_survey_20261108/03_reading/B26/W0514.md), arXiv:2205.11490v3 §3/Table 3/Appendix B).

Subword-Delimited Downsampling explicitly uses SentencePiece boundaries to make variable groups of UTF-8 bytes. CNN/max pooling composes each source group, and a local target LSTM emits bytes until an end marker. Its comparisons separate fixed, buffered-fixed, word-delimited, and subword-delimited strategies, although position, length, and lexical grouping still co-vary. Six-direction average BLEU rises from 16.56 fixed to 19.46 buffered-fixed and 19.98 SDD, while English-to-Turkish and biomedical cases resist the average trend. At WMT14 scale, standard subword translation gives 28.62, subwords plus the local LSTM 27.49, and SDD 27.27. Group boundaries cannot automatically compensate for a weaker recovery interface ([BIW-0075](../03_reading/R03/BIW-0075.md), Findings EMNLP 2022 §§3–8/Tables 3–9/Appendix C).

These studies separate three operations often conflated as tokenization: adding local features, reducing positions, and changing the output factorization. A fair comparison should identify which operation changes and retain a control for the local decoder where one is introduced.

### 4.4 CharacterBERT and the open-input/closed-target split

CharacterBERT UTF-8-encodes each supplied word, uses a word-local byte CNN/max/highway composer, and runs BERT at word positions. Its MLM classifier covers only the 100,000 most frequent words, and words outside that list are not masking targets. Local length caps and externally provided word boundaries remain. The reported medical pretraining takes 55 hours versus BERT's 26.5; several task/noise results improve, but ClinicalSTS reverses ([BIW-0066](../03_reading/R01/BIW-0066.md), arXiv:2010.10392v3 §§3–5/Appendix A.1; [BIP-0136–0138](../02_inventory/DETAILED_INVENTORY.md#BIP-0136)).

This is not a failure to become a byte generator. It is a deliberate understanding model that changes lexical composition while retaining word-position contextualization and closed pretraining targets. Its task benefit is evidence for that hybrid. The distinction matters when a survey asks whether input vocabulary independence has removed all vocabulary-related costs: here it plainly has not.

### 4.5 ByT5: simple bytes with a changed pretraining recipe

ByT5 retains UTF-8 bytes, uses a small lexical interface, and learns span reconstruction in an encoder–decoder. The encoder sees the whole corrupted source; the decoder causally emits missing spans. Average corruption length is increased to 20 bytes rather than mechanically copying a short subword setting. A roughly three-to-one encoder/decoder layer allocation puts more capacity on source processing. Those are material objective and allocation choices, not consequences of the byte alphabet ([BIW-0024/W0351](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md), TACL 2022 §§3/6; [BIP-0037–0043/0246](../02_inventory/DETAILED_INVENTORY.md#BIP-0037)).

Its strengths include intraword tasks and selected noise conditions. Table 5 reports Large-model transliteration character error rate (CER) of 10.5% versus mT5's 18.1%, grapheme-to-phoneme phoneme error rate (PER) of 1.8% versus 6.7%, and morphology accuracy of 89.7% versus 75.7%. The corresponding grapheme-to-phoneme word error rates are 15.4% versus 43.5%, a different error unit. These supervised outcomes are not general causal-LM scores. Equal 1,024-position inputs expose much less source text to bytes: the cited mixture averages about 4.1 UTF-8 bytes per mT5 subword. Table 9's pretraining throughput is about three quarters of mT5's on **TPUv3-64**. Table 10 reports 6.4–9.5× slower **XNLI** inference across the reported sizes on **TPUv3-32**; its XSum measurements instead use TPUv3-128. XNLI is a long-input sentence-pair task with short labels, so its slowdown cannot be explained solely by long generated outputs. Invalid-byte-ignore decoding is also different from a constrained valid generator ([ByT5 TACL 2022 §§4.4/7, Tables 5/9/10](https://aclanthology.org/2022.tacl-1.17.pdf); [carrying card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md)).

ByT5 also supplies a useful near-control between bytes and large subwords. Its **CharT5** ablation uses 47,198 character entries, SentencePiece constrained to single-character pieces, and byte fallback for coverage. It is neither an unrestricted code-point-only model nor a pure byte-step model. At 1.23B total parameters, CharT5 retains 36/12 encoder/decoder layers but uses width 1,376 and about 11% vocabulary-related parameters. Table 8 reports CharT5 versus ByT5-Large XNLI accuracy 79.0%/79.7%, TyDiQA F1 87.6/87.7, and GEM-XSum BLEU 11.2/11.5. Common characters can therefore shorten non-ASCII inputs while fallback retains coverage, with near-competitive results in this setup. Width, capacity allocation, and computation per original text differ, so this is not an isolated alphabet effect or a statistical-equivalence test ([ByT5 arXiv:2105.13626v3 §6.4, Tables 7–8](https://arxiv.org/html/2105.13626v3#S6.SS4); [targeted source verification](../05_review/FINAL_SURVEY_COVERAGE.md#p2-01--include-the-unusually-relevant-character-vocabularybyte-fallback-near-control)).

The contribution is broad byte-to-byte pretraining with a deliberately adjusted recipe. Neither the task wins nor the costs should be erased by trying to assign them to bytes alone. They show a useful system and identify the architecture, exposure, and task dependencies that a follow-up should control.

### 4.6 CANINE: code-point coverage, shortening, and removable supervision

CANINE addresses the size of a full Unicode lookup using multiple learned hash tables. Eight hash lookups with 16K buckets are concatenated to width 768; collisions are accepted. Local attention contextualizes code points before stride-four convolution maps 2,048 positions to 512 deep states. Sequence tasks repeat coarse states, concatenate early fine representations, and apply convolution and final attention. Classification can use the coarse CLS without the final fine layer ([BIW-0004](../03_reading/R01/BIW-0004.md), arXiv:2103.06874v4 §3.1/Figure 1).

Its objectives make supervision a separate axis. CANINE-C predicts bucketed code-point targets in shuffled masked-target autoregressive order, conditioned on the masked encoded sequence. Bucket collisions mean this is not exact original-code-point probability. CANINE-S predicts subwords at selected positions and discards the tokenizer and prediction head after pretraining. Both use next-sentence prediction; whitespace-based masking remains a structural prior. A deployed tokenizer-free input encoder can thus be trained with tokenizer-derived targets (source §3.2/Figure 2).

The n-gram result is especially important. CoNLL macro F1 rises from 74.0 for CANINE-C to 86.7 with hashed n-grams, near mBERT's 87.8, while parameters rise from 127M to 167M. Fine compositional access did not eliminate the usefulness of lexical memorization. The corrected headline gains also name different arms and metrics: CANINE-S SELECTP is +2.8, while CANINE-C+n-grams MINSPAN is +5.7. They are not a version flip. Separate n-gram prose/table deltas remain unreconciled, so the tabulated values should retain their table attribution (source Tables 2/5/7; [R1 §3](../05_review/FULL_READING_AUDIT_R1.md)).

Shortening improves feasibility, but not necessarily speed over a subword baseline. On the reported 64-TPUv3 setup, CANINE-S pretraining is 6,400 examples/s versus reimplemented mBERT's 9,000 and full-length character/subword-supervised processing's 900. Increasing stride gains throughput while damaging QA. This is a successful hierarchy whose quality and cost remain coupled to stride, restoration, targets, and lexical capacity.

### 4.7 Perceiver IO: deep work without a text partition

Perceiver IO cross-attends from latent queries to bytes or subwords, runs deep self-attention on a fixed latent array, and uses output queries for position- or task-specific results. Latent slots need not denote contiguous text spans. In its language setup, whole-word masking selects corruption while masked identities are predicted from the corrupted source. Parallel output queries are not a causal byte decoder ([BIW-0117](../03_reading/R01/BIW-0117.md), arXiv:2107.14795v3 §3/§4.1/Appendix F).

At roughly matched reported operations, byte Perceiver obtains 81.0 GLUE versus byte BERT's 71.5, with 201M versus 20M parameters. Token BERT is 81.1 at approximately 109B FLOPs versus byte Perceiver's approximately 113B. These comparisons show that a fixed workspace can make deep byte processing useful; they do not isolate capacity or establish causal serving. Narrowing latent count while widening slots can hurt despite similar FLOPs, so latent count and width are not fungible merely because their operation estimates match.

Together, the encoder and translation literature supplies a broad lesson: local detail can be made useful through composition, bottlenecks, query interfaces, and appropriate supervision. Full-source access changes what those mechanisms are allowed to compute. Their success is evidence for fine-input representation learning under those permissions, not a shortcut around the separate problem of online causal generation.

<a id="s05"></a>
## 5. Full-resolution computation and alternatives to segmentation

### 5.1 Deep byte attention before learned patches

Fine positions need not be compressed to support useful language prediction. Al-Rfou et al.'s deep self-attention model retains one position per byte and a 256-class next-byte head. All-position losses, temporary intermediate-layer classifiers, and auxiliary two-step-ahead targets help optimize a deep causal stack. Only the immediate next-byte classifier remains at inference. Text8's 27-symbol restricted alphabet and enwik8's byte stream are distinct experimental interfaces even when described together as character modeling ([BIW-0064](../03_reading/R09/BIW-0064.md), arXiv:1808.04444v2 §§2–4).

The 64-layer enwik8 model reports 1.06 bits per byte; evaluation recomputes a 512-byte context for each scored byte. This is strong likelihood evidence, not efficient serving. The later *Bridging the Gap for Tokenizer-Free Language Models* scales a plain 40-layer causal byte Transformer to roughly 836M parameters. Its processed-lm1b score of about 0.874 BPB becomes 23.0 word perplexity under the same corpus event counts. The corpus is sentence-shuffled, pretokenized, and already replaces rare words with UNK. Nevertheless, the result directly counters the claim that a byte clock intrinsically prevents competitive large-data likelihood. It does not establish an equal-compute comparison with all cited word systems or untouched-raw-text coverage ([BIW-0071](../03_reading/R09/BIW-0071.md), arXiv:1908.10322v1 §§2–3.2/Table 1/Eq.3).

The distinction between preprocessing and interface matters here. Removing a tokenizer from a neural model does not reverse information already removed when the benchmark was constructed. Nor does using original bytes guarantee a practical evaluator: stride-one full-window rescoring is a valid probability protocol but a poor stand-in for incremental generation. These systems are meaningful nonhierarchical controls precisely because their achievements and costs can be named separately.

### 5.2 Sparse edges and approximate connectivity

Sparse Transformer preserves positions while reducing which pairs interact. Its fixed patterns and strided patterns have different effects on language. At 12,288-position enwik8 context, dense/fixed/strided configurations report 1.00/0.99/1.13 BPB and Time/Iter 1.31/0.55/0.35. The table supplies no time unit. Fixed sparsity preserves or improves quality in this comparison; the fastest reported strided configuration loses materially. The million-position demonstration elsewhere is audio, not million-position language evidence ([BIW-0118](../03_reading/R09/BIW-0118.md), arXiv:1904.10509v1 §§3–7.2/Table 2).

Reformer separates three costs. Locality-sensitive hashing approximates content-based attention connectivity. Reversible paired residual streams reconstruct activations during backward computation, reducing depth-dependent training storage. Position-wise feed-forward chunking lowers peak intermediate tensors without changing the position-wise function. None of these reduces the number of text positions. Shared query/key projections belong to its attention mechanism, not lexical input/output tying ([BIW-0139](../03_reading/FIELD_ADDENDUM/arxiv_2001.04451v2.md), arXiv:2001.04451v2 §§2–3/Appendix A).

More hash rounds trade quality against cost; approximate attention is not guaranteed exact nearest-neighbor recovery. The component functions inside reversible blocks need not themselves be invertible. Activation reconstruction does not eliminate optimizer state, parameters, or inference KV, and execution chunks are not semantic segments. The largest Reformer models lack equally large full-attention controls, while the source's full-attention baselines already use memory-efficient recomputation rather than necessarily materializing every matrix. Its Figure 5 attention-evaluation timing holds total token count fixed while varying sequence length; it is not matched-quality cached serving (§5/Figure 5). These qualifications leave a substantial positive result: different execution and connectivity choices can make full-resolution long-sequence training feasible without learned segmentation.

### 5.3 Reusing and compressing history

Transformer-XL concatenates stopped-gradient hidden states from prior segments with current states and uses relative positions to avoid reset-position ambiguity. Forward history extends beyond the segment through stored states, while gradients do not cross the cached boundary. This is neither an unbounded fixed vector nor a learned text partition. The formal paper and separately scoped arXiv-v3 appendices remain one work with a version boundary ([BIW-0119](../03_reading/R09/BIW-0119.md), ACL 2019 §§3.1–3.3/4 and arXiv:1901.02860v3 appendices).

Its celebrated evaluation ratios—363× at attention length 800 and 1,874× at 3,800 in the enwik8 discussion—compare reuse with uncached full-window recomputation. They show the importance of the baseline, not a modern batched-serving advantage of that magnitude. Weight-updating dynamic evaluation is a different permission again. A recurrent hidden state, segment cache, and online optimizer can each retain information, but their retained objects, training paths, and test-time costs differ.

Compressive Transformer adds a smaller, older memory after ordinary recent memory. An auxiliary compression function can preserve the attention outputs produced from old states, with gradients stopped into source states and attention parameters for that loss. This consumer-aligned objective differs from reconstructing every hidden coordinate. Its enwik8 comparison favors convolution plus attention reconstruction over several alternatives, but compression rates are selected separately and the longer-backpropagation control changes unroll and batch. More compressed memory is nonmonotonic: 3,072 slots gives 0.97 versus 1.00 at 4,096 in the cited appendix ([BIW-0018/W0023](../../flued_multigranularity_survey_20261108/03_reading/B24/W0023.md), arXiv:1911.05507v1 §3.2/Table 5/Appendix B).

These examples shift the question from how many bytes were read to what form of history remains available. Retaining a sequence of states, compressing old states, and maintaining a fixed recurrent state provide different access and capacity. An average next-byte loss alone does not certify exact retrieval of an arbitrary past span.

### 5.4 Selective state and adaptive within-byte depth

MambaByte advances through every byte using a selective state-space recurrence. Input-conditioned updates and readouts operate with a fixed-size state per layer rather than an attention cache over all prior bytes. Its near-per-byte-FLOP comparisons with MEGABYTE favor it on several corpora but use different training-byte totals and approximate accounting. This is evidence for a full-resolution recurrent alternative, not a clean isolated architecture effect. The separate subword-drafter acceleration adds another model and uses a top-three verification policy, which does not establish exact target-law sampling ([BIW-0025/W0352](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md), arXiv:2401.13660v3 §§2–3/Appendix F).

Adaptive Computation Time changes a different axis: the number of internal recurrent transitions before advancing one byte. Halting probabilities determine a weighted state/output aggregate, and a ponder penalty discourages extra transitions. Its Wikipedia task explicitly uses one byte per input step, next byte as target, and a 256-class softmax. It does not shorten the stream. The reported errors are training-set errors and fairly similar with and without ACT; extra computation yields at most a slight benefit there. Its gradients treat discrete stopping counts as fixed, ignoring their discontinuities, and ponder count is not wall-clock or energy measurement ([BIW-0138](../03_reading/FIELD_ADDENDUM/arxiv_1603.08983v6.md), arXiv:1603.08983v6 §§2.2/3.5).

ACT is important even without a strong held-out byte win because it prevents an incomplete taxonomy. Computation can vary within a symbol, across selected symbols, across attention edges, or across stored history. Punctuation-associated effort traces are not validated word boundaries, but they are an early reminder that uncertainty and computational difficulty need not coincide. Later utility-based patching should be compared with that distinction without claiming direct intellectual borrowing.

**Table 2. Resources changed by alternatives to grouping.**

| Mechanism | Primary resource changed | Positions retained? | Distinct residual cost or limitation |
|---|---|---|---|
| Dense byte stack | Depth/capacity and optimization | Yes | Full per-position work and potentially expensive scoring |
| Sparse Transformer | Allowed attention edges | Yes | Pattern-dependent quality; sparse execution overhead |
| Reformer LSH | Approximate content connectivity | Yes | Hashing, sorting, rounds, and approximation |
| Reversible blocks | Training activation storage across depth | Yes | Recomputation; parameters/optimizer/inference state remain |
| FFN execution chunking | Peak intermediate activation memory | Yes | No reduction in byte prediction count |
| Transformer-XL | Repeated history computation | Yes, as cached states | Stopped gradients and persistent sequence memory |
| Compressive Transformer | Representation of older history | Recent and compressed states | Information loss and auxiliary compression work |
| MambaByte | State representation and update complexity | One update per byte | Fixed-state capacity rather than explicit past-position access |
| ACT | Internal transitions per byte | Yes | Halting optimization and added transitions |
| Perceiver IO | Sequence receiving deep processing | Fixed latent slots | Input/output cross-attention; encoder evidence |

The choice is not simply to compress or not compress. It is which resource to reduce, which information to preserve, and which approximation or recomputation to pay for.

<a id="s06"></a>
## 6. Learning groups: content, boundaries, and rate

### 6.1 A boundary does not specify a representation

Grouping contains at least three design variables: the partition or update locations, the content operator, and the pressure to reduce computation. Fixed concatenation preserves ordered byte coordinates at an input patch; a mean loses order unless its members are contextualized or position-coded; attention can retain task-selected combinations; endpoint selection relies on what the selected state has already encoded. Deletion keeps contextual survivors rather than explicitly aggregating every raw span. A fixed latent array need not partition text at all.

This is why DTP and H-Net are not interchangeable “pooling” systems. DTP averages completed contextual character spans and reports an advantage over endpoint sampling in its setup. H-Net directly selects contextual states and finds mean, max, and cross-attention aggregation roughly comparable under its learned boundaries. Different local encoders, tasks, and gradient paths make those results compatible. They do not establish a universal operator ranking ([DTP/BIW-0007](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md), §§3–5; [H-Net/BIW-0011](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md), arXiv:2507.07955v2 Appendix E.1).

### 6.2 Fixed grids, observed-byte rules, and external groups

MEGABYTE makes fixed patches competitive by adding an ordered patch embedding and a local autoregressive decoder. Fixed boundaries make scheduling and shapes predictable but place identical strings at different offsets and can divide useful local structures. SpaceByte instead triggers global processing after certain consumed bytes: roughly those that are neither ASCII alphanumeric nor UTF-8 continuation bytes, with additional BOS and consecutive-spacelike conditions. Its state is already contextual; it does not mean-pool words. A multibyte character can trigger after its first byte rather than after a completed scalar ([BIW-0009/W0009](../../flued_multigranularity_survey_20261108/03_reading/B05/W0009.md), v3 §2/Appendix C).

Rule-based boundaries are serious controls. Under independently optimized architectures at 10^19 training FLOPs, SpaceByte/SentencePiece/fixed-interval scores are 1.009/0.989/1.112 BPB on PG-19 but 0.748/0.768/0.804 on arXiv. The preferred policy changes by domain; these are selected frontier points, not equal-parameter systems differing only in a bit. The study also reports preliminary Chinese weakness. DTP's English whitespace result can match or beat learned routes, while Finnish favors unigram-guided pooling at a different realized rate. Rules exploit real structure, but their script and domain assumptions should be measured rather than universalized.

External segmentation can also be a useful engineering choice. SDD explicitly imports SentencePiece boundaries; CANINE-S imports subword labels; various adaptation systems imitate an ancestor tokenizer. These are not automatically weaker evidence because they are hybrid. Their important distinction is where the external resource is required: offline preprocessing, training targets, online inference, or output reconstruction. A deployable byte interface can legitimately borrow statistical lexical structure without pretending to have learned it end to end.

### 6.3 Soft candidate mixtures and cumulative assignments

Charformer's Gradient-Based Subword Tokenization enumerates candidate block widths, computes means, scores and repeats their representations, and mixes widths with a softmax before final fixed-stride reduction. Neighboring positions can favor incompatible widths, so the mixture is not a sampled coherent partition. A width-five convolution supplies local order-sensitive features; means alone would not. Optional global score calibration is suitable for the full-source encoder, not automatically for online use, and is disabled in multilingual experiments ([BIW-0005](../03_reading/R01/BIW-0005.md), arXiv:2106.12672v3 §§2.1.1–2.1.5/4.3).

MANTa predicts Bernoulli frontier probabilities with a local Transformer. Cumulative counts define a Poisson-binomial block-index distribution, approximated by a truncated Gaussian for soft membership. Weighted embeddings pass through depthwise convolution, max pooling, and projection. This is a differentiable membership approximation, not exact marginalization over every discrete segmentation. It caps retained blocks at one quarter of input length; excess representations can be truncated. Section 6.1 reports degeneration toward one block per byte without the bottleneck. Denoising alone does not reliably discover economical computation ([BIW-0006](../03_reading/R01/BIW-0006.md), arXiv:2212.07284v1 §3.1/§6.1/Appendix D).

The cap and the gradient solve different problems. A smooth path lets the policy learn; a capacity constraint prevents an expensive solution. Neither guarantees lossless retention. MANTa's 2.61-second training step versus byte T5's 9.06 and subword T5's 1.13 on 16 V100s shows useful encoder savings with a remaining subword gap. Inputs, schedules, and budgets differ; it is not evidence for accelerated byte generation (Table 5).

### 6.4 Hard routing and practical gradient estimators

HM-RNN learns when recurrent levels UPDATE, COPY, or FLUSH. COPY preserves state, while FLUSH transmits/resets information and can use top-down context. Its hard-sigmoid straight-through estimator is biased, and slope annealing differs by dataset. Boundary pictures near spaces do not establish word discovery; a later space-stripped segmentation task finds very low HM-LSTM word F1 under a different contract ([BIW-0016](../03_reading/R03/BIW-0016.md), arXiv:1609.01704v7 §3/Table 1).

DTP offers supervised unigram imitation, own-model entropy boundaries, and a jointly learned Gumbel arm. The latter combines hard choices with a differentiable assignment surrogate and a binomial boundary-count prior. Its entropy comes from the main model, unlike BLT's separately trained patcher. The Gumbel route is less stable in the reported experiments. H-Net instead thresholds cosine change between projected adjacent contextual states, uses EMA dechunking and straight-through treatment, and adds a ratio objective coupling hard selection with mean confidence. Removing smoothing destabilizes compression. A ratio loss is not a hard per-example quota: confidence and realized rate can disagree ([DTP card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md); [H-Net v2 §2 Eqs.1–10/§3.3 Figure 7](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md)).

H-Net's own task comparison shows why the hierarchy is attractive. At the XL budget, the BPE Transformer reports 55.5% average downstream accuracy at 0.69 GFLOPs/byte, versus 58.2% for two-stage H-Net at 0.69. The strong H-Net(space) control reaches 57.1% at 0.70, and one-stage H-Net 56.2% at 0.72. Table 1 lists approximately 1.3B parameters for BPE and 1.6B for the two-stage model, so this is not equal-parameter evidence. Training uses the same FineWeb-Edu subset, 8,192-byte versus 1,792-GPT-2-token examples, and approximately matched original text per batch and paper-estimated FLOPs. The resulting quality gain supports the complete hierarchical system under that budget, not an isolated effect of learned boundaries, identical retained examples, or faster wall time ([H-Net arXiv:2507.07955v2 §3.1, Tables 1–2](https://arxiv.org/html/2507.07955v2#S3); [carrying card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md)).

The cross-domain controls sharpen that result. Chinese XWinograd accuracy is 59.9%/62.9%/66.3% for BPE/space/two-stage H-Net; code BPB is 0.3376/0.3163/0.3161, making dynamic and space nearly tied on code. These runs use Llama-3 BPE and domain-adjusted model depths and budgets, rather than one identical cross-domain compute budget. Learned hierarchy can improve quality beyond a strong rule in a reported setting without dominating every rule/domain comparison (v2 §3.2/Table 4/Appendix E.2; [H-Net card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md)).

The REINFORCE alternative samples boundary actions and optimizes an expected conditional log-likelihood using a score-function gradient. The expectation objective is a Jensen lower bound on a boundary-marginalized likelihood. Practical variance reduction uses an early-exit byte classifier as a tokenization-independent difficulty baseline, detached batch-relative advantages, and discounted future rewards. Discounting deliberately introduces bias; an ideal score-function identity does not make the deployed estimator unconditionally unbiased. At rates around 0.2, the 147M FineWeb comparison reports 1.280 BPB for its w=1 policy versus 1.299 BPE-guided and 1.386 H-Net. Uniform routing still wins one ARC-Easy gold-continuation BPB cell; that cell is not answer accuracy ([BIW-0078](../03_reading/R09/BIW-0078.md), arXiv:2602.13940v4 §§2.4–2.7/Table 1/Appendices A/D).

These methods trade different forms of bias, variance, stability, and supervision. A useful analysis asks which gradients reach a boundary decision, what rate pressure acts separately, and whether the resulting policy is evaluated under its actual sampled or deterministic deployment rule. “End to end” does not resolve those questions.

### 6.5 Entropy, observed confidence, utility, and novelty

BLT uses a separately trained causal byte model, typically 100M parameters with a 512-byte window, to estimate predictive entropy and select patches. Entropy is uncertainty over possible next bytes before the actual byte is observed. SOMBRERO instead trains boundary confidence toward one minus a stop-gradient probability of the observed next byte. That target can use the training label without giving deployment future access. The two signals ask different questions and require different resources ([BLT/BIW-0010](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md), ACL 2025 §§2/4/Appendix O; [SOMBRERO/BIW-0012](../../flued_multigranularity_survey_20261108/03_reading/B24/W0012.md), v1 §3).

BLT's conference version also reports useful task-quality gains under a specified budget. Its 8B equal-training-FLOP comparison has the near-monotonic entropy variant exceed Llama 3 on four of seven downstream tasks. Exposures differ: Llama 3 uses about 4T bytes, entropy BLT about 4.5T, and space BLT about 6T, with different patch rates. Appendix P Table 10 gives ARC-Easy accuracy 68.9% for entropy BLT, 67.2% for space, and 67.4% for BPE, but the space arm comes from an earlier version without cross-attention. These results support a competitive byte hierarchy, not entropy's isolated superiority; local cross-attention, n-gram capacity, text exposure, and inference threshold all matter ([BLT ACL 2025 §5.2/Table 1, §7, Appendix P/Table 10](https://aclanthology.org/2025.acl-long.453.pdf); [conference-version card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md)).

SOMBRERO's controlled ladder resists attributing the whole gain to confidence supervision. At roughly 5× compression, 1.95 GFLOPs/byte, and 839B bytes, H-Net's 0.6701 becomes 0.6571 with byte smoothing; sigmoid routing gives 0.6578, and confidence supervision 0.6568. Most change in that ladder precedes the new target. At larger scale, more surprise enrichment accompanies essentially unchanged BPB and a lower downstream average. Better alignment to a diagnostic is not necessarily greater task utility (Table 1/Appendix D).

Utility patching estimates the loss reduction from refreshed global computation. A BLT-1B study fits a past-two-byte lookup from whole-layout loss differences; a smaller variant uses single-added-boundary scoring. These are not identical causal interventions. At about 10% rate, entropy-plus-dependence raises forced-true-prefix computed-value accuracy from 19.0% to 67.1%. Dependence alone is 67.8% there but final-answer accuracy falls to 4.8% versus entropy's 51.4%; free GSM8K remains around 2% or below. The signal can improve a tightly controlled intermediate event without solving the whole task ([BIW-0029/W0357](../../flued_multigranularity_survey_20261108/03_reading/B05/W0357.md), v1 §§3–10).

The related novelty study learns future repetition from past-byte contexts. It improves selected forced-prefix targets while worsening overall BPB and transferring poorly to code; changing inference boundaries can destroy a model trained on the original rule. The studies share author, pipeline, and evaluation resources rather than constituting independent replications ([BIW-0030/W0358](../../flued_multigranularity_survey_20261108/03_reading/B14/W0358.md), v1 §§3–6/Table 5). Together with ACT, they support a bounded conceptual conclusion: uncertainty, surprise, recurrence novelty, and incremental computational value are distinct. A cheap universally better utility policy remains unestablished.

### 6.6 Lexical discovery, deletion, and quantized codes

A computational boundary need not be a word. The segmental neural LM makes lexical discovery explicit by mixing an autoregressive character spelling model with lexical memory, summing permitted segmentations using semi-Markov dynamic programming, and adding expected-length regularization. Its generative history depends on prior characters rather than previous latent segmentation, enabling the dynamic program. Full-sentence MAP segmentation is recovered after observing the sentence; it is not the online generation policy. BR-phono F1 is 79.3 for the complete model versus 42.5 without memory and penalty, but boundary evaluation uses the union of splits and unseen character types are filtered. Optional VGG19 image attention adds another supervision source. Good marginal likelihood and human-boundary F1 remain distinct ([BIW-0042](../03_reading/R03/BIW-0042.md), ACL 2019 §§2–4/7/Appendix F).

MrT5 instead softly deletes contextual encoder positions during training and removes them at inference. Survivors may already encode neighboring content, so this is not raw-byte pruning before contextualization or necessarily explicit span aggregation. Its gate-learning machinery includes softmax1 and rate control, whose jobs should not be reduced to one generic sparsity penalty. At 50% target deletion, a selected timing falls from 44.29 to 29.99 ms, while TyDiQA GoldP EM/F1 falls from 69.90/79.58 to 68.27/77.73. Encoder shortening can be useful without preserving all tasks or shortening the autoregressive output ([BIW-0046/W0511](../../flued_multigranularity_survey_20261108/03_reading/B22/W0511.md), arXiv:2410.20771v3 §§3/5–6/Appendix C).

Discrete reconstruction tokenizers introduce yet another contract: a learned code sequence and decoder may make spelling errors, so reconstructive accuracy and any fallback determine whether the interface is lossless. The quantized-code records retain that distinction rather than assuming that a token's ancestry is an inverse map ([BIW-0013/BIP-0158–0159](../02_inventory/DETAILED_INVENTORY.md#BIP-0158)). Adjacent vision token merging illustrates size-weighted aggregation and multiplicity accounting, but it is not direct causal-byte evidence. Across these routes, a boundary, survivor, latent slot, and discrete code are different technical objects.

<a id="s07"></a>
## 7. Causal availability and state freshness

### 7.1 Causality belongs to every information path

For next-byte prediction, every feature must be computable from the permitted observed prefix. Attention masking is only one part of this requirement. Convolution, pooling, score calibration, residual connections, boundary annotations, positional features, and upsampling can each introduce unavailable information. A full-source translation encoder is allowed future source context; a causal target is not allowed future target bytes. These are different time axes, not inconsistent uses of causality.

MEGABYTE makes the distinction concrete through two shifts. The global input is shifted by a complete patch, so current-patch global conditioning comes from preceding patches. Local input is shifted by one byte, so the local decoder sees already emitted bytes in the current patch. DTP similarly exposes a completed segment only after completion; earlier positions use previous coarse context plus their fine path ([MEGABYTE](../03_reading/R03/BIW-0008.md), arXiv:2305.07185v2 §2.2/Eqs.2–6; [DTP](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md), §§3.1–3.3).

Hourglass needs an extra k−1 shift before shortening beyond ordinary next-symbol alignment. Every shortening operand must respect it, including attention keys and values. Its expressivity restriction must also be stated precisely: without fine-resolution Transformer layers, the shortened branch lacks current-group history, **but the shifted-input residual can still transmit the immediately previous symbol**. Appendix A.1's two-position-back copying construction exposes restricted access, not blanket within-group independence or a causal leak. One fine-resolution attention layer removes that restriction in the construction; it does not guarantee learned arbitrary-task accuracy ([BIW-0072](../03_reading/R03/BIW-0072.md), arXiv:2110.13711v2 §2.2/Appendix A.1/Table 9; [current correction](../05_review/CLAIM_RULES.md#6-hourglass-restrict-the-independence-claim-to-the-information-path)).

### 7.2 A leakage diagnostic and a failed repair

*Patching Leaks in the Charformer* demonstrates future access in a tested decoder construction. On independent 100-symbol random sequences, chance is 1%, yet early block positions can be predicted nearly perfectly. Convolutional lookahead explains one path; removing convolution leaves overlap through candidate n-grams. Masking or removing crossing candidates repairs the tested paths. This is an empirical mechanism diagnostic rather than a general suspicion about all grouping ([BIW-0074](../03_reading/R03/BIW-0074.md), arXiv:2205.14086v1 §§2–3/Tables 1–3).

A leak-free large-padding repair still nearly fails translation: German-to-English factor-two BLEU is 0.04 versus 25.49 for overlap removal. Correct visibility does not guarantee an adequate prediction horizon or optimization problem. The contrast is important because a causal audit and a quality test answer different questions. A model can be honest but weak, and a suspiciously easy synthetic diagnostic can reveal unavailable information without proving its natural-language advantage came entirely from that path.

### 7.3 Offline training targets and offline test features

Future-informed training labels do not automatically leak. A prefix-only router can learn to imitate offline token ends, observed-target confidence, or future loss improvements, just as an LM learns from next-symbol labels. The deployment issue is whether its action actually reads the future. Conversely, evaluating on full-string BPE starts, ends, or repeated subword positions can add unavailable side information if the tokenizer is not prefix-stable.

A ranked-BPE toy example illustrates the distinction. If `bc` is merged before `ab`, tokenizing `ab` can give `[ab]`, whereas `abc` can give `[a,bc]`; a start flag at `b` changes when future `c` arrives. This refutes universal prefix stability, not an actual leak-rate measurement for the Llama tokenizer in byte-simulation experiments. A one-byte shift of an offline end guide does not supply the missing argument. Training-only withdrawal results remain different evidence ([BIW-0108](../03_reading/R08/BIW-0108.md), arXiv:2604.27263v2 §§5.3–5.4; [BIW-0078](../03_reading/R09/BIW-0078.md), §4.3/Appendix D.1).

AU-Net selects regex-defined contextual endpoints, contracts them into higher multiword stages, and expands a state across the following segment. Timing induces longer predictive horizons under one next-byte objective rather than an explicit word-target loss. Its right-insertion-stability requirement is appropriate, but actual prefix stability of the complete regex remains unverified. Causal attention cannot certify preprocessing ([BIW-0077](../03_reading/R10/BIW-0077.md), arXiv:2506.14761v1 §§2.1–2.2/Appendix B).

### 7.4 Refresh without permanent commitment

Completed groups can make global context stale inside a long unfinished patch. Scratchpad Patching pools only the observed partial patch, runs the trunk, broadcasts the result, and overwrites transient state rather than committing another persistent patch. Training masks let each scratchpad attend to itself and earlier committed patches but not to other scratchpads, making old transient entries discardable without a hidden dependency chain ([BIW-0076](../03_reading/R05/BIW-0076.md), arXiv:2605.09630v1 §3).

At p=16, scratchpads raise average NLU from 48.0 to 54.2, near a flat byte model's 54.1, while the validation-FLOP saving factor shrinks from 5.7× to 2.9×. Persistent cache can remain small even as extra work buys freshness. H-Net patchifier variants can regress under matched-training-FLOP comparisons, and dense refresh can be slightly worse on natural language (§§4–5/Appendix E). The mechanism separates permanent state count, transient workspace, and refresh frequency. It does not make global recomputation free.

For deployment, partial prompts and termination add further obligations: how an unfinished group is represented at prefill end, when a boundary becomes known, whether a generation step can flush it, and how cache state aligns after speculative rejection. Those details cannot be inferred from a training diagram. They are natural places where an otherwise valid grouped predictor needs an explicit serving contract.

<a id="s08"></a>
## 8. Output dependence and multi-byte generation

### 8.1 Four ways to represent a future block

A k-byte flat categorical head has up to 256^k outcomes. Several alternatives avoid that exponential enumeration but define different objects. Local autoregression factors a dependent joint into conditionals. Independent heads predict future offsets from the same prefix. Probabilistic circuits introduce tractable dependence through latent structure. Denoising models generate a noisy block through multiple conditional updates. Training several targets in parallel does not decide which of these laws, if any, will be sampled.

**Table 3. Output models and their generation obligations.**

| Output construction | Dependence represented | Generation work | What is not implied |
|---|---|---|---|
| Local autoregression | Each byte conditions on earlier emitted block bytes | Serial local decisions; amortized trunk | Independent parallel emission |
| Independent offset heads | Product of prefix-conditioned marginals | Parallel proposals; optional verification | A coherent correlated continuation |
| Circuit draft | Normalized latent mixture/HMM/tree dependence | Structured sampling and conditional queries | Correctness of a surrounding cache/rejection wrapper |
| Block denoising | Joint structure through iterative noisy-state updates | Multiple denoising evaluations | Ordinary byte-chain NLL or one-pass ancestral generation |
| Auxiliary future classifiers | Separate predictive targets | May be discarded at inference | Any executable multi-output sampler |
| Candidate dictionary | Whole-unit selection among compiled candidates | Candidate scoring/search | Unrestricted novel spelling outside the candidate set |

### 8.2 Local autoregression and patch-tail responsibility

MEGABYTE parameterizes a patch as the product of byte conditionals given prior patches and earlier local bytes. The local Transformer supplies dependence without an exponential block vocabulary; the large trunk runs at patch rate. Byte decisions remain serial locally. Patch-tail losses expose the burden shifted onto the smaller decoder, while cross-patch context and shifted scoring address different limitations. Its strongest quoted Table 8 scoring configuration uses four times basic scoring work, not a free single-pass improvement ([BIW-0008](../03_reading/R03/BIW-0008.md), arXiv:2305.07185v2 §§2.3–2.4/Table 8).

BLT's decoder cross-attends to patch states and fine encoder features, while SDD uses a local LSTM. Neither makes the patch a self-contained lossless text code. A summary can be useful for prediction while failing to reconstruct every constituent independently. The local interface is therefore part of the quality–cost trade, not an implementation afterthought after boundaries have been selected.

### 8.3 Independent futures and confidence emission

Deep self-attention already uses future-offset classifiers as training-only supervision. LCA deploys a more explicit multi-byte head: its ordinary next-byte head uses fine residuals, while its multi-byte Transformer receives repeated previous-segment latent information and segment-aware attention. Earlier hidden slots are not earlier sampled byte identities. Causal attention over those slots does not transform the candidates into an autoregressive byte joint. Weighted next-byte, multi-byte, and rate losses train approximately 373M-parameter systems on 50B FineWeb-Edu bytes ([BIW-0015](../03_reading/R05/BIW-0015.md), arXiv:2608.15454v2 §§2–4).

Its threshold policy emits the first next-byte output, then accepts a left-to-right candidate prefix above a confidence threshold. This is approximate bulk emission. Lowering the threshold raises acceptance and throughput while reducing task quality; increasing candidates from three to seven at τ=.75 reduces DailySum throughput from 210.42 to 164.18 bytes/s. The policy is useful as an explicit quality–speed choice, not as exact target-law sampling. Separate verification experiments preserve a named next-byte head or use an external FlexiTokens verifier; their reported 2.1–2.3× speedups explicitly drop KV caching and add a resident verifier (§6.3/Appendix B).

### 8.4 Dependent normalized drafts and their costs

MtPC parameterizes normalized categorical leaves, nonnegative normalized sums, and decomposable products from a context representation. Mixture, HMM, and tree factorizations coordinate future byte positions; smoothness and decomposability permit tractable marginals and conditionals for verification. This is genuine structured dependence, not merely multiple softmax heads. Its training uses discounted overlapping future windows, a composite likelihood rather than once-per-byte chain NLL ([BIW-0079](../03_reading/R05/BIW-0079.md), arXiv:2511.11346v2 §3/Appendices B–C).

The head can be large. A 16-byte rank-32 tree projection is about 730M parameters versus 21M for a factorized projection. On EvaByte/L40S, eight-byte factorized/CP-rank32/CP-rank128 drafts accept 5.19/5.88/6.02 bytes per cycle but produce 176.3/191.0/182.3 bytes/s. Higher rank improves acceptance and loses throughput. At sixteen bytes, HMM accepts more than BTree yet runs slower. These batch-one measurements exclude prefill and suppress EOS; head size, adapters, cache setup, and inherited byteification remain parts of the system (Table 1/Appendix K).

The optimized sampler has a distinct unresolved guarantee. Algorithm 3 specifies ordinary speculative residual correction, but shared-state Algorithm 2 describes discarding the final verifier token after acceptance without clearly distinguishing an all-accepted bonus from a post-rejection correction or retaining residual probability state. A literal discard-and-ordinary-restart interpretation need not preserve the stochastic target law. Exactness of that wrapper remains unverified; this is not a measured released-code bug and does not invalidate throughput. Normalization of the draft and correctness of an inner rejection identity cannot certify their optimized composition (v2 Appendix F pp.19–21, Algorithms 2–3; [CLAIM_RULES §3](../05_review/CLAIM_RULES.md#3-mtpc-exact-source-level-qualification-not-a-software-verdict)).

### 8.5 Denoising blocks and named reference models

Fast BLT combines an autoregressive path with masked denoising over future byte blocks. Block Diffusion is a subword-token comparator that denoises a current block conditional on clean completed blocks. Bidirectional attention within the noisy block is legal for that block-generative process, not left-to-right byte causality. Its objective is a sum of negative evidence lower bounds, and generation spends multiple denoising evaluations. More parallel positions do not imply one-pass exact sampling ([Fast BLT/BIW-0014](../../flued_multigranularity_survey_20261108/03_reading/B14/W0014.md), v1 §3; [BIW-0089](../03_reading/R05/BIW-0089.md), arXiv:2503.09573v3 §§3–5/Appendix B, as versioned in its card).

Verification must name its target. Fast BLT's greedy procedure preserves its corresponding autoregressive path, not necessarily the original BLT before denoising training. Blockwise Parallel Decoding's inserted branches can alter the primary scorer even when original weights are frozen. It preserves that scorer's greedy trajectory, not automatically an unmodified pretrained model. Sequence-level beam distillation reduces target variation and improves agreement, but adds teacher work. Top-k or forced-minimum-block acceptance changes the policy. Its subword translation peak is 3.3× wall-time speedup at k=8; k=10 accepts more and runs slower ([BIW-0082](../03_reading/R05/BIW-0082.md), arXiv:1811.03115v1 §§3–7/Figure 4).

### 8.6 Exact stochastic correction and its scope

For target p and actual proposal q at a fixed prefix, sample x from q and accept with min(1,p(x)/q(x)). Accepted mass is min(p,q); the normalized positive residual (p−q)+ restores missing target mass after rejection. An all-accepted branch may draw an ordinary target bonus. Temperature and top-p transformations must be included inside the actual p and q used by the ratio. The correctness identity is separate from assumptions used to estimate speed, such as independent acceptance rates ([Leviathan et al., BIW-0083](../03_reading/R04/BIW-0083.md), ICML 2023 Algorithm 1/Appendix A.1; [Chen et al., BIW-0084](../03_reading/R04/BIW-0084.md), Algorithm 2/Theorem 1).

This identity explains the distinction in §8.4: a post-rejection residual restores missing probability mass, whereas an all-accepted bonus is optional. Retaining an equivalent correction state can be valid; retaining only an accepted-prefix hidden state does not specify that correction. A worked finite-prefix example and the wrapper's closure requirements are in [OQ-12](OPEN_QUESTIONS_EN.md#oq12).

The output literature therefore separates four achievements: predictive supervision, dependent modeling, useful acceptance, and preserved target behavior. It is possible to succeed at one and not establish the others. The most informative studies report all four separately together with measured cost.

<a id="s09"></a>
## 9. Probability interfaces and comparable likelihoods

### 9.1 Define the event before normalizing its score

The apparent commonality of “bits per byte” can conceal different probability objects. A native causal byte chain scores successive bytes. A canonical token path scores one segmentation chosen by a tokenizer. A completed-string marginal sums compatible token sequences. A raw-prefix probability includes continuations crossing the observation boundary. A byte-plus-boundary model scores marked histories. A denoiser scores missing text conditioned on a corrupted full source. All can produce byte-normalized numbers, but the denominator does not make their numerators identical.

For matching scored events, let L be summed negative log probability in nats, N the effective number of labels averaged by a mean cross-entropy, and B the corresponding original-byte count. Then

\[
S_{\mathrm{bits/original\ byte}}=\frac{L}{B\ln 2}
=\frac{\overline{\mathrm{CE}}_{\mathrm{nats}}N}{B\ln 2}.
\]

If logs are already bits, division by ln 2 is unnecessary. N is not padded array length. Prompt exclusion, ignored labels, EOS, normalization, repeated targets, and overlapping windows affect the contract. Corpus-weighted scores should aggregate matching loss and byte totals, not silently average heterogeneous example ratios. Label-smoothed, auxiliary, composite-window, and denoising-bound losses require recovering their actual numerator before being called ordinary byte-chain NLL ([CLAIM_RULES §2](../05_review/CLAIM_RULES.md#2-units-probability-objects-and-normalization)).

Canonical-path scores are not forbidden. “Negative log probability of the canonical token path per original byte” is a legitimate transparent statistic. It simply does not claim marginalization over alternative decodings. Likewise, the lm1b conversion uses the same processed corpus's 826,189 byte events and 159,658 word events, including its newline/EOS conventions: word perplexity is 2 raised to BPB times their ratio. It reexpresses one score without recovering rare words already replaced by UNK ([BIW-0071](../03_reading/R09/BIW-0071.md), arXiv:1908.10322v1 §3.2/Table 1/Eq.3).

### 9.2 Completed-text marginalization

Cao and Rimell treat segmentation as a latent path for completed-text likelihood. A probabilistic tokenizer supplies a proposal; importance weighting and without-replacement stochastic beam search reduce wasted evaluations of concentrated paths. Dynamic programming can be exact for the tokenizer proposal without being exact summation of a context-sensitive neural LM. A probability-space importance estimate and its logarithm also have different bias properties. An n-best sum covers a lower bound on the nonnegative path sum, not necessarily the full string law ([BIW-0080](../03_reading/R04/BIW-0080.md), EMNLP 2021 §§2–4; [BIP-0109/0272–0273](../02_inventory/DETAILED_INVENTORY.md#BIP-0109)).

The study's document perplexity uses whitespace words, and its handling of differently tokenized Transformer-XL batches disables recurrence. It is not a native-byte architecture comparison or a fully specified arbitrary-UTF-8 termination experiment. Its value is methodological: one canonical decomposition can miss probability assigned to alternatives. The cost and estimator uncertainty of recovering those alternatives remain part of the proposed solution.

### 9.3 Arbitrary prefixes and canonical support

An unfinished raw-text prefix asks a different question. In the simple vocabulary A/B/AA under longest-prefix encoding, observing token A can imply that AA was not selected, whereas observing the raw prefix A does not exclude another A. The mismatch can persist under perfect training because the conditional events differ. Better learning can improve representations but cannot make two different queries identical ([BIW-0132](../03_reading/R04/BIW-0132.md), arXiv:2406.16829v2 §2.2/Figure 1).

Stable-boundary recursion and prefix covers sum compatible token histories, including tokens extending beyond the observed prefix. Exact Byte develops cover probability ratios and incremental reuse to reduce redundant LM calls. Its exactness refers to a compatible lossless canonical-support process. A generic neural softmax assigns mass to noncanonical token sequences; masking and renormalizing that mass changes the original distribution. It may improve likelihood under ground-truth-zero assumptions without being exact marginalization of every path of the unmodified neural model ([BIW-0088](../03_reading/R04/BIW-0088.md), arXiv:2410.09303v2 §4/Appendix A.6; [BIW-0132](../03_reading/R04/BIW-0132.md), Appendix G–H).

The engineering gain also has a precise scope. Fewer LM queries do not eliminate cover enumeration, vocabulary aggregation, tokenization validity tests, or retained cache states. A linear model-call argument is not automatically linear end-to-end wall time. Positive EOS probability at every finite prefix does not alone imply almost-sure termination, since hazards can shrink sufficiently fast. Finite-prefix identities and completed-sequence termination assumptions should be stated separately.

### 9.4 Vocabulary inclusion is a different causal question

“Tokenization bias” can refer either to prefix-event misuse or to a learned effect of vocabulary membership. Lesci et al. estimate the latter near a vocabulary merge-rank cutoff using regression discontinuity. They compare average contextual surface-span log probabilities under assumptions of local continuity, consistency, exogenous cutoff, adequate fitting, and sufficiently fine discrete rank. Excluding nested subwords reduces but does not prove absence of interference ([BIW-0133](../03_reading/R04/BIW-0133.md), ACL 2025 §§3–4/Appendices B–D).

The default 57M-nonembedding-parameter, 32K-BPE MiniPile experiment estimates +2.88 nats near the cutoff, approximately a 17.8-fold ratio of exponentiated mean log scores. That is not a guaranteed ratio for each word or a universal effect in large models. The study reports standard-error bands and bandwidth sensitivity, not a stated numerical confidence interval for the headline estimate. Larger model, corpus, and tying variants co-vary in some comparisons. This evidence challenges the claim that vocabulary membership never matters, but does not directly test native-byte superiority or show that every larger vocabulary improves language modeling.

The two questions are complementary. Prefix correction repairs what is being conditioned on; vocabulary-inclusion studies investigate how finite learning changes surface probabilities. They should not be counted as independent replications of one universal failure mechanism.

### 9.5 Marked histories and the TokSuite exception

*Breaking the Token Ceiling* retains teacher termination mass by emitting an end-of-token marker rather than discarding terminated alternatives inside a prefix. A marked byte process can preserve a conditional teacher event given marked history. Hiding markers then asks for a different marginal over latent boundary placements and token histories. The source's appendix does not show all caller-side expansion, but supplied inputs could already be expanded; missing preprocessing in a listing is not proof that implementation omits EOT ([BIW-0103](../03_reading/R06/BIW-0103.md), arXiv:2609.12303v1 §2.2/Appendix F).

TokSuite is a localized metric exception rather than an invitation to reject all tokenizer comparisons. V2 C.2 describes BPB using cross-entropy divided by log₂ vocabulary size, which is not a general conversion to bits per original byte. The wording is confirmed in PDF p.21, but the actual run-to-log-to-Figure 6 transformation remains unknown. Figure 6 is therefore not used here to certify equal cross-tokenizer BPB or equal training sufficiency. Separate option ranking and the four-tokenizer same-source-text control retain their own evidence. The additional exact-byte option evaluation is Gemma-tokenizer-only, forty examples taking hours, not fourteen-way exact scoring ([BIW-0051/BIP-0286](../02_inventory/DETAILED_INVENTORY.md#BIP-0286); [CLAIM_RULES §4](../05_review/CLAIM_RULES.md#4-toksuite-exclude-an-unverified-figure-inference-not-the-whole-study)).

**Table 4. Probability objects that should retain distinct names.**

| Object | What receives probability | Additional requirement for a stronger claim |
|---|---|---|
| Native byte chain | Successive byte events under a byte model | Explicit specials, termination, and scoring windows |
| Canonical path per byte | One selected token sequence | Sum compatible paths before calling it a text marginal |
| Completed-string marginal | All compatible terminated paths | Support, EOS, losslessness, and estimator accounting |
| Raw-prefix cover | Compatible histories crossing an unfinished prefix | Canonical-support/normalization assumptions and actual cover validity |
| Marked byte history | Bytes plus boundary or EOT events | Marginalize hidden markers before claiming an unmarked law |
| Denoising conditional/bound | Corrupted-source targets or variational objective | Recover the relevant sequence likelihood if that is the desired metric |
| Gold-option score | A supplied continuation under a stated scorer | Generated choice or answer accuracy must be measured separately |

<a id="s10"></a>
## 10. Sharing, readout geometry, and optimization

### 10.1 Why word-table arguments do not settle byte tying

Press and Wolf tie a word input table to the transpose of the output classifier. Lookup updates affect occurring input rows, while a full softmax ordinarily affects all output rows; tying joins the paths and saves storage. Their PTB large model changes from 66M parameters/78.4 perplexity to 51M/74.3. A regularized output projection helps some low-dropout settings but not their large dropout-regularized model, and tying worsens skip-gram similarity. This is background evidence for task-dependent reuse, not a controlled byte result ([BIW-0035](../03_reading/R08/BIW-0035.md), arXiv:1608.05859v3 §§2–4/Tables 2/5–8).

Inan et al. separate embedding-derived soft targets from table reuse. At 650 units, baseline/augmented-loss/reused-embedding/combined perplexity is 77.7/74.7/73.9/73.2. The soft targets come from the model's own geometry rather than an independently pretrained teacher. Their theory obtains a shared column space up to a basis transformation under restrictive assumptions; exact table equality is still an imposed constraint. This factorial comparison is useful because supervision and reuse can otherwise be conflated ([BIW-0036](../03_reading/R08/BIW-0036.md), arXiv:1611.01462v3 §§3–6/Appendices A–B).

The storage arithmetic changes with a small alphabet. Two independent V×d tables versus one differ by Vd parameters, excluding bias and bridging projections. At V=256 and d=2,048, the saving is 524,288 parameters. This analyst accounting is not a measured result; it explains why billion-parameter byte models need a stronger tying rationale than large-vocabulary table savings alone. Regularization, gradient coupling, and geometry can still matter, but they must be tested.

### 10.2 The documented sharing axes

**Table 5. Sharing is a named relationship, not a model-wide adjective.**

| Work or artifact | Supported relationship | Evidence level and limitation |
|---|---|---|
| ByT5 Large XNLI operative configuration | Encoder/decoder input shared; decoder input/output unshared | Mutable [operative gin](https://storage.googleapis.com/t5-data/pretrained_models/byt5/large/operative_config.gin) for XNLI fine-tuning initialized from a million-step checkpoint, not a pristine pretraining log; matched [Mesh definition pinned at 4758510](https://github.com/tensorflow/mesh/blob/4758510b99614c51ecb56166faff9842befac193/mesh_tensorflow/transformer/transformer.py); paper-runtime dependency revision and tensor aliases unverified, with no all-size/port generalization |
| MEGABYTE v2 Eqs.4/6 | Local byte lookup and output use the same named matrix | Paper specification; global/local blocks not thereby tied |
| TokSuite v2 §3.3 | Causal input/output tables untied, including byte-tokenizer arm | Not original ByT5 checkpoint architecture |
| Byte Language Models v1 Appendix A.4 | Input/output embeddings untied | Resolution-preserving hybrid backbone; not a tying ablation |
| LCA v2 §3 | Next-byte and multi-byte heads share one unembedding | Head-to-head, not established input-to-output tying |
| MtPC v2 §§3.3–3.4 | Lower representations shared; optional private draft adapters | Position/component readouts separate; original lexical tying unspecified |
| Reformer v2 §2 | Query and key projection shared | Attention axis, not lexical axis |
| ACT v6 §2 | Transition/output maps reused across internal steps | Within-position recurrence, not lexical tying |
| ELMo v2 §3.1 | Representation shared across directions; softmax shared across directions | Separate directional LSTMs; designated narrow extraction |
| BLT/H-Net unspecified lexical axes | Unknown in examined evidence | Family inheritance and small alphabet do not decide the switch |

The carrying paths are the [sharing register](../02_inventory/TAXONOMY.md#version--and-axis-specific-sharing-register-current), [MEGABYTE](../03_reading/R03/BIW-0008.md), [LCA](../03_reading/R05/BIW-0015.md), [MtPC](../03_reading/R05/BIW-0079.md), [Reformer](../03_reading/FIELD_ADDENDUM/arxiv_2001.04451v2.md), [ACT](../03_reading/FIELD_ADDENDUM/arxiv_1603.08983v6.md), and [ELMo](../03_reading/FIELD_ADDENDUM/arxiv_1802.05365v2.md). Paper specification, static configuration, fixed code, and run-linked tensor alias verification are distinct levels. No architecture observation here by itself estimates the causal effect of toggling tying.

For a shared table, the gradient is the sum of input- and output-path contributions. Their norms and curvature need not balance, especially after optimizer preconditioning. Background work reports early output-gradient norm share around 70% in its examined token runs. Multiplying input gradients by five changes alignment modestly and worsens WikiText-2 perplexity from 35.71 to 36.64 while downstream tasks move differently. Some pairs differ in data or size, and conditions use single runs. The finding motivates measuring path dynamics rather than assuming balance or automatically amplifying one path ([BIW-0037/W0366](../../flued_multigranularity_survey_20261108/03_reading/B14/W0366.md), arXiv:2603.26663v1 §§3–6/Appendix E).

### 10.3 Dot products, normalization, and confidence

Head formulas determine more than names. Ordinary logits wᵢᵀh mix row norm, hidden norm, and direction. Row-normalized wᵢᵀh/||wᵢ|| retains hidden magnitude as an example-dependent inverse temperature. Full cosine with scale s removes that channel unless it is reintroduced: s·wᵢᵀh/(||wᵢ||||h||). A distance-based classifier adds a class-dependent squared-norm term. Shared base parameters can therefore produce different effective input and output vectors.

The subword-translation study *Normalization of Input-output Shared Embeddings* calls its row-normalized output method cosine even though it does not normalize h. WMT16 English-to-German Transformer-big BLEU moves from 29.3 baseline to 29.9 with normalized input/output and 29.7 with the row-normalized readout. This is a useful background distinction, not an isolated byte-head mechanism ([BIW-0091](../03_reading/R08/BIW-0091.md), arXiv:2001.07885v2 §2.2/Eq.28/Tables 1–4).

An analyst bound clarifies the role of scaling. If every unscaled logit lies in [−1,1], maximum class probability is at most e²/(e²+V−1), approximately 2.8% for V=256. Learned scales or hidden norms change the bound. This does not diagnose a cited model: the selected nGPT material includes trainable class scales and remains partial background. It merely shows why “cosine head” without its normalization and scale is an incomplete specification ([BIP-0197](../02_inventory/DETAILED_INVENTORY.md#BIP-0197)).

Rank arguments require equally explicit dimensions. If a V×d classifier has full row rank and d≥V, arbitrary logit vectors are algebraically reachable by some h. Training a causal network to produce them is another matter. A large-vocabulary softmax bottleneck cannot be invoked unchanged without checking V and d. Conversely, a selected pseudo-inverse construction requiring ZᵀZ=I_d needs V≥d and cannot be transplanted unchanged to V=256,d>256. These are dimensional checks on partial background sources, not performance verdicts ([BIP-0192/0199](../02_inventory/DETAILED_INVENTORY.md#BIP-0192)).

### 10.4 An especially informative byte-specific control

*Neural Machine Translation without Embeddings* replaces learned byte tables with fixed one-hot input/output coordinates and separate scalar scales. Learned Transformer projections remain. Common coordinates are not shared trainable matrices, and the paper's d=512 softmax leaves some unused-coordinate/special handling insufficiently explicit for a precisely 256-way law. Initially the fixed representation improves 19 of 20 translation directions ([BIW-0068](../03_reading/R01/BIW-0068.md), NAACL 2021 §§2–6/Tables 2–4).

The apparent representation gain changes after controlling dropout semantics. Dropping a one-hot active coordinate erases the whole teacher-forced token; elementwise dropout on a dense embedding only removes part of its vector. Giving learned embeddings explicit decoder token dropout makes fixed bytes nearly tied out of English and 0.45 BLEU worse on average into English. The study identifies a training-recipe interaction, not intrinsic embedding-free superiority. It is a model example of an explanatory negative control: the intervention changes regularization as well as storage, and the control reveals which conclusion survives.

### 10.5 Auxiliary gradients and latent use

Multiple losses can disagree, but negative gradient cosine is not itself proof of negative transfer. Background PCGrad projects conflicting task gradients; gradient-similarity weighting gates auxiliary contributions using local agreement. Their nonlanguage and generic-task evidence does not validate them as repairs for every byte/rate/reconstruction system. Separate gradients and teachers add memory and work, and gating can underperform direct addition even with a useful auxiliary teacher ([PCGrad/BIW-0022](../../flued_multigranularity_survey_20261108/03_reading/B16/W0328.md), arXiv:2001.06782v4 §2/Appendix J; [BIW-0023](../../flued_multigranularity_survey_20261108/03_reading/B16/W0331.md), arXiv:1812.02224v2 §§3–6).

“Collapse” also needs a mathematical object. A sentence VAE can have posterior/prior KL near zero while a strong decoder ignores its stochastic latent. The partial background records cover KL schedules, word dropout, restricted decoder receptive fields, and extra inference-network updates. MANTa's one-block-per-byte degeneration is an allocation failure, not that posterior phenomenon; a deterministic residual bypass is not diagnosed by posterior KL. For deterministic byte hierarchies, withholding or changing the coarse state under a matched intervention is a more relevant utility test. Consumer-aligned reconstruction, such as preserving attention outputs, offers one way to define what a compressed state must do without requiring coordinate identity.

<a id="s11"></a>
## 11. Objectives, hybrids, and pretrained conversion

### 11.1 Objectives have different jobs

A next-byte loss trains local prediction. Span denoising trains conditional restoration from corrupted source. Rate losses discourage costly update patterns. Intermediate classifiers improve optimization depth. Future-offset losses encourage predictive representations. Geometry matching aligns lexical spaces. Distillation transfers conditional behavior. Reconstruction tests retention. The same label “auxiliary” hides these distinct jobs.

The deep self-attention ablations quantify this distinction. Text8 development loss rises from 1.062 to 1.158 without intermediate losses and to 2.482 without all-position supervision under the reused recipe, versus 1.068 without the extra future target. These are not equally retuned universal-necessity tests, but all-position training is plainly a stronger factor there than one extra future head. Training parameters are 235M versus 219M at inference, so discarded heads still cost training work ([BIW-0064](../03_reading/R09/BIW-0064.md), arXiv:1808.04444v2 §§2–3/Table 4).

The byte-simulation study separates several token-related advantages experimentally: n-gram input capacity, four-byte grouping curricula, boundary hints, repeated positional coordinates, loss normalization, and temporary subword targets. A four-byte stage exposes more raw context while suppressing three quarters of prediction targets and changing input composition. A lasting later benefit cannot be attributed solely to throughput. A temporary next-subword head remains worse near the end of the 1.7B run, while the smaller-model gap mostly closes. These are specific interventions, not evidence that every linguistic auxiliary or multi-byte objective helps or fails ([BIW-0108](../03_reading/R08/BIW-0108.md), arXiv:2604.27263v2 §§5.1–5.6/Figures 1–6).

AU-Net induces horizons through routing and expansion under ordinary byte supervision. In its three-stage setting, simple versus multi-linear expansion changes HellaSwag from 60.6 to 66.0. The expansion mechanism matters independently of whether an auxiliary word target exists ([BIW-0077](../03_reading/R10/BIW-0077.md), arXiv:2506.14761v1 Appendix C/Tables 4–5). These contrasts argue for classifying learning signals by the functional job and information they supply, not by whether they sound more semantic than bytes.

### 11.2 Type geometry versus contextual function

Char2Subword learns a character Transformer/max-pool composer to approximate mBERT embeddings using cosine, L2, neighborhood-distance, and identity losses. Perturbed spellings share target vectors. Dynamic MLM then trains the composer through a frozen contextual host and fixed subword classifier. A hybrid can keep old embeddings for recognized words and compose unseen ones. Static vector imitation is one stage; contextual training changes neighborhood fidelity, and re-approximation can matter. Retained lookup storage and composition work remain ([BIW-0122](../03_reading/R06/BIW-0122.md), arXiv:2010.12730v3 §3/Tables 2–5).

This exposes an important transfer distinction. Two vectors can be close under an embedding metric while causing different downstream activations. Conversely, preserving one task can tolerate substantial vector changes. Character perturbations can improve robustness yet erase cross-language distinctions if augmentation maps different forms to the same target. The host's geometry, contextual computation, and task behavior must therefore be evaluated separately.

Zero-Shot Tokenizer Transfer amortizes table construction with a hypernetwork. A small Transformer composes a target token's decomposition under the original tokenizer and predicts input and, if needed, separate output embeddings. Training samples vocabularies through a frozen host; tables can then be generated once for a new tokenizer. Zero-shot means no target-tokenizer-specific adaptation, not no hypernetwork training. The untied GPT-2 condition diverges without an embedding anchor while the tied condition does not, a recipe-specific stabilization result rather than a universal tying law ([BIW-0126](../03_reading/R06/BIW-0126.md), arXiv:2405.07883v2 §§2–4/Appendix B).

### 11.3 Byteification changes the input geometry and clock

Bolmo attaches local recurrent modules to a pretrained Olmo backbone, retains a subword-suffix input table, and learns byte-plus-boundary outputs. Stage one aligns representations after four frozen host layers, imitates teacher boundaries, matches patch probabilities, and includes byte CE; stage two unfreezes the model. Passing gradients through frozen layers tests functional compatibility beyond input-vector matching. Equal local/global widths avoid a hard rank ceiling from narrow linear up-projection, but that algebra does not isolate rank as the cause of all empirical differences ([BIW-0097](../03_reading/R06/BIW-0097.md), arXiv:2512.15586v2 §3/Appendix E).

Its stage-two-only control is not catastrophic. Extra global compute narrows the gap, especially at larger scale, so alignment is helpful without being universally necessary. Conversion exposure is approximately 43.1B plus 172.9B bytes, additional to inherited pretraining. Frozen parameters still require backward-to-input computation through aligned layers. Trainable parameter count is not the training-work budget (§6.2/Figure 6/Tables 7–8).

*Distilling Token-Trained Models into Byte-Level Models* uses a different curriculum: align token-final encoder states to teacher embeddings, distill teacher-token distributions, train a router, then replace the token head and train a byte decoder before full unfreezing. Its first stage still emits teacher-vocabulary tokens. Under the equal-20B-byte comparison, staged alignment versus direct distillation gives LAMBADA 70.7 versus 31.2 and HellaSwag 73.6 versus 46.7. The severe failure belongs to that configuration; Bolmo's different control prevents turning it into a universal requirement ([BIW-0098](../03_reading/R06/BIW-0098.md), arXiv:2602.01007v1 §§4/6.1/Table 3).

Prefill and generation expose a timing problem. Adjacent observed states can define a boundary during prefill, but a generator cannot inspect the true next byte. Joint byte/boundary prediction supplies 512 classes; another variant uses a predicted second-byte embedding as a proxy. The latter is not actual lookahead or exact verification. Qwen JBP versus MBP gives GSM8K 53.5 versus 37.4 but MMLU 68.4 versus 69.2, showing task-dependent trade-offs rather than general failure of multi-byte methods (source §4.1/Table 4).

### 11.4 Bytes as a common supervision language

Cross-tokenizer distillation maps teacher probability into byte-prefix events and trains temporary position-specific student byte heads alongside token loss. Ordinary deployment keeps student tokens and removes those heads. The ten parallel heads do not condition on earlier sampled within-token bytes, so they are not an exact sequential byte decoder. Teacher cover probabilities use beam/pruning approximations. In the separate actual token-to-byte conversion, instruction following and MMLU deteriorate markedly: original versus BLD MMLU is 60.50 versus 39.06 and IFEval 66.31 versus 25.43 ([BIW-0099](../03_reading/R06/BIW-0099.md), arXiv:2604.07466v1 §3/Tables 1–3).

The same method can improve some cross-tokenizer cells, such as GSM8K versus SFT, while losing on MATH. Its approximate teacher precomputation is about 10.4 seconds per 100–150-byte sample on four RTX 3090s and about two days for the reported Tulu operation. That is offline teacher cost, not student latency. Source disagreement over LoRA modules and 260 versus 261 output classes remains unresolved at the run level; it does not erase the separately reported comparisons. A common alphabet enables a training bridge without guaranteeing retained instruction behavior or a universal exact teacher law.

*Breaking the Token Ceiling* compares dense token, byte, and marked-byte students using converted teacher targets. At about 1.8×10^21 FLOPs, the byte arms have lower validation BPB yet worse downstream results than token-supervised training. The advertised larger asymptotic marked-byte gain is a fit-sensitive extrapolation, not an observed four-point maximum-checkpoint gain. The observed comparison is 44.6 versus 44.4 in the cited maximum setting. Markers add about 30.94% FLOPs per source token under its convention; top-logit storage and teacher queries are additional lifecycle costs ([BIW-0103](../03_reading/R06/BIW-0103.md), arXiv:2609.12303v1 §§3–6/Appendices D–G).

### 11.5 Hybrid output can remain finite

T-FREE removes a learned subword vocabulary but uses rule-based complete units, padded trigram hashes, binary feature accumulation, and candidate-dictionary scoring. Multi-label BCE is not a normalized word softmax. Hashing an unseen input word does not permit unrestricted generation outside the compiled candidate set. The paper describes 500K common training words plus prompt additions in one regime and an 80K-English/20K-German evaluation dictionary in another ([BIW-0127](../03_reading/R10/BIW-0127.md), arXiv:2406.19223v2 §§3.1–3.2/4.1/Algorithms 1–5).

Its stated binary trigram set is also not universally injective. Under the padded distinct-trigram rule, `aaaa` and `aaaaa` have the same set `{_aa, aaa, aa_}`, even without hash collisions. This is analyst reasoning about the representation, not measured benchmark harm or a released-software collision. Length features or different runtime handling would require artifact evidence. The architecture is best understood as a sparse lexical hybrid, not native next-byte prediction and not proof that vocabulary concerns have disappeared.

Hybridization can occur at input, internal clock, targets, teachers, or output support. The important question is not whether a model deserves a pure label, but which dependencies it removes, which it retains, and whether the retained resources are included in the comparison.

<a id="s12"></a>
## 12. Multilingual allocation, robustness, and competence

### 12.1 Universal coverage does not equal equal context

Byte interfaces remove unknown-symbol dependence on a learned inventory, but UTF-8 length varies with script and parallel text length varies with language and translation. Petrov et al.'s FLORES comparison gives Shan/English ratios of 3.94 in bytes and 1.42 in code points; Cantonese/English is 0.87 and 0.31. Neither representation equalizes position consumption. These are ratios for parallel translations, not intrinsic measures of linguistic complexity. An UNK-heavy tokenizer can appear short by discarding information, so retention must accompany length ([BIW-0033/W0361](../../flued_multigranularity_survey_20261108/03_reading/B14/W0361.md), v2 §§3–4/Table 5).

The practical question is how many useful original-text units a finite context and compute budget provides to each population. Byte length, scalar length, grapheme length, and task-relevant semantic content are different normalizations. A model can shorten every language in absolute positions yet increase an unsupported language's relative disadvantage. Conversely, a longer encoding can preserve distinctions that an apparently efficient normalizer removes. Length parity is a resource diagnostic, not task fairness itself.

### 12.2 Changing encoding, morphology codes, or internal rates

Universal Byte-Level Encoding routes scalar values between disjoint UTF-8 and UTF-16LE alphabets before BPE. It changes base-code overhead while the LM still predicts merged subwords. At 32K vocabulary, one reported configuration shortens 189 of 204 language–script configurations, but Tibetan and Shan provide exceptions elsewhere. Three-seed LM means are 1.4900 for UBE versus 1.4854 BPB for ordinary byte BPE. Shorter representation is not a universal quality improvement; the equal-text comparison addresses a different exposure control from equal steps ([BIW-0031/W0359](../../flued_multigranularity_survey_20261108/03_reading/B14/W0359.md), v2 §3/Tables D.1/D.2/E.8/F.5).

MYTE uses language-specific Morfessor resources, recurrent morph-like strings, and variable-length codes followed by ByT5-style denoising. Morfessor segmentation, code construction, and neural learning have separate roles; these code bytes are not raw UTF-8 or jointly learned neural boundaries. Seen low-resource non-Latin mean length falls from 305 UTF-8 units to 145 code units, versus English 131 to 109. Unseen-script Ol Chiki Santali stays 365 to 365, while its English-relative ratio worsens from 2.80 to 3.35 because English compresses. This is a concrete allocation counterexample, not an absolute length increase for Santali ([BIW-0104](../03_reading/R07/BIW-0104.md), arXiv:2403.10691v2 §3/Table 2/Appendix A).

Task results are mixed. Main Table 4 gives ByT5→MyT5 QA 73.2→75.3 F1, NER 81.5→80.8, semantic parsing 25.1→19.6 exact match, and low-resource MT 20.1→20.4 chrF. Appendix Table 8 instead reports **MyT5 low-resource/overall means 21.1/21.8 versus ByT5 21.9/23.1**, both favoring ByT5. The tables' population/aggregation relationship is unreconciled; Table 8's fifteen language columns include Maltese and Shona, while C.2 lists fourteen names including Marathi and omitting Shona. A single reconciled MT ranking cannot be fabricated from them ([current row/column adjudication](../05_review/CLAIM_RULES.md#5-myte-explicitly-anchor-both-model-row-and-aggregate-column)).

MYTE's loss denominator is parallel English UTF-8 length, including its +1 convention, not target-language bytes. A missing minus sign and unspecified log base leave a scoring-contract question, not evidence that software computed negative surprisal. Equal 250K steps also do not match original-text exposure, preprocessing, or FLOPs, and original-byte reversibility after normalization is not established. These local limits do not negate the observed code-length gains; they identify which utility and probability claims are still separate.

MAGNET changes internal rate rather than the external encoding. A small Transformer, Gumbel choices, per-script binomial priors, segment means, repeated expansion, and byte skips allocate grouped positions. Across nine languages in three script groups, XQUAD mean 44.62 for bytes is essentially matched by 44.61 at one setting. Aggressive compression gives 41.06, with larger subgroup losses: Hindi 29.18→21.23 and Telugu SIB 68.63→53.90. Its whole-sequence script selector assumes one script, leaving general mixed-script streaming unresolved ([BIW-0045/W0510](../../flued_multigranularity_survey_20261108/03_reading/B26/W0510.md), v2 §§2–5/Table 3/Appendix D).

These three interventions target different causes of length. Alternate base coding changes storage units; morphology coding uses resource-derived recurrent forms; internal rate changes expensive positions without recoding the external text. Their downstream quality–cost curves and worst-group outcomes are more informative than treating them as interchangeable fairness remedies.

### 12.3 Data imbalance and annotation opportunity

Tokenizer-training imbalance and model-training imbalance are distinct interventions. The AMTA study varies them separately. Byte fallback eliminates unknowns but does not reliably prevent translation collapse. Adding held-out characters rescues one Chinese condition but not Tamil. Coverage can remove a representational obstruction while the learned model remains poorly supported by its sampling distribution ([BIW-0107](../03_reading/R07/BIW-0107.md), AMTA 2022 §§3–4/Figures 7/10/Table 3).

Endangered-language byte NMT combines one-hot inputs, a shared multilingual Transformer, high-resource pretraining, and fine-tuning. Several Indigenous-language directions improve, while some high-resource directions regress. Byte-permutation ensembles average inverse-aligned probabilities from independent models; those gains do not establish typo robustness, and an ordinary same-encoding ensemble is not present as a matched control ([BIW-0106](../03_reading/R07/BIW-0106.md), COLING 2022 §§3–5/Figures 5–6). Interface, transfer exposure, and ensemble diversity should remain separate explanations.

XTREME-UP foregrounds realistically scarce in-language annotation rather than only zero-shot behavior. Reported task averages favor ByT5 over mT5 on transliteration CER, 14.6 versus 37.6, and semantic-parsing exact match, 37.5 versus 21.8. Preliminary autocomplete includes Belarusian, Greek, Hebrew, and Uyghur reversals; OCR uses an identical external baseline. Estimated eight-hour annotation budgets exclude some development work. Total benchmark languages, baseline pairs, and task-specific evaluation subsets have different denominators; the 70-underrepresented-language benchmark versus prose's 39-language evaluation is insufficiently reconciled, not evidence that all seventy baseline evaluations occurred or that the benchmark only contains thirty-nine ([BIW-0105](../03_reading/R07/BIW-0105.md), arXiv:2305.11938v2 Table 4/Appendix B; [R1 §3](../05_review/FULL_READING_AUDIT_R1.md)).

A multidimensional understanding evaluation finds mBERT strong with scarce labels and a longer-tuned TyDi baseline overtaking CANINE on average. Task and language rankings vary. Annotation quantity and baseline tuning are therefore part of the interface comparison, not downstream details to hold outside its interpretation ([BIW-0032/W0360](../../flued_multigranularity_survey_20261108/03_reading/B08/W0360.md), formal §§3–4/Appendix Tables 4–7).

### 12.4 Dialects and task-dependent associations

The dialect study defines tokenization parity as a language/English length ratio and information parity as an English/language total-NLL ratio. Neither is task accuracy or fairness. Appendix F Table 8 gives dialect-identification TP correlations +0.638 for Phi, +0.4836 for mBERT, and −0.380 for Llama. DI information parity is −0.413 for Phi and +0.268 for Llama. Topic classification and extractive QA have different patterns ([BIW-0134](../03_reading/R10/BIW-0134.md), EMNLP 2025 §§3–5/Appendix F Table 8).

The later positive Llama sentence follows IP discussion and can refer to +0.268; it does not unambiguously contradict the negative TP column. Effective paired sample sizes and significance are not reported for those cells. Full encoder tuning and four-bit low-rank decoder adaptation also differ in resources and permissions. The associations do not isolate a causal fragmentation effect, and Latin-looking displays of mapped bytes do not prove irreversible Unicode corruption: decoding can reassemble proper text ([CLAIM_RULES §7](../05_review/CLAIM_RULES.md#7-new-r10-clarification-do-not-manufacture-a-dialect-tp-prose-contradiction)).

A field account should retain the interesting model/task-dependent signs without inventing a universal direction. Finer fragmentation might aid surface discrimination under some conditions, but pretraining, task supervision, model class, and tuning remain alternative causes. Fairness requires an explicit outcome and population, not a desired sign in a length correlation.

### 12.5 Noise: access, invariance, and learned coverage

Character access does not supply robustness by itself. Belinkov and Bisk show degradation in character-to-character, character-composed word, and BPE translation. German clean→natural BLEU falls 34.79→14.02 for charCNN and 29.97→12.68 for char2char. “Natural” noise is reconstructed from edit lexicons and inserted into clean parallel text, not an untouched naturally noisy parallel corpus ([BIW-0109](../03_reading/R07/BIW-0109.md), arXiv:1711.02173v2 §§3–4/Table 3, as fixed in the card).

The remedies trade different information. Mean character vectors impose scrambling invariance but discard order and reduce clean quality. Mixed random/keyboard/natural training gives German clean/random/keyboard/natural BLEU 31.29/30.04/29.81/31.60. Natural-only training can excel on its own corruption and fail on unseen types. The mixture is one training distribution, not an inference ensemble. An external spelling corrector helps German and worsens Czech (source §6/Tables 6–7).

ByT5 supplies later positive denoising-based evidence, especially for case perturbations. CharacterBERT and Char2Subword offer hybrid alternatives with task-specific noise training. TokSuite's multiple-choice perturbations reveal variation among byte-related systems, and NFKC can remove style perturbations before the model sees them while breaking original-string preservation. A pipeline's apparent invariance can arise from destroying distinctions rather than learning to reason through them. The useful benchmark therefore reports clean quality, actual corruption process, severity, and authorized equivalences together.

### 12.6 Valid Unicode, intended characters, and exact strings

*Beyond Perplexity* examines a 355M, 8K-BPE-plus-byte-fallback model, not a pure-byte model. Common-character partial progress is 96.21% but strict validity 50.47%; intended-character accuracy is a further outcome. Prefix offsets change how many bytes remain, entangling scalar length and completion difficulty with frequency. Continuation syntax alone cannot establish a legal scalar ([BIW-0044/W0509](../../flued_multigranularity_survey_20261108/03_reading/B22/W0509.md), v2 §§3–5/Appendices E–H).

Strict raw-stream validation should precede repair. Invalid-byte-ignore decoding can hide failures by dropping bytes; buffering an unfinished scalar during streaming is not itself malformed output. Report complete legality, incomplete termination, repaired display, intended scalar, and task answer separately. NFC/NFD equivalence can be appropriate for semantic text, while exact identifiers may require original bytes. NFKC/NFKD may erase stylistic or mathematical distinctions. A user-facing span beginning inside a grapheme can be an unsuitable boundary even if its byte offset is syntactically valid.

The metric must follow the task. Exact copy needs exact original text; transliteration may accept a defined normalized output; editing and position tasks need a specified indexing unit. Combining marks, emoji sequences, Indic clusters, and non-BMP scalars belong in the evaluation domain rather than being dismissed as exotic exceptions to an ASCII definition of character.

### 12.7 Recoverable spelling and usable character skills

SpellingBee trains an external character decoder on frozen token embeddings. Random-vector controls fail exact match, while similarity and lemma filtering lower trained-model scores: GPT-2-medium drops from 32.9% to 16.5% under the strongest filtering. This is recoverable orthography, not the host naturally executing a spelling instruction. A separate initialization intervention raises spelling-probe exact match to 93.5%, yet masked-LM losses differ by less than 0.01 after 1,000 updates in the reported run ([BIW-0110](../03_reading/R10/BIW-0110.md), NAACL 2022 §§2–3/Table 1 and §5/Figure 2).

The Strawberry study instead adds a character Transformer with block-causal cross-attention while retaining subword output. Explicit access accelerates supervised synthetic transformations, but the onset threshold is above **0.5%**, not 50% mastery, and Wikipedia editing remains only a few percent exact match at the plotted endpoint. Access can change learning speed without solving natural character competence ([BIW-0113](../03_reading/R10/BIW-0113.md), EMNLP 2025 §§3–4/Figures 3–7/Table 2).

CharBench separates frequency count, unique count, first position, and last position. Across seven prompted subword LMs, averages are 77.34%, 47.96%, 43.64%, and 32.37%. Correlations with target-token length differ by model and task; word length, segmentation, and answer magnitude covary. Undocumented guessing floors and malformed-output handling cannot be inferred. These English string tasks do not certify multilingual grapheme competence ([BIW-0114](../03_reading/R07/BIW-0114.md), proceedings Tables 1–3 and separately scoped v3 appendices).

Numeracy adds algorithmic requirements beyond digit visibility: place alignment, carry propagation, and answer formatting. The selected partial arithmetic record motivates grouping direction but does not support a native-byte superiority claim. Non-ASCII decimal digits and locale-specific separators remain thin evidence. A good protocol separates exact transcription from numerical correctness and varies carry length and grouping alignment under explicit equivalences ([BIW-0111/BIP-0231](../02_inventory/DETAILED_INVENTORY.md#BIP-0231)).

### 12.8 Long exact copy and delayed queries

Average next-byte loss can hide a wrong accent, missing mark, or changed digit that invalidates a long identifier. Attention on a source phrase is not generated whole-string exact match; the short ASCII attention analysis in the recent byte-scaling study is a diagnostic, not a copy benchmark ([BIW-0028/BIP-0053](../02_inventory/DETAILED_INVENTORY.md#BIP-0053)).

*Repeat After Me* gives a capacity distinction under an explicit read/answer protocol. A uniform length-L input over D symbols is read completely before copying begins, and every input-dependent influence on subsequent deterministic output is contained in a retained state from a finite distinguishable set S. The protocol permits no source replay, external cache, earlier input-dependent output stream, or other side channel outside that counted state. Each retained state determines at most one correct answer, so whole-string success is at most min(1, |S|/D^L). Writing b=log₂|S|, success at least 1−ε requires b≥L log₂D+log₂(1−ε), for 0≤ε<1. Online echoing while reading is a different protocol; any retained source/cache must be counted, and larger state changes the capacity available. The uniform-string result is not a natural-language impossibility claim. Query-before ingestion can permit filtering that a delayed query cannot ([BIW-0021/W0061](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md), arXiv:2402.01032v2 §§2.1/2.3, Appendix D, §3.5).

The useful consequence is an evaluation design, not a declaration that recurrence always fails. Vary source length, dependency distance, distractors, query timing, and internal-boundary positions. Include random capacity stress and redundant natural multilingual text. Require generated exact outputs and source-substitution controls. Access to a relevant state is an architectural precondition; trained use of it remains an empirical question.

<a id="s13"></a>
## 13. Compute, data exposure, and serving

### 13.1 A resource vector instead of a single budget

Different controls answer different questions. Equal positions studies learning per model step but changes original-text exposure. Equal retained text controls information exposure but changes positions and work. Equal parameters can redistribute a large lexical table into contextual layers. Equal training FLOPs permits different data and model sizes. Equal wall time depends on implementation and hardware. Matched-quality serving permits architecture-specific operating points. None is inherently the only fair comparison; all must be labeled.

A useful resource vector includes retained original text, unique and repeated exposure, original-text context, model positions, realized group-rate distribution, total/trunk/local/head parameters, training-only modules, estimated operations, measured time, and teacher/preprocessing costs. At inference add prefill, output length, persistent cache, transient workspace, resident drafter/verifier, precision, device, batch, concurrency, and quality. Unknown components remain unknown rather than zero.

This framework explains apparently conflicting results. Byte models may be parameter-efficient because vocabulary tables shrink, but compute-inefficient because every original string produces more positions. An irregular hierarchy may reduce operation counts but map poorly to accelerators. A faster training step may process less retained text. More accepted outputs can lose throughput because the head or verification is expensive. These are informative reversals, not contradictions to be averaged away.

### 13.2 Scaling fits and their parameter conventions

*Compute Optimal Tokenization* sweeps compression, model size, and byte exposure across 988 latent and 320 subword models, approximately 50M–6.7B parameters, 4B–1.1T training bytes, and 5×10^18–2×10^21 FLOPs. Its fitted English optimum near 10^20 FLOPs is about 3.7 bytes per global patch and about 60 training bytes per global parameter under the paper's convention. In the first scaling law, N excludes the local encoder/decoder and input/output embedding parameters (§3.1/Appendix B.1); the reported total-training-FLOP comparison nevertheless includes local modules and embeddings (§2.2/Appendix B.2). This fitted N is not whole-resident parameter storage, while entropy-model pretraining and scoring remain outside a fully itemized lifecycle budget ([BIW-0047](../03_reading/R05/BIW-0047.md), arXiv:2605.01188v2 §§2–3/Appendices A–F).

Loss is nonmonotonic in compression. The fitted optimum shifts from 3.69 bytes/patch at 10^20 FLOPs to 3.33 at 2×10^21. At approximately 2.1×10^9 inference FLOPs/byte, a 3.3B model at length four gives HellaSwag 74.1% versus 68.2% for 6.7B at length eight, while task rankings differ on ARC-Easy and ARC-Challenge. Training-optimal compression and deployment task choice need not coincide. These are operation-based operating points, not measured latency curves.

The recent *Byte Language Models* result provides a sharper frontier reversal. Its resolution-preserving backbone is a **3:1 Gated DeltaNet/Gated Softmax Attention hybrid**, not an all-attention Transformer. Bytes lead on its fitted same-parameter frontier, while subwords lead on tested training-FLOP frontiers. The recipe also changes local convolution width, adds hashed n-grams, and begins with four-byte mean-input/bag prediction. Its fitted N includes output but excludes input/hash tables; lookup/hash, averaging, loss, and optimizer operations are excluded from the stated compute convention. “Flat” means no explicit local–global–local hierarchy, not identical per-position operation type ([BIW-0028/W0356](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md), arXiv:2610.05978v1 §§2–4/Appendices A–C).

These studies justify conditional scaling conclusions. They do not supply a whole-resident-memory comparison, a wall-time theorem, or a controlled attribution to alphabet alone. Extrapolated gains should remain separate from observed checkpoints, as the marked-byte distillation results also demonstrate.

### 13.3 Retained text, packing, and tokenizer selection

A common source mixture need not give equal realized exposure. *Language-Specific Effects* reports discarding 30.4–43.5% of sampled text depending on tokenizer and language, and repetition versus one-pass conditions can change rankings; Chinese rank correlation reaches −.11 in one reported comparison. Downstream tasks near chance cannot support strong capability-equivalence conclusions. Retention and repetition must be counted after packing and filtering, not inferred from the sampling recipe ([BIW-0050/W0516](../../flued_multigranularity_survey_20261108/03_reading/B22/W0516.md), arXiv:2610.12144v1 Appendix A.4/§§5–7).

TokSuite's same-source-text control reconstructs a stream for four tokenizer arms but changes token exposure substantially: about 104.86B Llama, 114.89B Qwen, 100.23B Gemma, and 169.80B Comma. It excludes the byte arm and is not equal-step/equal-FLOP evidence. Its value as an exposure control survives the separate unresolved Figure 6 computation. A survey should preserve that control without using it to claim more than it matched ([BIW-0051](../02_inventory/WORK_CATALOG.md#BIW-0051), v2 §3/Appendices C/E–G).

Tokenizer selection is itself expensive. *Beyond Text Compression* tests six tokenizers on smaller/larger backbones and uses distributional features with logistic regression, calibrated SVMs, and Bradley–Terry ranking. Cross-scale Kendall τ is .33 for multiple choice, −.07 for summarization, and .87 for multilingual translation. Small-model ranking transfer is task-dependent, and none of the arms is a pure-byte LM. Nominal size classes vary in total parameters because vocabulary tables vary, while the common source subset is defined by GPT-2-token count, not equal tokens under each tokenizer ([BIW-0049](../03_reading/R08/BIW-0049.md), ACL 2025 §5/Tables 1/3/5/6/Appendix A).

*Tokenization Is More Than Compression* supplies a direct counterexample to minimum-length sufficiency. With 40,960 pieces, no-pretokenization PathPieceR yields 1.26B corpus tokens and 44.0% English multiple-choice average versus BPE merge's 1.49B and 50.0%. On the same BPE vocabulary, merge/greedy/PathPieceL gives 50.0/49.1/46.7%. Vocabulary construction, pretokenization, and inference segmentation have distinct effects. Equal model-token training still changes original text and compute; rank reversals across scales are not universal laws ([BIW-0131](../03_reading/R08/BIW-0131.md), EMNLP 2024 §§4–6/Appendices E–G).

The correct synthesis is not that compression is irrelevant. Fewer positions can be a major resource benefit, but token count alone is an incomplete quality proxy. Statistical proxy models can reduce search cost while retaining limited transfer populations and uncertainty.

### 13.4 Whole-lifecycle teacher and adaptation accounting

Teacher use has several locations. CANINE-S discards a subword classifier after training. BLT needs its entropy model online, even if training patch decisions are precomputed. Bolmo's alternative boundary experiments use a 370M auxiliary LM trained on 74.3B tokens for training-time entropy/cross-entropy merges rather than online inference. Scratchpad Patching runs an entropy trigger at deployment and trains an auxiliary model with a stopped-gradient boundary. These are distinct lifecycle placements, not a binary teacher/no-teacher property.

Conversion systems inherit a source checkpoint, then spend adaptation text, teacher forwards, backward-to-input passes, and possibly saved distributions. A frozen backbone is not free if gradients must traverse it. Logit storage is not just student parameter count. Sequence-level distillation adds teacher beam generation; hypernetworks add their own training across vocabularies. The relevant budget depends on the deployment question: amortized conversion for an existing checkpoint, from-scratch training, or repeated tokenizer transfer. A claim that one deployment is compact can be true while its total learning lifecycle is expensive.

### 13.5 Measured speed versus useful proxies

**Table 6. Representative efficiency observations and the quantities they actually measure.**

| Study | Reported observation | Interpretation that survives its conditions |
|---|---|---|
| ByT5 | About .75× mT5 pretraining throughput: Table 9, TPUv3-64; 6.4–9.5× XNLI inference slowdown: Table 10, TPUv3-32 | Position/exposure and task-specific cost; XNLI is not NER or evidence of a long-output-only cause; Table 10's XSum instead uses TPUv3-128 |
| MANTa | 2.61 versus 9.06 byte-T5 and 1.13 subword-T5 seconds/step | Encoder training-update time on 16 V100s, not decode latency |
| MEGABYTE | 8,192 bytes: 132→93 seconds | About 29.5% less elapsed time or 1.42× rate; models/contexts differ and timing setup is incomplete |
| H-Net | Dynamic implementation can train about twice as slowly as isotropic control | Irregular execution can reverse FLOP expectations |
| Scratchpad Patching | p=16 NLU 48.0→54.2; FLOP saving 5.7×→2.9× | Freshness buys quality with transient work despite small persistent cache |
| LCA | Three→seven candidates can lower 210.42→164.18 bytes/s | Acceptance/candidate count is not throughput; separate external-verifier gains are uncached |
| MtPC | Rank32→128 accepts 5.88→6.02 but slows 191.0→182.3 bytes/s | Head/sampling cost matters; batch one, prefill excluded, EOS suppressed |
| Transformer-XL | Up to 1,874× evaluation ratio in cited setting | Reuse versus uncached full-window rescoring, not modern batched serving |
| Bolmo 7B | About 125 versus 150 bytes/s at source-model compression; crossover near 6.6 bytes/patch | H100 batch-one operating points with quality trade-offs, not universal serving superiority |

Sources: [ByT5](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md), [MANTa](../03_reading/R01/BIW-0006.md), [MEGABYTE](../03_reading/R03/BIW-0008.md), [H-Net](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md), [scratchpads](../03_reading/R05/BIW-0076.md), [LCA](../03_reading/R05/BIW-0015.md), [MtPC](../03_reading/R05/BIW-0079.md), [Transformer-XL](../03_reading/R09/BIW-0119.md), [Bolmo](../03_reading/R06/BIW-0097.md), at the sections cited above.

Training bytes/s, accepted positions, weight-loading estimates, synthetic attention timing, and ponder counts are useful diagnostics. They are not end-to-end serving measurements. First byte is also not first complete scalar, and a scalar is not necessarily a stable displayed grapheme. Bursty multi-byte output can change latency distribution independently of mean byte rate. Modern comparisons need prefill, partial prompts, EOS, buffering, concurrency, peak memory, and tail latency at matched quality. The corpus remains thin on that combined contract.

<a id="s14"></a>
## 14. A consolidated problem–solution–technique taxonomy

### 14.1 Parent questions and overlapping mechanisms

The canonical inventory has twelve manual overlapping families, not learned clusters. Their purpose is to retain several relevant labels per record. The larger hierarchy asks six parent questions: representation, useful composition, computation placement, information/output law, learning/parameterization, and evidence of utility. These editorial parents do not create a new independent-problem census. The complete [classification essay](CLASSIFICATION_EN.md) also provides thirteen disjoint navigation routes covering all records exactly once; that reading partition is not a replacement for the overlapping scientific relationships.

**Table 7. Problem families, one-sentence strategies, and researcher-used techniques.**

| Parent question / canonical family | One-sentence solution strategy | Techniques and exact roles | Representative evidence and counterexample |
|---|---|---|---|
| What can be represented? C01 | Change the alphabet, code, or fallback to cover the declared domain. | Hash embeddings bound storage; byte bases supply fallback; standards define legality/equivalence. | CANINE collisions; GPT-2 merged positions; legal bytes do not imply correct text. |
| How are fine symbols composed? C02 | Build local features or aggregate contextual information before expensive processing. | CNN/highway, recurrence, means, concatenation, cross-attention, endpoint selection. | Character-aware LM's MLP negative; DTP/H-Net aggregation differences. |
| What chooses groups? C03 | Fix, teach, or learn boundaries with a distinct rate constraint. | Rules, external tokenizers, Gumbel/straight-through, entropy, utility labels, policy gradients. | MANTa's no-bottleneck degeneration; English whitespace competitiveness. |
| Where does compute occur? C04 | Alter update frequency, connectivity, state, or within-position depth. | Hierarchies, selective recurrence, sparse/LSH attention, latent arrays, ACT. | Sparse strided quality loss; ACT's training-only near-tie. |
| When is information available? C05 | Shift and mask every path and distinguish completed from partial groups. | Causal convolution/pooling, delayed expansion, transient scratchpad masks. | GBST leakage and leak-free failed padding; Hourglass residual distinction. |
| How are futures emitted? C06 | Choose a dependent joint, proposals, denoising, or verified continuation. | Local AR, offset heads, circuits, block diffusion, rejection correction. | Higher acceptance can be slower; threshold emission changes policy. |
| Which parameters are shared? C07 | Reuse named tables or transformations and specify their geometry. | Tying, normalized readouts, projections, class scales, gradient-path diagnostics. | MEGABYTE local I/O versus LCA head/head; no general byte tying winner. |
| How is learning stabilized? C08 | Supply the missing signal or gradient while measuring its actual utility. | Deep supervision, rate losses, EMA, curricula, dropout, auxiliary gradient controls. | One-hot dropout reversal; temporary subword head negative. |
| How is a host reused? C09 | Align representations, functions, or output laws in explicit stages. | Geometry imitation, frozen-host backpropagation, distillation, hypernetworks, selective/full unfreezing. | Bolmo noncatastrophic no-stage-one control; conversion behavior losses. |
| Who benefits on which task? C10 | Test the outcome on relevant languages, tasks, and corruptions. | Noise mixtures, probes, task interventions, subgroup evaluation, correlation studies. | Coverage without robustness; probe spelling without host utility. |
| What is scored? C11 | Match the probability event and denominator before comparing loss. | Latent-path estimates, prefix covers, marked processes, residual identities. | TokSuite figure computation unknown; canonical paths are not marginals. |
| What resource is improved? C12 | Compare explicit exposure, compute, memory, and serving frontiers. | Scaling fits, controlled budgets, retained-text accounting, statistical proxies. | Byte parameter advantage with subword training-FLOP advantage. |

The table is a synthesis of [C01–C12](../02_inventory/TAXONOMY.md), not 12 newly discovered types or 12 independent results. A source can contribute several mechanisms, and a mechanism can address several problems. Actual technique use differs from analyst analogy: PCGrad, sentence VAEs, and vision merging are background or adjacent evidence unless a named byte study uses them.

### 14.2 Technique relationships that matter across chapters

Several techniques recur in different roles. CNNs can extract word-internal patterns, provide order before soft pooling, or supply local causal context. Attention can retrieve explicit past positions, aggregate a patch, read a latent workspace, or query outputs. Dynamic programming can find shortest segmentations, sum latent paths, or organize a tokenizer proposal. Gating can carry features, select an expensive update, delete a state, halt recurrent computation, or suppress an auxiliary gradient. The shared technique name does not identify the same scientific problem or guarantee the same outcome.

Distillation is particularly heterogeneous. It can match vectors, contextual states, token logits, byte-prefix distributions, or complete teacher sequences. The first encourages geometric resemblance; the second tests host compatibility; the third transfers classifier behavior under aligned units; the fourth needs a probability-event conversion; the fifth can reduce multimodal target variation. Their costs, supports, and failure modes differ. Calling them all knowledge transfer without the matched object loses the mechanism.

The most useful comparison unit is consequently a small packet: a parent question, two or three source mechanisms, the strongest control, and the remaining outcome. For instance, entropy versus utility needs BLT's independent predictive distribution, SOMBRERO's observed-target confidence, the layout-utility intervention, and ACT's earlier effort diagnostic—not four votes for learned boundaries. Host compatibility needs Char2Subword's geometry/context stages, Bolmo's functional alignment, and the severe direct-distillation control—not a slogan that all byteification requires a warmup.

### 14.3 Negative findings as explanatory structure

Counterexamples should alter the explanatory model, not appear as a detached limitations list. PAQ's advantage constrains a historical neural-compression claim. Dropout matching changes the interpretation of embedding elimination. Leak-free failed padding separates temporal legality from learnability. MANTa's bottleneck failure separates differentiation from rate pressure. Domain and language reversals constrain rule-based and learned routing. Larger draft rank losing throughput separates expressivity from useful acceleration. MYTE's unsupported-script ratio separates absolute compression from parity. Spelling initialization's bounded null separates decodable information from objective utility.

The controls locate different bottlenecks—retention, optimization, timing, and execution—and therefore motivate different follow-up comparisons rather than one generic remedy.

<a id="s15"></a>
## 15. Evaluation design and the research frontier

### 15.1 Three complementary comparison designs

A mechanism-isolating experiment should hold relevant text, rate, capacity, and training semantics close enough to identify the intervention. A compute-frontier experiment should optimize each system under the same complete operation or measured-time budget, permitting different text and parameter choices. A deployment-frontier experiment should compare end-to-end serving at matched task quality and user workload. These are complementary. A strong frontier point does not isolate why it wins; a clean ablation need not be the best deployable system.

For representation, first match retained original text and original-text context. For efficiency, then match training work with teachers and search itemized. For deployment, fix prompt content, required output, quality tolerance, hardware/precision, batch/concurrency, and termination policy. Report what is allowed to change in each design. Corruption semantics should be matched as carefully as nominal dropout probability, as the one-hot control demonstrates.

### 15.2 A field evaluation matrix

**Table 8. Outcome instruments and necessary controls.**

| Evaluation family | Primary outcome | Required distinctions or controls |
|---|---|---|
| Coverage and preservation | Exact round trip, rejection/unknown fraction | Original versus processed bytes, scalars, graphemes, and positions |
| Unicode continuation | Complete strict validity and intended scalar | Valid unfinished prefix, remaining bytes, raw output before repair |
| Surface operations | Whole-string exact match and declared-unit edits | Copy/edit/count/index unit; normalization permissions |
| Morphology and translation | Task-specific accuracy, chrF, or declared metric | Rare forms, held-out lemmas, direction, annotation and clean controls |
| Robustness | Absolute clean/noisy scores and paired degradation | Natural/synthetic process, severity, unseen noise, matched augmentation |
| Numeracy | Numerical correctness and exact transcription | Carry chains, grouping, script, separators, parser failures |
| Long dependencies | Generated whole-span correctness | Distance, distractors, query timing, source substitution/removal |
| Language modeling | Named-event loss with explicit denominator | Path/marginal/prefix/marked distinction; EOS/PAD/prompt/overlap |
| Serving | Request latency, throughput, peak memory at matched quality | Prefill, partial prompts, all auxiliary models, buffering, concurrency |

Freeze source, tokenizer, and model versions; preserve reversible offset maps to processed views. Sample natural documents and human-reviewed parallel content across resource level, script, morphology, whitespace conventions, domain, and dialect. Language and script should not be treated as synonyms. Test scripts absent from tokenizer training separately from scripts absent from model training. Include natural code-switching and controlled mixed-script insertions.

Statistical units also matter. Language cells are not independent training seeds, repeated sentences are not new documents, and multiple tasks share models. Pair comparisons on the same examples and respect run/document/language structure when estimating uncertainty. Publish macro language averages, corpus-weighted totals, subgroup distributions, and worst-group changes. Chance or majority floors and malformed-output rates belong beside task accuracy, particularly when apparent equality occurs near a floor.

### 15.3 The most consequential open intersections

The strongest unanswered questions combine mechanisms rather than ask whether bytes are globally better. Can a cheap causal router estimate incremental value of a trunk update, not just uncertainty, while maintaining stable realized rates across domains? Can boundary choice and aggregation be separated under matched rates and capacity? Can transient refresh preserve a small cache without losing its advantage once batching and partial-prompt costs are measured? Can a dependent draft remain small enough that its additional acceptance pays for conditional sampling and verification?

For transfer, the question is functional preservation across several simultaneous changes: local geometry, sequence clock, boundary decisions, and output law. Staged objectives help some hosts and budgets, yet direct controls differ. Task-vector correspondence or retained backbone weights is not sufficient evidence that post-trained instruction behavior survives. Tests should include the original general tasks and new spelling-sensitive tasks under the same adaptation budget.

For multilingual work, general prefix-computable mixed-script routing, unseen-script generation, grapheme-preserving long exact copy, and non-ASCII arithmetic remain thinly evidenced. Existing losses and encodings motivate these questions but do not establish universal failures. The same is true of first-complete-scalar latency, stable-grapheme emission, and tail latency under matched-quality batch serving. These require outcome measurements rather than additional alphabet arguments.

The remaining specification questions concern MtPC's optimized state law, TokSuite's Figure 6 transformation, MYTE's aggregation, and prefix stability of offline guides. Their concrete closure evidence is collected in [OPEN_QUESTIONS_EN, OQ-12–15](OPEN_QUESTIONS_EN.md#oq12), separately from the outcome experiments above.

<a id="s16"></a>
## 16. Conclusion

The literature below the token is not one research program progressing toward a universally correct learned granularity. It is a family of solutions to lexical coverage, parameter sharing, local composition, sequence cost, information availability, output dependence, pretrained compatibility, and user-facing fidelity. Character antecedents supplied recurrence, gated composition, and contextual transfer; byte interfaces supplied compact coverage and direct symbol modeling; encoders and denoisers made fine-input learning practical; full-resolution methods changed connectivity, state, and execution; hierarchies moved expensive computation; and conversion methods made the interface itself a learnable transfer problem.

The central empirical pattern is redistribution. Smaller lexical tables can buy more contextual capacity but require more positions. Grouping can reduce trunk work while increasing local responsibility or delaying fresh context. Parallel futures can improve representations without defining a dependent law, and better dependent drafts can cost more than they save. Teachers can disappear from deployment while remaining substantial training resources. Universal representability can coexist with unequal effective context, brittle noise behavior, or wrong output.

No universal byte/subword ranking follows. The strongest positive results are conditional and substantive: improved selected surface-form tasks, useful scarce-data transfer, competitive full-resolution likelihoods, economical internal processing, and workable checkpoint conversion. The strongest negatives are equally informative because they locate the actual bottlenecks. The field advances when it names all four interfaces, specifies legal information paths and probability events, distinguishes parameter axes, and measures quality under the resource and task contract that matters. That framework supports byte, code-point, subword, word-composed, and mixed designs without requiring any one local architecture to be the destination.

<a id="appendix-a"></a>
## Appendix A. Methodology, evidence depth, and reference navigation

### A.1 Corpus construction and counting

The survey follows the authorized [PLAN](../PLAN.md), eight discovery/inventory streams, single-owner identity reconciliation, selected source readings, thematic synthesis, and independent review. Stable **BIW-0001–BIW-0141** identify 141 source entities. Stable **BIP-0001–BIP-0296** identify traceable question/mechanism/evidence records. A version, alias, appendix, or repeated citation does not become another entity. The exact source-type partition is 136 academic papers/preprints, one official research report, three standards, and one official model introduction. Combining papers and report gives 137 research documents; they are not 137 native-byte models. One proposal-only academic source contributes no BIP record.

The 296 records comprise 283 merged discovery-backed records, three audit records, and ten field-addendum subfindings. They include controls, specifications, and reviewer exceptions, so neither 296 nor 283 is an independent-problem or successful-experiment count. The twelve manual multi-label families have 506 record–family memberships and a union of all 296 records. The provenance ledger independently has 506 source-to-record edges; its identical total is coincidental, not the same relation. No algorithmic embedding clustering or exhaustive unique-parent census was performed.

### A.2 Reading support and its limits

Ninety-two distinct scoped FULL identities comprise 30 reused older readings and 62 new readings: 60 from R01–R10 plus ACT and Reformer. The old/new identity sets are disjoint. ELMo and GPT-2 are two additional intentional narrow PARTIAL extractions, not failed full reads: ELMo v2 §§1–3.4/Table 1, and official GPT-2 report p.4 §§2.2–2.3/adjacent §3.1. The rest of their result sections is not certified by those extractions. Other abstract/selected-primary reserves retain their depth ceiling and do not carry deciding quantitative claims here.

At record level, 233 have scoped-FULL support, four narrow-PARTIAL support, 53 discovery A/P support, three normative support, two introduction support, and one targeted correction/open-computation status. These are evidence availability classes, not independent effects. FULL does not mean reproduced, code-audited, correct in every theorem, complete in every cost field, or run-linked. This English authorship adds no new FULL credits and reports no experimental reproduction.

The evidence distinguishes paper specification, analyst derivation, static configuration/code, and run-linked runtime verification. Unknown runtime behavior stays unknown. Source discrepancies are not silently reconciled. Independent R1/R2 audits sampled designated passages rather than rereading the entire corpus; their zero-new-FULL accounting is preserved. Latest [CLAIM_RULES](../05_review/CLAIM_RULES.md) takes precedence over superseded card shorthand, particularly for MYTE, Hourglass, MtPC, TokSuite, and dialect metric attribution.

### A.3 Reference chain and reproducibility of interpretation

A substantive reference follows **parent question → BIP record → BIW identity → carrying card → actual version and section/table → current correction**. In-text card links retain the inspected version and public source. The [WORK_CATALOG](../02_inventory/WORK_CATALOG.md) supplies identities, aliases, versions, and four-unit baselines; [DETAILED_INVENTORY](../02_inventory/DETAILED_INVENTORY.md) supplies mechanisms and provenance; [EVIDENCE_STATUS](../02_inventory/EVIDENCE_STATUS.md) supplies claim ceilings; [TAXONOMY](../02_inventory/TAXONOMY.md) supplies canonical membership; and [FINAL_AUTHOR_COUNTS](../02_inventory/FINAL_AUTHOR_COUNTS.md) with [VALIDATION](../02_inventory/VALIDATION.md) supplies frozen reconciliation.

The companion [CLASSIFICATION_EN](CLASSIFICATION_EN.md) and [INVENTORY_READING_GUIDE_EN](INVENTORY_READING_GUIDE_EN.md) are navigation resources, not new sources of empirical effects. The four thematic drafts supply extended working treatments: [representation/history](01_REPRESENTATION_AND_HISTORY_EN.md), [grouping/generation](02_GROUPING_AND_GENERATION_EN.md), [geometry/compute](03_GEOMETRY_AND_COMPUTE_EN.md), and [multilingual evaluation](04_MULTILINGUAL_EVALUATION_EN.md). The final survey consolidates their overlapping parents while retaining case-level evidence.

Source-level audits are [DISCOVERY_CORRECTIONS](../05_review/DISCOVERY_CORRECTIONS.md), [FULL_READING_AUDIT_R1](../05_review/FULL_READING_AUDIT_R1.md), [FULL_READING_AUDIT_R2](../05_review/FULL_READING_AUDIT_R2.md), [FIELD_COVERAGE_AUDIT](../05_review/FIELD_COVERAGE_AUDIT.md), and [INVENTORY_CLASSIFICATION_REVIEW](../05_review/INVENTORY_CLASSIFICATION_REVIEW.md). Historical counts inside earlier audits describe their snapshots, not the current release. Critical claims use completed carrying evidence or explicitly bounded derivations, rather than treating an unverified abstract as sufficient.

### A.4 Remaining scope

This is a selected neural language-interface survey with relevant historical, statistical, normative, and nonbyte controls. It is not an exhaustive compression history, a universal tokenizer benchmark, or a common-resource leaderboard. Public source reading does not establish arbitrary mixed-script streaming behavior, unseen-script knowledge, long exact-copy competence, non-ASCII arithmetic, or modern serving frontiers where those comparisons were not performed. Such gaps are stated once by affected outcome rather than turned into a blanket defense of every method.

<a id="appendix-b"></a>
## Appendix B. Translation and terminology contract

The numbered sections, explicit anchors `s01`–`s16`, appendices, Tables 1–8, BIW/BIP identifiers, equations, and linked source versions are stable navigation objects. A complete translation should preserve their order and meaning, rather than replace the body with an abridgment. Byte, code point, Unicode scalar, grapheme cluster, restricted character, subword, word, alternate code, and annotation event must remain distinct. The four-unit tuple should remain in the order input/internal/output/supervision.

Terms with several technical meanings require their local object: causal attention versus statistical causal identification; lexical input/output tying versus head/head or Q/K sharing; training activation memory versus inference KV; canonical path versus string marginal versus raw-prefix probability; exact greedy matching versus stochastic target-law preservation; partial UTF-8 progress versus complete legality versus intended scalar. FULL should translate as scoped source-reading completion, never reproduced experimental validation. Intentional PARTIAL should not become blocked access or failed full reading.

Numerical uncertainty and local source conditions are part of the claim. In particular preserve MYTE's table-specific row/column values and unresolved aggregation, Hourglass's shifted residual, MtPC's open optimized-wrapper guarantee without a software verdict, TokSuite's unknown actual figure computation without discarding separate results, and the dialect TP/IP attribution without inventing a definite sign contradiction. Concise prose may remove repeated framing; it must not remove a material condition, counterexample, or distinction between observed and extrapolated results.
