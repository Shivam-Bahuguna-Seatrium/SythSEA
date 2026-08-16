"""Dataset and record entities."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field, model_validator

from synthsea.config.schemas import (
    AccessClass,
    DatasetStatus,
    ProvenanceRef,
    RecordStatus,
    StrictModel,
    utc_now,
)


class SourceDataset(StrictModel):
    dataset_id: str = Field(min_length=1)
    dataset_version: str = Field(min_length=1)
    source_uri_or_reference: str = Field(min_length=1)
    provenance: str = Field(min_length=1)
    license: str = Field(min_length=1)
    permitted_use: str = Field(min_length=1)
    access_class: AccessClass
    retention_rule: str = Field(min_length=1)
    language_profile_id: str = Field(min_length=1)
    acquisition_method: str = Field(min_length=1)
    content_hash: str = Field(min_length=1)
    record_count: int = Field(ge=0)
    created_at: datetime = Field(default_factory=utc_now)
    status: DatasetStatus = DatasetStatus.PENDING_REVIEW


class DataRecord(StrictModel):
    record_id: str = Field(min_length=1)
    dataset_id: str | None = None
    record_version: str = Field(min_length=1)
    instruction: str = Field(min_length=1)
    response: str = Field(min_length=1)
    language_profile_id: str = Field(min_length=1)
    task_category: str = Field(min_length=1)
    source_type: str = "source_dataset"
    access_class: AccessClass
    provenance_ref: ProvenanceRef
    quality_status: RecordStatus = RecordStatus.ELIGIBLE
    created_at: datetime = Field(default_factory=utc_now)
    content_hash: str | None = None
    switch_condition: str | None = None
    switch_points: list[int] = Field(default_factory=list)
    switch_direction: str | None = None
    language_proportion: float | None = Field(default=None, ge=0, le=1)
    communicative_intent: str | None = None

    @model_validator(mode="after")
    def validate_source_reference(self) -> DataRecord:
        if self.source_type == "source_independent" and self.dataset_id is not None:
            raise ValueError("source-independent records cannot reference a dataset")
        if self.source_type != "source_independent" and self.dataset_id is None:
            raise ValueError("dataset_id is required for source-backed records")
        return self
