# Final Evidence Checklist

The lecturer requires evidence that the pipeline is actually executed at least twice and that historical/SCD behaviour can be observed. Do not replace real execution evidence with fabricated screenshots.

## Evidence Generated Automatically

Every successful GitHub Actions run uploads an artifact named:

`milestone5-etl-evidence`

It contains:

- `etl_run_log.csv` . proves two successful pipeline executions
- `dim_machine_history.csv` . proves M001 historical versions and surrogate-key change
- `fact_history.csv` . proves facts resolve the historically correct Machine_Key
- `analytical_results.txt` . query output from the completed warehouse

## Screenshots to Capture for the Final Report

Save the real screenshots in this folder using these names:

1. `01_github_actions_success.png` . successful workflow run
2. `02_etl_run_1.png` . first ETL execution output
3. `03_dim_machine_after_run_1.png` . initial machine dimension state
4. `04_source_run_2_change.png` . M001 changed, M002 unchanged, M003 new
5. `05_etl_run_2.png` . second ETL execution output
6. `06_dim_machine_scd_history.png` . both M001 versions with effective/expiry/current fields
7. `07_fact_historical_keys.png` . PR001 and PR003 using different M001 surrogate keys
8. `08_analytical_results.png` . KPI/query output
9. `09_powerbi_executive_overview.png` . dashboard overview
10. `10_powerbi_factory_analysis.png`
11. `11_powerbi_machine_analysis.png`
12. `12_powerbi_product_analysis.png`

## README Evidence Gallery

The root README deliberately links to this checklist rather than embedding nonexistent images. Once the screenshots above are captured and committed, replace the evidence-status table in the root README with the actual Markdown image links.

This keeps the repository academically defensible: every image shown in the final submission will correspond to a real execution or real dashboard state.
