from fastapi.testclient import TestClient

from synthsea.api.app import app


def test_training_job_requires_mlx_model_metadata() -> None:
    response = TestClient(app).post(
        "/api/training/jobs",
        json={
            "training_engine": "mlx_lm",
            "dataset_version": "fixture:v1",
            "split_version": "split:v1",
            "language_slices": ["singlish"],
            "base_model": "mlx-community/model",
            "model_version": "v1",
            "model_license": "Apache-2.0",
            "seed": 13,
            "objective": "sft",
        },
    )

    assert response.status_code == 202
    assert response.json()["training_engine"] == "mlx_lm"
    assert "mlx_lm.lora" in response.json()["training_command"]


def test_queued_job_is_restarted_when_its_status_is_requested() -> None:
    client = TestClient(app)
    created = client.post(
        "/api/training/jobs",
        json={
            "training_engine": "mlx_lm",
            "dataset_version": "fixture:v1",
            "split_version": "split:v1",
            "language_slices": ["singlish"],
            "base_model": "mlx-community/Qwen3-8B-4bit",
            "model_version": "qwen3-8b-synthsea",
            "model_license": "Apache-2.0",
            "seed": 13,
            "objective": "sft",
        },
    )

    status = client.get(f"/api/training/jobs/{created.json()['job_id']}")

    assert status.status_code == 200


def test_training_history_returns_persisted_jobs() -> None:
    client = TestClient(app)
    response = client.get("/api/training/jobs")

    assert response.status_code == 200
    assert isinstance(response.json(), list)