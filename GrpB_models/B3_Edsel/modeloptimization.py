from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
from GrpB_models.B3_Edsel.model import XGBoostModel  # Import your model class


class XGBoostOptimizer:
        
    def __init__(self, file_path, max_evals=50):
        self.file_path = file_path
        self.max_evals = max_evals
        self.model = XGBoostModel(file_path)
        self.X_train, self.X_test, self.y_train, self.y_test = self.model.traintestsplit()

    def objective(self, params):
        params['max_depth'] = int(params['max_depth'])  # Convert max_depth to int
        params['n_estimators'] = int(params['n_estimators'])
        
        dtrain = xgb.DMatrix(self.X_train, label=self.y_train, enable_categorical=True)
        dtest = xgb.DMatrix(self.X_test, label=self.y_test, enable_categorical=True)
        
        model = xgb.train(
            params, dtrain, num_boost_round=1000,
            evals=[(dtrain, 'train'), (dtest, 'test')],
            early_stopping_rounds=20, verbose_eval=50 #maybe change to 50
        )
        
        y_pred = model.predict(dtest)
        mse = mean_squared_error(self.y_test, y_pred)
        
        return {'loss': mse, 'status': STATUS_OK}
    
    def optimize(self):
        space = {
            'learning_rate': hp.uniform('learning_rate', 0.001, 0.1),
            'max_depth': hp.quniform('max_depth', 3, 15, 1),
            'n_estimators': hp.quniform('n_estimators', 100, 2000, 10),
            'colsample_bytree': hp.uniform('colsample_bytree', 0.5, 1),
            'subsample': hp.uniform('subsample', 0, 1),
            'alpha': hp.uniform('alpha', 0, 10),
            'lambda': hp.uniform('lambda', 0, 10),
            'gamma': hp.uniform('gamma', 0, 10),
            'min_child_weight': hp.uniform('min_child_weight', 1, 15)
        }
        
        trials = Trials()
        best_params = fmin(fn=self.objective, space=space, algo=tpe.suggest, max_evals=self.max_evals, trials=trials)
        
        print("Best Hyperparameters:", best_params)
        return best_params




# Run optimization
if __name__ == "__main__":
    optimizer = XGBoostOptimizer('GrpB_models/B3_Edsel/marketing_campaign_dataset.csv', max_evals=50)
    best_params = optimizer.optimize()

#Best Hyperparameters: {'alpha': 7.006597027901627, 
# 'colsample_bytree': 0.6929304873945399, 
# 'gamma': 2.88294917603643, 
# 'lambda': 9.379355978740126, 
# 'learning_rate': 0.017638483192002327, 
# 'max_depth': 4.0, 
# 'min_child_weight': 4.481549741741674, 
# 'n_estimators': 360.0, 
# 'subsample': 0.37518827341965655}
        
