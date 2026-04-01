from collections import Counter

from app.core.config import WEIGHTS
from app.schemas.domain import RecommendationItem, Restaurant, UserProfile
from app.services.data_store import ORDER_EVENTS, RESTAURANTS
from app.services.logistics import (
    apply_operational_context,
    estimate_delivery_fee_brl,
    estimate_eta_min,
    haversine_km,
    is_viable,
    viability_score,
)


def _preference_score(user: UserProfile, restaurant: Restaurant) -> float:
    cuisine_bonus = 0.55 if restaurant.cuisine in user.preferred_cuisines else 0.15
    spend_gap = abs(restaurant.avg_ticket_brl - user.avg_spend_brl)
    spend_component = max(0.0, 1 - (spend_gap / 50))
    return round(min(1.0, cuisine_bonus + spend_component * 0.45), 4)


def _quality_score(restaurant: Restaurant) -> float:
    return round(restaurant.rating / 5, 4)


def _contextual_preference_adjustment(cuisine: str, hour: int) -> float:
    if hour in {11, 12, 13} and cuisine in {"regional", "saudavel"}:
        return 0.06
    if hour in {19, 20, 21} and cuisine in {"pizza", "hamburguer", "japonesa"}:
        return 0.08
    return 0.0


def _reason_tags(user: UserProfile, restaurant: Restaurant, distance_km: float, eta_min: int) -> list[str]:
    reasons: list[str] = []
    if restaurant.cuisine in user.preferred_cuisines:
        reasons.append("categoria que voce costuma pedir")
    if distance_km <= 3.0:
        reasons.append("muito perto da sua localizacao")
    if eta_min <= 30:
        reasons.append("entrega rapida estimada")
    if restaurant.rating >= 4.5:
        reasons.append("alta avaliacao dos clientes")
    return reasons or ["equilibrio entre preferencia e viabilidade"]


def rank_recommendations_for_user(
    user: UserProfile,
    top_n: int = 5,
    hour: int = 12,
    raining: bool = False,
    demand_level: str = "normal",
) -> list[RecommendationItem]:
    ranked: list[RecommendationItem] = []
    for restaurant in RESTAURANTS:
        distance_km = round(haversine_km(user.location, restaurant.location), 2)
        base_eta = estimate_eta_min(distance_km)
        base_fee = estimate_delivery_fee_brl(distance_km)
        eta_min, fee_brl = apply_operational_context(
            base_eta_min=base_eta,
            base_fee_brl=base_fee,
            hour=hour,
            raining=raining,
            demand_level=demand_level,
        )

        if not is_viable(distance_km, eta_min, fee_brl, restaurant.is_open):
            continue

        score_pref = min(
            1.0,
            _preference_score(user, restaurant)
            + _contextual_preference_adjustment(restaurant.cuisine, hour),
        )
        score_via = viability_score(distance_km, eta_min, fee_brl)
        score_qual = _quality_score(restaurant)
        score_final = round(
            score_pref * WEIGHTS.preference
            + score_via * WEIGHTS.viability
            + score_qual * WEIGHTS.quality,
            4,
        )

        ranked.append(
            RecommendationItem(
                restaurant_id=restaurant.id,
                restaurant_name=restaurant.name,
                cuisine=restaurant.cuisine,
                distance_km=distance_km,
                eta_min=eta_min,
                delivery_fee_brl=fee_brl,
                score_preference=score_pref,
                score_viability=score_via,
                score_quality=score_qual,
                score_final=score_final,
                reasons=_reason_tags(user, restaurant, distance_km, eta_min),
            )
        )

    ranked.sort(key=lambda rec: rec.score_final, reverse=True)
    return ranked[:top_n]


def top_next_cuisine(user_id: int) -> str | None:
    user_events = [event for event in ORDER_EVENTS if event.user_id == user_id]
    if not user_events:
        return None

    restaurant_by_id = {restaurant.id: restaurant for restaurant in RESTAURANTS}
    cuisines = [
        restaurant_by_id[event.restaurant_id].cuisine
        for event in user_events
        if event.restaurant_id in restaurant_by_id
    ]
    if not cuisines:
        return None

    return Counter(cuisines).most_common(1)[0][0]
