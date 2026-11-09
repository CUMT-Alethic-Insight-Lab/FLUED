# 07_BYTE_SURVEY｜真实检索与去重日志

2026-11-08｜sol。仅发送公开论文题名、公开机制词。未调用付费数据源、未安装软件、未上传内部资料、未执行论文代码。检索目的为发现和核验身份/局部主张，不将取得HTML计为全文精读。

## 1. 实际查询：11次 WebSearch

以下是实际发送的查询，不是建议检索式。发现顺序保留；检索范围覆盖经典、反例与2025–2026进展，不声称穷尽2026年11月全部新稿。

| # | 精确查询 | 区分目的与实际命中 |
|---|---|---|
| Q01 | `byte character language model Charformer CANINE MANTa learned tokenization encoder decoder differences` | 已收经典机制；命中MANTa原文、Charformer原文入口、此前未入的Scratchpad Patching |
| Q02 | `byte level language models disadvantages multilingual evaluation efficiency ByT5 subword 2023` | 防止仅正面byte叙事；命中MYTE、XTREME-UP及跨任务差异线索 |
| Q03 | `byte level language model 2026 dynamic multi byte prediction hierarchical diffusion token free` | 解码瓶颈，不将压缩和生成粒度混同；命中W0015、蒸馏新稿及EvaByte官方介绍 |
| Q04 | `"EvaByte" "arxiv"` | 核介绍与论文身份；未确认独立EvaByte arXiv稿，转为官方介绍类别；命中MTPC |
| Q05 | `"AU-Nets" byte 2025 Videau` | 非H-Net的因果多层路线；命中官方代码目录、作者机构记录和题名 |
| Q06 | `character level language modeling deep self attention Al Rfou 2019 Choe 2019 tokenization evaluation marginalization` | 经典非压缩/固定窗反例；命中AAAI原文入口，尚未直接命中概率边缘化 |
| Q07 | `"Using the Output Embedding to Improve Language Models" weight tying 2017` | 共享正面来源与历史更新规则；命中EACL正式页 |
| Q08 | `"Distilling Smaller, Stronger Byte Models"` | 跨接口蒸馏而非回访；命中2609.12303原记录，暴露搜索日期误标 |
| Q09 | `"From Bytes to Ideas" site:arxiv.org/abs` | 将AU-Net二手线索落到原站，确认2506.14761 |
| Q10 | `language model evaluation tokenization marginalization byte probability Choe 2019 "segmentation"` | 路径似然与文本概率；命中EMNLP2021原作2109.02550及后续争论线索 |
| Q11 | `"Tying Word Vectors and Word Classifiers" "1611.01462"` | 核经典理论身份；搜索结果多为引文，最终直接取已知arXiv v3，不用二手结论 |

未采用的结果包括自动生成综述站、身份可疑的“2609.tokenization-survey-modern-nlp.pdf”以及不相关应用；没有拿搜索聚合页替原文。Q02含一个内部式域名结果，未打开、未引用。

## 2. 20次 FetchURL与1次浏览器正文核验

20次均返回公开内容；有两次长HTML保存为工具输出，**只读指定开头范围，不宣称读完**。未遭公开来源403/支付墙；无需绕过或重试。重复取同作品abs用于固定版本/公式核验，不算新增作品。

