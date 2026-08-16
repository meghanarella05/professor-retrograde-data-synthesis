from __future__ import annotations

from app.astro_engine.constants import SIGN_NAMES


def _sign_from_longitude(longitude: float) -> str:
    return SIGN_NAMES[int((longitude % 360.0) // 30)]


def _d9_sign(longitude: float) -> str:
    sign_index = int((longitude % 360.0) // 30)
    segment_index = int(((longitude % 30) / (30 / 9)))
    navamsa_index = (sign_index * 9 + segment_index) % 12
    return SIGN_NAMES[navamsa_index]


def compute_vargas(planets: dict[str, float], ascendant_longitude: float) -> dict[str, dict[str, str]]:
    d1 = {planet: _sign_from_longitude(lon) for planet, lon in planets.items()}
    d1["Ascendant"] = _sign_from_longitude(ascendant_longitude)

    d9 = {planet: _d9_sign(lon) for planet, lon in planets.items()}
    d9["Ascendant"] = _d9_sign(ascendant_longitude)

    return {"D1": d1, "D9": d9}
