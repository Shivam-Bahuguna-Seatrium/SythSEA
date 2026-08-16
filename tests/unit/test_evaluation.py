from pathlib import Path

from synthsea.config.schemas import AccessClass, ProvenanceRef
from synthsea.data.models import DataRecord
from synthsea.evaluation.automatic import quality_pass_rate
from synthsea.evaluation.human import summarize_reviews
from synthsea.evaluation.leakage import find_prompt_overlap
from synthsea.evaluation.statistics import bootstrap_mean
from synthsea.export.reports import write_publication_package
from synthsea.review.annotation import review_record


def record(record_id: str, instruction: str = "hello") -> DataRecord:
    return DataRecord(
        record_id=record_id,
        dataset_id=None,
        record_version="v1",
        instruction=instruction,
        response="response",
        language_profile_id="singlish",
        task_category="fixture",
        source_type="source_independent",
        access_class=AccessClass.PUBLIC,
        provenance_ref=ProvenanceRef(
            source_type="source_independent", source_id=record_id, transformation="fixture"
        ),
    )


def test_evaluation_produces_metrics_human_summary_and_uncertainty(tmp_path: Path) -> None:
    records = [record("r1"), record("r2", "hello")]
    assert quality_pass_rate(records)[0].denominator == 2
    reviews = [
        review_record("r1", "quality", "a", "pass", {"quality": 4}),
        review_record("r1", "quality", "b", "fail", {"quality": 2}),
    ]
    assert summarize_reviews(reviews).disagreement_count == 1
    assert len(find_prompt_overlap(records)) == 1
    assert bootstrap_mean([0.5, 1.0]).estimate == 0.75
    path = tmp_path / "report.json"
    write_publication_package(
        path,
        {"methods": {}, "results": {}, "limitations": [], "provenance": {}, "manifest": {}},
    )
    assert path.is_file()
