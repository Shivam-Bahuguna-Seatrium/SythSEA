from synthsea.agents.code_switching import CodeSwitchPolicy
from synthsea.generation.adapters import DeterministicAdapter
from synthsea.generation.runner import GenerationConfig, GenerationRunner


def test_generation_runner_produces_traced_fixture_records() -> None:
    config = GenerationConfig(
        run_id="run-1",
        language_profile_id="singlish",
        condition_id="english_mix_10",
        seed=13,
        code_switching=CodeSwitchPolicy(
            enabled=True,
            condition="english_mix_10",
            direction="target_to_english",
            target_proportion=0.1,
            intent="discourse_marker",
        ),
    )
    result = GenerationRunner(DeterministicAdapter()).run(
        ["Explain hello", "Explain goodbye"], config
    )
    assert len(result.records) == 2
    assert all(
        record.provenance_ref.source_type == "source_independent"
        for record in result.records
    )
    assert all(record.switch_condition == "english_mix_10" for record in result.records)
    assert result.failures == []
