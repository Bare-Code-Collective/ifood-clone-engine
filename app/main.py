from fastapi import FastAPI

from app.api.routes import (
    analytics_router,
    health_router,
    recommendations_router,
    restaurants_router,
    simulation_router,
)

app = FastAPI(
    title="Baré Code Collective - iFood Engine",
    description="API para recomendacao de restaurantes com filtro de viabilidade logistica",
    version="0.2.0",
)

app.include_router(health_router)
app.include_router(restaurants_router)
app.include_router(recommendations_router)
app.include_router(analytics_router)
app.include_router(simulation_router)