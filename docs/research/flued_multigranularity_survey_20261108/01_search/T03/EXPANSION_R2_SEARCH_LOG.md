# T03 R2 实际检索与访问日志

日期：2026-11-08。范围仅来源生命周期、原文驻留/外置/重算/淘汰、派生失效、物化视图与存储层次；另补草案点名 HMT，并核销本专题 H-MEM 作者。入口要求见[覆盖审计](../../05_review/COVERAGE_AUDIT_R1.md)。本轮未使用学术数据源/用户登录浏览器，均为 WebSearch + FetchURL 公开来源。

## 实计与范围

- **40 次 WebSearch：39 次返回，1 次服务 HTTP 404。49 次 FetchURL：40 次可用，4 次 HTTP 失败，4 次返回内容不足（含乱码/后端错误/无摘要），1 次 ID 猜测误取无关作品而排除。**不把成功 HTTP 等同有效核验。
- 40 次可用 Fetch 对应：29 个核验作品的摘要/官方介绍及补充元数据共37次，另有 H-MEM 既有作品的摘要/方法/BibTeX 3次。没有把元数据多入口或版本重复计作品。
- **29个核验作品＝28个目录外新增确认候选＋1个HMT补核**（R2-001—029）。起始目录384实体；收尾目录已并发录入HMT为W0385，故001只补v3/正式版，不重复新增。002—029经当前385实体及八专题候选定向去重无重录；T04 R2日志HMT查询不计实体。最终归并仍归目录所有者，**未改总表、未自行分配 W-ID、未宣布全库数量增加29**。
- 深度：29作全部有原始摘要或官方简介；HMT另定向读 v3 §3.2—3.3，非精读。H-MEM定向读§3.1—3.3；经典 PDF 仅摘要/开头，未因全文返回计精读。**本代理 R2 全文精读0、代码核验0、复现0。**
- 只写 T03：`EXPANSION_R2.md`、本日志；原地修 `CANDIDATES.md` 的 T03-005；首轮日志保持历史不重算。

## 实际查询（不是建议查询）

所有平台 WebSearch；日期均2026-11-08。中文查询2条（Q10、Q38）；不据此称中文覆盖充分。

