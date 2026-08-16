import platform

from synthsea.api.schemas.workbench import FineTuningJobRequest
from synthsea.workspace.jobs import WorkspaceJobStore
from synthsea.workspace.mlx_training import MlxTrainingRunner


def test_non_macos_mlx_job_becomes_blocked_with_reason(tmp_path) -> None:
    store = WorkspaceJobStore(tmp_path)
    job = store.create(
        FineTuningJobRequest(
            dataset_version="fixture:v1",
            split_version="split:v1",
            language_slices=["singlish"],
            base_model="mlx-community/model",
            model_version="v1",
            model_license="Apache-2.0",
            seed=13,
            objective="sft",
        )
    )
    finished = MlxTrainingRunner(store).run(job.job_id)

    if platform.system() != "Darwin":
        assert finished.status == "blocked"
        assert "Apple Silicon" in finished.failure_reason