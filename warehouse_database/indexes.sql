-- Analytical and surrogate-key lookup indexes

CREATE INDEX ix_fact_production_date_key ON fact_production(date_key);
CREATE INDEX ix_fact_production_product_key ON fact_production(product_key);
CREATE INDEX ix_fact_production_machine_key ON fact_production(machine_key);
CREATE INDEX ix_fact_production_factory_key ON fact_production(factory_key);
CREATE INDEX ix_fact_production_employee_key ON fact_production(employee_key);
CREATE INDEX ix_fact_production_shift_key ON fact_production(shift_key);

CREATE INDEX ix_dim_machine_history
ON dim_machine(machine_id, effective_date, expiry_date);
