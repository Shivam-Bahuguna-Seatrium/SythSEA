"""Typed research metadata and readiness entities."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field, model_validator

from synthsea.config.schemas import AccessClass, StrictModel, utc_now
from synthsea.research.languages import validate_language_slices


class SourceType(StrEnum):
    ACADEMIC = "academic"
    OFFICIAL_VENUE = "official_venue"
    DATASET = "dataset"
    MODEL = "model"
    TECHNICAL = "technical"


class SourceStatus(StrEnum):
    CANDIDATE = "candidate"
    VERIFIED = "verified"
    UNAVAILABLE = "unavailable"
    CONFLICTED = "conflicted"
    REJECTED = "rejected"


class DossierStatus(StrEnum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    BLOCKED = "blocked"
    APPROVED = "approved"


class EvidenceState(StrEnum):
    VERIFIED = "verified"
    PROVISIONAL = "provisional"
    MISSING = "missing"
    UNSUPPORTED = "unsupported"
    RESTRICTED = "restricted"
    EXCLUDED = "excluded"
    STALE = "stale"
    FAILED = "failed"
    FIXTURE = "fixture"


class RequirementStatus(StrEnum):
    MISSING = "missing"
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETE = "complete"
    BLOCKED = "blocked"
    WAIVED = "waived"


class ClaimEvidenceStatus(StrEnum):
    VERIFIED = "verified"
    MISSING = "missing"
    UNSUPPORTED = "unsupported"
    RESTRICTED = "restricted"
    EXCLUDED = "excluded"
    BLOCKED = "blocked"


class SourceRecord(StrictModel):
    source_id: str = Field(min_length=1)
    source_type: SourceType
    title: str = Field(min_length=1)
    authors: list[str] = Field(default_factory=list)
    year: int | None = Field(default=None, ge=1900, le=2100)
    venue: str = ""
    doi_or_url: str = Field(min_length=1)
    retrieved_at: str = Field(min_length=1)
    contribution: str = ""
    limitation: str = ""
    relevance: str = ""
    verification_status: SourceStatus = SourceStatus.CANDIDATE
    access_class: AccessClass = AccessClass.PUBLIC
    license_or_terms: str = ""


class ResearchQuestion(StrictModel):
    question_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    hypotheses: list[str] = Field(min_length=1)
    language_slices: list[str] = Field(min_length=1)
    claim_ids: list[str] = Field(default_factory=list)
    status: str = "planned"

    @model_validator(mode="after")
    def validate_slices(self) -> ResearchQuestion:
        validate_language_slices(self.language_slices)
        return self


class ResearchDossier(StrictModel):
    dossier_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    title: str = Field(min_length=1)
    target_venue: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=utc_now)
    source_refs: list[str] = Field(default_factory=list)
    research_question_ids: list[str] = Field(min_length=1)
    novelty_summary: str = ""
    unresolved_items: list[str] = Field(default_factory=list)
    status: DossierStatus = DossierStatus.DRAFT


class ExperimentRequirement(StrictModel):
    requirement_id: str = Field(min_length=1)
    question_id: str = Field(min_length=1)
    claim_ids: list[str] = Field(default_factory=list)
    condition_id: str = Field(min_length=1)
    dataset_versions: list[str] = Field(min_length=1)
    language_slices: list[str] = Field(min_length=1)
    metrics: list[str] = Field(min_length=1)
    sample_size: int | None = Field(default=None, ge=1)
    statistical_method: str = Field(min_length=1)
    human_evaluation: str | None = None
    command: str = Field(min_length=1)
    expected_artifacts: list[str] = Field(min_length=1)
    status: RequirementStatus = RequirementStatus.MISSING

    @model_validator(mode="after")
    def validate_slices(self) -> ExperimentRequirement:
        validate_language_slices(self.language_slices)
        return self


class EvidenceRecord(StrictModel):
    evidence_id: str = Field(min_length=1)
    experiment_id: str = Field(min_length=1)
    artifact_path: str = Field(min_length=1)
    artifact_type: str = Field(min_length=1)
    checksum: str = Field(min_length=64, max_length=64)
    language_slice: str = Field(min_length=1)
    condition_id: str = Field(min_length=1)
    access_class: AccessClass
    status: EvidenceState
    provenance_refs: list[str] = Field(min_length=1)
    limitations: list[str] = Field(default_factory=list)
    command: str = ""
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    models: list[str] = Field(default_factory=list)
    prompts: list[str] = Field(default_factory=list)
    seeds: list[int] = Field(default_factory=list)
    environment: dict[str, str] = Field(default_factory=dict)
    dataset_versions: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_slice(self) -> EvidenceRecord:
        validate_language_slices([self.language_slice])
        if self.status is EvidenceState.RESTRICTED and self.access_class is AccessClass.PUBLIC:
            raise ValueError("restricted evidence cannot have public access class")
        return self


class ClaimEvidenceLink(StrictModel):
    claim_id: str = Field(min_length=1)
    claim_text: str = Field(min_length=1)
    claim_type: str = Field(min_length=1)
    evidence_ids: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    language_slices: list[str] = Field(default_factory=list)
    transformation: str = ""
    status: ClaimEvidenceStatus
    review_notes: str = ""

    @model_validator(mode="after")
    def validate_slices(self) -> ClaimEvidenceLink:
        if self.language_slices:
            validate_language_slices(self.language_slices)
        return self


class ReadinessReport(StrictModel):
    package_id: str = Field(min_length=1)
    blocking_issues: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    evidence_coverage: dict[str, int] = Field(default_factory=dict)
    citation_status: str = "blocked"
    reproducibility_status: str = "blocked"
    ethics_status: str = "blocked"
    venue_status: str = "unresolved"
    release_status: str = "blocked"
    generated_at: datetime = Field(default_factory=utc_now)