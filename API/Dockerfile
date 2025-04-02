FROM python:3.9

WORKDIR /app

# Copy requirements file first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a script to run both Streamlit and Flask applications
RUN echo '#!/bin/bash\n\
python -m flask run --host=0.0.0.0 &\n\
streamlit run app.py --server.port=8501 --server.address=0.0.0.0\n'\
> /app/start.sh && chmod +x /app/start.sh

# Expose ports for both Flask (5000) and Streamlit (8501)
EXPOSE 5000 8501

# Run both applications
CMD ["/app/start.sh"]
