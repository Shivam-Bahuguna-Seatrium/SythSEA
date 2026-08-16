"""Deterministic manuscript section assembly."""

from __future__ import annotations

from dataclasses import dataclass

REQUIRED_SECTIONS = (
    "title",
    "abstract",
    "keywords",
    "introduction",
    "related_work",
    "methodology",
    "architecture",
    "dataset_design",
    "experiments",
    "results",
    "discussion",
    "limitations",
    "ethics",
    "reproducibility",
    "conclusion",
    "references",
)


@dataclass(frozen=True)
class PaperSection:
    section_type: str
    content: str
    claim_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    required: bool = True
    status: str = "generated"
    version: str = "v1"


def assemble_sections(content: dict[str, str]) -> list[PaperSection]:
    return [
        PaperSection(section, content.get(section, "[MISSING EVIDENCE]"))
        for section in REQUIRED_SECTIONS
    ]


def language_result_section(
    results: dict[str, str], aggregate: str | None = None
) -> PaperSection:
    ordered = ("singlish", "malay", "tamil", "singapore_mandarin")
    lines = [f"{profile}: {results.get(profile, '[MISSING EVIDENCE]')}" for profile in ordered]
    if aggregate is not None:
        lines.append(f"aggregate: {aggregate}")
    return PaperSection("results", "\n".join(lines))
