FROM python:3.10-slim

WORKDIR /API

# Install dependencies directly in the Dockerfile
RUN pip install --no-cache-dir \
    flask==2.0.1 \
    pandas==1.3.3 \
    numpy==1.21.2 \
    scikit-learn==1.0 \
    gunicorn==20.1.0

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run the application with host set to 0.0.0.0 to make it accessible outside container
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
