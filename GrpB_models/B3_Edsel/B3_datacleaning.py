import pandas as pd
import numpy as np

# Read the CSV file
file_path = 'GrpB_models\B3_Edsel\marketing_campaign_dataset.csv'


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
        df['Acquisition_Cost'] = df['Acquisition_Cost'].replace('[\$,]', '', regex=True).astype(float) # Remove the dollar sign from the 'Acquisition_Cost' column
        df['Date'] = pd.to_datetime(df['Date']) # Convert the 'Date' column to datetime

        return df
