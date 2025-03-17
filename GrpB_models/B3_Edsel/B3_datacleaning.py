import pandas as pd
import numpy as np

# Read the CSV file
file_path = 'B3_Edsel/marketing_campaign_dataset.csv'


class DataCleaning:

    def __init__(self, file_path):
        self.file_path = file_path

    def clean_data(self):
        df = pd.read_csv(self.file_path)
        df = df.dropna()
        df = df.drop_duplicates()
        df = df.drop('Company', axis = 1) # Drop the 'Company' column
        df = df.drop('Location', axis = 1) # Drop the 'Location' column
        df = df.drop('Language', axis = 1) # Drop the 'Language' column
        df = df.drop('Customer_Segment', axis = 1) # Drop the 'Customer_Segment' column
        return df
    
    def add_weekdayweekend_to_date(self):
        df = self.clean_data()
        df['Date'] = pd.to_datetime(df['Date'])
        df["Day_Type"] = df["Date"].apply(lambda x: "Weekend" if x.weekday() >= 5 else "Weekday")
        return df

#print(DataCleaning(file_path).add_weekdayweekend_to_date())