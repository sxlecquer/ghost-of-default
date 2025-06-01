import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
import joblib


def load_data(path: str = '../default_credit_card.csv') -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.rename(columns={
        'ID': 'id',
        'LIMIT_BAL': 'limit_bal',
        'SEX': 'sex',
        'EDUCATION': 'education',
        'MARRIAGE': 'marriage',
        'AGE': 'age',
        'PAY_0': 'repay_status_1',
        'PAY_2': 'repay_status_2',
        'PAY_3': 'repay_status_3',
        'PAY_4': 'repay_status_4',
        'PAY_5': 'repay_status_5',
        'PAY_6': 'repay_status_6',
        'BILL_AMT1': 'bill_amount_1',
        'BILL_AMT2': 'bill_amount_2',
        'BILL_AMT3': 'bill_amount_3',
        'BILL_AMT4': 'bill_amount_4',
        'BILL_AMT5': 'bill_amount_5',
        'BILL_AMT6': 'bill_amount_6',
        'PAY_AMT1': 'pay_amount_1',
        'PAY_AMT2': 'pay_amount_2',
        'PAY_AMT3': 'pay_amount_3',
        'PAY_AMT4': 'pay_amount_4',
        'PAY_AMT5': 'pay_amount_5',
        'PAY_AMT6': 'pay_amount_6',
        'default.payment.next.month': 'default'
    })
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df['education'] = df['education'].replace({0: 4, 5: 4, 6: 4})
    df['marriage'] = df['marriage'].replace({0: 3})

    pay_cols = [col for col in df.columns if col.startswith('repay_')]
    for col in pay_cols:
        df[col] = df[col].replace(-2, -1)

    bill_cols = [f'bill_amount_{i}' for i in range(1, 7)]
    for col in bill_cols:
        df[col] = df[col].clip(lower=0)

    return df


def segregate_features(df: pd.DataFrame, unique_num: int) -> tuple[list[str], list[str]]:
    numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = df.select_dtypes(include=['object', 'category']).columns.tolist()

    possible_cat_features = [col for col in numeric_features if df[col].nunique() <= unique_num]
    numeric_features = [col for col in numeric_features if col not in possible_cat_features]
    categorical_features = categorical_features + possible_cat_features
    return numeric_features, categorical_features


def build_preprocessor(numeric_features, categorical_features):
    num_transformer = Pipeline(steps=[
        ('impute', SimpleImputer(strategy='median')),
        ('scale', StandardScaler())
    ])
    cat_transformer = Pipeline(steps=[
        ('impute', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    return ColumnTransformer([
        ('num', num_transformer, numeric_features),
        ('cat', cat_transformer, categorical_features)
    ], remainder='drop')


def build_model_pipeline(preprocessor):
    return Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(penalty='l2', C=0.5, solver='lbfgs'))
    ])


def prepare_model():
    df = load_data()
    df = clean_data(df)

    if 'id' in df.columns:
        df = df.drop(columns=['id'])

    numeric_features, categorical_features = segregate_features(df.drop(columns=['default']), 12)

    preprocessor = build_preprocessor(numeric_features, categorical_features)

    pipeline = build_model_pipeline(preprocessor)

    X = df[numeric_features + categorical_features]
    y = df['default']

    pipeline.fit(X, y)

    joblib.dump(pipeline, '../credit_model.joblib')


def load_model(path: str = "../credit_model.joblib") -> Pipeline:
    return joblib.load(path)


if __name__ == "__main__":
    prepare_model()
