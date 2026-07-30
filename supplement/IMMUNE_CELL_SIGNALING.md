# 免疫细胞与信号通路参考

> 本项目涉及的免疫细胞类型、功能标志物、关键信号通路速查表  
> 辅助实验设计和结果解读  
> 2026年7月

---

## 一、免疫细胞分类与功能

### 1.1 固有免疫细胞

| 细胞类型 | 核心功能 | 激活标志物 | 抑制标志物 | 效应分子 |
|---------|---------|-----------|-----------|---------|
| **NK细胞** | 直接杀伤肿瘤细胞 | CD69, NKG2D, CD107a | KIR, NKG2A | Perforin, Granzyme B, IFN-g |
| **巨噬细胞 M1** | 抗肿瘤,促炎 | CD80, CD86, MHC-II, iNOS | — | TNF, IL-12, NO, ROS |
| **巨噬细胞 M2** | 促肿瘤,抗炎 | CD163, CD206, Arg1 | — | IL-10, TGF-b, VEGF |
| **DC细胞** | 抗原提呈 | CD80, CD86, CD83, MHC-II | PD-L1, IL-10 | IL-12, CXCL10 |
| **MDSCs** | 免疫抑制 | CD11b+Gr-1+(小鼠), CD11b+CD33+(人) | — | Arg1, iNOS, ROS |
| **中性粒细胞** | 炎症,NETosis | CD66b, MPO | N2: TGF-b | ROS, MMP-9, NETs |
| **gammadelta T** | 固有样T细胞 | TCRgd, NKG2D | PD-1 | IFN-g, TNF, Perforin |

### 1.2 适应性免疫细胞

| 细胞类型 | 核心功能 | 表面标志 | 转录因子 | 效应因子 |
|---------|---------|---------|---------|---------|
| **CD8+ T (CTL)** | 直接杀伤肿瘤 | CD3+CD8+ | T-bet, Eomes | Perforin, GzmB, IFN-g |
| **CD4+ Th1** | 辅助CTL,抗肿瘤 | CD3+CD4+CXCR3+ | T-bet, STAT4 | IFN-g, TNF, IL-2 |
| **CD4+ Th2** | 体液免疫 | CD3+CD4+CCR4+ | GATA3, STAT6 | IL-4, IL-5, IL-13 |
| **CD4+ Th17** | 促炎,自身免疫 | CD3+CD4+CCR6+ | RORgt, STAT3 | IL-17A, IL-22 |
| **Treg** | 免疫抑制 | CD3+CD4+Foxp3+CD25+ | Foxp3, STAT5 | IL-10, TGF-b, IL-35 |
| **Tfh** | 生发中心,B细胞辅助 | CD3+CD4+CXCR5+PD-1+ | Bcl-6 | IL-21 |
| **B细胞** | 抗体产生 | CD19+CD20+ | Pax5 | 抗体, IL-10, IL-35 |
| **NKT细胞** | 快速免疫调节 | CD3+NK1.1+ | PLZF | IFN-g, IL-4 |

---

## 二、肿瘤免疫微环境 (TIME)

### 2.1 TIME分类

| 类型 | CD8+ T浸润 | PD-L1表达 | 突变负荷 | 对ICI响应 | 中药干预策略 |
|------|-----------|----------|---------|----------|-------------|
| **I型 (免疫炎症型)** | 高 | 高 | 高 | 好 | 增强已有免疫 |
| **II型 (免疫排斥型)** | 基质边缘 | 中 | 中 | 差 | 促进T细胞浸润 |
| **III型 (免疫沙漠型)** | 缺如 | 低 | 低 | 差 | 启动免疫应答 |
| **IV型 (免疫耗竭型)** | 高但功能低 | 高 | 高 | 部分 | 逆转T细胞耗竭 |

### 2.2 免疫细胞标志物流式方案

**小鼠TILs 8色方案**：

| 通道 | 标志物 | 细胞群 |
|------|--------|-------|
| FITC | CD45 | 白细胞 |
| PE | CD3 | T细胞 |
| PerCP-Cy5.5 | CD8 | CTL |
| PE-Cy7 | CD4 | Th |
| APC | Foxp3 | Treg |
| Alexa700 | PD-1 | 耗竭 |
| APC-Cy7 | CD69 | 早期活化 |
| BV421 | GzmB | 细胞毒功能 |

**人PBMC免疫检查点方案**：

| 通道 | 标志物 | 用途 |
|------|--------|------|
| FITC | CD3 | T细胞总数 |
| PE | PD-L1(CD274) | 检查点表达 |
| PerCP-Cy5.5 | CD8 | CTL亚群 |
| PE-Cy7 | PD-1(CD279) | 检查点表达 |
| APC | TIM-3(CD366) | 耗竭标志 |
| BV421 | LAG-3(CD223) | 耗竭标志 |

---

## 三、关键免疫信号通路

### 3.1 T细胞受体信号通路 (KEGG: hsa04660)

```
TCR -> CD3 -> LCK/ZAP70 -> LAT -> PLCg1
                                       │
                        ┌──────────────┴──────────────┐
                        v                             v
                   IP3 -> Ca2+                     DAG -> PKCq
                        │                             │
                    NFAT活化                     NF-kB/IKK活化
                        │                             │
                        └──────────┬──────────────────┘
                                   v
                              IL-2转录
                              + 细胞增殖/分化

中药调控节点:
  - LCK/ZAP70: 蒲公英Taraxasterol (激活)
  - NF-kB: Brazilin, Paeoniflorin (抑制)
  - Ca2+/NFAT: 姜黄素 (调节)
```

### 3.2 PD-1/PD-L1免疫检查点信号 (KEGG: hsa05235)

