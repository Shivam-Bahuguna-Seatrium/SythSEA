"""Artifact checksums and manifest creation."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from synthsea.config.schemas import AccessClass, ArtifactRef
from synthsea.data.storage import write_json


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_ref(path: Path, kind: str, access_class: AccessClass) -> ArtifactRef:
    return ArtifactRef(
        artifact_id=sha256_file(path)[:16],
        path=str(path),
        kind=kind,
        checksum=sha256_file(path),
        access_class=access_class,
    )


def write_manifest(
    path: Path,
    package_id: str,
    artifacts: list[ArtifactRef],
    access_class: AccessClass,
) -> None:
    write_json(
        path,
        {
            "manifest_version": "0.1.0",
            "package_id": package_id,
            "access_class": access_class.value,
            "created_at": "1970-01-01T00:00:00+00:00",
            "artifacts": [
                artifact.model_dump(mode="json", exclude_none=True) for artifact in artifacts
            ],
            "excluded_artifacts": [],
        },
    )


def write_reproducibility_manifest(path: Path, metadata: dict[str, Any]) -> None:
    required = {
        "inputs",
        "configs",
        "seeds",
        "prompts",
        "models",
        "environment",
        "outputs",
        "validation_status",
    }
    missing = required.difference(metadata)
    if missing:
        raise ValueError(f"reproducibility manifest missing: {', '.join(sorted(missing))}")
    write_json(path, metadata)
