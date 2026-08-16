"""Exact and normalized near-duplicate grouping."""

from __future__ import annotations

import re
from dataclasses import dataclass

from synthsea.data.models import DataRecord


@dataclass(frozen=True)
class DuplicateGroup:
    record_ids: list[str]
    selected_record_id: str
    comparison_basis: str


def _normalized_text(record: DataRecord) -> str:
    return re.sub(r"\s+", " ", f"{record.instruction} {record.response}".strip().lower())


def find_duplicates(records: list[DataRecord]) -> list[DuplicateGroup]:
    grouped: dict[str, list[str]] = {}
    for record in records:
        grouped.setdefault(_normalized_text(record), []).append(record.record_id)
    return [
        DuplicateGroup(
            record_ids=record_ids,
            selected_record_id=record_ids[0],
            comparison_basis="normalized_instruction_response",
        )
        for record_ids in grouped.values()
        if len(record_ids) > 1
    ]
