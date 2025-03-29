# Running the Project with Docker

To run this project using Docker, follow the steps below:

## Prerequisites

- Ensure Docker and Docker Compose are installed on your system.
- The project uses Python 3.10 as specified in the Dockerfile.
- Ensure that your terminal's directory is in the API folder

## Build and Run Instructions

1. Build the Docker image :

   ```bash
   docker build -t customer-segmentation-api .
   ```
2. Run the Docker image :

   ```bash
   docker run -p 8000:8000 customer-segmentation-api
   ```
3. The application will be accessible at `http://localhost:8000/docs`.

## Configuration

- The application exposes port `8000` as defined in the Dockerfile
- No additional environment variables are required for this setup.

## Notes

- The `cleaned main dataset.csv` file is included in the project directory for data processing.

For further details, refer to the project documentation or contact the development team.


## API functions

1. ### fetch_cluster
Takes in a customer id and returns the customer segment and corresponding business strategy

#### Features
1. customer_id : int, range from 0 to 19999

#### Example output

"Cluster 0: High-Value Power Users , Business strategy: Upsell bank products to increase profits"

2. ### Predict cluster
Given customer attribute inputs, predicts in real time the customer segment belonging to the customer, 
returns the customer segment and corresponding business strategy. This is our real-time segmentation model using K-mean algorithm.

#### Features

1. age : int 
2. gender : int (Male=0, Female=1)
3. monthly_income : int
4. account_balance : int
5. loyalty_score : int (1-1000)
6. education_level : int (Primary=0 , Secondary=1 , Tertiary=2, Postgrad=3)
7. facebook_interaction : int (1= exposed to facebook ads at least once, 0 otherwise)
8. twitter_interaction : int (1= exposed to twitter ads at least once, 0 otherwise)
9. email_interaction : int (1= clicked email ads at least once, 0 otherwise)
10. instagram_interaction : int (1= exposed to instagram ads at least once, 0 otherwise)
11. total_withdrawal_amount : int  (sum across all transactions)
12. total_deposit_amount : int (sum across all transactions)
13. transaction_count : int  
14. has_loan : int (False=0, True=1)

#### Example output

"Cluster 0: High-Value Power Users , Business strategy: Upsell bank products to increase profits"