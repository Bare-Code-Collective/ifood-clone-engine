from fastapi import APIRouter, Query

from app.services.simulation import run_simulation

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@router.get("/run")
def run_simulation_endpoint(
    runs: int = Query(default=100, ge=10, le=5000),
    top_k: int = Query(default=3, ge=1, le=10),
    seed: int = Query(default=42, ge=1, le=999999),
) -> dict:
    return run_simulation(runs=runs, top_k=top_k, seed=seed)
