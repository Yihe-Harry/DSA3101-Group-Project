import streamlit as st
import pandas as pd
import joblib
import os
import datetime
import xgboost as xgb
import models
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder




# setting the current working directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)


# business questions options
FUNCTIONS = {
    "Please select a function.": None, #Home page
    "Customer Clustering Dashboard": None, #Question A1
    "Customer Preference Prediction": "cus_pref_model.pkl", #Question B1
    "CTR-Based 'Real-Time' Campaign Optimizer": None, #Question B2
    "ROI Prediction": None, #Question B3
    
    "Customer Churn Prediction": {      #Question B5
        "Customer general data": "churn_model.pkl",
        "Customer credit card data": "churn_cc_model.pkl"
    }
}

######################### A1 stuff ################################
# API Base URL
API_BASE_URL = "http://127.0.0.1:5000"

# Set page configuration
st.set_page_config(
    page_title="Customer Clustering Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define cluster features
CLUSTER_FEATURES = [
    "age", "gender", "income/month", "account balance", "loyalty score", 
    "education level", "total_withdrawals", "total_deposits", 
    "transaction_count", "Facebook", "Twitter", "Email", "Instagram", "has_loan"
]

# Function to get cluster colors
def get_cluster_color(cluster_id):
    colors = {
        0: "#3498db",  # Blue
        1: "#2ecc71",  # Green
        2: "#e74c3c",  # Red
        3: "#f39c12",  # Orange
    }
    return colors.get(cluster_id, "#95a5a6")  # Default gray

# Function to get all customers
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_all_customers():
    try:
        response = requests.get(f"{API_BASE_URL}/api/customers")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['customers'])
            return df
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return pd.DataFrame()

# Function to get a specific customer
def get_customer(customer_id):
    try:
        response = requests.get(f"{API_BASE_URL}/api/customers/{customer_id}")
        if response.status_code == 200:
            return response.json()['customer']
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None

# Function to assign cluster to new customer
def assign_cluster(customer_data):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/assign_cluster", 
            json=customer_data
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None

# Function to update customer data
def update_customer(customer_id, updated_data):
    try:
        response = requests.put(
            f"{API_BASE_URL}/api/customers/{customer_id}", 
            json=updated_data
        )
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return False

# Function to add a new customer
def add_new_customer(customer_data):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/customers", 
            json=customer_data
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None
    

cluster_names = {0: "Comfort Seekers",
                 1: "Easy Explorers",
                 2: "Savvy Superusers",
                 3: "Wandering Spenders"}

cluster_strategy = {
                "Comfort Seekers": "Promote premium offerings like investment accounts or travel cards with moderate fees",
                "Easy Explorers": "Use visually engaging campaigns across social media platforms to grab attention",
                "Savvy Superusers": "Focus on no-fee and cashback products to appeal to budget awareness",
                "Wandering Spenders": "Use limited-time offers, sign up bonuses, or fun challenges to encourage repeat engagement"
            }

######################################################################


################## Functions for B5 ##################
def create_interaction_features(df):
    df['Age_Balance'] = df['Age'] * df['Balance']
    df['Age_NumOfProducts'] = df['Age'] * df['NumOfProducts']
    df['Age_IsActiveMember'] = df['Age'] * df['IsActiveMember']
    df['Balance_NumOfProducts'] = df['Balance'] * df['NumOfProducts']
    df['Balance_IsActiveMember'] = df['Balance'] * df['IsActiveMember']
    df['NumOfProducts_IsActiveMember'] = df['NumOfProducts'] * df['IsActiveMember']
    return df

def preprocess_credit_card_data():
    df = pd.read_excel('default of credit card clients.xls', header=1)
    
    # Replace -2 with 0 in pay columns
    df[['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']] = df[['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']].replace(-2, 0)
    
    # One-hot encoding
    df = pd.get_dummies(df, columns=['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6'], drop_first=True)
    
    # Define churn based on payment and usage patterns
    df['Sudden_Large_Payment'] = ((df['PAY_AMT1'] > df['BILL_AMT1'] * 0.9) | (df['PAY_AMT2'] > df['BILL_AMT2'] * 0.9)).astype(int)
    df['Decreasing_Usage'] = ((df['BILL_AMT2'] > df['BILL_AMT1']) & (df['BILL_AMT3'] > df['BILL_AMT2'])).astype(int)
    df['Churn'] = ((df[['BILL_AMT1', 'BILL_AMT2']].sum(axis=1) == 0) | (df['Decreasing_Usage'] == 1) | (df['Sudden_Large_Payment'] == 1)).astype(int)
    
    return df
###############################################################







# Title
st.title("🤖 Welcome to Group 13 AI banking system!")





# Step 1: Select Function
st.header("What would you like to do today?")
function_choice = st.selectbox("Choose a function:", list(FUNCTIONS.keys()))





