from fastapi.testclient import TestClient

from synthsea.api.app import app


def test_eligible_public_dataset_intake_has_lineage_reference() -> None:
    response = TestClient(app).post(
        "/api/datasets/intakes",
        json={
            "record_source": "fixtures/dataset.json",
            "dataset": {
                "dataset_id": "fixture-public",
                "dataset_version": "v1",
                "source_uri_or_reference": "fixture://source",
                "provenance": "fixture provenance",
                "license": "CC-BY-4.0",
                "permitted_use": "research",
                "access_class": "public",
                "retention_rule": "project",
                "language_profile_id": "singlish",
                "acquisition_method": "fixture",
                "content_hash": "hash",
                "record_count": 1,
                "status": "eligible",
            },
        },
    )

    assert response.status_code == 201
    assert response.json()["validation_status"] == "eligible"
    assert response.json()["lineage_artifact_id"] == "dataset:fixture-public:v1"