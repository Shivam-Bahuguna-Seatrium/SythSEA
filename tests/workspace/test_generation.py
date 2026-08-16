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