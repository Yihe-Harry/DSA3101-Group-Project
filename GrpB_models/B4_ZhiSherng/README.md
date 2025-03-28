# Overview
This folder contains the relevant documents and explanations related to the Cost-Effectiveness of Campaigns. The folder contains the following:

1. A README.md file (this file) which provides a description and explanations of how the model works
2. A cost_effectiveness_model.drawio which contains the complete architecture design of the model, developed throughout the entire process
3. A cost_effectiveness_model.png which contains the final architecture design of the model

This README.md file includes the following sections:

1. Introduction
2. Methodology and Justification 
3. Conclusion

# 1) Introduction
This report outlines a data-driven approach to balancing personalisation and cost-effectiveness in bank marketing campaigns. The proposed framework integrates customer segmentation, predictive modeling and constrained optimisation to determine the most efficient marketing spend while maximising customer response rates and Return on Investment (ROI). Additionally, the framework takes into account key concerns in the banking industry, including regulatory compliance, transparency and the need for interpretable models to ensure responsible and ethical marketing practices.



# 2) Methodology and Justification
### Step 1: Customer Segmentation 

To better understand customer behaviour, segmentation is performed using the model from question A1. This groups customers based on demographics and transaction data, allowing for more precise targeting. By identifying distinct customer clusters, we can define clear marketing objectives for each group, ensuring campaigns focus on relevant goals such as retention for high-value customers or conversion for low-engagement segments.

Segmentation also enables the use of more relevant Key Performance Indicators (KPIs) when evaluating marketing effectiveness. Instead of applying generic KPIs, we can track conversion rate for Value-Driven Frequent Users and transaction frequency for Affluent Inactives. This approach improves response rate predictions, refines budget allocation and ensures that marketing investments are efficiently distributed to maximise impact. By aligning marketing efforts with customer behaviour, segmentation enhances cost-effectiveness and overall campaign success.


### Step 2: Predicting Customer Response Probability
To predict the likelihood of a customer responding to a marketing campaign, a machine learning model such as Random Forest or XGBoost is trained using historical customer data and the current economic conditions. The goal of the model is to generate a response probability score from 0 to 1, where 0 indicates that the customer will not respond and 1 indicates that the customer will respond. The model utilises a diverse set of features to make accurate predictions:

* Customer Attributes – Demographic and financial characteristics such as age, income, credit score and financial behaviour, help identify trends in customer responsiveness.
* Past Response History – Analysing previous engagement with marketing campaigns enables the model to recognise patterns in how customers react to different outreach efforts.
* Transaction Data – Spending habits, savings patterns and recent financial activities provide crucial insights about a customer's likelihood to respond to marketing efforts.
* Economic Indicators – Economic factors like inflation rates, interest rates and economic stability can influence a customer’s financial behaviour and willingness to engage.

**Justification for the Chosen Approach**

XGBoost and Random Forest were chosen for their strong predictive power and ability to provide valuable insights into feature importance, making them well-suited for predicting customer responses. These models offer a balance between high performance and interpretability which is crucial for actionable insights. On the other hand, neural networks were deliberately excluded due to their "black-box" nature which complicates understanding of the reasons behind a customer’s predicted response.

Given the banking sector's need for transparency in decision-making, it is essential to understand which factors contribute to a customer's likelihood of responding to a marketing campaign. To further aid this, techniques such as SHapley Additive exPlanations (SHAP) and Local Interpretable Model-agnostic Explanations (LIME) will be applied. These methods provide detailed insights into how different customer attributes such as financial behaviour, transaction history and engagement patterns influence response probabilities. By leveraging these techniques, banks can ensure that marketing decisions are transparent, auditable and aligned with ethical and regulatory expectations while also refining their strategies based on key drivers of customer engagement.


### Step 3: Determining Optimal Personalisation Level & Cost Estimation
A Bayesian Optimisation approach is employed to optimise the personalisation level while considering the associated costs. This allows for the dynamic adjustment of personalisation strategies based on the predicted response rates and costs, such as sending mass emails, targeted SMS messages or personalised calls. Bayesian Optimisation can also be employed to refine key parameters such as interest rates, loan terms or discount levels, tailoring them based on individual customer segments, behaviours and recent activity. The goal is to determine the optimal personalisation level that balances high customer engagement with cost efficiency. The Bayesian Optimisation works as follow:

1.&nbsp; Objective Function Definition

The objective of the Bayesian Optimisation process is to identify the personalisation level that maxims the expected response rate while minimising the related cost. The objective function can be defined as:

$$
f(\text{personalisation level}) = \text{expected response rate} - \text{cost per personalisation}, \text{ where}
$$

