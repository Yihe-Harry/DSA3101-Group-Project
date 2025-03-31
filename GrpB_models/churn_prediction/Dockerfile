FROM python:3.10

WORKDIR /GrpB_models/churn_prediction

COPY . /GrpB_models/churn_prediction

RUN pip install --no-cache-dir pandas joblib scikit-learn imbalanced-learn openpyxl xlrd


CMD ["python", "churn_mod_train.py"]
