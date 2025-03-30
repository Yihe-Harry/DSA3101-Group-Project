from fastapi import FastAPI
from pydantic import BaseModel
from k_means_code import df, df_cluster, df_cluster2, cluster_names, kmeans2, scaler, cluster_strategy,less_cluster_features,KMeans,pd
import numpy as np
from typing import Optional
app = FastAPI()




#Re-add the customer id column as it was removed during clustering
df_cluster["customer id"] = df["customer id"]
df_cluster2["customer id"] = df["customer id"]

class fetchcluster_input(BaseModel):
    customer_id: int
class predictcluster_input(BaseModel):
    age:int
    gender:int
    monthly_income:int
    account_balance:int
    loyalty_score:int
    education_level:int
    facebook_interaction:int
    twitter_interaction:int
    email_interaction:int
    instagram_interaction:int
    total_withdrawal_amount:int
    total_deposit_amount:int
    transaction_count:int
    has_loan:int

class updatecustomer_input(BaseModel):
    customer_id: int
    age: Optional[int] = None
    gender: Optional[int] = None
    monthly_income: Optional[int] = None
    account_balance: Optional[int] = None
    loyalty_score: Optional[int] = None
    education_level: Optional[int] = None
    facebook_interaction: Optional[int] = None
    twitter_interaction: Optional[int] = None
    email_interaction: Optional[int] = None
    instagram_interaction: Optional[int] = None
    total_withdrawal_amount: Optional[int] = None
    total_deposit_amount: Optional[int] = None
    transaction_count: Optional[int] = None
    has_loan: Optional[int] = None


# --- 1. Precomputed cluster lookup from DataFrame ---
@app.post("/Get segment that customer belong to, from database")
def get_customer_segment(customer_id: int):

    customer_index=df_cluster2[df_cluster2["customer id"] == customer_id].index
    if customer_index.empty:
        return {"error": f"Customer id {customer_id} is not a valid customer id"}
    customer_details = df_cluster2[df_cluster2["customer id"] == customer_id].to_dict()
    cluster_num = df_cluster2.at[customer_index[0], "cluster_num"]
    cluster_name=cluster_names[cluster_num]
    business_strategy=cluster_strategy[cluster_name]
    return {f'Cluster {cluster_num}: {cluster_name} , Business strategy: {business_strategy}'}



# --- 1.1 Get customer details
@app.post("/Get customer details from database")
def get_customer_info(customer_id: int):
    if customer_id not in df_cluster2["customer id"].values:
        return "Invalid customer ID"
    return df_cluster2[df_cluster2["customer id"] == customer_id].iloc[0].to_dict()

# ---2. Update customer details in Dataframe ---
@app.post("/Update customer details")
def update_customer(update_data: updatecustomer_input):
    global df_cluster2

    # Find the customer by ID
    customer_index = df_cluster2[df_cluster2["customer id"] == update_data.customer_id].index
    if customer_index.empty:
        return(f"Customer with ID {update_data.customer_id} not found")

    # Iterate over fields, skip None, update only provided values
    customer_index = customer_index[0]
    def replace_entry(df,input,col_name,cust_index):
        if input is not None:
            df.at[cust_index,col_name]=input

    replace_entry(df_cluster2,update_data.age,"age",customer_index)
    replace_entry(df_cluster2, update_data.gender, "gender", customer_index)
    replace_entry(df_cluster2, update_data.monthly_income, "income/month", customer_index)
    replace_entry(df_cluster2, update_data.account_balance,"account balance" , customer_index)
    replace_entry(df_cluster2, update_data.loyalty_score, "loyalty score", customer_index)
    replace_entry(df_cluster2, update_data.education_level, "education level", customer_index)
    replace_entry(df_cluster2, update_data.facebook_interaction, "Facebook", customer_index)
    replace_entry(df_cluster2, update_data.twitter_interaction, "Twitter", customer_index)
    replace_entry(df_cluster2, update_data.email_interaction, "Email", customer_index)
    replace_entry(df_cluster2, update_data.instagram_interaction, "Instagram", customer_index)
    replace_entry(df_cluster2, update_data.total_withdrawal_amount, "total_withdrawals", customer_index)
    replace_entry(df_cluster2, update_data.total_deposit_amount, "total_deposits", customer_index)
    replace_entry(df_cluster2, update_data.transaction_count, "transaction_count", customer_index)
    replace_entry(df_cluster2, update_data.has_loan, "loan", customer_index)

    return {
        "message": f'Customer id {update_data.customer_id} updated successfully',
        "updated_customer": df_cluster2[df_cluster2["customer id"] == update_data.customer_id].iloc[0].to_dict()
    }

# ---3. Delete customer in Dataframe ---
@app.post("/Delete customer from database")
def delete_customer(customer_id: int):
    global df_cluster2

    # Check if the customer exists
    if customer_id not in df_cluster2['customer id'].values:
        return {"message": f"Customer with customer ID {customer_id} not found"}

    # Drop the row where customer_id matches
    df_cluster2 = df_cluster2[df_cluster2['customer id'] != customer_id]

    return {"message": f"Customer with ID {customer_id} deleted successfully"}


# ---4. Add customer to Dataframe ---
@app.post("/Add customer to database")
def add_customer(data:updatecustomer_input):
    global df_cluster2
    if data.customer_id in df_cluster2['customer id'].values:
        return {"message": "Customer ID already in databank, choose a different ID"}
    features = [
        data.age,
        data.gender,
        data.monthly_income,
        data.account_balance,
        data.loyalty_score,
        data.education_level,
        data.facebook_interaction,
        data.twitter_interaction,
        data.email_interaction,
        data.instagram_interaction,
        data.total_withdrawal_amount,
        data.total_deposit_amount,
        data.transaction_count,
        data.has_loan
    ]
    scaled_input = scaler.transform([features])
    cluster_num = kmeans2.predict(scaled_input)[0]
    features.append(cluster_num)
    features.append(data.customer_id)
    df_cluster2.loc[len(df_cluster2)]=features
    return {"message": "Customer successfully added to databank"}



# --- 5. Predict cluster for new input (Real-time segmentation) ---
@app.post("/Customer segmentation in real time")
def predict_customer_segment(data:predictcluster_input):
    features = [
        data.age,
        data.gender,
        data.monthly_income,
        data.account_balance,
        data.loyalty_score,
        data.education_level,
        data.facebook_interaction,
        data.twitter_interaction,
        data.email_interaction,
        data.instagram_interaction,
        data.total_withdrawal_amount,
        data.total_deposit_amount,
        data.transaction_count,
        data.has_loan
    ]
    scaled_input = scaler.transform([features])
    cluster_num = kmeans2.predict(scaled_input)[0]
    cluster_name = cluster_names[cluster_num]
    business_strategy = cluster_strategy[cluster_name]
    return f'Cluster {cluster_num}: {cluster_name} , Business strategy: {business_strategy}'

# --- 6. Dynamic retraining of K-means segmentation model
@app.post("/Updates segmentation model with the latest data")
def retrain_model():
    global df_cluster2

    df_temp=df_cluster2[less_cluster_features].dropna()
    x2_scaled = scaler.fit_transform(df_temp)
    kmeans2 = KMeans(n_clusters=4, random_state=42)
    clusters2 = kmeans2.fit_predict(x2_scaled)
    df_temp["cluster_num"] = clusters2
    df_temp["customer id"] = df_cluster2["customer id"]
    df_cluster2=df_temp

    return "Model successfully updated"



