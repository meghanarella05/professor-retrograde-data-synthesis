from pos_engine.engine import POSEngine
from pos_engine.models import TRAITS

def base():
    return {t: 1.0 for t in TRAITS}

def test_zodiac_scaling():
    e = POSEngine()
    out = e.context_vector(base(), zodiac="aries")
    assert out["E"] == 0.20
    assert out["As"] == 0.35
    assert out["O"] == 1.0

def test_planet_scaling():
    e = POSEngine()
    out = e.context_vector(base(), planet="mercury")
    assert out["O"] == 0.30
    assert out["Cur"] == 0.35
    assert out["ST"] == 0.30

def test_house_scaling():
    e = POSEngine()
    out = e.context_vector(base(), house=7)
    assert out["A"] == 0.35
    assert out["Em"] == 0.35
    assert out["Att"] == 0.35

def test_full_chain_is_componentwise():
    e = POSEngine()
    out = e.context_vector(base(), zodiac="aries", planet="mars", house=3, dchart="D9")
    assert out["O"] == 1 * 1 * 1 * .20 * .25
