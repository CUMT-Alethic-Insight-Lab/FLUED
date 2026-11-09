# T01 实际检索日志

日期：2026-11-08（Asia/Shanghai）。执行范围：压缩、合并、分段策略的学习来源与训练方式。遵照`../../PLAN.md`，仅写本目录，不改源码/现有证据表，不提交、不训练、不派代理。外部查询只含公共机制词、公开题名/标识，未上传内部材料。

## 1. 平台、计数与核验纪律

- 主平台：工具`WebSearch`发现，`FetchURL`读取原始摘要/会议官方简介；未使用学术数据源、私人会话或浏览器自动化。
- **WebSearch共47次：45次返回结果、2次HTTP 429失败。** Q35/Q36各重试一次，Q41/Q42恢复，未重复无限请求。
- **FetchURL共65次：61次取得可用摘要/官方简介，2次网络失败，1次返回反自动访问验证页而非论文，1次HTTP 429。** 61次可用读取得到56项去重作品，另5次是同作品的会议/正式版补核；两次网络失败各仅重试一次后成功。
- **作品计数：56项，身份＋摘要/官方简介核验56项；全文部分阅读0，全文精读0，代码核验0。** 26项标为精读优先。作者字段空白16项；其余部分作者仅记录可见首作者等，不声称完成全作者元数据。
- 仅搜索命中、未读摘要的条目不计56项。C31身份和摘要核验成立，但存在未确认撤回状态提示，**不能作为有效性能证据**。计数是作品发现数，不是有效理论或性能结论数。
- `CANDIDATES.md`逐项提供稳定ID、核验入口和全文入口；下表C编号指向该文件。原网页提取为摘要并不会变成“全文已读”。

## 2. 实际查询（按发出顺序）

所有行日期均为2026-11-08，平台均为WebSearch。引号保留实际输入；宽检索中的记忆题名只作检索词，录入候选前另行打开摘要。

### 批次一：机制广域（Q01–Q04）

| 查询号 | 实际查询 | 结果与处理 |
|---|---|---|
| Q01 | `token merging ToMe ToFu ToMA token pooling training image transformer paper` | 命中ToFu预印本/WACV、ToMe官方ICLR、ToMA；核C24/C29，ToMA及谱保持合并留扩展。非官方词条不用作核验。 |
| Q02 | `learned segmentation language model H-Net dynamic chunking BLT entropy Charformer CANINE` | 命中H-Net、MANTa、Sombrero及H-Net++；后核C06/C11/C12，H-Net++未取原始摘要，不计。 |
| Q03 | `prompt compression LLMLingua LongLLMLingua LLMLingua-2 Selective Context RECOMP paper` | 命中LLMLingua-2、E2LLM等原文及博客；C43/C53沿原文核验，博客不作事实源。 |
| Q04 | `learned segmentation reinforcement learning hierarchical multiscale recurrent neural networks adaptive computation skim text` | 命中Learning to Skim Text；后核C18，未据综述参考文献确认其他作品。 |

### 批次二：学习器、压缩目标与近期发展（Q05–Q10）

| 查询号 | 实际查询 | 结果与处理 |
|---|---|---|
| Q05 | `"token" "merging" "DynamicViT" "EViT" "TokenLearner"` | 返回相关工作段和DTM-Codec、PuMer、2026视觉删减等；用于定位谱系，未直接计入；C27/C28另搜。 |
| Q06 | `"MANTa" "Charformer" "CANINE" tokenization paper` | MANTa原站及Learn Your Tokens论文，核C06，其他沿引用取C04/C05，后者之外扩展待办。 |
| Q07 | `"Compressive Transformers" "AutoCompressors" "ICAE"` | 命中ICAE、Cramming及2026压缩记忆评测；后核C38/C47/C50。 |
| Q08 | `"RECOMP" "Learning to Compress" "Gist" prompt compression` | 命中Gist、CompAct及综述；核C36/C54；综述仅作为追查入口。 |
| Q09 | `"token merging" "2026" learnable compression` | 命中CIVIC、SeCo等，后核C34/C52；搜索结果中未知模型不背书。 |
| Q10 | `"prompt compression" "reinforcement learning" 2025 2026` | 命中TACO-RL正式页，后核C44；推理输出压缩多数非输入策略，本轮不纳入；EffComp只见ResearchGate线索，不计。 |

### 批次三：边界谱系与统计基线（Q11–Q16）

