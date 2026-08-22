# Milestone 6 . Power BI Dashboard Design

## Objective

Transform the PostgreSQL star schema into decision-support analytics for manufacturing managers. The warehouse analytics and dashboard specification are complete; the final binary `.pbix` must be authored in Power BI Desktop from the real warehouse.

## Data Model

Power BI should connect to:

- `Fact_Production`
- `Dim_Date`
- `Dim_Product`
- `Dim_Machine`
- `Dim_Factory`
- `Dim_Employee`
- `Dim_Shift`

Relationships are one-to-many from each dimension surrogate key to the corresponding fact foreign key, with single-direction dimension-to-fact filtering.

## Dashboard Page 1 . Executive Production Overview

KPIs:

- Production Events
- Total Units
- Total Cost
- Total Defects
- Good Units
- Defect Rate
- Cost Per Unit

Visuals:

- monthly production trend
- factory output comparison
- product output comparison

## Dashboard Page 2 . Factory Performance

Purpose: compare output, cost and quality across manufacturing locations.

Visuals:

- output by factory
- defects and defect rate by factory
- production cost by factory
- cost per unit by factory

## Dashboard Page 3 . Machine Efficiency and History

Purpose: analyse equipment productivity and demonstrate historical correctness.

Visuals:

- units per production minute
- output by machine
- defects by machine
- SCD history table for M001 showing historical factory assignment

## Dashboard Page 4 . Product and Shift Analysis

Visuals:

- product output ranking
- product cost contribution
- product defect rate
- output by shift
- shift defect rate

## Business Questions Answered

1. Which factory produces the highest volume?
2. Which factory has the lowest defect rate?
3. Which machines have the best output per production minute?
4. Which products contribute the most production volume?
5. Which products or shifts show higher defect rates?
6. How does production change over time?
7. What was M001's historical assignment for each production event?

## DAX Measures

The implementation-ready measures are version controlled in:

`powerbi_dashboard/measures.dax`

## Final Dashboard Artifact

Create and commit:

`powerbi_dashboard/Enterprise_Manufacturing_Analytics.pbix`

Then capture the real dashboard screenshots using the filenames defined in `submission/evidence/README.md`.
