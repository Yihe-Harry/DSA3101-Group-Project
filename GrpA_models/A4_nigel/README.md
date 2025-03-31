# Overview
This folder contains the framework we have developed to measure the success of marketing campaigns. It contains the following:
1. A README.md file (this file) which provides a description and explanations of our framework
2. A Jupyter Notebook containing the code used to calculate metrics and KPIs

This README.md file contains the following sections:
1. Introduction
2. Breakdown
3. Conclusion

# 1) Introduction 

For question A4, the objective is to develop a framework for measuring campaign success using data such as engagement rate, conversion rate and customer lifetime value. We will then be able to propose actionable insights on how to improve marketing strategies. An assumption we made is that what is considered 'good' or 'bad' would be different, depending on the identity of the bank. A larger bank which can afford to allocate a large amount of funds towards marketing can expect greater results as compared to a smaller bank with not as much funds. While it may be useful to compare with industry benchmarks, it is also important to compare KPIs with past campaigns done by our bank, to gain an idea of marketing performance relative to what is expected for our bank.

The marketing funnel consists of four key stages: Awareness, Consideration, Conversion, and Loyalty. Within our framework, marketing campaigns will be categorized into one of these stages. Customers typically progress through these stages sequentially, and weak performance at any stage can negatively impact the subsequent stages, making it crucial to ensure each stage functions effectively without leakages. Since each stage serves a distinct purpose, it is essential to evaluate campaigns based on their specific objectives.

# 2) Breakdown
This section contains an indepth analysis of each of the 4 stages in our framework. The code snippet provided under each KPI demonstrates a possible method for calculating the metric using the available data from the bank.

## Awareness
Awareness is the first stage of the marketing funnel. In this stage, the bank aims to capture the attention of people, build brand and product recognition, and project a positive image. By presenting itself as an option for potential customers, it increases the chances for consumer action down the line. For Awareness marketing campaigns, the aim is maximise reach and visibility, improve brand awareness, as well as create a positive perception for customers. Examples of awareness campaigns would be influencer posts and posters at MRT stations.

The success of Awareness campaigns should be evaluated based on reach,visibility, brand awareness and brand image. Reach, visibility and to an extent brand awareness can be measured more objectively while brand image is alot more subjective. As such, the KPIs we look at would be more focused on the first 3.

### KPIs
#### 1) Ad Views/Impressions - This measures ad traffic, or the number of people that have seen the campaign ads. Defined as number of people who viewed the ad
##### Actionable Insight: If ad views/impressions are low, it is an indicator that the campaign is not reaching enough people. This could suggest the need for broader targeting or increasing the budget to enhance the ad’s reach. 

#### 2) Website/Social media page Views/Impressions  - This measures the number of people that have visited the website or social media page. Defined as number of people who viewed the bank's website or social media page
##### Actionable Insight: This is an indicator of both reach and brand awareness. If this number is low but Ad Views/Impressions are high, it typically indicates that the ad does not resonate or capture the attention of the audience . This could suggest a need to change the ad design and content or to assess whether the platform used is suitable for the bank's target audience.

#### 3) Click through rate(CTR) (for online ads) - Measures the percentage of people who click on an ad after seeing it. Similar to 2), it is an indicator of how well the ad resonates with or captures the audiences' attention. Defined as

$$
f(\text{Click Through Rate}) = \left( \frac{\text{Number of Clicks}}{\text{Number of Impressions}} \right) \times 100, \text{ where}
$$

* **Number of Clicks** refers to the number of people who clicked on the ad.
* **Number of Impressions** refers to the number of people who viewed the ad.
##### Actionable Insight: A low CTR would suggest a need to change the ad design and content or to assess whether the platform used is suitable for the bank's target audience.

#### 4) Branded Search Volume - Measures brand awareness and interest. It is the number of times the bank or keywords related to the bank are searched for on a search engine, like Google, over a certain period. Defined as 

$$
f(\text{Branded Search Volume}) = \left( \frac{\text{Number of searches}}{\text{Number of Days}} \right) , \text{ where}
$$

* **Number of Searches** refers to the total number of searches containing Bank name or products on search engines
* **Number of Days** refers to the number of days contained in time the time period we are interested in
##### Actionable Insight:  A low number suggests low awareness and interest in the bank and may indicate that the awareness campaign has not been as effective in generating interest or making the brand memorable. If branded search volume is low, it could signal that the campaign is not reaching the right audience or is not leaving a strong enough impression for people to actively seek out the brand after encountering the ad. This could suggest a need to change the ad design and content or to assess whether the platform used is suitable for the bank's target audience. If the search volume is low, it could also be a sign of inconsistent messaging. Ensuring that the bank's branding is coherent across all channels—whether social media, YouTube ads, or influencer posts—will help reinforce the brand's identity, making it more likely for customers to search for it later.

