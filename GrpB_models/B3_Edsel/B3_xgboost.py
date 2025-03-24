import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from B3_datacleaning import DataCleaning
from B3_featureengineering import FeatureEngineering    


class XGBoostModel:

        def __init__(self, file_path):
            self.file_path = file_path

        def encode_categorical_features(self):
            df = FeatureEngineering(self.file_path).add_features()
            le = LabelEncoder()
            df['Day_Type'] = le.fit_transform(df['Day_Type'])
            df['Campaign_Type'] = le.fit_transform(df['Campaign_Type'])
            df['Target_Audience'] = le.fit_transform(df['Target_Audience'])
            df['Channel_Used'] = le.fit_transform(df['Channel_Used'])
            df['Is_Holiday'] = le.fit_transform(df['Is_Holiday'])
            print(df.dtypes)
            print(df.head())
            return df

        def traintestsplit(self):
            df = self.encode_categorical_features()
            X = df.drop(['ROI'], axis=1)
            y = df['ROI']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            return X_train, X_test, y_train, y_test
        
        def xgboostmodel(self):
            X_train, X_test, y_train, y_test = self.traintestsplit()

            # Define the model
            xg_reg = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000)

            # Define hyperparameters to tune
            param_grid = {
                'learning_rate': [0.01, 0.05, 0.1],
                'max_depth': [5, 7, 10],
                'n_estimators': [100, 200, 500],
                'colsample_bytree': [0.5, 0.7, 1],
                'subsample': [0.7, 0.8, 1],
                'alpha': [0, 1],
                'lambda': [0, 1]
            }

            # Set up GridSearchCV
            grid_search = GridSearchCV(estimator=xg_reg, param_grid=param_grid, scoring='neg_mean_squared_error', cv=3)
            grid_search.fit(X_train, y_train)
    
            # Get the best model
            best_model = grid_search.best_estimator_

            # Evaluate the model
            y_pred = best_model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            return mse, r2, grid_search.best_params_
        


print(XGBoostModel('GrpB_models\B3_Edsel\marketing_campaign_dataset.csv').xgboostmodel())

