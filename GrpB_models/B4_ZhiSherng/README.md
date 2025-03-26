# Overview
This folder contains the relevant documents and explanations relating to Cost-Effectiveness of Campaigns. The folder contains the following:

1. A (file name, will finalise soon) that contains the architecture design of the model
2. A README.md file (this file) which contains the description and explanations for how the model works

This README.md file includes the following sections:

1. Introduction
2. Methodology and justification 
3. Conclusion

# 1) Introduction
This report outlines a data-driven approach to balancing personalisation and cost-effectiveness in bank marketing campaigns. The proposed framework integrates customer segmentation, predictive modeling, and constrained optimisation to determine the most efficient marketing spend while maximising customer response rates and Return on Investment (ROI). Additionally, the framework takes into account key concerns in the banking industry, including regulatory compliance, transparency, and the need for interpretable models to ensure responsible and ethical marketing practices.



# 2) Methodology and justification
## 2.1) Approach
### Step 1: Customer Segmentation 

To better understand customer behaviour, segmentation is performed using the model from question A1. This groups customers based on demographics and transaction data, allowing for more precise targeting. By identifying distinct customer clusters, we can define clear marketing objectives for each group, ensuring campaigns focus on relevant goals, such as retention for high-value customers or conversion for low-engagement segments.

Segmentation also enables the use of more relevant ROI metrics when evaluating marketing effectiveness. Instead of applying generic KPIs, we can track Customer Lifetime Value (CLV) for high-value segments and Cost Per Successful Response (CPSR) for acquisition-focused groups. This approach improves response rate predictions, refines budget allocation, and ensures that marketing investments are efficiently distributed to maximise impact. By aligning marketing efforts with customer behaviour, segmentation enhances cost-effectiveness and overall campaign success.


### Step 2: Predicting Customer Response Probability
To predict the likelihood of a customer responding to a marketing campaign, a machine learning model, such as Random Forest or XGBoost, is trained using historical customer data and the current economic conditions. The objective is to generate a response probability score between 0 and 1, where values closer to 1 indicate a higher likelihood of engagement. The model utilises a diverse set of features to make accurate predictions:

1. Customer Attributes – Demographic and financial characteristics, such as age, income, credit score, and financial behaviour, help identify trends in customer responsiveness.
2. Past Response History – Analysing previous engagement with marketing campaigns enables the model to recognise patterns in how customers react to different outreach efforts.
3. Economic Indicators – External factors like inflation rates, interest rates, and economic stability can influence a customer’s financial behaviour and willingness to engage.
4. Transaction Data – Spending habits, savings patterns, and recent financial activities provide crucial signals about a customer's likelihood to respond to marketing efforts.

**Justification for the Chosen Approach**

XGBoost and Random Forest were chosen for their strong predictive power and ability to provide valuable insights into feature importance, making them well-suited for predicting customer responses. These models offer a balance between high performance and interpretability, which is crucial for actionable insights. On the other hand, neural networks were deliberately excluded due to their "black-box" nature, which complicates understanding of the reasons behind a customer’s predicted response.

Given the banking sector's need for transparency in decision-making, it is essential to understand which factors contribute to a customer's likelihood of responding to a marketing campaign. To aid this, techniques such as SHAP and Local Interpretable Model-agnostic Explanations (LIME) will be applied. These methods provide detailed insights into how different customer attributes—such as financial behaviour, transaction history, and engagement patterns influence response probabilities. By leveraging these explainability techniques, banks can ensure that marketing decisions are transparent, auditable, and aligned with ethical and regulatory expectations while also refining their strategies based on key drivers of customer engagement.


### Step 3: Determining Optimal Personalisation Level & Cost Estimation
A Bayesian Optimisation approach is employed to optimise the personalisation level while considering the associated costs. This allows for the dynamic adjustment of personalisation strategies, such as sending mass emails, targeted SMS messages, or personalised calls, based on the predicted response rates and costs. The goal is to determine the optimal personalisation level that balances high customer engagement with cost efficiency. The Bayesian Optimisation works as follow:

1. Objective Function Definition
The objective of the Bayesian optimisation process is to identify the personalisation level that maxims the expected response rate while minimizing the associated cost. The objective function can be defined as:

