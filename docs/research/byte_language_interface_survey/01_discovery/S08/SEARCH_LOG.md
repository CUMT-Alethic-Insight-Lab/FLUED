# S08 — Search and provenance log

2026-11-08. Public mechanism queries only. No internal documents uploaded. Only this assigned S08 directory was written. No other seven concurrent discovery streams were read. No production edits, installation, training, subagents, commits or paid resources.

## Deliverable accounting

- **34 work entities / 60 granular inventory records** (one record deliberately pairs two distinct evaluation studies while preserving their separate conditions).
- **16 catalog reuses + 2 scope-recovery reuses absent from catalog + 16 new discoveries relative to the inspected old catalog and recovery material =34.** Thus18 are catalog additions if catalog owner admits them, but only16 are genuinely new relative to both prior resources.
- **12 actual old FULL cards reused; 8 selected primary-text PARTIAL inspections; 14 abstract/metadata inspections; 0 newly completed FULL reads.** No source PDF fetch, abstract, or old card reread is counted as a fresh FULL reading.
- **6 successful Scholar search calls**, after invoking the required datasource skill and reading current scholar API documentation; **1 successful Bing browser search**,2attempted subsequent browser searches failed with TAB_NOT_ACTIVE. Browser control was shared across concurrent agents, so no repeated control-stealing loop was attempted. Scholarly searches supplied the remaining targeted discovery.
- **38 FetchURL calls:**35returned source content,1networkfailure,1HTTP404,1successfullyfetchedbutwrongidentityexcluded. This counts repeated abstract/PDF/version inspections separately as calls, not papers. One wrong-identity query was explicitly rejected rather than used.
- Six CSVs are retained as search-provenance artifacts, not temporary build output. No PDFs or conversion intermediates were created locally. FetchURL automatically stored one oversized tool result in the session's tool-results store; that was not a researcher-created temporary file and was used only for selected paginated reading.

## Local reuse and deduplication

Inputs actually inspected:

1. New survey `PLAN.md` in full; old `02_catalog/CATALOG.md` header/initial records plus targeted identifier/title/author searches across the complete file. No claim of human full-catalog semantic audit.
2. Old recovery `07_BYTE_SURVEY/COVERAGE_AUDIT.md`, `READING_RECOMMENDATIONS.md`, and relevant search-log matches; `08_GLOBAL_SCOPE/COVERAGE_AUDIT.md` for independent-scope and sample-count context. These are **old** recovery material, not another new stream.
3. Twelve actual FULL cards: `B05/W0007.md`, `B05/W0009.md`, `B05/W0011.md`, `B08/W0351.md`, `B14/W0352.md`, `B14/W0356.md`, `B08/W0360.md`, `B14/W0361.md`, `B08/W0363.md`, `B22/W0509.md`, `B22/W0516.md`, `B22/W0518.md`. All read through their returned ends, not merely card titles.
4. Relevant `docs/TERMS.md` instructions; no project terminology or global state was edited. Domain taxonomy uses established literature terms with explicit local definitions.

Dedup queries included stable IDs plus titles/authors: `2604.27263`, `1509.01626`, `1508.06615`, `1308.0850`, `1704.01444`, `1808.04444`, `2021.emnlp-main.161`, `2406.16829`, `2025.acl-long.1374`, `2025.emnlp-main.1224`, `2011.04006`, `2107.06499`, `BPE-Dropout`, `Generating Text`, `Character-Aware`, `Unpacking Tokenization`, `Tokenization Is More Than Compression`, `Exact Byte-Level`. Searches against recovery material specifically found Al-Rfou and Cao/Rimell already discovered as recoveryN06/N08; both are reuse. A follow-up search of old reading cards for the probability/control titles found no overlooked existing cards.

Catalogreuses:W0001,W0002,W0007,W0009,W0011,W0351,W0352,W0353,W0356,W0360,W0361,W0363,W0509,W0515,W0516,W0518. Counts derive from the selected register, not claimed exhaustive field coverage.

## Searches: exact queries, platforms, provenance, disposition

