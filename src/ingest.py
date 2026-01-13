from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional

import pandas as pd

# 1. Schema definition 

@dataclass(frozen=True)
class CACSchema:
    """
    Canonical column names wwe want downstream. 
    These are the minimum fields needed for attrition modeling. 
    """

    entity_id: str = 'entity_id'            # Unique id per registered entity
    contest_year: str = 'contest_year'      # int-like
    zip_code: str = 'zip_code'              # string, 5-digit preferred
    team_size: str = 'team_size'            # int-like
    registered_at: str = 'registered_at'    # timestamp
    submitted_at: str = 'submitted_at'      # timestamp (can be null)

REQUIRED_COLS: Iterable[str] = [
    CACSchema().entity_id,
    CACSchema().contest_year,
    CACSchema().registered_at
]

# Common raw column variants we might see in exports

DEFAULT_RENAME_MAP: Dict[str, str] = {
    # IDs
    'id': 'entity_id',
    'participant_id': 'entity_id', 
    'team_id': 'entity_id',
    'submission_id': 'enitity_id',

    # Year 
    'year': 'contest_year',
    'contestyear': 'contest_year',

    # ZIP 
    'zip': 'zip_code',
    'zipcode': 'zip_code',
    'zip_code': 'zip_code',

    # Team size
    'teamsize': 'team_size',
    'team_size': 'team_size',
    'num_members': 'team_size',
    'members': 'team_size',

    # Timestamps
    'registration_timestamp': 'registered_at',
    'registered_timestamp': 'registered_at',
    'registered_at': 'registered_at',
    'created_at': 'registered_at',

    'submission_timestamp': 'submitted_at',
    'submitted_timestamp': 'submitted_at',
    'submitted_at': 'submitted_at',
    'final_submission_at': 'submitted_at',
}

# 2. Helpers 

def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip('_')
    )
    return df

def _apply_rename_map(df: pd.DataFrame, rename_map: Dict[str, str]) -> pd.DataFrame:
    # Only rename columns that exist
    existing = {k: v for k, v in rename_map.items() if k in df.columns}
    return df.rename(columns=existing)

def _coerce_types(df: pd.DataFrame, schema: CACSchema) -> pd.DataFrame:
    df = df.copy()

    # entity_id as string
    if schema.entity_id in df.columns:
        df[schema.entity_id] = df[schema.entity_id].astype(str)

    # contest_year numeric -> Int64 (nullable)
    if schema.contest_year in df.columns:
        df[schema.contest_year] = pd.to_numeric(df[schema.contest_year], errors='coerce').astype('Int64')

    # team_size numeric -> Int64 (nullable)
    if schema.team_size in df.columns:
        df[schema.team_size] = pd.to_numeric(df[schema.team_size], errors='coerce').astype('Int64')

    # ZIP normalize to 5-digit string when possible 
    if schema.zip_code in df.columns:
        z = df[schema.zip_code].astype(str).str.extract(r"(\d{5})", expand=False)
        df[schema.zip_code] = z

    # timestamps -> datetime (UTC)
    for tcol in [schema.registered_at, schema.submitted_at]:
        if tcol in df.columns:
            df[tcol] = pd.to_datetime(df[tcol], errors='coerce', utc=True)
    
    return df

def _validate_required(df: pd.DataFrame, required_cols: Iterable[str]) -> None:
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f'Missing required columns after standardisation: {missing}')
    

# 3. Public Ingestion Function

def ingest_raw_csv(
    raw_csv_path: str | Path, 
    out_parquet_path: str | Path, 
    rename_map: Optional[Dict[str, str]] = None,
    schema: CACSchema = CACSchema(),
) -> pd.DataFrame:
    
    """
    Reads a raw CSV export, standardized columns, applies rename mapping, 
    coerces types, validates required fields, and writes a processed Parquet. 

    Returns the cleaned base DataFrame
    """

    raw_csv_path = Path(raw_csv_path)
    out_parquet_path = Path(out_parquet_path)
    out_parquet_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(raw_csv_path)

    df = _standardize_columns(df)
    df = _apply_rename_map(df, rename_map or DEFAULT_RENAME_MAP)
    df = _coerce_types(df, schema=schema)
    _validate_required(df, REQUIRED_COLS)

    # Keep only canonical + any extra columns 
    df.to_parquet(out_parquet_path, index=False)
    return df