#### 5) Social media mentions - comments on social media platforms mentioning the bank. This measures brand image and the publics' sentiment towards banks.
##### Actionable Insight:  If comments are largely negative, it is an indicator that the bank has a poor reputation, and rebranding may be necessary to change perspectives. It may also be helpful to reevaluate the bank's practices, products and services to find out the root cause.


## Consideration
Consideration is the second stage of the funnel. Awareness campaigns introduce potential customers to the bank and its products or services, while Consideration campaigns go a step further by encouraging them to actively evaluate our offerings In this stage, we want to allow customers to find out even more about our products and services, with hopes of increasing their interest, eventually leading to conversion. For Consideration marketing campaigns, the aim is to maximise customer engagement, and to push them towards conversion. These campaigns are generally more targeted as compared to Awareness campaigns. Examples of such campaigns would be targeted emails or Instagram ads directing them towards our hotline or website. 

The success of Consideration campaigns can be evaluated based on the level of customer engagement, while also taking into account cost related metric such as cost per lead to achieve a balance. From question A2, Customers with longer session durations, a history of loyalty, and more recent interactions were more likely to engage with marketing campaigns. This insights should be taken into account when coming up with KPIs and possible action steps.

### KPIs
#### 1)  Click through rate(CTR) (for online ads) - Measures the percentage of people who click on an ad after seeing it. Defined as

$$
f(\text{Click Through Rate}) = \left( \frac{\text{Number of Clicks}}{\text{Number of Impressions}} \right) \times 100, \text{ where}
$$

* **Number of Clicks** refers to the number of people who clicked on the ad.
* **Number of Impressions** refers to the number of people who viewed the ad.
##### Actionable Insight:  It is an indicator of how well the ad resonates with or captures the audiences' attention. A low CTR would suggest a need to change the ad design and content or to assess whether the platform used is suitable for the bank's target audience.

#### 2) Average Website Session Duration - average time spent on website by people who click on ads. This measures the level of engagement people have with the website. Defined as  

$$
f(\text{Average Website Session Duration}) = \left( \frac{\text{Total Time Spent on Website by All Users}}{\text{Number of Clicks}} \right), \text{ where}
$$

* **Total Time Spent on Website by All Users** refers to the cumulative time all users have spent on the website.  
* **Number of Clicks** refers to the total number of users who clicked on the ad.

##### Actionable Insight:  A longer time spent on the website is desirable as it generally indicates greater interest in the bank and its products and services. Moreover, customers with longer session durations are more likely to be responsive towards future marketing campaigns. As such, it would be beneficial to focus marketing efforts towards customers with longer website session duration. As clicking on ads or searching for the bank's website generally indicates a baseline level of interest in the bank, low website session duration numbers could suggest that the website is unappealing to audiences, which could indicate a need to improve the websites design or interface.

#### 3) Lead generation rate - Measures the rate in which leads are generated throughout a specific marketing campaign. Defined as

$$
f(\text{Lead generation rate}) = \left( \frac{\text{Total number of leads generated}}{\text{Duration of campaign}} \right), \text{ where}
$$

* **Total number of leads generated** refers to the number of people who indicated interest in the bank's products or services, either through filling in forms, signing up for newsletters, downloading product brochures or making inquiries etc.
* **Duration of campaign** refers to the total number of days in which the campaign took place.
##### Actionable insight: This metric can be used to assess both ads and the bank's website, along with other possible platforms such as email. A low rate could suggest that the messaging is not compelling enough, targeting is off, or that the process of accomplishing the desired action eg filling in form is too difficult/troublesome for audience. It may be a good idea to enhance user experience, improve on the ad messaging or adjust targeting strategies. One possible targeting strategy would be to target people who have responded to past marketing campaigns or people who have had recent interactions with the bank.

#### 4) Cost per lead(CPL)- Measures whether or not marketing strategy is cost effective. Defined as

$$
f(\text{Cost per Lead}) = \left( \frac{\text{Total cost of campaign}}{\text{Number of Leads generated}} \right), \text{ where}
$$
* **Total number of leads generated** refers to the number of people who indicated interest in the bank's products or services, either through filling in forms, signing up for newsletters, downloading product brochures or making inquiries etc.
* **Total Cost of Campaign** refers to the total amount spent by the bank over the course of the campaign.
##### Actionable insight:  It may be useful to compare CPL between channels to find the most cost efficient channel. More investment can be made towards these cost effective channels to maximise the number of leads generated while keeping cost low. If cost per lead is high, it could suggest that the messaging is not compelling enough, targeting is off, or that the process of accomplishing the desired action eg filling in form is too difficult/troublesome for audience. It may be a good idea to enhance user experience, improve on the ad messaging or adjust targeting strategies. One possible targeting strategy would be to target people who have responded to past marketing campaigns or people who have had recent interactions with the bank.


