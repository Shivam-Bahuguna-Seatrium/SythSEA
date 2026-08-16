"""Shared value types used across SynthSEA artifacts."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class AccessClass(StrEnum):
    PUBLIC = "public"
    RESTRICTED = "restricted"
    PRIVATE = "private"


class DatasetStatus(StrEnum):
    PENDING_REVIEW = "pending_review"
    ELIGIBLE = "eligible"
    RESTRICTED = "restricted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class RecordStatus(StrEnum):
    PENDING = "pending"
    ELIGIBLE = "eligible"
    REJECTED = "rejected"
    EXCLUDED = "excluded"
    FLAGGED = "flagged"


class Decision(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    FLAG = "flag"
    ABSTAIN = "abstain"
    RETRY = "retry"
    SKIPPED = "skipped"


class RunStatus(StrEnum):
    PLANNED = "planned"
    RUNNING = "running"
    PARTIAL = "partial"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


def utc_now() -> datetime:
    return datetime.now(UTC)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class ArtifactRef(StrictModel):
    artifact_id: str = Field(min_length=1)
    path: str = Field(min_length=1)
    kind: str = Field(min_length=1)
    checksum: str = Field(min_length=1)
    access_class: AccessClass
    source_refs: list[str] = Field(default_factory=list)
    license: str | None = None


class ProvenanceRef(StrictModel):
    source_type: str = Field(min_length=1)
    source_id: str | None = None
    source_version: str | None = None
    parent_refs: list[str] = Field(default_factory=list)
    transformation: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=utc_now)
