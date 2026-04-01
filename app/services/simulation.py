import random
from dataclasses import dataclass

from app.schemas.domain import Restaurant, UserProfile
from app.services.data_store import RESTAURANTS, USERS
from app.services.logistics import (
    apply_operational_context,
    estimate_delivery_fee_brl,
    estimate_eta_min,
    haversine_km,
    is_viable,
)
from app.services.recommender import rank_recommendations_for_user


@dataclass
class SessionContext:
    hour: int
    raining: bool
    demand_level: str


@dataclass
class SessionResult:
    user_id: int
    chosen_restaurant_id: int | None
    recommended_ids: list[int]
    recommended_is_viable: bool
    hit_at_k: bool
    baseline_hit_at_k: bool
    context: SessionContext
    eta_min: int | None
    fee_brl: float | None


def _sample_context(rnd: random.Random) -> SessionContext:
    hour = rnd.randint(8, 23)
    raining = rnd.random() < 0.25
    demand_roll = rnd.random()
    if demand_roll < 0.2:
        demand_level = "high"
    elif demand_roll < 0.7:
        demand_level = "normal"
    else:
        demand_level = "low"
    return SessionContext(hour=hour, raining=raining, demand_level=demand_level)


def _dynamic_eta_fee(distance_km: float, context: SessionContext) -> tuple[int, float]:
    base_eta = estimate_eta_min(distance_km)
    base_fee = estimate_delivery_fee_brl(distance_km)
    return apply_operational_context(
        base_eta_min=base_eta,
        base_fee_brl=base_fee,
        hour=context.hour,
        raining=context.raining,
        demand_level=context.demand_level,
    )


def _restaurant_operationally_open(restaurant: Restaurant, context: SessionContext, rnd: random.Random) -> bool:
    if not restaurant.is_open:
        return False
    # Simula indisponibilidade temporaria por pico ou operacao.
    outage_prob = 0.04 + (0.08 if context.demand_level == "high" else 0.0)
    return rnd.random() > outage_prob


def _candidate_restaurants(user: UserProfile, context: SessionContext, rnd: random.Random) -> list[tuple[Restaurant, int, float]]:
    candidates: list[tuple[Restaurant, int, float]] = []
    for restaurant in RESTAURANTS:
        distance = haversine_km(user.location, restaurant.location)
        eta, fee = _dynamic_eta_fee(distance, context)
        is_open_now = _restaurant_operationally_open(restaurant, context, rnd)
        if is_viable(distance, eta, fee, is_open_now):
            candidates.append((restaurant, eta, fee))
    return candidates


def _simulate_user_choice(
    user: UserProfile,
    candidates: list[tuple[Restaurant, int, float]],
    context: SessionContext,
    rnd: random.Random,
) -> int | None:
    if not candidates:
        return None

    weighted_candidates: list[tuple[int, float]] = []
    for rest, eta_min, fee_brl in candidates:
        cuisine_weight = 1.5 if rest.cuisine in user.preferred_cuisines else 0.8
        rating_weight = 0.7 + (rest.rating / 5.0)
        eta_weight = max(0.3, 1 - (eta_min / 80))
        fee_weight = max(0.3, 1 - (fee_brl / 20))
        weather_weight = 0.9 if context.raining else 1.0
        weighted_candidates.append((rest.id, cuisine_weight * rating_weight * eta_weight * fee_weight * weather_weight))

    total_weight = sum(weight for _, weight in weighted_candidates)
    pick = rnd.uniform(0.0, total_weight)
    acc = 0.0
    for rest_id, weight in weighted_candidates:
        acc += weight
        if pick <= acc:
            return rest_id
    return weighted_candidates[-1][0]


def _baseline_nearest(candidates: list[tuple[Restaurant, int, float]], user: UserProfile, top_k: int) -> list[int]:
    ranked = sorted(
        candidates,
        key=lambda item: haversine_km(user.location, item[0].location),
    )
    return [item[0].id for item in ranked[:top_k]]


def run_simulation(
    runs: int = 100,
    top_k: int = 3,
    seed: int = 42,
) -> dict:
    rnd = random.Random(seed)
    sessions: list[SessionResult] = []

    for _ in range(runs):
        user = rnd.choice(USERS)
        context = _sample_context(rnd)
        candidates = _candidate_restaurants(user, context, rnd)
        chosen_restaurant_id = _simulate_user_choice(user, candidates, context, rnd)
        recs = rank_recommendations_for_user(
            user=user,
            top_n=top_k,
            hour=context.hour,
            raining=context.raining,
            demand_level=context.demand_level,
        )
        rec_ids = [item.restaurant_id for item in recs]
        baseline_ids = _baseline_nearest(candidates, user=user, top_k=top_k)

        selected = next((r for r in RESTAURANTS if r.id == chosen_restaurant_id), None)
        if selected:
            dist = haversine_km(user.location, selected.location)
            eta_min, fee_brl = _dynamic_eta_fee(dist, context)
        else:
            eta_min = None
            fee_brl = None

        sessions.append(
            SessionResult(
                user_id=user.id,
                chosen_restaurant_id=chosen_restaurant_id,
                recommended_ids=rec_ids,
                recommended_is_viable=bool(rec_ids),
                hit_at_k=chosen_restaurant_id in rec_ids if chosen_restaurant_id else False,
                baseline_hit_at_k=chosen_restaurant_id in baseline_ids if chosen_restaurant_id else False,
                context=context,
                eta_min=eta_min,
                fee_brl=fee_brl,
            )
        )

    total = len(sessions)
    hits = sum(1 for s in sessions if s.hit_at_k)
    baseline_hits = sum(1 for s in sessions if s.baseline_hit_at_k)
    viable_recommendations = sum(1 for s in sessions if s.recommended_is_viable)
    eta_values = [s.eta_min for s in sessions if s.eta_min is not None]
    fee_values = [s.fee_brl for s in sessions if s.fee_brl is not None]
    rain_sessions = sum(1 for s in sessions if s.context.raining)
    high_demand_sessions = sum(1 for s in sessions if s.context.demand_level == "high")

    return {
        "config": {"runs": runs, "top_k": top_k, "seed": seed},
        "metrics": {
            "precision_at_k": round(hits / total, 4) if total else 0.0,
            "baseline_precision_at_k": round(baseline_hits / total, 4) if total else 0.0,
            "uplift_vs_baseline": round((hits - baseline_hits) / total, 4) if total else 0.0,
            "viable_recommendation_rate": round(viable_recommendations / total, 4) if total else 0.0,
            "avg_eta_min": round(sum(eta_values) / len(eta_values), 2) if eta_values else 0.0,
            "avg_delivery_fee_brl": round(sum(fee_values) / len(fee_values), 2) if fee_values else 0.0,
            "rain_session_rate": round(rain_sessions / total, 4) if total else 0.0,
            "high_demand_session_rate": round(high_demand_sessions / total, 4) if total else 0.0,
        },
        "samples": [
            {
                "user_id": s.user_id,
                "hour": s.context.hour,
                "raining": s.context.raining,
                "demand_level": s.context.demand_level,
                "chosen_restaurant_id": s.chosen_restaurant_id,
                "recommended_ids": s.recommended_ids,
                "hit_at_k": s.hit_at_k,
                "baseline_hit_at_k": s.baseline_hit_at_k,
            }
            for s in sessions[:10]
        ],
    }