## Conversion
Conversion is the third stage of the funnel. In this stage, potential customers have already expressed interest in the bank's services and products. The goal now is to give them a final push towards our desired outcome - whether it be to get them to open an account with the bank or to sign up for a new credit card. For Conversion campaigns, the aim is of course to maximise conversions and conversion rate. Examples of such campaigns would be personal recommendations sent through email or direct phone calls from a bank representative.

The success of Conversion campaigns can be evaluated based on conversion and conversion rate, which should be weighed against cost metrics to achieve a balance, such that a high level of conversions are obtained without having to overspend. The average conversion rate differs across platforms and is affected by numerous other factors such as the reputation of the bank and the quality of products and servies offered. As there isnt really a formula for what the optimal balance should be, the bank may have to experiment with different levels of ad spending and rely on previous benchmarks to find the optimal balance of conversions,conversion rate and spending.

### KPIs
#### 1) Conversion rate - Measures the effectiveness of the campaign at converting visitors/leads into customers. Defined as 

$$
f(\text{Conversion Rate}) = \left( \frac{\text{Number of Conversions}}{\text{Number of Impressions}} \right) \times 100, \text{ where}
$$

* **Number of Conversions** refers to the number of people who take a desired action(sign up for credit card, open account with bank etc)
* **Number of Impressions** refers to the number of people who viewed the ad.
##### Actionable Insight: Comparing conversion rates across platforms and past campaigns can help the bank to identify and compare between better and poorer performing platforms and campaigns. They can take insights and seek to emulate features from well performing campaigns, while avoiding mistakes made in poorer performing campaigns. They can also do A/B testing with different features to find out what works and what does not work, allowing them to optimise campaigns in the future. Comparing between platforms can also help the bank to determine which platforms work better for their target audience. A low conversion rate on a specific platform could indicate a need to improve targeting strategies, and assess whether or not a platform is suitable for the target audience. Segmentation of customers also allow for more personalised marketing, which could improve conversion rates. Targeting higher intent users who have expressed more interest in previous stages or improving incentives could also help with improving conversion rates.

#### 2) Number of conversions - Refers to number of people who take a desired action(sign up for credit card, open account with bank etc).
##### Actionable Insight: A low number of conversions but a high conversion rate would suggest that reach needs to be improved. The bank can increase ad spending or explore new platforms to reach out to a larger audience. The bank should also consider improving on Awareness and Consideration campaigns to maximise lead generation. If both conversion rates and number of conversions are low, it would be better to improve conversion rates first, before deciding to increase the scale of campaigns, to avoid unneccessary and inefficient spending.

#### 3) Cost per conversion - Measures the efficiency of campaign and allows us to assess which platforms are the most cost efficient. Defined as
$$
f(\text{Cost per Conversion}) = \left( \frac{\text{Total cost of campaign}}{\text{Number of Conversions generated}} \right), \text{ where}
$$
* **Number of Conversions** refers to the number of people who take a desired action(sign up for credit card, open account with bank etc)
* **Total Cost of Campaign** refers to the total amount spent by the bank over the course of the campaign.
Again, there is no ideal standard for what cost per conversion should be. A high customer lifetime value(see A4_Loyalty) could also justify having a high cost per conversion, as each conversion results in a higher level of earnings for the bank. A high cost per conversion is often a result of low conversion rates, so it would be useful to look into that as well. This part would elaborate more on the case where conversion rate is not low, but cost per conversion is high.
##### Actionable Insight: Cost per conversion can be compared between platforms to assess the cost efficiency of each platform. If cost per conversion for a particular platform is too high, it might signal that the platform may not be suitable for the target audience. If there is significant overlap between users of different platforms, the bank could consider focusing their spending on one platform instead. A high cost per conversion could also signal a need to narrow the scope of target audience. A possible solution is to create more specific audience segments and use more personalised offers targeted towards each segment. A/B testing can also be done to identify areas in which cost can be reduced without much consequence to conversion rates and number of conversions.


## Loyalty
Loyalty is the final stage of the funnel. This stage involves only customers who have been or are currently with the bank now. In this stage, the aim is to keep them as customers, and prevent them from switching banks. For Loyalty campaigns, we want to maintain customer satisfaction and retention, minimise churn rates, as well as maximise customer lifetime value. Examples of such campaigns would be loyalty programs and personalised customer service. 

The success of Loyalty campaigns can be evaluated based on the level of customer retention as well as the lifetime value provided by each customer.

