from synthsea.api.schemas.workbench import FineTuningJobRequest
from synthsea.workspace.jobs import WorkspaceJobStore


def test_mlx_job_records_command_and_model_license(tmp_path) -> None:
    job = WorkspaceJobStore(tmp_path).create(
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

    assert job.status == "queued"
    assert "mlx_lm.lora" in job.training_command


def test_mlx_job_prepares_an_8b_model_and_adapter_output(tmp_path) -> None:
    job = WorkspaceJobStore(tmp_path).create(
        FineTuningJobRequest(
            dataset_version="fixture:v1",
            split_version="split:v1",
            language_slices=["singlish"],
            base_model="mlx-community/Qwen3-8B-4bit",
            model_version="qwen3-8b-synthsea",
            model_license="Apache-2.0",
            seed=13,
            objective="sft",
        )
    )

    assert "mlx-community/Qwen3-8B-4bit" in job.training_command
    assert "--train" in job.training_command
    assert f"--adapter-path {tmp_path / 'jobs' / job.job_id / 'adapter'}" in job.training_command


def test_job_store_lists_persisted_history_newest_first(tmp_path) -> None:
    store = WorkspaceJobStore(tmp_path)
    first = store.create(
        FineTuningJobRequest(dataset_version="fixture:v1", split_version="split:v1", language_slices=["singlish"], base_model="mlx-community/model", model_version="first", model_license="Apache-2.0", seed=13, objective="sft")
    )
    second = store.create(
        FineTuningJobRequest(dataset_version="fixture:v1", split_version="split:v1", language_slices=["malay"], base_model="mlx-community/model", model_version="second", model_license="Apache-2.0", seed=14, objective="sft")
    )

    assert [job.job_id for job in store.list()] == [second.job_id, first.job_id]
    assert job.model_license == "Apache-2.0"