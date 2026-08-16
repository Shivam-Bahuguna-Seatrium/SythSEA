from synthsea.review.adjudication import adjudicate
from synthsea.review.annotation import ReviewRecord, review_record


def test_review_disagreement_is_append_only() -> None:
    first = review_record("r1", "quality", "reviewer_a", "pass", {"quality": 4})
    second = review_record("r1", "quality", "reviewer_b", "fail", {"quality": 2})
    outcome = adjudicate([first, second], "senior_reviewer", "fail")
    assert outcome.decision == "fail"
    assert len(outcome.source_review_ids) == 2
    assert first.decision == "pass"
    assert isinstance(second, ReviewRecord)
