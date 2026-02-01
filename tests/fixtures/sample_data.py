"""Sample data fixtures for testing."""

from datetime import datetime, timedelta

SAMPLE_BREWERY = {
    "id": "test-brewery-001",
    "name": "Test Brewing Co",
    "brewery_type": "micro",
    "city": "Portland",
    "state": "Oregon",
    "postal_code": "97201",
    "country": "United States",
    "latitude": "45.5152",
    "longitude": "-122.6784",
}

SAMPLE_BREWERIES = [
    SAMPLE_BREWERY,
    {
        "id": "test-brewery-002",
        "name": "Sample Ales",
        "brewery_type": "brewpub",
        "city": "Seattle",
        "state": "Washington",
        "postal_code": "98101",
        "country": "United States",
        "latitude": "47.6062",
        "longitude": "-122.3321",
    },
]


def generate_sample_transactions(count: int = 10) -> list[dict]:
    """Generate sample transactions for testing.

    Args:
        count: Number of transactions to generate.

    Returns:
        List of transaction dictionaries.
    """
    base_time = datetime.utcnow() - timedelta(days=1)
    transactions = []

    for i in range(count):
        transactions.append(
            {
                "transaction_id": f"txn_{i:04d}",
                "brewery_id": "test-brewery-001",
                "beer_name": "Test IPA",
                "quantity": 2,
                "unit_price": 7.50,
                "timestamp": (base_time + timedelta(minutes=i * 10)).isoformat(),
                "payment_method": "card",
            }
        )

    return transactions


SAMPLE_INVENTORY = [
    {
        "beer_name": "Hazy IPA",
        "brewery_id": "test-brewery-001",
        "quantity_available": 100,
        "reorder_point": 20,
        "last_updated": datetime.utcnow().isoformat(),
    },
    {
        "beer_name": "Stout",
        "brewery_id": "test-brewery-001",
        "quantity_available": 15,
        "reorder_point": 20,
        "last_updated": datetime.utcnow().isoformat(),
    },
]
