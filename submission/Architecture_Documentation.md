# Architecture Documentation

## Enterprise Data Warehouse Architecture

```text
Manufacturing Source Systems
            |
            v
      Staging Layer
            |
            v
      Python ETL Pipeline
            |
            v
 PostgreSQL Data Warehouse
            |
            v
       Star Schema
            |
            v
     Analytics Layer
            |
            v
       Power BI
```

## ETL Flow

```text
Extract
  |
Transform
  |
Validate
  |
Load Dimensions
  |
Apply SCD Type 2
  |
Load Fact Table
```

## SCD Type 2 Flow

```text
Source Change
      |
      v
Detect Difference
      |
      v
Expire Previous Record
      |
      v
Create New Historical Version
```
