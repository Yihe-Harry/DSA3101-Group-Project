FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir ucimlrepo iterative-stratification lazypredict bayesian-optimization pandas numpy scikit-learn lightgbm xgboost

CMD ["python", "main.py"]
