-- Manufacturing OLTP Database Schema
-- Run this script while connected to the manufacturing_oltp database.
-- Database creation is intentionally kept outside this file so the script is portable
-- across pgAdmin, psql, CI environments and managed PostgreSQL services.

CREATE TABLE Product (
    Product_ID VARCHAR(20) PRIMARY KEY,
    Product_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Unit_Cost DECIMAL(10,2) NOT NULL CHECK (Unit_Cost >= 0)
);

CREATE TABLE Factory (
    Factory_ID VARCHAR(20) PRIMARY KEY,
    Factory_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    Capacity INT NOT NULL CHECK (Capacity >= 0)
);

CREATE TABLE Machine (
    Machine_ID VARCHAR(20) PRIMARY KEY,
    Machine_Name VARCHAR(100) NOT NULL,
    Machine_Type VARCHAR(50) NOT NULL,
    Factory_ID VARCHAR(20) NOT NULL,
    Status VARCHAR(30) NOT NULL
);

CREATE TABLE Employee (
    Employee_ID VARCHAR(20) PRIMARY KEY,
    Employee_Name VARCHAR(100) NOT NULL,
    Department VARCHAR(50) NOT NULL,
    Role VARCHAR(50) NOT NULL
);

CREATE TABLE Shift (
    Shift_ID VARCHAR(20) PRIMARY KEY,
    Shift_Name VARCHAR(50) NOT NULL,
    Start_Time TIME NOT NULL,
    End_Time TIME NOT NULL
);

-- In this synthetic operational model, Production_Order records a completed
-- production execution event. Production_ID is therefore the transaction identifier
-- used for source-to-warehouse traceability.
CREATE TABLE Production_Order (
    Production_ID VARCHAR(20) PRIMARY KEY,
    Product_ID VARCHAR(20) NOT NULL,
    Machine_ID VARCHAR(20) NOT NULL,
    Factory_ID VARCHAR(20) NOT NULL,
    Employee_ID VARCHAR(20) NOT NULL,
    Shift_ID VARCHAR(20) NOT NULL,
    Production_Date DATE NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity >= 0),
    Production_Time INT NOT NULL CHECK (Production_Time >= 0),
    Production_Cost DECIMAL(12,2) NOT NULL CHECK (Production_Cost >= 0),
    Defect_Count INT NOT NULL CHECK (Defect_Count >= 0 AND Defect_Count <= Quantity)
);
