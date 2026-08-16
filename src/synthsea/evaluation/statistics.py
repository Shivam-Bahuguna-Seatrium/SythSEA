"""Deterministic uncertainty summaries."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Uncertainty:
    estimate: float
    lower: float
    upper: float
    method: str


def bootstrap_mean(values: list[float]) -> Uncertainty:
    if not values:
        raise ValueError("values must not be empty")
    estimate = sum(values) / len(values)
    return Uncertainty(estimate, min(values), max(values), "observed_min_max_fixture")
