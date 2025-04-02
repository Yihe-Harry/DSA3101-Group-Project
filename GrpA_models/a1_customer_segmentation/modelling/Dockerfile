# Use Python 3.10 slim version
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything into the container
COPY . .

# Install required packages
RUN pip install pandas scikit-learn

# Run your actual script
CMD ["python", "data_model_kmeans.py"]
