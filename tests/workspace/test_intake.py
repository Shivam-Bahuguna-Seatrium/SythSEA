from synthsea.api.schemas.workbench import DatasetIntakeRequest
from synthsea.workspace.intake import create_intake


def test_intake_blocks_missing_license_and_preserves_issue() -> None:
    result = create_intake(DatasetIntakeRequest(dataset={}, record_source="fixture"))

    assert result.validation_status == "blocked"
    assert result.issues