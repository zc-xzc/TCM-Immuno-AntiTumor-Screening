#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DeepDR示例脚本
按照官方文档实现药物响应预测的完整流程
"""

import os
import sys

# 环境设置（在支持CUDA的环境中可以注释掉以下两行）
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # 强制使用CPU
os.environ['DGLBACKEND'] = 'pytorch'       # 设置DGL后端

# 导入DeepDR库
from DeepDR import Data, Model, CellEncoder, DrugEncoder, FusionModule

def main():
    """主函数，演示DeepDR完整流程"""
    print("DeepDR药物响应预测示例")
    print("=" * 50)
    
    # 步骤1: 构建和清理数据
    print("\n步骤1: 构建和清理数据")
    print("=" * 30)
    try:
        data = Data.DrData(
            Data.DrRead.PairDef('CCLE', 'ActArea'),  # 集成响应数据
            cell_ft='EXP',  # 细胞特征类型
            drug_ft='Graph'  # 药物特征类型
        ).clean()
        print("数据构建和清理完成")
        print(f"数据包含 {len(data.pair_ls)} 个药物-细胞对")
    except Exception as e:
        print(f"数据构建失败: {e}")
        return
    
    # 步骤2: 分割响应数据
    print("\n步骤2: 分割响应数据")
    print("=" * 30)
    try:
        # 采用leave-cell-out分割方式，fold=1表示第一个折，ratio=[训练比例, 验证比例, 测试比例]
        train_data, val_data, _ = data.split(
            split_type='cell_out', 
            fold=1, 
            ratio=[0.8, 0.2, 0.0],  # 80%训练，20%验证，0%测试
            seed=1  # 随机种子
        )
        print("数据分割完成")
        print(f"训练集大小: {len(train_data[0].pair_ls)}")
        print(f"验证集大小: {len(val_data[0].pair_ls)}")
    except Exception as e:
        print(f"数据分割失败: {e}")
        return
    
    # 步骤3: 构建和加载数据集
    print("\n步骤3: 构建和加载数据集")
    print("=" * 30)
    try:
        # 构建训练数据集和数据加载器
        train_loader = Data.DrDataLoader(
            Data.DrDataset(train_data[0]), 
            batch_size=64, 
            shuffle=True
        )
        
        # 构建验证数据集和数据加载器
        val_loader = Data.DrDataLoader(
            Data.DrDataset(val_data[0]), 
            batch_size=64, 
            shuffle=False
        )
        print("数据集和数据加载器构建完成")
    except Exception as e:
        print(f"数据集构建失败: {e}")
        return
    
    # 步骤4: 构建预测模型
    print("\n步骤4: 构建预测模型")
    print("=" * 30)
    try:
        # 构建模型：DNN细胞编码器 + MPG药物编码器 + DNN融合模块
        model = Model.DrModel(
            cell_encoder=CellEncoder.DNN(6163, 100),  # DNN细胞编码器，输入维度6163，输出维度100
            drug_encoder=DrugEncoder.MPG(),  # MPG药物编码器
            fusion_module=FusionModule.DNN(100, 768)  # DNN融合模块，输入维度100和768
        )
        print("模型构建完成")
    except Exception as e:
        print(f"模型构建失败: {e}")
        return
    
    # 步骤5: 训练和验证模型
    print("\n步骤5: 训练和验证模型")
    print("=" * 30)
    try:
        # 训练模型
        result = Model.Train(
            model=model, 
            epochs=100,  # 训练轮数
            lr=1e-4,  # 学习率
            train_loader=train_loader,  # 训练数据加载器
            val_loader=val_loader  # 验证数据加载器
        )
        print("模型训练完成")
        print(f"最佳验证集指标: {result[1]}")
        
        # 获取训练好的模型
        trained_model = result[0]
    except Exception as e:
        print(f"模型训练失败: {e}")
        return
    
    # 步骤6: 进行预测
    print("\n步骤6: 进行预测")
    print("=" * 30)
    try:
        # 设置要预测的药物-细胞对
        data.pair_ls = [
            ['CAL120', '5-Fluorouracil'],
            ['CAL51', 'Afuresertib']
        ]
        
        # 进行预测
        prediction_result = Model.Predict(
            model=trained_model, 
            data=data
        )
        print("预测完成")
        print(f"预测结果: {prediction_result}")
        
        # 输出详细预测结果
        for i, pair in enumerate(data.pair_ls):
            print(f"\n细胞: {pair[0]}, 药物: {pair[1]}")
            print(f"预测响应值: {prediction_result[i]}")
            
    except Exception as e:
        print(f"预测失败: {e}")
        return
    
    print("\n" + "=" * 50)
    print("DeepDR示例运行完成！")

if __name__ == "__main__":
    main()