#!/usr/bin/env python
# coding: utf-8

# Installing packages 

import pandas as pd 
import os 
from sklearn.preprocessing import StandardScaler

# Loading dataset 
df = pd.read_csv("main_dataset_cleaned.csv",delimiter=",")
df.head()

# ## **Customer Segmentation**
# ##### - **Demographics**: Age, gender, income, education, marital status, job type
# ##### - **Banking behavior**: Account balance, loyalty score, withdrawals, deposits, net transactions, transaction count
# ##### - **Marketing engagement**: Social media campaign interactions (Facebook, Twitter, Instagram, Email)
# ##### - **Customer outcomes**: Whether they bought a product, churned, or responded to past campaigns

# ## **K Means Clustering: Banking Behaviour**

# Re-import necessary libraries after environment reset
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

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

# Drop rows with missing values
df_cluster = df[cluster_features].dropna()

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cluster)

# Elbow Method to determine optimal number of clusters
inertia = []
cluster_range = range(1, 11)

for k in cluster_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

# Plot the Elbow Curve
plt.figure(figsize=(8, 5))
plt.plot(cluster_range, inertia, marker='o')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia (Within-cluster Sum of Squares)')
plt.xticks(cluster_range)
plt.grid(True)
plt.tight_layout()
plt.show()


# ### **K Means (K=4)**
# Based on graph, taking the best number of clusters to be 4 and profiling them 

# Re-import necessary libraries after code reset
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

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

# Re-import necessary libraries after code execution state reset
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

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

# Profile clusters
cluster_profile = df_cluster.groupby('Cluster').mean(numeric_only=True).round(2)

# Create cluster descriptions
descriptions = {}
for i, row in cluster_profile.iterrows():
    desc = []
    if row['income/month'] > df_cluster['income/month'].mean():
        desc.append("high income")
    else:
        desc.append("low to mid income")
    
    if row['account balance'] > df_cluster['account balance'].mean():
        desc.append("good account balance")
    else:
        desc.append("lower account balance")
    
    if row['loyalty score'] > df_cluster['loyalty score'].mean():
        desc.append("loyal customers")
    else:
        desc.append("low loyalty")
    
    if row['transaction_count'] > df_cluster['transaction_count'].mean():
        desc.append("frequent users")
    else:
        desc.append("less active users")
    
    descriptions[i] = ", ".join(desc)

# Plot visual breakdowns
key_features = ['income/month', 'account balance', 'loyalty score', 'transaction_count']

fig, axs = plt.subplots(2, 2, figsize=(14, 10))
axs = axs.flatten()

for i, feature in enumerate(key_features):
    sns.boxplot(data=df_cluster, x='Cluster', y=feature, hue='Cluster', ax=axs[i], palette='Set2', legend=False)
    axs[i].set_title(f'{feature} by Cluster')

plt.tight_layout()
plt.show()

descriptions


# Naming the clusters according to the descriptions
# - Cluster 0: High value power users
# - Cluster 1: Value driven frequent users
# - Cluster 2: Affluent inacitves
# - Cluster 3: Budget conscious occasionals


# Saving df_k4 dataset

# Add descriptions
df_cluster['Banking Behavior'] = df_cluster['Cluster'].map(descriptions)

# Add suggested customer type names
cluster_names = {
    0: "High-Value Power Users",
    1: "Value-Driven Frequent Users",
    2: "Affluent Inactives",
    3: "Budget-Conscious Occasionals"
}
df_cluster['Customer Type'] = df_cluster['Cluster'].map(cluster_names)

# Reorder columns: Cluster, Customer Type, Banking Behavior, PCA1, PCA2, then everything else
cols = ['Cluster', 'Customer Type', 'Banking Behavior', 'PCA1', 'PCA2'] + \
       [col for col in df_cluster.columns if col not in ['Cluster', 'Customer Type', 'Banking Behavior', 'PCA1', 'PCA2']]

df_k4 = df_cluster[cols]

# Save the final DataFrame as df_k4.csv
df_k4.to_csv("df_k4.csv", index=False)


# Saving clusters information K=4
profile_k4['Cluster'] = profile_k4.index

# Add Banking Behavior descriptions
profile_k4['Banking Behavior'] = profile_k4.index.map(descriptions_k4)

# Add Customer Type
cluster_names_k4 = {
    0: "High-Value Power Users",
    1: "Value-Driven Frequent Users",
    2: "Affluent Inactives",
    3: "Budget-Conscious Occasionals"
}
profile_k4['Customer Type'] = profile_k4.index.map(cluster_names_k4)

