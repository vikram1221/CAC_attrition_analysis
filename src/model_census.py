from pathlib import Path 
import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'processed' / 'cac_enriched.parquet'

def prepare_features(df: pd.DataFrame):
    """
    Prepare leakage-safe features including Census enrichment. 
    """
    feature_cols = [
        'team_size',
        'reg_month', 
        'reg_dow', 
        'contest_year', 
        'median_income', 
        'low_income_area',
        'rural_proxy',
    ]

    feature_cols = [c for c in feature_cols if c in df.columns]

    X = df[feature_cols].copy()
    y = df['attrition'].copy()

    # Coservative imputation
    X['median_income'] = X['median_income'].fillna(X['median_income'].median())
    X = X.fillna(0)

    return X, y, feature_cols

def fit_logistic_regression(X, y):
    pipe = Pipeline(
        steps = [
            ('scaler', StandardScaler()),
            ('logit', LogisticRegression(solver='lbfgs'))
        ]
    )
    pipe.fit(X, y)
    return pipe

def summarize_coefficients(model, feature_names):
    coef = model.named_steps['logit'].coef_[0]
    odds_ratios = np.exp(coef)

    return (
        pd.DataFrame(
            {
                'feature': feature_names,
                'coefficient': coef, 
                'odds_ratio': odds_ratios
            }
        )
        .sort_values('odds_ratio', ascending=False)
        .reset_index(drop=True)
    )

def main():
    df = pd.read_parquet(DATA_PATH)

    X, y, feature_names = prepare_features(df)

    model = fit_logistic_regression(X, y)

    coef_summary = summarize_coefficients(model, feature_names)

    print('\n=== Census-Augmented Logistic Regression')
    print(coef_summary)
    print('\nBaseline attrition rate: ', y.mean())

if __name__ == '__main__':
    main()