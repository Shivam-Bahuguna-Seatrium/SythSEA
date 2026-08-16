from pathlib import Path

from synthsea.config.contracts import validate_contract
from synthsea.experiments.config import ExperimentConfig


def test_experiment_config_contract() -> None:
    config = ExperimentConfig(
        experiment_id="e1",
        condition_id="tier_b",
        language_profiles=["singlish"],
        dataset_versions=["fixture:v1"],
        seeds=[13],
        metrics=["quality_pass_rate"],
    )
    validate_contract(
        config.model_dump(mode="json", exclude_none=True),
        Path("specs/001-multilingual-instruction-pipeline/contracts/experiment-config.schema.json"),
    )
