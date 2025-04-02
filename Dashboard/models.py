import pandas as pd
import numpy as np
import xgboost as xgb
import lightgbm as lgb
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import roc_curve, confusion_matrix, accuracy_score, f1_score, roc_auc_score, average_precision_score
from data_preparation import label_split

def get_biz_threshold(y_test, y_pred_prob, cost=1, profit=1): #profit is lost profit due to false negative customer and cost is cost of marketing to a false positive customer
    fpr, tpr, ths = roc_curve(y_test, y_pred_prob)
    fnr = 1 - tpr
    pos_n = sum(y_test)  
    neg_n = len(y_test) - pos_n
    biz_loss = (fnr * profit * pos_n) + (fpr * cost * neg_n) #number of positive and negative used as weights for imbalanced data set
    return ths[np.argmin(biz_loss)] #outputs the threshold with minimum business loss

def lgb_impl(X_train, y_train, X_test, y_test, opt_params, cost=1, profit=1):
    mod = lgb.train(opt_params, lgb.Dataset(X_train, label=y_train), valid_sets=(lgb.Dataset(X_test, label=y_test),))
    y_pred_prob = mod.predict(X_test, num_iteration=mod.best_iteration)
    ths = get_biz_threshold(y_test, y_pred_prob, cost, profit)
    y_pred = (y_pred_prob > ths).astype(int)  
    return y_pred_prob, y_pred

def xgb_impl(X_train, y_train, X_test, y_test, opt_params, cost=1, profit=1):
    mod = xgb.train(opt_params, xgb.DMatrix(X_train, label=y_train), evals=[(xgb.DMatrix(X_test, label=y_test),'test')], num_boost_round = 1000, early_stopping_rounds = 25)
    y_pred_prob = mod.predict(xgb.DMatrix(X_test, label=y_test))
    ths = get_biz_threshold(y_test, y_pred_prob, cost, profit)
    y_pred = (y_pred_prob > ths).astype(int)  
    return y_pred_prob, y_pred

def mod_eval(y_test, y_pred_prob, y_pred):  
    acc = accuracy_score(y_test, y_pred)
    auroc = roc_auc_score(y_test, y_pred_prob)
    f1 = f1_score(y_test, y_pred)
    auprc = average_precision_score(y_test, y_pred_prob)
    prc_b = len(y_test[y_test == 1]) / len(y_test)
    print(f"Test Accuracy: {acc:.5f} | Test AUROC: {auroc:.5f} | Test F1: {f1:.5f} | Test AUPRC: {auprc:.5f}(baseline:{prc_b:.5f})")
    return acc, auroc, f1, auprc, prc_b

class CustomerPreferencePrediction:
    def __init__(self):
        self.hl_model = None
        self.pl_model = None
        self.td_model = None
        self.hl_y_pred_prob = None
        self.pl_y_pred_prob = None
        self.td_y_pred_prob = None
        self.hl_opt_params = {'bagging_fraction': 0.5436036759336191,
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
        self.pl_opt_params = {'colsample_bytree': 0.6281982507677273,
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
        self.td_opt_params = {'colsample_bytree': 0.4157942248802582,
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
        self.hl_ths = 0.5
        self.pl_ths = 0.5
        self.td_ths = 0.5
        self.scaler = MinMaxScaler()
        
    def train(self, X_train, y_train, X_test, y_test, use_biz_threshold = True):
        hl_y_train, hl_y_test, pl_y_train, pl_y_test, td_y_train, td_y_test = label_split(y_train, y_test)
        self.hl_model = lgb.train(self.hl_opt_params, lgb.Dataset(X_train, label=hl_y_train), valid_sets=(lgb.Dataset(X_test, label=hl_y_test),))
        self.pl_model = xgb.train(self.pl_opt_params, xgb.DMatrix(X_train, label=pl_y_train), evals=[(xgb.DMatrix(X_test, label=pl_y_test),'test')], num_boost_round = 1000, early_stopping_rounds = 25)
        self.td_model = xgb.train(self.td_opt_params, xgb.DMatrix(X_train, label=td_y_train), evals=[(xgb.DMatrix(X_test, label=td_y_test),'test')], num_boost_round = 1000, early_stopping_rounds = 25)
        self.hl_y_pred_prob = self.predict_proba(X_test)[:,0]
        self.pl_y_pred_prob = self.predict_proba(X_test)[:,1]
        self.td_y_pred_prob = self.predict_proba(X_test)[:,2]
        if use_biz_threshold:
            self.hl_ths = get_biz_threshold(hl_y_test, self.hl_y_pred_prob, cost=1, profit=2.5)
            self.pl_ths = get_biz_threshold(pl_y_test, self.pl_y_pred_prob, cost=1, profit=2)
            self.td_ths = get_biz_threshold(td_y_test, self.td_y_pred_prob, cost=1, profit=2)
        self.scaler.fit(self.predict_proba(X_train))
        
    def predict_proba(self, X_test):
        self.hl_y_pred_prob = self.hl_model.predict(X_test, num_iteration=self.hl_model.best_iteration)
        self.pl_y_pred_prob = self.pl_model.predict(xgb.DMatrix(X_test))
        self.td_y_pred_prob = self.td_model.predict(xgb.DMatrix(X_test))
        return np.column_stack((self.hl_y_pred_prob, self.pl_y_pred_prob, self.td_y_pred_prob))
    
    def predict(self, X_test):
        hl_y_pred = (self.hl_y_pred_prob > self.hl_ths).astype(int)
        pl_y_pred = (self.pl_y_pred_prob > self.pl_ths).astype(int)
        td_y_pred = (self.td_y_pred_prob > self.td_ths).astype(int)
        return np.column_stack((hl_y_pred, pl_y_pred, td_y_pred))
    
    def rank(self, X_test):
        y_pred_prob = self.predict_proba(X_test)
        norm_y_pred_probs = pd.DataFrame(self.scaler.transform(y_pred_prob), columns=["Housing Loan", "Personal Loan", "Term Deposit"])
        return norm_y_pred_probs.rank(axis=1, ascending=False)
    
    def eval(self, y_test, y_pred_prob, y_pred):
        print("Housing Loan:")
        hl_acc, hl_auroc, hl_f1, hl_auprc, hl_prc_b = mod_eval(y_test.iloc[:, 0], y_pred_prob[:, 0], y_pred[:, 0])
        print("Personal Loan:")
        pl_acc, pl_auroc, pl_f1, pl_auprc, pl_prc_b = mod_eval(y_test.iloc[:, 1], y_pred_prob[:, 1], y_pred[:, 1])
        print("Term Deposit:")
        td_acc, td_auroc, td_f1, td_auprc, td_prc_b = mod_eval(y_test.iloc[:, 2], y_pred_prob[:, 2], y_pred[:, 2])
        
        fin_acc = (hl_acc + pl_acc + td_acc) / 3
        fin_auroc = (hl_auroc + pl_auroc + td_auroc) / 3
        fin_f1 = (hl_f1 + pl_f1 + td_f1) / 3
        fin_auprc = (hl_auprc + pl_auprc + td_auprc) / 3
        fin_prc_b = (hl_prc_b + pl_prc_b + td_prc_b) / 3
        print("Overall:")
        print(f"Test Accuracy: {fin_acc:.5f} | Test AUROC: {fin_auroc:.5f} | Test F1: {fin_f1:.5f} | Test AUPRC: {fin_auprc:.5f} (baseline:{fin_prc_b:.5f})")
        return fin_acc, fin_auroc, fin_f1, fin_auprc, fin_prc_b   
