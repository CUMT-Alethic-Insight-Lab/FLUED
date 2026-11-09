# T08 R2 实际检索与核验日志

日期：2026-11-08。范围：覆盖审计F6、同内容/预算、UTF-8和独立因果验证。不上传内部文档；查询仅公共术语/题名/ID。用WebSearch、FetchURL和Kimi内置浏览器；未用学术数据源、外部问答/嵌入API或用户Chrome登录态。

## 1. 账本

- **36次实际WebSearch，均返回结果**；中文7、日文1、西班牙文1、英文27。中文查询不是对英文题名的中文翻译结果计数，也不按查询语言推断评价语言。
- **新增28个确认作品，23项P精读优先；本轮完整精读0，11作定向正文核查，代码核验0、复现0。** 8个正式ACL主入口、另一个ACL workshop、PMLR、中文原刊与arXiv共同提供来源，不把翻译聚合站作原始结论依据。
- 具体编号/稳定键/全文入口见 `EXPANSION_R2.md`。预印本—正式版、题名变体、官方仓说明合并；不把14个TokSuite模型、7个CLongEval任务或数据集语言数另算作品。
- 起始去重快照：全根92个Markdown、384个CATALOG实体；SHA256见扩展报告。公开作品不存在于旧CATALOG不等于没有任何地方提过，MrT5明确由未核线索升级。

## 2. 实际查询（原样，按执行顺序）

