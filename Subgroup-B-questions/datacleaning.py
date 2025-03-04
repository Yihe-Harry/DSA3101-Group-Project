import pandas as pd

# Read the CSV file
file_path = 'Subgroup-B-datasets/Edsel-data/marketing_campaign_dataset.csv'
df = pd.read_csv(file_path)

# Display the first few rows of the dataframe
print(df.head())

df = df.dropna()
df = df.drop_duplicates()
df = df.drop('Company', axis = 1) # Drop the 'Company' column

print(df.head())