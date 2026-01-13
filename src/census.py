from pathlib import Path
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

IN_PATH = ROOT / 'data' / 'processed' / 'cac_model.parquet'
OUT_PATH = ROOT / 'data' / 'processed' / 'cac_enriched.parquet'

# ACS 5-year 2023 median household income
ACS_YEAR = '2023'
ACS_VAR = "B19013_001E" # median household income
ACS_API = "https://api.census.gov/data"

def fetch_income_by_zcta(zips):
    """
    Fetch median household income by ZIP (ZCTA) from ACS.
    """
    zips = sorted(set(zips.dropna()))

    records = []

    for z in zips:
        
        params = {
            'get': ACS_VAR,
            'for': f'zip code tabulation area: {z}'
        }

        url = f'{ACS_API}/{ACS_YEAR}/acs/acs5'

        r = requests.get(url, params=params)
        if r.status_code != 200:
            continue

        data = r.json()
        if len(data) < 2:
            continue

        value = data[1][0]
        records.append(
            {
                'zip_code': z, 
                'median_income': pd.to_numeric(value, errors='coerce')
            }
        )

    return pd.DataFrame(records)

def classify_rural(df):
    """
    Simple rural proxy based on income.
    """

    df = df.copy()
    df['low_income_area'] = (df['median_income'] < 50000).astype('Int64')
    df['rural_proxy'] = df['median_income'].isna().astype('Int64')

    return df

def main():
    df = pd.read_parquet(IN_PATH)

    income_df = fetch_income_by_zcta(df['zip_code'])

    df = df.merge(income_df, on='zip_code', how='left')

    df = classify_rural(df)

    df.to_parquet(OUT_PATH, index=False)

    print("Census enrichment complete.")
    print(df[["entity_id", "zip_code", "median_income", "low_income_area", "rural_proxy"]])


if __name__ == '__main__':
    main()