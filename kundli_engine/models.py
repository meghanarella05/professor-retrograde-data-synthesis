from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class BirthDetails:
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"

@dataclass
class KundliChart:
    birth: BirthDetails
    ayanamsa: str
    ascendant: Dict
    planets: Dict
    houses: Dict
    divisional_charts: Dict = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)
