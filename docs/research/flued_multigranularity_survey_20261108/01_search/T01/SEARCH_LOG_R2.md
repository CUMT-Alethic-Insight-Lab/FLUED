# T01 R2 新增检索日志

日期：2026-11-08，Asia/Shanghai。任务：按覆盖/精读红队，只扩展学习边界、压缩策略、合并学习；不改旧编号、共享表或其它专题。文件所有权：仅`EXPANSION_R2.md`与本日志。第一轮SEARCH_LOG/CANDIDATES/HANDOFF未修改。

## 1. 输入与计数

实际读取：
- `05_review/COVERAGE_AUDIT_R1.md`全文。
- `05_review/READING_AUDIT_R1.md`全文。
- `02_catalog/CATALOG.md`分三页完整读取（400行，384作品）；只读使用，不把目录旧“精读0”快照当当前全项目状态。
- `05_review/DISCOVERY_AUDIT_R1.md`定向搜索T01、LapMerge、QuickMerge、PISCO等，读取匹配段；作者补项明确注明复用，不声称全文重审。

**本轮32次WebSearch：30次返回结果，2次429限流。** 两个失败查询各重试一次成功。5条中文查询、1条日文查询，均为实际发出而非建议式；英文26条（含2失败）。未使用学术数据源插件、未上传内部文件或关键词、未调用私人浏览器会话。

**44次FetchURL：35次取得可用摘要/原文；另外9次没有足够可用摘要内容。** 35次可用读取对应32个新作品、2个旧作品的元数据重核、1份不计数日文原文。非有效摘要按下列互斥分类核算，不将工具返回“成功”就计摘要。

**互斥核算以此为准**：
- 35次可用摘要/原文：新32、旧2、日文未计数1。
- 3次仅身份/元数据无摘要：F05、F28、F41。
- 2次仅ACL页脚：F19、F20。
- 1次出版社主页：F14。
- 1次PDF提取失败：F25。
- 1次PDF字节流：F27。
- 1次题名作者/摘要内容错配：F29。
- 合计35+3+2+1+1+1+1＝44。没有403、认证拒绝或验证墙绕过；F25为提取失败非拒绝，后合法作者公开PDF成功。

交付32项新候选，原始摘要核验32；其中4项另定向读正文（R2-005/012/029/032），0项全文精读、0代码核验。日文稿定向阅读另记，不加入作品数；旧LapMerge与QuickMerge++不加新编号。21项列精读优先。

## 2. 逐次实际查询

日期全部为2026-11-08，平台全部为WebSearch。R2-xxx对应EXPANSION_R2的稳定本地编号；英文原题先作检索词，不将记忆当作品核验。

