# Analytical Results After the Two-Run Demonstration

These results are derived from the four production facts in `source_data/run_1` and `source_data/run_2` and are reproducible with `analytics/production_kpi_analysis.sql`. The GitHub Actions workflow also exports query evidence as the `milestone5-etl-evidence` artifact.

## Enterprise KPIs

| KPI | Result |
|---|---:|
| Production events | 4 |
| Total units produced | 385 |
| Total defects | 7 |
| Good units | 378 |
| Defect rate | 1.82% |
| Total production cost | 85,000.00 |
| Cost per unit | 220.78 |
| Total production minutes | 425 |

## Factory Performance

| Factory | Units | Cost | Defects | Defect rate | Cost/unit |
|---|---:|---:|---:|---:|---:|
| F001 . Colombo Plant | 195 | 43,000.00 | 5 | 2.56% | 220.51 |
| F002 . Kandy Plant | 190 | 42,000.00 | 2 | 1.05% | 221.05 |

Interpretation: F001 has slightly higher output, while F002 has the lower defect rate in the demonstration dataset.

## Product Performance

| Product | Units | Cost | Defects | Defect rate |
|---|---:|---:|---:|---:|
| P001 . Industrial Pump | 210 | 52,000.00 | 3 | 1.43% |
| P002 . Control Valve | 175 | 33,000.00 | 4 | 2.29% |

P001 contributes the greater production volume and has the lower defect rate in this small controlled dataset.

## Machine Efficiency

| Machine | Units | Minutes | Units/minute |
|---|---:|---:|---:|
| M001 | 210 | 235 | 0.89 |
| M002 | 80 | 90 | 0.89 |
| M003 | 95 | 100 | 0.95 |

M003 has the highest units-per-minute value in the demonstration data. Because the dataset is intentionally small for an academic SCD demonstration, these results illustrate analytical capability rather than statistically generalisable operational performance.

## SCD Historical Result

M001 demonstrates historically correct machine assignment:

| Production | Date | Historical machine assignment | Production factory |
|---|---|---|---|
| PR001 | 2026-08-01 | M001 / F001 | F001 |
| PR003 | 2026-08-15 | M001 / F002 | F002 |

PR001 remains linked to the original M001 surrogate-key version after Run 2. PR003 uses the new surrogate-key version created when M001 moved to F002. This is the key historical-value demonstration required by the project.
