# 审计R1/R2/R3回目录的身份核销与引用门

当前台账定版2026-11-08 07:28:11 +0800：230唯一卡219FULL/11PARTIAL；身份与数学引用门不因读取升级改变，当前路径/范围以FINAL_ADDENDUM_INDEX为准。
快照：2026-11-08 05:20:47 +0800；只回填已核字段，未联网重取身份，不新增作品、不猜作者。

## 身份/版本字段的证据等级

- R1发现审计已核的H-MEM二作者、Beyond the Reranker前缀、LapMerge v2等现行规范保留；R1/R2/R3抽审只核样本，不代表全536项元数据已独立重查。
- 下表“独立审计”仅指相应报告锁定的原始页/作者字段；“证据卡”新增身份没有独立审计时明确次一级，冲突双记，不擅定谁错。理论审计分类不属于书目真伪认证。

| W-ID | 已回写字段 | 凭据及剩余 |
|---|---|---|
| W0152 | Jiayi Yao等（完整作者表本轮未得，不补猜）；arXiv:2405.16444v3；EuroSys2025；DOI10.1145/3689031.3696098 | [独立R2](../05_review/READING_AUDIT_R2.md)；[卡](../03_reading/B10/W0152.md)；目录未另核 |
| W0148 | Jiaming Tang、Yilong Zhao、Kan Zhu、Guangxuan Xiao、Baris Kasikci、Song Han；arXiv:2406.10774v2；页/词元预算单位不一致未擅修 | [独立R2](../05_review/READING_AUDIT_R2.md)；[卡](../03_reading/B11/W0148.md)；目录未另核 |
| W0316 | Nan Jiang、Lihong Li；ICML2016；PMLR48:652–661；正式补充A–D | [独立R2](../05_review/READING_AUDIT_R2.md)；[卡](../03_reading/B12/W0316.md)；目录未另核 |
| W0077 | Orion Weller、Michael Boratko、Iftekhar Naim、Jinhyuk Lee；arXiv:2508.21038v2；首页ICLR2026；固定正间隔不能省略 | [独立R2](../05_review/READING_AUDIT_R2.md)；[卡](../03_reading/B13/W0077.md)；目录未另核 |
| W0369 | John Hewitt、Percy Liang；EMNLP-IJCNLP2019，D19-1275；arXiv:1909.03368；正式页2733–2743 | [独立R2](../05_review/READING_AUDIT_R2.md)；[卡](../03_reading/B14/W0369.md)；目录未另核 |
| W0262 | Xuan Luo、Weizhi Wang、Xifeng Yan；arXiv:2503.23798v3，COLM2025；无普遍硬件/任务加速主张 | [独立R2](../05_review/READING_AUDIT_R2.md)；[卡](../03_reading/B15/W0262.md)；目录未另核 |
| W0217 | Ali Behrouz、Zeman Li、Praneeth Kacham、Majid Daliri、Yuan Deng、Peilin Zhong、Meisam Razaviyayn、Vahab Mirrokni；arXiv:2505.23735v1；原证明已读但不是容量定理已核准 | [独立R2](../05_review/READING_AUDIT_R2.md)；[卡](../03_reading/B16/W0217.md)；目录未另核 |
| W0328 | Tianhe Yu、Saurabh Kumar、Abhishek Gupta、Sergey Levine、Karol Hausman、Chelsea Finn；arXiv:2001.06782v4/NeurIPS2020及正式补充；A.3必要性限制见审计，不外推算法整体失败 | [独立R2](../05_review/READING_AUDIT_R2.md)；[卡](../03_reading/B16/W0328.md)；目录未另核 |
| W0334 | GuanWen Qiu、Da Kuang、Surbhi Goel；arXiv:2403.03375v3；B.1.5具体范围见审计；经验形成与理论常数分开 | [独立R2](../05_review/READING_AUDIT_R2.md)；[卡](../03_reading/B16/W0334.md)；目录未另核 |
| W0045 | Maxime Louis、Hervé Déjean、Stéphane Clinchant；Findings ACL2025 15506–15521；正式PDF首页48h、§3.2一天、落地页24h同版冲突；非仅预印本/正式版差异，不挑有利数字作训练成本排序 | [独立R3](../05_review/READING_AUDIT_R3.md)；[卡](../03_reading/B20/W0045.md)；目录未另核 |
| W0425 | Boris Motik、Ian Horrocks（所核arXiv v2作者，R3原文表及B19卡一致）；arXiv:1711.03987v2；原扩展曾列Pan Hu为首作者，与所核v2不符，主行规范为v2二作者；不自行解释来源原因或作者变更史 | [独立R3](../05_review/READING_AUDIT_R3.md)；[卡](../03_reading/B19/W0425.md)；目录未另核 |
| W0483 | Yiling Chen、Bo Waggoner；FOCS2016；arXiv:1703.08636v1（2017-03扩展稿）；R4已撤销R3错误解除；原印局部符号问题保留，可修复所核段，不反证强替代定理 | 身份由R3锁页继承；数学引用门由[最新R4](../05_review/READING_AUDIT_R4.md)取代旧R3；[卡](../03_reading/B17/W0483.md)；目录未另核 |
| W0471 | Sonia Horchidan、Fabian Zeiher、Henrik Boström、Paris Carbone；PVLDB19(1):29–42；PDF卷年2025；原Crossref印刷/在线/会议日期不同另存来源记录，不能单取2026称新作；算法/停止方向与实现未核 | [独立R3](../05_review/READING_AUDIT_R3.md)；[卡](../03_reading/B21/W0471.md)；目录未另核 |
| W0395 | Dong Hoon Lee、Seunghoon Hong；NeurIPS2024；arXiv:2412.10569v1；正文×0.1/附录÷0.1冲突，不能擅定实现 | [独立R3](../05_review/READING_AUDIT_R3.md)；[卡](../03_reading/B23/W0395.md)；目录未另核 |
| W0507 | ACL/Crossref正式五作者、正式PDF四作者缺Blair；arXiv2602.01672v3四作者另记 | R3§3.2及B18身份分版；不得将Blair倒填v3或自作唯一名单 |
| W0449 | PDF Denvy Deng vs ACL/arXiv Weiwei Deng并列 | B21原页记录、尚无独立审计核销；不解释同名/更名原因 |
| W0048 | v2完整主标题Compression Beyond the Uncompressed…、Shuyu Guo/Shuo Zhang/Zhaochun Ren | B24原PDF卡身份，非R3独立作者核验；当前完整阅读卡不等于表格逐行视觉核 |