| # | 实际查询 | 返回与取舍 |
|---|---|---|
| Q01 | `data provenance semirings incremental view maintenance deletion DRed Counting Gupta Mumick 1993` | IVM、DBSP、来源半环与新近清理线索；优先原作 |
| Q02 | `bitemporal database valid time transaction time Jensen Snodgrass temporal databases 1999` | 双时间综述、Language-Integrated Query 入口 |
| Q03 | `"Provenance Semirings" Green Karvounarakis Tannen 2007` | DOI、作者公开稿线索；不采新博客为证明 |
| Q04 | `"Maintaining views incrementally" 1993 abstract` | 1993原作与作者库入口；二手作者误标剔除 |
| Q05 | `"On the Propagation of Deletions and Annotations" provenance 2002` | 只发现引文，未取得原始摘要，本轮不确认 |
| Q06 | `"Why and Where" "provenance" Buneman 2001` | ICDT DOI入口 |
| Q07 | `"Tracing the lineage of view data" Widom abstract` | Stanford主库/正式历史页/作者稿；访问不足，不确认 |
| Q08 | `"DBToaster" "higher-order delta"` | 2012初版、2014扩展作者稿；仅记一个扩展作品簇 |
| Q09 | `"Differential Dataflow" 2013 paper` | CIDR/MS Research原作入口 |
| Q10 | `"来源追溯" "增量视图维护" 数据` | 软件学报正式中文原刊；其余博客排除 |
| Q11 | `"Provenance semirings" site:repository.upenn.edu` | **服务HTTP404**，不是作品不存在；未同式循环重试 |
| Q12 | `"Provenance semirings" "Abstract" Green` | 原作者UC Davis公开PDF可取 |
| Q13 | `"Maintaining views incrementally" "sigmod.org"` | 精确DOI、DRed/Counting后续 |
| Q14 | `"DBToaster" site:dbtoaster.org` | 官方项目介绍只作入口；本轮确认用作者论文摘要 |
| Q15 | `"Temporal Data Management" Jensen Snodgrass abstract 1999` | 10.1109/69.755613及作者PDF |
| Q16 | `"Temporal features in SQL:2011" sigmod record` | 官方页只返作者和PDF链接，不足摘要；不计候选 |
| Q17 | `"Self-adjusting computation" Acar 2009 abstract` | Self-Adjusting Stack Machines原作；不凭记忆填2009概要 |
| Q18 | `"ARIES" "research.ibm.com"` | 无充分原始摘要，超出当前最紧范围，未确认 |
| Q19 | `"The log-structured merge-tree" abstract O Neil 1996` | 正式DOI后续核验仅返参考文献；未计确认 |
| Q20 | `"Lethe" "deletion" SIGMOD 2020` | 与2023扩展线索；不把两者分别加数 |
| Q21 | `"DelF" "Safeguarding deletion correctness"` | USENIX正式摘要与开源全文 |
| Q22 | `"DynaMat" "view" 1999` | 扩展稿 A Case for Dynamic View Management；与1999前身关联 |
| Q23 | `"The five-minute rule" "working set model" memory` | 初查询有大量同名生活建议噪声，改精确研究入口 |
| Q24 | `"LSM-tree" "10.1007" 1996` | s002360050048原始DOI |
| Q25 | `"Lethe: A Tunable Delete-Aware LSM Engine" arxiv` | 2006.04777、作者官方系统入口 |
| Q26 | `"The Working Set Model for Program Behavior" Denning pdf` | Denning原作者公开稿 |
| Q27 | `"The Five-Minute Rule" "microsoft.com/en-us/research"` | 1997官方摘要；不搬用当年的五分钟常数 |
| Q28 | `"Pensieve" "CacheGen" "Mooncake" KV paper` | CacheGen号与多层缓存谱系 |
| Q29 | `"Pensieve: Stateful" "Serving" LLM` | 2312.05516最新至v3 |
| Q30 | `"FlexGen" "LLM in a Flash" arxiv` | 2303.06865、2312.11514 |
| Q31 | `"Mooncake" "2407.00079"` | FAST/系统与LMCache线索；最终读原始摘要 |
| Q32 | `"HiFC" "Flash-based" KV` | NeurIPS2025官方论文页；不按搜索2026日期改会年 |
| Q33 | `"Resilient Distributed Datasets" "usenix"` | NSDI2012原始摘要与BibTeX |
| Q34 | `"WiscKey" "usenix"` | FAST2016原始摘要；2017扩展不另计 |
| Q35 | `"View maintenance in a warehousing environment" Zhuge` | DOI原站403，停止；只留待核验 |
| Q36 | `"HMT: Hierarchical Memory Transformer for Efficient" 2025 ACL` | **NAACL2025正式页，6位作者**；与v1五位不同 |
| Q37 | `"A Case for Dynamic View Management" Kotidis Roussopoulos 2001 2002` | 2001正式卷年；PDF路径TODS2002不是出版年份 |
| Q38 | `"面向区块链的高效物化视图维护和可信查询" 作者` | 原刊作者/2020卷年；二手误作33卷、金姓名OCR错误，未采用 |
| Q39 | `"Leases: An efficient fault-tolerant mechanism" Cheriton Gray` | 经典缓存一致性原文与DOI |
| Q40 | `"Language-Integrated Query for Temporal Data" authors` | extended version标题后缀、GPCE2022与3位作者 |

## FetchURL 全台账

“可用”只表示列明用途足够；不表示全文读完。`R2-nnn` 对应扩展报告局部ID。来源URL就是实际请求，不伪装为查询结果自动浏览。

