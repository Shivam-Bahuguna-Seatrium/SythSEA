from synthsea.research.dossier import build_dossier
from synthsea.research.matrix import build_matrix
from synthsea.research.package import write_research_package
from synthsea.research.readiness import build_readiness


def test_fixture_report_package_contains_readiness_and_manuscript(tmp_path) -> None:
    dossier, _ = build_dossier([])
    matrix = build_matrix(dossier)
    readiness = build_readiness(dossier.dossier_id, dossier, [], [], [])

    package = write_research_package(tmp_path, dossier, matrix, [], [], readiness)

    assert (package / "manuscript.tex").is_file()
    assert (package / "readiness.json").is_file()
    assert 'MISSING EVIDENCE' in (package / "manuscript.tex").read_text()
    assert readiness.release_status == "blocked"