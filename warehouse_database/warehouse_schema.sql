-- Star Schema Relationships

ALTER TABLE Fact_Production
ADD FOREIGN KEY (Date_Key) REFERENCES Dim_Date(Date_Key),
ADD FOREIGN KEY (Product_Key) REFERENCES Dim_Product(Product_Key),
ADD FOREIGN KEY (Machine_Key) REFERENCES Dim_Machine(Machine_Key),
ADD FOREIGN KEY (Factory_Key) REFERENCES Dim_Factory(Factory_Key),
ADD FOREIGN KEY (Employee_Key) REFERENCES Dim_Employee(Employee_Key),
ADD FOREIGN KEY (Shift_Key) REFERENCES Dim_Shift(Shift_Key);