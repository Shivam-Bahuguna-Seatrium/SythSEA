from synthsea.config.schemas import AccessClass, ProvenanceRef
from synthsea.data.models import DataRecord
from synthsea.filtering.quality import validate_record


def test_quality_validator_rejects_empty_content() -> None:
    record = DataRecord(
        record_id="r1",
        dataset_id=None,
        record_version="v1",
        instruction="Say hello",
        response="valid response",
        language_profile_id="singlish",
        task_category="fixture",
        source_type="source_independent",
        access_class=AccessClass.PUBLIC,
        provenance_ref=ProvenanceRef(
            source_type="source_independent",
            source_id="r1",
            transformation="fixture",
        ),
    )
    decision = validate_record(record)
    assert decision.passed is True
    assert decision.reason_codes == []
