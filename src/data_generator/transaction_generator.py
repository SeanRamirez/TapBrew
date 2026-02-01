"""Generate synthetic transaction data for breweries."""

import random
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

BEER_STYLES = [
    "Hazy IPA",
    "West Coast IPA",
    "Pale Ale",
    "Pilsner",
    "Lager",
    "Stout",
    "Porter",
    "Wheat Beer",
    "Sour",
    "Amber Ale",
]

PRICE_RANGE = {"min": 5.0, "max": 12.0}
QUANTITY_RANGE = {"min": 1, "max": 4}


def generate_transaction(
    brewery_id: str,
    timestamp: datetime | None = None,
) -> dict[str, Any]:
    """Generate a single synthetic transaction.

    Args:
        brewery_id: ID of the brewery.
        timestamp: Transaction timestamp. If None, uses current time.

    Returns:
        Transaction dictionary.
    """
    return {
        "transaction_id": str(uuid4()),
        "brewery_id": brewery_id,
        "beer_name": random.choice(BEER_STYLES),
        "quantity": random.randint(QUANTITY_RANGE["min"], QUANTITY_RANGE["max"]),
        "unit_price": round(random.uniform(PRICE_RANGE["min"], PRICE_RANGE["max"]), 2),
        "timestamp": (timestamp or datetime.utcnow()).isoformat(),
        "payment_method": random.choice(["card", "cash", "mobile"]),
    }


def generate_transactions_batch(
    brewery_id: str,
    count: int = 100,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[dict[str, Any]]:
    """Generate a batch of transactions.

    Args:
        brewery_id: ID of the brewery.
        count: Number of transactions to generate.
        start_date: Start of date range.
        end_date: End of date range.

    Returns:
        List of transaction dictionaries.
    """
    start = start_date or datetime.utcnow() - timedelta(days=30)
    end = end_date or datetime.utcnow()
    time_range = (end - start).total_seconds()

    transactions = []
    for _ in range(count):
        random_offset = random.uniform(0, time_range)
        timestamp = start + timedelta(seconds=random_offset)
        transactions.append(generate_transaction(brewery_id, timestamp))

    return sorted(transactions, key=lambda x: x["timestamp"])
