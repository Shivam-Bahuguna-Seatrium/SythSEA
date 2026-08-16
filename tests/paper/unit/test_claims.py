from synthsea.paper.claims import validate_claims
from synthsea.paper.models import ClaimStatus, PaperClaim


def test_claim_without_evidence_is_blocked() -> None:
    claims = [
        PaperClaim(
            claim_id="claim-1",
            claim_text="Unsupported number",
            claim_type="numerical",
            status=ClaimStatus.VERIFIED,
        )
    ]
    result = validate_claims(claims)
    assert result.blocked_claim_ids == ["claim-1"]
