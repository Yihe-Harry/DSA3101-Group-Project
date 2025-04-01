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
1. Session Duration (TimeOnSite / Duration of call)
2. Campaign Channels
3. Previous loyalty (loyalty points / poutcome)
4. Duration since last contact (pdays)

Key metrics for tracking customer engagement over time:
1. Start of Campaign / Acquisition
      - Outreach Rate (% of customer that click on Email, Site / Pick up call): Provides insights on the effectiveness of campaign channels used.

2. During Campaign / Behaviour
      - Session Duration (Call Duration / Time on Site): Assess the quality of the interaction. If customers are spending more time on the site or staying on calls longer, it’s a positive sign that the campaign is piquing their interest.
  
3. End of Campaign: 
      - Churn Rate (% of customer that stopped engaging): Understanding if there exists a mismatch between customer needs and what was offered. 
      - Net Promoter Score: Tracks loyalty and likelihood to recommend, crucial for retention and brand loyalty

3. After Campaign: 
      - Customer Retension Rate: Retention is often more cost-effective than acquiring new customers, and high retention rates indicate that customers find ongoing value in products or services provided.
      - Customer Lifetime Value: Understanding the long-term financial impact of customers and aids in assessing the return on investment (ROI) from marketing efforts. By tracking CLV, we can better allocate resources, target high-value customers, and identify opportunities.



 

