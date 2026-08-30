from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict, Optional

from pos_engine.engine import POSEngine
from pos_engine.models import Chart, PlanetPlacement, HousePlacement
from kundli_engine.calculator import KundliCalculator
from kundli_engine.models import BirthDetails

kundli = KundliCalculator()

app = FastAPI(title="POS Backend", version="0.1.0")
engine = POSEngine()

class PlanetIn(BaseModel):
    sign: str
    house: int
    degree: Optional[float] = None

class ChartIn(BaseModel):
    ascendant: str
    planets: Dict[str, PlanetIn] = {}
    houses: Dict[int, str] = {}
    divisional_charts: Dict[str, dict] = {}

class BirthRequest(BaseModel):
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"

class InterpretRequest(BaseModel):
    chart: ChartIn
    base_traits: Dict[str, float] = Field(..., description="20 latent traits normalized to [0,1]")

@app.get("/health")
def health():
    return {"status": "ok", "model_version": engine.config["model_version"]}

@app.get("/model")
def model():
    return {
        "model_version": engine.config["model_version"],
        "traits": engine.config["traits"],
        "zodiac_styles": engine.config["zodiac_styles"],
    }

@app.post("/kundli/calculate")
def calculate_kundli(req: BirthRequest):
    birth = BirthDetails(**req.model_dump())
    return kundli.calculate(birth)

@app.post("/interpret")
def interpret(req: InterpretRequest):
    missing = [t for t in engine.config["traits"] if t not in req.base_traits]
    if missing:
        return {"error": "Missing traits", "missing": missing}

    invalid = {k:v for k,v in req.base_traits.items() if k in engine.config["traits"] and not 0 <= v <= 1}
    if invalid:
        return {"error": "Traits must be in [0,1]", "invalid": invalid}

    chart = Chart(
        ascendant=req.chart.ascendant,
        planets={k: PlanetPlacement(**v.model_dump()) for k,v in req.chart.planets.items()},
        houses={int(k): HousePlacement(sign=v) for k,v in req.chart.houses.items()},
        divisional_charts=req.chart.divisional_charts,
    )
    return engine.interpret_chart(chart, req.base_traits)
