# Slowly Changing Dimension Strategy

## 1. Why SCD Handling Is Required

Operational master data can change after production events have occurred. If the warehouse simply overwrites all descriptive values, historical reports may show production using attributes that were not true at the time of the event. The project therefore assigns an explicit change strategy to every dimension.

## 2. Dimension Change Strategy

| Dimension | Strategy | Rationale |
|---|---|---|
| `Dim_Date` | Type 0 / fixed | calendar dates do not require historical versioning |
| `Dim_Product` | Type 1 | current master corrections are sufficient for this project; event production cost is preserved in the fact table |
| `Dim_Factory` | Type 1 | current factory descriptive/capacity values are sufficient for the selected analytical scope |
| `Dim_Employee` | Type 1 | historical organisational-role tracking is outside the selected production scope |
| `Dim_Shift` | Type 1 | shift master corrections overwrite the current definition |
| `Dim_Machine` | **Type 2** | machine assignment/status/type changes can materially change historical production interpretation |

## 3. Dim_Machine SCD Type 2 Design

`Dim_Machine` uses:

- `Machine_Key` . surrogate key
- `Machine_ID` . natural/business key
- `Machine_Name`
- `Machine_Type`
- `Factory_ID`
- `Machine_Status`
- `Effective_Date`
- `Expiry_Date`
- `Is_Current`

Tracked source attributes are machine name, type, assigned factory and status.

## 4. Change Detection Logic

For each source machine the ETL determines whether it is:

1. **new** . no current row exists, so a new surrogate-keyed row is inserted
2. **unchanged** . tracked attributes equal the current row, so no new version is created
3. **changed** . the current row is expired and a new version receives a new `Machine_Key`

The warehouse permits only one `Is_Current = TRUE` row per `Machine_ID`.

## 5. Demonstration

### Run 1 . 2026-08-01

M001 is assigned to F001 (Colombo Plant):

```text
Machine_ID       M001
Factory_ID       F001
Effective_Date   2026-08-01
Expiry_Date      9999-12-31
Is_Current       TRUE
```

### Run 2 . 2026-08-15

M001 moves to F002 (Kandy Plant). The previous version is preserved:

```text
Old version
Factory_ID       F001
Effective_Date   2026-08-01
Expiry_Date      2026-08-14
Is_Current       FALSE

New version
Factory_ID       F002
Effective_Date   2026-08-15
Expiry_Date      9999-12-31
Is_Current       TRUE
```

The two versions have different surrogate keys.

## 6. Historical Fact Lookup

`Fact_Production` never joins a machine using only `Machine_ID`. During fact loading, the ETL finds the `Machine_Key` whose effective/expiry interval contains the production date. Therefore PR001 remains linked to the F001 version of M001, while PR003 links to the later F002 version.

This demonstrates the assignment requirements for historical data, surrogate-key changes, changed records, unchanged records, new records and incremental loading.
