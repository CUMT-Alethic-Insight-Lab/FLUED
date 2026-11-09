# 03_ADDRESS_READOUT：定向发现与来源核验日志

日期：2026-11-08；sol。公开检索仅发送机制词、公开题名/ID，不发送FLUED内部内容。本轮没有使用付费数据源或数据源插件，没有上传材料、安装软件或运行论文代码。

## 1. 检索策略与计数

不是追求新增篇数；围绕六个能改变解释的问题查找：内容/位置寻址、K/V非对称压缩、query输入权限、独立读出、多种秩瓶颈、跨层KV共享。经典线用NTM/D-NTM补地址和训练可达；反例线查归一化/稀释、已训状态可剪枝；最近线查2026 token维多头与值侧重组织。

**实际9条查询**：3条内置浏览器Bing检索并读渲染结果，6条WebSearch。搜索结果中的自动生成概括不作为论文证据，特别不采用Bing将DNC概括为“self-attention扩展”等措辞。实际引用均继续取公开原站。

**FetchURL共16次请求，15次成功，1次临时失败**；15个不同URL，其中失败URL已重试成功。获取长HTML不等于全文精读，本轮只做下列身份/方法定向核验。涉及9个论文实体；相对当前CATALOG，6项真新增候选、3项已入目录未读；新增原文FULL为0。没有对全部检索结果做穷尽编目。

## 2. 查询逐条记录

| 编号 | 实际工具与原样查询 | 有区分力结果及处理 |
|---|---|---|
| Q01 | 内置浏览器Bing：`Neural Turing Machines content location addressing differentiable neural computer memory 2014 2016` | 命中1410.5401；继续读NTM原站§3；DNC仅发现线索，未取其原文、不加入新增计数 |
| Q02 | 内置浏览器Bing：`attention key value cache compression independent keys values AsymKV 2025 2026` | 命中2506.05410；只采原文§3.1–3.2条件性等价，拒绝自动摘要“全部压缩无损”式省略 |
| Q03 | 内置浏览器Bing：`2026 linear attention token level multi head state reduction rank Dual DeltaNet` | 命中2610.38578与MHLA官方入口；CATALOG分别为W0203、W0219，不计新作 |
| Q04 | WebSearch：`"Cross-Layer Attention" "Reducing Transformer Key-Value Cache"` | 2405.12981，新增；区别跨层共享同一KV与AttnRes/Depth-Attention混合旧输出 |
| Q05 | WebSearch：`"Perceiver IO" output queries latent bottleneck` | 2107.14795及作者公开PDF；继续取arXiv摘要/HTML，核输出query内容与位置/任务信息。不是把W0107 Perceiver改名重算 |
| Q06 | WebSearch：`"Homogeneous Keys, Heterogeneous Values" AsymKV` | 固定v2 2506.05410、作者与代码线索；代码未打开/运行，正式NeurIPS录用仅按Atom备注标记 |
| Q07 | WebSearch：`"Neural Turing Machines" content location addressing` | 命中NTM与1607.00036 D-NTM；后者原文§4.3关于忽略内容、只用地址的病态解是高价值反例 |
| Q08 | WebSearch：`"Restoring Expressivity of Linear Attention via Token-Level Multi-Head"` | 2601.07832v1/v2；已入W0219未读。取v2 §4并查到块位置混合系数；未宣布当前输入动态产生该系数 |
| Q09 | WebSearch：`"linear attention" "dilution" "normalization" TransNormer` | 命中The Devil in Linear Transformer，2210.10340/EMNLP2022正式版；核原站摘要、作者与论文入口，证明及实验未精读 |

W0086的2602.04852来自已有目录，随后直接取v3摘要核验，不计第10条搜索。Q03–Q09命中的综述、博客、聚合页面未用作机制/结论的最终凭据。

## 3. 六项真新增候选：身份、原文版本和本轮读取范围

本地A01–A06仅为本审计引用编号，不创建W-ID，不改原目录。稳定ID及题名双重去重：对CATALOG检索6个arXiv ID及题名/方法别名；均无对应作品行。Perceiver IO只出现于W0107备注“不与Perceiver IO合并”，不是已编目的独立实体。

### A01：Neural Turing Machines

