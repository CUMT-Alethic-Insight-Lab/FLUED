# V12 — task-correct evidence and intervention countercontrols

## Coverage and accounting

Seven assigned distinct works: **7 FULL / 0 PARTIAL / 0 BLOCKED body**. N11 alone was recovered and read in this continuation; the other six FULL originals were not reread. FULL means the cited paper body and relevant printed appendices read, including carrying visual checks below; it does not mean independent reproduction, proof verification, source-code execution, or all figures pixel-inspected. No works were counted twice for venue/preprint versions. V05's separately owned cards are conceptual cross-references, not newly read or credited here. No new OpenReview anonymous body or ICLR 2027 venue decision is asserted.

| ID | Read edition and status | Relevant evidence locations / gaps |
|---|---|---|
| [BR-A04-R04](BR-A04-R04.md) | **FULL** ACL 2020 formal | §§3–6, Apps.A–C; PDF p.8 Tables 3–4 visually checked. |
| [W0373](W0373.md) | **FULL** TACL 2023 formal | §§3–7, Apps.B–C including backdoor proof and transformation algorithm; PDF pp.9,11–12 Figs.4–5,7–8 visually checked. Imperfect generated examples. |
| [W0370](W0370.md) | **FULL** EMNLP 2020 formal | §§2–4, Apps.A–B; PDF p.6 Table 1/Fig.2 visually checked. Probe is supervised and external. |
| [BR-A04-N07](BR-A04-N07.md) | **FULL** arXiv 2410.03727v3 | §§3–5, Apps.A–G incl. generation prompts; PDF pp.6–7,9 Figs.4–6,9 and Table 1 visually checked. Whole-response entailment not measured by answer mention. |
| [BR-A04-N08](BR-A04-N08.md) | **FULL** arXiv 2404.10198v3 | §§3–5, App.A; PDF pp.6,9,15 Tables 2–3,6–7 visually checked. Complete prompt strings and exact response classification code are external and not inspected; ambiguity remains between §3.1/Table 2 conditional figures and Table 4 bias denominators. |
| [BR-A04-N09](BR-A04-N09.md) | **FULL** arXiv 2211.00593v1 | §§2–4, Apps.A–M; PDF pp.10–11,24 Figs.6–7,20 visually checked. Fig.20 head-class labels appear shifted, and independently held-out selection/evaluation is not established. |
| [BR-A04-N11](BR-A04-N11.md) | **FULL** arXiv 2410.13032v1 | §§2–5, Apps.A–F; PDF pp.5–9,15,17,21–22 visually checked. Non-rejection does not establish ideal properties; original v1 contains Table 1 vs App.E interpretation conflicts, Type II error not studied, and synthetic controls do not establish nonlinear-redundancy sensitivity. |

## Synthesis boundaries

- Rationale removal, trained probes and internal hybrid patching are distinct experimental permissions. None automatically certifies native deployed content use, semantic correctness, preserved content, or a target-host mechanism.
- FaithEval makes a world-false context authoritative for a stipulated QA task; ClashEval separately treats incorrect source text as a hazard. These are different authority contracts, not contradictory scores. Both need full-response adjudication and both correct-prior/wrong-source and wrong-prior/correct-source controls.
- IOI's individual null and backup heads, group ablations and greedy counterexample demonstrate why weak single-node nulls do not imply full-path irrelevance, but do not prove every memory is blind or that any particular byte interface is exonerated.
- No-source-revisit options are native readout or query adaptation, in-state content retention/interference reform, appropriate learning objectives and conflict/abstention training; evaluate them with legal task-semantic counterfactuals, matched controls, host visibility and complete budgets. V12 is primarily an assay packet, not an architecture verdict.
- Elsewhere in the project, the independently audited RAM ledger is nominal 500M, but its five displayed rows sum to **500.040M**, not exactly 500.000M; it is not a V12 source or new credit.

## Source receipt and visual coverage

Seven acquired PDF originals are retained as `sources/<ID>.pdf` with `pdftotext -layout -enc UTF-8` derived `sources/<ID>.txt`. Curl used `--location --fail`, HTTPS-only protocols, standard Schannel certificate checks, direct defaults (`proxy_used=0`), no trust/proxy/system modification. Initial ACL downloads and N09 completed HTTP 200, curl 0, TLS verify 0; initial N07/N11 connection timeouts and N08 partial transfer timeout; an ordinary retry produced successful N07 and N08, while N11 still timed out after 12,402/716,352 bytes. A subsequent separately authorized N11-only exact-v1 request with 240-second maximum completed HTTP 200, curl 0, TLS verify 0, proxy 0. All seven successful files passed PDF signature/EOF and parser checks; no failed `.part` retained. Formal ACL PDFs were the requested proceedings editions; arXiv suffixes pin requested versions, not equivalence to proceedings.

Before the N11 recovery, project-research/workspace title and arXiv-ID searches found abstract-only references and the prior official-v1 HTML/PDF routes, not a saved body. A browser exact-title+ID search yielded generic irrelevant hits rather than a validated author-hosted same-version mirror. No other source was substituted.

| ID | Saved PDF bytes | SHA-256 |
|---|---:|---|
| BR-A04-R04 | 722810 | `1fe914b02b96e035408c4bc4c457bc3b48caf444e244fe8d93b373b4540b1765` |
| W0373 | 839848 | `18d931c0233ed89b58ab63ad82d862f5550be7648146216a1d6c635bbdb0b024` |
| W0370 | 1241111 | `cdcefa7c73130ff4c9692d7acc56ff09034d4a7da409175ce351e7d68bbd1d03` |
| BR-A04-N07 | 11915946 | `0738965cff0e1e4372362aa06d2597a94e6169a420e4481fc8d2ac13aeb62e65` |
| BR-A04-N08 | 2088151 | `31754304778701a022300f2cbc9864b2e6b4a1c2a17861bdfd803cd99a7cd063` |
| BR-A04-N09 | 1342518 | `af0ea3ca3912f819d2cd06b0f36f5c20bfcab72fbc83816d830c286af6872c91` |
| BR-A04-N11 | 716352 | `83c1d70aaa744acdf3eed4ef25ffee8ee91028e4e2b45eff87c9567536248854` |

Existing PyMuPDF rendered cited PDF pages to `sources/<ID>__p<page>.png`; those images were read directly, remain with the evidence, and are not independent result reproductions. All source text was paginated through its end. The official source and full printed paper distinguish supported findings from external artifact omissions. N08's external prompt/matcher implementation remains uninspected, as disclosed; it is not an unread part of its paper. N11's v1 source contradictions, selection/evaluation separation and uncalibrated nonlinear-redundancy sensitivity remain explicit gaps; independent code/proof inspection was not performed. No paywalled source, author-identity crosswalk, authentication or TLS/revocation bypass used.
