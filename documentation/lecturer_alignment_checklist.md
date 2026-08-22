# CCS3307 Lecturer Requirement Alignment Checklist

This checklist maps the repository to the requirements in the **Data Warehousing Project - Complete Project Guidelines**.

| Guideline requirement | Repository evidence | Status |
|---|---|---|
| Selected business domain | Manufacturing Industry in `documentation/business_requirements.md` | Complete |
| Major domain processes identified | Business requirements document | Complete |
| One selected business process | Production Operations Analytics | Complete |
| Need for a Data Warehouse | Business requirements document | Complete |
| Analytical requirements and business value | Business requirements and analytics documents | Complete |
| Data source identification | `documentation/source_system_analysis.md` | Complete |
| Data source rationale and integration | source system analysis | Complete |
| Source/OLTP database | `oltp_database/` and `documentation/oltp_design.md` | Complete |
| One Fact Table | `Fact_Production` | Complete |
| Fact grain defined before measures | `documentation/grain_definition.md` | Complete |
| Source measures explained | warehouse and business-requirements documents | Complete |
| Generated/calculated measures | Good Quantity, Defect Rate, Cost Per Unit | Complete |
| Required dimensions identified | Date, Product, Machine, Factory, Employee, Shift | Complete |
| Dimension attributes and purpose | `documentation/warehouse_design.md` | Complete |
| Surrogate keys | dimension DDL plus ETL lookups | Complete |
| SCD selection and rationale | `documentation/scd_strategy.md` | Complete |
| SCD Type 2 implementation | `Dim_Machine` and `run_etl.py` | Complete |
| Staging layer | `stg_*` tables created by ETL | Complete |
| Validation/cleaning/transformation | `run_etl.py` | Complete |
| Dimensions loaded before fact | ETL orchestration | Complete |
| Correct fact surrogate-key lookup | standard dimension lookups plus date-aware machine lookup | Complete |
| Technology selection | PostgreSQL, Python, Pandas, SQLAlchemy, GitHub Actions, Power BI design | Complete |
| Schema rationale | star-schema rationale in warehouse design | Complete |
| First pipeline execution | `source_data/run_1` | Complete |
| Second changed source execution | `source_data/run_2` | Complete |
| New/changed/unchanged demonstration | M003 new, M001 changed, M002 unchanged | Complete |
| Historical/SCD demonstration | M001 F001 then F002 versions | Complete |
| Incremental fact loading | `Production_ID` idempotency | Complete |
| Analytical queries | `analytics/production_kpi_analysis.sql` | Complete |
| Analytical results | `documentation/analytical_results.md` and CI evidence artifact | Complete |
| Architecture documentation | README diagrams and `submission/Architecture_Documentation.md` | Complete |
| Testing and validation | GitHub Actions workflow assertions | Complete |
| Code and source data | repository implementation files | Complete |
| Final detailed report | `submission/Final_Report.md` draft aligned to all 35 headings | Draft complete |
| Actual Power BI `.pbix` | `powerbi_dashboard/` contains implementation specification and DAX; binary file requires Power BI authoring | Pending |
| Execution/dashboard screenshots | `submission/evidence/README.md` defines required evidence; CI produces downloadable text/CSV evidence | Pending manual capture |
| Final ZIP submission | package after report, PBIX and screenshots are final | Pending |

## Current Conclusion

The repository covers the complete Data Warehouse design and implementation lifecycle required by the lecturer. Remaining items are final presentation artifacts rather than missing warehouse logic: the authored Power BI `.pbix`, screenshots from real executions/dashboard pages, and the final ZIP/PDF export.