* response rate is the probability of a customer engaging with the respective marketing outreach (e.g., opening an account, subscribing to a service, applying for a loan)
* cost per personalisation refers to the expenses associated with different marketing strategies (e.g., automated emails, targeted SMS, personalised calls)

2.&nbsp; Prior Distribution

At the outset, prior beliefs about customer behaviour are based on historical data and domain knowledge. Examples of initial assumptions include:

* Mass Emails: Low-cost but lower response rates.
* Targeted SMS: Moderate cost with higher engagement for tech-savvy customers.
* Personalised Calls: High cost but effective for high-value customers.
* Interest rates: Assumptions about how different segments respond to varying loan interest rates.
* Loan terms: Initial beliefs on the most effective loan term offers for each customer segment considering factors like age, income and financial behaviour.
* Discount levels: Preliminary assumptions on discount strategies for customers based on purchasing patterns or loyalty.

These assumptions make up the prior distribution, which is refined as more data is collected.

3.&nbsp; Surrogate Model

Since evaluating the objective function directly is a costly process, Bayesian Optimisation will use a Gaussian Process (GP) to approximate the relationship between personalisation levels, response rates and costs. This surrogate model captures the uncertainty about how each personalisation method performs, allowing the optimisation process to be more efficient.

As data is collected through testing different personalisation levels, the surrogate model is updated to reflect the relationship between personalisation methods and their respective outcomes. For example, the model may initially predict that personalised calls yield the highest response. However, after several iterations, it may learn that SMS reminders achieve similar engagement at a lower cost.

4.&nbsp; Acquisition Function

The acquisition function guides the optimisation process by suggesting the next personalisation level to evaluate. It identifies the points in the personalisation space that are likely to yield the most improvement, balancing exploration of unknown areas with exploitation of known good options.

Common acquisition functions include:
* Expected Improvement (EI): Focuses on areas where improvement is likely based on the current surrogate model
* Upper Confidence Bound (UCB): Balances the exploration of uncertain areas with the exploitation of the most promising solutions

The acquisition function is essential to optimise the balance between personalisation and cost, ensuring that the optimisation process explores new personalisation levels while honing in on the most cost-effective options.

5.&nbsp; Iterative Optimiation Process

The optimisation begins by testing a few initial personalisation levels, typically chosen through random sampling or prior knowledge. Following each test, the observed response rate and associated cost are used to update the surrogate model. This iterative process allows the model to refine its predictions and progressively identify the optimal personalisation strategy.

Upon each iteration, the surrogate model gains confidence in the expected response rates and costs for each personalisation level. The acquisition function then selects the next personalisation strategy to evaluate, guiding the search towards increasingly optimal solutions.

6.&nbsp; Convergence and Optimisation

The process continues until convergence is reached, which occurs when the optimisation model has sufficiently explored the trade-off between personalisation and cost, identifying the most cost-effective personalisation level that maximises the expected response rate. At this point, the optimal level of personalisation has been determined.

By applying Bayesian Optimisation, this approach dynamically adjusts the personalisation level for each customer segment based on both expected response rates and costs. The optimisation process ensures that marketing campaigns are both cost-efficient and highly personalised, leading to improved customer engagement and better overall campaign performance.

**Justification for the Chosen Approach**

Bayesian Optimisation is chosen to identify the most cost-effective personalisation strategy for each customer while dynamically adjusting engagement levels based on response probability and cost constraints. Although reinforcement learning could theoretically optimise personalisation in a dynamic manner, its lack of interpretability makes it unsuitable for financial applications where transparency is essential. Financial regulations and business decision-making processes require clear explanations of model outputs, making black-box optimisation approaches difficult to justify. By contrast, Bayesian Optimisation offers a structured, probabilistic method that effectively balances cost and response probability while ensuring transparency in decision-making.


### Step 4: Predicting ROI Metrics
To evaluate cost-effectiveness, additional models are used to predict ROI metrics such as return on ad spend, customer acquisition cost and cost per successful response. These predictions help quantify the financial impact of marketing efforts before optimisation, ensuring that marketing strategies align with business objectives.

**Justification for the Chosen Approach**

XGBoost is used to predict key ROI metrics of marketing campaigns. This model offers a strong balance between predictive accuracy and interpretability, allowing financial teams to audit and justify marketing investments. Since ROI models play a crucial role in corporate decision-making, they must provide clear and defensible justifications for financial forecasts to align with corporate reporting standards.

A key concern is ensuring that stakeholders understand how different factors contribute to ROI predictions. To address this, SHAP values are used to explain how various customer attributes influence the predicted financial outcomes. This approach enhances transparency, making the model’s outputs more interpretable for decision-makers and ensuring compliance with financial accountability requirements.


