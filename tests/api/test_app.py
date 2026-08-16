from fastapi.testclient import TestClient

from synthsea.api.app import app


def test_local_frontend_origin_receives_cors_headers() -> None:
    response = TestClient(app).options(
        "/api/health",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"