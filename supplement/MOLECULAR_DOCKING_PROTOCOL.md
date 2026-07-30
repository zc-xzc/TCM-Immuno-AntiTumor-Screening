# 分子对接与虚拟筛选标准协议

> 针对免疫抗肿瘤靶点的中药化合物虚拟筛选标准化流程  
> 适用靶点：PD-1/PD-L1, CTLA-4, LAG-3, TIM-3, NF-kB, STAT3  
> 2026年7月

---

## 一、协议概览

```
化合物库准备 (TCMSP/HERB)
     │
     v
ADME筛选 (SwissADME)
     │
     v
靶点结构准备 (PDB / AlphaFold)
     │
     v
分子对接 (AutoDock Vina / GNINA)
     │
     v
打分排序 + 结合模式分析
     │
     v
候选化合物 (TOP 10-50)
     │
     v
体外活性验证 (本仓库三级体系)
```

---

## 二、化合物库构建

### 2.1 来源与准备

| 来源 | 格式 | 数量 | 筛选级别 |
|------|------|------|---------|
| TCMSP (OB>=30%, DL>=0.18) | SDF | 1,000-5,000 | 一级筛选 |
| HERB Database | SDF/SMILES | 10,000+ | 全库筛选 |
| TCMIO (免疫相关) | SDF | 3,000-5,000 | 靶点富集筛选 |
| Self-built 19-herb library | SDF | 200-500 | 本仓库专属 |

### 2.2 ADME预筛选标准

```
Lipinski Rule of Five (RO5):
  - MW <= 500
  - LogP <= 5
  - HBD <= 5 (NH + OH)
  - HBA <= 10 (N + O)

Veber Rules:
  - Rotatable bonds <= 10
  - PSA <= 140 A^2

Enhanced筛选 (免疫需求):
  - GI absorption = High (SwissADME)
  - P-gp substrate = No (避免外排)
  - PAINS alert = 0
  - Brenk alert <= 1
```

---

## 三、靶点结构准备

### 3.1 关键免疫靶点PDB列表

| 靶点 | PDB ID | 分辨率 | 关键位点 | 是否含配体 | 推荐链 |
|------|--------|--------|---------|-----------|-------|
| PD-1 | 5IUS | 2.0 A | 结合界面 | 否 | A |
| PD-L1 | 5J89 | 2.3 A | C/F面 | 是 (BMS-202) | A |
| PD-1/PD-L1复合物 | 5IUS+5J89 | - | 蛋白-蛋白界面 | 否 | - |
| CTLA-4 | 5E03 | 2.8 A | MYPPPY基序 | 否 | A |
| LAG-3 | 6ULQ | 2.5 A | D1结构域 | 否 | A |
| TIM-3 | 5F71 | 2.3 A | FG loop | 否 | A |
| TIGIT | 5HHB | 2.4 A | CD155结合面 | 否 | A |
| STAT3 | 6NJS | 2.5 A | SH2结构域 | 是 | A |
| NF-kB p65 | 1VKX | 2.6 A | DNA结合域 | 否 | A/B |
| TLR4/MD-2 | 3FXI | 2.1 A | 疏水口袋 | 是 | A |

### 3.2 蛋白前处理 (PyMOL/AutoDock Tools)

```bash
# PyMOL脚本: 准备蛋白
fetch 5J89
remove solvent
select binding_site, chain A and resi 50-125
save pd-l1_processed.pdb, chain A

# AutoDock Tools: 加氢/电荷
# 或者使用脚本:
prepare_receptor -r pd-l1_processed.pdb -o pd-l1.pdbqt
```

### 3.3 AlphaFold2/3预测结构

当实验结构不可用或需要替代构象时：

