# 网络药理学标准分析流程

> 面向中药免疫抗肿瘤活性成分的"成分-靶点-通路-疾病"网络分析完整流程  
> 2026年7月

---

## 一、总体框架

```
中药(19味)           免疫-抗肿瘤
    │                    │
    v                    v
活性成分筛选      免疫/肿瘤靶点库
(TCMSP/ADME)     (TCMIO/DisGeNET)
    │                    │
    └────────┬───────────┘
             v
        成分-靶点交集
             │
             v
    ┌────────┴────────┐
    v                 v
GO/KEGG富集         PPI网络
    │                 │
    v                 v
通路注释          Hub基因识别
(免疫相关)       (cytoHubba)
    │                 │
    └────────┬─────────┘
             v
    中药-成分-靶点-通路网络
             │
             v
   分子对接+实验验证
```

---

## 二、数据库获取

### 2.1 活性成分获取与筛选

**TCMSP API脚本**：

```python
import requests
import pandas as pd

def query_tcmsp(herb_name, ob_threshold=30, dl_threshold=0.18):
    """从TCMSP查询中药活性成分"""
    # TCMSP API (需替换为实际端点)
    url = f"https://tcmsp-e.com/api.php"
    params = {
        "action": "search_herb",
        "herb_name": herb_name
    }

    try:
        response = requests.post(url, data=params)
        data = response.json()

        ingredients = []
        for item in data.get('result', []):
            # 筛选条件: OB>=30%, DL>=0.18
            ob = float(item.get('OB', 0))
            dl = float(item.get('DL', 0))
            caco2 = float(item.get('Caco-2', -1))

            if ob >= ob_threshold and dl >= dl_threshold and caco2 >= -0.4:
                ingredients.append({
                    'molecule_id': item['Mol_ID'],
                    'name': item['Molecule_name'],
                    'smiles': item.get('SMILES', ''),
                    'ob': ob,
                    'dl': dl,
                    'caco2': caco2,
                    'mw': item.get('MW', ''),
                    'logp': item.get('ALogP', ''),
                    'hbd': item.get('Hdon', ''),
                    'hba': item.get('Hacc', '')
                })

        return pd.DataFrame(ingredients)

    except Exception as e:
        print(f"TCMSP查询失败: {e}")
        # 回退到本地缓存数据
        return pd.read_csv(f'local_cache/{herb_name}_tcmsp.csv')


# 批量查询19味中药
herbs = [
    'Caesalpinia sappan', 'Taraxacum mongolicum',
    'Lonicera japonica', 'Houttuynia cordata',
    'Prunella vulgaris', 'Portulaca oleracea',
    # ...
]

all_compounds = []
for herb in herbs:
    df = query_tcmsp(herb)
    df['herb'] = herb
    all_compounds.append(df)
    print(f"{herb}: {len(df)} active ingredients")

combined = pd.concat(all_compounds, ignore_index=True)
combined.to_csv('19herbs_active_compounds.csv', index=False)
```

### 2.2 靶点获取

