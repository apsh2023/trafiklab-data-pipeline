# trafiklab-data-pipeline
A Python data ingestion pipeline for SL (Stockholm public transport) line data from Trafiklab.

## Project overview
This project is a personal learning project focused on building a small data pipeline with:
- API data fetching
- data cleaning and transformation
- basic statistics and reporting
- GitHub Actions CI for linting and tests
- environment configuration with .gitignore and .env

## Project plan

1. Fetch JSON from the SL API
2. Read transport categories from the response
3. Clean and transform raw items into a normalized structure
4. Calculate summary statistics by category and transport mode
5. Save output for reporting or further analysis

Source API:
https://transport.integration.sl.se/v1/lines?transport_authority_id=1

## Files
- [PROJECT_PLAN.md](PROJECT_PLAN.md) – project plan
- [scripts/fetch_sl_lines.py](scripts/fetch_sl_lines.py) – fetches the API and saves a summary
- [tests/test_fetch_sl_lines.py](tests/test_fetch_sl_lines.py) – CI validation tests
- [.github/workflows/ci.yml](.github/workflows/ci.yml) – GitHub Actions workflow
- [.env.example](.env.example) – example local environment configuration

## Run the fetch script
```bash
python scripts/fetch_sl_lines.py --output data/sl_lines_raw.json --summary-output data/sl_lines_summary.json
```

This script will:
- fetch the live API response
- save the raw JSON
- flatten each transport category into a single list
- calculate counts by category and transport mode
- save a summary JSON file

## CI validation
```bash
python -m pip install -r requirements.txt
pytest -q
```