| 查询 | 实际输入 | 发现与处理 |
|---|---|---|
| Q01 | `学习 分词 边界 无监督 词切分 神经 语言模型 联合 负面 词法归纳` | 命中Unsupervised Tokenization Learning、中文原刊跨域分词及模型介绍；取R2-022/013原始摘要。专利和博客不计论文。 |
| Q02 | `token merging learned token merger differentiable pooling task loss 2022 2023` | 命中Soft Token Merging、DTEM原文；R2-011/010。2025软件工程合并仅线索未核，不计。 |
| Q03 | `latent tree learning negative results syntax random baselines On the Dangers of Comparing` | 命中Do latent tree…，R2-006；检验学习结构稳定性而非只看任务准确率。 |
| Q04 | `unsupervised word segmentation Bayesian Goldwater 2009 segmental neural language models 2016 2018` | 命中masked SLM、多语低资源、双向分段、NPYLM；R2-002/003/004/005。Goldwater2009未另取原始摘要，不凑数。 |
| Q05 | `中文 无监督 分词 神经 段 语言模型 Sun Deng 2018` | 命中Sun/Deng EMNLP原文，R2-001；改进伪标签迁移只有OpenReview线索，未核不计。 |
| Q06 | `Efficient Vision Transformer via Token Merger PatchMerger learned 2022` | 命中PatchMerger2202.12015与Token Merger正式作者PDF，R2-009/012。 |
| Q07 | `task based sentence compression reinforcement learning 2000 Knight Marcu Filippova 2015` | 命中句压经典链及query-focused压缩；后取R2-030。Knight/Marcu入口随后错配，不计确认。 |
| Q08 | `Segmental Recurrent Neural Networks Kong Dyer Smith 2016 segmental language models Kawakami 2019` | 命中Kawakami引文和masked SLM，R2-016；SRNN标识下一批定位。 |
| Q09 | `latent tree learning optimizing downstream tasks latent structure Yogatama Choi 2017 2018 Williams negative` | 命中ListOps、DIORA、树模型综述，R2-007/008；综述不直接计作结果证据。 |
| Q10 | `Morfessor unsupervised segmentation words minimum description length Creutz Lagus 2002 ACL` | 命中2002经典和MDL/ML对照、旧DLG引文；R2-018/019随后原始摘要核验。 |
| Q11 | `中文 句子压缩 强化学习 重建 无监督 论文` | 命中ACL2022策略梯度句压与2018去噪自编码，R2-014/015；中文检索不等于取得中文正文，两作英文。 |
| Q12 | `中文 分词 联合学习 任务驱动 分词 分类 神经 论文` | 命中中文原刊、中文媒体对Wordhood记忆的介绍；R2-013/027沿原始来源核验。 |
| Q13 | `"Learning to Merge Tokens via Decoupled Embedding" "arxiv"` | 取得2412.10569、NeurIPS关联，R2-010。 |
| Q14 | `"Learning to Discover, Ground and Use Words"` | 取得1811.09353＝P19-1645，R2-016；自动论文解说表格不作为已读原表。 |
| Q15 | `"Segmental Recurrent Neural Networks" Kong 2016` | 取得1511.06018，R2-017；语音专门同名扩展不混并。 |
| Q16 | `"Unsupervised Discovery of Morphemes" 2002 aclanthology` | 取得W02-0603＝cs/0205057，R2-018；同时出现动态字符槽2102.01223，后核R2-025。 |
| Q17 | `"Unsupervised Learning of Word Boundary with Description Length Gain"` | 取得W99-0701与CityU作者机构摘要，R2-019。 |
| Q18 | `"DiffRate" differentiable compression rate efficient vision transformers` | 取得2305.17997，R2-020。 |
| Q19 | `"Learning to Compose Task-Specific Tree Structures" "Learning to Parse and Compose"` | 取得1707.02786、AAAI正式关联，R2-021；第二短题词不是凭记忆填真实题名。 |
| Q20 | `"Learning to Parse and Compose" Yogatama arxiv` | **HTTP429失败**；Q25唯一重试。 |
| Q21 | `"Sentence Compression by Deletion with LSTMs" aclanthology` | 取得D15-1042，R2-029；官方HTML无摘要后PDF补核。 |
| Q22 | `"Statistics-Based Summarization" "Step One" sentence compression` | 取得AAAI官方入口、2002扩展等；官方摘要错配，未计新作品。 |
| Q23 | `"Unsupervised multi-granular Chinese word segmentation"` | 由中文原刊参考链追DOI/PMID，核R2-024；2023地学BERTCWS只第三方线索不计。 |
| Q24 | `"Improving Chinese Word Segmentation with Wordhood Memory Networks"` | **HTTP429失败**；Q26唯一重试。 |
| Q25 | `"Learning to Parse and Compose" Yogatama arxiv` | Q20重试成功，参考文献给1611.09100和真实题名Learning to Compose Words into Sentences with Reinforcement Learning，R2-026。 |
| Q26 | `"Improving Chinese Word Segmentation with Wordhood Memory Networks"` | Q24重试成功，取得2020.acl-main.734和作者表，R2-027；不凭中文报道背书。 |
| Q27 | `"Bayesian Unsupervised Word Segmentation" Mochihashi abstract` | 取得NPYLM作者PDF，以及半监督Q17-1013，R2-005/028；同名模型实现不另计。 |
| Q28 | `"Evaluating Sentence Compression" "Pitfalls"` | 取得W11-1611及作者PDF，R2-032；句嵌入评价坑另作不在本专题不扩。 |
| Q29 | `"Grammar Induction with Neural Language Models" "Unusual Replication"` | 取得1808.10000＝D18-1544及同题工作坊短稿W18-5452，R2-031合并一项，扩展差异待编目。 |
| Q30 | `教師なし 単語分割 ベイズ 半教師あり 境界 学習 比較` | 命中日文作者原文、研究所讲义和一般网站。取得日文半监督稿定向正文；正式书目/与英文谱系未消歧，不计新增确认作品。 |
| Q31 | `"基于新词发现的跨领域中文分词方法" 张军 作者 2022` | 原刊/机构等确认中文论文，作者OCR对末名有冲突，R2-013仅可靠首作者；不凭维普/搜索乱码强填。 |
| Q32 | `"Learning to Merge Tokens in Vision Transformers" Renggli authors` | 原站首作者、作者主页/参考文献列全作者，R2-009；不将From投稿人当首作者。 |

