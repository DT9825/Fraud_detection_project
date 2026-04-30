import pandas as pd
import numpy as np

print("⏳ 1. 正在把原始数据拉进『特征加工厂』...")
# 为了快速验证，我们读取 50000 条
df = pd.read_csv('data/raw/train_transaction.csv', nrows=50000)

print("🛠️ 2. 开始施展特征工程魔法...")

# 【魔法 1：时间刺客】
# 假设 TransactionDT 的一天是 86400 秒，我们强行把它转成 0-23 的小时分布
df['Transaction_Hour'] = np.floor(df['TransactionDT'] / 3600) % 24
print("  -> 已生成: 交易小时特征 (Transaction_Hour)")

# 【魔法 2：小数点的秘密】
# 把金额的小数部分单独拎出来 (比如 14.99 变成 0.99)
df['TransactionAmt_Decimal'] = df['TransactionAmt'] - np.floor(df['TransactionAmt'])
print("  -> 已生成: 金额尾数特征 (TransactionAmt_Decimal)")

# 【魔法 3：频次照妖镜】(非常重要！)
# 统计每张卡(card1)在数据集里到底出现了多少次
df['Card_Freq_Count'] = df.groupby('card1')['TransactionID'].transform('count')
print("  -> 已生成: 银行卡高频使用特征 (Card_Freq_Count)")

# 【魔法 4：邮箱后缀挖掘】
# 骗子经常用一些临时邮箱，我们把邮箱后缀单独提取出来，作为分类特征
df['Email_Domain'] = df['P_emaildomain'].str.split('.').str[0]
# 用最简单的频率编码把它变成数字
email_freq = df['Email_Domain'].value_counts(normalize=True).to_dict()
df['Email_Domain_Encoded'] = df['Email_Domain'].map(email_freq)
print("  -> 已生成: 邮箱风险画像 (Email_Domain_Encoded)")


print("\n✅ 3. 特征加工完成！来看看新造出的神兵利器：")
# 展示新增的几列特征
new_features = ['isFraud', 'TransactionAmt', 'Transaction_Hour', 'TransactionAmt_Decimal', 'Card_Freq_Count', 'Email_Domain_Encoded']
print(df[new_features].head(10))

# 4. 把加工好的数据保存下来，留给接下来的模型用！
df.to_csv('data/processed/featured_transaction.csv', index=False)
print("\n💾 加工后的数据已保存至 'data/processed/featured_transaction.csv'！")