| ID | 实际查询 | 返回与本轮处理 |
|---|---|---|
| R2-Q01 | `字节级 语言模型 多语言 公平 计算预算 UTF-8 分词 比较` | 中文博客/智源报道、UBE/ByT5转述为主；不将博客性能叙事当确认。转公共原论文入口 |
| R2-Q02 | `中文 长文本 评测 证据定位 跨语言 检索 LongBench CLongEval LVEval` | 正式CLongEval、LVEval线索、长文二手综述；原摘要核R2-011/012，未用转载补数 |
| R2-Q03 | `多语言 字节 模型 UTF-8 续字节 首字节 熵 评估` | 多不相关中文/ACL老片段、智源报道；**未命中直接完整仪器**，记检索空白非证明不存在 |
| R2-Q04 | `"MAGNET" "multilingual fairness" tokenization` | arXiv2407.08818、NeurIPS正式入口；A核R2-002 |
| R2-Q05 | `"MrT5" dynamic token merging byte-level language models` | 2410.20771 v2/v3与作者条目；A+M核R2-003 |
| R2-Q06 | `"CausalGym" "RAVEL" "LEACE" causal probing` | CausalGym原始PDF/综述引用；未用综述替原始核验，定向拆查 |
| R2-Q07 | `日本語 バイト 言語モデル UTF-8 トークン 公平 評価` | 作者日文JGLUE说明、日语评测页与博客；选择JGLUE原作和作者说明R2-020，其他非直接入口不计 |
| R2-Q08 | `modelos de lenguaje bytes tokenización multilingüe evaluación equidad` | 原始2205.11490、2606.15044及西语学位内容；核前两R2-006/005。西语查询命中英文原文，不冒充西语论文 |
| R2-Q09 | `多语言 长上下文 跨语言 证据 检索 mLongRR` | MRL2024.18线索、2504.10906及中文多粒度文章；核R2-014/015。汉斯文章未核方法不计 |
| R2-Q10 | `"UTF-8" "continuation" "byte" "language models" evaluation` | 2606.14122直接专门评价；R2-001 A+M；2503.00224只是追查线索未核不计 |
| R2-Q11 | `"tokenization" "compute budget" "multilingual" "2025"` | 2605.01188及模块化适配论文；前者A核R2-004，适配论文不扩成泛列表 |
| R2-Q12 | `"CLongEval" "LVEval" "Evaluating Multilingual Long-Context Models for Retrieval and Reasoning"` | CLongEval原条目和MRL2024.18正式引文；后续核官方页 |
| R2-Q13 | `"OneRuler" multilingual long context benchmark` | 2503.01996及作者PDF；R2-013 A+M，区分RULER旧作品 |
| R2-Q14 | `"LVEval" benchmark arxiv` | 2402.05136原页；R2-012，旧/新版本统一不计两作 |
| R2-Q15 | `"Understanding Cross-Lingual In-Context Retrieval"` | 返回2504.10906的实际题名及正式EMNLP2025.1161；按原题名R2-015，未凭预想题名造论文 |
| R2-Q16 | `"MIRACL" multilingual retrieval 18 languages 2023` | TACL2023.63、2210.09984、官方项目；R2-016，项目早/晚题名归并 |
| R2-Q17 | `"XOR QA" cross lingual open retrieval question answering` | NAACL2021.46、2010.11856，另AfriQA2305.06897；R2-017/018 |
| R2-Q18 | `"RAVEL" evaluating interpretability methods disentangle language model representations` | 2402.17700作者/题名；R2-023 |
| R2-Q19 | `"LEACE" "Perfect linear concept erasure"` | 2306.03819原摘要、版本及正式出版索引；R2-024，不据标题推非线性删除保证 |
| R2-Q20 | `"Towards Best Practices of Activation Patching"` | 2309.16042，作者/题名；R2-025 |
| R2-Q21 | `"Is This the Subspace You Are Looking for"` | 2311.17030、ICLR原作，及2026新稿仅线索；R2-026 |
| R2-Q22 | `"Interpretability Illusion" "causal" subspace` | 2401.12631回应稿；R2-027与026成对，非重复版本 |
| R2-Q23 | `"faithfulness" "activation patching" "ground truth" benchmark` | 2403.17806等候选与泛综述；未核原摘要，不计新作，不把patch得分当独立真值 |
| R2-Q24 | `"Tokenizer Choice" "same" "compute" "bytes" language models` | 2610.12144、TokSuite正式PMLR入口/官方仓；R2-008/010 |
| R2-Q25 | `"tokenization" "fair" "Japanese" "Fujii" 2024` | 返回Parity-aware2508.04796及不相关体育同名；只核前者R2-009，未造Fujii特定论文 |
| R2-Q26 | `"Beyond Text Compression: Evaluating Tokenizers Across Scales"` | 2506.03101、ACL2025.1546作者/题名；R2-007 |
| R2-Q27 | `"SIB-200" "Belebele" benchmark languages parallel` | SIB200原作线索、Belebele正式引用；仅后续核Belebele R2-019，SIB200已被B08使用不借机加数 |
| R2-Q28 | `"The Belebele Benchmark" "122" ACL` | ACL2024.44与2308.16884，同作A核R2-019 |
| R2-Q29 | `"JGLUE: Japanese General Language Understanding Evaluation"` | LREC2022.317、日文年会/期刊线索；A+O核R2-020，未把日英版按两作品计 |
| R2-Q30 | `"LongBench: A Bilingual"` | ACL2024.172、2308.14508；R2-021，v2/Pro另作品未核不计 |
| R2-Q31 | `site:jcip.cipsc.org.cn 长文本 问答 证据 检索 评测` | 中文信息学报心理对话与法律MRC，未得直接byte/公平因果仪器；不为中文来源配额纳无关作 |
| R2-Q32 | `site:jos.org.cn 大语言模型 多语言 分词 字节 评测` | 软件学报综述、翻译覆盖模型与**多粒度蜕变测试**原刊；后者有仪器关联，Fetch正文R2-028 |
| R2-Q33 | `"MAGNET" "languages" "scripts" 2407.08818` | 原摘要与二手，未可靠补全实测语言；R2-002语言清单仍待核 |
| R2-Q34 | `"OneRuler" "languages" "Chinese" "Arabic" 26` | 原v2语言段与其他多语基准；原v3正文实核26语，不能因查询有Arabic就算涵盖阿语 |
| R2-Q35 | `"Understanding LLMs" "Cross-Lingual" "12" "languages" "Chinese"` | 正式v1/v3 PDF入口与arXivv1，辅助寻找语言/版本；正文按实际读取v1单独记 |
| R2-Q36 | `"面向神经机器翻译系统的多粒度蜕变测试" 作者 DOI` | 原刊关键词索引、万方/SciEngine引文；原刊核作者/DOI，二手OCR异字不继承；R2-028 |

## 3. 实际来源获取与消费范围

以下A条目均确实Fetch成功，不仅是题名记忆。M表示从已获取正文中**定向阅读所列段落**，不是把长页返回当读完整。

