from synthsea.research.dossier import build_dossier


def test_empty_dossier_preserves_unresolved_venue() -> None:
    dossier, questions = build_dossier([])

    assert dossier.status == "blocked"
    assert "official_venue_source_missing" in dossier.unresolved_items
    assert len(questions) == 3