# ETL Pipeline

This folder contains the ETL implementation and end-to-end execution logic for the Enterprise Manufacturing Data Warehouse.

## Pipeline Flow

```text
Source CSV Files
      -> Staging Layer
      -> Cleaning / Transformation
      -> Dimension Loading
      -> SCD Type 2 Processing
      -> Surrogate Key Resolution
      -> Fact_Production Loading
      -> Validation and Historical Analysis
```

## Components

- `extract.py` - source extraction helpers
- `staging.py` - staging-layer helpers
- `transform.py` - cleaning and standardization helpers
- `dimension_loader.py` - dimension and surrogate-key helpers
- `scd_type2.py` - SCD Type 2 helper logic
- `fact_loader.py` - fact-loading helper logic
- `validation.py` - data-quality helpers
- `run_etl.py` - executable end-to-end ETL orchestrator used for the two-run demonstration

## Milestone 5 Demonstration

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the initial source state:

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_1 --run-date 2026-08-01
```

Run the changed source state:

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_2 --run-date 2026-08-15
```

The second source state demonstrates:

- M001 changed from factory F001 to F002 and receives a new SCD Type 2 surrogate key
- M002 remains unchanged and does not receive another version
- M003 is inserted as a new dimension entity
- new production facts are loaded incrementally
- historical M001 production remains linked to the original machine version

Use `analytics/scd_verification.sql` to verify the result.

A GitHub Actions workflow at `.github/workflows/milestone5-etl-demo.yml` provisions PostgreSQL and performs both ETL executions automatically, then asserts the expected SCD and fact-table outcomes.
