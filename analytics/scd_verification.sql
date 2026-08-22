-- Milestone 5: SCD Type 2 and ETL execution verification

-- 1. Verify both ETL executions were logged.
SELECT run_id, executed_at, run_date, source_dir, status,
       facts_inserted, machine_versions_created
FROM etl_run_log
ORDER BY run_id;

-- 2. Verify M001 has two historical versions after Run 2.
SELECT machine_key, machine_id, machine_name, machine_type,
       factory_id, effective_date, expiry_date, is_current
FROM dim_machine
WHERE machine_id = 'M001'
ORDER BY effective_date, machine_key;

-- Expected after Run 2:
-- old version: M001 -> F001, is_current = false
-- new version: M001 -> F002, is_current = true

-- 3. Verify M002 stayed unchanged with one current version.
SELECT machine_key, machine_id, factory_id,
       effective_date, expiry_date, is_current
FROM dim_machine
WHERE machine_id = 'M002'
ORDER BY machine_key;

-- 4. Verify M003 was inserted as a new entity during Run 2.
SELECT machine_key, machine_id, factory_id,
       effective_date, expiry_date, is_current
FROM dim_machine
WHERE machine_id = 'M003';

-- 5. Verify fact rows reference the correct historical machine version.
SELECT
    f.production_key,
    d.full_date AS production_date,
    m.machine_key,
    m.machine_id,
    m.factory_id AS machine_factory_at_that_time,
    fac.factory_id AS production_factory,
    p.product_name,
    f.quantity_produced,
    f.production_cost,
    f.production_time,
    f.defect_count
FROM fact_production f
JOIN dim_date d ON d.date_key = f.date_key
JOIN dim_machine m ON m.machine_key = f.machine_key
JOIN dim_factory fac ON fac.factory_key = f.factory_key
JOIN dim_product p ON p.product_key = f.product_key
ORDER BY d.full_date, f.production_key;

-- 6. Historical comparison for M001 before and after the factory transfer.
SELECT
    d.full_date,
    m.machine_id,
    m.factory_id,
    SUM(f.quantity_produced) AS total_quantity,
    SUM(f.production_cost) AS total_cost,
    SUM(f.defect_count) AS total_defects
FROM fact_production f
JOIN dim_date d ON d.date_key = f.date_key
JOIN dim_machine m ON m.machine_key = f.machine_key
WHERE m.machine_id = 'M001'
GROUP BY d.full_date, m.machine_id, m.factory_id
ORDER BY d.full_date;
