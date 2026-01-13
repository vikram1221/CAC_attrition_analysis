from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

IN_PATH = ROOT / 'data' / 'processed' / 'cac_clean.parquet'
OUT_PATH = ROOT / 'data' / 'processed' / 'cac_model.parquet'

def build_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a binary target variable for attrition modeling.
    
    attrition = 1 -> registered but did not submit
    attrition = 0 -> registered and submitted
    """

    df = df.copy()

    # Basic validation
    required = ['entity_id', 'registered_at', 'submitted_at']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing required columns for labeling: {missing}')
    
    # Target label
    df['attrition'] = df['submitted_at'].isna().astype(int)

    # Helpful, leakage-safe features (known at registration time)
    # 1. registration day-of-year / month (seasonality)\
    df['reg_month'] = df['registered_at'].dt.month.astype('Int64')
    df['reg_dow'] = df['registered_at'].dt.dayofweek.astype('Int64')

    # 2. time between register and submit 
    df['days_to_submit'] = (
        (df['submitted_at'] - df['registered_at']).dt.total_seconds() / 86400.0
    )
    return df

def main():
    if not IN_PATH.exists():
        raise FileNotFoundError(f'Input file not found: {IN_PATH}')
    
    df = pd.read_parquet(IN_PATH)

    df_labeled = build_labels(df)

    # Basic sanity checks
    print('Rows: ', len(df_labeled))
    print('Attrition rate: ', df_labeled['attrition'].mean())

    # Show key columns 
    cols_to_show = ["entity_id", "contest_year", "zip_code", "team_size",
                    "registered_at", "submitted_at", "attrition"]
    cols_to_show = [c for c in cols_to_show if c in df_labeled.columns]
    print(df_labeled[cols_to_show])

    # Write model dataset
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_labeled.to_parquet(OUT_PATH, index=False)

    print(f'\nWROTE = {OUT_PATH}')

if __name__ == '__main__':
    main()

    