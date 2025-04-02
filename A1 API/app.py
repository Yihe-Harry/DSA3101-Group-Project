import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

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


# App title
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