## 3. FetchURL逐次账本

深度A为身份与摘要/官方简介；S为只消费标明的定向正文，非FULL。即便PDF整篇被返回，也不按篇数计精读。下列F序号为实际发出顺序。

| F号 | 实际URL | 结果与消费范围 |
|---|---|---|
| F01 | https://aclanthology.org/D18-1531/ | R2-001，A摘要 |
| F02 | https://aclanthology.org/2022.sigmorphon-1.5/ | R2-002，A摘要/正式元数据 |
| F03 | https://aclanthology.org/2022.acl-long.366/ | R2-003，A摘要/正式元数据 |
| F04 | https://arxiv.org/abs/2103.01421 | R2-004，A摘要/v1史 |
| F05 | https://aclanthology.org/P09-1012/ | R2-005身份元数据，**无摘要**，不计可用A |
| F06 | https://arxiv.org/abs/1709.01121 | R2-006，A摘要/v2史 |
| F07 | https://aclanthology.org/N18-4013/ | R2-007，A摘要 |
| F08 | https://aclanthology.org/N19-1116/ | R2-008，A摘要/作者 |
| F09 | https://arxiv.org/abs/2202.12015 | R2-009，A摘要，不从提交人填作者 |
| F10 | https://arxiv.org/abs/2412.10569 | R2-010，A摘要，模块/端到端两方式明确 |
| F11 | https://openaccess.thecvf.com/content/CVPR2024W/ELVM/html/Yuan_Efficient_Transformer_Adaptation_with_Soft_Token_Merging_CVPRW_2024_paper.html | R2-011，A摘要/作者/工作坊轨道 |
| F12 | https://www.jdl.link/doc/2011/20231127_t-ip2.pdf | R2-012，A摘要/首页身份；另S读§III.C–D、§IV.C印刷4160–4163；图片数值未完整提取，不算全文精读 |
| F13 | https://jeit.ac.cn/cn/article/doi/10.11999/JEIT210675?viewType=HTML | R2-013，中英文摘要A，参考链定位R2-024；未读全篇 |
| F14 | https://image.hanspub.org/Html/19-1541704_34795.htm | **返回出版社主页和无关最新文章**，不是目标作品；不计候选，不无限追 |
| F15 | https://aclanthology.org/2022.acl-long.90/ | R2-014，A摘要 |
| F16 | https://aclanthology.org/K18-1040/ | R2-015，A摘要 |
| F17 | https://arxiv.org/abs/1811.09353 | R2-016，A摘要/v1-v2史 |
| F18 | https://arxiv.org/abs/1511.06018 | R2-017，A摘要/v1-v2史 |
| F19 | https://aclanthology.org/W02-0603/ | **仅ACL页脚**，无身份摘要；R2-018用F26补核 |
| F20 | https://aclanthology.org/W99-0701/ | **仅ACL页脚**，无身份摘要；R2-019用F32补核 |
| F21 | https://arxiv.org/abs/2305.17997 | R2-020，A摘要/v1史 |
| F22 | https://arxiv.org/abs/1707.02786 | R2-021，A摘要/v1-v4史 |
| F23 | https://aclanthology.org/2022.emnlp-main.239/ | R2-022，A摘要 |
| F24 | https://arxiv.org/abs/2505.19631 | R2-023，A摘要/v1史 |
| F25 | https://aclanthology.org/P09-1012.pdf | **提取失败**，工具提示Failed to extract meaningful content，非拒绝访问；后F36作者合法公开版成功 |
| F26 | https://arxiv.org/abs/cs/0205057 | R2-018，A摘要/2002投稿史，确认ACL工作坊同作 |
| F27 | https://aclanthology.org/W99-0701.pdf | **返回PDF原始字节流不可读文本**；工具自动保存输出到会话缓存，未另写工作区文件，不视为全文取得/已读；后F32机构摘要补核 |
| F28 | https://aclanthology.org/D15-1042/ | R2-029作者/身份/卷年，**无摘要**；F37补 |
| F29 | https://aaai.org/papers/00703-aaai00-108-statistics-based-summarization-step-one-sentence-compression/ | **错配摘要**：作者Knight/Marcu、17届会议信息，但摘要谈保留歧义的文本生成；不确认本作摘要、不纳入32项 |
| F30 | https://pubmed.ncbi.nlm.nih.gov/32853795/ | R2-024，A原始文献收录摘要/DOI/出版史；非二手解说 |
| F31 | https://arxiv.org/abs/2102.01223 | R2-025，A摘要/v1-v3史 |
| F32 | https://scholars.cityu.edu.hk/en/publications/unsupervised-learning-of-word-boundary-with-description-length-ga/ | R2-019，A作者机构摘要和正式引文；完成F20/F27未完成的核验 |
| F33 | https://arxiv.org/abs/1611.09100 | R2-026，A摘要/v1史 |
| F34 | https://aclanthology.org/2020.acl-main.734/ | R2-027，A摘要、作者与v1/v2身份 |
| F35 | https://aclanthology.org/Q17-1013/ | R2-028，A摘要；作者来自Q27可见作者PDF线索，全表未独立正文复核 |
| F36 | http://chasen.org/~daiti-m/paper/acl2009segment.pdf | R2-005，A作者/摘要，另S读§5.2、Table3/4说明文字；未逐格校验图表、不计全文精读 |
| F37 | https://aclanthology.org/D15-1042.pdf | R2-029，A摘要；另S读§4/§5印刷362–367的损失、监督来源与语法/长度局限；非全文精读 |
| F38 | https://aclanthology.org/D19-1612/ | R2-030，A摘要 |
| F39 | https://arxiv.org/abs/2610.13858v2 | **既有C30/W0030**，A版本元数据重核；v2 10-12确认，不增作品、不宣称正文差分 |
| F40 | https://arxiv.org/abs/2508.13204 | **既有C31/W0031**，A摘要仍在、无取到撤回评论；状态未知，不增作品 |
| F41 | https://aclanthology.org/W11-1611/ | R2-032作者/身份，**无摘要**；F44补 |
| F42 | https://arxiv.org/abs/1808.10000 | R2-031，A摘要/史；负面方法问题与公平复核后正面结果同时保留 |
| F43 | https://www.ism.ac.jp/~daichi/paper/nlp2011semiseg.pdf | **不计新增**日文原稿，S读§1/§3/§4.3/§5叙述，作者栏可见；出版书目和关系未消歧，不把文件名年份单独当确认 |
| F44 | https://www.cis.upenn.edu/~ccb/publications/evaluating-sentence-compression-pitfalls-and-suggested-remedies.pdf | R2-032，A摘要；S读§3/§4长度混杂/未显著反转，不升级成确定优胜 |

