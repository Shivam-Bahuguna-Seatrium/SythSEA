from fastapi.testclient import TestClient

from synthsea.api.app import app


def test_restricted_lineage_does_not_become_public() -> None:
    response = TestClient(app).get("/api/artifacts/restricted-fixture/lineage")

    assert response.status_code == 200
    assert response.json()["access_class"] == "restricted"