"""Data quality checks for streaming data."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.logger import logger


@dataclass
class QualityCheckResult:
    """Result of a data quality check."""

    check_name: str
    passed: bool
    message: str
    timestamp: datetime
    details: dict | None = None


class DataQualityChecker:
    """Perform data quality checks on streaming data."""

    def __init__(self):
        """Initialize data quality checker."""
        self.checks = []

    def check_not_null(self, record: dict, fields: list[str]) -> QualityCheckResult:
        """Check that specified fields are not null.

        Args:
            record: Data record to check.
            fields: List of field names that should not be null.

        Returns:
            QualityCheckResult.
        """
        null_fields = [f for f in fields if record.get(f) is None]

        return QualityCheckResult(
            check_name="not_null",
            passed=len(null_fields) == 0,
            message=f"Null fields: {null_fields}" if null_fields else "All fields present",
            timestamp=datetime.utcnow(),
            details={"null_fields": null_fields},
        )

    def check_value_range(
        self,
        record: dict,
        field: str,
        min_val: float | None = None,
        max_val: float | None = None,
    ) -> QualityCheckResult:
        """Check that field value is within expected range.

        Args:
            record: Data record to check.
            field: Field name to check.
            min_val: Minimum acceptable value.
            max_val: Maximum acceptable value.

        Returns:
            QualityCheckResult.
        """
        value = record.get(field)

        if value is None:
            return QualityCheckResult(
                check_name="value_range",
                passed=False,
                message=f"Field {field} is null",
                timestamp=datetime.utcnow(),
            )

        in_range = True
        if min_val is not None and value < min_val:
            in_range = False
        if max_val is not None and value > max_val:
            in_range = False

        return QualityCheckResult(
            check_name="value_range",
            passed=in_range,
            message=f"{field}={value} in range [{min_val}, {max_val}]"
            if in_range
            else f"{field}={value} out of range",
            timestamp=datetime.utcnow(),
            details={"field": field, "value": value, "min": min_val, "max": max_val},
        )

    def run_all_checks(self, record: dict) -> list[QualityCheckResult]:
        """Run all configured quality checks.

        Args:
            record: Data record to check.

        Returns:
            List of QualityCheckResults.
        """
        results = []

        # Required fields check
        required_fields = ["transaction_id", "brewery_id", "beer_name", "quantity", "unit_price"]
        results.append(self.check_not_null(record, required_fields))

        # Value range checks
        results.append(self.check_value_range(record, "quantity", min_val=1, max_val=100))
        results.append(self.check_value_range(record, "unit_price", min_val=0.01, max_val=100.0))

        failed = [r for r in results if not r.passed]
        if failed:
            logger.warning(f"Quality checks failed: {[r.check_name for r in failed]}")

        return results