```python
# AlphaFold DB下载示例
import requests

def download_alphafold(uniprot_id, output_file):
    url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
    response = requests.get(url)
    with open(output_file, 'wb') as f:
        f.write(response.content)

# 免疫靶点UniProt IDs:
# PD-1: Q15116
# PD-L1: Q9NZQ7
# CTLA-4: P16410
# LAG-3: P18627
# TIM-3: Q8TDQ0
# TIGIT: Q495A1
```

---

## 四、分子对接 (AutoDock Vina)

### 4.1 对接盒设置

| 靶点 | 中心 (x,y,z) | 尺寸 (x,y,z) A | 说明 |
|------|-------------|---------------|------|
| PD-L1 (5J89) | 10.0, 20.0, 15.0 | 20, 20, 20 | 针对BMS-202结合口袋 |
| PD-1 (5IUS) | 0.0, -5.0, 10.0 | 22, 22, 22 | BC环区域 |
| CTLA-4 (5E03) | -5.0, 0.0, 5.0 | 22, 22, 22 | CD80/86结合面 |
| STAT3 SH2 (6NJS) | 15.0, -5.0, 10.0 | 20, 20, 20 | pY肽结合口袋 |
| NF-kB p65 (1VKX) | 0.0, 5.0, 0.0 | 24, 24, 24 | DNA结合区 |

### 4.2 批量对接脚本

```python
#!/usr/bin/env python3
"""TCM免疫靶点批量对接"""

import subprocess
import os
import pandas as pd
from glob import glob

# 配置
RECEPTOR = "pd-l1_5j89.pdbqt"
LIGAND_DIR = "ligands_pdbqt/"
OUTPUT_DIR = "docking_results/"
EXHAUSTIVENESS = 8
NUM_MODES = 9

# 对接配置
DOCKING_CONFIGS = {
    "PD-L1": {"center": [10.0, 20.0, 15.0], "size": [20, 20, 20]},
    "PD-1":  {"center": [0.0, -5.0, 10.0],  "size": [22, 22, 22]},
    "STAT3": {"center": [15.0, -5.0, 10.0], "size": [20, 20, 20]},
    "CTLA4": {"center": [-5.0, 0.0, 5.0],   "size": [22, 22, 22]},
}

def run_vina_docking(target, ligand_pdbqt, output_file):
    cfg = DOCKING_CONFIGS[target]
    cmd = [
        "vina",
        "--receptor", f"{target}_{RECEPTOR}",
        "--ligand", ligand_pdbqt,
        "--out", output_file,
        "--center_x", str(cfg["center"][0]),
        "--center_y", str(cfg["center"][1]),
        "--center_z", str(cfg["center"][2]),
        "--size_x", str(cfg["size"][0]),
        "--size_y", str(cfg["size"][1]),
        "--size_z", str(cfg["size"][2]),
        "--exhaustiveness", str(EXHAUSTIVENESS),
        "--num_modes", str(NUM_MODES)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return parse_vina_result(result.stdout)

def parse_vina_result(output):
    """从Vina输出中提取各模式的结合能"""
    results = []
    in_modes = False
    for line in output.split('\n'):
        if line.startswith('-----+'):
            in_modes = True
            continue
        if in_modes and line.strip():
            parts = line.split()
            if len(parts) >= 4:
                mode = int(parts[0])
                affinity = float(parts[1])
                results.append({"mode": mode, "affinity": affinity})
    return results
```

### 4.3 结果评分

```python
def score_docking(results_df, compound_info):
    """综合评分函数"""
    scores = []
    for _, row in results_df.iterrows():
        # 结合能评分 (<= -8.0 kcal/mol: 优秀)
        binding_score = min(1.0, max(0, (-row['affinity'] - 6.0) / 4.0))

        # 结合模式评分 (人工检查氢键/疏水)
        # 此处简化为基于rmsd多样性的评分
        mode_diversity = min(1.0, row['num_good_modes'] / 5)

        # 综合
        total = 0.6 * binding_score + 0.4 * mode_diversity
        scores.append(total)
    return scores

# 输出对接热图
import seaborn as sns

def plot_docking_heatmap(results_pivot, target_name):
    plt.figure(figsize=(10, 8))
    sns.heatmap(results_pivot, cmap='RdYlGn_r',
                annot=True, fmt='.1f',
                xticklabels=True, yticklabels=True)
    plt.title(f'{target_name} - Molecular Docking Scores (kcal/mol)')
    plt.xlabel('Compounds')
    plt.ylabel('Replicates')
    plt.tight_layout()
    plt.savefig(f'docking_heatmap_{target_name}.png', dpi=300)
```

