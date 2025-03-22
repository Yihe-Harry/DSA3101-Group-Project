This folder contains the relevant documents and explanations relating to Subgroup B question 4, Cost-Effectiveness of Campaigns

# Cost-Optimized Personalized Marketing Strategy for Banks
## 1) Introduction
This report outlines a data-driven approach to balancing personalisation and cost-effectiveness in bank marketing campaigns. The proposed framework integrates customer segmentation, predictive modeling, and constrained optimisation to determine the most efficient marketing spend while maximising customer response rates and Return on Investment (ROI).

## 2) Methodology
### Step 1: Customer Segmentation
To better understand customer behaviour, an initial segmentation is performed using unsupervised learning techniques such as K-Means clustering, DBSCAN, or autoencoders. This step helps group customers based on demographics, transaction patterns, engagement history, and economic conditions. 

### Step 2: Predicting Customer Response Probability
A machine learning model (e.g., logistic regression, XGBoost, or neural networks) is trained to predict the probability of each customer responding to a marketing campaign. The model leverages features such as:

Customer attributes (age, income, credit score, financial behavior)
Past response history (engagement with previous campaigns)
Economic indicators (inflation rates, interest rates)
Transaction data (spending patterns, savings behavior)
The output is a probability score between 0 and 1, representing the likelihood that the customer will respond to a given marketing effort.

### Step 3: Determining Optimal Personalisation Level & Cost Estimation
Instead of predicting personalisation levels and cost separately, a cost-aware personalisation model is employed. This model determines the optimal level of personalisation (e.g., generic email, targeted SMS, personalized call) while estimating the cost associated with each option.

Inputs: Customer profile, predicted response probability, campaign type
Outputs:
Personalisation level (e.g., mass email vs. tailored offer)
Estimated cost per personalisation level
Machine learning techniques such as reinforcement learning (RL) or Bayesian optimization can be used to dynamically adjust personalisation levels based on expected response.

### Step 4: Predicting ROI Metrics
To evaluate cost-effectiveness, additional models predict key business metrics, including:

Expected revenue per customer
Customer Lifetime Value (CLV)
Cost per successful response
These predictions help quantify the financial impact of marketing efforts before optimization.

### Step 5: Constrained Budget Optimisation
A constrained optimisation algorithm is applied to maximize response rates and ROI while ensuring that marketing costs remain within the allocated budget.

Objective Function: Maximise campaign effectiveness (response rate, revenue uplift)
Constraints:
Budget limitations (total marketing spend)
Customer fatigue limits (avoid excessive contact)
Regulatory constraints (compliance with data privacy laws)
Optimisation techniques such as Linear Programming (LP), Quadratic Programming (QP), or Reinforcement Learning can be used to allocate the budget across different customer segments efficiently.

## 3) Expected Outcome
By integrating predictive analytics with cost-aware optimisation, the proposed approach ensures that:

Personalisation is tailored to customer needs while staying cost-effective.
Marketing spend is optimised to maximise engagement and ROI.
Business constraints (budget, regulations, customer fatigue) are respected in campaign execution.
This model provides a scalable, data-driven solution for banks looking to enhance marketing efficiency while maintaining high response rates.