| Search | Platform / exact query and filters | Relevant returned result / disposition |
|---|---|---|
| Q01 | Built-in desktop browser, Bing: `tokenization language models characters subwords negative results fair comparison byte level likelihood marginal tokenization` | Rendered result identified **2604.27263**, *Decoupling the Benefits…*. Verified arXivabs,v2HTMLandAtom, admitted S08-W13. Broad tutorial result excluded. Browser tab created for research stayed hidden. |
| Q02 | Browser attempted: `character language modeling tokenization benefits leakage evaluation word boundaries marginal likelihood 2024 2025` | Failed TAB_NOT_ACTIVE; not executed search evidence, no result counted. |
| Q03 | Browser attempted: `"Tokenization is More Than Compression" "Token Healing" likelihood` | Failed TAB_NOT_ACTIVE after another agent took control; stopped further browser-search attempts. Not a successful query. |
| Q04 | ScholarAPI: `tokenization benefits language models`;2023–2026,num_results12,hl=en | Returned Goldman2024, BPE/tokenizer design studies, SpaceByte(reuse), BrokenTokenslead, arithmetic and regional studies. VerifiedGoldmanandSchmidtthroughformalpages. Excluded generictokenizationexplainer, unverifiedmegaChineseclaim, and low-value scope expansion. Saved `scholar_tokenization.csv`. |
| Q05 | ScholarAPI: `tokenization likelihood bias evaluation`;2021–2026,num_results8,hl=en | Returned Cao/Rimell(recoveryreuse),Phan2024,Lesci2025,dialectstudy. Verifiedprimarysources. Socialbiaspaperexcludedfromthismechanismscope; cross-tokenizerdistillationreservedforneighborstreamratherthanaddunreadrows. Saved `scholar_likelihood.csv`. |
| Q06 | ScholarAPI: `character language modeling recurrent networks`;2011–2018,num_results7,hl=en | ReturnedSutskever2011,Kim2016,Karpathy2015,Miyamoto/Cho2016,Hwang/Sung2017,Mikolov2012. Followedfirsttwoandtheirprimaryreferencechain; noassertionallreturnedworksreadoradmitted. Saved `scholar_history.csv`. |
| Q07 | ScholarAPI: `language models tokenization prefix bias`;2023–2026,num_results7,hl=en | ReturnedPhan2024,Lesci2025,ExactByte2025andBrokenTokenslead. FollowedExactByteformalabstract; rejectedunverifiedwebclaims. Saved `scholar_prefix.csv`. |
| Q08 | ScholarAPI: `Exact Byte-Level Probabilities Tokenized Language Models`;num_results4,hl=en | VerifiedformalICLR2025identitybutreturnednoarXivlink;calledformalPDFwhichfailednetworkonce. Saved `scholar_exact_identity.csv`. |
| Q09 | ScholarAPI: `"Exact Byte-Level Probabilities" arxiv`;num_results5,hl=en | Citationchainidentified**2410.09303**;absverifiedexactabstract/versionhistory. AlsofoundHayase2506.14123andICLR2026cross-tokenizerscoring;bothverifiedabstractsasreserveleads,not34workinventory. Saved `scholar_exact_arxiv.csv`. |

Scholar metadata sometimes labels NeurIPS2025 proceedings as2026. No year/title or claim is adopted from it when a primary source contradicts it. Citations counts were not used as evidence grades.

## FetchURL verification ledger

Location depth is conservative: “selected” means the locations in WORKS/INVENTORY, not every byte returned. A long extraction can contain uninspected appendix material. Source counts are API-call counts, not full readings.

