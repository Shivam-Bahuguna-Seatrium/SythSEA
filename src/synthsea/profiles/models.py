"""Language profile entities and eligibility rules."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from synthsea.config.schemas import StrictModel


class LanguageProfile(StrictModel):
    profile_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    language_or_variety: str = Field(min_length=1)
    region: str = Field(min_length=1)
    script_or_orthography: str = Field(min_length=1)
    inclusion_rules: list[str] = Field(min_length=1)
    cultural_context: str = Field(min_length=1)
    code_switching_notes: str = Field(min_length=1)
    resource_limitations: str = Field(min_length=1)
    validation_status: str = "pending_review"
    validated_by_role: str | None = None
    validated_at: datetime | None = None
    profile_version: str = "v1"

    def is_generation_eligible(self) -> bool:
        return self.validation_status == "approved" and self.validated_by_role is not None
