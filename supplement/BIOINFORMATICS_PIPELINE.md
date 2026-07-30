# 生物信息学与数据分析流程

> 中药免疫抗肿瘤筛选的数据分析标准流程  
> 含 PCA/OPLS-DA、网络药理学、分子对接、富集分析完整代码框架  
> 2026年7月

---

## 一、环境配置

### 1.1 Python环境

```bash
# 创建conda环境
conda create -n tcm_immuno python=3.10
conda activate tcm_immuno

# 核心依赖
pip install pandas numpy scipy scikit-learn
pip install matplotlib seaborn plotly
pip install rdkit-pypi
pip install biopython
pip install gseapy
pip install openpyxl
```

### 1.2 R环境

```r
# Bioconductor核心包
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install(c("clusterProfiler", "org.Hs.eg.db",
                        "STRINGdb", "igraph", "ropls",
                        "GSVA", "ComplexHeatmap"))
# 免疫分析
install.packages("CIBERSORT")  # 或从 https://cibersort.stanford.edu/ 获取
```

---

## 二、PCA/OPLS-DA 多变量分析 (Python)

### 2.1 UPLC-MS/MS 数据预处理

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# 读取LC-MS峰表 (行=样本, 列=特征)
# 格式: 样本名 | 分组 | m/z1 | m/z2 | ... | m/zN
data = pd.read_csv('lcms_peak_table.csv', index_col=0)

# 数据清洗
# 1. 缺失值处理 (80%规则: 保留>80%样本中出现的峰)
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
data_imputed = pd.DataFrame(
    imputer.fit_transform(data.iloc[:, 1:]),
    columns=data.columns[1:],
    index=data.index
)

# 2. 总离子流归一化
data_norm = data_imputed.div(data_imputed.sum(axis=1), axis=0) * 10000

# 3. UV缩放 (Pareto scaling更常用)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
data_scaled = pd.DataFrame(
    scaler.fit_transform(data_norm),
    columns=data_norm.columns,
    index=data_norm.index
)
```

### 2.2 PCA

```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(data_scaled)

# 可视化
plt.figure(figsize=(8, 6))
groups = data['group']  # 分组信息
for g in np.unique(groups):
    idx = np.where(groups == g)[0]
    plt.scatter(pca_result[idx, 0], pca_result[idx, 1],
                label=g, s=50, alpha=0.7)

plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
plt.title('PCA Score Plot')
plt.legend()
plt.savefig('pca_score_plot.png', dpi=300)
plt.show()
```

### 2.3 OPLS-DA

```python
from sklearn.cross_decomposition import PLSRegression

# 构建分类标签
y = (data['group'] == 'treatment').astype(int).values

# PLS-DA (含正交成分 = OPLS-DA近似)
plsda = PLSRegression(n_components=2)
plsda.fit(data_scaled, y)

# 评分图
pls_scores = plsda.x_scores

plt.figure(figsize=(8, 6))
for g in np.unique(groups):
    idx = np.where(groups == g)[0]
    plt.scatter(pls_scores[idx, 0], pls_scores[idx, 1],
                label=g, s=50, alpha=0.7)
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.title('PLS-DA Score Plot')
plt.legend()
plt.savefig('plsda_score_plot.png', dpi=300)
```

### 2.4 VIP分数计算

```python
def calculate_vip(pls_model, X, y):
    """计算VIP (Variable Importance in Projection)"""
    t = pls_model.x_scores_
    w = pls_model.x_weights_
    q = pls_model.y_loadings_

    p = X.shape[1]
    h = t.shape[1]

    vip = np.zeros((p,))
    ss = np.sum(t**2, axis=0) * np.sum(q**2, axis=0)

    for j in range(p):
        weights = (w[j, :]**2) * ss
        vip[j] = np.sqrt(p * np.sum(weights) / np.sum(ss))

    return vip

vip_scores = calculate_vip(plsda, data_scaled.values, y)

# 输出VIP>1的特征
vip_df = pd.DataFrame({
    'feature': data_scaled.columns,
    'vip_score': vip_scores
}).sort_values('vip_score', ascending=False)

