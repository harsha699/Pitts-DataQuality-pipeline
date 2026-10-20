"""
Data quality pipeline for Allegheny County Employee Salaries.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests


DATA_URL = (
    "https://data.wprdc.org/dataset/16e59d06-1233-4acc-924c-4651f24987ee/"
    "resource/33e12320-a94b-4525-bb5c-04d2e96c4d88/download/"
    "employee-salaries-wprdc-redactions-10.15.2026.csv"
)


def download_data(url: str, dest: Path) -> Path:
    """Download CSV if not already present."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"Using cached file: {dest}")
        return dest
    print(f"Downloading {url} ...")
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    dest.write_bytes(r.content)
    print(f"Saved to {dest}")
    return dest


def profile_dataframe(df: pd.DataFrame) -> dict:
    """Basic data quality profile."""
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "null_percentages": (df.isnull().mean() * 100).round(2).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning."""
    df = df.dropna(how="all")
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
    return df


def main(dataset_name: str = "allegheny-salaries"):
    run_date = datetime.utcnow().strftime("%Y-%m-%d")
    print(f"Starting pipeline run for {dataset_name} on {run_date}")

    raw_path = Path("data/raw") / f"{dataset_name}.csv"
    download_data(DATA_URL, raw_path)

    df = pd.read_csv(raw_path)
    print(f"Loaded {len(df)} rows")

    profile = profile_dataframe(df)
    print("Profile:", json.dumps(profile, indent=2))

    cleaned = clean_dataframe(df)

    archive_dir = Path("archive") / run_date
    archive_dir.mkdir(parents=True, exist_ok=True)

    output_path = archive_dir / f"{dataset_name}_cleaned.parquet"
    cleaned.to_parquet(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")

    profile_path = archive_dir / f"{dataset_name}_profile.json"
    with open(profile_path, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"Saved profile to {profile_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="allegheny-salaries")
    args = parser.parse_args()
    main(args.dataset)