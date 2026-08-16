"""Deterministic experiment execution over prepared records."""

from __future__ import annotations

from dataclasses import dataclass

from synthsea.config.schemas import RunStatus
from synthsea.data.models import DataRecord
from synthsea.experiments.config import ExperimentConfig
from synthsea.experiments.registry import RunFingerprint, fingerprint


@dataclass(frozen=True)
class ExperimentResult:
    fingerprint: RunFingerprint
    status: RunStatus
    records: list[DataRecord]


class ExperimentRunner:
    def run(self, config: ExperimentConfig, records: list[DataRecord]) -> ExperimentResult:
        return ExperimentResult(
            fingerprint=fingerprint(config),
            status=RunStatus.COMPLETED,
            records=records,
        )
