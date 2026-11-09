# T08 实际检索日志

日期：2026-11-08（本地）。阶段：公开文献发现与摘要初筛。工具：WebSearch + FetchURL；未使用学术数据源、登录态浏览器、外部上传或训练；因此未调用数据源API/技能。检索只发送下列公共机制词和公开题名/标识。内部材料只在本地阅读。

## 方法与计数

- 以公共题名/机制检索和公开标识直达摘要交叉核验；最初直接打开的ByT5、CANINE、MEGABYTE、BLT等已知标识只是入口，不以记忆计入候选。后续公开搜索再次确认身份，摘要实际获取后才列确认。
- 搜索结果snippet用于发现，不作全文阅读。候选表每项均有实际获取的原始摘要（A）或作者官方模型说明（O）。返回整页/仓README不意味着论文全文精读。
- **45个确认去重作品，27个精读优先，0篇全文精读。** 其中bGPT以作者官方介绍和BibTeX核验，其余有原摘要。同作预印本/正式版合并，研究变体不另计。
- 查询日志39次（其中1次HTTP429失败）；“返回/选择”列只记本轮实际观察和选择，不冒充完整召回量。下表与候选编号按机制交叉，不代表每个候选必须由唯一查询生成。

## 第一批：广域与内部问题公共化（Q01–Q09）

| ID | 平台 | 实际查询（原样） | 返回/选择与处理 |
|---|---|---|---|
| Q01 | WebSearch | `byte token language models ByT5 CANINE MEGABYTE BLT H-Net comparison tokenization multilingual` | 发现2610.05978；二手博客不作证据，定向Fetch原摘要 |
| Q02 | WebSearch | `weight tying language models input output embeddings Press Wolf Inan 2017 untied byte models` | 发现2603.26663、2610.01395；经典共享作为核验入口 |
| Q03 | WebSearch | `probing classifiers limitations causal interventions language models control tasks amnesic probing counterfactual retrieval evaluation` | 原始Amnesic与2408.15510；医学综述等非主线排除 |
| Q04 | WebSearch | `"H-Net" "Dynamic Chunking" language models 2025` | 2507.07955、2508.05628；查原摘要，区分H-Net与H-NET++ |
| Q05 | WebSearch | `"MambaByte" "bGPT" token free language models` | **HTTP429**，未产生有效检索结果；未原样无限重试，后续拆公共词重新检索 |
| Q06 | WebSearch | `MambaByte token free selective state space model SpaceByte bGPT arxiv` | 2401.13660、2404.14408与官方仓；Fetch原摘要 |
| Q07 | WebSearch | `multilingual tokenization fairness premium language modeling bits per byte tokenizers Ahia 2023 Petrov 2023` | 2305.15425、2607.16117、2607.24276；前两核验，第三只作追查 |
| Q08 | WebSearch | `byte language model 2026 UTF-8 hierarchical tokenizer free byte token comparison` | 2608.27658、UBE官方仓、Fast BLT二手入口；未把博客宣称当确认 |
| Q09 | WebSearch | `RAPTOR hierarchical retrieval tree recursive abstractive processing original chunks 2024` | 2603.26668、2506.06313、adRAP线索；前两核摘要，adRAP未核不计 |

首批实际Fetch：2105.13626第一次网络失败、2103.06874成功、2305.07185成功、2412.09871第一次网络失败；随后2610.05978、2603.26663、2507.07955、2508.05628、2006.00995、2408.15510成功。ByT5/BLT各重试一次成功，未无限重试。再核2401.13660、2404.14408、2305.15425、2607.16117、2608.27658、2401.18059、2603.26668、2506.06313摘要均成功。

## 第二批：共享、因果与近期相反结果（Q10–Q21）

