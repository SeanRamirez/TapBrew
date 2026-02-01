# API Endpoints

TapFlow API provides RESTful endpoints for accessing brewery analytics data.

**Base URL:**
- Local: `http://localhost:8000`
- Production: `https://tapflow-api.onrender.com`

**Interactive Docs:** `/docs` (Swagger UI) or `/redoc` (ReDoc)

## Overview

```mermaid
flowchart LR
    subgraph "API Endpoints"
        HEALTH[/health]
        SALES[/api/sales/*]
        INV[/api/inventory/*]
        PRED[/api/predict/*]
        METRICS[/metrics]
    end

    CLIENT[Client] --> HEALTH
    CLIENT --> SALES
    CLIENT --> INV
    CLIENT --> PRED
    PROM[Prometheus] --> METRICS
```

## Health & Status

### Health Check

Check API health status.

```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "0.1.0",
  "services": {
    "database": "connected",
    "redis": "connected",
    "kafka": "connected"
  }
}
```

### Metrics

Prometheus metrics endpoint.

```
GET /metrics
```

**Response:** Prometheus text format

---

## Sales Endpoints

### Real-Time Sales

Get current real-time sales metrics.

```
GET /api/sales/realtime
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `brewery_id` | string | No | Filter by brewery |
| `window` | string | No | Time window (1m, 5m, 1h). Default: 5m |

**Response:**
```json
{
  "window_start": "2024-01-15T10:25:00Z",
  "window_end": "2024-01-15T10:30:00Z",
  "metrics": {
    "total_transactions": 142,
    "total_revenue": 1847.50,
    "average_transaction": 13.01,
    "top_beers": [
      {"name": "Hazy IPA", "quantity": 45},
      {"name": "Pilsner", "quantity": 38}
    ]
  }
}
```

**Example:**
```bash
curl "https://tapflow-api.onrender.com/api/sales/realtime?window=1h"
```

### Sales Summary

Get aggregated sales data.

```
GET /api/sales/summary
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `brewery_id` | string | No | Filter by brewery |
| `start_date` | string | No | Start date (ISO format) |
| `end_date` | string | No | End date (ISO format) |
| `granularity` | string | No | hour, day, week. Default: day |

**Response:**
```json
{
  "period": {
    "start": "2024-01-01",
    "end": "2024-01-15"
  },
  "summary": {
    "total_revenue": 45230.00,
    "total_transactions": 3421,
    "unique_customers": 1205,
    "average_transaction": 13.22
  },
  "by_period": [
    {
      "date": "2024-01-01",
      "revenue": 3150.00,
      "transactions": 245
    }
  ]
}
```

**Example:**
```bash
curl "https://tapflow-api.onrender.com/api/sales/summary?start_date=2024-01-01&granularity=week"
```

### Sales by Beer

Get sales breakdown by beer type.

```
GET /api/sales/by-beer
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `brewery_id` | string | No | Filter by brewery |
| `limit` | int | No | Number of results. Default: 10 |
| `period` | string | No | today, week, month. Default: week |

**Response:**
```json
{
  "period": "week",
  "beers": [
    {
      "name": "Hazy IPA",
      "quantity_sold": 523,
      "revenue": 3922.50,
      "percentage_of_total": 23.5
    },
    {
      "name": "Pilsner",
      "quantity_sold": 412,
      "revenue": 2472.00,
      "percentage_of_total": 18.2
    }
  ]
}
```

---

## Inventory Endpoints

### Current Inventory

Get current inventory status.

```
GET /api/inventory/status
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `brewery_id` | string | No | Filter by brewery |
| `beer` | string | No | Filter by beer name |
| `low_stock_only` | bool | No | Only show low stock items |

**Response:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "inventory": [
    {
      "beer_name": "Hazy IPA",
      "brewery_id": "brew_001",
      "quantity_available": 45,
      "reorder_point": 20,
      "status": "ok",
      "days_until_runout": 12
    },
    {
      "beer_name": "Stout",
      "brewery_id": "brew_001",
      "quantity_available": 8,
      "reorder_point": 20,
      "status": "low",
      "days_until_runout": 2
    }
  ]
}
```

**Example:**
```bash
curl "https://tapflow-api.onrender.com/api/inventory/status?low_stock_only=true"
```

### Inventory History

Get historical inventory levels.

```
GET /api/inventory/history
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `brewery_id` | string | Yes | Brewery ID |
| `beer` | string | Yes | Beer name |
| `days` | int | No | Days of history. Default: 30 |

