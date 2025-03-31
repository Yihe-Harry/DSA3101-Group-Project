# Real-Time Customer Segmentation for Personalized Marketing

## Objective
- Develop a real-time segmentation model that updates dynamically as new customer data arrives.
- Improve the accuracy of customer targeting in marketing campaigns.
- Increase customer engagement through personalized marketing strategies.

## Expected Outcome
- More precise customer segmentation.
- Improved marketing efficiency and reduced ad spend wastage.
- Increased customer satisfaction due to personalized experiences.

## Structure
```
├── clean_data.py         # Script for cleaning and preprocessing customer data
├── model.py              # Script for clustering customers and real-time segmentation
├── README.md             # Project documentation
```

## Setup Instructions
### Prerequisites
Ensure you have Python installed along with the necessary libraries. You can install them using:
```bash
pip install pandas numpy scikit-learn
```

## How It Works
1. **Data Cleaning (clean_data.py)**
   - Removes duplicates and missing values.
   - Converts categorical variables to appropriate types.
   - Handles outliers using the IQR method.

2. **Clustering Model (model.py)**
   - Selects numerical features for clustering.
   - Normalizes the data.
   - Uses KMeans clustering to segment customers.
   - Simulates real-time customer data and assigns new customers to segments dynamically.
