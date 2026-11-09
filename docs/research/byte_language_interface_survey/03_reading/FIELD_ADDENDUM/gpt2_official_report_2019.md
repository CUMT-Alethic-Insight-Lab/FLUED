# Language Models are Unsupervised Multitask Learners (GPT-2 report) — official 2019 report

**Reading status: PARTIAL — designated narrow primary extraction.** Alec Radford et al., [official OpenAI report PDF](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf), p. 4 §§2.2–2.3 and adjacent §3.1, visually read in the browser. The official URL is the stable source identifier; this PDF is not revision-pinned. The rest of the report, performance tables and appendix were not fully audited. No BIW is assigned.

## Problem, proposed solution, and method roles

A fixed Unicode code-point alphabet can be large or exclude symbols, whereas the authors report a preliminary WebText quality gap for their standard raw-byte LMs relative to word-level systems. Their compromise is **byte-based byte-pair encoding (byte BPE)**: begin with 256 possible byte symbols, learn frequent adjacent merges, and operate the language model on the resulting vocabulary of merged pieces (§2.2). Greedy frequency-based BPE is the learned compression/vocabulary-construction method; the Transformer is the causal next-piece predictor (§2.3). The report says unrestricted merges waste vocabulary on word-plus-punctuation variants such as `dog.` and `dog!`, so it prevents merges across character categories with an exception for spaces. These constraints are part of the reported preprocessing contract, not properties of all byte-BPE schemes.

## Units and causal contract

The representation starts from UTF-8 bytes, but the actual **input and model positions are merged byte-BPE symbols**, and the next prediction is a vocabulary symbol, not one of 256 raw bytes. The adjacent model section specifies a **50,257-entry vocabulary** and context of **1,024 model tokens**, not 1,024 bytes. Learned merges and category pre-tokenization must be distinguished from UTF-8 coverage. The report's string-probability claim describes its own evaluation; probability of a selected canonical tokenization path, unmarked string marginal and byte-prefix event are different estimands, not automatically equal. Actual prefix stability of the complete-string tokenizer and EOS/partial-byte-output handling are **not established by this narrow check**. No separate byte entropy teacher is stated in §2.2.

## Evidence and scope

Section 2.2 says the authors observed standard byte-LM underperformance on WebText in preliminary attempts, but gives no fully specified matched-compute comparison there: this is a reported observation, **not a quantified general frontier**. Section 2.3 reports 1,024 model-token context and Table 2 gives model sizes; neither is a measured byte-normalized training or serving budget. Benchmark results elsewhere, tokenizer training cost, exact byte exposure, and real-time throughput are **not examined** here, rather than declared unreported in the full report.

## BIP implications

This is a primary historical anchor for byte-complete **subword** modeling, distinct from both code-point BPE and raw-byte next-step modeling. It is related to [BIP-0005](../../02_inventory/DETAILED_INVENTORY.md#BIP-0005)'s broader input-versus-supervision distinction, not the same CANINE mechanism. The byte alphabet supplies coverage but does not make output units bytes or prove equality between string and prefix probabilities. Pair with the established prefix-probability work [BIW-0088](../../02_inventory/WORK_CATALOG.md#BIW-0088) rather than deriving those later results from this report.
