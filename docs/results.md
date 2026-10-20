# Pennsylvania Open Data Quality Pipeline — First Results

## Overview
This project profiles and cleans public datasets from the Western Pennsylvania Regional Data Center (WPRDC), starting with Allegheny County Employee Salaries. The goal is to improve data usability and document quality issues over time.

**Repository**: https://github.com/harsha699/Pitts-DataQuality-pipeline  
**Data source**: Allegheny County Employee Salaries (WPRDC)  
**Pipeline**: Automated via GitHub Actions (weekly) + artifact retention

## Pipeline Steps
1. Download latest CSV from WPRDC
2. Profile (row count, null percentages, duplicates, dtypes)
3. Basic cleaning (drop empty rows, strip whitespace)
4. Save dated snapshot (Parquet) + quality report (JSON)
5. Upload results as GitHub Actions artifact (90-day retention)

## Quality Profile (First Run)
- **Rows processed**: 6,236
- **Columns**: 16
- **Duplicate rows**: 5
- **Null percentages**:
  - `DATE_TERM`: 82.01% (expected — most employees are still active)
  - All other columns: 0.0%
- **Data types**: Pay fields correctly numeric (`float64`); date fields currently strings (improvement opportunity)

## How to Reproduce
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/pipeline.py
