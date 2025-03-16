import pandas as pd
from B3_datacleaning import DataCleaning

class FeatureEngineering:
    
        def __init__(self, file_path):
            self.file_path = file_path
    
        def add_weekdayweekend_to_date(self):
            df = DataCleaning(self.file_path).clean_data()
            df['Date'] = pd.to_datetime(df['Date'])
            df["Day_Type"] = df["Date"].apply(lambda x: "Weekend" if x.weekday() >= 5 else "Weekday")
            return df
        
        def add_features(self):
            df["CTR"] = df["Clicks"] / df["Impressions"]  # Click-Through Rate
            df["CPC"] = df["Spend"] / df["Clicks"]  # Cost Per Click
            df["Conversion Rate"] = df["Conversions"] / df["Clicks"]
            return df