## 争议引用门：供综合使用，不在目录重裁

| 对象 | 当前引用限制 | 唯一审计落点 |
|---|---|---|
| W0059 | 不用MSE二值失真/投影推步作理论基座；不能连带否定对数损失主结果 | READING_AUDIT_R1 §3.3 |
| W0091 | 不用字面不相容的多类端点/保序假设推出实际softmax无条件最优保证 | R1 §3.2 |
| W0108 | 定理2兼容条件与式37空区间分开；候选根修复不是作者勘误 | R1 §3.1 |
| W0311 | 精确最优/贪心闭式/增长率未核；只可带条件谈构造/可行策略，不说未证最优等于已证伪 | R1 §3.4 |
| W0210 | 部分段按m归一可作零填充矩，不称负方差/未来泄漏/实现错 | R1 §3.6 |
| W0083/W0313/W0217 | 理论继承/结构主界/容量修正版未闭合；R2定位的局部错误按范围引用 | R2 §3 R2-01/03/04 |
| W0328/W0334 | 暂停A.3必要性及所印ReLU范数常数；不否定算法和经验现象全部结果 | R2 §3 R2-05/06 |
| W0483 | R3该解除已被R4撤回：局部原印符号错、所核证明段可修；仍带先验/评分/条件独立前提，不反证整定理 | [最新R4 §0/§7](../05_review/READING_AUDIT_R4.md) / [限制导航](../05_review/CLAIM_RESTRICTIONS.md)；旧R3非现行解除 |
| W0471 | score/停止方向是算法—叙述不一致，实际实现尚未核；暂停精准成本/停止路径背书，保留向量平均FNR对象 | R3 §3 R3-03 |
| W0509/W0521 | v2摘要/正文方向冲突、图14“无none”prompt待核；不将拒答当遗漏证书 | R3 §3 R3-04/05；当前阅读范围另看READING_STATUS |
| W0045/W0395/W0012 | 同版24/48h、乘/除温度、CAB文表不一致；成本/实现/归因未闭合，不猜作者意图 | R3 §3 R3-06/07、§3.8 |

R3最前称“8篇抽审”但锁定表实际列9个W-ID（含B22两项）；本目录不把该计数口径用于作品/FULL数，也不越权改审计。综合引用应说“R3所列样本”，不要凭该标题推全量审查。


## 最新快照同步R5：覆盖红队R2及非数学核销

快照2026-11-08 05:53:34 +0800。已读COVERAGE_AUDIT_R2；它没有本轮外部身份新增核验，不把其综述再当独立作者认证。主目录保留已核H-MEM、W0156、LapMerge、HMT版本桥接；DeepControl五/四作者与MnemisDenvy/Weiwei继续双记未知。

- 534学术＝533论文/报告＋1博士论文，另2官方；当前220尝试及READING_STATUS状态不是覆盖报告05:12:51的183/17历史账。
- R3§4正文57/20/3，八行表相加59/19/2；§1称8篇而对象表9项，按COVERAGE_AUDIT_R2§1.3登记审计历史算术/范围问题，不改原审计、不据此抹掉逐项核查，也不把现行状态倒填旧时。
- W0423较晚技术稿加Tej Chajed、TODO证明与原v1四作者分版：只复用卡已取得原页记录和覆盖R2已读片段，不将新作者倒填v1、不把取得技术稿视作互递归证明已解决。
- PARTIAL的材料未取得、作者自有证明省略/TODO、已有材料尚未读完三因分别见OPEN_ITEMS；数学争议本轮未重新核销，W0483旧R3解除已被R4撤销，最新R4/限制导航优先。

## 最新R6：最终补读书目/类型与主张门

- 关系新7已分W0537–W0543，六实际卡路径不改；Slot论文正式/预印本别名一作，实际FULL版本以卡为准。RD07未全文，背景综述不入7。
- W0160固定报告Kimi K3: Open Frontier Intelligence与官方repo介绍归同实体，新增Git对象稳定别名不加W-ID；类型报告升级使旧官方2变纯官方1、学术＋1，非新作品发现。README同版/日期未知不补猜。
- 新近期四原卡对应既有W0157/58/59/60，NSA W0098只旧卡复核；原作者顺序和卡简写不一致、Taylor名字形式等保来源，目录不自推更名/新署名。
- 必须采用R4对R3的纠正：W0483局部符号仍错但所核段可修，旧“疑点完全解除”撤回；W0507 9.4/4.8是instruct/base，不擅归检索器变化。CRC端点前提用FINAL_RIGOR_REVIEW§2，不新增证明裁判。
