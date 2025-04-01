
FROM python:3.10

WORKDIR /app

COPY GrpA_models/a3_behavioural_patterns /app/

RUN pip install --no-cache-dir pandas numpy scikit-learn seaborn matplotlib imbalanced-learn

CMD ["python", "behavioral_patterns_code.py"]
