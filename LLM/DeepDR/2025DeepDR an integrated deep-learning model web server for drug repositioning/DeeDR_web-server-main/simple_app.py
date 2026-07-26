from flask import Flask, request, jsonify, render_template
import os
import sys
import numpy as np
import pandas as pd

app = Flask(__name__)

# 加载数据集信息
def load_dataset_info():
    """加载数据集信息"""
    # 示例数据，实际使用时替换为真实数据
    datasets = {
        "DeepDR_HeTDR": {
            "diseases": "Datasets/DeepDR_HeTDR/disease_dict.txt",
            "drugs": "Datasets/DeepDR_HeTDR/drugdrug.txt",
            "drug_disease": "Datasets/DeepDR_HeTDR/drugDisease.txt"
        },
        "DeepDTnet_AOPEDF": {
            "drugs": "Datasets/DeepDTnet_AOPEDF/drugdrug.txt",
            "drug_protein": "Datasets/DeepDTnet_AOPEDF/drugProtein.txt"
        }
    }
    return datasets

@app.route('/')
def home():
    return render_template('simple_index.html')

@app.route('/datasets', methods=['GET'])
def get_datasets():
    """
    获取可用数据集列表
    """
    try:
        datasets = load_dataset_info()
        return jsonify({"status": "success", "datasets": list(datasets.keys())})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/predict', methods=['POST'])
def predict():
    """
    简化的预测端点，返回示例结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        model = data.get('model', 'DeepDR')
        pairs = data.get('pairs', [])
        
        if not pairs:
            return jsonify({"status": "error", "message": "No pairs provided for prediction"})
        
        # 示例预测结果，实际使用时替换为真实模型预测
        results = []
        for pair in pairs:
            cell = pair.get('cell', '')
            drug = pair.get('drug', '')
            # 生成随机预测值作为示例
            prediction = np.random.uniform(0, 1)
            results.append({
                "cell": cell,
                "drug": drug,
                "prediction": float(prediction),
                "model": model
            })
        
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/models', methods=['GET'])
def get_models():
    """
    获取可用模型列表
    """
    try:
        # 获取Models目录下的所有模型
        models_dir = "Models"
        models = [d for d in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, d))]
        return jsonify({"status": "success", "models": models})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # 确保templates目录存在
    if not os.path.exists('templates'):
        os.makedirs('templates')
        
    # 创建一个简单的HTML模板
    with open('templates/simple_index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeepDR 简化版 Web Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .section {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        h2 {
            color: #555;
        }
        .form-group {
            margin: 15px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select, button {
            margin: 5px 0;
            padding: 10px;
            width: 100%;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .pair {
            display: flex;
            gap: 10px;
            margin: 10px 0;
        }
        #result {
            margin-top: 20px;
            padding: 10px;
            background-color: #f0f0f0;
            border-radius: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>DeepDR 简化版 Web Server</h1>
    
    <div class="section">
        <h2>可用模型</h2>
        <div id="modelsList"></div>
    </div>
    
    <div class="section">
        <h2>药物响应预测</h2>
        <div class="form-group">
            <label for="modelSelect">选择模型:</label>
            <select id="modelSelect">
                <option value="DeepDR">DeepDR</option>
                <option value="HeTDR">HeTDR</option>
                <option value="AOPEDF">AOPEDF</option>
                <option value="KG-MTL">KG-MTL</option>
                <option value="deepDTnet">deepDTnet</option>
            </select>
        </div>
        
        <h3>药物-细胞对</h3>
        <div id="pairsContainer">
            <div class="pair">
                <input type="text" placeholder="细胞名称" class="cell-input" value="CAL120">
                <input type="text" placeholder="药物名称" class="drug-input" value="5-Fluorouracil">
            </div>
            <div class="pair">
                <input type="text" placeholder="细胞名称" class="cell-input" value="CAL51">
                <input type="text" placeholder="药物名称" class="drug-input" value="Afuresertib">
            </div>
        </div>
        <button id="addPairBtn">添加更多对</button>
        <button id="predictBtn">预测</button>
        
        <div id="result"></div>
    </div>
    
    <script>
        // 加载可用模型
        async function loadModels() {
            try {
                const response = await fetch('/models');
                const data = await response.json();
                if (data.status === 'success') {
                    const modelsList = document.getElementById('modelsList');
                    modelsList.innerHTML = '<h3>可用模型:</h3><ul>' + 
                        data.models.map(model => `<li>${model}</li>`).join('') + '</ul>';
                }
            } catch (error) {
                console.error('加载模型失败:', error);
            }
        }
        
        // 添加更多药物-细胞对
        document.getElementById('addPairBtn').addEventListener('click', () => {
            const container = document.getElementById('pairsContainer');
            const pairDiv = document.createElement('div');
            pairDiv.className = 'pair';
            pairDiv.innerHTML = `
                <input type="text" placeholder="细胞名称" class="cell-input">
                <input type="text" placeholder="药物名称" class="drug-input">
            `;
            container.appendChild(pairDiv);
        });
        
        // 预测
        document.getElementById('predictBtn').addEventListener('click', async () => {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '预测中...';
            
            // 收集所有药物-细胞对
            const pairs = [];
            const cellInputs = document.querySelectorAll('.cell-input');
            const drugInputs = document.querySelectorAll('.drug-input');
            const modelSelect = document.getElementById('modelSelect');
            const selectedModel = modelSelect.value;
            
            for (let i = 0; i < cellInputs.length; i++) {
                const cell = cellInputs[i].value.trim();
                const drug = drugInputs[i].value.trim();
                if (cell && drug) {
                    pairs.push({ cell: cell, drug: drug });
                }
            }
            
            if (pairs.length === 0) {
                resultDiv.innerHTML = '请输入至少一对药物-细胞';
                return;
            }
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 
                        model: selectedModel, 
                        pairs: pairs 
                    })
                });
                const data = await response.json();
                
                if (data.status === 'success') {
                    // 显示预测结果
                    let resultHTML = '<h3>预测结果:</h3>';
                    resultHTML += '<table><tr><th>细胞</th><th>药物</th><th>预测值</th><th>模型</th></tr>';
                    data.results.forEach(item => {
                        resultHTML += `<tr><td>${item.cell}</td><td>${item.drug}</td><td>${item.prediction.toFixed(4)}</td><td>${item.model}</td></tr>`;
                    });
                    resultHTML += '</table>';
                    resultDiv.innerHTML = resultHTML;
                } else {
                    resultDiv.innerHTML = '预测失败: ' + data.message;
                }
            } catch (error) {
                resultDiv.innerHTML = '预测失败: ' + error.message;
            }
        });
        
        // 页面加载时加载模型列表
        window.onload = loadModels;
    </script>
</body>
</html>
''')

    app.run(host='0.0.0.0', port=5000, debug=False)