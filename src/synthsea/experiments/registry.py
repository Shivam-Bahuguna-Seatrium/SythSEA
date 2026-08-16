"""Stable experiment fingerprints and run records."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from synthsea.experiments.config import ExperimentConfig


@dataclass(frozen=True)
class RunFingerprint:
    run_id: str
    canonical_config: str


@dataclass(frozen=True)
class SplitManifest:
    train_ids: tuple[str, ...]
    validation_ids: tuple[str, ...]
    test_ids: tuple[str, ...]


class RunRegistry:
    def __init__(self) -> None:
        self._runs: dict[str, RunFingerprint] = {}

    def register(self, config: ExperimentConfig) -> RunFingerprint:
        item = fingerprint(config)
        self._runs[item.run_id] = item
        return item

    def get(self, run_id: str) -> RunFingerprint | None:
        return self._runs.get(run_id)


def manifest_fingerprint(manifest: dict[str, Any]) -> str:
    canonical = json.dumps(manifest, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]


def fingerprint(config: ExperimentConfig) -> RunFingerprint:
    canonical = json.dumps(config.model_dump(mode="json"), sort_keys=True)
    run_id = hashlib.sha256(canonical.encode()).hexdigest()[:16]
    return RunFingerprint(run_id=run_id, canonical_config=canonical)
