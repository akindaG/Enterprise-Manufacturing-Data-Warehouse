-- Warehouse-level data quality and integrity checks

-- Duplicate source transaction identifiers. Expected: zero rows.
SELECT production_id, COUNT(*) AS duplicate_count
FROM fact_production
GROUP BY production_id
HAVING COUNT(*) > 1;

-- Invalid fact measures. Expected: zero rows.
SELECT *
FROM fact_production
WHERE quantity_produced < 0
   OR defect_count < 0
   OR defect_count > quantity_produced
   OR production_cost < 0
   OR production_time < 0;

-- Orphaned surrogate keys. Expected: all counts = 0.
SELECT
    COUNT(*) FILTER (WHERE d.date_key IS NULL) AS orphan_date,
    COUNT(*) FILTER (WHERE p.product_key IS NULL) AS orphan_product,
    COUNT(*) FILTER (WHERE m.machine_key IS NULL) AS orphan_machine,
    COUNT(*) FILTER (WHERE fac.factory_key IS NULL) AS orphan_factory,
    COUNT(*) FILTER (WHERE e.employee_key IS NULL) AS orphan_employee,
    COUNT(*) FILTER (WHERE s.shift_key IS NULL) AS orphan_shift
FROM fact_production f
LEFT JOIN dim_date d ON d.date_key=f.date_key
LEFT JOIN dim_product p ON p.product_key=f.product_key
LEFT JOIN dim_machine m ON m.machine_key=f.machine_key
LEFT JOIN dim_factory fac ON fac.factory_key=f.factory_key
LEFT JOIN dim_employee e ON e.employee_key=f.employee_key
LEFT JOIN dim_shift s ON s.shift_key=f.shift_key;

-- Facts must resolve to the machine version valid on the event date. Expected: zero rows.
SELECT f.production_id, d.full_date, m.machine_id, m.effective_date, m.expiry_date
FROM fact_production f
JOIN dim_date d ON d.date_key=f.date_key
JOIN dim_machine m ON m.machine_key=f.machine_key
WHERE d.full_date NOT BETWEEN m.effective_date AND m.expiry_date;
