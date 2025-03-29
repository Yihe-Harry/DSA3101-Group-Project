#pip install bayesian-optimization (install for bayesian optimisation)
from datapreparation import import_data, data_cleaning, data_split, label_split
import xgboost as xgb
import lightgbm as lgb
from bayes_opt import BayesianOptimization

def bayes_parameter_opt_lgb(X, y, init_round=15, opt_round=25, n_folds=3, random_seed=27,n_estimators=10000, output_process=False):
    train_data = lgb.Dataset(data=X_train, label=y, free_raw_data=False)
    
    def lgb_eval(learning_rate,num_leaves, feature_fraction, bagging_fraction, max_depth, max_bin, min_data_in_leaf, min_sum_hessian_in_leaf, lambda_l2):
        params = {
            'application':'binary',
            'metric':'auc',
            'learning_rate' : max(min(learning_rate, 1), 0), #efficient convergence
            "num_leaves" : int(round(num_leaves)), #controls complexity
            'feature_fraction' : max(min(feature_fraction, 1), 0), #dropout for feature
            'bagging_fraction' : max(min(bagging_fraction, 1), 0), #dropout for data
            'max_depth' : int(round(max_depth)), #prevent overfitting
            'max_bin' : int(round(max_bin)), #controls bin for continuous variables
            'min_data_in_leaf' : int(round(min_data_in_leaf)), #prevent overfitting
            'min_sum_hessian_in_leaf' : min_sum_hessian_in_leaf, #control complexity
            'lambda_l2' : lambda_l2, #regularisation for overfitting
            'verbose' : -1 #mute message
        }

        cv_result = lgb.cv(params, train_data, nfold=n_folds, seed=random_seed, stratified=True, metrics=['auc'])
        return max(cv_result['valid auc-mean'])
     
    lgbBO = BayesianOptimization(lgb_eval, {'learning_rate': (0.001, 0.7),
                                            'num_leaves': (5, 100),
                                            'feature_fraction': (0.1, 1),
                                            'bagging_fraction': (0.1, 1),
                                            'max_depth': (3, 20),
                                            'max_bin':(50,700),
                                            'min_data_in_leaf': (5,70),
                                            'min_sum_hessian_in_leaf':(0,1),
                                            'lambda_l2':(0,10)}, 
                                            random_state=27)
    
    lgbBO.maximize(init_points=init_round, n_iter=opt_round)
    
    model_auc=[]
    for model in range(len( lgbBO.res)):
        model_auc.append(lgbBO.res[model]['target'])
        
    print(f"Validation AUROC:{lgbBO.res[pd.Series(model_auc).idxmax()]['target']:.5f} ")
    return lgbBO.res[pd.Series(model_auc).idxmax()]['params']

def get_lgb_opt_params(X, y, init_round=15, opt_round=25, n_folds=3, random_seed=27,n_estimators=10000, output_process=False):
    opt_params=bayes_parameter_opt_lgb(X, y, init_round, opt_round, n_folds, random_seed,n_estimators, output_process)
    opt_params["num_leaves"] = int(round(opt_params["num_leaves"]))
    opt_params['max_depth'] = int(round(opt_params['max_depth']))
    opt_params['min_data_in_leaf'] = int(round(opt_params['min_data_in_leaf']))
    opt_params['max_bin'] = int(round(opt_params['max_bin']))
    opt_params['objective'] = 'binary'
    opt_params['metric'] = ['auc','aucpr', 'binary_error']
    opt_params['early_stopping_rounds'] = 50
    opt_params['random_state'] = 27
    return opt_params

def bayes_parameter_opt_xgb(X, y, label, init_round=15, opt_round=25, n_folds=3, random_seed=27,n_estimators=10000, output_process=False):
    train_data = xgb.DMatrix(X, label=y)
    
    def xgb_eval(learning_rate, max_depth, subsample, colsample_bytree, reg_lambda, reg_alpha, min_child_weight, gamma):
        params = {
            'objective': 'binary:logistic',
            'eval_metric': 'aucpr',  
            'learning_rate': max(min(learning_rate, 1), 0), #efficient convergence
            'max_depth': int(round(max_depth)), #prevent overfitting
            'subsample': max(min(subsample, 1), 0), #prevent overfitting
            'colsample_bytree': max(min(colsample_bytree, 1), 0), #prevent overfitting
            'reg_lambda': max(reg_lambda, 0), #l2 regularisation for complexity
            'reg_alpha': max(reg_alpha, 0), #l1 regularisation for complexity
            'min_child_weight': max(min_child_weight, 0), #control complexity
            'gamma': max(gamma, 0), #control complexity
            'verbosity': 1, #mute message
            'scale_pos_weight':len(df[df[label] == 0]) / len(df[df[label] == 1]) #weight for imbalanced data
        }

        cv_result = xgb.cv(params, train_data, num_boost_round=n_estimators, nfold=n_folds, seed=random_seed, stratified=True)
        return max(cv_result['test-aucpr-mean'])
     
    xgbBO = BayesianOptimization(xgb_eval, {'learning_rate': (0.001, 0.7), 
                                            'max_depth': (3, 20), 
                                            'subsample': (0.1, 1.0),
                                            'colsample_bytree': (0.1, 1.0),
                                            'reg_lambda': (0, 10),
                                            'reg_alpha': (0, 10),
                                            'min_child_weight': (0, 10),
                                            'gamma': (0, 10)}, 
                                            random_state=27)
    
    xgbBO.maximize(init_points=init_round, n_iter=opt_round)
    
    model_auc=[]
    for model in range(len( xgbBO.res)):
        model_auc.append(xgbBO.res[model]['target'])
    
    print(f"Validation AUPRC:{xgbBO.res[pd.Series(model_auc).idxmax()]['target']:.5f} ")
    return xgbBO.res[pd.Series(model_auc).idxmax()]['params']

def get_xgb_opt_params(X, y, label, init_round=15, opt_round=25, n_folds=3, random_seed=27,n_estimators=10000, output_process=False):
    opt_params=bayes_parameter_opt_xgb(X, y, label, init_round, opt_round, n_folds, random_seed,n_estimators, output_process) 
    opt_params['max_depth'] = int(round(opt_params['max_depth']))
    opt_params['objective'] = 'binary:logistic'  
    opt_params['eval_metric'] = ['aucpr']
    opt_params['random_state'] = 27
    return opt_params
