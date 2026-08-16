from synthsea.paper.compliance import validate_venue
from tests.paper.contract.test_venue_profile import make_profile


def test_readiness_report_blocks_unapproved_venue() -> None:
    result = validate_venue(make_profile(), ["abstract", "methods"])
    assert result.release_status == "blocked"
    assert "venue_not_approved" in result.blocking_issues