$$
f(\text{personalisation level}) = \text{expected response rate} - \text{cost per personalisation}, \text{ where}
$$

* response rate: Probability of a customer engaging with the marketing outreach (e.g., opening an account, subscribing to a service, applying for a loan)
* cost per personalisation: Expenses associated with different marketing strategies (e.g., automated emails, targeted SMS, personald calls)

2. Prior Distribution
At the outset, prior beliefs about customer behavior are based on historical data and domain knowledge. Examples of initial assumptions include:

*Mass Emails: Low-cost but lower response rates.
*Targeted SMS: Moderate cost with higher engagement for tech-savvy customers.
*Personalised Calls: High cost but effective for high-value customers.

These assumptions make up the prior distribution, which is refined as more data is collected.

3. Surrogate Model
Since directly evaluating the objective function is a costly process, Bayesian optimisation will use a Gaussian Process (GP) to approximate the relationship between personalisation levels, response rates, and costs. This surrogate model captures the uncertainty about how each personalisation method performs, allowing the optimisation process to be more efficient.

As data is collected through testing different personalisation levels, the surrogate model is updated to reflect the relationship between personalisation methods and their respective outcomes. For instance, the model may initially predict that personalised calls yield the highest response. However, after several iterations, it may learn that SMS reminders achieve similar engagement at a lower cost.

4. Acquisition Function
The acquisition function guides the optimisation process by suggesting the next personalisation level to evaluate. The acquisition function identifies the points in the personalisation space that are likely to yield the most improvement, balancing exploration of unknown areas with exploitation of known good options.

Common acquisition functions include:
*Expected Improvement (EI): Focuses on areas where improvement is likely based on the current surrogate model.
*Upper Confidence Bound (UCB): Balances the exploration of uncertain areas with the exploitation of the most promising solutions.

The acquisition function is key to optimizing the balance between personalisation and cost, ensuring that the optimisation process explores new personalisation levels while honing in on the most cost-effective options.

5. Iterative Optimiation Process
The optimisation begins by testing a few initial personalisation levels, typically chosen through random sampling or based on prior knowledge. Following each test, the observed response rate and associated cost are used to update the surrogate model. This iterative process allows the model to refine its predictions and progressively identify the optimal personalisation strategy.

With each iteration, the surrogate model gains confidence in the expected response rates and costs for each personalisation level. The acquisition function then selects the next personalisation strategy to evaluate, guiding the search toward increasingly optimal solutions.

6. Convergence and Optimisation
The process continues until convergence is reached, which occurs when the optimisation model has sufficiently explored the trade-off between personalisation and cost, identifying the most cost-effective personalisation level that maximises the expected response rate. At this point, the optimal level of personalisation has been determined.

Conclusion
By applying Bayesian optimisation, this approach dynamically adjusts the personalisation level for each customer segment based on both expected response rates and costs. The optimisation process ensures that marketing campaigns are both cost-efficient and highly personalised, leading to improved customer engagement and better overall campaign performance.

**Justification for the Chosen Approach**

Bayesian Optimisation is chosen to identify the most cost-effective personalisation strategy for each customer while dynamically adjusting engagement levels based on response probability and cost constraints. Although Reinforcement Learning (RL) could theoretically optimise personalisation in a dynamic manner, its lack of interpretability makes it unsuitable for financial applications where transparency is essential. Financial regulations and business decision-making processes require clear explanations of model outputs, making black-box optimisation approaches difficult to justify. By contrast, Bayesian Optimisation offers a structured, probabilistic method that effectively balances cost and response probability while ensuring transparency in decision-making.


### Step 4: Predicting ROI Metrics
To evaluate cost-effectiveness, additional models are used to predict key business metrics such as expected revenue per customer, Customer Lifetime Value (CLV), and cost per successful response. These predictions help quantify the financial impact of marketing efforts before optimisation, ensuring that marketing strategies align with business objectives.

**Justification for the Chosen Approach**

To measure the financial effectiveness of marketing campaigns, XGBoost is used to predict key ROI metrics, including Expected Revenue Uplift, CLV, and Cost per Successful Response. This model offers a strong balance between predictive accuracy and interpretability, allowing financial teams to audit and justify marketing investments. Since ROI models play a crucial role in corporate decision-making, they must provide clear and defensible justifications for financial forecasts to align with corporate reporting standards.

