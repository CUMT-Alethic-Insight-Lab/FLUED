# A08 — Broad recent advances and venue-coverage findings

2026-11-09. Scope owner: `01_discovery/A08/` only. This is an executed discovery/audit handoff, **not the final six-axis scientific synthesis, architecture selection, or an experiment authorization**. See [executed searches](SEARCH_LOG.md), [work/problem register](WORKS_AND_PROBLEMS.md), and [prioritized reading handoff](READING_HANDOFF.md).

## 1. Principal findings and what changed

1. **ICLR2027 is officially verifiable and selected public submissions are searchable, but this session did not enumerate the venue.** The [official CFP](https://iclr.cc/Conferences/2027/CallForPapers) places final decisions on2026-12-16. The [official group JSON](https://api2.openreview.net/groups?id=ICLR.cc/2027/Conference) verifies the venue and three public status streams. The UI remained at `Loading`; direct `/notes` list/individual routes and two PDFs returned a verification wall. Public `/notes/search` independently supplied forum IDs, exact titles, abstract text, record versions and active/withdrawn/desk-rejected venueids. **An official active submission is not an accepted paper.**
2. **The strongest new discovery value is not another source-revisit system.** Official recent submissions directly target state-dependent forgetting (V04), memory-update geometry (V03), inner-learning approximation (V05), output-dependent readout (V06), receiver-state compatibility (V14), training incentive (V02), early routing lock-in (V22), and task-predictive state (V24/V25). These survive a scope criterion that asks which broken information-chain link is being repaired, not whether the system has a hierarchy.
3. **Some current benchmark gaps can be optimization/accessibility gaps at demonstrably sufficient state, but this is conditional evidence, not capacity irrelevance.** R01 selected body sections show fixed-state curriculum changes and large learning-rate sensitivity; R02 selected §5–6 shows oracle gates can rescue query-first retrieval while native gates lag decodable relevance. V02 and V22 offer important new submitted hypotheses about supervision and timing. They must be paired with finite-capacity controls, unseen-query tests and actual native content dependence.
4. **Readout/consumer reforms deserve their own budget line.** V06's channel-conditioned bilinear readout, V12's survivor compensation, V20's finite-query cache construction, and V13/V14's stitching counterexamples concern **using or aligning representations**, not simply retaining more source. Their domains and permissions differ sharply; none directly establishes FLUED behavior.
5. **Existing evidence needs reuse and reconciliation, not another inflated FULL total.** Existing W0229/W0092/W0333/W0337/W0192/W0534 cards were actually opened, and W0050 remains PARTIAL. The newer BIW Charformer card demonstrates that some older W-only “unread” labels are stale. New venue records are abstract/metadata depth; selected primary bodies R01/R02/R07 are partial. **New full readings in A08: zero.**

### Working vocabulary, not new project terminology

Fast weights (**快速权重**: parameters updated from the current sequence to store transient associations); linear attention (**线性注意力**: attention-like processing with a recurrent/finite-feature aggregation rather than explicit all-pair softmax); state-space model/SSM (**状态空间模型**: sequence computation by an evolving internal state); native readout (**原生读出**: the actual deployed reader, with its real query visibility and training permissions); model stitching (**模型表示拼接**: connect frozen model pieces through a restricted learned interface); causal positivity (**因果正性**: each tested treatment must have nonzero assignment probability for identification). These are literature mechanisms with Chinese semantic anchors, not newly proposed named modules.

## 2. What coverage was actually obtained

| Dimension | Achieved | Not achieved / do not infer |
|---|---|---|
| Official venue identity | CFP and group JSON, exact invitation/status identifiers | Venue-wide bibliography or acceptance ledger |
| Public access | Official search abstracts and metadata; recent arXiv primary pages; selected bodies | Unread OpenReview PDFs, supplements, reviews, or private content |
| Pagination | Unquoted linear-attention offsets0–14; quoted associative-recall offsets0–9; other first pages explicitly logged | No exhaustion of196 quoted-linear or44 quoted-recall hits;10000 counts not verified totals |
| Classification | Six original axes, source access permissions, learning route, evidence depth, venue state, existing/new/recovered | No binary “multigranularity/not” or “enough/insufficient” as master classification |
| Scientific inspection |25 active forum metadata records,7 recent/recovered controls,3 status-control records;8 actual reused card entries | No additive count of globally new works or papers fully read; concurrent streams not deduplicated |
| Temporal reach | 2026 recent work and older controls actually relevant to gaps | No all-2026/all-ICLR2027 claim; newest revisions not systematically compared |
| Source permissions | Closed recurrent states, finite/query-aware compression, known-state teachers, external stores and hybrid KV distinguished | No assumption near-linear runtime implies constant-state, or all methods have the same retained information |

The main register extends slightly beyond a nominal15–30-work target because the work is a venue-access stream and includes independent controls; it is not quota completion. The critical result is precise searchable metadata/limitations and a discriminating queue, not a count. R01–R07 are **recovered** prior candidates/IDs, not seven discoveries made from nothing.

## 3. Audit of the older scope bias

Inputs actually read: original FOLLOWUP_DIRECTIONS; the six matching axis COVERAGE_AUDIT files and global audit; prior global SEARCH_LOG; selected current cards and catalog identity/version records. Old synthesis itself was **not re-read in full**. The document-location diagnosis below is therefore inherited from those explicit matching audits, while current card/version changes were directly checked here.

### 3.1 The selection target had changed

The [prior global audit](../../../flued_multigranularity_survey_20261108/07_scope_recovery/08_GLOBAL_SCOPE/COVERAGE_AUDIT.md) locates old REPORT's governing object in the multigranularity proposal and old red-team closure in H1–H5/four-scale coverage. That establishes a **scope mismatch**, not that its local evidence is worthless. Querying whether coarse-to-fine source access beats flat revisit cannot by itself answer why a compressed state fails to become a naturally used memory.

The older reports did contain regression, usable information, content-specific interventions and formation-history caveats. It would be inaccurate to say those topics were absent. The failure was their **organizational priority and unresolved core unread sources**, e.g. GDN/TTT/Titans and classic optimization/transfer originals. More source-lifecycle and navigation papers did not close state-update, native query or learning-history gaps.

### 3.2 Biases this pass explicitly resisted

- **Retrieval-first framing:** V03/V04/V05/V06/V15/V16/V17/V22/V25 and R03/R04/R06/R07 do not need original-source revisit. They enter because they target a substantive original question.
- **Aggregate leaderboard as mechanism:** V11 reports a matched-FLOP limitation; V21 changes terminal attention necessity by task; V01 claims hybrid recall can reside mostly in full KV. A better hybrid score does not prove the recurrent state is used.
- **Total-card count as coverage:** prior audits'219FULL/11PARTIAL snapshot is not a denominator for B/C/E/F adequacy. No recount was performed here. Actual relevant scoped cards and unresolved questions are named instead.
- **New search as false novelty:** R01/R04/R05/R07 were already found by scope-recovery agents, R02/R03 already have W IDs, and R06 has BIW-0096. They are recovered/reverified, not locally newly invented discoveries.
- **W-only inventory freeze:** current BIW full cards supersede older unread labels where applicable. Actual BIW-0005 v3 was opened; [WORK_CATALOG](../../../byte_language_interface_survey/02_inventory/WORK_CATALOG.md) shows returned scoped cards for CANINE/MANTa/MEGABYTE. A07 handles detailed interface interpretation.
- **Recent-arXiv venue laundering:** R01–R05 remain venue-unverified. No anonymous forum is matched to named arXiv authors. Metadata keywords, an author's manuscript heading and search snippets do not certify venue status.
- **Architecture-family verdict from one counterexample:** R01's local toggles and R02's Mamba-2 gates motivate tests; neither proves every recurrent failure is optimization or that every architecture has sufficient state for arbitrary future details.

## 4. Six-axis subdirection map: reuse, unread, new discovery, and empirical obligation

These are **multidimensional actions**, not mutually exclusive labels. `S` = enough existing evidence for a **bounded synthesis statement**, not architecture selection; `U` = existing but unread/partial source to complete; `N` = actual new-search metadata/primary selection to read; `X` = a genuinely new target-system experiment would be needed. All experimental statements are proposals, unexecuted and unauthorized here.

| Original subdirection | S: adequate existing bounded synthesis | U: existing evidence still unread/incomplete | N: actual recent discovery/recovery in A08 | X: what only a new experiment can settle |
|---|---|---|---|---|
| A: reconstruction vs task sufficiency | W0092 limited reader; W0023 response-reconstruction and W0038 mixed objectives via prior compression audit | W0067 rate-dependent objective ordering; W0066; do not replace with titles | V20 known-query exactness; V25 predictive rank; R07 prediction-state original | Fixed rate × objective × native consumer; rare-detail and task-shift performance |
| A: decoder ignores an available code | W0050 content vs constant-channel distinction; W0092 reader optimum | BIW-0096/R06 selected older evidence, not full | V17 surplus/strategy-sensitive latent objective | Freeze same code, train only bounded consumer vs writer-only/combined; equal extra compute |
| A: unknown future query vs known task family | W0061 finite-state copying conditions (prior card) and W0092 | W0080 and W0059 actual full scopes should be reused, not re-counted | R07; V20 explicitly finite protected-query set | Query-before/after and held-out query family under identical persistent-information contract |
| A: low-variance/rare information | Existing theory distinguishes retained information from usable information | W0067 and actual rare-detail benchmarks, not mean-reconstruction evidence | V25 suppression below predictive rank | Vary detail rarity independently of entropy, output frequency and available state bits |
| B: additive vs residual/corrective writes | W0229 unifies statistics, SGD and Gram correction | W0199/W0228/W0201 originals remain key unread chain in prior audits | V03; R03/R04 | Same keys/values, repeated and conflicting updates; total state and precision matched |
| B: erase/retention independence | W0229 nonstationary regression; existing LoLA/MoM cards via prior state audit | W0202/W0203/Titans/TTT updates need exact comparison | V04 feedback; R04 distinct erase address | Cross write-direction × erase-direction × gate-strength; delayed future utility |
| B: load vs delay vs similar distractors | W0212/W0229 conditional interference mechanisms via state audit | Zoology W0060 and Revisiting W0088 full-read gaps | V01; R01 selected §§4–6; R02 | Independently change number of stored bindings, elapsed steps and distractor similarity |
| B: nominal/effective/finite-precision capacity | Existing finite-state bound is not effective-bits measurement | W0086/V07 arXiv-forum version equivalence; classical low-precision retention gap | V08/V09 tensor state; V12 pruning; V23 prefill quantization | Total resident bits, covariance/optimizer buffers, roundoff, retention and rare-detail use |
| C: stored association vs native query | W0229 and W0092 already expose optimal/native gap | W0219 multihead linear attention and W0370 probing cost, not title-level coverage | V06 channel-specific readout; R02 gate/read relevance lag | Fixed bank with native, same-budget learned, and oracle-address queries; oracle separate |
| C: independent addresses/content/read-write consistency | Prior address audit's Landmark/HISA/Merlin/RAM cards | D-NTM original selected recovery; K/V asymmetry and normalization sources | V24 fixed-bank address derangement; V04 feedback | Address-only, value-only, binding-only changes plus true identity interface |
| C: multiple queries/tensor state vs more bytes | Prior MoM card distinguishes shared q from independent readout | MHLA W0219 original, RunningTensor/Triadic bodies | V08/V09/V10 | Match total state, read bandwidth and train FLOPs; distinguish tensor factorization from extra capacity |
| C: query-specific preservation vs unknown deployment queries | W0092 makes consumer restrictions explicit | Prompt-compression W0076 and finite-query theorem body | V20 | Known protected queries, unseen paraphrases, different task queries and free rollout scored separately |
| D: readable vs naturally consumed vs correct evidence | W0050 PARTIAL/W0192/W0534 sufficient for bounded distinction | W0050 missing supporting evidence; W0533 activation-patching standards | V01,V19; R02 selected actual patching body | Correct/wrong/constant/no-channel with non-target preservation and answer flip |
| D: retrieval omission vs useless memory | Prior causal audit's attribution limits; W0050 doesn't include retrieval in gold-evidence QA | W0383/W0384 conditional credit limits | V18 known-propensity retrieval intervention | Test unsurfaced items with randomized exposure; retention needs future-query weighting |
| D: mediator interaction and compensation | W0337 terminal compensation; W0534 patch-control caveat | Older causal audit's Hydra/multiple-mediators originals | V19 four counterfactual trajectories; V21 task-dependent removal | Same-background factorial interventions, repair controls, natural full recomputation vs local patch |
| E: incentive/accessibility vs capacity | W0333 gradient starvation, W0337 formation; no local diagnosis follows | W0088/W0213/W0332; R06 not completed | V02,V22; R01 curriculum | Keep state unchanged; control cumulative training, curriculum timing and task sampling; multi-seed trajectories |
| E: finite-data reuse and loss hides mechanism | W0333 conditional theory; existing W0331 same-direction caveat from prior audit | GradNorm/PCGrad-like full scope must not imply universal benefit | V15 finite-data dynamics; V16 trajectory objective | Measure actual optimizer updates and content consumption over time, not terminal cosine/loss only |
| E: latent bypass/objective mismatch | Existing W0050 constant/zero contrast; W0023/ICAE objective differences | R06 inference-lag original; W0067 rate effects | V17, R07 predictive objectives | Read/write relative update speed and stage order at equal total opportunity |
| F: transplant compatibility vs intrinsic defect | W0092/W0337 and prior transfer audit's self-stitch logic | LoLCATs/MOHAWK/Yosinski/stitching originals selected but no new FULL here | V13 answer transfer; V14 receiver dependence; R05 frozen host | Same-host self-stitch, matched connector/random source, frozen vs limited adaptation, task vs feature matching |
| F: companion components and placement | Prior transfer audit cites local paths/convolution/learning-rate confounds | GDN W0201 original and R05 selected body | V21 placement; R01 tuned component factorial | Component × companion × host, including formation-vs-repair histories |
| F: extra reasoning computation vs better memory | Existing regression can change readout without new source | Atlas full-card capacity caveat must remain | V11 matched-FLOP caveat; V05 sequential-update approximation | Extra pass matched by generic extra-compute baseline; causal permission and recurrent-state reset rules fixed |

**Synthesis can already proceed on bounded conceptual distinctions** in the S column. **Full reading remains necessary for numerical/theorem/algorithm recommendations** in U/N. **Architecture selection and local mechanism attribution remain experimental** in X. These claims do not say the academic field is exhausted.

## 5. Independent alternatives to multi-resolution source revisit

Source revisit means retaining or recovering past fine-grained source after a later query. The following alternatives target different failures and must not be evaluated by whether they implement that mechanism. Table entries are candidates, not defaults.

| Alternative | Information retained / changed | Credible original anchors | Minimum distinguishing control / outstanding cost |
|---|---|---|---|
| **Task-predictive closed state** | Preserve statistics sufficient for a declared future task/process, not reconstruct all past text | R07, V25; W0092 reader restriction | Prediction sufficient for one task is not arbitrary unknown-query memory. Compare objective/rate/task shift; no free source archive. |
| **Interference-aware writes and forgetting** | Same nominal recurrent bank, change covariance, correction geometry, erase address or state feedback | W0229; R03,R04,V03,V04 | Account covariance/feedback buffers and extra compute; repeated-key correction and unrelated-fact damage separately. |
| **Native query/readout repair** | Keep representation, change limited decoder/query geometry or compensate surviving directions | V06,V12; W0092/W0229 | Fixed writer and source permissions; compare oracle/extra-supervision readers separately. Vision readout must first become causal. |
| **Training incentive and formation timing** | Same state capacity, different data repetition, gap curriculum, route warm-up or relative updates | V02,V22,R01,R06; W0333/W0337 | Equal cumulative samples/updates/FLOPs as separate budgets; randomized timing and later recovery controls; held-out symbol/query tests. |
| **Receiver/connector adaptation** | Freeze compressor/source and adapt restricted consumer interface or companion transforms | V13,V14,R05; prior LoLCATs/MOHAWK audit | Self-stitch and random/constant source; transferred answer information is not transferred computation; teacher cost explicit. |
| **Same-scale tensor/multi-state decomposition** | Change binding order/query factorization rather than hierarchical source resolution | V08,V09; existing MoM/RAM cards | Fixed total bits and bandwidth; otherwise extra state is the explanation, not tensor order. |
| **Function-preserving numerical reparameterization** | Keep ideal full-precision map, alter quantization geometry | V23 | Full-precision invariance plus low-precision deployment; test long-state retention, not just prefill PPL/latency. |
| **Bounded hybrid exact exception or local path** | Add finite exact KV/local bandwidth, not arbitrary source revisit or a tree | V21 and prior LoLA/RAM/transfer cards | It is **not** a pure closed-state comparison. Separate total cached information and which path actually carries causal content. |

The external-store utility/causal papers V18/V19 inform evaluation, not a claim that a source-free compressor should implement agent memory. V10 is quasi-linear computation; until its retained information is read, it should not be marketed as constant-state. Multi-resolution source revisit remains another valid competitor under its **larger information-access contract**, not a universal explanatory theory.

## 6. Benchmark and methodological counterexamples that must survive synthesis

| Tempting claim | Specific counterexample/control | What it does and does not establish |
|---|---|---|
| Better perplexity means better exact recall | V02 claims precise recall deficit despite similar/better LM loss; W0050 separates reference utility/content | Need recall-sensitive slices and natural content tests; not evidence LM objective is universally unsuitable. |
| Recurrence fails because state is too small | R01 selected body: unchanged state learns with curriculum; R02 query-first + oracle gates; V02 supervision change | Capacity alone insufficient for these regimes; does not negate random-detail storage lower bounds. |
| Query-first fixes recurrent memory | R02 still fails natively; R01 selected §7 hits report no causal/bidirectional advantage in its tested task (not a full reading of §7) | Query visibility is a permission/control, not a guarantee of usable relevance. |
| A convolution ablation proves a recurrence-class gap | R01 §4.2 tuning substantially shrinks delta-family convolution gap; §4.3 diagonal ablation not representative of all Mamba | Within-cell effect and architecture-family ranking are different; retain tuning and reference quality caveats. |
| More rank/state is always the cure | V07/V12 report large pruning with compensated quality | Could reveal unused/redundant state; mean-NTP preservation not rare-detail retention or state capacity irrelevance. |
| Multiple passes are a free gain | V11 abstract says matched-FLOP overall result is slightly weaker | More computation vs more effective memory must be separated. |
| A successful stitch transfers computation | V13 says answer already present at donor site transfers; V14 shows receiver-state dependence | A high-score adapter can be an answer channel and may exploit supervised information; no universal impossibility of transfer follows. |
| A pathway is unnecessary because final ablation has little effect | W0337 formation vs terminal compensation; V21 parity vs recall removal difference | Need formation history and task-specific paths; no presumption all residual/local routes are toxic. |
| MQAR solved means every past position retrievable | Official withdrawn Selective-but-Not-Broad record contrasts content/position tasks; R01 held-out/length cautions | Different task contracts; withdrawal does not invalidate the counterexample idea, but its claims require body scrutiny. |
| Information or patch control implies natural use | W0092/W0534, R02 oracle positions, V19 latent traces with absent natural responses | Restricted-family optimum, edited capacity, probe readability and actual deployment dependency remain distinct. |
| Memory never retrieved must have zero utility | V18 positivity failure | Randomized exposure can identify current effects, but cannot alone determine future retention policy. |
| Finite-query exact compression preserves arbitrary future questions | V20 explicitly needs a finite protected set/known trace and rank/realizability conditions | Exactness under narrow permissions is valuable, not universal task sufficiency. |

## 7. Immediate scope handoff, not final synthesis

- Catalog owner: preserve V forum IDs/statuses and local R aliases; deduplicate parallel discoveries; do not equate note version2 with PDF revision2. Keep existing W/BIW versions and restricted FULL scopes.
- Reading owner: take the14-item queue in READING_HANDOFF, stop broad searching where a primary and counterexample already distinguish the problem. OpenReview full text still blocked; do not silently replace a blocked paper with its abstract.
- Axis owners: use the per-subdirection S/U/N/X map, then integrate actual full-reading results. Retain inaccessible sources as evidence gaps, not invented conclusions.
- Coordinator: A07 remains the detailed byte/interface/ICLR2027 stream. This pass only reuses the newer BIW evidence to repair stale unread labels. No complete English/Chinese total report, experiment run, production change or evidence-registry decision was made.

## 8. Validation boundary

Four Markdown deliverables only, all within assigned A08. Source verification is logged call-by-call or through exact templated query parameters. No proof/code/result replication, no paid access/install/commit/training. Static UTF-8/key/link checks and Git hygiene checks cover the delivered documents; they do not transform author claims into certified findings. Venue and literature coverage remain explicitly partial.