```python
# 成分靶点获取 (SwissTargetPrediction)
def get_compound_targets(smiles, species='human'):
    """使用SwissTargetPrediction API"""
    url = "https://swisstargetprediction.ch/api/v1/predict"
    try:
        response = requests.post(url, json={
            'smiles': smiles,
            'species': species
        })
        targets = response.json().get('targets', [])
        return [t['target'] for t in targets[:20]]  # top 20
    except:
        return []

# 免疫靶点库 (TCMIO)
def get_immune_targets():
    """核心免疫抗肿瘤靶点集"""
    immune_targets = {
        # 细胞因子
        'IL2', 'IL4', 'IL6', 'IL10', 'IL12A', 'IL12B',
        'IFNG', 'TNF', 'TGFB1', 'CSF2',
        # 免疫检查点
        'CD274', 'PDCD1', 'CTLA4', 'LAG3', 'HAVCR2', 'TIGIT',
        'CD80', 'CD86', 'ICOS', 'ICOSLG',
        # T细胞信号
        'CD3E', 'CD4', 'CD8A', 'CD8B', 'ZAP70', 'LAT', 'LCK',
        'CD28', 'PRF1', 'GZMB', 'GZMA',
        # 转录因子
        'STAT3', 'STAT1', 'NFKB1', 'RELA', 'FOXP3', 'TBX21', 'GATA3',
        'RORC', 'HIF1A',
        # 趋化因子
        'CXCL9', 'CXCL10', 'CXCL11', 'CXCR3', 'CCL2', 'CCL5',
        'CCR5', 'CCR7',
        # 巨噬细胞/DC
        'CD14', 'CD163', 'CD68', 'ITGAM', 'CSF1R',
        'CD80', 'CD86', 'CD40', 'TLR4', 'MYD88',
        # NK细胞
        'NKG2D', 'NCR1', 'FCGR3A',
        # 凋亡/增殖
        'TP53', 'BCL2', 'BAX', 'CASP3', 'CASP8',
        'MYC', 'EGFR', 'AKT1', 'MTOR', 'MAPK1', 'MAPK3',
        # 血管生成
        'VEGFA', 'VEGFR2', 'MMP9', 'HIF1A',
    }
    return immune_targets

# 交集分析
herb_compounds = pd.read_csv('19herbs_active_compounds.csv')
herb_targets = []
for _, row in herb_compounds.iterrows():
    targets = get_compound_targets(row['smiles'])
    herb_targets.append({
        'compound': row['name'],
        'herb': row['herb'],
        'targets': ';'.join(targets)
    })

target_df = pd.DataFrame(herb_targets)
target_df.to_csv('compound_targets.csv', index=False)
```

---

## 三、富集分析

### 3.1 GO/KEGG (Python)

```python
import gseapy as gp

# 合并所有靶点
all_targets = set()
for targets in target_df['targets'].str.split(';'):
    all_targets.update(targets)

# 免疫相关靶点
immune_tgts = get_immune_targets()
common_targets = list(all_targets & immune_tgts)

print(f"Total unique targets: {len(all_targets)}")
print(f"Immune-related targets: {len(common_targets)}")

if len(common_targets) > 0:
    # KEGG富集
    kegg_enrich = gp.enrichr(
        gene_list=common_targets,
        gene_sets='KEGG_2021_Human',
        organism='Human',
        outdir='kegg_results',
        no_plot=True
    )

    # 免疫相关通路筛选
    immune_pathways = ['T cell receptor', 'NK cell', 'PD-L1', 'PD-1',
                       'NF-kappa B', 'TNF', 'IL-17', 'JAK-STAT',
                       'PI3K-Akt', 'Toll-like receptor', 'NOD-like receptor',
                       'Cytokine-cytokine receptor', 'Chemokine',
                       'Antigen processing', 'Natural killer']

    results = kegg_enrich.results
    immune_results = results[
        results['Term'].apply(
            lambda t: any(kw.lower() in t.lower() for kw in immune_pathways)
        )
    ]

    # 通路气泡图
    from gseapy.plot import dotplot
    dotplot(kegg_enrich.results, title='KEGG Immune Pathways',
            figsize=(10, 8))
    plt.savefig('kegg_immune_pathways.png', dpi=300, bbox_inches='tight')

    # GO-BP富集
    go_bp = gp.enrichr(
        gene_list=common_targets,
        gene_sets='GO_Biological_Process_2023',
        organism='Human',
        outdir='go_bp_results',
        no_plot=True
    )

    # 免疫相关GO筛选
    immune_go_kw = ['T cell activation', 'immune response', 'cytokine',
                    'antigen presentation', 'leukocyte', 'lymphocyte',
                    'inflammatory', 'NF-kB', 'JAK-STAT']
    go_results = go_bp.results
    go_immune = go_results[
        go_results['Term'].apply(
            lambda t: any(kw.lower() in t.lower() for kw in immune_go_kw)
        )
    ]
```