## 4. 去重与版本策略

首次脚本检查41个原生ID/正式版别名/核心题名字符串，CATALOG命中0；新32题名的大小写无关子串检查亦0。后续交付再按新卡稳定ID/链接抽取进行检查。**这排除了当前目录的显式ID/题名重复，不证明全部作品关系已知**。两个特殊谱系保守处理：

- 1808.10000、D18-1544和同题同作者工作坊W18-5452先关联一实体；工作坊短稿不另计，下一轮查是否有实质扩展。
- 日文半监督原稿与Q17-1013、P09-1012是相关谱系，作者/细节有差，未经唯一实体负责人消歧前不加作品数。不因语言不同计成独立实证。

CATALOG读取校验快照SHA256：`bfb606c1c80c26e4a00793d36a1b32a5f04752334169c833e9ef1eda6f3f6ae5`。主目录仍是R1整合快照，本轮不代主代理增加总数；其它扩展代理的尚未归并新项仍可能跨专题交叉，需编目负责人最终归并。

稳定关系已在卡内关联：D18-1531/1810.03167；MSLM/2104.07829；多语/2110.08415；K18-1040/1809.02669；SRNN/1511.06018；Morfessor/cs/0205057/W02-0603；P19-1645/1811.09353；D19-1612/1904.09051等。作品数、版本数和实验证据簇分开。

