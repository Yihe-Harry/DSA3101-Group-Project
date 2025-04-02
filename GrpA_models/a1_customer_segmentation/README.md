#  Customer Segmentation Using K-Means Clustering

This project applies K-Means clustering to segment bank customers based on demographics and transactional behavior. The goal is to help financial institutions deliver more targeted and effective marketing strategies.

---

## Project Structure

### Folder 1: data
- `main_dataset_generation.py`  
  Extracts and compiles the initial customer dataset.
- `main_dataset.csv`  
  Raw dataset output from extraction.

### Folder 2: data_cleaning
- `data_cleaning.py`  
  Handles missing values, formats, and prepares data for modeling.
- `main_dataset_cleaned.csv`  
  Final cleaned dataset ready for clustering.

### Folder 3: Modeling & Analysis
- `model_kmeans.py`  
  Performs K-Means clustering (K=4 and K=5) and interprets the results.
- `df_k4.csv` & `cluster_profile_k4.csv`  
  K=4 clustering results and segment profiles.
- `df_k5.csv` & `cluster_profile_k5.csv`  
  K=5 clustering results and segment profiles.

---

## Methodology

- **Algorithm**: K-Means Clustering  
- **Features Used**: Income, Account Balance, Loyalty Score, Transaction Count  
- **Variants**: Models run with K=4 and K=5 for comparison

---

## Key Insights (K=4)

- Income and account balance were the most distinctive features.
- Identified 4 customer types: Power Users, Frequent Users, Affluent Inactives, and Budget-Conscious Occasionals.

---

## Business Impact

Segmentation enables personalized outreach strategies:
- Reward Power Users
- Re-engage Affluent Inactives
- Encourage usage from low-loyalty Frequent Users
- Offer value-driven deals to Occasionals

Improves marketing ROI, customer retention, and satisfaction.

---
