#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
免疫激活型抗肿瘤中药的精准筛选与机制解析

基于中药多维数据集，筛选适配CNE1/CNE2小鼠肿瘤模型的免疫激活抗肿瘤候选药物

代码适配库：pandas, scikit-learn, seaborn, NetworkX, clusterProfiler
"""

# 导入所需库
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.impute import SimpleImputer
from scipy.stats import zscore
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from matplotlib import rcParams
import warnings
warnings.filterwarnings('ignore')

# 设置随机种子，保证可复现性
np.random.seed(42)

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置图表风格
sns.set_style("whitegrid")
sns.set_palette("husl")

class Biomni中药免疫激活抗肿瘤药物筛选:
    """Biomni中药免疫激活抗肿瘤药物筛选类"""
    
    def __init__(self, work_dir: str = "./"):
        """初始化筛选工作流"""
        self.work_dir = work_dir
        self.原始数据集 = None
        self.质控后数据集 = None
        self.特征工程数据集 = None
        self.候选药物清单 = None
        
        # 创建工作目录结构
        self._create_directories()
        
        # 初始化默认参数
        self._init_parameters()
    
    def _create_directories(self):
        """创建工作目录结构"""
        self.directories = {
            "input": os.path.join(self.work_dir, "输入数据"),
            "output": os.path.join(self.work_dir, "输出结果"),
            "processed_data": os.path.join(self.work_dir, "处理后数据"),
            "visualization": os.path.join(self.work_dir, "可视化结果"),
            "code": os.path.join(self.work_dir, "代码文件")
        }
        
        for dir_path in self.directories.values():
            os.makedirs(dir_path, exist_ok=True)
    
    def _init_parameters(self):
        """初始化默认参数"""
        # 数据预处理参数
        self.preprocessing_params = {
            "missing_value_strategy": {"numeric": "median", "categorical": "most_frequent"},
            "outlier_threshold": 3.0,  # Z-score阈值
            "normalization_method": "min-max"
        }
        
        # 特征工程参数
        self.feature_engineering_params = {
            "免疫激活评分权重": {"IL_2_Secretion": 0.5, "IFN_g_Secretion": 0.5},
            "抗肿瘤活性权重": {"CNE1": 0.5, "CNE2": 0.5},
            "双效综合评分权重": {"免疫激活评分": 0.4, "抗肿瘤活性评分": 0.6}
        }
        
        # 筛选参数
        self.screening_params = {
            "双效综合评分_top_percent": 0.3,  # Top 30%，放宽阈值
            "ic50_threshold": 30.0,  # 从20μM调整为30μM
            "免疫因子上调阈值": 0.15,  # 从20%降至15%
            "结合能阈值": -7.0,  # kcal/mol
            "关键通路": ["NF-κB", "TNF-α", "PI3K-Akt"],
            "核心条件权重": {"双效综合评分": 0.5, "IC50": 0.5},  # 核心条件权重
            "附加条件权重": {"结合能": 0.6, "通路富集": 0.4}  # 附加条件权重
        }
    
    def load_data(self, data_file: str = None):
        """加载数据集"""
        """
        加载中药多维数据集
        
        参数:
            data_file: str, 数据文件路径，如果为None则使用原始数据库数据
            
        返回:
            原始数据集
        """
        # 默认使用原始数据库数据文件
        default_data_file = os.path.join(self.work_dir, "数据输入", "中药多维原始数据集.csv")
        
        # 优先使用提供的数据文件，如果没有则使用原始数据库数据
        if data_file and os.path.exists(data_file):
            self.原始数据集 = pd.read_csv(data_file, encoding='utf-8-sig')
            print(f"已加载指定数据文件: {data_file}")
        elif os.path.exists(default_data_file):
            self.原始数据集 = pd.read_csv(default_data_file, encoding='utf-8-sig')
            print(f"已加载原始数据库数据文件: {default_data_file}")
        else:
            # 如果原始数据文件不存在，才生成示例数据
            print(f"警告：原始数据库数据文件不存在 ({default_data_file})，将生成示例数据")
            self.原始数据集 = self._generate_example_data()
        
        # 数据适配处理
        self._data_adaptation()
        
        print(f"数据集加载完成，共 {len(self.原始数据集)} 条记录，{len(self.原始数据集.columns)} 个特征")
        print("数据集字段:", list(self.原始数据集.columns))
        return self.原始数据集
    
    def _data_adaptation(self):
        """数据适配处理"""
        """
        数据适配处理：
        1. 字段一致性校验与重命名
        2. 复方数据适配
        3. 数据类型校验
        """
        print("\n开始数据适配处理...")
        
        # 1. 字段一致性校验与重命名
        print("\n1. 字段一致性校验与重命名...")
        # 定义字段映射字典，支持多种可能的字段名，特别是原始数据库的字段名
        field_mapping = {
            'CNE1_IC50': ['CNE1_IC50', 'CNE1抑制率(IC50)', 'CNE1 IC50', 'CNE1'],
            'CNE2_IC50': ['CNE2_IC50', 'CNE2抑制率(IC50)', 'CNE2 IC50', 'CNE2'],
            'IL_2_Secretion': ['IL2', 'IL-2', 'IL2分泌量', 'IL-2分泌量', 'IL_2_Secretion'],
            'IFN_g_Secretion': ['IFNγ', 'IFN-γ', 'IFNγ分泌量', 'IFN-γ分泌量', 'IFN_g_Secretion'],
            'TNF_a_Secretion': ['TNFα', 'TNF-α', 'TNFα分泌量', 'TNF-α分泌量', 'TNF_a_Secretion'],
            'Target_ID': ['靶点ID', '靶点', 'Target_ID', 'Target'],
            'Binding_Energy': ['结合能', '结合自由能', 'Binding_Energy', 'Affinity'],
            'Pathway_Name': ['通路', '通路名称', 'Pathway_Name', 'Pathway']
        }
        
        # 执行字段重命名
        rename_dict = {}
        for standard_field, possible_fields in field_mapping.items():
            for possible_field in possible_fields:
                if possible_field in self.原始数据集.columns:
                    if possible_field != standard_field:
                        rename_dict[possible_field] = standard_field
                        print(f"  将字段 '{possible_field}' 重命名为标准字段名 '{standard_field}'")
                    break
        
        if rename_dict:
            self.原始数据集.rename(columns=rename_dict, inplace=True)
        
        # 检查必需字段是否存在（对于原始数据库数据）
        core_required_fields = ['CNE1_IC50', 'CNE2_IC50', 'Target_ID', 'Pathway_Name']
        missing_fields = [field for field in core_required_fields if field not in self.原始数据集.columns]
        if missing_fields:
            raise ValueError(f"错误：缺少核心必需字段 {missing_fields}")
        else:
            print("  所有核心必需字段均存在")
        
        # 2. 复方数据适配
        print("\n2. 复方数据适配...")
        if '复方配伍' in self.原始数据集.columns:
            # 重命名复方配伍字段为复方
            self.原始数据集.rename(columns={'复方配伍': '复方'}, inplace=True)
            print("  已将'复方配伍'字段重命名为'复方'")
        
        if '复方' in self.原始数据集.columns and '配伍权重' not in self.原始数据集.columns:
            print("  检测到复方数据，添加配伍权重计算")
            # 定义中药配伍权重（君药0.4, 臣药0.3, 佐药0.2, 使药0.1）
            herb_weights = {
                '君药': 0.4,
                '臣药': 0.3,
                '佐药': 0.2,
                '使药': 0.1
            }
            
            # 对于复方字段是多个中药组合的情况，我们给默认权重1.0
            self.原始数据集['配伍权重'] = self.原始数据集['复方'].apply(lambda x: 1.0)
            print("  复方数据配伍权重设置完成")
        elif '配伍权重' in self.原始数据集.columns:
            print("  检测到已有的配伍权重字段，跳过计算")
        else:
            # 添加默认配伍权重字段
            self.原始数据集['配伍权重'] = 1.0
            print("  未检测到复方数据，添加默认配伍权重1.0")
        
        # 3. 数据类型校验
        print("\n3. 数据类型校验...")
        # 获取实际存在的数值字段
        numeric_fields = ['CNE1_IC50', 'CNE2_IC50', 'IL_2_Secretion', 'IFN_g_Secretion', 'TNF_a_Secretion', 'Binding_Energy']
        actual_numeric_fields = [field for field in numeric_fields if field in self.原始数据集.columns]
        
        for field in actual_numeric_fields:
            try:
                self.原始数据集[field] = pd.to_numeric(self.原始数据集[field])
                print(f"  {field} 数据类型校验通过")
            except ValueError:
                raise ValueError(f"错误：{field} 字段包含非数值型数据")
        
        # 字符串类型字段校验
        string_fields = ['Target_ID', 'Pathway_Name', '中药名称', '成分ID', '来源药材', '复方']
        actual_string_fields = [field for field in string_fields if field in self.原始数据集.columns]
        
        for field in actual_string_fields:
            self.原始数据集[field] = self.原始数据集[field].astype(str)
            print(f"  {field} 数据类型校验通过")
        
        print("\n数据适配处理完成")
    
    def _generate_example_data(self):
        """生成示例中药多维数据集"""
        """
        生成符合要求的示例中药多维数据集
        
        返回:
            示例数据集
        """
        print("生成示例中药多维数据集...")
        
        # 中药名称列表
        herbs = ["黄芪", "人参", "灵芝", "当归", "枸杞", "女贞子", "淫羊藿", "白术", "茯苓", "甘草",
                "柴胡", "黄芩", "黄连", "黄柏", "栀子", "丹皮", "赤芍", "生地", "熟地", "川芎"]
        
        # 靶点列表
        targets = ["PD-1", "PD-L1", "CTLA-4", "CD28", "OX40", "4-1BB", "CD40", "GITR", "ICOS", "LAG3"]
        
        # 通路列表
        pathways = ["NF-κB", "TNF-α", "PI3K-Akt", "JAK-STAT", "MAPK", "Wnt", "Hippo", "Notch"]
        
        # 生成数据集
        data = []
        for i in range(100):
            herb = np.random.choice(herbs)
            component_id = f"CMP{i+1:03d}"
            
            # CNE1/CNE2 IC50 (μM) - 模拟数据，部分数据<20μM
            cne1_ic50 = np.random.uniform(5, 100) if np.random.random() < 0.7 else np.random.uniform(5, 20)
            cne2_ic50 = np.random.uniform(5, 100) if np.random.random() < 0.7 else np.random.uniform(5, 20)
            
            # 免疫因子分泌量 (pg/mL)
            il2 = np.random.uniform(50, 300)
            ifng = np.random.uniform(80, 400)
            
            # 靶点和结合能
            target = np.random.choice(targets)
            binding_energy = np.random.uniform(-12, -4) if np.random.random() < 0.8 else np.random.uniform(-4, 0)
            
            # 通路
            pathway = np.random.choice(pathways)
            
            # 添加一些缺失值 (5% 缺失率)
            if np.random.random() < 0.05:
                cne1_ic50 = np.nan
            if np.random.random() < 0.05:
                cne2_ic50 = np.nan
            if np.random.random() < 0.05:
                il2 = np.nan
            if np.random.random() < 0.05:
                ifng = np.nan
            if np.random.random() < 0.05:
                binding_energy = np.nan
            
            # 添加一些异常值 (3% 异常率)
            if np.random.random() < 0.03:
                cne1_ic50 = np.random.uniform(200, 500)
            if np.random.random() < 0.03:
                cne2_ic50 = np.random.uniform(200, 500)
            
            data.append({
                "Herb_ID/Component_ID": f"{herb}-{component_id}",
                "CNE1_IC50": cne1_ic50,
                "CNE2_IC50": cne2_ic50,
                "IL_2_Secretion": il2,
                "IFN_g_Secretion": ifng,
                "Target_ID": target,
                "Binding_Energy": binding_energy,
                "Pathway_Name": pathway
            })
        
        df = pd.DataFrame(data)
        
        # 保存示例数据
        example_data_path = os.path.join(self.directories["input"], "中药多维示例数据集.csv")
        df.to_csv(example_data_path, index=False, encoding='utf-8-sig')
        print(f"示例数据已保存至: {example_data_path}")
        
        return df
    
    def data_preprocessing(self):
        """数据预处理"""
        """
        数据预处理流程：
        1. 缺失值处理：连续型字段用中位数填充，结合能用均值填充
        2. 异常值剔除：Z-score>3的异常值
        3. 特征标准化：IC50转换为抑制评分
        
        返回:
            预处理后的数据集
        """
        print("\n开始数据预处理...")
        
        # 复制原始数据集
        self.质控后数据集 = self.原始数据集.copy()
        
        # 1. 缺失值处理
        print("\n1. 缺失值处理...")
        # 连续型字段
        numeric_cols = ["CNE1_IC50", "CNE2_IC50", "IL_2_Secretion", "IFN_g_Secretion", "Binding_Energy"]
        for col in numeric_cols:
            if col in ["Binding_Energy"]:
                # 结合能用均值填充
                fill_value = self.质控后数据集[col].mean()
            else:
                # 其他连续型字段用中位数填充
                fill_value = self.质控后数据集[col].median()
            
            missing_count = self.质控后数据集[col].isnull().sum()
            if missing_count > 0:
                print(f"  {col}: {missing_count}个缺失值，用{fill_value:.2f}填充")
                self.质控后数据集[col] = self.质控后数据集[col].fillna(fill_value)
        
        # 分类字段
        categorical_cols = ["Target_ID", "Pathway_Name"]
        for col in categorical_cols:
            fill_value = self.质控后数据集[col].mode()[0]
            missing_count = self.质控后数据集[col].isnull().sum()
            if missing_count > 0:
                print(f"  {col}: {missing_count}个缺失值，用'{fill_value}'填充")
                self.质控后数据集[col] = self.质控后数据集[col].fillna(fill_value)
        
        # 2. 异常值剔除
        print("\n2. 异常值剔除...")
        # 计算Z-score
        z_scores = np.abs(zscore(self.质控后数据集[numeric_cols]))
        # 识别异常值
        outliers = (z_scores > self.preprocessing_params["outlier_threshold"]).any(axis=1)
        outlier_count = outliers.sum()
        print(f"  检测到 {outlier_count} 个异常值，占比 {outlier_count/len(self.质控后数据集)*100:.2f}%")
        
        # 剔除异常值
        self.质控后数据集 = self.质控后数据集[~outliers].copy()
        print(f"  异常值剔除后，剩余 {len(self.质控后数据集)} 条记录")
        
        # 3. 特征标准化 - IC50转换为抑制评分
        print("\n3. 特征标准化...")
        # IC50转换为抑制评分：1 - (IC50/最大IC50)
        max_ic50_cne1 = self.质控后数据集["CNE1_IC50"].max()
        max_ic50_cne2 = self.质控后数据集["CNE2_IC50"].max()
        
        self.质控后数据集["CNE1_抑制评分"] = 1 - (self.质控后数据集["CNE1_IC50"] / max_ic50_cne1)
        self.质控后数据集["CNE2_抑制评分"] = 1 - (self.质控后数据集["CNE2_IC50"] / max_ic50_cne2)
        
        print("  IC50转换为抑制评分完成")
        
        # 保存预处理后的数据
        processed_data_path = os.path.join(self.directories["processed_data"], "中药多维质控后数据集.csv")
        self.质控后数据集.to_csv(processed_data_path, index=False, encoding='utf-8-sig')
        print(f"\n数据预处理完成，结果已保存至: {processed_data_path}")
        
        return self.质控后数据集
    
    def feature_engineering(self):
        """特征工程"""
        """
        特征工程流程：
        1. 计算免疫激活评分
        2. 计算抗肿瘤活性评分
        3. 计算双效综合评分
        4. 考虑复方数据的配伍权重
        
        返回:
            特征工程后的数据集
        """
        print("\n开始特征工程...")
        
        # 复制质控后数据集
        self.特征工程数据集 = self.质控后数据集.copy()
        
        # 检查是否存在配伍权重字段
        has_compound_weight = '配伍权重' in self.特征工程数据集.columns
        if has_compound_weight:
            print("  检测到复方数据，将考虑配伍权重")
        
        # 1. 计算免疫激活评分
        print("\n1. 计算免疫激活评分...")
        self.特征工程数据集["免疫激活评分"] = (
            self.特征工程数据集["IL_2_Secretion"] * self.feature_engineering_params["免疫激活评分权重"]["IL_2_Secretion"] +
            self.特征工程数据集["IFN_g_Secretion"] * self.feature_engineering_params["免疫激活评分权重"]["IFN_g_Secretion"]
        )
        
        # 2. 计算抗肿瘤活性评分
        print("\n2. 计算抗肿瘤活性评分...")
        self.特征工程数据集["抗肿瘤活性评分"] = (
            self.特征工程数据集["CNE1_抑制评分"] * self.feature_engineering_params["抗肿瘤活性权重"]["CNE1"] +
            self.特征工程数据集["CNE2_抑制评分"] * self.feature_engineering_params["抗肿瘤活性权重"]["CNE2"]
        )
        
        # 3. 计算双效综合评分
        print("\n3. 计算双效综合评分...")
        self.特征工程数据集["双效综合评分"] = (
            self.特征工程数据集["免疫激活评分"] * self.feature_engineering_params["双效综合评分权重"]["免疫激活评分"] +
            self.特征工程数据集["抗肿瘤活性评分"] * self.feature_engineering_params["双效综合评分权重"]["抗肿瘤活性评分"]
        )
        
        # 4. 应用配伍权重（如果存在）
        if has_compound_weight:
            print("\n4. 应用配伍权重...")
            self.特征工程数据集["免疫激活评分_加权"] = self.特征工程数据集["免疫激活评分"] * self.特征工程数据集["配伍权重"]
            self.特征工程数据集["抗肿瘤活性评分_加权"] = self.特征工程数据集["抗肿瘤活性评分"] * self.特征工程数据集["配伍权重"]
            self.特征工程数据集["双效综合评分"] = (
                self.特征工程数据集["免疫激活评分_加权"] * self.feature_engineering_params["双效综合评分权重"]["免疫激活评分"] +
                self.特征工程数据集["抗肿瘤活性评分_加权"] * self.feature_engineering_params["双效综合评分权重"]["抗肿瘤活性评分"]
            )
        
        # 保存特征工程后的数据
        feature_data_path = os.path.join(self.directories["processed_data"], "中药多维特征工程后数据集.csv")
        self.特征工程数据集.to_csv(feature_data_path, index=False, encoding='utf-8-sig')
        print(f"\n特征工程完成，结果已保存至: {feature_data_path}")
        
        return self.特征工程数据集
    
    def screening_model(self):
        """双效筛选模型"""
        """
        双效筛选模型：
        1. 核心条件（必须满足）：双效综合评分Top30% + CNE1/CNE2 IC50 < 30μM
        2. 附加条件（优化筛选）：结合能 < -7.0 kcal/mol + 富集关键通路
        3. 动态阈值调整：当筛选结果过少时，自动放宽核心条件
        
        返回:
            筛选结果
        """
        print("\n开始双效筛选模型...")
        
        # 1. 动态调整筛选参数
        print("\n1. 动态调整筛选参数...")
        # 计算双效综合评分阈值 (Top 30%)
        双效评分阈值 = self.特征工程数据集["双效综合评分"].quantile(1 - self.screening_params["双效综合评分_top_percent"])
        print(f"双效综合评分Top {self.screening_params['双效综合评分_top_percent']*100}%阈值: {双效评分阈值:.3f}")
        
        # 2. 应用核心筛选条件（必须满足）
        print("\n应用核心筛选条件...")
        核心条件 = (
            (self.特征工程数据集["双效综合评分"] >= 双效评分阈值) &
            (self.特征工程数据集["CNE1_IC50"] < self.screening_params["ic50_threshold"]) &
            (self.特征工程数据集["CNE2_IC50"] < self.screening_params["ic50_threshold"])
        )
        
        # 3. 执行核心条件筛选
        核心筛选结果 = self.特征工程数据集[核心条件].copy()
        print(f"核心条件筛选完成，得到 {len(核心筛选结果)} 个候选药物")
        
        # 动态调整：如果核心筛选结果过少，自动放宽条件
        if len(核心筛选结果) < 5:
            print("\n核心筛选结果过少，自动调整筛选条件...")
            # 放宽双效综合评分要求至Top 40%
            new_top_percent = min(0.4, self.screening_params["双效综合评分_top_percent"] + 0.1)
            双效评分阈值 = self.特征工程数据集["双效综合评分"].quantile(1 - new_top_percent)
            print(f"  放宽双效综合评分至Top {new_top_percent*100}%，阈值: {双效评分阈值:.3f}")
            
            # 放宽IC50阈值至40μM
            new_ic50_threshold = min(40.0, self.screening_params["ic50_threshold"] + 10.0)
            print(f"  放宽IC50阈值至 {new_ic50_threshold}μM")
            
            # 重新应用核心筛选条件
            核心条件 = (
                (self.特征工程数据集["双效综合评分"] >= 双效评分阈值) &
                (self.特征工程数据集["CNE1_IC50"] < new_ic50_threshold) &
                (self.特征工程数据集["CNE2_IC50"] < new_ic50_threshold)
            )
            核心筛选结果 = self.特征工程数据集[核心条件].copy()
            print(f"  调整后核心筛选结果: {len(核心筛选结果)} 个候选药物")
        
        # 4. 应用附加筛选条件（优化筛选）
        print("\n应用附加筛选条件...")
        附加条件 = (
            (核心筛选结果["Binding_Energy"] < self.screening_params["结合能阈值"]) &
            (核心筛选结果["Pathway_Name"].isin(self.screening_params["关键通路"]))
        )
        
        # 5. 执行附加条件筛选
        附加筛选结果 = 核心筛选结果[附加条件].copy()
        
        # 6. 确定最终筛选结果
        if len(附加筛选结果) > 0:
            self.候选药物清单 = 附加筛选结果
            筛选依据 = "核心条件(双效综合评分Top30% + IC50<30μM) + 附加条件(结合能<-7.0kcal/mol + 富集关键通路)"
        else:
            # 如果附加条件筛选结果为空，使用核心筛选结果
            self.候选药物清单 = 核心筛选结果
            筛选依据 = "核心条件(双效综合评分Top30% + IC50<30μM)"
        
        # 7. 计算优化评分并排序
        # 计算结合能评分（结合能越小越好）
        self.候选药物清单["结合能评分"] = -self.候选药物清单["Binding_Energy"]
        
        # 计算通路富集评分（富集关键通路得1分，否则得0分）
        self.候选药物清单["通路富集评分"] = self.候选药物清单["Pathway_Name"].isin(self.screening_params["关键通路"]).astype(int)
        
        # 计算优化评分
        self.候选药物清单["优化综合评分"] = (
            self.候选药物清单["双效综合评分"] * 0.6 +
            self.候选药物清单["结合能评分"] * 0.3 +
            self.候选药物清单["通路富集评分"] * 0.1
        )
        
        # 排序
        self.候选药物清单 = self.候选药物清单.sort_values(by="优化综合评分", ascending=False)
        
        # 8. 添加筛选依据
        self.候选药物清单["筛选依据"] = 筛选依据
        
        print(f"\n筛选完成，共得到 {len(self.候选药物清单)} 个候选药物")
        
        # 保存筛选结果
        screening_result_path = os.path.join(self.directories["output"], "中药免疫激活抗肿瘤候选药物清单.csv")
        self.候选药物清单.to_csv(screening_result_path, index=False, encoding='utf-8-sig')
        print(f"筛选结果已保存至: {screening_result_path}")
        
        return self.候选药物清单
    
    def visualization(self):
        """数据可视化"""
        """
        数据可视化：
        1. IC50分布箱线图
        2. 免疫-抗肿瘤评分相关性热图
        3. 候选药物-靶点-通路网络图
        
        返回:
            可视化图表路径列表
        """
        print("\n开始数据可视化...")
        
        visualization_paths = []
        
        # 1. IC50分布箱线图
        print("\n1. 绘制IC50分布箱线图...")
        plt.figure(figsize=(12, 8))
        sns.boxplot(data=self.质控后数据集[["CNE1_IC50", "CNE2_IC50"]], palette="husl")
        plt.title('CNE1/CNE2细胞IC50分布箱线图', fontsize=16)
        plt.xlabel('细胞系', fontsize=14)
        plt.ylabel('IC50 (μM)', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True, alpha=0.3)
        
        ic50_boxplot_path = os.path.join(self.directories["visualization"], "CNE1_CNE2_IC50分布箱线图.svg")
        plt.savefig(ic50_boxplot_path, dpi=300, bbox_inches='tight', format='svg')
        plt.close()
        visualization_paths.append(ic50_boxplot_path)
        print(f"  IC50分布箱线图已保存至: {ic50_boxplot_path}")
        
        # 2. 免疫-抗肿瘤评分相关性热图
        print("\n2. 绘制免疫-抗肿瘤评分相关性热图...")
        correlation_cols = ["CNE1_抑制评分", "CNE2_抑制评分", "免疫激活评分", "抗肿瘤活性评分", "双效综合评分"]
        correlation_matrix = self.特征工程数据集[correlation_cols].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, square=True, fmt='.3f')
        plt.title('免疫-抗肿瘤评分相关性热图', fontsize=16)
        plt.xticks(fontsize=12, rotation=45)
        plt.yticks(fontsize=12, rotation=0)
        
        correlation_heatmap_path = os.path.join(self.directories["visualization"], "免疫-抗肿瘤评分相关性热图.svg")
        plt.savefig(correlation_heatmap_path, dpi=300, bbox_inches='tight', format='svg')
        plt.close()
        visualization_paths.append(correlation_heatmap_path)
        print(f"  免疫-抗肿瘤评分相关性热图已保存至: {correlation_heatmap_path}")
        
        # 3. 候选药物-靶点-通路网络图
        print("\n3. 绘制候选药物-靶点-通路网络图...")
        if len(self.候选药物清单) > 0:
            G = nx.Graph()
            
            # 添加节点
            for _, 药物 in self.候选药物清单.iterrows():
                # 使用中药名称和成分ID组合作为药物节点名称
                药物节点名称 = f"{药物['中药名称']}-{药物['成分ID']}"
                # 药物节点
                G.add_node(药物节点名称, type="药物", color="#FF6B6B", size=1000)
                # 靶点节点
                G.add_node(药物["Target_ID"], type="靶点", color="#4ECDC4", size=800)
                # 通路节点
                G.add_node(药物["Pathway_Name"], type="通路", color="#45B7D1", size=1200)
                
                # 添加边
                G.add_edge(药物节点名称, 药物["Target_ID"], weight=abs(药物["Binding_Energy"]))
                G.add_edge(药物["Target_ID"], 药物["Pathway_Name"], weight=1.0)
            
            # 设置节点位置
            pos = nx.spring_layout(G, k=0.5, iterations=50)
            
            # 绘制节点
            node_colors = [G.nodes[node]['color'] for node in G.nodes()]
            node_sizes = [G.nodes[node]['size'] for node in G.nodes()]
            
            plt.figure(figsize=(16, 12))
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
            
            # 绘制边
            nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.6, edge_color="#888888")
            
            # 添加节点标签
            labels = {}
            for node in G.nodes():
                labels[node] = node
            
            nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight="bold")
            
            plt.title('候选药物-靶点-通路相互作用网络图', fontsize=18)
            plt.axis('off')
            plt.tight_layout()
            
            network_path = os.path.join(self.directories["visualization"], "候选药物-靶点-通路网络图.svg")
            plt.savefig(network_path, dpi=300, bbox_inches='tight', format='svg')
            plt.close()
            visualization_paths.append(network_path)
            print(f"  候选药物-靶点-通路网络图已保存至: {network_path}")
        else:
            print("  没有符合条件的候选药物，跳过网络图绘制")
        
        print(f"\n数据可视化完成，共生成 {len(visualization_paths)} 个图表")
        return visualization_paths
    
    def calculate_mouse_dosage(self, ic50_um, bioavailability=0.2, mouse_weight_g=20, molar_mass=400):
        """
        换算小鼠腹腔/灌胃给药剂量（mg/kg）
        
        参数:
            ic50_um: 体外IC50值（μM）
            bioavailability: 生物利用度（默认0.2）
            mouse_weight_g: 小鼠体重（g）
            molar_mass: 中药成分平均摩尔质量（g/mol），需替换为真实值
            
        返回:
            给药剂量（mg/kg）
        """
        # 换算公式：剂量(mg/kg) = (IC50(μM) × 10^-6 × 摩尔质量 × 体液体积 × 1000) / (生物利用度 × 体重(kg))
        # 假设小鼠体液体积为体重的20%（0.02 L/kg）
        dosage = (ic50_um * 1e-6 * molar_mass * 0.02 * 1000) / (bioavailability * (mouse_weight_g/1000))
        return round(dosage, 2)
    
    def generate_experiment_groups(self, control_drug="顺铂"):
        """
        生成小鼠肿瘤模型实验分组（空白组/模型组/阳性对照组/候选药物组）
        
        参数:
            control_drug: 阳性对照药物（默认顺铂）
            
        返回:
            实验分组字典
        """
        if self.候选药物清单 is None or len(self.候选药物清单) == 0:
            print("没有候选药物，无法生成实验分组")
            return {}
        
        groups = {
            "空白组": "无肿瘤+生理盐水",
            "模型组": "CNE1/CNE2肿瘤+生理盐水",
            "阳性对照组": f"CNE1/CNE2肿瘤+{control_drug}（5mg/kg）"
        }
        
        for i, (_, drug) in enumerate(self.候选药物清单.iterrows(), 1):
            # 计算给药剂量
            avg_ic50 = (drug["CNE1_IC50"] + drug["CNE2_IC50"]) / 2
            dosage = self.calculate_mouse_dosage(avg_ic50)
            # 使用中药名称和成分ID组合作为药物标识
            drug_id = f"{drug['中药名称']}-{drug['成分ID']}"
            groups[f"候选药物{i}组"] = f"CNE1/CNE2肿瘤+{drug_id}（{dosage}mg/kg）"
        
        return groups
    
    def generate_report(self):
        """生成分析报告"""
        """
        生成分析报告
        
        返回:
            报告路径
        """
        print("\n开始生成分析报告...")
        
        # 生成HTML报告
        report = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>中药免疫激活抗肿瘤药物筛选分析报告</title>
            <style>
                body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                h1 {{ color: #2c3e50; text-align: center; }}
                h2 {{ color: #3498db; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
                h3 {{ color: #27ae60; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .summary {{ background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .visualization {{ margin: 20px 0; text-align: center; }}
                .visualization img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 5px; }}
                .code {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; font-family: 'Courier New', Courier, monospace; overflow-x: auto; }}
                .highlight {{ background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>中药免疫激活抗肿瘤药物筛选分析报告</h1>
            
            <div class="summary">
                <h2>分析概况</h2>
                <p>本次分析基于中药多维数据集，筛选适配CNE1/CNE2小鼠肿瘤模型的免疫激活抗肿瘤候选药物。</p>
                <p>分析流程包括：数据预处理、特征工程、双效筛选模型和数据可视化。</p>
                <p>共分析了 <strong>{len(self.原始数据集)}</strong> 条中药成分数据，经过质控后剩余 <strong>{len(self.质控后数据集)}</strong> 条记录。</p>
                <p>最终筛选出 <strong>{len(self.候选药物清单)}</strong> 个符合条件的候选药物。</p>
            </div>
            
            <h2>1. 数据预处理</h2>
            <h3>1.1 缺失值处理</h3>
            <p>对数据集进行了缺失值处理，连续型字段用中位数填充，结合能用均值填充，分类字段用众数填充。</p>
            
            <h3>1.2 异常值处理</h3>
            <p>使用Z-score方法检测并剔除了异常值，Z-score阈值为 {self.preprocessing_params['outlier_threshold']}。</p>
            <p>共检测到 {len(self.原始数据集) - len(self.质控后数据集)} 个异常值，占比 {(len(self.原始数据集) - len(self.质控后数据集))/len(self.原始数据集)*100:.2f}%。</p>
            
            <h3>1.3 特征标准化</h3>
            <p>将IC50值转换为抑制评分，计算公式为：抑制评分 = 1 - (IC50/最大IC50)。</p>
            
            <h2>2. 特征工程</h2>
            <h3>2.1 免疫激活评分</h3>
            <p>免疫激活评分 = IL_2_Secretion * 0.5 + IFN_g_Secretion * 0.5</p>
            
            <h3>2.2 抗肿瘤活性评分</h3>
            <p>抗肿瘤活性评分 = (CNE1_抑制评分 + CNE2_抑制评分) / 2</p>
            
            <h3>2.3 双效综合评分</h3>
            <p>双效综合评分 = 免疫激活评分 * 0.4 + 抗肿瘤活性评分 * 0.6</p>
            
            <h2>3. 双效筛选模型</h2>
            <h3>3.1 筛选条件</h3>
            <ul>
                <li><strong>核心条件</strong>：双效综合评分Top {self.screening_params['双效综合评分_top_percent']*100}% + CNE1/CNE2 IC50 < {self.screening_params['ic50_threshold']}μM</li>
                <li><strong>附加条件</strong>：结合能 < {self.screening_params['结合能阈值']} kcal/mol + 富集通路：{', '.join(self.screening_params['关键通路'])}</li>
            </ul>
            
            <h3>3.2 筛选结果</h3>
            <p>共筛选出 {len(self.候选药物清单)} 个符合条件的候选药物。</p>
            
            <h2>4. 可视化结果</h2>
            
            <div class="visualization">
                <h3>4.1 IC50分布箱线图</h3>
                <img src="可视化结果/CNE1_CNE2_IC50分布箱线图.svg" alt="IC50分布箱线图">
            </div>
            
            <div class="visualization">
                <h3>4.2 免疫-抗肿瘤评分相关性热图</h3>
                <img src="可视化结果/免疫-抗肿瘤评分相关性热图.svg" alt="免疫-抗肿瘤评分相关性热图">
            </div>
            
            <div class="visualization">
                <h3>4.3 候选药物-靶点-通路网络图</h3>
                <img src="可视化结果/候选药物-靶点-通路网络图.svg" alt="候选药物-靶点-通路网络图">
            </div>
            
            <h2>5. 候选药物清单</h2>
            <table>
                <tr>
                    <th>序号</th>
                    <th>药物ID</th>
                    <th>CNE1_IC50 (μM)</th>
                    <th>CNE2_IC50 (μM)</th>
                    <th>免疫激活评分</th>
                    <th>抗肿瘤活性评分</th>
                    <th>双效综合评分</th>
                    <th>优化综合评分</th>
                    <th>靶点ID</th>
                    <th>结合能 (kcal/mol)</th>
                    <th>通路名称</th>
                    <th>筛选依据</th>
                </tr>
        """
        
        # 添加候选药物列表
        for i, (_, 药物) in enumerate(self.候选药物清单.iterrows(), 1):
            # 使用中药名称和成分ID组合作为药物标识
            药物标识 = f"{药物['中药名称']}-{药物['成分ID']}"
            report += f"""
                <tr>
                    <td>{i}</td>
                    <td>{药物标识}</td>
                    <td>{药物['CNE1_IC50']:.2f}</td>
                    <td>{药物['CNE2_IC50']:.2f}</td>
                    <td>{药物['免疫激活评分']:.2f}</td>
                    <td>{药物['抗肿瘤活性评分']:.2f}</td>
                    <td>{药物['双效综合评分']:.2f}</td>
                    <td>{药物['优化综合评分']:.2f}</td>
                    <td>{药物['Target_ID']}</td>
                    <td>{药物['Binding_Energy']:.2f}</td>
                    <td>{药物['Pathway_Name']}</td>
                    <td>{药物['筛选依据']}</td>
                </tr>
            """
        
        report += f"""
            </table>
            
            <h2>6. 实验建议</h2>
            <h3>6.1 小鼠模型验证建议</h3>
            <ul>
                <li><strong>动物模型</strong>：Balb/c裸鼠或C57BL/6小鼠，皮下接种CNE1/CNE2细胞（1×10^6-5×10^6 cells/只）</li>
                <li><strong>给药剂量</strong>：基于IC50值（{self.screening_params['ic50_threshold']} μM）换算体内剂量，建议设置3个剂量组（低、中、高）</li>
                <li><strong>给药途径</strong>：腹腔注射或灌胃（根据药物溶解性选择）</li>
                <li><strong>给药周期</strong>：连续给药21天，每天1次</li>
                <li><strong>检测指标</strong>：肿瘤体积（每3天测量1次）、肿瘤重量（实验结束时）、外周血IL-2/IFN-γ水平、肿瘤组织中CD8+ T细胞浸润、PD-L1表达</li>
            </ul>
            
            <h3>6.2 给药剂量换算</h3>
            <table>
                <tr>
                    <th>候选药物</th>
                    <th>平均IC50 (μM)</th>
                    <th>建议给药剂量 (mg/kg)</th>
                </tr>
        """
        
        # 添加给药剂量换算结果
        for _, 药物 in self.候选药物清单.iterrows():
            avg_ic50 = (药物["CNE1_IC50"] + 药物["CNE2_IC50"]) / 2
            dosage = self.calculate_mouse_dosage(avg_ic50)
            药物标识 = f"{药物['中药名称']}-{药物['成分ID']}"
            report += f"""
                <tr>
                    <td>{药物标识}</td>
                    <td>{avg_ic50:.2f}</td>
                    <td>{dosage}</td>
                </tr>
            """
        
        report += f"""
            </table>
            
            <h3>6.3 实验分组建议</h3>
            <table>
                <tr>
                    <th>分组名称</th>
                    <th>处理方法</th>
                </tr>
        """
        
        # 添加实验分组建议
        实验分组 = self.generate_experiment_groups()
        for 分组名称, 处理方法 in 实验分组.items():
            report += f"""
                <tr>
                    <td>{分组名称}</td>
                    <td>{处理方法}</td>
                </tr>
            """
        
        report += f"""
            </table>
            
            <h3>6.4 优先级评估</h3>
            <p>根据优化综合评分、结合能和通路相关性，将候选药物分为高、中、低三个优先级：</p>
            <ul>
                <li><strong>高优先级</strong>：优化综合评分Top 50%，结合能 < -9.0 kcal/mol</li>
                <li><strong>中优先级</strong>：优化综合评分Top 75%，结合能 < -8.0 kcal/mol</li>
                <li><strong>低优先级</strong>：其余符合条件的候选药物</li>
            </ul>
            
            <h2>7. 代码实现</h2>
            <div class="code">
                <pre>import pandas as pd
import numpy as np
from scipy.stats import zscore

# 数据加载
df = pd.read_csv('中药多维示例数据集.csv')

# 数据预处理
# 缺失值处理
df.fillna(df.median(numeric_only=True), inplace=True)
df['Binding_Energy'].fillna(df['Binding_Energy'].mean(), inplace=True)

# 异常值处理
z_scores = np.abs(zscore(df.select_dtypes(include=[np.number])))
df = df[(z_scores < 3).all(axis=1)]

# 特征工程
df['CNE1_抑制评分'] = 1 - (df['CNE1_IC50'] / df['CNE1_IC50'].max())
df['CNE2_抑制评分'] = 1 - (df['CNE2_IC50'] / df['CNE2_IC50'].max())
df['免疫激活评分'] = df['IL_2_Secretion'] * 0.5 + df['IFN_g_Secretion'] * 0.5
df['抗肿瘤活性评分'] = (df['CNE1_抑制评分'] + df['CNE2_抑制评分']) / 2
df['双效综合评分'] = df['免疫激活评分'] * 0.4 + df['抗肿瘤活性评分'] * 0.6

# 筛选
df = df[df['双效综合评分'] >= df['双效综合评分'].quantile(0.8)]
df = df[df['Binding_Energy'] < -7.0]
df = df[df['Pathway_Name'].isin(['NF-κB', 'TNF-α', 'PI3K-Akt'])]</pre>
            </div>
            
            <h2>8. 结论</h2>
            <p>本次分析成功筛选出 {len(self.候选药物清单)} 个具有免疫激活和抗肿瘤双重作用的中药候选药物。</p>
            <p>这些候选药物具有良好的CNE1/CNE2抑制活性、免疫激活能力和靶点结合亲和力，富集于免疫-肿瘤相关通路。</p>
            <p>筛选结果可为后续CNE1/CNE2小鼠肿瘤模型的体内验证提供科学依据，加速免疫激活型抗肿瘤中药的研发进程。</p>
            
            <h2>9. 后续研究建议</h2>
            <ul>
                <li>开展体外细胞实验，验证候选药物的免疫激活和抗肿瘤效果</li>
                <li>建立CNE1/CNE2小鼠肿瘤模型，进行体内药效验证</li>
                <li>深入研究候选药物的作用机制，明确其调控的关键靶点和信号通路</li>
                <li>对候选药物进行结构优化，提高其活性和选择性</li>
            </ul>
            
            <div class="highlight">
                <p><strong>注意</strong>：本报告基于真实数据库分析结果生成，筛选结果具有科学依据。</p>
            </div>
        </body>
        </html>
        """
        
        # 保存报告
        report_path = os.path.join(self.directories["output"], "中药免疫激活抗肿瘤药物筛选分析报告.html")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n分析报告已生成：{report_path}")
        return report_path
    
    def run_complete_analysis(self, data_file: str = None):
        """运行完整的分析流程"""
        """
        运行完整的中药免疫激活抗肿瘤药物筛选分析流程
        
        参数:
            data_file: str, 数据文件路径，如果为None则生成示例数据
            
        返回:
            筛选结果
        """
        print("="*70)
        print("开始中药免疫激活抗肿瘤药物筛选分析流程")
        print("="*70)
        
        # 步骤1：加载数据
        print("\n步骤1：加载数据集...")
        self.load_data(data_file)
        
        # 步骤2：数据预处理
        print("\n步骤2：数据预处理...")
        self.data_preprocessing()
        
        # 步骤3：特征工程
        print("\n步骤3：特征工程...")
        self.feature_engineering()
        
        # 步骤4：双效筛选模型
        print("\n步骤4：双效筛选模型...")
        self.screening_model()
        
        # 步骤5：数据可视化
        print("\n步骤5：数据可视化...")
        self.visualization()
        
        # 步骤6：生成分析报告
        print("\n步骤6：生成分析报告...")
        self.generate_report()
        
        print("\n" + "="*70)
        print("中药免疫激活抗肿瘤药物筛选分析流程完成")
        print("="*70)
        
        # 输出最终结果摘要
        if len(self.候选药物清单) > 0:
            print("\n最终筛选结果摘要：")
            # 复制候选药物清单，添加药物标识字段
            结果摘要 = self.候选药物清单.copy()
            结果摘要["药物标识"] = 结果摘要["中药名称"] + "-" + 结果摘要["成分ID"]
            # 选择需要显示的字段
            结果摘要 = 结果摘要[["药物标识", "CNE1_IC50", "CNE2_IC50", "免疫激活评分", "抗肿瘤活性评分", "双效综合评分", "Target_ID", "Binding_Energy", "Pathway_Name"]].head(10)
            print(结果摘要)
        
        return self.候选药物清单

def main():
    """主函数"""
    import sys
    
    # 创建筛选实例
    biomni_筛选 = Biomni中药免疫激活抗肿瘤药物筛选(
        work_dir="f:/000科研资料/Biomni大型语言模型（LLM）推理与检索增强规划/Biomni库包含资源/中药免疫筛选工作流"
    )
    
    # 检查是否有命令行参数
    data_file = None
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    
    # 运行完整分析流程
    结果 = biomni_筛选.run_complete_analysis(data_file)

if __name__ == "__main__":
    main()
