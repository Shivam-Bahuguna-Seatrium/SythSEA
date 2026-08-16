from synthsea.paper.claims import validate_claims
from synthsea.paper.models import ClaimStatus, PaperClaim
from synthsea.paper.renderer import render_manuscript
from synthsea.paper.sections import assemble_sections


def test_unsupported_claim_is_not_rendered_as_asserted_result() -> None:
    claim = PaperClaim(
        claim_id="claim-1",
        claim_text="Unsupported result",
        claim_type="numerical",
        status=ClaimStatus.UNSUPPORTED,
    )
    assert validate_claims([claim]).blocked_claim_ids == ["claim-1"]
    manuscript = render_manuscript(assemble_sections({"results": "[MISSING EVIDENCE]"}))
    assert "[MISSING EVIDENCE]" in manuscript