### Step 5: Constrained Budget Optimisation
To optimise marketing campaign budgets while ensuring high response rates and ROI, a variety of advanced optimisation techniques can be applied. These techniques address different levels of complexity in the relationships between campaign variables, objectives and constraints. The goal is to allocate marketing resources efficiently across customer segments while adhering to budget constraints, customer fatigue limits and regulatory compliance.

Quadratic Programming (QP)

When the relationships between variables are relatively simple, Quadratic Programming (QP) is a suitable choice. QP optimises the objective function when there are diminishing returns to marketing spend. It provides a simpler and more efficient solution compared to nonlinear methods, making it ideal for scenarios where a balance of complexity and computational efficiency is needed.

Nonlinear Programming

Nonlinear Programming is an appropriate method when the relationships between variables are complex. This algorithm captures intricate interactions between customer behaviour, campaign spend and engagement levels. It allows for more flexibility in modelling the optimisation process, ensuring that marketing strategies maximise both response rates and revenue uplift while staying within the prescribed budget. Nonlinear Programming is ideal for scenarios where traditional linear models may fail to capture the complexity of the relationships between various marketing factors.

Constrained Multi-Objective Optimisation

In cases where there are multiple competing objectives such as balancing marketing spend across customer segments, Constrained Multi-Objective Optimisation (CMO) is highly effective. CMO can optimise several objectives simultaneously, such as maximising customer engagement and retention while keeping within budgetary constraints. This approach ensures that trade-offs between different goals are made efficiently, allowing the bank to prioritise its marketing resources effectively.

Stochastic Optimisation

When there is significant uncertainty in the economic environment or in customer behaviour, Stochastic Optimisation offers a robust solution. By modelling uncertainties and variations in customer responses and market conditions, this technique allows for more flexible and adaptive marketing strategies. Stochastic optimisation helps ensure that the marketing campaign remains effective despite unpredictable changes in external factors, making it well-suited for volatile or uncertain conditions.

By applying these tailored optimisation algorithms, the bank can effectively allocate marketing resources, ensuring high response rates and ROI while adhering to budget constraints, minimising customer fatigue and maintaining regulatory compliance. Each algorithm offers a unique advantage based on the complexity of the relationships between marketing factors and the level of uncertainty present, making it possible to adapt the optimisation process to various business needs and environmental conditions.

**Justification for the Chosen Approach**

To optimise marketing campaign budgets while ensuring high response rates and ROI, the bank can leverage advanced optimisation techniques that consider the complexity of relationships between campaign variables, objectives and constraints. These techniques are chosen with regulatory compliance, transparency and ethical marketing practices in mind.

Quadratic Programming

QP is suitable for simpler relationships such as diminishing returns on marketing spend. It offers a more computationally efficient approach compared to nonlinear methods, making it practical for real-time optimisation. QP ensures transparency in decision-making, crucial for satisfying regulatory audits and demonstrating adherence to ethical standards. It efficiently balances marketing spend across customer segments while ensuring clear explanations of how budget allocations are made.

Nonlinear Programming

Nonlinear Programming is ideal for modelling complex, non-linear relationships between marketing factors, such as the interaction between customer engagement and campaign spend. It captures nuances like diminishing returns on spend and saturation of engagement, which simpler models may miss. Despite its complexity, it remains interpretable through techniques like sensitivity analysis, allowing the bank to ensure transparency and regulatory compliance. It also enables flexible optimisation within budget and regulatory constraints, promoting fairness and customer privacy.

Constrained Multi-Objective Optimisation

CMO is effective when multiple, sometimes conflicting objectives must be balanced, such as maximising response rates, boosting engagement and staying within budget. It ensures optimal allocation of resources while respecting constraints like customer fairness and legal limitations. CMO outputs are more interpretable, providing transparency into how different objectives are prioritised. This approach ensures the bank remains compliant with transparency and accountability regulations while optimising its marketing efforts.

Stochastic Optimisation

Stochastic optimisation is valuable in uncertain environments, where customer behaviour and external factors like economic conditions are unpredictable. It allows the bank to model uncertainty and dynamically adjust strategies to maintain engagement and ROI. By factoring in risk and external variations, stochastic optimisation supports responsible marketing, ensuring the bank stays within regulatory boundaries and avoids aggressive targeting or excessive contact in volatile conditions.

These optimisation models offer tailored solutions to balance marketing efficiency with regulatory compliance, transparency and ethical marketing practices. Each model addresses the complexity of relationships and the level of uncertainty in different marketing scenarios, helping the bank allocate resources effectively while meeting industry standards and customer expectations.