| Fetch | Exact URL | Outcome / actually used |
|---|---|---|
| F01 | https://arxiv.org/abs/2604.27263 | Abstract andv1/v2history; newcounterexampleidentity |
| F02 | https://aclanthology.org/2021.emnlp-main.161/ | Formalabstract; recoveryreuse |
| F03 | https://arxiv.org/abs/1509.01626 | Classifieridentity/versionhistory; nonLMboundary |
| F04 | https://arxiv.org/abs/1508.06615 | Characterinput/**wordoutput**explicitinabstract |
| F05 | https://arxiv.org/html/2604.27263v2 | Selected§§4–8andfigureprose; tables/curvesnothuman-audited |
| F06 | https://aclanthology.org/2024.findings-acl.134/ | Goldmanformalabstract/authors/pages |
| F07 | https://aclanthology.org/2025.acl-long.1546/ | Lotzformalabstract; existingW0515,notnew |
| F08 | https://arxiv.org/abs/2402.19155 | bGPTabstract; CPU/ABC–MIDIfiguresnotLMsuccess |
| F09 | https://arxiv.org/abs/1808.04444 | Historicaldirectmodelabstract/versionhistory |
| F10 | https://aclanthology.org/2024.emnlp-main.40/ | Schmidtformalidentity/abstract,PathPiececounterexample |
| F11 | https://arxiv.org/abs/1308.0850 | Gravesidentity/versionhistory; handwriting≠textmetric |
| F12 | https://arxiv.org/abs/1704.01444 | Byte-recurrentrepresentation/transferabstract |
| F13 | https://aclanthology.org/2020.findings-emnlp.414/ | Bostrom/Durrettformalabstract;unigramvsBPE |
| F14 | https://arxiv.org/abs/2406.16829 | Phan2024abstract/versionhistory |
| F15 | https://aclanthology.org/2025.acl-long.1374/ | Lesciformalidentity/abstract |
| F16 | https://aclanthology.org/2025.emnlp-main.1224/ | Dialectstudyformalabstract |
| F17 | https://aclanthology.org/2020.acl-main.170/ | BPE-Dropoutformalabstract |
| F18 | https://arxiv.org/abs/2011.04006 | LRAabstract/versionhistory |
| F19 | https://arxiv.org/abs/2107.06499 | Dedupabstract/versionhistory |
| F20 | https://www.cs.toronto.edu/~jmartens/docs/RNN_Language.pdf | Sutskever2011selected§§1,3.2–5.4,7;Table1cellsnotinspected |
| F21 | https://arxiv.org/html/2011.04006v1 | LRAselectedtasks/desiderata/profilingandAppendixsettings;notFULL |
| F22 | https://proceedings.iclr.cc/paper_files/paper/2025/hash/5ed5c3c846f684a54975ad7a2525199f-Abstract-Conference.html | ExactByteformalabstract;proofs/costunknown |
| F23 | https://arxiv.org/html/2406.16829v2 | Oversizedresult; paginatedReadfirst145linesused§§1–2/§3openingonly;remainingtextnotFULL |
| F24 | https://aclanthology.org/2016.acl-long.14/ | HTTP404; incorrectformal-stylealiasforSennrich,notaccessdenial; correctedviaP16-1162 |
| F25 | https://aclanthology.org/P18-1007/ | Kudoformalabstract |
| F26 | https://export.arxiv.org/api/query?id_list=2604.27263,2406.16829,1808.04444,1704.01444 | Atomtitle/authors/versionlock;restoredfirstauthorsmissingfromHTML |
| F27 | https://aclanthology.org/P16-1162/ | Sennrichformalmetadata;pageawardnarrativenotusedaseffectevidence |
| F28 | https://aclanthology.org/2021.emnlp-main.161.pdf | SelectedCao/Rimell§§2–4.4,6;missingnumericaltablecellsandcompletevisualaudit |
| F29 | https://arxiv.org/abs/1508.07909v5 | Originaltranslationabstractandv5history;subwordsnotbytes |
| F30 | https://arxiv.org/abs/2107.06499v2 | Locksdedupv2;noversion-bodycomparison |
| F31 | https://aclanthology.org/2025.acl-long.1374.pdf | Selectedcausal-estimation§§2–6/limitations/footnotes;Appendixproofsandplotsnotfullyread |
| F32 | https://arxiv.org/html/1808.04444v2 | Directmodelunits,training/evaluation,auxiliarylosses,LM1Bgap;tablenumericcellsmissing |
| F33 | https://arxiv.org/abs/2410.23430 | **Wrongidentity:** neutral-atomquantumreport. Rejectedimmediately;neitherworknorclaimcounted;correct2410.09303foundthroughQ09 |
| F34 | https://aclanthology.org/2025.emnlp-main.1224.pdf | Selectedtitle/authors,§§3–5.2/limitations;notappendices/tables;dialectidentificationparitysignreversal,LoRAvsfullfinetune,§5.3displayglyphinterpretationneedsrecheck |
| F35 | https://proceedings.iclr.cc/paper_files/paper/2025/file/5ed5c3c846f684a54975ad7a2525199f-Paper-Conference.pdf | Networkfetchfailureonce;noauthwallor404inferred;legitimatearXivversionlocatedinstead |
| F36 | https://arxiv.org/abs/2410.09303 | ExactBytev1/v2history,identicalformalabstract;arXivv2=2025-04-11 |
| F37 | https://arxiv.org/abs/2506.14123 | Hayaseetalv1–v3history/abstract;reserveleadnotinventorycount |
| F38 | https://proceedings.iclr.cc/paper_files/paper/2026/hash/40d50fe20d5e6922dbb52d7da6de03f1-Abstract-Conference.html | Cross-tokenizerscoringabstract;reserveleadnotinventorycount |

