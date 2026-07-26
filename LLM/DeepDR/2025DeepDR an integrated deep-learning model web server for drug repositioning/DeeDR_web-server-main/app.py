from flask import Flask, request, jsonify, render_template
import os
import sys
import numpy as np
import pandas as pd
import json

# 导入自定义模型模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from disease_centric import disease_centric_model
from target_centric import target_centric_model

app = Flask(__name__)

# 定义数据集和模型目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'Datasets')
MODEL_DIR = os.path.join(BASE_DIR, 'Models')

# 确保templates目录存在并生成模板文件
def generate_templates():
    """生成所有需要的HTML模板文件"""
    # 确保templates目录存在
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 创建主HTML模板
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeepDR Web Server</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background-color: #2c3e50;
            color: white;
            padding: 20px 0;
            margin-bottom: 30px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .features {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            margin: 30px 0;
        }
        
        .feature-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin: 20px;
            flex: 1;
            min-width: 300px;
            max-width: 500px;
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-card h2 {
            color: #3498db;
            margin-bottom: 15px;
            font-size: 1.8em;
        }
        
        .feature-card p {
            margin-bottom: 20px;
            color: #666;
        }
        
        .btn {
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 4px;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        
        .btn:hover {
            background-color: #2980b9;
        }
        
        .model-info {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin: 30px 0;
        }
        
        .model-info h2 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        .model-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .model-item {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 6px;
            border-left: 4px solid #3498db;
        }
        
        .model-item h3 {
            color: #3498db;
            margin-bottom: 10px;
        }
        
        footer {
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px 0;
            margin-top: 50px;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>DeepDR Web Server</h1>
            <p>基于深度学习的药物重定位集成平台</p>
        </div>
    </header>
    
    <div class="container">
        <div class="features">
            <div class="feature-card">
                <h2>以疾病为中心的DeepDR</h2>
                <p>针对特定疾病，推荐潜在的治疗药物。支持三种模型选项：基于异构网络的模型、集成异构网络与文本挖掘的模型，以及基于知识图谱的模型。</p>
                <a href="/disease_centric" class="btn">开始使用</a>
            </div>
            
            <div class="feature-card">
                <h2>以目标为中心的DeepDR</h2>
                <p>针对特定蛋白质靶点，推荐潜在的药物。支持四种模型选项：两种基于异构网络，一种基于知识图谱，以及结合知识图谱与分子图的协同模型。</p>
                <a href="/target_centric" class="btn">开始使用</a>
            </div>
        </div>
        
        <div class="model-info">
            <h2>集成模型</h2>
            <div class="model-grid">
                <div class="model-item">
                    <h3>DeepDR</h3>
                    <p>基于异构网络的深度学习方法，整合10个网络进行药物定位。</p>
                </div>
                <div class="model-item">
                    <h3>HeTDR</h3>
                    <p>利用异构网络和文本挖掘技术，整合药物特征与生物医学语料库中的疾病特征。</p>
                </div>
                <div class="model-item">
                    <h3>DisKGE</h3>
                    <p>基于知识图谱的药物重定位模型，使用RotatE算法学习实体表示。</p>
                </div>
                <div class="model-item">
                    <h3>DeepDTnet</h3>
                    <p>深度学习方法，在异质药物-基因-疾病网络中识别新靶点和药物重新定位。</p>
                </div>
                <div class="model-item">
                    <h3>AOPEDF</h3>
                    <p>基于网络的计算框架，采用任意阶接近度嵌入的深森林方法预测药物与靶点相互作用。</p>
                </div>
                <div class="model-item">
                    <h3>TarKGE</h3>
                    <p>基于知识图谱的靶点导向药物推荐模型。</p>
                </div>
                <div class="model-item">
                    <h3>KG-MTL</h3>
                    <p>大规模知识图谱增强的多任务学习模型，协同提取知识图谱和分子图的特征。</p>
                </div>
            </div>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <p>&copy; 2025 DeepDR Web Server. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
''')
    
    # 创建以疾病为中心的HTML模板
    with open('templates/disease_centric.html', 'w', encoding='utf-8') as f:
        f.write('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>以疾病为中心的DeepDR</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background-color: #2c3e50;
            color: white;
            padding: 20px 0;
            margin-bottom: 30px;
        }
        
        header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .back-link {
            color: #3498db;
            text-decoration: none;
            margin-bottom: 20px;
            display: inline-block;
        }
        
        .back-link:hover {
            text-decoration: underline;
        }
        
        .form-container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        
        .form-group select,
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        
        .form-row {
            display: flex;
            gap: 20px;
        }
        
        .form-row .form-group {
            flex: 1;
        }
        
        .btn {
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .btn:hover {
            background-color: #2980b9;
        }
        
        .btn-reset {
            background-color: #95a5a6;
        }
        
        .btn-reset:hover {
            background-color: #7f8c8d;
        }
        
        .results-container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
            display: none;
        }
        
        .results-container.show {
            display: block;
        }
        
        .results-header {
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
        }
        
        .results-header h2 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .results-header p {
            color: #666;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        
        th {
            background-color: #f9f9f9;
            font-weight: bold;
            color: #2c3e50;
        }
        
        tr:hover {
            background-color: #f5f5f5;
        }
        
        .drug-name {
            color: #3498db;
            text-decoration: none;
        }
        
        .drug-name:hover {
            text-decoration: underline;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #3498db;
        }
        
        .loading.show {
            display: block;
        }
        
        .disease-list {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .disease-list h2 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        .disease-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .disease-tag {
            background-color: #e3f2fd;
            color: #1976d2;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .disease-tag:hover {
            background-color: #bbdefb;
        }
        
        .visualize-btn {
            background-color: #2ecc71;
            margin-top: 20px;
        }
        
        .visualize-btn:hover {
            background-color: #27ae60;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>以疾病为中心的DeepDR</h1>
            <p>针对特定疾病推荐潜在的治疗药物</p>
        </div>
    </header>
    
    <div class="container">
        <a href="/" class="back-link">← 返回首页</a>
        
        <div class="disease-list">
            <h2>热门疾病</h2>
            <div class="disease-tags">
                {% for disease_id, disease_name in diseases %}
                <span class="disease-tag" data-disease-id="{{ disease_id }}">{{ disease_name }}</span>
                {% endfor %}
            </div>
        </div>
        
        <div class="form-container">
            <h2>药物预测</h2>
            <form id="predict-form">
                <div class="form-row">
                    <div class="form-group">
                        <label for="model">选择模型：</label>
                        <select id="model" name="model">
                            {% for model in models %}
                            <option value="{{ model }}">{{ model }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="disease_id">疾病ID/名称：</label>
                        <input type="text" id="disease_id" name="disease_id" placeholder="例如：C0342731 或 甲羟戊酸激酶缺乏" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="drugs_top">推荐药物数量：</label>
                        <select id="drugs_top" name="drugs_top">
                            <option value="10">10</option>
                            <option value="20" selected>20</option>
                            <option value="50">50</option>
                            <option value="100">100</option>
                        </select>
                    </div>
                </div>
                
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button type="submit" class="btn">预测</button>
                    <button type="reset" class="btn btn-reset">重置</button>
                </div>
            </form>
        </div>
        
        <div class="loading" id="loading">
            <p>正在预测中，请稍候...</p>
        </div>
        
        <div class="results-container" id="results-container">
            <div class="results-header">
                <h2>预测结果</h2>
                <p id="results-info"></p>
            </div>
            
            <table id="results-table">
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>药物ID</th>
                        <th>药物名称</th>
                        <th>预测分数</th>
                    </tr>
                </thead>
                <tbody id="results-body">
                </tbody>
            </table>
            
            <button class="btn visualize-btn" id="visualize-btn" style="display: none;">
                可视化关系路径
            </button>
        </div>
    </div>
    
    <script>
        // 疾病标签点击事件
        document.querySelectorAll('.disease-tag').forEach(tag => {
            tag.addEventListener('click', () => {
                const diseaseId = tag.dataset.diseaseId;
                document.getElementById('disease_id').value = diseaseId;
            });
        });
        
        // 表单提交事件
        document.getElementById('predict-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // 显示加载状态
            document.getElementById('loading').classList.add('show');
            document.getElementById('results-container').classList.remove('show');
            
            // 获取表单数据
            const formData = new FormData(e.target);
            const data = {
                model: formData.get('model'),
                disease_id: formData.get('disease_id'),
                drugs_top: formData.get('drugs_top')
            };
            
            try {
                // 发送预测请求
                const response = await fetch('/predict_disease', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    // 显示结果
                    displayResults(result);
                } else {
                    alert('预测失败：' + result.message);
                }
            } catch (error) {
                console.error('预测错误：', error);
                alert('预测失败，请稍后重试');
            } finally {
                // 隐藏加载状态
                document.getElementById('loading').classList.remove('show');
            }
        });
        
        // 显示预测结果
        function displayResults(result) {
            // 更新结果信息
            document.getElementById('results-info').textContent = 
                `模型：${result.model} | 疾病：${result.disease_name} (${result.disease_id}) | 推荐药物数：${result.results.length}`;
            
            // 清空现有结果
            const tbody = document.getElementById('results-body');
            tbody.innerHTML = '';
            
            // 添加新结果
            result.results.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.rank}</td>
                    <td>${item.drug_id}</td>
                    <td><a href="/drug_detail/${item.drug_id}" class="drug-name">${item.drug_name}</a></td>
                    <td>${item.score.toFixed(4)}</td>
                `;
                tbody.appendChild(row);
            });
            
            // 显示结果容器
            document.getElementById('results-container').classList.add('show');
            
            // 显示可视化按钮（如果模型支持）
            const visualizeBtn = document.getElementById('visualize-btn');
            if (result.model === 'DisKGE') {
                visualizeBtn.style.display = 'inline-block';
                visualizeBtn.onclick = () => {
                    window.location.href = `/visualize_path/${result.model}/${result.disease_id}`;
                };
            } else {
                visualizeBtn.style.display = 'none';
            }
        }
    </script>
</body>
</html>
''')
    
    # 创建以目标为中心的HTML模板
    with open('templates/target_centric.html', 'w', encoding='utf-8') as f:
        f.write('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>以目标为中心的DeepDR</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background-color: #2c3e50;
            color: white;
            padding: 20px 0;
            margin-bottom: 30px;
        }
        
        header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .back-link {
            color: #3498db;
            text-decoration: none;
            margin-bottom: 20px;
            display: inline-block;
        }
        
        .back-link:hover {
            text-decoration: underline;
        }
        
        .form-container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        
        .form-group select,
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        
        .form-row {
            display: flex;
            gap: 20px;
        }
        
        .form-row .form-group {
            flex: 1;
        }
        
        .btn {
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .btn:hover {
            background-color: #2980b9;
        }
        
        .btn-reset {
            background-color: #95a5a6;
        }
        
        .btn-reset:hover {
            background-color: #7f8c8d;
        }
        
        .results-container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
            display: none;
        }
        
        .results-container.show {
            display: block;
        }
        
        .results-header {
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
        }
        
        .results-header h2 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .results-header p {
            color: #666;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        
        th {
            background-color: #f9f9f9;
            font-weight: bold;
            color: #2c3e50;
        }
        
        tr:hover {
            background-color: #f5f5f5;
        }
        
        .drug-name {
            color: #3498db;
            text-decoration: none;
        }
        
        .drug-name:hover {
            text-decoration: underline;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #3498db;
        }
        
        .loading.show {
            display: block;
        }
        
        .target-list {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .target-list h2 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        .target-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .target-tag {
            background-color: #e8f5e8;
            color: #2e7d32;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .target-tag:hover {
            background-color: #c8e6c9;
        }
        
        .visualize-btn {
            background-color: #2ecc71;
            margin-top: 20px;
        }
        
        .visualize-btn:hover {
            background-color: #27ae60;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>以目标为中心的DeepDR</h1>
            <p>针对特定蛋白质靶点推荐潜在的药物</p>
        </div>
    </header>
    
    <div class="container">
        <a href="/" class="back-link">← 返回首页</a>
        
        <div class="target-list">
            <h2>热门靶点</h2>
            <div class="target-tags">
                {% for target_id, target_name in targets %}
                <span class="target-tag" data-target-id="{{ target_id }}">{{ target_name }}</span>
                {% endfor %}
            </div>
        </div>
        
        <div class="form-container">
            <h2>药物预测</h2>
            <form id="predict-form">
                <div class="form-row">
                    <div class="form-group">
                        <label for="model">选择模型：</label>
                        <select id="model" name="model">
                            {% for model in models %}
                            <option value="{{ model }}">{{ model }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="target_id">靶点ID/名称：</label>
                        <input type="text" id="target_id" name="target_id" placeholder="例如：9971 或 NR1H4" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="drugs_top">推荐药物数量：</label>
                        <select id="drugs_top" name="drugs_top">
                            <option value="10">10</option>
                            <option value="20" selected>20</option>
                            <option value="50">50</option>
                            <option value="100">100</option>
                        </select>
                    </div>
                </div>
                
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button type="submit" class="btn">预测</button>
                    <button type="reset" class="btn btn-reset">重置</button>
                </div>
            </form>
        </div>
        
        <div class="loading" id="loading">
            <p>正在预测中，请稍候...</p>
        </div>
        
        <div class="results-container" id="results-container">
            <div class="results-header">
                <h2>预测结果</h2>
                <p id="results-info"></p>
            </div>
            
            <table id="results-table">
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>药物ID</th>
                        <th>药物名称</th>
                        <th>预测分数</th>
                    </tr>
                </thead>
                <tbody id="results-body">
                </tbody>
            </table>
            
            <button class="btn visualize-btn" id="visualize-btn" style="display: none;">
                可视化关系路径
            </button>
        </div>
    </div>
    
    <script>
        // 靶点标签点击事件
        document.querySelectorAll('.target-tag').forEach(tag => {
            tag.addEventListener('click', () => {
                const targetId = tag.dataset.targetId;
                document.getElementById('target_id').value = targetId;
            });
        });
        
        // 表单提交事件
        document.getElementById('predict-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // 显示加载状态
            document.getElementById('loading').classList.add('show');
            document.getElementById('results-container').classList.remove('show');
            
            // 获取表单数据
            const formData = new FormData(e.target);
            const data = {
                model: formData.get('model'),
                target_id: formData.get('target_id'),
                drugs_top: formData.get('drugs_top')
            };
            
            try {
                // 发送预测请求
                const response = await fetch('/predict_target', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    // 显示结果
                    displayResults(result);
                } else {
                    alert('预测失败：' + result.message);
                }
            } catch (error) {
                console.error('预测错误：', error);
                alert('预测失败，请稍后重试');
            } finally {
                // 隐藏加载状态
                document.getElementById('loading').classList.remove('show');
            }
        });
        
        // 显示预测结果
        function displayResults(result) {
            // 更新结果信息
            document.getElementById('results-info').textContent = 
                `模型：${result.model} | 靶点：${result.target_name} (${result.target_id}) | 推荐药物数：${result.results.length}`;
            
            // 清空现有结果
            const tbody = document.getElementById('results-body');
            tbody.innerHTML = '';
            
            // 添加新结果
            result.results.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.rank}</td>
                    <td>${item.drug_id}</td>
                    <td><a href="/drug_detail/${item.drug_id}" class="drug-name">${item.drug_name}</a></td>
                    <td>${item.score.toFixed(4)}</td>
                `;
                tbody.appendChild(row);
            });
            
            // 显示结果容器
            document.getElementById('results-container').classList.add('show');
            
            // 显示可视化按钮（如果模型支持）
            const visualizeBtn = document.getElementById('visualize-btn');
            if (result.model === 'TarKGE' || result.model === 'KG-MTL') {
                visualizeBtn.style.display = 'inline-block';
                visualizeBtn.onclick = () => {
                    window.location.href = `/visualize_path/${result.model}/${result.target_id}`;
                };
            } else {
                visualizeBtn.style.display = 'none';
            }
        }
    </script>
</body>
</html>
''')
    
    # 创建药物详情HTML模板
    with open('templates/drug_detail.html', 'w', encoding='utf-8') as f:
        f.write('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>药物详情 - DeepDR</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background-color: #2c3e50;
            color: white;
            padding: 20px 0;
            margin-bottom: 30px;
        }
        
        .back-link {
            color: #3498db;
            text-decoration: none;
            margin-bottom: 20px;
            display: inline-block;
        }
        
        .back-link:hover {
            text-decoration: underline;
        }
        
        .drug-detail {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .drug-detail h2 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        .drug-info {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .info-item {
            margin-bottom: 15px;
        }
        
        .info-label {
            font-weight: bold;
            color: #555;
            margin-bottom: 5px;
        }
        
        .info-value {
            color: #333;
        }
        
        .related-drugs {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .related-drugs h2 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        .drug-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .drug-item {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #3498db;
        }
        
        .drug-item a {
            color: #3498db;
            text-decoration: none;
            font-weight: bold;
        }
        
        .drug-item a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>药物详情</h1>
        </div>
    </header>
    
    <div class="container">
        <a href="javascript:history.back()" class="back-link">← 返回上一页</a>
        
        <div class="drug-detail">
            <h2>{{ drug_name }}</h2>
            <div class="drug-info">
                <div>
                    <div class="info-item">
                        <div class="info-label">药物ID：</div>
                        <div class="info-value">{{ drug_id }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">药物名称：</div>
                        <div class="info-value">{{ drug_name }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">类型：</div>
                        <div class="info-value">小分子药物</div>
                    </div>
                </div>
                <div>
                    <div class="info-item">
                        <div class="info-label">作用机制：</div>
                        <div class="info-value">待补充</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">靶点：</div>
                        <div class="info-value">待补充</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">适应症：</div>
                        <div class="info-value">待补充</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="related-drugs">
            <h2>相似药物</h2>
            <div class="drug-list">
                <!-- 这里会显示相似药物列表 -->
                <div class="drug-item">
                    <a href="#">相似药物1</a>
                    <div>相似分数：0.95</div>
                </div>
                <div class="drug-item">
                    <a href="#">相似药物2</a>
                    <div>相似分数：0.92</div>
                </div>
                <div class="drug-item">
                    <a href="#">相似药物3</a>
                    <div>相似分数：0.89</div>
                </div>
                <div class="drug-item">
                    <a href="#">相似药物4</a>
                    <div>相似分数：0.87</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
''')
    
    # 创建可视化关系路径HTML模板
    with open('templates/visualize_path.html', 'w', encoding='utf-8') as f:
        f.write('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>可视化关系路径 - DeepDR</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background-color: #2c3e50;
            color: white;
            padding: 20px 0;
            margin-bottom: 30px;
        }
        
        .back-link {
            color: #3498db;
            text-decoration: none;
            margin-bottom: 20px;
            display: inline-block;
        }
        
        .back-link:hover {
            text-decoration: underline;
        }
        
        .visualization {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .visualization h2 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        #network {
            width: 100%;
            height: 600px;
            border: 1px solid #eee;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        
        .node-info {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 6px;
            margin-top: 20px;
        }
        
        .node-info h3 {
            color: #3498db;
            margin-bottom: 15px;
        }
        
        .node-info-item {
            margin-bottom: 10px;
        }
        
        .node-info-label {
            font-weight: bold;
            color: #555;
        }
    </style>
    <!-- 引入vis.js库 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" />
</head>
<body>
    <header>
        <div class="container">
            <h1>可视化关系路径</h1>
            <p>探索药物与疾病/靶点之间的关系网络</p>
        </div>
    </header>
    
    <div class="container">
        <a href="javascript:history.back()" class="back-link">← 返回上一页</a>
        
        <div class="visualization">
            <h2>{{ model_name }} 模型 - {{ disease_or_target_id }} 的关系网络</h2>
            <div id="network"></div>
            
            <div class="node-info" id="node-info">
                <h3>节点信息</h3>
                <p>点击节点查看详细信息</p>
            </div>
        </div>
    </div>
    
    <script>
        // 准备节点和边数据
        const nodes = new vis.DataSet([
            {% for node in nodes %}
            {id: "{{ node.id }}", label: "{{ node.label }}", group: "{{ node.type }}"},
            {% endfor %}
        ]);
        
        const edges = new vis.DataSet([
            {% for edge in edges %}
            {from: "{{ edge.source }}", to: "{{ edge.target }}", label: "{{ edge.label }}"},
            {% endfor %}
        ]);
        
        // 网络配置
        const container = document.getElementById('network');
        const data = {
            nodes: nodes,
            edges: edges
        };
        
        const options = {
            nodes: {
                shape: 'dot',
                size: 20,
                font: {
                    size: 12,
                    color: '#000000'
                },
                borderWidth: 2,
                shadow: true
            },
            edges: {
                width: 1,
                color: {
                    inherit: true
                },
                smooth: {
                    type: 'continuous'
                },
                font: {
                    size: 10,
                    align: 'middle'
                }
            },
            groups: {
                disease_target: {
                    color: {background: '#e74c3c', border: '#c0392b'},
                    shape: 'diamond'
                },
                drug: {
                    color: {background: '#3498db', border: '#2980b9'},
                    shape: 'circle'
                },
                protein: {
                    color: {background: '#2ecc71', border: '#27ae60'},
                    shape: 'box'
                }
            },
            interaction: {
                hover: true,
                tooltipDelay: 300,
                zoomView: true,
                dragView: true
            },
            layout: {
                hierarchical: {
                    enabled: false,
                    levelSeparation: 150
                }
            }
        };
        
        // 创建网络
        const network = new vis.Network(container, data, options);
        
        // 节点点击事件
        network.on('click', function(params) {
            if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                const node = nodes.get(nodeId);
                
                // 更新节点信息面板
                const infoDiv = document.getElementById('node-info');
                infoDiv.innerHTML = `
                    <h3>节点信息</h3>
                    <div class="node-info-item">
                        <span class="node-info-label">ID：</span>
                        <span>${nodeId}</span>
                    </div>
                    <div class="node-info-item">
                        <span class="node-info-label">标签：</span>
                        <span>${node.label}</span>
                    </div>
                    <div class="node-info-item">
                        <span class="node-info-label">类型：</span>
                        <span>${node.group}</span>
                    </div>
                `;
            }
        });
        
        // 初始视图适配
        network.once('stabilized', function() {
            network.fit();
        });
    </script>
</body>
</html>
''')

# 加载疾病字典
def load_disease_dict():
    """加载疾病字典"""
    disease_dict = {}
    # 尝试从不同位置加载疾病字典
    possible_paths = [
        os.path.join(DATASET_DIR, "DeepDR_HeTDR", "disease_dict.txt"),
        os.path.join(DATASET_DIR, "DeepDTnet_AOPEDF", "disease_dict.txt")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) == 2:
                        disease_dict[parts[0]] = parts[1]
            break
    return disease_dict

# 加载蛋白质字典
def load_protein_dict():
    """加载蛋白质字典"""
    protein_dict = {}
    # 尝试从不同位置加载蛋白质字典
    possible_paths = [
        os.path.join(DATASET_DIR, "DeepDR_HeTDR", "protein_dict"),
        os.path.join(DATASET_DIR, "DeepDTnet_AOPEDF", "protein_dict.txt")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) == 2:
                        protein_dict[parts[0]] = parts[1]
            break
    return protein_dict

# 加载药物字典
def load_drug_dict():
    """加载药物字典"""
    drug_dict = {}
    # 尝试从不同位置加载药物字典
    possible_paths = [
        os.path.join(DATASET_DIR, "DeepDR_HeTDR", "drugdrug.txt")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                # 假设第一行是药物列表
                drugs = f.readline().strip().split('\t')
                for i, drug in enumerate(drugs):
                    drug_dict[str(i)] = drug
            break
    return drug_dict

# 初始化全局字典
disease_dict = load_disease_dict()
protein_dict = load_protein_dict()
drug_dict = load_drug_dict()

# 主页路由
@app.route('/')
def home():
    return render_template('index.html')

# 以疾病为中心的DeepDR路由
@app.route('/disease_centric')
def disease_centric():
    models = ["deepDR", "HeTDR", "DisKGE"]
    return render_template('disease_centric.html', models=models, diseases=list(disease_dict.items())[:50])

# 以目标为中心的DeepDR路由
@app.route('/target_centric')
def target_centric():
    models = ["deepDTnet", "AOPEDF", "TarKGE", "KG-MTL"]
    return render_template('target_centric.html', models=models, targets=list(protein_dict.items())[:50])

# 模型预测路由 - 以疾病为中心
@app.route('/predict_disease', methods=['POST'])
def predict_disease():
    """以疾病为中心的药物预测"""
    try:
        data = request.get_json()
        model_name = data.get('model')
        disease_id = data.get('disease_id')
        drugs_top = int(data.get('drugs_top', 20))
        
        # 输入验证
        if not model_name or not disease_id:
            return jsonify({"status": "error", "message": "缺少必要参数"})
        
        # 使用disease_centric_model进行预测
        results = disease_centric_model.predict(model_name, disease_id, drugs_top)
        
        return jsonify({
            "status": "success", 
            "model": model_name,
            "disease_id": disease_id,
            "disease_name": disease_dict.get(disease_id, "未知疾病"),
            "results": results
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# 模型预测路由 - 以目标为中心
@app.route('/predict_target', methods=['POST'])
def predict_target():
    """以目标为中心的药物预测"""
    try:
        data = request.get_json()
        model_name = data.get('model')
        target_id = data.get('target_id')
        drugs_top = int(data.get('drugs_top', 20))
        
        # 输入验证
        if not model_name or not target_id:
            return jsonify({"status": "error", "message": "缺少必要参数"})
        
        # 使用target_centric_model进行预测
        results = target_centric_model.predict(model_name, target_id, drugs_top)
        
        return jsonify({
            "status": "success", 
            "model": model_name,
            "target_id": target_id,
            "target_name": protein_dict.get(target_id, "未知靶点"),
            "results": results
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# 获取可用模型列表
@app.route('/get_models')
def get_models():
    """获取可用模型列表"""
    try:
        models = [d for d in os.listdir(MODEL_DIR) if os.path.isdir(os.path.join(MODEL_DIR, d))]
        return jsonify({"status": "success", "models": models})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# 获取疾病列表
@app.route('/get_diseases')
def get_diseases():
    """获取疾病列表"""
    try:
        return jsonify({"status": "success", "diseases": list(disease_dict.items())})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# 获取靶点列表
@app.route('/get_targets')
def get_targets():
    """获取靶点列表"""
    try:
        return jsonify({"status": "success", "targets": list(protein_dict.items())})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# 药物详情页
@app.route('/drug_detail/<drug_id>')
def drug_detail(drug_id):
    """药物详情页"""
    drug_name = drug_dict.get(drug_id, f"药物{drug_id}")
    return render_template('drug_detail.html', drug_id=drug_id, drug_name=drug_name)

# 可视化关系路径
@app.route('/visualize_path/<model_name>/<disease_or_target_id>')
def visualize_path(model_name, disease_or_target_id):
    """可视化关系路径"""
    try:
        # 根据模型类型选择对应的可视化数据获取方法
        if model_name in ['deepDR', 'HeTDR', 'DisKGE']:
            # 以疾病为中心的模型
            vis_data = disease_centric_model.get_visualization_data(model_name, disease_or_target_id)
        elif model_name in ['deepDTnet', 'AOPEDF', 'TarKGE', 'KG-MTL']:
            # 以目标为中心的模型
            vis_data = target_centric_model.get_visualization_data(model_name, disease_or_target_id)
        else:
            # 未知模型，使用默认数据
            vis_data = {
                "nodes": [
                    {"id": disease_or_target_id, "label": "节点", "type": "disease_target"}
                ],
                "edges": []
            }
        
        return render_template('visualize_path.html', model_name=model_name, 
                               disease_or_target_id=disease_or_target_id, 
                               nodes=vis_data["nodes"], edges=vis_data["edges"])
    except Exception as e:
        return f"可视化失败：{str(e)}"

if __name__ == '__main__':
    # 生成所有模板文件
    generate_templates()
    
    # 启动服务器
    app.run(host='0.0.0.0', port=5000, debug=True)