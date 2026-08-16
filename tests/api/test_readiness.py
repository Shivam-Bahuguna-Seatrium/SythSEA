from fastapi.testclient import TestClient

from synthsea.api.app import app


def test_readiness_endpoint_never_reports_missing_report_as_ready() -> None:
    response = TestClient(app).get("/api/readiness")

    assert response.status_code == 200
    assert response.json()["releaseStatus"] == "blocked"