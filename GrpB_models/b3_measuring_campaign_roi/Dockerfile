FROM python:3.10

WORKDIR /GrpB_models/roi_prediction

COPY . /GrpB_models/roi_prediction 

RUN pip install --no-cache-dir  pandas numpy holidays scikit-learn matplotlib xgboost hyperopt joblib

CMD ["python", "main.py"]