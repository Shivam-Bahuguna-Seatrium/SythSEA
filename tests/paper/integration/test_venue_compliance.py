from synthsea.paper.compliance import validate_venue
from tests.paper.contract.test_venue_profile import make_profile


def test_venue_compliance_blocks_missing_required_sections() -> None:
    profile = make_profile().model_copy(update={"required_sections": ["abstract", "methods"]})
    result = validate_venue(profile, present_sections=["abstract"])
    assert result.release_status == "blocked"
    assert "missing_required_sections" in result.blocking_issues
