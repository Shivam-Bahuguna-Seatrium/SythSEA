"""Reproducibility metadata checks for report evidence."""

from __future__ import annotations

from synthsea.research.models import EvidenceRecord

REQUIRED_REPRODUCIBILITY_FIELDS = (
    "command",
    "inputs",
    "outputs",
    "models",
    "prompts",
    "seeds",
    "environment",
    "dataset_versions",
)


def missing_reproducibility_fields(record: EvidenceRecord) -> list[str]:
    missing: list[str] = []
    for field in REQUIRED_REPRODUCIBILITY_FIELDS:
        value = getattr(record, field)
        if not value:
            missing.append(field)
    return missing


def reproducibility_status(records: list[EvidenceRecord]) -> tuple[str, list[str]]:
    if not records:
        return "blocked", ["no_evidence"]
    missing: list[str] = []
    for record in records:
        missing.extend(
            f"{record.evidence_id}:{field}"
            for field in missing_reproducibility_fields(record)
        )
    return ("verified" if not missing else "blocked", missing)