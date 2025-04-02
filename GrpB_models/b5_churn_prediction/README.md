## Machine Learning Models for Customer Churn Prediction

This folder contains two machine learning models designed for:
1. [**Predicting customer churn in a banking churn dataset**](#model-1-customer-churn-prediction)
2. [**Predicting customer churn using credit card financial history**](#model-2-credit-card-default-prediction)

Both models use classification techniques to analyze customer behavior and identify patterns leading to churn or default.


### Model 1: Customer Churn Prediction

#### **Objective**
This model aims to predict whether a customer will churn (exit the bank) based on demographic and financial behavior data.

#### **Dataset**
- This dataset is obtained from Kaggle [Banking Customer Churn Prediction Dataset](https://www.kaggle.com/datasets/saurabhbadole/bank-customer-churn-prediction-dataset).
- It contains customer records with features such as **Age, Balance, NumOfProducts, Geography, Gender**, and the target variable **Exited (1 for churn, 0 for retained).**
- The dataset is preprocessed using **one-hot encoding** for categorical variables like Geography and Gender.

#### **Data preprocessing**
1. **Adding Interaction Features**
  - New features were created by multiplying key numerical variables to capture relationships between them.
  - Examples include **Age × Balance**, **Balance × NumOfProducts**, and **Age × IsActiveMember**.
  - These interaction terms help the model detect dependencies and improve predictive accuracy.
2. **Handling Class Imbalance with SMOTE**
   - Since churned customers are a minority class (20%), **Synthetic Minority Over-sampling Technique (SMOTE)** is used to balance the dataset.

#### **Modeling Approach**
1. **Logistic Regression**
   - A straightforward and interpretable baseline model used to establish a benchmark for recall.
   - Uses **grid search with cross-validation** to optimize hyperparameters.
2. **Random Forest Classifier**
   - A more complex, non-linear model to capture interactions between features.
   - Important features identified using feature importance ranking.
3. **Evaluation Metrics**
   - **Accuracy, Recall, F1-score** with a focus on maximizing recall, prioritizing the identification of churned customers due to the significant cost of customer attrition.

#### **Key Insights**
- **Model Performance:**
  - Random Forest outperforms Logistic Regression in both recall and F1-score.
  - The best Random Forest model achieved an accuracy of **74%**, recall of **81%**, and an F1-score of **56%**.
  - The optimal parameters for the Random Forest model include:
    - No bootstrapping
    - Max tree depth of 10
    - 5 minimum samples per leaf
    - Minimum of 15 samples to split
    - 1000 estimators
  - Therefore, we have selected Random Forest as our preferred method.

- **Feature Importance:**
  - Key features influencing churn include **Age**, **Number of products**, and **Account balance**.

- **Churn Patterns:**
  - The churn rate for individuals older than 37 is **more than three times higher** than for those aged 37 and below.
  - Customers with only one product have a churn rate that is **more than double** that of customers with multiple products.

- **Recommendations:**
  - The bank should focus on engaging older customers with tailored support.
  - Encourage customers with a single product to adopt additional services to reduce churn.


---

### Model 2: Credit Card Default Prediction

#### **Objective**
This model predicts whether a credit card customer is likely to default on their payments based on historical transaction data.

#### **Dataset**
- The dataset [Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) is sourced from the UCI Machine Learning Repository.
- It includes financial features such as the amount of given credit, history of past payment, amount of bill statement and amount of previous payment.
- The target variable for this dataset is default and does not have direct churn labels. We defined churn based on certain assumptions:
  - **The customer churns if no payments are made for two months**.
      - **Explanation**: A lack of payments for two consecutive months could signal that a customer is no longer actively using their credit card or may be experiencing financial difficulties. This behavior is often associated with customers who are at risk of discontinuing their relationship with the bank.
  - **The customer churns if they have decreased card usage over three months**.
      - **Explanation**: A decline in card usage over three months may suggest that the customer no longer finds the credit card valuable or is cutting back on spending due to dissatisfaction or financial difficulties. Such decreasing usage patterns can serve as an early indicator of churn, as customers who are disengaging with their credit cards may be preparing to switch to other financial institutions.
  - **The customer churns if they make large, sudden debt payments**.
      - **Explanation**: Customers who make large payments that significantly reduce their outstanding balance may be trying to clear their debt quickly. While this could indicate financial responsibility, it could also suggest a customer attempting to exit the credit card relationship, particularly if the payment is not part of their usual spending pattern. This behavior may be a sign that the customer is trying to close their account or avoid future interest charges, which could result in churn.

#### **Data preprocessing**
1. The value "-2" in PAY variables is found to be the same as "0" and hence all "-2" values will be replaced with "0".
2. **One-hot encoding for PAY variables** (to convert categorical payment history into numeric form).
3. **Derived Features:**
   - **Sudden Large Payment:** This feature identifies customers who make a significant payment (more than 90% of their bill) in either the first or second payment period. 1 is assigned if the payment amount in either period exceeds 90% of the corresponding bill amount, or 0 otherwise.
   - **Decreasing Usage:** This feature identifies customers whose credit card usage has decreased over the last three months. If the bill amounts for the last three months have been decreasing, it assigns a value of 1, or 0 otherwise.
   - **Churn Definition:** A combination of no payments for the last two months, sudden large payments, or decreasing usage.

#### **Modeling Approach**
1. **Logistic Regression**
   - Simple, interpretable baseline.
   - Used to compare against more complex models.
2. **Random Forest Classifier**
   - Captures complex interactions between financial history and default risk.
   - More stable against noisy labels.
3. **Evaluation Metrics**
- Since labels are based on assumptions, the model aims for a balance between **recall and F1-score** instead of optimizing only for recall.

#### **Key Insights**
- **Model Performance:**
  - Random Forest outperforms Logistic Regression in accuracy, recall and F1-score.
  - The best Random Forest model achieved an accuracy of **71%**, recall of **70%**, and an F1-score of **71%**.
  - The optimal parameters for the Random Forest model include:
    - No bootstrapping
    - No max tree depth
    - 1 minimum sample per leaf
    - Minimum of 5 samples to split
    - 100 estimators
  - Therefore, we have selected Random Forest as our preferred method.

- **Feature Importance:**
  - Important features include the **bill amounts**, the **amount of given credit** and **age**.

- **Churn Patterns:**
  - The t-statistic of -24.67 and the p-value of 4.45 × 10<sup>-133</sup> indicate a **statistically significant difference** in churn rates between **low and high balance customers**. This suggests that **account balance** is an important factor influencing customer churn.

- **Recommendations:**
  - The bank can consider assisting high-balance customers with debt management.


---

### Conclusion

This task focused on building models to predict customer churn. Both models utilized Random Forest classifiers, which outperformed Logistic Regression in key metrics such as recall and F1-score.

For the first model trained on the banking customer churn dataset, we identified critical features like **Age**, **Number of products**, and **Account balance**, which were key determinants of churn. The model demonstrated that older customers and those with only one product are more likely to churn, highlighting the need for targeted engagement and product diversification strategies to reduce churn.

In the second model trained on the UCI credit card data, we introduced custom features like **Sudden Large Payment** and **Decreasing Usage** to help identify customers at high risk of churning. A significant difference in churn rates was observed between low and high balance customers, emphasizing the importance of managing account balances for better customer retention. The model suggested that assisting high-balance customers with debt management could be an effective strategy.

Both models show the power of Random Forest in capturing complex patterns and interactions in customer behavior. Moving forward, focusing on the insights gained from these models—such as targeting high-risk customers based on balance and product usage—could help the bank enhance customer loyalty, increase retention, and drive long-term profitability.


