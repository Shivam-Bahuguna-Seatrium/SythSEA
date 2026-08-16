"""Dataset eligibility and provenance-aware ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from synthsea.config.schemas import DatasetStatus, RecordStatus, RunStatus
from synthsea.data.models import DataRecord, SourceDataset
from synthsea.tracking.catalog import Catalog


@dataclass(frozen=True)
class IngestionResult:
    dataset: SourceDataset
    records: list[DataRecord]


class DatasetIngestor:
    def __init__(self, catalog_path: Path | None = None) -> None:
        self.catalog = Catalog(catalog_path) if catalog_path is not None else None

    def validate_dataset(self, dataset: SourceDataset) -> None:
        if not dataset.license.strip():
            raise ValueError("license is required")
        if not dataset.provenance.strip():
            raise ValueError("provenance is required")
        if not dataset.retention_rule.strip():
            raise ValueError("retention_rule is required")
        if dataset.status not in {DatasetStatus.ELIGIBLE, DatasetStatus.RESTRICTED}:
            raise ValueError(f"dataset is not eligible for ingestion: {dataset.status.value}")

    def ingest(self, dataset: SourceDataset, records: list[DataRecord]) -> IngestionResult:
        self.validate_dataset(dataset)
        for record in records:
            if (
                record.source_type != "source_independent"
                and record.dataset_id != dataset.dataset_id
            ):
                raise ValueError(f"record {record.record_id} references a different dataset")
            if dataset.access_class.value != record.access_class.value:
                raise ValueError(f"record {record.record_id} access class does not match dataset")
            if record.quality_status is not RecordStatus.ELIGIBLE:
                raise ValueError(f"record {record.record_id} is not eligible")
        if self.catalog is not None:
            self.catalog.register_run(dataset.dataset_id, status=RunStatus.COMPLETED)
        return IngestionResult(dataset=dataset, records=records)
