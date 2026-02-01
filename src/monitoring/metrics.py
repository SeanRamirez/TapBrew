"""Prometheus metrics for TapFlow monitoring."""

from prometheus_client import Counter, Gauge, Histogram

# Request metrics
REQUEST_COUNT = Counter(
    "tapflow_requests_total",
    "Total number of requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "tapflow_request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# Data pipeline metrics
EVENTS_PROCESSED = Counter(
    "tapflow_events_processed_total",
    "Total number of events processed",
    ["pipeline", "status"],
)

PROCESSING_LAG = Gauge(
    "tapflow_processing_lag_seconds",
    "Processing lag in seconds",
    ["pipeline"],
)

# Data quality metrics
QUALITY_CHECKS_TOTAL = Counter(
    "tapflow_quality_checks_total",
    "Total number of quality checks",
    ["check_name", "result"],
)

ANOMALIES_DETECTED = Counter(
    "tapflow_anomalies_detected_total",
    "Total number of anomalies detected",
    ["field"],
)

# Business metrics
SALES_TOTAL = Counter(
    "tapflow_sales_total",
    "Total sales count",
    ["brewery_id", "beer_name"],
)

REVENUE_TOTAL = Counter(
    "tapflow_revenue_dollars_total",
    "Total revenue in dollars",
    ["brewery_id"],
)

INVENTORY_LEVEL = Gauge(
    "tapflow_inventory_level",
    "Current inventory level",
    ["brewery_id", "beer_name"],
)
