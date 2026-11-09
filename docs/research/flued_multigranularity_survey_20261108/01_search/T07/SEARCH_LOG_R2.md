# T07 实际检索日志 R2

日期：2026-11-08。与R1 `SEARCH_LOG.md`分开记账。任务：按新红队补非可加效用、闭环反事实／策略偏差、成本敏感获取／停止、信息价值经典及非英语入口。阅读输入：PLAN、READING_AUDIT_R1、COVERAGE_AUDIT_R1及CATALOG定向行；未改这些文件。

## 1. 实计与访问状态

- **WebSearch45次：成功44，失败1（HTTP429）**。中文6次（其中1次限流、同式一次重试）、日文2、法文1、英文36。语言按实际query字符串而非结果作者／网站国家统计；中文两字短语搜到英文结果不当非英语文献覆盖。
- **FetchURL47次：45次返回文本，2次工具错误（HTTP400、404）**。成功返回中IEEE只给题名、Wald只有书目／首页、Weitzman明确无摘要，均不计摘要核验；两个Atom批次只补元数据，不是全文。
- 内置浏览器3次操作：创建J-STAGE标签、读DOM、关闭同一自建标签；补全作者、DOI、卷期页及摘要。不看／不关其他会话标签。打开时总标签超过10、侧栏拥挤；已立即清理自建页，未越权整理其余11页。
- **有效新增33（T07-056–088），优先20，全文精读0、代码核验0、复现0。** 其中32论文／综述、1博士论文介绍。3个经典作品身份有据但未达摘要门槛，单列不计。2个高度相关Nan预印本保守合1研究簇；不把Shim异名预印本再加1。
- 只用WebSearch、FetchURL及内置浏览器；没有使用插件型学术数据源、第三方登录、付费资源、外部嵌入／问答服务，也未上传内部文档。

## 2. 实际WebSearch查询（45条）

以下是实际发送的完整query；不是建议式，也不包含后续未执行的检索方案。结果栏只描述发现用途，作品确认另见Fetch／DOM账。

