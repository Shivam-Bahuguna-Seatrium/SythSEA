from synthsea.paper.models import VenueFormat, VenueProfile, VenueStatus


def make_profile(format_family: VenueFormat = VenueFormat.MANUAL_REVIEW) -> VenueProfile:
    return VenueProfile(
        venue_id="regicon-2026",
        venue_name="RegiCON 2026",
        requirements_source="fixture://cfp",
        accessed_at="2026-08-13",
        format_family=format_family,
        template_reference="fixture://template",
        page_limit=10,
        author_mode="anonymous",
        required_sections=["abstract", "methods"],
        reference_style="springer",
        anonymization_rule="anonymous",
        version="v1",
    )


def test_venue_profile_can_be_approved_only_after_review() -> None:
    profile = make_profile()
    assert profile.status is VenueStatus.DRAFT
    reviewed = profile.model_copy(update={"status": VenueStatus.APPROVED})
    assert reviewed.status is VenueStatus.APPROVED
