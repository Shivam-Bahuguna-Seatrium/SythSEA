from synthsea.evaluation.automatic import quality_pass_rate
from tests.unit.test_experiments import make_record


def test_automatic_metric_has_language_slice() -> None:
    assert quality_pass_rate([make_record()])[0].language_profile_id == "singlish"
