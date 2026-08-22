# Enterprise Manufacturing Data Warehouse

[![Milestone 5 ETL and SCD Demonstration](https://github.com/akindaG/Enterprise-Manufacturing-Data-Warehouse/actions/workflows/milestone5-etl-demo.yml/badge.svg)](https://github.com/akindaG/Enterprise-Manufacturing-Data-Warehouse/actions/workflows/milestone5-etl-demo.yml)

## CCS3307 Data Warehousing Project

A complete Data Warehouse implementation for the **Manufacturing domain**, demonstrating the complete lifecycle required for a Data Warehousing solution:

```text
Business Domain
        ↓
Business Requirements
        ↓
Source Systems
        ↓
Dimensional Modelling
        ↓
ETL Pipeline
        ↓
SCD Type 2 Historical Tracking
        ↓
Analytical Queries
        ↓
Business Insights
```

## 1. Business Domain

**Manufacturing Industry**

## 2. Selected Business Process

**Production Operations Analytics**

The Data Warehouse focuses on manufacturing production events.

One fact record represents one completed production event for a product, machine, employee, shift and factory at a specific production date.

The warehouse supports analysis of:

- Production volume trends
- Factory performance
- Machine performance
- Product performance
- Production cost
- Quality and defects
- Historical machine changes

## 3. Data Warehouse Design

### Fact Table

`Fact_Production`

### Grain

One row represents one production event:

```text
One product produced
by one machine
handled by one employee
in one shift
at one factory
on one production date
```

### Dimensions

- Dim_Date
- Dim_Product
- Dim_Machine
- Dim_Factory
- Dim_Employee
- Dim_Shift

### Measures

- Quantity_Produced
- Production_Cost
- Production_Time
- Defect_Count

Generated analytical measures:

- Good Quantity
- Defect Rate
- Cost Per Unit
- Machine Efficiency

## 4. Architecture

```text
Operational Source Data
        ↓
Staging Layer
        ↓
Cleaning and Transformation
        ↓
Dimension Loading
        ↓
SCD Type 2 Processing
        ↓
Fact Loading
        ↓
PostgreSQL Data Warehouse
        ↓
Analytics / Reporting
```

## 5. Technology Stack

- Python 3.12
- Pandas
- SQLAlchemy
- PostgreSQL
- SQL
- GitHub Actions
- Power BI

Technology was selected because it provides a reproducible, cost-free implementation suitable for demonstrating ETL, dimensional modelling, surrogate keys, SCD and analytical reporting.

## 6. Slowly Changing Dimension Implementation

`Dim_Machine` uses **SCD Type 2**.

The pipeline demonstrates:

### First ETL Execution

```text
M001 → Colombo Factory
M002 → Kandy Factory
```

### Second ETL Execution

```text
M001 → Kandy Factory (Changed)
M002 → Kandy Factory (Unchanged)
M003 → Colombo Factory (New)
```

The previous M001 record remains in the warehouse while a new surrogate-key version becomes the current record.

## 7. ETL Pipeline

Implemented components:

```text
etl_pipeline/
├── extract.py
├── staging.py
├── transform.py
├── dimension_loader.py
├── scd_type2.py
├── fact_loader.py
├── validation.py
└── run_etl.py
```

The pipeline performs:

1. Extract source data
2. Load staging data
3. Validate data quality
4. Clean and transform data
5. Load dimensions
6. Generate surrogate keys
7. Apply SCD logic
8. Load Fact_Production
9. Validate warehouse results

## 8. Repository Structure

```text
.github/workflows/       Automated ETL verification
documentation/           Design decisions and reports
etl_pipeline/            ETL implementation
oltp_database/           Operational database scripts
source_data/             Run 1 and Run 2 source states
warehouse_database/      Star schema implementation
analytics/               Analytical SQL queries
```

## 9. Milestone Progress

| Milestone | Status |
|---|---|
| Milestone 1: Project Foundation | Complete |
| Milestone 2: Requirements and Warehouse Design | Complete |
| Milestone 3: Database Implementation | Complete |
| Milestone 4: ETL Pipeline Development | Complete |
| Milestone 5: Two ETL Runs and SCD Demonstration | Complete |
| Milestone 6: Analytical Queries and Dashboard | In Progress |

## 10. Alignment With CCS3307 Requirements

This project demonstrates:

✅ Selected business domain and business process

✅ Single Fact Table design

✅ Fact grain definition

✅ Appropriate measures and generated measures

✅ Dimension modelling

✅ Surrogate keys

✅ SCD Type 2 historical tracking

✅ Source database documentation

✅ Staging layer

✅ ETL pipeline

✅ Two pipeline executions with different source states

✅ Historical data preservation

✅ Analytical queries and business value demonstration

## 11. Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run ETL:

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_1 --run-date 2026-08-01
```

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_2 --run-date 2026-08-15
```

Run analytical queries:

```bash
psql -U postgres -d manufacturing_dw -f analytics/production_kpi_analysis.sql
```

## Current Status

Milestones 1-5 are completed. Milestone 6 dashboard implementation and final evidence preparation are in progress.
