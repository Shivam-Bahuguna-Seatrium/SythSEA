"""Dataset-intake endpoint."""

from fastapi import APIRouter

from synthsea.api.schemas.workbench import DatasetIntakeRequest, DatasetIntakeResponse
from synthsea.workspace.intake import create_intake

router = APIRouter(prefix="/api/datasets", tags=["datasets"])


@router.post("/intakes", response_model=DatasetIntakeResponse, status_code=201)
def create_dataset_intake(request: DatasetIntakeRequest) -> DatasetIntakeResponse:
    return create_intake(request)