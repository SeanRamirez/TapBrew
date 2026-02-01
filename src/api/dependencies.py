"""FastAPI dependencies for dependency injection."""

from functools import lru_cache
from typing import Generator

import redis

from src.utils.config import get_settings


@lru_cache()
def get_redis_client() -> redis.Redis:
    """Get Redis client instance."""
    settings = get_settings()
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True,
    )


def get_redis() -> Generator[redis.Redis, None, None]:
    """Dependency for Redis client."""
    client = get_redis_client()
    try:
        yield client
    finally:
        pass  # Connection pooling handles cleanup
