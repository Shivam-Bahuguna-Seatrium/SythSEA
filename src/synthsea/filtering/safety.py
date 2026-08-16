"""Safety screening interface for generated records."""

from __future__ import annotations

from synthsea.data.models import DataRecord
from synthsea.filtering.quality import QualityDecision


def safety_check(record: DataRecord) -> QualityDecision:
    text = f"{record.instruction} {record.response}".lower()
    blocked_terms = ("private key", "password dump")
    reasons = ["unsafe_content"] if any(term in text for term in blocked_terms) else []
    return QualityDecision(passed=not reasons, reason_codes=reasons)
