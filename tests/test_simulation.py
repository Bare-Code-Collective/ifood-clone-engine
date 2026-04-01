from fastapi.testclient import TestClient

from app.main import app
from app.services.simulation import run_simulation


def test_simulation_service_metrics_range() -> None:
    result = run_simulation(runs=60, top_k=3, seed=123)
    metrics = result["metrics"]

    assert 0.0 <= metrics["precision_at_k"] <= 1.0
    assert 0.0 <= metrics["baseline_precision_at_k"] <= 1.0
    assert 0.0 <= metrics["viable_recommendation_rate"] <= 1.0
    assert -1.0 <= metrics["uplift_vs_baseline"] <= 1.0
    assert 0.0 <= metrics["rain_session_rate"] <= 1.0
    assert 0.0 <= metrics["high_demand_session_rate"] <= 1.0
    assert metrics["avg_eta_min"] >= 0.0
    assert metrics["avg_delivery_fee_brl"] >= 0.0


def test_simulation_endpoint_returns_expected_contract() -> None:
    client = TestClient(app)
    response = client.get("/simulation/run?runs=50&top_k=3&seed=7")
    assert response.status_code == 200

    payload = response.json()
    assert "config" in payload
    assert "metrics" in payload
    assert "samples" in payload
    assert payload["config"]["runs"] == 50
    assert payload["config"]["top_k"] == 3
    assert "baseline_precision_at_k" in payload["metrics"]
