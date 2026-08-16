"""Governed dataset-intake service built on existing SynthSEA validation."""

from __future__ import annotations

from uuid import uuid4

from synthsea.api.schemas.workbench import DatasetIntakeRequest, DatasetIntakeResponse
from synthsea.config.schemas import DatasetStatus
from synthsea.data.ingest import DatasetIngestor
from synthsea.data.models import SourceDataset


def create_intake(request: DatasetIntakeRequest) -> DatasetIntakeResponse:
    intake_id = f"intake-{uuid4().hex[:12]}"
    try:
        dataset = SourceDataset.model_validate(request.dataset)
        DatasetIngestor().validate_dataset(dataset)
    except ValueError as error:
        return DatasetIntakeResponse(
            intake_id=intake_id,
            validation_status="blocked",
            issues=[str(error)],
        )
    if dataset.status is DatasetStatus.RESTRICTED:
        return DatasetIntakeResponse(
            intake_id=intake_id,
            validation_status="restricted",
            lineage_artifact_id=f"dataset:{dataset.dataset_id}:{dataset.dataset_version}",
        )
    return DatasetIntakeResponse(
        intake_id=intake_id,
        validation_status="eligible",
        lineage_artifact_id=f"dataset:{dataset.dataset_id}:{dataset.dataset_version}",
    )