from synthsea.generation.adapters import DeterministicAdapter
from synthsea.workspace.generation import GenerationWorkspaceService


def test_generation_run_persists_local_methodology_artifact(tmp_path) -> None:
    result = GenerationWorkspaceService(tmp_path, DeterministicAdapter()).run(
        topic="Singapore workplace communication",
        language_profile_id="singlish",
        prompt_count=2,
        seed=13,
        model_version="gpt-oss:20b",
    )

    assert result.model_version == "gpt-oss:20b"
    assert result.record_count == 2
    assert "instruction_generation" in result.stages
    assert (tmp_path / "generation" / f"{result.run_id}.json").is_file()
    assert (tmp_path / "generation" / f"{result.run_id}-data" / "README.md").is_file()
    saved = (tmp_path / "generation" / f"{result.run_id}.json").read_text()
    assert "workplace pragmatics" in saved
    assert "cultural explanation" in saved


def test_generation_audit_requires_downstream_benchmarks(tmp_path) -> None:
    service = GenerationWorkspaceService(tmp_path, DeterministicAdapter())
    result = service.run(
        topic="Singapore workplace communication",
        language_profile_id="singlish",
        prompt_count=2,
        seed=13,
        model_version="gpt-oss:20b",
    )

    audited = service.evaluate(result.run_id)

    assert audited.evaluation_status == "automatic_data_audit_complete"
    assert audited.quality_report["downstream_benchmark"] == "required"