| 查询号 | 实际查询 | 结果与处理 |
|---|---|---|
| Q11 | `"Token Merging: Your ViT But Faster" "TokenLearner" "Token Pooling" arxiv` | 命中ToMe、Token Pooling标识以及LapMerge，核C24/C25/C30。 |
| Q12 | `"Dynamic Token Pooling" "hierarchical" language models` | 命中ACL动态池化与多字节预测，核C07/C15；层级Transformer旧作未读摘要不计。 |
| Q13 | `"Charformer: Fast" "CANINE: Pre-training" arxiv` | 命中Charformer、CANINE标识与GQ-VAE，核C04/C05/C13。 |
| Q14 | `"Byte Latent Transformer" "SpaceByte" "MEGABYTE" arxiv` | 命中BLT、SpaceByte、Fast BLT，核C09/C10/C14。 |
| Q15 | `"Hierarchical Multiscale Recurrent Neural Networks" "Learning to Skip" arxiv` | 命中Skip RNN、HM-RNN标识，核C16/C17；若干引文带错号，未照抄。 |
| Q16 | `"Subword Regularization" "Neural Machine Translation of Rare Words" "SentencePiece"` | 命中三个统计分段作品的标识，后核C01–C03。 |

### 批次四：文本压缩定向补核（Q17–Q22）

| 查询号 | 实际查询 | 结果与处理 |
|---|---|---|
| Q17 | `"TokenLearner: What Can 8 Learned Tokens" arxiv` | 取arXiv:2106.11297，后核C26；正式版短题关系再追Q44。 |
| Q18 | `"DynamicViT: Efficient" "EViT: Expediting"` | 主要得到引文/第三方说明；不单凭这些完成核验，后Q23/Q24精确检索。 |
| Q19 | `"Learning to Compress Prompts with Gist Tokens" "Adapting Language Models to Compress Contexts"` | 命中Gist与其他相关工作段，核C36；AutoCompressors标识由随后Q20结果参考文献补出。 |
| Q20 | `"RECOMP: Improving" context compression arxiv` | 命中RECOMP原站及AutoCompressors/LongLLMLingua引文标识，核C39/C37/C41。 |
| Q21 | `"Selective Context" "Compressing Context to Enhance Inference Efficiency"` | 命中ACL正式摘要与原文§5.5粒度比较搜索片段，核C40；不将搜索片段视为表格已读。 |
| Q22 | `"LLMLingua" "LongLLMLingua" arxiv 2310` | 命中LongLLMLingua、LLMLingua官方仓库引文号，核C41/C42。 |

### 批次五：离散动作与固定层级（Q23–Q28）

| 查询号 | 实际查询 | 结果与处理 |
|---|---|---|
| Q23 | `DynamicViT arxiv 2021` | 原文参考文献给2106.02034；核C27；同时命中QuickMerge++，后核C31，状态另追Q45/Q46。 |
| Q24 | `EViT Expediting Vision Transformers via Token Reorganizations arxiv` | 命中EViT全题和2202.07800，核C28。 |
| Q25 | `Hierarchical Multiscale Recurrent Neural Networks arxiv` | 命中1609.01704，核C16；错误引文号不采用。 |
| Q26 | `Learning to Skip Text reinforcement learning arxiv LSTM Jump` | 命中Learning to Skim Text及Structural-Jump/Leap-LSTM，核C18；后两篇未读原始摘要不计。 |
| Q27 | `Compressive Transformers for Long-Range Sequence Modelling arxiv` | 命中1911.05507，核C23。 |
| Q28 | `MEGABYTE Predicting Million-byte Sequences Multiscale Transformers arxiv` | 命中2305.07185，核C08。 |

### 批次六：任务充分性、训练来源与可恢复近邻（Q29–Q34）

| 查询号 | 实际查询 | 结果与处理 |
|---|---|---|
| Q29 | `"Rationalizing Neural Predictions" arxiv` | 参考文献定位1606.04155，并发现可微二值选择1905.08160，核C20，C21另搜Q39。 |
| Q30 | `"PISCO" "COCOM" "xRAG" context compression` | 命中PISCO与2026两阶段训练配方，核C45/C48；COCOM/xRAG随后单查。 |
| Q31 | `"LoCoCo" "DODO" context compression` | 命中LoCoCo原站，核C46；DODO仅综述线索不计。 |
| Q32 | `"500xCompressor" "Cramming 1568"` | 命中Cramming的arXiv/ACL标识，核C47；500x后Q37补直接原始入口。 |
| Q33 | `"task-driven" "token merging" learning` | 命中TR-PTS、视频合并与ObjectNav任务删减；仅线索，不计确认候选，留任务驱动专门扩展。 |
| Q34 | `"recoverable compression" visual tokens "2025"` | 命中Recoverable Compression原始ID/AAAI入口和2026 Reroute，核C32/C33。 |

