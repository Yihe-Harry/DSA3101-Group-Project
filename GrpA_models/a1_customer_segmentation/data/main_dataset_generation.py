#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Installing packages 

import pandas as pd 
import os 

# Working Directory 
os.chdir("/Users/rachel/Desktop/DSA3101/dataset/UCI Bank Marketing/bank")


# In[3]:


# Loading dataset 
df = pd.read_csv("bank-full.csv",delimiter=";")
df.head()


# In[4]:


# Loading dataset 
os.chdir("../../")
df2 = pd.read_csv("eugene dataset.csv",delimiter= ",")
df2.head()


# In[5]:


# Add columns from df to df2
columns_to_add = ["housing", "loan", "marital", "job"]
for col in columns_to_add:
    df2[col] = df[col]

# Remove specified columns from df2
columns_to_remove = [
    "products owned", "duration of campaign(s) (days)", "total ad spend",
    "product type advertised", "product cost",
    "Facebook ad [clicks, impressions, CTR(Click thru rate)]",
    "Twitter ad [clicks, impressions, CTR(Click thru rate)]",
    "Instagram ad [clicks, impressions, CTR(Click thru rate)]",
    "Total ad [clicks, impressions, CTR(Click thru rate)]",
    "Email [Opens,clicks]"
]

df2_cleaned = df2.drop(columns=columns_to_remove, errors="ignore")  # Ignore errors if columns don't exist

# Ensure 'has customer bought product' and 'has customer churned' remain at the end
columns = [col for col in df2_cleaned.columns if col not in ["has customer bought product", "has customer churned"]]
columns += ["has customer bought product", "has customer churned"]  # Append these columns at the end

df2_cleaned = df2_cleaned[columns]  # Apply new column order

# Display the first few rows
df2_cleaned.head()


# In[6]:


# Save the cleaned dataset
df2_cleaned.to_csv("main dataset.csv", index=False)


# In[ ]:




