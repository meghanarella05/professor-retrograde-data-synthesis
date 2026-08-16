from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, Field


class BirthDetails(BaseModel):
    birth_date: date
    birth_time: str = Field(pattern=r"^\d{2}:\d{2}$")
    timezone_offset: float = 0.0
    place: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class PlanetPosition(BaseModel):
    name: str
    longitude: float
    sign: str
    nakshatra: str
    pada: int


class DashaPeriod(BaseModel):
    lord: str
    start: str
    end: str


class FullChartResponse(BaseModel):
    ascendant_sign: str
    planets: list[PlanetPosition]
    vargas: dict[str, dict[str, Any]]
    mahadasha_timeline: list[DashaPeriod]
