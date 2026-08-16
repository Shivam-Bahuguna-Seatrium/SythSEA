from pathlib import Path

import yaml

from synthsea.config.contracts import validate_contract
from synthsea.experiments.config import ExperimentConfig
from synthsea.generation.adapters import DeterministicAdapter
from synthsea.generation.runner import GenerationConfig, GenerationRunner


def test_cpu_quickstart_path() -> None:
    languages = yaml.safe_load(Path("configs/languages.yaml").read_text())
    assert len(languages["profiles"]) == 4
    result = GenerationRunner(DeterministicAdapter()).run(
        ["Explain hello"],
        GenerationConfig("smoke", "singlish", "tier_b_single_agent", 13),
    )
    assert len(result.records) == 1
    config = ExperimentConfig(
        experiment_id="smoke",
        condition_id="tier_b_single_agent",
        language_profiles=["singlish"],
        dataset_versions=["fixture:v1"],
        seeds=[13],
        metrics=["quality_pass_rate"],
    )
    validate_contract(
        config.model_dump(mode="json", exclude_none=True),
        Path("specs/001-multilingual-instruction-pipeline/contracts/experiment-config.schema.json"),
    )