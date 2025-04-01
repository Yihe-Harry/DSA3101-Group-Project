FROM python:3.10

WORKDIR /GrpB_models/b5_churn_prediction

COPY . /GrpB_models/b5_churn_prediction

RUN pip install --no-cache-dir pandas joblib scikit-learn imbalanced-learn openpyxl xlrd


CMD ["python", "churn_mod_train.py"]
