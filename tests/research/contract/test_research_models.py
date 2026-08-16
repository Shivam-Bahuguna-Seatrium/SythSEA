from datetime import UTC, datetime

import pytest

from synthsea.research.languages import aggregate_is_complete
from synthsea.research.models import (
    EvidenceRecord,
    EvidenceState,
    ExperimentRequirement,
    ResearchQuestion,
)


def test_research_question_rejects_unknown_language_slice() -> None:
    with pytest.raises(ValueError, match="unknown language slices"):
        ResearchQuestion(
            question_id="rq",
            question="Question",
            hypotheses=["Hypothesis"],
            language_slices=["unknown"],
        )


def test_aggregate_requires_all_four_language_slices() -> None:
    assert not aggregate_is_complete(["singlish", "malay"])
    assert aggregate_is_complete(["singlish", "malay", "tamil", "singapore_mandarin"])


def test_experiment_requirement_requires_command_and_artifact() -> None:
    with pytest.raises(ValueError):
        ExperimentRequirement(
            requirement_id="req",
            question_id="rq",
            condition_id="baseline",
            dataset_versions=["fixture:v1"],
            language_slices=["singlish"],
            metrics=["quality"],
            statistical_method="pending",
            command="",
            expected_artifacts=[],
        )


def test_evidence_record_rejects_restricted_public_state() -> None:
    with pytest.raises(ValueError, match="restricted evidence"):
        EvidenceRecord(
            evidence_id="evidence",
            experiment_id="experiment",
            artifact_path="result.json",
            artifact_type="result",
            checksum="0" * 64,
            language_slice="singlish",
            condition_id="baseline",
            access_class="public",
            status=EvidenceState.RESTRICTED,
            provenance_refs=["experiment"],
            environment={"python": "3.12"},
        )


def test_datetime_import_is_available_for_fixture_metadata() -> None:
    assert datetime.now(UTC).tzinfo is not None