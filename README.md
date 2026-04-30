




TransactionID：交易 ID（每条交易唯一编号）
TransactionAmt：交易金额
ProductCD：产品编码 / 业务类型码
DeviceType：设备类型（如手机、电脑）
isFraud：是否为欺诈交易（标签列，1 = 欺诈，0 = 正常）



# Fraud_Detection_Project 欺诈检测项目
基于图神经网络（GNN）+ 大模型（LLM）+ 可视化大屏的端到端金融交易欺诈检测系统，以下是项目完整结构及说明。
## 项目目录结构
Fraud_Detection_Project/
│
├── data/                  # 专门存放数据
│   ├── raw/               # 存放原始交易数据（如 train_transaction.csv 等）
│   └── processed/         # 存放处理后的数据（核心为图谱特征数据）
│
├── src/                   # 核心算法与数据处理脚本（主要工作区）
│   ├── 1_data_explore.py  # 数据初步探索、异常值/缺失值分析脚本
│   ├── 2_build_graph.py   # 表格数据转关系网（图结构构建脚本）
│   ├── 3_gnn_model.py     # 图神经网络模型搭建、训练与预测
│   ├── 4_llm_agent.py     # 对接DeepSeek/Qwen等大模型的分析接口
│   ├── 3_baseline_model.py #简单传统森林，做对比
│   └── 5_feature_engineering.py #新添数据，featured_transaction.csv
│ 
│   
├── backend/               # 轻量级后端服务（后续开发任务）
│   └── app.py             # 使用FastAPI或Flask，实现算法与前端的连接
│
├── frontend/              # 可视化大屏前端（核心得分点，后续开发任务）
│   ├── index.html         # 大屏主页面
│   └── js/                # 存放ECharts或G6的关系图谱渲染逻辑
│
└── README.md              # 项目说明文档（答辩PPT核心素材库）
## 核心说明
- 数据目录：`data/raw/` 仅本地存放原始数据，禁止上传GitHub，避免数据泄露；`data/processed/` 存放图构建后的特征数据，供模型调用。
- 核心代码区：`src/` 为整个项目的核心，按开发流程命名脚本，便于后续调试、迭代和答辩讲解。
- 前后端：后端负责提供接口，前端负责可视化展示，重点实现欺诈关系网的直观呈现。
- README.md：建议后续补充环境依赖、运行步骤、项目亮点等内容，完善答辩素材。
## 快速运行指引（可后续补充完善）
1. 将原始交易数据放入 `data/raw/` 目录；
2. 按顺序运行 `src/` 下的脚本，完成数据探索、图构建和模型训练；
3. 启动后端 `backend/app.py`，再打开 `frontend/index.html` 查看可视化效果。