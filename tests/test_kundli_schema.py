from kundli_engine.calculator import KundliCalculator
from kundli_engine.models import BirthDetails

def test_calculator_returns_canonical_chart():
    chart = KundliCalculator().calculate(BirthDetails(
        date="2004-01-15", time="10:30:00",
        latitude=12.9716, longitude=77.5946,
        timezone="Asia/Kolkata"
    ))
    assert "ascendant" in chart
    assert "planets" in chart
    assert "houses" in chart
    assert set(chart["houses"]) == set(range(1, 13))
    assert "Rahu" in chart["planets"]
    assert "Ketu" in chart["planets"]
