# T08 定向扩展 R2：非英语/多文字系统、UTF-8与公平因果仪器

日期：2026-11-08。输入：[覆盖审计R1](../../05_review/COVERAGE_AUDIT_R1.md)、[B08小结](../../03_reading/B08/BATCH_SUMMARY.md)、全目录与各专题卡。**新增28个确认作品，23项精读优先；本轮完整精读0，正文定向部分核查11个作品，代码核验/实验复现0。** 其余17项止于原始摘要/官方说明。本轮不是把全部工作冒充terra全文精读。

实际查询36次：中文7、日文1、西班牙文1、英文27；详细原式与访问账见[SEARCH_LOG_R2.md](SEARCH_LOG_R2.md)。查询语言只描述检索入口，不代表找到对应语言的实验，更不按作者地域推断覆盖。仅新增本文件和日志；不改`00_scope/`、既有源卡、总目录或证据表。内部材料未上传。

## 1. 去重与证据口径

- 起始快照：调研根目录92个Markdown，CATALOG共384个实体；CATALOG文本SHA256 `bfb606c1c80c26e4a00793d36a1b32a5f04752334169c833e9ef1eda6f3f6ae5`。全目录的稳定ID、正式版别名与候选题名用于核重，而不是只查T08。
- 28项均未在起始CATALOG作为作品收录。R2-003 MrT5是原T08未确认线索，此次升级摘要核验，不假称从未见过；LongBench、SIB/FLORES数据等被旧正文引用不等于已编目作品。Belebele此次正式核验；**不另把其依赖FLORES或SIB-200补成作品数**。
- 本地编号`T08-R2-001–028`不占W-ID，统一目录负责人再合并。正式版/arXiv同作只计一次；翻译介绍、仓README、模型数量、数据集子任务不另计。
- 深度 **A**：原始摘要/正式作品介绍核验；**M**：指定正文片段核验（非全文精读）；**O**：补作者官方说明。`P`=下一轮精读优先。作者字段未从可靠作者栏取得者写`—`，不把提交人当作者。
- 术语：UTF-8为可变长度Unicode字节编码；byte=字节，token=分词单元；BPB=每原文字节比特数；FLOPs=浮点运算次数；因果消费指目标内容变化特异性改变最终预测；蜕变测试指在预设输入变换下检查输出应满足的关系。Unicode码点、用户感知字素、分词位置和语义单位不是一回事。

## 2. 这次真正改变了什么

1. **不再是“没有公开UTF-8专门仪器”**：001分别评价结构合法性、目标字节精确匹配、候选likelihood。但它是**8K BPE+byte-fallback模型**的局部字符补全，非纯字节长程源依赖检验。仍未找到同时控制首/续位地板、语言、位置、同长度证据替换和长程消费的完整独立验证。
2. **同原文与同计算必须分账已有直接原文依据**：013 OneRuler主结果等token，附录D同输入；010 TokSuite主组固定token、原文字节差距显著；008配对补训至相同字节会翻转一项排序；005同语料主组实际算时不同。不能再把“dataset-controlled”改写成同FLOPs。
3. **中文检索产生了实质正式源**：028中文《软件学报》以多粒度替换测试翻译稳定性；020日文作者官方说明指出JSQuAD的token边界会破坏跨模型公平。二者不是byte消费证据，但能约束评价器设计。
4. **检索与消费有直接跨语种考场**：014五语都用拉丁字母，排除不了跨文字系统效应；013有26语但没有全语言对；015把源语言与问题语言拆开、答案固定英语以减少生成混杂；016是同语检索而非跨语检索。不能用“多语”一词盖平差别。
5. **干预本身有效也不必解释自然使用**：022将任意标签控制任务带入因果评价；026显示可激活原本休眠路径，027给相反解释与训练/评测异议。它们与R1的失忆探针、可靠性论文配对，而不是由一个工具给另一个工具自证正确。

## 3. 新增作品卡

