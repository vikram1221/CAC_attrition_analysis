from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'processed' / 'cac_model.parquet'

def prepare_features(df: pd.DataFrame):
    """
    Select leakage_safe features and target.
    """

    feature_cols = [
        'team_size',
        'reg_month',
        'reg_dow',
        'contest_year'
    ]

    # Keep only columns that actually exist
    feature_cols = [c for c in feature_cols if c in df.columns]

    X = df[feature_cols].copy()
    y = df['attrition'].copy()

    # Fill missing values conservatively
    X = X.fillna(X.median())

    return X, y, feature_cols

def fit_logistic_regression(X: pd.DataFrame, y: pd.Series):
    """
    Fit logistic regression with standardization
    """

    pipe = Pipeline(
        steps = [
            ('scaler', StandardScaler()),
            ('logit', LogisticRegression(solver='lbfgs'))
        ]
    )

    pipe.fit(X, y)
    return pipe

def summarize_coefficients(model, feature_names):
    """
    Convert coefficients to odds ratios for interpretation. 
    """
    coef = model.named_steps['logit'].coef_[0]
    odds_ratios = np.exp(coef)

    summary = pd.DataFrame(
        {
            'feature': feature_names,
            'coefficient': coef,
            'odds_ratio': odds_ratios,
        }
    ).sort_values('odds_ratio', ascending=True)

    return summary

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f'Missing model dataset: {DATA_PATH}')
    
    df = pd.read_parquet(DATA_PATH)

    X, y, feature_names = prepare_features(df)

    model = fit_logistic_regression(X, y)

    coef_summary = summarize_coefficients(model, feature_names)

    print('\n=== Logistic Regression Coefficients ===')
    print(coef_summary)

    print('\n Baseline attrition rate: ', y.mean())

if __name__ == '__main__':
    main()