from app.api.routes.analytics import router as analytics_router
from app.api.routes.health import router as health_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.restaurants import router as restaurants_router
from app.api.routes.simulation import router as simulation_router

__all__ = [
    "analytics_router",
    "health_router",
    "recommendations_router",
    "restaurants_router",
    "simulation_router",
]
