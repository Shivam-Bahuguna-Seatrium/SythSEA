"""Versioned human and automated review records."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from pydantic import Field

from synthsea.config.schemas import AccessClass, StrictModel, utc_now


class ReviewRecord(StrictModel):
    review_id: str = Field(default_factory=lambda: str(uuid4()))
    record_id: str
    review_type: str
    rubric_version: str = "v1"
    reviewer_role: str
    decision: str
    ratings: dict[str, int | float | str]
    rationale: str = ""
    reviewer_pseudonym: str
    created_at: datetime = Field(default_factory=utc_now)
    access_class: AccessClass = AccessClass.RESTRICTED


def review_record(
    record_id: str,
    review_type: str,
    reviewer_role: str,
    decision: str,
    ratings: dict[str, int | float | str],
    rationale: str = "",
) -> ReviewRecord:
    return ReviewRecord(
        record_id=record_id,
        review_type=review_type,
        reviewer_role=reviewer_role,
        decision=decision,
        ratings=ratings,
        rationale=rationale,
        reviewer_pseudonym=reviewer_role,
    )
