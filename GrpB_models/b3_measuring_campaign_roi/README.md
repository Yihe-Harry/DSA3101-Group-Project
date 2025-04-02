## Running the model training python script using Docker (If necessary)
Please ensure you have Docker installed and the repository cloned to your local device.
1. Navigate to the file directory
  ```bash
  cd DSA3101-Group-Project/GrpB_models/b3_measuring_campaign
  ```

2. Build the image
  ```bash
  docker build -t roi_prediction_model .
  ```
3. Run the container (Note: the following code assumes that the repository is in your local C drive)
  ```bash
  docker run --rm -v ${PWD}/C:/DSA3101-Group-Project/GrpB_models/b3_measuring_campaign roi_prediction_model
  ```
## Project Files 📂

### Notebooks 📖
- [📓 Model Analysis](https://github.com/Yihe-Harry/DSA3101-Group-Project/blob/main/GrpB_models/b3_measuring_campaign_roi/model_analysis.ipynb) - model_analysis.ipynb

### Dataset 📊
- [📂 Marketing Campaign Dataset](https://github.com/Yihe-Harry/DSA3101-Group-Project/blob/main/GrpB_models/b3_measuring_campaign_roi/marketing_campaign_dataset.csv) - marketing_campaign_dataset.csv

### Data Processing & Feature Engineering 🛠️
- [🔄 Data Cleaning](https://github.com/Yihe-Harry/DSA3101-Group-Project/blob/main/GrpB_models/b3_measuring_campaign_roi/data_cleaning.py) - data_cleaning.py
- [⚙️ Feature Engineering](https://github.com/Yihe-Harry/DSA3101-Group-Project/blob/main/GrpB_models/b3_measuring_campaign_roi/feature_engineering.py) - feature_engineering.py

### Model Training & Evaluation 🤖
- [🚀 XGBoost Model Training & Results](https://github.com/Yihe-Harry/DSA3101-Group-Project/blob/main/GrpB_models/b3_measuring_campaign_roi/roi_regression_xgboost.py) - roi_regression_xgboost.py
- [🎯 Hyperparameter Tuning](https://github.com/Yihe-Harry/DSA3101-Group-Project/blob/main/GrpB_models/b3_measuring_campaign_roi/model_optimization.py) - model_optimization.py

### Application & Deployment 🌍
- [🚪 Entry Point](https://github.com/Yihe-Harry/DSA3101-Group-Project/blob/main/GrpB_models/b3_measuring_campaign_roi/main.py) - main.py
- [💻 Streamlit Dashboard Interface](https://github.com/Yihe-Harry/DSA3101-Group-Project/blob/main/GrpB_models/b3_measuring_campaign_roi/app.py) - app.py
- [📦 Dockerfile](https://github.com/Yihe-Harry/DSA3101-Group-Project/blob/main/GrpB_models/b3_measuring_campaign_roi/Dockerfile) - Dockerfile

## Functionalities

Run `pip install pandas numpy holidays scikit-learn matplotlib xgboost hyperopt joblib` to download all necessary packages

Run `main.py` to run all scripts together and save the model in a .pkl file. It also produces a plot of the features ranked based on importance

Run `model_optimization.py` to return a set of the best parameters. These parameters can be used to replace the current parameters in [🚀 XGBoost Model Training & Results](https://github.com/Yihe-Harry/DSA3101-Group-Project/blob/main/GrpB_models/b3_measuring_campaign_roi/roi_regression_xgboost.py) if results are unsatisfactory.

## ROI Prediction using XGBoost model

To tackle the task of ROI regression, this project proposes the use of XGBoost, particularly given the large dataset of 200,000 entries. Through the analysis conducted in the notebooks, XGBoost demonstrates superior flexibility and provides deeper insights into the key factors influencing ROI. One notable advantage is its feature importance plot, which effectively highlights the most influential variables, offering businesses and banks actionable insights on where to focus for future campaigns.

Compared to Random Forest, XGBoost excels due to its boosting mechanism, which sequentially corrects errors from previous iterations, leading to better predictive performance. Additionally, XGBoost is computationally more efficient due to its parallelized execution and optimized handling of missing values, making it a more scalable choice for large datasets like this one.

## Objective

This pre-trained XGBoost aims to predict ROI of bank marketing campaigns while minimising as little error as possible.

## Limitations and Challenges

Since the dataset is fictitious, it lacks real-world patterns and variability, making it difficult to generate realistic ROI predictions. Additionally, the 'Customer Segment' feature was dropped due to irrelevant segment names in the dataset. In order to tackle this challenge, banks can incorporate the [customer segmentation models provided by Subgroup A](https://github.com/Yihe-Harry/DSA3101-Group-Project/tree/main/GrpA_models/a1_customer_segmentation) and gather the corresponding customer segment that each campaign was targeted to. This allows banks to use personalised marketing strategies as a feature in this XGBoost model, and perhaps it could answer which features are more important for various customer segments.

## Intended Usage

Users (Marketing analysts, bank management) could use this model to have their ROI values predicted. Users can fill up the numerical features like click rate, impression, etc. with their targets. They can also enter categorical features that contains their intended marketing strategy, like target customer segments and type of channels used. This way, the users are able to gauge if their targeted metrics and initial strategy can reap in a higher ROI.

## Possible solution

XGBoost is extremely efficient at handling multiple features and large datasets due to its gradient boosting algorithms, which can be a popular choice for banks, as they have access to much more customer data than any other business. This method is also considered a fairly modern technique. As some banks may feel that their vast amount of data is being under-utilised by older machine learning models, this XGBoost model ensures that large datasets can be used to train the model, and also develop more creative ROI predictions. As such, XGBoost offers a way for banks to use their data wisely.
