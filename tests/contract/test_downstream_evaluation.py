from synthsea.training.downstream import DownstreamEvaluator


def test_downstream_evaluation_requires_research_metadata() -> None:
    result = DownstreamEvaluator().evaluate(
        "e1", "run-1", "tier_c_synthsea", "fixture", "singlish", 0.5
    )
    assert result.dataset_tier == "tier_c_synthsea"
    assert result.checkpoint_ref == "fixture://run-1"
    assert result.language_profile_id == "singlish"
