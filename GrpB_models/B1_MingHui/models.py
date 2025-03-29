import numpy as np
import xgboost as xgb
import lightgbm as lgb
from sklearn.metrics import roc_curve, confusion_matrix, accuracy_score, f1_score, roc_auc_score, average_precision_score
from datapreparation import label_split

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

def final_model(X_train, y_train, X_test, y_test):
    hl_y_train, hl_y_test, pl_y_train, pl_y_test, td_y_train, td_y_test = label_split(y_train, y_test)
    print("Housing Loan:")
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
    hl_y_pred_prob, hl_y_pred = lgb_impl(X_train, hl_y_train, X_test, hl_y_test, hl_opt_params, cost=1, profit=2.5)
    hl_acc, hl_auroc, hl_f1, hl_auprc, hl_prc_b = mod_eval(hl_y_test, hl_y_pred_prob, hl_y_pred)
    
    print("Personal Loan:")
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
    pl_y_pred_prob, pl_y_pred = xgb_impl(X_train, pl_y_train, X_test, pl_y_test, pl_opt_params, cost=1, profit=2)
    pl_acc, pl_auroc, pl_f1, pl_auprc, pl_prc_b = mod_eval(pl_y_test, pl_y_pred_prob, pl_y_pred)

    print("Term Deposit:")
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
    td_y_pred_prob, td_y_pred = xgb_impl(X_train, td_y_train, X_test, td_y_test, td_opt_params, cost=1, profit=2)
    td_acc, td_auroc, td_f1, td_auprc, td_prc_b = mod_eval(td_y_test, td_y_pred_prob, td_y_pred)

    print("Overall:")
    y_pred_prob = np.column_stack((hl_y_pred_prob, pl_y_pred_prob, td_y_pred_prob))
    y_pred = np.column_stack((hl_y_pred, pl_y_pred, td_y_pred))
    fin_acc = (hl_acc + pl_acc + td_acc)/3
    fin_auroc = (hl_auroc + pl_auroc + td_auroc)/3
    fin_f1 = (hl_f1 + pl_f1 + td_f1)/3
    fin_auprc = (hl_auprc + pl_auprc + td_auprc)/3
    fin_prc_b = (hl_prc_b + pl_prc_b + td_prc_b)/3
    print(f"Test Accuracy: {fin_acc:.5f} | Test AUROC: {fin_auroc:.5f} | Test F1: {fin_f1:.5f} | Test AUPRC: {fin_auprc:.5f}(baseline:{fin_prc_b:.5f})")
    return y_pred_prob, y_pred

    
    
