import pytest

from synthsea.agents.code_switching import CodeSwitchPolicy


def test_code_switch_policy_requires_labels_when_enabled() -> None:
    policy = CodeSwitchPolicy(
        enabled=True,
        condition="english_mix_10",
        direction="target_to_english",
        target_proportion=0.1,
        intent="discourse_marker",
    )
    assert policy.enabled is True
    assert policy.target_proportion == 0.1


def test_code_switch_policy_rejects_invalid_proportion() -> None:
    with pytest.raises(ValueError):
        CodeSwitchPolicy(
            enabled=True,
            condition="english_mix",
            direction="target_to_english",
            target_proportion=1.2,
            intent="marker",
        )
