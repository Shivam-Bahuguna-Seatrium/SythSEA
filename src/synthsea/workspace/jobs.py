"""File-backed persistence and validation for local MLX-LM jobs."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from synthsea.api.schemas.workbench import FineTuningJobRequest, FineTuningJobResponse
from synthsea.research.languages import validate_language_slices
from synthsea.workspace.models import TrainingJobStatus, WorkspaceJob


class WorkspaceJobStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.jobs_root = root / "jobs"

    def create(self, request: FineTuningJobRequest) -> WorkspaceJob:
        validate_language_slices(request.language_slices)
        if request.dataset_version.startswith("restricted:"):
            status = TrainingJobStatus.BLOCKED
            reason = "restricted dataset requires an approved local training policy"
        elif (
            not request.base_model.startswith("mlx")
            and "mlx-community/" not in request.base_model
        ):
            status = TrainingJobStatus.BLOCKED
            reason = "base model must identify an MLX-compatible model"
        else:
            status = TrainingJobStatus.QUEUED
            reason = ""
        job_id = f"mlx-{uuid4().hex[:12]}"
        command = _mlx_command(request, self.jobs_root / job_id / "adapter")
        job = WorkspaceJob(
            job_id=job_id,
            status=status,
            dataset_version=request.dataset_version,
            split_version=request.split_version,
            language_slices=request.language_slices,
            base_model=request.base_model,
            model_version=request.model_version,
            model_license=request.model_license,
            seed=request.seed,
            objective=request.objective,
            adapter_config=request.adapter_config,
            mlx_lm_version="pending-local-check",
            training_command=command,
            unified_memory_mb=request.unified_memory_mb,
            failure_reason=reason,
        )
        self.save(job)
        return job

    def save(self, job: WorkspaceJob) -> None:
        self.jobs_root.mkdir(parents=True, exist_ok=True)
        path = self.jobs_root / f"{job.job_id}.json"
        path.write_text(json.dumps(job.model_dump(mode="json"), indent=2, default=str) + "\n")

    def get(self, job_id: str) -> WorkspaceJob:
        path = self.jobs_root / f"{job_id}.json"
        if not path.is_file():
            raise ValueError(f"training job not found: {job_id}")
        return WorkspaceJob.model_validate(json.loads(path.read_text()))

    def cancel(self, job_id: str) -> WorkspaceJob:
        job = self.get(job_id)
        cancelled = job.transition(TrainingJobStatus.CANCELLED, "cancelled by researcher")
        self.save(cancelled)
        return cancelled


def job_response(job: WorkspaceJob) -> FineTuningJobResponse:
    return FineTuningJobResponse(
        job_id=job.job_id,
        status=job.status.value,
        dataset_version=job.dataset_version,
        model_version=job.model_version,
        language_slices=job.language_slices,
        failure_reason=job.failure_reason,
        artifact_refs=job.artifact_refs,
        mlx_lm_version=job.mlx_lm_version,
        training_command=job.training_command,
        unified_memory_mb=job.unified_memory_mb,
    )


def _mlx_command(request: FineTuningJobRequest, adapter_path: Path) -> str:
    return (
        f"mlx_lm.lora --model {request.base_model} --train --data {request.dataset_version} "
        f"--seed {request.seed} --adapter-path {adapter_path}"
    )