| 编号 | 语言 | 实际query | 返回与取舍 |
|---|---|---|---|
| Q01 | 中文 | `"信息价值" "信息互补" 决策 序贯 信息获取` | 返回Informational Substitutes等英文原稿及二手；用于063，不将结果中文化当新作。 |
| Q02 | 中文 | `"主动特征获取" "成本" 强化学习` | 发现069、082、086；中文聚合页只导向原文，不当原始中文实证。 |
| Q03 | 日文 | `"情報価値" "最適停止" ベイズ` | 结果噪声多（研究者页、营销／开关等），未确认直接相关作品，改Q27限定J-STAGE。 |
| Q04 | 英文 | `"Informational Substitutes" "complements" Chen Waggoner` | 063，FOCS完整稿与介绍材料；不同介绍不增计数。 |
| Q05 | 英文 | `"Howard" "Information Value Theory" "1966"` | 056，IEEE身份入口；后以ADS原摘要核验。 |
| Q06 | 英文 | `"Near-optimal Nonmyopic Value of Information"` | 059、060、062线索；注意arXiv归档年不等首次发表年。 |
| Q07 | 英文 | `"Information Value Theory" "Abstract" Howard 1966` | ADS提供原摘要入口；不以其他文章引用替代。 |
| Q08 | 英文 | `"A Measure of the Information Provided by an Experiment" Lindley` | 正确题名含On；057，DOI与Project Euclid。 |
| Q09 | 英文 | `"Equivalent Comparisons of Experiments" Blackwell abstract` | 058，官方稳定DOI后Fetch。 |
| Q10 | 英文 | `"Optimal Search for the Best Alternative" Weitzman abstract` | 经典身份但RePEc无摘要；发现065、064，原作列P2待核不计。 |
| Q11 | 英文 | `"Principles of Metareasoning" Russell Wefald` | 1989／1991版本线索；正式页失败后读作者概述，P3不计新增。 |
| Q12 | 英文 | `"Selecting Computations" "Theory of Rational Metareasoning"` | 实际题名Selecting Computations: Theory and Applications，061。 |
| Q13 | 英文 | `"Classification with Costly Features" Janisch` | 070，正式AAAI与预印本关联；层级deep sets另篇未扩计。 |
| Q14 | 英文 | `"EDDI" "Partial VAE"` | 071，PMLR原始摘要。 |
| Q15 | 英文 | `"Active Feature Acquisition with Generative Surrogate Models"` | 072，区别既有2006.07701。 |
| Q16 | 英文 | `"Learning Diagnostic Policies" "Examples" Bayer Zubek` | 068及2004会议前驱；前驱未单独核验，不计。 |
| Q17 | 英文 | `"Learning Policies for Adaptive Information Acquisition"` | 返回噪声及087近期ACL线索；未把查询记忆当确切论文题名。 |
| Q18 | 英文 | `"Learning a Cost Sensitive Classifier" "Dulac"` | 顺序获取的法文／经典线索；后以机构介绍核085。 |
| Q19 | 英文 | `"Double Reinforcement Learning" "Kallus" "Uehara"` | 078，锁JMLR2020；相似ICML版本不另加。 |
| Q20 | 英文 | `"Counterfactual Off-Policy Evaluation with Gumbel-Max"` | 079，原始PMLR摘要，轨迹反事实。 |
| Q21 | 英文 | `"Propensity Overfitting" "Bandit"` | 081线索，后Q35准确定位原作。 |
| Q22 | 英文 | `"Adaptively Collected Data" "Bias" Nie Tian Taylor Zou` | 080，按作者定向定位；不采用第三方博客的泛化版本。 |
| Q23 | 英文 | `"A Reduction of Imitation Learning" "No-Regret"` | 076、077；当时结果摘要不能当全文。 |
| Q24 | 英文 | `"Evaluation of Active Feature Acquisition Methods for Time-varying Feature Settings"` | 082；核销R1 U3，静态／时变不同作。 |
| Q25 | 中文 | `"成本敏感" "特征获取" 综述` | 噪声与译文居多；不计有效中文作品，后换术语“代价敏感”。 |
| Q26 | 中文 | `"信息价值" "序贯" 决策 期刊` | **HTTP429**，此时不急重试，穿插原始页面读取后Q40仅重试一次。 |
| Q27 | 日文 | `site:jstage.jst.go.jp "情報" "逐次" "意思決定" ベイズ` | 发现084原刊；其他灾害／犯罪等领域条目未纳，避免靠语言凑数。 |
| Q28 | 法文 | `"acquisition d’information" "coût" décision séquentielle` | 085作者机构法文介绍；HAL学位线索未取得，不计。 |
| Q29 | 英文 | `"Adaptive Prediction" "Resource-Constrained" Nan Saligrama` | 074及重叠稿线索。 |
| Q30 | 英文 | `"Supervised Sequential Classification" "Trapeznikov"` | 073，预算监督停止经典。 |
| Q31 | 英文 | `"Information Value Theory" "howard" filetype:pdf stanford` | 没定位到可直接读取的作者原PDF；未抓超大合集／非正规转载凑经典核验，最终用ADS原摘要。 |
| Q32 | 英文 | `"Optimal Search for the Best Alternative" "weitzman" pdf harvard` | 多为引用／研究简介，仍无原摘要，P2不计。 |
| Q33 | 英文 | `"An approximate nonmyopic computation for value of information" Heckerman Horvitz` | 062，1991会议／1993期刊关联与作者机构入口；不并作独立两篇。 |
| Q34 | 英文 | `"Sequential Tests of Statistical Hypotheses" Wald 1945 abstract` | P1身份及官方页，Fetch未返回摘要；未用现代SPRT解说充原文。 |
| Q35 | 英文 | `"The Self-Normalized Estimator for Counterfactual Learning"` | 081，NeurIPS官方摘要与作者机构页；搜索曾返回2027材料，未纳。 |
| Q36 | 英文 | `"Bayesian Experimental Design: A Review" Chaloner Verdinelli` | 088，官方原摘要核验，DOI按期刊页面ss前缀。 |
| Q37 | 英文 | `"Beyond adaptive submodularity" "ratio" Fujii Sakaue` | 066，PMLR原作；非次模不自动意味着贪心必然差。 |
| Q38 | 英文 | `"Learning to Acquire Information" "He" "Daumé" "Eisner"` | 真命中075 Active Information Acquisition；最初记忆作者不同，以Atom更正为He／Mineiro／Karampatziakis。 |
| Q39 | 英文 | `"The Knowledge-Gradient Policy" "Sequential Information Collection"` | 067，作者机构原摘要；不因检索时间戳2024将发表年改写。 |
| Q40 | 中文 | `"信息价值" "序贯" 决策 期刊` | Q26一次重试成功；结果偏引用／书籍／非直接相关，不增计有效作。 |
| Q41 | 中文 | `"信息获取" "代价敏感" 分类` | 083中文原刊综述；其他错分代价应用不因关键词命中纳入。 |
| Q42 | 英文 | `"AFABench" "erratum" "CUBE-NM"` | 未搜到明确作者勘误；普通arXiv、仓库、学位论文入口，未复述争议精确成本。 |
| Q43 | 英文 | `"Optimal Nonmyopic Value of Information in Graphical Models" arxiv` | 060正式IJCAI PDF；未把近似UAI稿059合成同篇。 |
| Q44 | 英文 | `"Bayesian decision theory for clinical trials" "Sakamaki"` | 补084作者拼写线索，最终由官方DOM而非二手列表完整核名。 |
| Q45 | 英文 | `"Adaptive Classification for Prediction Under a Budget" "1704.07505"` | 确认两Nan稿标题及实质重叠线索，Fetch原摘要；保守计一簇。 |

