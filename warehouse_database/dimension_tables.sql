-- Data Warehouse Dimension Tables

CREATE TABLE Dim_Date (
    Date_Key INT PRIMARY KEY,
    Full_Date DATE,
    Day INT,
    Month INT,
    Quarter INT,
    Year INT
);

CREATE TABLE Dim_Product (
    Product_Key INT PRIMARY KEY,
    Product_ID VARCHAR(20),
    Product_Name VARCHAR(100),
    Category VARCHAR(50),
    Unit_Cost DECIMAL(10,2)
);

CREATE TABLE Dim_Machine (
    Machine_Key INT PRIMARY KEY,
    Machine_ID VARCHAR(20),
    Machine_Name VARCHAR(100),
    Machine_Type VARCHAR(50),
    Factory_ID VARCHAR(20),
    Effective_Date DATE,
    Expiry_Date DATE,
    Is_Current BOOLEAN
);

CREATE TABLE Dim_Factory (
    Factory_Key INT PRIMARY KEY,
    Factory_ID VARCHAR(20),
    Factory_Name VARCHAR(100),
    Location VARCHAR(100),
    Capacity INT
);

CREATE TABLE Dim_Employee (
    Employee_Key INT PRIMARY KEY,
    Employee_ID VARCHAR(20),
    Employee_Name VARCHAR(100),
    Department VARCHAR(50),
    Role VARCHAR(50)
);

CREATE TABLE Dim_Shift (
    Shift_Key INT PRIMARY KEY,
    Shift_ID VARCHAR(20),
    Shift_Name VARCHAR(50),
    Start_Time TIME,
    End_Time TIME
);