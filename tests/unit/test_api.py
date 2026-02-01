"""Tests for FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_returns_200(self, client):
        """Test that health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy_status(self, client):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        data = response.json()

        assert data["status"] == "healthy"
        assert data["service"] == "tapflow-api"


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root_returns_200(self, client):
        """Test that root endpoint returns 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_welcome_message(self, client):
        """Test that root returns welcome message."""
        response = client.get("/")
        data = response.json()

        assert "message" in data
        assert "TapFlow" in data["message"]
