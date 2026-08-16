from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_post_full_chart_returns_expected_keys(monkeypatch):
    monkeypatch.setattr("app.geo_service.geocode_place", lambda _place: (28.6139, 77.2090))
    monkeypatch.setattr(
        "app.astro_engine.planetary_longitudes",
        lambda _jd: {
            "Sun": 100.0,
            "Moon": 130.0,
            "Mars": 150.0,
            "Mercury": 170.0,
            "Jupiter": 190.0,
            "Venus": 210.0,
            "Saturn": 230.0,
            "Rahu": 250.0,
        },
    )

    response = client.post(
        "/api/chart/full",
        json={
            "birth_date": "1990-05-17",
            "birth_time": "10:30",
            "timezone_offset": 5.5,
            "place": "New Delhi, India",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == {"ascendant_sign", "planets", "vargas", "mahadasha_timeline"}
    assert "D1" in payload["vargas"]
    assert "D9" in payload["vargas"]
    assert any(planet["name"] == "Ketu" for planet in payload["planets"])
