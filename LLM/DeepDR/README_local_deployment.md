# DeepDR 本地部署指南

根据官方文档，DeepDR支持本地部署，本指南将详细介绍部署步骤和使用方法。

## 1. 环境要求

| 依赖项 | 版本要求 | 说明 |
|-------|---------|------|
| Python | 3.7.11 | 推荐版本 |
| PyTorch | 1.10.0+cu111 | 支持CUDA 11.1的版本 |
| torchvision | 0.11.0+cu111 | 与PyTorch版本匹配 |
| torchaudio | 0.10.0 | 与PyTorch版本匹配 |
| torch_geometric | 2.0.3 | 图神经网络库 |
| torch-cluster | 1.5.9 | 图神经网络扩展 |
| torch-scatter | 2.0.9 | 图神经网络扩展 |
| torch-sparse | 0.6.12 | 图神经网络扩展 |
| torch-spline-conv | 1.2.1 | 图神经网络扩展 |
| deepdr | 2.0.1 | 核心库 |

## 2. 安装步骤

### 2.1 使用conda创建环境（推荐）

```bash
# 创建conda环境
conda create -n deepdr python=3.7.11
conda activate deepdr

# 安装PyTorch及相关库
pip install torch==1.10.0+cu111 torchvision==0.11.0+cu111 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html

# 安装PyG相关库
pip install torch_geometric==2.0.3
pip install https://data.pyg.org/whl/torch-1.10.0%2Bcu113/torch_cluster-1.5.9-cp37-cp37m-linux_x86_64.whl
pip install https://data.pyg.org/whl/torch-1.10.0%2Bcu113/torch_scatter-2.0.9-cp37-cp37m-linux_x86_64.whl
pip install https://data.pyg.org/whl/torch-1.10.0%2Bcu113/torch_sparse-0.6.12-cp37-cp37m-linux_x86_64.whl
pip install https://data.pyg.org/whl/torch-1.10.0%2Bcu113/torch_spline_conv-1.2.1-cp37-cp37m-linux_x86_64.whl

# 安装DeepDR库
pip install deepdr -i https://pypi.org/simple
```

### 2.2 使用pip直接安装

如果已存在Python环境，可直接使用pip安装：

```bash
# 安装PyTorch及相关库
pip install torch==1.10.0+cpu torchvision==0.11.0+cpu torchaudio==0.10.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

# 安装PyG相关库
pip install torch_geometric==2.0.3
pip install torch-cluster==1.5.9 torch-scatter==2.0.9 torch-sparse==0.6.12 torch-spline-conv==1.2.1

# 安装DeepDR库
pip install deepdr -i https://pypi.org/simple
```

## 3. 验证安装

创建一个简单的测试脚本 `test_deepdr.py`：

```python
from DeepDR import Data, Model, CellEncoder, DrugEncoder, FusionModule
print("DeepDR库导入成功")
print(f"Data模块: {dir(Data)}")
print(f"Model模块: {dir(Model)}")
print(f"CellEncoder模块: {dir(CellEncoder)}")
print(f"DrugEncoder模块: {dir(DrugEncoder)}")
print(f"FusionModule模块: {dir(FusionModule)}")
```

运行测试脚本：

```bash
python test_deepdr.py
```

如果输出各模块的内容，则安装成功。

## 4. 使用示例

### 4.1 完整示例脚本

查看 `deepdr_example.py` 文件，该脚本演示了从数据准备到模型训练和预测的完整流程：

```bash
python deepdr_example.py
```

### 4.2 核心功能示例

#### 4.2.1 数据构建与清理

```python
from DeepDR import Data

# 使用集成响应数据
data = Data.DrData(
    Data.DrRead.PairDef('CCLE', 'ActArea'),  # 集成响应数据
    cell_ft='EXP',  # 细胞特征类型
    drug_ft='Graph'  # 药物特征类型
).clean()
```

#### 4.2.2 数据分割

```python
# 采用leave-cell-out分割方式
train_data, val_data, test_data = data.split(
    split_type='cell_out',
    fold=1,
    ratio=[0.8, 0.2, 0.0],
    seed=1
)
```

#### 4.2.3 模型构建

```python
from DeepDR import Model, CellEncoder, DrugEncoder, FusionModule

# 构建模型
model = Model.DrModel(
    cell_encoder=CellEncoder.DNN(6163, 100),
    drug_encoder=DrugEncoder.MPG(),
    fusion_module=FusionModule.DNN(100, 768)
)
```

#### 4.2.4 模型训练

```python
from DeepDR import Data

# 构建数据加载器
train_loader = Data.DrDataLoader(Data.DrDataset(train_data[0]), batch_size=64, shuffle=True)
val_loader = Data.DrDataLoader(Data.DrDataset(val_data[0]), batch_size=64, shuffle=False)

# 训练模型
result = Model.Train(
    model=model,
    epochs=100,
    lr=1e-4,
    train_loader=train_loader,
    val_loader=val_loader
)
```

#### 4.2.5 预测

```python
# 设置要预测的药物-细胞对
data.pair_ls = [['CAL120', '5-Fluorouracil'], ['CAL51', 'Afuresertib']]

# 进行预测
prediction = Model.Predict(model=result[0], data=data)
```

## 5. Web服务器部署

### 5.1 简化版Web服务器

已创建 `simple_app.py` 文件，提供了一个简化版的Web服务器，可用于演示DeepDR的基本功能：

```bash
python simple_app.py
```

服务器将运行在 http://localhost:5000

### 5.2 完整Web服务器集成

要集成完整的DeepDR功能，需要修改 `simple_app.py` 中的 `predict()` 函数，添加实际的DeepDR模型调用逻辑。

## 6. 常见问题

### 6.1 CUDA相关错误

如果在非CUDA环境中运行，可能会遇到CUDA相关错误。解决方法：

```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # 强制使用CPU
```

### 6.2 缺少依赖库

使用pip安装缺少的依赖库：

```bash
pip install [缺失的库名]
```

### 6.3 数据文件问题

DeepDR使用的集成数据存储在库的安装目录中，首次使用时会自动下载。

## 7. 扩展开发

### 7.1 自定义数据

可以使用自己的数据进行训练和预测，具体方法参考官方文档：

```python
# 使用自定义响应数据
data = Data.DrData(
    pair_ls=Data.DrRead.PairCSV('your_data.csv'),  # 自定义CSV文件
    cell_ft=your_cell_dict,  # 自定义细胞特征字典
    drug_ft=your_drug_dict  # 自定义药物特征字典
).clean()
```

### 7.2 自定义模型

可以组合不同的细胞编码器、药物编码器和融合模块，创建自定义模型：

```python
# 组合不同的编码器和融合模块
model = Model.DrModel(
    cell_encoder=CellEncoder.CNN(...),
    drug_encoder=DrugEncoder.AttentiveFP(...),
    fusion_module=FusionModule.MHA(...)
)
```

## 8. 参考资料

- [DeepDR官方文档](https://deepdr.readthedocs.io/en/latest/)
- [DeepDR GitHub仓库](https://github.com/ChengF-Lab/DeepDR)

## 9. 目录结构

```
DeepDR/
├── README_local_deployment.md  # 本地部署指南
├── deepdr_example.py          # 完整示例脚本
├── simple_app.py              # 简化版Web服务器
├── test_deepdr.py            # 安装验证脚本
└── test_server.py            # Web服务器测试脚本
```

## 10. 联系方式

如有问题，请参考官方文档或联系DeepDR开发团队。
