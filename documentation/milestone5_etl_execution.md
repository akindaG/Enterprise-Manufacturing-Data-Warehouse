# Milestone 5 - ETL Execution and SCD Type 2 Demonstration

## Objective

Demonstrate the complete Manufacturing Data Warehouse pipeline through two executions using different source-data states. The second execution proves historical preservation, surrogate-key changes, changed records, unchanged records, new records, and incremental fact loading.

## Pipeline

```text
CSV Source Files
      |
      v
Extract
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
Surrogate Key Lookups
      |
      v
Fact_Production Loading
      |
      v
Validation / Historical Queries
```

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

On Windows PowerShell:

```powershell
$env:DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/manufacturing_dw"
```

## First ETL Execution

Run:

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_1 --run-date 2026-08-01
```

### Run 1 source state

- M001 belongs to factory F001 (Colombo Plant).
- M002 belongs to factory F002 (Kandy Plant).
- Two production events are loaded.
- Initial dimension surrogate keys are generated.

Expected Dim_Machine conceptually:

| Machine | Factory | Effective Date | Expiry Date | Current |
|---|---|---|---|---|
| M001 | F001 | 2026-08-01 | 9999-12-31 | True |
| M002 | F002 | 2026-08-01 | 9999-12-31 | True |

## Source Changes Before Second Execution

`source_data/run_2/` represents a later operational state.

Meaningful changes:

1. **Changed record:** M001 moves from F001 to F002.
2. **Unchanged record:** M002 remains assigned to F002.
3. **New record:** M003 is introduced at F001.
4. **Incremental production:** PR003 and PR004 represent new production events on 2026-08-15.

## Second ETL Execution

Run:

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

M002 is unchanged, therefore no new historical version is created. Its existing surrogate key remains current.

### Expected behaviour for M003

M003 is a new business entity, therefore a new Dim_Machine row and surrogate key are generated.

## Historical Fact Relationship

The Run 1 fact for M001 remains linked to the original M001 surrogate key representing F001. The Run 2 fact for M001 resolves to the new surrogate key representing F002. This preserves the machine's correct historical context at the time each production event occurred.

## Validation

Execute:

```text
analytics/scd_verification.sql
```

The queries verify:

- both ETL runs in `etl_run_log`
- two versions of M001
- one unchanged version of M002
- the new M003 record
- fact rows linked to the correct historical Machine_Key
- production analysis before and after the M001 factory transfer

## Evidence to Capture for the Final Report

Take screenshots of:

1. Console output from Run 1.
2. `Dim_Machine` after Run 1.
3. The changed `run_2/machines.csv` source state.
4. Console output from Run 2.
5. `Dim_Machine` after Run 2 showing both M001 versions.
6. `etl_run_log` showing two successful executions.
7. `Fact_Production` joined to `Dim_Machine`, proving historical surrogate-key resolution.
8. At least one analytical comparison query.

## CCS3307 Requirement Demonstrated

This milestone demonstrates the required minimum flow:

```text
Source Data
   -> First ETL Execution
   -> Staging
   -> Data Warehouse
   -> Source Data Changed
   -> Second ETL Execution
   -> Updated Data Warehouse
   -> Historical Data / SCD Demonstration
   -> Analytical Queries
```
