## Objective

To find factors that are most strongly correlated with customer engagement in marketing campaigns and the key drivers for customer interaction and response. Using the findings we are then able to propose key metrics for tracking customer engagement over time.

## Dataset
1. bank_full_a2.csv  (Telemarketing of a Portuguese banking institution)
2. digital_marketing_campaign_dataset_a2.csv (Synthetic data taken from Kaggle -- The dataset underwent validation to ensure that the distributions and relationships between features align with realistic marketing scenarios)

## Methodology

1. Data Cleaning and Encoding
      - Categorical Variables Encoding: The script uses One-Hot Encoding to convert the categorical features such as job and
      marital into numerical features.
      - Categorical Columns Transformation: Variables like education, default, housing, loan, etc., are transformed into
        categorical types for further analysis.
      - Outcome Encoding: The target variable is converted into a binary outcome where 1 represents a placed deposit, and
        0 represents no placed deposit.
      - Removal of Unknown Contacts: Rows with unknown contact types are removed.

2. Exploratory Data Analysis (EDA)
      - Correlation Matrix: A heatmap is generated for the numerical variables to explore the correlation between features
        like age, balance, duration, campaign, etc.
      - Plots: Density plots and bar plots are created to visualize the distribution of key variables like duration, age,
        and pdays with respect to the outcome.

3. Logistic Regression
      - Model Training: A logistic regression model is trained on categorical variables to predict the likelihood of a
        client subscribing to a deposit/converted. Chosen as the outcome variable is binary and suspecting that the
        relationship is linear. 
      - P-values Analysis: The statistical significance of each feature is calculated using p-values from a logistic
        regression model.


## Findings

Factors that are most strongly correlated with customer engagement in marketing campaigns:
      - Session Duration (TimeOnSite / Duration of call)
      - Previous loyalty (loyalty points / poutcome)
      - Duration since last contact (pdays)

Key metrics for tracking customer engagement over time:
      1. Start of Campaign / Acquisition:
            - Outreach Rate (% of customer that click on Email, Site / Pick up call)
      2. During Campaign / Behaviour:
            - Session Duration (Call Duration / Time on Site)
      3. End of Campaign:
            - Churn Rate (% of customer that buy product)
            - Customer Satisfaction
      4. After Campaign:
            - Customer Retention Rate
            - Net Promoter Score (Tracks loyalty and likelihood to recommend)
            - Customer Lifetime Value



 

