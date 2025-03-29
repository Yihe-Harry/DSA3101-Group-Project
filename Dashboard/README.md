# Running the Dashboard with Docker

## Prerequisites

- Ensure Docker and Docker Compose are installed on your system.
- The dashboard uses Python 3.10 as specified in the Dockerfile.

## Build and Run Instructions

1. Build the Docker image :

   ```bash
   docker build -t my-streamlit-app .
   ```
2. Run the Docker image :

   ```bash
   docker run -p 8501:8501 my-streamlit-app
   ```
3. The application will be accessible at `http://localhost:8501`.

## Configuration

- The application exposes port `8501` as defined in the Docker Compose file.
- No additional environment variables are required for this setup.

## Notes

- The `default of credit card clients.xls` file is included in the project directory for data processing.

For further details, refer to the project documentation or contact the development team.

# Usage guide
