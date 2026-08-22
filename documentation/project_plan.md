# Enterprise Manufacturing Data Warehouse Project Plan

## Phase 1 . Business Analysis . Complete

- define manufacturing domain and major business processes
- select Production Operations Analytics as the single process
- document business requirements, analytical questions and business value
- identify source data and selection rationale

## Phase 2 . Source / OLTP Design . Complete

- create Product, Factory, Machine, Employee, Shift and Production_Order tables
- define primary/foreign keys and relationships
- provide representative initial operational data
- provide reproducible Run 1 and Run 2 CSV extracts

## Phase 3 . Dimensional Data Warehouse . Complete

- implement `Fact_Production`
- define event-level grain
- implement Date, Product, Machine, Factory, Employee and Shift dimensions
- implement surrogate keys and foreign-key relationships
- document star-schema rationale

## Phase 4 . ETL and Historical Processing . Complete

- extract source snapshots
- clean, validate and stage data
- load dimensions before facts
- apply Type 1 updates where appropriate
- implement Machine SCD Type 2
- perform date-aware historical Machine_Key lookup
- load facts incrementally by Production_ID

## Phase 5 . Two-Run Demonstration and Testing . Complete

- Run 1 initial load
- Run 2 changed source state
- demonstrate M001 changed, M002 unchanged and M003 new
- preserve historical M001 version
- validate incremental fact loading
- automate the scenario with GitHub Actions
- export CI evidence artifact

## Phase 6 . Analytics and Dashboard Specification . Complete

- analytical KPI SQL
- generated measures
- factory, product, machine, monthly and shift analysis
- historical SCD comparison
- documented analytical results
- Power BI page/model/DAX specification

## Phase 7 . Final Submission . In Progress

Completed:

- detailed Markdown report draft aligned to lecturer headings
- architecture documentation
- evidence checklist
- repository alignment audit

Remaining manual deliverables:

- actual Power BI `.pbix`
- execution/dashboard screenshots
- final PDF export
- presentation deck
- final project ZIP

## Optional Portfolio Enhancements . After Academic Submission

Only after the required project is complete:

- Docker local environment
- Airflow orchestration
- larger synthetic data volume
- data observability metrics
- predictive-maintenance extension
