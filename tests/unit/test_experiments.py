from synthsea.config.schemas import AccessClass, ProvenanceRef
from synthsea.data.models import DataRecord
from synthsea.experiments.baselines import DatasetTier
from synthsea.experiments.config import ExperimentConfig
from synthsea.experiments.registry import fingerprint
from synthsea.experiments.runner import ExperimentRunner


def make_record() -> DataRecord:
    return DataRecord(
        record_id="r1",
        dataset_id=None,
        record_version="v1",
        instruction="Say hello",
        response="hello",
        language_profile_id="singlish",
        task_category="fixture",
        source_type="source_independent",
        access_class=AccessClass.PUBLIC,
        provenance_ref=ProvenanceRef(
            source_type="source_independent", source_id="r1", transformation="fixture"
        ),
    )


def config() -> ExperimentConfig:
    return ExperimentConfig(
        experiment_id="exp-1",
        condition_id="tier_c_synthsea",
        language_profiles=["singlish"],
        dataset_versions=["fixture:v1"],
        seeds=[13],
        metrics=["quality_pass_rate"],
    )


def test_experiment_fingerprint_is_stable_and_tiers_are_distinct() -> None:
    assert fingerprint(config()).run_id == fingerprint(config()).run_id
    assert DatasetTier.HUMAN_SEED != DatasetTier.SYNTHSEA


def test_experiment_runner_completes_fixture() -> None:
    result = ExperimentRunner().run(config(), [make_record()])
    assert result.status.value == "completed"
    assert result.records[0].record_id == "r1"
