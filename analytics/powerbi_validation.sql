-- Power BI validation queries
-- Run after both ETL executions and compare the results with dashboard totals.

-- 1. Overall control totals
SELECT
    COUNT(*) AS production_events,
    SUM(quantity_produced) AS total_units,
    SUM(defect_count) AS total_defects,
    SUM(quantity_produced - defect_count) AS good_units,
    SUM(production_cost) AS total_cost,
    ROUND(
        SUM(defect_count)::numeric / NULLIF(SUM(quantity_produced), 0) * 100,
        2
    ) AS defect_rate_pct,
    ROUND(
        SUM(production_cost)::numeric / NULLIF(SUM(quantity_produced), 0),
        2
    ) AS cost_per_unit,
    ROUND(
        SUM(quantity_produced)::numeric / NULLIF(SUM(production_time), 0),
        2
    ) AS units_per_production_minute
FROM fact_production;

-- Expected after Run 1 + Run 2:
-- production_events = 4
-- total_units = 385
-- total_defects = 7
-- good_units = 378
-- total_cost = 85000.00
-- defect_rate_pct = 1.82
-- cost_per_unit = 220.78

-- 2. Factory validation
SELECT
    fac.factory_id,
    fac.factory_name,
    SUM(f.quantity_produced) AS total_units,
    SUM(f.defect_count) AS total_defects,
    SUM(f.quantity_produced - f.defect_count) AS good_units,
    SUM(f.production_cost) AS total_cost,
    ROUND(
        SUM(f.defect_count)::numeric / NULLIF(SUM(f.quantity_produced), 0) * 100,
        2
    ) AS defect_rate_pct,
    ROUND(
        SUM(f.production_cost)::numeric / NULLIF(SUM(f.quantity_produced), 0),
        2
    ) AS cost_per_unit
FROM fact_production f
JOIN dim_factory fac ON fac.factory_key = f.factory_key
GROUP BY fac.factory_id, fac.factory_name
ORDER BY fac.factory_id;

-- 3. Product validation
SELECT
    p.product_id,
    p.product_name,
    SUM(f.quantity_produced) AS total_units,
    SUM(f.defect_count) AS total_defects,
    SUM(f.production_cost) AS total_cost,
    ROUND(
        SUM(f.defect_count)::numeric / NULLIF(SUM(f.quantity_produced), 0) * 100,
        2
    ) AS defect_rate_pct
FROM fact_production f
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY p.product_id, p.product_name
ORDER BY p.product_id;

-- 4. Shift validation
SELECT
    s.shift_id,
    s.shift_name,
    SUM(f.quantity_produced) AS total_units,
    SUM(f.defect_count) AS total_defects,
    ROUND(
        SUM(f.defect_count)::numeric / NULLIF(SUM(f.quantity_produced), 0) * 100,
        2
    ) AS defect_rate_pct
FROM fact_production f
JOIN dim_shift s ON s.shift_key = f.shift_key
GROUP BY s.shift_id, s.shift_name
ORDER BY s.shift_id;

-- 5. Machine efficiency validation
SELECT
    m.machine_id,
    m.machine_name,
    SUM(f.quantity_produced) AS total_units,
    SUM(f.production_time) AS total_production_minutes,
    SUM(f.defect_count) AS total_defects,
    ROUND(
        SUM(f.quantity_produced)::numeric / NULLIF(SUM(f.production_time), 0),
        2
    ) AS units_per_production_minute
FROM fact_production f
JOIN dim_machine m ON m.machine_key = f.machine_key
GROUP BY m.machine_id, m.machine_name
ORDER BY m.machine_id;

-- 6. SCD Type 2 validation for dashboard history page
SELECT
    machine_key,
    machine_id,
    machine_name,
    machine_type,
    factory_id,
    machine_status,
    effective_date,
    expiry_date,
    is_current
FROM dim_machine
WHERE machine_id = 'M001'
ORDER BY effective_date, machine_key;

-- Expected: two M001 rows.
-- Historical version: F001, is_current = false.
-- Current version: F002, is_current = true.

-- 7. Historical fact-to-SCD-version validation
SELECT
    f.production_id,
    d.full_date AS production_date,
    m.machine_key,
    m.machine_id,
    m.factory_id AS historical_machine_factory,
    fac.factory_id AS production_factory,
    f.quantity_produced,
    f.production_cost,
    f.defect_count
FROM fact_production f
JOIN dim_date d ON d.date_key = f.date_key
JOIN dim_machine m ON m.machine_key = f.machine_key
JOIN dim_factory fac ON fac.factory_key = f.factory_key
WHERE m.machine_id = 'M001'
ORDER BY d.full_date, f.production_id;
