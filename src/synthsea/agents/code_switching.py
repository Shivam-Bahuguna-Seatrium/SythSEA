"""Controlled code-switching conditions."""

from __future__ import annotations

from pydantic import Field, model_validator

from synthsea.agents.base import DeterministicStage
from synthsea.config.schemas import StrictModel


class CodeSwitchPolicy(StrictModel):
    enabled: bool = False
    condition: str = "monolingual_control"
    direction: str | None = None
    target_proportion: float = Field(default=0, ge=0, le=1)
    intent: str | None = None

    @model_validator(mode="after")
    def validate_enabled_policy(self) -> CodeSwitchPolicy:
        if self.enabled and (not self.direction or not self.intent):
            raise ValueError("enabled code-switching requires direction and intent")
        return self


class CodeSwitchingStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="code_switching", version="v1")
