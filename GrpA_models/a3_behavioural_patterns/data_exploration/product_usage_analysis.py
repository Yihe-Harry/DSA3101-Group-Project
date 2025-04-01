import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


"""## Prouct usage analysis"""

# Compute mean number of products per cluster for those who bought vs. did not buy a product
df_merged["Num Products"] = df_merged["products owned"].apply(lambda x: len(x))
cluster_products = df_merged.groupby(["Cluster", "has customer bought product"]).agg({
    "Num Products": "mean"
}).reset_index()

# Visualization: Mean Number of Products Owned (Bought vs. Not Bought)
plt.figure(figsize=(10,5))
sns.barplot(data=cluster_products, x="Cluster", y="Num Products", hue="has customer bought product", palette="coolwarm")
plt.title("Mean Number of Products Owned per Cluster (Bought vs. Not Bought)")
plt.xlabel("Cluster")
plt.ylabel("Mean Number of Products")
plt.legend(title="Bought Product")
plt.show()
