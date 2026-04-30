import json
from openai import OpenAI

# 1. 配置阿里通义千问 (Qwen) 的 API
# 【注意】把下面的 "YOUR_QWEN_API_KEY" 换成你在阿里云申请的真实 Key
client = OpenAI(
    api_key="sk-cc6ab4db96624820b3d2cfc1cae44214", 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def generate_risk_report(transaction_data):
    """
    核心武器：调用大模型，将冰冷的数据转化为专业的风控报告
    """
    print(f"⏳ 正在呼叫 Qwen 风控专家，对交易 {transaction_data['交易流水号']} 进行深度审查...")

    # 2. 精心设计的 Prompt（提示词），这就是你的“架构师魔法”
    system_prompt = """
    你现在是国内顶尖电商平台的资深风控安全专家。
    你的任务是接收系统初筛出的高危交易数据，并结合图网络关联信息，撰写一份结构清晰、极具威慑力且专业的《风控审查决议书》。
    报告需包含：
    1. 风险定性（如：疑似黑产群控、盗刷洗钱等）
    2. 异常点深度剖析（结合时间、金额、图谱关联关系进行逻辑推理）
    3. 处置建议（如：拦截交易、冻结设备、人工复核等）
    语气要求：专业、客观、严谨、铁面无私。
    """

    user_prompt = f"请对以下高危交易特征进行评估分析：\n{json.dumps(transaction_data, ensure_ascii=False, indent=2)}"

    # 3. 发送请求给 Qwen 大模型
    try:
        response = client.chat.completions.create(
            model="qwen-plus", # 使用 qwen-plus 或 qwen-max 模型，效果极佳
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3 # 降低温度，让 AI 的回答更稳定、更像机器风控
        )
        
        report = response.choices[0].message.content
        return report

    except Exception as e:
        return f"❌ 呼叫大模型失败，请检查网络或 API Key: {e}"

# ==========================================
# 测试环节：模拟一个被你的算法抓到的“真骗子”
# ==========================================
if __name__ == "__main__":
    # 这是我们从前面 XGBoost/GNN 模型输出结果中，提取出来的某条极高危数据
    mock_fraud_data = {
        "交易流水号": "TX_884823901",
        "交易金额": "500.00 元",
        "交易时间": "凌晨 03:15",
        "初筛危险评分": "98.5% (极高危)",
        "图谱溯源分析": {
            "设备聚集度": "该设备(Device_A)在过去1小时内关联了 12 个不同账号",
            "地址聚集度": "收货地址与历史确诊的 3 个黑产节点重合",
            "邮箱特征": "使用了一次性临时邮箱后缀 (yopmail.com)"
        }
    }

    # 执行生成
    final_report = generate_risk_report(mock_fraud_data)
    
    print("\n" + "="*50)
    print("📋 【智鉴·网盾 - 智能风控审查决议书】")
    print("="*50)
    print(final_report)
    print("="*50)