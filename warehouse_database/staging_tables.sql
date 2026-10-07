-- Predefined staging layer. ETL truncates and appends each source snapshot.

CREATE TABLE stg_product (
    product_id VARCHAR(20),
    product_name VARCHAR(100),
    category VARCHAR(50),
    unit_cost DECIMAL(10,2)
);

CREATE TABLE stg_factory (
    factory_id VARCHAR(20),
    factory_name VARCHAR(100),
    location VARCHAR(100),
    capacity INT
);

CREATE TABLE stg_machine (
    machine_id VARCHAR(20),
    machine_name VARCHAR(100),
    machine_type VARCHAR(50),
    factory_id VARCHAR(20),
    status VARCHAR(30)
);

CREATE TABLE stg_employee (
    employee_id VARCHAR(20),
    employee_name VARCHAR(100),
    department VARCHAR(50),
    role VARCHAR(50)
);

CREATE TABLE stg_shift (
    shift_id VARCHAR(20),
    shift_name VARCHAR(50),
    start_time TIME,
    end_time TIME
);

CREATE TABLE stg_production (
    production_id VARCHAR(20),
    product_id VARCHAR(20),
    machine_id VARCHAR(20),
    factory_id VARCHAR(20),
    employee_id VARCHAR(20),
    shift_id VARCHAR(20),
    production_date DATE,
    quantity INT,
    production_time INT,
    production_cost DECIMAL(12,2),
    defect_count INT
);
