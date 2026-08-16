from __future__ import annotations

from datetime import datetime, timedelta

from app.astro_engine.constants import LAHIRI_AYANAMSA_DEGREES, SIGN_NAMES
from app.astro_engine.dasha import compute_vimshottari_timeline
from app.astro_engine.ephemeris import normalize_degrees, planetary_longitudes
from app.astro_engine.nakshatra import nakshatra_and_pada
from app.astro_engine.varga import compute_vargas
from app.models import BirthDetails


def _julian_day(dt_utc: datetime) -> float:
    epoch = datetime(1970, 1, 1)
    return 2440587.5 + (dt_utc - epoch).total_seconds() / 86400.0


def _parse_birth_datetime(details: BirthDetails) -> datetime:
    local_dt = datetime.fromisoformat(f"{details.birth_date.isoformat()}T{details.birth_time}:00")
    return local_dt - timedelta(hours=details.timezone_offset)


def compute_full_chart(details: BirthDetails, *, latitude: float, longitude: float) -> dict:
    birth_utc = _parse_birth_datetime(details)
    jd = _julian_day(birth_utc)

    tropical_positions = planetary_longitudes(jd)
    sidereal_positions = {
        planet: normalize_degrees(lon - LAHIRI_AYANAMSA_DEGREES)
        for planet, lon in tropical_positions.items()
    }
    sidereal_positions["Ketu"] = normalize_degrees(sidereal_positions["Rahu"] + 180.0)

    ascendant_longitude = normalize_degrees((jd * 280.46061837) + longitude + latitude * 0.25)
    ascendant_sign = SIGN_NAMES[int(ascendant_longitude // 30)]

    planets = []
    for planet_name, planet_longitude in sidereal_positions.items():
        nakshatra, pada = nakshatra_and_pada(planet_longitude)
        planets.append(
            {
                "name": planet_name,
                "longitude": round(planet_longitude, 6),
                "sign": SIGN_NAMES[int(planet_longitude // 30)],
                "nakshatra": nakshatra,
                "pada": pada,
            }
        )

    return {
        "ascendant_sign": ascendant_sign,
        "planets": planets,
        "vargas": compute_vargas(sidereal_positions, ascendant_longitude),
        "mahadasha_timeline": compute_vimshottari_timeline(
            sidereal_positions["Moon"],
            birth_utc,
        ),
    }