| F | 实际URL | 状态/用途 |
|---|---|---|
| 01 | https://arxiv.org/abs/2507.22925 | 可用；既有H-MEM摘要，作者栏被抽取器省略，不能据From字段填作者 |
| 02 | https://arxiv.org/html/2507.22925v1 | 可用；H-MEM方法§3.1—3.3与四层，不精读 |
| 03 | https://arxiv.org/abs/2405.06067 | 可用；HMT最新摘要，v1/v2/v3历史，R2-001 |
| 04 | https://arxiv.org/bibtex/2507.22925 | 可用；**Haoran Sun and Shaoning Zeng** 原始作者依据 |
| 05 | https://arxiv.org/bibtex/2405.06067 | 可用；最新题名与6位作者，R2-001补查 |
| 06 | https://sigmod.org/publications/discs/2001/out/p_tracingthelineayijej.htm | **HTTP404**；未核摘要 |
| 07 | https://arxiv.org/abs/2203.16684 | 可用；DBSP摘要，R2-007 |
| 08 | https://arxiv.org/abs/0708.2173 | 可用；dependency provenance摘要，R2-004 |
| 09 | https://arxiv.org/abs/2210.12077 | 可用；temporal LINQ摘要，R2-011 |
| 10 | https://doi.org/10.1145/1265530.1265535 | **HTTP403**；没有重试此受限入口；F13为搜索发现的原作者合法公开稿 |
| 11 | https://doi.org/10.1007/3-540-44503-X_20 | 可用；Springer原始摘要与作者，R2-002 |
| 12 | https://www.microsoft.com/en-us/research/publication/differential-dataflow/ | 可用；作者、CIDR2013与原始介绍，R2-008 |
| 13 | https://web.cs.ucdavis.edu/~green/papers/pods07.pdf | 可用文本；摘要/开头，R2-003；未阅读全文证明 |
| 14 | http://www1.cs.columbia.edu/~gravano/Qual/Papers/13%20-%20Maintaining%20Views%20Incrementally.pdf | 可用文本；摘要/开头Counting、DRed，R2-005 |
| 15 | https://www.cs.ox.ac.uk/files/9137/vldbj2014-dbtoaster-extended.pdf | 可用文本；扩展稿摘要/开头，R2-006 |
| 16 | https://people.cs.aau.dk/~csj/Papers/Files/1999_jensenIEEETKDE.pdf | 可用文本；摘要及§2时间定义定向阅读，R2-010 |
| 17 | https://sigmodrecord.org/2012/09/30/temporal-features-in-sql2011/ | **内容不足**；只有作者/PDF链接，不计确认 |
| 18 | http://ilpubs.stanford.edu/252/ | **页面后端错误** Failed to connect to database，不是论文正文 |
| 19 | http://ilpubs.stanford.edu/252/1/1997-3.pdf | **HTTP500**；有限合法替代来源后停止 |
| 20 | https://arxiv.org/abs/1711.03987 | 可用；Optimised Maintenance…摘要，R2-009 |
| 21 | https://arxiv.org/abs/1108.3265 | 可用；Self-Adjusting Stack Machines摘要，R2-012 |
| 22 | https://homes.cs.aau.dk/~tbp/BIT/moede23/lineage-full.pdf | **严重文字乱码**；无法核身份与摘要，不计确认，不凭搜索片段升级 |
| 23 | https://www.usenix.org/conference/usenixsecurity20/presentation/cohn-gordon | 可用；DELF作者与正式介绍，R2-013 |
| 24 | https://doi.org/10.1007/s002360050048 | **内容不足**；只有题名/参考文献，无摘要；LSM经典身份有线索但不计确认 |
| 25 | https://arxiv.org/abs/2504.10438 | 可用；delayed view semantics与Dynamic Tables摘要，R2-014 |
| 26 | https://arxiv.org/abs/2006.04777 | 可用；Lethe v4摘要/历史，R2-015 |
| 27 | https://www.microsoft.com/en-us/research/publication/the-five-minute-rule-ten-years-later/ | 可用；1997原作者官方摘要，R2-017 |
| 28 | http://denninginstitute.com/pjd/PUBS/WSModel_1968.pdf | 可用文本；working-set摘要/开头，R2-016 |
| 29 | https://arxiv.org/abs/2310.07240 | 可用；CacheGen v6摘要，R2-018 |
| 30 | https://arxiv.org/html/2405.06067v3 | 可用；HMT摘要与§3.2—3.3定向读取，不精读，R2-001 |
| 31 | https://arxiv.org/abs/2312.05516 | 可用；Pensieve摘要/至v3历史，R2-019 |
| 32 | https://arxiv.org/abs/2303.06865 | 可用；FlexGen作者/摘要，R2-020 |
| 33 | https://arxiv.org/abs/2312.11514 | 可用；LLM in a flash摘要，R2-021 |
| 34 | https://arxiv.org/abs/2407.00079 | 可用；Mooncake至v5历史/摘要，R2-022 |
| 35 | https://papers.neurips.cc/paper_files/paper/2025/hash/4431224d3762aa655f0aee4eaf04ff16-Abstract-Conference.html | 可用；HiFC正式摘要/DOI，R2-023 |
| 36 | https://arxiv.org/abs/2510.09665 | 可用；LMCache作者/摘要/至v2，R2-024 |
| 37 | https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia | 可用；RDD作者/摘要/BibTeX，R2-025 |
| 38 | https://www.usenix.org/conference/fast16/technical-sessions/presentation/lu | 可用；WiscKey作者/摘要/BibTeX，R2-026 |
| 39 | https://courses.cs.duke.edu/cps296.1/spring02/papers/KR-TODS2002.pdf | 可用但字符分词OCR不佳；题名/作者/摘要仍清楚：**A Case for Dynamic View Management**，R2-027；不是把文件名当题名/年份 |
| 40 | https://www.jos.org.cn/jos/article/html/5914?special_id=20250523142617001 | 可用；中文原刊摘要，R2-028；返回全文但不计精读 |
| 41 | https://aclanthology.org/2025.naacl-long.410/ | 可用；HMT正式版本作者/摘要/DOI，R2-001 |
| 42 | https://arxiv.org/bibtex/2203.16684 | 可用；DBSP完整作者/题名，R2-007 |
| 43 | https://arxiv.org/bibtex/1711.03987 | 可用；Datalog维护完整作者/确切题名，R2-009 |
| 44 | https://arxiv.org/bibtex/1108.3265 | 可用；Stack Machines作者，R2-012 |
| 45 | https://www.cs.cmu.edu/~15712/papers/gray89.pdf | 可用文本；Leases作者/摘要与§2定向阅读，R2-029 |
| 46 | https://www.jos.org.cn/jos/article/abstract/5914 | 可用；中文原刊作者顺序/正式年卷/摘要，R2-028 |
| 47 | https://doi.org/10.1145/223784.223848 | **HTTP403**；warehouse维护经典未取得摘要，不确认且不重试受限入口 |
| 48 | https://arxiv.org/abs/0704.3719 | **误猜标识，返回无关全息纠缠熵论文，排除**；不计来源维护候选。此请求不是Q01—Q40检索命中，不能当作有效发现。之后停止凭记忆猜编号 |
| 49 | https://arxiv.org/bibtex/0708.2173 | 可用；dependency provenance作者/题名，R2-004 |

