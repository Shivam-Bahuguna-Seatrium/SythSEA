"""Claim-to-evidence validation."""

from __future__ import annotations

from dataclasses import dataclass

from synthsea.paper.models import PaperClaim


@dataclass(frozen=True)
class ClaimValidation:
    blocked_claim_ids: list[str]
    verified_claim_ids: list[str]


def validate_claims(claims: list[PaperClaim]) -> ClaimValidation:
    blocked: list[str] = []
    verified: list[str] = []
    for claim in claims:
        if claim.can_render_as_result():
            verified.append(claim.claim_id)
        else:
            blocked.append(claim.claim_id)
    return ClaimValidation(blocked_claim_ids=blocked, verified_claim_ids=verified)
