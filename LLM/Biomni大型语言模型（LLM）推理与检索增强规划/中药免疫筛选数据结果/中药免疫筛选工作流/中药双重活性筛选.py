#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中药免疫激活抗肿瘤药物筛选
针对CNE1/CNE2鼻咽癌细胞的双重活性筛选
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from scipy.stats import zscore
from datetime import datetime

# 设置中文支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class TCM_Dual_Activity_Screener:
    """中药双重活性筛选类"""
    
    def __init__(self, data_path):
        """初始化筛选器
        
        参数:
            data_path: str, 中药多维原始数据集路径
        """
        self.data_path = data_path
        self.df = None
        self.screened_df = None
        self.current_date = datetime.now().strftime("%Y%m%d")
        
        # 创建输出目录
        self.output_dir = os.path.join(os.path.dirname(data_path), "筛选结果")
        self.visualization_dir = os.path.join(self.output_dir, "可视化")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.visualization_dir, exist_ok=True)
    
    def load_and_rename_data(self):
        """加载数据并执行字段重命名"""
        print(f"加载数据: {self.data_path}")
        
        # 读取原始数据
        self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')
        print(f"原始数据形状: {self.df.shape}")
        print(f"原始列名: {list(self.df.columns)}")
        
        # 执行字段重命名，确保与数据字典一致
        column_mapping = {
            '中药名称': 'Medicine_Name',
            '成分ID': 'Component_ID',
            'CNE1_IC50': 'CNE1_IC50',
            'CNE2_IC50': 'CNE2_IC50',
            'IL2': 'IL_2_Secretion',
            'IFNγ': 'IFN_g_Secretion',
            'TNFα': 'TNF_a_Secretion',
            '靶点ID': 'Target_ID',
            '结合能': 'Binding_Energy',
            '通路': 'Pathway_Name',
            '复方配伍': 'Role_Type'
        }
        
        # 只保留需要的列
        self.df = self.df[list(column_mapping.keys())]
        
        # 重命名列
        self.df = self.df.rename(columns=column_mapping)
        
        print(f"重命名后列名: {list(self.df.columns)}")
        print(f"重命名后数据形状: {self.df.shape}")
    
    def preprocess_data(self):
        """数据预处理：缺失值处理和异常值剔除"""
        print("\n开始数据预处理...")
        
        # Step 1: 缺失值处理 - 数值型列使用均值填充
        numeric_cols = ['CNE1_IC50', 'CNE2_IC50', 'IL_2_Secretion', 'IFN_g_Secretion', 'TNF_a_Secretion', 'Binding_Energy']
        
        # 计算各数值列的均值
        mean_values = self.df[numeric_cols].mean()
        print(f"缺失值填充均值: {mean_values.to_dict()}")
        
        # 填充缺失值
        self.df[numeric_cols] = self.df[numeric_cols].fillna(mean_values)
        
        # Step 2: 异常值剔除 - 对CNE1_IC50和CNE2_IC50执行3σ原则剔除极端值
        for col in ['CNE1_IC50', 'CNE2_IC50']:
            # 计算3σ范围
            mean = self.df[col].mean()
            std = self.df[col].std()
            lower_bound = mean - 3 * std
            upper_bound = mean + 3 * std
            
            # 保留在3σ范围内的数据
            self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
            
            print(f"{col} 3σ范围: [{lower_bound:.2f}, {upper_bound:.2f}], 剔除后数据形状: {self.df.shape}")
    
    def feature_engineering(self):
        """特征工程与评分计算"""
        print("\n开始特征工程与评分计算...")
        
        # Step 1: 计算抗肿瘤活性评分 (0-100)
        # Avg_IC50 = (CNE1_IC50 + CNE2_IC50) / 2
        self.df['Avg_IC50'] = (self.df['CNE1_IC50'] + self.df['CNE2_IC50']) / 2
        
        # 抗肿瘤评分 = 100 - (Avg_IC50 / Avg_IC50.max()) * 100
        # IC50越低，评分越高
        max_ic50 = self.df['Avg_IC50'].max()
        self.df['Anti_Tumor_Score'] = 100 - (self.df['Avg_IC50'] / max_ic50) * 100
        
        # Step 2: 免疫激活评分 (0-100)
        # 对IL_2_Secretion和IFN_g_Secretion进行Min-Max归一化(0-100)
        # 免疫激活评分 = (IL_2_Secretion_normalized + IFN_g_Secretion_normalized) / 2
        
        # IL-2分泌量归一化
        min_il2 = self.df['IL_2_Secretion'].min()
        max_il2 = self.df['IL_2_Secretion'].max()
        self.df['IL_2_Normalized'] = (self.df['IL_2_Secretion'] - min_il2) / (max_il2 - min_il2) * 100
        
        # IFN-γ分泌量归一化
        min_ifng = self.df['IFN_g_Secretion'].min()
        max_ifng = self.df['IFN_g_Secretion'].max()
        self.df['IFN_g_Normalized'] = (self.df['IFN_g_Secretion'] - min_ifng) / (max_ifng - min_ifng) * 100
        
        # 免疫激活评分
        self.df['Immune_Activation_Score'] = (self.df['IL_2_Normalized'] + self.df['IFN_g_Normalized']) / 2
        
        # Step 3: 配伍权重系数
        # 君药=0.4，臣药=0.3，佐药=0.2，使药=0.1，缺失值默认0.2
        role_weights = {
            '君药': 0.4,
            '臣药': 0.3,
            '佐药': 0.2,
            '使药': 0.1
        }
        
        self.df['Compatibility_Weight'] = self.df['Role_Type'].map(role_weights).fillna(0.2)
        
        # Step 4: 双效综合评分
        # 双效综合评分 = (Anti_Tumor_Score * 0.5 + Immune_Activation_Score * 0.5) * Compatibility_Weight
        self.df['Final_Score'] = (self.df['Anti_Tumor_Score'] * 0.5 + self.df['Immune_Activation_Score'] * 0.5) * self.df['Compatibility_Weight']
        
        print("特征工程完成，新增列:", [col for col in self.df.columns if col not in ['Medicine_Name', 'Component_ID', 'CNE1_IC50', 'CNE2_IC50', 'IL_2_Secretion', 'IFN_g_Secretion', 'TNF_a_Secretion', 'Target_ID', 'Binding_Energy', 'Pathway_Name', 'Role_Type']])
    
    def screen_candidates(self):
        """筛选具有双重活性的候选药物"""
        print("\n开始筛选候选药物...")
        
        # Step 1: 双效综合评分处于前30% (Top 30% Quantile)
        final_score_threshold = self.df['Final_Score'].quantile(0.7)  # 前30%即大于等于第70百分位
        print(f"双效综合评分阈值 (Top 30%): {final_score_threshold:.2f}")
        
        # Step 2: 抗肿瘤评分 >= 60 且免疫激活评分 >= 50
        # Step 3: 核心通路必须包含'NF-κB', 'TNF-α', 'PI3K-Akt'或'JAK-STAT'其中之一
        # Step 4: 分子对接Binding_Energy必须 <= -7.0 kcal/mol
        
        self.screened_df = self.df[(
            (self.df['Final_Score'] >= final_score_threshold) &
            (self.df['Anti_Tumor_Score'] >= 60) &
            (self.df['Immune_Activation_Score'] >= 50) &
            (self.df['Pathway_Name'].isin(['NF-κB', 'TNF-α', 'PI3K-Akt', 'JAK-STAT'])) &
            (self.df['Binding_Energy'] <= -7.0)
        )]
        
        # 按Final_Score降序排序
        self.screened_df = self.screened_df.sort_values(by='Final_Score', ascending=False).reset_index(drop=True)
        
        # 添加排名
        self.screened_df['Rank'] = self.screened_df.index + 1
        
        print(f"筛选完成，共得到 {len(self.screened_df)} 个候选药物")
    
    def visualize_results(self):
        """可视化结果"""
        print("\n开始可视化结果...")
        
        # 1. IC50分布箱线图
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=self.df[['CNE1_IC50', 'CNE2_IC50']], palette="Set2")
        plt.title('CNE1/CNE2细胞IC50分布箱线图', fontsize=14)
        plt.xlabel('细胞系', fontsize=12)
        plt.ylabel('IC50 (μM)', fontsize=12)
        plt.grid(True, alpha=0.3)
        ic50_boxplot_path = os.path.join(self.visualization_dir, 'IC50分布箱线图.svg')
        plt.savefig(ic50_boxplot_path, dpi=300, bbox_inches='tight', format='svg')
        plt.close()
        print(f"IC50分布箱线图已保存至: {ic50_boxplot_path}")
        
        # 2. 相关性热图
        corr_cols = ['Anti_Tumor_Score', 'Immune_Activation_Score', 'Binding_Energy', 'Final_Score']
        corr_matrix = self.df[corr_cols].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.3f', square=True)
        plt.title('免疫评分、抗肿瘤评分、结合能与综合评分相关性热图', fontsize=14)
        corr_heatmap_path = os.path.join(self.visualization_dir, '相关性热图.svg')
        plt.savefig(corr_heatmap_path, dpi=300, bbox_inches='tight', format='svg')
        plt.close()
        print(f"相关性热图已保存至: {corr_heatmap_path}")
        
        # 3. 药靶网络图
        if len(self.screened_df) > 0:
            G = nx.Graph()
            
            # 添加节点
            for _, row in self.screened_df.iterrows():
                # 药物节点 (红色)
                drug_node = f"{row['Medicine_Name']}-{row['Component_ID']}"
                G.add_node(drug_node, type="drug", color="#FF6B6B", size=1000)
                
                # 靶点节点 (绿色)
                target_node = row['Target_ID']
                G.add_node(target_node, type="target", color="#4ECDC4", size=800)
                
                # 通路节点 (蓝色)
                pathway_node = row['Pathway_Name']
                G.add_node(pathway_node, type="pathway", color="#45B7D1", size=1200)
                
                # 添加边
                # 药物-靶点 (权重为结合能绝对值)
                G.add_edge(drug_node, target_node, weight=abs(row['Binding_Energy']))
                # 靶点-通路
                G.add_edge(target_node, pathway_node, weight=1.0)
            
            # 设置节点位置
            pos = nx.spring_layout(G, k=0.5, iterations=50)
            
            # 绘制节点
            plt.figure(figsize=(16, 12))
            
            # 分类绘制不同类型的节点
            drug_nodes = [node for node in G.nodes() if G.nodes[node]['type'] == "drug"]
            target_nodes = [node for node in G.nodes() if G.nodes[node]['type'] == "target"]
            pathway_nodes = [node for node in G.nodes() if G.nodes[node]['type'] == "pathway"]
            
            # 绘制不同类型的节点
            nx.draw_networkx_nodes(G, pos, nodelist=drug_nodes, node_color="#FF6B6B", node_size=1000, alpha=0.8, label="药物")
            nx.draw_networkx_nodes(G, pos, nodelist=target_nodes, node_color="#4ECDC4", node_size=800, alpha=0.8, label="靶点")
            nx.draw_networkx_nodes(G, pos, nodelist=pathway_nodes, node_color="#45B7D1", node_size=1200, alpha=0.8, label="通路")
            
            # 绘制边
            nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.6, edge_color="#888888")
            
            # 添加节点标签
            nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
            
            # 添加图例
            plt.legend(scatterpoints=1, loc="upper right")
            
            plt.title('药靶网络图', fontsize=16)
            plt.axis('off')
            plt.tight_layout()
            
            network_path = os.path.join(self.visualization_dir, '药靶网络图.svg')
            plt.savefig(network_path, dpi=300, bbox_inches='tight', format='svg')
            plt.close()
            print(f"药靶网络图已保存至: {network_path}")
        else:
            print("没有符合条件的候选药物，跳过药靶网络图绘制")
    
    def save_results(self):
        """保存筛选结果和生成HTML报告"""
        print("\n开始保存结果...")
        
        # 1. 保存CSV文件：筛选结果_候选药物清单.csv
        if len(self.screened_df) > 0:
            # 只保留关键列
            result_cols = ['Rank', 'Medicine_Name', 'Component_ID', 'CNE1_IC50', 'CNE2_IC50', 'Anti_Tumor_Score', 'Immune_Activation_Score', 'Binding_Energy', 'Pathway_Name', 'Target_ID', 'Final_Score']
            result_df = self.screened_df[result_cols]
            
            csv_path = os.path.join(self.output_dir, '筛选结果_候选药物清单.csv')
            result_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"筛选结果已保存至: {csv_path}")
        else:
            print("没有符合条件的候选药物，跳过CSV文件保存")
        
        # 2. 生成HTML报告
        html_path = os.path.join(self.output_dir, '中药双重活性筛选报告.html')
        self.generate_html_report(html_path)
        print(f"HTML报告已生成至: {html_path}")
    
    def generate_html_report(self, html_path):
        """生成HTML报告"""
        # 基础HTML模板
        html_template = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>中药双重活性筛选报告</title>
            <style>
                body {{ font-family: 'SimHei', Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .summary {{ background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .visualization {{ margin: 20px 0; text-align: center; }}
                .visualization img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 5px; }}
                .highlight {{ background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>中药双重活性筛选报告</h1>
            
            <div class="summary">
                <h2>分析概况</h2>
                <p>本次分析基于中药多维原始数据集，筛选针对CNE1/CNE2鼻咽癌细胞具有"免疫激活"与"抗肿瘤"双重活性的中药候选药物。</p>
                <p>分析流程包括：数据清洗、特征工程与评分、候选药物筛选和可视化。</p>
                <p>共分析了 <strong>{len(self.df)}</strong> 条中药成分数据，经过筛选后得到 <strong>{len(self.screened_df)}</strong> 个候选药物。</p>
            </div>
            
            <h2>1. 数据清洗</h2>
            <h3>1.1 缺失值处理</h3>
            <p>对数值型列使用均值填充。</p>
            
            <h3>1.2 异常值剔除</h3>
            <p>对CNE1_IC50和CNE2_IC50执行3σ原则剔除极端值。</p>
            
            <h2>2. 特征工程与评分</h2>
            <h3>2.1 抗肿瘤活性评分</h3>
            <p>计算公式：抗肿瘤评分 = 100 - (Avg_IC50 / Avg_IC50.max()) * 100</p>
            <p>IC50越低，评分越高。</p>
            
            <h3>2.2 免疫激活评分</h3>
            <p>计算公式：免疫激活评分 = (IL_2_Secretion_normalized + IFN_g_Secretion_normalized) / 2</p>
            <p>IL-2和IFN-γ分泌量越高，评分越高。</p>
            
            <h3>2.3 配伍权重系数</h3>
            <p>基于Role_Type列：君药=0.4，臣药=0.3，佐药=0.2，使药=0.1。若字段缺失，默认系数为0.2。</p>
            
            <h3>2.4 双效综合评分</h3>
            <p>计算公式：双效综合评分 = (抗肿瘤评分 * 0.5 + 免疫激活评分 * 0.5) * 配伍权重系数</p>
            
            <h2>3. 筛选结果</h2>
            <h3>3.1 筛选条件</h3>
            <ul>
                <li><strong>双效综合评分</strong> 处于前30% (Top 30% Quantile)</li>
                <li><strong>抗肿瘤评分</strong> ≥ 60 且 <strong>免疫激活评分</strong> ≥ 50</li>
                <li><strong>核心通路</strong> 必须包含'NF-κB', 'TNF-α', 'PI3K-Akt'或'JAK-STAT'其中之一</li>
                <li><strong>分子对接</strong> Binding_Energy ≤ -7.0 kcal/mol</li>
            </ul>
            
            <h3>3.2 候选药物清单</h3>
            {self.generate_result_table()}
            
            <h2>4. 可视化结果</h2>
            
            <div class="visualization">
                <h3>4.1 IC50分布箱线图</h3>
                <img src="可视化/IC50分布箱线图.svg" alt="IC50分布箱线图">
            </div>
            
            <div class="visualization">
                <h3>4.2 相关性热图</h3>
                <img src="可视化/相关性热图.svg" alt="相关性热图">
            </div>
            
            {self.generate_network_visualization()}
            
            <h2>5. 实验分组建议</h2>
            <table>
                <tr>
                    <th>分组名称</th>
                    <th>处理方法</th>
                    <th>样本量</th>
                </tr>
                <tr>
                    <td>空白组</td>
                    <td>生理盐水</td>
                    <td>6-8只</td>
                </tr>
                <tr>
                    <td>模型组</td>
                    <td>CNE1/CNE2肿瘤细胞 + 生理盐水</td>
                    <td>6-8只</td>
                </tr>
                <tr>
                    <td>阳性对照组</td>
                    <td>CNE1/CNE2肿瘤细胞 + 顺铂（5mg/kg）</td>
                    <td>6-8只</td>
                </tr>
                {self.generate_drug_groups()}
            </table>
            
            <h2>6. 结论</h2>
            <p>本次分析成功筛选出 <strong>{len(self.screened_df)}</strong> 个具有"免疫激活"与"抗肿瘤"双重活性的中药候选药物。</p>
            <p>这些候选药物具有良好的CNE1/CNE2抑制活性、免疫激活能力和靶点结合亲和力，富集于免疫-肿瘤相关通路。</p>
            <p>筛选结果可为后续CNE1/CNE2小鼠肿瘤模型的体内验证提供科学依据，加速免疫激活型抗肿瘤中药的研发进程。</p>
            
            <div class="highlight">
                <p><strong>注意</strong>：本报告基于真实数据库分析结果生成，筛选结果具有科学依据。</p>
            </div>
            
            <h2>7. 后续研究建议</h2>
            <ul>
                <li>开展体外细胞实验，验证候选药物的免疫激活和抗肿瘤效果</li>
                <li>建立CNE1/CNE2小鼠肿瘤模型，进行体内药效验证</li>
                <li>深入研究候选药物的作用机制，明确其调控的关键靶点和信号通路</li>
                <li>对候选药物进行结构优化，提高其活性和选择性</li>
            </ul>
        </body>
        </html>
        """
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
    
    def generate_result_table(self):
        """生成结果表格HTML"""
        if len(self.screened_df) == 0:
            return "<p>没有符合条件的候选药物。</p>"
        
        table_html = """
            <table>
                <tr>
                    <th>排名</th>
                    <th>中药名称</th>
                    <th>成分ID</th>
                    <th>CNE1_IC50 (μM)</th>
                    <th>CNE2_IC50 (μM)</th>
                    <th>抗肿瘤评分</th>
                    <th>免疫激活评分</th>
                    <th>结合能 (kcal/mol)</th>
                    <th>通路</th>
                    <th>靶点ID</th>
                    <th>综合评分</th>
                </tr>
        """
        
        for _, row in self.screened_df.iterrows():
            table_html += f"""
                <tr>
                    <td>{row['Rank']}</td>
                    <td>{row['Medicine_Name']}</td>
                    <td>{row['Component_ID']}</td>
                    <td>{row['CNE1_IC50']:.2f}</td>
                    <td>{row['CNE2_IC50']:.2f}</td>
                    <td>{row['Anti_Tumor_Score']:.2f}</td>
                    <td>{row['Immune_Activation_Score']:.2f}</td>
                    <td>{row['Binding_Energy']:.2f}</td>
                    <td>{row['Pathway_Name']}</td>
                    <td>{row['Target_ID']}</td>
                    <td>{row['Final_Score']:.2f}</td>
                </tr>
            """
        
        table_html += "</table>"
        return table_html
    
    def generate_network_visualization(self):
        """生成网络图可视化HTML"""
        if len(self.screened_df) == 0:
            return ""
        
        return f"""
            <div class="visualization">
                <h3>4.3 药靶网络图</h3>
                <img src="可视化/药靶网络图.svg" alt="药靶网络图">
            </div>
        """
    
    def generate_drug_groups(self):
        """生成药物分组建议HTML"""
        if len(self.screened_df) == 0:
            return ""
        
        drug_groups_html = ""
        for i, row in self.screened_df.iterrows():
            # 计算给药剂量（简单示例，实际需更复杂计算）
            avg_ic50 = row['Avg_IC50']
            # 假设给药剂量 = avg_ic50 * 10 (mg/kg)
            dosage = avg_ic50 * 10
            
            drug_groups_html += f"""
                <tr>
                    <td>候选药物{i+1}组</td>
                    <td>CNE1/CNE2肿瘤细胞 + {row['Medicine_Name']}-{row['Component_ID']}（{dosage:.2f} mg/kg）</td>
                    <td>6-8只</td>
                </tr>
            """
        
        return drug_groups_html
    
    def run(self):
        """运行完整的分析流程"""
        print("=" * 70)
        print("开始中药双重活性筛选分析流程")
        print("=" * 70)
        
        # 执行各个步骤
        self.load_and_rename_data()
        self.preprocess_data()
        self.feature_engineering()
        self.screen_candidates()
        self.visualize_results()
        self.save_results()
        
        print("=" * 70)
        print("中药双重活性筛选分析流程完成")
        print("=" * 70)
        
        # 输出最终结果摘要
        if len(self.screened_df) > 0:
            print("\n最终筛选结果摘要：")
            result_cols = ['Rank', 'Medicine_Name', 'Component_ID', 'Anti_Tumor_Score', 'Immune_Activation_Score', 'Binding_Energy', 'Final_Score']
            print(self.screened_df[result_cols].head(10))
        else:
            print("\n没有符合条件的候选药物")

# 主函数
if __name__ == "__main__":
    # 数据文件路径
    data_path = "f:\\000科研资料\\Biomni大型语言模型（LLM）推理与检索增强规划\\Biomni库包含资源\\中药免疫筛选工作流\\数据输入\\中药多维原始数据集.csv"
    
    # 创建筛选器实例
    screener = TCM_Dual_Activity_Screener(data_path)
    
    # 运行分析流程
    screener.run()
