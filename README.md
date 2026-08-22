# Enterprise Manufacturing Data Warehouse

[![Milestone 5 ETL and SCD Demonstration](https://github.com/akindaG/Enterprise-Manufacturing-Data-Warehouse/actions/workflows/milestone5-etl-demo.yml/badge.svg)](https://github.com/akindaG/Enterprise-Manufacturing-Data-Warehouse/actions/workflows/milestone5-etl-demo.yml)

Academic and portfolio-grade Data Warehouse implementation for **CCS3307 Data Warehousing**.

The project demonstrates the complete Data Warehouse lifecycle required by the assignment:

```text
Business Domain
      ↓
Business Requirements
      ↓
Source Systems
      ↓
OLTP Database
      ↓
Staging Layer
      ↓
ETL Pipeline
      ↓
Dimensional Model
      ↓
SCD Type 2
      ↓
Fact Loading
      ↓
Analytics
```

## Business Domain

**Manufacturing Industry**

## Selected Business Process

**Production Operations Analytics**

The Data Warehouse analyses manufacturing production events. The selected process measures production quantity, cost, time, defects, machine performance, factory performance and shift performance.

## Data Warehouse Design

### Fact Table

`Fact_Production`

**Grain:** One row represents one completed production event for one product, produced by one machine, handled by one employee, during one shift, at one factory, on one production date.

### Dimensions

- `Dim_Date`
- `Dim_Product`
- `Dim_Machine`
- `Dim_Factory`
- `Dim_Employee`
- `Dim_Shift`

### Measures

- Quantity Produced
- Production Cost
- Production Time
- Defect Count

Generated measures:

- Good Quantity
- Defect Rate
- Cost Per Unit

## ETL Implementation

Implemented pipeline:

```text
Source CSV Files
        ↓
Staging Layer
        ↓
Validation and Cleaning
        ↓
Transformation
        ↓
Dimension Loading
        ↓
SCD Type 2 Processing
        ↓
Fact Production Loading
        ↓
Validation
```

## SCD Type 2 Demonstration

`Dim_Machine` uses SCD Type 2.

Two executions are demonstrated:

| Execution | Scenario |
|---|---|
| Run 1 | Initial warehouse loading |
| Run 2 | Changed machine assignment, new machine record and unchanged records |

This demonstrates:

- Historical records
- Surrogate key changes
- New records
- Changed records
- Unchanged records
- Incremental loading

## Technology Stack

- PostgreSQL
- Python
- Pandas
- SQLAlchemy
- SQL
- GitHub Actions
- Power BI

## Repository Structure

```text
oltp_database/       Source database scripts
warehouse_database/  Star schema implementation
source_data/         Run 1 and Run 2 source states
etl_pipeline/        ETL implementation
analytics/           Analytical SQL queries
documentation/       Design and project documentation
.github/             Automated validation workflow
```

## Milestone Status

| Milestone | Status |
|---|---|
| 1. Project Foundation | Complete |
| 2. Business Requirements and DW Design | Complete |
| 3. OLTP and Warehouse Database Implementation | Complete |
| 4. ETL Pipeline Development | Complete |
| 5. Two ETL Runs and SCD Type 2 Demonstration | Complete |
| 6. Analytical Queries and Dashboard Design | Complete |
| 7. Final Report and Evidence Package | In Progress |

## Assignment Alignment

The implementation satisfies the major CCS3307 requirements:

✅ One selected business process

✅ One Fact Table

✅ Fact grain definition

✅ Dimension modelling

✅ Surrogate keys

✅ SCD Type 2 implementation

✅ Staging layer

✅ ETL pipeline

✅ Two pipeline executions

✅ Historical data demonstration

✅ Analytical queries

✅ Business value demonstration

## Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run ETL executions:

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_1 --run-date 2026-08-01
python etl_pipeline/run_etl.py --source-dir source_data/run_2 --run-date 2026-08-15
```

## Current Stage

Milestones 1-6 are completed. The remaining work is final report preparation, screenshots, Power BI evidence and submission packaging.
