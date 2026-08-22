# OLTP Database Design

## Database
manufacturing_oltp

## Purpose
The OLTP database represents the operational environment where daily manufacturing transactions are recorded.

## Tables

### Product
Primary Key: Product_ID

Attributes:
- Product_Name
- Category
- Unit_Cost

### Machine
Primary Key: Machine_ID

Attributes:
- Machine_Name
- Machine_Type
- Factory_ID
- Status

### Factory
Primary Key: Factory_ID

Attributes:
- Factory_Name
- Location
- Capacity

### Employee
Primary Key: Employee_ID

Attributes:
- Employee_Name
- Department
- Role

### Shift
Primary Key: Shift_ID

Attributes:
- Shift_Name
- Start_Time
- End_Time

### Production_Order
Primary Key: Production_ID

Foreign Keys:
- Product_ID
- Machine_ID
- Factory_ID
- Employee_ID
- Shift_ID

Measures:
- Quantity
- Production_Time
- Production_Cost
- Defect_Count

## Relationship Overview
Product, Machine, Factory, Employee and Shift provide descriptive information for Production_Order transactions.
