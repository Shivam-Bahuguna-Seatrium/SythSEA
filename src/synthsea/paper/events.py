"""Paper-package run metadata and append-only events."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import Field

from synthsea.config.schemas import StrictModel, utc_now


class PaperRunEvent(StrictModel):
    package_id: str = Field(min_length=1)
    source_manifest: str = Field(min_length=1)
    venue_profile: str = Field(min_length=1)
    stage: str = Field(min_length=1)
    message: str = Field(min_length=1)
    timestamp: str = Field(default_factory=lambda: utc_now().isoformat())


def append_event(path: Path, event: PaperRunEvent) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event.model_dump(mode="json"), sort_keys=True) + "\n")
