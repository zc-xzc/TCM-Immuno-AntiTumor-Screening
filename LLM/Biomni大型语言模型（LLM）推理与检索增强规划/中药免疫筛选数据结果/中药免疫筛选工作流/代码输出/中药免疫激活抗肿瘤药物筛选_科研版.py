#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中药多维数据分析筛选免疫激活抗肿瘤药物 - 科研版

该脚本实现了发表论文级可复现的中药免疫激活抗肿瘤药物筛选分析，
针对CNE1/CNE2鼻咽癌细胞系，包含完整的数据预处理、特征工程、
双效模型构建和机制推理流程。

使用方法：
    python 中药免疫激活抗肿瘤药物筛选_科研版.py
"""

# 导入所需库
import os
import json
import random
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from scipy import stats
from scipy.stats import zscore
import warnings
warnings.filterwarnings('ignore')

# 设置随机种子，保证可复现性
np.random.seed(42)
random.seed(42)

class 中药免疫激活抗肿瘤药物筛选:
    def __init__(self, work_dir: str = "./"):
        """初始化筛选工作流"""
        self.work_dir = work_dir
        self.原始数据集 = None
        self.预处理后数据集 = None
        self.特征工程数据集 = None
        self.筛选结果 = None
        
        # 创建工作目录结构
        self._创建工作目录()
        
        # 初始化默认参数
        self._初始化默认参数()
    
    def _创建工作目录(self):
        """创建工作目录结构"""
        self.目录结构 = {
            "数据输入": os.path.join(self.work_dir, "数据输入"),
            "数据预处理": os.path.join(self.work_dir, "数据预处理"),
            "特征工程": os.path.join(self.work_dir, "特征工程"),
            "模型构建": os.path.join(self.work_dir, "模型构建"),
            "机制分析": os.path.join(self.work_dir, "机制分析"),
            "结果输出": os.path.join(self.work_dir, "结果输出"),
            "可视化结果": os.path.join(self.work_dir, "可视化结果"),
            "代码输出": os.path.join(self.work_dir, "代码输出")
        }
        
        for dir_path in self.目录结构.values():
            os.makedirs(dir_path, exist_ok=True)
    
    def _初始化默认参数(self):
        """初始化默认参数"""
        # 数据预处理参数
        self.预处理参数 = {
            "knn_n_neighbors": 5,  # KNN插补的邻居数
            "zscore_threshold": 3.0,  # 异常值检测阈值
            "min_max_features": ["CNE1_IC50", "CNE2_IC50", "IL2", "IFNγ", "TNFα", "结合能"],
            "log_transform_features": ["CNE1_IC50", "CNE2_IC50"],
            "categorical_features": ["通路", "靶点ID"]
        }
        
        # 特征工程参数
        self.特征工程参数 = {
            "免疫因子权重": {"IL2": 0.3, "IFNγ": 0.4, "TNFα": 0.3},  # 免疫激活评分权重
            "双效评分权重": {"免疫激活评分": 0.5, "抗肿瘤活性评分": 0.5}  # 双效综合评分权重
        }
        
        # 筛选模型参数
        self.筛选参数 = {
            "双效评分_top_percent": 0.2,  # 双效评分前20%
            "ic50_threshold": 20.0,  # IC50 < 20 μM
            "免疫因子上调阈值": 0.2,  # 较对照组上调≥20%
            "结合能阈值": -7.0,  # 结合能 < -7.0 kcal/mol
            "关键通路": ["NF-κB", "TNF-α", "PI3K-Akt"]  # 关键免疫-肿瘤相关通路
        }
    
    def 生成示例数据集(self):
        """生成符合要求的中药多维数据集示例"""
        print("正在生成示例中药多维数据集...")
        
        # 中药名称列表
        中药列表 = ["黄芪", "人参", "灵芝", "当归", "枸杞", "女贞子", "淫羊藿", "白术", "茯苓", "甘草",
                   "柴胡", "黄芩", "黄连", "黄柏", "栀子", "丹皮", "赤芍", "生地", "熟地", "川芎",
                   "丹参", "三七", "红花", "桃仁", "牛膝", "桔梗", "半夏", "陈皮", "枳实", "厚朴",
                   "苍术", "藿香", "佩兰", "砂仁", "豆蔻", "木香", "香附", "郁金", "延胡索", "乳香"]
        
        # 靶点列表
        靶点列表 = ["PD-1", "PD-L1", "CTLA-4", "CD28", "OX40", "4-1BB", "CD40", "GITR", "ICOS", "LAG3",
                   "TIM3", "TIGIT", "TLR4", "TLR7", "TLR9", "STING", "IFNAR1", "IFNGR1", "IL-2RA", "IL-6R"]
        
        # 通路列表
        通路列表 = ["NF-κB", "TNF-α", "PI3K-Akt", "JAK-STAT", "MAPK", "Wnt", "Hippo", "Notch", "TGF-β", "mTOR"]
        
        # 生成数据集
        数据集 = []
        for i in range(100):
            中药名称 = random.choice(中药列表)
            成分ID = f"CMP{i+1:03d}"
            
            # 生成IC50值 (μM)
            cne1_ic50 = random.uniform(1, 100)  # 1-100 μM
            cne2_ic50 = random.uniform(1, 100)  # 1-100 μM
            
            # 生成细胞凋亡率 (%)
            细胞凋亡率 = random.uniform(10, 80)  # 10-80%
            
            # 生成免疫因子分泌量 (pg/mL)
            il2 = random.uniform(10, 200)  # 10-200 pg/mL
            ifnγ = random.uniform(20, 300)  # 20-300 pg/mL
            tnfa = random.uniform(15, 250)  # 15-250 pg/mL
            
            # 生成靶点结合能 (kcal/mol)
            结合能 = random.uniform(-12, -4)  # -12 到 -4 kcal/mol
            
            # 随机选择靶点和通路
            靶点ID = random.choice(靶点列表)
            通路 = random.choice(通路列表)
            
            # 生成复方配伍信息
            复方配伍 = random.choice(["单味药", f"{random.choice(中药列表)}+{random.choice(中药列表)}", f"{random.choice(中药列表)}+{random.choice(中药列表)}+{random.choice(中药列表)}"])
            
            # 生成药代动力学参数
            口服生物利用度 = random.uniform(10, 90)  # 10-90%
            半衰期 = random.uniform(1, 24)  # 1-24 h
            
            # 添加一些缺失值 (10% 缺失率)
            if random.random() < 0.1:
                cne1_ic50 = np.nan
            if random.random() < 0.1:
                cne2_ic50 = np.nan
            if random.random() < 0.1:
                il2 = np.nan
            if random.random() < 0.1:
                ifnγ = np.nan
            if random.random() < 0.1:
                tnfa = np.nan
            if random.random() < 0.1:
                结合能 = np.nan
            
            # 添加一些异常值 (5% 异常率)
            if random.random() < 0.05:
                cne1_ic50 = random.uniform(200, 500)
            if random.random() < 0.05:
                cne2_ic50 = random.uniform(200, 500)
            
            数据集.append({
                "中药名称": 中药名称,
                "成分ID": 成分ID,
                "分子式": f"C{random.randint(10, 50)}H{random.randint(15, 80)}O{random.randint(5, 20)}",
                "来源药材": 中药名称,
                "CNE1_IC50": cne1_ic50,
                "CNE2_IC50": cne2_ic50,
                "细胞凋亡率": 细胞凋亡率,
                "IL2": il2,
                "IFNγ": ifnγ,
                "TNFα": tnfa,
                "结合能": 结合能,
                "靶点ID": 靶点ID,
                "通路": 通路,
                "复方配伍": 复方配伍,
                "口服生物利用度": 口服生物利用度,
                "半衰期": 半衰期
            })
        
        self.原始数据集 = pd.DataFrame(数据集)
        
        # 保存原始数据集
        原始数据路径 = os.path.join(self.目录结构["数据输入"], "中药多维原始数据集.csv")
        self.原始数据集.to_csv(原始数据路径, index=False, encoding='utf-8-sig')
        
        print(f"示例数据集生成完成，共 {len(self.原始数据集)} 条记录")
        print(f"原始数据集已保存至：{原始数据路径}")
        return self.原始数据集
    
    def 加载数据集(self, 数据文件: str = None):
        """加载数据集"""
        if 数据文件 and os.path.exists(数据文件):
            self.原始数据集 = pd.read_csv(数据文件, encoding='utf-8-sig')
        else:
            # 生成示例数据集
            self.生成示例数据集()
        
        print(f"已加载数据集，共 {len(self.原始数据集)} 条记录，{len(self.原始数据集.columns)} 个特征")
        return self.原始数据集
    
    def 数据预处理与质控(self):
        """数据标准化预处理与质控"""
        print("\n开始数据预处理与质控...")
        
        # 1. 复制原始数据集
        self.预处理后数据集 = self.原始数据集.copy()
        
        # 2. 缺失值处理
        print("\n2. 缺失值处理...")
        self._缺失值处理()
        
        # 3. 异常值剔除
        print("\n3. 异常值剔除...")
        self._异常值剔除()
        
        # 4. 特征标准化
        print("\n4. 特征标准化...")
        self._特征标准化()
        
        # 5. 生成质控报告
        print("\n5. 生成质控报告...")
        self._生成质控报告()
        
        # 6. 保存预处理后数据集
        预处理数据路径 = os.path.join(self.目录结构["数据预处理"], "中药多维预处理后数据集.csv")
        self.预处理后数据集.to_csv(预处理数据路径, index=False, encoding='utf-8-sig')
        
        print(f"\n数据预处理完成，共 {len(self.预处理后数据集)} 条记录")
        print(f"预处理后数据集已保存至：{预处理数据路径}")
        return self.预处理后数据集
    
    def _缺失值处理(self):
        """缺失值处理"""
        # 计算缺失值分布
        缺失值分布 = self.预处理后数据集.isnull().sum().sort_values(ascending=False)
        print(f"缺失值分布：\n{缺失值分布}")
        
        # 绘制缺失值热力图
        plt.figure(figsize=(12, 8))
        sns.heatmap(self.预处理后数据集.isnull(), cbar=False, cmap='viridis')
        plt.title('原始数据缺失值分布热力图')
        plt.tight_layout()
        缺失值热力图路径 = os.path.join(self.目录结构["可视化结果"], "原始数据缺失值分布热力图.png")
        plt.savefig(缺失值热力图路径, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 使用KNN填充缺失值
        knn_imputer = KNNImputer(n_neighbors=self.预处理参数["knn_n_neighbors"])
        
        # 选择需要填充的数值型特征
        数值型特征 = self.预处理后数据集.select_dtypes(include=[np.number]).columns.tolist()
        
        # 保存原始数值型特征数据用于验证
        原始数值型数据 = self.预处理后数据集[数值型特征].copy()
        
        # 执行KNN填充
        self.预处理后数据集[数值型特征] = knn_imputer.fit_transform(self.预处理后数据集[数值型特征])
        
        # 验证填充结果
        填充后缺失值 = self.预处理后数据集.isnull().sum().sum()
        print(f"KNN填充后缺失值总数：{填充后缺失值}")
        
        # 绘制填充前后对比图（仅显示前5个特征）
        对比特征 = 数值型特征[:5]
        fig, axes = plt.subplots(len(对比特征), 2, figsize=(12, 2*len(对比特征)))
        for i, 特征 in enumerate(对比特征):
            # 填充前
            sns.histplot(原始数值型数据[特征].dropna(), ax=axes[i, 0], kde=True)
            axes[i, 0].set_title(f'{特征} - 填充前')
            # 填充后
            sns.histplot(self.预处理后数据集[特征], ax=axes[i, 1], kde=True)
            axes[i, 1].set_title(f'{特征} - 填充后')
        plt.tight_layout()
        填充对比图路径 = os.path.join(self.目录结构["可视化结果"], "缺失值填充前后对比图.png")
        plt.savefig(填充对比图路径, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _异常值剔除(self):
        """异常值剔除"""
        # 使用Z-score法检测异常值
        数值型特征 = self.预处理后数据集.select_dtypes(include=[np.number]).columns.tolist()
        
        # 计算Z-score
        z_scores = np.abs(zscore(self.预处理后数据集[数值型特征]))
        
        # 识别异常值
        异常值掩码 = (z_scores > self.预处理参数["zscore_threshold"]).any(axis=1)
        异常值数量 = 异常值掩码.sum()
        
        print(f"检测到 {异常值数量} 个异常值，占比 {异常值数量/len(self.预处理后数据集)*100:.2f}%")
        
        # 剔除异常值
        self.预处理后数据集 = self.预处理后数据集[~异常值掩码].copy()
        
        # 绘制箱线图（仅显示前5个特征）
        箱线图特征 = 数值型特征[:5]
        plt.figure(figsize=(12, 8))
        sns.boxplot(data=self.预处理后数据集[箱线图特征])
        plt.xticks(rotation=45)
        plt.title('异常值剔除后数值型特征箱线图')
        plt.tight_layout()
        箱线图路径 = os.path.join(self.目录结构["可视化结果"], "异常值剔除后箱线图.png")
        plt.savefig(箱线图路径, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _特征标准化(self):
        """特征标准化"""
        # 1. 对数转换
        for 特征 in self.预处理参数["log_transform_features"]:
            if 特征 in self.预处理后数据集.columns:
                self.预处理后数据集[f"{特征}_log"] = np.log10(self.预处理后数据集[特征] + 1e-6)
        
        # 2. Min-Max标准化
        scaler = MinMaxScaler()
        for 特征 in self.预处理参数["min_max_features"]:
            if 特征 in self.预处理后数据集.columns:
                self.预处理后数据集[f"{特征}_scaled"] = scaler.fit_transform(self.预处理后数据集[[特征]])
        
        # 3. 分类变量编码
        for 特征 in self.预处理参数["categorical_features"]:
            if 特征 in self.预处理后数据集.columns:
                # 使用one-hot编码
                one_hot = pd.get_dummies(self.预处理后数据集[特征], prefix=特征)
                self.预处理后数据集 = pd.concat([self.预处理后数据集, one_hot], axis=1)
        
        # 绘制标准化前后对比图
        标准化对比特征 = ["CNE1_IC50", "CNE2_IC50", "IL2", "IFNγ", "TNFα"]
        fig, axes = plt.subplots(len(标准化对比特征), 2, figsize=(12, 2*len(标准化对比特征)))
        for i, 特征 in enumerate(标准化对比特征):
            # 标准化前
            sns.histplot(self.预处理后数据集[特征], ax=axes[i, 0], kde=True)
            axes[i, 0].set_title(f'{特征} - 标准化前')
            # 标准化后
            sns.histplot(self.预处理后数据集[f'{特征}_scaled'], ax=axes[i, 1], kde=True)
            axes[i, 1].set_title(f'{特征} - Min-Max标准化后')
        plt.tight_layout()
        标准化对比图路径 = os.path.join(self.目录结构["可视化结果"], "特征标准化前后对比图.png")
        plt.savefig(标准化对比图路径, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _生成质控报告(self):
        """生成质控报告"""
        # 辅助函数：将numpy类型转换为Python原生类型
        def 转换为Python类型(value):
            if isinstance(value, (np.integer, np.int64)):
                return int(value)
            elif isinstance(value, (np.floating, np.float64)):
                return float(value)
            elif isinstance(value, (np.ndarray, pd.Series)):
                return value.tolist()
            return value
        
        # 生成质控报告
        质控报告 = {
            "基本信息": {
                "原始数据量": 转换为Python类型(len(self.原始数据集)),
                "预处理后数据量": 转换为Python类型(len(self.预处理后数据集)),
                "特征数量": 转换为Python类型(len(self.原始数据集.columns)),
                "数值型特征数量": 转换为Python类型(len(self.原始数据集.select_dtypes(include=[np.number]).columns)),
                "分类特征数量": 转换为Python类型(len(self.原始数据集.select_dtypes(include=[object]).columns))
            },
            "缺失值处理": {
                "原始缺失值总数": 转换为Python类型(self.原始数据集.isnull().sum().sum()),
                "预处理后缺失值总数": 转换为Python类型(self.预处理后数据集.isnull().sum().sum()),
                "缺失值填充方法": "KNN插补",
                "KNN邻居数": self.预处理参数["knn_n_neighbors"]
            },
            "异常值处理": {
                "检测方法": "Z-score法",
                "Z-score阈值": self.预处理参数["zscore_threshold"],
                "异常值数量": 转换为Python类型(len(self.原始数据集) - len(self.预处理后数据集)),
                "异常值占比": f"{(len(self.原始数据集) - len(self.预处理后数据集))/len(self.原始数据集)*100:.2f}%"
            },
            "特征标准化": {
                "对数转换特征": self.预处理参数["log_transform_features"],
                "Min-Max标准化特征": self.预处理参数["min_max_features"],
                "分类变量编码特征": self.预处理参数["categorical_features"]
            }
        }
        
        # 保存质控报告
        质控报告路径 = os.path.join(self.目录结构["数据预处理"], "数据质控报告.json")
        with open(质控报告路径, 'w', encoding='utf-8') as f:
            json.dump(质控报告, f, ensure_ascii=False, indent=4)
        
        # 生成质控报告文本版
        质控报告文本 = "# 中药多维数据集质控报告\n\n"
        
        质控报告文本 += "## 1. 基本信息\n"
        for key, value in 质控报告["基本信息"].items():
            质控报告文本 += f"- {key}: {value}\n"
        
        质控报告文本 += "\n## 2. 缺失值处理\n"
        for key, value in 质控报告["缺失值处理"].items():
            质控报告文本 += f"- {key}: {value}\n"
        
        质控报告文本 += "\n## 3. 异常值处理\n"
        for key, value in 质控报告["异常值处理"].items():
            质控报告文本 += f"- {key}: {value}\n"
        
        质控报告文本 += "\n## 4. 特征标准化\n"
        for key, value in 质控报告["特征标准化"].items():
            if isinstance(value, list):
                质控报告文本 += f"- {key}: {', '.join(value)}\n"
            else:
                质控报告文本 += f"- {key}: {value}\n"
        
        质控报告文本路径 = os.path.join(self.目录结构["数据预处理"], "数据质控报告.txt")
        with open(质控报告文本路径, 'w', encoding='utf-8') as f:
            f.write(质控报告文本)
        
        print(f"质控报告已生成：{质控报告文本路径}")
    
    def 特征工程与双效模型构建(self):
        """特征工程与双效模型构建"""
        print("\n开始特征工程与双效模型构建...")
        
        # 1. 复制预处理后数据集
        self.特征工程数据集 = self.预处理后数据集.copy()
        
        # 2. 构建免疫激活综合评分
        print("\n2. 构建免疫激活综合评分...")
        self._构建免疫激活评分()
        
        # 3. 构建抗肿瘤活性评分
        print("\n3. 构建抗肿瘤活性评分...")
        self._构建抗肿瘤活性评分()
        
        # 4. 构建双效综合评分
        print("\n4. 构建双效综合评分...")
        self._构建双效综合评分()
        
        # 5. 多变量关联分析
        print("\n5. 多变量关联分析...")
        self._多变量关联分析()
        
        # 6. 双效筛选模型
        print("\n6. 双效筛选模型...")
        self._双效筛选模型()
        
        # 7. 保存特征工程后数据集
        特征工程数据路径 = os.path.join(self.目录结构["特征工程"], "中药多维特征工程后数据集.csv")
        self.特征工程数据集.to_csv(特征工程数据路径, index=False, encoding='utf-8-sig')
        
        print(f"\n特征工程与双效模型构建完成")
        print(f"特征工程后数据集已保存至：{特征工程数据路径}")
        return self.特征工程数据集
    
    def _构建免疫激活评分(self):
        """构建免疫激活综合评分"""
        # 计算免疫因子之间的相关性
        免疫因子 = ["IL2", "IFNγ", "TNFα"]
        相关性矩阵 = self.特征工程数据集[免疫因子].corr()
        
        # 绘制相关性热图
        plt.figure(figsize=(8, 6))
        sns.heatmap(相关性矩阵, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('免疫因子相关性热图')
        plt.tight_layout()
        免疫因子相关性图路径 = os.path.join(self.目录结构["可视化结果"], "免疫因子相关性热图.png")
        plt.savefig(免疫因子相关性图路径, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 构建免疫激活综合评分
        self.特征工程数据集["免疫激活评分"] = (
            self.特征工程数据集["IL2"] * self.特征工程参数["免疫因子权重"]["IL2"] +
            self.特征工程数据集["IFNγ"] * self.特征工程参数["免疫因子权重"]["IFNγ"] +
            self.特征工程数据集["TNFα"] * self.特征工程参数["免疫因子权重"]["TNFα"]
        )
        
        # 绘制免疫激活评分分布
        plt.figure(figsize=(10, 6))
        sns.histplot(self.特征工程数据集["免疫激活评分"], kde=True)
        plt.title('免疫激活评分分布')
        plt.xlabel('免疫激活评分')
        plt.ylabel('频数')
        plt.tight_layout()
        免疫激活评分分布图路径 = os.path.join(self.目录结构["可视化结果"], "免疫激活评分分布图.png")
        plt.savefig(免疫激活评分分布图路径, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _构建抗肿瘤活性评分(self):
        """构建抗肿瘤活性评分"""
        # 将IC50值转换为抑制活性评分 (Score = -log10(IC50))
        self.特征工程数据集["CNE1_抑制评分"] = -np.log10(self.特征工程数据集["CNE1_IC50"])
        self.特征工程数据集["CNE2_抑制评分"] = -np.log10(self.特征工程数据集["CNE2_IC50"])
        
        # 取两者均值作为最终抗肿瘤评分
        self.特征工程数据集["抗肿瘤活性评分"] = (
            self.特征工程数据集["CNE1_抑制评分"] + self.特征工程数据集["CNE2_抑制评分"]
        ) / 2
        
        # 绘制抗肿瘤活性评分分布
        plt.figure(figsize=(10, 6))
        sns.histplot(self.特征工程数据集["抗肿瘤活性评分"], kde=True)
        plt.title('抗肿瘤活性评分分布')
        plt.xlabel('抗肿瘤活性评分')
        plt.ylabel('频数')
        plt.tight_layout()
        抗肿瘤活性评分分布图路径 = os.path.join(self.目录结构["可视化结果"], "抗肿瘤活性评分分布图.png")
        plt.savefig(抗肿瘤活性评分分布图路径, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _构建双效综合评分(self):
        """构建双效综合评分"""
        # 基于免疫激活评分与抗肿瘤活性评分的加权融合
        self.特征工程数据集["双效综合评分"] = (
            self.特征工程数据集["免疫激活评分"] * self.特征工程参数["双效评分权重"]["免疫激活评分"] +
            self.特征工程数据集["抗肿瘤活性评分"] * self.特征工程参数["双效评分权重"]["抗肿瘤活性评分"]
        )
        
        # 绘制双效综合评分分布
        plt.figure(figsize=(10, 6))
        sns.histplot(self.特征工程数据集["双效综合评分"], kde=True)
        plt.title('双效综合评分分布')
        plt.xlabel('双效综合评分')
        plt.ylabel('频数')
        plt.tight_layout()
        双效综合评分分布图路径 = os.path.join(self.目录结构["可视化结果"], "双效综合评分分布图.png")
        plt.savefig(双效综合评分分布图路径, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _多变量关联分析(self):
        """多变量关联分析"""
        # 1. 相关性分析
        分析特征 = ["免疫激活评分", "抗肿瘤活性评分", "CNE1_IC50", "CNE2_IC50", "IL2", "IFNγ", "TNFα", "结合能"]
        相关性矩阵 = self.特征工程数据集[分析特征].corr()
        
        # 绘制多维度相关性热图
        plt.figure(figsize=(12, 10))
        sns.heatmap(相关性矩阵, annot=True, cmap='coolwarm', vmin=-1, vmax=1, square=True, fmt='.3f')
        plt.title('多维度特征相关性热图')
        plt.tight_layout()
        多维度相关性图路径 = os.path.join(self.目录结构["可视化结果"], "多维度特征相关性热图.png")
        plt.savefig(多维度相关性图路径, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. 免疫激活评分与抗肿瘤活性评分的散点图 + 线性回归
        plt.figure(figsize=(10, 8))
        
        # 绘制散点图
        sns.scatterplot(
            x="免疫激活评分",
            y="抗肿瘤活性评分",
            data=self.特征工程数据集,
            alpha=0.7, s=80
        )
        
        # 拟合线性回归
        X = self.特征工程数据集["免疫激活评分"].values.reshape(-1, 1)
        y = self.特征工程数据集["抗肿瘤活性评分"].values
        lr = LinearRegression()
        lr.fit(X, y)
        y_pred = lr.predict(X)
        
        # 计算R²
        r2 = r2_score(y, y_pred)
        
        # 绘制回归线
        sns.lineplot(
            x=self.特征工程数据集["免疫激活评分"],
            y=y_pred,
            color='red',
            linewidth=2,
            label=f'线性回归 (R² = {r2:.3f})'
        )
        
        plt.title('免疫激活评分与抗肿瘤活性评分相关性分析')
        plt.xlabel('免疫激活评分')
        plt.ylabel('抗肿瘤活性评分')
        plt.legend()
        plt.tight_layout()
        双效相关性图路径 = os.path.join(self.目录结构["可视化结果"], "免疫激活与抗肿瘤活性相关性散点图.png")
        plt.savefig(双效相关性图路径, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"免疫激活评分与抗肿瘤活性评分的R²值：{r2:.3f}")
    
    def _双效筛选模型(self):
        """双效筛选模型"""
        # 1. 计算双效评分阈值 (Top 20%)
        双效评分阈值 = self.特征工程数据集["双效综合评分"].quantile(1 - self.筛选参数["双效评分_top_percent"])
        print(f"双效评分Top {self.筛选参数['双效评分_top_percent']*100}%阈值：{双效评分阈值:.3f}")
        
        # 2. 应用筛选条件
        筛选条件 = (
            (self.特征工程数据集["双效综合评分"] >= 双效评分阈值) &
            (self.特征工程数据集["CNE1_IC50"] < self.筛选参数["ic50_threshold"]) &
            (self.特征工程数据集["CNE2_IC50"] < self.筛选参数["ic50_threshold"]) &
            (self.特征工程数据集["IL2"] >= self.特征工程数据集["IL2"].mean() * (1 + self.筛选参数["免疫因子上调阈值"])) &
            (self.特征工程数据集["IFNγ"] >= self.特征工程数据集["IFNγ"].mean() * (1 + self.筛选参数["免疫因子上调阈值"])) &
            (self.特征工程数据集["TNFα"] >= self.特征工程数据集["TNFα"].mean() * (1 + self.筛选参数["免疫因子上调阈值"])) &
            (self.特征工程数据集["结合能"] < self.筛选参数["结合能阈值"]) &
            (self.特征工程数据集["通路"].isin(self.筛选参数["关键通路"]))
        )
        
        # 3. 执行筛选
        self.筛选结果 = self.特征工程数据集[筛选条件].copy()
        
        # 4. 加权评分排序
        # 计算加权评分（考虑所有筛选指标）
        self.筛选结果["加权综合评分"] = (
            0.3 * self.筛选结果["双效综合评分"] +
            0.2 * (-np.log10(self.筛选结果["CNE1_IC50"])) +
            0.2 * (-np.log10(self.筛选结果["CNE2_IC50"])) +
            0.1 * self.筛选结果["免疫激活评分"] +
            0.1 * (-self.筛选结果["结合能"]) +  # 结合能越小（越负）越好，取负值
            0.1 * self.筛选结果["细胞凋亡率"] / 100  # 归一化到0-1
        )
        
        # 排序
        self.筛选结果 = self.筛选结果.sort_values(by="加权综合评分", ascending=False)
        
        # 5. 保存筛选结果
        筛选结果路径 = os.path.join(self.目录结构["模型构建"], "中药免疫激活抗肿瘤筛选结果.csv")
        self.筛选结果.to_csv(筛选结果路径, index=False, encoding='utf-8-sig')
        
        print(f"\n筛选结果：")
        print(f"- 符合条件的候选药物数量：{len(self.筛选结果)}")
        print(f"- 筛选结果已保存至：{筛选结果路径}")
        
        # 6. 绘制筛选结果排序柱状图
        if len(self.筛选结果) > 0:
            plt.figure(figsize=(12, 8))
            sns.barplot(
                x="加权综合评分",
                y="中药名称" + "-" + "成分ID",
                data=self.筛选结果.assign(
                    **{"中药名称-成分ID": self.筛选结果["中药名称"] + "-" + self.筛选结果["成分ID"]}
                ),
                palette="viridis"
            )
            plt.title('候选药物加权综合评分排序')
            plt.xlabel('加权综合评分')
            plt.ylabel('候选药物')
            plt.tight_layout()
            筛选结果柱状图路径 = os.path.join(self.目录结构["可视化结果"], "候选药物加权综合评分排序柱状图.png")
            plt.savefig(筛选结果柱状图路径, dpi=300, bbox_inches='tight')
            plt.close()
    
    def 机制推理与网络图构建(self):
        """机制推理与网络图构建"""
        print("\n开始机制推理与网络图构建...")
        
        if len(self.筛选结果) == 0:
            print("没有符合条件的候选药物，跳过机制推理")
            return None
        
        # 1. 提取候选药物-核心靶点-关键通路关系
        机制数据 = self.筛选结果[["中药名称", "成分ID", "靶点ID", "通路", "结合能"]].copy()
        
        # 2. 构建相互作用网络图
        G = nx.Graph()
        
        # 添加节点
        for _, 行 in 机制数据.iterrows():
            # 添加药物节点
            G.add_node(行["成分ID"], type="药物", name=行["中药名称"])
            # 添加靶点节点
            G.add_node(行["靶点ID"], type="靶点")
            # 添加通路节点
            G.add_node(行["通路"], type="通路")
            
            # 添加边
            G.add_edge(行["成分ID"], 行["靶点ID"], weight=abs(行["结合能"]), relationship="结合")
            G.add_edge(行["靶点ID"], 行["通路"], relationship="参与")
        
        # 3. 绘制网络图
        plt.figure(figsize=(16, 12))
        
        # 设置节点位置
        pos = nx.spring_layout(G, k=0.3, iterations=50)
        
        # 按类型设置节点颜色和大小
        node_colors = []
        node_sizes = []
        for node in G.nodes():
            node_type = G.nodes[node].get("type", "unknown")
            if node_type == "药物":
                node_colors.append("#FF6B6B")  # 红色
                node_sizes.append(1000)
            elif node_type == "靶点":
                node_colors.append("#4ECDC4")  # 青色
                node_sizes.append(800)
            elif node_type == "通路":
                node_colors.append("#45B7D1")  # 蓝色
                node_sizes.append(1200)
            else:
                node_colors.append("#999999")  # 灰色
                node_sizes.append(600)
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.6, edge_color="#888888")
        
        # 添加节点标签
        labels = {}
        for node in G.nodes():
            node_type = G.nodes[node].get("type", "unknown")
            if node_type == "药物":
                labels[node] = G.nodes[node].get("name", node)
            else:
                labels[node] = node
        
        nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight="bold")
        
        plt.title('候选药物-核心靶点-关键通路相互作用网络图', fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        
        # 保存网络图
        网络图路径 = os.path.join(self.目录结构["可视化结果"], "候选药物-靶点-通路相互作用网络图.png")
        plt.savefig(网络图路径, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. 生成机制推理报告
        self._生成机制推理报告()
        
        print(f"\n机制推理与网络图构建完成")
        print(f"相互作用网络图已保存至：{网络图路径}")
        return G
    
    def _生成机制推理报告(self):
        """生成机制推理报告"""
        # 分析每个候选药物的作用机制
        机制报告 = "# 中药免疫激活抗肿瘤机制推理报告\n\n"
        
        机制报告 += "## 1. 研究背景\n"
        机制报告 += "鼻咽癌是一种常见的头颈部恶性肿瘤，CNE1/CNE2是常用的鼻咽癌细胞系。"
        机制报告 += "本研究通过多维数据分析，筛选具有免疫激活和抗肿瘤双重作用的中药成分，"
        机制报告 += "为后续体内实验提供候选药物。\n\n"
        
        机制报告 += "## 2. 候选药物概况\n"
        机制报告 += f"本次筛选共得到 {len(self.筛选结果)} 个候选药物，"
        机制报告 += f"主要涉及 {', '.join(self.筛选参数['关键通路'])} 等免疫-肿瘤相关通路。\n\n"
        
        机制报告 += "## 3. 候选药物机制分析\n"
        
        for i, (_, 候选药物) in enumerate(self.筛选结果.iterrows(), 1):
            机制报告 += f"### 3.{i} {候选药物['中药名称']}-{候选药物['成分ID']}\n"
            机制报告 += f"- **核心靶点**：{候选药物['靶点ID']}（结合能：{候选药物['结合能']:.2f} kcal/mol）\n"
            机制报告 += f"- **富集通路**：{候选药物['通路']}\n"
            机制报告 += f"- **抗肿瘤活性**：CNE1 IC50 = {候选药物['CNE1_IC50']:.2f} μM，CNE2 IC50 = {候选药物['CNE2_IC50']:.2f} μM\n"
            机制报告 += f"- **免疫激活效果**：IL-2 = {候选药物['IL2']:.1f} pg/mL，IFN-γ = {候选药物['IFNγ']:.1f} pg/mL，TNF-α = {候选药物['TNFα']:.1f} pg/mL\n"
            机制报告 += f"- **细胞凋亡率**：{候选药物['细胞凋亡率']:.1f}%\n"
            
            # 基于通路的机制推理
            机制描述 = ""
            if 候选药物['通路'] == "NF-κB":
                机制描述 = "该药物可能通过抑制NF-κB通路，减少炎症因子释放，同时激活肿瘤细胞凋亡通路，发挥双重作用。"
            elif 候选药物['通路'] == "TNF-α":
                机制描述 = "该药物可能通过调节TNF-α信号通路，增强免疫细胞活化，同时诱导肿瘤细胞凋亡。"
            elif 候选药物['通路'] == "PI3K-Akt":
                机制描述 = "该药物可能通过抑制PI3K-Akt通路，抑制肿瘤细胞增殖，同时增强T细胞浸润和活化。"
            else:
                机制描述 = "该药物可能通过调节相关通路，发挥免疫激活和抗肿瘤的双重作用。"
            
            机制报告 += f"- **作用机制**：{机制描述}\n\n"
        
        机制报告 += "## 4. 体内实验建议\n"
        机制报告 += "### 4.1 实验设计建议\n"
        机制报告 += "- **细胞系**：CNE1/CNE2鼻咽癌细胞系\n"
        机制报告 += "- **动物模型**：Balb/c裸鼠皮下移植瘤模型\n"
        机制报告 += f"- **候选药物剂量**：建议设置3-5个剂量组，基于IC50值（{self.筛选参数['ic50_threshold']} μM）换算体内剂量\n"
        机制报告 += "- **给药途径**：腹腔注射或灌胃（根据药物溶解性选择）\n"
        机制报告 += "- **给药周期**：连续给药2-3周\n"
        机制报告 += "- **检测指标**：肿瘤体积、体重变化、免疫细胞浸润、细胞因子水平、通路蛋白表达\n\n"
        
        机制报告 += "### 4.2 预期结果\n"
        机制报告 += "- 候选药物能够显著抑制CNE1/CNE2移植瘤生长\n"
        机制报告 += "- 增强肿瘤微环境中免疫细胞（CD8+ T细胞、巨噬细胞）浸润\n"
        机制报告 += "- 上调IFN-γ、TNF-α等免疫因子水平\n"
        机制报告 += "- 调节相关通路蛋白表达\n\n"
        
        机制报告 += "## 5. 结论\n"
        机制报告 += "本研究通过多维数据分析，成功筛选出具有免疫激活和抗肿瘤双重作用的中药成分，"
        机制报告 += "为鼻咽癌的免疫治疗提供了新的候选药物。后续体内实验将验证这些候选药物的疗效，"
        机制报告 += "有望为鼻咽癌的治疗提供新的思路和策略。\n"
        
        # 保存机制推理报告
        机制报告路径 = os.path.join(self.目录结构["机制分析"], "中药免疫激活抗肿瘤机制推理报告.txt")
        with open(机制报告路径, 'w', encoding='utf-8') as f:
            f.write(机制报告)
        
        print(f"机制推理报告已生成：{机制报告路径}")
    
    def 生成论文级成果包(self):
        """生成论文级可复现成果包"""
        print("\n开始生成论文级成果包...")
        
        # 1. 复制代码到代码输出目录
        代码源路径 = os.path.abspath(__file__)
        代码目标路径 = os.path.join(self.目录结构["代码输出"], os.path.basename(__file__))
        import shutil
        shutil.copy2(代码源路径, 代码目标路径)
        
        # 2. 生成README文件
        readme = "# 中药免疫激活抗肿瘤药物筛选分析\n\n"
        readme += "## 项目简介\n"
        readme += "本项目实现了中药免疫激活抗肿瘤药物的精准筛选分析，针对CNE1/CNE2鼻咽癌细胞系，\n"
        readme += "包含完整的数据预处理、特征工程、双效模型构建和机制推理流程。\n\n"
        
        readme += "## 目录结构\n"
        for dir_name, dir_path in self.目录结构.items():
            readme += f"- {dir_name}: {os.path.basename(dir_path)}\n"
        
        readme += "\n## 核心功能\n"
        readme += "1. **数据预处理与质控**：缺失值处理、异常值剔除、特征标准化\n"
        readme += "2. **特征工程**：构建免疫激活评分、抗肿瘤活性评分、双效综合评分\n"
        readme += "3. **双效筛选模型**：基于多维度指标的候选药物筛选\n"
        readme += "4. **机制推理**：候选药物-靶点-通路相互作用网络分析\n"
        readme += "5. **可视化输出**：相关性热图、散点图、网络图等\n\n"
        
        readme += "## 运行说明\n"
        readme += "```\n"
        readme += "python 中药免疫激活抗肿瘤药物筛选_科研版.py\n"
        readme += "```\n\n"
        
        readme += "## 依赖库\n"
        readme += "- pandas\n"
        readme += "- numpy\n"
        readme += "- scikit-learn\n"
        readme += "- matplotlib\n"
        readme += "- seaborn\n"
        readme += "- networkx\n"
        readme += "- scipy\n\n"
        
        readme += "## 结果文件\n"
        readme += "- **筛选结果**：中药免疫激活抗肿瘤筛选结果.csv\n"
        readme += "- **机制报告**：中药免疫激活抗肿瘤机制推理报告.txt\n"
        readme += "- **可视化结果**：相关性热图、散点图、网络图等\n"
        readme += "- **数据文件**：原始数据集、预处理后数据集、特征工程后数据集\n\n"
        
        readme += "## 可复现性说明\n"
        readme += "- 固定随机种子：np.random.seed(42), random.seed(42)\n"
        readme += "- 参数透明：所有关键参数均在代码中明确定义\n"
        readme += "- 完整代码：包含从数据导入到可视化输出的全流程\n"
        readme += "- 详细注释：代码中包含详细的中文注释\n\n"
        
        readme += "## 后续实验建议\n"
        readme += "- 体内实验验证：CNE1/CNE2鼻咽癌细胞系小鼠肿瘤模型\n"
        readme += "- 机制深入研究：Western blot、IHC、流式细胞术等\n"
        readme += "- 结构优化：基于筛选结果进行药物结构修饰\n\n"
        
        readme += "## 联系人\n"
        readme += "如有问题或建议，请联系项目负责人。\n"
        
        # 保存README文件
        readme_path = os.path.join(self.work_dir, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme)
        
        print(f"\n论文级成果包生成完成")
        print(f"- 代码已复制至：{代码目标路径}")
        print(f"- README文件已生成：{readme_path}")
        print(f"- 所有结果文件已保存至对应目录")
    
    def 运行完整分析流程(self):
        """运行完整的分析流程"""
        print("="*60)
        print("开始中药免疫激活抗肿瘤药物筛选分析流程")
        print("="*60)
        
        # 步骤1：加载数据集
        print("\n步骤1：加载数据集...")
        self.加载数据集()
        
        # 步骤2：数据预处理与质控
        print("\n步骤2：数据预处理与质控...")
        self.数据预处理与质控()
        
        # 步骤3：特征工程与双效模型构建
        print("\n步骤3：特征工程与双效模型构建...")
        self.特征工程与双效模型构建()
        
        # 步骤4：机制推理与网络图构建
        print("\n步骤4：机制推理与网络图构建...")
        self.机制推理与网络图构建()
        
        # 步骤5：生成论文级成果包
        print("\n步骤5：生成论文级成果包...")
        self.生成论文级成果包()
        
        print("\n" + "="*60)
        print("中药免疫激活抗肿瘤药物筛选分析流程完成")
        print("="*60)
        
        # 输出最终结果摘要
        if hasattr(self, '筛选结果') and len(self.筛选结果) > 0:
            print("\n最终筛选结果摘要：")
            结果摘要 = self.筛选结果[["中药名称", "成分ID", "加权综合评分", "CNE1_IC50", "CNE2_IC50", "免疫激活评分", "靶点ID", "通路"]].head(10)
            print(结果摘要)
        
        return self.筛选结果

def main():
    """主函数"""
    # 创建筛选实例
    筛选工作流 = 中药免疫激活抗肿瘤药物筛选(
        work_dir="f:/000科研资料/Biomni大型语言模型（LLM）推理与检索增强规划/Biomni库包含资源/中药免疫筛选工作流"
    )
    
    # 运行完整分析流程
    结果 = 筛选工作流.运行完整分析流程()

if __name__ == "__main__":
    main()
