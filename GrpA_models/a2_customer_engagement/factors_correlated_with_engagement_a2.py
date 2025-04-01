import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from scipy.stats import ttest_ind
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Loading data
telemarketing_data_a2 = pd.read_csv("bank_full_a2.csv", sep=";")
digitalmarketing_data_a2 = pd.read_csv("digital_marketing_campaign_dataset_a2.csv")



# Data Cleaning (Telemarketing)
# Encoding categorical variables
encoder_job_a2 = OneHotEncoder(drop='first', sparse_output=False)
encoder_marital_a2  = OneHotEncoder(drop='first', sparse_output=False)

job_encoded_a2 = encoder_job_a2.fit_transform(telemarketing_data_a2[['job']])
marital_encoded_a2 = encoder_marital_a2.fit_transform(telemarketing_data_a2[['marital']])

job_encoded_df_a2 = pd.DataFrame(job_encoded_a2, columns=encoder_job_a2.get_feature_names_out(['job']))
marital_encoded_df_a2 = pd.DataFrame(marital_encoded_a2, columns=encoder_marital_a2.get_feature_names_out(['marital']))

# Combining encoded columns with the original dataframe
telemarketing_data_a2 = telemarketing_data_a2.drop(['job', 'marital'], axis=1)
telemarketing_data_a2 = pd.concat([telemarketing_data_a2, job_encoded_df_a2, marital_encoded_df_a2], axis=1)

# Mutate categorical columns
telemarketing_data_a2['education'] = telemarketing_data_a2['education'].astype('category')
telemarketing_data_a2['default'] = telemarketing_data_a2['default'].astype('category')
telemarketing_data_a2['housing'] = telemarketing_data_a2['housing'].astype('category')
telemarketing_data_a2['loan'] = telemarketing_data_a2['loan'].astype('category')
telemarketing_data_a2['day'] = telemarketing_data_a2['day'].astype('category')
telemarketing_data_a2['month'] = telemarketing_data_a2['month'].astype('category')
telemarketing_data_a2['poutcome'] = telemarketing_data_a2['poutcome'].astype('category')

# Outcome encoding (y -> 1 or 0)
telemarketing_data_a2['outcome'] = telemarketing_data_a2['y'].apply(lambda x: 1 if x == 'yes' else 0)

# Remove rows with unknown contact type
telemarketing_data_a2 = telemarketing_data_a2[telemarketing_data_a2['contact'] != 'unknown']



