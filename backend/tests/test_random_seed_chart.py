import random

from app.astro_engine import compute_full_chart
from app.models import BirthDetails


def test_compute_full_chart_fixed_seed_random_like_inputs(monkeypatch):
    random.seed(42)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)

    details = BirthDetails(
        birth_date=f"199{random.randint(0, 9)}-{month:02d}-{day:02d}",
        birth_time=f"{hour:02d}:{minute:02d}",
        timezone_offset=5.5,
        latitude=12.9716,
        longitude=77.5946,
    )

    monkeypatch.setattr(
        "app.astro_engine.planetary_longitudes",
        lambda _jd: {
            "Sun": 10.0,
            "Moon": 45.0,
            "Mars": 90.0,
            "Mercury": 120.0,
            "Jupiter": 150.0,
            "Venus": 180.0,
            "Saturn": 210.0,
            "Rahu": 300.0,
        },
    )

    chart = compute_full_chart(details, latitude=details.latitude, longitude=details.longitude)

    assert chart["ascendant_sign"]
    assert chart["planets"]
    assert "D1" in chart["vargas"] and "D9" in chart["vargas"]
    assert len(chart["mahadasha_timeline"]) > 0
