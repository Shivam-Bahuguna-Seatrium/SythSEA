from synthsea.config.schemas import AccessClass, ProvenanceRef
from synthsea.data.models import DataRecord
from synthsea.filtering.pipeline import QualityGate


def make_record(record_id: str, response: str) -> DataRecord:
    values = {
            "record_id": record_id,
            "dataset_id": None,
            "record_version": "v1",
            "instruction": "Say hello",
            "language_profile_id": "singlish",
            "task_category": "fixture",
            "source_type": "source_independent",
            "access_class": AccessClass.PUBLIC,
            "provenance_ref": ProvenanceRef(
                source_type="source_independent",
                source_id=record_id,
                transformation="fixture",
            ),
        }
    if response:
        return DataRecord(response=response, **values)
    return DataRecord.model_construct(response=response, **values)


def test_quality_gate_keeps_eligible_records_and_reasons() -> None:
    result = QualityGate().run([make_record("r1", "hello"), make_record("r2", "")])
    assert [record.record_id for record in result.eligible] == ["r1"]
    assert result.rejected[0].record_id == "r2"
    assert result.rejected[0].reason_codes == ["empty_content"]