# Step 2: Show models based on selected function
if function_choice:
    ######################## Question A1 #########################
    if function_choice == "Customer Clustering Dashboard":
        st.title("Customer Clustering Dashboard")
        st.markdown("---")

        # Create tabs
        tab1, tab2, tab3 = st.tabs([
            "📊 Cluster Information", 
            "🔍 Fetch Customer", 
            "🔮 Predict Cluster"
        ])

        # Tab 1: Cluster Information
        with tab1:
            st.header("Cluster Dashboard")
            
            # Get all customers data
            df = get_all_customers()
            
            if not df.empty:
                # Convert cluster to numeric if it exists
                if 'cluster' in df.columns:
                    df['cluster'] = pd.to_numeric(df['cluster'], errors='coerce')
                    
                    # Add cluster names to the dataframe
                    df['cluster_name'] = df['cluster'].map(cluster_names)
                    
                    st.subheader("Customer Distribution by Cluster")
                    
                    # Count customers by cluster
                    cluster_counts = df['cluster'].value_counts().reset_index()
                    cluster_counts.columns = ['Cluster', 'Count']
                    
                    # Add cluster names to the counts
                    cluster_counts['Cluster_Name'] = cluster_counts['Cluster'].map(cluster_names)
                    
                    # Sort the DataFrame by Cluster ID before creating the plot
                    cluster_counts = cluster_counts.sort_values('Cluster')

                    # Create the bar chart with sorted data
                    fig = px.bar(
                        cluster_counts, 
                        x='Cluster_Name', 
                        y='Count',
                        color='Cluster',
                        color_discrete_map={
                            0: "#3498db",
                            1: "#2ecc71",
                            2: "#e74c3c",
                            3: "#f39c12"
                        },
                        labels={'Cluster_Name': 'Cluster', 'Count': 'Number of Customers'},
                        category_orders={"Cluster_Name": [cluster_names[i] for i in range(4)]},
                    )

                    # Explicitly set the color scale to ensure it uses your mapping
                    fig.update_traces(marker_color=[
                        {
                            0: "#3498db",
                            1: "#2ecc71", 
                            2: "#e74c3c",
                            3: "#f39c12"
                        }[cluster] for cluster in cluster_counts['Cluster']
                    ])
                    
                    # Customize the hover template to show both cluster name and ID
                    fig.update_traces(
                        hovertemplate='<b>%{x}</b><br>Cluster ID: %{marker.color}<br>Customers: %{y}<extra></extra>'
                    )
                    
                    st.plotly_chart(fig)
                    
                    # Display cluster statistics
                    st.subheader("Cluster Statistics")
                    
                    # Create a DataFrame with customer counts and percentages
                    total_customers = len(df)
                    cluster_stats = cluster_counts.copy()
                    cluster_stats['Percentage'] = (cluster_stats['Count'] / total_customers * 100).round(2)
                    
                    # Add cluster descriptions from the dictionary based on cluster name
                    cluster_stats['Description'] = cluster_stats['Cluster_Name'].map(cluster_strategy)
                    
                    # Sort by Cluster ID (ascending order)
                    cluster_stats = cluster_stats.sort_values('Cluster')
                    
                    # Display statistics with cluster names
                    st.dataframe(
                        cluster_stats[['Cluster', 'Cluster_Name', 'Count', 'Percentage', 'Description']],
                        column_config={
                            "Cluster": st.column_config.NumberColumn("Cluster ID"),
                            "Cluster_Name": st.column_config.Column("Cluster Name"),
                            "Count": st.column_config.NumberColumn("Number of Customers"),
                            "Percentage": st.column_config.NumberColumn("% of Total", format="%.2f%%"),
                            "Description": st.column_config.Column("Marketing Strategy")
                        },
                        hide_index=True
                    )
                    
                    # Add more in-depth analysis
                    st.subheader("Cluster Profile Analysis")
                    
                    # Create tabs for detailed cluster analysis
                    cluster_tabs = st.tabs([cluster_names[0], cluster_names[1], cluster_names[2], cluster_names[3]])
                    
                    for i, tab in enumerate(cluster_tabs):
                        with tab:
                            cluster_id = i
                            cluster_name = cluster_names[i]
                            
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                # Display cluster info in a card
                                st.markdown(
                                    f"""
                                    <div style="padding: 20px; border-radius: 10px; background-color: {get_cluster_color(cluster_id)}; color: white;">
                                        <h3 style="margin-top: 0;">Cluster {cluster_id}: {cluster_name}</h3>
                                        <p>{cluster_strategy[cluster_name]}</p>
                                    </div>
                                    """, 
                                    unsafe_allow_html=True
                                )
                                
                                # Display key metrics for this cluster
                                cluster_df = df[df['cluster'] == cluster_id]
                                customer_count = len(cluster_df)
                                percentage = round((customer_count / total_customers * 100), 2)
                                
                                st.metric(label="Customers in Cluster", value=customer_count)
                                st.metric(label="Percentage of Total", value=f"{percentage}%")
                            
                            with col2:
                                # Display more detailed analysis for this cluster
                                if not cluster_df.empty:
                                    # Calculate age distribution
                                    if 'age' in cluster_df.columns:
                                        st.subheader("Age Distribution")
                                        age_fig = px.histogram(
                                            cluster_df, 
                                            x='age',
                                            nbins=20,
                                            color_discrete_sequence=[{
                                                0: "#3498db",
                                                1: "#2ecc71",
                                                2: "#e74c3c",
                                                3: "#f39c12"
                                            }[cluster_id]],
                                            labels={'age': 'Age', 'count': 'Number of Customers'},
                                            title=f'Age Distribution in {cluster_name}'
                                        )
                                        st.plotly_chart(age_fig, use_container_width=True)
                                    
                                    # Calculate average metrics for this cluster vs overall
                                    st.subheader("Key Metrics Comparison")
                                    metrics_to_compare = ['income/month', 'account balance', 'total_withdrawals', 'total_deposits', 'transaction_count', 'loyalty score']
                                    metrics_available = [m for m in metrics_to_compare if m in cluster_df.columns]
                                    
                                    if metrics_available:
                                        # Calculate averages
                                        cluster_avgs = cluster_df[metrics_available].mean().to_dict()
                                        overall_avgs = df[metrics_available].mean().to_dict()
                                        
                                        comparison_data = []
                                        for metric in metrics_available:
                                            # Format the metric name for display
                                            display_name = ' '.join(word.capitalize() for word in metric.split('_')).replace('/', ' per ')
                                            
                                            # Calculate percentage difference
                                            if overall_avgs[metric] > 0:  # Avoid division by zero
                                                pct_diff = round(((cluster_avgs[metric] - overall_avgs[metric]) / overall_avgs[metric] * 100), 1)
                                            else:
                                                pct_diff = 0
                                            
                                            # Format values for currency or numbers
                                            if 'income' in metric or 'balance' in metric or 'withdrawals' in metric or 'deposits' in metric:
                                                cluster_val = f"${cluster_avgs[metric]:,.2f}"
                                                overall_val = f"${overall_avgs[metric]:,.2f}"
                                            else:
                                                cluster_val = f"{cluster_avgs[metric]:.1f}"
                                                overall_val = f"{overall_avgs[metric]:.1f}"
                                            
                                            comparison_data.append({
                                                'Metric': display_name,
                                                'Cluster Average': cluster_val,
                                                'Overall Average': overall_val,
                                                'Difference': f"{pct_diff:+.1f}%"
                                            })
                                        
                                        # Create comparison dataframe
                                        comparison_df = pd.DataFrame(comparison_data)
                                        
                                        # Display comparison table
                                        st.dataframe(
                                            comparison_df,
                                            column_config={
                                                "Metric": st.column_config.Column("Metric"),
                                                "Cluster Average": st.column_config.Column(f"{cluster_name} Average"),
                                                "Overall Average": st.column_config.Column("Overall Average"),
                                                "Difference": st.column_config.Column("% Difference")
                                            },
                                            hide_index=True
                                        )
                else:
                    st.warning("Cluster information not available in the dataset")
            else:
                st.error("Unable to fetch customer data. Please check if the API is running.")


        # Tab 2: Fetch Customer Information
        with tab2:
            st.header("Fetch Customer Information")
            
            customer_id = st.text_input("Enter Customer ID", "")
            
            if st.button("Fetch Customer"):
                if not customer_id:
                    st.warning("Please enter a customer ID")
                else:
                    try:
                        # Check if ID can be converted to integer
                        int(customer_id)
                        
                        # Modified get_customer function to suppress API error messages
                        try:
                            response = requests.get(f"{API_BASE_URL}/api/customers/{customer_id}")
                            if response.status_code == 200:
                                customer = response.json()['customer']
                            else:
                                customer = None
                        except Exception:
                            customer = None
                        
                        if customer:
                            # Create columns
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.subheader("Customer Details")
                                
                                # Only include specific fields: customer id, age group, gender, loyalty score, education
                                # Create a cleaner display format with better column names
                                customer_info = {
                                    "Attribute": [],
                                    "Value": []
                                }
                                
                                # Customer ID
                                customer_info["Attribute"].append("Customer ID")
                                customer_info["Value"].append(customer.get("customer id", "N/A"))
                                
                                # Age Group
                                customer_info["Attribute"].append("Age Group")
                                customer_info["Value"].append(customer.get("age group", "N/A"))
                                
                                # Gender (convert to text for better readability)
                                customer_info["Attribute"].append("Gender")
                                gender_val = customer.get("gender", "N/A")
                                customer_info["Value"].append("Female" if gender_val == 0 else "Male" if gender_val == 1 else gender_val)
                                
                                # Loyalty Score
                                customer_info["Attribute"].append("Loyalty Score")
                                customer_info["Value"].append(round(float(customer.get("loyalty score", 0)), 2) if customer.get("loyalty score", "N/A") != "N/A" else "N/A")
                                
                                # Education Level (convert to text if numeric)
                                customer_info["Attribute"].append("Education Level")
                                education_val = customer.get("education level", "N/A")
                                if education_val in [0, 0.0]:
                                    education_text = "High School"
                                elif education_val in [0.33, 1/3]:
                                    education_text = "Bachelor's"
                                elif education_val in [0.67, 2/3]:
                                    education_text = "Master's"
                                elif education_val in [1, 1.0]:
                                    education_text = "PhD"
                                else:
                                    education_text = education_val
                                customer_info["Value"].append(education_text)
                                
                                # Display as a DataFrame with clear headers
                                df_info = pd.DataFrame(customer_info)
                                st.dataframe(
                                    df_info,
                                    hide_index=True,
                                    column_config={
                                        "Attribute": st.column_config.Column("Customer Information", width="medium"),
                                        "Value": st.column_config.Column("Details", width="medium")
                                    }
                                )
                            
                            with col2:
                                if 'cluster' in customer and 'cluster_description' in customer:
                                    st.subheader("Cluster Information")
                                    
                                    # Display cluster info in a visually appealing way
                                    cluster_id = int(customer['cluster'])
                                    cluster_desc = customer['cluster_description']
                                    
                                    # Show cluster card
                                    st.markdown(
                                        f"""
                                        <div style="padding: 20px; border-radius: 10px; background-color: {get_cluster_color(cluster_id)}; color: white;">
                                            <h3 style="margin-top: 0;">Cluster {cluster_id}</h3>
                                            <p>{cluster_desc}</p>
                                        </div>
                                        """, 
                                        unsafe_allow_html=True
                                    )
                                    
                                else:
                                    st.warning("Cluster information not available for this customer")
                        else:
                            st.error(f"No customer found with ID: {customer_id}. Please check that you've entered a valid customer ID and try again. Valid IDs are integers that exist in the database.")
                    except ValueError:
                        st.error("Invalid customer ID format. Customer IDs should be integers. Please enter a numeric customer ID (e.g., 1, 2, 3, etc.)")

        # Tab 3: Predict Cluster
        with tab3:
            st.header("Predict Customer Cluster")
            st.markdown("Enter customer information to predict which cluster they belong to.")
            
            # Create two columns for input fields to save space
            col1, col2 = st.columns(2)
            
            with col1:
                # Demographic information
                st.subheader("Demographics")
                age = st.number_input("Age", min_value=18, max_value=100, value=30, key="predict_age")
                gender = st.selectbox("Gender", options=[(1, "Male"), (0, "Female")], format_func=lambda x: x[1], key="predict_gender")[0]
                education_options = [
                    (0, "High School"),
                    (0.33, "Bachelor's"),
                    (0.67, "Master's"),
                    (1, "PhD")
                ]
                education_level = st.selectbox(
                    "Education Level", 
                    options=education_options,
                    format_func=lambda x: x[1],
                    key="predict_education"
                )[0]
                
                # Financial information
                st.subheader("Financial Information")
                income = st.number_input("Monthly Income", min_value=0, value=5000, key="predict_income")
                account_balance = st.number_input("Account Balance", min_value=0, value=10000, key="predict_balance")
                loyalty_score = st.slider("Loyalty Score", min_value=0, max_value=1000, value=500, key="predict_loyalty")
                has_loan = st.checkbox("Has Loan", key="predict_loan")
                
            with col2:
                # Transaction information
                st.subheader("Transaction Behavior")
                total_withdrawals = st.number_input("Total Withdrawals", min_value=0, value=2000, key="predict_withdrawals")
                total_deposits = st.number_input("Total Deposits", min_value=0, value=3000, key="predict_deposits")
                transaction_count = st.number_input("Transaction Count", min_value=0, value=25, step=1, key="predict_transactions")
                
                # Digital engagement
                st.subheader("Digital Engagement")
                facebook = st.checkbox("Active on Facebook", key="predict_facebook")
                twitter = st.checkbox("Active on Twitter", key="predict_twitter")
                instagram = st.checkbox("Active on Instagram", key="predict_instagram")
                email = st.checkbox("Responsive to Email", key="predict_email")
            
            # Predict button
            if st.button("Predict Cluster"):
                # Prepare data for API call
                customer_data = {
                    "age": age,
                    "gender": gender,
                    "income/month": income,
                    "account balance": account_balance,
                    "loyalty score": loyalty_score,
                    "education level": education_level,
                    "total_withdrawals": total_withdrawals,
                    "total_deposits": total_deposits,
                    "transaction_count": transaction_count,
                    "Facebook": int(facebook),
                    "Twitter": int(twitter),
                    "Instagram": int(instagram),
                    "Email": int(email),
                    "has_loan": int(has_loan)
                }
                
                # Call API to assign cluster
                result = assign_cluster(customer_data)
                
                if result:
                    # Display the result
                    cluster_id = result['cluster']
                    cluster_description = result['cluster_description']
                    
                    st.success(f"Prediction complete!")
                    
                    # Display cluster information in a visually appealing card
                    st.markdown(
                        f"""
                        <div style="padding: 20px; border-radius: 10px; background-color: {get_cluster_color(cluster_id)}; color: white; margin-top: 20px;">
                            <h2 style="margin-top: 0;">Cluster {cluster_id}</h2>
                            <p style="font-size: 18px;">{cluster_description}</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Check if any features were missing in the request
                    if result.get('missing_features') and len(result['missing_features']) > 0:
                        st.info(f"Note: Some features were not provided and were filled with average values: {', '.join(result['missing_features'])}")
                    
                    # Display feature importance visualization
                    st.subheader("Key Features for This Customer")
                    
                    # Get submitted feature values for visualization
                    feature_data = {
                        'Feature': [],
                        'Value': [],
                        'Category': []
                    }
                    
                    # Demographics
                    feature_data['Feature'].extend(['Age', 'Gender', 'Education'])
                    feature_data['Value'].extend([
                        age, 
                        'Male' if gender == 1 else 'Female',
                        dict(education_options)[education_level]
                    ])
                    feature_data['Category'].extend(['Demographics'] * 3)
                    
                    # Financial
                    feature_data['Feature'].extend(['Income', 'Account Balance', 'Loyalty Score', 'Loan'])
                    feature_data['Value'].extend([
                        f"${income:,.2f}/month",
                        f"${account_balance:,.2f}",
                        loyalty_score,
                        'Yes' if has_loan else 'No'
                    ])
                    feature_data['Category'].extend(['Financial'] * 4)
                    
                    # Transaction
                    feature_data['Feature'].extend(['Withdrawals', 'Deposits', 'Transactions'])
                    feature_data['Value'].extend([
                        f"${total_withdrawals:,.2f}",
                        f"${total_deposits:,.2f}",
                        transaction_count
                    ])
                    feature_data['Category'].extend(['Transaction'] * 3)
                    
                    # Digital
                    feature_data['Feature'].extend(['Facebook', 'Twitter', 'Instagram', 'Email'])
                    feature_data['Value'].extend([
                        'Active' if facebook else 'Inactive',
                        'Active' if twitter else 'Inactive',
                        'Active' if instagram else 'Inactive',
                        'Active' if email else 'Inactive'
                    ])
                    feature_data['Category'].extend(['Digital'] * 4)
                    
                    # Create DataFrame for display
                    df_features = pd.DataFrame(feature_data)
                    
                    # Display as a colorful table
                    st.dataframe(
                        df_features,
                        column_config={
                            "Feature": st.column_config.Column("Feature"),
                            "Value": st.column_config.Column("Value"),
                            "Category": st.column_config.Column("Category")
                        },
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Add an option to save this customer to the database
                    st.subheader("Save Customer to Database")
                    save_customer = st.checkbox("Would you like to save this customer to the database?", key="predict_save")
                    
                else:
                    st.error("Error predicting cluster. Please try again or check if the API is running.")

        # Footer
        st.markdown("---")
        st.caption("Customer Clustering Dashboard")

        # Display API status
        try:
            response = requests.get(f"{API_BASE_URL}")
            if response.status_code == 200:
                st.sidebar.success("✅ API is connected and running")
            else:
                st.sidebar.warning("⚠️ API is running but returned an unexpected response")
        except Exception as e:
            st.sidebar.error(f"❌ API is not connected. Make sure the Flask API is running at {API_BASE_URL}")

        # Add data information in the sidebar
        st.sidebar.title("Data Information")
        df = get_all_customers()
        if not df.empty:
            st.sidebar.metric("Total Customers", len(df))
            
            if 'cluster' in df.columns:
                clusters = df['cluster'].dropna().astype(int).unique()
                st.sidebar.metric("Number of Clusters", len(clusters))
                
            # Show dataset features
            available_features = [col for col in df.columns if col in CLUSTER_FEATURES]
            st.sidebar.write("Available Features:")
            st.sidebar.write(", ".join(available_features))

        # Add help and information
        with st.sidebar.expander("Help & Information"):
            st.write("""
            **Customer Clustering Dashboard**
            
            This app allows you to explore customer segments created using K-means clustering.
            
            **Features:**
            - Cluster Information: View cluster distribution and insights
            - Fetch Customer: Look up customers and their assigned clusters
            - Predict Cluster: Categorize new customers

            
            """)


        # Version information
        st.sidebar.markdown("---")
        st.sidebar.caption("Version 1.0.0 | Made with Streamlit")
    ################################################################################
    
    
    ############################ Question B1 ###################################
    if function_choice == "Customer Preference Prediction":
        st.title("📊 Customer Preference Prediction")
        
        model = joblib.load("cus_pref_model.pkl") 
        st.success(f"✅ Customer Preference model loaded successfully!")

        st.sidebar.header("Customer General Data Inputs")
        age = st.number_input("Age", min_value=18, max_value=95, value=40)
        job_list = ['technician', 'student', 'retired', 'admin', 'self-employed', 'housemaid', 'management', 'services', 'unemployed', 'entrepreneur', 'blue-collar']
        job = st.selectbox("Job", job_list)
        marital_list = ['single', 'married', 'divorced']
        marital = st.selectbox("Marital Status", marital_list)
        education = { 'primary': 0, 'secondary': 1, 'tertiary': 2 }.get(st.selectbox('education', ['primary', 'secondary', 'tertiary']), -1)
        default = st.selectbox("Has Credit in Default?", ['yes', 'no'])
        balance = st.number_input("Average Yearly Account Balance", value=3000)
        pdays = st.number_input("Number of Days since Previous Campaign", min_value=-1, value=-1)
        previous = st.number_input("Number of Contacts before Campaign", min_value=0, value=0)
        contact_list = ['cellular', 'telephone']
        contact = st.selectbox("Way of Contact", contact_list)
        date = st.date_input("Date of Last Contact", value = 'today', max_value = 'today')
        
        inputs = pd.DataFrame({
            'age': [age],
            'education': [1 if education=='primary' else 2 if education=='secondary' else 3 if education == 'tertiary' else -1],
            'default': [0 if default=='no' else 1],
            'balance': [balance],
            'pdays': [pdays],
            'previous': previous,
            'job_' + job: [1],
            'marital_' + marital: [1],
            'contact_' + contact: [1],
            'last_contact_day': [date.day],
            'last_contact_month': [date.month],
            'days_since_contact': [(date - datetime.date.today()).days]
            })
        inputs = inputs.reindex(columns = ['age', 'education', 'default', 'balance', 'last_contact_day', 'last_contact_month', 'pdays', 'previous', 'job_admin', 'job_blue-collar',
                                           'job_entrepreneur', 'job_housemaid', 'job_management', 'job_retired', 'job_self-employed', 'job_services', 'job_student', 'job_technician',
                                           'job_unemployed', 'marital_divorced', 'marital_married', 'marital_single', 'contact_cellular', 'contact_telephone', 'days_since_contact'], fill_value=0)


        if st.sidebar.button("Predict"):
            res = model.rank(inputs)
            prod_ranks = res.melt(var_name="bank_products", value_name="ranks").sort_values(by="ranks")
            st.header("Prediction Result")
            st.info("Ranking of Bank Products:")
            n = 1
            for prod in prod_ranks["bank_products"]:
                st.info(str(n) + ": " + prod)
                n += 1
    ###########################################################################

    ############################ Question B2 ###################################
    if function_choice == "CTR-Based 'Real-Time' Campaign Optimizer":
        #st.set_page_config(page_title="CTR-Based Ad Optimizer", layout="centered")
        st.title("🎯 CTR-Based 'Real-Time' Campaign Optimizer")

        if "df" not in st.session_state:
            st.session_state.df = pd.DataFrame({
                "Product": ["Credit Card", "Premium credit card", "Loan"],
                "Clicks": [0, 0, 0],
                "Impressions": [-1, 0, 0],
                "Status": ["Active"] * 3,
                "Similar_Ads": ["No"] * 3,
                "CTR": [0] * 3

            })
            st.session_state.total_impressions = 0

        # Mapping of similar products (customizable)
        similar_map = {
            "Credit Card": "Premium credit card"
        }

        df = st.session_state.df

        reset_df = df.copy()
        if st.button("reset"):
            df["Impressions"] = [-1, 0, 0]
            df["Clicks"] = 0
            df["Status"] = ["Active"] * 3
            df["CTR"] = [0, 0, 0]

        st.markdown("Click the reset button to refresh the page")

        total_impressions = st.session_state.total_impressions
        idx = 0
        placeholder = st.empty()
        placeholder2 = st.empty()

        if placeholder.button("✅ Click Main Ad"):
            df.at[idx, "Clicks"] += 1

        if placeholder2.button("🙈 Ignore Main Ad"):
            pass

        active_products = df[df["Status"] == "Active"]

        if not active_products.empty:
            current_product = "Credit Card"
            df.at[idx, "Impressions"] += 1
            st.subheader(f"📢 Main Ad : {current_product}")

            clicks = df.at[idx, "Clicks"]
            impressions = df.at[idx, "Impressions"]
            ctr = clicks / impressions if impressions > 0 else 0

            if ctr < 0.1 and impressions > 10:
                df.at[idx, "Status"] = "Inactive"

                active = df[(df["Status"] == "Active") & (df["Product"] == "Credit Card")]
                if len(active) == 0:
                    st.subheader("Customer not interested in credit card, stopped ads")
                    placeholder.empty()
                    placeholder2.empty()

                else:
                    prod = active.loc[active["CTR"].idxmax()]
                    current_product = prod["Product"]

            elif ctr > 0.4 and impressions > 5:
                df.at[idx, "Similar_Ads"] = "Yes"
                similar_product = similar_map[current_product]
                st.markdown("#### 🎯 Because you engaged, check this out too:")
                if st.button(f"✅ Click Ad 2: {similar_product}"):
                    df.at[idx, "Impressions"] -= 1
                    # Add or update similar product row
                    if similar_product in df["Product"].values:
                        pcc_idx = df[df["Product"] == similar_product].index[0]
                        df.at[pcc_idx, "Clicks"] += 1
                        df.at[pcc_idx, "Impressions"] += 1

                if st.button(f"🙈 Ignore Ad 2: {similar_product}"):
                    df.at[idx, "Impressions"] -= 1
                    if similar_product in df["Product"].values:
                        pcc_idx = df[df["Product"] == similar_product].index[0]
                        df.at[pcc_idx, "Impressions"] += 1

                pcc_idx = df[df["Product"] == "Premium credit card"].index[0]
                pcc_ctr = df.at[pcc_idx, "CTR"]
                pcc_impressions = df.at[pcc_idx, "Impressions"]
                if pcc_ctr > 0.4 and pcc_impressions > 10:
                    st.markdown(
                        "Since you are interested in premium credit cards, here is some information on our private banking services...")
                    st.markdown(
                        '<span style="text-decoration: underline; color: blue; cursor: pointer;">View our private banking services</span>',
                        unsafe_allow_html=True)

            if ctr > 0.6 and impressions > 10:
                st.markdown("#### Due to further engagement, here are more relevant products:")
                loan_idx = df[df["Product"] == "Loan"].index[0]
                if st.button(f"✅ Click ad 3: Loan"):
                    df.at[idx, "Impressions"] -= 1
                    df.at[loan_idx, "Clicks"] += 1
                    df.at[loan_idx, "Impressions"] += 1
                if st.button(f"🙈 Ignore ad 3: Loan"):
                    df.at[idx, "Impressions"] -= 1
                    df.at[loan_idx, "Impressions"] += 1

                loan_ctr = df.at[loan_idx, "CTR"]
                loan_impressions = df.at[loan_idx, "Impressions"]
                if loan_ctr > 0.4 and loan_impressions > 10:
                    st.markdown("Since you are interested in loans, here is some information on our savings accounts...")
                    st.markdown(
                        '<span style="text-decoration: underline; color: blue; cursor: pointer;">View our savings account benefits</span>',
                        unsafe_allow_html=True)

        # Show updated CTRs
        st.subheader("📊 Ad Campaign Overview")
        df["CTR"] = df["Clicks"] / df["Impressions"].replace(0, 1)
        st.dataframe(df.style.format({"CTR": "{:.2%}"}))
    ######################################################################
    ######################## Question B3 ##############################
    elif function_choice == "ROI Prediction":
        model = joblib.load("roi_xgboost.pkl")  # Ensure the model is saved as .pkl

        # Streamlit app title
        st.title("💵ROI Prediction App")
        st.markdown("🚀 Enter your campaign details and get real-time predictions!")




        # Sidebar for user inputs
        st.sidebar.header("Input Features")



        def user_inputs():
            Click_Through_Rate = st.sidebar.number_input("Click-Through Rate", min_value=0.0, max_value=1.0, step=0.001)
            Cost_Per_Click = st.sidebar.number_input("Cost Per Click", min_value=1, max_value=999999, step=1)
            Acquisition_Cost = st.sidebar.number_input("Acquisition Cost", min_value=1, max_value=999999, step=1)
            Campaign_Type = st.sidebar.selectbox("Campaign Type", ["Email", "Influencer", "Social Media", "Display", "Search"])
            Conversion_Rate = st.sidebar.number_input("Conversion Rate", min_value=0, max_value=1, step=500)
            Engagement_Score = st.sidebar.number_input("Engagement Score", min_value=0, max_value=10, step=1)
            Channel_Used = st.sidebar.selectbox("Channel Used", ["Email", "Facebook", "Website", "Youtube", "Instagram", "Google Ads"])
            Target_Audience = st.sidebar.selectbox("Target Audience", ["Men 18-24", "Men 25-34", "All Ages", "Women 25-34", "Women 35-44"])
            Day_Type = st.sidebar.selectbox("Day Type", ["Weekday", "Weekend"])
            Is_Holiday = st.sidebar.selectbox("Is Holiday", ["1", "0"])
            Duration = st.sidebar.selectbox("Duration", ["15", "30", "45", "60"])

            # Convert categorical feature
            data = pd.DataFrame({
                "Campaign_Type": [Campaign_Type],
                "Target_Audience": [Target_Audience],
                "Duration": [Duration],
                "Channel_Used": [Channel_Used],
                "Conversion_Rate": [Conversion_Rate],
                "Acquisition_Cost": [Acquisition_Cost],
                "Engagement_Score": [Engagement_Score],
                "Day_Type": [Day_Type],
                "Click-Through_Rate": [Click_Through_Rate],
                "Cost_Per_Click": [Cost_Per_Click],
                "Is_Holiday": [Is_Holiday]
                
            })

            # Categorical Mapping (Ensure it's consistent with training)
            category_mappings = {
                "Campaign_Type": {"Email": 0, "Influencer": 1, "Social Media": 2, "Display": 3, "Search": 4},
                "Channel_Used": {"Email": 0, "Facebook": 1, "Website": 2, "Youtube": 3, "Instagram": 4, "Google Ads": 5},
                "Target_Audience": {"Men 18-24": 0, "Men 25-34": 1, "All Ages": 2, "Women 25-34": 3, "Women 35-44": 4},
                "Day_Type": {"Weekday": 0, "Weekend": 1},
                "Is_Holiday": {"1": 1, "0": 0},
                "Duration": {"15": 15, "30": 30, "45": 45, "60": 60}
            }

            # Apply categorical mapping
            for col, mapping in category_mappings.items():
                data[col] = data[col].map(mapping)

            return data


        # Get user inputs
        input_data = user_inputs()
        dinput = xgb.DMatrix(input_data)

        # Predict button
        if st.sidebar.button("Predict ROI"):
            
            # Make prediction
            prediction = model.predict(dinput)
            
            # Display prediction result
            st.subheader(f"Predicted ROI: {prediction[0]:.2f}")
    ########################################################################


    ####################### Question B5 ####################################
    elif function_choice == "Customer Churn Prediction":  
        st.title("📊 Customer Churn Prediction")
        model_choice = st.selectbox(f"Choose a model for {function_choice}:", list(FUNCTIONS[function_choice].keys()))

        # Load the selected model
        MODEL_PATH = os.path.join(SCRIPT_DIR, FUNCTIONS[function_choice][model_choice])
        
        if not os.path.exists(MODEL_PATH):
            st.error(f"❌ Model file `{FUNCTIONS[function_choice][model_choice]}` not found!")
            st.stop()

        # Load model
        model = joblib.load(MODEL_PATH)
        st.success(f"✅ {model_choice} model loaded successfully!")

        if model_choice == "Customer general data":
            # sidebar inputs
            st.sidebar.header("Customer General Data Inputs")
            # inputs
            credit_score = st.sidebar.number_input("Credit Score", min_value=300, max_value=850, value=700)
            age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30)
            tenure = st.sidebar.number_input("Time with bank (in years)", min_value=0, value=3)
            balance = st.sidebar.number_input("Balance ($)", min_value=0, value=20000)
            num_of_products = st.sidebar.number_input("Number of Products", min_value=1, value=1)
            has_credit_card = st.sidebar.selectbox("Has Credit Card", ["Yes", "No"])
            has_credit_card = 1 if has_credit_card == "Yes" else 0
            is_active_member = st.sidebar.selectbox("Is Active Member", ["Yes", "No"])
            is_active_member = 1 if is_active_member == "Yes" else 0
            estimated_salary = st.sidebar.number_input("Estimated Salary ($)", min_value=0, value=50000)
            geography = st.sidebar.selectbox("Where is customer located at", ["France", "Germany", "Spain"])
            geography_germany = 1 if geography == "Germany" else 0
            geography_spain = 1 if geography == "Spain" else 0
            gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
            gender_male = 1 if gender == "Male" else 0

            #input data
            user_data = pd.DataFrame([[credit_score, age, tenure, balance, num_of_products, has_credit_card, is_active_member,
                                       estimated_salary, geography_germany, geography_spain, gender_male]],
                                     columns=['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard',
                                              'IsActiveMember', 'EstimatedSalary', 'Geography_Germany',
                                              'Geography_Spain', 'Gender_Male'])
            user_data = create_interaction_features(user_data)

            # prediction button
            if st.sidebar.button("Predict"):
                prediction = model.predict(user_data)[0]
                result_text = "⚠️ This customer is likely to churn!" if prediction == 1 else "👍 This customer is likely to stay."
    
                st.header("Prediction Result")
    
                # change background color based on prediction
                if prediction == 1:
                    #  red for churn
                    st.markdown(
                        f"<style>body {{background-color: red;}}</style>", 
                        unsafe_allow_html=True
                    )
                    st.error(result_text)  
                else:
                    # green for stay
                    st.markdown(
                        f"<style>body {{background-color: green;}}</style>", 
                        unsafe_allow_html=True
                    )
                    st.success(result_text) 

        elif model_choice == "Customer credit card data":
            df = preprocess_credit_card_data()

            # sidebar inputs
            st.sidebar.header("Customer Credit Card Data Inputs")
            
            # inputs
            limit_balance = st.sidebar.number_input("Credit Limit", min_value=1, value=10000)
            sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
            sex_value = 1 if sex == "Male" else 2
            education = st.sidebar.selectbox("Education", ["Graduate School", "University", "High School", "Others"])
            education_value = 1 if education == "Graduate School" else (2 if education == "University" else (3 if education == "High School" else 4))
            marriage = st.sidebar.selectbox("Marriage status", ["Married", "Single", "Other"])
            marriage_value = 1 if marriage == "Married" else (2 if marriage == "Single" else 3)
            age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30)
            
            pay_options = [
                "Paid duly", 
                "1 month delay", 
                "2 months delay", 
                "3 months delay", 
                "4 months delay", 
                "5 months delay", 
                "6 months delay", 
                "7 months delay", 
                "8 months delay", 
                "9 months and above"]
            
            pay_3_text = st.sidebar.selectbox("Repayment status this month", pay_options)
            pay_4_text = st.sidebar.selectbox("Repayment status 1 month ago", pay_options)
            pay_5_text = st.sidebar.selectbox("Repayment status 2 months ago", pay_options)
            pay_6_text = st.sidebar.selectbox("Repayment status 3 months ago", pay_options)

            pay_status_map = {
                "Paid duly": -1,
                "1 month delay": 1,
                "2 months delay": 2,
                "3 months delay": 3,
                "4 months delay": 4,
                "5 months delay": 5,
                "6 months delay": 6,
                "7 months delay": 7,
                "8 months delay": 8,
                "9 months and above": 9}
            
            pay_3 = pay_status_map.get(pay_3_text, -1)
            pay_4 = pay_status_map.get(pay_4_text, -1)
            pay_5 = pay_status_map.get(pay_5_text, -1)
            pay_6 = pay_status_map.get(pay_6_text, -1)
            
            bill_amt3 = st.sidebar.number_input("Bill statement this month", min_value=0, value=1000)
            bill_amt4 = st.sidebar.number_input("Bill statement 1 month ago", min_value=0, value=1000)
            bill_amt5 = st.sidebar.number_input("Bill statement 2 months ago", min_value=0, value=1000)
            bill_amt6 = st.sidebar.number_input("Bill statement 3 months ago", min_value=0, value=1000)
            
            pay_amt3 = st.sidebar.number_input("Amount paid this month", min_value=0, value=200)
            pay_amt4 = st.sidebar.number_input("Amount paid 1 month ago", min_value=0, value=200)
            pay_amt5 = st.sidebar.number_input("Amount paid 2 months ago", min_value=0, value=200)
            pay_amt6 = st.sidebar.number_input("Amount paid 3 months ago", min_value=0, value=200)
            
            column_names = [
                'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
                'PAY_3_0', 'PAY_3_1', 'PAY_3_2', 'PAY_3_3', 'PAY_3_4', 'PAY_3_5', 'PAY_3_6',
                'PAY_3_7', 'PAY_3_8', 'PAY_4_0', 'PAY_4_1', 'PAY_4_2', 'PAY_4_3',
                'PAY_4_4', 'PAY_4_5', 'PAY_4_6', 'PAY_4_7', 'PAY_4_8', 'PAY_5_0',
                'PAY_5_2', 'PAY_5_3', 'PAY_5_4', 'PAY_5_5', 'PAY_5_6', 'PAY_5_7',
                'PAY_5_8', 'PAY_6_0', 'PAY_6_2', 'PAY_6_3', 'PAY_6_4', 'PAY_6_5',
                'PAY_6_6', 'PAY_6_7', 'PAY_6_8', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5',
                'BILL_AMT6', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']

            pay_3_encoded = [1 if pay_3 == i else 0 for i in range(9)]
            pay_4_encoded = [1 if pay_4 == i else 0 for i in range(9)]
            pay_5_encoded = [1 if pay_5 == i else 0 for i in range(9)]
            pay_6_encoded = [1 if pay_6 == i else 0 for i in range(9)]

            pay_5_encoded = pay_5_encoded[:1] + pay_5_encoded[2:] 
            pay_6_encoded = pay_6_encoded[:1] + pay_6_encoded[2:]  

            user_data = pd.DataFrame([[limit_balance, sex_value, education_value, marriage_value, age] + 
                                      pay_3_encoded + pay_4_encoded + pay_5_encoded + pay_6_encoded + 
                                      [bill_amt3, bill_amt4, bill_amt5, bill_amt6] + 
                                      [pay_amt3, pay_amt4, pay_amt5, pay_amt6]],
                                     columns=column_names)

            # prediction button
            if st.sidebar.button("Predict"):
                prediction = model.predict(user_data)[0]
                result_text = "⚠️ This customer is likely to churn!" if prediction == 1 else "👍 This customer is likely to stay."
    
                st.header("Prediction Result")
    
                # change background color
                if prediction == 1:
                    #  red for churn
                    st.markdown(
                        f"<style>body {{background-color: red;}}</style>", 
                        unsafe_allow_html=True
                    )
                    st.error(result_text) 
                else:
                    #  green for stay
                    st.markdown(
                        f"<style>body {{background-color: green;}}</style>", 
                        unsafe_allow_html=True
                    )
                    st.success(result_text)
                    
        ####################################################

