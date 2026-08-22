-- Sample Manufacturing OLTP Data
-- Represents the initial operational state used by the Run 1 ETL demonstration.

INSERT INTO Product (Product_ID, Product_Name, Category, Unit_Cost) VALUES
('P001','Industrial Pump','Equipment',2500.00),
('P002','Control Valve','Equipment',800.00);

INSERT INTO Factory (Factory_ID, Factory_Name, Location, Capacity) VALUES
('F001','Colombo Plant','Colombo',5000),
('F002','Kandy Plant','Kandy',3000);

INSERT INTO Machine (Machine_ID, Machine_Name, Machine_Type, Factory_ID, Status) VALUES
('M001','Assembly Machine A','Assembly','F001','Active'),
('M002','Cutting Machine B','Cutting','F002','Active');

INSERT INTO Employee (Employee_ID, Employee_Name, Department, Role) VALUES
('E001','John Silva','Production','Operator'),
('E002','Nimal Perera','Production','Operator');

INSERT INTO Shift (Shift_ID, Shift_Name, Start_Time, End_Time) VALUES
('S001','Morning','08:00:00','16:00:00'),
('S002','Evening','16:00:00','00:00:00');

INSERT INTO Production_Order (
    Production_ID, Product_ID, Machine_ID, Factory_ID, Employee_ID, Shift_ID,
    Production_Date, Quantity, Production_Time, Production_Cost, Defect_Count
) VALUES
('PR001','P001','M001','F001','E001','S001','2026-08-01',100,120,25000,2),
('PR002','P002','M002','F002','E002','S002','2026-08-01',80,90,15000,1);