print(f"VIP > 1 的特征数: {(vip_scores > 1).sum()}")
vip_df[vip_df.vip_score > 1].to_csv('vip_features.csv', index=False)
```

### 2.5 R版本的OPLS-DA (推荐)

```r
library(ropls)

# 读取数据
data <- read.csv("lcms_peak_table.csv", row.names = 1)
group <- data$group

# OPLS-DA
opls_model <- opls(data[, -1], group,
                   predI = 1, orthoI = 1,
                   crossvalI = 7)

# 提取VIP
vip <- getVipVn(opls_model)
vip_df <- data.frame(feature = colnames(data)[-1],
                     vip_score = vip)
write.csv(vip_df[vip_df$vip_score > 1, ],
          "vip_features_ropls.csv", row.names = FALSE)
```

---

## 三、网络药理学分析 (Python)

### 3.1 核心靶点获取

```python
import requests
import pandas as pd

def get_tcmsp_targets(herb_name):
    """
    从TCMSP获取中药靶点
    实际使用需替换为TCMSP API调用
    """
    # 示例：硬编码或从已下载的数据库查询
    targets = pd.read_csv(f'tcmsp_{herb_name}_targets.csv')
    return targets

def get_immune_targets(immune_genes_file='immune_genes.txt'):
    """加载免疫相关靶点列表"""
    with open(immune_genes_file) as f:
        immune_genes = [line.strip() for line in f]
    return immune_genes

def get_cancer_targets():
    """获取肿瘤相关靶点 (从DisGeNET/TCGA)"""
    # 常用免疫抗肿瘤靶点列表
    cancer_immune_targets = [
        'IL6', 'TNF', 'VEGFA', 'EGFR', 'AKT1', 'STAT3',
        'NFKB1', 'RELA', 'MAPK1', 'MAPK3', 'PIK3CA',
        'PTEN', 'TP53', 'MYC', 'HIF1A', 'CD274', 'PDCD1',
        'CTLA4', 'LAG3', 'HAVCR2', 'TIGIT', 'CD8A',
        'CD4', 'FOXP3', 'IFNG', 'GZMB', 'PRF1'
    ]
    return cancer_immune_targets

# 交叉分析
herb_targets = get_tcmsp_targets('sappan')
immune_targets = get_immune_targets()
cancer_immune_targets = get_cancer_targets()

# 韦恩交集
all_immune_cancer = list(set(immune_targets) | set(cancer_immune_targets))
common_targets = list(set(herb_targets['target']) & set(all_immune_cancer))

print(f"中药靶点: {len(herb_targets)}")
print(f"免疫肿瘤相关靶点: {len(all_immune_cancer)}")
print(f"交集: {len(common_targets)}")
print("核心靶点:", common_targets[:20])
```

### 3.2 GO/KEGG 富集分析

```python
import gseapy as gp

# GO富集分析
go_enrich = gp.enrichr(
    gene_list=common_targets,
    gene_sets='KEGG_2021_Human',
    organism='human',
    outdir='enrichment_results'
)

# GO Biological Process
go_bp = gp.enrichr(
    gene_list=common_targets,
    gene_sets='GO_Biological_Process_2021',
    organism='human',
    outdir='go_bp_results'
)

# 可视化
from gseapy.plot import barplot, dotplot

# 气泡图
dotplot(go_enrich.results, title='KEGG Pathway Enrichment',
        figsize=(8, 6))
plt.savefig('kegg_bubble.png', dpi=300)

# 条形图
barplot(go_enrich.results, title='KEGG Top Pathways',
        figsize=(8, 4))
plt.savefig('kegg_bar.png', dpi=300)
```

### 3.3 PPI网络构建 (Cytoscape + STRING)

```python
# 方式1: 通过STRING API直接获取
import requests

string_api_url = "https://string-db.org/api"
method = "network"
params = {
    "identifiers": "\r".join(common_targets[:50]),  # STRING限制50个
    "species": 9606,  # 人类
    "required_score": 400,  # 中等置信度 (0.4*1000)
}

response = requests.post(f"{string_api_url}/json/{method}", data=params)
# 结果保存为Cytoscape兼容格式
with open('string_ppi_network.json', 'w') as f:
    f.write(response.text)