| # | 实际URL | 读取范围与用途 |
|---|---|---|
| F01 | https://arxiv.org/html/2605.09630v1 | 工具长输出；另Read保存文本1–65行：作者、摘要、引言/贡献。方法附录未读 |
| F02 | https://hkunlp.github.io/blog/2025/evabyte/ | 返回官方介绍至架构改进开头；不假定网页后文/图表已完整读取 |
| F03 | https://arxiv.org/abs/2403.10691 | 摘要、v1/v2历史；MYTE身份发现 |
| F04 | https://arxiv.org/html/2608.15454v2 | 工具长输出；另Read1–45行，摘要/引言与多步独立预测背景；方法/成本/附录未读 |
| F05 | https://arxiv.org/html/2212.07284 | MANTa作者栏、§3.1/3.2、§5/6与限制定向读；HTML部分表格只有标题，不能算全篇精读 |
| F06 | https://aclanthology.org/2023.findings-eacl.128/ | W0360正式摘要，确认实践反例范围 |
| F07 | https://arxiv.org/abs/2511.11346v2 | MTPC题名、摘要、v2=2026-06-02；未读方法和证明 |
| F08 | https://arxiv.org/abs/2609.12303v1 | 蒸馏摘要、v1=2026-09-11；缩放结论含外推，非直接实测全部结论 |
| F09 | https://aclanthology.org/E17-2025/ | Press/Wolf正式摘要：共享收益及更新更像输出表，两者在同一经典来源内 |
| F10 | https://arxiv.org/abs/1808.04444 | 深层字符自注意力摘要，v2=2018-12-10；固定上下文与辅助损失 |
| F11 | https://arxiv.org/abs/2106.12672v3 | Charformer摘要与v3=2022-02-23；byte模型与GBST候选块 |
| F12 | https://arxiv.org/abs/2305.07185v2 | MEGABYTE摘要与v2=2023-05-19；固定patch、局部/全局模型 |
| F13 | https://arxiv.org/abs/2506.14761v1 | AU-Net摘要与v1=2025-06-17；原字节→词→词组的多层结构 |
| F14 | https://arxiv.org/abs/2305.11938 | XTREME-UP作者栏、摘要及v2=2023-05-24；88语言、9任务，未独立取结果表 |
| F15 | https://arxiv.org/abs/2610.05978v1 | W0356摘要：扩展、局部抽象、接受位置数；与原卡同FLOPs反例对照 |
| F16 | https://aclanthology.org/2021.emnlp-main.161/ | 边缘似然原作正式摘要；多切分采样估计而非只算一条标准路径 |
| F17 | https://arxiv.org/abs/1611.01462v3 | Inan等摘要及v3=2017-03-11；理论框架与PTB实验，未核定理 |
| F18 | https://arxiv.org/abs/2103.06874v4 | CANINE摘要及v4=2022-05-18；直接字符或可选子词软先验 |
| F19 | https://arxiv.org/abs/2608.15454v2 | 固定W0015版次：v1=2026-08-16、v2=08-21；确认不是新作品 |
| F20 | https://arxiv.org/abs/2605.09630v1 | 固定N01日期及原数学排版，避免HTML重复文本将16读成1616 |

浏览器：创建后台标签打开 https://arxiv.org/abs/2403.10691v2 ，用 `page.text.snapshot(document)` 实际读作者、摘要、版本及ACL DOI。核得作者 **Tomasz Limisiewicz、Terra Blevins、Hila Gonen、Orevaoghene Ahia、Luke Zettlemoyer**；v2=2024-11-11，关联DOI `10.18653/v1/2024.acl-long.804`。未逐页比读arXiv与会议版。浏览器已有六十余标签，侧栏会拥挤；只新开这一标签，未触碰其他代理/用户标签。两次关闭该标签返回TAB_NOT_ACTIVE（中间激活亦成功过），疑似并发控制切换，未继续争抢；该标签可能仍保留，主代理可自行收尾。这不是公开来源访问失败。

### 版本/身份校验要点

- 搜索给蒸馏HTML标“2024-09-25”，与原记录v1=2026-09-11不一致；采用原记录日期，不倒引成2024工作。
- MTPC v1题名含Multi-Token、v2题名含Multi-Byte，是同`2511.11346`版本演化，不拆两篇。
- EvaByte只核到团队官方介绍及其他论文对其引用；**此轮独立论文身份未知**，不算第9篇学术作品。
- MANTa当前HTML未固定页首版本，本轮可核机制与作者但不伪称锁定某次修改；后续精读前补abs版史。
- 除明确提取作者栏者外，本日志不从arXiv的`From`字段推作者全名单。原文标题/ID可确认，不等作者/正式会议/内容每项都已核完。

## 3. 对CATALOG实际去重后的净发现

对`02_catalog/CATALOG.md`按稳定ID及题名/模型别名搜索。下列9项均无对应实体行；仅在本目录建议增加，不动原CATALOG。旧卡/报告可能在Related Work提到某名称，**提及不等收录，更不等已读**。

