# Source System Analysis

## Overview
The manufacturing organization uses operational systems that capture daily transactional data. These systems act as the source layer for the Data Warehouse ETL process.

## Source Systems

### Product System
Stores product information.

Attributes:
- Product_ID
- Product_Name
- Category
- Unit_Cost

### Machine System
Stores manufacturing machine information.

Attributes:
- Machine_ID
- Machine_Name
- Machine_Type
- Factory_ID
- Status

### Factory System
Stores factory details.

Attributes:
- Factory_ID
- Factory_Name
- Location
- Capacity

### Employee System
Stores employees involved in production activities.

Attributes:
- Employee_ID
- Employee_Name
- Department
- Role

### Shift System
Stores production shift information.

Attributes:
- Shift_ID
- Shift_Name
- Start_Time
- End_Time

### Production System
Main transactional source containing production events.

Attributes:
- Production_ID
- Product_ID
- Machine_ID
- Factory_ID
- Employee_ID
- Shift_ID
- Production_Date
- Quantity
- Production_Time
- Production_Cost
- Defect_Count
