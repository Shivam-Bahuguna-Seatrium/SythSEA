from synthsea.experiments.baselines import DatasetTier


def test_all_dataset_tiers_are_distinct() -> None:
    assert len(set(DatasetTier)) == 4
