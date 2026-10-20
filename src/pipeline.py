"""
Starter data quality pipeline for Pittsburgh / Pennsylvania open data.
Run locally or via GitHub Actions.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import pandas as pd


def profile_dataframe(df: pd.DataFrame) -> dict:
    """Basic data quality profile."""
    profile = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "null_percentages": (df.isnull().mean() * 100).round(2).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }
    return profile


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Placeholder cleaning steps — expand as needed."""
    # Example: drop fully empty rows, strip whitespace from string columns
    df = df.dropna(how="all")
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
    return df


def main(dataset_name: str = "sample"):
    run_date = datetime.utcnow().strftime("%Y-%m-%d")
    print(f"Starting pipeline run for {dataset_name} on {run_date}")

    # TODO: Replace with real download from OpenDataPA or WPRDC
    # Example: load a local sample or download CSV
    sample_path = Path("data/sample") / f"{dataset_name}.csv"
    if sample_path.exists():
        df = pd.read_csv(sample_path)
    else:
        print(f"Sample file not found: {sample_path}. Using empty DataFrame.")
        df = pd.DataFrame()

    if df.empty:
        print("No data to process.")
        return

    # Profile
    profile = profile_dataframe(df)
    print("Profile:", json.dumps(profile, indent=2))

    # Clean
    cleaned = clean_dataframe(df)

    # Save dated archive
    archive_dir = Path("archive") / run_date
    archive_dir.mkdir(parents=True, exist_ok=True)
    output_path = archive_dir / f"{dataset_name}_cleaned.parquet"
    cleaned.to_parquet(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")

    # Save profile report
    profile_path = archive_dir / f"{dataset_name}_profile.json"
    with open(profile_path, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"Saved profile to {profile_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="sample", help="Dataset name to process")
    args = parser.parse_args()
    main(args.dataset)
