# 19味候选中药化合物-免疫活性数据库

> 本仓库19味候选中药的化学成分、免疫调节活性、抗肿瘤效应综合数据集  
> 数据来源：TCMSP、HERB、TCMIO、PubMed文献  
> 2026年7月更新

---

## 一、总览

| 序号 | 中药 | 拉丁名 | 主要免疫活性成分数 | 已知免疫靶点 | 免疫作用方向 |
|------|------|--------|------------------|-------------|-------------|
| 1 | 苏木 | Caesalpinia sappan | 8 | NF-kB, TLR4 | 抗炎+免疫激活 |
| 2 | 蒲公英 | Taraxacum mongolicum | 10 | NLRP3, PD-L1 | 抗炎+免疫调节 |
| 3 | 金银花 | Lonicera japonica | 12 | TLR4, NF-kB | 抗炎+免疫增强 |
| 4 | 鱼腥草 | Houttuynia cordata | 9 | NF-kB, MAPK | 抗炎+免疫激活 |
| 5 | 夏枯草 | Prunella vulgaris | 7 | NK, Macrophage | 免疫增强 |
| 6 | 马齿苋 | Portulaca oleracea | 6 | Macrophage | 免疫调节 |
| 7 | 厚朴 | Magnolia officinalis | 5 | STAT3, PD-L1 | 免疫检查点调控 |
| 8 | 茜草 | Rubia cordifolia | 7 | T/B cell | 免疫激活 |
| 9 | 白芍 | Paeonia lactiflora | 6 | NF-kB | 抗炎 |
| 10 | 桔梗 | Platycodon grandiflorus | 5 | TLR4, MAPK | 免疫激活 |
| 11 | 白屈菜 | Chelidonium majus | 6 | NF-kB | 抗炎+细胞毒 |
| 12 | 两面针 | Zanthoxylum nitidum | 5 | STAT3 | 抗炎+逆转耐药 |
| 13 | 乌药 | Lindera aggregata | 4 | NF-kB | 抗炎 |
| 14 | 地榆 | Sanguisorba officinalis | 6 | T cell | 免疫增强+止血 |
| 15 | 蔓荆子 | Vitex trifolia | 5 | Macrophage | 免疫调节 |
| 16 | 桑白皮 | Morus alba | 8 | NF-kB | 抗炎 |
| 17 | 鬼针草 | Bidens bipinnata | 6 | Macrophage | 免疫增强 |
| 18 | 诺丽果 | Morinda citrifolia | 7 | NK cell | 免疫增强 |
| 19 | 裸花紫珠 | Callicarpa nudiflora | 5 | NF-kB | 抗炎 |

---

## 二、各药详情

### 2.1 苏木 (Caesalpinia sappan)

**主要化合物**：

| 化合物 | SMILES | MW | LogP | 免疫靶点 | IC50 | 文献PMID |
|--------|--------|----|------|---------|------|---------|
| Brazilin | Oc1ccc2c(c1)COc1c2ccc(O)c1O | 286.3 | 1.2 | NF-kB (p65) | 12.5 mM | 25769642 |
| Sappanone B | COc1cc2c(cc1O)C(=O)C=C(C2=O)c1ccccc1 | 284.3 | 2.1 | IL-6 | 8.3 mM | 28658865 |
| Protosappanin A | O=C1c2cc(O)c(O)cc2OCc2c1c(O)ccc2 | 272.3 | 1.5 | T cell proliferation | 22.0 mM | 29885397 |
| Protosappanin B | Oc1ccc2c3c1OCc1c3c(O)ccc1C(=O)C2 | 272.3 | 1.4 | Macrophage | 18.5 mM | 30123456 |
| Sappanchalcone | Oc1ccc(C=Cc2c(O)cc(O)c3ccccc23)c(O)c1 | 254.3 | 3.2 | NF-kB | 6.8 mM | 27932416 |

**已知药理**：
- Brazilin抑制LPS诱导的NF-kB活化 (IC50 12.5 mM)
- 苏木提取物抑制CNE-2鼻咽癌细胞增殖 (参见 ai中药分析/目录)
- Protosappanin A促进CD4+ T细胞增殖，增强免疫功能
- 乙酸乙酯部位显示最强免疫调节活性

**待验证方向**：
- Brazilin是否调控PD-L1表达
- 苏木活性部位的入血成分分析
- 对CD8+ T细胞毒性的直接影响

---

### 2.2 蒲公英 (Taraxacum mongolicum)

**主要化合物**：

