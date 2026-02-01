"""Pydantic models for API requests and responses."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    service: str


class SaleRecord(BaseModel):
    """Individual sale record."""

    id: str
    brewery_id: str
    beer_name: str
    quantity: int
    price: float
    timestamp: datetime


class SalesResponse(BaseModel):
    """Sales data response."""

    sales: list[SaleRecord]
    total_count: int
    total_revenue: float


class InventoryItem(BaseModel):
    """Inventory item model."""

    beer_name: str
    brewery_id: str
    quantity_available: int
    reorder_point: int
    last_updated: datetime


class DemandPredictionRequest(BaseModel):
    """Request for demand prediction."""

    beer_name: str
    brewery_id: str
    days_ahead: int = Field(default=7, ge=1, le=30)


class DemandPredictionResponse(BaseModel):
    """Demand prediction response."""

    beer_name: str
    brewery_id: str
    predictions: list[dict]
    confidence_interval: Optional[float] = None
