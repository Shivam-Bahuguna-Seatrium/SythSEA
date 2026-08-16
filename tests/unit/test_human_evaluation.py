from synthsea.evaluation.human import summarize_reviews
from synthsea.review.annotation import review_record


def test_human_evaluation_counts_reviewers() -> None:
    summary = summarize_reviews([review_record("r1", "quality", "reviewer", "pass", {})])
    assert summary.sample_count == 1
    assert summary.reviewer_roles == ["reviewer"]
