from fastapi import APIRouter, HTTPException

from app.astro_engine import compute_full_chart
from app.geo_service import resolve_birth_location
from app.models import BirthDetails, FullChartResponse

router = APIRouter()


@router.post("/full", response_model=FullChartResponse)
def generate_full_chart(details: BirthDetails) -> FullChartResponse:
    try:
        latitude, longitude = resolve_birth_location(details)
        chart = compute_full_chart(details, latitude=latitude, longitude=longitude)
        return FullChartResponse.model_validate(chart)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