A key concern is ensuring that stakeholders understand how different factors contribute to ROI predictions. To address this, SHAP values are used to explain how various customer attributes influence the predicted financial outcomes. This approach enhances transparency, making the model’s outputs more interpretable for decision-makers and ensuring compliance with financial accountability requirements.


### Step 5: Constrained Budget Optimisation
To optimise marketing campaign budgets while ensuring high response rates and ROI, a variety of advanced optimisation techniques can be applied. These techniques address different levels of complexity in the relationships between campaign variables, objectives, and constraints. The goal is to allocate marketing resources efficiently across customer segments while adhering to budget constraints, customer fatigue limits, and regulatory compliance.

Nonlinear Programming
Nonlinear programming is an appropriate method when the relationships between variables are complex. This algorithm captures intricate interactions between customer behaviour, campaign spend, and engagement levels. It allows for more flexibility in modelling the optimisation process, ensuring that marketing strategies maximise both response rates and revenue uplift while staying within the prescribed budget. Nonlinear programming is ideal for scenarios where traditional linear models may fail to capture the complexity of the relationships between various marketing factors.

Quadratic Programming (QP)
When the relationships between variables are simpler but still not strictly linear, Quadratic Programming (QP) becomes a suitable choice. QP optimises the objective function where the interaction between variables is quadratic, such as when there are diminishing returns to marketing spend. It provides a simpler, more efficient solution compared to nonlinear methods, making it ideal for scenarios where a balance of complexity and computational efficiency is needed.

Constrained Multi-Objective Optimisation (CMO)
In cases where there are multiple competing objectives, such as balancing marketing spend across customer segments, Constrained Multi-Objective Optimisation (CMO) is highly effective. CMO can optimise several objectives simultaneously, such as maximising customer engagement while keeping within budgetary constraints. This approach ensures that trade-offs between different goals are made efficiently, allowing the bank to prioritise its marketing resources effectively.

Stochastic Optimisation
When there is significant uncertainty in the economic environment or in customer behaviour, Stochastic Optimisation offers a robust solution. By modelling uncertainties and variations in customer responses and market conditions, this technique allows for more flexible and adaptive marketing strategies. Stochastic optimisation helps ensure that the marketing campaign remains effective despite unpredictable changes in external factors, making it well-suited for volatile or uncertain conditions.

By applying these tailored optimisation algorithms, the bank can effectively allocate marketing resources, ensuring high response rates and a positive ROI while adhering to budget constraints, minimising customer fatigue, and maintaining regulatory compliance. Each algorithm offers a unique advantage based on the complexity of the relationships between marketing factors and the level of uncertainty present, making it possible to adapt the optimisation process to various business needs and environmental conditions.

**Justification for the Chosen Approach**

To optimise marketing campaign budgets while ensuring high response rates and ROI, the bank can leverage advanced optimisation techniques that consider the complexity of relationships between campaign variables, objectives, and constraints. These techniques are chosen with regulatory compliance, transparency, and ethical marketing practices in mind.

1. Nonlinear Programming
Nonlinear programming is ideal for modelling complex, non-linear relationships between marketing factors, such as the interaction between customer engagement and campaign spend. It captures nuances like diminishing returns on spend and saturation of engagement, which traditional models miss. Despite its complexity, it remains interpretable through techniques like sensitivity analysis, allowing the bank to ensure transparency and regulatory compliance. It also enables flexible optimisation within budget and regulatory constraints, promoting fairness and customer privacy.

2. Quadratic Programming (QP)
Quadratic programming is suitable for simpler, quadratic relationships, such as diminishing returns on marketing spend. It offers a more computationally efficient approach compared to nonlinear methods, making it practical for real-time optimisation. QP ensures transparency in decision-making, crucial for satisfying regulatory audits and demonstrating adherence to ethical standards. It efficiently balances marketing spend across customer segments while ensuring clear explanations of how budget allocations are made.

