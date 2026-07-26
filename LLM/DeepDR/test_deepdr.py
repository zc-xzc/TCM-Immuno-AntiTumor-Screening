import os
import sys

# 强制使用CPU，避免CUDA依赖问题
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# 导入DeepDR库
try:
    from DeepDR import Data, Model, CellEncoder, DrugEncoder, FusionModule
    print("DeepDR库导入成功")
    
    # 测试Data模块
    print("\n测试Data模块...")
    print(f"Data模块包含的类和函数: {dir(Data)}")
    
    # 测试Model模块
    print("\n测试Model模块...")
    print(f"Model模块包含的类和函数: {dir(Model)}")
    
    # 测试CellEncoder模块
    print("\n测试CellEncoder模块...")
    print(f"CellEncoder模块包含的类和函数: {dir(CellEncoder)}")
    
    # 测试DrugEncoder模块
    print("\n测试DrugEncoder模块...")
    print(f"DrugEncoder模块包含的类和函数: {dir(DrugEncoder)}")
    
    # 测试FusionModule模块
    print("\n测试FusionModule模块...")
    print(f"FusionModule模块包含的类和函数: {dir(FusionModule)}")
    
    print("\n所有模块测试成功")
    
except Exception as e:
    print(f"DeepDR库导入失败: {e}")
    import traceback
    traceback.print_exc()