from fastapi import APIRouter, HTTPException, Query

from app.services.data_store import get_user
from app.services.recommender import rank_recommendations_for_user, top_next_cuisine

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/{user_id}")
def get_recommendations(
    user_id: int,
    top_n: int = Query(default=5, ge=1, le=20),
    hour: int = Query(default=12, ge=0, le=23),
    raining: bool = Query(default=False),
    demand_level: str = Query(default="normal", pattern="^(low|normal|high)$"),
) -> dict:
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    recommendations = rank_recommendations_for_user(
        user=user,
        top_n=top_n,
        hour=hour,
        raining=raining,
        demand_level=demand_level,
    )
    return {
        "user_id": user.id,
        "user_name": user.name,
        "context": {"hour": hour, "raining": raining, "demand_level": demand_level},
        "predicted_next_cuisine": top_next_cuisine(user_id=user_id),
        "items": [item.model_dump() for item in recommendations],
    }
