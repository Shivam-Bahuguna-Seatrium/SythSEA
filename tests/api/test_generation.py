from fastapi.testclient import TestClient

from synthsea.api.app import app


def test_generation_endpoint_requires_a_governed_request() -> None:
    response = TestClient(app).post("/api/generation/runs", json={})

    assert response.status_code == 422