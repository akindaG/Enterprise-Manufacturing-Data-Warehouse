# Power BI Dashboard Implementation

This folder contains the controlled implementation package for the final manufacturing analytics dashboard.

## Final Deliverable

Create the real Power BI Desktop file as:

```text
Enterprise_Manufacturing_Analytics.pbix
```

The `.pbix` must be created from the validated PostgreSQL warehouse. Do not commit a placeholder file with a `.pbix` extension.

## Files in This Folder

| File | Purpose |
|---|---|
| `README.md` | dashboard implementation overview |
| `build_guide.md` | step-by-step build and validation procedure |
| `measures.dax` | reusable Power BI DAX measures |
| `theme.json` | professional dashboard theme |
| `Enterprise_Manufacturing_Analytics.pbix` | real final dashboard, to be authored in Power BI Desktop |

Warehouse-side validation is provided by:

```text
analytics/powerbi_validation.sql
```

## Data Model

Import these seven analytical warehouse tables:

- `Fact_Production`
- `Dim_Date`
- `Dim_Product`
- `Dim_Machine`
- `Dim_Factory`
- `Dim_Employee`
- `Dim_Shift`

Create one-to-many relationships from each dimension surrogate key to the matching fact foreign key. Use single-direction filtering from dimension to fact.

Do not import `stg_*` tables into the Power BI semantic model. Staging tables are ETL implementation evidence, not reporting dimensions.

## Dashboard Pages

### 1. Executive Production Overview

KPI cards:

- Total Units
- Good Units
- Total Defects
- Defect Rate
- Total Cost
- Cost Per Unit
- Production Events

Visuals:

- production trend
- output by factory
- output by product

### 2. Factory Performance

- production output by factory
- total cost by factory
- defect rate by factory
- cost per unit by factory
- comparative KPI matrix

### 3. Machine Efficiency and SCD History

- units per production minute
- output by machine
- defects by machine
- historical table showing both M001 SCD Type 2 versions

### 4. Product and Shift Analysis

- output by product
- product defect rate
- output by shift
- shift defect rate
- product/shift matrix

## DAX Measures

Reusable measures are stored in `measures.dax`.

The controlled two-run warehouse should produce the following overall values:

| KPI | Expected value |
|---|---:|
| Production Events | 4 |
| Total Units | 385 |
| Total Defects | 7 |
| Good Units | 378 |
| Total Cost | 85000 |
| Defect Rate | 1.82% |
| Cost Per Unit | 220.78 |

Use `analytics/powerbi_validation.sql` to confirm these values before accepting the dashboard.

## Theme

Import `theme.json` from Power BI Desktop using:

**View > Themes > Browse for themes**

The theme is optional for correctness but recommended for a consistent professional presentation.

## Build Procedure

Follow `build_guide.md` exactly. It covers:

1. warehouse preparation
2. PostgreSQL connection
3. star-schema relationships
4. date-table configuration
5. DAX measures
6. all four dashboard pages
7. SQL-to-Power-BI validation
8. evidence screenshots
9. final completion gate

## Evidence

After the dashboard is complete, commit the actual screenshots under:

```text
submission/evidence/
```

Required dashboard evidence:

- `powerbi_executive_overview.png`
- `powerbi_factory_performance.png`
- `powerbi_machine_scd_history.png`
- `powerbi_product_shift_analysis.png`

## Completion Rule

This Power BI milestone is complete only when:

- the real `.pbix` file exists
- the model contains the seven-table star schema
- required DAX measures exist
- four dashboard pages exist
- dashboard values match SQL control totals
- M001 SCD history is visibly demonstrated
- dashboard screenshots are committed
