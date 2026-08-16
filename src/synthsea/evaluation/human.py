"""Human-review aggregation."""

from dataclasses import dataclass

from synthsea.review.annotation import ReviewRecord


@dataclass(frozen=True)
class HumanSummary:
    sample_count: int
    reviewer_roles: list[str]
    decisions: dict[str, int]
    disagreement_count: int


def summarize_reviews(reviews: list[ReviewRecord]) -> HumanSummary:
    decisions: dict[str, int] = {}
    for review in reviews:
        decisions[review.decision] = decisions.get(review.decision, 0) + 1
    by_record: dict[str, set[str]] = {}
    for review in reviews:
        by_record.setdefault(review.record_id, set()).add(review.decision)
    return HumanSummary(
        sample_count=len(reviews),
        reviewer_roles=sorted({review.reviewer_role for review in reviews}),
        decisions=decisions,
        disagreement_count=sum(len(values) > 1 for values in by_record.values()),
    )
