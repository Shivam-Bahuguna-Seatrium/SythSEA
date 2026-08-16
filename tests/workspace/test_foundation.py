import pytest

from synthsea.config.schemas import AccessClass
from synthsea.workspace.access import can_include_in_public_export, require_public_exportable
from synthsea.workspace.models import TrainingJobStatus, WorkspaceJob


def test_restricted_artifacts_are_excluded_from_public_export() -> None:
    assert can_include_in_public_export(AccessClass.PUBLIC)
    assert not can_include_in_public_export(AccessClass.RESTRICTED)
    with pytest.raises(ValueError, match="cannot be included"):
        require_public_exportable(AccessClass.PRIVATE)


def test_workspace_job_rejects_invalid_state_transition() -> None:
    job = WorkspaceJob(
        job_id="mlx-job",
        status=TrainingJobStatus.SUCCEEDED,
        dataset_version="fixture:v1",
        split_version="split:v1",
        language_slices=["singlish"],
        base_model="mlx-community/model",
        model_version="v1",
        model_license="test",
        seed=13,
        objective="sft",
    )

    with pytest.raises(ValueError, match="cannot transition"):
        job.transition(TrainingJobStatus.CANCELLED)