"""Configuration management for TapFlow."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Project
    project_name: str = "tapflow"
    environment: str = "development"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4

    # Kafka/Redpanda
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_schema_registry_url: str = "http://localhost:8081"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    # DuckDB
    duckdb_path: str = "data/tapflow.duckdb"

    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"

    # Data Generator
    brewery_count: int = 50
    simulation_days: int = 90
    events_per_second: int = 10

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
