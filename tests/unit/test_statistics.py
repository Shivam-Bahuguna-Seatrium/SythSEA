from synthsea.evaluation.statistics import bootstrap_mean


def test_statistics_are_deterministic() -> None:
    assert bootstrap_mean([1.0, 2.0]).estimate == bootstrap_mean([1.0, 2.0]).estimate
