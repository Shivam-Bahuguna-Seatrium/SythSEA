"""Shared paper-package entities and statuses."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from synthsea.config.schemas import AccessClass, StrictModel, utc_now


class VenueFormat(StrEnum):
    SPRINGER_LNCS = "springer_lncs"
    SPRINGER_NATURE = "springer_nature"
    VENUE_SPECIFIC = "venue_specific"
    NON_SPRINGER = "non_springer"
    MANUAL_REVIEW = "manual_review"


class VenueStatus(StrEnum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    CONFLICTED = "conflicted"
    SUPERSEDED = "superseded"


class EvidenceStatus(StrEnum):
    VERIFIED = "verified"
    MISSING = "missing"
    INCONSISTENT = "inconsistent"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"


class ClaimStatus(StrEnum):
    VERIFIED = "verified"
    MISSING = "missing"
    UNSUPPORTED = "unsupported"
    RESTRICTED = "restricted"
    EXCLUDED = "excluded"
    BLOCKED = "blocked"


class StrictPaperModel(StrictModel):
    """Paper models use strict extra-field rejection and assignment validation."""


class VenueProfile(StrictPaperModel):
    venue_id: str = Field(min_length=1)
    venue_name: str = Field(min_length=1)
    requirements_source: str = Field(min_length=1)
    accessed_at: str = Field(min_length=1)
    format_family: VenueFormat
    template_reference: str = Field(min_length=1)
    page_limit: int = Field(ge=1)
    author_mode: str = Field(min_length=1)
    required_sections: list[str] = Field(min_length=1)
    reference_style: str = Field(min_length=1)
    anonymization_rule: str = Field(min_length=1)
    version: str = Field(min_length=1)
    status: VenueStatus = VenueStatus.DRAFT


class EvidenceManifest(StrictPaperModel):
    manifest_id: str = Field(min_length=1)
    manifest_version: str = Field(min_length=1)
    source_root: str | None = None
    artifact_refs: list[str] = Field(min_length=1)
    experiment_ids: list[str] = Field(default_factory=list)
    language_profiles: list[str] = Field(min_length=1)
    conditions: list[str] = Field(default_factory=list)
    checksums: dict[str, str]
    access_summary: dict[str, int]
    limitations: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    verification_status: EvidenceStatus = EvidenceStatus.VERIFIED


class PaperClaim(StrictPaperModel):
    claim_id: str = Field(min_length=1)
    claim_text: str = Field(min_length=1)
    claim_type: str = Field(min_length=1)
    status: ClaimStatus
    evidence_refs: list[str] = Field(default_factory=list)
    citation_refs: list[str] = Field(default_factory=list)
    language_scope: list[str] = Field(default_factory=list)
    condition_scope: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    review_notes: str = ""

    def can_render_as_result(self) -> bool:
        return self.status is ClaimStatus.VERIFIED and bool(
            self.evidence_refs or self.citation_refs
        )


class PaperArtifact(StrictPaperModel):
    artifact_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    caption: str = ""
    source_refs: list[str] = Field(min_length=1)
    transformation: str = Field(min_length=1)
    language_slices: list[str] = Field(default_factory=list)
    condition_ids: list[str] = Field(default_factory=list)
    version: str = Field(min_length=1)
    access_class: AccessClass
    output_path: str = Field(min_length=1)
    validation_status: str = "pending"
