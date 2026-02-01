# Data Flow

This document describes how data flows through the TapFlow platform, from ingestion to serving.

## Data Pipeline Overview

```mermaid
flowchart LR
    subgraph "Ingestion"
        A[OpenBreweryDB] --> B[Brewery Loader]
        C[Transaction Generator] --> D[Streaming Simulator]
    end

    subgraph "Streaming"
        D --> E[Redpanda Topics]
        E --> F[Spark Streaming]
        F --> G{Data Quality Check}
        G -->|Pass| H[Bronze Layer]
        G -->|Fail| I[Dead Letter Queue]
    end

    subgraph "Batch Processing"
        H --> J[Silver Layer]
        J --> K[Gold Layer]
        K --> L[dbt Models]
    end

    subgraph "Serving"
        L --> M[Feature Store]
        M --> N[ML Models]
        N --> O[FastAPI]
        K --> O
    end
```

## Medallion Architecture

TapFlow implements the medallion (multi-hop) architecture pattern:

### Bronze Layer (Raw)

```mermaid
flowchart TB
    subgraph "Bronze Layer"
        direction TB
        RAW[Raw Events] --> APPEND[Append-Only Storage]
        APPEND --> PARTITION[Partitioned by Date]
        PARTITION --> IMMUTABLE[Immutable Records]
    end
```

**Characteristics:**
- Raw data exactly as received
- Append-only, immutable
- Partitioned by ingestion date
- Schema-on-read
- Full history retained

**Tables:**
| Table | Description | Partition Key |
|-------|-------------|---------------|
| `raw_transactions` | Sales transactions | `ingestion_date` |
| `raw_breweries` | Brewery metadata | `ingestion_date` |
| `raw_events` | System events | `ingestion_date` |

### Silver Layer (Validated)

```mermaid
flowchart TB
    subgraph "Silver Layer"
        direction TB
        BRONZE[Bronze Data] --> CLEAN[Data Cleaning]
        CLEAN --> DEDUP[Deduplication]
        DEDUP --> VALIDATE[Schema Validation]
        VALIDATE --> ENRICH[Enrichment]
        ENRICH --> SILVER[Silver Tables]
    end
```

**Characteristics:**
- Cleaned and validated
- Deduplicated records
- Strongly typed schemas
- Business keys applied
- Incremental updates

**Tables:**
| Table | Description | Update Frequency |
|-------|-------------|------------------|
| `transactions` | Validated sales | Real-time |
| `breweries` | Enriched brewery data | Daily |
| `inventory` | Current stock levels | Real-time |

### Gold Layer (Business-Ready)

```mermaid
flowchart TB
    subgraph "Gold Layer"
        direction TB
        SILVER[Silver Data] --> AGG[Aggregations]
        AGG --> METRICS[Business Metrics]
        METRICS --> DIMS[Dimension Tables]
        DIMS --> FACTS[Fact Tables]
    end
```

**Characteristics:**
- Business-level aggregations
- Optimized for queries
- Star schema design
- Pre-computed metrics
- SLA-bound freshness

**Tables:**
| Table | Description | Grain |
|-------|-------------|-------|
| `daily_sales_summary` | Daily sales by brewery/beer | Day |
| `hourly_metrics` | Hourly transaction metrics | Hour |
| `inventory_snapshots` | Point-in-time inventory | Hour |
| `brewery_performance` | KPIs by brewery | Day |

## Streaming Data Flow

### Transaction Processing

```mermaid
sequenceDiagram
    participant Gen as Data Generator
    participant Kafka as Redpanda
    participant Spark as Spark Streaming
    participant DQ as Data Quality
    participant Store as Storage

    Gen->>Kafka: Publish transaction
    Kafka->>Spark: Consume event
    Spark->>DQ: Validate schema
    alt Valid
        DQ->>Store: Write to Bronze
        Store->>Spark: Acknowledge
        Spark->>Kafka: Commit offset
    else Invalid
        DQ->>Kafka: Send to DLQ
        Spark->>Kafka: Commit offset
    end
```

### Real-Time Metrics

```mermaid
flowchart LR
    A[Transaction] --> B[Window: 1 min]
    B --> C{Aggregation}
    C --> D[Count]
    C --> E[Sum]
    C --> F[Avg]
    D & E & F --> G[Redis Cache]
    G --> H[API Response]
```

## Batch Processing Flow

### Daily Aggregation DAG

```mermaid
flowchart TB
    subgraph "Airflow DAG: daily_aggregations"
        START([Start]) --> SYNC[Sync Breweries]
        SYNC --> EXTRACT[Extract Transactions]
        EXTRACT --> TRANSFORM[dbt Run]
        TRANSFORM --> QUALITY[Data Quality Tests]
        QUALITY --> FEATURE[Update Feature Store]
        FEATURE --> NOTIFY[Send Notifications]
        NOTIFY --> END([End])
    end
```

### ML Training Pipeline

```mermaid
flowchart TB
    subgraph "Airflow DAG: ml_training"
        START([Start]) --> FEATURES[Extract Features]
        FEATURES --> SPLIT[Train/Test Split]
        SPLIT --> TRAIN[Train Models]
        TRAIN --> EVAL[Evaluate]
        EVAL --> REGISTER[Register in MLflow]
        REGISTER --> DEPLOY{Deploy?}
        DEPLOY -->|Yes| SERVE[Update Serving]
        DEPLOY -->|No| END([End])
        SERVE --> END
    end
```

## Data Quality Framework

### Quality Checks

```mermaid
flowchart TB
    subgraph "Data Quality Checks"
        INPUT[Incoming Data] --> SCHEMA[Schema Validation]
        SCHEMA --> NULL[Null Checks]
        NULL --> RANGE[Range Validation]
        RANGE --> UNIQUE[Uniqueness]
        UNIQUE --> FRESH[Freshness Check]
        FRESH --> ANOMALY[Anomaly Detection]
        ANOMALY --> OUTPUT{Pass?}
        OUTPUT -->|Yes| ACCEPT[Accept Record]
        OUTPUT -->|No| REJECT[Reject/Alert]
    end
```

### Quality Metrics

| Metric | Threshold | Action on Breach |
|--------|-----------|------------------|
| Schema validity | 100% | Reject record |
| Null rate | <5% | Warning |
| Duplicates | 0% | Deduplicate |
| Freshness | <2 hours | Alert |
| Anomaly score | <3σ | Flag for review |

## Feature Store Integration

```mermaid
flowchart LR
    subgraph "Feature Engineering"
        RAW[Raw Data] --> FEAT[Feature Computation]
        FEAT --> ONLINE[Online Store - Redis]
        FEAT --> OFFLINE[Offline Store - Parquet]
    end

    subgraph "Model Serving"
        ONLINE --> REALTIME[Real-time Inference]
        OFFLINE --> BATCH[Batch Predictions]
    end
```

## Data Retention Policy

| Layer | Retention | Storage Format |
|-------|-----------|----------------|
| Bronze | 90 days | Parquet |
| Silver | 1 year | Parquet |
| Gold | 2 years | Parquet |
| Cache | 24 hours | Redis |
| MLflow | Indefinite | SQLite + Artifacts |

## Related Documentation

- [System Architecture](./system-architecture.md) - Component overview
- [API Endpoints](../api/endpoints.md) - Data access patterns
- [Troubleshooting](../setup/troubleshooting.md) - Data pipeline issues
