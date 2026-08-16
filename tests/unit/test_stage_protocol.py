from synthsea.agents.base import DeterministicStage, StageContext


def test_stage_records_typed_result() -> None:
    stage = DeterministicStage(name="profile", version="v1")
    result = stage.run([{"record_id": "r1"}], StageContext(run_id="run-1"))
    assert result.stage_name == "profile"
    assert result.decision == "pass"
    assert result.output_records == [{"record_id": "r1"}]
