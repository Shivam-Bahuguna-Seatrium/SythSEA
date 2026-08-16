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