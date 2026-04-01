from pydantic import BaseModel


class RecommendationWeights(BaseModel):
    preference: float = 0.5
    viability: float = 0.3
    quality: float = 0.2


class LogisticsRules(BaseModel):
    max_distance_km: float = 8.0
    max_eta_min: int = 45
    max_delivery_fee_brl: float = 12.0


WEIGHTS = RecommendationWeights()
RULES = LogisticsRules()
