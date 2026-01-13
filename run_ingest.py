from pathlib import Path
from src.ingest import ingest_raw_csv

ROOT = Path(__file__).resolve().parent  # folder where run_ingest.py lives

print("RUN_INGEST STARTED ✅")
print("PROJECT ROOT =", ROOT)

RAW = ROOT / "data" / "raw" / "cac_raw.csv"
OUT = ROOT / "data" / "processed" / "cac_base.parquet"

print("RAW =", RAW)
print("RAW exists? =", RAW.exists())

df = ingest_raw_csv(RAW, OUT)

print("WROTE =", OUT)
print("SHAPE =", df.shape)
print(df.head(3))