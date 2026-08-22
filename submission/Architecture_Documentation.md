# Architecture Documentation

## 1. Source Architecture

```mermaid
flowchart LR
    O[(manufacturing_oltp)] --> X[Operational Extract]
    X --> R1[source_data/run_1]
    X --> R2[source_data/run_2]
    R1 --> ETL[Python ETL]
    R2 --> ETL
```

The PostgreSQL OLTP model defines the business source. Run 1 and Run 2 CSV directories are reproducible snapshots of the relevant operational entities for the assignment demonstration.

## 2. OLTP Schema

```mermaid
erDiagram
    FACTORY ||--o{ MACHINE : assigns
    PRODUCT ||--o{ PRODUCTION_ORDER : product
    MACHINE ||--o{ PRODUCTION_ORDER : machine
    FACTORY ||--o{ PRODUCTION_ORDER : production_location
    EMPLOYEE ||--o{ PRODUCTION_ORDER : operator
    SHIFT ||--o{ PRODUCTION_ORDER : shift
```

Detailed table attributes and keys are documented in `documentation/oltp_design.md`.

## 3. ETL Architecture

```mermaid
flowchart LR
    A[CSV Source State] --> B[Extract]
    B --> C[Clean + Validate]
    C --> D[(stg_* Tables)]
    D --> E[Load Type 0/1 Dimensions]
    E --> F[Machine SCD Type 2]
    F --> G[Surrogate-Key Lookups]
    G --> H[Load Fact_Production]
    H --> I[Validation]
    I --> J[Analytics]
```

## 4. Staging Schema

The ETL materialises one staging table per source entity:

```text
stg_product
stg_factory
stg_machine
stg_employee
stg_shift
stg_production
```

Staging tables temporarily hold the cleaned source-state data before dimension and fact processing.

## 5. Data Warehouse Star Schema

```mermaid
flowchart TB
    DD[Dim_Date] --> F[Fact_Production]
    DP[Dim_Product] --> F
    DM[Dim_Machine SCD2] --> F
    DF[Dim_Factory] --> F
    DE[Dim_Employee] --> F
    DS[Dim_Shift] --> F
```

`Fact_Production` contains one production event at the declared grain and uses warehouse dimension keys as foreign keys.

## 6. SCD Type 2 Process

```mermaid
flowchart TD
    S[Incoming Machine] --> L{Current Machine_ID exists?}
    L -- No --> N[Generate Machine_Key and insert current row]
    L -- Yes --> C{Tracked attributes changed?}
    C -- No --> U[Keep existing version]
    C -- Yes --> E[Expire old row: Is_Current=false]
    E --> K[Generate new Machine_Key]
    K --> V[Insert new current version]
```

## 7. Two-Run Data Flow

```mermaid
sequenceDiagram
    participant R1 as Run 1 Source
    participant ETL as ETL
    participant DW as Warehouse
    participant R2 as Run 2 Source
    R1->>ETL: Initial master data + PR001/PR002
    ETL->>DW: Initial dimensions and facts
    R2->>ETL: M001 changed, M002 unchanged, M003 new, PR003/PR004
    ETL->>DW: Expire M001 old version
    ETL->>DW: Insert M001 new version + M003
    ETL->>DW: Incrementally insert PR003/PR004
    DW-->>ETL: Historical facts remain on correct Machine_Key
```

## 8. Analytics / Reporting Architecture

```mermaid
flowchart LR
    DW[(PostgreSQL Star Schema)] --> SQL[Analytical SQL]
    DW --> PBI[Power BI Model]
    SQL --> KPI[KPIs and Results]
    PBI --> DASH[Interactive Dashboard]
```

The repository contains analytical SQL and a Power BI implementation specification. The final `.pbix` and screenshots are produced during the final visual-evidence stage.