### Step 6: Pilot Testing and Controlled Deployment

Before fully deploying the model to the entire customer base, the bank should first apply it to a small, controlled group of customers. This allows for a real-world test of the model’s effectiveness without exposing the entire customer segment to potential risks. During this pilot phase, the bank can closely monitor key metrics such as response rate, customer engagement and ROI to assess the model’s performance. This step helps identify any issues or unexpected outcomes that can be addressed before broader implementation. After evaluating the pilot results and making any necessary adjustments, the model can be gradually rolled out to larger segments, ensuring that the bank’s marketing efforts are both effective and cost-efficient.

### Step 7: Model Lifecycle Management

In order to ensure that the models remain effective over time, it’s essential to implement a Model Lifecycle Management strategy. This involves regular updates, retraining and evaluation of the model to keep it aligned with changing customer behaviour, market trends and new data sources. By continuously refining and adapting the model, businesses can maintain high levels of accuracy and effectiveness, optimising their marketing efforts for maximum impact and cost-efficiency.

To maintain the effectiveness of the model, it's crucial to use data that is no more than 2 years old, ensuring the model reflects the most current customer behaviours and market conditions. Regularly update the dataset to include new customer transactions and evolving demographic data. Additionally, periodically review and adjust the features used in the model to reflect any shifts in customer preferences or external factors, such as economic changes.

Models should be retrained every 6 months or sooner if there are significant shifts in customer behaviour or market conditions. Using a rolling window of data (such as the last 24 months) for training ensures the model stays relevant while avoiding overfitting to outdated patterns. Regular monitoring for concept drift can help trigger retraining when performance starts to degrade, ensuring that the model adapts to changing circumstances.

It is also essential to track key KPIs like response rates, conversion rates and ROI in real-time to monitor how well the model is performing. A/B testing can provide insights into whether a new model version outperforms the previous one. Regularly review model metrics like precision and accuracy and use interpretability tools like SHAP to ensure the model’s decisions remain transparent and aligned with business objectives.

As new data sources (e.g., social media, customer support interactions) become available, the bank should assess whether they should be incorporated into the model to improve its predictive power. Changes in customer behaviour may require recalibrating the model, adjusting features or integrating new data to reflect emerging patterns. A continuous feedback loop allows the model to evolve based on new insights, ensuring it stays aligned with current market conditions.

Effective Model Lifecycle Management ensures that marketing models remain relevant, accurate and adaptable to evolving conditions. By prioritising data freshness, regular retraining, continuous performance monitoring and the integration of new data sources, businesses can optimise their marketing strategies and achieve long-term success. This proactive approach ensures that marketing campaigns continue to drive high engagement and ROI while staying aligned with the latest customer trends and economic factors.

# 4) Conclusion
Balancing personalisation with cost-effectiveness in marketing campaigns is crucial for banks looking to maximise the impact of their marketing efforts while maintaining budget control. By leveraging AI techniques like customer segmentation, predictive modeling and Bayesian Optimisation, banks can ensure that their campaigns are not only personalised but also cost-efficient. 

Segmentation allows for precise targeting of customer groups, ensuring that marketing efforts deliver the right message to the right people. Predictive models enable the accurate forecasting of customer response probabilities, helping marketers allocate their efforts to the based on the predicted response probability of the customers. Furthermore, Bayesian Optimisation fine-tunes personalisation strategies, balancing customer engagement with the cost of delivering tailored messages.

The use of optimisation techniques such as Quadratic Programming, Nonlinear Programming and Stochastic Optimisation ensures that marketing budgets are allocated efficiently, even in the face of complex relationships and uncertainty. These methods enable banks to maintain the flexibility needed to adjust to market changes while ensuring that every marketing dollar is spent wisely. By continuously refining personalisation strategies and predicting ROI metrics, banks can maximise their marketing campaign's effectiveness, drive customer engagement and optimise spending. 

To ensure the ongoing success and relevance of AI-driven marketing models, banks must conduct pilot testing and implement effective model lifecycle management. Pilot testing allows for the real-world evaluation of the model on a small group of customers, helping identify potential issues before full deployment and refining the approach based on actual customer responses. Additionally, continuous model updates, including retraining with fresh data and regular performance monitoring, are crucial for adapting to changing market conditions and customer behaviours. By maintaining a robust lifecycle management process, banks can ensure that their AI models stay effective, cost-efficient and aligned with evolving marketing objectives, thereby maximising the long-term success of their personalised marketing campaigns. In this way, AI offers a comprehensive solution to balancing the twin objectives of personalisation and cost-effectiveness, ultimately leading to more successful and efficient marketing campaigns.