## 3. FetchURL逐请求账（47条）

`A`表示该返回内容参与摘要／官方介绍核验；`M`为元数据；`I`只有身份不足摘要；`E`工具错误；`S`补充作者介绍／谱系，不单独计作品。相同作品多URL不增计数。所有日期均2026-11-08。

| 请求 | 对象 | 实际URL | 状态／消费范围 |
|---|---|---|---|
| F01 | 063 | https://arxiv.org/abs/1703.08636 | A，摘要。 |
| F02 | 059 | https://arxiv.org/abs/1207.1394 | A，摘要；归档年另由M补核。 |
| F03 | 060 | https://ijcai.org/proceedings/2005/137 | A，官方摘要；书目抽取末尾警示不能当原作者事实。 |
| F04 | 056 | https://ieeexplore.ieee.org/document/4082064/ | I，只返回题名；未视为摘要／全文成功。 |
| F05 | 057 | https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-27/issue-4/On-a-Measure-of-the-Information-Provided-by-an-Experiment/10.1214/aoms/1177728069.full | A，摘要、身份、DOI。 |
| F06 | 058 | https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-24/issue-2/Equivalent-Comparisons-of-Experiments/10.1214/aoms/1177729032.full | A，摘要、身份、DOI。 |
| F07 | 061 | https://arxiv.org/abs/1408.2048 | A，摘要。 |
| F08 | P3 | https://www.sciencedirect.com/science/article/pii/000437029190015C | E，HTTP400，不重复调用。 |
| F09 | 070 | https://arxiv.org/abs/1711.07364 | A，摘要、AAAI2019 comment。 |
| F10 | 071 | https://proceedings.mlr.press/v97/ma19c.html | A，PMLR身份／摘要。 |
| F11 | 072 | https://arxiv.org/abs/2010.02433 | A，摘要。 |
| F12 | 068 | https://jair.org/index.php/jair/article/view/10420 | A，JAIR摘要与发表日期；作者／DOI由F40补。 |
| F13 | 078 | https://www.jmlr.org/papers/v21/19-827.html | A，官方摘要／作者／卷期。 |
| F14 | 079 | https://proceedings.mlr.press/v97/oberst19a.html | A，官方摘要／身份。 |
| F15 | 080 | https://proceedings.mlr.press/v84/nie18a.html | A，官方摘要／身份。 |
| F16 | 076 | https://proceedings.mlr.press/v15/ross11a.html | A，官方摘要／身份；作者简名保别名。 |
| F17 | 082 | https://www.jmlr.org/papers/v26/23-1635.html | A，时变AFA评估，非静态同名。 |
| F18 | 077 | https://arxiv.org/abs/1406.5979 | A，摘要。 |
| F19 | 073 | https://proceedings.mlr.press/v31/trapeznikov13a.html | A，官方摘要／身份。 |
| F20 | 074 | https://arxiv.org/abs/1705.10194 | A，摘要，后M发现admin overlap note。 |
| F21 | 069 | https://proceedings.neurips.cc/paper/2018/hash/e5841df2166dd424a57127423d276bbe-Abstract.html | A，正式摘要，题名由检索、作者及异名预印本由M。 |
| F22 | 065 | https://arxiv.org/abs/1905.01428 | A，摘要。 |
| F23 | 064 | https://arxiv.org/abs/1711.00405 | A，摘要。 |
| F24 | 084 | https://www.jstage.jst.go.jp/article/jjb/41/1/41_55/_article/-char/ja/ | A，日文题名／英文原摘要；抽取未含作者，后DOM补。 |
| F25 | 062 | https://arxiv.org/abs/1303.5720 | A，摘要。 |
| F26 | 081 | https://proceedings.neurips.cc/paper_files/paper/2015/hash/39027dfad5138c9ca0c474d71db915c3-Abstract.html | A，原摘要；F42补作者及介绍。 |
| F27 | 088 | https://projecteuclid.org/journals/statistical-science/volume-10/issue-3/Bayesian-Experimental-Design-A-Review/10.1214/ss/1177009939.full | A，官方摘要／身份。 |
| F28 | P1 | https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-16/issue-2/Sequential-Tests-of-Statistical-Hypotheses/10.1214/aoms/1177731118.full | I，Wald书目／首页，未返回摘要，不计有效新增。 |
| F29 | 066 | https://proceedings.mlr.press/v97/fujii19a.html | A，原摘要。 |
| F30 | 075 | https://arxiv.org/abs/1602.02181 | A，摘要；F40核作者避免将From当作者。 |
| F31 | 067 | https://collaborate.princeton.edu/en/publications/a-knowledge-gradient-policy-for-sequential-information-collection/ | A，作者机构摘要、正式引用及DOI。 |
| F32 | 083 | https://jos.org.cn/html/2020/1/5871.htm | A，原刊中文摘要，另仅消费成本分类开头；返回长正文不计全文精读。 |
| F33 | 086 | https://arxiv.org/abs/2502.11067 | A，摘要、v2更新时间。 |
| F34 | 056 | https://ui.adsabs.harvard.edu/abs/1966ITSSC...2...22H/abstract | A，ADS所载原摘要／作者／DOI，弥补IEEE空壳；不称正式全文。 |
| F35 | 085 | https://www.lip6.fr/actualite/personnes-fiche.php?ident=D1131 | A，作者机构法文介绍、博士论文正式列项和答辩日期；列出的其他文章只作待追。 |
| F36 | 084 | https://www.jstage.jst.go.jp/article/jjb/41/1/41_55/_article/-char/en | A，同篇英文摘要，不另计。 |
| F37 | 083 | https://jos.org.cn/jos/article/abstract/5871 | A，中文作者／发表／在线日期、题名及摘要补全。 |
| F38 | 084 | https://www.jstage.jst.go.jp/article/jjb/41/1/41_55/_ris/-char/ja | E，尝试元数据导出路径HTTP404；不是整篇不可访问。停止该路径，直接DOM补核。 |
| F39 | M1 | https://export.arxiv.org/api/query?id_list=1703.08636,1207.1394,1408.2048,1711.07364,2010.02433,1406.5979,1705.10194,1905.01428,1711.00405,1303.5720&max_results=10 | M，10条官方记录的题名、作者、comment、首发／更新日。 |
| F40 | M2 | https://export.arxiv.org/api/query?id_list=1602.02181,2502.11067,1709.05964,1109.2127&max_results=10 | M，4条；069异名稿、068JAIR正式关系、075真实作者等。 |
| F41 | 062 | https://www.microsoft.com/en-us/research/publication/approximate-nonmyopic-computation-value-information/?lang=ja | A/S，作者机构原介绍；日语UI但正文英文，不计新的日文作品。 |
| F42 | 081 | https://www.cs.cornell.edu/~adith/ | S，作者署名／作品年份及倾向过拟合解释；其他所列研究未Fetch摘要，不新增。 |
| F43 | 087 | https://aclanthology.org/2026.findings-emnlp.52/ | A，近期官方摘要及作者／正式信息；性能仅作者声称，不背书。 |
| F44 | 060 | https://www.ijcai.org/proceedings/2005/0137.pdf | A+开头定位，题名作者、摘要及§1开环／闭环区别；未阅读全文／证明，不能计FULL。 |
| F45 | P2 | https://ideas.repec.org/a/ecm/emetrp/v47y1979i3p641-54.html | I，Weitzman身份；明说无摘要／正式全文受限，不计有效新增。 |
| F46 | P3 | https://people.eecs.berkeley.edu/~russell/research-bo.html | S，作者概述元推理与局限，列1989／1991；不是锁定原作摘要，仍不计有效新增。 |
| F47 | 074别名簇 | https://arxiv.org/abs/1704.07505 | A，两稿高度相似摘要及早期日期；保守一簇，不因两个ID多计。 |

