# A07 — ICLR 2027 byte/language-interface discovery and coverage

**Snapshot:** 2026-11-09. **Owner:** A07, byte/interfaces only. **Deliverable type:** executed discovery, primary-source metadata checks, selected primary passages, and version-specific reuse; **not** a final broad scientific synthesis or newly completed full-paper reading. A08 owns the broad venue stream and central access map; this work did not wait for or edit its artifacts.

Companions: [search and access log](SEARCH_LOG.md), [work/problem records](WORKS_AND_PROBLEMS.md), [precise reading handoff](READING_HANDOFF.md).

## 1. Governing questions and evidence contract

The governing scope is `../../PLAN.md` and the original [follow-up list](../../../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md), not the multigranularity proposal. Byte input, Unicode code points, characters, subword inputs, hybrid supervision, learned segmentation, patch computation and output decoding are separate dimensions. The six main axes remain compression/task sufficiency; state writing/retention/capacity; addressing/native readout; deployed use/causal measurement; learning/shortcuts; component interaction/transfer. This specialist stream intersects those axes but does not claim to discharge all six streams.

- **M-live:** official group or conference page retrieved directly in this run.
- **M-index:** a search result for an official OpenReview forum supplied title, submission label and/or date; live forum retrieval was challenged. This is weaker and potentially stale metadata, not current decision verification.
- **S-index:** only indexed passages of the official PDF are available. An ICLR 2027 under-review header is a submission lead, not verified group membership or current status.
- **A:** original abstract/history retrieved. **P:** selected original sections read. Neither means FULL.
- **R:** actual existing full-reading card read and reused at its stated version. It earns **no new full-read credit** here.

New local IDs `A07-N01`–`A07-N13` are candidate identifiers, not newly allocated global BIW IDs. BIW/W aliases are retained. Multidimensional classification is by interface, supervision, causal permission, deployment role, venue confidence and evidence depth; it is not a single ranking of maturity.

## 2. Independently verified official ICLR 2027 access and status

### What is verified

