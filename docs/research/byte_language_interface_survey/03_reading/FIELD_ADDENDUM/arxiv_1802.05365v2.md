# Deep contextualized word representations (ELMo) — arXiv:1802.05365v2

**Reading status: PARTIAL — designated narrow primary extraction.** Matthew E. Peters et al., 2018, [versioned HTML](https://arxiv.org/html/1802.05365v2), [versioned PDF](https://arxiv.org/pdf/1802.05365v2). Read §§1–3.4 and Table 1. Sections 4–6 and the supplement were not fully audited, so no full-paper credit is claimed. The arXiv identifier is the stable source ID, not an invented BIW.

## Problem, solution, techniques

A static word vector cannot reflect a word's changing context or expose different levels of linguistic information. A character-CNN/highway network constructs a context-independent representation of each **word position**; a two-layer bidirectional language model (biLM) contextualizes it; the downstream model learns a softmax-weighted mixture of layer states and a scaling coefficient γ (§§3.1–3.4). The CNN composes word-internal character n-grams; highway layers gate the composition; separately parameterized forward and backward LSTMs model context; layer mixing selects task-useful representations. Pretrained biLM weights are frozen during supervised task training, after any optional domain-specific LM fine-tuning; the task head and layer weights are learned. This is an author-used transfer method, not byte-stream generation.

## Units, supervision, and sharing

Input composition uses characters **within words**, internal recurrent positions are words, and LM training predicts the next or preceding **word/token** in the respective direction via a softmax (§3.1). The exact character serialization or whether the actual implementation uses UTF-8 bytes is **not established by these paper passages**; do not classify ELMo as a raw-byte LM. Each directional LM is causal in its own direction, but their concatenated representation for downstream tasks uses both past and future full-sentence context, so it is not a prefix-only generator. EOS and streaming/partial-prompt contracts were not examined.

The forward and backward LMs share **their token-representation parameters with each other**, and share **their softmax parameters with each other**, while keeping the directional LSTMs separate (§3.1). This does **not** assert input-representation-to-softmax matrix tying. The character encoder uses 2048 convolutional filters, two highway layers and a 512-dimensional projection; the LM has two 4096-unit LSTM layers with 512 projections and a residual connection (§3.4).

## Evidence and bounded implications

The paper reports ten epochs on the 1B Word Benchmark; average forward/backward perplexity 39.7 versus the larger forward CNN-BIG-LSTM's 30.0 (§3.4). The architectures and directionality differ; this is not a controlled byte result. For the named supervised SQuAD baseline, Table 1 reports F1 81.1 without ELMo versus 85.8 with it, with task training and pretrained model resource costs; this check does not audit benchmark protocol or other numerical claims. Exact pretraining FLOPs, teacher-free-deployment implications, and runtime cost were **not examined**, not asserted absent.

Related parent question: [BIP-0005](../../02_inventory/DETAILED_INVENTORY.md#BIP-0005), the distinction between input coverage and prediction-target vocabulary. ELMo is a **character-input/word-output historical antecedent** and adds contextual layer mixture plus directional sharing; it does not solve or experimentally test that CANINE-specific pretraining question. It cannot establish open byte-output support, byte causality, or a byte-quality frontier.
