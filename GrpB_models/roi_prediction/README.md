## ROI Prediction using XGBoost model

To tackle the task of ROI regression, this project proposes the use of XGBoost, particularly given the large dataset of 200,000 entries. Through the analysis conducted in the notebooks, XGBoost demonstrates superior flexibility and provides deeper insights into the key factors influencing ROI. One notable advantage is its feature importance plot, which effectively highlights the most influential variables, offering businesses and banks actionable insights on where to focus for future campaigns.

Compared to Random Forest, XGBoost excels due to its boosting mechanism, which sequentially corrects errors from previous iterations, leading to better predictive performance. Additionally, XGBoost is computationally more efficient due to its parallelized execution and optimized handling of missing values, making it a more scalable choice for large datasets like this one.

## Objective

This pre-trained XGBoost aims to predict ROI of bank marketing campaigns while minimising as little error as possible.

## Limitations and Challenges

Since the dataset is fictitious, it lacks real-world patterns and variability, making it difficult to generate realistic ROI predictions. Additionally, the 'Customer Segment' feature was dropped due to irrelevant segment names in the dataset. In order to tackle this challenge, banks can incorporate the customer segmentation models provided by Subgroup A and gather the customer segment that each campaign was targeted to. This allows banks to use personalised marketing strategies as a feature in this XGBoost model, and perhaps it could answer which features are more important for various customer segments.

Another limitation could be its root mean square error of 1.7

## Intended Usage

Users (Marketing analysts, bank management) could use this model to have their ROI values predicted. Banks could fill up the numerical features like click rate, impression, etc. with their targets. They can also enter categorical features that contains their intended marketing strategy, like target customer segments and type of channels used. This way, the users are able to gauge if their targeted metrics and initial strategy can reap in a higher ROI.

## What it hopes to solve

XGBoost is extremely efficient at handling multiple features and large datasets due to its gradient boosting algorithms, which can be a popular choice for banks, as they have access to much more customer data than any other business. This method is also considered a fairly modern technique. As some banks may feel that their vast amount of data is being under-utilised by older machine learning models, this XGBoost model ensures that large datasets can be used to train the model, and also develop more creative ROI predictions. As such, XGBoost offers a way for banks to use their data wisely.

## How to run

pip install -r requirements.txt
run main.py file to retrieve a model and save it.
model_optimization.py creates a dictionary of the best parameters for the model.