"""Evidence manifest verification and source immutability."""

from __future__ import annotations

import hashlib
from pathlib import Path

from synthsea.paper.models import EvidenceManifest, EvidenceStatus


def verify_manifest(manifest: EvidenceManifest) -> EvidenceManifest:
    if not manifest.artifact_refs or not manifest.checksums:
        return manifest.model_copy(update={"verification_status": EvidenceStatus.MISSING})
    if not set(manifest.artifact_refs).issubset(manifest.checksums):
        return manifest.model_copy(update={"verification_status": EvidenceStatus.INCONSISTENT})
    return manifest.model_copy(update={"verification_status": EvidenceStatus.VERIFIED})


def snapshot_checksums(paths: list[Path]) -> dict[str, str]:
    return {str(path): _checksum(path) for path in paths}


def verify_unchanged(snapshot: dict[str, str]) -> bool:
    return all(_checksum(Path(path)) == checksum for path, checksum in snapshot.items())


def _checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
