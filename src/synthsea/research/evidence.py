"""Evidence registration, checksum verification, and public projections."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from synthsea.research.io import load_artifact, write_artifact
from synthsea.research.models import EvidenceRecord, EvidenceState


def load_evidence_records(path: Path) -> list[EvidenceRecord]:
    value = load_artifact(path)
    raw_records = value.get("records", value.get("evidence", []))
    if not isinstance(raw_records, list):
        raise ValueError(f"evidence records must be a list: {path}")
    return [EvidenceRecord.model_validate(raw) for raw in raw_records]


def checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_record(record: EvidenceRecord, source_root: Path) -> EvidenceRecord:
    artifact = source_root / record.artifact_path
    if record.status is EvidenceState.FIXTURE:
        if not artifact.is_file():
            return record.model_copy(update={"status": EvidenceState.MISSING})
        return record.model_copy(update={"status": EvidenceState.FIXTURE})
    if record.access_class.value in {"private", "restricted"}:
        return record.model_copy(update={"status": EvidenceState.RESTRICTED})
    if not artifact.is_file():
        return record.model_copy(update={"status": EvidenceState.MISSING})
    if checksum(artifact) != record.checksum:
        return record.model_copy(update={"status": EvidenceState.STALE})
    if not record.provenance_refs:
        return record.model_copy(update={"status": EvidenceState.UNSUPPORTED})
    return record.model_copy(update={"status": EvidenceState.VERIFIED})


def verify_records(records: list[EvidenceRecord], source_root: Path) -> list[EvidenceRecord]:
    return [verify_record(record, source_root) for record in records]


def coverage(records: list[EvidenceRecord]) -> dict[str, int]:
    result: dict[str, int] = {}
    for record in records:
        result[record.status.value] = result.get(record.status.value, 0) + 1
    return result


def public_records(records: list[EvidenceRecord]) -> tuple[list[EvidenceRecord], list[str]]:
    included: list[EvidenceRecord] = []
    excluded: list[str] = []
    for record in records:
        if record.access_class.value in {"private", "restricted"}:
            excluded.append(record.evidence_id)
        else:
            included.append(record)
    return included, excluded


def write_evidence_report(path: Path, records: list[EvidenceRecord]) -> None:
    write_artifact(path, {"records": [record.model_dump(mode="json") for record in records]})


def evidence_from_matrix(matrix: dict[str, Any]) -> list[EvidenceRecord]:
    raw_records = matrix.get("evidence", [])
    if not isinstance(raw_records, list):
        raise ValueError("matrix evidence must be a list")
    return [EvidenceRecord.model_validate(raw) for raw in raw_records]