-- Manufacturing OLTP Database Schema

CREATE DATABASE manufacturing_oltp;

-- Product master table
CREATE TABLE Product (
    Product_ID VARCHAR(20) PRIMARY KEY,
    Product_Name VARCHAR(100),
    Category VARCHAR(50),
    Unit_Cost DECIMAL(10,2)
);

CREATE TABLE Factory (
    Factory_ID VARCHAR(20) PRIMARY KEY,
    Factory_Name VARCHAR(100),
    Location VARCHAR(100),
    Capacity INT
);

CREATE TABLE Machine (
    Machine_ID VARCHAR(20) PRIMARY KEY,
    Machine_Name VARCHAR(100),
    Machine_Type VARCHAR(50),
    Factory_ID VARCHAR(20),
    Status VARCHAR(30)
);

CREATE TABLE Employee (
    Employee_ID VARCHAR(20) PRIMARY KEY,
    Employee_Name VARCHAR(100),
    Department VARCHAR(50),
    Role VARCHAR(50)
);

CREATE TABLE Shift (
    Shift_ID VARCHAR(20) PRIMARY KEY,
    Shift_Name VARCHAR(50),
    Start_Time TIME,
    End_Time TIME
);

CREATE TABLE Production_Order (
    Production_ID VARCHAR(20) PRIMARY KEY,
    Product_ID VARCHAR(20),
    Machine_ID VARCHAR(20),
    Factory_ID VARCHAR(20),
    Employee_ID VARCHAR(20),
    Shift_ID VARCHAR(20),
    Production_Date DATE,
    Quantity INT,
    Production_Time INT,
    Production_Cost DECIMAL(12,2),
    Defect_Count INT
);