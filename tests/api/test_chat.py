from fastapi.testclient import TestClient

from synthsea.api.app import app


def test_chat_models_returns_actionable_unavailable_local_service_state() -> None:
    response = TestClient(app).get("/api/chat/models")

    assert response.status_code == 200
    assert response.json()[0]["local_only"] is True