# Enterprise Manufacturing Analytics Data Warehouse

**Module:** CCS3307 Data Warehousing  
**Author:** Akinda Gunarathne

> This Markdown report is the submission-ready content draft. Final screenshots, the authored Power BI file and the final PDF export are added only after the real local/dashboard evidence has been captured.

## 1. Introduction

Manufacturing organisations generate operational records from products, factories, machines, employees, shifts and production activities. Transactional systems are designed to record operational activity efficiently, but they are not ideal for historical comparison, multidimensional analysis or repeatable management reporting. This project designs and implements an Enterprise Manufacturing Analytics Data Warehouse that converts production-event data into an analytical star schema.

## 2. Selected Business Domain

The selected domain is the **Manufacturing Industry**. Major processes in the domain can include production, inventory, procurement, maintenance, quality management and logistics. The project limits its analytical scope to one process so the fact table has a clear business meaning.

## 3. Business Requirements

Management requires consistent analysis of production volume, cost, duration, quality, factory performance, product performance, machine efficiency and shift performance. Historical machine context must remain correct after operational attributes change.

Detailed requirements are maintained in `documentation/business_requirements.md`.

## 4. Selected Business Process

The selected process is **Production Operations Analytics**. A completed production event records a product, machine, production factory, employee, shift, date, quantity, production time, production cost and defect count.

The process was selected because it is repeatable, measurable and suitable for one transaction-grain fact table.

## 5. Need for a Data Warehouse

Direct operational analysis requires repeated joins and does not naturally preserve historical versions of changing master data. The warehouse separates analytical workloads from transaction-oriented data, standardises the model, introduces surrogate keys and preserves selected machine history with SCD Type 2.

## 6. Business Value

The solution supports production optimisation, quality investigation, cost management, factory comparison, machine-performance analysis and historically correct reporting. It also creates a reproducible source-to-analytics pipeline that can be validated independently of the operational application.

## 7. Data Source Identification

The logical business source is the PostgreSQL `manufacturing_oltp` database. The ETL demonstration uses CSV extracts representing two operational source states:

- `source_data/run_1/`
- `source_data/run_2/`

Each state includes Products, Factories, Machines, Employees, Shifts and Production Orders.

## 8. Data Source Selection Rationale

The master sources provide descriptive dimension data, while Production Order provides the production-event transaction and measures. CSV snapshots make the two required executions deterministic and reproducible while remaining consistent with the documented OLTP model. Source selection and target mapping are detailed in `documentation/source_system_analysis.md`.

## 9. Source / OLTP Database

`manufacturing_oltp` contains:

- Product
- Factory
- Machine
- Employee
- Shift
- Production_Order

`Production_Order` is the transaction table for the selected process. In this synthetic source model, it represents a completed production execution event.

## 10. Source Database Schema

`Product_ID`, `Factory_ID`, `Machine_ID`, `Employee_ID`, `Shift_ID` and `Production_ID` are source primary keys. Machine references Factory. Production_Order references Product, Machine, Factory, Employee and Shift. Implementation files are under `oltp_database/` and the ER model is documented in `documentation/oltp_design.md`.

## 11. Fact Table Identification

The project contains one fact table: **`Fact_Production`**. It represents the selected Production Operations business process.

## 12. Fact Table Grain

One row represents **one completed production event for one product, produced by one machine, handled by one employee, during one shift, at one factory, on one production date**.

`Production_ID` is retained as a degenerate dimension for transaction traceability and incremental-load idempotency. The grain is documented in `documentation/grain_definition.md`.

## 13. Measures

Base measures are:

| Measure | Meaning | Additivity |
|---|---|---|
| Quantity_Produced | units produced during the event | additive |
| Production_Cost | cost incurred by the event | additive |
| Production_Time | production minutes | additive across disjoint events |
| Defect_Count | defective units | additive |

## 14. Generated / Calculated Measures

The analytical layer calculates:

- `Good_Quantity = Quantity_Produced - Defect_Count`
- `Defect_Rate = SUM(Defect_Count) / SUM(Quantity_Produced) * 100`
- `Cost_Per_Unit = SUM(Production_Cost) / SUM(Quantity_Produced)`

Defect Rate and Cost Per Unit are non-additive ratios and are recalculated at the requested aggregation level.

## 15. Dimension Identification

The dimensions are:

- `Dim_Date`
- `Dim_Product`
- `Dim_Machine`
- `Dim_Factory`
- `Dim_Employee`
- `Dim_Shift`

They answer the when, what, equipment, where, who and operational-shift questions surrounding each production event.

## 16. Dimension Attributes

Important descriptive attributes include product name/category, machine name/type/status/assigned factory, factory name/location/capacity, employee department/role and shift start/end times. `Dim_Machine` also contains effective and expiry dates plus a current flag for historical tracking.

## 17. Surrogate Key Design

Each dimension uses an integer warehouse surrogate key. Natural business keys are retained for source matching. Dimensions are processed before facts. During fact loading the ETL resolves the correct surrogate keys. `Dim_Machine` uses a date-aware lookup so facts reference the SCD version valid on the production date.

## 18. SCD Design

`Dim_Machine` is implemented as SCD Type 2. Date is fixed/Type 0. Product, Factory, Employee and Shift use Type 1 behaviour for the current project scope. The complete strategy matrix is in `documentation/scd_strategy.md`.

## 19. SCD Rationale

Machine assignment, type, status or descriptive identity can change over time and can affect interpretation of production history. Overwriting the old machine record could make historical facts appear under a later assignment. Type 2 therefore preserves historical machine versions using new surrogate keys.

## 20. Data Warehouse Schema

A **star schema** is used because the project focuses on one business process and requires simple multidimensional analysis. `Fact_Production` is the centre and each dimension connects directly to it. This reduces query complexity and is suitable for SQL analytics and Power BI.