# Reorder columns - updated 'Num Customers (k=4)' to match your actual column name
ordered_cols = ['Cluster', 'Customer Type', 'Banking Behavior', 'Num Customers (k=4)'] + \
               [col for col in profile_k4.columns if col not in ['Cluster', 'Customer Type', 'Banking Behavior', 'Num Customers (k=4)']]

profile_k4 = profile_k4[ordered_cols]

# Save to CSV
profile_k4.to_csv("cluster_profile_k4.csv", index=False)


# ### **K Means (K=5)**
# If taking the number of clusters to be 5 and profiling them:

# Re-import necessary libraries after code reset
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

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

# Run KMeans with k=5
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Add cluster labels and PCA components
df_cluster['Cluster'] = clusters
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df_cluster['PCA1'] = X_pca[:, 0]
df_cluster['PCA2'] = X_pca[:, 1]

# Plot PCA clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cluster, x='PCA1', y='PCA2', hue='Cluster', palette='Set2')
plt.title('Customer Segmentation (k=5) with PCA')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster')
plt.tight_layout()
plt.show()

# Cluster profiling: mean values of features for each cluster
cluster_profile = df_cluster.groupby('Cluster').mean(numeric_only=True).round(2)

# Display the cluster profile
print("Cluster Profile (k=5):")
cluster_profile


# Re-import necessary libraries
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt

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

# Run KMeans with k=5
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Add cluster labels and PCA components
df_cluster['Cluster'] = clusters
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df_cluster['PCA1'] = X_pca[:, 0]
df_cluster['PCA2'] = X_pca[:, 1]

# Profile clusters
cluster_profile = df_cluster.groupby('Cluster').mean(numeric_only=True).round(2)

# Create cluster descriptions for k=5
descriptions_k5 = {}
for i, row in cluster_profile.iterrows():
    desc = []
    if row['income/month'] > df_cluster['income/month'].mean():
        desc.append("high income")
    else:
        desc.append("low to mid income")
    
    if row['account balance'] > df_cluster['account balance'].mean():
        desc.append("good account balance")
    else:
        desc.append("lower account balance")
    
    if row['loyalty score'] > df_cluster['loyalty score'].mean():
        desc.append("loyal customers")
    else:
        desc.append("low loyalty")
    
    if row['transaction_count'] > df_cluster['transaction_count'].mean():
        desc.append("frequent users")
    else:
        desc.append("less active users")
    
    descriptions_k5[i] = ", ".join(desc)

# Plot boxplots for 5-cluster version
key_features = ['income/month', 'account balance', 'loyalty score', 'transaction_count']
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
axs = axs.flatten()

for i, feature in enumerate(key_features):
    sns.boxplot(data=df_cluster, x='Cluster', y=feature, hue='Cluster', ax=axs[i], palette='Set2', legend=False)
    axs[i].set_title(f'{feature} by Cluster (k=5)')

plt.tight_layout()
plt.show()

descriptions_k5


# Naming the clusters according to the descriptions
# - Cluster 0: High value power users
# - Cluster 1: Value driven frequent users
# - Cluster 2: Affluent inacitves
# - Cluster 3: Budget conscious occasionals
# - Cluster 4: Cautious regulars


# Add Banking Behavior descriptions
df_cluster['Banking Behavior'] = df_cluster['Cluster'].map(descriptions_k5)

# Add suggested customer type names
cluster_names_k5 = {
    0: "High-Value Power Users",
    1: "Budget-Conscious Occasionals",
    2: "Value-Driven Frequent Users",
    3: "Affluent Inactives",
    4: "Cautious Regulars"
}
df_cluster['Customer Type'] = df_cluster['Cluster'].map(cluster_names_k5)

# Reorder columns
cols = ['Cluster', 'Customer Type', 'Banking Behavior', 'PCA1', 'PCA2'] + \
       [col for col in df_cluster.columns if col not in ['Cluster', 'Customer Type', 'Banking Behavior', 'PCA1', 'PCA2']]

df_k5 = df_cluster[cols]

# Save the final DataFrame as df_k5.csv
df_k5.to_csv("df_k5.csv", index=False)


# Saving cluster information k=5
income_avg = df_cluster['income/month'].mean()
balance_avg = df_cluster['account balance'].mean()
loyalty_avg = df_cluster['loyalty score'].mean()
txn_avg = df_cluster['transaction_count'].mean()

# Create descriptions for each cluster in profile_k5
descriptions_k5 = {}

