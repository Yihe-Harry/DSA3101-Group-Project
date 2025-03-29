import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""## Transaction analysis"""

# Extract transaction history and compute mean withdrawals and deposits per cluster
def extract_transactions(transactions):
    withdrawals = [amount for days, type_, amount in transactions if type_ == "Withdrawal"]
    deposits = [amount for days, type_, amount in transactions if type_ == "Deposit"]
    return len(withdrawals), sum(withdrawals) / len(withdrawals) if withdrawals else 0, len(deposits), sum(deposits) / len(deposits) if deposits else 0

# Apply function to extract values
df_merged[['Num Withdrawals', 'Avg Withdrawal Amount', 'Num Deposits', 'Avg Deposit Amount']] = df_merged['Transaction history'].apply(lambda x: pd.Series(extract_transactions(x)))

# Group by Cluster
cluster_transactions = df_merged.groupby("Cluster").agg({
    "Num Withdrawals": "mean",
    "Avg Withdrawal Amount": "mean",
    "Num Deposits": "mean",
    "Avg Deposit Amount": "mean"
}).reset_index()

# Visualization: Mean Transactions per Cluster
fig, axes = plt.subplots(1, 2, figsize=(12,5))
sns.barplot(data=cluster_transactions, x="Cluster", y="Num Withdrawals", ax=axes[0], palette="Reds")
axes[0].set_title("Mean Number of Withdrawals per Cluster")
sns.barplot(data=cluster_transactions, x="Cluster", y="Num Deposits", ax=axes[1], palette="Blues")
axes[1].set_title("Mean Number of Deposits per Cluster")
plt.show()

# Visualization: Mean Transaction Amounts per Cluster
fig, axes = plt.subplots(1, 2, figsize=(12,5))
sns.barplot(data=cluster_transactions, x="Cluster", y="Avg Withdrawal Amount", ax=axes[0], palette="Reds")
axes[0].set_title("Mean Withdrawal Amount per Cluster")
sns.barplot(data=cluster_transactions, x="Cluster", y="Avg Deposit Amount", ax=axes[1], palette="Blues")
axes[1].set_title("Mean Deposit Amount per Cluster")
plt.show()
