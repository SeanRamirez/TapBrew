"""Sales API router."""

from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/sales", tags=["sales"])


@router.get("/realtime")
async def get_realtime_sales(
    limit: int = Query(default=100, ge=1, le=1000),
):
    """Get real-time sales data."""
    # TODO: Implement real-time sales fetching
    return {"sales": [], "total_count": 0, "message": "Not implemented yet"}


@router.get("/summary")
async def get_sales_summary(
    brewery_id: str | None = None,
    days: int = Query(default=7, ge=1, le=90),
):
    """Get sales summary for a time period."""
    # TODO: Implement sales summary
    return {"summary": {}, "brewery_id": brewery_id, "days": days}
