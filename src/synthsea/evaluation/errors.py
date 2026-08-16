"""Auditable error categories."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorFinding:
    record_id: str
    category: str
    detail: str


def categorize(record_id: str, category: str, detail: str) -> ErrorFinding:
    return ErrorFinding(record_id, category, detail)
