# TCM Immuno-Oncology 数据库与计算资源指南

> 面向中药免疫抗肿瘤活性成分筛选研究的综合资源导航  
> 收录数据库、在线工具、软件包的访问地址与使用说明  
> 更新日期：2026-07

---

## 一、中药化学成分数据库

### 1.1 综合成分数据库

| 数据库 | 网址 | 化合物数 | 特点 | 引用 |
|--------|------|----------|------|------|
| **TCMSP** | https://tcmsp-e.com/ | 12,144 | 含ADME参数（OB、DL、Caco-2），支持药动学筛选 | Ru et al., J Cheminform, 2014 |
| **TCMIO** | https://tcmio.xielab.net/ | 13,390 | **免疫肿瘤学专用**，收录TCM-免疫靶点-通路关系 | Fan et al., Front Pharmacol, 2020 |
| **HERB** | http://herb.ac.cn/ | 49,258 | 本草组鉴，高覆盖度，链接文献证据 | Fang et al., Nucleic Acids Res, 2021 |
| **SymMap v2** | https://www.symmap.org/ | 22,000+ | 整合症状-中药-成分-靶点关联 | Wu et al., Nucleic Acids Res, 2022 |
| **ETCM v2** | http://www.tcmip.cn/ETCM/ | 30,000+ | 含中药复方数据，质控严格 | Zhang et al., J Ethnopharmacol, 2024 |
| **BATMAN-TCM** | http://bionet.ncpsb.org.cn/batman-tcm/ | 48,584 | 基于药理学的成分-靶点预测 | Kong et al., Sci Rep, 2017 |
| **TCM@Taiwan** | https://tcm.cmu.edu.tw/ | 60,000+ | 台湾中药数据库，化合物结构齐全 | Chen et al., J Cheminform, 2014 |

### 1.2 中药入血成分数据库（血清药物化学）

| 数据库 | 网址 | 说明 |
|--------|------|------|
| **DCABM-TCM** | https://www.bidd.group/DCABM-TCM/ | 中药吸收入血成分及代谢物数据库，含1,800+中药的体内成分 | Liu et al., J Chem Inf Model, 2023 |
| **TCM-ID** | https://bidd.group/TCMID/ | 中药入血成分及靶点信息 | Chen et al., Nucleic Acids Res, 2021 |

### 1.3 天然产物通用数据库

| 数据库 | 网址 | 化合物数 | 特点 |
|--------|------|----------|------|
| **NPASS** | https://bidd.group/NPASS/ | 35,000+ | 天然产物活性与靶点数据库，含IC50/Ki |
| **COCONUT** | https://coconut.naturalproducts.net/ | 400,000+ | 开源天然产物集合，适合虚拟筛选 |
| **SuperNatural II** | https://bioinf-applied.charite.de/supernatural_new/ | 326,000+ | 含药物相似性和毒性预测 |
| **CMAUP** | https://bidd.group/CMAUP/ | 47,000+ | 天然产物-靶点-疾病关联 |

---

## 二、免疫肿瘤学数据库

| 数据库 | 网址 | 用途 |
|--------|------|------|
| **TCGA** | https://portal.gdc.cancer.gov/ | 33种癌症多组学数据，用于靶点差异表达和预后验证 |
| **GEO** | https://www.ncbi.nlm.nih.gov/geo/ | 基因表达数据集，用于免疫相关基因筛选 |
| **TIMER 2.0** | http://timer.cistrome.org/ | 肿瘤免疫浸润分析，评估免疫细胞组成 |
| **TISIDB** | https://cis.jhu.edu/cti2017/TISIDB/ | 肿瘤-免疫系统相互作用数据库 |
| **ImmPort** | https://www.immport.org/ | 免疫学共享数据，含细胞因子、免疫细胞表型 |
| **TumorImmune** | https://bioc.xjtu.edu.cn/ | 肿瘤免疫微环境综合分析 |
| **DGIdb** | https://www.dgidb.org/ | 药物-基因相互作用，用于筛选免疫相关靶点 |
| **STRING** | https://string-db.org/ | 蛋白-蛋白相互作用网络，置信度评分 |
| **IMGT** | https://www.imgt.org/ | 免疫球蛋白/T细胞受体数据库 |

---

## 三、网络药理学与分析平台

| 工具 | 网址 | 功能 |
|------|------|------|
| **TCMNPAS** | http://www.tcmnpas.com/ | 中药网络药理学一体化分析 |
| **DAVID** | https://david.ncifcrf.gov/ | GO/KEGG富集分析 |
| **Metascape** | https://metascape.org/ | 基因功能注释与富集分析 |
| **Cytoscape** | https://cytoscape.org/ | 网络可视化与分析（核心插件：cytoHubba、MCODE） |
| **KOBAS-i** | https://kobas.cbi.pku.edu.cn/ | KEGG/GO富集分析 |

---

## 四、分子对接与虚拟筛选工具

### 4.1 分子对接软件

