from synthsea.experiments.ablations import ablation_condition, full_pipeline_condition


def test_baseline_and_ablation_have_distinct_conditions() -> None:
    assert full_pipeline_condition().condition_id != ablation_condition("critic").condition_id
