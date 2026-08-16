"""Reviewer validation for language profiles."""

from __future__ import annotations

from datetime import datetime

from synthsea.profiles.models import LanguageProfile


def approve_profile(
    profile: LanguageProfile,
    reviewer_role: str,
    validated_at: datetime,
) -> LanguageProfile:
    if not reviewer_role.strip():
        raise ValueError("reviewer_role is required")
    return profile.model_copy(
        update={
            "validation_status": "approved",
            "validated_by_role": reviewer_role,
            "validated_at": validated_at,
        }
    )