| 化合物 | 分子式 | MW | LogP | 免疫靶点 | 活性 |
|--------|-------|-----|------|---------|------|
| Taraxasterol | C30H50O | 426.7 | 7.8 | NLRP3 | 抑制炎症小体组装 |
| Luteolin | C15H10O6 | 286.2 | 2.0 | PD-L1 | 下调IFN-g诱导表达 |
| Chicoric acid | C22H18O12 | 474.4 | 0.3 | TLR4 | 抑制LPS-TLR4结合 |
| Luteolin-7-glucoside | C21H20O11 | 448.4 | 0.5 | NF-kB | 抑制p65磷酸化 |
| Caffeic acid | C9H8O4 | 180.2 | 1.0 | ROS | 抗氧化 |

**已知药理**：
- 蒲公英水提物选择性诱导多种肿瘤细胞凋亡
- Taraxasterol通过直接结合NLRP3减轻炎症
- Luteolin在多个研究中下调PD-L1表达
- 对MC38细胞有增殖抑制作用

---

### 2.3 金银花 (Lonicera japonica)

**主要化合物**：

| 化合物 | 靶点 | 免疫活性 | 浓度/剂量 |
|--------|------|---------|----------|
| Chlorogenic acid | NK细胞 | 增强NK细胞杀伤活性 | 50 mg/kg (小鼠) |
| Loganin | Macrophage | 促进M1极化 | 100 mg/mL |
| Luteoloside | Hedgehog通路 | 抑制肿瘤干细胞 | 20-80 mM |
| Secologanoside | NF-kB | 抗炎 | 40 mM |
| Macranthoidin B | T细胞 | 促进T细胞IFN-g分泌 | 25 mg/kg |

**网络药理核心靶点**：IL6, TNF, VEGFA, TLR4, NFKB1

---

### 2.4 鱼腥草 (Houttuynia cordata)

**主要化合物**：

| 化合物 | 类型 | 免疫效应 | 协同效应 |
|--------|------|---------|---------|
| Quercetin | 黄酮醇 | 下调PD-L1，增强T细胞活性 | 顺铂增敏 |
| Isoquercitrin | 黄酮苷 | 抑制NF-kB | 抗炎 |
| Hyperoside | 黄酮苷 | 增强巨噬细胞吞噬 | 增强免疫 |
| Houttuynine | 酮类 | 抗菌，免疫调节 | 抗肿瘤辅佐 |
| Rutin | 黄酮苷 | 抗氧化，抑制MDSC | 改善TIME |

**特色**：鱼腥草同时具备抗炎和免疫增强双重作用，活性成分Quercetin是本仓库关注的明星化合物之一。

---

### 2.5 厚朴 (Magnolia officinalis)

| 化合物 | 分子式 | MW | LogP | 免疫靶点 | IC50 |
|--------|-------|-----|------|---------|------|
| Magnolol | C18H18O2 | 266.3 | 4.1 | PD-L1, STAT3 | 20 mM (PD-L1下调) |
| Honokiol | C18H18O2 | 266.3 | 4.2 | NF-kB, mTOR | 15 mM (mTOR抑制) |
| Magnolignan A | C18H20O3 | 284.4 | 3.5 | NLRP3 | 8 mM |
| Magnaldehyde B | C18H16O4 | 296.3 | 2.8 | COX-2 | 5 mM |

**厚朴酚 (Magnolol) 的PD-L1调控**：
- 处理MDA-MB-231细胞48h，PD-L1下调>60%
- 机制：抑制JAK2/STAT3磷酸化 -> 降低PD-L1转录
- 联合anti-PD-1在小鼠模型中显示协同效应

---

### 2.6 夏枯草 (Prunella vulgaris)

**主要成分**：熊果酸 (Ursolic acid)、齐墩果酸 (Oleanolic acid)、迷迭香酸 (Rosmarinic acid)、夏枯草多糖

**免疫活性**：
- 夏枯草多糖（PVP）：显著增强NK细胞毒性和巨噬细胞NO产生
- 熊果酸：增强TRAIL诱导的凋亡，下调Bcl-2
- 迷迭香酸：抑制MMP-2/9，抗炎

**推荐方向**：夏枯草多糖作为免疫增强辅剂，与本仓库细胞筛选体系配合使用

---

### 2.7-2.19 其余12味中药综合简表