```
肿瘤细胞PD-L1 + T细胞PD-1
         │
         v
    PD-1 ITIM/SHP-2磷酸化
         │
         v
    ┌────┴────┐
    v         v
  PI3K/Akt  RAS/MEK/ERK  (抑制)
  (抑制)      │
    │         v
    │    T细胞增殖下降
    v    细胞因子减少
  Bcl-xL下调
  抗凋亡下降

中药调控:
  - 上通路: PD-1/PD-L1阻断 (Magnolol, Luteolin)
  - 下通路: PI3K/Akt激活 (黄芪多糖)
```

### 3.3 NF-kB 信号通路 (KEGG: hsa04064)

```
炎性刺激 (TNF/LPS/IL-1)
    │
    v
IKK复合物 (IKKa/IKKb/NEMO)
    │
    v
IkBa磷酸化 -> 泛素化降解
    │
    v
p50/p65核转位
    │
    v
转录: 促炎因子, 趋化因子, 抗凋亡蛋白

中药抑制剂:
  - Brazilin (Ikkb直接结合)
  - Paeoniflorin (抑制Ikk活化)
  - Magnolol (抑制p65核转位)
  - Curcumin (降低p65乙酰化)
```

### 3.4 JAK/STAT 信号通路 (KEGG: hsa04630)

```
细胞因子结合 -> 受体二聚化
    │
    v
JAK磷酸化 (JAK1/2, TYK2)
    │
    v
STAT磷酸化 (STAT1/3/5/6)
    │
    v
STAT二聚化 -> 核转位 -> 转录

STAT3在多癌中持续活化:
  - 促进: 增殖, 存活, 血管生成
  - 抑制: 抗肿瘤免疫

中药STAT3抑制剂:
  - Nitidine (两面针碱): 直接结合SH2
  - Magnolol (厚朴酚): 抑制磷酸化
  - Berberine (小檗碱): 抑制转录活性
```

### 3.5 PI3K/Akt/mTOR (KEGG: hsa04151)

```
受体酪氨酸激酶/GPCR
    │
    v
PI3K -> PIP2 -> PIP3 -> PDK1
    │
    v
        Akt (Thr308/Ser473)
        │
    ┌───┴───┐
    v       v
  mTORC1  FoxO1
    │       │
    v       v
  蛋白合成  细胞周期

中药调控:
  - 人参皂苷Rg3: 抑制PI3K/Akt
  - 雷公藤红素: 抑制mTORC1
  - 黄芪多糖: 激活Akt (保护免疫细胞)
```

---

## 四、关键细胞因子功能速查

| 细胞因子 | 主要来源 | 主要功能 | 肿瘤免疫角色 |
|---------|---------|---------|------------|
| **IFN-g** | Th1, CTL, NK | 巨噬细胞活化, MHC上调 | 抗肿瘤 (关键) |
| **TNF** | Macrophage, Th1 | 促炎, 凋亡诱导 | 双相 (剂量依赖) |
| **IL-2** | CD4+ T | T细胞增殖 | 抗肿瘤 (促进CTL) |
| **IL-4** | Th2 | B细胞活化, Th2分化 | 促肿瘤 |
| **IL-6** | Macrophage, T | 促炎, STAT3活化 | 促肿瘤 (多数情况) |
| **IL-10** | Treg, M2 | 免疫抑制 | 促肿瘤 |
| **IL-12** | DC, Macrophage | Th1极化, NK活化 | 抗肿瘤 (强) |
| **IL-17A** | Th17, gdT | 促炎, 中性粒细胞募集 | 双相 |
| **TGF-b** | Treg, 肿瘤 | 免疫抑制, EMT | 促肿瘤 |
| **GM-CSF** | T cell, Mac | 粒细胞/巨噬细胞生成 | 双相 |

---

## 五、免疫检测方法推荐

### 5.1 体外细胞活性

| 方法 | 检测内容 | 优点 | 平台 |
|------|---------|------|------|
| MTT/CCK-8 | 细胞活力 | 简便 | 酶标仪 |
| 流式Annexin V/PI | 凋亡 | 准确 | 流式细胞仪 |
| LDH释放 | 细胞毒 | 高通量 | 酶标仪 |
| CFSE稀释 | T细胞增殖 | 动态 | 流式细胞仪 |
| ELISpot | 细胞因子斑点 | 单细胞敏感 | ELISpot阅读器 |

### 5.2 免疫功能检测

| 方法 | 靶标 | 说明 |
|------|------|------|
| ELISA | 可溶性细胞因子 | 上清/血清 |
| CBA (Cytometric Bead Array) | 多细胞因子 | 流式, 高通量 |
| Griess法 | NO (巨噬细胞) | 简便比色法 |
| 流式胞内染色 | IFN-g, GzmB, TNF | 需要BFA/GolgiStop |
| 流式表面染色 | PD-L1, CD80, CD86 | 直接标记 |
| Ezrin法 | 免疫突触 | 共聚焦显微镜 |

### 5.3 动物模型推荐

| 模型 | 肿瘤 | 用途 |
|------|------|------|
| MC38 s.c. | 结直肠癌 | 免疫原性，本仓库主模型 |
| B16-F10 s.c. | 黑色素瘤 | 低免疫原性，耐药模型 |
| LLC | 肺癌 | 肺微环境 |
| 4T1 | 乳腺癌 | 转移模型 |
| CT26 | 结直肠癌 | 高免疫原性 |

---

> **相关工具**：本仓库 `ai中药分析/` 目录含详细操作手册  
> **LLM辅助**：`LLM/Biomni/` 可用于免疫通路知识检索
