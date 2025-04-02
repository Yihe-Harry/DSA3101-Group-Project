FROM python:3.10

WORKDIR /GrpB_models/b3_measuring_campaign_roi

COPY . /GrpB_models/b3_measuring_campaign_roi

RUN pip install --no-cache-dir  pandas numpy holidays scikit-learn matplotlib xgboost hyperopt joblib

CMD ["python", "main.py"]