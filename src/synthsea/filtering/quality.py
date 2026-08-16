"""Deterministic content-quality checks."""

from __future__ import annotations

from dataclasses import dataclass

from synthsea.data.models import DataRecord


@dataclass(frozen=True)
class QualityDecision:
    passed: bool
    reason_codes: list[str]


def validate_record(record: DataRecord) -> QualityDecision:
    reasons: list[str] = []
    if not record.instruction.strip() or not record.response.strip():
        reasons.append("empty_content")
    if not record.language_profile_id.strip():
        reasons.append("missing_language_profile")
    if not record.task_category.strip():
        reasons.append("missing_task_category")
    return QualityDecision(passed=not reasons, reason_codes=reasons)
