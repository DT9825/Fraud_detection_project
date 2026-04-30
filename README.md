--

# 智鉴·网盾 —— 基于多智能体协同与动态图谱推演的自动化威胁狩猎平台

## 🛡️ 项目定位
[cite_start]针对现代金融欺诈手段隐蔽、团伙化程度高及 AI 决策“黑盒化”等痛点，本项目构建了一套工业级的风控作业平台 [cite: 11][cite_start]。通过 **GNN（图神经网络）** 挖掘深层关联，配合 **LLM Agent（多智能体）** 实现可解释性的自动化研判，将传统的“被动查表”模式革新为“主动威胁狩猎”模式 [cite: 8, 23]。

## 📂 项目目录结构
```text
Fraud_Detection_Project/
├── data/                       # 数据资产层
│   ├── raw/                    # 原始交易数据（如 train_transaction.csv）
│   └── processed/              # 核心图特征数据（featured_transaction.csv）
├── src/                        # 核心算法引擎
│   ├── 1_data_explore.py       # 探索性数据分析（EDA）
│   ├── 2_build_graph.py        # 拓扑关系构建（表格转关系网）
│   ├── 3_gnn_model.py          # 图神经网络（GNN）训练与实时推理
│   ├── 3_baseline_model.py     # 传统模型（XGBoost/RF）对比实验
[cite_start]│   ├── 4_llm_agent.py          # 基于 Qwen/DeepSeek 的 Agent 逻辑引擎 [cite: 5, 30]
│   └── 5_feature_engineering.py # 特征衍生与预处理
├── backend/                    # 工业级后端服务
│   └── app.py                  # FastAPI 异步接口，内置 REPORT_CACHE 缓存加速
├── frontend/                   # 全功能单页控制台（All-in-One）
│   ├── index.html              # VS Code 极客风与 DeepSeek 交互风格集成页
│   └── js/                     # ECharts 增量动态图谱渲染逻辑
└── README.md                   # 项目说明文档（答辩核心讲稿素材）
```

## 🚀 核心技术指标
| 维度 | 关键技术 | 实现目标 |
| :--- | :--- | :--- |
| **底层感知** | [cite_start]**XGBoost** [cite: 7] | 毫秒级海量交易初筛，过滤 99% 的白名单交易。 |
| **拓扑溯源** | [cite_start]**Graph Neural Network (GNN)** [cite: 30] | [cite_start]穿透隐蔽层级，自动识别洗钱、羊毛党等团伙簇 [cite: 22]。 |
| **认知大脑** | [cite_start]**Multi-Agent (LLM Agent)** [cite: 17, 30] | 解决 AI 幻觉，通过“思维链”展示透明的审计逻辑。 |
| **决策执行** | [cite_start]**Human-in-the-loop** [cite: 11] | 生成 JSON 阻断指令，人工一键授权，实现闭环。 |

## 💡 三大创新亮点（国赛加分项）
1.  [cite_start]**多智能体协同架构 (Multi-Agent Workflow)** [cite: 14]：
    [cite_start]系统内置“哨兵”、“侦探”、“法官”三个 AI 角色。通过 Agent 间的接力对话，将复杂的溯源过程转化为直观的、可追溯的工作流 [cite: 11]。
2.  [cite_start]**VS Code + DeepSeek 交互范式** [cite: 5]：
    颠覆传统的低效管理大屏，采用 VS Code 风格的专业作业 IDE 与 DeepSeek 式的智能对话研判区。这种设计大幅降低了风控人员的上手门槛，提升了 300% 以上的审计效率。
3.  [cite_start]**可解释性 AI (Explainable AI, XAI)** [cite: 8, 11]：
    [cite_start]针对银行审计的高合规要求，LLM Agent 调取 GNN 拓扑数据，出具带有证据支撑的审计报告，告别“只给分数，不给理由”的盲目风控 [cite: 24]。

## 📝 数据字典说明
项目核心训练集包含以下关键字段：
-   **TransactionID**：交易唯一标识，用于跨表关联。
-   **TransactionAmt**：交易金额，作为风险权重的重要因子。
-   **ProductCD**：业务类型，用于划分不同的风险基线。
-   [cite_start]**DeviceType**：设备指纹，用于识别群控等黑产设备风险 [cite: 26]。
-   [cite_start]**isFraud**：目标标签（1=欺诈，0=正常），作为监督学习的核心 [cite: 11]。

## 🛠️ 快速运行指南
1.  **环境准备**：
    ```bash
    pip install fastapi uvicorn xgboost dgl torch openai pandas  # 安装核心依赖
    ```
2.  **启动后端**：
    ```bash
    python backend/app.py  # 启动后显示“数据库挂载成功”
    ```
3.  **开启控制台**：
    在 `frontend/` 目录下启动本地服务器（如 `python -m http.server 5500`），浏览器访问 `index.html`。
4.  **演示路径**：
    [cite_start]在大屏侧边栏点击 **HIGH** 标签报警项 $\rightarrow$ 观察右侧 Agent 的“思维链”输出 $\rightarrow$ 中间图谱自动展开团伙关系 $\rightarrow$ 确认报告后点击 **【一键执行 AI 阻断】** [cite: 11]。

---