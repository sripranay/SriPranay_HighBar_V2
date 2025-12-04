from pathlib import Path
import pandas as pd
import numpy as np

def load_data(path: Path, sample=False, sample_n=500):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    df = pd.read_csv(path)
    # basic cleaning
    for c in ["spend","impressions","clicks","purchases","revenue"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    if "date" in df.columns:
        df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")
    # derived cols (safe)
    if "clicks" in df.columns and "impressions" in df.columns:
        df["ctr"] = np.where(df["impressions"]>0, df["clicks"]/df["impressions"], np.nan)
    if "revenue" in df.columns and "spend" in df.columns:
        df["roas"] = np.where(df["spend"]>0, df["revenue"]/df["spend"], np.nan)
    if sample:
        df = df.sample(min(len(df), sample_n), random_state=42)
    return df
