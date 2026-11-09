# R1–R4 主张限制｜综合者一页导航

2026-11-08。入口：[R1](READING_AUDIT_R1.md)／[R2](READING_AUDIT_R2.md)／[R3](READING_AUDIT_R3.md)／[R4](READING_AUDIT_R4.md)。**这是句子级引用限制，不是文献黑名单；局部证明缺口/反例不使机制与实验整体无效。** FULL是阅读范围，不是正确性/复现认证；PARTIAL/BLOCKED缺口不得用摘要或其它版本填平。

> **纠错优先：R3错误解除了W0483疑点，不能沿用。** 正确价值边际是`+I(E;B|A)`；原印符号有误，但该证明段可修复，不是定理反例。R3还把W0507的base/instruct差误解释为检索器变化；R3台账应为59/19/2、抽审9篇。详情及依据见[R4 §0/§7](READING_AUDIT_R4.md)。

## 1. 不可直接采用的强保证

| 卡与原文 | 综合者不能写成／允许保留 |
|---|---|
| [W0059](../03_reading/B04/W0059.md) [v5 B.5–6](https://arxiv.org/pdf/2106.10800v5) | 禁“均方误差失真只能0或B²”“任意损失同一保证”；仅否定所印投影/二值推步，**不连坐对数损失**；见R1。 |
| [W0091](../03_reading/B04/W0091.md) [v2 B.2/C.5](https://arxiv.org/pdf/2009.12789v2) | 禁“一般softmax族无条件保证所有ERM最优”；端点严格保序假设不相容，不能与全族有界log loss拼接；定义/实验另论。 |
| [W0083 MemTree](../03_reading/B09/W0083.md) [v3 B](https://arxiv.org/pdf/2410.14052v3)；[W0217 Atlas](../03_reading/B16/W0217.md) [v1 C](https://arxiv.org/pdf/2505.23735v1) | 禁“摘要阈值自动继承β/3”“原始键线性独立仍因加深获得超线性独立键数”；是转接/秩论证问题，构树与滑窗回归实验仍可限定引用。 |
| [W0328 PCGrad](../03_reading/B16/W0328.md) [v4 A.3](https://arxiv.org/pdf/2001.06782v4)；[W0334](../03_reading/B16/W0334.md) [v3 B.1.5](https://arxiv.org/pdf/2403.03375v3) | 禁A.3“必要性”及B.1/B.2所印小范数保证，R2有具体反例；不推成梯度手术或特征形成实验全无效。 |
| [W0313](../03_reading/B12/W0313.md) [v1命题21](https://arxiv.org/pdf/2610.21919v1)；[W0311](../03_reading/B07/W0311.md) [v3 F](https://arxiv.org/pdf/2508.14734v3) | 禁“γ→1贪心缺口趋零”；其e^−γ主界仍待核。AFABench精确最优/贪心常数未独立核定，3.25只可作给定策略上界；不是多步价值不存在。 |
| [W0534](../03_reading/B26/W0534.md) [v2 E.1/E.4 pp.45–46](https://arxiv.org/pdf/2311.17030v2) | 禁“四互异内积保持普遍保证可分”“高R²保证所有MLP都幻象”；R4四点反例只击中字面引理，正文零空间+休眠构造/实验保留。 |

## 2. 必须条件化、分版本或分指标

| 卡与原文 | 引用条件／暂停哪句话 |
|---|---|
| [W0108](../03_reading/B04/W0108.md) [正式式37](https://isl.stanford.edu/~cover/papers/transIT/0269equi.pdf)；[W0152](../03_reading/B10/W0152.md) [v3 A](https://arxiv.org/pdf/2405.16444v3) | 不传播空选点区间/漏sin展开；分别保留条件化马尔可夫细化与正确旋转性质；细增量须源端可见，位置校正不补跨块依赖。 |
| [W0169](../03_reading/B03/W0169.md) [v1表6/7](https://arxiv.org/pdf/2608.21610v1) | `.27/.420`并列，未显著≠等效；p=.040且CI跨零不证明所有bootstrap不合法；LLM calls=0不等完整冷建免费。 |
| [W0210 Merlin](../03_reading/B06/W0210.md) [v1式7–12/C.5](https://arxiv.org/pdf/2610.37645v1) | 当前未满段固定m是零填充矩，不是已见r项精确经验矩；两softmax混合不是单softmax恒等展开；总多状态缓存入账。 |
| [W0077](../03_reading/B13/W0077.md) [v2 §3](https://arxiv.org/pdf/2508.21038v2)；[W0061](../03_reading/B04/W0061.md) [v2 §2](https://arxiv.org/pdf/2402.01032v2) | 固定正间隔/全子集下界与均匀单遍整串复制计数不能裁决任意单槽、自然语料或外存交互回访；训练失败≠不存在。 |
| [W0471 ConANN](../03_reading/B21/W0471.md) [正式式9/算法2](https://www.vldb.org/pvldb/vol19/p29-horchidan.pdf) | score方向与`<`停止仍待实现核；只报向量精确top-L的**分布平均**FNR目标和限定实测，不称每题/语义证据保证；未证实验全错。 |
| [W0507](../03_reading/B18/W0507.md) [正式表1/10](https://aclanthology.org/2026.findings-emnlp.52.pdf) | 9.4pp是instruct基线、4.8pp是base/E5；训练可见金标、两层主接口、额外墙钟要写明；ACL/PDF作者人数差未解。 |
| [W0509](../03_reading/B22/W0509.md) [v2正文/H](https://arxiv.org/pdf/2606.14122v2)；[W0521](../03_reading/B22/W0521.md) [v3 B](https://arxiv.org/pdf/2503.01996v3) | UTF-8“common/rare谁高”摘要与详细结果冲突，不混结构合法/字符准确。Figure14“无none”真实提示未核，不以拒答作为漏召回证书。 |
| [W0395 DTEM](../03_reading/B23/W0395.md) [v1 §4.1/A.2](https://arxiv.org/pdf/2412.10569v1)；[W0045 PISCO](../03_reading/B20/W0045.md) [正式pp.1/4](https://aclanthology.org/2025.findings-acl.800.pdf) | ×/÷.1温度实现未核；24h/48h是成本叙述冲突，**不是测得预算区间**。可报模型/任务/硬件限定结果，不排完整成本名次。 |
| [W0012 SOMBRERO](../03_reading/B24/W0012.md) [v1表1/2](https://arxiv.org/pdf/2601.22805v1) | CAB `.6701→.6640`差`.0061`仍为改善，不沿用正文`.037`；高边界富集≠高BPB性能、因果效用或源回访。 |
| [W0510 MAGNET](../03_reading/B26/W0510.md) [v2图3/表3/6](https://arxiv.org/pdf/2407.08818v2)；[W0514 LOBEF](../03_reading/B26/W0514.md) [v3脚注5/表10](https://arxiv.org/pdf/2205.11490v3) | 同名平均值不一致/四层最优不获德英表支持；只报定位表值，保留脚本ID/单脚本/Moses词界权限；同epoch不是同FLOPs/墙钟。 |
| [W0524 MIRACL](../03_reading/B26/W0524.md) [正式式3](https://aclanthology.org/2023.tacl-1.63.pdf) | 印式除k是precision形式，不能拿来解释Recall；标准后端除全部已标相关项，历史run未复现；池化漏标、同语检索与下游消费分开。 |
| [W0466](../03_reading/B25/W0466.md) [§4/表2](https://www.vldb.org/conf/2007/papers/research/p950-lv.pdf)；[W0424](../03_reading/B25/W0424.md) [§3.4/5](https://www.cidrdb.org/cidr2013/Papers/CIDR13_Paper111.pdf) | 桶概率近似/全内存省表不等于总读省；偏序差分重建不等于神经摘要可逆/撤销全传播/物理擦除；B25其余PARTIAL仍按原读者补读。 |

## 3. 已解除的范围，以及不能误写成“全部解除”的项

- **确认而非反转**：[ByT5 W0351卡](../03_reading/B08/W0351.md)、[Large公开配置](https://storage.googleapis.com/t5-data/pretrained_models/byt5/large/operative_config.gin)：仅该配置输入两端共享、输出头不绑；不是全家族/全部权重核验（R1）。
- **版本差疑虑局部解除**：[W0523卡](../03_reading/B26/W0523.md)、[ACL v1](https://aclanthology.org/2025.emnlp-main.1161v1.pdf)→[v3](https://aclanthology.org/2025.emnlp-main.1161v3.pdf)：文本差主要作者排序；arXiv早版表号/叙述另有变化。仍禁“归因oracle=部署源消费上界”（R4）。
- **评分部分未知解除**：[W0528卡](../03_reading/B26/W0528.md)、[固定官方补丁](https://github.com/yahoojapan/JGLUE/blob/7ad8b36b4d74c4e8b0ed37dc48c576d3a490058d/fine-tuning/patch/transformers-4.9.2_jglue-1.3.0.patch)：码点Counter-F1、lower/空白/句号处理已静态核；无NFC/字素/byte一致性保证，不解除训练跨度错位（R4）。
- **不得沿用R3解除**：[W0483卡](../03_reading/B17/W0483.md)、[原文定理5.3.1 p.43](https://arxiv.org/pdf/1703.08636v1)：局部符号错保留，正确链式法则可修复所核证明段；不以此说强替代定理失败，也不说原印式正确（R4 §7）。

**共同合同：** 内容存在→可训练提取→指定族可读→部署自然消费不是同一命题；原源/索引/载荷/缓存、构建/训练/更新、冷/热I/O/重算与尾延迟须共同计费；token/视觉/外部文本证据不直接给FLUED byte接口免责。上述导航限制到实际核查版本及局部，未报告成本不等于零，局部证明反例不等于机制实验全无效。
