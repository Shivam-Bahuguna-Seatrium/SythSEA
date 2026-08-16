from pathlib import Path

import pytest

from synthsea.config.schemas import AccessClass, DatasetStatus, RecordStatus
from synthsea.data.ingest import DatasetIngestor
from synthsea.data.models import DataRecord, SourceDataset
from synthsea.data.provenance import source_provenance


def dataset(access_class: AccessClass = AccessClass.PUBLIC) -> SourceDataset:
    return SourceDataset(
        dataset_id="dataset-1",
        dataset_version="v1",
        source_uri_or_reference="fixture://dataset-1",
        provenance="fixture provenance",
        license="research-permitted",
        permitted_use="research",
        access_class=access_class,
        retention_rule="project lifetime",
        language_profile_id="singlish",
        acquisition_method="fixture",
        content_hash="hash-1",
        record_count=1,
        status=DatasetStatus.ELIGIBLE,
    )


def test_ingestion_preserves_provenance_and_status(tmp_path: Path) -> None:
    record = DataRecord(
        record_id="record-1",
        dataset_id="dataset-1",
        record_version="v1",
        instruction="Say hello",
        response="Hello",
        language_profile_id="singlish",
        task_category="conversation",
        source_type="source_dataset",
        access_class=AccessClass.PUBLIC,
        provenance_ref=source_provenance("dataset-1", "v1", "ingest"),
    )
    result = DatasetIngestor(tmp_path / "catalog.duckdb").ingest(dataset(), [record])
    assert result.dataset.status is DatasetStatus.ELIGIBLE
    assert result.records[0].quality_status is RecordStatus.ELIGIBLE


def test_ingestion_rejects_missing_license() -> None:
    with pytest.raises(ValueError, match="license"):
        SourceDataset.model_validate(dataset().model_dump(exclude={"license"}) | {"license": ""})


def test_source_independent_record_has_no_dataset() -> None:
    record = DataRecord(
        record_id="record-2",
        dataset_id=None,
        record_version="v1",
        instruction="Say hello",
        response="Hello",
        language_profile_id="singlish",
        task_category="conversation",
        source_type="source_independent",
        access_class=AccessClass.PUBLIC,
        provenance_ref=source_provenance("generated", "v1", "generation"),
    )
    assert record.dataset_id is None