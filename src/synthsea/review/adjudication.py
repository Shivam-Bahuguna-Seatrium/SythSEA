"""Append-only review disagreement and adjudication."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from synthsea.review.annotation import ReviewRecord


@dataclass(frozen=True)
class AdjudicationOutcome:
    adjudication_id: str
    record_id: str
    source_review_ids: list[str]
    reviewer_role: str
    decision: str


def adjudicate(
    reviews: list[ReviewRecord], reviewer_role: str, decision: str
) -> AdjudicationOutcome:
    if not reviews:
        raise ValueError("at least one review is required")
    record_ids = {review.record_id for review in reviews}
    if len(record_ids) != 1:
        raise ValueError("reviews must target one record")
    return AdjudicationOutcome(
        adjudication_id=str(uuid4()),
        record_id=reviews[0].record_id,
        source_review_ids=[review.review_id for review in reviews],
        reviewer_role=reviewer_role,
        decision=decision,
    )