| ID | 平台 | 实际查询（原样） | 返回/选择与处理 |
|---|---|---|---|
| Q10 | WebSearch | `"bGPT" "Beyond Language Modeling"` | 作者官方仓sanderwood/bgpt；Fetch模型介绍与BibTeX确认2402.19155 |
| Q11 | WebSearch | `"Fast BLT" byte latent transformer 2026 arxiv` | 发现2610.11790、2610.22100、2608.06398；前两Fetch，EntropyMoE未核不计 |
| Q12 | WebSearch | `"Do All Languages Cost the Same" tokenization` | 2305.13707及2023.emnlp-main.614；正式摘要确认同作 |
| Q13 | WebSearch | `"Using the Output Embedding to Improve Language Models" "Tying Word Vectors"` | 1608.05859、1611.01462、2602.04556；核原摘要 |
| Q14 | WebSearch | `"Designing and Interpreting Probes with Control Tasks" "Probing Classifiers"` | 2102.12452及正式综述入口；control tasks需专查 |
| Q15 | WebSearch | `"RULER" "NoLiMa" "BABILong" benchmark arxiv` | 2502.05167、2404.06654、2406.10149；先核前两，后续BABILong |
| Q16 | WebSearch | `"Designing and Interpreting Probes with Control Tasks"` | D19-1275、1909.03368；正式摘要核 |
| Q17 | WebSearch | `"Information-Theoretic Probing with Minimum Description Length"` | 2020.emnlp-main.14、2003.12298；正式摘要核 |
| Q18 | WebSearch | `"The Pitfalls of Probing" "Causal"` | **未命中所期待精确题名**；返回GPT-2 greater-than及不相关条目，不构造虚假候选 |
| Q19 | WebSearch | `"Towards Causal Probing" "Language Models"` | 2205.07043、2605.07631、正式可靠性论文；前两核，后者与2408.15510关联去重 |
| Q20 | WebSearch | `"Faithful or Plausible" "Attribution" language models` | 非目标精确题名，多为综述/低资源归因/二手；不纳入确认 |
| Q21 | WebSearch | `"Lost in the Middle" "HELMET" "BABILong"` | BABILong原文、许多泛综述；再用准确题名检索 |

该批实际摘要Fetch成功：1608.05859、1611.01462、2602.04556、EMNLP614、2610.11790、2610.22100、2502.05167、2404.06654；D19-1275、EMNLP2020.14、2102.12452、2205.07043、2605.07631、2406.10149、2025.ijcnlp-long.47。官方bGPT README成功。可靠性论文早题名/后题名同一摘要和正式关系吻合，不重复计数。

## 第三批：最近邻/反事实来源、近12个月补查（Q22–Q33）

| ID | 平台 | 实际查询（原样） | 返回/选择与处理 |
|---|---|---|---|
| Q22 | WebSearch | `"Fast Byte Latent Transformer"` | 2605.08044原始题名/作者；Fetch摘要，不以二手称ICML接收为定论 |
| Q23 | WebSearch | `"HELMET: How to Evaluate"` | 2410.02694、官方项目与ICLR2025索引；核摘要 |
| Q24 | WebSearch | `"Lost in the Middle: How Language Models Use Long Contexts"` | 2307.03172与2024.tacl-1.9；核正式摘要 |
| Q25 | WebSearch | `"Attention is not Explanation" "Attention is not not Explanation"` | N19-1357、D19-1002；正反配对核摘要，避免只收支持结论 |
| Q26 | WebSearch | `"Evaluating Attribution for Retrieval-Augmented Generation" counterfactual` | 2410.12380/2025.findings-acl.1087、2605.01425、2412.10571；核摘要/关系 |
| Q27 | WebSearch | `"Sufficient Context" "Retrieval" language models` | 2411.06037与官方仓/ICLR身份；核摘要 |
| Q28 | WebSearch | `"Universal Byte-Level Encoding" 2026` | 2610.01984与Samsung官方实现；核原摘要 |
| Q29 | WebSearch | `"2506.06313" title` | 官方arXiv列表/abs确认Beyond Chunking正式题名；不把无题名摘要当已知题名猜写 |
| Q30 | WebSearch | `"Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation"` | 官方条目作者Jie Wang等确认；二手多模态表述不导入候选机制 |
| Q31 | WebSearch | `"a compression view of where byte-level models should spend compute"` | 2610.22100完整前缀题名、作者确认；与2610.11790分作品、合证据簇 |
| Q32 | WebSearch | `"Universal Byte-Level Encoding" "Reduce Cross"` | 完整题名/官方仓确认，BPE双字母表不冒充原生byte LM |
| Q33 | WebSearch | `"ByT5" "MEGABYTE" "Byte Latent Transformer" "CANINE"` | 补到2023.findings-eacl.128反向比较；2410.20771仅引用线索未核 |

