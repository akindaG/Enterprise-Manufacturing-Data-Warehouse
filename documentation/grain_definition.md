# Fact Table Grain Definition

## Fact Table

`Fact_Production`

## Declared Grain

One row represents **one completed production event** for one product, produced by one machine, handled by one employee, during one shift, at one factory, on one production date.

The grain is defined before selecting measures and dimensions so every fact row has one unambiguous business meaning.

## Transaction Identifier

`Production_ID` is retained from the source system as a **degenerate dimension**. It does not require a separate dimension table because it has no descriptive attributes needed for analysis.

It is retained for three reasons:

1. source-to-warehouse traceability
2. reliable incremental-load de-duplication
3. preservation of distinct production events even when all measures and dimension keys happen to be identical

The warehouse also uses `Production_Key` as its internal surrogate primary key.

## Dimension Relationships at This Grain

Each fact row resolves exactly one key from each analytical dimension:

- `Date_Key`
- `Product_Key`
- `Machine_Key`
- `Factory_Key`
- `Employee_Key`
- `Shift_Key`

For the SCD Type 2 `Dim_Machine`, the ETL resolves the `Machine_Key` that was valid on the production date. This ensures historical facts remain associated with the correct machine version after a factory-assignment change.

## Base Measures

| Measure | Additivity | Meaning |
|---|---|---|
| `Quantity_Produced` | Additive | Units produced in the event |
| `Production_Cost` | Additive | Cost incurred by the event |
| `Production_Time` | Additive across disjoint events | Production minutes |
| `Defect_Count` | Additive | Defective units recorded in the event |

## Derived Measures

The analytical layer can derive:

- `Good_Quantity = Quantity_Produced - Defect_Count`
- `Defect_Rate = SUM(Defect_Count) / SUM(Quantity_Produced) * 100`
- `Cost_Per_Unit = SUM(Production_Cost) / SUM(Quantity_Produced)`

`Defect_Rate` and `Cost_Per_Unit` are non-additive ratios and must be recalculated for each requested aggregation level.

## Why This Grain Was Selected

Event-level grain preserves the most detailed production information available for the selected business process. It supports aggregation by date, product, machine, factory, employee and shift without losing detail. It also supports historical machine analysis before and after SCD Type 2 changes.

A coarser daily or monthly grain would reduce flexibility and make it impossible to distinguish individual production events or safely perform incremental loading by `Production_ID`.
