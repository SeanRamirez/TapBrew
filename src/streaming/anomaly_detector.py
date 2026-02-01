"""Real-time anomaly detection for streaming data."""

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import numpy as np

from src.utils.logger import logger


@dataclass
class AnomalyResult:
    """Result of anomaly detection."""

    is_anomaly: bool
    field: str
    value: float
    expected_mean: float
    expected_std: float
    z_score: float
    timestamp: datetime


class AnomalyDetector:
    """Detect anomalies using statistical methods."""

    def __init__(self, window_size: int = 1000, z_threshold: float = 3.0):
        """Initialize anomaly detector.

        Args:
            window_size: Number of recent values to consider.
            z_threshold: Z-score threshold for anomaly detection (default 3 sigma).
        """
        self.window_size = window_size
        self.z_threshold = z_threshold
        self.windows: dict[str, deque] = {}

    def _get_window(self, field: str) -> deque:
        """Get or create window for a field."""
        if field not in self.windows:
            self.windows[field] = deque(maxlen=self.window_size)
        return self.windows[field]

    def check(self, field: str, value: float) -> AnomalyResult:
        """Check if a value is anomalous.

        Args:
            field: Field name being checked.
            value: Value to check.

        Returns:
            AnomalyResult with detection details.
        """
        window = self._get_window(field)

        if len(window) < 30:
            # Not enough data for statistical analysis
            window.append(value)
            return AnomalyResult(
                is_anomaly=False,
                field=field,
                value=value,
                expected_mean=value,
                expected_std=0.0,
                z_score=0.0,
                timestamp=datetime.utcnow(),
            )

        mean = np.mean(list(window))
        std = np.std(list(window))

        if std == 0:
            z_score = 0.0
        else:
            z_score = abs((value - mean) / std)

        is_anomaly = z_score > self.z_threshold

        if is_anomaly:
            logger.warning(f"Anomaly detected: {field}={value}, z-score={z_score:.2f}")

        window.append(value)

        return AnomalyResult(
            is_anomaly=is_anomaly,
            field=field,
            value=value,
            expected_mean=mean,
            expected_std=std,
            z_score=z_score,
            timestamp=datetime.utcnow(),
        )

    def check_transaction(self, transaction: dict) -> list[AnomalyResult]:
        """Check a transaction for anomalies.

        Args:
            transaction: Transaction dictionary.

        Returns:
            List of anomaly results for numeric fields.
        """
        results = []

        numeric_fields = ["quantity", "unit_price"]
        for field in numeric_fields:
            if field in transaction and transaction[field] is not None:
                result = self.check(field, float(transaction[field]))
                results.append(result)

        return results
