"""MLX-LM job endpoints."""

from fastapi import APIRouter, BackgroundTasks, Depends

from synthsea.api.dependencies import job_store
from synthsea.api.schemas.workbench import FineTuningJobRequest, FineTuningJobResponse
from synthsea.workspace.jobs import WorkspaceJobStore, job_response
from synthsea.workspace.mlx_training import MlxTrainingRunner

router = APIRouter(prefix="/api/training", tags=["training"])


@router.post("/jobs", response_model=FineTuningJobResponse, status_code=202)
def create_training_job(
    request: FineTuningJobRequest,
    background_tasks: BackgroundTasks,
    store: WorkspaceJobStore = Depends(job_store),  # noqa: B008
) -> FineTuningJobResponse:
    job = store.create(request)
    if job.status.value == "queued":
        background_tasks.add_task(MlxTrainingRunner(store).run, job.job_id)
    return job_response(job)


@router.get("/jobs", response_model=list[FineTuningJobResponse])
def list_training_jobs(
    store: WorkspaceJobStore = Depends(job_store),  # noqa: B008
) -> list[FineTuningJobResponse]:
    """List locally persisted fine-tuning job history, newest first."""

    return [job_response(job) for job in store.list()]


@router.get("/jobs/{job_id}", response_model=FineTuningJobResponse)
def get_training_job(
    job_id: str,
    background_tasks: BackgroundTasks,
    store: WorkspaceJobStore = Depends(job_store),  # noqa: B008
) -> FineTuningJobResponse:
    job = store.get(job_id)
    if job.status.value == "queued":
        background_tasks.add_task(MlxTrainingRunner(store).run, job.job_id)
    return job_response(job)


@router.delete("/jobs/{job_id}", response_model=FineTuningJobResponse, status_code=202)
def cancel_training_job(
    job_id: str, store: WorkspaceJobStore = Depends(job_store)  # noqa: B008
) -> FineTuningJobResponse:
    return job_response(store.cancel(job_id))