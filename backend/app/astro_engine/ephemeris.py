from __future__ import annotations

PLANET_SPEEDS = {
    "Sun": 0.9856,
    "Moon": 13.1764,
    "Mars": 0.524,
    "Mercury": 1.607,
    "Jupiter": 0.083,
    "Venus": 1.174,
    "Saturn": 0.033,
    "Rahu": -0.053,
}

PLANET_OFFSETS = {
    "Sun": 280.0,
    "Moon": 218.0,
    "Mars": 50.0,
    "Mercury": 180.0,
    "Jupiter": 120.0,
    "Venus": 90.0,
    "Saturn": 300.0,
    "Rahu": 200.0,
}


def normalize_degrees(value: float) -> float:
    return value % 360.0


def planetary_longitudes(julian_day: float) -> dict[str, float]:
    days_since_j2000 = julian_day - 2451545.0
    longitudes: dict[str, float] = {}
    for planet, speed in PLANET_SPEEDS.items():
        longitudes[planet] = normalize_degrees(PLANET_OFFSETS[planet] + speed * days_since_j2000)
    return longitudes
