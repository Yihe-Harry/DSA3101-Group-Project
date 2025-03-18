import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import time

file_path = "cleaned_bank_customer_segmentation.csv"
df = pd.read_csv(file_path)

# Select numerical features for clustering (adjust as needed)
features = ["age", "income", "account_balance", "transaction_count"]  
df_selected = df[features]

# Normalize the data
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_selected)

# Train initial KMeans model
n_clusters = 4  
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
df["segment"] = kmeans.fit_predict(df_scaled)

# Simulate real-time customer data stream
def stream_new_data():
    """Simulates real-time new customer data arriving."""
    new_data = {
        "age": np.random.randint(18, 70),
        "income": np.random.uniform(20000, 150000),
        "account_balance": np.random.uniform(1000, 50000),
        "transaction_count": np.random.randint(1, 500),
    }
    return pd.DataFrame([new_data])

# Process new incoming data dynamically
def update_segmentation(kmeans, scaler):
    """Updates segmentation model in real-time as new data arrives."""
    while True:
        new_data = stream_new_data()
        new_data_scaled = scaler.transform(new_data)
        new_segment = kmeans.predict(new_data_scaled)[0]

        print(f"New customer data: {new_data.to_dict(orient='records')}")
        print(f"Assigned to Segment: {new_segment}")
        
        time.sleep(2)  # Simulate real-time delay

# Start real-time segmentation
update_segmentation(kmeans, scaler)
