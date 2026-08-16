from datetime import UTC, datetime

from synthsea.profiles.models import LanguageProfile
from synthsea.profiles.validation import approve_profile


def test_approved_profile_contains_required_validation_context() -> None:
    profile = LanguageProfile(
        profile_id="tamil",
        display_name="Singapore Tamil / Tamil",
        language_or_variety="Tamil",
        region="Singapore",
        script_or_orthography="Tamil",
        inclusion_rules=["Singapore context"],
        cultural_context="Singapore",
        code_switching_notes="Explicit English mixing",
        resource_limitations="Documented",
    )
    approved = approve_profile(profile, "qualified_language_reviewer", datetime.now(UTC))
    assert approved.is_generation_eligible()
    assert approved.script_or_orthography == "Tamil"
    assert approved.resource_limitations == "Documented"
