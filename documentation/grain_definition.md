# Fact Table Grain Definition

## Fact Table
Fact_Production

## Grain
One row represents one production event for one product, produced by one machine, handled by one employee, during one shift, at one factory on one production date.

## Measures
- Quantity_Produced
- Production_Cost
- Production_Time
- Defect_Count

Defining the grain ensures that every record in the fact table has a clear business meaning and prevents incorrect aggregation during analysis.
