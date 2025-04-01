#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('pip', 'install faker')
get_ipython().run_line_magic('pip', 'install pandas')


# In[2]:


from faker import Faker
from faker.providers import DynamicProvider
import pandas as pd
import random
import numpy as np
age = DynamicProvider(
     provider_name="age",
     elements=[i for i in range(21,70)],
)
gender = DynamicProvider(
     provider_name="gender",
     elements=["Male","Female"],
)
income=DynamicProvider(
    provider_name="income",
    elements=[i for i in range(3000,15000)],

)
education = DynamicProvider(
     provider_name="education",
     elements=["Primary","Secondary","Tertiary","Postgrad"],
)
campaign_type= DynamicProvider(
    provider_name="campaign_type",
    elements=["Facebook","Instagram","X"],
)
def random_campaign_types():
    x= random.sample(["Facebook", "Instagram", "Twitter"], random.randint(1, 3))
    num=random.randint(0,1)
    if num ==1:
        x.append("Email")
    return x
def random_products():
    x = random.sample(["W","X","Y","Z"], random.randint(0, 4))
    return x
duration = DynamicProvider(
     provider_name="duration",
     elements=[15,30,45,60],
)
product_type= DynamicProvider(
    provider_name="product_type",
    elements=["A","B","C","D","E"],
)
prev_campaign=DynamicProvider(
    provider_name="prev_campaign",
    elements=["Yes","No"],
)
outcome=DynamicProvider(
    provider_name="outcome",
    elements=["Yes","No"],
)
views=DynamicProvider(
    provider_name="views",
    elements=[i for i in range(1,10)],
)

def fake_loyalty(a,b):
    return random.randint(a,b)
def fake_balance(a,b):
    return random.randint(a,b)
def fake_adspend(a,b):
    return random.uniform(a,b)

product_cost={"A":100,"B":200,"C":300,"D":400,"E":500}
marketing_cost={"Facebook":10000,"X":18000,"Instagram":20000}
fake = Faker()
lst=[["customer id","age","gender","income/month","account balance","loyalty score","education level","products owned","type of campaign(s)","duration of campaign(s) (days)","total ad spend","product type advertised"
      , "prev campaign success","product cost","has customer bought product"],]
# then add new provider to faker instance
fake.add_provider(age)
fake.add_provider(gender)
fake.add_provider(income)
fake.add_provider(education)
fake.add_provider(campaign_type)
fake.add_provider(duration)
fake.add_provider(product_type)
fake.add_provider(prev_campaign)
fake.add_provider(outcome)
fake.add_provider(views)

for i in range(20000):

    l=[i+1,fake.age(),fake.gender(),fake.income(),fake_balance(100,10000),fake_loyalty(0,1000),fake.education(),random_products(),random_campaign_types(),15,fake_adspend(200,900)
      , fake.product_type(),fake.prev_campaign()]
    prod_cost=product_cost[l[-2]]
    l.append(prod_cost)
    l.append(fake.outcome())
    lst.append(l)

df=pd.DataFrame(lst[1:],columns=lst[0])
df["Facebook ad [clicks, impressions, CTR(Click thru rate)]"]=None
df["Twitter ad [clicks, impressions, CTR(Click thru rate)]"]=None
df["Instagram ad [clicks, impressions, CTR(Click thru rate)]"]=None
df["Total ad [clicks, impressions, CTR(Click thru rate)]"]=None
df["Email [Opens,clicks]"]=None

def ad_generator(row):
    platforms=row["type of campaign(s)"]
    total_clicks=0
    total_impressions=0
    if "Twitter" in platforms:
        twitter_clicks=int(random.randint(1,4))
        total_clicks +=twitter_clicks

        twitter_impressions=random.randint(4* twitter_clicks, 20* twitter_clicks)
        total_impressions+=twitter_impressions

        twitter_ctr=round(twitter_clicks/twitter_impressions,5)
        row["Twitter ad [clicks, impressions, CTR(Click thru rate)]"]= [twitter_clicks,twitter_impressions,twitter_ctr]

    if "Facebook" in platforms:
        facebook_clicks=int(random.randint(1,4))
        total_clicks += facebook_clicks

        facebook_impressions=random.randint(4* facebook_clicks, 20* facebook_clicks)
        total_impressions+=facebook_impressions

        facebook_ctr=round(facebook_clicks/facebook_impressions,5)
        row["Facebook ad [clicks, impressions, CTR(Click thru rate)]"] = [facebook_clicks,facebook_impressions,facebook_ctr]

    if "Instagram" in platforms:
        instagram_clicks=int(random.randint(1,4))
        total_clicks+=instagram_clicks

        instagram_impressions=random.randint(4* instagram_clicks, 20* instagram_clicks)
        total_impressions+=instagram_impressions

        instagram_ctr=round(instagram_clicks/instagram_impressions,5)
        row["Instagram ad [clicks, impressions, CTR(Click thru rate)]"] = [instagram_clicks,instagram_impressions,instagram_ctr]

    if "Email" in platforms:
        email_opens=random.randint(1,9)
        email_clicks=random.randint(0,email_opens)
        row["Email [Opens,clicks]"]=[email_opens,email_clicks]


    avg_ctr=round(total_clicks/total_impressions,5)
    row["Total ad [clicks, impressions, CTR(Click thru rate)]"]=[total_clicks,total_impressions,avg_ctr]
    return row
df2=df.apply(ad_generator,axis=1)

def generate_transactions(row):
    k=random.randint(0,6)
    dates=sorted(list(random.sample(range(-60,-1),k)))
    l=[]
    for date in dates:
        transaction_type=str((np.random.choice(["Withdrawal","Deposit"],size=1))[0])
        if transaction_type=="Withdrawal":
            amt=round(random.uniform(10,5000),2)
        else:
            amt=round(random.uniform(100,10000),2)
        l.append([date,transaction_type,amt])
    row["Transaction history"]=l
    return row

df3=df2.apply(generate_transactions,axis=1)


df3["has customer bought product"]=df3.pop("has customer bought product")
df3["has customer churned"]=np.random.choice(["Yes","No"],size=len(df3))



# In[3]:


df3.columns


# # Customer attributes(for segmentation):
# - age
# - gender
# - income
# - account balance
# - education level
# 
# #Attributes for recommendation system
# - products already owned by customer
# - product advertised during campaign
# - transaction history
# -did customer buy advertised product (Yes/No)
# 
# #KPI for campaign success
# - Click through rate(CTR)
# - Conversion rate for each campaign(calculated in analysis below)
# - Custom ROI metrics (ad spend relative to product cost, CAC, etc.)
# 
# #Customer campaign engagement metrics
# - (Online channels) Facebook/twitter/instagram ad [clicks/impressions(total no. of ads shown)/CTR]
# - (Offline channel) Email [clicks/opens(no. of times customer opens link in email)]
# 
# #Customer churn metrics
# - Transaction history [date, transaction type, transaction amount] (only up to past 60 days)
# - loyalty score (based on amount of years in bank + transaction frequency)
# 
# #Labels
# - did customer buy advertised product
# - did customer churn
# 

# In[4]:


df3


# In[11]:


df3.to_csv("my_dataset.csv", index=False)  # Set index=True if you want to keep the index


# In[ ]:




