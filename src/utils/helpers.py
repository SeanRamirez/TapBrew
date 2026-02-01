"""Helper functions for TapFlow."""

from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def format_timestamp(dt: datetime) -> str:
    """Format datetime to ISO string."""
    return dt.isoformat()


def safe_get(data: dict, *keys: str, default: Any = None) -> Any:
    """Safely get nested dictionary value.

    Args:
        data: Dictionary to search.
        keys: Sequence of keys to traverse.
        default: Default value if key not found.

    Returns:
        Value at nested key or default.
    """
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data
