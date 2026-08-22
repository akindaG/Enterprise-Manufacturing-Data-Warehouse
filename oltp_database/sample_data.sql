-- Sample Manufacturing OLTP Data

INSERT INTO Product VALUES
('P001','Industrial Pump','Equipment',2500.00),
('P002','Control Valve','Equipment',800.00);

INSERT INTO Factory VALUES
('F001','Colombo Plant','Colombo',5000),
('F002','Kandy Plant','Kandy',3000);

INSERT INTO Machine VALUES
('M001','Assembly Machine A','Assembly','F001','Active'),
('M002','Cutting Machine B','Cutting','F002','Active');

INSERT INTO Employee VALUES
('E001','John Silva','Production','Operator');

INSERT INTO Shift VALUES
('S001','Morning','08:00','16:00');

INSERT INTO Production_Order VALUES
('PR001','P001','M001','F001','E001','S001','2026-08-01',100,120,25000,2);