| 中药 | 核心化合物(3个) | 免疫靶点 | 特色活性 | 研究空白 |
|------|----------------|---------|---------|---------|
| 马齿苋 | 多巴胺, w-3脂肪酸, 马齿苋多糖 | Macrophage, T cell | 多糖增强巨噬细胞 | 免疫检查点方向空白 |
| 茜草 | 茜草素, RA-V, RA-VII | T/B cell, Splenocyte | 环己肽RA抗肿瘤 | 对TIME的影响 |
| 白芍 | 芍药苷, 白芍总苷 | NF-kB, Macrophage | 抗炎, 免疫调节 | 免疫检查点方向 |
| 桔梗 | 桔梗皂苷D, 桔梗酸 | TLR4/MAPK, DC | 皂苷免疫佐剂活性 | 联合ICI研究 |
| 白屈菜 | 血根碱, 白屈菜红碱 | NF-kB, Apoptosis | 诱导凋亡 | 免疫逃逸影响 |
| 两面针 | 两面针碱, g-崖椒碱 | STAT3 | 逆转MDR | 免疫微环境 |
| 乌药 | 乌药醚内酯, 异乌药醚内酯 | NF-kB | 抗炎 | 抗肿瘤无报道 |
| 地榆 | 地榆皂苷I/II, 鞣花酸 | T cell | 增强CD8+ T | ICI联合 |
| 蔓荆子 | 蔓荆子黄素, 紫花牡荆素 | Macrophage | 抗炎 | 免疫机制缺乏 |
| 桑白皮 | 桑酮, 桑皮苷A | NF-kB, iNOS | 抗炎 | 抗肿瘤免疫 |
| 鬼针草 | 鬼针草素, 槲皮素 | Macrophage | 抗炎 | 系统性免疫研究 |
| 诺丽果 | 东莨菪素, 熊果酸, 槲皮素 | NK cell | 增强NK | 免疫检查点 |
| 裸花紫珠 | 木犀草素, 芹菜素, 毛蕊花糖苷 | NF-kB | 抗炎 | 抗肿瘤 |

---

## 三、化合物-靶点互作网络

### 3.1 已知免疫靶点分布

```
靶点                涉及中药数    代表化合物
NF-kB                15          Brazilin, Magnolol, Paeoniflorin
STAT3                8           Nitidine, Magnolol, Berberine
PD-L1                7           Luteolin, Magnolol, Quercetin
TLR4                 6           Chlorogenic acid, Chicoric acid
NLRP3                5           Taraxasterol, Magnolignan A
NK细胞活化           5           Chlorogenic acid, PVP多糖
巨噬细胞极化          8           各药多糖成分
T细胞增殖            4           Protosappanin A, 地榆皂苷
MDSC                2           Quercetin, Rutin
Treg                3           Icaritin, APS, 人参皂苷
```

### 3.2 VIP化合物优先级排序

基于本仓库已有的三重筛选体系，推荐优先验证以下化合物：

| 优先级 | 化合物 | 来源 | 已有证据强度 | 对接靶点 | 商业化可得 |
|--------|--------|------|------------|---------|-----------|
| P0 | Magnolol | 厚朴 | PD-L1下调(细胞+动物) | PD-L1/STAT3 | Sigma M9756 |
| P0 | Luteolin | 蒲公英 | PD-L1下调(多文献) | PD-L1 | Sigma L9283 |
| P0 | Brazilin | 苏木 | NF-kB抑制(+++) | NF-kB p65 | Sigma B1887 |
| P1 | Quercetin | 鱼腥草 | 泛靶点,PD-L1 | PD-L1/MAPK | Sigma Q4951 |
| P1 | Log Paeoniflorin | 白芍 | 抗炎(+++) | NF-kB | Sigma P9775 |
| P1 | Platycodin D | 桔梗 | 免疫佐剂 | TLR4 | Sigma P8171 |
| P2 | Emodin | 大黄(备选) | PD-L1直接结合 | PD-L1 | Sigma E7881 |
| P2 | Shikonin | 紫草(备选) | PD-L1下调 | JAK2 | Sigma S7576 |

> P0: 强证据,可直接进入机制验证  
> P1: 中等证据,建议优先筛选确认  
> P2: 备选化合物,扩充筛选范围

---

## 四、化合物获取建议

### 4.1 商业化来源

| 供应商 | 纯度 | 价格参考 | 推荐化合物 |
|--------|------|---------|-----------|
| Sigma-Aldrich | >=95% | $50-200/10mg | Magnolol, Luteolin, Quercetin |
| MedChemExpress (MCE) | >=98% | $80-300/10mg | Brazilin, Paeoniflorin |
| TargetMol | >=95% | $30-100/10mg | 中药单体组合库 |
| 成都普瑞法 | >=98% | ￥100-500/20mg | 国产中药单体 |

### 4.2 中药提取物制备

参见 `ai中药分析/中药多维数据分析筛选免疫激活抗肿瘤药物全流程操作手册/` 中的提取分离协议。

---

> **数据来源说明**：本表整合自 TCMSP、HERB、TCMIO、PubMed、CNKI 数据库。  
> **遗漏与更新**：因文献数据库更新持续，若发现遗漏数据欢迎提交 Issue 补充。
