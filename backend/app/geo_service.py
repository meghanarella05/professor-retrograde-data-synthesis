from __future__ import annotations

from geopy.geocoders import Nominatim

from app.models import BirthDetails


def geocode_place(place: str) -> tuple[float, float]:
    geolocator = Nominatim(user_agent="vedic-chart-engine")
    location = geolocator.geocode(place)
    if not location:
        raise ValueError(f"Unable to resolve place: {place}")
    return float(location.latitude), float(location.longitude)


def resolve_birth_location(details: BirthDetails) -> tuple[float, float]:
    if details.latitude is not None and details.longitude is not None:
        return details.latitude, details.longitude
    if not details.place:
        raise ValueError("Either latitude/longitude or place must be provided")
    return geocode_place(details.place)
