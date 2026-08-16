"""Structured append-only run events."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import Field

from synthsea.config.schemas import StrictModel, utc_now


class RunEvent(StrictModel):
    run_id: str = Field(min_length=1)
    stage: str = Field(min_length=1)
    severity: str = Field(min_length=1)
    message: str = Field(min_length=1)
    metadata: dict[str, str] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: utc_now().isoformat())


class EventLogger:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: RunEvent) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.model_dump(mode="json"), sort_keys=True) + "\n")
