import streamlit as st
import pandas as pd
import numpy as np
import joblib  # To load the trained model
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder

model = joblib.load("xgboost_model.pkl")  # Ensure the model is saved as .pkl

st.title("ROI Prediction App")
st.write("This app predicts the ROI of marketing campaigns based on various features.")
st.write("Please enter the features below to get the predicted ROI.")
st.sidebar.header("Input Features")

# Define input fields based on dataset columns
def user_inputs():
    Click_Through_Rate = st.sidebar.number_input("Click-Through Rate", min_value=0, max_value=1, step=0.001)
    Cost_Per_Click = st.sidebar.number_input("Cost Per Click", min_value=1, max_value=999999, step=0.01)
    Acquisition_Cost = st.sidebar.number_input("Acquisition Cost", min_value=1, max_value=999999, step=0.01)
    Campaign_Type = st.sidebar.selectbox("Campaign Type", ["Email", "Influencer", "Social Media", "Display", "Search"])
    Conversion_Rate = st.sidebar.number_input("Conversion Rate", min_value=0, max_value=1, step=0.001)
    Engagement_Score = st.sidebar.number_input("Engagement Score", min_value=0, max_value=10, step=0.1)
    Channel_Used = st.sidebar.selectbox("Channel Used", ["Email", "Facebook", "Website", "Youtube", "Instagram", "Google Ads"])
    Target_Audience = st.sidebar.selectbox("Target Audience", ["Men 18-24", "Men 25-34", "All Ages", "Women 25-34", "Women 35-44"])
    Day_Type = st.sidebar.selectbox("Day Type", ["Weekday", "Weekend"])
    Is_Holiday = st.sidebar.selectbox("Is Holiday", ["1", "0"])
    Duration = st.sidebar.selectbox("Duration", ["15", "30", "45", "60"])

    data = pd.DataFrame({
        "Click_Through_Rate": [Click_Through_Rate],
        "Cost_Per_Click": [Cost_Per_Click],
        "Conversion_Rate": [Conversion_Rate],
        "Engagement_Score": [Engagement_Score],
        "Campaign_Type": [Campaign_Type],
        "Channel_Used": [Channel_Used],
        "Target_Audience": [Target_Audience],
        "Day_Type": [Day_Type],
        "Is_Holiday": [Is_Holiday],
        "Duration": [Duration],
        "Acquisition_Cost": [Acquisition_Cost]
    })

    #Convert categorical features to numerical using Label Encoding
    encoder = LabelEncoder()
    data["Campaign_Type"] = encoder.fit_transform(data["Campaign_Type"])
    data["Channel_Used"] = encoder.fit_transform(data["Channel_Used"])
    data["Target_Audience"] = encoder.fit_transform(data["Target_Audience"])
    data["Day_Type"] = encoder.fit_transform(data["Day_Type"])
    data["Is_Holiday"] = encoder.fit_transform(data["Is_Holiday"])
    data["Duration"] = encoder.fit_transform(data["Duration"])

    return data

# Get user inputs
input_data = user_inputs()

# Predict button
if st.sidebar.button("Predict ROI"):
    
    # Make prediction
    prediction = model.predict(input_data)
    
    # Display prediction result
    st.subheader(f"Predicted ROI: {prediction[0]:.2f}")
    st.write(f"RSME of the model: {np.sqrt(model.score(input_data, prediction)):.2f}")
    st.write("The model's ROI predictions are, on average, {:.2f} away from the actual ROI.".format(np.sqrt(model.score(input_data, prediction))))