Implementation: `warehouse_database/`  
Design rationale: `documentation/warehouse_design.md`

## 21. Staging Layer

The ETL loads cleaned source extracts to `stg_product`, `stg_factory`, `stg_machine`, `stg_employee`, `stg_shift` and `stg_production`. Staging isolates source ingestion from warehouse loading and provides an intermediate area for validation and transformation.

## 22. ETL Architecture

```text
Operational Source State
        -> Extract
        -> Clean and Validate
        -> Staging
        -> Dimension Loading
        -> SCD Type 2
        -> Surrogate-Key Resolution
        -> Fact Loading
        -> Warehouse Validation
        -> Analytics
```

The executable implementation is `etl_pipeline/run_etl.py`.

## 23. Transformation Process

The pipeline normalises column names, trims text, removes exact duplicates, validates required columns, validates business keys, converts numeric/date values, rejects negative measures, prevents defects exceeding quantity and verifies production foreign-key references. It also verifies the event factory against the machine assignment in the source state.

## 24. Dimension Loading

Date members are inserted using `YYYYMMDD` date keys. Product, Factory, Employee and Shift are loaded using Type 1 logic. Machine records are processed using Type 2 change detection. New warehouse surrogate keys are generated when new members or new machine versions are required.

## 25. Fact Table Loading

After dimensions are ready, each production event obtains Date, Product, Machine, Factory, Employee and Shift keys. Machine lookup includes the production date. `Production_ID` is checked before insertion so rerunning a source state does not duplicate facts.

## 26. Technology Selection and Rationale

- **PostgreSQL 16** . relational source/warehouse platform with strong SQL and constraint support
- **Python 3.12** . transparent ETL orchestration suitable for demonstrating each assignment step
- **Pandas** . reproducible CSV extraction and staging preparation
- **SQLAlchemy + psycopg2** . PostgreSQL connectivity and transactional execution
- **GitHub Actions** . automated reproducibility and verification of the two-run scenario
- **Power BI** . planned interactive dashboard layer using the star schema

The stack uses free/open tooling for the core implementation and makes the ETL logic directly inspectable.

## 27. Pipeline Execution . First Run

Run 1 uses `source_data/run_1` with ETL date `2026-08-01`.

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_1 --run-date 2026-08-01
```

Initial machines include M001 at F001 and M002 at F002. PR001 and PR002 are inserted as production facts.

## 28. Pipeline Execution . Second Run

Run 2 uses `source_data/run_2` with ETL date `2026-08-15`.

```bash
python etl_pipeline/run_etl.py --source-dir source_data/run_2 --run-date 2026-08-15
```

The later state demonstrates:

- M001 . changed from F001 to F002
- M002 . unchanged at F002
- M003 . new at F001
- PR003 and PR004 . new production facts

## 29. SCD Historical Data Demonstration

After Run 2, the original M001/F001 record is expired on `2026-08-14` and remains historical. A new M001/F002 version begins on `2026-08-15`. PR001 retains the old Machine_Key while PR003 resolves the new Machine_Key. This proves historical preservation rather than overwriting.

## 30. Analytical Queries / Results

`analytics/production_kpi_analysis.sql` provides enterprise KPIs, generated measures, factory analysis, product analysis, machine efficiency, monthly trends, shift analysis and historical machine comparison.

For the controlled demonstration data:

- total production = **385 units**
- total defects = **7**
- good quantity = **378 units**
- defect rate = **1.82%**
- total production cost = **85,000.00**
- cost per unit = **220.78**

Detailed results are in `documentation/analytical_results.md`.

## 31. Testing and Validation

The GitHub Actions workflow provisions PostgreSQL, creates the warehouse, executes both ETL runs and asserts:

- two successful ETL log entries
- two M001 SCD versions
- correct expired/current M001 records
- unchanged M002 remains one version
- new M003 exists
- four fact rows exist
- four unique Production_ID values exist
- PR001 uses the historical F001 machine version
- PR003 uses the new F002 machine version

The workflow also exports machine history, fact history, ETL log and analytical output as a downloadable evidence artifact.

## 32. Business Value Demonstration

The warehouse makes production data comparable across factories, products, machines, shifts and time. It can identify higher/lower defect rates, compare cost per unit, rank machine productivity and preserve historical context after machine reassignment. The SCD example demonstrates value that a current-state-only operational report cannot provide reliably.

## 33. Discussion of Results

The demonstration dataset is intentionally small because its purpose is to prove dimensional modelling, ETL behaviour, SCD history and analytical correctness. The architecture scales conceptually to larger source extracts without changing the declared fact grain. For a production deployment, additional orchestration, incremental extraction metadata, monitoring, security and larger data volumes would be added.

## 34. Conclusion

The project implements the full required Data Warehouse lifecycle for Manufacturing Production Operations: business requirements, source design, a declared fact grain, measures, dimensions, surrogate keys, SCD Type 2, staging, ETL, two source states, incremental loading, historical preservation, validation and analytical queries. Remaining submission work is limited to final visual artifacts: the authored Power BI `.pbix`, evidence screenshots, presentation materials and final PDF/ZIP packaging.

## 35. References

1. CCS3307 Data Warehousing . *Data Warehousing Project - Complete Project Guidelines*.
2. CCS3307 Data Warehousing lecture material . Data Warehousing fundamentals, OLTP/OLAP, facts, dimensions, surrogate keys, SCD and architectures.
3. CCS3307 Data Warehousing lecture material . ETL / ELT Pipeline Development.
4. PostgreSQL documentation, used for relational database and SQL implementation concepts.
5. Microsoft Power BI documentation, used as the intended dashboard implementation reference.
