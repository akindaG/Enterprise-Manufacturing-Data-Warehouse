# Power BI Dashboard Build Guide

This guide converts the validated PostgreSQL star schema into the final `Enterprise_Manufacturing_Analytics.pbix` deliverable.

## 1. Prerequisites

Use Power BI Desktop on Windows. Ensure PostgreSQL is running and the warehouse has been loaded with both source states.

Run from the repository root:

```bash
pip install -r requirements.txt
python etl_pipeline/run_etl.py --source-dir source_data/run_1 --run-date 2026-08-01
python etl_pipeline/run_etl.py --source-dir source_data/run_2 --run-date 2026-08-15
```

Validate the warehouse before opening Power BI:

```bash
psql -U postgres -d manufacturing_dw -f analytics/scd_verification.sql
psql -U postgres -d manufacturing_dw -f analytics/production_kpi_analysis.sql
psql -U postgres -d manufacturing_dw -f analytics/powerbi_validation.sql
```

Expected overall control totals after the two executions:

- Production Events: 4
- Total Units: 385
- Total Defects: 7
- Good Units: 378
- Total Production Cost: 85000
- Defect Rate: approximately 1.82%
- Cost Per Unit: approximately 220.78

## 2. Connect Power BI to PostgreSQL

1. Open Power BI Desktop.
2. Select **Get Data > PostgreSQL database**.
3. Server: `localhost:5432`.
4. Database: `manufacturing_dw`.
5. Choose **Import** mode for the academic demonstration.
6. Authenticate using the PostgreSQL account configured for the project.
7. Select these seven warehouse tables only:
   - `dim_date`
   - `dim_product`
   - `dim_machine`
   - `dim_factory`
   - `dim_employee`
   - `dim_shift`
   - `fact_production`
8. Select **Load**.

Do not import `stg_*` or `etl_run_log` into the semantic model. They are ETL/staging evidence, not analytical dimensions.

## 3. Configure the Star Schema

In Model view create or verify the following relationships:

| Dimension | Dimension key | Fact key | Cardinality | Filter direction |
|---|---|---|---|---|
| Dim_Date | Date_Key | Date_Key | 1:* | Single |
| Dim_Product | Product_Key | Product_Key | 1:* | Single |
| Dim_Machine | Machine_Key | Machine_Key | 1:* | Single |
| Dim_Factory | Factory_Key | Factory_Key | 1:* | Single |
| Dim_Employee | Employee_Key | Employee_Key | 1:* | Single |
| Dim_Shift | Shift_Key | Shift_Key | 1:* | Single |

The model must remain a star schema. Do not create relationships between dimensions.

### Date configuration

1. Select `Dim_Date`.
2. Mark it as the Date Table using `Full_Date`.
3. Sort month labels by numeric month if a text month label is added later.

### Hide technical fields

Hide surrogate keys from Report view where they are not intended for end-user analysis:

- `*_Key` columns
- SCD technical dates when not used on a visual

Keep `Production_ID`, `Machine_ID`, `Factory_ID`, `Effective_Date`, `Expiry_Date`, and `Is_Current` available for traceability and the historical demonstration page.

## 4. Create Measures

Create a dedicated measure table called `Measures` if desired, then copy the DAX definitions from `powerbi_dashboard/measures.dax`.

Required measures:

- Production Events
- Total Units
- Total Cost
- Total Production Minutes
- Total Defects
- Good Units
- Defect Rate %
- Cost Per Unit
- Units Per Production Minute

Formatting:

- `Total Cost` and `Cost Per Unit`: currency/decimal as appropriate for the report context
- `Defect Rate %`: percentage with 2 decimal places. If using the provided DAX that multiplies by 100, format as a decimal number with `%` in the title, not Power BI Percentage format. Alternatively remove `* 100` and use Percentage format.
- counts/units: whole numbers
- efficiency: 2 decimal places

## 5. Apply Theme

Import `powerbi_dashboard/theme.json` using:

**View > Themes > Browse for themes**

The theme provides a consistent professional manufacturing analytics appearance. Keep accessibility and contrast more important than decoration.

## 6. Page 1. Executive Production Overview

### KPI cards

Place cards for:

- Total Units
- Good Units
- Total Defects
- Defect Rate %
- Total Cost
- Cost Per Unit
- Production Events

### Visuals

1. **Production Trend**
   - Visual: line chart
   - X-axis: `Dim_Date[Full_Date]`
   - Y-axis: `[Total Units]`

2. **Output by Factory**
   - Visual: clustered bar/column chart
   - Axis: `Dim_Factory[Factory_Name]`
   - Value: `[Total Units]`

3. **Output by Product**
   - Axis: `Dim_Product[Product_Name]`
   - Value: `[Total Units]`

### Slicers

- Date
- Factory
- Product

## 7. Page 2. Factory Performance

Visuals:

1. Total Units by Factory
2. Total Cost by Factory
3. Defect Rate % by Factory
4. Cost Per Unit by Factory
5. Matrix with Factory, Total Units, Good Units, Total Defects, Defect Rate %, Total Cost, Cost Per Unit

Business purpose: compare output, quality, and production cost across manufacturing locations.

## 8. Page 3. Machine Efficiency and SCD History

Visuals:

1. Units Per Production Minute by Machine
2. Total Units by Machine
3. Total Defects by Machine
4. Historical table for M001 containing:
   - Machine_ID
   - Machine_Name
   - Factory_ID
   - Machine_Status
   - Effective_Date
   - Expiry_Date
   - Is_Current

Use a slicer for `Machine_ID` and select M001 when capturing the SCD evidence screenshot.

The table must visibly show both historical versions of M001 after Run 2.

## 9. Page 4. Product and Shift Analysis

Visuals:

1. Total Units by Product
2. Defect Rate % by Product
3. Total Units by Shift
4. Defect Rate % by Shift
5. Matrix by Product and Shift with Total Units, Good Units, Total Defects and Total Cost

## 10. Interaction and Usability Checks

Before submission verify:

- slicers affect intended visuals
- no accidental many-to-many relationships
- no bidirectional relationship unless explicitly justified
- totals match SQL validation results
- no raw surrogate keys shown in executive visuals
- chart titles state the business meaning
- numbers use consistent formatting
- SCD historical table preserves both M001 versions

## 11. Validation Against SQL

Run `analytics/powerbi_validation.sql` and compare every dashboard control total.

The dashboard is not accepted as complete until the Power BI values agree with the SQL warehouse values.

## 12. Save the Deliverable

Save the final dashboard as:

```text
powerbi_dashboard/Enterprise_Manufacturing_Analytics.pbix
```

Commit the real `.pbix` file to GitHub. Do not create a placeholder file with that extension.

## 13. Capture Evidence

Capture these real screenshots after validation:

- `submission/evidence/powerbi_executive_overview.png`
- `submission/evidence/powerbi_factory_performance.png`
- `submission/evidence/powerbi_machine_scd_history.png`
- `submission/evidence/powerbi_product_shift_analysis.png`

Also capture ETL and SQL evidence specified in `submission/evidence/README.md`.

## 14. Completion Gate

The Power BI milestone is complete only when all of the following are true:

- real `.pbix` exists
- seven-table star schema is visible
- required DAX measures exist
- four dashboard pages exist
- control totals match SQL
- M001 history is visible
- four dashboard screenshots are committed
