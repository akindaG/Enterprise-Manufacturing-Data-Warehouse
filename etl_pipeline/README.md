# ETL Pipeline

This folder contains the ETL implementation for the Enterprise Manufacturing Data Warehouse.

## Authoritative Executable

`run_etl.py` is the **authoritative end-to-end implementation** used by GitHub Actions and the two-run demonstration. The smaller module files (`extract.py`, `staging.py`, `transform.py`, `dimension_loader.py`, `scd_type2.py`, `fact_loader.py`, `validation.py`) are supporting/teaching helpers. Do not run them in sequence expecting them to replace the orchestrator.

## Pipeline Flow

```text
CSV Source-State Extracts
      -> Clean and Validate
      -> stg_* Tables
      -> Date + Type 1 Dimensions
      -> Machine SCD Type 2
      -> Surrogate-Key Resolution
      -> Fact_Production
      -> ETL Run Log
      -> Historical / Analytical Validation
```

## Data Quality Rules

`run_etl.py` validates:

- required files and columns
- non-empty source entities
- null/duplicate business keys
- valid numeric measures
- non-negative quantity, time, cost and defects
- `Defect_Count <= Quantity`
- parseable production dates
- no production date later than the ETL run date
- Product, Machine, Factory, Employee and Shift references
- production-event factory consistency with the source-state machine assignment

## Environment Configuration

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the template:

```bash
cp .env.example .env
```

The ETL accepts either `DATABASE_URL` or the individual `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` and `DB_PASSWORD` values. `DATABASE_URL` takes precedence.

## Run 1

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_1 --run-date 2026-08-01
```

Initial state:

- M001 assigned to F001
- M002 assigned to F002
- PR001 and PR002 loaded

## Run 2

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_2 --run-date 2026-08-15
```

Later state:

- M001 changes F001 -> F002 and receives a new SCD Type 2 version
- M002 remains unchanged
- M003 is new
- PR003 and PR004 are loaded incrementally

## Verification

```bash
psql -U postgres -d manufacturing_dw -f analytics/scd_verification.sql
psql -U postgres -d manufacturing_dw -f analytics/production_kpi_analysis.sql
```

The GitHub Actions workflow performs the same two-run demonstration automatically and uploads a `milestone5-etl-evidence` artifact containing ETL logs, machine history, historical fact relationships and analytical output.
