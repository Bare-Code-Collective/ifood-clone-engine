from fastapi.testclient import TestClient

from app.main import app


def test_recommendations_accept_context_params() -> None:
    client = TestClient(app)
    response = client.get("/recommendations/100?top_n=3&hour=20&raining=true&demand_level=high")
    assert response.status_code == 200
    payload = response.json()
    assert payload["context"]["hour"] == 20
    assert payload["context"]["raining"] is True
    assert payload["context"]["demand_level"] == "high"


def test_recommendations_invalid_demand_level() -> None:
    client = TestClient(app)
    response = client.get("/recommendations/100?demand_level=extreme")
    assert response.status_code == 422
