import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sqlalchemy.orm import sessionmaker
from backend.app.core.db import engine
from backend.app.core.utils import BASE_DIR
from backend.app.models.db_models import ActualOutcome, Prediction
from backend.app.models.enums import *


SessionLocal = sessionmaker(bind=engine)


def _load_orig_data(path: str = BASE_DIR / 'default_credit_card.csv') -> pd.DataFrame:
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


def _load_aug_data() -> pd.DataFrame:
    session = SessionLocal()
    rows = []
    preds = (
        session.query(Prediction)
        .join(ActualOutcome)
        .filter(ActualOutcome.actual_default != None)
        .all()
    )

    for pred in preds:
        row = {}
        for attr in Prediction.__table__.columns.keys():
            if attr not in ('sex_id', 'education_id', 'marriage_id'):
                row[attr] = getattr(pred, attr)

        row['sex'] = Sex(pred.sex.name).code
        row['education'] = Education(pred.education.name).code
        row['marriage'] = Marriage(pred.marriage.name).code

        row['default'] = pred.actual_outcome.actual_default
        rows.append(row)

    session.close()
    return pd.DataFrame(rows)


def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df['education'] = df['education'].replace({0: 4, 5: 4, 6: 4})
    df['marriage'] = df['marriage'].replace({0: 3})

    pay_cols = [col for col in df.columns if col.startswith('repay_')]
    for col in pay_cols:
        df[col] = df[col].replace(-2, -1)

    bill_cols = [f'bill_amount_{i}' for i in range(1, 7)]
    for col in bill_cols:
        df[col] = df[col].clip(lower=0)

    return df


def _segregate_features(df: pd.DataFrame, unique_num: int) -> tuple[list[str], list[str]]:
    numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = df.select_dtypes(include=['object', 'category']).columns.tolist()

    possible_cat_features = [col for col in numeric_features if df[col].nunique() <= unique_num]
    numeric_features = [col for col in numeric_features if col not in possible_cat_features]
    categorical_features = categorical_features + possible_cat_features
    return numeric_features, categorical_features


def _build_preprocessor(numeric_features, categorical_features):
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


def _build_model_pipeline(preprocessor):
    return Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(penalty='l2', C=0.5, solver='lbfgs'))
    ])


def _train_pipeline(df: pd.DataFrame):
    numeric_features, categorical_features = _segregate_features(df.drop(columns=['default']), 12)
    preprocessor = _build_preprocessor(numeric_features, categorical_features)
    pipeline = _build_model_pipeline(preprocessor)
    X = df[numeric_features + categorical_features]
    y = df['default']
    pipeline.fit(X, y)
    joblib.dump(pipeline, BASE_DIR / 'credit_model.joblib')


def train_model():
    df = _clean_data(_load_orig_data()).drop(columns=['id'], errors='ignore')
    _train_pipeline(df)


def retrain_model():
    orig = _clean_data(_load_orig_data()).drop(columns=['id'], errors='ignore')
    aug = _load_aug_data().drop(columns=['id', 'confidence'], errors='ignore')
    combined = pd.concat([orig, aug], ignore_index=True)
    _train_pipeline(combined)


def load_model(path: str = BASE_DIR / 'credit_model.joblib') -> Pipeline:
    return joblib.load(path)


if __name__ == "__main__":
    train_model()
    # retrain_model()
