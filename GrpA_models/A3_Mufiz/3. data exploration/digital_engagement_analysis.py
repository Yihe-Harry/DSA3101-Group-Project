import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""## Digital engagement analysis"""

# Extract CTR values from ad data
def extract_ctr(ad_data):
    return ad_data[2] if isinstance(ad_data, list) else None

df_merged["Facebook CTR"] = df_merged["Facebook ad [clicks, impressions, CTR(Click thru rate)]"].apply(extract_ctr)
df_merged["Twitter CTR"] = df_merged["Twitter ad [clicks, impressions, CTR(Click thru rate)]"].apply(extract_ctr)
df_merged["Instagram CTR"] = df_merged["Instagram ad [clicks, impressions, CTR(Click thru rate)]"].apply(extract_ctr)
df_merged["Total CTR"] = df_merged["Total ad [clicks, impressions, CTR(Click thru rate)]"].apply(extract_ctr)

# Compute mean CTR per cluster for those who bought vs. did not buy a product
cluster_ctr = df_merged.groupby(["Cluster", "has customer bought product"]).agg({
    "Facebook CTR": "mean",
    "Twitter CTR": "mean",
    "Instagram CTR": "mean",
    "Total CTR": "mean"
}).reset_index()

# Visualization: CTR per Cluster (Bought vs Not Bought)
fig, axes = plt.subplots(2, 2, figsize=(12,10))
sns.barplot(data=cluster_ctr, x="Cluster", y="Facebook CTR", hue="has customer bought product", ax=axes[0,0], palette="coolwarm")
axes[0,0].set_title("Facebook CTR per Cluster")
sns.barplot(data=cluster_ctr, x="Cluster", y="Twitter CTR", hue="has customer bought product", ax=axes[0,1], palette="coolwarm")
axes[0,1].set_title("Twitter CTR per Cluster")
sns.barplot(data=cluster_ctr, x="Cluster", y="Instagram CTR", hue="has customer bought product", ax=axes[1,0], palette="coolwarm")
axes[1,0].set_title("Instagram CTR per Cluster")
sns.barplot(data=cluster_ctr, x="Cluster", y="Total CTR", hue="has customer bought product", ax=axes[1,1], palette="coolwarm")
axes[1,1].set_title("Total CTR per Cluster")

plt.tight_layout()
plt.show()

"""Cluster 0 does not respond well to digital marketing strategies.

Cluster 1 and 2 shows that higher CTR will usually lead to a higher chance of buying a product for all digital engagement methods.

Cluster 3 shows that higher CTR will usually lead to a higher chance of buying a product for all digital engagement methods except Instagram

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Extract CTR and Impressions from ad data
def extract_ctr_impressions(ad_data):
    return pd.Series((ad_data[1], ad_data[2])) if isinstance(ad_data, list) else pd.Series((None, None))

df_merged[["Facebook Impressions", "Facebook CTR"]] = df_merged["Facebook ad [clicks, impressions, CTR(Click thru rate)]"].apply(extract_ctr_impressions)
df_merged[["Twitter Impressions", "Twitter CTR"]] = df_merged["Twitter ad [clicks, impressions, CTR(Click thru rate)]"].apply(extract_ctr_impressions)
df_merged[["Instagram Impressions", "Instagram CTR"]] = df_merged["Instagram ad [clicks, impressions, CTR(Click thru rate)]"].apply(extract_ctr_impressions)

# Convert to numeric values
df_merged["Facebook Impressions"] = pd.to_numeric(df_merged["Facebook Impressions"], errors='coerce')
df_merged["Facebook CTR"] = pd.to_numeric(df_merged["Facebook CTR"], errors='coerce')
df_merged["Twitter Impressions"] = pd.to_numeric(df_merged["Twitter Impressions"], errors='coerce')
df_merged["Twitter CTR"] = pd.to_numeric(df_merged["Twitter CTR"], errors='coerce')
df_merged["Instagram Impressions"] = pd.to_numeric(df_merged["Instagram Impressions"], errors='coerce')
df_merged["Instagram CTR"] = pd.to_numeric(df_merged["Instagram CTR"], errors='coerce')

# Plot CTR vs. Impressions for each cluster
clusters = df_merged["Cluster"].unique()
colors = sns.color_palette("tab10", n_colors=len(clusters))

for cluster, color in zip(clusters, colors):
    cluster_data = df_merged[df_merged["Cluster"] == cluster]
    plt.figure(figsize=(8,6))
    sns.lineplot(x=cluster_data["Facebook Impressions"], y=cluster_data["Facebook CTR"], label="Facebook", color="blue")
    sns.lineplot(x=cluster_data["Twitter Impressions"], y=cluster_data["Twitter CTR"], label="Twitter", color="red")
    sns.lineplot(x=cluster_data["Instagram Impressions"], y=cluster_data["Instagram CTR"], label="Instagram", color="green")
    plt.title(f"CTR vs. Impressions for Cluster {cluster}")
    plt.xlabel("Impressions")
    plt.ylabel("CTR")
    plt.legend()
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Extract CTR and Clicks from ad data
def extract_ctr_clicks(ad_data):
    return pd.Series((ad_data[0], ad_data[2])) if isinstance(ad_data, list) else pd.Series((None, None))

df_merged[["Facebook Clicks", "Facebook CTR"]] = df_merged["Facebook ad [clicks, impressions, CTR(Click thru rate)]"].apply(extract_ctr_clicks)
df_merged[["Twitter Clicks", "Twitter CTR"]] = df_merged["Twitter ad [clicks, impressions, CTR(Click thru rate)]"].apply(extract_ctr_clicks)
df_merged[["Instagram Clicks", "Instagram CTR"]] = df_merged["Instagram ad [clicks, impressions, CTR(Click thru rate)]"].apply(extract_ctr_clicks)

# Convert to numeric values
df_merged["Facebook Clicks"] = pd.to_numeric(df_merged["Facebook Clicks"], errors='coerce')
df_merged["Facebook CTR"] = pd.to_numeric(df_merged["Facebook CTR"], errors='coerce')
df_merged["Twitter Clicks"] = pd.to_numeric(df_merged["Twitter Clicks"], errors='coerce')
df_merged["Twitter CTR"] = pd.to_numeric(df_merged["Twitter CTR"], errors='coerce')
df_merged["Instagram Clicks"] = pd.to_numeric(df_merged["Instagram Clicks"], errors='coerce')
df_merged["Instagram CTR"] = pd.to_numeric(df_merged["Instagram CTR"], errors='coerce')

# Plot CTR vs. Clicks for each cluster
clusters = df_merged["Cluster"].unique()
colors = sns.color_palette("tab10", n_colors=len(clusters))

for cluster, color in zip(clusters, colors):
    cluster_data = df_merged[df_merged["Cluster"] == cluster]
    plt.figure(figsize=(8,6))
    sns.lineplot(x=cluster_data["Facebook Clicks"], y=cluster_data["Facebook CTR"], label="Facebook", color="blue")
    sns.lineplot(x=cluster_data["Twitter Clicks"], y=cluster_data["Twitter CTR"], label="Twitter", color="red")
    sns.lineplot(x=cluster_data["Instagram Clicks"], y=cluster_data["Instagram CTR"], label="Instagram", color="green")
    plt.title(f"CTR vs. Clicks for Cluster {cluster}")
    plt.xlabel("Clicks")
    plt.ylabel("CTR")
    plt.legend()
    plt.show()
