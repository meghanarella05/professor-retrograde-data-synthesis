from dataclasses import dataclass, field
from typing import Dict, Optional

TRAITS = ["O","C","E","A","ES","Cur","AD","D","Cr","Ad","ER","R","As","Em","Att","RT","Au","P","ST","SC"]

@dataclass
class PlanetPlacement:
    sign: str
    house: int
    degree: Optional[float] = None

@dataclass
class HousePlacement:
    sign: str

@dataclass
class Chart:
    ascendant: str
    planets: Dict[str, PlanetPlacement]
    houses: Dict[int, HousePlacement]
    divisional_charts: Dict[str, Dict] = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)

@dataclass
class TraitVector:
    values: Dict[str, float]

    def as_list(self):
        return [self.values[t] for t in TRAITS]
