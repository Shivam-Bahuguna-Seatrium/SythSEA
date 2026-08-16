"""Validated experiment configuration models."""

from __future__ import annotations

from pydantic import Field

from synthsea.agents.code_switching import CodeSwitchPolicy
from synthsea.config.schemas import StrictModel


class ExperimentConfig(StrictModel):
    experiment_id: str = Field(min_length=1)
    condition_id: str = Field(min_length=1)
    language_profiles: list[str] = Field(min_length=1)
    dataset_versions: list[str] = Field(min_length=1)
    seeds: list[int] = Field(min_length=1)
    models: list[str] = Field(default_factory=list)
    prompts: list[str] = Field(default_factory=list)
    code_switching: CodeSwitchPolicy = Field(default_factory=CodeSwitchPolicy)
    metrics: list[str] = Field(min_length=1)
    human_review: bool = False
    data_efficiency_size: int | None = Field(default=None, ge=1)
