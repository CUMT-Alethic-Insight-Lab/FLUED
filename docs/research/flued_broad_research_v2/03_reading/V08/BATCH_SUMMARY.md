# V08 — batch summary and access ledger

Snapshot 2026-11-09. Eight assigned work-level tasks, eight cards. This batch covers predictive-state theory, transient byte computation, multilingual training and frozen-model interface repair; it does not recommend an architecture. FULL describes source reading, not verified proofs/code or independent reproduction.

| Card | Locked source and actual coverage | Disposition / counting |
|---|---|---|
| [BIW-0076](BIW-0076.md) | arXiv 2605.09630v2; §§1–7/A–E; full PDF text and Figures 1–15/Tables 1–4 visually inspected | **FULL v2 version update**; v1 FULL separately reused; zero new works |
| [BR-A07-N07](BR-A07-N07.md) | arXiv 2609.19291v1; §§1–9/A–K; full PDF text, figures and central tables | **FULL newly completed** |
| [BR-A07-N09](BR-A07-N09.md) | arXiv 2610.04399v1; §§1–7/A–H, proof text, figures and central tables | **FULL newly completed** |
| [BR-A08-R07](BR-A08-R07.md) | 2001 institutional manuscript, revision unknown; introduction, §§1–3, theorem/lemma and proof text | **FULL paper-text read**; diagrams not independently inspected; not an independently checked proof. Under a stricter figure-inclusive count, retain as PARTIAL. |
| [BR-A08-V02](BR-A08-V02.md) | Official Incentive submission UUldzWxIL4 | **BLOCKED** body; abstract/status only |
| [BR-A08-V22](BR-A08-V22.md) | Official Routing submission 9vT48Lms48 | **BLOCKED** body; abstract/status only |
| [BR-A08-V25](BR-A08-V25.md) | Official predictive-state bottleneck submission 58JxyfvZJj | **BLOCKED** body; abstract/status only |
| [BR-A08-V14](BR-A08-V14.md) | Official receiver-state stitching submission 2M4nt7AFuD | **BLOCKED** body; abstract/status only |

**Counts:** 3 newly completed missing-original paper-text reads including R07's explicit diagram limitation; 1 newly completed FULL v2 update, not another work; 4 blocked bodies. Strict figure-inclusive count: 2 new FULL originals, 1 PARTIAL R07, 1 FULL update, 4 BLOCKED. One prior FULL v1 and the audit's earlier Table 4 are reused; Table 4 is now also independently inspected from v2. Eight tasks are not nine works.

## Main bounded findings

- The 2001 predictive-state construction assumes known finite POMDP dynamics and stores probabilities for future action/observation tests. It shows existence rather than learnability or stable finite-precision filtering; predictive sufficiency is not arbitrary history reconstruction. Original schematic images remain unavailable.
- Scratchpad v2 Table 4 p.20 has p8+SP BPB 0.7425 vs flat bytes 0.7283 at 500M/100B; 2B/100B 0.6920 vs 0.6933; 2B/400B 0.6345 vs 0.6366. Each cell is one run. At matched training FLOPs H-Net regresses (Fig.7 p.9). Table 1 p.7 also has fixed-p8 BoolQ 57.2→53.3 despite improved average accuracy. Training FLOPs rise 1.41–1.74×; trunk persistent KV is not complete serving memory and no latency was measured.
- Cross-lingual Table 2 p.7 verifies Arabic 0.9→12.6% and Russian 1.9→23.3% CLeq; the abstract's 12.6% maximum does not encompass that Russian value. Table D.2 p.26 displays a higher-fit but identification-questioned nonlinear estimate 0.15→0.49% for the same 360M Arabic comparison, compared with linear 0.9→12.6%. Table G.2 p.31 shows 29.9% vs 22.6% token increases (Arabic vs Russian); its caption's Russian-larger wording can refer to the absolute 269 vs 212 added tokens, not the percentage. Semantic word mapping uses additional model-generated dictionary supervision and token/byte exposure budgets differ.
- GlitchPatch v1 Figures 3–5 and 7 and Tables 1–4 show path-specific behavioral selection and global-merge collateral harm; full-vocabulary zero regression refers to initially normal token tests, not safety for all mixed contexts. Its own F.2 distinguishes applied rules that fail final testing from unchanged unrepaired cases. Offline search, calibration, actual normalization, token growth and measured-workload limits remain material.
- Four official submission bodies remain blocked. V02 and both title-associated arXiv works have official active-submission API snapshots independently checked in [source audit](../../05_review/ICLR2027_SOURCE_AUDIT.md); V14/V22/V25 use the prior A08 official API snapshot only. Note v2 is not a PDF revision; no ICLR acceptance or arXiv/forum PDF equivalence is established. Anonymity retained.

## Access and follow-up

[ACCESS_DIAGNOSTIC](ACCESS_DIAGNOSTIC.md) and [STAGING_MANIFEST](STAGING_MANIFEST.md) record exact URLs, retry outcomes, certificate constraints, files/hashes and source editions. Three arXiv PDFs are now fully staged with ordinary verified TLS. The institutional PSR site returned Schannel `CRYPT_E_REVOCATION_OFFLINE`, never disabled; a distinct NeurIPS 2001 proceedings PDF route timed out twice. Earlier FetchURL provided institutional full text; neither a local institutional PDF nor NeurIPS full edition was acquired. Original figures and any edition equivalence remain follow-up. The four OpenReview challenges were not solved or bypassed; body gaps cannot be resolved using abstracts.

To settle remaining claims, legitimately acquire the blocked originals and audit their precise state/precision, information exposure and compute, routing windows/repair budgets, predictive-rank task generators, and vision receiver×source×adapter controls. Do not infer field exhaustion or a target-host cause. No training, installs, foreign code, source-registry edits, shared table edits or commits were used.
