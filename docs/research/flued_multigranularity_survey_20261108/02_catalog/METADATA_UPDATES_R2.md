# R2元数据核销与来源边界

日期/快照：2026-11-08 03:54:19 +0800。只写02_catalog；复用已取得的审计/证据卡身份凭据，不新增外部检索或亲自精读。

## 可直接核销的确定书目项

| W-ID | 核销字段 | 凭据 | 状态/剩余 |
|---|---|---|---|
| W0111 | Haoran Sun、Shaoning Zeng；题名补H-MEM:前缀 | [发现A07](../05_review/DISCOVERY_AUDIT_R1.md)＋[覆盖§2.5](../05_review/COVERAGE_AUDIT_R1.md)＋[B02卡](../03_reading/B02/W0111.md) | 目录/旧批次名称已规范；本轮后续只读复查发现T03所有者也已修正源卡作者/题名前缀，目录未越权改源卡。旧错名仅作为本段历史错误记录：`Sheng Zeng`，不作为现行作者。 |
| W0156 | Beyond the Reranker:完整前缀；Sadanand Singh、Allam Reddy、Manan Chopra | [发现A11](../05_review/DISCOVERY_AUDIT_R1.md)＋B03卡 | 主键不变，短题保留为历史别名，不新增作品。 |
| W0030 | v2 2026-10-12及六作者 | [发现A02](../05_review/DISCOVERY_AUDIT_R1.md)原始提交史/Atom | 身份版本冲突已核销；正文v1/v2实质差异未读，后续全文入口钉v2。 |
| W0385 | HMT精确题名、五作者、v1 2024-05-09 | [覆盖§2.8](../05_review/COVERAGE_AUDIT_R1.md#L123) | 原目录主键/标题/别名查重无此ID，追加不重编号；仅审计v1定向正文，最新版本未核、未算精读。 |

## 发现审计28对象的身份字段回填

以下仅代表已有审计原始身份记录被目录复用；A15为仓库官方介绍，其余27为论文。完整作者能从审计取得者完整填，团队名单未全取得者继续明确不完整，不从From字段补人。

| 审计对象 | W-ID | 已回填作者 | 版本/状态边界 |
|---|---|---|---|
| A01 | W0012 | Pit Neitemeier、Alessio Serra、Jiaze Li、Sascha Wirges、Lukas Balles、Jan Hendrik Metzen | 2026-01-30；v1 |
| A02 | W0030 | Magdalena Trędowicz、Aleksandra Nowak、Tomasz Steifer、Łukasz Struski、Szymon Płotka、Jacek Tabor | v1 2026-10-09；v2 2026-10-12已由原始摘要史/Atom核销；正文版差仍待比 |
| A03 | W0050 | Minsu Oh、Seunghui Jwa、Chanjun Park、Yeo-Chan Yoon | 2026-10-14；v1 |
| A04 | W0059 | Yann Dubois、Benjamin Bloem-Reddy、Karen Ullrich、Chris J. Maddison | 2021-06-21首发；2022-01-28 v5；NeurIPS2021关联 |
| A05 | W0067 | Nicholas Stiles、Gregory W. Wornell | 2026-10-21；v1 |
| A06 | W0071 | Archish S、Mihir Agarwal、Ankit Garg、Neeraj Kayal、Kirankumar Shiragur | 2026-03-31；v1 |
| A07 | W0111 | Haoran Sun、Shaoning Zeng | 2025-07-23；v1；作者二人完整；H-MEM前缀按覆盖审计原文补齐 |
| A08 | W0138 | Kuang-Huei Lee、Xinyun Chen、Hiroki Furuta、John Canny、Ian Fischer | 2024-02-15首发；2024-07-22 v3 |
| A09 | W0139 | Howard Chen、Ramakanth Pasunuru、Jason Weston、Asli Celikyilmaz | 2023-10-08；v1 |
| A10 | W0142 | Hao-Lun Hsu、Nikki Lijing Kuang、Boyi Liu、Zhewei Yao、Yuxiong He | 2026-06-10；v1 |
| A11 | W0156 | Sadanand Singh、Allam Reddy、Manan Chopra | 2026-06-14；v1；题名前缀Beyond the Reranker已规范 |
| A12 | W0157 | DeepSeek-AI及作者团队（此处未列完整团队名单） | 原始页面及Atom均记v1=2026-04-26；2606编号与月份异常原因仍未知；HF模型页两次网络失败，模型卡未读 |
| A13 | W0158 | DeepSeek-AI及作者团队（此处未列完整团队名单） | 2026-09-17；v1；HTML读取仅至引言；HF模型页两次网络失败，不能称404或不存在 |
| A14 | W0159 | Qishuai Wen、Zhiyuan Huang、Xianghan Meng、Wei He、Chun-Guang Li | 2026-02-01 v1；2026-09-27 v6；NeurIPS2026为Atom备注，终稿轨道未独立核 |
| A15 | W0160 | MoonshotAI官方组织 | 仅README；commit/发布日期未固定、k3_tech_report.pdf未读；非论文实体 |
| A16 | W0203 | Yixiao Qian、Yaxin Zhang、Song Chen、Jiaxu Liu、Shengze Cai、Chao Xu | 2026-10-28；v1 |
| A17 | W0207 | Wanyun Cui | 2026-07-02；v1；B06只定向伴读，不计完整精读 |
| A18 | W0246 | Oliver Zahn、Matt Beton、Simran Chana | 2026-01-14首发；2026-02-04 v2；强正交主张仅作者摘要，不是已接受一般定理 |
| A19 | W0262 | Xuan Luo、Weizhi Wang、Xifeng Yan | 2025-03-31首发；2025-10-08 v3；COLM2025为官方元数据关联 |
| A20 | W0278 | Dezhen Lu、Runguo Li、Zixiang Ni、Yuchen Tang、Xingquan Kong、Jiaxing Yang、Jiarui Guo、Lingxiang Gao | 2026-11-03；v1 |
| A21 | W0287 | Kimi Team及Guangyu Chen、Yu Zhang、Jianlin Su等（本行非完整团队作者表） | 2026-03-16；v1 |
| A22 | W0308 | Jiaorong Feng、Qian Li、Ying Li | 2026-08-03；v1 |
| A23 | W0313 | Joseph Bingham | 2026-10-15；v1；证书和定理尚未独立验证 |
| A24 | W0337 | Aaditya K. Singh、Ted Moskovitz、Felix Hill、Stephanie C. Y. Chan、Andrew M. Saxe | 2024-04-10；v1 |
| A25 | W0339 | Chenyu Zhou、Yaqi Wu、Xiaolei Guo、Jiaqi Huang、Xianfa Zhang、Junxu Zhang、Zhuo Yu、Zhubo Shi、Jianghao Lin、Dongdong Ge | 2026-07-07首发；2026-08-22 v2；动作排序标签为一步支持召回代理，非轨迹Bellman值 |
| A26 | W0357 | Nicolás Vera Zúñiga | 2026-10-08；v1；同W0358一个相关证据簇 |
| A27 | W0358 | Nicolás Vera Zúñiga | 2026-10-15；v1；同W0357相同作者/项目仓库，不计独立复现；完整精读仍待排 |
| A28 | W0366 | Antonio Lopardo、Avyukth Harish、Catherine Arnett、Akshat Gupta | 2026-03-27；v1；ACL正式版关联本次审计未重核 |

## 证据卡新增书目字段（非目录独立认证）

B06卡声明用Atom/PDF补首作者，按卡元数据规范W0208 Ming Zhang、W0210 Hee Seung Hwang、W0212 Jianhai Zhang、W0237 Luke McDermott、W0229 Ke Alexander Wang；尤其W0212旧专题仅列Donghao不再作首作者定论。W0124按B03卡补When Your Agent Opens the Chat App前缀及作者；W0351补正式DOI和限定配置，W0169按卡记录Junaid Farooq。每行CATALOG都链接凭据并标“目录未另查”，有疑点由独立审计复核，不把卡当无误真值。

## 仍然不确定/不能核销为科学事实

- V4日期异常仍在原始页面/Atom复现，不自行改月份；V4/V4.1 HF模型页失败只表明当次未知，不写404/不存在。K3仍官方介绍、报告未读且未固定commit。
- HISA逐版局部阅读已存在，但AttentionIndex所比较实现/commit未钉，不能直接说v5已被反驳；MUVERA修正、MiTA逐版机制、PISCO48h/24h等仍待原文对齐。
- B05卡称W0358引用W0357并复用流水线/语料，支持暂保两作品、一相关证据簇；目录不据此独立判定替代/非替代，原生ID和计数均不合并。
- LoCoMo在H-MEM、HORMA的50对话/7512问与10会话/519题口径需要原作/派生文件消歧；只登记单位、划分、版本差异待核，不裁为造假或数据错误。
- B04等理论/统计疑点维持“阅读者提出、待独立核查”，不将卡片的反例、排版推测或代码解释升级成论文勘误。

## 原目录外扩展：不凑下一80篇

- HMT W0385从覆盖审计补录，放X001待锁最新版，不在原167中，所以不占B09–B16的80篇。当前385实体/383论文是新快照；旧419→384去重账仍成立。
- Geva/Berant2018 1806.03529、Bloom筛选、Neural Turing Machine/DNC/Memory Networks、数据库血缘/增量视图/双时间，以及中文/跨语种来源定位，仍属审计建议检索入口，不凭熟悉标题加已确认数。尤其1806.03529审计只看引用链，未独立摘要核，不当确认作品。
- 从原167只能调序而不能弥补原池没有的经典/中文文献。新80已优先生命周期、回退、同位预算、标签和全成本；F2/F3/F4经典桥接与F6中文真实检索仍需主代理安排检索代理，不伪称本轮已执行。

## 写入与历史记录

本轮不改01_search/03_reading/05_review、COORDINATION、源码或证据注册表。历史VALIDATION保留为R1快照并加R2索引；当前状态唯一入口是READING_STATUS。元数据修正不增作品，唯HMT明确追加1；不把已发生身份核销无限保持为未完成。


## 最新R3续轮：扩展入库与版本更新

快照2026-11-08 04:31:29 +0800；旧R2计数只作历史。当前533论文/报告、1博士论文、2官方介绍；120卡FULL117/PARTIAL3。详见COUNTS、READING_STATUS及EXPANSION_MERGE_R2。

- W0288：主标题`SATFormer: Learning When to Use Early Value Residuals in Transformers`；Skye Gunasekaran、Téa Wright、Rui-Jie Zhu、Jason Eshraghian；v3 2026-10-26；旧题Transformers with Selective Access to Early Representations为同ID别名。依据对应卡，非本目录独立外部重核。
- W0153：主标题`MemoRAG: Boosting Long Context Processing with Global Memory-Enhanced Retrieval Augmentation`；v1旧题Moving towards Next-Gen RAG…、作者Hongjin Qian/Peitian Zhang/Zheng Liu/Kelong Mao/Zhicheng Dou；v3 2025-04-09 WWW2025题名及作者变为Hongjin Qian、Zheng Liu、Peitian Zhang、Kelong Mao、Defu Lian、Zhicheng Dou、Tiejun Huang；两版卡均已补读，后版RLGF不倒填v1。依据对应卡，非本目录独立外部重核。
- W0380：主标题`Beyond Chunking: Discourse-Aware Hierarchical Retrieval for Long Document Question Answering`；v1题名DISRetrieval: Harnessing Discourse Structure for Long Document Retrieval，五作者Huiyao Chen、Yi Yang、Yinghui Li、Meishan Zhang、Min Zhang；v5 2026-05-07题名为本行，增Baotian Hu，v5完整作者顺序目录未补猜；卡已补读v1/v5，教师GPT-4o/mini口径疑点交红队。依据对应卡，非本目录独立外部重核。
- W0147：主标题`Look Back to Reason Forward: Revisitable Memory for Long-Context LLM Agents`；Yaorui Shi、Yuxin Chen、Siyuan Wang、Sihang Li、Hengxing Cai、Qi Gu、Xiang Wang、An Zhang；卡完整读v1 2025-09-27及v5 2026-03-02；v5首页ICLR2026，未穷尽逐版差分。依据对应卡，非本目录独立外部重核。
- W0083：主标题`Dynamic Tree Memory Representation for LLMs`；Alireza Rezazadeh、Zichao Li、Wei Wei、Yujia Bao；卡完整读v1 2024-10-17、v3 2025-03-19（首页ICLR2025）；两版同W-ID，理论转接疑点未独立核销。依据对应卡，非本目录独立外部重核。
- W0385 HMT：T03扩展已核v3/NAACL六作者/正式题含Efficient/DOI，保留v1五作者身份；合并不加实体，新进入B20。
- 所有新增作品保留作者未知、非标准DOI和保守簇备注；不把摘要/机构介绍当论文正文或独立效果证据。理论证据边界指向READING_AUDIT_R1，不在目录宣布新定理错误。


## 最新R4索引

本页以上为历史R2/R3记录，当前审计身份同步请以[AUDIT_METADATA_SYNC](AUDIT_METADATA_SYNC.md)和CATALOG为准；状态与后续以STATUS_AND_NEXT/READING_STATUS为准。R3对W0483的解除已被R4撤回，不可沿该旧结论传播。


## 当前R5状态索引

当前534学术＋2官方、220尝试以COUNTS/READING_STATUS为准；元数据及覆盖R2同步见AUDIT_METADATA_SYNC，分类欠账见OPEN_ITEMS。旧时态保留作历史，目录不进行新数学判词或新增精读批次。


## 最新最终补充入口

当前计数/编号以FINAL_ADDENDUM_INDEX、CATALOG、COUNTS/READING_STATUS为准；新RD7、同实体K3报告重分类与不改原卡路径的映射已明确。所有旧W0483“解除”句被R4撤回，旧文作历史不可再采；目录只维护索引，不独立判数学。
