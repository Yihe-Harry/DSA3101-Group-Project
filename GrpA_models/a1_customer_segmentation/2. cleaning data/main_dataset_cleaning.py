#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Installing packages 

import pandas as pd 
import os 
from sklearn.preprocessing import StandardScaler

# Working Directory 
os.chdir("/Users/rachel/Desktop/DSA3101/dataset")


# In[2]:


# Loading dataset 
df = pd.read_csv("main dataset.csv",delimiter=",")
df.head()


# #### **Age Categories**
# ##### 20-29, 30-39, 40-49, 50-59, 60-69

# In[3]:


## Age into bins

# Define age bins and labels
bins = [20, 29, 39, 49, 59, 69]  # Bin edges
labels = ['20-29', '30-39', '40-49', '50-59', '60-69']  # Bin labels

# Ensure 'age' is numeric
df['age'] = df['age'].astype(int)

# Create a new column with age groups
df['age group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)

# Reorder columns to place 'age group' next to 'age'
cols = df.columns.tolist()
age_index = cols.index('age')
cols.insert(age_index + 1, cols.pop(cols.index('age group')))
df = df[cols]
df.head()


# #### **Z Score standardisation**
# ##### Standardisation applied to age, income/month, account balance, & loyalty score

# In[4]:


## Z score Standardization for numerical features (including 'age')

# Define columns to standardize
#num_cols = ['age', 'income/month', 'account balance', 'loyalty score']

# Apply Z-score standardization
#scaler = StandardScaler()
#df_scaled = df.copy()  # Keep a copy of the original data
#df_scaled[num_cols] = scaler.fit_transform(df[num_cols])

# Display the first few rows
#df_scaled.head()


# #### **Ordinal encoding**
# #### **Age Group** 
# ##### 0:20-29, 1:30-39, 2:40-49, 3:50-59, 4:60-69
# #### **Education level**
# ##### 0:Primary, 1:Secondary, 2:Tiertary, 3:Postgrad

# In[5]:


## Oridnal encoding for age group and education level (ordinal)

from pandas.api.types import CategoricalDtype

# Make a copy of the original dataset
df_encoded = df.copy()

# Define category order
age_order = ['20-29', '30-39', '40-49', '50-59', '60-69']
edu_order = ['Primary', 'Secondary', 'Tertiary', 'Postgrad']

# Convert to categorical with specified order
df_encoded['age group'] = df_encoded['age group'].astype(CategoricalDtype(categories=age_order, ordered=True))
df_encoded['education level'] = df_encoded['education level'].astype(CategoricalDtype(categories=edu_order, ordered=True))

# Convert to numerical encoding (Ordinal)
df_encoded['age group'] = df_encoded['age group'].cat.codes
df_encoded['education level'] = df_encoded['education level'].cat.codes

# Display first few rows to verify
df_encoded.head()


# #### **Job groupings**
# ##### Groupings were done based on income levels / spending habits
# ##### **White collar**: management, admin, services
# ##### **Blue collar**: technician, blue collar, housemaid
# ##### **Self employed / Entrepreneur**: self employed, entrepreneur 
# ##### **Student**: Student
# ##### **unemployed**: unemployed
# ##### **Retired** : Retired
# ##### **Unknown** : Unknown

# In[6]:


# Define job category mapping
job_mapping = {
    'management': 'white collar',  # Stable high-income jobs
    'technician': 'blue collar',
    'admin.': 'white collar',
    'services': 'white collar',
    'blue-collar': 'blue collar',
    'housemaid': 'blue collar',
    'self-employed': 'self employed/entrepreneur',  # Separate category
    'entrepreneur': 'self employed/entrepreneur',  # Separate category
    'retired': 'retired',
    'unemployed': 'unemployed',
    'student': 'student',
    'unknown': 'unknown'
}

# Apply job grouping
df_encoded['job grouped'] = df_encoded['job'].map(job_mapping)

# Reorder columns to place 'job_grouped' immediately after 'job'
cols = df_encoded.columns.tolist()
job_index = cols.index('job')  # Find index of 'job' column
cols.insert(job_index + 1, cols.pop(cols.index('job grouped')))  # Move 'job_grouped' right after 'job'
df_encoded = df_encoded[cols]

# Display grouped job categories
df_encoded['job grouped'].value_counts()


# In[7]:


df_encoded.head()


# In[8]:


# Define categorical columns to one-hot encode
categorical_cols = ['job grouped', 'marital']

# Apply one-hot encoding
df_encoded = pd.get_dummies(df_encoded, columns=categorical_cols, drop_first=True)

# Convert binary categorical columns to 0 and 1
binary_cols = ['housing', 'loan', 'prev campaign success', 'gender', 'has customer bought product', 'has customer churned']
mapping_dict = {'yes': 1, 'no': 0, 'Yes': 1, 'No': 0, 'Male': 1, 'Female': 0}

for col in binary_cols:
    if col in df_encoded.columns:
        df_encoded[col] = df_encoded[col].map(mapping_dict).fillna(0).astype(int)

# Ensure encoded columns appear before 'has customer bought product' and 'has customer churned'
cols = df_encoded.columns.tolist()
target_columns = ['has customer bought product', 'has customer churned']

# Find index of the first target column
target_index = min(cols.index(target_columns[0]), cols.index(target_columns[1]))

# Identify one-hot encoded columns related to job and marital status
one_hot_cols = [col for col in df_encoded.columns if col.startswith(('job grouped_', 'marital_'))]

# Move one-hot encoded columns before 'has customer bought product' and 'has customer churned'
for col in reversed(one_hot_cols):
    cols.insert(target_index, cols.pop(cols.index(col)))

# Reorder the DataFrame
df_encoded = df_encoded[cols]

# Convert one-hot encoded columns to 0/1 (instead of True/False)
df_encoded[one_hot_cols] = df_encoded[one_hot_cols].astype(int)

# Display first few rows to verify
df_encoded.head()


# In[9]:


import ast

### ✅ Processing "type of campaign(s)" (Multi-Category One-Hot Encoding)

# Ensure missing values are handled properly
df_encoded['type of campaign(s)'] = df_encoded['type of campaign(s)'].fillna("[]")

# Convert string lists to actual lists safely
def safe_eval(value):
    try:
        return ast.literal_eval(value) if isinstance(value, str) else value
    except (ValueError, SyntaxError):  # Handles invalid formats
        return []

df_encoded['type of campaign(s)'] = df_encoded['type of campaign(s)'].apply(safe_eval)

# Extract unique campaign types (use LIST instead of SET)
all_campaigns = ['Facebook', 'Twitter', 'Email', 'Instagram']  # ✅ Ordered list

# Create separate binary columns for each campaign type
for campaign in all_campaigns:
    df_encoded[campaign] = df_encoded['type of campaign(s)'].apply(lambda x: 1 if campaign in x else 0)

# Reorder columns: Place Facebook, Twitter, Email, and Instagram right after "type of campaign(s)"
cols = df_encoded.columns.tolist()

# Get the index of "type of campaign(s)"
campaign_index = cols.index("type of campaign(s)")

# Move campaign columns right after "type of campaign(s)"
for col in reversed(all_campaigns):  # ✅ Now works because it's a list
    cols.insert(campaign_index + 1, cols.pop(cols.index(col)))

# Reorder the DataFrame
df_encoded = df_encoded[cols]

# Display first few rows to verify
df_encoded[['type of campaign(s)','Facebook','Instagram', 'Twitter','Email']].head()


# ##### **Transaction History**
# ##### **total_deposits**: Total money deposited
# ##### **net_transaction**: Deposits - Withdrawals (savings vs. overspending)
# ##### **transaction_count**:	Number of transactions
# ##### **last_transaction_days**:	Days since last transaction (helps identify inactive users)

# In[10]:


import ast
import pandas as pd

### ✅ Processing "Transaction history" (Extracting Financial Features)
def process_transaction_history(transaction_history):
    # Ensure transaction history is correctly formatted
    if isinstance(transaction_history, str):
        transaction_history = ast.literal_eval(transaction_history)  # Convert string to list
    elif not isinstance(transaction_history, list):
        transaction_history = []

    # Extract financial features
    total_withdrawals = sum(amount for date, type_, amount in transaction_history if type_ == "Withdrawal")
    total_deposits = sum(amount for date, type_, amount in transaction_history if type_ == "Deposit")
    transaction_count = len(transaction_history)  # Ensure transaction count is an integer
    last_transaction_day = max([date for date, _, _ in transaction_history], default=None)  # Most recent transaction

    return pd.Series([
        round(total_withdrawals, 2),  # Ensure two decimal places for currency
        round(total_deposits, 2),
        round(total_deposits - total_withdrawals, 2),  # Net transaction
        int(transaction_count),  # Ensure transaction count is integer
        last_transaction_day  # Keep NaN for missing latest transaction days
    ])

# Apply function to transaction history column
df_encoded[['total_withdrawals', 'total_deposits', 'net_transaction', 
    'transaction_count', 'last_transaction_day']] = df_encoded['Transaction history'].apply(process_transaction_history)

# Convert transaction_count to integer
df_encoded['transaction_count'] = df_encoded['transaction_count'].astype(int)

# Convert latest_transaction_days to integer while keeping NaNs
if 'last_transaction_day' in df_encoded.columns:
    df_encoded['last_transaction_day'] = df_encoded['last_transaction_day'].dropna().astype(int)

# Reorder columns: Place new financial columns right after "Transaction history"
cols = df_encoded.columns.tolist()
transaction_index = cols.index("Transaction history")

# List of new financial feature columns
financial_cols = ['total_withdrawals', 'total_deposits', 'net_transaction', 'transaction_count', 'last_transaction_day']

# Move financial columns right after "Transaction history"
for col in reversed(financial_cols):  # Reverse to maintain order
    cols.insert(transaction_index + 1, cols.pop(cols.index(col)))

# Reorder the DataFrame
df_encoded = df_encoded[cols]

# Display first few rows to verify
df_encoded[['Transaction history', 'total_withdrawals', 'total_deposits', 'net_transaction', 
    'transaction_count', 'last_transaction_day']].head()


# In[11]:


df_encoded[['last_transaction_day']].isna().sum()


# In[12]:


df_encoded = df_encoded.fillna("")  # Replace NaNs with empty strings


# In[13]:


df_encoded[['last_transaction_day']].isna().sum()


# In[14]:


# Save the dataset as "transformed main dataset.csv"
df_encoded.to_csv("cleaned main dataset.csv", index=False)


# In[ ]:




