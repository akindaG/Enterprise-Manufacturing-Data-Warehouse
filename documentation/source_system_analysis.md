# Source System Analysis

## 1. Source Architecture

The project models a normalized PostgreSQL operational database named `manufacturing_oltp` as the business source. For the reproducible two-run ETL demonstration, the relevant operational state is represented by CSV extracts under `source_data/run_1/` and `source_data/run_2/`.

The CSV files are **snapshots/extracts of the operational entities**, not six unrelated business systems. This design keeps the source model academically clear while making the two required source states easy to reproduce in GitHub Actions and on another computer.

```text
Manufacturing OLTP
        |
        | relevant operational extracts
        v
CSV Source-State Snapshots
        |
        v
Python ETL -> Staging -> Data Warehouse
```

## 2. Source Tables and Selection Rationale

| Source | What it contains | Why required | Warehouse target | Main transformations |
|---|---|---|---|---|
| `Product` / `products.csv` | product ID, name, category, unit cost | describes the product produced | `Dim_Product` | trim text, validate key, Type 1 master-data update |
| `Factory` / `factories.csv` | factory ID, name, location, capacity | supports location and factory performance analysis | `Dim_Factory` | validate capacity and key, Type 1 update |
| `Machine` / `machines.csv` | machine ID, name, type, assigned factory, status | supports equipment analysis and historical assignment tracking | `Dim_Machine` | change detection, surrogate key generation, SCD Type 2 |
| `Employee` / `employees.csv` | employee ID, name, department, role | supports workforce context for production events | `Dim_Employee` | trim text, validate key, Type 1 update |
| `Shift` / `shifts.csv` | shift ID, name, start and end times | supports shift-level analysis | `Dim_Shift` | validate key and time values, Type 1 update |
| `Production_Order` / `production_orders.csv` | completed production event and measures | represents the selected Production Operations business process | `Fact_Production` | date parsing, quality checks, dimension SK lookups, incremental load |

## 3. Relevant Source Attributes

### Product

- `Product_ID` . primary/business key
- `Product_Name`
- `Category`
- `Unit_Cost`

### Factory

- `Factory_ID` . primary/business key
- `Factory_Name`
- `Location`
- `Capacity`

### Machine

- `Machine_ID` . primary/business key
- `Machine_Name`
- `Machine_Type`
- `Factory_ID` . assigned factory
- `Status`

### Employee

- `Employee_ID` . primary/business key
- `Employee_Name`
- `Department`
- `Role`

### Shift

- `Shift_ID` . primary/business key
- `Shift_Name`
- `Start_Time`
- `End_Time`

### Production_Order

- `Production_ID` . transaction identifier
- `Product_ID`
- `Machine_ID`
- `Factory_ID`
- `Employee_ID`
- `Shift_ID`
- `Production_Date`
- `Quantity`
- `Production_Time`
- `Production_Cost`
- `Defect_Count`

## 4. Source Integration

`Production_Order` provides the transaction grain. Its business keys connect each production event to the Product, Machine, Factory, Employee and Shift master data. `Production_Date` supplies the Date dimension key.

The ETL validates these source relationships before loading. It rejects unknown product, machine, factory, employee or shift identifiers and checks that the production event factory agrees with the machine assignment in that source snapshot.

## 5. Two Source States

`run_1` represents the initial operational state. `run_2` represents the later state required by the assignment.

The second state deliberately contains:

- **changed:** M001 moves from F001 to F002
- **unchanged:** M002 remains at F002
- **new:** M003 is introduced at F001
- **incremental transactions:** PR003 and PR004 are added

This design allows the pipeline to demonstrate SCD history, surrogate-key changes, new records, unchanged records and incremental fact loading.