```

---

## 四、分子对接流程 (Python + AutoDock Vina)

### 4.1 化合物预处理

```python
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors

def prepare_ligand(smiles, output_name):
    """SMILES -> 3D结构 -> PDBQT"""
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)

    # 生成3D构象
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    AllChem.EmbedMolecule(mol, params)
    AllChem.MMFFOptimizeMolecule(mol)

    # 保存为PDB
    Chem.MolToPDBFile(mol, f'{output_name}.pdb')

    # 转换为PDBQT (需要meeko/obabel)
    # 命令行: obabel {output_name}.pdb -O {output_name}.pdbqt --gen3d

def admet_filter(smiles):
    """SwissADME风格ADME筛选"""
    mol = Chem.MolFromSmiles(smiles)
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Descriptors.NumHDonors(mol)
    hba = Descriptors.NumHAcceptors(mol)
    rot = Descriptors.NumRotatableBonds(mol)

    # Lipinski Rule of Five
    lipinski_pass = sum([
        mw <= 500,
        logp <= 5,
        hbd <= 5,
        hba <= 10
    ])

    # 口服吸收筛选 (参考SwissADME标准)
    oral_absorption = lipinski_pass >= 3

    return {
        'MW': round(mw, 1),
        'LogP': round(logp, 2),
        'HBD': hbd,
        'HBA': hba,
        'RotB': rot,
        'Lipinski': lipinski_pass,
        'OralAbsorption': oral_absorption
    }
```

### 4.2 Vina批量对接

```python
import subprocess
import os

def batch_docking(ligands_sdf, protein_pdbqt, output_dir):
    """批量分子对接"""
    os.makedirs(output_dir, exist_ok=True)

    # 读取配体
    supplier = Chem.SDMolSupplier(ligands_sdf)

    results = []
    for i, mol in enumerate(supplier):
        name = mol.GetProp('_Name') if mol.HasProp('_Name') else f'ligand_{i}'

        # 转换为PDBQT (meeko)
        pdbqt_file = f'{output_dir}/{name}.pdbqt'
        subprocess.run([
            'mk_prepare_ligand.py',
            '-i', f'ligand_{i}.pdb',
            '-o', pdbqt_file
        ])

        # Vina对接
        out_file = f'{output_dir}/{name}_vina_out.pdbqt'
        result = subprocess.run([
            'vina',
            '--receptor', protein_pdbqt,
            '--ligand', pdbqt_file,
            '--out', out_file,
            '--center_x', 10.0,
            '--center_y', 20.0,   # 根据对接位点调整
            '--center_z', 15.0,
            '--size_x', 20,
            '--size_y', 20,
            '--size_z', 20,
            '--exhaustiveness', 8
        ], capture_output=True, text=True)

        # 解析结果
        for line in result.stdout.split('\n'):
            if line.startswith('1'):
                affinity = float(line.split()[1])
                results.append({
                    'ligand': name,
                    'affinity_kcal_mol': affinity
                })
                break

    return pd.DataFrame(results).sort_values('affinity_kcal_mol')
```

### 4.3 CB-Dock 2 (在线替代)

对于Vina环境配置困难的情况，可使用CB-Dock 2的批量提交脚本：

```python
import requests
import time

def submit_cbdock2(smiles_list, protein_pdb_id='5J89'):
    """
    通过CB-Dock 2 API进行自动对接
    实际使用请参考 https://cadd.labshare.cn/cb-dock2/
    """
    # CB-Dock 2 接受蛋白PDB ID + SMILES
    # 返回预测结合位点和对接得分
    pass
```

---

## 五、数据可视化模板

### 5.1 火山图

```python
import numpy as np
import matplotlib.pyplot as plt

