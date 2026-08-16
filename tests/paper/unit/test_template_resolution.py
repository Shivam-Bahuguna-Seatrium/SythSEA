import pytest

from synthsea.paper.models import VenueFormat
from synthsea.paper.venue import resolve_template_family


def test_template_resolution_preserves_manual_review() -> None:
    assert resolve_template_family("unknown-template") is VenueFormat.MANUAL_REVIEW


def test_template_conflict_is_rejected() -> None:
    with pytest.raises(ValueError, match="conflict"):
        resolve_template_family("springer_lncs", "springer_nature")
