"""Source registry and literature-matrix helpers."""

from __future__ import annotations

from pathlib import Path

from synthsea.research.io import load_artifact, write_artifact
from synthsea.research.models import SourceRecord, SourceStatus


def load_sources(source_root: Path) -> list[SourceRecord]:
    if not source_root.exists():
        return []
    records: list[SourceRecord] = []
    for path in sorted(source_root.iterdir()):
        if path.suffix.lower() not in {".json", ".yaml", ".yml"}:
            continue
        value = load_artifact(path)
        raw_records = value.get("sources", [value])
        if not isinstance(raw_records, list):
            raise ValueError(f"sources must be a list: {path}")
        records.extend(SourceRecord.model_validate(raw) for raw in raw_records)
    return records


def source_key(source: SourceRecord) -> str:
    if source.doi_or_url.lower() not in {"unavailable", "unknown", "pending"}:
        return source.doi_or_url.strip().lower()
    return "|".join(
        (source.title.strip().lower(), str(source.year or ""), source.venue.strip().lower())
    )


def find_duplicate_sources(sources: list[SourceRecord]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for source in sources:
        key = source_key(source)
        if key in seen:
            duplicates.append(source.source_id)
        seen.add(key)
    return duplicates


def verified_sources(sources: list[SourceRecord]) -> list[SourceRecord]:
    return [source for source in sources if source.verification_status is SourceStatus.VERIFIED]


def literature_matrix(sources: list[SourceRecord]) -> list[dict[str, object]]:
    return [source.model_dump(mode="json") for source in sources]


def write_literature_matrix(path: Path, sources: list[SourceRecord]) -> None:
    write_artifact(path, {"sources": literature_matrix(sources)})