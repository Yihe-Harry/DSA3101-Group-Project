#pip install ucimlrepo (install to load data)
#pip install iterative-stratification (install for multilabel stratification)
import pandas as pd
from ucimlrepo import fetch_ucirepo
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from iterstrat.ml_stratifiers import MultilabelStratifiedKFold

def import_data():
    bank_marketing = fetch_ucirepo(id=222)
    X = bank_marketing.data.features
    y = bank_marketing.data.targets
    df = pd.concat([X,y], axis=1)
    return df

def col_ohe(df, col_list):
    onehotencoder = OneHotEncoder(handle_unknown='ignore', sparse_output = False)
    for var in col_list:
        var_encoded = pd.DataFrame(onehotencoder.fit_transform(df[[var]]), columns = onehotencoder.get_feature_names_out([var])).astype(int)
        df = pd.concat([df.drop(columns=var, axis=1),var_encoded], axis = 1)
    return df

def edu_ordinal(df):
    education_encoder=OrdinalEncoder(categories=[['primary','secondary','tertiary']], handle_unknown='use_encoded_value', unknown_value=-1)
    df['education'] = education_encoder.fit_transform(df[['education']]).astype(int)
    return df

def yn_map(df, col_list):
    df[col_list] = df[col_list].replace({'yes':1, 'no':0})
    return df

def time_eng(df):
    start_year = 2008
    df['year'] = start_year
    df['month'] = pd.to_datetime(df['month'], format='%b').dt.month
    for i in range(1, len(df)):
        if df.loc[i, 'month'] < df.loc[i - 1, 'month']:
            df.loc[i, 'year'] = df.loc[i - 1, 'year'] + 1
        else:
            df.loc[i, 'year'] = df.loc[i - 1, 'year']
    contact_date = pd.to_datetime(df['day_of_week'].astype(str) + '-' + df['month'].astype(str) + '-' + df['year'].astype(str), format='%d-%m-%Y')
    last_contact_date = contact_date.max()
    df['days_from_contact'] = (last_contact_date - contact_date).dt.days
    df.drop(columns=['year'], inplace=True, axis=1) #dropped since did not help with models
    return df

def data_cleaning(df):
    df = col_ohe(df, ['job', 'marital', 'contact'])
    df = edu_ordinal(df)
    df = yn_map(df, ['default', 'housing', 'loan', 'y'])
    df = time_eng(df)
    df.drop(columns=['poutcome', 'duration', 'campaign', 'job_nan', 'contact_nan'], inplace=True, axis=1)
    df.rename(columns={'job_admin.': 'job_admin', 'y': 'term_deposit', 'housing': 'housing_loan', 'loan': 'personal_loan'}, inplace=True)
    return df

def data_split(df):
    X = df.drop(columns=['housing_loan','personal_loan','term_deposit'])
    y = df[['housing_loan','personal_loan','term_deposit']]
    mlss = MultilabelStratifiedKFold(n_splits=5, random_state=27, shuffle=True)
    train_i, test_i = next(iter(mlss.split(X, y)))
    X_train, X_test = X.iloc[train_i], X.iloc[test_i]
    y_train, y_test = y.iloc[train_i], y.iloc[test_i]
    return X_train, y_train, X_test, y_test

def label_split(y_train, y_test):
    hl_y_train, hl_y_test =  y_train['housing_loan'], y_test['housing_loan']
    pl_y_train, pl_y_test =  y_train['personal_loan'], y_test['personal_loan']
    td_y_train, td_y_test =  y_train['term_deposit'], y_test['term_deposit']
    return hl_y_train, hl_y_test, pl_y_train, pl_y_test, td_y_train, td_y_test