| 本地卡 | 原始获取URL/关联 | 本轮消费 |
|---|---|---|
| 001 | https://arxiv.org/abs/2606.14122；https://arxiv.org/html/2606.14122v2 | A + 浏览器DOM读§1–4、§5.1开头；未读附录/全实验；记录abs/v2常见稀有方向冲突 |
| 002 | https://arxiv.org/abs/2407.08818 | A；NeurIPS完整题名作者由原站搜索关联；没有宣称读正式全文 |
| 003 | https://arxiv.org/abs/2410.20771；https://arxiv.org/html/2410.20771v3 | A+M，合成任务英语限制、§5/§6训练/任务语言、运行指标段；未读全附录表 |
| 004 | https://arxiv.org/abs/2605.01188 | A，v1/v2同作；988运行的全表未读 |
| 005 | https://arxiv.org/abs/2606.15044；https://arxiv.org/html/2606.15044v1 | A+M，§1、§3训练数据/表1–2/指标、相关语言与限制；未PDF复核表格、不复现 |
| 006 | https://arxiv.org/abs/2205.11490；https://arxiv.org/html/2205.11490v3 | A+M，§4.1–4.5设置、§5.1/5.2反例；表1语言行抽取遗漏，完整名单未核 |
| 007 | https://aclanthology.org/2025.acl-long.1546/ | 正式A，2506.03101由搜索关联 |
| 008 | https://arxiv.org/abs/2610.12144；https://arxiv.org/html/2610.12144v1 | A+M，§2.1–2.2、§4 caveats、评价建议/匹配字节相关句；长页其他部分未读 |
| 009 | https://arxiv.org/abs/2508.04796 | A，v3最新摘要，不倒填2025性能 |
| 010 | https://proceedings.mlr.press/v306/altintas26a.html；https://arxiv.org/abs/2512.20757；https://github.com/r-three/TokSuite；https://arxiv.org/html/2512.20757v2 | 正式/预印本A、作者README O、浏览器M§3–4及§7；未审代码、未读G.2，不声称14组同原文 |
| 011 | https://aclanthology.org/2024.findings-emnlp.230/ | 正式A，2403.03514关联；搜索显示2023异常日期未继承 |
| 012 | https://arxiv.org/abs/2402.05136 | A，v3 2025修订；其后模型名单非2024结果 |
| 013 | https://arxiv.org/abs/2503.01996；https://arxiv.org/html/2503.01996v3 | A+M，26语、主长度协议、附录D相关段和图24/25说明；不称全26语对全读 |
| 014 | https://aclanthology.org/2024.mrl-1.18/ | 正式A，五语均拉丁脚本原摘要明确 |
| 015 | https://aclanthology.org/2025.emnlp-main.1161/；https://arxiv.org/html/2504.10906v1 | 正式A、v1 M§2.1/§3.1，正式多版本有别；未读正式v3 PDF |
| 016 | https://aclanthology.org/2023.tacl-1.63/；https://project-miracl.github.io/ | 正式A、官方数据表O；同语检索、德/约鲁巴train零，早2210.09984关联 |
| 017 | https://aclanthology.org/2021.naacl-main.46/；https://nlp.cs.washington.edu/xorqa/ | 正式A、官方任务/预算和数据版本O；完整7语表未读 |
| 018 | https://arxiv.org/abs/2305.06897 | A；完整作者栏可用，语言/脚本表未读 |
| 019 | https://aclanthology.org/2024.acl-long.44/ | 正式A，2308.16884关联；122变体不是全语种机制核验 |
| 020 | https://aclanthology.org/2022.lrec-1.317/；https://techblog.yahoo.co.jp/entry/2022122030379907/ | 正式A+作者日语说明O，§2–4边界/评分警告；说明不另计论文 |
| 021 | https://aclanthology.org/2024.acl-long.172/ | 正式A，2308.14508关联；非LongBench v2/Pro |
| 022 | https://arxiv.org/abs/2402.12560；https://arxiv.org/html/2402.12560v1 | A+M，§5.2/5.3、English-only与1D限制；未执行pyvene或数据 |
| 023 | https://arxiv.org/abs/2402.17700 | A，不把自己提出方法的基准自动当独立潜变量真值 |
| 024 | https://arxiv.org/abs/2306.03819 | A，v4 2025；保证限定linear |
| 025 | https://arxiv.org/abs/2309.16042 | A，v2 2024；方法/指标敏感性 |
| 026 | https://arxiv.org/abs/2311.17030；https://arxiv.org/html/2311.17030v2 | A+M，§3子空间零空间/休眠方向与式(2)构造；未复算全部证明或实证 |
| 027 | https://arxiv.org/abs/2401.12631 | A，反论稿；与026不同作品，但共同争论簇 |
| 028 | https://www.jos.org.cn/html/2021/4/6221.htm | 原刊中文A+M摘要、§3.1–3.2、§4.1；表图图片未逐图核；DOI10.13328/j.cnki.jos.006221由原刊搜索索引核 |

