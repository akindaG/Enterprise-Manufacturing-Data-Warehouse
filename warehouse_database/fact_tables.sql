-- Data Warehouse Fact Table
-- Grain: one row per completed production event.
-- Production_ID is retained as a degenerate dimension / source transaction identifier
-- to provide traceability and idempotent incremental loading.

CREATE TABLE Fact_Production (
    Production_Key INT PRIMARY KEY,
    Production_ID VARCHAR(20) NOT NULL UNIQUE,
    Date_Key INT NOT NULL,
    Product_Key INT NOT NULL,
    Machine_Key INT NOT NULL,
    Factory_Key INT NOT NULL,
    Employee_Key INT NOT NULL,
    Shift_Key INT NOT NULL,
    Quantity_Produced INT NOT NULL CHECK (Quantity_Produced >= 0),
    Production_Cost DECIMAL(12,2) NOT NULL CHECK (Production_Cost >= 0),
    Production_Time INT NOT NULL CHECK (Production_Time >= 0),
    Defect_Count INT NOT NULL CHECK (
        Defect_Count >= 0 AND Defect_Count <= Quantity_Produced
    )
);