1. The [official call for papers](https://iclr.cc/Conferences/2027/CallForPapers) names the fifteenth ICLR and specifies abstract deadline **2026-09-18**, paper deadline **2026-09-25**, reviews **2026-11-05**, author/reviewer discussion **2026-11-05–18**, and final decisions **2026-12-16**, Anywhere on Earth. A submission is **not an acceptance**; no acceptance is claimed for any 2027 candidate.
2. The [official public group API](https://api2.openreview.net/groups?id=ICLR.cc/2027/Conference) returned one group with ID `ICLR.cc/2027/Conference`, public readers, website `https://iclr.cc/Conferences/2027`, title *The Fifteenth International Conference on Learning Representations*, and `public_submissions=true`. The response reports `fromCache=true`; this remains an official API response, not a live census of papers.
3. That group explicitly registers:
   - submission invitation `ICLR.cc/2027/Conference/-/Submission`;
   - active venue ID `ICLR.cc/2027/Conference/Submission`;
   - withdrawn venue ID `ICLR.cc/2027/Conference/Withdrawn_Submission`;
   - desk-rejected venue ID `ICLR.cc/2027/Conference/Desk_Rejected_Submission`;
   - rejected venue ID `ICLR.cc/2027/Conference/Rejected_Submission`.
   Its webfield defines **Active Submissions**, **Withdrawn Submissions**, **Desk Rejected Submissions**, and recent activity. This confirms that a title search must not silently collapse those states.

### What is not verified

- `FetchURL` for the group UI returned a loading shell; the built-in browser also rendered only the OpenReview loading/footer shell. Several individual forum, PDF and notes API routes returned **“Complete the check below to continue to OpenReview.”** No challenge was solved, no authentication bypassed, and no paid service used.
- The active-note query with `limit=1000&offset=0` was challenged. The notes-search query returned only a code-fence fragment, not a usable result list or count. **Zero usable submission-list pages** were enumerated; no pagination completeness claim is possible. No withdrawn/desk-rejected list was enumerated.
- Search-indexed official forum labels establish a discoverable submission record, not its current active/withdrawn/desk-rejected state. Papers with only official PDF snippets remain **unverified forum leads**. Current decisions, complete revisions, review text and latest PDF hashes are unknown.
- Authors of anonymous submissions are intentionally omitted. Public title/abstract matching to arXiv is not used to infer or report author identities. A public workshop record or author blog never proves that an anonymous conference submission was accepted.

## 3. Discovery result relative to the 141-entity byte catalog

The current [BIW catalog](../../../byte_language_interface_survey/02_inventory/WORK_CATALOG.md) contains 141 entities, not 141 new papers for this run. Its existing cards have overtaken several gaps in the older [byte audit](../../../flued_multigranularity_survey_20261108/07_scope_recovery/07_BYTE_SURVEY/COVERAGE_AUDIT.md): CANINE, Charformer, MANTa, MEGABYTE, classical sharing, marginal likelihood, multi-byte output, Scratchpad Patching, AU-Net and cross-interface distillation already have scoped full cards. **The older audit's “unread” labels must not be copied into the v2 queue.**

Title/stable-ID checks against both the BIW catalog and the earlier broad catalog found no matching record for the thirteen local candidates below. This is a catalog-gap claim, not proof that no unpublished note anywhere mentions them. Twelve have interpretable discovery evidence; `N13` is explicitly a title-only/unread mechanism lead.

| Discovery cohort | Concrete result | Permitted use |
|---|---|---|
| Official indexed 2027 forums missing from BIW | Turnip, Compiled Tokenizers, PriorBPB, ByteMark, Why Pretraining Fails to Share Cross-Lingual Knowledge | Searchable venue index with dates/status confidence; no current-state or acceptance claim |
| Official 2027 PDF leads missing from BIW | MRT; Separating Script and Vocabulary Effects; Learning to Retokenize; LEAD; BridgeSTOP; GlitchPatch; Who Gets a Token; Constructive Prediction | Discovery/reading candidates; forum/group membership and latest version still need confirmation |
| Existing BIW, newly recovered official 2027 PDF association | BIW-0103, *Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models* | Reuse v1 card; title-matched under-review PDF is not a new work or new FULL |
| Existing BIW, significant newer source | BIW-0076 Scratchpad Patching **v2, 2026-11-06**, versus card **v1, 2026-05-10** | Selected version-difference evidence; update-only reading needed |
| Existing recent controls rechecked by arXiv histories | BIW-0078 v4; BIW-0079 v2; BIW-0015 v2; BIW-0028 v1; BIW-0097 v2; BIW-0077 v1 | Version-scoped reuse; no ICLR 2027 association inferred |

These are discovery cohorts, not additive paper/full-reading totals. All details and uncertainty fields are in [WORKS_AND_PROBLEMS](WORKS_AND_PROBLEMS.md).

## 4. The most consequential recovered version: Scratchpad Patching v2

[Current history](https://arxiv.org/abs/2605.09630) lists v1 on 2026-05-10 and **v2 on 2026-11-06**. The existing [BIW-0076 full card](../../../byte_language_interface_survey/03_reading/R05/BIW-0076.md) reads v1. This run read selected [v2 original passages](https://arxiv.org/html/2605.09630v2), especially §§4–5, §7 limitations and Appendices B.3/C.2/D/E.4, and compared the corresponding v1 saved source around C.2/D. This is **P, not FULL v2**, and not an exhaustive textual diff.

### Changes material to conclusions

- v1 C.2 says all models are roughly 2B and describes the main approximately 400B-byte runs. v2 adds/foregrounds **500M and 2B, approximately 100B-byte scale/data comparisons**, Appendix C Table 4; §4.2 reports fixed-p8 500M BPB **0.7833 → 0.7425** with scratchpads but flat-byte **0.7283**. Thus improving a compressed baseline does not establish beating a flat model at the smaller scale/budget.
- v2 explicitly states that **every configuration is one training run**, with no seed variance (C.2). The v1 card correctly left this unknown; it should now be updated to the narrower statement for v2.
- v2 explicitly says **serving latency and throughput are not measured** (Appendix D), and KV reduction counts **persistent trunk patch states only** (Table 2 caption). These are analytical proxies, not whole-model resident memory or wall-clock acceleration.
- v2 quantifies training-FLOP multipliers over corresponding non-scratchpad patchifiers: **1.74× fixed-p8, 1.49× SpaceByte, 1.47× entropy, 1.41× H-Net** (§4.3). It retains the **H-Net failure at strict matched training FLOPs** (§5.1), rather than making all boundary families equally successful.
- v2 B.3 distinguishes main H-Net trigger **2.5** from the separate **1.5** checkpoint used for the inference-frequency ablation/illustration. Do not merge those checkpoint conditions.

**Inference:** this changes the follow-up priority from “read Scratchpad Patching from scratch” to “read and integrate v2 additions, inspect Table 4 and changed figures visually, retain v1 provenance.” It strengthens non-retrieval alternatives that decouple persistent storage from fresh causal computation. It does not establish a repair for FLUED or authorize an experiment. A NeurIPS checklist in the PDF is not venue/acceptance verification; this work stays in the general-literature section.

## 5. Key subdirection → existing synthesis / unread / new search / experiment

The main category is not exclusive: literature may suffice for explaining a mechanism while still being insufficient to select a production architecture.

| Subdirection and discriminating question | Adequate existing synthesis, with actual card/version | Unread existing or new search/read gap | Genuinely new empirical question, not executed |
|---|---|---|---|
| Raw bytes vs codepoints vs subwords; does deployed vocabulary freedom require vocabulary-free supervision? | BIW-0004 CANINE v4; BIW-0008 MEGABYTE v2; BIW-0077 AU-Net v1. Distinguish codepoint masked encoder, byte AR, rule hierarchy | N01 Turnip and N13 lexical-code organization; no new verified codepoint-native 2027 generator found | Same raw-text exposure and causal permission, change interface without changing host/decoder budget |
| Learned boundaries vs aggregation vs update frequency | BIW-0078 v4, BIW-0108 v2 and BIW-0076 v1 support a mechanism-level comparison | **BIW-0076 v2 update**; N01 Turnip; N02 MRT. Existing BIW-0040/0041 segmental models remain non-FULL in catalog | Hold persistent count/rate fixed while independently varying boundary rule, aggregation and transient updates |
| Streaming segmentation and train/generate consistency | Existing BIW-0078/0077 cards explicitly leave prefix stability/cache behavior unverified | N11 BridgeSTOP; N10 Learning to Retokenize. Need actual prefix, flush and partial UTF-8 contracts | Identical-prefix/different-future test, cache reuse and output equivalence at chunk boundaries; no full-sequence hints |
| Joint future bytes vs factorized proposals vs bytewise output | BIW-0079 v2, BIW-0015 v2, MEGABYTE v2 already cover distinct output distributions | No new confirmed 2027 raw-byte decoder beyond title-matched distillation found; N12 LEAD may affect output legality/preferences | Same target verifier/distribution, include EOS, proposal cost, rejected work, prefill and batch/concurrency |
| Byte input with subword supervision / converting frozen hosts | Existing BIW-0103 v1, BIW-0097 v2, BIW-0098 v1 and BIW-0099 v1 carry distinct mappings; R06 queue is not unread | N10 learned retokenization, N09 GlitchPatch and N04 compiled action spaces expand the interface interventions | Same-host self-connection and equal adaptation budget; distinguish interface distribution mismatch from intrinsic component defect |
| Multilingual morphology, script length and vocabulary coverage | Existing BIW-0104 MYTE v2 and BIW-0051/W0518 TokSuite v2 support conditional synthesis, not universal byte fairness | N02 MRT; N03 script/vocabulary decomposition; N07 disjoint-token cross-lingual pretraining; N12 LEAD | Same semantic content/raw bytes/compute as separate arms; normalization, script and language-switch strata |
| Character/string detail and lexical access | Existing CANINE v4, AU-Net v1; character benchmark cards already exist | N08 Who Gets a Token, N09 GlitchPatch, N10 learned retokenization | Exact names/identifiers/numbers and semantic answers separately; matched strings/normalization, not spelling alone as memory use |
| BPB and causal use of context | Existing BIW-0080 formal EMNLP 2021, BIW-0103 v1 and TokSuite v2 make marginal vs canonical path and accuracy limitations concrete | N05 PriorBPB, original paper/revisions still blocked; blog is P, not paper FULL | Controlled length-preserving content substitutions; distinguish an answer-length metric artifact from content-use failure |
| Shared embeddings and output geometry | Existing BIW-0035 v3, BIW-0036 v3 and BIW-0037/W0366 already form a positive/negative chain | Existing BIW-0038 pseudo-inverse tying is non-FULL; no verified new 2027 byte-head factorial found | Input/output tying × output normalization × small vocabulary, with matched optimizer and host |
| Tokenizer-independent downstream interface | Existing BIW-0088/0099 cover byte-probability/transfer distinctions | N06 ByteMark is an adjacent public-text-carrier example, not byte-native LM quality evidence | Transfer a detector/readout across tokenizers without assuming transferable hidden coordinates |
| Deployment resources | Existing MTPC v2 includes real decoder timing; MEGABYTE includes limited timing; other cards delimit estimates | N11 streaming pipeline; N01 entropy/local modules; v2 Scratchpad cost clarifications | Matched quality on the same hardware with all teacher, local state, packing, tokenization and verification costs |

## 6. Independent alternatives that do not require source revisit

These are competing research hypotheses, not selections or authorized trials.

1. **Refresh computation, not source storage:** transient within-patch states (BIW-0076) can distinguish stale global context from irreversible information loss.
2. **Keep fine-resolution recurrent state:** MambaByte/flat hybrid byte models (BIW-0025/0028) distinguish explicit segmentation necessity from a state-update/readout bottleneck.
3. **Use fixed/rule segmentation with a stronger local path:** MEGABYTE/AU-Net counter learned-boundary necessity; match update delay and output factorization before comparing.
4. **Change the boundary-learning estimator/objective:** score-function learning (BIW-0078) versus straight-through or externally annotated boundaries; do not confuse lower surrogate loss with actual generative accuracy.
5. **Transfer objectives across interfaces:** BIW-0103/0098/0099 change supervision; marked EOT probabilities are not automatically exact unmarked-byte marginals, and teacher cost is not free.
6. **Repair a frozen host's input segmentation:** GlitchPatch and learned retokenization can change composed lexical inputs while preserving the published string, without adding source retrieval or retraining the host. Generalization and search cost remain open.
7. **Fix output probability/decoding allocation:** MTPC, dynamic multi-byte prediction or encoder/decoder capacity redistribution change output cost and dependence without retaining a source index.
8. **Change encoding or metric:** morphology-aware/script-aware interfaces and PriorBPB can expose mistaken fairness/quality diagnoses without changing state capacity at all. Such measurement repairs are not proof that the model's semantic use improves.

## 7. Controls and counterexamples that must travel with any later synthesis

- **CANINE v4:** codepoints, not UTF-8 bytes; optional subword pretraining is compatible with a tokenization-free deployed encoder. More stride harms QA; n-gram memory can help entity tasks. This prevents an all-byte causal-LM retelling.
- **MEGABYTE v2:** serial local conditional outputs represent dependence; a million-byte image result is not million-byte text use. Longer text context did not monotonically improve its tabled result.
- **MambaByte v3:** a fixed recurrent state is a real alternative; top-3 draft acceptance does not certify exact greedy or sampling equivalence.
- **MTPC v2:** more accepted bytes can mean slower generation; larger probabilistic heads add substantial parameters, and EOS-suppressed timing is not complete answer latency.
- **RL tokenization v4:** uniform patching wins the reported ARC-Easy BPB cell; BPB is not task accuracy. Discounted rewards are biased; shifted offline BPE labels are not proven prefix-stable.
- **Byte simulation v2:** effects called throughput or boundaries have target-density/visibility confounds; temporary subword heads can hurt after withdrawal.
- **Classic tying v3:** word/BPE sharing can improve generalization yet fail for other objectives/settings; it is not a byte-vocabulary theorem.
- **Cao–Rimell 2021:** normalized canonical-token loss is not automatically marginalized string likelihood. This issue is distinct from PriorBPB's answer-length mixture.

## 8. Coverage limits and handoff decision

**Sufficient now:** reconstruct comparison coordinates, reuse version-locked classic/recent cards, document a real 2027 candidate set, and formulate alternatives independent of source revisit.

**Still blocked:** a live, paginated 2027 forum census; current active/withdrawn/desk-rejected status and submission revision hashes; full texts of several anonymous 2027 candidates. **Not done:** original full reads for the new candidates, review-based adjudication, any experiment, production change, evidence-registry update, installation, commit, or final total-report synthesis.

The [handoff](READING_HANDOFF.md) prioritizes twelve missing original readings plus one separate version-update task, with explicit access and download boundaries. Coverage is limited, not exhausted.