11个M：001、003、005、006、008、010、013、015、022、026、028。A/O不因整页返回较长而升级。

## 4. 失败、工具限制和未采用线索

- `https://arxiv.org/html/2504.10906v3`：HTTP404。改读合法公开v1及正式摘要，**没有**把版本可用性冒充一致性；正式v3正文未核。
- 浏览器第一次navigate：`TAB_NOT_ACTIVE`，重新activate本代理自建tab后正常；不是站点拒绝。游标一次与maxChars组合错误，按工具要求仅cursor续读成功；不算网络失败/论文不可得。
- 内置浏览器只创建并关闭本代理自己的1个后台标签，不触碰其他会话标签；没有用用户Chrome/Edge，不做登录上传。
- FetchURL多个HTML超过50K自动保存工具结果；使用Read/Grep仅消费与本轮问题相关段落，未下载/执行作者代码。工具存储位于会话自身缓存，不是新增项目脚本/训练工件。
- 中文信息学报两条返回与本专题不够直接，未用作数量填充；软件学报旧中文原刊028确有输入变换/独立评价关联后才收录。
- 2503.00224、2611.05033、2403.17806、SIB200、FLORES原作、LongBench v2/Pro、MYTE原作、中文汉斯混合文档研究等仅线索/文内引用，不计确认28。不是说这些作品不存在或不值得读，而是本轮未完成它们的原始身份+摘要核验/独立性审查。
- 本轮不调用配置下载补既有ByT5失败：B08已静态核Large输入/输出共享两轴，复用其有限范围；不重复做、也不把其静态代码证据推成共享消融。

## 5. 核重与最后检查协议

1. 比较28个规范主键及正式别名与CATALOG；再扫全调研目录各专题源卡/R2新文件。引用/未核线索与已建作品条目区别处理；不为保持28而隐去并发重复。
2. 检查R2-001–028连续唯一、P=23、M=11；每卡含稳定ID、原始来源、年份、核验深度、机制/实际语言、支持/反例及全文入口。
3. 查询编号R2-Q01–36连续，逐字计中文/日文/西文/英文，不把建议检索式算执行。
4. 验证`00_scope/USER_CONCEPT_V01.md`仍为原哈希，现有两份scope文档不修改；`git status --short`检查已跟踪文件零差异。研究Markdown交付不跑项目训练/单元测试。

本轮新增真实文献发现不等于覆盖收束。尤其022只英语、001只四语BPE-fallback、014只拉丁、015只是段内抽取，已在扩展正文标明，不能把它们拼成已完成byte-native多语长程消费验证。

### 最终实测核对结果

- 只读Python首次校验命令因Git Bash处理反斜杠字符串导致SyntaxError；没有执行到文件写入，也未生成脚本。改用Path.as_posix后运行成功；这是校验命令错误，不是论文获取失败。
- 实测28卡/连续001–028、23个P、36条连续查询。字段检查最初把028的“原刊PDF入口”漏判为无“全文”字样，人工核对其真实PDF链接已在；不把标签差异当缺文献。完整精读与运行验证仍为0。
- 重新遍历全调研根112个Markdown，规范主键及ACL/PMLR/DOI别名对当前385个目录实体均零命中；其他专题并发R2题名/标识检查无重复条目。仅2410.20771有旧待核线索命中，正确升级；该命中不是旧确认作品。最新目录SHA256 `62a2ea763390fd161551440f9ca68875999e8b1dc51811526742cb860e607a05`；本代理未改目录，不报全局简单相加数。
- 中文字符正则会同时命中含汉字的日文Q07；分类时先识别日文假名，故最终为中文7/日文1/西文1/英文27，不以汉字总命中8误报中文查询8。
- 两个输出UTF-8替代字符0；附件原样副本哈希未变；Git已跟踪文件无差异。本轮只写`EXPANSION_R2.md`与`SEARCH_LOG_R2.md`，没有动`00_scope/`或R1任何既有文件。
