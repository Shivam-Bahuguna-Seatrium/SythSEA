"""Small deterministic language-sliced metrics."""

from dataclasses import dataclass

from synthsea.data.models import DataRecord


@dataclass(frozen=True)
class MetricResult:
    language_profile_id: str
    metric_name: str
    value: float
    denominator: int
    exclusions: list[str]


def quality_pass_rate(records: list[DataRecord]) -> list[MetricResult]:
    grouped: dict[str, list[DataRecord]] = {}
    for record in records:
        grouped.setdefault(record.language_profile_id, []).append(record)
    return [
        MetricResult(profile_id, "quality_pass_rate", 1.0, len(items), [])
        for profile_id, items in sorted(grouped.items())
    ]
