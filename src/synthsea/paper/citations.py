"""Bibliography validation and BibTeX rendering."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BibliographyEntry:
    citation_key: str
    title: str
    authors: tuple[str, ...]
    year: int
    venue: str
    identifier: str
    source_reference: str
    in_text_use_count: int = 0
    validation_status: str = "verified"


def validate_bibliography(entries: list[BibliographyEntry]) -> list[str]:
    issues: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if entry.citation_key in seen:
            issues.append(f"duplicate:{entry.citation_key}")
        seen.add(entry.citation_key)
        if not entry.title or not entry.authors or not entry.identifier:
            issues.append(f"incomplete:{entry.citation_key}")
        if entry.in_text_use_count == 0:
            issues.append(f"unused:{entry.citation_key}")
    return issues


def render_bibtex(entries: list[BibliographyEntry]) -> str:
    blocks = []
    for entry in entries:
        authors = " and ".join(entry.authors)
        blocks.append(
            "@article{" + entry.citation_key + ",\n"
            f"  author = {{{authors}}},\n"
            f"  title = {{{entry.title}}},\n"
            f"  journal = {{{entry.venue}}},\n"
            f"  year = {{{entry.year}}},\n"
            f"  doi = {{{entry.identifier}}}\n"
            "}"
        )
    return "\n\n".join(blocks) + ("\n" if blocks else "")
