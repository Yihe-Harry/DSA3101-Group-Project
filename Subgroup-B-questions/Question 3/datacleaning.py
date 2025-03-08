import pandas as pd
import numpy as np

# Read the CSV file
file_path = 'Subgroup-B-datasets/Edsel-data/marketing_campaign_dataset.csv'


class DataCleaning:

    def __init__(self, file_path):
        self.file_path = file_path

    def clean_data(self):
        df = pd.read_csv(self.file_path)
        df = df.dropna()
        df = df.drop_duplicates()
        df = df.drop('Company', axis = 1) # Drop the 'Company' column
        return df

print(DataCleaning(file_path).clean_data())