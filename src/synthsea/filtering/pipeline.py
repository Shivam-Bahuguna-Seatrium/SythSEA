"""Final quality-gate coordination."""

from __future__ import annotations

from dataclasses import dataclass

from synthsea.data.models import DataRecord
from synthsea.filtering.deduplication import find_duplicates
from synthsea.filtering.quality import validate_record
from synthsea.filtering.safety import safety_check


@dataclass(frozen=True)
class RejectedRecord:
    record_id: str
    reason_codes: list[str]


@dataclass(frozen=True)
class QualityGateResult:
    eligible: list[DataRecord]
    rejected: list[RejectedRecord]


class QualityGate:
    def run(self, records: list[DataRecord]) -> QualityGateResult:
        rejected: list[RejectedRecord] = []
        candidates: list[DataRecord] = []
        for record in records:
            decisions = [validate_record(record), safety_check(record)]
            reasons = [reason for decision in decisions for reason in decision.reason_codes]
            if reasons:
                rejected.append(RejectedRecord(record.record_id, reasons))
            else:
                candidates.append(record)

        duplicate_ids = {
            record_id
            for group in find_duplicates(candidates)
            for record_id in group.record_ids[1:]
        }
        for record_id in sorted(duplicate_ids):
            rejected.append(RejectedRecord(record_id, ["duplicate"]))
        eligible = [record for record in candidates if record.record_id not in duplicate_ids]
        return QualityGateResult(eligible=eligible, rejected=rejected)
