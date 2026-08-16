"""Leakage and contamination checks."""

from dataclasses import dataclass

from synthsea.data.models import DataRecord


@dataclass(frozen=True)
class LeakageFinding:
    record_id: str
    category: str
    detail: str


def find_prompt_overlap(records: list[DataRecord]) -> list[LeakageFinding]:
    seen: dict[str, str] = {}
    findings: list[LeakageFinding] = []
    for record in records:
        key = record.instruction.strip().lower()
        if key in seen:
            findings.append(LeakageFinding(record.record_id, "prompt_overlap", seen[key]))
        else:
            seen[key] = record.record_id
    return findings