### 批次七：反例、表示空间与预训练比较（Q35–Q42）

| 查询号 | 实际查询 | 结果与处理 |
|---|---|---|
| Q35 | `"xRAG: Extreme Context Compression"` | **失败HTTP 429**；只在Q41重试一次。 |
| Q36 | `"Efficient Context Compression" "COCOM"` | **失败HTTP 429**；只在Q42重试一次。 |
| Q37 | `"500xCompressor" "arxiv"` | 命中2408.03094和ACL 2025.acl-long.1219，核C49。 |
| Q38 | `"Funnel-Transformer" arxiv pooling` | 参考文献与公开链接定位2006.03236，核C22。 |
| Q39 | `"Interpretable Neural Predictions with Differentiable Binary Variables"` | 命中ACL P19-1284与1905.08160，核C21。 |
| Q40 | `"token compression" "random" "2025" merging evaluation` | 命中K-Token Merging和UniPruneBench，核C51/C35；博客不作评测事实源。 |
| Q41 | `"xRAG: Extreme Context Compression"` | Q35唯一重试，成功；命中2405.13792、NeurIPS正式入口，核C55。 |
| Q42 | `"Efficient Context Compression" "COCOM"` | Q36唯一重试，成功；命中2407.09252与WSDM题名关联，核C56。 |

### 批次八：题名、正式版及状态校验（Q43–Q47）

| 查询号 | 实际查询 | 结果与处理 |
|---|---|---|
| Q43 | `"2604.15153" "Compressing"` | 原站搜索确认K-Token Merging全题含“for Large Language Models”，修正C51初次截断题名。 |
| Q44 | `"TokenLearner" "Adaptive Space-Time Tokenization for Videos" NeurIPS 2021` | 找到NeurIPS正式摘要/PDF路径与作者主页引文，随后打开官方摘要，与C26关联不新增作品。 |
| Q45 | `"2508.13204" QuickMerge` | 原站年度列表明确题名QuickMerge++和Dong Liu/Yanxuan Yu；列表评论截断“has been…”触发状态复核。 |
| Q46 | `"2508.13204" "withdrawn"` | 返回聚合页撤回字样，可能相邻记录；不作单作品撤回已确认。定向Fetch列表失败429，C31转状态警示，不再追打服务。 |
| Q47 | `"2610.13858" LapMerge authors` | 原站结果给Magdalena Trędowicz、Aleksandra Nowak等、v1/v2日期线索；C30保留版本差异待精读。 |

## 3. FetchURL取回账本

以下F序号严格按实际发出顺序，斜线后的数字是原始来源稳定标识而不是新增作品数。arXiv核验页均为`https://arxiv.org/abs/<编号>`；ACL为`https://aclanthology.org/<编号>/`。完整可点击URL逐项见CANDIDATES。**A＝身份＋摘要/官方简介，不代表打开PDF。**

| 批次 | 实际Fetch顺序 | 结果 |
|---|---|---|
| F01–F07 | F01 C11/2507.07955；F02 C06/2212.07284；F03 C05/2106.12672；F04 C04/2103.06874；F05 C10/2412.09871；F06 C09/2404.14408；F07 C07/2023.acl-long.353 | 7次A |
| F08–F15 | F08 C24/2210.09461；F09 C25/2110.03860；F10 C29/2312.01026；F11 C12/2601.22805；F12 C13/2512.21913；F13 C30/2610.13858；F14 C14/2605.08044；F15 C15/2608.15454 | 8次A |
| F16–F24 | F16 C26/2106.11297失败；F17 C36/2304.08467；F18 C37/2305.14788；F19 C38/2307.06945；F20 C39/2310.04408；F21 C40/2023.emnlp-main.391；F22 C42/2310.05736；F23 C41/2310.06839失败；F24 C43/2403.12968 | 7次A、2次网络失败 |
| F25–F33 | F25 C27/2106.02034；F26 C28/2202.07800；F27 C16/1609.01704；F28 C17/1708.06834；F29 C18/1704.06877；F30 C19/1711.02085；F31 C23/1911.05507；F32 C08/2305.07185；F33 C44/2025.findings-acl.81 | 9次A |
| F34–F42 | F34 C26/2106.11297重试；F35 C41/2310.06839重试；F36 C20/1606.04155；F37 C45/2501.16075；F38 C46/2406.05317；F39 C47/2025.acl-long.948；F40 C48/2609.05152；F41 C32/2409.01179；F42 C33/2606.12412 | 9次A，两个失败源各仅重试一次成功 |
| F43–F50 | F43 C01/1508.07909；F44 C02/1804.10959；F45 C03/1808.06226；F46 C21/P19-1284；F47 C22/2006.03236；F48 C49/2025.acl-long.1219；F49 C50/2610.19373；F50 C51/2604.15153 | 8次A |
| F51–F56 | F51 C34/2605.28115；F52 C52/2605.09463；F53 C53/2409.06679；F54 C54/2024.emnlp-main.1194；F55 C31/2508.13204；F56 C35/2511.02650 | 6次A |
| F57–F62 | F57 C55/2405.13792；F58 C56/2407.09252；F59 C24/ICLR官方；F60 C32/AAAI正式页；F61 C10/2025.acl-long.453；F62 C45/2025.findings-acl.800 | 5次A，其中3次同作品额外核验；AAAI为反自动访问页，不算摘要 |
| F63–F65 | F63 C29/WACV官方；F64 C26/NeurIPS官方；F65 C31/arXiv年度列表 | 2次同作品A；F65 HTTP 429，不可用 |

