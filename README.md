# Enterprise Manufacturing Data Warehouse

## Overview

An academic and portfolio-grade Data Warehouse implementation for CCS3307 Data Warehousing.

The project demonstrates the complete Data Warehouse lifecycle for a manufacturing organization:

```
Business Requirements
        ↓
Operational Data Sources
        ↓
ETL Pipeline
        ↓
Dimensional Data Warehouse
        ↓
Analytics Dashboard
```

## Business Domain

Manufacturing Industry

## Selected Business Process

**Production Operations Analytics**

The warehouse focuses on analysing manufacturing production events including:

- Production quantity
- Production cost
- Production time
- Defect analysis
- Factory performance
- Machine performance

## Data Warehouse Design

### Fact Table

`Fact_Production`

Grain:

> One row represents one production event for one product, produced by one machine, handled by one employee, during one shift, at one factory on a specific date.

### Dimensions

- Dim_Date
- Dim_Product
- Dim_Machine
- Dim_Factory
- Dim_Employee
- Dim_Shift

## Technology Stack

- PostgreSQL
- Python ETL
- Pandas
- SQL
- Power BI
- GitHub

## Project Structure

```
documentation/
source_data/
oltp_database/
staging_layer/
data_warehouse/
etl_pipeline/
analytics/
powerbi_dashboard/
```

## Development Roadmap

- [x] Repository initialization
- [ ] Business requirements documentation
- [ ] OLTP database design
- [ ] Star schema implementation
- [ ] ETL pipeline development
- [ ] SCD Type 2 implementation
- [ ] Analytics dashboard
- [ ] Portfolio enhancements
