"""Reproducibility appendix construction and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

REQUIRED_APPENDIX_FIELDS = (
    "prompts",
    "models",
    "seeds",
    "configs",
    "datasets",
    "commands",
    "environment",
    "checksums",
)


@dataclass(frozen=True)
class ReproducibilityAppendix:
    metadata: dict[str, Any]
    validation_status: str


def build_appendix(metadata: dict[str, Any]) -> ReproducibilityAppendix:
    missing = [field for field in REQUIRED_APPENDIX_FIELDS if not metadata.get(field)]
    return ReproducibilityAppendix(metadata, "blocked" if missing else "verified")