### DOM补核

- 创建 `https://www.jstage.jst.go.jp/article/jjb/41/1/41_55/_article/-char/ja/`，得到自建标签panel-tab-311。
- `page.text.snapshot`，document范围18000字符：官方DOM给完整9作者、2020年41卷1期55–91页、DOI `10.5691/jjb.41.55`和摘要。只消费这些身份／摘要及可见参考链，不算原文精读。
- 关闭panel-tab-311。其他标签仅出现在工具状态列表，未读／未操作。未将浏览器其他代理已打开的论文算本轮阅读。

## 4. 去重清单（33个新增原生键）

下表供总目录负责人归并；**不是新W-ID分配**。全部主键／标题已与本轮CATALOG快照只读比对，未命中已有384项。并发专题后续仍可能新增同一作，归并时以稳定键／研究簇处理。年份与实体类型见扩展正文。

| local ID | 主键 | 必须保留的别名／关系 |
|---|---|---|
| T07-056 | doi:10.1109/TSSC.1966.300074 | IEEE4082064；ADS1966ITSSC...2...22H。 |
| T07-057 | doi:10.1214/aoms/1177728069 | Lindley1956；MathNet译介不另计。 |
| T07-058 | doi:10.1214/aoms/1177729032 | Blackwell1953，区别W0101/W0102后续工作。 |
| T07-059 | arxiv:1207.1394 | UAI2005旧稿2012归档。 |
| T07-060 | ijcai:2005/137 | 正式PDF0137；与059目标／算法不同，不误并。 |
| T07-061 | arxiv:1408.2048 | UAI2012旧稿2014归档。 |
| T07-062 | arxiv:1303.5720 | UAI1991；1993相关期刊DOI10.1109/34.204912待逐版比，不增计。 |
| T07-063 | arxiv:1703.08636 | FOCS2016完整稿2017。 |
| T07-064 | arxiv:1711.00405 | SODA2018，非Weitzman原作。 |
| T07-065 | arxiv:1905.01428 | EC2019，非Doval原作。 |
| T07-066 | pmlr:v97/fujii19a | arxiv:1904.10748。 |
| T07-067 | doi:10.1137/070693424 | 作者机构及作者PDF同作。 |
| T07-068 | arxiv:1109.2127 | doi:10.1613/jair.1512；JAIR2005，归档2011。 |
| T07-069 | arxiv:1709.05964 | neurips:e5841df2166dd424a57127423d276bbe；2017预印本与2018正式异名，同计1。 |
| T07-070 | arxiv:1711.07364 | AAAI2019，v2为2018。 |
| T07-071 | pmlr:v97/ma19c | arxiv:1809.11142。 |
| T07-072 | arxiv:2010.02433 | 不同于W0305/arxiv:2006.07701；同作者不误合。 |
| T07-073 | pmlr:v31/trapeznikov13a | 全文主文件与补充入口不增作。 |
| T07-074 | arxiv:1705.10194 | arxiv:1704.07505，admin明确文字重叠；保守一簇待目录／terra消歧。 |
| T07-075 | arxiv:1602.02181 | 实际作者He/Mineiro/Karampatziakis。 |
| T07-076 | pmlr:v15/ross11a | arxiv:1011.0686；Drew与J.Andrew Bagnell作者别名。 |
| T07-077 | arxiv:1406.5979 | 不把AggreVaTe方法名增作。 |
| T07-078 | jmlr:19-827 | 相近ICML版本待实质关联，不增计。 |
| T07-079 | pmlr:v97/oberst19a | arxiv:1905.05824。 |
| T07-080 | pmlr:v84/nie18a | arxiv:1708.01977。 |
| T07-081 | neurips:39027dfad5138c9ca0c474d71db915c3 | 作者PDF及主页介绍；非现有W0317 CRM原作。 |
| T07-082 | jmlr:23-1635 | arxiv:2312.01530；不同于现有静态W0307；核销R1-U3。 |
| T07-083 | jos:5871 | 中文原刊，在线2019/卷年2020。 |
| T07-084 | doi:10.5691/jjb.41.55 | 日英摘要同作，9作者。 |
| T07-085 | lip6:person-D1131/thesis-2014 | 机构法文介绍与英文列项同博士论文；不是页面所列全部作品。 |
| T07-086 | arxiv:2502.11067 | 2025v1/2026v2；同作者／综述不算独立复证。 |
| T07-087 | acl:2026.findings-emnlp.52 | DeepControl方法名不增作；官方DOI字段无/v1，保原值待核。 |
| T07-088 | doi:10.1214/ss/1177009939 | 经典综述，非其所引各原作的核验替代品。 |

