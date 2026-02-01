"""Tests for data generator module."""

import pytest

from src.data_generator.transaction_generator import (
    BEER_STYLES,
    generate_transaction,
    generate_transactions_batch,
)


class TestTransactionGenerator:
    """Tests for transaction generation."""

    def test_generate_transaction_has_required_fields(self):
        """Test that generated transaction has all required fields."""
        transaction = generate_transaction("brew_001")

        assert "transaction_id" in transaction
        assert "brewery_id" in transaction
        assert "beer_name" in transaction
        assert "quantity" in transaction
        assert "unit_price" in transaction
        assert "timestamp" in transaction
        assert "payment_method" in transaction

    def test_generate_transaction_uses_brewery_id(self):
        """Test that transaction uses the provided brewery ID."""
        brewery_id = "test_brewery_123"
        transaction = generate_transaction(brewery_id)

        assert transaction["brewery_id"] == brewery_id

    def test_generate_transaction_valid_beer_name(self):
        """Test that generated beer name is from valid styles."""
        transaction = generate_transaction("brew_001")

        assert transaction["beer_name"] in BEER_STYLES

    def test_generate_transaction_positive_quantity(self):
        """Test that quantity is positive."""
        transaction = generate_transaction("brew_001")

        assert transaction["quantity"] >= 1

    def test_generate_transaction_positive_price(self):
        """Test that price is positive."""
        transaction = generate_transaction("brew_001")

        assert transaction["unit_price"] > 0

    def test_generate_transactions_batch_count(self):
        """Test that batch generates correct number of transactions."""
        count = 50
        transactions = generate_transactions_batch("brew_001", count=count)

        assert len(transactions) == count

    def test_generate_transactions_batch_sorted(self):
        """Test that batch transactions are sorted by timestamp."""
        transactions = generate_transactions_batch("brew_001", count=20)

        timestamps = [t["timestamp"] for t in transactions]
        assert timestamps == sorted(timestamps)