correlation_matrix_a2 = telemarketing_data_a2[['age', 'balance', 'duration', 'campaign', 'pdays', 'previous', 'outcome']].corr()
correlation_plot_a2 = sns.heatmap(correlation_matrix_a2, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title('Correlation Heatmap for Numerical Variables')
plt.tight_layout()
# Store the correlation plot in a variable
correlation_plot_fig_a2 = plt.gcf()


# Plot: Density Plot for Duration vs Outcome
duration_plot = sns.kdeplot(data=telemarketing_data_a2, x='duration', hue='outcome', common_norm=False, fill=True)
plt.title('Density Plot for Duration vs Outcome')
plt.tight_layout()
duration_plot_fig = plt.gcf()


# Plot: Density Plot for Age vs Outcome
age_plot = sns.kdeplot(data=telemarketing_data_a2, x='age', hue='outcome', common_norm=False, fill=True)
plt.title('Density Plot for Age vs Outcome')
plt.tight_layout()
age_plot_fig = plt.gcf()



# Plot: Density Plot for Pdays vs Outcome
pdays_plot = sns.kdeplot(data=telemarketing_data_a2, x='pdays', hue='outcome', common_norm=False, fill=True)
plt.title('Density Plot for Pdays vs Outcome')
pdays_plot_fig = plt.gcf() 



telemarketing_data_a2['pdays_group'] = pd.cut(telemarketing_data_a2['pdays'],
                                      bins=[-float('inf'), 90, 180, float('inf')],
                                      labels=['Under 90 days', '90 to 180 days', 'Above 180 days'])

# Now, group by 'pdays_group' and summarize the data
pdays_distribution_a2 = telemarketing_data_a2.groupby('pdays_group', observed = False).agg(
    deposit=('outcome', lambda x: (x == 1).sum()),  # Sum where outcome is 1
    calls=('outcome', 'size'),  # Count of rows in each group
    percentage=('outcome', lambda x: ((x == 1).sum() / len(x)) * 100)  # Calculate percentage
).reset_index()







categorical_vars_tele_a2 = ['education', 'default', 'housing', 'loan', 'day', 'month', 'poutcome']
X_cat_tele_a2 = pd.get_dummies(telemarketing_data_a2[categorical_vars_tele_a2], drop_first=True)
y_cat_tele_a2 = telemarketing_data_a2['outcome'].astype(int)


logistic_model_a2 = LogisticRegression()
logistic_model_a2.fit(X_cat_tele_a2, y_cat_tele_a2)

# P-values of logistic regression
import statsmodels.api as sm
logit__tele_model = sm.Logit(y_cat_tele_a2, X_cat_tele_a2)
X_cat_a2 = sm.add_constant(X_cat_tele_a2)
logit_model_a2 = sm.Logit(y_cat_tele_a2, X_cat_tele_a2)
result_a2 = logit_model_a2.fit()
print(result_a2.summary())





percentage_deposit_per_month_a2 = telemarketing_data_a2.groupby('month', observed=False)['outcome'].mean()
# Calculate the total count of each outcome per month for visualization
outcome_counts_by_month_a2 = telemarketing_data_a2.groupby(['month', 'outcome'], observed=False).size().unstack(fill_value=0)

# Plot: Percentage Deposit Per Month with two colors for outcome (0 and 1)
month_plot_a2 = outcome_counts_by_month_a2.plot(kind='bar', stacked=True, color=['lightblue', 'orange'], figsize=(10, 6))
plt.title('Percentage Deposit Per Month')
plt.tight_layout()
# Store the month plot in a variable
month_plot_fig = plt.gcf()




percentage_deposit_by_poutcome_a2 = telemarketing_data_a2.groupby('poutcome', observed=False)['outcome'].mean()
# Calculate the total count of each outcome per month for visualization
outcome_counts_by_poutcome_a2 = telemarketing_data_a2.groupby(['poutcome', 'outcome'], observed=False).size().unstack(fill_value=0)

# Plot: Percentage Deposit Per Month with two colors for outcome (0 and 1)
poutcome_plot_a2 = outcome_counts_by_poutcome_a2.plot(kind='bar', stacked=True, color=['lightblue', 'orange'], figsize=(10, 6))
plt.title('Percentage Deposit by Previous Success')
plt.tight_layout()
# Store the month plot in a variable
month_plot_fig = plt.gcf() 


poutcome_distribution_a2 = telemarketing_data_a2.groupby('poutcome', observed = False).agg(
    deposit=('outcome', lambda x: (x == 1).sum()), 
    calls=('outcome', 'size'), 
    percentage=('outcome', lambda x: ((x == 1).sum() / len(x)) * 100) 
).reset_index()




percentage_deposit_by_housing_a2 = telemarketing_data_a2.groupby('housing', observed=False)['outcome'].mean()
# Calculate the total count of each outcome per month for visualization
outcome_counts_by_housing_a2 = telemarketing_data_a2.groupby(['housing', 'outcome'], observed=False).size().unstack(fill_value=0)

# Plot: Percentage Deposit Per Month with two colors for outcome (0 and 1)
housing_plot_a2 = outcome_counts_by_housing_a2.plot(kind='bar', stacked=True, color=['lightblue', 'orange'], figsize=(10, 6))
plt.title('Percentage Deposit by Housing Loans')
plt.tight_layout()
# Store the month plot in a variable
month_plot_fig = plt.gcf() 

housing_distribution_a2 = telemarketing_data_a2.groupby('housing', observed = False).agg(
    deposit=('outcome', lambda x: (x == 1).sum()), 
    calls=('outcome', 'size'), 
    percentage=('outcome', lambda x: ((x == 1).sum() / len(x)) * 100) 
).reset_index()





# Digital Marketing

numerical_correlation_digital_a2 = digitalmarketing_data_a2[['Age', 'Income', 'AdSpend', 'ClickThroughRate', 'ConversionRate', 
                                                 'WebsiteVisits', 'PagesPerVisit', 'TimeOnSite', 'SocialShares', 
                                                 'EmailOpens', 'EmailClicks', 'PreviousPurchases', 'LoyaltyPoints', 'Conversion']].corr()


corrplot_figure_digital_a2 = plt.figure(figsize=(10, 8))
sns.heatmap(numerical_correlation_digital_a2, annot=True, cmap="coolwarm", fmt='.2f')
plt.title('Correlation Matrix')

AdSpend_plot_figure_a2 = plt.figure()
sns.kdeplot(data=digitalmarketing_data_a2, x='AdSpend', hue='Conversion', fill=True, common_norm=False, linewidth=1.5)
plt.title('Density Plot of AdSpend by Conversion')


# Separate AdSpend by Conversion values
AdSpend_converted_a2 = digitalmarketing_data_a2[digitalmarketing_data_a2['Conversion'] == 1]['AdSpend']
AdSpend_not_converted_a2 = digitalmarketing_data_a2[digitalmarketing_data_a2['Conversion'] == 0]['AdSpend']

# T-test between converted and not converted groups for AdSpend
t_stat_adspend_a2, p_value_adspend_a2 = ttest_ind(AdSpend_converted_a2, AdSpend_not_converted_a2)
print(f"T-test result for AdSpend: t-stat = {t_stat_adspend_a2}, p-value = {p_value_adspend_a2}")





TimeOnSite_plot_figure_a2 = plt.figure()
sns.kdeplot(data=digitalmarketing_data_a2, x='TimeOnSite', hue='Conversion', fill=True, common_norm=False, linewidth=1.5)
plt.title('Density Plot of TimeOnSite by Conversion')


TimeOnSite_converted_a2 = digitalmarketing_data_a2[digitalmarketing_data_a2['Conversion'] == 1]['TimeOnSite']
TimeOnSite_not_converted_a2 = digitalmarketing_data_a2[digitalmarketing_data_a2['Conversion'] == 0]['TimeOnSite']

# T-test between converted and not converted groups for AdSpend
t_stat_TimeOnSite_a2, p_value_TimeOnSite_a2 = ttest_ind(TimeOnSite_converted_a2, TimeOnSite_not_converted_a2)
print(f"T-test result for AdSpend: t-stat = {t_stat_TimeOnSite_a2}, p-value = {p_value_TimeOnSite_a2}")



# Convert categorical variables to numerical using LabelEncoder
categorical_variables_digital_a2 = digitalmarketing_data_a2[['Gender', 'CampaignChannel', 'CampaignType', 'Conversion']]
categorical_variables_digital_a2['Gender'] = LabelEncoder().fit_transform(categorical_variables_digital_a2['Gender'])
categorical_variables_digital_a2['CampaignChannel'] = LabelEncoder().fit_transform(categorical_variables_digital_a2['CampaignChannel'])
categorical_variables_digital_a2['CampaignType'] = LabelEncoder().fit_transform(categorical_variables_digital_a2['CampaignType'])

# Logistic regression to find important categorical variables
X_digital_a2 = categorical_variables_digital_a2.drop(columns='Conversion')
y_digital_a2 = categorical_variables_digital_a2['Conversion']

logistic_model_digital_a2 = LogisticRegression()
logistic_model_digital_a2.fit(X_digital_a2, y_digital_a2)

# Get p-values
import statsmodels.api as sm
X_with_intercept_digital_a2 = sm.add_constant(X_digital_a2)  # Add intercept term
logistic_model_sm_digital_a2 = sm.Logit(y_digital_a2, X_with_intercept_digital_a2)
result_digital_a2 = logistic_model_sm_digital_a2.fit()

# Display p-values
p_values_digital_a2 = result_digital_a2.pvalues
sorted_p_values_digital_a2 = p_values_digital_a2.sort_values()
lowest_5_p_values_digital_a2 = sorted_p_values_digital_a2.head(5)
print("Lowest 5 p-values:", lowest_5_p_values_digital_a2)