## 5. 未核、失败、勘误及剩余边界

### P1–P3经典待核（不计新增）

- P1 Wald1945：身份确认、摘要未取得；F28。不能从教材或当代SPRT用法倒填经典定理条件。
- P2 Weitzman1979：RePEc身份／1978工作稿关联确认、摘要未取得；F45。没有越过出版限制，064／065后续作品不充当原作全文。
- P3 Russell/Wefald1989／1991：正式页HTTP400、作者概述可读；F08／F46。不将主题概述当该篇原文摘要，原PDF与版本仍交terra。

### 勘误与风险

- Q42没有返回明确AFABench勘误，只能说**本轮未定位**。W0311争议精确式不恢复；不把旧发现卡中的候选问题升为已证理论。
- 本轮没有执行W0059勘误搜索，避免重复主理论负责人工作；直接遵守红队停用其有反例均方误差论证。不将未搜索写成“无勘误”。
- 083中文综述返回开头有“全1代价矩阵退化错误率”的局部疑点，非本轮数学全文审计；只作成本分类／引文入口，交terra核查。取得原刊不等于其公式正确。
- F03摘要中“链推广多树”一句与困难度结论表述张力，F44开头显示应区分链可解／一般多树困难；原文精确定理交terra。没有自己证明所有复杂度结论。
- 087官方摘要所报新模型／性能、理论条件和标签成本均未读，不能由正式页面的存在性核验升级为结果背书。

