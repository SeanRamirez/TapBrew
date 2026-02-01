# 🍺 TapFlow: Real-Time Brewery Analytics Platform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![API Status](https://img.shields.io/badge/API-Live-success)](https://tapflow-api.onrender.com/docs)

**Production-grade data engineering platform demonstrating real-time streaming, MLOps, and modern data stack patterns.**

[Live API](https://tapflow-api.onrender.com/docs) • [Dashboard](https://tapflow.vercel.app) • [Architecture](#architecture) • [Demo Video](https://youtube.com/...)

---

## 📊 Project Overview

TapFlow is a comprehensive data platform built to showcase senior-level data engineering skills including:

- **Real-time streaming** with Kafka-compatible event processing
- **Modern lakehouse architecture** using Delta Lake patterns with DuckDB
- **Production MLOps** with automated training, versioning, and deployment
- **Data quality frameworks** ensuring reliability at every layer
- **Infrastructure as Code** with full reproducibility

### Business Context

Brewery taprooms generate valuable data but lack analytics infrastructure. TapFlow provides:
- Real-time sales dashboards and inventory tracking
- Predictive analytics for demand forecasting
- Event performance analysis
- Automated alerts for inventory runouts

---

## 🏗️ Architecture

![System Architecture](docs/architecture/diagrams/architecture.png)

### Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Streaming** | Redpanda (Kafka-compatible), Spark Structured Streaming |
| **Storage** | DuckDB, Parquet, Delta Lake patterns, S3 |
| **Orchestration** | Apache Airflow |
| **Transformation** | dbt-core |
| **ML/AI** | MLflow, Feast, scikit-learn, Prophet |
| **API** | FastAPI, Redis, GraphQL |
| **Monitoring** | Prometheus, Grafana |
| **Infrastructure** | Docker, Terraform, GitHub Actions |

### Data Flow
```
OpenBreweryDB API → Synthetic Data Generator → Redpanda Topics
                                                      ↓
                                            Spark Streaming
                                    ↓               ↓              ↓
                              Bronze Layer    Data Quality    Real-time Cache
                                  ↓               Checks           (Redis)
                              Silver Layer          ↓
                                  ↓            Anomaly Alerts
                              Gold Layer
                                  ↓
                        dbt Transformations → Feature Store (Feast)
                                                      ↓
                                              ML Models (MLflow)
                                                      ↓
                                              FastAPI Endpoints
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- 8GB RAM minimum
- Git

### Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/tapflow.git
cd tapflow

# Copy environment template
cp docker/.env.example docker/.env

# Start all services
make start

# Wait for services to be healthy (~2 minutes)
# Access points will be displayed
```

**Services:**
- API: http://localhost:8000/docs
- Airflow: http://localhost:8080 (admin/admin)
- Grafana: http://localhost:3000 (admin/admin)
- Redpanda Console: http://localhost:8081

### Generate Sample Data
```bash
# Start data generation (streams to Redpanda)
make generate-data

# Or run manually
python src/data_generator/main.py --breweries 10 --days 30
```

---

## 📈 Key Features

### 1. Real-Time Streaming Pipeline

- **Sub-500ms latency** from event to dashboard
- Kafka-compatible streaming with Redpanda
- Spark Structured Streaming with windowed aggregations
- Exactly-once semantics with checkpointing

### 2. Data Quality Framework

- Great Expectations integration for schema validation
- Real-time anomaly detection (3σ statistical monitoring)
- Data freshness SLAs (<2 hours)
- Automated alerting to Slack

### 3. MLOps Pipeline

- **Demand Forecasting**: 30-day predictions with 85%+ accuracy (MAPE)
- **Inventory Prediction**: Automated runout alerts
- **Anomaly Detection**: Isolation Forest for unusual patterns
- Automated weekly retraining with drift detection
- A/B testing framework for model deployment

### 4. Modern Data Stack

- **Medallion Architecture**: Bronze/Silver/Gold layers
- **dbt-core**: Version-controlled transformations with 50+ tests
- **Incremental models**: Process only new data
- **Data lineage**: Full documentation of dependencies

### 5. Production Observability

- Prometheus metrics for all services
- Grafana dashboards (system, data quality, business)
- Custom data freshness and quality metrics
- PagerDuty/Slack integration for critical alerts

---

## 📊 Demo & Screenshots

### Live API Endpoints
```bash
# Real-time sales
curl https://tapflow-api.onrender.com/api/sales/realtime

# Demand forecast
curl -X POST https://tapflow-api.onrender.com/api/predict/demand \
  -H "Content-Type: application/json" \
  -d '{"beer_name": "Hazy IPA", "brewery_id": "brew_001"}'

# Inventory status
curl https://tapflow-api.onrender.com/api/inventory/status?beer=hazy_ipa
```

### Grafana Dashboard
![Dashboard Screenshot](docs/screenshots/dashboard.png)

### Data Quality Monitoring
![Quality Dashboard](docs/screenshots/data-quality.png)

---

## 🧪 Testing
```bash
# Run all tests
make test

# Unit tests only
pytest tests/unit -v

# Integration tests
pytest tests/integration -v

# Coverage report
make coverage
```

**Current Coverage: 85%+**

---

## 📚 Documentation

- [System Architecture](docs/architecture/system-architecture.md)
- [Data Pipeline Flow](docs/architecture/data-flow.md)
- [Local Development Setup](docs/setup/local-development.md)
- [Deployment Guide](docs/setup/deployment.md)
- [API Documentation](docs/api/endpoints.md)
- [Troubleshooting](docs/setup/troubleshooting.md)

---

## 🌐 Deployment

### Production (Hybrid Free Tier)

**Local Processing:**
- Spark jobs for heavy ETL
- Airflow DAGs for orchestration
- ML model training

**Cloud Services (Free Tier):**
- API: Render.com (750 hrs/month)
- Dashboard: Vercel (unlimited)
- Storage: AWS S3 (5GB free)
- Cache: Redis Cloud (30MB free)
```bash
# Deploy to cloud
make deploy
```

See [Deployment Guide](docs/setup/deployment.md) for details.

---

## 🎯 Project Goals & Learnings

**Technical Skills Demonstrated:**
- ✅ Real-time streaming architecture (Kafka, Spark)
- ✅ Data lakehouse implementation (medallion architecture)
- ✅ Production MLOps (training, versioning, serving)
- ✅ Data quality engineering (Great Expectations, monitoring)
- ✅ Modern data stack (dbt, orchestration, IaC)
- ✅ API development (FastAPI, caching, optimization)
- ✅ DevOps practices (Docker, CI/CD, monitoring)

**Business Impact:**
- Reduces inventory waste through predictive analytics
- Identifies profitable events through performance tracking
- Prevents stockouts with automated runout alerts
- Provides real-time business intelligence

---

## 🛠️ Development

### Project Structure
```
src/
├── data_generator/    # Synthetic data creation
├── streaming/         # Real-time processing
├── batch/            # Airflow DAGs
├── dbt/              # Data transformations
├── ml/               # ML pipeline & serving
├── api/              # FastAPI application
└── monitoring/       # Observability
```

### Contributing

While this is a portfolio project, suggestions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 👤 Author

**Your Name**
- LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- Portfolio: [yourwebsite.com](https://yourwebsite.com)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- OpenBreweryDB for brewery data
- Apache projects (Spark, Airflow, Kafka)
- dbt Labs for modern data transformation
- The data engineering community

---

## 📊 Project Stats

- **Lines of Code**: ~5,000+
- **Test Coverage**: 85%+
- **Build Time**: 6 weeks
- **Technologies**: 15+
- **Docker Services**: 10+

---

**⭐ If this project helped you learn or inspired your own work, please give it a star!**
