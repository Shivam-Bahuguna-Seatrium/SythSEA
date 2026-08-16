"""Local MLX-LM job execution for Apple Silicon workstations."""

from __future__ import annotations

import platform
import shutil
import subprocess

from synthsea.workspace.jobs import WorkspaceJobStore
from synthsea.workspace.models import TrainingJobStatus, WorkspaceJob


class MlxTrainingRunner:
    """Execute one auditable MLX-LM command outside the request lifecycle."""

    def __init__(self, store: WorkspaceJobStore) -> None:
        self.store = store

    def run(self, job_id: str) -> WorkspaceJob:
        job = self.store.get(job_id)
        if job.status is not TrainingJobStatus.QUEUED:
            return job
        if platform.system() != "Darwin":
            return self._block(
                job, "MLX-LM fine-tuning requires an Apple Silicon macOS workstation"
            )
        executable = shutil.which("mlx_lm.lora")
        if executable is None:
            return self._block(job, "Install mlx-lm before starting this fine-tuning job")
        running = job.transition(TrainingJobStatus.RUNNING)
        self.store.save(running)
        log_path = self.store.jobs_root / f"{job.job_id}.log"
        try:
            with log_path.open("w", encoding="utf-8") as log_file:
                result = subprocess.run(
                    running.training_command.split(),
                    check=False,
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
        except OSError as error:
            failed = running.transition(TrainingJobStatus.FAILED, str(error))
            self.store.save(failed)
            return failed
        if result.returncode != 0:
            failed = running.transition(
                TrainingJobStatus.FAILED, f"mlx_lm.lora exited with status {result.returncode}"
            )
            self.store.save(failed)
            return failed
        succeeded = running.transition(TrainingJobStatus.SUCCEEDED)
        succeeded = succeeded.model_copy(
            update={
                "artifact_refs": [
                    f"log:{log_path}",
                    f"checkpoint:reports/workspace/jobs/{job.job_id}-checkpoint",
                ]
            }
        )
        self.store.save(succeeded)
        return succeeded

    def _block(self, job: WorkspaceJob, reason: str) -> WorkspaceJob:
        blocked = job.transition(TrainingJobStatus.BLOCKED, reason)
        self.store.save(blocked)
        return blocked