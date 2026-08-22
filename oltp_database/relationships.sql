-- OLTP Foreign Key Relationships

ALTER TABLE Machine
ADD FOREIGN KEY (Factory_ID) REFERENCES Factory(Factory_ID);

ALTER TABLE Production_Order
ADD FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID),
ADD FOREIGN KEY (Machine_ID) REFERENCES Machine(Machine_ID),
ADD FOREIGN KEY (Factory_ID) REFERENCES Factory(Factory_ID),
ADD FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID),
ADD FOREIGN KEY (Shift_ID) REFERENCES Shift(Shift_ID);