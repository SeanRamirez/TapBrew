"""Caching utilities for API responses."""

import json
from typing import Any, Optional

import redis

from src.utils.logger import logger


class CacheManager:
    """Redis cache manager for API responses."""

    def __init__(self, client: redis.Redis, default_ttl: int = 300):
        """Initialize cache manager.

        Args:
            client: Redis client instance.
            default_ttl: Default TTL in seconds (5 minutes).
        """
        self.client = client
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache.

        Args:
            key: Cache key.

        Returns:
            Cached value or None if not found.
        """
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache.

        Args:
            key: Cache key.
            value: Value to cache.
            ttl: Time to live in seconds.

        Returns:
            True if successful.
        """
        try:
            self.client.setex(
                key,
                ttl or self.default_ttl,
                json.dumps(value, default=str),
            )
            return True
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache.

        Args:
            key: Cache key to delete.

        Returns:
            True if key was deleted.
        """
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.warning(f"Cache delete error: {e}")
            return False