**Response:**
```json
{
  "brewery_id": "brew_001",
  "beer_name": "Hazy IPA",
  "history": [
    {
      "date": "2024-01-15",
      "opening_quantity": 100,
      "closing_quantity": 45,
      "sold": 55,
      "restocked": 0
    }
  ]
}
```

---

## Prediction Endpoints

### Demand Forecast

Predict future demand for a beer.

```
POST /api/predict/demand
```

**Request Body:**
```json
{
  "brewery_id": "brew_001",
  "beer_name": "Hazy IPA",
  "days_ahead": 30
}
```

**Response:**
```json
{
  "brewery_id": "brew_001",
  "beer_name": "Hazy IPA",
  "model_version": "1.2.0",
  "confidence_interval": 0.95,
  "predictions": [
    {
      "date": "2024-01-16",
      "predicted_quantity": 42,
      "lower_bound": 35,
      "upper_bound": 49
    },
    {
      "date": "2024-01-17",
      "predicted_quantity": 38,
      "lower_bound": 31,
      "upper_bound": 45
    }
  ]
}
```

**Example:**
```bash
curl -X POST "https://tapflow-api.onrender.com/api/predict/demand" \
  -H "Content-Type: application/json" \
  -d '{"brewery_id": "brew_001", "beer_name": "Hazy IPA", "days_ahead": 7}'
```

### Inventory Runout Prediction

Predict when inventory will run out.

```
GET /api/predict/inventory-runout
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `brewery_id` | string | Yes | Brewery ID |
| `beer_name` | string | Yes | Beer name |

**Response:**
```json
{
  "brewery_id": "brew_001",
  "beer_name": "Hazy IPA",
  "current_quantity": 45,
  "predicted_runout_date": "2024-01-27",
  "days_remaining": 12,
  "confidence": 0.87,
  "recommendation": "Consider restocking by 2024-01-24"
}
```

---

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid brewery_id format",
    "details": {
      "field": "brewery_id",
      "value": "invalid",
      "constraint": "Must match pattern: brew_[0-9]+"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req_abc123"
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request parameters |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Dependency unavailable |

---

## Rate Limiting

| Tier | Requests/minute | Burst |
|------|-----------------|-------|
| Free | 60 | 10 |
| Authenticated | 300 | 50 |

Rate limit headers:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705315800
```

---

## Caching

Responses include cache headers:

```
Cache-Control: public, max-age=60
ETag: "abc123"
```

| Endpoint | Cache TTL |
|----------|-----------|
| `/api/sales/realtime` | 10 seconds |
| `/api/sales/summary` | 5 minutes |
| `/api/inventory/status` | 30 seconds |
| `/api/predict/*` | 1 hour |

---

## SDKs & Examples

### Python

```python
import httpx

API_BASE = "https://tapflow-api.onrender.com"

# Get real-time sales
response = httpx.get(f"{API_BASE}/api/sales/realtime")
data = response.json()
print(f"Revenue: ${data['metrics']['total_revenue']}")

# Get demand prediction
response = httpx.post(
    f"{API_BASE}/api/predict/demand",
    json={
        "brewery_id": "brew_001",
        "beer_name": "Hazy IPA",
        "days_ahead": 7
    }
)
predictions = response.json()["predictions"]
```

### JavaScript

```javascript
const API_BASE = "https://tapflow-api.onrender.com";

// Get inventory status
const response = await fetch(`${API_BASE}/api/inventory/status?low_stock_only=true`);
const data = await response.json();

// Filter critical items
const critical = data.inventory.filter(item => item.days_until_runout < 3);
```

### cURL

```bash
# Health check
curl https://tapflow-api.onrender.com/health

# Sales summary with date range
curl "https://tapflow-api.onrender.com/api/sales/summary?start_date=2024-01-01&end_date=2024-01-31"

# Post demand forecast
curl -X POST https://tapflow-api.onrender.com/api/predict/demand \
  -H "Content-Type: application/json" \
  -d '{"brewery_id": "brew_001", "beer_name": "Hazy IPA", "days_ahead": 14}'
```

---

## Related Documentation

- [System Architecture](../architecture/system-architecture.md) - How the API fits in
- [Data Flow](../architecture/data-flow.md) - Data sources for endpoints
- [Local Development](../setup/local-development.md) - Run API locally
