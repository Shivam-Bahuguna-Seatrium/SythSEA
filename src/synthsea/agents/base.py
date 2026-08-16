"""Typed stage protocol for the generation graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from synthsea.config.schemas import Decision, StrictModel


class StageContext(StrictModel):
    run_id: str
    metadata: dict[str, str] = {}


class StageResult(StrictModel):
    stage_name: str
    stage_version: str
    decision: Decision
    input_records: list[dict[str, Any]]
    output_records: list[dict[str, Any]]
    reason_codes: list[str] = []


@dataclass(frozen=True)
class DeterministicStage:
    name: str
    version: str

    def run(self, records: list[dict[str, Any]], context: StageContext) -> StageResult:
        return StageResult(
            stage_name=self.name,
            stage_version=self.version,
            decision=Decision.PASS,
            input_records=records,
            output_records=records,
        )


@dataclass
class StageGraph:
    stages: list[DeterministicStage] = field(default_factory=list)

    def run(self, records: list[dict[str, Any]], context: StageContext) -> list[StageResult]:
        results: list[StageResult] = []
        current = records
        for stage in self.stages:
            result = stage.run(current, context)
            results.append(result)
            current = result.output_records
        return results