额外取回入口：
- F59：https://iclr.cc/virtual/2023/poster/12173
- F60：https://ojs.aaai.org/index.php/AAAI/article/view/32229 （返回Anubis验证页，不绕过）
- F63：https://openaccess.thecvf.com/content/WACV2024/html/Kim_Token_Fusion_Bridging_the_Gap_Between_Token_Pruning_and_Token_WACV_2024_paper.html
- F64：https://proceedings.neurips.cc/paper/2021/hash/6a30e32e56fce5cf381895dfe6ca7b6f-Abstract.html
- F65：https://arxiv.org/list/cs.AI/2025?skip=4625&show=25 （HTTP 429；本轮无重试）

## 4. 实际失败、版本错位与未纳入项

1. 网络失败：F16/F23的arXiv页面分别在F34/F35重试成功，保留原失败记录不抹掉。
2. 搜索限流：Q35/Q36各重试一次成功；原站列表F65限流不追打。主干发现没有因失败把未核验候选凑数。
3. AAAI验证页：F60并非论文摘要。C32已有arXiv摘要核验，因此作品可计数，但AAAI正式版仍需合法元数据补核。
4. 搜索日期不可靠：Sombrero搜索显示2025，实际投稿2026-01；TACO-RL及Selective Context搜索的抓取/更新日期为2026，实际正式卷年2025/2023。候选使用来源投稿史/正式卷年。
5. 版本差异：PISCO预印本摘要48小时、正式版24小时，不合并成单一训练成本；E2LLM最新摘要含后来的评测，不倒引为2024已公布；LapMerge版本提取与搜索不一致，留版本差异。
6. QuickMerge++：Q45/Q46的聚合页有撤回提示，但未能把评论可靠定位至单作品。C31原摘要核验不受影响，**有效状态待核；不得据摘要性能做正面证据**。不把邻近列表文字硬判成撤回事实。
7. 未核验作品/扩展线索（均不在56项）：ToMA、谱保持合并、PuMer、DTM-Codec、Token Transforming、H-Net++、Learn Your Tokens、Hierarchical Transformers Are More Efficient Language Models、DODO、EffComp、Structural-Jump-LSTM、Leap-LSTM、TR-PTS、ObjectNav任务删减、MOOSComp、EnComp、OSCAR、FILCO、动态提示压缩等。这里只记录实际命中词，不承诺题名/年份/质量已核实。
8. 博客、Emergent Mind、ResearchGate及CSDN结果用于引路，不替代原始摘要。新模型如果只有第三方介绍，不升级为确认候选；没有付费或认证站点绕过。

## 5. 首轮覆盖与不足

覆盖统计/规则、预测难度教师、任务无关蒸馏、重建/预测自监督、下游标签/奖励；方式覆盖无训练、可微聚合、随机重参数化、离散策略梯度、联合与多阶段、冻结接口。直接比较证据最集中于C07、C24、C43/C44、C38/C45/C48；多粒度与来源回访的近邻集中C26/C32/C33/C54。

尚未完成：全文表格/训练梯度路径核查；广义语音分段与视频/导航任务策略的系统扩展；完整作者/会议元数据；上述回访近邻是否与“多粒度表示＋原始来源映射＋查询条件下钻”完整同构。没有声称覆盖整个领域或实现总计划的500–2000项。
