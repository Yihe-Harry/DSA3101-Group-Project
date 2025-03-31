

# Use a slim Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements file
COPY . /app


# Install dependencies
RUN pip install streamlit pandas

# Expose the port Streamlit will run on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "real_time_campaign_optimisation_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]