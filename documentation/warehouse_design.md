# Data Warehouse Design

## Modelling Approach

The warehouse follows the **Kimball dimensional modelling approach** using a star schema. The selected business process is Manufacturing Production Operations, represented by one central fact table surrounded by descriptive dimensions.

## Fact Table

### Fact_Production

**Grain:** one row represents one completed production event for one product, produced by one machine, handled by one employee, during one shift, at one factory, on one production date.

Columns:

- `Production_Key` - warehouse surrogate primary key
- `Production_ID` - source transaction identifier retained as a degenerate dimension
- `Date_Key`
- `Product_Key`
- `Machine_Key`
- `Factory_Key`
- `Employee_Key`
- `Shift_Key`
- `Quantity_Produced`
- `Production_Cost`
- `Production_Time`
- `Defect_Count`

`Production_ID` is not a foreign key. It provides source traceability and a stable idempotency key for incremental ETL loading, preventing legitimate production events with identical measures from being incorrectly treated as duplicates.

## Measures and Additivity

| Measure | Source | Additivity | Analytical Purpose |
|---|---|---|---|
| `Quantity_Produced` | Production source quantity | Additive | Total production volume |
| `Production_Cost` | Production source cost | Additive | Total manufacturing cost |
| `Production_Time` | Production source time | Additive across disjoint events | Total production minutes and average duration |
| `Defect_Count` | Production source defects | Additive | Total defective units |

Generated analytical measures are calculated from additive base measures:

- `Good_Quantity = Quantity_Produced - Defect_Count`
- `Defect_Rate = SUM(Defect_Count) / SUM(Quantity_Produced) * 100`
- `Cost_Per_Unit = SUM(Production_Cost) / SUM(Quantity_Produced)`

`Defect_Rate` and `Cost_Per_Unit` are non-additive ratios and should be recalculated at the requested aggregation level rather than summed.

## Dimension Tables

### Dim_Date

- `Date_Key`
- `Full_Date`
- `Day`
- `Month`
- `Quarter`
- `Year`

### Dim_Product

- `Product_Key` - surrogate key
- `Product_ID` - business key
- `Product_Name`
- `Category`
- `Unit_Cost`

### Dim_Machine

- `Machine_Key` - surrogate key
- `Machine_ID` - business key
- `Machine_Name`
- `Machine_Type`
- `Factory_ID` - assigned/home factory at that version
- `Effective_Date`
- `Expiry_Date`
- `Is_Current`

`Dim_Machine` is managed as **SCD Type 2**. A change to a tracked attribute expires the previous version and inserts a new version with a new `Machine_Key`.

### Dim_Factory

- `Factory_Key`
- `Factory_ID`
- `Factory_Name`
- `Location`
- `Capacity`

### Dim_Employee

- `Employee_Key`
- `Employee_ID`
- `Employee_Name`
- `Department`
- `Role`

### Dim_Shift

- `Shift_Key`
- `Shift_ID`
- `Shift_Name`
- `Start_Time`
- `End_Time`

## Factory Context Design Decision

`Fact_Production.Factory_Key` stores the **actual factory where the production event occurred**. `Dim_Machine.Factory_ID` stores the machine's **assigned factory for that historical machine version**. Keeping both is intentional. It allows the warehouse to compare actual event location with the machine's historical assignment and to preserve machine transfer history.

## Key Strategy

All business dimensions use warehouse surrogate keys in the fact table. Natural business identifiers remain inside dimensions for source matching. During fact loading, the ETL performs surrogate-key lookups after dimension loading. For `Dim_Machine`, the lookup also uses the production date so the fact references the correct historical SCD version.

## Star Schema Rationale

A star schema was selected because the project focuses on one production business process and requires straightforward analytical queries across products, machines, factories, employees, shifts and dates. The denormalized dimensional structure reduces join complexity and is well suited to OLAP and Power BI reporting.
