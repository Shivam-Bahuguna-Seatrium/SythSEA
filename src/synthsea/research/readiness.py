"""Release-readiness aggregation for research report packages."""

from __future__ import annotations

from synthsea.paper.models import VenueStatus
from synthsea.research.claims import validate_claim_links
from synthsea.research.evidence import coverage
from synthsea.research.models import (
    ClaimEvidenceLink,
    DossierStatus,
    EvidenceRecord,
    EvidenceState,
    ReadinessReport,
    ResearchDossier,
    SourceRecord,
    SourceStatus,
)
from synthsea.research.reproducibility import reproducibility_status


def build_readiness(
    package_id: str,
    dossier: ResearchDossier,
    claims: list[ClaimEvidenceLink],
    evidence: list[EvidenceRecord],
    sources: list[SourceRecord],
    venue_approved: bool = False,
    ethics_reviewed: bool = False,
) -> ReadinessReport:
    blockers: list[str] = []
    warnings: list[str] = []
    if dossier.status is not DossierStatus.APPROVED:
        blockers.append("dossier_not_approved")
    if not venue_approved:
        blockers.append("venue_not_approved")
    if not evidence:
        blockers.append("evidence_missing")
    if any(record.status is not EvidenceState.VERIFIED for record in evidence):
        blockers.append("evidence_not_verified")
    validated_claims, claim_blockers = validate_claim_links(claims, evidence, sources)
    del validated_claims
    blockers.extend(claim_blockers)
    verified_sources = [
        source for source in sources if source.verification_status is SourceStatus.VERIFIED
    ]
    citation_status = "verified" if verified_sources else "blocked"
    if citation_status == "blocked":
        blockers.append("citations_not_verified")
    repro_status, repro_blockers = reproducibility_status(evidence)
    if repro_status != "verified":
        blockers.append("reproducibility_incomplete")
        warnings.extend(repro_blockers)
    ethics_status = "reviewed" if ethics_reviewed else "blocked"
    if not ethics_reviewed:
        blockers.append("ethics_review_not_recorded")
    venue_status = VenueStatus.APPROVED.value if venue_approved else VenueStatus.DRAFT.value
    return ReadinessReport(
        package_id=package_id,
        blocking_issues=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
        evidence_coverage=coverage(evidence),
        citation_status=citation_status,
        reproducibility_status=repro_status,
        ethics_status=ethics_status,
        venue_status=venue_status,
        release_status="ready" if not blockers else "blocked",
    )