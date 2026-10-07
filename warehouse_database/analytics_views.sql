-- Semantic view consumed by Streamlit, SQL analysis and BI tools.

CREATE OR REPLACE VIEW vw_production_dashboard AS
SELECT
    f.production_key,
    f.production_id,
    d.full_date AS production_date,
    p.product_id,
    p.product_name,
    p.category,
    m.machine_id,
    m.machine_name,
    m.machine_type,
    m.machine_status,
    m.factory_id AS machine_factory_id,
    fac.factory_id,
    fac.factory_name,
    fac.location AS factory_location,
    e.employee_id,
    e.employee_name,
    e.department,
    e.role,
    s.shift_id,
    s.shift_name,
    f.quantity_produced,
    f.defect_count,
    (f.quantity_produced - f.defect_count) AS good_quantity,
    ROUND(
        f.defect_count::numeric / NULLIF(f.quantity_produced, 0) * 100,
        2
    ) AS defect_rate,
    f.production_time,
    f.production_cost,
    ROUND(
        f.production_cost::numeric / NULLIF(f.quantity_produced, 0),
        2
    ) AS cost_per_unit
FROM fact_production f
JOIN dim_date d ON d.date_key = f.date_key
JOIN dim_product p ON p.product_key = f.product_key
JOIN dim_machine m ON m.machine_key = f.machine_key
JOIN dim_factory fac ON fac.factory_key = f.factory_key
JOIN dim_employee e ON e.employee_key = f.employee_key
JOIN dim_shift s ON s.shift_key = f.shift_key;
