#  Customer Segmentation Using K-Means Clustering

This project applies K-Means clustering to segment bank customers based on demographics and transactional behavior. The goal is to help financial institutions deliver more targeted and effective marketing strategies.

---

## Folder Structure

File 1: data_generation_code.py
- This file contains the code used to generate the synthetic dataset used for 
customer segmentation. 

File 2: customer_segmentation.ipynb
- This file contains the code used to train the different types of segmentation models, before
deciding on the one being used for our project.
- It also contains analysis of some of the characteristics of the clusters.
- For the full reasoning/analysis, refer to customer_segmentation_final.ipynb


File 3: generated_bank_data.csv
- This file contains the Dataframe of customer data generated using data_generation_code.py.

File 4: final_segmentation_model.py
- This file contains the code used to train the final model being used.

File 5: generated_bank_data.csv
- This file contains the dataset generated using File 4. This dataset was used for training the customer segmentation model.

## Methodology

- **Algorithm**: K-Means Clustering  
- **Features Used**: Income, Account Balance, Loyalty Score, Transaction Count and other customer attributes
- **Variants**: Different models run with K=4 , K=5 and K=6 for comparison

---

## Key Insights (K=4)

- Identified the following 4 clusters based on customer behaviour:
1. Cluster 0: frequent users, high income, medium loyalty, semi-budget conscious
2. Cluster 1: Occasional users, medium income, medium loyalty, not budget conscious
3. Cluster 2: very frequent users, high income, medium loyalty, very budget conscious
4. Cluster 3: Semi-frequent users, medium income, low loyalty, not budget conscious

## Business Impact

- Segmentation enables personalized outreach strategies for each of the 4 clusters,
which can improve marketing ROI, customer retention, and satisfaction.

- We have successfully identified key segments with distinct behaviors, using a segmentation model built on
customer attributes and transactional data.
- We will use these key segments derived here to recommend targeted marketing approaches
for each cluster/segment in the Behavioral Patterns analysis in A3.


---
