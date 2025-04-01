# Importing necessary tools
from itertools import count
from faker import Faker
from faker.providers import DynamicProvider
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
import ace_tools_open as tools
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler

# Generating fake data using Faker library first
# Note that some of the data in certain columns will be adjusted to match real life data in the later parts

# From here on out, we will use Gaussian noise to introduce randomness to out dataset.4
# This is because this technique aids in preventing overfitting and improves the generalization capabilities of models.
# It also enhances the robustness of machine learning models by simulating real-world distortions
# https://medium.com/%40amit25173/what-is-gaussian-noise-and-why-its-useful-b3c50dd14628
age = DynamicProvider(
    provider_name="age",
    elements=[i for i in range(21, 70)],
)
gender = DynamicProvider(
    provider_name="gender",
    elements=["Male", "Female"],
)
income = DynamicProvider(
    provider_name="income",
    elements=[i for i in range(3000, 15000)],

)

campaign_type = DynamicProvider(
    provider_name="campaign_type",
    elements=["Facebook", "Instagram", "X"],
)


def random_campaign_types():
    x = random.sample(["Facebook", "Instagram", "Twitter"], random.randint(1, 3))
    num = random.randint(0, 1)
    if num == 1:
        x.append("Email")
    return x


def random_products():
    x = random.sample(["W", "X", "Y", "Z"], random.randint(0, 4))
    return x


duration = DynamicProvider(
    provider_name="duration",
    elements=[15, 30, 45, 60],
)
product_type = DynamicProvider(
    provider_name="product_type",
    elements=["A", "B", "C", "D", "E"],
)
prev_campaign = DynamicProvider(
    provider_name="prev_campaign",
    elements=["Yes", "No"],
)
outcome = DynamicProvider(
    provider_name="outcome",
    elements=["Yes", "No"],
)
views = DynamicProvider(
    provider_name="views",
    elements=[i for i in range(1, 10)],
)


def fake_loyalty(a, b):
    return random.randint(a, b)


def fake_balance(a, b):
    return random.randint(a, b)


def fake_adspend(a, b):
    return random.uniform(a, b)


product_cost = {"A": 100, "B": 200, "C": 300, "D": 400, "E": 500}
marketing_cost = {"Facebook": 10000, "X": 18000, "Instagram": 20000}
fake = Faker()
lst = [["customer id", "age", "gender", "income/month", "account balance", "loyalty score", "education level",
        "products owned", "type of campaign(s)", "duration of campaign(s) (days)", "total ad spend",
        "product type advertised"
           , "prev campaign success", "product cost", "has customer bought product"], ]
# then add new providers to faker instance
fake.add_provider(age)
fake.add_provider(gender)
fake.add_provider(income)
fake.add_provider(campaign_type)
fake.add_provider(duration)
fake.add_provider(product_type)
fake.add_provider(prev_campaign)
fake.add_provider(outcome)
fake.add_provider(views)
num_customers = 20000
for i in range(num_customers):
    # The below educational qualification distribution is reflective of the real world
    # https: // educationdata.org / education - attainment - statistics
    education = np.random.choice(['high school', 'bachelor', 'master', 'phd'], size=1, p=[0.444, 0.424, 0.099, 0.033])[
        0]
    l = [i + 1, fake.age(), fake.gender(), fake.income(), fake_balance(100, 10000), fake_loyalty(0, 1000), education,
         random_products(), random_campaign_types(), 15, fake_adspend(200, 900)
        , fake.product_type(), fake.prev_campaign()]
    prod_cost = product_cost[l[-2]]
    l.append(prod_cost)
    l.append(fake.outcome())
    lst.append(l)

df = pd.DataFrame(lst[1:], columns=lst[0])


def tuning(row):
    base = 2000
    income, age = row["income/month"], row["age"]

    age_factor = 100
    noise = np.random.normal(0, 500)

    # income generally increases with age, due to work promotions etc.
    new_income = max(round(base + (age - 18) * age_factor + noise, 2), 0)
    row["income/month"] = new_income
    income_balance_factor = 12

    # bank balance increases by $500 for each year of age, as income increases generally result in greater account balances
    age_balance_factor = 500
    random_balance_noise = np.random.normal(0, 5000)  # random noise for variability
    row["account balance"] = round(
        (new_income * income_balance_factor) + (age * age_balance_factor) + random_balance_noise, 2)
    return row


