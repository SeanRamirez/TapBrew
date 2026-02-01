"""Inventory API router."""

from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.get("/status")
async def get_inventory_status(
    beer: str | None = None,
    brewery_id: str | None = None,
):
    """Get current inventory status."""
    # TODO: Implement inventory status
    return {"inventory": [], "beer": beer, "brewery_id": brewery_id}


@router.get("/alerts")
async def get_inventory_alerts():
    """Get inventory alerts for low stock items."""
    # TODO: Implement inventory alerts
    return {"alerts": [], "count": 0}
