# Independent byte-level language-interface survey

## User contract

Deliver an independent, field-centered survey, not a FLUED proposal review. Build a very detailed inventory of problems encountered by prior work, one-sentence solution ideas, and the other AI methods/techniques used. Classify and group the inventory before composing the survey. English working reports and long English survey are authorized. A separate sol agent must translate the final English deliverables into Chinese, reducing repetitive defensive prose without deleting material conditions or uncertainty. Main agent coordinates rather than writing the scholarly synthesis.

The previous full follow-up list is preserved in ../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md. Only byte-interface survey work is activated here; other directions are not implicitly authorized experiments.

## Staffing and boundaries

- At most 10 concurrent agents; normal batches 8.
- Discovery, inventory, clustering, synthesis: nvtokens/gpt-6.1-sol.
- Selected-paper full reading: nvtokens/gpt-6.1-terra.
- Independent red team: separate sol authors from synthesis.
- Final Chinese translation: a separate sol translator, not the English author.
- Reuse agents for follow-ups. Tool/network transient errors may be retried 1–2 times; do not bypass denied access or authentication walls. Alternative legitimate author/open versions are permitted.
- Detailed work goes to Markdown; final agent replies <=250 Chinese characters or ~150 English words, stating files/counts/gaps/recommendations.
- No training, production edits, installs, paid resources, git commits or pushes. Never upload internal documents to external services. Public mechanism search terms only.
- Downloads/conversion intermediates must use explicit paths within the assigned project directory, not Downloads or /tmp. Prefer public HTTP fetch/download and paginated reads over competing browser control. Check tool availability before relying on it.
- Existing corpus is reusable, not presumed adequate: ../flued_multigranularity_survey_20261108/02_catalog/ and 03_reading/. Preserve stable W IDs when citing old works; do not alter old evidence cards or inflate fresh-reading counts.

## Scope

Separate byte, Unicode code point, grapheme, character, subword and mixed interfaces. Record input/internal/output/supervision units. Cover historical character work as explicitly labeled antecedents, not as byte-model evidence. Main axes:
1. Representation/encoding and historical routes.
2. Compression, differentiable grouping and boundary learning.
3. Causal generation, decoders, multi-byte/chunk prediction.
4. Weight sharing, interface geometry and optimization.
5. Multilinguality, UTF-8, robustness and evaluation.
6. Computational scaling, training and serving costs.
7. Hybrid interfaces, objectives, distillation and adaptation.
8. Field coverage, independent counterexamples and methodology.

FLUED implications form a final bounded section, not the survey's organizing purpose. Multigranularity/source revisiting is one relevant mechanism, not the governing frame.

## Directory ownership

00_scope/: coordinator's contract and scope records.
01_discovery/S01..S08/: individual sol discovery and inventory fragments.
02_inventory/: single catalog owner; canonical works, detailed problem-solution-technique records, stable row IDs, classification, reading queues.
03_reading/<batch>/: terra cards and batch reports; previously read work links are explicitly reused.
04_synthesis/: English thematic drafts and final survey, technical inventory, classification narrative, reading guide.
05_review/: independent source/coverage/rigor reviews and closure.
06_translation/: independent complete Chinese translations and terminology mapping.
COORDINATION.md: coordinator's batch/agent handoff record.

## Inventory record schema

Record ID; work title/stable URL/version; publication era and family; actual language unit; specific problem (one claim/row, not one paper/row); one-sentence solution; borrowed AI techniques and exact roles (CNN, latent pooling, state space, distillation, auxiliary losses, etc.; distinguish explicitly used from analyst analogy); learning signal and optimization; input/internal/output/supervision units; causality; evidence/ablation/comparator; result and applicable budget; remaining failure; source location; reading depth; potential mechanism cluster. Unknown fields remain unknown. The user means techniques used by prior researchers, not the assistant tools we use.

Do not split synonymous problems just to inflate rows. One work may support multiple genuinely distinct records. Track independent works and inventory rows separately. Positive results and failed approaches both enter.

## Evidence and synthesis standards

- Real searches with logs: exact query, platform, result provenance, exclusions, retry outcome.
- Verify identity and source. Abstract-only is not full reading; fetching/downloading does not mean reading. PARTIAL must name missing sections.
- Selected full readings include method, experiments, key figures/tables, relevant appendix; text extraction truncation must be followed with pagination. Code reproduction is separate from reading completion.
- Key claims cite version and section/page/table, with stable source/card paths. Do not infer weight tying from model family or a single unrelated config. Keep the distinct sharing axes explicit.
- Compare original text exposure, original-text context, computation, parameter count, output units, auxiliary teachers, and inference costs separately. Conversion to bits per byte requires valid probability/accounting conditions.
- Clustering is evidence-informed thematic grouping with explicit dimensions and multi-label assignments. Do not call it algorithmic embedding clustering unless actually performed and documented; do not add embedding service dependencies.
- Clear positive prose, tables and substantive comparison. Put a condition once next to the affected conclusion, not repetitive safety/disclaimer paragraphs.
- No arbitrary final length cap; enough detail for a serious long survey. Full Chinese translation must preserve structure, numbers, citations and technical meaning; cannot replace with summary.

## Workflow and finish line

A Eight sol discovery/inventory workstreams, using existing cards plus targeted online searches.
B Single-owner de-duplication, granular inventory and thematic taxonomy; independent coverage audit; prioritize missing full reads.
C Terra full readings in small non-overlapping batches, with appropriate retries; sol discovery follow-ups if needed.
D Sol syntheses and final English long survey + detailed inventory + classification guide.
E Separate sol red teams assess field coverage, evidence/units/budgets, and inventory fidelity; revise before translation.
F Independent sol translator produces full Chinese survey and detailed inventory/classification materials. Separate bilingual check verifies fidelity and prose. Correct discrepancies.
G Deliver navigable files, real counts and unresolved items. Do not declare original broader FLUED report repaired by finishing this survey.
