# Repository Quality Audit

## Audit Scope

The repository was reviewed against the CCS3307 Data Warehousing project guidelines, including the root configuration, GitHub Actions workflow, analytical SQL, design documentation, ETL modules, OLTP scripts, source-state CSV files, submission documents and warehouse DDL.

## Technical Corrections Applied

1. Removed `CREATE DATABASE` from the OLTP schema script because PostgreSQL does not automatically switch the connection after database creation.
2. Added explicit OLTP data-quality constraints and made Run 1 sample data consistent with the CSV demonstration state.
3. Added `.env.example` and ensured `.gitignore` explicitly allows that template to be versioned.
4. Added `python-dotenv` and environment-driven database configuration to the ETL.
5. Added referential-integrity and source-consistency validation before warehouse loading.
6. Strengthened warehouse dimension constraints and added a single-current-version rule for SCD Type 2 machines.
7. Added `Machine_Status` to `Dim_Machine` so the documented SCD rationale and source attributes are represented consistently.
8. Kept `Production_ID` as a unique degenerate dimension for traceability and safe incremental loading.
9. Extended analytical SQL to include generated measures, factory, product, machine, monthly, shift and historical analysis.
10. Extended GitHub Actions to compile all ETL modules, validate both executions and upload reproducible ETL/warehouse evidence.
11. Corrected documentation terminology so the operational PostgreSQL model and reproducible CSV source snapshots are described consistently.
12. Expanded the final report structure to match the lecturer's requested report sections.

## Repository Layer Review

| Layer | Review result |
|---|---|
| Root configuration | aligned; environment template and setup guidance present |
| `.github/workflows` | automated PostgreSQL two-run ETL and evidence generation |
| `oltp_database` | normalized source schema, relationships and representative Run 1 data |
| `source_data` | reproducible Run 1 and Run 2 states with changed/new/unchanged records |
| `warehouse_database` | one fact table, six dimensions, surrogate keys and SCD constraints |
| `etl_pipeline` | extraction, staging, validation, transformation, dimensions, SCD and fact loading |
| `analytics` | KPI, generated-measure and historical queries |
| `documentation` | business, source, grain, dimensions, SCD, ETL, dashboard and alignment rationale |
| `powerbi_dashboard` | dashboard specification and DAX measures; `.pbix` still requires Power BI authoring |
| `submission` | final-report draft, architecture documentation and evidence checklist |

## Remaining Manual Artifacts

The following cannot be truthfully generated merely by adding source code and therefore remain final manual evidence tasks:

- actual Power BI `.pbix` file
- screenshots of real local/CI ETL executions
- Power BI dashboard screenshots
- final PDF export of the reviewed report
- final presentation deck and ZIP submission

These are presentation/submission artifacts. The Data Warehouse implementation itself is represented and testable in the repository.
