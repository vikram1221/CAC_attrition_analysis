from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

IN_PATH = ROOT / 'data' / 'processed' / 'cac_base.parquet'
OUT_PATH = ROOT / 'data' / 'processed' / 'cac_clean.parquet'

def normalize_zip(zip_series: pd.Series) -> pd.Series:
    """
    Normalize ZIP codes to 5-digit strings. 
    Invalid ZIPs become NaN. 
    """
    return (
        zip_series
        .astype(str)
        .str.extract(r"(\d+)", expand=False)            # keep digits only
        .str.zfill(5)
        .where(lambda s: s.str.len() == 5)
    )

def main():
    df = pd.read_parquet(IN_PATH)

    df['zip_code'] = normalize_zip(df['zip_code'])

    df.to_parquet(OUT_PATH, index=False)

    print('Zip normalization complete.')
    print(df[['entity_id', 'zip_code']])

if __name__ == '__main__':
    main()