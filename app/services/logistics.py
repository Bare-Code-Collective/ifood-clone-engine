from math import asin, cos, radians, sin, sqrt

from app.core.config import RULES
from app.schemas.domain import Location


def haversine_km(origin: Location, destination: Location) -> float:
    earth_radius_km = 6371.0
    dlat = radians(destination.lat - origin.lat)
    dlon = radians(destination.lon - origin.lon)
    lat1 = radians(origin.lat)
    lat2 = radians(destination.lat)

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return earth_radius_km * c


def estimate_eta_min(distance_km: float) -> int:
    base_prep_time = 18
    travel_time = int(distance_km * 3.8)
    return base_prep_time + travel_time


def estimate_delivery_fee_brl(distance_km: float) -> float:
    base_fee = 3.5
    return round(base_fee + distance_km * 1.25, 2)


def apply_operational_context(
    base_eta_min: int,
    base_fee_brl: float,
    hour: int,
    raining: bool,
    demand_level: str,
) -> tuple[int, float]:
    rain_multiplier = 1.25 if raining else 1.0
    demand_multiplier = {"low": 0.95, "normal": 1.0, "high": 1.2}.get(demand_level, 1.0)
    hour_multiplier = 1.15 if hour in {11, 12, 13, 19, 20, 21} else 1.0

    eta_min = int(base_eta_min * rain_multiplier * demand_multiplier * hour_multiplier)
    fee_brl = round(
        base_fee_brl * (1 + (0.2 if raining else 0.0) + (0.15 if demand_level == "high" else 0.0)),
        2,
    )
    return eta_min, fee_brl


def viability_score(distance_km: float, eta_min: int, fee_brl: float) -> float:
    distance_component = max(0.0, 1 - (distance_km / RULES.max_distance_km))
    eta_component = max(0.0, 1 - (eta_min / RULES.max_eta_min))
    fee_component = max(0.0, 1 - (fee_brl / RULES.max_delivery_fee_brl))
    return round((distance_component + eta_component + fee_component) / 3, 4)


def is_viable(distance_km: float, eta_min: int, fee_brl: float, is_open: bool) -> bool:
    if not is_open:
        return False
    if distance_km > RULES.max_distance_km:
        return False
    if eta_min > RULES.max_eta_min:
        return False
    if fee_brl > RULES.max_delivery_fee_brl:
        return False
    return True
