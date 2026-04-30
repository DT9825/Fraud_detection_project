import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

print("⏳ 1. 正在加载数据 (这次我们多读一点，10万条)...")
df_trans = pd.read_csv('data/raw/train_transaction.csv', nrows=100000)

print("🛠️ 2. 正在提取基础特征 (传统模型的做法)...")
# 我们只挑选一些基础的金额、银行卡号、地址等数值特征
features = ['TransactionAmt', 'card1', 'card2', 'card3', 'card5', 'addr1', 'addr2']
X = df_trans[features]
y = df_trans['isFraud']

# 真实数据里有很多空值(NaN)，我们用 -999 填补（这是树模型常用的偷懒小妙招）
X = X.fillna(-999)

# 把数据拆分成“复习题（训练集 80%）”和“考试题（测试集 20%）”
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"🧠 3. 正在训练传统AI模型 (随机森林)...")
print(f"   训练集大小: {len(X_train)} 条，测试集大小: {len(X_test)} 条")
# 设置 n_jobs=-1 让你的电脑全速运转训练
clf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
clf.fit(X_train, y_train)

print("✅ 4. 训练完成！正在阅卷...\n")
y_pred = clf.predict(X_test)

print("="*40)
print("📊 【AI 考试成绩单（分类报告）】")
print("="*40)
print(classification_report(y_test, y_pred, digits=4))

print("\n📉 【混淆矩阵 (揭露 AI 的真实面目)】")
cm = confusion_matrix(y_test, y_pred)
print("                 🤖 AI预测正常(0)   🤖 AI预测欺诈(1)")
print(f"👤 实际是好人(0):      {cm[0][0]:<14} {cm[0][1]}")
print(f"👤 实际是骗子(1):      {cm[1][0]:<14} {cm[1][1]}")
print("="*40)