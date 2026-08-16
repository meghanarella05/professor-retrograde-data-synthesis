from __future__ import annotations

from app.astro_engine.constants import NAKSHATRAS

NAKSHATRA_SPAN = 360 / 27
PADA_SPAN = NAKSHATRA_SPAN / 4


def nakshatra_and_pada(longitude: float) -> tuple[str, int]:
    normalized = longitude % 360.0
    nakshatra_index = int(normalized // NAKSHATRA_SPAN) % len(NAKSHATRAS)
    pada = int((normalized % NAKSHATRA_SPAN) // PADA_SPAN) + 1
    return NAKSHATRAS[nakshatra_index], pada