3. Constrained Multi-Objective Optimisation (CMO)
CMO is effective when multiple, sometimes conflicting, objectives must be balanced—such as maximising response rates, boosting engagement, and staying within budget. It ensures optimal allocation of resources while respecting constraints like customer fairness and legal limitations. CMO outputs are more interpretable, providing transparency into how different objectives are prioritised. This approach ensures the bank remains compliant with transparency and accountability regulations while optimising its marketing efforts.

4. Stochastic Optimisation
Stochastic optimisation is valuable in uncertain environments, where customer behaviour and external factors like economic conditions are unpredictable. It allows the bank to model uncertainty and dynamically adjust strategies to maintain engagement and ROI. By factoring in risk and external variations, stochastic optimisation supports responsible marketing, ensuring the bank stays within regulatory boundaries and avoids aggressive targeting or excessive contact in volatile conditions.

These optimisation models offer tailored solutions to balance marketing efficiency with regulatory compliance, transparency, and ethical marketing practices. Each model addresses the complexity of relationships and the level of uncertainty in different marketing scenarios, helping the bank allocate resources effectively while meeting industry standards and customer expectations.



# 4) Conclusion
The proposal ensures a balance between personalisation and cost management by implementing a structured, data-driven methodology that strategically optimises both factors. Here's how it achieves that balance:

Customer Segmentation: The proposal begins by segmenting customers based on demographics and transaction data. This ensures that marketing efforts are targeted precisely, avoiding waste on customers less likely to engage. By aligning marketing goals with different customer clusters (e.g., retention for high-value customers, conversion for low-engagement customers), the proposal allows for personalised campaigns that are more likely to resonate with each segment. This reduces the need for blanket campaigns that would be both expensive and ineffective, thus optimizing costs.

Predicting Customer Response: Machine learning models like Random Forest or XGBoost are used to predict the likelihood of a customer responding to marketing outreach. By predicting customer engagement probabilities, marketing resources can be allocated efficiently. Only customers with high response probabilities are targeted with more personalised and potentially higher-cost marketing tactics, like personalised calls. This minimises wasted expenditure on customers less likely to engage and helps focus the budget on those most likely to respond.

Optimizing Personalisation and Costs Using Bayesian Optimisation: Bayesian optimisation dynamically adjusts the level of personalisation based on predicted response rates and costs. By balancing the expected benefits of personalised approaches (like higher response rates) against the associated costs (like personalised calls or SMS), it identifies the most cost-effective strategies for each customer segment. This ensures that the marketing campaign remains cost-effective while still providing a high level of personalisation where it will have the most impact.

ROI Metrics and Budget Allocation: Predicting metrics like Customer Lifetime Value (CLV) and Cost Per Successful Response (CPSR) helps align marketing efforts with the bank's financial goals. The proposal focuses on using predictive models to determine which tactics will provide the highest returns on investment. By factoring in these metrics from the outset, marketing strategies are designed not only to engage customers effectively but also to ensure that spending is in line with the expected financial return. This allows for better budget allocation and avoids overspending on ineffective channels.

Advanced Optimisation Techniques for Budget Constraints: Nonlinear programming, quadratic programming, and constrained multi-objective optimisation are used to maximise marketing effectiveness while staying within budget limits. These techniques ensure that marketing resources are allocated efficiently, accounting for customer fatigue, regulatory constraints, and the diminishing returns of overspending on certain tactics. By applying these methods, the bank can maintain an optimal balance between personalisation and cost-efficiency, even as market conditions or customer behaviors change.

Scalability and Adaptability: The model is designed to be scalable, allowing for continuous adjustment and optimisation as more data is collected. This iterative process means that over time, personalisation strategies become more cost-efficient, as the system learns which strategies yield the highest engagement at the lowest cost. This adaptability ensures that the bank can continue to offer personalised marketing campaigns without escalating costs.

The proposal’s approach strikes a careful balance by using advanced data analysis and optimisation techniques to ensure that personalised marketing strategies are both effective and cost-efficient. By segmenting customers, predicting engagement, and applying dynamic optimisation, it minimises unnecessary costs while enhancing the effectiveness of personalised campaigns, leading to better engagement and higher ROI. This balance is key to ensuring that marketing remains sustainable and aligned with business objectives.


