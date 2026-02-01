"""Simulate streaming data for real-time processing."""

import asyncio
import json
from typing import AsyncGenerator

from src.utils.config import get_settings
from src.utils.logger import logger

from .transaction_generator import generate_transaction


async def stream_transactions(
    brewery_ids: list[str],
    events_per_second: int | None = None,
) -> AsyncGenerator[dict, None]:
    """Generate streaming transactions.

    Args:
        brewery_ids: List of brewery IDs to generate transactions for.
        events_per_second: Rate of event generation.

    Yields:
        Transaction dictionaries.
    """
    settings = get_settings()
    rate = events_per_second or settings.events_per_second
    delay = 1.0 / rate

    logger.info(f"Starting transaction stream at {rate} events/second")

    import random

    while True:
        brewery_id = random.choice(brewery_ids)
        transaction = generate_transaction(brewery_id)
        yield transaction
        await asyncio.sleep(delay)


async def publish_to_kafka(
    producer,
    topic: str,
    brewery_ids: list[str],
    max_events: int | None = None,
) -> None:
    """Publish streaming transactions to Kafka.

    Args:
        producer: Kafka producer instance.
        topic: Kafka topic to publish to.
        brewery_ids: List of brewery IDs.
        max_events: Maximum number of events to publish.
    """
    count = 0
    async for transaction in stream_transactions(brewery_ids):
        message = json.dumps(transaction).encode("utf-8")
        producer.send(topic, value=message)
        count += 1

        if count % 100 == 0:
            logger.info(f"Published {count} transactions")

        if max_events and count >= max_events:
            break
