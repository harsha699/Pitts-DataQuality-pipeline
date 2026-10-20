# Methodology

## Data Quality Dimensions Tracked
- Completeness (null percentages)
- Uniqueness (duplicate rows)
- Consistency (basic type and format checks)
- Validity (placeholder for domain rules)

## Pipeline Steps
1. Ingest raw open data (CSV / API)
2. Profile
3. Clean / standardize
4. Write dated snapshot to archive
5. Generate quality report

## Future Enhancements
- PySpark for larger datasets
- Great Expectations validation suite
- Automated upload to object storage
- Public dashboard of quality scores over time