### T08-R2-001 · P · Beyond Perplexity: UTF-8 Validity in Byte-aware Language Models
- **身份**：Sangwhan Moon, Daisuke Oba, Youmi Ma, Tatsuya Hiraoka, Naoaki Okazaki；2026；arXiv:2606.14122，v2 2026-06-25。核验A+M：[摘要](https://arxiv.org/abs/2606.14122)、[v2正文](https://arxiv.org/html/2606.14122v2) §1–4、§5.1开头；[全文PDF](https://arxiv.org/pdf/2606.14122v2)。
- **机制/实测覆盖**：355M、80B训练token；英语/日语/韩语/简体中文，目标token比例10/30/30/30。§4.1明确8,000词BPE带byte-fallback，**非原生逐字节模型**。Level0无语境字符前缀，Level1有语境目标后缀，严格区分UTF-8合法与目标字符正确；DFA拒绝过长编码、代理项、越界码点。
- **支持/反例**：困惑度收敛不等于编码合法性收敛；有效字符也可能是错误字符。Level1仅Common层，因为Rare/Unseen的合成语境难可靠生成；不能称四频率层都完成语义测验。
- **版本冲突**：本次abs返回“rare更合法”，但v2 HTML摘要及引言写“common更合法（96.21% vs95.26%）”；不静默合并，以锁定v2的实际正文为该版本记录，差分待查。
- **精读问题**：逐字符频率/字节长度/前缀长度的独立控制及DFA实现；Level1 Gemini生成语境的验证；概率比较是否受候选长度影响；能否扩为长程相关内容替换而非局部补字？未运行bytecanary代码。

### T08-R2-002 · P · MAGNET: Improving the Multilingual Fairness of Language Models with Adaptive Gradient-Based Tokenization
- **身份**：Orevaoghene Ahia et al.（公开正式搜索列全作者）；2024；arXiv:2407.08818v2 = NeurIPS2024论文。[摘要](https://arxiv.org/abs/2407.08818) A；[正式入口](https://papers.neurips.cc/paper_files/paper/2024/hash/5572bc595de865c1450868fd5391e9c5-Abstract-Conference.html)经搜索身份关联；[全文](https://arxiv.org/pdf/2407.08818v2)。
- **机制/覆盖**：按语言/文字系统专门的边界预测器压缩字节；摘要确认非拉丁文字的过分割问题。**具体训练/测试语言清单本轮未从正文取得**，不以“多语公平”标签报已覆盖中文或混合文字。
- **支持/反例**：可检验统一压缩率是否仍使脚本不公平；语言/脚本特定模块也引入身份先验和额外容量，不等于通用自动边界。
- **精读问题**：各预测器语言可见性、代码切换时路由、各语原文覆盖/算量、共享与专用容量对照；公平granularity是否付出质量或额外算时？

### T08-R2-003 · P · MrT5: Dynamic Token Merging for Efficient Byte-level Language Models
- **身份**：Julie Kallini, Shikhar Murty, Christopher D. Manning, Christopher Potts, Róbert Csordás；2024初版/2025v3；arXiv:2410.20771。[摘要](https://arxiv.org/abs/2410.20771) A；[v3正文](https://arxiv.org/html/2410.20771v3) §5–6/相关语言与基线段定向M；[全文](https://arxiv.org/pdf/2410.20771v3)。R1仅待核线索，此次不再列待核。
- **机制/覆盖**：在ByT5编码器内删除位置，保留位置上下文吸收被删信息。续预训练15语：英法西德希保俄土阿越泰中印地斯瓦希里乌尔都；TyDi GoldP另有孟加拉/芬兰/印尼/韩/泰卢固等九语。**诊断拷贝任务却只有64字节随机英语大小写**，不是多脚本精确检索。
- **支持/反例**：逐语言压缩率不同；§5比较同缩短率下BPB、实测runtime，而非只报删除率；ByT5总体BPB仍最低，不能只摘最大75%缩短。
- **精读问题**：span-corruption BPB不是无条件长程自回归LM；编码器删后decoder可见权限、短答案成本、中文首/续位与错误类型；续训ByT5历史成本和训练原文量必须纳账。

### T08-R2-004 · P · Compute Optimal Tokenization
- **身份**：—；2026；arXiv:2605.01188v2。[摘要](https://arxiv.org/abs/2605.01188) A；[全文](https://arxiv.org/pdf/2605.01188v2)。
- **机制/覆盖**：作者称988个50M–7B潜token化模型，扫描bytes/token压缩率，compute-optimal尺度更应按字节数据量描述；称推广非英语，**具体语言及配对跨度未核**。
- **支持/反例**：最优压缩率随算力预算变化，可反对固定“每token常数信息量”的比较法；不是在任意语言上证明统一byte最优。
- **精读问题**：训练FLOPs是否含熵模型/局部编解码、未最优运行点与训练字节重复；模型选择/缩放拟合区间、非英语样本及真正相同原文/FLOPs交叉实验。

### T08-R2-005 · P · An Empirical Study of Tokenizers for Multilingual Large Language Models
- **身份**：Kieron Seven Jun Wei Lee, Muhammad Reza Qorib, Andrew Ivan Soegeng, Hwee Tou Ng（HTML作者栏抽取）；2026；arXiv:2606.15044v1。[摘要](https://arxiv.org/abs/2606.15044) A；[正文](https://arxiv.org/html/2606.15044v1) §1、§3.1–3.3、§4相关语言/限制段M；[全文](https://arxiv.org/pdf/2606.15044v1)。
- **机制/覆盖**：实际11语为英、缅、中、印尼、高棉、老挝、马来、他加禄、泰米尔、泰、越；BLT/MYTE/Parity-BPE/BPE同203GB FineWeb2语料、1.5B模型比较，FLORES+平行句及十语双向翻译。
- **支持/反例**：BLT下游弱是重要独立团队反例；“低资源暴露不足解释”是作者解释而非已隔离原因。正文表2归一到8×H200小时：BLT160、MYTE300、PA87、BPE68；**同数据不是同计算**。额外等38B各自token结果被作者省略，不能当已看过完整控制表。
- **精读问题**：H100/H200换算、BLT熵模型额外GPU账及全流程公平；语料切片是否逐位相同、BPB/公平指标方向、平行数据作为PA训练额外权限。表2需PDF复核后作定量引用。

### T08-R2-006 · P · Local Byte Fusion for Neural Machine Translation
- **身份**：—（本轮HTML作者栏不完整，未猜全）；2022初版/2023v3；arXiv:2205.11490。[摘要](https://arxiv.org/abs/2205.11490) A；[v3正文](https://arxiv.org/html/2205.11490v3) §4.1–4.5、§5.1/5.2的设置/反例段M；[全文](https://arxiv.org/pdf/2205.11490v3)。
- **机制/覆盖**：byte n-gram卷积或词边界自注意聚合；7源语到英语、另四组同脚本高低资源迁移。已读段明确德语/印地语/高棉/老挝及相关拉丁脚本迁移，**表1抽取漏行，未假填完整7语名单**。
- **支持/反例**：§4.3共用原句、过滤任端>800B、Moses预分词、同epoch；这比等token更接近同原文，但不等FLOPs。§5.1明确极低资源老挝(2.7K例)仍是子词占优；聚合有益不是所有语言无条件胜。
- **精读问题**：词边界由谁提供、无空格文字规则、one-hot与dense接口容量，正文v3摘要较abs弱化了“胜过子词/训练更快”措辞；需逐版对齐，不能并成普遍优势。

### T08-R2-007 · Beyond Text Compression: Evaluating Tokenizers Across Scales
- **身份**：Jonas F. Lotz, António V. Lopes, Stephan Peitz, Hendra Setiawan, Leonardo Emili；2025；arXiv:2506.03101 = ACL2025.acl-long.1546。[正式摘要](https://aclanthology.org/2025.acl-long.1546/) A；[全文](https://aclanthology.org/2025.acl-long.1546.pdf)。
- **机制/覆盖**：小模型预测大模型tokenizer排序，Zipf相关内在指标比压缩率更有预测性；摘要称英/多语设置，但**完整实测语言、平行内容及算力控制未核**。
- **支持/反例**：反对把压缩率当下游质量充分统计；预测相关不等于机制因果。
- **下一步**：核英/多语任务、未见语言、词频指标是否共享训练/测试分布及预算；不将“跨尺度预测”当跨文字系统可靠外推。

### T08-R2-008 · P · Language-Specific Effects of Tokenizer Choice in Multilingual Language Models
- **身份**：—（作者栏抽取不全，不用From补齐）；2026；arXiv:2610.12144v1。[摘要](https://arxiv.org/abs/2610.12144) A；[正文](https://arxiv.org/html/2610.12144v1) §2.1–2.2、§4 caveats、评价建议及附录对应句M；[全文](https://arxiv.org/pdf/2610.12144v1)。
- **机制/覆盖**：123模型/54tokenizer；31训练语言、11文字系统；逐语言BPB而非只平均；正文点名中日泰无词界组及孟加拉、韩语高敏感性。NFC/NFD/不归一化及替换字节表是明确变量。
- **支持/反例**：主组1.27B模型/9.2B固定训练token，原文字节不等；§4 caveats明说按字节匹配复训可翻转25个配对之一；数据重复会改变低资源分配效应。**这是公平评价的直接反例，不是该研究所有比较都无效。**
- **精读问题**：哪些配对翻转、训练数据重复与容量共变、原文BPB分母；正文建议用原文本而非decoded文本字节，平行语料另报bits/sentence。Belebele近chance被排除，不可按31语宣称全面理解任务覆盖。

### T08-R2-009 · Parity-Aware Byte-Pair Encoding: Improving Cross-lingual Fairness in Tokenization
- **身份**：—；2025初版/2026v3；arXiv:2508.04796。[摘要](https://arxiv.org/abs/2508.04796) A；[全文](https://arxiv.org/pdf/2508.04796v3)。
- **机制/覆盖**：每次合并改善当前压缩最差语言，公平最大化准则；具体原作语言集未核，005独立比较的11语不倒填为本作语言集。
- **支持/反例**：均等代价与整体压缩可以权衡；“未见系统退化”不等于统计等效或byte原生方案必败。
- **下一步**：平行数据权限、Gini统计、最差语言公平是否掩盖局部损失；与005共享方法而非独立算法发现，两研究效果不重复加权。

### T08-R2-010 · P · TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior
- **身份**：Gül Sena Altıntaş, Malikeh Ehghaghi, Brian Lester, Fengyuan Liu, Wanru Zhao, Marco Ciccone, Colin Raffel；2025初版/ICML2026；arXiv:2512.20757v2 = PMLR306:2134–2179。[正式摘要](https://proceedings.mlr.press/v306/altintas26a.html)、[官方仓说明](https://github.com/r-three/TokSuite)、[v2正文](https://arxiv.org/html/2512.20757v2) A+O+M（§3–4、§7）；[全文](https://arxiv.org/pdf/2512.20757v2)。
- **机制/覆盖**：14个主干/初始化配对模型，五语英中波斯意土；平行典型问题、拼音/繁简/重音/零宽字符/同形异码等扰动。用ByT5词表训练的新宿主**不是google原ByT5**；不把词表名当相同预训练模型。
- **支持/反例**：§3.3 untied、约1B非embedding参数、固定100K步×256×4096位置；100B token对应ByT5约100GB、Comma278GB、Gemma2 471GB，**原文暴露不等**。§G.2称另做四模型同文本，但本轮未读该附录，不能说全14模型已同文本复验。
- **精读问题**：总词表参数/FLOPs差异、G.2全文与各语言裁剪；40个canonical问由模型在环筛到高正确率，适合相对鲁棒性但不代表一般知识/源定位。归一化提高styled字符得分却丢格式，是任务权限变化；需另测精确字符任务。

### T08-R2-011 · P · CLongEval: A Chinese Benchmark for Evaluating Long-Context Large Language Models
- **身份**：Zexuan Qiu, Jingjing Li, Shijue Huang, Xiaoqi Jiao, Wanjun Zhong, Irwin King；2024；arXiv:2403.03514 = EMNLP Findings2024.230。[正式摘要](https://aclanthology.org/2024.findings-emnlp.230/) A；[全文](https://aclanthology.org/2024.findings-emnlp.230.pdf)。
- **机制/覆盖**：中文7任务/7267例，2K+人工QA；1K–100K窗口可用；6开源+2商业模型。中文覆盖是本作实际考场，不是搜索语言推断；不含据此可确认的跨语查询。
- **支持/反例**：专门覆盖中文长文，避免只拿英文长上下文替中文证；但文长、tokenizer、截断、模型训练差异尚未单变量。
- **精读问题**：各任务的原文字符/字节跨度、抽取与汇总评分、源位置/罕见数字、模型裁剪是否丢正确证据；能否加入相同来源权限下的替换必要性实验？

### T08-R2-012 · P · LV-Eval: A Balanced Long-Context Benchmark with 5 Length Levels Up to 256K
- **身份**：Tao Yuan et al.（abs作者栏）；2024初版/2025v3；arXiv:2402.05136。[摘要](https://arxiv.org/abs/2402.05136) A；[全文](https://arxiv.org/pdf/2402.05136v3)。
- **机制/覆盖**：中英11数据集，16K–256K五档、单跳/多跳QA；迷惑事实插入、关键词/短语替换与关键词召回评分。**“256K words”是原文称谓，不擅自改成256K原生token/中文字。**
- **支持/反例**：减少常识/训练泄漏，增加干扰，接近检验内容依赖；改名/改词若同时损伤语言分布会混淆干预。
- **精读问题**：正确与诱饵替换是否等长度/语义类型、答案位置保持、替换前后对照与human校准；跨语言长度单位；关键词召回与完整答案差异。原文新版本含后来模型，勿倒引为2024已有。

### T08-R2-013 · P · One ruler to measure them all: Benchmarking multilingual long-context language models
- **身份**：Yekyung Kim, Jenna Russell, Marzena Karpinska, Mohit Iyyer（原始搜索作者栏）；2025；arXiv:2503.01996v3。[摘要](https://arxiv.org/abs/2503.01996) A；[v3正文](https://arxiv.org/html/2503.01996v3) 语言、长度协议、附录D相关段M；[全文](https://arxiv.org/pdf/2503.01996v3)。
- **机制/覆盖**：26语：中捷丹荷英芬法德印地匈意日韩挪波斯波兰葡俄塞索托西斯瓦希里瑞典泰米尔乌克兰越。七合成检索/聚合任务，含无needle和跨语言指令；**没有阿拉伯语/泰语**，不能随意从“26语”补语言。
- **支持/反例**：原文直接区分主组等token和附录D相同输入，跨语指令可改变结果；等token下候选词池大小也不同。附录同输入仍见差距，但不因此排除所有训练/语义混杂。
- **精读问题**：各语原文是否平行/同难度、负例的校准与误拒、跨语言组合采样、不同输出预算/推理长度；不能把“可以答不存在”当漏召回已识别，更不能只摘英语第6作普适排名。

### T08-R2-014 · P · Evaluating Multilingual Long-Context Models for Retrieval and Reasoning（mLongRR）
- **身份**：Ameeta Agrawal, Andy Dang, Sina Bagheri Nezhad, Rhitabrat Pokharel, Russell Scheinberg；2024；ACL:2024.mrl-1.18（工作坊）。[正式摘要](https://aclanthology.org/2024.mrl-1.18/) A；[全文](https://aclanthology.org/2024.mrl-1.18.pdf)。
- **机制/覆盖**：英、越、印尼、斯瓦希里、索马里，**全部拉丁脚本**；多目标句检索/推理，三针难于一针，语言资源差距明显。
- **支持/反例**：同脚本也会显著分化，反对把所有多语差距归UTF-8字节数；但不能代表中日阿或跨脚本性能。
- **精读问题**：针与haystack语言、翻译自然性、同token vs同文本、目标关联和诱饵控制；答错是路由还是组合？分别条件于证据全部召回后评答案。

### T08-R2-015 · P · Understanding LLMs’ Cross-Lingual Context Retrieval: How Good It Is And Where It Comes From
- **身份**：Changjiang Gao, Hankun Lin, Xin Huang, Xue Han, Junlan Feng, Chao Deng, Jiajun Chen, Shujian Huang；2025；arXiv:2504.10906 = EMNLP2025.1161。[正式摘要](https://aclanthology.org/2025.emnlp-main.1161/) A；[v1正文](https://arxiv.org/html/2504.10906v1) §2.1/§3.1 M；[全文](https://aclanthology.org/2025.emnlp-main.1161.pdf)。v3 arXiv HTML404，未假称读过正式最新版方法。
- **机制/覆盖**：40+模型、XQuAD12语平行1190例；v1 en-x=英文context/答案、非英语问题，x-x=同语对照，目标直接在上下文中，减少知识储存/输出语言混杂。12语列表从已读行/表确认英德西越中印地阿希罗俄泰土；非长篇多源导航考场。
- **支持/反例**：可分离问题编码与答案检索，后训练/模型大小不是一回事；“更大预训练无助”仅其设定，不代表通用否定。隐藏相似性分期不自动等于因果形成机制。
- **精读问题**：正式v1/v2/v3差分、Oracle估计的权限、后训练数据/样本污染、错误语言检测与模型评判独立性；同原文与答案语言钉死后加入精确证据替换。

### T08-R2-016 · P · MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages
- **身份**：Xinyu Zhang et al.；2023 TACL；ACL:2023.tacl-1.63，早报告arXiv:2210.09984题名Making a MIRACL/Multilingual Information Retrieval Across a Continuum of Languages，按项目谱系合为一作，不拆报告计数。[正式摘要](https://aclanthology.org/2023.tacl-1.63/) A；[官方数据细目](https://project-miracl.github.io/) O；[全文](https://aclanthology.org/2023.tacl-1.63.pdf)。
- **机制/覆盖**：18语同语passage检索，原生母语标注相关性。官方表确含阿孟英西波斯芬法印地印尼日韩俄斯瓦希里泰卢固泰中德约鲁巴；德/约鲁巴train=0，不能说18语都有等量训练。
- **支持/反例**：母语query不靠英译，含非拉丁脚本；但是**query和语料同语**，不是XOR。只有召回/排序，不证明生成器因果消费。
- **精读问题**：同预算检索top-k内容跨度、Wikipedia库量不同、负样本/标注漏相关性、召回正确后读者使用；原始段ID用于来源定位而非仅相似度。

### T08-R2-017 · P · XOR QA: Cross-lingual Open-Retrieval Question Answering
- **身份**：Akari Asai, Jungo Kasai, Jonathan Clark, Kenton Lee, Eunsol Choi, Hannaneh Hajishirzi；2020预印本/NAACL2021；arXiv:2010.11856 = ACL:2021.naacl-main.46。[正式摘要](https://aclanthology.org/2021.naacl-main.46/) A；[官方任务/评分](https://nlp.cs.washington.edu/xorqa/) O；[全文](https://aclanthology.org/2021.naacl-main.46.pdf)。
- **机制/覆盖**：40K母语信息需求、7非英语言；跨语文档检索、英语跨度、目标语答案三任务拆分。已读官方例日语query→英语段，**完整7语名单本轮未从原表提取，不凭记忆补**。
- **支持/反例**：来源语言与问题语言可正交，区分检索失败/读出失败/目标语生成；官方R@2kt/5kt按选中token数预算，不等于byte接口公平原文跨度。
- **精读问题**：v1/v1.1数据更改、训练答案是否同源、snippet长短及跨接口评分；工具API结果单列权限与费用。对正确源替换与错源词重叠基线补行为必要性。

### T08-R2-018 · AfriQA: Cross-lingual Open-Retrieval Question Answering for African Languages
- **身份**：Odunayo Ogundepo et al.（abs完整作者栏已取得）；2023；arXiv:2305.06897v1。[摘要](https://arxiv.org/abs/2305.06897) A；[全文](https://arxiv.org/pdf/2305.06897v1)。
- **机制/覆盖**：10非洲语言/12K+跨语QA，其他语言内容为高覆盖来源；机器翻译与多语检索方法均有显著困难。**具体10语/脚本及英语、法语pivot分配未在本轮正文核验**。
- **支持/反例**：抵消把非英语等同中日韩的覆盖偏置，处理真实信息不对称；来源稀缺性可能主导而非路由结构。
- **下一步**：母语query原生性、证据语言/目标语表、词形与变音符、翻译中间费用和本地源缺失；不可拿“10语”替代实际逐语实验表。

### T08-R2-019 · The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants
- **身份**：Lucas Bandarkar et al.；2023预印本/ACL2024；arXiv:2308.16884 = ACL:2024.acl-long.44。[正式摘要](https://aclanthology.org/2024.acl-long.44/) A；[全文](https://aclanthology.org/2024.acl-long.44.pdf)。
- **机制/覆盖**：FLORES200来源短篇、122语言变体完全平行、四选一；支持内容语义一致的对照。**122变体不是122独立文字系统/不同实验任务**。
- **支持/反例**：同义平行问题减少原文内容差；但翻译难度、选项先验、token概率聚合与被动知识都可能解释得分，不能当来源必要性仪器。
- **下一步**：逐源/问题语言组合、原文长度/字节/Unicode归一化、无context和错误context差分；同底层FLORES与其他评测并非独立样本证据。

### T08-R2-020 · P · JGLUE: Japanese General Language Understanding Evaluation
- **身份**：Kentaro Kurihara, Daisuke Kawahara, Tomohide Shibata；2022；ACL:2022.lrec-1.317。[正式摘要](https://aclanthology.org/2022.lrec-1.317/) A；[作者日文说明](https://techblog.yahoo.co.jp/entry/2022122030379907/) O；[全文](https://aclanthology.org/2022.lrec-1.317.pdf)。日文年会短版链接E8-4仅作为同项目别名，不加作品。
- **机制/覆盖**：原生构建日语而非英语翻译；汉字/平假名/片假名/拉丁字母并存、无空格边界；JSQuAD为段内抽取，非长程来源树。
- **支持/反例**：作者日文说明§4明确XLM-R tokenizer与词界不一致使JSQuAD比较不公平，故排除该项；这是**评价器与token接口冲突的原始警告**，不直接推翻该模型所有任务。
- **精读问题**：正式论文与公开评分实现的字符跨度映射/分词一致性，日文数字/异体字/归一化；准确字符级评分后byte与subword宿主能否同原文公平比较？

### T08-R2-021 · LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding
- **身份**：Yushi Bai et al.；2023预印本/ACL2024；arXiv:2308.14508 = ACL:2024.acl-long.172。[正式摘要](https://aclanthology.org/2024.acl-long.172/) A；[全文](https://aclanthology.org/2024.acl-long.172.pdf)。旧目录大量引用此数据但未作为实体，本次补原作。
- **机制/覆盖**：中英21数据集/6任务；平均英文6711 words、中文13386 characters，单位不同不是相同语义内容。不是全语言对平行数据。
- **支持/反例**：压缩/检索可改善弱长窗模型，但仍落后强长窗模型；需把宿主能力与检索/压缩手术区分。
- **下一步**：每个子集语言/长度单位、是否重复上游QA、自动指标分词、截断权限、强平层/全源基线。LongBench v2/Pro不是本作版本，不在本轮加数。

### T08-R2-022 · P · CausalGym: Benchmarking causal interpretability methods on linguistic tasks
- **身份**：Aryaman Arora, Dan Jurafsky, Christopher Potts；2024；arXiv:2402.12560v1。[摘要](https://arxiv.org/abs/2402.12560) A；[正文](https://arxiv.org/html/2402.12560v1) §5.2/§5.3及限制段M；[全文](https://arxiv.org/pdf/2402.12560v1)。
- **机制/覆盖**：SyntaxGym英语最小对、Pythia14M–6.9B、7类特征寻找方法；作者明言仅英语/一维线性子空间。干预所学方向可导致任意标签映射，故加保留类别划分但换`he/she→dog/give`的控制任务。
- **支持/反例**：扣除任意映射表达力后，DAS与其他方法差距缩小；是独立于单一probe accuracy的验证，但控制任务仍不是全部非目标真值。
- **精读问题**：原始行为基础是否高于机会、训练/验证样本分离、随机初始化、干预范数与分布外，选择性是否等于非目标保真？英语语法控制不替代中文源内容/UTF-8控制。

### T08-R2-023 · P · RAVEL: Evaluating Interpretability Methods on Disentangling Language Model Representations
- **身份**：Jing Huang, Zhengxuan Wu, Christopher Potts, Mor Geva；2024；arXiv:2402.17700v2。[摘要](https://arxiv.org/abs/2402.17700) A；[全文](https://arxiv.org/pdf/2402.17700v2)。
- **机制/覆盖**：属性—值混叠、同时满足多因果条件的MDAS，Llama2-7B；具体实体/提示语言本轮未读，**不记为多语实验**。
- **支持/反例**：目标属性可改变、无关属性应保留；比单指标翻转更接近选择性测试。作者自己提出方法并在自有基准测，不等于全面独立真值。
- **精读问题**：属性相关性、数据/实体泄漏、测试未见模板、读者是否自然依赖；与022/026的表达力/休眠路径反例对照，查非线性残余信息。

### T08-R2-024 · P · LEACE: Perfect linear concept erasure in closed form
- **身份**：Nora Belrose, David Schneider-Joseph, Shauli Ravfogel, Ryan Cotterell, Edward Raff, Stella Biderman（公开搜索原始作者栏）；2023初版/2025v4；arXiv:2306.03819。[摘要](https://arxiv.org/abs/2306.03819) A；[全文](https://arxiv.org/pdf/2306.03819v4)。
- **机制/覆盖**：最小改动下保证线性分类器不可识别指定概念，逐层scrubbing；词性与性别偏差任务，未核非英语。
- **支持/反例**：闭式删除提供线性工具的可检验保证；**linear perfect不等于信息全消失或非目标无损**，更不证明最终预测未用非线性内容。
- **精读问题**：分布/矩假设、训练与测试泛化、有限样本、非线性外探针及重建控制；在字节地板属性和语义属性相关时，删除能否保持合法UTF-8与任务可解？

### T08-R2-025 · P · Towards Best Practices of Activation Patching in Language Models: Metrics and Methods
- **身份**：Fred Zhang, Neel Nanda；2023预印本/2024v2；arXiv:2309.16042。[摘要](https://arxiv.org/abs/2309.16042) A；[全文](https://arxiv.org/pdf/2309.16042v2)。
- **机制/覆盖**：改变corruption策略和评估量会得到不同定位/电路结论。实际任务/语言的完整表未核，不称覆盖多语。
- **支持/反例**：干预效果对仪器细节敏感，不能仅换个指标后讲同一因果故事。
- **精读问题**：高斯破坏vs语义替换、logit差/NLL/概率与饱和度、层间范数匹配、阳性真值与恢复对照；检索状态的整块置乱/错内容替换分别改变了什么？

### T08-R2-026 · P · Is This the Subspace You Are Looking for? An Interpretability Illusion for Subspace Activation Patching
- **身份**：Aleksandar Makelov, Georg Lange, Neel Nanda；2023预印本/ICLR2024（官方会议搜索关联）；arXiv:2311.17030v2。[摘要](https://arxiv.org/abs/2311.17030) A；[正文](https://arxiv.org/html/2311.17030v2) §3的零空间/休眠方向构造与式(2)M；[全文](https://arxiv.org/pdf/2311.17030v2)。
- **机制/覆盖**：人为构造“可区分输入但处于下游零空间”与“可操控输出但原输入不激活”的正交方向混合，patch有效而定位不忠实；还含IOI/事实召回实例，未全读实验。
- **支持/反例**：**能操控输出≠找到了自然运作的内容通道**；同时作者承认有成功情形，不是patching一律无效。
- **精读问题**：必要/充分、全组件替换/子空间操作、真实任务是否符合构造条件；与027反驳配读，独立于拟合目标的恢复、自然输入替换、holdout机制证据到底需要哪些？

### T08-R2-027 · P · A Reply to Makelov et al. (2023)’s “Interpretability Illusion” Arguments
- **身份**：—（仅From可见，不冒充作者）；2024；arXiv:2401.12631v1。[摘要](https://arxiv.org/abs/2401.12631) A；[全文](https://arxiv.org/pdf/2401.12631v1)。
- **机制/覆盖**：反驳026的illusion定义可能连直觉上合理解释都拒绝，认为实际幻觉与训练/评测范式相关；不是新增多语实验。
- **支持/反例**：防止只取反方消融论文宣布所有子空间解释失效；与026属于**争论簇**，不能记两次独立机制复现。
- **精读问题**：双方解释定义、构造约束、跨输入泛化和因果模型预测是否一致；查哪些争议是语义定义、哪些有新实验，可否形成双方都通过的控制协议。

### T08-R2-028 · P · 面向神经机器翻译系统的多粒度蜕变测试 / Multi-granularity Metamorphic Testing for Neural Machine Translation System
- **身份**：钟文康、葛季栋、陈翔、李传艺、唐泽、骆斌（原刊关键词索引核顺序）；《软件学报》2021，32(4):1051–1066；DOI:10.13328/j.cnki.jos.006221。[原刊中文正文/摘要](https://www.jos.org.cn/html/2021/4/6221.htm) A+M（摘要、§3.1–3.2、§4.1相关段）；[原刊PDF入口](https://www.jos.org.cn/jos/article/pdf/6221)。中文原刊来源，不是英文报告中文翻译转载。
- **机制/覆盖**：句/短语/词三级替换，比较翻译输出编辑距离及成分结构；5000 UM-Corpus英→中句对、教育/微博/新闻/口语/字幕，6商用系统。**多领域不是多语言，实际主测方向只有英→中**；MCMT中间语言不算本系统对各语全面评价。
- **支持/反例**：无高质量逐例真值时的变换一致性仪器；正文将“改变局部其余结构应不变”写为假设关系，不能把它当所有翻译必然成立的因果规律，也不是内容特异读取证明。
- **精读问题**：合理同义改写/重排会否被误报、BERT替换语法保真、独立人评校准、回译补偿比值与外部API随机性；鲁棒性、参考指标相关和真正语义正确性如何分别验证？

## 4. 非英语/多文字覆盖矩阵：只登记已看见的考场

| 对象 | 已核语言/文字或方向 | 已核任务层 | 尚不能抵充的覆盖 |
|---|---|---|---|
| 001 | 英/日/韩/简中；ASCII、CJK/假名/韩字可多字节 | 有/无语境局部字符补全；结构/目标匹配分离 | 长窗来源替换、所有Unicode层、代码切换；模型仍BPE fallback |
| 003 | 15语续训，XNLI15、TyDi GoldP9另列 | 编码压缩后的分类/QA；逐语速率 | 合成64B拷贝只有英语字母；QA有答案保证不测召回遗漏 |
| 005 | 11语；拉丁、汉字、缅/高棉/老挝/泰/泰米尔脚本 | 同数据LM、分类子集、十非英语言↔英翻译 | 训练11语不代表所有分类任务都11语；同数据不等算力 |
| 010 | 英中波斯意土；繁简、拼音、零宽、变音/同形码 | 相同canonical问题下人工扰动 | 五语不等五种独立脚本；世界知识题不等长程来源检索 |
| 013 | 26语含中日韩印地泰米尔、波斯、拉丁/西里尔 | 多针、聚合、无针、跨语指令 | 并非26×26全部语言对；无针拒答≠遗漏检出保证 |
| 014 | 英越印尼斯瓦希里索马里，均拉丁 | 一/多目标检索与推理 | 不跨文字系统，但可排除“仅脚本导致差距” |
| 015 | XQuAD12语，源英/答案英、问题x；另同语x-x | 段内抽取、已有答案可复制 | 不等长文档/多源导航、不是最终回答语言切换全集 |
| 016 | 18语；多个脚本，德/约鲁巴无train | query与源同语passage相关性 | 不是跨语、不是最终因果消费、库大小非匹配 |
| 017/018 | 7非英/10非洲语，完整清单尚未逐表核 | 跨语来源、span与生成拆分 | 不能按数量宣称脚本覆盖齐全，亦不已实现byte/token控制 |
| 019 | 122语言变体平行语义 | 短篇四选一 | 不等122独立证据簇/长窗成本控制 |
| 020 | 原生日语；汉字/假名/拉丁混写 | QA与分类；评分接口已知边界风险 | 不是多语言成绩，也非原生byte模型 |
| 028 | 主要英→中，五领域 | 局部变换一致性/翻译鲁棒性 | 不是五语实验或源回访 |

没有按作者、题名“multilingual”或查询语言补上缺失格子。独立因果仪器022目前明确**只英语**；023–027未核出的多语一律未知，不给字节接口免责。

## 5. 相同原文跨度与计算公平的可证伪对照表

| 论文/已读位置 | 真实控制 | 不应偷换成 | 对下一轮的要求 |
|---|---|---|---|
| 006 §4.3 | 同原句/同epoch，统一800B过滤、Moses后文本 | 同原始未经预处理字节、同FLOPs | 核预处理版本、长度/语种过滤偏差、每语实际步时 |
| 005 §3表1/2 | 共203GB源、不同token总数；另声称等38B token | 同训练计算；省略的附加实验全已审 | 图表PDF、归一化硬件模型、熵/形态预处理全账 |
| 008 §2.1、§4 caveats | 主组等token，另部分按字节配对 | 全54组等字节/等计算 | 哪一配对排序翻转；重复数据和原文字节单位分开 |
| 010 §3.3 | 固定主干/初始化/100K训练步、100B token | 全14组原文/总参数/FLOPs都相同 | 确认G.2四模型同文本结果、output词表成本、字节宿主under-training |
| 013长度协议+附录D | 等原生token主组；相同输入辅助组 | 主榜已同内容、跨语同难度或同延迟 | 同来源跨度、needle数/位置、干扰事实、输出预算与墙钟 |
| 004仅摘要 | 扫压缩率并寻找compute-optimal | 已核988训练全账或非英齐全 | 锁参数/字节规模、FLOPs定义和新旧训练/评估权限 |

**公平至少分两条曲线，而非强迫同时满足不兼容条件**：
1. 固定同一原文与正确证据跨度，报告接口造成的位置数、参数拆分、训练/推理算量、峰值显存/延迟变化，识别“同内容接口代价”。
2. 固定总资源预算，允许各接口读不同原文量，报告真实信息覆盖与质量前沿，识别“部署效率”。
跨语言还需人译平行内容/语义单元，不将相同UTF-8字节数当同语义；跨tokenizer BPB的分母用相同原文而非被归一化/丢字符后的decoded文本。合法性/字符准确、答案准确、源召回及内容必要性单列。

## 6. 独立因果仪器验证：比“又一个probe”多要求什么

这是一份从公开候选导出的下一轮核查清单，不是本轮完成了实验验证。

| 层 | 对应候选/检查 | 通过也不能推出什么 |
|---|---|---|
| 编码结构真值 | 001 UTF-8 DFA、长度/频率层；原文码点到首/续字节映射 | 字符语义正确、相关来源被读取 |
| 自然输入真值 | 012关键词/实体替换；028局部替换；正确源与同长度错源 | 变换只改一个语义因素；规则合理性需人工/独立校准 |
| 外接可读性 | R1的control tasks/MDL、024线性删除；新非线性holdout probe | 读出器成功就是部署消费；线性删除成功就是信息消失 |
| 干预表达力控制 | 022保持类别划分但换任意标签、随机方向/初始化 | 所有非目标属性不变或无分布外激活 |
| 目标/非目标双检 | 023多属性条件；与R1 W0374完整性—选择性配读 | “独立probe”就是潜变量真实标签；未测属性也无损 |
| 自然机制对照 | 025指标/破坏方式、026休眠路径与027反论 | 可操控输出就定位自然路径；或反之所有patch均无效 |
| 部署任务闭环 | 013负例/跨语、015固定答案语言、016/017召回与读者分拆 | 找到/引用正确源即证明预测特异依赖；单删无效排除冗余源联合贡献 |

优先在**相关内容替换、无关内容替换、同UTF-8类别/长度、位置不变**四者间做独立成对比较；区分输入协议和隐藏态手术。对于隐藏态，范数匹配、同秩随机、恢复/补回、未见实体/模板及多种读出器都只能增强识别，不能替代自然内容干预。尚无本轮已核论文覆盖这整套byte-native长程组合，缺口仍明确。

## 7. 精读/追查队列与停止条件

**P共23项**：001、002、003、004、005、006、008、010、011、012、013、014、015、016、017、020、022、023、024、025、026、027、028。逐卡P标记与此清单一致。

- **先读5项**：001（结构/语义分层）、005（独立BLT反例与真实成本）、010（同主干/不同内容暴露）、013（等token/等输入双协议）、022（任意因果标签控制）。
- **再读接口7项**：002/003/004/006/008/012/020；需同原文/同预算的原表和按语言拆分，不能只拿摘要速度倍数。
- **再读源定位5项**：011/014/015/016/017，不把数据集各子任务重复计作作品；015优先锁正式版修订。
- **反证配对**：023/024/025/026/027/028与R1的028/030/031以及B08卡配读。争论双方、同数据/同模型不是独立复现。

仍须跟进但**不计新增**：中文原刊索引未找到直接byte+因果长程仪器；MAGNET完整语言列表、AfriQA/XOR源语言表；MrT5原始表1/压缩gate代码；010 G.2同文本补训；008排序翻转的特定对照；001 abs/v2常见稀有方向冲突；015 v3 HTML缺失与正式版本差分。Byte接口权重共享的干净单变量长程消费仍未补齐；B08已核ByT5 Large的输入共享/输出不共享，本轮复用而不重复占数，也不外推所有尺寸。

**建议继续定向精读而非再扩一轮泛模型名**。28个新增已把“多语标签”“相同语料”“干预翻转”三种过宽证据升级为可逐项审计的问题；最重要的余缺是byte-native独立因果检验与完整预算。若下一批只增同模板多语平均或同团队新名字，可以停止该族；若改变上述三种竞争解释则继续，即使超出20–40亦可。

## 8. 最终静态验收与并发去重

- ID 001–028连续且唯一，P逐卡计数23；11个M范围在日志逐项列出，其余不升级阅读深度。28卡均有身份/稳定键、原始来源、年份、机制、支持/反例、全文链接及下一步问题。
- 交付前重新扫描**全调研目录112个Markdown**（含其他专题并发R2），规范主键与正式别名对现时**385实体CATALOG**均零冲突；其他R2文件的题名检索也未发现这些新作品。MrT5只在旧待核线索/日志中出现，已标注。现时CATALOG文本SHA256 `62a2ea763390fd161551440f9ca68875999e8b1dc51811526742cb860e607a05`；增长/元数据修订由其他所有者负责，本代理没有写总表。此快照不承诺并发后永久零重复，也不直接报全项目总量加28。
- 查询36条编号连续，按日文假名优先分类后中文7、日文1、西文1、英文27；输出UTF-8替换字符0。`USER_CONCEPT_V01.md`仍13965 bytes、SHA256 `61cd1df2502d679792138b1af55cd3735fdfab08d7780ec66d5aca62969459b3`，未改scope原文。
- `git status --short`/`git diff --stat`未见已跟踪文件修改；仅本轮两份T08新文档由本代理写入，其他未跟踪内容不触碰。未运行训练/项目测试、未生成项目临时脚本或日志；研究结论未声称实验复现通过。