| 软件 | 类型 | 网址 | 说明 |
|------|------|------|------|
| **AutoDock Vina** | 免费 | https://vina.scripps.edu/ | 学术界标准，速度与精度均衡 |
| **AutoDock 4** | 免费 | https://autodock.scripps.edu/ | 含柔性对接，适合精确计算 |
| **CB-Dock 2** | 在线 | https://cadd.labshare.cn/cb-dock2/ | 自动识别结合口袋，适合初学者 |
| **SwissDock** | 在线 | http://www.swissdock.ch/ | 基于EADock DSS，网页操作 |
| **GNINA** | 免费 | https://github.com/gnina/gnina | 基于CNN的深度学习对接评分 |

### 4.2 ADMET/成药性预测

| 工具 | 网址 | 功能 |
|------|------|------|
| **SwissADME** | http://www.swissadme.ch/ | 药动学参数预测（GI吸收、BBB穿透、P-gp底物） |
| **ADMETlab 2.0** | https://admetmesh.scbdd.com/ | 综合ADMET预测（40+参数） |
| **ProTox-II** | https://tox.charite.de/ | 毒性预测（LD50、肝毒性、细胞毒性） |
| **pkCSM** | https://biosig.lab.uq.edu.au/pkcsm/ | 药动学特性预测 |

### 4.3 蛋白结构资源

| 资源 | 网址 | 说明 |
|------|------|------|
| **PDB (RCSB)** | https://www.rcsb.org/ | 蛋白晶体结构（PD-1、PD-L1、CTLA-4等免疫靶点） |
| **AlphaFold DB** | https://alphafold.ebi.ac.uk/ | AI预测蛋白结构，替代实验结构 |
| **UniProt** | https://www.uniprot.org/ | 蛋白序列与功能注释 |

---

## 五、机器学习与AI药物发现工具

| 工具/平台 | 类型 | 应用场景 |
|-----------|------|----------|
| **DeepDR** | 深度学习 | 药物反应预测，已集成于 LLM/ 目录 |
| **Biomni** | LLM + RAG | 生物医学推理，支持RAG检索，已集成 |
| **DeepPurpose** | 深度学习 | 药物-靶点相互作用预测 |
| **DiffDock** | 扩散模型 | 基于扩散的分子对接，超越传统打分 |
| **ChemBERTa-2** | 预训练模型 | 分子SMILES表示与性质预测 |
| **MegaMolBART** | 生成式AI | 基于Transformer的分子生成 |

---

## 六、编程工具栈推荐

### Python 数据科学栈

```python
# 核心数据处理
pandas, numpy, scipy          # 数据处理与统计
scikit-learn                   # PCA, OPLS-DA 多变量分析
matplotlib, seaborn            # 数据可视化
plotly                         # 交互式图表

# 化学信息学
rdkit                          # 分子描述符、指纹、化学子结构
openbabel                      # 化学文件格式转换
meeko                          # 分子对接预处理（AutoDock Vina）
prody                          # 蛋白质结构分析

# 生物信息学
biopython                      # 序列分析、PDB 操作
gseapy                         # GO/KEGG 富集分析
```

### R/Bioconductor 包

```r
clusterProfiler                # GO/KEGG 富集分析
STRINGdb                       # PPI网络
igraph                         # 网络拓扑分析
CIBERSORT                      # 免疫细胞组分估算
ESTIMATE                       # 肿瘤纯度/免疫/基质评分
GSVA                           # 通路活性评分
ropls                          # PCA, PLS-DA, OPLS-DA
mixOmics                       # 多组学整合
```

---

## 七、关键数据库快速访问表

| 需求场景 | 推荐数据库/工具 | 优先级 |
|----------|----------------|--------|
| 中药化合物获取 | TCMSP -> HERB -> ETCM | 五星 |
| 免疫肿瘤靶点关联 | TCMIO -> TISIDB | 五星 |
| 入血成分查找 | DCABM-TCM | 四星 |
| 成分ADME筛选 | SwissADME -> ADMETlab | 五星 |
| 靶点预测 | BATMAN-TCM -> STITCH | 五星 |
| 网络构建 | Cytoscape + STRING | 五星 |
| 富集分析 | Metascape -> DAVID -> clusterProfiler | 五星 |
| 分子对接 | AutoDock Vina -> CB-Dock 2 | 五星 |
| 免疫浸润分析 | TIMER 2.0 -> CIBERSORT | 四星 |
| 临床验证 | TCGA -> GEO | 五星 |

---

## 附录：数据库选择决策树

```
中药免疫抗肿瘤活性成分筛选
│
├─ 需要化合物成分列表？ -> TCMSP / HERB / ETCM
├─ 需要ADME筛选？ -> SwissADME (OB>=30%, DL>=0.18)
├─ 需要预测靶点？
│   ├─ 单成分多靶点 -> SwissTargetPrediction / STITCH
│   └─ 多成分多靶点 -> BATMAN-TCM / TCMNPAS
├─ 需要免疫相关靶点？ -> TCMIO -> TISIDB
├─ 需要通路分析？
│   ├─ GO/KEGG -> DAVID / Metascape / clusterProfiler
│   └─ 免疫通路 -> KEGG (hsa04660 T cell receptor signaling)
├─ 需要分子对接验证？
│   ├─ 结构可用 -> AutoDock Vina
│   ├─ 无已知结构 -> AlphaFold
│   └─ 快速评估 -> CB-Dock 2
│
└─ 需要实验验证？
    ├─ 体外免疫激活 -> 本仓库的三重筛选体系
    └─ 体内 -> 荷瘤小鼠模型
```
