# Milestone 4: ETL Pipeline Development

This folder contains the ETL implementation layer for the Manufacturing Data Warehouse.

Pipeline flow:

Source Systems
→ Staging Layer
→ Transformation
→ Dimension Loading
→ SCD Type 2 Processing
→ Fact Loading
→ Validation

## Components

- extract.py: Extract data from operational sources
- staging.py: Load raw extracted data into staging tables
- transform.py: Clean and standardize source data
- dimension_loader.py: Load warehouse dimensions and generate surrogate keys
- scd_type2.py: Handle historical dimension changes
- fact_loader.py: Load Fact_Production records
- validation.py: Perform ETL quality checks
