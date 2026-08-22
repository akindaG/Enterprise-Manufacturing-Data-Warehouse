# Power BI Dashboard Implementation

This folder contains the implementation specification for the final analytics dashboard.

## Required Final File

`Enterprise_Manufacturing_Analytics.pbix`

The `.pbix` must be created in Power BI Desktop from the PostgreSQL star schema. It is intentionally not fabricated in the repository. After authoring, commit the real file here because `.gitignore` allows final `.pbix` deliverables.

## Data Model

Import or DirectQuery the following warehouse tables:

- `Fact_Production`
- `Dim_Date`
- `Dim_Product`
- `Dim_Machine`
- `Dim_Factory`
- `Dim_Employee`
- `Dim_Shift`

Create one-to-many relationships from each dimension surrogate key to the corresponding fact foreign key. Filter direction should normally remain single direction from dimension to fact.

## Dashboard Pages

### 1. Executive Production Overview

Cards:

- Total Units
- Total Cost
- Total Defects
- Good Units
- Defect Rate
- Cost Per Unit
- Production Events

Visuals:

- monthly output trend
- output by factory
- output by product

### 2. Factory Performance

- production output by factory
- total cost by factory
- defect rate by factory
- cost per unit by factory

### 3. Machine Efficiency and History

- units per production minute
- output by machine
- defects by machine
- table showing M001 historical factory assignments and SCD dates

### 4. Product and Shift Analysis

- output by product
- product defect rate
- shift output
- shift defect rate

## DAX

Reusable DAX measures are stored in `measures.dax`.

## Evidence

After the dashboard is complete, capture the four dashboard pages and save them under `submission/evidence/` using the filenames defined in `submission/evidence/README.md`.
