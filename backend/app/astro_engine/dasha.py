from __future__ import annotations

from datetime import datetime, timedelta

from app.astro_engine.constants import VIMSHOTTARI_SEQUENCE, VIMSHOTTARI_YEARS


def compute_vimshottari_timeline(moon_longitude: float, birth_utc: datetime, periods: int = 9) -> list[dict[str, str]]:
    nakshatra_index = int((moon_longitude % 360.0) // (360 / 27))
    sequence_index = nakshatra_index % len(VIMSHOTTARI_SEQUENCE)
    current_lord = VIMSHOTTARI_SEQUENCE[sequence_index]

    start = birth_utc
    timeline: list[dict[str, str]] = []
    for i in range(periods):
        lord = VIMSHOTTARI_SEQUENCE[(sequence_index + i) % len(VIMSHOTTARI_SEQUENCE)]
        years = VIMSHOTTARI_YEARS[lord]
        end = start + timedelta(days=int(years * 365.25))
        timeline.append({"lord": lord, "start": start.isoformat(), "end": end.isoformat()})
        start = end

    if not timeline or timeline[0]["lord"] != current_lord:
        raise RuntimeError("Failed to generate vimshottari sequence")

    return timeline
