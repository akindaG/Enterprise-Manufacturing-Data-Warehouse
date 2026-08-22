# CCS3307 Lecturer Requirement Alignment Checklist

## Domain and Process

| Requirement | Implementation |
|---|---|
| Select business domain | Manufacturing Industry |
| Select one business process | Production Operations Analytics |
| Explain business value | Production, cost, quality and performance analysis |

## Dimensional Modelling

| Requirement | Implementation |
|---|---|
| One Fact Table | Fact_Production |
| Grain definition | One production event per product, machine, employee, shift, factory and date |
| Dimensions | Date, Product, Machine, Factory, Employee, Shift |
| Surrogate keys | Implemented in dimension tables |
| Schema | Star Schema |

## ETL Requirements

| Requirement | Implementation |
|---|---|
| Source systems | CSV operational sources |
| Staging layer | Included in ETL flow |
| Extraction | Python extraction scripts |
| Transformation | Cleaning and validation |
| Dimension loading | Implemented before fact loading |
| Fact loading | Surrogate key resolution implemented |

## SCD Requirements

| Requirement | Implementation |
|---|---|
| Identify changing dimensions | Dim_Machine |
| SCD approach | Type 2 |
| Historical versions | Maintained using effective dates and current flags |
| Two executions | Run 1 and Run 2 source states |

## Analytical Demonstration

| Requirement | Implementation |
|---|---|
| Analytical queries | Production KPI SQL |
| Historical analysis | SCD-aware queries |
| Business insights | Documented in Milestone 6 |
| Dashboard preparation | Power BI design completed |

## Final Submission Remaining Items

- Capture execution screenshots
- Prepare final report
- Export Power BI dashboard
- Package ZIP submission
