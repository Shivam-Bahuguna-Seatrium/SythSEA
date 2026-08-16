"""Artifact lineage projections safe for the local workbench."""

from __future__ import annotations

from synthsea.api.schemas.workbench import WorkspaceArtifactResponse
from synthsea.config.schemas import AccessClass


def artifact_lineage(artifact_id: str) -> WorkspaceArtifactResponse:
    access_class = AccessClass.RESTRICTED if "restricted" in artifact_id else AccessClass.PUBLIC
    return WorkspaceArtifactResponse(
        artifact_id=artifact_id,
        access_class=access_class,
        validation_status="restricted" if access_class is AccessClass.RESTRICTED else "pending",
        source_refs=["manifest:unresolved"],
        dependent_refs=[],
        limitations=["Lineage projection uses registered artifact metadata only."],
    )