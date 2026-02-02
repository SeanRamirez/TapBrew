"""Simulate streaming data for real-time processing."""

import argparse
import asyncio
import json
import random
import sys
from typing import AsyncGenerator

from kafka import KafkaProducer
from kafka.errors import KafkaError

from src.data_generator.brewery_loader import fetch_breweries
from src.data_generator.transaction_generator import generate_transaction
from src.utils.config import get_settings
from src.utils.logger import logger


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

    while True:
        brewery_id = random.choice(brewery_ids)
        transaction = generate_transaction(brewery_id)
        yield transaction
        await asyncio.sleep(delay)


def create_kafka_producer(bootstrap_servers: str) -> KafkaProducer:
    """Create and return a Kafka producer.

    Args:
        bootstrap_servers: Kafka bootstrap servers address.

    Returns:
        Configured KafkaProducer instance.
    """
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks="all",
            retries=3,
        )
        logger.info(f"Connected to Kafka at {bootstrap_servers}")
        return producer
    except KafkaError as e:
        logger.error(f"Failed to connect to Kafka: {e}")
        raise


async def publish_to_kafka(
    producer: KafkaProducer,
    topic: str,
    brewery_ids: list[str],
    events_per_second: int = 10,
    max_events: int | None = None,
) -> None:
    """Publish streaming transactions to Kafka.

    Args:
        producer: Kafka producer instance.
        topic: Kafka topic to publish to.
        brewery_ids: List of brewery IDs.
        events_per_second: Rate of event generation.
        max_events: Maximum events to publish (None for infinite).
    """
    count = 0
    async for transaction in stream_transactions(brewery_ids, events_per_second):
        try:
            future = producer.send(topic, value=transaction)
            future.get(timeout=10)
            count += 1

            if count % 100 == 0:
                logger.info(f"Published {count} transactions to {topic}")
                logger.info(
                    f"Sample: {transaction['beer_name']} x{transaction['quantity']} "
                    f"@ ${transaction['unit_price']} from {transaction['brewery_id'][:20]}..."
                )

            if max_events and count >= max_events:
                logger.info(f"Reached max events limit: {max_events}")
                break

        except KafkaError as e:
            logger.error(f"Failed to send message: {e}")

    producer.flush()


async def main(args: argparse.Namespace) -> None:
    """Main entry point for the streaming simulator."""
    settings = get_settings()

    # Fetch breweries from OpenBreweryDB
    logger.info(f"Fetching {args.breweries} breweries from OpenBreweryDB...")
    breweries = await fetch_breweries(limit=args.breweries, state=args.state)

    if not breweries:
        logger.warning("No breweries fetched. Using fallback IDs.")
        brewery_ids = [f"brewery_{i}" for i in range(1, 6)]
    else:
        brewery_ids = [b["id"] for b in breweries]
        logger.info(f"Loaded {len(brewery_ids)} brewery IDs")
        for b in breweries[:3]:
            logger.info(f"  - {b.get('name', 'Unknown')} ({b.get('city', 'Unknown')}, {b.get('state', 'Unknown')})")

    # Create Kafka producer
    bootstrap_servers = args.kafka or settings.kafka_bootstrap_servers
    producer = create_kafka_producer(bootstrap_servers)

    # Start streaming
    logger.info(f"Streaming transactions to topic: {args.topic}")
    logger.info(f"Rate: {args.rate} events/second")
    logger.info("Press Ctrl+C to stop\n")

    try:
        await publish_to_kafka(
            producer=producer,
            topic=args.topic,
            brewery_ids=brewery_ids,
            events_per_second=args.rate,
            max_events=args.max_events,
        )
    except KeyboardInterrupt:
        logger.info("\nStopping streaming simulator...")
    finally:
        producer.close()
        logger.info("Kafka producer closed")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Stream synthetic brewery transactions to Kafka"
    )
    parser.add_argument(
        "--kafka",
        type=str,
        default="localhost:9092",
        help="Kafka bootstrap servers (default: localhost:9092)",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="transactions",
        help="Kafka topic to publish to (default: transactions)",
    )
    parser.add_argument(
        "--breweries",
        type=int,
        default=10,
        help="Number of breweries to fetch (default: 10)",
    )
    parser.add_argument(
        "--state",
        type=str,
        default=None,
        help="US state to filter breweries (e.g., california)",
    )
    parser.add_argument(
        "--rate",
        type=int,
        default=10,
        help="Events per second (default: 10)",
    )
    parser.add_argument(
        "--max-events",
        type=int,
        default=None,
        help="Maximum events to generate (default: unlimited)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args))
