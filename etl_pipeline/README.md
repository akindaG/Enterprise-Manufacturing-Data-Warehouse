# ETL Pipeline

This folder contains the ETL implementation and end-to-end execution logic for the Enterprise Manufacturing Data Warehouse.

## Pipeline Flow

```text
Source CSV Files
      -> Data Quality Validation
      -> Staging Layer
      -> Cleaning / Transformation
      -> Dimension Loading
      -> SCD Type 2 Processing
      -> Historical Surrogate Key Resolution
      -> Fact_Production Incremental Loading
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

## Executable Orchestrator

`run_etl.py` performs the complete assessed flow:

1. extracts all required source files
2. cleans and validates the source state
3. loads staging tables
4. loads `Dim_Date`
5. inserts or Type 1 updates the simple dimensions
6. applies SCD Type 2 to `Dim_Machine`
7. resolves dimension surrogate keys
8. resolves the historical `Machine_Key` by production date
9. loads new facts using `Production_ID` as the idempotency key
10. writes the execution result to `etl_run_log`

## Data Quality Rules

The orchestrator fails before warehouse loading when it detects:

- missing required columns
- empty source datasets
- null business keys
- duplicate business keys within a source state
- invalid production dates
- negative measures
- defect counts greater than the quantity produced

## Incremental Fact Loading

`Production_ID` is carried from the source into `Fact_Production` as a degenerate dimension / transaction identifier. The ETL checks this identifier before insertion, and the warehouse schema also enforces it as unique.

This prevents duplicate facts during reruns without incorrectly collapsing two legitimate production events that happen to share the same measures and dimension keys.

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

- M001 changes from factory F001 to F002 and receives a new SCD Type 2 surrogate key
- M002 remains unchanged and does not receive another version
- M003 is inserted as a new dimension entity
- PR003 and PR004 are loaded incrementally
- historical M001 production remains linked to the original machine version

Use `analytics/scd_verification.sql` to inspect the result.

## Automated Verification

`.github/workflows/milestone5-etl-demo.yml` provisions PostgreSQL and performs both ETL executions automatically. It checks SCD history, fact counts, unique production identifiers and historical surrogate-key resolution.
