-- Data Warehouse Fact Table

CREATE TABLE Fact_Production (
    Production_Key INT PRIMARY KEY,
    Date_Key INT,
    Product_Key INT,
    Machine_Key INT,
    Factory_Key INT,
    Employee_Key INT,
    Shift_Key INT,
    Quantity_Produced INT,
    Production_Cost DECIMAL(12,2),
    Production_Time INT,
    Defect_Count INT
);