for i, row in profile_k5.iterrows():
    desc = []
    if row['income/month (k=5)'] > income_avg:
        desc.append("high income")
    else:
        desc.append("low to mid income")
    
    if row['account balance (k=5)'] > balance_avg:
        desc.append("good account balance")
    else:
        desc.append("lower account balance")
    
    if row['loyalty score (k=5)'] > loyalty_avg:
        desc.append("loyal customers")
    else:
        desc.append("low loyalty")
    
    if row['transaction_count (k=5)'] > txn_avg:
        desc.append("frequent users")
    else:
        desc.append("less active users")
    
    descriptions_k5[i] = ", ".join(desc)

# Add the description and customer type columns
profile_k5['Banking Behavior'] = profile_k5.index.map(descriptions_k5)

cluster_names_k5 = {
    0: "High-Value Power Users",
    1: "Budget-Conscious Occasionals",
    2: "Value-Driven Frequent Users",
    3: "Affluent Inactives",
    4: "Cautious Regulars"
}
profile_k5['Customer Type'] = profile_k5.index.map(cluster_names_k5)

# Add Cluster column and reorder
profile_k5['Cluster'] = profile_k5.index

ordered_cols = ['Cluster', 'Customer Type', 'Banking Behavior', 'Num Customers (k=5)'] + \
               [col for col in profile_k5.columns if col not in ['Cluster', 'Customer Type', 'Banking Behavior', 'Num Customers (k=5)']]

profile_k5 = profile_k5[ordered_cols]

# Save to CSV
profile_k5.to_csv("cluster_profile_k5.csv", index=False)


# ### **Comparing K=4 vs K=5:**


# Re-import necessary libraries
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cluster)

# KMeans with k=4
kmeans_4 = KMeans(n_clusters=4, random_state=42)
clusters_4 = kmeans_4.fit_predict(X_scaled)
df_cluster['Cluster_4'] = clusters_4

# Profile for k=4
profile_k4 = df_cluster.groupby('Cluster_4')[['income/month', 'account balance', 'loyalty score', 'transaction_count']].mean().round(2)
profile_k4['Num Customers'] = df_cluster['Cluster_4'].value_counts().sort_index()
profile_k4.columns = [f"{col} (k=4)" for col in profile_k4.columns]

# KMeans with k=5
kmeans_5 = KMeans(n_clusters=5, random_state=42)
clusters_5 = kmeans_5.fit_predict(X_scaled)
df_cluster['Cluster_5'] = clusters_5

# Profile for k=5
profile_k5 = df_cluster.groupby('Cluster_5')[['income/month', 'account balance', 'loyalty score', 'transaction_count']].mean().round(2)
profile_k5['Num Customers'] = df_cluster['Cluster_5'].value_counts().sort_index()
profile_k5.columns = [f"{col} (k=5)" for col in profile_k5.columns]

# Combine both profiles
comparison_df = pd.concat([profile_k4, profile_k5], axis=1)

# Display updated comparison
print("Customer Segmentation Comparison (K=4 vs K=5):")
comparison_df


# ### **Calculating Silhouette Score**

from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Load your dataset
df = pd.read_csv("main_dataset_cleaned.csv")

# Select clustering features
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

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cluster)

# KMeans for k=4 and k=5
kmeans_4 = KMeans(n_clusters=4, random_state=42)
labels_4 = kmeans_4.fit_predict(X_scaled)
silhouette_k4 = silhouette_score(X_scaled, labels_4)

kmeans_5 = KMeans(n_clusters=5, random_state=42)
labels_5 = kmeans_5.fit_predict(X_scaled)
silhouette_k5 = silhouette_score(X_scaled, labels_5)

print(f"Silhouette Score for k=4: {silhouette_k4:.4f}")
print(f"Silhouette Score for k=5: {silhouette_k5:.4f}")


# **Customer Segmentation Analysis**: K=4 vs K=5 Clusters
# To uncover meaningful customer groups for targeted marketing, we applied K-Means clustering with k=4 and k=5 on a set of behavioral and financial features, including income, account balance, loyalty score, and transaction activity.
# 
# **K=4 Cluster Model**:
# The 4-cluster model produced distinct and well-separated segments. Each cluster showed clear differences in customer attributes:
# 
# One group represented high-income, loyal, and frequent users, likely high-value customers.
# Another comprised low-income, low-loyalty, and less active users, possibly disengaged or low-priority targets.
# The simplicity and clarity of this model make it effective for broad strategic targeting, especially for campaigns that require easily interpretable segment labels.
# 
# **K=5 Cluster Model**:
# The 5-cluster model offered finer granularity, particularly within the high-income segment:
# 
# The previous high-income group was split into two sub-segments: one with high loyalty and balance, and another with lower balance and more frequent activity. While this added detail could be valuable for hyper-targeted strategies (e.g., premium service upselling or churn prevention), one or two clusters showed overlapping profiles, suggesting potential redundancy.
