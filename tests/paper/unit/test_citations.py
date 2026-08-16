from synthsea.paper.citations import BibliographyEntry, render_bibtex, validate_bibliography


def test_citation_validation_reports_unused_entries() -> None:
    entry = BibliographyEntry("key", "Title", ("Author",), 2026, "Venue", "doi:1", "fixture")
    assert "unused:key" in validate_bibliography([entry])
    assert "@article{key" in render_bibtex([entry])
