# Milestone 6: Power BI Dashboard Design

## Objective

Transform warehouse data into decision-support analytics for manufacturing managers.

## Dashboard Pages

## 1. Executive Production Overview

KPIs:

- Total Units Produced
- Total Production Cost
- Defect Rate
- Cost Per Unit
- Production Events

Visuals:

- KPI cards
- Monthly production trend
- Factory comparison chart

## 2. Factory Performance

Purpose:

Identify high-performing and under-performing manufacturing locations.

Visuals:

- Output by factory
- Defects by factory
- Cost distribution

## 3. Machine Efficiency

Purpose:

Analyse equipment productivity.

Visuals:

- Units per production minute
- Machine output ranking
- Current SCD machine assignment analysis

## 4. Product Analysis

Purpose:

Understand product contribution.

Visuals:

- Product output ranking
- Product cost analysis
- Defect comparison

## Data Model

Power BI connects to the dimensional warehouse:

Fact_Production

Relationships:

- Fact_Production -> Dim_Date
- Fact_Production -> Dim_Product
- Fact_Production -> Dim_Machine
- Fact_Production -> Dim_Factory
- Fact_Production -> Dim_Employee
- Fact_Production -> Dim_Shift

## Business Questions Answered

1. Which factory produces the highest volume?
2. Which machines have the best efficiency?
3. Which products generate the highest production output?
4. Where are defect rates increasing?
5. How does production cost change over time?

## Recommended Power BI Measures

```DAX
Total Units = SUM(Fact_Production[Quantity_Produced])

Total Cost = SUM(Fact_Production[Production_Cost])

Defect Rate = DIVIDE(SUM(Fact_Production[Defect_Count]), SUM(Fact_Production[Quantity_Produced]))

Cost Per Unit = DIVIDE([Total Cost],[Total Units])
```
