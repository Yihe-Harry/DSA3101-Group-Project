# 1. General analysis of product usage across all customers
df3['num_products_owned'] = df3['products owned'].apply(lambda x: len(x))

# Plot distribution of products owned across all customers
plt.figure(figsize=(8, 6))
sns.histplot(df3['num_products_owned'], kde= False, bins=5)
plt.title('Distribution of Products Owned Across All Customers')
plt.xlabel('Number of Products Owned')
plt.ylabel('Frequency')
plt.show()

# 2. General transaction history analysis (total deposits vs withdrawals)

# Filter out rows where 'transaction_history' is NaN or not a list
df3_cleaned = df3[df3['Transaction history'].apply(lambda x: isinstance(x, list))]

# Now we can safely explode the 'transaction_history' column
df3_transactions = df3_cleaned.explode('Transaction history')

# Check for NaN values and filter them out if necessary
df3_transactions = df3_transactions[df3_transactions['Transaction history'].notna()]

# Extract the 'amount', 'type', and 'value' from the transaction history
df3_transactions[['amount', 'type', 'value']] = pd.DataFrame(df3_transactions['Transaction history'].tolist(), index=df3_transactions.index)

# Calculate total deposits and withdrawals across all customers
transaction_summary = df3_transactions.groupby('type')['value'].sum()

# Plot total deposits vs withdrawals
transaction_summary.plot(kind='bar', figsize=(10, 6))
plt.title('Total Deposits vs Withdrawals Across All Customers')
plt.ylabel('Total Amount')
plt.show()

# 3. General analysis of digital engagement (Clicks, Impressions, and CTR)
# Handle None/NaN values in the ad engagement columns
df3['Facebook ad [clicks, impressions, CTR(Click thru rate)]'] = df3['Facebook ad [clicks, impressions, CTR(Click thru rate)]'].apply(lambda x: x if isinstance(x, list) else [0, 0, 0])
df3['Instagram ad [clicks, impressions, CTR(Click thru rate)]'] = df3['Instagram ad [clicks, impressions, CTR(Click thru rate)]'].apply(lambda x: x if isinstance(x, list) else [0, 0, 0])

# Extracting click-through rates for Facebook, Instagram, etc.
df3_ads = df3[['Facebook ad [clicks, impressions, CTR(Click thru rate)]',
               'Instagram ad [clicks, impressions, CTR(Click thru rate)]']]

# Convert columns into separate click data for analysis
df3_ads[['Facebook_clicks', 'Facebook_impressions', 'Facebook_CTR']] = pd.DataFrame(df3_ads['Facebook ad [clicks, impressions, CTR(Click thru rate)]'].to_list(), index=df3_ads.index)
df3_ads[['Instagram_clicks', 'Instagram_impressions', 'Instagram_CTR']] = pd.DataFrame(df3_ads['Instagram ad [clicks, impressions, CTR(Click thru rate)]'].to_list(), index=df3_ads.index)

# Calculate overall average CTR across all customers
engagement = df3_ads[['Facebook_CTR', 'Instagram_CTR']].mean()

# Plot the average CTR for Facebook and Instagram
engagement.plot(kind='bar', figsize=(10, 6))
plt.title('Average Click-Through Rate (CTR) Across Digital Platforms')
plt.ylabel('Average CTR')
plt.show()



purchase_counts = df3['has customer bought product'].value_counts()

# Plot the count of customers who bought a product vs those who did not
plt.figure(figsize=(8, 6))
purchase_counts.plot(kind='bar', color=['green', 'red'])
plt.title('Number of People Who Bought a Product vs Did Not')
plt.xlabel('Product Purchase Status')
plt.ylabel('Number of Customers')
plt.xticks(rotation=0)
plt.show()


transaction_history_counts = df3['Transaction history'].apply(lambda x: len(x) > 0).value_counts()

# Plot the count of customers who have transaction history vs those who do not
plt.figure(figsize=(8, 6))
transaction_history_counts.plot(kind='bar', color=['blue', 'orange'])
plt.title('Number of People with Transaction History vs No Transaction History')
plt.xlabel('Transaction History Status')
plt.ylabel('Number of Customers')
plt.xticks([0, 1], ['No Transaction History', 'Has Transaction History'], rotation=0)
plt.show()






# Print overall insights and recommendations:
print("General Analysis and Recommendations:")
print(f"\nAverage number of products owned across all customers: {df3['num_products_owned'].mean():.2f}")
print(f"Total deposits across all customers: {transaction_summary.get('Deposit', 0)}")
print(f"Total withdrawals across all customers: {transaction_summary.get('Withdrawal', 0)}")