| 本地发现号 | 作品、稳定入口与版本 | 已核内容，及能改变哪项判断 | 此轮等级 |
|---|---|---|---|
| N01 | *Scratchpad Patching: Decoupling Compute from Patch Size in Byte-Level Language Models*，https://arxiv.org/abs/2605.09630v1 ，2026-05-10 | 临时块内状态更新且不增加持久patch KV数；原文引言说同FLOPs四类分块中三类匹配或优于无该机制者。构成“边界最优才是关键”的竞争解释，尚需读方法/消融 | 身份＋摘要/引言局部，新学术 |
| N02 | *MYTE: Morphology-Driven Byte Encoding for Better and Fairer Multilingual Language Modeling*，https://arxiv.org/abs/2403.10691v2 ，2024-11-11；ACL DOI见上 | 形态来源的编码而非单纯UTF-8；作者摘要称99语编码缩短。是否额外分词/形态资源、成本和生成可逆性尚未核 | 身份＋摘要，新学术 |
| N03 | *From Bytes to Ideas: Language Modeling with Autoregressive U-Nets*，https://arxiv.org/abs/2506.14761v1 ，2025-06-17 | byte到词、词对、最多四词；深层预测更远，浅层处理细节。多层训练目标与边界来源需全文，不因“多尺度”自动当回访 | 身份＋摘要，新学术 |
| N04 | *Fast and Expressive Multi-Byte Prediction with Probabilistic Circuits*，https://arxiv.org/abs/2511.11346v2 ，2026-06-02 | 用概率电路编码未来字节联合分布，比较独立预测与逐位预测的表达力/延迟；摘要主张保留验证器性能，具体保证和实测未读 | 身份＋摘要，新学术 |
| N05 | *Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models*，https://arxiv.org/abs/2609.12303v1 ，2026-09-11 | token logits转byte logits的近似/精确两种方法；低FLOPs与高算力区域可逆序；结论含缩放外推，教师与结束标记成本待读 | 身份＋摘要，新学术 |
| N06 | *Character-Level Language Modeling with Deeper Self-Attention*，https://arxiv.org/abs/1808.04444v2 ，2018-12-10；AAAI2019来源由Q06原刊命中 | 固定窗64层模型与中间层/位置辅助损失；非可学习压缩也能做强字符LM，不能把摘要结果当跨语字节实证 | 身份＋摘要，新学术 |
| N07 | *XTREME-UP: A User-Centric Scarce-Data Benchmark for Under-Represented Languages*，https://arxiv.org/abs/2305.11938v2 ，2023-05-24 | 88种欠代表语言、9类任务；公开检索命中byte正面结果，原abs只确认基准范围，效果表尚未取。与W0360配对避免“子词总更实用” | 身份＋摘要，新学术 |
| N08 | *You should evaluate your language model on marginal likelihood over tokenisations*，https://aclanthology.org/2021.emnlp-main.161/ ，EMNLP2021正式版；关联2109.02550仅搜索定位，未逐版比较 | 通过采样估计多切分边缘似然，域外差距与分词不确定性相关；为旧章路径/文本概率之分补原始方法来源 | 正式身份＋摘要，新学术 |
| N09 | *EvaByte: Efficient Byte-level Language Models at Scale*，https://hkunlp.github.io/blog/2025/evabyte/ ，路径年份2025，固定修订未知 | 官方介绍6.5B、1.5T bytes、EVA注意力及多字节预测；“少数据/快2倍”未核同条件实测，不当独立实验背书 | 官方介绍，新非论文候选 |

**计数：8项学术＋1项官方介绍；不是9篇新读完论文。** 原目录没有修改，因此542/543全库数字本轮保持不动。

## 4. 已收但漏读/漏综合：与净新增分开

| 已有实体 | 去重结论 | 当前应补的动作 |
|---|---|---|
| W0004 CANINE / W0005 Charformer / W0006 MANTa / W0008 MEGABYTE | 已入库，此轮原站核身份/局部机制，净新增0 | 经典原作均无独立卡；CANINE旧章用评价论文转述，Charformer/MANTa缺正式机制展开 |
| W0015 Dynamic Multi-Byte Prediction，2608.15454v2 | 已入库，净新增0 | 已收未读，独立生成轴中优先级应高于再补泛RAG近邻 |
| W0364 Press/Wolf / W0365 Inan等 | 已入库，净新增0 | 正面/理论共享原作未读；Press/Wolf经典已含输出方向更新观察 |
| W0360多维评价 / W0356 Byte Language Models | 已入库且已有FULL卡，净新增0 | 不是漏收；应重综合其实践与同FLOPs反例，避免只摘论文摘要优势 |
| W0512 Compute Optimal Tokenization / W0515 Beyond Text Compression | 已入库未读，净新增0；本轮未访问原文 | 公平预算与模型规模关系需精读，不以其标题当证据 |
| W0014 Fast BLT / W0352 MambaByte / W0518 TokSuite | 已入库且有FULL卡，净新增0；本轮查卡未重读其外网全文 | 解码/验证目标/概率比较已局部覆盖，缺的是独立主线组织，不是再加同名目录 |

## 5. 边界与检索停止理由

本轮的范围是字节/字符接口、表示压缩、生成、共享、跨语及成本，不覆盖全部神经字符模型史、所有机器翻译语言对或全部Unicode评分实现。缺漏不能从某查询无命中推成文献不存在。新发现已足以改变覆盖地图，继续泛搜的边际价值低于把经典与这批直接机制交给独立全文阅读。所有主张按摘要/局部阅读权限保留，不创建FULL卡、不给出未经全文核验的论文胜负表。
