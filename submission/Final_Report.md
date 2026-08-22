# Final Report

# Enterprise Manufacturing Data Warehouse

## 1. Introduction

Manufacturing organizations generate large amounts of production data from operational systems. This project develops a Data Warehouse to transform operational production information into analytical insights.

## 2. Business Process

Selected process:

**Production Operations**

One fact record represents one production event for a product, machine, factory, employee and shift at a specific date and time.

## 3. Data Warehouse Architecture

Source Systems → Staging → ETL → Data Warehouse → Analytics

## 4. Dimensional Model

Fact Table:

- Fact_Production

Dimensions:

- Dim_Date
- Dim_Product
- Dim_Machine
- Dim_Factory
- Dim_Employee
- Dim_Shift

## 5. ETL Implementation

The pipeline performs:

1. Extraction
2. Data validation
3. Transformation
4. Dimension loading
5. SCD Type 2 processing
6. Fact loading

## 6. Slowly Changing Dimension

Dim_Machine implements SCD Type 2 to preserve historical machine changes.

The pipeline demonstrates two executions:

- Initial warehouse load
- Incremental load after source changes

## 7. Analytics

The warehouse supports:

- Production KPIs
- Factory analysis
- Machine efficiency analysis
- Product performance analysis

## 8. Conclusion

The completed Data Warehouse provides a scalable foundation for manufacturing intelligence and reporting.
