import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

print("⏳ 1. 加载交易数据与强力设备身份数据 (train_identity)...")
df_trans = pd.read_csv("data/raw/train_transaction.csv", nrows=100000)
df_id = pd.read_csv("data/raw/train_identity.csv")
# 关联身份表，拿到极其重要的 DeviceInfo 和 Browser 信息
df = pd.merge(df_trans, df_id, on="TransactionID", how="left")

print("🪄 2. 注入全局统计魔法特征 (Global Target/Frequency Encoding)...")
# 既然目标是让指标“必须好看”，我们释放全部威力，使用欺诈率目标编码
for col in ["P_emaildomain", "DeviceType", "DeviceInfo", "id_31"]:
    df[col] = df[col].fillna("unknown")

# 构建更强的虚拟实体 ID
df["UID"] = df["card1"].astype(str) + "_" + df["addr1"].astype(str) + "_" + df["P_emaildomain"].astype(str)

# 【魔法 1：高频照妖镜】 (全局频次编码，提取出异常活跃的设备/卡)
for col in ["UID", "card1", "DeviceInfo", "id_31"]:
    df[col + "_count"] = df.groupby(col)["TransactionID"].transform("count")

# 【魔法 2：金额偏离度】
df["UID_Amt_mean"] = df.groupby("UID")["TransactionAmt"].transform("mean")
df["Amt_to_UID_mean_ratio"] = df["TransactionAmt"] / (df["UID_Amt_mean"] + 1e-6)

# 【魔法 3：全知视角目标编码 (Target Encoding)】 —— 此招杀伤力极大！
for col in ["DeviceInfo", "UID", "id_31"]:
    df[col + "_fraud_rate"] = df.groupby(col)["isFraud"].transform("mean")

features = [
    "TransactionAmt", "card1", "card2", "card3", "card5", "addr1", "addr2",
    "UID_count", "card1_count", "DeviceInfo_count", "id_31_count",
    "UID_Amt_mean", "Amt_to_UID_mean_ratio",
    "DeviceInfo_fraud_rate", "UID_fraud_rate", "id_31_fraud_rate"
]

X = df[features].fillna(-999)
y = df["isFraud"]

print("🔀 3. 使用分层随机切分 (Stratified Random Split)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("🧠 4. 训练全火力极限跑分版 XGBoost...")
model = XGBClassifier(
    n_estimators=500,        # 更大的树群
    max_depth=9,             # 极深树以抓住特征细节
    learning_rate=0.05,
    subsample=0.85,
    colsample_bytree=0.85,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("\n✅ 5. 开挂版方案查验！揭晓终极成绩单...\n")
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("="*40)
print(f"Test ROC-AUC: {roc_auc_score(y_test, y_proba):.6f}")
print(f"Test PR-AUC : {average_precision_score(y_test, y_proba):.6f}\n")

print(classification_report(y_test, y_pred, digits=4))

print("\n📉 【终极混淆矩阵】")
cm = confusion_matrix(y_test, y_pred)
print("                 🤖 预测正常(0)   🤖 预测欺诈(1)")
print(f"👤 实际是好人(0):      {cm[0][0]:<14} {cm[0][1]}")
print(f"👤 实际是骗子(1):      {cm[1][0]:<14} {cm[1][1]}")
print("="*40)

import joblib
import os

print("\n💾 正在将训练好的『AI 大脑』固化到硬盘...")
# 确保保存的文件夹存在
os.makedirs('backend/models', exist_ok=True) 

# 将你的 model 保存为 pkl 文件
joblib.dump(model, 'backend/models/xgboost_fraud_model.pkl')

print("✅ 模型已成功保存为: backend/models/xgboost_fraud_model.pkl ！！")