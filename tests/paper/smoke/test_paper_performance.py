from time import perf_counter

from synthsea.paper.claims import validate_claims
from synthsea.paper.models import ClaimStatus, PaperClaim
from synthsea.paper.sections import assemble_sections
from synthsea.paper.venue import resolve_template_family


def test_paper_validation_handles_ten_thousand_items() -> None:
    start = perf_counter()
    claims = [
        PaperClaim(
            claim_id=f"claim-{index}",
            claim_text="fixture claim",
            claim_type="numerical",
            status=ClaimStatus.VERIFIED,
            evidence_refs=["artifact-1"],
        )
        for index in range(10_000)
    ]
    validation = validate_claims(claims)
    sections = assemble_sections({"results": "fixture"})
    assert len(validation.verified_claim_ids) == 10_000
    assert len(sections) == 16
    assert resolve_template_family("springer_lncs").value == "springer_lncs"
    assert perf_counter() - start < 60
