"""Access-aware artifact selection for public and restricted exports."""

from __future__ import annotations

from synthsea.config.schemas import AccessClass, ArtifactRef


def public_artifacts(artifacts: list[ArtifactRef]) -> tuple[list[ArtifactRef], list[str]]:
    included = [artifact for artifact in artifacts if artifact.access_class is AccessClass.PUBLIC]
    excluded = [
        artifact.artifact_id
        for artifact in artifacts
        if artifact.access_class is not AccessClass.PUBLIC
    ]
    return included, excluded
