import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import minmax_scale

# 添加模型目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'Models'))

class TargetCentricModel:
    """以目标为中心的DeepDR模型集成类"""
    
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(__file__), 'Models')
        self.datasets_dir = os.path.join(os.path.dirname(__file__), 'Datasets')
        self.loaded_models = {}
        
    def load_model(self, model_name):
        """加载指定的模型"""
        if model_name in self.loaded_models:
            return self.loaded_models[model_name]
        
        model = None
        if model_name == 'deepDTnet':
            # 加载deepDTnet模型
            model = self._load_deepdtnet_model()
        elif model_name == 'AOPEDF':
            # 加载AOPEDF模型
            model = self._load_aopedf_model()
        elif model_name == 'TarKGE':
            # 加载TarKGE模型
            model = self._load_tarkge_model()
        elif model_name == 'KG-MTL':
            # 加载KG-MTL模型
            model = self._load_kgmtl_model()
        
        if model:
            self.loaded_models[model_name] = model
        
        return model
    
    def _load_deepdtnet_model(self):
        """加载deepDTnet模型"""
        try:
            # 这里实现deepDTnet模型的加载逻辑
            deepdtnet_dir = os.path.join(self.models_dir, 'deepDTnet')
            # deepDTnet可能需要加载多个组件
            return {"status": "loaded", "path": deepdtnet_dir}
        except Exception as e:
            print(f"加载deepDTnet模型失败: {str(e)}")
            return None
    
    def _load_aopedf_model(self):
        """加载AOPEDF模型"""
        try:
            # 这里实现AOPEDF模型的加载逻辑
            aopedf_dir = os.path.join(self.models_dir, 'AOPEDF')
            # 导入AOPEDF模型
            sys.path.append(aopedf_dir)
            from AOPEDF import AOPEDF as AOPEDFModel
            return AOPEDFModel()
        except Exception as e:
            print(f"加载AOPEDF模型失败: {str(e)}")
            return None
    
    def _load_tarkge_model(self):
        """加载TarKGE模型"""
        try:
            # 这里实现TarKGE模型的加载逻辑
            tarkge_dir = os.path.join(self.models_dir, 'KG-MTL')  # 假设TarKGE基于KG-MTL架构
            return {"status": "loaded", "path": tarkge_dir}
        except Exception as e:
            print(f"加载TarKGE模型失败: {str(e)}")
            return None
    
    def _load_kgmtl_model(self):
        """加载KG-MTL模型"""
        try:
            # 这里实现KG-MTL模型的加载逻辑
            kgmtl_dir = os.path.join(self.models_dir, 'KG-MTL')
            
            # 导入KG-MTL模型组件
            sys.path.append(kgmtl_dir)
            from model import KGMTLModel
            
            # 加载预训练模型
            # 假设模型文件名为model.pth
            model_path = os.path.join(kgmtl_dir, 'model.pth')
            if os.path.exists(model_path):
                # 这里需要根据KG-MTL模型的具体实现来加载
                return {"status": "loaded", "path": kgmtl_dir, "model_type": "KG-MTL"}
            else:
                print("未找到KG-MTL模型文件")
                return {"status": "loaded", "path": kgmtl_dir}
        except Exception as e:
            print(f"加载KG-MTL模型失败: {str(e)}")
            return None
    
    def predict(self, model_name, target_id, drugs_top=20):
        """
        使用指定模型预测针对特定靶点的药物
        
        参数:
        model_name: str - 模型名称 ('deepDTnet', 'AOPEDF', 'TarKGE', 'KG-MTL')
        target_id: str - 靶点ID
        drugs_top: int - 返回的药物数量
        
        返回:
        list - 药物推荐列表，包含rank, drug_id, drug_name, score
        """
        model = self.load_model(model_name)
        
        # 如果模型加载失败，仍然返回模拟结果
        if not model:
            print(f"无法加载模型: {model_name}，返回模拟结果")
            return self._generate_random_results(drugs_top)
        
        if model_name == 'deepDTnet':
            return self._predict_deepdtnet(model, target_id, drugs_top)
        elif model_name == 'AOPEDF':
            return self._predict_aopedf(model, target_id, drugs_top)
        elif model_name == 'TarKGE':
            return self._predict_tarkge(model, target_id, drugs_top)
        elif model_name == 'KG-MTL':
            return self._predict_kgmtl(model, target_id, drugs_top)
        else:
            print(f"不支持的模型: {model_name}，返回模拟结果")
            return self._generate_random_results(drugs_top)
    
    def _predict_deepdtnet(self, model, target_id, drugs_top):
        """使用deepDTnet模型进行预测"""
        try:
            # 实现deepDTnet模型的预测逻辑
            deepdtnet_data_dir = os.path.join(self.datasets_dir, 'DeepDTnet_AOPEDF')
            
            # 加载药物-蛋白质关联矩阵
            drug_protein_path = os.path.join(deepdtnet_data_dir, 'drugProtein.txt')
            if not os.path.exists(drug_protein_path):
                # 如果没有真实数据，生成随机结果
                return self._generate_random_results(drugs_top)
            
            drug_protein = pd.read_csv(drug_protein_path, sep='\t', header=None)
            
            # 将靶点ID转换为索引（假设靶点在列上）
            target_idx = int(target_id) if target_id.isdigit() else 0
            target_idx = min(target_idx, drug_protein.shape[1] - 1)
            
            # 使用药物-蛋白质关联值作为预测分数
            scores = drug_protein.iloc[:, target_idx].values
            
            # 排序并返回结果
            sorted_indices = np.argsort(scores)[::-1][:drugs_top]
            
            results = []
            for rank, idx in enumerate(sorted_indices, 1):
                results.append({
                    "rank": rank,
                    "drug_id": str(idx),
                    "drug_name": f"药物{idx}",
                    "score": float(round(scores[idx], 4))
                })
            
            return results
        except Exception as e:
            print(f"deepDTnet预测失败: {str(e)}")
            return self._generate_random_results(drugs_top)
    
    def _predict_aopedf(self, model, target_id, drugs_top):
        """使用AOPEDF模型进行预测"""
        try:
            # 这里实现AOPEDF模型的预测逻辑
            # AOPEDF是基于深森林的模型，需要特定的输入格式
            
            # 生成示例结果
            results = []
            for i in range(drugs_top):
                results.append({
                    "rank": i+1,
                    "drug_id": str(i),
                    "drug_name": f"药物{i}",
                    "score": round(np.random.uniform(0.7, 1.0), 4)
                })
            
            return results
        except Exception as e:
            print(f"AOPEDF预测失败: {str(e)}")
            return self._generate_random_results(drugs_top)
    
    def _predict_tarkge(self, model, target_id, drugs_top):
        """使用TarKGE模型进行预测"""
        try:
            # 这里实现TarKGE模型的预测逻辑
            # TarKGE基于知识图谱嵌入，需要计算药物与靶点之间的距离
            
            # 生成示例结果
            results = []
            for i in range(drugs_top):
                results.append({
                    "rank": i+1,
                    "drug_id": str(i),
                    "drug_name": f"药物{i}",
                    "score": round(np.random.uniform(0.7, 1.0), 4)
                })
            
            return results
        except Exception as e:
            print(f"TarKGE预测失败: {str(e)}")
            return self._generate_random_results(drugs_top)
    
    def _predict_kgmtl(self, model, target_id, drugs_top):
        """使用KG-MTL模型进行预测"""
        try:
            # 这里实现KG-MTL模型的预测逻辑
            # KG-MTL是知识图谱增强的多任务学习模型
            
            # 生成示例结果
            results = []
            for i in range(drugs_top):
                results.append({
                    "rank": i+1,
                    "drug_id": str(i),
                    "drug_name": f"药物{i}",
                    "score": round(np.random.uniform(0.7, 1.0), 4)
                })
            
            return results
        except Exception as e:
            print(f"KG-MTL预测失败: {str(e)}")
            return self._generate_random_results(drugs_top)
    
    def _generate_random_results(self, drugs_top):
        """生成随机结果（用于测试）"""
        results = []
        for i in range(drugs_top):
            results.append({
                "rank": i+1,
                "drug_id": str(i),
                "drug_name": f"药物{i}",
                "score": round(np.random.uniform(0.7, 1.0), 4)
            })
        return results
    
    def get_visualization_data(self, model_name, target_id):
        """获取可视化数据"""
        if model_name not in ['TarKGE', 'KG-MTL']:
            return {"nodes": [], "edges": []}
        
        # 生成示例可视化数据
        nodes = [
            {"id": target_id, "label": "靶点", "type": "disease_target"},
            {"id": "drug1", "label": "药物1", "type": "drug"},
            {"id": "drug2", "label": "药物2", "type": "drug"},
            {"id": "protein1", "label": "蛋白质1", "type": "protein"},
            {"id": "protein2", "label": "蛋白质2", "type": "protein"}
        ]
        
        edges = [
            {"source": target_id, "target": "protein1", "label": "关联"},
            {"source": target_id, "target": "protein2", "label": "关联"},
            {"source": "protein1", "target": "drug1", "label": "作用于"},
            {"source": "protein2", "target": "drug2", "label": "作用于"},
            {"source": "drug1", "target": "drug2", "label": "相似"}
        ]
        
        return {"nodes": nodes, "edges": edges}

# 创建全局模型实例
target_centric_model = TargetCentricModel()