"""Venue-profile loading and explicit template resolution."""

from __future__ import annotations

from synthsea.paper.models import VenueFormat, VenueProfile


def resolve_template_family(primary: str, secondary: str | None = None) -> VenueFormat:
    if secondary is not None and primary != secondary:
        raise ValueError("template conflict requires manual resolution")
    mapping = {
        "springer_lncs": VenueFormat.SPRINGER_LNCS,
        "springer_nature": VenueFormat.SPRINGER_NATURE,
        "venue_specific": VenueFormat.VENUE_SPECIFIC,
        "non_springer": VenueFormat.NON_SPRINGER,
    }
    return mapping.get(primary, VenueFormat.MANUAL_REVIEW)


def approve_venue(profile: VenueProfile) -> VenueProfile:
    if profile.format_family is VenueFormat.MANUAL_REVIEW:
        raise ValueError("manual template resolution is required")
    return profile.model_copy(update={"status": "approved"})
