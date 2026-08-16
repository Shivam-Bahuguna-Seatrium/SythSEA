"""Language-slice rules for research planning and reporting."""

from __future__ import annotations

LANGUAGE_SLICES = (
    "singlish",
    "malay",
    "tamil",
    "singapore_mandarin",
)


def missing_language_slices(slices: list[str] | tuple[str, ...]) -> list[str]:
    declared = set(slices)
    return [language_slice for language_slice in LANGUAGE_SLICES if language_slice not in declared]


def validate_language_slices(slices: list[str] | tuple[str, ...]) -> None:
    unknown = sorted(set(slices).difference(LANGUAGE_SLICES))
    if unknown:
        raise ValueError(f"unknown language slices: {', '.join(unknown)}")


def aggregate_is_complete(slices: list[str] | tuple[str, ...]) -> bool:
    validate_language_slices(slices)
    return not missing_language_slices(slices)