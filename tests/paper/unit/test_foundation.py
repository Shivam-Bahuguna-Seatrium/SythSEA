from pathlib import Path

from synthsea.config.schemas import AccessClass
from synthsea.paper.contracts import validate_paper_contract
from synthsea.paper.models import ClaimStatus, PaperArtifact, PaperClaim, VenueFormat, VenueProfile


def test_paper_models_and_contracts_validate() -> None:
    venue = VenueProfile(
        venue_id="regicon-2026",
        venue_name="RegiCON 2026",
        requirements_source="fixture://cfp",
        accessed_at="2026-08-13",
        format_family=VenueFormat.MANUAL_REVIEW,
        template_reference="fixture://template",
        page_limit=10,
        author_mode="anonymous",
        required_sections=["abstract", "methods"],
        reference_style="springer",
        anonymization_rule="anonymous",
        version="v1",
    )
    assert venue.status.value == "draft"
    claim = PaperClaim(
        claim_id="claim-1",
        claim_text="A verified result",
        claim_type="numerical",
        status=ClaimStatus.VERIFIED,
        evidence_refs=["artifact-1"],
    )
    assert claim.can_render_as_result()
    artifact = PaperArtifact(
        artifact_id="table-1",
        title="Results",
        source_refs=["artifact-1"],
        transformation="fixture",
        version="v1",
        access_class=AccessClass.PUBLIC,
        output_path="tables/results.tex",
    )
    assert artifact.access_class is AccessClass.PUBLIC
    validate_paper_contract(
        venue.model_dump(mode="json"),
        Path("specs/002-springer-paper-package/contracts/venue-profile.schema.json"),
    )
