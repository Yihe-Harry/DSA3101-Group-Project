import pandas as pd
import numpy as np

file_path = "bank_customer_segmentation.csv"  # Update with the correct file path
df = pd.read_csv(file_path)

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df = df.dropna()
df = df.drop_duplicates()

# Convert Categorical Columns to Appropriate Types
categorical_cols = ["gender", "occupation", "marital_status"]
for col in categorical_cols:
    df[col] = df[col].astype("category")

# Handle Outliers (Using IQR Method)
numeric_cols = df.select_dtypes(include=["number"]).columns
Q1 = df[numeric_cols].quantile(0.25)
Q3 = df[numeric_cols].quantile(0.75)
IQR = Q3 - Q1
df = df[np.logical_not(((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR))).any(axis=1))]

df.to_csv("cleaned_bank_customer_segmentation.csv", index=False)
print("Data cleaning completed. Cleaned file saved as 'cleaned_bank_customer_segmentation.csv'.")
