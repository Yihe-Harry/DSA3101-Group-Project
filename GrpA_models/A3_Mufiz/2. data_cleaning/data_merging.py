import pandas as pd

df_original = pd.read_csv("eugene dataset.csv")
df_segmented = pd.read_csv("df_k4.csv")


df_segmented['customer_id'] = df_segmented.index + 1 #adding back in the removed column of customer_id to merge
df_segmented = df_segmented[['customer_id'] + [col for col in df_segmented.columns if col != 'customer_id']] #reorder column for better visualisation
df_merged = df_original.join(df_segmented['Cluster'])
df_merged = df_merged.drop(['customer id', 'age', 'gender', 'education level', 'income/month', 'loyalty score'], axis=1)
df_merged.to_csv("df_merged.csv")
