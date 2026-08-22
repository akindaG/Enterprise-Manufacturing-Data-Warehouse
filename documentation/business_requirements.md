# Business Requirements

## Project

**Enterprise Manufacturing Analytics Data Warehouse**

## 1. Selected Business Domain

The selected domain is the **manufacturing industry**. Manufacturing organisations generate operational data from products, factories, machines, employees, shifts and production events. The domain is suitable for a Data Warehouse because management decisions depend on analysing performance across these entities and across time rather than only viewing the current operational state.

Major business processes that may exist in this domain include production operations, inventory management, procurement, maintenance, quality management, order fulfilment and logistics.

## 2. Selected Business Process

The project deliberately focuses on **one business process: Production Operations Analytics**.

This process was selected because it produces repeatable measurable events and directly supports the assignment requirement for a single fact table. During a production event, a product is produced by a machine, at a factory, by an employee, during a shift, on a production date. The event records production quantity, production duration, production cost and defects.

The single fact table representing this process is `Fact_Production`.

## 3. Problems with Direct Operational Analysis

Operational data is designed for recording current transactions, not historical analytics. Direct analysis creates several problems:

- production data is distributed across transactional and master entities
- operational joins are repetitive and inconvenient for business users
- current master-data values can overwrite important historical context
- trend analysis requires repeated transformation of dates and measures
- comparing factories, products, machines and shifts becomes cumbersome
- slowly changing machine assignments cannot be analysed correctly without historical versions
- analytical workloads can interfere with transaction-oriented systems

## 4. Why a Data Warehouse Is Required

The Data Warehouse creates a stable analytical model separate from operational processing. It integrates production events with conformed descriptive dimensions, uses surrogate keys, preserves machine history through SCD Type 2, and exposes additive measures that can be aggregated safely for reporting.

## 5. Data Warehouse Objectives

The solution must:

1. integrate manufacturing production data into a dimensional model
2. maintain one production fact table at a clearly declared event-level grain
3. provide Date, Product, Machine, Factory, Employee and Shift dimensions
4. generate and use warehouse surrogate keys
5. include a staging layer for validation and preparation
6. preserve meaningful machine history through SCD Type 2
7. support incremental loading using `Production_ID`
8. demonstrate at least two ETL executions with changed source states
9. provide analytical SQL and dashboard-ready metrics
10. make the implementation reproducible through code, source data and documentation

## 6. Analytical Requirements and Business Questions

### Production and Time Analysis

- What is total production output?
- How does production change by month and year?
- What is the total production time?
- How many completed production events occurred?

### Factory Analysis

- Which factory produces the highest output?
- Which factory has the lowest defect rate?
- How does production cost differ by factory?
- What is the cost per unit for each factory?

### Product Analysis

- Which products have the highest production volume?
- Which products generate the most production cost?
- Which products have the highest defect rate?

### Machine Analysis

- Which machines produce the highest output?
- Which machines have the highest units per production minute?
- How did production associated with a machine change before and after a factory reassignment?

### Shift and Quality Analysis

- Which shifts produce the highest output?
- Which shifts have the highest defect rate?
- How many good units are produced after defects are removed?

## 7. Measures

Source measures:

- `Quantity_Produced`
- `Production_Cost`
- `Production_Time`
- `Defect_Count`

Generated analytical measures:

- `Good_Quantity = Quantity_Produced - Defect_Count`
- `Defect_Rate = SUM(Defect_Count) / SUM(Quantity_Produced) * 100`
- `Cost_Per_Unit = SUM(Production_Cost) / SUM(Quantity_Produced)`

The first four are additive across disjoint production events. `Defect_Rate` and `Cost_Per_Unit` are non-additive ratios and must be recalculated at each reporting level.

## 8. Business Value

The warehouse enables management to compare production performance, identify quality problems, evaluate machine efficiency, understand cost drivers, compare factory and shift performance and perform historically correct analysis after machine attributes change. This transforms operational records into repeatable decision-support information.