def volcano_plot(data, fc_col='fold_change', pval_col='p_value',
                 fc_thresh=1.5, pval_thresh=0.05):
    """差异代谢物/基因火山图"""
    data['-log10_pval'] = -np.log10(data[pval_col])
    data['regulation'] = 'NS'
    up_idx = (data[fc_col] > fc_thresh) & (data[pval_col] < pval_thresh)
    down_idx = (data[fc_col] < 1/fc_thresh) & (data[pval_col] < pval_thresh)
    data.loc[up_idx, 'regulation'] = 'Up'
    data.loc[down_idx, 'regulation'] = 'Down'

    colors = {'Up': '#E41A1C', 'Down': '#377EB8', 'NS': '#A0A0A0'}
    plt.figure(figsize=(8, 6))
    for reg, grp in data.groupby('regulation'):
        plt.scatter(grp[fc_col], grp['-log10_pval'],
                   c=colors[reg], label=reg, alpha=0.5, s=10)

    plt.axhline(-np.log10(pval_thresh), color='grey', linestyle='--', alpha=0.5)
    plt.axvline(fc_thresh, color='grey', linestyle='--', alpha=0.5)
    plt.axvline(1/fc_thresh, color='grey', linestyle='--', alpha=0.5)

    plt.xlabel('Fold Change (log2 scaled)')
    plt.ylabel('-log10(p-value)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('volcano_plot.png', dpi=300)
```

### 5.2 热图

```python
import seaborn as sns

def feature_heatmap(data_norm, annotation, top_n=50):
    """差异特征热图"""
    # 选择差异最大top_n
    feature_var = data_norm.var(axis=0).sort_values(ascending=False)
    top_features = feature_var.head(top_n).index

    # 绘制
    g = sns.clustermap(
        data_norm[top_features].T,
        z_score=0,  # 行标准化
        cmap='RdBu_r',
        col_colors=annotation['group'].map({
            'control': '#4DAF4A',
            'treatment': '#E41A1C'
        }),
        figsize=(12, 10),
        xticklabels=False
    )
    g.savefig('heatmap_top50.png', dpi=300)
```

---

## 六、完整分析管线示例

```bash
#!/bin/bash
# run_full_pipeline.sh
# TCM免疫抗肿瘤筛选完整数据分析管线

# Step 1: LC-MS 数据预处理
python scripts/01_preprocess_lcms.py \
    --input data/raw/peak_table.csv \
    --output data/processed/

# Step 2: PCA/OPLS-DA
Rscript scripts/02_oplsda.R \
    --input data/processed/norm_peaks.csv \
    --group info/group_info.csv \
    --output results/oplsda/

# Step 3: VIP筛选 + 数据库匹配
python scripts/03_vip_database_match.py \
    --vip results/oplsda/vip_scores.csv \
    --vip_threshold 1.0 \
    --database tcmsp_local.db \
    --output results/vip_compounds/

# Step 4: 网络药理学
python scripts/04_network_pharmacology.py \
    --compounds results/vip_compounds/identified.csv \
    --target_db data/targets/ \
    --output results/network/

# Step 5: 分子对接
python scripts/05_molecular_docking.py \
    --compounds results/network/candidates.csv \
    --protein_pdb data/proteins/PD-L1.pdb \
    --output results/docking/

# Step 6: 结果汇总
python scripts/06_summary_report.py \
    --input_dir results/ \
    --output report/
```

---

## 七、数据文件标准格式

### 7.1 LC-MS峰表格式

```csv
sample_id,group,mz_100.05,mz_120.08,mz_150.12,...
S01,control,1250.3,450.2,8920.1,...
S02,control,1310.8,421.5,8750.6,...
S03,treatment,980.2,892.1,12540.3,...
S04,treatment,1020.5,810.4,13210.8,...
```

### 7.2 化合物活性表格式

```csv
compound,smiles,target,ic50_umol,activity
brazilin,Oc1ccc2c(c1)COc1c2ccc(O)c1O,NFKB1,12.5,inhibitor
sappanone_B,COc1cc2c(cc1O)C(=O)C=C(C2=O)c1ccccc1,IL6,8.3,inhibitor
quercetin,Oc1cc(O)c2c(c1)oc(-c1ccc(O)c(O)c1)c(O)c2=O,PD-L1,15.2,downregulator
```

---

> **更多脚本**：参见 `ai中药分析/` 目录中的完整操作手册  
> **AI辅助分析**：参见 `LLM/` 目录中的Biomni和DeepDR集成工具