- 作者核验：Alex Graves、Greg Wayne、Ivo Danihelka；arXiv Atom作者栏实取，不把From联系人当完整作者。
- 固定版本：[1410.5401v2 PDF](https://arxiv.org/pdf/1410.5401v2)，v1 2014-10-20，v2 2014-12-10。
- 实际获取并读：[v2 HTML](https://arxiv.org/html/1410.5401v2) §3.1–3.4、§4.1及部分§4.2；摘要/版本史另取abs。Fetch文本停在后续实验，未读全篇，不计FULL。
- 核到：每头归一化权重读槽；擦除/增加分离；内容匹配、前一步位置权重、平移、锐化联合寻址；控制器类型与同时读取头数决定不同计算限制。
- 适用边界：合成序列算法、固定有限内存，不是任意自然语言记忆保证；位置式寻址不等原文回访。

### A02：Dynamic Neural Turing Machine with Soft and Hard Addressing Schemes

- 作者核验：Caglar Gulcehre、Sarath Chandar、Kyunghyun Cho、Yoshua Bengio，Atom与HTML首页一致。
- 固定版本：[1607.00036v2 PDF](https://arxiv.org/pdf/1607.00036v2)，v1 2016-06-30、v2 2017-03-17。arXiv元数据题名为Soft and Hard；[v2 HTML](https://arxiv.org/html/1607.00036v2)首页为Continuous and Discrete Addressing Schemes。记录同ID版内题名差，不拆作品。
- 实际读：HTML §2–4、§6.1–6.3及表1；返回在§6.4截断，后续实验未读，不计FULL。
- 核到：固定可训练地址分区与可写内容分区；训练/推理对地址分区权限不同；连续/离散寻址、多步读取、REINFORCE和课程训练。§4.3明确报告模型可把地址当附加权重矩阵而忽略内容，提出读写一致性正则。
- 反例边界：这说明“有记忆模块也可能不消费其动态内容”，不证明FLUED发生同一病因。§6显示D-NTM仍落后MemN2N/DMN+，不同对照训练与任务配置应精读，不包装成普遍成功。

### A03：Homogeneous Keys, Heterogeneous Values: Exploiting Local KV Cache Asymmetry for Long-Context LLMs（AsymKV）

- 作者：Wanyun Cui、Mingwei Xu，HTML与Atom双核。
- 固定版本：[2506.05410v2 HTML](https://arxiv.org/html/2506.05410v2)、[PDF](https://arxiv.org/pdf/2506.05410v2)，v1 2025-06-04、v2 2025-11-06；Atom备注Accepted by NeurIPS2025，未另核会议正式页。
- 实际读：摘要、§3.1–3.2全文公式与少量§4.6描述；长返回保存于工具缓存后定位读取，未通读实验和附录，不计FULL。
- **已核关键条件**：先把两原键替为相同k*，之后才可对两value求和，用cardinality修正softmax分母，保持该“等键替换后”注意力输出。对原始不同key的替换本身仍近似。
- §3.1还明确用对角Fisher近似Hessian，并为稳定删除梯度项。故不能写“无训练参数所以无需构建梯度计算”，也不能把摘要lossless扩写成任意K/V或内容重建无损。
- 对本轴：这是广播重复计数/值聚合最直接的新原始公式参照，无需引入多粒度回访。

### A04：Reducing Transformer Key-Value Cache Size with Cross-Layer Attention（CLA）

- 作者：William Brandon、Mayank Mishra、Aniruddha Nrusimha、Rameswar Panda、Jonathan Ragan Kelly（Atom拼写）；HTML提取漏首名，已用Atom补核。
- 固定版本：[2405.12981v1 HTML](https://arxiv.org/html/2405.12981v1)、[PDF](https://arxiv.org/pdf/2405.12981v1)，2024-05-21。
- 实际读：摘要、§2.1–2.3和表格开头；没有读全部训练对照/附录，不计FULL。
- 核到：只有部分层计算K/V，其他层用先前层KV，不是把多个层写进一个摘要。可与MHA/GQA/MQA组合；减少独立KV层数。
- 重要反例：§2.3明确共享KV仍被每个层分别从主存重读，因此不直接减少核心注意力decode带宽/延迟。少存不等少读，跨pipeline还需通信。

### A05：Perceiver IO: A General Architecture for Structured Inputs & Outputs

- 作者身份核验来自成功的arXiv摘要页：Andrew Jaegle首作，Sebastian Borgeaud等共15名；HTML提取漏Jaegle，未据漏名改作者顺序。
- 固定版本：[2107.14795v3 HTML](https://arxiv.org/html/2107.14795v3)、[PDF](https://arxiv.org/pdf/2107.14795v3)，v1 2021-07-30、v3 2022-03-15。
- 首次abs Fetch网络失败；原URL仅重试1次成功，不使用登录或任何绕过。随后取官方HTML。
- 实际读：§3.1–3.2及Figure3文字，未通读实验/附录，不计FULL。
- 核到：输出query可由位置编码、任务/模态嵌入、目标位置输入特征或学得固定向量构造；不同输出独立查询同一latent数组。**query携带的信息是实验权限的一部分**，不能把所有结果归压缩latent本身。
- 边界：不是在线无限历史的任意未来query记忆，字节语言理解也不代证FLUED长程因果生成。

### A06：The Devil in Linear Transformer（TransNormer）

- 正式作者：Zhen Qin、Xiaodong Han、Weixuan Sun、Dongxu Li、Lingpeng Kong、Nick Barnes、Yiran Zhong；来自ACL正式元数据。
- 固定正式版：[EMNLP2022 2022.emnlp-main.473](https://aclanthology.org/2022.emnlp-main.473/)、[PDF](https://aclanthology.org/2022.emnlp-main.473.pdf)，7025–7041，DOI 10.18653/v1/2022.emnlp-main.473。关联arXiv2210.10340，未逐版比较。
- 本次仅读正式摘要/书目；原证明和实验尚未读，不计FULL。
- 作者原始摘要明确把无界梯度与注意力稀释分列，提出归一化替换缩放及早层对角局部注意。它提供需要查证的训练/读出替代机制，**不是本审计已验证的梯度定理**。

## 4. 三项已入但未读：不得重算“新增”

| 对应ID | 本次原始来源与读取范围 | 漏洞类型/下一步 |
|---|---|---|
| W0219 MHLA | [2601.07832v2 HTML](https://arxiv.org/html/2601.07832v2)，摘要与§4.1–4.2、部分因果分块说明；Atom核作者Kewei Zhang、Ye Huang等8人，版本2026-01-14 | **漏读/尚不能充分综合**。按token块“头”计算局部summary，再用块索引系数矩阵混合；§4.2是可学习矩阵、位置局部性初始化，并非明确每步由输入动态生成。需核附录因果推理/混合成本，不能照抄引言query-adaptive为已分离动态query |
| W0203 Dual DeltaNet | [2610.38578v1摘要](https://arxiv.org/abs/2610.38578v1)，2026-10-28，Atom作者Yixiao Qian等6人 | **漏读**。摘要称key侧修正+value侧重组织；理论/效果未核，不直接借其“strongest overall”作裁决 |
| W0086 On State Reduction | [2602.04852v3摘要](https://arxiv.org/abs/2602.04852v3)，2026-09-29；作者首名Philipp Nazari沿目录，返回未给完整作者栏，不补全未核名单 | **漏读**。训练后状态低秩与剪枝提供“状态大而未用满”的反例方向，不等于把任何任务依赖的秩砍半均安全 |

另：本轮15张已读卡中W0229/W0212/W0204/W0214的相关机制已被旧综合部分采用，不能说完全漏综合；应改变其在总框架的位置，而非重新发现。W0287/W0289的跨层读出也已有原证，但原综合用“不是回访”作差异终点，尚未充分围绕封闭记忆可用性展开。

## 5. Fetch请求清单与未核验范围

请求顺序分组；每项一次，唯注明重试者两次：

1. `https://arxiv.org/html/1410.5401v2` 成功。
2. `https://arxiv.org/abs/1607.00036` 成功。
3. `https://arxiv.org/html/2506.05410v2` 成功，长内容工具缓存后局部读。
4. `https://arxiv.org/html/2405.12981v1` 成功，长内容局部读。
5. `https://arxiv.org/abs/2107.14795` 首次网络失败；同URL重试一次成功。
6. `https://arxiv.org/html/2601.07832v2` 成功，长内容局部读。
7. `https://aclanthology.org/2022.emnlp-main.473/` 成功。
8. `https://arxiv.org/abs/1410.5401` 成功。
9. `https://arxiv.org/abs/2405.12981` 成功。
10. `https://arxiv.org/abs/1607.00036v2` 成功。
11. `https://arxiv.org/abs/2610.38578v1` 成功。
12. `https://arxiv.org/abs/2602.04852v3` 成功。
13. `https://arxiv.org/html/2107.14795v3` 成功，长内容局部读。
14. `https://arxiv.org/html/1607.00036v2` 成功，返回实验后部截断。
15. [公开arXiv Atom元数据](https://export.arxiv.org/api/query?id_list=1410.5401,1607.00036,2405.12981,2506.05410,2601.07832,2610.38578&max_results=6) 成功；一次返回6实体身份/版本，用于补HTML抽取漏首作者。它是公开原站HTTP端点，不是数据源插件查询。

本轮未遇403/登录/付费拒绝；未读完整DNC、Hopfield、Slot Attention原文，没有认证全部新作的证明、正式会议版差、代码版本或实测速度。官方原文可达并不等于本次全文已读。没有把合法公开来源的临时失败解释成作品不存在。

## 6. 交付验证

使用本机 `python` 只读脚本验证：三份Markdown均可按UTF-8读取；26个本地Markdown链接全部指向存在文件；审计样本表确为15张（13 FULL/2 PARTIAL）；推荐表序号1–12完整且不重复。另一次脚本核得目录543个唯一W-ID、230条状态及其卡存在/开头声明相容，6个新增稳定ID无目录命中。文档任务未运行训练、项目测试或论文复现。没有修改旧目录、卡、综合、源码、证据表或术语表；未提交。浏览器提示现有标签超过10个会使侧栏拥挤；仅关闭了本轮创建的Q01标签，Q02/Q03检索标签仍为后台，未操作其他会话标签。
