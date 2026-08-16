"""Venue and paper-readiness checks."""

from __future__ import annotations

from dataclasses import dataclass, field

from synthsea.paper.models import VenueProfile, VenueStatus


@dataclass(frozen=True)
class ComplianceResult:
    blocking_issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    release_status: str = "blocked"


def validate_venue(profile: VenueProfile, present_sections: list[str]) -> ComplianceResult:
    issues: list[str] = []
    required = set(profile.required_sections)
    if not required.issubset(present_sections):
        issues.append("missing_required_sections")
    if profile.status is not VenueStatus.APPROVED:
        issues.append("venue_not_approved")
    return ComplianceResult(
        blocking_issues=issues,
        release_status="ready" if not issues else "blocked",
    )
