# Customer behavior analysis
This project analyzes customer behavior across different segments to help banks develop more informed and data-driven marketing strategies. The goal is to help financial institutions deliver more targeted and effective marketing strategies.

---

## Project Structure

### Folder 1: Data Retrieval
- `eugene_data.py`  
  Extracts and compiles the initial customer dataset.
- `eugene_data.csv`  
  Raw dataset output from extraction.
- `df_k4.csv`
  Dataset that contains customer segmentation

### Folder 2: Data Cleaning
- `data_merging.py`  
  Merges customer segmentation results with original dataset to get more relevant features.
- `df_merged.csv`  
  Final cleaned dataset ready for analysis.

### Folder 3: Data Analysis
- `digital_engagement_analysis.py`  
  Explores relationship between Click-Thru-Rate(CTR) and purchase behaviour, CTR and impressions to provide marketing strategies.
- `product_usage_analysis.py`  
  Explores the relationship between product ownership and purchase behaviour
- `transaction_analysis.py`  
  Explores transaction type and amount amongst different segments.

---


## Key Insights 

High-Value Power users do not respond well to digital marketing strategies. Value-Driven Frequent users and Affluent inactives show that higher CTR for these groups will usually lead to a higher chance of buying a product for all digital engagement methods. Budget-Conscious Occasionals shows that higher CTR will usually lead to a higher chance of buying a product for all digital engagement methods except Instagram. For all modes of digital engagement, as the number of impressions increases, the CTR decreases

Previous product ownership shows no trends of future product purchases.

High-Value Power users tend to make the highest amount of withdrawals in terms of volume and frequency while Affluent Inactives tend to make the highest amount of deposits in terms of volume and frequency.


---

## Business Impact

For High-Value Power users, a marketing strategy or product related to withdrawals would be the most effective in getting their business while for Affluent inactive users a marketing strategy or product that is related to deposits will be the most effective.

For Budget-Conscious Occasionals, a digital marketing strategy will be the most effective. This can be done via any social media except Instagram. However, this should not be overdone and the number of impressions we should show them should be limited to a rough range of 8-12. This digital engagement strategy is the same for Value-Driven frequent users except that they respond well to all forms of social media. However, they too should also be limited to 8-12 impressions per social media outlet.


---
