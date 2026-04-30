import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

print("⏳ 正在构建交易关系图谱...")

# 1. 读取少量数据用于演示
df_trans = pd.read_csv('data/raw/train_transaction.csv', nrows=500)
df_id = pd.read_csv('data/raw/train_identity.csv', nrows=500)
df = pd.merge(df_trans, df_id, on='TransactionID', how='left')

# 2. 初始化一个空的“图”
G = nx.Graph()

# 3. 添加节点和边（核心逻辑）
# 规则：我们将“TransactionID（交易流水号）”作为核心节点
# 如果两笔交易使用了相同的 card1（银行卡号）或 P_emaildomain（邮箱后缀），我们就认为它们有关联，连一条边！
for index, row in df.iterrows():
    tx_id = row['TransactionID']
    is_fraud = row['isFraud']
    
    # 添加交易节点，并打上是否欺诈的标签 
    G.add_node(tx_id, type='transaction', fraud=is_fraud)

# 寻找共享特征并连线 (简单起见，这里演示共享银行卡 card1 的连线逻辑)
card_groups = df.groupby('card1')['TransactionID'].apply(list)
for card, tx_list in card_groups.items():
    if len(tx_list) > 1: # 如果同一张卡对应了多笔交易
        # 把这些交易两两相连，形成一个小团伙
        for i in range(len(tx_list)):
            for j in range(i+1, len(tx_list)):
                G.add_edge(tx_list[i], tx_list[j], relation='same_card')

print(f"✅ 图谱构建完成！共有 {G.number_of_nodes()} 个节点，{G.number_of_edges()} 条关系边。")

# 4. 可视化这张网（找出可能存在的“团伙”）
plt.figure(figsize=(10, 8))
# 欺诈节点标红色，正常节点标绿色
color_map = ['red' if G.nodes[node].get('fraud') == 1 else 'lightgreen' for node in G]

print("📊 正在渲染图谱，请查看弹出的图片窗口...")
nx.draw(G, node_color=color_map, with_labels=False, node_size=30, alpha=0.7)
plt.title("E-commerce Fraud Network (Red = Fraud, Green = Normal)")
plt.show()