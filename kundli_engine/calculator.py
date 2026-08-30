from datetime import datetime
from zoneinfo import ZoneInfo

try:
    import swisseph as swe
except ImportError:
    swe = None

SIGNS = [
    "aries","taurus","gemini","cancer","leo","virgo",
    "libra","scorpio","sagittarius","capricorn","aquarius","pisces"
]

PLANETS = {
    "Sun": swe.SUN if swe else 0,
    "Moon": swe.MOON if swe else 1,
    "Mars": swe.MARS if swe else 4,
    "Mercury": swe.MERCURY if swe else 2,
    "Jupiter": swe.JUPITER if swe else 5,
    "Venus": swe.VENUS if swe else 3,
    "Saturn": swe.SATURN if swe else 6,
    "Rahu": swe.MEAN_NODE if swe else 10,
}

def _sign(deg):
    return SIGNS[int((deg % 360) // 30)]

def _house_from_asc(sign_index, planet_sign_index):
    return ((planet_sign_index - sign_index) % 12) + 1

class KundliCalculator:
    """MVP Vedic chart calculator.

    Uses Swiss Ephemeris with Lahiri sidereal mode and whole-sign houses.
    It intentionally returns chart facts only; POS interpretation remains separate.
    """

    def __init__(self):
        if swe is None:
            raise RuntimeError("Install pyswisseph to use the Kundli calculator.")

    def calculate(self, birth):
        local = datetime.fromisoformat(f"{birth.date}T{birth.time}")
        local = local.replace(tzinfo=ZoneInfo(birth.timezone))
        utc = local.astimezone(ZoneInfo("UTC"))
        hour = utc.hour + utc.minute/60 + utc.second/3600
        jd = swe.julday(utc.year, utc.month, utc.day, hour)

        swe.set_sid_mode(swe.SIDM_LAHIRI)
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

        # Swiss Ephemeris houses gives a tropical/sidereal ascendant;
        # we use its sidereal ascendant and then derive whole-sign houses.
        cusps, ascmc = swe.houses_ex(jd, birth.latitude, birth.longitude, b'P')
        asc_deg = ascmc[0]
        asc_sign = _sign(asc_deg)
        asc_idx = SIGNS.index(asc_sign)

        planets = {}
        for name, pid in PLANETS.items():
            xx, _ = swe.calc_ut(jd, pid, flags)
            deg = xx[0] % 360
            sign = _sign(deg)
            sign_idx = SIGNS.index(sign)
            house = _house_from_asc(asc_idx, sign_idx)
            planets[name] = {
                "sign": sign,
                "degree": round(deg % 30, 6),
                "longitude": round(deg, 6),
                "house": house,
                "retrograde": bool(xx[3] < 0),
            }

        # Ketu is exactly opposite Rahu.
        rahu = planets["Rahu"]["longitude"]
        ketu = (rahu + 180) % 360
        ketu_sign = _sign(ketu)
        planets["Ketu"] = {
            "sign": ketu_sign,
            "degree": round(ketu % 30, 6),
            "longitude": round(ketu, 6),
            "house": _house_from_asc(asc_idx, SIGNS.index(ketu_sign)),
            "retrograde": True,
        }

        houses = {
            i+1: {"sign": SIGNS[(asc_idx+i) % 12]}
            for i in range(12)
        }

        return {
            "birth": {
                "date": birth.date,
                "time": birth.time,
                "latitude": birth.latitude,
                "longitude": birth.longitude,
                "timezone": birth.timezone,
            },
            "ayanamsa": "Lahiri",
            "ascendant": {
                "sign": asc_sign,
                "longitude": round(asc_deg % 360, 6),
                "degree": round(asc_deg % 30, 6),
            },
            "planets": planets,
            "houses": houses,
            "divisional_charts": {},
            "metadata": {
                "zodiac": "sidereal",
                "house_system": "whole_sign",
                "ephemeris": "Swiss Ephemeris",
                "note": "Divisional chart calculation is intentionally a separate module boundary."
            }
        }