实际Fetch成功：2605.08044、2410.02694、TACL2024.9、N19-1357、D19-1002、2025.findings-acl.1087、2411.06037、2610.01984、2605.01425、2412.10571；后补2023.findings-eacl.128、2025.acl-long.453（BLT正式版去重）、2610.01395。

## 第四批：身份补齐与版本关联（Q34–Q39）

| ID | 平台 | 实际查询（原样） | 返回/选择与处理 |
|---|---|---|---|
| Q34 | WebSearch | `"A Multi-dimensional Evaluation of Tokenizer-free Multilingual Pretrained Models"` | 作者Jimin Sun等、arXiv2210.07111/正式EACL关系确认 |
| Q35 | WebSearch | `"ByT5: Towards a token-free future" authors` | 原始作者与TACL2022关系确认；搜索含MRT5只留追查 |
| Q36 | WebSearch | `"MEGABYTE: Predicting Million-byte Sequences" authors` | 原始作者与NeurIPS2023关系；排除社区复现作为原作身份来源 |
| Q37 | WebSearch | `"Rate–Utility Frontiers for Language Encodings"` | Ingo Ziegler、Martin Krebs、Desmond Elliott作者核 |
| Q38 | WebSearch | `"Easy to anticipate, hard to compute" "Vera"` | Nicolás Vera Zúñiga完整名和2610.11790原条目核 |
| Q39 | WebSearch | `"Weight Tying Biases Token Embeddings Towards the Output Space" authors` | 完整作者、2026.findings-acl.2027正式关系确认；一作不加数 |

## 补充配置/代码获取的限制（不计作品）

| URL | 实际结果 | 对结论的影响 |
|---|---|---|
| `https://huggingface.co/google/byt5-small/raw/main/config.json` | network fetch failed | 不声称本轮外部独立证实ByT5 untied |
| `https://huggingface.co/google/byt5-small/resolve/main/config.json` | 另一次network failed，随后停止 | 仅两次合理尝试，不换镜像绕过限制；交接需合法公共配置核验 |
| `https://github.com/jxiw/MambaByte` | 官方README成功 | 只核介绍和指标换算示例，不认模型共享已核 |
| `https://raw.githubusercontent.com/jxiw/MambaByte/main/mamba_ssm/models/mixer_seq_simple.py` | network failed | MambaByte权重共享状态留待核 |
| `https://raw.githubusercontent.com/sanderwood/bgpt/main/model.py` | HTTP404 | 文件路径猜测失效，不据此推断仓库无模型 |
| `https://raw.githubusercontent.com/sanderwood/bgpt/main/modeling_bGPT.py` | network failed | bGPT权重共享状态留待核，不继续穷举路径 |

未读取或执行这些公共代码，未安装依赖、下载权重、调用GPU或上传内部材料。公开作者README中的夸张能力语句只作为作者主张，不当成验证结果。

## 搜索边界与排除

- 未追求全域覆盖；本轮45作品不能代表子领域总量，也不声称首创组合已完成文献排除。
- 最新12个月按2025-11-08至2026-11-08看**首发或实质修订**，不按搜索引擎抓取日期。例如ACL2019条目显示2026更新时间仍是2019作品；Bridge-RAG编号与自报历史不一致，已留待核。
- 近期优先13项：010/011/012/013/014/015/019/022/023/024/031/041/044；另030与040在此期间修订，**不是新首发**，未制造年际增长统计。
- 用户草案所列DeepSeek V4/V4.1、Kimi K3、Attention Residuals、MiTA、LongCat等由其他专题或后续验证承接；本专题**没有**因内部草案称“已核对”就背书。相关链接留在原样草案，未当确认候选。
- UTF-8首/续字节因果评价专门研究的公开覆盖仍薄；尚未找到与内部仪器逐项同构的公开方案，不能把“没找到”写成“不存在”。
