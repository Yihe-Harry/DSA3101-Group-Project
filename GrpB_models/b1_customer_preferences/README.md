# Subgroup B1: Predicting Customer Preferences
## Running the Project with Docker

### Prerequisites

- Ensure you have Docker installed on your local machine. You can download and install Docker from https://www.docker.com/products/docker-desktop/.
- This project uses Python 3.10 as specified in the Dockerfile.

### Build and Run Instructions
1. Navigate to the file directory
   ```bash
   cd DSA3101-Group-Project/GrpB_models/b1_customer_preferences
   ```
2. Build the Docker image :

   ```bash
   docker build -t cus_pref_model .
   ```
3. Run the Docker image :

   ```bash
   docker run cus_pref_model
   ```
## Overview
This directory contains the models and insights for predicting individual customer preferences. The directory contains the following:

1. data_preparation.py — functions for data importing, cleaning and feature engineering.
2. hyperparameter_tuning.py — functions for hyperparameter tuning.
3. models.py — functions to run the models used.
4. main.py — full pipeline of data preparation, training and fitting ensemble model.
5. modelling_summary.ipynb — details of thought process and insights of the models.
6. Dockerfile — instructions for building Docker image.

## Data Preparation
### Dataset Description
The dataset used is the Bank Marketing data from UCI Machine Learning Repository. It includes the customer profile information(age, education, etc.), bank product information(housing_loan, personal_loan, term_deposit) and campaign information(duration, campaign).
### Data Preprocessing
We removed poutcome column with majority of missing value, changed the data type of columns(default, housing_loan, etc. ), renamed columns(job_admin. -> job_admin, etc.), use one-hot encoding(job, marital, contact) and label encoding(education) and created day_since_contact feature which represents the recency of last contact.
### Data Split
There are imbalanced labels for personal loan and term deposit so iterative stratification was used for a stratified split of the multi-label data to train and test.

## Modelling Process
### Modelling Approach
We used a one vs many approach with gradient boosting models to classify whether customers possess the bank products. After fitting different models to each bank product using lazypredict library, we found that Light Gradient Boosting model is the best for classifying housing loan and XGboost model for personal loan and term deposit. The performance of gradient boosting models corresponds our understanding that such models work well with imbalanced data. 
After tuning and fitting our data into each model, we classified each bank product using a threshold that minimises the business loss formula that we defined. For the recommendation system model, we concatenated the results for the different labels together to give recommendation rankings of the bank products using normalised prediction probabilities.
### Hyperparameter Tuning
Bayesian optimisation was used for the models for efficiency.
### Model Evaluation
The metric we chose to focus on for housing loan, the balanced label, is Area under Receiver Operating Characteristic curve(AUROC) and for the imbalanced labels, personal loan and term deposit, Area under Precision-Recall curve(AUPRC) since predicting customers who would buy the bank products(positive cases) are more important. For the ensemble model, we used macro averages as we treat all the bank products as of equal importance.
### Results
For the ensemble classification model, we achieved an 83.2% macro accuracy(included for easy understanding), macro AUROC score of 0.789 and macro AUPRC score of 0.543(baseline: 0.277).
### Analysis
The feature importance over all models show that days_since_contact, balance and last_contact_month are generally the most important features.

## Key Insights
### Housing Loan
The target group for housing loans are youths and middle age customers with lower bank balance, this corresponds with the business understanding that the youths and middle age are more likely to buy new houses and loans are generally for customers lacking funding for their new houses. It is recommended to suggest housing loan to these target groups to increase success rate of sales of marketing campaigns.

### Personal Loan
The target group of personal loan is customers with low bank balance and special groups such as students are more inclined to take personal loans due to financial circumstances. There is also seasonal trend with July having the highest personal loan adoption proportion so it is recommended to reach out to customers about personal loans during months of higher proportion for a higher success rate of sales of marketing campaigns.

### Term Deposit
The subsciption of term deposit is closely tied to the contacts the customers received with a general decrease in subscriptions across day since last contact and general increase of subscription with increased frequency of contact. It is recommended to contact the customers after a short period since subscription increase initially with day since last contact and with appropriate frequency since subscription rate drops drastically after 15 contacts. Contacting customers during peak subscription months like March, September, etc. can increase success rates of sales of marketing campaigns.

![Prediction Result](https://raw.githubusercontent.com/Yihe-Harry/DSA3101-Group-Project/main/Dashboard/Images/prediction_result.JPG)

## Conclusion
For marketing campaigns, targeting bank products to the right customer segments at the right time is crucial for maximizing the success of marketing campaigns and improving customer engagement. By aligning product offerings with customer preferences, the bank can enhance customer satisfaction while increasing sales conversion rates.

