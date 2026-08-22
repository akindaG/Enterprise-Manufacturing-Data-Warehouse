# Milestone 5 - ETL Execution and SCD Type 2 Demonstration

## Objective

Demonstrate the complete Enterprise Manufacturing Data Warehouse pipeline through two executions using different source-data states. The second execution proves historical preservation, surrogate-key changes, changed records, unchanged records, new records and incremental fact loading.

## Pipeline

```text
CSV Source Files
      |
      v
Extract
      |
      v
Data Quality Validation
      |
      v
Staging Tables
      |
      v
Cleaning / Transformation
      |
      v
Dimension Loading
      |
      v
SCD Type 2 Processing for Dim_Machine
      |
      v
Historical Surrogate Key Resolution
      |
      v
Fact_Production Incremental Loading
      |
      v
Validation / Historical Queries
```

## Fact Idempotency Improvement

The source `production_id` is stored in `Fact_Production` as `Production_ID`, a degenerate dimension / source transaction identifier.

The ETL checks this identifier before inserting a fact. This is more reliable than comparing measures and dimension keys because two legitimate production events may have identical quantities, costs, durations, defects and dimensional context.

The warehouse enforces `Production_ID` as unique, providing a second integrity layer in addition to the ETL check.

## Data Quality Rules

Before loading, the ETL validates:

- all required files and columns are present
- source datasets are non-empty
- source business keys are not null
- source business keys are unique within each source state
- production measures are non-negative
- `Defect_Count` does not exceed `Quantity_Produced`
- production dates are valid

## Prerequisites

1. PostgreSQL is running.
2. The warehouse tables from `warehouse_database/` have been created.
3. Python dependencies are installed:

```bash
pip install -r requirements.txt
```

4. Set the warehouse connection if it differs from the default:

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/manufacturing_dw"
```

Windows PowerShell:

```powershell
$env:DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/manufacturing_dw"
```

## First ETL Execution

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_1 --run-date 2026-08-01
```

### Run 1 source state

- M001 belongs to factory F001, Colombo Plant.
- M002 belongs to factory F002, Kandy Plant.
- PR001 and PR002 are loaded as the initial production events.
- Initial dimension surrogate keys are generated.

Expected `Dim_Machine` conceptually:

| Machine | Factory | Effective Date | Expiry Date | Current |
|---|---|---|---|---|
| M001 | F001 | 2026-08-01 | 9999-12-31 | True |
| M002 | F002 | 2026-08-01 | 9999-12-31 | True |

## Source Changes Before the Second Execution

`source_data/run_2/` represents a later operational state:

1. **Changed record:** M001 moves from F001 to F002.
2. **Unchanged record:** M002 remains assigned to F002.
3. **New record:** M003 is introduced at F001.
4. **Incremental production:** PR003 and PR004 are new production events on 2026-08-15.

## Second ETL Execution

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_2 --run-date 2026-08-15
```

### Expected SCD Type 2 result for M001

| Machine Key | Machine | Factory | Effective Date | Expiry Date | Current |
|---|---|---|---|---|---|
| original SK | M001 | F001 | 2026-08-01 | 2026-08-14 | False |
| new SK | M001 | F002 | 2026-08-15 | 9999-12-31 | True |

The original row is preserved instead of overwritten. A new surrogate key identifies the new historical version.

### Expected behaviour for M002

M002 is unchanged, so no new historical version is created and its existing surrogate key remains current.

### Expected behaviour for M003

M003 is a new business entity, so a new `Dim_Machine` row and surrogate key are generated.

## Historical Fact Relationship

The Run 1 fact `PR001` remains linked to the original M001 surrogate key representing F001. The Run 2 fact `PR003` resolves to the new M001 surrogate key representing F002. This preserves the machine's correct historical context at the time each production event occurred.

## Automated Verification

The GitHub Actions workflow at `.github/workflows/milestone5-etl-demo.yml` provisions PostgreSQL, compiles the ETL code, creates the warehouse schema, runs both source states and checks the expected results.

Assertions include:

- exactly two successful ETL execution records
- exactly two M001 SCD versions
- old M001/F001 version expired
- new M001/F002 version current
- one unchanged M002 version
- one current M003 version
- exactly four production facts
- exactly four distinct `Production_ID` values
- zero duplicate `Production_ID` values
- PR001 linked to the historical M001/F001 version
- PR003 linked to the new M001/F002 version

## Manual SQL Verification

Execute:

```bash
psql -U postgres -d manufacturing_dw -f analytics/scd_verification.sql
```

The queries display the ETL log, SCD versions, fact-to-dimension relationships, fact identifier uniqueness and historical production comparison.

## Evidence to Capture for the Final Report

1. Successful GitHub Actions check.
2. Console output from Run 1.
3. `Dim_Machine` after Run 1.
4. Changed `source_data/run_2/machines.csv`.
5. Console output from Run 2.
6. `Dim_Machine` after Run 2 showing both M001 versions.
7. `etl_run_log` showing two successful executions.
8. `Fact_Production` showing PR001 to PR004.
9. Fact-to-machine join proving historical surrogate-key resolution.
10. At least one historical analytical comparison query.

## CCS3307 Requirement Demonstrated

```text
Source Data
   -> First ETL Execution
   -> Staging
   -> Data Warehouse
   -> Source Data Changed
   -> Second ETL Execution
   -> Updated Data Warehouse
   -> SCD Historical Preservation
   -> Incremental Fact Loading
   -> Analytical Verification
```
