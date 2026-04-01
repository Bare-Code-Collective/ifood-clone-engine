from fastapi import APIRouter

from app.services.data_store import RESTAURANTS

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("")
def list_restaurants() -> list[dict]:
    return [restaurant.model_dump() for restaurant in RESTAURANTS]
