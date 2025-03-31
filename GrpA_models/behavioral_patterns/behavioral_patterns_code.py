

import pandas as pd
import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from final_segmentation_model import kmeans, clusters

df=pd.read_csv("generated_bank_data.csv")
num_customers=len(df)


# Cluster and their behavioral characteristics
'''
Cluster 0: frequent users, high income, medium loyalty, very budget conscious

Cluster 1: Occasional users, low income, low-medium loyalty, not budget conscious

Cluster 2: Semi-frequent users, medium income, medium-high loyalty, not budget conscious

Cluster 3: Semi-frequent users, medium income, low loyalty, semi- budget conscious.
'''


df["cluster"]=clusters

# Creating CTR for each of the individual campaigns
df["fb_ctr"]=df["fb clicks"]/df["fb impressions"]
df["insta_ctr"]=df["insta clicks"]/df["insta impressions"]
df["tw_ctr"]=df["tw clicks"]/df["tw impressions"]

fig3, axs3 = plt.subplots(2, 2, figsize=(18, 10))

ctr_overall = df.groupby('cluster')['CTR'].mean()
ctr_fb = df.groupby('cluster')['fb_ctr'].mean()
ctr_insta = df.groupby('cluster')['insta_ctr'].mean()
ctr_tw = df.groupby('cluster')['tw_ctr'].mean()

ctr_overall.plot(kind='bar', ax=axs3[0, 0], color='tab:blue')
axs3[0, 0].set_title("Overall CTR by Cluster")
axs3[0, 0].set_xlabel("Cluster")
axs3[0, 0].set_ylabel("Overall CTR")

ctr_fb.plot(kind='bar', ax=axs3[1, 0], color='tab:green')
axs3[1, 0].set_title("Facebook CTR by Cluster")
axs3[1, 0].set_xlabel("Cluster")
axs3[1, 0].set_ylabel("Facebook CTR")

ctr_insta.plot(kind='bar', ax=axs3[0, 1], color='tab:orange')
axs3[0, 1].set_title("Instagram CTR by Cluster")
axs3[0, 1].set_xlabel("Cluster")
axs3[0, 1].set_ylabel("Instagram CTR")

ctr_tw.plot(kind='bar', ax=axs3[1, 1], color='tab:purple')
axs3[1, 1].set_title("Twitter CTR by Cluster")
axs3[1, 1].set_xlabel("Cluster")
axs3[1, 1].set_ylabel("Twitter CTR")


# 2. Product usage

fig, axs = plt.subplots(1, 3, figsize=(18, 5))
proportion_1s_loan = df.groupby('cluster')['has_loan'].mean()
proportion_1s_creditcard = df.groupby('cluster')['has customer bought product'].mean()
proportion_1s_internet = df.groupby('cluster')['uses internet banking'].mean()

proportion_1s_loan.plot(kind='bar', ax=axs[0], color='tab:blue')
axs[0].set_title("Housing Loan ownership by Cluster")
axs[0].set_ylabel("Proportion")
axs[0].set_xlabel("Cluster")

proportion_1s_creditcard.plot(kind='bar', ax=axs[1], color='tab:green')
axs[1].set_title("Credit card purchase by cluster")
axs[1].set_ylabel("Proportion")
axs[1].set_xlabel("Cluster")

proportion_1s_internet.plot(kind='bar', ax=axs[2], color='tab:orange')
axs[2].set_title("Internet Banking by Cluster")
axs[2].set_xlabel("Cluster")
axs[2].set_ylabel("Proportion")



# 3. Transaction data/history

fig2, axs2 = plt.subplots(1, 3, figsize=(18, 5))

sns.boxplot(data=df, x='cluster', y='transaction_count', ax=axs2[0])
axs2[0].set_title('Transaction count by Cluster')

sns.boxplot(data=df, x='cluster', y='total_withdrawals', ax=axs2[1])
axs2[1].set_title('Withdrawal amount by Cluster')

sns.boxplot(data=df, x='cluster', y='total_deposits', ax=axs2[2])
axs2[2].set_title('Deposit amount by Cluster')

plt.tight_layout()
plt.show()

