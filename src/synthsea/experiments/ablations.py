"""Baseline and ablation condition definitions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentCondition:
    condition_id: str
    tier: str
    changed_variables: tuple[str, ...]
    enabled_stages: tuple[str, ...]


def baseline_condition() -> ExperimentCondition:
    return ExperimentCondition("tier_b_single_agent", "tier_b_single_agent", (), ("generation",))


def full_pipeline_condition() -> ExperimentCondition:
    return ExperimentCondition("tier_c_synthsea", "tier_c_synthsea", (), ("all",))


def ablation_condition(disabled_stage: str) -> ExperimentCondition:
    return ExperimentCondition(
        condition_id=f"ablation_without_{disabled_stage}",
        tier="tier_c_synthsea",
        changed_variables=(f"disabled_stage:{disabled_stage}",),
        enabled_stages=(f"all_except:{disabled_stage}",),
    )
