"""Downstream instruction adaptation records."""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import Field

from synthsea.config.schemas import StrictModel


class DownstreamEvaluation(StrictModel):
    evaluation_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    dataset_tier: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    adaptation_config: dict[str, str]
    checkpoint_ref: str = Field(min_length=1)
    language_profile_id: str = Field(min_length=1)
    metric_name: str = Field(min_length=1)
    value: float
    uncertainty: dict[str, float] = {}
    sample_definition: str = Field(min_length=1)
    artifact_ref: str = Field(min_length=1)


@dataclass(frozen=True)
class DownstreamEvaluator:
    def evaluate(
        self,
        evaluation_id: str,
        run_id: str,
        dataset_tier: str,
        model_version: str,
        language_profile_id: str,
        value: float,
    ) -> DownstreamEvaluation:
        return DownstreamEvaluation(
            evaluation_id=evaluation_id,
            run_id=run_id,
            dataset_tier=dataset_tier,
            model_version=model_version,
            adaptation_config={"mode": "cpu_fixture"},
            checkpoint_ref=f"fixture://{run_id}",
            language_profile_id=language_profile_id,
            metric_name="downstream_utility",
            value=value,
            sample_definition="fixture evaluation sample",
            artifact_ref=f"artifact://{evaluation_id}",
        )
