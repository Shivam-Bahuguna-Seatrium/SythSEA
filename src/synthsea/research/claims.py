"""Claim-to-evidence validation."""

from __future__ import annotations

from synthsea.research.models import (
    ClaimEvidenceLink,
    ClaimEvidenceStatus,
    EvidenceRecord,
    EvidenceState,
    SourceRecord,
    SourceStatus,
)


def validate_claim_links(
    claims: list[ClaimEvidenceLink],
    evidence: list[EvidenceRecord],
    sources: list[SourceRecord],
) -> tuple[list[ClaimEvidenceLink], list[str]]:
    evidence_by_id = {record.evidence_id: record for record in evidence}
    source_by_id = {source.source_id: source for source in sources}
    validated: list[ClaimEvidenceLink] = []
    blockers: list[str] = []
    for claim in claims:
        linked_evidence = [evidence_by_id.get(identifier) for identifier in claim.evidence_ids]
        linked_sources = [source_by_id.get(identifier) for identifier in claim.source_ids]
        if any(record is None for record in linked_evidence) or any(
            source is None for source in linked_sources
        ):
            status = ClaimEvidenceStatus.MISSING
        elif any(
            record.status is not EvidenceState.VERIFIED
            for record in linked_evidence
            if record
        ):
            status = ClaimEvidenceStatus.BLOCKED
        elif any(
            source.verification_status is not SourceStatus.VERIFIED
            for source in linked_sources
            if source
        ):
            status = ClaimEvidenceStatus.BLOCKED
        elif not claim.evidence_ids and not claim.source_ids:
            status = ClaimEvidenceStatus.UNSUPPORTED
        else:
            status = ClaimEvidenceStatus.VERIFIED
        if status is not ClaimEvidenceStatus.VERIFIED:
            blockers.append(f"claim:{claim.claim_id}:{status.value}")
        validated.append(claim.model_copy(update={"status": status}))
    return validated, blockers