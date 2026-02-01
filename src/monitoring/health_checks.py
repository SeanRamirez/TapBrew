"""Health check utilities for TapFlow services."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx

from src.utils.config import get_settings
from src.utils.logger import logger


@dataclass
class HealthStatus:
    """Health status of a service."""

    service: str
    healthy: bool
    message: str
    latency_ms: float | None = None
    timestamp: datetime | None = None
    details: dict | None = None


async def check_redis_health() -> HealthStatus:
    """Check Redis connection health."""
    settings = get_settings()
    start = datetime.utcnow()

    try:
        import redis

        client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            socket_timeout=5,
        )
        client.ping()
        latency = (datetime.utcnow() - start).total_seconds() * 1000

        return HealthStatus(
            service="redis",
            healthy=True,
            message="Connected",
            latency_ms=latency,
            timestamp=datetime.utcnow(),
        )
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return HealthStatus(
            service="redis",
            healthy=False,
            message=str(e),
            timestamp=datetime.utcnow(),
        )


async def check_kafka_health() -> HealthStatus:
    """Check Kafka connection health."""
    settings = get_settings()

    try:
        from kafka import KafkaAdminClient

        admin = KafkaAdminClient(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            request_timeout_ms=5000,
        )
        topics = admin.list_topics()

        return HealthStatus(
            service="kafka",
            healthy=True,
            message="Connected",
            timestamp=datetime.utcnow(),
            details={"topics_count": len(topics)},
        )
    except Exception as e:
        logger.error(f"Kafka health check failed: {e}")
        return HealthStatus(
            service="kafka",
            healthy=False,
            message=str(e),
            timestamp=datetime.utcnow(),
        )


async def check_all_services() -> dict[str, HealthStatus]:
    """Check health of all services.

    Returns:
        Dictionary of service names to health status.
    """
    checks = {
        "redis": check_redis_health,
        "kafka": check_kafka_health,
    }

    results = {}
    for service, check_fn in checks.items():
        try:
            results[service] = await check_fn()
        except Exception as e:
            results[service] = HealthStatus(
                service=service,
                healthy=False,
                message=f"Check failed: {e}",
                timestamp=datetime.utcnow(),
            )

    return results
