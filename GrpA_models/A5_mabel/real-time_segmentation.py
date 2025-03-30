### Segmentation Model from Subgroup A question 1

# Installing packages 

import pandas as pd 
import os 
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Loading dataset 
df = pd.read_csv("cleaned main dataset.csv",delimiter=",")
df.head()

# Select features for clustering
cluster_features = [
    'age', 'age group', 'gender', 'income/month', 'account balance',
    'loyalty score', 'education level', 'Facebook', 'Twitter', 'Email',
    'Instagram', 'prev campaign success', 'total_withdrawals',
    'total_deposits', 'net_transaction', 'transaction_count',
    'housing', 'loan', 'job grouped_retired', 'job grouped_self employed/entrepreneur',
    'job grouped_student', 'job grouped_unemployed', 'job grouped_unknown',
    'job grouped_white collar', 'marital_married', 'marital_single'
]

# Drop missing values
df_cluster = df[cluster_features].dropna()

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cluster)

# Run KMeans with k=4
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Add cluster labels and PCA components
df_cluster['Cluster'] = clusters
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df_cluster['PCA1'] = X_pca[:, 0]
df_cluster['PCA2'] = X_pca[:, 1]

# Save the final DataFrame as df_k4.csv
df_cluster.to_csv("df_k4.csv", index=False)

# Plot PCA clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cluster, x='PCA1', y='PCA2', hue='Cluster', palette='Set2')
plt.title('Customer Segmentation (k=4) with PCA')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster')
plt.tight_layout()
plt.show()

# Cluster profiling: mean values of features for each cluster
cluster_profile = df_cluster.groupby('Cluster').mean(numeric_only=True).round(2)

# Display the cluster profile
print("Cluster Profile (k=4):")
cluster_profile

#################################

### Subgroup A Question 5

# Select features for clustering
cluster_features = [
    'age', 'age group', 'gender', 'income/month', 'account balance',
    'loyalty score', 'education level', 'Facebook', 'Twitter', 'Email',
    'Instagram', 'prev campaign success', 'total_withdrawals',
    'total_deposits', 'net_transaction', 'transaction_count',
    'housing', 'loan', 'job grouped_retired', 'job grouped_self employed/entrepreneur',
    'job grouped_student', 'job grouped_unemployed', 'job grouped_unknown',
    'job grouped_white collar', 'marital_married', 'marital_single'
]

# Drop missing values
df_cleaned = df[cluster_features].dropna()

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cleaned)

# Run KMeans for the initial segmentation (Update 1)
kmeans = KMeans(n_clusters=4, random_state=42)
clusters_initial = kmeans.fit_predict(X_scaled)

# Add initial cluster labels to the DataFrame
df_cleaned['Cluster_Update_1'] = clusters_initial

# Define a fixed customer (eg. customer 33)
fixed_customer = [33]

# Filter for the customer and store their initial cluster assignment
df_fixed_customer = df_cleaned.loc[fixed_customer, ['age', 'income/month', 'loyalty score', 'account balance', 'transaction_count', 'Cluster_Update_1']]

print(df_fixed_customer)

## Simulating real-time updates

# Income raised from 3109-->5600, loyalty score: 788--> 850, account balance: 1418 --> 1700, tx: 2 --> 6 
df_cleaned.loc[33, ['income/month', 'loyalty score', 'account balance', 'transaction_count']] = [5600, 850, 1700, 6] 
## simulating a pay raise, increased transactions, withdrawal and deposits for cm33

# Re-standardize after the updates (exclude non-numeric columns such as 'Cluster_Update_1')
X_scaled_updated = scaler.transform(df_cleaned[cluster_features])

# Run KMeans again for the updated segmentation (Update 2)
clusters_updated = kmeans.fit_predict(X_scaled_updated)
df_cleaned['Cluster_Update_2'] = clusters_updated

# Get updated cluster assignments for the same customer
df_fixed_customer['Cluster_Update_2'] = df_cleaned.loc[fixed_customer, 'Cluster_Update_2']

# Show changes in cluster assignments
print("\nCluster Changes for Selected Customer:")
print(df_fixed_customer)

## Cluster changed from 1 to 0 (Value-Driven Frequent Users --> High-Value Power Users)

# Visualize changes
plt.figure(figsize=(6, 4))
sns.heatmap(df_fixed_customer[['Cluster_Update_1', 'Cluster_Update_2']], annot=True, cmap="coolwarm", fmt=".0f")
plt.title("Cluster Changes for Selected Customer")
plt.xlabel("Update")
plt.ylabel("Customer ID")
plt.show()
