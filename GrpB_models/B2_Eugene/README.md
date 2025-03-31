# Running the Project with Docker

To run the **Real-Time Campaign Optimization** project using Docker, follow these steps:

## Prerequisites

- Ensure Docker and Docker Compose are installed on your system.
- The project requires Python 3.10 as specified in the Dockerfile.

## Build and Run Instructions

1. Build the Docker image:
   ```bash
   docker build -t streamlit-ctr-app .
   ```
2. Start the container:
   ```bash
   docker run -p 8501:8501 streamlit-ctr-app
   ```

## Configuration

- The application exposes port `8501` for the Streamlit interface. Ensure this port is available on your host machine.
- If required, create a `.env` file in the project root directory to specify environment variables.

## Additional Notes

For further details, refer to the provided Dockerfile.


## Code explanation

The main purpose of the code is to dynamically update the type of ads and offers being sent 
to each customer according to their degree of engagement with ads, measured by the Click-Through Rate (CTR).

### I will be making two assumptions: 
- A higher CTR (i.e. engagement rate) indicates higher interest in purchasing the product being advertised, and vice versa.
- A customer interested in purchasing a product will be equally interested in purchasing products deemed as substitutes or complements to the advertised product
### Reasons
- An explanation of the first assumption is that a high CTR reflects strong user intent or curiosity toward the product, signaling potential purchase interest.
- An explanation of the second assumption is that customers usually explore or purchase products due to its usefulness, and hence are often open to substitutes or upgrades that fulfill the same need or purpose. (E.g.
normal credit card vs premium credit card), or other products that are considered complements to the advertised product.


### Algorithm

1. We define upper engagement thresholds (CTR =40% and CTR=60%), and a lower engagement threshold (CTR=10%). The main product being advertised is a normal credit card. The higher the CTR, the higher volume of ads regarding substitutes/complements to normal credit card we will send.
2. If CTR on normal credit card ads exceed 40%, it is considered high interest, and we upsell by pushing advertisements on premium credit cards, since by assumption 1, the customer likely will be highly interested in premium credit cards as well.
3. Similarly, if CTR on normal credit card ads exceed 60%, we advertise both premium credit cards and loans.
4. If CTR on premium credit card ads exceed 40%, we advertise private banking services. If the CTR on said ads drops below 40%, we stop sending private banking service ads.
5. If CTR on loan ads exceed 40%, we advertise saving accounts. If the CTR on said ads drops below 40%, we stop sending saving accounts ads.
6. If CTR of normal credit card ads drop below 10%, since it is the main product being advertised, we stop sending all ads to the customer.
7. ** Note: The CTR rates used in the algorithm are quite inflated for convenience of showcase during the roadshow. The realistic upper engagement thresholds is approx. (CTR= 2% and CTR=3%),
lower threshold is (CTR=0.50%), considering the average CTR is around 1%




https://www.wordstream.com/blog/ws/2017/02/28/facebook-advertising-benchmarks  (Average CTR of Facebook ads is 0.90%)
https://firstpagesage.com/reports/clickthrough-rates-ctrs-by-industry/ (CTR of google ads range from 1% to 2%)