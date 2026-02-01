"""Spark Structured Streaming processor for real-time data."""

from typing import Any

from src.utils.config import get_settings
from src.utils.logger import logger


class StreamProcessor:
    """Process streaming data with Spark Structured Streaming."""

    def __init__(self, spark_session=None):
        """Initialize stream processor.

        Args:
            spark_session: Optional SparkSession. If None, creates new session.
        """
        self.settings = get_settings()
        self.spark = spark_session or self._create_spark_session()

    def _create_spark_session(self):
        """Create Spark session for streaming."""
        try:
            from pyspark.sql import SparkSession

            return (
                SparkSession.builder.appName("TapFlow-Streaming")
                .config("spark.sql.streaming.checkpointLocation", "data/checkpoints")
                .getOrCreate()
            )
        except ImportError:
            logger.warning("PySpark not available, returning None")
            return None

    def read_from_kafka(self, topics: list[str]):
        """Read streaming data from Kafka topics.

        Args:
            topics: List of Kafka topics to subscribe to.

        Returns:
            Streaming DataFrame.
        """
        if not self.spark:
            raise RuntimeError("Spark session not available")

        return (
            self.spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", self.settings.kafka_bootstrap_servers)
            .option("subscribe", ",".join(topics))
            .option("startingOffsets", "latest")
            .load()
        )

    def process_sales(self, df) -> Any:
        """Process sales streaming data.

        Args:
            df: Input streaming DataFrame.

        Returns:
            Processed streaming DataFrame.
        """
        from pyspark.sql import functions as F

        return df.select(
            F.from_json(F.col("value").cast("string"), self._get_sales_schema()).alias("data")
        ).select("data.*")

    def _get_sales_schema(self):
        """Get schema for sales data."""
        from pyspark.sql.types import (
            DoubleType,
            IntegerType,
            StringType,
            StructField,
            StructType,
            TimestampType,
        )

        return StructType(
            [
                StructField("transaction_id", StringType(), True),
                StructField("brewery_id", StringType(), True),
                StructField("beer_name", StringType(), True),
                StructField("quantity", IntegerType(), True),
                StructField("unit_price", DoubleType(), True),
                StructField("timestamp", TimestampType(), True),
                StructField("payment_method", StringType(), True),
            ]
        )
