-- Milestone 6: Production Operations Analytics
-- Business KPI queries for Power BI semantic model

-- 1. Overall production performance
SELECT
    SUM(quantity_produced) AS total_units,
    SUM(defect_count) AS total_defects,
    ROUND(SUM(defect_count)::numeric / NULLIF(SUM(quantity_produced),0) * 100, 2) AS defect_rate_pct,
    SUM(production_cost) AS total_cost,
    ROUND(SUM(production_cost) / NULLIF(SUM(quantity_produced),0), 2) AS cost_per_unit
FROM fact_production;

-- 2. Factory performance
SELECT
    f.factory_name,
    SUM(p.quantity_produced) AS units_produced,
    SUM(p.production_cost) AS production_cost,
    SUM(p.defect_count) AS defects,
    ROUND(SUM(p.defect_count)::numeric / NULLIF(SUM(p.quantity_produced),0) * 100,2) AS defect_rate_pct
FROM fact_production p
JOIN dim_factory f ON p.factory_key=f.factory_key
GROUP BY f.factory_name
ORDER BY units_produced DESC;

-- 3. Product performance
SELECT
    p.product_name,
    SUM(f.quantity_produced) AS quantity,
    SUM(f.production_cost) AS cost
FROM fact_production f
JOIN dim_product p ON f.product_key=p.product_key
GROUP BY p.product_name
ORDER BY quantity DESC;

-- 4. Machine efficiency
SELECT
    m.machine_id,
    m.machine_name,
    SUM(f.quantity_produced) AS output,
    SUM(f.production_time) AS production_minutes,
    ROUND(SUM(f.quantity_produced)::numeric / NULLIF(SUM(f.production_time),0),2) AS units_per_minute
FROM fact_production f
JOIN dim_machine m ON f.machine_key=m.machine_key
GROUP BY m.machine_id,m.machine_name
ORDER BY units_per_minute DESC;

-- 5. Time trend
SELECT
    d.year,
    d.month,
    SUM(f.quantity_produced) AS monthly_output,
    SUM(f.production_cost) AS monthly_cost
FROM fact_production f
JOIN dim_date d ON f.date_key=d.date_key
GROUP BY d.year,d.month
ORDER BY d.year,d.month;
