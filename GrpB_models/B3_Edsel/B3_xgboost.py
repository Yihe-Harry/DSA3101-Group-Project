import numpy as np
import pandas as pd
import xgboost as xgb
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from B3_datacleaning import DataCleaning
from B3_featureengineering import FeatureEngineering
import matplotlib.pyplot as plt


class XGBoostModel:

        def __init__(self, file_path):
            self.file_path = file_path

        def encode_categorical_features(self):
            df = FeatureEngineering(self.file_path).add_features()
            #le = LabelEncoder()
            #df['Day_Type'] = le.fit_transform(df['Day_Type'])
            #df['Campaign_Type'] = le.fit_transform(df['Campaign_Type'])
            #df['Target_Audience'] = le.fit_transform(df['Target_Audience'])
            #df['Channel_Used'] = le.fit_transform(df['Channel_Used'])
            #df['Is_Holiday'] = le.fit_transform(df['Is_Holiday'])
            categorical_cols = ['Day_Type', 'Campaign_Type', 'Target_Audience', 'Channel_Used', 'Is_Holiday']
            df[categorical_cols] = df[categorical_cols].astype('category')  # XGBoost handles categories natively
            df = df.drop('Day_Type', axis = 1)
            df = df.drop('Is_Holiday', axis = 1)
            df = df.drop('Channel_Used', axis = 1)
            df = df.drop('Duration', axis = 1)
            df = df.drop('Target_Audience', axis = 1)
            df = df.drop('Acquisition_Cost', axis = 1)
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
            dtrain = xgb.DMatrix(X_train, label=y_train, enable_categorical=True)
            dtest = xgb.DMatrix(X_test, label=y_test, enable_categorical=True)


            # Define hyperparameters to tune
            params = {
                'objective': 'reg:squarederror',
                'eval_metric': 'rmse',
                'learning_rate': 0.01,
                'max_depth': 10,
                'n_estimators': 1000,
                'colsample_bytree': 0.3,
                'subsample': 0.5,
                'alpha': 4,
                'lambda': 10,
                'tree_method': 'hist'  # Required for categorical handling
            }

            model = xgb.train(
            params, dtrain, num_boost_round=1000,
            evals=[(dtrain, 'train'), (dtest, 'test')],
            early_stopping_rounds=20, verbose_eval=50
            )

            # Predictions
            y_pred = model.predict(dtest)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            return mse, r2, model

model = XGBoostModel('GrpB_models/B3_Edsel/marketing_campaign_dataset.csv')
df = model.encode_categorical_features()
mse, r2, trained_model = model.xgboostmodel()
print(f'MSE: {mse}, R2: {r2}')

xgb.plot_importance(trained_model)
plt.show()