import os
import torch
print('PyTorch版本:', torch.__version__)
print('CUDA可用:', torch.cuda.is_available())
print('CUDA版本:', torch.version.cuda)

# 尝试导入DeepDR的核心模块
try:
    print('\n尝试导入DeepDR...')
    from deepdr import Data, Model, CellEncoder, DrugEncoder, FusionModule
    print('DeepDR导入成功!')
    
    # 尝试创建一个简单的模型
    print('\n尝试创建模型...')
    model = Model.DrModel(
        CellEncoder.DNN(6163, 100),
        DrugEncoder.MPG(),
        FusionModule.DNN(100, 768)
    )
    print('模型创建成功!')
    
    # 将模型移动到GPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    print(f'模型已移动到设备: {device}')
    
    print('\nDeepDR在CUDA环境下运行成功!')
except ImportError as e:
    print(f'导入错误: {e}')
except Exception as e:
    print(f'运行错误: {e}')