## Exclusions and source-critical observations

- Direct positive byte evidence retained: recurrent byte representation learning, direct byte Transformer, selected modern fixed-state/hierarchical results. The counterexample remit is not a negative-only inclusion filter.
- Character-input/word-output Kim model, characterCNNclassifier, LRAencoder/pixel tasks, bGPTbinary conversion/CPU accuracy, and single-slot candidateembeddingretrieval are **not mislabeled as causal byte-language generation**. They remain useful task/representation evidence with distinct output units.
- Three different “tokenization bias” meanings remain separate: (i) canonicalpathversustextmarginal;(ii) text-prefixversustoken-prefixconditioning;(iii) locallearnedvocabulary-inclusioneffect. Treating them as synonyms would erase each paper's actual problem.
- Declared source text limitations remain: arXivHTMLcanomitfirstauthors, duplicate numbers (“44”for4), and empty table cells. Atom/formalpagesrepairidentity; tables/figureswaitforfullreader. No visual numeric reconstruction was invented.
- Dialectpaper§5.3 discusses Latin-like renderings of byte-BPEsymbols as misinterpreted characters; that observation **alone** is not proof an invertible byte tokenizer loses Unicode or fails semantically. Preserve its empirical task correlations while requesting encoding-level verification for that interpretation.
- Browserreportedmanyotheropenresearchtabs. OnlytheS08-createdtabiseligibleforcleanup; nootheragent/userwindowwasclosed. Sharedbrowseractivationerrorsareloggedratherthanreroutedthroughunapprovedexternalbrowsers.

## Verification plan/results

Local checks count work/recordIDs and grades, resolve Markdownrelativefilelinks, checkUTF-8andwhitespace, and comparegitstatus. No code/tests/trainingareappropriateforaliteratureinventory. SearchCSVsaretaskdeliverables; no temporarytrainingorbuildfilescreated. Final validationresultsareappendedbelowafterexecution.

### Executed validation

- Python standard-library assertions **PASS**:34workrows;60unique,sequentialR001–R060records;16catalog/2recovery/16new;R/P/A=12/8/14;allMarkdownrelativefilelinksexist;noUTF-8replacementcharactersortrailingwhitespace.
- `git diff --check` **PASS**. `git status --short` retains the initial top-level untracked survey roots, proposal and bundles; no tracked source/document edits. Because the survey root was already untracked, this check is not evidence of exclusive ownership inside it; all actual writes in this stream targeted S08 explicitly.
- Assigned directory contains the4requestedMarkdownfilesand6provenanceCSVs,~107KBMarkdown. No test/build/trainingoutputwascreated; noirrelevanttemporaryfilecleanupneeded.
- Attempt to close this stream's own browser research tab failed TAB_NOT_ACTIVE after shared control changed. Left that single hidden tab open rather than competing for control; no other tabs were touched. Browser already had more than ten tabs and reported sidebar crowding; user-facing navigation was not requested or opened by this stream.