df = df.apply(tuning, axis=1)

## Age into bins

# Define age bins and labels
bins = [20, 29, 39, 49, 59, 69]  # Bin edges
labels = ['20-29', '30-39', '40-49', '50-59', '60-69']  # Bin labels

# Ensure 'age' is numeric
df['age'] = df['age'].astype(float)

# Create a new column with age groups
df['age group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)

# Reorder columns to place 'age group' next to 'age'
cols = df.columns.tolist()
age_index = cols.index('age')
cols.insert(age_index + 1, cols.pop(cols.index('age group')))
df = df[cols]

num_cols = ['age', 'income/month', 'account balance', 'loyalty score']
# Apply minmax normalisation
scaler = MinMaxScaler()
df_scaled = df.copy()  # Keep a copy of the original data
df_scaled[num_cols] = scaler.fit_transform(df[num_cols])
df = df_scaled

# Ordinal mapping and normalisation of the education column
education_dict = {"high school": 1, "bachelor": 2, "master": 3, "phd": 4}


def normalise_edu(row):
    edu_level = row["education level"]
    row["education level"] = (education_dict[edu_level] - 1) / 3
    return row


df = df.apply(normalise_edu, axis=1)


# Tuning of outcomes start here
# 1. Buy product relative to income

# The higher the income, more likely to buy product (eg credit card)
# This is because credit cards are considered high risk, high reward
# https://www.helcim.com/guides/credit-card-statistics-and-trends/#:~:text=People%20with%20higher%20incomes%20are%20more%20likely%20to,with%20lower%20incomes%20don%27t%20use%20them%20as%20frequently.

# Average conversion rate around 3%
# https://www.ruleranalytics.com/blog/insight/conversion-rate-by-industry/

def tune_income_with_outcome(row):
    income = row["income/month"]
    age = row["age"]

    # the below equation reflects the increase in credit card acquisition probability as income and age increases
    # the 0.07 factor is used to maintain the overall conversion rate of around 3%
    prob = (0.6 * income + 0.4 * age) * 0.07
    outcome = np.random.choice(["Yes", "No"], p=[prob, 1 - prob])
    row["has customer bought product"] = outcome
    return row


df = df.apply(tune_income_with_outcome, axis=1)

# 2. engagement decrease with age

# Initialise the columns
df["fb impressions"] = None
df["fb clicks"] = None
df["insta impressions"] = None
df["insta clicks"] = None
df["tw impressions"] = None
df["tw clicks"] = None


# the higher the age, the lower the social media usage
# https://www.pewresearch.org/internet/2021/04/07/social-media-use-in-2021/

def tune_engagement(row):
    age = row["age"]

    # Here, max_impressions decrease as age increases, reflecting the above fact
    max_impressions = max((1 - age * 0.9) * 200, 0)
    min_impressions = int(0.5 * max_impressions)
    fb_impressions = np.random.randint(min_impressions, max_impressions)
    tw_impressions = np.random.randint(min_impressions, max_impressions)
    insta_impressions = np.random.randint(min_impressions, max_impressions)

    # Here, proportion of clicks relative to impressions also decrease with age, reflecting lower engagement in the older generation
    fb_clicks = int(round(np.random.uniform(0, 0.3) * (1 - age * 0.9) * fb_impressions, 0))
    tw_clicks = int(round(np.random.uniform(0, 0.3) * (1 - age * 0.9) * tw_impressions, 0))
    insta_clicks = int(round(np.random.uniform(0, 0.3) * (1 - age * 0.9) * insta_impressions, 0))

    row["fb impressions"] = fb_impressions
    row["fb clicks"] = fb_clicks
    row["insta impressions"] = insta_impressions
    row["insta clicks"] = insta_clicks
    row["tw impressions"] = tw_impressions
    row["tw clicks"] = tw_clicks
    return row


df = df.apply(tune_engagement, axis=1)

# Calculating the CTR engagement metric
df["total clicks"] = df["fb clicks"] + df["tw clicks"] + df["insta clicks"]
df["total impressions"] = df["fb impressions"] + df["insta impressions"] + df["tw impressions"]
df["CTR"] = round(df["total clicks"] / df["total impressions"], 3)

# 3. Internet banking, housing loans

# Individuals with higher education often possess greater familiarity with technology, making them more comfortable with online banking platforms.
# https://www.techscience.com/cmc/v72n3/47525/html

# Higher-income households are more likely to accumulate assets, providing collateral that facilitates mortgage approval.
# https://jefjournal.org.za/index.php/jef/article/view/452/853

# Advanced education also typically leads to increased income

df["uses internet banking"] = None
df["has housing loan"] = None


def tune_products(row):
    edu_level, income = row["education level"], row["income/month"]

    # This equation below showcases that increases in income and education level increases the chances of owning housing loans
    housing_chance = np.random.uniform(0, 0.3 * edu_level + 0.7 * income)
    row["has housing loan"] = np.random.choice([1, 0], p=[housing_chance, 1 - housing_chance])

    internet_banking_chance = edu_level
    row["uses internet banking"] = np.random.choice([1, 0], p=[internet_banking_chance, 1 - internet_banking_chance])
    return row


df = df.apply(tune_products, axis=1)

# Convert the outcome columns and gender column into one-hot representations
gender_dict = {"Male": 0, "Female": 1}
yes_dict = {"Yes": 1, "No": 0}
df_DT = df[["age", "gender", "income/month", "account balance", "loyalty score", "education level",
            "has customer bought product"]]


def convert_DT(row):
    row["gender"] = gender_dict[row["gender"]]
    row["has customer bought product"] = yes_dict[row["has customer bought product"]]
    return row


df_DT2 = df_DT.apply(convert_DT, axis=1)
df = df.apply(convert_DT, axis=1)

# 4. Transaction amount and frequency
# Higher income leads to higher transaction amount in general, due to larger disposable income and higher propensity to purchase expensive items
# Younger customers tend to transact more frequently, due to the popularity of digital banking services among the younger generation
# Younger customers also tend to transact smaller amounts of money on average, due to smaller cash flow


avg_transact_amt = 200
avg_transact_freq = 15

# This equation below shows that higher income leads to higher transaction amount
# Also shows that frequency of transactions decrease as age increases
df["total_withdrawals"] =  round((df["income/month"] * avg_transact_amt)  * ((1-df["age"])* avg_transact_freq),2) + np.random.normal(0, 100,size=num_customers)
df["total_deposits"] =  round((df["income/month"] * avg_transact_amt)  * ((1-df["age"])* avg_transact_freq),2) + np.random.normal(0, 100,num_customers)

df["total_withdrawals"]= df["total_withdrawals"].apply(lambda x:max(x,0))
df["total_deposits"]=df["total_deposits"].apply(lambda x:max(x,0))

def transaction_count(row):
    if row["total_withdrawals"]==0 and row["total_deposits"]==0:
        row["transaction_count"]=0
    else:
        row["transaction_count"] = int(max(round(15 * row["age"], 0),2))

    return row
df=df.apply(transaction_count,axis=1)

# The Facebook, Twitter, Instagram, Email columns = 1 when the customer click the ad at least once, 0 otherwise
df["Facebook"]=df["fb clicks"].apply(lambda x:min(1,x))
df["Twitter"]=df["tw clicks"].apply(lambda x:min(1,x))
df["Instagram"]=df["insta clicks"].apply(lambda x:min(1,x))
df["Email"]=np.random.choice([0,1],size=num_customers)

df.rename(columns={"has housing loan":"has_loan"}, inplace=True)


# 5. Loyalty tuning
# Loyalty is shaped by income, and gender
# https://blog.accessdevelopment.com/three-of-the-most-influential-factors-when-it-comes-to-loyalty
# Here, we define loyalty to increase with income
df["loyalty score"]= 100 + df["income/month"] * 300 + np.random.normal(0,100,size=num_customers)

# Here we define loyalty score to differ by gender
df["loyalty score"]=df["loyalty score"] + df["gender"]  * 300

# Ensure loyalty score is >=0
df["loyalty score"]=df["loyalty score"].apply(lambda x:max(x,0))
#df.to_csv("generated_bank_data.csv")