## 5. 检索不足、负面和元数据

- 经典不是怀旧配额：DLG、MDL/ML、贝叶斯联合分段直接改变“该监督什么/怎么更新”的假说；未泛扩数据库、图RAG、所有语音视频。
- 非英语：实际中文原刊可访问；中文句压入口失败已排除。日文原文有可读训练/解码分离和概率直接融合退化的讨论，但不能因文件可读就确认完整书目。非英语查询质量参差（Q30混入普通机器学习词条），不虚报高召回率。
- R2-006/007和R2-032为直接负面/评价反例；R2-031在指出原评测问题后仍支持其公平结果，防止单向选择证据。未显著不是等效，更不是确定反向优胜。
- LapMerge版本由实际F39核销；SOMBRERO/Compressed Memory作者从发现审计透明复用，不记本轮另取网络核验。QuickMerge++未取到撤回证据，维持未知；PISCO成本冲突留下一轮。
- 本地Grep初次传错上下文参数（`C`），改为合法`-C`后读取成功；这是本地调用错误，不是论文来源访问失败，不计WebSearch/FetchURL次数。
- 不使用arXiv编号推断异常首发日期；本轮所有新作最晚2025，正式版与预印本分列，不靠2026网页重建时间计新作。

## 6. 交付验证：PASS

已执行本地只读`python -c`结构校验：

- 32个新增ID连续无重，21★与声明一致；每卡有身份、原始来源/核验深度、全文入口、学习信号/方式、对假说作用。
- 32条实际查询、44条逐次Fetch行连续；5条中文查询、1条日文查询，余26英文请求（含2失败）。
- 自动从候选卡抽取31个arXiv/ACL主键/别名，另以41条人工整理的ID/DOI尾码/核心题名补查，目录重复命中0；32个新作品核心题名亦无大小写忽略的子串重复。
- 年份脚本核算：2010年前3、2010—2019年14、2020—2025年15，已修正初稿分组计数；两文件UTF-8替代字符0。
- 目录在并发期间从初读384实体变为385实体（非本代理修改）；已用**更新后的385实体目录重做别名去重，仍0重复**。最终结构检验所读SHA256为`fd8cc7506d7e8bf9cb536e2eb834bbce60ec4738f8cacad957b594dd07efe05a`。这不是全项目最终新增总数，跨专题并发扩展仍须统一归并。
- 首次校验命令因Bash对正则中的反引号作命令替换而失败，改用`chr(96)`构造后通过；未生成临时脚本、缓存或输出文件，不将失败隐藏为首遍通过。
- `git status --short`与本轮开始相同：调研父目录、既有草案及四个bundle未跟踪，无跟踪源码修改。T01目录当前5个Markdown中，原有CANDIDATES/HANDOFF/SEARCH_LOG本轮未编辑；只新建`EXPANSION_R2.md`与`SEARCH_LOG_R2.md`。共享目录并发变化不属于本代理，未回写、未清理。

未运行软件测试/训练、未提交、未另派代理。此校验确认交付结构/可追溯账和当前目录显式去重，不认证论文定理、统计或模型效果，也不等于重新检查每个链接的实时可用性。
