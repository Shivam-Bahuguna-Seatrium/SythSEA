from fastapi.testclient import TestClient

from synthsea.api.app import app


def test_health_endpoint_reports_local_api_status() -> None:
    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_invalid_intake_returns_a_governed_blocked_state() -> None:
    response = TestClient(app).post(
        "/api/datasets/intakes", json={"dataset": {}, "record_source": "fixture"}
    )

    assert response.status_code == 201
    assert response.json()["validation_status"] == "blocked"