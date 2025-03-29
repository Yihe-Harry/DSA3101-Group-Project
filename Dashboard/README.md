# Running the Dashboard with Docker

## Prerequisites

- Ensure Docker and Docker Compose are installed on your system.
- The dashboard uses Python 3.10 as specified in the Dockerfile.

## Build and Run Instructions
1. Navigate to the dashboard directory
   ```bash
   cd DSA3101-Group-Project/Dashboard
   ```
2. Build the Docker image :

   ```bash
   docker build -t my-streamlit-app .
   ```
3. Run the Docker image :

   ```bash
   docker run -p 8501:8501 my-streamlit-app
   ```
4. The application will be accessible at `http://localhost:8501`.

## Configuration

- The application exposes port `8501` as defined in the Docker Compose file.
- No additional environment variables are required for this setup.

## Notes

- The `default of credit card clients.xls` file is included in the project directory for data processing.

For further details, refer to the project documentation or contact the development team.

# Usage guide
## Home page

When you first open the dashboard, you will be greeted with a selection prompt. From the dropdown menu, choose the function you'd like to use. This will allow you to navigate to the corresponding feature and begin your analysis.

<p align="center">
  <img src="Images/dashboard%20home%20page.JPG" width="800">
</p>

## Function: CTR-Based 'Real-Time' Campaign Optimizer

## Function: Customer Churn Prediction
This function predicts whether a specific customer is likely to churn in the future. It utilizes two distinct models to generate accurate predictions:

1. Customer general data
   - Use this model if you have access to the customer's basic bank information, enter the required details and click 'Predict' to determine the likelihood of the customer churning.
![Model 1](Images/customer%20general%20data.JPG)
3. Customer credit card data.
   - Use this model if you have the customer's credit card payment information, enter the details and click 'Predict' to find out the likelihood of customer churn.
![Model 2](Images/customer%20cc%20data.JPG)

