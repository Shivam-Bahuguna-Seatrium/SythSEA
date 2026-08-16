"""Persistent local-workspace entities and state transitions."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from synthsea.config.schemas import StrictModel, utc_now


class TrainingJobStatus(StrEnum):
    DRAFT = "draft"
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


_ALLOWED_TRANSITIONS = {
    TrainingJobStatus.DRAFT: {TrainingJobStatus.QUEUED, TrainingJobStatus.BLOCKED},
    TrainingJobStatus.QUEUED: {
        TrainingJobStatus.RUNNING,
        TrainingJobStatus.CANCELLED,
        TrainingJobStatus.BLOCKED,
    },
    TrainingJobStatus.RUNNING: {
        TrainingJobStatus.SUCCEEDED,
        TrainingJobStatus.FAILED,
        TrainingJobStatus.CANCELLED,
    },
    TrainingJobStatus.SUCCEEDED: set(),
    TrainingJobStatus.FAILED: set(),
    TrainingJobStatus.CANCELLED: set(),
    TrainingJobStatus.BLOCKED: set(),
}


class WorkspaceJob(StrictModel):
    job_id: str = Field(min_length=1)
    status: TrainingJobStatus
    dataset_version: str = Field(min_length=1)
    split_version: str = Field(min_length=1)
    language_slices: list[str] = Field(min_length=1)
    base_model: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    model_license: str = Field(min_length=1)
    seed: int
    objective: str = Field(min_length=1)
    adapter_config: dict[str, object] = Field(default_factory=dict)
    training_engine: str = "mlx_lm"
    mlx_lm_version: str = ""
    training_command: str = ""
    unified_memory_mb: int = Field(default=0, ge=0)
    failure_reason: str = ""
    artifact_refs: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    def transition(self, next_status: TrainingJobStatus, reason: str = "") -> WorkspaceJob:
        if next_status not in _ALLOWED_TRANSITIONS[self.status]:
            raise ValueError(f"cannot transition {self.status.value} to {next_status.value}")
        return self.model_copy(
            update={"status": next_status, "failure_reason": reason, "updated_at": utc_now()}
        )