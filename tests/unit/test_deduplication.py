from synthsea.config.schemas import AccessClass, ProvenanceRef
from synthsea.data.models import DataRecord
from synthsea.filtering.deduplication import find_duplicates


def record(record_id: str, text: str) -> DataRecord:
    return DataRecord(
        record_id=record_id,
        dataset_id=None,
        record_version="v1",
        instruction="Say hello",
        response=text,
        language_profile_id="singlish",
        task_category="fixture",
        source_type="source_independent",
        access_class=AccessClass.PUBLIC,
        provenance_ref=ProvenanceRef(
            source_type="source_independent",
            source_id=record_id,
            transformation="fixture",
        ),
    )


def test_exact_duplicates_are_grouped_deterministically() -> None:
    groups = find_duplicates([record("r1", " Hello "), record("r2", "hello")])
    assert len(groups) == 1
    assert groups[0].record_ids == ["r1", "r2"]
    assert groups[0].selected_record_id == "r1"
