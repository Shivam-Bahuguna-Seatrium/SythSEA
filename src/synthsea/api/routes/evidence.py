"""Lineage and readiness endpoints."""

from fastapi import APIRouter

from synthsea.api.dependencies import workspace_root
from synthsea.api.schemas.workbench import WorkspaceArtifactResponse
from synthsea.workspace.lineage import artifact_lineage
from synthsea.workspace.readiness import readiness

router = APIRouter(prefix="/api", tags=["evidence"])


@router.get("/artifacts/{artifact_id}/lineage", response_model=WorkspaceArtifactResponse)
def get_lineage(artifact_id: str) -> WorkspaceArtifactResponse:
    return artifact_lineage(artifact_id)


@router.get("/readiness")
def get_readiness() -> dict[str, object]:
    status, items = readiness(workspace_root().parent)
    return {"releaseStatus": status, "items": [item.model_dump(mode="json") for item in items]}