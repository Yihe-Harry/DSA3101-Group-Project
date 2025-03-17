from faker import Faker
from faker.providers import DynamicProvider
import pandas as pd
import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
age = DynamicProvider(
     provider_name="age",
     elements=[i for i in range(18,70)],
)
gender = DynamicProvider(
     provider_name="gender",
     elements=["Male","Female"],
)
income=DynamicProvider(
    provider_name="income",
    elements=[i for i in range(3000,15000)],

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
num_customers=20000





product_cost={"A":100,"B":200,"C":300,"D":400,"E":500}
marketing_cost={"Facebook":10000,"X":18000,"Instagram":20000}
fake = Faker()
lst=[["customer id","age","gender","income/month","account balance","loyalty score","education level","products owned","type of campaign(s)","duration of campaign(s) (days)","total ad spend","product type advertised"
      , "prev campaign success","product cost","has customer bought product"],]
# then add new provider to faker instance
fake.add_provider(age)
fake.add_provider(gender)
fake.add_provider(income)
fake.add_provider(campaign_type)
fake.add_provider(duration)
fake.add_provider(product_type)
fake.add_provider(prev_campaign)
fake.add_provider(outcome)
fake.add_provider(views)

for i in range(20000):
    education = np.random.choice(['high school', 'bachelor', 'master', 'phd'], size=1, p=[0.444, 0.424, 0.099, 0.033])[0]
    l=[i+1,fake.age(),fake.gender(),fake.income(),fake_balance(100,10000),fake_loyalty(0,1000),education,random_products(),random_campaign_types(),15,fake_adspend(200,900)
      , fake.product_type(),fake.prev_campaign()]
    prod_cost=product_cost[l[-2]]
    l.append(prod_cost)
    l.append(fake.outcome())
    lst.append(l)








df=pd.DataFrame(lst[1:],columns=lst[0])

def tuning(row):
    base=2000
    income,age=row["income/month"],row["age"]
    age_factor=100 #100$ income increase for every year
    noise=np.random.normal(0,500)
    new_income=max(round( base + (age-18) * age_factor + noise,2),0)
    row["income/month"]=new_income
    income_balance_factor=12
    age_balance_factor = 500  # bank balance increases by $500 for each year of age
    random_balance_noise = np.random.normal(0, 5000)  # random noise for variability
    row["account balance"]=round((new_income*income_balance_factor) + (age * age_balance_factor) + random_balance_noise,2)
    return row

df=df.apply(tuning,axis=1)

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


# Analysis starts here
facebook_df=df2[df2["type of campaign(s)"].apply(lambda x: "Facebook" in x)]
instagram_df=df2[df2["type of campaign(s)"].apply(lambda x: "Instagram" in x)]
twitter_df=df2[df2["type of campaign(s)"].apply(lambda x: "Twitter" in x)]

#calculations of conversion rates
facebook_conversion_rate= (facebook_df["has customer bought product"].value_counts().get("Yes",0))/len(facebook_df)
instagram_conversion_rate= (instagram_df["has customer bought product"].value_counts().get("Yes",0))/len(instagram_df)
twitter_conversion_rate= (twitter_df["has customer bought product"].value_counts().get("Yes",0))/len(twitter_df)

print(f'Facebook campaign conversion rate: {facebook_conversion_rate}')
print(f'Instagram campaign conversion rate: {instagram_conversion_rate}')
print(f'Twitter campaign conversion rate: {twitter_conversion_rate}')

# ROI calculations based off my custom ROI metric
#ROI for facebook campaign= (total number of facebook clicks/ total ad clicks on all platforms) * product price
facebook_converts=facebook_df[facebook_df["has customer bought product"]=="Yes"]
facebook_converts["ROI"]=None
def get_ROI(row):
    facebook_clicks,total_clicks=row["Facebook ad [clicks, impressions, CTR(Click thru rate)]"][0],row["Total ad [clicks, impressions, CTR(Click thru rate)]"][0]
    profit=row["product cost"]
    row["ROI"]= facebook_clicks/total_clicks * profit
    return row
facebook_converts=facebook_converts.apply(get_ROI,axis=1)
facebook_roi=facebook_converts["ROI"].sum() - marketing_cost["Facebook"]


#Decision tree
gender_dict={"Male":0,"Female":1}
education_dict={"high school":1,"bachelor":2,"master":3,"phd":4}
yes_dict={"Yes":1,"No":0}
df_DT=df3[["age","gender","income/month","account balance","loyalty score","education level","has customer bought product"]]
def convert_DT(row):
    row["gender"]=gender_dict[row["gender"]]
    row["education level"]=education_dict[row["education level"]]
    row["has customer bought product"]=yes_dict[row["has customer bought product"]]
    return row
df_DT2=df_DT.apply(convert_DT,axis=1)

X=df_DT2.drop(columns=["has customer bought product"])
y=df_DT2["has customer bought product"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Decision Tree
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Get Feature Importances
feature_importances = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)
y_pred = model.predict(X_test)

# Compute Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy:.2f}')




#df.to_csv("fakebank.csv")