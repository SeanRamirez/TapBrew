"""Predictions API router."""

from fastapi import APIRouter

from src.api.models import DemandPredictionRequest, DemandPredictionResponse

router = APIRouter(prefix="/api/predict", tags=["predictions"])


@router.post("/demand", response_model=DemandPredictionResponse)
async def predict_demand(request: DemandPredictionRequest):
    """Predict demand for a specific beer."""
    # TODO: Implement demand prediction using ML model
    return DemandPredictionResponse(
        beer_name=request.beer_name,
        brewery_id=request.brewery_id,
        predictions=[],
        confidence_interval=0.95,
    )


@router.get("/inventory-runout")
async def predict_inventory_runout(
    brewery_id: str,
    beer_name: str,
):
    """Predict when inventory will run out."""
    # TODO: Implement runout prediction
    return {
        "brewery_id": brewery_id,
        "beer_name": beer_name,
        "predicted_runout_date": None,
        "days_remaining": None,
    }
