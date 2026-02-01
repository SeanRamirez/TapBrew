# Troubleshooting Guide

Common issues and solutions for TapFlow development and deployment.

## Quick Diagnostics

```bash
# Check all service status
make health

# View recent logs
make logs

# Check Docker resources
docker system df
docker stats --no-stream
```

## Local Development Issues

### Docker Services Won't Start

**Symptom:** `docker compose up` fails or containers exit immediately.

**Solutions:**

1. **Check Docker is running:**
   ```bash
   docker info
   ```

2. **Check port conflicts:**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # or on Linux
   netstat -tlnp | grep 8000
   ```

3. **Reset Docker environment:**
   ```bash
   make clean
   docker system prune -a
   make start
   ```

4. **Check available memory:**
   ```bash
   # Increase Docker memory to 8GB+ in Docker Desktop settings
   docker info | grep Memory
   ```

### API Returns 500 Errors

**Symptom:** API endpoints return internal server errors.

**Solutions:**

1. **Check API logs:**
   ```bash
   docker compose -f docker/docker-compose.yml logs api
   ```

2. **Verify environment variables:**
   ```bash
   docker compose -f docker/docker-compose.yml exec api env | grep -E "(REDIS|KAFKA|DUCKDB)"
   ```

3. **Test database connection:**
   ```bash
   docker compose -f docker/docker-compose.yml exec api python -c "
   import duckdb
   db = duckdb.connect('data/tapflow.duckdb')
   print('DuckDB OK:', db.execute('SELECT 1').fetchone())
   "
   ```

4. **Test Redis connection:**
   ```bash
   docker compose -f docker/docker-compose.yml exec api python -c "
   import redis
   r = redis.Redis(host='redis', port=6379)
   print('Redis OK:', r.ping())
   "
   ```

### Kafka/Redpanda Connection Failures

**Symptom:** "Kafka broker not available" or connection timeouts.

**Solutions:**

1. **Check Redpanda is running:**
   ```bash
   docker compose -f docker/docker-compose.yml logs redpanda
   ```

2. **Verify topics exist:**
   ```bash
   docker compose -f docker/docker-compose.yml exec redpanda \
     rpk topic list
   ```

3. **Create missing topics:**
   ```bash
   docker compose -f docker/docker-compose.yml exec redpanda \
     rpk topic create transactions --partitions 3
   ```

4. **Check broker address in config:**
   ```bash
   # Should be "redpanda:9092" inside Docker network
   grep KAFKA_BOOTSTRAP_SERVERS .env
   ```

### Tests Failing

**Symptom:** `pytest` tests fail locally.

**Solutions:**

1. **Ensure test dependencies installed:**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run with verbose output:**
   ```bash
   pytest tests/unit -v --tb=long
   ```

3. **Check for import errors:**
   ```bash
   python -c "from src.api.main import app; print('Imports OK')"
   ```

4. **Reset test database:**
   ```bash
   rm -f data/test_tapflow.duckdb
   pytest tests/unit -v
   ```

### Data Generator Not Producing Data

**Symptom:** No data appearing in Kafka topics.

**Solutions:**

1. **Check generator logs:**
   ```bash
   python -m src.data_generator.main --breweries 5 --days 1 --debug
   ```

2. **Verify OpenBreweryDB API:**
   ```bash
   curl -s "https://api.openbrewerydb.org/v1/breweries?per_page=3" | python -m json.tool
   ```

3. **Test Kafka producer:**
   ```bash
   docker compose -f docker/docker-compose.yml exec redpanda \
     rpk topic produce transactions
   # Type a message and press Enter, then Ctrl+D
   ```

## Production Deployment Issues

### Render Deployment Fails

**Symptom:** Build or deploy fails on Render.

**Solutions:**

1. **Check build logs in Render dashboard**

2. **Verify Dockerfile:**
   ```bash
   # Test build locally
   docker build -f docker/api/Dockerfile -t tapflow-api .
   docker run -p 8000:8000 tapflow-api
   ```

3. **Check environment variables are set in Render**

4. **Verify health check endpoint:**
   ```bash
   curl -v https://tapflow-api.onrender.com/health
   ```

### Render Service Sleeping

**Symptom:** First request takes 30+ seconds.

**Explanation:** Free tier services sleep after 15 minutes of inactivity.

**Solutions:**
1. Accept cold start latency (free)
2. Use external uptime monitor (e.g., UptimeRobot)
3. Upgrade to paid plan ($7/month)

### Vercel Build Fails

**Symptom:** Dashboard deployment fails.

**Solutions:**

1. **Check build logs in Vercel dashboard**

2. **Test build locally:**
   ```bash
   cd dashboard
   npm install
   npm run build
   ```

3. **Verify environment variables in Vercel settings**

4. **Check API URL is correct:**
   ```bash
   # Should be the full Render URL
   echo $NEXT_PUBLIC_API_URL
   ```

### Redis Connection Refused

**Symptom:** "Connection refused" to Redis Cloud.

**Solutions:**

1. **Verify credentials:**
   ```bash
   redis-cli -h <host> -p <port> -a <password> ping
   ```

2. **Check IP allowlist in Redis Cloud dashboard**

3. **Verify TLS settings** (Redis Cloud requires TLS):
   ```python
   import redis
   r = redis.Redis(
       host='your-host',
       port=your-port,
       password='your-password',
       ssl=True  # Required for Redis Cloud
   )
   ```

## Data Pipeline Issues

### dbt Models Failing

**Symptom:** `dbt run` fails with errors.

**Solutions:**

1. **Check dbt logs:**
   ```bash
   cd src/dbt
   dbt run --debug
   ```

2. **Verify source data exists:**
   ```bash
   dbt source freshness
   ```

3. **Test specific model:**
   ```bash
   dbt run --select model_name
   dbt test --select model_name
   ```

4. **Validate SQL syntax:**
   ```bash
   dbt compile --select model_name
   cat target/compiled/tapflow/models/model_name.sql
   ```

### Airflow DAGs Not Running

**Symptom:** DAGs show but don't execute.

**Solutions:**

1. **Check DAG is enabled** (toggle in Airflow UI)

2. **Check scheduler logs:**
   ```bash
   docker compose -f docker/docker-compose.yml logs airflow-scheduler
   ```

3. **Verify DAG has no import errors:**
   ```bash
   docker compose -f docker/docker-compose.yml exec airflow-scheduler \
     airflow dags list-import-errors
   ```

4. **Trigger manual run:**
   ```bash
   docker compose -f docker/docker-compose.yml exec airflow-scheduler \
     airflow dags trigger daily_aggregations
   ```

### Data Quality Alerts

**Symptom:** Data quality checks failing.

**Solutions:**

1. **Check which checks failed:**
   ```bash
   dbt test --store-failures
   ```

2. **Investigate failed records:**
   ```sql
   SELECT * FROM dbt_test__audit.failed_checks LIMIT 10;
   ```

3. **Review thresholds in `src/streaming/data_quality_checks.py`**

## Performance Issues

### Slow API Responses

**Symptom:** API latency > 1 second.

**Solutions:**

1. **Check Redis cache hit rate:**
   ```bash
   docker compose -f docker/docker-compose.yml exec redis \
     redis-cli INFO stats | grep keyspace
   ```

2. **Profile slow queries:**
   ```python
   # Add to query
   import time
   start = time.time()
   # ... query ...
   print(f"Query took {time.time() - start:.2f}s")
   ```

3. **Add database indexes:**
   ```sql
   CREATE INDEX idx_transactions_brewery ON transactions(brewery_id);
   ```

### High Memory Usage

**Symptom:** Containers being OOM killed.

**Solutions:**

1. **Check memory limits:**
   ```bash
   docker stats --no-stream
   ```

2. **Increase container memory in `docker-compose.yml`:**
   ```yaml
   services:
     spark:
       deploy:
         resources:
           limits:
             memory: 4G
   ```

3. **Reduce Spark executor memory:**
   ```python
   spark = SparkSession.builder \
       .config("spark.executor.memory", "1g") \
       .getOrCreate()
   ```

## Getting Help

If you can't resolve an issue:

1. **Check existing issues:** [GitHub Issues](https://github.com/yourusername/tapflow/issues)
2. **Create detailed bug report** with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Relevant logs
   - Environment details

## Related Documentation

- [Local Development](./local-development.md) - Setup guide
- [Deployment](./deployment.md) - Production deployment
- [System Architecture](../architecture/system-architecture.md) - How it works
