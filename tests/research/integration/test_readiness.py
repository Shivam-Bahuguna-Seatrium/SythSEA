from synthsea.research.dossier import build_dossier
from synthsea.research.readiness import build_readiness


def test_empty_evidence_blocks_citations_and_reproducibility() -> None:
    dossier, _ = build_dossier([])
    readiness = build_readiness(dossier.dossier_id, dossier, [], [], [])

    assert readiness.release_status == "blocked"
    assert readiness.citation_status == "blocked"
    assert readiness.reproducibility_status == "blocked"
    assert "ethics_review_not_recorded" in readiness.blocking_issues