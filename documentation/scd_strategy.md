# Slowly Changing Dimension Strategy

## Selected Dimension
Dim_Machine

## SCD Type
Slowly Changing Dimension Type 2

## Reason
Machine information can change over time, such as factory assignment or operational status. Historical versions must be preserved for accurate production analysis.

## Attributes
- Machine_Key
- Machine_ID
- Machine_Name
- Machine_Type
- Factory_ID
- Effective_Date
- Expiry_Date
- Current_Flag

## Example
Before change:

Machine M001
Factory Colombo
Current_Flag = TRUE

After transfer:

Old record:
Factory Colombo
Current_Flag = FALSE

New record:
Factory Kandy
Current_Flag = TRUE

This preserves historical machine information while allowing current reporting.
