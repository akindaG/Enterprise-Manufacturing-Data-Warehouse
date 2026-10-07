-- Dimension tables for the Enterprise Manufacturing Data Platform

CREATE TABLE Dim_Date (
    Date_Key INT PRIMARY KEY,
    Full_Date DATE NOT NULL UNIQUE,
    Day INT NOT NULL CHECK (Day BETWEEN 1 AND 31),
    Month INT NOT NULL CHECK (Month BETWEEN 1 AND 12),
    Quarter INT NOT NULL CHECK (Quarter BETWEEN 1 AND 4),
    Year INT NOT NULL
);

CREATE TABLE Dim_Product (
    Product_Key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Product_ID VARCHAR(20) NOT NULL UNIQUE,
    Product_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Unit_Cost DECIMAL(10,2) NOT NULL CHECK (Unit_Cost >= 0)
);

CREATE TABLE Dim_Machine (
    Machine_Key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Machine_ID VARCHAR(20) NOT NULL,
    Machine_Name VARCHAR(100) NOT NULL,
    Machine_Type VARCHAR(50) NOT NULL,
    Factory_ID VARCHAR(20) NOT NULL,
    Machine_Status VARCHAR(30) NOT NULL,
    Effective_Date DATE NOT NULL,
    Expiry_Date DATE NOT NULL,
    Is_Current BOOLEAN NOT NULL,
    CONSTRAINT ck_dim_machine_dates CHECK (Expiry_Date >= Effective_Date),
    CONSTRAINT uq_dim_machine_version UNIQUE (Machine_ID, Effective_Date)
);

CREATE UNIQUE INDEX ux_dim_machine_current
ON Dim_Machine (Machine_ID)
WHERE Is_Current = TRUE;

CREATE TABLE Dim_Factory (
    Factory_Key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Factory_ID VARCHAR(20) NOT NULL UNIQUE,
    Factory_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    Capacity INT NOT NULL CHECK (Capacity >= 0)
);

CREATE TABLE Dim_Employee (
    Employee_Key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Employee_ID VARCHAR(20) NOT NULL UNIQUE,
    Employee_Name VARCHAR(100) NOT NULL,
    Department VARCHAR(50) NOT NULL,
    Role VARCHAR(50) NOT NULL
);

CREATE TABLE Dim_Shift (
    Shift_Key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Shift_ID VARCHAR(20) NOT NULL UNIQUE,
    Shift_Name VARCHAR(50) NOT NULL,
    Start_Time TIME NOT NULL,
    End_Time TIME NOT NULL
);