---

## 五、对接后分析

### 5.1 结合模式评估标准

```
优秀: binding affinity <= -8.0 kcal/mol
      氢键数 >= 3
      关键残基疏水相互作用
      RMSD < 2.0 A (与已知抑制剂相比)

良好: binding affinity -7.0 ~ -8.0 kcal/mol
      氢键数 2-3
      位于结合口袋内

一般: binding affinity > -7.0 kcal/mol
      位于结合口袋边缘或外部
```

### 5.2 关键残基对照

| 靶点 | 关键氢键残基 | 关键疏水残基 |
|------|-------------|-------------|
| PD-L1 | Tyr56, Gln66, Asp122, Lys124 | Met115, Tyr123, Ile54 |
| PD-1 | Asn66, Gln99, Glu103 | Tyr68, Ile126, Leu128 |
| CTLA-4 | Met99, Tyr100, Glu104 | Tyr105, Phe108 |
| STAT3 SH2 | Arg609, Ser611, Glu612 | Ile589, Trp623 |

---

## 六、虚拟筛选→实验验证流程

### 6.1 候选化合物排序

```
一级筛选: 5000+ 化合物
   │ ADME (SwissADME)
   v
二级筛选: 1000+ 化合物
   │ 分子对接 (Vina, cutoff -7.5 kcal/mol)
   v
三级筛选: 50-100 化合物
   │ 结合模式分析 (关键残基互作)
   v
四级筛选: 10-20 化合物
   │ 结合自由能计算 (MM/GBSA, 可选)
   v
最终候选: 5-10 化合物
   │ 商业化可得性检查
   v
体外验证
   (本仓库三级筛选体系)
```

### 6.2 验证优先级

| 靶点 | 推荐验证方法 | 参考阳性对照 |
|------|------------|-------------|
| PD-L1 (下调) | WB + 流式 (蛋白表达) | BMS-202 (小分子) |
| PD-1/PD-L1 (阻断) | ELISA (竞争结合) | Atezolizumab (抗体) |
| STAT3 (抑制) | p-STAT3 WB | Stattic |
| NF-kB (抑制) | p-p65 WB + 荧光素酶 | BAY 11-7082 |

---

## 七、GNINA (深度学习对接) 补充

```bash
# GNINA安装
conda install -c gnina gnina

# 对接命令
gnina -r pd-l1.pdbqt \
      -l ligands.sdf \
      --autobox_ligand known_ligand.pdbqt \
      --cnn_scoring all \
      -o docked.sdf

# 优点: CNN打分更准确,无需手动设定结合盒
# 缺点: 速度较慢
```

---

## 八、常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 所有化合物得分均差 | 结合盒位置不准确 | 使用CB-Dock 2重新预测结合口袋 |
| 高得分化合物无活性 | 评分函数限制 | MM/GBSA再打分；考虑构象熵 |
| 对接结果重现性差 | Vina随机性 | 固定随机种子；增加exhaustiveness至16 |
| 化合物与已知抑制剂竞争 | 非特异性结合 | MD模拟验证结合稳定性 |

---

> **工具引用**:
> - AutoDock Vina: Eberhardt et al., J Comput Chem, 2021
> - GNINA: McNutt et al., J Cheminform, 2021
> - CB-Dock 2: Yang et al., Nucleic Acids Res, 2022
> - SwissADME: Daina et al., Sci Rep, 2017