### 3.2 富集分析可视化

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_go_kegg_summary(kegg_df, go_df, top_n=15):
    """整合GO/KEGG结果"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))

    # KEGG气泡图
    top_kegg = kegg_df.head(top_n)
    axes[0].scatter(
        -np.log10(top_kegg['Adjusted P-value']),
        range(len(top_kegg)),
        s=top_kegg['Overlap'].str.split('/').str[0].astype(int) * 20,
        alpha=0.6
    )
    axes[0].set_yticks(range(len(top_kegg)))
    axes[0].set_yticklabels(top_kegg['Term'].str[:50])
    axes[0].set_xlabel('-log10(Adjusted P-value)')
    axes[0].set_title('KEGG Pathway Enrichment')

    # GO气泡图
    top_go = go_df.head(top_n)
    axes[1].scatter(
        -np.log10(top_go['Adjusted P-value']),
        range(len(top_go)),
        s=top_go['Overlap'].str.split('/').str[0].astype(int) * 20,
        alpha=0.6
    )
    axes[1].set_yticks(range(len(top_go)))
    axes[1].set_yticklabels(top_go['Term'].str[:50])
    axes[1].set_xlabel('-log10(Adjusted P-value)')
    axes[1].set_title('GO Biological Process Enrichment')

    plt.tight_layout()
    plt.savefig('enrichment_summary.png', dpi=300)
```

---

## 四、PPI网络构建与Hub基因识别

### 4.1 STRING网络获取

```python
def build_ppi_network(target_genes, score_threshold=400):
    """通过STRING API构建PPI"""
    url = "https://string-db.org/api/json/network"

    # STRING每次最多查询100个基因，分批处理
    batch_size = 100
    all_interactions = []

    for i in range(0, len(target_genes), batch_size):
        batch = target_genes[i:i+batch_size]
        params = {
            'identifiers': '%0d'.join(batch),
            'species': 9606,
            'required_score': score_threshold,
            'network_type': 'physical',  # 物理相互作用
        }

        resp = requests.post(f"{url}", data=params)
        interactions = resp.json()

        for interaction in interactions:
            all_interactions.append({
                'source': interaction['preferredName_A'],
                'target': interaction['preferredName_B'],
                'score': interaction['score'],
                'experiments': interaction['experiments'],
                'database': interaction['database']
            })

    ppi_df = pd.DataFrame(all_interactions)
    ppi_df.to_csv('ppi_network_string.csv', index=False)
    return ppi_df
```

### 4.2 Cytoscape自动导出

```python
# 通过py4cytoscape导出
# 需先启动Cytoscape
import py4cytoscape as p4c

def export_to_cytoscape(ppi_df, node_info_df):
    """将PPI网络发送到Cytoscape"""
    try:
        # 创建网络
        net = p4c.networks.create_network_from_data_frames(
            edges=ppi_df,
            nodes=node_info_df,
            title="TCM-Immune PPI Network",
            collection="TCM Immuno"
        )

        # 应用样式
        p4c.styles.create_visual_style(
            "tcm_immune_style",
            defaults={
                'NODE_SIZE': 40,
                'NODE_FILL_COLOR': '#E41A1C',
                'EDGE_WIDTH': 3
            }
        )

        # 导出网络文件
        p4c.export_image("tcm_ppi_network", type='PNG')
        print("Network exported to Cytoscape")

    except Exception as e:
        print(f"Cytoscape connection failed: {e}")
        print("Saving as CSV for manual import")
        ppi_df.to_csv('ppi_for_cytoscape.csv', index=False)
```

### 4.3 Python网络分析 (无需Cytoscape)

```python
import networkx as nx

G = nx.from_pandas_edgelist(ppi_df, 'source', 'target',
                            edge_attr='score')

# 网络指标
centrality = {
    'degree': nx.degree_centrality(G),
    'betweenness': nx.betweenness_centrality(G),
    'closeness': nx.closeness_centrality(G),
}

# 合并
cent_df = pd.DataFrame(centrality)
cent_df['hub_score'] = (
    cent_df['degree'].rank(pct=True) +
    cent_df['betweenness'].rank(pct=True) +
    cent_df['closeness'].rank(pct=True)
) / 3

# 识别Hub基因
hub_genes = cent_df.nlargest(20, 'hub_score')
print("Top Hub Genes:")
print(hub_genes)

plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.3, iterations=50)
nx.draw(G, pos, node_size=[G.degree(n)*30 for n in G.nodes()],
        node_color='lightblue', edge_color='gray',
        with_labels=True, font_size=8)
plt.savefig('ppi_network.png', dpi=300, bbox_inches='tight')
```

---

## 五、网络构建与可视化

### 5.1 中药-成分-靶点-通路网络

```python
# 构建四层网络
import networkx as nx

G_total = nx.Graph()

# 添加节点
for _, row in compound_df.iterrows():
    G_total.add_node(f"c_{row['compound']}",
                     type='compound',
                     herb=row['herb'])

for target in common_targets:
    G_total.add_node(f"t_{target}", type='target')

for pathway in important_pathways:
    G_total.add_node(f"p_{pathway}", type='pathway')

# 添加边
# 成分-靶点
for _, row in compound_target_df.iterrows():
    G_total.add_edge(f"c_{row['compound']}",
                     f"t_{row['target']}",
                     type='compound-target')

# 靶点-通路
for target, pathways in target_pathway_dict.items():
    for pathway in pathways[:3]:  # 每个靶点取前3个通路
        G_total.add_edge(f"t_{target}",
                         f"p_{pathway}",
                         type='target-pathway')
```

---

## 六、结果报告模板

### 6.1 标准输出表

| 输出内容 | 格式 | 说明 |
|---------|------|------|
| 活性成分列表 | CSV | 含OB/DL/Caco-2值 |
| 靶点-成分关联 | CSV | 成分-靶点-中药三元组 |
| KEGG富集结果 | CSV+图 | Top20通路+P值 |
| GO富集结果 | CSV+图 | Top20 GO terms |
| Hub基因列表 | CSV | PPI拓扑指标 |
| 成分-靶点网络图 | PNG/SVG | Cytoscape或matplotlib |

---

## 七、本仓库19味中药网络药理学快速启动

```python
# 一键运行: 19味中药 -> 网络药理学
# 前提: compounds.csv 和 targets.csv 已准备

herbs_19 = [
    'sappan', 'dandelion', 'honeysuckle', 'houttuynia',
    'prunella', 'portulaca', 'magnolia', 'rubia',
    'paeonia', 'platycodon', 'chelidonium', 'zanthoxylum',
    'lindera', 'sanguisorba', 'vitex', 'morus',
    'bidens', 'morinda', 'callicarpa'
]

all_networks = {}
for herb in herbs_19:
    print(f"\nAnalyzing {herb}...")

    # 获取成分
    compounds = pd.read_csv(f'data/{herb}_compounds.csv')

    # 获取靶点
    targets = pd.read_csv(f'data/{herb}_targets.csv')

    # 交集分析
    immune_tgts = get_immune_targets()
    common = list(set(targets['target']) & immune_tgts)

    print(f"  Compounds: {len(compounds)}")
    print(f"  Immune targets: {len(common)}")

    all_networks[herb] = {
        'compounds': compounds,
        'targets': targets,
        'immune_targets': common
    }

# 整合分析（全库交集）
all_immune_targets = set()
for herb, data in all_networks.items():
    all_immune_targets.update(data['immune_targets'])

print(f"\nTotal immune targets across 19 herbs: {len(all_immune_targets)}")
```

---

> **引用工具**:
> - Cytoscape: Shannon et al., Genome Res, 2003
> - clusterProfiler: Wu et al., Innovation, 2021
> - NetworkX: Hagberg et al., SciPy, 2008
> - gseapy: Kuleshov et al., Nucleic Acids Res, 2016
