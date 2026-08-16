"""Typed request and response contracts for the local workbench."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from synthsea.config.schemas import AccessClass, StrictModel


class DatasetIntakeRequest(StrictModel):
    dataset: dict[str, Any]
    record_source: str = Field(min_length=1)


class DatasetIntakeResponse(StrictModel):
    intake_id: str
    validation_status: Literal["draft", "eligible", "blocked", "restricted", "failed"]
    issues: list[str] = Field(default_factory=list)
    lineage_artifact_id: str | None = None


class FineTuningJobRequest(StrictModel):
    training_engine: Literal["mlx_lm"] = "mlx_lm"
    dataset_version: str = Field(min_length=1)
    split_version: str = Field(min_length=1)
    language_slices: list[str] = Field(min_length=1)
    base_model: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    model_license: str = Field(min_length=1)
    seed: int
    objective: str = Field(min_length=1)
    adapter_config: dict[str, Any] = Field(default_factory=dict)
    unified_memory_mb: int = Field(default=0, ge=0)


class FineTuningJobResponse(StrictModel):
    job_id: str
    status: Literal["draft", "queued", "running", "succeeded", "failed", "cancelled", "blocked"]
    training_engine: Literal["mlx_lm"] = "mlx_lm"
    dataset_version: str
    model_version: str
    language_slices: list[str]
    failure_reason: str = ""
    artifact_refs: list[str] = Field(default_factory=list)
    mlx_lm_version: str = ""
    training_command: str = ""
    unified_memory_mb: int = 0


class ChatConversationRequest(StrictModel):
    model_version: str = Field(min_length=1)
    access_class: AccessClass
    temperature: float = Field(default=0.2, ge=0, le=2)
    seed: int = 13


class ChatConversationResponse(StrictModel):
    conversation_id: str
    model_version: str
    status: Literal["active", "unavailable", "blocked", "archived"]
    exploratory: Literal[True] = True


class ChatMessageRequest(StrictModel):
    content: str = Field(min_length=1)


class ChatMessageResponse(StrictModel):
    message_id: str
    role: Literal["user", "assistant"]
    content: str
    model_version: str
    exploratory: Literal[True] = True
    input_tokens: int = 0
    output_tokens: int = 0


class LocalModelResponse(StrictModel):
    model_version: str
    available: bool
    local_only: Literal[True] = True
    unavailable_reason: str = ""


class WorkspaceArtifactResponse(StrictModel):
    artifact_id: str
    access_class: AccessClass
    validation_status: str
    source_refs: list[str] = Field(default_factory=list)
    dependent_refs: list[str] = Field(default_factory=list)
    checksum: str = ""
    language_slices: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class ReadinessItemResponse(StrictModel):
    item_id: str
    category: str
    severity: Literal["blocking", "warning", "info"]
    status: str
    message: str
    artifact_refs: list[str] = Field(default_factory=list)
    language_slices: list[str] = Field(default_factory=list)
    resolution_action: str = ""