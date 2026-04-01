from pydantic import BaseModel, Field


class Location(BaseModel):
    lat: float
    lon: float


class Restaurant(BaseModel):
    id: int
    name: str
    cuisine: str
    avg_ticket_brl: float
    rating: float = Field(ge=0.0, le=5.0)
    location: Location
    is_open: bool = True


class UserProfile(BaseModel):
    id: int
    name: str
    preferred_cuisines: list[str]
    avg_spend_brl: float
    location: Location


class OrderEvent(BaseModel):
    user_id: int
    restaurant_id: int
    total_brl: float
    hour: int = Field(ge=0, le=23)


class RecommendationItem(BaseModel):
    restaurant_id: int
    restaurant_name: str
    cuisine: str
    distance_km: float
    eta_min: int
    delivery_fee_brl: float
    score_preference: float
    score_viability: float
    score_quality: float
    score_final: float
    reasons: list[str]
