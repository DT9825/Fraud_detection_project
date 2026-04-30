#测试用
import pandas as pd

print("⏳ 正在加载电商交易数据，请稍候 (文件有点大)...")

# 1. 读取我们刚才下载的两个核心数据表
# 为了电脑不卡死，我们先只读取前 10000 行试试水
df_transaction = pd.read_csv('data/raw/train_transaction.csv', nrows=10000)
df_identity = pd.read_csv('data/raw/train_identity.csv', nrows=10000)

# 2. 把交易表和设备信息表，通过交易ID (TransactionID) 拼接到一起
df_merged = pd.merge(df_transaction, df_identity, on='TransactionID', how='left')

print("\n✅ 数据加载与拼接完成！")
print(f"-> 我们一共加载了 {df_merged.shape[0]} 条交易记录，每条记录有 {df_merged.shape[1]} 个特征。")

# 3. 看看“欺诈标签 (isFraud)”的分布
# isFraud = 1 代表这是欺诈交易，0 代表正常交易
fraud_counts = df_merged['isFraud'].value_counts()
fraud_ratio = fraud_counts[1] / len(df_merged) * 100

print("\n🔍 欺诈情况大揭秘：")
print(f"正常交易数量: {fraud_counts[0]}")
print(f"欺诈交易数量: {fraud_counts.get(1, 0)}") # 用get防止前1万条里没有欺诈
print(f"欺诈比例: {fraud_ratio:.2f}%")

print("\n📊 看看前 3 条数据的基本长相：")
# 只挑选几个大家看得懂的列展示出来
display_columns = ['TransactionID', 'TransactionAmt', 'ProductCD', 'DeviceType', 'isFraud']
print(df_merged[display_columns].head(3))