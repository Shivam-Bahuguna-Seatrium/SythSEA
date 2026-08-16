from pathlib import Path

import pytest

from synthsea.config.contracts import validate_contract
from synthsea.config.loader import ConfigurationError, load_yaml
from synthsea.config.schemas import AccessClass, ArtifactRef, RunStatus
from synthsea.data.manifests import artifact_ref, sha256_file
from synthsea.data.provenance import source_provenance
from synthsea.data.storage import read_json, read_parquet, write_json, write_parquet
from synthsea.tracking.catalog import Catalog


def test_schema_rejects_unknown_access_class() -> None:
    with pytest.raises(ValueError):
        ArtifactRef(
            artifact_id="a",
            path="a.json",
            kind="fixture",
            checksum="hash",
            access_class="unknown",
        )


def test_yaml_loader_requires_mapping(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text("- invalid\n", encoding="utf-8")
    with pytest.raises(ConfigurationError, match="mapping"):
        load_yaml(path)


def test_catalog_registers_run(tmp_path: Path) -> None:
    catalog = Catalog(tmp_path / "catalog.duckdb")
    catalog.register_run("run-1", RunStatus.PLANNED, "config-1")
    assert catalog.get_run("run-1")["status"] == "planned"
    catalog.close()


def test_artifact_storage_and_checksum(tmp_path: Path) -> None:
    json_path = tmp_path / "artifact.json"
    parquet_path = tmp_path / "artifact.parquet"
    write_json(json_path, {"record_id": "r1"})
    write_parquet(parquet_path, [{"record_id": "r1", "value": 1}])
    assert read_json(json_path)["record_id"] == "r1"
    assert read_parquet(parquet_path)[0]["value"] == 1
    first_hash = sha256_file(json_path)
    json_path.write_text('{"record_id": "r2"}\n', encoding="utf-8")
    assert sha256_file(json_path) != first_hash


def test_provenance_and_contract_validation(tmp_path: Path) -> None:
    provenance = source_provenance("dataset-1", "v1", "ingest")
    assert provenance.source_id == "dataset-1"
    artifact_path = tmp_path / "artifact.json"
    write_json(artifact_path, {"ok": True})
    reference = artifact_ref(artifact_path, "fixture", AccessClass.PUBLIC)
    validate_contract(
        {
            "manifest_version": "0.1.0",
            "package_id": "pkg-1",
            "access_class": "public",
            "created_at": "2026-08-13T00:00:00Z",
            "artifacts": [reference.model_dump(mode="json", exclude_none=True)],
            "excluded_artifacts": [],
        },
        Path("specs/001-multilingual-instruction-pipeline/contracts/artifact-manifest.schema.json"),
    )
