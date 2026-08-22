# Data Warehouse Design

## Approach
Kimball dimensional modelling approach using a star schema.

## Fact Table
Fact_Production

Columns:
- Production_Fact_Key
- Date_Key
- Product_Key
- Machine_Key
- Factory_Key
- Employee_Key
- Shift_Key
- Quantity_Produced
- Production_Cost
- Production_Time
- Defect_Count

## Dimension Tables

### Dim_Date
- Date_Key
- Full_Date
- Day
- Month
- Quarter
- Year

### Dim_Product
- Product_Key
- Product_ID
- Product_Name
- Category
- Unit_Cost

### Dim_Machine
- Machine_Key
- Machine_ID
- Machine_Name
- Machine_Type
- Factory_ID
- Effective_Date
- Expiry_Date
- Current_Flag

### Dim_Factory
- Factory_Key
- Factory_ID
- Factory_Name
- Location
- Capacity

### Dim_Employee
- Employee_Key
- Employee_ID
- Employee_Name
- Department
- Role

### Dim_Shift
- Shift_Key
- Shift_ID
- Shift_Name
- Start_Time
- End_Time

## Star Schema
Fact_Production is the central fact table connected to all dimension tables.
