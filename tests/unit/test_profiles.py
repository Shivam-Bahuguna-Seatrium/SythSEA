from datetime import UTC, datetime

import pytest

from synthsea.profiles.models import LanguageProfile
from synthsea.profiles.validation import approve_profile


def test_profile_requires_approval_before_generation() -> None:
    profile = LanguageProfile(
        profile_id="singlish",
        display_name="Singapore English / Singlish",
        language_or_variety="Singapore English and Singlish",
        region="Singapore",
        script_or_orthography="Latin",
        inclusion_rules=["Singapore context"],
        cultural_context="Singapore",
        code_switching_notes="Explicit English mixing",
        resource_limitations="Documented in review",
    )
    assert profile.is_generation_eligible() is False

    approved = approve_profile(
        profile,
        reviewer_role="qualified_language_reviewer",
        validated_at=datetime.now(UTC),
    )
    assert approved.is_generation_eligible() is True
    assert approved.validated_by_role == "qualified_language_reviewer"


def test_profile_rejects_empty_inclusion_rules() -> None:
    with pytest.raises(ValueError):
        LanguageProfile(
            profile_id="bad",
            display_name="Bad",
            language_or_variety="Bad",
            region="Singapore",
            script_or_orthography="Latin",
            inclusion_rules=[],
            cultural_context="Singapore",
            code_switching_notes="Notes",
            resource_limitations="Known",
        )
