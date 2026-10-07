-- Fact table
-- Grain: one row per completed production event.
-- Production_ID is retained as a degenerate dimension and idempotency key.

CREATE TABLE Fact_Production (
    Production_Key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Production_ID VARCHAR(20) NOT NULL UNIQUE,
    Date_Key INT NOT NULL,
    Product_Key BIGINT NOT NULL,
    Machine_Key BIGINT NOT NULL,
    Factory_Key BIGINT NOT NULL,
    Employee_Key BIGINT NOT NULL,
    Shift_Key BIGINT NOT NULL,
    Quantity_Produced INT NOT NULL CHECK (Quantity_Produced >= 0),
    Production_Cost DECIMAL(12,2) NOT NULL CHECK (Production_Cost >= 0),
    Production_Time INT NOT NULL CHECK (Production_Time >= 0),
    Defect_Count INT NOT NULL CHECK (
        Defect_Count >= 0 AND Defect_Count <= Quantity_Produced
    )
);
