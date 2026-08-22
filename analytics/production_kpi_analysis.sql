-- Production Operations Analytics
-- Analytical queries used to demonstrate the business value of Fact_Production
-- and its dimensions after the two ETL executions.

-- 1. Enterprise production KPIs and generated measures
SELECT
    COUNT(*) AS production_events,
    SUM(quantity_produced) AS total_units,
    SUM(defect_count) AS total_defects,
    SUM(quantity_produced - defect_count) AS good_units,
    ROUND(SUM(defect_count)::numeric / NULLIF(SUM(quantity_produced), 0) * 100, 2) AS defect_rate_pct,
    SUM(production_cost) AS total_cost,
    ROUND(SUM(production_cost)::numeric / NULLIF(SUM(quantity_produced), 0), 2) AS cost_per_unit,
    SUM(production_time) AS total_production_minutes
FROM fact_production;

-- 2. Factory performance
SELECT
    fac.factory_id,
    fac.factory_name,
    SUM(f.quantity_produced) AS units_produced,
    SUM(f.quantity_produced - f.defect_count) AS good_units,
    SUM(f.production_cost) AS production_cost,
    SUM(f.defect_count) AS defects,
    ROUND(SUM(f.defect_count)::numeric / NULLIF(SUM(f.quantity_produced), 0) * 100, 2) AS defect_rate_pct,
    ROUND(SUM(f.production_cost)::numeric / NULLIF(SUM(f.quantity_produced), 0), 2) AS cost_per_unit
FROM fact_production f
JOIN dim_factory fac ON f.factory_key = fac.factory_key
GROUP BY fac.factory_id, fac.factory_name
ORDER BY units_produced DESC;

-- 3. Product performance and quality
SELECT
    p.product_id,
    p.product_name,
    SUM(f.quantity_produced) AS quantity,
    SUM(f.quantity_produced - f.defect_count) AS good_quantity,
    SUM(f.production_cost) AS cost,
    SUM(f.defect_count) AS defects,
    ROUND(SUM(f.defect_count)::numeric / NULLIF(SUM(f.quantity_produced), 0) * 100, 2) AS defect_rate_pct
FROM fact_production f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_id, p.product_name
ORDER BY quantity DESC;

-- 4. Machine efficiency. Grouping by business key combines historical SCD versions
-- while still allowing version-level analysis through machine_key when required.
SELECT
    m.machine_id,
    m.machine_name,
    SUM(f.quantity_produced) AS output,
    SUM(f.production_time) AS production_minutes,
    SUM(f.defect_count) AS defects,
    ROUND(SUM(f.quantity_produced)::numeric / NULLIF(SUM(f.production_time), 0), 2) AS units_per_minute
FROM fact_production f
JOIN dim_machine m ON f.machine_key = m.machine_key
GROUP BY m.machine_id, m.machine_name
ORDER BY units_per_minute DESC;

-- 5. Monthly production and cost trend
SELECT
    d.year,
    d.month,
    SUM(f.quantity_produced) AS monthly_output,
    SUM(f.production_cost) AS monthly_cost,
    SUM(f.defect_count) AS monthly_defects
FROM fact_production f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 6. Shift performance
SELECT
    s.shift_id,
    s.shift_name,
    SUM(f.quantity_produced) AS output,
    SUM(f.production_cost) AS cost,
    SUM(f.defect_count) AS defects,
    ROUND(SUM(f.defect_count)::numeric / NULLIF(SUM(f.quantity_produced), 0) * 100, 2) AS defect_rate_pct
FROM fact_production f
JOIN dim_shift s ON f.shift_key = s.shift_key
GROUP BY s.shift_id, s.shift_name
ORDER BY output DESC;

-- 7. Historical machine-assignment comparison for the SCD Type 2 demonstration
SELECT
    d.full_date,
    m.machine_key,
    m.machine_id,
    m.factory_id AS assigned_factory_at_that_time,
    m.machine_status,
    fac.factory_id AS actual_production_factory,
    SUM(f.quantity_produced) AS output,
    SUM(f.production_cost) AS cost,
    SUM(f.defect_count) AS defects
FROM fact_production f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_machine m ON f.machine_key = m.machine_key
JOIN dim_factory fac ON f.factory_key = fac.factory_key
WHERE m.machine_id = 'M001'
GROUP BY d.full_date, m.machine_key, m.machine_id, m.factory_id, m.machine_status, fac.factory_id
ORDER BY d.full_date;
