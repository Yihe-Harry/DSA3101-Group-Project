#pip install ucimlrepo (install to load data)
#pip install iterative-stratification (install for multilabel stratification)
#pip install bayesian-optimization (install for bayesian optimisation)

import pandas as pd
import numpy as np

from ucimlrepo import fetch_ucirepo
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from iterstrat.ml_stratifiers import MultilabelStratifiedKFold

import xgboost as xgb
import lightgbm as lgb

from lazypredict.Supervised import LazyClassifier 
from sklearn.metrics import roc_curve, accuracy_score, f1_score, roc_auc_score, average_precision_score
from bayes_opt import BayesianOptimization

from datapreparation import import_data, data_cleaning, data_split, label_split
from hyperparametertuning import get_lgb_opt_params, get_xgb_opt_params
from models import final_model

####################Data Preparation####################
df = import_data()
df = data_cleaning(df)
X_train, y_train, X_test, y_test = data_split(df)
hl_y_train, hl_y_test, pl_y_train, pl_y_test, td_y_train, td_y_test = label_split(y_train, y_test)

####################Hyperparameter Tuning####################
#hl_opt_params = get_lgb_opt_params(X_train, hl_y_train, init_round=10, opt_round=15, n_folds=5, random_seed=27,n_estimators=10000)
#pl_opt_params = get_xgb_opt_params(X_train, pl_y_train, 'personal_loan',init_round=5, opt_round=10, n_folds=3, random_seed=27,n_estimators=10000)
#td_opt_params = get_xgb_opt_params(X_train, td_y_train, 'term_deposit', init_round=5, opt_round=10, n_folds=3, random_seed=27,n_estimators=10000)

hl_opt_params = {'bagging_fraction': 0.5436036759336191,
                 'feature_fraction': 0.6350682445913682,
                 'lambda_l2': 0.7603696537169113,
                 'learning_rate': 0.08311636662252349,
                 'max_bin': 678,
                 'max_depth': 13,
                 'min_data_in_leaf': 11,
                 'min_sum_hessian_in_leaf': 0.013629501631003293,
                 'num_leaves': 85,
                 'objective': 'binary',
                 'metric': ['auc', 'aucpr', 'binary_error'],
                 'early_stopping_rounds': 50,
                 'random_state': 27}

pl_opt_params = {'colsample_bytree': 0.6281982507677273,
                 'gamma': 7.893772986546304,
                 'learning_rate': 0.15099355435566217,
                 'max_depth': 5,
                 'min_child_weight': 0.266886079288865,
                 'reg_alpha': 2.4504076812212494,
                 'reg_lambda': 7.6974043195909285,
                 'subsample': 0.8266454238259481,
                 'objective': 'binary:logistic',
                 'eval_metric': ['aucpr'],
                 'random_state': 27}

td_opt_params = {'colsample_bytree': 0.4157942248802582,
                 'gamma': 6.3755371156668526,
                 'learning_rate': 0.05582075825068678,
                 'max_depth': 13,
                 'min_child_weight': 4.415522445961107,
                 'reg_alpha': 6.740077939792876,
                 'reg_lambda': 2.394036323235528,
                 'subsample': 0.8215037183327571,
                 'objective': 'binary:logistic',
                 'eval_metric': ['aucpr'],
                 'random_state': 27}

####################Models####################

y_pred_prob, y_pred = final_model(X_train, y_train, X_test, y_test)