## 未确认与未完成

1. `Tracing the lineage of view data in a warehousing environment`（2000）有准确标题/作者与DOI检索线索，但三个入口含404、500、乱码和后端失败，不计确认。下轮可由terra读公开PDF或由目录元数据人员追出版页；本轮不无限重试。
2. `View Maintenance in a Warehousing Environment`（1995）只有检索/原站403；`On Propagation of Deletions and Annotations Through Views`（2002）仅发现；ARIES仅发现。均不计数。
3. LSM-tree 1996、SQL:2011介绍只抓到元数据/参考文献，身份可追但摘要不足；不拿“经典常识”抵充核验。
4. 近窗Mooncake/LMCache更新已核，但未逐版读差异；HiFC按NeurIPS2025正式卷年记录，不采搜索结果2026网页日期。
5. 词法/正则全目录去重仅能避免稳定ID/题名明显重录，不能证明证据独立性；29作不代表29套互相独立实验。DynaMat前身/扩展、DBToaster2012/2014、HMT预印本/NAACL正式版均保守记一簇。
6. 抽取器省略首位作者、搜索日期错误、OCR错字均存在；作者不齐留空，精读须用原作者/出版页锁版本。所有强语义论断仍需terra原节证据、代码生命周期和真实成本复核。

## 本地交付校验与并发核销

只读Python结构校验最终 **PASS**：29张局部卡连续唯一，P1=20/P2=9；40个查询与49个Fetch请求连续；40可用/4HTTP/4不足/1无关可复算；每卡具身份、深度、全文入口与terra/下一步问题；UTF-8无替代字符、无行尾空白，相对链接存在；T03所有Markdown无首轮H-MEM旧错名。

校验期间发现两件事并已纠正口径：初版校验器仅接受PDF而未接受原刊HTML全文，导致028被误报，修校验规则后通过（不为通过测试添加虚假PDF）；随后稳定ID去重检查捕捉到主目录并发新增HMT为W0385，将“29新增”改为“28目录外新增＋HMT补核1”。最终当前385实体总目录的唯一重合是2405.06067；其他专题当前文本唯一匹配为T04 R2日志的HMT查询，没有新增实体重录。目录W0111已被其负责人并发修正作者/前缀；本代理没有回写。

`git status --short --untracked-files=all -- <T03目录>` 列出首轮3文件与本轮2文件；首轮文件保留，未清理其他代理工件。`git diff --check -- <T03目录>` 返回0，但这些未跟踪Markdown不受其完整内容检查，因此以结构/UTF-8实测为准。无源码变更，不运行训练/项目测试；没有生成脚本文件、测试日志、下载权重或实验产物。