### KPIs
#### 1)Churn Rate -  Measures the percentage of the bank's customers that stop engaging with the bank during the time period. It allows the bank to determine how well they are retaining their customers and is an indicator of customer loyalty and satisfaction. Defined as 

$$
f(\text{Churn Rate}) = \left( \frac{\text{Customers Lost}}{\text{Total Customers at Start of Period}} \right) \times 100
$$

* **Customers Lost ** refers to the number of customers who stopped engaging with the bank during the time period.  
* **Total Customers at Start of Period** refers to the number of customers with the bank at the beginning of the period.
##### Actionable Insight: A high churn rate may suggest that the bank may not be successfully maintaining relationships with customers or maintaining customer satisfaction. The bank may want to look into ways to strengthen their relationships with customers. Examples include loyalty programs and improved customer service. It may be a good idea for the bank to collect feedback from customers via surveys or direct conversations, in order to find out what might be causing customers to feel dissatisfied. Another reason for a high churn rate is that the bank's products and services may be inferior compared to other banks. It is important to conduct regular competitor analyses to ensure quality and pricing of products and services remain competitive in the market. Customer segmentation and increased personalisation in marketing may help the bank address specific needs of customers which can lead to greater customer satisfaction.

#### 2)Active Engagement Rate(for loyalty programs) - Measures how well loyalty programs resonate with customers or meet their needs. Defined as 

$$
f(\text{Active Engagement Rate}) = \left( \frac{\text{Number of Active Customers}}{\text{Total Participants Enrolled in Loyalty Program}} \right) \times 100
$$

* **Number of Active Customers** refers to customers who engage with the loyalty program by earning points, redeeming rewards, etc.  
* **Total Participants Enrolled in Loyalty Program** refers to all customers who have signed up for the loyalty program over a given time period.
##### Actionable Insight: A low active engagement rate indicates that customers enrolled in loyalty programs are not actively participating in programs. It could suggest a need to improve the level of rewards to incentivise particpation. This could increase spending. A high customer lifetime value could justify increased spending on loyalty programs. Another possible action could be to look into the process to earn or redeem rewards. An overly complicated process could deter customers from participating due to lack of patience or interest. Customer segmentation can personalisation can be incorporated into loyalty programs to align more accurately with customer needs and preferences, which could incentivise engagement.

#### 3)Customer Lifetime Value (CLV) - Estimates the total profit the bank can expect from each customer over their relationship with the bank. Defined as  

$$
f(\text{Customer Lifetime Value}) = \left( f(\text{Average Revenue per Customer}) \times f(\text{Average Customer Lifespan}) \right) - f(\text{Average Customer Acquisition Cost})
$$

where 

**Average Revenue per Customer** is calculated as:  

   $$
   f(\text{Average Revenue per Customer}) = \frac{\text{Total Revenue from customers}}{\text{Total number of Customers}}
   $$

**Average Customer Lifespan** is calculated as:  

   $$
   f(\text{Average Customer Lifespan}) = \frac{\sum{\text{Customer Lifespan (in years)}}}{\text{Total number of Customers}}
   $$

**Average Customer Acquisition Cost** is calculated as:  

   $$
   f(\text{Average Customer Acquisition Cost}) = \frac{\text{Total Marketing and Sales Expenses across first 3 stages}}{\text{Total number of New Customers Acquired}}
   $$



##### Actionable Insight: This metric helps the bank to determine how much they can afford to spend for customer acquisition and retention. Aside from that, a low customer lifetime value suggests that the bank is not maximising what they are getting out of each customer. Looking into each of the 3 factors(Average Revenue, Average Customer Lifespan, Average Customer Acquisition Cost) in CLV may offer a more in depth insight on which aspects require improvements. For low average revenue, the bank can look into ways to increase the value they provide to each customer, such as offering additional services, upselling, or cross-selling products. For a low average customer lifespan, the bank can look into improving customer retention by enhancing customer satisfaction, improving loyalty programs, or offering personalized experiences to encourage long-term relationships. Lastly, if the customer acquisition cost (CAC) is high, the bank can look into reducing spending on marketing campaigns, or improving the efficiency of marketing strategies in the previous three stages.


# 3) Conclusion
In conclusion, when evaluating a marketing campaign's success, it is important to keep in mind the objective of the marketing campaign. Different marketing campaigns have different goals, such as improving brand recognition and awareness or getting customers to buy a product. As such, we should avoid a one-size-fits-all approach but rather adapt our evaluation KPIs accordingly. By breaking down our marketing campaigns into the 4 stages specified above, we can more directly pinpoint weaknesses and areas of improvement. This will enable us to more efficiently utilise the resources allocated towards marketing, ultimately helping the bank cut unnecessary costs and increase ROI and profitability.
