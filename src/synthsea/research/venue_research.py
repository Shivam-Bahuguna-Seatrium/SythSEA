"""Conservative checks for official venue source records."""

from __future__ import annotations

from synthsea.paper.models import VenueStatus
from synthsea.research.models import SourceRecord, SourceStatus, SourceType


def venue_status(sources: list[SourceRecord], venue_name: str) -> tuple[VenueStatus, list[str]]:
    official = [
        source
        for source in sources
        if source.source_type is SourceType.OFFICIAL_VENUE
        and venue_name.lower() in source.title.lower() + source.relevance.lower()
    ]
    verified = [
        source for source in official if source.verification_status is SourceStatus.VERIFIED
    ]
    unresolved: list[str] = []
    if not official:
        unresolved.append("official_venue_source_missing")
    elif not verified:
        unresolved.append("official_venue_source_not_verified")
    if len({source.doi_or_url for source in verified}) > 1:
        return VenueStatus.CONFLICTED, ["conflicting_verified_venue_sources"]
    return (VenueStatus.APPROVED if not unresolved else VenueStatus.DRAFT), unresolved