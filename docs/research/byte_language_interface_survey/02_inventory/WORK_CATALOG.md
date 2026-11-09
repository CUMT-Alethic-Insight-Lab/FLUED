# Canonical work catalog — independent byte-language interfaces

**Frozen author/translator release:** [FINAL_AUTHOR_COUNTS](FINAL_AUTHOR_COUNTS.md) and [VALIDATION](VALIDATION.md) give current verified counts, exact IDs and the R2 claim-rule adoption. Earlier receipt statistics inside historical sections are not the current cohort.

2026-11-09 · owner: `02_inventory` · entity register, not the survey text.

Read [evidence status](EVIDENCE_STATUS.md), [correction log](CORRECTION_LOG.md), [COUNTS](COUNTS.md) for denominators, [detailed problems](DETAILED_INVENTORY.md) for findings, [taxonomy](TAXONOMY.md) for manual multi-label grouping and [reading queue](READING_QUEUE.md) for assignments.

## Identity and reading contract

`BIW` means byte-interface work: one stable ID per independent source entity, including explicitly labeled standards/introduction. IDs are frozen in this release and must never be reassigned or renumbered on sorting, publication, title change or new arXiv revision; append new IDs. Existing W IDs remain aliases, not overwritten identities. A title variant or formal/preprint version normally shares one BIW; related but distinct papers do not. `BIP` means byte-interface problem: a separately identifiable problem/mechanism/evidence record, not a paper or an independent successful effect.

141 entities =136academic papers (including oneproposal-only), oneofficialresearchreport, threestandards andoneofficialintroduction;140entities contribute records. The prior137 identities and250 discovery work appearances are preserved; four new dedicated sources are mapped explicitly.

Current card evidence precedes historical notes. Full-reading status is version/scoped, not proof/code certification. Detailed record count is a provenance-rich question/mechanism/evidence inventory, NOT a census of independent scientific problems. Read AUTHOR_HANDOFF before synthesis.

## Stable entity index (current)

| BIW | Kind / original W | Work | Current depth | Carrying card or ceiling |
|---|---|---|---|---|
| [BIW-0001](#BIW-0001) | academic paper/W0001 | Neural Machine Translation of Rare Words with Subword Units | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0002](#BIW-0002) | academic paper/W0002 | Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0003](#BIW-0003) | academic paper/W0003 | SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0004](#BIW-0004) | academic paper/W0004 | CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation | NF — returned scoped FULL | [R01/BIW-0004](../03_reading/R01/BIW-0004.md) |
| [BIW-0005](#BIW-0005) | academic paper/W0005 | Charformer: Fast Character Transformers via Gradient-based Subword Tokenization | NF — returned scoped FULL | [R01/BIW-0005](../03_reading/R01/BIW-0005.md) |
| [BIW-0006](#BIW-0006) | academic paper/W0006 | MANTa: Efficient Gradient-Based Tokenization for Robust End-to-End Language Modeling | NF — returned scoped FULL | [R01/BIW-0006](../03_reading/R01/BIW-0006.md) |
| [BIW-0007](#BIW-0007) | academic paper/W0007 | Efficient Transformers with Dynamic Token Pooling | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md) |
| [BIW-0008](#BIW-0008) | academic paper/W0008 | MEGABYTE: Predicting Million-byte Sequences with Multiscale Transformers | NF — returned scoped FULL | [R03/BIW-0008](../03_reading/R03/BIW-0008.md) |
| [BIW-0009](#BIW-0009) | academic paper/W0009 | SpaceByte: Towards Deleting Tokenization from Large Language Modeling | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B05/W0009.md) |
| [BIW-0010](#BIW-0010) | academic paper/W0010 | Byte Latent Transformer: Patches Scale Better Than Tokens | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md) |
| [BIW-0011](#BIW-0011) | academic paper/W0011 | Dynamic Chunking for End-to-End Hierarchical Sequence Modeling | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md) |
| [BIW-0012](#BIW-0012) | academic paper/W0012 | SOMBRERO: Measuring and Steering Boundary Placement in End-to-End Hierarchical Sequence Models | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B24/W0012.md) |
| [BIW-0013](#BIW-0013) | academic paper/W0013 | A gated quantized VAE for learning variable length tokens (GQ-VAE) | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B24/W0013.md) |
| [BIW-0014](#BIW-0014) | academic paper/W0014 | Fast Byte Latent Transformer | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B14/W0014.md) |
| [BIW-0015](#BIW-0015) | academic paper/W0015 | Dynamic Multi-Byte Prediction With Hierarchical Language Models | NF — returned scoped FULL | [R05/BIW-0015](../03_reading/R05/BIW-0015.md) |
| [BIW-0016](#BIW-0016) | academic paper/W0016 | Hierarchical Multiscale Recurrent Neural Networks | NF — returned scoped FULL | [R03/BIW-0016](../03_reading/R03/BIW-0016.md) |
| [BIW-0017](#BIW-0017) | academic paper/W0022 | Funnel-Transformer: Filtering out Sequential Redundancy for Efficient Language Processing | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0018](#BIW-0018) | academic paper/W0023 | Compressive Transformers for Long-Range Sequence Modelling | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B24/W0023.md) |
| [BIW-0019](#BIW-0019) | academic paper/W0024 | Token Merging: Your ViT But Faster | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B24/W0024.md) |
| [BIW-0020](#BIW-0020) | academic paper/W0038 | In-context Autoencoder for Context Compression in a Large Language Model | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B24/W0038.md) |
| [BIW-0021](#BIW-0021) | academic paper/W0061 | Repeat After Me: Transformers are Better than State Space Models at Copying | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md) |
| [BIW-0022](#BIW-0022) | academic paper/W0328 | Gradient Surgery for Multi-Task Learning | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B16/W0328.md) |
| [BIW-0023](#BIW-0023) | academic paper/W0331 | Adapting Auxiliary Losses Using Gradient Similarity | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B16/W0331.md) |
| [BIW-0024](#BIW-0024) | academic paper/W0351 | ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md) |
| [BIW-0025](#BIW-0025) | academic paper/W0352 | MambaByte: Token-free Selective State Space Model | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md) |
| [BIW-0026](#BIW-0026) | academic paper/W0353 | Beyond Language Models: Byte Models are Digital World Simulators | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0027](#BIW-0027) | academic paper/W0355 | When Tokenizers Fail: Byte-Level Chunking for Zero-Shot Transfer to Low-Resource Languages | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B14/W0355.md) |
| [BIW-0028](#BIW-0028) | academic paper/W0356 | Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md) |
| [BIW-0029](#BIW-0029) | academic paper/W0357 | Easy to anticipate, hard to compute: boundary dependence finds the computed outputs that entropy patching misses | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B05/W0357.md) |
| [BIW-0030](#BIW-0030) | academic paper/W0358 | Patch where the text is new: a compression view of where byte-level models should spend compute | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B14/W0358.md) |
| [BIW-0031](#BIW-0031) | academic paper/W0359 | Universal Byte-Level Encoding: UTF-8/UTF-16 Routing to Reduce Cross-Script Token-Budget Disparities | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B14/W0359.md) |
| [BIW-0032](#BIW-0032) | academic paper/W0360 | A Multi-dimensional Evaluation of Tokenizer-free Multilingual Pretrained Models | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B08/W0360.md) |
| [BIW-0033](#BIW-0033) | academic paper/W0361 | Language Model Tokenizers Introduce Unfairness Between Languages | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B14/W0361.md) |
| [BIW-0034](#BIW-0034) | academic paper/W0363 | Rate–Utility Frontiers for Language Encodings: Comparing Tokens, Bytes, and Pixels Under Controlled Linguistic Content | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B08/W0363.md) |
| [BIW-0035](#BIW-0035) | academic paper/W0364 | Using the Output Embedding to Improve Language Models | NF — returned scoped FULL | [R08/BIW-0035](../03_reading/R08/BIW-0035.md) |
| [BIW-0036](#BIW-0036) | academic paper/W0365 | Tying Word Vectors and Word Classifiers: A Loss Framework for Language Modeling | NF — returned scoped FULL | [R08/BIW-0036](../03_reading/R08/BIW-0036.md) |
| [BIW-0037](#BIW-0037) | academic paper/W0366 | Weight Tying Biases Token Embeddings Towards the Output Space | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B14/W0366.md) |
| [BIW-0038](#BIW-0038) | academic paper/W0367 | Rethinking Weight Tying: Pseudo-Inverse Tying for LM Stable Training and Updates | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0039](#BIW-0039) | academic paper/W0368 | AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0040](#BIW-0040) | academic paper/W0386 | Unsupervised Neural Word Segmentation for Chinese via Segmental Language Modeling | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0041](#BIW-0041) | academic paper/W0387 | A Masked Segmental Language Model for Unsupervised Natural Language Segmentation | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0042](#BIW-0042) | academic paper/W0401 | Learning to Discover, Ground and Use Words with Segmental Neural Language Models | NF — returned scoped FULL | [R03/BIW-0042](../03_reading/R03/BIW-0042.md) |
| [BIW-0043](#BIW-0043) | academic paper/W0404 | Unsupervised Learning of Word Boundary with Description Length Gain | NF — returned scoped FULL | [R02/BIW-0043](../03_reading/R02/BIW-0043.md) |
| [BIW-0044](#BIW-0044) | academic paper/W0509 | Beyond Perplexity: UTF-8 Validity in Byte-aware Language Models | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B22/W0509.md) |
| [BIW-0045](#BIW-0045) | academic paper/W0510 | MAGNET: Improving the Multilingual Fairness of Language Models with Adaptive Gradient-Based Tokenization | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B26/W0510.md) |
| [BIW-0046](#BIW-0046) | academic paper/W0511 | MrT5: Dynamic Token Merging for Efficient Byte-level Language Models | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B22/W0511.md) |
| [BIW-0047](#BIW-0047) | academic paper/W0512 | Compute Optimal Tokenization | NF — returned scoped FULL | [R05/BIW-0047](../03_reading/R05/BIW-0047.md) |
| [BIW-0048](#BIW-0048) | academic paper/W0514 | Local Byte Fusion for Neural Machine Translation | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B26/W0514.md) |
| [BIW-0049](#BIW-0049) | academic paper/W0515 | Beyond Text Compression: Evaluating Tokenizers Across Scales | NF — returned scoped FULL | [R08/BIW-0049](../03_reading/R08/BIW-0049.md) |
| [BIW-0050](#BIW-0050) | academic paper/W0516 | Language-Specific Effects of Tokenizer Choice in Multilingual Language Models | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B22/W0516.md) |
| [BIW-0051](#BIW-0051) | academic paper/W0518 | TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior | RF — reused scoped FULL | [oldWcard](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md) |
| [BIW-0052](#BIW-0052) | academic paper | Generating Text with Recurrent Neural Networks | NF — returned scoped FULL | [R02/BIW-0052](../03_reading/R02/BIW-0052.md) |
| [BIW-0053](#BIW-0053) | academic paper | Generating Sequences With Recurrent Neural Networks | NF — returned scoped FULL | [R02/BIW-0053](../03_reading/R02/BIW-0053.md) |
| [BIW-0054](#BIW-0054) | academic paper | Character-level Convolutional Networks for Text Classification | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0055](#BIW-0055) | academic paper | Character-Aware Neural Language Models | NF — returned scoped FULL | [R02/BIW-0055](../03_reading/R02/BIW-0055.md) |
| [BIW-0056](#BIW-0056) | academic paper | Finding Function in Form: Compositional Character Models for Open Vocabulary Word Representation | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0057](#BIW-0057) | academic paper | Multilingual Language Processing From Bytes | NF — returned scoped FULL | [R02/BIW-0057](../03_reading/R02/BIW-0057.md) |
| [BIW-0058](#BIW-0058) | academic paper | Neural Machine Translation in Linear Time | NF — returned scoped FULL | [R02/BIW-0058](../03_reading/R02/BIW-0058.md) |
| [BIW-0059](#BIW-0059) | academic paper | Fully Character-Level Neural Machine Translation without Explicit Segmentation | NF — returned scoped FULL | [R03/BIW-0059](../03_reading/R03/BIW-0059.md) |
| [BIW-0060](#BIW-0060) | academic paper | A Character-Level Decoder without Explicit Segmentation for Neural Machine Translation | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0061](#BIW-0061) | academic paper | Byte-based Neural Machine Translation | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0062](#BIW-0062) | academic paper | Exploring the Limits of Language Modeling | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0063](#BIW-0063) | academic paper | Learning to Generate Reviews and Discovering Sentiment | NF — returned scoped FULL | [R02/BIW-0063](../03_reading/R02/BIW-0063.md) |
| [BIW-0064](#BIW-0064) | academic paper | Character-Level Language Modeling with Deeper Self-Attention | NF — returned scoped FULL | [R09/BIW-0064](../03_reading/R09/BIW-0064.md) |
| [BIW-0065](#BIW-0065) | academic paper | Neural Machine Translation with Byte-Level Subwords | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0066](#BIW-0066) | academic paper | CharacterBERT: Reconciling ELMo and BERT for Word-Level Open-Vocabulary Representations From Characters | NF — returned scoped FULL | [R01/BIW-0066](../03_reading/R01/BIW-0066.md) |
| [BIW-0067](#BIW-0067) | academic paper | CharBERT: Character-aware Pre-trained Language Model | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0068](#BIW-0068) | academic paper | Neural Machine Translation without Embeddings | NF — returned scoped FULL | [R01/BIW-0068](../03_reading/R01/BIW-0068.md) |
| [BIW-0069](#BIW-0069) | academic paper | MoCE: Adaptive Mixture of Contextualization Experts for Byte-based Neural Machine Translation | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0070](#BIW-0070) | academic paper | Revisiting Character-Based Neural Machine Translation with Capacity and Compression | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0071](#BIW-0071) | academic paper | Bridging the Gap for Tokenizer-Free Language Models | NF — returned scoped FULL | [R09/BIW-0071](../03_reading/R09/BIW-0071.md) |
| [BIW-0072](#BIW-0072) | academic paper | Hierarchical Transformers Are More Efficient Language Models | NF — returned scoped FULL | [R03/BIW-0072](../03_reading/R03/BIW-0072.md) |
| [BIW-0073](#BIW-0073) | academic paper | A Vocabulary-Free Multilingual Neural Tokenizer for End-to-End Task Learning | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0074](#BIW-0074) | academic paper | Patching Leaks in the Charformer for Efficient Character-Level Generation | NF — returned scoped FULL | [R03/BIW-0074](../03_reading/R03/BIW-0074.md) |
| [BIW-0075](#BIW-0075) | academic paper | Subword-Delimited Downsampling for Better Character-Level Translation | NF — returned scoped FULL | [R03/BIW-0075](../03_reading/R03/BIW-0075.md) |
| [BIW-0076](#BIW-0076) | academic paper | Scratchpad Patching: Decoupling Compute from Patch Size in Byte-Level Language Models | NF — returned scoped FULL | [R05/BIW-0076](../03_reading/R05/BIW-0076.md) |
| [BIW-0077](#BIW-0077) | academic paper | From Bytes to Ideas: Language Modeling with Autoregressive U-Nets | NF — returned scoped FULL | [R10/BIW-0077](../03_reading/R10/BIW-0077.md) |
| [BIW-0078](#BIW-0078) | academic paper | You Can Learn Tokenization End-to-End with Reinforcement Learning | NF — returned scoped FULL | [R09/BIW-0078](../03_reading/R09/BIW-0078.md) |
| [BIW-0079](#BIW-0079) | academic paper | Fast and Expressive Multi-Byte Prediction with Probabilistic Circuits | NF — returned scoped FULL | [R05/BIW-0079](../03_reading/R05/BIW-0079.md) |
| [BIW-0080](#BIW-0080) | academic paper | You should evaluate your language model on marginal likelihood over tokenisations | NF — returned scoped FULL | [R04/BIW-0080](../03_reading/R04/BIW-0080.md) |
| [BIW-0081](#BIW-0081) | official introduction | EvaByte: Efficient Byte-level Language Models at Scale | O: official introduction | Discovery scope only; not escalated |
| [BIW-0082](#BIW-0082) | academic paper | Blockwise Parallel Decoding for Deep Autoregressive Models | NF — returned scoped FULL | [R05/BIW-0082](../03_reading/R05/BIW-0082.md) |
| [BIW-0083](#BIW-0083) | academic paper | Fast Inference from Transformers via Speculative Decoding | NF — returned scoped FULL | [R04/BIW-0083](../03_reading/R04/BIW-0083.md) |
| [BIW-0084](#BIW-0084) | academic paper | Accelerating Large Language Model Decoding with Speculative Sampling | NF — returned scoped FULL | [R04/BIW-0084](../03_reading/R04/BIW-0084.md) |
| [BIW-0085](#BIW-0085) | academic paper | Better & Faster Large Language Models via Multi-token Prediction | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0086](#BIW-0086) | academic paper | Block Transformer: Global-to-Local Language Modeling for Fast Inference | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0087](#BIW-0087) | academic paper | Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0088](#BIW-0088) | academic paper | Exact Byte-Level Probabilities from Tokenized Language Models for FIM-Tasks and Model Ensembles | NF — returned scoped FULL | [R04/BIW-0088](../03_reading/R04/BIW-0088.md) |
| [BIW-0089](#BIW-0089) | academic paper | Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models | NF — returned scoped FULL | [R05/BIW-0089](../03_reading/R05/BIW-0089.md) |
| [BIW-0090](#BIW-0090) | standard | RFC 3629: UTF-8, a transformation format of ISO 10646 | N: selected standard | Discovery scope only; not escalated |
| [BIW-0091](#BIW-0091) | academic paper | Normalization of Input-output Shared Embeddings in Text Generation Models | NF — returned scoped FULL | [R08/BIW-0091](../03_reading/R08/BIW-0091.md) |
| [BIW-0092](#BIW-0092) | academic paper | nGPT: Normalized Transformer with Representation Learning on the Hypersphere | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0093](#BIW-0093) | academic paper | Breaking the Softmax Bottleneck: A High-Rank RNN Language Model | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0094](#BIW-0094) | academic paper | Generating Sentences from a Continuous Space | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0095](#BIW-0095) | academic paper | Improved Variational Autoencoders for Text Modeling using Dilated Convolutions | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0096](#BIW-0096) | academic paper | Lagging Inference Networks and Posterior Collapse in Variational Autoencoders | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0097](#BIW-0097) | academic paper | Bolmo: Byteifying the Next Generation of Language Models | NF — returned scoped FULL | [R06/BIW-0097](../03_reading/R06/BIW-0097.md) |
| [BIW-0098](#BIW-0098) | academic paper | Distilling Token-Trained Models into Byte-Level Models | NF — returned scoped FULL | [R06/BIW-0098](../03_reading/R06/BIW-0098.md) |
| [BIW-0099](#BIW-0099) | academic paper | Cross-Tokenizer LLM Distillation through a Byte-Level Interface | NF — returned scoped FULL | [R06/BIW-0099](../03_reading/R06/BIW-0099.md) |
| [BIW-0100](#BIW-0100) | academic paper | Nested Byte-Level Vocabularies Are Cheap to Deploy and Expensive to Share: A Pre-Registered Negative Result | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0101](#BIW-0101) | academic paper | Kronecker Embeddings: Byte-Level Structured Token Representations for Parameter-Efficient Language Models | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0102](#BIW-0102) | proposal-onlypaper | Super Tiny Language Models | P: proposal-only | Discovery scope only; not escalated |
| [BIW-0103](#BIW-0103) | academic paper | Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models | NF — returned scoped FULL | [R06/BIW-0103](../03_reading/R06/BIW-0103.md) |
| [BIW-0104](#BIW-0104) | academic paper | MYTE: Morphology-Driven Byte Encoding for Better and Fairer Multilingual Language Modeling | NF — returned scoped FULL | [R07/BIW-0104](../03_reading/R07/BIW-0104.md) |
| [BIW-0105](#BIW-0105) | academic paper | XTREME-UP: A User-Centric Scarce-Data Benchmark for Under-Represented Languages | NF — returned scoped FULL | [R07/BIW-0105](../03_reading/R07/BIW-0105.md) |
| [BIW-0106](#BIW-0106) | academic paper | Byte-based Multilingual NMT for Endangered Languages | NF — returned scoped FULL | [R07/BIW-0106](../03_reading/R07/BIW-0106.md) |
| [BIW-0107](#BIW-0107) | academic paper | How Robust is Neural Machine Translation to Language Imbalance in Multilingual Tokenizer Training? | NF — returned scoped FULL | [R07/BIW-0107](../03_reading/R07/BIW-0107.md) |
| [BIW-0108](#BIW-0108) | academic paper | Decoupling the Benefits of Subword Tokenization for Language Model Training via Byte-level Simulation | NF — returned scoped FULL | [R08/BIW-0108](../03_reading/R08/BIW-0108.md) |
| [BIW-0109](#BIW-0109) | academic paper | Synthetic and Natural Noise Both Break Neural Machine Translation | NF — returned scoped FULL | [R07/BIW-0109](../03_reading/R07/BIW-0109.md) |
| [BIW-0110](#BIW-0110) | academic paper | Models in a Spelling Bee: Language Models Implicitly Learn the Character Composition of Tokens | NF — returned scoped FULL | [R10/BIW-0110](../03_reading/R10/BIW-0110.md) |
| [BIW-0111](#BIW-0111) | academic paper | Tokenization counts: the impact of tokenization on arithmetic in frontier LLMs | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0112](#BIW-0112) | academic paper | Tokenization Falling Short: On Subword Robustness in Large Language Models | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0113](#BIW-0113) | academic paper | The Strawberry Problem: Emergence of Character-level Understanding in Tokenized Language Models | NF — returned scoped FULL | [R10/BIW-0113](../03_reading/R10/BIW-0113.md) |
| [BIW-0114](#BIW-0114) | academic paper | CharBench: Evaluating the Role of Tokenization in Character-Level Tasks | NF — returned scoped FULL | [R07/BIW-0114](../03_reading/R07/BIW-0114.md) |
| [BIW-0115](#BIW-0115) | standard | Unicode Standard Annex #15: Unicode Normalization Forms (revision 57) | N: selected standard | Discovery scope only; not escalated |
| [BIW-0116](#BIW-0116) | standard | Unicode Standard Annex #29: Unicode Text Segmentation (revision 47) | N: selected standard | Discovery scope only; not escalated |
| [BIW-0117](#BIW-0117) | academic paper | Perceiver IO: A General Architecture for Structured Inputs & Outputs | NF — returned scoped FULL | [R01/BIW-0117](../03_reading/R01/BIW-0117.md) |
| [BIW-0118](#BIW-0118) | academic paper | Generating Long Sequences with Sparse Transformers | NF — returned scoped FULL | [R09/BIW-0118](../03_reading/R09/BIW-0118.md) |
| [BIW-0119](#BIW-0119) | academic paper | Transformer-XL: Attentive Language Models beyond a Fixed-Length Context | NF — returned scoped FULL | [R09/BIW-0119](../03_reading/R09/BIW-0119.md) |
| [BIW-0120](#BIW-0120) | academic paper | Character-based Neural Machine Translation | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0121](#BIW-0121) | academic paper | Achieving Open Vocabulary Neural Machine Translation with Hybrid Word-Character Models | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0122](#BIW-0122) | academic paper | Char2Subword: Extending the Subword Embedding Space Using Robust Character Compositionality | NF — returned scoped FULL | [R06/BIW-0122](../03_reading/R06/BIW-0122.md) |
| [BIW-0123](#BIW-0123) | academic paper | WECHSEL: Effective initialization of subword embeddings for cross-lingual transfer of monolingual language models | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0124](#BIW-0124) | academic paper | FOCUS: Effective Embedding Initialization for Monolingual Specialization of Multilingual Models | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0125](#BIW-0125) | academic paper | OFA: A Framework of Initializing Unseen Subword Embeddings for Efficient Large-scale Multilingual Continued Pretraining | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0126](#BIW-0126) | academic paper | Zero-Shot Tokenizer Transfer | NF — returned scoped FULL | [R06/BIW-0126](../03_reading/R06/BIW-0126.md) |
| [BIW-0127](#BIW-0127) | academic paper | T-FREE: Subword Tokenizer-Free Generative LLMs via Sparse Representations for Memory-Efficient Embeddings | NF — returned scoped FULL | [R10/BIW-0127](../03_reading/R10/BIW-0127.md) |
| [BIW-0128](#BIW-0128) | academic paper | Mimicking Word Embeddings using Subword RNNs | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0129](#BIW-0129) | academic paper | Byte Pair Encoding is Suboptimal for Language Model Pretraining | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0130](#BIW-0130) | academic paper | Unpacking Tokenization: Evaluating Text Compression and its Correlation with Model Performance | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0131](#BIW-0131) | academic paper | Tokenization Is More Than Compression | NF — returned scoped FULL | [R08/BIW-0131](../03_reading/R08/BIW-0131.md) |
| [BIW-0132](#BIW-0132) | academic paper | Understanding and Mitigating Tokenization Bias in Language Models | NF — returned scoped FULL | [R04/BIW-0132](../03_reading/R04/BIW-0132.md) |
| [BIW-0133](#BIW-0133) | academic paper | Causal Estimation of Tokenisation Bias | NF — returned scoped FULL | [R04/BIW-0133](../03_reading/R04/BIW-0133.md) |
| [BIW-0134](#BIW-0134) | academic paper | Tokenization and Representation Biases in Multilingual Models on Dialectal NLP Tasks | NF — returned scoped FULL | [R10/BIW-0134](../03_reading/R10/BIW-0134.md) |
| [BIW-0135](#BIW-0135) | academic paper | BPE-Dropout: Simple and Effective Subword Regularization | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0136](#BIW-0136) | academic paper | Deduplicating Training Data Makes Language Models Better | A: abstract/metadata | Discovery scope only; not escalated |
| [BIW-0137](#BIW-0137) | academic paper | Long Range Arena: A Benchmark for Efficient Transformers | P: selected primary/recovery | Discovery scope only; not escalated |
| [BIW-0138](#BIW-0138) | academic paper / W0248 | Adaptive Computation Time for Recurrent Neural Networks | NF — returned scoped FULL | [FIELD_ADDENDUM](../03_reading/FIELD_ADDENDUM/arxiv_1603.08983v6.md) |
| [BIW-0139](#BIW-0139) | academic paper | Reformer: The Efficient Transformer | NF — returned scoped FULL | [FIELD_ADDENDUM](../03_reading/FIELD_ADDENDUM/arxiv_2001.04451v2.md) |
| [BIW-0140](#BIW-0140) | academic paper | Deep contextualized word representations (ELMo) | P — intentional narrow primary extraction | [FIELD_ADDENDUM](../03_reading/FIELD_ADDENDUM/arxiv_1802.05365v2.md) |
| [BIW-0141](#BIW-0141) | official research report | Language Models are Unsupervised Multitask Learners (GPT-2 report) | P — intentional narrow primary extraction | [FIELD_ADDENDUM](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md) |

<a id="BIW-0001"></a>
## BIW-0001 — Neural Machine Translation of Rare Words with Subword Units

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0001`.
- **Full-source target / version:** https://arxiv.org/pdf/1508.07909v5. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Orthographic characters inside words → BPE subwords → translated subwords; corpus merge statistics then translation supervision. Original BPE application is character-based, **not modern byte-level BPE**. Tokenization is offline, not a prefix-safe learned boundary policy.
- **Learning and causal baseline:** Orthographic characters inside words → BPE subwords → translated subwords; corpus merge statistics then translation supervision. Original BPE application is character-based, **not modern byte-level BPE**. Tokenization is offline, not a prefix-safe learned boundary policy.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0001](DETAILED_INVENTORY.md#BIP-0001).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S02/W0001**, [WORKS](../01_discovery/S02/WORKS.md) line 16: Sennrich, Haddow & Birch, **Neural Machine Translation of Rare Words with Subword Units** (2015/ACL 2016), [1508.07909v5](https://arxiv.org/abs/1508.07909v5)
  - Original register aliases / era / family / provenance: W0001; reused catalogue
  - Source-scoped evidence/depth: A: v5 abstract/history; detailed algorithm not newly read.
- **S07/W0001**, [WORKS](../01_discovery/S07/WORKS.md) line 18: **Neural Machine Translation of Rare Words with Subword Units**; [1508.07909v5](https://arxiv.org/abs/1508.07909v5), 2016 revision of 2015 preprint
  - Original register aliases / era / family / provenance: W0001
  - Source-scoped evidence/depth: A; no old FULL card.
- **S08/S08-W01**, [WORKS](../01_discovery/S08/WORKS.md) line 32: **Neural Machine Translation of Rare Words with Subword Units**, Sennrich, Haddow & Birch; 2015 preprint / ACL 2016. [v5 abstract](https://arxiv.org/abs/1508.07909v5), [formal paper](https://aclanthology.org/P16-1162.pdf). **A**, abstract plus formal metadata, not paper sections.
  - Original register aliases / era / family / provenance: S08-W01 / **W0001** / catalog reuse
  - Source-scoped evidence/depth: **Neural Machine Translation of Rare Words with Subword Units**, Sennrich, Haddow & Birch; 2015 preprint / ACL 2016. [v5 abstract](https://arxiv.org/abs/1508.07909v5), [formal paper](https://aclanthology.org/P16-1162.pdf). **A**, abstract plus formal metadata, not paper sections. Abstract: +1.1/+1.3 BLEU vs back-off dictionary on WMT15 En–De/En–Ru. Not a byte-LM result; budget and segmentation controls not inspected.

<a id="BIW-0002"></a>
## BIW-0002 — Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0002`.
- **Full-source target / version:** https://aclanthology.org/P18-1007.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Strings → sampled subword sequences → target subwords; unigram segmentation probabilities plus translation training. Multiple segmentations during training, not differentiable latent pooling. Exact normalization/preprocessing not inspected.
- **Learning and causal baseline:** Strings → sampled subword sequences → target subwords; unigram segmentation probabilities plus translation training. Multiple segmentations during training, not differentiable latent pooling. Exact normalization/preprocessing not inspected.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0002](DETAILED_INVENTORY.md#BIP-0002).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S02/W0002**, [WORKS](../01_discovery/S02/WORKS.md) line 17: Kudo, **Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates** (ACL 2018), [formal abstract](https://aclanthology.org/P18-1007/), pp.66–75
  - Original register aliases / era / family / provenance: W0002; reused catalogue
  - Source-scoped evidence/depth: A: formal abstract. arXiv v1 fetch returned tools/footer rather than abstract; not evidence for method details.
- **S07/W0002**, [WORKS](../01_discovery/S07/WORKS.md) line 19: **Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates**; [ACL 2018 P18-1007](https://aclanthology.org/P18-1007/), associated 1804.10959v1
  - Original register aliases / era / family / provenance: W0002
  - Source-scoped evidence/depth: A formal abstract. arXiv extraction failed to expose abstract; formal source used.
- **S08/S08-W02**, [WORKS](../01_discovery/S08/WORKS.md) line 33: **Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates**, Kudo; ACL 2018. [Formal abstract](https://aclanthology.org/P18-1007/), [PDF](https://aclanthology.org/P18-1007.pdf). **A**.
  - Original register aliases / era / family / provenance: S08-W02 / **W0002** / catalog reuse
  - Source-scoped evidence/depth: **Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates**, Kudo; ACL 2018. [Formal abstract](https://aclanthology.org/P18-1007/), [PDF](https://aclanthology.org/P18-1007.pdf). **A**. Abstract says consistent low-resource/domain gains; actual tables, sample budget, tokenizer training cost unknown here.

<a id="BIW-0003"></a>
## BIW-0003 — SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0003`.
- **Full-source target / version:** https://arxiv.org/pdf/1808.06226v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Raw Unicode-character strings → BPE/unigram subwords → text. Tokenizer training is not end-to-end neural boundary learning.
- **Learning and causal baseline:** Raw Unicode-character strings → BPE/unigram subwords → text. Tokenizer training is not end-to-end neural boundary learning.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0242](DETAILED_INVENTORY.md#BIP-0242), [BIP-0243](DETAILED_INVENTORY.md#BIP-0243).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S07/W0003**, [WORKS](../01_discovery/S07/WORKS.md) line 20: **SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing**; [1808.06226v1](https://arxiv.org/abs/1808.06226v1), 2018
  - Original register aliases / era / family / provenance: W0003
  - Source-scoped evidence/depth: A; plus [tagged v0.2.0 schema](https://raw.githubusercontent.com/google/sentencepiece/v0.2.0/src/sentencepiece_model.proto), S, `TrainerSpec.byte_fallback` and `NormalizerSpec`. Byte fallback is documented implementation evidence, not attributed to the 2018 abstract.

<a id="BIW-0004"></a>
## BIW-0004 — CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Jonathan H. Clark, Dan Garrette, Iulia Turc, John Wieting, *CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation*, arXiv [2103.06874v4](https://arxiv.org/pdf/2103.06874v4), 18 May 2022; TACL 2022. Aliases S01/W0004, S02/W0004, S05/W0004, S06/W0004, S07/W0004. **Reading: FULL**: entire v4 PDF, §§1–6, Tables 1–8, Figures 1–2 and Appendix A, PDF pp. 1–18; Table 2 visually checked. Figures serve as architecture/data schematics, not separate measured experiments. No implementation or independent reproduction verified.

- Input is Unicode **codepoints**, not UTF-8 bytes or graphemes. Eight independent learned hash lookups with 16k buckets each are concatenated to width 768; collisions are possible. Optional character 1–4-gram hashes add memorization without input vocabulary (§3.1, p.4, footnotes 13–17). Normalization policy not independently established.
- A local-attention Transformer (blocks 128) contextualizes codepoints; stride-4 convolution compresses 2048 positions to 512; 12 global Transformer layers operate there. Sequence tasks repeat each compressed state four times, concatenate the initial representations, apply width-4 convolution and a final full-attention layer. Classification uses compressed CLS and discards the final layer (§3.1, Figure 1). This is a fixed-grid hierarchy, not predicted variable boundaries.
- Bidirectional masked encoder, not a causal next-byte generator. **CANINE-C** samples 15% whitespace-based spans, masks with private-use codepoints, and predicts selected codepoints in a shuffled autoregressive order conditioned on the masked encoded sequence and already revealed targets; labels are codepoint IDs modulo bucket count, so collisions make this no exact codepoint-probability distribution (§3.2.1, Figure 2). **CANINE-S** uses masked subword identities from a separate vocabulary, selected character-position readout and same-length random replacements; tokenizer and subword prediction head are discarded after pretraining (§3.2.2). Both use next-sentence prediction. At training targeted upsampling uses only supervised positions as queries, with full upsampled keys/values (§3.2.3); task-dependent output is labels or span endpoints, not text generation.
- Sharing axes: repeated compressed representations are spatial replication, not shared output-head parameters. Paper does not specify encoder input hash tables tied to C bucket output or S subword output, nor any two output heads shared (C and S are alternatives). Do not infer either. No generation/EOS/sampling verifier is specified.
- **Carrying card:** [R01/BIW-0004](../03_reading/R01/BIW-0004.md).
- **Canonical problem records:** [BIP-0003](DETAILED_INVENTORY.md#BIP-0003), [BIP-0004](DETAILED_INVENTORY.md#BIP-0004), [BIP-0005](DETAILED_INVENTORY.md#BIP-0005).
- **Units — input / internal / output / supervision (current):** Unicode code points / local states→stride4 latent states→queried code-point positions / task labels or masked bucket/subword heads / CANINE-C bucketed shuffled masked targets or CANINE-S subword targets, both NSP.

**Central correction P1-06; R01 metadata/result refinement:** R01 v4 full card: Table 2 CANINE-S SELECTP66.0−63.2=+2.8; CANINE-C+n-grams MINSPAN57.0−51.3=+5.7. These are different variants/metrics, not an unexplained abs-versus-HTML version reversal. §4.2 prose +3.8/+6.9 conflicts with Table 2/AppendixTable 7 +4.9/+5.7 and remains flagged. Codepoints, hash buckets, shuffled masked targets/optional subword supervision, no causal byte generator.

### Current substantive interface, technique, evidence and limits

### Interface and technique

- Input is Unicode **codepoints**, not UTF-8 bytes or graphemes. Eight independent learned hash lookups with 16k buckets each are concatenated to width 768; collisions are possible. Optional character 1–4-gram hashes add memorization without input vocabulary (§3.1, p.4, footnotes 13–17). Normalization policy not independently established.
- A local-attention Transformer (blocks 128) contextualizes codepoints; stride-4 convolution compresses 2048 positions to 512; 12 global Transformer layers operate there. Sequence tasks repeat each compressed state four times, concatenate the initial representations, apply width-4 convolution and a final full-attention layer. Classification uses compressed CLS and discards the final layer (§3.1, Figure 1). This is a fixed-grid hierarchy, not predicted variable boundaries.
- Bidirectional masked encoder, not a causal next-byte generator. **CANINE-C** samples 15% whitespace-based spans, masks with private-use codepoints, and predicts selected codepoints in a shuffled autoregressive order conditioned on the masked encoded sequence and already revealed targets; labels are codepoint IDs modulo bucket count, so collisions make this no exact codepoint-probability distribution (§3.2.1, Figure 2). **CANINE-S** uses masked subword identities from a separate vocabulary, selected character-position readout and same-length random replacements; tokenizer and subword prediction head are discarded after pretraining (§3.2.2). Both use next-sentence prediction. At training targeted upsampling uses only supervised positions as queries, with full upsampled keys/values (§3.2.3); task-dependent output is labels or span endpoints, not text generation.
- Sharing axes: repeated compressed representations are spatial replication, not shared output-head parameters. Paper does not specify encoder input hash tables tied to C bucket output or S subword output, nor any two output heads shared (C and S are alternatives). Do not infer either. No generation/EOS/sampling verifier is specified.

### Atomic findings and evidence

1. **[BIP-0003](DETAILED_INVENTORY.md#BIP-0003)** — Long fine-grained sequences make attention costly; use local character attention, stride-4 convolution, then a deep shorter stack and reconstruct only needed positions. Table 2: reimplemented mBERT 9,000 examples/s, 179M parameters; CANINE-S 6,400 examples/s, 127M; full-length character+subword supervision 900 examples/s. These are pretraining throughput on the authors' reported 64 TPUv3 setup, not serving latency or equal FLOPs. Table 6's increased stride 5/6 gains throughput but damages QA; removing targeted upsampling slows 6,400 to 5,200 examples/s. Baseline quality and throughput are not isolated architectural causal effects.
2. **[BIP-0004](DETAILED_INVENTORY.md#BIP-0004)** — Need a tokenization-independent deployed encoder without requiring vocabulary-free pretraining: CANINE-S uses subword supervision only during pretraining. Table 2 reports SELECTP F1 66.0 vs 63.2 mBERT = **+2.8**, MINSPAN 52.5 vs 51.3 = +1.2. Abstract's **+5.7** is the distinct CANINE-C+n-grams MINSPAN comparison 57.0 vs 51.3, not CANINE-S SELECTP. The §4.2 prose says +3.8 and +6.9 for the n-gram arm, inconsistent with Table 2's +4.9 and +5.7; Table 2 and Appendix Table 7 agree on +4.9/+5.7, so do not silently reconcile.
3. **[BIP-0005](DETAILED_INVENTORY.md#BIP-0005)** — Compositional encoding can lose useful lexical memorization; add hashed n-grams. Table 5: CoNLL macro F1 mBERT/CANINE-C/C+n-grams 87.8/74.0/86.7; MasakhaNER 72.4/65.5/76.8. Amharic score 50 vs mBERT 0 contributes to the latter macro difference because mBERT lacks that script; not an equal-vocabulary advantage across all languages. Error analysis reports missed rare names and split entity spans for C. N-grams also increase parameters 127M→167M (§4.4 and Appendix Table 8).

### Budgets and limits

Multilingual Wikipedia, 104 languages, smoothed sampling, 124k steps × batch 4096, reported ~2.5 corpus passes; LAMB LR .018, warmup 2.5%, 64 Cloud TPUv3 for about one day each (§4.1.3). 512 subwords vs 2048 codepoints is approximate text-context matching, not verified identical examples or raw-byte exposure; parameters counted at finetuning. QA scores average three finetuning replicas; inference costs not established. Reduced 8k hash buckets particularly hurt MINSPAN; learned ordinary character vocabulary also underperforms hashing (Table 6). Robustness to all scripts and causal use are unproven.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0004`.
- **Full-source target / version:** https://arxiv.org/pdf/2103.06874v4. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Unicode code points / stride-4 latent positions then restored code-point positions / task heads or bucketed code points / CANINE-C masked buckets or CANINE-S subwords.
- **Learning and causal baseline:** Bidirectional source encoder. Shuffled masked-target autoregression is not left-to-right text generation; optional subword target is discarded at deployment.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0003](DETAILED_INVENTORY.md#BIP-0003), [BIP-0004](DETAILED_INVENTORY.md#BIP-0004), [BIP-0005](DETAILED_INVENTORY.md#BIP-0005).
- **Reading ownership:** [R01](batches/R01.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/W0004**, [WORKS](../01_discovery/S01/WORKS.md) line 54: *CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation*, [2103.06874v4 HTML](https://arxiv.org/html/2103.06874v4), 2022-05-18
  - Original register aliases / era / family / provenance: W0004; 2021/2022 Unicode encoder; CATALOG-REUSE
  - Source-scoped evidence/depth: PARTIAL primary: §3.1–3.2.3 inspected via paginated saved response, not experiments/appendices. abs v4 reports 2.8 F1 while fetched v4 HTML abstract says 5.7; hold numeric headline until PDF identity recheck.
- **S02/W0004**, [WORKS](../01_discovery/S02/WORKS.md) line 29: Clark et al., **CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation**, [2103.06874v4](https://arxiv.org/html/2103.06874v4), 2022-05-18
  - Original register aliases / era / family / provenance: W0004; reused catalogue
  - Source-scoped evidence/depth: P: §3.1–3.2, table1; v4 abs says +2.8 F1 while HTML abstract says +5.7; table1 distinguishes CANINE-S vs CANINE-C+n-grams, so never quote an unqualified gain.
- **S05/W0004**, [WORKS](../01_discovery/S05/WORKS.md) line 19: CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation; [2103.06874v4](https://arxiv.org/abs/2103.06874v4), 2022-05-18, Clark et al.
  - Original register aliases / era / family / provenance: W0004
  - Source-scoped evidence/depth: **A**, old catalog plus fresh abs check; Unicode code-point input, downsampled internal states, character or optional subword pretraining signal; bidirectional encoder, task output. No independent old card. Abstract reports +2.8 TyDi QA F1 vs mBERT with 28% fewer parameters; source exposure and tuning not resolved by abstract.
- **S06/W0004**, [WORKS](../01_discovery/S06/WORKS.md) line 19: **CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation**; [2103.06874v4](https://arxiv.org/abs/2103.06874v4), 2022-05-18
  - Original register aliases / era / family / provenance: W0004; 2021/2022 encoder downsampling
  - Source-scoped evidence/depth: Original abstract: +2.8 TyDi QA F1 with 28% fewer parameters vs comparable mBERT. Hashing/downsampling identity also corroborated by RF W0360; full layer/FLOP/timing budget unknown here. **A**; no card.
- **S07/W0004**, [WORKS](../01_discovery/S07/WORKS.md) line 21: **CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation**; [2103.06874v4](https://arxiv.org/abs/2103.06874v4), 2022
  - Original register aliases / era / family / provenance: W0004
  - Source-scoped evidence/depth: A primary; code-point/objective details also inherited from W0360 RF, not a replacement for original method reading.

</details>

<a id="BIW-0005"></a>
## BIW-0005 — Charformer: Fast Character Transformers via Gradient-based Subword Tokenization

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Yi Tay, Vinh Q. Tran, Sebastian Ruder, Jai Gupta, Hyung Won Chung, Dara Bahri, Zhen Qin, Simon Baumgartner, Cong Yu, Donald Metzler, *Charformer: Fast Character Transformers via Gradient-based Subword Tokenization*, [arXiv 2106.12672v3](https://arxiv.org/pdf/2106.12672v3), 23 February 2022, ICLR 2022. Aliases S01/W0005, S02/W0005, S06/W0005, S07/W0005. **Reading: FULL**: v3 pp.1–20, §§1–6 and Appendix §§7.1–7.4, Tables 1–16 and Figure 3, including visual checks pp.9–10. Previous v2 fragments are not a full version-diff; specific changes versus v2 remain unverified. Reading does not verify implementation or experiments.

Input UTF-8 bytes (256 values, illegal UTF-8 discarded; paper says last 100 byte IDs reused as sentinels, §3.1 fn5). Internal output of GBST is one latent per fixed stride 2–4; Transformer encoder consumes latent sequence; decoder generates byte/sentinel sequences autoregressively. Training masks spans averaging 20 bytes and teacher-forces cross entropy to reconstruct masked spans (§2.2, §3.1). Encoder has access to the complete corrupted source, not a prefix-only stream. No causal-decoder GBST, exact online segmentation, sampling or EOS policy established. Normalization beyond stated UTF-8 filtering is not specified.
- **Carrying card:** [R01/BIW-0005](../03_reading/R01/BIW-0005.md).
- **Canonical problem records:** [BIP-0006](DETAILED_INVENTORY.md#BIP-0006), [BIP-0152](DETAILED_INVENTORY.md#BIP-0152).
- **Units — input / internal / output / supervision (current):** UTF-8 bytes / candidate block soft mixtures then fixed-stride pooled states / autoregressive byte/sentinel sequences / span denoising, mean20byte spans.

**Central correction P1-06; v3 now read:** R01 reads v3 whole method/results/appendix: soft candidate mixtures then fixed downsampling; optional global score calibration is non-prefix and disabled multilingual. Prior v2 fragments remain historical; exhaustive v2→v3 diff unverified. Appendix illustrative range excludes upper bound4, conceptual method uses1–4; actual experimental config unverified, not an occasion for repeated FULL.

### Current substantive interface, technique, evidence and limits

### Interface, mechanism, objective

Input UTF-8 bytes (256 values, illegal UTF-8 discarded; paper says last 100 byte IDs reused as sentinels, §3.1 fn5). Internal output of GBST is one latent per fixed stride 2–4; Transformer encoder consumes latent sequence; decoder generates byte/sentinel sequences autoregressively. Training masks spans averaging 20 bytes and teacher-forces cross entropy to reconstruct masked spans (§2.2, §3.1). Encoder has access to the complete corrupted source, not a prefix-only stream. No causal-decoder GBST, exact online segmentation, sampling or EOS policy established. Normalization beyond stated UTF-8 filtering is not specified.

GBST enumerates non-overlapping candidate blocks for each size b=1…M, mean-pools each, linearly scores, repeats each representation/score back across its b original byte positions, softmaxes over competing sizes per position and computes a weighted representation; a final fixed-stride mean pool sets compression (§2.1.1–2.1.5, Figure 2). The main setup uses a width-5 pre-GBST 1-D convolution rather than expensive enumeration of offset grids; convolution incorporates local ordering/context absent from simple bag means. Optional score calibration uses global score-by-score attention, permitting information from all positions; disabled on multilingual experiments. These are soft preferences, not a coherent sampled segmentation. Figure 3 is a single English example, not boundary ground truth. The simplified Appendix §7.4 uses `range(1, max_subword_block_width)` with default 4 (thus 1–3), while the conceptual description and Figure 3 discuss widths 1–4: it is illustrative code, so actual experiments' inclusion of width 4 requires separate source/config verification.

Weight axes: paper does not explicitly specify whether byte encoder/decoder input embeddings or input/output projections are tied for the reported runs; neither GBST shared scoring network across positions nor contextual mixtures establishes such tying. Output-head-to-head sharing not applicable/unspecified. No external teacher.

### Atomic findings

1. **[BIP-0006](DETAILED_INVENTORY.md#BIP-0006)** — Problem: fixed tokenization gives rigid segmentation and byte attention is expensive. Solution: learn candidate byte-block mixtures under the downstream denoising objective before fixed-rate reduction. On TyDiQA-GoldP at matched ds=4, small GBST F1 66.6 vs local-attention/strided-convolution 64.9; base 73.2 vs 70.6 (Table 7, §4.3). The paper accidentally cites Table 9 there; Table 9 is the 1.23B experiment. Raising ds from 2 to 4 worsens base 75.8→73.2. Offset enumeration did not consistently beat convolution (Table 8).
2. **[BIP-0152](DETAILED_INVENTORY.md#BIP-0152)** — Problem: total model parameters hide compute redistribution. Solution: deep/narrow encoder-heavy SBase (24 encoder/6 decoder layers, 134M) rather than the 203M base. On English GLUE average SBase 83.6 vs byte T5-SBase 82.6 and subword T5 84.3; unscaled Charformer 81.4 vs byte T5 81.5 (Table 1)—not an across-task win. Table 6: 16 TPUv3, batch 64, 1024-byte inputs, ds=3, SBase 20 steps/s, 8.7e12 forward FLOPs, 1.34 GB peak/device versus byte T5 8.2, 2.9e13, 3.09 GB. T5 subword row is 512 tokens at 9.3 steps/s; unequal raw contexts and architecture preclude a universal speedup.
3. Multilingual mC4: mT5 582M vs Charformer SBase 134M; Table 5 gives 1.54 vs 1.98 steps/s for 64 TPUv3 at batch 1024; mT5 L=1024 subword, Charformer L=2048 byte and ds=2; long-PT batch 2048 is 1.01 steps/s. Equal compressed-position exposure vs roughly equal original text are different arms; sentencepiece ≈4.1 bytes/token is an estimate, not exact alignment. F1 on multilingual TyDiQA 80.8 mT5 vs 81.2 long-PT, but zero-shot XNLI 75.4 vs 67.8 (Table 4), and byte T5 base was pretrained at 1024 rather than 2048 due to cost. Fine-tuning froze GBST for XNLI/PAWS-X; Table 16 freezing can harm XNLI at some strides. Calibration did not help multilingual. At 1.23B, Charformer 86.3 vs ByT5 87.7 F1 with ~100k fewer training steps (Appendix §7.2, Table 9).
4. Social-media classification is not synthetic typo proof: Wiki Comments accuracy Charformer Base 92.7 vs byte T5 93.2, despite higher AUC-PR 79.7 vs 75.4 (Table 2); claims must name metric. Nonconcatenative morphology and stable causal online operation remain untested.

**Training.** English C4 1M steps, batch 64, L=1024, 16 TPUv3, Adafactor inverse-square-root learning rate; multilingual mC4 101 languages, 1M steps with varied batch/length (§3, Appendix §7.1). Fine-tuning/decode serving speed, same-document identity across baseline corpora, total FLOPs/teacher/cache budgets beyond reported metrics unknown.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0005`.
- **Full-source target / version:** https://arxiv.org/pdf/2106.12672v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** 256 byte values / soft candidate-block mixtures then fixed-rate pooled positions / byte decoder / span-denoising byte targets (method inspected in v2; v3 comparison pending).
- **Learning and causal baseline:** Span-denoising encoder with full source context; byte decoder autoregressive. Encoder GBST cannot be moved into a decoder merely by adding a causal attention mask.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0006](DETAILED_INVENTORY.md#BIP-0006), [BIP-0152](DETAILED_INVENTORY.md#BIP-0152).
- **Reading ownership:** [R01](batches/R01.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/W0005**, [WORKS](../01_discovery/S01/WORKS.md) line 55: *Charformer: Fast Character Transformers via Gradient-based Subword Tokenization*, [2106.12672v3](https://arxiv.org/abs/2106.12672v3), 2022-02-23
  - Original register aliases / era / family / provenance: W0005; 2021/2022 learned local byte grouping; CATALOG-REUSE
  - Source-scoped evidence/depth: ABSTRACT only. Claimed 28–100% speed improvement is across specified task comparisons, not a universal serving multiplier. No old independent full card.
- **S02/W0005**, [WORKS](../01_discovery/S02/WORKS.md) line 30: Tay et al., **Charformer: Fast Character Transformers via Gradient-based Subword Tokenization**, [2106.12672v3 identity](https://arxiv.org/abs/2106.12672v3), 2022-02-23; **method actually read in [v2](https://arxiv.org/html/2106.12672v2)**, 2021-07-02
  - Original register aliases / era / family / provenance: W0005; reused catalogue
  - Source-scoped evidence/depth: P: v2 §§2.1–2.2, §3.1 setup. v3 HTML fetch failed. Differences v2→v3 not checked.
- **S06/W0005**, [WORKS](../01_discovery/S06/WORKS.md) line 20: **Charformer: Fast Character Transformers via Gradient-based Subword Tokenization**; [2106.12672v3](https://arxiv.org/abs/2106.12672v3), 2022-02-23
  - Original register aliases / era / family / provenance: W0005; 2021/2022 byte encoder
  - Source-scoped evidence/depth: Abstract reports 28–100% speed improvement over vanilla byte/subword Transformers; workloads/hardware and complete parameter budget not read. Candidate-block scoring is explicit, not analyst analogy. **A**.
- **S07/W0005**, [WORKS](../01_discovery/S07/WORKS.md) line 22: **Charformer: Fast Character Transformers via Gradient-based Subword Tokenization**; [2106.12672v3](https://arxiv.org/abs/2106.12672v3), 2022
  - Original register aliases / era / family / provenance: W0005
  - Source-scoped evidence/depth: A; GBST candidate/block scoring described in abstract; full objective and causality details missing.

</details>

<a id="BIW-0006"></a>
## BIW-0006 — MANTa: Efficient Gradient-Based Tokenization for Robust End-to-End Language Modeling

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Nathan Godey, Roman Castagné, Éric de la Clergerie, Benoît Sagot, *MANTa: Efficient Gradient-Based Tokenization for Robust End-to-End Language Modeling*, [arXiv 2212.07284v1](https://arxiv.org/pdf/2212.07284v1), 14 December 2022. Aliases S01/W0006, S02/W0006, S06/W0006, S07/W0006. **Reading: FULL**: whole 12-page PDF §§1–7, Limitations, Tables 1–9, Figures 1–4, Appendices A–D; Figures 3–4 and segmentation example Table 6 visually inspected. Full reading is not code verification, replication or attribution proof.

UTF-8 bytes plus span sentinels form the encoder input; a sliding-window local Transformer predicts a Bernoulli frontier probability for every byte. The cumulative frontier count defines a Poisson-binomial block-index distribution; a truncated Gaussian with matched mean/variance approximates byte-to-block membership (§3.1.1–2). Weighted byte embeddings are processed by a depthwise 1-D convolution and max pooled per block, making composition order-sensitive, then linearly projected to the T5 encoder width (§3.1.3, Appendix D). The retained block sequence is truncated to `min(LB,L/4)`, incentivizing fewer blocks; it is a hard capacity constraint, not merely an LM objective. Rounded expected block indices are used for post-hoc visualization; soft assignments are actually used during training (§6.2). Extra eligible block representations beyond the cap are discarded, so absence of text loss cannot be assumed. Appendix A caches kernel-times-byte products shared across block slots for computational savings; this is an intermediate compute cache, not an autoregressive KV cache.
- **Carrying card:** [R01/BIW-0006](../03_reading/R01/BIW-0006.md).
- **Canonical problem records:** [BIP-0007](DETAILED_INVENTORY.md#BIP-0007), [BIP-0153](DETAILED_INVENTORY.md#BIP-0153), [BIP-0154](DETAILED_INVENTORY.md#BIP-0154).
- **Units — input / internal / output / supervision (current):** UTF-8 bytes / Gaussian soft byte-to-block assignment, depthwiseCNN/max, retained≤L/4blocks / autoregressive byte/sentinel targets / span denoising; hard length bottleneck, not task loss alone.

**Central correction P1-06; metadata and evidence refinement:** R01 confirms authors Nathan Godey, Roman Castagné, Éric de la Clergerie, Benoît Sagot; Gaussian soft assignment, order-sensitive depthwise CNN/max pooling, hardL/4 truncation and autoregressive byte decoder. No-truncation degeneration is qualitative, not a missing quantified table to invent. Clean-to-noisy separation is weak without adaptation;2.61/9.06s train steps is not decode latency.

### Current substantive interface, technique, evidence and limits

### Input, mechanism and causality

UTF-8 bytes plus span sentinels form the encoder input; a sliding-window local Transformer predicts a Bernoulli frontier probability for every byte. The cumulative frontier count defines a Poisson-binomial block-index distribution; a truncated Gaussian with matched mean/variance approximates byte-to-block membership (§3.1.1–2). Weighted byte embeddings are processed by a depthwise 1-D convolution and max pooled per block, making composition order-sensitive, then linearly projected to the T5 encoder width (§3.1.3, Appendix D). The retained block sequence is truncated to `min(LB,L/4)`, incentivizing fewer blocks; it is a hard capacity constraint, not merely an LM objective. Rounded expected block indices are used for post-hoc visualization; soft assignments are actually used during training (§6.2). Extra eligible block representations beyond the cap are discarded, so absence of text loss cannot be assumed. Appendix A caches kernel-times-byte products shared across block slots for computational savings; this is an intermediate compute cache, not an autoregressive KV cache.

Encoder frontier/local aggregation can inspect the corrupted source around each byte; it is not a proven causal streaming grouping method. Decoder uses an autoregressive byte/sentinel output, teacher-conditioned on prior target bytes and full encoded corrupted source. 15% random bytes in spans averaging 20 bytes are replaced with sentinels, which also label reconstructed spans (§3.2.1). No exact output EOS/invalid UTF-8 handling or production sampling/verifier was specified. No explicit encoder input ↔ decoder input, input ↔ output, or output-head ↔ output-head weight-sharing specification found; do not infer it from T5 ancestry. No teacher or distillation is used.

### Problem–solution evidence and boundaries

1. **[BIP-0007](DETAILED_INVENTORY.md#BIP-0007)** — For rigid vocabulary and expensive fine-grained encoding, learn local frontier probabilities jointly with byte denoising, approximate block membership and feed order-sensitive soft pooled representations to a compressed encoder. Without the `L/4` bottleneck, §6.1 reports the block count often degenerates to approximately one per byte, hurting speed and eventual quality; the paper provides no quantified matched ablation. Gaussian assignment is not an exact sum over segmentations, nor proof that discovered segments are linguistic words.
2. **[BIP-0153](DETAILED_INVENTORY.md#BIP-0153)** — Adapt to unfamiliar domains/noise by allowing segmentation to update during fine-tuning. MedNLI accuracy: 57M MANTa-Small 75.6 vs T5-Small 75.3; 125M CharacterBERT 77.9 and BERT 77.7 use different corpora/model allocation (Table 3). Toxic comments: 200M MANTa 93.2 vs Charformer 92.7 and T5 91.5, latter results external (Table 4). Synthetic SST-2 Figure 3: deleting/replacing/inserting random bytes at 5/10/15%, clean-trained models are similarly degraded; when fine-tuned on noisy data MANTa and ByT5 are better retained than T5. This is not evidence of broad clean-to-noisy superiority, multilingual robustness or a causal segmentation-only gain.
3. **[BIP-0154](DETAILED_INVENTORY.md#BIP-0154)** — Training speed is controlled separately from text exposure. Table 5: 16 V100, batch 1024, 1024 bytes vs 256 subword tokens, MANTa 2.61 s/step, 57M byte T5 9.06, 60M T5 1.13; ≈3.47× rather than exactly 4× faster than that byte baseline and 2.31× slower than subword. Not a decoding latency measurement. Model's Limitations expressly says byte-by-byte decoding adds generation cost. Small scaled ByT5 has a different architecture and is trained 200k steps at batch 64 under a same-training-time budget; MANTa/T5 train 65k at batch 1024, so these are not same-byte comparisons. MANTa 65k×1024 sequences at L=1024/2048 versus prior Charformer 1M×64 has roughly comparable nominal input positions, not exactly matched original text.
4. GLUE dev small: MANTa 77.1 vs T5 76.6; base 80.3 vs Charformer 81.4 and T5 84.3, different training batches/cited experiments (Tables 1–2). Appendix C test average 78.7 is a separate test result, not dev. English only; hyperparameter search limited (§6.4).

**Training** English mC4 C4-compatible split; documents over 2^15 bytes filtered (§3.2.1). Adafactor LR 0.01 for encoder-decoder and 0.001 for embedding/frontier/pooling, triangular schedule and warmup; small/base 57M/200M. Small/base frontier layers 1/2, attention window 16, depthwise kernel 3, 64/128 byte-embedding width (Appendix B). Total exact raw byte exposure, inference budget, and exact parameter tying unknown.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0006`.
- **Full-source target / version:** https://arxiv.org/pdf/2212.07284v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes / soft variable blocks with quarter-length truncation / bytes and sentinels / span-denoising targets.
- **Learning and causal baseline:** Encoder segmentation uses full corrupted source; decoder emits bytes serially. Gaussian assignment and bottleneck support training, not a prefix-streaming guarantee.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0007](DETAILED_INVENTORY.md#BIP-0007), [BIP-0153](DETAILED_INVENTORY.md#BIP-0153), [BIP-0154](DETAILED_INVENTORY.md#BIP-0154).
- **Reading ownership:** [R01](batches/R01.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/W0006**, [WORKS](../01_discovery/S01/WORKS.md) line 56: *MANTa: Efficient Gradient-Based Tokenization for Robust End-to-End Language Modeling*, [2212.07284v1](https://arxiv.org/abs/2212.07284), 2022-12-14
  - Original register aliases / era / family / provenance: W0006; 2022 differentiable byte tokenizer; CATALOG-REUSE
  - Source-scoped evidence/depth: ABSTRACT here; old recovery method notes are secondary leads. English GLUE, out-of-domain and synthetic perturbations; precise costs unknown here.
- **S02/W0006**, [WORKS](../01_discovery/S02/WORKS.md) line 31: Godey, de la Clergerie & Sagot, **MANTa: Efficient Gradient-Based Tokenization for Robust End-to-End Language Modeling**, [2212.07284v1](https://arxiv.org/html/2212.07284v1), 2022-12-14
  - Original register aliases / era / family / provenance: W0006; reused catalogue
  - Source-scoped evidence/depth: P: §§3.1–3.2, §5, §§6.1–6.4, Limitations; tables with missing cells not reconstructed. Fixed v1 resolves the older recovery audit’s unknown HTML version.
- **S06/W0006**, [WORKS](../01_discovery/S06/WORKS.md) line 21: **MANTa: Efficient Gradient-Based Tokenization for Robust End-to-End Language Modeling**; [2212.07284v1](https://arxiv.org/abs/2212.07284), 2022-12-14
  - Original register aliases / era / family / provenance: W0006; 2022 differentiable tokenizer
  - Source-scoped evidence/depth: Abstract: faster than strict byte model with comparable GLUE/robustness. Recovery notes encoder-only shortening; do not upgrade that into a newly verified complete timing comparison. **A**.
- **S07/W0006**, [WORKS](../01_discovery/S07/WORKS.md) line 23: **MANTa: Efficient Gradient-Based Tokenization for Robust End-to-End Language Modeling**; [2212.07284v1](https://arxiv.org/abs/2212.07284v1), 2022
  - Original register aliases / era / family / provenance: W0006
  - Source-scoped evidence/depth: A primary; recovery audit's targeted mechanism reading is reused but not upgraded to FULL.

</details>

<a id="BIW-0007"></a>
## BIW-0007 — Efficient Transformers with Dynamic Token Pooling

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **状态：全文精读**。Piotr Nawrot、Jan Chorowski、Adrian Łańcucki、Edoardo M. Ponti，ACL 2023；[DOI 10.18653/v1/2023.acl-long.353](https://doi.org/10.18653/v1/2023.acl-long.353)，[会议PDF](https://aclanthology.org/2023.acl-long.353.pdf)；实际读取[arXiv 2211.09761v2 HTML](https://arxiv.org/html/2211.09761) 的§1–8、表1–2、图3–5文字及附录A–B；图形曲线未逐点数字化，代码未审。HTML正文§3.2存在一处“does include future information”笔误，紧随的因果解释和公式明确要求不含未来。
- **Carrying card:** [old scoped FULL/BIW-0007](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md).
- **Canonical problem records:** [BIP-0008](DETAILED_INVENTORY.md#BIP-0008), [BIP-0009](DETAILED_INVENTORY.md#BIP-0009), [BIP-0010](DETAILED_INVENTORY.md#BIP-0010), [BIP-0011](DETAILED_INVENTORY.md#BIP-0011), [BIP-0012](DETAILED_INVENTORY.md#BIP-0012).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** **Characters**, not UTF-8 → contiguous mean-pooled segments → next characters; unigram labels, own-model entropy labels, Gumbel task gradients, or spaces. Completed-segment delay maintains causality.
- **Learning and causal baseline:** **Characters**, not UTF-8 → contiguous mean-pooled segments → next characters; unigram labels, own-model entropy labels, Gumbel task gradients, or spaces. Completed-segment delay maintains causality.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0007`.
- **Full-source target / version:** https://arxiv.org/pdf/2211.09761v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **Characters**, not UTF-8 → contiguous mean-pooled segments → next characters; unigram labels, own-model entropy labels, Gumbel task gradients, or spaces. Completed-segment delay maintains causality.
- **Learning and causal baseline:** **Characters**, not UTF-8 → contiguous mean-pooled segments → next characters; unigram labels, own-model entropy labels, Gumbel task gradients, or spaces. Completed-segment delay maintains causality.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md). Scope header: **状态：全文精读**。Piotr Nawrot、Jan Chorowski、Adrian Łańcucki、Edoardo M. Ponti，ACL 2023；[DOI 10.18653/v1/2023.acl-long.353](https://doi.org/10.18653/v1/2023.acl-long.353)，[会议PDF](https://aclanthology.org/2023.acl-long.353.pdf)；实际读取[arXiv 2211.09761v2 HTML](https://arxiv.org/html/2211.09761) 的§1–8、表1–2、图3–5文字及附录A–B；图形曲线未逐点数字化，代码未审。HTML正文§3.2存在一处“does include future information”笔误，紧随的因果解释和公式明确要求不含未来。
- **Canonical problems:** [BIP-0008](DETAILED_INVENTORY.md#BIP-0008), [BIP-0009](DETAILED_INVENTORY.md#BIP-0009), [BIP-0010](DETAILED_INVENTORY.md#BIP-0010), [BIP-0011](DETAILED_INVENTORY.md#BIP-0011), [BIP-0012](DETAILED_INVENTORY.md#BIP-0012).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S02/W0007**, [WORKS](../01_discovery/S02/WORKS.md) line 43: Nawrot et al., **Efficient Transformers with Dynamic Token Pooling**, [ACL2023](https://aclanthology.org/2023.acl-long.353/); card actually reads 2211.09761v2
  - Original register aliases / era / family / provenance: W0007; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B05/W0007.md`; §§1–8,A–B per card.
- **S03/W0007**, [WORKS](../01_discovery/S03/WORKS.md) line 17: W0007 · Efficient Transformers with Dynamic Token Pooling (2023); [2211.09761v2](https://arxiv.org/html/2211.09761v2), ACL 2023.acl-long.353 C: [B05/W0007](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md), all card text
  - Original register aliases / era / family / provenance: W0007 · Efficient Transformers with Dynamic Token Pooling (2023); [2211.09761v2](https://arxiv.org/html/2211.09761v2), ACL 2023.acl-long.353
  - Source-scoped evidence/depth: C: [B05/W0007](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md), all card text
- **S06/W0007**, [WORKS](../01_discovery/S06/WORKS.md) line 22: **Efficient Transformers with Dynamic Token Pooling**; [2211.09761v2](https://arxiv.org/html/2211.09761v2), associated [ACL2023](https://aclanthology.org/2023.acl-long.353/); [old card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md)
  - Original register aliases / era / family / provenance: W0007; 2023 character pooling
  - Source-scoped evidence/depth: ~41M parameters; ~1M boundary network overhead. text8 SF=4 training step ~2.5× faster, memory/resource reduction 50–60%, GV100 32GB; not per-method end-to-end generation. **RF** §§3–5/Fig.5.
- **S08/S08-W21**, [WORKS](../01_discovery/S08/WORKS.md) line 52: **Efficient Transformers with Dynamic Token Pooling**, ACL 2023; actual card reads [2211.09761v2](https://arxiv.org/html/2211.09761v2). **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md).
  - Original register aliases / era / family / provenance: S08-W21 / **W0007** / catalog reuse
  - Source-scoped evidence/depth: **Efficient Transformers with Dynamic Token Pooling**, ACL 2023; actual card reads [2211.09761v2](https://arxiv.org/html/2211.09761v2). **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md). ~41M, cleaned corpora, 3 seeds. Text8 whitespace 1.133 BPC vs Unigram1.134/Gumbel1.136; rates differ. Finnish counterexample to universal whitespace superiority; exact per-method end-to-end generation time absent.

</details>

<a id="BIW-0008"></a>
## BIW-0008 — MEGABYTE: Predicting Million-byte Sequences with Multiscale Transformers

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Lili Yu, Dániel Simig, Colin Flaherty, Armen Aghajanyan, Luke Zettlemoyer, Mike Lewis; [arXiv 2305.07185v2, 19 May 2023](https://arxiv.org/pdf/2305.07185v2). Aliases: S01/W0008, S02/W0008, S03/W0008, S06/W0008.

**Reading depth: FULL, fresh.** Read PDF pp. 1–9 §§1–10, Tables 1–10, Figures 1–5; pp. 12–16 Appendices A–D, Tables 11–14 and pseudocode. Figure 4/5 and Table 7 were visually checked on p. 8. References pp. 10–12 were consulted as needed. Full means the paper and its carrying appendix were read, not that its code, numerical results, or sampling correctness were reproduced. The paper does not specify all prompting, EOS, or deployment-cache details.
- **Carrying card:** [R03/BIW-0008](../03_reading/R03/BIW-0008.md).
- **Canonical problem records:** [BIP-0013](DETAILED_INVENTORY.md#BIP-0013), [BIP-0014](DETAILED_INVENTORY.md#BIP-0014), [BIP-0015](DETAILED_INVENTORY.md#BIP-0015), [BIP-0169](DETAILED_INVENTORY.md#BIP-0169), [BIP-0170](DETAILED_INVENTORY.md#BIP-0170), [BIP-0284](DETAILED_INVENTORY.md#BIP-0284).
- **Units — input / internal / output / supervision (current):** 256bytes / concatenatedfixedPbyte globalpatches+causal local bytestates / next-bytecategorical / next-byteAR likelihood; globalshiftonepatch/localshiftonebyte.

**Central correction P1-04:** MEGABYTE2305.07185v2 §2.2 Eqs4/6 explicitly reuse E_local-embed for local byte input and local output. Global input table and global/local layer sharing are different unspecified axes; paper specification is now confirmed by R03 FULL card, not runtime alias certification.

### Current substantive interface, technique, evidence and limits

**Reading depth: FULL, fresh.** Read PDF pp. 1–9 §§1–10, Tables 1–10, Figures 1–5; pp. 12–16 Appendices A–D, Tables 11–14 and pseudocode. Figure 4/5 and Table 7 were visually checked on p. 8. References pp. 10–12 were consulted as needed. Full means the paper and its carrying appendix were read, not that its code, numerical results, or sampling correctness were reproduced. The paper does not specify all prompting, EOS, or deployment-cache details.

### Interface, task, and causal contract

Text input and supervised targets are bytes with vocabulary 256; internal units are fixed P-byte patches, concatenated byte embeddings and a shorter global Transformer sequence, plus an autoregressive local Transformer within each patch; output is a categorical next-byte distribution. Raw image and audio bytes use the same architectural idea but are distinct evidence, not language results. Normalization and document-boundary/EOS conventions are not fully specified. A global input patch is shifted one entire patch; the local byte inputs are shifted one byte and start with local padding. Masked attention thus makes each patch's global signal depend on earlier patches, and its local output on preceding bytes in that patch (§2.2, Eqs. 2–6; Fig. 1–2; Appendix B). Its within-patch joint is a product of conditional byte distributions, not parallel independent byte predictions. No speculative verifier is involved; arbitrary partial-patch prompts and EOS policy are not explicitly specified.

The paper's Eq. 4 and Eq. 6 use **the same local byte embedding matrix for local input lookup and local output projection**. This is an explicit paper-level input/output tying specification, not verified tensor aliasing. Global byte input embeddings are separately named, and global/local layer sharing and any source/target or multi-head tying are not specified.

### Atomic problem / solution / actual techniques

- **BIP-0013, BIP-0014:** Per-byte large-model attention and feed-forward work limits context and compute. **Solution:** run a large causal Transformer once per fixed patch and a smaller causal Transformer for each patch's bytes. Techniques: concatenation/reshape preserves within-patch positional input, masked attention supplies global/local context, and a learned linear projection passes global to local (§2, §3). For full attention the theoretical cost is O(T²/P²+TP), O(T^(4/3)) when P∝T^(1/3); this is not a measured end-to-end serving bound.
- **BIP-0015:** Independent parallel byte heads cannot represent dependencies such as the exclusive alternatives “cat” and “dog.” **Solution:** locally autoregress over bytes (§2.4), preserving dependency at serial local decode cost. No claim of parallel exact block generation.
- **BIP-0169 / BIP-0170:** Patch offset causes nonuniform within-patch quality and may lose local cross-boundary context. **Solution:** optional causal convolutions (widths 3, 5, 7) in patch embedding, optional local cross-patch attention, and/or two half-patch-offset scoring passes. Rotary embeddings represent relative positions for cross-patch attention (§2.3); cross-patch is not mandatory.
- **BIP-0284:** Headline speed/quality comparisons can mix contexts and scoring work. **Solution in the evaluation:** match per-byte forward time approximately and train on equal byte exposure (§4.1), then separately report more expensive evaluation variants. Equal measured forward time is not exact equality of FLOPs, parameters, all training costs, or inference cost.

### Evidence, controls, budgets, and negative results

- Table 2, §5: on five text sets each trained for **80B bytes**, PG19 BPB is 1.000 versus Transformer 1.057 and PerceiverAR 1.104; Code 0.411 versus 0.575 and 0.546. Global/local 758M/262M, patch 8, context 8192 bytes; Transformer 320M/1024 bytes; PerceiverAR 248M, 8192-byte input and 1024 latents. Contexts and total parameters differ despite the paper's matched-speed/data design. Training data sizes and mean document lengths are Table 1.
- §5 / Table 3: 400B-byte training PG19 word-level perplexity is 36.4 versus byte Transformer 69.4 and byte PerceiverAR 88.8. Prior subword BlockRecurrent 26.5 and PerceiverAR 28.9 are not matched-recipe controls; word-normalized scoring here is an author's conversion, not proof of token-path/text-marginal equivalence. Table 3 combines published results with differing contexts and budgets.
- Table 6, §8.1: generate 8192 bytes: 350M Transformer 132 seconds versus 1.3B global + 218M local 93 seconds, patch 8; contexts 1024 versus 8192 and BPB 1.064 versus 0.991. Paper calls this about 40% faster; 93/132 is about 0.70 elapsed time. The excerpt does not state hardware/batch/cache settings for this timing; do not generalize it to production latency.
- Table 7: on arXiv, base 0.6871 BPB, no local 1.263, no global 1.373, no cross-patch 0.6781 and CNN 0.6871; ablations are compute/data controlled, not identical parameter configurations. Audio/image differ. Table 8, PG19: basic 0.9079 at 1× inference; strided 0.8926 at 2×; sliding 0.8918 at 2×; both 0.8751 at 4×. Thus strided scoring is not ordinary single-pass serving quality. Fig. 4 shows improving position-wise likelihood through an 8K window; it does not establish million-byte language use. D.3, Table 14: 8192 vs 16384-byte contexts yield 0.8751 vs 0.8787, no longer-context gain in that setup. Million-byte result is ImageNet640, not language.
- Appendix A: Adam, warmup 500, dropout .1, weight decay .1, gradient norm 1, mixed precision. No teacher is reported; detailed serving cache and end-to-end FLOPs are unknown. Appendix C acknowledges PerceiverAR implementation deviations.

**Inventory handoff:** retain separate causal factorization, data/context budgets, precise local tying axis, scoring-cost and modality scope for [BIP-0013](DETAILED_INVENTORY.md#BIP-0013), [0014](DETAILED_INVENTORY.md#BIP-0014), [0015](DETAILED_INVENTORY.md#BIP-0015), [0169](DETAILED_INVENTORY.md#BIP-0169), [0170](DETAILED_INVENTORY.md#BIP-0170), [0284](DETAILED_INVENTORY.md#BIP-0284).


**Current R1 adjudication ([FULL_READING_AUDIT_R1](../05_review/FULL_READING_AUDIT_R1.md)):** 132→93seconds for the same8192bytes is about29.5%less elapsed time or1.42×throughput; the paper’s “40%faster” can refer to rate, not40%time reduction. Best0.8751BPB costs4×basic scoring, not free single-pass serving.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0008`.
- **Full-source target / version:** https://arxiv.org/pdf/2305.07185v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes / fixed global patches plus local byte states / bytes / next-byte likelihood.
- **Learning and causal baseline:** Global input shifted one patch, local input one byte. Local autoregressive conditioning defines the patch joint; teacher-forced patch parallelism is not independent unknown-byte sampling.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0013](DETAILED_INVENTORY.md#BIP-0013), [BIP-0014](DETAILED_INVENTORY.md#BIP-0014), [BIP-0015](DETAILED_INVENTORY.md#BIP-0015), [BIP-0169](DETAILED_INVENTORY.md#BIP-0169), [BIP-0170](DETAILED_INVENTORY.md#BIP-0170), [BIP-0284](DETAILED_INVENTORY.md#BIP-0284).
- **Reading ownership:** [R03](batches/R03.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/W0008**, [WORKS](../01_discovery/S01/WORKS.md) line 57: *MEGABYTE: Predicting Million-byte Sequences with Multiscale Transformers*, [2305.07185v2](https://arxiv.org/abs/2305.07185v2), 2023-05-19
  - Original register aliases / era / family / provenance: W0008; 2023 fixed-patch byte hierarchy; CATALOG-REUSE
  - Source-scoped evidence/depth: ABSTRACT only. Use language modeling experiment claim only; image/audio million-byte results are not independent language evidence.
- **S02/W0008**, [WORKS](../01_discovery/S02/WORKS.md) line 44: Yu et al., **MEGABYTE: Predicting Million-byte Sequences with Multiscale Transformers**, [2305.07185v2](https://arxiv.org/html/2305.07185v2), 2023-05-19
  - Original register aliases / era / family / provenance: W0008; reused catalogue
  - Source-scoped evidence/depth: P: §2.1–2.2 and introductory mechanism; full tables/appendix not read. Header extraction omits first author; old catalogue supplies Yu et al.
- **S03/W0008**, [WORKS](../01_discovery/S03/WORKS.md) line 18: W0008 · MEGABYTE: Predicting Million-byte Sequences with Multiscale Transformers (2023); [2305.07185v2](https://arxiv.org/html/2305.07185v2) P: original §2.1–2.4, §3.2 generation serial-path paragraph; search-located PG19/appendix D.3 statements, not full tables/appendices
  - Original register aliases / era / family / provenance: W0008 · MEGABYTE: Predicting Million-byte Sequences with Multiscale Transformers (2023); [2305.07185v2](https://arxiv.org/html/2305.07185v2)
  - Source-scoped evidence/depth: P: original §2.1–2.4, §3.2 generation serial-path paragraph; search-located PG19/appendix D.3 statements, not full tables/appendices
- **S06/W0008**, [WORKS](../01_discovery/S06/WORKS.md) line 23: **MEGABYTE: Predicting Million-byte Sequences with Multiscale Transformers**; [2305.07185v2](https://arxiv.org/abs/2305.07185v2), 2023-05-19
  - Original register aliases / era / family / provenance: W0008; 2023 fixed-patch decoder
  - Source-scoped evidence/depth: Abstract supports subquadratic attention and improved decoding parallelism, competitive long-context subword LM; exact language context, global+local total parameters, measured generation hardware absent here. Million-byte multimodal capability is not a language throughput result. **A**.

</details>

<a id="BIW-0009"></a>
## BIW-0009 — SpaceByte: Towards Deleting Tokenization from Large Language Modeling

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **状态：全文精读**。Kevin Slagle，2024；[arXiv:2404.14408v3](https://arxiv.org/html/2404.14408v3)，NeurIPS 2024。实际读HTML §1–7、图3及表1–2、限制、附录A.1和C伪代码，附录B只定向核查总训练成本；其余附录未逐项精读，图形曲线未逐点数字化。HTML顶端抽取漏了标题前缀及作者，以[官方元数据](https://export.arxiv.org/api/query?id_list=2404.14408)核正；代码未独立执行。
- **Carrying card:** [old scoped FULL/BIW-0009](../../flued_multigranularity_survey_20261108/03_reading/B05/W0009.md).
- **Canonical problem records:** [BIP-0016](DETAILED_INVENTORY.md#BIP-0016), [BIP-0017](DETAILED_INVENTORY.md#BIP-0017).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Bytes → selected contextual byte states → next bytes; **fixed spacelike rule**, no boundary gradient. Causal observed-byte triggers; not whole-word pooling.
- **Learning and causal baseline:** Bytes → selected contextual byte states → next bytes; **fixed spacelike rule**, no boundary gradient. Causal observed-byte triggers; not whole-word pooling.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0009`.
- **Full-source target / version:** https://arxiv.org/pdf/2404.14408v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes → selected contextual byte states → next bytes; **fixed spacelike rule**, no boundary gradient. Causal observed-byte triggers; not whole-word pooling.
- **Learning and causal baseline:** Bytes → selected contextual byte states → next bytes; **fixed spacelike rule**, no boundary gradient. Causal observed-byte triggers; not whole-word pooling.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0009.md). Scope header: **状态：全文精读**。Kevin Slagle，2024；[arXiv:2404.14408v3](https://arxiv.org/html/2404.14408v3)，NeurIPS 2024。实际读HTML §1–7、图3及表1–2、限制、附录A.1和C伪代码，附录B只定向核查总训练成本；其余附录未逐项精读，图形曲线未逐点数字化。HTML顶端抽取漏了标题前缀及作者，以[官方元数据](https://export.arxiv.org/api/query?id_list=2404.14408)核正；代码未独立执行。
- **Canonical problems:** [BIP-0016](DETAILED_INVENTORY.md#BIP-0016), [BIP-0017](DETAILED_INVENTORY.md#BIP-0017).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S02/W0009**, [WORKS](../01_discovery/S02/WORKS.md) line 45: Slagle, **SpaceByte: Towards Deleting Tokenization from Large Language Modeling**, [2404.14408v3](https://arxiv.org/html/2404.14408v3)
  - Original register aliases / era / family / provenance: W0009; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B05/W0009.md`; definition/text inconsistency retained in card.
- **S03/W0009**, [WORKS](../01_discovery/S03/WORKS.md) line 19: W0009 · SpaceByte: Towards Deleting Tokenization from Large Language Modeling (2024); [2404.14408v3](https://arxiv.org/html/2404.14408v3) C: [B05/W0009](../../flued_multigranularity_survey_20261108/03_reading/B05/W0009.md)
  - Original register aliases / era / family / provenance: W0009 · SpaceByte: Towards Deleting Tokenization from Large Language Modeling (2024); [2404.14408v3](https://arxiv.org/html/2404.14408v3)
  - Source-scoped evidence/depth: C: [B05/W0009](../../flued_multigranularity_survey_20261108/03_reading/B05/W0009.md)
- **S05/W0009**, [WORKS](../01_discovery/S05/WORKS.md) line 20: SpaceByte: Towards Deleting Tokenization from Large Language Modeling; [2404.14408v3](https://arxiv.org/html/2404.14408v3), Slagle, 2024
  - Original register aliases / era / family / provenance: W0009
  - Source-scoped evidence/depth: **RC** [B05 card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0009.md). UTF-8 byte → selected causal positions/global states → byte, next-byte loss. Exact lead/continuation rule, compute-frontier comparisons, preliminary Chinese failure; card itself states some appendices were only targeted.
- **S06/W0009**, [WORKS](../01_discovery/S06/WORKS.md) line 24: **SpaceByte: Towards Deleting Tokenization from Large Language Modeling**; [2404.14408v3](https://arxiv.org/html/2404.14408v3); [card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0009.md)
  - Original register aliases / era / family / provenance: W0009; 2024 rule-based local/global
  - Source-scoped evidence/depth: 10^18/10^19 training-FLOP grids; quality versus inference-FLOPs/byte. At each architecture's optimum PG19 1.009 vs SentencePiece .989 BPB, arXiv .748 vs .768, GitHub .500 vs .508. No general measured decode speedup. **RF** §§2,4–7/App.C.
- **S08/S08-W22**, [WORKS](../01_discovery/S08/WORKS.md) line 53: **SpaceByte: Towards Deleting Tokenization from Large Language Modeling**, [2404.14408v3](https://arxiv.org/html/2404.14408v3), 2024. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0009.md).
  - Original register aliases / era / family / provenance: S08-W22 / **W0009** / catalog reuse
  - Source-scoped evidence/depth: **SpaceByte: Towards Deleting Tokenization from Large Language Modeling**, [2404.14408v3](https://arxiv.org/html/2404.14408v3), 2024. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0009.md). 10^18/10^19 FLOP grids; PG19 1.009 vs SentencePiece .989, arXiv .748/.768, GitHub .500/.508 at separately optimized inference points. Chinese limitation admitted without table. Dynamic implementation and formal rule wording discrepancy retained.

</details>

<a id="BIW-0010"></a>
## BIW-0010 — Byte Latent Transformer: Patches Scale Better Than Tokens

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **状态：全文精读（会议版）**。Artidoro Pagnoni、Ram Pasunuru、Pedro Rodriguez、John Nguyen、Benjamin Muller、Margaret Li、Chunting Zhou、Lili Yu、Jason Weston、Luke Zettlemoyer、Gargi Ghosh、Mike Lewis、Ari Holtzman、Srinivasan Iyer；ACL 2025，[DOI 10.18653/v1/2025.acl-long.453](https://doi.org/10.18653/v1/2025.acl-long.453)，关联[arXiv:2412.09871v1](https://arxiv.org/abs/2412.09871v1)。实际获取并转读[会议PDF](https://aclanthology.org/2025.acl-long.453.pdf) §1–10、表1–5和附录B–H、L–Q的相关段落，尤其H算量、N上下文、P分段消融；未列附录及上述附录中不相关部分未逐项精读，双栏转换会交错邻列，图中曲线未逐点数字化。HTML v1抓取在§5开头截断，故以会议PDF为准；未比较两版逐项差异、未审核代码。
- **Carrying card:** [old scoped FULL/BIW-0010](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md).
- **Canonical problem records:** [BIP-0018](DETAILED_INVENTORY.md#BIP-0018), [BIP-0019](DETAILED_INVENTORY.md#BIP-0019), [BIP-0020](DETAILED_INVENTORY.md#BIP-0020), [BIP-0021](DETAILED_INVENTORY.md#BIP-0021), [BIP-0022](DETAILED_INVENTORY.md#BIP-0022).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Bytes + hashed byte n-grams → entropy patches/cross-attention latents → next bytes; **separate causal byte-LM teacher**, not jointly optimized boundaries.
- **Learning and causal baseline:** Bytes + hashed byte n-grams → entropy patches/cross-attention latents → next bytes; **separate causal byte-LM teacher**, not jointly optimized boundaries.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0010`.
- **Full-source target / version:** https://aclanthology.org/2025.acl-long.453.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes + hashed byte n-grams → entropy patches/cross-attention latents → next bytes; **separate causal byte-LM teacher**, not jointly optimized boundaries.
- **Learning and causal baseline:** Bytes + hashed byte n-grams → entropy patches/cross-attention latents → next bytes; **separate causal byte-LM teacher**, not jointly optimized boundaries.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md). Scope header: **状态：全文精读（会议版）**。Artidoro Pagnoni、Ram Pasunuru、Pedro Rodriguez、John Nguyen、Benjamin Muller、Margaret Li、Chunting Zhou、Lili Yu、Jason Weston、Luke Zettlemoyer、Gargi Ghosh、Mike Lewis、Ari Holtzman、Srinivasan Iyer；ACL 2025，[DOI 10.18653/v1/2025.acl-long.453](https://doi.org/10.18653/v1/2025.acl-long.453)，关联[arXiv:2412.09871v1](https://arxiv.org/abs/2412.09871v1)。实际获取并转读[会议PDF](https://aclanthology.org/2025.acl-long.453.pdf) §1–10、表1–5和附录B–H、L–Q的相关段落，尤其H算量、N上下文、P分段消融；未列附录及上述附录中不相关部分未逐项精读，双栏转换会交错邻列，图中曲线未逐点数字化。HTML v1抓取在§5开头截断，故以会议PDF为准；未比较两版逐项差异、未审核代码。
- **Canonical problems:** [BIP-0018](DETAILED_INVENTORY.md#BIP-0018), [BIP-0019](DETAILED_INVENTORY.md#BIP-0019), [BIP-0020](DETAILED_INVENTORY.md#BIP-0020), [BIP-0021](DETAILED_INVENTORY.md#BIP-0021), [BIP-0022](DETAILED_INVENTORY.md#BIP-0022).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S01/W0010**, [WORKS](../01_discovery/S01/WORKS.md) line 58: *Byte Latent Transformer: Patches Scale Better Than Tokens*, [ACL 2025.453 PDF](https://aclanthology.org/2025.acl-long.453.pdf); [old FULL card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md)
  - Original register aliases / era / family / provenance: W0010; 2024/ACL 2025 learned local byte encoder; CATALOG-REUSE
  - Source-scoped evidence/depth: Reused FULL card actually read. §3, Table 4/5, appendix H/P references inherited from card; teacher compute and original-text exposures not fully matched.
- **S02/W0010**, [WORKS](../01_discovery/S02/WORKS.md) line 46: Pagnoni et al., **Byte Latent Transformer: Patches Scale Better Than Tokens**, [ACL2025 formal PDF](https://aclanthology.org/2025.acl-long.453.pdf)
  - Original register aliases / era / family / provenance: W0010; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B05/W0010.md`; formal PDF rather than an unexamined arXiv update.
- **S03/W0010**, [WORKS](../01_discovery/S03/WORKS.md) line 20: W0010 · Byte Latent Transformer: Patches Scale Better Than Tokens (2024/ACL 2025); [formal PDF](https://aclanthology.org/2025.acl-long.453.pdf) C: [B05/W0010](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md)
  - Original register aliases / era / family / provenance: W0010 · Byte Latent Transformer: Patches Scale Better Than Tokens (2024/ACL 2025); [formal PDF](https://aclanthology.org/2025.acl-long.453.pdf)
  - Source-scoped evidence/depth: C: [B05/W0010](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md)
- **S04/W0010**, [WORKS](../01_discovery/S04/WORKS.md) line 25: **W0010**, 2024/ACL2025, *Byte Latent Transformer: Patches Scale Better Than Tokens*; [ACL paper](https://aclanthology.org/2025.acl-long.453.pdf) CATALOG reuse; F-card `OLD/03_reading/B05/W0010.md`
  - Original register aliases / era / family / provenance: **W0010**, 2024/ACL2025, *Byte Latent Transformer: Patches Scale Better Than Tokens*; [ACL paper](https://aclanthology.org/2025.acl-long.453.pdf)
  - Source-scoped evidence/depth: CATALOG reuse; F-card `OLD/03_reading/B05/W0010.md` Causal offsets/local windows; separately trained default 100M entropy model. Up to 8B tests vs Llama3. 8B equal-FLOP comparison not equal bytes; entropy teacher not separately costed in principal formula. §§3/4/7/10 relevant. Tying status unknown.
- **S06/W0010**, [WORKS](../01_discovery/S06/WORKS.md) line 25: **Byte Latent Transformer: Patches Scale Better Than Tokens**; [ACL2025 formal PDF](https://aclanthology.org/2025.acl-long.453.pdf), not silently swapped with arXiv v1; [card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md)
  - Original register aliases / era / family / provenance: W0010; 2024/2025 entropy patching
  - Source-scoped evidence/depth: 8B equal-main-training-FLOP comparison exposes different raw-byte amounts (Llama3 ~4T, entropy BLT ~4.5T, space ~6T). App.H counts local/global/cross-attention model FLOPs but does not separately include default 100M entropy model or its training/preprocessing. **RF** §§2–5,7,10/App.H,N,P.
- **S07/W0010**, [WORKS](../01_discovery/S07/WORKS.md) line 31: **Byte Latent Transformer: Patches Scale Better Than Tokens**; [ACL 2025 conference PDF](https://aclanthology.org/2025.acl-long.453.pdf)
  - Original register aliases / era / family / provenance: W0010
  - Source-scoped evidence/depth: RF: `03_reading/B05/W0010.md`, entire card; old reading has scoped appendix selection.

</details>

<a id="BIW-0011"></a>
## BIW-0011 — Dynamic Chunking for End-to-End Hierarchical Sequence Modeling

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **状态：全文精读**。Sukjun Hwang、Brandon Wang、Albert Gu，2025首发，[arXiv:2507.07955v2](https://arxiv.org/html/2507.07955v2)；[官方Atom](https://export.arxiv.org/api/query?id_list=2507.07955)核完整作者。HTML提取页眉漏首作者，不能误写成两人；实际读§1–4及实验结果表2–5、附录B、C、E.1–E.3与F相关部分；其他附录和参考文献未逐项精读，曲线未逐点数字化、未审代码。abs页面一次网络失败，HTML及Atom成功；未比对后续正式版。
- **Carrying card:** [old scoped FULL/BIW-0011](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md).
- **Canonical problem records:** [BIP-0023](DETAILED_INVENTORY.md#BIP-0023), [BIP-0024](DETAILED_INVENTORY.md#BIP-0024), [BIP-0025](DETAILED_INVENTORY.md#BIP-0025), [BIP-0026](DETAILED_INVENTORY.md#BIP-0026), [BIP-0027](DETAILED_INVENTORY.md#BIP-0027), [BIP-0028](DETAILED_INVENTORY.md#BIP-0028).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Bytes → **selected contextual states** at learned boundaries → next bytes; LM, straight-through routing, EMA smoothing, ratio loss. Prefix-causal.
- **Learning and causal baseline:** Bytes → **selected contextual states** at learned boundaries → next bytes; LM, straight-through routing, EMA smoothing, ratio loss. Prefix-causal.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0011`.
- **Full-source target / version:** https://arxiv.org/pdf/2507.07955v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes → **selected contextual states** at learned boundaries → next bytes; LM, straight-through routing, EMA smoothing, ratio loss. Prefix-causal.
- **Learning and causal baseline:** Bytes → **selected contextual states** at learned boundaries → next bytes; LM, straight-through routing, EMA smoothing, ratio loss. Prefix-causal.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md). Scope header: **状态：全文精读**。Sukjun Hwang、Brandon Wang、Albert Gu，2025首发，[arXiv:2507.07955v2](https://arxiv.org/html/2507.07955v2)；[官方Atom](https://export.arxiv.org/api/query?id_list=2507.07955)核完整作者。HTML提取页眉漏首作者，不能误写成两人；实际读§1–4及实验结果表2–5、附录B、C、E.1–E.3与F相关部分；其他附录和参考文献未逐项精读，曲线未逐点数字化、未审代码。abs页面一次网络失败，HTML及Atom成功；未比对后续正式版。
- **Canonical problems:** [BIP-0023](DETAILED_INVENTORY.md#BIP-0023), [BIP-0024](DETAILED_INVENTORY.md#BIP-0024), [BIP-0025](DETAILED_INVENTORY.md#BIP-0025), [BIP-0026](DETAILED_INVENTORY.md#BIP-0026), [BIP-0027](DETAILED_INVENTORY.md#BIP-0027), [BIP-0028](DETAILED_INVENTORY.md#BIP-0028).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S02/W0011**, [WORKS](../01_discovery/S02/WORKS.md) line 47: Hwang, Wang & Gu, **Dynamic Chunking for End-to-End Hierarchical Sequence Modeling** (H-Net), [2507.07955v2](https://arxiv.org/html/2507.07955v2)
  - Original register aliases / era / family / provenance: W0011; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B05/W0011.md`; aggregation ablation in AppendixE.1.
- **S03/W0011**, [WORKS](../01_discovery/S03/WORKS.md) line 21: W0011 · Dynamic Chunking for End-to-End Hierarchical Sequence Modeling (2025); [2507.07955v2](https://arxiv.org/html/2507.07955v2) C: [B05/W0011](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md)
  - Original register aliases / era / family / provenance: W0011 · Dynamic Chunking for End-to-End Hierarchical Sequence Modeling (2025); [2507.07955v2](https://arxiv.org/html/2507.07955v2)
  - Source-scoped evidence/depth: C: [B05/W0011](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md)
- **S04/W0011**, [WORKS](../01_discovery/S04/WORKS.md) line 26: **W0011**, 2025, *Dynamic Chunking for End-to-End Hierarchical Sequence Modeling*; [v2](https://arxiv.org/html/2507.07955v2) CATALOG reuse; F-card `OLD/03_reading/B05/W0011.md`
  - Original register aliases / era / family / provenance: **W0011**, 2025, *Dynamic Chunking for End-to-End Hierarchical Sequence Modeling*; [v2](https://arxiv.org/html/2507.07955v2)
  - Source-scoped evidence/depth: CATALOG reuse; F-card `OLD/03_reading/B05/W0011.md` Causal route from current/past states; EMA plus straight-through derivative. Same approximate byte exposure/FLOPs, not equal parameters; ~1.3B Transformer-equivalent upper scale. §§2/3.3 and Appendix E/F; no full-appendix claim beyond card. Tying unknown.
- **S06/W0011**, [WORKS](../01_discovery/S06/WORKS.md) line 26: **Dynamic Chunking for End-to-End Hierarchical Sequence Modeling** (H-Net); [2507.07955v2](https://arxiv.org/html/2507.07955v2); [card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md)
  - Original register aliases / era / family / provenance: W0011; 2025 learned hierarchy
  - Source-scoped evidence/depth: Same dataset and approximately byte-matched batches/compute, not equal total parameters. XL BPE .69 vs two-stage .69 GFLOPs/byte, average downstream 55.5 vs 58.2. Implementation training up to ~2× slower than isotropic model; variable batches/OOM and asynchronous generation remain. **RF** §§2–4/App.B,E.
- **S08/S08-W23**, [WORKS](../01_discovery/S08/WORKS.md) line 54: **Dynamic Chunking for End-to-End Hierarchical Sequence Modeling**, [2507.07955v2](https://arxiv.org/html/2507.07955v2), 2025. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md).
  - Original register aliases / era / family / provenance: S08-W23 / **W0011** / catalog reuse
  - Source-scoped evidence/depth: **Dynamic Chunking for End-to-End Hierarchical Sequence Modeling**, [2507.07955v2](https://arxiv.org/html/2507.07955v2), 2025. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md). Same-data/approximately isoFLOP comparisons; one-stage not always above space baseline; code space/dynamic nearly tied. Implementation can train ~2× slower than isotropic baseline; limited seed evidence.

</details>

<a id="BIW-0012"></a>
## BIW-0012 — SOMBRERO: Measuring and Steering Boundary Placement in End-to-End Hierarchical Sequence Models

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**：读取[2601.22805v1 HTML](https://arxiv.org/html/2601.22805v1)正文§1–5及附录A–C；以本机pdftotext补读[v1 PDF](https://arxiv.org/pdf/2601.22805v1)全文17页、表2及附录D。颜色编码边界不可由文本恢复，以下引用附录作者解释而不声称独立视觉核对。原PDF首页作者含 Pit Neitemeier、Alessio Serra、Jiaze Li、Sascha Wirges、Lukas Balles、Jan Hendrik Metzen；HTML作者抽取漏首名，应以原PDF为准。2026预印本，[版本记录](https://arxiv.org/abs/2601.22805)仅v1；未核正式发表。
- **Carrying card:** [old scoped FULL/BIW-0012](../../flued_multigranularity_survey_20261108/03_reading/B24/W0012.md).
- **Canonical problem records:** [BIP-0156](DETAILED_INVENTORY.md#BIP-0156), [BIP-0157](DETAILED_INVENTORY.md#BIP-0157).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Bytes → boundary states → next bytes; LM + ratio + stop-gradient next-byte-confidence boundary loss. Prefix-causal policy; training targets know the next byte.
- **Learning and causal baseline:** Bytes → boundary states → next bytes; LM + ratio + stop-gradient next-byte-confidence boundary loss. Prefix-causal policy; training targets know the next byte.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0012`.
- **Full-source target / version:** https://arxiv.org/pdf/2601.22805v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes → boundary states → next bytes; LM + ratio + stop-gradient next-byte-confidence boundary loss. Prefix-causal policy; training targets know the next byte.
- **Learning and causal baseline:** Bytes → boundary states → next bytes; LM + ratio + stop-gradient next-byte-confidence boundary loss. Prefix-causal policy; training targets know the next byte.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B24/W0012.md). Scope header: **FULL**：读取[2601.22805v1 HTML](https://arxiv.org/html/2601.22805v1)正文§1–5及附录A–C；以本机pdftotext补读[v1 PDF](https://arxiv.org/pdf/2601.22805v1)全文17页、表2及附录D。颜色编码边界不可由文本恢复，以下引用附录作者解释而不声称独立视觉核对。原PDF首页作者含 Pit Neitemeier、Alessio Serra、Jiaze Li、Sascha Wirges、Lukas Balles、Jan Hendrik Metzen；HTML作者抽取漏首名，应以原PDF为准。2026预印本，[版本记录](https://arxiv.org/abs/2601.22805)仅v1；未核正式发表。
- **Canonical problems:** [BIP-0156](DETAILED_INVENTORY.md#BIP-0156), [BIP-0157](DETAILED_INVENTORY.md#BIP-0157).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S02/W0012**, [WORKS](../01_discovery/S02/WORKS.md) line 48: Neitemeier et al., **SOMBRERO: Measuring and Steering Boundary Placement in End-to-End Hierarchical Sequence Models**, [2601.22805v1](https://arxiv.org/html/2601.22805v1)
  - Original register aliases / era / family / provenance: W0012; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B24/W0012.md`; unresolved table/prose numeric tension and unverified colored examples retained.

</details>

<a id="BIW-0013"></a>
## BIW-0013 — A gated quantized VAE for learning variable length tokens (GQ-VAE)

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**：Theo Datta、Kayla Huang、Sham Kakade、David Brandfonbrener，2025，[2512.21913v1全文](https://arxiv.org/html/2512.21913v1)，§I–IV及全部正文图表标题与结果已读；[版本历史](https://arxiv.org/abs/2512.21913)仅v1，未见独立附录。全文阅读不等于实现核验。
- **Carrying card:** [old scoped FULL/BIW-0013](../../flued_multigranularity_survey_20261108/03_reading/B24/W0013.md).
- **Canonical problem records:** [BIP-0158](DETAILED_INVENTORY.md#BIP-0158), [BIP-0159](DETAILED_INVENTORY.md#BIP-0159).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Card says character/byte input; **exact numerical encoding unresolved** → gated quantized codes → characters/lengths, then downstream codes; reconstruction + gate/length/codebook/commitment losses. Whole input encoder, offline tokenizer.
- **Learning and causal baseline:** Card says character/byte input; **exact numerical encoding unresolved** → gated quantized codes → characters/lengths, then downstream codes; reconstruction + gate/length/codebook/commitment losses. Whole input encoder, offline tokenizer.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0013`.
- **Full-source target / version:** https://arxiv.org/pdf/2512.21913v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Card says character/byte input; **exact numerical encoding unresolved** → gated quantized codes → characters/lengths, then downstream codes; reconstruction + gate/length/codebook/commitment losses. Whole input encoder, offline tokenizer.
- **Learning and causal baseline:** Card says character/byte input; **exact numerical encoding unresolved** → gated quantized codes → characters/lengths, then downstream codes; reconstruction + gate/length/codebook/commitment losses. Whole input encoder, offline tokenizer.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B24/W0013.md). Scope header: **FULL**：Theo Datta、Kayla Huang、Sham Kakade、David Brandfonbrener，2025，[2512.21913v1全文](https://arxiv.org/html/2512.21913v1)，§I–IV及全部正文图表标题与结果已读；[版本历史](https://arxiv.org/abs/2512.21913)仅v1，未见独立附录。全文阅读不等于实现核验。
- **Canonical problems:** [BIP-0158](DETAILED_INVENTORY.md#BIP-0158), [BIP-0159](DETAILED_INVENTORY.md#BIP-0159).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S02/W0013**, [WORKS](../01_discovery/S02/WORKS.md) line 49: Datta et al., **GQ-VAE: A gated quantized VAE for learning variable length tokens**, [2512.21913v1](https://arxiv.org/html/2512.21913v1)
  - Original register aliases / era / family / provenance: W0013; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B24/W0013.md`. Do not label as a proven UTF-8 causal LM.

</details>

<a id="BIW-0014"></a>
## BIW-0014 — Fast Byte Latent Transformer

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**｜Julie Kallini、Artidoro Pagnoni、Tomasz Limisiewicz、Gargi Ghosh、Luke Zettlemoyer、Christopher Potts、Xiaochuang Han、Srinivasan Iyer，2026-05-08，[arXiv 2605.08044v1](https://arxiv.org/html/2605.08044v1)、[PDF](https://arxiv.org/pdf/2605.08044v1)。读§1–7及附录A和B/C代表性超参数、1B/3B结果表；未逐格数字化全部表。HTML分页扫描截断，后用PDF读取相关附录。代码未审、实验/证明未复现。
- **Carrying card:** [old scoped FULL/BIW-0014](../../flued_multigranularity_survey_20261108/03_reading/B14/W0014.md).
- **Canonical problem records:** [BIP-0029](DETAILED_INVENTORY.md#BIP-0029), [BIP-0030](DETAILED_INVENTORY.md#BIP-0030), [BIP-0031](DETAILED_INVENTORY.md#BIP-0031).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Bytes / entropy patches + fixed future-byte blocks / bytes or block drafts / next-byte CE + masked diffusion denoising. Clean AR path causal; denoising block bidirectional with corruption; draft verification preserves corresponding model's greedy prefix only.
- **Learning and causal baseline:** Bytes / entropy patches + fixed future-byte blocks / bytes or block drafts / next-byte CE + masked diffusion denoising. Clean AR path causal; denoising block bidirectional with corruption; draft verification preserves corresponding model's greedy prefix only.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0014`.
- **Full-source target / version:** https://arxiv.org/pdf/2605.08044v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes / entropy patches + fixed future-byte blocks / bytes or block drafts / next-byte CE + masked diffusion denoising. Clean AR path causal; denoising block bidirectional with corruption; draft verification preserves corresponding model's greedy prefix only.
- **Learning and causal baseline:** Bytes / entropy patches + fixed future-byte blocks / bytes or block drafts / next-byte CE + masked diffusion denoising. Clean AR path causal; denoising block bidirectional with corruption; draft verification preserves corresponding model's greedy prefix only.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0014.md). Scope header: **FULL**｜Julie Kallini、Artidoro Pagnoni、Tomasz Limisiewicz、Gargi Ghosh、Luke Zettlemoyer、Christopher Potts、Xiaochuang Han、Srinivasan Iyer，2026-05-08，[arXiv 2605.08044v1](https://arxiv.org/html/2605.08044v1)、[PDF](https://arxiv.org/pdf/2605.08044v1)。读§1–7及附录A和B/C代表性超参数、1B/3B结果表；未逐格数字化全部表。HTML分页扫描截断，后用PDF读取相关附录。代码未审、实验/证明未复现。
- **Canonical problems:** [BIP-0029](DETAILED_INVENTORY.md#BIP-0029), [BIP-0030](DETAILED_INVENTORY.md#BIP-0030), [BIP-0031](DETAILED_INVENTORY.md#BIP-0031).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S03/W0014**, [WORKS](../01_discovery/S03/WORKS.md) line 22: W0014 · Fast Byte Latent Transformer (2026); [2605.08044v1](https://arxiv.org/html/2605.08044v1) C: [B14/W0014](../../flued_multigranularity_survey_20261108/03_reading/B14/W0014.md)
  - Original register aliases / era / family / provenance: W0014 · Fast Byte Latent Transformer (2026); [2605.08044v1](https://arxiv.org/html/2605.08044v1)
  - Source-scoped evidence/depth: C: [B14/W0014](../../flued_multigranularity_survey_20261108/03_reading/B14/W0014.md)
- **S06/W0014**, [WORKS](../01_discovery/S06/WORKS.md) line 27: **Fast Byte Latent Transformer**; [2605.08044v1](https://arxiv.org/html/2605.08044v1), 2026-05-08; [card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0014.md)
  - Original register aliases / era / family / provenance: W0014; 2026 parallel decoder
  - Source-scoped evidence/depth: 1B/3B. Cost is calls × parameters × 2-byte weights under small-batch/small-KV assumptions, not measured wall-clock. Quality drops on several tasks; verifier does not recover original BLT distribution after changed training. **RF** §§2–7/App.A–C.

</details>

<a id="BIW-0015"></a>
## BIW-0015 — Dynamic Multi-Byte Prediction With Hierarchical Language Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Abraham Toluwase Owodunni, Chibuzor Okocha, Christan Grant, Tomasz Limisiewicz and Sachin Kumar, [arXiv:2608.15454v2](https://arxiv.org/pdf/2608.15454v2), 21 August 2026. Aliases S03/W0015, S06/W0015. **Reading: FULL** for the paper's substantive text, §§1–8 and limitations, pp.1–13, Appendix A/B, Algorithm 1, Figures 1–9 and Tables 1–5; text extraction and graphical reading of p.13. No code, checkpoint, numerical replication, or independent verification of sampling guarantees. Source: [PDF](../03_reading/R05/sources/BIW-0015.pdf), [UTF-8 extraction](../03_reading/R05/sources/BIW-0015.txt). Figure curves without numeric table are interpreted qualitatively.

Input and target are bytes; boundary predictor creates variable-length latent segments, mean-pools causal encoder states, and a deep causal Transformer models segments. A Gumbel-sigmoid boundary signal and a rate-range auxiliary penalty train boundaries jointly. The next-byte head adds byte-encoder residuals and predicts x[t+1]; the separate multi-byte (MBP) Transformer receives duplicated, upsampled *previous-segment* latent outputs plus a downsampled segment residual and is supervised at x[t+2]. The segment attention mask permits self, preceding positions of the same segment, and the preceding segment; same-segment inputs are duplicates of past-segment information, not future true bytes (§§2–3, Fig.2). Thus attending to earlier slots is not conditioning on their sampled byte identities. The first byte is the normal autoregressive head; the remaining candidates are parallel conditional predictions, not a within-block autoregressive joint.
- **Carrying card:** [R05/BIW-0015](../03_reading/R05/BIW-0015.md).
- **Canonical problem records:** [BIP-0032](DETAILED_INVENTORY.md#BIP-0032), [BIP-0033](DETAILED_INVENTORY.md#BIP-0033), [BIP-0034](DETAILED_INVENTORY.md#BIP-0034).
- **Units — input / internal / output / supervision (current):** Bytes / causalmeanpooledsegments and duplicatedpast-segmentMBPlatents / NBPbyte andparallelfuturebytes / NBPCE+MBPCE+ratepenalty; sharedunembeddingbutseparateheadTransformers.

**Central correction P1-04:** LCA2608.15454v2 §3: two decoder heads share a single unembedding, while Transformer layers are separate; no byte input/output tying inference. R05 confirms past-latent parallel candidates, not dependence on sampled sibling bytes; threshold is approximate, verified modes name NBP/FxT and drop KV caching in reported speculative results.

### Current substantive interface, technique, evidence and limits

### Units, method, and actual sharing

Input and target are bytes; boundary predictor creates variable-length latent segments, mean-pools causal encoder states, and a deep causal Transformer models segments. A Gumbel-sigmoid boundary signal and a rate-range auxiliary penalty train boundaries jointly. The next-byte head adds byte-encoder residuals and predicts x[t+1]; the separate multi-byte (MBP) Transformer receives duplicated, upsampled *previous-segment* latent outputs plus a downsampled segment residual and is supervised at x[t+2]. The segment attention mask permits self, preceding positions of the same segment, and the preceding segment; same-segment inputs are duplicates of past-segment information, not future true bytes (§§2–3, Fig.2). Thus attending to earlier slots is not conditioning on their sampled byte identities. The first byte is the normal autoregressive head; the remaining candidates are parallel conditional predictions, not a within-block autoregressive joint.

**Weight axes:** the two decoder heads share one vocabulary unembedding matrix (§3 p.4); their transformer layers are separate. Input embedding ↔ output tying is not specified. No inference from head-sharing to all layers or embedding tables. The architecture supplies one MBP decoder instead of a separate offset head per predicted byte; allocation of depths changes when matching total parameters, so this is not proof that adding MBP to a fixed existing network costs zero parameters.

**Objective:** weighted next-byte cross-entropy + MBP cross-entropy + boundary-rate loss (Eq.2); λ0=1, λ1=1, λ2=10 pretraining. The causal encoder sees only observed prefix. Algorithm 1 recomputes/updates segment trunk on a predicted boundary or missing cached state; otherwise reuses it. Prompt initializes from an already observed byte prefix; edge cases for partially filled segments, EOS, complete tensor indices and cache implementation are not fully specified. Algorithm's stated number of candidates and slices have index ambiguities; no code audit.

### Atomic findings / BIP links

- [BIP-0032](DETAILED_INVENTORY.md#BIP-0032): Serial byte output remains expensive even with compressed trunks. Solution: use a segment-aligned, single boundary-masked MBP decoder. MLP-MBP uses separate future-offset MLPs; model comparison controls total parameter count, not training FLOPs. Fig.3 finds LCA on the performance/throughput frontier on three of four plotted tasks, not unqualified wins.
- [BIP-0033](DETAILED_INVENTORY.md#BIP-0033): Confident parallel candidates can be wrong. Threshold policy accepts the first next-byte token, then only the left-to-right MBP prefix with probabilities ≥τ; it is **not exact sampling**. On five tasks Table 1 MLP candidate acceptance is 58.08–65.01%, LCA 45.95–51.68%, while LCA typically performs better at comparable throughput; confidence/acceptance alone is not quality. Fig.4 lowering τ .9→.7 raises acceptance 50.1→56.7%, increases throughput about 10%, but lowers mean task metric about 3 points. At τ=.75, n=3→7, DailySum throughput 210.42→164.18 bytes/s (App. B Table 3), contrary to an unconditional 'more candidates are faster' claim.
- [BIP-0034](DETAILED_INVENTORY.md#BIP-0034): Verification can preserve a *named* autoregressive reference rather than threshold approximation. Self-verification targets the LCA next-byte head; external verification targets a separately resident FlexiTokens (FxT) model. §6.3/Fig.8 report 2.1–2.3× external speedups at n=7 across three tasks, same-size draft and verifier; figure compares outputs/task scores and invokes standard speculative acceptance, but code and exact transformed proposal probabilities are not independently checked. App.B explicitly says **all speculative-acceptance results drop KV caching**; this is not cached serving evidence, and external model residency/memory and precision are unreported. App.B Table 5 reports self 45.85–46.36% and external 47.97–52.04%, but adjacent prose says 78–84%: source contradiction, not reconcilable here. Figure 6 reports 29–37% throughput increase from n=3 to n=7/8 under verification; Fig.7's 100-step sample averages 3.05/6 accepted.

### Budgets and evaluation

§4: all variants ~373M parameters, context 4096, pretrained 50B English FineWeb-Edu bytes, 1 epoch, 1,048,576 bytes per step on four B200 GPUs; 3× target compression, 2,000 warmup steps, Adam 3e-4/cosine. SFT Tulu-3 for five epochs, translation Opus-100 French/Spanish→English for two epochs. Evaluation B200 batch 1, τ=.9, n=3 unless stated; IFEval temperature .7/top-p .9, other tasks greedy. Reported wall-clock throughput is bytes/s, not full training or system cost. No broader multilingual, bigger-scale, energy, concurrency, or independently checked reference-distribution evidence. Appendix A Table 2 contains a formatting/architecture-depth ambiguity: §4.2 says a two-layer LCA head, the table extraction/layout is unclear; do not infer exact total depth without checking author artifacts.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0015`.
- **Full-source target / version:** https://arxiv.org/pdf/2608.15454v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes / hierarchical segments and duplicated past-segment latents / next byte and future-offset bytes / next-byte CE + MBP CE + boundary loss.
- **Learning and causal baseline:** Prefix-causal hidden inputs; main confidence-threshold output policy is approximate. Self/external verification and exact sampling claims must be examined separately; shared output projection concerns heads, not input/output tables.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0032](DETAILED_INVENTORY.md#BIP-0032), [BIP-0033](DETAILED_INVENTORY.md#BIP-0033), [BIP-0034](DETAILED_INVENTORY.md#BIP-0034).
- **Reading ownership:** [R05](batches/R05.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S03/W0015**, [WORKS](../01_discovery/S03/WORKS.md) line 23: W0015 · Dynamic Multi-Byte Prediction With Hierarchical Language Models (2026); [2608.15454v2](https://arxiv.org/html/2608.15454v2), 2026-08-21 P: original §2.1–3.1; selected §4.4, §6.1–6.3 and Appendix B cache note; full result tables/appendix not read
  - Original register aliases / era / family / provenance: W0015 · Dynamic Multi-Byte Prediction With Hierarchical Language Models (2026); [2608.15454v2](https://arxiv.org/html/2608.15454v2), 2026-08-21
  - Source-scoped evidence/depth: P: original §2.1–3.1; selected §4.4, §6.1–6.3 and Appendix B cache note; full result tables/appendix not read
- **S06/W0015**, [WORKS](../01_discovery/S06/WORKS.md) line 28: **Dynamic Multi-Byte Prediction With Hierarchical Language Models**; [2608.15454v2](https://arxiv.org/abs/2608.15454v2), 2026-08-21
  - Original register aliases / era / family / provenance: W0015; 2026 parallel dynamic output
  - Source-scoped evidence/depth: Throughput/quality frontier claimed on generation, QA, summarization, MT; no numerical rate, hardware, verification fidelity, cache contract or baseline full parameter count read. **A**; prioritize full paper.

</details>

<a id="BIW-0016"></a>
## BIW-0016 — Hierarchical Multiscale Recurrent Neural Networks

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Junyoung Chung, Sungjin Ahn, Yoshua Bengio; [arXiv 1609.01704v7, 9 March 2017](https://arxiv.org/pdf/1609.01704v7), ICLR 2017. Alias S02/W0016.

**Reading depth: FULL, fresh.** Read pp. 1–10 §§1–5, Figures 1–5, Tables 1–3 and methods/experiment footnotes; pp. 11–13 are references and there is no additional paper appendix. Visually checked Table 1 and boundary/state plots, pp. 7 and 9. Figure 5 was interpreted from its author caption and discussion; no quantitative visual data were extracted. No code or experiment was verified.
- **Carrying card:** [R03/BIW-0016](../03_reading/R03/BIW-0016.md).
- **Canonical problem records:** [BIP-0145](DETAILED_INVENTORY.md#BIP-0145), [BIP-0146](DETAILED_INVENTORY.md#BIP-0146).
- **Units — input / internal / output / supervision (current):** PTB/text8characters; enwik8byte-valued205symbol benchmark / boundary-controlledmultilevelLSTM / nextsamealphabet symbol / nextsymbolNLL withbiasedstraight-throughboundarygradient.

### Current substantive interface, technique, evidence and limits

**Reading depth: FULL, fresh.** Read pp. 1–10 §§1–5, Figures 1–5, Tables 1–3 and methods/experiment footnotes; pp. 11–13 are references and there is no additional paper appendix. Visually checked Table 1 and boundary/state plots, pp. 7 and 9. Figure 5 was interpreted from its author caption and discussion; no quantitative visual data were extracted. No code or experiment was verified.

### Interface and model

The character language model inputs and predicts the next symbol via softmax; its supervision is next-symbol negative log likelihood, internal units are continuous recurrent states and discrete learned boundary events, not emitted words (§§3–4). The input/output embedding tying, tying across layers, and any output-head sharing are unspecified; scalar gates combine layer outputs but are not shared-head evidence. Text8 uses lowercase alphabet plus space, 27 symbols; PTB is the authors' preprocessed character stream and includes an unknown token in the displayed example. enwik8 is a byte-valued Wikipedia benchmark described as 205 symbols including markup; do not reclassify PTB/Text8 as general UTF-8 byte modeling. Corpus 90M/5M/5M split for enwik8; exact PTB normalization and unknown replacement rules are inherited from cited preprocessing and not fully specified here (§4.1). End-of-sequence and sampling details are not spelled out.

**Problem:** fixed-rate or every-step recurrent updates do not align naturally with variable-duration latent structure. **Solution:** use learned hard boundary signals to control sparse multilevel LSTM updates, exact copies, and resets, without boundary labels. Techniques: LSTM gates maintain within-segment state; a hard sigmoid plus binary step detector identifies updates; top-down recurrence injects previous upper context upon reset; bottom-up transfer sends completed lower summaries; a biased straight-through estimator differentiates the discrete step using the hard-sigmoid surrogate (§3.2–3.3).

**Timing:** At layer ℓ, current lower-layer boundary zᶩ⁻¹_t and previous same-layer boundary zᶩ_(t−1) choose the operation. Previous same-layer boundary takes precedence: FLUSH ejection/reset, with top-down input from previous upper-layer state. Otherwise lower boundary 1 gives UPDATE, lower boundary 0 gives COPY of both hidden and cell state exactly. Bottom-up signal is gated by the current lower boundary. This ordering is causal: lower layer's current state is available after it reads x_t, and prediction is for x_(t+1). Hard reset trades retention for transmission; semantics of a boundary are not automatically a word or meaning. The layer-gated output draws on all three levels at every prediction (§§3.2, 4.1, Fig. 2).

**Optimization:** forward deterministic threshold (or tested stochastic Bernoulli, or a soft non-discretized control); gradients use the hard-sigmoid straight-through approximation. PTB slope increases `min(5,1+0.04*epoch)`; step without slope annealing is used on Text8/enwik8 because larger-data scheduling was difficult, not because annealing was proven unnecessary (§3.3, §4.1). Adam, gradient clip 1; truncated 100-step segments carry hidden state forward; PTB batch 64, lr .002. No auxiliary teacher or segmentation labels.

### Evidence and limitations

- Table 1 visually checked: PTB layer-normalized LSTM 1.29 bits/symbol; HM-LSTM sampling 1.27, soft 1.27, step 1.25, step + annealing 1.24. LayerNorm HyperNetworks 1.23 is better. Hutter enwik8 layer-normalized HM-LSTM 1.32 versus 1.39 matching-layer-norm LSTM, tied with recurrent highway networks at 1.32; decomp8 1.28 is a non-neural compressor. These are reported BPC, not matched compute experiments.
- Table 2 Text8: HM-LSTM 1.32 without layer norm and 1.29 with it versus BatchNorm LSTM 1.36; 1024 hidden units per recurrent layer, 2048 output embedding, batch 128. Total parameters, FLOPs, time and device not reported in the paper. Training/test splits are inherited, not independently checked.
- Figs. 3–4: first-level boundaries often near space but also inside words; second-level interpretation is qualitative. In one 270-position example, 270/56/9 updates by level imply 335 versus 810 hypothetical standard updates, around 59% fewer update events, **not** measured wall-clock speed. Handwriting table reports 1081/1137/1167 log likelihood for baseline/HM/HM plus annealing; it does not establish text results.
- Follow-up evidence from the independent card [BIW-0042](../03_reading/R03/BIW-0042.md), Table 1, finds an HMLSTM word F1 of 10.1 on space-stripped BR-phono, versus 79.3 for its segmental model; a different task and implementation, not a matched refutation of the original results. Space-visible boundary pictures cannot prove semantic word discovery.

**Inventory handoff:** [BIP-0145](DETAILED_INVENTORY.md#BIP-0145), [BIP-0146](DETAILED_INVENTORY.md#BIP-0146): preserve gate timing, biased gradients and dataset-specific slope choices; update-count economy is not validated latency.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0016`.
- **Full-source target / version:** https://arxiv.org/pdf/1609.01704v7. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Character symbols → hierarchical recurrent states → next character; LM NLL, hard boundaries, straight-through gradient and slope annealing. PTB/text8 are character benchmarks; enwik8 is reported as 205 symbols/BPC. Do not relabel all as raw UTF-8. Causal UPDATE/COPY/FLUSH.
- **Learning and causal baseline:** Character symbols → hierarchical recurrent states → next character; LM NLL, hard boundaries, straight-through gradient and slope annealing. PTB/text8 are character benchmarks; enwik8 is reported as 205 symbols/BPC. Do not relabel all as raw UTF-8. Causal UPDATE/COPY/FLUSH.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0145](DETAILED_INVENTORY.md#BIP-0145), [BIP-0146](DETAILED_INVENTORY.md#BIP-0146).
- **Reading ownership:** [R03](batches/R03.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S02/W0016**, [WORKS](../01_discovery/S02/WORKS.md) line 18: Chung, Ahn & Bengio, **Hierarchical Multiscale Recurrent Neural Networks** (2016/ICLR 2017), [1609.01704v7](https://arxiv.org/html/1609.01704v7), 2017-03-09
  - Original register aliases / era / family / provenance: W0016; reused catalogue
  - Source-scoped evidence/depth: P: §§1–3.3 and character experiments §4.1, including tables1–2 and boundary discussion; handwriting and remaining material not read.

</details>

<a id="BIW-0017"></a>
## BIW-0017 — Funnel-Transformer: Filtering out Sequential Redundancy for Efficient Language Processing

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0022`.
- **Full-source target / version:** https://arxiv.org/pdf/2006.03236v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Subword/WordPiece positions → shortened hidden sequence → sequence prediction or restored token representations; pretraining/task losses. Bidirectional encoder precedent, not a byte boundary learner. WordPiece identification also explicitly supported by CANINE §3.1 footnote.
- **Learning and causal baseline:** Subword/WordPiece positions → shortened hidden sequence → sequence prediction or restored token representations; pretraining/task losses. Bidirectional encoder precedent, not a byte boundary learner. WordPiece identification also explicitly supported by CANINE §3.1 footnote.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0151](DETAILED_INVENTORY.md#BIP-0151).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S02/W0022**, [WORKS](../01_discovery/S02/WORKS.md) line 28: Dai et al., **Funnel-Transformer: Filtering out Sequential Redundancy for Efficient Language Processing** (2020), [2006.03236v1](https://arxiv.org/abs/2006.03236v1)
  - Original register aliases / era / family / provenance: W0022; reused catalogue
  - Source-scoped evidence/depth: A, plus primary cross-reference from CANINE; exact Funnel pooling wiring and loss not newly read.

<a id="BIW-0018"></a>
## BIW-0018 — Compressive Transformers for Long-Range Sequence Modelling

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**：Jack W. Rae、Anna Potapenko、Siddhant M. Jayakumar、Chloe Hillier、Timothy P. Lillicrap，[1911.05507v1](https://arxiv.org/html/1911.05507v1)，2019预印本；读§1–6、算法1/2及补充A–E，并用本机PDF转换补读表5/8/9。版本记录仅v1；未运行代码。
- **Carrying card:** [old scoped FULL/BIW-0018](../../flued_multigranularity_survey_20261108/03_reading/B24/W0023.md).
- **Canonical problem records:** [BIP-0035](DETAILED_INVENTORY.md#BIP-0035), [BIP-0036](DETAILED_INVENTORY.md#BIP-0036).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Experiment-dependent character symbols or subword states → compressed FIFO memory → original LM units; state AE versus attention-response reconstruction versus BPTT. Compression concerns old causal memory, not input token boundaries.
- **Learning and causal baseline:** Experiment-dependent character symbols or subword states → compressed FIFO memory → original LM units; state AE versus attention-response reconstruction versus BPTT. Compression concerns old causal memory, not input token boundaries.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0023`.
- **Full-source target / version:** https://arxiv.org/pdf/1911.05507v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Experiment-dependent character symbols or subword states → compressed FIFO memory → original LM units; state AE versus attention-response reconstruction versus BPTT. Compression concerns old causal memory, not input token boundaries.
- **Learning and causal baseline:** Experiment-dependent character symbols or subword states → compressed FIFO memory → original LM units; state AE versus attention-response reconstruction versus BPTT. Compression concerns old causal memory, not input token boundaries.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B24/W0023.md). Scope header: **FULL**：Jack W. Rae、Anna Potapenko、Siddhant M. Jayakumar、Chloe Hillier、Timothy P. Lillicrap，[1911.05507v1](https://arxiv.org/html/1911.05507v1)，2019预印本；读§1–6、算法1/2及补充A–E，并用本机PDF转换补读表5/8/9。版本记录仅v1；未运行代码。
- **Canonical problems:** [BIP-0035](DETAILED_INVENTORY.md#BIP-0035), [BIP-0036](DETAILED_INVENTORY.md#BIP-0036).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S02/W0023**, [WORKS](../01_discovery/S02/WORKS.md) line 60: Rae et al., **Compressive Transformers for Long-Range Sequence Modelling**, [1911.05507v1](https://arxiv.org/html/1911.05507v1)
  - Original register aliases / era / family / provenance: W0023; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B24/W0023.md`; exact per-task units and compute caveats in card.
- **S04/W0023**, [WORKS](../01_discovery/S04/WORKS.md) line 30: **W0023**, 2019/ICLR2020, *Compressive Transformers for Long-Range Sequence Modelling*; [v1](https://arxiv.org/html/1911.05507v1) CATALOG reuse; F-card `OLD/03_reading/B24/W0023.md`
  - Original register aliases / era / family / provenance: **W0023**, 2019/ICLR2020, *Compressive Transformers for Long-Range Sequence Modelling*; [v1](https://arxiv.org/html/1911.05507v1)
  - Source-scoped evidence/depth: CATALOG reuse; F-card `OLD/03_reading/B24/W0023.md` Causal FIFO memory; stop-gradient isolates auxiliary compressor objective. enwik8 bpc vs PG-19 PPL separately. Compression rate selected per row, BPTT has doubled unroll/half batch; not a clean single-budget auxiliary comparison.
- **S06/W0023**, [WORKS](../01_discovery/S06/WORKS.md) line 29: **Compressive Transformers for Long-Range Sequence Modelling**; [1911.05507v1](https://arxiv.org/html/1911.05507v1); [card](../../flued_multigranularity_survey_20261108/03_reading/B24/W0023.md)
  - Original register aliases / era / family / provenance: W0023; 2019/2020 byte recurrence/compression
  - Source-scoped evidence/depth: Relevant byte evidence: p.6 Table5 .973 BPC label for convolution+attention reconstruction; compression c tuned independently. PG19 33.6 vs Transformer-XL 36.3 PPL is **subword**, not byte evidence. enwik8 cache3072 .97 vs4096 1.00; no monotonic cache guarantee. **RF** §§3,5/App.B.

</details>

<a id="BIW-0019"></a>
## BIW-0019 — Token Merging: Your ViT But Faster

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**：Daniel Bolya、Cheng-Yang Fu、Xiaoliang Dai、Peizhao Zhang、Christoph Feichtenhofer、Judy Hoffman；[2210.09461v3 HTML](https://arxiv.org/html/2210.09461v3)，ICLR 2023。先读§1–7、附录A/B，本轮以同版HTML本地解析并分页补读附录C–E。两次同版PDF下载均180秒超时；OpenReview正式页PDF因证书吊销服务器离线无法下载，未关闭证书校验。HTML插图本轮未独立视觉核验；未执行第三方代码。
- **Carrying card:** [old scoped FULL/BIW-0019](../../flued_multigranularity_survey_20261108/03_reading/B24/W0024.md).
- **Canonical problem records:** [BIP-0160](DETAILED_INVENTORY.md#BIP-0160), [BIP-0161](DETAILED_INVENTORY.md#BIP-0161).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Image/video/audio patch tokens → similarity-merged tokens → task labels; pretrained features, optional task fine-tuning. Noncausal vision matching; **not text/byte evidence**.
- **Learning and causal baseline:** Image/video/audio patch tokens → similarity-merged tokens → task labels; pretrained features, optional task fine-tuning. Noncausal vision matching; **not text/byte evidence**.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0024`.
- **Full-source target / version:** https://arxiv.org/pdf/2210.09461v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Image/video/audio patch tokens → similarity-merged tokens → task labels; pretrained features, optional task fine-tuning. Noncausal vision matching; **not text/byte evidence**.
- **Learning and causal baseline:** Image/video/audio patch tokens → similarity-merged tokens → task labels; pretrained features, optional task fine-tuning. Noncausal vision matching; **not text/byte evidence**.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B24/W0024.md). Scope header: **FULL**：Daniel Bolya、Cheng-Yang Fu、Xiaoliang Dai、Peizhao Zhang、Christoph Feichtenhofer、Judy Hoffman；[2210.09461v3 HTML](https://arxiv.org/html/2210.09461v3)，ICLR 2023。先读§1–7、附录A/B，本轮以同版HTML本地解析并分页补读附录C–E。两次同版PDF下载均180秒超时；OpenReview正式页PDF因证书吊销服务器离线无法下载，未关闭证书校验。HTML插图本轮未独立视觉核验；未执行第三方代码。
- **Canonical problems:** [BIP-0160](DETAILED_INVENTORY.md#BIP-0160), [BIP-0161](DETAILED_INVENTORY.md#BIP-0161).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S02/W0024**, [WORKS](../01_discovery/S02/WORKS.md) line 61: Bolya et al., **Token Merging: Your ViT But Faster**, [2210.09461v3](https://arxiv.org/html/2210.09461v3)
  - Original register aliases / era / family / provenance: W0024; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B24/W0024.md`; source membership tracking is not value invertibility.

</details>

<a id="BIW-0020"></a>
## BIW-0020 — In-context Autoencoder for Context Compression in a Large Language Model

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**：Tao Ge、Jing Hu、Lei Wang、Xun Wang、Si-Qing Chen、Furu Wei；[2307.06945v4](https://arxiv.org/html/2307.06945v4)，2024，ICLR 2024；读§1–5、图表和附录A–D。版本历史见[arXiv](https://arxiv.org/abs/2307.06945)，未逐版比较，全文阅读不等于代码复现。
- **Carrying card:** [old scoped FULL/BIW-0020](../../flued_multigranularity_survey_20261108/03_reading/B24/W0038.md).
- **Canonical problem records:** [BIP-0259](DETAILED_INVENTORY.md#BIP-0259), [BIP-0260](DETAILED_INVENTORY.md#BIP-0260).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Subword context → continuous slots → subword output; autoencoding + continuation + instruction adaptation; frozen target LLM, LoRA encoder. Adjacent latent-interface comparator, not byte evidence.
- **Learning and causal baseline:** Subword context → continuous slots → subword output; autoencoding + continuation + instruction adaptation; frozen target LLM, LoRA encoder. Adjacent latent-interface comparator, not byte evidence.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0038`.
- **Full-source target / version:** https://arxiv.org/pdf/2307.06945v4. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Subword context → continuous slots → subword output; autoencoding + continuation + instruction adaptation; frozen target LLM, LoRA encoder. Adjacent latent-interface comparator, not byte evidence.
- **Learning and causal baseline:** Subword context → continuous slots → subword output; autoencoding + continuation + instruction adaptation; frozen target LLM, LoRA encoder. Adjacent latent-interface comparator, not byte evidence.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B24/W0038.md). Scope header: **FULL**：Tao Ge、Jing Hu、Lei Wang、Xun Wang、Si-Qing Chen、Furu Wei；[2307.06945v4](https://arxiv.org/html/2307.06945v4)，2024，ICLR 2024；读§1–5、图表和附录A–D。版本历史见[arXiv](https://arxiv.org/abs/2307.06945)，未逐版比较，全文阅读不等于代码复现。
- **Canonical problems:** [BIP-0259](DETAILED_INVENTORY.md#BIP-0259), [BIP-0260](DETAILED_INVENTORY.md#BIP-0260).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S07/W0038**, [WORKS](../01_discovery/S07/WORKS.md) line 30: **In-context Autoencoder for Context Compression in a Large Language Model**; [2307.06945v4](https://arxiv.org/html/2307.06945v4), 2024
  - Original register aliases / era / family / provenance: W0038
  - Source-scoped evidence/depth: RF: `03_reading/B24/W0038.md`, entire card.

</details>

<a id="BIW-0021"></a>
## BIW-0021 — Repeat After Me: Transformers are Better than State Space Models at Copying

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** - Samy Jelassi, David Brandfonbrener, Sham M. Kakade, Eran Malach，2024；[arXiv:2402.01032v2](https://arxiv.org/abs/2402.01032v2)，[实际读取HTML v2](https://ar5iv.labs.arxiv.org/html/2402.01032v2)，[PDF](https://arxiv.org/pdf/2402.01032v2)。状态 **FULL（全文阅读）**：已读正文及附录A–D、构造与实验细节；图中曲线未数字化。读完与证明正确性分开，§2与附录C/D存在下述待作者/红队核实的形式问题。
- **Carrying card:** [old scoped FULL/BIW-0021](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md).
- **Canonical problem records:** [BIP-0235](DETAILED_INVENTORY.md#BIP-0235).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** **RC** [B04 card](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md). Synthetic discrete symbols/tokens, **not byte-specific**; exact whole-string copy supervision, finite-state capacity argument and attention construction. Long-distance diagnostic antecedent, with formal issues explicitly retained in card.
- **Learning and causal baseline:** **RC** [B04 card](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md). Synthetic discrete symbols/tokens, **not byte-specific**; exact whole-string copy supervision, finite-state capacity argument and attention construction. Long-distance diagnostic antecedent, with formal issues explicitly retained in card.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0061`.
- **Full-source target / version:** https://arxiv.org/pdf/2402.01032v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **RC** [B04 card](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md). Synthetic discrete symbols/tokens, **not byte-specific**; exact whole-string copy supervision, finite-state capacity argument and attention construction. Long-distance diagnostic antecedent, with formal issues explicitly retained in card.
- **Learning and causal baseline:** **RC** [B04 card](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md). Synthetic discrete symbols/tokens, **not byte-specific**; exact whole-string copy supervision, finite-state capacity argument and attention construction. Long-distance diagnostic antecedent, with formal issues explicitly retained in card.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md). Scope header: - Samy Jelassi, David Brandfonbrener, Sham M. Kakade, Eran Malach，2024；[arXiv:2402.01032v2](https://arxiv.org/abs/2402.01032v2)，[实际读取HTML v2](https://ar5iv.labs.arxiv.org/html/2402.01032v2)，[PDF](https://arxiv.org/pdf/2402.01032v2)。状态 **FULL（全文阅读）**：已读正文及附录A–D、构造与实验细节；图中曲线未数字化。读完与证明正确性分开，§2与附录C/D存在下述待作者/红队核实的形式问题。
- **Canonical problems:** [BIP-0235](DETAILED_INVENTORY.md#BIP-0235).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S05/W0061**, [WORKS](../01_discovery/S05/WORKS.md) line 34: Repeat After Me: Transformers are Better than State Space Models at Copying; [2402.01032v2](https://arxiv.org/abs/2402.01032v2), Jelassi et al., 2024
  - Original register aliases / era / family / provenance: W0061
  - Source-scoped evidence/depth: **RC** [B04 card](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md). Synthetic discrete symbols/tokens, **not byte-specific**; exact whole-string copy supervision, finite-state capacity argument and attention construction. Long-distance diagnostic antecedent, with formal issues explicitly retained in card.

</details>

<a id="BIW-0022"></a>
## BIW-0022 — Gradient Surgery for Multi-Task Learning

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL。** Tianhe Yu、Saurabh Kumar、Abhishek Gupta、Sergey Levine、Karol Hausman、Chelsea Finn，NeurIPS 2020，arXiv:2001.06782v4，[官方PDF](https://arxiv.org/pdf/2001.06782v4)。实际续读PDF正文pp.1–10及附录A–J pp.14–27，图形依图注/正文，参考文献未逐条追读。HTML仅得部分正文，官方PDF补足。未核代码、未复现、未独立验证定理。
- **Carrying card:** [old scoped FULL/BIW-0022](../../flued_multigranularity_survey_20261108/03_reading/B16/W0328.md).
- **Canonical problem records:** [BIP-0200](DETAILED_INVENTORY.md#BIP-0200).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Image/task states/actions, not byte interface; supervised/reward losses
- **Learning and causal baseline:** **Background.** PCGrad projects conflicting shared gradients. Multi-task order/noise, per-task backward cost; convex/smooth and single-step guarantees limited. Original card preserves Appendix A.3 concern rather than certifying proof.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0328`.
- **Full-source target / version:** https://arxiv.org/pdf/2001.06782v4. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Image/task states/actions, not byte interface; supervised/reward losses
- **Learning and causal baseline:** **Background.** PCGrad projects conflicting shared gradients. Multi-task order/noise, per-task backward cost; convex/smooth and single-step guarantees limited. Original card preserves Appendix A.3 concern rather than certifying proof.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B16/W0328.md). Scope header: **FULL。** Tianhe Yu、Saurabh Kumar、Abhishek Gupta、Sergey Levine、Karol Hausman、Chelsea Finn，NeurIPS 2020，arXiv:2001.06782v4，[官方PDF](https://arxiv.org/pdf/2001.06782v4)。实际续读PDF正文pp.1–10及附录A–J pp.14–27，图形依图注/正文，参考文献未逐条追读。HTML仅得部分正文，官方PDF补足。未核代码、未复现、未独立验证定理。
- **Canonical problems:** [BIP-0200](DETAILED_INVENTORY.md#BIP-0200).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S04/W0328**, [WORKS](../01_discovery/S04/WORKS.md) line 31: **W0328**, 2020, *Gradient Surgery for Multi-Task Learning*; [v4](https://arxiv.org/pdf/2001.06782v4) CATALOG reuse; F-card `OLD/03_reading/B16/W0328.md`
  - Original register aliases / era / family / provenance: **W0328**, 2020, *Gradient Surgery for Multi-Task Learning*; [v4](https://arxiv.org/pdf/2001.06782v4)
  - Source-scoped evidence/depth: CATALOG reuse; F-card `OLD/03_reading/B16/W0328.md` **Background.** PCGrad projects conflicting shared gradients. Multi-task order/noise, per-task backward cost; convex/smooth and single-step guarantees limited. Original card preserves Appendix A.3 concern rather than certifying proof.

</details>

<a id="BIW-0023"></a>
## BIW-0023 — Adapting Auxiliary Losses Using Gradient Similarity

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL。** Yunshu Du、Wojciech M. Czarnecki、Siddhant M. Jayakumar、Mehrdad Farajtabar、Razvan Pascanu、Balaji Lakshminarayanan；arXiv:1812.02224v2，2020-11-25，[官方PDF](https://arxiv.org/pdf/1812.02224v2)。实际读正文pp.1–11及补充A–F pp.15–21，图中数值以图注/正文为准；参考文献未逐条追读。代码未核、实验未复现；证明已读但未独立验证。
- **Carrying card:** [old scoped FULL/BIW-0023](../../flued_multigranularity_survey_20261108/03_reading/B16/W0331.md).
- **Canonical problem records:** [BIP-0201](DETAILED_INVENTORY.md#BIP-0201).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Image/task/reward targets, not byte interface
- **Learning and causal baseline:** **Background.** Nonnegative gradient-cosine gate; local descent not finite-budget generalization guarantee. Rotation MNIST, RL/teacher settings; Appendix B slow-descent and perfect-teacher counterexamples.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0331`.
- **Full-source target / version:** https://arxiv.org/pdf/1812.02224v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Image/task/reward targets, not byte interface
- **Learning and causal baseline:** **Background.** Nonnegative gradient-cosine gate; local descent not finite-budget generalization guarantee. Rotation MNIST, RL/teacher settings; Appendix B slow-descent and perfect-teacher counterexamples.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B16/W0331.md). Scope header: **FULL。** Yunshu Du、Wojciech M. Czarnecki、Siddhant M. Jayakumar、Mehrdad Farajtabar、Razvan Pascanu、Balaji Lakshminarayanan；arXiv:1812.02224v2，2020-11-25，[官方PDF](https://arxiv.org/pdf/1812.02224v2)。实际读正文pp.1–11及补充A–F pp.15–21，图中数值以图注/正文为准；参考文献未逐条追读。代码未核、实验未复现；证明已读但未独立验证。
- **Canonical problems:** [BIP-0201](DETAILED_INVENTORY.md#BIP-0201).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S04/W0331**, [WORKS](../01_discovery/S04/WORKS.md) line 32: **W0331**, 2018/2020, *Adapting Auxiliary Losses Using Gradient Similarity*; [v2](https://arxiv.org/pdf/1812.02224v2) CATALOG reuse; F-card `OLD/03_reading/B16/W0331.md`
  - Original register aliases / era / family / provenance: **W0331**, 2018/2020, *Adapting Auxiliary Losses Using Gradient Similarity*; [v2](https://arxiv.org/pdf/1812.02224v2)
  - Source-scoped evidence/depth: CATALOG reuse; F-card `OLD/03_reading/B16/W0331.md` **Background.** Nonnegative gradient-cosine gate; local descent not finite-budget generalization guarantee. Rotation MNIST, RL/teacher settings; Appendix B slow-descent and perfect-teacher counterexamples.

</details>

<a id="BIW-0024"></a>
## BIW-0024 — ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **状态：全文实读；代码/配置作限定范围静态核验，未执行。** Linting Xue、Aditya Barua、Noah Constant、Rami Al-Rfou、Sharan Narang、Mihir Kale、Adam Roberts、Colin Raffel；arXiv:2105.13626；TACL 2022，doi:10.1162/tacl_a_00461。读 [正式版PDF](https://aclanthology.org/2022.tacl-1.17.pdf) §1–8、表1–10和图3；表格用 `pdftotext -layout` 补取，表4/5、7/8再以PDF页面图核对。该正式版无补充附录。未复现实验，不将静态代码核验当成运行验证。
- **Carrying card:** [old scoped FULL/BIW-0024](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md).
- **Canonical problem records:** [BIP-0037](DETAILED_INVENTORY.md#BIP-0037), [BIP-0038](DETAILED_INVENTORY.md#BIP-0038), [BIP-0039](DETAILED_INVENTORY.md#BIP-0039), [BIP-0040](DETAILED_INVENTORY.md#BIP-0040), [BIP-0041](DETAILED_INVENTORY.md#BIP-0041), [BIP-0042](DETAILED_INVENTORY.md#BIP-0042), [BIP-0043](DETAILED_INVENTORY.md#BIP-0043), [BIP-0220](DETAILED_INVENTORY.md#BIP-0220), [BIP-0246](DETAILED_INVENTORY.md#BIP-0246).

**Central correction P1-01, P1-04:** ByT5 Table 10, printed p300/PDF10 and §7 p301: G2P, Dakshina, XNLI and GEM-XSum. Replace the discovery NER latency name with XNLI; XNLI6.4–9.5× has sentence-pair input and single-digit label, XSum3.7–6.4×. Separate encoder/input work from output length. Old Large/XNLI operative gin: encoder/decoder inputs shared, decoder input/softmax untied; static configuration+Mesh definition only, no universal size/port/runtime claim.

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** UTF-8 bytes plus special IDs / full-resolution byte encoder and decoder positions / byte spans or task text / span corruption (mean 20 bytes) plus supervised task targets.
- **Learning and causal baseline:** Bidirectional corrupted/full source; causal target decoder. Span corruption is pretraining, not unconditional next-byte LM. Invalid output is decoded with errors=ignore; Large-only config evidence is not runtime aliasing.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0351`.
- **Full-source target / version:** https://aclanthology.org/2022.tacl-1.17.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** UTF-8 bytes plus special IDs / full-resolution byte encoder and decoder positions / byte spans or task text / span corruption (mean 20 bytes) plus supervised task targets.
- **Learning and causal baseline:** Bidirectional corrupted/full source; causal target decoder. Span corruption is pretraining, not unconditional next-byte LM. Invalid output is decoded with errors=ignore; Large-only config evidence is not runtime aliasing.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md). Scope header: **状态：全文实读；代码/配置作限定范围静态核验，未执行。** Linting Xue、Aditya Barua、Noah Constant、Rami Al-Rfou、Sharan Narang、Mihir Kale、Adam Roberts、Colin Raffel；arXiv:2105.13626；TACL 2022，doi:10.1162/tacl_a_00461。读 [正式版PDF](https://aclanthology.org/2022.tacl-1.17.pdf) §1–8、表1–10和图3；表格用 `pdftotext -layout` 补取，表4/5、7/8再以PDF页面图核对。该正式版无补充附录。未复现实验，不将静态代码核验当成运行验证。
- **Canonical problems:** [BIP-0037](DETAILED_INVENTORY.md#BIP-0037), [BIP-0038](DETAILED_INVENTORY.md#BIP-0038), [BIP-0039](DETAILED_INVENTORY.md#BIP-0039), [BIP-0040](DETAILED_INVENTORY.md#BIP-0040), [BIP-0041](DETAILED_INVENTORY.md#BIP-0041), [BIP-0042](DETAILED_INVENTORY.md#BIP-0042), [BIP-0043](DETAILED_INVENTORY.md#BIP-0043), [BIP-0220](DETAILED_INVENTORY.md#BIP-0220), [BIP-0246](DETAILED_INVENTORY.md#BIP-0246).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S01/W0351**, [WORKS](../01_discovery/S01/WORKS.md) line 59: *ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models*, [TACL 2022.17 PDF](https://aclanthology.org/2022.tacl-1.17.pdf); [old FULL card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md)
  - Original register aliases / era / family / provenance: W0351; 2021/TACL 2022 byte encoder–decoder; CATALOG-REUSE
  - Source-scoped evidence/depth: Reused FULL card actually read. 1024 input positions and 1M steps do not mean same text as mT5; output generation length and task matter. Large config's encoder/decoder-input sharing does not imply tied output softmax or all-size sharing.
- **S03/W0351**, [WORKS](../01_discovery/S03/WORKS.md) line 24: W0351 · ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models (2021/TACL 2022); [formal PDF](https://aclanthology.org/2022.tacl-1.17.pdf) C: [B08/W0351](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md)
  - Original register aliases / era / family / provenance: W0351 · ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models (2021/TACL 2022); [formal PDF](https://aclanthology.org/2022.tacl-1.17.pdf)
  - Source-scoped evidence/depth: C: [B08/W0351](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md)
- **S04/W0351**, [WORKS](../01_discovery/S04/WORKS.md) line 19: **W0351**, 2021/2022, *ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models*; [TACL2022](https://aclanthology.org/2022.tacl-1.17.pdf) CATALOG reuse; F-card `OLD/03_reading/B08/W0351.md`; fresh fixed-commit README only
  - Original register aliases / era / family / provenance: **W0351**, 2021/2022, *ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models*; [TACL2022](https://aclanthology.org/2022.tacl-1.17.pdf)
  - Source-scoped evidence/depth: CATALOG reuse; F-card `OLD/03_reading/B08/W0351.md`; fresh fixed-commit README only Bidirectional source encoder, causal target decoder. mT5 total-parameter comparisons; 300M–12.9B ByT5, 1M steps, fixed positions not equal text. Table 1/8–10 and §§3/6. **Only Large operative gin previously statically checked**: encoder/decoder input shared, decoder input/softmax untied. Config reportedly points to XNLI fine-tuning initialized from 1M checkpoint, not pristine pretraining log. HF Small/Large fresh fetches failed.
- **S05/W0351**, [WORKS](../01_discovery/S05/WORKS.md) line 21: ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models; [TACL 2022 PDF](https://aclanthology.org/2022.tacl-1.17.pdf), Xue et al.
  - Original register aliases / era / family / provenance: W0351
  - Source-scoped evidence/depth: **RC** [B08 card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md). UTF-8 byte throughout interface; span-denoising, bidirectional source and causal target. Noise, transliteration, morphology, exposure and decode conventions; tables 1–10.
- **S06/W0351**, [WORKS](../01_discovery/S06/WORKS.md) line 30: **ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models**; [TACL2022 formal PDF](https://aclanthology.org/2022.tacl-1.17.pdf); [card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md)
  - Original register aliases / era / family / provenance: W0351; 2021/2022 byte encoder-decoder
  - Source-scoped evidence/depth: 300M–12.9B total parameters; tiny vocab shifts budget into network; encoder:decoder depth3:1. 1024-position batches expose ~¼ mT5 raw text (mean4.1 bytes/token). TPUv3-64 throughput ~.75× mT5; task inference ranges near parity to ~9.5× slower. **RF** Tables1,9,10.
- **S07/W0351**, [WORKS](../01_discovery/S07/WORKS.md) line 24: **ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models**; [TACL 2022](https://aclanthology.org/2022.tacl-1.17.pdf)
  - Original register aliases / era / family / provenance: W0351
  - Source-scoped evidence/depth: RF: `03_reading/B08/W0351.md`, entire card; formal §§1–8, Tables 1–10 covered by old reader.
- **S08/S08-W24**, [WORKS](../01_discovery/S08/WORKS.md) line 55: **ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models**, TACL 2022 [formal PDF](https://aclanthology.org/2022.tacl-1.17.pdf). **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md).
  - Original register aliases / era / family / provenance: S08-W24 / **W0351** / catalog reuse
  - Source-scoped evidence/depth: **ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models**, TACL 2022 [formal PDF](https://aclanthology.org/2022.tacl-1.17.pdf). **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md). 3:1 encoder/decoder depths vs mT5 1:1; same positions sees ~¼ text; task-dependent latency and quality reversals. Illegal bytes decoded with ignore, not hard validity guarantee. Large-only sharing config in card does not establish all sizes.

**Central correction — audit P1-01/P03/A04:** Table10 latency uses XNLI, not NER. XNLI has long sentence-pair input and a single digit output, so its slowdown cannot be assigned solely to long output. NER timing belongs to the independent W0360 study. Large/XNLI static gin and mutable current Small config are separate sharing evidence.

</details>

<a id="BIW-0025"></a>
## BIW-0025 — MambaByte: Token-free Selective State Space Model

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**｜Junxiong Wang、Tushaar Gangavarapu、Jing Nathan Yan、Alexander M. Rush，COLM 2024，[arXiv 2401.13660v3 HTML](https://arxiv.org/html/2401.13660v3)、[PDF](https://arxiv.org/pdf/2401.13660v3)。读正文§1–7，相关附录A–G、H样例定向；HTML与PDF表号不同，下文明确来源。实现未核、未复现。
- **Carrying card:** [old scoped FULL/BIW-0025](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md).
- **Canonical problem records:** [BIP-0044](DETAILED_INVENTORY.md#BIP-0044), [BIP-0045](DETAILED_INVENTORY.md#BIP-0045), [BIP-0046](DETAILED_INVENTORY.md#BIP-0046).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** UTF-8 bytes / fixed-size selective recurrent state / bytes / next-byte CE; optional serving drafter uses subwords.
- **Learning and causal baseline:** Strict prefix-causal byte chain; fixed recurrent state. The optional top-3 speculative byte verifier is approximate, with an extra subword drafter.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0352`.
- **Full-source target / version:** https://arxiv.org/pdf/2401.13660v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** UTF-8 bytes / fixed-size selective recurrent state / bytes / next-byte CE; optional serving drafter uses subwords.
- **Learning and causal baseline:** Strict prefix-causal byte chain; fixed recurrent state. The optional top-3 speculative byte verifier is approximate, with an extra subword drafter.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md). Scope header: **FULL**｜Junxiong Wang、Tushaar Gangavarapu、Jing Nathan Yan、Alexander M. Rush，COLM 2024，[arXiv 2401.13660v3 HTML](https://arxiv.org/html/2401.13660v3)、[PDF](https://arxiv.org/pdf/2401.13660v3)。读正文§1–7，相关附录A–G、H样例定向；HTML与PDF表号不同，下文明确来源。实现未核、未复现。
- **Canonical problems:** [BIP-0044](DETAILED_INVENTORY.md#BIP-0044), [BIP-0045](DETAILED_INVENTORY.md#BIP-0045), [BIP-0046](DETAILED_INVENTORY.md#BIP-0046).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S01/W0352**, [WORKS](../01_discovery/S01/WORKS.md) line 60: *MambaByte: Token-free Selective State Space Model*, [2401.13660v3](https://arxiv.org/abs/2401.13660v3), 2024-08-09; [old FULL card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md)
  - Original register aliases / era / family / provenance: W0352; 2024 recurrent direct byte; CATALOG-REUSE
  - Source-scoped evidence/depth: Reused FULL card actually read + abs recheck. Similar per-byte FLOPs comparison uses different byte exposure; top-3 speculative verification does not ensure exact original sampling distribution.
- **S03/W0352**, [WORKS](../01_discovery/S03/WORKS.md) line 25: W0352 · MambaByte: Token-free Selective State Space Model (2024); [2401.13660v3](https://arxiv.org/html/2401.13660v3) C: [B14/W0352](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md)
  - Original register aliases / era / family / provenance: W0352 · MambaByte: Token-free Selective State Space Model (2024); [2401.13660v3](https://arxiv.org/html/2401.13660v3)
  - Source-scoped evidence/depth: C: [B14/W0352](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md)
- **S05/W0352**, [WORKS](../01_discovery/S05/WORKS.md) line 22: MambaByte: Token-free Selective State Space Model; [2401.13660v3](https://arxiv.org/html/2401.13660v3), Wang et al., COLM 2024
  - Original register aliases / era / family / provenance: W0352
  - Source-scoped evidence/depth: **RC** [B14 card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md). Byte/fixed recurrent state/byte, next-byte loss, causal. Comparable per-byte compute versus MEGABYTE; word-PPL conversion is dataset-specific; card has no numeric robustness table to support a fresh noise ranking.
- **S06/W0352**, [WORKS](../01_discovery/S06/WORKS.md) line 31: **MambaByte: Token-free Selective State Space Model**; [2401.13660v3](https://arxiv.org/html/2401.13660v3), COLM2024 association; [card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md)
  - Original register aliases / era / family / provenance: W0352; 2024 selective SSM
  - Source-scoped evidence/depth: 353M,8192-byte windows,30B train bytes vs MEGABYTE80B at comparable approximate FLOPs/byte. 110M extra subword drafter, A100,8192-byte generation:2.6× own byte baseline with top-3 acceptance; not exact greedy/sample distribution. **RF** HTML Tables2,7,8/App.E–F.
- **S08/S08-W25**, [WORKS](../01_discovery/S08/WORKS.md) line 56: **MambaByte: Token-free Selective State Space Model**, [2401.13660v3](https://arxiv.org/html/2401.13660v3), COLM 2024. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md).
  - Original register aliases / era / family / provenance: S08-W25 / **W0352** / catalog reuse
  - Source-scoped evidence/depth: **MambaByte: Token-free Selective State Space Model**, [2401.13660v3](https://arxiv.org/html/2401.13660v3), COLM 2024. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0352.md). At similar FLOPs/byte beats reported MEGABYTE rows; text exposure differs. A100 2.6× speculative speedup uses additional110M subword drafter; not tokenizer-prior-free serving or exact sampling equivalence.

</details>

<a id="BIW-0026"></a>
## BIW-0026 — Beyond Language Models: Byte Models are Digital World Simulators

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0353`.
- **Full-source target / version:** https://arxiv.org/pdf/2402.19155v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U bytes of binary/text/audio/image formats → byte-model states (architecture not inspected) → bytes → next-byte prediction. C sequential, exact conditioning protocols unknown.
- **Learning and causal baseline:** U bytes of binary/text/audio/image formats → byte-model states (architecture not inspected) → bytes → next-byte prediction. C sequential, exact conditioning protocols unknown.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0282](DETAILED_INVENTORY.md#BIP-0282).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S08/S08-W26**, [WORKS](../01_discovery/S08/WORKS.md) line 57: **Beyond Language Models: Byte Models are Digital World Simulators**, Wu et al.; [2402.19155v1 abstract](https://arxiv.org/abs/2402.19155v1), 2024-02-29. **A**, old catalog only official introduction, no old FULL card.
  - Original register aliases / era / family / provenance: S08-W26 / **W0353** / catalog reuse
  - Source-scoped evidence/depth: **Beyond Language Models: Byte Models are Digital World Simulators**, Wu et al.; [2402.19155v1 abstract](https://arxiv.org/abs/2402.19155v1), 2024-02-29. **A**, old catalog only official introduction, no old FULL card. Abstract claims ABC→MIDI .0011 BPB and CPU operation accuracy >99.99%, plus multimodal results. These specific figures are conversion/simulation, not natural-language LM performance. Text-specific tables need paper before citation.

<a id="BIW-0027"></a>
## BIW-0027 — When Tokenizers Fail: Byte-Level Chunking for Zero-Shot Transfer to Low-Resource Languages

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**｜Sanjeev Kumar、Atsuki Yamaguchi、Nikolaos Aletras，2026-08-27，[arXiv 2608.27658v1](https://arxiv.org/html/2608.27658v1)。浏览器续读正文§1–7及附录A.1–A.4/B、表1–6；实现和实验未核。
- **Carrying card:** [old scoped FULL/BIW-0027](../../flued_multigranularity_survey_20261108/03_reading/B14/W0355.md).
- **Canonical problem records:** [BIP-0047](DETAILED_INVENTORY.md#BIP-0047), [BIP-0048](DETAILED_INVENTORY.md#BIP-0048), [BIP-0049](DETAILED_INVENTORY.md#BIP-0049).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** UTF-8 bytes → learned chunks → pretrained subword backbone → bytes / downstream word labels; AR + alignment + rate + intermittent Hindi POS signal. Hybrid training provenance.
- **Learning and causal baseline:** UTF-8 bytes → learned chunks → pretrained subword backbone → bytes / downstream word labels; AR + alignment + rate + intermittent Hindi POS signal. Hybrid training provenance.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0355`.
- **Full-source target / version:** https://arxiv.org/pdf/2608.27658v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** UTF-8 bytes → learned chunks → pretrained subword backbone → bytes / downstream word labels; AR + alignment + rate + intermittent Hindi POS signal. Hybrid training provenance.
- **Learning and causal baseline:** UTF-8 bytes → learned chunks → pretrained subword backbone → bytes / downstream word labels; AR + alignment + rate + intermittent Hindi POS signal. Hybrid training provenance.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0355.md). Scope header: **FULL**｜Sanjeev Kumar、Atsuki Yamaguchi、Nikolaos Aletras，2026-08-27，[arXiv 2608.27658v1](https://arxiv.org/html/2608.27658v1)。浏览器续读正文§1–7及附录A.1–A.4/B、表1–6；实现和实验未核。
- **Canonical problems:** [BIP-0047](DETAILED_INVENTORY.md#BIP-0047), [BIP-0048](DETAILED_INVENTORY.md#BIP-0048), [BIP-0049](DETAILED_INVENTORY.md#BIP-0049).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S05/W0355**, [WORKS](../01_discovery/S05/WORKS.md) line 23: When Tokenizers Fail: Byte-Level Chunking for Zero-Shot Transfer to Low-Resource Languages; [2608.27658v1](https://arxiv.org/html/2608.27658v1), Kumar, Yamaguchi, Aletras, 2026
  - Original register aliases / era / family / provenance: W0355
  - Source-scoped evidence/depth: **RC** [B14 card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0355.md). Byte/local Mamba/dynamic chunks/pretrained subword backbone/byte; LM + alignment + rate + Hindi POS assistance. Causal pretraining, word-label probe evaluation. Strong backbone/language counterexamples and unmatched compute.
- **S07/W0355**, [WORKS](../01_discovery/S07/WORKS.md) line 28: **When Tokenizers Fail: Byte-Level Chunking for Zero-Shot Transfer to Low-Resource Languages**; [2608.27658v1](https://arxiv.org/html/2608.27658v1), 2026
  - Original register aliases / era / family / provenance: W0355
  - Source-scoped evidence/depth: RF: `03_reading/B14/W0355.md`, entire card; explicitly not wholly frozen.

</details>

<a id="BIW-0028"></a>
## BIW-0028 — Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**｜Jie Wang、Shiwei Luo、Qi Zhang、Yuanbin Wu，2026-10-05，[arXiv 2610.05978v1 HTML](https://arxiv.org/html/2610.05978v1)、[PDF](https://arxiv.org/pdf/2610.05978v1)。读正文§1–6，HTML截于附录D，续用PDF定向读A–C、D结果、E.1–E.2、F.1–F.3、G；未逐项数字化所有大表/图。代码和实验未核，F.1证明仅阅读未独立复证。
- **Carrying card:** [old scoped FULL/BIW-0028](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md).
- **Canonical problem records:** [BIP-0050](DETAILED_INVENTORY.md#BIP-0050), [BIP-0051](DETAILED_INVENTORY.md#BIP-0051), [BIP-0052](DETAILED_INVENTORY.md#BIP-0052), [BIP-0053](DETAILED_INVENTORY.md#BIP-0053).

**Central correction P1-02, P1-04:** 2610.05978v1 §1/2.1 and Appendix A.4: Qwen3.5-style resolution-preserving hybrid Gated DeltaNet:Gated Softmax Attention=3:1; flat means no explicit local–global–local hierarchy, dense is also contrasted with MoE and does not mean every layer is full softmax. DeltaNet convolution4→16, hashed5–8grams and four-byte curriculum co-vary. Appendix A.4 explicitly specifies UNTIED input/output embeddings. Fitted unique-active N includes output but excludes input/hash tables; C.2 Eq.11 operation budget counts recurrent/full attention but omits lookup/hash/bag averaging/loss/optimizer. Byte parameter frontier wins under this N, subword training-FLOP frontier wins throughout tested range; not full resident-parameter or walltime equality.

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Bytes plus hashed 5–8-grams / full-resolution hybrid Gated DeltaNet:Gated Softmax Attention 3:1; initial fixed four-byte mean groups / bytes or initial unordered four-byte bags / first 30% bag targets, remaining 70% next-byte targets.
- **Learning and causal baseline:** Causal prediction under its curriculum. Flat/full-resolution means no explicit local–global hierarchy, not a pure softmax Transformer. Oracle speculation is a separate true-prefix simulation.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0356`.
- **Full-source target / version:** https://arxiv.org/pdf/2610.05978v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes plus hashed 5–8-grams / full-resolution hybrid Gated DeltaNet:Gated Softmax Attention 3:1; initial fixed four-byte mean groups / bytes or initial unordered four-byte bags / first 30% bag targets, remaining 70% next-byte targets.
- **Learning and causal baseline:** Causal prediction under its curriculum. Flat/full-resolution means no explicit local–global hierarchy, not a pure softmax Transformer. Oracle speculation is a separate true-prefix simulation.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md). Scope header: **FULL**｜Jie Wang、Shiwei Luo、Qi Zhang、Yuanbin Wu，2026-10-05，[arXiv 2610.05978v1 HTML](https://arxiv.org/html/2610.05978v1)、[PDF](https://arxiv.org/pdf/2610.05978v1)。读正文§1–6，HTML截于附录D，续用PDF定向读A–C、D结果、E.1–E.2、F.1–F.3、G；未逐项数字化所有大表/图。代码和实验未核，F.1证明仅阅读未独立复证。
- **Canonical problems:** [BIP-0050](DETAILED_INVENTORY.md#BIP-0050), [BIP-0051](DETAILED_INVENTORY.md#BIP-0051), [BIP-0052](DETAILED_INVENTORY.md#BIP-0052), [BIP-0053](DETAILED_INVENTORY.md#BIP-0053).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S01/W0356**, [WORKS](../01_discovery/S01/WORKS.md) line 61: *Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation*, [2610.05978v1](https://arxiv.org/abs/2610.05978v1); [old FULL card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md)
  - Original register aliases / era / family / provenance: W0356; 2026 dense byte counterexample; CATALOG-REUSE
  - Source-scoped evidence/depth: Reused FULL card actually read. Same-parameter byte advantage coexists with subword advantage throughout reported compute-optimal curves; not a tokenizer-only swap.
- **S03/W0356**, [WORKS](../01_discovery/S03/WORKS.md) line 26: W0356 · Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation (2026); [2610.05978v1](https://arxiv.org/html/2610.05978v1) C: [B14/W0356](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md)
  - Original register aliases / era / family / provenance: W0356 · Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation (2026); [2610.05978v1](https://arxiv.org/html/2610.05978v1)
  - Source-scoped evidence/depth: C: [B14/W0356](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md)
- **S04/W0356**, [WORKS](../01_discovery/S04/WORKS.md) line 29: **W0356**, 2026, *Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation*; [v1](https://arxiv.org/html/2610.05978v1) CATALOG reuse; F-card `OLD/03_reading/B14/W0356.md`
  - Original register aliases / era / family / provenance: **W0356**, 2026, *Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation*; [v1](https://arxiv.org/html/2610.05978v1)
  - Source-scoped evidence/depth: CATALOG reuse; F-card `OLD/03_reading/B14/W0356.md` Causal; first30% grouped objective then70% byte objective; hashed n-grams/convolution width also differ from token baseline. Same-parameter byte advantage but subword best at matched FLOPs in reported frontier; not tying ablation.
- **S05/W0356**, [WORKS](../01_discovery/S05/WORKS.md) line 24: Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation; [2610.05978v1](https://arxiv.org/html/2610.05978v1), Wang et al., 2026
  - Original register aliases / era / family / provenance: W0356
  - Source-scoped evidence/depth: **RC** [B14 card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md). Byte, early four-byte pooled/bag objective then byte LM; hash n-grams and convolution are additional changes. Same-parameter and same-compute rankings diverge; ASCII copy-attention examples are not exact-copy causality evidence.
- **S06/W0356**, [WORKS](../01_discovery/S06/WORKS.md) line 32: **Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation**; [2610.05978v1](https://arxiv.org/html/2610.05978v1); [card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md)
  - Original register aliases / era / family / provenance: W0356; 2026 dense byte scaling counterexample
  - Source-scoped evidence/depth: Same-parameter optimum favors byte; same-training-FLOP optimum favors subword. Byte8192 vs subword2048 positions. FLOPs omit hashing/loss/optimizer; accepted-position simulation is not timed decoding. **RF** §2/Fig.1/App.A–C,G.
- **S07/W0356**, [WORKS](../01_discovery/S07/WORKS.md) line 32: **Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation**; [2610.05978v1](https://arxiv.org/html/2610.05978v1), 2026
  - Original register aliases / era / family / provenance: W0356
  - Source-scoped evidence/depth: RF: `03_reading/B14/W0356.md`, entire card; scoped appendix reading retained.
- **S08/S08-W27**, [WORKS](../01_discovery/S08/WORKS.md) line 58: **Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation**, [2610.05978v1](https://arxiv.org/html/2610.05978v1), 2026-10-05. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md).
  - Original register aliases / era / family / provenance: S08-W27 / **W0356** / catalog reuse
  - Source-scoped evidence/depth: **Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation**, [2610.05978v1](https://arxiv.org/html/2610.05978v1), 2026-10-05. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md). Equal-parameter curves favor bytes, equal-training-FLOP curves favor subwords throughout tested range. Speculative result is oracle accepted positions, not measured runtime. FLOPs omit hash/loss/optimizer parts.

**Central correction — audit P1-02/P17/A19:** “flat” means full sequence resolution/no explicit local–global hierarchy. The backbone is Gated DeltaNet:Gated Softmax Attention 3:1 (v1 §2.1 fn1), not a generic pure full-softmax Transformer; convolution width refers to DeltaNet. Frontier reversal is retained. This is audit-inherited primary evidence, not a new FULL.

</details>

<a id="BIW-0029"></a>
## BIW-0029 — Easy to anticipate, hard to compute: boundary dependence finds the computed outputs that entropy patching misses

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **状态：全文精读**。Nicolás Vera Zúñiga，2026，[arXiv:2610.11790v1 HTML全文](https://arxiv.org/html/2610.11790v1)，[PDF](https://arxiv.org/pdf/2610.11790v1)；实际读取§1–13、表1–6和附录A，未运行或审核代码/日志。另读同作者[2610.22100v1全文§1–8](https://arxiv.org/html/2610.22100v1)定位作品关系。
- **Carrying card:** [old scoped FULL/BIW-0029](../../flued_multigranularity_survey_20261108/03_reading/B05/W0357.md).
- **Canonical problem records:** [BIP-0054](DETAILED_INVENTORY.md#BIP-0054).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Bytes → BLT-style patches → bytes; offline boundary-utility proxies fitted by past-two-byte context. Deployment causal; labels may use future training targets.
- **Learning and causal baseline:** Bytes → BLT-style patches → bytes; offline boundary-utility proxies fitted by past-two-byte context. Deployment causal; labels may use future training targets.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0357`.
- **Full-source target / version:** https://arxiv.org/pdf/2610.11790v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes → BLT-style patches → bytes; offline boundary-utility proxies fitted by past-two-byte context. Deployment causal; labels may use future training targets.
- **Learning and causal baseline:** Bytes → BLT-style patches → bytes; offline boundary-utility proxies fitted by past-two-byte context. Deployment causal; labels may use future training targets.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0357.md). Scope header: **状态：全文精读**。Nicolás Vera Zúñiga，2026，[arXiv:2610.11790v1 HTML全文](https://arxiv.org/html/2610.11790v1)，[PDF](https://arxiv.org/pdf/2610.11790v1)；实际读取§1–13、表1–6和附录A，未运行或审核代码/日志。另读同作者[2610.22100v1全文§1–8](https://arxiv.org/html/2610.22100v1)定位作品关系。
- **Canonical problems:** [BIP-0054](DETAILED_INVENTORY.md#BIP-0054).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S02/W0357**, [WORKS](../01_discovery/S02/WORKS.md) line 50: Vera Zúñiga, **Easy to anticipate, hard to compute: boundary dependence finds the computed outputs that entropy patching misses**, [2610.11790v1](https://arxiv.org/html/2610.11790v1)
  - Original register aliases / era / family / provenance: W0357; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B05/W0357.md`; same author/data/code cluster as W0358, not independent replication.
- **S06/W0357**, [WORKS](../01_discovery/S06/WORKS.md) line 33: **Easy to anticipate, hard to compute: boundary dependence finds the computed outputs that entropy patching misses**; [2610.11790v1](https://arxiv.org/html/2610.11790v1); [card](../../flued_multigranularity_survey_20261108/03_reading/B05/W0357.md)
  - Original register aliases / era / family / provenance: W0357; 2026 compute allocation counterexample
  - Source-scoped evidence/depth: Default BLT-1B estimator includes 199M entropy FLOPs/byte vs299M local and2653M/patch global matmul forward. Table-only48% default compute loses final-answer quality; offline reference training/scoring excluded. Tiny math-domain/teacher-forced results, free-solving ~2% or less. **RF** §§3–10,12.

</details>

<a id="BIW-0030"></a>
## BIW-0030 — Patch where the text is new: a compression view of where byte-level models should spend compute

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**｜Nicolás Vera Zúñiga，2026-10-15，[arXiv 2610.22100v1 原文](https://arxiv.org/html/2610.22100v1)。浏览器实际读§1–9、表1–5和限制；此版本无正文附录。首次无版本HTML Fetch网络失败，版本化浏览器成功。代码未核、实验未复现。
- **Carrying card:** [old scoped FULL/BIW-0030](../../flued_multigranularity_survey_20261108/03_reading/B14/W0358.md).
- **Canonical problem records:** [BIP-0162](DETAILED_INVENTORY.md#BIP-0162), [BIP-0163](DETAILED_INVENTORY.md#BIP-0163).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Bytes → novelty-rule patches → bytes; future-repeat labels estimated offline, table keyed by past bytes at deployment. LZ77-motivated novelty, not entropy or direct utility.
- **Learning and causal baseline:** Bytes → novelty-rule patches → bytes; future-repeat labels estimated offline, table keyed by past bytes at deployment. LZ77-motivated novelty, not entropy or direct utility.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0358`.
- **Full-source target / version:** https://arxiv.org/pdf/2610.22100v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes → novelty-rule patches → bytes; future-repeat labels estimated offline, table keyed by past bytes at deployment. LZ77-motivated novelty, not entropy or direct utility.
- **Learning and causal baseline:** Bytes → novelty-rule patches → bytes; future-repeat labels estimated offline, table keyed by past bytes at deployment. LZ77-motivated novelty, not entropy or direct utility.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0358.md). Scope header: **FULL**｜Nicolás Vera Zúñiga，2026-10-15，[arXiv 2610.22100v1 原文](https://arxiv.org/html/2610.22100v1)。浏览器实际读§1–9、表1–5和限制；此版本无正文附录。首次无版本HTML Fetch网络失败，版本化浏览器成功。代码未核、实验未复现。
- **Canonical problems:** [BIP-0162](DETAILED_INVENTORY.md#BIP-0162), [BIP-0163](DETAILED_INVENTORY.md#BIP-0163).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S02/W0358**, [WORKS](../01_discovery/S02/WORKS.md) line 51: Vera Zúñiga, **Patch where the text is new: a compression view of where byte-level models should spend compute**, [2610.22100v1](https://arxiv.org/html/2610.22100v1), 2026-10-15
  - Original register aliases / era / family / provenance: W0358; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B14/W0358.md`, §§1–9/tables1–5; fresh abstract identity check only.

</details>

<a id="BIW-0031"></a>
## BIW-0031 — Universal Byte-Level Encoding: UTF-8/UTF-16 Routing to Reduce Cross-Script Token-Budget Disparities

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**｜Hyunsik Kim、Youngmoon Jung，2026-10-02，[arXiv 2610.01984v2 HTML](https://arxiv.org/html/2610.01984v2)，[同版PDF](https://arxiv.org/pdf/2610.01984v2)。前轮读正文§1–5和部分附录；本次将公开v2 PDF转为项目内临时文本，分页续读附录B–I及长表，覆盖PDF pp.20–66，补齐原有截断。长表已通读，未逐格独立复算；代码、实验与证明未独立验证。
- **Carrying card:** [old scoped FULL/BIW-0031](../../flued_multigranularity_survey_20261108/03_reading/B14/W0359.md).
- **Canonical problem records:** [BIP-0055](DETAILED_INVENTORY.md#BIP-0055), [BIP-0219](DETAILED_INVENTORY.md#BIP-0219).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Codepoint-routed UTF-8/UTF-16LE base symbols in disjoint alphabets (512) **then BPE subwords** / subword positions / subwords / next subword. No grapheme normalization.
- **Learning and causal baseline:** Deterministic encoding plus learned BPE preprocessing; causal subword LM, no learned dynamic byte segmentation.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0359`.
- **Full-source target / version:** https://arxiv.org/pdf/2610.01984v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Codepoint-routed UTF-8/UTF-16LE base symbols in disjoint alphabets (512) **then BPE subwords** / subword positions / subwords / next subword. No grapheme normalization.
- **Learning and causal baseline:** Deterministic encoding plus learned BPE preprocessing; causal subword LM, no learned dynamic byte segmentation.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0359.md). Scope header: **FULL**｜Hyunsik Kim、Youngmoon Jung，2026-10-02，[arXiv 2610.01984v2 HTML](https://arxiv.org/html/2610.01984v2)，[同版PDF](https://arxiv.org/pdf/2610.01984v2)。前轮读正文§1–5和部分附录；本次将公开v2 PDF转为项目内临时文本，分页续读附录B–I及长表，覆盖PDF pp.20–66，补齐原有截断。长表已通读，未逐格独立复算；代码、实验与证明未独立验证。
- **Canonical problems:** [BIP-0055](DETAILED_INVENTORY.md#BIP-0055), [BIP-0219](DETAILED_INVENTORY.md#BIP-0219).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S01/W0359**, [WORKS](../01_discovery/S01/WORKS.md) line 62: *Universal Byte-Level Encoding: UTF-8/UTF-16 Routing to Reduce Cross-Script Token-Budget Disparities*, [2610.01984v2](https://arxiv.org/abs/2610.01984v2); [old FULL card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0359.md)
  - Original register aliases / era / family / provenance: W0359; 2026 representation-layer counterexample; CATALOG-REUSE
  - Source-scoped evidence/depth: Reused FULL card actually read. Script-length gains and model-quality gains differ; equal-position/equal-text budgets differ; full reversible encoder does not guarantee arbitrary generated stream validity.
- **S05/W0359**, [WORKS](../01_discovery/S05/WORKS.md) line 25: Universal Byte-Level Encoding: UTF-8/UTF-16 Routing to Reduce Cross-Script Token-Budget Disparities; [2610.01984v2](https://arxiv.org/html/2610.01984v2), Kim and Jung, 2026
  - Original register aliases / era / family / provenance: W0359
  - Source-scoped evidence/depth: **RC** [B14 card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0359.md). Deterministic scalar routing to disjoint byte alphabets then **BPE subwords**, not pure byte LM. No normalization; routing reduces some encoding lengths but final token and LM rankings vary.

</details>

<a id="BIW-0032"></a>
## BIW-0032 — A Multi-dimensional Evaluation of Tokenizer-free Multilingual Pretrained Models

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **状态：全文实读；代码未核验、未复现。** Jimin Sun、Patrick Fernandes、Xinyi Wang、Graham Neubig，2023，arXiv:2210.07111；[EACL Findings正式版PDF](https://aclanthology.org/2023.findings-eacl.128.pdf)，doi:10.18653/v1/2023.findings-eacl.128。读取正文§1–7、附录A/B全部表1–8；表4–7使用PDF页面图核对表头和结论相关语言，未逐字抄录各语言。论文附录A将具体超参转引原模型代码，不能由论文自行还原全部实际截断和训练参数。
- **Carrying card:** [old scoped FULL/BIW-0032](../../flued_multigranularity_survey_20261108/03_reading/B08/W0360.md).
- **Canonical problem records:** [BIP-0056](DETAILED_INVENTORY.md#BIP-0056), [BIP-0057](DETAILED_INVENTORY.md#BIP-0057), [BIP-0058](DETAILED_INVENTORY.md#BIP-0058), [BIP-0059](DETAILED_INVENTORY.md#BIP-0059), [BIP-0060](DETAILED_INVENTORY.md#BIP-0060).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Compares mBERT subwords, CANINE codepoints, mT5 subwords, ByT5 bytes / different model positions / NER, QA or classification outputs / fine-tuning labels after different pretraining.
- **Learning and causal baseline:** Full-input understanding, with generative heads for T5 variants; not a matched causal LM comparison.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0360`.
- **Full-source target / version:** https://aclanthology.org/2023.findings-eacl.128.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Compares mBERT subwords, CANINE codepoints, mT5 subwords, ByT5 bytes / different model positions / NER, QA or classification outputs / fine-tuning labels after different pretraining.
- **Learning and causal baseline:** Full-input understanding, with generative heads for T5 variants; not a matched causal LM comparison.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0360.md). Scope header: **状态：全文实读；代码未核验、未复现。** Jimin Sun、Patrick Fernandes、Xinyi Wang、Graham Neubig，2023，arXiv:2210.07111；[EACL Findings正式版PDF](https://aclanthology.org/2023.findings-eacl.128.pdf)，doi:10.18653/v1/2023.findings-eacl.128。读取正文§1–7、附录A/B全部表1–8；表4–7使用PDF页面图核对表头和结论相关语言，未逐字抄录各语言。论文附录A将具体超参转引原模型代码，不能由论文自行还原全部实际截断和训练参数。
- **Canonical problems:** [BIP-0056](DETAILED_INVENTORY.md#BIP-0056), [BIP-0057](DETAILED_INVENTORY.md#BIP-0057), [BIP-0058](DETAILED_INVENTORY.md#BIP-0058), [BIP-0059](DETAILED_INVENTORY.md#BIP-0059), [BIP-0060](DETAILED_INVENTORY.md#BIP-0060).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S01/W0360**, [WORKS](../01_discovery/S01/WORKS.md) line 63: *A Multi-dimensional Evaluation of Tokenizer-free Multilingual Pretrained Models*, [EACL Findings 2023.128 PDF](https://aclanthology.org/2023.findings-eacl.128.pdf); [old FULL card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0360.md)
  - Original register aliases / era / family / provenance: W0360; 2023 tokenizer-free practical counterexample; CATALOG-REUSE
  - Source-scoped evidence/depth: Reused FULL card actually read. Four-language controlled data axis plus larger appendix language sets; cost only 100 English samples on V100 batch 1. More tuning reverses some CANINE comparisons.
- **S05/W0360**, [WORKS](../01_discovery/S05/WORKS.md) line 26: A Multi-dimensional Evaluation of Tokenizer-free Multilingual Pretrained Models; [EACL Findings 2023](https://aclanthology.org/2023.findings-eacl.128.pdf), Sun, Fernandes, Wang, Neubig
  - Original register aliases / era / family / provenance: W0360
  - Source-scoped evidence/depth: **RC** [B08 card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0360.md). mBERT subword/CANINE code point; mT5 subword/ByT5 byte. Different dense parameters and pretrained data; controlled fine-tuning amounts, per-language tables, English-only latency.
- **S06/W0360**, [WORKS](../01_discovery/S06/WORKS.md) line 34: **A Multi-dimensional Evaluation of Tokenizer-free Multilingual Pretrained Models**; [EACL2023 formal PDF](https://aclanthology.org/2023.findings-eacl.128.pdf); [card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0360.md)
  - Original register aliases / era / family / provenance: W0360; 2023 evaluation negative cases
  - Source-scoped evidence/depth: mBERT178M vs CANINE132M; mT5/ByT5 ~300M but radically different nonvocab budgets. V10032GB,batch1,100 English examples: XNLI40.94 vs36.49ms mT5/ByT5, NER171.99 vs333.72ms. Crosslingual quality not accompanied by per-language timing. **RF** §3.2/App.Tables1–8.
- **S07/W0360**, [WORKS](../01_discovery/S07/WORKS.md) line 25: **A Multi-dimensional Evaluation of Tokenizer-free Multilingual Pretrained Models**; [EACL Findings 2023](https://aclanthology.org/2023.findings-eacl.128.pdf)
  - Original register aliases / era / family / provenance: W0360
  - Source-scoped evidence/depth: RF: `03_reading/B08/W0360.md`, entire card, including corrected appendix language averages.
- **S08/S08-W28**, [WORKS](../01_discovery/S08/WORKS.md) line 59: **A Multi-dimensional Evaluation of Tokenizer-free Multilingual Pretrained Models**, [EACL Findings 2023 PDF](https://aclanthology.org/2023.findings-eacl.128.pdf). **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0360.md).
  - Original register aliases / era / family / provenance: S08-W28 / **W0360** / catalog reuse
  - Source-scoped evidence/depth: **A Multi-dimensional Evaluation of Tokenizer-free Multilingual Pretrained Models**, [EACL Findings 2023 PDF](https://aclanthology.org/2023.findings-eacl.128.pdf). **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0360.md). 100/1k/10k/all labels, XNLI/NER/TyDi. Longer baseline tuning flips CANINE QA average vs mBERT; language-specific reversals. V100 batch1 cost measured English only; pretraining not equal text or architecture.

</details>

<a id="BIW-0033"></a>
## BIW-0033 — Language Model Tokenizers Introduce Unfairness Between Languages

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**｜Aleksandar Petrov、Emanuele La Malfa、Philip H. S. Torr、Adel Bibi，NeurIPS 2023；读[arXiv 2305.15425v2 PDF](https://arxiv.org/pdf/2305.15425v2)，正文§1–8及附录A、B（方言）、C长表定向检查。Fetch正文PDF抽取截到参考文献，另以内存PDF逐页读取主表与方言附录；未逐行数字化C全部语言。实现和实验未复现。
- **Carrying card:** [old scoped FULL/BIW-0033](../../flued_multigranularity_survey_20261108/03_reading/B14/W0361.md).
- **Canonical problem records:** [BIP-0061](DETAILED_INVENTORY.md#BIP-0061).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** UTF-8 bytes, code points, subwords counted separately / positions / no newly trained LM output / no new learning objective; parallel translations measured.
- **Learning and causal baseline:** UTF-8 bytes, code points, subwords counted separately / positions / no newly trained LM output / no new learning objective; parallel translations measured.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0361`.
- **Full-source target / version:** https://arxiv.org/pdf/2305.15425v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** UTF-8 bytes, code points, subwords counted separately / positions / no newly trained LM output / no new learning objective; parallel translations measured.
- **Learning and causal baseline:** UTF-8 bytes, code points, subwords counted separately / positions / no newly trained LM output / no new learning objective; parallel translations measured.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0361.md). Scope header: **FULL**｜Aleksandar Petrov、Emanuele La Malfa、Philip H. S. Torr、Adel Bibi，NeurIPS 2023；读[arXiv 2305.15425v2 PDF](https://arxiv.org/pdf/2305.15425v2)，正文§1–8及附录A、B（方言）、C长表定向检查。Fetch正文PDF抽取截到参考文献，另以内存PDF逐页读取主表与方言附录；未逐行数字化C全部语言。实现和实验未复现。
- **Canonical problems:** [BIP-0061](DETAILED_INVENTORY.md#BIP-0061).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S05/W0361**, [WORKS](../01_discovery/S05/WORKS.md) line 27: Language Model Tokenizers Introduce Unfairness Between Languages; [2305.15425v2](https://arxiv.org/pdf/2305.15425v2), Petrov et al., NeurIPS 2023
  - Original register aliases / era / family / provenance: W0361
  - Source-scoped evidence/depth: **RC** [B14 card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0361.md). Parallel-sentence tokenizer length measurements: byte, code point and subword separately. No new LM training; dialect and UNK controls matter.
- **S06/W0361**, [WORKS](../01_discovery/S06/WORKS.md) line 35: **Language Model Tokenizers Introduce Unfairness Between Languages**; [2305.15425v2](https://arxiv.org/pdf/2305.15425v2); [card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0361.md)
  - Original register aliases / era / family / provenance: W0361; 2023 cross-language resource accounting
  - Source-scoped evidence/depth: FLORES-200 semantic-content comparison: ByT5 Shan/English3.94 byte-length ratio, CANINE1.42 code-point ratio. RoBERTa timing example is not byte-model timing. Supports exposure/context accounting, not cross-model FLOPs conversion. **RF** §§3–6/Table5.
- **S08/S08-W29**, [WORKS](../01_discovery/S08/WORKS.md) line 60: **Language Model Tokenizers Introduce Unfairness Between Languages**, [2305.15425v2](https://arxiv.org/pdf/2305.15425v2), NeurIPS 2023. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0361.md).
  - Original register aliases / era / family / provenance: S08-W29 / **W0361** / catalog reuse
  - Source-scoped evidence/depth: **Language Model Tokenizers Introduce Unfairness Between Languages**, [2305.15425v2](https://arxiv.org/pdf/2305.15425v2), NeurIPS 2023. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0361.md). ByT5 Shan/English3.94 vs CANINE1.42; overall highest/lowest ratios ~4.53/~4.58. Universal coverage does not guarantee parallel-content position parity; counts ≠ capability or universal pricing ratio.

</details>

<a id="BIW-0034"></a>
## BIW-0034 — Rate–Utility Frontiers for Language Encodings: Comparing Tokens, Bytes, and Pixels Under Controlled Linguistic Content

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **状态：全文实读（正文方法/实验/限制及相关附录A、B、C、D）**。Ingo Ziegler、Martin Krebs、Desmond Elliott，2026；arXiv:2607.16117v1，[HTML](https://arxiv.org/html/2607.16117v1)、[v1 PDF](https://arxiv.org/pdf/2607.16117v1)。FetchURL HTML正文至附录B开头即截断且页头漏首作者；另合法获取PDF并用pdftotext读取表1–2、附录A、B、C.1–C.3、D，首作者以PDF首页为准。未执行论文代码或复现实验；图形仅依据正文、图注及PDF文本数据核查。
- **Carrying card:** [old scoped FULL/BIW-0034](../../flued_multigranularity_survey_20261108/03_reading/B08/W0363.md).
- **Canonical problem records:** [BIP-0062](DETAILED_INVENTORY.md#BIP-0062), [BIP-0283](DETAILED_INVENTORY.md#BIP-0283).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** U subwords/UTF-8 bytes/pixel patches → bidirectional Transformer and one learned-query slot → candidate-embedding retrieval or topic class → InfoNCE/alignment/supervised CE. C full source/task known; not next-byte generation.
- **Learning and causal baseline:** U subwords/UTF-8 bytes/pixel patches → bidirectional Transformer and one learned-query slot → candidate-embedding retrieval or topic class → InfoNCE/alignment/supervised CE. C full source/task known; not next-byte generation.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0363`.
- **Full-source target / version:** https://arxiv.org/pdf/2607.16117v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U subwords/UTF-8 bytes/pixel patches → bidirectional Transformer and one learned-query slot → candidate-embedding retrieval or topic class → InfoNCE/alignment/supervised CE. C full source/task known; not next-byte generation.
- **Learning and causal baseline:** U subwords/UTF-8 bytes/pixel patches → bidirectional Transformer and one learned-query slot → candidate-embedding retrieval or topic class → InfoNCE/alignment/supervised CE. C full source/task known; not next-byte generation.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0363.md). Scope header: **状态：全文实读（正文方法/实验/限制及相关附录A、B、C、D）**。Ingo Ziegler、Martin Krebs、Desmond Elliott，2026；arXiv:2607.16117v1，[HTML](https://arxiv.org/html/2607.16117v1)、[v1 PDF](https://arxiv.org/pdf/2607.16117v1)。FetchURL HTML正文至附录B开头即截断且页头漏首作者；另合法获取PDF并用pdftotext读取表1–2、附录A、B、C.1–C.3、D，首作者以PDF首页为准。未执行论文代码或复现实验；图形仅依据正文、图注及PDF文本数据核查。
- **Canonical problems:** [BIP-0062](DETAILED_INVENTORY.md#BIP-0062), [BIP-0283](DETAILED_INVENTORY.md#BIP-0283).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S05/W0363**, [WORKS](../01_discovery/S05/WORKS.md) line 28: Rate–Utility Frontiers for Language Encodings: Comparing Tokens, Bytes, and Pixels Under Controlled Linguistic Content; [2607.16117v1](https://arxiv.org/html/2607.16117v1), Ziegler, Krebs, Elliott, 2026
  - Original register aliases / era / family / provenance: W0363
  - Source-scoped evidence/depth: **RC** [B08 card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0363.md). Byte/subword/pixel inputs; bidirectional transformer, learned single-query pooling, task-specific InfoNCE or classification. No autoregressive reconstruction; controlled parallel content, 204-candidate retrieval floors.
- **S08/S08-W30**, [WORKS](../01_discovery/S08/WORKS.md) line 61: **Rate–Utility Frontiers for Language Encodings: Comparing Tokens, Bytes, and Pixels Under Controlled Linguistic Content**, [2607.16117v1](https://arxiv.org/html/2607.16117v1), 2026. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0363.md).
  - Original register aliases / era / family / provenance: S08-W30 / **W0363** / catalog reuse
  - Source-scoped evidence/depth: **Rate–Utility Frontiers for Language Encodings: Comparing Tokens, Bytes, and Pixels Under Controlled Linguistic Content**, [2607.16117v1](https://arxiv.org/html/2607.16117v1), 2026. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B08/W0363.md). SIB-200 701/99/204 split, 13languages/5scripts, latent width1–256. “Recovery” = retrieval among204 candidates, not lossless text reconstruction; task-optimal encodings differ. FLOPs to best checkpoint omit selection/early-stop overhead.

</details>

<a id="BIW-0035"></a>
## BIW-0035 — Using the Output Embedding to Improve Language Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Ofir Press and Lior Wolf, [arXiv:1608.05859v3](https://arxiv.org/pdf/1608.05859v3), 21 Feb 2017, 7 PDF pages. Alias S04/W0364. Related formal publication EACL 2017; this card is locked to arXiv v3, not an unexamined comparison of versions. **Reading: FULL:** §§1–4, Tables 1–8, references; no appendix in this version. PDF p.5 Table 6–8 visually verified. Not code or checkpoint verification.

**Problem:** word language models store separate input and output representations for the same vocabulary and weak input-row updates for infrequent words. **Solution:** reuse a common input embedding as the transposed output classifier, optionally inserting a regularized projection, and use the common BPE vocabulary for three-way neural translation sharing.
- **Carrying card:** [R08/BIW-0035](../03_reading/R08/BIW-0035.md).
- **Canonical problem records:** [BIP-0184](DETAILED_INVENTORY.md#BIP-0184), [BIP-0185](DETAILED_INVENTORY.md#BIP-0185), [BIP-0186](DETAILED_INVENTORY.md#BIP-0186).
- **Units — input / internal / output / supervision (current):** WordLMorBPEsource/target / recurrentLMorattentiveNMT / nextword/subword / CE; tiedIOandthree-wayNMT distinct, projectionregularizationoptional.

### Current substantive interface, technique, evidence and limits

### Problem, solution, unit and method

**Problem:** word language models store separate input and output representations for the same vocabulary and weak input-row updates for infrequent words. **Solution:** reuse a common input embedding as the transposed output classifier, optionally inserting a regularized projection, and use the common BPE vocabulary for three-way neural translation sharing.

The main LM consumes previous **word IDs**, maintains LSTM hidden vectors, emits a distribution over next **word IDs**, and is supervised with next-word cross-entropy. Text8 is a dataset name, not evidence of a byte prediction interface; actual preprocessing/vocabulary is as referenced. Neural translation consumes source BPE subword IDs, emits target BPE subwords autoregressively with attention over source and teacher-forced previous targets. Encoder input ↔ decoder input ↔ decoder output is the three-way sharing axis; decoder-only variant ties decoder input ↔ decoder output but not encoder input. Neither implies recurrent-layer sharing. Shared source/target union vocabulary includes tokens appearing on only one side. Any output bias, EOS, beam-search configuration and exact partial-subword scoring not specified; no verification algorithm.

Borrowed LSTM preserves history, attention conditions decoding on source, BPE supplies joint symbols, dropout controls overfitting, optional P is an H×H projection between recurrent state and tied output table regularized by λ||P||² with λ=.15 (§3); P is not a second vocabulary classifier. SGD optimizes LM, and NMT uses Adadelta. The updates explain that untied input rows are updated only on occurrence whereas output softmax ordinarily updates every row; in tied S, input and output gradients add, with most rows resembling untied output-side updates. This is not an unconditional statement that training trajectories or matrices are identical. Historical earlier bilinear models already employed tying; the work and concurrent Inan paper explicitly discuss this.

### Evidence and counterexamples

- **BIP-0184:** PTB large 66M baseline test perplexity 78.4 versus 51M tied 74.3; with Bayesian dropout 75.2 (66M) versus 73.2 (51M) (Table 5). Train perplexity moves in the opposite direction (37.8→48.5 for ordinary dropout), consistent with but not proving regularization. Rare-word input update reasoning relies on conventional unregularized per-token gradient and full softmax; optimizer/weight decay can modify practical updates.
- **BIP-0185:** PTB small no-dropout model 4.65M, test 114.5; tied 2.65M, 112.4; projection regularization alone 4.69M, 111.7; combined 2.69M, 100.9 (Table 6). Table 7 text8 195.3/187.1/199.0/183.2; IMDB 94.3/94.8/94.4/91.5; BBC 110.8/106.8/108.7/98.9: individual tying or projection can worsen, combination improves these examples. Authors report P did not help the large dropout-regularized model (§4.2). Projection is not shown necessary under all dropout and hidden-size settings.
- **Counterexample:** tying skip-gram word2vec degrades embedding similarity (Table 2: SimLex input/output/tied .30/.29/.17; MEN .66/.61/.50), unlike RNN LM. Table 4 rank correlations tied vs output/input in small LM .65/.31 and large .77/.45; related but different representations.
- **BIP-0186:** NMT EN→FR baseline/decoder-only/three-way 168M/122M/80M and test BLEU 33.13/33.26/33.46; EN→DE 165M/119M/79M and 16.79/16.54/17.15 (Table 8). Shared BPE overlaps reported EN–FR 85k shared, 2k source-only, 7k target-only; EN–DE 80k, 3k, 11k (Table 1). Models trained 300k updates with 89,500 BPE merges; hidden size 1000, embeddings 500 (§4.3). Equal optimizer updates are not equal FLOPs or wall time. The parallel-data selection, no seed variance or serving cost limit claims of statistical equivalence.

**Inventory scope:** this is evidence on word or BPE tables and recurrent translation, not a controlled experiment on small-byte heads; no extrapolation of the parameter savings or benefit to V=256.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0364`.
- **Full-source target / version:** https://arxiv.org/pdf/1608.05859v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Word → LSTM states → word (LM); BPE subword → encoder/decoder → BPE subword (NMT); next-unit CE
- **Learning and causal baseline:** **General background, not byte evidence.** Decoder causal; source NMT bidirectional access. PTB/text8/IMDB/BBC; NMT 300K updates, 500-d embeddings/1000 hidden. Update rules, tying, projection regularization, three-way tying distinct. Table bodies incompletely extracted.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0184](DETAILED_INVENTORY.md#BIP-0184), [BIP-0185](DETAILED_INVENTORY.md#BIP-0185), [BIP-0186](DETAILED_INVENTORY.md#BIP-0186).
- **Reading ownership:** [R08](batches/R08.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S04/W0364**, [WORKS](../01_discovery/S04/WORKS.md) line 20: **W0364**, 2016/2017, Press & Wolf, *Using the Output Embedding to Improve Language Models*; [arXiv v3](https://arxiv.org/html/1608.05859v3), [EACL](https://aclanthology.org/E17-2025/) CATALOG reuse; P §§3/4.2/4.3; no old card
  - Original register aliases / era / family / provenance: **W0364**, 2016/2017, Press & Wolf, *Using the Output Embedding to Improve Language Models*; [arXiv v3](https://arxiv.org/html/1608.05859v3), [EACL](https://aclanthology.org/E17-2025/)
  - Source-scoped evidence/depth: CATALOG reuse; P §§3/4.2/4.3; no old card **General background, not byte evidence.** Decoder causal; source NMT bidirectional access. PTB/text8/IMDB/BBC; NMT 300K updates, 500-d embeddings/1000 hidden. Update rules, tying, projection regularization, three-way tying distinct. Table bodies incompletely extracted.

</details>

<a id="BIW-0036"></a>
## BIW-0036 — Tying Word Vectors and Word Classifiers: A Loss Framework for Language Modeling

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Hakan Inan, Khashayar Khosravi, Richard Socher, ICLR 2017, [arXiv:1611.01462v3](https://arxiv.org/pdf/1611.01462v3), 11 March 2017; alias S04/W0365. **Reading FULL:** PDF pp.1–13, §§1–7, full Appendix A/B and Figures 1–2/Tables 1–4; visually checked pp.6–8 due to extraction errors. No missing appendix in locked version. Reading is not verification of proof, training code, or results.

Word-ID input, two-layer LSTM hidden states, word-class softmax output and next-word one-hot supervision, conditioned on prior words. The PTB vocabulary keeps 10k frequent words and replaces the rest with `<unk>`; PTB train/valid/test 923k/73k/82k words, Wikitext-2 2.088M/217k/245k tokens with 33,278 words (§6). No native byte model, raw-text byte budgets, EOS handling, arbitrary byte-prefix probability or generation verifier is specified.
- **Carrying card:** [R08/BIW-0036](../03_reading/R08/BIW-0036.md).
- **Canonical problem records:** [BIP-0187](DETAILED_INVENTORY.md#BIP-0187), [BIP-0188](DETAILED_INVENTORY.md#BIP-0188), [BIP-0189](DETAILED_INVENTORY.md#BIP-0189).
- **Units — input / internal / output / supervision (current):** PTB10K/WikiText2wordIDs / LSTMstates / wordsoftmax / CE+optionalembedding-derivedKL; REimposesW=Lᵀ, theoremconditionalsharedsubspaceonly.

### Current substantive interface, technique, evidence and limits

### Interface, problem and technique

Word-ID input, two-layer LSTM hidden states, word-class softmax output and next-word one-hot supervision, conditioned on prior words. The PTB vocabulary keeps 10k frequent words and replaces the rest with `<unk>`; PTB train/valid/test 923k/73k/82k words, Wikitext-2 2.088M/217k/245k tokens with 33,278 words (§6). No native byte model, raw-text byte budgets, EOS handling, arbitrary byte-prefix probability or generation verifier is specified.

**Problem / one-sentence solution:** one-hot targets ignore semantic proximity among vocabulary classes and separate input/output tables spend parameters; derive target distributions from same-model embedding similarity, add KL loss, and independently test reusing input word vectors as the output class projection. L ∈ R^(d×V) has word columns and W ∈ R^(V×d); RE enforces **W=Lᵀ** and removes output bias. This is input-table ↔ output classifier sharing, not layer-to-layer or independent head sharing. AL is a separate supervision choice: with target word y, soft teacher `softmax(Lᵀ L_y / τ)` matches `softmax(W h / τ)` under added KL weighted α. It is learned from the model’s own embeddings, not a separate large distillation teacher. CE remains the standard evaluation loss. LSTM, variational dropout (same mask through unrolling), gradient clipping and SGD are the actual techniques (§§2–3, Appendix A).

### Derivation and proper limits — BIP-0187/0188

The paper's §4 argues shared column space under **equal embedding and hidden dimensions, zero bias, augmented-only loss, zero attainable training loss, high-temperature approximation, mean-zero logits, full-rank L/W and enough linearly independent hidden states**. Under these assumptions it obtains `W=Lᵀ A`, with A a square basis transformation; exact numerical equality is **an additional architectural constraint**, not the theorem's conclusion. A must be absorbed by a sufficiently flexible hidden transformation; the argument is conditional and its centering/zero-loss assumptions are not independently proved by this reading. For V≤d, the usual low-dimensional vocabulary subspace intuition can become vacuous and needs separate analysis; this paper does not test V=256 or fully normalized cosine classifiers.

Figure 1 reports a 20k contiguous PTB-word, 300-unit model with no dropout/weight decay and normalized embedding rows; 10 runs. At temperature 10 subspace distance falls from ~1 for CE to ~.06 for purely augmented loss; not equality of tables, and not a direct test that test perplexity gains are caused solely by the derived mechanism. The practical loss uses τ=20 and α=γτ, γ=.5–.8 PTB or 1–1.5 WikiText-2; experimental distributional learning is separate from parameter reuse.

### Factorial results and budgets — BIP-0189

Four arms baseline/AL/RE/REAL, identical nominal hidden sizes but RE eliminates a V×d classifier table, hence unequal parameter count (Table 1). PTB test perplexity:

| Units | baseline | AL | RE | REAL |
|---|---:|---:|---:|---:|
| 200 | 87.3 | 82.9 | 85.1 | 82.7 |
| 650 | 77.7 | 74.7 | 73.9 | 73.2 |
| 1500 | 72.6 | 71.2 | 69.0 | 68.5 |

Wikitext-2 small test 105.9/103.8/100.5/98.9; medium 95.3/93.1/87.7/87.0. Large Wikitext-2 configurations were not run for insufficient resources. Small PTB models were retrained from their own first-run final parameters, which improved non-baseline results (Table 1 footnote), so compare with that protocol in mind. WikiText-2 halves (Table 2), small test on partition 1: 148.0/142.5/141.9/140.6; partition 2 148.6/143.7/140.9/138.4. Neither proves the cause is purely dataset size.

Table 3 large baseline VD-LSTM 66M vs REAL 51M, and tied recurrent-highway network 24M vs 32M baseline; train/runtime/FLOPs unreported. Appendix A: 35-step truncated backpropagation; LR 1 with size-dependent decay, gradient norm thresholds 5/5/6; different dropout rates by size/dataset; no fixed matched compute or separate teacher. Full comparative seed counts not reported. These findings support distinct AL and RE entries, not a universal or pure-byte tying advantage.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0365`.
- **Full-source target / version:** https://arxiv.org/pdf/1611.01462v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Word → recurrent state → word; CE + embedding-derived soft target KL
- **Learning and causal baseline:** **Background.** Causal word prediction, PTB 10K/WikiText-2 33,278 vocabulary, 200/650/1500 hidden. Theory requires equal dimensions, zero bias, augmented loss, high temperature, zero loss and rank/span conditions; not arbitrary-byte optimality. Four-way CE/AL/RE/REAL comparison.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0187](DETAILED_INVENTORY.md#BIP-0187), [BIP-0188](DETAILED_INVENTORY.md#BIP-0188), [BIP-0189](DETAILED_INVENTORY.md#BIP-0189).
- **Reading ownership:** [R08](batches/R08.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S04/W0365**, [WORKS](../01_discovery/S04/WORKS.md) line 21: **W0365**, 2016/2017, Inan, Khosravi & Socher, *Tying Word Vectors and Word Classifiers: A Loss Framework for Language Modeling*; [v3](https://arxiv.org/html/1611.01462v3) CATALOG reuse; P §§3–4/6.1–6.3, Appendix A/B selective
  - Original register aliases / era / family / provenance: **W0365**, 2016/2017, Inan, Khosravi & Socher, *Tying Word Vectors and Word Classifiers: A Loss Framework for Language Modeling*; [v3](https://arxiv.org/html/1611.01462v3)
  - Source-scoped evidence/depth: CATALOG reuse; P §§3–4/6.1–6.3, Appendix A/B selective **Background.** Causal word prediction, PTB 10K/WikiText-2 33,278 vocabulary, 200/650/1500 hidden. Theory requires equal dimensions, zero bias, augmented loss, high temperature, zero loss and rank/span conditions; not arbitrary-byte optimality. Four-way CE/AL/RE/REAL comparison.

</details>

<a id="BIW-0037"></a>
## BIW-0037 — Weight Tying Biases Token Embeddings Towards the Output Space

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **FULL**｜Antonio Lopardo、Avyukth Harish、Catherine Arnett、Akshat Gupta，2026-03-27，[arXiv 2603.26663v1](https://arxiv.org/html/2603.26663v1)。读§1–8、表1–2及附录A–H，含梯度干预与下游表7；代码/实验未独立验证。
- **Carrying card:** [old scoped FULL/BIW-0037](../../flued_multigranularity_survey_20261108/03_reading/B14/W0366.md).
- **Canonical problem records:** [BIP-0190](DETAILED_INVENTORY.md#BIP-0190), [BIP-0191](DETAILED_INVENTORY.md#BIP-0191).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Token/subword → Transformer → token; next-token CE plus diagnostic/intervention
- **Learning and causal baseline:** **Background.** OLMo/Pythia/GPT-Neo/Qwen comparisons not all same data/size; 10K-step input-gradient ×5 intervention single runs. §§3–6, Appendix E Table 7. No byte-table or cosine-head factorial.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0366`.
- **Full-source target / version:** https://arxiv.org/pdf/2603.26663v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Token/subword → Transformer → token; next-token CE plus diagnostic/intervention
- **Learning and causal baseline:** **Background.** OLMo/Pythia/GPT-Neo/Qwen comparisons not all same data/size; 10K-step input-gradient ×5 intervention single runs. §§3–6, Appendix E Table 7. No byte-table or cosine-head factorial.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B14/W0366.md). Scope header: **FULL**｜Antonio Lopardo、Avyukth Harish、Catherine Arnett、Akshat Gupta，2026-03-27，[arXiv 2603.26663v1](https://arxiv.org/html/2603.26663v1)。读§1–8、表1–2及附录A–H，含梯度干预与下游表7；代码/实验未独立验证。
- **Canonical problems:** [BIP-0190](DETAILED_INVENTORY.md#BIP-0190), [BIP-0191](DETAILED_INVENTORY.md#BIP-0191).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S04/W0366**, [WORKS](../01_discovery/S04/WORKS.md) line 22: **W0366**, 2026, Lopardo et al., *Weight Tying Biases Token Embeddings Towards the Output Space*; [v1](https://arxiv.org/html/2603.26663v1) CATALOG reuse; F-card `OLD/03_reading/B14/W0366.md`
  - Original register aliases / era / family / provenance: **W0366**, 2026, Lopardo et al., *Weight Tying Biases Token Embeddings Towards the Output Space*; [v1](https://arxiv.org/html/2603.26663v1)
  - Source-scoped evidence/depth: CATALOG reuse; F-card `OLD/03_reading/B14/W0366.md` **Background.** OLMo/Pythia/GPT-Neo/Qwen comparisons not all same data/size; 10K-step input-gradient ×5 intervention single runs. §§3–6, Appendix E Table 7. No byte-table or cosine-head factorial.

</details>

<a id="BIW-0038"></a>
## BIW-0038 — Rethinking Weight Tying: Pseudo-Inverse Tying for LM Stable Training and Updates

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0367`.
- **Full-source target / version:** https://arxiv.org/pdf/2602.04556v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Token/subword (exact tokenizer per experiment not read) → hidden state → same vocabulary; LM objective
- **Learning and causal baseline:** **Background.** Shared orthonormal-column memory and SPD transform. 256M–1.3B continued/from-scratch tests; full result tables/appendix not checked. `V≥d` feasibility is essential for proposed `Z^T Z=I_d`; byte-vocabulary transfer not automatic. Complete authors need primary PDF header.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0192](DETAILED_INVENTORY.md#BIP-0192).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S04/W0367**, [WORKS](../01_discovery/S04/WORKS.md) line 23: **W0367**, 2026, *Rethinking Weight Tying: Pseudo-Inverse Tying for LM Stable Training and Updates*; [v2](https://arxiv.org/html/2602.04556v2) CATALOG reuse; P §4 Eqs4–13, selected introduction/discussion; extracted title may be shortened
  - Original register aliases / era / family / provenance: **W0367**, 2026, *Rethinking Weight Tying: Pseudo-Inverse Tying for LM Stable Training and Updates*; [v2](https://arxiv.org/html/2602.04556v2)
  - Source-scoped evidence/depth: CATALOG reuse; P §4 Eqs4–13, selected introduction/discussion; extracted title may be shortened **Background.** Shared orthonormal-column memory and SPD transform. 256M–1.3B continued/from-scratch tests; full result tables/appendix not checked. `V≥d` feasibility is essential for proposed `Z^T Z=I_d`; byte-vocabulary transfer not automatic. Complete authors need primary PDF header.

<a id="BIW-0039"></a>
## BIW-0039 — AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0368`.
- **Full-source target / version:** https://arxiv.org/pdf/2610.01395v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Text tokens, image tokens, protein units in different tasks; not established as byte text
- **Learning and causal baseline:** **Background candidate.** Claimed support-aware finite-cap table update and first-moment-only optimization, 124M–1B decoder/T5-style tasks. Abstract reports ~20% optimizer-state saving/~1% step overhead. No detailed corroboration here; full author list and experiment geometry need reading.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0193](DETAILED_INVENTORY.md#BIP-0193).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S04/W0368**, [WORKS](../01_discovery/S04/WORKS.md) line 24: **W0368**, 2026, *AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models*; [v1 abs](https://arxiv.org/abs/2610.01395v1) CATALOG reuse; A; HTML failed
  - Original register aliases / era / family / provenance: **W0368**, 2026, *AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models*; [v1 abs](https://arxiv.org/abs/2610.01395v1)
  - Source-scoped evidence/depth: CATALOG reuse; A; HTML failed **Background candidate.** Claimed support-aware finite-cap table update and first-moment-only optimization, 124M–1B decoder/T5-style tasks. Abstract reports ~20% optimizer-state saving/~1% step overhead. No detailed corroboration here; full author list and experiment geometry need reading.

<a id="BIW-0040"></a>
## BIW-0040 — Unsupervised Neural Word Segmentation for Chinese via Segmental Language Modeling

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0386`.
- **Full-source target / version:** https://arxiv.org/pdf/1810.03167v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Chinese characters → latent character segments → characters plus segment-end; marginal sentence likelihood. Generative segment decoder uses past context, while best posterior segmentation of observed text uses the full sentence.
- **Learning and causal baseline:** Chinese characters → latent character segments → characters plus segment-end; marginal sentence likelihood. Generative segment decoder uses past context, while best posterior segmentation of observed text uses the full sentence.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0147](DETAILED_INVENTORY.md#BIP-0147), [BIP-0148](DETAILED_INVENTORY.md#BIP-0148).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S02/W0386**, [WORKS](../01_discovery/S02/WORKS.md) line 20: Sun & Deng, **Unsupervised Neural Word Segmentation for Chinese via Segmental Language Modeling** (EMNLP 2018), [1810.03167v1](https://arxiv.org/html/1810.03167v1); [formal page](https://aclanthology.org/D18-1531/)
  - Original register aliases / era / family / provenance: W0386; reused catalogue
  - Source-scoped evidence/depth: P: §§2–3, equations4–9 and tables1–2; no full-reading claim. Training includes unlabelled test text; Gigaword character pretraining and guideline-labelled variants are separate resources.

<a id="BIW-0041"></a>
## BIW-0041 — A Masked Segmental Language Model for Unsupervised Natural Language Segmentation

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0387`.
- **Full-source target / version:** https://aclanthology.org/2022.sigmorphon-1.5.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Natural-language characters → latent segments → segmentation/LM scoring; masked span Transformer context. Bidirectional context explicitly used; not a causal generator by default. Encoding bytes/codepoints and detailed mask schedule unknown.
- **Learning and causal baseline:** Natural-language characters → latent segments → segmentation/LM scoring; masked span Transformer context. Bidirectional context explicitly used; not a causal generator by default. Encoding bytes/codepoints and detailed mask schedule unknown.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0150](DETAILED_INVENTORY.md#BIP-0150).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S02/W0387**, [WORKS](../01_discovery/S02/WORKS.md) line 22: Downey, Xia, Levow & Steinert-Threlkeld, **A Masked Segmental Language Model for Unsupervised Natural Language Segmentation** (SIGMORPHON 2022), [formal page](https://aclanthology.org/2022.sigmorphon-1.5/), pp.39–50
  - Original register aliases / era / family / provenance: W0387; reused catalogue
  - Source-scoped evidence/depth: A: formal abstract. Chinese and English segmentation comparisons stated, not independently table-checked.

<a id="BIW-0042"></a>
## BIW-0042 — Learning to Discover, Ground and Use Words with Segmental Neural Language Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Kazuya Kawakami, Chris Dyer, Phil Blunsom; [ACL 2019 official PDF, pp. 6429–6441](https://aclanthology.org/P19-1645.pdf). Alias S02/W0401.

**Reading depth: FULL, fresh.** Read §§1–9, Fig. 1, Tables 1–5, and all Appendices A–F, Tables 6–7 (printed pp. 6429–6437 and 6440–6441). Visually checked Tables 1–7, including the numerically dense pp. 6434–6436 and 6441. The intervening pp. 6437–6439 are references, consulted as needed. This is source reading, not independent proof, code inspection or reproduction.
- **Carrying card:** [R03/BIW-0042](../03_reading/R03/BIW-0042.md).
- **Canonical problem records:** [BIP-0149](DETAILED_INVENTORY.md#BIP-0149).
- **Units — input / internal / output / supervision (current):** Finitecharacters/phonemes, Englishspacesremoved; optionalimagefeatures / prefixLSTM+lexicalmemory+latentsegments / segmentsfromlexiconorcharacterAR / semi-MarkovmarginalNLL+expectedlengthpenalty; optionalVGG19grounding.

### Current substantive interface, technique, evidence and limits

**Reading depth: FULL, fresh.** Read §§1–9, Fig. 1, Tables 1–5, and all Appendices A–F, Tables 6–7 (printed pp. 6429–6437 and 6440–6441). Visually checked Tables 1–7, including the numerically dense pp. 6434–6436 and 6441. The intervening pp. 6437–6439 are references, consulted as needed. This is source reading, not independent proof, code inspection or reproduction.

### Four units and actual probability object

Input and supervision are finite-set **characters** (or phoneme symbols in BR-phono); English whitespace is removed, Chinese is already unspaced (§5). Internal representation uses a character-history LSTM plus variable-length latent character segments and a learned lexical memory; output is a sequence of segments generated either in one lexical draw or character-by-character, terminated by special end-of-word and end-of-sequence symbols. This is not established UTF-8 byte modeling. Development/test samples containing character types absent from training are dropped, so the reported performance does not demonstrate open-alphabet coverage. Encoding, exact normalization, and dropped-sample counts are not fully disclosed. The image-conditioned variant additionally inputs pretrained VGG19 convolutional features; image conditioning is a separate source of supervision and compute, not a text-only control.

**Problem:** optimizing a powerful character language model need not recover word-like latent structure, while deterministic word segmentation discards segmentation uncertainty. **One-sentence solution:** marginalize all permitted character segmentations while mixing an open-ended character segment generator with a learned distribution over recurring observed substrings, and regularize posterior segment lengths (§§2–4). Actual techniques: prefix LSTM encodes past characters; a separate LSTM spells each segment; a gated mixture chooses spelling or a lexical-memory categorical draw; semi-Markov dynamic programming marginalizes segmentations; the expectation semiring computes the differentiable expected powered-length penalty; image attention supplies optional external grounding (§§2–4, 6).

**Exact factorization/timing:** p(x)=Σ_{s:concat(s)=x}∏ᵢp(sᵢ|x before sᵢ); a conditional semi-Markov assumption makes the history state depend on the characters already generated, not on previous latent segmentation. p(s|history)=g p_char(s|history)+(1−g)p_lex(s|history). The spelling LSTM autoregressively emits characters then /W; it cannot emit the sentence-ending symbol initially within a segment; the overall sequence ends with a special /S segment (§2.1). The memory's string values are fixed training substrings, minimum length two, frequency ≥F and length ≤L; vector keys and mixture/character distributions are learned. If both branches can generate the same segment their probabilities are added. The forward DP sums over permissible spans, O(n²) as stated, with a maximum span L in the recurrence (§3). The paper does not specify arbitrary partial-segment prefix conditioning, serving caches or a separate verifier; one must not assume a single greedy segmentation equals marginal likelihood. The highest-probability segmentation is recovered with max/backpointers **after observing the whole sentence**, so its use of the full sentence differs from prefix-causal generation. This is not an independently proved probability algorithm.

Training minimizes `−log p(x) + λ E_{s|x} Σ_segments |s|^β` (§4); memory/length penalty are part of the model's inductive bias, not a generic outcome of end-to-end likelihood. History and segment LSTM are explicitly distinct parameter sets; a vocabulary lookup-to-output tie, across-head tie, or any other embedding sharing is not specified. β's numerical setting is not stated in Appendix C; do not infer it.

### Results and constraints

- Table 1 BR-phono word-token F1: complete model 79.3; without memory and penalty 42.5, with memory only 43.3, penalty only 49.5; entropy-based character LSTM 55.0, HMLSTM 10.1, held-out-likelihood-tuned unigram DP 56.1 and bigram HDP 56.9. Boundary evaluation requires **both word boundaries** correct; Appendix F reports segmentation on the union of train/validation/test, not a pure held-out test. Prior-feature methods reach 87.0/88.0 under different features and segmentation-tuning regimes (§7); this is not universal segmentation SOTA.
- Table 2 F1 on BR-text/PTB/CTB/PKU is 73.5/56.9/79.8/73.1 versus bigram HDP 57.3/40.1/67.5/66.9. Chinese corpora use different gold conventions. Table 3 shows errors such as `go ing`; §7 explicitly says all models oversegment multidigit dates/numbers.
- Table 4 test BPC: on PTB, SNLM 1.56, ordinary LSTM 1.65, HDP 1.80; removed spaces mean these are **not comparable to standard spaced PTB results** (§5.1). BPC means per author-defined character/phoneme, not raw byte. Appendix F's numerator concerns the marginal sequence likelihood, including the modeled terminal event as described, but exact corpus-wide special-symbol accounting is not separately tabulated.
- COCO Table 5: character LSTM without/with image 1.55/1.42 BPC, word F1 34.4/35.0; SNLM 1.52/1.38 BPC, F1 46.3/53.1. Visual attention uses pretrained VGG19 features, 8000/2000/10000 images train/dev/test, one caption per image (Appendix B), so conditioning is an additional data and pretrained-model budget, not evidence text alone discovers grounding.
- Appendix A Tables 6–7: BR-text training 7832 sentences/129k characters, PTB 42068/5.1M, CTB 50734/3.1M, PKU 17149/2.6M; L=10/F=10 for Brent, L=5/F=25 for Chinese, L=10/F=100 for PTB and COCO. Appendix C/E: 512-dimensional embeddings and LSTM, 0.5 non-recurrent dropout, Adam 0.01, gradient clip 1; λ/L/F tuned on held-out likelihood, not gold segmentation. Larger memory means total parameters are not matched to plain LSTM; a 1024-hidden-unit LSTM did not improve the Brent baselines (§7). Actual parameter totals, training FLOPs and latency, VGG pretraining budget and random-seed variability are not reported. Bayesian Gibbs baselines use 1000 iterations with annealing (Appendix D).

**Inventory handoff:** [BIP-0149](DETAILED_INVENTORY.md#BIP-0149) should carry separate marginal language scoring and full-sentence MAP segmentation, closed-character filtering, explicit length/lexicon priors, grounded-image budget, union-set F1, and negative cases.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0401`.
- **Full-source target / version:** https://aclanthology.org/P19-1645.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Unsegmented characters → latent word-like segments → predictive character-sequence distribution; language likelihood, optionally visual grounding. Exact inference factorization and causal segmentation behavior unknown here.
- **Learning and causal baseline:** Unsegmented characters → latent word-like segments → predictive character-sequence distribution; language likelihood, optionally visual grounding. Exact inference factorization and causal segmentation behavior unknown here.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0149](DETAILED_INVENTORY.md#BIP-0149).
- **Reading ownership:** [R03](batches/R03.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S02/W0401**, [WORKS](../01_discovery/S02/WORKS.md) line 21: Kawakami, Dyer & Blunsom, **Learning to Discover, Ground and Use Words with Segmental Neural Language Models** (ACL 2019), [P19-1645](https://aclanthology.org/P19-1645/), pp.6429–6441; associated 1811.09353v2
  - Original register aliases / era / family / provenance: W0401; reused catalogue
  - Source-scoped evidence/depth: A: formal abstract/identity. Versioned arXiv HTML failed; do not infer lexicon mixture or DP details from other SLM papers.

</details>

<a id="BIW-0043"></a>
## BIW-0043 — Unsupervised Learning of Word Boundary with Description Length Gain

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Chunyu Kit and Yorick Wilks**, CoNLL 1999, official [proceedings PDF](https://aclanthology.org/W99-0701.pdf), printed/PDF pp. 1–6. Alias S02/W0404. **Reading: FULL** for this assigned text-interface work: all §§1–5, Figure 1, equations, footnote and all results, including visual reading of Table 1 on p.4, which is absent from the text extraction. No appendix in this paper. Full reading is not reproduction or proof verification.

- [BIP-0144](DETAILED_INVENTORY.md#BIP-0144): Unknown word boundaries and unknown words make reliance on a fixed dictionary and delimiters inadequate. **Solution:** count substrings in a corpus, score their description-length gain, and dynamically choose a flat segmentation maximizing a corpus-derived gain score (§§1–3).
- This is a **non-neural** historical minimum-description-length/statistical segmentation method, not a trained byte Transformer. Shannon–Fano empirical code length from corpus symbol frequencies provides the scoring criterion; a dictionary-rule replacement accounts for storing a candidate substring once and replacing its occurrences with an index; a Viterbi-style dynamic program searches segmentations. Expected-maximization and hierarchical chunking are only future work (§5).
- Input is a character/symbol sequence with corpus-wide n-gram counts, not a specified UTF-8 byte stream; representation is indexed string candidates; output is a sequence of segments/boundaries, and there are **no learned neural readout heads**. Training supervision is unlabeled corpus counts; whitespace is used for external evaluation, not supplied as boundary labels, although spaces **are present as ordinary characters to the learner** (§4). Lowercasing and replacing full stops by `@` are described for the example; exact encoding/alphabet and any global normalization beyond what is stated are unknown.
- Entire corpus and the whole utterance are available for candidate counts and decoding; there is no causal streaming-generation claim, teacher, next-byte distribution, EOS policy, verifier, or head-sharing question.
- **Carrying card:** [R02/BIW-0043](../03_reading/R02/BIW-0043.md).
- **Canonical problem records:** [BIP-0144](DETAILED_INVENTORY.md#BIP-0144).
- **Units — input / internal / output / supervision (current):** Corpuscharacter/symbol strings (spaces visible ordinarysymbols) / indexedsubstringcounts and DPsegments / boundaries/segments / unsuperviseddescription-lengthgain, non-neural.

### Current substantive interface, technique, evidence and limits

### Problem, solution, techniques and units

- [BIP-0144](DETAILED_INVENTORY.md#BIP-0144): Unknown word boundaries and unknown words make reliance on a fixed dictionary and delimiters inadequate. **Solution:** count substrings in a corpus, score their description-length gain, and dynamically choose a flat segmentation maximizing a corpus-derived gain score (§§1–3).
- This is a **non-neural** historical minimum-description-length/statistical segmentation method, not a trained byte Transformer. Shannon–Fano empirical code length from corpus symbol frequencies provides the scoring criterion; a dictionary-rule replacement accounts for storing a candidate substring once and replacing its occurrences with an index; a Viterbi-style dynamic program searches segmentations. Expected-maximization and hierarchical chunking are only future work (§5).
- Input is a character/symbol sequence with corpus-wide n-gram counts, not a specified UTF-8 byte stream; representation is indexed string candidates; output is a sequence of segments/boundaries, and there are **no learned neural readout heads**. Training supervision is unlabeled corpus counts; whitespace is used for external evaluation, not supplied as boundary labels, although spaces **are present as ordinary characters to the learner** (§4). Lowercasing and replacing full stops by `@` are described for the example; exact encoding/alphabet and any global normalization beyond what is stated are unknown.
- Entire corpus and the whole utterance are available for candidate counts and decoding; there is no causal streaming-generation claim, teacher, next-byte distribution, EOS policy, verifier, or head-sharing question.

### Method detail and reproducibility qualification

§2 eqs. (1–5) define `DLG(s|X)=DL(X)−DL(X[r→s] ⊕ s)` and `aDLG(s)=DLG(s)/c(s)`. §3 eq. (6) specifies the sum of **average** gains per occurrence; however Figure 1 / eq. (7) describe a sum of `DLG(s)` over segments. The paper does not resolve this apparent specification mismatch; do not silently present the exact recurrence as independently proved to optimize eq. (6). Count-one candidates stop the inner loop; standalone symbols have zero score while one-symbol extraction rules have negative gain. With n utterance length and m maximum common-prefix length, authors state O(n²) without pruning, O(mn) worst bound, O(an) average for corpus average prefix length a (§3–4). Corpus count construction cost, RAM, actual wall time and exact lexicon implementation are not reported here.

### Evidence, limits and counterexamples

- §4 Table 1 (visually checked): as count-corpus size increases from **0.54M to 6.13M characters**, precision increases **67.75→79.33%** but recall decreases **70.39→63.01%**. At 6.13M the random-guess row is **26.40% precision, 20.97% recall**. Thus added counts do not monotonically improve both metrics; longer multiword chunks can suppress reference word boundaries.
- Correctness is a predicted boundary immediately before/after a visible space; this favors a particular orthographic reference and misses some plausible subword analyses (§4). Examples include multiword chunks such as `fulton_county` and erroneous word splits. The paper discusses PTB WSJ but the numerical table is Brown; no comparable strong earlier baseline is established. Prior hierarchical work reported >90% recall without comparable precision, and is not a fair single-number comparison (§4). Evaluation independence / whether the full Brown corpus supplies counts and evaluated passages separately is not established.
- No compute-matched generative comparison, cross-language byte experiment or per-result confidence intervals are reported. This work supplies an early information-theoretic segmentation antecedent, not evidence that maximum compression produces human word boundaries.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0404`.
- **Full-source target / version:** https://aclanthology.org/W99-0701.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Unsegmented orthographic string → lexical segments → segmentation; description-length gain, not neural prediction loss. Encoding granularity beyond the institutional abstract is unknown; no UTF-8 assertion. Whole-utterance segmentation, not certified online byte generation.
- **Learning and causal baseline:** Unsegmented orthographic string → lexical segments → segmentation; description-length gain, not neural prediction loss. Encoding granularity beyond the institutional abstract is unknown; no UTF-8 assertion. Whole-utterance segmentation, not certified online byte generation.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0144](DETAILED_INVENTORY.md#BIP-0144).
- **Reading ownership:** [R02](batches/R02.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S02/W0404**, [WORKS](../01_discovery/S02/WORKS.md) line 15: Kit & Wilks, **Unsupervised Learning of Word Boundary with Description Length Gain** (CoNLL 1999), pp.1–6. [Institutional record](https://scholars.cityu.edu.hk/en/publications/unsupervised-learning-of-word-boundary-with-description-length-ga/); [ACL PDF](https://aclanthology.org/W99-0701.pdf)
  - Original register aliases / era / family / provenance: W0404; reused catalogue
  - Source-scoped evidence/depth: A: institutional abstract and bibliography. ACL landing extraction gave only footer, not paper content.

</details>

<a id="BIW-0044"></a>
## BIW-0044 — Beyond Perplexity: UTF-8 Validity in Byte-aware Language Models

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** - **FULL（阅读范围）**：已读[v2 HTML全文](https://arxiv.org/html/2606.14122v2)正文、附录A–L；本轮直接阅读[v2 PDF](https://arxiv.org/pdf/2606.14122v2)第5、8、18页，补齐表2/3/8/9，并对比v1同页。首作者Sangwhan Moon、Daisuke Oba、Youmi Ma、Tatsuya Hiraoka、Naoaki Okazaki；2026，[v2 PDF](https://arxiv.org/pdf/2606.14122v2)。网页抽取遗漏首作者，以原PDF首页为准。FULL不等于代码/结果核验；本卡未运行代码、未重做实验。
- **身份版本异常**：[arXiv abs版本记录](https://arxiv.org/abs/2606.14122)显示v2但摘要说罕见字符更合法；锁定v2 PDF/HTML摘要及§5.1.1明确常见更高：部分得分96.21%对95.26%。两版PDF首页均为常见更高，而两版abs页面均显示相反方向；目前未获得官方更正，见下方版本复核。
- **学习、对象与权限**：§4、附录B/D为355M自回归模型，8k BPE词表+字节回退，英/日/韩/中目标token占比10/30/30/30，80B训练token；不是纯字节模型。内容为字符UTF-8字节，先导字节和续字节的合法性不同；给前缀后预测后续，不是query访问历史源或多粒度存储。只看前文与局部字节前缀，模型不见后续目标；不存在可再下钻的原库接口或生命周期实验。训练8×B200、76小时（附录B），其他模型与评估成本另计。
- **仪器/结果**：§3.2式(1)为部分进度得分，式(4)须精确生成目标续字节且回到字符边界，式(5)比较教师强制整条候选的对数似然和。附录E限定E0/ED/F0/F4后续范围，拒绝过长、代理项、超上界；阅读的是作者描述，未核状态机实现。§5.1/附录H：common部分96.21%、rare95.26%、unseen86.97%，严格合法分别50.47%、30.24%、33.33%，指标不能混写。L1目标字符准确率60.30%（§5.2），生成一个合法字符不等于字符正确，更不等于长文证据被消费。
- **控制与缺口**：§5.1.2另取139个未见三字节汉字，并扫前缀1–3字节；未见四字节组同时改变编码长度、码点与暴露，不能归因于单变量。§3.3/附录I–J：语境由Gemini 3 Pro合成，语言识别、唯一性、长度筛选，无人工语义核验；L1主要common，不支持稀有语境结论。式(5)比较的gold/生成候选可能token长度不同、总对数概率受长度影响；51个ΔLL>0错误仅证明该子集的作者观察，束搜索可恢复是猜想而非实测（§5.2、附录L）。
- **最近邻/FLUED**：相比MrT5的编码端删除，这里测输出侧结构与目标字符。建议分报严格UTF-8、部分进度、字符精确率、答案/证据位置与正确源替换的行为必要性；本论文仅支持前两类及局部字符，不直接给长程依赖或byte接口性能保证。
- **Carrying card:** [old scoped FULL/BIW-0044](../../flued_multigranularity_survey_20261108/03_reading/B22/W0509.md).
- **Canonical problem records:** [BIP-0063](DETAILED_INVENTORY.md#BIP-0063), [BIP-0064](DETAILED_INVENTORY.md#BIP-0064), [BIP-0065](DETAILED_INVENTORY.md#BIP-0065).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** 8K BPE plus byte fallback / mixed-token causal states / mixed tokens decoded to byte continuations / next-token CE, separate legality and target-character diagnostics.
- **Learning and causal baseline:** Causal mixed-token training and continuation generation; prefix-offset diagnostics are not training constraints. Legality, scalar correctness and semantic answers remain distinct.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0509`.
- **Full-source target / version:** https://arxiv.org/pdf/2606.14122v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** 8K BPE plus byte fallback / mixed-token causal states / mixed tokens decoded to byte continuations / next-token CE, separate legality and target-character diagnostics.
- **Learning and causal baseline:** Causal mixed-token training and continuation generation; prefix-offset diagnostics are not training constraints. Legality, scalar correctness and semantic answers remain distinct.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0509.md). Scope header: - **FULL（阅读范围）**：已读[v2 HTML全文](https://arxiv.org/html/2606.14122v2)正文、附录A–L；本轮直接阅读[v2 PDF](https://arxiv.org/pdf/2606.14122v2)第5、8、18页，补齐表2/3/8/9，并对比v1同页。首作者Sangwhan Moon、Daisuke Oba、Youmi Ma、Tatsuya Hiraoka、Naoaki Okazaki；2026，[v2 PDF](https://arxiv.org/pdf/2606.14122v2)。网页抽取遗漏首作者，以原PDF首页为准。FULL不等于代码/结果核验；本卡未运行代码、未重做实验。 - **身份版本异常**：[arXiv abs版本记录](https://arxiv.org/abs/2606.14122)显示v2但摘要说罕见字符更合法；锁定v2 PDF/HTML摘要及§5.1.1明确常见更高：部分得分96.21%对95.26%。两版PDF首页均为常见更高，而两版abs页面均显示相反方向；目前未获得官方更正，见下方版本复核。
- **Canonical problems:** [BIP-0063](DETAILED_INVENTORY.md#BIP-0063), [BIP-0064](DETAILED_INVENTORY.md#BIP-0064), [BIP-0065](DETAILED_INVENTORY.md#BIP-0065).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S01/W0509**, [WORKS](../01_discovery/S01/WORKS.md) line 64: *Beyond Perplexity: UTF-8 Validity in Byte-aware Language Models*, [2606.14122v2 PDF](https://arxiv.org/pdf/2606.14122v2); [old FULL card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0509.md)
  - Original register aliases / era / family / provenance: W0509; 2026 byte-aware output counterexample; CATALOG-REUSE
  - Source-scoped evidence/depth: Reused FULL card actually read. Strict UTF-8 validity, partial progress and correct target character separate. PDF says common>rare; abs metadata says opposite; do not pick whichever supports narrative.
- **S03/W0509**, [WORKS](../01_discovery/S03/WORKS.md) line 27: W0509 · Beyond Perplexity: UTF-8 Validity in Byte-aware Language Models (2026); [2606.14122v2 PDF](https://arxiv.org/pdf/2606.14122v2) C: [B22/W0509](../../flued_multigranularity_survey_20261108/03_reading/B22/W0509.md)
  - Original register aliases / era / family / provenance: W0509 · Beyond Perplexity: UTF-8 Validity in Byte-aware Language Models (2026); [2606.14122v2 PDF](https://arxiv.org/pdf/2606.14122v2)
  - Source-scoped evidence/depth: C: [B22/W0509](../../flued_multigranularity_survey_20261108/03_reading/B22/W0509.md)
- **S05/W0509**, [WORKS](../01_discovery/S05/WORKS.md) line 29: Beyond Perplexity: UTF-8 Validity in Byte-aware Language Models; [2606.14122v2](https://arxiv.org/html/2606.14122v2), Moon et al., 2026
  - Original register aliases / era / family / provenance: W0509
  - Source-scoped evidence/depth: **RC** [B22 card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0509.md). 8k BPE **with byte fallback**, 355M causal LM, 80B training tokens. Not pure byte modeling. Validity, target correctness, frequency and prefix controls; abs/PDF contradiction unresolved.
- **S07/W0509**, [WORKS](../01_discovery/S07/WORKS.md) line 29: **Beyond Perplexity: UTF-8 Validity in Byte-aware Language Models**; [2606.14122v2 PDF](https://arxiv.org/pdf/2606.14122v2), 2026
  - Original register aliases / era / family / provenance: W0509
  - Source-scoped evidence/depth: RF: `03_reading/B22/W0509.md`, entire card including abs/PDF conflict.
- **S08/S08-W31**, [WORKS](../01_discovery/S08/WORKS.md) line 62: **Beyond Perplexity: UTF-8 Validity in Byte-aware Language Models**, [2606.14122v2](https://arxiv.org/html/2606.14122v2), 2026-06-25. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0509.md).
  - Original register aliases / era / family / provenance: S08-W31 / **W0509** / catalog reuse
  - Source-scoped evidence/depth: **Beyond Perplexity: UTF-8 Validity in Byte-aware Language Models**, [2606.14122v2](https://arxiv.org/html/2606.14122v2), 2026-06-25. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0509.md). 355M; partial vs strict legality differ sharply; common/rare direction in abs conflicts with both PDFs. Character frequency/byte length confounds, synthetic contexts not fully human-validated; legality ≠ target correctness.

</details>

<a id="BIW-0045"></a>
## BIW-0045 — MAGNET: Improving the Multilingual Fairness of Language Models with Adaptive Gradient-Based Tokenization

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** - **状态：FULL（限定所列论文）**。Orevaoghene Ahia、Sachin Kumar、Hila Gonen、Valentin Hofmann、Tomasz Limisiewicz、Yulia Tsvetkov、Noah A. Smith，NeurIPS 2024；[arXiv v2 PDF](https://arxiv.org/pdf/2407.08818v2)。读PDF pp.1–19正文与附录A–E，图按图注和正文理解，未逐像素数字化。HTML入口404，PDF正常；不等于代码或实验认证。
- **学习/对象**：§2.1–2.2、式(1)–(4)：因果字节前缀经小Transformer、脚本专门边界预测器，Gumbel采样与下一字节交叉熵联合训练；每脚本二项先验控制段数，段内平均作为中层载荷，重复上采样并带字节skip；不是监督真实词界，也不是按未来问题回访。脚本ID前置（附录D），推理选择器能看到整条序列脚本，正文脚注10明确假设单脚本，代码切换未解决；句级脚本识别若用未来字符需另核因果部署。
- **数据/粒度/可见性**：§3.1九语：英语、西班牙语、法语；俄语、乌克兰语、白俄罗斯语；泰卢固语、孟加拉语、印地语。OSCAR各语预训练约2.3–2.5亿字节（附录C图6）；FLORES平行句计算英语/俄语/泰卢固语锚点字节/空格词比例。输入和输出是字节，表示是动态段；脚本标签是路由地址不是载荷。没有原文档ID、更新删除或长期源回访合同。
- **结果/对照/代价**：§4表2、§5表3及附录表6：字节、共享DTP 5×/10×、多种BPE，与三个预测器的模型比较；最优模型因任务而异。XQUAD平均字节44.62、MAGNET(1,2,4) 44.61；极高(5,10,20) 41.06，印地语从29.18降21.23；SIB泰卢固语68.63降53.90。图4只报英/印/俄相对推理时间；附录D约126M参数、4张A40、38000步、两种子。未见等真实原文字节、参数和实际总训练/部署墙钟同时匹配的完整账。
- **独立复核线索**：正文图3与附录表6(a)同名XNLI行若干值不一致，例如byte西语71.09 vs 71.77、平均68.68 vs 69.12；可能是绘图或版本/设置差异，暂不裁论文错，交独立复核。附录表6(d)的(3,6,12) SIB平均69.87与正文表3的71.43也待核。比对参数量是否包含多预测器同容量控制，文内未给等容量单预测器隔离。
- **决策**：同一真实原文、字节数、脚本标签权限、总参数及端到端时间分账；加共享预测器同容量与混写/无空格语种对照。高压缩伤特定语言时不能按平均分通过；不据此选定架构。
- **Carrying card:** [old scoped FULL/BIW-0045](../../flued_multigranularity_survey_20261108/03_reading/B26/W0510.md).
- **Canonical problem records:** [BIP-0222](DETAILED_INVENTORY.md#BIP-0222), [BIP-0223](DETAILED_INVENTORY.md#BIP-0223).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** **RC** [B26 card](../../flued_multigranularity_survey_20261108/03_reading/B26/W0510.md). Byte/dynamic segment/byte, Gumbel boundary learning and per-script rate prior; next-byte cross-entropy. Nine languages, three script groups; entire-sequence script selector assumes single script.
- **Learning and causal baseline:** **RC** [B26 card](../../flued_multigranularity_survey_20261108/03_reading/B26/W0510.md). Byte/dynamic segment/byte, Gumbel boundary learning and per-script rate prior; next-byte cross-entropy. Nine languages, three script groups; entire-sequence script selector assumes single script.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0510`.
- **Full-source target / version:** https://arxiv.org/pdf/2407.08818v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **RC** [B26 card](../../flued_multigranularity_survey_20261108/03_reading/B26/W0510.md). Byte/dynamic segment/byte, Gumbel boundary learning and per-script rate prior; next-byte cross-entropy. Nine languages, three script groups; entire-sequence script selector assumes single script.
- **Learning and causal baseline:** **RC** [B26 card](../../flued_multigranularity_survey_20261108/03_reading/B26/W0510.md). Byte/dynamic segment/byte, Gumbel boundary learning and per-script rate prior; next-byte cross-entropy. Nine languages, three script groups; entire-sequence script selector assumes single script.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B26/W0510.md). Scope header: - **状态：FULL（限定所列论文）**。Orevaoghene Ahia、Sachin Kumar、Hila Gonen、Valentin Hofmann、Tomasz Limisiewicz、Yulia Tsvetkov、Noah A. Smith，NeurIPS 2024；[arXiv v2 PDF](https://arxiv.org/pdf/2407.08818v2)。读PDF pp.1–19正文与附录A–E，图按图注和正文理解，未逐像素数字化。HTML入口404，PDF正常；不等于代码或实验认证。 - **学习/对象**：§2.1–2.2、式(1)–(4)：因果字节前缀经小Transformer、脚本专门边界预测器，Gumbel采样与下一字节交叉熵联合训练；每脚本二项先验控制段数，段内平均作为中层载荷，重复上采样并带字节skip；不是监督真实词界，也不是按未来问题回访。脚本ID前置（附录D），推理选择器能看到整条序列脚本，正文脚注10明确假设单脚本，代码切换未解决；句级脚本识别若用未来字符需另核因果部署。
- **Canonical problems:** [BIP-0222](DETAILED_INVENTORY.md#BIP-0222), [BIP-0223](DETAILED_INVENTORY.md#BIP-0223).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S05/W0510**, [WORKS](../01_discovery/S05/WORKS.md) line 30: MAGNET: Improving the Multilingual Fairness of Language Models with Adaptive Gradient-Based Tokenization; [2407.08818v2](https://arxiv.org/pdf/2407.08818v2), Ahia et al., NeurIPS 2024
  - Original register aliases / era / family / provenance: W0510
  - Source-scoped evidence/depth: **RC** [B26 card](../../flued_multigranularity_survey_20261108/03_reading/B26/W0510.md). Byte/dynamic segment/byte, Gumbel boundary learning and per-script rate prior; next-byte cross-entropy. Nine languages, three script groups; entire-sequence script selector assumes single script.

</details>

<a id="BIW-0046"></a>
## BIW-0046 — MrT5: Dynamic Token Merging for Efficient Byte-level Language Models

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** - **FULL（阅读范围）**：Julie Kallini、Shikhar Murty、Christopher D. Manning、Christopher Potts、Róbert Csordás；2024初版，[arXiv v3](https://arxiv.org/html/2410.20771v3) 2025-04-02，[PDF](https://arxiv.org/pdf/2410.20771v3)。已读§1–8及附录A–J，包括理论计算式与分语言表；未独立复现、核代码或证明。HTML作者列表遗漏Kallini，以[原记录](https://arxiv.org/abs/2410.20771)和PDF为准。
- **学习来源**：§3式(1)–(7)：在ByT5 Small已预训练模型的第3编码层后加可学习删除门；遮蔽片段恢复交叉熵加删除正则，比例积分控制器控制目标删除率。训练用软注意力掩码、推理硬删隐状态；softmax1避免全部门趋于删除时普通softmax平移不变。附录D另约束注意力得分膨胀。任务损失驱动，并非人工边界标签或终局访问效用监督。
- **粒度/可见性/生命周期**：输入字节，经双向编码上下文聚合后按位置删除；保留位置隐状态可混入被删内容，但不是保留可寻址原始字节。下游编码层与解码器交叉注意力只能见存活表示，问答输入中的问题可参与双向编码，删门并非独立于问题的写前索引；不可因此外推因果自回归模型。早层完整字节只在当次前向存活，未报告可回访源库。多深度处理与多粒度可下钻不是同义。
- **关键对照**：§5/F与无删除、同层随机删除、词尾固定删除、学习边界均值池化和卷积池化比较；目标删50%时MrT5片段恢复每字节位数优于这些同近似长度缩减对照，但不优于无删除。§6表4：TyDiQA GoldP（已保证提供含答案段）ByT5 69.90/79.58 EM/F1，MrT5 68.27/77.73，运行时间下降33.31%；XNLI中文表8 62.12→60.34。表5拼写纠错66.73→63.18、找词76.61→72.02，并非无损。
- **成本与失败**：§5表3单序列44.29→29.99ms（50%目标），是该设置推理时间；附录C式(9)(10)把删前后编码、自回归解码与交叉注意力分账，含输出长短假设，不是端到端成本实测。附录E.2：续训5000步、每步2^20 token，15语等量字节取样，需加上ByT5历史预训练、门和动态打包/批次padding；长答案会摊薄编码侧收益。并未提供中文首/续字节误差或字符规范化错误分解。
- **FLUED关联**：相比W0509输出字符有效性，此作是编码端单层删除与语义迁移；与可保源、按query下钻不同。可引用“匹配删率时可优于随机/固定/两种池化”的限定经验；建议同源替换检验存活表示是否被实际消费，而非凭可解码性断言必要。
- **Carrying card:** [old scoped FULL/BIW-0046](../../flued_multigranularity_survey_20261108/03_reading/B22/W0511.md).
- **Canonical problem records:** [BIP-0066](DETAILED_INVENTORY.md#BIP-0066), [BIP-0067](DETAILED_INVENTORY.md#BIP-0067), [BIP-0068](DETAILED_INVENTORY.md#BIP-0068), [BIP-0069](DETAILED_INVENTORY.md#BIP-0069).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Bytes → surviving contextual states → bytes; ByT5 span recovery plus deletion regularization/controller. Bidirectional encoder, causal target decoder; deletion is not literal pairwise averaging.
- **Learning and causal baseline:** Bytes → surviving contextual states → bytes; ByT5 span recovery plus deletion regularization/controller. Bidirectional encoder, causal target decoder; deletion is not literal pairwise averaging.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0511`.
- **Full-source target / version:** https://arxiv.org/pdf/2410.20771v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes → surviving contextual states → bytes; ByT5 span recovery plus deletion regularization/controller. Bidirectional encoder, causal target decoder; deletion is not literal pairwise averaging.
- **Learning and causal baseline:** Bytes → surviving contextual states → bytes; ByT5 span recovery plus deletion regularization/controller. Bidirectional encoder, causal target decoder; deletion is not literal pairwise averaging.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0511.md). Scope header: - **FULL（阅读范围）**：Julie Kallini、Shikhar Murty、Christopher D. Manning、Christopher Potts、Róbert Csordás；2024初版，[arXiv v3](https://arxiv.org/html/2410.20771v3) 2025-04-02，[PDF](https://arxiv.org/pdf/2410.20771v3)。已读§1–8及附录A–J，包括理论计算式与分语言表；未独立复现、核代码或证明。HTML作者列表遗漏Kallini，以[原记录](https://arxiv.org/abs/2410.20771)和PDF为准。 - **学习来源**：§3式(1)–(7)：在ByT5 Small已预训练模型的第3编码层后加可学习删除门；遮蔽片段恢复交叉熵加删除正则，比例积分控制器控制目标删除率。训练用软注意力掩码、推理硬删隐状态；softmax1避免全部门趋于删除时普通softmax平移不变。附录D另约束注意力得分膨胀。任务损失驱动，并非人工边界标签或终局访问效用监督。
- **Canonical problems:** [BIP-0066](DETAILED_INVENTORY.md#BIP-0066), [BIP-0067](DETAILED_INVENTORY.md#BIP-0067), [BIP-0068](DETAILED_INVENTORY.md#BIP-0068), [BIP-0069](DETAILED_INVENTORY.md#BIP-0069).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S01/W0511**, [WORKS](../01_discovery/S01/WORKS.md) line 65: *MrT5: Dynamic Token Merging for Efficient Byte-level Language Models*, [2410.20771v3](https://arxiv.org/abs/2410.20771v3), 2025-04-02; [old FULL card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0511.md)
  - Original register aliases / era / family / provenance: W0511; 2024/2025 encoder-side byte deletion; CATALOG-REUSE
  - Source-scoped evidence/depth: Reused FULL card actually read. ByT5 initialization plus 5k continuation steps; encoder savings diminish with long target output; no-delete quality remains stronger.
- **S02/W0511**, [WORKS](../01_discovery/S02/WORKS.md) line 36: Kallini et al., **MrT5: Dynamic Token Merging for Efficient Byte-level Language Models**, [2410.20771v3](https://arxiv.org/html/2410.20771v3), 2025-04-02
  - Original register aliases / era / family / provenance: W0511; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B22/W0511.md`, §§1–8, A–J per card; card itself read.
- **S04/W0511**, [WORKS](../01_discovery/S04/WORKS.md) line 27: **W0511**, 2024/2025, *MrT5: Dynamic Token Merging for Efficient Byte-level Language Models*; [v3](https://arxiv.org/html/2410.20771v3) CATALOG reuse; F-card `OLD/03_reading/B22/W0511.md`
  - Original register aliases / era / family / provenance: **W0511**, 2024/2025, *MrT5: Dynamic Token Merging for Efficient Byte-level Language Models*; [v3](https://arxiv.org/html/2410.20771v3)
  - Source-scoped evidence/depth: CATALOG reuse; F-card `OLD/03_reading/B22/W0511.md` ByT5-Small continued training 5K steps, 15 languages, target deletion. Gate after encoder layer3; decoder causal over target. Baselines no/random/fixed deletion and pooling. Runtime gains trade quality; long answers dilute encoder saving. Exact tying not rechecked.
- **S06/W0511**, [WORKS](../01_discovery/S06/WORKS.md) line 36: **MrT5: Dynamic Token Merging for Efficient Byte-level Language Models**; [2410.20771v3](https://arxiv.org/html/2410.20771v3),2025-04-02; [card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0511.md)
  - Original register aliases / era / family / provenance: W0511; 2024/2025 encoder pruning
  - Source-scoped evidence/depth: ByT5 Small base,5000 continuation steps; 50% deletion 44.29→29.99ms/sequence; TyDiQA F1 79.58→77.73 with33.31% runtime reduction. Long outputs dilute savings; ByT5 pretraining not free. **RF** §§3,5–6/App.C,E.
- **S07/W0511**, [WORKS](../01_discovery/S07/WORKS.md) line 26: **MrT5: Dynamic Token Merging for Efficient Byte-level Language Models**; [2410.20771v3](https://arxiv.org/html/2410.20771v3), 2025
  - Original register aliases / era / family / provenance: W0511
  - Source-scoped evidence/depth: RF: `03_reading/B22/W0511.md`, entire card.

</details>

<a id="BIW-0047"></a>
## BIW-0047 — Compute Optimal Tokenization

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Tomasz Limisiewicz, Artidoro Pagnoni, Srini Iyer, Mike Lewis, Sachin Mehta, Alisa Liu, Margaret Li, Gargi Ghosh, Luke Zettlemoyer; [arXiv:2605.01188v2 PDF](https://arxiv.org/pdf/2605.01188v2), 26 May 2026. Alias S06/W0512. **Reading: FULL:** §§1–8 and Appendices A–F, pp.1–41, Tables 1–10, Figures 1–26; visually checked pp.13 and 29 (including table alignment); [PDF](../03_reading/R05/sources/BIW-0047.pdf), [text](../03_reading/R05/sources/BIW-0047.txt). Figures extracted as text were used for caption/author conclusions, not independent numerical curve reconstruction; no fitting or experiments rerun.

**Problem:** compute-optimal token counts are not comparable when tokenizers encode different original-text amounts. **Solution:** sweep compression, parameter size and text exposure under specified compute budgets, fit loss versus bytes and compression, and compare latent and external tokenizers. BLT inputs/targets are bytes, its internal global units are variable entropy-selected byte patches, and local encoder/decoder map bytes↔latent using cross-attention; hash n-grams omitted (§2.1/App.A). Baseline alternatives are characters (148k vocabulary, ~1.01 bytes/token), Llama-3 BPE (126k, 4.57 bytes/token), masked-vocabulary variants, and SuperBPE (200k, 6.16); character is **not** byte, even if close on this English corpus. A separate 256-symbol byte arm appears in App.F.5. Token models supervise next subword/character token. No exact original-string marginalization over alternative segmentations is established: reported byte-normalized loss should not silently be upgraded to marginal text probability.
- **Carrying card:** [R05/BIW-0047](../03_reading/R05/BIW-0047.md).
- **Canonical problem records:** [BIP-0239](DETAILED_INVENTORY.md#BIP-0239), [BIP-0240](DETAILED_INVENTORY.md#BIP-0240), [BIP-0241](DETAILED_INVENTORY.md#BIP-0241).
- **Units — input / internal / output / supervision (current):** BytesforBLT and256bytearm,148Kcharacters/separatesubwords forcontrols / entropypatches orbaselinepositions / respective nextunit / ARlikelihood withbyte-normalizedC4score; fittedN≠totalresidentparams.

### Current substantive interface, technique, evidence and limits

### Question, method and unit audit

**Problem:** compute-optimal token counts are not comparable when tokenizers encode different original-text amounts. **Solution:** sweep compression, parameter size and text exposure under specified compute budgets, fit loss versus bytes and compression, and compare latent and external tokenizers. BLT inputs/targets are bytes, its internal global units are variable entropy-selected byte patches, and local encoder/decoder map bytes↔latent using cross-attention; hash n-grams omitted (§2.1/App.A). Baseline alternatives are characters (148k vocabulary, ~1.01 bytes/token), Llama-3 BPE (126k, 4.57 bytes/token), masked-vocabulary variants, and SuperBPE (200k, 6.16); character is **not** byte, even if close on this English corpus. A separate 256-symbol byte arm appears in App.F.5. Token models supervise next subword/character token. No exact original-string marginalization over alternative segmentations is established: reported byte-normalized loss should not silently be upgraded to marginal text probability.

Autoregressive next-unit likelihood and common 8192 original-byte contexts, byte-normalized validation loss on C4; BFGS/least-squares is used to fit isoFLOP minima and power laws, not a learned tokenization algorithm. N in the first fitted law excludes local encoder/decoder or input/output embedding parameters (§3.1/App.B.1). Approximation C≈6NB/T describes the global module; the **actual comparison budget is reported as exact total training FLOPs** in §2.2 and App.B.2 says total compute includes local modules and embeddings. The N convention must not be misrepresented as omitting those costs from all FLOPs. Per-family input/output embedding tying and independent entropy model training/scoring costs are not stated sufficiently to certify; explicitly unknown. No latency, cache, memory or hardware serving measurement is supplied.

### Findings and BIP updates

- [BIP-0239](DETAILED_INVENTORY.md#BIP-0239): 988 latent + 320 subword models, total 50M–6.7B, 4B–1.1T training bytes and 5e18–2e21 FLOPs (§2.2), fixed batch 2M bytes and LR 4e-4 AdamW, warmup-stable-decay. At C=1e20, fitted English optimum is roughly 60 training bytes per **global** parameter (Fig.3); fitted α=.465 β=.471. This approximate association is conditional on recipe, corpus, architecture, N convention and cost function, not a universal byte-per-total-parameter constant. App.A Table 4/5 explicitly reports distinct total parameters (e.g. 143M global →199M BLT total).
- [BIP-0240](DETAILED_INVENTORY.md#BIP-0240): At fixed training compute and model/data optimum, loss versus compression is non-monotonic; fitted BLT optimum decreases from ~3.69 bytes/patch at 1e20 to 3.33 at 2e21 (§3.4). App.C Table 8 at 1e20 gives entropy patches (ρ,T,BPB)=(62.1,3.71,.960), fixed patches (60.0,3.87,.973), subword (58.8,5.36,.947); authors note the subword 5.36 estimate is distorted by the poorly fitting character extreme and alternative fit is 4.11. Their BFGS initialization search is not confidence across independent training seeds; Table 1's 95% numerical-Hessian intervals are fit uncertainty (subword α .501 [.471,.532], β .446 [.387,.506]), not a demonstrated training-seed interval.
- [BIP-0241](DETAILED_INVENTORY.md#BIP-0241): Training-optimal compression is not automatically usage-optimal. §3.5 at matched ~2.1e9 inference FLOPs/byte, 3.3B/T4 gets HellaSwag 74.1% vs 6.7B/T8 68.2%. App.F.6 says T8 is competitive on ARC-Easy while T4 does better on ARC-Challenge; frontier is task-dependent. These are estimated operations, not real decoder latency, prefill, throughput, peak memory or energy.

**Cross-lingual and contrasting controls:** §5/Table 3 (1e20 FLOPs per monolingual language, entropy BLT): English ρ=62.1,T=3.71; Arabic 75.8,4.58; Hindi 95.5,8.09. Hindi parity 2.6 is relative UTF-8 byte length of parallel sentences, not measured semantic entropy. English doubled-byte control and five real languages support association, not a language-invariant law. Joint multilingual training (App.D) weights language sampling by parity and yields roughly shared ρ≈70; in-language data and mixture differ from monolingual. Appendix E identifies original-text context and vocabulary costs as differences from prior contrary scaling results. F.5 byte 256 vs character 148k gap is substantial at small compute, narrows at larger measured budgets; not proof of asymptotic equivalence.

**Open cost items:** entropy-boundary scoring model's original pretraining and segmentation/scoring amortization, total system-resident auxiliary parameters and reuse across runs are not itemized. All important user-facing accounting must list these as unknown rather than assuming free or omitted; normalized input, BOS/EOS accounting, dataset uniqueness, model training seeds, hardware and measured wall times likewise not established. Fixed optimizer recipe is not individually tuned across budgets (§7.2).


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0512`.
- **Full-source target / version:** https://arxiv.org/pdf/2605.01188v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** UTF-8 byte latent models; separate character/BPE/SuperBPE comparators / latent tokens / bytes or respective symbols / causal LM CE; entropy patcher; AdamW and power-law/IsoFLOP fitting.
- **Learning and causal baseline:** UTF-8 byte latent models; separate character/BPE/SuperBPE comparators / latent tokens / bytes or respective symbols / causal LM CE; entropy patcher; AdamW and power-law/IsoFLOP fitting.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0239](DETAILED_INVENTORY.md#BIP-0239), [BIP-0240](DETAILED_INVENTORY.md#BIP-0240), [BIP-0241](DETAILED_INVENTORY.md#BIP-0241).
- **Reading ownership:** [R05](batches/R05.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S06/W0512**, [WORKS](../01_discovery/S06/WORKS.md) line 37: **Compute Optimal Tokenization**; [2605.01188v2](https://arxiv.org/html/2605.01188v2),2026-05-26
  - Original register aliases / era / family / provenance: W0512; 2026 scaling analysis
  - Source-scoped evidence/depth: §§2–3:988 latent+320 subword models,50M–6.7B,4B–1.1T bytes,5e18–2e21 training FLOPs,8192-byte context. Important: fitted N is trunk-only/excludes BLT local modules or subword embeddings, not deployment-total params. **P**; appendix compute/uncertainty and entropy-cost closure missing.

</details>

<a id="BIW-0048"></a>
## BIW-0048 — Local Byte Fusion for Neural Machine Translation

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** - **状态：FULL**。Makesh Narsimhan Sreedhar、Xiangpeng Wan、Yu Cheng、Junjie Hu；[arXiv v3 PDF](https://arxiv.org/pdf/2205.11490v3)，读pp.1–14正文与附录A–F。HTML对照辅助，代码未执行；FULL不是复现或逐图像数字化。
- **学习与粒度**：§3、式(3)–(8)：翻译交叉熵训练；nCF经浅层编码后以1–4字节卷积融合，重复回原字节长度并加权，不是持久压缩；WSF用词跨度构造块注意力掩码，再给高层完整字节序列。编码器见完整源句，解码器仅见已生成前缀及完整源，不是因果字节流结构。位置/词边界是地址，值仍为字节表征，未提供文档回访、撤销。
- **预处理权限**：§4.3先剔除源或目标超过800字节样本（作者称<0.5%），全部方案Moses预分词；空白仍作为字节。§9无空格中文可能需要外部分词器；七语测试并未证明通用于所有无空格文字。表1给德、印地、尼泊尔、泰米尔、泰卢固、柬埔寨、老挝→英语。
- **结果和成本**：表3老挝→英BPE 9.2、dense byte 5.9、nCF 6.4、WSF 6.5；不是普遍胜子词。表4零样本对照子词词表只由高资源语言训练，未知词率高，不能把所有差值归因融合。附录B表7/8：subword 68.7M vs one-hot byte 44.1M；3090、5k步训练5176.8s vs 4184.1s，验证推理22.445s vs 50.963s；同epoch训练不再更快，非同FLOPs/参数。
- **待独立复核**：附录D表10数值似乎第3层28.8最高，而§4.2脚注称4层最好；设置或排版原因未核，不先断言错误。v3摘要称与子词竞争；[abs](https://arxiv.org/abs/2205.11490)可能显示另一版，不得把摘要较强措辞倒填v3。
- **对草案**：把外部词界、预分词后字节数、过滤和编码器完整源权限列入合同；同内容与同算力两表，补无空格、极低资源和整句墙钟对照，暂不因此改最小原型。
- **Carrying card:** [old scoped FULL/BIW-0048](../../flued_multigranularity_survey_20261108/03_reading/B26/W0514.md).
- **Canonical problem records:** [BIP-0070](DETAILED_INVENTORY.md#BIP-0070), [BIP-0071](DETAILED_INVENTORY.md#BIP-0071), [BIP-0072](DETAILED_INVENTORY.md#BIP-0072), [BIP-0073](DETAILED_INVENTORY.md#BIP-0073).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Bytes → **full-length** locally fused byte states → target bytes; translation CE. Source bidirectional; word-span fusion uses Moses-derived word boundaries. Fusion is not necessarily sequence compression.
- **Learning and causal baseline:** Bytes → **full-length** locally fused byte states → target bytes; translation CE. Source bidirectional; word-span fusion uses Moses-derived word boundaries. Fusion is not necessarily sequence compression.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0514`.
- **Full-source target / version:** https://arxiv.org/pdf/2205.11490v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes → **full-length** locally fused byte states → target bytes; translation CE. Source bidirectional; word-span fusion uses Moses-derived word boundaries. Fusion is not necessarily sequence compression.
- **Learning and causal baseline:** Bytes → **full-length** locally fused byte states → target bytes; translation CE. Source bidirectional; word-span fusion uses Moses-derived word boundaries. Fusion is not necessarily sequence compression.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B26/W0514.md). Scope header: - **状态：FULL**。Makesh Narsimhan Sreedhar、Xiangpeng Wan、Yu Cheng、Junjie Hu；[arXiv v3 PDF](https://arxiv.org/pdf/2205.11490v3)，读pp.1–14正文与附录A–F。HTML对照辅助，代码未执行；FULL不是复现或逐图像数字化。 - **学习与粒度**：§3、式(3)–(8)：翻译交叉熵训练；nCF经浅层编码后以1–4字节卷积融合，重复回原字节长度并加权，不是持久压缩；WSF用词跨度构造块注意力掩码，再给高层完整字节序列。编码器见完整源句，解码器仅见已生成前缀及完整源，不是因果字节流结构。位置/词边界是地址，值仍为字节表征，未提供文档回访、撤销。
- **Canonical problems:** [BIP-0070](DETAILED_INVENTORY.md#BIP-0070), [BIP-0071](DETAILED_INVENTORY.md#BIP-0071), [BIP-0072](DETAILED_INVENTORY.md#BIP-0072), [BIP-0073](DETAILED_INVENTORY.md#BIP-0073).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S01/W0514**, [WORKS](../01_discovery/S01/WORKS.md) line 66: *Local Byte Fusion for Neural Machine Translation*, [2205.11490v3 PDF](https://arxiv.org/pdf/2205.11490v3); [old FULL card](../../flued_multigranularity_survey_20261108/03_reading/B26/W0514.md)
  - Original register aliases / era / family / provenance: W0514; 2022/2023 local byte representations; CATALOG-REUSE
  - Source-scoped evidence/depth: Reused FULL card actually read. >800-byte source/target filtering; seven→English directions; Lao loses to BPE; train/inference cost directions differ.
- **S02/W0514**, [WORKS](../01_discovery/S02/WORKS.md) line 37: Sreedhar et al., **Local Byte Fusion for Neural Machine Translation**, [2205.11490v3](https://arxiv.org/pdf/2205.11490v3)
  - Original register aliases / era / family / provenance: W0514; reused FULL card
  - Source-scoped evidence/depth: R: `OLD/03_reading/B26/W0514.md`, pp.1–14/A–F per card.
- **S04/W0514**, [WORKS](../01_discovery/S04/WORKS.md) line 28: **W0514**, 2022/2023, *Local Byte Fusion for Neural Machine Translation*; [v3](https://arxiv.org/pdf/2205.11490v3) CATALOG reuse; F-card `OLD/03_reading/B26/W0514.md`
  - Original register aliases / era / family / provenance: **W0514**, 2022/2023, *Local Byte Fusion for Neural Machine Translation*; [v3](https://arxiv.org/pdf/2205.11490v3)
  - Source-scoped evidence/depth: CATALOG reuse; F-card `OLD/03_reading/B26/W0514.md` Full source + causal target. n-gram CNN fusion vs word-span block attention; not persistent compression. BPE 68.7M vs one-hot-byte44.1M; 3090 timing directions differ. Seven source languages, Lao exception. No generic tied/untied claim.
- **S05/W0514**, [WORKS](../01_discovery/S05/WORKS.md) line 31: Local Byte Fusion for Neural Machine Translation; [2205.11490v3](https://arxiv.org/pdf/2205.11490v3), Sreedhar et al.
  - Original register aliases / era / family / provenance: W0514
  - Source-scoped evidence/depth: **RC** [B26 card](../../flued_multigranularity_survey_20261108/03_reading/B26/W0514.md). Byte inputs/outputs; convolutional or word-span fusion, output retains byte length. Translation loss, full source visibility, causal target. Moses preprocessing, Lao counterexample and train/inference cost reversal.
- **S06/W0514**, [WORKS](../01_discovery/S06/WORKS.md) line 38: **Local Byte Fusion for Neural Machine Translation**; [2205.11490v3](https://arxiv.org/pdf/2205.11490v3); [card](../../flued_multigranularity_survey_20261108/03_reading/B26/W0514.md)
  - Original register aliases / era / family / provenance: W0514; 2022/2023 local fusion
  - Source-scoped evidence/depth: Subword68.7M vs one-hot byte44.1M; RTX3090,5k training steps5176.8s vs4184.1s but validation inference22.445s vs50.963s. Same epoch reverses train-speed claim; fusion ≠ lasting compression. **RF** §3/App.B Tables7–8.
- **S07/W0514**, [WORKS](../01_discovery/S07/WORKS.md) line 27: **Local Byte Fusion for Neural Machine Translation**; [2205.11490v3](https://arxiv.org/pdf/2205.11490v3), 2023
  - Original register aliases / era / family / provenance: W0514
  - Source-scoped evidence/depth: RF: `03_reading/B26/W0514.md`, entire card.

</details>

<a id="BIW-0049"></a>
## BIW-0049 — Beyond Text Compression: Evaluating Tokenizers Across Scales

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source/version:** Jonas F. Lotz, António V. Lopes, Stephan Peitz, Hendra Setiawan, Leonardo Emili, ACL 2025 proceedings pp. 32155–32173, [official PDF](https://aclanthology.org/2025.acl-long.1546.pdf); aliases S06/W0515, S08/S08-W32. **Reading: FULL:** PDF pp. 1–19, §§1–8 and limitations, Appendix A Tables 7–12/Figure 2; visually checked pp. 3, 6, 17–18 for model/budget/results/table alignment. No missing paper appendix. This is literature reading, not a rerun or code audit.

- **Problem:** large-model tokenizer selection is expensive, and compression can fail as a proxy for task quality. **One-sentence solution:** test six existing tokenizers on matched-backbone small/large decoders and predict multilingual rankings with token-distribution features and supervised pairwise models.
- Models take English pretraining text segmented into PHI-3-MINI, GPT-2, GPT-NeoX, Falcon, tiktoken or Aya 23 subword IDs; there is **no pure-byte model arm** (fallback bytes within a subword tokenizer do not establish one). Hidden positions, outputs and autoregressive cross-entropy targets are tokenizer-specific subwords. Full decoder self-attention and vocabulary softmax perform causal next-token prediction; translation and summarization are supervised fine-tuning with source/target prompts, and evaluation uses generation or multiple-choice scoring. End-of-sequence/partial-prefix details and sampling policy are not stated. Appendix A Table 8 explicitly says **input embedding ↔ output classifier tied**; it does not imply sharing across distinct layers/models. No speculative multi-head sharing.
- **Borrowed methods and roles:** Zipf-style descriptive features (unique token cardinality; log-rank/log-frequency area; slope; deviation from linear fit) and token count evaluate tokenizer/text compatibility, not a learned model representation; features restricted to log(rank)≤6. Logistic regression evaluates held-out-tokenizer pairwise choices; a linear-kernel support-vector machine combines cardinality, power-law deviation and slope, then a separate RBF-kernel SVM with Platt calibration feeds Bradley–Terry ranking with leave-one-language-out validation (§5). This is a tiny, correlated six-tokenizer/four-language evaluation, not proof that Zipf features generalize to all tasks.
- **Carrying card:** [R08/BIW-0049](../03_reading/R08/BIW-0049.md).
- **Canonical problem records:** [BIP-0074](DETAILED_INVENTORY.md#BIP-0074).
- **Units — input / internal / output / supervision (current):** Sixsubwordtokenizers, nopurebytearm / matched-backbonedecoderpositions / nextsubwordortaskgeneration / sameEnglish100BGPT2tokensubsetoneepoch, then supervisedtaskfinetuning; input/outputtied.

### Current substantive interface, technique, evidence and limits

### Problem, method and units

- **Problem:** large-model tokenizer selection is expensive, and compression can fail as a proxy for task quality. **One-sentence solution:** test six existing tokenizers on matched-backbone small/large decoders and predict multilingual rankings with token-distribution features and supervised pairwise models.
- Models take English pretraining text segmented into PHI-3-MINI, GPT-2, GPT-NeoX, Falcon, tiktoken or Aya 23 subword IDs; there is **no pure-byte model arm** (fallback bytes within a subword tokenizer do not establish one). Hidden positions, outputs and autoregressive cross-entropy targets are tokenizer-specific subwords. Full decoder self-attention and vocabulary softmax perform causal next-token prediction; translation and summarization are supervised fine-tuning with source/target prompts, and evaluation uses generation or multiple-choice scoring. End-of-sequence/partial-prefix details and sampling policy are not stated. Appendix A Table 8 explicitly says **input embedding ↔ output classifier tied**; it does not imply sharing across distinct layers/models. No speculative multi-head sharing.
- **Borrowed methods and roles:** Zipf-style descriptive features (unique token cardinality; log-rank/log-frequency area; slope; deviation from linear fit) and token count evaluate tokenizer/text compatibility, not a learned model representation; features restricted to log(rank)≤6. Logistic regression evaluates held-out-tokenizer pairwise choices; a linear-kernel support-vector machine combines cardinality, power-law deviation and slope, then a separate RBF-kernel SVM with Platt calibration feeds Bradley–Terry ranking with leave-one-language-out validation (§5). This is a tiny, correlated six-tokenizer/four-language evaluation, not proof that Zipf features generalize to all tasks.

### Budget and evidence

All arms see one epoch of the same English-centric FineWeb **100B GPT-2-token subset**, rather than 100B tokens under each tokenizer; actual raw bytes, each tokenizer's token exposure and context in original bytes, exact context length and data filtering are not specified in the paper. Fixed 2M arm-specific tokens/batch; source data equality is stronger than equal token exposure, but total token steps and compute can differ. Nominal 350M group actually 337M–566M and nominal 2.7B group 2.6B–3.2B because vocabulary sizes vary 32k–256k, including tied table parameters (Table 1/Appendix A Table 8). For example GPT-2 356M/210 H100 h versus Aya 566M/490 h at small scale, GPT-2 2.7B/1650 h versus Aya 3.2B/2120 h at large scale. Appendix Table 7 gives 5.58 versus 8.17 and 36.62 versus 43.10 labelled TFLOPs; total vs rate/unit interpretation is not explained, so do not convert to training totals. Table 1 reports tiktoken large 2050 h while Table 7 reports 1540 h: unresolved source inconsistency. No multi-seed repeat; §Limitations acknowledges uncertainty. FLOPs, parameter and text controls are not simultaneous.

**BIP-0074:** Table 3, visual PDF p.6, gives cross-scale Kendall τ of **0.33** multiple-choice, **−0.07** X-SUM, **0.87 (p<.05)** multilingual translation; small-model rankings are not generally reliable despite strong translation association. For translation (MetricX lower better), compression ρ=.77, cardinality −.79, AUC .77, power-law deviation .78, slope −.44; these signs reflect the metric direction, not necessarily a universal preference. For X-SUM no intrinsic feature significantly predicts performance. Tiktoken large X-SUM SL-BLEURT 39.0 versus GPT-2 43.0 (Table 4), so 'negligible English effects' has an explicit exception. For translation, Aya 350M-group average MetricX 8.7 vs GPT-2 2.7B-group 9.6 (lower better); model counts and training budgets differ. Paired comparisons: single power-law feature mean held-out F1 .70, three-feature linear SVM .76 (Table 5); leave-one-language-out Kendall τ .73–.87 (Table 6). Translation languages CS, DE, RU, ZH paired with EN; held-out is among those languages, not novel scripts or additional families. Pretraining was English-centric, whereas downstream translation uses supervised bilingual fine-tuning for 3 epochs; 'unseen' is pretraining distribution, not zero-shot no exposure.

Budget for X-SUM fine-tuning is 10 epochs, translation 3 epochs (Tables 9–10). Table 12 measures **model tokens/sec**, batch 1, single H100 on eight WMT21 directions; token/sec across differing units is not original-text bytes/sec or latency per equal document. For EN→ZH at large scale Aya 63.4 versus GPT-2 45.7 tokens/s despite larger vocabulary; therefore do not assert every larger-vocabulary arm is slower. Distinct input/output lengths and tokenizer lengths are unaccounted. Model-based SL-BLEURT/MetricX are evaluation resources, not training teachers. Preserve rank uncertainty, limited samples, unequal parameters and fine-tune exposure in inventory.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0515`.
- **Full-source target / version:** https://aclanthology.org/2025.acl-long.1546.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** English/multilingual subword tokenizers / token states / token LM/task predictions / LM training + intrinsic Zipf-inspired metrics. Not automatically a pure-byte study.
- **Learning and causal baseline:** English/multilingual subword tokenizers / token states / token LM/task predictions / LM training + intrinsic Zipf-inspired metrics. Not automatically a pure-byte study.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0074](DETAILED_INVENTORY.md#BIP-0074).
- **Reading ownership:** [R08](batches/R08.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S06/W0515**, [WORKS](../01_discovery/S06/WORKS.md) line 39: **Beyond Text Compression: Evaluating Tokenizers Across Scales**; [ACL2025](https://aclanthology.org/2025.acl-long.1546/),pp.32155–32173
  - Original register aliases / era / family / provenance: W0515; 2025 tokenizer-budget methodology
  - Source-scoped evidence/depth: Abstract: small models predict larger-model tokenizer differences; compression less predictive than combined metrics in unseen languages; English effects negligible. Exact scales/training exposure/FLOPs and byte baseline unknown. **A**, methodological comparator only.
- **S08/S08-W32**, [WORKS](../01_discovery/S08/WORKS.md) line 63: **Beyond Text Compression: Evaluating Tokenizers Across Scales**, [ACL2025 formal abstract](https://aclanthology.org/2025.acl-long.1546/), pp.32155–32173. **A**, no old FULL card.
  - Original register aliases / era / family / provenance: S08-W32 / **W0515** / catalog reuse
  - Source-scoped evidence/depth: **Beyond Text Compression: Evaluating Tokenizers Across Scales**, [ACL2025 formal abstract](https://aclanthology.org/2025.acl-long.1546/), pp.32155–32173. **A**, no old FULL card. Small-model tokenizer ranking, multilingual differences, Zipf-inspired intrinsic metrics; English effects negligible in reported setting. Does not certify compression as sufficient, nor ranking transfer to all byte architectures.

</details>

<a id="BIW-0050"></a>
## BIW-0050 — Language-Specific Effects of Tokenizer Choice in Multilingual Language Models

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** - **FULL（阅读范围）**：Clara Meister、Gül Sena Altıntaş、Antoine Bosselut；[arXiv v1 HTML](https://arxiv.org/html/2610.12144v1)、[v1 PDF](https://arxiv.org/pdf/2610.12144v1)，2026-10-08。PDF首页核对首作者，HTML抽取漏掉。已读正文及附录A–F，本轮视觉补读PDF pp.18、21、25–27、29、33、35的关键表1/4/5/6/8/10/14/16。阅读不等于独立复现或代码核验。
- **决策/来源**：§2/附录A：54种静态分词器、123个语言模型；主比较1.27B decoder、约9.2B token、31种训练语言，同语料混合与大致同训练步但实际内容字节随分词变化。分词算法/预分词/Unicode NFC、NFD或不规范化、训练语种权重离线决定；运行时不是query驱动回查源，未报告粗细源生命周期。输入子词/字节与隐藏层深度不同，不构成多粒度原文寻址。
- **测量**：§7和附录A.5：BPB分母是原始文本UTF-8字节，不是规范化后解码字节；FLORES平行句再报每句bit，中文/德文/孟加拉平均每句124/159/356字节（附录B），跨语BPB不能当同语义单位。训练打包器丢30.4%–43.5%所抽原文且逐语种变化（A.4），同token/同抽样不等于同实际训练原文。
- **对照与反例**：§4图1：跨54分词器BPB波动与语料份额ρ=-0.52；排除语种惩罚与份额ρ=-0.33、p=.068，未经控制不显著，书写系统和资源份额混杂。§5/附录D：重复数据下反向分配泰米尔BPB +.2674；单遍+.1386，资源相关由-.59转+.34且不显著。附录B：无重复与重复的逐语言排序最低中文ρ=-.11；续训到双倍token的逐语言排序最低芬兰语+.64。不可仅报总体排名稳定。
- **更多界限**：§6/附录E，控制训练字节后压缩率系数仅四种调整之一显著；因共线性13项未识别，个别符号翻转。表16按分词器家族留出，逐语特征预测31语平均BPB成对排序0.890；是基于已训练模型标签的筛选器，不是免训练真实因果保证。附录F：Belebele 27模型0.2259–0.2715、机会0.25而被排除；中文XNLI最高0.374，不能声称31语理解全面有效。
- **FLUED/最近邻**：相比W0518的既有词表稳健性，此项有单设计因子配对与数据重复控制；提醒同token、同原文、同训练算力分开报告，按语种/脚本及原字节首续位评价。不能把词表结果直接外推字节模型。
- **Carrying card:** [old scoped FULL/BIW-0050](../../flued_multigranularity_survey_20261108/03_reading/B22/W0516.md).
- **Canonical problem records:** [BIP-0075](DETAILED_INVENTORY.md#BIP-0075), [BIP-0076](DETAILED_INVENTORY.md#BIP-0076).

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** U tokenizer-specific subwords/bytes and normalization → causal LM positions → symbols → next-unit loss; 54 tokenizers/123models.
- **Learning and causal baseline:** U tokenizer-specific subwords/bytes and normalization → causal LM positions → symbols → next-unit loss; 54 tokenizers/123models.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0516`.
- **Full-source target / version:** https://arxiv.org/pdf/2610.12144v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U tokenizer-specific subwords/bytes and normalization → causal LM positions → symbols → next-unit loss; 54 tokenizers/123models.
- **Learning and causal baseline:** U tokenizer-specific subwords/bytes and normalization → causal LM positions → symbols → next-unit loss; 54 tokenizers/123models.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0516.md). Scope header: - **FULL（阅读范围）**：Clara Meister、Gül Sena Altıntaş、Antoine Bosselut；[arXiv v1 HTML](https://arxiv.org/html/2610.12144v1)、[v1 PDF](https://arxiv.org/pdf/2610.12144v1)，2026-10-08。PDF首页核对首作者，HTML抽取漏掉。已读正文及附录A–F，本轮视觉补读PDF pp.18、21、25–27、29、33、35的关键表1/4/5/6/8/10/14/16。阅读不等于独立复现或代码核验。 - **决策/来源**：§2/附录A：54种静态分词器、123个语言模型；主比较1.27B decoder、约9.2B token、31种训练语言，同语料混合与大致同训练步但实际内容字节随分词变化。分词算法/预分词/Unicode NFC、NFD或不规范化、训练语种权重离线决定；运行时不是query驱动回查源，未报告粗细源生命周期。输入子词/字节与隐藏层深度不同，不构成多粒度原文寻址。
- **Canonical problems:** [BIP-0075](DETAILED_INVENTORY.md#BIP-0075), [BIP-0076](DETAILED_INVENTORY.md#BIP-0076).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S05/W0516**, [WORKS](../01_discovery/S05/WORKS.md) line 32: Language-Specific Effects of Tokenizer Choice in Multilingual Language Models; [2610.12144v1](https://arxiv.org/html/2610.12144v1), Meister, Altıntaş, Bosselut, 2026
  - Original register aliases / era / family / provenance: W0516
  - Source-scoped evidence/depth: **RC** [B22 card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0516.md). 54 tokenizers/123 LMs; byte/subword and normalization variants; causal LM loss. Original-byte BPB denominator, packing losses, per-language behavior, task floors.
- **S08/S08-W33**, [WORKS](../01_discovery/S08/WORKS.md) line 64: **Language-Specific Effects of Tokenizer Choice in Multilingual Language Models**, [2610.12144v1](https://arxiv.org/html/2610.12144v1), 2026-10-08. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0516.md).
  - Original register aliases / era / family / provenance: S08-W33 / **W0516** / catalog reuse
  - Source-scoped evidence/depth: **Language-Specific Effects of Tokenizer Choice in Multilingual Language Models**, [2610.12144v1](https://arxiv.org/html/2610.12144v1), 2026-10-08. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0516.md). ~1.27B, ~9.2B tokens,31languages. Packing discards30.4–43.5% sampled text, language-dependent; repetition changes per-language rankings. Some downstream tasks near chance excluded. Not an equal-original-text causal ranking.

</details>

<a id="BIW-0051"></a>
## BIW-0051 — TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior

- **Reading status:** RF — reused old scoped FULL. Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** - **FULL（阅读范围）**：Gül Sena Altıntaş、Malikeh Ehghaghi、Brian Lester、Fengyuan Liu、Wanru Zhao、Marco Ciccone、Colin Raffel，2026；[arXiv v2全文](https://arxiv.org/html/2512.20757v2)，[正式元数据](https://proceedings.mlr.press/v306/altintas26a.html) PMLR 306:2134–2179。HTML作者栏遗漏Ehghaghi，正式来源补全。已读§1–9及附录A–H；本轮视觉补读[v2 PDF](https://arxiv.org/pdf/2512.20757v2) p.7表1、p.22表5、p.40表24–26。未运行代码。
- **模型和粒度**：§3统一14个现成分词器、约1B非嵌入参数模型，公共词串共享初始化，训练100k步；含ByT5字节、BPE、Unigram等。词表离线学，随题输入变化但无查询后取源、层级原文存储或回退；这不是压缩门学习。不同词表导致嵌入/输出参数与计算不同，不是真总参数或总FLOPs严格相同。§3.3同token预算对应ByT5约100GB、Comma 278GB、Gemma 471GB原文字节。
- **题集**：§4和附录D/E：40个英文简单四选一题，由模型在环筛选使超过70%模型答对，再由母语者翻为中、波斯、意、土；加20道数学和44道STEM题。汉语含简繁、拼音、零宽符、键盘误写；答案经选项似然评估而非长源定位。表面扰动对语义/答案是否完全等价仍取决人工标注，不可当总体知识代表。
- **结果/成本**：§5：全类Unicode样式平均相对准确率跌幅0.53；英文噪声0.15、非英文0.21；汉语无音调拼音平均跌幅0.60（附录E.1）。XGLM NFKC规范化对样式有利却不可逆丢格式，字符精确任务权限改变；BLT/Bolmo在外部模型对照未继承ByT5同等稳健，跨架构语料混杂（G.4）。附录F精确字节概率计算40样本需数小时对普通评估数分钟，且标准题正确率下降。
- **同原文对照**：G.2四种分词器Llama/Gemma/Comma/Qwen按Llama记录重建相同文本流，步数与token量不同，Comma约169.80B对基准约100B；平均相对跌幅两条件均0.24。只能说明这四种设置中的稳健性模式，并非严格同计算或14种均同文；文本流顺序与语言裁剪仍有差异。原文表述同文，不可自动假设每语言截断完全一致。
- **FLUED关联**：与W0516比较，TokSuite测扰动下选择题而非跨语言BPB；建议分开报告原始字节/规范化后文本、任务允许丢格式与否、干净准确率及扰动跌幅，并加源替换必要性实验。本作无法证明来源召回或真实消费。
- **Carrying card:** [old scoped FULL/BIW-0051](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md).
- **Canonical problem records:** [BIP-0077](DETAILED_INVENTORY.md#BIP-0077), [BIP-0078](DETAILED_INVENTORY.md#BIP-0078), [BIP-0079](DETAILED_INVENTORY.md#BIP-0079), [BIP-0080](DETAILED_INVENTORY.md#BIP-0080), [BIP-0285](DETAILED_INVENTORY.md#BIP-0285), [BIP-0286](DETAILED_INVENTORY.md#BIP-0286).

**Central correction P1-03, P1-04, P1-05:** TokSuite2512.20757v2 §3.3: all14 causal Lingua Llama-style arms use untied embeddings, including the ByT5 TOKENIZER arm, not original ByT5. G.2 common-text subset is Llama3.2/Gemma2/Comma/Qwen3 only, excludes bytes and does not control per-language token counts or exact batch order. C.2 PDF p.21 and HTML both say divide CE by log₂(vocabulary size): wording is confirmed wrong for BPB, not merely an HTML artifact. Fixed public commit0db0ba5648a4fa4efae010a94f69fc1042a354aa train.py→LMTransformer.forward→cross_entropy logs natural-log token-average CE; Figure 6 run/log/plot transformation remains unverified. Quarantine Figure 6 as evidence of cross-tokenizer equal BPB/equal training sufficiency. Appendix F ordinary option score is byte-length-normalized log-likelihood; exact-byte extra evaluation is ONLY Gemma2-tokenizer model,40examples/hours with Latin/SentencePiece restrictions, not14-way exact scoring. Other tasks/text-budget results are not automatically invalid.

### Current substantive interface, technique, evidence and limits

- **Units: input / internal / output / supervision:** Fourteen tokenizer-specific interfaces including ByT5 byte tokenizer / common causal Llama-3.2-1B-style states / matching tokenizer vocabulary / next-unit CE; choice scoring and exact-byte evaluation are distinct metrics.
- **Learning and causal baseline:** Causal next-unit models with untied embeddings per paper §3.3. Common nonembedding size does not equal total parameters/FLOPs or same text. C.2 BPB formula remains a targeted open audit question.
Field-centered mechanisms, concrete numerical evidence, comparator budgets and limits from this read old card are carried by the linked canonical BIPs. Old-card project/proposal implications are not imported into the independent field inventory; reading scope remains that of the card, not a new original-paper read.

**Final R2 / claim-rules adoption** ([CLAIM_RULES](../05_review/CLAIM_RULES.md); [FULL_READING_AUDIT_R2](../05_review/FULL_READING_AUDIT_R2.md)): R2 independently visually reconfirms TokSuite v2 C.2/PDFp21 printed CE/log₂(vocabulary size), not a general BPB conversion. Figure6 actual log-to-BPB transformation and paper-run provenance remain UNKNOWN: do not claim it implements the printed formula, is repaired by a reviewer formula, or certifies equal cross-tokenizerBPB/training sufficiency. The prior three-file static inspection at0db0ba5648a4fa4efae010a94f69fc1042a354aa is attributed to DISCOVERY_CORRECTIONS, not repeated byR2. Separate option ranking, Gemma-only exact-byte side evaluation and the four-tokenizer text control are not invalidated. Runtimeplotclosure still needs immutable plotcode/logfields/eventbyte totals/weighting/smoothing/EOS/PAD/prompt/overlap/run mapping.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; old W catalog reuse. Original W: `W0518`.
- **Full-source target / version:** https://arxiv.org/pdf/2512.20757v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Fourteen tokenizer-specific interfaces including ByT5 byte tokenizer / common causal Llama-3.2-1B-style states / matching tokenizer vocabulary / next-unit CE; choice scoring and exact-byte evaluation are distinct metrics.
- **Learning and causal baseline:** Causal next-unit models with untied embeddings per paper §3.3. Common nonembedding size does not equal total parameters/FLOPs or same text. C.2 BPB formula remains a targeted open audit question.
- **Reading status:** RF — reused scoped FULL card. [Existing card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md). Scope header: - **FULL（阅读范围）**：Gül Sena Altıntaş、Malikeh Ehghaghi、Brian Lester、Fengyuan Liu、Wanru Zhao、Marco Ciccone、Colin Raffel，2026；[arXiv v2全文](https://arxiv.org/html/2512.20757v2)，[正式元数据](https://proceedings.mlr.press/v306/altintas26a.html) PMLR 306:2134–2179。HTML作者栏遗漏Ehghaghi，正式来源补全。已读§1–9及附录A–H；本轮视觉补读[v2 PDF](https://arxiv.org/pdf/2512.20757v2) p.7表1、p.22表5、p.40表24–26。未运行代码。 - **模型和粒度**：§3统一14个现成分词器、约1B非嵌入参数模型，公共词串共享初始化，训练100k步；含ByT5字节、BPE、Unigram等。词表离线学，随题输入变化但无查询后取源、层级原文存储或回退；这不是压缩门学习。不同词表导致嵌入/输出参数与计算不同，不是真总参数或总FLOPs严格相同。§3.3同token预算对应ByT5约100GB、Comma 278GB、Gemma 471GB原文字节。
- **Canonical problems:** [BIP-0077](DETAILED_INVENTORY.md#BIP-0077), [BIP-0078](DETAILED_INVENTORY.md#BIP-0078), [BIP-0079](DETAILED_INVENTORY.md#BIP-0079), [BIP-0080](DETAILED_INVENTORY.md#BIP-0080), [BIP-0285](DETAILED_INVENTORY.md#BIP-0285), [BIP-0286](DETAILED_INVENTORY.md#BIP-0286).
- **Reading ownership:** reuse only / narrow recheck, not a new complete read.

### Source identity, original aliases, versions and actual depth

- **S03/W0518**, [WORKS](../01_discovery/S03/WORKS.md) line 28: W0518 · TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior (2026); [2512.20757v2](https://arxiv.org/html/2512.20757v2), [PMLR](https://proceedings.mlr.press/v306/altintas26a.html) C: [B22/W0518](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md)
  - Original register aliases / era / family / provenance: W0518 · TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior (2026); [2512.20757v2](https://arxiv.org/html/2512.20757v2), [PMLR](https://proceedings.mlr.press/v306/altintas26a.html)
  - Source-scoped evidence/depth: C: [B22/W0518](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md)
- **S05/W0518**, [WORKS](../01_discovery/S05/WORKS.md) line 33: TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior; [2512.20757v2](https://arxiv.org/html/2512.20757v2); [ICML 2026 identity](https://proceedings.mlr.press/v306/altintas26a.html), Altıntaş et al.
  - Original register aliases / era / family / provenance: W0518
  - Source-scoped evidence/depth: **RC** [B22 card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md). 14 tokenizers incl. bytes; approximately 1B nonembedding parameters; causal pretraining and answer-option scoring. Noise, Unicode styling and translated five-language questions; only four-tokenizer subset matches reconstructed text streams.
- **S06/W0518**, [WORKS](../01_discovery/S06/WORKS.md) line 40: **TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior**; [2512.20757v2](https://arxiv.org/html/2512.20757v2),[PMLR306](https://proceedings.mlr.press/v306/altintas26a.html); [card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md)
  - Original register aliases / era / family / provenance: W0518; 2025/2026 matched-interface evaluation
  - Source-scoped evidence/depth: Equal token steps expose100–477.22GB raw text and unequal total embedding/head parameters. Four-tokenizer same-text followup has unequal steps/compute; not all14 or byte baseline. Exact byte-probability scoring40 samples takes hours vs minutes. **RF** §3/App.F,G.2.
- **S08/S08-W34**, [WORKS](../01_discovery/S08/WORKS.md) line 65: **TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior**, [PMLR306 formal record](https://proceedings.mlr.press/v306/altintas26a.html), [2512.20757v2](https://arxiv.org/html/2512.20757v2), ICML2026. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md).
  - Original register aliases / era / family / provenance: S08-W34 / **W0518** / catalog reuse
  - Source-scoped evidence/depth: **TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior**, [PMLR306 formal record](https://proceedings.mlr.press/v306/altintas26a.html), [2512.20757v2](https://arxiv.org/html/2512.20757v2), ICML2026. **R** [old card](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md). Same token budget yields100–477.22GB raw text. Four-tokenizer same-text subset excludes ByT5; no claim of14-way same-text evidence. Unicode normalization may erase distinctions. Precise byte-probability evaluation expensive; curated small question bank.

**Audit P1-03/04/05:** source S08-R060 is not a new joint TokSuite/dialect experiment. Its budget component merges with existing exposure findings; the dialect component belongs to BIW-0134. TokSuite uses untied causal embeddings (§3.3), not original ByT5 weights. C.2 BPB prose is a pending formula/implementation clarification, distinct from Appendix F exact option scoring.

</details>

<a id="BIW-0052"></a>
## BIW-0052 — Generating Text with Recurrent Neural Networks

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Ilya Sutskever, James Martens, Geoffrey Hinton**, ICML 2011, [official paper 524](https://icml.cc/2011/papers/524_icmlpaper.pdf), proceedings pp. 1017–1024, PDF pp. 1–8. Aliases S01/H01, S08/S08-W03. **Reading: FULL:** §§1–7, figures 1–3, full Table 1 visually checked at PDF p.6, experiments and sample/negative evidence §§5–6; no appendix in the PDF. No implementation, independent training or reproduction was attempted.

- [BIP-0081](DETAILED_INVENTORY.md#BIP-0081): An additive recurrent transition may not efficiently express the conjunction of the current symbol and prior context. **Solution:** let the current character gate a factorized hidden-to-hidden transition. The full third-order tensor would be expensive; three factor matrices form shared rank-one transition components, combined with character-dependent coefficients (§3, eqs. 3–9; Fig. 3). This is a multiplicative recurrent neural network (MRNN), not LSTM gates or dynamically learned segmentation.
- [BIP-0082](DETAILED_INVENTORY.md#BIP-0082): exploding/vanishing gradients and products of differently scaled parameters make standard gradient optimization difficult. **Solution:** use the Hessian-free (HF) second-order optimizer, Gauss–Newton curvature-vector products and structural damping (§§2, 3.3, 5.2). The architectural and optimization interventions are not separately controlled end-to-end against all alternatives.
- **Carrying card:** [R02/BIW-0052](../03_reading/R02/BIW-0052.md).
- **Canonical problem records:** [BIP-0081](DETAILED_INVENTORY.md#BIP-0081), [BIP-0082](DETAILED_INVENTORY.md#BIP-0082).
- **Units — input / internal / output / supervision (current):** Restricted86character alphabet after cleaning/transliteration/UNK / multiplicative recurrent state / next restricted character / next-characterCE in transformed-characterbits, not originalUTF-8.

### Current substantive interface, technique, evidence and limits

### Atomic problem → solution → technique

- [BIP-0081](DETAILED_INVENTORY.md#BIP-0081): An additive recurrent transition may not efficiently express the conjunction of the current symbol and prior context. **Solution:** let the current character gate a factorized hidden-to-hidden transition. The full third-order tensor would be expensive; three factor matrices form shared rank-one transition components, combined with character-dependent coefficients (§3, eqs. 3–9; Fig. 3). This is a multiplicative recurrent neural network (MRNN), not LSTM gates or dynamically learned segmentation.
- [BIP-0082](DETAILED_INVENTORY.md#BIP-0082): exploding/vanishing gradients and products of differently scaled parameters make standard gradient optimization difficult. **Solution:** use the Hessian-free (HF) second-order optimizer, Gauss–Newton curvature-vector products and structural damping (§§2, 3.3, 5.2). The architectural and optimization interventions are not separately controlled end-to-end against all alternatives.

### Interface, timing, learning and sharing

86-symbol character alphabet, comprising 85 allowed symbols plus unknown; loss is next character cross-entropy in bits per **transformed character**, not full UTF-8 byte likelihood. Wikipedia has XML/markup removed and articles permuted; NYT comprises articles; ML corpus uses extracted plain text, transliterates many special characters/Greek letters and keeps sentences ≥70% alphanumeric (§5.1). Thus arbitrary original strings cannot be recovered from the scored stream. Hidden state is continuous; each softmax prediction conditions on the observed prefix, samples are fed back for causal generation (§4); no explicit EOS or partial UTF-8 policy is specified. One recurrent transition and output are reused across time; the factor basis is shared among character-conditioned transitions, not identical per-character transitions. Character one-hot input and output projection have distinct named matrices in the formulation; no input/output weight tying or multi-head sharing is claimed.

### Evidence and budgets

- In the same-approximately-parameter architectural comparison (§3.2), a 350-unit/350-factor MRNN reaches **1.56 bpc** versus **1.65** for a 500-unit ordinary RNN on ML test data; the latter has slightly more parameters. This is evidence under that training configuration, not a universal mechanism ablation.
- Table 1 (§5, PDF p.6), test bpc ordered **sequence memoizer / PAQ / MRNN**: Wiki **1.66 / 1.51 / 1.60**, NYT **1.49 / 1.38 / 1.48**, ML **1.33 / 1.22 / 1.31**. The MRNN beats the Bayesian nonparametric memoizer, but **dictionary-disabled PAQ remains better on all three**, despite its word-aware mixture components. Train data sizes were matched to roughly 100MB; on larger ~1GB corpora MRNN gives Wiki 1.55 and NYT 1.47, not a matched-data baseline comparison.
- 1500 hidden units and factors, ~4.9M parameters; ~5 days per dataset on 8 GPUs with 4GB each. Each HF step uses 48,000 sequences × 250 characters for gradients, 2,400 sequences for curvature products; first 50 positions supply context, only last 200 are scored. 160 HF steps and up to 150 conjugate-gradient iterations per step, damping μ=0.1 and initial λ=10 (§5.2). Compute equality, joules and runtime of competing implementations are not reported.
- Held-out debagging of seven middle words among 500 11-word examples: MRNN 34%, memoizer 27% (§5.4). Qualitative Wikipedia completion was selected from fewer than ten samples, contains hallucinated/nonsemantic text, and cannot establish reliable reasoning (§6). No author appendix attached. Teacher, verifier, caches and serving throughput unreported/not applicable.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://icml.cc/2011/papers/524_icmlpaper.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **86-symbol prescribed character alphabet** including an unknown symbol / recurrent steps / same characters / next character. ML corpus includes ASCII transliteration and cleaning. Not a 256-byte model.
- **Learning and causal baseline:** Maximum sequence likelihood; factored multiplicative RNN and Hessian-free optimization; strictly left-to-right prediction.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0081](DETAILED_INVENTORY.md#BIP-0081), [BIP-0082](DETAILED_INVENTORY.md#BIP-0082).
- **Reading ownership:** [R02](batches/R02.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/H01**, [WORKS](../01_discovery/S01/WORKS.md) line 27: Sutskever, Martens & Hinton, *Generating Text with Recurrent Neural Networks*, [ICML 2011 proceedings PDF](https://icml.cc/2011/papers/524_icmlpaper.pdf)
  - Original register aliases / era / family / provenance: H01; 2011 recurrent character antecedent; NEW
  - Source-scoped evidence/depth: PARTIAL: §1, §3.1–3.3, §4, §5.1–5.3, §7 inspected. Numerical table extraction incomplete; qualitative samples and all experiments not fully audited.
- **S08/S08-W03**, [WORKS](../01_discovery/S08/WORKS.md) line 34: **Generating Text with Recurrent Neural Networks**, Sutskever, Martens & Hinton; ICML 2011. [Author PDF](https://www.cs.toronto.edu/~jmartens/docs/RNN_Language.pdf), **P** §§1,3.2–5.4,7; Table 1 cells and full experiment audit missing.
  - Original register aliases / era / family / provenance: S08-W03 / S08-N01 / **NEW**
  - Source-scoped evidence/depth: **Generating Text with Recurrent Neural Networks**, Sutskever, Martens & Hinton; ICML 2011. [Author PDF](https://www.cs.toronto.edu/~jmartens/docs/RNN_Language.pdf), **P** §§1,3.2–5.4,7; Table 1 cells and full experiment audit missing. ~4.9M parameters; ~100MB corpora; ~5 days/8 GPUs/run. Matched-data memoizer and dictionary-disabled PAQ; MRNN beats memoizer, loses to PAQ. Data cleaning/UNK means not arbitrary UTF-8.

</details>

<a id="BIW-0053"></a>
## BIW-0053 — Generating Sequences With Recurrent Neural Networks

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Alex Graves**, [arXiv:1308.0850v5, 5 June 2014](https://arxiv.org/pdf/1308.0850v5), first posted 2013. Aliases S01/H02, S03/S03-N07, S08/S08-W04. **Reading: FULL for the assigned text-interface evidence:** all main-paper text §§1–6, equations and Tables 1–4, text samples pp.12–17 including visual inspection of p.16 where CJK font extraction failed and Table 1 on p.8; references pp.41–43. Handwriting-only image plates were not visually audited; their numerical/text methods are read but are not treated as evidence of text-model quality. No supplementary appendix appears in the locked PDF. Reading is not source-code or experiment verification.

- [BIP-0083](DETAILED_INVENTORY.md#BIP-0083): Word softmax has large-vocabulary, sparsity and open-string limitations while short-memory generation can drift. **Solution:** train a stacked LSTM autoregressively on the next symbol, using memory and input-to-layer/output skip connections, then sample each symbol and feed it back (§§2–3). LSTM cell gates preserve state; skip connections shorten optimization paths; truncated backpropagation limits backward history. Word and character heads are alternate experiments, not a jointly trained shared multi-head model.
- §3.1 PTB compares **49 character classes** (4.3M weights) with **10,000 word classes** (~54M), each a one-layer 1000-cell LSTM. PTB vocabulary replaces other words with UNK; sentence-end symbol is included and scored, beginning is a null input. Therefore this character experiment is not necessarily raw original-text byte modeling. §3.2 Wikipedia instead consumes the observed **205 distinct one-byte symbols**, including multibyte-encoded characters; input/output are byte events, hidden state continuous. This is a restricted observed alphabet, not a guarantee of all 256 possible byte values. It does not describe a validator for incomplete UTF-8, EOS policy for Wikipedia generation, or a text-decoder verifier.
- Causality: next-symbol softmax given past. A sampled symbol becomes next input. Wikipedia forward hidden and cell state persist for 100 contiguous 100-byte sequences (up to 10K-byte exposure), but gradients stop every 100 bytes; reset and processing order are specified (§3.2). Recurrent weights are shared over time. Input skip matrices and output matrices are separately denoted (§2 eqs. 1–4); embedding/readout aliasing and any inter-layer parameter tying are **not specified**.
- **Carrying card:** [R02/BIW-0053](../03_reading/R02/BIW-0053.md).
- **Canonical problem records:** [BIP-0083](DETAILED_INVENTORY.md#BIP-0083).
- **Units — input / internal / output / supervision (current):** PTB49characters or10Kwords; Wikipedia205observedbyte-symbols / stackedLSTM state / same next-symbol alphabet / causal next-symbol likelihood; static vs online weight-updated evaluation separate.

### Current substantive interface, technique, evidence and limits

### Problem, idea, techniques and interface

- [BIP-0083](DETAILED_INVENTORY.md#BIP-0083): Word softmax has large-vocabulary, sparsity and open-string limitations while short-memory generation can drift. **Solution:** train a stacked LSTM autoregressively on the next symbol, using memory and input-to-layer/output skip connections, then sample each symbol and feed it back (§§2–3). LSTM cell gates preserve state; skip connections shorten optimization paths; truncated backpropagation limits backward history. Word and character heads are alternate experiments, not a jointly trained shared multi-head model.
- §3.1 PTB compares **49 character classes** (4.3M weights) with **10,000 word classes** (~54M), each a one-layer 1000-cell LSTM. PTB vocabulary replaces other words with UNK; sentence-end symbol is included and scored, beginning is a null input. Therefore this character experiment is not necessarily raw original-text byte modeling. §3.2 Wikipedia instead consumes the observed **205 distinct one-byte symbols**, including multibyte-encoded characters; input/output are byte events, hidden state continuous. This is a restricted observed alphabet, not a guarantee of all 256 possible byte values. It does not describe a validator for incomplete UTF-8, EOS policy for Wikipedia generation, or a text-decoder verifier.
- Causality: next-symbol softmax given past. A sampled symbol becomes next input. Wikipedia forward hidden and cell state persist for 100 contiguous 100-byte sequences (up to 10K-byte exposure), but gradients stop every 100 bytes; reset and processing order are specified (§3.2). Recurrent weights are shared over time. Input skip matrices and output matrices are separately denoted (§2 eqs. 1–4); embedding/readout aliasing and any inter-layer parameter tying are **not specified**.

### Training, comparisons, counterexamples

- PTB: 930K/74K/82K train/validation/test words; SGD 0.0001, momentum .99, derivative clip ±1. Table 1: character no-noise static **1.32 bpc / PPL 167**, fixed noise **1.27 / 140**, adaptive noise **1.26 / 133**; dynamic evaluation with online weight updates gives 1.29, 1.24, 1.24 bpc respectively. Word no-noise static 1.27 / 138; fixed-noise static 1.25 / 126, dynamic 1.23 / 117. The paper's bpc/PPL conversion uses ~5.6 test characters per word; this is not automatically original UTF-8 BPB. The word model is much larger; dynamic and fixed-weight evaluation are materially different budgets.
- PTB prior comparisons (§3.1): Kneser–Ney 5-gram PPL 141, PAQ8 131.1, dynamically evaluated RNN 123.2, RNN/5-gram/cache ensemble 89.4; not a same-parameter/same-compute benchmark.
- Wikipedia §3.2/Table 2: 96M train bytes, 4M validation, seven 700-cell layers ~21.3M weights, 4 epochs SGD .0001 momentum .9, clip ±1. Train **1.42**, validation **1.67 static versus 1.33 dynamic** bpc (on byte events); compare PAQ contest 1.28 including code over the whole contest data, not equal split or a fixed-weight test. No wall time, hardware, total FLOPs, serving latency, state-cache size or text teacher are reported. Wikipedia samples preserve some markup and script-like fragments but become nonsensical beyond short phrases; dynamic weight updates adapt to recent topics.
- §§4–5 concern a different modality: pen-offset Gaussian-mixture plus Bernoulli output and handwriting-conditioned moving soft alignment. Handwriting train/test pooling lacks independent test data; text-based results must not inherit handwriting claims. The moving-window end heuristic and biased sampling apply to handwriting, not to text EOS or text exactness.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1308.0850v5. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Text sequence / recurrent steps / discrete text units / next data point. Text alphabet and character-vs-codepoint implementation **unknown here**; continuous handwriting is a separate experiment, not byte-language evidence.
- **Learning and causal baseline:** LSTM sequence prediction; autoregressive text generation.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0083](DETAILED_INVENTORY.md#BIP-0083).
- **Reading ownership:** [R02](batches/R02.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/H02**, [WORKS](../01_discovery/S01/WORKS.md) line 28: Graves, *Generating Sequences With Recurrent Neural Networks*, [arXiv 1308.0850v5](https://arxiv.org/abs/1308.0850); v5 2014-06-05, first 2013-08-04
  - Original register aliases / era / family / provenance: H02; 2013–2014 recurrent character antecedent; NEW
  - Source-scoped evidence/depth: ABSTRACT only; text methods, corpus normalization, optimizer, comparison and budget not read. Character-route classification is historical; not a byte claim.
- **S03/S03-N07**, [WORKS](../01_discovery/S03/WORKS.md) line 49: S03-N07 · Generating Sequences With Recurrent Neural Networks (2013/2014), Alex Graves; [1308.0850](https://arxiv.org/abs/1308.0850), history v1–v5; this abstract current, v5 PDF queued A
  - Original register aliases / era / family / provenance: S03-N07 · Generating Sequences With Recurrent Neural Networks (2013/2014), Alex Graves; [1308.0850](https://arxiv.org/abs/1308.0850), history v1–v5; this abstract current, v5 PDF queued
  - Source-scoped evidence/depth: A
- **S08/S08-W04**, [WORKS](../01_discovery/S08/WORKS.md) line 35: **Generating Sequences With Recurrent Neural Networks**, Graves; 2013 / [arXiv 1308.0850v5](https://arxiv.org/abs/1308.0850v5), 2014-06-05. **A**, abstract/version history only; [PDF](https://arxiv.org/pdf/1308.0850v5).
  - Original register aliases / era / family / provenance: S08-W04 / S08-N02 / **NEW**
  - Source-scoped evidence/depth: **Generating Sequences With Recurrent Neural Networks**, Graves; 2013 / [arXiv 1308.0850v5](https://arxiv.org/abs/1308.0850v5), 2014-06-05. **A**, abstract/version history only; [PDF](https://arxiv.org/pdf/1308.0850v5). Demonstrates text and handwriting; handwriting realism is not language likelihood or byte evidence. Text metrics, budgets, LSTM controls need paper.

</details>

<a id="BIW-0054"></a>
## BIW-0054 — Character-level Convolutional Networks for Text Classification

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1509.01626v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Prescribed **70-character** one-hot alphabet / temporal CNN features / document class / class label. Out-of-alphabet and blank characters become zero; length 1014. Chinese Sogou is converted to Pinyin using segmentation/transliteration.
- **Learning and causal baseline:** Supervised classification; SGD, momentum, max pooling, dropout; complete document window, **not causal generation**.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0084](DETAILED_INVENTORY.md#BIP-0084), [BIP-0125](DETAILED_INVENTORY.md#BIP-0125).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S01/H03**, [WORKS](../01_discovery/S01/WORKS.md) line 29: Zhang, Zhao & LeCun, *Character-level Convolutional Networks for Text Classification*, [1509.01626v3 HTML](https://arxiv.org/html/1509.01626v3), 2016-04-04 version; NeurIPS 2015 work
  - Original register aliases / era / family / provenance: H03; 2015 CNN character antecedent; NEW
  - Source-scoped evidence/depth: PARTIAL: §2.1–2.4, §3, §4 Sogou setup, §5–6; underlying numerical tables/figures not fully available in extraction. Do not count earlier *Text Understanding from Scratch* separately without entity reconciliation.
- **S08/S08-W05**, [WORKS](../01_discovery/S08/WORKS.md) line 36: **Character-level Convolutional Networks for Text Classification**, Zhang, Zhao & LeCun; NIPS 2015 / [1509.01626v3](https://arxiv.org/abs/1509.01626v3), 2016-04-04. **A**.
  - Original register aliases / era / family / provenance: S08-W05 / S08-N03 / **NEW**
  - Source-scoped evidence/depth: **Character-level Convolutional Networks for Text Classification**, Zhang, Zhao & LeCun; NIPS 2015 / [1509.01626v3](https://arxiv.org/abs/1509.01626v3), 2016-04-04. **A**. Abstract compares bag-of-words/n-grams/TFIDF, word CNNs and RNNs. Classification success does not establish generative LM quality, multilingual byte coverage, or exact string probabilities.

<a id="BIW-0055"></a>
## BIW-0055 — Character-Aware Neural Language Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Yoon Kim, Yacine Jernite, David Sontag, Alexander M. Rush**, AAAI 2016, [arXiv:1508.06615v4, 1 December 2015](https://arxiv.org/pdf/1508.06615v4). Aliases S01/H04, S04/S04-N04, S05/S05-N04, S07/S07-N01, S08/S08-W06. **Reading: FULL:** all main-paper sections and Tables 1–8, Fig. 1 and visual Fig. 2, PDF pp.1–9; no appendix in locked PDF. GPU memory claim and table layout checked visually. Full reading is not experimental reproduction.

- [BIP-0085](DETAILED_INVENTORY.md#BIP-0085): Independent word embeddings fail to share orthographic/morphological information, particularly for rare words. **Solution:** compose each **already segmented input word** from learned character embeddings using width-varying character CNN filters, max-over-time pooling and gated highway layers, then feed the fixed vector to a word-time LSTM to predict the next word (Model, Fig. 1). CNN detects character n-grams; pooling makes a word-sized vector; highway carry/transform gating mixes local features; LSTM carries causal word history. This is character-input/**word-output**, not byte-to-byte autoregression.
- Input unit is corpus-defined indexed characters with begin/end-of-word markers inside pretokenized words. Table 1 lists e.g. PTB 51 characters, other-language data up to 260; character encoding, Unicode normalization and exact inventory not specified. Input word boundaries and preprocessing remain external. Output and supervised target are words in a fixed vocabulary, including UNK; a composition vector can be calculated for unseen spellings but the reported experiment replaces OOV/singletons with UNK and cannot assign distinct output IDs to arbitrary new words. No byte-prefix validity or text-byte verifier exists.
- Next-word cross-entropy is causal over previous whole words, not within-word character generation. For DATA-L a two-level hierarchical word softmax uses ~√|V| random equal-size clusters; DATA-S uses full softmax. Tying axes: character embedding Q and word output P refer to different vocabularies and roles; no claim of input/output tying, shared output heads, encoder/decoder sharing, or runtime tensor alias is made. CNN and LSTM weights are reused across words/time.
- **Carrying card:** [R02/BIW-0055](../03_reading/R02/BIW-0055.md).
- **Canonical problem records:** [BIP-0085](DETAILED_INVENTORY.md#BIP-0085), [BIP-0126](DETAILED_INVENTORY.md#BIP-0126), [BIP-0127](DETAILED_INVENTORY.md#BIP-0127).
- **Units — input / internal / output / supervision (current):** Indexed characters inside presegmented words / CNN-max-highway word vectors and word-timeLSTM / fixed word vocabulary / next-wordCE; characteralphabet exact encoding unreported.

### Current substantive interface, technique, evidence and limits

### Interface and actual method

- [BIP-0085](DETAILED_INVENTORY.md#BIP-0085): Independent word embeddings fail to share orthographic/morphological information, particularly for rare words. **Solution:** compose each **already segmented input word** from learned character embeddings using width-varying character CNN filters, max-over-time pooling and gated highway layers, then feed the fixed vector to a word-time LSTM to predict the next word (Model, Fig. 1). CNN detects character n-grams; pooling makes a word-sized vector; highway carry/transform gating mixes local features; LSTM carries causal word history. This is character-input/**word-output**, not byte-to-byte autoregression.
- Input unit is corpus-defined indexed characters with begin/end-of-word markers inside pretokenized words. Table 1 lists e.g. PTB 51 characters, other-language data up to 260; character encoding, Unicode normalization and exact inventory not specified. Input word boundaries and preprocessing remain external. Output and supervised target are words in a fixed vocabulary, including UNK; a composition vector can be calculated for unseen spellings but the reported experiment replaces OOV/singletons with UNK and cannot assign distinct output IDs to arbitrary new words. No byte-prefix validity or text-byte verifier exists.
- Next-word cross-entropy is causal over previous whole words, not within-word character generation. For DATA-L a two-level hierarchical word softmax uses ~√|V| random equal-size clusters; DATA-S uses full softmax. Tying axes: character embedding Q and word output P refer to different vocabularies and roles; no claim of input/output tying, shared output heads, encoder/decoder sharing, or runtime tensor alias is made. CNN and LSTM weights are reused across words/time.

### Training, results and negative cases

- PTB input training ~1M word tokens / 10k words, large English 20M / 60k; other datasets and inventories Table 1. Architecture small/large: 15-d character embeddings; widths 1–6 / 1–7; two LSTM layers of 300 / 650; highway one/two layers (Table 2). Truncated backpropagation 35 **word steps**, SGD learning rate 1 halved on inadequate validation PPL improvement; batch 20/100, dropout 0.5, gradient norm ≤5; 25 epochs non-Arabic, 30 Arabic (Experimental Setup).
- PTB Table 3: small character 92.3 vs small word 97.6 PPL, each ~5M parameters; large character **78.9 / 19M** vs 85.4 / 20M word baseline and published LSTM-2 **78.4 / 52M**. The ≈60% saving is relative to the latter, not the authors' 20M word model.
- Table 4 DATA-S large models: Czech 371 vs word 493 vs morphology 398; German 239 vs 286 vs 263; Arabic **148 vs 172 vs 148**—a tie with morphology, not a strict win on every cell. DATA-L Table 5 character vs word: German 305 vs 347, English 216 vs 236; published morphological log-bilinear Russian **300** beats char **313**, so broad 'beats every morphology comparator' is false. Actual vocabularies, architectures and sizes differ; PPLs across different languages/tokenizations should not be compared as common byte probabilities.
- [BIP-0126](DETAILED_INVENTORY.md#BIP-0126): Table 7 on small/large PTB: no highway **100.3/84.6**, one highway **92.3/79.7**, two **90.1/78.9**, ordinary one-layer MLP **111.2/92.6**. Authors suggest optimization difficulty rather than prove it; extra CNN layers did not help, combined word+character input gave 81 PPL (Further Observations). Nearest-neighbor/PCA analyses reveal orthographic and some semantic associations, not causal identification of morphemes; filters generally do not align with valid morphemes.
- [BIP-0127](DETAILED_INVENTORY.md#BIP-0127): Fixed word output and local composition cost remain. Large PTB character model trained at **~1500 word tokens/s** vs word model **~3000/s**; precomputing all input-word compositions can match scoring speed at memory expense. All GPUs had 2GB memory; large DATA-L models were not trained due to memory. No GPU model, energy, matched-FLOPs or inference latency provided. No external teacher; no model-code execution.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1508.06615v4. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Characters inside externally delimited words / CNN-highway word vectors and word-time LSTM / fixed-vocabulary words / next-word NLL.
- **Learning and causal baseline:** All spelling characters of an observed input word are visible locally; sentence recurrence is word-causal. Learned character input is not character/byte output.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0085](DETAILED_INVENTORY.md#BIP-0085), [BIP-0126](DETAILED_INVENTORY.md#BIP-0126), [BIP-0127](DETAILED_INVENTORY.md#BIP-0127).
- **Reading ownership:** [R02](batches/R02.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/H04**, [WORKS](../01_discovery/S01/WORKS.md) line 30: Kim, Jernite, Sontag & Rush, *Character-Aware Neural Language Models*, [1508.06615v4 HTML](https://arxiv.org/html/1508.06615v4), 2015-12-01
  - Original register aliases / era / family / provenance: H04; 2015/AAAI 2016 character-to-word antecedent; NEW
  - Source-scoped evidence/depth: PARTIAL: Model subsections including eqs. 3–10; experimental setup, PTB Table 3, highway discussion and runtime paragraph inspected. Tables 4–8 numerical cells not fully checked.
- **S04/S04-N04**, [WORKS](../01_discovery/S04/WORKS.md) line 36: **S04-N04**, 2015/AAAI2016, Kim et al., *Character-Aware Neural Language Models*; [latest listed v4](https://arxiv.org/abs/1508.06615) **New**; A abstract/history; author list cross-checked by primary search metadata
  - Original register aliases / era / family / provenance: **S04-N04**, 2015/AAAI2016, Kim et al., *Character-Aware Neural Language Models*; [latest listed v4](https://arxiv.org/abs/1508.06615)
  - Source-scoped evidence/depth: **New**; A abstract/history; author list cross-checked by primary search metadata **Historical mixed-interface antecedent.** PTB and morphologically rich languages; abstract reports60% fewer parameters. Exact character inventory/tying and fairness details not read. Does not demonstrate pure-byte LM.
- **S05/S05-N04**, [WORKS](../01_discovery/S05/WORKS.md) line 53: Character-Aware Neural Language Models; Kim, Jernite, Sontag, Rush; [1508.06615v4](https://arxiv.org/abs/1508.06615v4), 2015-12-01 / AAAI 2016
  - Original register aliases / era / family / provenance: S05-N04
  - Source-scoped evidence/depth: **A** original abstract/history. Character CNN + highway composition → word-position LSTM → **word predictions**, not byte-to-byte generation. Arabic/Czech/French/German/Spanish/Russian morphology evidence in abstract; character inventory/normalization unresolved.
- **S07/S07-N01**, [WORKS](../01_discovery/S07/WORKS.md) line 40: **Character-Aware Neural Language Models**; [1508.06615v4](https://arxiv.org/abs/1508.06615), 2015 / AAAI 2016 association not separately checked
  - Original register aliases / era / family / provenance: S07-N01; **new**
  - Source-scoped evidence/depth: A current abs with v4 history; no exact character inventory, original tables or total budget inspected.
- **S08/S08-W06**, [WORKS](../01_discovery/S08/WORKS.md) line 37: **Character-Aware Neural Language Models**, Kim, Jernite, Sontag & Rush; 2015 preprint / AAAI 2016. [1508.06615v4 abstract](https://arxiv.org/abs/1508.06615v4), 2015-12-01. **A**.
  - Original register aliases / era / family / provenance: S08-W06 / S08-N04 / **NEW**
  - Source-scoped evidence/depth: **Character-Aware Neural Language Models**, Kim, Jernite, Sontag & Rush; 2015 preprint / AAAI 2016. [1508.06615v4 abstract](https://arxiv.org/abs/1508.06615v4), 2015-12-01. **A**. Abstract: English PTB competitive with 60% fewer parameters; rich-morphology improvements over word/morpheme LSTMs. Closed/open output treatment and cost not inspected.

</details>

<a id="BIW-0056"></a>
## BIW-0056 — Finding Function in Form: Compositional Character Models for Open Vocabulary Word Representation

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/1508.02096. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Characters within given words / composed word vectors, then task positions / LM or POS outputs / task labels. Input is open at word-composition level; **output LM vocabulary and exact character encoding unknown**.
- **Learning and causal baseline:** Bidirectional LSTM composes each word; language-modeling/POS training. Bidirectional spelling encoder is not evidence of noncausal sentence LM; sentence-level permission not inspected.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0128](DETAILED_INVENTORY.md#BIP-0128).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S01/H05**, [WORKS](../01_discovery/S01/WORKS.md) line 31: Ling et al., *Finding Function in Form: Compositional Character Models for Open Vocabulary Word Representation*, [1508.02096v2](https://arxiv.org/abs/1508.02096), 2016-05-23
  - Original register aliases / era / family / provenance: H05; 2015/2016 character-to-word antecedent; NEW
  - Source-scoped evidence/depth: ABSTRACT only. Character antecedent; byte replacement technically conceivable, empirical transfer not established.

<a id="BIW-0057"></a>
## BIW-0057 — Multilingual Language Processing From Bytes

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Dan Gillick, Cliff Brunk, Oriol Vinyals, Amarnag Subramanya**, [arXiv:1512.00103v2, 2 April 2016](https://arxiv.org/pdf/1512.00103v2). Alias S01/H06. **Reading: FULL:** §§1–7, Fig. 1 and caption, Tables 1–4 (including visually verified Table 2–4), Fig. 2 visually, its caption and discussion, pp.1–11 including references. The t-SNE figure was visually inspected but not independently re-analysed; no appendix in the locked PDF. No code or experimental verification.

- [BIP-0129](DETAILED_INVENTORY.md#BIP-0129): language-specific tokenization and processing pipelines hinder a compact cross-script annotator. **Solution:** read UTF-8 byte windows with a shared LSTM and train one model on all languages for each task. Input includes 256 byte values, GO and DROP; windows can split multibyte Unicode characters (§§1, 3.1–3.2). No Unicode normalization policy specified. Representations are continuous LSTM states; output is **span annotations**, not text bytes.
- [BIP-0130](DETAILED_INVENTORY.md#BIP-0130): cross-product classification over all possible start/length/label triples is large and rigid. **Solution:** autoregressively serialize each annotation as separate `start, length, label` events followed by STOP. The same softmax covers all start positions, lengths, labels and STOP; each prediction may choose any event type. Invalid or incomplete spans are rare and ignored, not formally precluded (§3.1). No independent verifier or enforcement is described. Greedy argmax feeds prior outputs back; beam search improved <0.2 absolute (§5).
- [BIP-0131](DETAILED_INVENTORY.md#BIP-0131): local-string memorization and independently segmented windows hurt generalization and cross-boundary spans. **Solution:** randomly replace input bytes with DROP without changing labels and overlap inference windows (§§4–5). Train 60-byte windows at one-byte shifts, ignore training spans not fully contained. At inference use 60-byte windows overlapped by 30 bytes, retain last 30-byte predictions except initial window as described; overlap adds roughly twice the input processing on long texts and does not mathematically guarantee coverage of arbitrarily long spans. Handling of retained crossing spans is not fully specified.
- **Carrying card:** [R02/BIW-0057](../03_reading/R02/BIW-0057.md).
- **Canonical problem records:** [BIP-0129](DETAILED_INVENTORY.md#BIP-0129), [BIP-0130](DETAILED_INVENTORY.md#BIP-0130), [BIP-0131](DETAILED_INVENTORY.md#BIP-0131).
- **Units — input / internal / output / supervision (current):** UTF-8bytes+GO/DROP in60byte windows / same recurrentLSTM parameters in input/output phases / start,length,label events+STOP / annotation conditional likelihood, not next textbyte.

### Current substantive interface, technique, evidence and limits

### Problems, solutions, unit boundaries

- [BIP-0129](DETAILED_INVENTORY.md#BIP-0129): language-specific tokenization and processing pipelines hinder a compact cross-script annotator. **Solution:** read UTF-8 byte windows with a shared LSTM and train one model on all languages for each task. Input includes 256 byte values, GO and DROP; windows can split multibyte Unicode characters (§§1, 3.1–3.2). No Unicode normalization policy specified. Representations are continuous LSTM states; output is **span annotations**, not text bytes.
- [BIP-0130](DETAILED_INVENTORY.md#BIP-0130): cross-product classification over all possible start/length/label triples is large and rigid. **Solution:** autoregressively serialize each annotation as separate `start, length, label` events followed by STOP. The same softmax covers all start positions, lengths, labels and STOP; each prediction may choose any event type. Invalid or incomplete spans are rare and ignored, not formally precluded (§3.1). No independent verifier or enforcement is described. Greedy argmax feeds prior outputs back; beam search improved <0.2 absolute (§5).
- [BIP-0131](DETAILED_INVENTORY.md#BIP-0131): local-string memorization and independently segmented windows hurt generalization and cross-boundary spans. **Solution:** randomly replace input bytes with DROP without changing labels and overlap inference windows (§§4–5). Train 60-byte windows at one-byte shifts, ignore training spans not fully contained. At inference use 60-byte windows overlapped by 30 bytes, retain last 30-byte predictions except initial window as described; overlap adds roughly twice the input processing on long texts and does not mathematically guarantee coverage of arbitrarily long spans. Handling of retained crossing spans is not fully specified.

### Architecture, causal visibility, sharing and optimization

Four 320-wide stacked LSTMs and embeddings, ~900K parameters; **same LSTM recurrent parameter set in encoder/input and decoder/output phases** (§3), shared across languages within each task, with separate POS and NER models. This is phase/temporal and language sharing—not evidence that input byte embedding equals output event projection or that distinct output heads tie. Full 60-byte input is consumed before any output, so annotation is not online causal generation of source text; outputs condition on previous labels, with teacher forcing and conditional maximum likelihood during training. Output order reversed by end position and input forward yielded <1-point gains. Tried attention, converged in fewer steps but no NER improvement (p.3 footnote). SGD batch 128, initial LR .3, single CPU several days; POS and NER dropout and byte-dropout each .2 and .3 respectively. No teacher, FLOPs, benchmark wall-clock per input, cache or GPU training measurement.

### Results, controls and limits

- Supervised data: POS 13 languages, 2.87M original word tokens expanded to 25.3M overlapping training segments; NER 4 languages, 0.88M tokens expanded to 6.0M segments (§6). Overlap segments are **not independent original-text exposure**. Compare same-model multilingual training to separately trained models with same parameters but less per-language training data; extra multilingual data and sharing are confounded.
- Table 1 average POS accuracy: CRF external clusters **96.04**, CRF same labeled data **95.41**, multilingual BTS **95.85**, separate BTS* **95.06**. English BTS 93.87 < separate 94.00 and CRF 94.51; Finnish BTS 95.48 < separate 96.05, despite being above CRF+ 94.34. Gains are not uniform.
- Table 2 exact-span F1 English/German/Spanish/Dutch: BTS **86.50/76.22/82.95/82.84**, BTS* **84.57/72.08/81.83/78.08**. English external-data Passos **90.90**, so no universal state of the art; comparisons mix supervision resources, features and architectures.
- Table 3 vanilla → conventional dropout → plus byte dropout: POS **94.78→95.35→95.85**, NER F1 **74.75→78.76→82.13**. Table 4 depth 1→4 at width 320: NER **76.15→82.13**; width 640 at depth 4 **82.18**. Changed depth, capacity and optimization are confounded. §6.2 notes no clear way to increase recall using a span-probability threshold; visualizations of label clusters do not prove language-invariant representations.
- Authors explicitly say they had **no annotated code-switching test** (p.2 footnote). Compact ~900K parameters and under 10MB vs ~50MB per CRF model include different resources; no general serving latency or code-switch capability has been demonstrated.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1512.00103v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** UTF-8 bytes / LSTM over complete 60-byte segments / start, length, label, STOP symbols / supervised serialized annotation triples, not next text bytes.
- **Learning and causal baseline:** Whole segment is encoded before causal annotation-symbol generation. Teacher-forced triple factorization; byte dropout and overlap alter learning/exposure, not causal text-generation capability.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0129](DETAILED_INVENTORY.md#BIP-0129), [BIP-0130](DETAILED_INVENTORY.md#BIP-0130), [BIP-0131](DETAILED_INVENTORY.md#BIP-0131).
- **Reading ownership:** [R02](batches/R02.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/H06**, [WORKS](../01_discovery/S01/WORKS.md) line 32: Gillick, Brunk, Vinyals & Subramanya, *Multilingual Language Processing From Bytes*, [1512.00103v2 HTML](https://arxiv.org/html/1512.00103v2), 2016-04-02
  - Original register aliases / era / family / provenance: H06; 2015 preprint/2016 byte annotation; NEW
  - Source-scoped evidence/depth: PARTIAL: §1, §3–5, §6.3 and relevant result prose; numerical task tables not independently read. Segment overlap and ignored cross-boundary spans are part of the contract.

</details>

<a id="BIW-0058"></a>
## BIW-0058 — Neural Machine Translation in Linear Time

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Nal Kalchbrenner, Lasse Espeholt, Karen Simonyan, Aäron van den Oord, Alex Graves, Koray Kavukcuoglu**, [arXiv:1610.10099v2, 15 March 2017](https://arxiv.org/pdf/1610.10099v2). Alias S01/H07. **Reading: FULL:** §§1–7, Tables 1–5, Figs. 1–6 and references, PDF pp.1–9; visually checked Tables 2–4 on p.6 and the saliency heatmaps on p.8. No appendix in locked PDF. No code or runtime measurement verified independently.

[BIP-0132](DETAILED_INVENTORY.md#BIP-0132): recurrent seq2seq decoders are serial in training, fixed-vector encoders compress source information, and all-pairs attention incurs length-dependent cost. **Solution:** stack a resolution-preserving dilated convolutional source encoder with a causally masked dilated convolutional target decoder, dynamically unfold until EOS (§§2–4, Figs. 1–3). Dilations expand receptive field quickly; residual blocks ease deep optimization, layer normalization avoids computing statistics across future target positions. Unlike dense attention, each decoder position has finite reachable source/target context, determined by convolution depth and dilation; source encoder is unmasked so can use surrounding source positions. It is not an online source-streaming translation guarantee.
- **Carrying card:** [R02/BIW-0058](../03_reading/R02/BIW-0058.md).
- **Canonical problem records:** [BIP-0132](DETAILED_INVENTORY.md#BIP-0132).
- **Units — input / internal / output / supervision (current):** Hutter90M/5M/5Mbyte splits with205observedsymbols; MT296English/323Germancharacters / dilated convolution states / next benchmark symbol or targetcharacter+EOS / causalLM or conditionaltranslation likelihood.

### Current substantive interface, technique, evidence and limits

### Problem, approach and actual interfaces

[BIP-0132](DETAILED_INVENTORY.md#BIP-0132): recurrent seq2seq decoders are serial in training, fixed-vector encoders compress source information, and all-pairs attention incurs length-dependent cost. **Solution:** stack a resolution-preserving dilated convolutional source encoder with a causally masked dilated convolutional target decoder, dynamically unfold until EOS (§§2–4, Figs. 1–3). Dilations expand receptive field quickly; residual blocks ease deep optimization, layer normalization avoids computing statistics across future target positions. Unlike dense attention, each decoder position has finite reachable source/target context, determined by convolution depth and dilation; source encoder is unmasked so can use surrounding source positions. It is not an online source-streaming translation guarantee.

- Hutter Wiki LM §5 uses 90M/5M/5M **bytes** train/validation/test with 205 observed character/symbol vocabulary; Table 3 explicitly says bits/byte, while the prose calls it bits/character. Given the 205-symbol Hutter byte setup also described in Graves, the byte-level reading is plausible, but this paper itself does not specify its complete encoding/normalization; do not generalize to all 256 bytes. Input and target share the character-symbol alphabet; model state is 315-symbol context of continuous conv features and target is next symbol. The underlying source data contains XML.
- En→De translation §6 instead explicitly uses 296 English and 323 German **characters** with no word/morpheme segmentation, not arbitrary raw bytes; exact encoding, dropped/replaced characters and normalization are unreported. Targets are target characters plus EOS. Causal target prediction conditions on previous target characters and available encoder features; §3.2 pads source representations to ~1.2× input length, and beyond it can continue without source representation, until EOS. Training conditional log likelihood, inference beam 12 by total likelihood, EOS-completed outputs only, no length normalization or source-coverage penalty. No independent verifier.
- Input lookup table and output projection are described separately; no input/output tying, encoder/decoder tying, cross-language embedding tying, or multi-head parameter sharing is specified. Convolution weights share across time/position. No teacher specified.

### Setup and evidence

- LM: 30 residual multiplicative blocks in six cycles of dilation 1,2,4,8,16; masked kernel width 3, hidden width 512, reported receptive field **315**; batches of 500 symbols supply first 100 as context and predict last 400. Adam .0003, weight decay .0001, dropout .1 (§5). Test **1.31 bits/byte** vs recurrent highway 1.32, large layer-normalized HyperLSTM 1.34, Graves stacked LSTM 1.67 (Table 3). These are prior reported results, not necessarily identical training, parameter or compute budgets.
- MT: 30 encoder and 30 decoder ReLU residual blocks, width 800, size-3 kernels; Adam .0003; 2013 validation, 2014/2015 WMT test; sentence pad to next multiple of 50 with extra 20% source padding (§6). **Tables 2 and 4 visually show BLEU 23.75/26.26 and bits/character .521/.532**, respectively, for 2014/2015. **The v2 abstract instead claims 22.85/25.53 and .380/.389**; the paper does not reconcile this internal discrepancy. Use versioned table numbers with the inconsistency disclosed rather than substituting the abstract.
- Table 2 2014 character GNMT 22.62, wordpiece GNMT 24.61, BPE→character attention 21.33; phrase-based 20.7/24.0. Thus character ByteNet is better than the listed character baseline but not wordpiece GNMT on 2014; these are not equal-data/compute claims. Table 5 outputs include reordering and errors. Fig. 6 visualizes gradients aggregated by word; the alignment-like structure is an observational sensitivity map, not direct evidence of an attention alignment mechanism.
- Fixed-depth theoretical time O(c(|S|+|T|)) with c related to receptive-field depth is an operation-complexity statement, not a measured practical latency, a guarantee of arbitrary-long dependencies, or proof of parallel autoregressive target emission. Model total parameters, number of training examples/steps, total FLOPs, hardware and serving wall time are not reported in the paper. No benchmark of caching or modern streaming speed.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1610.10099v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **Character** input/output per abstract / resolution-preserving convolutional sequence / target characters / translation or character LM. Dataset-level byte-vs-codepoint alphabets unknown. The name ByteNet is not unit evidence.
- **Learning and causal baseline:** Dilated 1-D CNN encoder and decoder; translation likelihood/LM. Decoder generates autoregressively; exact masks not inspected; source encoder has source-sequence access.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0132](DETAILED_INVENTORY.md#BIP-0132).
- **Reading ownership:** [R02](batches/R02.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/H07**, [WORKS](../01_discovery/S01/WORKS.md) line 33: Kalchbrenner et al., *Neural Machine Translation in Linear Time* (ByteNet), [1610.10099v2](https://arxiv.org/abs/1610.10099), 2017-03-15
  - Original register aliases / era / family / provenance: H07; 2016/2017 convolutional character antecedent; NEW
  - Source-scoped evidence/depth: ABSTRACT only. Linear-time architecture claim is author-reported; training/inference wall time and budgets unknown.

</details>

<a id="BIW-0059"></a>
## BIW-0059 — Fully Character-Level Neural Machine Translation without Explicit Segmentation

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Jason Lee, Kyunghyun Cho, Thomas Hofmann; [arXiv 1610.03017v3, 13 June 2017](https://arxiv.org/pdf/1610.03017v3). Aliases S01/H08, S02/S02-N01, S05/S05-N05.

**Reading depth: FULL, fresh.** Read PDF pp. 1–11 §§1–8, all Tables 1–8 and Figures 1–2; references pp. 12–13 consulted as needed. The locked PDF has no appendix. Visually checked Tables 5 and 8 and Figure 2 on pp. 8 and 11. The authors link a webpage with supplementary qualitative translations; it is not required for the paper's reported quantitative experiments and was not independently inspected. This is reading, not code or result reproduction.
- **Carrying card:** [R03/BIW-0059](../03_reading/R03/BIW-0059.md).
- **Canonical problem records:** [BIP-0086](DETAILED_INVENTORY.md#BIP-0086), [BIP-0087](DETAILED_INVENTORY.md#BIP-0087), [BIP-0088](DETAILED_INVENTORY.md#BIP-0088).
- **Units — input / internal / output / supervision (current):** Finite300/400sourcecharacteralphabets afterMoses, RussianISO9transliteration / CNNstride5max+highway+BiGRU / targetcharacters / teacher-forcedtranslationNLL; byteencoding not established.

### Current substantive interface, technique, evidence and limits

**Reading depth: FULL, fresh.** Read PDF pp. 1–11 §§1–8, all Tables 1–8 and Figures 1–2; references pp. 12–13 consulted as needed. The locked PDF has no appendix. Visually checked Tables 5 and 8 and Figure 2 on pp. 8 and 11. The authors link a webpage with supplementary qualitative translations; it is not required for the paper's reported quantitative experiments and was not independently inspected. This is reading, not code or result reproduction.

### Units, causality, and preprocessing

Input and target are finite **character alphabets** after Moses tokenization; encoder internal units are continuous, fixed-stride pooled source segments and contextual bidirectional GRU states; output and supervision are target character events (§§4–5). This is a character antecedent, not an established raw UTF-8 byte model; exact Unicode representation, out-of-alphabet/UNK mapping and normalization are not reported. Source alphabets in Tables 1–2 are 300 bilingual and 400 multilingual. The source encoder is bidirectional and can see the whole input sentence; the target decoder is a causal two-layer GRU conditioned on past output characters and attention over all source segments (§2, §4.2). Training minimizes teacher-forced conditional character negative log-likelihood; test uses beam width 20 with length normalization (§5.4). EOS and arbitrary partial-prefix policies are not detailed. One multilingual encoder/decoder is shared among four source languages, with no source language-ID; source/target input embedding tying, decoder input/output tying and any layer-weight tying are not specified.

### Problems and actual techniques

- **BIP-0086:** Character sequences are much longer, multiplying encoder and cross-attention work. **Solution:** character embeddings → one-dimensional CNN with width 1–8 filters → ReLU → nonoverlapping max pool stride 5 → four highway layers → bidirectional GRU, so target attention sees roughly one state per five characters (§4.1, Fig. 1). CNN detects local n-grams, max pooling compresses, highway gates information, and GRU supplies sentence context. Pooling cells are fixed; convolutional receptive fields may overlap their neighboring cells, which is **not** learned variable-length segmentation.
- **BIP-0087:** Explicit subword segmentation can obscure orthographic similarities and struggle on rare forms. **Solution:** train source character composition directly against translation likelihood with character-level target generation. Table 7 provides illustrative robustness and morphology examples, not a corruption benchmark: its long German number is incorrectly translated by both systems.
- **BIP-0088:** Independent language-pair encoders limit cross-lingual sharing. **Solution:** pool four source languages into one character encoder and English decoder, using language-proportional minibatches and no language label (§5.5). Russian Cyrillic is transliterated to Latin via ISO-9 to promote sharing; this is an additional preprocessing intervention, not token-free untouched text. Multilingual data also adds target-English training examples, so improved translation cannot be attributed to shared alphabet alone.

### Results, controls, and limits

WMT15 DE/CS/FI/RU→EN, corpus sizes 4.5M/12.1M/1.9M/2.3M sentence pairs before filters; BPE source training caps at 50 subwords whereas character models cap at 450 characters (§5.2; Table 3). Different retained examples and transliteration make this not an isolated interface-only intervention. BPE uses 20k merge operations for bilingual models; multilingual BPE 50k on per-language roughly equal-character samples. Multilingual char CNN has more filters than bilingual char; the core recurrent sizes are kept fixed, not entire parameter totals.

Table 5 (visually verified), test2 BLEU: DE bilingual BPE→char 25.27 versus char→char 25.83; CS 22.40 versus 22.46; FI 13.98 versus 13.10; RU 22.83 versus 22.73. Multilingual char→char scores DE 25.79, CS 23.24, FI 15.74, RU 23.33 versus multilingual BPE→char 25.23/22.42/14.40/22.81. BPE→BPE is a published external baseline. Human Table 6 reports multilingual improvements predominantly in fluency, with adequacy ties in several conditions; the authors hypothesize English decoder training exposure is responsible but do not isolate it. Qualitative examples and manually mixed code-switching sentences are not population-level robustness evidence.

Single pre-2016 Titan X 12GB, Adam .0001, batch 64, gradient norm 1, validation BLEU stopping (§5.3). Text reports roughly 35% slower training at equal batch; Table 8's FI bilingual rows use **different batch sizes** (BPE 128 vs char 64), 2461.72 vs 2371.93 seconds per 1000 updates and 66.63 vs 71.71 minutes for 3000 sentences online. Equal-batch multilingual timings are 1646.37 vs 2514.23 s/1000 updates. Training FLOPs, total parameters, exact retained data and cache details are not supplied; no teacher is reported.

**Inventory handoff:** [BIP-0086](DETAILED_INVENTORY.md#BIP-0086), [0087](DETAILED_INVENTORY.md#BIP-0087), [0088](DETAILED_INVENTORY.md#BIP-0088): preserve character-vs-byte distinction, filters, transliteration, target-data confounding and qualitative errors.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1610.03017v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Characters → convolution/max-pooled source segments → target characters; translation NLL. Entire source visible; target decoder causal. Not byte-native evidence.
- **Learning and causal baseline:** Characters → convolution/max-pooled source segments → target characters; translation NLL. Entire source visible; target decoder causal. Not byte-native evidence.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0086](DETAILED_INVENTORY.md#BIP-0086), [BIP-0087](DETAILED_INVENTORY.md#BIP-0087), [BIP-0088](DETAILED_INVENTORY.md#BIP-0088).
- **Reading ownership:** [R03](batches/R03.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/H08**, [WORKS](../01_discovery/S01/WORKS.md) line 34: Lee, Cho & Hofmann, *Fully Character-Level Neural Machine Translation without Explicit Segmentation*, [1610.03017v3](https://arxiv.org/abs/1610.03017), 2017-06-13
  - Original register aliases / era / family / provenance: H08; 2016 preprint/2017 character NMT antecedent; NEW
  - Source-scoped evidence/depth: ABSTRACT only. WMT'15 DE/CS/FI/RU→EN, multilingual many-to-one; detailed highway/recurrent wiring, budgets and truncation not read.
- **S02/S02-N01**, [WORKS](../01_discovery/S02/WORKS.md) line 19: Lee, Cho & Hofmann, **Fully Character-Level Neural Machine Translation without Explicit Segmentation** (2016/TACL 2017), [1610.03017v3](https://arxiv.org/html/1610.03017v3), 2017-06-13
  - Original register aliases / era / family / provenance: S02-N01; **fresh**
  - Source-scoped evidence/depth: P: §§3.3–5.5, selected §§6–7 cost/limitations; tables mostly absent in extraction. Source filtering, Moses tokenization and Russian transliteration inspected.
- **S05/S05-N05**, [WORKS](../01_discovery/S05/WORKS.md) line 54: Fully Character-Level Neural Machine Translation without Explicit Segmentation; [1610.03017v3](https://arxiv.org/abs/1610.03017v3), 2017-06-13 / TACL 2017
  - Original register aliases / era / family / provenance: S05-N05
  - Source-scoped evidence/depth: **A** original abstract/history. Character CNN/max-pool source compression, character-to-character translation and multilingual shared encoder. DE/CS/FI/RU→EN; exact Unicode unit and unseen-character policy need full read.

</details>

<a id="BIW-0060"></a>
## BIW-0060 — A Character-Level Decoder without Explicit Segmentation for Neural Machine Translation

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/1603.06147. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **Subword source / encoder states / character target / translation characters**. Character alphabet and exact coding unknown. Not fully token-free and not byte evidence.
- **Learning and causal baseline:** Attention-based encoder–decoder; full source, autoregressive character output.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0089](DETAILED_INVENTORY.md#BIP-0089).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S01/H09**, [WORKS](../01_discovery/S01/WORKS.md) line 35: Chung, Cho & Bengio, *A Character-Level Decoder without Explicit Segmentation for Neural Machine Translation*, [1603.06147v4](https://arxiv.org/abs/1603.06147), 2016-06-21
  - Original register aliases / era / family / provenance: H09; 2016 mixed-interface antecedent; NEW
  - Source-scoped evidence/depth: ABSTRACT only. Four WMT'15 EN→CS/DE/RU/FI pairs; numerical ensemble/single-model budgets and specialized decoder mechanism not read.
- **S03/S03-N08**, [WORKS](../01_discovery/S03/WORKS.md) line 50: S03-N08 · A Character-Level Decoder without Explicit Segmentation for Neural Machine Translation (2016); [1603.06147v4](https://arxiv.org/abs/1603.06147), v4 2016-06-21 A
  - Original register aliases / era / family / provenance: S03-N08 · A Character-Level Decoder without Explicit Segmentation for Neural Machine Translation (2016); [1603.06147v4](https://arxiv.org/abs/1603.06147), v4 2016-06-21
  - Source-scoped evidence/depth: A

<a id="BIW-0061"></a>
## BIW-0061 — Byte-based Neural Machine Translation

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/W17-4123.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes / translation hidden sequence / bytes / parallel translation; exact UTF-8 implementation to recheck in PDF. Character comparator explicitly distinct.
- **Learning and causal baseline:** NMT learning; complete source and generated target prefix are the task-level contract, precise architecture uninspected.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0090](DETAILED_INVENTORY.md#BIP-0090).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S01/H10**, [WORKS](../01_discovery/S01/WORKS.md) line 36: Costa-jussà, Escolano & Fonollosa, *Byte-based Neural Machine Translation*, [SCLeM 2017 W17-4123](https://aclanthology.org/W17-4123/), proceedings pp.154–158
  - Original register aliases / era / family / provenance: H10; 2017 direct byte NMT; NEW
  - Source-scoped evidence/depth: ABSTRACT only; claims similar test quality for most pairs and slightly reduced training time. Pair-level exceptions, equal-budget accounting and baseline wiring unknown.
- **S05/S05-N12**, [WORKS](../01_discovery/S05/WORKS.md) line 61: Byte-based Neural Machine Translation; Costa-jussà, Escolano, Fonollosa; [SCLeM 2017](https://aclanthology.org/W17-4123/), pp.154–158, DOI 10.18653/v1/W17-4123
  - Original register aliases / era / family / provenance: S05-N12
  - Source-scoped evidence/depth: **A** original abstract. Direct byte-versus-character NMT antecedent: similar test quality for most pairs, slightly reduced training time for byte. Not byte-versus-subword evidence; language roster, architecture and actual byte encoding need paper inspection.

<a id="BIW-0062"></a>
## BIW-0062 — Exploring the Limits of Language Modeling

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/1602.02410. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Character-composed and word routes on lm1b / word LM states / word predictions in benchmark comparison / next-word LM. Character encoding and exact variant-specific output layers **not read**.
- **Learning and causal baseline:** Character CNN/LSTM techniques investigated; recurrent language modeling. No pure byte claim.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0133](DETAILED_INVENTORY.md#BIP-0133).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S01/H11**, [WORKS](../01_discovery/S01/WORKS.md) line 37: Jozefowicz et al., *Exploring the Limits of Language Modeling*, [1602.02410v2](https://arxiv.org/abs/1602.02410), 2016-02-11
  - Original register aliases / era / family / provenance: H11; 2016 large word LM with character inputs; NEW
  - Source-scoped evidence/depth: ABSTRACT only. Best single PPL 30.0 and ensemble 23.7 are different systems; do not attribute both to an isolated character-CNN swap or claim output vocabulary removal.

<a id="BIW-0063"></a>
## BIW-0063 — Learning to Generate Reviews and Discovering Sentiment

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Alec Radford, Rafal Jozefowicz, Ilya Sutskever**, [arXiv:1704.01444v2, 6 April 2017](https://arxiv.org/pdf/1704.01444v2). Aliases S01/H12, S06/S06-N07, S08/S08-W07. **Reading: FULL:** all §§1–5, Tables 1–5 and Figs. 1–5, including visual checks of curves, histogram, colored reviews and tables, PDF pp.1–9; no appendix in the locked paper. This is reading, not independent model/code verification.

- [BIP-0091](DETAILED_INVENTORY.md#BIP-0091): supervised sentence/document representations require task labels and may be limited by pretraining domain. **Solution:** train an unsupervised byte-level next-symbol model on in-domain reviews and fit a supervised linear classifier to frozen final cell states. The single-layer 4096-unit multiplicative LSTM (mLSTM) combines input-conditioned multiplicative recurrence with LSTM memory; L1 logistic regression selects downstream features (§§1–4). Input and target are UTF-8 bytes, internal unit is a continuous recurrent hidden/cell state, output is a probability over next bytes; downstream targets are review/sentence labels, not predicted text bytes.
- [BIP-0092](DETAILED_INVENTORY.md#BIP-0092): recurrent optimization and context versus training memory are costly at byte resolution. **Solution:** choose mLSTM via smaller one-pass pilots, weight normalization, Adam, data parallelism and forward-state persistence with truncated gradients. Fig. 1 shows faster convergence than an equal-hidden-size ordinary LSTM under explored settings/time, not a controlled separation of every ingredient.
- [BIP-0093](DETAILED_INVENTORY.md#BIP-0093): generic fixed features can plateau on larger/out-of-domain tasks. **Solution tested:** measure frozen-vector transfer and dataset-size response; no general cure established. Authors propose domain mismatch, late-document bias and linear classifier capacity as hypotheses, not isolated causal findings (§§4.3–4.4).
- [BIP-0094](DETAILED_INVENTORY.md#BIP-0094): an association between a unit and a label need not control generation. **Solution:** select a sentiment-correlated cell and fix it to −1 or +1 during sampling; resulting review samples visibly shift sentiment (Table 5, §4.5). This is an intervention on one model under these prompts and choices, not a proof of universal sentiment disentanglement; negative samples can contain positive sentences.
- **Carrying card:** [R02/BIW-0063](../03_reading/R02/BIW-0063.md).
- **Canonical problem records:** [BIP-0091](DETAILED_INVENTORY.md#BIP-0091), [BIP-0092](DETAILED_INVENTORY.md#BIP-0092), [BIP-0093](DETAILED_INVENTORY.md#BIP-0093), [BIP-0094](DETAILED_INVENTORY.md#BIP-0094).
- **Units — input / internal / output / supervision (current):** UTF-8bytes / 4096unitmLSTM recurrent hidden/cell / next-byte, or separate sentimentclass readout / unsupervisedbyteCE and supervisedL1logistic downstreamlabels.

### Current substantive interface, technique, evidence and limits

### Problem inventory and mechanisms

- [BIP-0091](DETAILED_INVENTORY.md#BIP-0091): supervised sentence/document representations require task labels and may be limited by pretraining domain. **Solution:** train an unsupervised byte-level next-symbol model on in-domain reviews and fit a supervised linear classifier to frozen final cell states. The single-layer 4096-unit multiplicative LSTM (mLSTM) combines input-conditioned multiplicative recurrence with LSTM memory; L1 logistic regression selects downstream features (§§1–4). Input and target are UTF-8 bytes, internal unit is a continuous recurrent hidden/cell state, output is a probability over next bytes; downstream targets are review/sentence labels, not predicted text bytes.
- [BIP-0092](DETAILED_INVENTORY.md#BIP-0092): recurrent optimization and context versus training memory are costly at byte resolution. **Solution:** choose mLSTM via smaller one-pass pilots, weight normalization, Adam, data parallelism and forward-state persistence with truncated gradients. Fig. 1 shows faster convergence than an equal-hidden-size ordinary LSTM under explored settings/time, not a controlled separation of every ingredient.
- [BIP-0093](DETAILED_INVENTORY.md#BIP-0093): generic fixed features can plateau on larger/out-of-domain tasks. **Solution tested:** measure frozen-vector transfer and dataset-size response; no general cure established. Authors propose domain mismatch, late-document bias and linear classifier capacity as hypotheses, not isolated causal findings (§§4.3–4.4).
- [BIP-0094](DETAILED_INVENTORY.md#BIP-0094): an association between a unit and a label need not control generation. **Solution:** select a sentiment-correlated cell and fix it to −1 or +1 during sampling; resulting review samples visibly shift sentiment (Table 5, §4.5). This is an intervention on one model under these prompts and choices, not a proof of universal sentiment disentanglement; negative samples can contain positive sentences.

### Training and scope

Deduplicated Amazon corpus >82M reviews / >38B training bytes, 1000 equal-review shards with one each for validation and test. Single epoch, 1M updates, 128 sequences × 256 bytes per minibatch; states reset per shard and persist across updates while backward gradients are truncated at 256 steps. Adam initial 5e−4 linearly decayed to zero, weight normalization; 4 Pascal Titan X GPUs for ~one month; model parameter count described approximately equal to number of reviews, not an exact count. LM reaches **1.12 bits/byte** (§3); dataset encoding/normalization beyond stated preprocessing and LM evaluation split details are not fully specified. Compute/FLOPs, sampling temperature, KV/state serving budget and input-output embedding tying are not reported. Recurrent weights share over time; no claim of input/output sharing or separate shared heads. Next-byte probabilities are causal and samples are autoregressive; no UTF-8 validity verifier, partial-byte-prefix policy, or explicit general EOS model is specified.

For transfer (§4), replace internal newlines with spaces, strip leading/trailing whitespace, add newline+space as start marker and final space as end marker; encode UTF-8, zero initialize and apply tanh to final cell states. Newline is review delimiter in pretraining. Thus labels supervise the readout even though LM training uses no sentiment labels; these are not zero-label task accuracies.

### Comparators, numerical evidence and negative cases

- Table 1 MR/CR/SUBJ/MPQA accuracy: byte mLSTM **86.9/91.4/94.6/88.5** vs AdaSent **83.1/86.3/95.5/93.3**. CR is Amazon product reviews and authors say it almost certainly overlaps training; this is not independently verified. SST binary **91.8%** vs 30-model supervised ensemble **90.2%**, but fine-grained **52.9%** below published **53.6%**. Label-efficiency Fig. 2 averages 100 runs and uses percentile bands; labels and distribution are not matched to all baseline methods.
- IMDB Table 2: thresholding selected single unit **92.30%**, all 4096 features **92.88%**; semi-supervised virtual adversarial **94.09%**. Fig. 3 visually shows overlap between positive and negative activation histograms; Fig. 4 is six selected high-contrast examples, not an unbiased population assay. Pilot search and feature selection limit interpretation of a single striking cell.
- Yelp binary 598K training examples: full representation **95.22%**, bag-of-words TF-IDF **93.66%**, 500k n-gram linear classifier **95.64%**. Fig. 5 shows a plateau after ~10 labels with only ~1 point improvement across four orders of magnitude. SICK Table 4: Pearson **.792** vs skip-thought **.858** and Tree-LSTM **.868**; Microsoft paraphrase Table 3: **75.0 accuracy/82.8 F1** vs metric-based **77.4/84.1**. Baselines differ in training domains, models and supervision; results do not isolate byte granularity as the cause.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1704.01444v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** UTF-8 bytes / 4096-unit multiplicative LSTM recurrent state / bytes, then separate sentiment class / next-byte likelihood plus downstream readout labels.
- **Learning and causal baseline:** Strict next-byte recurrence; state persists across truncated 256-step training subsequences. Adam and weight normalization train the mLSTM; sentiment logistic regression is a separate supervised readout.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0091](DETAILED_INVENTORY.md#BIP-0091), [BIP-0092](DETAILED_INVENTORY.md#BIP-0092), [BIP-0093](DETAILED_INVENTORY.md#BIP-0093), [BIP-0094](DETAILED_INVENTORY.md#BIP-0094).
- **Reading ownership:** [R02](batches/R02.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/H12**, [WORKS](../01_discovery/S01/WORKS.md) line 38: Radford, Jozefowicz & Sutskever, *Learning to Generate Reviews and Discovering Sentiment*, [1704.01444v2 HTML](https://arxiv.org/html/1704.01444v2), 2017-04-06
  - Original register aliases / era / family / provenance: H12; 2017 direct byte recurrent representation; NEW
  - Source-scoped evidence/depth: PARTIAL: §2–3, §4 opening and §4.1/4.3/4.4/4.5 inspected; full plots/tables not audited. One epoch, four Titan X GPUs, about one month (author report); domain transfer is limited.
- **S06/S06-N07**, [WORKS](../01_discovery/S06/WORKS.md) line 54: **Learning to Generate Reviews and Discovering Sentiment**, Radford/Jozefowicz/Sutskever; [1704.01444v2](https://arxiv.org/html/1704.01444v2),2017-04-06
  - Original register aliases / era / family / provenance: S06-N07; **fresh discovery**
  - Source-scoped evidence/depth: §§2–3:38B training bytes,one pass,~1M updates,4 Pascal Titan X,~one month,1.12BPB; same-state-size LSTM comparator converges slower in stated search. §4.3 document/domain capacity ceiling; no matched-compute subword scaling or serving curve. **P**.
- **S08/S08-W07**, [WORKS](../01_discovery/S08/WORKS.md) line 38: **Learning to Generate Reviews and Discovering Sentiment**, Radford, Jozefowicz & Sutskever; [1704.01444v2](https://arxiv.org/abs/1704.01444v2), 2017-04-06. **A**, abstract; title/authors verified through arXiv Atom.
  - Original register aliases / era / family / provenance: S08-W07 / S08-N05 / **NEW**
  - Source-scoped evidence/depth: **Learning to Generate Reviews and Discovering Sentiment**, Radford, Jozefowicz & Sutskever; [1704.01444v2](https://arxiv.org/abs/1704.01444v2), 2017-04-06. **A**, abstract; title/authors verified through arXiv Atom. Abstract reports SST binary transfer and controllable sentiment generation. Positive evidence for learned byte representations, not general reasoning/long-context capability or matched-budget subword victory.

</details>

<a id="BIW-0064"></a>
## BIW-0064 — Character-Level Language Modeling with Deeper Self-Attention

- **Reading status:** NF — returned new scoped FULL (R09), actual card read for integration; no fresh original-paper credit to inventory owner.
- **Carrying card:** [R09/BIW-0064](../03_reading/R09/BIW-0064.md).
- **Current units: input / internal / output / supervision:** enwik8 raw bytes or text8 cleaned27ASCII symbols / full512symbol causal attention positions / 256class next-byte head / nextunit+intermediate-layer+all-position+future-targetCE; no deployedauxheads.
- **Canonical records:** [BIP-0095](DETAILED_INVENTORY.md#BIP-0095), [BIP-0096](DETAILED_INVENTORY.md#BIP-0096), [BIP-0097](DETAILED_INVENTORY.md#BIP-0097), [BIP-0098](DETAILED_INVENTORY.md#BIP-0098), [BIP-0099](DETAILED_INVENTORY.md#BIP-0099), [BIP-0265](DETAILED_INVENTORY.md#BIP-0265).

### Current card-grounded detail

**Status: FULL**, scoped to [arXiv 1808.04444v2, 10 Dec 2018](https://arxiv.org/pdf/1808.04444v2), pp. 1–7, including Figures 1–7, Tables 1–6 and the qualitative analysis; no carrying appendix in this version. [Local PDF](../03_reading/R09/sources/BIW-0064.pdf) and [UTF-8 extract](../03_reading/R09/sources/BIW-0064.txt). FULL is source reading, not reproduction or proof of runtime behavior. Numerical plots were read via their descriptions/captions, not digitized.

### Problem, solution and units

A deep nonrecurrent model is a counterexample to the premise that recurrent state or learned grouping is necessary for good character/byte likelihood ([BIP-0095](DETAILED_INVENTORY.md#BIP-0095)). The authors use causal full self-attention in a fixed 512-symbol window, 64 layers, two heads, dimension 512, FFN 2048, no cross-batch state; learned separate positional vectors are added at each layer (pp. 1–3). Input and supervision are bytes, internal positions remain one per byte, and the output is a 256-class next-byte softmax. Text8 is a restricted 27-character cleaned, lowercased English alphabet, so byte and character coincide there; enwik8 is 100M raw Wikipedia bytes with 205 observed values, not 205 Unicode characters ([BIP-0265](DETAILED_INVENTORY.md#BIP-0265)). Model vocabulary still contains all 256 classes. Unicode legality, EOS, arbitrary stream stopping and input/output weight tying are unreported.

For x_i the predictor sees x_<i only under the causal mask. Training samples independent random windows; no state crosses batches. At evaluation a new 512-byte context is recomputed for every predicted byte, final layer/final position only. The authors explicitly call this expensive; no measured serving throughput is supplied ([BIP-0099](DETAILED_INVENTORY.md#BIP-0099)).

### Researcher-used optimization techniques

- [BIP-0097](DETAILED_INVENTORY.md#BIP-0097): all final-layer positions receive equal next-symbol supervision, including early positions with short context. This is ordinary causal teacher forcing, not a new inference sampler.
- [BIP-0096](DETAILED_INVENTORY.md#BIP-0096): independent intermediate-layer classifiers provide deep supervision; layer l stops contributing at l/(2n) of training, all auxiliary layer losses gone halfway. This is not external distillation.
- [BIP-0098](DETAILED_INVENTORY.md#BIP-0098): independent classifiers also predict two steps ahead with 0.5 multiplier. Only the immediate next-symbol classifier remains at inference; independent heads are not a normalized joint multi-byte sampler.

Training uses momentum 0.99, learning rate .003, 16 random windows/step, 4M steps, dropout .55 in attention and ReLU. Best checkpoint around 2.5M steps takes 175 hours on a single TPU v2. T64 has 235M training versus 219M inference parameters; T12 44M/41M, 8M steps, dropout .2 (pp. 3–4). Total FLOPs and comparable competitor compute are unreported.

### Experiments and controls

- Text8 test Table 1: T64 1.13 bits/character, T12 1.18, versus 1.27 mLSTM and 1.19 mLSTM with **test-time weight-updating** dynamic evaluation; the Transformer is not dynamically evaluated. On enwik8 Table 3: T64 1.06 bits/byte, T12 1.11, mLSTM 1.24, dynamic-eval mLSTM 1.08. These are not matched-parameter or matched-compute comparisons.
- Text8 dev Table 4, 512 context: baseline 1.062; no multiple positions 2.482; no intermediate-layer losses 1.158; no per-layer positional embeddings 1.069; no multiple targets 1.068; SGD 1.065. Hyperparameters reused except SGD learning-rate search; the differences are not isolated under retuned equal budgets.
- Table 2 text8 test improves 1.34 at context 32 to 1.13 at 512; authors say 1024 did not help. Figure 7's constructed fake name 434 characters away shows a qualitative copying example, not an aggregate exact-copy success rate. Table 6 enwik9 examples at temperature 1 and its 0.85 bpb use a different larger dataset.
- On processed lm1b, Table 5 gives byte T64 1.03 bpb / 40.6 word PPL versus a cited word model 23.7 PPL. Footnote conversion uses 826,189 bytes / 159,658 word events. The corpus was already tokenized with unknown-word substitutions; this is not original-text open-vocabulary evaluation.

### Synthesis implication

Retain full-resolution, uncached dense byte attention as a historical quality baseline and explicitly separate deeper supervision from inference-time computation savings. Recurrent, sparse and hierarchical systems need common raw-text, state/cache, parameter, and compute contracts before causal efficiency claims are compared. Audit R1's rule that test-time weight adaptation differs from recurrent-state reuse applies directly here.


<details>
<summary>Prior catalog provenance and source aliases — historical depth, superseded by current receipt</summary>

- **Entity / provenance:** paper; recovery discovery reused, absent old W catalog. No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1808.04444v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** enwik8 raw bytes OR text8 27 cleaned ASCII symbols / fixed 512-position causal attention / 256-class byte outputs / next-unit plus intermediate-layer, all-position and future-offset CE.
- **Learning and causal baseline:** Fixed-prefix causal LM, no cross-batch recurrent memory or cached evaluation. Auxiliary future targets never become future input; training-only heads are discarded.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0095](DETAILED_INVENTORY.md#BIP-0095), [BIP-0096](DETAILED_INVENTORY.md#BIP-0096), [BIP-0097](DETAILED_INVENTORY.md#BIP-0097), [BIP-0098](DETAILED_INVENTORY.md#BIP-0098), [BIP-0099](DETAILED_INVENTORY.md#BIP-0099), [BIP-0265](DETAILED_INVENTORY.md#BIP-0265).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S01/H13**, [WORKS](../01_discovery/S01/WORKS.md) line 39: Al-Rfou et al., *Character-Level Language Modeling with Deeper Self-Attention*, [1808.04444v2](https://arxiv.org/abs/1808.04444v2), 2018-12-10
  - Original register aliases / era / family / provenance: H13; 2018 preprint/AAAI 2019 dense character/byte benchmarks; RECOVERY-REUSE N06
  - Source-scoped evidence/depth: ABSTRACT only, also present in recovery N06. 64 layers; abstract 1.13/1.06 bits per character are dataset-specific. Context, data cleaning and compute not read.
- **S03/S03-N04**, [WORKS](../01_discovery/S03/WORKS.md) line 39: S03-N04 · Character-Level Language Modeling with Deeper Self-Attention (2018/AAAI 2019); [1808.04444v2](https://arxiv.org/abs/1808.04444v2) recovery BYTE N06; A
  - Original register aliases / era / family / provenance: S03-N04 · Character-Level Language Modeling with Deeper Self-Attention (2018/AAAI 2019); [1808.04444v2](https://arxiv.org/abs/1808.04444v2)
  - Source-scoped evidence/depth: recovery BYTE N06; A
- **S04/S04-N05**, [WORKS](../01_discovery/S04/WORKS.md) line 37: **S04-N05**, 2018/AAAI2019, *Character-Level Language Modeling with Deeper Self-Attention*; [v2](https://arxiv.org/html/1808.04444v2) **Recovery reuse**, old byte-audit N06; P Auxiliary Losses/Training/Evaluation/Ablations
  - Original register aliases / era / family / provenance: **S04-N05**, 2018/AAAI2019, *Character-Level Language Modeling with Deeper Self-Attention*; [v2](https://arxiv.org/html/1808.04444v2)
  - Source-scoped evidence/depth: **Recovery reuse**, old byte-audit N06; P Auxiliary Losses/Training/Evaluation/Ablations Causal fixed512 context;64 layers ~235M, dropout.55,4M planned steps; best ~2.5M/175h TPUv2. Extra heads discarded at inference; training/inference params differ. Tying status not specified here.
- **S06/S06-N01**, [WORKS](../01_discovery/S06/WORKS.md) line 48: **Character-Level Language Modeling with Deeper Self-Attention**, Al-Rfou et al.; [1808.04444v2](https://arxiv.org/html/1808.04444v2),2018-12-10/AAAI2019
  - Original register aliases / era / family / provenance: S06-N01; **recovery reuse**, byte audit N06
  - Source-scoped evidence/depth: Training/evaluation prose:235M training params; inference discards auxiliary heads;64 layers,4M steps,batch16; best checkpoint~175h/single TPUv2. Reprocesses full512 prefix each prediction. Strong historical nonhierarchical result, not efficient modern cached decode. **P**; numerical table/figure rendering missing.
- **S08/S08-W08**, [WORKS](../01_discovery/S08/WORKS.md) line 39: **Character-Level Language Modeling with Deeper Self-Attention**, Al-Rfou et al.; [1808.04444v2 HTML](https://arxiv.org/html/1808.04444v2), 2018-12-10 / AAAI 2019. **P**, model, auxiliary losses, datasets/training/evaluation, ablations and LM1B comparison prose; numerical Tables 1–6 missing. Old recovery N06 already discovered it.
  - Original register aliases / era / family / provenance: S08-W08 / S08-N06 / **RECOVERY REUSE**
  - Source-scoped evidence/depth: **Character-Level Language Modeling with Deeper Self-Attention**, Al-Rfou et al.; [1808.04444v2 HTML](https://arxiv.org/html/1808.04444v2), 2018-12-10 / AAAI 2019. **P**, model, auxiliary losses, datasets/training/evaluation, ablations and LM1B comparison prose; numerical Tables 1–6 missing. Old recovery N06 already discovered it. 64 layers, ~235M parameters, best checkpoint ~175 TPU-v2 hours; 1.13 text8 BPC / 1.06 enwik8 BPB in abstract. Evaluation recomputes whole context; LM1B prose acknowledges word-model gap; do not conflate cleaned text8 and unrestricted Unicode.



</details>

<a id="BIW-0065"></a>
## BIW-0065 — Neural Machine Translation with Byte-Level Subwords

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1909.03341v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** UTF-8→BPE byte n-grams / **subword** positions / byte-subwords→decoded text / translation likelihood. Symbols can split code points; learned vocabulary still exists.
- **Learning and causal baseline:** Transformer with optional depthwise CNN or bidirectional GRU input contextualizer; full source access; causal target decoder, but exact decoder-side contextualizer use/masks not inspected.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0134](DETAILED_INVENTORY.md#BIP-0134), [BIP-0135](DETAILED_INVENTORY.md#BIP-0135).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S01/H14**, [WORKS](../01_discovery/S01/WORKS.md) line 40: Wang, Cho & Gu, *Neural Machine Translation with Byte-Level Subwords*, [1909.03341v2 HTML](https://arxiv.org/html/1909.03341v2), 2019-12-05
  - Original register aliases / era / family / provenance: H14; 2019 preprint/AAAI 2020 byte-derived **subword**; NEW
  - Source-scoped evidence/depth: PARTIAL: Byte Level Text Representation; settings and contextualization/noisy-set/transfer result prose. Tables lack full numeric extraction. Contextualization location must be checked before using a BiGRU causally.

<a id="BIW-0066"></a>
## BIW-0066 — CharacterBERT: Reconciling ELMo and BERT for Word-Level Open-Vocabulary Representations From Characters

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Hicham El Boukkouri, Olivier Ferret, Thomas Lavergne, Hiroshi Noji, Pierre Zweigenbaum, Junichi Tsujii, *CharacterBERT: Reconciling ELMo and BERT for Word-Level Open-Vocabulary Representations From Characters*, [arXiv 2010.10392v3](https://arxiv.org/pdf/2010.10392v3), 31 October 2020, COLING 2020. Alias S01/H15. **Reading: FULL**: PDF pp.1–13, §§1–6, Tables 1–3, Figures 1–8 and Appendix A.1; Figures 5–8 visually inspected, including numerical quartiles in Figure 8. No code execution/weights verified.

This is a word-tokenized English encoder with byte-composed words, **not** a raw-stream byte encoder or byte generator. The preprocessing supplies whole tokens/words (uncased BERT-base regime); each token is UTF-8 encoded, including non-ASCII, and represented with a 263-entry alphabet (256 bytes and seven specials) and maximum local length 50 including specials (§3.1 fn6). Exact truncation semantics and normalization beyond uncased setting are not stated. Character-CNN borrowed from ELMo embeds each byte in 16 dimensions, applies seven 1-D convolution banks of widths 1–7, max-pools and concatenates, uses two highway layers and projects to 768; this creates one word-position embedding for the 12-layer bidirectional BERT encoder (§3.1, Figure 2). Position and segment embeddings remain.
- **Carrying card:** [R01/BIW-0066](../03_reading/R01/BIW-0066.md).
- **Canonical problem records:** [BIP-0136](DETAILED_INVENTORY.md#BIP-0136), [BIP-0137](DETAILED_INVENTORY.md#BIP-0137), [BIP-0138](DETAILED_INVENTORY.md#BIP-0138).
- **Units — input / internal / output / supervision (current):** UTF-8 bytes inside externally segmented word tokens,263entries and localcap50 / CNN-highway word vectors+BERT word positions / task heads or temporary100Kword classifier / whole-wordMLM+NSP; outside100Knevermasked.

### Current substantive interface, technique, evidence and limits

### Interface and roles

This is a word-tokenized English encoder with byte-composed words, **not** a raw-stream byte encoder or byte generator. The preprocessing supplies whole tokens/words (uncased BERT-base regime); each token is UTF-8 encoded, including non-ASCII, and represented with a 263-entry alphabet (256 bytes and seven specials) and maximum local length 50 including specials (§3.1 fn6). Exact truncation semantics and normalization beyond uncased setting are not stated. Character-CNN borrowed from ELMo embeds each byte in 16 dimensions, applies seven 1-D convolution banks of widths 1–7, max-pools and concatenates, uses two highway layers and projects to 768; this creates one word-position embedding for the 12-layer bidirectional BERT encoder (§3.1, Figure 2). Position and segment embeddings remain.

MLM plus next sentence prediction: only top-100k frequent whole words are eligible targets and tokens outside that set are never masked (§3.2, §5.1.1 fn12). Thus input open vocabulary does not mean open-vocabulary MLM head. Outputs at evaluation are entity labels, relation or inference classes, or a continuous sentence similarity score. No autoregressive sampling, EOS or verifier. Baseline BERT shares wordpiece input matrix and MLM output (§5.1.1); CharacterBERT replaces input lookup with CNN and uses a separate temporary 100k-word classifier: no direct input-byte-table ↔ word-softmax tie is documented; cross-task head sharing is not established. The paper attributes slower pretraining partly to loss of the baseline tying optimization, not a controlled tying-only ablation.

### Atomic findings

1. **[BIP-0136](DETAILED_INVENTORY.md#BIP-0136)** — Problem: general-domain WordPiece over-fragments specialized terminology. Solution: retain externally supplied word units but compose each from UTF-8 bytes with an ELMo-style CNN. On 1M medical tokens, ~13% of occurrences are whole in a medical vocabulary yet split by the general vocabulary (Figure 1, §2); this statistic alone does not demonstrate downstream causation. Example `choledocholithiasis`: 2 medical vs 7 general pieces (Table 1).
2. **[BIP-0137](DETAILED_INVENTORY.md#BIP-0137)** — Problem: open inputs and open targets are easily conflated. Solution: fixed 100k frequent word classifier limits the MLM prediction problem while allowing byte-composed input representations. Rare words receive no direct masking targets, although can appear as context. Since word positions are presegmented and 50-local-unit capped, neither unrestricted arbitrary raw text handling nor unlimited rare word recovery follows.
3. **[BIP-0138](DETAILED_INVENTORY.md#BIP-0138)** — Under matched pretraining recipes, medical CharacterBERT's nine-model ensembles improve over medical BERT roughly 1.5 ChemProt F1, 2 DDI F1, 0.5 MEDNLI/i2b2 points (§5.4, Figure 5); visually checked Appendix Figure 8 ensemble medians are 75.40 vs 73.94 ChemProt, 82.74 vs 80.20 DDI, 85.97 vs 85.65 MedNLI accuracy, 89.75 vs 89.51 i2b2 F1. **ClinicalSTS reverses**: 85.62 vs 86.08 Pearson ensemble median, with unstable single-model results and only 600 training examples. Do not generalize the medical gains to every task. Noise Figure 7 evaluates deletion/addition/replacement/swap per token; at 40% test-only noise the paper describes ~5-point advantage (the plot axis is accuracy although §5.5 calls it F1). Gains combine representation, output objective, preprocessing and training costs; not a CNN-only causal ablation.

### Budgets and controls

General data: English Wikipedia 2.14B and OpenWebText 1.28B tokens; medical MIMIC-III 505M and PMC OA abstracts 522M tokens (Table 2). Matched architectures 109.5M BERT vs 104.6M CharacterBERT; 16 V100-SXM2-16GB GPUs, LAMB, 3519 updates batch 8192 length 128 then 782 updates batch 4096 length 512; word vs wordpiece positions do not ensure equal original-text context/exposure (§4.2). BERT pretraining 26.5h, CharacterBERT 55h; average fine-tuning 19% slower but DDI training 14% faster and inference slightly faster in this setup (§5.1). Ten fine-tuning seeds, 15 epochs, single V100, Adam, mean/std and leave-one-out nine-model voting/averaging ensembles (§4.3). No external teacher, equal-FLOP or generation/serving budget established.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2010.10392v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** UTF-8 bytes inside presegmented words, 263 entries and max local length 50 / CNN-highway word positions / fixed top-100K word MLM or task heads / whole-word MLM + NSP, outside-top100K words never masked.
- **Learning and causal baseline:** Bidirectional word-context encoder. Local byte CNN inherits ELMo-style composition; whole-word MLM/NSP supervised by a temporary closed vocabulary. No raw-stream causal decoder.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0136](DETAILED_INVENTORY.md#BIP-0136), [BIP-0137](DETAILED_INVENTORY.md#BIP-0137), [BIP-0138](DETAILED_INVENTORY.md#BIP-0138).
- **Reading ownership:** [R01](batches/R01.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/H15**, [WORKS](../01_discovery/S01/WORKS.md) line 41: El Boukkouri et al., *CharacterBERT: Reconciling ELMo and BERT for Word-Level Open-Vocabulary Representations From Characters*, [2010.10392v3 HTML](https://arxiv.org/html/2010.10392v3), 2020-10-31
  - Original register aliases / era / family / provenance: H15; 2020 word-level encoder with local byte inputs; NEW
  - Source-scoped evidence/depth: PARTIAL: §3, §4.1/4.2 setup, §5.1, §5.4–5.5. Output vocabulary restriction, byte footnote and 26.5h/55h pretrain costs inspected; all task figures/appendix not read.

</details>

<a id="BIW-0067"></a>
## BIW-0067 — CharBERT: Character-aware Pre-trained Language Model

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2020.coling-main.4.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Characters plus BPE/subword inputs / fused token positions / pretrained/task heads / noisy-language-model auxiliary task and base objectives. Exact character encoding and auxiliary target alphabet unknown. Distinct from H15 CharacterBERT.
- **Learning and causal baseline:** Sequential character representations plus heterogeneous interaction with subwords; noisy LM; encoder-style contextual understanding, exact causal masks uninspected.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0100](DETAILED_INVENTORY.md#BIP-0100), [BIP-0101](DETAILED_INVENTORY.md#BIP-0101).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S01/H16**, [WORKS](../01_discovery/S01/WORKS.md) line 42: Ma et al., *CharBERT: Character-aware Pre-trained Language Model*, [COLING 2020.4](https://aclanthology.org/2020.coling-main.4/), proceedings pp.39–50
  - Original register aliases / era / family / provenance: H16; 2020 character–subword hybrid; NEW
  - Source-scoped evidence/depth: ABSTRACT only; QA/sequence labeling/classification and adversarial misspellings. No basis for declaring subword vocabulary eliminated.
- **S07/S07-N05**, [WORKS](../01_discovery/S07/WORKS.md) line 44: **CharBERT: Character-aware Pre-trained Language Model**; [2011.01513v1](https://arxiv.org/abs/2011.01513), 2020
  - Original register aliases / era / family / provenance: S07-N05; **new**
  - Source-scoped evidence/depth: A; exact NLM target, corruption distribution and freezing schedule require full read.

<a id="BIW-0068"></a>
## BIW-0068 — Neural Machine Translation without Embeddings

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Uri Shaham and Omer Levy, *Neural Machine Translation without Embeddings*, NAACL 2021 [official PDF](https://aclanthology.org/2021.naacl-main.17.pdf), proceedings pp.181–186. Aliases S01/H17, S05/S05-N13. **Reading: FULL**: all six pages §§1–8, Figures 1–2 and Tables 1–4; all tables visually checked, including Table 4's reversals. Paper has no appendix. Reading is neither implementation inspection nor reproducibility verification.

UTF-8 source bytes, including whitespace, are encoded as fixed one-hot vectors; encoder output is source-conditioned Transformer states, decoder inputs are target bytes, outputs next-target coordinate logits. Source encoder sees the whole source; decoder is causal/teacher-forced at training, conditional autoregressive translation at inference (§§2–3). No learned token embedding matrix: source and target use the same byte-to-coordinate map, positional embeddings are added, and three independently learned scalar scales cover encoder input, decoder input and decoder output. Paper says hidden width d=512 exceeds 256 byte symbols and Figure 2 defines `softmax_d(Y)`; it does not clearly explain which dimensions map to special tokens or how unused output coordinates are masked/handled, nor exact EOS/invalid UTF-8 policy. Do not silently assume a 256-way normalized byte distribution. The non-embedding Transformer projections remain learned, so this is not a parameter-free representation.
- **Carrying card:** [R01/BIW-0068](../03_reading/R01/BIW-0068.md).
- **Canonical problem records:** [BIP-0102](DETAILED_INVENTORY.md#BIP-0102), [BIP-0139](DETAILED_INVENTORY.md#BIP-0139).
- **Units — input / internal / output / supervision (current):** UTF-8 source/target bytes / Transformer byte positions from fixed one-hot coordinates / softmax_d coordinate logits (special/unused-coordinate treatment unreported) / teacher-forced translationCE+label smoothing.

### Current substantive interface, technique, evidence and limits

### Interface and learning

UTF-8 source bytes, including whitespace, are encoded as fixed one-hot vectors; encoder output is source-conditioned Transformer states, decoder inputs are target bytes, outputs next-target coordinate logits. Source encoder sees the whole source; decoder is causal/teacher-forced at training, conditional autoregressive translation at inference (§§2–3). No learned token embedding matrix: source and target use the same byte-to-coordinate map, positional embeddings are added, and three independently learned scalar scales cover encoder input, decoder input and decoder output. Paper says hidden width d=512 exceeds 256 byte symbols and Figure 2 defines `softmax_d(Y)`; it does not clearly explain which dimensions map to special tokens or how unused output coordinates are masked/handled, nor exact EOS/invalid UTF-8 policy. Do not silently assume a 256-way normalized byte distribution. The non-embedding Transformer projections remain learned, so this is not a parameter-free representation.

Sharing axes: embedding-based baselines explicitly share source/target vocabularies and embeddings (§4); Figure 2 describes a common learned E for input/output. In the embeddingless variant the source input/target input/output coordinate convention is common and fixed, **not** shared trainable matrices; encoder and decoder each have a separate learned input scale, and output has another. Layer, head, or vocabulary-projection tying beyond this is not specified. No teacher, verifier or auxiliary model.

### Atomic findings

1. **[BIP-0102](DETAILED_INVENTORY.md#BIP-0102)** — Problem: learned byte embedding tables are conventional but their benefit is unclear when alphabet size < hidden width. Solution: replace the shared learned input/output lookup and unembedding with fixed one-hot coordinates and predict by direct hidden-coordinate softmax. With ordinary baseline recipe Table 2 finds higher BLEU without embeddings in 19/20 directions, tie ru→en, ~+0.5 average; e.g. en→zh 21.0 vs embedded-byte 20.2; ja→en 12.2 vs 11.4. This apparent gain is confounded: elementwise decoder-input dropout deletes the entire fixed one-hot token but only coordinates of a dense learned embedding (§6).
2. **[BIP-0139](DETAILED_INVENTORY.md#BIP-0139)** — Problem: tokenization changes the semantics of standard dropout. Solution: test explicit decoder-side token dropout p=.2 on embedding-based controls and allow tuning it. Table 3 mean validation gains on xx→en: +0.92 BLEU learned-byte, +0.83 fixed-byte; 7/160 validation conditions decrease. Under tuned token dropout Table 4 reverses headline interpretation: en→xx learned vs fixed bytes nearly equal; xx→en fixed is on average 0.45 BLEU worse, while subword exceeds the next best by 0.76. Example ja→en learned byte 12.3 vs fixed 11.2; ru→en 22.5 vs 22.0. Thus removing learned embedding is not independently demonstrated beneficial after the optimization control. The authors' exposure-bias explanation is a hypothesis.

### Budget, preprocessing, and complete table evidence

IWSLT English↔10 languages, 20 directions; 100k–215k sentence pairs (Table 1). Remove >800-byte pairs and then extreme source/target byte-length ratios to total 5% removal, common data; BPE uses Moses and 10k merges, raw character/byte baselines do not (§4). 6-layer encoder/decoder, 4 heads, d=512, FFN=1024; Adam, 50k updates, 64k raw-byte max batch, top-five checkpoints averaged, label smoothing .1; dropout .2/.3 tuned, SacreBLEU on raw reference. Equal source texts/number of batches per epoch are intended; different sequence length and tokenization do not equalize compute, total parameters, decoding latency or memory. Paper gives no GPU/hardware or exact per-arm parameter/FLOP/serving budgets.

Table 2 columns subword / character / learned-byte / fixed-byte, first 10 en→{zh,es,ar,ru,de,ja,tr,vi,fa,he}: 19.9/20.8/20.2/21.0; 36.8/36.3/36.3/36.8; 12.5/12.5/12.3/12.9; 18.1/17.6/17.4/18.2; 29.4/28.6/28.7/29.1; 12.0/12.5/12.5/13.1; 13.6/13.7/13.8/14.1; 29.7/28.2/28.0/28.7; 11.5/11.7/12.0/12.1; 26.1/26.9/26.4/26.7. Reverse directions are in Table 2; the subword system leads or ties the best alternative in all ten, and the fixed-byte column does not establish a cross-direction advantage. Table 4 has complete post-control direction rows, not only averages; its outcomes are independently inspectable via the fixed source.

### All 20 directions, before and after token-dropout selection

The four numbers in each cell are **subword / character / learned-byte / fixed-byte** SacreBLEU. “Before” is Table 2's original setup; “after” is Table 4 where decoder token dropout is available as a validation-selected hyperparameter. These are test scores, not paired uncertainty estimates; the change is not an isolated intervention on a single fixed model.

| Direction | Before | After |
|---|---|---|
| en→zh | 19.9 / 20.8 / 20.2 / 21.0 | 20.3 / 21.2 / 20.8 / 21.0 |
| en→es | 36.8 / 36.3 / 36.3 / 36.8 | 36.7 / 36.8 / 36.8 / 36.8 |
| en→ar | 12.5 / 12.5 / 12.3 / 12.9 | 12.7 / 13.1 / 12.7 / 12.9 |
| en→ru | 18.1 / 17.6 / 17.4 / 18.2 | 18.5 / 18.2 / 17.7 / 18.2 |
| en→de | 29.4 / 28.6 / 28.7 / 29.1 | 29.8 / 29.3 / 29.2 / 29.1 |
| en→ja | 12.0 / 12.5 / 12.5 / 13.1 | 12.4 / 13.1 / 12.5 / 13.1 |
| en→tr | 13.6 / 13.7 / 13.8 / 14.1 | 13.9 / 14.3 / 14.4 / 14.1 |
| en→vi | 29.7 / 28.2 / 28.0 / 28.7 | 30.0 / 29.1 / 28.9 / 28.7 |
| en→fa | 11.5 / 11.7 / 12.0 / 12.1 | 11.5 / 12.2 / 12.1 / 12.1 |
| en→he | 26.1 / 26.9 / 26.4 / 26.7 | 26.8 / 27.1 / 27.1 / 26.7 |
| zh→en | 16.8 / 16.6 / 15.6 / 16.1 | 17.3 / 17.2 / 16.3 / 16.1 |
| es→en | 39.6 / 38.5 / 38.4 / 38.8 | 40.0 / 39.1 / 39.1 / 38.8 |
| ar→en | 31.5 / 30.2 / 30.3 / 30.8 | 32.0 / 31.1 / 31.2 / 30.8 |
| ru→en | 22.7 / 21.9 / 22.0 / 22.0 | 22.9 / 22.4 / 22.5 / 22.0 |
| de→en | 35.4 / 34.0 / 34.1 / 34.5 | 35.6 / 34.9 / 35.0 / 34.5 |
| ja→en | 13.1 / 12.6 / 11.4 / 12.2 | 13.5 / 12.8 / 12.3 / 11.2 |
| tr→en | 23.3 / 22.5 / 22.3 / 23.3 | 24.3 / 23.3 / 23.7 / 23.3 |
| vi→en | 26.8 / 25.0 / 24.7 / 25.3 | 27.4 / 25.9 / 25.9 / 25.3 |
| fa→en | 23.5 / 22.4 / 22.1 / 22.6 | 24.5 / 23.2 / 23.3 / 22.6 |
| he→en | 37.8 / 36.9 / 37.0 / 37.4 | 38.2 / 37.8 / 37.4 / 37.4 |


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2021.naacl-main.17.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** UTF-8 bytes / byte-position Transformer / byte logits via fixed output coordinates / translation. Fixed one-hot input/output maps, three learned scaling scalars; Transformer projections remain learned.
- **Learning and causal baseline:** Translation cross entropy, label smoothing, Adam; decoder token dropout is crucial; complete source encoder, causal target prefix.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0102](DETAILED_INVENTORY.md#BIP-0102), [BIP-0139](DETAILED_INVENTORY.md#BIP-0139).
- **Reading ownership:** [R01](batches/R01.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S01/H17**, [WORKS](../01_discovery/S01/WORKS.md) line 43: Shaham & Levy, *Neural Machine Translation without Embeddings*, [NAACL 2021.17 PDF](https://aclanthology.org/2021.naacl-main.17.pdf), pp.181–186; arXiv 2008.09396 alias
  - Original register aliases / era / family / provenance: H17; 2020 preprint/NAACL 2021 embedding-free byte NMT; NEW
  - Source-scoped evidence/depth: PARTIAL: §2–6 and conclusion inspected, Tables 1–4 numerical cells not fully available; no FULL claim. Six encoder/six decoder layers, d=512, 50k steps, 64k-byte batch cap, >800-byte filtering plus ratio filtering to 5%.
- **S05/S05-N13**, [WORKS](../01_discovery/S05/WORKS.md) line 62: Neural Machine Translation without Embeddings; Uri Shaham, Omer Levy; [NAACL 2021](https://aclanthology.org/2021.naacl-main.17/)
  - Original register aliases / era / family / provenance: S05-N13
  - Source-scoped evidence/depth: **A** original abstract. UTF-8 one-hot byte representations, byte-to-byte EN→10-language translation; decoder-input dropout becomes token dropout. Comparable/rivaling character and subword quality is reported, but data, normalization and actual cost need full read.

</details>

<a id="BIW-0069"></a>
## BIW-0069 — MoCE: Adaptive Mixture of Contextualization Experts for Byte-based Neural Machine Translation

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/2411.01474. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Unicode bytes / contextualized byte sequence / translation output (exact decoder units to confirm) / translation. No evidence here for persistent sequence compression.
- **Learning and causal baseline:** Adaptive selection and mixing of attention heads as contextualization experts; task training. Source contextualization can use known source; precise routing and masks unknown.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0140](DETAILED_INVENTORY.md#BIP-0140).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S01/H18**, [WORKS](../01_discovery/S01/WORKS.md) line 44: Huang et al., *MoCE: Adaptive Mixture of Contextualization Experts for Byte-based Neural Machine Translation*, [2411.01474v2](https://arxiv.org/abs/2411.01474), 2025-02-07
  - Original register aliases / era / family / provenance: H18; 2024/2025 adaptive local byte NMT; NEW
  - Source-scoped evidence/depth: ABSTRACT only. TED-59 fewer-parameter advantage is author summary, no matched FLOPs/wall-time or per-language rows read.

<a id="BIW-0070"></a>
## BIW-0070 — Revisiting Character-Based Neural Machine Translation with Capacity and Compression

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/1808.09943. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Character / deep seq2seq, optionally skipped/compressed source time / character target / translation. Exact character encoding unknown.
- **Learning and causal baseline:** Depth and conditional computation over time; task-level full source and causal target. Skip gradient estimator not inspected.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0141](DETAILED_INVENTORY.md#BIP-0141).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S01/H19**, [WORKS](../01_discovery/S01/WORKS.md) line 45: Cherry et al., *Revisiting Character-Based Neural Machine Translation with Capacity and Compression*, [1808.09943v1](https://arxiv.org/abs/1808.09943), 2018-08-29
  - Original register aliases / era / family / provenance: H19; 2018 character capacity/compression antecedent; NEW
  - Source-scoped evidence/depth: ABSTRACT only. Deep character baseline reportedly beats identical word-fragment architecture; compression alternatives trade quality for time. Detailed experiment/budget reading is genuinely missing.

<a id="BIW-0071"></a>
## BIW-0071 — Bridging the Gap for Tokenizer-Free Language Models

- **Reading status:** NF — returned new scoped FULL (R09), actual card read for integration; no fresh original-paper credit to inventory owner.
- **Carrying card:** [R09/BIW-0071](../03_reading/R09/BIW-0071.md).
- **Current units: input / internal / output / supervision:** UTF-8byte stream of pretokenized/shuffled lm1b withUNKsubstitutions / full512byte Transformer positions / 256next-byte classes / causal byteCE; convertedwordPPL uses sameprocessedcorpus counts.
- **Canonical records:** [BIP-0142](DETAILED_INVENTORY.md#BIP-0142), [BIP-0143](DETAILED_INVENTORY.md#BIP-0143).

### Current card-grounded detail

**Status: FULL**, [arXiv 1908.10322v1, 27 Aug 2019](https://arxiv.org/pdf/1908.10322v1), §§1–6, Tables 1–3 and Figure 1; no substantive appendix in this version. [PDF](../03_reading/R09/sources/BIW-0071.pdf), [extract](../03_reading/R09/sources/BIW-0071.txt). Figure 1 curves are interpreted from the authors' text and caption, not independently digitized.

### Problem, solution, mechanism

[BIP-0142](DETAILED_INVENTORY.md#BIP-0142): the apparent large-data word/character performance gap need not imply tokenization is intrinsically required. Their proposed remedy is a larger *plain* 40-layer causal Transformer, not pooling, learned segmentation, external boundary teacher or a new objective. UTF-8 byte input and next-byte supervision use one position per byte internally and a 256-way next-byte output (§2). A 512-byte window is sampled across sentence boundaries; 16 heads, d=1024, FFN=8192, ~836M total parameters including ~66K byte embeddings. The attention mask ensures a representation after byte i predicts i+1, not future bytes; no recurrence is used. Whether the input/output matrices are tied, EOS/invalid UTF-8 policy and generation/cache implementation are unreported.

Training uses Adam initial 1e-4, geometric decay .99 each 10k steps, 2M steps, batch 1024, dropout .3 (§2.1). This is 2M × 1024 × 512 ≈1.05 trillion sampled byte positions, **not** unique corpus bytes; training corpus is 4,132,763,660 bytes. Accelerator model, wall time and total training FLOPs are unreported. No claim of matched wall-clock/compute against word baselines follows.

### Corpus, probability object and controls

The lm1b benchmark is a pretokenized, sentence-shuffled word corpus with rare words replaced by UNK (§3.1). No additional tokenizer is applied to its byte stream, but the *underlying data are not raw, untouched original text*. Spaces/newlines and literal UNK text remain observable. Table 1 counts 798,947,561 training word events, 4,132,763,660 bytes; test 159,658 word events including EOS and 826,189 bytes including newlines. 95% of training sentences are shorter than 256 bytes and 99.78% below 512: it is not a strong long-document context test.

[BIP-0143](DETAILED_INVENTORY.md#BIP-0143): for the **same scored processed corpus and matching event counts**, convert the native byte-chain score by PPL_word = 2^(BPB × 826189/159658). This merely re-expresses that path's total log likelihood per word event; it does not equate a subword canonical-path probability with an arbitrary marginalized string probability, nor repair incompatible EOS/newline accounting. The paper's notation that information is segmentation-independent is conditional on a common probability event, not a theorem that separately trained models assign it equal mass.

Scoring from scratch at stride 1 maximizes available 512-byte context and is used for final test. For development, stride 256 scores the second half of each overlapping window in parallel, with contexts varying by position: dev 0.874055 BPB at stride 1 versus 0.87413 at 256 (§2.2). This is scoring acceleration, not cached sequential generation throughput.

### Results and negative evidence

Table 2 reports this ~0.8B byte model at 0.874 BPB / 23.0 word PPL, versus previous 0.2B byte T64 1.033 / 40.6; cited word or wordpiece systems range 21.8–28.0, including Transformer-XL word model 0.8B/21.8, a 1.0B word model at 23.0 and a 4.9B wordpiece model at 24.0. The [versioned HTML Table 2](https://arxiv.org/html/1908.10322v1) was consulted because the PDF text extraction interleaves the rows. These are literature comparisons, not controlled architecture/compute experiments. Test PPL equality at 23.0 does not prove equal real-world tokenizer-free deployment costs.

§5 probes isolated words followed by a space, extracting causal feed-forward activations at that space and cosine/Spearman similarity. Table 3 reports best layer versus Swivel: MEN .35 vs .76, MTurk .32 vs .72, rare words .46 vs .48, SimLex .31 vs .40. Swivel has a different corpus, vocabulary/OOV treatment and objective. Figure 1's first 10 layers generally improve, with later plateaus or exceptions. These probes do not establish a general downstream advantage.

### Implication

Plain full-resolution byte scaling is a serious nonhierarchical comparator. Measure tokenized preprocessing, original text and scored-event alignment separately from inference interface, model size, cache and compute; omit all unsupported claims about equal cost or universal multilingual gains.


<details>
<summary>Prior catalog provenance and source aliases — historical depth, superseded by current receipt</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1908.10322v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Raw **UTF-8 bytes** / 512-position causal Transformer / 256 byte values / next byte. Dataset is pretokenized lm1b with rare words already replaced by UNK; model is not given separate boundary labels.
- **Learning and causal baseline:** 40-layer, 836M Transformer; causal attention, Adam; random 512-byte training windows, 2M steps; test stride 1.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0142](DETAILED_INVENTORY.md#BIP-0142), [BIP-0143](DETAILED_INVENTORY.md#BIP-0143).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S01/H20**, [WORKS](../01_discovery/S01/WORKS.md) line 46: Choe et al., *Bridging the Gap for Tokenizer-Free Language Models*, [1908.10322v1 HTML](https://arxiv.org/html/1908.10322v1), 2019-08-27
  - Original register aliases / era / family / provenance: H20; 2019 dense byte LM; NEW
  - Source-scoped evidence/depth: PARTIAL: §2–4 inspected; §5 probes and complete numerical tables not audited. Converted word PPL 23.0 on this corpus, not an equal-compute or raw-web universal result.



</details>

<a id="BIW-0072"></a>
## BIW-0072 — Hierarchical Transformers Are More Efficient Language Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Piotr Nawrot, Szymon Tworkowski, Michał Tyrolski, Łukasz Kaiser, Yuhuai Wu, Christian Szegedy, Henryk Michalewski; [arXiv 2110.13711v2, 16 April 2022](https://arxiv.org/pdf/2110.13711v2). Aliases S02/S02-N02, S03/S03-N09.

**Reading depth: FULL, fresh.** Read PDF pp. 1–8 §§1–6, Algorithm 1, Figures 1–7 and Tables 1–8; Appendices A–D, pp. 11–13, including proof-like causality/expressivity arguments and hardware/hyperparameters. Tables 4–8 visually checked on p. 7. Figures 1, 6, 7 read at the paper's plotted trend/caption level, not independently digitized. No implementation or numerical result was reproduced.
- **Carrying card:** [R03/BIW-0072](../03_reading/R03/BIW-0072.md).
- **Canonical problem records:** [BIP-0103](DETAILED_INVENTORY.md#BIP-0103), [BIP-0104](DETAILED_INVENTORY.md#BIP-0104).
- **Units — input / internal / output / supervision (current):** enwik8rawbytes / fixedkshortened states+fine-resolutionresidual / next-byte (authorBPC label) / causal nextsymbol likelihood; additionalk−1shiftappliesQ/K/V.

### Current substantive interface, technique, evidence and limits

**Reading depth: FULL, fresh.** Read PDF pp. 1–8 §§1–6, Algorithm 1, Figures 1–7 and Tables 1–8; Appendices A–D, pp. 11–13, including proof-like causality/expressivity arguments and hardware/hyperparameters. Tables 4–8 visually checked on p. 7. Figures 1, 6, 7 read at the paper's plotted trend/caption level, not independently digitized. No implementation or numerical result was reproduced.

### Units, probability, and architecture

The enwik8 experiment receives the first 100M **raw English Wikipedia bytes**, split 90M/5M/5M; the paper calls its next-byte score bits per character. It does not establish Unicode character or grapheme modeling. Full-resolution embedded byte symbols are reduced by fixed factor k to hidden-vector groups and later upsampled; supervision and output are categorical next-symbol autoregressive likelihood (§§2–3.3). There are also image experiments; those are not language results. No EOS or arbitrary partial-group prompt policy is specified. One input/output embedding tying axis, cross-depth parameter sharing, and output-head tying are not stated in the paper; do not infer any from Transformer-XL.

**Problem:** full-resolution Transformer layers spend expensive attention and feed-forward compute on every position. **One-sentence solution:** interleave full-resolution causal layers with shifted shortening, deep group-resolution layers and an upsampling/residual path to restore per-symbol output. Actual techniques: average/learned linear/attention pooling; Transformer-XL relative causal attention or locality-sensitive hashing; repeat, linear or attention-based upsampling; full-resolution skip/residual connections; optional randomized shortening factor (§2, Algorithm 1). Attention pooling carries both pooled queries and full-resolution keys/values, so the additional k−1 right shift must apply to the entire source used to construct Q, K **and** V, not just Q. This is the causality condition described in §2.2 and Appendix A; source code was not audited to certify its enforcement.

A normal one-symbol next-token shift precedes full-resolution processing; another k−1 right shift before each shortening ensures no group representation used for prediction sees a target inside its group (Fig. 4, Appendix A.2). The fine-scale residual is separately causal, so it can carry earlier symbols within a group. Without fine-resolution Transformer layers the shortened branch cannot carry current-group history, but the shifted-input residual can convey the immediately previous symbol; Appendix A.1 demonstrates a more specific copying limitation. At least one fine layer enables within-group contextual dependence in that construction; this is not a guarantee of learned accuracy for arbitrary tasks. The learned projections are not a learned variable boundary.

### Results, comparison and qualifications

- Table 1/§3.2: enwik8 validation, 200k steps; 8-layer full-resolution baseline 1.151 BPC, 5.75 GB, 0.73 steps/s, 28M parameters; `2@1 4@3 2@1` 1.128 BPC, 4.88 GB, 1.00 steps/s, 34M. These are training measurements, not inference throughput; batch/model details and several hardware setups are in Appendices B–C. Larger parameter count means parameter equality is not the control.
- §3.3, Table 2: the 146M model achieves test 0.98 BPC with overlapping 4096-byte windows, step 128, scoring only last 128, after 350k steps; Transformer-XL 277M 0.99, Adaptive Span 209M 0.98, and better historical models reach 0.95–0.97. Context/scoring and external systems are not fully matched; 0.98 is not a field-wide SOTA claim.
- §4.1/Table 4: randomized training k∈{2,3} improves same-k validation versus fixed counterparts. Example `2@1 8@k 2@1` gives 1.104/1.116 at k=2/3 versus fixed 1.116/1.124. Authors hypothesize information is distributed more uniformly; this mechanism was not directly established.
- Table 6: removing all fine layers is poor (1.460 BPC); (1,1) fine-layer allocation gives 1.171 and (2,2) 1.128, though extra depth is extra compute. Table 7 enwik8 repeat/linear/attention variants 1.148/1.163/1.145 or 1.132; Table 8 average/linear pooling 1.129/1.159, attention with average 1.124. Image rankings differ; §4.6 leaves best hierarchy unsettled.
- Appendix B: Adam β=(.9,.98), no weight decay or clipping, 200k-step enwik8 ablations, batch 8, dropout .15 and 4e−4 selected; Appendix D reports three baseline repeats for ablations and single runs otherwise. No teacher; full training FLOPs, detailed decoding latency/cache and explicit EOS accounting are unknown. ImageNet32 score 3.741 bits/dim is separate modality evidence.

**Inventory handoff:** [BIP-0103](DETAILED_INVENTORY.md#BIP-0103) and [BIP-0104](DETAILED_INVENTORY.md#BIP-0104): preserve extra shift on all attention-pooling operands, fine-path necessity, fixed group semantics, and windowed scoring costs.


**Current R1 adjudication ([FULL_READING_AUDIT_R1](../05_review/FULL_READING_AUDIT_R1.md)):** Without fine-resolution Transformer layers, the shortened branch lacks current-group history, but the direct one-step-shifted input residual still conveys the immediately preceding symbol. Appendix A.1/Table 9 demonstrates a particular two-position-back copying dependency this restricted access cannot express; it does NOT show blanket independence of every within-group position. A fine-resolution attention layer removes that restriction in the construction, not a guarantee of learned arbitrary-task accuracy. Additional k−1 shifting must still cover all shortening Q/K/V inputs.

**Final R2 / claim-rules adoption** ([CLAIM_RULES](../05_review/CLAIM_RULES.md); [FULL_READING_AUDIT_R2](../05_review/FULL_READING_AUDIT_R2.md)): R2 reconfirms Hourglass v2 AppendixA.1/Table9: only the shortened branch lacks current-group history; the shifted-input residual can convey the immediately previous symbol. The particular two-position-back copy limitation is not blanket within-group independence and not evidence of a causal leak. One fine-resolution attention layer removes that restriction in the construction, not every dependency/learned-accuracy guarantee. Extra k−1 shifting must respect all pooling information paths includingQ/K/V.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2110.13711v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** enwik8 symbols/characters and separately image values → fixed-rate shortened states → original-resolution next symbols; autoregressive LM. No variable boundary learner.
- **Learning and causal baseline:** enwik8 symbols/characters and separately image values → fixed-rate shortened states → original-resolution next symbols; autoregressive LM. No variable boundary learner.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0103](DETAILED_INVENTORY.md#BIP-0103), [BIP-0104](DETAILED_INVENTORY.md#BIP-0104).
- **Reading ownership:** [R03](batches/R03.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S02/S02-N02**, [WORKS](../01_discovery/S02/WORKS.md) line 32: Nawrot et al., **Hierarchical Transformers Are More Efficient Language Models** (Hourglass), [2110.13711v2](https://arxiv.org/html/2110.13711v2), 2022-04-16
  - Original register aliases / era / family / provenance: S02-N02; **fresh**
  - Source-scoped evidence/depth: P: §§2.1–2.3, algorithm1 and §3.1 opening. Detailed experiments, figures and appendix causal proof not read.
- **S03/S03-N09**, [WORKS](../01_discovery/S03/WORKS.md) line 51: S03-N09 · Hierarchical Transformers Are More Efficient Language Models (Hourglass, 2021/2022); [2110.13711v2](https://arxiv.org/html/2110.13711v2), 2022-04-16 P: §2.2–2.3; abstract; appendix not read
  - Original register aliases / era / family / provenance: S03-N09 · Hierarchical Transformers Are More Efficient Language Models (Hourglass, 2021/2022); [2110.13711v2](https://arxiv.org/html/2110.13711v2), 2022-04-16
  - Source-scoped evidence/depth: P: §2.2–2.3; abstract; appendix not read

</details>

<a id="BIW-0073"></a>
## BIW-0073 — A Vocabulary-Free Multilingual Neural Tokenizer for End-to-End Task Learning

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/2204.10815. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **Characters** → neural tokenizer units → NLI/sentiment labels; segmentation distilled from heuristic subwords then task learning. No byte/causal-generation assertion.
- **Learning and causal baseline:** **Characters** → neural tokenizer units → NLI/sentiment labels; segmentation distilled from heuristic subwords then task learning. No byte/causal-generation assertion.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0155](DETAILED_INVENTORY.md#BIP-0155).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S02/S02-N03**, [WORKS](../01_discovery/S02/WORKS.md) line 33: Islam et al., **A Vocabulary-Free Multilingual Neural Tokenizer for End-to-End Task Learning**, [2204.10815v1](https://arxiv.org/abs/2204.10815), 2022-04-22
  - Original register aliases / era / family / provenance: S02-N03; **fresh**
  - Source-scoped evidence/depth: A: primary abstract. HTML404. MANTa Related Work understates this as merely imitation; abstract explicitly claims subsequent task learning, which requires full-read reconciliation.

<a id="BIW-0074"></a>
## BIW-0074 — Patching Leaks in the Charformer for Efficient Character-Level Generation

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Lukas Edman, Antonio Toral, Gertjan van Noord; [arXiv 2205.14086v1, 27 May 2022](https://arxiv.org/pdf/2205.14086v1). Alias S02/S02-N05. This is distinct from the same authors' subword-delimited downsampling work [BIW-0075](../03_reading/R03/BIW-0075.md).

**Reading depth: FULL, fresh.** Read all six PDF pages: §§1–5, Figures 1–2, Tables 1–5, Appendices A–C, including diagnostic and translation training details. No source code, trained model or result was independently executed.
- **Carrying card:** [R03/BIW-0074](../03_reading/R03/BIW-0074.md).
- **Canonical problem records:** [BIP-0166](DETAILED_INVENTORY.md#BIP-0166), [BIP-0167](DETAILED_INVENTORY.md#BIP-0167).
- **Units — input / internal / output / supervision (current):** UTF-8bytes forMT; independent100symbols forleakdiagnostic / fixedGBSTblocks+groupTransformer+localLSTM / targetbytes or diagnostic nextsymbol / translationCE or randomnextsymboldiagnostic.

### Current substantive interface, technique, evidence and limits

**Reading depth: FULL, fresh.** Read all six PDF pages: §§1–5, Figures 1–2, Tables 1–5, Appendices A–C, including diagnostic and translation training details. No source code, trained model or result was independently executed.

### Interface, causal failure and method

Though called character-level, translation systems actually operate on **UTF-8 bytes** (Appendix B.2 footnote 8): input/output/translation supervision are bytes; internal fixed-size pooled blocks are continuous hidden vectors. The leak diagnostic instead uses sequences of independent random symbols in a vocabulary of **100**, not UTF-8 text. Training discards pairs with English sentences longer than 256 characters; normalization and EOS behavior are not specified. Input/output embedding ties, encoder/decoder ties, output heads and recurrent-weight-sharing axes are not specified.

**Problem:** applying the encoder-origin Charformer grouping naively in a causal decoder leaks target tokens through convolutional positional embeddings and n-gram windows that overlap future pooling blocks (§2, Fig. 1). **One-sentence solution:** replace the convolution by sinusoidal positions and either remove n-grams crossing blocks or causally mask their contributions; use a local LSTM after the group-level Transformer for byte-by-byte generation. Actual techniques: GBST computes candidate n-gram means, learned weighted mixtures and final fixed-stride means; sinusoidal encoding removes convolution leakage; boundary-aware removal/masking prevents future block access; causal LSTM provides fine-resolution local dependence (§§2–3). Source encoding may use complete source; target generation conditions on earlier output. The paper is evidence about its tested construction, not an implementation audit proving every decoder arrangement safe.

Three alternatives are compared: (1) pad by twice the downsampling factor, making the model predict two blocks ahead; (2) sinusoidal encoding plus remove overlapping n-grams; (3) sinusoidal encoding plus causal masking of overlaps (Fig. 2). Masking retains some n-gram information but yields position-inconsistent partial means. The authors' suggestion that this explains quality loss is a hypothesis. The paper does not establish a named verifier, exact EOS handling, or general partial-prefix serving.

### Diagnostic, experiments, negative controls

- Appendix A/Table 1: 5000 Adam iterations, lr 1e−4, batch 32; evaluation over 100 batches = 3200 samples of random 12-symbol sequences. Chance accuracy is 1%. At factor 4 with convolution, the first three positions of each four-position block are near 100% accurate: direct evidence of future information in this construction. The same factor with sinusoidal embeddings still has 13.47% and 3.38% accuracy at first two positions, showing the n-gram overlap leak remains. Random test success is a useful check, not a general proof.
- Table 2: German→English BLEU at δ=2: noncausal 0.00, extra padding 0.04, removal 25.49, masking 24.59; at δ=4 removal 22.07 versus masking 17.47. English→German δ=2: 0.00/0.80/22.17/21.90. Padding removes leakage but fails to learn useful translation; Appendix C/Table 5 shows similar Arabic trends.
- Table 3: German→English BLEU for no-downsampling byte model 27.4, subword 27.2, Lee-convolution δ=2 27.1, removed-GBST δ=2 24.8; English→Turkish respectively 11.9/11.3/11.1/10.6. Results depend on language and metric; leak-free GBST is not accuracy-neutral. Factor 4 is generally worse. In δ=2 German→English timing (Table 4), r-GBST two-step train-to-completion 10:15:02 vs Lee 13:22:48; normal byte 14:52:21 and normal subword 3:52:31. Early stopping changes epochs, so completion times are not per-step efficiency; the per-epoch times are 10:38, 13:09, 14:37 and 5:34 respectively.
- IWSLT17 English↔German/Arabic, SETIMES2 English↔Turkish; SentencePiece baseline vocabulary 16k/16k/8k. Transformer Base, AdamW 2e−4, warmup 4k, batch 128, label smoothing .1, early-stopping patience 10, one V100 32GB (Appendix B). Per-model total parameters, FLOPs, exact sentence counts and teacher/cache policy are not specified; no distillation teacher is reported.

**Inventory handoff:** [BIP-0166](DETAILED_INVENTORY.md#BIP-0166), [BIP-0167](DETAILED_INVENTORY.md#BIP-0167): retain 100-symbol test vs UTF-8 translation distinction; test correctness and translation quality separately.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2205.14086v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Despite character title, experiments use **UTF-8 bytes** (AppendixB.2) → fixed blocks → target bytes; translation supervision and random-symbol leakage diagnostic.
- **Learning and causal baseline:** Despite character title, experiments use **UTF-8 bytes** (AppendixB.2) → fixed blocks → target bytes; translation supervision and random-symbol leakage diagnostic.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0166](DETAILED_INVENTORY.md#BIP-0166), [BIP-0167](DETAILED_INVENTORY.md#BIP-0167).
- **Reading ownership:** [R03](batches/R03.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S02/S02-N05**, [WORKS](../01_discovery/S02/WORKS.md) line 34: Edman, Toral & van Noord, **Patching Leaks in the Charformer for Efficient Character-Level Generation**, [2205.14086v1](https://arxiv.org/html/2205.14086v1), 2022-05-27
  - Original register aliases / era / family / provenance: S02-N05; **fresh**
  - Source-scoped evidence/depth: P: §§2–4 and AppendixB.2–B.3; most numeric tables not extracted. **Not the same paper as N06**; N06 cites this as earlier work.

</details>

<a id="BIW-0075"></a>
## BIW-0075 — Subword-Delimited Downsampling for Better Character-Level Translation

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Lukas Edman, Antonio Toral, Gertjan van Noord; [Findings of EMNLP 2022, pp. 981–992, official PDF](https://aclanthology.org/2022.findings-emnlp.69.pdf). Alias S02/S02-N06; the arXiv version and this official paper are one work.

**Reading depth: FULL, fresh.** Read all 12 PDF pages: §§1–10, Fig. 1, Tables 1–16, Appendices A–D and limitations. Visually checked Tables 3–7 on printed pp. 985–987 to resolve PDF extraction column ordering. No code, reported scores or training runs independently verified.
- **Carrying card:** [R03/BIW-0075](../03_reading/R03/BIW-0075.md).
- **Canonical problem records:** [BIP-0168](DETAILED_INVENTORY.md#BIP-0168).
- **Units — input / internal / output / supervision (current):** UTF-8bytes+group/endmarkers withSentencePiece boundaries / variable externallysubword-delimited groups / autoregressive local bytes/endmarker / translationlikelihood; goldtraininggroupmasks, generatedendmarkerinference.

### Current substantive interface, technique, evidence and limits

**Reading depth: FULL, fresh.** Read all 12 PDF pages: §§1–10, Fig. 1, Tables 1–16, Appendices A–D and limitations. Visually checked Tables 3–7 on printed pp. 985–987 to resolve PDF extraction column ordering. No code, reported scores or training runs independently verified.

### Interface, objective, causality, sharing

Footnote 6 and Appendix B.2 explicitly say the so-called character system processes **UTF-8 bytes**; input, output and translation prediction labels are bytes plus boundary/termination markers; hidden units are variable-size, externally subword-delimited pooled byte groups and Transformer states. SentencePiece proposes source and target subword boundaries; it is therefore not a tokenizer-free grouping method. At target training time ground-truth boundaries/lengths govern masks; at inference the decoder emits an end-of-word symbol per group, then proceeds to the next group (§4.1–4.2). Exact mechanics of incremental subword-boundary recovery beyond the described end symbol, EOS behavior and deployment tokenizer cost are not quantified. Source is bidirectional; target block attention masks prevent future-block leakage while the local LSTM receives previously emitted byte embeddings shifted by one. Cross-entropy details/label smoothing are not stated; AdamW optimization and early-stopping BLEU are specified in Appendix B.3. Input/output embedding, source/target, head and layer tying are not specified.

### Problems and one-sentence solutions

- **BIP-0168 / grouping:** Fixed byte blocks split words at position-dependent offsets; word-level blocks can become too long for a pooling and decoding bottleneck. **Solution:** SentencePiece-delimit variable groups, apply the same CNN/max-pooling encoder and causal group mask in the decoder, and generate each group with a recurrent upsampler terminated by an end marker (§§3–4, Fig. 1). Techniques used: CNN for local patterns, max pooling for group aggregation, Transformer for contextual group representation, autoregressive LSTM for byte-level recovery, and SentencePiece for boundary proposal. LSTM input is the current repeated group representation plus prior byte embedding; variable block lengths require per-example masks and repeat counts. Word boundaries, not learned neural segmentation, govern WDD; SDD uses subword boundaries.
- **Position/length/morpheme confounding:** A single fixed-versus-subword result would conflate offset, length and lexical grouping. **Solution:** compare fixed, buffered-fixed (spaces pad to align word starts), word-delimited (WDD) and subword-delimited (SDD) groups; selected difference contrasts measure bundled interventions, not clean independent causal estimates of linguistic morphology (§3, Table 3). A SentencePiece token is not guaranteed a morpheme.
- **Task/evaluation bottleneck:** Character recovery may matter more to translation than classification. **Solution:** test the same grouping families on translation, NLI and review classification, plus OOD/low/high-resource conditions (§§6–8, Appendices C–D). Interpretation about cross-attention or recoverability is author speculation, not isolated ablation.

### Evidence and budgets

- Table 3, six-direction average BLEU: fixed 16.56, buffered fixed 19.46, WDD 18.58, SDD 19.98; the paper's calculated position contrast +2.90, length +1.41, morphology +0.52 are comparisons between entire systems, with SDD vs buffered fixed **−0.93** for German→English. No random-boundary baseline is reported. Table 4: average SDD 19.98 versus byte-without-downsampling 19.03 and subword 19.02, but SDD English→Turkish 11.31 vs byte 11.87. COMET English→German 0.023 versus subword 0.073, marked significant negative; not universal superiority.
- Table 6 biomedical DE→EN: byte 11.71 BLEU, SDD 9.41, subword 9.37; EN→DE byte 4.74, SDD 4.05, subword 4.36. Table 7 NLI SDD 81.30%, WDD 81.89%, buffered fixed 81.81%, showing SDD not best on every task. §7's embedding probe uses separate T5-vocabulary models and cannot be read as a direct intervention on the translation model.
- Main translation training examples are 199k en↔de, 224k en↔ar, 197k en↔tr; sentence counts, datasets and domain details are in Appendix A Table 10. Transformer Base, max positions 2048, effective batch 128 over four accumulation steps, AdamW 2e−4, warmup 10k, one V100; stopping by validation BLEU. Approximate average 4 bytes/group, but SentencePiece's maximum length is in characters and Arabic commonly 2–3 UTF-8 bytes per character (§5, B.2). Parameter totals are 56M SDD, 46M byte, and 51–62M subword for the three main pairs (Table 13), so this is not equal total capacity.
- Table 9 translation training time versus subword: SDD ×2.61 per iteration and ×3.34 to completion; no-downsampling byte ×3.58 and ×4.69. Thus SDD still costs more than subword; times combine epoch counts and implementation. Test-time latency, full FLOPs and tokenizer cost are not specified. No teacher is reported.
- Appendix C Table 15, 4.509M WMT14 de→en: standard subword 28.62 BLEU, subword with two-step LSTM 27.49, SDD 27.27; two-step head is itself a confound/limitation at higher resource. Appendix D Xhosa↔Zulu: byte 6.51/6.42, SDD 6.35/6.32, subword 4.59/5.89. No pretraining, and only one additional language pair.

**Inventory handoff:** [BIP-0168](DETAILED_INVENTORY.md#BIP-0168): preserve externally supplied segmentation, boundary markers/causality, train–inference distinction, non-isolated contrast labels, parameter/time budgets and high-resource/OOD counterexamples.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2022.findings-emnlp.69.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Detailed character/byte encoding must be checked in this paper, not inherited from N05 → subword-delimited groups → translation. Subword-informed structural prior; exact predictor/aggregator/cost unknown at current depth.
- **Learning and causal baseline:** Detailed character/byte encoding must be checked in this paper, not inherited from N05 → subword-delimited groups → translation. Subword-informed structural prior; exact predictor/aggregator/cost unknown at current depth.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0168](DETAILED_INVENTORY.md#BIP-0168).
- **Reading ownership:** [R03](batches/R03.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S02/S02-N06**, [WORKS](../01_discovery/S02/WORKS.md) line 35: Edman, Toral & van Noord, **Subword-Delimited Downsampling for Better Character-Level Translation**, [formal page](https://aclanthology.org/2022.findings-emnlp.69/), [official bibliography](https://aclanthology.org/2022.findings-emnlp.69.bib), pp.981–992; [2212.01304v1](https://arxiv.org/abs/2212.01304v1)
  - Original register aliases / era / family / provenance: S02-N06; **fresh**
  - Source-scoped evidence/depth: A: formal abstract/metadata, arXiv identity checked. Full method and comparator tables still missing.

</details>

<a id="BIW-0076"></a>
## BIW-0076 — Scratchpad Patching: Decoupling Compute from Patch Size in Byte-Level Language Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Lin Zheng, Vasilisa Bashlovkina, Timothy Dozat, Dan Garrette, Laura Rimell, Joshua Maynez, [arXiv:2605.09630v1](https://arxiv.org/pdf/2605.09630v1), 10 May 2026. Aliases S02/S02-R01, S03/S03-N01, S06/S06-N03. **Reading: FULL:** substantive §§1–7, limitations and Appendix A–E, pp.1–23; Tables 1–3, Figures 1–15. PDF pp.7–8 visual confirmation; [PDF](../03_reading/R05/sources/BIW-0076.pdf), [extraction](../03_reading/R05/sources/BIW-0076.txt). No implementation execution or reproduction.

UTF-8 bytes are inputs and next-byte outputs/supervision; vocabulary 320 = 256 bytes plus 64 special IDs (§2.2). Internal units are locally encoded bytes, committed contiguous patches, and *transient* within-patch scratchpad states. The common causal Transformer encoder/trunk/decoder uses local cross-attention to aggregate bytes, with a mean-pooled query; the decoder gets broadcast trunk output plus byte encoder residual (§2, Appendix B). H-Net is only a reimplemented single-stage patchifier variant, not the complete original multistage H-Net.
- **Carrying card:** [R05/BIW-0076](../03_reading/R05/BIW-0076.md).
- **Canonical problem records:** [BIP-0105](DETAILED_INVENTORY.md#BIP-0105), [BIP-0106](DETAILED_INVENTORY.md#BIP-0106), [BIP-0107](DETAILED_INVENTORY.md#BIP-0107).
- **Units — input / internal / output / supervision (current):** UTF-8bytes+specials,vocab320 / local bytes,committedpatches,transientpartialpatchstates / next-byte / decoderCE+auxLMCE,auxgradientstoppedatencoder.

### Current substantive interface, technique, evidence and limits

### Input and method

UTF-8 bytes are inputs and next-byte outputs/supervision; vocabulary 320 = 256 bytes plus 64 special IDs (§2.2). Internal units are locally encoded bytes, committed contiguous patches, and *transient* within-patch scratchpad states. The common causal Transformer encoder/trunk/decoder uses local cross-attention to aggregate bytes, with a mean-pooled query; the decoder gets broadcast trunk output plus byte encoder residual (§2, Appendix B). H-Net is only a reimplemented single-stage patchifier variant, not the complete original multistage H-Net.

**Problem / one-sentence solution:** large patches reduce persistent trunk sequence and cache but cause patch-level information to lag the observed byte prefix; temporarily pool each observed partial patch, run the shared trunk, and broadcast its updated state without committing it to the trunk's persistent cache.

At prefix n, a partial scratchpad aggregates byte states from the patch start through n; it informs subsequent next-byte prediction. During parallel training every scratchpad or committed state sees itself and preceding *committed* patch states only; scratchpads do not attend one another, all have the patch's positional index, and prior scratchpads are not retained. Thus refinement is by growing the observed prefix, **not scratchpad-to-scratchpad recurrence**. Patch boundary takes precedence over an overlapping trigger. At inference scratchpad cache entries are overwritten, but local encoder/decoder computation, scratchpad working memory, and committed trunk cache still exist (§3/Fig.4).

**AI techniques and supervision:** auxiliary two-layer Transformer + byte LM head estimates next-byte entropy online; threshold fires a scratchpad. Equal-weight auxiliary and decoder next-byte losses train jointly, but auxiliary gradient is stopped at encoder output (App. B.3). Entropy-patch variant reuses that auxiliary head at a separate threshold; H-Net shares auxiliary layers but uses a distinct LM output head from the router. The trunk is shared across permanent and transient states; input↔output embedding and auxiliary↔decoder readout tying are not specified. H-Net router uses MLP and ratio-loss target, not a claim that all patchifier families learn boundaries.

### Evidence and implications

- [BIP-0105](DETAILED_INVENTORY.md#BIP-0105): stale global context can be refreshed causally before patch completion while persistent patch count stays unchanged. Table 1, fixed p=16 NLU average 48.0→54.2 with scratchpads versus flat byte 54.1; validation FLOPs reduction 5.7×→2.9×. Increasing quality also costs compute, so persistent cache reduction is not free.
- [BIP-0106](DETAILED_INVENTORY.md#BIP-0106): *where* to spend extra computation matters. Fig.7 compares models at matched training FLOPs: improvements or matches in three patchifier families, but **H-Net can regress**; appendix E.3 offers one-byte-offset router/update redundancy as a hypothesis, not an identified causal proof. Fixed-p8 entropy triggering beats fixed-stride/space-like updates on the reported quality/FLOPs frontier; dense scratchpads yield marginal code/math gains at roughly 3× training FLOPs and can be slightly worse on natural language (E.2 Fig.12).
- [BIP-0107](DETAILED_INVENTORY.md#BIP-0107): a training-time trigger makes inference-time compute tunable without retraining (§5.3 Figs.9–10); language and task outcomes remain separate. FLORES-200 average rank has flat byte as strongest, SP narrows the gap (Fig.8), so English and code results do not establish multilingual superiority.

Table 2: on MBPP, p16 baseline vs SP vs flat byte pass@1 18.2 vs 27.5 vs 26.3, reported cache reduction 16× and inference FLOPs/byte 5.6× vs 3.7×; HumanEval 10.5 vs 14.8 vs 15.5, SP 16× cache and 4.5× FLOPs reduction. These are per-paper inference cache/FLOP estimates, not measured wall-clock speedups; byte-level total serving memory, transient workspace, cache implementations and peak memory are not established. Multiple-choice evaluation uses validation-derived compute proxies, not direct task latency.

### Budget/controls

§4 / App.C–D: ~2B total params, identical ~400B raw bytes (DCLM, Stack v2, OpenWebMath), 50k updates, batch 8M bytes, TPUs, AdamW 1e-3 and cosine; 8192-byte byte contexts vs 2216 subword tokens ≈8192 bytes. Parameter-matched but fixed exposure means training FLOPs vary; FLOP-matched family curves address a separate question. Code pass@1 is estimated from 5 samples at temperature .2/top-p .95, MBPP 3-shot/HumanEval zero-shot; eight NLU tasks 5-shot. Tokenizer baseline is stronger on average NLU (55.9 vs byte 54.1), weaker on code; don't flatten task-dependent counterexamples. Scratchpad trigger head's compute must be included in any complete downstream accounting; exact precision, wall time and local-cache footprint not reported.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; recovery discovery reused, absent old W catalog. No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2605.09630v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes → persistent patches plus temporary partial-patch states → bytes; next-byte LM, entropy-triggered scratchpads. Refresh uses only observed partial patch; no claim of future access.
- **Learning and causal baseline:** Bytes → persistent patches plus temporary partial-patch states → bytes; next-byte LM, entropy-triggered scratchpads. Refresh uses only observed partial patch; no claim of future access.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0105](DETAILED_INVENTORY.md#BIP-0105), [BIP-0106](DETAILED_INVENTORY.md#BIP-0106), [BIP-0107](DETAILED_INVENTORY.md#BIP-0107).
- **Reading ownership:** [R05](batches/R05.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S02/S02-R01**, [WORKS](../01_discovery/S02/WORKS.md) line 52: Zheng et al., **Scratchpad Patching: Decoupling Compute from Patch Size in Byte-Level Language Models**, [2605.09630v1](https://arxiv.org/abs/2605.09630v1), 2026-05-10
  - Original register aliases / era / family / provenance: S02-R01; **reused recovery discovery**, old `07_BYTE_SURVEY/N01`
  - Source-scoped evidence/depth: A: primary abstract rechecked; old audit had abstract/introduction only, no FULL card.
- **S03/S03-N01**, [WORKS](../01_discovery/S03/WORKS.md) line 36: S03-N01 · Scratchpad Patching: Decoupling Compute from Patch Size in Byte-Level Language Models (2026); [2605.09630v1](https://arxiv.org/html/2605.09630v1) recovery BYTE N01; P: original §3.1–3.2 and selected §1/§4/§5 search hits
  - Original register aliases / era / family / provenance: S03-N01 · Scratchpad Patching: Decoupling Compute from Patch Size in Byte-Level Language Models (2026); [2605.09630v1](https://arxiv.org/html/2605.09630v1)
  - Source-scoped evidence/depth: recovery BYTE N01; P: original §3.1–3.2 and selected §1/§4/§5 search hits
- **S06/S06-N03**, [WORKS](../01_discovery/S06/WORKS.md) line 50: **Scratchpad Patching: Decoupling Compute from Patch Size in Byte-Level Language Models**, Zheng et al.; [2605.09630v1](https://arxiv.org/html/2605.09630v1),2026-05-10
  - Original register aliases / era / family / provenance: S06-N03; **recovery reuse**, byte audit N01
  - Source-scoped evidence/depth: ~2B params,~400B raw bytes; common reimplemented backbone, not exact original H-Net/SpaceByte/BLT. Main comparison fixed-data, not fixed training FLOPs. §5.1 equal-FLOP H-Net variant can worsen. Cache16× reduction refers trunk patch cache, not peak all-model memory or latency. **P**, missing full table/appendix audit.

</details>

<a id="BIW-0077"></a>
## BIW-0077 — From Bytes to Ideas: Language Modeling with Autoregressive U-Nets

- **Reading status:** NF — returned new scoped FULL (R10), actual card read for integration; no fresh original-paper credit to inventory owner.
- **Carrying card:** [R10/BIW-0077](../03_reading/R10/BIW-0077.md).
- **Current units: input / internal / output / supervision:** Rawbytes / regexword-like groups,2/4groups andfinebytestates / next-bytes ONLY / onebyteARobjective; deeper anticipation from shiftedexpansion, noauxword-targetloss.
- **Canonical records:** [BIP-0108](DETAILED_INVENTORY.md#BIP-0108).

### Current card-grounded detail

**Reading status: FULL**, scoped to [arXiv:2506.14761v1](https://arxiv.org/pdf/2506.14761v1), 17 June 2025, all text §§1–5, Figures 1–3, Tables 1–3, limitations and Appendices A–H, including Tables 4–11. Key Tables 2, 4, 5, 7 were visually checked from the fixed PDF; [PDF](../03_reading/R10/sources/BIW-0077.pdf), [text](../03_reading/R10/sources/BIW-0077.txt), [p.7](../03_reading/R10/sources/BIW-0077-p7.png), [p.13](../03_reading/R10/sources/BIW-0077-p13.png), [p.14](../03_reading/R10/sources/BIW-0077-p14.png). FULL is paper reading, not code execution, causal proof, or reproduction. [BIP-0108](DETAILED_INVENTORY.md#BIP-0108).

### Problem → solution → techniques

A single segmentation couples representation granularity and how much future text the expensive model must anticipate. **AU-Net** uses an autoregressive Transformer U-shaped contraction/expansion hierarchy over raw bytes: select contextual states at externally specified segment ends, run wider causal attention on the shortened stream, then expand and add skip connections. Stage 2 follows regex-defined word-like units; stages 3 and 4 aggregate two and four such units, with sentence-end exceptions. The word boundary prior is **hand-specified**, not learned (§§2.1–2.2, Appendix B).

Author-used mechanisms and roles: causal self-attention implicitly composes contextual segment vectors; linear projection changes stage width; position-specific multi-linear projections expand a coarse state across positions of the **following** segment; skips preserve high-resolution signal; a byte-stage sliding window limits attention cost; fully sharded training, packing and compilation enable experiments. The multi-word anticipation is induced by shifted next-segment use, **not an auxiliary multi-token loss** (§1, Fig. 2). It is not evidence of a separately normalized word-level output model.

### Units and causal contract

- Input/output and supervised events: raw bytes, autoregressive next-byte training; internal positions are bytes, regex chunks, and groups of 2 or 4 chunks; no discrete word-ID prediction head. One conditional byte chain is the reported language-model object; deeper horizons describe what those internal states must support, not extra normalized joint outputs. Teacher/tokenizer for its splits: none learned, but a manually chosen GPT-4o-inspired regex is a strong external segmentation prior.
- Figure 2: the state after `SAT ` informs the next segment `ON `, rather than its own already seen bytes. Training evaluates stages in parallel; inference activates the byte stage every byte, coarse stages at their boundaries, caching latest stage outputs (§2.1.2). §2.2 requires decisions to be stable under rightward insertion. Appendix B regex contains bounded letter/number groups, punctuation and lookahead-sensitive whitespace alternatives, so this is an implementation obligation, **not a verified proof that every published regex decision is prefix-stable**. Partial prompts, end-of-sequence flush, exact masks and actual cache implementation are unreported or unverified; no leakage conclusion follows merely from that absence.
- Fixed stage capacities for compilation pad shorter and abruptly truncate overlong stage sequences (§3.1); exact truncation frequencies and quality impact are unreported. This is not unrestricted adaptive compute.

### Evidence, controls and costs

- DCLM is predominantly English; BPE and byte Transformer, and byte Mamba, are explicit comparators. Data equivalence uses the corpus average 4.56 bytes per LLaMA-3 token, rather than verified identical prefix-by-prefix contexts (§§2.3, 3.1). Estimated training FLOPs sum stage costs weighted by contraction. H100 80GB training throughput is **bytes/s/GPU**, not cached serving latency.
- Table 2 p.7, 60B token-equivalent exposure: BPE 1.8B parameters, 7e20 FLOPs, 210k bytes/s/GPU; AU-Net-2 1.3B, 5e20, 225k; AU-Net-3 2.5B, 7e20, 180k; AU-Net-4 4.2B, 8e20, 155k. TriviaQA BPE 26.3, AU-Net-2 20.4, AU-Net-3 22.6, AU-Net-4 15.5. They are **equal-data, not equal-parameter or exactly equal-FLOP** arms.
- At 370B token-equivalent, BPE/AU-Net-2/3/4 use 4e21/3e21/4e21/5e21 FLOPs and score HellaSwag 70.2/69.9/72.9/73.7 and GSM8K 4.4/3.0/3.7/5.3. Across separate approximately compute-controlled scaling runs (Fig. 3), 2/3 stages track BPE on HellaSwag/ARC-Easy/NQ; TQA initially lags, and MMLU/GSM8K lag at 1e22. Neither set supports blanket superiority at matched quality and serving budget.
- Appendix C Table 4: 3-stage simple versus multi-linear upsampling gives HellaSwag 60.6 vs 66.0, TQA 13.3 vs 18.7, showing expansion choice matters. Table 5 varies deep-stage layer allocation; 75% is selected. Appendix E Table 7: character-spell 91.5 BPE vs 97.3 AU-Net-2, inverse spelling 80.6 vs 91.7; word-task average 36.9 vs 33.1, character-task average 39.3 vs 42.7. This is not a win on every editing task.
- Table 3 multilingual MMLU average 31.4 vs 32.4, but Chinese 33.0 vs 28.0 and Japanese 29.5 vs 28.2. English-to-low-resource generation is difficult; §5 limitations explicitly acknowledge non-space-delimited-language limitations. FLORES results are not training-controlled evidence across languages or general script fairness.
- Appendix D/H details model configurations, 2048 BPE versus 8192 byte nominal sequence lengths in Table 6 and optimizer/FLOP settings in Tables 9–11. Appendix G is a heading in this fixed version; no separate detailed body is supplied there. Exact sampling settings, generation wall-clock, cache memory, and full tokenizer/FSDP overhead are unreported.

### BIP implication

For BIP-0108, distinguish **longer-horizon hidden representations trained by the same byte loss** from explicitly supervised or jointly sampled multi-byte output. This paper supports rule-based multi-rate causal scheduling with costly expansion choices, not learned semantic boundaries or general guarantees on streaming regex behavior. Table-specific, unequal-parameter/data/compute conditions must remain next to comparisons.


<details>
<summary>Prior catalog provenance and source aliases — historical depth, superseded by current receipt</summary>

- **Entity / provenance:** paper; recovery discovery reused, absent old W catalog. No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2506.14761v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Bytes → words/word pairs/up-to-four-word representations → multiscale future predictions; exact source of word boundaries and output factorization unknown here.
- **Learning and causal baseline:** Bytes → words/word pairs/up-to-four-word representations → multiscale future predictions; exact source of word boundaries and output factorization unknown here.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0108](DETAILED_INVENTORY.md#BIP-0108).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S02/S02-R02**, [WORKS](../01_discovery/S02/WORKS.md) line 53: Youbi Idrissi et al., **From Bytes to Ideas: Language Modeling with Autoregressive U-Nets**, [2506.14761v1](https://arxiv.org/abs/2506.14761v1), 2025-06-17
  - Original register aliases / era / family / provenance: S02-R02; **reused recovery discovery**, old `07_BYTE_SURVEY/N03`
  - Source-scoped evidence/depth: A: primary abstract rechecked; prior recovery discovery, not fresh.
- **S03/S03-N03**, [WORKS](../01_discovery/S03/WORKS.md) line 38: S03-N03 · From Bytes to Ideas: Language Modeling with Autoregressive U-Nets (2025); [2506.14761v1](https://arxiv.org/abs/2506.14761v1) recovery BYTE N03; A, no method/full experiments read
  - Original register aliases / era / family / provenance: S03-N03 · From Bytes to Ideas: Language Modeling with Autoregressive U-Nets (2025); [2506.14761v1](https://arxiv.org/abs/2506.14761v1)
  - Source-scoped evidence/depth: recovery BYTE N03; A, no method/full experiments read



</details>

<a id="BIW-0078"></a>
## BIW-0078 — You Can Learn Tokenization End-to-End with Reinforcement Learning

- **Reading status:** NF — returned new scoped FULL (R09), actual card read for integration; no fresh original-paper credit to inventory owner.
- **Carrying card:** [R09/BIW-0078](../03_reading/R09/BIW-0078.md).
- **Current units: input / internal / output / supervision:** Bytes+specials / fullbyteencoder→selectedcausalstates→repeat/addbytepath / next-byteconditionals / expected boundary-policy conditionalLM lowerbound, score-functiongradient, discountedreward/earlyexit/rate losses.
- **Canonical records:** [BIP-0164](DETAILED_INVENTORY.md#BIP-0164), [BIP-0165](DETAILED_INVENTORY.md#BIP-0165).

### Current card-grounded detail

**Status: FULL**, [arXiv 2602.13940v4, 14 Sep 2026](https://arxiv.org/pdf/2602.13940v4), §§1–5, Tables 1–3, Figure 3–4 captions, and Appendices A–D including D.1. [PDF](../03_reading/R09/sources/BIW-0078.pdf), [UTF-8 extract](../03_reading/R09/sources/BIW-0078.txt); [HTML Table 1](https://arxiv.org/html/2602.13940v4#S4.T1) checked to disambiguate extract row layout. Appendix B boundary plots are read through captions and authors' descriptions, not independently digitized. FULL means source coverage, not correctness proof, actual prefix stability or code execution.

### Problem, architecture, information contract

[BIP-0164](DETAILED_INVENTORY.md#BIP-0164): straight-through estimators backpropagate a surrogate through hard choices. The researchers instead sample discrete boundary actions and use the score-function (REINFORCE) policy gradient jointly with ordinary next-byte gradients; this is a different learning route, not Gumbel/straight-through or external-teacher distillation (§§2.2–2.3). Input/output/supervision are byte positions and next bytes, with special characters included in the vocabulary; internal units are first full-resolution byte states, selected latent token states, then byte states again. The byte encoder/decoder are causal windowed Transformers, the middle is full causal attention on selected states. Downsampling selects the encoder state at each boundary; upsampling distributes the corresponding processed latent and adds the byte skip state. It is not a mean-pooling span representation.

At byte i, the autoregressive encoder has bytes through i; sampled a_i determines whether that state enters the middle sequence, and predictions target later bytes. The paper writes policy dependence both as x≤i and x<i in §2.4/Equation 18; the state-based construction and Equation 19 use x≤i. Interpret the index as a post-input action for predicting x_(i+1), not permission to inspect that next byte. BOS/EOS and partially completed UTF-8/prompt policy are unreported. Actual stream implementation/cache alignment is unverified. The policy is one learned Bernoulli decision per byte; training distributions over boundary paths and byte conditional predictions are different from a single deterministic tokenizer or an already-marginalized byte-chain likelihood.

### Objective, variance and rate

The formal objective is E_a~πθ[log pθ(y|x,a)], a Jensen lower bound on log Σ_a πθ(a|x)pθ(y|x,a) (Appendix A.1). Its score-function derivative has an ordinary conditional-LM term plus log p times ∇log π (A.2). This ideal identity should not be confused with an unbiased or globally optimal guarantee for the **implemented** estimator.

[BIP-0165](DETAILED_INVENTORY.md#BIP-0165): one policy sample per sequence is too noisy. The early-exit next-byte classifier gives a tokenization-independent difficulty baseline, initialized from the final head; reward is final log probability minus early-head log probability. Future rewards are discounted γ=.99 to reduce variance **at the cost of bias**, and batch-relative same-position advantages are detached. The same-batch mean includes the current sample; absent a leave-one-out correction, a textbook exact-baseline/unbiasedness claim additionally needs qualification. This is a mathematical observation, not a measured training failure. Policy and rate coefficients are .01, early loss .1 (§§2.4–2.7).

A linear projection of each byte state and up to seven preceding boundary actions yields a logit (window w=8), scaled by 16, shifted toward target rate 1/5, and soft-capped during training. A detached difference between mean boundary probability and target exerts a batch-mean-logit rate pressure. Training samples Bernoulli actions. §2.5 says soft-capping is removed for evaluation, but an exact deterministic versus sampled evaluation rule is not clearly specified; do not claim one. w=1 removes the preceding-boundary scan; it performs comparably or better on several cells. The paper describes an efficiency desideratum of <0.1% extra pretraining compute; that is a **target**, not a measured end-to-end overhead guarantee.

### Budget and results

Appendix D/Table 2: FineWeb filtered to ≥4096 bytes and truncated to exactly 4096; 147M parameters, 4 byte-encoder + 12 middle + 4 byte-decoder layers, hidden size 768, 12 heads, byte attention window 64, effective batch 128, 6×10^9 training bytes, AdamW; target rate .2. CodeParrot uses 90M, 4/6/4 layers, 3.4×10^9 bytes. These byte counts are reported training exposure, not proven unique original bytes. Training FLOPs are an estimate of 6 operations per matrix parameter per byte/token with lookup assumptions, not measured full-system power/wall time (§4.2). Hardware, end-to-end serving latency, complete teacher/tokenizer lifecycle cost and multi-seed run dispersion are unreported; table ± is labeled standard error, not established seed variability.

Table 1's gold-continuation BPB, **not zero-shot accuracy**, for uniform / Dynamic / H-Net / BPE-guided / ours w=1 / ours w=8 is respectively: FineWeb 1.376 / 1.372 / 1.386 / 1.299 / 1.280 / 1.297; PIQA 1.660 / 1.737 / 1.641 / 1.589 / 1.561 / 1.557; ARC-Easy 1.974 / 2.011 / 2.000 / 2.084 / 1.987 / 2.016. Thus uniform wins ARC-Easy numerically, and w=1 beats w=8 on FineWeb and LAMBADA (1.584 vs 1.737), despite broad author prose; do not say full policy wins every task. Table 3 actual boundary rates are uniform .200, Dynamic .200, H-Net .206, ours .204, BPE .207. Figure 4 caption reports CodeParrot validation .769 H-Net vs .568 ours at estimated 0.95×10^18 FLOPs. No baseline is an independently tuned full-size subword LM.

### BPE guidance and prefix-stability qualification

The FineWeb BPE-guided control trains a 200k vocabulary, draws end-of-token boundaries offline, and right-shifts indicators one byte (§4.3, Appendix D.1). The authors assert this eliminates lookahead. **That assertion is not a general prefix-stability proof.** As a generic counterexample, rank byte-pair merges `cd` above `bc` above `ab`: `abc` tokenizes as `a|bc`, but `abcd` as `ab|cd`. The boundary after `b` differs despite identical observed prefix `abc`; a one-byte-shifted indicator exposed after `c` can reveal `d`. This toy construction is not a test of the paper's actual tokenizer or evidence of a measured leak. The actual BPE preprocessing, special pretokenization and prefix stability remain unverified. The policy's causal mask cannot remove already encoded offline future information. This directly carries forward the review audit's offline-boundary warning.

### Implication

Compare a discrete policy against straight-through and BPE-guided controls at matched realized rates, cost and causal visibility; treat discount bias and early-head overhead as explicit design choices. More semantically shaped examples and gold-answer likelihood at 147M do not establish stronger generative accuracy, broader language fairness, exact word boundaries or matched serving efficiency.


<details>
<summary>Prior catalog provenance and source aliases — historical depth, superseded by current receipt</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2602.13940v4. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** UTF-8 bytes → sampled boundary-state sequence → next bytes; score-function/REINFORCE plus variance reduction and rate regulation. Prefix-only boundary actions.
- **Learning and causal baseline:** UTF-8 bytes → sampled boundary-state sequence → next bytes; score-function/REINFORCE plus variance reduction and rate regulation. Prefix-only boundary actions.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0164](DETAILED_INVENTORY.md#BIP-0164), [BIP-0165](DETAILED_INVENTORY.md#BIP-0165).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S02/S02-N04**, [WORKS](../01_discovery/S02/WORKS.md) line 54: Dauncey & Wattenhofer, **You Can Learn Tokenization End-to-End with Reinforcement Learning**, [2602.13940v4](https://arxiv.org/html/2602.13940v4), 2026-09-14; v1 identity also checked
  - Original register aliases / era / family / provenance: S02-N04; **fresh**
  - Source-scoped evidence/depth: P: v4 §§2.1–2.4 plus targeted snippets §§2.5–2.7/4/Appendix D; not complete experiments/appendix. v1 HTML failed. Four versions exist; conclusions use v4 text actually inspected, not a silent v1/v4 mix.



</details>

<a id="BIW-0079"></a>
## BIW-0079 — Fast and Expressive Multi-Byte Prediction with Probabilistic Circuits

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Andreas Grivas, Lorenzo Loconte, Emile van Krieken, Piotr Nawrot, Yu Zhao, Euan Wielewski, Pasquale Minervini, Edoardo Ponti and Antonio Vergari; [arXiv:2511.11346v2 PDF](https://arxiv.org/pdf/2511.11346v2), 2 June 2026, ICML 2026. Aliases S03/S03-N02; v1 title says Multi-Token. PDF p.1 includes Lorenzo Loconte; fetched HTML header omitted him. **Reading: FULL**: §§1–5, limitations and Appendices A–N, pp.1–34; Tables 1–30 and Figures 1–7, with PDF p.7–8 graphical check; [PDF](../03_reading/R05/sources/BIW-0079.pdf), [extraction](../03_reading/R05/sources/BIW-0079.txt). No execution, proof audit, weight alias verification, or independent replication.

Input/context and generated/supervised events are byte-model token IDs, not learned segment IDs: EvaByte vocabulary 320 (256 bytes plus special symbols); byte-fied Llama vocabulary 268 (Appendix E). A frozen autoregressive single-token head is the target verifier; the auxiliary draft predicts n=8 or 16 future bytes jointly. The proposed conditional circuit maps one context embedding to a normalized n-byte joint. Appendix B: input categoricals sum to one; nonnegative sum-unit softmax weights are normalized; smoothness means all children of each sum have identical variable scope, decomposability means children of a product have disjoint scope. These allow exact marginal/conditional evaluation and ancestral sampling. Fully factorized FF, global latent-mixture CP, time-inhomogeneous HMM and hierarchical binary-tree factorizations encode different dependencies, not merely four head labels. HMM hidden states have sequential dependency; binary-tree branches sample in parallel by tree level.
- **Carrying card:** [R05/BIW-0079](../03_reading/R05/BIW-0079.md).
- **Canonical problem records:** [BIP-0171](DETAILED_INVENTORY.md#BIP-0171), [BIP-0172](DETAILED_INVENTORY.md#BIP-0172), [BIP-0173](DETAILED_INVENTORY.md#BIP-0173).
- **Units — input / internal / output / supervision (current):** EvaByte320IDs orbyte-fiedLlama268IDs / STPprefixstates+conditionalprobabilisticcircuits / normalized8/16futurebytejoint / overlapping-windowdiscountedcompositelikelihood; originalSTPverifierseparate.

### Current substantive interface, technique, evidence and limits

### Interfaces and probability

Input/context and generated/supervised events are byte-model token IDs, not learned segment IDs: EvaByte vocabulary 320 (256 bytes plus special symbols); byte-fied Llama vocabulary 268 (Appendix E). A frozen autoregressive single-token head is the target verifier; the auxiliary draft predicts n=8 or 16 future bytes jointly. The proposed conditional circuit maps one context embedding to a normalized n-byte joint. Appendix B: input categoricals sum to one; nonnegative sum-unit softmax weights are normalized; smoothness means all children of each sum have identical variable scope, decomposability means children of a product have disjoint scope. These allow exact marginal/conditional evaluation and ancestral sampling. Fully factorized FF, global latent-mixture CP, time-inhomogeneous HMM and hierarchical binary-tree factorizations encode different dependencies, not merely four head labels. HMM hidden states have sequential dependency; binary-tree branches sample in parallel by tree level.

**Sharing axes (§3.3–3.4):** an n×r×v×d output tensor has separate unembedding parameters indexed by position and mixture component. A fully shared lower Transformer provides representations to target and draft; optional draft-specific LoRA adapters in the last 1/2/4 layers change that axis; verifier remains original. Position/component tying is only suggested as future work in Appendix G, not the experiment. Whether original target input/output embeddings are tied is unspecified. The verifier and draft have separate cache components when adapters require it (Appendix F).

Training uses observed assistant-answer tokens under the Tulu 3 chat template, overlapping future windows and exponentially discounted per-position objectives, with γ=.9 for n>8 (§4.1). It is **composite likelihood of overlapping windows**, not the NLL of one original text chain. The conversion of Llama from a subword model is prior external distillation; its teacher training and conversion resources are not included. KL teacher loss was tested and doubled time/memory with insufficient benefit (Appendix J); proposed main training is not KL distillation.

### Problem / solution / evidence linked to inventory

- [BIP-0171](DETAILED_INVENTORY.md#BIP-0171): Independent future categorical predictions produce incoherent combinations. Introduce normalized latent mixtures and a binary-tree circuit with efficient marginalization and parallel sampling; the 'Cretoria' example is illustrative, not a measured error rate (§§1–3).
- [BIP-0172](DETAILED_INVENTORY.md#BIP-0172): Richer draft distributions can raise accepted candidates but cost more per cycle. EvaByte, n=8, L40S, sampling: FF 176.3±0.9 bytes/s, CP rank 32 191.0±1.6, rank 128 182.3±1.1, despite acceptance 5.19, 5.88, 6.02 respectively (Table 1). n=16 HMM acceptance 6.93 but 168.0 bytes/s versus BTree 6.76 and 199.2 (§4, Appendix K Table 8). EvaByte greedy FF at n=16 reaches 265.4 versus BTree 242.6 bytes/s (Table 11); expressive circuit is not always preferable. Appendix C Table 2: 16-byte FF output projection 21M params; rank-32 BTree ~730M, CP ~671M, so 'small-head' overhead is material.
- [BIP-0173](DETAILED_INVENTORY.md#BIP-0173): Speculative verification trades draft work for preservation of the **target STP model**, not the older EvaByte MTP decoding policy. Algorithm 3 samples the joint, computes prefix marginals and conditional q via ratios, accepts with p/q, and uses normalized max(p−q,0) residual on rejection; Algorithm 2 reuses target shared states and omits a final token under an optimized wrapper whose rejection-residual handling is unclear, but obtains one fallback if none accepted. Claimed greedy identity and sampling-distribution preservation are conditional on matching the actual draft and target conditionals. The paper does not specify proposal temperature/top-p transformation in these algorithms; if any are applied, the ratios must use the transformed actual proposal, and the target's transformations define the preserved policy. Do not independently certify that implementation. EOS is forcibly suppressed, so this is not a variable-length termination benchmark.

### Exposure, cost, counterexamples

§4 and Appendix I: 939,344 Tulu examples; remove 34,067 above 8192 bytes, split remaining 905,277 99/1, train 55 drafts. Head-only 1 epoch then second epoch with LoRA, 2×80GB GPUs, batch 256 ≈2M tokens, Adam fixed 3e-4. English-only prompt/response filter, 250 prompts in each of three sets, batch 1, prefill excluded; main L40S, additional RTX3090, Fig.5 memory BF16/cache-on and 1,024 generated tokens. Main samples have EOS suppressed. Reported best sampling speeds 5.15× EvaByte STP and 2.24× Llama STP; 1.17× best factorized draft, under stated models and device (§4.4). HMM, more LoRA, and larger rank can increase acceptance while decreasing throughput. Training logs/context-filter normalization details and end-to-end first-token, prefill, teacher conversion, serving concurrency, and energy costs remain unknown. PDF §4 Figure 3 caption says Llama sampling is exception to n-extension; Appendix M caption instead says EvaByte greedy; numeric Appendix K Tables 8,11,14,17 are authoritative for the listed settings. No cross-paper inference from 'same in expectation' to identical samples.



**Current R1 adjudication ([FULL_READING_AUDIT_R1](../05_review/FULL_READING_AUDIT_R1.md)):** UNRESOLVED SAMPLING-CONTRACT BOUNDARY: normalized circuits and Algorithm 3 ordinary rejection/residual correction do not certify the optimized shared-state Algorithm 2. The final token can be an optional all-accepted target bonus OR a required post-rejection positive-residual draw. Discarding the latter after a nonempty accepted prefix and restarting from the ordinary target can bias output; retained residual state/actual implementation is unverified. Audit diagnostic p=(.5,.5),q=(.9,.1) at the second position after a deterministic accepted first yields(.7,.3) under literal discard/restart, versus(.5,.5) with residual correction. This is an analyst algebraic counterexample to an unsafe reading, NOT a measured released-code bug. Cite circuit modeling, composite objective and measured throughput under conditions; do NOT cite optimized stochastic target-law preservation as established. Resolve fixed rejection branches/residual carry-over/actual transformed p,q before such a claim; no repeat FULL needed.

**Final R2 / claim-rules adoption** ([CLAIM_RULES](../05_review/CLAIM_RULES.md); [FULL_READING_AUDIT_R2](../05_review/FULL_READING_AUDIT_R2.md)): R2/CLAIM_RULES boundary — MtPC v2 AppendixF: Algorithm3 pp21 lines25–29 draw normalized positive residual when s<n; lines30–31 draw an ordinary target bonus when s=n. Optimized Algorithm2 p20 describes dropping the final verifier token after any acceptance and keeping a shared hidden state, without separating those two roles or specifying retained correction probability state. A literal partial-acceptance discard-and-ordinary-restart interpretation need not preserve the stochastic target law; exact optimized-wrapper preservation remains UNVERIFIED. The analyst two-symbol example yields(.7,.3)rather than(.5,.5)under that interpretation, not an executed sampler or a measured released-code bug. Do not infer greedy mismatch, circuit failure, invalid throughput or actual software bias. Closure needs fixed run-linked branches/state/cache and actual transformed p/q, not a repeatFULL.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; recovery discovery reused, absent old W catalog. No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2511.11346v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Byte (EvaByte or byte-fied Llama) / conditional probability circuit over future window / byte / overlapping-window composite NLL, head training then LoRA. Mixtures/HMM/tree circuits trade expressivity for latency. Exact-greedy and distribution-preserving sampling are claimed relative to verifier; algorithm audit still needed. v1 title Multi-Token vs v2 Multi-Byte: one entity. API lists Lorenzo Loconte absent from extracted HTML author header; full author list not certified here.
- **Learning and causal baseline:** Byte (EvaByte or byte-fied Llama) / conditional probability circuit over future window / byte / overlapping-window composite NLL, head training then LoRA. Mixtures/HMM/tree circuits trade expressivity for latency. Exact-greedy and distribution-preserving sampling are claimed relative to verifier; algorithm audit still needed. v1 title Multi-Token vs v2 Multi-Byte: one entity. API lists Lorenzo Loconte absent from extracted HTML author header; full author list not certified here.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0171](DETAILED_INVENTORY.md#BIP-0171), [BIP-0172](DETAILED_INVENTORY.md#BIP-0172), [BIP-0173](DETAILED_INVENTORY.md#BIP-0173).
- **Reading ownership:** [R05](batches/R05.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N02**, [WORKS](../01_discovery/S03/WORKS.md) line 37: S03-N02 · Fast and Expressive Multi-Byte Prediction with Probabilistic Circuits (2025/2026); [2511.11346v2](https://arxiv.org/html/2511.11346v2), v2 2026-06-02 recovery BYTE N04; P: abstract; selected §2–4 passages, especially loss and verifier; proof/algorithms/complete tables uninspected
  - Original register aliases / era / family / provenance: S03-N02 · Fast and Expressive Multi-Byte Prediction with Probabilistic Circuits (2025/2026); [2511.11346v2](https://arxiv.org/html/2511.11346v2), v2 2026-06-02
  - Source-scoped evidence/depth: recovery BYTE N04; P: abstract; selected §2–4 passages, especially loss and verifier; proof/algorithms/complete tables uninspected

</details>

<a id="BIW-0080"></a>
## BIW-0080 — You should evaluate your language model on marginal likelihood over tokenisations

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Kris Cao and Laura Rimell, “You should evaluate your language model on marginal likelihood over tokenisations,” EMNLP 2021, [official PDF](https://aclanthology.org/2021.emnlp-main.161.pdf), pp. 2104–2114. Aliases S03-N05, S05-R03, S08-W10. **Reading: FULL**, fresh: §§1–6, Figures 1–3, Tables 1–2, pp. 2104–2111; remaining pages references; no appendix in this version. Table 1/2 visually checked on PDF p. 2109. PDF/text retained in `sources/BIW-0080.{pdf,txt}`. Full reading is not reproduction or independent proof.

- **Problem / one-sentence solution:** A canonical segmentation gives only one token-path score for text that admits many segmentations; estimate the sum of neural-model probabilities of compatible segmentations using a probabilistic tokenizer as a proposal, with variance-reduction techniques (§2).
- **Units:** Input is document text and a unigram SentencePiece segmentation lattice; internal/supervised output is left-to-right subword tokens; reported perplexity is normalized by whitespace-delimited words, **not bytes**. The 50,529-piece vocabulary and English/German training are specified, but normalization and EOS/document termination conventions are not explicit enough to certify a lossless raw UTF-8 completed-string event. Their §2 writes a product for document token sequences; do not silently add an EOS factor or infer that all unconstrained neural paths are represented by the proposal lattice.
- **Model/training/causality:** 18-layer Transformer-XL, hidden 1024, pretrained on one-best WMT news tokens, predicts next token from past tokens. In evaluation Transformer-XL cross-segment memory is disabled because of batching with different tokenizations (§4). The paper's repeated-word “memory/caching” is an in-context behavior, not an active Transformer-XL recurrence experiment. Input/output embedding tying and attention-head/layer sharing: not reported in this paper; no separate multi-byte head or verifier.
- **Estimator:** If proposal Q has support over the intended legal tokenizations, ordinary importance sampling averages Pθ(T,D)/Q(T|D) in probability space, unbiased for that sum; taking its log is downward biased in expectation by Jensen and a single random log estimate is **not** guaranteed a deterministic lower bound. Without-replacement sampling uses stochastic beam search, Gumbel perturbations and inclusion probabilities rather than treating selected paths as independent; its corrected probability estimator is the object preceding the log. The authors also forcibly include canonical one-best and discuss bias; n-best sums unweighted distinct path probabilities and is a deterministic lower bound for the full nonnegative sum, but high bias. Exact lattice forward/Viterbi computation supplies Q, not the expensive context-sensitive LM sum (§§2.1–2.2). Restricting samples to one segmentation per repeated whitespace type changes the proposal support; do not call that alone an unbiased estimate over all unconstrained segmentations.
- **Carrying card:** [R04/BIW-0080](../03_reading/R04/BIW-0080.md).
- **Canonical problem records:** [BIP-0109](DETAILED_INVENTORY.md#BIP-0109), [BIP-0272](DETAILED_INVENTORY.md#BIP-0272), [BIP-0273](DETAILED_INVENTORY.md#BIP-0273).
- **Units — input / internal / output / supervision (current):** Documentstrings+unigramSentencePiece lattice / Transformer-XL subwordpositions (evalmemorydisabled) / token-pathprobabilities summed/estimated / existingtokenLM; reportedPPL denominatorwhitespacewords.

### Current substantive interface, technique, evidence and limits

### Contract and method

- **Problem / one-sentence solution:** A canonical segmentation gives only one token-path score for text that admits many segmentations; estimate the sum of neural-model probabilities of compatible segmentations using a probabilistic tokenizer as a proposal, with variance-reduction techniques (§2).
- **Units:** Input is document text and a unigram SentencePiece segmentation lattice; internal/supervised output is left-to-right subword tokens; reported perplexity is normalized by whitespace-delimited words, **not bytes**. The 50,529-piece vocabulary and English/German training are specified, but normalization and EOS/document termination conventions are not explicit enough to certify a lossless raw UTF-8 completed-string event. Their §2 writes a product for document token sequences; do not silently add an EOS factor or infer that all unconstrained neural paths are represented by the proposal lattice.
- **Model/training/causality:** 18-layer Transformer-XL, hidden 1024, pretrained on one-best WMT news tokens, predicts next token from past tokens. In evaluation Transformer-XL cross-segment memory is disabled because of batching with different tokenizations (§4). The paper's repeated-word “memory/caching” is an in-context behavior, not an active Transformer-XL recurrence experiment. Input/output embedding tying and attention-head/layer sharing: not reported in this paper; no separate multi-byte head or verifier.
- **Estimator:** If proposal Q has support over the intended legal tokenizations, ordinary importance sampling averages Pθ(T,D)/Q(T|D) in probability space, unbiased for that sum; taking its log is downward biased in expectation by Jensen and a single random log estimate is **not** guaranteed a deterministic lower bound. Without-replacement sampling uses stochastic beam search, Gumbel perturbations and inclusion probabilities rather than treating selected paths as independent; its corrected probability estimator is the object preceding the log. The authors also forcibly include canonical one-best and discuss bias; n-best sums unweighted distinct path probabilities and is a deterministic lower bound for the full nonnegative sum, but high bias. Exact lattice forward/Viterbi computation supplies Q, not the expensive context-sensitive LM sum (§§2.1–2.2). Restricting samples to one segmentation per repeated whitespace type changes the proposal support; do not call that alone an unbiased estimate over all unconstrained segmentations.

### Findings and limitations

- **[BIP-0109](DETAILED_INVENTORY.md#BIP-0109), [BIP-0272](DETAILED_INVENTORY.md#BIP-0272):** §4.1 evaluates 128 tokenizations/document on multi-host TPU, 15–30 min/dataset; 500 documents per English/German WMT/Wiki set, 500 English CustomNews/arXiv and 200 German mC4. Table 1: English arXiv canonical 179.20 versus 175.87 consistent WOR+1-best and 175.98 n-best; German mC4 194.02 versus 192.84 and 192.21 respectively. Finite-sample estimates can score worse than the single best (e.g. English arXiv consistent WR 176.38 but German mC4 206.89), illustrating variance/support/proposal effects rather than contradiction of a true nonnegative path sum. Training text exposure, model parameter/FLOP totals and TPU count are not reported here.
- **[BIP-0273](DETAILED_INVENTORY.md#BIP-0273):** §4.2/Figure 2 reports document-level Spearman correlation of tokenization entropy with marginal gap 0.57 English, 0.49 German, but large gaps can occur at low entropy. Table 2: on English arXiv, all-word first/same/different-segmentation subsequent losses 9.94/3.97/14.93. This is a conditional observational analysis, not proof that enforcing consistency improves model training. §4.4/Figure 3 finds roughly five candidates dominate an oracle reordering of 128 n-best candidates, not that five arbitrary samples suffice.
- Normalization, de-duplication across paths and explicit final EOS matter for any claimed text probability. This is completed-document marginalization over alternative paths, not BIW-0088's conditional byte-prefix conversion; their different support assumptions must be stated when comparing them.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; recovery discovery reused, absent old W catalog. No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2021.emnlp-main.161.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U text ↔ unigram subword segmentation lattice → Transformer-XL token positions → tokens → next-token pretraining. Evaluation sums/estimates text probability over segmentations; tokenizer proposal, importance sampling, stochastic beam search without replacement. C token-autoregressive; test memory explicitly disabled.
- **Learning and causal baseline:** U text ↔ unigram subword segmentation lattice → Transformer-XL token positions → tokens → next-token pretraining. Evaluation sums/estimates text probability over segmentations; tokenizer proposal, importance sampling, stochastic beam search without replacement. C token-autoregressive; test memory explicitly disabled.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0109](DETAILED_INVENTORY.md#BIP-0109), [BIP-0272](DETAILED_INVENTORY.md#BIP-0272), [BIP-0273](DETAILED_INVENTORY.md#BIP-0273).
- **Reading ownership:** [R04](batches/R04.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N05**, [WORKS](../01_discovery/S03/WORKS.md) line 40: S03-N05 · You should evaluate your language model on marginal likelihood over tokenisations (EMNLP 2021); [formal source](https://aclanthology.org/2021.emnlp-main.161/) recovery BYTE N08; A
  - Original register aliases / era / family / provenance: S03-N05 · You should evaluate your language model on marginal likelihood over tokenisations (EMNLP 2021); [formal source](https://aclanthology.org/2021.emnlp-main.161/)
  - Source-scoped evidence/depth: recovery BYTE N08; A
- **S05/S05-R03**, [WORKS](../01_discovery/S05/WORKS.md) line 42: You should evaluate your language model on marginal likelihood over tokenisations; [EMNLP 2021 original](https://aclanthology.org/2021.emnlp-main.161/); associated arXiv:2109.02550 not version-compared
  - Original register aliases / era / family / provenance: S05-R03
  - Source-scoped evidence/depth: **A**, already recovery N08. Sampling-based string likelihood over alternative tokenizations; larger one-best versus marginal difference reported out of domain. Estimator details, sampling counts, variance and normalization conditions not read.
- **S08/S08-W10**, [WORKS](../01_discovery/S08/WORKS.md) line 41: **You should evaluate your language model on marginal likelihood over tokenisations**, Cao & Rimell; [EMNLP 2021 PDF](https://aclanthology.org/2021.emnlp-main.161.pdf), pp.2104–2114. **P**, §§2–4.4,6; Table 1/2 numerical cells and complete appendix/figure checks not done. Recovery N08 already discovered it.
  - Original register aliases / era / family / provenance: S08-W10 / S08-N08 / **RECOVERY REUSE**
  - Source-scoped evidence/depth: **You should evaluate your language model on marginal likelihood over tokenisations**, Cao & Rimell; [EMNLP 2021 PDF](https://aclanthology.org/2021.emnlp-main.161.pdf), pp.2104–2114. **P**, §§2–4.4,6; Table 1/2 numerical cells and complete appendix/figure checks not done. Recovery N08 already discovered it. 18 layers/1024 hidden, vocabulary 50,529; 128 samples/document, multi-host TPU, 15–30 minutes/dataset; English/German. Up to 1.9% EN-arXiv /0.9% DE-mC4 relative PPL improvement in prose. Denominator whitespace words, not subword tokens. Log-estimator bias and finite-sample cost matter.

</details>

<a id="BIW-0081"></a>
## BIW-0081 — EvaByte: Efficient Byte-level Language Models at Scale

- **Entity / provenance:** official introduction; recovery discovery reused, absent old W catalog. No old global W ID; local aliases below.
- **Full-source target / version:** https://hkunlp.github.io/blog/2025/evabyte/. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Byte+64 specials / dense byte positions with EVA memory slots / byte / average CE of 8 heads. Medusa-like trees for self-speculation; blog does not certify sampling preservation. 6.5B/1.5T bytes; speed caption H800, batch 1, 512 bytes or tokens. Training mix evolved; 5× data-efficiency claim is not equal-data/compute ablation.
- **Learning and causal baseline:** Byte+64 specials / dense byte positions with EVA memory slots / byte / average CE of 8 heads. Medusa-like trees for self-speculation; blog does not certify sampling preservation. 6.5B/1.5T bytes; speed caption H800, batch 1, 512 bytes or tokens. Training mix evolved; 5× data-efficiency claim is not equal-data/compute ablation.
- **Reading status:** O — official introduction, no paper FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0174](DETAILED_INVENTORY.md#BIP-0174), [BIP-0175](DETAILED_INVENTORY.md#BIP-0175).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N06**, [WORKS](../01_discovery/S03/WORKS.md) line 41: S03-N06 · EvaByte: Efficient Byte-level Language Models at Scale (2025); [official introduction](https://hkunlp.github.io/blog/2025/evabyte/) recovery BYTE N09; O: entire returned text, figures not visually read; no immutable revision established
  - Original register aliases / era / family / provenance: S03-N06 · EvaByte: Efficient Byte-level Language Models at Scale (2025); [official introduction](https://hkunlp.github.io/blog/2025/evabyte/)
  - Source-scoped evidence/depth: recovery BYTE N09; O: entire returned text, figures not visually read; no immutable revision established

<a id="BIW-0082"></a>
## BIW-0082 — Blockwise Parallel Decoding for Deep Autoregressive Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Mitchell Stern, Noam Shazeer and Jakob Uszkoreit, [arXiv:1811.03115v1](https://arxiv.org/pdf/1811.03115v1), 7 November 2018; NeurIPS 2018. Alias S03/S03-N10. **Reading: FULL**: all 10 PDF pages, §§1–8, Figures 1–4 and Tables 1–4; the v1 PDF contains no appendix. Graph and table at pp.6/8 checked visually; [PDF](../03_reading/R05/sources/BIW-0082.pdf), [text](../03_reading/R05/sources/BIW-0082.txt). No implementation or independent proof verification.

Machine translation consumes source and emits target **subword tokens**, with EOS; image super-resolution consumes low-resolution images and predicts raster-order R/G/B channel intensities 0–255, not UTF-8 language bytes (§7.2, §7.4). The autoregressive Transformer serves both as sequence model and named scoring verifier p1. At each step offset-specific feed-forward heads propose independent greedy future tokens, then the Transformer scores all proposed positions in parallel using the proposed prior positions and accepts the longest prefix identical to p1 greedy output (§3/Fig.1). For a fixed p1, this exactly recovers its greedy sequence; it is not a stochastic exact-sampling algorithm. With a combined model, verification simultaneously computes next-cycle proposals for all candidate prefixes, avoiding the second full invocation (§4/Fig.2).
- **Carrying card:** [R05/BIW-0082](../03_reading/R05/BIW-0082.md).
- **Canonical problem records:** [BIP-0177](DETAILED_INVENTORY.md#BIP-0177), [BIP-0178](DETAILED_INVENTORY.md#BIP-0178), [BIP-0179](DETAILED_INVENTORY.md#BIP-0179).
- **Units — input / internal / output / supervision (current):** MTsubwords or separateimagechannelvalues / sharedTransformer+offset-specificFFNbranches / greedycandidate tokens throughsharedprojection / sampled-offsetCE andoptionalsequence-levelbeamdistillation.

### Current substantive interface, technique, evidence and limits

### Units and design

Machine translation consumes source and emits target **subword tokens**, with EOS; image super-resolution consumes low-resolution images and predicts raster-order R/G/B channel intensities 0–255, not UTF-8 language bytes (§7.2, §7.4). The autoregressive Transformer serves both as sequence model and named scoring verifier p1. At each step offset-specific feed-forward heads propose independent greedy future tokens, then the Transformer scores all proposed positions in parallel using the proposed prior positions and accepts the longest prefix identical to p1 greedy output (§3/Fig.1). For a fixed p1, this exactly recovers its greedy sequence; it is not a stochastic exact-sampling algorithm. With a combined model, verification simultaneously computes next-cycle proposals for all candidate prefixes, avoiding the second full invocation (§4/Fig.2).

**Sharing axes:** one base Transformer is shared across positions and p1…pk; each output is transformed by a separate branch of an inserted k-output FFN with a residual, then the *same original vocabulary projection* is applied to all heads (§6/Fig.3). Input ↔ output embedding tying is unspecified. Frozen base and backbone fine-tuning are separate conditions. Crucially §7.1 footnote says p1 itself is transformed, even with frozen original weights, so exact output preservation refers to **the modified p1**, not necessarily the original unmodified pretrained baseline; k-dependent BLEU proves that distinction.

Training uses one uniformly selected offset cross-entropy per minibatch, an unbiased estimate of the mean of k losses, instead of computing all at once due to memory. Sequence-level distillation uses beam outputs of a separately pretrained Transformer teacher (same hyperparameters, different seed), not a KL penalty. Extra teacher data generation, student refinement and possibly changed scorer are part of the total method.

### Atomic problem-solution-technique findings

- [BIP-0177](DETAILED_INVENTORY.md#BIP-0177): Serial greedy decoding underutilizes parallel scoring. Propose k outputs in parallel and verify/accept the longest exact-greedy prefix. WMT14 En→De development Table 1: frozen-base regular reaches mean accepted block 1.76, distilled frozen 1.91; exact verification maintains each modified scorer's output, not necessarily original baseline. Single-token fallback is key.
- [BIP-0178](DETAILED_INVENTORY.md#BIP-0178): Multiple plausible continuations reduce agreement of independent heads. Reduce target variation with sequence-level beam distillation, and optionally fine-tune the base. Table 1 both: k=8 gives BLEU 26.11/mean block 4.69; k=10 25.60/4.95. This combines teacher-derived training text and changed scorer; speed-quality trade-off cannot be attributed to heads alone. Frozen-base and fine-tuned conditions have different verifiers.
- [BIP-0179](DETAILED_INVENTORY.md#BIP-0179): Exact greedy agreement trades accuracy for throughput; top-k membership, distance threshold for pixels or hard minimum block each relax it and are **not exact**. Top-2, k=8 yields 25.71 BLEU/5.34 accepted (§7.1); hard minimum causes larger BLEU degradation for small acceptance gain. §7.3/Fig.4 actual single-sentence translation wall time peaks 3.3× at k=8 and ~4.7 accepted; k=10 accepts more but is slower. Image 4× is a separate approximate-pixel case, not a byte-LM measurement.

**Budgets:** WMT14 base Transformer trained 1M steps on eight P100; each expanded model trains an *additional* 1M steps on the same hardware; teacher also requires a separate base training run and beam-generation pass (§7.1). Image base 1M + refinement 250k steps on eight P100. BLEU newstest2013 development and newstest2014 test; Table 4 results mix literature baselines and their own distilled/fine-tuned runs. Exact original text/token counts, parameter counts, precision, cache footprint, prefill and serving load are not fully specified; no universal operation-to-wall-speed equivalence. Image human evaluation Table 3 uses 90% bootstrap intervals and is not direct text quality evidence.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1811.03115v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **Subwords for MT**, image channel intensities elsewhere / shared decoder + FFN heads / same units / CE or distilled sequences. Longest exact-greedy prefix vs approximate top-k are separate; 3.3× MT fastest result has changed model/quality tradeoff.
- **Learning and causal baseline:** **Subwords for MT**, image channel intensities elsewhere / shared decoder + FFN heads / same units / CE or distilled sequences. Longest exact-greedy prefix vs approximate top-k are separate; 3.3× MT fastest result has changed model/quality tradeoff.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0177](DETAILED_INVENTORY.md#BIP-0177), [BIP-0178](DETAILED_INVENTORY.md#BIP-0178), [BIP-0179](DETAILED_INVENTORY.md#BIP-0179).
- **Reading ownership:** [R05](batches/R05.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N10**, [WORKS](../01_discovery/S03/WORKS.md) line 52: S03-N10 · Blockwise Parallel Decoding for Deep Autoregressive Models (2018), Stern/Shazeer/Uszkoreit; [1811.03115v1](https://arxiv.org/html/1811.03115v1) P: §2–6 and selected §7.1/§7.3/§7.4 paragraphs; not full experiment/figure review
  - Original register aliases / era / family / provenance: S03-N10 · Blockwise Parallel Decoding for Deep Autoregressive Models (2018), Stern/Shazeer/Uszkoreit; [1811.03115v1](https://arxiv.org/html/1811.03115v1)
  - Source-scoped evidence/depth: P: §2–6 and selected §7.1/§7.3/§7.4 paragraphs; not full experiment/figure review

</details>

<a id="BIW-0083"></a>
## BIW-0083 — Fast Inference from Transformers via Speculative Decoding

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Yaniv Leviathan, Matan Kalman and Yossi Matias, ICML 2023, PMLR 202, [official PDF](https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf), proceedings pp. 19274–19286. Alias S03-N11. **Reading: FULL**, fresh: paper pp. 1–8, Figures 1–5 and Tables 1–3; Appendix A.1–A.5, pp. 11–13, Tables 4–5 (references pp. 9–10). Visual checks: PDF pp. 6 and 11. Local `sources/BIW-0083.{pdf,txt}`. Full reading is not proof audit or code reproduction.

- **[BIP-0110](DETAILED_INVENTORY.md#BIP-0110):** Serial autoregressive target calls are slow in memory/communication-bound settings; use a cheap proposer to draft a run of tokens, score all draft prefixes with the target Transformer in one parallel pass, and probabilistically correct rejection so the target distribution is preserved (§2, Algorithm 1; Appendix A.1).
- Input/context and outputs are model tokens, not bytes; internal representations are causal Transformer states. Tested GPT-like LM uses BERT tokenization with 8k tokens; T5 encoder–decoder takes source tokens and causally generates target tokens. Supervision is inherited from existing pretrained/fine-tuned model checkpoints; no new loss, distillation or target retraining is required in timing experiments. Distillation and nonautoregressive proposers are possible future alternatives, not tested training methods here. Target and draft share a token space; their weights, embeddings, output projections, and attention heads are not asserted shared. T5-specific embedding tying is not established in this paper.
- With target distribution p and proposer q **after** any desired temperature, top-k, nucleus or argmax transformation, draft x~q; accept with min(1,p(x)/q(x)); at the first rejection draw from normalized positive residual (p−q)+ and discard later drafts. If all γ drafts are accepted, draw one additional target token. This makes 1…γ+1 tokens per target pass. Appendix A.1 proves accepted mass min(p,q) plus rejection mass (p−q)+ = p. q need not cover p: residual handles target-only support; q(x)=0 is never proposed. This is the ideal sampling law, not identical pseudorandom trajectories or guaranteed bitwise equality; finite precision and final EOS/length handling are implementation matters not specified by the proof.
- **Carrying card:** [R04/BIW-0083](../03_reading/R04/BIW-0083.md).
- **Canonical problem records:** [BIP-0110](DETAILED_INVENTORY.md#BIP-0110).
- **Units — input / internal / output / supervision (current):** Genericmodeltokens / cheapdraft+causaltargetprefixstates / target-lawtokens / inheritedpretrainedcheckpoints; exactrejection/residualcorrectionnotnewtrainingobjective.

### Current substantive interface, technique, evidence and limits

### Problem, mechanism and units

- **[BIP-0110](DETAILED_INVENTORY.md#BIP-0110):** Serial autoregressive target calls are slow in memory/communication-bound settings; use a cheap proposer to draft a run of tokens, score all draft prefixes with the target Transformer in one parallel pass, and probabilistically correct rejection so the target distribution is preserved (§2, Algorithm 1; Appendix A.1).
- Input/context and outputs are model tokens, not bytes; internal representations are causal Transformer states. Tested GPT-like LM uses BERT tokenization with 8k tokens; T5 encoder–decoder takes source tokens and causally generates target tokens. Supervision is inherited from existing pretrained/fine-tuned model checkpoints; no new loss, distillation or target retraining is required in timing experiments. Distillation and nonautoregressive proposers are possible future alternatives, not tested training methods here. Target and draft share a token space; their weights, embeddings, output projections, and attention heads are not asserted shared. T5-specific embedding tying is not established in this paper.
- With target distribution p and proposer q **after** any desired temperature, top-k, nucleus or argmax transformation, draft x~q; accept with min(1,p(x)/q(x)); at the first rejection draw from normalized positive residual (p−q)+ and discard later drafts. If all γ drafts are accepted, draw one additional target token. This makes 1…γ+1 tokens per target pass. Appendix A.1 proves accepted mass min(p,q) plus rejection mass (p−q)+ = p. q need not cover p: residual handles target-only support; q(x)=0 is never proposed. This is the ideal sampling law, not identical pseudorandom trajectories or guaranteed bitwise equality; finite precision and final EOS/length handling are implementation matters not specified by the proof.

### Evidence, budget and counterexamples

- §4.1/Table 2: T5 v1.1 XXL 11B target, T5-small 77M, base 250M or large 800M drafts, batch 1, one TPU-v4, compared with T5X on WMT English–German and CNN/DailyMail summarization. Small draft: translation 2.6× at temperature 1 (γ=7, α=.62), 3.4× greedy; summarization 2.3× at temperature 1 (γ=5, α=.53), 3.1× greedy. Larger draft can yield *less* walltime speedup despite higher acceptance: translation greedy base .80/2.8× versus small .75/3.4×. Source/target lengths, training FLOPs and total memory footprint are not specified.
- §3: α is mean distribution overlap, not greedy string match; expected output `(1−α^(γ+1))/(1−α)` assumes i.i.d. acceptance. Walltime formula further assumes enough parallel compute, long outputs, and equal target-pass latency; extra draft and rejected-target arithmetic can increase FLOPs. Memory access to weights and KV cache can shrink, but both models and their caches must be provisioned. Appendix A.3/Table 4 shows prediction/runtime discrepancies from implementation and i.i.d. approximation. Appendix A.5's lenient mode **changes** the output distribution, unlike strict main results.
- §4.2/Table 3 reports 10k target tokens for acceptance only, including 97M GPT-like/6M draft and 137B LaMDA; it is not a 137B measured end-to-end latency result. LaMDA uses top-40 filtering. Results cannot be relabeled byte-serving benchmarks. Independently developed Chen et al. BIW-0084 uses a different distributed 70B setup and reversed p/q notation.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Token LM, no native-byte experiment established / draft+target / token / no retraining required. Exact target-distribution algorithm per abstract; T5-XXL 2–3× is implementation-specific; algorithm/proof not read.
- **Learning and causal baseline:** Token LM, no native-byte experiment established / draft+target / token / no retraining required. Exact target-distribution algorithm per abstract; T5-XXL 2–3× is implementation-specific; algorithm/proof not read.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0110](DETAILED_INVENTORY.md#BIP-0110).
- **Reading ownership:** [R04](batches/R04.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N11**, [WORKS](../01_discovery/S03/WORKS.md) line 53: S03-N11 · Fast Inference from Transformers via Speculative Decoding (2023), Leviathan/Kalman/Matias; [ICML formal](https://proceedings.mlr.press/v202/leviathan23a.html), pp.19274–19286 A
  - Original register aliases / era / family / provenance: S03-N11 · Fast Inference from Transformers via Speculative Decoding (2023), Leviathan/Kalman/Matias; [ICML formal](https://proceedings.mlr.press/v202/leviathan23a.html), pp.19274–19286
  - Source-scoped evidence/depth: A

</details>

<a id="BIW-0084"></a>
## BIW-0084 — Accelerating Large Language Model Decoding with Speculative Sampling

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Charlie Chen, Sebastian Borgeaud, Geoffrey Irving, Jean-Baptiste Lespiau, Laurent Sifre, John Jumper, [arXiv:2302.01318v1](https://arxiv.org/pdf/2302.01318v1), submitted 2 February 2023 ([history](https://arxiv.org/abs/2302.01318)). Alias S03-N12. **Reading: FULL**, fresh: pp. 1–7, Algorithms 1–2, Table 1, Figure 1; supplementary pp. 10–11 Table 2 and Theorem 1 proof; references pp. 8–10. Math damaged by text extraction, so algorithm/proof and tables visually checked against rendered PDF pp. 3, 6, 10–11. Local `sources/BIW-0084.{pdf,txt}`. Full reading is not an independent proof audit, execution or reproduction.

- **[BIP-0110](DETAILED_INVENTORY.md#BIP-0110):** A model-parallel large autoregressive Transformer reloads weights/cache and synchronizes devices per generated token; generate a short cheap draft and score its prefixes together with the large model, then correct rejections to sample from the target law without modifying the target.
- The paper names **q target and p draft**, opposite to Leviathan et al. Algorithm 2 proposes K tokens sequentially from p, evaluates q at K+1 causal prefixes in parallel, accepts each proposed x with min(1,q(x)/p(x)), and at the first rejection samples from normalized max(0,q−p); if all accepted, draws one more q token. Theorem 1 counts accepted mass min(p,q) and rejection mass (q−p)+. No requirement that draft cover every target-supported token; the residual recovers target-only support. Apply nucleus/top-k/temperature to the distributions **before** correction. Correctness is distributional within hardware numerics, not same random seed/trajectory; algorithm's minimum target length could overshoot and EOS/stopping handling is not separately specified.
- Inputs and outputs are model tokens; latent states and KV cache are token-indexed. Draft and target use the same tokenizer and dataset; both use autoregressive training, but exact original exposure and draft optimizer/loss schedule are not reported here. Target 70B Chinchilla is pretrained, while authors train an additional 4B draft, so this work is not training-free as a whole. Input/output embedding tying, attention-head sharing and draft/target parameter sharing are not specified; no multi-byte output head. Sequence-level distillation/multiple heads are discussed alternatives, not their reported 4B experiment.
- **Carrying card:** [R04/BIW-0084](../03_reading/R04/BIW-0084.md).
- **Canonical problem records:** [BIP-0110](DETAILED_INVENTORY.md#BIP-0110).
- **Units — input / internal / output / supervision (current):** Sametokenizer draft/targetmodeltokens / distributed70Btarget+trained4Bdraft / correctedtarget-lawtokens / ARtraining plusdraftthenverify; not bytebenchmark.

### Current substantive interface, technique, evidence and limits

### Problem, technique, units

- **[BIP-0110](DETAILED_INVENTORY.md#BIP-0110):** A model-parallel large autoregressive Transformer reloads weights/cache and synchronizes devices per generated token; generate a short cheap draft and score its prefixes together with the large model, then correct rejections to sample from the target law without modifying the target.
- The paper names **q target and p draft**, opposite to Leviathan et al. Algorithm 2 proposes K tokens sequentially from p, evaluates q at K+1 causal prefixes in parallel, accepts each proposed x with min(1,q(x)/p(x)), and at the first rejection samples from normalized max(0,q−p); if all accepted, draws one more q token. Theorem 1 counts accepted mass min(p,q) and rejection mass (q−p)+. No requirement that draft cover every target-supported token; the residual recovers target-only support. Apply nucleus/top-k/temperature to the distributions **before** correction. Correctness is distributional within hardware numerics, not same random seed/trajectory; algorithm's minimum target length could overshoot and EOS/stopping handling is not separately specified.
- Inputs and outputs are model tokens; latent states and KV cache are token-indexed. Draft and target use the same tokenizer and dataset; both use autoregressive training, but exact original exposure and draft optimizer/loss schedule are not reported here. Target 70B Chinchilla is pretrained, while authors train an additional 4B draft, so this work is not training-free as a whole. Input/output embedding tying, attention-head sharing and draft/target parameter sharing are not specified; no multi-byte output head. Sequence-level distillation/multiple heads are discussed alternatives, not their reported 4B experiment.

### Measurements and boundaries

- Results/Table 1: target Chinchilla 70B (80 layers, width 8192, 64 heads), draft 4B (8 layers, width 6144, 48 heads; supplementary Table 2). Both served on 16 TPU v4s; draft 1.8 ms/token, target baseline 14.1 ms/token. Batch 1, K=4: XSum nucleus p=.8 ROUGE-2 .112→.114, reported 1.92× (7.52 ms/token); greedy .157→.156, 2.01× (7.00 ms/token). HumanEval 100-shot nucleus p=.95, temperature .8: 45.1%→47.0%, 2.46× (5.73 ms/token). Reported 1.92× is not exactly 14.1/7.52; retain published figures without inferring a precision explanation.
- 11,305 XSum generations up to 128 tokens and 16,400 HumanEval generations up to 512 tokens (§Results). Numbers are token generation, not bytes, and task metric agreement cannot independently establish equality of distributions. Model size, hardware and latency are given; training FLOPs, full token-data exposure and memory utilization are not.
- Figure 1: longer lookahead increases loop time, reduces fraction accepted and may increase tail latency variance; XSum nucleus minimizes mean latency at K=3, not universally K=4. A standard 7B draft served on 16 TPUs suffers communication overhead; wider shallow design is tailored to distributed residency. Attention KV reads and all-reduce costs matter; speedup is not guaranteed at large batches or compute saturation. Related Work explicitly describes independent concurrent Leviathan work; preserve both papers as distinct.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2302.01318v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Token draft/target / modified rejection sampling / token / unchanged target. 70B Chinchilla distributed setup 2–2.5×; target law preserved within numerical limits per abstract; no byte-specific speed inference.
- **Learning and causal baseline:** Token draft/target / modified rejection sampling / token / unchanged target. 70B Chinchilla distributed setup 2–2.5×; target law preserved within numerical limits per abstract; no byte-specific speed inference.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0110](DETAILED_INVENTORY.md#BIP-0110).
- **Reading ownership:** [R04](batches/R04.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N12**, [WORKS](../01_discovery/S03/WORKS.md) line 54: S03-N12 · Accelerating Large Language Model Decoding with Speculative Sampling (2023); [2302.01318v1](https://arxiv.org/abs/2302.01318) A
  - Original register aliases / era / family / provenance: S03-N12 · Accelerating Large Language Model Decoding with Speculative Sampling (2023); [2302.01318v1](https://arxiv.org/abs/2302.01318)
  - Source-scoped evidence/depth: A

</details>

<a id="BIW-0085"></a>
## BIW-0085 — Better & Faster Large Language Models via Multi-token Prediction

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/2404.19737. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Abstract generic tokens; exact byte experiments not inspected / shared trunk + independent heads / future units / parallel multi-offset CE. Auxiliary training helps sample efficiency; 13B coding gains and up-to-3× inference remain paper-specific, not normalized byte results.
- **Learning and causal baseline:** Abstract generic tokens; exact byte experiments not inspected / shared trunk + independent heads / future units / parallel multi-offset CE. Auxiliary training helps sample efficiency; 13B coding gains and up-to-3× inference remain paper-specific, not normalized byte results.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0176](DETAILED_INVENTORY.md#BIP-0176).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N13**, [WORKS](../01_discovery/S03/WORKS.md) line 55: S03-N13 · Better & Faster Large Language Models via Multi-token Prediction (2024); [2404.19737v1](https://arxiv.org/abs/2404.19737), 2024-04-30 A
  - Original register aliases / era / family / provenance: S03-N13 · Better & Faster Large Language Models via Multi-token Prediction (2024); [2404.19737v1](https://arxiv.org/abs/2404.19737), 2024-04-30
  - Source-scoped evidence/depth: A

<a id="BIW-0086"></a>
## BIW-0086 — Block Transformer: Global-to-Local Language Modeling for Fast Inference

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/2406.02657. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Tokens, tokenizer details unknown here / fixed global blocks + local token decoder / token / scratch pretraining AR loss inferred only at high level from abstract; exact objective uninspected. 10–20× author throughput claim vs equivalent PPL/tasks; batch/hardware/params need full read.
- **Learning and causal baseline:** Tokens, tokenizer details unknown here / fixed global blocks + local token decoder / token / scratch pretraining AR loss inferred only at high level from abstract; exact objective uninspected. 10–20× author throughput claim vs equivalent PPL/tasks; batch/hardware/params need full read.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0180](DETAILED_INVENTORY.md#BIP-0180).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N14**, [WORKS](../01_discovery/S03/WORKS.md) line 56: S03-N14 · Block Transformer: Global-to-Local Language Modeling for Fast Inference (2024); [2406.02657v2](https://arxiv.org/abs/2406.02657), v2 2024-11-01 A
  - Original register aliases / era / family / provenance: S03-N14 · Block Transformer: Global-to-Local Language Modeling for Fast Inference (2024); [2406.02657v2](https://arxiv.org/abs/2406.02657), v2 2024-11-01
  - Source-scoped evidence/depth: A

<a id="BIW-0087"></a>
## BIW-0087 — Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/2401.10774. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Token / multiple heads + tree attention / token / head-only or joint fine-tuning; self-distillation optional. Medusa-1 frozen vs Medusa-2 changed backbone; typical acceptance not automatically exact sampling. Abstract 2.2× and 2.3–3.6× need matched conditions.
- **Learning and causal baseline:** Token / multiple heads + tree attention / token / head-only or joint fine-tuning; self-distillation optional. Medusa-1 frozen vs Medusa-2 changed backbone; typical acceptance not automatically exact sampling. Abstract 2.2× and 2.3–3.6× need matched conditions.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0181](DETAILED_INVENTORY.md#BIP-0181).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N15**, [WORKS](../01_discovery/S03/WORKS.md) line 57: S03-N15 · Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads (2024); [2401.10774v3](https://arxiv.org/abs/2401.10774), v3 2024-06-14 A
  - Original register aliases / era / family / provenance: S03-N15 · Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads (2024); [2401.10774v3](https://arxiv.org/abs/2401.10774), v3 2024-06-14
  - Source-scoped evidence/depth: A

<a id="BIW-0088"></a>
## BIW-0088 — Exact Byte-Level Probabilities from Tokenized Language Models for FIM-Tasks and Model Ensembles

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Buu Phan, Brandon Amos, Itai Gat, Marton Havasi, Matthew Muckley, Karen Ullrich, [arXiv:2410.09303v2](https://arxiv.org/pdf/2410.09303v2), 11 April 2025 ([version history](https://arxiv.org/abs/2410.09303)). Aliases S03-N16, S08-W18. The v2 PDF itself says “Published as a conference paper at ICLR 2025”; independent page-by-page comparison against the OpenReview proceedings PDF was not completed (OpenReview served a verification wall), so do not assert byte identity with a distinct formal file. **Reading: FULL of locked v2**, fresh: §§1–7 and Figures 1–6, Tables 1–2, Appendix A.1–A.8 and B–E (pp. 1–10 and 13–22; references pp. 11–12). Visual checks pp. 5, 7, 9, 10, 14, 16; other figures considered via captions/extracted text. Local `sources/BIW-0088.{pdf,txt}`. Reading is not independent proof, executable verification, or equivalence certification.

- **[BIP-0111](DETAILED_INVENTORY.md#BIP-0111), [BIP-0278](DETAILED_INVENTORY.md#BIP-0278):** A prompt may end inside the token that would encode a completed string, making canonical-token-prefix conditioning narrower than raw-byte-prefix conditioning; enumerate mutually exclusive token-prefix covers of the raw-byte prefix and use their summed probability to compute the next-byte conditional without retraining (§§2–4).
- The theoretical alphabet includes EOS as a separate symbol (not part of another token), assumed absorbing on termination; text/bytes map losslessly to unique canonical encodings. A cover is a valid token prefix whose last token covers the end of the query and whose earlier tokens stop before it. The byte-prefix event is the disjoint union of covers; `P(next byte | prefix)=P(prefix+byte)/P(prefix)` when the denominator is positive (§4.1, Lemma 1, A.2). The paper's process assumes EOS almost-sure finite termination; positive EOS probability at every step alone need not establish almost-sure termination. Special FIM tokens can be fixed as conditioning events by restricting covers to those beginning with that token prefix (Corollary 1, A.3), but this does not mean the suffix is independently observable to an ordinary left-to-right model: suffix visibility comes from the model's FIM prompt format.
- **Crucial exactness qualification:** A tokenizer-induced true distribution puts zero mass on noncanonical token encodings. Ordinary softmax models can assign positive mass to them. A.6 proposes zeroing provably invalid next-token choices and renormalizing; that improves canonical-token cross entropy under the stated support assumptions **but changes the original neural token distribution**. Thus the canonical-cover algorithm is exact for the assumed/corrected process, not automatically the raw neural model's detokenized distribution with noncanonical paths. §4.2 calls validity checks optional in the incremental step; disabling them is not a universal exactness guarantee. Invalid tokenization means a noncanonical segmentation, **not invalid UTF-8**. Lossy normalization, UNK, independent special tokens and actual vocab/decoder behavior require separate verification.
- **Mechanism/cost:** BPE/MPE cover search scans possible last-token start positions backward and tests `encode(decode(path))==path`; §4.1.1 states at most nℓ model runs for length n and longest token ℓ. Incrementally reuse existing covers and group the next byte of already-covered tokens, adding next-token candidates from the canonical prefix; theoretically one new model inference per generated byte after initialization, plus vocabulary aggregation, tokenizer and cover/cache storage (§4.2, Algorithm 3). No general constant end-to-end time/memory claim follows. A.1 relies on a genuinely fixed pretokenization boundary to cancel unknown initial-token probabilities; not all tokenizers or prefixes have one. Appendix B says an average four-byte token may require four byte decisions; §7 warns about substantial memory. No teacher, new model training or shared output head is required. Head/embedding/layer sharing in the pretrained models is not specified.
- **Units/causality:** Experiments use UTF-8 byte outputs plus control tokens; internal networks and original supervision are autoregressive subword token IDs; byte decision conditions on the raw prefix and only appropriately preceding control tokens. PSM puts suffix before a middle control marker; SPM puts suffix before the unfinished prefix, making mid-token continuation salient (§6.1). The method does not create a native byte-trained architecture.
- **Carrying card:** [R04/BIW-0088](../03_reading/R04/BIW-0088.md).
- **Canonical problem records:** [BIP-0111](DETAILED_INVENTORY.md#BIP-0111), [BIP-0182](DETAILED_INVENTORY.md#BIP-0182), [BIP-0278](DETAILED_INVENTORY.md#BIP-0278).
- **Units — input / internal / output / supervision (current):** UTF-8byteprefix/controltokens / existingcausalsubword LM andcoverstates / correctednext-byteconditional / pretrainednext-tokenmodel, nofurthertraining; canonical-support/corrected-processassumptions explicit.

### Current substantive interface, technique, evidence and limits

### Problem / solution / exact probability object

- **[BIP-0111](DETAILED_INVENTORY.md#BIP-0111), [BIP-0278](DETAILED_INVENTORY.md#BIP-0278):** A prompt may end inside the token that would encode a completed string, making canonical-token-prefix conditioning narrower than raw-byte-prefix conditioning; enumerate mutually exclusive token-prefix covers of the raw-byte prefix and use their summed probability to compute the next-byte conditional without retraining (§§2–4).
- The theoretical alphabet includes EOS as a separate symbol (not part of another token), assumed absorbing on termination; text/bytes map losslessly to unique canonical encodings. A cover is a valid token prefix whose last token covers the end of the query and whose earlier tokens stop before it. The byte-prefix event is the disjoint union of covers; `P(next byte | prefix)=P(prefix+byte)/P(prefix)` when the denominator is positive (§4.1, Lemma 1, A.2). The paper's process assumes EOS almost-sure finite termination; positive EOS probability at every step alone need not establish almost-sure termination. Special FIM tokens can be fixed as conditioning events by restricting covers to those beginning with that token prefix (Corollary 1, A.3), but this does not mean the suffix is independently observable to an ordinary left-to-right model: suffix visibility comes from the model's FIM prompt format.
- **Crucial exactness qualification:** A tokenizer-induced true distribution puts zero mass on noncanonical token encodings. Ordinary softmax models can assign positive mass to them. A.6 proposes zeroing provably invalid next-token choices and renormalizing; that improves canonical-token cross entropy under the stated support assumptions **but changes the original neural token distribution**. Thus the canonical-cover algorithm is exact for the assumed/corrected process, not automatically the raw neural model's detokenized distribution with noncanonical paths. §4.2 calls validity checks optional in the incremental step; disabling them is not a universal exactness guarantee. Invalid tokenization means a noncanonical segmentation, **not invalid UTF-8**. Lossy normalization, UNK, independent special tokens and actual vocab/decoder behavior require separate verification.
- **Mechanism/cost:** BPE/MPE cover search scans possible last-token start positions backward and tests `encode(decode(path))==path`; §4.1.1 states at most nℓ model runs for length n and longest token ℓ. Incrementally reuse existing covers and group the next byte of already-covered tokens, adding next-token candidates from the canonical prefix; theoretically one new model inference per generated byte after initialization, plus vocabulary aggregation, tokenizer and cover/cache storage (§4.2, Algorithm 3). No general constant end-to-end time/memory claim follows. A.1 relies on a genuinely fixed pretokenization boundary to cancel unknown initial-token probabilities; not all tokenizers or prefixes have one. Appendix B says an average four-byte token may require four byte decisions; §7 warns about substantial memory. No teacher, new model training or shared output head is required. Head/embedding/layer sharing in the pretrained models is not specified.
- **Units/causality:** Experiments use UTF-8 byte outputs plus control tokens; internal networks and original supervision are autoregressive subword token IDs; byte decision conditions on the raw prefix and only appropriately preceding control tokens. PSM puts suffix before a middle control marker; SPM puts suffix before the unfinished prefix, making mid-token continuation salient (§6.1). The method does not create a native byte-trained architecture.

### Empirical evidence and counterexamples

- Figure 6 p.9, CodeLlama-7B HumanEval Random Span: SPM token greedy 45.0 vs byte greedy 63.9; pass@10 token 66.5 vs byte 84.3, **+17.8 percentage points**, where @10 is maximum over the plotted temperature sweep; token healing 62.7/83.8 and token alignment 63.0/82.9. PSM token 64.9/84.0 vs byte 65.7/84.1. Thus the headline 18% is not 18% relative and not improvement over healing. Appendix C Table 3: byte beam width 1/2/4 yields SPM 63.9/65.9/66.8 and PSM 65.7/66.8/67.7, with additional KV-cache cost; greedy byte vs greedy token is a different decision policy even if ideal sequence distributions coincide.
- **[BIP-0182](DETAILED_INVENTORY.md#BIP-0182):** Table 1 averages byte distributions of top-2 models with different tokenizers: MMLU 65.4 vs best individual 63.4, PIQA 80.7 vs 80.3. Counterexample GSM8K 55.8 vs Yi-1.5-6B byte 61.5; unequal members can hurt. Table 2 HumanEval top-2 ensemble 42.1 vs best single token score 38.4 (**+3.7 percentage points**), but vs best byte score 36.5 it is +5.6 points; MBPP 53.6 ties best single byte Yi-Coder. These are ensembles with two models and two caches, not free single-model gains. Total GPU time, memory and training data exposure are unreported.
- Figure 2's A/AA/B Markov example gives zero canonical-token continuation A after A although raw prefix A can continue with A. Third-order synthetic GPT-2 6-layer test/Figure 3 approximates planted transitions (100 contexts per last-3-byte state, Appendix A.7); not a large-scale proof. Appendix A.5 considers stochastic BPE dropout, while Appendix E demonstrates greedy alignment can create invalid encodings. Token healing only backs up limited context; Appendix D supplies concrete code failures. No independent validation of the authors' proofs or implementations was performed.



**Current R1 adjudication ([FULL_READING_AUDIT_R1](../05_review/FULL_READING_AUDIT_R1.md)):** R1 probability boundary: cover construction is exact for its stated lossless canonical-support process; mask/renormalization changes a generic raw-softmax LM. Almost-sure termination is an additional assumption, not implied solely by positive EOS hazard at every finite prefix; finite-prefix identity and completed-sequence assumptions are separate.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2410.09303v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Token LM input/internal; UTF-8 byte experiments output; theory uses byte/character interchangeably with declared abstract alphabet. Cover-prefix event sums and incremental next-byte sampling, no retraining. Deterministic tokenizer/valid-encoding and ideal-vs-neural conditions require FULL read; **not interchangeable with unconstrained multi-segmentation marginalization**.
- **Learning and causal baseline:** Token LM input/internal; UTF-8 byte experiments output; theory uses byte/character interchangeably with declared abstract alphabet. Cover-prefix event sums and incremental next-byte sampling, no retraining. Deterministic tokenizer/valid-encoding and ideal-vs-neural conditions require FULL read; **not interchangeable with unconstrained multi-segmentation marginalization**.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0111](DETAILED_INVENTORY.md#BIP-0111), [BIP-0182](DETAILED_INVENTORY.md#BIP-0182), [BIP-0278](DETAILED_INVENTORY.md#BIP-0278).
- **Reading ownership:** [R04](batches/R04.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N16**, [WORKS](../01_discovery/S03/WORKS.md) line 58: S03-N16 · Exact Byte-Level Probabilities from Tokenized Language Models for FIM-Tasks and Model Ensembles (2024/2025); [2410.09303v2](https://arxiv.org/html/2410.09303v2), v2 2025-04-11 P: §3/4 search-located claims, §4.2 full selected passage; proofs, complete experiments and model assumptions uninspected
  - Original register aliases / era / family / provenance: S03-N16 · Exact Byte-Level Probabilities from Tokenized Language Models for FIM-Tasks and Model Ensembles (2024/2025); [2410.09303v2](https://arxiv.org/html/2410.09303v2), v2 2025-04-11
  - Source-scoped evidence/depth: P: §3/4 search-located claims, §4.2 full selected passage; proofs, complete experiments and model assumptions uninspected
- **S08/S08-W18**, [WORKS](../01_discovery/S08/WORKS.md) line 49: **Exact Byte-Level Probabilities from Tokenized Language Models for FIM-Tasks and Model Ensembles**, Phan et al.; [ICLR 2025 formal abstract](https://proceedings.iclr.cc/paper_files/paper/2025/hash/5ed5c3c846f684a54975ad7a2525199f-Abstract-Conference.html), [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/5ed5c3c846f684a54975ad7a2525199f-Paper-Conference.pdf). **A**. Corresponding [arXiv2410.09303v2 abstract](https://arxiv.org/abs/2410.09303v2), 2025-04-11, verified by identical abstract and submission history (v1 2024-10-11). Formal/preprint body differences and full author list not compared; distinct earlier report2406.16829 remains a separate work, with lineage to be checked by full reader.
  - Original register aliases / era / family / provenance: S08-W18 / S08-N16 / **NEW**
  - Source-scoped evidence/depth: **Exact Byte-Level Probabilities from Tokenized Language Models for FIM-Tasks and Model Ensembles**, Phan et al.; [ICLR 2025 formal abstract](https://proceedings.iclr.cc/paper_files/paper/2025/hash/5ed5c3c846f684a54975ad7a2525199f-Abstract-Conference.html), [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/5ed5c3c846f684a54975ad7a2525199f-Paper-Conference.pdf). **A**. Corresponding [arXiv2410.09303v2 abstract](https://arxiv.org/abs/2410.09303v2), 2025-04-11, verified by identical abstract and submission history (v1 2024-10-11). Formal/preprint body differences and full author list not compared; distinct earlier report2406.16829 remains a separate work, with lineage to be checked by full reader. Abstract: Byte-Token Representation Lemma and next-byte sampler; FIM and ensemble applications. Reported 18% improvement's exact metric/relative-vs-absolute meaning and 3.7% ensemble gain not promoted to audited figures. Runtime/exactness conditions require full read.

</details>

<a id="BIW-0089"></a>
## BIW-0089 — Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Marianne Arriola, Aaron Kerem Gokaslan, Justin T. Chiu, Zhihan Yang, Zhixuan Qi, Jiaqi Han, Subham Sekhar Sahoo, Volodymyr Kuleshov, [arXiv:2503.09573v3 PDF](https://arxiv.org/pdf/2503.09573v3), 17 May 2025, ICLR 2025. Alias S03/S03-N17. **Reading: FULL:** §§1–8, limitations and Appendices A–D, PDF pp.1–28; Tables 1–8, figures and masks, with pp.8–9 visually checked. PDF p.1 includes Justin T. Chiu, omitted from fetched HTML header. [PDF](../03_reading/R05/sources/BIW-0089.pdf), [text](../03_reading/R05/sources/BIW-0089.txt). Reading does not independently prove the NELBO derivation or validate code.

**Nonbyte comparator:** LM1B uses bert-base-uncased tokenization, 128-token context; OWT uses GPT-2 tokenizer, 1024 tokens (Appendix C.1). BERT lowercasing/normalization means original-text losslessness is not assumed; GPT-2 tokens are not individual bytes. Input, output and supervision are those tokenizer tokens; internal units are blocks of L′ tokens and masked/noised token states. No direct byte experiment is established.
- **Carrying card:** [R05/BIW-0089](../03_reading/R05/BIW-0089.md).
- **Canonical problem records:** [BIP-0183](DETAILED_INVENTORY.md#BIP-0183).
- **Units — input / internal / output / supervision (current):** LM1BBERTuncasedtokens orOWTGPT2subwords / cleancommittedblocks+maskednoisycurrentblock / denoisedsubwordtokens / blockNELBO(upperboundonNLL), notexactbyteCE.

### Current substantive interface, technique, evidence and limits

### Units and mechanism

**Nonbyte comparator:** LM1B uses bert-base-uncased tokenization, 128-token context; OWT uses GPT-2 tokenizer, 1024 tokens (Appendix C.1). BERT lowercasing/normalization means original-text losslessness is not assumed; GPT-2 tokens are not individual bytes. Input, output and supervision are those tokenizer tokens; internal units are blocks of L′ tokens and masked/noised token states. No direct byte experiment is established.

**Problem/solution:** full-sequence discrete diffusion requires fixed-size generation and cannot directly cache a finalized prefix; factorize the joint autoregressively over blocks and model each block conditional with masked discrete diffusion (§3 Eq.4–6). Blocks see preceding *clean, committed* blocks; positions inside the current noisy block attend bidirectionally to each other, not future clean blocks. During sampling cache finalized preceding blocks, iteratively denoise the current block, then commit. This is not standard left-to-right per-token causal decoding inside a block. One denoiser network is reused across blocks and timesteps; input/output embedding tying unspecified.

The objective is a sum of block negative evidence lower bounds (NELBO), i.e. an upper bound on NLL, estimated using randomly masked within-block tokens; output perplexity is a corresponding upper bound, not exact AR cross entropy (§4, App.A/B). At block length 1, expectation reduces to AR NLL, but the training estimator can have greater gradient variance. Train clean and noisy concatenated copies with a specialized block mask: each token enters twice; vectorized single Transformer pass permits noisy same-block attention and clean *previous-block* attention only (§3.2/App.B.6). Learned clipped mask-rate schedules use grid searches to minimize loss-estimator variance as proxy for gradient variance (§5); clipping is an optimization/sampling-design choice, not proof of exact likelihood equivalence for finite estimators.

### Evidence and BIP-0183

[BIP-0183](DETAILED_INVENTORY.md#BIP-0183) should separate three genuine concerns:

1. **Objective variance:** LM1B L′=1 Table 1: ordinary AR perplexity 22.88, diffusion bound ≤25.56, tuned fully-masked schedule 22.88; random-batch AR 24.37. Table 8: for L′=4, clipped U[.45,.95] gives 29.21, linear gives 30.18, after 3B-token fine-tune; ranges for L′=16 differ. These numbers support a variance/optimization explanation under the setup, not a general causal proof for every diffusion gap.
2. **Quality versus sequential granularity:** OWT Table 4 at 524B tokens: AR 17.54, MDLM ≤22.98, BD3-LM L′=16 ≤22.27, L′=8 ≤21.68, L′=4 ≤20.73. More autoregressive blocks narrow the measured gap but parallelism decreases. All bound values must retain ≤. Table 5 PubMed BD3 ≤42.52 vs AR 48.59, but PTB BD3 ≤96.81 vs AR 81.07; no universal victory.
3. **Generation budgets:** Table 7 (300 samples) at 1024 tokens: AR GPT-2-large generative perplexity 14.1, BD3-LM L′=4 25.7, L′=16 33.4; SSD-LM 37.2 at 40K evaluations vs 281.3 at 1K. BD3 and MDLM use nominal T=5000 diffusion steps and no-remasking cache/first-hitting sampling; reported ≤1000 actual network evaluations for L=1024, not automatically lower wall latency or first-emission delay. SSD-LM 400M parameters / 122B pretraining tokens differs from 110M / 524B for others. Table 6 samples 500 docs: BD3 L′16 median 798, max 9982 versus SEDD capped at 1024. EOS or last-256-token entropy <4 stops long runs; degenerate samples are regenerated for generative perplexity (App.C.5). This filtering affects interpretation. Handling arbitrary user prompts that end mid-block is not specified in the paper; do not invent it.

### Training and costs

Appendix C: 12-layer 768-wide 110M model, 850k standard full-context diffusion pretraining steps + 150k block-diffusion fine-tuning steps; LM1B 65B tokens / 73 epochs, OWT 524B / 60 epochs; batch 512, AdamW 3e-4, hardware 3090/A5000/A6000/A100. Concatenated/wrapped training sequences differ from originally padded comparisons, so authors retrain corresponding baselines; OWT generation experiments avoid artificially inserted context-boundary BOS/EOS. Vectorization yields reported 20–25% **training** speedup relative to two forwards; Appendix B.7 reports A5000 kernel-only speedups and ~15% forward speedup, neither establishes production generation throughput. Sampling uses nucleus p=.9 BD3/AR/MDLM, p=.99 SEDD, p=.95 SSD; corrected 64-bit Gumbels and first-hitting algorithm (C.5). Cache residency, actual end-to-end latency, decoding step granularity and full model-energy budgets remain unreported.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2503.09573v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Generic language tokens; byte experiments unknown / AR blocks + within-block discrete denoising / token / exact variational objective uninspected. Supports flexible length and KV cache per abstract; likelihood estimator not AR CE, streaming latency unknown.
- **Learning and causal baseline:** Generic language tokens; byte experiments unknown / AR blocks + within-block discrete denoising / token / exact variational objective uninspected. Supports flexible length and KV cache per abstract; likelihood estimator not AR CE, streaming latency unknown.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0183](DETAILED_INVENTORY.md#BIP-0183).
- **Reading ownership:** [R05](batches/R05.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N17**, [WORKS](../01_discovery/S03/WORKS.md) line 59: S03-N17 · Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models (2025); [2503.09573](https://arxiv.org/abs/2503.09573), v3 2025-05-17 A
  - Original register aliases / era / family / provenance: S03-N17 · Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models (2025); [2503.09573](https://arxiv.org/abs/2503.09573), v3 2025-05-17
  - Source-scoped evidence/depth: A

</details>

<a id="BIW-0090"></a>
## BIW-0090 — RFC 3629: UTF-8, a transformation format of ISO 10646

- **Entity / provenance:** standard; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://www.rfc-editor.org/rfc/rfc3629.html. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Octets / deterministic UTF-8 validation state / Unicode scalars / none (normative grammar, no learned model).
- **Learning and causal baseline:** No learning or neural causality. Incomplete legal stream prefix differs from complete legal UTF-8 string; buffering implication is analyst guidance, not an RFC LM algorithm.
- **Reading status:** N — selected normative text. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0112](DETAILED_INVENTORY.md#BIP-0112).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S03/S03-N18**, [WORKS](../01_discovery/S03/WORKS.md) line 60: S03-N18 · RFC 3629: UTF-8, a transformation format of ISO 10646 (2003), F. Yergeau; [RFC Editor](https://www.rfc-editor.org/rfc/rfc3629.html) S: §3–4 pp.4–6, §6/§10 selected text
  - Original register aliases / era / family / provenance: S03-N18 · RFC 3629: UTF-8, a transformation format of ISO 10646 (2003), F. Yergeau; [RFC Editor](https://www.rfc-editor.org/rfc/rfc3629.html)
  - Source-scoped evidence/depth: S: §3–4 pp.4–6, §6/§10 selected text
- **S05/S05-U01**, [WORKS](../01_discovery/S05/WORKS.md) line 68: [RFC 3629, UTF-8, a transformation format of ISO 10646](https://www.rfc-editor.org/rfc/rfc3629.html), Yergeau, November 2003; **N**, §§1, 3–4, 7, 10
  - Original register aliases / era / family / provenance: S05-U01
  - Source-scoped evidence/depth: Byte, scalar and legal-sequence definitions; ASCII 00–7F; lead C2–F4 with second-byte restrictions; continuation 80–BF; reject overlong encodings, surrogates and >10FFFF. Grammar/validation are not learned AI techniques or empirical LM quality results.

<a id="BIW-0091"></a>
## BIW-0091 — Normalization of Input-output Shared Embeddings in Text Generation Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Jinyang Liu, Yujia Zhai, Zizhong Chen, [arXiv:2001.07885v2](https://arxiv.org/pdf/2001.07885v2), 24 January 2020. Alias S04/S04-N01. **Reading FULL:** pp.1–7, §§1–5, Equations 1–29, Tables 1–4, Figure 2 and references; PDF pp.4–5 visually checked for formulas, language directions and tables. No appendix in this locked version. No code or learned weight verification.

Problem: tied input/output embeddings cause row magnitude to influence logit as well as direction, possibly biasing generation. Solution: transform shared embedding vectors when used as input/output or add norm-dependent score offsets; compare four geometries in neural translation. Source and target are subword tokens, hidden states continuous vectors, output and supervision target subword tokens with cross-entropy/label smoothing; the decoder is causal given source. Beam search supplies translations, not exact sampling or verification. Word or BPE results are **not byte-head ablations**; token normalization and exact special-symbol/EOS accounting are not specified.
- **Carrying card:** [R08/BIW-0091](../03_reading/R08/BIW-0091.md).
- **Canonical problem records:** [BIP-0194](DETAILED_INVENTORY.md#BIP-0194), [BIP-0195](DETAILED_INVENTORY.md#BIP-0195), [BIP-0196](DETAILED_INVENTORY.md#BIP-0196).
- **Units — input / internal / output / supervision (current):** Joinedortargetsubwordvocab / Transformer/DynamicConvconditionaldecoder / targetsubword / translationCE+labelsmoothing; normalizedsharedbasevectors,notsmallbyte-headtest.

### Current substantive interface, technique, evidence and limits

### Problem, solution and sharing axes

Problem: tied input/output embeddings cause row magnitude to influence logit as well as direction, possibly biasing generation. Solution: transform shared embedding vectors when used as input/output or add norm-dependent score offsets; compare four geometries in neural translation. Source and target are subword tokens, hidden states continuous vectors, output and supervision target subword tokens with cross-entropy/label smoothing; the decoder is causal given source. Beam search supplies translations, not exact sampling or verification. Word or BPE results are **not byte-head ablations**; token normalization and exact special-symbol/EOS accounting are not specified.

Paper notation takes W columns `w_i`; score baseline is `w_iᵀh` with zero bias. Four methods (§2.2):
1. **L2-normalized input and output shared:** `u_i=w_i/||w_i||`; same normalized vector is lookup and classifier. It removes learned input norm as a degree of freedom.
2. **Squared-norm output:** input is raw `w_i`, output `u_i=w_i/||w_i||²`; small norms can amplify logits. Shared base parameters do not mean identical effective input and output vectors.
3. **Squared distance:** raw input/output vectors and dynamic bias yield `w_iᵀh − ||w_i||²/2`, dropping the class-independent `||h||²/2` term.
4. Paper's named **cosine** uses `w_iᵀh/||w_i|| = ||h|| cos(w_i,h)` (Eq.28): rows normalized but **h is not normalized**. Its effective inverse temperature varies with ||h||. Same argmax as full cosine for nonzero h, different softmax probabilities and gradients from fixed-temperature cosine.

WMT and IWSLT De→En use a joined vocabulary and all embedding weights shared; IWSLT Es→En and Ro→En only target decoder input/output embedding is shared (§3.1); distinct encoder/decoder blocks do not thereby share weights. Causal input-output model with Transformer or DynamicConv; label smoothing .1, Adam and beam search are actual methods, not teacher distillation.

### Assumptions and numerical evidence

- **BIP-0194:** §§2.1–2.2 motivate a sparse nonnegative mixture `h=Wα`, `sum α=1`, and iid unit-sphere embedding directions; under these idealizations the cross terms have zero expectation and dominant self-term depends on row norm. This is an explanatory model, not evidence that learned neural hidden states literally lie in that convex hull or that real embeddings are independent. The paper's purported 'convex' relaxation includes an L2 equality constraint, which is generally not a convex feasible set; treat this argument cautiously. Normality of scores is not calibrated probabilities after arbitrary learned hidden states. No claim that norm information is intrinsically harmful.
- **BIP-0195:** WMT16 En→De (4.5M sentence pairs, 32k joint SentencePiece/BPE; Table 1/2) Transformer-big baseline 29.3 BLEU, normalized input 29.9, square output 29.4, distance 29.8, row-normalized 'cosine' 29.7. DynamicConv baseline 29.7, respective 30.2/30.0/29.8/29.9. WMT Transformer dimensions 1024, 6+6 blocks, 16 heads, label smoothing .1; simulated 128-GPU batch 458k with FP16. Reported GPU families RTX 2080Ti/P100/T4, but total hours, seeds, actual runtime overhead and parameter counts not given; paper's near-free overhead claim is analytical O(DV), not a benchmark.
- **BIP-0196:** IWSLT14 Table 3 visually says **De→En**, **Es→En**, **Ro→En**; its prose says English-to-other and is inconsistent. Follow the setup and table rather than silently choosing prose: baseline → square-output 34.30→35.16, 34.24→34.97, 36.90→37.50 BLEU; input-normalized 35.00/34.65/37.09. Table 4 DynamicConv De→En baseline 34.52 vs row-normalized score 34.93. Authors propose lower embedding dimension makes loss of magnitude flexibility matter, but no dimension-controlled ablation establishes this cause.
- Beam width/length penalty: Transformer WMT 4/.6, IWSLT 5/1; DynamicConv WMT 5/.5, IWSLT 4/1; WMT averages 10 checkpoints (§3.2). BLEU alone and no repeated seeds limit statistical confidence. These are translation experiments with task-specific sharing and vocabularies, not evidence for all causal byte LMs.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2001.07885v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** BPE/SentencePiece subword → Transformer/DynamicConv → subword; translation CE + label smoothing
- **Learning and causal baseline:** **Background.** WMT16 En-De32K and IWSLT14, decoder causal. Row normalization, square-normalized output, distance and “cosine” variants distinct; ~0.6 BLEU WMT text claim, table bodies missing. Theory's sparse-mixture/iid-sphere assumptions not certified.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0194](DETAILED_INVENTORY.md#BIP-0194), [BIP-0195](DETAILED_INVENTORY.md#BIP-0195), [BIP-0196](DETAILED_INVENTORY.md#BIP-0196).
- **Reading ownership:** [R08](batches/R08.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N01**, [WORKS](../01_discovery/S04/WORKS.md) line 33: **S04-N01**, 2020, *Normalization of Input-output Shared Embeddings in Text Generation Models*; [v2](https://arxiv.org/html/2001.07885v2) **New**; P §§2.2/3.1–3.2; authors Jinyang Liu, Yujia Zhai, Zizhong Chen from extracted text
  - Original register aliases / era / family / provenance: **S04-N01**, 2020, *Normalization of Input-output Shared Embeddings in Text Generation Models*; [v2](https://arxiv.org/html/2001.07885v2)
  - Source-scoped evidence/depth: **New**; P §§2.2/3.1–3.2; authors Jinyang Liu, Yujia Zhai, Zizhong Chen from extracted text **Background.** WMT16 En-De32K and IWSLT14, decoder causal. Row normalization, square-normalized output, distance and “cosine” variants distinct; ~0.6 BLEU WMT text claim, table bodies missing. Theory's sparse-mixture/iid-sphere assumptions not certified.

</details>

<a id="BIW-0092"></a>
## BIW-0092 — nGPT: Normalized Transformer with Representation Learning on the Hypersphere

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2410.01131v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Token/subword → normalized states → token; next-token CE
- **Learning and causal baseline:** **Background.** Unit input/output vectors plus trainable per-class logit scales; many architectural/optimizer changes. OpenWebText0.5B/1B; steps-to-quality not wall-clock speedup; v1 says step cost +60–80% at long context. Tying not inferred.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0197](DETAILED_INVENTORY.md#BIP-0197), [BIP-0198](DETAILED_INVENTORY.md#BIP-0198).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N02**, [WORKS](../01_discovery/S04/WORKS.md) line 34: **S04-N02**, 2024, *nGPT: Normalized Transformer with Representation Learning on the Hypersphere*; [v1](https://arxiv.org/html/2410.01131v1) **New**; P §§2.1/2.6/3.1; complete author metadata deferred
  - Original register aliases / era / family / provenance: **S04-N02**, 2024, *nGPT: Normalized Transformer with Representation Learning on the Hypersphere*; [v1](https://arxiv.org/html/2410.01131v1)
  - Source-scoped evidence/depth: **New**; P §§2.1/2.6/3.1; complete author metadata deferred **Background.** Unit input/output vectors plus trainable per-class logit scales; many architectural/optimizer changes. OpenWebText0.5B/1B; steps-to-quality not wall-clock speedup; v1 says step cost +60–80% at long context. Tying not inferred.

<a id="BIW-0093"></a>
## BIW-0093 — Breaking the Softmax Bottleneck: A High-Rank RNN Language Model

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1711.03953v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Word → recurrent states → word; next-word likelihood
- **Learning and causal baseline:** **Background.** Mixture of softmaxes addresses log-probability matrix rank constraints; PTB/WikiText2/1BWord reports. No proof of bottleneck in byte model with hidden width≥256; full theorem/ablations unread.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0199](DETAILED_INVENTORY.md#BIP-0199).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N03**, [WORKS](../01_discovery/S04/WORKS.md) line 35: **S04-N03**, 2017/ICLR2018, *Breaking the Softmax Bottleneck: A High-Rank RNN Language Model*; [v3](https://arxiv.org/html/1711.03953v3) **New**; P abstract/introduction only; Yang/Dai/Salakhutdinov/Cohen identity needs complete header recheck
  - Original register aliases / era / family / provenance: **S04-N03**, 2017/ICLR2018, *Breaking the Softmax Bottleneck: A High-Rank RNN Language Model*; [v3](https://arxiv.org/html/1711.03953v3)
  - Source-scoped evidence/depth: **New**; P abstract/introduction only; Yang/Dai/Salakhutdinov/Cohen identity needs complete header recheck **Background.** Mixture of softmaxes addresses log-probability matrix rank constraints; PTB/WikiText2/1BWord reports. No proof of bottleneck in byte model with hidden width≥256; full theorem/ablations unread.

<a id="BIW-0094"></a>
## BIW-0094 — Generating Sentences from a Continuous Space

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1511.06349v4. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Words → global Gaussian latent + LSTM → words; ELBO/reconstruction + prior KL
- **Learning and causal baseline:** **Background.** Full-sentence recognition during training, autoregressive decoder. KL annealing and word dropout; PTB VAE slightly worse than ordinary LM even with nonzero KL. Not deterministic-byte collapse evidence.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0202](DETAILED_INVENTORY.md#BIP-0202), [BIP-0203](DETAILED_INVENTORY.md#BIP-0203).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N06**, [WORKS](../01_discovery/S04/WORKS.md) line 38: **S04-N06**, 2015/2016, Bowman et al., *Generating Sentences from a Continuous Space*; [v4](https://arxiv.org/html/1511.06349v4) **New**; P §3.1/§4; whole generation/appendix unread
  - Original register aliases / era / family / provenance: **S04-N06**, 2015/2016, Bowman et al., *Generating Sentences from a Continuous Space*; [v4](https://arxiv.org/html/1511.06349v4)
  - Source-scoped evidence/depth: **New**; P §3.1/§4; whole generation/appendix unread **Background.** Full-sentence recognition during training, autoregressive decoder. KL annealing and word dropout; PTB VAE slightly worse than ordinary LM even with nonzero KL. Not deterministic-byte collapse evidence.

<a id="BIW-0095"></a>
## BIW-0095 — Improved Variational Autoencoders for Text Modeling using Dilated Convolutions

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1702.08139v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **20K word vocabulary** → Gaussian latent/LSTM recognition → words through causal dilated CNN; ELBO
- **Learning and causal baseline:** **Background.** Yahoo/Yelp100K train,40epochs; receptive fields15/63/125/187. Intermediate capacity optimizes LM vs latent dependence; classification optimum differs. No byte result.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0204](DETAILED_INVENTORY.md#BIP-0204).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N07**, [WORKS](../01_discovery/S04/WORKS.md) line 39: **S04-N07**, 2017, *Improved Variational Autoencoders for Text Modeling using Dilated Convolutions*; [v2](https://arxiv.org/html/1702.08139v2) **New**; P §§2.2–2.3/3.2–3.3; complete author header needs recheck
  - Original register aliases / era / family / provenance: **S04-N07**, 2017, *Improved Variational Autoencoders for Text Modeling using Dilated Convolutions*; [v2](https://arxiv.org/html/1702.08139v2)
  - Source-scoped evidence/depth: **New**; P §§2.2–2.3/3.2–3.3; complete author header needs recheck **Background.** Yahoo/Yelp100K train,40epochs; receptive fields15/63/125/187. Intermediate capacity optimizes LM vs latent dependence; classification optimum differs. No byte result.

<a id="BIW-0096"></a>
## BIW-0096 — Lagging Inference Networks and Posterior Collapse in Variational Autoencoders

- **Entity / provenance:** paper; recovery discovery reused, absent old W catalog. No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1901.05534v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Word-text/image benchmarks (byte not established) → latent posterior → autoregressive units; ELBO
- **Learning and causal baseline:** **Background.** Extra inference updates before generator, controlled by mutual information. Recovery reports2–3× ordinary VAE time; full matching/appendices missing. Do not assume finite-budget dominance.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0205](DETAILED_INVENTORY.md#BIP-0205).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N08**, [WORKS](../01_discovery/S04/WORKS.md) line 40: **S04-N08**, 2019, He et al., *Lagging Inference Networks and Posterior Collapse in Variational Autoencoders*; [v2](https://arxiv.org/abs/1901.05534v2) **Recovery reuse**, LD-N01/global N2; fresh A/history plus prior recovery P
  - Original register aliases / era / family / provenance: **S04-N08**, 2019, He et al., *Lagging Inference Networks and Posterior Collapse in Variational Autoencoders*; [v2](https://arxiv.org/abs/1901.05534v2)
  - Source-scoped evidence/depth: **Recovery reuse**, LD-N01/global N2; fresh A/history plus prior recovery P **Background.** Extra inference updates before generator, controlled by mutual information. Recovery reports2–3× ordinary VAE time; full matching/appendices missing. Do not assume finite-budget dominance.

<a id="BIW-0097"></a>
## BIW-0097 — Bolmo: Byteifying the Next Generation of Language Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Benjamin Minixhofer, Tyler Murray, Tomasz Limisiewicz, Anna Korhonen, Luke Zettlemoyer, Noah A. Smith, Edoardo M. Ponti, Luca Soldaini, Valentin Hofmann. [arXiv 2512.15586v2, 9 February 2026](https://arxiv.org/pdf/2512.15586v2). Alias S04-N09.

**Reading: FULL.** Read PDF pp. 1–20, 29–35: §§1–8, Tables 1–8, Figures 1–9 and Appendices A–F, including rendered Figures 1, 2, 5, 6, 8, 9 and Tables 1, 4, 7. References skimmed. PDF and extracted text in `sources/BIW-0097.*`. Full reading means paper-level evidence, not independent verification, code execution or replication.
- **Carrying card:** [R06/BIW-0097](../03_reading/R06/BIW-0097.md).
- **Canonical problem records:** [BIP-0206](DETAILED_INVENTORY.md#BIP-0206), [BIP-0207](DETAILED_INVENTORY.md#BIP-0207), [BIP-0208](DETAILED_INVENTORY.md#BIP-0208), [BIP-0209](DETAILED_INVENTORY.md#BIP-0209).
- **Units — input / internal / output / supervision (current):** UTF-8bytesPLUSretainedoldsubwordsuffixlookups / localmLSTMstates andselectedvariablepatches+Olmo global / fused512byte/boundaryclasses / boundaryBCE,hostrepresentationmatching,patchprobabilitydistillation,thenbyte/boundaryCE.

### Current substantive interface, technique, evidence and limits

**Reading: FULL.** Read PDF pp. 1–20, 29–35: §§1–8, Tables 1–8, Figures 1–9 and Appendices A–F, including rendered Figures 1, 2, 5, 6, 8, 9 and Tables 1, 4, 7. References skimmed. PDF and extracted text in `sources/BIW-0097.*`. Full reading means paper-level evidence, not independent verification, code execution or replication.

### Interface and training

- **Units:** UTF-8 byte input plus a sparse retained subword-suffix lookup, causal byte encodings, dynamically pooled variable-length latent patches processed by the pretrained Olmo Transformer, next-byte-plus-boundary output; byte and boundary supervision plus teacher subword alignment. Special symbols/termination policy for arbitrary partial-prefix prompts are not fully specified. Not a pure byte-only parameterization: an original subword vocabulary table is retained (§3.1 p.5).
- **Architecture:** byte embedding is added to the longest matching suffix from the old subword input table at each position, using only observed prefix. One local mLSTM+FFN encoder, four local mLSTM+FFN decoder layers, patch-final encoder-state selection, Olmo global decoder, projection/residual depooling. Equal local/global dimensions are 4096 (7B), 2048 (1B); Table 7 p.34. Encoder and decoder are distinct stacks; the old subword **input** table is retained, original **output** table removed, with a new 512-class fused byte/boundary head. No claim of input/output weight tying or local encoder/decoder layer sharing is established by these descriptions. Teacher and student share initialized global weights, not necessarily storage during training.
- **Causality (§3.1.1 pp.7–9, Fig.2):** prefill boundary after byte t compares contextualized t and t+1 using cosine distance of projections, so needs one observed future byte. During autoregressive decoding the separate output head predicts `(next byte, boundary after that byte)` jointly in 512 classes; it does not peek at the as-yet ungenerated next byte. Discrete boundaries receive external supervision. Continuous noncausal boundary scores fed to a smoothed decoder could leak future-byte information; the authors avoid this, not prove all alternative end-to-end schemes unsafe. No speculative verifier.
- **Stage 1 (§3.2.1 pp.9–11):** frozen global model; oracle teacher-token boundaries align patch positions. Boundary binary cross-entropy imitates token ends. Encoder loss compares states after the first **n=4 frozen global layers**, as in model stitching, rather than only static input embeddings; frozen weights still require backward propagation through these layers into the input. Decoder matches the product of probabilities of teacher-forced byte/boundary symbols in each gold patch to the teacher's realized next-token probability using temperature-5 binary cross-entropy, plus byte cross-entropy. Weights boundary/encoder/distillation/CE = 4/1/1/1. The likelihood comparison is patch/path-based; it is not an independent proof of an unmarked text marginal over all segmentations.
- **Stage 2 (§3.2.2):** unfreeze all weights, remove distillation and retain byte+boundary cross-entropy and supervised boundary binary cross-entropy. 9.8B source tokens ≈43.1B bytes stage 1 plus 39.3B ≈172.9B bytes stage 2, not just 39.3B total conversion exposure. Dolma 3 mixture ≈172B tokens, <1 epoch per run, and 75M synthetic character-task tokens drawn from 150k words with no CUTE test-word overlap (Appendix C). Stage 1 75k steps, stage 2 150k, H100 throughput Table 8 p.35; original teacher pretraining and upstream checkpoint costs additional.

### Distinct problem → solution → evidence

1. **[BIP-0206](DETAILED_INVENTORY.md#BIP-0206):** matching a static token vector need not match its downstream functional effect → route alignment gradients through the first four frozen host layers and match their representations, using oracle segment positions; n=0 is static-vector matching. The text (§3.2.1) reports n=4 substantially better; no numerical n-sweep table is given here.
2. **[BIP-0207](DETAILED_INVENTORY.md#BIP-0207):** a narrow linear-up-projected encoder imposes a hard rank ceiling → make local and global widths equal. Appendix E/Fig.9 shows broad spectral structure in several input/output tables, with Qwen3-4B input an exception; concatenation has no identical hard limit. Rank argument does not isolate all causes of performance.
3. **[BIP-0208](DETAILED_INVENTORY.md#BIP-0208):** random byte interfaces risk destructive updates and expensive iteration → learn interfaces before end-to-end updates. §6.2/Fig.6 gives a key counterexample: without stage 1, training is **not catastrophic**. Equalize approximately global FLOPs by adding 6.5B tokens, +17% of 39.3B, to stage-2-only; stage 1 helps especially 1B, gap narrows. It does **not** equalize optimizer-state memory, scheduling or fully measured compute.
4. **[BIP-0209](DETAILED_INVENTORY.md#BIP-0209):** aligned backbone parameters alone need not imply post-training compatibility → add a source model's task vector to matching global layers only. §5.2/Fig.4 reports IFEval 31.1→67.4 versus source RL-zero 66.9; requires base-input/base-output embedding compatibility, because local byte modules are not transferred. Appendix D/Fig.8 tests embedding resets on Tulu-3 loss, showing conspicuous failures (including OLMo-2 1B Instruct and some SFT/DPO/Gemma); size correlation R²=0.05, so not a reliable universal pass.

### Results, controls and limits

Table 1 p.13: Bolmo 7B 7.63B total vs Olmo 3 7.30B, BLT 10.55B; CUTE 78.6 vs 56.9, EXECUTE 71.6 vs 55.1; HumanEval pass@1 40.6 vs 49.0, pass@16 74.7 vs 71.1; math aggregate 48.9 vs 55.3. Code sampling temperature 0.6/top-p 0.6; pass@16 improvement does not establish inherent diversity advantage. Table 4 p.30 continued Olmo on the same mix scores CUTE 72.9; synthetic training is a material confound, though controlled comparison remains favorable to Bolmo. At 1B, BLT includes 4.53B total parameters and remains slightly stronger on average (§5). Appendix A Table 3: oracle versus learned boundaries and boundary-type comparisons help distinguish representation and routing errors.

§5.1/Fig.3 increases compression by supervised per-example BPE, entropy or cross-entropy merges; BPE performed better, but the 370M auxiliary LM was trained on 74.3B tokens and entropy/CE use it at training, not inference. Desired and realized compression differ. Figure 7/§6.3: batch 1 H100, about 125 vs 150 bytes/s at similar compression and 1s vs 0.8s on 72K-byte prefill; Bolmo overtakes near 6.6 bytes/patch, with quality tradeoffs and no batched-serving validation. Original-text context, teacher inference and GPU costs differ across baselines; random seeds and full training FLOPs are not fully reported. Do not infer a guaranteed win across domains or hardware.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2512.15586v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Byte (+ boundary mark or fused byte/boundary class) → local byte/global patch → byte/boundary; subword-boundary BCE, representation matching, patch-likelihood distillation, CE
- **Learning and causal baseline:** Source global checkpoint frozen stage1 then unfrozen; future byte for prefill boundary vs separately predicted output boundary. ~43B bytes stage1 +173B stage2,1B/7B. Approximate FLOP-matched stage2-only ablation not catastrophic. Full generation causality proof/table checks pending.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0206](DETAILED_INVENTORY.md#BIP-0206), [BIP-0207](DETAILED_INVENTORY.md#BIP-0207), [BIP-0208](DETAILED_INVENTORY.md#BIP-0208), [BIP-0209](DETAILED_INVENTORY.md#BIP-0209).
- **Reading ownership:** [R06](batches/R06.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N09**, [WORKS](../01_discovery/S04/WORKS.md) line 41: **S04-N09**, 2025/2026, Minixhofer et al., *Bolmo: Byteifying the Next Generation of Language Models*; [v2](https://arxiv.org/html/2512.15586v2) **New**; P §3.2, §5.2/§6.2, Appendix E paragraph; later Nature version not compared
  - Original register aliases / era / family / provenance: **S04-N09**, 2025/2026, Minixhofer et al., *Bolmo: Byteifying the Next Generation of Language Models*; [v2](https://arxiv.org/html/2512.15586v2)
  - Source-scoped evidence/depth: **New**; P §3.2, §5.2/§6.2, Appendix E paragraph; later Nature version not compared Source global checkpoint frozen stage1 then unfrozen; future byte for prefill boundary vs separately predicted output boundary. ~43B bytes stage1 +173B stage2,1B/7B. Approximate FLOP-matched stage2-only ablation not catastrophic. Full generation causality proof/table checks pending.

</details>

<a id="BIW-0098"></a>
## BIW-0098 — Distilling Token-Trained Models into Byte-Level Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Zishuo Bao, Jiaqi Leng, Junxiong Wang, Bowen Peng, Yucheng Lu. [arXiv 2602.01007v1, 1 February 2026](https://arxiv.org/pdf/2602.01007v1). Alias S04-N10.

**Reading: FULL.** Entire 17-page PDF, §§1–8, Tables 1–13, Figures 1–3 and Appendices A–E; visually checked pp.4, 7, 15, 17. Source and text: `sources/BIW-0098.*`. This is a full paper reading, not code validation or reproduction.
- **Carrying card:** [R06/BIW-0098](../03_reading/R06/BIW-0098.md).
- **Canonical problem records:** [BIP-0210](DETAILED_INVENTORY.md#BIP-0210), [BIP-0211](DETAILED_INVENTORY.md#BIP-0211), [BIP-0212](DETAILED_INVENTORY.md#BIP-0212).
- **Units — input / internal / output / supervision (current):** UTF-8bytes / Mamba2byteencoder,learnedchunks,pretrainedTransformer / stage1teachersubwords,stage2byte/boundarytags / sequentialembeddingL2,tokenKL,boundaryBCE,thenbyteCE.

### Current substantive interface, technique, evidence and limits

**Reading: FULL.** Entire 17-page PDF, §§1–8, Tables 1–13, Figures 1–3 and Appendices A–E; visually checked pp.4, 7, 15, 17. Source and text: `sources/BIW-0098.*`. This is a full paper reading, not code validation or reproduction.

### Units, model, timing and training

UTF-8 byte input; Mamba2 encoder; learned variable-length byte chunks; pretrained causal Transformer global states; Stage 1 produces **teacher-vocabulary subwords**, Stage 2 produces bytes plus boundary tags. The labels include token embeddings, token distributions, token-end boundaries and next byte, sequentially (§§3–4). It is not byte-output generation during Stage 1. Four-layer Mamba2+FFN local encoder and decoder, 1536 width, Table 12 p.16; global teacher initialized from Llama-3.2 3B, Qwen-3 4B or OLMo-2 1B. Teacher token head initializes Stage 1 and is replaced in Stage 2; no evidence of local encoder–decoder weights or output/embedding tying; MBP auxiliary and primary heads are separate in role, their parameter tying is unspecified.

Prefill router compares state at current byte with the next byte, giving a token-end probability (§4.1.1). To avoid future-byte leakage on generation, Joint Boundary Prediction (JBP) predicts 512 `(byte, boundary)` classes at each step. Alternative MBP predicts x[t+1] and x[t+2] in parallel; the latter's predicted embedding is a proxy for the next state used to decide the former's boundary. This is not access to the true future nor an exact verifier. Shifted upsampling exposes a completed chunk's global state only at its final byte; earlier bytes use the previous chunk (or learned NULL). Details of actual sample-versus-argmax policy, EOS, and partial-prompt termination are not supplied.

Stage 1: first minimize squared distance between the encoder's token-final state and static teacher token embedding; next train encoder plus backbone using teacher-forced token-distribution KL at teacher boundaries; finally freeze backbone and train router against teacher boundary binary labels. FineWeb 30B bytes (~7B tokens), three phases; Stage 2 adds 95B bytes: first fit fresh dechunk/decoder while backbone is frozen, then unfreeze all and train next-byte objective. Total 125B bytes excludes original teacher pretraining, online teacher passes and optional post-training. AdamW, cosine schedule, 8192-byte sequences and batch 256; Appendix E Table 13 records per-phase rates. No total accelerator-hours, number of seeds, or teacher generation costs stated.

### Atomic inventory findings

1. **[BIP-0210](DETAILED_INVENTORY.md#BIP-0210)** — Problem: embedding, token-distribution and boundary objectives couple representations at different resolutions and may compete. Solution: a three-phase curriculum separates those tasks before byte output adaptation. §6.1/Table 3 equal-exposure 20B-byte comparison: 10B alignment + 10B joint distillation vs 20B direct distillation, same specified learning rates; LMB 70.7 vs 31.2, HellaSwag 73.6 vs 46.7. This is severe **within this configuration**, not a theorem that pre-alignment is universally required: Bolmo's different stage-2-only experiment is noncatastrophic. The paper asserts competing-gradient instability but does not provide a gradient-conflict measurement.
2. **[BIP-0211](DETAILED_INVENTORY.md#BIP-0211)** — Problem: input byte adaptation can retain dependence on a subword classifier. Solution: substitute dechunking and a new local byte decoder and then unfreeze, explicitly distinguishing the stages. Table 1 p.6 Llama teacher/Stage1/Stage2 MMLU 56.0/51.6/51.8, Qwen 73.0/66.8/68.5; Stage 1 is token-output, so its apparently good retention is not a complete byte-to-byte result. Cross-paper baseline training sets, base models and total compute vary.
3. **[BIP-0212](DETAILED_INVENTORY.md#BIP-0212)** — Problem: prefill lookahead is unavailable when emitting a new byte. Solution: classify the byte+boundary jointly, or approximate future context using a second byte head. Table 4 p.7 Qwen JBP vs MBP GSM8K 53.5 vs 37.4, while MMLU 68.4 vs 69.2; this does not prove all multi-byte approaches fail long reasoning. §6.3/Table 5 Mamba2 vs matched-size Transformer encoder MMLU 70.2 vs 31.3 under the stated alignment setup; author's causal explanation is hypothesis, not isolated mechanism proof.

### Other evidence and counterexamples

Table 1 claims Llama Stage 2 average drop 2.80 vs teacher, compared with reported H-Net 9.85 and BLT 7.34, but the latter have different teacher, model sizes and training recipes. Appendix D/Table 11 is a materially less favorable direct 1B-family comparison: Stage 2 average 58.1, Bolmo 60.3, BLT 62.8; 1B parameter accounting and data differ. Table 2 adds on-policy distillation from Llama-3.2 3B Instruct with 77k Tulu prompts to the **Stage 1** model, MMLU 52.52→54.64; not an end-to-end byte generation result.

Appendix A/Table 6: Llama original/Stage1/Stage2 HellaSwag clean 73.76/72.90/71.20 and noise average 54.10/53.29/51.40; per-noise Stage 1 can improve but aggregate does not. Whitespace-penalty boundary training reduces clean 73.76 to 58.50 despite smaller clean/noisy gap (Table 7); Figure 3 shows boundaries near spaces. Robustness score definition in Eq.5 and Table 6 caption's harmonic-mean wording conflict; do not treat this metric as unambiguous. Appendix B Table 9 split vs integrated router LMB 39.1 vs 58.7; architectural capacity is confounded. Appendix C Table 10 larger teachers do not uniformly help: Qwen 4B Stage1 ARC-C 50.9 with same-size teacher vs 54.8 with 8B, while MMLU 71.9 vs 71.4. This contradicts the appendix's blanket claim of decline across all metrics.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2602.01007v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Byte → H-Net-like states → **subwords stage1**, then byte or joint byte/boundary stage2; embedding L2, token KL, boundary BCE, byte CE
- **Learning and causal baseline:** Sequential alignment→joint distillation→frozen-backbone boundary learning; head-only adaptation→end-to-end.30B+95B bytes; Llama/Qwen/OLMo families. Causal shift/lookahead strategy requires deeper audit. Claimed loss competition not a measured gradient-cosine history.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0210](DETAILED_INVENTORY.md#BIP-0210), [BIP-0211](DETAILED_INVENTORY.md#BIP-0211), [BIP-0212](DETAILED_INVENTORY.md#BIP-0212).
- **Reading ownership:** [R06](batches/R06.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N10**, [WORKS](../01_discovery/S04/WORKS.md) line 42: **S04-N10**, 2026, Leng et al., *Distilling Token-Trained Models into Byte-Level Models*; [v1](https://arxiv.org/html/2602.01007v1) **New**; P §4.1–4.2/§5 setup/§6 descriptions; appendix/results incomplete
  - Original register aliases / era / family / provenance: **S04-N10**, 2026, Leng et al., *Distilling Token-Trained Models into Byte-Level Models*; [v1](https://arxiv.org/html/2602.01007v1)
  - Source-scoped evidence/depth: **New**; P §4.1–4.2/§5 setup/§6 descriptions; appendix/results incomplete Sequential alignment→joint distillation→frozen-backbone boundary learning; head-only adaptation→end-to-end.30B+95B bytes; Llama/Qwen/OLMo families. Causal shift/lookahead strategy requires deeper audit. Claimed loss competition not a measured gradient-cosine history.

</details>

<a id="BIW-0099"></a>
## BIW-0099 — Cross-Tokenizer LLM Distillation through a Byte-Level Interface

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Avyav Kumar Singh, Yen-Chen Wu, Alexandru Cioba, Alberto Bernacchia and Davide Buffelli. [arXiv 2604.07466v1, 8 April 2026](https://arxiv.org/pdf/2604.07466v1). Alias S04-N11.

**Reading: FULL.** Full 13-page PDF, §§1–6, Tables 1–4, Figures 1–4 and Appendices A–C; visual inspection of pp.7, 12–13 confirmed tables/plots. `sources/BIW-0099.pdf` and `.txt`. Reading does not establish theorem, implementation, published checkpoint or reproduction correctness.
- **Carrying card:** [R06/BIW-0099](../03_reading/R06/BIW-0099.md).
- **Canonical problem records:** [BIP-0213](DETAILED_INVENTORY.md#BIP-0213), [BIP-0214](DETAILED_INVENTORY.md#BIP-0214).
- **Units — input / internal / output / supervision (current):** Student-tokenizedtext (ordinaryCTD); separateBPE→byteexperiment / studenttokenprefixstates+temporary10parallelbyteheads / normalstudenttokens,byteonlyintransfercase / tokenCE+approxteacherbyteKL+byteCE;260vs261classsource conflict.

### Current substantive interface, technique, evidence and limits

**Reading: FULL.** Full 13-page PDF, §§1–6, Tables 1–4, Figures 1–4 and Appendices A–C; visual inspection of pp.7, 12–13 confirmed tables/plots. `sources/BIW-0099.pdf` and `.txt`. Reading does not establish theorem, implementation, published checkpoint or reproduction correctness.

### Interface and precise mechanism

Ordinary deployment takes student-tokenized input, Transformer states and a student-token output distribution; a **temporary** byte interface supplies intermediate training supervision and is normally removed. A separate BPE→byte tokenizer-transfer experiment replaces input/output token tables and does deploy a byte-vocabulary token model; do not conflate that case with ordinary cross-tokenizer transfer. Teacher/student tokenizers can normalize irreversibly (§3.1 footnote); reversibility is an assumption, not an established universal property. The paper does not fully specify special-symbol mappings, EOS accounting or arbitrary partial-prefix handling.

[**BIP-0213**](DETAILED_INVENTORY.md#BIP-0213): mismatched token vocabularies cannot be directly logit-KL matched → approximate teacher's conditional byte distribution by summing compatible tokenization paths, then KL-match student byte predictions. §3.1 eqs.2–3 define byte-prefix coverings; §3.2/Fig.1 uses 10 **parallel** position-specific linear projections from one causal student token-prefix state, with token CE + byte CE + byte KL. These heads do not see previously *sampled* within-token bytes; teacher conditionals do use observed earlier bytes, so the student training interface is not an exact sequential byte model. Tokens exceeding ten bytes get only their first ten supervised. Teacher distributions are beam/pruning approximations, not automatically exact raw-byte probabilities. A naive student-token probability projection would require a teacher query for each vocabulary candidate and compound approximation error.

Q/V rank-64 LoRA is described in §4, while Appendix B Table 4 explicitly lists Q, K, V, O, gate, up and down projections; this is an unresolved source contradiction, not grounds to report one as the actual verified run. Likewise §4 states ten 260-class heads (256+4 special), Appendix B Table 4 says 261. Ten heads are separate positions; any weight sharing among them, between byte and token heads, or input and token output tables is unspecified. FVT initializes transferred tables by copying shared tokens, averaging source decompositions and Gaussian fallback; no claim this makes input/output tied. Backbone is frozen except LoRA; classifier/embedding training permissions described at high level but actual parameter counts and checkpoint aliasing are unverified.

### Results and budgets

[**BIP-0214**](DETAILED_INVENTORY.md#BIP-0214): byte supervision can transfer some knowledge without reliably retaining instruction behavior → compare same-recipe alternatives and separately test actual byte-vocabulary conversion. Table 1 p.7 Llama-3.2 3B Instruct→Qwen2 tokenizer: original IFEval 66.31, BLD 30.58, MinED 62.83, ALM+SFT 58.51; BLD PiQA 75.68 versus original 75.46 and AGI-ZH 35.97 versus original 42.93. Table 2 actual →byte: original vs BLD MMLU 60.50 vs 39.06, IFEval 66.31 vs 25.43, PiQA 75.46 vs 67.52; multiple baselines degrade. Table 3 heterogeneous OpenMath-Llama3.1-8B→Gemma2 2B: GSM8K 62.55±1.33 BLD vs 59.29±1.35 SFT and teacher 87.26±0.92; MATH BLD 20.08±1.82 vs SFT 22.40±1.87, zero-shot chain-of-thought. Values ± are reported uncertainties; seed count not identified. These comparisons do not establish dominance or model-level causal explanations.

Appendix C beam K=10, relative pruning ε=0.01: Jensen–Shannon divergence 0.0045 from K=100, ε=10⁻⁶ **reference**, not a proven exact distribution. At four RTX 3090, 100–150 byte samples ~10.4s/sample and complete Tulu-3 teacher-probability precomputation ~2 days; storage and total GPU energy unknown. Table 4: five epochs, per-device batch 2, four gradient-accumulation steps, sequence 512, AdamW LR 2e-5, 1000 warmup, KL weight .1 and byte CE weight 1. Tulu-3 SFT for tokenizer-transfer, OpenMathInstruct-2 for math; the number of unique original bytes and total student/teacher FLOPs are not given. Appendix A's byte-head-only training/validation losses decline; this is not proof of exact within-token dependency modeling. Figure 3–4 are sensitivity plots, not a zero-error certificate.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2604.07466v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Subword input/state/output in principal CTD; auxiliary **260-class byte** heads; BPE→byte transfer separate
- **Learning and causal baseline:** CE(token)+CE(byte)+KL(byte),10 parallel linear heads predict≤10 bytes/token, discarded normally. Rank64 Q/V LoRA,1B–8B models; Tulu3/OpenMath. Teacher byte distribution approximated; large BPE→byte quality losses. Not fully joint autoregressive byte distribution for auxiliary future heads.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0213](DETAILED_INVENTORY.md#BIP-0213), [BIP-0214](DETAILED_INVENTORY.md#BIP-0214).
- **Reading ownership:** [R06](batches/R06.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N11**, [WORKS](../01_discovery/S04/WORKS.md) line 43: **S04-N11**, 2026, *Cross-Tokenizer LLM Distillation through a Byte-Level Interface*; [v1](https://arxiv.org/html/2604.07466v1) **New**; P §3.2/§4 Tables1–3/§5 and Appendix A description
  - Original register aliases / era / family / provenance: **S04-N11**, 2026, *Cross-Tokenizer LLM Distillation through a Byte-Level Interface*; [v1](https://arxiv.org/html/2604.07466v1)
  - Source-scoped evidence/depth: **New**; P §3.2/§4 Tables1–3/§5 and Appendix A description CE(token)+CE(byte)+KL(byte),10 parallel linear heads predict≤10 bytes/token, discarded normally. Rank64 Q/V LoRA,1B–8B models; Tulu3/OpenMath. Teacher byte distribution approximated; large BPE→byte quality losses. Not fully joint autoregressive byte distribution for auxiliary future heads.

</details>

<a id="BIW-0100"></a>
## BIW-0100 — Nested Byte-Level Vocabularies Are Cheap to Deploy and Expensive to Share: A Pre-Registered Negative Result

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2608.28151v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **Byte-level BPE subwords** caps2048/8192/32768 → shared Transformer → capped subwords; CE
- **Learning and causal baseline:** 3.1M/10.6M body,200M tokens/run,30models. Embedding/head untied by design; abstract/body report tie sensitivity better at every cap but table details not checked. Multi-cap sharing vs input/output tying are different axes; exact sliced logits ≠ equal quality.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0215](DETAILED_INVENTORY.md#BIP-0215).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N12**, [WORKS](../01_discovery/S04/WORKS.md) line 44: **S04-N12**, 2026, *Nested Byte-Level Vocabularies Are Cheap to Deploy and Expensive to Share: A Pre-Registered Negative Result*; [v1](https://arxiv.org/html/2608.28151v1) **New**; P §§II–VI text; extracted author metadata absent
  - Original register aliases / era / family / provenance: **S04-N12**, 2026, *Nested Byte-Level Vocabularies Are Cheap to Deploy and Expensive to Share: A Pre-Registered Negative Result*; [v1](https://arxiv.org/html/2608.28151v1)
  - Source-scoped evidence/depth: **New**; P §§II–VI text; extracted author metadata absent 3.1M/10.6M body,200M tokens/run,30models. Embedding/head untied by design; abstract/body report tie sensitivity better at every cap but table details not checked. Multi-cap sharing vs input/output tying are different axes; exact sliced logits ≠ equal quality.

<a id="BIW-0101"></a>
## BIW-0101 — Kronecker Embeddings: Byte-Level Structured Token Representations for Parameter-Efficient Language Models

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2605.29459v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **BPE token positions**, deterministic constituent-byte/position encoder → projected token vectors → token head; LM objective
- **Learning and causal baseline:** Mixed interface. Abstract reports3seed nanoGPT124M/2.5B tokens,91–94% frontier input-side saving; not whole-model reduction. Geometry/output-head capacity controls and byte-similar semantic confusions require full reading.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0216](DETAILED_INVENTORY.md#BIP-0216).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N13**, [WORKS](../01_discovery/S04/WORKS.md) line 45: **S04-N13**, 2026, *Kronecker Embeddings: Byte-Level Structured Token Representations for Parameter-Efficient Language Models*; [v1](https://arxiv.org/abs/2605.29459v1) **New**; A, Rohan Shravan metadata from submission; full author header unverified
  - Original register aliases / era / family / provenance: **S04-N13**, 2026, *Kronecker Embeddings: Byte-Level Structured Token Representations for Parameter-Efficient Language Models*; [v1](https://arxiv.org/abs/2605.29459v1)
  - Source-scoped evidence/depth: **New**; A, Rohan Shravan metadata from submission; full author header unverified Mixed interface. Abstract reports3seed nanoGPT124M/2.5B tokens,91–94% frontier input-side saving; not whole-model reduction. Geometry/output-head capacity controls and byte-similar semantic confusions require full reading.

<a id="BIW-0102"></a>
## BIW-0102 — Super Tiny Language Models

- **Entity / provenance:** paper (proposal-only); new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2405.14159v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Proposed byte→BPE-delimited pooled states→byte-per-next-BPE-token
- **Learning and causal baseline:** **Research proposal, not completed empirical tying counterexample.** Weight sharing and LoRA FFN adaptation proposed;90–95% parameter claim cannot be cited as achieved byte LM result.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** none — proposal screened, not counted as an achieved mechanism/result.
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N14**, [WORKS](../01_discovery/S04/WORKS.md) line 46: **S04-N14**, 2024, Hillier et al., *Super Tiny Language Models*; [v1](https://arxiv.org/html/2405.14159v1) **New, screened only; no inventory row**; P §§4–5/conclusion
  - Original register aliases / era / family / provenance: **S04-N14**, 2024, Hillier et al., *Super Tiny Language Models*; [v1](https://arxiv.org/html/2405.14159v1)
  - Source-scoped evidence/depth: **New, screened only; no inventory row**; P §§4–5/conclusion **Research proposal, not completed empirical tying counterexample.** Weight sharing and LoRA FFN adaptation proposed;90–95% parameter claim cannot be cited as achieved byte LM result.

<a id="BIW-0103"></a>
## BIW-0103 — Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Kalyani Marathe, Artidoro Pagnoni, Tomasz Limisiewicz, Margaret Li, Mike Lewis, Luke Zettlemoyer and Srinivasan Iyer. [arXiv 2609.12303v1, 11 September 2026](https://arxiv.org/pdf/2609.12303v1). Aliases S04-N15, S06-N04, S07-N11.

**Reading: FULL.** Full 52-page PDF §§1–10 and Appendices A–G, including Tables 1–24, conversion pseudocode and special cases in F, sensitivity D/E; visually checked pp.5, 9, 37, 38, 40, 46. Read plots for their qualitative claims, not every curve coordinate. PDF and UTF-8 text are in `sources/BIW-0103.*`; `pdftotext` reported PDF graphics/font warnings, so key figures were rendered. Full text reading is not proof/code verification.
- **Carrying card:** [R06/BIW-0103](../03_reading/R06/BIW-0103.md).
- **Canonical problem records:** [BIP-0113](DETAILED_INVENTORY.md#BIP-0113), [BIP-0114](DETAILED_INVENTORY.md#BIP-0114).
- **Units — input / internal / output / supervision (current):** Subwords,UTF-8bytes,orbytes+EOT261classes / densecausalstudentpositions / sameunitor markedbyteevent / groundtruthCEorteacherKL; markedprocessnotunmarkedprefixmarginal.

### Current substantive interface, technique, evidence and limits

**Reading: FULL.** Full 52-page PDF §§1–10 and Appendices A–G, including Tables 1–24, conversion pseudocode and special cases in F, sensitivity D/E; visually checked pp.5, 9, 37, 38, 40, 46. Read plots for their qualitative claims, not every curve coordinate. PDF and UTF-8 text are in `sources/BIW-0103.*`; `pdftotext` reported PDF graphics/font warnings, so key figures were rendered. Full text reading is not proof/code verification.

### Units, probability and actual supervision

All students are dense decoder-only causal Transformers. Input/internal/output are either subword-token positions, UTF-8 byte positions or byte-plus-`<eot>` positions; labels are next ground-truth units for cross-entropy or Llama-3-8B teacher distributions for KL distillation. Byte vocabulary is 256+4 specials, marked vocabulary adds EOT (261); token vocab 128,256 (§3/Table 1). Boundary markers remain part of the modeled output, not automatically the unmarked byte marginal. EOS/BOS and markers are present in the illustrated sequence (§2.2), but a complete raw-byte partial-prompt policy and marginalization at arbitrary prefix are not specified. No verifier. Inputs and outputs are distinct embedding tables **in the parameter accounting** (Appendix A Table 9 counts both), but actual tensor aliasing, shared decoding heads or checkpoint wiring were not independently checked.

[**BIP-0113**](DETAILED_INVENTORY.md#BIP-0113): teacher distribution is over whole BPE tokens and byte-prefix mass may have already terminated → approximate method filters tokens sharing the observed within-token prefix and renormalizes, while marked method appends an EOT to every teacher token and includes its mass as a separate output class. Figure 2 p.5 example: after `is`, candidate `isu=.5`, `isk=.125`, `is=.125`, the approximate distribution normalizes u/k to .8/.2 and discards termination; marked distribution u/k/EOT = 2/3, 1/6, 1/6. Subsequent teacher calls are required to recover continuations of terminated alternatives when conditioning on an **unmarked** byte prefix. Exactness is conditional on the marked token history and complete token-distribution mapping, not proof of the unmarked-byte next-symbol marginal. Appendix F.1 pseudocode introduces the EOT alphabet size but does not show appending EOT to `token_to_bytes`, `gold`, or adjusting lengths; that preprocessing appears required for the pseudocode to express the prose, and is not independently verified. The released implementation was not inspected.

### Experiment, results and independent interpretation

[**BIP-0114**](DETAILED_INVENTORY.md#BIP-0114): equal layer size and cross-tokenization validation loss do not determine downstream accuracy or equal cost → sweep 3 representations × supervised/distilled, training compute and 3 learning rates and report both observed curves and extrapolations. Models have 1.2846B Transformer-layer parameters; Table 9 totals are 1.810B token vs 1.286B byte/marked, 25 layers, width 2048. Token 2048 positions, byte 9216, marked 11264; truncate/pad to those contexts, QK normalization in byte arms, and global batches ≈0.5M **units**, not equal original text. 64 H200 per run; Llama-2 data mixture, Llama-3-8B teacher, AdamW, three learning rates 1e-3/4e-3/8e-3 and 10% warmup (Appendix A). Some large runs repeat data (§10); no total unique text, full teacher inference compute, I/O, serving latency or seed variance is supplied. The experiment ranges up to approximately 1T bytes; input counts at points and marker counts should not be interchanged.

Figure 4 p.9 measured multiple-choice averages: subword leads strongly at low FLOPs; byte curves catch up within the plotted range, but ranges differ across model arms. At the ≈1.8×10²¹ FLOP 220B-token reference, all four byte models have lower validation BPB yet worse downstream than token-supervised (§§5–6). Maximum available checkpoints in Table 18 p.37: marked distilled 44.6 six-task average vs token distilled 44.4, Llama-3.2-1B 45.9 and Gemma-2B 50.3; different training exposures prevent a matched-training comparison. Asymptotic prediction at LR 4e-3 and validation set 1 is 52.4 marked vs 48.4 token distilled, a **4 percentage point extrapolation** (Table 5), not the observed 44.6–44.4 difference and not a guarantee.

The two-stage extrapolation fits BPB vs FLOPs then downstream error vs BPB. Figure 21 leave-one-out sensitivity at LR 4e-3 gives marked-distilled asymptote range Δc=.0098, vs token-distilled .0025; changing residual weighting and validation set alters extrapolations (Appendix D, Figures 22–23). Validation set 2 Table 21 at LR 1e-3 predicts token distilled 49.2 vs marked 48.6, reversing the celebrated asymptotic ranking; Table 22 reports no crossover for that pair. Thus no universal 4-point gain or firm high-compute crossover is justified. Table 6's 6.33×10²² FLOPs is a *predicted* marked compute to reach token model's predicted asymptote, not a measured equal-score crossover.

Marker cost is ≈30.94% more FLOPs per same source token: 4.5 content bytes versus 5.5 marked units, plus 9.44 vs 8.81 GFLOPs/unit (Table 3); the gains are confounded by extra compute and boundaries. Table 7's 6.35× text-saving and 5.19× storage-saving ratios are at that extrapolated fixed-compute comparison, not total end-to-end resources. Appendix A.6 controls saved teacher logits: token arm stores top 600 float32 logits + int32 indices, byte arm all ~260 float32 logits per byte; no free teacher computation, full online logit generation, disk I/O or 8B-teacher pretraining budget is included. §10 explicitly notes marked-byte inference can be significantly more expensive, and matched-inference-cost study is absent.



**Current R1 adjudication ([FULL_READING_AUDIT_R1](../05_review/FULL_READING_AUDIT_R1.md)):** R1 refinement: EOT expansion may be caller-supplied in token_to_bytes/lengths/gold. The listing does not show that preprocessing; absence of an internal append does not demonstrate an implementation defect. Marked-history exactness is not an unmarked-byte marginal, and four-point gain remains extrapolated.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; recovery discovery reused, absent old W catalog. No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2609.12303v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Byte OR byte+end-of-token OR subword → dense Transformer → corresponding alphabet; CE vs teacher distributions
- **Learning and causal baseline:** Causal; fixed1.28B layer parameters but token total1.81B vs byte1.28B;≤1T bytes. Approximate prefix marginalization vs exact boundary-marked representation; extra30.94% compute/data for marked stream reported. Asymptotic superiority is fitted extrapolation; teacher/storage/full costs pending.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0113](DETAILED_INVENTORY.md#BIP-0113), [BIP-0114](DETAILED_INVENTORY.md#BIP-0114).
- **Reading ownership:** [R06](batches/R06.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S04/S04-N15**, [WORKS](../01_discovery/S04/WORKS.md) line 47: **S04-N15**, 2026, Marathe et al., *Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models*; [v1](https://arxiv.org/html/2609.12303v1) **Recovery reuse**, byte-audit N05; P §§1.1/2/3
  - Original register aliases / era / family / provenance: **S04-N15**, 2026, Marathe et al., *Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models*; [v1](https://arxiv.org/html/2609.12303v1)
  - Source-scoped evidence/depth: **Recovery reuse**, byte-audit N05; P §§1.1/2/3 Causal; fixed1.28B layer parameters but token total1.81B vs byte1.28B;≤1T bytes. Approximate prefix marginalization vs exact boundary-marked representation; extra30.94% compute/data for marked stream reported. Asymptotic superiority is fitted extrapolation; teacher/storage/full costs pending.
- **S06/S06-N04**, [WORKS](../01_discovery/S06/WORKS.md) line 51: **Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models**; [2609.12303v1](https://arxiv.org/abs/2609.12303v1),2026-09-11
  - Original register aliases / era / family / provenance: S06-N04; **recovery reuse**, byte audit N05
  - Source-scoped evidence/depth: Abstract:~1B layer-parameter-matched,up to1T bytes; token wins low-FLOP regime; byte can surpass later;~one-sixth data,~one-fifth logit-storage claims. Up-to4% asymptotic error advantage is forecast, not observed final training point. Teacher generation/storage total cost missing. **A**.
- **S07/S07-N11**, [WORKS](../01_discovery/S07/WORKS.md) line 50: **Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models**; [2609.12303v1](https://arxiv.org/abs/2609.12303v1), 2026
  - Original register aliases / era / family / provenance: S07-N11; **recovery reuse**
  - Source-scoped evidence/depth: A; already recovery `07_BYTE_SURVEY` N05. Exact probability statement, full training budget and empirical vs asymptotic crossover need full read.

</details>

<a id="BIW-0104"></a>
## BIW-0104 — MYTE: Morphology-Driven Byte Encoding for Better and Fairer Multilingual Language Modeling

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Tomasz Limisiewicz, Terra Blevins, Hila Gonen, Orevaoghene Ahia, Luke Zettlemoyer, [arXiv 2403.10691v2, 11 November 2024](https://arxiv.org/pdf/2403.10691v2). Alias S05-R01. Backlink [BIP-0221](DETAILED_INVENTORY.md#BIP-0221). ACL 2024 publication is not assumed identical to this later version.

**Reading: FULL** for this fixed PDF: §§1–7, limitations, Appendix A–C, Tables 1–9 and Figures 1–12; selected figures and Tables 2–4, 6–8 visually checked. Table 9 was visually inspected because text extraction loses row alignment; verify any additional individual LM cells on the PDF before use. Reading does not independently establish reversibility, code behavior, probability accounting or reproduce results.
- **Carrying card:** [R07/BIW-0104](../03_reading/R07/BIW-0104.md).
- **Canonical problem records:** [BIP-0221](DETAILED_INVENTORY.md#BIP-0221).
- **Units — input / internal / output / supervision (current):** Originaltext transcodedtomorphology-derivedMYTEcodes / bytecodeencoder-decoderstates / MYTEcodes/taskstrings / spanrestorationandtasklabels; codesnot rawUTF-8, Morfessorcodebookexternal.

### Current substantive interface, technique, evidence and limits

**Reading: FULL** for this fixed PDF: §§1–7, limitations, Appendix A–C, Tables 1–9 and Figures 1–12; selected figures and Tables 2–4, 6–8 visually checked. Table 9 was visually inspected because text extraction loses row alignment; verify any additional individual LM cells on the PDF before use. Reading does not independently establish reversibility, code behavior, probability accounting or reproduce results.

### Problem, solution, techniques

**Problem:** UTF-8 uses disproportionately many bytes for many scripts and multilingual subword segmentation also allocates uneven sequence lengths. **One-sentence solution:** transcode text using a 256-symbol byte alphabet with variable-length codepoints assigned to a multilingual inventory of frequent automatically inferred morph-like strings, then train a ByT5-like model on those codes (§§2–3).

- **Morfessor**, not a neural boundary module or an annotated morphology teacher, infers segmentations separately per language; adaptive lexicon/corpus-loss weight targets ~4,096 morphs each. It consumes Wikipedia-derived frequency information, 45 MUSE lexicons and 54 Wikipedia-derived lexicons, capped at 30,000 lexemes/language, not zero preprocessing (§3.1, Appendix A). The union is ranked by Morfessor loss contribution. Language and corpus contamination and segmentation errors remain possible.
- **Variable-length coding**: 26 ASCII uppercase codes are repurposed, one becoming a capitalization marker, with 25 leading bytes allocated to eight script groups, including a mixed-script group. Continuations come from 0x80–0xBF; 64 top morphs per group use two bytes, next 4,096 three, subsequent up to 262,144 four (§3.2, Table 1). Unmatched material retains the base-encoding route. Lexicon preprocessing uses decomposed Unicode—Appendix A prints “NKFD”, presumably intended NFKD, but does not clearly settle every model input's normalization; do not silently certify the implementation. Decomposition can discard original Unicode composition/compatibility distinctions: no demonstrated bitwise inverse to original UTF-8, normalization policy and decoder/error cases need implementation verification.
- **Transformer encoder–decoder span denoising** learns representations and generates masked spans; the external morphology statistics determine a fixed codebook rather than being trained jointly. Input/output/supervision are MYTE code bytes plus task/control symbols, not raw UTF-8; UTF-8 bytes are the source text and comparison denominator. The encoder sees corrupted full context; target decoder is autoregressive, conditioned on encoder and prior output bytes. No special verification/sampling algorithm or partial-prefix policy is established. Encoder-input↔decoder-input and decoder-input↔output projection tying are **unknown for these actual runs**, as are other head-sharing axes; inherited family identity alone is insufficient.

### Results, controls and budgets

- Flores parallel-text lengths, not downstream LM successes for 99 languages: Table 2 seen non-Latin low-resource means UTF-8 305→MYTE 145 units (50% reduction), English 131→109 (16%). Five unseen languages with seen scripts average 196→138 (23%); unseen Ol Chiki Santali 365→365 (0%) and English-relative parity worsens 2.80→3.35 because English is compressed. Appendix B/Table 9 gives per-language lengths and language-model scores for the three shared multilingual model sizes; those 99 rows are not 99 separately trained models or 99 downstream task results.
- §5.1–5.3: small/base/large 300M/582M/1.23B models trained 250k steps on mC4 span restoration versus reimplemented ByT5 for the same steps, not original million-step checkpoint. Same step count does not establish equal original text, context bytes, FLOPs or equal preprocessing cost. App. C reports v3-8 TPU ~90h small/230h base, v3-32 ~190h large, A40 inference; no total FLOPs or explicit per-language exposure.
- Figure 5 reports Spearman −0.81 between compression and large-model score change, −0.77 for latency change. Table 3 large all-language average reported ByT5→MyT5 13.4→4.6 in **bits per parallel English UTF-8 byte**, 31.8→26.7 ms/sentence; non-Latin 18.2→5.4 and 37.3→27.0 ms. It is not bits per target raw byte. PDF Eq. 1 itself prints a sum of log probabilities without a leading minus despite interpreting positive surprisal; log base and exact scoring/termination are not established here. Figure 12 shows small/base exceptions even though main text broadly says all languages improve.
- Table 4 low-resource task averages: QA F1 73.2→75.3; NER 81.5→80.8; semantic parse EM 25.1→19.6; MT chrF 20.1→20.4. App. B Table 7 has losses on each reported semantic-parsing language. **Source inconsistency:** App. B Table 8 shows average LR/overall MT21.1/21.8 forMyT5 vs21.9/23.1 ByT5, contrary in direction to Table 4; its language list also differs from App. C.2 (Marathi vs Maltese among 15). Do not reconcile these silently. Baselines mT5 and Flan-PaLM in Table 4 use inherited results with differing setups. QA, NER, semantic parsing and MT are separately fine-tuned; compare their heterogeneous metrics only within task. App. C.2 reports batch 128 for NER, 64 others; 6,500/6,000/1,000/10,000 task steps and learning rate 1e−3.

**Inventory implications:** BIP-0221 should distinguish reducing UTF-8 code length from a learned pooling mechanism, record morphology-resource dependence, normalized rather than original byte invertibility, unseen-script failure, task losses and Table 4/8 conflict. Source’s speculative explanation of parsing loss is not causally isolated.



**Current R1 adjudication ([FULL_READING_AUDIT_R1](../05_review/FULL_READING_AUDIT_R1.md)):** Confirmed card transcription correction: Appendix B Table 8 (PDF p.17) headers are AVG LR, AVG. MyT5 low-resource/overall MT means are21.1/21.8; ByT5 are21.9/23.1. Both favor ByT5, whereas mainTable 4 low-resource20.4 vs20.1 favors MyT5; retain table/population labels, no blended sign. Table 8 includesMaltese(mt) andShona(sn); C.2 namesMarathi and omitsShona, listing14names versus15languagecolumns. Evaluated population and main/appendix reconciliation remain unresolved. Missingminus in Eq1 is notation/scoring uncertainty, not proof of negative-surprisal execution.

**Final R2 / claim-rules adoption** ([CLAIM_RULES](../05_review/CLAIM_RULES.md); [FULL_READING_AUDIT_R2](../05_review/FULL_READING_AUDIT_R2.md)): R2 reconfirms MYTE v2 Table8 row/column mapping: MyT5 low-resource/overall21.1/21.8; ByT5 low-resource/overall21.9/23.1. Do not follow the baseline-first convention of Table4 and swap model labels. MainTable4 instead reports MyT520.4 versusByT520.1 for its LRsummary; sets/aggregation and the14-name/15-column language population remain unresolved. Cite each table/population, not a fabricated single MT ranking. The parallel-English-byte denominator is not target-languageBPB; sign/log-base uncertainty is not evidence of failed scoring software.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; recovery discovery reused, absent old W catalog. No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2403.10691v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **A**, original identity/abstract freshly checked. Already recovery N02. Morpheme-driven alternate byte encoding; shorter encodings reported for 99 languages. Encoding tables, morphological resources, invertibility and budget need original method reading. Do not label UTF-8-native or imply unsupervised morphology.
- **Learning and causal baseline:** **A**, original identity/abstract freshly checked. Already recovery N02. Morpheme-driven alternate byte encoding; shorter encodings reported for 99 languages. Encoding tables, morphological resources, invertibility and budget need original method reading. Do not label UTF-8-native or imply unsupervised morphology.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0221](DETAILED_INVENTORY.md#BIP-0221).
- **Reading ownership:** [R07](batches/R07.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S05/S05-R01**, [WORKS](../01_discovery/S05/WORKS.md) line 40: MYTE: Morphology-Driven Byte Encoding for Better and Fairer Multilingual Language Modeling; Limisiewicz et al.; [ACL 2024](https://aclanthology.org/2024.acl-long.804/), pp.15059–15076; [arXiv v2](https://arxiv.org/abs/2403.10691v2), 2024-11-11
  - Original register aliases / era / family / provenance: S05-R01
  - Source-scoped evidence/depth: **A**, original identity/abstract freshly checked. Already recovery N02. Morpheme-driven alternate byte encoding; shorter encodings reported for 99 languages. Encoding tables, morphological resources, invertibility and budget need original method reading. Do not label UTF-8-native or imply unsupervised morphology.

</details>

<a id="BIW-0105"></a>
## BIW-0105 — XTREME-UP: A User-Centric Scarce-Data Benchmark for Under-Represented Languages

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Sebastian Ruder, Jonathan H. Clark et al., [arXiv 2305.11938v2, 24 May 2023](https://arxiv.org/pdf/2305.11938v2), S05-R02; backlink [BIP-0227](DETAILED_INVENTORY.md#BIP-0227).

**Reading: FULL** fixed PDF §§1–7, Tables 1–12, Appendix A language list, Appendix B.1–B.8 task cards, C prompts; visually checked main Table 4 and autocomplete Table 8. Some dense ASR Table 6 cells have extraction alignment errors; do not quote a cell without visually verifying it. The detailed per-language outcomes elsewhere linked to the authors' repository are not all reproduced by the article. No benchmark code, model weights or implementation run was verified.
- **Carrying card:** [R07/BIW-0105](../03_reading/R07/BIW-0105.md).
- **Canonical problem records:** [BIP-0227](DETAILED_INVENTORY.md#BIP-0227).
- **Units — input / internal / output / supervision (current):** Task-dependentbytes(ByT5),subwords(mT5),audio/imagefrontends / pretrainedencoder-decoder orretrievalvectors / tasktext,labels,top3wordsorpassageIDs / scarcein-languageannotations plusupstreamresources.

### Current substantive interface, technique, evidence and limits

**Reading: FULL** fixed PDF §§1–7, Tables 1–12, Appendix A language list, Appendix B.1–B.8 task cards, C prompts; visually checked main Table 4 and autocomplete Table 8. Some dense ASR Table 6 cells have extraction alignment errors; do not quote a cell without visually verifying it. The detailed per-language outcomes elsewhere linked to the authors' repository are not all reproduced by the article. No benchmark code, model weights or implementation run was verified.

### Problem and technical response

**Problem:** multilingual evaluation often uses high-resource tasks and zero-shot setups rather than realistic user-facing needs with limited labeled data. **One-sentence solution:** establish standardized in-language scarce-data splits and task-specific metrics for nine technologies spanning 88 under-represented languages, with joint multilingual fine-tuning and a five-example prompting baseline (§3, Table 1).

**Real techniques/roles:** mT5-base uses subword inputs/outputs; ByT5-base uses byte inputs/outputs; both are pretrained encoder–decoder Transformers jointly fine-tuned separately for each task. Flan-PaLM 62B uses subwords and English instruction plus five target-language exemplars, without task fine-tuning. Maestro-U transcribes audio first; Google Vision OCR reads images first, and the text model can post-correct. Retrieval maps query/passages to vectors and nearest-neighbor search; NER uses byte-span alignment; code-mixed test data uses PaLM-generated candidates plus human verification (B.8). These are external components/resources, not byte modeling advantages or free supervision. Table 4 OCR actually uses only Google OCR for both rows. Input/output: text→text for translation, transliteration, QA and structured semantic parsing, partial word prefix→top-3 completed words for autocomplete, text→entity spans and text→retrieved passage IDs; audio/image frontends yield text for baseline ASR/OCR. Fine-tuning supervises task target text or retrieval labels; ByT5 generates target bytes autoregressively from full encoded source. Its exact output/input tying and encoder↔decoder embedding tying are **not specified here**; no independent head-sharing assertion. Exact EOS, beam and arbitrary-byte-prefix probability treatment not established.

### Evidence and limitations

- §3.2/Table 1: maximum *estimated* eight hours labeling per under-represented language per task; high-resource supervised data unrestricted. Estimates exclude interface design, annotator training and validation. For instance, averages 120 MT pairs/UL, 426 in-language QA, 1,401 NER, 273 semantic parsing, 9 OCR pages (~290 lines); ASR 2,647 examples/UL. MT App. B.5 gives 499/498/1,012 train/dev/test examples per covered language, while Table 1's per-UL average 120 reflects benchmark budget; distinguish full data card and selected setup. §3.3 says 93 MT languages exist but evaluation is on 39 UL and the baseline trains only 39 pairs; Table 1 instead shows 70 UL for MT and 70,000 test examples. This internal scope discrepancy is unresolved; do not conflate the two.
- Table 3 gives both base models ~580M and 94.3% non-English pretraining, versus 62B Flan-PaLM 22%; models, objectives, architectures, data, prompting and decoding are not isolated tokenizer interventions. Fine-tuning uses TPU, but total pretraining data bytes, FLOPs, task compute and per-language source exposure are not provided. B.4: transliteration 30 directions jointly, 10k steps, batch 128, TPU v3 except large ByT5 v4; NFC plus language-specific visual normalization. B.3 autocomplete NFKC, max ten context words and target >5 characters, prefix length 0 to target length−3. B.3 Table 8 is explicitly **preliminary**, 10 epochs, up to 2,000 train examples/language, not the final benchmark.
- Main Table 4, mT5→ByT5: ASR CER 8.5→8.2 (lower better), autocomplete Acc@3 12.7→27.6, transliteration CER 37.6→14.6, English→UL MT chrF 22.5→26.9, QA F1 59.7→71.4, retrieval MRR .23→.29, NER F1 74→84, semantic parsing EM 21.8→37.5. These are task averages, not 88 independent byte wins; OCR is the identical 11.1 baseline.
- B.3/Table 8 preliminary autocomplete: ByT5 Acc@3 is below mT5 on Belarusian (8.99 vs 12.4), Greek (14.91 vs 21.74), Hebrew (13.87 vs 19.0), and Uyghur (0.23 vs 3.41). Its overall 22.84 vs 14.85 is over the preliminary 23-language set. Performance correlates with Latin alphabet similarity (r=.75 ByT5 vs .56 mT5, chrF), an observational comparison, not script-level causal proof. B.8/Table 10 semantic parsing ByT5-base average 43.77 > ByT5-large 34.84 (all languages), rejecting simple larger-is-always-better.
- ASR Appendix B.1 selectively uses post-correction only if dev beats upstream; filters empty Maestro-U predictions. This conditions evaluation and hides pure correction harms, and output quality depends on the upstream model. OCR baseline is not a trained byte model. Five-shot model is far larger but less multilingual in pretraining and is not compute- or training-matched.

**BIP-0227:** benchmark scope is not byte-model advantage scope. Record language cells, normalizations, task-specific output/metrics and teacher/frontend provenance. Scarce annotation is not zero-shot or absence of pretraining/supervised external resources.



**Current R1 adjudication ([FULL_READING_AUDIT_R1](../05_review/FULL_READING_AUDIT_R1.md)):** R1 scope refinement: full data-card499MTexamples versus selected120average is pre-subsampling versus benchmark-budget scope, not a contradiction.93total languages versus39baselinepairs also differ in scope.70UL benchmark population versus prose39ULevaluation remains insufficiently documented; do not assert70baselineevaluations or a39-language-onlybenchmark.

<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; recovery discovery reused, absent old W catalog. No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2305.11938v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **A**, already recovery N07. 88 languages/9 user technologies, scarce-data rather than zero-shot contract. Abstract establishes benchmark scope, **not** the byte/subword score ordering, unit details or annotation budgets.
- **Learning and causal baseline:** **A**, already recovery N07. 88 languages/9 user technologies, scarce-data rather than zero-shot contract. Abstract establishes benchmark scope, **not** the byte/subword score ordering, unit details or annotation budgets.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0227](DETAILED_INVENTORY.md#BIP-0227).
- **Reading ownership:** [R07](batches/R07.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S05/S05-R02**, [WORKS](../01_discovery/S05/WORKS.md) line 41: XTREME-UP: A User-Centric Scarce-Data Benchmark for Under-Represented Languages; Ruder et al.; [2305.11938v2](https://arxiv.org/abs/2305.11938v2), 2023-05-24
  - Original register aliases / era / family / provenance: S05-R02
  - Source-scoped evidence/depth: **A**, already recovery N07. 88 languages/9 user technologies, scarce-data rather than zero-shot contract. Abstract establishes benchmark scope, **not** the byte/subword score ordering, unit details or annotation budgets.

</details>

<a id="BIW-0106"></a>
## BIW-0106 — Byte-based Multilingual NMT for Endangered Languages

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Mengjiao Zhang and Jia Xu, COLING 2022, official [pp. 4407–4417 PDF](https://aclanthology.org/2022.coling-1.388.pdf), alias S05-N01; backlinks [BIP-0224](DETAILED_INVENTORY.md#BIP-0224), [BIP-0225](DETAILED_INVENTORY.md#BIP-0225).

**Reading: FULL** §§1–6, Tables 1–9, Figures 1–6, Appendices A–C; Figures 5–6 and Tables 4, 7–9 visually checked. No code or weights executed.
- **Carrying card:** [R07/BIW-0106](../03_reading/R07/BIW-0106.md).
- **Canonical problem records:** [BIP-0224](DETAILED_INVENTORY.md#BIP-0224), [BIP-0225](DETAILED_INVENTORY.md#BIP-0225).
- **Units — input / internal / output / supervision (current):** UTF-8byteonehotinput / multilingualTransformer / learned256wayoutputbytehead / teacher-forcedtranslationCE; independentpermutationensembleaveragesinversealignedprobabilities.

### Current substantive interface, technique, evidence and limits

**Reading: FULL** §§1–6, Tables 1–9, Figures 1–6, Appendices A–C; Figures 5–6 and Tables 4, 7–9 visually checked. No code or weights executed.

### Atomic problems and proposed solutions

1. **Translation vocabulary bottleneck/OOV:** use UTF-8 bytes directly and train a multilingual encoder–decoder Transformer with one-hot byte vectors in place of learned source and target byte embedding tables (§3.1–3.3). A learned 256-way linear+softmax is the output head; it is not tied to a learned input embedding since that embedding is absent. Each multilingual model shares its Transformer across language pairs; distinct ensemble models do **not** share weights. Output-head↔other-head axes beyond this are not reported.
2. **Sensitivity to arbitrary byte IDs:** train z independent Transformer models on z bijective permutations of the same UTF-8 values; permute each model's output probabilities back to original byte index, average them, then use beam search (§3.4, Eq. 8–9, Fig. 4). This is a compute-costly prediction ensemble, not augmentation of one model or typo-robustness testing.
3. **Low-resource transfer:** pretrain on five high-resource language→English pairs, then fine-tune multilingual model on ten Indigenous language→Spanish pairs; compare mono- and multilingual pretraining (§4.5, §5.3).

**Causality and units:** raw text UTF-8→one-hot byte positions→Transformer states→autoregressive target bytes, with target-byte cross-entropy under gold previous target during training and beam decoding on generated prefixes (§3.2–3.3). Full source is visible through encoder. Inverse-map generated bytes to text; invalid UTF-8, EOS and partial-prefix behavior are not specified, and a verifier is not described. Byte permutation is not a new natural orthography, nor are source character perturbations tested. Subword comparators use 10k BPE merge operations and shared source/target embeddings; this changes embedding design and vocabulary size as well as units (§4.2–4.3).

### Evidence and budgets

- IWSLT14 six→English directions, five high resource plus Slovenian; filter >800 bytes from training (~5%). IndCorpus has ten source→Spanish languages, 3,883–125,008 pairs/language (Appendix A Tables 5–6). IndCorpus dev is repurposed as test because its test is unavailable; train 50 epochs, no early stopping. IWSLT trains up to 200 epochs, patience 5. Adam, inverse-square-root schedule, warmup 4k; 6+6 layers, 4 heads IWSLT, 5+5, 2 heads IndCorpus, hidden 512, FFN 1024, RTX 3090 (§4, App. B). Total parameters, FLOPs, runtime, sampling ratios and best-hyperparameter search are not specified.
- Table 1 no-ensemble multilingual vs monolingual: Slovenian→English byte BLEU 2.2→20.7, subword 8.9→20.2; byte multilingual Arabic 30.4 < byte monolingual 30.8, German 34.2 < 34.4, Turkish 22.5 < 22.8. Do not call all pairs improved over monolingual or attribute all of +18.5 to bytes rather than multilingual transfer.
- Table 3 four-language Indigenous joint training yields mean byte B-N 1.6 vs BMNMT 3.6 BLEU; subword W-N 1.6 vs W-M 2.7. Table 8 mean chrF 17.3→23.8 vs 16.7→21.2. Shipibo byte BLEU 0→3.9 and chrF 12.0→27.0; this is a four-pair analysis, not all ten.
- Table 4 transfer/fine-tuning ten pairs: mean B-N 2.3, byte multilingual 3.5, W-N/W-M both 1.9 BLEU. Byte pretrained Shipibo mono→multi 0.6→2.7, but 2.7 is lower than 3.9 from the separately trained case in Table 3: pretraining need not beat native joint training. Table 9 averages chrF 21.5→24.6 byte mono→multi, W-N/W-M 17.0→17.4.
- Figure 5 tests z=1,2,4,6,8 with five repetitions per size, uncertainty bars; averages generally increase and variance falls, but Quechua z=8 is slightly below z=6. Figure 6 chrF also plateaus or dips. The paper does not isolate random permutation vs same-encoding independently initialized ensemble; compute scales with z independent runs/inference and repetitions are not free. Cost-matched single-model or ordinary ensemble control is absent.

**Inventory implications:** BIP-0224 must separate unit, shared training and transfer, filtering and dev-as-test. BIP-0225 is invariance to ID assignment/ensemble variance, not robustness to spelling noise; avoid causal claims that random mapping itself accounts for generic ensembling gains.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2022.coling-1.388.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **P** original §§3–4 and §5.4/associated discussion, not complete table/appendix reading. UTF-8 one-hot input and byte output; shared multilingual transformer, translation CE, beam search, random bijective byte permutations and probability-aligned model ensemble. IWSLT14 + IndCorpus; dev used as test for IndCorpus, >800-byte filter removes about 5% IWSLT training samples. Ensemble size 1/2/4/6/8 changes model budget.
- **Learning and causal baseline:** **P** original §§3–4 and §5.4/associated discussion, not complete table/appendix reading. UTF-8 one-hot input and byte output; shared multilingual transformer, translation CE, beam search, random bijective byte permutations and probability-aligned model ensemble. IWSLT14 + IndCorpus; dev used as test for IndCorpus, >800-byte filter removes about 5% IWSLT training samples. Ensemble size 1/2/4/6/8 changes model budget.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0224](DETAILED_INVENTORY.md#BIP-0224), [BIP-0225](DETAILED_INVENTORY.md#BIP-0225).
- **Reading ownership:** [R07](batches/R07.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S05/S05-N01**, [WORKS](../01_discovery/S05/WORKS.md) line 50: Byte-based Multilingual NMT for Endangered Languages; Mengjiao Zhang, Jia Xu; [COLING 2022](https://aclanthology.org/2022.coling-1.388/), pp.4407–4417; [PDF](https://aclanthology.org/2022.coling-1.388.pdf)
  - Original register aliases / era / family / provenance: S05-N01
  - Source-scoped evidence/depth: **P** original §§3–4 and §5.4/associated discussion, not complete table/appendix reading. UTF-8 one-hot input and byte output; shared multilingual transformer, translation CE, beam search, random bijective byte permutations and probability-aligned model ensemble. IWSLT14 + IndCorpus; dev used as test for IndCorpus, >800-byte filter removes about 5% IWSLT training samples. Ensemble size 1/2/4/6/8 changes model budget.

</details>

<a id="BIW-0107"></a>
## BIW-0107 — How Robust is Neural Machine Translation to Language Imbalance in Multilingual Tokenizer Training?

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Shiyue Zhang, Vishrav Chaudhary, Naman Goyal, James Cross, Guillaume Wenzek, Mohit Bansal, Francisco Guzmán, AMTA 2022, official [pp. 97–116 PDF](https://aclanthology.org/2022.amta-research.8.pdf). Alias S05-N02; backlink [BIP-0226](DETAILED_INVENTORY.md#BIP-0226).

**Reading: FULL:** §§1–7 and Appendix A.1–A.5; Tables 1–4; Figures 1–10, with main/ablation plots visually checked, including byte fallback Figures 7 and 10. Not code, runtime, or proof verification.
- **Carrying card:** [R07/BIW-0107](../03_reading/R07/BIW-0107.md).
- **Canonical problem records:** [BIP-0226](DETAILED_INVENTORY.md#BIP-0226).
- **Units — input / internal / output / supervision (current):** Unigram/BPEsubwords withoptionalUTF-8fallback / fullsourceencoder+causaltargetdecoder / targetsubwords / paralleltranslationtraining; tokenizer/modeldatasamplingindependentlyvaried.

### Current substantive interface, technique, evidence and limits

**Reading: FULL:** §§1–7 and Appendix A.1–A.5; Tables 1–4; Figures 1–10, with main/ablation plots visually checked, including byte fallback Figures 7 and 10. Not code, runtime, or proof verification.

### Problem, solution and units

**Problem:** tokenizer training data imbalance and model training data imbalance are commonly changed together, hiding which creates translation loss. **One-sentence solution:** vary language proportions in a fixed-size SentencePiece training corpus while fixing the parallel data and model sampling, then independently alter model sampling and examine UNK and segmentation diagnostics (§§3–4).

Actual techniques: SentencePiece unigram probabilistic segmentation learns a 5K bilingual or 20K multilingual vocabulary; BPE is an ablation. A 12-layer encoder/12-layer decoder Transformer (6+6 ablation), trained on parallel sentence pairs with Adam and decoded with beam 5, translates autoregressively from full source to target subwords. UTF-8 byte fallback is only a substitute representation for unseen characters inside a subword vocabulary, not a native byte model; standard token/character normalization, probability or invalid-prefix policy are not characterized in the paper. No special verifier is introduced. Sharing of encoder input↔decoder input, input↔output projection, and other output heads is not specified. Full raw source context/exposure in bytes, total parameters/FLOPs and teacher supervision beyond parallel corpus are unreported.

Bilingual setup: eight languages, 14 English-centric directions, 2M monolingual tokenizer-training sentences, English share 0–100% including 0.001% and 99.999%; parallel NMT training data fixed, three seeds, 5K vocabulary, 0.99995 character coverage except Chinese 0.995; FLORES101 dev/devtest; spBLEU and chrF (§3.1, Table 1). Multilingual setup: 10M tokenizer sentences, one 20K vocabulary and one model for 14 directions; select one of English, Icelandic, Tamil or Chinese, vary its share while evenly weighting other seven, one seed. Fairseq, 4K-token batches, accumulated gradients 4, early stopping patience 20, batch 32 inference (App. A.1). Ethical statement reports 1,890 bilingual experiments with 8 V100 each taking <1 hour to ~2 days, and 31 multilingual experiments ~1.5 days on 64 GPUs; do not treat as matched compute to byte models.

### Results and counterexamples

- Figure 1/§3.3: Latin-language pair degradation mainly at ≥99.999% English (~20 minority sentences of 2M); non-Latin target Chinese falls already at 90%, Tamil and Greek at 99.9%. 12/14 best spBLEU scores lie at English 10–90%; average Pearson correlation with balance .38. In 8-language model average .49, not a universal effect.
- English “never starved” is conditional on contamination: Tamil/Chinese monolingual data contain 3.6%/2.6% ASCII English characters. Removing them at 0.001% English makes en–zh/zh–en spBLEU 17.7/25.5→0.2/0.1 (§3.3). This is an intervention on training vocabulary source, not proof of comparable multilingual exposure.
- UNK fraction is per subword, while character proximity is subword length/character length. Apparent threshold warnings around 3.7% and .87 are dataset-specific; a rise in UNK can *reduce* apparent subword length. Multilingual Tamil declines at 1% share with neither warning (§4.2); thresholds neither necessary nor sufficient.
- **Fallback negative control:** §3.4/Figure 7: zero UNKs yet no reliable robustness gain; Icelandic/Danish still collapse at 99.999%, with greater degradation than default in that setting; non-Latin failures appear at same proportions and effects differ by direction. In eight-language Chinese experiment fallback is somewhat more stable ≥1% but worsens at ≤0.1% (Figure 10). Appendix A.3.4 incorrectly says 32K vocabulary where Fig. 7 caption says byte fallback; use the caption/main text and flag ambiguity.
- Table 2 varying tokenizer sampling exponent at fixed model exponent .2 yields overall spBLEU 31.3, 30.9, 31.2 for S=0,.3,1; varying model exponent at fixed tokenizer S=0 yields 29.9,31.3,30.7 for S=0,.2,1. Wider change here supports more model-sampling sensitivity only in these tested settings. Table 3 adding held-out non-Latin characters to 100%-English vocabulary improves en–zh 0.6→20.0, but en–ta only 0→0.1 and ta–en 0.2→0.1; explicit characters are not a universal solution. Larger 32K vocabulary postpones non-Latin drops but hurts Tagalog under extreme skew.

**BIP-0226:** retain separate tokenizer-data/model-data axes, byte fallback failure, unknown-token and segmentation diagnostics, shared-script/contamination caveats and task/data/compute limits. Neither lossless fallback nor this study provides a causal verdict on native UTF-8 byte LMs.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2022.amta-research.8.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **A** original abstract. Vary tokenizer-corpus language mix separately from model-training mix; UNK and character-proximity diagnostics. Abstract says model-training sampling matters more. Byte-fallback failure appears only in search snippet: **not accepted as inspected paper evidence**.
- **Learning and causal baseline:** **A** original abstract. Vary tokenizer-corpus language mix separately from model-training mix; UNK and character-proximity diagnostics. Abstract says model-training sampling matters more. Byte-fallback failure appears only in search snippet: **not accepted as inspected paper evidence**.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0226](DETAILED_INVENTORY.md#BIP-0226).
- **Reading ownership:** [R07](batches/R07.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S05/S05-N02**, [WORKS](../01_discovery/S05/WORKS.md) line 51: How Robust is Neural Machine Translation to Language Imbalance in Multilingual Tokenizer Training?; Shiyue Zhang et al.; [AMTA 2022](https://aclanthology.org/2022.amta-research.8/), pp.97–116
  - Original register aliases / era / family / provenance: S05-N02
  - Source-scoped evidence/depth: **A** original abstract. Vary tokenizer-corpus language mix separately from model-training mix; UNK and character-proximity diagnostics. Abstract says model-training sampling matters more. Byte-fallback failure appears only in search snippet: **not accepted as inspected paper evidence**.

</details>

<a id="BIW-0108"></a>
## BIW-0108 — Decoupling the Benefits of Subword Tokenization for Language Model Training via Byte-level Simulation

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Théo Gigant, Bowen Peng, Jeffrey Quesnelle, arXiv [2604.27263v2](https://arxiv.org/pdf/2604.27263v2), 14 May 2026; aliases S05/S05-N03, S08/S08-W13. **Reading: FULL:** PDF pp.1–14, main §§1–8, Appendix A Tables 1–2, Appendix B Figure 7. Figures 1–7 and hyperparameter tables visually inspected, not only text-extracted. No missing paper appendix; graph values below are approximate readings, not released measurements. FULL is not code, data, or theorem certification.

Problem: subword tokenization simultaneously changes capacity, original-text throughput, segmentation hints, positional distances, and objective. Solution: simulate each effect separately inside a byte-resolution LLaMA-3-style model and measure validation byte cross-entropy before/after temporary interventions.
- **Carrying card:** [R08/BIW-0108](../03_reading/R08/BIW-0108.md).
- **Canonical problem records:** [BIP-0115](DETAILED_INVENTORY.md#BIP-0115), [BIP-0116](DETAILED_INVENTORY.md#BIP-0116), [BIP-0117](DETAILED_INVENTORY.md#BIP-0117), [BIP-0118](DETAILED_INVENTORY.md#BIP-0118), [BIP-0119](DETAILED_INVENTORY.md#BIP-0119), [BIP-0120](DETAILED_INVENTORY.md#BIP-0120), [BIP-0270](DETAILED_INVENTORY.md#BIP-0270).
- **Units — input / internal / output / supervision (current):** UTF-8bytes (paper512vocab,specialIDsmasksunreported) andexternalBPEhints / byteorinitial4byte-sumpositions / byte,temporarilynextsubword / byteCEwithseparatecapacity/throughput/boundary/position/normalization/targetinterventions.

### Current substantive interface, technique, evidence and limits

### Interface, causal timing and experimental scope

Problem: subword tokenization simultaneously changes capacity, original-text throughput, segmentation hints, positional distances, and objective. Solution: simulate each effect separately inside a byte-resolution LLaMA-3-style model and measure validation byte cross-entropy before/after temporary interventions.

Input is UTF-8 bytes (paper Table 2 lists token vocabulary 512; exact special IDs and masks not specified); hidden positions ordinarily correspond to bytes; output and supervision are next-byte IDs. Subword boundary and subword-output experiments additionally use LLaMA-3 BPE annotations from offline complete sequences. Inference sharing of byte input/output matrices is **not stated**; don't import a LLaMA default. Temporary subword output head shares no stated axis with byte head; whether it is newly initialized and how unused byte head is trained are not specified. No verifier; no specific sampling/EOS/partial-prefix policy.

Baseline 1,747,060,736 parameters, 32 layers, 2048 width, 32 heads/8 KV heads, length 8192, global batch 128, 100k steps, AdamW (β .9/.95, weight decay .1), peak LR 3e−4, 2k warmup and final 10k cosine decay; ~160 B200 GPU-hours/run (Appendix A). Nominal baseline processes 104.86B byte-position inputs over 100k updates before packing/filter/overlap details, not verified unique text. Early four-byte stage nominally feeds four times as many raw bytes for 50k updates at same hidden positions; it only supervises 1/4 of byte positions, so cannot isolate throughput from supervision density or input grouping. English-centric FineWeb-Edu; exact source byte budget, dedup/filtering, seed counts, actual measured FLOPs, head cost, and training context packing remain unknown. Paper says isoFLOPs on matching hidden positions, not a measured equal total systems-cost audit.

### Atomic intervention findings and affected BIPs

- **BIP-0115 / capacity:** use Engram-inspired multihead input n-gram lookup as a capacity intervention, not a change in output alphabet: max n=3, eight heads, base 15k buckets/order, 71,065,088 added parameters (§5.1, Table 2). Figure 1 shows a small byte-loss improvement at 1.7B, Figure 7a a larger gap at 68M. No full embedding-capacity factorial or tied-vs-untied ablation.
- **BIP-0116 / throughput:** sum each consecutive four byte embeddings into one latent position, predict only the first byte of the *next* group for 50k steps then return to ordinary byte training (§5.2, Fig. 2). The first 50k stage suppresses 3/4 targets and changes sequence order/representation and raw context as well as exposure. Following switch validation loss drops below baseline: visually ~0.78 vs ~0.80 immediately before late decay near 90k, and ~0.74 vs ~0.76 at 100k. These are approximate from curves, not proof of independent throughput causation.
- **BIP-0117/0118 / boundaries:** binary embeddings for BPE starts or ends are added to byte input; §5.3 claims start boundaries are causal and ends leak future information. An offline tokenizer can revise earlier starts when a future byte changes previous segmentation; the paper does not establish prefix consistency of starts, hence do not endorse a general causality claim. Fig. 3a end labels have bigger advantage while supplied at evaluation, but are privileged; Fig. 3b training-only 50k then withdrawal shows start-arm post-switch below baseline and end-arm near baseline. Validation during initial intervention is without the hints for the training-only curves; the discontinuities should not be read as identical evaluation regimes. Labels come from an external tokenizer, not a learned verifier.
- **BIP-0270 / position:** repeat subword index over constituent bytes as RoPE position (§5.4). Fig. 4a shows a modest gain with hints; Fig. 4b after reverting at 50k is worse than baseline for much of the remaining run, so no durable advantage established. Since offline IDs derive from segmentation starts, prefix consistency is likewise unverified. Repeated indices encode an external boundary prior rather than byte distances.
- **BIP-0119 / normalization:** keep byte chain but normalize accumulated next-byte log-loss by subword count instead of byte count (§5.5). Figure 5 near-overlap: small improvement, not evidence that changing output-unit family has no effect. Paper's algebra is for decomposing probability under the byte model and same context, not a proof that a separately trained subword softmax has that probability or that normalization turns canonical token path probability into marginal text probability. Variable M/N across batches can alter weighting, not just a global learning-rate factor.
- **BIP-0120 / subword prediction:** temporary separate next-subword softmax targets at end-of-subword states for 50k then revert to byte output (§5.6); Figure 6 remains worse near 100k (~.79 vs ~.76), with transition/unused-head confounds. It is not a negative result on all multi-byte prediction or a proven exact byte likelihood. BPE-derived target boundaries and training-time head create a different supervision budget.

Appendix B Figure 7 repeats qualitative experiments at 68M, with 20k-step temporary interventions and 150k total steps; n-gram gain relatively larger, throughput gain visible, subword-head gap largely closes. No error bands/seeds shown. Strongest claims remain English-specific and not full-factorial; causal and morphology explanations are hypotheses rather than isolated independent proof.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2604.27263v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U UTF-8 bytes (some experiments sum four byte embeddings) → Llama-3-like dense positions → next byte, temporarily subword head in one arm → byte CE plus experimental priors/alternate targets. C baseline prefix-only; end-boundary prior deliberately contains future information; start-boundary prefix consistency needs explicit check rather than accepting its label.
- **Learning and causal baseline:** U UTF-8 bytes (some experiments sum four byte embeddings) → Llama-3-like dense positions → next byte, temporarily subword head in one arm → byte CE plus experimental priors/alternate targets. C baseline prefix-only; end-boundary prior deliberately contains future information; start-boundary prefix consistency needs explicit check rather than accepting its label.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0115](DETAILED_INVENTORY.md#BIP-0115), [BIP-0116](DETAILED_INVENTORY.md#BIP-0116), [BIP-0117](DETAILED_INVENTORY.md#BIP-0117), [BIP-0118](DETAILED_INVENTORY.md#BIP-0118), [BIP-0119](DETAILED_INVENTORY.md#BIP-0119), [BIP-0120](DETAILED_INVENTORY.md#BIP-0120), [BIP-0270](DETAILED_INVENTORY.md#BIP-0270).
- **Reading ownership:** [R08](batches/R08.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S05/S05-N03**, [WORKS](../01_discovery/S05/WORKS.md) line 52: Decoupling the Benefits of Subword Tokenization for Language Modeling; [2604.27263v2](https://arxiv.org/abs/2604.27263v2), 2026-05-14; [HTML](https://arxiv.org/html/2604.27263v2)
  - Original register aliases / era / family / provenance: S05-N03
  - Source-scoped evidence/depth: **P**, original §§2.2, 5.1–5.6 and §8; figure narratives read, curves not digitized; appendix tables missing in extraction. 1.7B LLaMA-3-style dense UTF-8 LM on English-centric FineWeb-Edu; n-gram input tables, four-byte pooling curriculum, boundary embeddings, repeated subword RoPE positions, loss renormalization, temporary subword output head. Several interventions only first 50k steps; English morphology caveat explicit. Author roster not verified, do not use submitter field as author list.
- **S08/S08-W13**, [WORKS](../01_discovery/S08/WORKS.md) line 44: **Decoupling the Benefits of Subword Tokenization for Language Model Training via Byte-level Simulation**, Gigant, Peng & Quesnelle; [2604.27263v2 HTML](https://arxiv.org/html/2604.27263v2), 2026-05-14. **P**, §§4–8 and figure captions/prose; Appendix A numerical tables and all curves not audited. Title/authors/version verified by Atom.
  - Original register aliases / era / family / provenance: S08-W13 / S08-N11 / **NEW**
  - Source-scoped evidence/depth: **Decoupling the Benefits of Subword Tokenization for Language Model Training via Byte-level Simulation**, Gigant, Peng & Quesnelle; [2604.27263v2 HTML](https://arxiv.org/html/2604.27263v2), 2026-05-14. **P**, §§4–8 and figure captions/prose; Appendix A numerical tables and all curves not audited. Title/authors/version verified by Atom. 1.7B, FineWeb-Edu English; most interventions first 50k steps then removed, ~160 B200 GPU-hours/run reported; smaller 68M appendix. Throughput/boundary benefits, weak n-gram-input and loss-rescaling effects, next-subword objective worse at this scale. Not a complete factorial study or downstream benchmark.

</details>

<a id="BIW-0109"></a>
## BIW-0109 — Synthetic and Natural Noise Both Break Neural Machine Translation

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Yonatan Belinkov and Yonatan Bisk, ICLR 2018, [arXiv 1711.02173v2, 24 February 2018](https://arxiv.org/pdf/1711.02173v2); S05-N06; backlink [BIP-0228](DETAILED_INVENTORY.md#BIP-0228).

**Reading: FULL:** complete fixed PDF §§1–8, Tables 1–8 and Figures 1–2; this 13-page version has references but no appendix. Figures 1 and 2 visually checked. No pretrained implementation, exact Unicode alphabet or weights verified.
- **Carrying card:** [R07/BIW-0109](../03_reading/R07/BIW-0109.md).
- **Canonical problem records:** [BIP-0228](DETAILED_INVENTORY.md#BIP-0228).
- **Units — input / internal / output / supervision (current):** Mosesword-charCNN/meanChar,character-to-character,orBPE / word/character/subwordstates / targetwords,characters,orsubwordsbyarm / translationlabelswithnoise-type-mixturetraining, notinferenceensemble.

### Current substantive interface, technique, evidence and limits

**Reading: FULL:** complete fixed PDF §§1–8, Tables 1–8 and Figures 1–2; this 13-page version has references but no appendix. Figures 1 and 2 visually checked. No pretrained implementation, exact Unicode alphabet or weights verified.

### Distinct problems and solutions

1. **Character access alone does not ensure robustness:** test pretrained character-to-character CNN/highway/recurrent encoder with recurrent autoregressive decoder and a Nematus subword BPE encoder–decoder on German/Czech→English; test separately trained character-CNN word representation on French/German/Czech→English (§3).
2. **Scrambling sensitivity:** average character embeddings within each tokenized source word (meanChar) to impose order invariance. This is a specific architectural invariance; it destroys order distinctions and remains sensitive to substitution/natural errors (§6.1).
3. **Multiple corruption types:** train a source-side word-charCNN (width 6, 1000 filters, 25-dimensional character embeddings, tanh+max pooling; two-layer LSTM encoder and decoder) on a uniformly per-sentence mixture of fully random scrambling, keyboard errors and harvested natural edits (§§3, 6.2). “Ensemble” here means an ensemble of *noise types within one model's training*, not multiple models at inference.

**Units and causality:** Moses-tokenized source words are sequences of characters for charCNN/meanChar, aggregated to one word representation; target decoder is word-based; char2char instead consumes and outputs characters; Nematus consumes and produces BPE subwords. Character definition/alphabet, Unicode normalization and exact OOV policy are not stated. Encoder processes the full source; attention decoder generates output left-to-right, trained on target translation. Exact decoding/search, EOS and any shared encoder/decoder embeddings or input/output head tying are not stated. No verifier. This is **character/word** evidence, not evidence about native UTF-8 byte models.

### Data, comparison and results

- IWSLT16 TED parallel training French/German/Czech→English 235K/210K/122K sentences and 5.2M/4M/2.1M source words (§4.1, Table 1); char2char and Nematus use existing pretrained WMT systems, so not parameter-, corpus- or compute-matched to newly trained charCNN. Compute, parameters, time and exact baseline exposure are not reported.
- Natural noise is reconstructed using edit lexicons, **not a naturally noisy parallel MT test corpus**: word-level substitutions are applied whenever available, one random edit selected uniformly; France/Germany/Czech dictionaries have 65,156/1,344/6,036 words and ~2.5–2.7 edits per entry (Table 2). It changes around 40–51% of tokens, versus much lower coverage for long German/Czech words. Train/test can share replacement pairs. Synthetic swap/middle-random preserve first/last and apply ≥4 characters; fully random applies all words; keyboard noise substitutes an adjacent key (§4.2).
- Table 3 German clean→natural BLEU: charCNN 34.79→14.02; char2char 29.97→12.68; Nematus 34.22→10.68; full random 1.02/.28/.29 respectively. Figure 1 shows degradation begins with smaller shares of changed words, and human translation of a scrambled German passage succeeds where all three fail (Table 4); human evidence is illustrative, not a controlled population study.
- Table 5 natural German Google Translate 18.6→25.0 BLEU after Google spelling correction vs clean 38.7; Czech natural 12.3→11.2 after spelling correction: external spellchecking can worsen results.
- MeanChar protects against scrambling by construction but has clean German BLEU 27.53 vs clean charCNN 34.79 and falls on keyboard/natural; Czech meanChar is particularly weak (Table 6). Noise training uses one fixed noisy training set with the *same* number of sentences/words as clean, but changes the source inputs; mixed training samples noise type uniformly (§6.2).
- Table 7 German charCNN trained on natural alone: clean 25.79, natural 34.59, keyboard 4.80, random 0.93. Rand+Key+Nat yields clean 31.29, random 30.04, keyboard 29.81, natural 31.60; not the best specialist but stronger average. Synthetic-only training fails to match natural-noise specialist; mixing trades specialist score and clean performance for coverage. Manual German sample ~40 edits: 34% phonetic and 32% omissions, neither captured directly by synthetic rules (§7.2). Figure 2 is suggestive filter-weight-variance analysis, not proof individual filters implement separate causal mechanisms.

**BIP-0228:** record natural-edit lexicon and changed training exposure, distinctions between invariance and learned mixed-noise robustness, target word units, language/script scope, comparable budgets, and failures on unseen corruption classes. Claims do not transfer automatically to byte models or arbitrary scripts.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1711.02173v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **A** original abstract/history. Character-based NMT can be brittle; noise-robust training and structure-invariant representations/character CNN are tested responses. Abstract does not establish strict byte model behavior or exact severity/budget.
- **Learning and causal baseline:** **A** original abstract/history. Character-based NMT can be brittle; noise-robust training and structure-invariant representations/character CNN are tested responses. Abstract does not establish strict byte model behavior or exact severity/budget.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0228](DETAILED_INVENTORY.md#BIP-0228).
- **Reading ownership:** [R07](batches/R07.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S05/S05-N06**, [WORKS](../01_discovery/S05/WORKS.md) line 55: Synthetic and Natural Noise Both Break Neural Machine Translation; Belinkov and Bisk; [1711.02173v2](https://arxiv.org/abs/1711.02173v2), 2018-02-24
  - Original register aliases / era / family / provenance: S05-N06
  - Source-scoped evidence/depth: **A** original abstract/history. Character-based NMT can be brittle; noise-robust training and structure-invariant representations/character CNN are tested responses. Abstract does not establish strict byte model behavior or exact severity/budget.

</details>

<a id="BIW-0110"></a>
## BIW-0110 — Models in a Spelling Bee: Language Models Implicitly Learn the Character Composition of Tokens

- **Reading status:** NF — returned new scoped FULL (R10), actual card read for integration; no fresh original-paper credit to inventory owner.
- **Carrying card:** [R10/BIW-0110](../03_reading/R10/BIW-0110.md).
- **Current units: input / internal / output / supervision:** Frozenuncontextualizedsubwordembedding / independent trainedTransformerprobe / character spelling / teacher-forcedspelling; separateexperiment initializesRoBERTaembeddings thenmaskedsubword LM.
- **Canonical records:** [BIP-0229](DETAILED_INVENTORY.md#BIP-0229), [BIP-0230](DETAILED_INVENTORY.md#BIP-0230).

### Current card-grounded detail

**Reading status: FULL** for [NAACL 2022 proceedings PDF](https://aclanthology.org/2022.naacl-main.373.pdf), pp. 5061–5068, §§1–6, Figures 1–2, Tables 1–2 and Appendices A–E (Tables 3–4, Figures 3–6). [PDF](../03_reading/R10/sources/BIW-0110.pdf), [text](../03_reading/R10/sources/BIW-0110.txt); [Table 1](../03_reading/R10/sources/BIW-0110-p3.png) and [Table 2](../03_reading/R10/sources/BIW-0110-p4.png) visually checked. No code was run. [BIP-0229](DETAILED_INVENTORY.md#BIP-0229), [BIP-0230](DETAILED_INVENTORY.md#BIP-0230).

### Problem → solution → techniques

Does an opaque subword-ID interface prevent language-model embeddings from retaining spelling? The authors train **SpellingBee**, an independently learned character-generating Transformer probe conditioned on a **frozen, uncontextualized token embedding**, with teacher-forced character predictions, then greedy-decode unseen vocabulary types (§2). Controls train the same probe on random vectors and filter related training vocabulary; this measures information recoverable by a trained nonlinear decoder, not the original LM's ability to spell when prompted.

A distinct intervention reverses the procedure: train randomly initialized embeddings to predict all their vocabulary spellings, then use the embedding matrix to initialize an otherwise matched randomly initialized RoBERTa-Large before masked-LM training (§5). The external spelling objective is explicitly used during that initialization, not a deployed byte encoder or a per-step auxiliary loss throughout masked-LM training.

### Units and learning contract

Original hosts are RoBERTa masked-subword LMs, GPT-2 autoregressive subword LM and AraBERT masked-subword LM. Probe input is one embedding per vocabulary type; output and supervision are character sequences including vocabulary boundary markers such as leading-space or continuation markers. Probe inference is left-to-right within a spelling, not the host's natural generation path. The comparison intervention's input and targets remain subword tokens with masked positions; not a byte-level generator, not a multilingual causality experiment. Exact Unicode preprocessing or grapheme segmentation is not established. Input/output tying in each host is not needed here and is not established by this source.

### Results and controls

- Table 1 p.5063: sample 1,000 held-out types, train on 32,000, average 10 random splits. With no related-word filter, exact-match (EM) is RoBERTa-base 27.3%, RoBERTa-large 31.8%, GPT-2-medium 32.9%, AraBERT-large 40.9%; corresponding chrF 44.7/48.7/51.6/62.3. Random-vector control EM is 0.0%, chrF 7.0.
- The similarity filter removes the top 20 nearest training vectors per test embedding; the lemma filter first applies similarity and then removes shared lemmas. For RoBERTa-large EM falls to 18.2%/17.7%, GPT-2 17.9%/16.5%, AraBERT 21.9%/19.5%. Arabic vs English is confounded by vocabulary, token length, objective and corpus; not a causal language comparison. Lemmatization itself is an external tool for filtering, not an LM training teacher (§3).
- Table 2 compares whole-word embeddings: without filtering RoBERTa-base EM 43.0 vs CharacterBERT 28.2 and GloVe 2.0; similarity filtered 9.6 vs 12.9 vs 1.6. Character-aware embedding is not uniformly superior, and spellability is not downstream competence. Figure 1 probes depend strongly on training-set size.
- §5/Figure 2: a separate probe confirms injected spellings with 93.5% EM; for Wikipedia masked-LM training, losses differ by <0.01 after 1,000 updates over this run. Training stops at ~16,000 steps / 24 hours with the 24hBERT setup. This is a negative result **for this initialization and MLM task**, not evidence that character access is never useful or that spelling loss cannot help downstream editing.
- Appendix B–C: high-frequency and short types are easier; length and frequency are correlated, and random controls yield partial n-gram matches. Appendix D manually inspects 100 errors and displays 20; errors can preserve prefixes/capitalization while still being wrong. Appendix E probe is a six-layer encoder-decoder, width 512, Adam for 1,000 steps, up to 1,024 tokens/batch, LR 5e-4, dropout 0.1. §2 calls it a Transformer decoder and Appendix E calls it encoder-decoder: preserve the description difference; implementation architecture is unverified.
- Teacher or probe training cost is separate from host training; absolute GPU hardware, original model pretraining compute and byte-normalized exposure are not reported in this paper. No probability assertion about byte-chain likelihood follows.

### BIP implication

For BIP-0229 retain **probe-decodable but not necessarily directly accessible** information and strong filtering sensitivity. For BIP-0230 retain the null masked-LM initialization result as a matched intervention, not a universal negation of spelling-aware systems; compare its outcome with character-aware task-trained interventions only under their different tasks, objectives and budgets.


<details>
<summary>Prior catalog provenance and source aliases — historical depth, superseded by current receipt</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2022.naacl-main.373.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **P** original §§2–3, §5 and relevant result prose, not complete table/appendix verification. Teacher-forced transformer spelling decoder from frozen token embeddings; held-out types, random-vector baseline, similarity/lemma filters; separate spelling-pretrained embedding intervention. English and AraBERT Arabic; character inventory and normalization not established.
- **Learning and causal baseline:** **P** original §§2–3, §5 and relevant result prose, not complete table/appendix verification. Teacher-forced transformer spelling decoder from frozen token embeddings; held-out types, random-vector baseline, similarity/lemma filters; separate spelling-pretrained embedding intervention. English and AraBERT Arabic; character inventory and normalization not established.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0229](DETAILED_INVENTORY.md#BIP-0229), [BIP-0230](DETAILED_INVENTORY.md#BIP-0230).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S05/S05-N07**, [WORKS](../01_discovery/S05/WORKS.md) line 56: Models in a Spelling Bee: Language Models Implicitly Learn the Character Composition of Tokens; Itzhak and Levy; [NAACL 2022](https://aclanthology.org/2022.naacl-main.373/), pp.5061–5068; [PDF](https://aclanthology.org/2022.naacl-main.373.pdf)
  - Original register aliases / era / family / provenance: S05-N07
  - Source-scoped evidence/depth: **P** original §§2–3, §5 and relevant result prose, not complete table/appendix verification. Teacher-forced transformer spelling decoder from frozen token embeddings; held-out types, random-vector baseline, similarity/lemma filters; separate spelling-pretrained embedding intervention. English and AraBERT Arabic; character inventory and normalization not established.



</details>

<a id="BIW-0111"></a>
## BIW-0111 — Tokenization counts: the impact of tokenization on arithmetic in frontier LLMs

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2402.14903v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **A+P opening** [HTML](https://arxiv.org/html/2402.14903v1) title, abstract, Figure 1 caption. Decimal digit chunks in subword LMs, comma-enforced right-to-left grouping and chain-of-thought-inspired rewriting. GPT-3.5/4 March-2023 models, not a pure-byte controlled training comparison; later controls/appendix not read.
- **Learning and causal baseline:** **A+P opening** [HTML](https://arxiv.org/html/2402.14903v1) title, abstract, Figure 1 caption. Decimal digit chunks in subword LMs, comma-enforced right-to-left grouping and chain-of-thought-inspired rewriting. GPT-3.5/4 March-2023 models, not a pure-byte controlled training comparison; later controls/appendix not read.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0231](DETAILED_INVENTORY.md#BIP-0231).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S05/S05-N08**, [WORKS](../01_discovery/S05/WORKS.md) line 57: Tokenization counts: the impact of tokenization on arithmetic in frontier LLMs; Aaditya K. Singh, DJ Strouse; [2402.14903v1](https://arxiv.org/abs/2402.14903v1), 2024-02-22
  - Original register aliases / era / family / provenance: S05-N08
  - Source-scoped evidence/depth: **A+P opening** [HTML](https://arxiv.org/html/2402.14903v1) title, abstract, Figure 1 caption. Decimal digit chunks in subword LMs, comma-enforced right-to-left grouping and chain-of-thought-inspired rewriting. GPT-3.5/4 March-2023 models, not a pure-byte controlled training comparison; later controls/appendix not read.

<a id="BIW-0112"></a>
## BIW-0112 — Tokenization Falling Short: On Subword Robustness in Large Language Models

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2024.findings-emnlp.86.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **A** original abstract. Token structure, complex tasks and typo perturbations; BPE-dropout is the explicitly reported mitigation. Models, training exposure, task language and dropout protocol unresolved.
- **Learning and causal baseline:** **A** original abstract. Token structure, complex tasks and typo perturbations; BPE-dropout is the explicitly reported mitigation. Models, training exposure, task language and dropout protocol unresolved.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0232](DETAILED_INVENTORY.md#BIP-0232).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S05/S05-N09**, [WORKS](../01_discovery/S05/WORKS.md) line 58: Tokenization Falling Short: On Subword Robustness in Large Language Models; Chai, Fang, Peng, Li; [Findings EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.86/), pp.1582–1599
  - Original register aliases / era / family / provenance: S05-N09
  - Source-scoped evidence/depth: **A** original abstract. Token structure, complex tasks and typo perturbations; BPE-dropout is the explicitly reported mitigation. Models, training exposure, task language and dropout protocol unresolved.

<a id="BIW-0113"></a>
## BIW-0113 — The Strawberry Problem: Emergence of Character-level Understanding in Tokenized Language Models

- **Reading status:** NF — returned new scoped FULL (R10), actual card read for integration; no fresh original-paper credit to inventory owner.
- **Carrying card:** [R10/BIW-0113](../03_reading/R10/BIW-0113.md).
- **Current units: input / internal / output / supervision:** Tokenizedsyntheticeditinginputs pluscharactersofcurrent/pastobservedtokens / block-causalcharacterTransformer andcrossattention todecoder / tokenIDs / supervised19transformationtasks, no raw-byte LM.
- **Canonical records:** [BIP-0233](DETAILED_INVENTORY.md#BIP-0233).

### Current card-grounded detail

**Reading status: FULL** for [EMNLP 2025 proceedings PDF](https://aclanthology.org/2025.emnlp-main.1434.pdf), pp. 28252–28263, §§1–5, Figures 1–8, Tables 1–2, limitations and Appendix A Tables 3–4. [PDF](../03_reading/R10/sources/BIW-0113.pdf), [text](../03_reading/R10/sources/BIW-0113.txt); [Figures 3–5](../03_reading/R10/sources/BIW-0113-p7.png), [Figures 6–7](../03_reading/R10/sources/BIW-0113-p8.png), [Table 2/Figure 8](../03_reading/R10/sources/BIW-0113-p9.png) visually checked. No code or reproduction. [BIP-0233](DETAILED_INVENTORY.md#BIP-0233).

### Problem → solution → techniques

Can a token LM learn access to a token's constituent characters efficiently, and is a direct character channel useful? The authors train 19 supervised synthetic transformations (seven word-level and 12 character-level) and compare a vanilla decoder with one augmented by character information. Their **specific architecture** (§3.3/Fig. 2) is a one-block character Transformer with block-causal self-attention, learnable within-token positions and inter-token alignment embeddings; its representations are passed to token states through block-causal cross-attention at each main layer. Characters of the **current consumed token and all past tokens** are visible; future-token characters are masked. Output remains autoregressive **subword/token IDs**. The small character module does not directly generate bytes or replace the subword output vocabulary.

The paper applies concept-percolation analysis as a theory/analogy for a delayed transition, not as a separately implemented model component. A percolation fit/curve collapse does not establish the sole cause of spelling failures, a measured intrinsic mutual-information value, or mechanism identity with commonsense learning. Its §3.1 reporting-bias/information account is an author interpretation, not an experimentally isolated effect of tokenization.

### Units and causal evaluation

Synthetic vocabulary comprises single ASCII-like characters, digits, space, task tokens, and randomly constructed fixed-length word IDs; held inputs and targets can be token→token, token→characters, characters→token, or mixed. The main LM predicts token IDs autoregressively in a **supervised transformation sequence**; spelling strings are accessible as side input for already supplied/generated IDs. Bidirectional access *within the current input token* is permitted because it is already observed, but future token characters cannot be consulted for next-token prediction. Strict output alignment, special-token shifts and deployed preprocessing need code-level verification. It is not a pretrained raw-byte LM, and its direct supervision differs from natural unsupervised language modeling.

Training uniformly samples the 19 tasks for 750k iterations, batch 64, Adam learning rate 1e-5 with cosine decay (§3.4). Base decoder is 8 layers, width 512, 10M parameters excluding embedding matrices; the character block adds about 1M. Approximately 60 runs each take ~one day on a single A100; no matched-FLOP or production-serving latency is reported. Synthetic words are sampled uniformly, not Zipf-distributed; K∈{4,6,8}, vocabulary range described in §3.2. Appendix A gives the vocabulary and 16-word sentence generation algorithms.

### Evidence and limits

- Figures 3–5: vanilla character-task exact-match curves rise later as vocabulary and per-token length increase, whereas direct character information moves onset earlier and makes curves much less vocabulary-sensitive within these tested configurations. **Onset is accuracy >0.5%, not 50% or full task mastery** (§4). Figure 4 shows final accuracy and times still vary across configurations; do not assert a universal sharp phase transition from threshold choice alone.
- Table 2, K=4, vocabulary 8192: base 10M >750k steps vs 10M +1M character block 77k; base 150M 81k vs 150M +1M 20k. At vocabulary 16384: base 10M >750k vs 110k with character block; base 150M 110k vs 45k with block. Claims of ~15× parameter requirement refer to this narrow comparison and exclude the embedding matrices, not a measured 15× inference speedup.
- Figure 6: on 5M Wikipedia-sourced sentences with GPT-2 and LLaMA-2 tokenizers and the same synthetic editing objectives, the character-aware curve improves over nearly flat baseline, but **absolute exact match is only a few percent for character tasks at the graph endpoint**. This is real text input, not evidence of general pretrained LLM understanding or downstream-task preservation. Figure 7: mid-layer insertion works best in the experiment, and shrinking the character encoder to 1/8 width retains similar curves; quadratic character attention remains a cost and the suggested recurrent/local alternatives are not implemented results.
- Figure 8 and p.28260 use a rescaling by **sqrt(|V| × k)**, as verified visually; plain PDF text extraction dropped the square root. Curves collapse approximately in this constructed setup. The plotted correlation supports the proposed scaling interpretation, not proof of an exact law for production language models. Caption, visual figure and text discuss this square-root scale.
- The paper itself notes limitations from synthetic data and size. The reported evaluation does not show maintained natural-language quality, calibrated byte probabilities, equal-compute inference, larger models, end-to-end mixed-script generation, or causal ablation of tokenizer apart from changing the character-input channel; these are unreported, not negative results.

### BIP implication

BIP-0233 can now name block-causal character cross-attention and its precise visibility rather than an unspecified “lightweight change.” Link it to SpellingBee only as complementary evidence: trained-probe recoverability, task-supervised access, and organic next-token training are different claims. Specify the 0.5% threshold and controlled synthetic task, and avoid interpreting fitted graph percolation as an independently established causal explanation.


<details>
<summary>Prior catalog provenance and source aliases — historical depth, superseded by current receipt</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2025.emnlp-main.1434.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **A** original abstract. Nineteen synthetic character tasks; percolation-based concept-emergence interpretation and a lightweight architecture modification. **Modification unspecified at this depth**; do not invent character CNN/auxiliary head. Claimed causal account needs methods/controls, especially against CharBench.
- **Learning and causal baseline:** **A** original abstract. Nineteen synthetic character tasks; percolation-based concept-emergence interpretation and a lightweight architecture modification. **Modification unspecified at this depth**; do not invent character CNN/auxiliary head. Claimed causal account needs methods/controls, especially against CharBench.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0233](DETAILED_INVENTORY.md#BIP-0233).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S05/S05-N10**, [WORKS](../01_discovery/S05/WORKS.md) line 59: The Strawberry Problem: Emergence of Character-level Understanding in Tokenized Language Models; [EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1434/)
  - Original register aliases / era / family / provenance: S05-N10
  - Source-scoped evidence/depth: **A** original abstract. Nineteen synthetic character tasks; percolation-based concept-emergence interpretation and a lightweight architecture modification. **Modification unspecified at this depth**; do not invent character CNN/auxiliary head. Claimed causal account needs methods/controls, especially against CharBench.



</details>

<a id="BIW-0114"></a>
## BIW-0114 — CharBench: Evaluating the Role of Tokenization in Character-Level Tasks

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Omri Uzan and Yuval Pinter, AAAI 2026, 40(39), pp. 33296–33304, [official PDF](https://ojs.aaai.org/index.php/AAAI/article/download/40615/44576), DOI 10.1609/aaai.v40i39.40615; S05-N11; backlink [BIP-0234](DETAILED_INVENTORY.md#BIP-0234). Additional author preprint [arXiv 2508.02591v3](https://arxiv.org/pdf/2508.02591v3), with appendix, is separately version-scoped and not presumed identical to the proceedings.

**Reading: FULL** for the fixed proceedings §§Introduction–Limitations, Tables 1–3 and Figures 1–5, plus supplementary author preprint v3 Appendix A–D and Figures 6–15 (visually checked). Table 3 and Figures 3–5 in the proceedings also visually checked. Appendix figures have caption/plot-label mismatches described below, and a complete version-to-proceedings comparison was not conducted. The authors’ evaluation/parser code and dataset were not read; parser validity, valid-evaluation exclusion counts, baseline guessing floors and model version snapshots are not established. FULL denotes reading, not verification.
- **Carrying card:** [R07/BIW-0114](../03_reading/R07/BIW-0114.md).
- **Canonical problem records:** [BIP-0234](DETAILED_INVENTORY.md#BIP-0234).
- **Units — input / internal / output / supervision (current):** Englishstringquestions tokenizedbysubword LMs / pretrainedcausalLMstates / numerictextanswers / deterministictasklabelsforpromptedevaluation, no modeltraining/nativebytearm.

### Current substantive interface, technique, evidence and limits

**Reading: FULL** for the fixed proceedings §§Introduction–Limitations, Tables 1–3 and Figures 1–5, plus supplementary author preprint v3 Appendix A–D and Figures 6–15 (visually checked). Table 3 and Figures 3–5 in the proceedings also visually checked. Appendix figures have caption/plot-label mismatches described below, and a complete version-to-proceedings comparison was not conducted. The authors’ evaluation/parser code and dataset were not read; parser validity, valid-evaluation exclusion counts, baseline guessing floors and model version snapshots are not established. FULL denotes reading, not verification.

### Problem and solution

**Problem:** apparent language-model failures in character counting or finding positions are often blamed on subword tokenization, despite confounding word length, target count and pretrained model differences. **One-sentence solution:** construct deterministic large-scale English string questions and correlate per-item accuracy with word, label and tokenization features across different models without perturbing strings.

The benchmark samples 175,000 MiniPile strings stratified length 4–10 characters, creates four template tasks (frequency count, unique-character count, first and last occurrence with zero-based indices), and grades numeric output against deterministic Python-like answers (§CharBench, Table 1). The preprint v3 Appendix A instructs answer only the final number and explicitly treats case as distinct; Appendix B uses intersection-over-union of errors on valid evaluations only, C signed numeric error, D mixed-case indicators. The exact parser, handling of malformed responses and exclusion rates remain unknown. English only; character definition, Unicode normalizations and precisely which MiniPile filters apply are not fully reported in proceedings.

**Models/units:** seven prompted autoregressive LMs (GPT-4o, GPT-4o-mini, GPT-3.5-turbo, DeepSeek-V3, Llama-3.3-70B, Llama-3.1-405B, Mistral-7B) use BPE subword inputs/internal sequence and generated numeric text outputs. This is not an architecture intervention; no controlled native byte model. Each prompt is visible before answer, output is causal generation, temperature 0. No external model teacher, verifier beyond deterministic computed answers, or training carried out by this benchmark. Pretraining/finetuning text, total FLOPs and API cost remain unknown; external API models may not be perfectly deterministic even at temperature zero. Input↔output embedding sharing, cross-head sharing and exact decoder EOS are unreported for the actual evaluated model versions.

### Evidence and independent assessment

- Table 2: seven-model average 77.34% frequency counting, 47.96% unique count, 43.64% first and 32.37% last position, overall 50.33%. GPT-4o overall 70.73%, first 64.65%, last 63.14%; Mistral-7B frequency 71.65% exceeds Llama-3.3-70B 61.90% despite lower overall (34.72 vs 39.98). No majority or random guessing comparator is provided; class distributions and valid-output filtering are needed before estimating floors.
- Table 3 reports **univariate Pearson** correlations of binary correctness with word length (WL), gold answer (GT), GT/WL, number of tokens (NT), compression ratio and target-token character length (TTL). GPT-4o frequency correctness versus GT −.340, WL −.099, NT .009; first occurrence versus TTL −.245, WL −.136, GT −.170; last occurrence TTL −.259, WL −.180. Figure 3 visually shows lower positional accuracy for longer target tokens, but also varying word length; it is not a matched randomized intervention. Across-model average first occurrence GT −.306 has greater magnitude than TTL −.230, and last WL −.185 exceeds TTL −.148. Therefore the stronger claim that TTL dominates all models/tasks is false; it is strongest among listed features for GPT-4o in both indexing tasks.
- Error-set overlaps Figure 5 are nonzero even for counting (~.12–.31 between distinct models), and substantially higher for many last-position pairs (~.32–.74); do not restate 'negligible' as literally zero. Preprint D flags mixed case differently for count and indexing; its bars show both positive and negative associations depending on task/model. In preprint Figures 8/9 and 12/13 the captions swap the counting-task names relative to the plotted chart titles; use caution assigning numerical values to tasks. The published Figure 3 caption says accuracy by word length but plot includes target-token length; Figure 4 caption mentions spread although plotted variables are gold truth, word length, token count.
- Gold answers, queried index, word length, corpus frequency and segmentation co-vary; per-feature correlations do not identify independent causal effects, and conditioning an analysis on observed labels is not a controlled tokenizer retrain. Nor do weak aggregate token-count associations prove tokenization irrelevant. Do not infer mechanisms of Strawberry or SpellingBee from this work's related-work citations.

**BIP-0234:** retain task-dependent observational relationships, no byte comparator, case/English limitations, missing chance baselines and parser implementation, as well as exact model-specific counterexamples. Compare matched word lengths and labels and run controlled interface interventions before causal attribution.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://ojs.aaai.org/index.php/AAAI/article/download/40615/44576. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** **A** original journal/conference page. Counting versus positional character tasks; token features weakly correlate with counting correctness, word length/count matter more; containing-token length negatively correlates with positional success. Correlational evidence, no matched byte/subword retraining established.
- **Learning and causal baseline:** **A** original journal/conference page. Counting versus positional character tasks; token features weakly correlate with counting correctness, word length/count matter more; containing-token length negatively correlates with positional success. Correlational evidence, no matched byte/subword retraining established.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0234](DETAILED_INVENTORY.md#BIP-0234).
- **Reading ownership:** [R07](batches/R07.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S05/S05-N11**, [WORKS](../01_discovery/S05/WORKS.md) line 60: CharBench: Evaluating the Role of Tokenization in Character-Level Tasks; Omri Uzan, Yuval Pinter; [AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/40615), 40(39):33296–33304, DOI 10.1609/aaai.v40i39.40615, published 2026-03-14
  - Original register aliases / era / family / provenance: S05-N11
  - Source-scoped evidence/depth: **A** original journal/conference page. Counting versus positional character tasks; token features weakly correlate with counting correctness, word length/count matter more; containing-token length negatively correlates with positional success. Correlational evidence, no matched byte/subword retraining established.

</details>

<a id="BIW-0115"></a>
## BIW-0115 — Unicode Standard Annex #15: Unicode Normalization Forms (revision 57)

- **Entity / provenance:** standard; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://www.unicode.org/reports/tr15/tr15-57.html. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Unicode code points / canonical or compatibility decomposition/composition / normalized code points / none (deterministic, not lossless original-byte preservation).
- **Learning and causal baseline:** No learned signal. Normalization can be many-to-one; task-equivalence permission must be specified before calling changed text robust or exactly preserved.
- **Reading status:** N — selected normative text. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0218](DETAILED_INVENTORY.md#BIP-0218).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S05/S05-U02**, [WORKS](../01_discovery/S05/WORKS.md) line 69: [UAX #15, Unicode Normalization Forms, revision 57](https://www.unicode.org/reports/tr15/tr15-57.html), Unicode 17.0.0, 2025-07-30; **N**, §§1.1–1.2 and compatibility-loss warning
  - Original register aliases / era / family / provenance: S05-U02
  - Source-scoped evidence/depth: Canonical versus compatibility equivalence, NFC/NFD/NFKC/NFKD; normalization is a deterministic many-to-one interface policy, not free semantic robustness. Full annex not read.

<a id="BIW-0116"></a>
## BIW-0116 — Unicode Standard Annex #29: Unicode Text Segmentation (revision 47)

- **Entity / provenance:** standard; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://www.unicode.org/reports/tr29/tr29-47.html. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Unicode code points / versioned boundary algorithm / extended grapheme clusters / none (normative segmentation with possible tailoring).
- **Learning and causal baseline:** No learned signal. Segmentation uses versioned context/rules, and a scalar boundary is not always a grapheme boundary.
- **Reading status:** N — selected normative text. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0217](DETAILED_INVENTORY.md#BIP-0217).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S05/S05-U03**, [WORKS](../01_discovery/S05/WORKS.md) line 70: [UAX #29, Unicode Text Segmentation, revision 47](https://www.unicode.org/reports/tr29/tr29-47.html), Unicode 17.0.0, 2025-08-17; **N**, §§1–3 introductory/conformance passages and Table 1a
  - Original register aliases / era / family / provenance: S05-U03
  - Source-scoped evidence/depth: Code points versus extended grapheme clusters, Indic/Hangul/combining examples, documented tailoring. Full boundary rule implementation/tests not read; clusters approximate rather than universally define user-perceived characters.

<a id="BIW-0117"></a>
## BIW-0117 — Perceiver IO: A General Architecture for Structured Inputs & Outputs

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Andrew Jaegle, Sebastian Borgeaud, Jean-Baptiste Alayrac, Carl Doersch, Catalin Ionescu, David Ding, Skanda Koppula, Daniel Zoran, Andrew Brock, Evan Shelhamer, Olivier Hénaff, Matthew M. Botvinick, Andrew Zisserman, Oriol Vinyals, João Carreira, *Perceiver IO: A General Architecture for Structured Inputs & Outputs*, [arXiv 2107.14795v3](https://arxiv.org/pdf/2107.14795v3), 15 March 2022, ICLR 2022. Aliases S06/S06-N02, S07/S07-N10. **Reading: FULL**: PDF pp.i–xxix, §§1–5 and appendices A–I, with detailed focus on language §4.1, Appendices D/E/F, Tables 1/2/11–15, Figure 7; Table 1 visually checked. PDF extractor emitted font warnings and some diagrams were illegible as text; numerical Table 1 was rendered, language results are readable. Non-language demonstration video supplement was not opened; it is not required to resolve the language experiment. Full reading does not certify code, weights, source sequence equality, or reproductions.

Read–process–write attention (§3; Fig.2): learned latent queries cross-attend to M input vectors, L Transformer-style self-attention blocks process N latents, and O output queries cross-attend to latents, producing one output per query. Attention's principal term is O((M+O+LN)NF) at fixed feature width F (Appendix E.2), not input-independent cost or a guarantee of constant end-to-end runtime. Output queries can be position, task or input-feature conditioned; output positions are parallel conditional on the same latent. Output subsampling can reduce train cost, demonstrated in multimodal autoencoding (§3.2), not established as the actual language training setup.
- **Carrying card:** [R01/BIW-0117](../03_reading/R01/BIW-0117.md).
- **Canonical problem records:** [BIP-0121](DETAILED_INVENTORY.md#BIP-0121), [BIP-0122](DETAILED_INVENTORY.md#BIP-0122), [BIP-0123](DETAILED_INVENTORY.md#BIP-0123), [BIP-0258](DETAILED_INVENTORY.md#BIP-0258).
- **Units — input / internal / output / supervision (current):** 2048UTF-8bytes or512SentencePiece / 256learned latent slots, deep latent selfattention / masked byte/subword IDs or query-specific task labels / 15%whitespace-word corruption,MLM and task labels.

### Current substantive interface, technique, evidence and limits

### Technique, interfaces and permissions

Read–process–write attention (§3; Fig.2): learned latent queries cross-attend to M input vectors, L Transformer-style self-attention blocks process N latents, and O output queries cross-attend to latents, producing one output per query. Attention's principal term is O((M+O+LN)NF) at fixed feature width F (Appendix E.2), not input-independent cost or a guarantee of constant end-to-end runtime. Output queries can be position, task or input-feature conditioned; output positions are parallel conditional on the same latent. Output subsampling can reduce train cost, demonstrated in multimodal autoencoding (§3.2), not established as the actual language training setup.

Language input is 2048 UTF-8 bytes plus special tokens or 512 SentencePiece tokens, with learned position features; 256 bytes + 4 specials. Internal representation is 256 latent vectors width 1280 for 26 processing layers (IO++) uses 40 layers and width 1536). Pretraining output queries are learned position-specific vectors; paper's Table 11 gives O=2048 or 512 queries although §4.1 describes one per masked input. Loss predicts masked byte or token identity, a classification output, and 15% whitespace-delimited words are selected for masking (§4.1, Appendix F.2–F.3). Input is the full corrupted sequence. The query position need not expose the gold byte, but the latent can contain right-hand **unmasked** context; this is bidirectional masked prediction, not a left-to-right byte probability or generative decoder. Downstream GLUE outputs use task-specific queries and classification/regression heads. EOS, partial byte prefix, sampling, verifier and inference-cache policy are not reported.

Sharing axes: task-specific query vectors and task-specific MLP heads are not evidence that byte embedding is tied to output classification or that all task heads share weights. Language-specific byte input ↔ masked-output projection and cross-depth latent-layer sharing are unspecified. Appendix A.1 explicitly shares ImageNet processing weights across repeated blocks, while A.2 JFT-pretrained ImageNet does not; neither result establishes language layer sharing. No language teacher or distillation is described.

### Atomic findings, evidence, and counterexamples

1. **[BIP-0121](DETAILED_INVENTORY.md#BIP-0121)** — Long bytes cause quadratic full-sequence attention: map inputs to a fixed-size latent attention workspace before deep processing. Table 1: FLOP-matched byte BERT 6 layers, 20M, 130B FLOPs, 2.9 training steps/s, GLUE 71.5; byte Perceiver 26 layers, 201M, 113B, 7.6 steps/s, 81.0. This is ~2.62× training step rate under the reported setup, not an equal-parameter comparison or generative serving benchmark. The FLOPs are theoretical inference-style model operations; Appendix D counts multiplies and adds separately. Exact language hardware is not stated in the language appendix; do not assume ImageNet's 64 TPUv3. Both use batch 2048 and the same optimization schedule, but raw text identity between tokenizations is not established.
2. **[BIP-0122](DETAILED_INVENTORY.md#BIP-0122)** — Outputs of different shapes need not inherit input indexing: query the latent with output positions or task vectors. SentencePiece BERT 110M/109B/81.1 vs byte Perceiver 201M/113B/81.0; same approximate compute, not same total parameters. Multitask query 81.8 vs separate-task 81.0 (Table 2), but train protocols differ. Standard task output heads remain task-specific; query/readout flexibility is not evidence of a shared generative vocabulary projection.
3. **[BIP-0123](DETAILED_INVENTORY.md#BIP-0123)** — Byte-level language representations may suffer information loss through the latent bottleneck. Appendix F Table 15: at roughly matched FLOPs, N=128,width 1920 gives 75.84 GLUE versus N=256,width 1280 gives 80.95 and N=512,width 896 gives 80.92; neither N nor width varies independently. A compact workspace is not automatically adequate. Table 14 shows task-level differences; e.g. byte IO++ MNLI matched 84.13 vs token BERT 85.56, even though overall IO++ 81.76 vs 81.14. English-only GLUE is not multilingual evidence.
4. **[BIP-0258](DETAILED_INVENTORY.md#BIP-0258)** — Query-based access exposes output-specific selection without rereading original source after encoding, but all source information available to outputs must already be in latents. Appendix F Figure 7 shows content- and position-selective encoder attention; it is not evidence of lossless storage or a multi-hop causal retrieval guarantee. Non-language Appendix I reports that even parallel output batching cannot avoid simultaneously encoding all inputs.

**Pretraining:** C4/English Wikipedia 70/30 token mixture, concatenate 10 documents then crop, 500k steps × 2048 batch, LAMB LR .00125, 1000 warmup, cosine decay, weight decay .01 (Appendix F.3, Table 12). 2048 bytes vs 512 subwords target roughly similar text, not verified exact matching. Perceiver IO++ 425M/241B/4.2 steps/s/81.8 is a larger budget, not a matched-FLOP uplift. Image/video/audio/StarCraft results do not establish byte language generation or text retrieval fidelity.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; recovery discovery reused, absent old W catalog. No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2107.14795v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** 2048 UTF-8 bytes or 512 SentencePiece tokens / 256 latent slots / masked byte positions or task logits / CE at masked positions chosen from 15% whitespace words.
- **Learning and causal baseline:** Bidirectional masked-source modeling, not AR byte generation. Whole-word corruption is a word prior despite byte alphabets; query-position outputs attend to shared latents.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0121](DETAILED_INVENTORY.md#BIP-0121), [BIP-0122](DETAILED_INVENTORY.md#BIP-0122), [BIP-0123](DETAILED_INVENTORY.md#BIP-0123), [BIP-0258](DETAILED_INVENTORY.md#BIP-0258).
- **Reading ownership:** [R01](batches/R01.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S06/S06-N02**, [WORKS](../01_discovery/S06/WORKS.md) line 49: **Perceiver IO: A General Architecture for Structured Inputs & Outputs**, Jaegle et al.; [2107.14795v3](https://arxiv.org/html/2107.14795v3),2022-03-15
  - Original register aliases / era / family / provenance: S06-N02; **recovery reuse**, address/readout A05
  - Source-scoped evidence/depth: §4.1: encoder/decoder cross-attention plus deep latent self-attention,26 processing layers in described token model; comparable FLOPs vs BERT; >2× byte-BERT wall-clock training speed,81.8 GLUE in higher-compute byte configuration. Full total-parameter/TPU table and appendix not audited. **P**.
- **S07/S07-N10**, [WORKS](../01_discovery/S07/WORKS.md) line 49: **Perceiver IO: A General Architecture for Structured Inputs & Outputs**; [2107.14795v3](https://arxiv.org/html/2107.14795v3), 2022
  - Original register aliases / era / family / provenance: S07-N10; **recovery reuse**
  - Source-scoped evidence/depth: P §§3–3.2 and §4.1 actually read; Tables 1–2 numbers not fully recovered in extracted text; original remaining sections/appendices not read. Already in recovery `03_ADDRESS_READOUT` A05.

</details>

<a id="BIW-0118"></a>
## BIW-0118 — Generating Long Sequences with Sparse Transformers

- **Reading status:** NF — returned new scoped FULL (R09), actual card read for integration; no fresh original-paper credit to inventory owner.
- **Carrying card:** [R09/BIW-0118](../03_reading/R09/BIW-0118.md).
- **Current units: input / internal / output / supervision:** enwik8bytes / full12,288byte positions with predefinedsparse causal edges / next-bytes / next-byteNLL; other image/audio tasks distinct.
- **Canonical records:** [BIP-0236](DETAILED_INVENTORY.md#BIP-0236), [BIP-0237](DETAILED_INVENTORY.md#BIP-0237).

### Current card-grounded detail

**Status: FULL**, [arXiv 1904.10509v1, 23 Apr 2019](https://arxiv.org/pdf/1904.10509v1), §§1–8, Figures 1–5 and Tables 1–4; the fixed v1 has no appendix. [PDF](../03_reading/R09/sources/BIW-0118.pdf), [extract](../03_reading/R09/sources/BIW-0118.txt). Image/audio examples are background; figure patterns and sample images were interpreted from source captions and descriptions, not numerically remeasured.

### Problem and causal mechanism

[BIP-0236](DETAILED_INVENTORY.md#BIP-0236): dense attention interactions scale quadratically in byte positions. Keep every input and next-output position but replace edges by predefined sparse causal patterns (§§3–5). A length-n sequence still has n byte states and categorical next-byte supervision; no learned patching, pooling, or fixed-size recurrent state is introduced. A current state may attend only at or before its input index; next symbol is the target. The paper does not specify an EOS or incomplete UTF-8 policy, runtime caching scheme, or input/output tying for the enwik8 experiment.

A p-factor pattern supplies short multi-layer paths between past and future positions, with O(n n^(1/p)) effective attention interactions under the construction, O(n√n) at p=2—not a claim that the *entire model* or measured generation has that cost. Strided attention combines a local window with periodic earlier positions. Fixed attention combines block-local access with selected summary positions from prior blocks; c=8,16,32 avoids the expressivity bottleneck of one summary (§4.3). Different heads can use different summaries. Sequential/interleaved, merged, and multiple-head implementations are described; multi-layer reachability is not equal to unrestricted dense attention's one-layer mapping.

[BIP-0237](DETAILED_INVENTORY.md#BIP-0237): practical scaling also uses preactivation residuals and 1/√(2N) residual-output initialization instead of the earlier deep-supervision approach; checkpoint/recompute attention and feed-forward activations in backward; block-sparse kernels, fused softmax and skipped causal upper triangle; FP32 master weights with FP16 activation/gradients, dynamic loss scaling, and FP32 query-key products when sampling (§§5.2–5.6). Adam, 5k warmup, gradient clipping 1, weight decay .01, cosine decay; normally eight V100s (§6). No claim of runtime verification from reading the paper.

### Evidence and costs

Enwik8 §7.2: first 90M bytes train, final 10M validation/test; context 12,288 bytes, 30 layers, 8 heads, d=512, dropout .4, stride 128 and c=32, merged fixed patterns, 80 epochs, ~95M parameters. Table 1: 0.99 BPB, compared with 1.06 Al-Rfou, 1.03/88M Transformer-XL and 0.99/277M Transformer-XL. Seeds 1–3 give 0.992 ± 0.001 as reported. These are not matched-compute experiments.

Table 2's enwik8 12,288-context comparisons: dense 1.00 BPB / **1.31 Time/Iter**, fixed 0.99 / **0.55 Time/Iter**, strided **1.13 / 0.35 Time/Iter**. Strided is the important negative: fewer interactions and smaller reported per-iteration number did not preserve text quality. The table gives **Time/Iter without a stated time unit**; do not silently label the numbers seconds, or call them per-byte inference/decode latency. Training versus evaluation phase is not explicitly defined by the table; it appears in a training comparison, not a measured serving benchmark. Exact batch/precision for this specific comparison is not stated. §7.2 Table 3 varies minimum evaluation context 6,144→12,160, with 0.9952→0.9908 BPB and progressively fewer positions scored in parallel. Those are scoring costs/context, not free fixed-cost improvements.

CIFAR-10 Table 2 reverses the text pattern: strided 2.80 versus dense 2.82 and fixed 2.85 bits/dim. §7.4/Table 4's million-position demonstration is **audio**, 1,048,576 positions with only 3M parameters and 2.99 bits/byte; not million-byte language modeling. Matched-quality batched serving, prefill, and measured generation latency are unreported.

### Implication

Fixed sparse attention plus actual kernels is a full-resolution alternative to shortening and fixed-state compression. Evaluate its quality and hardware cost at equal context and output units, and retain the text-specific strided failure rather than claiming sparsity always helps. Distinguish checkpointed training activation memory from persistent inference cache, as emphasized in the field audit.


<details>
<summary>Prior catalog provenance and source aliases — historical depth, superseded by current receipt</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1904.10509v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** enwik8 raw bytes / byte positions with fixed/strided sparse connectivity / bytes / autoregressive NLL; causal masks. Mixed-precision/checkpointing are explicit implementation techniques.
- **Learning and causal baseline:** enwik8 raw bytes / byte positions with fixed/strided sparse connectivity / bytes / autoregressive NLL; causal masks. Mixed-precision/checkpointing are explicit implementation techniques.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0236](DETAILED_INVENTORY.md#BIP-0236), [BIP-0237](DETAILED_INVENTORY.md#BIP-0237).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S06/S06-N05**, [WORKS](../01_discovery/S06/WORKS.md) line 52: **Generating Long Sequences with Sparse Transformers**, Child/Gray/Radford/Sutskever; [1904.10509v1](https://arxiv.org/html/1904.10509v1),2019-04-23
  - Original register aliases / era / family / provenance: S06-N05; **fresh discovery**
  - Source-scoped evidence/depth: §7.2:95M model,12288-byte context,80 epochs,0.992±.001BPB/3 seeds. Table 2 dense1.00/1.31 vs fixed.99/.55 vs strided1.13/.35 for loss/time-per-iteration; unit not displayed in extracted header, so do not silently label seconds.8V100 default training. **P**; no complete reproduction or serving timing.



</details>

<a id="BIW-0119"></a>
## BIW-0119 — Transformer-XL: Attentive Language Models beyond a Fixed-Length Context

- **Reading status:** NF — returned new scoped FULL (R09), actual card read for integration; no fresh original-paper credit to inventory owner.
- **Carrying card:** [R09/BIW-0119](../03_reading/R09/BIW-0119.md).
- **Current units: input / internal / output / supervision:** enwik8bytes,text8characters orworddatasets / currentpositions+per-layer stopped-gradient segment memories / nextunit of actualdataset / causalLM; RECL900/500/400/128 isWikiTextword metric.
- **Canonical records:** [BIP-0238](DETAILED_INVENTORY.md#BIP-0238).

### Current card-grounded detail

**Status: FULL**, text-interface scope. Primary source: [ACL 2019 formal paper, pp. 2978–2988](https://aclanthology.org/P19-1285.pdf), §§1–5, Figures 1–2 and Tables 1–9. That PDF cites but does not contain appendices. For the carrying appendix, separately read [arXiv 1901.02860v3, 2 June 2019](https://arxiv.org/pdf/1901.02860v3), Appendices A–E and Table 10; full formal/preprint equivalence is **not** asserted. [Local formal PDF](../03_reading/R09/sources/BIW-0119.pdf), [extract](../03_reading/R09/sources/BIW-0119.txt), [v3 PDF](../03_reading/R09/sources/BIW-0119-arxiv-v3.pdf) and [v3 extract](../03_reading/R09/sources/BIW-0119-arxiv-v3.txt). Attention-visualization figures in D were read through their descriptions and captions, not independently visually recertified. No code was run.

### Problem, solution and units

[BIP-0238](DETAILED_INVENTORY.md#BIP-0238): independent fixed windows fragment context during training and stride-one full-window rescoring repeats work. Reuse past segment activations as memory at each Transformer layer, and add relative-position attention scores to avoid confusing identical absolute positions across segments (§§3.1–3.3). This is neither learned grouping nor an unbounded fixed-size recurrent vector: each layer stores a sequence of past hidden states. The same formulation applies to different token units, but enwik8 is **raw bytes**, text8 cleaned 27-character text, and WikiText-103/lm1b/PTB are word units; do not pool their metrics.

For current segment, queries come from the current layer input; keys/values concatenate stopped-gradient cached earlier states with current layer input under a causal mask. The sequence advances in order. Cached values affect forward predictions, but **gradients do not pass into the prior segment**, and recurrence shifts down one layer per segment rather than being conventional same-layer RNN recurrence. Default memory length M equals segment length L in training and may span multiple segments or be enlarged for evaluation. Finite memory and layer depth bound accessible history for a given realization. Relative sinusoidal distances plus learned content/position biases and separate content/position key projections prevent the specific reset-position ambiguity; they do not establish an exact full-history model. Output/supervision are next-byte categorical predictions for enwik8, next word for word datasets. General §3 describes logits via word embeddings; actual byte-table aliasing is not independently established. EOS, UTF-8 repair and partial-prompt policy are unreported.

### Comparisons, budgets and negative controls

- Formal §4.1 Table 2: enwik8 12-layer / 41M / 1.06 bits per byte versus 12-layer Al-Rfou 44M / 1.11 and 64-layer Al-Rfou 235M / 1.06; 18-layer 88M / 1.03 and 24-layer 277M / 0.99. The largest reported attention length is 784 during training and 3,800 at evaluation. The reused context extends effective conditioning, but this is neither a same-FLOP nor a same-cache comparison. text8 Table 3 gives 1.08 bits/cleaned character for 277M versus 1.13 for 235M baseline.
- WikiText-103 Table 6 / arXiv Appendix A Table 10: with ~128M parameters, recurrence and their relative encoding reach PPL 26.77, while relative encoding without recurrence reaches 29.02 in the principal ablation; under **same GPU memory** with different backprop lengths, 26.77 versus 27.98. The comparison does not isolate independent effects under equal sequence length and total FLOPs. Table 7's shuffled-sentence word benchmark gives 25.2 with both, 25.7 with Shaw relative encoding, 27.1 without recurrence; it is not a byte-language ablation.
- Table 8's 900 vs 500/400 and 128 relative effective context length figures are **word positions** on WikiText-103 and model-group/threshold specific, not enwik8 bytes or a universal ability bound. Appendix C defines the best-short-context baseline, r=0.1 hard examples and 1% incremental relative-perplexity-gain stopping criterion.
- Table 9 and §3.2: Al-Rfou-style from-scratch fixed-window evaluator is reported 363× slower at attention length 800 and 1,874× at 3,800, measured per token on one GPU in the enwik8 discussion. This is an unusually favorable **uncached full-window recomputation baseline** versus reuse, not a modern matched-quality, matched-cache, batched-serving or end-to-end generation speedup. GPU model, batch, precision, absolute latency, total training FLOPs and cache memory are unreported in this table.
- arXiv Appendix B precomputes projections for relative distances and rearranges them to avoid naively repeating the positional projection per pair. It does not make all self-attention linear-time. Appendix D attention maps are not evidence that an output has causally copied a source; Appendix E samples are word-level WikiText, not enwik8 byte-generation measurements.

### Implication

Retain recurrence with stopped-gradient cache and relative position as a full-byte-resolution historical alternative to both sparse edges and hierarchical compression. Explicitly separate state persistence, test-time weight adaptation, cache storage, training activations, and real serving cost. No architectural variant here by itself proves effective unlimited memory.


<details>
<summary>Prior catalog provenance and source aliases — historical depth, superseded by current receipt</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/P19-1285.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** enwik8 bytes/text8 characters; other experiments words/subwords / cached prior-segment hidden states / respective symbols / causal LM with segment recurrence and relative positions. Precise gradient stop/cache treatment not newly read.
- **Learning and causal baseline:** enwik8 bytes/text8 characters; other experiments words/subwords / cached prior-segment hidden states / respective symbols / causal LM with segment recurrence and relative positions. Precise gradient stop/cache treatment not newly read.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0238](DETAILED_INVENTORY.md#BIP-0238).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S06/S06-N06**, [WORKS](../01_discovery/S06/WORKS.md) line 53: **Transformer-XL: Attentive Language Models beyond a Fixed-Length Context**, Dai et al.; [1901.02860v3](https://arxiv.org/abs/1901.02860),[ACL2019](https://aclanthology.org/P19-1285/)
  - Original register aliases / era / family / provenance: S06-N06; **fresh discovery**
  - Source-scoped evidence/depth: Original abstract verifies .99 enwik8 and1.08 text8; up-to1800× evaluation speed is abstract-wide/baseline-specific, not a modern byte serving guarantee. Total byte-config params/compute and timing protocol remain missing. **A**.



</details>

<a id="BIW-0120"></a>
## BIW-0120 — Character-based Neural Machine Translation

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/1511.04586v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Whitespace-bounded character composition → word vectors/translation attention → within-word character generation. Layer-wise embedding mimicry then full fine-tuning; IBM4 soft alignment supervision.
- **Learning and causal baseline:** Whitespace-bounded character composition → word vectors/translation attention → within-word character generation. Layer-wise embedding mimicry then full fine-tuning; IBM4 soft alignment supervision.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0244](DETAILED_INVENTORY.md#BIP-0244), [BIP-0263](DETAILED_INVENTORY.md#BIP-0263), [BIP-0264](DETAILED_INVENTORY.md#BIP-0264).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S07/S07-N02**, [WORKS](../01_discovery/S07/WORKS.md) line 41: **Character-based Neural Machine Translation**; [1511.04586v1](https://arxiv.org/html/1511.04586v1), 2015
  - Original register aliases / era / family / provenance: S07-N02; **new**
  - Source-scoped evidence/depth: P abstract and §§2.5–2.6 actually inspected. Title corrected against primary HTML; *Finding Function in Form* is a different referenced work, not this paper. Full experiments, vocabulary inventory and costs not read.

<a id="BIW-0121"></a>
## BIW-0121 — Achieving Open Vocabulary Neural Machine Translation with Hybrid Word-Character Models

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/1604.00788. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Mainly word translation, character recurrent components for rare source/unknown target words. Conditional fallback, not all-position byte processing.
- **Learning and causal baseline:** Mainly word translation, character recurrent components for rare source/unknown target words. Conditional fallback, not all-position byte processing.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0245](DETAILED_INVENTORY.md#BIP-0245).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S07/S07-N03**, [WORKS](../01_discovery/S07/WORKS.md) line 42: **Achieving Open Vocabulary Neural Machine Translation with Hybrid Word-Character Models**; [1604.00788v2](https://arxiv.org/abs/1604.00788), 2016
  - Original register aliases / era / family / provenance: S07-N03; **new**
  - Source-scoped evidence/depth: A; switching rule, gradients and fallback evaluation missing.

<a id="BIW-0122"></a>
## BIW-0122 — Char2Subword: Extending the Subword Embedding Space Using Robust Character Compositionality

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Gustavo Aguilar, Bryan McCann, Tong Niu, Nazneen Rajani, Nitish Keskar and Thamar Solorio. [arXiv 2010.12730v3, 24 September 2021](https://arxiv.org/pdf/2010.12730v3). Author names checked against PDF p.1; venue is not specified in this locked PDF, so not inferred. Alias S07-N04.

**Reading: FULL.** Entire PDF, §§1–6, Tables 1–6, Figures 1–5 and Appendices A–B; visually inspected pp.6–8 for Tables 2–5 and attention figure. `sources/BIW-0122.pdf` and `.txt`. This is an original-paper read, not a replication or model/code inspection.
- **Carrying card:** [R06/BIW-0122](../03_reading/R06/BIW-0122.md).
- **Canonical problem records:** [BIP-0247](DETAILED_INVENTORY.md#BIP-0247), [BIP-0248](DETAILED_INVENTORY.md#BIP-0248), [BIP-0249](DETAILED_INVENTORY.md#BIP-0249), [BIP-0250](DETAILED_INVENTORY.md#BIP-0250).
- **Units — input / internal / output / supervision (current):** Charactersinword/subwordspellings / characterTransformer-maxpool vectors→mBERTpositions / originalsubwordMLM/tasklabels / geometry/identitymimicry,frozenhostMLM,reapproximation; no bytegenerator.

### Current substantive interface, technique, evidence and limits

**Reading: FULL.** Entire PDF, §§1–6, Tables 1–6, Figures 1–5 and Appendices A–B; visually inspected pp.6–8 for Tables 2–5 and attention figure. `sources/BIW-0122.pdf` and `.txt`. This is an original-paper read, not a replication or model/code inspection.

### Actual units and architecture

A **character-compositional antecedent**, not a byte-level generative LM. Input composer operates over characters of words or subwords, with character embeddings and sinusoidal positions; character Transformer, linear projection, max-pooling and layer normalization output one vector per word/subword. The resulting sequence is consumed by a bidirectional mBERT host. Pretraining predicts original **subword-vocabulary** masked labels; downstream heads predict language-identification, POS, NER or sentiment labels. The paper calls inputs characters but does not specify exact Unicode normalization or whether indexing handles code points versus grapheme clusters; character alphabet coverage, unknown characters and maximum length are not specified. No autoregressive causality, byte output, EOS handling or verifier is claimed.

MLM adaptation uses the original subword output embedding matrix E as a fixed projection; host upper Transformer weights and E are frozen during this adaptation (§3.2 footnote 6), while gradients update the composer. This is *not* a generically tied character input/output table: composer and old fixed output table are different parameter objects. The original mBERT embedding table is retained in hybrid mode for known full words; full mode replaces the input table with the composer, although E is still used for the MLM supervision stage. Head sharing, layer sharing and downstream fine-tuning parameter permissions are not specified precisely enough to claim all models or modules are frozen during downstream fine-tuning.

### Four distinct problems and solutions

1. **[BIP-0247](DETAILED_INVENTORY.md#BIP-0247):** composed word vectors can disrupt the original host's learned geometry → imitate existing mBERT lexical embedding vectors using four explicitly distinct terms: cosine distance, vector L2 distance, squared error in cosine distances to ground-truth nearest neighbors, and token identity CE through fixed E (§3.1/Table 2). CE alone yields 58.1 average neighbor precision; all four 60.0, versus cosine-only 28.5. These are embedding-retrieval outcomes, not direct task accuracies.
2. **[BIP-0248](DETAILED_INVENTORY.md#BIP-0248):** spelling and casing changes can fragment words into misleading subwords → imitate the same reference embedding using single-character mistype, repeat, swap, drop, case-toggle or punctuation edits for vocabulary items longer than four characters; over 100 keyboard layouts for substitutions (Table 1). Table 3 qualitative `BUSINESS` example finds semantically closer neighbors with noise augmentation. The model does not train on every multi-edit variation, nor prove semantic invariance to all spelling changes.
3. **[BIP-0249](DETAILED_INVENTORY.md#BIP-0249):** static type-level imitation alone need not work within contextual host layers → run dynamic MLM through frozen mBERT using 1M Wikipedia sequences of 512 subword tokens, 200k each in English, Spanish, Hindi, Nepali and Arabic; 15% selected subwords with 80/10/10 character masking/random/unchanged. Figure 4 shows neighbor precision drops after contextualization, then re-approximating embeddings raises reported mean precision to 82.4. The last re-approximation matters; no claim that contextualization alone improves embedding-neighborhood fidelity.
4. **[BIP-0250](DETAILED_INVENTORY.md#BIP-0250):** composing every lookup may be unnecessary → hybrid routing uses original embeddings for recognized full words and composes whole unseen words instead of splitting them; full mode composes all input units (§3.3). On Hindi-English validation, Table 4 hybrid adapted vs mBERT: POS 89.64 vs 87.86, NER 74.91 vs 72.94; es-en NER 63.32 vs 62.66. Hybrid improvement does not isolate composer from its altered segmentation and training.

### Additional results, counterexamples and budgets

Table 4 held-out test: mBERT vs adapted hybrid average 82.23→83.03, es-en sentiment weighted accuracy 56.43→59.07, Hindi-English NER 72.57→73.38; not every column improves (es-en LID 98.36→98.33). On es-en sentiment validation DeepWordBug, mBERT drops 56.10→39.32, composer 57.71→45.30 (§5). Error analysis identifies ambiguity between languages sharing nearly identical forms; augmentation can erase distinctions. Table 5 Hindi-English POS development input length is 21.7 original word units vs 41.3 after subword tokenization; these do not measure wallclock or full text-compute parity.

§5 reports mBERT 177M total and 91M embedding-table parameters versus 50M composer (~45% reduction of that input component); hybrid retains the lookup table, so it does **not** realize this full replacement storage saving. The abstract says no inference-speed sacrifice, while §5 concedes composer needs more computation and reports no timing table; total memory, caching, hardware, FLOPs, training epochs/seed counts and downstream permissions remain unknown. A qualitative attention visualization (Fig.5) is illustrative, not a causal explanation. The paper's §5 error analysis says 112 English→Spanish and 101 Spanish→English, then calls the 101 English; retain the inconsistency rather than silently resolving it.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2010.12730v3. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Character Transformer + pooling predicts pretrained subword embedding geometry; frozen-mBERT MLM adaptation; full-word or hybrid fallback deployment.
- **Learning and causal baseline:** Character Transformer + pooling predicts pretrained subword embedding geometry; frozen-mBERT MLM adaptation; full-word or hybrid fallback deployment.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0247](DETAILED_INVENTORY.md#BIP-0247), [BIP-0248](DETAILED_INVENTORY.md#BIP-0248), [BIP-0249](DETAILED_INVENTORY.md#BIP-0249), [BIP-0250](DETAILED_INVENTORY.md#BIP-0250).
- **Reading ownership:** [R06](batches/R06.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S07/S07-N04**, [WORKS](../01_discovery/S07/WORKS.md) line 43: **Char2Subword: Extending the Subword Embedding Space Using Robust Character Compositionality**; [2010.12730v3](https://arxiv.org/html/2010.12730v3), 2021 revision of 2020 preprint
  - Original register aliases / era / family / provenance: S07-N04; **new**
  - Source-scoped evidence/depth: P §§3.1–3.3 actually read, not all experiments/appendices. Initial search snippet called it Findings EMNLP 2020; **do not carry that unverified venue label**. HTML author extraction is malformed; author list needs PDF check.

</details>

<a id="BIW-0123"></a>
## BIW-0123 — WECHSEL: Effective initialization of subword embeddings for cross-lingual transfer of monolingual language models

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2022.naacl-main.293.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** New target-language tokenizer + semantically initialized subword embeddings from multilingual static vectors; RoBERTa and GPT-2 transfer.
- **Learning and causal baseline:** New target-language tokenizer + semantically initialized subword embeddings from multilingual static vectors; RoBERTa and GPT-2 transfer.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0251](DETAILED_INVENTORY.md#BIP-0251).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S07/S07-N06**, [WORKS](../01_discovery/S07/WORKS.md) line 45: **WECHSEL: Effective initialization of subword embeddings for cross-lingual transfer of monolingual language models**; [NAACL 2022 formal page](https://aclanthology.org/2022.naacl-main.293/)
  - Original register aliases / era / family / provenance: S07-N06; **new**
  - Source-scoped evidence/depth: A formal abstract; “up to 64× less training effort” is author conditional claim, not a universal compute ratio.

<a id="BIW-0124"></a>
## BIW-0124 — FOCUS: Effective Embedding Initialization for Monolingual Specialization of Multilingual Models

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/2305.14481. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** New subword embeddings composed from shared-vocabulary anchors, chosen using static token semantic similarity and sparsemax.
- **Learning and causal baseline:** New subword embeddings composed from shared-vocabulary anchors, chosen using static token semantic similarity and sparsemax.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0252](DETAILED_INVENTORY.md#BIP-0252).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S07/S07-N07**, [WORKS](../01_discovery/S07/WORKS.md) line 46: **FOCUS: Effective Embedding Initialization for Monolingual Specialization of Multilingual Models**; [2305.14481v2](https://arxiv.org/abs/2305.14481), 2023
  - Original register aliases / era / family / provenance: S07-N07; **new**
  - Source-scoped evidence/depth: A; source XLM-R; precise optimizer/freezing/budget and low-overlap failure need original tables.

<a id="BIW-0125"></a>
## BIW-0125 — OFA: A Framework of Initializing Unseen Subword Embeddings for Efficient Large-scale Multilingual Continued Pretraining

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/abs/2311.08849. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Aligned multilingual static vectors initialize unseen subwords; matrix factorization limits embedding growth. Subword vocabulary adaptation, not byte generation.
- **Learning and causal baseline:** Aligned multilingual static vectors initialize unseen subwords; matrix factorization limits embedding growth. Subword vocabulary adaptation, not byte generation.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0253](DETAILED_INVENTORY.md#BIP-0253), [BIP-0254](DETAILED_INVENTORY.md#BIP-0254).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S07/S07-N08**, [WORKS](../01_discovery/S07/WORKS.md) line 47: **OFA: A Framework of Initializing Unseen Subword Embeddings for Efficient Large-scale Multilingual Continued Pretraining**; [2311.08849v2](https://arxiv.org/abs/2311.08849), 2024 revision
  - Original register aliases / era / family / provenance: S07-N08; **new**
  - Source-scoped evidence/depth: A; environment/carbon claim not independently cost-audited; disentangle initialization and factorization.

<a id="BIW-0126"></a>
## BIW-0126 — Zero-Shot Tokenizer Transfer

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** Benjamin Minixhofer, Edoardo M. Ponti and Ivan Vulić. [arXiv 2405.07883v2, 28 October 2025](https://arxiv.org/pdf/2405.07883v2). PDF mentions NeurIPS 2024; this card reports the locked v2 text rather than assuming the 2024 proceedings body is identical. Alias S07-N09.

**Reading: FULL.** Complete 22-page PDF §§1–7, Algorithm 1, Figures 1–6, Tables 1–14 and Appendices A–K, with visual reading of pp.6, 20–22. Source/extraction `sources/BIW-0126.*`; no experiments, proof or checkpoint verification performed.
- **Carrying card:** [R06/BIW-0126](../03_reading/R06/BIW-0126.md).
- **Canonical problem records:** [BIP-0255](DETAILED_INVENTORY.md#BIP-0255), [BIP-0256](DETAILED_INVENTORY.md#BIP-0256), [BIP-0257](DETAILED_INVENTORY.md#BIP-0257).
- **Units — input / internal / output / supervision (current):** Targetsubwords decomposedintooriginaltokenpieces / bidirectionalhypernetwork→targetinput/separateoutputembeddings→host / targetvocablogitsortasklabels / frozen-hostMLMorARCE+embeddingwarmup/anchors,optionalfullmodelcontinuation.

### Current substantive interface, technique, evidence and limits

**Reading: FULL.** Complete 22-page PDF §§1–7, Algorithm 1, Figures 1–6, Tables 1–14 and Appendices A–K, with visual reading of pp.6, 20–22. Source/extraction `sources/BIW-0126.*`; no experiments, proof or checkpoint verification performed.

### Input, model, objectives, timing and sharing axes

This is predominantly **subword tokenizer transfer**, not a byte-native LM. Target tokenizer maps input text to target subwords; a pretrained host consumes target-token embeddings and outputs target-subword logits (Mistral causal LM), or masked-token/class labels for bidirectional XLM-R. Hypernetwork input is each target token decomposed by the original tokenizer into original-token embeddings; transformed host representations remain target-token positions. Its output is the predicted target input embedding and, if needed, a **separate** target output embedding head (§§2–3). It can support either tied or untied host input/output tables, but no generic claim that all target models tie them is warranted; the manually untied GPT-2 experiment has two distinct prediction heads, Appendix B. The hypernetwork shares its Transformer across target vocabulary entries, not the input/output prediction heads. At transfer the predicted vocabulary tables can be computed once and used as static lookup/readout; its offline amortized cost is not zero. Explicit raw normalization, special IDs, EOS generation and cache policy depend on host/tokenizer and are not fully provided.

[**BIP-0255**](DETAILED_INVENTORY.md#BIP-0255): retraining a full host separately for every tokenizer is costly → pretrain a per-host hypernetwork across many sampled tokenizers, predict a new vocabulary's embeddings without training on that target tokenizer, and optionally continue training. Zero-shot refers to **target-tokenizer adaptation**, not a randomly initialized or untrained hypernetwork. Algorithm 1: rolling text queue of size n, current training batch within queue, enumerate substrings up to l without crossing pretokens, frequency plus Gaussian noise (noise scale lognormal), choose top 32768 and use UnigramLM; dependent text/tokenizer sampling prevents rare token starvation. A three-layer bidirectional Transformer composes source token embeddings for each target token; language-specific learned vector added for multilingual models. It does not condition directly on the tokenization function, instead amortizes over sampled functions. Original host's internal parameters ψ remain frozen during hypernetwork training while gradients traverse the host; task loss is masked LM or causal next-token CE plus overlapping-token anchor.

[**BIP-0256**](DETAILED_INVENTORY.md#BIP-0256): direct hypernetwork learning can be unstable → MIMICK-style squared-distance warmup against original embedding table then auxiliary squared-distance anchor for shared vocabulary items. Appendix B/Fig.3: **manually untied GPT-2** diverges without the anchor; original tied GPT-2 does not. This is not a general proof every untied LM diverges or that warmup alone explains the result. For optional n-shot, §4.1 describes 50k × 32 × 512 = 819.2M target-token presentations, 16,384 sampled output candidates and zero-shot embeddings as anchor; it explicitly refers to training the full model (§4.3), unlike frozen-host zero-shot transfer. Teacher model pretraining and target-tokenizer construction are additional costs.

[**BIP-0257**](DETAILED_INVENTORY.md#BIP-0257): original character-based tokenizers may not represent arbitrary invalid-UTF-8 target byte tokens → add missing byte symbols and initial BPE merges that reconstitute characters; added embedding rows are random and trainable. Appendix J Table 12 evaluates preservation on English MADLAD-400 **pretokens**, not all possible strings: BERT 99.6%, Mistral 99.9%, TinyLlama 99.9%, GPT-2 100%; additional rows 162/522/362/0. Unigramification is another lossy approximation trained through linear programming on 1M common pretokens, not equivalence for every input. §I restricts pretokenization by adapted GPT-2 regex, optional prefix spaces and whitespace spans up to 16; languages lacking whitespace are excluded from multilingual hypernetwork training, §4.1.

### Evidence, counterexamples and costs

Table 1 p.6 XLM-R XNLI original 72.6, lexical 63.3, FVT 68.4, FOCUS 68.6, hypernetwork 71.2; average target sequence length −14%. The paper derives >16% speedup as 1/(1−.14), not an independently timed end-to-end measurement (§4.2 footnote 11). Table 2 Mistral-7B natural-language average 76.9 original, 55.6 FOCUS, 73.0 zero-shot and 74.9 after 800M target-token presentations; HumanEvalPack average pass@1 28.1/13.3/23.2/27.6. Tokenizer and actual text/context differ. XCOPA Table 3 improves 54.6→57.1 on average but several language scores are near chance; multilingual MMLU Table 4 loses 8–15 points despite shorter sequences. Appendix F Figure 5 overlap probability still correlates with accuracy; weaker dependence than FOCUS is not independence. Table 6 Farsi loses six points despite unseen-language successes. Table 5 MT-Bench GPT-3.5 judge: original Mistral-Instruct 7.33, zero-shot transfer 6.56; TinyLlama chat Appendix H Table 11 5.5→4.0, clear incomplete transfer, not a universal compatibility guarantee.

Training 200k steps incl. 10k warmup, 128×128 sequences; English/code mixture 7:3 or 26-language corpus; XLM-R hypernetwork ~one day TPU v3-8, Mistral ~three days TPU v4-32 (§4.1). Table 14 Mistral hypernetwork 678M parameters vs 7.2B host. §5 estimates 252T host + 30T hypernetwork FLOPs per training batch for n=s=128, 32768 vocab entries × 7 decomposition positions, ≈12% extra **for that training batch**, not inference overhead per generated token. Target vocabulary generation, tokenizer construction, cached table storage and real serving break-even are not timed; claimed speed/quality improvements do not pay back the one-time hypernetwork expense automatically.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2405.07883v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Transformer hypernetwork composes source-token pieces into new input/output embeddings; task loss through pretrained backbone, embedding warmup/anchors; bytes added to ensure arbitrary decomposition.
- **Learning and causal baseline:** Transformer hypernetwork composes source-token pieces into new input/output embeddings; task loss through pretrained backbone, embedding warmup/anchors; bytes added to ensure arbitrary decomposition.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0255](DETAILED_INVENTORY.md#BIP-0255), [BIP-0256](DETAILED_INVENTORY.md#BIP-0256), [BIP-0257](DETAILED_INVENTORY.md#BIP-0257).
- **Reading ownership:** [R06](batches/R06.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S07/S07-N09**, [WORKS](../01_discovery/S07/WORKS.md) line 48: **Zero-Shot Tokenizer Transfer**; [2405.07883v2](https://arxiv.org/html/2405.07883v2), 2025 revision; NeurIPS 2024 is associated work, not automatic version equivalence
  - Original register aliases / era / family / provenance: S07-N09; **new**
  - Source-scoped evidence/depth: P §§2–3.2 actually read; §5 byte-conversion paragraph and Appendix B relevant paragraph located; all experiment tables and appendices not read.

**Identity spot-check in this consolidation:** official arXiv abstract https://arxiv.org/abs/2405.07883v2 was read in the built-in browser: Minixhofer/Ponti/Vulić; v1 2024-05-13, v2 2025-10-28. This validates identity/revision only, not methods/FULL. The audit P20 and S07 refer to this same entity.

</details>

<a id="BIW-0127"></a>
## BIW-0127 — T-FREE: Subword Tokenizer-Free Generative LLMs via Sparse Representations for Memory-Efficient Embeddings

- **Reading status:** NF — returned new scoped FULL (R10), actual card read for integration; no fresh original-paper credit to inventory owner.
- **Carrying card:** [R10/BIW-0127](../03_reading/R10/BIW-0127.md).
- **Current units: input / internal / output / supervision:** Regexword/digit/punctuation/whitespaceunits, exactbyte/Unicodehandling unverified / hashedbinarytrigramsets+word-timeTransformer / finite-dictionary-selectedwholeunits / multilabelBCEfeaturetargets;not bytechain.
- **Canonical records:** [BIP-0261](DETAILED_INVENTORY.md#BIP-0261).

### Current card-grounded detail

**Reading status: FULL** for [arXiv:2406.19223v2](https://arxiv.org/pdf/2406.19223v2), 7 January 2025: §§1–7, limitations, Figures 1–4, Table 1 and Appendices A–J, including algorithms 1–5, Tables 2–10 and Figures 5–16. [PDF](../03_reading/R10/sources/BIW-0127.pdf), [extracted text](../03_reading/R10/sources/BIW-0127.txt); [p.4](../03_reading/R10/sources/BIW-0127-p4.png), [p.6](../03_reading/R10/sources/BIW-0127-p6.png), [p.17](../03_reading/R10/sources/BIW-0127-p17.png), [p.21](../03_reading/R10/sources/BIW-0127-p21.png) visually inspected. The text extractor emitted malformed character encodings in graphical fragments, replaced in the UTF-8 text; claims below are checked against readable prose, pseudocode, tables and selected page images. No model code run. [BIP-0261](DETAILED_INVENTORY.md#BIP-0261).

### Problem → solution → AI techniques

Large corpus-trained subword input/output matrices and independently learned near-duplicate entries use memory, and a tokenizer's fixed inventory can transfer unevenly. T-FREE instead splits text into word-like units and uses sparse hashed overlapping character-trigram patterns to share representation across spelling-similar units. Its **Llama-2-like causal Transformer** predicts a multi-label pattern for the next unit, decoded by scoring a replaceable word dictionary (§§2–4). This is a word-level **hybrid textual interface**, neither an all-byte chain nor segmentation-free processing.

The authors use a rule-based regex splitter, padded trigram windows, multiple hashes modulo an independently chosen table size, summed learned rows for the input, a sigmoid multi-label binary cross-entropy (BCE) head, and sparse dictionary-matrix scoring of output patterns. A chosen subset of hash activations is computed on lowercase forms to couple capitalization variants (§3.1; Appendix A Algorithms 1–5). These mechanisms are actually used; morphological generalization and lower hallucination are interpretations, not verified semantic properties. Weight tying between input and output matrices is not established by §§3/A; do not infer it.

### Interface, probability, and collision contract

- **Units:** input unit is a regex-split word, digit, punctuation or special whitespace marker; its internal feature is a set of multiple hashed trigrams (paper says byte-wise stride, while examples and pseudocode describe characters; exact Unicode/byte handling remains unspecified without implementation inspection). The recurrent backbone step represents a complete unit. Supervision is the multi-hot feature pattern of the next unit, not a word-softmax cross-entropy or next-byte likelihood. Generation outputs dictionary-selected whole words/special units; whitespace/non-whitespace rules reconstruct text (Appendix B).
- A single input word can be hashed without being an entry in a trained word vocabulary. Output is more constrained: §3.2 builds a candidate dictionary with precomputed feature patterns, averages sigmoid feature scores per candidate and chooses/samples among candidates. Algorithm 5 applies softmax to these scores then argmax. Evaluation uses the top **80k English + 20k German** words (§4.1); §3.2 separately describes top 500k training words plus words from the prompt. These are different described candidate regimes, not evidence of unrestricted novel-word generation. Adding a prompt word to a dictionary is not unconstrained spelling. The induced categorical distribution is dictionary-dependent, not the independent-BCE training objective's normalized word distribution.
- §3.1 asserts unique trigram and word encodings. **Correction/qualification:** collision-free hash patterns for individual trigrams would not guarantee word-level injectivity after binary set aggregation: padded `aaaa` and `aaaaa` have the same distinct trigram set `{_aa, aaa, aa_}`. This is an analyst counterexample under the paper's stated padded set rule, not a measured collision in released code. Limitations §7 itself acknowledges repeated trigrams are accumulated only once. Hash collisions create an additional possibility; actual collision frequency is unreported. Thus the Fig. 1 caption's “bijective” statement is not a general proven property.
- Full-prompt input can be encoded and next complete-word choices are causal at the backbone step. Character-by-character continuation inside an unfinished unit, exact end-of-sequence behavior, arbitrary Unicode-preserving round-trip, and runtime caching are not established. No code execution is needed to mark the paper FULL.

### Experiments, positive and negative evidence

- §4.1: 1B ablations train 50k steps, sequence 2048, batch 1024; 3B training 90k English steps followed by 20k German with 20% English replay (Fig. 4 and Appendix D Table 3). §4.1 also says 110k steps on English before continuation; this is a **source conflict**, not resolved as 110k English plus 20k. Baselines use 32k/64k SentencePiece BPE/unigram trained on 20GB SlimPajama, with the baseline's Appendix C NFKC setting and byte fallback. Different unit lengths mean equal step/token budgets do not establish equal source-text exposure or total FLOPs.
- Figure 3: at v=8k, m=10, k=0, median benchmark difference vs 64k unigram is positive across 18 zero-shot tasks; ≤2k has large negative outliers. 8k-vs-64k is 12.5% of vocabulary-shaped embedding/head parameters, not total model: 0.84B vs 1.07B total. Figure 7 shows performance dips again above 8k; no universal monotonic capacity story.
- Appendix E Table 5: fertility uses UDPipe reference counts, not bytes or task accuracy; English 1.1636 vs unigram-64k 1.2802, German 1.1829 vs 2.0043. Other language values depend on script, reference segmentation and the compared tokenizer, not equality of language utility. §7 says Chinese and code downstream tasks were not evaluated; fertility alone is not generation quality.
- Figure 4's German improvement is a two-task HellaSwag/ARC-Challenge average; 20k continued German steps increase T-FREE by ~5 percentage points with little baseline improvement. Appendix J Table 8: German ARC-Challenge 0-shot rises from 24.3 to 32.0 T-FREE vs 22.5 to 25.7 unigram, while German XNLI is 37.1→35.7 vs 35.7→36.0. Do not generalize the two-task headline to every task. Both have English degradation on the plotted average.
- Appendix G Fig. 6: reported 68GB vs 38GB profiler peak for one 1B forward/backward, batch 8 and 4k positions, 64k vs 8k interface. Fig. 14 depicts Llama-3-8B/trigramified runtime accounting with 512k candidates, ~50 sparse entries each (~25M stored activations); it is an estimated/depicted pipeline, not a matched-quality serving benchmark. Head compression is offset by candidate scoring, dictionary memory and variable source-text/step length; prefill, concurrency and GPU details of serving are unreported.

### BIP implication

BIP-0261 should say **subword-tokenizer-free with rule-based word splitting and candidate-limited word outputs**. This is shared sparse lexical geometry, not learned byte patching. Retain candidate set, unnormalized feature-training versus candidate-decoding distinction, repeated-trigram noninjectivity, and English/German-only adaptation in any comparison.


<details>
<summary>Prior catalog provenance and source aliases — historical depth, superseded by current receipt</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2406.19223v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Words represented by sparse hashed character triplets; smaller embedding/head interface. **Character-derived word interface**, not pure-byte or ordinary subword output.
- **Learning and causal baseline:** Words represented by sparse hashed character triplets; smaller embedding/head interface. **Character-derived word interface**, not pure-byte or ordinary subword output.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0261](DETAILED_INVENTORY.md#BIP-0261).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S07/S07-N12**, [WORKS](../01_discovery/S07/WORKS.md) line 51: **T-FREE: Subword Tokenizer-Free Generative LLMs via Sparse Representations for Memory-Efficient Embeddings**; [2406.19223v2](https://arxiv.org/abs/2406.19223v2), 2025 revision
  - Original register aliases / era / family / provenance: S07-N12; **new**
  - Source-scoped evidence/depth: A; full decoding candidate-set mechanism and open-vocabulary guarantee unknown; title variants across search/HTML need formal PDF lock.



</details>

<a id="BIW-0128"></a>
## BIW-0128 — Mimicking Word Embeddings using Subword RNNs

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/D17-1010.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Spellings → compositional OOV word embeddings → supervised tagging; type-level embedding mimicry without original embedding corpus. Character/RNN role inferred only as far as title and abstract, not exact architecture.
- **Learning and causal baseline:** Spellings → compositional OOV word embeddings → supervised tagging; type-level embedding mimicry without original embedding corpus. Character/RNN role inferred only as far as title and abstract, not exact architecture.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0262](DETAILED_INVENTORY.md#BIP-0262).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S07/S07-N13**, [WORKS](../01_discovery/S07/WORKS.md) line 52: **Mimicking Word Embeddings using Subword RNNs**; [EMNLP 2017 D17-1010](https://aclanthology.org/D17-1010/), MIMICK
  - Original register aliases / era / family / provenance: S07-N13; **new**
  - Source-scoped evidence/depth: A formal abstract; objective form/architecture and complete language tables need full read.

<a id="BIW-0129"></a>
## BIW-0129 — Byte Pair Encoding is Suboptimal for Language Model Pretraining

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2020.findings-emnlp.414.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U BPE/unigram subwords → masked Transformer positions → masked subwords → denoising likelihood. C bidirectional masked modeling, not left-to-right generation.
- **Learning and causal baseline:** U BPE/unigram subwords → masked Transformer positions → masked subwords → denoising likelihood. C bidirectional masked modeling, not left-to-right generation.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0266](DETAILED_INVENTORY.md#BIP-0266).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S08/S08-W09**, [WORKS](../01_discovery/S08/WORKS.md) line 40: **Byte Pair Encoding is Suboptimal for Language Model Pretraining**, Bostrom & Durrett; [Findings EMNLP 2020 abstract](https://aclanthology.org/2020.findings-emnlp.414/), [PDF](https://aclanthology.org/2020.findings-emnlp.414.pdf). **A**.
  - Original register aliases / era / family / provenance: S08-W09 / S08-N07 / **NEW**
  - Source-scoped evidence/depth: **Byte Pair Encoding is Suboptimal for Language Model Pretraining**, Bostrom & Durrett; [Findings EMNLP 2020 abstract](https://aclanthology.org/2020.findings-emnlp.414/), [PDF](https://aclanthology.org/2020.findings-emnlp.414.pdf). **A**. Identical pretraining architecture in English/Japanese; unigram matches/beats BPE on downstream tasks, better morphology alignment. A counterexample to a particular subword algorithm, not to all tokenization. Budgets unknown.

<a id="BIW-0130"></a>
## BIW-0130 — Unpacking Tokenization: Evaluating Text Compression and its Correlation with Model Performance

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2024.findings-acl.134.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U character-to-BPE subwords → pretrained LM positions → task outputs (exact heads unknown here) → pretraining plus task fine-tuning. C not established in abstract.
- **Learning and causal baseline:** U character-to-BPE subwords → pretrained LM positions → task outputs (exact heads unknown here) → pretraining plus task fine-tuning. C not established in abstract.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0267](DETAILED_INVENTORY.md#BIP-0267).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S08/S08-W11**, [WORKS](../01_discovery/S08/WORKS.md) line 42: **Unpacking Tokenization: Evaluating Text Compression and its Correlation with Model Performance**, Goldman et al.; [Findings ACL 2024](https://aclanthology.org/2024.findings-acl.134/), pp.2274–2286. **A**.
  - Original register aliases / era / family / provenance: S08-W11 / S08-N09 / **NEW**
  - Source-scoped evidence/depth: **Unpacking Tokenization: Evaluating Text Compression and its Correlation with Model Performance**, Goldman et al.; [Findings ACL 2024](https://aclanthology.org/2024.findings-acl.134/), pp.2274–2286. **A**. Tokenizer training from 1M documents down to character baseline; English and Turkish subset. Compression correlates with task performance, more on generation/small models. Not an intervention proving compression is the only cause.

<a id="BIW-0131"></a>
## BIW-0131 — Tokenization Is More Than Compression

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source:** Craig W. Schmidt, Varshini Reddy, Haoran Zhang, Alec Alameddine, Omri Uzan, Yuval Pinter, Chris Tanner, EMNLP 2024, official proceedings pp. 678–702, [PDF](https://aclanthology.org/2024.emnlp-main.40.pdf); aliases S08/S08-W12. **Reading: FULL**, main §§1–7, limitations, Appendix A–G, especially A algorithms, B training configuration, D convergence, E segmentation/initialization, F random vocabulary controls, G Tables 4–14; PDF pp. 1–25 extracted and paginated; visually checked PDF pp. 6, 8, 25 (Tables 1/12–14, Figures 2/4–5). No missing author appendix in this version. FULL means paper reading, not reproduction or independent validation of code/claims.

- **Problem:** Is compression alone sufficient for an effective tokenizer? **One-sentence solution:** minimize the token count for a fixed vocabulary with a shortest-path segmenter, and manipulate vocabulary initialization, constraints and segmentation independently where possible.
- Byte-level **lossless subword tokenization**, not a native per-byte language model: all 256 single-byte strings are in each vocabulary as fallback; model inputs, internal positions, softmax outputs and next-token supervision are subword IDs. The model is causal next-token prediction over the resulting offline segmentation; document-global shortest-path segmentation need not be stable for an arbitrary raw-byte prefix. EOS, answer-likelihood normalization and partial-token prefix scoring are not specified sufficiently here; no verifier/sampling algorithm claimed. Input/output embedding tying not specified in the paper configuration; do not infer it from MPT. The vocabulary is built once, not learned end-to-end by the LM.
- **Borrowed methods and exact roles:** dynamic programming on a byte-position DAG finds the minimum-token segmentation, with max token length 16 and O(nL); tie-break longest or randomized. Top-down pruning estimates removal-cost by reusing forward/backward shortest-path information, O(nL²) per iteration, ignoring interacting nearby occurrences of the same token (Appendix A). A 262,144-item starting set is obtained from byte n-gram frequencies, BPE or unigram; preserve single bytes. This is heuristic vocabulary optimization, not a globally optimal vocabulary. Baselines use BPE merges, unigram likelihood/Viterbi, WordPiece greedy, SaGe contextual skip-gram vocabulary scoring; random-frequency-weighted RandTrain is a further control (Appendix F).
- 54 nominal 350M models = 18 configurations × 32,768/40,960/49,152 vocabulary sizes; six nominal 1.3B and four 2.4B models, all 40,960 vocabulary. These are not a complete factorial. Paper Appendix G Tables 12–13 display a **seventh 1.3B row** absent from Table 14 and the 64-model account; leave run-count discrepancy unresolved rather than reconciling silently. Additional eight RandTrain runs are discussed separately in ethics/F. Approx. 200B model tokens each, batch 1,024 × 2,048, AdamW, max context 2,048 subword positions, Pile pretraining; tokenizer learned on 6 GB MiniPile. Equal token counts do not ensure equal underlying text exposure or original-byte context: Appendix G Table 11 CTC varies 1.25–2.33B on the evaluated corpus. The raw training bytes actually retained per arm and per-arm FLOPs are not reported. 350M training ~48 h on 4 × 8 A100; 1.3B ~69 h on same; 2.4B ~117 h on 8 nodes. Ethics statement reports 138,432 GPU-hours across its broader set. Total vs nonembedding size, seeds and KV-cache/serving cost unreported.
- **Carrying card:** [R08/BIW-0131](../03_reading/R08/BIW-0131.md).
- **Canonical problem records:** [BIP-0268](DETAILED_INVENTORY.md#BIP-0268), [BIP-0269](DETAILED_INVENTORY.md#BIP-0269).
- **Units — input / internal / output / supervision (current):** Byte-completeBPE/unigram/PathPieceSUBWORDS / offline-segmentedcausalpositions / nextsubword / tokenCE; DPminimizestokencountforfixedvocabulary, notneural byte boundarylearning.

### Current substantive interface, technique, evidence and limits

### Interface, mechanism, and budgets

- **Problem:** Is compression alone sufficient for an effective tokenizer? **One-sentence solution:** minimize the token count for a fixed vocabulary with a shortest-path segmenter, and manipulate vocabulary initialization, constraints and segmentation independently where possible.
- Byte-level **lossless subword tokenization**, not a native per-byte language model: all 256 single-byte strings are in each vocabulary as fallback; model inputs, internal positions, softmax outputs and next-token supervision are subword IDs. The model is causal next-token prediction over the resulting offline segmentation; document-global shortest-path segmentation need not be stable for an arbitrary raw-byte prefix. EOS, answer-likelihood normalization and partial-token prefix scoring are not specified sufficiently here; no verifier/sampling algorithm claimed. Input/output embedding tying not specified in the paper configuration; do not infer it from MPT. The vocabulary is built once, not learned end-to-end by the LM.
- **Borrowed methods and exact roles:** dynamic programming on a byte-position DAG finds the minimum-token segmentation, with max token length 16 and O(nL); tie-break longest or randomized. Top-down pruning estimates removal-cost by reusing forward/backward shortest-path information, O(nL²) per iteration, ignoring interacting nearby occurrences of the same token (Appendix A). A 262,144-item starting set is obtained from byte n-gram frequencies, BPE or unigram; preserve single bytes. This is heuristic vocabulary optimization, not a globally optimal vocabulary. Baselines use BPE merges, unigram likelihood/Viterbi, WordPiece greedy, SaGe contextual skip-gram vocabulary scoring; random-frequency-weighted RandTrain is a further control (Appendix F).
- 54 nominal 350M models = 18 configurations × 32,768/40,960/49,152 vocabulary sizes; six nominal 1.3B and four 2.4B models, all 40,960 vocabulary. These are not a complete factorial. Paper Appendix G Tables 12–13 display a **seventh 1.3B row** absent from Table 14 and the 64-model account; leave run-count discrepancy unresolved rather than reconciling silently. Additional eight RandTrain runs are discussed separately in ethics/F. Approx. 200B model tokens each, batch 1,024 × 2,048, AdamW, max context 2,048 subword positions, Pile pretraining; tokenizer learned on 6 GB MiniPile. Equal token counts do not ensure equal underlying text exposure or original-byte context: Appendix G Table 11 CTC varies 1.25–2.33B on the evaluated corpus. The raw training bytes actually retained per arm and per-arm FLOPs are not reported. 350M training ~48 h on 4 × 8 A100; 1.3B ~69 h on same; 2.4B ~117 h on 8 nodes. Ethics statement reports 138,432 GPU-hours across its broader set. Total vs nonembedding size, seeds and KV-cache/serving cost unreported.

### Results and counterexamples

- **BIP-0268:** On 10 English 5-shot multiple-choice tasks, not open-ended generation, Appendix G Table 11 gives no-pretokenization PathPieceR 40,960: 1.26B corpus tokens and 44.0% average; BPE merge 1.49B and 50.0%. Globally Pearson correlation of token count with accuracy is +0.241 (Table 2): shorter is not a sufficient general quality criterion, not evidence that computational compression lacks benefit. Equal token training and tokenizer differences confound both data exposure and computation. Top five methods were not individually significantly inferior to all others under the authors’ one-sided signed-rank testing; 30 task-by-vocabulary observations are not 30 independent training seeds (§5.2).
- **BIP-0269:** At 40,960, same BPE vocabulary with merge/greedy/PathPieceL yields 50.0/49.1/46.7% (Appendix E Fig. 8, Table 6); Unigram likelihood/greedy/PathPieceL 49.1/48.5/43.1% at this size (Table 6). Thus changing only inference segmentation can reverse compression-derived expectations. Initial BPE is better than initial Unigram or n-gram for PathPieceL (p≤0.01, §6.3); none vs FirstSpaceDigit vs SpaceDigit is not pure one-variable control because digit pre-tokenization is also present in the latter two. Space-separated and nonspace-delimited languages cannot be generalized from English.
- Appendix F: with BPE initialization RandTrain+greedy 48.596 versus SaGe 49.154, p=.0645; no significant SaGe improvement. PathPieceL+BPE 49.373 versus RandTrain+PathPieceL 46.46, p=.0137; poorly performing RandTrain+PathPieceL for n-gram initialization limits other comparisons. Digit constraint hurts SaGe n-gram in one test (p=.025) but is not significant in another (p=.54).
- At 40,960, BPE/PathPieceL-BPE/SaGe-BPE/Unigram give 50.0/49.4/49.2/49.1% at 350M, 53.1/49.2/52.2/52.4% at 1.3B, 54.2/52.7/55.0/54.7% at 2.4B (Table 14). An anomalous 1.3B 100k checkpoint is acknowledged (§ limitations, Fig. 7), so ranking reversals and significance are not definitive cross-scale laws.

**Inventory instruction:** retain separate compression-sufficiency and three-stage-design records; annotate token budgets, English/task restriction and the above strong controls/negative results. Do not turn morphological alignment speculation into a measured mechanism or use this as evidence about a pure-byte decoder.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2024.emnlp-main.40.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U subword sequences via PathPiece/BPE variants → LM positions → LM/task outputs → pretraining; precise losses/optimizer unknown. C exact original protocol not inspected.
- **Learning and causal baseline:** U subword sequences via PathPiece/BPE variants → LM positions → LM/task outputs → pretraining; precise losses/optimizer unknown. C exact original protocol not inspected.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0268](DETAILED_INVENTORY.md#BIP-0268), [BIP-0269](DETAILED_INVENTORY.md#BIP-0269).
- **Reading ownership:** [R08](batches/R08.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S08/S08-W12**, [WORKS](../01_discovery/S08/WORKS.md) line 43: **Tokenization Is More Than Compression**, Schmidt et al.; [EMNLP 2024](https://aclanthology.org/2024.emnlp-main.40/), pp.678–702. **A**.
  - Original register aliases / era / family / provenance: S08-W12 / S08-N10 / **NEW**
  - Source-scoped evidence/depth: **Tokenization Is More Than Compression**, Schmidt et al.; [EMNLP 2024](https://aclanthology.org/2024.emnlp-main.40/), pp.678–702. **A**. 64 models, 350M–2.4B. Minimum-token segmentation for fixed vocabulary does not imply best downstream quality; pre-tokenization and BPE-initialized vocabulary matter. Exact compute/text-exposure controls need full read.

</details>

<a id="BIW-0132"></a>
## BIW-0132 — Understanding and Mitigating Tokenization Bias in Language Models

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Buu Phan, Marton Havasi, Matthew Muckley and Karen Ullrich, [arXiv:2406.16829v2](https://arxiv.org/pdf/2406.16829v2), 5 July 2024, ICML 2024 Theoretical Foundations of Foundation Models workshop. Alias S08-W14. **Reading: FULL of locked v2**, fresh: §§1–5, Figures 1–3, Appendix A–H (pp. 1–4 and 7–18; references pp. 5–6); relevant BPE Figure 5, §G and algorithm/Figure 3 visually checked in PDF pp. 4, 14–15. `sources/BIW-0132.{pdf,txt}`; some math glyphs in extracted text are corrupted and key portions were cross-checked against original PDF renders. Reading is not a proof audit or code reproduction.

- **[BIP-0274](DETAILED_INVENTORY.md#BIP-0274):** A string-prefix query and the token-prefix obtained by encoding that string are generally different conditional events; for maximum-prefix encoding (MPE), find a stable boundary and exactly sum compatible token prefixes with branch/pass recursion under the stated canonical-support assumptions (§§2–3).
- **Counterexample (§2.2, Figure 1):** alphabet A/B, vocabulary A/B/AA and deterministic longest-prefix encoding: given the *token* A, an ideal model next predicts B with probability 1 because an AA continuation would have merged, whereas a raw text prefix A can continue with A at positive source probability. This mismatch can persist with perfect training because the queried events differ; it does not mean training cannot improve any learned representation or any other tokenization bias. Noncanonical token sequences are “invalid” under that encoder, not invalid Unicode or UTF-8.
- A stable `V*` token is not a substring of any other vocabulary token. Under the paper's MPE assumptions, conditioning on its encoded token prefix equals conditioning on the corresponding character prefix. Divide two probabilities of extensions after the most recent stable boundary (§3.1), assuming nonzero denominator and a suitable initial boundary. MPC (§3.2, Algorithm 1, Appendix E) branches by summing next tokens beginning with the remaining query, and passes by recursively scoring the unique MPE-selected shorter token. Complexity is linear in query length measured in model calls, not constant in vocabulary scans, prompt length, walltime, or KV-memory.
- **[BIP-0275](DETAILED_INVENTORY.md#BIP-0275):** BPE can revise a preceding prefix segmentation (Appendix H cites `hello` vs `hellow`), so greedy MPE recursion cannot simply be transferred. H.1–H.3 instead enumerate valid covering encodings backward, multiply canonical-prefix probability by last-token probability, sum disjoint covers, and obtain conditional ratios. Maximum token length can bound candidate starting positions, but the paper's Algorithm 2 describes iterating over positions and does not establish a constant total runtime. Its algorithm and prose differ on explicitly checking candidate validity: correctness requires applying the described validity condition/zeroing invalid mass.
- **Real neural model caveat (§2, Appendix G):** The ideal induced token process has zero probability on invalid continuations and undefined conditional distributions after invalid prefixes. A softmax model usually assigns positive mass; Appendix G proposes masking these events and renormalizing, with KL/canonical-token likelihood non-worsening under ground-truth-zero assumptions. That is a changed model, not exact marginalization of all noncanonical paths of the original unmodified neural model. The stable-boundary/refactoring claim must not be generalized from the deterministic canonical process to an arbitrary unmasked neural process. No lossless claim for normalization, UNK or undocumented pretokenizers.
- **Carrying card:** [R04/BIW-0132](../03_reading/R04/BIW-0132.md).
- **Canonical problem records:** [BIP-0274](DETAILED_INVENTORY.md#BIP-0274), [BIP-0275](DETAILED_INVENTORY.md#BIP-0275).
- **Units — input / internal / output / supervision (current):** Genericcharacterprefix (toyA/B), MPE/BPEtokens / existingcausaltokenLM / underlying-symbolconditional / unchangednext-tokenLM, mask/renormalizationchangesneuralprocess.

### Current substantive interface, technique, evidence and limits

### Problems and technique

- **[BIP-0274](DETAILED_INVENTORY.md#BIP-0274):** A string-prefix query and the token-prefix obtained by encoding that string are generally different conditional events; for maximum-prefix encoding (MPE), find a stable boundary and exactly sum compatible token prefixes with branch/pass recursion under the stated canonical-support assumptions (§§2–3).
- **Counterexample (§2.2, Figure 1):** alphabet A/B, vocabulary A/B/AA and deterministic longest-prefix encoding: given the *token* A, an ideal model next predicts B with probability 1 because an AA continuation would have merged, whereas a raw text prefix A can continue with A at positive source probability. This mismatch can persist with perfect training because the queried events differ; it does not mean training cannot improve any learned representation or any other tokenization bias. Noncanonical token sequences are “invalid” under that encoder, not invalid Unicode or UTF-8.
- A stable `V*` token is not a substring of any other vocabulary token. Under the paper's MPE assumptions, conditioning on its encoded token prefix equals conditioning on the corresponding character prefix. Divide two probabilities of extensions after the most recent stable boundary (§3.1), assuming nonzero denominator and a suitable initial boundary. MPC (§3.2, Algorithm 1, Appendix E) branches by summing next tokens beginning with the remaining query, and passes by recursively scoring the unique MPE-selected shorter token. Complexity is linear in query length measured in model calls, not constant in vocabulary scans, prompt length, walltime, or KV-memory.
- **[BIP-0275](DETAILED_INVENTORY.md#BIP-0275):** BPE can revise a preceding prefix segmentation (Appendix H cites `hello` vs `hellow`), so greedy MPE recursion cannot simply be transferred. H.1–H.3 instead enumerate valid covering encodings backward, multiply canonical-prefix probability by last-token probability, sum disjoint covers, and obtain conditional ratios. Maximum token length can bound candidate starting positions, but the paper's Algorithm 2 describes iterating over positions and does not establish a constant total runtime. Its algorithm and prose differ on explicitly checking candidate validity: correctness requires applying the described validity condition/zeroing invalid mass.
- **Real neural model caveat (§2, Appendix G):** The ideal induced token process has zero probability on invalid continuations and undefined conditional distributions after invalid prefixes. A softmax model usually assigns positive mass; Appendix G proposes masking these events and renormalizing, with KL/canonical-token likelihood non-worsening under ground-truth-zero assumptions. That is a changed model, not exact marginalization of all noncanonical paths of the original unmodified neural model. The stable-boundary/refactoring claim must not be generalized from the deterministic canonical process to an arbitrary unmasked neural process. No lossless claim for normalization, UNK or undocumented pretokenizers.

### Units, learning and experiments

- Formal alphabet is generic “characters,” not automatically UTF-8 bytes. Input is a surface string encoded as tokens; hidden representation is token-indexed; original training supervision is next canonical token cross entropy; corrected prediction is next underlying alphabet symbol or string-prefix probability. Underlying trained model is causal GPT-2-style Transformer; no fine-tuning, external verifier, multi-byte head, teacher, or added loss in correction. Embedding/output tying, attention-head or layer sharing are not specified. EOS and exact preprocessing beyond the toy alphabet are not fully specified in this version.
- §4/Figure 3: a synthetic third-order A/B Markov source, random transition matrix, six-layer GPT-2, 100 evaluations with varied context lengths per fixed last-three-character state. Corrected MPE estimate tracks source while naive next-token aggregation fails for several states. Appendix H.4/Figure 7 repeats under BPE, with an informative counterexample: the naive baseline happens to be correct at BAA because of the specific merge order. This toy setup is not a real-text performance or runtime benchmark; parameter count, data/training compute, GPU time, memory, and confidence intervals are not reported.
- Prefix probability is a cylinder event including all possible continuations, unlike BIW-0080's completed-document marginal with its own support and EOS ambiguities; BIW-0088 develops a later related cover formulation and downstream FIM/ensemble tests. They are related works, not interchangeable versions. (§1, Appendix A, H.)


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2406.16829v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U generic alphabet characters (toy A/B, not demonstrated Unicode code points) ↔ MPE/BPE tokens → token LM → corrected character conditionals → ordinary next-token training. C correction conditions on raw string prefix instead of a narrower token-prefix event.
- **Learning and causal baseline:** U generic alphabet characters (toy A/B, not demonstrated Unicode code points) ↔ MPE/BPE tokens → token LM → corrected character conditionals → ordinary next-token training. C correction conditions on raw string prefix instead of a narrower token-prefix event.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0274](DETAILED_INVENTORY.md#BIP-0274), [BIP-0275](DETAILED_INVENTORY.md#BIP-0275).
- **Reading ownership:** [R04](batches/R04.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S08/S08-W14**, [WORKS](../01_discovery/S08/WORKS.md) line 45: **Understanding and Mitigating Tokenization Bias in Language Models**, Phan, Havasi, Muckley & Ullrich; [2406.16829v2](https://arxiv.org/abs/2406.16829v2), 2024-07-05; [HTML](https://arxiv.org/html/2406.16829v2). **P**, §§1–2 and opening §3; missing algorithm proofs, full experiments, Appendix G/H. HTML drops first author; Atom restores it.
  - Original register aliases / era / family / provenance: S08-W14 / S08-N12 / **NEW**
  - Source-scoped evidence/depth: **Understanding and Mitigating Tokenization Bias in Language Models**, Phan, Havasi, Muckley & Ullrich; [2406.16829v2](https://arxiv.org/abs/2406.16829v2), 2024-07-05; [HTML](https://arxiv.org/html/2406.16829v2). **P**, §§1–2 and opening §3; missing algorithm proofs, full experiments, Appendix G/H. HTML drops first author; Atom restores it. Markov-chain demonstration; zero-mass/undefined-invalid-encoding assumptions explicit in §3.1 opening. MPE model-run complexity linear in sequence length per abstract; no general production-speed conclusion.

</details>

<a id="BIW-0133"></a>
## BIW-0133 — Causal Estimation of Tokenisation Bias

- **Reading status:** NF — new scoped FULL (R01–R08). Card contents actually read for integration, not a second original-paper full read.
- **Authoritative fixed-source metadata / scope:** **Source.** Pietro Lesci, Clara Meister, Thomas Hofmann, Andreas Vlachos, Tiago Pimentel, ACL 2025, [official PDF](https://aclanthology.org/2025.acl-long.1374.pdf), pp. 28325–28340. Alias S08-W15. **Reading: FULL**, fresh: §§1–8, limitations, Figures 1–5, Appendices A–D, Figures 6–9, pp. 28325–28333 and 28337–28340 (references pp. 28334–28336). Figures 2–9 checked in PDF pp. 28331–28332 and 28339–28340. Local `sources/BIW-0133.{pdf,txt}`. This is reading, not causal identification verification, code execution or reproduction.

- **[BIP-0276](DETAILED_INVENTORY.md#BIP-0276):** Vocabulary choice and word frequency are entangled, so a naive comparison of in/out-of-vocabulary items confounds treatment; the authors use regression discontinuity near a predetermined vocabulary merge-rank cutoff to estimate a *local* effect of membership on average contextual character-span log probability (§§3–4).
- Treatment W=1 iff a subword is included; the outcome averages log probability of its surface span across observed contexts. Potential outcomes refer to models trained with versus without the vocabulary item. Merge index is **discrete**, not a continuous randomized covariate; identification invokes continuity of both potential-outcome conditional expectations, consistency, exogenous cutoff, an adequately specified local fit, and an approximation that rank is sufficiently fine-grained. Appendix C excludes nested subwords to reduce violation of no-interference; this does not independently establish it. Eq. 7 scores canonical token paths under a no-prefix-mismatch assumption; finite model noncanonical mass and tokenizer normalization are not fully audited here.
- The paper specifies a 5k-subword window around the cutoff and uses linear least squares (Appendix C Eq. 30); the exact number on each side, eligible near-cutoff sample sizes, and numerical confidence interval for 2.88 are not reported. Figure 5/Appendix D Fig. 7 uses shaded **standard errors**, unstable below 500 and apparently stabilizing with ≥1k on each side; Figure 9 shows LOESS curves with confidence bands, not a stated numerical 95% CI for the headline estimate. Rank-dependent confounders, overlapping treatments, finite bandwidth and structural model constraints remain concerns even if cutoff was chosen in advance.
- **Units:** Underlying text is a generic alphabet called characters (may denote bytes, code points or graphemes); actual tokenizer uses byte-level pretokenization and byte alphabet (Appendix C), internal input/labels and autoregressive output are subwords, and reported outcome is contextual log-probability of a surface span in nats. The character sequence formalism explicitly includes EOS for completed strings, whereas the empirical outcome concerns span continuations, not an EOS-normalized document score. Causal **treatment** is a statistical intervention on vocabulary membership; it is unrelated to causally masked attention or the different prefix-event mismatch in BIW-0132/0088.
- **AI components:** Llama-2-style autoregressive Transformer trained on next-token prediction, AdamW, learning rate 6e−4, β=(.9,.95), decay .1, warmup/stable/cosine-decay schedule, 2048-token context, batch 128, 50k steps, same seed, checkpoints every 2k (Appendix C). Default 57M is non-embedding parameter count, 6 layers, 24 attention heads, hidden 768. Input/output embeddings are tied for default 57M; a separate 100M FineWeb-Edu comparison explicitly has tied and untied input/output variants. No claim about attention-head sharing, interlayer tying or separately shared multi-byte heads.
- **Carrying card:** [R04/BIW-0133](../03_reading/R04/BIW-0133.md).
- **Canonical problem records:** [BIP-0276](DETAILED_INVENTORY.md#BIP-0276), [BIP-0277](DETAILED_INVENTORY.md#BIP-0277).
- **Units — input / internal / output / supervision (current):** Surface spans/byte-derivedBPEpretokenization / causalsubword LM / contextualspanlogscoreinnats / nexttokenCE plusstatisticalRDvocabulary-membershipeffectestimation, not byteARexperiment.

### Current substantive interface, technique, evidence and limits

### Problem, intervention, technique

- **[BIP-0276](DETAILED_INVENTORY.md#BIP-0276):** Vocabulary choice and word frequency are entangled, so a naive comparison of in/out-of-vocabulary items confounds treatment; the authors use regression discontinuity near a predetermined vocabulary merge-rank cutoff to estimate a *local* effect of membership on average contextual character-span log probability (§§3–4).
- Treatment W=1 iff a subword is included; the outcome averages log probability of its surface span across observed contexts. Potential outcomes refer to models trained with versus without the vocabulary item. Merge index is **discrete**, not a continuous randomized covariate; identification invokes continuity of both potential-outcome conditional expectations, consistency, exogenous cutoff, an adequately specified local fit, and an approximation that rank is sufficiently fine-grained. Appendix C excludes nested subwords to reduce violation of no-interference; this does not independently establish it. Eq. 7 scores canonical token paths under a no-prefix-mismatch assumption; finite model noncanonical mass and tokenizer normalization are not fully audited here.
- The paper specifies a 5k-subword window around the cutoff and uses linear least squares (Appendix C Eq. 30); the exact number on each side, eligible near-cutoff sample sizes, and numerical confidence interval for 2.88 are not reported. Figure 5/Appendix D Fig. 7 uses shaded **standard errors**, unstable below 500 and apparently stabilizing with ≥1k on each side; Figure 9 shows LOESS curves with confidence bands, not a stated numerical 95% CI for the headline estimate. Rank-dependent confounders, overlapping treatments, finite bandwidth and structural model constraints remain concerns even if cutoff was chosen in advance.
- **Units:** Underlying text is a generic alphabet called characters (may denote bytes, code points or graphemes); actual tokenizer uses byte-level pretokenization and byte alphabet (Appendix C), internal input/labels and autoregressive output are subwords, and reported outcome is contextual log-probability of a surface span in nats. The character sequence formalism explicitly includes EOS for completed strings, whereas the empirical outcome concerns span continuations, not an EOS-normalized document score. Causal **treatment** is a statistical intervention on vocabulary membership; it is unrelated to causally masked attention or the different prefix-event mismatch in BIW-0132/0088.
- **AI components:** Llama-2-style autoregressive Transformer trained on next-token prediction, AdamW, learning rate 6e−4, β=(.9,.95), decay .1, warmup/stable/cosine-decay schedule, 2048-token context, batch 128, 50k steps, same seed, checkpoints every 2k (Appendix C). Default 57M is non-embedding parameter count, 6 layers, 24 attention heads, hidden 768. Input/output embeddings are tied for default 57M; a separate 100M FineWeb-Edu comparison explicitly has tied and untied input/output variants. No claim about attention-head sharing, interlayer tying or separately shared multi-byte heads.

### Results, controls and interpretation

- Default 57M BPE, K=32k, MiniPile, 50k steps: Figure 2 estimates +2.88 nats, fitted −7.72 versus −10.60, ≈17.8-fold ratio of exponentiated **mean log scores** near cutoff, not a guaranteed 17× ratio for each item. Median effect 1.52; standard-deviation effect −3.17, interquartile-range −4.42. Local results depend on above assumptions; headline ≈17 is not a universal byte-LM effect (§6).
- Figure 6 visually gives 8k/32k/128k mean effects 1.05/2.88/2.81 nats; Figure 8 gives BPE/BPE2WP/WordPiece 2.88/3.14/2.51. Fig. 4 indicates smaller effects in 340M/850M relative to 57M but not disappearance, with trends across training different from those across tokenizer choices. Figure 4's ties, size and corpus vary together in some curves: do not assert a clean tying-only causal effect from the plot.
- MiniPile is 6 GB, 1M training and 10k validation documents; separate 100M variants train on 20B FineWeb-Edu tokens and evaluate MiniPile. Experiments use an A100 80 GB server; total FLOPs, walltimes and actual eligible observations are unreported. Mostly English and small models. The apparent growing effect during training is not a theorem that more training increases all tokenization biases; perfect distribution matching yields zero effect in Theorem 1, while Theorem 2's approximately uniform initialization produces roughly log vocabulary-size bias (Appendix B).
- **[BIP-0277](DETAILED_INVENTORY.md#BIP-0277):** compare correctly matched interventions, budgets, and local samples; this paper is a counterexample to claims that vocabulary inclusion is always irrelevant, not a direct test of native-byte architecture or a guarantee of benefits from enlarging vocabularies.


<details>
<summary>Original catalog aliases, version sources and discovery depth — historical, not current</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2025.acl-long.1374.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U abstract character strings (paper explicitly allows bytes or graphemes) → BPE/WordPiece LM → tokens mapped to string probabilities → next-token learning. Separate statistical signal: vocabulary inclusion treatment, merge rank running variable, regression-discontinuity estimator. C token-causal models; statistical causal claim local near vocabulary cutoff.
- **Learning and causal baseline:** U abstract character strings (paper explicitly allows bytes or graphemes) → BPE/WordPiece LM → tokens mapped to string probabilities → next-token learning. Separate statistical signal: vocabulary inclusion treatment, merge rank running variable, regression-discontinuity estimator. C token-causal models; statistical causal claim local near vocabulary cutoff.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0276](DETAILED_INVENTORY.md#BIP-0276), [BIP-0277](DETAILED_INVENTORY.md#BIP-0277).
- **Reading ownership:** [R04](batches/R04.md), returned terra FULL; integration completed.

### Source identity, original aliases, versions and actual depth

- **S08/S08-W15**, [WORKS](../01_discovery/S08/WORKS.md) line 46: **Causal Estimation of Tokenisation Bias**, Lesci, Meister, Hofmann, Vlachos & Pimentel; [ACL 2025 PDF](https://aclanthology.org/2025.acl-long.1374.pdf), pp.28325–28340. **P**, §§2–6 and limitations, especially §4.2–4.4/footnote 5; Appendix A/D, all diagnostic graphics not audited.
  - Original register aliases / era / family / provenance: S08-W15 / S08-N13 / **NEW**
  - Source-scoped evidence/depth: **Causal Estimation of Tokenisation Bias**, Lesci, Meister, Hofmann, Vlachos & Pimentel; [ACL 2025 PDF](https://aclanthology.org/2025.acl-long.1374.pdf), pp.28325–28340. **P**, §§2–6 and limitations, especially §4.2–4.4/footnote 5; Appendix A/D, all diagnostic graphics not audited. 57M/340M/850M non-embedding models, default MiniPile 50k steps; 8k/32k/128k vocabularies. Default 57M estimate 2.88 nats (~17×) locally; continuity, bandwidth and functional form conditions essential. This “bias” is **not** Phan's prefix mismatch.

</details>

<a id="BIW-0134"></a>
## BIW-0134 — Tokenization and Representation Biases in Multilingual Models on Dialectal NLP Tasks

- **Reading status:** NF — returned new scoped FULL (R10), actual card read for integration; no fresh original-paper credit to inventory owner.
- **Carrying card:** [R10/BIW-0134](../03_reading/R10/BIW-0134.md).
- **Current units: input / internal / output / supervision:** Model-specificsubwords / fullyfinetunedencoderor4-bitLoRAdecoder / tasklabels/spans / supervisedDI/TC/EQA; TP/IPPearsonassociations,notnativebytecausalintervention.
- **Canonical records:** [BIP-0124](DETAILED_INVENTORY.md#BIP-0124).

### Current card-grounded detail

**Reading status: FULL** for [EMNLP 2025 proceedings PDF](https://aclanthology.org/2025.emnlp-main.1224.pdf), pp. 23992–24010, §§1–8, Tables 1–9 and Appendices A–G, including Figures 1–14. [PDF](../03_reading/R10/sources/BIW-0134.pdf), [text](../03_reading/R10/sources/BIW-0134.txt); [Figure 5/6](../03_reading/R10/sources/BIW-0134-p8.png), [Table 8](../03_reading/R10/sources/BIW-0134-p18.png), [§5.3](../03_reading/R10/sources/BIW-0134-p7.png) visually checked. No tokenizer or model code was run. [BIP-0124](DETAILED_INVENTORY.md#BIP-0124); this fulfills the requested source reading in DISCOVERY_CORRECTIONS T8 without editing shared inventory.

### Problem → solution → research methods

Does a language's token-length disparity relative to English consistently predict performance on dialect tasks? The authors measure **tokenization parity (TP)**, the language/English ratio of tokenizer sequence lengths on parallel content, and **information parity (IP)**, English/language total negative-log-likelihood ratio under a model (§3.1, pp.23994–95); they correlate each with separately adapted task performance rather than presenting a new tokenizer. They use Pearson correlation, parallel FLORES sentences, script/resource groupings, full fine-tuning of BERT encoders, and 4-bit quantized low-rank adaptation (LoRA) for decoder models. These are observed associations across models/languages, not randomized causal tokenization interventions.

### Units, tasks and adaptation budget

Input is model-specific subword units (WordPiece, byte-BPE or SentencePiece depending on model); encoder outputs dialect/topic labels or answer spans, decoder instruction tuning generates labels/spans. TP is relative sequence length for parallel sentences, not a score for the individual byte or an ordinal fairness guarantee. IP compares conditional sequence log-loss under a stated model and reference translation; it is not a measured semantic representation, a byte-normalized probability, or fairness itself. No native byte-step LM is trained.

The tasks are dialect identification (DI), topic classification (TC; 29 languages), and extractive QA (EQA; 24 dialect variants), with training/evaluation sets from multiple sources (§2, Appendix A). TP/IP measured on 54 FLORES language/variety entries; relevant subsets are correlated with task results. mBERT is an encoder baseline, with language-specific encoder DI variants; Phi-3.5-mini and Llama-3.2-3B are the adapted decoder comparators. Language, script, data source, model pretraining, size, task and tuning remain entangled.

Decoder SFT uses 4-bit quantization and LoRA rank 8 or 16, alpha 8, dropout 0.1, batch 1/2/4 with gradient accumulation 8, LR 2e-4 or 5e-5, with Optuna; encoder full fine-tuning uses 3 epochs, AdamW LR 2e-5, batch 8/16, weight decay 0.01 (§4.1). Appendix E reports A100/V100, ~4 hours–1.5 days for decoder experiments vs 1–2 hours for encoders. Number of GPUs, per-task full hyperparameters and pretraining budgets are not fully specified; this is not an equal-compute architecture comparison. The authors say encoders outperform decoders in all tasks, but their own Table 7 reports Korean EQA F1 0.10/0.092 for mBERT vs 0.482/0.500 Phi; such general language should be understood at reported aggregate level, not every cell.

### Actual task-dependent correlations and scope

Appendix F Table 8 p.24009, visually checked; Figure 5 rounds the same overall values:

| Task | Model | Pearson r(TP, task score) | Pearson r(IP, task score) |
|---|---|---:|---:|
| DI | Phi-3.5 | +0.638 | −0.413 |
| DI | Llama-3.2 | −0.380 | +0.268 |
| DI | mBERT | +0.4836 | not reported |
| TC | Phi-3.5 | −0.683 | +0.812 |
| TC | Llama-3.2 | −0.716 | +0.687 |
| TC | mBERT | −0.605 | not reported |
| EQA | Phi-3.5 | −0.834 | +0.618 |
| EQA | Llama-3.2 | −0.528 | +0.097 |
| EQA | mBERT | −0.938 | not reported |

Overall DI reverses the TP sign relative to TC/EQA for Phi and mBERT; Llama DI retains the expected negative sign. IP changes sign for Phi DI vs TC/EQA. The named table coefficients remain unchanged. R2 withdraws the earlier definite TP prose-conflict assertion: §5.2 first gives negative Llama TP, while a later positive sentence may refer to Llama IP (+0.268). Attribute each sign to TP or IP; an unambiguous TP contradiction is not established. The explanation that finer fragments help surface dialect discrimination is a hypothesis. It is not proof that fragmentation causes improved fairness.

Table 8's per-group Phi TC correlations vary from +0.873 (Latin-high) to −0.785 (Latin-low); Phi non-Latin-high IP is −0.862 whereas overall IP is +0.812. These group values are descriptive and should not be substituted for overall numbers. Per-correlation sample sizes and significance/uncertainty are not reported in Table 8; available task/language counts do not establish the effective paired n in each cell. No p-values are inferred.

### Glyph example and coverage correction

§5.3/Figure 6 presents Llama-3.2 displayed fragments for Arabic and an example Devanagari character र with UTF-8 bytes `E0 A4 B0` shown as Latin-looking `à¤°` (§5.3, pp.23998–99). The authors themselves say byte sequences **may be reassembled** as proper Unicode on decoding. Displayed byte-mapped glyphs alone are not evidence that actual text was corrupted, lost, or irreversibly decoded; not all byte-level vocabularies use literal Latin-1 as their actual internal encoding. The exact tokenizer artifact, its byte-to-symbol mapping, per-token round trip and output error rates were not verified. The observation of fragmentation and the speculation about downstream harm must remain separate.

Appendix G's “missing characters” count means **characters absent as standalone vocabulary entries**, not unrepresentable Unicode characters, and is not by itself proof of loss; byte fallbacks and multi-character tokens matter. Appendix G explicitly notes a language-specific model can perform well despite missing standalone entries. Distinguish this paper from TokSuite's independent text-budget and Figure 6 metric issues; they are not one joint experiment.

### BIP implication

BIP-0124 is supported at full-paper scope with task-dependent signs and adaptation differences. Report fragmentation, probability parity, task correctness and resource budgets as separate axes; do not turn parity into capability or infer fairness, causal mechanisms or irreversibility from printed glyphs. No unreported runtime/correlation uncertainty warrants another full read.

**Final R2 / claim-rules adoption** ([CLAIM_RULES](../05_review/CLAIM_RULES.md); [FULL_READING_AUDIT_R2](../05_review/FULL_READING_AUDIT_R2.md)): Current R2 adoption — dialect TP and IP must be named separately. Appendix F Table 8 gives DI TP correlations +0.638 (Phi), +0.4836 (mBERT), −0.380 (Llama), and DI IP −0.413 (Phi), +0.268 (Llama). Section5.2 explicitly describes Llama TP as negative; the later positive sentence follows IP discussion and may refer to IP. The earlier definite “TP prose contradicts the table” assertion is withdrawn, not a confirmed source conflict. Coefficients and task-dependent associations are unchanged. Effective paired n/significance are not reported in Table8; no causal fairness or Unicode-corruption conclusion follows. Decoder4-bitLoRA and encoderfulltuning are different budgets. T8 whole-source reading is complete; runtime/tokenizer artifacts remain unverified.

<details>
<summary>Prior catalog provenance and source aliases — historical depth, superseded by current receipt</summary>

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2025.emnlp-main.1224.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** Model-specific subwords / encoder or decoder representations / dialect or topic labels, QA spans / downstream labels; quantized LoRA for decoders versus full encoder tuning.
- **Learning and causal baseline:** Encoder and decoder task permissions differ; tokenizer parity associations do not isolate pretraining/capacity or imply a causal tokenizer effect.
- **Historical discovery reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0124](DETAILED_INVENTORY.md#BIP-0124).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S08/S08-W16**, [WORKS](../01_discovery/S08/WORKS.md) line 47: **Tokenization and Representation Biases in Multilingual Models on Dialectal NLP Tasks**, Kanjirangat et al.; [EMNLP 2025 abstract](https://aclanthology.org/2025.emnlp-main.1224/), [PDF](https://aclanthology.org/2025.emnlp-main.1224.pdf). **P**, PDF title/authors, §§3–5.2 and limitations selected; numerical tables/appendices not audited. Authors Vani Kanjirangat, Tanja Samardžić, Ljiljana Dolamic, Fabio Rinaldi. Decoder fine-tuning uses quantized LoRA, encoder full fine-tuning; unequal adaptation permissions/budgets. Dialect identification shows the opposite parity correlation from the simplistic fewer-fragments-is-better claim. §5.3's visible Latin-like token glyphs must not be mistaken for proof that byte-BPE irreversibly corrupts Unicode.
  - Original register aliases / era / family / provenance: S08-W16 / S08-N14 / **NEW**
  - Source-scoped evidence/depth: **Tokenization and Representation Biases in Multilingual Models on Dialectal NLP Tasks**, Kanjirangat et al.; [EMNLP 2025 abstract](https://aclanthology.org/2025.emnlp-main.1224/), [PDF](https://aclanthology.org/2025.emnlp-main.1224.pdf). **P**, PDF title/authors, §§3–5.2 and limitations selected; numerical tables/appendices not audited. Authors Vani Kanjirangat, Tanja Samardžić, Ljiljana Dolamic, Fabio Rinaldi. Decoder fine-tuning uses quantized LoRA, encoder full fine-tuning; unequal adaptation permissions/budgets. Dialect identification shows the opposite parity correlation from the simplistic fewer-fragments-is-better claim. §5.3's visible Latin-like token glyphs must not be mistaken for proof that byte-BPE irreversibly corrupts Unicode. Latin/non-Latin and high/low-resource comparisons; token-length parity and information parity predict different task families. Correlation does not isolate tokenizer from data/model capacity.


**Current targeted correction (not FULL):** Dialect formal EMNLP2025 §4.1/5.2, PDF4/6 printed23995/23997: decoder4-bit quantized LoRA versus encoder full fine-tuning. Tokenization parity is positively associated with dialect identification for mBERT and Phi3.5; Llama3.2 shows the expected negative sign but performs worse. Phi3.5 information parity also reverses expected direction. Pearson associations, not randomized tokenizer effects; Table8 was read in R10; current TP/IP coefficients and R2 referent clarification supersede this earlier pending-depth note. R060 TokSuite budget component is merged elsewhere; this is a distinct work/problem, not a joint study. Visible byte-BPE glyphs alone do not prove irreversible Unicode corruption.


</details>

<a id="BIW-0135"></a>
## BIW-0135 — BPE-Dropout: Simple and Effective Subword Regularization

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://aclanthology.org/2020.acl-main.170.pdf. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U stochastically segmented BPE subwords → translation states → subwords → parallel translation loss. Explicit technique: drop merges during training; standard BPE at test. C complete source / target autoregression.
- **Learning and causal baseline:** U stochastically segmented BPE subwords → translation states → subwords → parallel translation loss. Explicit technique: drop merges during training; standard BPE at test. C complete source / target autoregression.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0271](DETAILED_INVENTORY.md#BIP-0271).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S08/S08-W17**, [WORKS](../01_discovery/S08/WORKS.md) line 48: **BPE-Dropout: Simple and Effective Subword Regularization**, Provilkov, Emelianenko & Voita; [ACL 2020 formal abstract](https://aclanthology.org/2020.acl-main.170/), [PDF](https://aclanthology.org/2020.acl-main.170.pdf). **A**.
  - Original register aliases / era / family / provenance: S08-W17 / S08-N15 / **NEW**
  - Source-scoped evidence/depth: **BPE-Dropout: Simple and Effective Subword Regularization**, Provilkov, Emelianenko & Voita; [ACL 2020 formal abstract](https://aclanthology.org/2020.acl-main.170/), [PDF](https://aclanthology.org/2020.acl-main.170.pdf). **A**. Abstract up to +2.3 BLEU over BPE and +0.9 over previous subword regularization. Robustness can improve without abandoning a fixed vocabulary; actual cost and dataset tables missing.

<a id="BIW-0136"></a>
## BIW-0136 — Deduplicating Training Data Makes Language Models Better

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2107.06499v2. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U original text for dedup, model tokenizer unknown here → LM states → LM tokens → ordinary LM objective after data cleaning. Dedup algorithms' exact names not inferred from abstract. C LM direction not established from this source alone.
- **Learning and causal baseline:** U original text for dedup, model tokenizer unknown here → LM states → LM tokens → ordinary LM objective after data cleaning. Dedup algorithms' exact names not inferred from abstract. C LM direction not established from this source alone.
- **Reading status:** A — abstract/metadata, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0279](DETAILED_INVENTORY.md#BIP-0279).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S08/S08-W19**, [WORKS](../01_discovery/S08/WORKS.md) line 50: **Deduplicating Training Data Makes Language Models Better**, Lee et al.; [2107.06499v2](https://arxiv.org/abs/2107.06499v2), 2022-03-24 / ACL 2022 association not independently checked. **A**.
  - Original register aliases / era / family / provenance: S08-W19 / S08-N17 / **NEW**
  - Source-scoped evidence/depth: **Deduplicating Training Data Makes Language Models Better**, Lee et al.; [2107.06499v2](https://arxiv.org/abs/2107.06499v2), 2022-03-24 / ACL 2022 association not independently checked. **A**. Abstract: near duplicates, >4% validation overlap in standard datasets, less memorized output and fewer steps at equal/better accuracy. General methodology evidence, not a byte-vs-subword comparison; exact corpus/control budgets need full read.

<a id="BIW-0137"></a>
## BIW-0137 — Long Range Arena: A Benchmark for Efficient Transformers

- **Entity / provenance:** paper; new relative to inspected old catalog + recovery (not a claim of global scholarly novelty). No old global W ID; local aliases below.
- **Full-source target / version:** https://arxiv.org/pdf/2011.04006v1. Version scope and formal/preprint differences are recorded below.
- **Units: input / internal / output / supervision:** U text byte/character setup as named (precise text encoder mapping unverified), ListOps symbols, grayscale pixel intensities → encoder sequences → class labels → supervised CE. C explicitly encoder-only tasks permitted, **not autoregressive LM**.
- **Learning and causal baseline:** U text byte/character setup as named (precise text encoder mapping unverified), ListOps symbols, grayscale pixel intensities → encoder sequences → class labels → supervised CE. C explicitly encoder-only tasks permitted, **not autoregressive LM**.
- **Reading status:** P — selected primary/recovery passages, not FULL. No old scoped FULL card is registered for this entity; a primary-source partial visit or an official introduction is not FULL.
- **Canonical problems:** [BIP-0280](DETAILED_INVENTORY.md#BIP-0280), [BIP-0281](DETAILED_INVENTORY.md#BIP-0281).
- **Reading ownership:** reference only / reserve, see READING_QUEUE.

### Source identity, original aliases, versions and actual depth

- **S08/S08-W20**, [WORKS](../01_discovery/S08/WORKS.md) line 51: **Long Range Arena: A Benchmark for Efficient Transformers**, Tay et al.; [2011.04006v1 HTML](https://arxiv.org/html/2011.04006v1), 2020-11-08 / ICLR 2021 association not rechecked. **P**, §§2.1–2.3,3.2–3.5 and A.1.2–A.2.1; full result-table cells not read.
  - Original register aliases / era / family / provenance: S08-W20 / S08-N18 / **NEW**
  - Source-scoped evidence/depth: **Long Range Arena: A Benchmark for Efficient Transformers**, Tay et al.; [2011.04006v1 HTML](https://arxiv.org/html/2011.04006v1), 2020-11-08 / ICLR 2021 association not rechecked. **P**, §§2.1–2.3,3.2–3.5 and A.1.2–A.2.1; full result-table cells not read. IMDb up to 4k, AAN 4k/document, pixel Path-X 16k; no pretraining by design. Quality/speed/memory tradeoffs on 4×4 TPUv3; pixel classification or LRA average does not establish byte-language generation.

<a id="BIW-0138"></a>
## BIW-0138 — Adaptive Computation Time for Recurrent Neural Networks

- **Identity / era / kind:** arXiv:1603.08983v6; Alex Graves; 2017; academic paper. New dedicated entity after exact source/title search of prior137byte-survey catalog found no match. Old-corpus alias W0248 is preserved: the prior broader catalog registered ACT at abstract level, so this is corpus reuse with a new scoped FULL, not fresh discovery.
- **Stable source alias:** `FAD-ACT` → `BIW-0138`; [arxiv_1603.08983v6.md](../03_reading/FIELD_ADDENDUM/arxiv_1603.08983v6.md). Revisions keep thissameBIW.
- **Fixed public source:** https://arxiv.org/pdf/1603.08983v6
- **Reading status:** NF — new scoped FULL; actual card read for integration, not neworiginalpapercredit toinventoryowner.
- **Four units:** Wikipedia task: raw Unicode/XML bytes / repeated recurrent hidden transitions within each byte / 256-class next-byte softmax / next-byte CE plus ponder penalty. Other synthetic tasks have separate units.
- **Actual techniques and roles:** Within-byte LSTM transitions, sigmoid cumulative halting and weighted state/output aggregation; task loss plus transition-count/remainder penalty, not sequence shortening.
- **Canonical granular findings:** [BIP-0287](DETAILED_INVENTORY.md#BIP-0287), [BIP-0288](DETAILED_INVENTORY.md#BIP-0288), [BIP-0289](DETAILED_INVENTORY.md#BIP-0289).

### Actual card source scope, evidence and limits

**Reading status: FULL**, source-text reading for the requested text-interface contribution, not code or experiment reproduction. Alex Graves, 2017, [versioned HTML](https://arxiv.org/html/1603.08983v6), [versioned PDF](https://arxiv.org/pdf/1603.08983v6). Read §§1–4, all four synthetic task descriptions and relevant figures/captions, Wikipedia §3.5 and Figures 21–24; no appendix in this version. The HTML rendering of the Wikipedia error chart was visually inspected; numerical curve coordinates were not digitized. The source card originally used only its arXiv identity; the central BIW/source-alias mapping above is now authoritative.

### Problem, intervention, and roles

A conventional recurrent network must choose an a priori fixed amount of transformation at each input position, even when predictive utility of computation differs across inputs. **ACT allocates a learned number of repeated recurrent transitions at each position**, without reducing the number of input positions (§§1–2). A recurrent state transition and output projection are reused at all internal steps; an input flag marks the first internal step of a new external position. A sigmoid halting unit supplies nonnegative weights until their cumulative sum reaches `1−ε`; the final weight is the remaining mass. State and output passed onward are weighted mean-field sums of intermediate states and outputs (Eqs. 3–9). The mean-field combination is an author modeling assumption, not a proof that interpolated hidden states preserve their semantics.

**AI techniques and exact roles:** LSTM provides recurrent state; a learned sigmoid determines within-input computational depth; the weighted state/output mixture makes the step choices trainable without sampled policy-gradient noise. The task cross-entropy plus `τ Σ_t (N(t)+R(t))` penalizes ponder cost (Eqs. 10–12); `M` is a hard maximum, and ε=0.01. The number of steps changes discontinuously: §2.2 explicitly holds `N(t)` constant for differentiation and ignores the discontinuities. Thus “deterministic and differentiable” in the abstract must not be read as a globally smooth or exact derivative of the halting rule. Ponder is a proxy for transition count, not measured energy or wall time.

### Interface and causal contract

In §3.5 the raw Unicode Wikipedia text, including XML markup, is presented **one byte per input time step**, with **the next byte as target** and a 256-class softmax. Internal units are repeated hidden-state transitions at that byte; there is no merged token or patch. Conditioning uses input and recurrent state available at that position, and the weighted state propagates to the next; no future source text is introduced by the described forward recurrence. 500 consecutive training bytes are sampled and state reset at each sequence start. Text generation termination, incomplete Unicode scalar handling, and a production streaming interface are **unreported**. No external segmentation teacher is described for this experiment. The paper calls the task character prediction even though it explicitly specifies bytes; its bit-per-character label here must retain that qualification.

### Evidence, comparisons and costs

- **Wikipedia (§3.5; Figures 21–24):** one 1,500-cell LSTM layer versus the same basic recurrent setup without ACT; output 256. ACT and non-ACT have fairly similar errors, and ACT's average ponder is much lower than on synthetic problems. The author describes some data-efficiency indications, not a decisive language-model gain. **All reported errors are training-set errors**, not held-out quality. Figure 21 visually shows overlapping ranges around roughly 1.5–1.6 bits per named character, not a matched-serving frontier; do not manufacture exact values from the chart. Figure 23 describes more ponder at spaces and punctuation; Figure 24 contrasts XML transitions and unpredictable ID numbers against entropy/loss. These are selected qualitative traces, not validated segmentation boundaries or a causal proof of useful computation.
- **Synthetic controls (§§3.1–3.4):** parity without ACT is near 40% error versus below 5% for suitable penalties; logic approximately 0.2 sequence error without ACT and near zero for τ≤0.01. Addition is solved by ACT across the tested grid. Sorting falls from around 12% to 6% at the best penalty but takes approximately **9×** the baseline computations; its long-sequence error still rises. These are different synthetic tasks, not language results.
- **Training (§3):** Adam at 10⁻⁴, asynchronous Hogwild with 16 threads, 20 initializations per time penalty, 10K iterations for the Wikipedia task; each iteration is a single-thread update so total updates are approximately 16× iteration count. Penalty grid selection cost is material, and the paper says language runs took many days. Precise hardware, per-model wall-clock, total FLOPs and cached/batched serving speed are **unreported**. `M=100` except where noted; it is a safety limit rather than the observed average.

### BIP implications and limits

Related, not identical, questions are [BIP-0054](DETAILED_INVENTORY.md#BIP-0054), [BIP-0157](DETAILED_INVENTORY.md#BIP-0157), and [BIP-0162](DETAILED_INVENTORY.md#BIP-0162): ACT's own qualitative effort-versus-entropy distinction predates those work-specific boundary mechanisms. Do not merge them: repeated work per byte is not learned segmentation, a utility label, or an intervention demonstrating a better boundary. Report held-out performance, realized transition distribution, batching overhead and normalized cost before claiming useful adaptive byte compute. Runtime behavior and exact model artifacts were not inspected; this does not change the paper-reading status.


- **Original W:** `W0248`; [broader old catalog](../../flued_multigranularity_survey_20261108/02_catalog/CATALOG.md), ACT row, abstract only before this new FULL.

<a id="BIW-0139"></a>
## BIW-0139 — Reformer: The Efficient Transformer

- **Identity / era / kind:** arXiv:2001.04451v2; Kitaev, Kaiser, Levskaya; 2020; academic paper. New dedicated entity after exact source/title search of prior137byte-survey catalog found no match. No broader old-catalog W alias found in the targeted identity search.
- **Stable source alias:** `FAD-REFORMER` → `BIW-0139`; [arxiv_2001.04451v2.md](../03_reading/FIELD_ADDENDUM/arxiv_2001.04451v2.md). Revisions keep thissameBIW.
- **Fixed public source:** https://arxiv.org/pdf/2001.04451v2
- **Reading status:** NF — new scoped FULL; actual card read for integration, not neworiginalpapercredit toinventoryowner.
- **Four units:** enwik8-64K byte-text benchmark / all 65,536 fine-resolution positions / next benchmark unit / causal LM objective; exact enwik8 vocabulary serialization/size unreported in read source. Translation/image/copy tasks are separate.
- **Actual techniques and roles:** LSH approximate attention, shared Q/K map, reversible paired residual activation reconstruction, and position-wise FFN execution chunking; no learned byte boundaries.
- **Canonical granular findings:** [BIP-0290](DETAILED_INVENTORY.md#BIP-0290), [BIP-0291](DETAILED_INVENTORY.md#BIP-0291), [BIP-0292](DETAILED_INVENTORY.md#BIP-0292).

### Actual card source scope, evidence and limits

**Reading status: FULL**, version-locked source text and relevant appendix, not implementation or experimental reproduction. Nikita Kitaev, Łukasz Kaiser and Anselm Levskaya, 2020; [versioned HTML](https://arxiv.org/html/2001.04451v2), [versioned PDF](https://arxiv.org/pdf/2001.04451v2). Read §§1–6, Tables 1–4, Figures 1–5 and Appendix A, including experimental text and figure captions; Figures 3 and 5 were additionally inspected visually. Figure curves were not digitized and HTML text rendering of some complexity formulas is imperfect; complexity is attributed to the stated method rather than inferred from malformed table extraction. The source card used its arXiv identity; the central BIW mapping above now identifies this entity.

### Problem, solution, and AI technique roles

**Problem:** byte-length inputs make dense attention expensive, while storing deep-stack activations and wide feed-forward intermediates separately stresses training memory. A shorter sequence is one option, but it is not the only one.

**Solution:** retain every sequence position and combine three independent resource interventions (§§1–3):

1. **Locality-sensitive hashing (LSH) attention** uses random angular projections to bucket similar query/key vectors, sorts by hash and original position, and restricts attention to sorted chunks including a previous chunk. Multiple independently hashed rounds improve recall at added cost. This is an approximate attention connectivity scheme, not learned byte boundaries or a guarantee of finding all exact nearest neighbors. The abstract reports `O(L log L)` rather than dense quadratic attention; actual cost depends on hash rounds, bucket/chunk choices and implementation.
2. **Reversible residual blocks** preserve two state streams: `y1=x1+F(x2)`, `y2=x2+G(y1)`; reconstruct `x2=y2−G(y1)` and `x1=y1−F(x2)` in the backward pass. Here F is attention, G feed-forward. This trades recomputation for reduced depth-dependent *training activation* storage; it does not eliminate parameters, input activations, optimizer state or inference KV state, and the component functions need not themselves be invertible.
3. **Position-wise feed-forward chunking** computes the same independent-position operation in smaller sequential pieces to lower peak intermediates. It is an execution partition, not a semantic chunk model or fewer text positions. §3 additionally proposes loss chunking for large vocabularies and parameter swapping, which are distinct mechanisms, not byte-likelihood gains by themselves.

The model uses a **shared query/key projection**, with normalized keys, to make a position hash consistently against itself (§2). This is projection sharing, not embedding/output tying or a tied inverse. Appendix A handles multiple hash rounds using normalization and a duplicate-count correction. In a decoder the mask is computed from original position indices after sorting; self-attention to the same position is suppressed except where there is no other valid key. This paper-level specification is not a test of incremental cache behavior.

### Units, causal contract, and comparisons

Enwik8-64K is a byte-text language benchmark: the paper calls the 65,536-long examples “tokens,” but the benchmark axis is byte-level text, not BPE chunks or learned patches. The internal representation remains one position per input unit; causal language modeling predicts the next unit and masks future source indices (§2). The synthetic copy task uses symbol classes, not evidence of raw-byte language understanding; imagenet64 is an image task; WMT14 English–German tests an encoder–decoder with distinct input/output language tokens and is not a raw-byte experiment. The exact enwik8 vocabulary encoding, end-of-sequence conventions, partially filled prompt state, and deployed prefix-caching behavior are **not specified by the sections used**; do not assert a 256-way output based solely on the dataset name. No byte tokenization teacher is described.

### Results, controls, and budget boundaries

- **Copy (Table 2, §2.1):** examples `0 w 0 w` with |w|=511; next-symbol loss/accuracy scores only the second, predictable half. A one-layer model trained with full attention scores 100% with full attention but 94.8%, 92.5%, 76.9%, 52.5% with 8, 4, 2, 1 test hashes. An LSH-4-trained model obtains 99.9% at 4 test hashes and 100% at 8. Extra hashes affect cost; these results concern synthetic copy, not byte generation.
- **Ablations (§5, Figure 3):** 3-layer full versus shared-QK or reversible comparisons use equal parameter counts for reversibility; curves on enwik8 and imagenet64 are similar in the displayed runs. This supports these configurations, not numerical equality in all settings. Main experiments report model width 1024, FFN width 4096, eight heads, total batch eight, Adafactor, training on eight GPUs or TPU v3 cores. The source says full-attention baselines use a memory-efficient implementation that recomputes attention (§2), so the baseline is not necessarily a naive materialized attention matrix.
- **Hash rounds and length (§5, Figures 4–5):** quality approaches full attention with more hashes in the reported image ablation; attention evaluation time versus sequence length is plotted with total token count held fixed. Figure 5 right is **synthetic attention evaluation**, not end-to-end autoregressive serving. Its LSH curves vary with hashes and are not a universal constant latency guarantee.
- **Large models (§5):** up to 20-layer Reformers fit and train, while the authors could not train equally large full Transformer baselines because of speed/memory. A 12-layer enwik8 model at 20K steps and dropout 0.1 reports 1.19 bits/dim; a longer tuned run reports 1.05 test bits/dim. These are not matched-quality/full-attention cost wins. Full training compute, total tuning, modern batched decoding and latency to complete a UTF-8 character are **unreported**.
- **Different output task (§5, Table 4):** reversible translation base at 100K steps has BLEU 27.6 (sacreBLEU uncased 27.4/cased 26.9); longer no-weight-sharing base reaches 28.0. The authors do not use LSH on these short sentence examples. Translation embedding/output sharing choices are separate from QK sharing; neither establishes byte input-output weight tying.

### BIP implications and limits

[BIP-0236](DETAILED_INVENTORY.md#BIP-0236) concerns quadratic attention on byte-length context; [BIP-0237](DETAILED_INVENTORY.md#BIP-0237) concerns practical execution. Reformer adds a related but distinct hash-based, full-position mechanism and reversible/FFN activation-memory controls; its paper is not a replacement for the R09 Sparse Transformer source. The meaningful comparison must separate source bytes, positions, quality, attention approximation, training memory/recomputation and generation-time cache/latency. Paper architecture is not a runtime-alias or leak-free implementation certificate. Code was not run; missing artifact verification is not a paper-reading gap.


<a id="BIW-0140"></a>
## BIW-0140 — Deep contextualized word representations (ELMo)

- **Identity / era / kind:** arXiv:1802.05365v2; Peters et al.; 2018; academic paper. New dedicated entity after exact source/title search of prior137byte-survey catalog found no match. No broader old-catalog W alias found in the targeted identity search.
- **Stable source alias:** `FAD-ELMO` → `BIW-0140`; [arxiv_1802.05365v2.md](../03_reading/FIELD_ADDENDUM/arxiv_1802.05365v2.md). Revisions keep thissameBIW.
- **Fixed public source:** https://arxiv.org/pdf/1802.05365v2
- **Reading status:** P — intentional narrow primary extraction; actual card read for integration, not neworiginalpapercredit toinventoryowner.
- **Four units:** Characters inside externally delimited words (exact byte serialization unexamined) / word-time forward/backward LSTMs / next/preceding word softmax or task heads / bidirectional word-LM pretraining and supervised task loss.
- **Actual techniques and roles:** Character-CNN/highway word composition, contextual biLM, frozen-task integration with learned layer softmax mixture and scale; directional representation/softmax sharing, separate directional LSTMs.
- **Canonical granular findings:** [BIP-0293](DETAILED_INVENTORY.md#BIP-0293), [BIP-0294](DETAILED_INVENTORY.md#BIP-0294).

### Actual card source scope, evidence and limits

**Reading status: PARTIAL — designated narrow primary extraction.** Matthew E. Peters et al., 2018, [versioned HTML](https://arxiv.org/html/1802.05365v2), [versioned PDF](https://arxiv.org/pdf/1802.05365v2). Read §§1–3.4 and Table 1. Sections 4–6 and the supplement were not fully audited, so no full-paper credit is claimed. The source card used the stable arXiv identifier; the central BIW/source-alias mapping above has now been assigned.

### Problem, solution, techniques

A static word vector cannot reflect a word's changing context or expose different levels of linguistic information. A character-CNN/highway network constructs a context-independent representation of each **word position**; a two-layer bidirectional language model (biLM) contextualizes it; the downstream model learns a softmax-weighted mixture of layer states and a scaling coefficient γ (§§3.1–3.4). The CNN composes word-internal character n-grams; highway layers gate the composition; separately parameterized forward and backward LSTMs model context; layer mixing selects task-useful representations. Pretrained biLM weights are frozen during supervised task training, after any optional domain-specific LM fine-tuning; the task head and layer weights are learned. This is an author-used transfer method, not byte-stream generation.

### Units, supervision, and sharing

Input composition uses characters **within words**, internal recurrent positions are words, and LM training predicts the next or preceding **word/token** in the respective direction via a softmax (§3.1). The exact character serialization or whether the actual implementation uses UTF-8 bytes is **not established by these paper passages**; do not classify ELMo as a raw-byte LM. Each directional LM is causal in its own direction, but their concatenated representation for downstream tasks uses both past and future full-sentence context, so it is not a prefix-only generator. EOS and streaming/partial-prompt contracts were not examined.

The forward and backward LMs share **their token-representation parameters with each other**, and share **their softmax parameters with each other**, while keeping the directional LSTMs separate (§3.1). This does **not** assert input-representation-to-softmax matrix tying. The character encoder uses 2048 convolutional filters, two highway layers and a 512-dimensional projection; the LM has two 4096-unit LSTM layers with 512 projections and a residual connection (§3.4).

### Evidence and bounded implications

The paper reports ten epochs on the 1B Word Benchmark; average forward/backward perplexity 39.7 versus the larger forward CNN-BIG-LSTM's 30.0 (§3.4). The architectures and directionality differ; this is not a controlled byte result. For the named supervised SQuAD baseline, Table 1 reports F1 81.1 without ELMo versus 85.8 with it, with task training and pretrained model resource costs; this check does not audit benchmark protocol or other numerical claims. Exact pretraining FLOPs, teacher-free-deployment implications, and runtime cost were **not examined**, not asserted absent.

Related parent question: [BIP-0005](DETAILED_INVENTORY.md#BIP-0005), the distinction between input coverage and prediction-target vocabulary. ELMo is a **character-input/word-output historical antecedent** and adds contextual layer mixture plus directional sharing; it does not solve or experimentally test that CANINE-specific pretraining question. It cannot establish open byte-output support, byte causality, or a byte-quality frontier.


<a id="BIW-0141"></a>
## BIW-0141 — Language Models are Unsupervised Multitask Learners (GPT-2 report)

- **Identity / era / kind:** Official OpenAI 2019 technical report; mutable unpinned public PDF; official research report. New dedicated entity after exact source/title search of prior137byte-survey catalog found no match. No broader old-catalog W alias found in the targeted identity search.
- **Stable source alias:** `FAD-GPT2` → `BIW-0141`; [gpt2_official_report_2019.md](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md). Revisions keep thissameBIW.
- **Fixed public source:** https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf
- **Reading status:** P — intentional narrow primary extraction; actual card read for integration, not neworiginalpapercredit toinventoryowner.
- **Four units:** UTF-8 byte base alphabet before BPE / merged byte-BPE model positions / merged vocabulary symbols (50,257) / causal next-piece prediction; context1,024 model tokens, not1,024 bytes.
- **Actual techniques and roles:** Frequency-derived byte-pair merges with category-boundary constraints and space exception; causal Transformer on merged symbols, not a raw256-way byte output.
- **Canonical granular findings:** [BIP-0295](DETAILED_INVENTORY.md#BIP-0295), [BIP-0296](DETAILED_INVENTORY.md#BIP-0296).

### Actual card source scope, evidence and limits

**Reading status: PARTIAL — designated narrow primary extraction.** Alec Radford et al., [official OpenAI report PDF](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf), p. 4 §§2.2–2.3 and adjacent §3.1, visually read in the browser. The official URL is the stable source identifier; this PDF is not revision-pinned. The rest of the report, performance tables and appendix were not fully audited. The receipt originally assigned no BIW; the stable central mapping is now stated above.

### Problem, proposed solution, and method roles

A fixed Unicode code-point alphabet can be large or exclude symbols, whereas the authors report a preliminary WebText quality gap for their standard raw-byte LMs relative to word-level systems. Their compromise is **byte-based byte-pair encoding (byte BPE)**: begin with 256 possible byte symbols, learn frequent adjacent merges, and operate the language model on the resulting vocabulary of merged pieces (§2.2). Greedy frequency-based BPE is the learned compression/vocabulary-construction method; the Transformer is the causal next-piece predictor (§2.3). The report says unrestricted merges waste vocabulary on word-plus-punctuation variants such as `dog.` and `dog!`, so it prevents merges across character categories with an exception for spaces. These constraints are part of the reported preprocessing contract, not properties of all byte-BPE schemes.

### Units and causal contract

The representation starts from UTF-8 bytes, but the actual **input and model positions are merged byte-BPE symbols**, and the next prediction is a vocabulary symbol, not one of 256 raw bytes. The adjacent model section specifies a **50,257-entry vocabulary** and context of **1,024 model tokens**, not 1,024 bytes. Learned merges and category pre-tokenization must be distinguished from UTF-8 coverage. The report's string-probability claim describes its own evaluation; probability of a selected canonical tokenization path, unmarked string marginal and byte-prefix event are different estimands, not automatically equal. Actual prefix stability of the complete-string tokenizer and EOS/partial-byte-output handling are **not established by this narrow check**. No separate byte entropy teacher is stated in §2.2.

### Evidence and scope

Section 2.2 says the authors observed standard byte-LM underperformance on WebText in preliminary attempts, but gives no fully specified matched-compute comparison there: this is a reported observation, **not a quantified general frontier**. Section 2.3 reports 1,024 model-token context and Table 2 gives model sizes; neither is a measured byte-normalized training or serving budget. Benchmark results elsewhere, tokenizer training cost, exact byte exposure, and real-time throughput are **not examined** here, rather than declared unreported in the full report.

### BIP implications

This is a primary historical anchor for byte-complete **subword** modeling, distinct from both code-point BPE and raw-byte next-step modeling. It is related to [BIP-0005](DETAILED_INVENTORY.md#BIP-0005)'s broader input-versus-supervision distinction, not the same CANINE mechanism. The byte alphabet supplies coverage but does not make output units bytes or prove equality between string and prefix probabilities. Pair with the established prefix-probability work [BIW-0088](WORK_CATALOG.md#BIW-0088) rather than deriving those later results from this report.


## Non-equivalences and excluded leads

- CharacterBERT (BIW-0066; word-local UTF-8 CNN, closed word MLM) is not CharBERT (BIW-0067; parallel character/subword channels).
- Finding Function in Form (BIW-0056, 1508.02096v2) is not Character-based NMT (BIW-0120, 1511.04586v1). The latter’s staged mimicry/IBM4 supervision is not transferred to the former.
- Patching Leaks (BIW-0074, 2205.14086v1) and Subword-Delimited Downsampling (BIW-0075, formal EMNLP2022 / 2212.01304v1) are distinct papers, not earlier/later versions of one effect.
- Prefix-event correction (BIW-0132), exact byte-prefix conversion (BIW-0088) and regression-discontinuity vocabulary effect (BIW-0133) are separate works/estimands, not one “tokenization bias” result.
- MtPC v1 Multi-Token / v2 Multi-Byte title variants stay BIW-0079; do not add a second paper. Its incomplete author-header issue remains for terra. Formal/preprint exact-conversion body differences remain unverified, not silently equated.
- W0357/W0358 are distinct papers but one dependent author/data/code evidence cluster; count two works, not independent replication.
- The tagged SentencePiece v0.2.0 byte_fallback schema is an implementation attachment to BIW-0003, not an extra research paper or proof that the feature existed in 2018.
- Clockwork RNN audio-only context, S4 token-only generation claim, Unicode core chapter auxiliary fetch and unverified search leads are not extra catalog entities. S08 reserve Sampling One Byte / Cross-Tokenizer Likelihood / Broken Tokens remain unadmitted leads; no invented BIW, record or FULL credit.