### 非英语入口效果的实话

中文／日文／法文实际query已进入日志，但中文多次只返回英文预印本译介或非相关结果。最终3个非英语原始入口中两篇是综述、一项是博士论文机构介绍；**不声称已补全中文原始算法、跨语种评价或非英语证据消费**。不按作者姓名或机构地域推断语言。

### 检索边界

未无限重试：Q26仅一次同式重试，成功；F08不重试；F38导出路径404后停止该路径、用已能正常打开的原刊DOM核元数据，不绕拒绝。没有下载模型、执行论文代码、训练、提交、改总目录或上传内部文本。新发现文件不替换首轮历史日志，新增约束由EXPANSION_R2明确覆盖。

## 6. 交付核对

本轮只新增 `EXPANSION_R2.md` 与 `SEARCH_LOG_R2.md`。静态核对项：local ID056–088连续唯一、优先标记20、33主键与现目录无重复、查询Q01–45、FetchF01–47、UTF-8无替代字符、受限写入路径、限定目录Git状态。没有代码改动，pytest／项目构建／训练不能验证文献交付，故不运行；只读检查不生成脚本／缓存／测试日志。

最终静态验收：**PASS**。首次检查把目录实体数固定断言为384，实际读得385而中止；确认并发负责人新增W0385/HMT后，移除过时的固定数量断言、保留逐主键／题名去重检查，重跑通过：新增33、优先20、Q45、F47，中文6／日文2／法文1／英文36，当前目录385、重复主键0、UTF-8无替代字符。没有为通过检查改动其他代理文件。`git status --short -- <T07目录>`仅显示该未跟踪目录；`git diff --check`为空仅表示无已跟踪diff错误，不当作未跟踪内容已验收，实质检查来自上述文件解析。
