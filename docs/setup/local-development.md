# Local Development Setup

This guide walks you through setting up TapFlow for local development.

## Prerequisites

### Required Software

| Software | Version | Installation |
|----------|---------|--------------|
| Docker | 24.0+ | [Install Docker](https://docs.docker.com/get-docker/) |
| Docker Compose | 2.20+ | Included with Docker Desktop |
| Python | 3.11+ | [Install Python](https://www.python.org/downloads/) |
| Git | 2.40+ | [Install Git](https://git-scm.com/downloads) |

### System Requirements

- **RAM:** 8GB minimum (16GB recommended)
- **Disk:** 10GB free space
- **CPU:** 4 cores recommended

### Verify Prerequisites

```bash
# Check Docker
docker --version
docker compose version

# Check Python
python3 --version

# Check Git
git --version
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tapflow.git
cd tapflow
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env
cp docker/.env.example docker/.env

# Edit configuration (optional)
# nano .env
```

### 3. Start Services

```bash
# Using Make (recommended)
make start

# Or using Docker Compose directly
docker compose -f docker/docker-compose.yml up -d
```

### 4. Verify Services

Wait ~2 minutes for all services to initialize, then verify:

```bash
# Check service health
make health

# Or manually
docker compose -f docker/docker-compose.yml ps
```

## Service Access Points

Once running, access services at:

| Service | URL | Credentials |
|---------|-----|-------------|
| **API Docs** | http://localhost:8000/docs | - |
| **API Health** | http://localhost:8000/health | - |
| **Airflow** | http://localhost:8080 | admin / admin |
| **Grafana** | http://localhost:3000 | admin / admin |
| **Redpanda Console** | http://localhost:8081 | - |
| **Prometheus** | http://localhost:9090 | - |

## Development Workflow

### Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

### Running Tests

```bash
# All tests
make test

# Unit tests only
pytest tests/unit -v

# Integration tests (requires Docker services)
pytest tests/integration -v

# With coverage
make coverage
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Type checking
make typecheck
```

### Generate Sample Data

```bash
# Start data generation
make generate-data

# Or run manually with options
python -m src.data_generator.main --breweries 10 --days 30

# Stream data to Kafka
python -m src.data_generator.streaming_simulator
```

## Common Development Tasks

### Rebuild Containers

```bash
# Rebuild all containers
make rebuild

# Rebuild specific service
docker compose -f docker/docker-compose.yml build api
```

### View Logs

```bash
# All services
make logs

# Specific service
docker compose -f docker/docker-compose.yml logs -f api

# Last 100 lines
docker compose -f docker/docker-compose.yml logs --tail=100 spark
```

### Access Container Shell

```bash
# API container
docker compose -f docker/docker-compose.yml exec api bash

# Run Python in container
docker compose -f docker/docker-compose.yml exec api python
```

### Database Access

```bash
# DuckDB CLI
docker compose -f docker/docker-compose.yml exec api \
  python -c "import duckdb; db = duckdb.connect('data/tapflow.duckdb'); print(db.execute('SHOW TABLES').fetchall())"

# Redis CLI
docker compose -f docker/docker-compose.yml exec redis redis-cli
```

### Run dbt Models

```bash
# Enter dbt directory
cd src/dbt

# Run all models
dbt run

# Run specific model
dbt run --select daily_sales_summary

# Test models
dbt test
```

## Project Structure

```
tapflow/
├── src/                    # Source code
│   ├── api/               # FastAPI application
│   ├── data_generator/    # Synthetic data generation
│   ├── streaming/         # Real-time processing
│   ├── batch/             # Airflow DAGs
│   ├── dbt/               # Data transformations
│   ├── ml/                # ML models and serving
│   └── utils/             # Shared utilities
├── tests/                  # Test suite
├── docker/                 # Docker configuration
├── docs/                   # Documentation
├── data/                   # Local data storage
├── notebooks/              # Jupyter notebooks
└── scripts/                # Utility scripts
```

## Environment Variables

Key environment variables (see `.env.example` for full list):

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Runtime environment | development |
| `API_PORT` | FastAPI port | 8000 |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker address | redpanda:9092 |
| `REDIS_HOST` | Redis host | redis |
| `DUCKDB_PATH` | DuckDB database path | data/tapflow.duckdb |
| `LOG_LEVEL` | Logging level | INFO |

## Stopping Services

```bash
# Stop all services
make stop

# Stop and remove volumes (clean slate)
make clean
```

## Next Steps

- [Deployment Guide](./deployment.md) - Deploy to production
- [API Endpoints](../api/endpoints.md) - Explore the API
- [Troubleshooting](./troubleshooting.md) - Common issues

## Related Documentation

- [System Architecture](../architecture/system-architecture.md)
- [Data Flow](../architecture/data-flow.md)
