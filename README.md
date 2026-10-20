# Pittsburgh / Pennsylvania Open Data Quality Pipeline

An open-source, scheduled data quality pipeline that profiles, cleans, and archives Pennsylvania (starting with Pittsburgh-area and statewide) open datasets. 

**Goal**: Improve usability of public data while generating reusable methods, documentation, and evidence of original contributions.

## Features (Planned)
- Automated weekly/monthly runs via GitHub Actions
- Data profiling and quality scoring
- Cleaning / standardization steps
- Dated archive of historical snapshots (1+ year retention)
- Public documentation and results site

## Quick Start
```bash
# Clone the repo
git clone https://github.com/harsha699/Pitts-DataQuality-pipeline.git
cd Pitts-DataQuality-pipeline

# Install dependencies
pip install -r requirements.txt

# Run locally (example)
python src/pipeline.py --dataset sample
```

## Project Structure
```
.
├── .github/workflows/     # Scheduled CI / ETL runs
├── src/                   # Pipeline code
├── data/sample/           # Sample or cached datasets
├── archive/               # Historical dated outputs (gitignored if large)
├── docs/                  # Methodology and reports
├── requirements.txt
└── README.md
```

## Status
- [x] Repository created
- [ ] First dataset selected
- [ ] Basic pipeline implemented
- [ ] GitHub Actions schedule added
- [ ] Storage (R2 / B2) connected
- [ ] First publication draft

## License
MIT
